---
type: change_log
scope: session
created: "2026-06-29"
updated: "2026-06-29"
area: "[[Personal]]"
project: "[[Symphony]]"
application: "[[Echo Forge]]"
entities:
  - "[[Symphony]]"
related: []
aliases: []
confidence: verified
source_session: "8e111370-744b-4d70-8c21-e2ed84e0d2d9"
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/echo-forge
  - app/echoforge
  - area/personal
  - kind/changelog
  - project/symphony
  - scope/session
---
# Echo Forge WFM Strategies Discard Change Log

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `sqx/activities/worker/verify_wfm.go`
  - `sqx/activities/worker/evaluate_wfm.go`
  - `sqx/workflows/generic_workflow.go`
  - `sqx/cmd/sqx-worker/main.go`
  - `deploy/manifest.json`

## Motivo

- Evitar que Temporal se atasque en bucles infinitos de reintento para las actividades `verify_wfm_extracted` y `evaluate_wfm` cuando una estrategia es descartada legítimamente en la optimización WFM (y por ende no existe su matriz en MongoDB).

## Fuentes usadas

- Checkpoint anterior y base de código de Symphony.

## Resolución aplicada

- Si la matriz no se encuentra en MongoDB y la importación de la Wave ya terminó con éxito, `VerifyWFMExtractedActivity` retorna `nil` y `EvaluateWFMActivity` retorna un veredicto `"FAIL"` grácil.
- Implementamos una resolución por fuerza bruta de hashes SHA256 de claves `wfm_run_key` para obtener la `wave_key` cuando el payload JSON provenga de la versión anterior de Temporal sin este campo.

## Validación

- Se ejecutaron los tests unitarios e integrados locales con éxito (`go test ./sqx/...`).
- Se preparó el release compilado de la versión `0.1.32`.
- Se desplegó e inició exitosamente el worker `0.1.32` en el servidor Zeus.
