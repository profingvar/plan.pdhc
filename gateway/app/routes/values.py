from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.concept_models import ValueCatalog, CanonicalLib
from app.services.name_uniqueness import NameUniquenessService

values_web_bp = Blueprint('values_web', __name__, url_prefix='/values')


@values_web_bp.route('/')
def list_values():
    page = max(1, request.args.get('page', 1, type=int))
    pagination = ValueCatalog.query.order_by(ValueCatalog.value_name).paginate(
        page=page, per_page=50, error_out=False
    )
    return render_template('values/list.html', pagination=pagination)


@values_web_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_value():
    if request.method == 'POST':
        name = request.form.get('value_name', '').strip()
        canon_lib = request.form.get('canonical_lib')

        if not name:
            flash('Value name is required.', 'error')
            return redirect(url_for('values_web.create_value'))
        if not canon_lib:
            flash('Canonical library is required.', 'error')
            return redirect(url_for('values_web.create_value'))

        error = NameUniquenessService.validate_name_for_manual_entry(
            name, ValueCatalog, 'value_name'
        )
        if error:
            flash(error, 'error')
            return redirect(url_for('values_web.create_value'))

        value = ValueCatalog(
            value_name=name,
            canonical_lib=canon_lib,
            canonical_refnumber=request.form.get('canonical_refnumber'),
            value_display_text=request.form.get('value_display_text'),
            value_explanation=request.form.get('value_explanation'),
            author=request.form.get('author'),
        )
        db.session.add(value)
        db.session.commit()
        flash('Value created.', 'success')
        return redirect(url_for('values_web.list_values'))

    return render_template('values/create.html',
                           canonical_libs=CanonicalLib.query.all())


@values_web_bp.route('/<guid>')
def view_value(guid):
    value = ValueCatalog.query.filter_by(guid=guid).first_or_404()
    return render_template('values/view.html', value=value)


@values_web_bp.route('/<guid>/edit', methods=['GET', 'POST'])
@login_required
def edit_value(guid):
    value = ValueCatalog.query.filter_by(guid=guid).first_or_404()
    if request.method == 'POST':
        value.value_name = request.form.get('value_name', value.value_name).strip()
        value.value_display_text = request.form.get('value_display_text')
        value.value_explanation = request.form.get('value_explanation')
        value.canonical_refnumber = request.form.get('canonical_refnumber')
        value.author = request.form.get('author')
        value.vers_number = (value.vers_number or 1) + 1
        db.session.commit()
        flash('Value updated.', 'success')
        return redirect(url_for('values_web.view_value', guid=guid))
    return render_template('values/edit.html', value=value,
                           canonical_libs=CanonicalLib.query.all())


@values_web_bp.route('/<guid>/delete', methods=['POST'])
@login_required
def delete_value(guid):
    value = ValueCatalog.query.filter_by(guid=guid).first_or_404()
    db.session.delete(value)
    db.session.commit()
    flash('Value deleted.', 'success')
    return redirect(url_for('values_web.list_values'))
