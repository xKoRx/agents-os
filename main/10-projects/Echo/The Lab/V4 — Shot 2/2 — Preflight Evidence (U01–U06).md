# V4 Shot 2 — Evidencia de preflight (U01–U06 + A01/A02), revisión 2

**Fecha de recolección:** 2026-10-20 23:48–00:40 CLST y 2026-10-21 11:15–11:40 CLST. **Emitida por:** Submanager Shot 2 (GLM-5.3-Flash Max, host daedalus, local). **Naturaleza:** trabajo directo read-only del submanager; NO constituye verificación independiente (reconocido en el dictamen Manager 2026-10-21). Los deltas de repo se citan contra `xKoRx/echo` @ `d74b6525` (origin/master 2026-10-20) y rama `origin/feature/e04-dev-ingest-recovery` @ `4aad647b`; PG DEV = `echo-develop` @ .220 vía MCP `aranea-postgres-rw` (sólo SELECT). Sin secretos; sin dumps pesados.

**Clasificación de estados:** `VERIFIED` = evidencia mecánica reproducible obtenida por consulta/comando citado; `SPECIFIED_FOR_IMPLEMENTATION` = diseño fijado en el paquete rev 2, por demostrar en implementación; `NOT_DEMONSTRATED` = frontera abierta, acotada a la acción que bloquea.

## Correcciones respecto de FINDINGS-U01-U06.md (2026-10-20)

| # | Afirmación de la rev 1 | Estado real verificado | Evidencia |
|---|---|---|---|
| C1 | "065 (lab_curves_v3) NO aplicada en DEV" | **FALSA.** `echo.lab_curves`, `lab_curve_points`, `lab_curve_metrics` existen en DEV con el schema exacto de 065 (registry_namespace, strategy_version_ref, algorithm_id, algorithm_version, config_digest, history_digest…) y owner `echo_user`. El efecto de 065 está aplicado a mano como el de las demás | E06 |
| C2 | "distribución del journal: mediana ~500, p95 ~25k ops" | **Incorrecta.** Distribución real REFERENCE por (strategy_id, canonical_symbol): 210 grupos, p50=19, p75=33, p95=59, p99=24.682, max=56.884 ops; por strategy_id: 131, p50=30, p95=64, max=132.805. Los SLOs y el workload del benchmark se congelan con la distribución medida | E09 |
| C3 | "DEV con efectos aplicados a mano, sin tabla de control" (alcance parcial) | **Alcance completo:** DEV NO tiene ninguna tabla `schema_migrations` en ningún schema; toda la historia 001→065/068-carece de control. La reconciliación de la tabla de control es prerrequisito del plan de migraciones, no un detalle | E05 |
| C4 | "066 sin aplicar en DEV" | **Confirmada.** No existen `echo.futures_*`; además el Core DEV desplegado (binario 2026-10-20 04:05) no muestra actividad de proyector ni del topic en logs recientes (0 líneas en últimas 200 y en ventana 20:00+) | E08 |

## E01 — Divergencia e04 vs master (R01)

- **Entorno:** clon `~/aranea/work/lab-v4-shot2-20261020/echo` (daedalus). **Fecha:** 2026-10-21.
- **Comando:** `git log --oneline d74b6525..4aad647b`; `git rev-list --count 4aad647b..d74b6525`; `git diff d74b6525...4aad647b --stat`.
- **Resultado:** 5 commits exclusivos de e04 (`2360369c` seeds+ingest wiring, `2498042f` policy_id gate, `3d260e81` platform token + migración, `988e0ae6` guard DeleteVar/dump mirror, `4aad647b` renumber 064→068); 305 commits del lado master; diff 34 archivos (+1.388/−852).
- **Limitación:** equivalencia por contenido verificada por lectura de diffs y `git cherry` (patch-id), no por ejecución de tests de ambas ramas.
- **Referencia:** reproducible con los mismos comandos en cualquier clon que tenga ambos refs.

## E02 — Protección de seeds: master ya supera la variante e04 (R01)

- **Entorno:** ídem E01. **Fecha:** 2026-10-21.
- **Comando:** `git show d74b6525:v2/sdk/etcd/echo_seed_test.go` (y `v3/sdk/etcd/echo_seed_test.go`).
- **Resultado:** master contiene `//go:build seeds` + `requireSeedAuthorization` (opt-in `ECHO_SEED_ALLOW`, `ETCD_ENDPOINTS` obligatorio, guard `isProductionClusterHost` contra apuntar DEV al clúster PROD) en v2 y v3. e04 además trae tooling nuevo (`v3/sdk/etcd/bootstrap.go` +215, `echo_config.go` +80, `cmd/echo-etcd-bootstrap` +127) y reescritura de seed tests que master no necesita.
- **Limitación:** no se ejecutaron las suites `seeds` de ninguna rama (prohibido: escritura ETCD).
- **Referencia:** repo `xKoRx/echo`, paths citados.

## E03 — e04 modifica 061 en sitio (R01)

- **Entorno:** ídem. **Fecha:** 2026-10-21.
- **Comando:** `git diff d74b6525...4aad647b -- v3/sdk/postgres/migrations/061_identity_bwc_foundation.up.sql`; `git log --oneline 4aad647b -- <061>`.
- **Resultado:** el commit `2360369c` agrega a 061 `echo.fn_mig061_owned()` y convierte en condicionales los drops de `v_lab_strategy_screener` y de 4 constraints FK de tablas `lab_*`. Es un **edit in-place de una migración ya aplicada** — se rechaza su adopción; la intención (lab legacy admin-owned en DEV) se captura en la migración nueva de retiro legacy de V4 con guard de ownership equivalente.
- **Limitación:** ninguna material; la intención está además confirmada físicamente en E07.
- **Referencia:** diff citado.

## E04 — Migración 068 y CHECK de plataforma ya aplicado a mano en DEV (R01)

- **Entorno:** repo + PG DEV. **Fecha:** 2026-10-21.
- **Comando:** `git show 4aad647b:v3/sdk/postgres/migrations/068_strategy_version_forge_platform.up.sql`; SQL: `SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid='echo.strategy_versions'::regclass AND contype='c'`.
- **Resultado:** 068 reemplaza `chk_strategy_versions_platform` a `IN ('MT5','MT4','MetaTrader5','MetaTrader4')` (down se niega si hay filas Forge); DEV YA tiene ese CHECK de 4 tokens (efecto aplicado a mano, archivo de migración ausente de master). La receta de identidad `contracts.StrategyVersionRef` incluye `target_platform` en el hash (`v3/sdk/contracts/evidence.go:16-31`) → normalizar la grafía cambiaría `version_ref`; los tokens sellados se preservan tal cual.
- **Limitación:** ninguna.
- **Referencia:** diff + SQL citados.

## E05 — DEV sin tabla de control de migraciones (R01)

- **Entorno:** PG DEV. **Fecha:** 2026-10-21.
- **Comando:** `SELECT table_name FROM information_schema.tables WHERE table_name ILIKE '%migration%'` (sin filtro de schema).
- **Resultado:** 0 filas. El runner canónico es golang-migrate + `schema_migrations` (header de 061; toolkit `v3/toolkit/cmd/apply-migration`), pero DEV nunca tuvo la tabla.
- **Limitación:** la reconstrucción del estado "qué migración quedó aplicada" se hará por verificación de efectos objeto a objeto en la tarea de reconciliación (no por la tabla, que no existe).
- **Referencia:** SQL citado.

## E06 — 065 aplicada en DEV, owner echo_user (R01 — corrige C1)

- **Entorno:** PG DEV. **Fecha:** 2026-10-21.
- **Comando:** SQL `information_schema.columns` sobre `echo.lab_curves`; join `pg_class/pg_roles`.
- **Resultado:** schema de `lab_curves` coincide campo a campo con `065_lab_curves_v3.up.sql` (única migración que crea esas tablas); owner `echo_user`.
- **Limitación:** contenido (filas) no auditado; irrelevante para el plan (V4 reemplaza las superficies lab legacy).
- **Referencia:** SQL + archivo de migración.

## E07 — Objetos lab legacy admin-owned en DEV (R01/R03 — soporta el guard)

- **Entorno:** PG DEV. **Fecha:** 2026-10-21.
- **Comando:** `SELECT c.relname, r.rolname FROM pg_class c ... WHERE relname IN ('v_lab_strategy_screener','lab_strategy_segments','lab_canonical_trades','lab_strategy_outcomes','lab_strategy_metric_snapshots',...)`.
- **Resultado:** los 5 objetos citados por el guard de e04 son owner `admin`; `strategy_versions`, `promotion_records`, `canonical_operations`, `trade_journal`, `lab_curves*` son owner `echo_user`. No existen `strategy_histories` ni `futures_*`.
- **Limitación:** ninguna.
- **Referencia:** SQL citado.

## E08 — 066 sin objetos y proyector sin actividad observable (R05)

- **Entorno:** PG DEV + systemd/journalctl --user (daedalus, servicios DEV). **Fecha:** 2026-10-21.
- **Comando:** SQL `information_schema.tables WHERE relname IN ('futures_operations','futures_fills',...)`; `systemctl --user list-units --type=service --state=running | grep echo`; `journalctl --user -u echo-core-dev.service -n 200 --no-pager | grep -icE "projector|operation-facts"`.
- **Resultado:** 0 tablas `futures_*` (066 sin aplicar en DEV); servicios DEV activos: `echo-core-dev` (StateFun :9090), `echo-gateway-dev` (:8090), `echo-front-dev` (:4173); binarios desplegados `echo-core` 2026-10-20 04:05, `echo-gateway` 2026-10-19 10:19; 0 líneas de proyector/topic en logs recientes.
- **Limitación:** observación directa sobre DEV; **PROD no inspeccionado** (fuera de alcance por mandato): la existencia de consumidores físicos de 066 en PROD queda `NOT_DEMONSTRATED` y bloquea sólo el retiro/drop de 066, no el desarrollo.
- **Referencia:** comandos citados.

## E09 — Distribución real del journal y tamaños serializados (R06)

- **Entorno:** PG DEV. **Fecha:** 2026-10-21.
- **Comando:** `SELECT strategy_id, canonical_symbol, count(*) FROM echo.trade_journal WHERE account_role='REFERENCE' AND status IN ('CLOSED','CLOSED_BY_USER','CLOSED_BY_AGENT') GROUP BY 1,2` + `percentile_cont`; medición de bytes: `octet_length(jsonb_agg(jsonb_build_object(<campos wire v1>))::text)` sobre 3 grupos representativos.
- **Resultado:** 210 grupos (strategy, symbol): p50=19, p75=33, p95=59, p99=24.682, max=56.884 ops; 131 estrategias: p50=30, p95=64, max=132.805. Tamaño: 412–421 B/op; p50 ≈ 7,9 KB; p95 ≈ 24,8 KB; p99 ≈ 10,3 MB; **max medido 23,65 MB (56.884 ops)**. El formato medido es NDJSON/JSON con los 16 campos de `CanonicalOperationInputV1`; el envelope real añade cabecera y digests (mismo orden de magnitud).
- **Limitación:** la serialización de medición fue jsonb de PG (no el serializador Go canónico); delta esperado <10%. La historia max (132.805 ops de una estrategia completa multi-símbolo) no se serializó entera: su cota superior es ~55 MB (132.805 × 421 B) — excede el request único de 64 MiB sólo combinada con otra historia grande; los caps por historia lo cubren.
- **Referencia:** SQL citado; campos wire en `v3/sdk/contracts/strategy_history.go`.

## E10 — Cobertura de risk_money en journal (R03)

- **Entorno:** PG DEV. **Fecha:** 2026-10-21.
- **Comando:** `SELECT account_role, count(*), count(risk_money) FROM echo.trade_journal GROUP BY 1`.
- **Resultado:** REFERENCE 137.276 filas, 88.750 con risk_money (64,7%); EXECUTION 245.438, 101.543 (41,4%). Semántica del emisor (`v3/core/internal/functions/mm_engine.go:892-960`): riesgo inicial pre-offset **por ticket** del slave, calculado por el Core como única autoridad (`ComputeCanonicalRisk`, SL del master proyectado al broker del slave; NULL si no computable); `MoneyManagementType` FIXED_LOT/FIXED_RISK_USD.
- **Limitación:** semántica de ticket, no de presupuesto de ciclo declarado (ver taxonomía R03 en el paquete).
- **Referencia:** SQL + archivo:línea.

## E11 — Volúmenes DEV de identidad/historia (U06)

- **Entorno:** PG DEV. **Fecha:** 2026-10-21.
- **Comando:** counts sobre `strategy_versions`, `strategy_identity_mappings`, `promotion_records`, `strategy_history_state`, `canonical_operations`.
- **Resultado:** 6 versiones (2 plataformas distintas), 7 mappings, 6 promotion_records, 1 history head, 14 canonical_operations (14/14 con `initial_risk_money > 0`).
- **Limitación:** dataset pequeño de verificación; sirve de fixture, no de muestra estadística.
- **Referencia:** SQL citado.

## E12 — Contratos del motor y autoridad económica (R02/R03)

- **Entorno:** repo @ `d74b6525`. **Fecha:** 2026-10-21.
- **Comando:** lectura de `v3/sdk/futures/domain/operation.go` (Operation/Order/Fill), `v3/sdk/futures/operation/engine.go:1051` (pin de `MMConfigSnapshot` al materializar), `v3/sdk/futures/operation/wire.go:64` (OperationFact), `v3/sdk/futures/accounting/ledger.go` (`ApplyFill(fill, feePerContract)`, realización exacta por ticks + fee por contrato/lado), `v3/sdk/futures/domain/economics.go:44` (EconomicPlanRow), `v3/core/internal/functions/mm_engine.go:533-538` (sello canónico del riesgo en CoreCommand).
- **Resultado:** el agregado Operation ya transporta MMConfigSnapshot pinneado al materializar y Orders con parciales (`CumulativeFilledQty`); el Ledger es la autoridad existente de realizaciones/costes (usado por el backtester; aún no cableado a los facts del runtime live); el sello de riesgo por ticket vive hoy en el Core (motor MT4/MT5), no en el motor futures.
- **Limitación:** ninguna para nivel de contrato; la verificación conductual (parciales/costes → historia) queda como caso verificable T de implementación.
- **Referencia:** archivos:líneas citados.

## E13 — Replacement V1 destructivo y patrón de receipts (R04)

- **Entorno:** repo @ `d74b6525`. **Fecha:** 2026-10-21.
- **Comando:** lectura de `v3/sdk/postgres/strategy_history_service.go:100-160` y `v3/sdk/postgres/migrations/061_identity_bwc_foundation.up.sql:394-414` (promotion_records); `v3/gateway/internal/strategy_history_handler.go:85` (`readLimitedBody` sobre el request completo) y `v3/gateway/internal/config.go:96` (`historyDefaultMaxBodyBytes = 64 MiB`).
- **Resultado:** el replacement V1 hace `DeleteImportedOperations` (DELETE+INSERT) → destruye la revisión previa; `promotion_records` ya implementa el patrón receipt (idempotency_key sha256, payload_digest, accepted_body_canonical jsonb, status) — el nuevo receipt de ingestion será tabla propia con ese patrón, sin generalizar promotion_records. El límite de 64 MiB aplica al **request completo** (v1: PUT de historia; v2: POST version+historias), sin partial success.
- **Limitación:** ninguna.
- **Referencia:** archivos:líneas citados.

## Clasificación de consumidores que determinan naming/cutover (R05 — U05)

| Clase | Elementos | Verificación | Determina |
|---|---|---|---|
| Procesos desplegados (DEV) | echo-core-dev (StateFun :9090), echo-gateway-dev, echo-front-dev | VERIFIED hoy (E08) | ventanas de deploy y cutover de topics |
| Productores del topic `echo.futures.operation-facts.v1` | operation owner (StateFun), futuresruntime, futures-bridge | VERIFIED en código (`v3/sdk/statefun/futures_constants.go:128`, `v3/sdk/futures/operation/wire.go:40`) | naming del topic v2 y cutover de productores |
| Consumidores del topic v1 | proyector 066 (código en repo; sin actividad observable en DEV; tablas ausentes) | VERIFIED ausencia física DEV; PROD NOT_DEMONSTRATED | retiro de 066 (drop gated, nunca por grep) |
| Dependencia build-time `v3/sdk/futures` | backtester (49 archivos), core functions/futuresruntime/futuresvertical, futures-bridge, projector | VERIFIED en código (inventario 2026-10-20) | secuencia de renombres Go, coordinación con `feature/ef-runtime-pools` (dueña del grammar de typenames Java) |
| Identidad de contrato compartida | `contracts.StrategyVersionRef` (platform en el hash) | VERIFIED (E04) | prohibición de normalizar tokens sellados |
| Superficies lab legacy (front/Hasura/SQL/worker) | inventario 2026-10-20 (backend, 4 cmds worker, 3 jobs SQL, LabView.vue, 8 yamls Hasura) | VERIFIED en código | inventario CURRENT→TARGET (REUSE/ADAPT/REPLACE/DELETE/OUT_OF_SCOPE) en primera tarea de integración |
| Frontera abierta | consumidores físicos en PROD de 065/066 y de naming futures | NOT_DEMONSTRATED (sin acceso PROD por mandato) | bloquea SÓLO el drop/retiro de 066 en cualquier entorno compartido con PROD; no bloquea desarrollo, migraciones aditivas 067+ ni cutover en DEV |

## Estado U01–U06 / A01 / A02 tras la reparación

| Unidad | Estado | Base |
|---|---|---|
| U01 lineage versión/MM/Q_i | VERIFIED (flujos existentes) + Q_i runtime SPECIFIED_FOR_IMPLEMENTATION | E10, E12 |
| U02 histórico/retención/reproducción | VERIFIED (gap destructivo comprobado) + revisionado SPECIFIED_FOR_IMPLEMENTATION | E13 |
| U03 tamaños/transporte | VERIFIED (medido 2026-10-21) | E09, E13 |
| U04 capacidad/SLOs | SPECIFIED_FOR_IMPLEMENTATION (metodología y gates congelados; runtime inexistente NO certificado) | paquete §R06 |
| U05 naming/migración | VERIFIED (inventario código + física DEV) con frontera PROD NOT_DEMONSTRATED acotada | E03-E08, tabla consumidores |
| U06 baseline/entornos | VERIFIED (re-verificado 2026-10-21) | E01-E07, E11 |
| A01 | PARCIAL (igual que rev 1): IDs estables demostrados; Q_i genérico inexistente, delta especificado | E10, E12 |
| A02 | SÍ con condición (igual que rev 1): retención posible con registro de revisiones + artefacto por revisión | E13 |
