from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.api.auth import sso_login_required
from app import db
from app.models.concept_models import (
    CanonicalLib, ConceptType, ResponseType, Unit, PlanDefType, IntendedUse,
)

lookup_web_bp = Blueprint('lookup_web', __name__)


# ─── Canonical Libraries ───────────────────────────────────────────────────────

@lookup_web_bp.route('/canonical-libs/')
def list_canonical_libs():
    items = CanonicalLib.query.order_by(CanonicalLib.canonical_lib_name).all()
    return render_template('lookup/canonical_libs/list.html', items=items)


@lookup_web_bp.route('/canonical-libs/create', methods=['GET', 'POST'])
@sso_login_required
def create_canonical_lib():
    if request.method == 'POST':
        name = request.form.get('canonical_lib_name', '').strip()
        if not name:
            flash('Name is required.', 'error')
            return redirect(url_for('lookup_web.create_canonical_lib'))
        if CanonicalLib.query.filter_by(canonical_lib_name=name).first():
            flash('A canonical library with that name already exists.', 'error')
            return redirect(url_for('lookup_web.create_canonical_lib'))
        item = CanonicalLib(
            canonical_lib_name=name,
            canonical_lib_display_text=request.form.get('canonical_lib_display_text'),
            canonical_lib_url=request.form.get('canonical_lib_url'),
            author=request.form.get('author'),
        )
        db.session.add(item)
        db.session.commit()
        flash('Canonical library created.', 'success')
        return redirect(url_for('lookup_web.list_canonical_libs'))
    return render_template('lookup/canonical_libs/create.html')


@lookup_web_bp.route('/canonical-libs/<guid>')
def view_canonical_lib(guid):
    item = CanonicalLib.query.filter_by(guid=guid).first_or_404()
    return render_template('lookup/canonical_libs/view.html', item=item)


@lookup_web_bp.route('/canonical-libs/<guid>/edit', methods=['GET', 'POST'])
@sso_login_required
def edit_canonical_lib(guid):
    item = CanonicalLib.query.filter_by(guid=guid).first_or_404()
    if request.method == 'POST':
        item.canonical_lib_name = request.form.get('canonical_lib_name', item.canonical_lib_name).strip()
        item.canonical_lib_display_text = request.form.get('canonical_lib_display_text')
        item.canonical_lib_url = request.form.get('canonical_lib_url')
        item.author = request.form.get('author')
        item.vers_number = (item.vers_number or 1) + 1
        db.session.commit()
        flash('Canonical library updated.', 'success')
        return redirect(url_for('lookup_web.view_canonical_lib', guid=guid))
    return render_template('lookup/canonical_libs/edit.html', item=item)


@lookup_web_bp.route('/canonical-libs/<guid>/delete', methods=['POST'])
@sso_login_required
def delete_canonical_lib(guid):
    item = CanonicalLib.query.filter_by(guid=guid).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash('Canonical library deleted.', 'success')
    return redirect(url_for('lookup_web.list_canonical_libs'))


# ─── Units ─────────────────────────────────────────────────────────────────────

@lookup_web_bp.route('/units/')
def list_units():
    items = Unit.query.order_by(Unit.unit_name).all()
    return render_template('lookup/units/list.html', items=items)


@lookup_web_bp.route('/units/create', methods=['GET', 'POST'])
@sso_login_required
def create_unit():
    if request.method == 'POST':
        name = request.form.get('unit_name', '').strip()
        if not name:
            flash('Name is required.', 'error')
            return redirect(url_for('lookup_web.create_unit'))
        if Unit.query.filter_by(unit_name=name).first():
            flash('A unit with that name already exists.', 'error')
            return redirect(url_for('lookup_web.create_unit'))
        item = Unit(
            unit_name=name,
            unit_display_text=request.form.get('unit_display_text'),
            author=request.form.get('author'),
        )
        db.session.add(item)
        db.session.commit()
        flash('Unit created.', 'success')
        return redirect(url_for('lookup_web.list_units'))
    return render_template('lookup/units/create.html')


@lookup_web_bp.route('/units/<guid>')
def view_unit(guid):
    item = Unit.query.filter_by(guid=guid).first_or_404()
    return render_template('lookup/units/view.html', item=item)


@lookup_web_bp.route('/units/<guid>/edit', methods=['GET', 'POST'])
@sso_login_required
def edit_unit(guid):
    item = Unit.query.filter_by(guid=guid).first_or_404()
    if request.method == 'POST':
        item.unit_name = request.form.get('unit_name', item.unit_name).strip()
        item.unit_display_text = request.form.get('unit_display_text')
        item.author = request.form.get('author')
        item.vers_number = (item.vers_number or 1) + 1
        db.session.commit()
        flash('Unit updated.', 'success')
        return redirect(url_for('lookup_web.view_unit', guid=guid))
    return render_template('lookup/units/edit.html', item=item)


@lookup_web_bp.route('/units/<guid>/delete', methods=['POST'])
@sso_login_required
def delete_unit(guid):
    item = Unit.query.filter_by(guid=guid).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash('Unit deleted.', 'success')
    return redirect(url_for('lookup_web.list_units'))


# ─── Response Types ────────────────────────────────────────────────────────────

@lookup_web_bp.route('/response-types/')
def list_response_types():
    items = ResponseType.query.order_by(ResponseType.response_type_name).all()
    return render_template('lookup/response_types/list.html', items=items)


@lookup_web_bp.route('/response-types/create', methods=['GET', 'POST'])
@sso_login_required
def create_response_type():
    if request.method == 'POST':
        name = request.form.get('response_type_name', '').strip()
        if not name:
            flash('Name is required.', 'error')
            return redirect(url_for('lookup_web.create_response_type'))
        if ResponseType.query.filter_by(response_type_name=name).first():
            flash('A response type with that name already exists.', 'error')
            return redirect(url_for('lookup_web.create_response_type'))
        item = ResponseType(
            response_type_name=name,
            response_type_display_text=request.form.get('response_type_display_text'),
            author=request.form.get('author'),
        )
        db.session.add(item)
        db.session.commit()
        flash('Response type created.', 'success')
        return redirect(url_for('lookup_web.list_response_types'))
    return render_template('lookup/response_types/create.html')


@lookup_web_bp.route('/response-types/<guid>')
def view_response_type(guid):
    item = ResponseType.query.filter_by(guid=guid).first_or_404()
    return render_template('lookup/response_types/view.html', item=item)


@lookup_web_bp.route('/response-types/<guid>/edit', methods=['GET', 'POST'])
@sso_login_required
def edit_response_type(guid):
    item = ResponseType.query.filter_by(guid=guid).first_or_404()
    if request.method == 'POST':
        item.response_type_name = request.form.get('response_type_name', item.response_type_name).strip()
        item.response_type_display_text = request.form.get('response_type_display_text')
        item.author = request.form.get('author')
        item.vers_number = (item.vers_number or 1) + 1
        db.session.commit()
        flash('Response type updated.', 'success')
        return redirect(url_for('lookup_web.view_response_type', guid=guid))
    return render_template('lookup/response_types/edit.html', item=item)


@lookup_web_bp.route('/response-types/<guid>/delete', methods=['POST'])
@sso_login_required
def delete_response_type(guid):
    item = ResponseType.query.filter_by(guid=guid).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash('Response type deleted.', 'success')
    return redirect(url_for('lookup_web.list_response_types'))


# ─── Concept Types ─────────────────────────────────────────────────────────────

@lookup_web_bp.route('/concept-types/')
def list_concept_types():
    items = ConceptType.query.order_by(ConceptType.concept_type_name).all()
    return render_template('lookup/concept_types/list.html', items=items)


@lookup_web_bp.route('/concept-types/create', methods=['GET', 'POST'])
@sso_login_required
def create_concept_type():
    if request.method == 'POST':
        name = request.form.get('concept_type_name', '').strip()
        if not name:
            flash('Name is required.', 'error')
            return redirect(url_for('lookup_web.create_concept_type'))
        if ConceptType.query.filter_by(concept_type_name=name).first():
            flash('A concept type with that name already exists.', 'error')
            return redirect(url_for('lookup_web.create_concept_type'))
        item = ConceptType(
            concept_type_name=name,
            concept_type_display_text=request.form.get('concept_type_display_text'),
            author=request.form.get('author'),
        )
        db.session.add(item)
        db.session.commit()
        flash('Concept type created.', 'success')
        return redirect(url_for('lookup_web.list_concept_types'))
    return render_template('lookup/concept_types/create.html')


@lookup_web_bp.route('/concept-types/<guid>')
def view_concept_type(guid):
    item = ConceptType.query.filter_by(guid=guid).first_or_404()
    return render_template('lookup/concept_types/view.html', item=item)


@lookup_web_bp.route('/concept-types/<guid>/edit', methods=['GET', 'POST'])
@sso_login_required
def edit_concept_type(guid):
    item = ConceptType.query.filter_by(guid=guid).first_or_404()
    if request.method == 'POST':
        item.concept_type_name = request.form.get('concept_type_name', item.concept_type_name).strip()
        item.concept_type_display_text = request.form.get('concept_type_display_text')
        item.author = request.form.get('author')
        item.vers_number = (item.vers_number or 1) + 1
        db.session.commit()
        flash('Concept type updated.', 'success')
        return redirect(url_for('lookup_web.view_concept_type', guid=guid))
    return render_template('lookup/concept_types/edit.html', item=item)


@lookup_web_bp.route('/concept-types/<guid>/delete', methods=['POST'])
@sso_login_required
def delete_concept_type(guid):
    item = ConceptType.query.filter_by(guid=guid).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash('Concept type deleted.', 'success')
    return redirect(url_for('lookup_web.list_concept_types'))
