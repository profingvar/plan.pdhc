"""GA-4 #516 — the opt-in authoring panel is wired into the templates.

Renders the concept + builder templates and asserts the mount point and the
JS include are present. The panel itself renders client-side and only when
GET /api/v1/authoring/models returns enabled, so nothing shows when the tool
is off — these tests just pin that the wiring exists and the templates still
render.
"""
from flask import render_template

from app import create_app


_CTX = {
    "canonical_libs": [], "concept_types": [], "response_types": [], "units": [],
    "valuesets": [], "concept": None,
    "concepts_json": "[]", "units_json": "[]", "valuesets_json": "[]",
    "plandef_types_json": "[]", "existing_goals_json": "[]",
    "existing_actions_json": "[]", "produced_forms": [], "plandef": None,
}


class _Concept:
    guid = "g"; concept_name = "x"; concept_display_text = ""; concept_explain = ""
    status = "draft"; canonical_lib = None; canonical_refnumber = ""; concept_type = None
    response_type = None; unit = None; valueset = None; range_low = None; range_high = None
    anchor_low_text = ""; anchor_high_text = ""


def _render(tpl, **extra):
    app = create_app(testing=True)
    ctx = dict(_CTX, **extra)
    with app.test_request_context("/"):
        return render_template(tpl, **ctx)


def test_concept_create_has_assistant_mount_and_script():
    html = _render("concepts/create.html")
    assert 'data-authoring-assistant="concept"' in html
    assert "authoring_assistant.js" in html


def test_concept_edit_has_assistant_mount_and_script():
    html = _render("concepts/edit.html", concept=_Concept())
    assert 'data-authoring-assistant="concept"' in html
    assert "authoring_assistant.js" in html


def test_builder_has_assistant_mount_and_script():
    html = _render("plandefinitions/builder.html")
    assert 'data-authoring-assistant="plandef"' in html
    assert "authoring_assistant.js" in html
