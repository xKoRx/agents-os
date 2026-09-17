---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
application: "[[xKoRx/echo]]"
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
related: []
aliases: []
confidence: verified
source_session: "2026-09-17 E-06 WP-B corrección C1"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-17-echo-e06-wpb-c1-correction-logged

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` (estado, tabla de entrega, bitácora)
  - repo `xKoRx/echo` @ `cdb0c163`: `v3/gateway/internal/reference_binding_handler{,_test}.go`, `v3/sdk/postgres/reference_binding_store{,_test}.go`, `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/{TASKS,VERIFICATION}.md` (commit `cdb0c163`, push FF `cd2aca67..cdb0c163` sobre `feature/e06-reference-enrollment-binding`)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-e06-wpb-c1-correction.md` (nuevo)

## Motivo

- **Corrección C1 de la auditoría Manager sobre NORMAL WP-B (T05/T06):** C1-1 `proof.recorded_at` pasa a sello server-side del Gateway (400 ante presencia en el proof; replay conserva el original sin fabricar CONTRACT_CONFLICT); C1-2 el primer ACK revalida `client_account_role=reference` del catálogo (404/409/503 sin mutación; replay de ACK committeado idempotente); C1-3 outcome CREATED/REPLAY atómico del INSERT vía `InsertPreparedWithOutcome` (UNIQUE PostgreSQL como única autoridad; 201+200 concurrente); C1-4 fallo operacional del lookup de Version en el ACK ⇒ 503 UNAVAILABLE retryable y no 400 INVALID_INPUT.

## Fuentes usadas

- Misión Manager E-06 (contratos C1-1…C1-4, tests obligatorios, allowed files, prohibiciones)
- SPEC v1.2.2 §5.5/§8/§13/§14/§17.1 (congelado); baseline `cd2aca6` (parent `1614028b`, merge-base `5dd998f1`)
- Handoff WP-B en la nota del proyecto (estado `E06_WPB_READY_FOR_MANAGER_REVIEW`)

## Resolución aplicada

- Delta exacto: 4 archivos productivos allowed + TASKS/VERIFICATION; SPEC, migration 064, contracts, 061–063, Bridge, MQL, core, Hasura, ClientConfig, server.go, Forge, master: sin cambios; `go.mod`/`go.sum` delta 0; WP-B ya aceptado no reabierto; T08+ no iniciado.
- Goldens §17.1 recalculados por el fixture sin `recorded_at` y verificados byte-exacto contra el canonical real con herramienta independiente.

## Validación

- PG REAL 17.11 descartable: `run.sh` PASS ×2; Go E-06 17/17 `sdk/postgres` + 22/22 `gateway/internal` con `-race`; `sdk/domain` PASS plain/race; vet OK; builds sdk/gateway/bridge OK.
- Regresión: failing set idéntico por nombre al baseline puro `cd2aca6` (29=29 gateway, 53=53 postgres; colateral TC-06-1 + `TestScratch_QueryDB`); skip-mode idéntico.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin paths de máquina sensibles, sin memoria interna

## Rollback

- Revert del commit `cdb0c163` en la branch feature (FF hacia atrás) y revertir las tres notas del vault si el Manager rechaza la corrección.
