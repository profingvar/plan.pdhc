# §6.8 FHIR R5 conformance corpus

Auto-generated FHIR resources from every §6 terminology endpoint, used by
`make conformance` to validate against the HL7 official R5 validator.

**Do not edit by hand** — `make corpus` overwrites everything here.

## Workflow

```bash
# 1. Regenerate the corpus from current code
make corpus

# 2. Validate it (requires VALIDATOR_JAR to point to a downloaded copy)
make conformance
```

If `VALIDATOR_JAR` is missing, the target tells you where to download:
<https://github.com/hapifhir/org.hl7.fhir.core/releases/latest>

Default location: `~/.local/share/fhir/validator_cli.jar`. Override with
`make conformance VALIDATOR_JAR=/some/other/path.jar`.

## Two-layer validation

This corpus + jar is the **slow / canonical layer** (ADR D5). Every test
run also exercises the **fast / pydantic layer** via `fhir.resources`,
which catches shape errors at unit-test speed. The full validator
catches FHIR-semantic checks (binding rules, slicing, profile
conformance) that pydantic can't.

## CI wiring (open)

The corpus emitter is wired locally. Adding a CI job that downloads
`validator_cli.jar` on first run (cached) and runs `make conformance`
against PRs is the remaining devops step, called out in
`plan_pdhc_fhir_terminology_profile_instruction.md` §9 Risk 4
(validator-infra long-tail).
