---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Production Operational Audit 2026-09-27]]"
  - "[[Echo — Production Operational Audit 2026-09-22]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
aliases:
  - Echo PROD operational audit 2026-09-28
  - auditoria operacional Echo PROD 28-sep
  - revisión 0 operaciones Echo PROD
tags:
  - kind/doc
  - area/echo
  - action/audit
created: "2026-09-28"
updated: "2026-09-28"
---

# Echo — Production Operational Audit 2026-09-28

## Propósito

Auditoría de regresión read-only disparada por el owner: *"Echo PROD tiene 0 operaciones"*. Ejecutada 2026-09-28 ~14:25–14:40 UTC (lunes, mercados abiertos desde el domingo por la noche). Sin capability `aranea-ssh` (variante telemetría, igual que 09-22 y 09-27). Regresión contra [[Echo — Production Operational Audit 2026-09-27]].

**Veredicto: `OPERATIONAL_DEGRADED`.** El pipeline E2E está íntegro y vivo (journal al segundo, bridges con heartbeat, Lab 861 corridas/24 h, ETCD/PG sanos). La degradación es una sola y es de trading: **la copia a cuentas de ejecución está bloqueada en las terminales MT4** — los 2 únicos targets viables de hoy rechazaron las 4 órdenes con **error 4109 "trade not allowed"** (= AutoTrading / permiso de trading deshabilitado en el terminal, lado Windows, fuera de Echo). Por eso hay 0 posiciones abiertas y no se abren nuevas.

## Respuesta directa a "0 operaciones"

La vista **Operaciones** del front V3 (`OperationsView.vue`, RFC-004) es la vista de **posiciones ABIERTAS** (Panic Close): lee `getActivePositions` + subscription. Muestra 0 porque `echo.active_positions` tiene 0 filas: no queda nada abierto desde el 24-sep y **hoy nada nuevo pudo abrirse** (los 4 intentos de copia rebotaron en el terminal). No es un defecto del front ni del modelo V3: el dato es correcto; lo anómalo es la causa.

## Cadena de evidencia (traza 2026-09-28 14:00 UTC, trade_id `01a0e8f5-8680…`)

1. **Señal viva:** strategy `magic_250901045` (NDX) abre en cuenta reference `2089125533` 14:00:01 — ticket `269855669` (leg REFERENCE con ticket real).
2. **Planner correcto:** `execution_planner` intenta los 3 targets del whitelist — `418302` rechazado por estado `ARCHIVED` (WARN correcto, "intent rejected by account state"), `442688` y `431007281` aceptados.
3. **Core→Kafka→bridge→EA OK:** `Processing CoreCommand` → `Command sent to Execution EA` (delivery 612 µs) en `bridge-mt4-ttp` (442688) y `bridge-mt4-ftmo` (431007281).
4. **El terminal MT4 rechaza:** `ExecutionResult received from Execution EA: [OPEN_FAILED]`, `error_code 4109`, `"Unknown error 4109"` → journal `FAILED`, ticket 0. Core registra `execution_store: [OPEN_FAILED] … failed on EA`.
5. **Journal persiste al segundo:** 4 FAILED hoy (13:00 y 14:00 UTC, 2 cuentas × 2 señales) + 12 REFERENCE con tickets + cierres con PnL (`profit_net` persistido).

El fallo nace **en el terminal MT4 del host Windows** (ambos hosts: `mt4-ttp` y `mt4-ftmo`), no en Echo. 4109 en MQL4 = `ERR_TRADE_NOT_ALLOWED`: botón AutoTrading off, "Allow Algo Trading" desmarcado en el EA, o sesión read-only (password investor). Dos brokers distintos fallando a la vez sugiere un evento común de fin de semana (restart de terminales con autotrading apagado o actualización de MT4) — **causa exacta en terminal = EVIDENCE_GAP** (sin capability sobre los hosts Windows).

## Trading hoy (journal, ventana 36 h)

- **Última copia exitosa: 24-sep 13:00 UTC** (6 legs con ticket). 25–27 sep sin intentos EXECUTION (señales sin targets vivos + fin de semana).
- **Hoy lunes:** 4 intentos EXECUTION, **4 FAILED** (4109, ticket 0). 12 REFERENCE con tickets (GDAXI/NDX en `2089125371`/`2089125533`), cierres con PnL neto persistido.
- `active_positions` = 0 (estado real: sin exposición en cuentas Echo).

## Gates

| Gate | Estado | Justificación |
|---|---|---|
| G1/G2 runtime | DEGRADED (carry-over) | Sin SSH: PIDs/SHA `.71` no verificables; telemetría muestra core+bridges vivos (accounts heartbeat <1 min, `service.version` 2.0.0) |
| G3 config | PASS | ETCD `/echo/production/` = 37 keys (32 baseline + 5 del rollout 25-sep); sin señales de mutación |
| G4 servicios | PASS | PG `echo` con 5 backends app vivos; Hasura/etcd responden; Lab 861 corridas/24 h, última 14:30 UTC |
| G5 transporte | PASS | Journal al segundo del evento; comandos entregados al EA en <1 ms; snapshots de cuenta/instrumento fluyendo |
| G6 datos | PASS | Duplicados no re-chequeados (sin señal); consistencia journal↔estados correcta; FAILED bien tipificados |
| G7/G8 trading | **DEGRADED** | Copia bloqueada por 4109 en los 2 targets vivos; reference fluyendo con tickets |
| G9 observabilidad | PASS | Loki level-labels operativos; WARNs del core discriminables; misma latencia de ingesta |
| G10 cambios | NOT_APPLICABLE | Sin despliegues ni cambios Echo desde la auditoría 27-sep; el 4109 es config de terminal, no código |

## Hallazgos

- **AUD-17 (P1 — nuevo): copia EXECUTION bloqueada por 4109 en terminales.** Evidencia: traza completa arriba; 4 FAILED hoy; precedentes del mismo patrón en `442688`/`431007281` el **14–15 sep** (auto-recuperado: 18–24 sep copiaron bien) y clusters aislados 10-ago y 25-jun. Causa demostrada a nivel sistema (rechazo en terminal); causa exacta en terminal = EVIDENCE_GAP. **Owner:** re-habilitar AutoTrading / "Allow Algo Trading" del EA en las terminales MT4 de `442688` (TTP G5, host `mt4-ttp`) y `431007281` (FTMO portfolio, host `mt4-ftmo`) y verificar que el botón no se apague en restarts. **Gate de regresión:** próximo disparo de `magic_250901045` ⇒ ≥1 leg con ticket≠0 en CADA una de las dos cuentas.
- **AUD-18 (P2 — nuevo): la whitelist de copia viva depende de una sola estrategia.** De 13 estrategias con policies, 12 apuntan sólo a cuentas ARCHIVED (`2089126183`, `2089126186`, `418302`); sólo `250901045` (NDX) tenía targets vivos hoy — y ambos cayeron al 4109 ⇒ 0 camino de copia operativo. `251002014` (DAX, gate AUD-10) tiene 8 targets de los cuales 4 vivas (`183623` WSF NEW!, `431019411` FTMO Full XAU!, `80570850`/`80575718` Orion). Owner: decidir si se re-vinculan estrategias a cuentas activas o se acepta el status quo.
- **AUD-19 (P4 — nuevo): cuentas reference con fila `accounts` muerta.** `2089125371`/`2089125533`/`2089125306` figuran `INACTIVE` con `updated_at` 2025-12-23, pero generan legs REFERENCE con tickets hoy. Causa = hipótesis (snapshots de `accounts` sólo para execution accounts; estado INACTIVE legacy). Impacto: vistas de cuentas del front pueden mostrarlas mal; trading no afectado.
- **Carry-over vigente:** AUD-10 gate DAX **sigue abierto** (magic `251002014` no disparó; las señales GDAXI de hoy fueron de otras magics y todas sus cuentas whitelist están ARCHIVED — el planner las excluyó correctamente, sin errores `mm_engine`); AUD-02 (`4aad647b` fuera de master), AUD-03 (sin SSH: SHA de binarios `.71`), AUD-04 (lag Kafka PROD — sin capability), AUD-05 (alertas de silencio), AUD-14 (2 legs reliquia jun-04, sin re-chequeo hoy), AUD-15 (knob WARN vs DEBUG efectivo).

## EVIDENCE_GAPS

Sin SSH: procesos/listeners/SHA de `.71`. Sin capability Windows: settings de AutoTrading en las terminales MT4 (causa exacta del 4109), lag de consumer groups Kafka PROD. Inspección directa de terminales no ejecutada (nunca se hace desde esta auditoría).

## Conclusión

El sistema procesa, persiste y decide correctamente; lo que falla es el último paso físico (permiso de trading en 2 terminales MT4) y, estructuralmente, la whitelist de copia tiene un único camino vivo. Con AUD-17 corregido, la copia debería recuperar el comportamiento del 22–24 sep sin tocar nada de Echo.
