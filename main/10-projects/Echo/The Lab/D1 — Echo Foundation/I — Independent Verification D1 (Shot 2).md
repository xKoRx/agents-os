---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[A — Technical SPEC D1]]"
  - "[[C — Test Plan D1]]"
  - "[[D — Acceptance Gate D1]]"
  - "[[G — Implementation Evidence D1 (Shot 1)]]"
  - "[[H — Manager Review after Shot 1]]"
aliases:
  - D1 independent verification shot 2
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d1
created: "2026-09-23"
updated: "2026-09-23"
---

# I — Independent Verification D1 (Shot 2)

## Propósito

Evidencia de la verificación independiente adversarial (Shot 2) del mandato D1 2026-09-23: intentar falsificar el PASS de Shot 1 contra `e35d4347` sin confiar en sus tests, sin corregir product code y dejando los defectos reproducibles para Shot 3. Ninguna afirmación aquí sin ejecución detrás.

## Contenido

### Alcance de verificación

- Repositorio `xKoRx/echo`; branch de implementación `feature/d1-echo-foundation` HEAD `e35d43474a36d46fee9bf2879c669c75d44a6986`; baseline real `3596fc48` (ancestry lineal verificado: `3596fc48→00e6716a→8bd7308d→a063416a→e35d4347`; merge-base = baseline; 17 archivos, +4311/−9).
- Branch/worktree de verificación propios: `d1-shot2-verify` @ `e35d4347` en worktree aislado (fuera del repo del desarrollador); la branch del desarrollador no fue tocada, no hay merge a master.
- PostgreSQL real desechable propio: 17.11 en `127.0.0.1:15449/d1_verify` (PGDATA y logs bajo el worktree de verificación), schema reconstruido desde cero 000+001..064 con harness propio (`harness/apply_schema.sh`, independiente del run.sh de Shot 1).

### Verificación arquitectural (§5)

Diff completo `3596fc48..e35d4347` inspeccionado por lectura (no sólo nombres): una sola autoridad durable (`echo.canonical_operations` + `echo.strategy_history_state`, FK RESTRICT a `echo.strategy_versions` 061); sin dual-write a TradeSet/E05 (cero referencias a `canonical_trade_sets`/`canonical_metric_sets` en product code); canonical_operations pertenece a Echo (schema `echo`); Lab sin ingestion (sólo lectura futura); sin segunda Strategy identity ni symbol authority (resolver consulta `canonical_symbol`+`is_active` de `echo.symbol_mappings`, lado correcto verificado contra DDL 001); sin escritura de journal/posiciones (grep + test de delta 0 de Shot 1 replicado en lectura); sin activation/provisioning/trading (handler sin productor Kafka ni comandos broker); sin imports Forge/Symphony (imports: stdlib + `lib/pq` + SDK Echo); sin JSONB de trades; sin lifecycle/open/partial/deals/legs (DDL y DTO sin esas columnas/campos); REFERENCE excluido de la sustitución (`DELETE ... AND source IN ('SQX','MT5')`).

### Pruebas nuevas independientes (todas en la branch de verificación, jamás en la del desarrollador)

- `v3/sdk/contracts/d1_shot2_verify_test.go` (10 tests): verificador de digests reimplementado desde la receta documentada (SHA-256 sobre array JSON con escaping propio, sin usar `wire.HashTagged`); orden de entrada irrelevante; sensibilidad (A, B, instrumento, timezone, contenido, count, dataset vacío) y convergencia de representaciones equivalentes con offset distinto; tabla adversarial de decimales (24 formas rechazadas: `1.0`,`1.00`,`01.0`,`+1`,`-0`,`1.`, exponentes, NaN/Inf, whitespace, hex, `.5`, `00`, coma, trailing zeros…); límites NUMERIC(38,18) (20+18 dígitos aceptado verbatim; 21 enteros, 19 fraccionarios rechazados a nivel contrato); fronteras de período (SQX `<A`; MT5 `[A,B)`; `B<=A` rechazado; `closed_at==opened_at` válido; zona IANA inválida); economía exacta big.Rat (`0.1+0.2=0.3` ok; `0.30000000000000004` rechazado; inconsistencia de 1 unidad rechazada; `-0` rechazado); duplicados dentro de dataset, mismo id SQX+MT5 permitido; count/digest mismatch; política wire (claves duplicadas, null tipado, number tokens, dataset ausente, unknown fields retenidos e inertes — incluido intento de smuggling `namespace`/`strategy_version_ref` en el body).
- `v3/sdk/postgres/d1_shot2_verify_test.go` (12 tests contra PG real): concurrencia A vs B 40 iteraciones, replay vs replace 30+20, A/B/C 25 — post-corrida se verifica por lectura directa: head ∈ datasets completos, filas 100% de ese dataset (sin mezcla), counts==head, REFERENCE intacta; replacement concurrente con lector continuo (441 GETs, 30 replacements); rollback real con `pg_cancel_backend` a mitad de transacción y rollback por deadline de contexto (además del seam after_delete); 4 escenarios de datasets vacíos (incluido reemplazo de historia no vacía por ambos vacíos y replay UNCHANGED vacío con digest definido); symbol authority (canónico aceptado; alias/inactivo/inexistente → `UNKNOWN_INSTRUMENT`; `symbol_mappings` sin mutación); tenancy con el MISMO `version_ref` en dos namespaces (GET cruzado 404, replacement de B no toca A, history digests distintos, 404 idéntico para refs desconocidos); inmutabilidad REFERENCE byte-a-byte en put/replay/replacement/empty/failed/concurrent; bulk acotado por sqlmock (700→3 statements, 2000→8, 251→2); readback exacto de decimales largos y límite DB real (PG rechaza 21 enteros por SQL directo); timing e2e 700 ops ≈197 ms / 5000 ops ≈1.28 s, replay sin writes.
- `v3/gateway/internal/d1_shot2_http_verify_test.go` (6 tests, httptest + servicio + PG reales): auth (401 sin/incorrecto token; 503 fail-closed sin token configurado en PUT y GET); smuggling de namespace por body ignorado (historia queda en namespace server-side); 16 ataques wire/HTTP con status exacto (400 duplicados/null/number token/dataset ausente/contract version; 422 enum/geometría/economía/digest/count/21-enteros/19-fraccionarios/símbolo desconocido; 404 versión desconocida; 413 oversized; 400 UTF-8 malformado); read surface (order_by inválido 400 no 503, source filter, rangos opened/closed, limit, orden determinista con empates, REFERENCE visible vía `source=REFERENCE`, sin exposición cross-tenant); ciclo 201 CREATED → 200 UNCHANGED → 200 REPLACED; sondeo de proyección sub-segundo del GET.
- Race detector (`go test -race`): limpio en contracts, en la batería de concurrencia PG y en la batería HTTP.

### Resultados

- Contracts: `TestShot2*` 10/10 PASS (paquete completo 95.1% coverage, verde).
- Postgres (DATABASE_URL 15449): paquete completo verde salvo `TestScratch_QueryDB` (preexistente, ver Regresiones); `TestShot2*` 12/12 PASS.
- Gateway: `v3/gateway/internal` verde (incluye D1 de Shot 1 + 6 nuevos); `v3/lab-worker/...` 5/5 paquetes ok; único FAIL del árbol gateway: `TestAutomationHandler_HandleMessage_ValidAction` (preexistente).
- Migración 064 desde PG vacío: apply estricto OK; segunda aplicación idempotente OK; probe `BEGIN+064+ROLLBACK` sin objetos residuales (99 tablas antes/después); down 064 deja 0 objetos D1 y PG063 íntegro; re-up reconstruye constraints/índices/FK verificados por catálogo.
- Regresiones reproducidas en baseline `3596fc48` (checkout master limpio, go.work externo sin tocar el repo): `TestScratch_QueryDB` y `TestAutomationHandler_HandleMessage_ValidAction` fallan IDÉNTICAMENTE en baseline y en `e35d4347` ⇒ clasificación preexistente CONFIRMADA (mismo modo de fallo, mismo conjunto).
- Seed tests ETCD no ejecutados (Environment Contract; sin `go test ./...` raíz).

### Hallazgos

| ID | Severidad | Alcance | Reproducer |
|---|---|---|---|
| F-S2-01 | MEDIUM | Read surface: `GetHistory` lee head y operaciones en dos statements sin tx de lectura; un replacement que commitea entre ambos produce una respuesta GET que empareja head (digest/counts) de un snapshot con operaciones de otro. Sin mezcla de filas y sin corrupción durable (el par head+ops persistido siempre es consistente). | `TestShot2ConcurrentReadDuringReplace` (worktree de verificación): 30 replacements con lector continuo ⇒ `reads=441 mixed_rows=0 torn_head_ops=7`. |
| F-S2-02 | LOW | Proyección HTTP del GET formatea instantes con `time.RFC3339` (segundos): filas con fracción de segunda se leen truncadas (DB guarda microsegundos; el repo lee exacto; sólo el wire del GET pierde precisión). Emparenta con la observación de que la receta de digest lleva nanosegundos mientras PG persiste microsegundos (replay/UNCHANGED no se ven afectados; el digest se calcula del request, no de la DB). | `TestShot2HTTPGetSubSecondProjection`: fila `10:00:00.5Z` leída `10:00:00Z` por GET. |

Observaciones informativas (no defectos): fast-path `UNCHANGED` es read-only y no linealizable respecto a un replacement en vuelo (benigno: cero efecto durable, el replay posterior converge bajo lock); `pg_advisory_xact_lock(hashtext(ns),hashtext(ref))` puede sobre-serializar identidades distintas por colisión teórica de hash (no rompe corrección); el request vive en memoria ~3-4× su tamaño (decode raw + structs + inserts), coherente con el techo configurable de 64 MiB vía ETCD.

### Correcciones mínimas propuestas para Shot 3

1. F-S2-01: ejecutar head+operaciones de `GetHistory` dentro de una única transacción de lectura (misma snapshot; `REPEATABLE READ` o al menos ambas queries en una tx read-only) en `v3/sdk/postgres/strategy_history_service.go`.
2. F-S2-02: usar `time.RFC3339Nano` (o millisecond RFC3339) en `projectHistoryHead` para `opened_at`/`closed_at`/`training_end_at`/`live_start_at` en `v3/gateway/internal/strategy_history_handler.go`, y versionar el contrato si se considera breaking para consumidores.

## Fuentes

- [[A — Technical SPEC D1]] · [[C — Test Plan D1]] · [[D — Acceptance Gate D1]] · [[F — Continuity D1]] · [[G — Implementation Evidence D1 (Shot 1)]] · [[H — Manager Review after Shot 1]]
- Agent run atribuible: `80-agents/journal/agent-runs/2026-09-23-zcode-glm53-d1-echo-foundation-shot2.md`
- Worktree de verificación (branch `d1-shot2-verify` con tests reproducers, sin push): repositorio `xKoRx/echo`, worktree externo registrado 2026-09-23; PG desechable `127.0.0.1:15449/d1_verify` con schema 001..064 y datos de prueba.
