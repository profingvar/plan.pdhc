# planp Makefile — local dev + §6.8 conformance scaffolding.
#
# Day-to-day:
#   make test            # run pytest (includes D5 fast-layer FHIR validation)
#
# §6.8 canonical conformance:
#   make corpus          # emit sample resources from every new §6 endpoint
#                        # into tests/fhir_corpus/*.json
#   make conformance     # validate the corpus against HL7 validator_cli.jar
#                        # (requires VALIDATOR_JAR pointing to a downloaded copy)

VENV ?= venv
PY := $(VENV)/bin/python
PYTEST := $(VENV)/bin/pytest

VALIDATOR_JAR ?= $(HOME)/.local/share/fhir/validator_cli.jar
CORPUS_DIR := tests/fhir_corpus
FHIR_VERSION := 5.0.0


.PHONY: help test corpus conformance check-jar

help:
	@echo "Targets: test, corpus, conformance, check-jar"

test:
	$(PYTEST) -q

corpus:
	@mkdir -p $(CORPUS_DIR)
	$(PY) tests/conformance_corpus_emit.py $(CORPUS_DIR)
	@echo "Corpus refreshed at $(CORPUS_DIR)/"
	@ls -1 $(CORPUS_DIR)/*.json | wc -l | xargs -I{} echo "{} JSON files"

check-jar:
	@if [ ! -f "$(VALIDATOR_JAR)" ]; then \
		echo "MISSING $(VALIDATOR_JAR)"; \
		echo "Download from https://github.com/hapifhir/org.hl7.fhir.core/releases/latest"; \
		echo "and place at $(VALIDATOR_JAR), or pass VALIDATOR_JAR=<path>."; \
		exit 1; \
	fi

conformance: check-jar corpus
	@echo "Validating $(CORPUS_DIR)/*.json against FHIR R5..."
	java -jar "$(VALIDATOR_JAR)" -version $(FHIR_VERSION) $(CORPUS_DIR)/*.json
