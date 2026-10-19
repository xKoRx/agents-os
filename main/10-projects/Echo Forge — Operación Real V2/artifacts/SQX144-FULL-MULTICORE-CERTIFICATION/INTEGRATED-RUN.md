---
type: evidence
schema_version: 1
status: final
created: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
baseline: "SQX 144.2953; harness candidate-local /home/echo-dev/forge-cert-20261018/ en los 3 hosts; etapa S5 del driver fc-stage.sh"
tags:
  - kind/evidence
  - area/echo
  - tech/performance
---

# INTEGRATED-RUN — Prueba D (Builder → Retester → Optimizer con continuidad probada)

## Cadena ejecutada por host (una sola campaña secuencial, 1 SQX por VM en todo momento)

1. **Builder** (`fc-build`, builder_test.cfx): genera 20 estrategias auténticas con stop funcional `Build finished because databank is full`; output sincronizado a `databanks/Results` (SHA de los 20 sellado en `state/builder-output.sha256`).
2. **Cohort de prueba** (explícito, sin tocar el ranking productivo ni `top_n=5`): 10 estrategias seleccionadas por regla determinista (orden lexicográfico, muestreo uniforme 10/20); SHA sellado en `state/cohort.sha256` + `state/cohort-list.txt`.
3. **Retester** (`fc-retest`): UNA ejecución sqcli con las 10 del cohort como lote físico (`str to test: 10`, 10/10 resultados sincronizados); SHA de la entrada sellado (`rec/integ-retest-input.sha256`).
4. **Optimizer** (`fc-opt`): 10 ejecuciones WFO secuenciales (1 estrategia del cohort por SQX, contrato intacto), cada una sellada (`rec/integ-opt-XX-source.sha256`) y completada (`Task finished`, resultados WFO en databank Results).

## Sello de continuidad (por host)

El driver recalculó el SHA256 de cada estrategia del cohort y lo buscó dentro del manifiesto del output del builder:

| Host | Cohort | Hashes del cohort presentes en el output del builder | Resultado |
|---|---|---|---|
| Kronos | 10 | 0 faltantes | `continuity seal: cohort hashes missing from builder output = 0` |
| Hera | 10 | 0 faltantes | ídem |
| Zeus | 10 | 0 faltantes | ídem |

## Validaciones de la cadena

- **Identidad**: las mismas 10 estrategias (por SHA256 de bytes del .sqx) atraviesan Builder→Retester→Optimizer. Cero estrategias inventadas (toda entrada proviene de un manifiesto sellado), cero duplicados inesperados, cero cruces entre estrategias (cada optimizer corre en su propio proyecto con databank limpio y 1 semilla).
- **Cero resultados de databanks antiguos**: los bancos Results/output/custom se limpian antes de cada run (`fc-prep.sh`, `seed_one`, S4/S5) y los conteos de sincronización de la consola cuadran por run (ej. `output: 0 → 10`).
- **Cero pérdida silenciosa**: `task_finished_ok` exige marcador de fin + conteo esperado; los 3 hosts terminaron `CAMPAIGN_COMPLETE` con todos los gates DONE.
- **Multicore en la cadena**: el retest del cohort corre en lote físico y las 30 optimizaciones integradas (10 × 3 hosts) demostraron cálculo multicore (medias calc 41,5-64,9 Kronos / 40,7-51,5 Hera / 16,1-21,4 Zeus; detalle en HOST-CPU-MATRIX.csv).

## Veredicto

`INTEGRATED_BUILDER_RETESTER_OPTIMIZER = PASS` — la continuidad Builder→Retester→Optimizer está demostrada físicamente en los 3 hosts con procedencia auténtica, hashes idénticos en cada salto y finalización correcta.
