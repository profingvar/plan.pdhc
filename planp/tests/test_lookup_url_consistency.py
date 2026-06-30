"""Ticket #329: every serializer URL for a lookup-blueprint resource must
include the `/api/v1/lookup/` prefix. ValueSet.to_dict and Concept.to_dict
historically emitted bare `/api/v1/valuesets/` paths, which 404 against
the real blueprint registration in app/__init__.py.
"""
import uuid
import pytest

from app import db
from app.models.concept_models import CanonicalLib, ValueSet, Concept


@pytest.fixture
def lib(client):
    cl = CanonicalLib(
        guid=f'cl-{uuid.uuid4()}',
        canonical_lib_name=f'lookup-url-test-{uuid.uuid4()}',
    )
    db.session.add(cl)
    db.session.commit()
    yield cl
    try:
        db.session.delete(cl)
        db.session.commit()
    except Exception:
        db.session.rollback()


class TestLookupURLConsistency:
    def test_valueset_to_dict_self_url_uses_lookup(self, lib):
        vs = ValueSet(
            guid=f'vs-{uuid.uuid4()}',
            canonical_lib=lib.guid,
            valueset_name=f'lookup-url-vs-{uuid.uuid4()}',
            valueset_display_text='Test ValueSet',
            author='pytest',
        )
        db.session.add(vs)
        db.session.commit()
        try:
            d = vs.to_dict(include_values=False)
            assert d['url'].endswith(f'/api/v1/lookup/valuesets/{vs.guid}'), d['url']
        finally:
            db.session.delete(vs)
            db.session.commit()

    def test_concept_to_dict_valueset_url_uses_lookup(self, lib):
        vs = ValueSet(
            guid=f'vs-{uuid.uuid4()}',
            canonical_lib=lib.guid,
            valueset_name=f'lookup-url-vs2-{uuid.uuid4()}',
            valueset_display_text='Test ValueSet 2',
            author='pytest',
        )
        db.session.add(vs)
        c = Concept(
            guid=f'c-{uuid.uuid4()}',
            canonical_lib=lib.guid,
            concept_name=f'lookup-url-concept-{uuid.uuid4()}',
            valueset=vs.guid,
            vers_number=1,
        )
        db.session.add(c)
        db.session.commit()
        try:
            d = c.to_dict()
            assert 'valueset_url' in d
            assert d['valueset_url'].endswith(f'/api/v1/lookup/valuesets/{vs.guid}'), d['valueset_url']
        finally:
            db.session.delete(c)
            db.session.delete(vs)
            db.session.commit()
