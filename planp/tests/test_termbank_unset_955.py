"""#955 — an unset TERMBANK_BASE_URL reads as unset and is refused by name.

The client used to fall back to "https://termbank.pdhc.se", a name with no
vhost, so a lost .env key showed up only as "the New Concept widget finds no
codes". Now nothing is fabricated, no request is made, and every answer says
what is missing.
"""
import pytest
import requests

from app.services import termbank_client as tc
from app.services.termbank_client import NOT_CONFIGURED, TermbankClient


@pytest.fixture
def unset(monkeypatch):
    monkeypatch.delenv("TERMBANK_BASE_URL", raising=False)
    calls = []
    monkeypatch.setattr(tc.requests, "get", lambda *a, **k: calls.append(a) or pytest.fail("no request may be made"))
    return calls


def test_no_default_url_is_fabricated():
    assert not hasattr(tc, "DEFAULT_BASE_URL")


@pytest.mark.parametrize("value", [None, "", "   "])
def test_unset_or_blank_is_not_configured(monkeypatch, value):
    if value is None:
        monkeypatch.delenv("TERMBANK_BASE_URL", raising=False)
    else:
        monkeypatch.setenv("TERMBANK_BASE_URL", value)
    c = TermbankClient()
    assert c.configured is False and c.base_url is None


def test_search_refuses_by_name_without_calling(unset):
    assert TermbankClient().search("diabetes") == {"error": NOT_CONFIGURED, "results": [], "query": "diabetes"}
    assert unset == []


def test_lookup_and_health_return_nothing_without_calling(unset):
    c = TermbankClient()
    assert c.lookup("loinc", "4548-4") is None
    assert c.health() is None
    assert unset == []


def test_a_set_value_is_used_as_given(monkeypatch):
    monkeypatch.setenv("TERMBANK_BASE_URL", "http://host.docker.internal:9012/")
    c = TermbankClient()
    assert c.configured and c.base_url == "http://host.docker.internal:9012"


def test_the_proxies_answer_503_naming_the_variable(client, monkeypatch):
    monkeypatch.delenv("TERMBANK_BASE_URL", raising=False)
    monkeypatch.setattr(client.application, "termbank_client", TermbankClient())
    from tests.conftest import SAMPLE_READONLY_BLOB, set_sso_session
    set_sso_session(client, SAMPLE_READONLY_BLOB)  # plan-pages-only (2026-11-20)
    r = client.get("/api/v1/termbank/concept/loinc/4548-4")
    assert r.status_code == 503
    assert "TERMBANK_BASE_URL" in r.get_data(as_text=True)
    assert client.get("/api/v1/termbank/search?q=hba1c").get_json()["error"] == NOT_CONFIGURED
