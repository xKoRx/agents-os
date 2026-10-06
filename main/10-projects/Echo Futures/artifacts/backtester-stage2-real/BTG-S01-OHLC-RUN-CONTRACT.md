---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[BTG-S01-OWNER-S2-BARS-AUTHORITY]]"
  - "[[BTG-S01-SOURCE-BAR-SDK-FINAL-REVIEW]]"
  - "[[BTG-S01-IDENTITY-CONFIG]]"
  - "[[BTG-S01-S2-1M-FORENSICS]]"
  - "[[Echo Futures — BT-S01 Backtester V1 Design]]"
last_verified: "2026-10-06"
confidence: verified
aliases: []
tags:
  - kind/resource
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 — contrato propuesto del port OHLC y del primer run

## Síntesis vigente

**READY_FOR_MANAGER_SDD_FREEZE**, limitado a interfaces e implementación técnica de input/driver/venue, sobre `xKoRx/echo@407e03dd7ebce1f93b04ea5ff5bb5a33f1bac1ef`. Este artifact es una propuesta de PLAN_REQUEST y forensics, no aprobación Owner de un nuevo perfil económico ni SPEC/PLAN/TASKS de producto ya congelados. El prerequisito SDK tiene revisión independiente favorable; la ingesta completa de NT, el port y el run real siguen sin certificación. Root informó 13 exports físicos Last en un stage legible y un worker de adquisición en curso; este shot no inspeccionó sus bytes ni atribuye formato, timezone o cobertura.

La siguiente entrega debe extender el mismo Backtester V1 mediante un payload SourceBar nativo, un modelo OHLC explícito y el driver causal existente. Reutiliza S2 H4/5m, GerardMM, Operation, Provider, Calendar/SessionGrid, ledger, fills/finality, controles y artifacts. No requiere otro engine, MM alternativo, Strategy aproximada, pseudo ticks, BBO inventado ni un campaign framework.

**FIRST_REAL_RUN_CONFIG = BLOCKED_CONFIGURATION_AUTHORITY.** Dos EVAL account-days después de warmup real evitan necesitar rows day3+ o funded, pero las rows Owner SL USD2000/TP USD1500 no completan un snapshot account/provider/calendar/scaling/costos. El inventario vigente [[BTG-S01-IDENTITY-CONFIG]] no recuperó uno instalado. El port puede implementarse y verificarse mientras se obtiene esa autoridad. `OHLC_PATH_AMBIGUOUS` es un resultado diagnóstico admisible; no implica que GerardMM real haya sido ejercido hasta COMPLETE.

## Evidencia y provenance

### Baselines y autoridad

- SDK prerequisite `407e03dd7ebce1f93b04ea5ff5bb5a33f1bac1ef`, rama `codex/btg-s01-source-bars-remediation`, worktree observado limpio y HEAD exacto; cinco archivos SDK productivos bars/analytics en delta respecto al certificado. El reviewer previo comprobó 407 igual a remoto.
- Backtester certificado `cd451972b242c8933321e03001decd4b6d778c61`; Echo master `372af59a7b83604781346613da01e3d510ea1360`; D6 `d08a30ce9815f820fda7132e20dc42cc345eb8e8`; Agents-OS master `07ea74689eeb56988653cce61cc836be32c0effe`. Root refrescó esos refs al despachar; este shot no hizo otro refresh remoto ni mutó sus ramas.
- Autoridad Owner [[BTG-S01-OWNER-S2-BARS-AUTHORITY]]: S2 actual `S2_H4_TREND_BB_PULLBACK_V1`, H4 trend/5m entry MARKET después de BAR_CLOSE, histórico NQ Last1m real, SL primero cuando la misma vela toca SL y TP; expiries físicos y rollover determinista; sin cambios de señal/riesgo para mejorar métricas.
- [[Echo Futures — BT-S01 Backtester V1 Design]] y [[Echo Futures — BT-S04 Final Remediation and Certification]] conservan cuentas, controles, scheduling TRADE/BBO, economía causal, identity/artifacts y límites V1. El delta OHLC debe describirse aparte y preservar su compatibilidad.
- Echo AGENTS/CONSTITUTION y reglas 01/02/08/09/10 leídas: coordinator sin writes de código, PLAN posee AllowedFiles, tests anteriores preservados; no suites con egress ni seeds. Router Aranea y contrato Echo/Forge cargados; alcance local, sin infraestructura/trading/AddOns ni accounts físicos.

## Cápsula compartida mínima B/C

### Puerto y normalización — propietario B

Conservar `DatasetSource`, `DatasetSelection`, `HistoricalCursor` y `Candidate` actuales. Agregar `SourceBar *bars.SourceBar` a `HistoricalRecord`. El record legacy mantiene Candidate y SourceBar nil; el record OHLC mantiene SourceBar y Candidate vacío. Nunca ambos ni ninguno. QuoteSideEvidence sólo es legal en Candidate QUOTE. No se agrega una interfaz de engine por codec.

```go
// API propuesta para congelar en B; nombres finales deben quedar iguales para C.
type HistoricalRecord struct {
    SourceRecordRef string
    SourceOrder int64
    Candidate market.MarketCandidateEnvelope // contrato existente
    QuoteSideEvidence *QuoteSideEvidence     // contrato existente
    SourceBar *bars.SourceBar                // nuevo, exclusivo
}
func (r HistoricalRecord) Validate() error
func (r HistoricalRecord) StreamID() string
func (r HistoricalRecord) AvailableAt() time.Time
```

Para OHLC, `AvailableAt()` devuelve SourceBar.AvailableAt, `StreamID()` devuelve SourceBar.StreamID y `SourceOrder == SourceOrdinal`, `SourceRecordRef == RecordRef` son validaciones. Para legacy, AvailableAt sigue siendo Candidate.EventTs y los resultados serializados/identidades anteriores no cambian por nil/omitempty. B debe validar exclusividad y coherencia antes del primer efecto; C conserva admisión causal, conteos y EOF. No usar SourceOrdinal como canonical StreamSeq ni cantidad de trades.

`bars.SourceBar` del freeze ya fija StreamID, SourceBarID, RecordRef, ordinal positivo, intervalo exactamente1m, AvailableAt>=IntervalEnd, OHLC exacto positivo y consistente, volumen entero no negativo y SourceDigest. Intervalos menores, mayores o cruzados no se parten ni se completan artificialmente; un partial export se reporta/rechaza con referencia. La ingesta base usa AvailableAt=IntervalEnd cuando el export comprobado lo soporta; cualquier latencia histórica explícita entra en el contrato.

El adapter propuesto `internal/datasets/ntminute` recibe archivos y descriptor validado por caller. Su descriptor fija mapping export→contrato físico, método/schema comprobados, timestamp end, timezone/tzdata/offset y plantilla de sesión. Layout, pathname Windows y read receipt quedan fuera de logical identity; bytes originales, checksum y parser version se conservan en el manifest de representación. El manifest lógico fija normalized schema, streams, orden, cobertura, conteos/digests y referencia durable. Cambio de timezone/interpretación del intervalo cambia registros/digest. Un DST repetido o inexistente sin desambiguación suficiente produce error, no un offset adivinado.

El adapter hace k-way merge bounded de streams ordenados con desempate estable por instant/stream/sourceordinal/ref. Parsing exacto decimal→units.Price, sin float64; volumen sin redondeo. Orden/registros repetidos se validan; duplicate ID idéntico es no-op sólo bajo el contrato compartido, payload distinto es conflicto. La selección valida contrato y rango; no filtra silenciosamente un corpus equivocado. No concatenar expiries como un stream merged ni deducir identidad de un nombre NT current.

### RunSpec e identidad — propietario B

Agregar `MarketDataOHLC1mModel = "OHLC_1M_MODEL_V1"`; ejecución exige policy explícita `SL_FIRST_NEXT_OPEN_V1` y ambiguity policy `FAIL_VISIBLE_V1`. Estas identifican el modelo acotado descrito aquí, nunca una observación intrabar. Representar los parámetros en un bloque OHLC opcional bajo ExecutionModel y/o ValuationModel, omitido para legacy, con tipos cerrados; nombres concretos de campos son libertad técnica B pero C recibe el freeze antes de escribir.

- BidOffsetTicks/AskOffsetTicks no negativos, SlippageTicks no negativo, FeePerContract Money/currency explícitos, TIF resolved explícito, freshness del mark modelado y calendario negociable. Cero es legal sólo escrito; ausencia no se resuelve como cero.
- Versiones de modelo, end/open ordering, SL-first, ambiguity, offsets, fees, slippage y régimen de freshness pertenecen a ImmutableInputs y BaseImmutableInputs vía ExecutionModel/ValuationModel. Las mismas config/dataset/time bounds producen input_sha256 igual en proceso fresco; cambiar cada parámetro material lo cambia.
- Mantener `NET_FIFO_LIQUIDATION_V1` y aritmética exacta. Bid/ask del modelo son executable-side/valuation evidence declarada, no quote observada. No poblar canonical QUOTE/BBO o TRADE con esos precios.
- Rechazar combinación OHLC con OBSERVED_BBO, TradeModel implícito, quote-side claims o modelo sin policy. Preservar validation y artifacts de datasets TRADE/BBO.

No se necesita editar `identity.go` si la nueva configuración ya queda transitivamente serializada en ExecutionModel/ValuationModel; su AllowedFiles permite hacerlo sólo para un cambio justificado y compatible, verificado contra baseline.

### Clock y fases — propietario C

Un record completo es conocido en AvailableAt/end. El driver descompone su consumo modelado en un Open causa distinto a IntervalStart y un closed-source causa en AvailableAt. El Open sólo expone Open, stream/contract y refs del modelo; H/L/C/volumen del minuto no están en ningún scope/MarketContext/ledger/Strategy hasta closed-source. Que el decoder ya tenga bytes completos no autoriza leerlos desde decisiones del Open. No se retrocede reloj ni se asignan timestamps de ticks inexistentes.

En una frontera ordinaria `t=end(A)=start(B)`, el batch OHLC comprometido de A y BAR_CLOSE5m/H4/Signal/admission/ACK/drain concluyen antes del Open B, aun compartiendo UTC. Una orden aceptada por ese Signal puede llenar en Open B como cursor posterior físico de su contrato, jamás en Close A ni con extrema de A. El ordinal causal/phase del modelo fija el orden y queda en evidencia. TRADE/BBO mantienen sus fases existentes, incluida expiry de fase5 posterior al cursor fase4.

El minuto abierto tiene settlement modelado en end con evidencia `[start,end)` y policy/phase/source ref. Si un account-day/session/provider/control/expiry boundary cae dentro del intervalo, no reatribuir ni repartir extremos: diagnóstico antes de mutación económica dependiente. Si un boundary coincide con end, no dejar que un stop intrabar se atribuya automáticamente al día/provider posterior. Para el slice inicial, cuando el orden entre settlement del intervalo previo y boundary pueda cambiar el outcome con exposición/órdenes, fallar `OHLC_BOUNDARY_AMBIGUOUS` y conservar prefix; permitir boundaries sin obligación o sin discrepancia demostrable. Una política futura de atribución requiere freeze explícito; no se cambia la arquitectura del scheduler para esconderlo.

`HistoricalRecord.AvailableAt` no basta como única raíz del loop: se necesita la raíz Open sin HLC y el cierre del payload posterior; de lo contrario MARKET@BAR_CLOSE pierde el Open siguiente o se filtra el futuro. En AvailableAt retrasado, un Signal sólo puede ejecutarse en el primer Open posterior a su verdadera admisión, nunca en un Open ya consumido.

## Reconstrucción y contexto de mercado

Usar `analytics.Input{SourceBar:...}` y sus effects reales. Cada source1m alimenta directamente los builders5m/H4 instalados mediante SessionGrid; 5m no alimenta H4. Source provenance del freeze conserva referencias/intervalos/digests sin canonical stream/trade counters ficticios. Closed source no revisa agregado cerrado; corrections TRADE heredadas permanecen projection-only.

La cobertura de source1m es una dimensión explícita. Missing-minute en intervalo negociable esperado bloquea readiness y BAR_CLOSE evaluable del agregado afectado. SourceBarCount aislado no prueba que los intervalos cubran toda la región. Un gap closed-market se explica por el Calendar y no exige interpolación. El slice mínimo puede detener el run en `SOURCE_COVERAGE_INCOMPLETE` al primer gap material, con reporte; recuperar y seguir requiere volver a una historia analítica completa/consecutiva para las demandas reales, nunca declarar ready porque llegó el siguiente minuto. Preservar snapshots parciales sólo como diagnóstico y no como entradas silenciosas de S2.

Warmup usa datos reales, Warmup=true, cero Signals/ciclos/fills/fees. S2 defaults congelados: SMA50 H4 exige51 barras H4 cerradas y Bollinger20 exige20 barras5m, con eligible H4 `CloseBoundary <= entryBar.BucketOpen`. El preflight genérico existente sólo verifica alguna evaluación warmup: el port debe evidenciar los counts/cobertura concretos y el gate S2; no afirmar readiness desde ese check conservador. Warmup no consume EVAL ordinal.

**Seam descubierto que no puede omitirse:** `config/views.go:163` sirve Mark sólo desde `current:trade`. Direct SourceBar→analytics no da Mark a GerardMM. C debe componer un `runViews` local que embebe `*config.SnapshotViews` y sobreescribe sólo `Market()` con `operation.MarketContext` modelado, más `operation.ExecutableQuoteSource` para sizing del lado correcto. El contexto es por contrato físico con sourceRef/phase/asOf/model version y ready/freshness; métodos de config, Provider, MM selectors y actualización económica siguen heredados. No modificar SDK config/views ni poner modelo en TradeLadder/QuoteLadder; el feed compartido sigue siendo dueño de bars/readiness/session para Strategy.

Un mark del contrato futuro en preparación no valoriza inventory del anterior. Marks con obligación se actualizan mediante ledger.ApplyMark y la proyección económica existente antes de decisiones. La evidencia de freshness/coverage debe servir los misses a MM; no devolver último close como válido fuera del régimen explícito.

## Venue mínimo y límites MM

1. MARKET pendiente llena al primer Open posterior elegible de su contrato/stream y sesión con lados modelados y slippage. No hay liquidez/depth/impact aleatorio ni fill en accepting cursor. Expiry, Provider cutoffs y falta de datos pueden impedirlo.
2. Resting STOP_MARKET mantiene protección incluso si S2 no está ready. Si Open salta el stop adversamente, fill en Open adverso/lado ejecutable más slippage; si hay cruce interior sin gap, se usa stop trigger/lado modelado bajo policy. Nunca regalar stop price cuando el Open ya es peor.
3. Entry al Open sólo permite inspeccionar SL/TP del entrybar después de ese fill. Entry al Close/Signal nunca se somete a extremos anteriores del triggerbar.
4. Para exposición/thresholds estables, SL y TP tocados en el mismo minuto resuelven SL antes del profit-exit por autoridad Owner. TP es la condición monetaria account-wide de GerardMM, con fees/PnL/headroom reales; no una nueva LIMIT ni la basis Bollinger. El driver sólo hace visible la causa modelada al runtime compartido, no sustituye `Manager.Evaluate` con su propia fórmula de decisión.
5. Hechos salen por SealedEvent→applySealedFill→ExecutionFill/ExecutionUpdate→reconcile/finality→ledger/provider/economics→drain reales. FeePerContract se cobra una vez por fill/qty/lado; spread/slip ya incluidos en precio, sin segundo descuento. CANCEL_REPLACE/finality heredados conservan causalidad.
6. Los adds actuales se disparan por MMTriggerQuote y usan el MarketContext; un modo OHLC que sólo entrega AccountEconomics no ejercita todo el MM. No fabricar QuoteUpdate/canonical quote para simularlos ni omitirlos silenciosamente. Antes de comprometer un minuto, detectar si adds o changes dinámicos de stop/objetivo admiten trayectorias económicamente distintas; fallo nombrado `OHLC_PATH_AMBIGUOUS`, incluyendo sourcebar/config/Operation/thresholds y digest del estado previo, sin efectos del minuto. Una prueba conservadora que no pueda excluir esa posibilidad debe fallar visible, no asumir orden.

Una trayectoria O-L-H-C/O-H-L-C no está autorizada ni demuestra menor PnL universal; un add puede cambiar quantity, target, stop y fees. Para ejecutar esos minutos hasta COMPLETE hace falta una política modelada Owner concreta o histórico más fino suficiente. Incluso scaling nil no elimina necesariamente stop/TP dinámicos de economía/fills; tampoco está autorizado elegir nil sólo para que el run pase.

No crear un framework de branching/exploración de todas las rutas para este shot. La implementación mínima certificable tiene path estable más diagnóstico conservador de lo no resoluble. Si no puede aplicar el contrato monetario TP mediante runtime real sin inventar política, reportar ese bloqueo; nunca declarar COMPLETE de Gerard por un venue que sólo cubre stops.

## Rollover y primer slice real

Reutilizar catálogo/schedule/prepare/selection/pins/DRAIN_CYCLE. El schedule debe tener fuente explícita de roll dates físicos; ni MergeNonBackAdjusted ni el archivo NT current prueban cuándo seleccionar cada expiry. El corpus de adquisición puede confirmar contratos/cobertura/overlap, pero el calendario de roll no se deduce de una continuidad merged o del mayor volumen sin autoridad. No transferir exposure, cambiar entry price ni marcar old-contract con new-contract. Si falta old-contract para drenaje, error `OLD_CONTRACT_DATA_UNAVAILABLE`.

Un primer smoke puede usar un solo expiry con suficiente prehistoria real y dos account-days EVAL autorizados; no necesita roll schedule multi-expiry ni funded/day3. Debe fijar trade_start/end a cobertura comprobada, obtener51 H4/20 5m cerradas completas y mantener accounting/context/start state explícitos. Esto certifica sólo el slice; la prueba Owner de rollover y el horizonte solicitado de tres años siguen pendientes. Un run que pasa calentamiento pero encuentra ambigüedad es un diagnóstico reproducible, no Stage2 completo.

## Recuperación de configuración: valores existentes frente a nuevas decisiones

| Campo | Autoridad recuperada | Qué todavía falta para el run |
|---|---|---|
| Strategy | Owner S2 actual; defaults source/D4-B1 SMA50/BB20/dev2/lookback64/buffer1 | Materializar exact config/digest, tick_size del contrato y stream físico; no nueva optimización. |
| MM planes | EVAL ordinal1/2 SL USD2000 / TP USD1500; selectors exactos en shared code | Materializar dos rows/selectors con account boundary real. No day3/funded si el run no los alcanza. |
| MM scaling | Schema y ResearchScaling seed existen; nil falla closed para adds en BACKTEST | Config scaling actual o elección Owner explícita. Seed/nil no es baseline real autorizado. |
| Account/context | V1 una cuenta, starting flat; Generic100K fija initial USD100000 sólo cuando se elige ese contexto | Perfil/contexto/binding/stage/ordinal/reset y estado económico inicial consistente. No nominal de D6 inferido como selección. |
| Provider | Shared GAU50-EVAL@1 documentado: GROSS6, DLL1100, trailingEOD2000, ventanas Chicago, consistencia30%; Generic SIM soportado | Owner debe seleccionar perfil aplicable. GAU50 de D6 y fixture SIM no son autoridad automática BTG. Terms/min traded days/target pueden quedar explícitamente ausentes para diagnóstico sin PASS de prop. |
| Calendar | SessionGrid/Calendar resolver shared y timezone/tzdata forman identidad | Dataset de calendario/overrides históricos comprobado para el rango, NT export tz/template y boundary de cuenta. Plantilla NT no sustituye calendar contract. |
| Costs/model | V1 soporta offsets/slippage/fees explícitos, incluso cero declarado | Números aplicables o elección de modelo declarada; no default de tests, BBO observado ni costos reales inferidos de Last. |
| Multi-expiry | Catálogo/schedule/pins existentes y Owner pide rollover físico | Cobertura old/new y fechas de selección con provenance. Puede diferirse sólo para smoke de un contrato. |

[[BTG-S01-IDENTITY-CONFIG]] comprobó mediante canales RO ausencia de `/echo/development/futures/config_snapshot` y `/futures/enabled`, ningún catálogo Gerard/Futures recuperado y CoreDEV physical source master sin runtime Futures. Configs locales recuperadas eran transporte/AddOn, fixtures y artifacts Forge. Ese reporte es evidencia instalada acotada, no inexistencia universal. Este shot no repitió probes ni amplió permisos/infra.

**Input mínimo Owner realmente nuevo:** referencia exacta al snapshot account/provider/MM scaling/calendar/costos que quiera usar; si no existe, seleccionar y aprobar un paquete offline concreto con esos campos resueltos y digeridos, preservando S2 y las dos rows2000/1500. Esa selección puede ser un único perfil compuesto en vez de muchas preguntas sueltas. No preguntarle otra vez por alias S2, parámetros default, day1/2 ni rows funded/day3 que el slice no usa. La decisión intrabar dinámica sólo se solicita cuando el diagnóstico o el perfil elegido pruebe que el slice la necesita; la regla SL-first ya decidida se mantiene.

No existe base para afirmar que hoy los dos días pueden correr con una configuración sharedProvider/account actual recuperada. Sí existe base para implementar el port, construir un candidato de RunSpec y recuperar datos; únicamente una autoridad adicional sobre los campos faltantes lo convierte en primer run exacto. Proponer costos0 o adds off es nueva elección declarada, no recuperación de actual Gerard.

## AllowedFiles propuestos y dispatch sin escritura concurrente

Root informó freeze B input-only en `specs/btg-s01-ntminute-ingress/{SPEC,PLAN,TASKS}` y dispatch NORMAL de implementación sobre407; ese paquete vigente prevalece sobre el mapa propuesto B aquí. C necesita su SPEC/CHANGE, PLAN y TASKS congelados antes de implementar. El inventario NT de Root confirmó ls y muestras endpoint; la adquisición de bytes completos aún no fue comprobada por este shot. Este worker sólo entrega el mapa como PLAN_REQUEST; no escribió esos archivos en el repo de producto.

**B — parser/dataset/RunSpec (propuesta; el freeze Root input-only es autoridad):** modificar sólo `v3/backtester/dataset.go`, `v3/backtester/spec.go` y, únicamente si hay razón de identidad, `v3/backtester/identity.go`. Nuevos `v3/backtester/internal/datasets/ntminute/ntminute.go`, `v3/backtester/internal/datasets/ntminute/ntminute_test.go`, `v3/backtester/ohlc_spec_test.go`, `v3/backtester/ohlc_dataset_test.go`. No driver/venue/SDK/CLI ni tests existentes. Puede agregar archivos helper nuevos bajo ntminute sólo tras ampliar AllowedFiles en TASKS; no wildcard de writes.

**C — driver/venue/context:** modificar sólo `v3/backtester/driver.go`, `v3/backtester/run.go`, `v3/backtester/compose.go`, `v3/backtester/compose_account.go`, `v3/backtester/projection.go`, `v3/backtester/finish.go`, `v3/backtester/effects.go`, `v3/backtester/internal/simexecution/venue.go`. Nuevos `v3/backtester/ohlc_driver.go`, `v3/backtester/ohlc_market_context.go`, `v3/backtester/ohlc_driver_test.go`, `v3/backtester/ohlc_market_context_test.go`, `v3/backtester/internal/simexecution/ohlc.go`, `v3/backtester/internal/simexecution/ohlc_test.go`. No dataset/spec/identity/parser/SDK/CLI ni tests anteriores. Conservar archivos heredados fuera de scope; usar nuevos helpers pequeños para reducir delta.

**Integración serial Root/despacho posterior:** `v3/backtester/cmd/echo-backtest/main.go`, `v3/backtester/cmd/echo-backtest/run.go` y nuevos `v3/backtester/cmd/echo-backtest/ohlc_test.go` sólo si CLI necesita source selection/record timestamp adaptado. `openCorpus` y sequenceSource actuales conocen Candidate; deben soportar SourceBar con los getters B. `reproduce` usa el mismo reader y logical corpus; no un segundo parser ni branch engine. ResultSpec/model fields ya viajan en los structs; si un artifact schema requiere otro archivo, Root amplía PLAN expresamente antes del cambio.

B y C pueden escribir en worktrees separados tras compartir la capsule congelada; C depende de los tipos B para compilar, por lo que las pruebas integradas finales esperan el commit B. No resolver la dependencia duplicando tipos o dando permiso a C para editar spec.go. Se admite probar C en una copia externa con el commit B verificado; no merge/cherry-pick/master mutation sin nuevo mandato.

SDK bars/analytics del407, S2, GerardMM, Operation, Provider, accounting y todos los tests existentes quedan PROHIBITED. Si una imposibilidad real exige seam SDK, C devuelve evidencia y Root congela ampliación mínima con refresh/intersección D6; no modificar ese runtime preventivamente. Ningún archivo D6/AddOn/bridge/accounts/ETCD/deploy/seeds ni sync está permitido.

## Verificación mínima necesaria antes del primer run

- B: bytes NT reales de un contrato→normalized digest/count/interval/ref, DST ambiguo, malformed OHLC/volumen, duplicate/conflict, selección errónea y layouts/chunkings con misma identidad; modo/costos/clock policy digests sensibles, legacy identity byte-equal en proceso fresco.
- C: instante igual close→Signal→ACK→nextOpen; modificar High/Low/Close de minuto futuro no altera prefix previo al end; accepting cursor/triggerbar nunca fill; SourceBar availability y gap bloquean sin mutación/evaluación; bars5m/H4 exactos y regla eligibleH4 compartida.
- Venue/runtime: SL-first con exposición estable; entryOpen+stop en entrybar; long/short stop gap; fee una vez; pinned physical contract y old/new roll gap sin PnL falso; dynamic add/stop/TP ambiguo falla antes de efectos y sin fake quotes; control/day/session boundary ambiguo diagnóstico; protective match aun Strategy not-ready.
- Port E2E: S2 real→GerardMM real→Operation→Provider→venue→ExecutionFill/accounting/finality/artifact, con snapshot explícito y datos reales. Tests sintéticos sólo prueban contratos, no certificación histórica. Dos procesos frescos sobre inputs/build iguales dan records/outcomes/input digest iguales; stdout/timing/path no forman identidad.
- Preservar regresiones SDK del407 y backtester S04; ampliar suite sólo si el delta/fallos lo justifican. Tests nuevos con aserciones de invariantes, sin editar oráculos previos;95% de lógica nueva alcanzable con denominador explícito, no broad package legacy promedio. go vet/race/coverage específicos y CLI build offline/namespace de red vacío; staticcheck si disponible, ausencia documentada sin instalar.
- Run real: SHA originales/manifest/config/RunSpec/build, coverage/gaps, warming counts, per-contract sources, model disclosure, first error/outcome, records/runtime/memory/artifact size y reproduction. COMPLETE sólo después del dominio real ejercido, sin claim tick-true/LIVE parity/campaign economics ni FIXED_WITH_REAL_RERUN por mera suite verde.

## Límites y contradicciones

### Evidencia del shot y cierre

Revisión estática enfocada de los authorities y source exact407: dataset/spec/identity, driver root ordering/timers/market pipeline/warmup/readiness, compose/account/provider/calendar, venue matching y mark/MarketContext. No código/probe de producto creado y no suite ejecutada: el outcome es una cápsula de diseño/readiness; correr fixtures previas no aportaría evidencia del port aún inexistente. Baseline source observado limpio antes y después. Probes nuevos/practical reusable assets: NONE; no producto/harness promovido.

ONE-SHOT cerrado por mandato, Root permanece abierto. Agent-run registra el segmento material de evaluación de código, no performance de implementación. Model identifier exacto no expuesto de forma verificable a este worker: `agent_model=unknown`, `model_source=unknown`; no se infiere a partir del rol TOP. `SESSION_FEEDBACK=NONE`, `REUSABLE_BEHAVIOR_CANDIDATES=NONE`, `PRO_CHAT_POOL_DELTA=0` (Codex LOCAL, sin consumo Chat Pro). Persistencia por delta en este artifact/run/log; sin L0/L1/transcript placeholder ni checkpoint duplicado. Próximo paso Root: congelar SDD B/C, recuperar o acordar snapshot faltante, esperar adquisición y ejecutar los gates/real slice con evidencia.
