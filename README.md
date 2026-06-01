# plan.pdhc

Plan-definition authoring service for the **PDHC** platform — the
PlanDef Builder.

This is one of the service repositories that together form
[Planned Data in Healthcare](https://pdhc.se). It is the authoring
surface where clinicians and care designers build FHIR R5
`PlanDefinition` resources: concepts, value sets, response types,
timing, and the activity structure that downstream services then
execute, apply, and observe against.

## What this service does

- CRUD over **Concepts**, **ValueSets**, and **Values** (the
  terminology substrate)
- Authoring of **PlanDefinition** resources composed of activities,
  schedules, and concept-bound questions
- Bulk loading of concept catalogues via a service-key API
- Emission of valid FHIR R5 `PlanDefinition` and `Questionnaire`
  bundles for downstream services (`request.pdhc`, `1177.pdhc`,
  provider services)
- SSO-backed access control via `sso.pdhc`

The PDHC platform deliberately separates **authoring** (plan.pdhc) from
**execution and alerting** (request.pdhc). This service is the "what
should happen" side of the boundary.

## Layout

- `planp/` — Flask application, models, API, builder UI, migrations
- `start.sh` — single entry point
- `planp/.env.example` — required environment variables
- `DEPLOYMENT_PLAN.md` — historical numbered deployment plan (internal reference)

## Running locally

```bash
cp planp/.env.example planp/.env   # then fill in the values
docker compose up -d db            # postgres on 9031
flask db upgrade
python -m gunicorn --bind 127.0.0.1:9030 'app:create_app()'
```

See `planp/.env.example` for required environment.

## License

MIT — see [LICENSE](LICENSE).
