FROM python:3.11-slim

# Build context is the REPO ROOT (one level above this Dockerfile) so we
# can COPY the documentation that lives at the project root. See
# planp/docker-compose.yml — `context: ..` + `dockerfile: planp/Dockerfile`.

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY planp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY planp/app/ ./app/
COPY planp/migrations/ ./migrations/
COPY planp/docs/ ./docs/
COPY planp/db_schema_snapshot.md ./docs/
COPY planp/entrypoint.sh .

# Root-level docs surfaced via GET /api/v1/docs/<filename>. Listed
# explicitly (not by glob) so a stray root-level .md doesn't silently
# end up in the image. Keep in sync with DOCS_CATALOG in
# planp/app/api/capability.py.
COPY plan_description.md \
     progress.md \
     top_rules.md \
     repo_css.md \
     pdhc_markdown_layout_standard.md \
     changed_files.md \
     nginx_implement_server19March.md \
     plan_pdhc_fhir_terminology_profile_instruction.md \
     plan_pdhc_fhir_terminology_profile_DECISIONS.md \
     ./docs/
# readme.md — catalog uses lowercase. On miserver and on case-insensitive
# macOS dev boxes either case resolves; on a case-sensitive Linux build
# context (e.g. CI) you must ensure the lowercase variant exists on disk.
COPY readme.md ./docs/readme.md

RUN chmod +x entrypoint.sh

EXPOSE 9030

ENTRYPOINT ["./entrypoint.sh"]
