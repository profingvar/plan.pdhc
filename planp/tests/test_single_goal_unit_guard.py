"""2026-11-19 (MMD_plan): the single-goal inference stamps the goal only on
transactions measuring in the goal's unit. Before, cgm_mean_glucose (mmol/L)
was stamped on sleep (h), blood pressure (mmHg), anxiety and stress, and the
gateway stored all of them as glucose."""
import pytest


@pytest.fixture
def plan(app, db_session):
    from app.models.activity_models import (Activity, PlanDefinitionActivity,
                                            PlanDefinitionGoal, Transaction)
    from app.models.concept_models import CanonicalLib, Concept, Unit
    from app.models.fhir_models import PlanDefinition
    lib = CanonicalLib(canonical_lib_name="t-lib-goalguard")
    mmol, h = Unit(unit_name="mmol/L-gg"), Unit(unit_name="h-gg")
    db_session.add_all([lib, mmol, h]); db_session.flush()
    gluc = Concept(canonical_lib=lib.guid, concept_name="gluc", unit=mmol.guid)
    cgm = Concept(canonical_lib=lib.guid, concept_name="cgm", unit=mmol.guid)
    sleep = Concept(canonical_lib=lib.guid, concept_name="sleep", unit=h.guid)
    anx = Concept(canonical_lib=lib.guid, concept_name="anx")
    pd = PlanDefinition(name="mmd", title="MMD", status="active", version="1.0.0")
    a1, a2 = Activity(title="CGM"), Activity(title="Sleep")
    db_session.add_all([gluc, cgm, sleep, anx, pd, a1, a2]); db_session.flush()
    db_session.add_all([
        PlanDefinitionGoal(plandefinition_guid=pd.guid, concept_guid=gluc.guid, concept_name="gluc"),
        Transaction(activity_guid=a1.guid, concept_guid=cgm.guid),
        Transaction(activity_guid=a2.guid, concept_guid=sleep.guid),
        Transaction(activity_guid=a2.guid, concept_guid=anx.guid),
        PlanDefinitionActivity(plandefinition_guid=pd.guid, activity_guid=a1.guid, sort_order=0),
        PlanDefinitionActivity(plandefinition_guid=pd.guid, activity_guid=a2.guid, sort_order=1)])
    db_session.commit()
    return pd, gluc


def test_goal_only_on_same_unit_transactions(plan):
    from app.api.plandefinitions import _plandef_full_dict
    pd, gluc = plan
    acts = {a["title"]: a for a in _plandef_full_dict(pd)["activities"]}
    assert acts["CGM"]["goal_concept_guid"] == gluc.guid
    assert acts["CGM"]["transactions"][0]["goal_concept_guid"] == gluc.guid
    assert acts["Sleep"]["goal_concept_guid"] is None
    assert [t["goal_concept_guid"] for t in acts["Sleep"]["transactions"]] == [None, None]
