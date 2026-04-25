# Plan.pdhc — FHIR Questionnaire: add questionnaire-itemControl extension for Slider concepts

## Background

When Plan produces a FHIR Questionnaire from the form catalogue, concepts with Response Type **Slider** are emitted as:

```json
{
  "linkId": "1a5e2929-a249-4aa2-94a1-c1c16f78804b",
  "text": "Hur upplever du din livskvalitet",
  "type": "integer",
  "extension": [
    { "url": "http://hl7.org/fhir/StructureDefinition/minValue", "valueInteger": 0 },
    { "url": "http://hl7.org/fhir/StructureDefinition/maxValue", "valueInteger": 10 }
  ]
}
```

This is valid FHIR, but downstream consumers (request.pdhc, 1177.pdhc, provider portals) cannot distinguish a slider from a plain integer input without guessing from the min/max pattern.

## Requested change

When a concept has `response_type == "slider"`, add the standard HL7 `questionnaire-itemControl` extension to the Questionnaire item:

```json
{
  "linkId": "1a5e2929-a249-4aa2-94a1-c1c16f78804b",
  "text": "Hur upplever du din livskvalitet",
  "type": "integer",
  "extension": [
    { "url": "http://hl7.org/fhir/StructureDefinition/minValue", "valueInteger": 0 },
    { "url": "http://hl7.org/fhir/StructureDefinition/maxValue", "valueInteger": 10 },
    {
      "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
      "valueCodeableConcept": {
        "coding": [
          {
            "system": "http://hl7.org/fhir/questionnaire-item-control",
            "code": "slider",
            "display": "Slider"
          }
        ]
      }
    }
  ]
}
```

## Where to change

The Questionnaire builder in Plan — wherever items are assembled from form-definition rows. When the concept's `response_type` is `"slider"` (or the equivalent internal field), append the extension above alongside the existing minValue/maxValue extensions.

## Why

- **FHIR compliance**: `questionnaire-itemControl` is the standard way to signal rendering intent. See [HL7 extension definition](http://hl7.org/fhir/R5/extension-questionnaire-itemcontrol.html).
- **Downstream rendering**: request.pdhc, 1177.pdhc, and provider portals all need to know whether to render a slider widget or a plain number input. Without the extension they must infer from min/max, which is fragile and breaks for integer fields that happen to have a range but are not sliders.
- **Interoperability**: third-party FHIR renderers (e.g. LHC-Forms, HAPI) will only render a slider if the extension is present.

## Implementation status

**Implemented.** The `questionnaire-itemControl` extension with `code: "slider"` is now emitted by plan.pdhc's FHIR Questionnaire builder for slider-type concepts.

**Downstream support:**

- **1177.pdhc** — Detects the `questionnaire-itemControl` extension and renders a mechanical slider widget with colored fill track, tick marks, anchor labels, and live value badge. Falls back to anchor label detection (`questionnaire-sliderStepValue`) for Questionnaires produced before the extension was added.
- **request.pdhc** — Passes the extension through transparently in ServiceRequest bundles. No special handling required.

## Impact

No breaking change — this adds an extension to existing items. Existing consumers that don't check for it are unaffected.
