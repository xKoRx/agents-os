---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Production Operational Audit 2026-09-21]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
aliases:
  - Echo PROD operational audit 2026-09-22
  - auditoria operacional Echo PROD 22-sep
tags:
  - kind/doc
  - area/echo
  - action/audit
created: "2026-09-22"
updated: "2026-09-22"
---

# Echo — Production Operational Audit 2026-09-22

## Propósito

Auditoría operacional E2E read-only de Echo PROD solicitada por el owner ante la percepción de que el sistema "no está entrando en operaciones" después de una ventana de cambios de config (2026-09-21 14:00 UTC → 2026-09-22 11:15 UTC). Ejecutada 2026-09-22 10:57–11:15 UTC desde Daedalus. Regresión contra [[Echo — Production Operational Audit 2026-09-21]]. Read-only absoluto: cero órdenes, cero mutaciones. **Limitación de acceso de esta sesión: sin capability `aranea-ssh`** (el toolset sólo trajo ETCD/PG/Hasura/observabilidad RO), por lo que el inventario de procesos en `.71` no fue re-observable y se sustituyó por telemetría; queda documentado como gap, no improvisado.

**Veredicto: `OPERATIONAL_DEGRADED`** — el sistema SÍ está operando (referencias fluyendo al segundo, Lab recuperado, 17/18 terminales conectadas, cero regresiones de infraestructura), y la percepción del owner tiene una explicación técnica demostrada: (1) casi todas las señales de la ventana pertenecen a estrategias **reference-only por diseño** (la whitelist de copia es de 18 estrategias históricas y ninguna de las que disparó desde ayer 14:00 está en ella, salvo una), y (2) la única estrategia que intentó copiar de verdad (GDAXI `magic_251002014`) **falló siempre en `mm_engine` por un gap de configuración antiguo: GDAXI no existe en `symbol_mappings`** (AUD-10, vigente desde abril, no causado por los cambios recientes). Más el carry-over de gaps de verificabilidad de ayer (SHA binarios, lag Kafka) y una terminal deliberadamente fuera (130339). Ninguna operación perdida, duplicada o huérfana; cero filtración DEV→PROD.

## Contenido

### A. Resumen ejecutivo

Echo PROD opera correctamente en su capa de transporte y persistencia: 16 trades de referencia persistidos desde ayer 14:00 UTC con `created_at` al segundo del evento, `account_sync` escribiendo hace segundos, el pipeline Lab **recuperado** (36 corridas en la última hora; la regresión AUD-01 de ayer está cerrada), Hasura consistente, ETCD de producción intacto (32 keys, valores idénticos al baseline, cero indicios DEV) y el gateway vivo publicando config el lunes 15:46 UTC. La razón por la que "no entran operaciones" es de **política de copia, no de salud**: desde ayer 14:00 UTC hubo cero legs EXECUTION porque (a) las estrategias que dispararon son en su mayoría reference-only, y (b) el único fanout real (GDAXI 251002014, hoy 09:52) murió en `mm_engine` con `MM_CALCULATION_ERROR` porque `FIXED_RISK` necesita un `InstrumentSnapshot` que no existe para GDAXI en ninguna cuenta — `symbol_mappings` no tiene ninguna fila GDAXI. Ese gap es de abril-2026 y afecta a toda señal GDAXI copiable desde entonces. Los cambios del owner en la ventana (130339→CLOSE_ONLY ayer 14:38, policies de `magic_250901048` republicadas ayer 15:46, commit local del front en master local sin push) quedaron correlacionados y no rompieron nada en PROD.

### B. Fecha, ventana y ambiente verificado

- Ejecución: 2026-09-22, 10:57–11:15 UTC (07:57–08:15 CLT).
- Ventana auditada: 2026-09-21 14:00 → 2026-09-22 11:15 UTC (post-auditoría de ayer hasta ahora).
- Ambiente: **PROD** (`/echo/production/`; `deployment.environment=production` en toda la telemetría). DEV (Daedalus, donde corre esta sesión) usado sólo como correlación de cambios, nunca como objetivo.
- Capacidad RO usada: `aranea-postgres-ro`, `aranea-etcd-ro`, `aranea-observability-ro`, `aranea-hasura-prod-ro`. **No disponible: `aranea-ssh`** ⇒ G1/G2 a nivel proceso/PID/SHA = EVIDENCE_GAP.

### C. Inventario real observado (G1, variante sin SSH)

| Componente | Evidencia de vida en la ventana | Ambiente | Estado |
|---|---|---|---|
| Echo Core | WARN/INFO en Loki hasta 11:12 UTC de hoy; procesó el fanout GDAXI 09:52; service.version 2.0.0 | PROD | ALIVE (telemetría); PID/START/SHA = EVIDENCE_GAP |
| Echo Gateway | Última actividad 2026-09-21 15:46 UTC (ClientConfig 183623 + execution policies 250901048); silencio posterior = normal event-driven (AUD-09) | PROD | ALIVE (telemetría) |
| Echo Functions | `functions/enabled=true`; fanout y close_handler operando (mismos logs core) | PROD | ALIVE (indirecto) |
| Echo Bridge ×3 | Prometheus `echo_bridge_executions_connected` fresco (scrape 11:05): 18 series, 17 en `1`, mt4-ttp/mt4-ftmo/mt4-real | PROD | ALIVE; 130339 `0` (AUD-12) |
| Lab worker | `echo.lab_job_runs`: última corrida 11:04:48 UTC; 36 corridas/última hora; 397 hoy, 372 ayer | PROD | **RECUPERADO (cierra AUD-01)** |
| PostgreSQL .220 | `numbackends('echo')=5`; account_sync/max(updated_at) hace segundos | PROD | UP |
| Hasura .48 | v2.38.0, metadata consistente | PROD | UP |
| etcd .250–.254 | `/echo/production/` 32 keys, lectura RO OK | compartido | UP |
| Terminales | 18 cuentas en métrica de bridge (6 TTP + 2 FTMO + 10 real, incluida la nueva 80581422) | Windows | 17/18 conectadas |

Límites: sin SSH no hubo `ps aux`/`ss -tlnp` (procesos, listeners y binarios de .71 no re-verificados hoy; el snapshot vigente es el de ayer 13:40–14:00 UTC); Kafka PROD sin capability (lag no medible; AUD-04 vigente); hosts Windows sin acceso directo.

### D. Respuesta directa a la pregunta del owner: "¿por qué no entra en operaciones?"

Cadena causal demostrada con evidencia:

1. El pipeline está sano: desde 2026-09-21 14:00 UTC se persistieron 16 trades REFERENCE (NDX, GDAXI, USDJPY, XAUUSD) con tickets de broker y `created_at` en el segundo del evento; cierres de hoy (USDJPY 11:41 UTC) procesados por `close_handler`; cero duplicados; `active_positions=0` == cero legs EXECUTION abiertas (consistencia).
2. La copia es **selectiva por estrategia**: el universo de estrategias con copia histórica son 18 (`account_strategy_risk_policy`; NDX 250901045/048/050, USDJPY 251002044/047/049/052/053/054 y 260104004, GOLD 2506/2509). De las señales desde ayer 14:00, **ninguna** pertenece a ese set salvo el fanout de GDAXI 251002014 — las NDX de anoche (2510020xx, 250901047/049) y las USDJPY de hoy (260104008/011) son reference-only por diseño. Sin WARN alguno: no llegan a intentarlo.
3. El único intento de copia real de la ventana (GDAXI 251002014, hoy 09:52 UTC, 8 cuentas candidatas) falló completo: 4 excluidas por estado (ARCHIVED ×3, CLOSE_ONLY 130339 — comportamiento correcto, WARN "account state does not accept opens") y 4 ACTIVE (183623, 431019411, 80570850, 80575718) abortadas en `mm_engine` con **`FIXED_RISK requires InstrumentSnapshot but it's nil`** (MM_CALCULATION_ERROR).
4. Causa raíz del punto 3: **`echo.symbol_mappings` no contiene ninguna fila para GDAXI** (sólo NDX y USDJPY, 13 filas; GDAXI nunca tuvo una fila EXECUTION en todo el historial del journal). Sin mapeo canónico→símbolo de broker, las terminales de las cuentas de ejecución no resuelven GDAXI y el snapshot de instrumento llega nulo. La config de riesgo de 251002014 existe desde 2026-04-04 ⇒ **todas las señales GDAXI copiables mueren en silencio desde abril**. No fue causado por los cambios recientes del owner.
5. La señal copiable más reciente que sí funcionó fue la copia NDX de ayer 13:44 (`magic_250901048`, 2 legs con tickets 63121779/23149775) — trazada por la auditoría de ayer. Esa estrategia no ha vuelto a disparar desde entonces.

Conclusión: no hay rotura; hay (i) azar de qué estrategias dispararon y (ii) un gap de config GDAXI antiguo que conviene cerrar (AUD-10) si se espera que la cohorte 2510 de GDAXI copie.

### E. Matriz G1–G10

| Gate | Resultado | Justificación (evidencia) |
|---|---|---|
| G1 INVENTORY | DEGRADED | Topología demostrada por telemetría (core/gateway/bridges/lab-worker/PG/Hasura/etcd); sin SSH no se re-observaron procesos/listeners de .71 (gap nuevo de esta sesión, no del sistema). |
| G2 RUNTIME | DEGRADED | Liveness por servicio demostrado con timestamps frescos (core 11:12Z hoy, gateway 21-sep 15:46Z, bridges 11:05Z, lab 11:04Z) y service.version 2.0.0; PID/arranque/SHA binarios = EVIDENCE_GAP sin SSH (AUD-03 vigente). |
| G3 CONFIG | PASS | ETCD `/echo/production/` 32 keys (igual que ayer), valores idénticos al baseline (Kafka .247–249:9092, PG .220/echo, gateway localhost:9090, pipe `echo_`, functions on); cero filtración DEV (nada apunta a .44/.161/echo-develop); password ETCD válida por evidencia funcional (lab-worker autenticando a PG 36×/h, account_sync hace segundos). |
| G4 SERVICES | PASS | Lab **recuperado** (AUD-01 cerrado: 397/372 corridas día, recencia segundos); PG 5 backends; Hasura consistente v2.38.0; bridges 17/18 (la 18 = 130339 CLOSE_ONLY deliberado, AUD-12); gateway al día en config. |
| G5 TRANSPORT | PASS | `trade_journal` persistiendo al segundo; cierres del día procesados; `ClientConfig published to Kafka` fresco (21-sep 15:46Z). Nota: `created_at−opened_at` en filas REFERENCE es −3 h **por diseño del dato** (hora de broker UTC+3 en `opened_at`, artefacto histórico AUD-11) — no interpretarlo como latencia del pipeline; la frescura real la demuestra `created_at`. |
| G6 DATA | PASS | 0 duplicados (trade_id+account_id) desde el 20-sep; `active_positions=0` == legs EXECUTION abiertas 0; cuentas sincronizadas hace segundos; sin huérfanos. |
| G7 TRADING | PASS (pasivo) con hallazgo | Última copia completa con tickets: ayer 13:44 (NDX 250901048). Hoy cero copias por las causas de §D; el fanout GDAXI demostró exclusiones correctas y fallo determinista en mm_engine (AUD-10). Sin FAILED nuevos en la ventana. |
| G8 RISK | PASS (pasivo) | Fanout excluyendo en vivo cuentas ARCHIVED/CLOSE_ONLY (WARNs verificados con account/state exactos); exposición estable: 17 ACTIVE ≈ $1.257M, ARCHIVED ≈ $902k, CLOSE_ONLY ≈ $110k, INACTIVE ≈ $108k; sin legs abiertas sin dueño. |
| G9 OBSERVABILITY | PASS con gaps | Loki fluyendo (core/gateway/bridge/lab-worker/journal); label `level` permitió escanear WARNs de streams pesados sin line-filters; Prometheus fresco. Gaps carry-over: sin alerta de silencio del Lab (AUD-05), `echo_agent_*` stale, Jaeger sin verificar. |
| G10 CHANGE IMPACT | PASS | `origin/master` intacto en `5dd998f1` (sin despliegues PROD; los binarios corren desde ago/sep según snapshot de ayer); cambios de la ventana = config operacional vía Hasura→gateway (130339→CLOSE_ONLY 14:38Z, 183623 ACTIVE + execution policies de 250901048 15:46Z) + commit front **local** en master local `3596fc48` (hijo de `5dd998f1`, sin push, sin efecto PROD) + trabajo DEV Daedalus (contrato §5.7). ETCD PROD sin cambios. |

### F. Cambios de la ventana (2026-09-21 14:00 → 2026-09-22 11:15 UTC)

| QUÉ | CUÁNDO (UTC) | DÓNDE | AFECTA PROD? |
|---|---|---|---|
| Cuenta 130339 (WSF NEW!) → CLOSE_ONLY | 21-sep 14:38 | config cuentas (Hasura → gateway → Kafka) | SÍ, deliberado; su terminal aparece desconectada (0 en métrica bridge); sin posiciones abiertas ⇒ sin exposición huérfana (AUD-12) |
| Gateway publica ClientConfig 183623 ACTIVE (ALLOW_ALL, 4 símbolos) + "Published updated execution policies" de `magic_250901048` (6 policies) | 21-sep 15:46 | Kafka PROD | SÍ, operación normal de config; 183623 sigue ACTIVE y su fila de riesgo no cambió (updated_at 03-may) |
| Commit front `3596fc48` en **master local** de Daedalus (hijo directo de `5dd998f1`, sin push): secret Hasura DEV opcional en front | 22-sep 00:29 (-03) | repo local, sin push | NO (sólo repo/DEV; coincide con contrato §5.7) |
| Trabajo DEV en Daedalus (front :4173, Core/Gateway DEV, CORS allow-all DEV) | ventana | DEV | NO (namespace `/echo/development/`; ETCD PROD sin deltas) |
| Lab worker retoma corridas (recuperación de AUD-01) | observado continuo hoy | .71 | SÍ, positivo |
| Sin despliegues, reinicios ni migraciones en PROD Echo | toda la ventana | .71 | confirmado por config ETCD estable + telemetría continua |

### G. Evidencia E2E

**Muestra 1 — intento de copia GDAXI (2026-09-22 09:52 UTC, trade `01a0c92c-5180-7cab-8000-07b03fe541ab`):** referencia 2089125371 ticket 269561296 persistida al segundo; fanout de 8 cuentas: 4 rechazadas por estado (2089126183/2089126186/26221863 ARCHIVED, 130339 CLOSE_ONLY) y 4 (183623, 431019411, 80570850, 80575718) con `MM_CALCULATION_ERROR` nil-InstrumentSnapshot en mm_engine ⇒ cero legs EXECUTION. Trazabilidad WARN↔config 1:1 contra `account_strategy_risk_policy`.

**Muestra 2 — ciclo de referencia con cierre (21→22 sep, USDJPY `01a0c775` y `01a0c85a`, cuentas 2089126830):** abiertas 01:52/06:02 UTC, cerradas 11:41 UTC hoy con precios; `close_handler` reportó "no open executions found" (correcto: eran reference-only). Persistencia y dedup OK.

**Muestra 3 — Lab vivo:** `lab_job_runs` última corrida 11:04:48 UTC con 36 corridas en la última hora (baseline sano ~860/día según auditoría 2026-08-21; hoy 397 al momento del corte).

No se generaron operaciones nuevas (prohibido read-only); sin inspección directa de terminales Windows (sin capability).

### H. Estado de trading y riesgo

- Terminales: 17/18 conectadas (`echo_bridge_executions_connected`); 130339 fuera (AUD-12). Nueva serie 80581422 "Orion 250%Refund" ARCHIVED conectada al bridge (ruido menor, AUD-13).
- Posiciones: 0 EXECUTION abiertas; 6 referencias GDAXI abiertas (estrategias 2510/2509) sobre 2089125371; journal↔positions consistente.
- Exposición (balances agregados, sin PnL derivado): ACTIVE 17 ≈ $1.257M; ARCHIVED 20 ≈ $902k; CLOSE_ONLY 1 ≈ $110k; INACTIVE 11 ≈ $108k (stale desde junio, esperado).
- Fallos de ejecución: sin FAILED nuevos en la ventana; los 3 históricos (4109) siguen acotados.
- Controles: exclusiones por estado operando en vivo con motivo exacto; HWM/automation activos; sin desconecciones no explicadas.

### I. Hallazgos

- **AUD-10 · P2 · TRADING_CONFIG — GDAXI sin mapeo de símbolo: copias imposibles desde abril.** Evidencia: 4×WARN `MM_CALCULATION_ERROR` (09:52 UTC) con `FIXED_RISK requires InstrumentSnapshot but it's nil`; `symbol_mappings` sin filas GDAXI (sólo NDX/USDJPY); riesgo de 251002014 vigente desde 2026-04-04; cero EXECUTION GDAXI en todo el journal. Impacto: toda señal GDAXI copiable se pierde silenciosamente (sólo WARN en Loki, sin alerta). Causa: demostrada (gap de config, no código). Owner: decidir si GDAXI debe copiar → agregar filas `symbol_mappings` (GDAXI→símbolo por broker de las 8 cuentas candidatas) y republicar config, o sacar GDAXI de la config de copia. Gate de regresión: próximo disparo de 251002014 genera ≥1 leg EXECUTION con ticket.
- **AUD-11 · P3 · DATA_HYGIENE — `opened_at` de filas REFERENCE trae hora de broker (UTC+3).** Evidencia: delta `created_at−opened_at` = −10798…−10800 s en 100% de filas REFERENCE de todos los días de la semana (medido 14–22 sep); legs EXECUTION mezclan +1–3 s y offsets por broker. Impacto: cualquier métrica de latencia sobre reference rows es inválida; la auditoría de ayer midió 1–2 s sobre legs de ejecución (válido). Acción: normalizar zona horaria en ingesta o documentar la semántica por columna; sin urgencia.
- **AUD-12 · P3 · CONFIG — 130339 CLOSE_ONLY + terminal desconectada.** Cambio humano ayer 14:38 UTC; bridge reporta `connected=0`; balance $110k; sin posiciones abiertas ⇒ sin riesgo inmediato. Acción: confirmar que la desconexión es intencional y que no hay legs pendientes de cerrar en esa cuenta.
- **AUD-13 · P3 · HYGIENE — 80581422 "Orion 250%Refund" ARCHIVED conectada al bridge.** Ruido de inventario; el planner la excluye por estado. Incluir en el próximo mantenimiento de terminales.
- **AUD-01 · CERRADO — Lab recuperado.** 397/372 corridas día con recencia de segundos; la causa raíz de los gaps del fin de semana sigue sin demostrarse (owner nunca reportó qué ejecutó a las 01:58/13:10 UTC del lunes); mantener el gate de 72 h de recencia y la alerta pendiente (AUD-05).
- **Carry-over vigente:** AUD-02 (merge a master del fix de seed tests `4aad647b` — el master local `3596fc48` **no** lo contiene; un `go test ./...` desde master puede volver a romper la password ETCD de ambos ambientes), AUD-03 (SHA binarios PROD), AUD-04 (Kafka PROD RO), AUD-05 (alertas de silencio/errores), AUD-08 (verificación mod_revision `/sqx-flowkit/production/`).

### J. Riesgos no verificables (EVIDENCE_GAP)

- Procesos/listeners/binarios de `.71` hoy (sin SSH esta sesión): el snapshot vigente es el de ayer 13:40–14:00 UTC.
- Lag/backlog de Kafka PROD (sin capability RO; AUD-04).
- Estado físico directo de terminales MT4 (mediado por bridge).
- Valor de `/echo/production/postgres/password` (secreto excluido por diseño; validez demostrada funcionalmente).
- Causa raíz original de los gaps del Lab del fin de semana (cerrado operacionalmente, no forensemente).
- Contenido exacto de las 6 execution policies de `magic_250901048` republicadas ayer 15:46 (las filas de `account_strategy_risk_policy` no cambiaron, pero el payload publicado no es legible con estas capacidades).

### K. Comparación contra auditoría previa (2026-09-21)

| Dimensión | Ayer 13:40–14:00 UTC | Hoy 10:57–11:15 UTC | Delta |
|---|---|---|---|
| Transporte/persistencia | vivo, 1–2 s | vivo, al segundo (created_at) | sin regresión |
| Lab pipeline | silencioso (AUD-01 P1) | 36 corridas/h, recencia segundos | **MEJORA, AUD-01 cerrado** |
| Terminales | 18/18 | 17/18 (130339 fuera, deliberado) | cambio de config esperado |
| Copias | 1 copia NDX con tickets (13:44) | 0 copias (explicado en §D) | sin rotura; gap GDAXI expuesto (AUD-10) |
| ETCD PROD | 32 keys, password válida | 32 keys, valores idénticos, auth fresca | sin cambios |
| Git | master `5dd998f1` | ídem + commit front local sin push | sin efecto PROD |
| Exposición ACTIVE | ≈ $1.265M | ≈ $1.257M | estable |

### L. Veredicto operacional

**`OPERATIONAL_DEGRADED`** — no por una rotura nueva (no la hay: cero regresiones de infraestructura y la respuesta a la pregunta del owner está demostrada), sino porque (i) persisten las degradaciones demostradas sin causa raíz forense del período anterior (gaps del Lab cerrados operacionalmente pero no explicados) y los gaps de verificabilidad estructurales (SHA binarios, lag Kafka, y hoy además procesos `.71` sin SSH), y (ii) existe un defecto de config de trading activo desde abril (AUD-10) que pierde señales copiables en silencio. Ninguno de estos ítems compromete capital hoy; ninguno fue causado por los cambios recientes del owner. `INSUFFICIENT_EVIDENCE` no aplica.

## Fuentes

- Física (10:57–11:15 UTC): PostgreSQL RO (`pg_stat_database`, `trade_journal`, `accounts`, `active_positions`, `lab_job_runs`, `symbol_mappings`, `account_strategy_risk_policy`, `information_schema`), etcd RO (`/echo/production/` 32 keys, valores no-secretos), Loki/Prometheus ARGUS (Loki `P8E80F9AEF21F6940`: core WARN vía label `level`, gateway, lab-worker; Prometheus `PBFA97CFB590B2093`: `echo_bridge_executions_connected`), Hasura PROD RO (v2.38.0 consistente), git local Daedalus (`~/go/src/github.com/xKoRx/echo`).
- Documentales: [[Echo — Production Operational Audit 2026-09-21]] (baseline de regresión y hallazgos AUD-01…09), [[Echo + Echo Forge — Environment Contract]] §5.6–§5.7 y §7, [[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]].
