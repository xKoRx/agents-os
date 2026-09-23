---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[A — Technical SPEC D1]]"
  - "[[D — Acceptance Gate D1]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
aliases:
  - D1 implementation evidence
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d1
created: "2026-09-23"
updated: "2026-09-23"
---

# G — Implementation Evidence D1 (Shot 1)

## Propósito

Evidencia real de implementación del Shot 1 de D1 — Echo Foundation (mandato 2026-09-23): baseline, branch, commits, migración, archivos, tests ejecutados con resultados exactos, evidencia PG, regresiones clasificadas, riesgos y feedback para el Shot 2 (verificación independiente). Ningún hecho aquí declarado sin ejecución detrás.

## Contenido

### Baseline y rama

- Repositorio canónico Echo: `xKoRx/echo`, checkout `/home/kor/go/src/github.com/xKoRx/echo` (worktree limpio). Baseline de planificación `5dd998f1` verificada como ancestro; HEAD real de master al iniciar = `3596fc48` (1 commit front local, propiedad de otra sesión, inerte para D1) ⇒ branch creada desde el HEAD real, reconciliación conservadora según mandato.
- Branch de trabajo: `feature/d1-echo-foundation` en worktree aislado `/home/kor/aranea/work/d1-echo-foundation-20260923/echo`. Sin merge a master. HEAD final: `e35d4347` (serie lineal de 4 commits sobre `3596fc48`).

### Commits

- `00e6716a` feat(contracts): contrato D1 `strategy-history.v1` (CanonicalOperationInputV1) + tests casos 1-25.
- `8bd7308d` feat(postgres): migración `064_canonical_operations` (up/down) + harness `tests/d1_foundation/run.sh`.
- `a063416a` feat(postgres): repository + `StrategyHistoryService.ReplaceHistory` + tests PG casos 26-43 + adaptación mecánica de TRUNCATEs E-03/E-04.
- `e35d4347` feat(gateway): boundary `PUT/GET /api/v1/strategy-versions/{strategy_version_ref}/history` + config + tests casos 44-54.

### Contrato compartido (v3/sdk/contracts)

- `strategy_history.go`: DTOs request/dataset/operación/response, enums SQX|MT5|REFERENCE, LONG|SHORT, LOT|CONTRACT|BASE_UNIT; decimales canónicos como strings (sin JSON floats, techo NUMERIC(38,18) verificado pre-persistencia); geometría LONG/SHORT obligatoria; economía exacta `net = gross + commission + swap` vía big.Rat; períodos derivados sólo de `opened_at` (A exclusiva; MT5 en [A,B) con B nullable); timezone IANA (time.LoadLocation); instantes normalizados a UTC; recetas de digest `wire.HashTagged` con tags `strategy-history-operation.v1` / `strategy-history-dataset.v1` / `strategy-history-head.v1` y orden canónico `(opened_at, closed_at, source_trade_id)`; códigos D1 aditivos (UNKNOWN_INSTRUMENT, INVALID_OPERATION, PERIOD_VIOLATION, DUPLICATE_SOURCE_TRADE_ID, COUNT_MISMATCH, DIGEST_MISMATCH, HISTORY_CONFLICT). Decode lossless con perfil `echo-wire-json.v1` (duplicados/nulls/number tokens rechazados). `NormalizedOperationV1` de S0/E05 queda supersedida para este uso sin tocar contratos existentes (sin dual-write).

### Migración 064

- `v3/sdk/postgres/migrations/064_canonical_operations.up.sql` / `.down.sql`: `echo.canonical_operations` (IDENTITY PK bigint; FK `(registry_namespace, strategy_version_ref)` → `echo.strategy_versions` RESTRICT; UNIQUE identidad durable por source; CHECKs source/side/volume_unit/positivos/economía/tiempo/currency/record_digest; NUMERIC(38,18) exacto; índices opened_at/closed_at mínimos) y `echo.strategy_history_state` (head activo por StrategyVersion, no revision log). Grants guardados por rol (patrón 061/063) + USAGE de secuencia. Down destructivo sólo de las dos tablas D1.
- Autoridades reutilizadas: StrategyVersion = PK real `(registry_namespace, version_ref)` de 061 (write-once); símbolo canónico = lado canonical de `echo.symbol_mappings` activos vía `SymbolMappingInstrumentResolver` (sin registro paralelo, sin aliases, fail-closed 422).

### Servicio y boundary

- `v3/sdk/postgres/strategy_history_service.go`: pipeline SPEC §8 completo con replay fast-path (mismo history_digest ⇒ UNCHANGED sin writes) y transacción única: advisory xact lock por identidad, relectura del head bajo lock (convergencia concurrente), delete sólo SQX+MT5 (REFERENCE jamás), bulk insert acotado (chunks de 250 filas ⇒ 3 statements para 700 trades, demostrado con sqlmock), upsert del head, commit; rollback total ante cualquier fallo. Seam interno `replaceFault` (sólo tests del paquete) para el caso 41.
- `v3/gateway/internal/strategy_history_handler.go` + `config.go` + `server.go` + `main.go`: `PUT/GET /api/v1/strategy-versions/{strategy_version_ref}/history` sobre el Gateway existente; Bearer opaco constant-time con token dedicado `gateway/strategy_history/token` (503 fail-closed sin token); namespace server-side `gateway/strategy_history/namespace` (default `forge-live`); body limit configurable default 64 MiB; deadline default 60s; clasificador 400/404/422/409/503 según SPEC §10; GET read surface con source/rangos/order_by/limit. Cero efectos de trading (delta journal/posiciones = 0 demostrado en test).

### Comandos y resultados de tests (exactos)

- Entorno de pruebas: PG 17.11 desechable local `127.0.0.1:15445/d1_foundation` (PGDATA en `~/aranea/work/d1-echo-foundation-20260923/pg-data`), schema reconstruido 001..064 por `v3/sdk/postgres/tests/d1_foundation/run.sh` (probe BEGIN+ROLLBACK, apply estricto, idempotente, down+up: todos OK).
- `go test ./v3/sdk/contracts` (GOWORK=off): ok — 20 funciones TestHistory PASS; coverage paquete 95.1%, archivo nuevo 96.3%.
- `DATABASE_URL=... go test ./v3/sdk/postgres/`: 11 funciones TestD1 PASS (26-43 + fallos de persistencia + B seteada). Único FAIL: `TestScratch_QueryDB` — preexistente en master sin modificar (scratch hardcodeado a DEV `.220` con credencial rotada; demostrado idéntico en `3596fc48`).
- `DATABASE_URL=... go test ./v3/gateway/...`: `v3/gateway/internal` ok — 6 funciones TestD1 PASS (44-54). Único FAIL: `TestAutomationHandler_HandleMessage_ValidAction` (automation) — preexistente conocido (Environment Contract §5.6), demostrado idéntico en master sin modificar.
- `go test ./v3/lab-worker/...`: ok 5/5 paquetes (consumidores E05 sin impacto).
- Build completo de los 7 módulos v3 + `go vet` limpio + gofmt limpio.

### Evidencia PG (aserciones programáticas ejecutadas)

- Primera carga: `CREATED` + counts SQX=2 MT5=1 exactos; readback byte-exacto de decimals NUMERIC (igualdad big.Rat) y record_digest idéntico al recetado.
- Replay exacto: `UNCHANGED`, mismo digest, `updated_at` del head sin cambio, cero deletes/inserts.
- Replacement: `REPLACED` con digest nuevo; counts finales SQX=2 MT5=2 REFERENCE=1; operación fuera del snapshot eliminada.
- REFERENCE preservada en replay, replacement y rollback (counts REFERENCE=1 en todo punto).
- Rollback forzado (fallo inyectado post-delete): dataset anterior íntegro y head previo conservado.
- Concurrente: dos PUT en paralelo convergen a un head ∈ {A,B} y filas 100% de ese dataset (sin mezcla).
- Direct rows: side/economics/currency/precio negativo/source enum/closed<open/digest malformado rechazados por constraints reales; UNIQUE (ns,ref,source,trade) forzada.
- Sin side effects: `trade_journal`/`active_positions` delta 0; el handler no tiene productor Kafka.

### Regresiones y clasificación

- Adaptación mecánica autorizada por Test Plan §5: 4 TRUNCATEs de harnesses E-03/E-04 (`strategy_identity_repository_test.go`, `identity_bwc_gate_test.go`, `tests/identity_bwc/30c_down_threshold_probe.sql`, `forge_ingest_handler_test.go`) incorporan las 2 tablas D1 (FK nuevas hacia strategy_versions obligan a truncar relacionadas en un solo statement). Sin cambio de semántica.
- 2 fallos clasificados preexistentes (no D1): `TestScratch_QueryDB` y `TestAutomationHandler_HandleMessage_ValidAction`, ambos demostrados idénticos en master `3596fc48` sin modificar.
- Seed tests ETCD no ejecutados: no se corrió `go test ./...` a nivel raíz (riesgo conocido de seed tests v1/v2/v3 contra ETCD real en master sin el fix E-04).

### Riesgos restantes

- La migración 064 no está aplicada en ninguna base real (DEV `echo-develop` incluida): aplicar por flujo de release/owner. En DEV vigente conviene además reconciliar el estado parcial de 061.
- `SymbolMappingInstrumentResolver` exige presencia canónica activa en `symbol_mappings`: si un productor trae un instrumento cuyo mapping no existe aún, la ingesta fallará 422 (fail-closed por diseño; sembrar mappings es acción owner).
- `historyDefaultMaxBodyBytes` 64 MiB y `deadline` 60s son defaults frozen iniciales: medir con datasets multi-año reales en D2 y ajustar por ETCD si hace falta.
- Los digests D1 están congelados de facto por los tests (tags y orden de campos en `strategy_history.go`): cualquier cambio de receta rompe replay con datos ya persistidos — versionar contrato antes de tocar.
- Reemplazo es full-snapshot por diseño (M01-M12): datasets de millones de filas pagarán delete+insert completo; aceptado para V3, revisar si el volumen real lo exige.

## Fuentes

- [[A — Technical SPEC D1]] · [[B — Implementation Plan D1]] · [[C — Test Plan D1]] · [[D — Acceptance Gate D1]] · [[F — Continuity D1]]
- Agent run atribuible: `80-agents/journal/agent-runs/2026-09-23-zcode-glm53-d1-echo-foundation-shot1.md`
- Feedback para Shot 2: `80-agents/journal/feedback/session/2026-09-23-d1-echo-foundation-shot1-feedback.md`
- Repo `xKoRx/echo`, branch `feature/d1-echo-foundation`, HEAD `e35d4347` (local, sin push).
