---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Production Operational Audit 2026-10-13]]"
  - "[[Echo — Production Operational Audit 2026-10-04]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
aliases:
  - Echo PROD operational audit 2026-10-14
  - auditoria operacional Echo PROD 14-oct
tags:
  - kind/doc
  - area/echo
  - action/audit
created: "2026-10-14"
updated: "2026-10-14"
---

# Echo — Production Operational Audit 2026-10-14

## Propósito

Auditoría de regresión read-only solicitada por el owner ("necesito validar que todo esté corriendo perfectamente"). Ejecutada 2026-10-14 ~23:16–23:30 UTC (miércoles, mercados abiertos). Ventana auditada: desde la auditoría del 13-oct 16:20 UTC (~31 h). Regresión contra [[Echo — Production Operational Audit 2026-10-13]] (`OPERATIONAL_DEGRADED` por AUD-24). Capacidades usadas: `aranea-ssh` (`echo-runtime-prod`), `aranea-postgres-ro`, `aranea-hasura-prod-ro`, `aranea-etcd-ro`, Loki/Prometheus (`aranea-observability-ro`). Nota de método: las primeras lecturas SSH de la sesión cayeron en el profile default (`sqx-zeus`, flota Forge, sin procesos Echo, lectura inofensiva); todo el gate G1 en adelante se ejecutó con el profile explícito `echo-runtime-prod`.

**Veredicto: `OPERATIONAL_DEGRADED`.** El sistema opera correctamente end-to-end hoy: copia E2E con tickets reales en segundos, 17/17 terminales conectadas, 0 FAILED en 96 h, 0 ERROR en core y bridge, config-flow entregando. La degradación es una sola y es la misma de ayer, ahora latente: **AUD-24 sigue demostrado (TTP G5 `504079710` con 0 filas en `trade_journal` en toda la historia) y sin causa demostrada**. El riesgo concreto del 13-oct se disolvió por cierre de las posiciones en broker (no por remedio), y el gate de regresión de AUD-24 (próxima copia a G5 ⇒ fila en journal) sigue sin poder ejercitarse porque en la ventana no se copió ningún trade a G5.

## Respuesta directa: "¿todo corriendo perfectamente?"

Casi. Todo lo que el sistema estaba haciendo hoy lo hizo bien (ver gates: 11 PASS + 0 FAIL). Lo que no está perfecto: el defecto AUD-24 no está reparado — la cuenta TTP G5 sigue fuera del journal, así que la próxima señal que se le copie volverá a quedar sin gestión activa (SL dinámico/cierre al cierre del master) y sin auditoría de PnL. Las 3 posiciones huérfanas de ayer ya no existen: cerraron en broker (equity=balance en el latido fresco de hoy, terminal conectada), pero Echo no participó en ese cierre porque no tenía legs que cerrar.

## Cadena de evidencia (traza 2026-10-14 10:00 UTC, trade_id `01a13a80-01b0…`, master scalpa `2089126830`)

1. **Señal viva:** leg REFERENCE USDJPY BUY 1.13 abierta 10:00:31, ticket `270462686`.
2. **Copia física:** 3 legs EXECUTION creadas 10:00:32–33 (1–2 s) con tickets reales: Orion NEWGEN `80570850` 1.99 lots ticket `63936572`, Orion Instant `80575718` 0.62 ticket `63936573`, FTMO Full XAU `431019411` 1.99 ticket `49605636`.
3. **Cierres fluyendo con PnL:** copias cerradas 11:49 (−36.85 / −8.74) y 14:49 (−52.95); master cerrado 20:25:40 (+93.43) — ciclo completo journalizado hoy.
4. **Volumen del día:** 14 legs EXECUTION CLOSED + 31 REFERENCE CLOSED + 1 REFERENCE OPEN; 0 FAILED en 96 h (AUD-17/4109 se mantiene cerrado).
5. **Latidos:** 17 cuentas ACTIVE con `updated_at` al segundo (última 23:19:09); `lab_job_runs` con 1.724 corridas en 48 h y la última a 23:22:35 (lab-worker vivo; coincide con el proceso `recompute --triggered-by SCHEDULED` visto en `ps aux`).

## Estado de AUD-24 (la única degradación)

Re-verificado hoy 23:20 UTC: `SELECT count(*) FROM echo.trade_journal WHERE account_id='504079710'` = **0 filas** (toda la tabla). La cuenta late fresco (23:19:09), está `ACTIVE` con 6 policies y conectada en Prometheus (`echo_bridge_executions_connected=1` en `mt4-ttp`). En 48 h **no recibió ninguna copia nueva** (0 legs EXECUTION), así que el gate de regresión definido el 13-oct (próxima copia ⇒ fila con ticket≠0) no se pudo ejercitar. Las 3 posiciones huérfanas de ayer (`18893127`/`18894146`/`18898488`, USTEC) ya no están en `active_positions` y la cuenta no muestra PnL flotante: cerraron en broker fuera de Echo (vía TP/SL estático o intervención owner manual — indistinguible sin logs del terminal, gap documentado). Mientras AUD-24 no se repare, cada copia futura a G5 replica el patrón: posición viva sin legs, sin gestión activa y sin PnL auditable.

## Gates

| Gate | Estado | Justificación |
|---|---|---|
| G1 runtime | PASS | Host `echo`, uid `echo-dev`; core (`441462`), gateway (`442685`), functions (`441170`), nginx, promtail vivos; listeners 80/9080/9090/8080/8090 + `:45021` (AUD-23 carry-over, benigno conocido); 0 `echo-bridge` en `.71` (normal, corren en Windows) |
| G2 identidad | PASS | Binarios `/home/kor/echo/*` con arranques 25-sep (PIDs idénticos al 13-oct = sin reinicios); `service.version=2.0.0` y `deployment.environment=production` en logs; SHA exacto UNKNOWN declarado (viewer no lee `/home/kor/echo`) |
| G3 config | PASS | ETCD `/echo/production/` = 37 keys (estable vs baseline); valores contrastados: Kafka `.247-.249:9092`, gateway core `localhost:9090`; sin filtración DEV observada |
| G4 servicios | PASS | PG `echo` con 6 backends app; Hasura v2.38.0 con metadata consistente (0 inconsistentes); etcd/Loki/Prometheus consultados OK (un rebote transitorio del pool del MCP PG fue del lado cliente, no del sistema) |
| G5 transporte | PASS | Traza REF→3 EXEC en 1–2 s con tickets reales hoy; cierres con PnL journalizados; 17/17 terminales conectadas (Prometheus, la única serie en 0 es la archivada `80581422`); snapshots/latidos al segundo |
| G6 datos | PASS | Journal al segundo del evento; 0 duplicados `(trade_id, account_id)`; 0 FAILED en 96 h |
| G7 consistencia | PASS (mejoró vs 13-oct) | 0 `active_positions` vs 3 legs OPEN en journal: 1 REF viva (los masters INACTIVE no snapshot-ean posiciones, patrón conocido) + 2 reliquia jun-04 (AUD-28 pendiente). Las 3 divergencias de G5 del 13-oct desaparecieron (cierre en broker). Sin divergencias nuevas |
| G8 trading | PASS | E2E completo hoy con tickets y PnL; exclusiones del planner correctas (WARNs trazan 1:1 a Slaves ARCHIVED); trades nativos de Axi journalizan con ticket≠0; 0 FAILED |
| G9 observabilidad | PASS | Core: 0 ERROR / 4 WARN en 3 h (todas exclusiones correctas del trade XAUUSD, verificadas por label `level`); bridge: 0 WARN + 0 ERROR en 3 h; gateway en silencio event-driven normal (34 líneas/24 h) |
| G10 cambios | PASS | 0 commits en el repo desde el 13-oct (`origin/master@372af59a`, mismo del rollout 25-sep); ETCD sin mutación; único delta de la ventana = cierre en broker de las 3 posiciones G5 (efecto de mercado/owner, no código). Adyacente sin impacto: flota Forge arrancó worker Symphony 0.2.138 en `sqx-zeus` hoy 13:21 (otro producto, sin procesos Echo) |
| G11 config-flow | PASS (con gaps estructurales) | Entrega demostrada hoy: trigger `accounts_config` publicó ClientConfigs a Kafka (última ola completa 13:31 UTC, 34 eventos/24 h); serve funcional (símbolos ya transformados operando, 17/17 conectadas); `hdb_catalog.event_log` sin permiso RO = EVIDENCE_GAP; AUD-25 vigente = riesgo latente |
| G12 estado | PASS (con hallazgos) | 17/17 ACTIVE con latido de segundos; cobertura `client_allowed_symbols`→`symbol_mappings` = 0 gaps; 1 cuenta ciega nueva documentada (AUD-29); 305 policies muertas hacia ARCHIVED/INACTIVE (peso muerto conocido); zombies de topic sin verificación directa = EVIDENCE_GAP (sin Kafka PROD) |

## Hallazgos

- **AUD-24 (P1 — VIGENTE, ahora latente): TTP G5 MT5 (`504079710`) sigue sin journalizar.** 0 filas all-time re-verificado; causa sigue en hipótesis (wiring de la cuenta en el path de journal del core/bridge para cuentas 504xxxxx). El riesgo puntual del 13-oct se disolvió por cierre en broker de las 3 posiciones, no por remedio; el gate de regresión sigue sin ejercitar (0 copias a G5 en la ventana). **Owner:** investigar antes de que el master NDX vuelva a copiar a G5; cada copia mientras tanto nace huérfana.
- **AUD-25 (P2 — VIGENTE): el fix de triggers vive sólo en metadata viva.** Re-verificado hoy: `v3/hasura/` sin `event_triggers` ni header `Authorization` (grep 0 matches; 0 commits desde el 13-oct). Un apply futuro desde el repo reproduciría el incidente del 12-oct. **Owner:** persistir triggers+header en el repo o blindar el runbook de apply.
- **AUD-26 (P3 — VIGENTE): `magic_260104001` sigue sin ninguna policy** (0 filas); sus señales siguen reference-only por defecto de config, no por decisión demostrada.
- **AUD-27 (P3 — VIGENTE y extendido): estrategias con camino de copia muerto.** GDAXI (`magic_251002035`) sigue con sus 2 policies hacia Slaves ARCHIVED. Extensión de hoy: la estrategia XAU del master `2089125306` (`magic_250901015`) tiene el mismo patrón — su trade XAUUSD BUY 0.10 de 22:01 (ticket `270492778`) sigue OPEN sin copiar porque sus 2 policies apuntan a `2089126183`/`2089126186` (ARCHIVED; WARNs "intent rejected by account state" correctas en core). Mismo tratamiento owner: dar targets o aceptar reference-only.
- **AUD-28 (P4 — VIGENTE): legs reliquia jun-04** (`802591` ticket `26790904` y `442688` ticket `26790522`) siguen OPEN en journal en cuentas hoy ARCHIVED; residuo contable, limpieza owner pendiente.
- **AUD-29 (P3 — NUEVO): Axi Select (`3094610`) es cuenta ciega.** ACTIVE execution_agent con 0 filas en `account_strategy_risk_policy`: jamás recibirá copias. Opera nativa y sus 4 trades de hoy journalizan bien (ticket≠0, PnL). Puede ser diseño (cuenta native-only); requiere decisión owner explícita para dejar de tratarla como hallazgo.
- **Positivos de regresión:** AUD-17 (4109) se mantiene cerrado (0 FAILED/96 h); el incidente de triggers sigue reparado (publicación funcional hoy 13:31 UTC); AUD-19 (masters INACTIVE journalizando) persiste benigno; AUD-23 (listener `:45021`) persiste benigno conocido; la flota 17/17 estable y el patrón de copia parcial (whitelist chica) se mantiene como diseño.

## EVIDENCE_GAPS

`hdb_catalog.event_log`/`event_invocation_logs` sin permiso del perfil RO (la entrega se demostró funcionalmente por logs del gateway). Lectura directa del topic compactado, lag de consumer groups y zombies post-purga en Kafka PROD (sin capability). Causa raíz de AUD-24 (requiere inspección de código/config del core o logs del terminal TTP). SHA de binarios en `.71` (viewer). Cierre de las 3 posiciones G5 (manual owner vs TP/SL, indistinguible sin logs del terminal). Inspección directa de terminales Windows (nunca se ejecuta desde esta auditoría).

## Conclusión

Echo PROD hoy está operando limpio de punta a punta: la copia E2E cerró su ciclo completo (señal→copias en segundos→cierres→PnL) con tickets reales, las 17 terminales laten, el config-flow entrega y no hay errores en ningún servicio. No es `OPERATIONAL_PASS` por una sola razón, la misma de ayer: AUD-24 sigue demostrado y sin causa. La diferencia con ayer es que ya no hay exposición viva — las 3 posiciones huérfanas cerraron en broker — así que la degradación es latente y condicional: se materializa en la próxima copia a TTP G5. La acción owner con fecha límite implícita sigue siendo la misma: reparar (o al menos diagnosticar) el journal de las cuentas 504xxxxx antes del próximo trade copiado a G5, y de paso decidir AUD-26/27/29 (targets o reference-only explícito para scalpa/XAU/GDAXI/Axi).
