---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P2
area: "[[Echo]]"
parent:
sprint:
start: 2026-08-20
due:
progress: 75
repo: xKoRx/echo (~/go/src/github.com/xKoRx/echo)
jira:
prs:
aliases:
  - echo discovery
  - echo recap
  - Echo Discovery
tags:
  - project/echo
  - kind/project
  - area/echo
created: 2026-08-20
updated: 2026-09-07
cssclasses:
  - wide
---

# Echo - Discovery y Estado

%% Naming: Echo - Discovery y Estado es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo - Discovery y Estado
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P2 · **Sprint:** —
> **Repo:** `xKoRx/echo` (`~/go/src/github.com/xKoRx/echo`) · **Inicio:** 2026-08-20
> Proyecto de **comprensión** (discovery/recap) del ecosistema echo-core: entender código, reportería y estado actual. [[Echo Forge]] es un proyecto distinto.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[Echo - Discovery y Estado]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- Recuperar el estado completo del ecosistema **echo** (core, no forge): qué existe, dónde está el código, en qué versión está (v1/v2/v3), qué quedó a medio hacer y cómo sigue la reportería.
- Identificar el nombre y ubicación reales del subsistema de reportería que se estaba avanzando (el owner olvidó el nombre; hay que dejarlo documentado con evidencia).
- Documentar el **norte del proyecto** (Roadmap Olympus / Analytics V3), el **estado real de sus etapas** y la deuda abierta, con las fuentes que lo respaldan.
- Dejar un recap consolidado y retomable: cualquier agente fresco debe poder continuar desde esta nota sin preguntar nada.

## 🧭 El norte: Olympus → The Lab → Analytics V3

**La ambición** (Roadmap Olympus, `v3/ROADMAP.md`, dic-2025 → abr-2026): backoffice propio en 5 iteraciones — Watchtower (visibilidad) → Commander (control) → Shield (protección) → **The Lab (analítica)** → Oracle (lógica avanzada). La iteración vigente al pausar el proyecto era **The Lab**: saber **qué tan buena es realmente una estrategia**, con datos confiables, comparando en **R** (múltiplos del riesgo inicial) para que el sizing monetario no distorsione la señal. En el front es el quinto tab, "The Lab" (branding: *"Experimental Research & Strategy Backtesting Sandbox"*; tab interno "Strategy Lab").

**Por qué R, y por qué rehacer desde la base**: las estrategias usan ATR para el SL y sizing por riesgo fijo (USD 200/2000), entonces 1R del lunes ≠ 1R del viernes en distancia de precio, y el trailing mueve el SL durante el trade. Decisión fundacional: **R se calcula contra el riesgo INICIAL del trade, nunca contra el SL final ni el legacy**. Eso exige congelar al OPEN: `initial_stop_loss`, `initial_risk_pips`, `initial_risk_money` + snapshot de MM (`money_management_type`, `configured_risk_amount/currency`, `risk_policy_id`).

**Reglas fundacionales — contrato FINAL vigente (canonical minimal 043+045, RFC-009 rev.8, RFC-010)**:
- **Identidad**: `UNIQUE (trade_id, account_id)`. El mismo `trade_id` une las patas REFERENCE y EXECUTION del mismo ciclo (correlación por identidad; nada de `reference_trade_id`/`master_trade_id`). `account_role` (REFERENCE|EXECUTION) separado de `source_type` (ECHO|NATIVE|IMPORT|MANUAL_FIX).
- `trade_journal` guarda **facts mínimos del trade por cuenta, nada más**: identidad, lifecycle (status OPEN/CLOSED + close_reason), precios, timestamps event/recorded, SL/TP (initial_* sellado + último conocido), `risk_pips`/`risk_money`, `profit_gross/commission/swap/profit_pips`. **GENERATED en Postgres**: `profit_net`, `r_multiple = profit_pips / risk_pips` (estricto; nunca `profit_net/risk_money` ni R paralela), `duration_seconds`.
- Regla de oro del scope: **si puede derivarse desde facts mínimos o pertenece a analytics, no vive en `trade_journal`**. Fuera explícitamente: DQ flags, MM snapshot (`configured_*`, `money_management_type`, `risk_policy_id`), `history_segment`, MAE/MFE, latencias/slippage, pairing, hashes/event ids.
- **Timeline del Lab = `*_recorded`** (reloj Postgres; los clocks de broker/EA no son confiables — 045 añadió event/recorded por eso). Duration del Lab coherente con recorded. `*_event` queda como auditoría del clock de origen.
- **SaveOpen** (UPSERT por `(trade_id, account_id)`): idéntico → idempotente; completa NULLs → permitido; facts distintos → **conflicto explícito, nunca last-write-wins silencioso**. Facts sellados: ticket, open_price, opened_at, side, lot_size, símbolos, risk_pips/risk_money, initial SL/TP. **SaveClose** escribe solo facts de cierre; nunca toca GENERATED.
- **CLOSE sin OPEN → no insert + log + métrica** (`close_without_open` como gap operativo visible; se rechazó `fallbackInsertClose` para no esconder bugs). Errores: `ErrCloseWithoutOpen`, `ErrTradeJournalOpenConflict`, `ErrTradeJournalCloseConflict`, `ErrTradeJournalOpenAfterClosed`.
- **Curvas V1**: `R_CURVE` = acumulado de `r_multiple`; `CAPITAL_CURVE` V1 = `profit_net` real sobre capital virtual inicial **10.000 USD**, labels `RECORDED_GLOBAL/RECORDED` (no FK). Sin simulación de policies, sin `lab_capital_policies`, sin fixed-lot/on-demand en V1. `account_strategy_risk_policy` existe operacionalmente y es **enriquecimiento read-only** desde Lab.
- **DQ pertenece al Lab** (flags en `lab_strategy_outcomes`: MISSING_RISK_PIPS, MISSING_PROFIT_PIPS, etc.), nunca al journal. **Outcomes V1 = REFERENCE-only**; `result_R = r_multiple` (sin recálculo).
- `lab_api_*` son **row shapes** (tipos de retorno `RETURNS SETOF`), NO storage ni worker que les escriba. `v_lab_strategy_screener` + `fn_lab_strategy_*` leen las tablas core. `v_trade_execution_delta` reservada para Execution Fidelity futura, no consumida por Strategy Analytics V1.
- V1 moneda: **USD** (sin `strategy_definitions.currency`). Unidad de `*_pips`: normalizada por tick_size del broker (no pips forex clásicos).
- La verdad nace en el runtime al abrir la señal; analytics nunca recalcula hacia atrás. Prohibido: `UNKNOWN_FROM_EXECUTION`, `tickSize=0.0001`, R desde SL legacy/final, insertar sin metadata normativa (skip + log + métrica).
- Segmentos TRAINING/PRE_LIVE/LIVE viven en `lab_strategy_segments` (resueltos por `closed_at_recorded`), no en el journal.

> [!warning] Excepción documentada a RFC-010: síntesis NATIVE (20-08-2026)
> La síntesis `synthesizeNativeOpenFromClose` (commit `e25165ba`, autorizada explícitamente por el owner) **fabrica el OPEN desde el CloseResult cuando un close NATIVE llega sin open** — exactamente el tipo de "fila fabricada" que RFC-010 rechazó para no esconder bugs operativos. Justificación: los EAs legacy nunca enviarán el open completo (redeploy manual pendiente), y sin esto las nativas no existirían en el journal. Alcance acotado: solo NATIVE + solo ante `ErrCloseWithoutOpen`; queda como red de seguridad que debería volverse inerte (o eliminarse) cuando los EAs nuevos estén instalados en todos los terminales. Si algún día se retira, que sea decisión explícita del owner.
> **Doble tensión con el diseño final**: (1) el fix y el hotfix del 19-08 usan la columna `origin` ('NATIVE'), que rev.8 lista como **prohibida** (el contrato es `source_type` ECHO|NATIVE|IMPORT|MANUAL_FIX) — de hecho `origin` es hoy el **único blocker del gate de readiness** contra prod; (2) ver punto anterior. Resolver = migración que elimine `origin` + recodificar la clasificación NATIVE por `source_type` en sdk/core/bridge.

> [!warning] Materialización real vs specs: tres generaciones de arquitectura
> La historia tiene **tres generaciones** (reconstruidas 2026-08-21 con los handoffs del owner):
> **(A) The Lab legacy** — funciones/vistas SQL directamente sobre el journal (legacy, muerto conceptualmente).
> **(B) RFC-003 / Analytics Foundation** (~principios de mayo) — migraciones `029` (raw_trade_events, raw_trade_imports, canonical_trades, analytics_job_runs) y `030` (execution_trade_pairs, strategy_reference_outcomes); se implementó bastante (migraciones, backfills, jobs, tests). Restos pueden seguir vivos en repo/prod — clasificar antes de borrar nada.
> **(C-vNext) `042_trade_journal_vnext`** — intento de meter analytics+auditoría+MM+DQ+correlación DENTRO del journal; fue auditado y **rechazado** ("el journal se estaba convirtiendo en todo mezclado"). Nunca aplicado a prod tal cual.
> **(C-final) `043_trade_journal_canonical_minimal` + `045_trade_journal_event_vs_recorded`** — el pivot definitivo (~31-may/2-jun): "el journal guarda facts mínimos del trade por cuenta, nada más; analytics vive fuera". Esto es lo que corre en prod y es el linaje que importa para RFC-009.
> El spec vNext fat de la charla de mayo (familia `initial_*`, `data_quality_flags`, snapshot MM, `history_segment`, `strategy_definitions.currency`) quedó superado por C-final: en prod son `risk_pips`/`r_multiple` (GENERATED), sin flags/MM/segmentos; `043_currency` archivada sin aplicar. El norte conceptual (R contra riesgo inicial, verdad en el runtime) **sí** sobrevive.

**Arquitectura objetivo (RFC-009 "Analytics V3 / Strategy Lab V3 Clean")**:
`[L0] trade_journal vNext → [L1] lab_import_batches/rows → [L2] lab_canonical_trades → [L3] lab_strategy_outcomes + lab_strategy_segments + lab_capital_policies → [L4] lab_equity_curve_points → [L5] lab_strategy_metric_snapshots → [L6] read models Hasura (v_lab_strategy_screener, fn_lab_*, lab_api_*) → [L7] lab_job_runs (auditoría)`, con worker batch `echo-lab-worker` + dominio en `v3/sdk/lab`. La calidad se separa explícitamente en **Strategy Quality / Execution Fidelity / Account Impact / Data Quality / Historical Segment Analysis / MM Simulation** — nada de mega-score opaco.

**Métricas núcleo del panel**: `result_R, expectancy_R, median_R, profit_factor_R, SQN_R, win_rate, avg_win_R, avg_loss_R, payoff_ratio_R, largest_win/loss_R, total_R, max_drawdown_R, current_drawdown_R, recovery_factor_R` + cobertura (`result_R_coverage_pct, data_quality_score, missing_initial_risk_count, excluded_trades_pct`).

**Modelo de etapas con gate** (definido post-audit Stage 0):
- **Etapa 0 — Audit & Readiness**: existieron **dos auditorías** y está resuelto cuál manda: `v3/scripts/analytics_v3/stage0_audit.sql` (11-may, audita el vNext/042 muerto → **DEAD**, da BLOCKED por columnas inexistentes) vs `v3/sdk/postgres/scripts/lab_clean_readiness_check.sql` (13-14 may, doc `docs/lab/00-trade-journal-readiness.md`) = **el gate oficial vigente**. Ninguna corre en CI. **Veredicto real del gate contra prod (corrido 21-08-2026): `NO_GO`** — 1 blocker: la columna prohibida `origin` sigue presente en `echo.trade_journal`; 1 warn: `policy_row_coverage_pct = 0%` (351 políticas en `account_strategy_risk_policy` pero ninguna resuelve para los 2287 trades REFERENCE live). Resto verde: 0 columnas faltantes, GENERATED OK, constraints OK, event/recorded 100%, drift event→recorded promedio ~3.1h (reloj de broker desviado, esperable). **Además el script del gate está roto tal cual commiteado** (**4 CTEs tipados** `WITH x(name text)` = sintaxis inválida en PostgreSQL; líneas 13/57/194/389 — verificado ejecutándolo 21-08: `syntax error at or near "text"`) — el último "GO" documentado no pudo salir de este archivo sin una corrección local no commiteada. Deuda de tooling.
- **Etapa 0.5 — Journal Readiness Fixes** (Issues 1-7 del next_steps) + **RFC-010 (persistencia OPEN/CLOSE)**: el hilo histórico cerró su "Etapa 3" (tests core, SELECT→INSERT/UPDATE, 4 errores de conflicto, métricas) y dejó "Etapa 4" (E2E real + DB real + readiness) sin evidencia de cierre en ese hilo. Hoy los 4 errores RFC-010 existen (`trade_journal_errors.go`), `fallbackInsertClose` NO existe, y la síntesis NATIVE (20-08) es la única excepción.
- **Etapas 1..10 de Lab Clean (RFC-009)**: 1 schema base (046 core tables, 047 read models) · 2 SDK/domain · 3 worker skeleton/repos · 4 canonical builder · 5 outcomes builder · 6 curves builder · 7 metric snapshots builder · 8 read models/Hasura · 9 front · 10 legacy removal. **Estado verificado en prod (21-08)**: etapas 1-9 construidas y operando (worker con 21.628 runs de recompute + curvas + snapshots, última actividad hoy; front consumiendo `v_lab_strategy_screener` + `fn_lab_*`; outcomes 2287 filas 100% REFERENCE-only con `result_r`; `lab_canonical_trades` 2611 filas con timeline `*_recorded` conforme rev.8). La **Etapa 10 (legacy removal) está PARCIALMENTE hecha** vía migración 052 (dropeó `strategy_reference_outcomes`, `mv_strategy_overview`, `v_strategy_screener`, **solo 4 de las `lab_out_*`** y vistas viejas), pero quedan restos vivos (resto de `lab_out_*`, tablas RFC-003 dormantes, front dual-stack — detalle y fases de cierre en [[Echo - Cierre del Lab y Limpieza del Journal]]).

## 📊 Estado actual

- **Producto integrado — 2026-09-07:** el padre de producto es [[Echo — Producto Integrado]]; el track live es el subproyecto de agente [[Echo — Live Platform V1]] (E-01…E-13; E2 histórico partido). Esta nota conserva Discovery/historia, no el roadmap de ejecución. Contrato SDK B + FR-1…FR-5 en S0. Lab R AUTO money→pips→journal: el contrato nuevo exige base explícita, sin cambiar R pips histórico.


- **Qué es echo:** ecosistema propio de trading algorítmico en Go (monorepo `xKoRx/echo`): EAs MT4/MT5 → Bridge (Windows, Named Pipes) → Kafka → Core (StateFun) → ledger canónico `echo.trade_journal` en Postgres → backoffice Vue 3 + Hasura GraphQL. La versión activa es **v3**; `v1` está deprecated y `v2` es la generación anterior. El roadmap general es **"Olympus"**: Watchtower → Commander → Shield → Lab → Oracle (`v3/ROADMAP.md`).
- **La reportería (investigada 2026-08-20):** no es un servicio aparte; son dos superficies:
  - **Daily Ops** — reporte diario de operaciones, Tab 3 de **Watchtower** (`/watchtower`, tab `daily`). Datos: matview `echo.mv_daily_operations` (migraciones 001/056/057); UI: `v3/front/src/composables/useDailyOperations.js` + `OperationsGrid.vue`; API: suscripción GraphQL `echo_mv_daily_operations` vía Hasura. **Maduro.** Sobre esto era el último fix (ver abajo).
  - **The Lab** — el panel nuevo de analytics. En navegación se llama **"The Lab"** (`/lab`, quinto tab del backoffice); branding interno: **"Experimental Research & Strategy Backtesting Sandbox"** (`LabView.vue:6`); tab de analytics: **"Strategy Lab"** (id `strategyLabClean`, RFC-009 "Strategy Analytics Clean V1"). Worker batch `v3/lab-worker` (jobs `recompute`/`materialize-curves`/`materialize-snapshots` sobre `echo.lab_*`) + Lens Registry en el front (`echo_v_lab_strategy_screener`). **WIP activo**; fue donde hubo commits más recientes (hasta 2026-07-18) y de lo que trata el stash pendiente.
- **Estado git (actualizado 2026-08-21):** `master` @ `e25165ba` **pusheado a origin** (= `c8aa59a4` + el fix de síntesis nativa mergeado ff y pusheado el 2026-08-20 en la noche). Working tree limpio. Stash viejo (base 2026-05-20, 52 archivos: ~98% node_modules + 7 de código real, con +5 sobre la migración 047 ya aplicada) sigue pendiente de decisión.
- **Estado prod (auditado 2026-08-20, read-only):** host `192.168.31.71` — core = build hotfix del 19-08 22:28 (md5 idéntico al worktree), gateway = build 05-07, lab-worker = 14-07 (timer cada 5 min, OK), front nginx OK. Hasura real: `192.168.31.48:8080` (la referencia `.75` del env del repo está caída/obsoleta). Postgres `192.168.31.220`: pipeline vivo (inserciones ECHO hasta hoy), pg_cron refresca `mv_daily_operations` cada 10s con éxito, pero la matview tiene **0 filas**.
- **Por qué no se ven nativas en Daily Ops (causas raíz reales, 2026-08-20):**
  1. **CAUSA RAÍZ (cerrada con fix 2026-08-20, VERIFICADO funcionando 2026-08-21):** los terminales MT4/MT5 corren EAs pre-`0abdf720` (05-07): el open nativo viaja SIN `lot_size`/side/símbolos y el core lo rechazaba (`lot_size must be positive`). Solución deployada: **síntesis del OPEN desde el CloseResult** en el core (`NewTradeJournalOpenFromCloseResult`, commit `e25165ba`, deploy 20-08 22:26 con backup `echo-core.bak-20260820-pre-synthesis`). **Verificación empírica 21-08: 18 filas NATIVE (CLOSED, EXECUTION, GOLD) — las primeras NATIVE de la historia del journal** (06:00–17:59 UTC). Alertas de calidad del path NATIVE: las 18 tienen `risk_pips NULL` (el close legacy no trae SL inicial → sin R) y duraciones ≈3h exactas (10798–10800s en todas → el `opened_at_ms` que reporta el EA legacy parece sintético). Fix canónico pendiente del owner: recompilar EAs post-05-07 e instalarlos en terminales.
  2. **Daily Ops está vacío las tardes/noches por diseño de ventana (cerrado 21-08 con queries):** la matview muestra "operaciones desde el último reset diario HWM" y `daily_hwm_reset_at` rueda 22:00–23:00 UTC, después del último close (viernes 17:59 UTC) → 0 filas post-reset aunque el refresh de pg_cron corra bien cada 10 s (17.252 runs OK hoy). **CORRECCIÓN del dato del 20-08:** el universo de cuentas es **48** (17 ACTIVE / 20 ARCHIVED / 11 INACTIVE) — no existían "2186 INACTIVE". El filtro `status='ACTIVE'` igual excluye **102 de los 124 trades del 21-08** (~82%, en cuentas INACTIVE). Dos decisiones de producto abiertas: semántica de la ventana y visibilidad de cuentas no-ACTIVE (→ [[Echo - Cierre del Lab y Limpieza del Journal]] D3).
- **Deploy:** host único `192.168.31.71` vía `deploy-prod.sh` (systemd: core, gateway, lab-worker + timer). Build: `build_v3.sh`. OJO: `deploy-prod.sh` tiene credenciales hardcodeadas (ssh + Postgres + Hasura, mismo password reutilizado con sudo total) y **NO despliega el bridge** (Windows, manual no trazable).
- **Deuda conocida (actualizada 21-08):** (1) opens nativos con `lot_size=0` rechazados por el core (mitigado por la síntesis; fix canónico = redeploy de EAs → N1); (2) decisión de producto Daily Ops: ventana HWM vespertina + filtro ACTIVE que oculta ~82% de la actividad de hoy (universo real 48 cuentas → D3); (3) password único reutilizado (`ssh` con sudo, Postgres, Hasura) y secret de Hasura embebido en el `.env` público del front (→ S1); (4) `deploy-prod.sh` no despliega el bridge (manual, no trazable); (5) incidente 20-08 `mm_engine: SNAPSHOT IS NIL` — **sin recurrencia el 21-08** (0 ERROR en core); (6) referencia a Hasura `192.168.31.75` obsoleta en env del repo (el real es `.48`); (7) metadata Hasura en repo no trackea `mv_daily_operations` ni `v_trade_stream` (drift con instancia live); (8) Makefile raíz y `ESTRUCTURA_PROYECTO.md` describen v1; (9) **extensiones no ratificadas del contrato**: `origin`/`comment` (056) y estado `FAILED`+`error_*` (060) — migraciones 058-060 no estaban registradas en el vault hasta el 21-08; (10) front dual-stack: `journal.js` consulta `mv_strategy_overview` dropeada por 052 → queries legacy rotas; account selector del Lab depende del stack legacy (→ E4).

- **Pipeline Analytics V3 — estado real de etapas (evaluado 2026-08-21: resumen de mayo del owner + evidencia de repo + audit real contra prod):**
  - **Etapa 0 (Audit): DONE.** Corrida con psql real en develop (BLOCKED: 8437 CLOSED todos legacy, R coverage 0%, MM 0%) y en prod (BLOCKED_NO_VNEXT_MIGRATION: schema legacy de 38 columnas). Veredictos correctos: la etapa detectaba, no arreglaba.
  - **Etapa 0.5 (Journal Readiness Fixes): implementada y después SUPERADA POR UN PIVOT DE DISEÑO.** La charla de mayo (~11-18 may) implementó el spec "vNext" (UPSERT `ON CONFLICT (trade_id, account_id) DO UPDATE` + COALESCE para `initial_*`, contrato ReferenceEvent con R/MM, producers MT4/MT5 con `initial_risk_pips = |price−SL|/tickSize`, execution skip sin placeholders, scripts 042/043). **Pero prod nunca llegó a vivir en ese spec**: ~31-may/2-jun la tabla fue reemplazada por `043_trade_journal_canonical_minimal` — modelo canónico mínimo con `status`, `risk_pips` y `r_multiple` (columna GENERATED), **sin** `data_quality_flags`, sin snapshot MM (`configured_risk_amount` no existe), sin `history_segment`. El 042_vNext nunca se aplicó tal cual; el `043_strategy_definitions_currency` quedó **archivado sin aplicar** (`strategy_definitions.currency` no existe); y el journal completo fue **reconstruido desde cero el ~2-jun** (no queda ninguna fila anterior). El script oficial `stage0_audit.sql` sigue auditando el spec vNext muerto → por eso da BLOCKED hoy.
  - **Etapa 1 (Lab Clean): CONSTRUIDA Y CORRIENDO — el gate se saltó.** 31 tablas `lab_*` en prod (canonical, outcomes, segments, equity curves, snapshots, 17 `lab_out_*`, 6 `lab_api_*`, job_runs, imports), worker `echo-lab-worker` en prod (timer cada 5 min desde ~14-jul), front Strategy Lab. Sin re-audit READY documentado que lo autorizara.
  - **Gate 0.5 hoy (audit real 21-ago): formalmente BLOCKED, pero por desalineación script↔schema, no por datos.** Métricas equivalentes reales: **r_pct 97.59%** global CLOSED (2548/2611) y **98.03%** en REFERENCE (umbral READY ≥95); profit_net 100%; `r_multiple` usable 98.03%. MM: **inmedible** (la columna no existe en el modelo canónico). 63 CLOSED sin R (45 ECHO/REFERENCE dispersos + 18 NATIVE del 21-ago).
  - **Puntos finos del review de mayo — estado tras el pivot**: (1) flags pegados (`MISSING_INITIAL_RISK` con valor presente): **moot** — el mecanismo de flags no existe en el modelo canónico (contrapartida: nada marca los 63 trades sin R); (2) unidad ticks-vs-pips: vigente como decisión; (3) test real de repositorio del UPSERT: sigue pendiente; (4) retry/DLQ para execution: sigue pendiente.

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [x] Recuperar estado vault-side de echo (área, memoria, changelog) #owner/agent #type/research #area/echo
> - [x] Investigar estado git del monorepo echo (ramas, stash, fix pendiente) #owner/agent #type/research #area/echo
> - [x] Identificar el subsistema de reportería (nombre + ubicación + estado) #owner/agent #type/research #area/echo
> - [x] Auditar qué corre en prod (core/gateway/lab-worker/BD/Hasura, read-only) #owner/agent #type/research #area/echo
> - [x] Consolidar hotfix: verificado en prod → merge ff + push a master + limpieza de rama/worktree #owner/agent #type/dev #area/echo
> - [x] Documentar recap en esta nota #owner/agent #type/research #area/echo
> - [ ] Decidir qué hacer con el stash viejo (feature lab_clean, base 2026-05-20) → [[Echo - Cierre del Lab y Limpieza del Journal]] **D4** #owner/me #type/dev #area/echo
> - [x] Fix nativas: síntesis de OPEN nativo desde CloseResult en core (implementado con tests, mergeado `e25165ba`, deployado en prod 20-08 22:26) #owner/agent #type/dev #area/echo
> - [ ] Fix canónico EA: redeployar EAs post-`0abdf720` en cada terminal MT4/MT5 (confirmar antes cuál EA emite el open nativo: `execution_agent_v3` vs `reference_v3` — evidencia mixta 21-08) → [[Echo - Cierre del Lab y Limpieza del Journal]] **N1** #owner/me #type/dev #area/echo
> - [ ] Opcional: backfill del hueco NATIVE 1-jun→20-08 → [[Echo - Cierre del Lab y Limpieza del Journal]] **N3** #owner/me #type/research #area/echo
> - [x] Verificar primera NATIVE en `trade_journal` tras el deploy del 20-08 → **VERIFICADO 21-08: 18 filas NATIVE CLOSED** (con alertas de calidad: `risk_pips` NULL + duración ~3h sintética; sin nuevas al cierre del día) #owner/agent #type/research #area/echo
> - [ ] Investigar `opened_at_ms` sintético del path NATIVE → [[Echo - Cierre del Lab y Limpieza del Journal]] **N2** #owner/me #type/research #area/echo
> - [ ] Decidir semántica Daily Ops: ventana HWM vespertina + filtro ACTIVE (oculta ~82% de la actividad de hoy; universo real 48 cuentas) → [[Echo - Cierre del Lab y Limpieza del Journal]] **D3** #owner/me #type/research #area/echo
> - [x] **Identificar el gate oficial**: es `lab_clean_readiness_check.sql` (no stage0_audit). Corrido contra prod el 21-08 → **NO_GO: 1 blocker (columna prohibida `origin`) + 1 warn (policy coverage 0%)** #owner/agent #type/research #area/echo
> - [ ] **Cerrar el gate** → consolidada en [[Echo - Cierre del Lab y Limpieza del Journal]] **Fase 1 (G1-G4)** #owner/me #type/dev #area/echo
> - [ ] **Reconstruction report** (checklist §49-59) → base cubierta por [[Echo - Reporte de Estado Lab y Journal 2026-08-21]]; faltante (flows runtime, writer/reader lab_*) en [[Echo - Cierre del Lab y Limpieza del Journal]] **E1** #owner/me #type/research #area/echo
> - [ ] **Limpieza Etapa 10 (restos)** → consolidada en [[Echo - Cierre del Lab y Limpieza del Journal]] **Fase 2 (E2-E5)** #owner/me #type/dev #area/echo
> - [ ] Agregar test real de repositorio del UPSERT → [[Echo - Cierre del Lab y Limpieza del Journal]] **C1** #owner/me #type/dev #area/echo
> - [ ] Seguridad: rotar password único reutilizado y sacar secret del `.env` del front → [[Echo - Cierre del Lab y Limpieza del Journal]] **S1** #owner/me #type/dev #area/echo
> - [x] Investigar incidente 20-08 `mm_engine: SNAPSHOT IS NIL` → **no reapareció el 21-08 (0 ERROR en core desde 12:00)**; mantener en observación #owner/agent #type/research #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

%% Rollup de iniciativa — descomentar solo en proyectos padre para ver las tareas #owner/me (incluye puentes) de todos los subproyectos, agrupadas por nota. Cambiar la ruta por la carpeta de esta iniciativa. Nunca muestra tareas de agente.
```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
const pages=dv.pages('"10-projects/CARPETA-DE-LA-INICIATIVA"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-08-20** — Sesión de levantamiento (cold): bootstrap AGENTS-OS, resolución de entidad vía Graphify, lectura de fuentes vault ([[Echo]], [[echo-core]], changelog, memorias internas 07-16/07-18/08-14), investigación del repo delegada a subagentes (estado git + reportería/arquitectura v3). Proyecto creado con `materialize_schema_note.py`.
- **2026-08-20** — Hallazgo git: master limpio pero stale (último commit 2026-07-18); el fix Daily Ops nativas del 2026-08-14 vive SOLO en rama local `hotfix/native-dailyops-broker` (commit `c8aa59a4`, 2026-08-19) con worktree en `/private/tmp` — sin push ni merge. Stash viejo (2026-05-20) contiene feature real `lab_clean` (front + gateway + migración 047). Credenciales hardcodeadas en `deploy-prod.sh`.
- **2026-08-20** — Hallazgo reportería: la reportería de v3 son **Daily Ops** (tab 3 de Watchtower, maduro, matview `mv_daily_operations` — el objetivo del último hotfix) y **The Lab** (analytics WIP activo, `v3/lab-worker` + `echo.lab_*`). Roadmap general "Olympus" (`v3/ROADMAP.md`). Detalle y evidencia en Estado actual.
- **2026-08-20** — Auditoría prod (subagente, read-only): core de prod = build hotfix (md5 idéntico al worktree, deploy 19-08 22:28); broker fix FUNCIONA en logs. Causas reales de "no veo nativas": (1) opens nativos con `lot_size=0` rechazados por el core (10 saltados; validación `trade_journal.go:280`); (2) `mv_daily_operations` = 0 filas para TODO (filtro ACTIVE + 2186 cuentas INACTIVE vs 17 ACTIVE). Hasura real `.48`; `.75` obsoleto. Incidente aparte: `mm_engine SNAPSHOT IS NIL`.
- **2026-08-20** — Consolidación ejecutada por decisión del owner ("si corre en prod → merge+push; sino elimina"): verificado que corre en prod → `git merge --ff-only hotfix/native-dailyops-broker` + `git push origin master` (master @ `c8aa59a4`), rama local y worktree `/private/tmp` eliminados. Prod no fue tocado (sin redeploy).
- **2026-08-20** — Nombre del panel analytics confirmado: **The Lab** / branding "Experimental Research & Strategy Backtesting Sandbox" / tab "Strategy Lab" (`strategyLabClean`, RFC-009).
- **2026-08-20 (noche) — Fix nativas implementado y deployado por orden del owner:** investigación final determinó causa raíz en el ORIGEN (EAs de terminales pre-05-07 sin `lot_size` en opens nativos; journal NATIVE roto desde el 1-jun con 28 skips desde el 19-08; bridge/core exculpados). Implementada opción core-only: síntesis del OPEN desde CloseResult (`e25165ba`, +499/−7, tests domain+core PASS; fallos sdk preexistentes verificados en master). Merge ff + push. Deploy `build_v3.sh core` + `deploy-prod.sh core` a `192.168.31.71` (20-08 22:26; backup previo `echo-core.bak-20260820-pre-synthesis`, md5 verificado). Servicio activo, arranque limpio, pipeline ECHO fluyendo. Rama `fix/native-open-synthesis` eliminada tras merge.
- **2026-08-21** — Documentación mayor con el resumen histórico del owner (charla de mayo sobre Etapa 0.5 + review): norte del proyecto (Olympus/The Lab/Analytics V3, reglas fundacionales, L0-L7, RFC-009) registrado en esta nota; cronología reconciliada (roadmap→audit→0.5→Lab Clean saltando gate→prod). **Audit real contra prod (subagente, read-only):** veredicto formal BLOCKED pero por script desalineado del schema — prod pivotó a `043_trade_journal_canonical_minimal` (sin flags/MM del spec vNext; 042 tal cual nunca aplicado; 043_currency archivada; journal reconstruido ~2-jun). Métricas reales del gate: r_pct 97.59% global / 98.03% REFERENCE, profit_net 100% — en umbrales READY con el criterio equivalente. 31 tablas `lab_*` confirman Etapa 1. **Fix nativas VERIFICADO: 18 filas NATIVE CLOSED del 21-08 (primeras de la historia)**, con alertas (`risk_pips` NULL + duraciones ≈3h sintéticas → tarea de investigación abierta).
- **2026-08-21 (tarde/noche) — Handoff del refactor de trade_journal validado e integrado**: los tres documentos históricos del owner (charla 0.5 + review + handoff canonical) explican el linaje completo: **A) Lab legacy → B) RFC-003 (029/030, raw_*/canonical_trades, implementado y hoy dormante) → C-vNext (042, rechazado por "todo mezclado" en el journal) → C-final (043 canonical minimal + 045 event/recorded)**. Reglas fundacionales reescritas al contrato FINAL (rev.8 + RFC-010). Validación read-only contra repo+prod (subagente, 12 ítems): gate oficial = `lab_clean_readiness_check.sql` (stage0_audit es DEAD) y su veredicto real es **NO_GO por la columna prohibida `origin`** (la misma que usan los fixes de nativas de agosto → doble tensión documentada) + warn policy coverage 0%; el script del gate está roto tal cual commiteado (CTEs tipados); 045 confirmado (Lab usa `*_recorded`, journal duration usa event); RFC-010 confirmado (4 errores, sin fallbackInsertClose); etapas 1-9 de Lab Clean operando (worker 21.6k runs, outcomes REFERENCE-only, canonical conforme rev.8); Etapa 10 parcial (052 dropeó gran parte del legacy, quedan restos DEAD y LEGACY_ACTIVE clasificados).
- **2026-08-21 (noche) — Doble validación read-only (repo + prod), correcciones mayores y proyecto de ejecución creado**: por pedido del owner se validó todo el estado de nuevo (dos subagentes read-only + verificación directa de los hechos load-bearing). Confirmado: gate `summary|1|1|NO_GO` (blocker `origin`, warn policies 0%) y script del gate roto con **4** CTEs tipados (13/57/194/389 — ejecutado el original: `syntax error at or near "text"`). **Correcciones al estado previo:** (a) `origin` fue **reintroducido a propósito por la migración 056** (22-may) porque `mv_daily_operations` la lee — la salida exige reescribir la matview con `source_type`; (b) universo de cuentas = **48** (17/20/11), el "2186 INACTIVE" era falso; (c) el vacío de Daily Ops quedó **explicado**: ventana HWM diaria (reset 22:00–23:00 UTC post-último-close) + filtro ACTIVE que oculta 102/124 trades de hoy; (d) HEAD = `e25165ba`; (e) existen **51 filas FAILED** (migración 060: estado `FAILED`+`error_*` no ratificado en el contrato) y migraciones 058-060 no registradas acá; (f) 052 dropeó solo 4 `lab_out_*`. Nuevo: [[Echo - Cierre del Lab y Limpieza del Journal]] (roadmap de ejecución con fases D/G/E/N/C/S) y [[Echo - Reporte de Estado Lab y Journal 2026-08-21]] (reporte autocontenido para evaluar con otra IA). Las tareas de ejecución de esta nota ahora apuntan al proyecto nuevo.

## 🧭 Decisiones

- **2026-08-20** — Este proyecto es de **comprensión** (discovery/recap), separado de cualquier proyecto de cambio sobre echo, según la regla dura de no mezclar iniciativas. Las decisiones de cambio (merge hotfix, recuperar stash, deploy) quedan como tareas `#owner/me` pendientes, no se ejecutan desde acá.
- **2026-08-20** — Nombre canónico del proyecto: "Echo - Discovery y Estado"; aliases: `echo discovery`, `echo recap`.
- **2026-08-21** — El norte documentado arriba (R contra riesgo inicial, L0-L7, RFC-009) proviene del resumen de trabajo del owner (~mayo-2026, charla con IA sobre Etapa 0.5) + `v3/ROADMAP.md` + `v3/docs/lab/*`. Se registró como vigente salvo evidencia contraria; la historia completa vive en esas fuentes.
- **2026-08-21** — Cronología reconciliada: roadmap (dic-25→abr-26) → Stage 0 audit BLOCKED (6-11 may) → charla Etapa 0.5 + review (~11-18 may) → construcción Lab Clean igual (19-20 may, saltándose el gate) → profit net align (25 may) → lab-worker a prod (~14 jul) → último commit (18 jul) → saga nativas (ago). El vault llegó después de todo eso, por eso no había registro local del plan.

## 🔗 Docs / Links

- [[Echo - Cierre del Lab y Limpieza del Journal]] — proyecto de ejecución (roadmap de limpieza y cierre del Lab)
- [[Echo - Reporte de Estado Lab y Journal 2026-08-21]] — reporte validado completo (autocontenido, para evaluar con otra IA)
- [[Echo]] (área) · [[echo-core]] (aplicación) · [[echo-core-changelog]] · [[echo-go-workspace]] (workspace `~/go/src/github.com/xKoRx`)
- Repo: `xKoRx/echo` → `~/go/src/github.com/xKoRx/echo` (monorepo: v1/v2/v3 + agent + core + pipe + tools)
- **Roadmap del proyecto:** `v3/ROADMAP.md` — "Roadmap Olympus" (Watchtower → Commander → Shield → **Lab** → Oracle), definido dic-2025→abr-2026, previo al uso del vault.
- **Next steps registrados del analytics (The Lab):** `v3/docs/lab/analytics_v3_stage0_next_steps.md` (2026-05-06) — plan de remediación Stage 0.5 con Issues 1-7 y mapa de dependencias, escrito cuando el audit Stage 0 dio veredicto BLOCKED. OJO: quedó desactualizado — tras el veredicto se construyó igualmente el lab_clean (commits 19/20-may, migraciones 044+, lab-worker en prod desde 14-jul).
- [[Echo Forge]] es OTRO proyecto (fábrica cuantitativa); no confundir.

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

- 

### Motivos / principios

- 

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:** 
- **Memoria interna:** 
- **Motivo:** 

## Checkpoint — 2026-09-06 — Boundary and live authority TOP

ECHO-FORGE-TO-ECHO-BOUNDARY-AND-LIVE-AUTHORITY-V1-TOP: PASS / CLOSED para contrato documental [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]; no implementación/auditoría de producto/evaluación de trading. O1–O3, source map y slices en esa autoridad única. NEXT EXACT del seam: ratificación O1–O3 → `ECHO-FORGE-LIVE-IDENTITY-WIRE-V1-NORMAL`. Factory db8a022 mantiene C1 sin nuevo deploy/cert. Feedback [[2026-09-06-echo-live-authority-session-feedback]]; run [[2026-09-06-codex-gpt-6-astra-high-echo-live-authority]]; log [[2026-09-06-echo-forge-live-authority-contract]].

## Checkpoint — 2026-09-07 — Architecture durability review (Fable 5.1)

ECHO-ECHO-FORGE-V1-ARCHITECTURE-DURABILITY-AND-CONTRACT-CONSISTENCY-REVIEW: PASS / CLOSED. Decisión **B — FREEZE AFTER BOUNDED CORRECTIONS** en [[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]]: grafo identidad/versión/magic/ingestión/binding/comando ratificado; siete correcciones acotadas (C-1 `CanonicalStrategyID` pura sin `HOST_KEY`; C-2 economía desde deals; C-3 coverage por collector; C-4 correlación broker para UNKNOWN; C-5 reserva como estado del comando; C-6 `trade_routing` una fila por evento; C-7 O1/O3 = default técnico, O2 sólo catálogo CC owner). Ningún TOP sobrevivió. Source db8a022/e25165ba sin avance sobre checkpoint anterior; C1/C2 no implementados. NEXT EXACT Echo: `ECHO-FORGE-LIVE-IDENTITY-WIRE-V1-NORMAL` (incluye C-1) sin esperar O1/O3; factory mantiene C1. Feedback [[2026-09-07-echo-architecture-durability-review-session-feedback]]; run [[2026-09-07-cursor-claude-fable-5-1-echo-architecture-durability-review]]; log [[2026-09-07-echo-forge-architecture-durability-review]].
