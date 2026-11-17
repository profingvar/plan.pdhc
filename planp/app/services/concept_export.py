"""#951 stage D: the concept catalogue out, in the format it comes back in.

The column contract is the importer's own (REQUIRED + OPTIONAL), in the
template's order, followed by the template's review-only columns left blank.
So export -> edit -> re-import is a round trip, and re-importing an unchanged
file is a NO-OP: the importer reports every row `unchanged` and bumps no
`vers_number` (D.3, tested).

What is written, and what is NOT (D.4, L2):
- `display_text` is `concept_display_text`, which plan wrote itself. SNOMED's
  own descriptions are never emitted -- plan does not store them, and a
  public repo / file must not carry them.
- lookups are written by NAME (the importer resolves names), so the file is
  readable and portable between databases;
- a LOCAL concept is written with a BLANK `canonical_lib`, the importer's own
  spelling of "local" (#786);
- categories are '; '-joined names.
"""
from __future__ import annotations

import io

from app.models.concept_models import CanonicalLib, ConceptType, ResponseType, Unit
from app.services.canonical_libs import LOCAL_LIB_NAME
from app.services.concept_importer import OPTIONAL_COLUMNS, REQUIRED_COLUMNS

#: Never imported; present so a reviewer can work in the exported file.
REVIEW_COLUMNS = ['review_snomed_fsn', 'review_confidence', 'review_source', 'review_note']
HEADER = REQUIRED_COLUMNS + OPTIONAL_COLUMNS + REVIEW_COLUMNS


def _names(model, name_attr):
    return {r.guid: getattr(r, name_attr) for r in model.query.all()}


def rows(concepts) -> list[dict]:
    libs = _names(CanonicalLib, 'canonical_lib_name')
    types = _names(ConceptType, 'concept_type_name')
    resp = _names(ResponseType, 'response_type_name')
    units = _names(Unit, 'unit_name')
    out = []
    for c in concepts:
        lib = libs.get(c.canonical_lib)
        out.append({
            'concept_name': c.concept_name,
            'display_text': c.concept_display_text,
            'canonical_lib': None if lib == LOCAL_LIB_NAME else lib,
            'canonical_ref': c.canonical_refnumber,
            'concept_type': types.get(c.concept_type),
            'response_type': resp.get(c.response_type),
            'unit': units.get(c.unit),
            'range_low': c.range_low,
            'range_high': c.range_high,
            'category': '; '.join(k.category_name for k in c.categories) or None,
            'concept_explain': c.concept_explain,
        })
    return out


def build_xlsx(concepts) -> io.BytesIO:
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'concepts'
    ws.append(HEADER)
    for r in rows(concepts):
        ws.append([r.get(h) for h in HEADER])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf
