"""Form definitions web UI — list, create, view, edit, produce FormDefinitions."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.api.auth import sso_login_required
from app.models.forms_models import FormDefinition, FormDefinitionItem
from app.models.concept_models import Concept
from app.services.form_definitions_service import (
    create_form_definition, update_form_definition, delete_form_definition,
    get_form_definition, add_item, update_item, remove_item, reorder_items,
    produce, get_resolved_preview,
    FormBuilderError, NotFoundError,
)

forms_defs_web_bp = Blueprint('forms_defs_web', __name__)


@forms_defs_web_bp.route('/forms/definitions')
@sso_login_required
def list_definitions():
    status_filter = request.args.get('status', '')
    show_all = request.args.get('show_all', '') == '1'
    query = FormDefinition.query

    if not show_all:
        query = query.filter(FormDefinition.archived == False)

    if status_filter:
        query = query.filter(FormDefinition.status == status_filter)

    definitions = query.order_by(FormDefinition.title).all()
    return render_template('forms/definitions_list.html',
                           definitions=definitions, status_filter=status_filter,
                           show_all=show_all)


@forms_defs_web_bp.route('/forms/definitions/create', methods=['GET', 'POST'])
@sso_login_required
def create_definition():
    if request.method == 'POST':
        data = {
            'title': request.form.get('title', ''),
            'name': request.form.get('name', ''),
            'description': request.form.get('description', ''),
        }
        try:
            result = create_form_definition(data)
            flash(f'Form definition "{result["title"]}" created.', 'success')
            return redirect(url_for('forms_defs_web.edit_definition', guid=result['guid']))
        except FormBuilderError as e:
            flash(f'Error: {e.message}', 'error')
            return redirect(url_for('forms_defs_web.create_definition'))

    return render_template('forms/definitions_create.html')


@forms_defs_web_bp.route('/forms/definitions/<guid>')
@sso_login_required
def view_definition(guid):
    try:
        definition = get_form_definition(guid)
    except NotFoundError:
        flash('Form definition not found.', 'error')
        return redirect(url_for('forms_defs_web.list_definitions'))

    return render_template('forms/definitions_view.html', definition=definition)


@forms_defs_web_bp.route('/forms/definitions/<guid>/edit', methods=['GET', 'POST'])
@sso_login_required
def edit_definition(guid):
    try:
        definition = get_form_definition(guid)
    except NotFoundError:
        flash('Form definition not found.', 'error')
        return redirect(url_for('forms_defs_web.list_definitions'))

    if request.method == 'POST':
        action = request.form.get('action', '')

        if action == 'update_metadata':
            data = {
                'title': request.form.get('title', ''),
                'description': request.form.get('description', ''),
            }
            try:
                update_form_definition(guid, data)
                flash('Definition updated.', 'success')
            except FormBuilderError as e:
                flash(f'Error: {e.message}', 'error')
            return redirect(url_for('forms_defs_web.edit_definition', guid=guid))

        elif action == 'add_item':
            concept_guid = request.form.get('concept_guid', '')
            try:
                add_item(guid, {
                    'concept_guid': concept_guid,
                    'required': request.form.get('required') == 'on',
                    'display_text_override': request.form.get('display_text_override', ''),
                    'group_label': request.form.get('group_label', ''),
                })
                flash('Concept added.', 'success')
            except FormBuilderError as e:
                flash(f'Error: {e.message}', 'error')
            return redirect(url_for('forms_defs_web.edit_definition', guid=guid))

        elif action == 'update_item':
            item_guid = request.form.get('item_guid', '')
            try:
                update_item(item_guid, {
                    'required': request.form.get(f'required_{item_guid}') == 'on',
                    'enabled': request.form.get(f'enabled_{item_guid}') == 'on',
                    'display_text_override': request.form.get(f'display_{item_guid}', ''),
                    'group_label': request.form.get(f'group_{item_guid}', ''),
                })
                flash('Item updated.', 'success')
            except FormBuilderError as e:
                flash(f'Error: {e.message}', 'error')
            return redirect(url_for('forms_defs_web.edit_definition', guid=guid))

        elif action == 'remove_item':
            item_guid = request.form.get('item_guid', '')
            try:
                remove_item(item_guid)
                flash('Item removed.', 'success')
            except FormBuilderError as e:
                flash(f'Error: {e.message}', 'error')
            return redirect(url_for('forms_defs_web.edit_definition', guid=guid))

        elif action == 'reorder':
            ordered = request.form.get('ordered_guids', '')
            if ordered:
                try:
                    reorder_items(guid, ordered.split(','))
                    flash('Items reordered.', 'success')
                except FormBuilderError as e:
                    flash(f'Error: {e.message}', 'error')
            return redirect(url_for('forms_defs_web.edit_definition', guid=guid))

    # GET — load concepts for picker
    concepts = Concept.query.order_by(Concept.concept_name).all()
    # Refresh definition after any POST
    definition = get_form_definition(guid)

    return render_template('forms/definitions_edit.html',
                           definition=definition, concepts=concepts)


@forms_defs_web_bp.route('/forms/definitions/<guid>/delete', methods=['POST'])
@sso_login_required
def delete_definition_route(guid):
    try:
        delete_form_definition(guid)
        flash('Form definition deleted.', 'success')
    except FormBuilderError as e:
        flash(f'Error: {e.message}', 'error')
        return redirect(url_for('forms_defs_web.view_definition', guid=guid))
    return redirect(url_for('forms_defs_web.list_definitions'))


@forms_defs_web_bp.route('/forms/definitions/<guid>/produce', methods=['POST'])
@sso_login_required
def produce_definition(guid):
    try:
        result = produce(guid)
        flash(f'FHIR Questionnaire produced (v{result["version"]}).', 'success')
        return redirect(url_for('forms_web.form_detail', form_guid=result['form_guid']))
    except FormBuilderError as e:
        flash(f'Production failed: {e.message}', 'error')
        return redirect(url_for('forms_defs_web.edit_definition', guid=guid))


@forms_defs_web_bp.route('/forms/definitions/<guid>/archive', methods=['POST'])
@sso_login_required
def archive_definition(guid):
    fd = FormDefinition.query.filter_by(guid=guid).first_or_404()
    fd.archived = not fd.archived
    db.session.commit()
    label = 'archived' if fd.archived else 'unarchived'
    flash(f'Form definition {label}.', 'success')
    return redirect(request.referrer or url_for('forms_defs_web.list_definitions'))
