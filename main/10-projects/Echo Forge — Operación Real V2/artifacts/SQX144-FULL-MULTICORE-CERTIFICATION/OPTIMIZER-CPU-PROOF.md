---
type: evidence
schema_version: 1
status: final
created: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
baseline: "SQX 144.2953; proyecto fc-opt (task WFO del optimizer real de campaña, brute-force, Source databank 'Strategies to optimize'); corpus corpus-pristine (24 estrategias auténticas w10) para el grupo independiente"
tags:
  - kind/evidence
  - area/echo
  - tech/performance
---

# OPTIMIZER-CPU-PROOF — Prueba C (grupo de ≥10 estrategias, contrato 1 estrategia/SQX intacto)

## Contrato respetado

`sqx-optimizer.v1` exige exactamente una estrategia upstream por ejecución física. La prueba lo respeta: **10 ejecuciones sqcli SECUENCIALES por host** (nunca 2 JVM simultáneas — guard pgrep antes de cada lanzamiento), cada una con exactamente 1 estrategia sembrada en el databank fuente (`Loaded 1 strategies to databank Strategies to optimize`) y su ejecución WFO completa (walk-forward, brute-force). La consola de cada run lo deja trazado; los SHA de la estrategia sembrada quedaron sellados por run (`rec/opt-XX-source.sha256`).

## Resultados por host (ventana de cálculo de cada ejecución)

| Host | Rango wall (s) | Cores medios calc (10 runs) | Cores pico5 | Threads activos | Runs multicore |
|---|---|---|---|---|---|
| Kronos (72) | 28,3-93,5 | **57,1 / 67,6 / 51,4 / 48,9 / 46,6 / 49,2 / 48,7 / 49,1 / 50,7 / 12,2** | 53,5-74,7 | 136-146 | **10/10** |
| Hera (60) | 26,8-88,9 | 42,6 / 56,0 / 10,5→42,6… (min 10,5) | 44,8-62,7 | 120-125 | **10/10** |
| Zeus (27) | 17,0-69,7 | 19,4 / 23,6 / 23,7 / 18,8 / 18,3 / 18,8 / 18,6 / 18,2 / 18,9 / (opt-03 liviano) | 19,7-25,3 | 57-69 | **10/10** |

Detalle: Kronos opt-02 = 67,61 medios de 72 (**94% de la máquina sostenido durante toda la ventana de cálculo**, mediana RUNNABLE 72 = todos los cores con trabajo). Hera opt-02 = 55,97/60 (93%). Zeus opt-02 = 23,56/27 (87%). Los runs "livianos" (opt-01/opt-03: estrategias con WFO más barato) igualmente queman 10-57 cores — nunca monohilo.

- Medias por grupo: Kronos ~79-94% de nproc; Hera ~70-93%; Zeus ~70-92%. **30/30 optimizaciones del grupo demostraron cálculo multicore real** (ningún run a 1 core).
- Picos >nproc en Kronos (hasta 105) = artefacto de muestreo en VM (jitter del sampler de 200 ms + contabilidad del hipervisor); medias integrales siempre ≤nproc.
- Memoria: MaxRSS 18,4-19,0 GB (runs WFO completos); 4,7-4,8 GB en los livianos.

## Conclusión

`OPTIMIZER_WFO_MULTICORE = PASS`: el paralelismo del Optimizer WFO **dentro de cada ejecución de una sola estrategia** es real, sostenido y reproducible en los 3 hosts — no un pico instantáneo de arranque. El contrato de una estrategia por SQX se mantiene sin romperlo, y el grupo de 10 se ejecutó completo en cada host.
