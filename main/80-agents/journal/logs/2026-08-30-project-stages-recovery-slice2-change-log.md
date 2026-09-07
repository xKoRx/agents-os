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
  - "[[2026-08-30-durable-retester-optimizer-recovery-rca]]"
  - "[[2026-08-30-zcode-glm-5-3-flash-project-stages-recovery-slice1]]"
aliases: []
confidence: verified
source_session: DURABLE-PROJECT-STAGES-RECOVERY-SLICE2-PRODUCER-OUTPUT-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-30-project-stages-recovery-slice2-change-log

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` (append-only checkpoint Slice 2)
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` (delta de continuidad)
  - `80-agents/journal/agent-runs/2026-08-30-zcode-glm-5-3-flash-project-stages-recovery-slice2.md` (created)
  - `80-agents/journal/feedback/system-1/2026-08-30-project-stages-recovery-slice2-session-feedback.md` (created, pedido explícito del owner)
- **Código (repo externo `xKoRx/symphony` @ master):**
  - Commit `8caa97a9471d433a6a520d76af315a7c4f4dd4ce` "fix(sqx): seal project producer output before upload" (12 archivos, +1504/−22; parent `9945f85`; push OK, `HEAD == origin/master`)
  - `sqx/core/capabilities/persistence.go`, `sqx/core/capabilities/storage.go`, `sqx/adapters/registry-postgres/stage_producer_output.go` + test, `sqx/activities/worker/pipeline/step.go`, `sqx/activities/worker/project_activity.go`, `sqx/activities/worker/steps/steps.go`, `sqx/activities/worker/steps/project_stage_recovery.go` + test, `sqx/adapters/storage-minio/minio_storage.go`, `sqx/adapters/storage-minio/durable_artifacts.go`, `sqx/adapters/storage-minio/pre_put_test.go` (nuevo)

## Razón

- Implementación de Slice 2 de la decisión [[2026-08-30-durable-retester-optimizer-recovery-rca]]: cerrar W5 (upload iniciado / commit desconocido) y W6 (objeto aceptado por MinIO sin Evaluation) sellando la autoridad existente `sqx.stage_producer_outputs` ANTES de cualquier PUT. SINGLETON GATE resuelto POSSIBLE (el naming físico publicado depende de HOST_KEY — congelado por test del propio repo — y el binario SQX está fuera del repo), por lo que la exclusión de autoridad se garantiza con un comando transaccional nuevo que lockea la fila StageExecution en vez de un check-then-insert por (stage,key); el contrato genérico de Record para Apply queda intacto.

## Efecto

- `PROJECT_STAGE_RECOVERY_SLICE2: PASS / CLOSED`; W5/W6 cubiertos (record-before-put + ListByStage + recovery RUNNING+producer con probe exact/missing/transient/mismatch); precedencia Results > Evaluation > Producer > físico preservada; sin schema/migration/SDK, write-once intacto, Builder sin cambios. Falta certificación de fault/retry en sesión separada para declarar `PROJECT_STAGE_RECOVERY: CERTIFIED_CLOSED / FROZEN`.
