"""#912 — a service key granted `admin`, because the role was never compared.

`requires_role` checked the service-key path FIRST and returned on a valid
key, before `min_role` was read:

    sk = _service_key_outcome()
    if sk is True:
        return fn(*args, **kwargs)        # <- here
    ...
    required = role_levels.get(min_role, 0)   # never reached

So `@requires_role('admin')` and `@requires_role('read_only')` were the same
decorator for a key holder, and the decorator's own docstring promised
`admin → is_su_admin` — a gate that existed only on the SSO branch. The #804
shape, in an authorisation decorator, which is the worst place for it:
the docstring is what a reader consults to decide whether a route is
protected.

**It was noticed and mis-framed.** `test_loader_identity_retired.py`'s
docstring says "plan.pdhc checks the service-key path FIRST in requires_role,
so a valid key skipped the SSO gate entirely" — true, and the conclusion drawn
was that loader.pdhc's key was dangerous rather than that the comparison was
missing for everyone.

**Why it was a ticket and not an incident.** One entry in `KNOWN_SERVICES`,
and an unset key admits nobody — platform CLAUDE.md records
`SIM_PDHC_SERVICE_KEY` as unset in production. The fix landed before alert.pdhc
is added to that dict (its step 2.b-ii), which would have made the
role-blindness reachable with a key that needs only `read_write`.

The one admin route is `concepts.import_concepts` — bulk import into the
terminology store that cdr, gateway and ips all resolve codes against.
"""
from __future__ import annotations

import pytest

from app.api.auth import KNOWN_SERVICES, ROLE_LEVELS, _service_key_outcome

SOURCE = 'sim.pdhc'
KEY = 'sim-key-for-912-tests'


@pytest.fixture
def keyed(app):
    """The sim key configured, so the key path is live."""
    old = app.config.get('SIM_PDHC_SERVICE_KEY')
    app.config['SIM_PDHC_SERVICE_KEY'] = KEY
    yield app
    if old is None:
        app.config.pop('SIM_PDHC_SERVICE_KEY', None)
    else:
        app.config['SIM_PDHC_SERVICE_KEY'] = old


def _hdr(key=KEY, source=SOURCE):
    h = {}
    if source is not None:
        h['X-Source-Service'] = source
    if key is not None:
        h['X-Service-Key'] = key
    return h


class TestTheOutcomeResolvesARole:
    def test_a_valid_key_returns_its_GRANTED_ROLE_not_True(self, keyed):
        with keyed.test_request_context('/', headers=_hdr()):
            out = _service_key_outcome()
        assert out == 'read_write'
        assert out is not True, (
            "returning True is what made min_role decorative — the role has "
            "to come back so it can be compared"
        )

    def test_no_headers_still_falls_through_to_SSO(self, keyed):
        with keyed.test_request_context('/'):
            assert _service_key_outcome() is None

    def test_a_wrong_key_is_False(self, keyed):
        with keyed.test_request_context('/', headers=_hdr(key='nope')):
            assert _service_key_outcome() is False

    def test_an_unknown_source_is_False(self, keyed):
        with keyed.test_request_context('/', headers=_hdr(source='hittepa')):
            assert _service_key_outcome() is False

    def test_half_the_headers_is_False_not_None(self, keyed):
        """Present-but-incomplete must not fall through to SSO as though no
        key had been offered."""
        with keyed.test_request_context('/', headers=_hdr(key=None)):
            assert _service_key_outcome() is False
        with keyed.test_request_context('/', headers=_hdr(source=None)):
            assert _service_key_outcome() is False

    def test_an_UNSET_configured_key_admits_nobody(self, app):
        """Even when the caller sends an empty key, which is what a
        half-configured sibling sends."""
        old = app.config.get('SIM_PDHC_SERVICE_KEY')
        app.config['SIM_PDHC_SERVICE_KEY'] = ''
        try:
            with app.test_request_context('/', headers=_hdr(key='')):
                assert _service_key_outcome() is False
            with app.test_request_context('/', headers=_hdr(key='anything')):
                assert _service_key_outcome() is False
        finally:
            if old is None:
                app.config.pop('SIM_PDHC_SERVICE_KEY', None)
            else:
                app.config['SIM_PDHC_SERVICE_KEY'] = old


class TestNothingGrantsAdmin:
    def test_no_service_is_granted_admin(self):
        """The default, asserted so adding one is a visible decision rather
        than a line nobody reviewed."""
        granted = {role for _var, role in KNOWN_SERVICES.values()}
        assert 'admin' not in granted, (
            f"a service is granted admin: {KNOWN_SERVICES}. The one admin "
            "route is concepts.import_concepts — bulk import into the "
            "terminology store cdr, gateway and ips resolve codes against."
        )

    def test_every_granted_role_is_a_real_role(self):
        for _var, role in KNOWN_SERVICES.values():
            assert role in ROLE_LEVELS, role

    def test_the_entry_shape_is_the_pair(self):
        for name, entry in KNOWN_SERVICES.items():
            assert isinstance(entry, tuple) and len(entry) == 2, (name, entry)


class TestTheRoleIsActuallyCompared:
    """The finding, made into a guard.

    Driven through `requires_role` itself rather than through a route, so the
    assertion is about the decorator and does not depend on which routes
    happen to carry which level today — one admin route exists, and a test
    that pinned it would start passing vacuously the day it moved.
    """

    def _probe(self, keyed, min_role, headers):
        from app.api.auth import requires_role
        calls = []

        @requires_role(min_role)
        def _view():
            calls.append(True)
            return 'ok'

        with keyed.test_request_context('/', headers=headers):
            out = _view()
        return calls, out

    def test_a_read_write_key_is_ADMITTED_on_read_write(self, keyed):
        calls, _ = self._probe(keyed, 'read_write', _hdr())
        assert calls == [True]

    def test_a_read_write_key_is_ADMITTED_on_read_only(self, keyed):
        calls, _ = self._probe(keyed, 'read_only', _hdr())
        assert calls == [True]

    def test_a_read_write_key_is_REFUSED_on_ADMIN(self, keyed):
        """THE test. Before #912 this passed through, and no test could have
        caught it because the behaviour it asserts did not exist — which is
        why five months of green tests did not notice (compare #729)."""
        calls, out = self._probe(keyed, 'admin', _hdr())
        assert calls == [], "a read_write key reached an admin route"
        body, status = out
        assert status == 403
        payload = body.get_json()
        assert payload['granted_role'] == 'read_write'
        assert payload['required_role'] == 'admin'

    def test_the_refusal_NAMES_both_roles(self, keyed):
        """So a sibling's log says what it had and what it needed, instead
        of sending someone to re-check a key that was never wrong."""
        _calls, out = self._probe(keyed, 'admin', _hdr())
        payload = out[0].get_json()
        assert 'granted_role' in payload and 'required_role' in payload

    def test_an_INVALID_key_is_403_on_every_level(self, keyed):
        for lvl in ('read_only', 'read_write', 'admin'):
            calls, out = self._probe(keyed, lvl, _hdr(key='wrong'))
            assert calls == []
            assert out[1] == 403

    def test_no_key_at_all_still_reaches_the_SSO_branch(self, keyed):
        """Not 403: absent headers must fall through, or every anonymous
        request would be told its credentials were invalid."""
        calls, out = self._probe(keyed, 'read_only', {})
        assert calls == []
        assert out[1] == 401


class TestTheCompareIsConstantTime:
    def test_hmac_compare_digest_is_used_and_plain_equality_is_not(self):
        """sso's own /api/auth/me/service says why in a comment: the
        endpoint gates every service's token validation, and `!=` leaks the
        secret by timing. The same argument applies here.

        Asserted on the PARSED code, with comments and docstrings gone.
        The first version searched the raw source and failed — because the
        function's own comment explains the fix by quoting the expression
        it replaced. That is the FOURTH time in one session I have written
        a source guard that matches the comment explaining the guard
        (#885 once, #904 twice). `ast.unparse` drops comments entirely,
        which is the instrument that actually answers the question.
        """
        import ast
        import inspect
        from app.api import auth

        tree = ast.parse(inspect.getsource(auth._service_key_outcome).lstrip())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if (node.body and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Constant)
                        and isinstance(node.body[0].value.value, str)):
                    node.body[0].value.value = ""
        code = ast.unparse(tree)

        assert 'compare_digest' in code
        # The expression itself, in CODE: a Compare of key against expected
        # with NotEq. Searching for the text would be the same mistake again.
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare) and any(
                    isinstance(op, ast.NotEq) for op in node.ops):
                names = {n.id for n in ast.walk(node)
                         if isinstance(n, ast.Name)}
                assert not {'key', 'expected'} <= names, (
                    "a plain != between key and expected is back")


class TestTheDocstringNowHolds:
    def test_requires_role_documents_the_service_key_path(self):
        """The #804 half of this finding: the docstring promised
        `admin → is_su_admin` and described only the SSO branch."""
        from app.api.auth import requires_role
        doc = requires_role.__doc__ or ''
        assert 'SERVICE KEY' in doc
        assert '#912' in doc
