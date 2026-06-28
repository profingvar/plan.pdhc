"""Tests — #294 RFC decision D3 dual-name emission in to_dict().

plan.pdhc's PlanDefinition / Concept / Transaction / Activity / Goal
serializers emit BOTH the generic `guid` AND the role-specific name
(`plan_definition_guid`, `concept_guid`, `transaction_guid`,
`activity_guid`, `goal_guid`) during the transition. `guid` will be
dropped after one release cycle.
"""


def test_plan_definition_to_dict_emits_both(app, db_session):
    from app.models.fhir_models import PlanDefinition
    pd = PlanDefinition(name='t1d-followup', title='T1D follow-up',
                        type='clinical', status='active')
    d = pd.to_dict()
    assert 'guid' in d
    assert 'plan_definition_guid' in d
    assert d['guid'] == d['plan_definition_guid']


def test_concept_to_dict_emits_both(app, db_session):
    from app.models.concept_models import Concept
    c = Concept(concept_name='HbA1c', canonical_lib='loinc',
                canonical_refnumber='4548-4')
    d = c.to_dict()
    assert 'guid' in d
    assert 'concept_guid' in d
    assert d['guid'] == d['concept_guid']


def test_transaction_to_dict_emits_both(app, db_session):
    from app.models.activity_models import Transaction
    t = Transaction(activity_guid='act-1', concept_guid='c-1')
    d = t.to_dict()
    assert 'guid' in d
    assert 'transaction_guid' in d
    assert d['guid'] == d['transaction_guid']


def test_activity_to_dict_emits_both(app, db_session):
    from app.models.activity_models import Activity
    a = Activity(title='Sample collection')
    d = a.to_dict()
    assert 'guid' in d
    assert 'activity_guid' in d
    assert d['guid'] == d['activity_guid']


def test_goal_to_dict_emits_both(app, db_session):
    from app.models.activity_models import PlanDefinitionGoal
    g = PlanDefinitionGoal(plandefinition_guid='pd-1',
                            concept_guid='c-1',
                            priority='high-priority',
                            target_type='quantity')
    d = g.to_dict()
    assert 'guid' in d
    assert 'goal_guid' in d
    assert d['guid'] == d['goal_guid']
