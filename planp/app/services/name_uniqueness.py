import re
from app import db


class NameUniquenessService:
    """Ensures name uniqueness for concepts, values, and valuesets."""

    @staticmethod
    def make_unique_name(name, model_class, name_field):
        """For API/import: auto-suffix if name already exists."""
        existing = model_class.query.filter(
            getattr(model_class, name_field) == name
        ).first()
        if not existing:
            return name

        base = re.sub(r'_\d+$', '', name)
        counter = 1
        while True:
            candidate = f'{base}_{counter}'
            exists = model_class.query.filter(
                getattr(model_class, name_field) == candidate
            ).first()
            if not exists:
                return candidate
            counter += 1

    @staticmethod
    def validate_name_for_manual_entry(name, model_class, name_field, exclude_guid=None):
        """For web UI: reject duplicates. Returns error message or None."""
        query = model_class.query.filter(
            getattr(model_class, name_field) == name
        )
        if exclude_guid:
            query = query.filter(model_class.guid != exclude_guid)
        if query.first():
            return f'A record with name "{name}" already exists.'
        return None


def make_unique_concept_name(name):
    from app.models.concept_models import Concept
    return NameUniquenessService.make_unique_name(name, Concept, 'concept_name')


def make_unique_value_name(name):
    from app.models.concept_models import ValueCatalog
    return NameUniquenessService.make_unique_name(name, ValueCatalog, 'value_name')


def make_unique_valueset_name(name):
    from app.models.concept_models import ValueSet
    return NameUniquenessService.make_unique_name(name, ValueSet, 'valueset_name')
