"""2026-11-20 — a PlanDefinition's version moves when its content does.

MMD_plan was edited several times and stayed 1.0.0, so nothing downstream
could say which version of the plan it was built from.
"""
from __future__ import annotations

import json
import uuid

import pytest

from app.services import plandef_version as pv
from tests.conftest import SAMPLE_ACCESS_BLOB, set_sso_session


@pytest.mark.parametrize("given,want", [
    ("1.0.0", "1.0.1"), ("1.1.0", "1.1.1"), ("1.1", "1.1.1"), ("2", "2.0.1"),
    (" 3.4.9 ", "3.4.10"), ("draft", None), ("1.0.0-rc1", None), ("", None)])
def test_bump_patch(given, want):
    assert pv.bump_patch(given) == want


class _PD:
    def __init__(self, **kw):
        for f in pv.CONTENT_FIELDS:
            setattr(self, f, None)
        self.version, self.goal, self.action = "1.0.0", "[]", '[{"a": 1, "b": 2}]'
        for k, v in kw.items():
            setattr(self, k, v)


def test_a_content_change_bumps_the_patch():
    pd = _PD(title="t"); snap = pv.Snapshot(pd)
    pd.action = '[{"a": 1, "b": 3}]'
    assert snap.settle(pd) is True and pd.version == "1.0.1"


def test_a_save_that_changes_nothing_keeps_the_version():
    pd = _PD(title="t"); snap = pv.Snapshot(pd)
    pd.action = '[{"b": 2, "a": 1}]'          # same JSON, other key order
    assert snap.settle(pd) is False and pd.version == "1.0.0"


def test_a_version_the_editor_typed_wins():
    pd = _PD(title="t"); snap = pv.Snapshot(pd)
    pd.title, pd.version = "t2", "2.0.0"
    assert snap.settle(pd) is False and pd.version == "2.0.0"


def test_an_unparseable_version_is_left_alone():
    pd = _PD(title="t", version="draft"); snap = pv.Snapshot(pd)
    pd.title = "t2"
    assert snap.settle(pd) is False and pd.version == "draft"


def _create(client, app, title):
    from app.models.fhir_models import PlanDefinition
    r = client.post("/plandefinitions/create", data={"title": title, "goal": "[]", "action": "[]"})
    assert r.status_code == 302
    with app.app_context():
        pd = PlanDefinition.query.filter_by(title=title).one()
        return pd.fhir_id, pd.guid


def _stored(app, guid):
    from app.models.fhir_models import PlanDefinition
    with app.app_context():
        pd = PlanDefinition.query.filter_by(guid=guid).one()
        return pd.version, pd.fhir_data.get("version")


def test_editor_save_with_a_change_bumps_version_and_fhir_export(client, app):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    title = f"ver-web-{uuid.uuid4().hex[:8]}"
    fhir_id, guid = _create(client, app, title)
    client.post(f"/plandefinitions/{fhir_id}/edit", data={
        "title": title, "version": "1.0.0", "goal": "[]", "action": "[]"})
    assert _stored(app, guid) == ("1.0.0", "1.0.0")          # nothing changed
    client.post(f"/plandefinitions/{fhir_id}/edit", data={
        "title": title, "description": "now with a description",
        "version": "1.0.0", "goal": "[]", "action": "[]"})
    assert _stored(app, guid) == ("1.0.1", "1.0.1")


def test_api_update_with_a_change_bumps_version(client, app):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post("/api/v1/plandefinitions", json={
        "title": f"ver-api-{uuid.uuid4().hex[:8]}", "actions": []})
    guid = r.get_json()["guid"]
    client.put(f"/api/v1/plandefinitions/{guid}", json={"description": "changed"})
    assert _stored(app, guid)[0] == "1.0.1"
    client.put(f"/api/v1/plandefinitions/{guid}", json={"description": "changed"})
    assert _stored(app, guid)[0] == "1.0.1"                   # same content again
    client.put(f"/api/v1/plandefinitions/{guid}", json={"description": "x", "version": "2.0.0"})
    assert _stored(app, guid)[0] == "2.0.0"
