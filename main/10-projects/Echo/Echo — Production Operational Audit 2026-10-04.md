---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Production Operational Audit 2026-09-28]]"
  - "[[Echo — Production Operational Audit 2026-09-27]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
aliases:
  - Echo PROD operational audit 2026-10-04
  - auditoria operacional Echo PROD 04-oct
tags:
  - kind/doc
  - area/echo
  - action/audit
created: "2026-10-04"
updated: "2026-10-04"
---

# Echo — Production Operational Audit 2026-10-04

## Propósito

Auditoría operacional read-only completa de Echo PROD pedida por el owner: *"necesito saber si está corriendo correctamente; revisa integraciones y logs de las aplicaciones clave para determinar si hay algún fallo crítico"*. Ejecutada 2026-10-04 ~23:00–00:10 UTC (domingo, apertura de mercado 22:00 UTC incluida en la ventana). Con `aranea-ssh` disponible (primera auditoría con runtime `.71` verificado desde la matriz del 15-sep). Regresión contra [[Echo — Production Operational Audit 2026-09-28]].

**Veredicto: `OPERATIONAL_PASS`.** No se encontró ningún fallo crítico. El runtime de `.71` corre sin reinicios desde el rollout del 25-sep con el tip vigente de `origin/master` (`372af59a`, cero drift); la configuración ETCD está intacta y sin contaminación DEV; el pipeline E2E procesa y persiste al segundo del evento (demostrado en vivo con la apertura dominical de las 22:00); **AUD-17 quedó cerrado** — la copia a cuentas de ejecución se recuperó y el gate de regresión (ticket≠0 en 442688 y 431007281) está cumplido; la copia fluye hoy por ~15 cuentas y ~14 estrategias (AUD-18 sustancialmente mejorado); 0 ERROR en core/bridge en 24 h y exactamente 1 WARN (rechazo esperado "market closed" en la apertura). Los hallazgos nuevos son P3/P4 operativos (volumen de logs, un listener extra, higiene de métricas), ninguno afecta trading.

## Cadena de evidencia (traza apertura 2026-10-04 22:00 UTC, trade_id `01a10993-8040-7f41-8000-731368b978e8`)

1. **Señal viva en apertura:** strategy `magic_250901050` (NDX) abre BUY en cuenta reference `2089125533` a las 22:00:24 UTC — ticket `270086196`, fila OPEN persistida al segundo.
2. **Planner dispara la copia:** 2 segundos después (22:00:26) la pierna EXECUTION hacia `80577453` (mt4-real) es rechazada por el broker con **error 10018 "market closed"** (símbolo broker `US100`, lot 2.42) — el broker de esa cuenta aún no abría su sesión mientras la reference ya cotizaba. Journal registra FAILED con error_code 10018, ticket 0.
3. **Core correlaciona:** Loki core level=WARN contiene exactamente esa única línea en 24 h (`execution_store: [OPEN_FAILED] open command execution failed on EA`, error_code 10018, execution_account_id 80577453, mismo trace_id `01a10993…`). Sin `mm_engine` errors ni rechazos del planner en la ventana.
4. **Transporte vivo al momento de la auditoría:** bridge `mt4-real` publicando `AccountSnapshot published` (80570850, balance 105,622.94) y `InstrumentSnapshot published` (WSF `USDJPYc` → canónico `USDJPY`) con timestamps del instante de la consulta; journal `max(created_at)` = 22:00:26 (siguiente señal pendiente de apertura de sesión de los brokers NDX); `accounts.updated_at` heartbeat <1 min.
5. **Broker mediado por terminal verificado en la semana:** legs CLOSED con tickets reales en 15 cuentas de ejecución distintas (Sep 29–Oct 2), incluyendo NDX, GOLD y USDJPY — evidencia física de broker en ambas plataformas (TTP 2879xxxx, FTMO 4909xxxx, Orion/WSF 6347xxxx/2368xxxx).

## Trading en la ventana (journal, 27-sep → 04-oct)

| Fecha | EXECUTION | REFERENCE | Nota |
|---|---|---|---|
| 27-sep (sáb) | — | 1 CLOSED | mercado cerrado |
| 28-sep | 4 FAILED (4109) | 21 CLOSED | AUD-17, bloqueo terminales |
| 29-sep | 5 CLOSED | 18 CLOSED | copia recuperada (mt4-real primero) |
| 30-sep | 1 CLOSED | 22 CLOSED | |
| 01-oct | 31 CLOSED | 33 CLOSED | rabajo de 11+ estrategias nuevas (magic_251002044–054, 260104004); 442688 y 431007281 vuelven con tickets |
| 02-oct | 4 CLOSED | 69 CLOSED | |
| 03-oct (vie) | — | — | sin señales, sin cierres (0 filas, no es gap) |
| 04-oct (dom) | 1 FAILED (10018) | 1 OPEN | apertura 22:00 UTC |

- **Gate de regresión AUD-17: CUMPLIDO.** `442688` leg CLOSED ticket `28793918` (01-oct 11:03 USDJPY); `431007281` legs CLOSED tickets `49091561`, `49091562`, `49147469` (01–02 oct). El 4109 no volvió a ocurrir desde el 28-sep.
- **AUD-18 mejorado:** la copia ya no depende de una sola estrategia — Oct 1 muestra ~14 estrategias con targets vivos (magic_250601005, 250901048/050, 251002044–054, 260104004) repartidas en 15 cuentas de ejecución.
- `active_positions` = 0 con la pierna OPEN del día siendo REFERENCE (consistente: la tabla es de ejecución; leg OPEN de ejecución = 0).
- Exposición agregada (balances, sin PnL derivado): 17 ACTIVE ≈ $1,265,426 · 21 ARCHIVED ≈ $1,011,559 · 11 INACTIVE ≈ $108,001.

## Gates

| Gate | Estado | Justificación |
|---|---|---|
| G1 runtime | PASS | SSH viewer `echo-runtime-prod`: hostname `echo`, uid 1001(echo-dev); `echo-core` PID 441462, `echo-gateway` PID 442685, `echo-functions` PID 441170, nginx, promtail; sin `echo-bridge` en .71 (correcto, corren en Windows) |
| G2 identidad | PASS (máx alcanzable) | Binarios `/home/kor/echo/echo-*`, START sep25 = rollout 25-sep; `service.version` 2.0.0 en OTEL; SHA exacto no legible por viewer — declarado; `origin/master` remoto = `372af59a` = commit del rollout ⇒ sin drift |
| G3 config | PASS | ETCD `/echo/production/` = 37 keys (igual que 09-28); brokers Kafka `.247-.249:9092`, PG `.220/echo`, gateway core `localhost:9090`, functions enabled, telemetry level WARN; cero endpoints DEV (no .44:19091, no .161, no echo-develop) |
| G4 servicios | PASS | PG `echo` 6 backends vivos (814.8M xact); Hasura v2.38.0 metadata consistente; etcd/ARGUS sirviendo; Lab 138 corridas/24 h, última 23:55:55 UTC |
| G5 transporte | PASS | Journal al segundo del evento (22:00:24/26); bridge publicando snapshots de cuenta e instrumento en el instante de la auditoría; gateway en silencio event-driven ≥48 h (normal); 17 execution connections en Prometheus |
| G6 datos | PASS | 0 grupos duplicados (trade_id, account_id) sobre 3,918 filas; consistencia journal↔active_positions correcta; FAILED bien tipificados (10018 con error_message) |
| G7 trading | PASS | AUD-17 cerrado: 4109 extinto desde 28-sep; 15 cuentas con tickets reales en la semana; apertura dominical procesada (reference OPEN con ticket; copia rechazada sólo por sesión de broker) |
| G8 riesgo | PASS | `account_strategy_risk_policy` vigente (49 cuentas con configs); 0 WARN del planner en 24 h (sin exclusiones anómalas); exposición agregada reportada sin PnL derivado; cuenta archivada fuera del planner |
| G9 observabilidad | PASS | Loki level-labels operativos (DEBUG/INFO/WARN presentes, 0 ERROR); Prometheus `echo_bridge_executions_connected` vivo por cuenta/host; latencia de ingesta al segundo |
| G10 cambios | PASS | Repo sin commits desde 27-sep; `origin/master` sin mover (`372af59a`); procesos sin reinicio desde sep25; único cambio de la ventana = owner re-habilitó AutoTrading en terminales (fix AUD-17, lado Windows) + onboarding de estrategias nuevas vía config |

## Hallazgos

- **AUD-17 (P1 del 28-sep): CERRADO.** Evidencia: gate de regresión cumplido (arriba). Owner re-habilitó AutoTrading entre el 28-sep 14:00 y el 29-sep (mt4-real copió ya el 29-sep 00:46; TTP/FTMO el 01-oct). Sin acción pendiente.
- **AUD-20 (P3 — nuevo): volumen de logs del core sigue en ~14.9M líneas / 8.7 GB por día en Loki pese a `telemetry/logs/level=WARN` en ETCD.** Evidencia: `query_loki_stats` 24 h echo-core (3 streams, 8.76 GB) con knob WARN vigente; el WARN real del día fue 1 línea ⇒ casi todo el volumen es DEBUG/INFO que no refleja el knob. Causa = hipótesis (el knob no aplica al exportador OTEL, o el proceso del 25-sep no lo recargó). Impacto: costo/retención de ARGUS y ruido en queries. **Owner:** confirmar semántica del knob para logs OTEL o bajar el nivel efectivo del core. Gate de regresión: `query_loki_stats` 24 h del core en un orden de magnitud menor tras el fix.
- **AUD-21 (P4 — nuevo): rechazo 10018 "market closed" en apertura dominical** en `80577453` (US100) mientras la reference ya cotizaba (22:00:26 UTC). Es un evento de sesión de broker distinta, no un defecto Echo; no hubo reintento (diseño sin retry en error de terminal). Monitor: si las aperturas dominicales fallan sistemáticamente en cuentas específicas, evaluar retardo de apertura o cola de reintento.
- **AUD-22 (P4 — nuevo): cuenta `80581422` archivada el 23-sep 15:33 por decisión owner** — su desconexión de ejecución (23-sep ~14:20) es consecuencia esperada, sus 2 estrategias (260104004, 250601005) siguen copiando en otras cuentas. Nota de higiene: la serie Prometheus `echo_bridge_executions_connected=0` sigue exportándose para la cuenta archivada (limpiar del scrape o filtrar).
- **AUD-23 (P4 — nuevo): listener extra `:45021` en `.71`** no presente en el baseline del 15-sep; el viewer no muestra el proceso dueño (sin root). UNKNOWN por diseño de permisos; verificación owner (`ss -tlnp` con root). Sin evidencia de riesgo (no es puerto de Echo).
- **Carry-over vigente:** AUD-02 (`4aad647b` sigue fuera de master; master intacto en `372af59a`), AUD-03 (SHA exacto de binarios `.71` — mitigado por correlación fecha-rollout + master tip), AUD-04 (lag de consumer groups Kafka PROD — sin capability), AUD-05 (alertas de silencio), AUD-14 (2 legs reliquia jun-04 sin re-chequeo), AUD-15 (reclasificado dentro de AUD-20).
- **AUD-19 (P4 del 28-sep): sin regresión** — cuentas reference siguen generando legs con tickets aunque su fila `accounts` diga INACTIVE legacy; trading no afectado.

## EVIDENCE_GAPS

Inspección directa de las terminales MT4 Windows (hosts `mt4-ttp`/`mt4-ftmo`/`mt4-real`) no ejecutada — sin capability SSH sobre esos hosts; el estado de AutoTrading se infiere de resultados físicos (tickets) y Prometheus. Lag exacto de consumer groups Kafka PROD sin capability. SHA256 exacto de binarios no legible con viewer (correlacionado por fecha de START + tip de master).

## Conclusión

Echo PROD está corriendo correctamente: procesa, decide, persiste y copia con evidencia física de broker en todas las plataformas, sin fallos críticos ni regresiones respecto de la auditoría del 28-sep; el único incidente previo (AUD-17, 4109) quedó cerrado con su gate cumplido y la copia es hoy más diversa que nunca. Los pendientes son de higiene operativa (volumen de logs, métricas de cuenta archivada, un listener extra por identificar) y quedan con owner y gate de regresión definidos.
