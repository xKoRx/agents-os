# CLF-Q03-R1 — RESOURCE RECEIPT (Hefesto)

Fecha: 2026-10-26 · Host: Hefesto (local, ~13 GiB RAM física, ~11–12 GiB swap) · Medido en esta sesión, no asumido.

## Cómputo R1

| fase | unidades | wall | nota |
|---|---|---|---|
| G2 NQZ6 (27 corridas) | 27 intentos exitosos + 26×2 intentos de construcción fallidos (rc=2, ~5 s c/u, preservados) | máx 106 s por corrida; suma de duraciones de la ola 2.146 s + 2 corridas de sanidad (~65 s y ~75 s) | ola con techo global 5 motores, admisión por MemAvailable ≥1.400 MB |
| Suites Go clf | 1 corrida | 105 s (+ detectors cached) | verde |
| Suites python campaign-lab | 7 suites | <3 s total | 173 tests verdes |
| Censo/ledger/recibos/deliverables | scripts read-only | <2 min | sin motores |

## Recursos físicos observados

- **Motores concurrentes máximos: 5** (techo global 6 no alcanzado; no fue necesario).
- **MemAvailable mínima durante la ola: ~4,0 GiB** (primera lectura de admisión); rango típico 4,0–6,7 GiB. Post-ola: ~7 GiB disponibles.
- **Swap usado: 0 B** durante toda la ejecución (swap es amortiguador, no capacidad nominal).
- **PSI:** no se muestreó por intervalo en R1; el criterio de admisión usado fue MemAvailable con margen (patrón Q03). Declarado explícitamente, no maquillado.
- **OOM: 0** (ningún fallo de motor por memoria; 27/27 COMPLETE).
- **Procesos huérfanos: 0** al cierre (verificado por pgrep sobre el binario R1; los matches residuales eran el propio shell de verificación).
- **RSS por motor:** clase observada ~1,9–2,0 GiB (coherente con Q03); no se muestreó RSS p95 por PID en R1 (la ola admite por MemAvailable global).

## Históricos evitados (economía del gate)

- 34 IDs del catálogo: **0 ejecuciones G5**. El guard lo habría bloqueado de todos modos (0 CHALLENGE_PASSED en 18 identidades con campaña); el costo evitado del histórico completo (89+ identidades históricas en R03 tomó horas de parrilla) no se incurrió ni en intento.
- 8 identidades sin operación completa en el último contrato **no consumieron** trimestre: C01, C04, C06, S01, S02, S15, S17, T04.
- Las 19 con G2C PASS no re-ejecutaron su campaña NQU6 (bit-idéntica, ya verificada): 0 motores gastados en repetición.

## Intentos preservados (nunca sobrescritos)

- `q03r1/g2-nqz6/out-R1-*-intento1-fanout` (26) — sin re-asociación de fan-out.
- `q03r1/g2-nqz6/out-R1-*-intento2-accountids` (26) — sin re-asociación de account_strategy_ids.
- Ningún intento exitoso fue pisado; `run` reusa COMPLETE+reconciled con bytes de plan idénticos (`result_state=REUSABLE`).
