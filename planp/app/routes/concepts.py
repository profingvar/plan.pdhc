import io
import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.api.auth import sso_login_required
from app import db
from app.models.concept_models import (
    Concept, CanonicalLib, ConceptType, ResponseType, Unit, ValueSet,
)
from app.services.name_uniqueness import NameUniquenessService
from app.services.concept_importer import (
    parse_xlsx, parse_csv, validate_and_import, compute_sha256, ImportError_,
)

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
            anchor_low_text=request.form.get('anchor_low_text') or None,
            anchor_high_text=request.form.get('anchor_high_text') or None,
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


@concepts_web_bp.route('/<guid>/edit', methods=['GET', 'POST'])
@sso_login_required
def edit_concept(guid):
    concept = Concept.query.filter_by(guid=guid).first_or_404()

    if request.method == 'POST':
        name = request.form.get('concept_name', '').strip()

        # Check uniqueness only if name changed
        if name != concept.concept_name:
            error = NameUniquenessService.validate_name_for_manual_entry(
                name, Concept, 'concept_name'
            )
            if error:
                flash(error, 'error')
                return redirect(url_for('concepts_web.edit_concept', guid=guid))

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
                    return redirect(url_for('concepts_web.edit_concept', guid=guid))

        concept.concept_name = name
        concept.canonical_lib = request.form.get('canonical_lib')
        concept.canonical_refnumber = request.form.get('canonical_refnumber')
        concept.concept_display_text = request.form.get('concept_display_text')
        concept.concept_explain = request.form.get('concept_explain')
        concept.concept_type = request.form.get('concept_type') or None
        concept.response_type = response_type_guid or None
        concept.unit = request.form.get('unit') or None
        concept.valueset = valueset_guid or None
        concept.range_low = request.form.get('range_low', type=float)
        concept.range_high = request.form.get('range_high', type=float)
        concept.anchor_low_text = request.form.get('anchor_low_text') or None
        concept.anchor_high_text = request.form.get('anchor_high_text') or None

        db.session.commit()
        flash('Concept updated.', 'success')
        return redirect(url_for('concepts_web.view_concept', guid=guid))

    return render_template('concepts/edit.html',
                           concept=concept,
                           canonical_libs=CanonicalLib.query.all(),
                           concept_types=ConceptType.query.all(),
                           response_types=ResponseType.query.all(),
                           units=Unit.query.all(),
                           valuesets=ValueSet.query.all())


@concepts_web_bp.route('/<guid>/delete', methods=['POST'])
@sso_login_required
def delete_concept(guid):
    concept = Concept.query.filter_by(guid=guid).first_or_404()
    db.session.delete(concept)
    db.session.commit()
    flash(f'Concept "{concept.concept_name}" deleted.', 'success')
    return redirect(url_for('concepts_web.list_concepts'))


@concepts_web_bp.route('/import', methods=['GET', 'POST'])
@sso_login_required
def import_concepts_page():
    """Admin upload page for bulk-importing concepts (ticket #134).

    Requires SU admin: a non-admin SSO user reaches the page but the
    POST handler refuses with a flashed error.
    """
    blob = session.get('sso_user') or {}
    is_admin = bool(blob.get('is_su_admin'))
    report = None

    if request.method == 'POST':
        if not is_admin:
            flash('Only SU admins can bulk-import concepts.', 'error')
            return redirect(url_for('concepts_web.import_concepts_page'))

        f = request.files.get('file')
        if not f or not f.filename:
            flash('Please choose a file to upload.', 'error')
            return redirect(url_for('concepts_web.import_concepts_page'))

        raw = f.read()
        if not raw:
            flash('Uploaded file is empty.', 'error')
            return redirect(url_for('concepts_web.import_concepts_page'))

        sha = compute_sha256(raw)
        ext = os.path.splitext(f.filename)[1].lower()
        try:
            if ext == '.xlsx':
                rows = parse_xlsx(io.BytesIO(raw))
            elif ext == '.csv':
                rows = parse_csv(io.BytesIO(raw))
            else:
                flash(f'Unsupported file extension {ext!r}; use .xlsx or .csv', 'error')
                return redirect(url_for('concepts_web.import_concepts_page'))
        except ImportError_ as e:
            flash(f'Parse error: {e}', 'error')
            return redirect(url_for('concepts_web.import_concepts_page'))

        dry_run = (request.form.get('dry_run', '').strip().lower() == 'true')
        operator = blob.get('email') or blob.get('user_guid') or 'sso:unknown'
        report = validate_and_import(
            rows, operator=operator, filename=f.filename,
            sha256=sha, dry_run=dry_run,
        )
        if report['rejected']:
            flash(
                f'{report["summary"]["n_accepted"]} imported, '
                f'{report["summary"]["n_rejected"]} rejected.',
                'warning',
            )
        else:
            flash(
                f'{report["summary"]["n_accepted"]} concept(s) imported '
                + ('(dry-run).' if report['summary']['dry_run'] else 'successfully.'),
                'success',
            )

    return render_template('concepts/import.html', report=report)
