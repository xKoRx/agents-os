---
type: change_log
schema_version: 1
scope: session
created: "2026-08-28"
updated: "2026-08-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-28-durable-artifact-verified-reads-slice1b]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-SLICE1B-WFM-APPLY-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-28-durable-artifact-verified-reads-slice1b

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated / deleted / conflict-resolution
- **Archivo(s):**
  - `xKoRx/symphony` commit `ce21d253680fa925d4c9d33e25b39fc0b94519f4`.
  - Apply result/workflow, Final Reretester steps, WFM activity/physical/workflow y tests de contrato/carry.

## Motivo

- Cerrar Slice 1B de verified reads sin reabrir el Artifact Plane write-once: Apply devolvía sólo `ObjectKey`, Final Reretester conservaba fallback key-only y WFM pasaba key-only a la capa física.

## Fuentes usadas

- Baseline Symphony `1e2564062987b7762f29c499b90c1e91522c1a96`, SDK `ea09cc1bb8b34e661c8f31f887dce58613b0475a`, contrato durable existente y pruebas focalizadas del slice.

## Resolución aplicada

- Se añadió `Artifact` exacto al resultado Apply y se validó el carrier antes/después del workflow; Final Reretester y WFM consumen refs durables verificadas; WFM clasifica conflictos de integridad como non-retryable y conserva retry de errores transitorios; survivors preservan Artifact.

## Validación

- PASS: `go test ./activities/worker/...`, `go test ./activities/worker/steps/...`, pruebas focalizadas Apply/WFM/Final Reretester/robust selection, bindings Apply/WFM, `go vet ./activities/worker/...`, `go vet ./workflows/...`, `git diff --check`.
- Broad/workflows: degradado sólo por fallos baseline documentados de fixtures `flow_run_start` no registrado y harnesses preexistentes; no se corrigieron por estar fuera de alcance.
- `HEAD == origin/master == ce21d253680fa925d4c9d33e25b39fc0b94519f4`; foreign dirty preservado.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit `ce21d253680fa925d4c9d33e25b39fc0b94519f4`; no requiere rollback de schema, migración ni storage.
