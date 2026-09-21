---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[Echo — Access & Physical Capability Matrix]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
aliases:
  - Echo PROD operational audit 2026-09-21
  - Auditoría operacional Echo PROD
tags:
  - kind/doc
  - area/echo
  - action/audit
created: "2026-09-21"
updated: "2026-09-21"
---

# Echo — Production Operational Audit 2026-09-21

## Propósito

Auditoría operacional E2E read-only de Echo PROD tras la ventana de cambios del fin de semana 2026-09-18…21 (America/Santiago), ejecutada 2026-09-21 ~13:40–14:00 UTC. Evalúa funcionamiento real (no health checks) sobre evidencia física y persistencia, correlaciona los cambios del fin de semana y deja el camino reproducible en la skill [[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]. Auditoría estrictamente read-only: cero órdenes, cero mutaciones, cero reinicios; acceso por capacidades RO vigentes ([[aranea-mcps-expert]]).

**Veredicto: `OPERATIONAL_DEGRADED`.** El flujo crítico de trading (bridge → Kafka → core → copia → journal → Lab) funciona y fue demostrado con operaciones reales del día, pero el pipeline Lab (echo-lab-worker) estuvo silencioso 66+ h en la ventana (viernes completo + fin de semana) con un segundo gap el lunes, sin filas de error ni logs, y la causa exacta de los gaps no está demostrada con evidencia RO.

## Contenido

### A. Resumen ejecutivo

Echo PROD está arriba y operando: los tres procesos server (`echo-core`, `echo-gateway`, `echo-functions`) corren sin reinicios desde hace semanas en el host `192.168.31.71`, con PostgreSQL conectado (6 backends vivos), Kafka PROD fluyendo (latencia evento→persistencia 1–2 s) y 18 terminales de ejecución conectadas vía 3 bridges Windows (`mt4-ttp`, `mt4-ftmo`, `mt4-real`). El día de la auditoría se trazó una copia completa Reference→2 ejecuciones con tickets físicos de broker y exclusión correcta de cuentas ARCHIVED. La copia de eventos del fin de semana fue exclusivamente en DEV (branches E-08/E-09/E-04 + despliegues Daedalus); `origin/master` no cambió desde 2026-09-16 y no hubo ningún despliegue ni reinicio en PROD. Dos incidentes de config del fin de semana (sobrescritura de la password ETCD de producción por seed tests, documentada en el contrato §5.5/§5.6) tocaron el namespace PROD: esta auditoría verifica con evidencia fresca que la password ya funciona (auth PG exitosa vía ETCD a las 13:10–13:56 UTC), pero el pipeline Lab guardó silencio 66+ h sin que ningún mecanismo lo reportara. Ninguna operación perdida, duplicada o huérfana fue detectada en la ventana.

### B. Fecha, ventana y ambiente verificado

- Ejecución: 2026-09-21, 13:40–14:00 UTC (10:40–11:00 CLT).
- Ventana de cambios auditada: 2026-09-18 00:00 → 2026-09-21 14:00 UTC (America/Santiago).
- Ambiente: **PROD** (`/echo/production/` ETCD namespace; `deployment.environment=production` en toda la telemetría observada). DEV (Daedalus) se menciona sólo como correlación de cambios, nunca como objetivo de verificación de PROD.

### C. Inventario real (G1)

| Componente | Host | Servicio / proceso | Ambiente | Build / versión observada | Estado |
|---|---|---|---|---|---|
| Echo Core | 192.168.31.71 (`echo`) | `echo-core` PID 110701, user `kor`, desde 2026-08-20 | PROD | `/home/kor/echo/echo-core`, service.version 2.0.0 (OTEL); SHA UNKNOWN (ver AUD-03) | RUNNING, CPU ~5% |
| Echo Gateway | 192.168.31.71 | `echo-gateway` PID 713, desde 2026-08-09 | PROD | `/home/kor/echo/echo-gateway`, 2.0.0; SHA UNKNOWN | RUNNING, idle-event-driven |
| Echo Functions (StateFun) | 192.168.31.71 | `echo-functions` PID 320982, desde 2026-09-12 | PROD | `/home/kor/echo/echo-functions`, 2.0.0 | RUNNING (sirve `/statefun` al core) |
| Lab worker | 192.168.31.71 | `echo-lab-worker` transitorio por timer (~5 min, 3 jobs/ciclo) | PROD | code_version 0.0.1, job_version v1 | INTERMITENTE (ver AUD-01) |
| Front nginx | 192.168.31.71 | nginx master + 4 workers, :80, desde 2026-09-16 | PROD | — | RUNNING |
| Log shipper | 192.168.31.71 | promtail → Loki ARGUS, desde 2026-09-12 | PROD | — | RUNNING |
| Echo Bridge ×3 | Windows `mt4-ttp`, `mt4-ftmo`, `mt4-real` | `echo-bridge` (service_name/`echo.bridge.id`) | PROD | 2.0.0; acceso OS directo NO disponible | RUNNING, 18/18 cuentas `executions_connected=1` |
| PostgreSQL | 192.168.31.220 | PG 17.6, db `echo` (schema `echo`); DEV `echo-develop` en el mismo clúster | PROD | 17.6 | UP, 6 backends en db `echo` |
| Hasura | 192.168.31.48:8080 | Hasura CE v2.38.0 | PROD | v2.38.0 | UP, metadata consistente |
| Kafka | 192.168.31.247–249:9092 | clúster PROD (sin capability MCP certificada) | PROD | — | UP (evidencia indirecta) |
| etcd | 192.168.31.250–254:2379 | clúster, namespaces `/echo/production/` (32 keys), `/echo/development/`, `/sqx-flowkit/*`, `/deployer*`, `/symphony/` | compartido | — | UP, lectura RO OK |
| Observabilidad ARGUS | Grafana/Prometheus/Loki/Jaeger | datasources activos | PROD | — | UP (logs de hace segundos) |
| Core/Gateway DEV | 192.168.31.161 (Daedalus) | `systemd --user` (fuera del alcance PROD) | DEV | Core `5dd998f1`, Gateway `3d260e81` | RUNNING (contrato §5.1–§5.6) |

Límites del inventario: el viewer `echo-runtime-prod` no puede leer `/home/kor/echo` (permiso) ni ejecutar binarios ⇒ SHA/commit de los binarios PROD = UNKNOWN (AUD-03); los hosts Windows de los bridges no tienen perfil SSH RO dedicado; Kafka PROD no tiene capability MCP (AUD-04); listener `:45021` en .71 no identificado (P3, benigno por no coincidir con puertos Echo documentados).

### D. Diagrama del flujo operativo observado

```text
MT4 terminales (18 cuentas: 6 TTP, 2 FTMO, 10 AXI/real)
    ↓ named pipes echo_execution_<cuenta> (pipe_prefix=echo_)
echo-bridge ×3 (Windows: mt4-ttp / mt4-ftmo / mt4-real, v2.0.0)
    ↓ publica snapshots + trade events → Kafka PROD .247-249:9092
echo-core (.71:9090, consume; pool PG 5–20 conns → PG .220/echo)
    ↓ POST /statefun
echo-functions (.71, StateFun worker; functions/enabled=true)
    ↓ journal/account_sync/position_sync/automation_evaluator/execution_planner
PostgreSQL .220 db echo schema echo (trade_journal, accounts, active_positions, lab_*)
    ↑ ClientConfig: Hasura .48 trigger accounts_config → echo-gateway (.71:8090) → Kafka
    ↑ config runtime: etcd /echo/production/ (clúster .250–.254)
    ↓ telemetría OTEL → Loki/Prometheus (ARGUS)
lab-worker (timer ~5 min): materialize_snapshots, equity curves, strategy snapshots → lab_* (DEGRADADO, AUD-01)
```

### E. Matriz G1–G10

| Gate | Resultado | Justificación (evidencia) |
|---|---|---|
| G1 INVENTORY | PASS | Topología física verificada vía SSH viewer + PG + etcd + Loki/Prometheus; límites documentados (SHAs, hosts Windows, Kafka PROD). |
| G2 RUNTIME | DEGRADED | Procesos, paths, PIDs, fechas de arranque y service.version 2.0.0 identificados; commit/SHA exactos de binarios PROD = UNKNOWN (viewer sin lectura de `/home/kor/echo`, Loki sin retención de agosto). UNKNOWN ≠ PASS a nivel SHA. |
| G3 CONFIG | PASS | Namespace `/echo/production/` leído sin secretos: PG .220/echo/schema echo/pool 5–20, Kafka .247–249, gateway 8090+localhost:9090, bridge pipe `echo_`, functions enabled, telemetry OTEL; comportamiento runtime coincide config a config; cero indicios de filtración DEV→PROD (nada apunta a .44/.161/echo-develop). Password ETCD: no legible por diseño; evidencia funcional fresca de validez (auth PG 13:10–13:56 UTC). |
| G4 SERVICES | DEGRADED | Core/Gateway/Functions/nginx/PG/ETCD/Hasura/ARGUS operativos y frescos; lab-worker silencioso 66 h+ + gap lunes (AUD-01) ⇒ degradación de un servicio real, aunque fuera del path de trading. |
| G5 TRANSPORT | PASS (indirecto) | Ruta completa bridge→Kafka→core→StateFun→PG demostrada con eventos reales (persistencia 1–2 s tras `opened_at`); `kafka_errors` sin incremento en 24 h; gateway publicó ClientConfig el 2026-09-18 12:47 UTC. Lag de consumer groups PROD no medible directamente (AUD-04, EVIDENCE_GAP). |
| G6 DATA | PASS | `trade_journal` con escritura continua (0 filas sábado = mercado cerrado, patrón normal); cero duplicados (trade_id+account_id); `active_positions` (2) == legs OPEN de ejecución (2); cuentas sincronizadas hace segundos; tablas legacy stale (canonical_trades 2026-05-04, execution_trade_pairs/account_equity_snapshots vacías) = deuda, P3. |
| G7 TRADING | PASS (pasivo) | E2E con tickets físicos: copia del día (trade `01a0c4da`, 3 legs con tickets broker) y ciclo OPEN→CLOSE multi-cuenta (`01a0a304`, 6 legs cerrados con precios); 3 FAILED históricos acotados (4109, ticket 0) sin huérfanos; re-envíos del lunes dedupados idempotente. Inspección directa del terminal/broker no ejecutada: BROKER_STATE mediado por eventos del terminal. |
| G8 RISK | PASS (pasivo) | `automation_evaluator` evaluando con HWM; cuentas ARCHIVED excluidas del fanout en vivo (WARN verificado en trade del día); 6 automation_profiles, 9 rules, 351 risk_policies, 152 strategies; exposición observada: 17 ACTIVE ≈ $1.265M balance agregado, 20 ARCHIVED ≈ $901k, 11 INACTIVE stale desde junio (esperado). Sin PnL/riesgo calculado con datos parciales. |
| G9 OBSERVABILITY | PASS con gaps | Loki (core DEBUG ~15M líneas/día, bridge, gateway, lab-worker) y Prometheus (métricas bridge frescas) fluyendo; Hasura consistente. Gaps: Jaeger/traces no verificados, métricas `echo_agent_*` stale, sin alerta de silencio del Lab (AUD-05), gateway en silencio ≥24 h = normal por diseño event-driven. |
| G10 CHANGE IMPACT | PASS | Correlación completa: cero cambios de código en PROD (master `5dd998f1` desde 2026-09-16; sin reinicios: core 20-ago, gateway 09-ago); cambios del fin de semana = branches DEV E-08/E-09/E-04 + despliegues Daedalus + incidentes ETCD (documentados en contrato §5.1–§5.6). Impacto PROD del fin de semana: password ETCD production (AUD-02, ya restaurada según evidencia) y gaps del Lab (AUD-01, correlación temporal con actividad del fin de semana, causa no demostrada). |

### F. Cambios del fin de semana (ventana 18–21 sep 2026)

| QUÉ | CUÁNDO (UTC) | DÓNDE | SHA / ARTEFACTO | EFECTO ESPERADO | AFECTA PROD? |
|---|---|---|---|---|---|
| Branch E-08 (routing/commands/riesgo) pushes + correcciones C1/C2 | 2026-09-20 13:17→18:47 (-03) | repo `xKoRx/echo`, `feature/e08-*` @ `c2e88a0d` | commits 79da8f8e…c2e88a0d | código DEV; migración 066 en DEV | NO (sólo repo) |
| Branch E-09 (execution fidelity) implementación completa | 2026-09-20 19:30→2026-09-21 04:18 (-03) | `feature/e09-*` @ `0798ce4a` | commits e892b3d7…0798ce4a | código DEV; migración 067 | NO (sólo repo) |
| Deploy Core DEV + unidades systemd --user en Daedalus | 2026-09-21 ~01:04 | Daedalus `.161` | `5dd998f1` | DEV arriba | NO (DEV) |
| Deploy Gateway DEV + ingestión DEV funcional | 2026-09-21 03:38 | Daedalus | Gateway `2360369c`→cert `3d260e81` | DEV ingest PASS | NO (DEV) |
| Certificación golden E-04/F-04-03 en Gateway DEV | 2026-09-21 04:18 | Daedalus | `3d260e81` + corpus F04-02 | join DEV PASS | NO (DEV) |
| Seed tests sobrescriben password ETCD `/echo/development/` y `/echo/production/postgres/password` (causa raíz repo, master aún la contiene) | ventana 2026-09-20→21; PROD vista corrupta 04:18 y restaurada por owner (evidencia funcional 13:10+) | etcd clúster real | keys de config, no datos | ninguna esperada; efecto real: auth PG rota para procesos que re-leen config | **SÍ** (AUD-02) |
| Dump test v1 espeja `/sqx-flowkit/development/` sobre `/sqx-flowkit/production/` | ~2026-09-21 12:27 | etcd real | fix `988e0ae6` publicado; verificación owner pendiente | ninguna esperada; impacto potencial workers flowkit (Forge) | **ADYACENTE** (AUD-08) |
| Publicación `feature/e04-dev-ingest-recovery` @ `4aad647b` (aisla seeds, renumeración 064→068) | 2026-09-21 09:39 (-03) | repo | `4aad647b` | blindar seed tests (pendiente merge a master) | NO (repo; mitiga recurrencia) |
| Gateway PROD publica ClientConfig (trigger Hasura) | 2026-09-18 12:47 | .71 → Kafka | evento de config, no deploy | sync de config de cuentas | operación normal |
| **Sin despliegues, sin reinicios, sin migraciones en PROD Echo** | toda la ventana | .71 | — | — | confirmado |

Baseline operativo previo (último conocido): core desde 2026-08-20 (hotfix `e25165ba`, verificado md5 en su momento), gateway desde 2026-08-09, functions desde 2026-09-12. El comportamiento actual es consistente con ese baseline; ningún defecto actual es atribuible a un cambio de código reciente (no los hubo en PROD).

### G. Evidencia E2E (operaciones reales existentes, sin generar nuevas)

**Muestra 1 — copia del día (2026-09-21 13:44 UTC), trade `01a0c4da-cdc8-7364-8000-383f11be2c7d` (NDX BUY):** Reference `2089125533` ticket 269545552 (1.30 lots) → ejecuciones `80577453` ticket 63121779 (2.34) y `130339` ticket 23149775 (3.35); filas creadas 13:44:30–13:44:32 UTC (≈1–2 s tras `opened_at`); `active_positions` refleja exactamente los 2 legs abiertos (última actualización 13:49 UTC); el fanout excluyó con WARN las cuentas ARCHIVED `2089126183`, `2089126186`, `80574724` ("account state does not accept opens"); strategy vía magic (fanout selectivo; la mayoría de trades del día son Reference-only, comportamiento esperado del gate de copia).

**Muestra 2 — ciclo completo OPEN→CLOSE (pre-ventana, 15→16 sep), trade `01a0a304-86d0-7e21-8001-29554bda121a` (USDJPY BUY):** Reference `2089126830` ticket 269350342 + 5 legs de ejecución con tickets físicos (130339/22820309, 80570850/62920658, 431019411/48378071, 80575718/62920661) más 1 FAILED (`443202`, error 4109, ticket 0); todas las legs exitosas con `close_price` y `closed_at` registrados el 16-sep.

**Muestra 3 — reapertura de mercado (2026-09-20 22:01–22:36 UTC):** primeras operaciones post-fin de semana (XAUUSD Reference cerrada, NDX Reference abierta) persistidas en horario esperado ⇒ sin gap de datos por el fin de semana.

Lectura honesta: no se generaron operaciones nuevas (prohibido), no se inspeccionó el terminal gráfico del broker (fuera de capacidad) y el lag de Kafka no se midió directamente; la evidencia de ejecución física son los tickets/precios broker registrados por los eventos del terminal.

### H. Estado de trading y riesgo

- Terminales: 18/18 `echo_bridge_executions_connected=1` (6 TTP, 2 FTMO, 10 real/AXI), versión bridge 2.0.0, snapshots de cuenta/instrumento fluyendo hace <2 min al momento de la auditoría.
- Posiciones abiertas: 21 filas OPEN en journal (19 Reference + 2 Execution); `active_positions` = 2 (las 2 de ejecución); consistencia journal↔positions OK.
- Exposición observada (sin calcular riesgo derivado): 17 cuentas ACTIVE con balance agregado ≈ $1.265M; sincronización de balances hace segundos (account_sync bulk OK).
- Fallos de ejecución: 3 FAILED en la ventana ampliada (14–15 sep, error 4109 "trade not allowed", ticket 0) sobre cuentas 442688, 431007281, 443202; sin reintento posterior (diseño actual: quedan FAILED); 55 FAILED históricos concentrados en junio. Sin órdenes UNKNOWN, sin outcomes huérfanos, sin duplicados económicos.
- Controles: fanout excluye estados no-operativos (verificado en vivo); HWM/automation_evaluator activo; riesgo por cuenta-estrategia (351 políticas) presente; sin señales de pérdida de cobertura ni desconecciones en la ventana.

### I. Incidentes y anomalías

Ver hallazgos AUD-01…AUD-09 en la sección L. Resumen: 1 degradación operacional demostrada (Lab silencioso), 1 incidente de config ya remediado con evidencia (password ETCD PROD), 3 gaps de verificabilidad (SHA binarios, Kafka lag, broker directo) y anomalías menores benignas (re-envíos idempotentes, listener :45021, tablas legacy, métricas stale, volumen DEBUG).

### J. Riesgos no verificables (EVIDENCE_GAP)

- Commit/SHA exacto de los binarios PROD en ejecución (G2): no legible con capabilities vigentes.
- Consumer lag de Kafka PROD y salud de brokers: sin capability RO dedicada; sólo evidencia indirecta.
- Estado físico directo de terminales MT4/cuentas broker (GUI/terminal): mediado por eventos del bridge; no inspeccionado independientemente.
- Valor actual de `/echo/production/postgres/password`: secreto excluido por diseño del MCP RO; validez demostrada sólo funcionalmente (auth exitosa fresca).
- Causa exacta de los gaps del lab-worker: journal del servicio no exportado a Loki (unidades de usuario ausentes del shipper) y `systemctl` fuera del allowlist viewer ⇒ requiere acción owner.
- Integridad histórica (mod_revision) de `/sqx-flowkit/production/` tras el intento de espejo del 12:27Z: estructura actual intacta, verificación owner pendiente.

### K. Comparación baseline vs actual

| Dimensión | Baseline (2026-08-20/21 y 09-15) | Actual (2026-09-21) | Delta |
|---|---|---|---|
| Procesos .71 | core+gateway+functions+lab-worker+nginx RUNNING | mismos, mismos PIDs/arranques | sin cambios |
| Pipeline journal | vivo, inserciones ECHO diarias | vivo, 1–2 s latencia | sin regresión |
| Lab pipeline | timer cada 5 min OK, ~861 corridas/día 24/7 | paradas 17-sep 21:55→21-sep 01:58 y 03:44→13:10 | **REGRESIÓN (AUD-01)** |
| Terminales/bridges | conectadas | 18/18 conectadas, sin errores kafka 24 h | sin regresión |
| Config ETCD PROD | password válida | password válida (tras incidente fin de semana) | remediado; riesgo de recurrencia mientras master contenga seed tests |
| Datos | sin duplicados; matview con issues históricos | sin duplicados; matview no re-auditada (fuera de ventana) | neutro |

### L. Acciones correctivas por severidad (hallazgos)

- **AUD-01 · P1 · OPERATIONAL — Lab pipeline silencioso.** Evidencia: `lab_job_runs` 861 corridas/día 24/7 hasta 17-sep 21:55 UTC; 0 corridas 18–20-sep y primera del 21-sep a 01:58 UTC; segundo gap 03:44→13:10 UTC; 0 filas FAILED y 0 logs del worker en los gaps (nunca emitió "starting") ⇒ fallo a nivel timer/unidad o muerte pre-flush; `systemctl`/journal no accesibles RO. Impacto: métricas Lab congeladas (screener/equity/decisiones sobre datos stale); trading no afectado. Causa demostrada: NO; hipótesis (a) password ETCD PROD corrupta rompió auth PG del worker en cada ciclo (encaja con el gap del lunes si la corrupción se produjo 03:44–04:18Z y fue restaurada antes de 13:10; no explica por sí sola el fin de semana salvo corrupción más temprana + restauraciones múltiples) o (b) timer/unidad detenida manualmente o por evento del host. Owner. Acción mínima: inspeccionar estado del timer/unidad y journal de `echo-lab-worker` en .71, fijar causa, y dejar alerta de recencia (AUD-05). Gate de regresión: `max(created_at) echo.lab_job_runs` < 15 min continuo por 72 h.
- **AUD-02 · P1 · SECURITY/CONFIG — password ETCD production (incidente del fin de semana, estado actualizado).** El contrato §5.5/§5.6 la documenta corrupta (seed) y pendiente de restaurar; esta auditoría aporta evidencia fresca de que YA funciona: auth PG exitosa vía ETCD en 5+ ciclos del lab-worker (13:10–13:56 UTC) y escrituras del core toda la mañana. Pendiente del owner: confirmar el valor/mechanismo aplicado y completar el blindaje (merge a master del fix de seeds `4aad647b`): **master `5dd998f1` todavía contiene los seed tests que escriben a ETCD real**; mientras eso persista, un `go test ./...` desde un checkout de master puede re-clobberizar ambos ambientes con PROD core/gateway sin reiniciar pero con todo proceso que re-lea config (lab-worker, futuros restarts) rompiéndose en silencio. Gate de regresión: `/echo/production/postgres/password` con mod_revision sin escrituras externas; lab-worker sin gaps.
- **AUD-03 · P2 · VERIFICATION — identidad de binarios PROD (commit/SHA) no verificable.** Acción mínima: publicar BUILD.md/SHA por release en .71 (patrón ya usado en DEV) o fingerprint md5/sha256 por el owner una vez, y registrar en la matriz de capabilities. Gate: próxima auditoría G2 en PASS.
- **AUD-04 · P2 · EVIDENCE — sin capability RO de Kafka PROD** (`aranea-kafka-prod-ro` es plan diferido): lag/backlog/DLQ no medibles directamente. Acción: certificar capability RO o exportar lag como métrica. Gate: G5 con lag directo.
- **AUD-05 · P2 · OBSERVABILITY — sin alerta de silencio del Lab** (66 h sin detectar). Acción: alerta Grafana sobre recencia de `lab_job_runs` (o heartbeat métrico) + alerta sobre `kafka_errors_total` y sobre filas FAILED nuevas. Gate: alerta disparando en drill controlado (no en PROD real).
- **AUD-06 · P3 · BEHAVIOR — intents fallidos re-enviados por terminales se dedupan idempotente** (3 eventos, 21-sep 00:12–00:36 UTC, sólo `updated_at`); FAILED (4109) sin política de reintento. Acción: decidir si FAILED requiere reintento/alarma operacional o queda como registro.
- **AUD-07 · P3 · HYGIENE — deuda observada:** tablas legacy stale (`canonical_trades` 04-may; `execution_trade_pairs`, `account_equity_snapshots` vacías; `analytics_job_runs` 04-may), listener `:45021` sin identificar en .71, métricas `echo_agent_*` stale, core emite ~15M líneas DEBUG/día a Loki (costo). Acción: inventario y limpieza diferida; identificar :45021.
- **AUD-08 · P3 · ADJACENT — posible espejo `/sqx-flowkit/production/` (12:27Z).** Estructura actual intacta (105 keys, historial 2025, `postgres/` con 6 keys; `minio/endpoint` idéntico a DEV, lo que puede ser diseño compartido). Owner: verificar mod_revision (>12:20Z ⇒ reconciliar) e impacto en workers flowkit Zeus/Hera/Kronos. No afecta a Echo core.
- **AUD-09 · INFO — gateway en silencio ≥24 h = normal** (logging event-driven; última actividad 18-sep 12:47 UTC, dentro de ventana). No requiere acción; documentado como patrón de interpretación.

### M. Dependencias del owner

1. Investigar y remediar la causa de los gaps del lab-worker en .71 (timer/journal; AUD-01) y confirmar qué se ejecutó a las 01:58 y 13:10 UTC del 21-sep.
2. Confirmar restauración de `/echo/production/postgres/password` y acelerar merge a master del fix de seed tests (`4aad647b`) (AUD-02).
3. Fingerprint de binarios PROD una vez (AUD-03) y decisión sobre capability Kafka PROD RO (AUD-04).
4. Alertas de recencia Lab + errores (AUD-05).
5. Verificación mod_revision `/sqx-flowkit/production/` (AUD-08).

### N. Veredicto operacional

**`OPERATIONAL_DEGRADED`** — el flujo crítico (ingesta de eventos, copia con tickets físicos, persistencia, riesgo pasivo) funciona correctamente y sin regresiones atribuibles al fin de semana; la degradación demostrada (Lab silencioso 66 h+, causa no demostrada) más los gaps de verificabilidad (SHA binarios, lag Kafka) impiden `OPERATIONAL_PASS` bajo el criterio de esta auditoría. `INSUFFICIENT_EVIDENCE` no aplica: la evidencia recolectada alcanza para el veredicto.

## Fuentes

- Física (13:40–14:00 UTC): SSH viewer `echo-runtime-prod` (.71: hostname/id/ps/ss/ls), PostgreSQL RO `mcp_echo_prod_ro` (pg_stat_database, trade_journal, accounts, active_positions, lab_job_runs, information_schema), etcd RO (`/echo/production/` 32 keys; `/sqx-flowkit/production|development/`), Loki/Prometheus ARGUS (echo-core/gateway/bridge/lab-worker; `echo_bridge_executions_connected`), Hasura PROD RO (v2.38.0 consistente), git local `~/go/src/github.com/xKoRx/echo` (log --all).
- Documentales: [[Echo + Echo Forge — Environment Contract]] §5.1–§5.6 y §7; [[Echo — Access & Physical Capability Matrix]]; [[30-resources/agents/skills/aranea-mcps-expert/SKILL.md|aranea-mcps-expert]]; [[30-resources/runbooks/aranea-ssh-mcp|aranea-ssh-mcp]]; [[30-resources/runbooks/aranea-etcd-mcp|aranea-etcd-mcp]]; [[Echo - Discovery y Estado]]; [[Echo - Reporte de Estado Lab y Journal 2026-08-21]].
- Skill reproducible: [[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]].
