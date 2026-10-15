# FINAL-NDX-FIDELITY-CLOSURE — Cierre de fidelidad Echo Forge (frontera pre-Echo)

**STATUS: FORGE_PRE_ECHO_BLOCKED_INFRA** (2026-10-14, sesión one-shot ~7h)
**Frontera**: funnel Forge completo y duradero; TOP-1 real durable; 20/21 backtests MT5 bloqueados por un defecto de infraestructura de flota MT5 caracterizado con causa raíz exacta. Cero integración Echo.

## Resultado ejecutivo

El funnel físico NDX · SQX 144 · MT5 NDX_SQX quedó **operacional punta a punta**: las 21 estrategias Robust V2 de wave2b se re-consumen de forma durable, re-derivando sus decisiones byte-idénticas (§9), aplican, se reretestean con el CFX del Owner sobre ~109M ticks reales en SQX 144 (3/3 hosts), exportan TradeSet + MQ5 y compilan a EX5 21/21. El defecto de canonicalización de símbolo que bloqueaba la fidelidad quedó corregido (release 0.2.138, commits `27311b1`/`9a94f94`), el defecto del plugin Java de `duration_seconds` quedó sanado en flota (fuentes HEAD desplegadas 3/3 + clases efectivas verificadas), y la cadena de fidelidad quedó **demostrada con dos scores COMPUTED reales y deterministas** (86.18 en wave3q; 96.69 en wave3r/s para la misma estrategia — mismo ScoreRef, evidencia durable deduplicada).

El bloqueo restante es exclusivamente de la fase `mt5_backtesting`: en cada wave sólo **un** terminal MT5 sobrevive por host (los terminales concurrentes posteriores al primero salen con código 0 en ~1s), por lo que 20/21 children de backtest fallan fail-closed en el contrato de journals (`journal tester sin delta de la ejecución`). Con 1 elegible, el ranking GLOBAL produce TOP-1 (no TOP-5).

## Respuestas al mandato (§1)

1. **¿21 backtesteadas correctamente en MT5?** No: **1/21 por wave** (f8719ecf en wave3r y wave3s; 02ca621f en wave3n/o/p; 863d5c81 en wave3q). Las demás fallan por el defecto INFRA-1 de abajo.
2. **¿Cuántas comparables con SQX?** 1 con score COMPUTED (`f8719ecf`), con reconciliación estructural MATCH y 101↔101 trades.
3. **Diferencias trades/Net**: f8719ecf: trades 101↔101 (delta 0), net SQX 3766.21 vs MT5 3298.79 (delta −467.42, −12.4%) — diferencia real de feeds/economía (spread/comisión/swap por motor), no defecto.
4. **Fidelity Score**: f8719ecf = **96.69** (`sha256:8e4599f56b710de753974f978c506ad1c06d1e6e25d9cd9c76f9a96da8be2590`, COMPUTED). En wave3q, 863d5c81 = 86.18 (mismo contrato).
5. **Top 5**: no alcanzable esta sesión; **TopProjection efectiva = 1** (TOP-1 real durable).
6. **Finalistas**: promotion `finalist_promotion@1.0.0` ENFORCE COMPLETED → Decision `sha256:61760e33f7716467b93e31d3ef0151792b15717f0b604417d0e3e0cd01482c3c` con finalista f8719ecf (rank 1).
7. **Problemas antes de integrar Forge con Echo**: INFRA-1 (única defecto abierto; ver abajo) + higiene menor (`sqx/tools` roto en master; magic-readback gate sin fixture local).

## Defecto abierto INFRA-1 — terminal MT5 "single-live" por host (bloquea 20/21)

**Síntoma**: los 21 children `MT5BacktestArtifactWorkflow` arrancan; 3-4 actividades corren concurrentes (MaxConcurrentActivityExecutionSize = `mt5/slot_count`); el **primer** terminal lanzado corre el backtest completo; **todo terminal lanzado mientras otro vive muere en ~1s con exit code 0** antes de iniciar el tester. Sin journal nuevo de tester, `log_snapshot.WriteDeltas` falla cerrado: `mt5 artifact backtest: journal contract: mt5 logs: journal tester sin delta de la ejecución` (no-retryable, 20/21 children FAILED).

**Evidencia física (2026-10-14, worker-kronos)**:
- wave3q: slot-3 tester inició 14:00:12 y corrió; slots 2/4 lanzados 14:00:28-30 muertos a 14:00:20-30 con `MCP bind error 127.0.0.1:22346 (10048)`.
- Fix puertos únicos aplicado 4/4 (slot-1 22345/22346, slot-2 22355/22356, slot-3 22365/22366, slot-4 22375/22376; backups `C:\stager\assistant_slotN.ini.bak-20261014`; UTF-16 preservado) → wave3r: **sin bind errors** (`MCP started on 127.0.0.1:22366`) y **los terminales siguen muriendo** → el puerto era un colateral, no la causa.
- wave3r: slot-2 tester corrió 15:18:46→15:22:33 (3:44, "successfully finished"); slots 3/4 lanzados 15:19:11-21 muertos a 15:19:12-21.
- Los 4 slots comparten `terminal.lic` idéntico (SHA256 `049102B9…B8DFF`, clones de `C:\MT5\test`) → hipótesis principal: constraint de instancia única de MT5 ligada a identidad de instalación compartida; NO confirmada por experimento (presupuesto).

**Vía de mitigación intentada y revertida**: `mt5/slot_count=1` (ETCD `/sqx-mt5-worker/production/`) + respawn del worker (stager supervisa, `windows-scm`, backoff 5s) → **el worker queda colgado en startup** (~33MB, sin pollers Temporal; 2 intentos). Rollback a `slot_count=4` + respawn → worker sano (67MB) y los 21 compile children pendientes se consumieron al instante. El cuelgue con count=1 es un **segundo defecto de producto** (no diagnosticado a fondo); la serialización vía config requiere arreglarlo.

**Fix recomendado (fuera de este mandato)**: (a) diagnosticar el multi-instancia MT5 (certificados/licencia por slot o flags de instalación) con probes manuales controlados; o (b) arreglar el hang del worker con `slot_count=1` y serializar; o (c) concurrencia de backtest = 1 a nivel de orquestación (p.ej. semáforo durable). Tras el fix: re-despachar una wave nueva (identidad wave3t+) → ~115 min al TOP 5 (backtests ~4 min × 21 serializados).

## Continuidad wave2b (§9) — PASS

- wave2b FlowRun `0cbd0f34-c4f2-459e-b670-242bddd35b85` → 21 decisiones `OPTIMIZER_SELECTION/SELECTED`.
- wave3p, wave3r y wave3s re-derivaron **21/21 decisiones con `output` JSON byte-idéntico** (md5 comparado por StrategyRef, no sólo 21==21), incluyendo rank 1, runs_count, oos_percent, cell_evaluation_ref y robustness. Los 21 StrategyRefs coinciden 1:1 con `wave2b_selected_21.tsv` del vault.

## Fixes de producto y operaciones (esta sesión)

| Ítem | Evidencia |
|---|---|
| `27311b1` alias `ndxm_darwinex_tick_utc02→ndx` + decoder fidelity por canónico + 9 regresiones | suites evaluation/worker verdes; repro exacto del fallo wave3p sobre el payload real (SHA verificado) con source viejo y PASS con fix |
| Plugin Java: fuentes HEAD (`trades/` con `Duration.between` + config EF-G30 fail-closed) desplegadas 3/3 | hashes agregados idénticos (`ff0968c9…`); clases efectivas con `java/time/Duration` 3/3; Snippets.jar sincronizado por entradas SQ/ (backups `.bak-20261014`) |
| Causa jar stale: cache `internal/tmp/compiled` era `echo-dev` sin escritura para `kor` | chmod `a+rwX` 3/3; recompilado on-demand verificado (Zeus 13:05 local) |
| Release **0.2.138** (`9a94f94`) | rollout 3/3 por SHA `7dc1932e…` + proceso corriendo (el verificador del script falla sólo por SSH-keyless en Daedalus) |
| wave3q TradeSet 3bf04cb9: 106 trades, **bad_duration=0** (wave3p: 55/106 inválidos) | validado decodificando el payload durable (SHA OK, PASS del decoder completo) |
| Puertos MCP únicos 4/4 en slots MT5 (sin roll-back necesario) | Select-String 3/3 verificado + slot-1 intacto |
| ETCD `mt5/slot_count` terminó en **4** (estado original) | readback RO; respawns verificados |

## Data parity (§11)

- Periodo configurado (ambos motores): 2025-07-01 → 2026-10-09 (CFX `a51c1cc3…bafb3`; MT5 `from/to` en spec, GMT, USD, 1:100, deposit 100000, 100% real ticks, Darwinex-Demo, build 6182).
- MT5: ticks verificados hasta 2026-10-08 (smoke). SQX: dataset `NDXm_darwinex_tick_UTC02` 2.577GB idéntico 3/3 (`f70a2f43…`), mtime 2026-10-12.
- **Resolución**: el último trade SQX de las 21 estrategias es ≤ 2026-10-06; f8719ecf además tiene **101↔101 trades idénticos** SQX↔MT5 → la diferencia de cobertura del último día (10-08 vs 10-09) **no afecta ningún trade ni el score**. La diferencia de net (−12.4%) es feed/economía real (spread 1, comisión 5.5, swap Darwinex modelados por motor), resultado de Fidelity y no defecto.
- Advertencia contractual: el periodo se superpone con historia de campañas previas — **no** es validación predictiva OOS limpia.

## Frontera pre-Echo (§2/§16) — verificada

- `echo.ingest_configured=false` en el watcher de la campaña; cero HTTP hacia Echo.
- `handoff_manifests`: 0 filas para wave3q/r/s (las 8 filas existentes son de campañas históricas `forge-f50e5cdb`/`forge-0ce72173`).
- Promotion ejecutada: `finalist_promotion@1.0.0` local durable; **`finalist_promotion@2.0.0` no configurada; `forge_seal_handoff` no ejecutado; cero deployments Echo.**

## Artefactos

- `FINAL-NDX-FIDELITY-CLOSURE.csv` — 21 filas, una por StrategyRef de wave2b, estado terminal real por estrategia.
- Bundle raw: `bundle/` (flow JSONs wave3q/r/s, CFX+SHA, manifest 0.2.138, SHA256SUMS, refs durables, journals MT5, clasificación de fallos).
- Refs durables clave: FlowRun wave3s `cd697133-4d2a-49d3-bd24-45c391b404d8` (workflow `sqx-main-v1-348b7cbd-e535-4165-8d55-935997422c91`); RankingSnapshot `sha256:359de45b6a401cb94ff4e7149dec25311b6eefac51beff6eccbf896083e857d8` (GLOBAL, requested 5, effective 1); Score `sha256:8e4599f5…a8be2590` (COMPUTED 96.69); Promotion Decision `sha256:61760e33…88c69f9c`.

## TopProjection final (TOP-1 de 1 elegible)

1. **f8719ecf-07f7-45de-9601-45c75cdd444b** — Fidelity **96.69** (trades 101↔101, net 3766.21→3298.79) — Decision finalista `sha256:61760e33…`.

No se inventan finalistas: con 1 elegible COMPUTED, el contrato entrega TOP-1.


---

# ENMIENDA 2026-10-15 — MT5_SERIAL_RECOVERY_PASS → FORGE_PRE_ECHO_PASS

**STATUS PREVIO**: FORGE_PRE_ECHO_BLOCKED_INFRA (INFRA-1 bloqueaba 20/21 backtests MT5 por wave).
**STATUS ACTUAL**: **FORGE_PRE_ECHO_PASS** — INFRA-1 remediado por serialización de activities; funnel wave3t 21/21 con MT5 real, scores COMPUTED, ranking GLOBAL TOP-5 real y promoción local @1.0.0. Evidencia completa en `artifacts/mt5-serial-recovery-20261014/`.

## Remediación INFRA-1 (serial)

- Fix de producto (`sqx-mt5-worker/main.go`): `MaxConcurrentActivityExecutionSize` ya no deriva de `SlotAllocator.Capacity()`; es la constante física `mt5ActivityConcurrency=1`. El pool conserva 4 slots con identidad/lease (`mt5/slot_count=4`). Commits symphony `5eaeaa2` (fix+tests) y `11436e7` (gitignore staging para `vcs.modified=false`).
- Release **0.2.141** publicada (windows `bf247d61…`, linux `57537674…`, `vcs.modified=false`, desde `1a48cb3`); rollout Linux 3/3 verificado por SHA; worker Windows activado 0.2.107→0.2.141 vía el stager canónico reparado (tarea `StagerReconcile` + `stager.exe` de xKoRx/stager HEAD; el binario 8/13 rechazaba `shutdown_timeout: infinite` y la tarea no existía — por eso 0.2.107 estaba estancado desde el 24-sep).
- Smoke **MT5_SERIAL_SMOKE_3_OF_3_PASS** con 3 EX5 auténticos del cohort (02ca621f, 3bf04cb9, 89171ea6): 3× success, HTM durable bajo `07_smoke_serial_20261014/`, journals frescos, inputs reconciliados por SHA256, slot-2, un solo terminal a la vez (watcher 2 s, nunca >1).
- Defecto ambiental adicional detectado y remediado durante el smoke: desde ~16:42 local del 14-oct, session 0 del host worker-kronos no materializaba el `.htm` del tester (tester passed, sin reporte) con cualquier launcher; logs con `MDI create failed` y sin precarga del experto. Fix: `tscon 2 /dest:console` (sesión KoR Disc→Active), zombie `MetaEditor64` (C:\MT5\test, desde 12-oct, puerto 22345) terminado, y worker movido a tarea interactiva `EchoForgeMT5WorkerSession` (misma resolución de release vía CURRENT del stager). `StagerRuntime` quedó Disabled mientras dure esta modalidad. La causa raíz exacta de la degradación de session 0 quedó sin determinar (ver UNRESOLVED).

## Wave3t (E2E final, identidad libre)

- Fuente: wave2b FlowRunRef `0cbd0f34-c4f2-459e-b670-242bddd35b85` (contrato de continuación reutilizado; 21/21 decisiones V2 re-derivadas idénticas — demostrado en wave3p/r/s con output byte-idéntico).
- FlowRunRef wave3t: `7f2efabe-3778-4981-8135-5893bdd23875` (workflow `sqx-main-v1-4c491359-ff12-4ab4-8664-0e40b4786e94`), COMPLETED 2026-10-15T03:28:19Z. Duración ≈ 2 h 17 min (21 backtests serializados + compiles).
- Determinismo cross-wave: f8719ecf HTM wave3t **byte-idéntico** a wave3s (etag `6cb04dcf…`, net 3298.79, 101 trades) y fidelity 96.6920 == 96.69 wave3s.
- **21/21 backtests MT5 técnicamente completados** (21 HTM durables publicados; cero fallos de infraestructura; paridad de trades SQX↔MT5 1:1 en las 21).
- **21/21 Score COMPUTED** (`mt5_fidelity_shadow.v1`); **ranking GLOBAL** `mt5-final-fidelity-ranking` (score_descending.v1): requested 5, **effective 5**; RankingSnapshotRef `sha256:8afa7b12afc8f9fb9dc29555a2df4ffe02a4df20a31dcffa5fd126879b0eb979`.
- **Promoción** `finalist_promotion@1.0.0` AVAILABLE: Decision `sha256:20dcf02b1a0ebb09e51c6226c77baaa6fd845c13e57b63e3f588a02079c83963`, 5 finalistas (TOP_PROJECTION_PROMOTED).

## TOP 5 final (GLOBAL)

1. **3e1762b9-629f-4273-ad03-f71439bb02c1** — fidelity **99.6911** (MT5 net 1756.74 / 95 trades)
2. **89171ea6-9ece-4f15-acee-c79da3abc288** — 99.4237 (3998.18 / 146)
3. **93413f58-76cf-4d7f-ba6b-e172d940937a** — 98.4042 (2103.83 / 52)
4. **ddd47d26-be00-49cd-879c-478787d58152** — 98.0092 (1961.41 / 113)
5. **0cb29320-7838-4a1f-b401-ec5bab293166** — 97.5077 (2175.36 / 43)

(f8719ecf, la TOP-1 de la wave anterior con cohort incompleto, queda rank 8 con 96.6920 — el TOP-5 anterior no certificaba los mejores de la cohorte; éste sí.)

## Frontera pre-Echo

- `echo.ingest_configured=false`; 0 llamadas HTTP a Echo; `forge_seal_handoff` no ejecutado; `finalist_promotion@2.0.0` no configurada; 0 deployments de EAs.
- CSV 21/21: `FINAL-NDX-FIDELITY-CLOSURE-21.csv`. Bundle raw + SHA256SUMS en `bundle/`.

## UNRESOLVED

1. **Degradación de session 0 en worker-kronos** (root cause sin determinar): el `.htm` del tester dejó de materializarse desde session 0 a partir del ~16:42 local del 14-oct; reproducible (worker 0.2.107-era sessions OK por la mañana; manual + worker fallan por la tarde; sesión interactiva OK siempre). Workaround operativo vigente (worker en sesión interactiva); el host requerirá un reboot de mantenimiento o investigación de window stations cuando la ventana operativa lo permita.
2. **Hang del worker con `mt5/slot_count=1`** (defecto de producto, sin diagnosticar): no bloquea (la serialización vive en el worker, no en el pool).
3. `78225ff4` fidelity 50.0000: net SQX negativo (−199.03) hace degenerar el componente de net; trades 117↔117. Revisión de negocio opcional, no defecto.
