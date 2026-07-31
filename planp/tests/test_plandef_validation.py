"""GA-1 — deterministic PlanDef/Concept validation invariants (epic #516)."""
import pytest

from app import db
from app.models.concept_models import (
    CanonicalLib, Concept, ResponseType, Unit, ValueSet,
)
from app.services import plandef_validation as v


def _goc(model, name_field, name, **extra):
    """get-or-create a lookup row by its unique name (session-scoped DB)."""
    row = model.query.filter(getattr(model, name_field).ilike(name)).first()
    if row:
        return row
    row = model(**{name_field: name}, **extra)
    db.session.add(row)
    db.session.commit()
    return row


@pytest.fixture
def seed(app):
    with app.app_context():
        lib = _goc(CanonicalLib, 'canonical_lib_name', 'LOINC-GA')
        data = {
            'lib': lib.guid,
            'rt_qty': _goc(ResponseType, 'response_type_name', 'Quantity').guid,
            'rt_choice': _goc(ResponseType, 'response_type_name', 'Single Choice').guid,
            'rt_text': _goc(ResponseType, 'response_type_name', 'Text').guid,
            'rt_zorp': _goc(ResponseType, 'response_type_name', 'Zorp').guid,
            # names that exist in PROD but aren't in forms_service.RESPONSE_TYPE_MAP
            'rt_numerical': _goc(ResponseType, 'response_type_name', 'numerical').guid,
            'rt_freetext': _goc(ResponseType, 'response_type_name', 'Free text').guid,
            'rt_slider': _goc(ResponseType, 'response_type_name', 'Slider').guid,
            'unit': _goc(Unit, 'unit_name', 'mmHg').guid,
            'vs': _goc(ValueSet, 'valueset_name', 'yesno', canonical_lib=lib.guid).guid,
        }
        yield data


class _FakeTermbankMiss:
    def lookup(self, system, code):
        return None

    def search(self, q, limit=20):
        return {"results": []}


class _FakeTermbankHit:
    def lookup(self, system, code):
        return {"resourceType": "Parameters"}

    def search(self, q, limit=20):
        return {"results": []}


def _codes(issues):
    return {i.code for i in issues}


def test_quantity_without_unit_is_error(app, seed):
    with app.app_context():
        issues = v.validate_concept({
            'response_type': seed['rt_qty'],
            'canonical_lib': seed['lib'],
            'canonical_refnumber': '8480-6',
        })
    assert 'E-UNIT-REQUIRED' in _codes(issues)


def test_quantity_with_unit_has_no_unit_error(app, seed):
    with app.app_context():
        issues = v.validate_concept({
            'response_type': seed['rt_qty'],
            'unit': seed['unit'],
            'canonical_lib': seed['lib'],
            'canonical_refnumber': '8480-6',
        })
    assert 'E-UNIT-REQUIRED' not in _codes(issues)
    assert v.summarise(issues)['ok'] is True


def test_choice_without_valueset_is_error_even_via_api_path(app, seed):
    # This is the API-bypass case the web route half-catches.
    with app.app_context():
        issues = v.validate_concept({
            'response_type': seed['rt_choice'],
            'canonical_lib': seed['lib'],
            'canonical_refnumber': 'LA33-6',
        })
    assert 'E-VALUESET-REQUIRED' in _codes(issues)


def test_unknown_response_type_is_error(app, seed):
    with app.app_context():
        issues = v.validate_concept({
            'response_type': seed['rt_zorp'],
            'canonical_lib': seed['lib'],
            'canonical_refnumber': 'x',
        })
    assert 'E-RESPONSE-TYPE-UNKNOWN' in _codes(issues)


def test_prod_numerical_alias_is_recognised_and_needs_unit(app, seed):
    # 'numerical' is a real prod response type absent from RESPONSE_TYPE_MAP;
    # the validator must recognise it (no UNKNOWN) and treat it as a quantity.
    with app.app_context():
        no_unit = _codes(v.validate_concept({
            'response_type': seed['rt_numerical'],
            'canonical_lib': seed['lib'], 'canonical_refnumber': '8480-6',
        }))
        with_unit = _codes(v.validate_concept({
            'response_type': seed['rt_numerical'], 'unit': seed['unit'],
            'canonical_lib': seed['lib'], 'canonical_refnumber': '8480-6',
        }))
    assert 'E-RESPONSE-TYPE-UNKNOWN' not in no_unit
    assert 'E-UNIT-REQUIRED' in no_unit
    assert 'E-UNIT-REQUIRED' not in with_unit


def test_prod_free_text_alias_is_recognised_no_unit_needed(app, seed):
    with app.app_context():
        codes = _codes(v.validate_concept({
            'response_type': seed['rt_freetext'],
            'canonical_lib': seed['lib'], 'canonical_refnumber': 'note',
        }))
    assert 'E-RESPONSE-TYPE-UNKNOWN' not in codes
    assert 'E-UNIT-REQUIRED' not in codes
    assert 'E-VALUESET-REQUIRED' not in codes


def test_slider_does_not_require_a_unit(app, seed):
    # a 0-10 slider is dimensionless — requiring a unit would be a false positive
    with app.app_context():
        codes = _codes(v.validate_concept({
            'response_type': seed['rt_slider'],
            'canonical_lib': seed['lib'], 'canonical_refnumber': 'scale',
        }))
    assert 'E-UNIT-REQUIRED' not in codes
    assert 'E-RESPONSE-TYPE-UNKNOWN' not in codes


def test_missing_response_type_is_error(app, seed):
    with app.app_context():
        issues = v.validate_concept({'canonical_refnumber': 'x'})
    assert 'E-RESPONSE-TYPE-UNKNOWN' in _codes(issues)


def test_missing_terminology_binding_is_error(app, seed):
    with app.app_context():
        issues = v.validate_concept({
            'response_type': seed['rt_qty'],
            'unit': seed['unit'],
            'canonical_lib': seed['lib'],
        })
    assert 'E-TERM-MISSING' in _codes(issues)


def test_inverted_range_is_error(app, seed):
    with app.app_context():
        issues = v.validate_concept({
            'response_type': seed['rt_qty'], 'unit': seed['unit'],
            'canonical_lib': seed['lib'], 'canonical_refnumber': '8480-6',
            'range_low': 250, 'range_high': 60,
        })
    assert 'E-RANGE-INVERTED' in _codes(issues)


def test_dangling_unit_reference_is_error(app, seed):
    with app.app_context():
        issues = v.validate_concept({
            'response_type': seed['rt_qty'],
            'unit': '00000000-0000-0000-0000-000000000000',
            'canonical_lib': seed['lib'], 'canonical_refnumber': '8480-6',
        })
    assert 'E-DANGLING-REF' in _codes(issues)


def test_termbank_unverified_is_warning_only(app, seed):
    with app.app_context():
        issues = v.validate_concept(
            {
                'response_type': seed['rt_qty'], 'unit': seed['unit'],
                'canonical_lib': seed['lib'], 'canonical_refnumber': '9999-9',
            },
            termbank=_FakeTermbankMiss(),
        )
    codes = _codes(issues)
    assert 'W-TERM-UNVERIFIED' in codes
    # a warning must not flip ok=False
    assert v.summarise(issues)['error_count'] == 0


def test_termbank_hit_produces_no_terminology_warning(app, seed):
    with app.app_context():
        issues = v.validate_concept(
            {
                'response_type': seed['rt_qty'], 'unit': seed['unit'],
                'canonical_lib': seed['lib'], 'canonical_refnumber': '8480-6',
            },
            termbank=_FakeTermbankHit(),
        )
    assert 'W-TERM-UNVERIFIED' not in _codes(issues)


def test_no_termbank_keeps_core_deterministic(app, seed):
    # Without a termbank client the terminology-existence check is skipped
    # (no network) — a valid quantity has zero errors.
    with app.app_context():
        issues = v.validate_concept({
            'response_type': seed['rt_qty'], 'unit': seed['unit'],
            'canonical_lib': seed['lib'], 'canonical_refnumber': '8480-6',
        })
    assert v.summarise(issues)['ok'] is True


# --- plandef-level -------------------------------------------------------
def test_empty_plandef_warns(app):
    with app.app_context():
        issues = v.validate_plandef({})
    assert 'W-EMPTY-PLANDEF' in _codes(issues)


def test_plandef_dangling_concept_ref_is_error(app):
    with app.app_context():
        issues = v.validate_plandef({
            'transactions': [{'concept_guid': 'not-a-real-guid'}],
        })
    assert 'E-DANGLING-REF' in _codes(issues)


def test_plandef_unit_contradiction_warns(app, seed):
    with app.app_context():
        c = Concept(
            concept_name='bp-systolic-test', canonical_lib=seed['lib'],
            canonical_refnumber='8480-6', response_type=seed['rt_qty'],
            unit=seed['unit'],
        )
        db.session.add(c)
        db.session.commit()
        issues = v.validate_plandef({
            'goals': [{'concept_guid': c.guid, 'target_unit': 'kPa'}],
        })
    assert 'W-UNIT-CONTRADICTS' in _codes(issues)
