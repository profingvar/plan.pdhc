"""#942 — plan owns the concept reference format; the reference passes the corpus."""
import json
import pathlib

import pytest

from app import concept_urn as cu

CORPUS = json.loads((pathlib.Path(__file__).resolve().parents[2] / "conformance" / "concept_urn_cases.json").read_text())


@pytest.mark.parametrize("c", CORPUS["guid_of"], ids=lambda c: repr(c["value"]))
def test_guid_of(c):
    assert cu.guid_of(c["value"]) == c["guid"]


def test_build_round_trips_and_refuses():
    g = "64928bff-9a46-472a-bbf1-dcfc694f945b"
    assert cu.guid_of(cu.build(g)) == g and cu.build(g.upper()) == cu.PREFIX + g
    with pytest.raises(ValueError):
        cu.build("x")
