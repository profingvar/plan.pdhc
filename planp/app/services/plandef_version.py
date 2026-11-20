"""A PlanDefinition's version moves when its content does (2026-11-20).

Editing a plan rewrote it in place and kept `version` at whatever the form
sent back, which was the stored value, so MMD_plan stayed 1.0.0 through every
edit. Nothing downstream (sim's output, an analysis, a CarePlan) could say
which version of the plan it was built from.

Rule: if a save changes the plan's content and the editor did not set a
version themselves, the patch level is bumped (1.0.0 -> 1.0.1). A version the
editor typed wins. A save that changes nothing leaves the version alone. A
version string that is not dotted numbers is left as it is, not guessed at.
"""
from __future__ import annotations

import json
import re

#: Fields whose change makes it a different plan. Bookkeeping (dates, fhir_data,
#: the version itself) is not content.
CONTENT_FIELDS = ('title', 'name', 'description', 'status', 'type',
                  'subject_type', 'publisher', 'purpose', 'usage', 'copyright',
                  'form_definition_guid', 'validity_duration')
_JSON_FIELDS = ('goal', 'action')
_SEMVER = re.compile(r'^\s*(\d+)(?:\.(\d+))?(?:\.(\d+))?\s*$')


def _norm_json(raw):
    try:
        value = json.loads(raw) if isinstance(raw, str) else raw
    except (TypeError, ValueError):
        return raw
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def fingerprint(pd) -> str:
    body = {f: getattr(pd, f, None) for f in CONTENT_FIELDS}
    body.update({f: _norm_json(getattr(pd, f, None)) for f in _JSON_FIELDS})
    return json.dumps(body, sort_keys=True, default=str, ensure_ascii=False)


def bump_patch(version: str | None) -> str | None:
    """'1.0.0' -> '1.0.1', '1.1' -> '1.1.1', '2' -> '2.0.1'; None when the
    string is not dotted numbers."""
    m = _SEMVER.match(version or '')
    if not m:
        return None
    major, minor, patch = (int(g) if g is not None else 0 for g in m.groups())
    return f'{major}.{minor}.{patch + 1}'


class Snapshot:
    """Taken before an edit is applied; `settle` decides the version after."""

    def __init__(self, pd):
        self.version = pd.version
        self.fp = fingerprint(pd)

    def settle(self, pd) -> bool:
        """Bump `pd.version` if the content changed and the editor left the
        version as it was. Returns True when it bumped."""
        if (pd.version or '') != (self.version or ''):
            return False                     # the editor chose a version
        if fingerprint(pd) == self.fp:
            return False                     # nothing changed
        bumped = bump_patch(pd.version or '1.0.0')
        if bumped is None:
            return False
        pd.version = bumped
        return True
