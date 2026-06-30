import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def _limiter_key():
    """Per-source rate-limit bucket.

    For requests carrying valid-shape service-key headers we use the
    source-service name as the bucket key (so each trusted sibling has
    its own bucket and cdr.pdhc + sim.pdhc + dashboard.pdhc don't compete
    against each other through the shared Docker bridge IP). For SSO /
    anonymous requests we fall back to the remote address.
    """
    from flask import request
    from app.api.auth import KNOWN_SERVICES
    src = request.headers.get('X-Source-Service', '').strip()
    if src and src in KNOWN_SERVICES and request.headers.get('X-Service-Key'):
        return f"service:{src}"
    return get_remote_address()


def _service_caller():
    """Return True when the caller looks like a trusted sibling service —
    used by `exempt_when` on the burst-prone lookup blueprints to lift
    the rate-limit for canonicaliser warmup. Validity of the key itself
    is enforced later by `requires_role`'s service-key path; this only
    decides whether to BYPASS the limiter, not whether the caller is
    actually trusted."""
    from flask import request
    from app.api.auth import KNOWN_SERVICES
    src = request.headers.get('X-Source-Service', '').strip()
    return bool(src and src in KNOWN_SERVICES and request.headers.get('X-Service-Key'))


limiter = Limiter(key_func=_limiter_key, default_limits=['200/minute'])


def create_app(testing=False):
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get(
            'TEST_DATABASE_URL', app.config['SQLALCHEMY_DATABASE_URI']
        )

    app.config.setdefault('RATELIMIT_DEFAULT', '200/minute')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)

    # Trusted sibling services (X-Source-Service + X-Service-Key) bypass
    # the rate limiter globally — the canonicaliser warmup hits lookup +
    # concepts in burst and would otherwise trip the default. Validity of
    # the key is still enforced by requires_role's service-key path; this
    # only decides whether to BYPASS the limiter, not whether the caller
    # is trusted.
    @limiter.request_filter
    def _service_caller_bypass():
        return _service_caller()
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Session config for SSO token storage
    app.permanent_session_lifetime = timedelta(hours=24)

    # When auth is disabled (local dev), Flask-Login treats every request
    # as authenticated so @login_required passes through.
    if app.config.get('AUTH_DISABLED'):
        from app.models.user_models import User

        @app.before_request
        def _auto_login():
            from flask_login import login_user, current_user
            if not current_user.is_authenticated:
                try:
                    user = User.query.filter_by(role='admin').first()
                    if user:
                        login_user(user)
                except Exception:
                    pass

    # Import models so they are registered with SQLAlchemy
    from app.models import user_models, concept_models, fhir_models, activity_models, forms_models  # noqa: F401

    @login_manager.user_loader
    def load_user(user_id):
        return user_models.User.query.get(int(user_id))

    # Register API blueprints
    from app.api.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    from app.api.lookup_tables import lookup_bp
    app.register_blueprint(lookup_bp, url_prefix='/api/v1/lookup')

    from app.api.concepts import concepts_bp
    app.register_blueprint(concepts_bp, url_prefix='/api/v1')

    from app.api.fhir_plandefinitions import fhir_plandef_bp
    app.register_blueprint(fhir_plandef_bp, url_prefix='/api/v1')

    from app.api.plandefinitions import plandefinitions_bp
    app.register_blueprint(plandefinitions_bp, url_prefix='/api/v1')

    from app.api.capability import capability_bp
    app.register_blueprint(capability_bp, url_prefix='/api/v1')

    # Terminology surface — $validate-code + termbank proxies (platform-plan §0.2)
    from app.api.terminology import bp as terminology_bp
    app.register_blueprint(terminology_bp, url_prefix='/api/v1')

    # FHIR R5 ValueSet resource + $expand (§6.1 — conformant terminology profile).
    # Additive: does NOT replace the /api/v1/lookup/valuesets CRUD JSON.
    from app.api.fhir_valueset import fhir_valueset_bp
    app.register_blueprint(fhir_valueset_bp, url_prefix='/api/v1')

    # FHIR R5 ConceptMap + $translate (§6.4 — local↔canonical mapping).
    from app.api.fhir_conceptmap import fhir_conceptmap_bp
    app.register_blueprint(fhir_conceptmap_bp, url_prefix='/api/v1')

    # FHIR R5 CodeSystem + $lookup (§6.3 — local concepts published as
    # CodeSystem plan-pdhc-local; external systems delegate to termbank).
    from app.api.fhir_codesystem import fhir_codesystem_bp
    app.register_blueprint(fhir_codesystem_bp, url_prefix='/api/v1')

    # Termbank HTTP client — one instance per app, with TTL cache
    from app.services.termbank_client import TermbankClient
    app.termbank_client = TermbankClient()

    # Register web UI blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.lookup_tables import lookup_web_bp
    app.register_blueprint(lookup_web_bp)

    from app.routes.concepts import concepts_web_bp
    app.register_blueprint(concepts_web_bp)

    from app.routes.values import values_web_bp
    app.register_blueprint(values_web_bp)

    from app.routes.valuesets import valuesets_web_bp
    app.register_blueprint(valuesets_web_bp)

    from app.routes.plandefinitions import plandef_web_bp
    app.register_blueprint(plandef_web_bp)

    from app.api.forms import forms_bp
    app.register_blueprint(forms_bp, url_prefix='/api/v1')

    from app.routes.forms import forms_web_bp
    app.register_blueprint(forms_web_bp)

    from app.api.form_definitions import form_defs_bp
    app.register_blueprint(form_defs_bp, url_prefix='/api/v1')

    from app.api.dispatch import dispatch_bp
    app.register_blueprint(dispatch_bp, url_prefix='/api/v1')

    from app.routes.form_definitions import forms_defs_web_bp
    app.register_blueprint(forms_defs_web_bp)

    # Health endpoint (required by SSO service registry).
    # Shape per CLAUDE.md §10 — matches cgm.pdhc pattern.
    @app.route('/api/health')
    @limiter.exempt
    def health():
        from flask import jsonify
        from sqlalchemy import text
        db_ok = False
        try:
            db.session.execute(text('SELECT 1'))
            db_ok = True
        except Exception:
            pass
        status = 'ok' if db_ok else 'degraded'
        code = 200 if db_ok else 503
        resp = jsonify({
            'status': status,
            'database': 'connected' if db_ok else 'unavailable',
            'service': 'plan.pdhc',
            'version': os.environ.get('APP_VERSION', 'dev'),
        })
        # Ticket #70 / CLAUDE.md §10: let www.pdhc.se/services.html read the
        # JSON body cross-origin so it can drive real status/DB dots. Specific
        # origin + Vary: Origin (not "*") keeps future Allow-Credentials
        # spec-compliant. Use .add() for Vary to preserve the existing
        # "Vary: Cookie" emitted by the session middleware.
        # NOTE: Flask-CORS is also active on /api/* with origins="*", so it
        # may override this header via its after_request hook. Acceptance test
        # below will flag that; if it does, we narrow Flask-CORS for this path.
        resp.headers['Access-Control-Allow-Origin'] = 'https://www.pdhc.se'
        resp.headers['Access-Control-Allow-Methods'] = 'GET'
        resp.headers.add('Vary', 'Origin')
        resp.headers['Cache-Control'] = 'no-store'
        return resp, code

    # Bootstrap superuser on first run
    with app.app_context():
        _bootstrap_superuser(app)

    _register_cli(app)

    return app


def _register_cli(app):
    """Register flask-cli commands. Currently: import-concepts (#134)."""
    import io as _io
    import os as _os
    import json as _json
    import click

    @app.cli.command('import-concepts')
    @click.argument('path', type=click.Path(exists=True, dir_okay=False))
    @click.option('--operator', default=None,
                  help='Identity to record in the audit log.')
    @click.option('--dry-run', is_flag=True,
                  help='Validate only; do not commit changes.')
    @click.option('--json-out', 'json_out', is_flag=True,
                  help='Emit the report as JSON instead of a human summary.')
    def import_concepts_cmd(path, operator, dry_run, json_out):
        """Bulk-import concepts from a .xlsx or .csv file (ticket #134)."""
        from app.services.concept_importer import (
            parse_xlsx, parse_csv, validate_and_import,
            compute_sha256, ImportError_,
        )

        with open(path, 'rb') as fh:
            raw = fh.read()
        sha = compute_sha256(raw)
        ext = _os.path.splitext(path)[1].lower()
        try:
            if ext == '.xlsx':
                rows = parse_xlsx(_io.BytesIO(raw))
            elif ext == '.csv':
                rows = parse_csv(_io.BytesIO(raw))
            else:
                click.echo(f'unsupported extension {ext!r}; use .xlsx or .csv',
                           err=True)
                raise SystemExit(2)
        except ImportError_ as e:
            click.echo(f'parse error: {e}', err=True)
            raise SystemExit(2)

        op = operator or f'cli:{_os.environ.get("USER", "unknown")}'
        report = validate_and_import(
            rows, operator=op, filename=_os.path.basename(path),
            sha256=sha, dry_run=dry_run,
        )

        if json_out:
            click.echo(_json.dumps(report, indent=2))
        else:
            s = report['summary']
            click.echo(
                f'rows: {s["n_in"]}  accepted: {s["n_accepted"]} '
                f'(created {s["n_created"]} / updated {s["n_updated"]})  '
                f'rejected: {s["n_rejected"]}'
                + ('  (dry-run)' if s['dry_run'] else '')
            )
            for rej in report['rejected']:
                click.echo(
                    f'  row {rej["row"]}: {rej.get("concept_name") or "?"} '
                    f'— {rej["reason"]}'
                )

        raise SystemExit(0 if not report['rejected'] else 1)


def _bootstrap_superuser(app):
    """Create the bootstrap superuser if no users exist (Rule 23)."""
    from app.models.user_models import User

    try:
        if User.query.count() == 0:
            su_username = os.environ.get('BOOTSTRAP_SU_USERNAME', 'admin')
            su_password = os.environ.get('BOOTSTRAP_SU_PASSWORD')
            if su_password:
                su = User(
                    username=su_username,
                    role='admin',
                    is_active=True,
                )
                su.set_password(su_password)
                db.session.add(su)
                db.session.commit()
                app.logger.info(f'Bootstrap superuser "{su_username}" created.')
            else:
                app.logger.warning(
                    'No BOOTSTRAP_SU_PASSWORD set — skipping superuser creation.'
                )
    except Exception:
        # Table may not exist yet (before first migration)
        pass
