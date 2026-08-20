/*
 * Guided authoring assistant — builder/concept-form panel (GA-4, epic #516).
 *
 * Opt-in, non-blocking. Mounts a "Check" (deterministic Layer-1 validate) and,
 * when an API key is configured, an "Assist" (Claude Layer-2 suggest) affordance
 * onto:
 *   - a concept form  : <div data-authoring-assistant="concept">
 *   - the plan builder : <div data-authoring-assistant="plandef">
 *
 * It calls the opt-in API at /api/v1/authoring/*. If the tool is disabled
 * (GET /models -> {enabled:false}) or the call fails, the panel simply does
 * not render — nothing about the existing form/save behaviour changes. The
 * assistant only proposes a REVIEWED DRAFT the author confirms; it never saves.
 */
(function () {
  "use strict";

  var API = "/api/v1/authoring";

  // #571: the Layer-2 Anthropic key is entered per session and held ONLY in
  // this tab's memory (never localStorage, never the server, never .env). It
  // is sent as X-Anthropic-Key on the single /assist call the operator
  // triggers, and is gone on logout / reload.
  var SESSION_KEY = "";

  function fetchJSON(url, opts) {
    opts = opts || {};
    opts.credentials = "same-origin";
    return fetch(url, opts).then(function (r) {
      return r.ok ? r.json() : Promise.reject(new Error("HTTP " + r.status));
    });
  }

  function h(tag, attrs, kids) {
    var e = document.createElement(tag);
    attrs = attrs || {};
    Object.keys(attrs).forEach(function (k) {
      if (k === "style") e.setAttribute("style", attrs[k]);
      else if (k === "class") e.className = attrs[k];
      else if (k === "html") e.innerHTML = attrs[k];
      else e.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) {
      e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return e;
  }

  var CARD = "background:#f9f9f9;border:1px solid #e2e2e2;border-radius:6px;" +
             "padding:0.75rem 1rem;margin-bottom:1rem;";
  var BTN = "display:inline-flex;align-items:center;gap:0.35rem;padding:0.4rem 0.8rem;" +
            "border:1px solid #4a6;background:#eef7f0;color:#264;border-radius:5px;" +
            "cursor:pointer;font-size:0.9rem;";

  // ---- issue rendering ---------------------------------------------------
  function renderIssues(target, summary) {
    target.innerHTML = "";
    if (!summary) return;
    if (summary.ok && (!summary.issues || summary.issues.length === 0)) {
      target.appendChild(h("div", {
        style: "color:#264;background:#eef7f0;border:1px solid #bd9;padding:0.5rem 0.75rem;border-radius:5px;"
      }, ["✓ Looks good — no problems found."]));
      return;
    }
    var head = "" + (summary.error_count || 0) + " error(s), " +
               (summary.warning_count || 0) + " warning(s)";
    target.appendChild(h("div", { style: "font-weight:600;margin-bottom:0.35rem;" }, [head]));
    (summary.issues || []).forEach(function (i) {
      var err = i.severity === "error";
      var box = h("div", {
        style: "border-left:3px solid " + (err ? "#c33" : "#e6a100") + ";" +
               "background:" + (err ? "#fdf0f0" : "#fdf8ec") + ";" +
               "padding:0.35rem 0.6rem;margin-bottom:0.3rem;border-radius:3px;font-size:0.88rem;"
      });
      box.appendChild(h("span", {
        style: "font-weight:600;color:" + (err ? "#c33" : "#a67c00") + ";"
      }, [(err ? "ERROR " : "WARN ") + (i.code || "")]));
      box.appendChild(h("span", { style: "margin-left:0.4rem;" }, [i.message || ""]));
      if (i.field) box.appendChild(h("span", { style: "color:#888;" }, [" (" + i.field + ")"]));
      if (i.hint) box.appendChild(h("div", { style: "color:#555;margin-top:0.15rem;" }, ["→ " + i.hint]));
      target.appendChild(box);
    });
  }

  // ---- concept form ------------------------------------------------------
  function val(id) {
    var e = document.getElementById(id);
    return e ? (e.value || "") : "";
  }

  function conceptPayload() {
    return {
      response_type: val("response_type"),
      unit: val("unit"),
      valueset: val("valueset"),
      canonical_lib: val("canonical_lib"),
      canonical_refnumber: val("canonical_refnumber"),
      range_low: val("range_low"),
      range_high: val("range_high")
    };
  }

  function setSelectByName(selectId, name) {
    if (!name) return false;
    var sel = document.getElementById(selectId);
    if (!sel) return false;
    var want = String(name).trim().toLowerCase();
    var i, opt, cand;
    for (i = 0; i < sel.options.length; i++) {
      opt = sel.options[i];
      cand = (opt.getAttribute("data-name") || opt.textContent || "").trim().toLowerCase();
      if (cand && cand === want) { sel.value = opt.value; return true; }
    }
    for (i = 0; i < sel.options.length; i++) {
      opt = sel.options[i];
      cand = (opt.getAttribute("data-name") || opt.textContent || "").trim().toLowerCase();
      if (cand && (cand.indexOf(want) !== -1 || want.indexOf(cand) !== -1)) {
        sel.value = opt.value; return true;
      }
    }
    return false;
  }

  function setInput(id, value) {
    var e = document.getElementById(id);
    if (e && value !== null && value !== undefined && value !== "") e.value = value;
  }

  function applyProposal(p) {
    if (!p) return;
    setInput("canonical_refnumber", p.canonical_refnumber);
    setInput("range_low", p.range_low);
    setInput("range_high", p.range_high);
    setSelectByName("response_type", p.response_type);
    setSelectByName("unit", p.unit_display || p.unit_ucum);
    setSelectByName("canonical_lib", p.canonical_lib);
    // valueset is only a hint (no id to bind) — left for the author.
  }

  function renderProposal(target, res) {
    target.innerHTML = "";
    if (!res.assistant_available) {
      target.appendChild(h("div", { style: "color:#a67c00;" },
        ["Assistant unavailable (" + (res.reason || "unknown") + "). The Check button still works."]));
    }
    if (res.reuse_candidates && res.reuse_candidates.length) {
      var ul = h("ul", { style: "margin:0.25rem 0 0.5rem 1rem;font-size:0.85rem;color:#333;" });
      res.reuse_candidates.slice(0, 5).forEach(function (c) {
        var label = c.concept_name
          ? (c.concept_name + (c.canonical_refnumber ? " [" + c.canonical_refnumber + "]" : ""))
          : ((c.display || "") + " " + (c.system || "") + " " + (c.code || ""));
        ul.appendChild(h("li", {}, [label + " — " + (c.why || "")]));
      });
      target.appendChild(h("div", { style: "font-weight:600;font-size:0.85rem;" }, ["Reuse an existing concept?"]));
      target.appendChild(ul);
    }
    var p = res.proposal;
    if (p) {
      var pretty = [
        ["Response type", p.response_type],
        ["Unit", (p.unit_display || "") + (p.unit_ucum ? " (UCUM " + p.unit_ucum + ")" : "")],
        ["Terminology", (p.canonical_lib || "") + " " + (p.canonical_refnumber || "")],
        ["Range", (p.range_low != null ? p.range_low : "") + " – " + (p.range_high != null ? p.range_high : "")],
        ["Answers", p.valueset_hint || ""]
      ].filter(function (r) { return String(r[1]).trim(); });
      var tbl = h("div", { style: "font-size:0.88rem;margin:0.35rem 0;" });
      pretty.forEach(function (r) {
        tbl.appendChild(h("div", {}, [
          h("span", { style: "display:inline-block;width:110px;color:#666;" }, [r[0] + ":"]),
          h("span", { style: "font-weight:600;" }, [String(r[1])])
        ]));
      });
      target.appendChild(tbl);
      if (p.rationale) {
        target.appendChild(h("div", { style: "font-size:0.85rem;color:#444;font-style:italic;margin-bottom:0.4rem;" },
          [p.rationale]));
      }
      var apply = h("button", { type: "button", style: BTN }, ["Apply to form (review before saving)"]);
      apply.addEventListener("click", function () {
        applyProposal(p);
        apply.textContent = "✓ Applied — review, then Save";
      });
      target.appendChild(apply);
    }
    if (res.validation) {
      var vwrap = h("div", { style: "margin-top:0.5rem;" });
      target.appendChild(h("div", { style: "font-weight:600;font-size:0.85rem;margin-top:0.4rem;" },
        ["Check of this suggestion:"]));
      target.appendChild(vwrap);
      renderIssues(vwrap, res.validation);
    }
  }

  function buildConceptPanel(mount, models) {
    var card = h("div", { style: CARD });
    card.appendChild(h("h4", { style: "margin:0 0 0.5rem 0;" }, ["Authoring assistant (optional)"]));

    var checkBtn = h("button", { type: "button", style: BTN }, ["✓ Check this concept"]);
    var out = h("div", { style: "margin-top:0.5rem;" });
    checkBtn.addEventListener("click", function () {
      out.innerHTML = "Checking…";
      fetchJSON(API + "/validate", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ kind: "concept", payload: conceptPayload() })
      }).then(function (res) { renderIssues(out, res); })
        .catch(function () { out.textContent = "Check unavailable right now."; });
    });
    card.appendChild(checkBtn);
    card.appendChild(out);

    // #571: Layer-2 "Suggest" uses a PER-SESSION key entered here — never
    // stored server-side or in .env, gone on logout/reload.
    card.appendChild(h("hr", { style: "border:none;border-top:1px solid #e2e2e2;margin:0.75rem 0;" }));

    var keyInput = h("input", {
      type: "password", class: "form-control", autocomplete: "off",
      placeholder: "Anthropic API key — this session only",
      style: "max-width:320px;"
    });
    var keyStatus = h("span", { style: "font-size:0.8rem;margin-left:0.5rem;color:#666;" }, [""]);
    var useBtn = h("button", { type: "button", style: BTN }, ["Use key this session"]);
    var forgetBtn = h("button", { type: "button", style: BTN + "margin-left:0.4rem;" }, ["Forget key"]);
    var layer2 = h("div", { style: "margin-top:0.6rem;" });

    function renderLayer2() {
      layer2.innerHTML = "";
      keyStatus.textContent = SESSION_KEY ? "key set for this session" : "no key this session";
      if (!SESSION_KEY) {
        layer2.appendChild(h("div", { style: "font-size:0.8rem;color:#888;" },
          ["Enter your Anthropic key above to enable Claude suggestions for this session. The Check button works without a key."]));
        return;
      }
      layer2.appendChild(h("label", { style: "font-size:0.85rem;font-weight:600;" },
        ["Describe what you want to collect, and let the assistant propose the binding:"]));
      var intent = h("textarea", {
        class: "form-control", rows: "2",
        placeholder: "e.g. track morning peak expiratory flow"
      });
      layer2.appendChild(intent);
      var modelSel = h("select", { class: "form-control", style: "max-width:260px;margin-top:0.4rem;" });
      (models.models || []).forEach(function (m) {
        var o = h("option", { value: m }, [m]);
        if (m === models.default_model) o.setAttribute("selected", "selected");
        modelSel.appendChild(o);
      });
      layer2.appendChild(h("div", { style: "display:flex;align-items:center;gap:0.5rem;margin-top:0.4rem;" },
        [h("span", { style: "font-size:0.8rem;color:#666;" }, ["Model:"]), modelSel]));
      var assistBtn = h("button", { type: "button", style: BTN + "margin-top:0.5rem;" }, ["Suggest"]);
      var pout = h("div", { style: "margin-top:0.5rem;" });
      assistBtn.addEventListener("click", function () {
        var q = intent.value.trim();
        if (!q) { pout.textContent = "Type what you want to collect first."; return; }
        if (!SESSION_KEY) { pout.textContent = "Enter your Anthropic key first."; return; }
        pout.innerHTML = "Thinking…";
        fetchJSON(API + "/assist", {
          method: "POST",
          headers: { "content-type": "application/json", "X-Anthropic-Key": SESSION_KEY },
          body: JSON.stringify({ intent: q, model: modelSel.value })
        }).then(function (res) { renderProposal(pout, res); })
          .catch(function () { pout.textContent = "Assistant unavailable right now."; });
      });
      layer2.appendChild(assistBtn);
      layer2.appendChild(pout);
    }

    useBtn.addEventListener("click", function () {
      var v = (keyInput.value || "").trim();
      if (!v) { keyStatus.textContent = "paste your Anthropic key first"; return; }
      SESSION_KEY = v; keyInput.value = "";
      renderLayer2();
    });
    forgetBtn.addEventListener("click", function () { SESSION_KEY = ""; renderLayer2(); });

    card.appendChild(h("div", { style: "display:flex;align-items:center;gap:0.4rem;flex-wrap:wrap;" },
      [keyInput, useBtn, forgetBtn, keyStatus]));
    card.appendChild(h("div", { style: "font-size:0.75rem;color:#999;margin-top:0.2rem;" },
      ["Held only in this browser tab for this session — sent to the server only to make the one Claude call you trigger, never stored, and gone on logout or reload."]));
    card.appendChild(layer2);
    renderLayer2();

    mount.appendChild(card);
  }

  // ---- plan builder ------------------------------------------------------
  function plandefPayload() {
    var txns = [];
    document.querySelectorAll('select[name*="concept"]').forEach(function (s) {
      if (s.value) txns.push({ concept_guid: s.value });
    });
    var payload = { transactions: txns };
    // Include goal/target-unit rows from the hidden goal JSON if present.
    var gj = document.getElementById("goalJson");
    if (gj && gj.value) {
      try {
        var goals = JSON.parse(gj.value);
        if (Array.isArray(goals)) payload.goals = goals;
      } catch (e) { /* ignore malformed preview state */ }
    }
    return payload;
  }

  function renderRealisability(target, res) {
    target.innerHTML = "";
    if (!res || res.available === false) {
      var why = res && res.reason === "rosetta_not_configured"
        ? "openEHR export target not configured yet."
        : "openEHR check unavailable (" + ((res && res.reason) || "error") + ").";
      target.appendChild(h("div", { style: "color:#a67c00;" }, [why]));
      return;
    }
    var head = res.realisable_count + " of " + res.total +
               " data point(s) are openEHR-realisable" +
               (res.all_realisable ? " ✓" : "");
    target.appendChild(h("div", { style: "font-weight:600;margin-bottom:0.35rem;" }, [head]));
    if (res.templates && res.templates.length) {
      target.appendChild(h("div", { style: "font-size:0.82rem;color:#666;margin-bottom:0.35rem;" },
        ["Template(s): " + res.templates.join(", ")]));
    }
    (res.concepts || []).forEach(function (c) {
      var color = c.status === "realisable" ? "#4a6"
                : c.status === "pending" ? "#e6a100" : "#c33";
      var bg = c.status === "realisable" ? "#eef7f0"
             : c.status === "pending" ? "#fdf8ec" : "#fdf0f0";
      var box = h("div", {
        style: "border-left:3px solid " + color + ";background:" + bg +
               ";padding:0.35rem 0.6rem;margin-bottom:0.3rem;border-radius:3px;font-size:0.88rem;"
      });
      box.appendChild(h("span", { style: "font-weight:600;text-transform:uppercase;color:" + color + ";" },
        [c.status]));
      box.appendChild(h("span", { style: "margin-left:0.4rem;" },
        [c.concept_name || c.concept_guid]));
      (c.blockers || []).forEach(function (b) {
        box.appendChild(h("div", { style: "color:#555;margin-top:0.15rem;" }, ["→ " + b]));
      });
      target.appendChild(box);
    });
  }

  function buildBuilderPanel(mount, models) {
    var card = h("div", { style: CARD });
    card.appendChild(h("h4", { style: "margin:0 0 0.5rem 0;" }, ["Check this plan (optional)"]));

    var btn = h("button", { type: "button", style: BTN }, ["✓ Check plan"]);
    var out = h("div", { style: "margin-top:0.5rem;" });
    btn.addEventListener("click", function () {
      out.innerHTML = "Checking…";
      fetchJSON(API + "/validate", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ kind: "plandef", payload: plandefPayload() })
      }).then(function (res) { renderIssues(out, res); })
        .catch(function () { out.textContent = "Check unavailable right now."; });
    });

    var oe = h("button", { type: "button", style: BTN + "margin-left:0.5rem;" },
      ["⇄ Check openEHR export"]);
    var oeOut = h("div", { style: "margin-top:0.5rem;" });
    oe.addEventListener("click", function () {
      oeOut.innerHTML = "Checking openEHR export readiness…";
      fetchJSON(API + "/openehr-realisable", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(plandefPayload())
      }).then(function (res) { renderRealisability(oeOut, res); })
        .catch(function () { oeOut.textContent = "openEHR check unavailable right now."; });
    });

    card.appendChild(btn);
    card.appendChild(oe);
    card.appendChild(out);
    card.appendChild(oeOut);
    mount.appendChild(card);
  }

  // ---- boot --------------------------------------------------------------
  document.addEventListener("DOMContentLoaded", function () {
    var conceptMount = document.querySelector('[data-authoring-assistant="concept"]');
    var builderMount = document.querySelector('[data-authoring-assistant="plandef"]');
    if (!conceptMount && !builderMount) return;
    fetchJSON(API + "/models").then(function (models) {
      if (!models || !models.enabled) return; // opt-in: render nothing when off
      if (conceptMount) buildConceptPanel(conceptMount, models);
      if (builderMount) buildBuilderPanel(builderMount, models);
    }).catch(function () { /* disabled or unreachable -> stay hidden */ });
  });
})();
