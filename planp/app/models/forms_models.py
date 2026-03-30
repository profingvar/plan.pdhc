"""Forms models — FHIR Questionnaire production, versioning, and responses."""
import uuid
from datetime import datetime, timezone
from app import db


class Questionnaire(db.Model):
    __tablename__ = 'questionnaires'

    id = db.Column(db.Integer, primary_key=True)
    form_guid = db.Column(db.String(36), nullable=False, index=True)
    version = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='draft')
    fhir_json = db.Column(db.JSON, nullable=False)
    content_fingerprint = db.Column(db.String(64), nullable=True, index=True)
    production_key = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
    created_by = db.Column(db.String(255), nullable=True)
    archived = db.Column(db.Boolean, default=False, nullable=False, server_default='0')

    items = db.relationship('QuestionnaireItem', backref='questionnaire', cascade='all, delete-orphan')

    __table_args__ = (
        db.UniqueConstraint('form_guid', 'version', name='uq_form_guid_version'),
    )

    @staticmethod
    def generate_guid():
        return str(uuid.uuid4())

    def to_dict(self):
        return {
            'form_guid': self.form_guid,
            'version': self.version,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'fhir_json': self.fhir_json,
            'content_fingerprint': self.content_fingerprint,
            'production_key': self.production_key,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
        }

    def to_summary(self):
        return {
            'form_guid': self.form_guid,
            'latest_version': self.version,
            'title': self.title,
            'status': self.status,
            'description': self.description,
        }


class QuestionnaireItem(db.Model):
    __tablename__ = 'questionnaire_items'

    id = db.Column(db.Integer, primary_key=True)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaires.id'), nullable=False)
    form_guid = db.Column(db.String(36), nullable=False, index=True)
    form_version = db.Column(db.Integer, nullable=False)
    link_id = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    required = db.Column(db.Boolean, default=False)
    options = db.Column(db.JSON, nullable=True)
    min_value = db.Column(db.Float, nullable=True)
    max_value = db.Column(db.Float, nullable=True)
    default_value = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            'link_id': self.link_id,
            'text': self.text,
            'type': self.type,
            'required': self.required,
            'options': self.options,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'default_value': self.default_value,
        }


class QuestionnaireResponse(db.Model):
    __tablename__ = 'questionnaire_responses'

    id = db.Column(db.Integer, primary_key=True)
    response_guid = db.Column(db.String(36), nullable=False, unique=True,
                              default=lambda: str(uuid.uuid4()))
    form_guid = db.Column(db.String(36), nullable=False, index=True)
    form_version = db.Column(db.Integer, nullable=False)
    patient_guid = db.Column(db.String(36), nullable=False, index=True)
    fhir_json = db.Column(db.JSON, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'response_guid': self.response_guid,
            'form_guid': self.form_guid,
            'form_version': self.form_version,
            'patient_guid': self.patient_guid,
            'fhir_json': self.fhir_json,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
        }


class FormDefinition(db.Model):
    """Authored form blueprint — the intermediate layer between concepts and FHIR Questionnaires."""
    __tablename__ = 'form_definitions'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, index=True,
                     default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='draft')
    author = db.Column(db.String(255), nullable=True)
    vers_number = db.Column(db.Integer, nullable=False, default=1)
    produced_form_guid = db.Column(db.String(36), nullable=True)
    production_key = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    date_updated = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
                             onupdate=lambda: datetime.now(timezone.utc))
    archived = db.Column(db.Boolean, default=False, nullable=False, server_default='0')

    items = db.relationship('FormDefinitionItem', backref='form_definition',
                            cascade='all, delete-orphan',
                            order_by='FormDefinitionItem.sort_order')

    def to_dict(self, include_items=False):
        d = {
            'guid': self.guid,
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'author': self.author,
            'vers_number': self.vers_number,
            'produced_form_guid': self.produced_form_guid,
            'production_key': self.production_key,
            'item_count': len(self.items) if self.items else 0,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None,
        }
        if include_items:
            d['items'] = [item.to_dict() for item in self.items]
        return d

    def to_summary(self):
        return {
            'guid': self.guid,
            'name': self.name,
            'title': self.title,
            'status': self.status,
            'item_count': len(self.items) if self.items else 0,
            'produced_form_guid': self.produced_form_guid,
        }


class FormDefinitionItem(db.Model):
    """A single concept reference within a FormDefinition, with per-item overrides."""
    __tablename__ = 'form_definition_items'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False,
                     default=lambda: str(uuid.uuid4()))
    form_definition_guid = db.Column(db.String(36), db.ForeignKey('form_definitions.guid'),
                                     nullable=False, index=True)
    concept_guid = db.Column(db.String(36), nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    display_text_override = db.Column(db.String(500), nullable=True)
    required = db.Column(db.Boolean, nullable=False, default=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    item_type_override = db.Column(db.String(50), nullable=True)
    group_label = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('form_definition_guid', 'concept_guid',
                            name='uq_formdef_concept'),
    )

    def to_dict(self):
        return {
            'guid': self.guid,
            'form_definition_guid': self.form_definition_guid,
            'concept_guid': self.concept_guid,
            'sort_order': self.sort_order,
            'display_text_override': self.display_text_override,
            'required': self.required,
            'enabled': self.enabled,
            'item_type_override': self.item_type_override,
            'group_label': self.group_label,
            'notes': self.notes,
            'date_created': self.date_created.isoformat() if self.date_created else None,
        }
