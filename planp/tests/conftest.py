import os
import tempfile
import pytest
from app import create_app, db as _db


@pytest.fixture(scope='session')
def app():
    """Create a Flask app configured for testing with SQLite."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret'
    os.environ['FLASK_SECRET_KEY'] = 'test-flask-secret'
    os.environ['BOOTSTRAP_SU_USERNAME'] = 'admin'
    os.environ['BOOTSTRAP_SU_PASSWORD'] = 'admin123'
    os.environ['AUTH_DISABLED'] = 'false'  # Tests validate auth behavior
    os.environ['SSO_BASE_URL'] = 'http://sso-test:9000'
    os.environ['SSO_CLIENT_ID'] = 'test-client-id'
    os.environ['SSO_CLIENT_SECRET'] = 'test-client-secret'
    os.environ['SSO_CALLBACK_URL'] = 'http://localhost:9030/api/v1/auth/callback'

    application = create_app(testing=True)
    application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    application.config['TESTING'] = True

    with application.app_context():
        _db.create_all()

        # Bootstrap superuser now that tables exist
        from app.models.user_models import User
        if User.query.count() == 0:
            su = User(username='admin', role='admin', is_active=True)
            su.set_password('admin123')
            _db.session.add(su)
            _db.session.commit()

        yield application
        _db.drop_all()

    os.close(db_fd)
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def mock_sso_validate_per_request(monkeypatch, request):
    """Ticket #49 shim: the auth decorators now re-validate with SSO on
    every protected request. In tests we short-circuit that to return
    the blob stashed by set_sso_session(), preserving the original
    test ergonomics while still exercising the new re-validation code
    path end-to-end. The TestSSOCallback class is skipped because those
    tests explicitly exercise validate_token via a requests.get patch.
    """
    cls = getattr(request.node, 'cls', None)
    if cls is not None and cls.__name__ == 'TestSSOCallback':
        return
    from flask import session as flask_session

    def fake_validate_token(token):
        return flask_session.get('sso_user')

    monkeypatch.setattr(
        'app.services.sso_service.validate_token', fake_validate_token)


@pytest.fixture(scope='function')
def db_session(app):
    """Provide a clean database session for each test."""
    with app.app_context():
        _db.session.begin_nested()
        yield _db.session
        _db.session.rollback()


# Sample SSO access blob for testing
SAMPLE_ACCESS_BLOB = {
    'user_guid': 'test-guid-1234',
    'email': 'doctor@hospital.se',
    'user_type': 'professional',
    'is_su_admin': False,
    'professional_guid': 'prof-guid-5678',
    'professional_role': 'doctor',
    'fhir_resource_type': 'Practitioner',
    'organization_ids': ['org-guid-0001'],
    'groups': [{
        'group_guid': 'grp-guid-0001',
        'group_name': 'Planning Team',
        'category': 'planning',
        'status': 'approved',
        'is_admin': False,
    }],
    'effective_phases': ['planning'],
}

SAMPLE_SU_BLOB = {
    'user_guid': 'su-guid-0001',
    'email': 'admin@pdhc.se',
    'user_type': 'professional',
    'is_su_admin': True,
    'professional_guid': 'prof-guid-su',
    'professional_role': 'doctor',
    'fhir_resource_type': 'Practitioner',
    'organization_ids': [],
    'groups': [],
    'effective_phases': [],
}

SAMPLE_READONLY_BLOB = {
    'user_guid': 'ro-guid-0001',
    'email': 'viewer@hospital.se',
    'user_type': 'professional',
    'is_su_admin': False,
    'professional_guid': 'prof-guid-ro',
    'professional_role': 'nurse',
    'fhir_resource_type': 'Practitioner',
    'organization_ids': ['org-guid-0001'],
    'groups': [{
        'group_guid': 'grp-guid-0002',
        'group_name': 'Analysis Team',
        'category': 'analysis',
        'status': 'approved',
        'is_admin': False,
    }],
    'effective_phases': ['analysis'],  # No 'planning' phase
}


def set_sso_session(client, blob):
    """Helper: set SSO access blob in the test client session."""
    with client.session_transaction() as sess:
        sess['sso_user'] = blob
        sess['sso_token'] = 'mock-jwt-token'
