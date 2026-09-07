---
type: change_log
schema_version: 1
scope: session
created: "2026-08-30"
updated: "2026-08-30"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-30-zcode-glm-5-3-flash-project-stages-recovery-slice2]]"
  - "[[embedded-postgres-maven-dns-timeout]]"
aliases: []
confidence: verified
source_session: DURABLE-PROJECT-STAGES-RECOVERY-SLICE2-EMPTY-RACE-CORRECTION-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-30-project-stages-recovery-slice2-empty-race-correction-change-log

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` (append-only checkpoint de la correction)
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` (delta de continuidad)
  - `80-agents/journal/agent-runs/2026-08-30-zcode-glm-5-3-flash-project-stages-recovery-slice2-empty-race-correction.md` (created)
  - `80-agents/memory/public/known-error/symphony/embedded-postgres-maven-dns-timeout.md` (updated: mitigación OpenDB per-PID + workaround PG manual con `TEST_POSTGRES_DSN` y DB virgen por invocación)
- **Código (repo externo `xKoRx/symphony` @ master):**
  - Commit `abe19d09a0bafc7ec21abbf54ca136684e202177` "fix(sqx): serialize empty completion with producer authority" (4 archivos, +336/−2; parent exacto `8caa97a`; push OK, `HEAD == origin/master`)
  - `sqx/adapters/registry-postgres/stage_execution.go`, `sqx/adapters/registry-postgres/stage_producer_output.go`, `sqx/adapters/registry-postgres/stage_producer_output_test.go`, `sqx/adapters/registry-postgres/control_plane_integration_test.go`

## Razón

- Correction de control-plane linearizability sobre Slice 2: `RecordSingletonStageProducerOutput` lockeaba la StageExecution sin leer `status` y `CompleteStageExecution` no inspeccionaba `stage_producer_outputs`, de modo que dos interleavings (producer-then-empty y empty-then-producer) podían terminar en el estado contradictorio `COMPLETED []` + producer row. El invariante (`COMPLETED EMPTY ⇒ 0 producer rows`; producer row ⇒ stage no terminó EMPTY) exige exclusión dentro de la misma transacción PG que controla el lifecycle — un recheck a nivel aplicación sería TOCTOU.

## Efecto

- `PROJECT_STAGE_RECOVERY_SLICE2: PASS / CLOSED` con la correction como parte del slice: gate RUNNING-exclusivo en el singleton (terminal ⇒ CONTRACT_CONFLICT, incluido exact replay; PENDING excluido por evidencia: ResolveStageExecution persiste siempre RUNNING), empty-completion gate serializado a nivel PG (replay sobre estado inconsistente sembrado ⇒ fail closed, nunca ACK), lock order StageExecution→producer outputs en ambos paths, linearizability demostrada con carrera concurrente PG real (XOR de ACK, estado inválido imposible), generic `RecordStageProducerOutput` de Apply intacto, sin schema/migration/storage/ProjectActivity. Delta de suite completa vs baseline `8caa97a` en worktree hermano: VACÍO. Siguiente exacto: DURABLE-PROJECT-STAGES-RECOVERY-FAULT-CERTIFICATION-NORMAL.
