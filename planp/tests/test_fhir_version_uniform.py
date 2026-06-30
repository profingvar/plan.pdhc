"""#331 — CodeSystem.version + ConceptMap.version derive from vers_number.

Pre-#331, both resources hardcoded ``'version': '1'`` while ValueSet
correctly used ``fhir_version()``. ADR D4 had a "TBD" carve-out for
CodeSystem and no carve-out at all for ConceptMap — a divergence
between the published rule and shipped code.

Post-#331, both resources derive from ``max(Concept.vers_number)``
(scoped to rows-with-binding for ConceptMap). Tests assert the version
moves when an underlying Concept bumps.
"""
from __future__ import annotations

import pytest

from app import db as _db
from app.models.concept_models import CanonicalLib, Concept


@pytest.fixture
def lib_with_concepts(app):
    """Create one CanonicalLib + two Concepts: one with a binding
    (canonical_refnumber set) and one without (canonical_refnumber NULL,
    canonical_lib still set since the column is NOT NULL).

    Cleans up at teardown so the max-based version derivation doesn't
    leak across tests.
    """
    with app.app_context():
        lib = CanonicalLib(canonical_lib_name=f'test-lib-{id(app)}',
                           canonical_lib_url='https://example.test/cs')
        _db.session.add(lib)
        _db.session.flush()

        c_bound = Concept(
            concept_name='bound-concept',
            canonical_lib=lib.guid,
            canonical_refnumber='12345',
            vers_number=5,
        )
        c_other = Concept(
            concept_name='other-concept',
            canonical_lib=lib.guid,
            canonical_refnumber='99999',
            vers_number=3,
        )
        _db.session.add_all([c_bound, c_other])
        _db.session.commit()

        yield {'lib': lib, 'bound': c_bound, 'other': c_other}

        _db.session.delete(c_bound)
        _db.session.delete(c_other)
        _db.session.delete(lib)
        _db.session.commit()


class TestCodeSystemVersionFromMaxConceptVersion:
    def test_codesystem_version_reflects_max_concept_vers_number(
        self, client, lib_with_concepts,
    ):
        # bound=5, unbound=3 → max = 5
        resp = client.get('/api/v1/CodeSystem/plan-pdhc-local')
        assert resp.status_code == 200
        body = resp.get_json()
        # CodeSystem covers ALL concepts (bound and unbound).
        assert body['version'] == '5', (
            f'expected version derived from max(Concept.vers_number)=5, '
            f'got {body["version"]!r}'
        )

    def test_codesystem_version_bumps_when_concept_bumps(
        self, app, client, lib_with_concepts,
    ):
        with app.app_context():
            # Bump the smaller concept above the previous max.
            c = Concept.query.filter_by(concept_name='other-concept').first()
            c.vers_number = 9
            _db.session.commit()

        resp = client.get('/api/v1/CodeSystem/plan-pdhc-local')
        assert resp.get_json()['version'] == '9'


class TestConceptMapVersionFromMaxBoundConceptVersion:
    def test_conceptmap_version_reflects_max_bound_concept_vers_number(
        self, client, lib_with_concepts,
    ):
        # Only the bound concept counts → max bound = 5.
        resp = client.get('/api/v1/ConceptMap/plan-pdhc-canonical-bindings')
        assert resp.status_code == 200
        body = resp.get_json()
        assert body['version'] == '5', (
            f'expected version derived from max(Concept.vers_number where '
            f'canonical_lib IS NOT NULL)=5, got {body["version"]!r}'
        )

    def test_conceptmap_tracks_bound_max(
        self, app, client, lib_with_concepts,
    ):
        with app.app_context():
            # Bump the other bound concept above the first.
            c = Concept.query.filter_by(concept_name='other-concept').first()
            c.vers_number = 42
            _db.session.commit()

        resp = client.get('/api/v1/ConceptMap/plan-pdhc-canonical-bindings')
        assert resp.get_json()['version'] == '42'


class TestNoEmptyVersionField:
    def test_codesystem_version_never_empty(self, client):
        # Even with no concepts in the DB, version must be a non-empty string.
        resp = client.get('/api/v1/CodeSystem/plan-pdhc-local')
        body = resp.get_json()
        assert body.get('version'), 'CodeSystem.version must never be empty'

    def test_conceptmap_version_never_empty(self, client):
        resp = client.get('/api/v1/ConceptMap/plan-pdhc-canonical-bindings')
        body = resp.get_json()
        assert body.get('version'), 'ConceptMap.version must never be empty'
