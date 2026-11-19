"""#951 -- concept categories (many per concept), import provenance, export.

Written to the ticket's own controls (section 9): every positive assertion has
the control that would make it pass vacuously.
"""
import io

import pytest
from openpyxl import load_workbook

from app import db
from app.models.concept_models import (
    CanonicalLib, Concept, ConceptCategory, ConceptCategoryLink, ConceptImport,
    ConceptImportImmutable, ConceptType, ResponseType, Unit,
)
from app.services import concept_categories as cat_svc
from app.services.concept_export import HEADER, build_xlsx
from app.services.concept_importer import (
    OPTIONAL_COLUMNS, REQUIRED_COLUMNS, parse_csv, parse_xlsx, validate_and_import,
)
from tests.conftest import SAMPLE_SU_BLOB, set_sso_session

HDR = "concept_name,display_text,canonical_lib,canonical_ref,concept_type,response_type,unit,range_low,range_high"
ROW_A = "dx-a-951,Term A,SNOMED,73211009,measurement,numeric,L/min,,"
ROW_B = "dx-b-951,Term B,,,measurement,numeric,L/min,,"


@pytest.fixture(autouse=True)
def _seed(app):
    with app.app_context():
        for model, col, names in ((CanonicalLib, 'canonical_lib_name', ['LOINC', 'SNOMED', 'PDHC', 'local']),
                                  (ConceptType, 'concept_type_name', ['measurement', 'symptom']),
                                  (ResponseType, 'response_type_name', ['numeric', 'yes_no']),
                                  (Unit, 'unit_name', ['L/min'])):
            for n in names:
                if not model.query.filter(getattr(model, col) == n).first():
                    db.session.add(model(**{col: n}))
        for n in ('diabetes-2026', 'cardio-2026'):
            if not ConceptCategory.query.filter_by(category_name=n).first():
                db.session.add(ConceptCategory(category_name=n))
        db.session.commit()
        yield
        ConceptCategoryLink.query.delete()
        Concept.query.delete()
        db.session.execute(db.text("DELETE FROM concept_imports"))
        db.session.commit()


def _imp(csv_text, **kw):
    rows = parse_csv(io.BytesIO(csv_text.encode()))
    kw.setdefault('operator', 'test'); kw.setdefault('filename', 'f.csv'); kw.setdefault('sha256', 'x')
    return validate_and_import(rows, **kw)


def _cats(name):
    return [c.category_name for c in Concept.query.filter_by(concept_name=name).one().categories]


# ------------------------------------------------------------------ stage B

def test_a_batch_category_lands_on_every_row(app):
    with app.app_context():
        r = _imp(f"{HDR}\n{ROW_A}\n{ROW_B}\n", category='diabetes-2026')
        assert r['summary']['n_rejected'] == 0 and r['summary']['n_category_links'] == 2
        assert _cats('dx-a-951') == ['diabetes-2026'] and _cats('dx-b-951') == ['diabetes-2026']


def test_a_row_category_beats_the_batch_default_and_may_name_several(app):
    with app.app_context():
        r = _imp(f"{HDR},category\n{ROW_A},cardio-2026; diabetes-2026\n{ROW_B},\n", category='diabetes-2026')
        assert r['summary']['n_rejected'] == 0
        assert _cats('dx-a-951') == ['cardio-2026', 'diabetes-2026']
        assert _cats('dx-b-951') == ['diabetes-2026']


def test_an_unknown_ROW_category_rejects_that_row_by_name_and_creates_nothing(app):
    with app.app_context():
        n_before = ConceptCategory.query.count()
        r = _imp(f"{HDR},category\n{ROW_A},diabetis-2026\n{ROW_B},\n")
        assert [x['reason'] for x in r['rejected']] == ["category not found: 'diabetis-2026'"]
        assert r['summary']['n_accepted'] == 1
        assert ConceptCategory.query.count() == n_before
        assert Concept.query.filter_by(concept_name='dx-a-951').first() is None


def test_an_unknown_BATCH_category_refuses_the_whole_file(app):
    with app.app_context():
        r = _imp(f"{HDR}\n{ROW_A}\n", category='nope')
        assert r['rejected'][0]['row'] == 'file' and 'nope' in r['rejected'][0]['reason']
        assert Concept.query.count() == 0 and ConceptImport.query.count() == 0


def test_a_second_import_ADDS_a_category_and_keeps_the_first(app):
    with app.app_context():
        _imp(f"{HDR}\n{ROW_A}\n", category='diabetes-2026')
        r = _imp(f"{HDR}\n{ROW_A}\n", category='cardio-2026')
        assert r['summary']['n_unchanged'] == 1
        assert _cats('dx-a-951') == ['cardio-2026', 'diabetes-2026']


def test_extra_columns_are_TOLERATED(app):
    """B.5: pinned, not by omission. The template's review_* columns ride along."""
    with app.app_context():
        r = _imp(f"{HDR},review_snomed_fsn,review_note,anything_else\n{ROW_A},FSN,note,x\n")
        assert r['summary']['n_accepted'] == 1 and r['summary']['n_rejected'] == 0


def test_concept_explain_is_importable(app):
    with app.app_context():
        _imp(f"{HDR},concept_explain\n{ROW_A},Guideline 2026 section 4.2\n")
        assert Concept.query.filter_by(concept_name='dx-a-951').one().concept_explain == 'Guideline 2026 section 4.2'


# ------------------------------------------------------------------ stage C

def test_a_real_import_is_RECORDED_and_a_dry_run_is_not(app):
    with app.app_context():
        dry = _imp(f"{HDR}\n{ROW_A}\n", category='diabetes-2026', dry_run=True)
        assert dry['import_guid'] is None and ConceptImport.query.count() == 0
        assert ConceptCategoryLink.query.count() == 0

        r = _imp(f"{HDR}\n{ROW_A}\n{ROW_B}\n", category='diabetes-2026', entry_point='api',
                 operator='op@x', filename='g.csv', sha256='abc')
        rec = ConceptImport.query.one()
        assert rec.guid == r['import_guid']
        assert (rec.operator, rec.filename, rec.sha256, rec.entry_point) == ('op@x', 'g.csv', 'abc', 'api')
        assert (rec.n_in, rec.n_created, rec.n_rejected, rec.default_categories) == (2, 2, 0, 'diabetes-2026')
        assert {c.import_guid for c in Concept.query.all()} == {rec.guid}
        assert {l.import_guid for l in ConceptCategoryLink.query.all()} == {rec.guid}


def test_an_UPDATE_does_not_claim_the_concept_was_created_by_the_later_import(app):
    with app.app_context():
        first = _imp(f"{HDR}\n{ROW_A}\n")['import_guid']
        _imp(f"{HDR}\n{ROW_A.replace('Term A', 'Term A2')}\n")
        c = Concept.query.filter_by(concept_name='dx-a-951').one()
        assert c.import_guid == first and c.concept_display_text == 'Term A2'


def test_an_import_record_cannot_be_edited(app):
    with app.app_context():
        _imp(f"{HDR}\n{ROW_A}\n")
        rec = ConceptImport.query.one()
        rec.operator = 'someone else'
        with pytest.raises(ConceptImportImmutable):
            db.session.commit()
        db.session.rollback()


# ------------------------------------------------------------------ the three entry points (B.3)

def test_entry_point_CLI(app, tmp_path):
    path = str(tmp_path / 'x951.csv')
    with open(path, 'w') as fh:
        fh.write(f"{HDR}\n{ROW_A}\n")
    res = app.test_cli_runner().invoke(args=['import-concepts', path, '--category', 'cardio-2026'])
    assert res.exit_code == 0, res.output
    with app.app_context():
        assert _cats('dx-a-951') == ['cardio-2026']
        assert ConceptImport.query.one().entry_point == 'cli'


def test_entry_point_API(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    r = client.post('/api/v1/concepts/import', content_type='multipart/form-data', data={
        'file': (io.BytesIO(f"{HDR}\n{ROW_A}\n".encode()), 'a.csv'), 'category': 'cardio-2026'})
    assert r.status_code == 200, r.get_json()
    with app.app_context():
        assert _cats('dx-a-951') == ['cardio-2026']
        assert ConceptImport.query.one().entry_point == 'api'


def test_entry_point_WEB_FORM(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    r = client.post('/concepts/import', content_type='multipart/form-data', data={
        'file': (io.BytesIO(f"{HDR}\n{ROW_A}\n".encode()), 'a.csv'), 'category': 'cardio-2026'})
    assert r.status_code == 200
    with app.app_context():
        assert _cats('dx-a-951') == ['cardio-2026']
        assert ConceptImport.query.one().entry_point == 'web'


# ------------------------------------------------------------------ stage A: filter, hand edit

def test_the_filter_returns_the_category_and_ONLY_it_and_unfiltered_returns_both(app, client):
    with app.app_context():
        _imp(f"{HDR}\n{ROW_A}\n", category='diabetes-2026')
        _imp(f"{HDR}\n{ROW_B}\n")
        guid = ConceptCategory.query.filter_by(category_name='diabetes-2026').one().guid
    names = lambda q: sorted(c['concept_name'] for c in client.get(f'/api/v1/concepts{q}').get_json()['items'])
    assert names('?category=diabetes-2026') == ['dx-a-951']
    assert names(f'?category={guid}') == ['dx-a-951']                 # guid works too
    assert names('?category=cardio-2026') == []
    assert {'dx-a-951', 'dx-b-951'} <= set(names('?per_page=200'))  # the control
    assert client.get('/api/v1/concepts?category=nope').status_code == 400


def test_the_wire_carries_categories_with_urls(app, client):
    with app.app_context():
        _imp(f"{HDR}\n{ROW_A}\n", category='diabetes-2026')
    item = client.get('/api/v1/concepts?category=diabetes-2026').get_json()['items'][0]
    assert [c['category_name'] for c in item['categories']] == ['diabetes-2026']
    assert item['categories'][0]['url'].endswith(item['categories'][0]['guid'])
    assert item['import_url'].endswith(item['import_guid'])


def test_a_hand_edit_REPLACES_the_set_and_an_unknown_one_is_400(app, client):
    with app.app_context():
        _imp(f"{HDR}\n{ROW_A}\n", category='diabetes-2026')
        guid = Concept.query.filter_by(concept_name='dx-a-951').one().guid
    set_sso_session(client, SAMPLE_SU_BLOB)
    r = client.put(f'/api/v1/concepts/{guid}', json={'categories': ['cardio-2026']})
    assert r.status_code == 200, r.get_json()
    assert [c['category_name'] for c in r.get_json()['categories']] == ['cardio-2026']
    assert client.put(f'/api/v1/concepts/{guid}', json={'categories': ['nope']}).status_code == 400
    with app.app_context():
        assert _cats('dx-a-951') == ['cardio-2026']


def test_the_category_table_is_CLOSED_to_an_anonymous_read(client):
    assert client.get('/api/v1/lookup/concept-categories').status_code == 401


# ------------------------------------------------------------------ stage D: export + round trip

def test_the_export_header_is_the_importers_contract_plus_review_columns():
    assert HEADER[:len(REQUIRED_COLUMNS)] == REQUIRED_COLUMNS
    assert set(OPTIONAL_COLUMNS) <= set(HEADER) and 'category' in HEADER and 'concept_explain' in HEADER


def test_the_ROUND_TRIP_is_a_no_op(app):
    """D.3: export N, re-import unchanged -> nothing created, nothing rejected,
    no version moved, categories intact."""
    with app.app_context():
        _imp(f"{HDR},category,concept_explain\n{ROW_A},cardio-2026; diabetes-2026,Section 4\n{ROW_B},,\n")
        before = {c.concept_name: c.vers_number for c in Concept.query.all()}
        buf = build_xlsx(Concept.query.order_by(Concept.concept_name).all())
        ws = load_workbook(io.BytesIO(buf.getvalue())).active
        vals = {r[0]: dict(zip(HEADER, r)) for r in ws.iter_rows(min_row=2, values_only=True)}
        assert vals['dx-b-951']['canonical_lib'] is None, "local exports blank"
        assert vals['dx-a-951']['canonical_lib'] == 'SNOMED'
        buf.seek(0)
        r = validate_and_import(parse_xlsx(buf), operator='t', filename='rt.xlsx', sha256='y')
        assert (r['summary']['n_created'], r['summary']['n_rejected'], r['summary']['n_unchanged']) == (0, 0, 2)
        assert {c.concept_name: c.vers_number for c in Concept.query.all()} == before
        assert _cats('dx-a-951') == ['cardio-2026', 'diabetes-2026']


def test_the_export_takes_the_list_filters_and_is_GATED(app, client):
    with app.app_context():
        _imp(f"{HDR}\n{ROW_A}\n", category='diabetes-2026')
        _imp(f"{HDR}\n{ROW_B}\n")
    assert client.get('/api/v1/concepts/export.xlsx').status_code == 401
    set_sso_session(client, SAMPLE_SU_BLOB)
    r = client.get('/api/v1/concepts/export.xlsx?category=diabetes-2026')
    assert r.status_code == 200
    names = [row[0] for row in load_workbook(io.BytesIO(r.data)).active.iter_rows(min_row=2, values_only=True)]
    assert names == ['dx-a-951']


def test_an_import_record_lists_what_it_produced(app, client):
    with app.app_context():
        g = _imp(f"{HDR}\n{ROW_A}\n", category='diabetes-2026')['import_guid']
    set_sso_session(client, SAMPLE_SU_BLOB)
    d = client.get(f'/api/v1/concept-imports/{g}').get_json()
    assert len(d['created_concepts']) == 1 and len(d['category_links']) == 1
    assert d['default_categories'] == ['diabetes-2026']


# ------------------------------------------------------------------ the migration

def test_one_alembic_head_and_a_short_revision_id():
    import pathlib, re
    vers = pathlib.Path(__file__).resolve().parents[1] / 'migrations' / 'versions'
    revs, downs = set(), set()
    for f in vers.glob('*.py'):
        t = f.read_text()
        revs.add(re.search(r"^revision = ['\"]([^'\"]+)", t, re.M).group(1))
        m = re.search(r"^down_revision = ['\"]([^'\"]+)", t, re.M)
        if m:
            downs.add(m.group(1))
    heads = revs - downs
    assert len(heads) == 1, heads   # the head itself is pinned by the newest migration's test
    assert all(len(r) <= 32 for r in revs)


# ------------------------------------------------------------------ A.6 the web form

def test_web_CREATE_and_EDIT_set_categories_and_an_empty_selection_clears(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    with app.app_context():
        d, c = (ConceptCategory.query.filter_by(category_name=n).one().guid for n in ('diabetes-2026', 'cardio-2026'))
        lib = CanonicalLib.query.filter_by(canonical_lib_name='local').one().guid
    r = client.post('/concepts/create', data={'concept_name': 'web-951', 'canonical_lib': lib,
                                              'categories': [d, c], 'categories_present': '1'})
    assert r.status_code in (200, 302)
    with app.app_context():
        concept = Concept.query.filter_by(concept_name='web-951').one()
        assert _cats('web-951') == ['cardio-2026', 'diabetes-2026']
        guid = concept.guid
    page = client.get(f'/concepts/{guid}/edit').get_data(as_text=True)
    assert 'name="categories"' in page and 'diabetes-2026' in page
    client.post(f'/concepts/{guid}/edit', data={'concept_name': 'web-951', 'canonical_lib': lib,
                                                'categories': [c], 'categories_present': '1'})
    with app.app_context():
        assert _cats('web-951') == ['cardio-2026']
    client.post(f'/concepts/{guid}/edit', data={'concept_name': 'web-951', 'canonical_lib': lib,
                                                'categories_present': '1'})
    with app.app_context():
        assert _cats('web-951') == []
    assert 'Categories' in client.get(f'/concepts/{guid}').get_data(as_text=True)


def test_a_LEGACY_name_round_trips_but_a_new_one_must_follow_the_grammar(app):
    """Production 2026-11-17: 58 of 107 concepts have pre-rule names; the
    round trip rejected all of them. An existing name is a key, a new one is not."""
    with app.app_context():
        lib = CanonicalLib.query.filter_by(canonical_lib_name='local').one().guid
        db.session.add(Concept(concept_name='bp_systolic', canonical_lib=lib, concept_display_text='Systolic'))
        db.session.commit()
        buf = build_xlsx(Concept.query.filter_by(concept_name='bp_systolic').all())
        r = validate_and_import(parse_xlsx(buf), operator='t', filename='rt.xlsx', sha256='y')
        assert (r['summary']['n_rejected'], r['summary']['n_created']) == (0, 0), r['rejected']
        r2 = _imp(f"{HDR}\nbp_diastolic,Diastolic,,,measurement,numeric,L/min,,\n")
        assert r2['summary']['n_rejected'] == 1 and 'lowercase' in r2['rejected'][0]['reason']
