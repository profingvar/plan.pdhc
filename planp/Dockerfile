FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY migrations/ ./migrations/
COPY docs/ ./docs/
COPY db_schema_snapshot.md ./docs/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 9030

ENTRYPOINT ["./entrypoint.sh"]
