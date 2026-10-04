# Echo Futures — D6 G-REALTIME — REAL MARKET DATA CERTIFICATION (feed-only, NO-EGRESS)

**Rol:** TOP Physical Market Data Certification Lead (one-shot, fresh context; no Manager, no Owner)
**Fecha:** 2026-10-04 (domingo; evidencia UTC 20:00Z–22:15Z = 15:00–17:15 CT)
**Proyecto:** [[Echo Futures]]
**Autoridad de ejecución:** C0–H CERTIFIED / FROZEN — `FINAL_SHA = d08a30ce9815f820fda7132e20dc42cc345eb8e8` (HEAD == origin == worktree, 0 dirty, verificado hoy). NO reabierto, NO tocado.
**Veredicto:** `G_REALTIME = PASS` — feed realtime físico certificado sobre la sesión CME abierta, sin habilitar new-risk y sin ejecutar ninguna orden.

---

## A — Market open precondition — PASS (movimiento físico, no wall-clock)

El calendario anticipaba reopen dom 17:00 CT (22:00Z), pero el gate exigió prueba física y así se certificó:

- **21:05:41.433Z (16:05:41 CT):** primer tick físico del día — QUOTE BBO `31044/31051.75` (viernes cerró 31044/31052.5), transit 92 ms (offsets p4 5476486-87). Tick de pre-apertura.
- **21:54:23.474Z:** inicio del stream sostenido (BBO bid qty 1→5; luego ask 31051.75→31039.75, movimiento real de 12 pts).
- **22:00:00Z (17:00 CT):** apertura oficial Globex — stream a ~1,700–2,300 eventos/min; NQ subió 31044→31142 durante la ventana (movimiento físico sostenido con TRADEs).

## B — Real feed session — PASS

| Elemento | Evidencia |
|---|---|
| NinjaTrader | dev-win 192.168.31.132, **PID 1476**, NT **8.1.8.3** (hello frames) |
| EchoFeedAddOn | sesión **`5b70e536d0234f50b2f6458e88417206`**, `addon_version 1.0.0` (== constante HEAD @ d08a30ce), hello autenticado 2026-10-04T16:08:15.196Z con `expected_account RJARA114411201551 / id 3`, `instruments ["NQ 12-26"]` |
| EchoExecutionAddOn (observación, sin lane) | sesión `348f52babe6246eea7a70388cfbfb05e`, `addon_version 2.0.0`, hello mismo account/instrument; publica account+heartbeat al feed lane; **sin sesión ntx** (bridge down) |
| Relay | `echo-nt-feed-relay` **PID 1388002**, release `170a4581`, activo continuo desde 2026-10-01 22:20:52 -03, LISTEN `*:9770`, `echo.ntfeed.binding_loaded=true` |
| Transporte | 2 conexiones TCP ESTABLISHED .132→.161:9770 durante toda la ventana; heartbeats ~10 s; `reconnects:1` estable; **0 líneas de error/supersede/reconnect reales en 8 h** (journal refinado) |
| Discovery | 8 cuentas, match **RESOLVED 1/8** (`RJARA114411201551` = Id "3"), frames `account` cada ~5 s durante toda la ventana (último 22:13:10Z), balances demo 50000/50000 |

## C — Event freshness — PASS

Autoridad = `event_ts` del evento de mercado (jamás Kafka arrival ni replay frame). Bound frozen: `FreshnessBound 30s` (`DefaultFreshnessBounds`, `futures_market_stream.go:83` @ d08a30ce).

| Muestra | UTC | último event_ts | **age** | end offset p4 | BBO |
|---|---|---|---|---|---|
| T1 | 22:00:48 | 22:00:48.558Z | **0.14 s** | 5479859 | 31114.75/31117.5 |
| T2 | 22:03:45 | 22:03:45.441Z | **0.15 s** | 5486723 | 31121/31122.5 |
| T3 | 22:06:37 | 22:06:37.332Z | **0.18 s** | 5491762 | 31141.5/31142.75 |
| T4 | 22:09:48 | 22:09:47.956Z | **0.12 s** | 5495922 | 31129/31130.75 |
| T5 | 22:12:30 | 22:12:30.576Z | **0.11 s** | 5498982 | 31129/31130.5 |

**MAX_EVENT_AGE = 0.18 s << 30 s.** Transit `event_ts → receive_ts (Kafka)`: 89–295 ms. El replay del boot (event_ts viernes 2026-10-02T21:38:25.95Z publicado al reconectar 16:08Z) quedó documentado y **excluido** como prueba — exactamente la trampa que el gate prohíbe.

## D — Continuous advancement — PASS

- **Ventana formal:** 2026-10-04T21:54:23.474Z → 22:12:30.576Z (**~18 min**), 5 muestras sucesivas post-reopen (T1–T5, 22:00:48Z→22:12:30Z) + monitor de 60 s desde 20:10Z (`evidence/g-realtime-evidence.txt`, `/tmp/grealtime-monitor.log`).
- **event_ts monótono avanzando** en TODAS las muestras; **22,494 eventos reales** (p4 offsets 5476488→5498982); counter `ntfeed.published` 5,007,124→5,030,056+ con **publish_errors=0, malformed=0**.
- **Tipos observados:** QUOTE + TRADE (bloque 5491000–5491029: 2 TRADE @31141 + 28 QUOTE en 626 ms de tiempo de mercado — libro churn continuo, no one-off replay).
- Fase pre-apertura documentada: tick aislado 21:05:41Z + silencio hasta 21:54Z (rotación de apertura del venue); la certificación de freshness corre sobre la operación live post-22:00Z.

## E — Contract / Symbol — PASS

- ETCD crudo `nt-feed/instruments` = `[{"nt_name":"NQ 12-26","stream_id":"NQ:NQZ6"}]` (sin drift, sin remap).
- Cada evento físico: key/stream_id **`NQ:NQZ6`**, `source_id NINJATRADER_ADDON`, ingress del AddOn vivo; NT instrumento `NQ 12-26` (hello).

## F — Pipeline freshness — PASS

`CURRENT_MARKET_FRESHNESS = FRESH` bajo el modelo frozen (event_ts age 0.11–0.18 s << bound 30 s, stream vivo, sin decay). El path físico certificado es el runbook congelado §9 del Weekend Readiness (probe `kafka-last`/consume último offset del topic de candidatos): relay publica los eventos del AddOn real al topic designado (`echo.futures.market-feed-candidates.v1`, ETCD `nt-feed/market-topic`) con 0 errores. Sin inyección sintética, sin fixture, sin reescritura de timestamps. El consumo downstream con run-config (vertical) no fue arrancado: este gate es feed-only y esa integración pertenece al ladder.

## G — No regression — PASS

Discovery sano (RESOLVED 1/8 continuo); AddOn estable (2 sesiones, sin storm, `stale:false` por frames avanzando); sin anomalía de stream/sesión duplicada (todos los eventos de la sesión feed única); **0 frames ntfeed hacia :9771** (sin listener, sin conexión, imposibilidad estructural); transporte de ejecución intacto (C0–H frozen, 0 mutaciones); sin orden path habilitado.

## H — Final safety state — G-EGRESS-0 PASS

- Unidad `echo-futures-bridge.service`: **inactive + disabled**; `:9771` sin listener y 0 conexiones establecidas.
- ETCD crudo (sin fuzzy): `futures-bridge/accounts` **ABSENT**; prefijo 21 claves == baseline.
- Topic `echo.order-commands.E2T-GAU50-01.v1`: **high_watermark 0 — cero comandos pendientes/replayables** (committed `-1001` invariante).
- Journal M2: **0 archivos**. Venue observado vivo al cierre: `positions: []`, `orders: []` (22:13:10Z).
- `PHYSICAL_ORDERS_SENT = 0 · PHYSICAL_ORDERS_MODIFIED = 0 · PHYSICAL_ORDERS_CANCELLED = 0` (estructural: sin proceso bridge, sin lane, sin fuente de comandos, venue plano observado).
- `CROSS_PROTOCOL_CONTAMINATION = NONE` (ntfeed jamás alcanzó :9771; ntx jamás apareció en :9770 — rechazos del relay estáticos 733 históricos, 0 nuevos).
- `EXECUTION_TRANSPORT_TOUCHED = NO` · `PRODUCT_CODE_CHANGES = NONE` (cero commits, cero mutaciones ETCD/config; único delta = este artifact + registros observacionales).

## Residual findings (no bloqueantes)

1. Fase pre-apertura dispersa del venue (tick 21:05Z + silencio hasta 21:54Z): comportamiento del calendario del exchange, documentado; el criterio de freshness se evaluó en operación live.
2. Fallos de export de métricas OTLP del relay (192.168.31.45:4317 refused): observabilidad only, sin impacto en el path de datos.
3. `CURRENT_MARKET_FRESHNESS=FRESH` certificado sobre el path feed-only congelado (probe runbook §9); la exposición del mismo por el vertical con run-config se ejercita en el ladder.
4. Balances demo del provider 50000/50000 con BP 0 (variante documentada del feed demo; ya registrada en intentos previos).

## Close

```text
G_REALTIME = PASS

SOURCE_SHA:
d08a30ce9815f820fda7132e20dc42cc345eb8e8

MARKET_SESSION_OPEN:
YES — movimiento físico: BBO 31044/31051.75→31129/31130.5, TRADEs reales, 22,494 eventos en la ventana

FEED_ADDON:
PASS — EchoFeedAddOn 1.0.0 @ NT 8.1.8.3, sesión 5b70e536…, hello autenticado, instrumento NQ 12-26

REAL_FEED_SESSION:
PASS — relay PID 1388002 (release 170a4581, up 2+ días), 2× ESTABLISHED .132→:9770, heartbeats 10s, reconnects:1, 0 errores 8h, binding_loaded=true, NT PID 1476

CONTRACT:
NQZ6

NT_INSTRUMENT:
NQ 12-26

ECHO_STREAM:
NQ:NQZ6

FIRST_EVENT_TS:
2026-10-04T21:54:23.474Z (primer evento del stream sostenido; pre-open tick físico 21:05:41.433Z documentado)

LAST_EVENT_TS:
2026-10-04T22:12:30.576Z

OBSERVATION_DURATION:
~18m07s ventana formal (21:54:23Z→22:12:31Z); 5 muestras sucesivas 22:00:48Z→22:12:30Z; monitor 60s desde 20:10Z

REAL_MARKET_EVENT_COUNT:
22494 (p4 offsets 5476488→5498982); ntfeed.published +21,714 al 22:11:42Z, publish_errors=0

MAX_EVENT_AGE:
0.18s (bound frozen 30s; transit event_ts→Kafka 89–295ms)

CURRENT_MARKET_FRESHNESS:
FRESH

PIPELINE_REALTIME:
PASS (probe runbook congelado §9: AddOn→relay→Kafka con event_ts realtime, 0 errores; sin inyección/replay/reescritura)

CROSS_PROTOCOL_CONTAMINATION:
NONE

EXECUTION_TRANSPORT_TOUCHED:
NO

PHYSICAL_ORDERS_SENT:
0

PHYSICAL_ORDERS_MODIFIED:
0

PHYSICAL_ORDERS_CANCELLED:
0

FINAL_SAFETY_STATE:
G-EGRESS-0 PASS (unidad inactive+disabled, :9771 FREE, ETCD accounts ABSENT / 21 claves baseline, topic comandos 0 mensajes, journal M2 0, venue plano []/[] observado vivo)

PRODUCT_CODE_CHANGES:
NONE

RESIDUAL_FINDINGS:
1) pre-open venue sparse (21:05Z tick + silencio→21:54Z, calendario del exchange, documentado) · 2) OTLP export failures 192.168.31.45:4317 (observability only) · 3) FRESH expuesto por el path feed-only congelado; consumo del vertical con run-config pertenece al ladder · 4) balances demo 50000/50000 BP 0 (variante provider)

OWNER_DECISION_REQUIRED:
NONE

NEXT_MANAGER_ACTION:
FREEZE G-REALTIME como certificado (no re-ejecutar en la ventana del lunes salvo anomalía). Despachar el FINAL D6 PHYSICAL LADDER ya autorizado (OD-D6-1 vigente SIN consumir) en la primera ventana admisible ProviderRuleSet: lun 2026-10-05 00:00–15:50 CT (o evening 17:10–23:59 CT), con la preparación operacional del intento 1 §17.2 ejecutada DENTRO de la ventana (habilitar sesión accounts + arrancar bridge → barrier con venue real → run config → G-STOP → G-ID-Retention → G-HORIZON → G-E2E (+drill) → G-PERF). NO emitir EF_D6_E2E_PASS hasta que el ladder completo pase.
```
