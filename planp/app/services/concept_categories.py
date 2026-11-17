"""#951: the ONE place a category reference is resolved.

The `resolve_or_local` lesson (#786): the form, the API, the importer and the
filter each resolving names on their own is how they drift. All four call this.

A reference is a category NAME or GUID. An unknown reference is an error,
never a new category: auto-creating turns a typo into a category (the
"snomd" failure mode in another field, #951 B.4). Categories are created
deliberately, through `/api/v1/lookup/concept-categories`.
"""
from __future__ import annotations

from app import db
from app.models.concept_models import ConceptCategory, ConceptCategoryLink

#: Several categories in one cell or parameter are separated by this.
SEPARATOR = ';'


class UnknownCategory(ValueError):
    pass


def split(value) -> list[str]:
    """'a; b ;' -> ['a', 'b']. None / blank -> []."""
    if value is None:
        return []
    return [p.strip() for p in str(value).split(SEPARATOR) if p.strip()]


def resolve(ref: str) -> ConceptCategory:
    """One category by name or guid. Raises UnknownCategory."""
    row = (ConceptCategory.query.filter_by(category_name=ref).first()
           or ConceptCategory.query.filter_by(guid=ref).first())
    if row is None:
        raise UnknownCategory(f'category not found: {ref!r}')
    return row


def resolve_all(value) -> list[ConceptCategory]:
    """Every reference in `value` (a list or a ';'-joined string), in order,
    without duplicates. Raises on the first unknown one."""
    refs = value if isinstance(value, (list, tuple)) else split(value)
    out, seen = [], set()
    for ref in refs:
        row = resolve(str(ref).strip())
        if row.guid not in seen:
            seen.add(row.guid)
            out.append(row)
    return out


def add(concept_guid: str, categories, *, import_guid: str | None = None) -> int:
    """Link `concept_guid` to each category it is not yet linked to.

    ADDITIVE: an import never removes a category a concept already has --
    with many categories per concept (D1) a second guideline adds its own and
    leaves the first. Returns the number of links created. Caller commits.
    """
    have = {l.category_guid for l in ConceptCategoryLink.query.filter_by(concept_guid=concept_guid)}
    n = 0
    for c in categories:
        if c.guid in have:
            continue
        db.session.add(ConceptCategoryLink(concept_guid=concept_guid, category_guid=c.guid,
                                           import_guid=import_guid))
        have.add(c.guid)
        n += 1
    return n


def replace(concept_guid: str, categories) -> None:
    """Set a concept's categories to exactly `categories` (a hand edit).

    Links that stay keep their `import_guid`; only removed ones go. Caller
    commits.
    """
    want = {c.guid for c in categories}
    for link in ConceptCategoryLink.query.filter_by(concept_guid=concept_guid).all():
        if link.category_guid not in want:
            db.session.delete(link)
    add(concept_guid, categories)
