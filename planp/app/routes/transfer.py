"""Transfer page (web) — #530.

Renders the operator-facing trigger for promoting synthetic cdr_6 content
into a working CDR. All the work happens via the JSON API
(``/api/v1/transfer/*``), which proxies cdr_6's server-side engine (#529);
this route only serves the page. SSO-gated like every other builder page.
"""
from flask import Blueprint, render_template

from app.api.auth import sso_login_required

transfer_web_bp = Blueprint("transfer_web", __name__)


@transfer_web_bp.route("/transfer")
@sso_login_required
def transfer_page():
    return render_template("transfer.html")
