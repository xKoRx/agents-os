---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[I — Independent Verification D1 (Shot 2)]]"
  - "[[J — Manager Decision after Shot 2]]"
  - "[[D — Acceptance Gate D1]]"
  - "[[F — Continuity D1]]"
  - "[[G — Implementation Evidence D1 (Shot 1)]]"
aliases:
  - D1 final correction and gate
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d1
created: "2026-09-23"
updated: "2026-09-23"
---

# K — Final Correction and Gate D1 (Shot 3)

## Propósito

Evidencia final del Shot 3 de D1 — Echo Foundation (mandato 2026-09-23): corrección de los dos hallazgos aceptados (F-S2-01, F-S2-02) sin reabrir el scope congelado, conversión de los reproducers en regresiones permanentes, rerun del gate D1 completo y veredicto final. Ninguna afirmación sin ejecución detrás.

## Veredicto

**D1_FINAL_PASS** (2026-09-23, HEAD final `64b616ff`). Los 18 criterios del Acceptance Gate + G19 (consistent read surface) + G20 (timestamp fidelity) PASS. Deviations: NONE.

## Correcciones

### F-S2-01 — Consistent read snapshot (MEDIUM, cerrado)

- **Antes:** `StrategyHistoryService.GetHistory` leía history head y operaciones en dos statements separados sobre el pool sin snapshot única; un replacement que commiteaba entre ambos producía un GET con head de un snapshot y filas de otro (Shot 2: `torn_head_ops=7/441`, sin mezcla de filas ni corrupción durable).
- **Después:** ambas lecturas corren dentro de una única transacción `READ ONLY` `REPEATABLE READ` (`s.db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelRepeatableRead, ReadOnly: true})`); head y operaciones usan el mismo `*sql.Tx` vía `NewStrategyHistoryRepository(tx)`. MVCC puro: cero writes, sin locks adicionales, los writers nunca se bloquean. `defer tx.Rollback()` garantiza cierre en toda ruta de error; errores de begin/commit clasificados como `ErrHistoryUnavailable` (503 retryable); 404, filtros source/opened/closed, `order_by`, `limit`, cancelación de contexto y aislamiento de namespace preservados.
- **Path:** `v3/sdk/postgres/strategy_history_service.go` (GetHistory; commit `a25794c9`).
- **Test permanente:** `v3/sdk/postgres/strategy_history_concurrent_read_regression_test.go` → `TestD1GetHistoryConsistentReadSnapshot` (60 replacements alternando datasets A/B con lector GET continuo; exige reads≥20, `torn=0`, `mixed=0`, counts+digests+history-digest del head coherentes con el ÚNICO dataset de las filas, REFERENCE intacta y visible en cada lectura, convergencia durable final).
  - Rojo contra `e35d4347` sin fix: `torn reads=10 (reads=780)`.
  - Verde con fix: 3/3 PASS (`reads=678/743/709, torn=0, mixed=0, ref=1`), también dentro de la suite completa y bajo `-race`.
  - Reproducer ORIGINAL de Shot 2 (`TestShot2ConcurrentReadDuringReplace`, rama `d1-shot2-verify` @ `6fafe683`, corrido sin commitear contra el código final): `reads=428 mixed_rows=0 torn_head_ops=0` y `reads=404 mixed_rows=0 torn_head_ops=0` — corrida equivalente (30 replacements) al 7/441 original.

### F-S2-02 — Timestamp fidelity (LOW, cerrado)

- **Antes:** la proyección HTTP formateaba instantes con `time.RFC3339` (segundos): DB `10:00:00.5Z` se leía por GET como `10:00:00Z` (probado en Shot 2).
- **Después:** TODA la proyección timestamp del read surface `strategy-history.v1` usa `time.RFC3339Nano`: `training_end_at`, `live_start_at`, `opened_at`, `closed_at` en `projectHistoryHead` (4 sitios), y `accepted_at` del response PUT en `historyReadyResponse` (autorizado por el mandato §9 "accepted_at si aplica"). No cambia representación almacenada, digests, migración ni contrato (el parse RFC3339 de los filtros de query es input, no proyección, y se dejó intacto).
- **Path:** `v3/gateway/internal/strategy_history_handler.go` + `v3/sdk/postgres/strategy_history_service.go` (1 línea `accepted_at`; commit `64b616ff`).
- **Test permanente:** `v3/gateway/internal/strategy_history_timestamp_regression_test.go` → `TestD1HTTPHistoryTimestampFidelity` (boundary A sub-segundo `2024-06-30T21:00:00.5Z` en el head; operación SQX con fracciones no triviales `.123456`/`.654321`; operación MT5 de segundo exacto sin fracción espuria; round-trip validado parseando el response a `time.Time` y comparando instantes con `.Equal`; coherencia history_digest GET/PUT).
  - Rojo contra `e35d4347` sin fix: `training_end_at: got=2024-06-30T21:00:00Z want=2024-06-30T21:00:00.5Z`.
  - Verde con fix: 3/3 PASS; probe ORIGINAL de Shot 2 (`TestShot2HTTPGetSubSecondProjection`) contra el código final: `GET opened_at=2024-05-10T10:00:00.5Z` exacto, sin `FINDING-PROBE`.

## Final HEAD

- Repositorio `xKoRx/echo`; branch final aislada `feature/d1-echo-foundation-final` (worktree `/home/kor/aranea/work/d1-final-20260923/echo`, fuera del checkout del desarrollador; sin merge a master, sin push).
- Base: `e35d43474a36d46fee9bf2879c669c75d44a6986` (implementation HEAD Shot 1). Commits:
  - `a25794c9` fix(d1): F-S2-01 GetHistory lee head+operaciones en una única snapshot REPEATABLE READ READ ONLY (+ regresión permanente).
  - `64b616ff` fix(d1): F-S2-02 proyecta timestamps de strategy-history.v1 con RFC3339Nano (+ regresión permanente).
- HEAD final: `64b616fff9ac2c76de6260a42c73ec4c363d6c54`; worktree limpio.
- Verifier branch `d1-shot2-verify` @ `6fafe683` inspeccionada: contiene EXCLUSIVAMENTE 3 archivos de test (+2317/−0); se reutilizaron sus reproducers como base de las regresiones permanentes y se corrieron intactos contra el código final como evidencia; nada de esa branch se heredó al producto.

## Diff scope (e35d4347..64b616ff)

Exactamente 4 archivos, +379/−7:

| Archivo | Tipo | Contenido |
|---|---|---|
| `v3/sdk/postgres/strategy_history_service.go` | productivo | transacción de lectura REPEATABLE READ READ ONLY + `accepted_at` RFC3339Nano |
| `v3/gateway/internal/strategy_history_handler.go` | productivo | 4 sitios de proyección → `RFC3339Nano` |
| `v3/sdk/postgres/strategy_history_concurrent_read_regression_test.go` | test | regresión permanente F-S2-01 |
| `v3/gateway/internal/strategy_history_timestamp_regression_test.go` | test | regresión permanente F-S2-02 |

Cero cambios en schema, migración 064, digest recipes, campos canónicos, replacement semantics, source/period rules, economics, symbol handling, auth, REFERENCE policy o límites de body. Sin cleanup oportunista (los 5 archivos lab-worker que `gofmt -l` reporta están byte-idénticos a `e35d4347`: ruido de formato preexistente fuera del scope congelado).

## Tests (comandos y resultados)

Entorno: PG desechable propio 17.11 `127.0.0.1:15450/d1_final` (PGDATA y logs bajo el worktree final; schema reconstruido desde cero por el harness). Go 1.27.1 linux/amd64. Sin PROD, sin DEV compartida, sin ETCD, sin Kafka (los scratch que las requieren quedan en su estado preexistente certificado).

| Comando | Resultado |
|---|---|
| `DATABASE_URL=…15450/d1_final bash v3/sdk/postgres/tests/d1_foundation/run.sh` (×2: pre-fix y HEAD final) | OK — rebuild 000+001..063, probe BEGIN+064+ROLLBACK sin residuos, apply 064 estricto, idempotente, down+up; objetos D1 verificados por catálogo |
| `cd v3/sdk/contracts && GOWORK=off go test ./...` | ok (contracts + schema + wire + fakeconsumer) |
| `GOWORK=off go test -run 'TestHistory\|TestShot2' -v .` (contracts) | 20/20 `--- PASS` |
| `DATABASE_URL=… go test ./v3/sdk/postgres/ -v` | 139 `--- PASS`, 1 `--- FAIL: TestScratch_QueryDB` (preexistente certificada, modo idéntico) |
| `DATABASE_URL=… go test ./v3/gateway/...` | `internal` ok (incluye 8 funciones TestD1 HTTP + regresión nueva); `automation` 1 FAIL preexistente `TestAutomationHandler_HandleMessage_ValidAction` (modo idéntico); `scheduler` ok |
| `go test ./v3/lab-worker/...` | 5/5 paquetes ok |
| `GOWORK=off go test -race ./...` (contracts) | ok, sin DATA RACE |
| `DATABASE_URL=… go test -race ./v3/sdk/postgres/ -v` | sin DATA RACE; único FAIL el scratch preexistente |
| `DATABASE_URL=… go test -race ./v3/gateway/internal/` | ok, sin DATA RACE |
| `go build ./...` por módulo (gateway, lab-worker, sdk, core, bridge, toolkit, e2e) | 7/7 OK |
| `go vet` (postgres, gateway/..., lab-worker/...) y `gofmt -l` en archivos del diff | limpio |

## Gate matrix (18 criterios + G19/G20)

| # | Criterio | Veredicto | Evidencia (esta branch) |
|---|---|---|---|
| G01 | SPEC sin desviación semántica no aprobada | PASS | diff 4 archivos revisado línea a línea; únicamente los 2 fixes autorizados |
| G02 | Migraciones aplican en PG aislado | PASS | harness 064 completo en 15450 (probe/estricto/idempotente/down-up) |
| G03 | SDK expone contrato versionado producer-agnostic | PASS | `strategy-history.v1` intacto; suite contracts verde |
| G04 | StrategyVersion authority reutilizada | PASS | `TestD1HistoryExistingStrategyVersionAccepted` / Unknown→404 |
| G05 | Canonical-symbol authority reutilizada | PASS | `TestD1HistoryCanonicalInstrumentAuthority`; sin registro paralelo |
| G06 | PUT acepta snapshot SQX+MT5 completa y persiste | PASS | ciclo 201 CREATED verificado en suite HTTP |
| G07 | 1 trade cerrado = 1 fila | PASS | readback byte-exacto (casos 33-34) |
| G08 | SL y TP obligatorios | PASS | validadores de geometría (casos 4-6) |
| G09 | Replay idéntico = no-op | PASS | UNCHANGED cero churn (caso 38) |
| G10 | PUT válido cambiante reemplaza atómicamente | PASS | REPLACED + convergencia concurrente (casos 39/42) |
| G11 | Operación inválida rechaza request completo | PASS | 422 sin mutación (caso 49) |
| G12 | Fallo a mitad de replacement preserva dataset previo | PASS | rollback forzado post-delete (caso 41) |
| G13 | REFERENCE jamás tocada por replacement | PASS | casos 40 + regresión F-S2-01 (visible e intacta en cada lectura concurrente) |
| G14 | Readback/range query funciona | PASS | `TestD1RangeQueries` + read surface HTTP (source/rangos/order_by/limit) |
| G15 | Suites unit + PG + HTTP/contract pasan | PASS | 139 PG PASS, contracts 20/20, gateway internal ok |
| G16 | Regresiones existentes pasan o clasificadas | PASS | únicamente las 2 preexistencias certificadas (ver Regression status); adaptaciones E-03/E-04 de Shot 1 intactas |
| G17 | Sin side effects PROD/journal/activation/provisioning/capital/broker | PASS | trabajo 100% local en PG desechable; delta productivo sin rutas de trading; tests de no-efectos de Shot 1 verdes |
| G18 | Evidencia Agents-OS + feedback persistidos | PASS | este documento + agent run + feedback + change log + cierre |
| G19 | Consistent read surface (nuevo) | PASS | regresión permanente `torn=0` + reproducer Shot 2 `torn_head_ops=0` (antes 7/441) |
| G20 | Timestamp fidelity (nuevo) | PASS | regresión permanente round-trip exacto + probe Shot 2 `.5Z` fiel (antes truncado) |

## Regression status

- `TestScratch_QueryDB`: FAIL preexistente, modo idéntico al certificado por Shot 1/Shot 2 (`scratch_query_test.go:25: pq: password authentication failed for user "echo_user"`, scratch hardcodeado a DEV compartida). No tocada; no bloquea D1.
- `TestAutomationHandler_HandleMessage_ValidAction`: FAIL preexistente, modo idéntico (`mock: Unexpected Method Call — Execute(context, string, jsontext.Value)`). No tocada; no bloquea D1.
- Ningún failure nuevo introducido por esta branch: el conjunto de fallos del árbol afectado es exactamente el mismo que en `e35d4347` y en baseline `3596fc48` (clasificación de Shot 2).

## Remaining risks (persisten después de D1)

- Migración 064 no aplicada en ninguna base real (DEV `echo-develop` incluida): acción owner por flujo de release. En DEV vigente subsiste además el estado parcial de 061.
- `SymbolMappingInstrumentResolver` es fail-closed: instrumentos sin mapping canónico activo rechazan la ingesta 422; sembrar `symbol_mappings` es acción owner antes de D2/integración.
- Defaults frozen (body 64 MiB, deadline 60s) a medir con datasets multi-año reales en D2; ajustables por ETCD sin cambio de contrato.
- Reemplazo full-snapshot por diseño (M01-M12): volúmenes de millones de filas pagan delete+insert completo; aceptado para V3.
- Los digests D1 quedan congelados de facto por los tests; cualquier cambio de receta exige versionar contrato.
- `TestScratch_QueryDB` sigue conteniendo una credencial versionada en repo (riesgo preexistente registrado en el Environment Contract; fuera del scope D1).

## Final verdict

D1 queda **PASS**: la foundation Echo de historia canónica de estrategias (contrato `strategy-history.v1`, migración 064, replacement atómico idempotente, read surface, autoridades StrategyVersion y símbolo canónico, REFERENCE intocable, cero efectos de trading) está implementada, atacada adversarialmente y corregida en su totalidad; los dos únicos defectos aceptados están cerrados con regresiones permanentes que reproducen el defecto en rojo contra `e35d4347` y pasan en verde, y el gate completo (18 criterios + G19/G20) se re-ejecutó verde sobre `64b616ff` salvo las dos regresiones preexistentes certificadas ajenas a D1.

## Fuentes

- [[I — Independent Verification D1 (Shot 2)]] · [[J — Manager Decision after Shot 2]] · [[D — Acceptance Gate D1]] · [[F — Continuity D1]] · [[G — Implementation Evidence D1 (Shot 1)]]
- Agent run atribuible: `80-agents/journal/agent-runs/2026-09-23-zcode-glm53-d1-echo-foundation-shot3.md`
- Repo `xKoRx/echo`, branch `feature/d1-echo-foundation-final`, HEAD `64b616ff` (local, sin push; worktree registrado `/home/kor/aranea/work/d1-final-20260923/echo`)
