---
type: change_log
schema_version: 1
scope: session
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-29-exporter-double-execution-root-cause]]"
  - "[[2026-08-29-zcode-glm-5-3-flash-exporter-hop-removal-correction]]"
aliases: []
confidence: verified
source_session: DURABLE-VERIFIED-READS-EXPORTER-HOP-REMOVAL-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-29-exporter-hop-removal-correction-change-log

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):** `sqx/activities/worker/steps/steps.go` (reubicación del side-effect legacy en `ImportMetadataStep`), `sqx/activities/worker/steps/steps_test.go` (Tests A/B + fail-closed), `sqx/activities/worker/steps/steps_builder_evidence_test.go` (fixtures `looseMetadataWriter()` ×3), `sqx/workflows/generic_workflow.go` (helper puro `shouldSkipLegacyOverviewExporter` + bypass durable V1), `sqx/workflows/generic_workflow_overview_exporter_test.go` (nuevo; Tests D/E/F + unit helper). En [[xKoRx/symphony]]: commit `e241dd9`, parent `1f0880c`, push `origin/master`, `HEAD == origin/master`.
- **Archivo(s) Agents OS:** checkpoint del proyecto [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]], nota interna [[agents-os-operating-continuity]], agent run [[2026-08-29-zcode-glm-5-3-flash-exporter-hop-removal-correction]], este change log.

## Motivo

- Ejecutar la corrección aprobada por el RCA [[2026-08-29-exporter-double-execution-root-cause]]: la tarea `overview_exporter` top-level es at-least-once con artefactos byte-no-deterministas sobre keys write-once ⇒ retry legítimo produce `CONTRACT_CONFLICT`; el Builder durable debe ser el único productor físico del overview metadata y heredar el side-effect legacy de `StrategyMetadata` (sin el marcador `ExportRun`, sin consumidor material).

## Fuentes usadas

- Source de `symphony` @`1f0880c`: `steps.go` (lógica `skipLegacyDatabank`, parseo NDJSON, `durableBuilderCaps`), `generic_workflow.go` (scheduling `project`/`overview_exporter`, `flowRunWritebackEnabled`), `config.go` (predicados durables), `project_activity.go` (`enableMetadata`), `sqx-worker/main.go`+`persistence.go` (inyección `metaWriter`/`Evidence`), configs `input/example/`.

## Resolución aplicada

- Builder durable: `SaveStrategyMetadataBatch` EXACTAMENTE ONCE, `SaveExportRun` ZERO, fail-closed sin `MetadataWriter`; stages durables no-builder siguen suprimidos; path legacy/no-durable preservado; bypass del exporter top-level sólo en durable V1 con Builder demostrado en el mismo spec (decisión pura determinística, sin DB/MinIO/clock); `wfm_exporter` intacto; GroupSQXWorkflow fuera de alcance.

## Validación

- Tests A–F nuevos PASS; suites `sqx/activities/worker/steps`, `sqx/activities/worker`, `sqx/cmd/sqx-worker` y compile sweep (excl. `sqx/tools`) PASS; `./sqx/workflows` conserva exactamente los 24 failures preexistentes del baseline puro `1f0880c` (demostrado con worktree hermano limpio; root cause: fixtures sin mock `flow_run_start`, no causal).

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert e241dd9` en `symphony` restaura el comportamiento previo (el bypass es aditivo y sin schema/migración; no hay datos persistentes nuevos).
