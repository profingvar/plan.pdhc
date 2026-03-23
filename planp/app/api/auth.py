import functools
import secrets
from flask import Blueprint, request, jsonify, redirect, session, url_for, current_app
from app import limiter

auth_bp = Blueprint('auth', __name__)
limiter.limit("200/minute")(auth_bp)


# ---------------------------------------------------------------------------
# SSO-aware role decorator
# ---------------------------------------------------------------------------

def requires_role(min_role):
    """Decorator enforcing minimum role level.

    When AUTH_DISABLED is True (local dev), all requests pass through.
    When AUTH_DISABLED is False (production), checks SSO access blob in session.

    Role mapping (plan.pdhc → SSO access blob):
      read_only  → any authenticated session
      read_write → professional with "planning" in effective_phases, or SU admin
      admin      → is_su_admin
    """
    role_levels = {'read_only': 1, 'read_write': 2, 'admin': 3}

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if current_app.config.get('AUTH_DISABLED'):
                return fn(*args, **kwargs)

            blob = session.get('sso_user')
            if not blob:
                return jsonify({'error': 'Authentication required'}), 401

            required = role_levels.get(min_role, 0)

            # SU admins bypass all checks
            if blob.get('is_su_admin'):
                return fn(*args, **kwargs)

            # Determine effective role from access blob
            effective = 1  # read_only — any authenticated user
            if blob.get('user_type') == 'professional':
                if 'planning' in blob.get('effective_phases', []):
                    effective = 2  # read_write
            if effective < required:
                return jsonify({'error': 'Insufficient permissions'}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def sso_login_required(fn):
    """Decorator for web routes: redirects to SSO login if no session.

    When AUTH_DISABLED is True, does nothing (Flask-Login auto-login handles it).
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if current_app.config.get('AUTH_DISABLED'):
            return fn(*args, **kwargs)
        if not session.get('sso_user'):
            from app.services.sso_service import get_sso_login_url
            state = secrets.token_urlsafe(32)
            session['sso_state'] = state
            return redirect(get_sso_login_url(state))
        return fn(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@auth_bp.route('/login', methods=['GET'])
def login():
    """H1 — redirect to SSO for authentication.

    When AUTH_DISABLED is True, returns a message (local dev uses auto-login).
    """
    if current_app.config.get('AUTH_DISABLED'):
        return jsonify({'message': 'Auth disabled — auto-login active'}), 200

    from app.services.sso_service import get_sso_login_url
    state = secrets.token_urlsafe(32)
    session['sso_state'] = state
    return redirect(get_sso_login_url(state))


@auth_bp.route('/callback', methods=['GET'])
def callback():
    """H3→H4 — receive JWT from SSO redirect, validate, store access blob."""
    if current_app.config.get('AUTH_DISABLED'):
        return jsonify({'error': 'Auth disabled'}), 400

    # Check for SSO error response
    error = request.args.get('error')
    if error:
        desc = request.args.get('error_description', 'Authentication failed')
        return jsonify({'error': error, 'message': desc}), 401

    # CSRF state validation
    state = request.args.get('state', '')
    expected_state = session.pop('sso_state', None)
    if not state or state != expected_state:
        return jsonify({'error': 'CSRF state mismatch'}), 403

    token = request.args.get('token', '')
    if not token:
        return jsonify({'error': 'No token received'}), 400

    # H4 — validate token with SSO
    from app.services.sso_service import validate_token
    blob = validate_token(token)
    if blob is None:
        return jsonify({'error': 'Token validation failed'}), 401

    # Store access blob and token in session
    session['sso_user'] = blob
    session['sso_token'] = token
    session.permanent = True

    # Redirect to dashboard
    return redirect(url_for('main.dashboard'))


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Clear SSO session."""
    session.pop('sso_user', None)
    session.pop('sso_token', None)
    session.pop('sso_state', None)

    if current_app.config.get('AUTH_DISABLED'):
        return jsonify({'message': 'Logged out'}), 200

    return redirect(url_for('main.dashboard'))


@auth_bp.route('/me', methods=['GET'])
def me():
    """Return current user's access blob from session."""
    if current_app.config.get('AUTH_DISABLED'):
        from app.models.user_models import User
        user = User.query.filter_by(role='admin').first()
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({'error': 'No user'}), 404

    blob = session.get('sso_user')
    if not blob:
        return jsonify({'error': 'Not authenticated'}), 401
    return jsonify(blob), 200
