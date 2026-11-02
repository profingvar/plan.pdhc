"""plan's terminology surface: reads public, writes gated — #913.

I filed #913 reading this as ten routes somebody forgot to gate. Measured
properly, it is a deliberate and consistent pattern:

    app/api/fhir_valueset.py     6 read route functions (10 URL patterns —
                                 four declare both `$expand` and its
                                 `%24`-encoded spelling), ungated,
                                 0 write routes
    app/api/lookup_tables.py    19 route functions: 12 write routes, all
                                 @requires_role('read_write'), and 7
                                 ungated GET-only reads

Thirteen open reads, twelve gated writes, no exceptions. (#913 said nine
and five. Both figures came from grep counts and both were wrong — the
finding is unchanged and slightly stronger.) That is a design, not
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

        And a correction to #913, which said "ten FHIR ValueSet routes".
        There are **six route FUNCTIONS carrying ten URL patterns**: four
        functions declare two `@route` decorators each, for the literal
        `$expand` / `$validate-code` and the `%24`-encoded spelling of the
        same operation. My ticket counted DECORATORS with grep and called
        them routes.

        It changes nothing about the finding and it is the kind of number a
        security ticket should get right, so both are asserted here with
        the reason they differ.
        """
        fhir = _routes(API / 'fhir_valueset.py')
        lookup = _routes(API / 'lookup_tables.py')

        assert len(fhir) == 6, 'route functions'
        decorators = (API / 'fhir_valueset.py').read_text().count(
            '@fhir_valueset_bp.route')
        assert decorators == 10, 'URL patterns'

        # 19 route functions: 12 gated writes, 7 ungated GET-only reads.
        # My ticket said 9 and 5. Both came from grep counts taken before
        # this file existed, and both were wrong — there is a
        # `list_items`/`read_item` pair I had not seen. The FINDING is
        # unchanged and slightly stronger; the numbers were not.
        assert len(lookup) == 19
        assert sum(1 for _n, _m, d in lookup if _gated(d)) == 12
        assert sum(1 for _n, m, d in lookup
                   if m == {'GET'} and not _gated(d)) == 7

    def test_EVERY_ungated_route_is_GET_only(self):
        """The clean statement of the invariant, and the one worth having:
        zero ungated writes anywhere in the terminology surface."""
        for module in ('lookup_tables.py', 'fhir_valueset.py'):
            for name, methods, decs in _routes(API / module):
                if _gated(decs) or name in FHIR_READ_OPERATIONS:
                    continue
                assert methods == {'GET'}, (module, name, sorted(methods))
