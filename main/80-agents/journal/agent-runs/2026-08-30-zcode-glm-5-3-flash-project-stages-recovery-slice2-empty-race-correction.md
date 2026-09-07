---
type: agent_run
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
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
model_source: builtin:zai-coding-plan/GLM-5.3-Flash
task_type: coding
task_complexity: high
outcome: success
verification: verified
evaluator: agent
user_rework: unknown
source_session: DURABLE-PROJECT-STAGES-RECOVERY-SLICE2-EMPTY-RACE-CORRECTION-NORMAL
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-08-30-zcode-glm-5-3-flash-project-stages-recovery-slice2-empty-race-correction

## Trabajo

- **Objetivo:** cerrar la carrera residual producer-vs-empty sobre `xKoRx/symphony` @ `8caa97a`: `RecordSingletonStageProducerOutput` sin gate de lifecycle y `CompleteStageExecution` sin inspección de `stage_producer_outputs` permitían terminar en `COMPLETED []` + producer row (dos interleavings). Correction exclusiva de control-plane linearizability: sin reimplementar Slice 2, sin storage, sin ProjectActivity, sin recovery state machine, sin producer context digest, sin schema/migration.
- **Alcance atribuible a esta combinación superficie×modelo:** confirmación material del defecto en código, investigación PENDING (ResolveStageExecution es el único writer de inserts y siempre persiste RUNNING ⇒ gate RUNNING exclusivo), rechazo razonado de exact-replay-en-COMPLETED (el recovery de COMPLETED ocurre vía StageExecutionResults; ningún path productivo llega a record en terminal), Correction A (locked read recupera `status`, terminal ⇒ `CONTRACT_CONFLICT`, ni insert ni ACK-as-replay), Correction B (gate de existencia dentro de la misma tx bajo el mismo lock, antes de aceptar cualquier EMPTY completion, incluido replay COMPLETED [] con row existente ⇒ fail closed), lock order documentado (StageExecution row → producer outputs en ambos paths), y 8 tests nuevos + adaptación de 3 existentes al gate.
- **Artefactos afectados:** 4 archivos (budget 4/6): `registry-postgres/stage_execution.go` (+18), `registry-postgres/stage_producer_output.go` (+30/−2), `registry-postgres/stage_producer_output_test.go` (+58), `registry-postgres/control_plane_integration_test.go` (+230). Commit `abe19d09a0bafc7ec21abbf54ca136684e202177` (parent exacto `8caa97a`, push OK, `HEAD == origin/master`).

## Evidencia

- **Validaciones ejecutadas:** tests A–I del mandato PASS — A producer-then-empty (conflicto, RUNNING, 1 row), B empty-then-producer (conflicto, COMPLETED [], 0 rows, replay vacío ACK preservado), C carrera concurrente PG real (6 iteraciones + 10 réplicas; XOR de ACK por iteración; `NOT(COMPLETED [] AND rows>0)` asertado por iteración; ambos órdenes de linearización aceptados), D producer tras COMPLETED non-empty (conflicto, 0 rows), E FAILED/CANCELLED vía fixture aislada (conflicto, 0 rows), F path non-empty normal PASS (record + `[EvaluationRef]` ⇒ COMPLETED, 1 row, 1 result), G replay empty sin producer ACK (test preexistente + fold en B), H estado inconsistente sembrado `COMPLETED []` + row vía SQL de fixture aislada ⇒ replay `CONTRACT_CONFLICT` sin ACK, I regresión genérica Apply intacta (`InsertOnceAndExactReconcile` PASS sin cambios). Targeted misión `-run 'StageProducerOutput|CompleteStageExecution'` PASS 62s; suites steps 0.7s / worker 9.9s / storage-minio 1.2s PASS; compile sweep `./sqx/...` (sin tools) exit 0; vet registry-postgres PASS.
- **Resultado observable:** commit `abe19d0` en origin/master; la suite completa de registry-postgres bajo scratch-DSN produce exactamente el MISMO set de 4 fallos con y sin el diff (delta vacío demostrado con worktree hermano en `8caa97a` + DBs vírgenes por invocación): 1 ajeno documentado (`TestUpsertStrategyV2_V0V1V2Coexistence`) + 3 ambientales del cluster Strategy Identity bajo DSN compartido, todos pre-existentes ⇒ cero regresión causal.
- **Limitaciones de la evidencia:** sin E2E físico ni fault certification (mandato: primero cerrar la race; NEXT EXACT es la fault certification); el modo DSN-scratch difiere del harness efímero per-PID canónico en el cluster Strategy Identity (3 fallos idénticos en baseline, fuera de alcance); `sqx/workflows` 24 fixtures y `sqx/tools` no reabiertos (baseline ajeno).
- **Hallazgo de entorno a reportar:** `postgrestest.OpenDB` usa cache per-PID (`sqx-embedded-postgres-<pid>`) que el cache pre-poblado 2026-08-29 no cubre (eso cubre sólo `OpenIsolatedDB`) ⇒ bajo el bloqueo DNS LAN los tests de `newControlPlane` no pueden arrancar ephemeral; workaround validado: PG manual desde el `.txz` cacheado (`initdb`+`pg_ctl`, binarios mínimos sin `psql`/`createdb` ⇒ DSN contra la DB default `postgres`) + `TEST_POSTGRES_DSN`, creando DB VIRGEN por cada invocación de `go test` (las claves deterministas de los fixtures persisten y contaminan conteos/uniques entre corridas). Registrado en [[embedded-postgres-maven-dns-timeout]].

## Evaluación

%% Scores opcionales 1–5: agregar al frontmatter sólo cuando exista evidencia suficiente. Si son autoevaluados, conservar evaluator: agent. %%
