---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
  - "[[Echo Forge — F-02 Finalist Model V2 Contract]]"
  - "[[Echo Forge — F-03 SQX Long-Running Contract]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
last_verified: "2026-09-16"
confidence: verified
aliases:
  - F-05-I SPEC
  - release matrix and read surface contract
  - Echo Forge F-05-I
related:
  - "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
  - "[[Echo Forge — Factory V2 Completion]]"
entities:
  - "[[Echo Forge]]"
  - "[[xKoRx/symphony]]"
tags:
  - kind/resource
  - area/echo
  - project/echo-forge
created: "2026-09-13"
updated: "2026-09-16"
---

# Echo Forge — F-05-I Release Matrix and Read Surface Contract

Esta Resource es el contrato técnico de `F-05-I — Cohesive release and read surfaces` (preparación de implementación de F-05). Define qué debe quedar cierto. La ejecución vive en [[Echo Forge — F-05-I Cohesive release and read surfaces]]. F-05-I NO publica release, NO ejecuta gates físicos y NO marca ningún T2.11/T2.12/T2.13. Veredicto válido al implementar: `F-05-I IMPLEMENTED / SOURCE VERIFIED`.

Baseline de source: `xKoRx/symphony@b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` (= HEAD de `origin/feature/f04-magic-version-handoff`; release `0.2.98`). Branch de implementación: `codex/f05-release-prep`, creada desde el SHA exacto, nunca desde master ni desde un checkout local divergente (el checkout local del repo puede estar en `9fad768`, que NO contiene C5; la autoridad es el SHA). Contratos frozen inputs: F-01/F-02/F-03/F-04, S0 Echo, B1A/B1B/B2.

`DATABASE MIGRATION: NONE`. Toda la superficie es read-only sobre tablas/colecciones existentes; cero writes en runtime; cero cambios de schema.

## Síntesis vigente

### Problema

El pipeline V2 termina en FinalistPromotion V2 + Apply + (branch F-04) seal/handoff, y toda esa verdad vive en PostgreSQL/MongoDB/MinIO/Temporal, pero no existe ninguna superficie de consulta: `forge.Service` (result v1/v2) y `ControlPlane.LoadForgeCampaignResult` no tienen callers productivos; no hay HTTP/API/GraphQL/Hasura; `sqx-flowkit` sólo hace `push-output`; y la inspección real del owner pasa por `sqx/tools/*.go` (scripts `go run` con hosts hardcodeados) o SQL manual. Además, el estado release/certificación por capacidad vive disperso en notas y no en un artefacto determinístico.

### Veredicto central

**Capas, no un producto nuevo:**

```text
PostgreSQL/MongoDB authorities (existentes, intocables)
→ narrow read ports (capabilities, read-only, nuevas)
→ read services + proyección funnel (core/forge + core/releasematrix, puras)
→ CLI JSON determinístico (subcomandos sqx-flowkit inspect)
→ release matrix (artefacto repo + validador)
→ handoff F-05-C (checklist + manifest template + contrato read-surface)
```

- **Arquitectura elegida: CLI JSON sobre la librería existente.** No se crea servidor HTTP (auth/deploy es territorio F-05-C+/front), no se toca `internal/di` (flowkit ya trae Postgres/etcd/telemetry; Mongo se bootea con `sharedmongo.New` igual que `sqx/cmd/sqx-worker/persistence.go`), no se duplican authorities. El contrato JSON versionado ES el backend contract que el futuro front consumirá envolviendo los mismos read services.
- **Release matrix = declaración validada, no segunda autoridad.** Vive como artefacto versionado en el repo (`deploy/release-matrix.json`) + validador puro (`sqx/core/releasematrix`). La autoridad de release sigue siendo `deploy_release.sh`/`release-authority`/stager; la matriz declara estados con evidencia y jamás deriva un estado de otro.
- **Funnel = proyección pura sobre stage_executions.** Topología V2 dinámica: los boundaries son los `stage_key` realmente ejecutados (stages omitidos no aparecen; stages repetidos agregan). Cero hardcode builder→…→handoff.
- **Zero finalists es resultado válido** (`STRUCTURAL_EMPTY`/`TOP_PROJECTION_EMPTY`, ranking `NOT_MATERIALIZED`), nunca error de software.

### Alcance exacto (in scope)

1. Read ports nuevos (sólo lecturas): listado de campañas (paginado determinístico), stage executions por FlowRunRef exacto, participaciones por FlowRunRef/StrategyRef, versiones/manifests/entregas por StrategyRef.
2. Read services: campaña (`LoadForgeCampaignResult` existente), flow run (`forge.Service.Result` existente, finalmente cableado a un caller), inspección de estrategia (identidad + magic + versiones + handoff por refs exactos), timeline de stages + funnel projection.
3. CLI `sqx-flowkit`: subcomandos `campaign get|list`, `run get|stages`, `strategy get`, `release-matrix`; salida JSON versionada a stdout; exit codes por error kind; `push-output` queda byte-idéntico en comportamiento.
4. Release matrix: paquete `sqx/core/releasematrix` (schema `sqx-release-matrix.v1`), artefacto `deploy/release-matrix.json` con las capacidades F-01…F-04 + pipeline + release pipeline, estados implementada/verificada/released/deployed/certificada-física/cross-lane independientes con evidencia.
5. Handoff F-05-C: `docs/echo-forge/f05-read-surface.md` (contrato JSON/commands/semántica), `docs/echo-forge/f05-conformance-checklist.md`, `docs/echo-forge/f05-certification-manifest-template.json`.
6. Tests: unit/contract/persistence/BWC/negative + race + vet según matriz del proyecto.

### Out of scope (prohibido en F-05-I)

- Marcar PASS cualquier gate físico (T2.11/T2.12/T2.13, E-04 T21/AC-37, Windows/MT5, FULL golden).
- Publicar release (`release-authority`, `deploy_release.sh`, MinIO publish, stager).
- Fabricar golden real o usar fixtures sintéticas como evidencia CERT.
- Frontend, SQX viewer `-gui`, edición de estrategias, HTTP server, GraphQL/Hasura.
- Writes a cualquier DB (incluida Echo), nuevas tablas/columnas/migrations, backfills.
- Reabrir semántica F-01…F-04/S0/B1A/B1B/B2/Magic V1/Finalist V2/HandoffManifestV1.
- Exponer evidencia Mongo secundaria (databank/wfm/deviation/export_runs) — documento como no-superficie de F-05-I.

## Release matrix contract (`sqx-release-matrix.v1`)

- **Dónde vive:** artefacto `deploy/release-matrix.json` (declaración humana/NORMAL, versionada en git) + validador `sqx/core/releasematrix` (parseo, validación estructural, clasificación) + superficie `sqx-flowkit release-matrix` (imprime el JSON validado). No runtime-generated, no segunda autoridad de release.
- **Filas = capacidades** (mínimo): F-01 identity; F-02 Finalist V2; F-03 SQX long-running; F-04 magic allocation; F-04 StrategyVersion seal; F-04 handoff+delivery; pipeline core (ForgeCampaign+GenericSQX workflows); WFM evaluator; global ranking; robust selection; apply selected run; MT5 reconcile+score shadow; B1A/B1B/B2 (histórico CLOSED con SHA/release de época); release pipeline (deploy_release/release-authority/stager); F-05-I read surface (sí misma).
- **Campos por capability:** `capability`, `contract_refs[]`, `producer_paths[]` (paths clave, no wildcard), `persistence_authority`, `read_surface`, `required_refs[]`, `implementation_sha`, y `states` con UNA entrada independiente por dimensión: `implemented`, `source_verified`, `released`, `deployed`, `physically_certified`, `cross_lane_certified`.
- **Estados por dimensión:** objeto `{status: DONE|OPEN|DEFERRED|NOT_APPLICABLE, evidence: string, gate?: string}`. El validador chequea estructura y presencia, y **prohíbe derivar**: nunca exige ni infiere implicación entre dimensiones (p.ej. released NO implica deployed). Guard test negativo: el artefacto committed NO contiene `physically_certified.status=DONE` ni `cross_lane_certified.status=DONE` (en F-05-I todo eso es OPEN/DEFERRED con gate del backlog CERT-*).
- **Orden determinístico:** capabilities ordenadas por `capability` ascendente; JSON marshaling estable.
- **Contenido de verdad inicial** (desde [[Echo Forge — Factory V2 Completion]]): F-04 = implemented/source verified `b57bfb2` + released `0.2.98` + deployed linux PASS/windows OPEN + physical DEFERRED (CERT-F04-01/02/03) + cross-lane DEFERRED (CERT-E04-01). F-01/F-02/F-03 CLOSED con SHAs históricos y release de época; sus dimensiones físicas históricas declaradas con evidencia de época, sin re-certificar.

## Read surface contract

### Comandos y documentos (todos JSON a stdout, `schema` obligatorio)

| Comando | Salida | Autoridad leída |
|---|---|---|
| `sqx-flowkit campaign get <ForgeCampaignRef>` | `sqx-forge-campaign-result.v1` (modelo existente) | PG `forge_campaigns*` vía `LoadForgeCampaignResult` |
| `sqx-flowkit campaign list [--limit N] [--cursor C]` | `sqx-campaign-list.v1` (ref, status, created_at; orden `created_at DESC, ref ASC`) | PG `forge_campaigns` (listado presentación; identidad sigue siendo el ref exacto) |
| `sqx-flowkit run get <FlowRunRef> [--ranking name]` | `forge-result.v1|v2` (modelo existente) | PG + Mongo vía `forge.Service.Result` |
| `sqx-flowkit run stages <FlowRunRef>` | `sqx-run-stage-timeline.v1` + funnel embebido | PG `stage_executions`/`flow_run_strategies` |
| `sqx-flowkit strategy get <StrategyRef>` | `sqx-strategy-inspect.v1` | PG `strategies`/`strategy_magic`/`strategy_versions`/`handoff_manifests`/`handoff_deliveries`/`flow_run_strategies` |
| `sqx-flowkit release-matrix` | `sqx-release-matrix.v1` validado | artefacto repo |

- `campaign get`/`run get`/`strategy get` resuelven **sólo por ref exacto**; `list` es paginación de presentación con cursor explícito y nunca define identidad ("latest" no es ref válido y debe fallar `INVALID_ARGUMENT`).
- `strategy get` (shape): identity (strategy_ref, canonical_strategy_id opaco, instrument/direction/timeframe desde la fila durable, logical_type/classification_version si existen), participation[] (flow_run_ref + role, orden determinístico `participated_at, flow_run_ref`), `magic` (objeto `{registry_namespace, magic_decimal, allocation_ref, assigned_at}` o `null` si no hay fila), `strategy_versions[]` (`version_ref, payload_digest, sealed_at`; orden `sealed_at, version_ref`), `handoff[]` (`idempotency_key, payload_digest, wave_key, version_ref, decision_ref, created_at` + `delivery {state, updated_at}`; orden `created_at, idempotency_key`).
- **Provenance:** cada elemento lleva refs durables exactas (FlowRunRef, StrategyRef, DecisionRef, RankingSnapshotRef, ScoreRef, EvaluationRef donde el modelo ya los expone, StageExecutionRef, allocation_ref, version_ref, idempotency_key). Prohibido: lookup por latest, filename como identity, timestamp como join, parse de CanonicalStrategyID, rankings como autoridad de membership. Ausencia opcional = `null` explícito; nunca ref inventada.

### Funnel projection (`sqx-forge-funnel-projection.v1`)

- Input: stage executions de UN FlowRunRef (orden determinístico `(created_at, stage_instance_key)`) + participaciones.
- Output `boundaries[]`: una entrada por `stage_key` observado, ordenada por `(min(created_at) del key, stage_key ASC)`; cada entrada: `{stage_key, executions_total, by_status {PENDING,RUNNING,COMPLETED,FAILED,CANCELLED}, strategy_subjects_seen, strategy_subjects_completed, error_codes[]}`.
- Stages omitidos por el workflow NO aparecen (no zero-fill); stages repetidos agregan bajo el mismo key. Ningún mapeo stage→stage hardcodeado; la topología se lee de los datos.
- El funnel es **projection**: no crea refs, no muta authorities, no redefine membership. Los finalistas/counters de campaña vienen del result/campaign model, no del funnel.
- Zero finalists: `run get` devuelve promotion AVAILABLE con `finalists: []` + reason estructural y ranking `NOT_MATERIALIZED` cuando corresponde; exit 0.

### Error / empty semantics (freeze)

| Caso | Comportamiento |
|---|---|
| Ref malformado / "latest" | `INVALID_ARGUMENT`, exit 2 |
| Run/campaign/strategy ausente | `NOT_FOUND`, exit 4 (exit code nuevo `ExitNotFound = 4`); sin cuerpo parcial |
| >1 snapshot para el ranking autoritativo | `AMBIGUOUS_RESULT` (taxonomía existente de `forge.Service`) |
| Run existe, stage aún pendiente | timeline con stage `PENDING`; jamás se reporta como 0 o ausente |
| Stage fallido | `FAILED` + `error_code`/`error_message` persistidos, sin ocultar |
| Flow terminal sin ranking producido | `NOT_PRODUCED` (válido, exit 0) |
| Ausencia opcional (magic/versiones/handoff pre-F-04) | `null` explícito; ausencia ≠ cero |
| Métrica opcional ausente | omitida (`omitempty`), nunca 0 |
| Zero finalists / zero supply | resultado válido COMPLETED (`STRUCTURAL_EMPTY`), exit 0 |
| Provenance incompleta/contradictoria | `CONTRACT_INCONSISTENCY` (exit 50) con detalle; falla explícita, sin adivinar |
| Historia V1 (policy 1.0.0) | legible vía result v1 path existente; sin coerción a V2 |
| Store caído | `INFRASTRUCTURE_FAILURE`, exit 50 |

- No existe estado `PARTIAL` inventado: la parcialidad se representa con los estados existentes por nivel (campaign FAILED con `failure_code` + waves started/completed; flow COMPLETED con counts; stages con status individual). La ausencia nunca se esconde como cero.
- JSON determinista: sin timestamps de query, marshaling de structs (orden de campos fijo), mismo estado durable ⇒ mismos bytes.

### Exit codes (flowkit, aditivos)

`0` respuesta válida (incluye NOT_MATERIALIZED/zero finalists/NOT_PRODUCED) · `2` INVALID_ARGUMENT · `4` NOT_FOUND (nuevo) · `10` config/DI · `50` CONTRACT_INCONSISTENCY/INFRASTRUCTURE/otros internos. `push-output` conserva sus códigos actuales.

## BWC y preservación

- F-01 identity, F-02 Finalist V2 + result v1/v2, F-03 long-running, F-04 magic/seal/handoff, S0, B1A/B1B/B2: **no-touch semántico**; la superficie sólo los lee.
- `forge.Service`, `LoadForgeCampaignResult`, models `ForgeResult`/`ForgeCampaignResult`: sin cambios de shape; nuevos consumers solamente.
- `sqx-flowkit push-output`: flags, salida y exit codes byte-idénticos.
- Deploy pipeline (`deploy_release.sh`, `deployer/`, `deploy/manifest.json`): intocado.
- Historia V1: legible; nada se reescribe.
- `DATABASE MIGRATION: NONE`. Si la implementación cree necesitar schema: `STOP — MANAGER REVIEW — FROZEN_CONTRACT_COLLISION`.

## Fixtures

- Permitidas: harness `postgrestest` (+ `testdata/brownfield.sql`), fixtures determinísticas existentes, nuevas fixtures de read-surface etiquetadas sintéticas (convención: campo `"synthetic": true` o nombre `*_synthetic_*` en testdata).
- **`fixture != authentic physical golden`:** ninguna fixture satisface gates CERT; los states físicos de la matriz quedan OPEN/DEFERRED.

## Certificación

- **SOURCE/CONTRACT (F-05-I PASS):** matriz de tests del proyecto ([[Echo Forge — F-05-I Cohesive release and read surfaces]]) verde en scope enfocado; BWC push-output; determinismo JSON; negative tests; cero diffs en contratos frozen; `git diff --check`.
- **DEFERRED CERTIFICATION (no bloquea F-05-I):** T2.11/T2.12/T2.13, E-04 T21/AC-37, físico Windows/MT5, FULL golden, release/deploy ⇒ campaña [[Echo + Echo Forge — Deferred Certification Backlog]] (CERT-F05-01…03 tras CERT-F04-*).

## Handoff que F-05-I deja a F-05-C

1. `deploy/release-matrix.json` validado (estados por capacidad con evidencia; campos físicos OPEN/DEFERRED).
2. `docs/echo-forge/f05-read-surface.md`: contrato de read surface (esquemas JSON, comandos, error/empty semantics) — base para el front futuro sin acceso directo a DB.
3. `docs/echo-forge/f05-conformance-checklist.md`: checklist de conformance para la campaña (qué verificar por superficie, con refs).
4. `docs/echo-forge/f05-certification-manifest-template.json`: template del manifest de certificación con campos físicos explícitamente vacíos (`null` + `"status": "OPEN"`); F-05-C los llena con evidencia real, F-05-I no inventa valores.

## Invariantes / STOP

STOP — MANAGER REVIEW si: se requiere modificar F-01…F-04/S0/B1A/B1B/B2 o cualquier schema DB (migration ≠ NONE); se quiere publicar release o tocar el pipeline deploy; se exige HTTP server/auth; la baseline `b57bfb2` desaparece o `origin/feature/f04-magic-version-handoff` avanza materialmente (`BASELINE_MOVED`); un test verde depende de mocks presentados como evidencia física; el funnel necesita hardcodear stages; alguna read surface escribe.

`GOD REQUIRED: NONE`.

## Evidencia y provenance

- Inspección read-only `xKoRx/symphony@b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` (2026-09-13).
- Read models sin callers: `sqx/core/forge/result.go` (`forge.Service`, taxonomía INVALID_ARGUMENT/NOT_FOUND/AMBIGUOUS_RESULT/CONTRACT_INCONSISTENCY/INFRASTRUCTURE_FAILURE; `NOT_MATERIALIZED` zero-supply), `sqx/core/forge/campaign_result.go` (`VerifyForgeCampaignResult`, estados PENDING/RUNNING/COMPLETED/FAILED/CANCELLED), `sqx/adapters/registry-postgres/forge_campaign_result.go`, `flow_run_result.go` (`FlowRunResultReader`), `stage_execution.go` (`LoadStageExecution*`), `decision_store.go` (`LoadDecision`, `LoadFinalistPromotion`), `strategy_version.go` (`LoadStrategyVersion`, `LoadHandoffManifest`, `LoadHandoffDelivery`), `magic_allocation.go` (`LoadMagicAllocation`), `strategy_manifest_identity.go` (fila durable instrument/direction/timeframe).
- Ports existentes: `sqx/core/capabilities/forge_result_query.go` (`FlowRunResultReader`, `FinalistPromotionResultReader`, `GlobalRankingSnapshotQuery`); Mongo impl `sqx/adapters/metadata-mongo/ranking_snapshot_query.go`; `LoadEvaluation` en `capabilities/persistence.go`.
- Cero HTTP/GraphQL/Hasura en `sqx/` (`git grep` baseline). CLI actual: `sqx/cmd/sqx-flowkit/main.go` sólo `push-output`. Tools informales: `sqx/tools/{inspect_selected_runs,list_minio,query_mongo,find_minio_keys,inspect_etcd,insert_metadata}.go`.
- Authorities: PostgreSQL `sqx` schema (flow_runs, flow_run_strategies, stage_executions+results, decisions+evidence, strategies, stage_producer_outputs, output_namespace_ownership, forge_campaigns/waves/finalists/stop_evaluations, strategy_magic, strategy_versions, handoff_manifests, handoff_deliveries, magic_instruments, magic_monthly_counters; migrations 001–016); MongoDB db `forge` (databank_metadata, wfm_matrices, strategy_state, type_rankings, wave_reports, mt5_backtest_results, export_runs, deviation_results, ranking snapshots); MinIO `sqx-strategies` + buckets deploy; Temporal correlation columns en flow_runs/stage_executions/forge_campaigns; etcd coordinación.
- Wiring sin `internal/di` changes: patrón `sharedmongo.New(di.Container.Etcd, di.Container.Telemetry)` + `registrypostgres.NewControlPlaneFromClient(deps.PostgresClient)` de `sqx/cmd/sqx-worker/persistence.go`; flowkit ya invoca `di.InitSelective` con Postgres/etcd/telemetry.
- Estados/semánticas existentes reutilizadas sin invención: LifecycleStatus (domain/control_plane.go), ranking/promotion statuses (domain/forge_result.go), ScoreStatus NOT_COMPARABLE/INVALID_INPUT, warnings PERIOD_MISMATCH/FIDELITY_NOT_COMPARABLE/PNL_SIGN_FLIP, STRUCTURAL_EMPTY/TOP_PROJECTION_EMPTY, failure/cancel reason enums (migration 011).
- Release surfaces existentes: `deploy/manifest.json`, `deploy_release.sh`, `deployer/cmd/release-authority` (`sqx-release-authority.v1`), `deployer-watcher`, stager.

## Límites y contradicciones

- `campaign list`/pagination es presentación: si el owner quiere "la campaña actual", eso sigue siendo decisión humana sobre refs exactos; la superficie no resuelve identidad por recencia.
- La matriz declara estados; no los ejecuta ni los audita automáticamente. Su verdad es la evidencia referenciada.
- El funnel no afirma "supervivencia entre boundaries" como dato durable; expone counts por boundary. Las transiciones son lectura del consumidor (presentation ≠ authority).
- La superficie Mongo de ranking es la ya usada por `forge.Service`; databank/wfm/deviation quedan fuera y su exposición sería un cambio de scope aparte.
