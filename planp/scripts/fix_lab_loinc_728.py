"""#728 follow-up: correct plan.pdhc's LOINC bindings for the 19 lab concepts whose
code did not mean what the concept measures (checked against termbank's LOINC
table 2026-11-17). Same path as PUT /concepts/<guid>: guard_concept on the
effective state, then vers_number+1 and date_valid=now. DRY unless APPLY=1."""
import os, sys
from datetime import datetime, timezone
from app import create_app
app = create_app()
from app import db
from app.models.concept_models import Concept, CanonicalLib
from app.services.save_guard import guard_concept, SaveBlocked

LOINC = {  # concept_name: (old, new, termbank display)
 "fasting_plasma_glucose": ("1558-6", "14771-0", "Fasting glucose [Moles/volume] in Serum or Plasma"),
 "random_plasma_glucose": ("2345-7", "14749-6", "Glucose [Moles/volume] in Serum or Plasma"),
 "total_cholesterol": ("2093-3", "14647-2", "Cholesterol [Moles/volume] in Serum or Plasma"),
 "hdl_cholesterol": ("2085-9", "14646-4", "Cholesterol in HDL [Moles/volume] in Serum or Plasma"),
 "ldl_cholesterol": ("18262-6", "22748-8", "Cholesterol in LDL [Moles/volume] in Serum or Plasma"),
 "non_hdl_cholesterol": ("43396-1", "70204-3", "Cholesterol non HDL [Moles/volume] in Serum or Plasma"),
 "triglycerides": ("2571-8", "14927-8", "Triglyceride [Moles/volume] in Serum or Plasma"),
 "free_t4": ("3024-7", "14920-3", "Thyroxine (T4) free [Moles/volume] in Serum or Plasma"),
 "egfr": ("33914-3", "62238-1", "GFR by Creatinine-based formula (CKD-EPI)/1.73 sq M"),
 "urine_acr": ("14959-1", "32294-1", "Albumin/Creatinine [Ratio] in Urine (mg/mmol)"),
 "cgm_raw": ("41653-7", "105272-9", "Glucose [Moles/volume] in Interstitial fluid"),
 "cgm_mean_glucose": ("97506-0", "105273-7", "Glucose [Moles/volume] Reporting Period mean, Interstitial fluid"),
 "cgm_cv": ("97507-8", "104638-2", "Glucose SD/Glucose mean, Reporting Period, Interstitial fluid"),
 "B-glucos": ("090307", "15074-8", "Glucose [Moles/volume] in Blood"),  # was filed as SNOMED
}
LOCAL = {  # no active LOINC code in termbank says exactly this
 "hba1c": ("4548-4", "HBA1C-IFCC", "IFCC mmol/mol: the only IFCC molar code (106634-9) is deprecated"),
 "cgm_tir": ("97509-4", "CGM-TIR", "no LOINC 'time in range' code; 97510-2 counts readings, not time"),
 "cgm_tar": ("97508-6", "CGM-TAR", "104640-8 is level 1 only (10.1-13.9); the concept is all >10.0"),
 "cgm_tbr": ("97510-2", "CGM-TBR", "104641-6 is level 1 only (3.0-3.8); the concept is all <3.9"),
 "cgm_hypo_count": ("97511-0", "CGM-HYPO-COUNT", "no LOINC code for CGM hypoglycaemia events"),
}
apply = os.environ.get("APPLY") == "1"
with app.app_context():
    libs = {l.canonical_lib_name: l.guid for l in CanonicalLib.query.all()}
    n = 0
    for name, spec in list(LOINC.items()) + list(LOCAL.items()):
        cs = Concept.query.filter_by(concept_name=name).all()
        assert len(cs) == 1, (name, len(cs))
        c = cs[0]
        old, new = spec[0], spec[1]
        lib = libs["loinc"] if name in LOINC else libs["local"]
        cur_lib = {v: k for k, v in libs.items()}[c.canonical_lib]
        assert c.canonical_refnumber == old, (name, c.canonical_refnumber, old)
        eff = {"response_type": c.response_type, "unit": c.unit, "valueset": c.valueset,
               "canonical_lib": lib, "canonical_refnumber": new,
               "range_low": c.range_low, "range_high": c.range_high}
        try:
            guard_concept(eff)
        except SaveBlocked as e:
            print("BLOCKED", name, e.as_dict()); sys.exit(1)
        print(f"{name:24} {cur_lib}:{old:9} -> {'loinc' if name in LOINC else 'local'}:{new:15} v{c.vers_number}->v{(c.vers_number or 1)+1}  {spec[2]}")
        if apply:
            c.canonical_lib = lib; c.canonical_refnumber = new
            c.vers_number = (c.vers_number or 1) + 1
            c.date_valid = datetime.now(timezone.utc)
        n += 1
    if apply:
        db.session.commit()
    print(("APPLIED " if apply else "DRY RUN ") + str(n))
