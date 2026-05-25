import json
import re
from datetime import date, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.api.auth import sso_login_required
from app import db
from app.models.fhir_models import PlanDefinition
from app.models.activity_models import (
    Activity, Transaction, PlanDefinitionGoal, PlanDefinitionActivity,
)
from app.models.concept_models import (
    Concept, CanonicalLib, ConceptType, ResponseType, Unit, PlanDefType,
    ValueSet, ValueSetValue, ValueCatalog,
)
from app.models.forms_models import FormDefinition, Questionnaire
from app.services.fhir_service import FHIRService
from app.services.name_uniqueness import NameUniquenessService

plandef_web_bp = Blueprint('plandefinitions_web', __name__, url_prefix='/plandefinitions')


@plandef_web_bp.route('/')
def list_plandefs():
    page = max(1, request.args.get('page', 1, type=int))
    show_all = request.args.get('show_all', '') == '1'
    query = PlanDefinition.query
    if not show_all:
        query = query.filter(PlanDefinition.archived == False)
    pagination = query.order_by(
        PlanDefinition.date_created.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    # Build a lookup of form definition titles by guid
    form_guids = [pd.form_definition_guid for pd in pagination.items if pd.form_definition_guid]
    form_lookup = {}
    if form_guids:
        forms = FormDefinition.query.filter(FormDefinition.guid.in_(form_guids)).all()
        form_lookup = {f.guid: f.title for f in forms}
    return render_template('plandefinitions/list.html', pagination=pagination,
                           form_lookup=form_lookup, show_all=show_all)


def _build_existing_data(plandef):
    """Build the full goals/actions structure for an existing PlanDefinition."""
    goals = []
    for g in PlanDefinitionGoal.query.filter_by(
        plandefinition_guid=plandef.guid
    ).order_by(PlanDefinitionGoal.sort_order).all():
        goals.append(g.to_dict())

    # Load actions from the stored JSON (preserves both regular and form actions)
    actions = []
    if plandef.action:
        try:
            actions = json.loads(plandef.action)
            if not isinstance(actions, list):
                actions = []
        except (json.JSONDecodeError, TypeError):
            actions = []

    # For regular (non-form) actions, enrich with relational Activity data
    enriched = []
    for act_data in actions:
        if act_data.get('is_form'):
            enriched.append(act_data)
        else:
            # Try to match with relational Activity by id/guid
            act_guid = act_data.get('id')
            if act_guid:
                act = Activity.query.filter_by(guid=act_guid).first()
                if act:
                    d = act.to_dict()
                    d['sort_order'] = act_data.get('sort_order', 0)
                    txns = Transaction.query.filter_by(
                        activity_guid=act.guid
                    ).order_by(Transaction.sort_order).all()
                    d['transactions'] = [t.to_dict() for t in txns]
                    enriched.append(d)
                    continue
            enriched.append(act_data)

    return goals, enriched


@plandef_web_bp.route('/builder')
@sso_login_required
def builder():
    plandef_id = request.args.get('plandef_id')
    plandef = None
    existing_goals = []
    existing_actions = []
    if plandef_id:
        plandef = PlanDefinition.query.filter_by(fhir_id=plandef_id).first()
        if plandef:
            existing_goals, existing_actions = _build_existing_data(plandef)

    concepts = Concept.query.order_by(Concept.concept_name).all()
    units = Unit.query.order_by(Unit.unit_name).all()
    valuesets = ValueSet.query.order_by(ValueSet.valueset_name).all()
    plandef_types = PlanDefType.query.order_by(PlanDefType.plandef_type_name).all()
    form_definitions = FormDefinition.query.filter(
        FormDefinition.archived == False
    ).order_by(FormDefinition.title).all()

    # Build list of produced (active) questionnaires for the form picker
    from sqlalchemy import func
    latest_version = (
        db.session.query(
            Questionnaire.form_guid,
            func.max(Questionnaire.version).label('max_version')
        ).group_by(Questionnaire.form_guid).subquery()
    )
    produced_forms = (
        Questionnaire.query
        .join(latest_version,
              (Questionnaire.form_guid == latest_version.c.form_guid) &
              (Questionnaire.version == latest_version.c.max_version))
        .filter(Questionnaire.archived == False)
        .order_by(Questionnaire.title).all()
    )

    return render_template(
        'plandefinitions/builder.html',
        plandef=plandef,
        concepts_json=json.dumps([c.to_dict() for c in concepts]),
        units_json=json.dumps([u.to_dict() for u in units]),
        valuesets_json=json.dumps([v.to_dict() for v in valuesets]),
        plandef_types_json=json.dumps([t.to_dict() for t in plandef_types]),
        existing_goals_json=json.dumps(existing_goals),
        existing_actions_json=json.dumps(existing_actions),
        form_definitions=form_definitions,
        produced_forms=produced_forms,
    )


@plandef_web_bp.route('/create', methods=['POST'])
@sso_login_required
def create_plandef():
    title = request.form.get('title', '').strip()
    if not title:
        flash('Title is required.', 'error')
        return redirect(url_for('plandefinitions_web.builder'))

    goal_json = request.form.get('goal', '[]')
    action_json = request.form.get('action', '[]')

    try:
        goals_data = json.loads(goal_json)
        actions_data = json.loads(action_json)
    except json.JSONDecodeError:
        flash('Invalid JSON in goals or actions.', 'error')
        return redirect(url_for('plandefinitions_web.builder'))

    # Derive name
    name = request.form.get('name', '').strip()
    if not name:
        name = re.sub(r'\W+', '_', title.lower()).strip('_')

    error = NameUniquenessService.validate_name_for_manual_entry(
        name, PlanDefinition, 'name'
    )
    if error:
        flash(error, 'error')
        return redirect(url_for('plandefinitions_web.builder'))

    # Compute effective period
    ep_start = None
    ep_end = None
    validity = request.form.get('validity_duration', '').strip()
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

    # Create PlanDefinition row
    plandef = PlanDefinition(
        title=title,
        name=name,
        description=request.form.get('description'),
        status=request.form.get('status', 'draft'),
        type=request.form.get('type'),
        version=request.form.get('version', '1.0.0'),
        subject_type=request.form.get('subject_type', 'Patient'),
        publisher=request.form.get('publisher'),
        purpose=request.form.get('purpose'),
        usage=request.form.get('usage'),
        copyright=request.form.get('copyright'),
        author=request.form.get('author'),
        editor=request.form.get('editor'),
        reviewer=request.form.get('reviewer'),
        endorser=request.form.get('endorser'),
        form_definition_guid=request.form.get('form_definition_guid') or None,
        validity_duration=validity or None,
        effective_period_start=ep_start,
        effective_period_end=ep_end,
        goal=goal_json,
        action=action_json,
    )
    db.session.add(plandef)
    db.session.flush()  # get guid

    # Persist goals relationally
    for idx, g in enumerate(goals_data):
        goal = PlanDefinitionGoal(
            plandefinition_guid=plandef.guid,
            concept_guid=g.get('concept_guid'),
            concept_name=g.get('concept_name'),
            priority=g.get('priority'),
            target_type=g.get('target_type'),
            target_quantity=g.get('target_quantity'),
            target_operator=g.get('target_operator'),
            target_range_low=g.get('target_range_low'),
            target_range_high=g.get('target_range_high'),
            target_categorical_text=g.get('target_categorical_text'),
            target_value_guid=g.get('target_value_guid'),
            target_unit=g.get('target_unit'),
            sort_order=idx,
        )
        db.session.add(goal)

    # Persist activities + transactions
    for idx, act_data in enumerate(actions_data):
        activity = Activity(
            guid=act_data.get('id') or None,
            title=act_data.get('title'),
            description=act_data.get('description'),
            performer_type=act_data.get('performer_type'),
            subject_type=act_data.get('subject_type'),
            timing_type=act_data.get('timing_type'),
            timing_frequency=act_data.get('timing_frequency'),
            timing_period=act_data.get('timing_period'),
            timing_period_unit=act_data.get('timing_period_unit'),
            timing_bounds_mode=act_data.get('timing_bounds_mode'),
            timing_bounds_count=act_data.get('timing_bounds_count'),
            timing_duration=act_data.get('duration_value'),
            timing_duration_unit=act_data.get('duration_unit'),
            timing_bounds_duration_value=act_data.get('timing_bounds_duration_value'),
            timing_bounds_duration_unit=act_data.get('timing_bounds_duration_unit'),
            notes=act_data.get('notes'),
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
                expected_value=txn_data.get('expected_value'),
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

    flash('PlanDefinition created.', 'success')
    return redirect(url_for('plandefinitions_web.view_plandef', fhir_id=plandef.fhir_id))


@plandef_web_bp.route('/<fhir_id>')
def view_plandef(fhir_id):
    plandef = PlanDefinition.query.filter_by(fhir_id=fhir_id).first_or_404()
    linked_form = None
    if plandef.form_definition_guid:
        linked_form = FormDefinition.query.filter_by(guid=plandef.form_definition_guid).first()
    return render_template('plandefinitions/view.html', plandef=plandef, linked_form=linked_form)


@plandef_web_bp.route('/<fhir_id>/edit', methods=['POST'])
@sso_login_required
def edit_plandef(fhir_id):
    plandef = PlanDefinition.query.filter_by(fhir_id=fhir_id).first_or_404()

    plandef.title = request.form.get('title', plandef.title)
    plandef.description = request.form.get('description', plandef.description)
    plandef.status = request.form.get('status', plandef.status)
    plandef.type = request.form.get('type', plandef.type)
    plandef.version = request.form.get('version', plandef.version)
    plandef.publisher = request.form.get('publisher', plandef.publisher)
    plandef.form_definition_guid = request.form.get('form_definition_guid') or None

    goal_json = request.form.get('goal', '[]')
    action_json = request.form.get('action', '[]')

    try:
        goals_data = json.loads(goal_json)
        actions_data = json.loads(action_json)
    except json.JSONDecodeError:
        flash('Invalid JSON.', 'error')
        return redirect(url_for('plandefinitions_web.builder', plandef_id=fhir_id))

    plandef.goal = goal_json
    plandef.action = action_json

    # Delete old relational rows
    PlanDefinitionGoal.query.filter_by(plandefinition_guid=plandef.guid).delete()
    old_links = PlanDefinitionActivity.query.filter_by(plandefinition_guid=plandef.guid).all()
    old_activity_guids = [l.activity_guid for l in old_links]
    PlanDefinitionActivity.query.filter_by(plandefinition_guid=plandef.guid).delete()

    # Recreate goals
    for idx, g in enumerate(goals_data):
        goal = PlanDefinitionGoal(
            plandefinition_guid=plandef.guid,
            concept_guid=g.get('concept_guid'),
            concept_name=g.get('concept_name'),
            priority=g.get('priority'),
            target_type=g.get('target_type'),
            target_quantity=g.get('target_quantity'),
            target_operator=g.get('target_operator'),
            target_range_low=g.get('target_range_low'),
            target_range_high=g.get('target_range_high'),
            target_categorical_text=g.get('target_categorical_text'),
            target_value_guid=g.get('target_value_guid'),
            target_unit=g.get('target_unit'),
            sort_order=idx,
        )
        db.session.add(goal)

    # Recreate activities + transactions
    new_activity_guids = set()
    for idx, act_data in enumerate(actions_data):
        act_guid = act_data.get('id')
        activity = None
        if act_guid:
            activity = Activity.query.filter_by(guid=act_guid).first()
        if activity:
            activity.title = act_data.get('title', activity.title)
            activity.description = act_data.get('description', activity.description)
            activity.timing_type = act_data.get('timing_type')
            activity.timing_frequency = act_data.get('timing_frequency')
            activity.timing_period = act_data.get('timing_period')
            activity.timing_period_unit = act_data.get('timing_period_unit')
            activity.timing_bounds_mode = act_data.get('timing_bounds_mode')
            activity.timing_bounds_count = act_data.get('timing_bounds_count')
            activity.timing_duration = act_data.get('duration_value')
            activity.timing_duration_unit = act_data.get('duration_unit')
            activity.timing_bounds_duration_value = act_data.get('timing_bounds_duration_value')
            activity.timing_bounds_duration_unit = act_data.get('timing_bounds_duration_unit')
            # Clear old transactions
            Transaction.query.filter_by(activity_guid=activity.guid).delete()
        else:
            activity = Activity(
                title=act_data.get('title'),
                description=act_data.get('description'),
                performer_type=act_data.get('performer_type'),
                subject_type=act_data.get('subject_type'),
                timing_type=act_data.get('timing_type'),
                timing_frequency=act_data.get('timing_frequency'),
                timing_period=act_data.get('timing_period'),
                timing_period_unit=act_data.get('timing_period_unit'),
                timing_bounds_mode=act_data.get('timing_bounds_mode'),
                timing_bounds_count=act_data.get('timing_bounds_count'),
                timing_duration=act_data.get('duration_value'),
                timing_duration_unit=act_data.get('duration_unit'),
                timing_bounds_duration_value=act_data.get('timing_bounds_duration_value'),
                timing_bounds_duration_unit=act_data.get('timing_bounds_duration_unit'),
                notes=act_data.get('notes'),
            )
            db.session.add(activity)
            db.session.flush()

        new_activity_guids.add(activity.guid)

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
                expected_value=txn_data.get('expected_value'),
                unit=txn_data.get('unit'),
                range_min=txn_data.get('range_min'),
                range_max=txn_data.get('range_max'),
                requirement_type=txn_data.get('requirement_type'),
                sort_order=t_idx,
            )
            db.session.add(txn)

    # Clean up orphaned activities
    for old_guid in old_activity_guids:
        if old_guid not in new_activity_guids:
            other_links = PlanDefinitionActivity.query.filter_by(activity_guid=old_guid).count()
            if other_links == 0:
                Transaction.query.filter_by(activity_guid=old_guid).delete()
                Activity.query.filter_by(guid=old_guid).delete()

    # Regenerate FHIR JSON
    plandef.fhir_data = FHIRService.create_fhir_plandefinition(plandef)
    db.session.commit()

    flash('PlanDefinition updated.', 'success')
    return redirect(url_for('plandefinitions_web.view_plandef', fhir_id=fhir_id))


@plandef_web_bp.route('/<fhir_id>/delete', methods=['POST'])
@sso_login_required
def delete_plandef(fhir_id):
    plandef = PlanDefinition.query.filter_by(fhir_id=fhir_id).first_or_404()

    # Clean up relational rows
    PlanDefinitionGoal.query.filter_by(plandefinition_guid=plandef.guid).delete()
    links = PlanDefinitionActivity.query.filter_by(plandefinition_guid=plandef.guid).all()
    for link in links:
        Transaction.query.filter_by(activity_guid=link.activity_guid).delete()
        other = PlanDefinitionActivity.query.filter(
            PlanDefinitionActivity.activity_guid == link.activity_guid,
            PlanDefinitionActivity.plandefinition_guid != plandef.guid,
        ).count()
        if other == 0:
            Activity.query.filter_by(guid=link.activity_guid).delete()
    PlanDefinitionActivity.query.filter_by(plandefinition_guid=plandef.guid).delete()

    db.session.delete(plandef)
    db.session.commit()
    flash('PlanDefinition deleted.', 'success')
    return redirect(url_for('plandefinitions_web.list_plandefs'))


@plandef_web_bp.route('/<fhir_id>/archive', methods=['POST'])
@sso_login_required
def archive_plandef(fhir_id):
    plandef = PlanDefinition.query.filter_by(fhir_id=fhir_id).first_or_404()
    plandef.archived = not plandef.archived
    db.session.commit()
    label = 'archived' if plandef.archived else 'unarchived'
    flash(f'PlanDefinition {label}.', 'success')
    return redirect(request.referrer or url_for('plandefinitions_web.list_plandefs'))


@plandef_web_bp.route('/<fhir_id>/export')
def export_plandef(fhir_id):
    plandef = PlanDefinition.query.filter_by(fhir_id=fhir_id).first_or_404()
    resource = plandef.fhir_data or FHIRService.create_fhir_plandefinition(plandef)
    return jsonify(resource), 200, {
        'Content-Disposition': f'attachment; filename=PlanDefinition_{fhir_id}.json'
    }
