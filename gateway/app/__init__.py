import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)


def create_app(testing=False):
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get(
            'TEST_DATABASE_URL', app.config['SQLALCHEMY_DATABASE_URI']
        )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

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
    from app.models import user_models, concept_models, fhir_models, activity_models  # noqa: F401

    @login_manager.user_loader
    def load_user(user_id):
        return user_models.User.query.get(int(user_id))

    # Register API blueprints
    from app.api.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    from app.api.lookup_tables import lookup_bp
    app.register_blueprint(lookup_bp, url_prefix='/api/v1')

    from app.api.concepts import concepts_bp
    app.register_blueprint(concepts_bp, url_prefix='/api/v1')

    from app.api.fhir_plandefinitions import fhir_plandef_bp
    app.register_blueprint(fhir_plandef_bp, url_prefix='/api/v1')

    from app.api.plandefinitions import plandefinitions_bp
    app.register_blueprint(plandefinitions_bp, url_prefix='/api/v1')

    from app.api.capability import capability_bp
    app.register_blueprint(capability_bp, url_prefix='/api/v1')

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

    # Bootstrap superuser on first run
    with app.app_context():
        _bootstrap_superuser(app)

    return app


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
