---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/README|Clutifx compiled]]"
aliases:
  - hefesto baseline audit
  - auditoría backtester hefesto
tags:
  - kind/doc
  - area/echo
  - tech/backtester
created: "2026-10-23"
updated: "2026-10-23"
---

# HEFESTO-BASELINE-AUDIT — Estado físico del backtester Echo Futures

Auditoría read-only del host oficial de backtests (Hefesto, `kor@192.168.31.164`), ejecutada el **2026-10-23** por la misión GOD (Clutifx Strategy Extraction). Sin mutaciones: ninguna ejecución de backtest fue lanzada por esta misión (un intento de `reproduce` falló en EXIT=2 al leer el formato del resultado — `result.json` del modo `platform-batch` vs `result.json.gz` esperado por el CLI — sin arrancar motor alguno, y fue abortado por orden del Owner antes de reintentarse). Evidence channel: SSH MCP (perfil `hefesto`) + clon local `xKoRx/echo` en Daedalus para los docs de ramas ya publicadas en origin.

## 1. Runtime vigente (A1)

| Ítem | Valor verificado | Evidencia |
|---|---|---|
| Host oficial | `hefesto` (192.168.31.164, Ubuntu, 13 GB RAM, `/` 200G con 139G libres, load ~0.4, sin procesos de backtest activos al corte) | `hostname`, `ps aux`, `df`, `free` |
| Repo del motor | `xKoRx/echo`, checkout `~/go/src/github.com/xKoRx/echo` | `git -C ... status` |
| Rama vigente del experimento histórico | `experiment/campaign-lab-s04` @ `c6ae3dbc` (limpia al corte inicial) | `git branch -vv` |
| Ciclo correctivo ACTIVO (paralelo, otra sesión) | commit **`e951d258`** (2026-10-23 13:25 -0300, minutos después del corte inicial): fix del wedge `PROTECTED_CLOSE_ORDER_MISMATCH` (repro determinista FBC-5M-R500 2023-12-21T14:36:03.84Z, 4/4); WIP remanente en `safety_entry_fence_test.go` (+21) y un `.md` sin trackear | `git log -1 --stat`, `git status` |
| Otro checkout | `xKoRx/echo-futures` @ `feature/d5-m1a-p150` (`cdef2b6`, limpio) — simulador discreto D5-M1A-P150, NO es el backtester de corpus | `git status` |
| Ramas relevantes | `experiment/challenge-history-20261018` @ `20c73fd4` (1 commit sin push: auditoría independiente NORMAL del 26/26); `master` @ `d74b6525` | `git branch -vv` |
| Binario sellado del histórico 26/26 (r5) | `~/echo-work/runs/challenge-history-20261018-r5/echo-backtest` sha256 `7d6e5e85ef81289325c7c84740e2ec0a153eba579dafeaa96694786c0b9e69d7` | `sha256sum` |
| Binario sellado campaign-lab R02 | `~/echo-work/runs/R02-HIST-20261022/echo-backtest-d1d5` engine `dc865aa9…` @ source `d111ce62` (vcs.modified=false) | `R02-RECEIPTS.md`, `receipt.json` por job |
| Instalación portable | `~/echo-backtest-873/package/corpus/` (corpus .nt) | `ls` |
| CLI | `echo-backtest` con modos `platform-prepare`, `platform-batch`, `run`, `reproduce`, `prepare-functional-nt`, `validate-catalog`, `daily-report`, `publish` | `--help` del binario r5 |
| Motor Strategy/MM | `v3/backtester/` + `v3/sdk/futures/`: `Strategy` = módulo técnico puro determinista (`Spec/InstrumentID/Requirements/DecodeConfig/DecodeState/EncodeState/Evaluate`→Signals; sin cuentas, sin relojes, sin I/O); implementaciones `strategies/{tg,fbc,orb,mr,s1,s2,fixture}` + `tgmm`; MM `gerardmm/riskgeometry/riskgeommm`; analytics owner (`analytics/{tg,mr}`) feed-once-per-bar; execution `internal/simexecution` (protected close); provider `provider/` (rule sets E2T) | headers de paquete Go |
| Scratch de esta misión | `/tmp/god-audit/` (sólo lectura + 2 scripts python propios) | — |

**Advertencia de estado**: la sesión correctiva R03 estaba TRABAJANDO en el working tree durante la auditoría (el diff pasó de 4 archivos/+125 a 1 archivo/+21 entre dos snapshots y luego apareció el commit `e951d258`). Nada de R03 fue tocado por esta misión. `R03-PROTECTED-CLOSE/` (`repro-fbc-5m-r500`, `lab-diag`) y el worktree `r03-diag` (rama `r03-diag` @ `a029744a`) son de esa sesión.

## 2. Inventario de estrategias y variantes (A2) — el universo de 89 identidades

Fuente primaria: `~/echo-work/runs/R02-HIST-20261022/R02-HISTORICAL-MANIFEST.json` + `rows-consolidated.json` (finalizer R02, commit `c6ae3dbc`), verificados por conteo directo.

**89 identidades = 26 NATIVE + 63 SG** (las cifras hipotéticas del Owner de 26 challenge / 63 SG / 89 universo son EXACTAS):

- **26 NATIVE** (presupuesto propio del challenge): TG-CH300-{F0, F1-TREND, F2-SR, F3-TREND-SR} (4, módulo `tg`); FBC-CH300-{5M,15M,30M,60M} (4, módulo `fbc`); ORB-CH300-{5M,15M,30M} (3) + ORB-NATIVE-C01..C05 (5, módulo `orb`; **C01..C05 son alias/equivalencias de los ORB-CH300** colapsados por el finalizer — no son familias nuevas); MR-01..MR-10 (10, módulo `mr`).
- **63 SG** = 21 configs base × 3 presupuestos de riesgo (R250/R500/R750; perfil `PROFILE-ATR14-WILDER-M1-X1-GROSS{R}-1TO1`): 21 = 4 TG + 4 FBC + 3 ORB + 10 MR. SG comparte SEÑAL con su base NATIVE (el ranking de familias colapsa NATIVE/SG a un voto por familia de entrada).
- Módulos: `tg`=16, `fbc`=16, `orb`=17, `mr`=40 filas.

**Desglose conceptual correcto** (no confundir):

| Nivel | Conteo | Qué es |
|---|---|---|
| Implementaciones de Strategy (código) | 6 módulos (`tg`, `fbc`, `orb`, `mr`, `s1`, `s2`; +`fixture` de tests) | Paquetes Go con spec congelada |
| Familias conceptuales de entrada | 21 con alias colapsados (14 sin colapsar: 10 MR + 4 TG; FBC/ORB cuentan 7 únicos porque ORB-NATIVE-Cxx ≡ ORB-CH300) | Señal distinguible |
| Configs/variantes | 26 NATIVE + 63 SG = 89 | Identidad experimental |
| Campañas | 1 campaña continua `CHALLENGE_ONLY/CONTINUOUS_V1` por config (26/26 del histórico) + campaign-lab R02 (89) | — |

## 3. Ejecuciones históricas y su validación (A3)

### 3.1 Challenge-history 26/26 (rama `experiment/challenge-history-20261018`)

- **26/26 `COMPLETE_RECONCILED`, 0 fallos de oráculo**, consolidando 3 run roots bajo el sello de preparación único `b72ff90b…`: r4 (12 filas, binario `7d6e5e85…`), r5 (10 filas, mismo binario), hefesto (4 filas ORB-NATIVE-C02..C05 + canario MR-08 medido, binario `4fd0f823…`, wall 23.3 s, RSS pico 1.81 GiB). Fuente: `specs/FEAT-CHALLENGE-HISTORY/VERIFICATION.md` §"Historical execution closure 2026-10-20" + `TRADESGERARD-CONTROL.md` (vault, corte 2026-10-20 v2).
- Totales económicos 26/26: 1.198 compras, 95 pases (7,93%), gasto 143.760 USD, net −911.729,82, 1.071 pérdidas por presupuesto, 24 pendientes, 37.333 ciclos.
- Auditoría independiente acotada (commit `20c73fd4`, sin push): veredicto **NORMAL** (cost labels, 8 terminales bloqueados, TG-F0 slot livelock, recompute 95/95 passes).
- Canario r5 (`critical-gates.json`): 4/4 (`TG-CH300-F1-TREND`, `FBC-CH300-15M`, `MR-08`, `ORB-NATIVE-C04`) COMPLETE_RECONCILED re-certificados antes de FULL; cobertura delta Go 95,07%; selección por cobertura, no por PnL.

### 3.2 Campaign-lab R02 (universo 89, `~/echo-work/runs/R02-HIST-20261022`)

- Manifiesto 89/89 con decisión exclusiva: **REUSE_VERIFIED 29 / RUN_REQUIRED 60** (causas: `D1_D5_CAUSAL_NON_INTERFERENCE` 28, `D5_ACTIVITY_INVALIDATED` 33, `R01_ATTEMPT_PARTIAL` 27, `D1_ORACLE_CANONICAL` 1).
- Consolidación final: **66 COMPLETE reconciliadas / 23 PARTIAL** (`ENGINE_BLOCKED_TECHNICAL` por `SIM_SUBMIT_FAILED: PROTECTED_CLOSE_ORDER_MISMATCH` — defecto del MOTOR, no pérdida económica; composición de las 23: **17 SG FBC/ORB + 3 SG-TG (F0-R250, F0-R500, F1-TREND-R250) + 3 SG-MR (MR-08-R750, MR-10-R250, MR-10-R500)**; recibos `PAUSED_SAME_CAUSE-QUARANTINE.json`). **El fix del defecto fue commiteado después (`e951d258`, verificado físicamente en Hefesto por esta misión; no consta en el clone Daedalus por no estar pusheado); las 23 filas quedan pendientes de re-ejecución por el ciclo R03 (ajeno a esta misión).**
- ECONOMIC_GATE: 2.126 compras, 219 pases (10,3%), gasto 450.960 USD, conciliación por cuenta `declared_matches_own_account` por fila.
- FREQUENCY_GATE: 55.974 entradas sobre 44.352 días elegibles (campaña-suma), identidad de ceros/gaps vía `RESEARCH_SESSION_EXCLUDED`.
- ENGINE_GATE: binario sellado `dc865aa9…` @ `d111ce62`; equivalencia del oráculo D1 probada hoja-a-hoja (6/70705 diferencias, todas identidad de intento); suite python del lab 124/124; failure set del paquete = 18 top-level == baseline documentado, cero regresiones.
- RESOURCE_GATE: supervisor con techo global 6 motores, admisión por presupuesto reservado (RSS medido + margen), guard de swap por tendencia, cool-down 60 s, misma-causa×2 ⇒ HALT con recibo.
- Prueba de identidad NQZ6 (gate v3, `4d63c874`): 47/47 COMPLETE reconciliados bajo `dc865aa9/d111ce62`; 28 jobs comparables fill-identical; exactamente las 19 FBC/ORB pasaron de 0 actividad a actividad real (fix D5 del binding de ventana de sesión a calendario propio).
- Adjudicación final de investigación (`R02-DECISION-STRATEGIES.md`, `OWNER_ACCEPTANCE=REVIEW`): 5 `RESEARCH_SHORTLIST_25PCT_OBSERVED` (SG-MR-06-R500/R750, SG-MR-09-R500/R750, SG-FBC-CH300-15M-R250), 37 below-floor, 11 frecuentes-débiles, 5 raras/complementarias, 8 discard, 23 engine-blocked. Sólo 2 familias alcanzan ≥25% observado (MR-06, MR-09) con IC Wilson declarado.

### 3.3 Reproducibilidad

- Evidencia existente suficiente por recibos: identidad fill-identical 28/28 entre binarios (NQZ6), oráculo D1 equivalente hoja-a-hoja, replays de campañas anteriores IDENTICAL documentados (BTG-S06, BTX-PERF), determinism suite del paquete.
- **Spot-check independiente NO ejecutado** (orden del Owner de no ejecutar backtests durante esta misión; el único intento falló en la lectura del formato antes de arrancar motor). Las filas quedan acreditadas por los recibos sellados anteriores; ninguna fila fue marcada `NOT_VERIFIED` por esta causa porque TODAS las 66 completas tienen recibo de conciliación externa y las 23 PARTIAL están correctamente cuarentenadas con causa.

## 4. Datos (D3)

- **Corpus**: `NQ_HISTORY_AVAILABLE_VALID_SESSIONS_V1`, 13 exports físicos NQ (NQZ3→NQZ6 pasando por H4/M4/U4…), 1.096.110 filas 1m, desde 2023-10-01T22:00Z hasta 2026-10-06T03:50Z (~3 años). Digest del manifiesto `934e24cd…`; sello de preparación `b72ff90b…`; esquema `NT_LAST_1M_OHLCV_V1` con timestamps `NT_EXPORT_UTC_END_1M_V1` (UTC, fin de barra).
- **Sesiones**: 785 candidatas → 672 elegibles, 113 excluidas (45 sin calendario histórico verificado). Ejecución usa 926.685 minutos nativos con warmup por contrato. Exclusiones documentadas por sesión con motivo (`MISSING_NATIVE_MINUTES`, `FULL_1M_INTERVAL_OUTSIDE_CONFIGURED_SESSION_REGION`); sin interpolación silenciosa. `ALL_AVAILABLE_VALID_SESSIONS / PARTIAL_DATA_COVERAGE` — nunca "historia completa" sin calificar.
- **Calendario**: `CME_NQ_HISTORICAL_PARTIAL_20231001_20261006_V1`, timezone America/Chicago, semana 17:00→16:00+1 con `trade_date_shift`. Identidad de calendario sha256 `3279fa19…`.
- **Instrumento**: NQ CME, tick 0.25, point value $20, tick value $5, qty min 1.
- **Costos**: fee 2,49 USD/lado/contrato, slippage modelado 1 tick, spread mínimo 2 ticks con offsets bid/ask de 1 tick (`tgmm`).
- **Provider challenge**: E2T GAU50 (3 fases EVALUATION/LIVESIM/LIVE): daily loss 1.100 USD (PREV_DAY_CLOSE, flatten), trailing 2.000 USD EOD, ventanas de nuevo riesgo 10:00–15:55 NY, forced flat 15:55 NY, caps de progresión 2/4/6.
- **Ticks**: NO hay corpus de ticks en Hefesto; la validación de mayor precisión se hace sobre barras 1m (fuente NinjaTrader Last). El plan de la misión GOD (F) define validación con ticks como pendiente físico.

## 5. Capacidad y límites operativos

- 13 GB RAM total; techo práctico demostrado 6 motores concurrentes (supervisor R02); RSS pico de un oráculo de 30 cuentas: 2.9 GiB; una fila SG típica: ~1.8 GiB / 1h50m wall (MR-09-R250) y 1h54m (FBC-15M-R250).
- Binarios no son byte-reproducibles entre máquinas (documentado en VERIFICATION.md); identidad por `binary_sha256` por fila.
- Prohibiciones vigentes respetadas: no se detuvieron procesos ajenos, no se mutó WIP R03, no se ejecutaron campañas, no se modificó nada sellado.

## 6. Gate A

```text
HEFESTO_RUNTIME_IDENTIFIED        = PASS  (host, repos, ramas, binarios, CLI, motor, datos, costos verificados físicamente)
EXISTING_STRATEGY_INVENTORY_RECONCILED = PASS  (89 = 26 NATIVE + 63 SG exactas; alias ORB identificados; 6 módulos de implementación)
EXISTING_RESULTS_AUDITED          = PASS  (26/26 COMPLETE_RECONCILED + R02 66/89 consolidadas con recibos; 23 ENGINE_BLOCKED documentadas y su fix ya commiteado por ciclo ajeno R03, re-ejecución pendiente)
BACKTESTER_READINESS              = PARTIAL  (motor certificado y corpus vigente para NQ 1m; el universo 89 tiene 23 filas pendientes del ciclo R03 ajeno; sin corpus de ticks; nuevas estrategias Clutifx requieren implementación que esta misión no hizo por mandato)
```

`BACKTESTER_READINESS=PARTIAL` no bloquea el catálogo documental Clutifx: sólo impide declarar "listo para ejecutar estrategias Clutifx nuevas", que de todas formas requiere un encargo de implementación posterior aprobado por el Owner.
