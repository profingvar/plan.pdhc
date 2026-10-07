"""#786 item 2 — "for concepts with no reference to canonical libs assume local".

`Concept.canonical_lib` is `nullable=False`, and before this THREE independent
paths each refused rather than defaulting:

  * the web form (`concepts/create.html`): an empty `Select...` option, `required`
  * the JSON API (`app/api/concepts.py`): 400 "canonical_lib are required"
  * the CSV importer (`app/services/concept_importer.py`): ValueError

So an author writing a purely local concept had to know to pick "local" out of
eight libraries, on every path, every time. The rule is the opposite: a term
with no reference into a published vocabulary IS local. That is a statement
about what the concept is, not a field someone forgot.

This module is the ONE place that decides it. The three callers resolve through
`resolve_or_local`, so the default cannot drift between the form, the API and
the importer -- the same reasoning that gave sso.pdhc a single CSV column
contract in #784, after its export and import had disagreed for months.

Measured on the live database 2026-10-07, the DATA already obeys the rule:
loinc 35 concepts / 0 missing a reference number, snomed 21 / 0, atc 9 / 0,
local 34 / 2 missing. Both reference-less concepts were already local. So this
closes an authoring gap; it is not a migration.
"""
from __future__ import annotations

from app import db
from app.models.concept_models import CanonicalLib

# The name is the identity here: `canonical_lib_name` is unique, and the live
# row has been called "local" since before this change. Matching is
# case-insensitive so "Local" from a CSV resolves to the same row rather than
# creating a second one.
LOCAL_LIB_NAME = "local"
LOCAL_LIB_URL = "https://plan.pdhc.se"
LOCAL_LIB_DISPLAY = "Local (no canonical vocabulary)"


def find_local_lib() -> CanonicalLib | None:
    """The local library row, or None. Does not create anything."""
    return (CanonicalLib.query
            .filter(db.func.lower(CanonicalLib.canonical_lib_name)
                    == LOCAL_LIB_NAME)
            .first())


def ensure_local_lib(author: str | None = None) -> CanonicalLib:
    """The local library row, creating it if this database has none.

    Creating a terminology library as a side effect of saving a concept would
    normally be too clever. It is right here for one reason: the rule makes
    `local` definitionally required, and nothing seeds it. It exists on the
    production database only because somebody once added it through the lookup
    table UI, so a fresh deploy would have the default resolve to nothing and
    every reference-less concept would fail exactly as before.

    Idempotent, and `canonical_lib_name` is unique, so a race loses the insert
    rather than producing a duplicate.
    """
    lib = find_local_lib()
    if lib is not None:
        return lib
    lib = CanonicalLib(
        canonical_lib_name=LOCAL_LIB_NAME,
        canonical_lib_display_text=LOCAL_LIB_DISPLAY,
        canonical_lib_url=LOCAL_LIB_URL,
        author=author or "system (#786 default)",
    )
    db.session.add(lib)
    db.session.flush()          # so the guid is available to the caller now
    return lib


def resolve_or_local(value: str | None, *, author: str | None = None) -> str:
    """The canonical_lib GUID to store for `value`, defaulting to local.

    `value` may be a guid, a library name, or empty/None. Empty means local --
    that is the whole point. An unrecognised NON-empty value is returned
    unchanged so the caller's own validation still reports it: silently
    rewriting a misspelled "snomd" to local would turn a typo into a wrong
    terminology binding, which is far worse than an error message.
    """
    if value is not None and str(value).strip():
        v = str(value).strip()
        by_guid = CanonicalLib.query.filter_by(guid=v).first()
        if by_guid is not None:
            return by_guid.guid
        by_name = (CanonicalLib.query
                   .filter(db.func.lower(CanonicalLib.canonical_lib_name)
                           == v.lower())
                   .first())
        if by_name is not None:
            return by_name.guid
        return v                # unknown: hand it back, let the caller refuse
    return ensure_local_lib(author=author).guid
