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
from app.models.concept_models import (LOCAL_CODESYSTEM_ID, CanonicalLib,
                                       fhir_canonical_url)

# The name is the identity here: `canonical_lib_name` is unique, and the live
# row has been called "local" since before this change. Matching is
# case-insensitive so "Local" from a CSV resolves to the same row rather than
# creating a second one.
LOCAL_LIB_NAME = "local"
#: #923: was the bare `https://plan.pdhc.se`, which is plan's BASE URL and not
#: an identifier for anything. plan already publishes its local concept set as
#: the CodeSystem `plan-pdhc-local` at this canonical url (ADR D3) — measured
#: live 2026-11-04, version 2, 99 concepts — so plan disagreed with itself, the
#: same way it did about snomed. 34 of 99 concepts bind to `local`, and this
#: value is what they get as `compose.include[].system`.
#:
#: DERIVED, not written out. My first version hardcoded the string, and
#: `test_no_other_file_hardcodes_plan_fhir_url` caught it — there is one helper
#: for plan's own canonical urls and this is not allowed to be a second source
#: of the same fact. Better anyway: it follows PLAN_BASE if that ever moves.
LOCAL_LIB_URL = fhir_canonical_url('CodeSystem', LOCAL_CODESYSTEM_ID)
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


# ---------------------------------------------------------------------------
# #875 — the canonical URL rule, in one place for the same reason as above
# ---------------------------------------------------------------------------
#
# `canonical_lib_url` is now UNIQUE, and FOUR write paths could set it with
# no check at all: the JSON API create and update (`app/api/lookup_tables.py`)
# and the HTML admin create and update (`app/routes/lookup_tables.py`). Every
# one of them already guarded `canonical_lib_name` for uniqueness — the name
# was protected in two layers and the URL in none, which is how `icd10` came
# to hold `snomed`'s URL in production.
#
# Without these helpers the UNIQUE constraint turns that mistake from a
# silent wrong answer into an IntegrityError 500, which is better but still
# not an answer anyone can act on.

def normalise_lib_url(raw: str | None) -> str | None:
    """`''` and whitespace mean NO url — which is NULL, not an empty string.

    Load-bearing for the UNIQUE constraint. Postgres permits many NULLs under
    one, so any number of libraries may lack a URL; two empty STRINGS, by
    contrast, collide with each other. Without this, the second library saved
    with a blank URL field would be refused as conflicting with the first,
    which is both wrong and baffling.
    """
    value = (raw or "").strip()
    return value or None


def url_conflict(url: str | None, *, exclude_guid: str | None = None):
    """The CanonicalLib already holding ``url``, or None.

    ``exclude_guid`` is the row being edited — without it, every update would
    report the row conflicting with itself.
    """
    if not url:
        return None
    q = CanonicalLib.query.filter_by(canonical_lib_url=url)
    if exclude_guid:
        q = q.filter(CanonicalLib.guid != exclude_guid)
    return q.first()


# ---------------------------------------------------------------------------
# #923 — the canonical_lib_url CONVENTION, in one place for the third time
# ---------------------------------------------------------------------------
#
# #875 made the url UNIQUE and guarded the four write paths. It did not say what
# a url should BE, and the audit found that the three code systems which HAVE a
# registered FHIR URI were published under values that are not them. snomed's
# was the serious one: a human BROWSER address carrying a perspective, a concept
# id, an edition and a language list, emitted as `compose.include[].system` for
# every SNOMED value. A consumer resolving it gets a web page.
#
# Measured 2026-11-04. The platform already uses the registered forms
# overwhelmingly — `http://loinc.org` in 39 files, `http://snomed.info/sct` in
# 23 including PLAN'S OWN source and test suite — so plan's terminology registry
# disagreed with plan's own code. Live confirmation: the FHIR Device ips created
# from an alert implant assertion the same day carries
# `system = "http://snomed.info/sct"`.
#
# WHY A DERIVED RULE AND NOT A BLOCKLIST. The obvious guard is "reject a url
# with a query string", because an identifier does not need one. It catches
# snomed's and nothing else: `kva`'s old value,
# `https://verktyg.internetmedicin.se/koder/kva`, is a third-party browser tool
# with NO query string. A blocklist of such hosts would be brittle and would
# always be one host behind. So the rule is positive instead: for a library we
# have decided about, there is exactly one acceptable url, derived.

#: Code systems with a registered FHIR URI. The external authority decides
#: these, not us; they are written out because that is the whole point.
REGISTERED_SYSTEM_URLS: dict[str, str] = {
    "snomed": "http://snomed.info/sct",
    "loinc": "http://loinc.org",
    "atc": "http://www.whocc.no/atc",
}

#: Libraries published under termbank's CodeSystem space because they have no
#: registered FHIR URI. `kva` JOINED these under #923: its old value was a
#: browser link into a third-party tool, and it is bound by 0 concepts, so the
#: change is free. If KVÅ is ever given a registered URI, move it to
#: REGISTERED_SYSTEM_URLS deliberately rather than editing the data.
TERMBANK_CODESYSTEM_PREFIX = "https://termbank.pdhc.se/CodeSystem/"
TERMBANK_LIBS: frozenset[str] = frozenset({
    "icd10", "icd11-mms", "icf", "socialstyrelsen", "kva",
})


def expected_lib_url(name: str | None) -> str | None:
    """The one url this library must carry, or None when we have not decided.

    None is deliberate and is not a licence: a library nobody has reasoned
    about yet should not be forced into a shape, because we do not know its
    authority. It still has to be identifier-shaped — see
    ``url_convention_error``.
    """
    n = (name or "").strip().lower()
    if not n:
        return None
    if n in REGISTERED_SYSTEM_URLS:
        return REGISTERED_SYSTEM_URLS[n]
    if n == LOCAL_LIB_NAME:
        return LOCAL_LIB_URL
    if n in TERMBANK_LIBS:
        return f"{TERMBANK_CODESYSTEM_PREFIX}{n}"
    return None


def url_convention_error(name: str | None, url: str | None) -> str | None:
    """Why this url may not be stored for this library, or None.

    Two rules, in order:

    1. A url carrying a QUERY STRING or a FRAGMENT is a human browser address,
       not an identifier. This applies to every library including ones we have
       not decided about, because no identifier needs either.
    2. A library we HAVE decided about must carry exactly its decided url.

    An absent url is permitted: ``canonical_lib_url`` is nullable and many
    libraries legitimately have none (#875 relies on that for the UNIQUE
    constraint). Whitespace counts as absent, the same way ``normalise_lib_url``
    treats it — the callers pass through that first, but a helper that only
    holds when its caller is correct is not a helper.
    """
    url = (url or "").strip()
    if not url:
        return None
    # The DELIMITER's presence is the signal, not the parsed value's. `urlsplit`
    # reports `query=''` for a url ending in a bare `?`, which is falsy — so a
    # check on the parsed value lets `https://example.org/cs?` through, and that
    # is still the shape this rule exists to refuse. My own test caught it.
    if "?" in url or "#" in url:
        return (
            "canonical_lib_url must be an identifier, not a browser address: "
            "this one carries a "
            + ("query string" if "?" in url else "fragment")
            + ". A consumer resolves this value as a code system `system`."
        )
    want = expected_lib_url(name)
    if want is not None and url != want:
        return (
            f"canonical_lib_url for {name!r} must be {want!r} (#923). "
            f"Change the convention in app/services/canonical_libs.py if that "
            f"is wrong, rather than the data."
        )
    return None
