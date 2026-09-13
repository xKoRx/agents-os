---
agent: echo-functional-cartographer
role: Echo Functional Cartography
task_id: KBC-B
status: COMPLETE
baseline: echo f7ddea18cab51db72c9765aa74381328134d7ce7 (feature/e02-control-safety-journal-recovery, working tree clean) · origin/master a99f9a63354bbe72219d1e590bb93757ed08e45e · vault (no relevante, sólo escritura de este artifact)
inputs: xKoRx/echo (todo el tree, lectura committed); specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2, specs/FEAT-FORGE-INGESTION-E1, specs/SPECS.md; artifact 01-knowledge-architecture.md (handoff)
scope: cartografía funcional Echo read-only (WHAT IS, no WHAT SHOULD BE); distinción explícita IMPLEMENTADO vs EN PROGRESO vs SOLO-SPEC
started_at: 2026-09-12T23:30:00-03:00
updated_at: 2026-09-13T00:20:00-03:00
---

# KBC-B — Echo Functional Cartography

## Assignment

Mapear cómo funciona Echo HOY en el baseline `f7ddea18` (branch `feature/e02-control-safety-journal-recovery`): entrypoints, dominio, persistencia, orquestación, APIs, integraciones, runtime/config, observability, retry/failure/recovery y tests como evidencia. Producción de evidence packs compactos (claim → file → symbol → test → confidence) en este único artifact. READ-ONLY: ninguna mutación del repo ni del vault fuera de este archivo.

## Baseline

- Verificado con `git rev-parse HEAD` al inicio: `f7ddea18cab51db72c9765aa74381328134d7ce7` en `feature/e02-control-safety-journal-recovery`, working tree clean (sin dirty). Coincide exactamente con el baseline de campaña declarado; todo lo citado abajo es estado committed.
- `origin/master` = `a99f9a63354bbe72219d1e590bb93757ed08e45e` ("docs(e04): record controlled integration"); el branch activo está ~8 commits adelantado con la feature E-02.
- Convención de paths: todo path es relativo al repo `xKoRx/echo`; `v3/...` es el árbol activo; `v1/`, `v2/` y raíces `agent/`, `core/` (v1) son generaciones legacy aún presentes en `go.work` (16 módulos, incluidos v1/v2) y en `build_v3.sh` sólo se construye v3 (binarios a `v3/bin/`).
- Últimos commits del branch (contexto de la feature): `cf81a7f0` (quarantine + journalctl), `38eda71b` (PublishSync durable facts), `2b538f1c` (front session actor tokens), `0ff4b04a` (gateway actor auth + durable webhook delivery), más docs E-02.

## Findings

### 1. Entrypoints y callers/callees (IMPLEMENTADO)

- Binarios activos Go (cada uno con `main()` propio, `cmd/` + `internal/`): `v3/core/cmd/echo-core` (Core V3: StateFun HTTP server para Flink + carga de execution policies desde PG + publicación a Kafka `echo.execution-policies.v1`); `v3/gateway/cmd/echo-gateway` (HTTP API, webhooks Hasura→Kafka, boundary Forge, automation, scheduler); `v3/bridge/cmd/echo-bridge` (Windows-only, `//go:build windows`: named pipes MT4/MT5 ↔ Kafka); `v3/lab-worker/cmd/lab-worker` (+ subcomandos `recompute`, `materialize-curves`, `materialize-snapshots`, `job-run-smoke`) y `cmd/lab-materialize-pg`, `cmd/lab-recompute-pg`; `v3/tools/journalctl` (CLI de recuperación de journal: `quarantine list|show|resolve|discard`, `replay-facts`, `stats`; `DATABASE_URL` obligatoria). Confidence HIGH (main.go leídos).
- Binario DEPRECADO: `v3/core/cmd/echo-functions` (`main` marcado "DEPRECATED: Use echo-core instead") — servidor StateFun legacy. Confidence HIGH.
- Toolkit utilitario: `v3/toolkit/cmd/{etcd-check,pg-check,hasura-schema,hasura-lab-smoke,hasura-lab-clean-smoke,hasura-track-thelab,apply-migration,deploy-wizard}`. Confidence HIGH.
- Frontend: `v3/front` (Vue 3 + Vite + Vitest; views `CommanderView`, `LabView`, `OperationsView`, `ShieldView`, `WatchtowerView` + `admin/`); bundle sin admin secret (verificado por `v3/scripts/check-frontend-bundle.sh` y tests front). Confidence HIGH.
- Clientes broker: EAs MQL `v3/clients/mt{4,5}` (`reference_v3.mq4/5`, `execution_agent_v3.mq4/5`, `develop_trade_seed_v3.mq4/5`, librerías `Echo*.mqh`) y DLLs `v3/clients/dll/`. Status Legacy/Implemented según `specs/SPECS.md`. Confidence HIGH.
- Cadena runtime principal: EA (MT5) → named pipe → Echo Bridge → Kafka → Core (Flink StateFun: StrategyConfig → ExecutionPlanner → MMEngine → TradeJournal) → Kafka `echo.core-commands.v1` (topic por cuenta `echo.commands.<account>.v1`) → Bridge → EA de ejecución; Gateway queda fuera del hot path de trading (webhooks + boundary Forge). Confidence HIGH (código + `v3/kafka/README.md`).

### 2. Dominio: modelos, identidad, lifecycle (IMPLEMENTADO, contrato congelado)

- Contrato canónico compartido: `v3/sdk/contracts` (paquete `contracts`) con schema JSON congelado `v3/sdk/contracts/schema/echo-contracts-v1.schema.json`. Confidence HIGH.
- Identidad: `v3/sdk/contracts/identity.go` — `CheckCanonicalStrategyID` (UTF-8 exacto hasta 1024 bytes = "wide ID"), `CheckSemanticKey`, `CheckSha256Ref` (`sha256:` + 64 hex), `CheckUUIDLower`, `SortUTF8` (sets canónicos). Límites ratificados en comentarios de SPEC §7. Confidence HIGH.
- PromotionRecord: `v3/sdk/contracts/promotion.go` — `HandoffManifestV1` (+`DecodeHandoffManifestV1`, `Validate`, `PayloadDigest`), `HandoffStrategy`, `HandoffVersion`, `MagicAllocation` (campo `magic_decimal` string de int64 positivo), `BuildLineage`, `MemberProof`, `HandoffEvidence`, `HistoricalAdapter`; status congelado `PromotionRecordStatusIngested = "INGESTED"` (único estado válido de receipt, `Validate` lo impone). `IdempotencyKey(registryNamespace, waveKey, canonicalStrategyID, strategyVersionRef)` deriva la key de idempotencia. Confidence HIGH.
- RuntimeBinding / EconomicCommand / Coverage: `v3/sdk/contracts/runtime.go` — `RuntimeBinding` con estados `ACTIVE`/`CLOSED`, `EconomicCommand`, `CoverageRecord` con `KNOWN_COMPLETE`/`PARTIAL`/`UNKNOWN`. Confidence HIGH.
- TradingFact / Operation lifecycle: `v3/sdk/contracts/trading.go` — `TimeEvidence` (basis UTC/OFFSET/BROKER_LOCAL/UNKNOWN), `OperationSide` (LONG/SHORT), `OperationState` (OPEN, PARTIALLY_CLOSED, CLOSED, CLOSED_INCOMPLETE_ECONOMICS, UNKNOWN), `QuantityUnit` (LOT/BASE_UNIT/CONTRACT), `OperationEconomics` con convención `CostSignConvention = "SIGNED_CONTRIBUTION"`, `InitialRisk`. Confidence HIGH.
- Persistencia de identidad (E-0/E-03): repos `v3/sdk/postgres/strategy_identity_repository.go`, `strategy_version_repository.go` (`StrategyVersion`, `Insert`, `Get`, `ListByMapping`), `promotion_record_repository.go` (`Insert` → tabla `echo.promotion_records`, `GetByID`, `GetByIdempotency`). Confidence HIGH.
- Domain events de trading: `v3/sdk/domain/snapshots.go` (Topics), `reference_event.go`, `trade_close.go`, `close_request.go`, `execution_policy.go`. Confidence HIGH.

### 3. Persistencia (IMPLEMENTADO)

- PostgreSQL único esquema de app `echo`; 75 migraciones en `v3/sdk/postgres/migrations/` (001..062 + extras numerados intermedios). Baseline 001 crea ~25 tablas (`accounts`, `brokers`, `trade_journal`, `strategy_definitions`, `symbol_mappings`, `automation_profiles/rules`, `portfolios`, `prop_rulesets`, `scheduled_jobs`, `news_events`, `lab_out_*`, etc.). Confidence HIGH.
- Migración de identidad BWC `061_identity_bwc_foundation` crea `echo.strategy_identity_mappings`, `echo.strategy_versions`, `echo.promotion_records` (con constraints de idempotencia/decision/version_ref/payload_digest), `echo.strategy_identity_aliases`, y respalda tablas previas en `echo.mig061_backup_*`; agrega columnas de identidad ancha a `trade_journal`, `account_strategy_risk_policy`, `account_strategy_impact_snapshots`, `strategy_portfolio_allocations`. Confidence HIGH.
- Migración de cuarentena `062_journal_quarantine` crea `echo.journal_quarantine` (envelope_type, trade_id, account_id, payload jsonb, payload_digest, reject_reason, conflict_field, status PENDING/RESOLVED/DISCARDED, índice único parcial para pendientes). Confidence HIGH.
- Repositories (capa de acceso SQL, paquete `v3/sdk/postgres`): `trade_journal_repository.go` (+`trade_journal_open.go`, `trade_journal_close.go`, `trade_journal_errors.go` con errores sentinela `ErrTradeJournalOpenConflict`, `ErrTradeJournalOpenAfterClosed`, `ErrTradeJournalCloseConflict`, `ErrCloseWithoutOpen`), `journal_quarantine_repository.go`, `accounts_repository.go`, `active_positions_repository.go`, `execution_policies_repository.go`, `symbol_mapping_repository.go`, `news_event_repository.go`, `ingestion_service.go`, `ingestion_artifact.go`. Confidence HIGH.
- The Lab / analytics: tablas `lab_*` (migraciones 025–059: `the_lab`, `analytics_foundation`, `lab_strategy_v3`, read models `lab_out_*`, `lab_clean_core_tables` 046, screener money metrics 053, R distribution 050/051); dominio analítico puro en `v3/sdk/lab/{domain,formulas,metrics,curves,riskpolicy,segments,dataquality,ids}`. Confidence HIGH.
- etcd: toda la config de servicios (gateway, core, bridge) se carga desde etcd vía `v3/sdk/di` + `LoadConfigFromEtcd`; keys de auth en `gateway/auth/*_token` bajo namespace por app/env. Confidence HIGH.
- Hasura: metadata `v3/hasura/metadata/tables/` (7 archivos) trackea tablas/vistas para el front: `e02_front_tables.yaml` (brokers, automation_*, account_strategy_risk_policy, symbol_mappings, scheduled_jobs, market_sessions, prop_rulesets, strategy_definitions, portfolios, portfolio_accounts, account_prop_metrics, v_trade_stream), `the_lab.yaml`, `lab_clean.yaml`, `strategy_portfolio_lab.yaml`, `accounts.yaml`, `news_*.yaml`. `v3/hasura/config.yaml` apunta a Hasura develop `192.168.31.75:8080` (comentario registra prod `192.168.31.48:8080`), admin secret por env `HASURA_CLI_ADMIN_SECRET`. Confidence HIGH.

### 4. Orquestación (IMPLEMENTADO — NO es Temporal)

- La orquestación es Flink StateFun (SDK `github.com/apache/flink-statefun/statefun-sdk-go/v3`), no Temporal: ningún `go.mod` de la plataforma depende de Temporal (grep de `go.temporal`/`temporal.io` = 0 resultados); las menciones "temporal" en código son comentarios en español. Functions registradas en `v3/core/cmd/echo-core/main.go`: StrategyConfigFn, ExecutionPlannerFn, MMEngineFn, AccSnapshotFn, InstSnapshotFn, TradeJournalFn (+ automation evaluator interno). Compose de deploy en `v3/core/deploy/flink-statefun/{develop,production}`. Confidence HIGH.
- Scheduler interno: `v3/gateway/internal/scheduler/scheduler.go` — polling de `echo.scheduled_jobs` cada 1 min (`GetPendingJobs`, `MarkExecuted`, `MarkFailed`, `IncrementAttempts`) y ejecución vía `automation.ExecutorDeps`. Confidence HIGH.
- Automation: `v3/gateway/internal/automation/` — `NewsBlackoutEvaluator` (RFC-007) genera ScheduledJobs por ventana de noticias; registry de evaluators (`evaluator_registry.go`), executor que publica acciones a Kafka (`echo.automation-actions.v1`). En Core existe también `core/internal/automation/` (evaluator + trigger cache). Confidence HIGH.

### 5. APIs y auth (IMPLEMENTADO, E-02 en el branch)

- Gateway HTTP (default port 8082, `DefaultServerConfig`), rutas en `v3/gateway/internal/server.go`: `GET /health`; `GET /api/v1/auth/hasura` (auth hook de Hasura); `POST /api/v1/webhooks/account-config`, `/api/v1/webhooks/symbol-mapping`, `/api/v1/webhooks/automation-profiles`, `/api/v1/webhooks/execution-policy` (actor `service_hasura_webhook`); `POST /api/v1/close-positions` y `/api/v1/admin/republish` (actor `control_operator`); boundary Forge `POST /api/v1/forge/promotions`, `GET /api/v1/forge/promotions/by-key/{key}`, `GET /api/v1/forge/promotions/{receipt_id}`. Confidence HIGH.
- Auth de actores (E-02): `v3/gateway/internal/auth_middleware.go` — 4 actores (`front_read`, `config_operator`, `control_operator`, `service_hasura_webhook`), tokens desde env (`GATEWAY_*_TOKEN`) o etcd, `AuthConfig.Validate` rechaza tokens duplicados entre actores (503 AUTH_MISCONFIG), distinción 401 (inválida) vs 403 (credencial ajena), nunca loguea tokens. `hasura_auth_hook.go` emite sólo roles Hasura `readonly` / `config_operator` desde body JSON, fail-closed (503 AUTH_MISCONFIG sin config). CORS exige origin explícito salvo `*` + env develop. Confidence HIGH.
- Front auth (E-02): `v3/front/src/services/session_tokens.js` — tokens de sesión por actor (control/config/lectura) en storage de sesión, prompt; sin admin secret ni Bearer materializado en bundle (evidencia E-02 VERIFICATION + `check-frontend-bundle.sh`). Confidence HIGH.
- Bridge HTTP interno (Windows): `POST /api/v1/register` (registro de EA → ClientConfig) y `GET /api/v1/health` en `v3/bridge/internal/http_server.go`. Confidence HIGH.
- No hay GraphQL propio: Hasura es el único GraphQL y el front le accede directamente con el rol del auth hook; el Gateway no expone GraphQL. Confidence HIGH.

### 6. Integraciones (IMPLEMENTADO / PARCIAL)

- MT5/MT4: EAs MQL ↔ Bridge por named pipes (`v3/bridge/internal/pipe_manager.go`, `pipe_handler.go`, `reference_pipe_handler.go`, `client_config_pipe.go`, `telemetry_pipe_handler.go`); detección de órdenes nativas `EchoOrderDetection.mqh` (Completed según SPECS.md). Confidence HIGH.
- Kafka: 17 topics canónicos declarados en `v3/sdk/domain/snapshots.go` (`echo.reference-events.v1`, `echo.core-commands.v1`, `echo.execution-results.v1`, `echo.trade-closes.v1`, `echo.close-commands.v1`, `echo.close-results.v1`, `echo.snapshot-batches.v1`, `echo.account-snapshots.v1` DEPRECATED, `echo.instrument-snapshots.v1` DEPRECATED, `echo.execution-policies.v1`, `echo.system-events.v1`, `echo.native-opens.v1`, `echo.position-snapshots.v1`, `echo.account-configs.v1`, `echo.symbol-mappings.v1`, `echo.automation-profiles.v1`, `echo.automation-actions.v1`) + topic por cuenta `echo.commands.<account>.v1` en `bridge/internal/session/command_consumer.go`. Consumer groups Sarama (V2_8_0_0, autocommit 1s, offsets Newest). Confidence HIGH.
- Forge ingestion (boundary receptor, E-04/E-01): `POST /api/v1/forge/promotions` → `ForgeIngestHandler` (`v3/gateway/internal/forge_ingest_handler.go`) con bearer propio (`forge_ingest_auth.go`), límite de body, clasificación de errores (`classifyIngestError`, wire errors con retryable) y modo misconfig 503 fail-closed. Service: `v3/sdk/postgres/ingestion_service.go` `Ingest()` — valida manifest, version de autoridad, copia artefactos operativos (`FilesystemStore` en `artifact_root` con allowlist, `NewFilesystemStore`), mapea tx strategy_version/mapping/promotion, receipt INGESTED, replay idempotente (200 exact-replay sin re-fetch de artefactos), 409 en conflictos. `ArtifactSource` de producción es `unavailableArtifactSource` fail-closed (no hay store remoto allowlisteado en V1). Confidence HIGH.
- No hay integración SQX en este repo (SQX/Forge vive en `xKoRx/symphony`, fuera de este baseline). Confidence HIGH.
- Flink StateFun vía HTTP (h2c) — ver sección 4. No se encontraron otras integraciones externas (sin Slack/email/etc.). Confidence MEDIUM (ausencia verificada por grep, no exhaustiva).

### 7. Runtime / config (IMPLEMENTADO)

- Config por etcd con namespace por servicio+env (`v3/sdk/di`, `etcd.NamespacePrefix()`); env vars directas soportadas: `ENV`, `DATABASE_URL` (journalctl, toolkit), `GATEWAY_{FRONT_READ,CONFIG_OPERATOR,CONTROL_OPERATOR,SERVICE_HASURA_WEBHOOK}_TOKEN`, `GATEWAY_ENV`, `CORS_ALLOWED_ORIGINS`, `CORE_INTERNAL_URL`, `HASURA_CLI_ADMIN_SECRET`. Forge ingest keys frozen `gateway/forge_ingest/*` (artifact_root, store_allowlist, max_artifact_bytes, token). Confidence HIGH.
- Build/deploy: `build_v3.sh` (SDK/Core Linux, Bridge Windows, Gateway, Toolkit, Front Vue, clientes MT4/MT5 + DLLs → `v3/bin/`), `Makefile`, `build_all.sh` (legacy), `deploy/postgres` (setup.sql, teardown.sql, migrations), `deploy-prod.sh`. Compose Flink-StateFun develop/production en `v3/core/deploy/flink-statefun/`. No se encontró docker-compose de plataforma completa. Confidence HIGH.
- Legacy convive: módulos v1/v2 siguen en `go.work` y algunos binarios v2 compilan (evidencia E-02 VERIFICATION menciona `v2/toolkit`), pero el activo es v3. Confidence HIGH.

### 8. Observability (IMPLEMENTADO)

- OpenTelemetry full: `v3/sdk/telemetry/client.go` exporta logs/metrics/traces vía OTLP gRPC (`otlploggrpc`, `otlpmetricgrpc`, `otlptracegrpc`) con endpoints configurables (`boot.go`); semconv por servicio en `v3/sdk/telemetry/semconv/{bridge,core,common}.go`; bundle de métricas en `metricbundle/echo.go`. Confidence HIGH.
- Métricas de dominio: counters como `echo.trade_journal.quarantine.total`, `echo.trade_journal.open.conflict`, `echo.trade_journal.close_without_open.total`, `echo.session.circuit_breaker.triggered`, `echo.lab.job_run_id` (attrs). Confidence HIGH.
- Trazas en Bridge: spans por mensaje EA con attrs `echo.source`, `echo.duration_ms`, `echo.timeout`. Confidence HIGH.

### 9. Retry / failure / recovery (IMPLEMENTADO con gates físicos parciales)

- Durable delivery Bridge→Kafka (E-02): productor síncrono `PublishSync` (`v3/sdk/messaging/kafka_producer.go`) usado para todos los facts de trading (reference events, execution results, close results, trade closes) y handlers Gateway (commit `0ff4b04a`/`38eda71b`). Confidence HIGH.
- Journal ACK/cuarentena (E-02): `TradeJournalFn` (`v3/core/internal/functions/trade_journal.go`) clasifica errores al persistir: conflictos y errores determinísticos de payload → `quarantinePayload` a `echo.journal_quarantine` (razones `POISON_PAYLOAD`, `CLOSE_WITHOUT_OPEN`, conflictos open/close, reason derivado en `quarantineReason`) con ACK a Flink; errores transientes de persistencia → error hacia Flink (retry del runtime). Métrica de cuarentena emitida. Confidence HIGH.
- CLI de recuperación: `v3/tools/journalctl` — `replay-facts` reconstruye journal PG→PG por tipo de envelope (reference_event, trade_intent, execution_result, trade_close, close_result) sin publicar a Kafka (garantizado estructuralmente por `deps_guard_test.go::TestJournalctlDoesNotImportMessaging`); `quarantine list|show|resolve|discard` y `stats`. Confidence HIGH.
- Idempotencia de ingestión Forge: replay exacto 200 sin re-fetch de artefactos, 409 en digest/identity/mapping conflicts, rollback en failure de promotion (`TestIngest_RollbackOnPromotionFailure`), recuperación de timeouts pre-commit y commit-then-lost-response vía GET/replay (tests `TestIngest_TimeoutPreCommit_Retry`, `TestIngest_CommitThenLostResponse_GetThenReplay`). Confidence HIGH.
- Circuit breaker por sesión de ejecución en Bridge (`echo.session.circuit_breaker.triggered`, `command_consumer.go`). Confidence MEDIUM (símbolo visto, semántica no leída a fondo).
- Scheduler de jobs: reintentos con `IncrementAttempts` y MarkFailed. Confidence MEDIUM.

### 10. Tests como evidencia (137 archivos `*_test.go` en v3)

- Matriz de auth E-02: `gateway/internal/auth_middleware_test.go` (`TestAuthMiddlewareActorMatrix`, `TestAuthMiddlewareCoversEveryActorClass`, `TestAuthMiddlewareFailsClosedWhenTokenMissing`, `TestAuthConfigRejectsDuplicateActorTokens`, `TestCORSRequiresExplicitOriginOutsideDevelop`); `hasura_auth_hook_test.go` (`TestHasuraAuthHookRolesAndFailClosed`, `TestHasuraAuthHookFailsClosedOnDuplicateActorTokens`). Confidence HIGH.
- Gate de identidad/BWC E-0: `sdk/postgres/identity_bwc_gate_test.go` (`TestEnsureJournalParentRows_Rejects1025` —rechaza IDs >1024—, `TestSchemaProtection_WriteOnceViaGo`, `TestNoEchoMagicAllocator`, `TestCertification_AllAcceptanceCriteriaNamed`). Confidence HIGH.
- Ingestión Forge E-01/E-04: `sdk/postgres/ingestion_service_test.go` (30+ tests: `TestIngest_G01_201`, `TestIngest_ExactReplay_200_NoArtifact`, `TestIngest_G07_409`, `TestIngest_IdentityConflict`, `TestIngest_MappingConflictMagic`, `TestIngest_NoEchoAllocator`, `TestCorpus_ValidationMatrix`, `TestArtifact_*`, etc.) y `ingestion_noneffects_test.go` (`TestIngest_NoRuntimeTables`, `TestIngest_StatusOnlyIngested`, `TestSOURCE_NoMigrationDelta`, `TestSOURCE_NoContractsDelta` — protegen el scope del SOURCE). Confidence HIGH.
- Cuarentena: `core/internal/functions/trade_journal_test.go`, `sdk/postgres/journal_quarantine_repository_test.go` (`TestStablePayloadDigestIsDeterministic`), suites SQL `sdk/postgres/tests/journal_quarantine/run.sh` (assert up/down fail-closed). Confidence HIGH.
- E2E determinístico sin Flink/Kafka reales: `v3/e2e` (framework en memoria: `ExecutionEngine`, `StateStore`, `EgressCollector`; `TestFullFlow_OpenAndClose`, `TestFullFlow_MultipleSlaves_OpenAndClose`, `TestFullFlow_WithSLTPAdjustment`, `TestFullFlow_FixedRiskCalculation`, `TestCloseFlow_*`, `TestOpenFlow_*`, `symbol_mapping_test.go`, `trade_journal_test.go`). Es simulación, no pruebas físicas de broker. Confidence HIGH.
- Front: 33 tests Vitest (10 archivos, `v3/front/tests/unit` + `src/components/__tests__`) según evidencia E-02. Confidence MEDIUM (número tomado de VERIFICATION.md, no re-ejecutado).
- NO cubierto por tests físicos: exactitud de ejecución contra broker real MT5, compose Flink/PG/Kafka real (T14 de E-02 quedó PHYSICAL_PARTIAL), failover real de Kafka. Confidence HIGH (declarado en VERIFICATION.md).

## Evidence

| Claim | File (xKoRx/echo) | Symbol | Test/Config | Confidence |
|---|---|---|---|---|
| Orquestación es Flink StateFun, no Temporal | v3/core/cmd/echo-core/main.go; go.mod | main | grep go.temporal = 0 | HIGH |
| Journal cuarentena determinística | v3/core/internal/functions/trade_journal.go | TradeJournalFn.quarantinePayload, quarantineReason | trade_journal_test.go; migration 062 | HIGH |
| Recovery CLI sin Kafka | v3/tools/journalctl/main.go | run, replayFacts | deps_guard_test.go::TestJournalctlDoesNotImportMessaging | HIGH |
| Receipt INGESTED único estado | v3/sdk/contracts/promotion.go | PromotionRecordStatusIngested, PromotionRecord.Validate | ingestion_noneffects_test.go::TestIngest_StatusOnlyIngested | HIGH |
| Wide ID 1024 bytes + magic int64 | v3/sdk/contracts/identity.go; promotion.go | CheckCanonicalStrategyID, MagicAllocation | identity_bwc_gate_test.go::TestEnsureJournalParentRows_Rejects1025 | HIGH |
| Ingestión con replay idempotente 409/200 | v3/sdk/postgres/ingestion_service.go | IngestionService.Ingest, commitAcceptance | ingestion_service_test.go (TestIngest_G07_409, TestIngest_ExactReplay_200_NoArtifact) | HIGH |
| Auth por 4 actores, fail-closed | v3/gateway/internal/auth_middleware.go | AuthConfig.Validate, authMiddleware | auth_middleware_test.go::TestAuthMiddlewareActorMatrix | HIGH |
| Hasura auth hook roles readonly/config_operator | v3/gateway/internal/hasura_auth_hook.go | NewHasuraAuthHook, writeHasuraSession | hasura_auth_hook_test.go | HIGH |
| Bridge Windows named pipes | v3/bridge/cmd/echo-bridge/main.go | main (`//go:build windows`) | build_v3.sh (bridge targets Windows) | HIGH |
| PublishSync para trading facts | v3/sdk/messaging/kafka_producer.go; bridge pipe handlers | KafkaProducer.PublishSync | commit 38eda71b; gateway handler tests | HIGH |
| Topic por cuenta echo.commands.<account>.v1 | v3/bridge/internal/session/command_consumer.go | CommandConsumer | command_consumer_test.go | HIGH |
| 17 topics canónicos | v3/sdk/domain/snapshots.go | Topics | v3/kafka/README.md | HIGH |
| Boundary Forge misconfig 503 fail-closed | v3/gateway/internal/forge_ingest_handler.go; server.go | ForgeIngestHandler.ServeHTTP, Misconfigured | forge_ingest_handler_test.go; TestServer_MountsForgeIngest | HIGH |
| Artifact store filesystem + allowlist; source remoto fail-closed | v3/sdk/postgres/ingestion_artifact.go | FilesystemStore, ArtifactSource, unavailableArtifactSource | ingestion_artifact_test.go | HIGH |
| Scheduler 1-min + news blackout RFC-007 | v3/gateway/internal/scheduler/scheduler.go; automation/news_blackout_evaluator.go | JobScheduler, NewsBlackoutEvaluator | scheduler_test.go; news_blackout_evaluator_test.go | HIGH |
| Migraciones numeradas 001..062 (75 archivos con pares .up/.down y README), esquema echo | v3/sdk/postgres/migrations/ | 001..062 | tests SQL sdk/postgres/tests/ | HIGH |
| Tablas identidad 061 | v3/sdk/postgres/migrations/061_identity_bwc_foundation.up.sql | strategy_identity_mappings, strategy_versions, promotion_records, strategy_identity_aliases | strategy_identity_repository_test.go | HIGH |
| OTLP logs/metrics/traces | v3/sdk/telemetry/client.go | Client (initLogsOTLP, etc.) | — (config-driven) | HIGH |
| E-02 PHYSICAL_PARTIAL (sin compose físico) | specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/VERIFICATION.md | — | declaración del propio SPEC | HIGH |
| E2E es simulación en memoria | v3/e2e/doc.go | ExecutionEngine, StateStore | full_flow_test.go suite | HIGH |

## Implemented vs Spec-Only

- IMPLEMENTADO (código + tests en baseline): Core StateFun runtime + TradeJournal con cuarentena durable + journalctl recovery; Gateway completo (webhooks, close-positions, republish, automation, scheduler, forge ingest) con auth de 4 actores y Hasura auth hook; Bridge Windows (pipes, command consumer, sessions); SDK contracts frozen v1 (identidad, promotion, runtime, trading); repos Postgres (migraciones 001..062, identidad BWC 061, cuarentena 062); lab-worker batch + sdk/lab analytics; OTel observability; front Vue con session tokens por actor; EAs MQL MT4/MT5.
- IMPLEMENTADO PERO CON GATES FÍSICOS PENDIENTES: E-02 (auth + journal recovery) está en el branch como código + tests CONTRACT PASS, pero su VERIFICATION.md declara PHYSICAL_PARTIAL: no se ejecutó compose Flink/PG/Kafka/Hasura real (T14), T15 pendiente; status en SPECS.md "Implementation-Ready / Manager Source Review". E-01/E-04 (forge ingestion) está Spec-Active con implementación y 30+ tests CONTRACT, incluida la interlock con E-03; el cliente HTTP real en Symphony no existe (F-04 usa FakeConsumer; Echo congela POST/GET por el lado receptor).
- SOLO-SPEC / NO implementado en este repo: CommandID UUIDv5 (diferido explícitamente a E-08 en SPEC E-02); cliente HTTP Forge emisor (lado Symphony); jobs completos de materialización lab (lab-worker hoy: smoke + recompute/materialize; RFC-009 progresivo); varias features de clientes MT en Spec-Active (MT5-MT4 alignment, news restrictions lado EA); no hay Temporal, no hay otro message broker, no hay multi-tenant.
- Status model oficial por feature en `specs/SPECS.md` (Legacy/Implemented/Spec-Active/Completed); ningún feature del catálogo está marcado Completed salvo FEAT-CLIENTS-NATIVE-ORDER-DETECTION.

## Conflicts / Unknowns

- Ninguna contradicción dura de evidencia detectada. Conflictos menores documentados: topics legacy `echo.account-snapshots.v1`/`echo.instrument-snapshots.v1` marcados DEPRECATED aún presentes en `Topics`; binario `echo-functions` DEPRECATED aún compilable.
- Unknown 1: semántica exacta del circuit breaker de sesión (`echo.session.circuit_breaker.triggered`) no leída a fondo (no es load-bearing para la wiki). Confidence MEDIUM.
- Unknown 2: número exacto de tests front (33) tomado de VERIFICATION.md, no re-ejecutado en esta sesión. Confidence MEDIUM.
- Unknown 3: `v1/` y `v2/` quedan cartografiados sólo como legacy (existencia y rol en go.work); su comportamiento interno no fue mapeado (fuera de prioridad para la wiki; el activo es v3).
- Unknown 4: composición exacta de tablas Hasura en `the_lab.yaml`/`lab_clean.yaml` no enumerada tabla-por-tabla (se verificó que existen y el patrón de tracking).
- Nota: el working tree estaba clean; no fue necesario leer vía `git show`.

## Corrections

- [KBC-G fix F-2, ciclo 2] Corregido conteo de topics: "18 topics canónicos" → "17 topics canónicos" (Findings Kafka y Evidence). Evidencia: `xKoRx/echo` `v3/sdk/domain/snapshots.go` L254-270, struct `Topics` contiene exactamente 17 entradas (2 marcadas DEPRECATED: `echo.account-snapshots.v1`, `echo.instrument-snapshots.v1`); la única otra ocurrencia de un string `echo.*.v1` en el archivo (L314) es un comentario, no una declaración. Confidence HIGH.

## Handoff

- Para integration cartographer (Fase D): la frontera Forge→Echo implementada es exactamente `POST/GET /api/v1/forge/promotions` + `IngestionService` + `echo.promotion_records`; el receipt sólo tiene estado INGESTED; la emisión real HTTP desde Symphony no existe aún (F-04 en FakeConsumer, `HandoffIngress.Deliver` frozen); artifact copy es filesystem local con allowlist y source remoto fail-closed. Los tests `ingestion_service_test.go` y `ingestion_noneffects_test.go` son el corpus de golden gates a citar.
- Para wiki documentarian (Fase F): estable para documentar como realidad vigente — arquitectura v3 (Bridge/Core/Gateway/Flink StateFun/Kafka/Postgres/etcd/Hasura/Vue), contratos frozen `v3/sdk/contracts`, auth de actores E-02, cuarentena + journalctl, lab-worker. Movedizo — E-02 no está cerrado (PHYSICAL_PARTIAL, branch feature aún no mergeado a master a99f9a63); E-01/E-04 Spec-Active pendiente de verifier; todo lo citado debe llevar el baseline `f7ddea18` y reconciliarse contra HEAD al publicar.
- Recomendación de citación: usar `specs/SPECS.md` como índice de estado por feature y `specs/FEAT-*/VERIFICATION.md` como registro de gates, pero no como fuente de comportamiento (el comportamiento vive en código y tests citados arriba).
- Para legacy curator: `v3/core/cmd/echo-functions` (deprecated) y topics DEPRECATED en `Topics` son candidatos a señal de "legacy dentro del activo"; v1/v2 quedan como evidencia histórica sin acción.
- Este artifact es el único output escrito por esta tarea; ningún archivo del repo ni del vault fue modificado.
