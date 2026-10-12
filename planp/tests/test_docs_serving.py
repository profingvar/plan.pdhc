"""#338 — DEPLOYMENT_PLAN.md is NOT advertised by /api/v1/docs.

The historical "PDHC Gateway" deployment plan does not match the
current container-based deploy model (rollup #325). It has been
rewritten in place; the file is kept in the repo for historical
context but must not be served to API consumers as authoritative.
"""
from __future__ import annotations


class TestDeploymentPlanNotServed:
    def test_deployment_plan_not_in_docs_catalog(self, client):
        resp = client.get('/api/v1/docs')
        assert resp.status_code == 200
        body = resp.get_json()
        filenames = {d['filename'] for d in body['documents']}
        assert 'DEPLOYMENT_PLAN.md' not in filenames, (
            'DEPLOYMENT_PLAN.md must not be served via /api/v1/docs — it '
            'contains stale "PDHC Gateway" framing. See rollup #325 / #338.'
        )

    def test_deployment_plan_download_404(self, client):
        resp = client.get('/api/v1/docs/DEPLOYMENT_PLAN.md')
        assert resp.status_code == 404, (
            'GET /api/v1/docs/DEPLOYMENT_PLAN.md must 404 (not in DOCS_CATALOG).'
        )

    def test_api_reference_still_served(self, client):
        # Sanity: legitimate docs are still served.
        resp = client.get('/api/v1/docs/api_reference.md')
        assert resp.status_code == 200


class TestEveryCatalogEntryActuallyResolves:
    """#786 item 3. The catalog advertised a document that 404'd, and hid the
    two most current ones.

    The failure was invisible by construction: `_get_docs_list()` uses the same
    resolver as the download route and simply OMITS anything that does not
    resolve. So a broken entry disappeared from the listing instead of
    appearing as broken, and nobody could see that the catalog and the
    filesystem disagreed. These tests compare the two directly.
    """

    def test_no_catalog_entry_is_unresolvable(self, client):
        """`db_schema_snapshot.md` was the one that failed: it lives at
        `planp/db_schema_snapshot.md`, and the resolver searched `planp/docs/`,
        the project root and `/project-docs` -- never `planp/` itself.
        """
        from app.api.capability import DOCS_CATALOG, _resolve_doc_path
        unresolved = [f for f in DOCS_CATALOG if _resolve_doc_path(f) is None]
        assert unresolved == [], (
            'these are advertised in DOCS_CATALOG but resolve to no file, so '
            'they are silently dropped from /docs: %r' % unresolved)

    def test_no_catalog_entry_depends_on_a_CASE_INSENSITIVE_filesystem(self):
        """The one `_resolve_doc_path` cannot catch on a Mac.

        `readme.md` was advertised; the file is `README.md`. macOS matches
        those, so `os.path.isfile` returned True locally and every test
        passed. CI and the Linux server do not, so the entry resolved to
        None and vanished from /docs on exactly the two machines that
        matter — and because the resolver omits what it cannot resolve, the
        only symptom was a document quietly missing from the listing.

        So this compares the catalogue against the REAL directory entries,
        character for character, instead of asking the filesystem whether a
        path exists.
        """
        import os
        from app.api.capability import DOCS_CATALOG, _resolve_doc_path

        mismatched = []
        for name in DOCS_CATALOG:
            path = _resolve_doc_path(name)
            if path is None:
                continue          # the other test reports these
            actual = os.path.basename(path)
            # `_resolve_doc_path` joins the catalogue name onto a directory,
            # so `path` echoes the name back whatever the file is really
            # called. Ask the DIRECTORY what it holds.
            real = os.listdir(os.path.dirname(path))
            if actual not in real:
                exact = [f for f in real if f.lower() == actual.lower()]
                mismatched.append((name, exact[0] if exact else "?"))
        assert mismatched == [], (
            'these resolve only because this filesystem ignores case; on '
            'Linux they will not resolve at all: %r' % (mismatched,))

    def test_the_schema_snapshot_is_served(self, client):
        resp = client.get('/api/v1/docs/db_schema_snapshot.md')
        assert resp.status_code == 200

    def test_the_schema_snapshot_is_generated_not_hand_written(self, client):
        """It was hand-maintained, dated 2026-03-20, and claimed 17 tables
        while the database had 22 -- the whole forms/questionnaire subsystem
        was absent while the dashboard counted Forms on its front page.
        It is now generated, and the marker says so.
        """
        body = client.get('/api/v1/docs/db_schema_snapshot.md').data.decode()
        assert 'gen_db_schema_snapshot.py' in body
        assert 'Tables: 22' in body or '**Tables:** 22' in body

    def test_the_two_rule_25_documents_are_offered(self, client):
        """Rule 25 requires docs/technical.md and docs/user_manual.md to
        exist. They did -- and were advertised nowhere, while /docs listed
        eleven documents older than 60 days."""
        body = client.get('/api/v1/docs').get_json()
        filenames = {d['filename'] for d in body['documents']}
        assert 'technical.md' in filenames
        assert 'user_manual.md' in filenames

    def test_sso_documents_stay_out_of_this_services_catalog(self, client):
        """Deliberately absent. routes/main.py records that a previous second
        copy of this catalog drifted by advertising exactly these; sso.pdhc
        serves its own documentation."""
        body = client.get('/api/v1/docs').get_json()
        filenames = {d['filename'] for d in body['documents']}
        assert 'sso_technical_manual.md' not in filenames
        assert 'sso_user_guide.md' not in filenames


class TestNoDocumentIsShadowed:
    """#786 item 3, follow-up — a hazard the resolver fix itself created.

    Adding `planp/` to the search path is what made `db_schema_snapshot.md`
    resolvable, because that is where it lives. But `planp/` now sits BEFORE
    the project root, so any document present in both locations silently
    resolves to the `planp/` copy.

    That is not hypothetical: writing this ticket's notes, progress.md and
    changed_files.md were appended under `planp/` instead of the repo root,
    creating 135-line and 15-line stubs beside the real 1142-line and 447-line
    files. /docs then served the stubs. The resolver was doing exactly what it
    was told; the two files were the mistake.

    So the invariant is not "the resolver works" but "no catalog document
    exists in more than one search directory". A shadowed document is worse
    than a missing one: a missing one 404s, a shadowed one serves a plausible
    wrong answer.
    """

    def test_no_catalog_document_exists_in_two_search_directories(self):
        import os
        from app.api import capability
        from app.api.capability import DOCS_CATALOG

        planp_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(capability.__file__))))
        search_dirs = [
            os.path.join(planp_dir, 'docs'),
            planp_dir,
            os.path.dirname(planp_dir),
            '/project-docs',
        ]
        shadowed = {}
        for filename in DOCS_CATALOG:
            hits = [d for d in search_dirs
                    if os.path.isfile(os.path.join(d, filename))]
            if len(hits) > 1:
                shadowed[filename] = hits
        assert shadowed == {}, (
            'these documents exist in more than one search directory, so /docs '
            'serves whichever comes first and the other copy is invisible: %r'
            % shadowed)
