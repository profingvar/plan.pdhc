import functools
import secrets
from flask import Blueprint, request, jsonify, redirect, session, url_for, current_app
from app import limiter

auth_bp = Blueprint('auth', __name__)
limiter.limit("200/minute")(auth_bp)


# ---------------------------------------------------------------------------
# Ticket #49: NO blob caching. Every protected request re-validates the
# stored bearer with sso.pdhc /api/auth/me/service. This makes the per-user
# session flush (SSO ticket #44) take effect immediately — a revoked token
# gets a 401 on the very next call here. `session['sso_user']` is retained
# only as a display-only cache (rendered in base.html); it is NEVER trusted
# for authorization decisions and is refreshed from each fresh validation.
# ---------------------------------------------------------------------------

def _sso_change_password_url():
    base = current_app.config['SSO_BASE_URL'].rstrip('/')
    return f'{base}/change-password'


def _refresh_blob_or_clear():
    """Re-validate the stored bearer; refresh session cache; return blob or None.

    On 401/invalid, drops the session entirely. Callers get None and MUST
    route the user to re-login.
    """
    from app.services.sso_service import validate_token
    token = session.get('sso_token')
    if not token:
        return None
    blob = validate_token(token)
    if blob is None:
        # Stale token (expired, revoked, or flushed by SU) — wipe session.
        session.pop('sso_token', None)
        session.pop('sso_user', None)
        return None
    # Refresh the display-only cache with the fresh blob.
    session['sso_user'] = blob
    return blob


# ---------------------------------------------------------------------------
# SSO-aware role decorator
# ---------------------------------------------------------------------------

def requires_role(min_role):
    """Decorator enforcing minimum role level.

    When AUTH_DISABLED is True (local dev), all requests pass through.
    When AUTH_DISABLED is False (production), re-validates the stored bearer
    with SSO on every request (no blob caching — Rule 11).

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

            blob = _refresh_blob_or_clear()
            if not blob:
                return jsonify({'error': 'Authentication required'}), 401

            # Ticket #43: block actions while SSO requires a password change.
            if blob.get('must_change_password'):
                return jsonify({
                    'error': 'Password change required',
                    'change_password_url': _sso_change_password_url(),
                }), 403

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
    """Decorator for web routes: re-validates SSO per request; redirects
    to SSO login if stored bearer is missing or stale, or to SSO
    /change-password if SSO flagged a forced password change.

    When AUTH_DISABLED is True, does nothing (Flask-Login auto-login handles it).
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if current_app.config.get('AUTH_DISABLED'):
            return fn(*args, **kwargs)

        blob = _refresh_blob_or_clear()
        if not blob:
            from app.services.sso_service import get_sso_login_url
            state = secrets.token_urlsafe(32)
            session['sso_state'] = state
            return redirect(get_sso_login_url(state))

        # Ticket #43: forced password reset — send user to SSO's change-password
        # page. Once they change it, SSO clears the flag and future blobs will
        # pass this check.
        if blob.get('must_change_password'):
            return redirect(_sso_change_password_url())

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

    # Ticket #49: keep only the bearer in session for later re-validation.
    # session['sso_user'] is a display-only cache refreshed on every
    # validated request — the decorators do not trust it for auth.
    session['sso_token'] = token
    session['sso_user'] = blob
    session.permanent = True

    # Ticket #43: if SSO flagged this user for forced password change, go
    # straight to the SSO change-password page rather than the dashboard.
    if blob.get('must_change_password'):
        return redirect(_sso_change_password_url())

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
    """Return current user's access blob, freshly re-validated with SSO.

    Ticket #49: re-validates per request so the client learns about session
    flushes (SSO #44) and forced password resets (SSO #43) as soon as they
    happen — no stale session copy.
    """
    if current_app.config.get('AUTH_DISABLED'):
        from app.models.user_models import User
        user = User.query.filter_by(role='admin').first()
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({'error': 'No user'}), 404

    blob = _refresh_blob_or_clear()
    if not blob:
        return jsonify({'error': 'Not authenticated'}), 401
    return jsonify(blob), 200
