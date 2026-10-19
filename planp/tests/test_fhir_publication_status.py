"""#839 — the FHIR resource status must follow the content, not a constant.

All three terminology wrappers hardcoded ``'status': 'active'`` while every one
of plan's 99 Concepts carried ``status='draft'``. A client reading a `$lookup`
got a CodeSystem declaring itself active whose every concept carried the
property ``status = draft``. Both came from this service, and they contradicted
each other.

These tests pin the derivation itself, which is pure, and then the thing that
actually matters: that each endpoint's status CHANGES when the content changes.
A test asserting only `== 'draft'` today would pass just as happily against the
old hardcoded constant if someone reinstated it with a different literal.
"""
from __future__ import annotations

import pytest

from app.api.fhir_helpers import (
    CONCEPT_STATUSES,
    FHIR_PUBLICATION_STATUSES,
    derive_publication_status,
)


# ---------------------------------------------------------------- the rule

@pytest.mark.parametrize("statuses,expected", [
    ([], "draft"),                              # no content claims nothing
    (["draft"], "draft"),
    (["draft", "draft"], "draft"),
    (["active"], "active"),
    (["draft", "active"], "active"),            # one adopted concept is enough
    (["retired", "active"], "active"),
    (["retired"], "retired"),
    (["retired", "retired"], "retired"),
    (["draft", "retired"], "draft"),            # not all retired
])
def test_derivation(statuses, expected):
    assert derive_publication_status(statuses) == expected


def test_production_state_derives_draft():
    """99 concepts, all draft — so the real answer today is draft, not active."""
    assert derive_publication_status(["draft"] * 99) == "draft"


@pytest.mark.parametrize("junk", [
    [None], [""], ["  "], ["DRAFT "], ["unknown"], ["published"], ["Active"],
])
def test_unrecognised_values_cannot_promote(junk):
    """A stray status must not promote a resource.

    `DRAFT ` and `Active` are normalised (trimmed, lowercased) and so count;
    anything outside the three allowed values is ignored rather than trusted.
    """
    got = derive_publication_status(junk)
    assert got in FHIR_PUBLICATION_STATUSES
    if junk in ([None], [""], ["  "], ["unknown"], ["published"]):
        assert got == "draft"


def test_case_and_whitespace_normalised():
    assert derive_publication_status(["  Active  "]) == "active"
    assert derive_publication_status(["RETIRED"]) == "retired"


def test_allowed_set_matches_what_the_codesystem_advertises():
    """fhir_codesystem describes the property as (draft, active, retired).

    If that description and the enforced set ever diverge, the CHECK
    constraint added by this ticket's migration becomes a lie.
    """
    assert CONCEPT_STATUSES == ("draft", "active", "retired")
    assert set(CONCEPT_STATUSES) <= set(FHIR_PUBLICATION_STATUSES)


def test_generator_input_is_accepted():
    """The call sites pass a generator over query rows, not a list."""
    assert derive_publication_status(s for s in ["draft", "active"]) == "active"


# ------------------------------------------------- it must actually be wired

@pytest.fixture
def one_concept(app):
    """A Concept that definitely exists, so the wiring tests never skip.

    The two tests below are the only ones that prove the endpoints are actually
    wired to the derivation rather than to a fresh constant. Skipping them on an
    empty database would leave exactly the gap #839 was filed about — a check
    that reports success without having run.
    """
    from app import db as _db
    from app.models.concept_models import CanonicalLib, Concept

    with app.app_context():
        lib = CanonicalLib.query.filter_by(
            canonical_lib_name='status839_lib').first()
        if lib is None:
            lib = CanonicalLib(
                canonical_lib_name='status839_lib',
                canonical_lib_url='https://termbank.pdhc.se/CodeSystem/status839',
                author='test',
            )
            _db.session.add(lib)
            _db.session.flush()
        c = Concept.query.filter_by(concept_name='status839_concept').first()
        if c is None:
            c = Concept(
                canonical_lib=lib.guid,
                canonical_refnumber='839',
                concept_name='status839_concept',
                concept_display_text='Status derivation test concept',
            )
            _db.session.add(c)
            _db.session.commit()
        guid = c.guid
        original = c.status
    yield guid
    with app.app_context():
        c = Concept.query.filter_by(guid=guid).first()
        if c is not None:
            c.status = original
            _db.session.commit()


def _resource(body):
    """Unwrap a FHIR searchset Bundle, or pass a bare resource through.

    `GET /api/v1/CodeSystem` answers a Bundle; `$lookup` and the by-id routes
    answer the resource. Handling both keeps the test about status derivation
    rather than about which shape the route happens to return.
    """
    if isinstance(body, dict) and body.get("resourceType") == "Bundle":
        entries = body.get("entry") or []
        assert entries, "Bundle had no entry to read a status from"
        return entries[0].get("resource") or {}
    return body or {}


def _statuses_of(app, db, Concept):
    return [r[0] for r in db.session.query(Concept.status).all()]


def test_codesystem_status_tracks_its_concepts(client, app, one_concept):
    """The endpoint must MOVE with the data.

    This is the regression that matters: a hardcoded literal satisfies any
    single-value assertion, so the test flips the content and requires the
    answer to follow.
    """
    from app import db
    from app.models.concept_models import Concept

    with app.app_context():
        c = Concept.query.filter_by(guid=one_concept).first()

        c.status = "draft"
        db.session.commit()
        assert _resource(client.get("/api/v1/CodeSystem").get_json())["status"] \
            == "draft"

        c.status = "active"
        db.session.commit()
        assert _resource(client.get("/api/v1/CodeSystem").get_json())["status"] \
            == "active", ("CodeSystem.status did not follow the content — it is "
                          "probably hardcoded again")

        # all-retired only reports retired when NOTHING else is draft/active
        c.status = "retired"
        db.session.commit()
        others = [r[0] for r in db.session.query(Concept.status)
                  .filter(Concept.guid != one_concept).all()]
        expected = derive_publication_status(["retired"] + others)
        assert _resource(client.get("/api/v1/CodeSystem").get_json())["status"] \
            == expected


def test_conceptmap_status_is_not_a_constant(client, app, one_concept):
    from app import db
    from app.models.concept_models import Concept

    with app.app_context():
        c = Concept.query.filter_by(guid=one_concept).first()

        c.status = "draft"
        db.session.commit()
        assert _resource(client.get("/api/v1/ConceptMap").get_json())["status"] \
            == "draft"

        c.status = "active"
        db.session.commit()
        assert _resource(client.get("/api/v1/ConceptMap").get_json())["status"] \
            == "active"
