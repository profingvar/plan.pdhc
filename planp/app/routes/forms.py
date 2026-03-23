"""Forms web UI — list and detail views for FHIR Questionnaires."""
from flask import Blueprint, render_template, request
from app import db
from app.api.auth import sso_login_required
from app.models.forms_models import Questionnaire, QuestionnaireResponse
from sqlalchemy import func

forms_web_bp = Blueprint('forms_web', __name__)


@forms_web_bp.route('/forms')
@sso_login_required
def list_forms():
    status_filter = request.args.get('status', '')

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

    if status_filter:
        query = query.filter(Questionnaire.status == status_filter)

    forms = query.order_by(Questionnaire.title).all()

    return render_template('forms/list.html', forms=forms, status_filter=status_filter)


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
