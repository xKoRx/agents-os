---
type: evidence
schema_version: 1
status: final
created: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
baseline: "SQX 144.2953; proyecto fc-retest (project.cfx verbatim del retest task real de campaña, SHA de8b3ac8…); corpus overview1117 (823 .sqx auténticos de campaña, mismo subset ordenado en los 3 hosts)"
tags:
  - kind/evidence
  - area/echo
  - tech/performance
---

# RETESTER-CPU-PROOF — Prueba B (lotes físicos N=10/30/90/300/600 por host)

## Naturaleza del lote

Cada run del ladder es **UNA ejecución sqcli** que carga un databank con N estrategias y las retestea internamente: la consola lo prueba en cada run (`Loaded N strategies to databank input` + `Batch size computed to: 5, … str to test: N, totalCores: C`). No son N children ni N procesos: un solo proceso SQX por VM en todo momento (guard de singleton, 0 colisiones en toda la campaña).

## Escalera por host (ventana de cálculo: desde "All backtest data prepared" hasta "Task finished")

| Host | N | task (s) | cores medios calc | cores pico5 | threads activos | throughput (str/s) |
|---|---|---|---|---|---|---|
| Kronos (72) | 10 | 2,14 | 2,25 | 2,23 | 71 | 4,7 |
| Kronos | 30 | 2,86 | 1,48 | 2,07 | 93 | 10,5 |
| Kronos | 90 | 4,61 | 41,57 | 36,10 | 138 | 19,5 |
| Kronos | 300 | 9,45 | **67,93** | **73,62** | 140 | 31,7 |
| Kronos | 600 | 16,16 | **62,91** | **73,27** | 140 | 37,1 |
| Hera (60) | 10 | 2,08 | 2,20 | 2,39 | 64 | 4,8 |
| Hera | 30 | 2,65 | 21,31 | 19,54 | 83 | 11,3 |
| Hera | 90 | 3,62 | 26,06 | 23,58 | 120 | 24,9 |
| Hera | 300 | 8,81 | 44,45 | **60,21** | 125 | 34,1 |
| Hera | 600 | 14,14 | **53,24** | **61,47** | 129 | 42,4 |
| Zeus (27) | 10 | 0,84 | 0,37 | 0,37 | 40 | 11,9 |
| Zeus | 30 | 1,50 | 1,55 | 1,72 | 55 | 20,0 |
| Zeus | 90 | 2,41 | 7,32 | 7,06 | 56 | 37,3 |
| Zeus | 300 | 6,40 | 23,74 | **24,81** | 60 | 46,9 |
| Zeus | 600 | 11,37 | **24,18** | **25,06** | 58 | 52,8 |

## Lectura

- **Escalado real**: al crecer N el motor distribuye más trabajo entre cores y el throughput mejora monotónicamente en los 3 hosts (Kronos 4,7→37,1; Hera 4,8→42,4; Zeus 11,9→52,8 str/s). Los picos alcanzan ~100% de los cores asignados (73,3/72 Kronos; 61,5/60 Hera; 25,1/27 Zeus) y las medias integrales de la ventana cálida llegan a 87-92%.
- El N bajo es genuinamente poco paralelizable (trabajo insuficiente): n10/n30 queman 1-2 cores. Esto es la causa del defecto de suministro del funnel productivo (batch_size:1), ya diagnosticado en P0 — la capacidad aparece cuando el lote crece.
- Memoria máxima (MaxRSS time -v): 18,5-18,6 GB en n600 (los 3 hosts); 13,6 GB en n300; heap JTO por host: Kronos/Hera -Xms34g/-Xmx55g (paridad con P0), Zeus -Xms16g/-Xmx28g (69 GB RAM).
- `RETESTER_BATCH_MULTICORE = PASS`: lotes ≥10 en una sola ejecución SQX (hasta 600), multicore reproducible en los 3 hosts, outputs 600/600 sincronizados (`Databank 'fc-retest/output' saved … 600/600`).
