---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-07"
updated: "2026-10-07"
---

# BTG-S04 — GOD LOCAL: auditoría adversarial independiente

## Propósito

Determinar por falsificación si el candidato permite validar estrategias y el dominio runtime compartido con cronología, riesgo, fills y contabilidad correctos, y si su rendimiento es utilizable. Auditoría ONE-SHOT independiente; no implementación S05, aceptación de gate ni autorización LIVE.

**STATE = READY_FOR_PRIMARY_REVIEW_WITH_FINDINGS.** El candidato falla invariantes materiales. BASIC y CAMPAIGN existentes son ejecuciones históricas inspeccionadas, no resultados económicos certificados por S04. Las pruebas nuevas, perfiles y comparación acotada real se ejecutaron offline. Los defectos compartidos del dominio también afectan al runtime: igualdad entre caminos no demuestra seguridad.

## Contenido

### 1. Identidad, autoridad y alcance ejecutado

- Producto `xKoRx/echo`, rama correctiva `codex/btg-s03-remediation`, **SHA auditado `1bf45050780554c1135edc619bf01a8a4b04ba08`**. HEAD local y remoto coinciden al inicio y al cierre. Incluye `09702442`, `adfe4087` y el inert-skip final; no se auditó sólo el candidato histórico `c1c0e7d4`.
- Checkout correctivo preservado: tracked diff vacío; únicamente `reports/` sin seguimiento. No merge/rebase/cherry-pick, cambios productivos, órdenes físicas, compras, DB/collector, ETCD, secretos, D6 ni despliegue.
- Carril independiente: clon local separado, detached, en workspace Aranea `work/btg-s04-god-20261007/echo`. **Commit local de siete archivos de tests nuevos: `d5b16049bbee7295063e88d8d8f7fa0a4bbe34fe`**, padre exacto el SHA auditado. No rama/PR documental ni push de producto. Parche portable `evidence/btg-s04-tests.patch`.
- GOD disponible: **`gpt-6-astra`, effort high**, verificado en `turn_context` del host; no sustitución de nivel. Cuota/tokens consumidos UNKNOWN. Tres especialistas ONE-SHOT disjuntos, autorizados por el despacho: runtime, campaña/contexto y rendimiento/fuentes. Auditor raíz: causalidad, skip, venue, integración y juicio independiente.
- Bootstrap fresco Agents-OS; technical-project-manager, contrato de ambientes, instrucciones del repositorio y skill de verificación focalizada. Autoridad: despacho/Owner actual > deltas S03 > S02 aplicable > históricos. ROI supersedido. S2, USD, compra120, exportación Windows y arquitectura comercial no reabiertos.
- Toolchain **Go1.27.1 linux/amd64**. Host disponible al presupuestar:24 CPU lógicos,92GiB RAM total/66GiB disponible,23GiB disco libre. Pruebas funcionales: GOMAXPROCS2, `-p 2`, timeout180s; campaña GOMEMLIMIT8GiB blando. Rendimiento: GOMAXPROCS1/proceso, GOMEMLIMIT2GiB blando, timeout180s, máximo4 procesos y objetivo8GiB/2GiB evidencia. No timeout ni carga de horas. Progreso por resultados/contadores agregados, sin dump por evento para aparentar actividad.

**Build ejecutada S04:** binarios finales de tests, compilados desde el commit de tests y ejecutados con filtros acotados. `go test -c` no inserta aquí `vcs.revision`; identidad fijada por padre producto, hashes de fuentes y binario, sin fingir build productiva limpia:

| Binario | SHA256 |
|---|---|
| `evidence/build/backtester-s04.test` | `76bdea01fb2eb5534881dbda5937dcfc61fc4e3b3b9f89dd450149c0ec42a712` |
| `evidence/build/venue-s04.test` | `6421ac92cd1a625ffbc38a683109bb46314d89132483957a2bb7ef014a6eef64` |
| `evidence/build/runtime-s04.test` | `60bc91c5aa2c8cbf7b7827e562120742c4cc5c3f6261d5c576c0a2805798d85b` |
| Performance realmente medida, `evidence/performance/backtester-s04-perf.test` | `964e489360eef2d8ea6be99758ad6c289535d157bab95e02001f5154be7095b8` |

`evidence/provenance.json`, `build/build.txt`, `build/executions.json` y el manifest global fijan commands, source/test SHA, binarios y logs. Las comparaciones de performance utilizan la misma build de performance; no mezclan el binario final con mediciones anteriores.

### 2. Veredictos separados

| Dimensión | Resultado S04 | Límite material |
|---|---|---|
| DOMAIN_PARITY | **NOT_DEMONSTRATED completo; PASS_BOUND** | Backtester público vs seis owners/adapters StateFun reales, S1, NO_ADDS y CONFIGURED, mismos hechos. Account-state producer/runtime accounting independiente y transporte físico excluidos. |
| FIRST_ORDER_CHAIN | **PASS_BOUND; seguridad CONFIGURED FAIL** | Cadena inicial completa hasta terminal pasa; ADD efectivo deja exposición sin cobertura completa. |
| SIMEXECUTION_CORRECTNESS | **FAIL** | Reloj futuro, callbacks con contexto anterior, extremos revisitados, fases invertidas y fills sellados por lote. |
| OPTIMIZATION_EQUIVALENCE | **FAIL** | MM flat consumidor recibe8QUOTE/1fill en ALL y0/0 en SKIP; primera divergencia estructural preservada. |
| CAMPAIGN_ACCOUNTING | **FAIL parcial** | Cash ledger probado correcto, pero términos heredados, demora de reemplazo y agregados vacíos. |
| MODULE_SUBSTITUTION | **FAIL** | Runtime público restringido; backtester instala factory después de declarar requirements. |
| PERFORMANCE | **MEASURED_WITH_FINDINGS** | Carga activa y perfiles útiles; skip experimental, asignación superlineal y retención. No certificado3años. |
| INDEPENDENT_RUN_CONCURRENCY | **PASS_BOUND** |12 corridas,1/2/4 procesos, identidad semántica y de artifacts por RunID; beneficio medido en4 experimentos. |
| DATA_COVERAGE | **PARTIAL** |13 originales/derivados verificados; gaps reales bloquean continuidad. MIXED no implementado. |
| PHYSICAL_RUNTIME_READINESS | **NOT_DEMONSTRATED** | Sin D6 nuevo; certificado de otro SHA no transferible automáticamente. |

PASS_BOUND expresa sólo el perímetro probado. REPRODUCED = aserción independiente ejecutada; OBSERVED = lectura/source/archivo verificable; INFERRED = implicación no reproducida; NOT_RUN = prueba no ejecutada. No se rellenan pendientes con N/A.

### 3. Reproducción y oráculos

Desde el clon independiente, `reproduce-s04.sh` ejecuta cuatro grupos con timeout y falla deliberadamente cuando el candidato viola el contrato. Configura `GOPROXY=off GOSUMDB=off`: ninguna suite amplia ni dependencia externa de ejecución. Comandos principales:

```sh
GOMAXPROCS=2 GOMEMLIMIT=8GiB timeout 180s go test -p 2 ./v3/backtester -run '^TestBTGS04_' -count=1 -v
GOMAXPROCS=2 timeout 180s go test -p 2 ./v3/backtester/internal/simexecution -run '^TestBTGS04_' -count=1 -v
GOMAXPROCS=2 GOMEMLIMIT=8GiB timeout 180s go test -p 2 ./v3/backtester -run '^TestBTGS04Campaign' -count=1 -v
GOMAXPROCS=2 timeout 180s go test -p 2 ./v3/core/internal/futuresvertical -run '^TestBTGS04_' -count=1 -v
```

El prefijo/root ejecuta12 tests superiores:9FAIL y3PASS, incluyendo probe de capacidad MIXED cuyo PASS confirma rechazo, no cumplimiento. Venue2FAIL. Campaña10 nuevos,5PASS/5FAIL→4 problemas distintos. Runtime4 superiores: bounded y partial/late PASS; scaling y sustitución FAIL. El workload paramétrico de performance se ejecuta con escenarios/env específicos, no se cuenta como cobertura vacía. Logs finales prevalecen sobre exploraciones de construcción del harness.

Oráculo ALL/SKIP nuevo: comparación JSON estructural recursiva, mapeo de identidad directo/inverso biyectivo, preservación de referencias orden/fill/operación/reserva. Sólo se interpreta el campo textual con gramática conocida `stage-1 admission request <ID>`; no borrado indiscriminado de strings. Prueba negativa confirma que no acepta fill referido a otra orden ni dos IDs colapsados. Se preservan timestamps, razones, cantidades, precios/fees exactos, contexto y payload. DATASET contiene políticas distintas por construcción y no integra la comparación material; step_seq se conserva como diagnóstico, no equivalencia de número de pasos. No se afirma T35/T36 completo: este fixture no recorre todos los forming/context reads.

Oráculos independientes adicionales: frontera solicitada vs reloj, timer deadline, orden causal de fases, sufijo geométrico conocido LONG/SHORT, cobertura protectora vs exposición, caja por evento, objetivo de segunda cuenta y matemática monetaria exacta del circuito−625USD. Dos caminos con el mismo bug no pueden satisfacer estos invariantes sólo por coincidir.

### 4. Findings priorizados

Todas las referencias de source son de `xKoRx/echo@1bf45050780554c1135edc619bf01a8a4b04ba08`; todos los tests listados fueron ejecutados. Los comandos de §3 se especializan con `-run '^<nombre>$'` para reproducción mínima. P0 = bloqueo de seguridad del dominio; P1 = validez/alcance/rendimiento material; P2 = export/provenance/retención a corregir. Ninguna severidad implica orden física ejecutada.

#### S04-07 · P0 · Protección incompleta tras ADD ejecutado — REPRODUCED

Requisito B: riesgo protegido, claims/finality y q_exec_max. `TestBTGS04_RuntimeConfiguredScalingFills` usa composición real runtime + bridge simulado, GerardMM CONFIGURED, ratio0.4, cap por orden5/account-wide10. Entry5@21715, protective5@21695; TRADE/BBO alineados al fill real del add2@21705 adverso o21740 favorable. Se drenan eventos, cancelaciones y finality; cero provider denials.

Esperado: exposición7 totalmente cubierta respetando cap/finality. Actual adverso: stop5 WORKING, **2 sin cobertura**; primera divergencia en MM del ADD FILL, acciones vacías. Favorable: stop5 CANCELLED, stop2 WORKING@21722.25, **5 sin cobertura** incluso después de liberar claims. `gerardmm.go:506–528,562–585`: `!improves` evita reconciliar cantidad cuando el precio no mejora; cancel/replace protege sólo el remanente2 y no repone5 tras finality.

Evidencia `runtime/scaling-adverse.json`, `scaling-pyramid.json`, `sealed-build-tests.log` conserva órdenes, estados, entradas/decisiones MM y provider. Defecto heredado de `3069debc7`/ediciones `a5cdb410e`, no demostrado introducido por S03. S05: separar reconciliación de cantidad y tightening de precio; preservar claims hasta finality, límites y prevención de doble cierre. Rerun ambos sentidos, parciales, finality y ADD pendiente con force-close.

#### S04-01 · P1 · Walker salta el scheduler y consume futuro — REPRODUCED

Requisito A1/frozen2–5. `ohlc_driver.go:170–201,227–359,611–659`. `walkIntrabarPath` ocurre dentro de Open en vez de intercalarse como próximas coordenadas del scheduler. Tests `CausalAdvanceNeverObservesFuture`, `CausalMidMinuteControl`, `CausalMidMinuteTimer`, `CausalSimultaneousStreams` con prefijo `TestBTGS04_`.

Un minuto O100/H101/L99/C100 y `AdvanceUntil(start+30s)` devuelve frontier+30 pero reloj **+56.470588235s ALL / +59.999999999s SKIP**. Control cashflow+1 y timer provider+30s encolados previamente fallan **CLOCK_REGRESSION** antes de aplicarse. Dos streams NQH7/NQZ6 con Open simultáneo fallan **DATASET_READ_FAILED/SOURCE_ORDER_INVALID** al segundo stream. No se utilizó egress ni input fuera del catálogo. V1 con el mismo control intermedio pasa, aislando la regresión V2.

`checkNativeBoundaries` omite flat sin working; con inventario/órdenes puede rechazar fronteras internas como OHLC_BOUNDARY_AMBIGUOUS. Ese rechazo explícito es una capacidad ausente, no ejecución fiel. Timer que cree una orden después de Open y reactivación posterior quedan bloqueados por la intercalación defectuosa; no se califican PASS.

S05: entregar siguiente paso/fin de tramo al mismo scheduler que controles, timers y otros streams, limitar avance a frontier solicitada y conservar estado por intervalo. Una referencia ALL que también falla no certifica SKIP. Evidencia `causality/sealed-build-tests.log`, `clock.log`.

#### S04-02 · P1 · Flat no prueba inercia: se pierden consumidores — REPRODUCED

Requisito A2/frozen4. Guard `ohlc_driver.go:262`: net0 y sin working. `TestBTGS04_InertSkipFlatActiveMM` usa la interfaz normal MoneyManager: Operation activa flat, MM espera QUOTE para solicitar entrada; no estrategia comercial nueva ni edición interna. ALL recibe **8QUOTE/1fill**, SKIP **0QUOTE/0fills**.

`TestBTGS04_StructuralReferenceSkipFirstDivergence`: primera diferencia **record material33: OPERATION_APPLY@22:11:06.666666666Z vs ECONOMICS@22:12Z**;4 pares de IDs ya conciliados. ALL84records/ledger revision41, SKIP38/revision29. Igualdad terminal Strategy/risk no borra decisiones omitidas.

S05: capacidad explícita de cada consumidor/obligación y próxima coordenada causal; consumidor desconocido impide skip. No basta posición neta. Inventario bruto compensado no se reprodujo: el ledger soporta inventario direccional FIFO, no se inventó hedge. Matriz de reserva/admisión pendiente/fill-cancel exige rerun tras S04-01. Evidencia `equivalence.log`, tests estructurales y sealed log.

#### S04-03 · P1 · Fill/callback observa reloj y MarketContext anteriores — REPRODUCED

Requisito A3. `ohlc_driver.go:318` liquida eventos antes de actualizar clock/mark del step. `TestBTGS04_FillCallbacksSeeCurrentClockAndMark` envuelve GerardMM CONFIGURED sin cambiar decisiones y captura antes de Evaluate. Fill ejecutado **22:11:10Z** se entrega con clock/mark **22:11:06.666666666Z**; siguiente fill13.333333333 observa clock10. Tres fills, seis discrepancias de clock/mark.

S05: publicar reloj, disponibilidad/contexto y observación de precio correspondientes antes de entregar cada fill/callback; mantener orden de ledger/risk requerido. No reescribir timestamps de evidencia para ocultar el atraso. Impacta decisiones temporales, stale/risk y claims de paridad.

#### S04-04 · P1 · Close vuelve a recorrer extremos ya pasados — REPRODUCED

Requisito A3 y S02 V2. `processNativeClose`, `ohlc_driver.go:408–419`, conserva ADVERSE/FAVORABLE antes de CLOSE. `TestBTGS04_PastExtremesNotRevisitedAfterLateAdd` LONG/SHORT: barra O150/H151/L149/C150, entrada1 y ADD1 tardío **22:11:38.823529411Z**. Sufijo futuro real LONG[150,151]/SHORT[149,150]. Al Close22:12 se reaplica149 LONG/151 SHORT; luego el opuesto. Equity observada **99910.02→99990.02**, dayPnL−89.98→−9.98;2contratos cambian USD40 por punto.

Esperado: sólo sufijo no consumido y Close; actual genera riesgo/equity de un pasado que esa exposición no tuvo. Fixture no depende de recalcular PnL fuera del engine. S05: separar semántica V1/V2 y marcar trayectoria consumida por stream/intervalo; no omitir marks necesarios del recorrido auténtico.

#### S04-05 · P1 · Fases Open/Close V2 mantienen el orden V1 — REPRODUCED

Requisito S02 Open/step4 antes Close5. `driverRootPhase`, `ohlc_driver.go:34`, usa Close1/Open6. `TestBTGS04_V2CloseSignalCannotUseEarlierOpen`: **SIGNAL index63 antes OPEN index76** en2026-09-07T22:10Z. Permite señal recién cerrada aprovechar Open anterior en el mismo UTC. Primera divergencia es el orden de records; no se afirma un slippage monetario cuantificado universal.

S05: versionar las fases conforme al contrato y probar deadline/fill/signal con igual timestamp; conservar V1 golden semántico. No ordenar sólo por timestamp ocultando causalidad.

#### S04-06 · P1 · Venue sella ADD antes de protección y varios fills antes del drain — REPRODUCED

Requisito B/S02 prioridad protectora y un fill→drain. `internal/simexecution/ohlc.go:248–301`; `venue.go:539` ordena por aceptación/ID. Tests `TestBTGS04_IntrabarProtectionBeforeAdd` y `...IntrabarDrainBeforeNextFill`: long1, ADD buy1 y protective sell stop95, precio94. Primero se sella **a-add@94.5**, después stop; invertir IDs hace ganar stop pero **ambos fills ya están sellados** cuando el caller recibe el primero. Cancel más temprano posible llega tarde, net queda1 en lugar0.

S05: prioridad semántica explícita y entrega incremental para drenar efectos antes de reconsiderar el siguiente candidato; no todos contra el snapshot previo. Oráculo inspecciona eventos/net del venue, independiente de la coincidencia de dos engines. Logs `causality/sealed-build-venue.log`.

#### S04-08 · P1 · Runtime público no permite sustituir Strategy/MM — REPRODUCED + OBSERVED

Requisito B/frozen1/5. `TestBTGS04_RuntimeModuleSubstitution`: ConfigSnapshot acepta ModuleFixture y backtester público lo compone; `futuresruntime.Compose` retorna **unsupported strategy module "fixture"**. `runtime.go:185–196` sólo S1/S2; opciones61–64 sólo allocator;145 construye GerardMM fijo. Inyectar en constructors internos de Functions no acredita composición pública completa.

S05: factory común tipada de Strategy/MM resuelta por ambas composiciones antes de requirements. Rerun Strategy alternativa, MM alternativo deny, parámetros y NO_ADDS/CONFIGURED. No añadir excepción comercial al scheduler.

#### S04-09 · P1 · Requirements de Strategy sustituida se ignoran — REPRODUCED

`TestBTGS04CampaignSubstitutionRequirements`; `compose.go:364` compone streams antes de asignar factory367; `composeStreams:525` consulta builtin. Fixture normal exige5m+H4, configuración base builtin sólo5m. Después de5h05 de datos, `BAR_RANGE|NQ:NQZ6|4h|recent:1` falta en MarketContext, tanto V1 como V2.

Primera divergencia está en registro de requirements antes de warmup. S05: instalar/resolver módulo antes de construir analytics/streams; probar reads y versiones materializados, no sólo número de callbacks. Es distinto de S04-08.

#### S04-10 · P1 · Segunda cuenta hereda términos FUNDED — REPRODUCED

Requisito campaña continua, nueva cuenta EVALUATION sin autoridad financiera heredada. `seedAccountAuthorities`, `compose_account.go:96`, no actualiza `currentTerms`; sólo compose376/run224 lo hacen. `run.go:826` evalúa lifecycle con el puntero viejo.

`TestBTGS04CampaignReplacementRestoresEvaluationTerms`: después de ReplaceAccount, contexto EVALUATION target3000, términos lifecycle FUNDED/targetnil. `...SecondAccountCanPassAfterReinvestment` reproduce9sesiones: cuenta1 cobra4 y se retira; cuenta2 activa2026-09-15T22:01Z, consigue **balance105502,4fills/2operaciones y2días rentables**, permanece EVALUATION hastaSep18T21Z. Reset count1, esperado2.

Cash ledger sigue conciliado, pero segunda cuenta no puede pasar. S05: sembrar términos desde cada AccountContext nuevo junto con autoridades financieras, mantener streams/Strategy continuos. Rerun pass→4cobros→recompra→segundo pass y burn/reemplazo.

#### S04-11 · P1 · Recompra ON_DEMAND espera casi un día — REPRODUCED; interpretación declarada

`TestBTGS04CampaignBurnReplacementLatency`, `campaign.go:362–391`: EVALUATION avanza hasta account-day/horizonte; burn se inspecciona después. Breach latched+quiescence **2026-09-07T22:11Z**; reporte termina cuentaSep08T22:00, nueva activa22:01: **23h50 después**. Próximo minuto negociable del mismo día era22:12; test permite2min y falla.

Se interpreta ON_DEMAND/activación próxima1m según S02§9.1 y despacho; si Primary propone una frontera caller posterior como semántica, debe adjudicar explícitamente ese requisito, conservando la demora observada. Impacto: oportunidades omitidas, no pérdida de rings. S05: checkpoint/yield de política al desenlace material y drain, activación prospectiva; evitar polling caro por step.

#### S04-12 · P2 · Totales cobrados vacíos pese a caja correcta — REPRODUCED

`TestBTGS04CampaignCollectedTotals`:1cobro1500/caja6380 y4cobros6000/caja10760 tras recompra, pero `CollectedGross/Net` vacíos. `campaign.go:294–298` suma d.payouts; request557 sólo agrega allPayouts; además acumulador vacío produce UNREPRESENTABLE en addMoney862.

S05: acumular cobros finales de toda la campaña con cero monetario exacto inicializado y conciliar export con rows/cash. No reportar este defecto como dinero perdido/creado: los créditos probados sí son correctos.

#### S04-13 · P1 · Copia histórica superlineal para obtener última revisión — REPRODUCED/profile

`compose_account.go:314–319 latestRevision` llama `Ledger.Revisions()` que copia todo (`sdk/futures/accounting/ledger.go:899–902`); `projection.go:51` repite. Carga600min: **3.278GB asignados;2.15GiB/70,74% de alloc_space en Revisions**, latestRevision≈36%CPU acumulado. Cada lectura del último elemento copia prefijo de tamaño creciente. Datos120/300/600 y perfiles en performance.

S05: getter O(1) de última revisión/snapshot necesario sin alterar dinero exacto ni eliminar evidencia. Rerun trazas y tres duraciones; corregir antes de paralelizar trabajo dependiente. No se atribuye todo el wall a I/O.

#### S04-14 · P2 · Retención de revisiones/marks crece con duración — REPRODUCED

`ledger.go:890` append permanente,863–866 copia marks.120/300/600min retienen **665/1745/3545 revisiones**, heap vivo post-GC **3.68/6.07/10.82MB**; timers2/nativePending0. Evidencia de conteo+source, no conclusión por peakRSS. Sin OOM demostrado ni proyección3años.

S05: inventariar consumidores y retener estado/dedup/riesgo necesario más evidencia/digest streaming. No borrar MARK/equity indispensables, no floats. ResultWriter ya escribe/olvida records; no se demostró cola writer ilimitada.

#### S04-15 · P1 · MIXED_MINUTE ausente — OBSERVED + capability probe ejecutado

**REQUIREMENT_NOT_IMPLEMENTED**, no DATA_UNAVAILABLE/N/A. `spec.go:653–680` sólo acepta OBSERVED_BBO, TRADE_MODEL y OHLC_1M_MODEL_V1. `TestBTGS04_MixedMinuteCapabilityBoundary` confirma rechazo antes de consumir datos: `market_data_mode must be ...`. El PASS de probe certifica ausencia, no requisito.

Delta mínimo S05: modo/contrato de disponibilidad y selección por minuto con secuencia de ticks observados intacta, trayectoria OHLC sólo donde declarada, sin BBO observado inventado ni fallback LIVE stale. Fixtures sintéticos bastan para empezar; no comprar/descargar ticks ni bloquear la terminación OHLC por datos inexistentes.

#### S04-16 · P2 · Provenance y equivalencia serializada requieren corrección — OBSERVED

Binario actual S03 `reports/echo-backtest-s03r` **SHA2561704c037f57571b08e6c59f6ecab2e45c876a0501095990140e55089ff784745**, revision1bf4505, **vcs.modified=true**; inputs declaran `tree_clean=true`. Status sólo reports/ no trackeado: posible causa sin inferir source oculto. Reporte que cita build anterior3f1311e2…71d20d no acredita automáticamente estos artifacts. Inputs/build actual no prueban por sí solos qué ejecutable produjo archivos pasados.

V1 golden conserva RunID, records y economía: únicos diffs estructurales son campo vacío `summary.fidelity.observed_steps_policy` y digest lógico consecuente. SHA antiguo **b11bd4e7776762523f29c9dda8e264c98818f5e209c7b051e72e6e671222a637**, nuevo **9058477ae14394feda76a37719d77dca08e142b88c0095876815d6d26d25c5a1**: **no byte-idénticos**. S05 definir compatibilidad semántica/serialización y registrar ejecutable, tracked diff, untracked y artifact durante ejecución. Source `effects.applySealedFill` todavía etiqueta PriceSource OHLCModelV1 para V2: observación adicional de metadata, sin atribuir aquí cambio económico.

### 5. Paridad real acotada, campaña y pruebas que pasaron

`TestBTGS04_RuntimeBacktesterBounded` conduce `NewRunWithComposition/AdvanceUntil/Finish` y seis owners StateFun reales: market_stream, analytics, strategy, fanout, operation y provider. Mismos75 TRADE normalizados, S1/config/calendar/RunID,2026-09-29T08:00→14:11Z, disponibilidad/reloj monótono. No dos Evaluate ni dos strategy.Engine aislados.

Cadena: OPEN→admission→reserva/revalidate→submit→ACK→fill→submit/ACK protector→salida→terminal. NO_ADDS y CONFIGURED pasan comparación de señales completas, commands ordenados, cuatro entradas/decisiones MM con state/claims/economics/version/Mark/Ready, facts provider y terminal sin exposición. Runtime recibe por ingress tipado exactamente los ACK/fills sellados y observaciones económicas del histórico; los IDs tienen biyección comprobada. Ledger histórico100000→99375 y oráculo independiente `5*5*(21690−21715)=−625USD` coinciden.

**Boundary:** no account-state producer/proyector contable runtime independiente: runtime consume esas observaciones autoritativas, no recalcula contabilidad. Se prepara contexto/market antes de facts y se retienen decisiones/expiraciones hasta drenar hechos; esto no demuestra ese scheduling en Flink/transporte físico. Recorder productivo emite cero MM_EVALUATION; tap de tests preserva las cuatro evaluaciones. MMState ausente de serializer terminal se compara aparte. Falta S2 full-domain y todas las lecturas forming/barras/versiones; imports compartidos no llenan esa cobertura.

Test independiente runtime `PartialCancelLateDuplicate`: parcial2→cancel→late3→duplicado, exposición5 correcta, claims/reservas conservados hasta finality; PASS. Aún no counterpart diferencial histórico de toda esta matriz. Cinco regresiones existentes focalizadas pasan: ProviderDeny, StaleGrantInvalidation, AccountDayTargetExit, ProviderForceClose, TERM03_ForceCloseWhileBridgeDown. No sustituyen nueva matriz timeout/reconciliación completa.

Campaña independiente: tres burns producen compras5000→4880→4760→4640 sin debitar otra vez pérdidas nominales; fourth request PENDING_AT_HORIZON deja3cobros/1compra/caja9380, sin retiro ni dinero inventado. Control duplicado debita una vez, conflicto y stale digest nombrados, control posterior a horizonte queda pendiente. Piso configurado **97555.25 STATIC_LOCK**, ganancia120000 no lo convierte en trailing, touch exacto bloquea y latch persiste. Proveedor compartido evaluado con observaciones controladas, más engine burn separado: TESTED_SYNTHETIC.

**A5 resuelto:** `ReplaceAccount` conserva streams/feed/market/analytics/Strategy. Reader real de MarketContext compara61evaluaciones, readiness/5m/H4/session/versions, V1 y V2 con reemplazo vs referencia continua: PASS; cuenta nueva100000. Párrafo S03 sobre reconstruir rings está obsoleto. El fixture declara requirements builtinS2 para aislar continuidad; S04-09 demuestra por separado la factory tardía. `intrabarSteppedFlag` global y pool/estado por stream siguen OBSERVED como riesgo de aislamiento; efecto monetario específico por contaminación no reproducido porque multistream falla antes en S04-01.

Regresiones existentes adicionales offline: DST account-day25h, rollover3contratos/una cuenta/6fills/balance99782.56, gaps OHLC middle/tail/warmup y diagnósticos de fuente offending pasan. Son fixtures de sus modos existentes, **no certificación de V2 multistream**. Siete regresiones de venue ticks pasan: next-cursor ask/bid, stop espera quote, cancel-before/too-late, accepting-cursor no fill y market sin quote espera. No generación de ticks sintéticos LIVE.

### 6. Rendimiento, I/O y concurrencia

Workloads con igual build/datos/config/instrumentación por comparación. Tabla Run wall excluye creación de corpus de fixture; CPU/RSS son proceso instrumentado. Alloc en MB decimales. ALL/SKIP **experimental**, aunque un fixture coincida, por S04-01/02.

| Workload | Wall s | User+sys s | Alloc MB | RSS KiB | Revisions |
|---|---:|---:|---:|---:|---:|
| LONG120min CONFIGURED ALL |1.138|1.09+0.08|258.6|26684|665|
| LONG300min ALL |3.934|3.65+0.36|1025.8|35356|1745|
| LONG600min ALL |10.714|9.85+0.99|3278.3|58144|3545|
| SHORT120min ALL |1.177|1.16+0.05|258.4|25900|665|
| LONG120min SKIP |1.065|1.04+0.08|231.1|25752|665|
| LONG120min ALL+writer |1.340|1.25+0.09|267.2|28276|665|
| Warmup115min+5inert ALL |0.734|0.72+0.04|228.2|22344|243|
| Mismo warmup SKIP |0.123|0.13+0.02|18.5|20356|243|
| Adds120min ALL |0.254|0.27+0.02|48.3|21044|252|
| Flat wide120min, K48000 ALL |30.139|29.26+1.10|10840.8|34400|243|
| Mismo wide SKIP |0.119|0.11+0.04|18.6|19784|243|
| Flat-doji120min K0 ALL |0.152|0.16+0.02|18.6|19400|243|

Carga sostenida120 mantiene50contratos durante105min;300/600 durante285/585min; asserts verifican exposición efectiva. Adds produce4fills/protección, no carga máxima. Warmup mide22evaluaciones de fixture, cero fills; no representa51H4 de S2 ni separa warmup/trading por temporizador interno. Multistream no se mide como capacidad sana después de su fallo. K potencial calculado; records/bytes/GC/heap en JSON. Contadores internos exactos dispatched/skipped y triggers por consumidor **NOT_DEMONSTRATED**, instrumentación mínima pendiente sin justificar framework.

LONG600 entrega12661records/9393888JSONbytes. Perfil writer: Record7.58%,gzip/flate3.79%; OwnerState.clone con roundtrip JSON≈50%CPU acumulado. Añadir writer cuesta≈0.20s en120min; no demuestra beneficio de compresión paralela. Major faults0, filesystem inputs0 para fixtures; **iowait exacto no medido**, no confundir sysCPU con espera. No extrapolar a disco remoto ni3años.

Campaña con burn/reemplazos y payouts/pausas también medida, sin dividir continuidad: primera suite8tests wall45.15s/user57.46/sys3.06/RSS166872KiB incluye compilación;9sesiones reinversión wall22.84/user29.45/sys1.71/RSS176300KiB. Resultado funcional mixto documentado, no certificado económico. Varias CPUs user>wall no implica trayectoria paralela.

**Experimentos independientes:** sustained LONG/SHORT y adds LONG/SHORT, cada uno RunID/digest/output propios.1worker3.5558s;2workers1.9353s (**1.84x**);4workers1.5151s (**2.35x**). Una observación por configuración, sin intervalo estadístico. Orden invertido con2workers; **12trazas completas framed y12result.json.gz idénticos por RunID**, sin quitar IDs/records. Dos fallos recorder en economics50 producen mismo prefix/error **RECORDER_FAILED**, root ordinal32/step334/22:15Z, ejecución FAILED. No ENOSPC real ni cancelación kernel probados. Race acotado de performance PASS; race de falsificadores sin avisos DATA RACE pero funcionalmente FAIL, no se anuncia como gate verde.

**Decisión S05:** un escritor por trayectoria dependiente; procesos2–4 para experimentos/BASIC/CAMPAIGN independientes con buffers/output separados tienen beneficio medido. Nunca días/cuentas/expiries/fills de una trayectoria en paralelo. Priorizar getter O(1), retención y clones redundantes. Parsing/prefetch/hash/compresión son candidatos sólo si perfil futuro lo justifica; no construir pool genérico ahora. Mantener exactitud monetaria, MARK/equity/riesgo/evidencia y backpressure/error/cancel si se incorpora I/O concurrente.

### 7. Fuentes reales, continuidad y producto existente

13 originales locales transferidos desde Daedalus verificados contra manifest SHA: **1096336rows**, extremos nominales2023-10-01T22:01Z→2026-10-06T03:50Z.13 derivados son subsecuencias byte-exactas,226líneas excluidas verificadas por hash,1096110retenidas. Originales inmutables. Inventario S01 reporta24831min abiertos ausentes; S04 revalidó archivos/hashes, no repitió el censo de calendario completo.

Primer bloqueo RAW NQZ3: línea8416 termina2023-10-10T00:16Z y8417 termina00:19Z; faltan intervalos[00:16,00:17) y[00:17,00:18). No rellenar ni atribuir feriado/no-trade por conjetura. Derivado NQZ3 elimina6outside-session; segmento elegible históricoOct10T00:31→Nov23T03:29. WarmupOct15T22 permite ventana Oct29 hasta esa frontera de cobertura. Es frontera de datos inspeccionada, no recomendación de correr todo bajo V2 defectuoso.13archivos no prueban3años continuos ni permiten sumar saldos iniciales de expiries.

| Modalidad | Implementación / evidencia |
|---|---|
| OHLC-only | IMPLEMENTED / TESTED_SYNTHETIC nuevo / TESTED_REAL en artifacts existentes; correctness V2 FAIL. |
| Ticks observados / TRADE_MODEL | IMPLEMENTED / TESTED_SYNTHETIC acotado, secuencia/venue y comparación runtime; TESTED_REAL nuevo NOT_RUN. No BBO observado inventado. |
| MIXED_MINUTE | REQUIREMENT_NOT_IMPLEMENTED; rechazo ejecutado S04-15. |

BASIC existente V2+CONFIGURED: warmupOct15T22, tradingOct29T22→Oct30T22,9fills/7operaciones/−2123.80USD. Artifact y fresh reproduce ya presentes tienen SHA **b4d193f6c3ac5ede786dbdc2949eb3d667e9a09aaed2a1655868123726003939**, RunID `bt-b15d13d1c100dfd0e3f2fee1f8b878f41438a1055f2a57380830937a37ff36d6`. **Readback de archivos, no fresh rerun S04**.1m35s histórico no remedido.

CAMPAIGN existente: warmup2023-10-15T22Z, trading **2023-10-29T22Z→2023-11-02T22Z exclusivo =96h/4sesiones23h**, no3días. SantiagoOct29 19:00−03→Nov2 19:00−03. Sesiones abrenOct29/30/31/Nov1 22Z, cierran21Z siguiente.1compra,5000→4880,0payouts,20fills/24operaciones, balance98007.24/EVALUATION/ACTIVE_AT_HORIZON. Artifact SHA **936b5c553dbc45b52eb784da71f4f26ec5d6617d8e6f0abac963d4e4d9a25450**.3m23s no remedido. Ese caso no prueba burn, touchfloor ni reinversión; nuevos sintéticos cubren y falsifican esas superficies.

### 8. Límite físico y pendientes reales

D6 canónico `artifacts/d6-final-physical-certification-20261005/D6-FINAL-PHYSICAL-CERTIFICATION.md` pertenece a `d08a30ce9815f820fda7132e20dc42cc345eb8e8`. Git confirma **no ancestro** del SHA auditado; merge-base `7fbd7e990ac6628df3e4cc2717e96efd83bfbbf6`. Difieren NinjaTrader adapter/AddOn/recovery tests (`runtime/d6-differing-files.txt`). C0–H/G-REALTIME sólo reutilizables para su ambiente/build/componentes realmente invariantes. Ladder final allí bloqueada antes de egress,0órdenes; primera orden física y escalones siguientes NOT_RUN. S04 no repite D6 ni certifica plataforma/red/broker.

Pendientes explícitos: paridad completa S2/account-state producer/accounting runtime/transporte; matriz diferencial cancel/late/duplicate y close/force-close+ADD; alternativos MM públicos; pending admission/reserva y timer que genera orden una vez reparado scheduler; rechazo/timeout broker y reconciliación nueva completa; todo forming/context reads/bar/riskcurve/caja T35/T36; aislamiento económico del pool/flags por contrato/cuenta; V2 DST/roll multistream; real ticks y MIXED;3años continuos sobre gaps resueltos por política autorizada; counters precisos por consumidor e iowait; fallos ENOSPC/cancel/drain I/O y writers al mismo path. Ninguno oculto como N/A. No nuevo riesgo sin autoridad ni safety bloqueada por datos de entrada sigue siendo obligación de S05.

### 9. Reparaciones mínimas y reruns S05

1. **Seguridad compartida S04-07**: cantidad protectora después de ADD y finality, sin resize de exposición no autorizado. Conservar parciales/duplicados ya verdes.
2. **Causalidad/venue S04-01/03/04/05/06**: scheduler incremental, frontier, clock/mark antes de callback, fase V2 correcta, no extremos repetidos, protección y drain uno por uno; estado por stream/intervalo. Reejecutar todos los falsificadores, timers/materialcontrol y multistream antes de economía larga.
3. **Skip S04-02**: no certificar ni habilitar por net0/!working. Desconocidos impiden el atajo. Definir demanda/obligaciones/próxima coordenada causal usando seams existentes; T35/T36 estructural con IDs relacionados y estado/contexto completo.
4. **Composición y campaña S04-08…12**: factories antes de requirements, dominio público intercambiable, currentTerms nuevo, checkpoint causal de burn y sumas exactas campaña-wide. Rerun primera y segunda cuenta con cuatro cobros efectivos, pauses/pending y MarketContext continuo.
5. **Costo S04-13/14**: O(1) último estado, streaming/retención revisada, eliminar snapshots/copias redundantes medidos. Preservar marks/risk/digest; luego medir1/2/4 experimentos independientes y misma traza. No optimizador, portfolio, servidor de profiling ni cambio de dinero a floats.
6. **MIXED/provenance/cobertura S04-15/16**: delta mínimo controlado; compatibilidad V1 explícita; build/artifact link real. Una vez semántica corregida, rerun BASIC100000 y CAMPAIGN5000/compra120/una cuenta/máximo4cobros con S2/GerardMM actuales y horizonte válido completo, sin recortar warmup/trading para fabricar velocidad.

S05 recibe reparaciones y límites para ejecutar y entregar resultados a revisión del Owner. No S06, aceptación propia, tuning ROI ni despliegue. Los casos negativos quedan rojos como evidencia, no se cambian asserts para pasar.

### 10. Evidencia durable y cierre del auditor

Workspace externo Aranea `work/btg-s04-god-20261007/`: `echo/` tests y `evidence/` logs, perfiles, JSON, manifests y builds; script `reproduce-s04.sh`. Manifest `EVIDENCE-SHA256SUMS` (**226 archivos**, SHA256 `beef01ef8b2f3e115120160eac2c7837adfcec89e4aae53355c5ad70826adc53`), bundle `BTG-S04-evidence.tar.gz` (SHA256 `1de87cb240a217b79cd192d3663a04cfb2daa4ed4bacc77090838a0ae171897f`, 39078645 bytes) y parche `btg-s04-tests.patch` (SHA256 `5f6d730a2ade1a9e29d9826e47f239dcd94901c60b08443999009caf7d759c2c`) entregados junto al informe. El bundle contiene fuentes de tests, builds y evidencia; hashes individuales readback verificados. El informe canónico vive sólo aquí; fragments de workers son soporte externo, no nuevos informes canónicos.

Clasificación: falsificadores de invariantes PERMANENT_REGRESSION candidatos; comparator/context-reader/runtime differential y workload verificable HARNESS_TOOLKIT_CANDIDATE; scripts de profiling/orquestación DISPOSABLE_REPRODUCER. No promoción de framework/skill durante S04. Fricción reusable: comprobar exposición efectiva del benchmark y requirements realmente materializados; una ruta idénticamente incompleta no es oráculo. Registros y feedback de los cuatro agentes validados; cierre propio por delta. Continuidad en BTG-PLAN, sin duplicar L0/L1/memoria global ni cerrar programa/sesión Primary. Quota UNKNOWN. No gate aceptado.

## Fuentes

- Despacho Owner BTG-S04 actual y [[BTG-S03-OWNER-MANDATE-20261006]].
- [[BTG-S02-DESIGN]] aplicable; [[BTG-S03-IMPLEMENTATION]] histórico; [[BTG-S03-REMEDIATION]] claims UNREVIEWED; [[BTG-PLAN]] por delta.
- S01 seleccionado: `xKoRx/agents-os@e4a177eb:main/10-projects/Echo Futures/artifacts/backtester-stage2-real/BTG-S01-REAL-GERARD-RESULT.md` y `BTG-S01-REAL-GAP-FORENSICS.md`; manifests revalidados, calendario total histórico no rehecho.
- `xKoRx/echo@1bf45050780554c1135edc619bf01a8a4b04ba08`, commit local tests `d5b16049bbee7295063e88d8d8f7fa0a4bbe34fe`; `evidence/provenance.json` y manifest global.
- Soportes externos `evidence/runtime/summary.md`, `campaign/summary.md`, `performance/summary.md`, logs finales y perfiles. Sus límites se integran arriba y no se transforman en gates por autoridad del implementador.
