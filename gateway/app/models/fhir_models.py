import uuid
from datetime import datetime, timezone
from app import db


class PlanDefinition(db.Model):
    __tablename__ = 'plan_definitions'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    fhir_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    # Metadata
    name = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='draft')
    type = db.Column(db.String(100), nullable=True)
    version = db.Column(db.String(50), default='1.0.0')
    subject_type = db.Column(db.String(100), default='Patient')

    # Descriptive
    publisher = db.Column(db.String(255), nullable=True)
    purpose = db.Column(db.Text, nullable=True)
    usage = db.Column(db.Text, nullable=True)
    copyright = db.Column(db.Text, nullable=True)

    # Contributors
    author = db.Column(db.String(500), nullable=True)
    editor = db.Column(db.String(500), nullable=True)
    reviewer = db.Column(db.String(500), nullable=True)
    endorser = db.Column(db.String(500), nullable=True)

    # Timing
    approval_date = db.Column(db.Date, nullable=True)
    last_review_date = db.Column(db.Date, nullable=True)
    effective_period_start = db.Column(db.Date, nullable=True)
    effective_period_end = db.Column(db.Date, nullable=True)
    validity_duration = db.Column(db.String(50), nullable=True)

    # Related
    related_artifact = db.Column(db.Text, nullable=True)
    library = db.Column(db.String(500), nullable=True)

    # Builder JSON (backward compatibility)
    goal = db.Column(db.Text, nullable=True)
    action = db.Column(db.Text, nullable=True)

    # Canonical FHIR representation
    fhir_data = db.Column(db.JSON, nullable=True)

    # Timestamps
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                             onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    goals = db.relationship('PlanDefinitionGoal', backref='plan_definition',
                            lazy='dynamic', foreign_keys='PlanDefinitionGoal.plandefinition_guid',
                            primaryjoin='PlanDefinition.guid == PlanDefinitionGoal.plandefinition_guid')
    activity_links = db.relationship('PlanDefinitionActivity', backref='plan_definition',
                                     lazy='dynamic',
                                     foreign_keys='PlanDefinitionActivity.plandefinition_guid',
                                     primaryjoin='PlanDefinition.guid == PlanDefinitionActivity.plandefinition_guid')

    def to_dict(self):
        return {
            'guid': self.guid,
            'fhir_id': self.fhir_id,
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'type': self.type,
            'version': self.version,
            'subject_type': self.subject_type,
            'publisher': self.publisher,
            'author': self.author,
            'date_created': self.date_created.isoformat() if self.date_created else None,
        }
