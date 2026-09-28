---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Production Operational Audit 2026-09-22]]"
  - "[[Echo — Production Operational Audit 2026-09-21]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
aliases:
  - Echo PROD operational audit 2026-09-27
  - auditoria operacional Echo PROD 27-sep
tags:
  - kind/doc
  - area/echo
  - action/audit
created: "2026-09-27"
updated: "2026-09-27"
---

# Echo — Production Operational Audit 2026-09-27

## Propósito

Auditoría operacional E2E read-only de Echo PROD tras la ventana 2026-09-22 11:15 UTC → 2026-09-28 01:50 UTC, cuyo evento dominante es el **despliegue a PROD del 2026-09-25 ~02:00 UTC** (commit `372af59a` = `origin/master`: migraciones 061–065, ETCD, metadata Hasura, core/gateway/lab-worker/front vía `deploy-prod.sh`). Ejecutada 2026-09-28 01:30–01:55 UTC desde Daedalus. Regresión contra [[Echo — Production Operational Audit 2026-09-22]] y [[Echo — Production Operational Audit 2026-09-21]]. Read-only absoluto: cero órdenes, cero mutaciones. **Limitación de acceso: sin capability `aranea-ssh`** (el toolset sólo trajo ETCD/PG/Hasura/observabilidad RO), por lo que G1/G2 se degradan a telemetría — igual que la sesión del 09-22; queda gap documentado, no improvisado.

**Veredicto: `OPERATIONAL_DEGRADED`** — no por rotura funcional (no se encontró ninguna: el despliegue del 25-sep se correlacionó completo y sin regresiones, el pipeline E2E procesa y persiste al segundo, hubo 37 legs de copia real con tickets 22–24 sep y los controles de riesgo operan en vivo), sino porque (i) los gates de inventario/runtime quedan DEGRADED por la ausencia estructural de SSH (procesos, listeners y SHA de binarios de `.71` no verificables con las capabilities de la sesión — carry-over AUD-03), (ii) el fix de AUD-10 (DAX/GDAXI) está desplegado pero **sin verificación E2E** porque la estrategia copiable no ha vuelto a disparar, y (iii) persisten hallazgos de higiene menores con causa demostrada (2 legs OPEN reliquias de junio, knob de telemetría WARN vs DEBUG efectivo). Ninguno compromete capital hoy.

## Contenido

### A. Resumen ejecutivo

Echo PROD está operando correctamente tras el despliegue del 25-sep: el core sincroniza cuentas/posiciones hace segundos, el gateway publicó el config completo post-deploy (17 cuentas, 136 estrategias, **357 execution policies = exactamente las 357 filas vigentes en PG**), los 3 bridges de ejecución mantienen 17/18 terminales conectadas y publicando InstrumentSnapshots con transform canónico activo, el Lab corre 861 corridas/24 h con recencia de minutos, Hasura está consistente y el journal registró su última fila (cierre XAUUSD) a las 22:01 UTC del domingo 27, tras la apertura de mercado. La copia real funcionó durante la semana: 32–37 legs EXECUTION con tickets de broker 22–24 sep en NDX y USDJPY, con ciclos completos OPEN→CLOSED y PnL neto. Los WARN/ERROR del core en 48 h son 9 líneas, todas explicadas (2 ERRORs de `context canceled` en el reinicio del deploy, exclusiones ARCHIVED correctas, close_handler correcto sobre señales reference-only). Cero filtración DEV→PROD; ETCD de producción estable.

### B. Fecha, ventana y ambiente verificado

- Ejecución: 2026-09-28 01:30–01:55 UTC (27-sep 22:30–22:55 CLT).
- Ventana auditada: 2026-09-22 11:15 → 2026-09-28 01:55 UTC (incluye el fin de semana, con mercado cerrado sábado y apertura dominical ~21:00–22:00 UTC — cero filas de journal el sábado es mercado cerrado, no gap).
- Ambiente: **PROD** (`/echo/production/`; `deployment.environment=production` en toda la telemetría; host `echo` en .71).
- Capacidad RO usada: `aranea-postgres-ro`, `aranea-etcd-ro`, `aranea-observability-ro` (Loki `P8E80F9AEF21F6940`, Prometheus `PBFA97CFB590B2093`), `aranea-hasura-prod-ro`. **No disponible `aranea-ssh`** ⇒ G1/G2 a nivel proceso/PID/SHA = EVIDENCE_GAP (idéntico al 09-22).

### C. Inventario real observado (G1, variante sin SSH)

| Componente | Evidencia de vida | Ambiente | Estado |
|---|---|---|---|
| Echo Core v2.0.0 | account_sync/position_sync en Loki a las 01:46 UTC (hace segundos); 9 WARN/ERROR en 48 h, todos explicados | PROD | ALIVE (telemetría); PID/START/SHA = EVIDENCE_GAP |
| Echo Gateway v2.0.0 | Force-sync administrativo completo post-deploy (25-sep 02:08 UTC: 17 cuentas/136 estrategias/357 policies); silencio posterior = normal event-driven (AUD-09) | PROD | ALIVE (telemetría) |
| Echo Functions | `functions/enabled=true`; fanout, planner y close_handler operando en logs core | PROD | ALIVE (indirecto) |
| Echo Bridge ×3+ | Prometheus fresco (scrape al segundo): 18 series, 17 `connected=1` (mt4-ttp 6, mt4-ftmo 2, mt4-real 10); logs DEBUG al segundo con `InstrumentSnapshot published` (USDJPY, XAUUSD→GOLD) | PROD | ALIVE; 80581422 `0` (AUD-13) |
| Lab worker | `echo.lab_job_runs`: última corrida 01:38 UTC; 861 corridas/24 h (baseline sano ~860/día); `materialize-snapshots completed` | PROD | ALIVE (AUD-01 sigue cerrado) |
| PostgreSQL .220 | `numbackends('echo')=5`; auth fresca de core/lab-worker (xact_commit 782M) | PROD | UP |
| Hasura .48 | v2.38.0, metadata consistente | PROD | UP |
| etcd .250–.254 | `/echo/production/` 37 keys (32 legibles + 5 secret-named excluidas por diseño); lectura RO OK | compartido | UP |
| Terminales | 18 cuentas en métrica (incluye 80636976 "Orion LOVE!" y 80577453 nuevas vs 09-22); 130339 ya no aparece en la métrica | Windows | 17/18 conectadas |

Novedad de inventario: el host `mt4-demo` aparece en Loki con telemetría `env=production` (recibió configs post-deploy, "stored for reconnection", sin series `connected` en Prometheus). Ver AUD-16.

### D. El despliegue del 2026-09-25, correlacionado (G10)

Cadena de evidencia física que demuestra qué se desplegó y que el rollout terminó consistente:

| QUÉ | CUÁNDO (UTC) | EVIDENCIA |
|---|---|---|
| Reinicio de core (deploy) | 25-sep ~02:00 | ERRORs `kache: failed to subscribe to topic` con `error="context canceled"` en ambos caches (shutdown ordenado del proceso viejo); no recursen en 48 h |
| Gateway republish completo | 25-sep 02:08 | `Administrative force-sync completed`: 17 accounts, 136 strategies, **357 policies** — coincide 1:1 con `count(*)=357` de `account_strategy_risk_policy` en PG |
| Bridges reciben config | 25-sep 02:08 | WARNs `Config update received but no session found - stored for reconnection` (80636976, 80577453) en mt4-demo/ttp/ftmo; patrón auto-reparable, sin recurrencia |
| Migraciones 061–065 | 25-sep | Tablas `mig061_backup_account_strategy_risk_policy` y `automation_profiles_full` presentes; `trade_journal` con columnas nuevas `*_event`/`*_recorded`, `origin`, `profit_net`, `error_code/message` (separación event/recorded time del trabajo D1/D2) |
| Seed de `symbol_mappings` | 25-sep (o ventana) | 13 → **27 filas**: +DAX×6 brokers (DARWINEX GDAXI, FTMO GER40.cash, ORION GER30, THE5ERS DAX40, TTP GER40., WSF DE40.c), +GOLD×7, +EURUSD×1, todas `is_active=true` con `created_at` histórico preservado (seed/backfill, no inserts de cero) |
| Metadata Hasura | 25-sep | Consistente hoy (`get_inconsistent_metadata` vacío) |
| Qué NO se desplegó | ventana | D4 Shot 1 (live analytical refresh) queda en `origin/feature/d4-live-analytical-refresh` (`2af4b21f`), fuera de master; las keys ETCD `gateway/forge_ingest/*` existen sólo en `/echo/development/` (54 keys) y no en production — frontera DEV/PROD correcta |

Estado git de la ventana: `origin/master` = `372af59a` (24-sep, único tip; sin commits nuevos en master desde entonces). El front local de Daedalus sigue en `3596fc48` (behind 13). **AUD-02 sigue vigente: `4aad647b` (fix de seed tests) NO está en `origin/master`** — verificado hoy con `git merge-base --is-ancestor`.

### E. Matriz G1–G10

| Gate | Resultado | Justificación |
|---|---|---|
| G1 INVENTORY | DEGRADED | Topología demostrada por telemetría (core/gateway/bridges×3+demo/lab-worker/PG/Hasura/etcd, environment=production); sin SSH no se re-observaron procesos/listeners/binarios de .71 (gap estructural de capability, carry-over). |
| G2 RUNTIME | DEGRADED | `service.version=2.0.0` uniforme y timestamps frescos al segundo en core/bridge/gateway/lab-worker; reinicio del deploy correlacionado (25-sep 02:00–02:08 UTC); PID/arranque/SHA = EVIDENCE_GAP (AUD-03). |
| G3 CONFIG | PASS | Valores ETCD leídos idénticos al baseline (Kafka .247–249:9092, PG .220/`echo`, core `localhost:9090`, gateway 8090, pipe `echo_`, functions on); 37 keys (32 visibles; 5 secretas excluidas por diseño — validez demostrada funcionalmente por auth PG fresca); cero endpoints DEV (.44/.161/echo-develop) en production; DEV aislado con sus keys nuevas forge_ingest. MISMATCH menor: `telemetry/logs/level=WARN` declarado vs DEBUG fluyendo (AUD-15). |
| G4 SERVICES | PASS | PG 5 backends; Hasura v2.38.0 consistente; Lab 861 corridas/24 h con recencia de minutos (AUD-01 cerrado se mantiene); bridges 17/18; gateway al día (force-sync 357/357 policies). |
| G5 TRANSPORT | PASS | Journal persistiendo al segundo (última fila 27-sep 22:01:03 UTC = cierre XAUUSD post-apertura dominical); account_sync/position_sync hace segundos; InstrumentSnapshots fluyendo con transform canónico (USDJPY→USDJPY, XAUUSD→GOLD). Lag directo Kafka PROD = EVIDENCE_GAP (AUD-04). |
| G6 DATA | PASS con hallazgo | 0 duplicados (trade_id+account_id); `active_positions=0` consistente con broker flat; cuentas ACTIVE (17) sincronizadas en la última hora. Hallazgo de higiene: 2 legs EXECUTION `OPEN` reliquias del 4-jun (AUD-14) — sin exposición viva. |
| G7 TRADING | PASS | Copia real demostrada: 37 legs EXECUTION con tickets 22–24 sep (NDX/USDJPY), ciclos completos OPEN→CLOSED con PnL neto (p.ej. 251002047 → +501.08 USD en 442688); 0 FAILED en la ventana; pipeline activo el mismo día del deploy (24 refs el 25-sep) y en la reapertura del domingo. DAX: mappings desplegados, sin señal copiable desde entonces — verificación E2E del fix pendiente (gate de regresión AUD-10). |
| G8 RISK | PASS (con actividad) | Exclusiones por estado operando en vivo y verificadas 1:1 (fanout XAUUSD 27-sep 21:41: 2089126183/2089126186 rechazadas ARCHIVED con motivo exacto); 357 policies publicadas y cargadas; exposición estable (ACTIVE 17 ≈ $1.263M, ARCHIVED 21 ≈ $1.012M, INACTIVE 11 ≈ $108k); sin posiciones huérfanas vivas. |
| G9 OBSERVABILITY | PASS con gaps | Loki fluyendo por servicio con label `level` (escaneo WARN/ERROR barato: 9 líneas/48 h en core); Prometheus scrape fresco al segundo. Carry-over: sin alertas de silencio (AUD-05), Jaeger sin verificar, `echo_agent_*` stale. |
| G10 CHANGE IMPACT | PASS | Único cambio de la ventana = deploy 372af59a del 25-sep, correlacionado físico completo (§D) sin regresiones; master sin commits posteriores; D4/forge_ingest correctamente fuera de PROD; sin despliegues ocultos (ETCD estable + telemetría continua). |

### F. Evidencia E2E

**Muestra 1 — ciclo completo post-deploy (XAUUSD `01a0e587-8cc8-7dbe-8000-63fe5425122a`, 27→28 sep):** señal 21:41 UTC → execution_planner fanout con exclusión correcta de cuentas ARCHIVED (WARNs con account/state exactos) → referencia persistida en journal → cierre procesado 22:01 → `close_handler` 00:31 "no open executions found" (correcto: reference-only). Trazabilidad WARN↔config 1:1.

**Muestra 2 — copia real con PnL (NDX/USDJPY, 22–24 sep):** 37 legs EXECUTION con tickets de broker reales; p.ej. `magic_251002047` 23-sep 22:41: tickets 28671652 (442688, +501.08), 48735718 (431007281, +489.25); `magic_250901050` 24-sep: 63278249 (80577453, −350.21). Persistencia, dedup y liquidación consistentes.

**Muestra 3 — Lab vivo:** 861 corridas/24 h, última 01:38 UTC (`materialize_snapshots` success, PG conectado vía ETCD).

No se generaron operaciones nuevas (prohibido read-only); sin inspección directa de terminales Windows (sin capability).

### G. Sub-rutina "¿por qué no copia?" (25–27 sep)

Cero legs EXECUTION desde el 24-sep no es defecto: las señales que dispararon fueron GDAXI 251002015/034/035/038 (25-sep) y XAUUSD 250901015 (27-sep), y **ninguna está en la whitelist de copia** (`account_strategy_risk_policy`; las copiables son NDX 250901045/048/050, USDJPY 251002044/047/049/052/053/054 + 260104004, GOLD 2506/2509, DAX 251002014). La estrategia DAX copiable (251002014) no volvió a disparar desde el 22-sep. Reference-only por diseño; sin WARNs anómalos.

### H. Estado de trading y riesgo

- Terminales: 17/18 conectadas; 80581422 (ARCHIVED, AUD-13) en `0`; 130339 desapareció de la métrica y su fila pasó a ARCHIVED (AUD-12 cerrado como deliberado).
- Posiciones: 0 posiciones vivas en `active_positions`; las 2 filas OPEN del journal son reliquias de junio (AUD-14), no exposición.
- Exposición (balances agregados, sin PnL derivado): ACTIVE 17 ≈ $1.263M; ARCHIVED 21 ≈ $1.012M; INACTIVE 11 ≈ $108k (stale, esperado). Sin status CLOSE_ONLY.
- Fallos de ejecución: 0 FAILED en la ventana; los 3 históricos (4109) siguen acotados.
- Controles: automation_profiles/automation_rules presentes; exclusiones en vivo con motivo; 357 policies consistentes gateway↔PG.

### I. Hallazgos

- **AUD-14 · P3 · DATA_HYGIENE — 2 legs EXECUTION OPEN reliquias del 4-jun, jamás cerradas en journal.** Evidencia: `019e94a6…` (442688, NDX 0.01 @30496.48, ticket 26790522) y `019e94f5…` (802591, USDJPY 1.4 @160.043, ticket 26790904), `created_at`=`updated_at`=2026-06-04, mientras `active_positions=0` (broker flat; ambas cuentas conectadas). Corrige el claim del 09-22 ("0 legs OPEN"): esas filas existen desde junio; el conteo de esa auditoría estaba scopeado a la ventana. Impacto: distorsión de métricas de posiciones abiertas; sin riesgo de capital. Causa: hipótesis (cierre externo/manual no observado por Echo antes de la integración del bridge). Owner: decidir reconciliación (marcar CLOSED con motivo de conciliación o backfill). Gate de regresión: `count(journal OPEN EXECUTION) == count(active_positions)`.
- **AUD-15 · P3 · OBSERVABILITY_CONFIG — knob `telemetry/logs/level=WARN` no honrado en caliente.** Evidencia: ETCD `/echo/production/telemetry/logs/level=WARN` vs streams core/bridge emitiendo DEBUG (core ~55k líneas/48 h — volumen moderado, no crítico). Causa: hipótesis (knob aplicado sólo al arranque; valor cambiado post-deploy sin reinicio, o no cableado en PROD). Owner: verificar en el próximo reinicio o habilitar hot-reload.
- **AUD-16 · P4 · INVENTORY — bridge `mt4-demo` en telemetría PROD sin documentar.** Evidencia: Loki `host_name=mt4-demo`, `env=production`, recibió configs post-deploy ("stored for reconnection"), sin series `connected` en Prometheus. Componente no presente en auditorías previas. Owner: clasificar (flota demo/reference) o documentar; sin acción urgente.
- **AUD-10 · ACTUALIZADO (fix desplegado, verificación pendiente).** `symbol_mappings` pasó de 13 a 27 filas con DAX×6 brokers activos (seed con `created_at` preservado en la ventana del deploy). La estrategia copiable 251002014 no ha vuelto a disparar ⇒ sin demostración E2E aún. Gate de regresión intacto: próximo disparo copiable de DAX genera ≥1 leg EXECUTION con ticket.
- **AUD-12 · CERRADO (confirmado deliberado).** 130339 re-clasificada ARCHIVED, fuera de la métrica del bridge, sin posiciones.
- **AUD-13 · VIGENTE.** 80581422 (ARCHIVED "Orion 250%Refund") ahora `connected=0`; ruido de inventario sin impacto (el planner la excluye por estado).
- **AUD-01 · MANTIENE CERRADO.** Lab 861/24 h continuo; sin recurrencia de los gaps del fin de semana del 21-sep.
- **Carry-over vigente:** AUD-02 (4aad647b sigue fuera de `origin/master` — re-verificado hoy), AUD-03 (SHA binarios PROD), AUD-04 (Kafka PROD RO), AUD-05 (alertas de silencio/errores), AUD-08 (mod_revision `/sqx-flowkit/production/`), AUD-11 (artefacto timezone en `opened_at`; el nuevo par `*_event`/`*_recorded` del esquema apunta a mitigarlo — semántica aún por confirmar).

### J. Riesgos no verificables (EVIDENCE_GAP)

- Procesos/listeners/binarios de `.71` (sin SSH esta sesión; gap estructural AUD-03).
- SHA exacto de los binarios corriendo (sólo `service.version=2.0.0` en telemetría; la correlación del deploy es temporal, no criptográfica).
- Lag/backlog de consumer groups Kafka PROD (sin capability RO; AUD-04).
- Estado físico directo de terminales MT4 Windows (mediado por bridge).
- Valores de las 5 keys secret-named de `/echo/production/` (excluidas por diseño; validez demostrada funcionalmente).
- Que mig061–065 aplicó el 100% de sus objetos: evidencia indirecta fuerte (tablas backup, columnas nuevas, metadata Hasura consistente), no catálogo completo.
- Verificación E2E del fix DAX (pendiente del próximo disparo copiable).

### K. Comparación contra auditoría previa (2026-09-22)

| Dimensión | 22-sep 11:15 UTC | 28-sep 01:55 UTC | Delta |
|---|---|---|---|
| Transporte/persistencia | vivo, al segundo | vivo, al segundo (última fila 22:01 UTC domingo) | sin regresión |
| Lab pipeline | 36/h, recuperado | 861/24 h continuo | estable/sano |
| Terminales | 17/18 (130339 fuera deliberado) | 17/18 (80581422 ARCHIVED fuera) | equivalente |
| Copias | 0 en la ventana (GDAXI muerto por AUD-10) | 37 legs con tickets 22–24 sep, PnL real | **MEJORA** |
| AUD-10 GDAXI | activo desde abril | mappings desplegados (27 filas); verificación E2E pendiente | **fix en PROD, gate pendiente** |
| ETCD PROD | 32 keys visibles | 32 visibles + valores íntegros; DEV separado con forge_ingest | sin cambios no deseados |
| Git | master `5dd998f1`, front local sin push | master `372af59a` DEPLOYADO; front local behind 13; 4aad647b sigue fuera | deploy correlacionado |
| Exposición ACTIVE | ≈ $1.257M | ≈ $1.263M | estable |
| Schema BD | journal sin `*_event/*_recorded` | esquema post-061–065 con event/recorded time + origin/profit_net | evolución esperada del deploy |

### L. Veredicto operacional

**`OPERATIONAL_DEGRADED`** — con la aclaración de que **no se encontró ninguna rotura funcional**: el deploy del 25-sep se correlacionó completo y consistente (core reiniciado, 357/357 policies republicadas, bridges y Lab operando, Hasura consistente, cero errores residuales), el trading real funcionó toda la semana con tickets y PnL, y los controles de riesgo operan en vivo. La etiqueta DEGRADED se debe a (i) los gates G1/G2 sin SSH (gap de capability estructural, carry-over AUD-03, idéntico al 09-22 — procesos/SHA de .71 no verificables), (ii) el fix AUD-10 desplegado pero sin su gate de regresión E2E (sin disparo copiable de DAX desde el fix), y (iii) hallazgos de higiene menores con causa demostrada (AUD-14/15/16). Con SSH disponible para re-observar procesos/SHA, la sustancia de esta auditoría sería `OPERATIONAL_PASS`. `INSUFFICIENT_EVIDENCE` no aplica: la evidencia funcional es amplia y fresca.

## Fuentes

- Física (01:30–01:55 UTC): PostgreSQL RO (`pg_stat_database`, `trade_journal` + esquema, `active_positions`, `accounts`, `lab_job_runs`, `symbol_mappings`, `account_strategy_risk_policy`, `information_schema`), etcd RO (`/echo/production/` 32 keys legibles + inventario `/echo/development/`), Loki `P8E80F9AEF21F6940` (core/bridge/lab-worker/gateway con label `level`; stats y queries acotadas), Prometheus `PBFA97CFB590B2093` (`echo_bridge_executions_connected` instant 18 series), Hasura PROD RO (v2.38.0 + metadata consistente), git local Daedalus (`~/go/src/github.com/xKoRx/echo`: `origin/master=372af59a`, `merge-base --is-ancestor 4aad647b` negativo).
- Documentales: [[Echo — Production Operational Audit 2026-09-22]] (baseline de regresión y hallazgos AUD-01…13), memoria del rollout DEV→PROD del 2026-09-25, [[Echo + Echo Forge — Environment Contract]], [[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]].
