"""Forms web UI — list, detail, produce, publish, retire for FHIR Questionnaires."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.api.auth import sso_login_required
from app.models.forms_models import Questionnaire, QuestionnaireResponse
from app.models.concept_models import Concept
from app.models.fhir_models import PlanDefinition
from app.services.forms_service import (
    resolve_question_set, build_fhir_questionnaire, validate_fhir_questionnaire,
    create_or_append_form_version, publish_form_version,
    QuestionServiceError, BuildError, ValidationError, PublishError,
)
from sqlalchemy import func

forms_web_bp = Blueprint('forms_web', __name__)


@forms_web_bp.route('/forms')
@sso_login_required
def list_forms():
    status_filter = request.args.get('status', '')
    show_all = request.args.get('show_all', '') == '1'

    latest_version = (
        db.session.query(
            Questionnaire.form_guid,
            func.max(Questionnaire.version).label('max_version')
        ).group_by(Questionnaire.form_guid).subquery()
    )

    query = (
        Questionnaire.query
        .join(latest_version,
              (Questionnaire.form_guid == latest_version.c.form_guid) &
              (Questionnaire.version == latest_version.c.max_version))
    )

    if not show_all:
        query = query.filter(Questionnaire.archived == False)

    if status_filter:
        query = query.filter(Questionnaire.status == status_filter)

    forms = query.order_by(Questionnaire.title).all()

    return render_template('forms/list.html', forms=forms, status_filter=status_filter,
                           show_all=show_all)


@forms_web_bp.route('/forms/<form_guid>')
@sso_login_required
def form_detail(form_guid):
    version = request.args.get('version', type=int)

    if version:
        questionnaire = Questionnaire.query.filter_by(
            form_guid=form_guid, version=version
        ).first_or_404()
    else:
        questionnaire = Questionnaire.query.filter_by(
            form_guid=form_guid
        ).order_by(Questionnaire.version.desc()).first_or_404()

    all_versions = Questionnaire.query.filter_by(
        form_guid=form_guid
    ).order_by(Questionnaire.version.desc()).all()

    response_counts = dict(
        db.session.query(
            QuestionnaireResponse.form_version,
            func.count(QuestionnaireResponse.id)
        ).filter_by(form_guid=form_guid)
        .group_by(QuestionnaireResponse.form_version)
        .all()
    )

    return render_template('forms/detail.html',
                           form=questionnaire,
                           all_versions=all_versions,
                           response_counts=response_counts)


# ---------------------------------------------------------------------------
# Produce form (GET = picker page, POST = run pipeline)
# ---------------------------------------------------------------------------

@forms_web_bp.route('/forms/produce', methods=['GET', 'POST'])
@sso_login_required
def produce_form():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'draft')
        source_type = request.form.get('source_type', 'concept_guids')

        if not title and source_type == 'concept_guids':
            flash('Title is required when producing from concepts.', 'error')
            return redirect(url_for('forms_web.produce_form'))

        try:
            if source_type == 'plandefinition':
                plandef_guid = request.form.get('plandefinition_guid', '').strip()
                if not plandef_guid:
                    flash('Select a PlanDefinition.', 'error')
                    return redirect(url_for('forms_web.produce_form'))

                external_questions = resolve_question_set(
                    plandef_guid, source_type='plandefinition'
                )
                if not title:
                    title = external_questions.get('title', '')
                if not description:
                    description = external_questions.get('description', '')
                production_key = f'plandef:{plandef_guid}'
            else:
                concept_guids = request.form.getlist('concept_guids')
                if not concept_guids:
                    flash('Select at least one concept.', 'error')
                    return redirect(url_for('forms_web.produce_form'))

                external_questions = resolve_question_set(
                    concept_guids, source_type='concept_guids'
                )
                production_key = None

            external_questions['title'] = title
            external_questions['description'] = description

            meta = {'title': title, 'description': description}
            form_guid = Questionnaire.generate_guid()

            fhir_q = build_fhir_questionnaire(
                form_guid=form_guid, version=1, status=status,
                meta=meta, external_questions=external_questions,
            )
            validate_fhir_questionnaire(fhir_q)

            result = create_or_append_form_version(
                form_guid=form_guid, content_fingerprint=None,
                production_key=production_key, meta=meta, status=status,
                fhir_questionnaire=fhir_q,
            )

            flash(f'Form "{title}" produced (v{result["version"]}).', 'success')
            return redirect(url_for('forms_web.form_detail', form_guid=result['form_guid']))

        except (QuestionServiceError, BuildError, ValidationError) as e:
            flash(f'Production failed: {e.message}', 'error')
            return redirect(url_for('forms_web.produce_form'))

    # GET — render picker page
    concepts = (
        Concept.query
        .order_by(Concept.concept_name)
        .all()
    )
    plandefinitions = (
        PlanDefinition.query
        .order_by(PlanDefinition.title)
        .all()
    )
    return render_template('forms/produce.html',
                           concepts=concepts,
                           plandefinitions=plandefinitions)


# ---------------------------------------------------------------------------
# Publish (draft → active)
# ---------------------------------------------------------------------------

@forms_web_bp.route('/forms/<form_guid>/publish', methods=['POST'])
@sso_login_required
def publish_form(form_guid):
    version = request.form.get('version', type=int)
    try:
        publish_form_version(form_guid, version=version)
        flash('Form published.', 'success')
    except PublishError as e:
        flash(f'Publish failed: {e.message}', 'error')
    return redirect(url_for('forms_web.form_detail', form_guid=form_guid))


# ---------------------------------------------------------------------------
# Retire (active → retired)
# ---------------------------------------------------------------------------

@forms_web_bp.route('/forms/<form_guid>/retire', methods=['POST'])
@sso_login_required
def retire_form(form_guid):
    version = request.form.get('version', type=int)
    q = Questionnaire.query.filter_by(form_guid=form_guid, version=version).first()
    if not q:
        flash('Form version not found.', 'error')
        return redirect(url_for('forms_web.list_forms'))

    if q.status != 'active':
        flash('Only active forms can be retired.', 'error')
        return redirect(url_for('forms_web.form_detail', form_guid=form_guid))

    q.status = 'retired'
    db.session.commit()
    flash(f'Form v{version} retired.', 'success')
    return redirect(url_for('forms_web.form_detail', form_guid=form_guid))


# ---------------------------------------------------------------------------
# Edit form metadata (draft only, no responses)
# ---------------------------------------------------------------------------

@forms_web_bp.route('/forms/<form_guid>/edit', methods=['GET', 'POST'])
@sso_login_required
def edit_form(form_guid):
    version = request.args.get('version', type=int)

    if version:
        questionnaire = Questionnaire.query.filter_by(
            form_guid=form_guid, version=version
        ).first_or_404()
    else:
        questionnaire = Questionnaire.query.filter_by(
            form_guid=form_guid
        ).order_by(Questionnaire.version.desc()).first_or_404()

    # Only draft forms with no responses can be edited
    response_count = QuestionnaireResponse.query.filter_by(
        form_guid=form_guid, form_version=questionnaire.version
    ).count()

    if questionnaire.status != 'draft':
        flash('Only draft forms can be edited. Produce a new version instead.', 'error')
        return redirect(url_for('forms_web.form_detail', form_guid=form_guid))

    if response_count > 0:
        flash('This version has responses and cannot be edited. Produce a new version instead.', 'error')
        return redirect(url_for('forms_web.form_detail', form_guid=form_guid))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title:
            flash('Title is required.', 'error')
            return redirect(url_for('forms_web.edit_form', form_guid=form_guid,
                                    version=questionnaire.version))

        questionnaire.title = title
        questionnaire.description = description

        # Update the FHIR JSON title/description too
        fhir = questionnaire.fhir_json
        if isinstance(fhir, dict):
            fhir['title'] = title
            fhir['description'] = description
            from sqlalchemy.orm.attributes import flag_modified
            flag_modified(questionnaire, 'fhir_json')

        db.session.commit()
        flash('Form updated.', 'success')
        return redirect(url_for('forms_web.form_detail', form_guid=form_guid,
                                version=questionnaire.version))

    return render_template('forms/edit.html', form=questionnaire)


# ---------------------------------------------------------------------------
# Delete form version (draft only, no responses) or all versions
# ---------------------------------------------------------------------------

@forms_web_bp.route('/forms/<form_guid>/delete', methods=['POST'])
@sso_login_required
def delete_form(form_guid):
    delete_all = request.form.get('delete_all') == 'true'

    if delete_all:
        # Check no active/retired versions exist
        non_draft = Questionnaire.query.filter(
            Questionnaire.form_guid == form_guid,
            Questionnaire.status != 'draft'
        ).count()
        if non_draft > 0:
            flash('Cannot delete all versions — some are active or retired.', 'error')
            return redirect(url_for('forms_web.form_detail', form_guid=form_guid))

        # Check no responses exist for any version
        responses = QuestionnaireResponse.query.filter_by(form_guid=form_guid).count()
        if responses > 0:
            flash('Cannot delete — form has responses.', 'error')
            return redirect(url_for('forms_web.form_detail', form_guid=form_guid))

        Questionnaire.query.filter_by(form_guid=form_guid).delete()
        db.session.commit()
        flash('All form versions deleted.', 'success')
        return redirect(url_for('forms_web.list_forms'))

    # Delete single version
    version = request.form.get('version', type=int)
    q = Questionnaire.query.filter_by(form_guid=form_guid, version=version).first()
    if not q:
        flash('Form version not found.', 'error')
        return redirect(url_for('forms_web.list_forms'))

    if q.status != 'draft':
        flash('Only draft versions can be deleted.', 'error')
        return redirect(url_for('forms_web.form_detail', form_guid=form_guid))

    response_count = QuestionnaireResponse.query.filter_by(
        form_guid=form_guid, form_version=version
    ).count()
    if response_count > 0:
        flash('Cannot delete — this version has responses.', 'error')
        return redirect(url_for('forms_web.form_detail', form_guid=form_guid))

    db.session.delete(q)
    db.session.commit()
    flash(f'Form v{version} deleted.', 'success')

    # If other versions remain, show the latest
    remaining = Questionnaire.query.filter_by(form_guid=form_guid).first()
    if remaining:
        return redirect(url_for('forms_web.form_detail', form_guid=form_guid))
    return redirect(url_for('forms_web.list_forms'))


@forms_web_bp.route('/forms/<form_guid>/archive', methods=['POST'])
@sso_login_required
def archive_form(form_guid):
    """Toggle archived flag on all versions of a form."""
    forms = Questionnaire.query.filter_by(form_guid=form_guid).all()
    if not forms:
        flash('Form not found.', 'error')
        return redirect(url_for('forms_web.list_forms'))
    new_state = not forms[0].archived
    for f in forms:
        f.archived = new_state
    db.session.commit()
    label = 'archived' if new_state else 'unarchived'
    flash(f'Form {label}.', 'success')
    return redirect(request.referrer or url_for('forms_web.list_forms'))
