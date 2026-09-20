---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[Polymarket Engine — MVP]]"
sprint:
start: 2026-09-20
due:
progress: 0
repo: "https://github.com/xKoRx/polymarket-engine"
jira:
prs:
aliases:
  - PE-004
  - New Market Maturation
  - Sports-independent market maturation
  - POC-S05
tags:
  - kind/project
  - area/personal
  - domain/trading
  - tech/polymarket
  - topic/prediction-markets
created: 2026-09-20
updated: 2026-09-20
---

# POC-S05 — New Market Maturation

> [!info]+ PE-004 · planificación canónica
> **Padre:** [[Polymarket Engine — MVP]] · **Estado:** PLAN_DOCUMENTED / LOCAL_GATE_PENDING · **Prioridad:** P1 · **Hipótesis:** PE-004 · **Progreso implementación:** 0%. Esta nota, no un handoff externo ni el chat, es el único planner del subproyecto. Ningún gate de implementación está aprobado por el solo hecho de haber redactado la SPEC.

## 🎯 Objetivo

Diseñar, implementar y certificar una POC **descriptiva y causal**, read-only y sin órdenes, que mida la maduración observada de mercados de Polymarket desde una ancla explícita y conocible: cambios en spread, profundidad, impacto y actividad durante **1 minuto, 5 minutos y 1 hora**. Contrastar contra cohortes comparables y controles negativos PE-019 (display-price switching) y PE-020 (bid-ask bounce). Determinar si existe un patrón reproducible antes de formular una estrategia económica de trading. El descenso del spread NO equivale a beneficio ejecutable ni justifica BUY/SELL. No implementar producción, LIVE ni un predictor direccional en esta POC.

**Entregables:** contrato venue y temporal verificable; cohorte y denominadores no sesgados; ingestión lifecycle observada sin inventar historia; snapshots as-of de profundidad; observador Strategy+Factory; 20 fixtures nativas deterministas; SCREEN/REPLAY/SHADOW de observación en dataset aislado; scorecard y resultados con censura; gates, tests, recibos y decisión de investigación separada del permiso live. La captura empírica y validación OOS son fases posteriores, nunca resultados inventados.

## 📊 Estado actual

- **20-09-2026, esta nota:** proyecto y plan documental creados sobre `xKoRx/agents-os@master` tras comprobar que la ruta exacta no existía en el árbol remoto. **No se verificó el checkout local de Agents-OS, sus escritores, la indexación Graphify ni el estado actual de RS v0.3.** Reconciliar cambios locales antes de tocar el mismo archivo; no reset/rebase/overwrite de trabajo ajeno.
- **Engine remoto AUDITADO, no ejecutado:** `xKoRx/polymarket-engine@main` commit `9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5` (`9ae5dde`); no implica HEAD local ni build verde. `7bd264d` es baseline histórico, no HEAD. El M4 no-live certificado en el padre NO certifica PE-004. Comprobar HEAD, tests, flags, cambios pendientes y data-dir real en A0.
- **Venue:** Market AsyncAPI oficial documenta `event_type=new_market` y opt-in `custom_feature_enabled:true`; `id` = Gamma market ID, `market` = condition ID, `assets_ids` = IDs de tokens, `event_message.id` = parent Event ID, `timestamp` = epoch-ms del aviso. No demuestra suscripción global, entrega completa, hora de publicación, primer trade o creación on-chain. No hay 7 casos reales capturados ni historial L2 completo verificado: `REAL_DATA_READY=NO`.
- **Transporte existente:** `internal/transport/marketws/marketws.go::connectRaw` ya envía opt-in + initial_dump; `cmd/engine/record.go::framesSink.onFrame` captura todo raw recibido mediante ACK durable con ConnectionID/Epoch. No agregar collector independiente. `internal/protocol/marketws.go::ParseMarketWSEvent` conoce `new_market` pero solo guarda Raw (`Documented=false`); no objeto lifecycle tipado. `catalog.Reducer.applyRecord` solo proyecta Gamma: aviso WS aún no aparece en Catalog. Books y Regimes omiten lifecycle WS.
- **Datos existentes reutilizables:** `catalog.InspectEntity` expone `FirstKnownAt` y revisions `KnownAt/SourceAt/CaptureRef`; `catalog.MarketContent.Dates` preserva `createdAt/updatedAt` como dato reportado, no como ancla de primera observación; Books respeta full snapshot, epoch y gap. `catalog.UniverseSpec.Events` está declarado pero `collectMembers` no lo filtra: prohibido usarlo como event-scope hasta corregirlo.
- **Gaps de integración confirmados remotamente:** `frames.AssetSnapshot` contiene BBO y `Levels` (conteo), **no profundidad precio×size** ni lifecycle as-of; `cmd/engine/screen.go` y `experiment.RunShadow` están acoplados a `fixture-neutral`, hacen cortes después de recorrer todo el journal y usan simplificaciones distintas del reducer Books. SHADOW inventa profundidad 10 por lado y no resuelve fees: no es evidencia de PnL PE-004. `replay.RunObservation` verifica manifest/books, pero no ejecuta Strategy ni scorecard PE-004. `replayRegimesReducer.digest()` vacío no demuestra equivalencia de estado Regimes.
- **Safety de datos:** `screen` y `RunShadow` hacen `capture.Open` (puede escribir boot/recovery); **NUNCA apuntarlos a RS v0.3 o al data-dir activo**. Usar una copia descartable pinneada y verificada. `capture.OpenView` para lecturas auténticamente read-only cuando aplique.
- **Estado honesto:** `SPEC_v1=DOCUMENTED_PENDING_LOCAL_FREEZE`, `FIXTURES=20_DEFINED/0_NATIVE`, `ENGINE_LOCAL_HEAD=UNKNOWN`, `CAPTURE_REAL_CASES=0`, `HYPOTHESIS_VALIDATED=NO`, `LIVE_DISABLED`. No existen pruebas ejecutadas de PE-004 en esta preparación; el coding agent no empieza código hasta G0.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/polymarket-engine` | `main` remoto; branch local exacta **A0 por verificar** | remoto `9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5`; **A0 pin de HEAD local obligatorio** | [SPEC funcional v1](#spec-funcional-v1) | [SPEC técnica v1](#spec-técnica-v1) | DOCUMENTED; NO CODE / LOCAL_FREEZE_PENDING |
| `xKoRx/agents-os` | `master` remoto; checkout local A0 | commit de creación de esta nota verificable en GitHub; local UNKNOWN | esta nota canónica | frontmatter `project` v1 + gates y WPs aquí | planner remoto creado; validar lint/Graphify local |

## 🧩 Subproyectos

Ninguno. PE-019 y PE-020 son controles negativos **dentro de PE-004**, no crear proyectos/estrategias adicionales ni un planner paralelo.

## ✅ Tareas

> [!note]+ Fuente única, ownership y criterio de estado
> Todo WP permanece `[ ]` hasta evidencia física y recibo exacto en esta nota. `[/]` es trabajo empezado; `[r]` revisión; `[x]` evidencia aceptada. Las tareas del agente van aquí (`#owner/agent`); el padre necesita una única tarea puente `#owner/me #type/supervision`, todavía por reconciliar de forma segura con el archivo local enorme. El agente NO la cierra. No estimar `progress` por documentación ajena al código.

- [ ] **A0 · Gate local y SPEC freeze:** verificar estado git/HEAD de ambos repos, writers y S05 único, RS v0.3, capturas y params; contrastar 14 seams auditados con HEAD local, fijar branch/base/allowed files; registrar resultados y congelar SPEC solo si G0–G3 PASS. #owner/agent #type/research #area/personal
- [ ] **A1 · Catalog/temporal:** persistir/coherentemente consultar primera observación, anclas O/B y revisiones as-of; no retroactividad ni false event-scope; F02–F05/F19. #owner/agent #type/dev #area/personal
- [ ] **A2 · WS lifecycle tipado:** parser Protocol de `new_market`, mapping y reconciliación Catalog, idempotencia raw→ACK→replay; mantener flag existente; F01/F03/F04/F05/F08. #owner/agent #type/dev #area/personal
- [ ] **A3 · Books→Frames causal:** first usable two-sided, epoch/reconnect/gap, snapshot profundidad pinneada a cut y refs metadata; F06–F11/F15–F17. #owner/agent #type/dev #area/personal
- [ ] **B1 · Observer/Factory PE-004:** Strategy determinista sin I/O, tres ventanas, cohortes/denominadores, quality/reasons, Candidate=nil; F01–F20. #owner/agent #type/dev #area/personal
- [ ] **B2 · Economía descriptiva e hipotética:** reutilizar Economics real as-of, fee/tick intervalos, depth Q1/5/10 y veto PnL sin salida; F09/F10/F12/F15. #owner/agent #type/dev #area/personal
- [ ] **B3 · Controles y scorecard:** PE-019/020, dedup trade, reason codes, censura, experiment manifest/metrics; F12–F14/F18. #owner/agent #type/dev #area/personal
- [ ] **C1 · SCREEN PE-004 causal:** registry mínimo, forward cut por instante, quality verdadera del reducer y output descriptivo sin orders; F01–F20. #owner/agent #type/dev #area/personal
- [ ] **C2 · REPLAY/SHADOW aislados:** pipeline PE004 en copia descartable con manifest/seed/digest, igualdad de schedules y ningún active boot; F07/F08/F16/F20. #owner/agent #type/dev #area/personal
- [ ] **C3 · Certificación no-live:** 20/20 fixtures, build/vet/test/race, cobertura >=95% por paquete tocado sin exclusiones manipuladas, regresión M4, baseline/manifest/recibos, final owner review; no GO económico inferido. #owner/agent #type/dev #area/personal

## SPEC funcional v1

### Hipótesis y diseño del experimento

**PE-004-A, mecanismo falsable:** entrada asíncrona de participantes, cambios de liquidez/cotización/tick/fees al conocerse un nuevo mercado pueden alterar las distribuciones de spread, depth, impacto y actividad. Estimando primario: cambio de spread cotizado y profundidad ejecutable de cohortes observadas entre t0 y los cortes 60, 300, 3600 s, reportando cobertura y censura. Secundarios: impacto Q, midpoint, first book/trade observado y régimen. Comparar cohortes con controles de categoría/evento/régimen cuando existan suficientes casos, cluster por parent Event; efecto nulo, inverso o explicable por missingness desconfirma generalización. **PE-004-B (trade) BLOQUEADO:** requiere predictor preregistrado ex ante, benchmark conocido antes del corte, acción concreta, salida causal, estudio OOS, fees/impact/slippage/adverse selection/capital y robustez. A no implica B.

**Población:** TODOS los mercados Gamma detectados prospectivamente en periodo preregistrado, incluidos nunca-two-sided, sin trades, inactivos y censurados; no seleccionar por resultado posterior, book futuro, supervivencia o existencia actual de trade. Unidad market + asset, incertidumbre agrupada por parent Event; denominadores separados `N_discovered`, `N_eligible`, `N_book_seen`, `N_usable`, `N_window_complete`, `N_halted`, `N_gap`, `N_missing_trade`. El ranking de horizontes ex post no se usa para seleccionar estrategia. Horizonte de cohortes **individual por market**, nunca reloj global compartido.

**Cohortes:** O=`CATALOG_FIRST_OBSERVED`: `catalog.EntityInspect.FirstKnownAt` de Gamma market, guardado originalmente en captura, v1 canónica. W=`WS_FIRST_NOTICE_OBSERVED` solo luego de A2 con payload validado y recepción durable, segregada de O. B=`FIRST_USABLE_BOOK_OBSERVED` primera dos-sided full+mapping+tick/quality aceptables; es un análisis complementario de liquidez, NO listing. C=`CREATION_KNOWN` permanece BLOCKED hasta semántica certificada de creación/publicación y feed sin lag anterior: `new_market.timestamp`, `Gamma.createdAt`, `startDate` y first seen no son intercambiables. No sustituir `created_at` retroactivamente con Gamma tardío.

**Ventanas preregistradas:** `t0+60s`, `t0+300s`, `t0+3600s`. Eventos y revisiones con `known_at <= cutoff`, cut `capture_seq` cerrado; `received_at` decide causalidad, `source_at/event_time` es atributo del venue, no reloj compartido. Regla de métricas: BBO `bid=max(bids),ask=min(asks)`, mid=(bid+ask)/2, spread=ask-bid, relative_spread=spread/mid cuando mid>0, depth por suma niveles, BUY VWAP a asks y SELL VWAP a bids para tamaños Q; sin depth suficiente => `INSUFFICIENT_DEPTH`; si no hay dos lados => no precio. Δmid solo entre dos observaciones del MISMO asset válidas/contiguas. El último trade nunca altera profundidad ni reemplaza quote. Velocidad a primer book/trade OBSERVADO con right censor y muestra explícita. Reportar mediana/IQR y distribución por régimen sin atribuir causalidad a cambios de tick/fees.

**Controles PE-019/020:** un cambio de display UI entre midpoint/last trade con book fijo produce `DISPLAY_PRICE_ONLY` y cero señal. Trades alternando bid/ask con book fijo producen `BID_ASK_BOUNCE_ONLY`, Δmid=0 y cero señal. No extrapolar umbral UI a contrato ejecutable. `SPREAD_COMPRESSED_DESCRIPTIVE_ONLY` no es retorno neto. Ningún `ActionCandidate`, órdenes, señales live ni estimación PnL si no existe salida ejecutable as-of.

### Semántica temporal, lifecycle y parámetros

| Campo | Semántica autorizada | Nunca inferir |
|---|---|---|
| `market_created_at` | creación del objeto indicado solo con contrato semántico certificado; por ahora UNKNOWN | Gamma `createdAt`=listing o WS timestamp=creación efectiva |
| `market_published_at` | publicación externa probada, UNKNOWN hasta fuente | Gamma `startDate`=publicación |
| `accepting_orders_at` | primera transición false→true OBSERVADA o timestamp venue certificado; almacenar fuente+receive | boolean true actual=instante inicial |
| `first_catalog_observed_at` | primera recepción durable Gamma market (`FirstKnownAt`) | fecha Gamma pasada como local know-at |
| `first_ws_observed_at` | primera recepción durable WS para identidad validada y epoch | event timestamp como receive; cobertura global |
| `first_usable_book_at` | primer full book two-sided, mapped/tick-valid y quality usable | snapshot REST como WS delta base; one-sided válido para spread |
| `first_trade_at` | primera operación histórica solo con feed completo certificado; si no `first_trade_observed_at` | ausencia desde t0=jamás negociado |

Lifecycle son facetas observadas, no linealidad garantizada: DISCOVERED, ORDERS_UNKNOWN/ACCEPTED, BOOK_SEEN/USABLE, TRADING_OBSERVED, HALTED, CLOSED/RESOLVED. Revisión stale no reabre HALTED/CLOSED; contradicción Gamma vs WS => `LIFECYCLE_CONFLICT`. Estado source + known-at + capture_ref siempre. Gap declarado `evidence_gap`, epoch nueva requiere full snapshot; silencio WS sano no es gap, sin interpolar. `max_book_age=30s` es parámetro **de investigación**, no umbral del venue. Más viejo al corte => STALE; no rellenar con próximo book.

**`PE004_params_v1` propuestos, freeze tras A0:** `anchor=CATALOG_FIRST_OBSERVED`, `windows_s=[60,300,3600]`, `max_book_age_s=30`, `min_two_sided_samples=2`, `size_grid_shares=[1,5,10]`, `tick_policy=AS_OF`, `fee_mode=AS_OF_OR_UNKNOWN`, `decision_mode=DESCRIPTIVE_ONLY`, `no_orders=true`; nombres/parámetros existentes en vault local tienen precedencia y discrepancias se registran, no se sobrescriben automáticamente. Identidad del resultado: `market+anchor_kind+t0+window+params_revision+cut_seq+catalog_revision+regime_revision+book_epoch`; re-run mismo manifest produce mismo ordered digest.

**Criterio de producto:** resultado empírico solo cuando hay muestras reales prospectivas, datos as-of, cohortes/denominadores/censura y controles; `REAL_DATA_READY=NO` no bloquea terminar correctamente el core offline, pero bloquea afirmar que PE-004 produce edge.

## SPEC técnica v1

### Autoridades de venue, datos y repo

- [[Polymarket Engine — MVP]]; [[Polymarket — Edge Research Consolidado 2026-09-16]]; [[Polymarket — Technical Platform Map — synced 2026-09-17]]. Referencias venue verificadas: https://docs.polymarket.com/asyncapi.json (NewMarketEvent, opt-in y timestamp); https://docs.polymarket.com/market-data/realtime-data (SDK normalizado != wire); https://docs.polymarket.com/market-data/discover-markets; https://docs.polymarket.com/market-data/market-details. Gamma OpenAPI https://docs.polymarket.com/api-spec/gamma-openapi.yaml fue identificado, NO extraído íntegro; fields semánticos creation/acceptance siguen UNKNOWN hasta contrato verificado. Data v2 no provee replay L2 garantizado.
- `xKoRx/polymarket-engine@9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5`: solo auditoría GitHub remota, sin `go test` ni `git status` local. No clonar lógica del engine dentro de PE-004. Preserve M1/M2 contracts, Go exact decimals, no floats económicos, no nuevos stores/schedulers/collectors/genérico sin segundo consumidor.

### Interfaces y dueño exacto (verificado en remoto; reconfirmar local en A0)

| Seam | Símbolos/archivo | Responsabilidad / condición |
|---|---|---|
| Gamma discovery | `catalog.Service.RunScan`, `catalog.PageSource` / `internal/catalog/scan.go` | reusar scan Gamma durably ACK; scan parcial nunca prueba ausencia |
| As-of metadata | `catalog.Service.InspectEntity`, `MarketContent`, `FirstKnownAt` / `internal/catalog/inspect.go`, `content.go` | first seen local, versiones raw/known-at; no backdating |
| WS subscription/capture | `marketws.connectRaw`, `framesSink.onFrame` / `internal/transport/marketws/marketws.go`, `cmd/engine/record.go` | opt-in ya presente; conservar raw, epoch, capture seq, ACK |
| Lifecycle parser | `protocol.ParseMarketWSEvent`, `MarketWSEnvelope` / `internal/protocol/marketws.go` | mínimo payload typed, discriminator type/event_type, Gamma/Condition/asset IDs disjuntos, strict parse/raw |
| Lifecycle projection | `catalog.Reducer.applyRecord` / `internal/catalog/reducer.go` | vincular aviso WS a Catalog sin falsificar revisión Gamma; dedup, first WS known-at, reconciliación |
| Universe | `catalog.Service.CompileUniverse`, `collectMembers` / `internal/catalog/universe.go` | `Events` filter está incompleto; initial revision `Created=true` aunque `Changed=false`; no prometer feedback auto |
| Capture | `capture.Envelope` / `internal/capture/envelope.go` | BootID, CaptureSeq, ConnectionID, Epoch, receive wall/mono, provenance; no store duplicado |
| Books/quality | `books.Engine`, `applyBook`, `Shard.Transitions` / `internal/books/reducer.go` | full replace, stale/gap/reconnect; first usable derivado causal |
| Frames | `frames.Dispatcher.RequestCut`, `AssetSnapshot` / `internal/frames/dispatcher.go`, `frames.go` | conservar barreras FIFO; nivel precio×size pinned as-of al cut, sin lookup latest/futuro |
| Observer | `strategy.Strategy`, `Factory`, `Assessment` / `internal/strategy/api.go` | nuevo paquete local PE004; callbacks sin I/O; INCONCLUSIVE + Candidate=nil |
| Economics | `economics.WalkSide`, `BuildQuote` / `internal/economics/economics.go` | reuso exact decimal, fee interval/unresolved, real book cut |
| Execution wiring | `cmd/engine/screen.go::runScreen`, `applyOwnerRecord`; `internal/replay/replay.go::RunObservation`; `internal/experiment/experiment.go::RunShadow` | separar fixture neutral de PE004; cortes forward por observación; manifest y data-dir aislados; no synthetics como execution edge |

**Modelo de entrada propuesto** (adoptar contratos reales en A0): observación `{source,source_raw_ref,raw_hash,market_gamma_id,parent_event_gamma_id?,condition_id,asset_id?,capture_seq,boot_id,connection_id,epoch,received_wall,received_mono_offset_ns,venue_event_time_raw?,known_at,revision_refs,quality}`; datos faltantes NULL/UNKNOWN, no rellenar. `MarketWS` puede recibir arrays de eventos; parse elemento a elemento. Dedup de mercado por namespace y condición verificada, no por slug/event ID; mensaje repetido preserva evidencia sin duplicar cohorte. Si IDs colisionan => `IDENTITY_CONFLICT`/quarantine. Una notificación no crea mágicamente un Market Gamma revision.

**Salida inmutable:** observaciones de cohorte por market+asset+cut con `anchor_kind`, `window`, `cut_seq`, refs catálogo/regime/tick/fee, epoch, sample quality/reason, spread/mid/depth/impact/trade flags y missingness. No permitir retroactualizar ventana 1m después de recibir metadata/book 5m. `frames.AssetSnapshot.Levels` es solo count; el dueño Frames debe agregar un snapshot de L2 versionado o un ref resoluble por cut con evidencia durable, eligiendo UNA opción local y probándola. `Runtime` no entrega DB, red, wallet, signer ni clock global a la Strategy.

**Firma lógica conforme API real:** `Describe` identifica `PE-004` versión, mecanismo, metrics; `Universe` declara cohortes específicas por market (NO `spec.Events` defectuoso); `RequiredData` exige metadata as-of y books válidos para métrica, trades opcionales, max ages; `Start` fija manifest/params/versiones; `Detect` solo observa y calcula métricas causales de frames, posibilidad de `Opportunity` **instrumental**; `Evaluate` siempre `Assessment{Decision:INCONCLUSIVE,ReasonCodes:[DESCRIPTIVE_ONLY],Candidate:nil,Metrics:...}` (errores por faltante), no aceptar por umbral de spread; `Observe` recibe feedback y escribe solo por runtime/owner existente, no I/O dentro de callback; `Stop` idempotente. Si métricas agregadas no caben en Strategy, ampliar salida de research mínima por composition/Experiment sin cambiar formato de `ActionCandidate`.

**Riesgos de referencia del pipeline actual:** SCREEN/SHADOW parsean asset con búsqueda textual y solo `book`, fuerzan OBSERVED_USABLE sin reducer completo, generan N cortes al terminar, no desempatan array event; SHADOW ofrece fake size=10, FeeUnresolved, notional bruto y `INCONCLUSIVE`; ambos pueden abrir y mutar journal por `capture.Open`. No usar como oráculo de calidad ni para backtest. REPLAY observation manifiesta hash de segmentos pero no scorecard de PE004. La nueva integración debe capturar/proyectar/emitir cortes en orden de recepción hasta cutoff y conservar denominadores de frames INELIGIBLE. No tocar data-dir de RS vivo.

### Fixtures F01–F20: especificación de corpus a serializar, no tests ya hechos

**B0 sintética común:** `t0=2026-09-20T12:00:00.000Z`; parent Gamma E1=9001; Market Gamma M1=1001; Condition C1=`0x` + 64 `a`; YES/NO token A101/A102 (sintéticos); Gamma G1 recibido t0, `FirstKnownAt=t0`; boot B1, WS epoch W1; tick T1=.01, fee F1=0 **solo fixture**, acceptingOrders=true conocido t0 (sin afirmar hora de primer true). Por asset, books full at +1s, +60s,+300s,+3600s con bid `0.40×10`, ask `0.60×10`; midpoint=.50, spread=.20, relative=.40, Q10 VWAP buy=.60/sell=.40 e impacto relativo al best=0; no trade ni gap por defecto. Si una fila reemplaza un instante/evento/revisión, sustituye B0 (NO duplica). Reasignar q1..qN por orden local de recepción; qN no es secuencia venue. Raw bytes + manifest SHA256 + timelines + expected JSON + digest y source `GENERATED/synthetic=true` por fixture. Para no imputar snapshot viejo, toda ventana requiere libro de corte fresco <=30s. Ninguna fixture es evidencia empírica.

| Fixture | Cambio explícito sobre B0 | Resultado y gate esperado |
|---|---|---|
| F01 | new_market q1 t0; book q2 +1; trade TX1 q3 +20 a .60; books q4 +60,q5 +300,q6 +3600 | 1 market, book +1, first trade **observed** +20, spread .20 en cortes, ninguna acción ni true creation time |
| F02 | M2/C2 independiente, Gamma createdAt declarado t0-1h pero recibido t0 | ancla O=t0; creation cohort bloqueada; LATE_DISCOVERY; ningún pasado importado |
| F03 | new_market idéntico repetido +2, hash igual; book +3 | un mercado, duplicate count 1; mismo first known |
| F04 | book recibido +1, aviso WS +3 con venue time t0 | EVENT_OUT_OF_ORDER; no antedatar first WS local ni proyectar evento antes de +3 |
| F05 | Gamma G1 no mapea asset↔condition hasta G2 +15; aviso +10; full +16 | metadata insufficient antes +15; primer usable >=+16; no backfill del libro +1 |
| F06 | no books hasta +3600 inclusive; heartbeat sano | NO_USABLE_BOOK, no spread 0, censura >=1h, no inference never-traded |
| F07 | books +1,+30; gap declarado +40..+120; W2 full +121; cuts >=300 | 1m KNOWN_CAPTURE_GAP/INCOMPLETE; no interpolation; reanchor nuevo epoch |
| F08 | W1 book +1; W2 +21; delta +22 antes del full +25 | WAIT_INITIAL_BOOK descarta delta; no mezcla epochs |
| F09 | T1 .01 cambia a T2 .001 en +21 y full +22 | REGIME_TICK_CHANGED; dos intervalos, no attribution orgánica |
| F10 | F1=0 a F2>0 desde +21; book sin cambio | FEE_REGIME_CHANGED; no precio/fee futuro en cálculo previo |
| F11 | G2 halt/accepting=false +30; aviso viejo +45 y book +60 | MARKET_HALTED, descriptiva censurada, nunca opportunity ejecutable |
| F12 | book +1 .40/.60; +60 .48/.52 ×10; fee F1 0 | spread .20→.04; mid .50; roundtrip contemporáneo BUY .52/SELL .48 negativo; DESCRIPTIVE_ONLY |
| F13 | book fijo .40/.60; display UI .50→.40 at +10; last trade .40 | PE019 DISPLAY_PRICE_ONLY; BBO/mid invariables; cero action |
| F14 | TX1 bid .40 +10; TX2 ask .60 +20; book fijo | PE020 BID_ASK_BOUNCE_ONLY; trade delta .20; Δmid=0; cero action |
| F15 | bid .40×10; asks .60×0.1 y .95×9.9; Q10 | buy VWAP=.9465, impact=.3465; no false midpoint/synthetic depth |
| F16 | +300 future book .48/.52 inyectado con known_at=+300 al frame +60 | LOOKAHEAD_REJECTED en +60; prueba roja si detector contaminado acepta futuro |
| F17 | book +1,+60, luego +330,+3600; a +300 book tiene 240s | STALE_BOOK_AT_CUTOFF; INCOMPLETE, no inventar capture gap por silencio |
| F18 | todos los libros B0; no trade observado | NO_TRADE_OBSERVED_IN_CAPTURE; time-to-trade censurado, spread aún medible |
| F19 | M1 ancla t0; M2/C2 ancla t0+30m; parent E1 compartido | dos relojes individuales; M2 no tiene 1h completa al t0+1h; cluster parent=1 |
| F20 | B0 mismo raw con schedules [1], [7,3,1], [32] | outputs ordenados byte-equivalentes y digest idéntico, no clock/red/write activo |

**Harness de fixtures:** cada caso contiene `id,fixture_schema_version=1,synthetic=true,source=GENERATED,params_revision,raw_capture_records,metadata/epoch timelines,expected_anchors,expected_quality/reasons,expected_metrics,expected_digest`. FAIL si aparece order, dato futuro, gap inventado, dedup erróneo, timestamp interpolado, market ID confundido con token, fee futura o índice revisado ex post. Verificar raw→Capture durable→Catalog/Books/Frames→Observer→Scorecard→REPLAY para cada caso. 20 definidas semánticamente; **0 serializadas y 0 ejecutadas a fecha de la nota**.

### Work packages · secuencia, ownership, tests y gates

| WP | Owner / allowed files verificados remotamente (reconfirmar A0) | Entrada→salida, pruebas, gate | Dependencia |
|---|---|---|---|
| A0 | READ ONLY: checkout engine+vault; no modified files | git HEAD/status/branch/writers/RS, comparar 14 seams y source SHA, resolver S05+params; G0–G3 o BLOCKED | ninguna |
| A1 | `internal/catalog/{scan,inspect,content,reducer,universe}.go` SOLO correctivo requerido | first-known/anchors/revisions/initial universe; F02–05,19; G-TEMP/G-UNIVERSE | A0 |
| A2 | `internal/protocol/marketws.go`, `internal/catalog/reducer.go`, composición `cmd/engine/record.go` solo si necesaria | typed new_market, id/epoch, raw→journal→catalog, dedup; F01,03,04,05,08; G-CAPTURE-RAW/G-LIFECYCLE | A0,A1 |
| A3 | `internal/books/{books,reducer}.go`, `internal/frames/{frames,dispatcher}.go` y testdata OWNED | full/epoch/gap/quality, depth pinned as-of; F06–11,15–17; G-DEPTH/G-FORWARD | A1,A2 |
| B1 | nuevo `internal/strategy/pe004/` + tests, `internal/strategy/api.go` solo extension indispensable | Strategy/Factory descriptive, metrics/denominators, no-I/O/no orders; F01–20; G-STRATEGY | A1–A3 |
| B2 | reutilizar `internal/economics/economics.go`, `internal/regimes/` solo delta demostrado | Q1/5/10 depth real + fees as-of/unknown, no mark-to-mid; F09,10,12,15; G-ECON | A3,B1 |
| B3 | `internal/strategy/pe004/`, `internal/experiment/experiment.go` bajo ownership existente | controles PE019/020, scorecard/manifest, trade dedup/censor; F12–14,18; G-NEG-019/020 | B1,B2 |
| C1 | `cmd/engine/screen.go` + composition tests | registry PE004 y cortes DURANTE replay, no all-at-end; calidad real; 20 fixtures; G-SCREEN | B1–B3 |
| C2 | `internal/replay/replay.go`, `internal/experiment/experiment.go`, integration/testdata aislados | manifests pinned, schedules identical, SHADOW observation-only, no active boot; F07,08,16,20; G-ISOLATION/G-REPLAY | C1 |
| C3 | exclusivamente tests/fixtures/evidence/docs PE004 y regresiones propias por owner | 20/20, build/vet/test/race, coverage >=95% por paquete tocado, M4 no regresión, SHA/hashes/receipts; G-REGRESSION | C2 |

**Scope gates:** cada WP fija en esta tabla antes de editar rutas exactas, tests y SHA local de A0; no aplicar whitelist genérica como permiso a tocar módulos enteros. Rechazar trabajo con cambios ajenos, lock activo, divergencia de HEAD o decisiones incompatibles. Los cambios transversales los hace owner del módulo, no la Strategy. Ejecutar WP secuencialmente salvo paralelismo por ownership disjunto y barreras documentadas. No reset, force push, rebase ni overwrite; no push del engine y no interrumpir RS.

**G0** repositorios/working trees y writer ownership; **G1** schema venue y límites de cobertura (creation aún blocked puede continuar O); **G2** seams/HEAD locales y allowed files; **G3** 7 timestamps/known-at/cohort/as-of; **G4** 20 fixtures native + manifest SHA/expected; **G5** frozen SPEC/params/economics/negative controls; **G6** todo WP con archivos/deps/test/policy; **G7** nota AGENTS-OS schema/lint/Graphify/bridge. Gates implementación específicos: `G-CAPTURE-RAW`, `G-LIFECYCLE`, `G-UNIVERSE`, `G-DEPTH`, `G-FORWARD`, `G-STRATEGY`, `G-ECON`, `G-NEG-019/020`, `G-SCREEN`, `G-ISOLATION`, `G-REPLAY`, `G-REGRESSION`. Registrar PASS solo con comando, SHA y recibo verificable; ausente = NOT_RUN. RS dataset o Gamma vivo no accesible = DATA_BLOCKED, jamás resultado económico inventado.

### Reglas de riesgo, seguridad y NO_GO

- `LIVE_DISABLED` / `NO_ORDER` toda la POC. SCREEN observación, REPLAY/SHADOW virtual offline y dataset descartable. No habilitar wallet, creds, signer, execution real, permisos IAM, LIVE lease ni capital. Tiny-live US$300 del engine padre no autoriza trading en PE004.
- No interpretar el precio UI, midpoint ni último trade como fill. Depth must be real as-of; fee UNRESOLVED/SUSPECT conserva incertidumbre, salida futura desconocida => net UNKNOWN. No usar costes promedio inventados ni fee 0 fuera de fixture sintética.
- No usar `/data-dir` activo ni `capture.Open` sobre journal RS vivo. Inspeccionar con OpenView y copia con hashes/manifest. Un cambio de boot, writes sobre dataset o pérdida de raw aborta test.
- No falsos PASS de tests, cobertura, real cases, backtest net, Graphify o aceptación humana. Sin datos completos no concluir ausencia de transacciones ni historia L2. Cualquier violación de tiempo, fee, identidad, epoch, owners o dato futuro = gate FAIL/INCONCLUSIVE, no reparar con interpolación.

## 📆 Bitácora

- **2026-09-20 — Creación documental remota:** se creó la nota canónica con plantilla `project` v1 replicada desde fuente, SPEC funcional/técnica, 20 casos sintéticos especificados, 10 WPs y mandato de implementación. Código engine solo auditado remotamente en `9ae5ddec...`; no se corrieron tests, no se tocó el dataset, no se implementó PE004. Pendiente G0 local, tarea puente del padre, lint/Graphify y freeze real. No registrar como completada la planificación operacional si esos gates no están probados.

## 🧭 Decisiones

- **D-001:** separar maduración descriptiva PE004-A de predictor económico PE004-B bloqueado; ningún ActionCandidate.
- **D-002:** v1 primera observación Gamma local como ancla canónica; WS notice y first book son cohortes diferentes; created/publication no inferidos.
- **D-003:** no nueva infraestructura ni duplicación Economics, Catalog o Frames; mínimos del owner y tests negativos.
- **D-004:** no usar SCREEN/SHADOW neutral actual como backtest causal; dataset disposable, forward cuts y L2 realmente conocido.
- **D-005:** parámetros propuestos sujetos a reconciliación local, sin tocar congelación M1/M2; cuando falte evidencia, estado BLOCKED/INCONCLUSIVE.

## 🔗 Docs / Links

- [[Polymarket Engine — MVP]] · [[Polymarket — Edge Research Consolidado 2026-09-16]] · [[Polymarket — Technical Platform Map — synced 2026-09-17]] · [[Polymarket Engine — Opportunity Context]].
- Venue: https://docs.polymarket.com/asyncapi.json · https://docs.polymarket.com/market-data/discover-markets · https://docs.polymarket.com/market-data/realtime-data.
- Code audit: https://github.com/xKoRx/polymarket-engine/tree/9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5.
- Handoff externo de investigación existe en ChatGPT Library `/PE-004/PE-004-New-Market-Maturation-Research-Handoff-2026-09-20.md`, únicamente evidencia auxiliar histórica; esta nota es autosuficiente, fuente de verdad del proyecto.

## 💡 Ideas

### Backlog de ideas

- Variante creación real C únicamente después de certificar timestamps y cobertura histórica; predictor B y tiny-live como **proyecto/fase futuros sujetos a nueva SPEC y aprobación humana**, no en este mandato.

### Motivos / principios

- Time-to-validated-hypothesis; observación ≠ oportunidad; known-at ≠ venue time; quote ≠ fill; reproducibilidad antes de extrapolación.

### Memoria pública / interna

- **Pública:** esta nota, referencias pinneadas, manifests/fixtures y recibos del engine cuando existan.
- **Interna:** no persistir deliberación de agente ni secretos en notas de proyecto.
- **Motivo:** cualquier coding agent debe retomar por el estado de tareas y gates sin depender del historial de chat.

---

## MANDATO DE IMPLEMENTACIÓN AUTÓNOMO — emitir a coding agent SOLO tras G0

**Rol y alcance:** Principal Go implementer PE-004, ownership estricto. No redescubrir investigación venue salvo contradicción efectiva de versión. Leer `AGENTS.md`, `main/AGENTS.md`, bootstrap, padre, esta nota y autoridades enlazadas; no cerrar sesión completa de Agents-OS salvo instrucción. Primer output verificable: `pwd; git status --short; git rev-parse HEAD; git branch --show-current` en engine y vault; corroborar writers, RS capture, plantilla/path/bridge y params. Local HEAD puede diferir del remoto `9ae5dde`; actualizar esta nota con el SHA real antes de ejecución. Si conflicto en archivos o está activo otro writer, STOP y devolver bloqueo concreto; sin git reset/checkout/rebase/force/push. A0 read-only y reconciliación de tabla `Entrega de desarrollo` preceden a código.

**Freeze obligatorio:** comprobar archivos, símbolos y firmas de la matriz, decidir un único transporte de profundidad exacta pinned al cut, preservar fronteras de M1/M2 y resolver parámetros locales. Establecer branch/base, allowed files por WP y fixtures serializadas nativas con `expected` y hash. Actualizar `SPEC_v1=FROZEN` en nota solo con G0–G5 respaldados; si solo cohort C sigue bloqueada, congelar O/B con limitación C y no llamarla muestra de creación real. Si Gamma actual difiere del contrato identificado, documentar y fail-closed antes de usar campos ambiguos.

**Fase A:** A1 known-at y cohorte Gamma; A2 parse/identity+projection lifecycle WS durable, dedup y reconciliación as-of; A3 epoch/book full/quality+L2 depth pinneado al forward cut. Tests F01–11,15–17,19. Jamás escribir timestamp retroactivo por fuente más tardía, aplicar delta W2 antes full, usar UI como BBO, inferir gap desde silencio ni marcar usable sin dos lados. Un full snapshot sustituye niveles, no fusiona.

**Fase B:** B1 observer/Factory independiente del `neutral`, determinista sin I/O/clock global; `Detect` genera solo observaciones instrumentales, `Evaluate` INCONCLUSIVE + DESCRIPTIVE_ONLY + Candidate=nil, Observe y Stop idempotentes. B2 costos hipotéticos por Economics exacto y profundidad real con fee as-of o unknown, Q1/5/10; B3 negative controls PE019/020 y scorecard con cohortes, censura, missingness y denominator. Ejecutar F01–20; cero órdenes, cero signal live, cero PnL neto inferido de caída de spread.

**Fase C:** C1 integrar registry de Strategy y cortar frames durante el recorrido ordenado antes de que entren records futuros. No usar `applyOwnerRecord` con bandera OBSERVED_USABLE artificial ni parse de asset por simple substring como autoridad; proyectar calidad real. C2 REPLAY/SHADOW en corpus desechable con manifiesto pinned y `capture.OpenView` de lectura, sin tocar RS; reproducibilidad entre schedules 1/7-3-1/32, false positives negativos cero. C3 build/vet/test/race, cobertura por paquete tocado >=95% después de caminos críticos, regression del certificado previo y lint/esquema del proyecto. No usar runner `--skip-suites` para PASS.

**Entrega final del agente:** actualizar esta nota WP por WP `[ ]→[/]→[r]→[x]` únicamente con evidencia, progreso real y bitácora por hito; reportar SHA inicial/final, diff allowed-files, commands/output de tests, coverage, hash raw+manifest+scorecard, G0–G7 e implementación gates, 20 fixtures y casos reales (si 0, 0). Estado de investigación distinto de autorización LIVE. Cuando esté TODO listo para revisión, puente humano máximo `[r]`, jamás `[x]` automático. Si no hay datos o APIs del venue disponibles, entregar core offline con `REAL_DATA_BLOCKED` y próximo trabajo preciso, no inventar una estrategia rentable.
