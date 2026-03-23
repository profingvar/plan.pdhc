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
