"""#923 — a canonical_lib_url must be an IDENTIFIER, not a browser address.

#875 made the url UNIQUE and guarded all four write paths. It never said what
a url should BE, and the audit that followed found the three code systems which
HAVE a registered FHIR URI published under values that are not them.

snomed's was the serious one, measured in production 2026-11-04:

    https://browser.ihtsdotools.org/?perspective=full&conceptId1=404684003
        &edition=MAIN/SNOMEDCT-SE/2025-11-30&release=&languages=sv,en

A human browser address carrying a perspective, a concept id, an edition and a
language list — emitted as `compose.include[].system` on every ValueSet read,
for 21 SNOMED concepts. A consumer resolving it gets a web page. The registered
URI is `http://snomed.info/sct`, which the platform already uses in 23 files
INCLUDING plan's own source and test suite: plan's terminology registry
disagreed with plan's own code. Live confirmation the same day: the FHIR Device
ips created from an alert implant assertion carries
`system = "http://snomed.info/sct"`.

`local` had the same shape for a different reason — the bare `https://plan.pdhc.se`,
plan's BASE url, while plan publishes its local concept set as the CodeSystem
`plan-pdhc-local` at its own canonical url (ADR D3, live, 99 concepts). 34 of 99
concepts bind to `local`.

WHY A DERIVED RULE AND NOT A BLOCKLIST, because this is the part worth keeping.
The obvious guard is "reject a url with a query string": an identifier needs
none. It catches snomed's and NOTHING else — `kva`'s old value,
`https://verktyg.internetmedicin.se/koder/kva`, is a third-party browser tool
with no query string at all. A blocklist of such hosts is always one host
behind. So the rule is positive: for a library we have decided about there is
exactly one acceptable url, derived from its name.
"""
import uuid

import pytest

from app import db
from app.models.concept_models import CanonicalLib
from app.services.canonical_libs import (LOCAL_LIB_NAME, LOCAL_LIB_URL,
                                         REGISTERED_SYSTEM_URLS,
                                         TERMBANK_CODESYSTEM_PREFIX,
                                         TERMBANK_LIBS, expected_lib_url,
                                         url_convention_error)
from tests.conftest import SAMPLE_ACCESS_BLOB, set_sso_session

API = '/api/v1/lookup/canonical-libs'
WEB_CREATE = '/canonical-libs/create'
WEB_EDIT = '/canonical-libs/{guid}/edit'

#: The five values that were LIVE in production before #923, each with the
#: value decided for it. Parametrised so a regression names the library.
OLD_TO_NEW = [
    ('snomed',
     'https://browser.ihtsdotools.org/?perspective=full&conceptId1=404684003'
     '&edition=MAIN/SNOMEDCT-SE/2025-11-30&release=&languages=sv,en',
     'http://snomed.info/sct'),
    ('loinc', 'https://LOINC.org', 'http://loinc.org'),
    ('atc', 'https://www.whocc.no/atc_ddd_index/', 'http://www.whocc.no/atc'),
    ('kva', 'https://verktyg.internetmedicin.se/koder/kva',
     'https://termbank.pdhc.se/CodeSystem/kva'),
    ('local', 'https://plan.pdhc.se',
     'https://plan.pdhc.se/fhir/CodeSystem/plan-pdhc-local'),
]
IDS = [o[0] for o in OLD_TO_NEW]


def _n(tag):
    return f"{tag}-{uuid.uuid4()}"


@pytest.fixture
def rows(client):
    """Create rows directly and remove them after, so these tests leave the
    shared sqlite file as they found it."""
    made = []

    def make(name, url=None):
        item = CanonicalLib(guid=str(uuid.uuid4()), canonical_lib_name=name,
                            canonical_lib_url=url)
        db.session.add(item)
        db.session.commit()
        made.append(item)
        return item

    yield make
    for item in made:
        db.session.delete(db.session.merge(item))
    db.session.commit()


class TestTheConvention:
    @pytest.mark.parametrize("name,old,new", OLD_TO_NEW, ids=IDS)
    def test_each_decided_library_has_exactly_one_acceptable_url(
            self, name, old, new):
        assert expected_lib_url(name) == new

    @pytest.mark.parametrize("name", sorted(TERMBANK_LIBS))
    def test_a_termbank_library_derives_its_url_from_its_name(self, name):
        """Derived rather than listed, so adding one cannot produce a typo."""
        assert expected_lib_url(name) == f"{TERMBANK_CODESYSTEM_PREFIX}{name}"

    @pytest.mark.parametrize("name", sorted(REGISTERED_SYSTEM_URLS))
    def test_a_registered_system_uses_the_EXTERNAL_authority_url(self, name):
        """Not a termbank url: the authority is somebody else's."""
        want = expected_lib_url(name)
        assert want == REGISTERED_SYSTEM_URLS[name]
        assert not want.startswith(TERMBANK_CODESYSTEM_PREFIX)

    def test_the_local_library_uses_plans_OWN_codesystem_url(self):
        assert expected_lib_url(LOCAL_LIB_NAME) == LOCAL_LIB_URL
        assert LOCAL_LIB_URL.endswith('/CodeSystem/plan-pdhc-local')

    def test_an_UNDECIDED_library_is_not_forced_into_a_shape(self):
        """None is deliberate: a library nobody has reasoned about yet should
        not be given an authority we invented for it."""
        assert expected_lib_url('some-new-vocabulary') is None

    def test_the_name_match_is_case_insensitive(self):
        assert expected_lib_url('SNOMED') == expected_lib_url('snomed')
        assert expected_lib_url('  Loinc  ') == 'http://loinc.org'


class TestTheRule:
    @pytest.mark.parametrize("name,old,new", OLD_TO_NEW, ids=IDS)
    def test_the_OLD_production_value_is_refused(self, name, old, new):
        err = url_convention_error(name, old)
        assert err is not None, f"{name}'s pre-#923 value is still accepted"

    @pytest.mark.parametrize("name,old,new", OLD_TO_NEW, ids=IDS)
    def test_the_DECIDED_value_is_accepted(self, name, old, new):
        assert url_convention_error(name, new) is None

    def test_snomeds_refusal_names_the_BROWSER_problem_not_the_convention(self):
        """Two different refusals, and the message should say which. snomed's
        old value fails the general identifier rule, so the reader learns the
        class of mistake rather than just 'wrong string'."""
        err = url_convention_error(*OLD_TO_NEW[0][:2])
        assert 'query string' in err and 'browser' in err

    def test_kvas_refusal_names_the_CONVENTION_because_the_url_looks_fine(self):
        """The case that defeats a query-string check: kva's old value is a
        third-party browser tool with no query string at all."""
        name, old, new = OLD_TO_NEW[3]
        assert '?' not in old and '#' not in old, "premise of this test"
        err = url_convention_error(name, old)
        assert new in err

    @pytest.mark.parametrize("bad", [
        'https://example.org/cs?x=1',
        'https://example.org/cs#frag',
        'https://example.org/cs?',
    ], ids=['query', 'fragment', 'empty-query'])
    def test_a_query_or_fragment_is_refused_for_ANY_library(self, bad):
        """Including one we have no convention for — no identifier needs
        either, so this rule does not depend on knowing the authority."""
        assert url_convention_error('some-new-vocabulary', bad) is not None

    def test_CONTROL_an_undecided_library_with_a_clean_url_is_accepted(self):
        """Without this, the rule above would pass for a guard that refused
        every unknown library outright."""
        assert url_convention_error('some-new-vocabulary',
                                    'https://example.org/cs/v1') is None

    @pytest.mark.parametrize("empty", [None, '', '   '])
    def test_CONTROL_no_url_is_accepted(self, empty):
        """`canonical_lib_url` is nullable and #875's UNIQUE constraint depends
        on many libraries legitimately having none."""
        assert url_convention_error('snomed', empty) is None


class TestAllFourWritePaths:
    """The dish, not the ingredient. #875 found the asymmetry that the NAME was
    guarded on four paths and the URL on none; a convention checked in only
    some of them is the same mistake one layer up."""

    def test_api_CREATE_refuses_a_browser_url(self, client, rows):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post(API, json={
            'canonical_lib_name': 'snomed-probe923',
            'canonical_lib_url': OLD_TO_NEW[0][1]})
        assert resp.status_code == 400, resp.get_data(as_text=True)
        assert 'browser' in resp.get_json()['error']

    def test_api_CREATE_refuses_a_decided_library_under_the_wrong_url(
            self, client, rows):
        """`loinc` with a clean but wrong url — the convention half, through
        the route rather than the helper."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post(API, json={
            'canonical_lib_name': 'loinc',
            'canonical_lib_url': 'https://LOINC.org'})
        assert resp.status_code == 400
        assert 'http://loinc.org' in resp.get_json()['error']

    def test_api_UPDATE_refuses_and_leaves_the_row_alone(self, client, rows):
        mine = rows(_n('u923'), 'https://example.org/cs/v1')
        was = mine.canonical_lib_url
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.put(f'{API}/{mine.guid}',
                          json={'canonical_lib_url': OLD_TO_NEW[0][1]})
        assert resp.status_code == 400
        db.session.expire_all()
        assert CanonicalLib.query.filter_by(
            guid=mine.guid).first().canonical_lib_url == was

    def test_api_UPDATE_validates_against_the_NEW_name_on_a_rename(
            self, client, rows):
        """A rename and a url change can arrive in the same PUT. Checking the
        OLD name would validate against the wrong convention — the row would
        become `loinc` carrying something that is not loinc's url."""
        mine = rows(_n('rn923'), 'https://example.org/cs/v1')
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.put(f'{API}/{mine.guid}', json={
            'canonical_lib_name': 'loinc',
            'canonical_lib_url': 'https://example.org/not-loinc'})
        assert resp.status_code == 400, (
            "renaming to `loinc` while setting a non-loinc url was accepted")
        assert 'http://loinc.org' in resp.get_json()['error']

    def test_html_CREATE_refuses_and_redirects(self, client, rows):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post(WEB_CREATE, data={
            'canonical_lib_name': 'snomed-web923',
            'canonical_lib_url': OLD_TO_NEW[0][1]})
        assert resp.status_code == 302
        assert CanonicalLib.query.filter_by(
            canonical_lib_name='snomed-web923').first() is None, (
                "the row was created despite the refusal")

    def test_html_EDIT_refuses_and_leaves_the_row_alone(self, client, rows):
        mine = rows(_n('we923'), 'https://example.org/cs/v1')
        was = mine.canonical_lib_url
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post(WEB_EDIT.format(guid=mine.guid), data={
            'canonical_lib_name': mine.canonical_lib_name,
            'canonical_lib_url': OLD_TO_NEW[0][1]})
        assert resp.status_code == 302
        db.session.expire_all()
        assert CanonicalLib.query.filter_by(
            guid=mine.guid).first().canonical_lib_url == was

    def test_CONTROL_all_four_accept_a_conventional_url(self, client, rows):
        """Without this, the six refusals above would pass for write paths
        that had simply stopped working."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        ok = client.post(API, json={'canonical_lib_name': _n('okapi923'),
                                    'canonical_lib_url': f'https://example.org/{uuid.uuid4()}'})
        assert ok.status_code == 201, ok.get_data(as_text=True)
        guid = ok.get_json()['guid']
        upd = client.put(f'{API}/{guid}',
                         json={'canonical_lib_url': f'https://example.org/{uuid.uuid4()}'})
        assert upd.status_code == 200
        web = client.post(WEB_CREATE, data={
            'canonical_lib_name': _n('okweb923'),
            'canonical_lib_url': f'https://example.org/{uuid.uuid4()}'})
        assert web.status_code == 302
        # clean up what this control created
        for g in (guid,):
            row = CanonicalLib.query.filter_by(guid=g).first()
            if row:
                db.session.delete(row)
        for row in CanonicalLib.query.filter(
                CanonicalLib.canonical_lib_name.like('okweb923-%')).all():
            db.session.delete(row)
        db.session.commit()


class TestTheLocalUrlIsDerivedNotWritten:
    def test_it_comes_from_the_one_helper(self):
        """My first version hardcoded the string and
        `test_no_other_file_hardcodes_plan_fhir_url` caught it. There is one
        helper for plan's own canonical urls, and this must not be a second
        source of the same fact."""
        from app.models.concept_models import (LOCAL_CODESYSTEM_ID,
                                               fhir_canonical_url)
        assert LOCAL_LIB_URL == fhir_canonical_url('CodeSystem',
                                                   LOCAL_CODESYSTEM_ID)

    def test_the_module_does_not_spell_the_url_out(self):
        """Asserted on the SOURCE, because the test above would also pass for a
        literal that happens to match today."""
        import inspect

        from app.services import canonical_libs
        src = inspect.getsource(canonical_libs)
        assert 'plan.pdhc.se/fhir/' not in src
