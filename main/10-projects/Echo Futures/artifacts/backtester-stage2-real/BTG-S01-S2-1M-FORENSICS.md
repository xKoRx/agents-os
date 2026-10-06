---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[Echo Futures — BT-S01 Backtester V1 Design]]"
  - "[[Echo Futures — BT-S04 Final Remediation and Certification]]"
  - "[[Echo Futures — D4-B1 Q12 S2 Exact Strategy]]"
  - "[[Echo Futures — D4-B2 Q13 Gerard Hardscalping MoneyManagement]]"
  - "[[BTG-PLAN]]"
  - "[[BTG-S01-SUBMANAGER-PROMPT]]"
  - "[[BTG-S01-OWNER-S2-BARS-AUTHORITY]]"
last_verified: "2026-10-06"
confidence: verified
aliases: []
tags:
  - kind/resource
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-S2-1M-FORENSICS

## Síntesis vigente

**SOURCE FACT:** Backtester V1 certificado `cd451972b242c8933321e03001decd4b6d778c61` reutiliza S2, GerardMM, Operation, Provider, calendar, bars y accounting. No acepta velas OHLC como causa histórica. El dataset sólo entrega `MarketCandidateEnvelope`; analytics sólo agrega TRADE canónico; SimExecution ejecuta MARKET/STOP_MARKET sobre un cursor posterior del contrato con lado ejecutable. Un importador CSV por sí solo no implementa el mandato nuevo.

**OWNER AUTHORITY 2026-10-06** ([[BTG-S01-OWNER-S2-BARS-AUTHORITY]], leído desde rama de evidencia del Manager): baseline S2 actual + GerardMM actual, NQ Last 1m real, sin cambiar rentabilidad ni optimizar. En una misma vela que toca SL y TP, SL primero. La identidad “Gerard” queda resuelta por elección explícita de S2; no reasignar a S1. Las barras solicitadas abarcan 2023-10-01..2026-10-06 y expiries físicos 12-23, 03/06/09/12-24, 03/06/09/12-25, 03/06/09-26 y 12-26 current. Descarga visible/MergeNonBackAdjusted son evidencia Owner de configuración, todavía no bytes exportados ni cobertura certificada. Ticks NQ03-26 2026-01-02..2026-03-20 confirmados por Owner no demuestran un año completo.

**TECHNICAL PROPOSAL, READY_FOR_MANAGER_REVIEW:** añadir causa OHLC explícita al mismo driver y una entrada de source-bar al builder/analytics compartido; agregar directamente 1m a cada timeframe requerido; ofrecer ejecución modelada por vela en la misma SimExecution, con los mismos hechos y ledger. No convertir O/H/L/C en `CanonicalMarketEvent` ni fabricar QUOTE. El alcance nuevo es input/fidelidad; no es un defecto probado en S2 ni autorización para cambiar sus reglas. No hay implementación ni corrida real en este artifact.

**DECISION NEEDED:** SL-first no determina qué sucede cuando adds adversos/favorables y stops/objetivo dinámicos cambian dentro del mismo minuto. No existe contrato que autorice escoger O-L-H-C u O-H-L-C y llamarlo globalmente pesimista. Primer port implementable puede fallar de forma nombrada antes de mutar ese minuto (`OHLC_PATH_AMBIGUOUS`) y preservar diagnóstico; continuar un run completo con esos minutos requiere una política de ejecución intrabar acordada, no desactivar scaling ni inventar ticks.

## Evidencia y provenance

### Baselines refrescados y frontera

- Repo `xKoRx/echo`, certificado local limpio: `cd451972b242c8933321e03001decd4b6d778c61`.
- `origin/master`: `372af59a7b83604781346613da01e3d510ea1360`.
- `origin/feature/d6-shot1-execution-vertical`: `d08a30ce9815f820fda7132e20dc42cc345eb8e8`.
- Repo `xKoRx/agents-os`, master: `07ea74689eeb56988653cce61cc836be32c0effe`.
- Refresh vía `git ls-remote`, 2026-10-06. Ningún cambio de producto, deploy, D6 activo, AddOn, bridge, perfil, trading o infraestructura. Antes de implementar archivos SDK compartidos, refrescar D6 y comparar exclusivamente intersección de AllowedFiles; no tocar su worktree.
- Instrucciones leídas: AGENTS OS bootstrap/constitución/router Aranea/Environment Contract; Echo `AGENTS.md`, `CONSTITUTION.md`, reglas tooling, independencia y anti-test-masking; technical-project-manager. Rol de este shot: worker forensics, sin subdelegación.

### Seams comprobados desde source certificado

| Dueño / fuente relativa a `xKoRx/echo` | Hecho relevante |
|---|---|
| `v3/backtester/dataset.go:43` | `HistoricalRecord` contiene sólo candidate canónico, source ref/order y quote evidence. Ningún OHLC ni intervalo de vela. |
| `v3/backtester/internal/datasets/ndjson/ndjson.go:589` | Adapter decodifica TRADE/QUOTE. Identidad y selección validadas; representación/receipt no sustituyen identidad lógica. |
| `v3/sdk/futures/analytics/engine.go:129` | `Input` contiene canonical event, timers/readiness/calendario; no ingesta de closed source-bar. `feedBuilders` llama `Builder.ApplyTrade`. |
| `v3/sdk/futures/bars/builder.go:132` | Builder compartido exige TRADE, SessionGrid y epoch. Timer cierra sin nuevo tick; no fabrica barras vacías; correction es proyección y nunca reevaluación. |
| `v3/sdk/futures/bars/grid.go:10` | Regiones ancladas a apertura de sesión, `[open,close)`, breaks no reinician grid, early close trunca. No agrupar por UTC `floor(4h)` ni usar plantilla NT como autoridad implícita. |
| `v3/sdk/futures/bars/bar.go:29` | BarRecord cuenta trades y source stream seq canónicos. No escribir un ordinal de vela como stream seq ni inventar trade count. Provenance sólo LIVE/REBUILD: source-bar necesita metadata diferenciada/versionada. |
| `v3/backtester/driver.go:173` | Igual timestamp ordena boundary fase3 → mercado fase4 → timer fase5. Un Open de minuto siguiente sin batch especial se consume antes del Signal de cierre5m. |
| `v3/backtester/driver.go:475` | Pipeline compartido: admitir/proyectar → analytics → matching → marks/fills → reconciliar → decisiones → drain. Ninguna decisión anticipa datos de root futuro. |
| `v3/backtester/internal/simexecution/venue.go:288` | Orden no ejecuta en cursor aceptante. Market requiere quote válido; stop cruza last del propio contrato y llena al lado ejecutable, con gap/slippage. No TP limit ni native modify. |
| `v3/backtester/spec.go:211`, `run.go:614` | `TRADE_MODEL` ya declara offsets bid/ask alrededor de Last, slippage fijo, fees; no fabrica canonical QUOTE. OHLC necesita modo/provenance propios, reutilizando matemática de lados y fees. |
| `v3/backtester/driver.go:938` | En TRADE_MODEL no se entrega QuoteUpdate canónico. Economía/valuation entran por las rutas compartidas; no llamar a MM como atajo. |
| `v3/backtester/compose_account.go:31`, `compose.go:557` | Se instancian `config.NewGerardMM` real y `s2.New`; no estrategia/MM alternativos de backtest. |

### S2 exacta: config y causalidad

| Campo | Autoridad reusable actual |
|---|---|
| module/spec | `config.ModuleS2` / `S2_H4_TREND_BB_PULLBACK_V1` |
| instrument | NQ estructural; no modificar |
| timeframes | 4h trend + 5m entry; barra TRADE conceptual OHLC Last de fuente real |
| trend_ma_period | default source/D4-B1 = 50 |
| bollinger_period | default = 20 |
| bollinger_deviation | default = 2.0; stddev POPULATION |
| stop_buffer_ticks | default = 1; source convierte cero a default1, por tanto cero en JSON no demuestra buffer cero |
| trend_lookback / entry_lookback | default64; H4 exige al menos trendPeriod+1 |
| tick_size | requerido, positivo, del ContractSnapshot validado; no default en S2 |
| stream_id | envelope físico `NQ:<contract_id>`; si parámetro ausente toma envelope; mismatch falla |
| config identity/version/digest + binding/account/provider/calendario | caller/config snapshot explícitos; no defaults inferidos de fixtures |

`v3/sdk/futures/strategies/s2/s2.go:148` resuelve defaults sin cambiar params congelados. EVALUATE sólo en BAR_CLOSE; H4 absorbe y no emite Signal. 5m incluye su propio close en Bollinger. Trend usa H4 más reciente cuyo `CloseBoundary <= entryBar.BucketOpen` (`eligibleTrend`), no el H4 que recién cierra con ese 5m. Ejemplo 11:55→12:00 no usa H4 cerrado12:00; 12:00→12:05 sí. El comentario inicial source dice algo contradictorio sobre igualdad al open, pero implementación y D4-B1 §7.3 coinciden; no corregir lógica por ese comentario.

Warmup real: 51 H4 cerradas y 20 5m cerradas bajo defaults, `Warmup=true`, cero Signals/ciclo abierto. Driver sólo prueba recepción mínima y S2 conserva su readiness exacta. Se reporta prefijo faltante de inicio2023-10-01; no inventar closes para cubrirlo. La basis es cierre técnico del ciclo y nunca TP económico. Strategy emite MARKET después del cierre aceptado; D4-B1 §10 no fija fill al precio Close.

### GerardMM y config pendiente

`v3/sdk/futures/gerardmm/config.go` y `v3/sdk/futures/config/mm.go` reutilizan `GerardMMDef{Currency,Plans,Scaling}` y `MMConfigPerStrategy`: `economic_stage`, `trading_business_day_ordinal`, `funded_mode`, `account_currency`. Plans exige row set; no plan built-in. EVALUATION días1/2 Owner: SL USD2000, TP USD1500. Día3+ y FUNDED sólo habilitan riesgo si existen rows/config explícitas; no repetir día1 automáticamente ni tomar números de tests. Scaling nil bloquea adds; LIVE requiere scaling explícito. `ResearchScaling()` es seed declarado (0.25R/2/1.0 adverso, 0.50R/1/0.5 favorable), no baseline actual autorizado.

Root comunicó inventario previo: ETCD Futures enabled/snapshot ausentes y CoreDEV sin Futures; no duplicamos infraestructura. Config actual runtime no está físicamente demostrada. Para este baseline S2 se puede materializar defaults D4-B1/source como configuración declarada con digest; aún deben obtenerse o decidirse Currency/plan rows/scaling, account stage/day selector, ContractSnapshot, Provider rules/limits/terms y calendario real. Preguntar sólo por los campos realmente faltantes después del inventario; no usar `Generic20BusinessDaysSpec`, seeds o GAU50 fixtures como autoridad instalada.

### Timestamp NT y reconstrucción

**INPUT CONTRACT REQUIRED:** export NT barras por contrato, sin ajustes, Last1m; comprobar bytes, SHA256, columns, timezone/IANA o UTC, formato y versión/export method, plantilla de sesión aplicada y política MergeNonBackAdjusted. El end timestamp de NT se interpreta como final de intervalo sólo tras comprobar el export concreto. `bar_start = end - 1m` bajo vela normal; partial/truncation necesita intervalo comprobado. Horas repetidas DST sin offset/tz desambiguable fallan, no se adivinan. Mantener `[start,end)` como intervalo de precios y `available_at=end` como conocimiento HLC completo.

Cada 1m completa alimenta directamente ambas demandas 5m y4h mediante SessionGrid; `open=first.open`, `high=max(high)`, `low=min(low)`, `close=last.close`, volumen=sum real. No cascada5m→H4, ni pseudo trades, ni quote inventado. Rechazar 1m que cruza una región de calendario sin resolución real; nunca distribuir High/Low de un intervalo entre regiones por conveniencia. Missing-minute dentro de sesión esperada genera gap reportado y bloquea readiness/decisión del agregado afectado; no ffill ni empty-bars. Gaps de mercado cerrado se clasifican por calendario y no como pérdida. Source refs, intervalos y digest de contribuciones viven en provenance explícita; no inventar canonic stream sequence/trade count. Repeated identical sourcebar id es no-op; diferente payload mismo id falla. Slice SDK inicial acepta fuente OHLC inmutable y ordenada; correcciones/reemplazos OHLC sobre agregado ya cerrado se rechazan explícitamente. Corrections TRADE heredadas siguen projection-only, sin reevaluación.

### Ejecución OHLC mínima y límite honesto

1. Batch de frontera cerrado: source1m termina → commit agregado compartido → BAR_CLOSE5m/H4 y Signal → admission/MM/Provider/ACK/drain → ofrecer Open de siguiente sourcebar como cursor posterior del mismo contrato. Ordenar por ordinal causal, aunque cierre y siguiente apertura tengan misma UTC; versión de modo OHLC entra en RunSpec/input digest. Preservar fase/ordering actual para datasets TRADE/BBO.
2. MARKET aceptado desde trigger5m no usa O/H/L/C de esa trigger bar. Próximo Open observado de una vela posterior negociable del contrato propio es fill modelado con lados/offsets/slippage explícitos. No garantiza fill si Signal expira durante gap, sesión cerrada, falta contrato o cutoff. Entrybar means la vela posterior que contiene el fill; ahí sí se pueden evaluar SL/TP posteriores al fill bajo la política modelada, nunca retroactivamente en trigger bar.
3. Protección resting física se procesa aun si Strategy no está ready. Si sourcebar posterior para exposición estable toca SL y objetivo monetario actual, resolver SL antes del profit exit por regla Owner; TP es dinámica account-wide de GerardMM, no una LIMIT ni basis S2. Stop gap usa Open adverso/lado ejecutable y costos; no regalar fill al precio stop. Hechos salen por `SealedEvent`, `ExecutionFill`, `ExecutionUpdate`, reconciliación/finality y accounting reales.
4. Decisiones MM nunca se recalculan con información futura del minuto antes de su cierre. Bar completo sólo se conoce en end; cualquier ubicación de ejecución dentro del intervalo es modelada, no observada. Registrar `[start,end)`, timestamp de settlement y policy version. No retroceder reloj ni enmascarar cruces de account-day/Provider/session boundaries; intervalo no separable con datos reales o cuya atribución económica cambia outcome exige diagnóstico nombrado antes de commit.
5. Si un add, cambio de stop, profit objective o rama favorable/adversa permite órdenes de eventos que difieren económicamente dentro de1m, no usar “adverse first” como teorema de menor PnL. Un add puede acercar TP y mover stop, por lo que las trayectorias extremales no dominan globalmente. Candidato inicial fail-closed para esos intervalos (`OHLC_PATH_AMBIGUOUS`), con capsule de vela/Operation/config/thresholds y estado previo. Una política de trayectoria acordada permite un resultado de modelo específico; no certifica tick-true, fills exactos LIVE ni bound económico universal.

### Rollover físico

Reutilizar ContractCatalog, ContractSchedule, prepare/warmup candidato, `DRAIN_CYCLE`, selección y pins. Cada contrato conserva stream, barras, calendar, quote/model mark y ledger propios; el cambio seleccionado no transfiere posición ni ajusta entry price. La marca de contrato nuevo no valoriza posición vieja. Consumir old-contract hasta resolver inventory/protecciones/finality; falta datos produce `OLD_CONTRACT_DATA_UNAVAILABLE`, sin flat sintético. NQ price gap de rollover no se traduce a PnL por simple cambio de seleccionado. Corpus MergeNonBackAdjusted no prueba que cada archivo sea realmente expiry-only; inspeccionar solapamientos/export y rechazar continuidad ajustada que se etiqueta física.

### Capsule SDK aislada — lista para despacho NORMAL ahora

**STATUS: READY_FOR_LOCAL_IMPLEMENTATION.** Se puede implementar y verificar este slice sin bytes NT, sin configuración MM y sin decidir trayectoria de ejecución. Produce el seam SDK y sus regresiones, todavía no un backtest OHLC. Manager puede congelar esta capsule técnica como tarea ordinaria dentro de la autoridad Owner de reconstruir5m/H4; no pedir otra decisión de producto para tipos/validación/aggregación compartida.

**Ownership exclusivo SDK. AllowedFiles EXACTOS:** nuevos `v3/sdk/futures/bars/source_bar.go`, `v3/sdk/futures/bars/source_bar_test.go`, `v3/sdk/futures/analytics/source_bar_test.go`; modificar únicamente `v3/sdk/futures/bars/bar.go` y `v3/sdk/futures/analytics/engine.go`. El método `(*Builder).ApplySourceBar` vive en source_bar.go y usa Builder/Grid/Ring existentes; no editar builder.go. No modificar config, strategy, s2, gerardmm, operation, provider, accounting, runtime shells, Driver, dataset parser o venue. Sin nuevo módulo/framework. D6 refresh/diff de estos dos archivos compartidos antes de primer edit.

**Contrato mínimo del source type:** identidad stream física y `SourceBarID`, `SourceRecordRef`, ordinal de fuente y digest tipado; `IntervalStart`, `IntervalEnd`, `AvailableAt`; OHLC exactos units.Price y Volume real. Intervalo1m completo `[start,end)`; AvailableAt>=end y analytics.Now>=AvailableAt, ningún HLC conocido antes. O/C dentro [L,H], prices positivos, volume>=0, identidad stream/contract coherente. Builder no tiene tick table: validación de tick múltiplo pertenece al caller/ContractSnapshot futuro, nunca default inventado aquí.

**Procedimiento cerrado:** `analytics.Input.SourceBar` se valida como causa única; mismo stream owner. Resolver calendar/grid en start (no end que ya pertenece a región posterior); intervalo debe caber completo en una sola región del timeframe. Mode/source kind se fencea por builder al primer input; mezclar TRADE y fuenteOHLC bajo la misma authority falla de forma nombrada. Recorrer `sortedTimeframes`, agregar cada1m a cada builder por first.open/maxH/minL/last.close/sumvolume y misma grid; se preservan ring, BarID, closure, subscribers y EffectBarsSnapshot/ForwardBarClosed existentes. Nunca emitir ForwardCanonicalTrade/QuoteNotification por esta entrada. No cascadear5m→H4.

**Provenance mínima:** extender BarRecord con evidencia de fuenteOHLC diferenciada y optional fields para ordinal/digest/contribuciones, y BuildProvenance explícita de sourcebar. No completar OpenSeq/CloseSeq/SourceUptoStreamSeq/TradeCount con número inventado; son unavailable con source-kind visible. Version de barraOHLC incluye digest/ordinal real de fuente; Version y JSON del pathTRADE siguen exactamente iguales cuando campos nuevos omitidos. No reutilizar labels LIVE/REBUILD para hacer pasar la fuente agregada por canonic ticks.

**Orden de cierre/caller:** sourcebar terminada en frontera debe aplicarse antes de disparar BarCloseTimer de ese builder; asegura que último close/high/low están committed. SDK no adelanta su propia clock ni cambia fases del driver. Si caller ya cerró el agregado y luego intenta agregar esa fuente, rechazar explícitamente; no reabrir/reemitir decisión. Natural close por sourcebar de región posterior conserva semantics del builder. Timers/calendar boundaries reutilizan paths existentes. Partial1m que cruza región/corte o llega antes de available_at falla; no repartir extremos ni crear emptybars.

**Admisión sourcebar:** fuente inmutable y ordenada por stream. Guard separado de canonical stream sequence: redelivery idéntica no agrega volumen/ordinal y diferente payload del mismo id/ordinal es conflicto. Out-of-order, overlap y replacement/correction OHLC no soportados por este slice fallan nombrados; no skip silencioso. El guard debe ser acotado y determinista, suficiente para idempotencia del orden estricto sin retener corpus completo. TRADE redelivery/correction/epoch behavior permanece intacto.

**Regresiones nuevas necesarias de este slice:** (1) 5×1m OHLCV→5m exacta; 240×1m→H4 exacta directamente y sin5m intermediate; (2) sourcebar end en frontera dentro región anterior, cierre timer con última1m committed; (3) SessionGrid open/DST/break/earlyclose,1m crossing rechazo; (4) AvailableAt/Now prematuros rechazo; (5) duplicate identical no-op/conflict/overlap/out-of-order nombrados; (6) mezclaTRADE/OHLC rechazada, provenance/version no falsifica canonic trades; (7) mismos Effects/BarID/subscriber y ring lookback bounded; (8) missing1m no ffill/emptybar, completeness/source coverage visible para que caller decida readiness y gaps; (9) TRADE paquetes bars/analytics actuales verdes, snapshots/Version iguales; (10) sourcebar rejected after closure no second BAR_CLOSED. No afirmar S2/fill/Provider parity con estos tests aislados.

**Gate de salida:** source seam y pruebas nuevas PASS, targets SDK sin seeds/red; code SHA y diff exactos; Manager recibe firmas y ejemplo de composición para siguiente driver slice. No autoaceptar corpus, políticas MM ni primer real run. Coverage nuevo ≥95% con caminos críticos primero. Pruebas existentes sólo se ejecutan, no se editan.

### Ownership y AllowedFiles para siguientes implementers LOCAL

No se autoriza código en este shot. Lista candidata a congelar por Manager con ownership exclusivo; preferir archivos nuevos para el seam y conservar métodos anteriores. Cualquier archivo extra exige evidencia del primer seam real, no refactor general.

| Workstream | AllowedFiles candidate | Tarea verificable |
|---|---|---|
| A — sourcebar/shared bars | nuevos `v3/sdk/futures/bars/source_bar.go`, `source_bar_test.go`; `bars/bar.go`; `v3/sdk/futures/analytics/engine.go`; nuevo `analytics/source_bar_test.go` | Tipo validado de intervalo OHLC cerrado, provenance/version diferente de canonic trade; método Builder que agrega1m a cada demanda; entrada analytics que produce mismos snapshots/BarClosed effects y timers/grid/correction semantics. No tocar S2/gerardmm. |
| B — dataset + run contract | `v3/backtester/dataset.go`, `spec.go`; nuevos `internal/datasets/ntbars/*.go`; `cmd/echo-backtest/run.go`, `reproduce.go` sólo selección del reader | Discriminante sourcebar vs candidate; importar bytes con timestamps/contratos/gaps/selection/digests; rechazar mixed identity y formato ambiguo; modelo/version/costos explícitos reproducibles. |
| C — driver + execution | `v3/backtester/driver.go`, `run.go`, `projection.go`; nuevos `bar_driver.go`, `bar_driver_test.go`, `internal/simexecution/bar.go`, `bar_test.go`; `internal/simexecution/venue.go` sólo seam imprescindible de eligibility/facts | Batch cierre→Signal→posteriorOpen, modelo SL-first y diagnóstico ambigüedad; marks y economics modelados por seam actual; mismas observaciones/finality/ledger/caps. Ledger y MM no poseen política OHLC. |
| D — evidence/integration owner | nuevos `v3/backtester/btg_s01_bars_e2e_test.go`; `result.go`, `reproduce.go` sólo si identity/resolved model/provenance no se serializan completos; docs acotadas del FEAT vigente | Misma corrida/raw bytes/config reproduce digests; residual/gaps/límite declarado; run real sólo tras corpus y config, smoke→horizon disponible sin campaign. |

B posee spec/dataset y C los consume; A posee SDK y C lo consume; acordar firmas mínimas antes de editar, sin writes concurrentes en un archivo. D independiente QA no modifica production code y usa archivos nuevos. Tests existentes intocables salvo TEST_CHANGE_REQUEST aprobado. No tocar Core shell/D6/bridge/AddOns/ETCD/PG/seed tests. Una tarea con dos rutas de mercado conserva un mismo Operation/MM/Provider/accounting; no otro engine.

### Regresiones críticas nuevas requeridas

| ID candidate | Oráculo |
|---|---|
| BAR-01 | NT end timestamp09:31 pertenece a09:30..09:31; boundaries5m/H4 correctas, DST repetido no se adivina. |
| BAR-02 | Cinco barras1m reconstruyen OHLCV5m exacto; H4 directamente desde1m exacta; template de sesión/break/earlyclose gobierna grid. |
| BAR-03 | Cambiar H/L/C de minuto futuro no cambia Signal ya emitido ni fills previos; H4 misma frontera no visible hasta siguiente5m conforme D4-B1. |
| BAR-04 | Missing-minute dentro de sesión invalida agregado/readiness y queda en gap evidence; cierre de mercado no genera barras/gaps falsos; EOF incompleto no COMPLETE. |
| BAR-05 | Duplicate sourcebar no suma volume; mismoID distintoOHLC falla; correction no reevalúa Signal. Provenance no falsifica trade count/stream seq. |
| BAR-06 | Signal5m@t→ACK→Open siguiente1m@t posterior ordinal; fill exactamente próximo Open propio, nunca Close/High/Low de trigger ni minuto subsiguiente accidental. |
| BAR-07 | LONG ySHORT: same-entrybar/posteriorbar toca SL+TP→SLfirst; stop gap llena lado ejecutableOpen más slippage; economics fee exacto una vez. |
| BAR-08 | Adds adversos/favorables + stop/TP dinámicos ambiguos cortan antes de mutación con capsule reproducible; no reducir qty, no quitar scaling, no dobleclose ni liberar claim antesfinality. |
| BAR-09 | Calendar/provider/account-day boundary no produce hechos retrodatados; intervalo incompatible o atribución ambigua fail-visible. |
| BAR-10 | Rollover dos contratos con gran gap, old position/stop conservados, cero PnL por cambio de seleccionado, olddata faltante falla y prepared context de nuevo contrato aislado. |
| BAR-11 | Modelo/costos/ordered bar refs/coverage alterados cambian input identity; misma fuente/config reproduce señales/fills/economics/digest; reader chunks sólo cambia receipt. |
| BAR-12 | S2 defaults y params explicit iguales producen mismos Signals; warmup real cero entradas; día3/funded/scaling ausente conservan fail-closed; sin campaña ni sweep de objetivos. |

### Verificación ejecutada

Sólo paquetes/regex explícitos, en network namespace aislado, `GOPROXY=off GOSUMDB=off`, sin seeds. `go test -count=1`:

- `v3/backtester/internal/simexecution`: `TestMarketBuyFillsNextCursorAtAskPlusSlip`, `TestAcceptingCursorNeverFills`, `TestStopGapFillsAtExecutableSide`, `TestStopWaitsForQuoteAfterTrigger` — PASS.
- `v3/sdk/futures/strategies/s2`: `TestS2_S203_SameBoundaryH4Visibility`, `TestS2_S201_Warmup`, `TestS2_A11_DeterministicReplay_SameOutcome` — PASS.
- `v3/backtester`: `TestRolloverE2E_ThreeContractsOneAccount`, `TestDriver_ExactMoneyAndFeeOnce`, `TestDriver_DayBoundariesDST` — PASS.

Estos diez tests prueban seams heredados, no aceptación OHLC. No test nuevo ni fuente modificada; no run contra bytes NT, no métricas históricas calculadas, no gate Owner autocerrado. BAR-01..12 son obligaciones futuras, no PASS.

## Límites y contradicciones

- BLOCKER INPUT: dataset worker comunicó `NQ1m NOT_ACQUIRED`: CUsersKoR raíz legible, Documents/db/minute ACL denied; Owner desconoce ruta. ExportGUI mínimo sigue pendiente del workstream autorizado; no ampliar ACL/perfil ni asumir fixture. Este dato es handoff del Manager, no inspección física de este shot.
- BLOCKER CONFIG: scaling exacto, rows día3/funded, Provider/account/costs/calendario aún deben fijarse por autoridad; source defaults S2 sí reusable. Esto limita certificación longitudinal y funded, no exige otro diseño general.
- MODEL LIMIT: OHLC no establece secuencia de cruces ni cadence BBO. SLfirst confirmado, adds/stop moves todavía no resueltos por esa sola regla. Una ambigüedad diagnosticada no es bug S2 ni permiso para ajustar rentabilidad.
- FUTURE TASK: materializar port nativo y ejecutar primero smoke real con identidad/config selladas; comparar primerdivergence y reparar únicamente dueño probado, rerun mismo histórico. Sin optimizer/campaign.
- REUSABLE CANDIDATES: timestamp=end separa intervalo de disponibilidad; causal ordinal distingue cierre y apertura mismaUTC; fuente agregada nunca se etiqueta canonical ticks; roll físico nunca repricing implícito. Quedan en este artifact; no nueva memoria pública duplicada.
- RUN REGISTER: review/source forensics + tests registrados; feedback NONE (ninguna fricción de Sistema1 demostrada); transcript/L0/L1 no creados; cierre explícito por mandato del Manager. Pro delta0: este shot usó sólo LOCAL, cero CLOUD Pro-pool.
