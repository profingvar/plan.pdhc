"""#925 — the lookup read posture is a DECISION, not the absence of a decorator.

WHAT WAS WRONG. `_crud_routes` decorated CREATE/UPDATE/DELETE with
`@requires_role('read_write')` and decorated LIST and READ with nothing, so six
lookup tables served full records to anyone while CLAUDE.md §3 recorded this
service as `Auth: SSO`. That is §11's shape on a different service: a handbook
claim that no code implemented.

IT WAS AN OMISSION, NOT A POSTURE, and the proof is in the same module.
`/values` is the one lookup route written by hand instead of through the
factory, and its GET carries `@requires_role('read_only')`. The author who
wrote a read route by hand reached for the gate; the factory forgot it.
`/api/v1/ValueSet` is gated too while `CodeSystem` and `ConceptMap` are not —
three postures across one set of blueprints, measured in production 2026-11-04.

THE FIX IS THE REQUIRED PARAMETER, not the two gates. `public_read` is
keyword-only and has no default, so a new lookup table cannot be registered
without someone deciding, and the decision is visible at the registration line
rather than being the absence of a decorator forty lines away.

WHY FOUR READS STAY OPEN. Measured across all 26 repos: the deeper problem is
that plan.pdhc has **no working machine-auth door**. `KNOWN_SERVICES` holds only
`sim.pdhc` and `SIM_PDHC_SERVICE_KEY` is unset in production, so that dict
admits nobody; and `outbound_session_headers()`, which several clients do send,
carries `X-Operator-Session-Id` only — session propagation (#408), not
authentication. So every internal consumer reads plan unauthenticated BY
NECESSITY. Gating those four would break deployed services, one of them
silently. That sequencing is its own ticket.
"""
import uuid

import pytest

from app.api import lookup_tables
from tests.conftest import SAMPLE_ACCESS_BLOB, set_sso_session

#: Each open table with the consumer that forces it. The reason is in the test
#: so a future reader who wants to gate one knows what to fix first.
OPEN_WITH_REASON = [
    ('canonical-libs',
     "cdr1's #874 whole-system assertion gate; sends only X-Operator-Session-Id"),
    ('response-types',
     "request.pdhc context_service.py:61, headers={'Accept': ...} only"),
    ('units',
     "request.pdhc context_service.py:62, headers={'Accept': ...} only"),
    ('plandef-types',
     "request.pdhc plan_definition_service.py:96; _headers() LOOKS like a "
     "credential and is not"),
]

GATED = [
    ('concept-types',
     "sim's only caller targets /api/v1/concept-types without the /lookup "
     "prefix — measured 404, so it is already broken"),
    ('intended-uses', "no consumer in any of the 26 repos"),
]


class TestTheParameterIsRequired:
    """The actual fix. Everything below is a consequence of it."""

    def test_registering_a_table_without_a_posture_is_a_TypeError(self):
        from flask import Blueprint
        from app.models.concept_models import IntendedUse
        bp = Blueprint('probe925', __name__)
        with pytest.raises(TypeError):
            lookup_tables._crud_routes(bp, '/probe', IntendedUse,
                                       'intended_use_name')

    def test_it_is_keyword_only(self):
        """Positional would let someone pass it by accident in the display_text
        slot. `*` makes the call site say the word."""
        import inspect
        sig = inspect.signature(lookup_tables._crud_routes)
        p = sig.parameters['public_read']
        assert p.kind is inspect.Parameter.KEYWORD_ONLY
        assert p.default is inspect.Parameter.empty

    def test_every_registration_states_its_posture_explicitly(self):
        """Read from the PARSE TREE, so prose about `public_read` cannot satisfy
        it and a seventh table added without the keyword fails here as well as
        at import. Also pins the six postures: flipping one must update this
        list, which is the point."""
        import ast
        import inspect
        src = inspect.getsource(lookup_tables)
        tree = ast.parse(src)
        seen = {}
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == '_crud_routes'):
                url = node.args[1].value if len(node.args) > 1 else None
                kw = {k.arg: k.value for k in node.keywords}
                assert 'public_read' in kw, f"{url} registered without a posture"
                seen[url.lstrip('/')] = kw['public_read'].value
        assert seen == {
            'canonical-libs': True,
            'response-types': True,
            'units': True,
            'plandef-types': True,
            'concept-types': False,
            'intended-uses': False,
        }, seen


class TestTheGatedTables:
    @pytest.mark.parametrize("table,why", GATED, ids=[g[0] for g in GATED])
    def test_LIST_refuses_an_unauthenticated_caller(self, client, table, why):
        resp = client.get(f'/api/v1/lookup/{table}')
        assert resp.status_code == 401, (
            f"/{table} answered {resp.status_code} with no credential ({why})")

    @pytest.mark.parametrize("table,why", GATED, ids=[g[0] for g in GATED])
    def test_READ_refuses_BEFORE_it_looks_anything_up(self, client, table, why):
        """401 and not 404 for a guid that does not exist. A 404 would mean the
        gate runs after the lookup, which leaks existence."""
        resp = client.get(f'/api/v1/lookup/{table}/{uuid.uuid4()}')
        assert resp.status_code == 401, (
            f"got {resp.status_code}; a 404 would mean the gate is behind the "
            f"lookup and an attacker could probe for guids")

    @pytest.mark.parametrize("table,why", GATED, ids=[g[0] for g in GATED])
    def test_CONTROL_an_authenticated_caller_still_gets_through(
            self, client, table, why):
        """Without this, the two tests above would pass for a route that was
        simply broken."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        assert client.get(f'/api/v1/lookup/{table}').status_code == 200


class TestTheOpenTablesStayOpen:
    """CONTROLS. These are not aspirations — gating any of them breaks a
    DEPLOYED consumer, and the reason travels with the assertion."""

    @pytest.mark.parametrize("table,why", OPEN_WITH_REASON,
                             ids=[o[0] for o in OPEN_WITH_REASON])
    def test_LIST_still_answers_without_a_credential(self, client, table, why):
        resp = client.get(f'/api/v1/lookup/{table}')
        assert resp.status_code == 200, (
            f"/{table} now refuses an unauthenticated read, which breaks: {why}")


class TestWritesWereAlwaysGatedAndStillAre:
    @pytest.mark.parametrize("table", [t for t, _ in OPEN_WITH_REASON + GATED])
    def test_an_unauthenticated_CREATE_is_refused(self, client, table):
        """The original control from #925, kept: it is what made "reads are
        open" evidence rather than a proxy letting everything through."""
        resp = client.post(f'/api/v1/lookup/{table}', json={'x': 'y'})
        assert resp.status_code == 401


class TestValuesIsTheRouteThatProvedTheIntent:
    def test_it_was_already_gated_and_still_is(self, client):
        """`/values` is hand-written rather than registered through the factory,
        and it carries `@requires_role('read_only')`. It is the evidence that
        the open reads were an omission: the same authors, the same module, a
        read route, a gate."""
        assert client.get('/api/v1/lookup/values').status_code == 401

    def test_the_factory_now_agrees_with_it_where_it_can(self):
        """Not all six, because four have uncredentialed deployed consumers —
        but the two that could be brought in line have been."""
        import inspect
        src = inspect.getsource(lookup_tables.list_values)
        assert "read_only" in src


#: name field per open table, so a test can seed its own row instead of relying
#: on whatever the rest of the suite happened to leave in the database.
NAME_FIELD = {
    'canonical-libs': 'canonical_lib_name',
    'response-types': 'response_type_name',
    'units': 'unit_name',
    'plandef-types': 'plandef_type_name',
    'intended-uses': 'intended_use_name',
    'concept-types': 'concept_type_name',
}


def _seed(client, table, name, author='loader.pdhc'):
    """Create a row carrying `author`, authenticated, and return its guid.

    Seeding matters: the test database holds none of production's rows, so a
    test that merely asserts `loader.pdhc` is absent passes VACUOUSLY. A
    mutation proved exactly that — removing the strip failed only 1 of these
    tests until each one planted the value it is looking for.
    """
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    resp = client.post(f'/api/v1/lookup/{table}',
                       json={NAME_FIELD[table]: name, 'author': author})
    assert resp.status_code == 201, resp.get_data(as_text=True)
    return resp.get_json()['guid']


class TestThePublicProjectionDropsInternalHistory:
    """#925 decision 3. The DATA is not rewritten — only what is served.

    Measured in production 2026-11-04, the publicly readable tables served
    `author` values naming `loader.pdhc` (RETIRED by #736 — no repo, its live
    never-rotated key destroyed), a migration revision id, and two internal
    ticket slugs. The ticket proposed correcting the data; rewriting `author`
    would falsify WHO created the row, which is the same argument CLAUDE.md §2
    makes for leaving a superseded ticket number in a code comment alone.
    """

    @pytest.mark.parametrize("table,why", OPEN_WITH_REASON,
                             ids=[o[0] for o in OPEN_WITH_REASON])
    def test_a_public_LIST_carries_no_author(self, client, table, why):
        """Seeds the row it looks for. Without that this asserted over whatever
        rows the suite happened to leave behind, and a mutation removing the
        strip failed only one of the four."""
        _seed(client, table, f'probe925-list-{table}')
        rows = client.application.test_client().get(
            f'/api/v1/lookup/{table}').get_json()
        assert isinstance(rows, list) and rows, "nothing to assert on"
        for r in rows:
            assert 'author' not in r, f"/{table} still serves `author`"

    def test_a_public_READ_carries_no_author(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        created = client.post('/api/v1/lookup/units', json={
            'unit_name': 'probe925', 'unit_display_text': 'probe',
            'author': 'probe.pdhc'}).get_json()
        guid = created['guid']
        fresh = client.application.test_client()          # unauthenticated
        body = fresh.get(f'/api/v1/lookup/units/{guid}').get_json()
        assert body['unit_name'] == 'probe925'
        assert 'author' not in body

    def test_CONTROL_the_DATA_is_still_there(self, client, app):
        """The projection changed; the record did not. Without this the tests
        above would pass for a fix that deleted the column's contents."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        created = client.post('/api/v1/lookup/units', json={
            'unit_name': 'probe925b', 'unit_display_text': 'probe',
            'author': 'probe.pdhc'}).get_json()
        with app.app_context():
            from app.models.concept_models import Unit
            row = Unit.query.filter_by(guid=created['guid']).first()
            assert row is not None
            assert row.author == 'probe.pdhc', "the data was rewritten, not hidden"

    def test_CONTROL_a_GATED_table_still_serves_author(self, client):
        """Scoped to PUBLIC reads. A gated table cannot be read anonymously, so
        there is nothing to hide from — and keeping `author` there proves the
        strip is a projection choice rather than a blanket removal."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        created = client.post('/api/v1/lookup/intended-uses', json={
            'intended_use_name': 'probe925c', 'author': 'probe.pdhc'}).get_json()
        body = client.get(
            f"/api/v1/lookup/intended-uses/{created['guid']}").get_json()
        assert body.get('author') == 'probe.pdhc'

    @pytest.mark.parametrize("table,why", OPEN_WITH_REASON,
                             ids=[o[0] for o in OPEN_WITH_REASON])
    def test_no_retired_identity_is_named_in_a_public_response(
            self, client, table, why):
        """The specific production finding, asserted by VALUE rather than by
        field name — and it PLANTS that value first.

        This test was vacuous when written: the test database holds none of
        production's rows, so "loader.pdhc is absent" was true before the fix
        and after it. Seeding is what makes it evidence."""
        _seed(client, table, f'probe925-retired-{table}', author='loader.pdhc')
        raw = client.application.test_client().get(
            f'/api/v1/lookup/{table}').get_data(as_text=True)
        assert 'probe925-retired' in raw, "the seeded row is not in the response"
        for retired in ('loader.pdhc', 'monitor.pdhc', '2gate.pdhc'):
            assert retired not in raw, (
                f"/{table} names the retired identity {retired!r}")
