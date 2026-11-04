"""plan's terminology surface: reads public, writes gated — #913.

I filed #913 reading this as ten routes somebody forgot to gate. Measured
properly, it is a deliberate and consistent pattern:

    app/api/fhir_valueset.py     6 read route functions (10 URL patterns —
                                 four declare both `$expand` and its
                                 `%24`-encoded spelling), ungated,
                                 0 write routes
    app/api/lookup_tables.py    19 route functions: 12 write routes, all
                                 @requires_role('read_write')

**As of 2026-11-03 the reads are no longer all public.** #913's third option
was built: what ENUMERATES is `read_only`-gated, what answers about a single
code the caller already holds stays public. See `TestOptionThree`. That is a design, not
an oversight, and FHIR terminology servers commonly publish `$expand` and
`$validate-code` as reference data.

**But it is written down nowhere.** No comment in either module says reads
are public by design, so the convention has to be inferred from twenty-four
decorators — which is exactly how I came to read it as a gap, and how the
next person adding a route will guess. An unstated invariant is one commit
from being broken by someone being helpful.

So this file states it and enforces it. The valuable direction is the write
one: a NEW write route added without a role gate is a silent privilege
change, and nothing else in the suite would notice.

**What #913 is actually about, after the measurement.** Not the gating. It is
that alert.pdhc's step 2.b-ii would register the Socialstyrelsen urval — 19
ValueSets, 219 memberships, copyright-protected — into a surface that is
public ON PURPOSE. Confirmed reachable: `GET /api/v1/ValueSet` answers 200
unauthenticated through the proxy, whose vhost has no `auth_basic`,
`auth_request`, `deny` or `allow` and is a bare `location / { proxy_pass }`.

That is a licensing decision for the operator, and this file does not
pretend to settle it. It only makes sure the surface cannot change shape by
accident while the decision is pending.
"""
from __future__ import annotations

import ast
import pathlib

import pytest

API = pathlib.Path(__file__).parent.parent / 'app' / 'api'

#: Methods that change state. A route carrying any of these must be gated.
WRITE_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}

#: FHIR expresses some READS as POST, because the parameters do not fit in a
#: URL. These are reads and are deliberately exempt from the write rule —
#: named individually rather than pattern-matched, so adding one is a
#: decision rather than a side effect of choosing a function name.
FHIR_READ_OPERATIONS = {
    'expand_valueset_by_parameters',
    'scoped_validate_code_by_post',
}


def _routes(path: pathlib.Path):
    """(function name, methods, decorator names) for every route in a module."""
    tree = ast.parse(path.read_text())
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        methods, names, is_route = set(), [], False
        for dec in node.decorator_list:
            call = dec if isinstance(dec, ast.Call) else None
            target = call.func if call else dec
            label = ast.unparse(target)
            names.append(label)
            if label.endswith('.route'):
                is_route = True
                for kw in (call.keywords if call else []):
                    if kw.arg == 'methods':
                        try:
                            methods |= {m.value for m in kw.value.elts}
                        except AttributeError:
                            pass
                if not methods:
                    methods.add('GET')      # Flask's default
        if is_route:
            out.append((node.name, methods, names))
    return out


def _gated(decorator_names) -> bool:
    return any('requires_role' in n for n in decorator_names)


class TestEveryWriteIsGated:
    """The direction that matters. A new ungated write route is a silent
    privilege change, and this is the only thing that would notice."""

    @pytest.mark.parametrize('module', ['lookup_tables.py',
                                        'fhir_valueset.py',
                                        'terminology.py',
                                        'concepts.py'])
    def test_no_state_changing_route_is_ungated(self, module):
        path = API / module
        if not path.exists():
            pytest.skip(f'{module} is not present')
        offenders = [
            (name, sorted(methods)) for name, methods, decs in _routes(path)
            if (methods & WRITE_METHODS)
            and name not in FHIR_READ_OPERATIONS
            and not _gated(decs)
        ]
        assert offenders == [], (
            f'{module}: state-changing routes with no @requires_role: '
            f'{offenders}'
        )

    def test_the_fhir_read_exemptions_really_are_reads(self):
        """Named exemptions, checked against what they are called. A list of
        names is only as good as the reason each is on it: both of these are
        FHIR operations that read, expressed as POST because their
        parameters do not fit in a URL."""
        for name in FHIR_READ_OPERATIONS:
            assert 'expand' in name or 'validate' in name, name


class TestTheReadSurfaceIsPublicOnPurpose:
    """Stated so it stops being folklore. If this ever becomes wrong, the
    change should break a test rather than surprise a consumer — alert's
    gate calls `$validate-code` on every candidate."""

    def test_the_fhir_valueset_blueprint_has_no_write_routes_at_all(self):
        writes = [(n, sorted(m)) for n, m, _d in _routes(API / 'fhir_valueset.py')
                  if (m & WRITE_METHODS) and n not in FHIR_READ_OPERATIONS]
        assert writes == []

    def test_validate_code_stays_reachable_without_a_role(self):
        """alert.pdhc's candidate gate asks this per candidate (its 3.c).
        Gating it would make every candidate fail closed as
        `vocabulary_miss` — correct behaviour for an unaskable vocabulary,
        and a silent stop to the whole module."""
        gated = [n for n, _m, d in _routes(API / 'fhir_valueset.py')
                 if 'validate_code' in n and _gated(d)]
        assert gated == [], (
            'validate-code became role-gated; alert.pdhc calls it per '
            'candidate and would fail every one closed. If that is intended, '
            'alert needs a read_only grant in KNOWN_SERVICES first.')

    def test_the_counts_are_what_the_measurement_found(self):
        """Numbers, so a drift in either direction is visible.

        Also a correction to #913, which said "ten FHIR ValueSet routes":
        there are **six route FUNCTIONS carrying ten URL patterns**, four
        declaring both the literal `$expand` / `$validate-code` and the
        `%24`-encoded spelling. My ticket counted DECORATORS with grep. The
        lookup figures in it ("9 gated / 5 ungated") were wrong too — 12 and
        7 before this change — because a `list_items`/`read_item` pair was
        missed. Every count asserted from a grep that day was off.
        """
        fhir = _routes(API / 'fhir_valueset.py')
        lookup = _routes(API / 'lookup_tables.py')

        assert len(fhir) == 6, 'route functions'
        assert (API / 'fhir_valueset.py').read_text().count(
            '@fhir_valueset_bp.route') == 10, 'URL patterns'
        # 19 -> 20 with #935's narrow `whole-system-libs` read.
        assert len(lookup) == 20


class TestOptionThree:
    """The policy as built on 2026-11-03, in three tiers.

    #913 offered three options and this is the third: keep
    `$validate-code` public, gate what ENUMERATES. The reason is the
    asymmetry — `$validate-code` answers a question about a code the caller
    already holds, while `$expand` and the list routes hand over the
    material. One leaks a bit about something you brought; the others leak
    the selection.

    Chosen because it is the one that matches who actually calls what,
    measured 2026-11-02:

        $validate-code      cdr.pdhc, 7 files (its #857/#874 write gate)
        $expand / listings  alert.pdhc only, and alert holds a key anyway

    So gating the enumerating reads costs one consumer that needs a
    credential regardless, while gating `$validate-code` would have cost cdr
    a key on a hot path.
    """

    #: Routes that hand over a WHOLE selection, or the map to find one.
    #: Named individually rather than matched on `list_`/`expand_`, so each
    #: one is a decision rather than a side effect of a function name.
    ENUMERATING = {
        'search_valuesets',          # GET /ValueSet — the map
        'expand_valueset_by_id',     # every member of one
        'expand_valueset_by_parameters',
        'list_values',               # EVERY code in the store, the broadest
        'list_valuesets',
        'list_valueset_values',      # every member of one, native spelling
    }

    #: Deliberately public. Each line is a reason, not a permission.
    PUBLIC_BY_DESIGN = {
        # One code, yes/no. cdr.pdhc asks it on its write gate and alert's
        # candidate gate asks it per candidate; gating it would fail every
        # candidate closed as vocabulary_miss.
        'scoped_validate_code_by_id',
        'scoped_validate_code_by_post',
        # One resource's metadata, no expansion — a name, not a list.
        'read_valueset',
        'read_value',
        # The generic CRUD factory's reads. None carries the restricted
        # selection.
        #
        # THIS COMMENT USED TO SAY the six tables were all public and that
        # "gating these would have broken" cdr's whole-system gate. #925 gated
        # TWO of them — `concept-types` and `intended-uses` — so that is no
        # longer true of those two, and leaving the sentence would have it read
        # as a reason not to.
        #
        # The classification cannot tell them apart, and that is a real limit
        # worth naming rather than hiding: `_crud_routes` registers all six
        # tables through ONE pair of function names, so this set is per
        # FUNCTION and not per table. Which table is gated lives at the
        # registration line, as `public_read=` (#925) — that is where the
        # decision is, and this test cannot see it.
        #
        # Still true, and the reason the four open ones stay open: cdr.pdhc
        # reads /api/v1/lookup/canonical-libs on its #874 whole-system gate
        # with no credential, and request.pdhc reads response-types and units
        # the same way.
        'list_items',
        'read_item',
        # #935. The three fields cdr's #874 gate actually needs — library
        # name, canonical url, the flag — and nothing else. It exists so that
        # gate's dependency on an open read is EXPLICIT rather than
        # accidental: today it reads the whole table because the table happens
        # to be open, and gating that would silently degrade a deployed
        # security control to its hard-coded floor.
        'list_whole_system_libs',
    }

    def _all(self):
        out = []
        for module in ('fhir_valueset.py', 'lookup_tables.py'):
            out += [(module, *r) for r in _routes(API / module)]
        return out

    @pytest.mark.parametrize('name', sorted(ENUMERATING))
    def test_every_enumerating_read_is_gated(self, name):
        found = [(m, d) for m, n, _meth, d in self._all() if n == name]
        assert found, f'{name} no longer exists — update ENUMERATING'
        for module, decs in found:
            assert _gated(decs), (
                f'{module}:{name} enumerates and is ungated. It hands over a '
                'selection, and the Socialstyrelsen urval is registered here.'
            )

    @pytest.mark.parametrize('name', sorted(PUBLIC_BY_DESIGN))
    def test_the_public_ones_stay_public(self, name):
        found = [(m, d) for m, n, _meth, d in self._all() if n == name]
        assert found, f'{name} no longer exists — update PUBLIC_BY_DESIGN'
        for module, decs in found:
            assert not _gated(decs), (
                f'{module}:{name} became gated. If deliberate, check the '
                'consumer first: cdr.pdhc calls $validate-code and '
                '/lookup/canonical-libs, and alert asks $validate-code per '
                'candidate.'
            )

    def test_the_two_sets_do_not_overlap(self):
        assert not (self.ENUMERATING & self.PUBLIC_BY_DESIGN)

    def test_every_route_is_classified(self):
        """No route may be neither. A new one has to join a tier, which is
        the point — the convention was enacted in 24 decorators and written
        down nowhere, and that is how I came to read it as an oversight."""
        unclassified = [
            (m, n, sorted(meth)) for m, n, meth, d in self._all()
            if n not in self.ENUMERATING
            and n not in self.PUBLIC_BY_DESIGN
            and not (meth & WRITE_METHODS)
        ]
        assert unclassified == [], (
            f'unclassified read routes: {unclassified}. Add each to '
            'ENUMERATING or PUBLIC_BY_DESIGN, with the reason.'
        )


class TestWhatOptionThreeDoesNOTCover:
    """Measured while building it, and deliberately left alone.

    `GET /api/v1/CodeSystem` and `GET /api/v1/CodeSystem/<id>` call
    `_build_codesystem()`, whose `include_concepts` defaults to **True** —
    so both hand over plan's ENTIRE local Concept catalogue, ungated.

    That is a second enumerating surface and it is NOT what #913 decided.
    The restricted material is the Socialstyrelsen URVAL: which codes are
    flagged, which lives in the nineteen ValueSets and is now gated. A
    CodeSystem listing reveals plan's own concepts — PDHC's content, not a
    national selection under licence.

    So the scope ends here, on purpose. Extending the gate into CodeSystem
    would have been scope creep on a decision the operator made about
    ValueSets, and `$lookup` is on cdr's hot path the same way
    `$validate-code` is.

    This test exists so the fact is recorded rather than rediscovered, and
    so the day someone registers licence-restricted content as a CODE
    SYSTEM rather than a selection, the question is already written down.
    """

    def test_the_codesystem_search_is_still_ungated_and_still_enumerates(self):
        cs = API / 'fhir_codesystem.py'
        routes = {n: d for n, _m, d in _routes(cs)}
        assert 'search_codesystems' in routes
        assert not _gated(routes['search_codesystems']), (
            'the CodeSystem search became gated — if deliberate, good, but '
            'cdr.pdhc calls $lookup on this blueprint and the note in this '
            'test needs rewriting rather than deleting')
        src = cs.read_text()
        assert 'include_concepts: bool = True' in src, (
            'the default changed — if it is now False the enumeration is '
            'closed and this test should say so instead')
