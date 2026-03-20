import functools
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity,
)
from app import db, limiter
from app.models.user_models import User

auth_bp = Blueprint('auth', __name__)
limiter.limit("200/minute")(auth_bp)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def requires_role(min_role):
    """Decorator enforcing minimum role level.
    When AUTH_DISABLED is True (local dev), all requests pass through.
    """
    role_levels = {'read_only': 1, 'read_write': 2, 'admin': 3}

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            from flask import current_app
            if current_app.config.get('AUTH_DISABLED'):
                return fn(*args, **kwargs)

            # Auth is enabled — enforce JWT + role
            @jwt_required()
            def _protected():
                identity = get_jwt_identity()
                user = User.query.filter_by(guid=identity).first()
                if not user or not user.is_active:
                    return jsonify({'error': 'User not found or inactive'}), 401
                if role_levels.get(user.role, 0) < role_levels.get(min_role, 0):
                    return jsonify({'error': 'Insufficient permissions'}), 403
                return fn(*args, **kwargs)
            return _protected()
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10/minute")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    if not user.is_active:
        return jsonify({'error': 'Account is inactive'}), 403

    access_token = create_access_token(identity=user.guid)
    refresh_token = create_refresh_token(identity=user.guid)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(),
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Stateless JWT — client discards token. Blocklist can be added later.
    return jsonify({'message': 'Logged out'}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    identity = get_jwt_identity()
    user = User.query.filter_by(guid=identity).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = User.query.filter_by(guid=identity).first()
    if not user or not user.is_active:
        return jsonify({'error': 'User not found or inactive'}), 401
    access_token = create_access_token(identity=user.guid)
    return jsonify({'access_token': access_token}), 200
