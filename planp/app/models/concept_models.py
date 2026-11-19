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
    # UNIQUE since #875. It was not, and two libraries held the same URL:
    # `icd10` carried a copy of `snomed`'s, so `resolve_canonical_lib`'s
    # `.first()` on this column collapsed them and answered with `snomed` by
    # row order. The cost was measured — `$validate-code` said FALSE for 89
    # correctly-stored ICD-10 codes, and `_build_compose` served them under
    # the SNOMED CT system URI, which is wrong FHIR published outward.
    #
    # Nullable AND unique is deliberate: Postgres permits many NULLs under a
    # UNIQUE, so a library with no URL is not a collision, while two claiming
    # the same URL is. The write paths normalise '' to NULL for exactly this
    # reason — empty strings DO collide with each other, and "no URL" must
    # not become a conflict between two libraries that both lack one.
    canonical_lib_url = db.Column(db.String(500), unique=True, nullable=True)
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    # Is this library's answer space the ENTIRE code system?
    #
    # Default False, which is the behaviour every existing library has: a code
    # is adopted only if some Concept or ValueCatalog row references it, and
    # $validate-code answers per code. That is right for a measurement
    # vocabulary, where an unplanned code is meaningless.
    #
    # True says the opposite and is for a CLASSIFICATION: a diagnosis is chosen
    # from the whole of ICD-11 (~85 000 codes) at the point of care, so the
    # adopted set cannot be enumerated in advance and plan declares adoption at
    # SYSTEM granularity instead. This is not a loosening of the gate -- plan
    # still answers the question, and still says no for an unregistered library.
    #
    # It also completes the design in icd11.pdhc's plan §5.b, which specifies a
    # single system-bound Concept with no `valueset` because "its answer space is
    # an entire code system". Without this flag that Concept makes ICD-11
    # authorable in a PlanDefinition but leaves every actual code unadopted.
    whole_system_answer_space = db.Column(
        db.Boolean, nullable=False, server_default='false', default=False)
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
            'whole_system_answer_space': bool(self.whole_system_answer_space),
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
            'url': f"{PLAN_BASE}/api/v1/lookup/valuesets/{self.guid}",
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
    # RETIRED by #841; read by nothing. Concept.status was never an adoption
    # gate -- no route, CLI or template could move a Concept out of 'draft',
    # so all 99 rows held the column default and the FHIR surface that derived
    # from it (#839) could only ever report 'draft'. The column is KEPT rather
    # than dropped: it holds a single constant value, so there is no
    # information to lose either way, and keeping it avoids an irreversible
    # migration on the platform's semantic authority. It is deliberately not
    # in to_dict(), not writable through the API, and not advertised as a
    # CodeSystem property. Do not read it, and do not reinstate it without
    # answering #841's governance question first.
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

    # #951 D4: the import that CREATED this concept, if one did. NULL for every
    # concept made before #951 or by hand -- not knowing is not invented.
    import_guid = db.Column(db.String(36), db.ForeignKey('concept_imports.guid'), nullable=True)

    # Marked for deletion: a request, not a deletion. The term stays usable
    # until someone deletes it; NULL = not marked.
    marked_for_deletion_at = db.Column(db.DateTime, nullable=True)
    marked_for_deletion_by = db.Column(db.String(255), nullable=True)

    # #951 D1: MANY categories per concept (a diabetes-guideline term may also
    # belong to a cardiovascular one). Read through the link table.
    categories = db.relationship(
        'ConceptCategory', secondary='concept_category_links',
        primaryjoin='Concept.guid == ConceptCategoryLink.concept_guid',
        secondaryjoin='ConceptCategoryLink.category_guid == ConceptCategory.guid',
        lazy='selectin', viewonly=True, order_by='ConceptCategory.category_name')

    # Named subsets this concept is marked for (many per concept).
    subsets = db.relationship(
        'ConceptSubset', secondary='concept_subset_links',
        primaryjoin='Concept.guid == ConceptSubsetLink.concept_guid',
        secondaryjoin='ConceptSubsetLink.subset_guid == ConceptSubset.guid',
        lazy='selectin', viewonly=True, order_by='ConceptSubset.subset_name')

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
        # #294 RFC D3 (2026-06-28): emit both generic `guid` and
        # role-specific `concept_guid` during the transition. `guid`
        # will be dropped after one release cycle.
        d = {
            'guid': self.guid,
            'concept_guid': self.guid,
            'url': f"{PLAN_BASE}/api/v1/concepts/{self.guid}",
            'canonical_lib': self.canonical_lib,
            'canonical_refnumber': self.canonical_refnumber,
            'concept_name': self.concept_name,
            'concept_display_text': self.concept_display_text,
            'concept_explain': self.concept_explain,
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
            d['valueset_url'] = f"{PLAN_BASE}/api/v1/lookup/valuesets/{self.valueset}"
        if self.canonical_lib:
            d['canonical_lib_url'] = f"{PLAN_BASE}/api/v1/lookup/canonical-libs/{self.canonical_lib}"
        # #951: the categories, each with its url -- the concept_type_url pattern.
        d['categories'] = [
            {'guid': c.guid, 'category_name': c.category_name,
             'url': f"{PLAN_BASE}/api/v1/lookup/concept-categories/{c.guid}"}
            for c in self.categories]
        d['import_guid'] = self.import_guid
        if self.import_guid:
            d['import_url'] = f"{PLAN_BASE}/api/v1/concept-imports/{self.import_guid}"
        return d


# ---------------------------------------------------------------------------
# #951 -- categories and import provenance
# ---------------------------------------------------------------------------
# Two axes kept apart on purpose. `intended_uses` answers "what is this term
# FOR" and stays untouched (D3, operator 2026-11-06). A CATEGORY answers "where
# does this term belong / come from" (e.g. a guideline): a third axis beside
# `concept_type`, which is the KIND of term (measured live 2026-11-17:
# Observation 71, Diagnosis 19, Medication 9, Procedure 7; D2).

class ConceptCategory(db.Model):
    """One category. The standard lookup-table shape."""
    __tablename__ = 'concept_categories'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    category_name = db.Column(db.String(255), unique=True, nullable=False)
    category_display_text = db.Column(db.String(500), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_valid = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'guid': self.guid,
            'url': f"{PLAN_BASE}/api/v1/lookup/concept-categories/{self.guid}",
            'category_name': self.category_name,
            'category_display_text': self.category_display_text,
            'author': self.author,
            'vers_number': self.vers_number,
        }


class ConceptCategoryLink(db.Model):
    """Concept <-> category, MANY to MANY (D1). The `valueset_values` shape.

    `import_guid` says which import put the link there; NULL when a person
    did it by hand. The link is the editable half of D4; the import record
    below is the immutable half.
    """
    __tablename__ = 'concept_category_links'

    id = db.Column(db.Integer, primary_key=True)
    concept_guid = db.Column(db.String(36), db.ForeignKey('concepts.guid', ondelete='CASCADE'), nullable=False, index=True)
    category_guid = db.Column(db.String(36), db.ForeignKey('concept_categories.guid'), nullable=False, index=True)
    import_guid = db.Column(db.String(36), db.ForeignKey('concept_imports.guid'), nullable=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('concept_guid', 'category_guid', name='uq_concept_category'),
    )


class ConceptSubset(db.Model):
    """A NAMED SUBSET of concepts, e.g. the terms of one scenario or study.

    Not a category: a category says what a term IS (Condition, Symptom), a
    subset says which piece of work it was picked for. Many per concept, and
    an operator makes one simply by naming it while marking terms.
    """
    __tablename__ = 'concept_subsets'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    subset_name = db.Column(db.String(255), unique=True, nullable=False)
    author = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class ConceptSubsetLink(db.Model):
    __tablename__ = 'concept_subset_links'

    id = db.Column(db.Integer, primary_key=True)
    concept_guid = db.Column(db.String(36), db.ForeignKey('concepts.guid', ondelete='CASCADE'), nullable=False, index=True)
    subset_guid = db.Column(db.String(36), db.ForeignKey('concept_subsets.guid', ondelete='CASCADE'), nullable=False, index=True)
    author = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('concept_guid', 'subset_guid', name='uq_concept_subset'),
    )


class ConceptImportImmutable(RuntimeError):
    """An import record is a fact about the past; it is never edited."""


class ConceptImport(db.Model):
    """One REAL (non-dry-run) run of the concept importer (#951 stage C).

    Persists what `validate_and_import` always computed and then threw away:
    who, which file (name + sha256), the counts, the categories applied. With
    `Concept.import_guid` and `ConceptCategoryLink.import_guid` it answers
    "exactly what did the 2026 diabetes-guideline file produce", which an
    editable category on the concept alone cannot (D4).
    """
    __tablename__ = 'concept_imports'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    operator = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(500), nullable=True)
    sha256 = db.Column(db.String(64), nullable=True)
    entry_point = db.Column(db.String(16), nullable=False)   # cli / api / web
    #: The batch default category names, '; '-joined; NULL when none was given.
    default_categories = db.Column(db.Text, nullable=True)
    n_in = db.Column(db.Integer, nullable=False)
    n_created = db.Column(db.Integer, nullable=False)
    n_updated = db.Column(db.Integer, nullable=False)
    n_unchanged = db.Column(db.Integer, nullable=False)
    n_rejected = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'guid': self.guid,
            'url': f"{PLAN_BASE}/api/v1/concept-imports/{self.guid}",
            'operator': self.operator, 'filename': self.filename, 'sha256': self.sha256,
            'entry_point': self.entry_point,
            'default_categories': self.default_categories.split('; ') if self.default_categories else [],
            'n_in': self.n_in, 'n_created': self.n_created, 'n_updated': self.n_updated,
            'n_unchanged': self.n_unchanged, 'n_rejected': self.n_rejected,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


@db.event.listens_for(ConceptImport, 'before_update', propagate=True)
def _import_record_is_immutable(mapper, connection, target):
    raise ConceptImportImmutable(f'concept import {target.guid} may not be modified')
