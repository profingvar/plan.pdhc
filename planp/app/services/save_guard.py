"""Fail-closed save enforcement — GA-5 (#521).

Runs the deterministic validators (:mod:`app.services.plandef_validation`) on the
concept/plandef save paths and BLOCKS a save that has ERROR-severity issues.
Warnings pass. An admin/SU can force a save past errors with
``override_validation`` (a form field or JSON key) — the override is written to
the application log as an audit trail. The whole mechanism is gated by
``PLANDEF_VALIDATION_ENFORCED`` (default on; a kill-switch).

Callers build the validator payload and call :func:`guard_concept` /
:func:`guard_plandef`; on a block a :class:`SaveBlocked` is raised carrying the
issues, which the web route renders as a flash and the API returns as HTTP 422.
"""
from __future__ import annotations

from flask import current_app, request, session

from app.services import plandef_validation as v


class SaveBlocked(Exception):
    """Raised when a save is rejected by fail-closed validation."""
    def __init__(self, issues):
        self.issues = issues
        super().__init__("save blocked by validation")

    @property
    def errors(self):
        return [i for i in self.issues if i.severity == v.ERROR]

    def messages(self):
        return [f"{i.code}: {i.message}" for i in self.issues if i.severity == v.ERROR]

    def as_dict(self):
        return {
            "error": "validation_failed",
            "error_count": len(self.errors),
            "issues": [i.to_dict() for i in self.issues],
            "hint": "Fix the errors, or an admin may re-submit with "
                    "override_validation=1 to force the save (audited).",
        }


def _enforced() -> bool:
    return bool(current_app.config.get("PLANDEF_VALIDATION_ENFORCED", True))


def _blob() -> dict:
    return session.get("sso_user") or {}


def _is_admin() -> bool:
    if current_app.config.get("AUTH_DISABLED"):
        return True
    return bool(_blob().get("is_su_admin"))


def _override_requested() -> bool:
    if request.is_json:
        body = request.get_json(silent=True) or {}
        return bool(body.get("override_validation"))
    return (request.form.get("override_validation") or "").strip().lower() in (
        "1", "true", "on", "yes",
    )


def _audit_override(kind: str, errors) -> None:
    blob = _blob()
    who = (blob.get("email") or blob.get("user_guid")
           or ("local-admin" if current_app.config.get("AUTH_DISABLED") else "unknown"))
    current_app.logger.warning(
        "VALIDATION OVERRIDE (#521): %s save forced by %s despite %d error(s): %s",
        kind, who, len(errors), [i.code for i in errors],
    )


def _guard(issues, kind: str):
    """Enforce fail-closed given a list of issues. No-op when disabled or clean;
    audits + allows on admin override; raises SaveBlocked otherwise."""
    errors = [i for i in issues if i.severity == v.ERROR]
    if not errors or not _enforced():
        return
    if _override_requested() and _is_admin():
        _audit_override(kind, errors)
        return
    raise SaveBlocked(issues)


def guard_concept(payload, *, termbank=None):
    _guard(v.validate_concept(payload, termbank=termbank), "concept")


def guard_plandef(payload):
    _guard(v.validate_plandef(payload), "plandef")
