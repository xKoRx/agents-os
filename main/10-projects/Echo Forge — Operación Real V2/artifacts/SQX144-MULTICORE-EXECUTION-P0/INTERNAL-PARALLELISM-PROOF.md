---
type: evidence_pack
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
baseline: "SQX 144.2953 headless CLI; Kronos 76 vCPU; 1 proceso sqcli por VM"
tags:
  - kind/evidence-pack
  - area/echo
  - tech/performance
---

# INTERNAL-PARALLELISM-PROOF — concurrencia interna de UNA instancia SQX 144

Objeto: demostrar (o refutar) que una ÚNICA instancia sqcli 144 aprovecha múltiples cores con trabajo interno paralelizable. Protocolo: host Kronos ocioso, install candidate-local `sqx144-p0` (copia de flota + data.db del día + History compartido read-only), settings `coreUsage=100% / highPriority=true`, un solo sqcli por VM (preflight `pgrep -x sqcli|java`), medición independiente cada 200 ms de jiffies del process-group (`/proc`) y cada 1 s de jiffies y estado por thread (`/proc/<jvm>/task/*`). Crudo en `/home/echo-dev/forge-multicore-p0/rec/`.

## 1. Builder genético — saturación sostenida

`build144-r3`: proyecto Build real de campaña (Builder_G1: 8 islas, población 400, StopCondition databank-full 6000, setup UTC02 H1 tick-precision). Durante 40 min hasta el corte SIGTERM:

- **media de 68,46 cores activos** en fase caliente con fracción de muestras hot = 1,00 (nunca cayó bajo 0,5 core);
- **pico de ventana 5 s: 77,6** (≥ todos los cores, ruido del sampler incluido);
- mediana de threads RUNNABLE 72 (máx 82); 150 threads con CPU acumulada real; el proceso sqcli (que ES la JVM: el launcher Go exec-reemplaza, comm=sqcli) llegó a 273 threads;
- total consumido al corte: ~82.600 core-segundos (jiffies/100).

Esto responde POOL CREATED → POOL ACTIVE → CPU UTILIZED con correlación: 72 executors preparados, ~72 concurrentemente RUNNABLE, ~68,5 cores consumidos.

## 2. Retest por databank — escalado de throughput sin meseta

Ladder N=10→600 sobre corpus auténtico (823 estrategias de campaña, subset ordenado, SHA registrado por run). SQX calcula su batch interno ("Batch size computed to: 5 … str to test: N, totalCores: 72") y ejecuta:

| N | task (s) | throughput (str/s) | pico 5 s (cores) |
|---:|---:|---:|---:|
| 10 | 2,21 | 4,5 | 4,8 |
| 30 | 2,85 | 10,5 | 9,3 |
| 90 | 4,34 | 20,7 | 19,8 |
| 150 | 6,51 | 23,0 | 31,7 |
| 300 | 10,20 | 29,4 | 58,7 |
| 450 | 13,00 | 34,6 | **72,6** |
| 600 | 16,35 | **36,7** | **74,1** |

El throughput crece monótonamente hasta N=600 sin meseta y el pico de cores toca los 76 disponibles a N≈450-600. Repetibilidad: N=300 repetido (7,71/56,9 vs 9,94/58,7) y N=30 repetido dos veces (4,3/9,3; 3,5/9,9; 3,2/9,5). La baja utilización con N pequeño NO es un fallo de escalado: con 10 estrategias no hay trabajo para 76 cores; con 600 sí y los usa.

## 3. Optimizer mono-estrategia (contrato exactly-1-upstream) — WFO paralelo

`opt144-r3` (config real Optimize142: walk-forward type=2 period=10 optimization=15, brute-force maxSteps=20, maxOptimizations=15000, 1 estrategia):

- **pico 5 s: 72,6 cores; máx RUNNABLE 67; 82 threads con ticks**; media del run completo 20,6 (diluida por boot ~18 s y fases de E/S sobre un wall de 37 s);
- MaxRSS 18,2 GB (heap efectivo -Xms4g/-Xmx55g OK).

Cierra la pregunta abierta en S02 §3 ("optimizer de 1 estrategia satura los cores — DESCONOCIDO"): SÍ paraleliza internamente el WFO hasta llenar la máquina en fase caliente; su media baja en campañas se debe a la proporción boot/E/O, no al motor.

## 4. Qué NO es la causa (verificado en esta sesión)

- El launcher: el proceso `sqcli` ejecuta la JVM in-process (exec-replace); no hay capa intermedia que limite hilos; sin `taskset`/affinity (`process_nonwindows.go` sólo `Setpgid`).
- La JVM: Zulu 25.0.2 ve 76 cores ("Using: 72 cores" = N×100 % − overhead; con '-1' usa N−1, medido en S01); heap efectivo correcto; ParallelGC; MaxRSS 7-18 GB sin presión.
- Quota/cgroups/steal: sin límites (S01) y host idle verificado por preflight+load en cada run.

## 5. Límite honesto

- El corpus del ladder son estrategias livianas (~2 core-s/estrategia en UTC02 2026); el shape de la curva (escalado monótono + pico en todos los cores) es el hallazgo, no el coste absoluto por estrategia.
- `distinct_cpus` del sampler per-tid quedó inválido (desalineación del campo psr); la distribución por core no se usa como evidencia — los canales válidos son group-jiffies, per-tid ticks, RUNNABLE, task-time y throughput.
- jcmd attach no funcionó (snapshots vacíos); los nombres de pool interno de SQX no quedaron capturados; la evidencia de hilos es por /proc (tid, estado, ticks).
