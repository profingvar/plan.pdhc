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
