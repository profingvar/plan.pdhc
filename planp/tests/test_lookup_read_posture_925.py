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

#1011 (stage 3 of #931): THE FOUR ARE GATED NOW. #931 gave each consumer a
read_only key, and two days of plan's read_shadow log showed one keyless
consumer left (provider1.pdhc, keyed by #1011) plus crawlers. So every table
below is in GATED, and the required parameter is what stays.
"""
import uuid

import pytest

from app.api import lookup_tables
from tests.conftest import SAMPLE_ACCESS_BLOB, set_sso_session

#: Every table, with why it is gated. The first four were OPEN until #1011,
#: each forced open by a consumer with no credential; #931 gave those consumers
#: keys, and the reason now says who reads it with one.
GATED = [
    ('canonical-libs',
     "#1011: was open for cdr1's #874 gate; cdr now reads /whole-system-libs "
     "with its #931 key, and sim's synthea path sends its key"),
    ('response-types',
     "#1011: request.pdhc context_service and provider1 plan_client, keyed"),
    ('units',
     "#1011: request.pdhc context_service, keyed (#931)"),
    ('plandef-types',
     "#1011: request.pdhc plan_definition_service, keyed (#931)"),
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
            # #1011: the four that #925 had to leave open.
            'canonical-libs': False,
            'response-types': False,
            'units': False,
            'plandef-types': False,
            'concept-types': False,
            'intended-uses': False,
        # #951: a category name can name a guideline; closed by default.
        'concept-categories': False,
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


class TestWritesWereAlwaysGatedAndStillAre:
    @pytest.mark.parametrize("table", [t for t, _ in GATED])
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
        """#925 brought two of the six in line; #1011 the other four."""
        import inspect
        src = inspect.getsource(lookup_tables.list_values)
        assert "read_only" in src


class TestThePublicProjectionDropsInternalHistory:
    """#925 decision 3: a PUBLIC read drops `author`; the DATA is not rewritten.

    Since #1011 no registered table is public, so the projection has no live
    subject — but `public_read=True` is still a legal decision for a future
    table, and the branch it selects must still behave. These tests register
    the factory on a THROWAWAY app sharing the test database, so they exercise
    the real `_crud_routes` without re-opening a production route.
    """

    @pytest.fixture
    def public_units(self, app):
        from flask import Blueprint, Flask
        from app import db
        from app.models.concept_models import Unit
        tmp = Flask('probe925')
        tmp.config.update(SQLALCHEMY_DATABASE_URI=app.config['SQLALCHEMY_DATABASE_URI'],
                          TESTING=True)
        db.init_app(tmp)
        bp = Blueprint('probe925', __name__)
        lookup_tables._crud_routes(bp, '/units', Unit, 'unit_name',
                                   'unit_display_text', public_read=True)
        tmp.register_blueprint(bp, url_prefix='/x')
        with app.app_context():
            row = Unit(unit_name=f'probe925-{uuid.uuid4().hex[:6]}',
                       author='loader.pdhc')
            db.session.add(row)
            db.session.commit()
            guid = row.guid
        return tmp.test_client(), guid

    def test_a_public_LIST_carries_no_author(self, public_units):
        c, guid = public_units
        rows = c.get('/x/units').get_json()
        assert any(r['guid'] == guid for r in rows), "the seeded row is not there"
        assert all('author' not in r for r in rows)

    def test_a_public_READ_carries_no_author(self, public_units):
        c, guid = public_units
        body = c.get(f'/x/units/{guid}').get_json()
        assert body['guid'] == guid and 'author' not in body

    def test_no_retired_identity_is_named_in_a_public_response(self, public_units):
        """PLANTS the value first — written vacuous once (#925), seeded since."""
        c, _guid = public_units
        raw = c.get('/x/units').get_data(as_text=True)
        assert 'probe925-' in raw
        for retired in ('loader.pdhc', 'monitor.pdhc', '2gate.pdhc'):
            assert retired not in raw

    def test_CONTROL_the_DATA_is_still_there(self, app, public_units):
        _c, guid = public_units
        with app.app_context():
            from app.models.concept_models import Unit
            assert Unit.query.filter_by(guid=guid).first().author == 'loader.pdhc'

    def test_CONTROL_a_GATED_table_serves_author_to_a_reader(self, client):
        """Scoped to PUBLIC reads: the production tables are gated, so their
        authenticated readers get the full record."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        created = client.post('/api/v1/lookup/units', json={
            'unit_name': f'probe925c-{uuid.uuid4().hex[:6]}',
            'author': 'probe.pdhc'}).get_json()
        body = client.get(f"/api/v1/lookup/units/{created['guid']}").get_json()
        assert body.get('author') == 'probe.pdhc'
