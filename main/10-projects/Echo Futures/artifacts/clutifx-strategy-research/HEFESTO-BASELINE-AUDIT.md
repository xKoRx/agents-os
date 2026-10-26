# HEFESTO-BASELINE-AUDIT — Preflight físico (Clutifx GOD, 2026-10-23)

Estado: **GATE P0 = PASS** · Ejecutor: manager ZCode (GLM-5.3) vía SSH `hefesto` (kor@192.168.31.164)

```text
HEFESTO_PREFLIGHT = PASS
SOURCE_BASELINE   = ae1b09bc (experiment/campaign-lab-s04, limpio, HEAD==origin)
R03_ISOLATION     = VERIFIED (R03 cerrado 89/89 COMPLETE_RECONCILED; 0 procesos activos)
DATASET_SEAL      = ba6f09853a0e923e41a40544e3aeca0a9eb28c41cbf645727818b5cb9ea6b6cd
RESOURCE_BUDGET   = VERIFIED
```

## Runtime y repositorio

- Checkout `~/go/src/github.com/xKoRx/echo`, rama `experiment/campaign-lab-s04`, árbol limpio, HEAD `ae1b09bc` == origin. Go go1.27.1 (`~/opt/go/bin/go`, GOROOT export requerido en shell no-login; go.work go 1.25.5).
- **R03 ya cerró** (el mandato lo describía en ejecución): commit final `ae1b09bc`; fix `e951d258` (PROTECTED_CLOSE_ORDER_MISMATCH); binario sellado `e21a28dc…` en `~/echo-work/runs/R03-PROTECTED-CLOSE/echo-backtest-r03`; 89/89 COMPLETE_RECONCILED; 3.037 compras → 328 pases (10,8%).
- Sin procesos echo/backtest/supervisor; sin tmux/screen; worktree único (el principal).

## Corpus (sellado)

- `~/echo-work/data/corpus/*.nt` — 13 contratos NQ (Z3, H4, M4, U4, Z4, H5, M5, U5, Z5, H6, M6, U6, Z6), 1.096.110 barras 1m Last.
- Formato NinjaTrader `YYYYMMDD HHMMSS;O;H;L;C;V`, **UTC, convención fin de barra** (`NT_EXPORT_UTC_END_1M_V1`, loader `v3/backtester/internal/datasets/ntminute`).
- Cobertura física 2023-10-01 22:01 → 2026-10-06 03:50 UTC. Sin ticks ⇒ no simular precisión intrabar (modelos de ejecución disponibles: `OBSERVED_BBO | TRADE_MODEL | OHLC_1M_MODEL_V1 | MIXED_MINUTE`).
- Calendario `BTG_FUNCTIONAL_NQ_WEEKLY_V1` (CME, America/Chicago, dom–jue 17:00→16:00+1); exclusiones por manifiesto `exclusions-manifest.json`.
- Costos congelados del perfil funcional: tick 0.25, point value 20 USD, fee 2.49 USD/contrato, slippage 1 tick, TIF máx 1 min de lado.

## Recursos (política Owner invariante)

- 12 núcleos · 13 GiB RAM · 138 GiB libres en / · /tmp tmpfs 7 GiB (NO scratch grande; usar `~/echo-work/tmp-clf-*`).
- **6 motores SIEMPRE con cola pendiente; único freno = anti-OOM** (avail < 600 MiB o swap +200 MiB/90 s ⇒ enfriar admisiones, jamás matar sanos). Sub-admisión = defecto.
- Evidencia R03: pico 6 motores, avail mín 139 MiB, swap pico 9,9 GiB, 0 OOM; RSS/job 2,9–3,4 GiB; mediana 6.690 s/job.

## Aislamiento Clutifx (creado en esta misión)

- Worktree `~/go/src/github.com/xKoRx/echo-clf`, rama **`experiment/clutifx-s01`**, base `ae1b09bc`, build verificado (`go build ./v3/backtester/...` OK).
- Run root `~/echo-work/clutifx-backtest/{manifests,binaries,configs,pilot,development,validation,holdout,sensitivity,verifier,reports,checkpoint}`.
- Prohibido: master, working tree de campaign-lab-s04, procesos ajenos, LIVE, cuentas prop.

## Contratos del runtime (ver `v3/`)

- `Strategy` pura y determinista (`v3/sdk/futures/strategy/strategy.go`): Evaluate con triggers tipados (BarClose/MarketEvent/SessionTransitions), `SignalDraft` con technical stop y SIN target monetario; warmup sin señales; `CycleAware` para rollover.
- Registro por factory switch (`v3/sdk/futures/config/composition.go` `ResolveStrategy`); módulo nuevo = caso nuevo + `v3/sdk/futures/strategies/clf/`.
- MM separado (`operation/mm.go`; gerardmm) y proveedor dueño de admisión (GAU50: GROSS 6, DLL 1100, DD 2000 trailing; ventana de compra histórica desde **10:00 NY** en `platform_profile.go`).
- CLI `echo-backtest` (run/reproduce/publish/platform-prepare/platform-batch/campaign); campañas vía `research_lab.py` + supervisor py (cap 6, clases RSS, `.retryN`, reusable byte-verificado).
- Coverage: ≥95% `v3/sdk` (código nuevo Clutifx vive ahí).

## Hallazgo material

El catálogo de estrategias referenciado por el mandato no existía físicamente (vault/Hefesto/branches). Reconstrucción como versión de implementación: `CLUTIFX-EXPERIMENT-MATRIX.md` (34 IDs) + `CLUTIFX-STRATEGIES-MASTER.md` + `CLUTIFX-OBJECTIVE-DETECTORS.md` con procedencia RECONSTRUCTED y citas MKE.
