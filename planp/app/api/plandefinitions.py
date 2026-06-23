import json
import re
import uuid as uuid_mod
import bleach
from datetime import date, timedelta
from flask import Blueprint, request, jsonify
from app import db, limiter
from app.api.auth import requires_role
from app.models.fhir_models import PlanDefinition
from app.models.activity_models import (
    Activity, Transaction, PlanDefinitionGoal, PlanDefinitionActivity,
)
from app.models.concept_models import Concept, Unit
from app.models.forms_models import FormDefinition
from app.services.fhir_service import FHIRService
from app.services.name_uniqueness import NameUniquenessService

PLAN_BASE = "https://plan.pdhc.se"

plandefinitions_bp = Blueprint('plandefinitions_api', __name__)
limiter.limit("200/minute")(plandefinitions_bp)


def _is_valid_uuid(val):
    try:
        uuid_mod.UUID(str(val))
        return True
    except (ValueError, AttributeError):
        return False


def _sanitize(val):
    if val is None:
        return None
    return bleach.clean(str(val).strip())


def _plandef_full_dict(pd):
    """Return PlanDefinition dict with goals and activities."""
    result = pd.to_dict()
    result['fhir_data'] = pd.fhir_data
    result['action'] = pd.action
    if pd.form_definition_guid:
        fd = FormDefinition.query.filter_by(guid=pd.form_definition_guid).first()
        result['form_definition'] = fd.to_summary() if fd else None
    goals = []
    for g in PlanDefinitionGoal.query.filter_by(plandefinition_guid=pd.guid) \
            .order_by(PlanDefinitionGoal.sort_order).all():
        gd = g.to_dict()
        if g.concept_guid:
            gd['concept_url'] = f"{PLAN_BASE}/api/v1/concepts/{g.concept_guid}"
        goals.append(gd)
    result['goals'] = goals

    # Single-goal inference: if the plan has exactly one Goal, every
    # activity implicitly measures against it. This lets downstream
    # consumers (request.pdhc sr_context, gateway report enrichment)
    # resolve "which measurement concept is this observation for?" from
    # the snapshot alone, without any Goal↔Activity FK in the model.
    # When multi-goal plans need explicit assignment, add a real
    # goal_guid column on Activity and populate it here instead.
    default_goal_guid = goals[0].get('guid') if len(goals) == 1 else None
    default_goal_concept_guid = goals[0].get('concept_guid') if len(goals) == 1 else None
    default_goal_concept_name = goals[0].get('concept_name') if len(goals) == 1 else None

    links = PlanDefinitionActivity.query.filter_by(plandefinition_guid=pd.guid) \
        .order_by(PlanDefinitionActivity.sort_order).all()
    activities = []
    for link in links:
        act = Activity.query.filter_by(guid=link.activity_guid).first()
        if act:
            d = act.to_dict()
            d['sort_order'] = link.sort_order
            d['goal_guid'] = default_goal_guid
            d['goal_concept_guid'] = default_goal_concept_guid
            d['goal_concept_name'] = default_goal_concept_name
            txns = []
            for t in Transaction.query.filter_by(activity_guid=act.guid).order_by(Transaction.sort_order).all():
                td = t.to_dict()
                if t.concept_guid:
                    concept = Concept.query.filter_by(guid=t.concept_guid).first()
                    td['concept_name'] = concept.concept_name if concept else ''
                    td['concept_url'] = f"{PLAN_BASE}/api/v1/concepts/{t.concept_guid}"
                    # Unit lives on the concept (termdefinition), not the
                    # transaction. Carry it forward so downstream consumers
                    # (request.pdhc dispatcher) emit a Quantity with the
                    # canonical unit envelope without having to refetch.
                    if concept and concept.unit:
                        unit = Unit.query.filter_by(guid=concept.unit).first()
                        if unit:
                            td['concept_unit_name'] = unit.unit_name
                else:
                    td['concept_name'] = ''
                # Carry the goal linkage onto the transaction too so
                # consumers don't have to walk activities → transactions
                # just to enrich a single observation.
                td['goal_guid'] = default_goal_guid
                td['goal_concept_guid'] = default_goal_concept_guid
                td['goal_concept_name'] = default_goal_concept_name
                txns.append(td)
            d['transactions'] = txns
            activities.append(d)
    result['activities'] = activities
    return result


@plandefinitions_bp.route('/plandefinitions', methods=['GET'])
def list_plandefinitions():
    page = max(1, request.args.get('page', 1, type=int))
    per_page = max(1, min(200, request.args.get('per_page', 20, type=int)))

    query = PlanDefinition.query

    # Archived plandefs are soft-deleted and must not surface in normal
    # listings (e.g. request.pdhc's ServiceRequest picker). This mirrors
    # the builder list view, which already filters archived out by default.
    # ?include_archived=1 opts back in for admin/audit use.
    if request.args.get('include_archived', '') != '1':
        query = query.filter(PlanDefinition.archived == False)

    status = request.args.get('status')
    if status:
        query = query.filter(PlanDefinition.status == status)

    search = request.args.get('search', '').strip()
    if search:
        like = f'%{search}%'
        query = query.filter(PlanDefinition.title.ilike(like))

    pagination = query.order_by(PlanDefinition.date_created.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        'items': [pd.to_dict() for pd in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
    }), 200


@plandefinitions_bp.route('/plandefinitions', methods=['POST'])
@requires_role('read_write')
def create_plandefinition():
    data = request.get_json(silent=True) or {}
    title = _sanitize(data.get('title'))
    if not title:
        return jsonify({'error': 'title is required'}), 400

    name = _sanitize(data.get('name')) or re.sub(r'\W+', '_', title.lower()).strip('_')
    error = NameUniquenessService.validate_name_for_manual_entry(
        name, PlanDefinition, 'name'
    )
    if error:
        return jsonify({'error': error}), 409

    # Compute effective period from validity_duration
    ep_start = ep_end = None
    validity = data.get('validity_duration', '').strip() if data.get('validity_duration') else None
    if validity:
        ep_start = date.today()
        try:
            parts = validity.split()
            amount = int(parts[0])
            unit = parts[1] if len(parts) > 1 else 'd'
            if unit in ('wk', 'w'):
                amount *= 7
            elif unit in ('mo', 'm'):
                amount *= 30
            ep_end = ep_start + timedelta(days=amount)
        except (ValueError, IndexError):
            pass

    goals_data = data.get('goals', [])
    actions_data = data.get('actions', [])

    plandef = PlanDefinition(
        title=title,
        name=name,
        description=_sanitize(data.get('description')),
        status=data.get('status', 'draft'),
        type=data.get('type'),
        version=data.get('version', '1.0.0'),
        subject_type=data.get('subject_type', 'Patient'),
        publisher=_sanitize(data.get('publisher')),
        purpose=_sanitize(data.get('purpose')),
        usage=_sanitize(data.get('usage')),
        copyright=_sanitize(data.get('copyright')),
        author=_sanitize(data.get('author')),
        editor=_sanitize(data.get('editor')),
        reviewer=_sanitize(data.get('reviewer')),
        endorser=_sanitize(data.get('endorser')),
        validity_duration=validity,
        effective_period_start=ep_start,
        effective_period_end=ep_end,
        form_definition_guid=data.get('form_definition_guid') or None,
        goal=json.dumps(goals_data),
        action=json.dumps(actions_data),
    )
    db.session.add(plandef)
    db.session.flush()

    # Persist goals
    for idx, g in enumerate(goals_data):
        goal = PlanDefinitionGoal(
            plandefinition_guid=plandef.guid,
            concept_guid=g.get('concept_guid'),
            concept_name=_sanitize(g.get('concept_name')),
            priority=g.get('priority'),
            target_type=g.get('target_type'),
            target_quantity=g.get('target_quantity'),
            target_operator=g.get('target_operator'),
            target_range_low=g.get('target_range_low'),
            target_range_high=g.get('target_range_high'),
            target_categorical_text=_sanitize(g.get('target_categorical_text')),
            target_value_guid=g.get('target_value_guid'),
            target_unit=g.get('target_unit'),
            sort_order=idx,
        )
        db.session.add(goal)

    # Persist activities + transactions
    for idx, act_data in enumerate(actions_data):
        activity = Activity(
            title=_sanitize(act_data.get('title')),
            description=_sanitize(act_data.get('description')),
            performer_type=act_data.get('performer_type'),
            subject_type=act_data.get('subject_type'),
            timing_type=act_data.get('timing_type'),
            timing_frequency=act_data.get('timing_frequency'),
            timing_period=act_data.get('timing_period'),
            timing_period_unit=act_data.get('timing_period_unit'),
            timing_duration=act_data.get('duration_value'),
            timing_duration_unit=act_data.get('duration_unit'),
            timing_bounds_mode=act_data.get('timing_bounds_mode'),
            timing_bounds_count=act_data.get('timing_bounds_count'),
            timing_bounds_duration_value=act_data.get('timing_bounds_duration_value'),
            timing_bounds_duration_unit=act_data.get('timing_bounds_duration_unit'),
            notes=_sanitize(act_data.get('notes')),
        )
        db.session.add(activity)
        db.session.flush()

        link = PlanDefinitionActivity(
            plandefinition_guid=plandef.guid,
            activity_guid=activity.guid,
            sort_order=idx,
        )
        db.session.add(link)

        for t_idx, txn_data in enumerate(act_data.get('transactions', [])):
            txn = Transaction(
                activity_guid=activity.guid,
                concept_guid=txn_data.get('concept_guid'),
                expected_value=_sanitize(txn_data.get('expected_value')),
                unit=txn_data.get('unit'),
                range_min=txn_data.get('range_min'),
                range_max=txn_data.get('range_max'),
                requirement_type=txn_data.get('requirement_type'),
                sort_order=t_idx,
            )
            db.session.add(txn)

    # Generate FHIR JSON
    db.session.flush()
    plandef.fhir_data = FHIRService.create_fhir_plandefinition(plandef)
    db.session.commit()

    return jsonify(_plandef_full_dict(plandef)), 201


@plandefinitions_bp.route('/plandefinitions/<guid>', methods=['GET'])
def read_plandefinition(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    pd = PlanDefinition.query.filter_by(guid=guid).first()
    if not pd:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(_plandef_full_dict(pd)), 200


@plandefinitions_bp.route('/plandefinitions/<guid>', methods=['PUT'])
@requires_role('read_write')
def update_plandefinition(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    pd = PlanDefinition.query.filter_by(guid=guid).first()
    if not pd:
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json(silent=True) or {}

    string_fields = ('title', 'name', 'description', 'type', 'version', 'subject_type',
                     'publisher', 'purpose', 'usage', 'copyright', 'author', 'editor',
                     'reviewer', 'endorser')
    for f in string_fields:
        if f in data:
            setattr(pd, f, _sanitize(data[f]))

    if 'status' in data:
        pd.status = data['status']

    if 'form_definition_guid' in data:
        pd.form_definition_guid = data['form_definition_guid'] or None

    if 'validity_duration' in data:
        validity = data['validity_duration']
        pd.validity_duration = validity
        if validity:
            pd.effective_period_start = date.today()
            try:
                parts = validity.split()
                amount = int(parts[0])
                unit = parts[1] if len(parts) > 1 else 'd'
                if unit in ('wk', 'w'):
                    amount *= 7
                elif unit in ('mo', 'm'):
                    amount *= 30
                pd.effective_period_end = pd.effective_period_start + timedelta(days=amount)
            except (ValueError, IndexError):
                pass

    # Update goals if provided
    if 'goals' in data:
        goals_data = data['goals']
        PlanDefinitionGoal.query.filter_by(plandefinition_guid=pd.guid).delete()
        pd.goal = json.dumps(goals_data)
        for idx, g in enumerate(goals_data):
            goal = PlanDefinitionGoal(
                plandefinition_guid=pd.guid,
                concept_guid=g.get('concept_guid'),
                concept_name=_sanitize(g.get('concept_name')),
                priority=g.get('priority'),
                target_type=g.get('target_type'),
                target_quantity=g.get('target_quantity'),
                target_operator=g.get('target_operator'),
                target_range_low=g.get('target_range_low'),
                target_range_high=g.get('target_range_high'),
                target_categorical_text=_sanitize(g.get('target_categorical_text')),
                target_value_guid=g.get('target_value_guid'),
                target_unit=g.get('target_unit'),
                sort_order=idx,
            )
            db.session.add(goal)

    # Update activities if provided
    if 'actions' in data:
        actions_data = data['actions']
        pd.action = json.dumps(actions_data)

        # Remove old links and orphaned activities
        old_links = PlanDefinitionActivity.query.filter_by(plandefinition_guid=pd.guid).all()
        old_guids = [l.activity_guid for l in old_links]
        PlanDefinitionActivity.query.filter_by(plandefinition_guid=pd.guid).delete()

        new_guids = set()
        for idx, act_data in enumerate(actions_data):
            act_guid = act_data.get('id')
            activity = Activity.query.filter_by(guid=act_guid).first() if act_guid else None

            if activity:
                activity.title = _sanitize(act_data.get('title', activity.title))
                activity.description = _sanitize(act_data.get('description', activity.description))
                activity.timing_type = act_data.get('timing_type')
                activity.timing_frequency = act_data.get('timing_frequency')
                activity.timing_period = act_data.get('timing_period')
                activity.timing_period_unit = act_data.get('timing_period_unit')
                activity.timing_duration = act_data.get('duration_value')
                activity.timing_duration_unit = act_data.get('duration_unit')
                activity.timing_bounds_mode = act_data.get('timing_bounds_mode')
                activity.timing_bounds_count = act_data.get('timing_bounds_count')
                activity.timing_bounds_duration_value = act_data.get('timing_bounds_duration_value')
                activity.timing_bounds_duration_unit = act_data.get('timing_bounds_duration_unit')
                Transaction.query.filter_by(activity_guid=activity.guid).delete()
            else:
                activity = Activity(
                    title=_sanitize(act_data.get('title')),
                    description=_sanitize(act_data.get('description')),
                    performer_type=act_data.get('performer_type'),
                    subject_type=act_data.get('subject_type'),
                    timing_type=act_data.get('timing_type'),
                    timing_frequency=act_data.get('timing_frequency'),
                    timing_period=act_data.get('timing_period'),
                    timing_period_unit=act_data.get('timing_period_unit'),
                    timing_duration=act_data.get('duration_value'),
                    timing_duration_unit=act_data.get('duration_unit'),
                    timing_bounds_mode=act_data.get('timing_bounds_mode'),
                    timing_bounds_count=act_data.get('timing_bounds_count'),
                    timing_bounds_duration_value=act_data.get('timing_bounds_duration_value'),
                    timing_bounds_duration_unit=act_data.get('timing_bounds_duration_unit'),
                    notes=_sanitize(act_data.get('notes')),
                )
                db.session.add(activity)
                db.session.flush()

            new_guids.add(activity.guid)
            link = PlanDefinitionActivity(
                plandefinition_guid=pd.guid,
                activity_guid=activity.guid,
                sort_order=idx,
            )
            db.session.add(link)

            for t_idx, txn_data in enumerate(act_data.get('transactions', [])):
                txn = Transaction(
                    activity_guid=activity.guid,
                    concept_guid=txn_data.get('concept_guid'),
                    expected_value=_sanitize(txn_data.get('expected_value')),
                    unit=txn_data.get('unit'),
                    range_min=txn_data.get('range_min'),
                    range_max=txn_data.get('range_max'),
                    requirement_type=txn_data.get('requirement_type'),
                    sort_order=t_idx,
                )
                db.session.add(txn)

        # Clean orphans
        for old_guid in old_guids:
            if old_guid not in new_guids:
                if PlanDefinitionActivity.query.filter_by(activity_guid=old_guid).count() == 0:
                    Transaction.query.filter_by(activity_guid=old_guid).delete()
                    Activity.query.filter_by(guid=old_guid).delete()

    # Regenerate FHIR JSON
    db.session.flush()
    pd.fhir_data = FHIRService.create_fhir_plandefinition(pd)
    db.session.commit()

    return jsonify(_plandef_full_dict(pd)), 200


@plandefinitions_bp.route('/plandefinitions/<guid>', methods=['DELETE'])
@requires_role('read_write')
def delete_plandefinition(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    pd = PlanDefinition.query.filter_by(guid=guid).first()
    if not pd:
        return jsonify({'error': 'Not found'}), 404

    # Clean up relational rows
    PlanDefinitionGoal.query.filter_by(plandefinition_guid=pd.guid).delete()
    links = PlanDefinitionActivity.query.filter_by(plandefinition_guid=pd.guid).all()
    for link in links:
        Transaction.query.filter_by(activity_guid=link.activity_guid).delete()
        other = PlanDefinitionActivity.query.filter(
            PlanDefinitionActivity.activity_guid == link.activity_guid,
            PlanDefinitionActivity.plandefinition_guid != pd.guid,
        ).count()
        if other == 0:
            Activity.query.filter_by(guid=link.activity_guid).delete()
    PlanDefinitionActivity.query.filter_by(plandefinition_guid=pd.guid).delete()

    db.session.delete(pd)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200
