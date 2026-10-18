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

# BENCHMARK-COMPARISON — matriz completa de runs

Duración de tarea = `TASK FINISHED ... in N s` del project log SQX (la unidad que domina el builder: 60 min de 69 en w10). Wall = `/usr/bin/time -v` (incluye ~21 s de boot fijo JVM + sync). Host Kronos ocioso durante toda la sesión. Corpus restaurado pristine + SHA verificado antes de CADA run.

## Corpus estándar (24 estrategias, ~48.000 trades)

| Run | Código ejecutado | TASK (s) | Wall (s) | MaxRSS (GB) |
|---|---|---|---|---|
| baseline-run2 | baseline | 28 | n/m | n/m |
| baseline-run3 | baseline | 21 | 45,0 | 5,68 |
| baseline-run4 | baseline | 21 | 49,4 | 5,97 |
| baseline-run5 | baseline | 27 | 58,0 | 5,99 |
| candidate-run1..3,5 (swap user/libs jar) | **baseline** (swap inefectivo, ver DEPLOYMENT-MECHANISM.md) | 31, 18, 21, 23 | 44–58 | 5,6–6,2 |
| candidate-run4 (swap user/libs jar) | **baseline** (ídem) | 17 | 48,4 | 6,15 |
| candreal-run1 | candidato | 7 | 43,7 | 2,49 |
| candreal-run2 | candidato | 8 | 46,7 | 2,75 |
| candreal-run3 | candidato | 9 | 48,2 | 2,82 |

- Baseline (código 0.3.1, n=9): mediana 21 s, media 22,9 s, rango 17–31 s.
- Candidato (n=3): mediana 8 s, media 8,0 s, rango 7–9 s.
- **Speedup task ≈ 2,6× (medianas) / 2,9× (medias); distribuciones no solapadas.**
- MaxRSS: −50% (5,7–6,2 → 2,5–2,8 GB).
- Throughput por estrategia: 0,88 s/estr → 0,33 s/estr (medias).

## Corpus heavy (6 estrategias builder 2,6–5,4 MB, ~16.000 trades)

| Run | Código | TASK (s) | Wall (s) | MaxRSS (GB) |
|---|---|---|---|---|
| heavybase-run1 | baseline | 9 | 37,1 | 2,91 |
| heavybase-run2 | baseline | 9 | 39,2 | 3,05 |
| heavycand-run1 | candidato | 3 | 37,2 | 1,91 |
| heavycand-run2 | candidato | 4 | 40,9 | 2,09 |

- **Speedup task ≈ 2,6× (9 → 3,5 s media); MaxRSS −33%.** Mantiene la proporción con corpus 8× más pesado por estrategia → el speedup es estructural del exporter, no del corpus.

## Sonda empty (0 estrategias, código baseline)

- emptybase-run1/2: TASK 12/13 ms, wall ~20,8 s → el costo fijo de maquinaria de la tarea es despreciable; el wall fijo (~21 s) es boot JVM de `sqcli`, idéntico en baseline y candidato (44–58 s wall en todos los runs).

## Atribución del speedup (JFR)

- Baseline: ~60–65% del CPU de tarea en regex (`Pattern.*` + `String.replaceAll`), `norm` inclusive 16%.
- Candidato: **0 muestras de `Pattern.compile` bajo métodos del exporter**; total de samples de la JVM completa 2.986 → 2.483 (−17%) con boot idéntico; samples atribuibles al exporter −40%.

## Limitaciones (no extrapolar como medidas físicas)

1. Las duraciones son de ESTA flota (Kronos, host ocioso) y ESTOS corpus; no se ejecutó el builder de 1000 estrategias ni el corpus w10 completo (mandato).
2. La extrapolación aritmética a w10 (649 estr × 5,5 s ≈ 60 min → ~23 min si el perfil por estrategia fuera igual) es INFERENCIA, no medición: el corpus w10 real era de estrategias builder recientes y puede diferir en mezcla de costos. La decisión de integración debe apoyarse en el speedup relativo medido (2,6×) y, tras integrar, en un run real.
3. El speedup medido corresponde a la fase CustomAnalysis del overview producer; NO afecta al build genético (126 s) ni al sync del databank (145 s en w10).
4. n=3 en la celda candidato del corpus estándar y n=2 en heavy: suficiente ante distribuciones no solapadas, insuficiente para estimar percentiles finos.
