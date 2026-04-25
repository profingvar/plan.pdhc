/* termbank_panel.js — renders termbank.pdhc concept details into any
 * element with class "termbank-panel" that has data-system and data-code
 * attributes. Used on Concept and ValueCatalog view pages.
 *
 * The panel calls plan.pdhc's same-origin proxy at
 *   /api/v1/termbank/concept/<system>/<code>
 * which fans out to termbank.pdhc and applies a TTL cache.
 */
(function () {
  function escapeHtml(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function valueOfPart(p) {
    if (p.valueString != null) return p.valueString;
    if (p.valueCode != null) return p.valueCode;
    if (p.valueInteger != null) return String(p.valueInteger);
    if (p.valueDecimal != null) return String(p.valueDecimal);
    if (p.valueBoolean != null) return String(p.valueBoolean);
    if (p.valueDateTime != null) return p.valueDateTime;
    if (p.valueUri != null) return p.valueUri;
    return "";
  }

  function render(panel, body) {
    var content = panel.querySelector("[data-termbank-content]");
    if (!body || body.error || !body.parameter) {
      content.innerHTML =
        '<p style="color:var(--text-muted);font-style:italic;">' +
        "Termbank unavailable or no entry for this canonical." +
        "</p>";
      return;
    }
    var byName = {};
    body.parameter.forEach(function (p) {
      if (!byName[p.name]) byName[p.name] = p;
    });

    var display = (byName.display || {}).valueString || "";
    var version = (byName.version || {}).valueString || "";

    var meta = (byName._meta || {}).part || [];
    var canonicalUri = "";
    var status = "";
    var parentUri = "";
    meta.forEach(function (part) {
      if (part.name === "canonical_uri") canonicalUri = part.valueUri || "";
      if (part.name === "status") status = part.valueCode || "";
      if (part.name === "parent_uri") parentUri = part.valueUri || "";
    });

    var designations = body.parameter.filter(function (p) {
      return p.name === "designation";
    });
    var properties = body.parameter.filter(function (p) {
      return p.name === "property";
    });

    var html = "";
    html += '<div style="display:grid;grid-template-columns:140px 1fr;gap:0.5rem 1rem;margin-bottom:0.5rem;">';
    html += '<span class="detail-label">Display</span><span><strong>' + escapeHtml(display) + "</strong></span>";
    if (version)
      html += '<span class="detail-label">Version</span><span>' + escapeHtml(version) + "</span>";
    if (status)
      html += '<span class="detail-label">Status</span><span>' + escapeHtml(status) + "</span>";
    if (canonicalUri)
      html +=
        '<span class="detail-label">Canonical URI</span>' +
        '<span><code style="font-size:0.85em;">' + escapeHtml(canonicalUri) + "</code></span>";
    if (parentUri)
      html +=
        '<span class="detail-label">Parent URI</span>' +
        '<span><code style="font-size:0.85em;">' + escapeHtml(parentUri) + "</code></span>";
    html += "</div>";

    if (designations.length) {
      html += '<details style="margin-top:0.5rem;"><summary>Designations (' + designations.length + ")</summary><ul style=\"margin-top:0.25rem;\">";
      designations.forEach(function (d) {
        var lang = "", value = "", use = "";
        d.part.forEach(function (p) {
          if (p.name === "language") lang = p.valueCode || "";
          if (p.name === "value") value = p.valueString || "";
          if (p.name === "use") use = (p.valueCoding || {}).code || "";
        });
        html +=
          '<li><code style="font-size:0.85em;">' +
          escapeHtml(lang) +
          (use ? "/" + escapeHtml(use) : "") +
          "</code> " +
          escapeHtml(value) +
          "</li>";
      });
      html += "</ul></details>";
    }

    if (properties.length) {
      html += '<details style="margin-top:0.5rem;"><summary>Properties (' + properties.length + ')</summary><ul style="margin-top:0.25rem;">';
      properties.forEach(function (prop) {
        var code = "", value = "";
        prop.part.forEach(function (p) {
          if (p.name === "code") code = p.valueCode || "";
          if (p.name === "value") value = valueOfPart(p);
        });
        html +=
          '<li><code style="font-size:0.85em;">' +
          escapeHtml(code) +
          "</code> " +
          escapeHtml(value) +
          "</li>";
      });
      html += "</ul></details>";
    }

    content.innerHTML = html;
  }

  function load(panel) {
    var system = panel.getAttribute("data-system");
    var code = panel.getAttribute("data-code");
    var content = panel.querySelector("[data-termbank-content]");
    content.innerHTML = "Loading…";
    fetch(
      "/api/v1/termbank/concept/" +
        encodeURIComponent(system) +
        "/" +
        encodeURIComponent(code)
    )
      .then(function (r) {
        return r.ok ? r.json() : Promise.reject(r);
      })
      .then(function (body) {
        render(panel, body);
      })
      .catch(function () {
        content.innerHTML =
          '<p style="color:var(--text-muted);font-style:italic;">' +
          "Termbank unavailable or no entry for this canonical." +
          "</p>";
      });
  }

  function init() {
    document.querySelectorAll(".termbank-panel").forEach(function (panel) {
      load(panel);
      var btn = panel.querySelector("[data-termbank-refresh]");
      if (btn) btn.addEventListener("click", function () { load(panel); });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
