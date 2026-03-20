from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.concept_models import ValueSet, ValueSetValue, ValueCatalog, CanonicalLib
from app.services.name_uniqueness import NameUniquenessService

valuesets_web_bp = Blueprint('valuesets_web', __name__, url_prefix='/valuesets')


@valuesets_web_bp.route('/')
def list_valuesets():
    page = max(1, request.args.get('page', 1, type=int))
    pagination = ValueSet.query.order_by(ValueSet.valueset_name).paginate(
        page=page, per_page=50, error_out=False
    )
    return render_template('valuesets/list.html', pagination=pagination)


@valuesets_web_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_valueset():
    if request.method == 'POST':
        name = request.form.get('valueset_name', '').strip()
        canon_lib = request.form.get('canonical_lib')

        if not name:
            flash('ValueSet name is required.', 'error')
            return redirect(url_for('valuesets_web.create_valueset'))
        if not canon_lib:
            flash('Canonical library is required.', 'error')
            return redirect(url_for('valuesets_web.create_valueset'))

        error = NameUniquenessService.validate_name_for_manual_entry(
            name, ValueSet, 'valueset_name'
        )
        if error:
            flash(error, 'error')
            return redirect(url_for('valuesets_web.create_valueset'))

        vs = ValueSet(
            valueset_name=name,
            canonical_lib=canon_lib,
            canonical_refnumber=request.form.get('canonical_refnumber'),
            valueset_display_text=request.form.get('valueset_display_text'),
            valueset_explanation=request.form.get('valueset_explanation'),
            author=request.form.get('author'),
        )
        db.session.add(vs)
        db.session.commit()
        flash('ValueSet created.', 'success')
        return redirect(url_for('valuesets_web.list_valuesets'))

    return render_template('valuesets/create.html',
                           canonical_libs=CanonicalLib.query.all())


@valuesets_web_bp.route('/<guid>')
def view_valueset(guid):
    vs = ValueSet.query.filter_by(guid=guid).first_or_404()
    members = (ValueSetValue.query
               .filter_by(valueset_guid=guid)
               .order_by(ValueSetValue.sort_order)
               .all())
    values = []
    for m in members:
        v = ValueCatalog.query.filter_by(guid=m.value_guid).first()
        if v:
            values.append({'value': v, 'sort_order': m.sort_order})
    all_values = ValueCatalog.query.order_by(ValueCatalog.value_name).all()
    return render_template('valuesets/view.html', vs=vs, values=values, all_values=all_values)


@valuesets_web_bp.route('/<guid>/edit', methods=['GET', 'POST'])
@login_required
def edit_valueset(guid):
    vs = ValueSet.query.filter_by(guid=guid).first_or_404()
    if request.method == 'POST':
        vs.valueset_name = request.form.get('valueset_name', vs.valueset_name).strip()
        vs.valueset_display_text = request.form.get('valueset_display_text')
        vs.valueset_explanation = request.form.get('valueset_explanation')
        vs.canonical_refnumber = request.form.get('canonical_refnumber')
        vs.author = request.form.get('author')
        vs.vers_number = (vs.vers_number or 1) + 1
        db.session.commit()
        flash('ValueSet updated.', 'success')
        return redirect(url_for('valuesets_web.view_valueset', guid=guid))
    return render_template('valuesets/edit.html', vs=vs,
                           canonical_libs=CanonicalLib.query.all())


@valuesets_web_bp.route('/<guid>/delete', methods=['POST'])
@login_required
def delete_valueset(guid):
    vs = ValueSet.query.filter_by(guid=guid).first_or_404()
    ValueSetValue.query.filter_by(valueset_guid=guid).delete()
    db.session.delete(vs)
    db.session.commit()
    flash('ValueSet deleted.', 'success')
    return redirect(url_for('valuesets_web.list_valuesets'))


@valuesets_web_bp.route('/<guid>/add-value', methods=['POST'])
@login_required
def add_value_to_set(guid):
    vs = ValueSet.query.filter_by(guid=guid).first_or_404()
    value_guid = request.form.get('value_guid')
    if not value_guid:
        flash('Select a value to add.', 'error')
        return redirect(url_for('valuesets_web.view_valueset', guid=guid))

    existing = ValueSetValue.query.filter_by(
        valueset_guid=guid, value_guid=value_guid
    ).first()
    if existing:
        flash('Value already in this set.', 'error')
        return redirect(url_for('valuesets_web.view_valueset', guid=guid))

    max_order = db.session.query(db.func.max(ValueSetValue.sort_order)).filter_by(
        valueset_guid=guid
    ).scalar() or 0

    link = ValueSetValue(
        valueset_guid=guid,
        value_guid=value_guid,
        sort_order=max_order + 1,
    )
    db.session.add(link)
    db.session.commit()
    flash('Value added to set.', 'success')
    return redirect(url_for('valuesets_web.view_valueset', guid=guid))


@valuesets_web_bp.route('/<guid>/update-sort', methods=['POST'])
@login_required
def update_sort_order(guid):
    ValueSet.query.filter_by(guid=guid).first_or_404()
    members = ValueSetValue.query.filter_by(valueset_guid=guid).all()
    for m in members:
        new_order = request.form.get(f'order_{m.value_guid}', type=int)
        if new_order is not None:
            m.sort_order = new_order
    db.session.commit()
    flash('Sort order updated.', 'success')
    return redirect(url_for('valuesets_web.view_valueset', guid=guid))


@valuesets_web_bp.route('/<guid>/remove-value/<value_guid>', methods=['POST'])
@login_required
def remove_value_from_set(guid, value_guid):
    ValueSetValue.query.filter_by(
        valueset_guid=guid, value_guid=value_guid
    ).delete()
    db.session.commit()
    flash('Value removed from set.', 'success')
    return redirect(url_for('valuesets_web.view_valueset', guid=guid))
