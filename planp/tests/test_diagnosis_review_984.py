"""#984 section 1 — the diagnosis-review PlanDefinition step.

Contract: ~/T7_sidewinder/plans/984_diagnosis_review_contract.md. Covers the
code_scope grammar (refused by name, never dropped), the FHIR export shape,
the builder (editor) save + reload round-trip, and the API round-trip.
"""
import json
import re
import uuid

import pytest

from app.services import diagnosis_review as dr
from app.services.fhir_service import FHIRService
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB

CANON = "https://icd11.pdhc.se/fhir/ActivityDefinition/diagnosis-review"
EXT = "https://plan.pdhc.se/fhir/StructureDefinition/diagnosis-code-scope"


def _review(**over):
    act = {"is_diagnosis_review": True, "title": "Diagnosgenomgång diabetes",
           "description": "Årlig genomgång", "code_scope": ["5A1"],
           "timing_type": "repeat", "timing_frequency": 1, "timing_period": 1,
           "timing_period_unit": "a", "timing_bounds_mode": None}
    act.update(over)
    return act


def _codes(issues):
    return [i["code"] for i in issues]


# --- grammar ---------------------------------------------------------------

@pytest.mark.parametrize("prefix", [
    "5", "5A", "5A1", "5A11", "5A11.0", "5A11.Z", "BA00.00", "1A0", "CA23.3Y", "8",
])
def test_good_prefixes_accepted(prefix):
    assert dr.code_scope_prefix_error(prefix) is None
    assert dr.validate_actions([_review(code_scope=[prefix])]) == []


@pytest.mark.parametrize("prefix,why", [
    ("5A11&XS25", "&"),                 # cluster
    ("5A11/BA00", "/"),                 # cluster
    ("XS25", "extension"),              # extension code
    ("XA", "extension"),
    ("X", "extension"),
    ("5A*", "wildcard"),
    ("5A%", "wildcard"),
    ("5A?", "wildcard"),
    ("5a1", "lower case"),
    (" 5A1", "space"),
    ("5A1 ", "space"),
    ("", "empty"),
    ("I10", "I is not an ICD-11 letter"),
    ("O0", "O is not an ICD-11 letter"),
    ("5A111", "too long stem"),
    ("5A11.", "dot without extension"),
    ("5A11.000", "too many after dot"),
    ("5A.1.2", "two dots"),
])
def test_bad_prefixes_refused_by_name(prefix, why):
    issues = dr.validate_actions([_review(code_scope=[prefix])])
    assert _codes(issues) == ["E-DIAGREVIEW-SCOPE-INVALID"], why
    assert repr(prefix)[1:-1] in issues[0]["message"] or prefix in issues[0]["message"]
    assert issues[0]["action_index"] == 0


def test_every_bad_prefix_is_named_not_only_the_first():
    issues = dr.validate_actions([_review(code_scope=["5A1", "XS25", "5A11&XS25"])])
    msgs = " ".join(i["message"] for i in issues)
    assert len(issues) == 2 and "XS25" in msgs and "5A11&XS25" in msgs


def test_non_string_prefix_refused():
    assert _codes(dr.validate_actions([_review(code_scope=[51])])) == ["E-DIAGREVIEW-SCOPE-INVALID"]


def test_empty_scope_refused():
    assert _codes(dr.validate_actions([_review(code_scope=[])])) == ["E-DIAGREVIEW-SCOPE-EMPTY"]


@pytest.mark.parametrize("scope", [None, "5A1", {"a": 1}])
def test_missing_or_non_list_scope_refused(scope):
    act = _review(code_scope=scope)
    if scope is None:
        act.pop("code_scope")
    assert _codes(dr.validate_actions([act])) == ["E-DIAGREVIEW-SCOPE-MISSING"]


def test_review_cannot_also_be_a_form():
    assert "E-DIAGREVIEW-IS-FORM" in _codes(dr.validate_actions([_review(is_form=True)]))
    assert "E-DIAGREVIEW-IS-FORM" in _codes(dr.validate_actions([_review(form_guid=str(uuid.uuid4()))]))


def test_review_is_never_performed_by_the_patient():
    assert _codes(dr.validate_actions([_review(performer_type="Patient")])) == ["E-DIAGREVIEW-PERFORMER"]
    assert dr.validate_actions([_review(performer_type="Practitioner")]) == []


def test_review_carries_no_transactions():
    act = _review(transactions=[{"concept_guid": "x"}])
    assert _codes(dr.validate_actions([act])) == ["E-DIAGREVIEW-TRANSACTIONS"]
    assert dr.validate_actions([_review(transactions=[])]) == []


def test_code_scope_on_a_non_review_action_is_refused_not_ignored():
    for act in ({"title": "x", "code_scope": ["5A1"]},
                {"is_form": True, "form_guid": "g", "code_scope": ["5A1"]},
                {"is_diagnosis_review": False, "code_scope": ["5A1"]}):
        assert _codes(dr.validate_actions([act])) == ["E-DIAGREVIEW-SCOPE-WITHOUT-REVIEW"]


def test_non_boolean_flag_refused():
    assert _codes(dr.validate_actions([_review(is_diagnosis_review="true")])) == ["E-DIAGREVIEW-FLAG"]


def test_plain_and_form_actions_untouched():
    assert dr.validate_actions([{"title": "a", "transactions": []},
                                {"is_form": True, "form_guid": "g"}]) == []


def test_python_and_javascript_grammar_are_the_same_string():
    """The builder carries its own copy of the regex for the in-browser hint."""
    import pathlib
    tpl = (pathlib.Path(__file__).resolve().parents[1]
           / "app/templates/plandefinitions/builder.html").read_text()
    m = re.search(r"const DIAG_STEM_PREFIX_RE = /(.+)/;", tpl)
    assert m and m.group(1) == dr.STEM_PREFIX_RE.pattern


# --- FHIR export -------------------------------------------------------------

class _PD:
    """Minimal stand-in for the model; create_fhir_plandefinition reads attrs."""
    def __init__(self, actions):
        self.fhir_id = str(uuid.uuid4())
        self.guid = str(uuid.uuid4())
        self.action = json.dumps(actions)
        self.goal = None
        for a in ("name", "title", "status", "version", "type", "subject_type",
                  "publisher", "description", "purpose", "usage", "copyright",
                  "approval_date", "last_review_date", "effective_period_start",
                  "effective_period_end", "author", "editor", "reviewer", "endorser",
                  "related_artifact", "library", "form_definition_guid"):
            setattr(self, a, None)
        self.name = "t"


def _export(actions, app):
    with app.app_context():
        return FHIRService.create_fhir_plandefinition(_PD(actions))["action"]


def test_fhir_export_shape_exactly_as_contract(app):
    (act,) = _export([_review(code_scope=["5A1", "5A2"])], app)
    assert act == {
        "title": "Diagnosgenomgång diabetes",
        "description": "Årlig genomgång",
        "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/action-type",
                             "code": "update", "display": "Update"}]},
        "definitionCanonical": CANON,
        "participant": [{"type": "practitioner"}],
        "extension": [{"url": EXT, "valueString": "5A1"},
                      {"url": EXT, "valueString": "5A2"}],
        "timingTiming": {"repeat": {"frequency": 1, "period": 1, "periodUnit": "a"}},
    }


def test_fhir_timing_identical_to_a_form_with_the_same_fields(app):
    timing = {"timing_type": "repeat", "timing_frequency": 2, "timing_period": 3,
              "timing_period_unit": "mo", "timing_bounds_mode": "count",
              "timing_bounds_count": 4}
    form = {"is_form": True, "form_guid": str(uuid.uuid4()), "title": "f", **timing}
    f_act, r_act = _export([form, _review(**timing)], app)
    assert r_act["timingTiming"] == f_act["timingTiming"] == {
        "repeat": {"frequency": 2, "period": 3, "periodUnit": "mo", "count": 4}}
    # bounds by duration, too
    timing2 = dict(timing, timing_bounds_mode="duration", timing_bounds_duration_value=6,
                   timing_bounds_duration_unit="mo")
    f2, r2 = _export([dict(form, **timing2), _review(**timing2)], app)
    assert r2["timingTiming"] == f2["timingTiming"]
    # once -> no timingTiming, as for forms
    f3, r3 = _export([dict(form, timing_type="once"), _review(timing_type="once")], app)
    assert "timingTiming" not in r3 and "timingTiming" not in f3


def test_fhir_form_export_unchanged_by_refactor(app):
    g = str(uuid.uuid4())
    (f,) = _export([{"is_form": True, "form_guid": g, "title": "F"}], app)
    assert f == {"title": "F", "type": {"coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/action-type",
        "code": "collect-information", "display": "Collect information"}]},
        "definitionCanonical": f"https://plan.pdhc.se/api/v1/forms/{g}"}


# --- editor (builder) save + reload -----------------------------------------

def _builder_existing_actions(client, fhir_id):
    page = client.get(f"/plandefinitions/builder?plandef_id={fhir_id}").get_data(as_text=True)
    m = re.search(r"const EXISTING_ACTIONS = (.*);\n", page)
    return page, json.loads(m.group(1))


def test_builder_offers_the_swedish_step(client):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    page = client.get("/plandefinitions/builder").get_data(as_text=True)
    assert "Diagnosgenomgång (ICD-11)" in page
    assert "addDiagnosisReviewAction" in page
    assert "Kodområde (ICD-11)" in page


def test_editor_save_reload_and_resave_keeps_the_step(client, app):
    from app.models.fhir_models import PlanDefinition
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    title = f"dr-web-{uuid.uuid4().hex[:8]}"
    actions = [_review(code_scope=["5A1", "BA00.0"])]
    r = client.post("/plandefinitions/create", data={
        "title": title, "goal": "[]", "action": json.dumps(actions)})
    assert r.status_code == 302 and "/builder" not in r.headers["Location"]
    with app.app_context():
        pd = PlanDefinition.query.filter_by(title=title).one()
        fhir_id = pd.fhir_id
        assert pd.fhir_data["action"][0]["extension"] == [
            {"url": EXT, "valueString": "5A1"}, {"url": EXT, "valueString": "BA00.0"}]

    page, existing = _builder_existing_actions(client, fhir_id)
    assert existing == actions  # stored whole, not enriched from Activity

    # re-save what the editor loaded (the round-trip) — nothing lost
    r = client.post(f"/plandefinitions/{fhir_id}/edit", data={
        "title": title, "goal": "[]", "action": json.dumps(existing)})
    assert r.status_code == 302 and "/builder" not in r.headers["Location"]
    _, again = _builder_existing_actions(client, fhir_id)
    assert again == actions
    with app.app_context():
        pd = PlanDefinition.query.filter_by(fhir_id=fhir_id).one()
        assert pd.fhir_data["action"][0]["definitionCanonical"] == CANON


def test_editor_save_refuses_bad_scope_by_name(client, app):
    from app.models.fhir_models import PlanDefinition
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    title = f"dr-bad-{uuid.uuid4().hex[:8]}"
    r = client.post("/plandefinitions/create", data={
        "title": title, "goal": "[]",
        "action": json.dumps([_review(code_scope=["5A1", "XS25"])])}, follow_redirects=True)
    body = r.get_data(as_text=True)
    assert "E-DIAGREVIEW-SCOPE-INVALID" in body and "XS25" in body
    with app.app_context():
        assert PlanDefinition.query.filter_by(title=title).count() == 0


def test_editor_edit_refuses_empty_scope_and_changes_nothing(client, app):
    from app.models.fhir_models import PlanDefinition
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    title = f"dr-edit-{uuid.uuid4().hex[:8]}"
    client.post("/plandefinitions/create", data={
        "title": title, "goal": "[]", "action": json.dumps([_review()])})
    with app.app_context():
        fhir_id = PlanDefinition.query.filter_by(title=title).one().fhir_id
    r = client.post(f"/plandefinitions/{fhir_id}/edit", data={
        "title": title + "-renamed", "goal": "[]",
        "action": json.dumps([_review(code_scope=[])])}, follow_redirects=True)
    assert "E-DIAGREVIEW-SCOPE-EMPTY" in r.get_data(as_text=True)
    with app.app_context():
        pd = PlanDefinition.query.filter_by(fhir_id=fhir_id).one()
        assert pd.title == title
        assert json.loads(pd.action)[0]["code_scope"] == ["5A1"]


# --- API round-trip ------------------------------------------------------------

def test_api_create_read_update_round_trip(client):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    form = {"is_form": True, "form_guid": str(uuid.uuid4()), "title": "F"}
    actions = [form, _review(code_scope=["5A1"])]
    r = client.post("/api/v1/plandefinitions", json={
        "title": f"dr-api-{uuid.uuid4().hex[:8]}", "actions": actions})
    assert r.status_code == 201, r.get_json()
    body = r.get_json()
    guid, fhir_id = body["guid"], body["fhir_id"]
    assert json.loads(body["action"]) == actions

    fhir = client.get(f"/api/v1/PlanDefinition/{fhir_id}").get_json()
    assert fhir["action"][1]["definitionCanonical"] == CANON
    assert fhir["action"][0]["type"]["coding"][0]["code"] == "collect-information"

    actions[1]["code_scope"] = ["5A1", "5A2"]
    r = client.put(f"/api/v1/plandefinitions/{guid}", json={"actions": actions})
    assert r.status_code == 200, r.get_json()
    assert json.loads(client.get(f"/api/v1/plandefinitions/{guid}").get_json()["action"]) == actions
    fhir = client.get(f"/api/v1/PlanDefinition/{fhir_id}").get_json()
    assert [e["valueString"] for e in fhir["action"][1]["extension"]] == ["5A1", "5A2"]


def test_api_refuses_bad_scope_with_422(client):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post("/api/v1/plandefinitions", json={
        "title": f"dr-api-bad-{uuid.uuid4().hex[:8]}",
        "actions": [_review(code_scope=["5A*"])]})
    assert r.status_code == 422
    body = r.get_json()
    assert body["error"] == "diagnosis_review_invalid"
    assert body["issues"][0]["code"] == "E-DIAGREVIEW-SCOPE-INVALID" and "5A*" in body["issues"][0]["message"]

    ok = client.post("/api/v1/plandefinitions", json={
        "title": f"dr-api-ok-{uuid.uuid4().hex[:8]}", "actions": [_review()]}).get_json()
    r = client.put(f"/api/v1/plandefinitions/{ok['guid']}",
                   json={"actions": [_review(is_form=True)]})
    assert r.status_code == 422 and r.get_json()["issues"][0]["code"] == "E-DIAGREVIEW-IS-FORM"
    # unchanged
    assert json.loads(client.get(f"/api/v1/plandefinitions/{ok['guid']}").get_json()["action"]) == [_review()]


def test_builder_reload_keeps_scope_even_when_the_action_names_its_activity(client):
    """A stored review action that carries the `id` of its Activity row must
    still come back whole: enriching it from Activity would drop code_scope
    and is_diagnosis_review, and the next editor save would lose the step."""
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    body = client.post("/api/v1/plandefinitions", json={
        "title": f"dr-id-{uuid.uuid4().hex[:8]}", "actions": [_review()]}).get_json()
    act_guid = body["activities"][0]["guid"]
    with_id = [dict(_review(), id=act_guid)]
    assert client.put(f"/api/v1/plandefinitions/{body['guid']}",
                      json={"actions": with_id}).status_code == 200
    _, existing = _builder_existing_actions(client, body["fhir_id"])
    assert existing == with_id


def test_a_repeated_prefix_is_refused_by_name():
    from app.services.diagnosis_review import validate_actions
    issues = validate_actions([{"is_diagnosis_review": True, "title": "x", "code_scope": ["5A1", "BA0", "5A1"]}])
    assert [i["code"] for i in issues] == ["E-DIAGREVIEW-SCOPE-DUPLICATE"]
    assert "5A1" in issues[0]["message"]
    assert validate_actions([{"is_diagnosis_review": True, "title": "x", "code_scope": ["5A1", "BA0"]}]) == []
