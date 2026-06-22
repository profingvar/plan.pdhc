import uuid
from datetime import datetime, timezone
from app import db

PLAN_BASE = "https://plan.pdhc.se"


# ---------------------------------------------------------------------------
# FHIR canonical URL + version helpers (ADR D3, D4)
# ---------------------------------------------------------------------------
# Single source of truth for FHIR canonical URLs emitted by the
# terminology profile (ValueSet / CodeSystem / ConceptMap). The canonical
# URL is a FHIR identifier and is not required to resolve — routes
# remain under /api/v1/ for backward compatibility.
#
# DO NOT hardcode the "/fhir/" scheme anywhere else: import these
# helpers. ADR Risk §9.3 + the lint test in tests/test_fhir_helpers.py
# enforce this.

LOCAL_CODESYSTEM_ID = "plan-pdhc-local"
LOCAL_CONCEPTMAP_ID = "plan-pdhc-canonical-bindings"


def fhir_canonical_url(resource: str, resource_id: str) -> str:
    """Build the FHIR canonical url for a terminology resource.

    Form: {PLAN_BASE}/fhir/{Resource}/{id}  (per ADR D3)
    Example: https://plan.pdhc.se/fhir/CodeSystem/plan-pdhc-local
    """
    return f"{PLAN_BASE}/fhir/{resource}/{resource_id}"


def fhir_version(model_obj) -> str:
    """FHIR `version` field derivation (per ADR D4).

    Reads `vers_number` (integer) off the model and returns str(n).
    Defaults to "1" if the attribute is missing or None.
    """
    n = getattr(model_obj, 'vers_number', None) or 1
    return str(n)


# ---------------------------------------------------------------------------
# Lookup tables
# ---------------------------------------------------------------------------

class CanonicalLib(db.Model):
    __tablename__ = 'canonical_libs'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    canonical_lib_name = db.Column(db.String(255), unique=True, nullable=False)
    canonical_lib_display_text = db.Column(db.String(500), nullable=True)
    canonical_lib_url = db.Column(db.String(500), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_valid = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'guid': self.guid,
            'canonical_lib_name': self.canonical_lib_name,
            'canonical_lib_display_text': self.canonical_lib_display_text,
            'canonical_lib_url': self.canonical_lib_url,
            'author': self.author,
            'vers_number': self.vers_number,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_valid': self.date_valid.isoformat() if self.date_valid else None,
        }


class ConceptType(db.Model):
    __tablename__ = 'concept_types'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    concept_type_name = db.Column(db.String(255), unique=True, nullable=False)
    concept_type_display_text = db.Column(db.String(500), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_valid = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'guid': self.guid,
            'concept_type_name': self.concept_type_name,
            'concept_type_display_text': self.concept_type_display_text,
            'author': self.author,
            'vers_number': self.vers_number,
        }


class ResponseType(db.Model):
    __tablename__ = 'response_types'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    response_type_name = db.Column(db.String(255), unique=True, nullable=False)
    response_type_display_text = db.Column(db.String(500), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_valid = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'guid': self.guid,
            'response_type_name': self.response_type_name,
            'response_type_display_text': self.response_type_display_text,
            'author': self.author,
            'vers_number': self.vers_number,
        }


class Unit(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    unit_name = db.Column(db.String(255), unique=True, nullable=False)
    unit_display_text = db.Column(db.String(500), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_valid = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'guid': self.guid,
            'unit_name': self.unit_name,
            'unit_display_text': self.unit_display_text,
            'author': self.author,
            'vers_number': self.vers_number,
        }


class PlanDefType(db.Model):
    __tablename__ = 'plandef_types'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    plandef_type_name = db.Column(db.String(255), unique=True, nullable=False)
    plandef_type_display_text = db.Column(db.String(500), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_valid = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'guid': self.guid,
            'plandef_type_name': self.plandef_type_name,
            'plandef_type_display_text': self.plandef_type_display_text,
            'author': self.author,
            'vers_number': self.vers_number,
        }


class IntendedUse(db.Model):
    __tablename__ = 'intended_uses'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    intended_use_name = db.Column(db.String(255), unique=True, nullable=False)
    intended_use_display_text = db.Column(db.String(500), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_valid = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'guid': self.guid,
            'intended_use_name': self.intended_use_name,
            'intended_use_display_text': self.intended_use_display_text,
            'author': self.author,
            'vers_number': self.vers_number,
        }


# ---------------------------------------------------------------------------
# Values and ValueSets
# ---------------------------------------------------------------------------

class ValueCatalog(db.Model):
    __tablename__ = 'values_catalog'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    canonical_lib = db.Column(db.String(36), db.ForeignKey('canonical_libs.guid'), nullable=False)
    canonical_refnumber = db.Column(db.String(255), nullable=True)
    value_name = db.Column(db.String(255), nullable=False)
    value_display_text = db.Column(db.String(500), nullable=True)
    value_explanation = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_valid = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    canonical_lib_rel = db.relationship('CanonicalLib', foreign_keys=[canonical_lib],
                                         primaryjoin='ValueCatalog.canonical_lib == CanonicalLib.guid')

    def to_dict(self):
        d = {
            'guid': self.guid,
            'url': f"{PLAN_BASE}/api/v1/lookup/values/{self.guid}",
            'canonical_lib': self.canonical_lib,
            'canonical_refnumber': self.canonical_refnumber,
            'value_name': self.value_name,
            'value_display_text': self.value_display_text,
            'value_explanation': self.value_explanation,
            'author': self.author,
            'vers_number': self.vers_number,
            'date_created': self.date_created.isoformat() if self.date_created else None,
        }
        if self.canonical_lib:
            d['canonical_lib_url'] = f"{PLAN_BASE}/api/v1/lookup/canonical-libs/{self.canonical_lib}"
        return d


class ValueSet(db.Model):
    __tablename__ = 'valuesets'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    canonical_lib = db.Column(db.String(36), db.ForeignKey('canonical_libs.guid'), nullable=False)
    canonical_refnumber = db.Column(db.String(255), nullable=True)
    valueset_name = db.Column(db.String(255), unique=True, nullable=False)
    valueset_display_text = db.Column(db.String(500), nullable=True)
    valueset_explanation = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_valid = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    canonical_lib_rel = db.relationship('CanonicalLib', foreign_keys=[canonical_lib],
                                         primaryjoin='ValueSet.canonical_lib == CanonicalLib.guid')
    values = db.relationship('ValueSetValue', backref='valueset_rel', lazy='dynamic')

    def to_dict(self, include_values=True):
        d = {
            'guid': self.guid,
            'url': f"{PLAN_BASE}/api/v1/valuesets/{self.guid}",
            'canonical_lib': self.canonical_lib,
            'canonical_refnumber': self.canonical_refnumber,
            'valueset_name': self.valueset_name,
            'valueset_display_text': self.valueset_display_text,
            'valueset_explanation': self.valueset_explanation,
            'author': self.author,
            'vers_number': self.vers_number,
            'date_created': self.date_created.isoformat() if self.date_created else None,
        }
        if self.canonical_lib:
            d['canonical_lib_url'] = f"{PLAN_BASE}/api/v1/lookup/canonical-libs/{self.canonical_lib}"
        if include_values:
            links = ValueSetValue.query.filter_by(
                valueset_guid=self.guid
            ).order_by(ValueSetValue.sort_order).all()
            values = []
            for link in links:
                val = ValueCatalog.query.filter_by(guid=link.value_guid).first()
                if val:
                    v = val.to_dict()
                    v['sort_order'] = link.sort_order
                    values.append(v)
            d['values'] = values
        return d


class ValueSetValue(db.Model):
    __tablename__ = 'valueset_values'

    id = db.Column(db.Integer, primary_key=True)
    valueset_guid = db.Column(db.String(36), db.ForeignKey('valuesets.guid'), nullable=False)
    value_guid = db.Column(db.String(36), db.ForeignKey('values_catalog.guid'), nullable=False)
    sort_order = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('valueset_guid', 'value_guid', name='uq_valueset_value'),
    )

    value_rel = db.relationship('ValueCatalog', foreign_keys=[value_guid],
                                 primaryjoin='ValueSetValue.value_guid == ValueCatalog.guid')

    def to_dict(self):
        return {
            'valueset_guid': self.valueset_guid,
            'value_guid': self.value_guid,
            'sort_order': self.sort_order,
        }


# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    canonical_lib = db.Column(db.String(36), db.ForeignKey('canonical_libs.guid'), nullable=False)
    canonical_refnumber = db.Column(db.String(255), nullable=True)
    concept_name = db.Column(db.String(255), nullable=False)
    concept_display_text = db.Column(db.String(500), nullable=True)
    concept_explain = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='draft')

    concept_type = db.Column(db.String(36), db.ForeignKey('concept_types.guid'), nullable=True)
    response_type = db.Column(db.String(36), db.ForeignKey('response_types.guid'), nullable=True)
    unit = db.Column(db.String(36), db.ForeignKey('units.guid'), nullable=True)

    range_low = db.Column(db.Float, nullable=True)
    range_high = db.Column(db.Float, nullable=True)
    anchor_low_text = db.Column(db.String(255), nullable=True)
    anchor_high_text = db.Column(db.String(255), nullable=True)

    valueset = db.Column(db.String(36), db.ForeignKey('valuesets.guid'), nullable=True)
    no_of_values_connected = db.Column(db.Integer, default=0)

    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_valid = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.CheckConstraint(
            '(range_low IS NULL OR range_high IS NULL OR range_low <= range_high)',
            name='ck_concept_range'
        ),
    )

    canonical_lib_rel = db.relationship('CanonicalLib', foreign_keys=[canonical_lib],
                                         primaryjoin='Concept.canonical_lib == CanonicalLib.guid')
    concept_type_rel = db.relationship('ConceptType', foreign_keys=[concept_type],
                                        primaryjoin='Concept.concept_type == ConceptType.guid')
    response_type_rel = db.relationship('ResponseType', foreign_keys=[response_type],
                                         primaryjoin='Concept.response_type == ResponseType.guid')
    unit_rel = db.relationship('Unit', foreign_keys=[unit],
                                primaryjoin='Concept.unit == Unit.guid')
    valueset_rel = db.relationship('ValueSet', foreign_keys=[valueset],
                                    primaryjoin='Concept.valueset == ValueSet.guid')

    def to_dict(self):
        d = {
            'guid': self.guid,
            'url': f"{PLAN_BASE}/api/v1/concepts/{self.guid}",
            'canonical_lib': self.canonical_lib,
            'canonical_refnumber': self.canonical_refnumber,
            'concept_name': self.concept_name,
            'concept_display_text': self.concept_display_text,
            'concept_explain': self.concept_explain,
            'status': self.status,
            'concept_type': self.concept_type,
            'response_type': self.response_type,
            'unit': self.unit,
            'range_low': self.range_low,
            'range_high': self.range_high,
            'anchor_low_text': self.anchor_low_text,
            'anchor_high_text': self.anchor_high_text,
            'valueset': self.valueset,
            'no_of_values_connected': self.no_of_values_connected,
            'author': self.author,
            'vers_number': self.vers_number,
            'date_created': self.date_created.isoformat() if self.date_created else None,
        }
        if self.concept_type:
            d['concept_type_url'] = f"{PLAN_BASE}/api/v1/lookup/concept-types/{self.concept_type}"
        if self.response_type:
            d['response_type_url'] = f"{PLAN_BASE}/api/v1/lookup/response-types/{self.response_type}"
        if self.unit:
            d['unit_url'] = f"{PLAN_BASE}/api/v1/lookup/units/{self.unit}"
        if self.valueset:
            d['valueset_url'] = f"{PLAN_BASE}/api/v1/valuesets/{self.valueset}"
        if self.canonical_lib:
            d['canonical_lib_url'] = f"{PLAN_BASE}/api/v1/lookup/canonical-libs/{self.canonical_lib}"
        return d
