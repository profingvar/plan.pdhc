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


@pytest.fixture(scope='function')
def db_session(app):
    """Provide a clean database session for each test."""
    with app.app_context():
        _db.session.begin_nested()
        yield _db.session
        _db.session.rollback()


def get_auth_header(client):
    """Helper: login as bootstrap admin and return auth header."""
    resp = client.post('/api/v1/auth/login', json={
        'username': 'admin',
        'password': 'admin123',
    })
    data = resp.get_json()
    token = data['access_token']
    return {'Authorization': f'Bearer {token}'}
