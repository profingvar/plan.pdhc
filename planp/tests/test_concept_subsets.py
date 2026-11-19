"""Named subsets on the concept list, and sorting by name / class / created."""
from datetime import datetime, timezone

import pytest

from app import db
from app.models.concept_models import (
    CanonicalLib, Concept, ConceptCategory, ConceptCategoryLink, ConceptSubset,
    ConceptSubsetLink,
)
from tests.conftest import SAMPLE_SU_BLOB, set_sso_session


@pytest.fixture(autouse=True)
def _seed(app):
    with app.app_context():
        lib = CanonicalLib.query.filter_by(canonical_lib_name='local').first()
        if lib is None:
            lib = CanonicalLib(canonical_lib_name='local'); db.session.add(lib); db.session.flush()
        cats = {}
        for n in ('Symptom', 'Condition'):
            cats[n] = ConceptCategory.query.filter_by(category_name=n).first() or ConceptCategory(category_name=n)
            db.session.add(cats[n])
        db.session.flush()
        # name, created day, category
        for name, day, cat in (('sub-aaa', 3, 'Symptom'), ('sub-bbb', 1, None),
                               ('sub-ccc', 2, 'Condition')):
            c = Concept(concept_name=name, canonical_lib=lib.guid,
                        date_created=datetime(2026, 11, day, tzinfo=timezone.utc))
            db.session.add(c); db.session.flush()
            if cat:
                db.session.add(ConceptCategoryLink(concept_guid=c.guid, category_guid=cats[cat].guid))
        db.session.commit()
        yield
        ConceptSubsetLink.query.delete(); ConceptSubset.query.delete()
        ConceptCategoryLink.query.delete(); Concept.query.delete()
        db.session.commit()


def _order(client, **params):
    html = client.get('/concepts/', query_string=params).get_data(as_text=True)
    return sorted(('sub-aaa', 'sub-bbb', 'sub-ccc'), key=html.index)


def _guid(app, name):
    with app.app_context():
        return Concept.query.filter_by(concept_name=name).one().guid


def test_sort_by_created(client):
    assert _order(client, sort='created') == ['sub-bbb', 'sub-ccc', 'sub-aaa']
    assert _order(client, sort='created', dir='desc') == ['sub-aaa', 'sub-ccc', 'sub-bbb']


def test_sort_by_class_puts_unclassified_last(client):
    assert _order(client, sort='class') == ['sub-ccc', 'sub-aaa', 'sub-bbb']
    assert _order(client, sort='class', dir='desc') == ['sub-aaa', 'sub-ccc', 'sub-bbb']


def test_default_and_unknown_sort_is_by_name(client):
    assert _order(client) == ['sub-aaa', 'sub-bbb', 'sub-ccc']
    assert _order(client, sort='nonsense') == ['sub-aaa', 'sub-bbb', 'sub-ccc']


def test_header_link_flips_direction(client):
    html = client.get('/concepts/?sort=created&dir=asc').get_data(as_text=True)
    assert 'sort=created&amp;dir=desc' in html
    assert 'sort=class&amp;dir=asc' in html


def test_mark_creates_subset_and_filter_shows_only_members(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    a, c = _guid(app, 'sub-aaa'), _guid(app, 'sub-ccc')
    r = client.post('/concepts/subsets/mark', data={
        'subset_name': '  Andrea scenario ', 'action': 'add',
        'concept_guid': [a, c], 'next': '/concepts/?sort=created'})
    assert r.status_code == 302 and r.headers['Location'].endswith('/concepts/?sort=created')
    with app.app_context():
        s = ConceptSubset.query.one()
        assert s.subset_name == 'Andrea scenario'
        assert ConceptSubsetLink.query.filter_by(subset_guid=s.guid).count() == 2
        sg = s.guid
    html = client.get(f'/concepts/?subset={sg}').get_data(as_text=True)
    assert 'sub-aaa' in html and 'sub-ccc' in html and 'sub-bbb' not in html
    # Marking again adds nothing.
    client.post('/concepts/subsets/mark', data={'subset_name': 'Andrea scenario',
                                                'concept_guid': [a]})
    with app.app_context():
        assert ConceptSubsetLink.query.count() == 2


def test_remove_unmarks_only_ticked(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    a, c = _guid(app, 'sub-aaa'), _guid(app, 'sub-ccc')
    client.post('/concepts/subsets/mark', data={'subset_name': 'S', 'concept_guid': [a, c]})
    client.post('/concepts/subsets/mark', data={'subset_name': 'S', 'action': 'remove',
                                                'concept_guid': [a]})
    with app.app_context():
        assert [l.concept_guid for l in ConceptSubsetLink.query] == [c]
        assert ConceptSubset.query.count() == 1   # removing never deletes the subset


def test_remove_from_unknown_subset_creates_nothing(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    client.post('/concepts/subsets/mark', data={'subset_name': 'nope', 'action': 'remove',
                                                'concept_guid': [_guid(app, 'sub-aaa')]})
    with app.app_context():
        assert ConceptSubset.query.count() == 0


def test_mark_requires_name_and_ticks(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    client.post('/concepts/subsets/mark', data={'subset_name': '   ',
                                                'concept_guid': [_guid(app, 'sub-aaa')]})
    client.post('/concepts/subsets/mark', data={'subset_name': 'X'})
    with app.app_context():
        assert ConceptSubset.query.count() == 0


def test_mark_refuses_offsite_redirect(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    r = client.post('/concepts/subsets/mark', data={
        'subset_name': 'S', 'concept_guid': [_guid(app, 'sub-aaa')], 'next': 'https://evil.example/'})
    assert 'evil.example' not in r.headers['Location']


def test_mark_needs_login(app, client):
    r = client.post('/concepts/subsets/mark', data={'subset_name': 'S',
                                                    'concept_guid': [_guid(app, 'sub-aaa')]})
    assert r.status_code in (302, 401, 403)
    with app.app_context():
        assert ConceptSubset.query.count() == 0


def test_subsets_migration_is_the_single_head():
    import pathlib, re
    vers = pathlib.Path(__file__).resolve().parents[1] / 'migrations' / 'versions'
    revs, downs = set(), set()
    for f in vers.glob('*.py'):
        t = f.read_text()
        revs.add(re.search(r"^revision = ['\"]([^'\"]+)", t, re.M).group(1))
        m = re.search(r"^down_revision = ['\"]([^'\"]+)", t, re.M)
        if m:
            downs.add(m.group(1))
    assert revs - downs == {'c5d1e2f3a4b7'}


# ------------------------------------------------------------------ marked for deletion

def test_mark_for_deletion_flags_without_deleting_and_filter_lists_them(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    a = _guid(app, 'sub-aaa')
    r = client.post('/concepts/deletion-marks', data={'action': 'mark', 'concept_guid': [a],
                                                      'next': '/concepts/?sort=class'})
    assert r.status_code == 302 and r.headers['Location'].endswith('/concepts/?sort=class')
    with app.app_context():
        c = Concept.query.filter_by(guid=a).one()            # still there
        assert c.marked_for_deletion_at is not None
        assert c.marked_for_deletion_by == SAMPLE_SU_BLOB['email']
        assert Concept.query.filter(Concept.marked_for_deletion_at.isnot(None)).count() == 1
    html = client.get('/concepts/?subset=marked-for-deletion').get_data(as_text=True)
    assert 'sub-aaa' in html and 'sub-bbb' not in html and 'sub-ccc' not in html
    assert 'Marked for deletion (1)' in html
    view = client.get(f'/concepts/{a}').get_data(as_text=True)
    assert 'Unmark deletion' in view and 'to delete' in view


def test_unmark_deletion(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    a, c = _guid(app, 'sub-aaa'), _guid(app, 'sub-ccc')
    client.post('/concepts/deletion-marks', data={'action': 'mark', 'concept_guid': [a, c]})
    client.post('/concepts/deletion-marks', data={'action': 'unmark', 'concept_guid': [a]})
    with app.app_context():
        marked = [x.concept_name for x in Concept.query.filter(Concept.marked_for_deletion_at.isnot(None))]
        assert marked == ['sub-ccc']
        assert Concept.query.filter_by(guid=a).one().marked_for_deletion_by is None


def test_remark_keeps_first_marker(app, client):
    set_sso_session(client, SAMPLE_SU_BLOB)
    a = _guid(app, 'sub-aaa')
    client.post('/concepts/deletion-marks', data={'action': 'mark', 'concept_guid': [a]})
    with app.app_context():
        first = Concept.query.filter_by(guid=a).one().marked_for_deletion_at
    client.post('/concepts/deletion-marks', data={'action': 'mark', 'concept_guid': [a]})
    with app.app_context():
        assert Concept.query.filter_by(guid=a).one().marked_for_deletion_at == first


def test_deletion_mark_needs_login_and_ticks(app, client):
    a = _guid(app, 'sub-aaa')
    r = client.post('/concepts/deletion-marks', data={'action': 'mark', 'concept_guid': [a]})
    assert r.status_code in (302, 401, 403)
    set_sso_session(client, SAMPLE_SU_BLOB)
    client.post('/concepts/deletion-marks', data={'action': 'mark'})
    with app.app_context():
        assert Concept.query.filter(Concept.marked_for_deletion_at.isnot(None)).count() == 0


def test_list_buttons_post_to_deletion_route_without_needing_a_subset_name(client):
    html = client.get('/concepts/').get_data(as_text=True)
    assert 'formaction="/concepts/deletion-marks" formnovalidate' in html
