---
type: evidence_doc
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/evidence
  - area/echo
  - tech/performance
---

# BENCHMARK-COMPARISON S02 — matriz de runs con multicore medido

Protocolo idéntico al de S01 (corpus pristine restaurado + SHA256 verificado antes de cada run; host Kronos ocioso; copia candidate-local; sqcli como proceso independiente de la flota), más dos instrumentos nuevos: (a) **sampler /proc** que muestrea cada 200 ms los jiffies CPU de todo el process group del sqcli (`rec/<label>-cpu.csv`), y (b) JFR por-run (`rec/<label>.jfr`, settings=profile). Duración de tarea = `TASK FINISHED ... in N s` del project log.

## Matriz (fase caliente = media de muestras >0,3 core; pico = mejor ventana de 5 s)

| Run | Código | TASK (s) | Wall (s) | MaxRSS (GB) | Cores hot | Pico 5 s |
|---|---|---|---|---|---|---|
| base-r1/r2/r3 | baseline 0.3.1 | 28 / 21 / 20 | 69–76 | 7,1–7,3 | 1,98–2,07 | 5,2–6,3 |
| s01-r1/r2/r3 | S01 | 7 / 6 / 9 | 57–65 | 3,0 | 2,02–2,10 | 4,1–5,4 |
| s02w8-r2 | S02 w=8 | 3 | 44,5 | 2,90 | 2,95 | 10,4 |
| s02w4-r1 | S02 w=4 | 3 | 45,9 | 2,93 | 2,58 | 7,5 |
| s02w16-r1 | S02 w=16 | 3 | 49,2 | 3,00 | 3,31 | 16,8 |
| s02w32-r1 | S02 w=32 | 4 | 49,0 | 3,05 | 3,62 | 20,3 |
| s02-r1/r2/r3 | S02 w=auto(8) | 9 / 11 / 4 | 57–59 | 3,0–3,1 | 2,48–2,55 | 12,2–13,2 |
| base-h1/h2 (heavy) | baseline | 4 / 4 | 47–50 | 3,0 | 2,3 | 4,1–4,7 |
| s02-h1/h2 (heavy) | S02 | 2 / 2 | 49–54 | 2,2–2,5 | 2,3–2,4 | 6,2–7,0 |

(`s02w8-r1` quedó contaminado por el reinicio de la matriz tras un fix de scripts; se excluye. Los 3 runs `s02ctl-*` quedaron INVALIDADOS: un sqcli huérfano del intento anterior retenía el lock single-instance de SQX y los boots duraron 2–3 s sin ejecutar tarea — gotcha registrado para futuros benchmarks.)

## Resumen

- **TASK mediana**: baseline 21 s → S01 7 s → S02 **4 s** (S02 n=7: 3,3,3,4,9,11,4). Speedup total ~5,3×; S02 añade ~1,75× sobre S01.
- **Multicore real, tres canales independientes**:
  1. Sampler /proc: fase caliente de S02 a 2,6–3,6 cores medios con picos 5 s de **10–20 cores** (según workers) vs 2,0/4–6 en baseline.
  2. JFR por hilo: baseline y S01 concentran TODAS las muestras en `main`; S02 ejecuta **8 hilos `EchoForgeOverview-W1..W8` con 172–224 muestras cada uno** (~45% del total de muestras fuera de main).
  3. Sonda aislada: fase de filas 7,67 s → 1,59/1,64 s (4,7–4,8×).
- **Escalado**: el pico de cores crece monotónicamente con `workers` (7,5 → 10,4 → 16,8 → 20,3 para 4/8/16/32); el wall deja de mejorar más allá de w≈8 porque el task pasa a estar dominado por fases SQX fijas (carga y re-serialización del databank, boot). Default elegido: `min(8, cores−1)` — margen en host compartido.
- **Memoria**: MaxRSS se mantiene ≈ S01 (−57% vs baseline) incluso con 8 workers: las filas retenidas hasta el join son pequeñas frente al heap de 4 GB.

## Atribución y límite superior honesto

- JFR muestra que el main thread gasta la mayor parte del task en `FileHandler.saveFile` / `OrdersList.serialize` / `writeOrderFormat8` / jdom output: **la re-serialización SQX del databank tras el exporter es secuencial y NO es paralelizable desde el snippet**; su varianza (±5 s, también presente en S01: baseline 17–31 s) explica los outliers 9/11 s de fase-4. El techo end-to-end del candidato dentro de una tarea CustomAnalysis es: fase filas ÷ workers + save secuencial + boot.
- Wall de hoy ~+20% respecto de la sesión S01 para baseline (69–76 vs 44–58 s): comparaciones válidas intra-sesión; los números absolutos de S01 no son comparables 1:1.
- Corpus estándar 24 estr (~48 k trades) y heavy 6 estr (~16 k trades): el speedup de fase de filas se mantuvo entre corpus; la extrapolación a w10 (649 estr) sigue siendo INFERENCIA hasta un run real.

## Reproducción

- Runner: `/home/echo-dev/forge-perf-s02/run-matrix.sh` (Kronos) → `rec/matrix.log`, `rec/<label>-{time.txt,cpu.csv,jfr}`, `out/<label>/`.
- Análisis: `analyze-s02.py` (wall/RSS/cores), `jfr-main.py` (stacks main), `parity2.py` (heredado de S01).
- Evidencia cruda preservada en la copia candidate-local; el repo contiene el código en `perf/overview-s02`.
