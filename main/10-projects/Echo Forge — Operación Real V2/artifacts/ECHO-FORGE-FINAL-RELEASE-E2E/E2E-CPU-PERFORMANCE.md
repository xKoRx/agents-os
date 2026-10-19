# E2E-CPU-PERFORMANCE — w11 (2026-10-19)

## Ventanas canónicas del builder (global_log del proyecto, método de la certificación)

Corrida del builder en Kronos (sqcli 18:46:17→18:53:48Z, proyecto `custom`, logs `global_log_20261019_184617.log`):

| Fase | Ventana (UTC) | Duración | Evidencia |
|---|---|---|---|
| Boot + task de datos | 18:46:17 → ~18:47:45 | ~1,5 min | TASK Build STARTED tras carga; w10 tenía ~2m05s de datos |
| Generación genética | 18:47:45 (Build STARTED→FINISHED) | **1m27s** | 1572 generadas, 1000 aceptadas, 846 en databank; Main test total 1761,5 s en 87 s de muro ⇒ backtests de fitness multi-hilo (~20×) |
| **CustomAnalysis S02** | 18:47:45 → 18:49:55 (TASK Custom analysis) | **2m10s (130 s)** | 846 estrategias exportadas; ver abajo |
| Save/sync + upload | 18:49:55 → 18:53:48 | ~4 min | 846 .sqx a MinIO (18:51:57–18:53:13) + overview/monthly/manifest |

## CustomAnalysis S02: throughput y prueba de ruta paralela

- Tasa observada: 846 estrategias / 130 s = **0,154 s/estrategia**.
- Tasas de referencia certificadas (mismo host, mismo corpus tipo, ventana TASK):
  - 0.3.1 secuencial: 242,62 s / 300 = 0,809 s/estr (el baseline w10).
  - S01-only: 106,8 s / 300 = 0,356 s/estr.
  - S02 w16 (ladder FULL): 18,09 s / 300 = 0,060 s/estr + fase de escritura ordenada.
- La tasa observada es 5,3× el baseline secuencial y 2,3× S01-only — **matemáticamente inalcanzable sin la ruta paralela**; cae dentro de la predicción w16 para 846 estrategias (~45 s paralelos + escritura ordenada + sync ≈ 85–130 s).
- Prueba directa de bytecode: canarios 3/3 con marker `Parallel workers: N` + cmp byte-exacto de las 8 clases + javap (ver `PLUGIN-ROLLOUT-3OF3.md`).
- Limitación declarada: el sampler de CPU (arrancó 18:52Z) NO cubrió la ventana CA (18:47:45–18:49:55); no hay medición group-jiffies de ESA ventana. La compensación es la ventana TASK del global_log (fuente canónica de la certificación) + la aritmética de tasas + el ladder w16 certificado (17,2 cores medios, 312 core-s, MaxRSS 15,5 GB). **El speedup E2E declarado proviene de ventanas equivalentes, no de un benchmark aislado.**

## Comparación contra w10 (fases equivalentes)

| Fase | w10 (0.3.1) | w11 (0.3.2 + S02) | Comentario |
|---|---|---|---|
| sqcli builder completo | ~66 min (intento 3) | **7,5 min** | La diferencia excede a la CA sola; la generación genética también corrió más rápida en esta corrida (Main test multicore 1761 s en 87 s). No se declara speedup de generación: factor ambiental no aislado. |
| CustomAnalysis | secuencial (peso dominante del builder 69 min del cert) | **130 s / 846 estr** | Única fase con atribución directa S02. |
| FlowRun total | 3h03m | **2h06m** | Menor corpus downstream equivalente no garantizado: cohort 846 vs 649 y 35 vs 22 seleccionadas; la comparación de total es informativa, no una métrica de speedup. |

## CPU del group (sampler Kronos, 154 muestras activas, jiffies Δ10 s)

- CPU media 501% (≈5 cores) — coherente con batch_size=1 (un sqcli por actividad, trabajo serial por estrategia; el mandato no exige saturación aquí).
- Pico 5894% (≈59 cores) en la ventana del optimizer WFO (grilla interna multicore del motor).
- MaxRSS 14,7 GB; máx 305 threads. CSV completo en Kronos `/tmp/w11-cpu.csv` (efímero).
- Retester N=10 vs 35: la ruta individual (SingleOptims=false, ≤N cores) es la de diseño; la certificación GAP-2 demostró cómputo real — sin cambio en esta corrida.
