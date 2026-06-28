import uuid
from datetime import datetime, timezone
from app import db

PLAN_BASE = "https://plan.pdhc.se"


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    performer_type = db.Column(db.String(100), nullable=True)
    subject_type = db.Column(db.String(100), nullable=True)

    # Timing
    timing_type = db.Column(db.String(20), nullable=True)  # 'once' or 'repeat'
    timing_frequency = db.Column(db.Integer, nullable=True)
    timing_period = db.Column(db.Float, nullable=True)
    timing_period_unit = db.Column(db.String(10), nullable=True)  # d, wk, mo
    timing_duration = db.Column(db.Float, nullable=True)
    timing_duration_unit = db.Column(db.String(10), nullable=True)

    # Bounded recurrence — NULL means unbounded (backward compatible).
    # mode='count' → bounds_count holds total occurrences (Timing.repeat.count)
    # mode='duration' → bounds_duration_* hold the window (Timing.repeat.boundsDuration)
    timing_bounds_mode = db.Column(db.String(20), nullable=True)
    timing_bounds_count = db.Column(db.Integer, nullable=True)
    timing_bounds_duration_value = db.Column(db.Float, nullable=True)
    timing_bounds_duration_unit = db.Column(db.String(10), nullable=True)

    notes = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                             onupdate=lambda: datetime.now(timezone.utc))

    transactions = db.relationship('Transaction', backref='activity', lazy='dynamic',
                                   foreign_keys='Transaction.activity_guid',
                                   primaryjoin='Activity.guid == Transaction.activity_guid')

    def to_dict(self):
        # #294 RFC D3 (2026-06-28): emit both generic `guid` and
        # role-specific `activity_guid`. Activity is the parent of
        # Transaction; the activity_guid name keeps consumers
        # unambiguous when joining PlanDefinition snapshots.
        return {
            'guid': self.guid,
            'activity_guid': self.guid,
            'title': self.title,
            'description': self.description,
            'performer_type': self.performer_type,
            'subject_type': self.subject_type,
            'timing_type': self.timing_type,
            'timing_frequency': self.timing_frequency,
            'timing_period': self.timing_period,
            'timing_period_unit': self.timing_period_unit,
            'duration_value': self.timing_duration,
            'duration_unit': self.timing_duration_unit,
            'timing_bounds_mode': self.timing_bounds_mode,
            'timing_bounds_count': self.timing_bounds_count,
            'timing_bounds_duration_value': self.timing_bounds_duration_value,
            'timing_bounds_duration_unit': self.timing_bounds_duration_unit,
            'notes': self.notes,
        }


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    activity_guid = db.Column(db.String(36), db.ForeignKey('activities.guid'), nullable=False)
    concept_guid = db.Column(db.String(36), db.ForeignKey('concepts.guid'), nullable=True)

    expected_value = db.Column(db.String(500), nullable=True)
    unit = db.Column(db.String(100), nullable=True)
    range_min = db.Column(db.Float, nullable=True)
    range_max = db.Column(db.Float, nullable=True)
    requirement_type = db.Column(db.String(50), nullable=True)  # required, recommended

    sort_order = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        # #294 RFC D3 (2026-06-28): emit both generic `guid` and
        # role-specific `transaction_guid` during the transition.
        # `guid` will be dropped after one release cycle.
        d = {
            'guid': self.guid,
            'transaction_guid': self.guid,
            'url': f"{PLAN_BASE}/api/v1/transactions/{self.guid}",
            'activity_guid': self.activity_guid,
            'concept_guid': self.concept_guid,
            'expected_value': self.expected_value,
            'unit': self.unit,
            'range_min': self.range_min,
            'range_max': self.range_max,
            'requirement_type': self.requirement_type,
            'sort_order': self.sort_order,
        }
        if self.concept_guid:
            d['concept_url'] = f"{PLAN_BASE}/api/v1/concepts/{self.concept_guid}"
        return d


class PlanDefinitionGoal(db.Model):
    __tablename__ = 'plandefinition_goals'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    plandefinition_guid = db.Column(db.String(36), db.ForeignKey('plan_definitions.guid'), nullable=False)
    concept_guid = db.Column(db.String(36), db.ForeignKey('concepts.guid'), nullable=True)
    concept_name = db.Column(db.String(255), nullable=True)
    priority = db.Column(db.String(50), nullable=True)

    # Target
    target_type = db.Column(db.String(50), nullable=True)  # quantity, range, categorical
    target_quantity = db.Column(db.Float, nullable=True)
    target_operator = db.Column(db.String(10), nullable=True)  # >=, <=, =, etc.
    target_range_low = db.Column(db.Float, nullable=True)
    target_range_high = db.Column(db.Float, nullable=True)
    target_categorical_text = db.Column(db.String(500), nullable=True)
    target_value_guid = db.Column(db.String(36), nullable=True)
    target_unit = db.Column(db.String(100), nullable=True)

    sort_order = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        # #294 RFC D3: emit both generic `guid` and role-specific
        # `goal_guid` during the transition.
        d = {
            'guid': self.guid,
            'goal_guid': self.guid,
            'plandefinition_guid': self.plandefinition_guid,
            'concept_guid': self.concept_guid,
            'concept_name': self.concept_name,
            'priority': self.priority,
            'target_type': self.target_type,
            'target_quantity': self.target_quantity,
            'target_operator': self.target_operator,
            'target_range_low': self.target_range_low,
            'target_range_high': self.target_range_high,
            'target_categorical_text': self.target_categorical_text,
            'target_value_guid': self.target_value_guid,
            'target_unit': self.target_unit,
            'sort_order': self.sort_order,
        }
        if self.concept_guid:
            d['concept_url'] = f"{PLAN_BASE}/api/v1/concepts/{self.concept_guid}"
        if self.target_value_guid:
            d['target_value_url'] = f"{PLAN_BASE}/api/v1/lookup/values/{self.target_value_guid}"
        return d


class PlanDefinitionActivity(db.Model):
    __tablename__ = 'plandefinition_activities'

    id = db.Column(db.Integer, primary_key=True)
    plandefinition_guid = db.Column(db.String(36), db.ForeignKey('plan_definitions.guid'), nullable=False)
    activity_guid = db.Column(db.String(36), db.ForeignKey('activities.guid'), nullable=False)
    sort_order = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('plandefinition_guid', 'activity_guid', name='uq_plandef_activity'),
    )

    activity_rel = db.relationship('Activity', foreign_keys=[activity_guid],
                                    primaryjoin='PlanDefinitionActivity.activity_guid == Activity.guid')

    def to_dict(self):
        return {
            'plandefinition_guid': self.plandefinition_guid,
            'activity_guid': self.activity_guid,
            'url': f"{PLAN_BASE}/api/v1/activities/{self.activity_guid}",
            'sort_order': self.sort_order,
        }
