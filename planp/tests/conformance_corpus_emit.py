"""§6.8 — emit a representative FHIR corpus from every §6 endpoint.

Boots a self-contained test app (SQLite tmp DB), seeds a minimum dataset
(CanonicalLib + Concept + ValueSet + ValueCatalog + ValueSetValue), then
calls every new FHIR terminology route and writes the JSON response to a
dated dir. The HL7 R5 validator_cli.jar consumes these via `make conformance`.

Run:   python tests/conformance_corpus_emit.py [out_dir]
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

# Ensure the app module is importable when this script is run directly.
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def _bootstrap_env(tmp_db_path: str) -> None:
    os.environ['DATABASE_URL'] = f'sqlite:///{tmp_db_path}'
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['JWT_SECRET_KEY'] = 'corpus-jwt-secret'
    os.environ['FLASK_SECRET_KEY'] = 'corpus-flask-secret'
    os.environ['BOOTSTRAP_SU_USERNAME'] = 'admin'
    os.environ['BOOTSTRAP_SU_PASSWORD'] = 'admin123'
    os.environ['AUTH_DISABLED'] = 'false'
    os.environ['SSO_BASE_URL'] = 'http://sso-test:9000'
    os.environ['SSO_CLIENT_ID'] = 'corpus'
    os.environ['SSO_CLIENT_SECRET'] = 'corpus-secret'
    os.environ['SSO_CALLBACK_URL'] = 'http://localhost:9030/api/v1/auth/callback'


def _seed(app):
    from app import db as _db
    from app.models.concept_models import (
        CanonicalLib, Concept, ValueCatalog, ValueSet, ValueSetValue,
    )

    with app.app_context():
        lib = CanonicalLib(
            canonical_lib_name='corpus_loinc',
            canonical_lib_display_text='LOINC (corpus)',
            canonical_lib_url='https://termbank.pdhc.se/CodeSystem/corpus-loinc',
            author='corpus',
        )
        _db.session.add(lib)
        _db.session.flush()

        hba1c = Concept(
            canonical_lib=lib.guid,
            canonical_refnumber='4548-4',
            concept_name='corpus_hba1c',
            concept_display_text='HbA1c (corpus)',
            concept_explain='Hemoglobin A1c — corpus sample.',
        )
        _db.session.add(hba1c)
        _db.session.flush()

        v_yes = ValueCatalog(
            canonical_lib=lib.guid, canonical_refnumber='Y',
            value_name='corpus_yes', value_display_text='Yes',
        )
        v_no = ValueCatalog(
            canonical_lib=lib.guid, canonical_refnumber='N',
            value_name='corpus_no', value_display_text='No',
        )
        _db.session.add_all([v_yes, v_no])
        _db.session.flush()

        vs = ValueSet(
            canonical_lib=lib.guid,
            valueset_name='CorpusYesNo',
            valueset_display_text='Corpus Yes/No',
        )
        _db.session.add(vs)
        _db.session.flush()
        _db.session.add_all([
            ValueSetValue(valueset_guid=vs.guid, value_guid=v_yes.guid, sort_order=1),
            ValueSetValue(valueset_guid=vs.guid, value_guid=v_no.guid, sort_order=2),
        ])
        _db.session.commit()

        return {
            'lib_url': lib.canonical_lib_url,
            'concept_guid': hba1c.guid,
            'valueset_guid': vs.guid,
        }


def _write(out_dir: str, name: str, body: dict) -> None:
    path = os.path.join(out_dir, f'{name}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(body, f, indent=2, ensure_ascii=False, sort_keys=True)
    print(f'  wrote {path}')


def emit_corpus(out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)

    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    try:
        _bootstrap_env(db_path)

        from app import create_app, db as _db
        from app.api.fhir_codesystem import LOCAL_CS_URL as CS_URL
        from app.models.concept_models import (
            LOCAL_CODESYSTEM_ID, LOCAL_CONCEPTMAP_ID,
        )

        app = create_app(testing=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

        with app.app_context():
            _db.create_all()

        seeds = _seed(app)
        client = app.test_client()

        print(f'Emitting FHIR corpus → {out_dir}')

        # Resource reads
        for path, name in [
            (f'/api/v1/CodeSystem/{LOCAL_CODESYSTEM_ID}', 'codesystem_local_read'),
            (f'/api/v1/ConceptMap/{LOCAL_CONCEPTMAP_ID}', 'conceptmap_read'),
            (f"/api/v1/ValueSet/{seeds['valueset_guid']}", 'valueset_read'),
        ]:
            _write(out_dir, name, client.get(path).get_json())

        # Searchset bundles
        for path, name in [
            ('/api/v1/CodeSystem', 'codesystem_search_bundle'),
            ('/api/v1/ConceptMap', 'conceptmap_search_bundle'),
            ('/api/v1/ValueSet', 'valueset_search_bundle'),
        ]:
            _write(out_dir, name, client.get(path).get_json())

        # Operations
        _write(out_dir, 'valueset_expand',
               client.get(f"/api/v1/ValueSet/{seeds['valueset_guid']}/$expand")
               .get_json())

        _write(out_dir, 'valueset_validate_code_scoped',
               client.get(
                   f"/api/v1/ValueSet/{seeds['valueset_guid']}/$validate-code"
                   f"?system={seeds['lib_url']}&code=Y"
               ).get_json())

        _write(out_dir, 'valueset_validate_code_global_cdr_shape',
               client.get(
                   f"/api/v1/ValueSet/$validate-code"
                   f"?system=corpus_loinc&code=4548-4"
               ).get_json())

        _write(out_dir, 'codesystem_lookup_local',
               client.get(
                   f"/api/v1/CodeSystem/$lookup"
                   f"?system={CS_URL}&code={seeds['concept_guid']}"
               ).get_json())

        _write(out_dir, 'conceptmap_translate_local_to_canonical',
               client.get(
                   f"/api/v1/ConceptMap/$translate"
                   f"?system={CS_URL}&code={seeds['concept_guid']}"
               ).get_json())

        _write(out_dir, 'conceptmap_translate_canonical_to_local',
               client.get(
                   f"/api/v1/ConceptMap/$translate"
                   f"?system={seeds['lib_url']}&code=4548-4"
               ).get_json())

        # Capability statement
        _write(out_dir, 'capability_statement',
               client.get('/api/v1/metadata').get_json())

        print(f'Done — {len(os.listdir(out_dir))} files.')
    finally:
        os.close(db_fd)
        if os.path.exists(db_path):
            os.remove(db_path)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'fhir_corpus')
    emit_corpus(out)
