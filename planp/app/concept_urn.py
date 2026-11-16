"""THE concept reference format, owned by plan.pdhc (#942).

plan.pdhc mints the concept GUIDs, so plan owns how they are referenced:

    concept-urn   = "urn:pdhc:concept/" guid          ; code_canonical, canonical form
    concept-coding= system "urn:pdhc:concept" + code guid
    legacy-url    = "http" ["s"] "://" host "/api/v1/concepts/" guid   ; accepted on READ only
    guid          = 8HEXDIG "-" 4HEXDIG "-" 4HEXDIG "-" 4HEXDIG "-" 12HEXDIG

Readers return the GUID LOWER-CASE (plan writes uuid4 lower-case; measured
2026-11-16: every stored value in cdr1/2/3 already is) and return None for
anything else -- a termbank URI, a non-GUID tail, whitespace. None matters:
under a disclosure block a point with no concept stays HIDDEN.

Consumers do not import this. They implement it and prove it against
``conformance/concept_urn_cases.json``, keeping a byte-identical copy in their
tests; ``tools/check_canonical_uri_conformance.py`` fails on a drifted copy.
"""
from __future__ import annotations

import re

SYSTEM = "urn:pdhc:concept"
PREFIX = SYSTEM + "/"
_GUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
_URN_RE = re.compile(rf"^urn:pdhc:concept/({_GUID})$")
_LEGACY_RE = re.compile(rf"^https?://[^/\s]+/api/v1/concepts/({_GUID})$")
_GUID_RE = re.compile(rf"^{_GUID}$")


def build(guid: str) -> str:
    if not isinstance(guid, str) or not _GUID_RE.match(guid):
        raise ValueError(f"{guid!r} is not a concept GUID")
    return PREFIX + guid.lower()


def guid_of(value: str | None) -> str | None:
    if not isinstance(value, str):
        return None
    m = _URN_RE.match(value) or _LEGACY_RE.match(value)
    return m.group(1).lower() if m else None
