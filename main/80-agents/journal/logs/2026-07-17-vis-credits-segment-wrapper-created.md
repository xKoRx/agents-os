---
type: change_log
scope: session
created: 2026-07-17
updated: 2026-07-17
area: "[[Meli]]"
project:
application: "[[vis-credits-segment-wrapper]]"
entities:
  - "[[vis-credits-segment-wrapper]]"
  - "[[vis-credits-consumer]]"
  - "[[vis-items-loader-tagging]]"
related: []
aliases:
  - vis credits segment wrapper application created
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/meli
  - kind/change-log
  - scope/session
---

# vis-credits-segment-wrapper application created

## Cambio

- **Tipo:** created
- **Archivo:** `30-resources/applications/vis-credits-segment-wrapper.md`

## Motivo

- Se necesitaba registrar la aplicación que responde la decisión de Credits consultada por `vis-credits-consumer`.

## Fuentes usadas

- Repositorio local `/Users/rjara/fuentes/vis-credits-segment-wrapper`.
- `assets/segments.yaml`.
- `internal/core/usecase/credit_available_usecase.go`.
- `filter/evals.go`.
- `clients/process/segment.go`.
- `clients/vehicle_risk_profile.go`.

## Validación

- No existía una nota canónica previa para `vis-credits-segment-wrapper`.
- La nota se creó usando `70-templates/application.md`.
