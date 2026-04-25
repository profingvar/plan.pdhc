"""Seed termbank canonical libs + add (canonical_lib, canonical_refnumber) indexes

Implements platform-plan step 0.2.a:

  - Seeds five rows into ``canonical_libs``, one per termbank.pdhc system.
    The ``canonical_lib_name`` value matches termbank's ``system`` value
    exactly (loinc, socialstyrelsen, icd10, atc, snomed) so that
    ``(canonical_lib_name, canonical_refnumber)`` deterministically
    constructs the termbank canonical URL.
  - Adds composite indexes on ``(canonical_lib, canonical_refnumber)`` for
    Concept, ValueSet, and ValueCatalog so the upcoming ``$validate-code``
    endpoint can answer "is this canonical referenced anywhere?" in O(log n).

Idempotent: re-running this migration is a no-op for any already-existing
``canonical_lib_name`` (only inserts missing ones). Safe to apply on a
plan.pdhc instance that has been deployed via tarball without alembic
ever running.

Revision ID: c2d6ef39a1f0
Revises: b3a1f7c9d401
Create Date: 2026-04-25 14:30:00.000000+00:00
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from alembic import op


revision = "c2d6ef39a1f0"
down_revision = "b3a1f7c9d401"
branch_labels = None
depends_on = None


# (canonical_lib_name, display_text, canonical_lib_url)
# canonical_lib_name MUST match termbank.pdhc's `system` field exactly
# (Rule 27 / canonical URI determinism). Keep this list in sync with the
# systems that termbank actually has — ICD-11, KVÅ, ICF etc. can be added
# in a separate migration when those land in termbank.
CANONICAL_LIBS = [
    ("loinc",
     "LOINC",
     "https://termbank.pdhc.se/CodeSystem/loinc"),
    ("socialstyrelsen",
     "Socialstyrelsens termbank",
     "https://termbank.pdhc.se/CodeSystem/socialstyrelsen"),
    ("icd10",
     "ICD-10-SE",
     "https://termbank.pdhc.se/CodeSystem/icd10"),
    ("atc",
     "ATC (Anatomical Therapeutic Chemical)",
     "https://termbank.pdhc.se/CodeSystem/atc"),
    ("snomed",
     "SNOMED CT (SE Managed Service)",
     "https://termbank.pdhc.se/CodeSystem/snomed"),
]

SEED_AUTHOR = "termbank.pdhc"


def upgrade() -> None:
    # ---- 1. Composite indexes for fast $validate-code lookups -------------
    # Each table is indexed on (canonical_lib, canonical_refnumber) so the
    # endpoint's UNION over Concept / ValueCatalog (and occasionally ValueSet)
    # is index-driven.
    op.create_index(
        "ix_concepts_canonical_lib_refnumber",
        "concepts",
        ["canonical_lib", "canonical_refnumber"],
        unique=False,
    )
    op.create_index(
        "ix_valuesets_canonical_lib_refnumber",
        "valuesets",
        ["canonical_lib", "canonical_refnumber"],
        unique=False,
    )
    op.create_index(
        "ix_values_catalog_canonical_lib_refnumber",
        "values_catalog",
        ["canonical_lib", "canonical_refnumber"],
        unique=False,
    )

    # ---- 2. Seed canonical_libs (idempotent on canonical_lib_name) --------
    bind = op.get_bind()
    now = datetime.now(timezone.utc)
    for name, display, url in CANONICAL_LIBS:
        existing = bind.execute(
            sa.text(
                "SELECT 1 FROM canonical_libs WHERE canonical_lib_name = :n"
            ),
            {"n": name},
        ).first()
        if existing is not None:
            continue
        bind.execute(
            sa.text(
                """
                INSERT INTO canonical_libs (
                    guid,
                    canonical_lib_name,
                    canonical_lib_display_text,
                    canonical_lib_url,
                    author,
                    vers_number,
                    date_created,
                    date_valid
                ) VALUES (
                    :guid, :name, :display, :url, :author,
                    1, :now, :now
                )
                """
            ),
            {
                "guid": str(uuid.uuid4()),
                "name": name,
                "display": display,
                "url": url,
                "author": SEED_AUTHOR,
                "now": now,
            },
        )


def downgrade() -> None:
    bind = op.get_bind()
    # Only delete rows we authored (don't touch any workgroup-added rows
    # that happen to share a name).
    for name, _display, _url in CANONICAL_LIBS:
        bind.execute(
            sa.text(
                """
                DELETE FROM canonical_libs
                WHERE canonical_lib_name = :n AND author = :author
                """
            ),
            {"n": name, "author": SEED_AUTHOR},
        )

    op.drop_index(
        "ix_values_catalog_canonical_lib_refnumber",
        table_name="values_catalog",
    )
    op.drop_index(
        "ix_valuesets_canonical_lib_refnumber",
        table_name="valuesets",
    )
    op.drop_index(
        "ix_concepts_canonical_lib_refnumber",
        table_name="concepts",
    )
