import os
from flask import Blueprint, render_template, send_file, abort, jsonify, current_app
from app import db
from app.models.concept_models import (
    Concept, ValueCatalog, ValueSet, CanonicalLib,
    ConceptType, ResponseType, Unit,
)
from app.models.fhir_models import PlanDefinition

main_bp = Blueprint('main', __name__)

# Documentation files and their descriptions
DOCS_CATALOG = {
    'api_reference.md': 'Comprehensive REST API reference with examples',
    'db_schema_snapshot.md': 'Database schema — all 17 tables with samples and GUIDs',
    'plan_description.md': 'Domain architecture — concepts, values, valuesets, PlanDefinitions',
    'readme.md': 'Deployment plan — step-by-step setup and configuration',
    'progress.md': 'Progress log — completed and pending steps',
    'top_rules.md': 'Project rules (immutable)',
    'repo_css.md': 'Frontend design system — colours, typography, components',
    'pdhc_markdown_layout_standard.md': 'Markdown formatting standard',
    'changed_files.md': 'Registry of all created and edited files',
    'nginx_implement_server19March.md': 'Nginx reverse proxy deployment template',
    'sso_technical_manual.md': 'SSO integration — technical architecture, handshake flow, configuration',
    'sso_user_guide.md': 'SSO login — user guide for logging in and permissions',
}


def _resolve_doc_path(filename):
    """Resolve a doc filename to its absolute path.

    Search order: gateway/docs/ → project root → /project-docs/ (Docker mount)
    """
    gateway_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    search_dirs = [
        os.path.join(gateway_dir, 'docs'),
        os.path.dirname(gateway_dir),
        '/project-docs',
    ]
    for d in search_dirs:
        path = os.path.join(d, filename)
        if os.path.isfile(path):
            return path
    return None


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
