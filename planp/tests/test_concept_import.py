"""Tests for the concept catalogue bulk importer (ticket #134)."""
import io
import os

import pytest

from app import db
from app.models.concept_models import (
    Concept, CanonicalLib, ConceptType, ResponseType, Unit,
)
from app.services.concept_importer import (
    parse_csv, validate_and_import, ImportError_,
)

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


@pytest.fixture(autouse=True)
def _seed_lookups(app):
    """Seed the lookup tables once for these tests."""
    with app.app_context():
        if not CanonicalLib.query.filter_by(canonical_lib_name='LOINC').first():
            db.session.add(CanonicalLib(canonical_lib_name='LOINC'))
            db.session.add(CanonicalLib(canonical_lib_name='SNOMED'))
            db.session.add(CanonicalLib(canonical_lib_name='PDHC'))
        if not ConceptType.query.filter_by(concept_type_name='measurement').first():
            db.session.add(ConceptType(concept_type_name='measurement'))
            db.session.add(ConceptType(concept_type_name='symptom'))
        if not ResponseType.query.filter_by(response_type_name='numeric').first():
            db.session.add(ResponseType(response_type_name='numeric'))
            db.session.add(ResponseType(response_type_name='yes_no'))
        if not Unit.query.filter_by(unit_name='L/min').first():
            db.session.add(Unit(unit_name='L/min'))
        db.session.commit()
        yield
        # Clean up any concepts created by tests so they don't bleed
        # across this session-scoped app fixture.
        Concept.query.delete()
        db.session.commit()


def _import_csv(path, **kwargs):
    with open(path, 'rb') as fh:
        rows = parse_csv(io.BytesIO(fh.read()))
    kwargs.setdefault('operator', 'test')
    kwargs.setdefault('filename', os.path.basename(path))
    kwargs.setdefault('sha256', 'fake-sha')
    return validate_and_import(rows, **kwargs)


def test_happy_path(app):
    """Sample fixture imports cleanly with all rows accepted."""
    with app.app_context():
        report = _import_csv(os.path.join(FIXTURE_DIR, 'concepts_sample.csv'))

        assert report['summary']['n_in'] == 3
        assert report['summary']['n_accepted'] == 3
        assert report['summary']['n_rejected'] == 0
        assert report['summary']['n_created'] == 3
        assert report['summary']['n_updated'] == 0
        assert set(report['accepted']) == {
            'peak-flow-am', 'peak-flow-pm', 'asthma-symptom-cough',
        }

        c = Concept.query.filter_by(concept_name='peak-flow-am').first()
        assert c.range_low == 100.0
        assert c.range_high == 800.0
        loinc = CanonicalLib.query.filter_by(canonical_lib_name='LOINC').first()
        assert c.canonical_lib == loinc.guid


def test_idempotent_reimport_updates_not_duplicates(app):
    """Re-running the same file updates in place (n_updated > 0, no dupes)."""
    with app.app_context():
        _import_csv(os.path.join(FIXTURE_DIR, 'concepts_sample.csv'))
        report = _import_csv(os.path.join(FIXTURE_DIR, 'concepts_sample.csv'))

        assert report['summary']['n_accepted'] == 3
        assert report['summary']['n_updated'] == 3
        assert report['summary']['n_created'] == 0
        # Exactly one row per concept_name (no auto-suffixing on re-import)
        for name in ('peak-flow-am', 'peak-flow-pm', 'asthma-symptom-cough'):
            assert Concept.query.filter_by(concept_name=name).count() == 1


def test_canonical_ref_change_is_conflict(app):
    """Changing canonical_ref on an existing concept is rejected."""
    with app.app_context():
        _import_csv(os.path.join(FIXTURE_DIR, 'concepts_sample.csv'))

        csv_text = (
            'concept_name,display_text,canonical_lib,canonical_ref,'
            'concept_type,response_type,unit,range_low,range_high\n'
            'peak-flow-am,Morning PEF,LOINC,99999-9,measurement,numeric,L/min,,\n'
        )
        rows = parse_csv(io.BytesIO(csv_text.encode('utf-8')))
        report = validate_and_import(
            rows, operator='test', filename='x.csv', sha256='x',
        )

        assert report['summary']['n_accepted'] == 0
        assert report['summary']['n_rejected'] == 1
        assert 'canonical_ref conflict' in report['rejected'][0]['reason']


def test_invalid_concept_name(app):
    """Non-lowercase-hyphen names are rejected with a clear reason."""
    with app.app_context():
        csv_text = (
            'concept_name,display_text,canonical_lib,canonical_ref,'
            'concept_type,response_type,unit,range_low,range_high\n'
            'Peak Flow,bad,LOINC,1,measurement,numeric,L/min,,\n'
        )
        rows = parse_csv(io.BytesIO(csv_text.encode('utf-8')))
        report = validate_and_import(
            rows, operator='test', filename='x.csv', sha256='x',
        )
        assert report['summary']['n_rejected'] == 1
        assert 'lowercase' in report['rejected'][0]['reason']


def test_missing_canonical_lib(app):
    """Rows referencing an unknown canonical_lib are rejected (FK guard)."""
    with app.app_context():
        csv_text = (
            'concept_name,display_text,canonical_lib,canonical_ref,'
            'concept_type,response_type,unit,range_low,range_high\n'
            'foo-bar,baz,NOT-A-LIB,1,measurement,numeric,L/min,,\n'
        )
        rows = parse_csv(io.BytesIO(csv_text.encode('utf-8')))
        report = validate_and_import(
            rows, operator='test', filename='x.csv', sha256='x',
        )
        assert report['summary']['n_rejected'] == 1
        assert 'canonical_lib not found' in report['rejected'][0]['reason']


def test_range_low_gt_high_rejected(app):
    """range_low > range_high is rejected before reaching the DB CHECK."""
    with app.app_context():
        csv_text = (
            'concept_name,display_text,canonical_lib,canonical_ref,'
            'concept_type,response_type,unit,range_low,range_high\n'
            'inverted,bad,LOINC,1,measurement,numeric,L/min,99,1\n'
        )
        rows = parse_csv(io.BytesIO(csv_text.encode('utf-8')))
        report = validate_and_import(
            rows, operator='test', filename='x.csv', sha256='x',
        )
        assert report['summary']['n_rejected'] == 1
        assert 'range_low' in report['rejected'][0]['reason']


def test_dry_run_does_not_persist(app):
    """dry_run=True returns a report but rolls back."""
    with app.app_context():
        Concept.query.filter_by(concept_name='peak-flow-am').delete()
        db.session.commit()

        report = _import_csv(
            os.path.join(FIXTURE_DIR, 'concepts_sample.csv'),
            dry_run=True,
        )
        assert report['summary']['n_accepted'] == 3
        assert report['summary']['dry_run'] is True
        assert Concept.query.filter_by(concept_name='peak-flow-am').first() is None


def test_missing_required_column(app):
    """A file missing a required header is rejected at parse time."""
    bad_csv = b'concept_name,display_text,canonical_lib\nfoo,bar,LOINC\n'
    with pytest.raises(ImportError_) as excinfo:
        parse_csv(io.BytesIO(bad_csv))
    assert 'Missing required column' in str(excinfo.value)
