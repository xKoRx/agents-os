---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo - Cierre del Lab y Limpieza del Journal]]"
  - "[[Echo - Discovery y Estado]]"
  - "[[echo-core]]"
aliases:
  - reporte estado lab echo
  - reporte limpieza trade journal
tags:
  - kind/doc
  - area/echo
  - project/echo
  - change/report
created: 2026-08-21
updated: 2026-08-21
cssclasses:
  - wide
---

# Echo - Reporte de Estado Lab y Journal 2026-08-21

%% Naming: documento de evaluación autocontenido; puede leerse sin otro contexto del vault. %%

## Propósito

- Reporte **completo y autocontenido** del estado del ecosistema **Echo** (trading algorítmico propio) enfocado en dos objetivos: **terminar de limpiar `trade_journal`** y **terminar The Lab (Lab Clean)** tal como estaba planificado. Escrito para ser **evaluado por otra IA** sin acceso al resto del vault: incluye contexto, historia, contrato vigente, estado validado con evidencia, inventario de problemas y un roadmap propuesto.
- Toda la evidencia fue validada el **2026-08-21 (~20:45 -04 / 00:45 UTC 22-08)** en modo **estrictamente read-only** contra producción (host deploy `192.168.31.71`, PostgreSQL `192.168.31.220`, Hasura `192.168.31.48:8080`) y contra el repo (`~/go/src/github.com/xKoRx/echo`, monorepo, rama `master` @ `e25165ba`, working tree limpio). **No se hizo ninguna modificación** de código, datos ni configuración.
- Al final hay una sección **"Preguntas para el evaluador"** — las decisiones abiertas donde se busca una segunda opinión.

## Contenido

### 1. Qué es Echo (contexto mínimo)

- **Pipeline:** EAs MT4/MT5 en terminales Windows → Bridge (Windows, Named Pipes) → Kafka → Core (StateFun, Go) → ledger canónico `echo.trade_journal` en PostgreSQL → backoffice Vue 3 + Hasura GraphQL. Monorepo `xKoRx/echo` con generaciones v1 (deprecated), v2 (anterior) y **v3 (activa)**.
- **Roadmap general "Olympus"** (`v3/ROADMAP.md`, dic-2025→abr-2026): Watchtower (visibilidad) → Commander (control) → Shield (protección) → **The Lab (analítica — iteración vigente al pausar)** → Oracle. The Lab = quinto tab del backoffice, branding "Experimental Research & Strategy Backtesting Sandbox", tab interno "Strategy Lab".
- **La apuesta del Lab:** medir qué tan buena es realmente una estrategia en **R** (múltiplos del riesgo inicial), con datos confiables. Decisión fundacional: R se calcula contra el riesgo INICIAL del trade (nunca SL final/legacy), lo que exige congelar facts al OPEN. Arquitectura por capas L0→L7: journal → imports → canonical → outcomes/segments → curvas → snapshots → read models (Hasura) → auditoría de jobs (`lab_job_runs`), con worker batch `echo-lab-worker`.
- **Superficies de reportería:** (a) **Daily Ops** — tab 3 de Watchtower, maduro, matview `echo.mv_daily_operations` refrescada por pg_cron cada 10 s; (b) **The Lab** — analytics WIP activo.
- **Infra:** deploy vía `deploy-prod.sh` (systemd: echo-core, echo-gateway, echo-lab-worker + timer de 5 min; **no** deploya el bridge Windows — manual). Build vía `build_v3.sh`. Credenciales hardcodeadas en `deploy-prod.sh` (deuda de seguridad conocida; no se reproducen acá).

### 2. Historia: tres generaciones de arquitectura (reconstruida y validada)

- **(A) Lab legacy** — funciones/vistas SQL directamente sobre el journal. Muerto conceptualmente; sus funciones (`fn_strategy_kpis` y familia) siguen vivas en prod y consumidas por el front legacy.
- **(B) RFC-003 / Analytics Foundation** (~principios de mayo) — migraciones `029` (`raw_trade_events`, `raw_trade_imports`, `canonical_trades`, `analytics_job_runs`) y `030` (`execution_trade_pairs`, `strategy_reference_outcomes`). Implementado (migraciones, backfills, jobs SQL), hoy **dormante**: 8437 filas congeladas desde el 2026-05-04, cero writers Go vivos.
- **(C-vNext) `042_trade_journal_vnext`** — intento de meter analytics+auditoría+MM+DQ+correlación DENTRO del journal. **Rechazado** ("el journal se estaba convirtiendo en todo mezclado"). Nunca aplicado a prod tal cual.
- **(C-final) `043_trade_journal_canonical_minimal` + `045_trade_journal_event_vs_recorded`** — el pivot definitivo: "el journal guarda facts mínimos del trade por cuenta, nada más; analytics vive fuera". Es lo que corre en prod. El journal completo fue reconstruido desde cero ~2-jun (no queda ninguna fila anterior). **Cronología fina (git):** los números de migración definen el orden de aplicación, pero los commits se mezclan — `042` (06-may), `045` (13-may), `052` (19-may), `056` (22-may), `058` (25-may), `059`/`060` (28-may) y recién `043`+`057` el **31-may** (commit `5069c291`): el pivot canónico mínimo fue finalizado/restructurado al final, consistente con el journal reconstruido ~2-jun.
- **Extensiones post-contrato (mayo, no ratificadas en el contrato escrito):** `056` **reintrodujo `origin` y `comment`** en el journal para que `mv_daily_operations` las exponga; `057` corrigió el signo de `profit_net` (`profit_gross + commission + swap`) y `058` alineó el historial del Lab a ese signo; `059` añadió `max_open_delay_seconds` a las policies; `060` añadió estado `FAILED` + `error_code`/`error_message` al journal (51 filas FAILED ya existen en prod).
- **Saga nativas (agosto):** los terminales corren EAs pre-`0abdf720` (05-07) → los opens nativos llegaban incompletos (`lot_size=0`) → el core los rechazaba → journal NATIVE roto desde el 1-jun. Fixes: broker backfill en bridge + provisioning sin broker (14/19-08, `c8aa59a4`) y **síntesis del OPEN desde el CloseResult** en core (20-08, `e25165ba`, autorizada por el owner como excepción documentada a RFC-010). Resultado: las **primeras 18 filas NATIVE de la historia** aparecieron el 21-08 (06:00–17:59 UTC) — siguen siendo exactamente 18 al cierre de este reporte (sin nuevas; mercado cerrado el viernes).

### 3. Contrato vigente (reglas fundacionales, RFC-009 rev.8 + RFC-010)

- **Identidad:** `UNIQUE (trade_id, account_id)`; el mismo `trade_id` une las patas REFERENCE y EXECUTION del mismo ciclo. `account_role` (REFERENCE|EXECUTION) separado de `source_type` (ECHO|NATIVE|IMPORT|MANUAL_FIX).
- **Scope:** `trade_journal` guarda facts mínimos del trade por cuenta: identidad, lifecycle (OPEN/CLOSED + close_reason), precios, timestamps event/recorded, SL/TP (initial sellado + último conocido), riesgo (`risk_pips`/`risk_money`), P&L (`profit_gross/commission/swap/profit_pips`). **GENERATED en Postgres:** `profit_net`, `r_multiple = profit_pips / risk_pips` (estricto), `duration_seconds`. **Regla de oro:** si puede derivarse o pertenece a analytics, no vive en el journal. Fuera explícitamente: DQ flags, MM snapshot, `history_segment`, MAE/MFE, latencias, pairing, hashes.
- **Columnas prohibidas** (lista explícita del gate): `origin`, `trade_status`, `account_type`, `reference_trade_id`, `initial_risk_*`, `final_*`, `history_segment`, `data_quality_*`, `money_management_type`, `configured_*`, `risk_policy_id`, MAE/MFE, etc. — el léxico completo del vNext rechazado.
- **Timeline del Lab = `*_recorded`** (reloj Postgres; los clocks de broker/EA no son confiables). `*_event` queda como auditoría del clock de origen.
- **SaveOpen** (UPSERT por identidad): idéntico → idempotente; completa NULLs → permitido; facts distintos → **conflicto explícito** (`ErrTradeJournalOpenConflict`, etc.). **SaveClose** escribe solo facts de cierre. **CLOSE sin OPEN → rechazo + log + métrica** (`ErrCloseWithoutOpen`; se rechazó `fallbackInsertClose` — verificado: no existe en el código).
- **Curvas V1:** `R_CURVE` = acumulado de `r_multiple`; `CAPITAL_CURVE` = `profit_net` sobre capital virtual 10.000 USD. **Outcomes V1 = REFERENCE-only**, `result_R = r_multiple` sin recálculo. DQ pertenece al Lab.
- **Extensiones reales NO ratificadas en el contrato escrito:** (1) `origin` + `comment` reintroducidas por 056 (contra la lista de prohibidas); (2) estado `FAILED` + `error_code`/`error_message` (060) — rev.8 solo definía OPEN/CLOSED; (3) RFC-009 sigue "Propuesta rev.8" y RFC-010 "Draft" pese a estar mayormente implementados. El contrato escrito y el schema real divergen en esos puntos.

### 4. Estado validado (2026-08-21, read-only)

**Servicios (192.168.31.71):**

- echo-core `active` desde 20-08 22:26 (build del deploy con síntesis nativa; backup `pre-synthesis` presente). echo-gateway `active` desde 09-08 (build 05-07). echo-lab-worker: oneshot + timer cada 5 min, últimas runs hoy 20:28/20:33/20:38 -04 **SUCCEEDED**.
- Logs core desde 12:00 hoy: **0 ERROR**; incidente `mm_engine SNAPSHOT IS NIL` **no reapareció**; 29 WARN `close_handler: NO_OPEN_POSITIONS` (bursts 12:00-13:59, luego nada); 1 WARN `execution_planner: no execution policies found in cache`.

**`echo.trade_journal` (41 columnas):**

- Volumen: **2664 filas** (124 creadas hoy). Desglose: ECHO/REFERENCE 2287 CLOSED · ECHO/EXECUTION 306 CLOSED + **51 FAILED** + 2 OPEN · NATIVE/EXECUTION 18 CLOSED.
- **`origin` varchar(10) DEFAULT 'ECHO' PRESENTE** (la prohibida) junto a `source_type` varchar(16) con CHECK ECHO/NATIVE/IMPORT/MANUAL_FIX. `comment` varchar(255) también presente (no está en la lista de prohibidas del gate).
- GENERATED correctos: `r_multiple` (con guards NULL/0), `profit_net`, `duration_seconds`; `profit_pips` NO generated (correcto según contrato). Constraints 11/11 OK; UNIQUE(trade_id, account_id) OK.
- Calidad: **63 CLOSED sin `r_multiple`** (45 ECHO/REFERENCE + 18/18 NATIVE con `risk_pips` NULL). Cobertura LIVE REFERENCE: `risk_pips` 98.03%, `profit_net` 100%, `r_multiple` 98.03%. Drift |recorded−event| promedio **~3.1 h** (reloj de broker desviado; en varias NATIVE `opened_at_event` es POSTERIOR a `created_at`). NATIVE: duraciones ≈3h exactas (10798–10800 s) → `opened_at_ms` del EA legacy parece sintético.

**Gate oficial (`v3/sdk/postgres/scripts/lab_clean_readiness_check.sql`):**

- **Roto tal cual commiteado:** 4 CTEs con anotación de tipo inválida en PostgreSQL (`WITH required(name text)`, `WITH forbidden(name text)`, `WITH required_policy_col(name text)`, `WITH expectations(col text, expected_not_null boolean)` — líneas 13/57/194/389). Ejecutado el original con `ON_ERROR_STOP`: `ERROR: syntax error at or near "text"`, caret bajo `text`, exit 3. **Ningún veredicto puede salir de este archivo sin parche local.**
- Con copia corregida en /tmp (solo se quitó la anotación de tipo): **`summary|1|1|NO_GO`**.
  - **Blocker (1):** `origin` FAIL_PRESENT. Único. Todo lo demás verde: 38/38 columnas requeridas, GENERATED OK, constraints OK, event/recorded 100%, `v_trade_execution_delta` OK, columnas de policy 16/16.
  - **Warn (1):** `policy_row_coverage_pct = 0.00%` (umbral 80).
- El veredicto documentado en `v3/docs/lab/00-trade-journal-readiness.md` sigue siendo el BLOCKED de mayo — no hay GO registrado jamás.

**Por qué existe `origin` (cadena de dependencias):** la migración `056` (commit `4e8caa1b`, 22-may) la reintrodujo **a propósito** porque `mv_daily_operations` (Daily Ops) hace `SELECT tj.origin, tj.comment` y el front distingue operaciones NATIVE vs ECHO con ella. Los fixes de agosto (broker + síntesis nativa) escriben `origin='NATIVE'` además de `source_type='NATIVE'` (ambas columnas se setean en paralelo — semántica redundante). **Eliminarla** exige: migración que reescriba la matview con `source_type`, DROP de la columna, y ajustar `sdk/postgres/trade_journal_open.go` (insertOpenRowTx/updateOpenRowTx), `trade_journal_repository.go` (SaveClose), campo `Origin` del dominio, telemetría core y queries GraphQL del front.

**Pipeline Lab (worker cada 5 min, 64.897 job runs):** `lab_canonical_trades` 2611 · `lab_strategy_outcomes` 2287 (100% vía source_type ECHO — REFERENCE-only en la práctica; la tabla no tiene columna account_role) · `lab_strategy_segments` **0 filas** (los segmentos TRAINING/PRE_LIVE/LIVE no están poblados) · `lab_import_batches/rows` 0 (path IMPORT_HISTORICAL sin uso; existe solo un stub en el worker) · `lab_equity_curve_points` 4529 (2287 CAPITAL + 2242 R) · `lab_strategy_metric_snapshots` 9284, fresquísimas (última write hoy 20:43 -04). Últimas 5 runs SUCCEEDED con error_count=0.

**Policies (`account_strategy_risk_policy`):** 351 filas, 25 cuentas (15 ACTIVE / 9 ARCHIVED / 1 INACTIVE), 136 `strategy_id` tipo `magic_*`, `valid_until` NULL en todas, updates 03→25-may. **Cruce con trades REFERENCE CLOSED: 0 matches** (ni pares ni cuentas) → explica el warn del gate: los `strategy_id` de las policies no corresponden a los de los trades cerrados. Es un desalineamiento de provisioning/diseño, no un problema del journal.

**Daily Ops (`mv_daily_operations`):** 0 filas. pg_cron: 2 jobs de `REFRESH ... CONCURRENTLY` cada 10 s, hoy 17.252 runs succeeded / 0 failed. **Causa del vacío (cerrada con queries):** (1) la matview es "operaciones desde el último reset diario HWM" y el `daily_hwm_reset_at` de las 17 cuentas ACTIVE rueda 22:00–23:00 UTC — después del último close de hoy (viernes 17:59 UTC, cierre de mercado) → vaciamiento vespertino **esperado por diseño de ventana**; (2) además el filtro `status='ACTIVE'` excluye **102 de los 124 trades de hoy** (cuentas INACTIVE). Universo real de cuentas: **48** (17 ACTIVE / 20 ARCHIVED / 11 INACTIVE) — **CORRECCIÓN:** el "2186 cuentas INACTIVE" reportado el 20-08 era falso.

**Legacy / Etapa 10 parcial:**

- RFC-003 dormante: `raw_trade_imports` 8437 + `canonical_trades` 8437 (congeladas 05-04), `raw_trade_events` 0, `execution_trade_pairs` 0, `analytics_job_runs` 13. Cero writers Go (solo funciones SQL de 029 y tests).
- `052` dropeó: `mv_strategy_overview`, `v_strategy_screener`, `strategy_reference_outcomes`, `strategy_metric_snapshots`, `strategy_virtual_equity_points`, 4 funciones `fn_strategy_*` y **solo 4** tablas `lab_out_*` (drawdown_summary, r_distribution, equity_base100, detail_summary). **Las demás `lab_out_*` siguen vivas en prod** (31 tablas lab_* totales), sin consumidor identificado en el stack clean.
- stage0_audit.sql (v3/scripts/analytics_v3/) audita el schema vNext/042 muerto → **DEAD**, no corre limpio contra post-043.
- Front dual-stack: (a) **legacy** `journal.js` + `strategyLensProvider` — consulta `echo_mv_strategy_overview` (**dropeada por 052 → queries rotas**) y funciones vivas (`fn_strategy_kpis`, familia execution-fidelity); (b) **clean** `strategyLabClean.js` + `strategyLabCleanProvider` — `v_lab_strategy_screener` + `fn_lab_*`. El account selector del Lab usa `getExecutionAccountsRanking` de journal.js (dependencia cruzada viva).
- Git: `master` @ `e25165ba` (20-08, pusheado; CORRECCIÓN: el "c8aa59a4" del estado del discovery era el commit previo), working tree limpio, un stash del 20-05 (52 archivos: ~98% junk de node_modules + 7 de código real, entre ellos un +5 sobre la migración 047 **ya aplicada** — pop riesgoso).
- Hasura `.48` healthy (healthz OK). Metadata del repo no trackea `mv_daily_operations` ni `v_trade_stream` (drift con la instancia live; la referencia `.75` del env del front está obsoleta).

### 5. Inventario consolidado de problemas

**BLOCKERs (impiden el objetivo "gate GO"):**

1. Columna prohibida `origin` presente en `trade_journal` (reintroducida por 056; leída por `mv_daily_operations`; escrita en paralelo a `source_type` por los fixes de agosto) → gate `NO_GO`.
2. Script del gate roto tal cual commiteado (4 CTEs tipados, sintaxis inválida en PostgreSQL) → el gate oficial no es ejecutable sin parche local no commiteado.

**WARNs / estados parciales:**

3. `policy_row_coverage_pct = 0%`: 351 policies (strategy_id `magic_*`) sin ningún match contra los trades REFERENCE CLOSED.
4. 63 CLOSED sin `r_multiple` (45 ECHO/REFERENCE dispersos + 18/18 NATIVE sin `risk_pips`); sin flags DQ en el modelo canónico, son invisibles para el usuario.
5. Calidad del path NATIVE: `risk_pips` NULL en todas, duraciones ≈3h sintéticas, drift event↔recorded ~3.1 h con `opened_at_event` a veces posterior al recorded.
6. `lab_strategy_segments` vacía (0 filas) y `lab_import_*` sin uso (path IMPORT_HISTORICAL = stub) — partes del diseño RFC-009 sin operar.
7. Etapa 10 parcial: tablas RFC-003 dormantes (8437+ filas), `lab_out_*` restantes vivas, front dual-stack con queries legacy rotas (`mv_strategy_overview` dropeada), account selector dependiente del stack legacy.
8. Daily Ops: vaciamiento vespertino por ventana HWM (¿semántica deseada?) + filtro ACTIVE que oculta ~82% de la actividad de hoy (102/124 trades en cuentas INACTIVE; universo 48 cuentas).
9. Drift documental: RFC-009 "Propuesta"/RFC-010 "Draft" vs implementación real; extensiones no ratificadas (`FAILED`+`error_*` de 060, `origin`/`comment` de 056); docs Stage 0 y `stage0_audit.sql` huérfanos; Makefile raíz y `ESTRUCTURA_PROYECTO.md` describen v1.
10. Seguridad/ops: password único reutilizado (ssh sudo/PG/Hasura), secret de Hasura en `.env` público del front, `deploy-prod.sh` no deploya el bridge (manual no trazable), metadata Hasura desalineada.
11. Stash del 20-05 sin decidir (7 archivos reales + junk; conflicto potencial con 047 aplicada).

**Mejoras confirmadas hoy (para no re-abrir):** incidente `SNAPSHOT IS NIL` no reaparece; worker y pipeline Lab sanos; 0 ERROR en core; síntesis nativa verificada funcionando (18 NATIVE); `fallbackInsertClose` no existe; los 4 errores RFC-010 presentes; cero writers Go al legacy.

### 6. Tensiones de diseño abiertas (el corazón de la evaluación)

1. **`origin` vs `source_type`:** el contrato final prohíbe `origin`, pero Daily Ops la usa para distinguir NATIVE y los fixes de agosto la escriben. Salidas posibles: (a) eliminar `origin` consolidando en `source_type` (tocando matview+repo+dominio+core+front) — restaura el contrato; (b) legitimar `origin` actualizando el gate — rompe la regla de oro "una fuente por hecho" y el contrato rev.8. Nota: ambas columnas ya viajan en paralelo con la misma información en el path NATIVE, así que (a) no pierde información.
2. **Síntesis NATIVE (`e25165ba`):** fabrica el OPEN desde el CloseResult — exactamente lo que RFC-010 rechazó para no esconder bugs. Justificación: EAs legacy en terminales nunca enviarán el open completo. Debería volverse inerte al redeployar EAs; retirarla después requiere decisión explícita (¿cuándo? ¿con qué criterio de verificación?).
3. **Estado `FAILED` (060):** 51 filas reales usan un estado que el contrato escrito no define. ¿Se ratifica en RFC-010 (con su ciclo de vida: quién abre/cierra un FAILED, qué facts exige) o se revisa?
4. **Semántica de Daily Ops:** ¿"desde el último reset HWM" es lo que el usuario quiere ver (hoy muestra vacío las tardes/noches post-reset)? ¿Y el filtro ACTIVE con 102/124 trades de hoy en INACTIVE?
5. **Segmentación del Lab:** `lab_strategy_segments` vacía — ¿el diseño TRAINING/PRE_LIVE/LIVE sigue siendo objetivo o se descarta del V1?

### 7. Roadmap propuesto (detalle en [[Echo - Cierre del Lab y Limpieza del Journal]])

- **Fase 0 — Decisiones (bloquean todo):** D1 `origin` vs `source_type` (recomendado: eliminar) · D2 síntesis NATIVE (mantener hasta EAs nuevos, luego retirar con decisión) · D3 Daily Ops (ventana HWM + cuentas no-ACTIVE) · D4 stash 20-05.
- **Fase 1 — Cerrar el gate (GO):** G1 commitear fix de los 4 CTEs (independiente, barato) · G2 migración de salida de `origin` (matview+columna+código+front, con tests) · G3 resolver/explicar policy coverage 0% · G4 re-correr gate y documentar GO en `00-trade-journal-readiness.md`.
- **Fase 2 — Etapa 10 completa:** E1 inventario final pre-borrado · E2 archivar RFC-003 (backup + DROP) · E3 archivar stage0_audit + docs · E4 unificar front del Lab (migrar account selector, remover stack muerto) · E5 destino de `lab_out_*` restantes.
- **Fase 3 — Calidad nativos:** N1 redeploy EAs actuales en terminales (confirmar antes cuál EA emite el open nativo: `execution_agent_v3` según historia operativa vs `reference_v3` según inspección de código del 21-08) · N2 `opened_at_ms` sintético · N3 backfill opcional 1-jun→20-08 · N4 visibilidad DQ de los 63 sin R.
- **Fase 4 — Contrato/robustez:** C1 test real de repositorio del UPSERT · C2 retry/DLQ execution · C3 promover RFCs y ratificar extensiones (056/060).
- **Fase 5 — Seguridad/ops:** S1 rotar password único + secret del front · S2 metadata Hasura · S3 docs de raíz + runbook bridge.
- Orden crítico sugerido: **G1 primero** (fix de sintaxis, independiente, desbloquea poder correr el gate en cualquier momento), luego **D1→G2→G4** para el GO, y N1 en paralelo (habilita retirar la síntesis y cerrar D2).

### 8. Preguntas para el evaluador

1. ¿Eliminas `origin` (migración + matview + código) o actualizas el gate para legitimarla? ¿Algún argumento para mantener dos columnas con la misma semántica en el path NATIVE?
2. ¿Cómo manejarías la retirada futura de la síntesis NATIVE: criterio objetivo (N días sin síntesis tras redeploy de EAs), o decisión manual del owner?
3. El warn de policies (0%): ¿lo tratarías como (a) dato stalkeado a limpiar, (b) bug de provisioning de `strategy_id`, o (c) diseño correcto y el gate debería relaxar el umbral?
4. ¿Ratificarías `FAILED` + `error_*` en RFC-010 tal como quedó en 060, o rediseñarías el lifecycle antes de más código encima?
5. Priorización del roadmap: ¿estás de acuerdo con G1→D1→G2→G4 como camino crítico, o cambiarías el orden (p.ej.security S1 antes de tocar el journal)?
6. ¿Algo que falte en el inventario de Etapa 10 o riesgos no considerados en las fases 2-5?

## Fuentes

- Validación prod read-only 2026-08-21 (~20:45 -04): systemctl/journalctl en `192.168.31.71`; psql en `192.168.31.220` (db `echo`): `\d echo.trade_journal`, counts por source_type/account_role/status, gate original + copia corregida (`summary|1|1|NO_GO`), inventario lab_*/views/routines, policies, matview + pg_cron, queries de elegibilidad HWM/ACTIVE; Hasura `.48:8080/healthz`.
- Validación repo read-only 2026-08-21: git (HEAD `e25165ba`, stash, branches); migraciones 042-060 leídas; `lab_clean_readiness_check.sql` verificado línea a línea (CTEs tipados en 13/57/194/389); grep de `origin`/`source_type` en sdk/core/bridge/front; consumidores front (`journal.js`, `strategyLensProvider`, `strategyLabClean*`); writers legacy (cero Go); RFC-009/010 y `trade_journal_errors.go`; lab-worker (jobs y tablas); EAs (`reference_v3`/`execution_agent_v3`); `deploy-prod.sh`/`build_v3.sh`.
- Historia y contrato: reconstrucción del 20/21-08 en [[Echo - Discovery y Estado]] (handoffs del owner + auditorías previas), `v3/ROADMAP.md`, `v3/docs/lab/*`, `v3/docs/rfcs/RFC-009*`, `RFC-010*`.
