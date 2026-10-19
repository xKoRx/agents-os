---
type: evidence
schema_version: 1
status: final
created: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
baseline: "SQX 144.2953 (sqcli SHA 7d312106 en los 3 hosts); candidate-local /home/echo-dev/forge-cert-20261018/sqx144-cert; proyecto fc-build"
tags:
  - kind/evidence
  - area/echo
  - tech/performance
---

# BUILDER-CPU-PROOF — Prueba A (Builder real, 3 hosts, 1 instancia SQX por VM)

## Configuración certificada (fc-build v5)

Fuente: `xKoRx/symphony` `input/00_configs/builder_test.cfx` @ `492a271e` (el builder de los flujos E2E de Forge), envuelto como proyecto `fc-build` (task body `<Settings>` extraído tal cual, databanks Output/Input/Existing portfolio declarados, segundo símbolo `XAUUSD_darwinex`→`XAUUSD_dukascopy` por datos disponibles en los hosts). Islands=8, MaxGenerations=10, MaxStrategies=20 (interno), StopCondition `databank-full` con passedStrategies=1000, `CustomAnalysis method="none"`, motor MetaTrader5 (hedged), H1, USATECHIDXUSD_darwinex + XAUUSD_dukascopy. SHA del cfx desplegado (idéntico en 3 hosts): `812dc3cb9c3d0c93…` — WORKLOAD-PROVENANCE.md.

Stop funcional real observado: `Build strategies : Build finished because databank is full` + `Task finished` (20 estrategias aceptadas por el cap interno MaxStrategies=20; el stop dispara por databank lleno, no por timeout).

## Fases medidas por host (samplers /proc @200 ms + poller de consola @2 s + time -v)

| Host | Cores | boot (JVM+datos) | calc genético | save/serialización | wall total | estrategias |
|---|---|---|---|---|---|---|
| Kronos | 72 | 17,9 s @ 2,4 cores | **9,85 s @ 49,15 medios / 68,06 pico (68% / 95%)** | 1,5 s @ 0,07 | 34,0 s | 20 |
| Hera | 60 | 17,7 s @ 5,2 | **~11 s @ 40,76 medios / 51,7 pico (68% / 86%)** | 1,7 s @ 0,02 | 31,4 s | 20 |
| Zeus | 27 | 9,9 s @ 5,4 | **1,65 s @ 23,77 medios / 26,95 pico (88% / 100%)** | 1,7 s @ 0,02 | 17,4 s | 20 |

Marcadores de consola por run: `Using: N cores, core usage configuration: '100%'`, `Preparing thread executors: N` (72/60/27), `All backtest data prepared`, `Build finished because databank is full`, `Task finished`, `Databank 'fc-build/Results' saved … in Ns`. El estado intermedio se verificó vía HTTP API local de SQX (`/call?cmd=-project action=status`).

## Capacidad sostenida del genético (maratón v2 + antecedente)

- **Maratón v2** (Builder_G1 darwinex→UTC02, islas 8 × pop 400, MaxGenerations 100): los tres hosts sostuvieron carga **~72-75 (Kronos), ~60-62 (Hera), ~24-25 (Zeus) durante ~3 h** (loadavg muestreado en vivo: 73,5/62,1/24,7 en t+2 min; 73,0/61,6/23,8 en t+27 min; 73,7/61,5/25,7 en t+53 min; 75,3/62,5/24,7 en t+2 h13; 73,2/61,9/24,5 en t+2 h50 — sqcli único proceso en cada VM, 94,6% us en top). La config rechazó el 100% de ~957.570 estrategias generadas (gates de fitness de la era darwinex sobre datos UTC02): el stop funcional era inalcanzable y se detuvo por decisión documentada del harness. Raw overwritten por la re-ejecución v5 (mismo label): la maratón queda como observación de capacidad sostenida, no como run certificado de completitud.
- **Antecedente P0 certificado** (mismo host Kronos, 2026-10-18): builder genético 68,46 cores medios × 40 min, mediana RUNNABLE 72 (`SQX144-MULTICORE-EXECUTION-P0/CPU-BENCHMARK.csv`).

## CustomAnalysis

`BUILDER_CUSTOMANALYSIS_MULTICORE = NOT_APPLICABLE` para esta certificación: ni Builder_G1 ni builder_test ejecutan CA (`method="none"`); la CA del builder de producción (overview producer) es inyectada por el flujo en un workspace efímero ya limpiado — no había CFX real con CA para medir. Evidencia física previa de esa fase: **secuencial, ~1,05 core sostenido, 87% del wall (60 de 69 min), ~5,5 s/estrategia** (FlowRun 79385c32, `SQX144-CPU-UTILIZATION-20261018/CPU-ROOT-CAUSE.md`); remediación registrada en REMEDIATION-PLAN.md §4 (fuera de alcance: este mandato no implementa features).

## Veredictos

- `BUILDER_GENETIC_MULTICORE = PASS` (picos 95-100% de la máquina en la ventana de cálculo en los 3 hosts; capacidad sostenida demostrada por maratón + P0).
- `BUILDER_END_TO_END_MULTICORE = PASS` (todas las fases del ciclo medidas y justificadas: boot serial corto, genético masivamente paralelo, save serial ~1,5 s; stop funcional; CA no aplica en la config certificada).
