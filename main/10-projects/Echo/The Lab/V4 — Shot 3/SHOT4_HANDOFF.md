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

### CONTINUACIÓN 2 — CORRECCIÓN DE EXPERIENCIA (2026-10-22, en curso)

El Owner RECHAZÓ la experiencia visible del LAB V4 (recorrido de portfolios/snapshot/jobs; consola de infraestructura, no producto). Estados registrados en el planificador:

| Estado | Valor |
|---|---|
| UX | **USER_UX_REJECTED** — la primera entrega debe funcionar como el Strategy Lab de V3: screener de todas las estrategias → selección → dashboard con historia y operaciones |
| ALCANCE | **STRATEGY_SCREENER_AND_DETAIL_REQUIRED** — entrada LAB = screener; listado con métricas/filtros/orden/paginación server-side; selector de curva real (4 perfiles V4); detalle con curva, DD, historia, principal/alternativas, operaciones |
| CANARY | **CANARY_PAUSED_FOR_UX_CORRECTION** — sin despliegues mientras se corrige la experiencia; la demo 8099 existente NO se borra |
| ACCESO MCP | resuelto durante esta continuación: catálogo aranea-ssh restaurado (sonda read-only `sqx-zeus` respondió `sqx-ulab-zeus-0`); el bloqueo previo del gate 6 (sesión expirada) ya no aplica cuando el canary se reanude |

Resultado al cierre: UX_IMPLEMENTATION=READY_FOR_OWNER_REVIEW|PARTIAL|BLOCKED, OWNER_UX_ACCEPTANCE=PENDING, evidencia A–J y SHA en la subsección final de esta continuación.

#### Resultado de la corrección — UX_IMPLEMENTATION: READY_FOR_OWNER_REVIEW (2026-10-22)

| Estado | Valor |
|---|---|
| UX_IMPLEMENTATION | **READY_FOR_OWNER_REVIEW** — recorrido screener→dashboard funcionando en la demo, verificado en navegador (A–J) |
| BACKEND_REGRESSIONS | **NINGUNA OBSERVADA** — suite completa `TestLab*` verde (1146s, PG descartable); nuevo `TestLabStrategyScreener` PASS |
| OWNER_UX_ACCEPTANCE | **PENDING** — el Owner no revisó aún esta UI |
| CANARY | **PAUSED_FOR_UX_REVIEW** — sin despliegues; el paquete canary queda intacto |

**SHA exacto:** `feature/lab-v4-shot4 @ 86af0a68` (sobre `93d776f0`; 1 commit, 15 archivos, +2564/−64). Binarios reconstruidos desde ese SHA; `vite build` con `VITE_GATEWAY_ENDPOINT=http://127.0.0.1:8099 VITE_SESSION_TOKEN=demo-token-labv4` (sin popups de token).

**Entrada y detalle (rutas exactas):** entrada `/lab` (tab único `strategyLab`, título "Strategy Lab — catálogo, curvas y detalle de estrategias"); contenedor `front/src/components/lab/v4/StrategyLabV4Tab.vue` (estado del recorrido en query: `?tab=strategyLab&strategy=&profile=&q=&sym=&mode=&sort=&dir=&page=&writer=`); tabla `StrategyScreenerV4Table.vue`; dashboard `StrategyDashboardV4.vue`; catálogo de perfiles `labV4Profiles.js`. Registro de tabs en `lens/lensRegistry.js` (sólo Strategy Lab; la consola labV4, Strategy Lab Clean V3, Curve V3, Account Lab y Portfolios quedan FUERA de la entrada — componentes y backends se conservan sin dos implementaciones activas; query/localStorage heredados normalizan al recorrido nuevo).

**Catálogo completo (backend):** nuevo read model `ListLabStrategyScreener` (`v3/sdk/postgres/lab_screener.go`) — una fila por ESTRATEGIA (canonical_strategy_id), generación canónica resuelta con reglas explícitas: SELECTION (principal de la selección vigente 069) / SINGLE (única historia activa) / UNRESOLVED (N candidatas sin selección ⇒ fila visible SIN métricas, jamás elección silenciosa) / NO_HISTORY. Métricas SOLO publicadas (lab.curves + lab.metric_results) del perfil pedido; STALE cuando la curva no es del head. Filtro/orden/paginación server-side sobre el conjunto consultable (el front nunca descarga el conjunto). Rutas nuevas: `GET /api/v2/lab/screener` y `GET /api/v2/lab/strategies/{ref}/histories/{hid}/operations/{op}/movements` (gateway server.go + boundary). Detalle enriquecido: métricas por perfil, cadena de revisiones, período observado, instrumentos.

**Perfiles reales disponibles (selector de curva):** r_net_cumulative.v1 (R acumulado; exige Q_i CYCLE_BUDGET), recorded_money.v1 (PnL registrado; no es saldo de cuenta), normalized_10k_open_balance.v1 y normalized_10k_initial_balance.v1 (capital 10k, r=1%, causal/con reinversión y presupuesto fijo; CAPITAL_EXHAUSTED visible). Unidad y condiciones visibles por perfil. No disponibles en V4 con motivo declarado en la UI: TF (la identidad de versión no lo transporta), SQN/recovery (no calculados; el front no recalcula), expectancy en perfiles no-R (INSUFFICIENT).

**Evidencia del recorrido A–J (UI real conectada al boundary+PG de la demo):** capturas en `~/aranea/work/lab-v4-shot4-20261021/evidence-ux/` — 01 screener sesión limpia (A; 11 estrategias, badges de resolución, estados honestos), 02 cambio de curva R→money (E; scalp-cl pasa INSUFFICIENT_DATA→READY USD 100: no cosmético), 03 filtro símbolo CL server-side (F; 2 filas), 04 dashboard orb-nq-15m (G; identidad, tiles con unidad por métrica, curva exacta, distribución, DD), 05 operaciones con movimientos de orb-3 (I; 2 parciales + comisión ⇒ 216 ≠ ticket simple), 06 STALE tras PUT N+1 (J; curva rev1 etiquetada STALE con ops del head), 07 detalle rev2 tras drenar worker (J; READY coherente 4,5 R, N1 SUPERSEDED, PF UNDEFINED honesto). B verificado (query `tab=labV4` y localStorage `portfolios` caen en el screener); H verificado (volver conserva perfil+símbolo+filas; deep-link directo al dashboard funciona).

**URL interna de la demo corregida:** `http://127.0.0.1:8099/lab?writer=worker-writer` (loopback, bearer `demo-token-labv4` por build config; sin writer el detalle usa forge-live por convención heredada). Boundary 8099 + PG descartable 54349 DB `echo_labv4_demo2` (seed `TestLabV4DemoSeedScreenerForUI`, 10 estrategias + selección + portfolio 60/40; worker real `lab-worker-v4` drenó las colas). La demo anterior (`echo_labv4_demo`) NO se borró. Nota operativa: el change event del filtro de símbolo también dispara con Enter (el fill sintético de Playwright no genera change nativo; wiring verificado por dispatch).

**Límites reales:** sin despliegue a PROD ni merge (canary pausado); TF no declarado en el modelo V4; SQN/recovery/data-quality-score no existen en V4 y se muestran como "—" con motivo; la ordenación server-side carga el conjunto de estrategias×perfil del namespace (volumen de catálogo, no de historias; latencia no medida bajo carga); Account Lab/Portfolios sin acceso desde la entrada (capacidad conservada en código/APIs); seguridad dinámica S3-E02 sigue NOT_RUN.

## CONTINUACIÓN 3 — AJUSTES PUNTUALES SOBRE EL RECORRIDO ENTREGADO (2026-10-22)

Mandato del Owner: ajustes puntuales (identidad al navegar desde el catálogo, coherencia de revisión en el dashboard, clasificación de métricas/metadata), sin reconstruir la pantalla, sin nuevos shots, conservando la demo. Ejecutor: implementador LOCAL (GLM-5.3-Flash, host-declarado). Corte de entrada verificado `feature/lab-v4-shot4 @ 86af0a68` (base `93d776f0`, worktree `~/aranea/work/lab-v4-shot4-20261021/echo`, árbol limpio). **SHA final: `95df47b2` (1 commit principal — amend incluye el oráculo de recovery); sobre 86af0a68.**

| Estado | Valor |
|---|---|
| UX_IMPLEMENTATION | **READY_FOR_OWNER_REVIEW** (ajustes verificados en navegador; misma experiencia visual salvo los ajustes pedidos) |
| OWNER_UX_ACCEPTANCE | **PENDING** — el Owner no revisó aún |
| CANARY | **PAUSED_FOR_UX_REVIEW** — sin despliegues; paquete canary intacto; NINGÚN bundle de demo se promueve (config/credenciales de demo, fixtures, no es el catálogo real del Owner ni G11) |
| MCP_TOOLING_RESTORED | **SÍ** (catálogo aranea-ssh accesible; registrado de la continuación 2) — esta sesión NO lo usó: todo el trabajo fue local |
| PROD_TARGET_ACCESS_NOT_YET_VERIFIED | **VIGENTE** — una sonda exitosa a Zeus NO valida echo-runtime-prod; no se investigó el destino PROD (fuera de alcance del mandato) |

### §1 Identidad correcta al navegar desde el catálogo

- **Fallback `forge-live` eliminado** del recorrido (`StrategyLabV4Tab.vue` / `labV4.js`): no hay writer global en la URL ni productor por defecto. La FILA transporta la identidad resuelta (`registry_namespace`, `strategy_version_ref`, `producer_writer`, `history_id`, head, selección) y el dashboard la usa tal cual; el backend sigue resolviendo namespace del CONTEXTO AUTENTICADO (config+bearer), nunca del query parameter.
- **Selección no resuelta**: la fila UNRESOLVED/NO_HISTORY abre un estado visible con las historias CANDIDATAS y su identidad completa (nuevo read model `ListLabStrategyCandidates` + ruta `GET /api/v2/lab/strategies/{id}/candidates`); cada candidata ofrece "elegir principal" (decisión explícita, jamás primera historia ni productor por defecto). Defecto de esquema real descubierto por este flujo: `mm_context_digest` NOT NULL+CHECK impedía seleccionar estrategias SIN contexto MM (503 silencioso) → **migración 073** (mm nullable + `UNIQUE NULLS NOT DISTINCT`) y normalización ""→NULL en `SelectPrimaryHistory`/`GetHistorySelection` (`IS NOT DISTINCT FROM`).
- **Prueba funcional (demo, navegador real, sin writer en URL):** `orb-nq-15m` (productor `worker-writer`) y `mr-dax-5m` (productor `backtest-observer-writer`, segundo productor agregado al seed) abren ambas con identidad/métricas/operaciones propias; deep-link `?strategy=mr-dax-5m` recargado OK; volver conserva filtros/curva/página (`?q=mr` + 2 filas verificados); elegir candidata del segundo productor en trend-eurusd-h1 pasa la fila a SELECTION con la métrica de la elegida. Capturas `~/aranea/work/lab-v4-shot4-20261021/evidence-ux3/01,04,05,06,09`. Sin pruebas dinámicas restringidas (harness respetado).

### §2 Coherencia de revisión en el dashboard (caso J)

- El detalle se **PINNEA a la revisión PUBLICADA del perfil pedido** (`GET .../histories/{hid}?profile=…`): curva, métricas y operaciones de la MISMA generación; `head_revision` y `displayed_revision` viajan separados. Mientras N+1 está aceptado sin publicar: banner "Actualización pendiente… N publicada / head N+1 en cálculo; no se mezclan generaciones", tabla "Operaciones (revisión N)" y movimientos pedidos con `?revision=N` (la revisión de la operación inspeccionada, no el head del momento). Al publicar N+1: curva, métricas y operaciones cambian COHERENTES (sin banner, revisión nueva).
- El SCREENER también alinea el conteo de operaciones a la generación mostrada (jamás un head N+1 pendiente presentado como explicación del resultado N). Defecto adicional corregido: el read model de perfiles por historia dejaba ganar una fila arbitraria entre revisiones (con rev1+rev2 publicadas podía mostrar la generación vieja como vigente) — ahora la revisión MAYOR publicada gana el mapa.
- **Prueba (demo):** rev N publicada → PUT N+1 con cambio económico visible (orb-7) SIN drenar → dashboard muestra N pinneada con banner y desglose expandido coherente (captures `02,03,07`) → drenar worker → recarga del mismo enlace muestra N+1 completo sin banner (`10`). Sin modificar revisiones aceptadas ni algoritmos económicos.

### §3 Métricas y metadata — clasificación de faltantes

- **Estados**: a los B.6.5 (DEFINED/NO_OBSERVATIONS/INSUFFICIENT_DATA/UNDEFINED) se agregan **NOT_IMPLEMENTED** y **NOT_APPLICABLE** (**migración 072**, CHECK extendido). INSUFFICIENT_DATA ya no sustituye "no implementado" ni "no aplicable"; ningún faltante se muestra como cero.
- **EXPECTANCY**: `expectancy` en la UNIDAD DEL PERFIL (R en r_net_cumulative; moneda en los demás), sobre deltas causales por operación (`OpDelta` construido por cada compute) dividido por cerradas EVALUABLES con base declarada — los parciales de una abierta jamás suman como terminales y el R jamás se re-etiqueta a dinero. (Legacy `expectancy_r` sigue en las curvas viejas; el sort del screener usa `expectancy` con fallback.)
- **RECUPERACIÓN** (B.6.5 riesgo realizado): `recovery_factor` = neto del perfil / drawdown máximo ABSOLUTO en la misma unidad (R usa DD en R, sin dividir por base cero); DD cero ⇒ UNDEFINED con motivo; cola tras agotamiento ⇒ INSUFFICIENT_DATA del prefijo.
- **PROFIT FACTOR**: sobre la contribución del perfil (PF en R para perfil R, en moneda para money); monedas mezcladas (o declaradas junto a montos sin moneda) ⇒ **NOT_APPLICABLE** fail-closed (los loaders transportan ahora la moneda de movimientos/neto).
- **SQN**: publicado como **NOT_IMPLEMENTED** con motivo (la definición aplicable al perfil no está aprobada; la fórmula legacy no se copió; sin ampliación del catálogo).
- **TIMEFRAME**: transportado verbatim desde la definición canónica del productor (`echo.strategy_definitions.timeframe` vía join por canonical_strategy_id) en fila del screener y detalle; NULL/sin fila ⇒ "no declarado". **Jamás inferido** del nombre ni de la frecuencia observada. Demo con 3 casos: declarado (15m/5m/H1), fila sin TF, sin fila.
- Prueba backend: `metrics_classification_test.go` (5 casos: unidad por perfil, no-re-etiquetado R→USD, monedas mezcladas NOT_APPLICABLE, cola tras agotamiento INSUFFICIENT, denominadores cero UNDEFINED/NO_OBSERVATIONS) + oráculos extendidos en `lab_screener_test.go`/`lab_readmodels_test.go` (pinneo de revisión, candidatos, TF, clasificación).

### Verificación

- Suites: `go test ./v3/sdk/lab/analyze/` ok (incluye clasificación nueva); `./v3/sdk/postgres -run TestLab` **completa ok (1439s, PG descartable 54329 DB efímera propia)** + re-ejecución dirigida del subconjunto afectado por el fix final de generación (catálogo/staleness/N-reproducible/selección/screener). go vet limpio; `vite build` OK. PREEXISTING ambiental intacto (sin tocar).
- Front: identidad por fila, banner STALE, tiles por unidad (expectancy/recuperación/SQN), TF transportado, candidatos con elección prevista — capturas `evidence-ux3/01..10`.
- Demo viva: **`http://127.0.0.1:8099/lab`** (SIN `?writer=`); boundary `bin-ux3/labv4-boundary` @ 95df47b2 (código de producto; los binarios se construyeron del árbol final, el amend solo tocó un test); PG descartable 54349 DB **`echo_labv4_demo3`** (re-creada con 072/073; seed con 2 productores y TF declarado/no declarado; worker real `bin-ux3/lab-worker-v4` drenó las colas). **La demo usa FIXTURES**: no es el catálogo real del Owner ni G11. DBs demo previas (`echo_labv4_demo`, `echo_labv4_demo2`) intactas. Fuente/build/base exactos: `xKoRx/echo@feature/lab-v4-shot4` @ `95df47b2`, base `86af0a68` (corte entregado), base reportada `93d776f0`; front build con `VITE_GATEWAY_ENDPOINT=http://127.0.0.1:8099` y token de demo por build config (sin popups; sin tokens en este documento ni en capturas).

### SHARED_ENVIRONMENTS / límites

Sin cambios en compartidos: PG descartables propios (54329 tests DB efímera, 54349 demo3 propia) + artifacts propios; sin PROD, trading, Kafka, metadata Hasura, merges, deploys ni reinicios de productores. Sin investigación del destino PROD. Residual: cobertura del delta cubierta por pruebas dirigidas (identidad/revisiones/métricas/navegación); la suite larga completa se ejecutó UNA vez con el código previo al guard final y el subconjunto afectado se re-ejecutó con el final.



## CONTINUACIÓN 4 — REAL_ECHO_DATA_INTEGRATION (2026-10-22, en curso → entregada)

Mandato del Owner: datos REALES de Echo en LAB (frentes A/B/C independientes; un bloqueo en B/C no detiene A). Ejecutor: implementador LOCAL (GLM-5.3-Flash, host-declarado). Corte de entrada `95df47b2` (worktree `~/aranea/work/lab-v4-shot4-20261021/echo`, árbol limpio). **SHA final de producto: `10a4eddd`** (4 commits: `a4280fb2` adapter journal→V4 + loader; `52a4fad2` fix clave idempotencia opfacts; `dc6afaef` fix acumulación de operaciones; `10a4eddd` test productpath preexistente). Rama pusheada a origin.

| Estado | Valor |
|---|---|
| REAL_ECHO_DATA_INTEGRATION | **IN_PROGRESS → FRENTE_A_ENTREGADO** (universo completo visible y conciliado; B demostrado con 2 defectos corregidos; C verificado con bloqueo exacto) |
| REAL_DATA_READY | **NO declarado por disponer de fixtures** — la pantalla principal consume la BD real procesada (echo_labv4_real) |
| OWNER_UX_ACCEPTANCE | PENDING (recorrido real verificado en navegador por este agente; el Owner no revisó aún) |
| CANARY | PAUSED (sin despliegues; paquete intacto) |
| PROD_TARGET_ACCESS | Verificado SOLO LECTURA (MCP `aranea-postgres-ro` = `192.168.31.220/echo`, confirmado contra ETCD `/echo/production/postgres/{host,database}`; transacción REPEATABLE READ READ ONLY en el loader; 0 escrituras en origen) |

### ECHO_REAL_CATALOG (corte del snapshot del loader 2026-10-22T15:46Z; manifiesto en real-artifacts/load-manifest-*.json)

Fuente: `echo.trade_journal` + `echo.strategy_definitions` (PROD `192.168.31.220/echo`, RO). Journal 4.485 filas: REFERENCE 3.579 CLOSED + 1 OPEN; EXECUTION 836 (ECHO) + FAILED 69; NATIVE (EXECUTION) incluido en EXECUTION; cuarentena 1.168 envelopes rechazados por el propio Echo. **136 estrategias con actividad REFERENCE, cada una con exactamente 1 cuenta** (una historia por estrategia ⇒ resolución SINGLE, sin selecciones necesarias); 136/136 con definición canónica y TIMEFRAME declarado (transportado verbatim, jamás inferido). Exclusiones explícitas: EXECUTION/copias (D1-M02: fuera del REAL, sirven después a fidelidad), FAILED (rechazos de orden, con conteo por estrategia), definitions sin actividad REFERENCE. `strategy_versions`/`identity_mappings` en PROD: vacías ⇒ identidad versionada vía receta **definition-v1 (ANALYTIC)** sobre el contenido canónico de `strategy_definitions` (sin timestamps; ejecutable del runtime NO acreditable desde esta vía — límite registrado, jamás hashes inventados).

### ECHO_REAL_HISTORY

3.580 operaciones fuente → 3.580 aceptadas (0 rechazadas): 3.579 CLOSED→CLOSED_SUMMARY (neta+moneda obligatorias; gross/comisión/swap transportados como costes declarados KNOWN_NONZERO) + 1 OPEN→ECONOMIC_MOVEMENTS status OPEN sin movements. FAILED excluidas con conteo. Q_i: `risk_money` = sello MM de Echo AL ABRIR (mm_engine `sealOpenRiskOnCommand`, |precio−SL|×lote pre-offset; la fila del journal es la evidencia de origen) ⇒ **CYCLE_BUDGET** con `risk_evidence_ref=echo.trade_journal/<uuid>#initial_risk_money`; 92 filas sin sello viajan SIN Q_i ⇒ degradan R/10k a INSUFFICIENT_DATA con la operación nombrada (122 estrategias READY×3 perfiles + 136/136 money READY; 14 INSUFFICIENT honestos). Actualización (A5): re-corrida completa con claves de contenido ⇒ **136 UNCHANGED sin revisión nueva** demostrado; durante la sesión se observó N+1 REAL en vivo (cierres de magia_2509/2510 entre cortes ⇒ ACCEPTED). Defecto corregido en el adapter: CoverageJSON contenía el timestamp de corrida ⇒ N+1 espuria por corrida (estable por contenido; el corte vive en el manifiesto).

### USER_UI

URL interna comprobada: **`http://127.0.0.1:8100/lab`** (boundary `bin-real/labv4-boundary` @ 10a4eddd, loopback, bearer por env 600; namespace `echo-prod`; front build `dist-real` con `VITE_SESSION_TOKEN` de build config — sin popups). Origen REAL identificado por fila (ns echo-prod · productor echo-journal-loader · historia reference-<cuenta> · rev N · LIVE); **fixtures visibles: 0** (sistema de demo 8099/echo_labv4_demo3 intacto y separado). Evidencia de navegador: `evidence-real/01-dashboard-real-r-magic_251002017.png` (magic_251002017 GDAXI H1 84 ops: −11,0287 R, expectancy −0,1313 R, PF 0,5861, win 36,9%, DD 13,4274 R, READY), `02-screener-real-136.png` (catálogo 136, TF transportado), `03-dashboard-backtest-motor-real.png`. **Conciliación exacta verificada**: Σ profit_net fuente de magic_251002017 = −24.355,45 = final del perfil money publicado (USD); a nivel operación: trade_id ↔ source_operation_id con montos y evidencia por uuid.

### NEW_RUNTIME_COMPATIBILITY

Corte vigente del motor: **`origin/feature/ef-runtime-pools` @ `960bf60a`** (44 commits / +55.104 líneas sobre la base común `d74b6525`; NO integrado a LAB — sus hooks LAB **no existen** en esa rama: opfacts vive sólo en `feature/lab-v4-shot4`). Dictamen por capacidad del recorrido Operation→Orders→Fills→realizaciones→observer→servicio→worker→UI, demostrado con **ejecución REAL del motor** (binario LAB @ dc6afaef, runspec auténtico sellado de la campaña 873 `basic-NQZ5-01` re-declarado al binario ejecutante, corpus NQZ5/NQH6 local con digests verificados, LAB_FACTS_* con slots REALES): **SUPPORTED_VERIFIED** para multi-fill/multi-orden por operación (166 fills del motor ⇒ 38 operaciones con fills reconocidos, parciales preservados como REALIZED_PNL por fill), Q_i sellado por el MM del motor (CYCLE_BUDGET con decision ref), grano dual, live/backtest sin colisión (BACKTEST convive con LIVE en el mismo namespace, jamás cambia StrategyVersion), conciliación exacta gross (realized_gross motor −25.295 = final money LAB −25.295). **SUPPORTED_WITH_SOURCE_LIMITATIONS**: costes del run (charged_costs 4.452,12) NO transportados — `cost_transport NONE_V1` declarado (jamás cero falso); revisiones por publish (197 revisiones, retención; coalescing worker ok). **BLOCKED (integración, no capacidad)**: el emisor VIGENTE (960bf60a) no puede publicar a LAB hasta integrar los hooks — decisión de producto owner-gated (no se integró la rama). Defectos reales corregidos en el adapter opfacts (con regresiones): clave de idempotencia sin contenido/head ⇒ conflicto falso en re-publicación; PUT sin set acumulado ⇒ historia reducida a la última operación. Preexistente corregido: productpath test desalineado con la firma de `GetLabHistoryDetail` desde la continuación UX.

### FORGE_ENDPOINT

Rutas V2 efectivamente montadas en el SHA (gateway `server.go:206-219` + boundary): POST `/api/v2/strategy-ingestions`, GET by-key, PUT/GET `/api/v2/strategy-versions/{ref}/histories/{hid}`, análisis de ventana, lab/catalog, lab/screener, movements, selections, portfolios, candidates, curves points. **HTTP_LOCAL_VERIFIED (2026-10-22, @ 10a4eddd)**: POST→201 receipt ACCEPTED; replay mismo key+body→200 mismo receipt; GET by-key→receipt; sin token→401; sin `X-Producer-Writer`→400 (contrato: bearer + writer declarado + `X-Idempotency-Key` sha256:64hex + `contract_version strategy-ingestion.v2`); lectura real en 8100 con coverage/provenance. Contrato de autenticación: Bearer (LAB_BOUNDARY_TOKEN / tokens gateway en ETCD; jamás en informe). **REACHABLE_FROM_FORGE: NO demostrado** — el boundary es loopback por diseño y el gateway DEV desplegado en `.161:8090` (release `2af4b21f`) NO incluye rutas V2; habilitación exacta: deploy del gateway desde `feature/lab-v4-shot4` (owner-gated) o exponer el boundary en LAN. **AUTHENTIC_END_TO_END_VERIFIED: NO** — G11 sigue **BLOCKED_EXTERNAL_ARTIFACT** (trade lists del reretester en el host MT5 Kronos + registro de promoción sha:b325fd29; artefactos MinIO 10_tradelist/13_mt5_backtest/08_applied vacíos). Prueba de protocolo hecha con fixture en el namespace de demo (`lab-worker-it`, fila `forge-protocol-probe` en echo_labv4_demo3), nunca en echo-prod.

### OPEN_BLOCKERS

1. G11 auténtico: requiere trade lists del reretester (host MT5) + registro de promoción Forge (recurso nombrado arriba). 2. Reachability Forge→V2: requiere deploy gateway owner-gated (o decisión de exposición LAN del boundary). 3. Integración hooks LAB en `ef-runtime-pools` (para que el motor VIGENTE publique a LAB): decisión de producto/owner, no ejecutada. 4. Canary PROD: PAUSED (paquete listo en canary-pkg/; acceso SSH MCP resuelto). 5. S3-E02 sigue NOT_RUN (restricción harness). 6. Badge "ECHO: OFFLINE" en el front servido por el boundary: sonda de health del backoffice sin endpoint en el boundary (cosmético, fuera del camino de datos LAB). 7. Deuda menor: revisiones por publish del backtest (retención; worker la drena), y el UNRESOLVED no aplica (cada estrategia con 1 historia).

### ARTIFACTS

Manifests de carga + conciliación: `~/aranea/work/lab-v4-shot4-20261021/real-artifacts/load-manifest-*.json` (por estrategia: ID origen → version_ref → historia → conteos → período → netos por moneda → estado). Logs de runs del motor: `real-artifacts/backtest-run{,2,3}.log` (run1/run2 = repros de los 2 defectos; run3 COMPLETE). Runs sealed: `bt-artifacts-real/bt-d89c4271…/result.json.gz` + `runspec-real.json`. Env de credenciales mode 600: `real-artifacts/env/` (sin secretos en este documento). Evidencia navegador: `evidence-real/01..03*.png`. Producto: `xKoRx/echo@feature/lab-v4-shot4` @ `10a4eddd` (pusheado). Procesos dejados vivos como checkpoint: PG descartable 54349 (DB echo_labv4_real), boundary 8100, worker (drena y queda en loop), demo 8099 intacta.
