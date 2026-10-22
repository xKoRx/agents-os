---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[0 — Submanager State]]"
  - "[[SHOT3_ADVERSARIAL_REPORT]]"
  - "[[SHOT4_EXECUTION_PACKAGE]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-21"
updated: "2026-10-21"
---

# SHOT4_HANDOFF

## Propósito

Handoff final de Shot 4 (SHOT4_AUTHORIZED_CORRECTIONS_AND_I1_COMPLETION): correcciones S3-F01–F08, capacidades S3-M01–M06, evidencia S3-E01, límites S3-E02 conservados. Ejecutor: Implementation Submanager LOCAL (motor efectivo GLM-5.3-Flash, host-declarado; el perfil GPT-6-Luna del encabezado del mandato no pudo verificarse desde este runtime y se registra la discrepancia). Corte de entrada `xKoRx/echo@61ac1f720d07513e48b0310b84b5b415b80ff48f`; rama de producto `feature/lab-v4-shot4`; SHA final del candidato `ed458c5e` (9 commits desde el corte: 6 implementación + fixes revisor 1 + 3 de la devolución PM + fixes F1-F3 del revisor acotado). PG descartable propio 54349 (`~/aranea/work/lab-v4-shot4-20261021/pgdata`), sin tocar servicios compartidos ni el clon Shot 2.

## Estados separados (dictamen PRIMARY MANAGER 2026-10-21)

| Estado | Valor |
|---|---|
| IMPLEMENTATION_COMPLETENESS | **I1_PARTIAL → I1_COMPLETADO_EN_FUNCIONAL** — faltantes CODE_MISSING del dictamen cerrados en este mismo Shot 4 (selección, wiring B, comparación, portfolios snapshot); ver Inventario de sustitución |
| FUNCTIONAL_VERIFICATION | **PASS** en entorno aislado (PG descartable 54349 + HTTP real + front build); sin deploy |
| INDEPENDENT_DELTA_REVIEW | **COMPLETE_ACOTADA** — revisor fresco sobre 2eccb317 (SHOT4_DELTA_WITH_FINDINGS, resuelto); nueva revisión acotada del delta 2eccb317→final en curso al cierre |
| EXTERNAL_INTEGRATION | **PENDING_AUTHENTIC_FORGE_ARTIFACT** (G11; orígenes consultados registrados); metadata Hasura preparada sin aplicar |
| DEPLOYMENT_AND_CUTOVER | **NOT_DEPLOYED** — sin merge, sin deploy, cutover/071 gated por autorización (BLOCKED_EXTERNAL_PERMISSION) |
| SECURITY_DYNAMIC_COVERAGE | **NOT_RUN — harness safety restriction** (S3-E02; T33/T36) |

## Registro de implementación

| Commit | Paquete | Contenido |
|---|---|---|
| `adfd3be0` | P0–P3 | S3-F01–F08 (ingesta exacta, revisiones inmutables, receipts semánticos, down 067, fixtures) |
| `04158d51` | P4–P5 | S3-M01 HTTP v2; S3-M02 Q_i causal + lab/opfacts |
| `99574e0f` | P6 | S3-M03 cola transaccional + worker + 4 perfiles + B.6.5 |
| `52fe4cb9` | P7 | S3-M04 read models + rutas + tab Vue + metadata (archivo) |
| `540e045c` | P8 | S3-M05 composición estática D11 |
| `fa24546f` | P9 | S3-E01 capacidad ingesta + worker binario + orden O(n log n) |
| `2eccb317` | Revisión | fixes del revisor independiente (TestQISeal engine, N-reproducible, precisiones) |
| `a2b40827` | **Dictamen PM 1** | I1 restituido: servicio selección principal/alternativas (069), invalidación transaccional, PORTFOLIO_SNAPSHOT worker con CAS, comparación de copias, rutas gateway, paneles Vue, demo 7 flujos |
| `6cb00134` | **Dictamen PM 2** | Wiring B real: projector sink (ruta runtime) + backtester observer (ruta BACKTEST) vía opfacts.FactsPublisher compartido; 2 demos de recorrido de producto |
| `8a7381fd` | **Dictamen PM 3** | Evidencia separada: cómputo REAL 4 perfiles sobre 132.805 ops, lease recovery, grano dual en curvas (CLOSED_SUMMARY por cierre), coverage enfocado medido |
| `ed458c5e` | **Revisor acotado** | F1 identidad real fail-fast (jamás slots sintéticos); F2 log de cómputo preservado; F3 operation_count real en lab.curves |

## Matriz caso por caso (requisito → implementación → test → SHA → resultado → evidencia)

### Gates G1–G11

| Gate | Requisito | Implementación | Test | SHA | Resultado | Evidencia |
|---|---|---|---|---|---|---|
| G1 | Ingesta vertical usable | handler HTTP v2 + receipts + CAS + catálogo | TestStrategyHistoryV2_FullVertical; A01-A23 | 2eccb317+ | PASS | HTTP real+PG 54349; 23/23 repros |
| G2 | Grano dual + economía por Operation | servicio v2 + opfacts Tracker identificación específica | A01/A02/A18; TestABLogicalVsAccountFIFO; TestPartialExitsFortyPercentR; productpath | 8a7381fd | PASS | A/B=5 vs FIFO=15 visible; 0.4R; net=14 en PG |
| G3 | Cuatro perfiles + métricas B.6.5 | lab/analyze puro + worker | TestLabWorkerOracles; TestLabCapacityCompute132k; compute_test.go | 8a7381fd | PASS | +114/10.100/10.098 en DB; 132k×4 perfiles 1.7-3.3s |
| G4 | Metadata D16/MM + selección | snapshot completo + header_json + read model + servicio selección | A05; TestLabSelectionFlowsI1; TestLabCatalogAndStaleness | a2b40827 | PASS | metadata round-trip; 7 flujos; STALE visible |
| G5 | Retención + cadena inmutable + receipts | guards 069 + sink obligatorio + receipts semánticos | A03-A05/A09-A17; TestLabWorkerObsoleteWorkerAndFencing | 2eccb317 | PASS | 15/15 sondas SQL hostiles (revisor) |
| G6 | Experiencia visible | read models + tab Vue + selección + portfolios | TestLabCatalogAndStaleness; vite build; TestStrategyHistoryV2_FullVertical | a2b40827 | PASS funcional | flujos demostrados por servicio+rutas; UI read-only |
| G7 | Composición estática D11 | analyze.ComputePortfolio + CreateLabPortfolio + snapshot worker | TestPortfolioSixtyForty; TestLabPortfolioCreateAndCompose; flujo 6 TestLabSelectionFlowsI1 | a2b40827 | PASS | 60/40⇒6k/4k; allocations publicadas en DB |
| G8 | Copias/referencias | comparación con evidencia disponible (digest idéntico ⇒ copia; deltas READY; insuficiencias explícitas) | flujo 4+7 TestLabSelectionFlowsI1 | a2b40827 | PASS (básico I1) | sin correlaciones inventadas |
| G9 | Sustitución legacy | V4 conectado; 071 gated | TestLabV4RetirementSafeByDefault | 2eccb317 | PARCIAL | clasificación por superficie abajo; BLOCKED_EXTERNAL_PERMISSION |
| G10 | Capacidad | ingesta 132.805 + cómputo 4 perfiles + catálogo 20k + lease recovery | TestLabCapacity132k; TestLabCapacityCompute132k; TestLabCatalog20kPageLatency; TestLabWorkerLeaseRecovery | 8a7381fd | PASS (dev) | 2m40s ingesta (884 ops/s revisor); 1.7-3.3s/perfil; ~65ms página; recovery OK |
| G11 | Forge auténtico | — (búsqueda en ubicaciones canónicas sin resultado) | — | — | PENDING | ver EXTERNAL_INTEGRATION |

### Casos T (sólo los que cambian o dependen de lo nuevo; el resto conservan su estado del corte 2eccb317 verificado por el revisor)

| Caso | Requisito | Test | Resultado |
|---|---|---|---|
| T04/T16 | curva por historia visible + historia vs alternativas | TestLabSelectionFlowsI1 (flujo 4) | PASS |
| T07/T40 | atribución por Operation + curva R por parciales | TestABLogicalVsAccountFIFO + TestPartialExitsFortyPercentR + productpath | PASS |
| T13/T42 | PUT snapshot completo + N reproducible | A05 + TestLabWorkerNReproducibleAfterNPlusOne | PASS |
| T14/T15 | publicación worker V4 + claim/lease/fencing | TestLabWorker* + TestLabWorkerLeaseRecovery + 132k | PASS |
| T16-T19 | selección/alternativas/comparación/D16 | TestLabSelectionFlowsI1 + read models | PASS |
| T21/T22 | algoritmos causales (open balance / initial balance) | compute_test.go TestNormalizedOracles + oráculos DB | PASS |
| T24 | capital agotado calculado | compute_test.go + portfolio exhausto | PASS |
| T30/T31/T41 | portfolio DDL→servicio + composición + start flat | portfolio_test.go + CreateLabPortfolio + flujo 6 | PASS |
| T37/T38 | manifiesto completo + coalescing | TestLabWorkerEnqueueAndCoalesce + manifest CAS | PASS |
| T43/T44/T45 | window_local/curve_running + selección + paneles | ComputeMetrics (curve_running) + selección + Vue | PARCIAL — window_local definido en catálogo, paneles por ventana en I2 de UI |
| T33/T36 | seguridad dinámica | — | NOT_RUN — harness safety restriction |
| T34 | migración proyección/adapters | M01-M04 + wiring B (6cb00134) | PASS |
| T08/T27/T28 | Forge auténtico/copia adapter | — | PENDING artefacto (G11); sintético cubre contrato |

### Casos C01–C06

| Caso | Estado | Evidencia |
|---|---|---|
| C01 | CERRADO | cadena 067→071 + atomicidad + retiro safe-by-default (TestLabV4 7/7) |
| C02 | CERRADO | recetas identity + mismo version_ref al recalcular (TestLabV4PlatformKindsIdentityRecipes) |
| C03 | CERRADO | Q_i causal sello una sola vez + tags distintos (TestQISeal_* + TestEntryDecisionCarriesCycleBudget) |
| C04 | CERRADO | grano dual + A/B=5 + parciales/costes + conciliación (opfacts + productpath) |
| C05 | CERRADO | sink obligatorio + cadena única + N reproducible + artefacto write-ahead (A03-A05/A09/A22 + N-reproducible) |
| C06 | CERRADO (caps) / MEDIDO (capacidad) | caps semánticos + 413 real; capacidad separada por fase (abajo) |

## Evidencia de capacidad SEPARADA por fase (dictamen PM item 5)

| Fase | Evidencia | Límite declarado |
|---|---|---|
| Transporte HTTP V2 | 413 real con MaxBytesReader (TestStrategyHistoryV2_PayloadTooLarge); techo 128MiB configurado | memoria de decodificación acotada por MaxBytesReader; medición de RSS del gateway: NOT_DEMONSTRATED (sin entorno de carga) |
| Persistencia de historia | 132.805 ops íntegras vía servicio común: 2m40s (828 ops/s propio; 884 ops/s revisor) — log preservado | medición local; no extrapolada a 25k ni a concurrencia |
| Cálculo y publicación | 4 perfiles sobre 132.805 ops: 1.7–3.3s cómputo por perfil, 132.805 puntos c/u, filas READY visibles (TestLabCapacityCompute132k) | cómputo secuencial de un worker; paralelismo no medido |
| Catálogo 20k | página 1 ≈65ms, página cursor ≈60ms (LIMIT 50) | consulta paginada; sin carga de 20k historias completas |
| Carga analítica y backlog | drenaje filtrado demostrado; backlog masivo concurrente: NOT_DEMONSTRATED (worker único secuencial en I1) | — |
| Recuperación y recursos | lease vencido → reclaim + fencing monotónico (TestLabWorkerLeaseRecovery); memoria: go test estándar sin límites (RSS no medido: NOT_DEMONSTRATED) | — |

Coverage crítico medido (no se cierra el gate 95%): lab/analyze **88.1%** (oráculos y estados honestos cubiertos; faltan ventanas window_local y ramas de formato), lab/opfacts **52.3%** (núcleo económico cubierto; faltan ramas de error y adapter PG), postgres (paquete legacy+V4): no medido globalmente — el gate de coverage queda **NO_MET con números**, no declarado.

## Inventario de sustitución — clasificación por estado (dictamen PM item 4)

| Superficie | Estado | Detalle |
|---|---|---|
| Ruta runtime → LAB (projector) | **SOURCE_READY_NOT_DEPLOYED** | sink + config LAB_HISTORY_* + demo producto (6cb00134); deploy requiere ownership del proceso DEV |
| Ruta backtester → LAB | **SOURCE_READY_NOT_DEPLOYED** | RunState.SetLabFactsObserver + demo (6cb00134); wiring del binario de campaña a config queda en la operativa del run |
| Experiencia LAB (front) | **SOURCE_READY_NOT_DEPLOYED** | tab V4 + selección + portfolios (build OK); deploy front requiere ownership |
| lab.curves/points/metrics + portfolios (070) | **SOURCE_READY_NOT_DEPLOYED** | migraciones no aplicadas a ninguna base compartida |
| Selección principal (069 tabla+servicio) | **SOURCE_READY_NOT_DEPLOYED** | ídem |
| echo.lab_curves D3 (065) + LabCurveRepository | **RETIRED_VERIFIED=NO / BLOCKED_EXTERNAL_PERMISSION** | consumidores actuales en DEV sin verificar ownership; retiro real = 071 gated (071 BLOCKED_SKIP honesto) |
| Worker legacy (lab-canonical-a0, lab-materialize-pg) | **BLOCKED_EXTERNAL_PERMISSION** | proceso DEV ajeno; lab-worker-v4 disponible (SOURCE_READY) |
| Metadata Hasura lab.* | **SOURCE_READY_NOT_DEPLOYED** | yaml read-only en repo; apply requiere ownership |
| Migraciones históricas 001-066 y adapters específicos de mercado | **PROTEGIDOS (OUT_OF_SCOPE)** | no se tocan para lograr un grep sin "futures"; journals/recovery intactos |
| Nomenclatura genérica | **PARCIAL_VERIFICABLE** | lab.* + execution.* genéricos en V4; la transición restante está en las filas SOURCE_READY/BLOCKED de arriba (no se declara completa por naming) |

## EXTERNAL_INTEGRATION — registro exacto G11

Artefacto requerido: sealed handoff Forge (forge_seal_handoff_v1) auténtico o equivalente autorizado. Orígenes consultados (read-only, 2026-10-21): `/srv/echo-work/runs/*` (17 directorios de campañas), `/srv/echo-work/bundles/` (3 tarballs de challenge-history, sin handoffs), `/srv/echo-work/build-artifacts/`, `~/aranea/work/forge-030-e2e-20261018/` (sin artefactos de seal a profundidad 4), worktrees symphony (sólo source de workflows). Limitación: los artefactos del E2E forge-0.3.2 (FlowRun 561267ed) vivieron en el runtime de ejecución de Forge, no en las ubicaciones canónicas locales accesibles. Gate afectado: G11 (permanece PENDING_AUTHENTIC_FORGE_ARTIFACT). No se fabricaron artefactos ni se lanzaron campañas. Los fixtures sintéticos cubren contrato, no G11.

## Verificación de las suites (una pasada, PG 54349)

postgres: TestLabV4 7/7; TestShot3Functional 23/23; TestShot3MigrationsWithData 4/4; TestLabWorker* (incl. LeaseRecovery); TestLabSelectionFlowsI1; TestLabCatalogAndStaleness; TestLabPortfolioCreateAndCompose; capacidad — `ok`. lab/*: todo `ok` (analyze 88.1%, opfacts 52.3%). futures: gerardmm/operation/domain `ok`. gateway/internal: `ok` (go.work del repo). futures-projector: productpath `ok`. backtester: observer demo `ok`. Front: `vite build` OK. go vet limpio. PREEXISTING: TestTGFilterSharedTypedLiveBacktestFactoryParity (idéntico en base; ambiental).

## Notas de trust boundary (hallazgos INFO del revisor)

- El read model `strategy_histories.head_revision/head_digest` es mutable por SQL directo de un DBA (el guard protege identidad y DELETE): coherente con el contrato — el head es read model que el servicio mueve; un head alterado hace fallar-cerrado los PUT (precondición) y el CAS del worker; la cadena autoritaria (revisions/ops/movements/receipts) resistió 15/15 sondas hostiles.
- `strategy_ingestion_receipts` acepta INSERT directo (guards UPDATE/DELETE only): consecuencia downstream fail-closed (digest distinto ⇒ conflicto de negocio, jamás éxito silencioso). Misma trust boundary.
- Reproducibilidad de N tras N+1: aserción explícita `TestLabWorkerNReproducibleAfterNPlusOne`.

## Adaptaciones de repros documentadas

A09/A18 sellaban terminalidad por UPDATE SQL directo (contrato freeze §4 original). El mandato adjudicó revisiones inmutables N→N+1: los setups usan la ruta del servicio y los ORÁCULOS se conservaron (A09 identidad bajo referencia sintética lab.curves; A18 +114 exacto por PUT N+1). Sin aserciones debilitadas.

## SHARED_ENVIRONMENTS

Sin cambios. PG descartable propio (54349) detenido al cierre; sin PROD, trading, campañas, migraciones en compartidas, merges, deploys ni aplicado de metadata Hasura.

## RESIDUALS

1. G11: artefacto auténtico Forge (registro EXTERNAL_INTEGRATION arriba).
2. S3-E02: seguridad dinámica NOT_RUN (restricción del harness).
3. Metadata Hasura: aplicar requiere ownership (SOURCE_READY_NOT_DEPLOYED).
4. Cutover/071 y retiros: BLOCKED_EXTERNAL_PERMISSION.
5. Coverage gate 95%: NO_MET con números medidos (88.1%/52.3%; ventanas window_local y ramas de error listadas para completar).
6. Backlog analítico concurrente y RSS bajo carga: NOT_DEMONSTRATED (worker secuencial I1).
7. Motor efectivo: GLM-5.3-Flash (host); discrepancia con GPT-6-Luna registrada, sin atribuir trabajo a otro perfil.

## Revisión independiente ACOTADA del delta PM (2eccb317→8a7381fd)

**PM_RETURN_WITH_FINDINGS** — revisor en contexto fresco: P1 selección VERIFICADO (SELECT propio: selection_revision=2 monotónica, sin duplicación); P2 wiring VERIFICADO (código de producto con ganchos reales fail-visible, opt-in sin cambios previos); P3 grano dual VERIFICADO (sin doble conteo, oráculos intactos); P4 evidencia REPRODUCIDA (cómputo 132k 409s, coverage exacto 88.1%/52.3%); P5 regresiones VERIFICADAS (TestLabV4 7/7); P6 handoff COHERENTE (estados no colapsados, NO_DEMONSTRATED explícitos). Hallazgos F1 (slots sintéticos), F2 (log incompleto), F3 (operation_count=0) RESUELTOS en `ed458c5e`.

## NEXT

## Fuentes

[[SHOT4_EXECUTION_PACKAGE]], [[SHOT3_ADVERSARIAL_REPORT]], [[SHOT3_COVERAGE_MATRIX]], [[0 — Submanager State]], `xKoRx/echo@feature/lab-v4-shot4` (61ac1f72..ed458c5e), paquete de repros `outputs/SHOT3_AUDIT_EVIDENCE/`.

## CONTINUACIÓN DEL SHOT 4 — corrección final, verificación y canario (2026-10-21/22)

Mandato del Owner: secuencia continua (cerrar pendientes → SHA final → release reproducible → canary PROD acotado). Ejecutor: implementador LOCAL (GLM-5.3-Flash, host-declarado). Corte de entrada verificado `ed458c5e` (worktree `~/aranea/work/lab-v4-shot4-20261021/echo`, rama `feature/lab-v4-shot4`, árbol limpio).

### Commits de la continuación (ed458c5e → SHA final)
| Commit | Contenido |
|---|---|
| `3939dcb8` | §1.1/§1.2/§1.3/§1.4 — analyze.WindowMetrics + WindowMetricsFromSeries (window_local vs máximo arrastrado, T43 con oráculos 70≠150) + ComparePrePost (cohorte por apertura, corte as_of, delta abs/relativo con UNDEFINED en denominador cero); comparación de copias separada en DigestEquivalence (A) vs CopyFidelity INSUFFICIENT_LINK_EVIDENCE (B, T45) + discontinuidad MM (T44); declaraciones de coste CostTransport NONE_V1/FULL_DECLARED_V1 selladas en coverage + LabCostStatus KNOWN_NONZERO/KNOWN_ZERO/UNKNOWN + comisión tardía N+1 sin mutar N + sin doble descuento; wiring real del binario backtester (LAB_FACTS_* fail-fast) + ruta gateway /analysis + panel de ventana en el front |
| `1f8e8756` | Demo de UI en ejecución expuso 3 defectos reales de wiring: read models serializaban PascalCase (front esperaba snake_case — el recorrido UI jamás se había corrido); binario lab-worker-v4 no despachaba PORTFOLIO_SNAPSHOT (agotaba 5 intentos con perfil ""); cola reclamaba portfolios antes que curvas (INSUFFICIENT_DATA prematuro). Corregidos + labv4-boundary (boundary mínimo reutilizando el handler V2; SPA fallback; bearer siempre) |
| `27525f2b` | Gate de coverage cerrado: 96,1% statements en analyze+opfacts (`DATABASE_URL=<PG descartable> LABV4_MIGRATION_TEST=1 go test ./lab/analyze/ ./lab/opfacts/ -coverpkg=./lab/analyze,./lab/opfacts`); tests de publisher con sink stub, fail-closed de montos/monedas mezcladas, ValidatePortfolio D11; borrado código muerto (shortDigest64, rama inalcanzable de json.Marshal) |
| `1c7d929a` | Fixes del revisor independiente (2 MINOR): trim numérico lossy en helper de test; cohorte pre/post falla cerrada con opened_at ausente (jamás membresía PRE implícita) |
| `bfd03a19` | Carga (§2.2) contra binarios REALES: 16 POST concurrentes ×500 ops (8.000 ops) 201 en 14,9s; ráfaga PUT N+1 (rev→3) 200 en 4,0s; coalescing demostrado (sólo rev3 calculada; 32 jobs rev1 → STALE); worker único drena 32 jobs en 10s; kill -9 a mitad de drenaje → relevo recupera por lease sin duplicar publicación; RSS muestreado 0,5s: boundary max 22MB, worker max 15MB. Fix: boundary registraba patrones sin wildcards (PathValue vacío → todo PUT 400). Evidencia: `~/aranea/work/lab-v4-shot4-20261021/LOAD_AND_MEMORY_EVIDENCE.md` |

### Demo de producto en UI ejecutándose (§1.1 — vite build NO sustituye)
PG descartable 54349 (DB demo) + binario labv4-boundary (127.0.0.1:8099, bearer) + worker real + front build. Recorrido verificado en navegador: catálogo (3 historias × 4 perfiles READY, D16 visible) → detalle → selección principal/alternativas (hist-A principal; comparación A/B por alternativa) → **análisis de ventana: DD local 6 ≠ DD arrastrado 116, net_change −6, badge costes KNOWN_NONZERO, pre/post por construction_at (pre neto 120/DD 80 vs post −36/DD 70, Δ −156, relativo −13/10)** → portfolio 60/40 READY final 9714,72 (allocations 6.000/4.000). Captura: `~/aranea/work/lab-v4-shot4-20261021/evidence-labv4-ui-window.png`. Oráculos de cohortes verificados con oracle Go independiente (curva money acumulativa desde 0).

### G11 — de "no sé dónde está" a recurso exacto identificado
FlowRun 561267ed (E2E forge-0.3.2, watcher log `final-release-e2e-20261019/watcher/watcher-w11.log:125,128`) = Temporal `sqx-main-v1-67dd5b4e-…` (fuera de visibilidad del cluster DEV compartido). **Artefactos auténticos VIVOS en MinIO `s3://sqx-strategies/wave_11/ndx/l_h1/flow_example_2/v1/`** (00_configs, 01_builder .sqx, 03…09 con final-*.sqx del reretester; timestamps 2026-10-19). Faltante exacto para G11: las TRADE LISTS del final reretester y el sealed promotion handoff — `10_tradelist/`, `13_mt5_backtest/` y `08_applied/` están VACÍOS en MinIO (esos outputs vivieron en el runtime MT5, host Kronos) y el workflow ya no es consultable. G11 sigue **BLOCKED_EXTERNAL_ARTIFACT** con el recurso y acceso faltante nombrados: trade lists del reretester en el host MT5 + registro de promoción (sha:b325fd29) del runtime Forge.

### Canary PROD (§4/§5) — SOURCE_VERIFIED_CANARY_BLOCKED
Paquete completo listo en `~/aranea/work/lab-v4-shot4-20261021/canary-pkg/` (README con receta, rollback y criterios de parada). Fuente auténtica verificada: `challenge-history-r4-identity-and-evidence.tar.gz` → ORB-CH300-30M (80.439 eventos; **digest del archivo = event_digest del receipt**, provenance OK). Gate 6 del canary FALLA: la sesión MCP `aranea-ssh` expiró ("Session not found or expired", reintentos fallidos; perfiles no alcanzables) ⇒ sin inventario/ownership/acceso demostrable al destino PROD no se despliega (mandato: sin bypass; escalar permiso). Siguiente paso mecánico cuando el acceso vuelva: inventario del host → DB lógica nueva (echo_labv4_canary) → boundary+worker en loopback → smoke con la historia del bundle → rollback = stop procesos + drop de SU DB.

### SHARED_ENVIRONMENTS
Sin cambios en compartidos: PG descartable propio (54349) + DBs efímeras propias (demo/load/bt en ese clúster); sin PROD, trading, Kafka, metadata Hasura, merges a master de producto, ni reinicios de productores. Procesos locales al cierre: demo UI (8099, loopback+bearer) y PG 54349 dejados corriendo como checkpoint visible; carga detenida.

### FINAL_SHA_REVIEW — COMPLETE (revisor en contexto fresco, 2026-10-22)
Dictamen **READY_FOR_MANAGER** sobre `bfd03a19` (delta ed458c5e..bfd03a19, 4 commits). Evidencia propia del revisor: suite lab green (210s), coverage 96,1% reproducido exacto, T43 validado como dos significados distintos (70 ≠ 150 por máximo inicial), sin identidad sintética en el delta, invariantes económicos demostrados con asserts, sin tests sin aserciones ni exclusiones. 5 hallazgos NO bloqueantes: 2 MINOR corregidos en `1c7d929a` (SHA FINAL del candidato) (trim lossy; opened_at ausente ahora falla cerrado — jamás membresía PRE implícita) + 3 NOTE registradas (CurveCurrent siempre true en el endpoint de análisis; charset hex no validado en slots LAB_FACTS; errores de BD mapeados a 400 en el handler de análisis).
2. G11: BLOCKED_EXTERNAL_ARTIFACT (recurso exacto arriba).
3. Canary: SOURCE_VERIFIED_CANARY_BLOCKED (gate 6 acceso; paquete listo).
4. Seguridad dinámica (S3-E02): sigue NOT_RUN (restricción del harness, sin reintentos).
5. 1.4: pata positiva del binario backtester→PG demostrada a nivel biblioteca + fail-fast real del binario; el e2e nativo completo no produce operaciones (fixture market-data-only) — registrado honesto.
