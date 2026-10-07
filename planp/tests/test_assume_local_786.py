"""#786 item 2 — "for concepts with no reference to canonical libs assume local".

Before this, three independent paths each refused instead of defaulting: the
web form (`required` with an empty option), the JSON API (400), and the CSV
importer (ValueError). So an author writing a purely local concept had to know
to pick "local" out of eight libraries, on every path, every time.

The rule is a statement about what the concept IS, not a field someone forgot
to fill in. These tests go through each of the three real entry points, because
the defect was that each one independently said no.

One distinction is load-bearing and has its own tests: **blank means local, an
unrecognised name is still an error.** Blank is an assertion ("this term is
ours"); "snomd" is a typo, and silently resolving a typo to local would attach
a wrong terminology claim to clinical data.
"""
import io
import uuid

import pytest

from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB


def _local_name_count(db_session):
    from app.models.concept_models import CanonicalLib
    from app import db
    return (CanonicalLib.query
            .filter(db.func.lower(CanonicalLib.canonical_lib_name) == 'local')
            .count())


class TestTheSharedDefault:
    """app/services/canonical_libs.py — the one place that decides."""

    def test_blank_resolves_to_local(self, app, db_session):
        from app.services.canonical_libs import resolve_or_local, find_local_lib
        with app.app_context():
            guid = resolve_or_local('')
            assert guid
            assert find_local_lib().guid == guid

    def test_none_resolves_to_local(self, app, db_session):
        from app.services.canonical_libs import resolve_or_local, find_local_lib
        with app.app_context():
            assert resolve_or_local(None) == find_local_lib().guid

    def test_whitespace_resolves_to_local(self, app, db_session):
        """A CSV cell containing a space is blank, not a library named " "."""
        from app.services.canonical_libs import resolve_or_local, find_local_lib
        with app.app_context():
            assert resolve_or_local('   ') == find_local_lib().guid

    def test_it_creates_local_only_once(self, app, db_session):
        """Nothing seeds `local`, so the default has to be able to establish
        it -- but it must not add a second row on every save."""
        from app.services.canonical_libs import resolve_or_local
        with app.app_context():
            a = resolve_or_local(None)
            b = resolve_or_local(None)
            c = resolve_or_local('')
            assert a == b == c
            assert _local_name_count(db_session) == 1

    def test_a_library_NAME_resolves_to_its_guid(self, app, db_session):
        """So a CSV may say "local" or "snomed" rather than a guid."""
        from app.services.canonical_libs import resolve_or_local, ensure_local_lib
        with app.app_context():
            local = ensure_local_lib()
            assert resolve_or_local('local') == local.guid
            assert resolve_or_local('LOCAL') == local.guid, 'must be case-insensitive'

    def test_an_unknown_name_is_handed_back_not_silently_localised(
            self, app, db_session):
        """THE important one. A misspelled vocabulary must NOT become local.

        Turning "snomd" into a local binding would record that the clinic
        invented a term it was actually trying to cite from SNOMED -- a wrong
        terminology claim attached to clinical data, and invisible. The caller's
        own validation is left to reject it.
        """
        from app.services.canonical_libs import resolve_or_local, find_local_lib
        with app.app_context():
            out = resolve_or_local('snomd')
            assert out == 'snomd'
            assert find_local_lib() is None or out != find_local_lib().guid


class TestTheApiPath:
    def test_a_concept_with_no_canonical_lib_is_created_as_local(self, client):
        """Was 400 'concept_name and canonical_lib are required'."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post('/api/v1/concepts', json={
            'concept_name': f'local-only-{uuid.uuid4().hex[:8]}',
        })
        assert resp.status_code == 201, resp.get_json()
        body = resp.get_json()
        assert body['canonical_lib']

        lib = client.get(f"/api/v1/lookup/canonical-libs/{body['canonical_lib']}")
        assert lib.status_code == 200
        assert lib.get_json()['canonical_lib_name'].lower() == 'local'

    def test_concept_name_is_still_required(self, client):
        """The default applies to the vocabulary, not to the name. A concept
        with no name is not a concept."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post('/api/v1/concepts', json={'canonical_lib': ''})
        assert resp.status_code == 400
        assert 'concept_name' in resp.get_json()['error']

    def test_an_unknown_library_still_fails(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post('/api/v1/concepts', json={
            'concept_name': f'bad-lib-{uuid.uuid4().hex[:8]}',
            'canonical_lib': 'definitely-not-a-library',
        })
        assert resp.status_code in (400, 404), resp.get_json()

    def test_an_explicit_library_is_still_honoured(self, client):
        """The default must not override a real choice."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        made = client.post('/api/v1/lookup/canonical-libs', json={
            'canonical_lib_name': f'ExplicitLib_{uuid.uuid4()}'})
        lib_guid = made.get_json()['guid']
        resp = client.post('/api/v1/concepts', json={
            'concept_name': f'explicit-{uuid.uuid4().hex[:8]}',
            'canonical_lib': lib_guid,
        })
        assert resp.status_code == 201
        assert resp.get_json()['canonical_lib'] == lib_guid


class TestTheCsvImportPath:
    def test_a_blank_canonical_lib_column_imports_as_local(self, app, db_session):
        """Was ValueError 'canonical_lib is required', which made a spreadsheet
        of purely local concepts -- the common case when a clinic writes its
        own -- impossible to import without typing "local" into every row."""
        from app.services.concept_importer import validate_and_import
        name = f'csv-local-{uuid.uuid4().hex[:8]}'
        with app.app_context():
            report = validate_and_import(
                [{'concept_name': name, 'display_text': 'CSV local',
                  'canonical_lib': '', 'canonical_ref': '',
                  'concept_type': '', 'response_type': '', 'unit': ''}],
                operator='test', filename='t.csv', sha256='x')
            assert report['summary']['n_accepted'] == 1, report
            assert report['rejected'] == [], report

            from app.models.concept_models import Concept
            from app.services.canonical_libs import find_local_lib
            c = Concept.query.filter_by(concept_name=name).first()
            assert c is not None
            assert c.canonical_lib == find_local_lib().guid

    def test_an_unknown_canonical_lib_still_reports_an_error(self, app, db_session):
        from app.services.concept_importer import validate_and_import
        with app.app_context():
            report = validate_and_import(
                [{'concept_name': f'csv-bad-{uuid.uuid4().hex[:8]}',
                  'display_text': 'x', 'canonical_lib': 'snomd',
                  'canonical_ref': '', 'concept_type': '',
                  'response_type': '', 'unit': ''}],
                operator='test', filename='t.csv', sha256='x')
            assert report['summary']['n_accepted'] == 0, report
            assert report['rejected'], report
            assert 'canonical_lib not found' in report['rejected'][0]['reason']


class TestTheFormPath:
    def test_the_create_form_preselects_local(self, client):
        """The server applies the default regardless, but a form that still
        showed an empty "Select..." would teach the author otherwise."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        client.post('/api/v1/concepts',
                    json={'concept_name': f'seed-{uuid.uuid4().hex[:8]}'})
        html = client.get('/concepts/create').data.decode()
        assert 'local — no canonical vocabulary (default)' in html
        # and it is no longer a required field with an empty value
        i = html.index('name="canonical_lib"')
        select = html[i:i + 200]
        assert 'required' not in select, select
