---
type: change_log
scope: session
created: "2026-07-31"
updated: "2026-07-31"
area: "[[Echo]]"
project: "[[Echo Forge - Trade List Export Contrato Remoto]]"
application: "[[sqx-worker]]"
entities:
  - "[[sqx-worker]]"
related:
  - "[[trade-list-exporter-local-path-cross-worker]]"
  - "[[2026-07-31-temporal-activity-contract-remote-only]]"
confidence: verified
source_session: cursor-2026-07-31-trade-list-remote-contract-design
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Change log — diseño del contrato remoto de trade list (EF-G32)

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Trade List Export Contrato Remoto.md` (created — proyecto de agente y planificador único, plan T1-T8)
  - `10-projects/Echo Forge/agentes/Echo Forge - Cierre de Etapa 4.md` (updated — tarea puente en `[/]` y entrada de bitácora)
  - `80-agents/memory/public/decision/symphony/2026-07-31-temporal-activity-contract-remote-only.md` (created — regla reusable)
  - `80-agents/memory/public/known-error/symphony/trade-list-exporter-local-path-cross-worker.md` (updated — fix esperado → diseño cerrado)
  - `80-agents/memory/internal/agent-memory/2026-07-31-trade-list-upsert-affinity-redesign.md` (updated — continuidad)
  - repo `symphony`: `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` (updated — EF-G32 §10.9, tabla de GAPs y orden de remediación §10.8)
- **Segunda pasada (corrección de rumbo del owner):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Trade List Export Contrato Remoto.md` (updated — D4 y D10 revertidas; nuevas D11/D12/D13; tareas T2b/T2c/T2d; T3 ampliada al adapter y al ciclo de limpieza; T5 con `SetSQXExecBasePath`; T7 con 4 tests nuevos; T8 con barrido de residuos)
  - `80-agents/memory/public/decision/symphony/2026-07-31-storage-path-deterministic-by-logical-identity.md` (updated — extensión: el trade list se alinea con EF-G27; corolario "un adapter no construye rutas")
  - `80-agents/memory/public/decision/symphony/2026-07-31-task-local-dirs-input-output-only.md` (created — contrato de disco local de una task)
  - `80-agents/memory/public/known-error/symphony/trade-list-exporter-local-path-cross-worker.md` (updated — los dos incumplimientos adyacentes viajan en el mismo PR)
  - `80-agents/memory/internal/agent-memory/2026-07-31-trade-list-upsert-affinity-redesign.md` (updated — qué NO reabrir, con la lección de proceso)
  - repo `symphony`: `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` (updated — §10.9.3 key MinIO, §10.9.4 directorios locales, DoD ampliado, título del gap)

## Motivo

- El usuario pidió rediseñar la task de exportar trade lists como arquitecto y
  dejar un plan ejecutable por una IA ligera. El diseño quedó cerrado (activity
  única con contrato remoto) y emergió una regla que aplica a cualquier activity
  de Symphony, no solo a trade list.
- En la revisión, el owner rechazó el naming del artefacto y el tercer directorio
  local. Al verificar, tenía razón en ambos y con un agravante que yo no había
  visto: la key del trade list **contradecía una decisión ya firmada del repo**
  (EF-G27, `BuildMinIOPath` como mecanismo único sin segmentos de ejecución).
  Lección de proceso registrada: antes de defender el statu quo por costo de
  migración, verificar si existe una decisión previa que lo prohíba.

## Fuentes usadas

- `sqx/activities/worker/trade_list_exporter_activity.go`
- `sqx/activities/worker/project_activity.go` (`UpsertTradeList`, `temporalNonRetryable`)
- `sqx/activities/worker/steps/trade_lists.go`, `sqx/activities/worker/pipeline/builder.go`
- `sqx/workflows/generic_workflow.go` (ambos bloques `case "trade_list_exporter"`)
- `sqx/cmd/sqx-worker/main.go` (wiring y registro de activities)
- `sqx/adapters/storage-minio/trade_lists.go`, `sqx/adapters/metadata-mongo/trade_lists.go`
- `sqx/core/capabilities/trades.go`, `sqx/core/runtime/config.go`, `input/example/config.json`
- `specs/FEAT-SQX-TRADE-LIST-METADATA/`, `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10
- `go.temporal.io/sdk v1.35.0` (`NewNonRetryableApplicationError`, `ApplicationError.Unwrap`)

## Notas

- Cero cambios de código productivo en esta sesión.
- Fuentes adicionales de la segunda pasada: `sqx/core/domain/paths.go` (contrato
  de `BuildMinIOPath`), `sqx/core/domain/canonical_strategy_id.go`,
  `sqx/core/capabilities/trade_keys.go` (código muerto),
  `sdk/pkg/sqx/trade_manifest.go` (`TradeArtifactRef.Validate` no restringe la
  key), `sqx/core/runtime/config.go` (`GetSQXPaths`, `CleanProjectDatabanks`,
  `sqxExecBasePath` nunca inicializado en producción).
- Pendiente: reindex Graphify del vault vía `agents-os-graphify-maintenance`
  (se crearon dos decisiones L3 nuevas).
