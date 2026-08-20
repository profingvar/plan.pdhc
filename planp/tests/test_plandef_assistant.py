"""GA-2 — Claude-backed authoring assistant (epic #516). HTTP is mocked."""
import json

import pytest

from app import db
from app.models.concept_models import CanonicalLib, ResponseType, Unit
from app.services import plandef_assistant as a


def _goc(model, name_field, name, **extra):
    row = model.query.filter(getattr(model, name_field).ilike(name)).first()
    if row:
        return row
    row = model(**{name_field: name}, **extra)
    db.session.add(row)
    db.session.commit()
    return row


@pytest.fixture
def seed(app):
    with app.app_context():
        _goc(CanonicalLib, 'canonical_lib_name', 'LOINC-GA')
        _goc(ResponseType, 'response_type_name', 'Quantity')
        _goc(Unit, 'unit_name', 'mmHg')
        yield


class _FakeResp:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload) if isinstance(payload, dict) else str(payload)

    def json(self):
        return self._payload


def _anthropic_reply(text):
    return {"content": [{"type": "text", "text": text}]}


def _enable(app, monkeypatch, key='sk-test'):
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', True)
    monkeypatch.setitem(app.config, 'ANTHROPIC_API_KEY', key)
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_MODELS',
                        ['claude-sonnet-5', 'claude-opus-4-8'])
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_DEFAULT_MODEL',
                        'claude-sonnet-5')


def test_disabled_returns_reason(app):
    with app.app_context():
        # default config has the assistant disabled
        res = a.suggest_concept('track systolic blood pressure')
    assert res['assistant_available'] is False
    assert res['reason'] == a.R_DISABLED


def test_missing_key_degrades_gracefully(app, monkeypatch):
    with app.app_context():
        monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', True)
        monkeypatch.setitem(app.config, 'ANTHROPIC_API_KEY', '')
        monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_MODELS', ['claude-sonnet-5'])
        monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_DEFAULT_MODEL', 'claude-sonnet-5')
        res = a.suggest_concept('track systolic blood pressure')
    assert res['assistant_available'] is False
    assert res['reason'] == a.R_NO_KEY


def test_non_allowlisted_model_is_refused(app, monkeypatch):
    with app.app_context():
        _enable(app, monkeypatch)
        res = a.suggest_concept('track bp', model='gpt-4-turbo')
    assert res['assistant_available'] is False
    assert res['reason'] == a.R_BAD_MODEL


def test_happy_path_parses_and_self_validates(app, monkeypatch, seed):
    reply = _anthropic_reply(json.dumps({
        "response_type": "Quantity",
        "unit_ucum": "mm[Hg]",
        "unit_display": "mmHg",
        "canonical_lib": "LOINC-GA",
        "canonical_refnumber": "8480-6",
        "valueset_hint": None,
        "range_low": 60,
        "range_high": 250,
        "rationale": "Systolic BP is a quantity in mmHg; LOINC 8480-6.",
    }))
    with app.app_context():
        _enable(app, monkeypatch)
        monkeypatch.setattr(a.requests, 'post',
                            lambda *args, **kw: _FakeResp(200, reply))
        res = a.suggest_concept('track systolic blood pressure',
                                model='claude-sonnet-5', api_key='sk-test')
    assert res['assistant_available'] is True
    assert res['model_used'] == 'claude-sonnet-5'
    assert res['proposal']['canonical_refnumber'] == '8480-6'
    # self-check resolved names->guids and found a valid concept (no errors)
    assert res['validation']['ok'] is True
    assert res['resolution_notes'] == []


def test_malformed_reply_degrades(app, monkeypatch, seed):
    with app.app_context():
        _enable(app, monkeypatch)
        monkeypatch.setattr(
            a.requests, 'post',
            lambda *args, **kw: _FakeResp(200, _anthropic_reply("no json here at all")))
        res = a.suggest_concept('track bp', model='claude-sonnet-5', api_key='sk-test')
    assert res['assistant_available'] is False
    assert res['reason'] == a.R_MALFORMED


def test_http_error_degrades(app, monkeypatch, seed):
    with app.app_context():
        _enable(app, monkeypatch)
        monkeypatch.setattr(a.requests, 'post',
                            lambda *args, **kw: _FakeResp(500, {"error": "boom"}))
        res = a.suggest_concept('track bp', model='claude-sonnet-5', api_key='sk-test')
    assert res['assistant_available'] is False
    assert res['reason'] == a.R_NETWORK


def test_proposal_with_unknown_unit_is_flagged(app, monkeypatch, seed):
    # Model proposes a unit that isn't a lookup row -> resolution note + the
    # validator sees no unit -> E-UNIT-REQUIRED (self-check catches it).
    reply = _anthropic_reply(json.dumps({
        "response_type": "Quantity",
        "unit_ucum": "furlong",
        "unit_display": "furlong",
        "canonical_lib": "LOINC-GA",
        "canonical_refnumber": "8480-6",
        "rationale": "deliberately odd unit",
    }))
    with app.app_context():
        _enable(app, monkeypatch)
        monkeypatch.setattr(a.requests, 'post',
                            lambda *args, **kw: _FakeResp(200, reply))
        res = a.suggest_concept('track something', model='claude-sonnet-5', api_key='sk-test')
    assert res['assistant_available'] is True
    assert any('furlong' in n for n in res['resolution_notes'])
    codes = {i['code'] for i in res['validation']['issues']}
    assert 'E-UNIT-REQUIRED' in codes
