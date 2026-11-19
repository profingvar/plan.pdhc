"""Named concept subsets: mark and unmark concepts from the concept list.

Unlike a category (refused when unknown, #951 B.4), a subset is created by
naming it: marking terms for "andrea scenario" IS the act of making that
subset. Names are trimmed and matched exactly, so a typo shows up as a second
subset in the filter list, where it is visible, rather than silently merging.
"""
from __future__ import annotations

from app import db
from app.models.concept_models import Concept, ConceptSubset, ConceptSubsetLink

MAX_NAME = 255


class SubsetError(ValueError):
    pass


def get_or_create(name: str, *, author: str | None = None) -> ConceptSubset:
    name = (name or '').strip()
    if not name:
        raise SubsetError('Subset name is required')
    if len(name) > MAX_NAME:
        raise SubsetError(f'Subset name is longer than {MAX_NAME} characters')
    row = ConceptSubset.query.filter_by(subset_name=name).first()
    if row is None:
        row = ConceptSubset(subset_name=name, author=author)
        db.session.add(row)
        db.session.flush()
    return row


def mark(concept_guids, subset: ConceptSubset, *, author: str | None = None) -> int:
    """Link each existing concept not yet in the subset. Returns links made."""
    guids = {g for g in concept_guids if g}
    known = {c.guid for c in Concept.query.filter(Concept.guid.in_(guids))} if guids else set()
    have = {l.concept_guid for l in ConceptSubsetLink.query.filter_by(subset_guid=subset.guid)}
    n = 0
    for g in sorted(known - have):
        db.session.add(ConceptSubsetLink(concept_guid=g, subset_guid=subset.guid, author=author))
        n += 1
    return n


def unmark(concept_guids, subset: ConceptSubset) -> int:
    guids = [g for g in concept_guids if g]
    if not guids:
        return 0
    return (ConceptSubsetLink.query
            .filter(ConceptSubsetLink.subset_guid == subset.guid,
                    ConceptSubsetLink.concept_guid.in_(guids))
            .delete(synchronize_session=False))
