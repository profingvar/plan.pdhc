"""#841 — the FHIR resource status is a property of the RESOURCE, not of
Concept.status, and Concept.status is retired.

This file previously pinned the opposite (#839): the three terminology
wrappers derived their `status` from the Concepts underneath, having formerly
hardcoded `'active'`. #841 found why that derivation could not work. Nothing in
plan could move a Concept out of `draft` — no promote/publish/activate/retire
route, no control in `concepts/create.html` or `concepts/edit.html`, and the
importer hardcodes `status='draft'` — so all 99 Concepts held the column
default. A required FHIR field derived from a field that cannot change is
permanently one value, and looks like information while carrying none.

The operator's decision (2026-10-20): status is not meant to gate adoption.

So these tests now pin the inverse property, which is the one worth guarding:

  * each resource reports `active`, because it IS in use — plan's Concepts
    validate every CDR write through the canonicaliser's plan-Concept tier;
  * the resource status does NOT move when a Concept's status changes, which
    is what proves the derivation is gone rather than merely returning `active`
    today by coincidence;
  * the retired field is gone from every surface that used to expose it, so it
    cannot quietly come back as a half-wired gate.

Asserting only `== 'active'` would pass against the #839 derivation on a
database that happened to hold one active Concept, which is why
`test_status_does_not_follow_concept_status` exists.
"""
from __future__ import annotations

import uuid

import pytest

from app.api.fhir_helpers import (
    FHIR_PUBLICATION_STATUSES,
    RESOURCE_PUBLICATION_STATUS,
)
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB


# ------------------------------------------------------------- the constant

def test_resource_status_is_a_valid_fhir_publication_status():
    assert RESOURCE_PUBLICATION_STATUS in FHIR_PUBLICATION_STATUSES


def test_resource_status_is_active():
    """`draft` would be the #839 regression; `unknown` would be a cop-out."""
    assert RESOURCE_PUBLICATION_STATUS == 'active'


def test_the_derivation_is_gone():
    """Guard against reinstatement. #841 removed the fold over content; if it
    comes back, it must come back with a governance answer attached."""
    import app.api.fhir_helpers as helpers
    assert not hasattr(helpers, 'derive_publication_status')
    assert not hasattr(helpers, 'CONCEPT_STATUSES')


# ---------------------------------------------------------------- the wiring

@pytest.fixture
def one_concept(app):
    """A Concept that definitely exists, so the wiring tests never skip.

    An empty database would leave exactly the gap #839 was filed about — a
    check reporting success without having run.
    """
    from app import db as _db
    from app.models.concept_models import CanonicalLib, Concept

    with app.app_context():
        lib = CanonicalLib.query.filter_by(
            canonical_lib_name='status841_lib').first()
        if lib is None:
            lib = CanonicalLib(
                canonical_lib_name='status841_lib',
                canonical_lib_url='https://termbank.pdhc.se/CodeSystem/status841',
                author='test',
            )
            _db.session.add(lib)
            _db.session.flush()
        c = Concept.query.filter_by(concept_name='status841_concept').first()
        if c is None:
            c = Concept(
                canonical_lib=lib.guid,
                canonical_refnumber='841',
                concept_name='status841_concept',
                concept_display_text='Status retirement test concept',
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
    """Unwrap a FHIR searchset Bundle, or pass a bare resource through."""
    if isinstance(body, dict) and body.get("resourceType") == "Bundle":
        entries = body.get("entry") or []
        assert entries, "Bundle had no entry to read a status from"
        return entries[0].get("resource") or {}
    return body or {}


@pytest.mark.parametrize("url", [
    '/api/v1/CodeSystem',
    '/api/v1/ValueSet',
    '/api/v1/ConceptMap',
])
def test_every_terminology_resource_reports_active(client, one_concept, url):
    resp = client.get(url)
    assert resp.status_code == 200, resp.get_data(as_text=True)
    res = _resource(resp.get_json())
    assert res.get('status') == 'active', url


@pytest.mark.parametrize("url", [
    '/api/v1/CodeSystem',
    '/api/v1/ValueSet',
    '/api/v1/ConceptMap',
])
def test_status_does_not_follow_concept_status(client, app, one_concept, url):
    """THE test. Move a Concept's status through every allowed value and the
    resource status must not budge.

    Under #839's derivation, flipping this Concept to `active` or `retired`
    changed the CodeSystem and ConceptMap answer. That coupling is what #841
    removed, so a resource status that still tracked it would be the
    regression — and a test asserting only `== 'active'` could not see it.
    """
    from app import db as _db
    from app.models.concept_models import Concept

    seen = set()
    for value in ('draft', 'active', 'retired', 'anything-at-all'):
        with app.app_context():
            c = Concept.query.filter_by(guid=one_concept).first()
            c.status = value
            _db.session.commit()
        res = _resource(client.get(url).get_json())
        seen.add(res.get('status'))
    assert seen == {'active'}, f"{url} status moved with Concept.status: {seen}"


# -------------------------------------------------- the field is really gone

def test_codesystem_no_longer_advertises_a_status_property(client, one_concept):
    """It described "Concept editorial status (draft, active, retired)" — an
    editorial lifecycle that did not exist."""
    res = _resource(client.get('/api/v1/CodeSystem').get_json())
    codes = {p.get('code') for p in res.get('property', [])}
    assert 'status' not in codes, codes


def test_no_concept_emits_a_status_property(client, one_concept):
    res = _resource(client.get('/api/v1/CodeSystem').get_json())
    for concept in res.get('concept', []):
        codes = {p.get('code') for p in concept.get('property', [])}
        assert 'status' not in codes, concept.get('code')


def test_to_dict_has_no_status_key(app, one_concept):
    from app.models.concept_models import Concept
    with app.app_context():
        c = Concept.query.filter_by(guid=one_concept).first()
        assert 'status' not in c.to_dict()


def test_the_api_will_not_set_status_on_create(client, app):
    """A caller POSTing `status` must not be able to set it. The column keeps
    its default; the field is not part of the write surface any more."""
    from app.models.concept_models import Concept

    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    name = f'status841-create-{uuid.uuid4().hex[:8]}'
    resp = client.post('/api/v1/concepts', json={
        'concept_name': name,
        'status': 'active',
    })
    assert resp.status_code == 201, resp.get_json()
    assert 'status' not in resp.get_json()
    with app.app_context():
        c = Concept.query.filter_by(concept_name=name).first()
        assert c is not None
        assert c.status == 'draft', "POSTed status reached the column"


def test_the_api_will_not_set_status_on_update(client, app, one_concept):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    resp = client.put(f'/api/v1/concepts/{one_concept}',
                      json={'status': 'active'})
    assert resp.status_code in (200, 204), resp.get_data(as_text=True)
    from app.models.concept_models import Concept
    with app.app_context():
        c = Concept.query.filter_by(guid=one_concept).first()
        assert c.status != 'active', "PATCHed status reached the column"
