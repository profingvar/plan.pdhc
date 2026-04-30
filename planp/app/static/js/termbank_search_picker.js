/* termbank_search_picker.js — click-to-fill search widget for the
 * Concept and ValueCatalog create/edit forms.
 *
 * Auto-binds to any element with class "termbank-search-picker" and
 * these data attributes:
 *   data-name-input    — DOM id of the form's name field (display)
 *   data-system-select — DOM id of the canonical_lib <select>
 *   data-code-input    — DOM id of the canonical_refnumber <input>
 *
 * The widget reads system options from the named canonical_lib select,
 * so it stays in sync with whatever CanonicalLib rows the page renders.
 *
 * Calls /api/v1/termbank/search with a "prechosen libs" multi-select
 * (one checkbox per canonical lib) so users can scope the search
 * across several systems at once. Repeated `system=…` query params
 * are sent — termbank's /search honours them. On click of a result
 * the form fields are populated.
 */
(function () {
  function escapeHtml(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function debounce(fn, ms) {
    var t;
    return function () {
      var args = arguments, ctx = this;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(ctx, args); }, ms);
    };
  }

  // Fallback list of termbank systems when no canonical_lib <select> is
  // exposed on the page (e.g. on edit forms that don't let you change
  // the library). Keep in sync with the seed migration's CANONICAL_LIBS.
  var FALLBACK_SYSTEMS = ["loinc", "socialstyrelsen", "icd10", "atc", "snomed", "icf"];

  function readEntries(libSelect) {
    // Each entry is { name, label } — name is the short canonical
    // identifier sent to termbank's `/search?system=`, label is the
    // human-friendly display.
    if (!libSelect) {
      return FALLBACK_SYSTEMS.map(function (n) { return { name: n, label: n }; });
    }
    var entries = [];
    Array.prototype.forEach.call(libSelect.options, function (opt) {
      if (!opt.value) return;
      var name = (opt.getAttribute("data-name") || opt.textContent || "").trim();
      var label = (opt.textContent || "").trim() || name;
      if (name) entries.push({ name: name, label: label });
    });
    return entries;
  }

  function buildSystemCheckboxes(panel, entries) {
    // Modern container; falls back to the legacy <select data-termbank-system>
    // for templates that haven't been migrated yet.
    var box = panel.querySelector("[data-termbank-systems]");
    if (!box) {
      var legacy = panel.querySelector("[data-termbank-system]");
      if (legacy) {
        legacy.innerHTML = '<option value="">All libraries</option>';
        entries.forEach(function (e) {
          var o = document.createElement("option");
          o.value = e.name;
          o.textContent = e.label;
          legacy.appendChild(o);
        });
      }
      return;
    }
    box.innerHTML = "";
    box.style.display = "flex";
    box.style.flexWrap = "wrap";
    box.style.gap = "0.5rem 0.9rem";
    entries.forEach(function (e) {
      var label = document.createElement("label");
      label.style.display = "inline-flex";
      label.style.alignItems = "center";
      label.style.gap = "0.25rem";
      label.style.fontSize = "0.85em";
      label.style.cursor = "pointer";
      var cb = document.createElement("input");
      cb.type = "checkbox";
      cb.value = e.name;
      cb.setAttribute("data-termbank-system-cb", "");
      label.appendChild(cb);
      label.appendChild(document.createTextNode(" " + e.label));
      box.appendChild(label);
    });
  }

  function selectedSystems(panel) {
    var modern = panel.querySelectorAll("[data-termbank-system-cb]:checked");
    if (modern && modern.length) {
      return Array.prototype.map.call(modern, function (cb) { return cb.value; });
    }
    var legacy = panel.querySelector("[data-termbank-system]");
    if (legacy && legacy.value) return [legacy.value];
    return [];
  }

  function applyResult(panel, result) {
    var nameId = panel.getAttribute("data-name-input");
    var sysId = panel.getAttribute("data-system-select");
    var codeId = panel.getAttribute("data-code-input");

    var nameInput = nameId ? document.getElementById(nameId) : null;
    var libSelect = sysId ? document.getElementById(sysId) : null;
    var codeInput = codeId ? document.getElementById(codeId) : null;

    if (codeInput) codeInput.value = result.code || "";

    if (libSelect) {
      // Match by option text (= canonical_lib_name on server)
      Array.prototype.forEach.call(libSelect.options, function (opt) {
        if ((opt.textContent || "").trim() === result.system) {
          libSelect.value = opt.value;
        }
      });
    }

    if (nameInput && !nameInput.value.trim() && result.display) {
      nameInput.value = result.display;
    }

    // Visual feedback — flash the affected fields
    [nameInput, libSelect, codeInput].forEach(function (el) {
      if (!el) return;
      var prev = el.style.backgroundColor;
      el.style.backgroundColor = "#fff8c5";
      setTimeout(function () { el.style.backgroundColor = prev; }, 600);
    });
  }

  function renderResults(panel, body) {
    var box = panel.querySelector("[data-termbank-results]");
    if (!body || body.error) {
      box.innerHTML =
        '<p style="color:var(--text-muted);font-style:italic;">' +
        "Termbank unavailable." +
        "</p>";
      return;
    }
    var results = body.results || [];
    if (!results.length) {
      box.innerHTML =
        '<p style="color:var(--text-muted);font-style:italic;">' +
        "No matches." + "</p>";
      return;
    }

    var html = '<ul class="termbank-results-list" style="list-style:none;padding:0;margin:0;border:1px solid var(--border-color, #ddd);border-radius:4px;max-height:240px;overflow-y:auto;">';
    results.forEach(function (r, i) {
      html +=
        '<li style="padding:0.4rem 0.6rem;border-bottom:1px solid #eee;cursor:pointer;display:flex;justify-content:space-between;gap:0.5rem;"' +
        ' data-result-index="' + i + '">' +
        '<span><strong>' + escapeHtml(r.display || "") + "</strong>" +
        '<br><code style="font-size:0.8em;color:var(--text-muted);">' +
        escapeHtml(r.system || "") + ":" + escapeHtml(r.code || "") + "</code></span>" +
        '<span style="font-size:0.75em;color:var(--text-muted);align-self:center;">' +
        escapeHtml(r.status || "") + "</span>" +
        "</li>";
    });
    html += "</ul>";
    box.innerHTML = html;

    Array.prototype.forEach.call(box.querySelectorAll("[data-result-index]"), function (li) {
      li.addEventListener("click", function () {
        var idx = parseInt(li.getAttribute("data-result-index"), 10);
        applyResult(panel, results[idx]);
      });
      li.addEventListener("mouseover", function () {
        li.style.backgroundColor = "#f5f5f5";
      });
      li.addEventListener("mouseout", function () {
        li.style.backgroundColor = "";
      });
    });
  }

  function bind(panel) {
    var qInput = panel.querySelector("[data-termbank-q]");
    var libSelectId = panel.getAttribute("data-system-select");
    var libSelect = libSelectId ? document.getElementById(libSelectId) : null;

    buildSystemCheckboxes(panel, readEntries(libSelect));

    function search() {
      var q = (qInput.value || "").trim();
      if (q.length < 2) {
        panel.querySelector("[data-termbank-results]").innerHTML = "";
        return;
      }
      var url = "/api/v1/termbank/search?q=" + encodeURIComponent(q) + "&limit=10";
      selectedSystems(panel).forEach(function (s) {
        url += "&system=" + encodeURIComponent(s);
      });
      fetch(url)
        .then(function (r) { return r.ok ? r.json() : { error: "http_" + r.status, results: [] }; })
        .then(function (body) { renderResults(panel, body); })
        .catch(function () { renderResults(panel, { error: "unreachable", results: [] }); });
    }

    var debounced = debounce(search, 300);
    qInput.addEventListener("input", debounced);
    panel.addEventListener("change", function (ev) {
      if (ev.target && ev.target.matches("[data-termbank-system-cb], [data-termbank-system]")) {
        search();
      }
    });
  }

  function init() {
    document.querySelectorAll(".termbank-search-picker").forEach(bind);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
