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
