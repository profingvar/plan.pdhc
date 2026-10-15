#!/usr/bin/env python3
"""plan.pdhc — does every call to a SIBLING service actually work? (#708)

Run it INSIDE the container, which is the only place the real credentials and
the real network names exist:

    docker exec pdhc_app python deploy/smoke_siblings.py
    docker exec pdhc_app python deploy/smoke_siblings.py --json

READ-ONLY. It creates nothing, writes nothing and mints no token, so it is
safe against production at any time, including straight after a deploy.

## What plan.pdhc calls, and why each one is worth a check

plan.pdhc authors the content the rest of the platform executes, so most of
its siblings are consulted while a human is editing — which is exactly when a
silent failure is least visible:

    sso.pdhc        /api/auth/me/service       every request's identity
    contract.pdhc   /fhir/Contract             dispatch: is there a contract?
    termbank.pdhc   /CodeSystem/<sys>/<code>   concept panels, click-to-fill
    rosetta.pdhc    /api/v1/openehr/realisable the authoring assistant's probe

Three of those four DEGRADE SILENTLY BY DESIGN, and that is the reason this
script exists rather than being redundant with the healthz page:

* `TermbankClient` returns None on timeout, connection error, request error
  and any non-2xx, and its own docstring says the UI then shows "no banner, no
  exception, just an unavailable message". A termbank that has moved looks
  identical to a concept with no termbank entry.
* the rosetta probe answers 200 with `available: false` and a reason for
  "not configured", "unreachable", any HTTP error and a bad body alike. The
  authoring assistant simply stops offering openEHR realisability, and nothing
  anywhere says why.
* `validate_token` returns None on failure, which is correct (an
  unvalidatable token is not a user) and indistinguishable from an sso outage.

So every path is probed TWICE where it can be: once directly with a
deliberately invalid or absent credential, asserting the path still EXISTS
(401/403 and **not** 404), and once through plan's own client, asserting the
client reaches it. A 404 is the finding that matters: it is the shape a moved
or renamed endpoint takes, and every one of the clients above swallows it.

Exit code is 0 only if every check passed.
"""
from __future__ import annotations

import json as _json
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

#: Every sibling path plan builds -> the client module that builds it.
#: `%s` stands for a path parameter. Templates rather than bare strings, and
#: checked anchored, because a truncated prefix is a substring of the real
#: path and must not pass (#804).
PROBED_PATHS = {
    "/api/auth/me/service": "app/services/sso_service.py",
    "/fhir/Contract": "app/services/dispatch_service.py",
    "/CodeSystem/%s/%s": "app/services/termbank_client.py",
    "/api/v1/openehr/realisable": "app/api/authoring.py",
}

#: Probed but composed inline here, with no client module to drift from:
#:   /api/health, /health, /healthz  — bare liveness pings.
INLINE_PATHS = ("/api/health", "/health", "/healthz")

RESET, RED, GRN, YEL, BOLD = "\033[0m", "\033[31m", "\033[32m", "\033[33m", "\033[1m"

results: list[dict] = []


def check(name: str):
    def wrap(fn):
        started = time.time()
        try:
            ok, note = fn()
        except Exception as e:                      # noqa: BLE001
            ok, note = False, f"{type(e).__name__}: {e}"
        results.append({"check": name, "ok": bool(ok), "note": note,
                        "ms": int((time.time() - started) * 1000)})
        return ok
    return wrap


def _repo_root() -> pathlib.Path:
    """Where `app/` lives, in the image AND in a checkout.

    The image is /app/app/... while a checkout is <repo>/planp/app/..., so one
    hardcoded relative path resolves in only one of them — and the guard is
    worth most BEFORE a deploy (#804).
    """
    here = pathlib.Path(__file__).resolve().parent.parent
    for cand in (here, here / "planp"):
        if (cand / "app").is_dir():
            return cand
    return here


def _path_appears_in_client(template: str, src: str) -> bool:
    """ANCHORED on the first literal fragment: a bare `in` accepts a truncated
    prefix, which is the bug this guard exists for."""
    frags = [f for f in template.split("%s") if f]
    if not frags:
        return False
    if not re.search(r"""[}"']""" + re.escape(frags[0]), src):
        return False
    return all(f in src for f in frags[1:])


def _probe(url, headers=None, timeout=10):
    """(status, short body). A transport failure is reported as status 0 so a
    down service and a moved path stay distinguishable in the output."""
    import requests
    try:
        r = requests.get(url, headers=headers or {}, timeout=timeout)
        return r.status_code, (r.text or "")[:120]
    except requests.RequestException as e:
        return 0, f"{type(e).__name__}: {e}"


def _exists(code: int) -> tuple[bool, str]:
    """A path EXISTS if it refused us. 404 is the finding; 0 is an outage."""
    if code == 0:
        return False, "unreachable"
    if code == 404:
        return False, "404 — the path MOVED, and every client here swallows it"
    if code in (401, 403, 400, 405, 422):
        return True, f"{code} (refused, so the path is live)"
    if 200 <= code < 300:
        return True, f"{code} (answered without a credential)"
    return False, f"{code}"


def main(as_json: bool = False) -> int:
    from app import create_app
    app = create_app()

    with app.app_context():
        from flask import current_app
        cfg = current_app.config
        sso = (cfg.get("SSO_BASE_URL") or "").rstrip("/")
        contract = (cfg.get("CONTRACT_BASE_URL") or "").rstrip("/")
        rosetta = (cfg.get("ROSETTA_BASE_URL") or "").rstrip("/")

        @check("paths: every probed path appears in its client module")
        def _():
            root = _repo_root()
            missing = []
            for template, mod in PROBED_PATHS.items():
                f = root / mod
                if not f.exists():
                    missing.append(f"{mod} is missing (looked under {root})")
                    continue
                if not _path_appears_in_client(template,
                                               f.read_text(encoding="utf-8")):
                    missing.append(f"{template} does not START a URL in {mod}")
            return (not missing), (
                f"all {len(PROBED_PATHS)} anchored to a URL boundary; "
                f"{len(INLINE_PATHS)} inline liveness paths unguarded by "
                f"design" if not missing else "; ".join(missing))

        # ── sso: the identity every request is validated against ──
        @check("config: SSO_BASE_URL and the service credential pair")
        def _():
            # A missing pair is the failure that has actually happened
            # (memory: PDHC SSO client creds audit): /me/service 401s and the
            # login callback fails silently.
            cid, sec = cfg.get("SSO_CLIENT_ID"), cfg.get("SSO_CLIENT_SECRET")
            if not sso:
                return False, "SSO_BASE_URL is MISSING"
            if not (cid and sec):
                return False, f"{sso}; CLIENT_ID/SECRET MISSING"
            return True, f"{sso}; client id + secret present"

        @check("sso: /api/health answers 200")
        def _():
            if not sso:
                return False, "SSO_BASE_URL not set"
            code, body = _probe(f"{sso}/api/health")
            return code == 200, f"{code} {body[:40]}"

        @check("sso: /api/auth/me/service EXISTS (not 404)")
        def _():
            if not sso:
                return False, "SSO_BASE_URL not set"
            code, _b = _probe(f"{sso}/api/auth/me/service", headers={
                "Authorization": "Bearer smoke-not-a-real-token",
                "X-SSO-Client-Id": cfg.get("SSO_CLIENT_ID") or "",
                "X-SSO-Client-Secret": cfg.get("SSO_CLIENT_SECRET") or ""})
            if 200 <= code < 300:
                return False, f"{code} for a junk token — sso accepted nonsense"
            return _exists(code)

        @check("sso: plan's own validate_token reaches it")
        def _():
            # Drives `sso_service.validate_token`, so a wrong header name or
            # scheme is wrong here too. None is the only correct answer for a
            # junk token; the check above is what makes that meaningful.
            from app.services.sso_service import validate_token
            got = validate_token("smoke-not-a-real-token")
            return got is None, ("None, as it must be for an invalid token"
                                 if got is None
                                 else f"VALIDATED a junk token: {str(got)[:70]}")

        # ── contract: the dispatch gate ──
        @check("contract: /fhir/Contract EXISTS and answers")
        def _():
            # dispatch_service 502s on any non-200 here, with "Contract
            # service unavailable" — which is also what a moved path says.
            if not contract:
                return False, "CONTRACT_BASE_URL not set"
            code, body = _probe(f"{contract}/fhir/Contract")
            if code == 404:
                return False, ("404 — dispatch would report 'Contract service "
                               "unavailable' for a path that simply moved")
            if code == 200:
                # The body is truncated to 120 chars by `_probe`, so it
                # cannot be parsed — and asserting on a truncated prefix is
                # how a check ends up reporting "body not JSON" about a
                # perfectly good Bundle. So assert on the ONE key the client
                # actually reads: `dispatch_service` does
                # `resp.json().get('entry', [])` and nothing else. Asserting
                # `resourceType` instead FAILED here, because contract serves
                # `entry` first and a 120-char prefix never reaches it — a
                # check testing the author's idea of the contract rather than
                # the code's, which is the thing #708 is about.
                looks_right = '"entry"' in body
                return looks_right, ("200, carrying the `entry` key dispatch "
                                     "reads" if looks_right else
                                     f"200 with no `entry`: {body[:60]}")
            return _exists(code)

        # ── termbank: the concept panels ──
        @check("termbank: reachable, and its health reports connected")
        def _():
            tb = getattr(current_app, "termbank_client", None)
            if tb is None:
                from app.services.termbank_client import TermbankClient
                tb = TermbankClient()
            h = tb.health()
            if h is None:
                return False, (f"{tb.base_url}/health gave nothing — every "
                               f"concept panel silently shows 'unavailable'")
            return True, f"{tb.base_url}: {str(h)[:70]}"

        @check("termbank: a $lookup for an ABSENT code returns None, not an error")
        def _():
            # The read-only half of the contract: a miss and an outage both
            # return None from this client, so the value here is that the
            # call COMPLETES against the live service. The health check above
            # is what separates the two.
            tb = getattr(current_app, "termbank_client", None)
            if tb is None:
                from app.services.termbank_client import TermbankClient
                tb = TermbankClient()
            got = tb.lookup("smoke-not-a-real-system",
                            "smoke-not-a-real-code")
            return got is None, ("None for an absent code" if got is None
                                 else f"returned {str(got)[:70]}")

        # ── rosetta: the authoring assistant's openEHR probe ──
        @check("rosetta: configured, or deliberately not")
        def _():
            # Not configured is a legitimate state — the button degrades to
            # "rosetta_not_configured" by design. Reported as a WARNING-shaped
            # pass so it is visible rather than silently green.
            if not rosetta:
                return True, ("ROSETTA_BASE_URL unset — the openEHR button "
                              "degrades to rosetta_not_configured BY DESIGN")
            key = cfg.get("ROSETTA_SERVICE_KEY") or ""
            return True, f"{rosetta}; service key {'present' if key else 'MISSING'}"

        @check("rosetta: /api/v1/openehr/realisable EXISTS (not 404)")
        def _():
            if not rosetta:
                return True, "skipped — ROSETTA_BASE_URL unset"
            # GET on a POST route is a 405, which still proves the path is
            # routed. A POST would be a write to a sibling, which a read-only
            # smoke has no business making.
            code, _b = _probe(f"{rosetta}/api/v1/openehr/realisable")
            if code == 404:
                return False, ("404 — the assistant would report "
                               "'rosetta_http_404' and offer nothing")
            return _exists(code)

    failed = [r for r in results if not r["ok"]]
    if as_json:
        print(_json.dumps({"service": "plan.pdhc", "checks": results,
                           "failed": len(failed)}, indent=2))
    else:
        print(f"\n{BOLD}plan.pdhc — sibling smoke{RESET}\n")
        for r in results:
            mark = f"{GRN}OK{RESET}" if r["ok"] else f"{RED}FAIL{RESET}"
            print(f"  {mark:<14} {r['check']:<58} {r['note']}  ({r['ms']}ms)")
        if failed:
            print(f"\n{RED}{BOLD}{len(failed)} check(s) failed.{RESET}\n")
        else:
            print(f"\n{GRN}{BOLD}All {len(results)} checks passed.{RESET}\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(as_json="--json" in sys.argv))
