---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Production Operational Audit 2026-10-04]]"
  - "[[Echo — Production Operational Audit 2026-09-28]]"
  - "[[80-agents/journal/logs/2026-10-12-echo-prod-trigger-delivery-incident-audit-gates.md|change_log incidente triggers 2026-10-12]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
aliases:
  - Echo PROD operational audit 2026-10-13
  - auditoria operacional Echo PROD 13-oct
  - auditoria post migracion MT5 Echo PROD
tags:
  - kind/doc
  - area/echo
  - action/audit
created: "2026-10-13"
updated: "2026-10-13"
---

# Echo — Production Operational Audit 2026-10-13

## Propósito

Auditoría de regresión read-only disparada por el owner: *"veo muy pocas operaciones abiertas, ayer arreglé un par de cagazos pero no estoy seguro si todo quedó fino"*. Ejecutada 2026-10-13 ~16:04–16:20 UTC (martes, mercados abiertos). La ventana de cambios auditada es el 2026-10-11/12: el incidente de event triggers PROD sin header `Authorization` (401 silencioso, arreglado por owner con headers + redeliver) y la migración TTP MT4→MT5 (cuentas MT4 archivadas como `[MIGRATED MT5]`, nuevas cuentas MT5 `504xxxxx`, purga de zombies del topic). Primera auditoría tras la incorporación de los gates G11/G12 a la skill. Capacidades usadas: `aranea-ssh` (`echo-runtime-prod`), `aranea-postgres-ro`, `aranea-hasura-prod-ro`, `aranea-etcd-ro`, Loki/Prometheus (`aranea-observability-ro`). Regresión contra [[Echo — Production Operational Audit 2026-10-04]] (`OPERATIONAL_PASS`) y el change_log del incidente 2026-10-12.

**Veredicto: `OPERATIONAL_DEGRADED`.** Los arreglos del owner quedaron finos: la cadena config-flow vuelve a entregar (demostrado funcionalmente), la flota migrada 17/17 late y la copia E2E fluye con tickets reales. La pregunta "pocas operaciones" se explica por config vigente, no por los fixes. La degradación es una sola y es nueva: **TTP G5 MT5 (`504079710`) no journaliza** — tiene 3 posiciones vivas copiadas hoy sin una sola fila en `trade_journal`, por lo que Echo no podrá cerrarlas activamente cuando el master cierre.

## Respuesta directa a "muy pocas operaciones abiertas"

Hay 10 posiciones abiertas en 6 cuentas, que corresponden a los 4 trades que el master mantiene abiertos y que están habilitados para copiar. El master (`2089126830` scalpa + `2089125533` NDX + `2089125371` GDAXI) tiene 6 posiciones abiertas: 4 se copiaron y 2 no pueden copiarse por config vigente. La copia parcial es el patrón histórico por diseño: en 7 días el master abrió ~60 señales USDJPY y sólo ~15 generaron legs EXECUTION (whitelist chica + sizing, ver AUD-18/26/27). No hay efecto de los fixes de ayer en el volumen: el mismo patrón existe antes y después del 12-oct.

## Cadena de evidencia (traza 2026-10-13 14:00 UTC, trade_id `01a13635-b1b8…`, magic `260104004`)

1. **Señal viva:** leg REFERENCE en master `2089126830` 14:00:52 — ticket `270402822` (USDJPY BUY 0.70).
2. **Planner correcto:** acepta 4 targets y rechaza con WARN correcto 2 cuentas `ARCHIVED` (`26221863`, `80581422` — "intent rejected by account state").
3. **Copia física:** 4 legs EXECUTION creadas 14:00:58 (6 s) con tickets reales: WSF 2X1 `138189` 3.14 lots (broker symbol `USDJPYC`), FTMO Full XAU `431019411` 1.57, Orion NEWGEN `80570850` 1.57, Orion Instant `80575718` 0.51.
4. **Snapshots fluyendo:** `snapshot_at` de `active_positions` fresco al minuto (19:04 hora broker para cuentas TTP/FTMO, 16:04 para Orion — offsets UTC+3 correctos).
5. **Cierres fluyendo:** 55 filas CLOSED en 72 h; **0 FAILED en 72 h** (AUD-17/4109 se mantiene cerrado).

Los 3 trades NDX de hoy (06:00, 07:00, 11:00 UTC, magics del master NDX `2089125533`) se copiaron a FTMO portfolio `431007281` (MT4) y TTP G5 `504079710` (MT5, tickets `18893127`/`18894146`/`18898488`).

## Config-flow post-fix (G11)

- **Entrega demostrada:** el gateway publicó ClientConfigs a Kafka vía trigger `accounts_config` en 72 eventos/48 h; la última ola completa (todas las cuentas ACTIVE) fue **anoche 23:21 UTC**, dentro de la ventana de fixes del owner — los triggers vuelven a entregar tras el 401 silencioso.
- **Serve funcional:** las 17 cuentas laten <1 min y operan con `allowed_symbols` ya transformados a nombres de broker existentes (`USDJPYC`/WSF, `USTEC`/TTP, `US100CASH`/FTMO, `NDX` en journal) — el cache del bridge y los EAs están recibiendo.
- **Cero errores de bridge:** `{service_name="echo-bridge", level="ERROR"}` = 0 entradas en 3 h (no hay `Symbol not available` ni `feed_count=0` residuales del incidente).
- **ETCD:** `/echo/production/` = 37 keys, sin cambio vs baseline 28-sep (config de infra estable).
- `hdb_catalog.event_log` sin lectura owner/admin = EVIDENCE_GAP estructural (ver gaps).

## Flota tras la migración MT4→MT5

17 cuentas ACTIVE (todas `execution_agent`): 3 MT4 (`80577453` Orion 2NDX1XAU!, `431007281` FTMO portfolio!, `3094610` Axi Select!) + 14 MT5 (TTP G1–G5 + ADX,Vortex `504xxxxx`, Orion `805xxxxx`, WSF `138189`/`183623`). Las 17 con latido de segundos y terminal conectada en Prometheus (17/17); la serie extra `echo_bridge_executions_connected=0` es `80581422`, cuenta archivada fuera de flota (higiene métrica, ya listada como pendiente P3 del 04-oct). Las viejas cuentas MT4 de TTP figuran `ARCHIVED` renombradas `[MIGRATED MT5]` y el planner las excluye correctamente (WARN "account state does not accept opens" = exclusión correcta, no error).

## Gates

| Gate | Estado | Justificación |
|---|---|---|
| G1 runtime | PASS | Host `echo`, usuario `echo-dev`; core (`441462`), gateway (`442685`), functions (`441170`), nginx, promtail vivos; 0 `echo-bridge` en `.71` (normal, corren en Windows) |
| G2 identidad | PASS | Binarios `/home/kor/echo/*` con arranques 25-sep (sin reinicio); `service.version=2.0.0` en producción; SHA exacto UNKNOWN declarado (viewer) |
| G3 config | PASS | ETCD `/echo/production/` = 37 keys (sin mutación vs baseline); telemetría `env=production`; sin filtración DEV observada |
| G4 servicios | PASS | PG `echo` con 5 backends app; Hasura v2.38.0; metadata consistente (0 inconsistentes); etcd/ARGUS consultados OK |
| G5 transporte | PASS | Traza REF→EXEC en 6 s con tickets en 4 brokers; 17/17 terminales conectadas; snapshots al minuto |
| G6 datos | PASS | Journal al segundo del evento; 0 duplicados `(trade_id, account_id)`; 0 FAILED/72 h |
| G7 consistencia | **DEGRADED** | 10 `active_positions` vs 15 legs OPEN: 3 posiciones de TTP G5 **sin legs en journal** (AUD-24, nuevo) + 2 legs reliquia jun-04 en cuentas ARCHIVED (AUD-28, carry-over AUD-14) |
| G8 trading | PASS | E2E completo con tickets reales hoy; copia parcial = config vigente demostrada (AUD-26/27); exclusiones correctas; 0 FAILED |
| G9 observabilidad | PASS | Loki/Prometheus vivos; WARNs discriminables por label; core WARN = ruido benigno conocido (close_handler sin legs + exclusiones ARCHIVED); bridge ERROR 0/3 h |
| G10 cambios | PASS | 0 commits desde 11-oct (`origin/master@372af59a`, mismo del rollout 25-sep); fixes de la ventana = config/infra, sin despliegue |
| G11 config-flow | PASS (con gap) | Entrega demostrada (72 ClientConfig/48 h, última ola post-fix anoche 23:21 UTC); serve funcional; bridge 0 errores; `hdb_catalog` sin permiso RO = EVIDENCE_GAP; hallazgo AUD-25 |
| G12 estado | PASS (con hallazgos) | 17/17 ACTIVE con latido de segundos; cobertura `client_allowed_symbols`→`symbol_mappings` = 0 gaps en las 17; policies muertas documentadas (AUD-26/27/28); zombies de topic sin verificación directa = EVIDENCE_GAP |

## Hallazgos

- **AUD-24 (P1 — nuevo): TTP G5 MT5 (`504079710`) no journaliza.** Evidencia: 3 tickets vivos en `active_positions` (`18893127`/`18894146`/`18898488`, USTEC BUY 0.15, abiertos hoy 09:00/10:00/14:00 UTC, con SL/TP en broker) con **cero filas** en `trade_journal`: ni por `account_id` (la cuenta no tiene historia en toda la tabla) ni por ticket global. Sus gemelas de los mismos trades sí journalizan (FTMO portfolio `431007281`). Es la primera cuenta MT5 migrada que copió trades y el defecto se vuelve visible ahora. **Impacto:** cuando el master cierre esos trades, el `close_handler` no encontrará legs para G5 (patrón `NO_OPEN_POSITIONS` ya visible en WARNs) y las posiciones quedarán abiertas hasta que el broker las cierre por TP/SL estático — la gestión activa (SL dinámico, cierre al cierre del master) no aplicará; PnL/riesgo de la cuenta no auditables. **Causa: hipótesis** (wiring de la cuenta nueva en el path de journal del core/bridge; verificar cómo se registraron las 504xxxxx vs las Orion/WSF MT5 que sí journalizan). **Owner:** investigar antes del próximo cierre del master NDX; gate de regresión: próximo trade copiado a `504079710` ⇒ fila EXECUTION en journal con ticket≠0.
- **AUD-25 (P2 — reconfirmado/agravado): el fix de triggers vive sólo en metadata viva.** El repo `v3/hasura/metadata/` no declara `event_triggers` (deuda documentada del rollout 25-sep: "un `metadata apply` directo los borraría") ni el header `Authorization` reparado ayer (grep 0 matches en todo el árbol). Un apply futuro desde el repo reproduciría el incidente del 12-oct en su modalidad más grave: sin triggers, `feed_count=0` silencioso con G1–G10 verdes. **Owner:** persistir triggers+header en `v3/hasura/` (o blindar el runbook de apply como merge aditivo sin metadata de triggers).
- **AUD-26 (P3 — nuevo, familia AUD-18): `magic_260104001` sin ninguna policy.** Estrategia activa del master scalpa (`2089126830`): su señal de hoy 15:01 (USDJPY BUY 0.80, trade `01a1366d`) quedó reference-only con WARN `NO_EXECUTION_POLICIES` (0 filas en `account_strategy_risk_policy`). Decisión owner: darle targets o aceptarla reference-only.
- **AUD-27 (P3 — carry-over AUD-10/18 refinado): DAX/GDAXI sigue sin camino vivo.** El master GDAXI emite canonical `GDAXI` (magic `251002035`, trade `01a13145` abierto ayer 15:00, sigue OPEN sin copiar); sus 2 policies apuntan ambas a cuentas ARCHIVED (`2089126183`/`2089126186`, rechazo "account state" en logs); los mappings tienen el par DAX activo para 6 brokers bajo canonical `DAX`. En toda la historia del journal hay **0 legs EXECUTION** con canonical GDAXI o DAX. No es regresión de la ventana.
- **AUD-28 (P4 — carry-over AUD-14): legs reliquia jun-04.** Los 2 legs OPEN del 4-jun viven en cuentas hoy ARCHIVED por la migración: `442688` `[MIGRATED MT5] TTP G5!` (ticket `26790522` NDX 0.01) y `802591` `TTP G4!` (ticket `26790904` USDJPY 1.4). Residuo contable que infla la inconsistencia journal↔posiciones; no afecta trading. Limpieza owner con backup (mismo tratamiento que las fantasmas del 25-sep).
- **Positivos de regresión:** AUD-17 (4109) se mantiene cerrado (0 FAILED/72 h); el incidente de triggers quedó reparado y entregando; AUD-19 (masters INACTIVE con legs REF) persiste benigno; AUD-18 mejoró con la migración (hoy hay 6 estrategias con targets vivos vs 1 el 28-sep).

## EVIDENCE_GAPS

`hdb_catalog.event_log`/`event_invocation_logs` sin permiso del perfil RO (la entrega se demostró funcionalmente, no por lectura de la cola). Lectura directa del topic compactado y lag de consumer groups Kafka PROD (sin capability; los zombies post-purga no se verificaron en el topic). Causa raíz de AUD-24 (requiere inspección de código/config del core o logs de ejecución del bridge TTP). SHA de binarios en `.71` (viewer no lee `/home/kor/echo`). Inspección directa de terminales Windows (nunca se ejecuta desde esta auditoría).

## Conclusión

Los arreglos del 12-oct quedaron finos: triggers entregando (demostrado con la ola de ClientConfig post-fix), flota migrada 17/17 operando, copia E2E con tickets reales y cero fallos de ejecución. Las "pocas operaciones abiertas" son el estado correcto del sistema bajo la config vigente (master con 4 señales copiables + 2 estrategias sin camino de copia: AUD-26/27). El único defecto nuevo es AUD-24 (journal ciego para TTP G5) y tiene una ventana de riesgo concreta: el próximo cierre del master NDX dejaría 3 posiciones de G5 sin gestión activa — tratar hoy.
