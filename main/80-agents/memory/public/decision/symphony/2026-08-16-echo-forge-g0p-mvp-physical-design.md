---
type: decision
schema_version: 1
scope: application
created: "2026-08-16"
updated: "2026-08-16"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
related:
  - "[[2026-08-15-echo-forge-g0l-owner-amendments]]"
  - "[[2026-08-16-echo-forge-mvp-physical-design]]"
aliases:
  - Echo Forge G0-P physical design
  - Echo Forge persistence MVP decision
confidence: verified
source_session:
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - app/echo-forge
  - application/echoforge
  - area/echo
  - project/echo-forge
  - tech/symphony
---

# Decision — Echo Forge MVP physical design G0-P

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- G0-L aprobó entidades, ownership y bindings, pero dejó abiertas las formas físicas, idempotencia, recovery y compatibilidad brownfield que bloqueaban G1-MT5.
- Symphony `b5c71d5` ya usa `sqx.strategies`, aggregates Mongo mutables/overwrite, ArtifactRef incompleto y Temporal IDs heterogéneos; A1 debía proponer un slice incremental sin big bang.
- Un primer cierre de G0-P/G1-MT5 se invalidó por no resolver de forma suficiente la frontera SDK/Core/adapter, las shapes exactas, el linkage de resultados y la matriz completa de recovery. Esta decisión registra la versión corregida que lo supersede.

## Decisión

1. Reutilizar `sqx.strategies.id` como `strategy_ref`. FlowRun usa UUID + `sha256(config_id,flow_intent_token)` con token globalmente unique y atestado `flow-intent.v1`; reutilizarlo con otro config/intent es `CONTRACT_CONFLICT`. StageExecution usa UUID + slot hash de task/stage/subject/inputs y execution hash de FlowRun/slot/generation. Evaluation, MetricSet, TradeSet y Score usan refs SHA-256 deterministas.
2. Persistir `flow_runs`, `flow_run_strategies`, `stage_executions` y `stage_execution_results` en PostgreSQL; extender `sqx.strategies` aditivamente. La unique StageExecution es `(flow_run_id,stage_instance_key,generation)`. `is_origin=true` exige `PRODUCED` o `IMPORTED`; `is_origin=false` exige `REUSED` o `REPROCESSED`.
3. Persistir evidence inmutable solo en `evaluations`, `metric_sets`, `trade_sets` y `scores`; externalizar trades a MinIO NDJSON gzip y embeber ArtifactRefs/bindings acotados. RankingSnapshot y Decision quedan fuera de G1-MT5/M4 y no reciben stores nuevos.
4. Mantener contratos nuevos en `sqx/core/domain`, scoring puro en `sqx/core/evaluation`, ports en `sqx/core/capabilities` y DTOs privados en los adapters existentes. El SDK `pkg/sqx` queda legacy sin cambios porque no se demostró consumidor externo del nuevo contrato MVP.
5. Exigir en las collections evidence v1 write concern `majority+journal`, recovery read `majority+primary`, context deadline y outcome `UNKNOWN_COMMIT`; la configuración legacy sin concerns explícitos no se hereda como garantía.
6. Ejecutar una saga recuperable FlowRun/StageExecution→MinIO→Mongo→legacy projection→`stage_execution_results`/CAS. `v1_shadow` registra projection receipts; rollback normal a `legacy` exige drain, reconciliation y cero estados `PENDING` o `GAP` hasta el cutoff.
7. Aceptar A1 como `APPROVED_WITH_FINAL_AMENDMENTS`, cerrar `G0-P = MVP_PHYSICAL_DESIGN / CLOSED` y `G1-MT5 = APPROVED / CLOSED`, y congelar el diseño hasta evidencia de A2/G2.

## Rationale

- Control plane necesita constraints/transacciones; evidence necesita append-only/recompute; bytes grandes no caben de forma segura en BSON ni Temporal history.
- Separar intent key de la referencia operacional distingue retry de rerun; usar refs de evidence deterministas permite recuperar un commit Mongo incierto y detectar payload conflicts por digest.
- Separar el slot StageExecution de `generation` conserva idempotencia del retry y permite g2 dentro del mismo FlowRun sin colisión SQL.
- Distinguir `is_origin` de participation role permite responder primera entrada producida/importada sin tabla adicional.
- Collections nuevas evitan el índice contradictorio de `strategy_evaluations`, el overwrite de `mt5_backtest_results` y un backfill que invente origen.
- El scope mínimo no necesita ranking ni decisiones para persistir Score shadow. Diferirlos evita diseñar lifecycle, cohort assembly e índices sin una query consumidora de M4.
- Los packages Core/adapters existentes ya contienen el worker, dominio y stores del vertical; mover los tipos al SDK ampliaría el contrato público sin evidencia de consumo.

## Consecuencias

- A2-TOP implementa migrations/control boundaries y recovery; A2-NORMAL agrega DTOs/repositories/wiring dentro del contrato cerrado.
- MT5 continúa M0–M3 y adopta el diseño recién en M4; shadow crea Score pero no RankingSnapshot, Decision ni invalidación.
- Rollback cambia flags a `legacy`; las filas, collections y artifacts v1 permanecen auditables y las stores brownfield no se destruyen.
- El cambio normal a `legacy` puede quedar bloqueado por projection gaps; no se declara rollback exitoso si readers legacy ocultarían evidence reciente.
- El detalle implementable de formulas, shapes, índices, packages, recovery, rangos y conformance permanece en [[Echo Forge - Arquitectura de Datos y Migración de Persistencia#A1 — PHYSICAL MODEL v1]].

## Alternativas descartadas

- Usar Wave, Temporal RunID, `request_id` legacy aislado o SHA de artefacto como identidad; solo el `flow_intent_token` global atestado participa junto a `config_id`, y su unique independiente detecta reutilización cross-config.
- Reutilizar/renombrar collections legacy como autoridad v1 o hacer big-bang migration.
- Embutir trades en BSON o diseñar RankingSnapshot/Decision dentro del slice shadow sin consumidor requerido.
- Introducir Kafka, outbox, event sourcing o una transacción distribuida en el MVP.
- Esperar p95/p99 y cardinalidades del sistema futuro antes de aprobar el primer diseño físico.
