"""#935 — serve what the consumer needs inline, not behind a second gated call.

Two additions, both following plan's OWN precedent: `concepts.py` already adds
`valueset_values` to the serialised concept "so no extra call is needed".

1. `concept_type_name` on GET /api/v1/concepts/<guid>.

   A concept's `concept_type` is a GUID whose name lives at
   /api/v1/lookup/concept-types — and #925 GATED that lookup. sim.pdhc has no
   plan credential at all (and per #931 plan's service-key door admits nobody
   anyway), and its `get_lookup_name` returns None on any non-200, so the
   failure would be SILENT. #917 part 2 needs this name to decide whether a
   simulated term emits a Condition, a MedicationStatement or a Procedure
   instead of an Observation.

   My #925 reasoning for gating concept-types was that its only non-plan
   caller requested /api/v1/concept-types WITHOUT the /lookup prefix and
   therefore 404s. True then; #917 creates a new caller, so the gate is wrong
   for it — and the answer is to stop needing the call, not to un-gate.

2. GET /api/v1/lookup/whole-system-libs — the three fields cdr1's #874
   whole-system assertion gate actually reads, and nothing else.

   Today that gate reads the WHOLE canonical-libs table through a client
   sending only `X-Operator-Session-Id` — session propagation (#408), not
   authentication. So a deployed SECURITY CONTROL depends on that endpoint
   happening to be open, and gating it would silently degrade the gate to its
   hard-coded floor. This route makes the dependency explicit.

   A narrow view would NOT have been safe before #875: cdr's client computes
   which urls are unambiguous, because `icd10` once carried `snomed`'s url.
   #875 made `canonical_lib_url` UNIQUE, verified in production.
"""
import uuid

import pytest

from app import db
from app.models.concept_models import (CanonicalLib, Concept, ConceptType)
from tests.conftest import SAMPLE_ACCESS_BLOB, set_sso_session

NARROW = '/api/v1/lookup/whole-system-libs'
#: Exactly the fields the consumer reads. Asserted as an equality so this
#: endpoint cannot quietly grow into a second enumerating surface.
NARROW_FIELDS = {'canonical_lib_name', 'canonical_lib_url',
                 'whole_system_answer_space'}


def _n(tag):
    return f"{tag}-{uuid.uuid4()}"


@pytest.fixture
def rows(client):
    """Create rows directly and remove them after, so these tests leave the
    shared sqlite file as they found it."""
    made = []

    def make(model, **kw):
        item = model(guid=str(uuid.uuid4()), **kw)
        db.session.add(item)
        db.session.commit()
        made.append(item)
        return item

    yield make
    for item in made:
        db.session.delete(db.session.merge(item))
    db.session.commit()


class TestConceptTypeNameIsInline:
    def test_the_read_route_resolves_the_name(self, client, rows):
        ct = rows(ConceptType, concept_type_name=_n('Diagnsosis ICD10'))
        lib = rows(CanonicalLib, canonical_lib_name=_n('lib935'))
        c = rows(Concept, concept_name=_n('probe935'),
                 canonical_lib=lib.guid, concept_type=ct.guid)
        body = client.get(f'/api/v1/concepts/{c.guid}').get_json()
        assert body['concept_type'] == ct.guid, 'the GUID must still be there'
        assert body['concept_type_name'] == ct.concept_type_name

    def test_a_consumer_no_longer_needs_the_GATED_lookup(self, client, rows):
        """The point, asserted as the thing it replaces: the name is reachable
        from this one response, so nobody has to call
        /api/v1/lookup/concept-types — which answers 401 without a credential
        since #925."""
        ct = rows(ConceptType, concept_type_name=_n('Medication'))
        lib = rows(CanonicalLib, canonical_lib_name=_n('lib935b'))
        c = rows(Concept, concept_name=_n('probe935b'),
                 canonical_lib=lib.guid, concept_type=ct.guid)
        fresh = client.application.test_client()          # unauthenticated
        body = fresh.get(f'/api/v1/concepts/{c.guid}').get_json()
        assert body['concept_type_name'] == ct.concept_type_name
        assert fresh.get('/api/v1/lookup/concept-types').status_code == 401, (
            'premise of this test: the lookup is gated')

    def test_it_is_absent_when_the_concept_has_no_type(self, client, rows):
        """`concept_type` is nullable. Absent is not the same as None, and a
        key that appears with a null value invites a consumer to treat it as
        resolved."""
        lib = rows(CanonicalLib, canonical_lib_name=_n('lib935c'))
        c = rows(Concept, concept_name=_n('probe935c'),
                 canonical_lib=lib.guid, concept_type=None)
        body = client.get(f'/api/v1/concepts/{c.guid}').get_json()
        assert 'concept_type_name' not in body

    def test_CONTROL_the_LIST_route_deliberately_does_not_carry_it(
            self, client, rows):
        """Deliberate, not an oversight: no working consumer needs it there,
        and resolving a name per row on a 200-row page is a cost nobody asked
        for. #917 part 2 reads the single-concept route."""
        ct = rows(ConceptType, concept_type_name=_n('Procedure'))
        lib = rows(CanonicalLib, canonical_lib_name=_n('lib935d'))
        name = _n('probe935d')
        rows(Concept, concept_name=name, canonical_lib=lib.guid,
             concept_type=ct.guid)
        items = client.get(f'/api/v1/concepts?search={name}').get_json()['items']
        assert items, 'the concept is not in the list at all'
        assert 'concept_type_name' not in items[0]
        assert items[0]['concept_type'] == ct.guid, (
            'the GUID is still there, so a caller that needs the name can '
            'fetch the one concept')


class TestTheNarrowWholeSystemRead:
    def test_it_answers_without_a_credential(self, client):
        """PUBLIC by decision. cdr's gate sends only an operator session id."""
        fresh = client.application.test_client()
        assert fresh.get(NARROW).status_code == 200

    def test_it_returns_only_the_FLAGGED_libraries(self, client, rows):
        flagged = rows(CanonicalLib, canonical_lib_name=_n('ws935'),
                       canonical_lib_url=f'https://example.org/{uuid.uuid4()}',
                       whole_system_answer_space=True)
        plain = rows(CanonicalLib, canonical_lib_name=_n('plain935'),
                     canonical_lib_url=f'https://example.org/{uuid.uuid4()}',
                     whole_system_answer_space=False)
        names = {r['canonical_lib_name']
                 for r in client.get(NARROW).get_json()}
        assert flagged.canonical_lib_name in names
        assert plain.canonical_lib_name not in names, (
            'an unflagged library leaked into the whole-system view')

    def test_it_returns_EXACTLY_three_fields(self, client, rows):
        """An equality, not a superset check. The endpoint exists because it is
        narrower than the table; if it grows it stops being that, and the
        argument for keeping it public stops holding."""
        rows(CanonicalLib, canonical_lib_name=_n('ws935b'),
             canonical_lib_url=f'https://example.org/{uuid.uuid4()}',
             whole_system_answer_space=True)
        body = client.get(NARROW).get_json()
        assert body, 'nothing to assert on'
        for row in body:
            assert set(row) == NARROW_FIELDS, sorted(row)

    def test_it_agrees_with_the_full_table(self, client, rows):
        """Two views of one fact must not drift. The full table is the
        authority; this is a projection of it."""
        rows(CanonicalLib, canonical_lib_name=_n('ws935c'),
             canonical_lib_url=f'https://example.org/{uuid.uuid4()}',
             whole_system_answer_space=True)
        narrow = {r['canonical_lib_name'] for r in client.get(NARROW).get_json()}
        full = {r['canonical_lib_name']
                for r in client.get('/api/v1/lookup/canonical-libs').get_json()
                if r.get('whole_system_answer_space')}
        assert narrow == full

    def test_CONTROL_it_does_not_carry_author_either(self, client, rows):
        """#925 stopped serving `author` on the public lookup reads because it
        named the retired `loader.pdhc`. A new public read must not reintroduce
        it."""
        rows(CanonicalLib, canonical_lib_name=_n('ws935d'),
             canonical_lib_url=f'https://example.org/{uuid.uuid4()}',
             whole_system_answer_space=True, author='loader.pdhc')
        raw = client.get(NARROW).get_data(as_text=True)
        assert 'author' not in raw
        assert 'loader.pdhc' not in raw

    def test_it_is_READ_only(self, client):
        """A write surface here would be a second way to flag a library, which
        is a decision that belongs on the table's own guarded routes."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        for verb in ('post', 'put', 'delete'):
            resp = getattr(client, verb)(NARROW, json={})
            assert resp.status_code == 405, f'{verb.upper()} is {resp.status_code}'
