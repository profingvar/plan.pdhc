from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.api.auth import sso_login_required
from app import db
from app.models.concept_models import (
    Concept, CanonicalLib, ConceptType, ResponseType, Unit, ValueSet,
)
from app.services.name_uniqueness import NameUniquenessService

concepts_web_bp = Blueprint('concepts_web', __name__, url_prefix='/concepts')


@concepts_web_bp.route('/')
def list_concepts():
    page = max(1, request.args.get('page', 1, type=int))
    pagination = Concept.query.order_by(Concept.concept_name).paginate(
        page=page, per_page=50, error_out=False
    )
    return render_template('concepts/list.html', pagination=pagination)


@concepts_web_bp.route('/create', methods=['GET', 'POST'])
@sso_login_required
def create_concept():
    if request.method == 'POST':
        name = request.form.get('concept_name', '').strip()
        canon_lib = request.form.get('canonical_lib')

        error = NameUniquenessService.validate_name_for_manual_entry(
            name, Concept, 'concept_name'
        )
        if error:
            flash(error, 'error')
            return redirect(url_for('concepts_web.create_concept'))

        # Business rule: single-choice response types require a valueset
        response_type_guid = request.form.get('response_type')
        valueset_guid = request.form.get('valueset')
        if response_type_guid:
            rt = ResponseType.query.filter_by(guid=response_type_guid).first()
            if rt and rt.response_type_name.lower() in (
                'single choice', 'single_choice', 'singlechoice', 'categorical'
            ):
                if not valueset_guid:
                    flash('Single-choice response type requires a ValueSet.', 'error')
                    return redirect(url_for('concepts_web.create_concept'))

        concept = Concept(
            concept_name=name,
            canonical_lib=canon_lib,
            canonical_refnumber=request.form.get('canonical_refnumber'),
            concept_display_text=request.form.get('concept_display_text'),
            concept_explain=request.form.get('concept_explain'),
            concept_type=request.form.get('concept_type') or None,
            response_type=response_type_guid or None,
            unit=request.form.get('unit') or None,
            valueset=valueset_guid or None,
            range_low=request.form.get('range_low', type=float),
            range_high=request.form.get('range_high', type=float),
        )
        db.session.add(concept)
        db.session.commit()
        flash('Concept created.', 'success')
        return redirect(url_for('concepts_web.list_concepts'))

    return render_template('concepts/create.html',
                           canonical_libs=CanonicalLib.query.all(),
                           concept_types=ConceptType.query.all(),
                           response_types=ResponseType.query.all(),
                           units=Unit.query.all(),
                           valuesets=ValueSet.query.all())


@concepts_web_bp.route('/<guid>')
def view_concept(guid):
    concept = Concept.query.filter_by(guid=guid).first_or_404()
    return render_template('concepts/view.html', concept=concept)
