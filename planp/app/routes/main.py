import os
from flask import Blueprint, render_template, send_file, abort, jsonify, current_app
from sqlalchemy import func
from app import db
from app.models.concept_models import (
    Concept, ValueCatalog, ValueSet, CanonicalLib,
    ConceptType, ResponseType, Unit,
)
from app.models.fhir_models import PlanDefinition
from app.models.forms_models import Questionnaire, QuestionnaireResponse

main_bp = Blueprint('main', __name__)

# Single source of truth for the doc catalog lives in app.api.capability.
# Keeping a second copy here drifted: prior to 2026-06-24 this dict
# referenced SSO docs the API catalog didn't, and missed the two
# terminology-profile docs the API catalog adds.
from app.api.capability import DOCS_CATALOG, _resolve_doc_path


def _format_size(size_bytes):
    if size_bytes < 1024:
        return f'{size_bytes} B'
    elif size_bytes < 1024 * 1024:
        return f'{size_bytes / 1024:.1f} KB'
    else:
        return f'{size_bytes / (1024 * 1024):.1f} MB'


def _get_docs_list():
    docs = []
    for filename, description in DOCS_CATALOG.items():
        path = _resolve_doc_path(filename)
        if path:
            size = os.path.getsize(path)
            docs.append({
                'filename': filename,
                'description': description,
                'size': _format_size(size),
                'size_bytes': size,
            })
    return docs


@main_bp.route('/')
def dashboard():
    counts = {
        'concepts': db.session.query(Concept).count(),
        'value_count': db.session.query(ValueCatalog).count(),
        'valuesets': db.session.query(ValueSet).count(),
        'plandefinitions': db.session.query(PlanDefinition).count(),
        'canonical_libs': db.session.query(CanonicalLib).count(),
        'concept_types': db.session.query(ConceptType).count(),
        'response_types': db.session.query(ResponseType).count(),
        'units': db.session.query(Unit).count(),
        'forms': db.session.query(func.count(func.distinct(Questionnaire.form_guid))).scalar() or 0,
        'form_responses': db.session.query(QuestionnaireResponse).count(),
    }
    return render_template('dashboard.html', counts=counts)


@main_bp.route('/docs')
def docs_page():
    docs = _get_docs_list()
    return render_template('docs.html', docs=docs)


@main_bp.route('/docs/<filename>')
def download_doc(filename):
    # Security: only serve files in the catalog
    if filename not in DOCS_CATALOG:
        abort(404)
    path = _resolve_doc_path(filename)
    if not path:
        abort(404)
    return send_file(path, as_attachment=True, download_name=filename)


@main_bp.route('/docs/api.json')
def api_docs_json():
    """Redirect-free JSON version of the API reference (parsed from capability)."""
    from app.api.capability import ENDPOINTS
    return jsonify({
        'name': 'PDHC PlanDef Builder API',
        'version': '1.0.0',
        'total_endpoints': len(ENDPOINTS),
        'endpoints': ENDPOINTS,
    }), 200
