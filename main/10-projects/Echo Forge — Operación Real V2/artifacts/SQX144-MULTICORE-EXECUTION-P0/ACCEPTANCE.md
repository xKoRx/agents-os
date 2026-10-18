---
type: acceptance
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
baseline: "xKoRx/symphony 492a271e (0.3.1); SQX 144.2953; Kronos"
verdict: "SQX144_MULTICORE_EXECUTION_PASS_WITH_SUPPLY_DEFECT"
tags:
  - kind/acceptance
  - area/echo
  - tech/performance
---

# ACCEPTANCE — gate de viabilidad del proyecto (sección 12 del mandato)

## PASS funcional — criterio por criterio

| # | criterio | estado | evidencia |
|---|---|---|---|
| 1 | Una sola instancia SQX por VM | PASS | preflight `pgrep` en cada run; lock single-instance respetado; cero instancias múltiples |
| 2 | Una JVM SQX efectiva por ejecución | PASS | sqcli exec-reemplaza a la JVM (mismo PID, 258-273 threads); sin procesos java hijos |
| 3 | SQX 144 reconoce la CPU asignada | PASS | "Using: 72 cores, core usage configuration: '100%'" en cada arranque; ajuste 76→72 coherente con coreUsage |
| 4 | Workload paralelo suficiente | PASS | builder genético (islands 8 × pop 400); databanks 10-600; WFO optimizer |
| 5 | Múltiples hilos de cálculo real | PASS | mediana RUNNABLE 72 (builder), máx 67 (optimizer); 82-150 threads con ticks acumulados por /proc |
| 6 | Utilización sostenida alta en fases paralelizables | PASS | builder 68,46 cores × 40 min (fracción hot 1,00); retest picos 72,6-74,1; optimizer pico 72,6 |
| 7 | Throughput escala hasta límite medible | PASS | retest 4,5→36,7 str/s monotónico N=10→600 sin meseta; builder/optimizer saturan la máquina |
| 8 | Paridad de resultados funcionales | PASS (alcance declarado) | repetibilidad 144: n30 ×3 y n300 ×2 con perfiles equivalentes; 142≈144 en workload equivalente (±3,5 % wall); NO se re-valida paridad semántica del funnel (sin cambio de código/config en producción) |
| 9 | No rompe soporte multiversión | PASS | flota 142/144 intacta; candidates aislados; hallazgo de incompatibilidad de DATOS UTC02→142 documentado (no introducido por esta sesión) |
| 10 | Sin cambios a workflows productivos ni identidades durables | PASS | cero mutaciones de repo/ETCD/PG/MinIO/flota; release 0.3.1 intacta @ 492a271e |

## FAIL — ninguno aplicable

No se verificó ninguno de los casos de FAIL del mandato: SQX no queda limitado a 1-few cores bajo workload comprobablemente paralelizable; la mejora NO requiere múltiples instancias por VM (todo el evidence es 1 sqcli); hay throughput adicional demostrado; paridad no rota; FlowRun indiviso; contrato del optimizer intacto; condiciones reproducibles (repeats incluidos).

## BLOCKED — no aplica

`SQX144_MULTICORE_PROJECT_VIABILITY_BLOCKED` NO se emite: la viabilidad multinúcleo de SQX 144 quedó demostrada dentro de una instancia por VM. Lo que el mandato destapa es un DEFECTO DE SUMINISTRO del funnel (batch_size:1 + source secuencial), con corrección de configuración propuesta y gated en REMEDIATION.md.

## Veredicto

**`SQX144_MULTICORE_EXECUTION_PASS_WITH_SUPPLY_DEFECT`**

- PASS en el objetivo NIVEL A (capacidad del motor): demostrado con medición física en las tres superficies (builder/retest/optimizer).
- DEFECTO en el suministro (NIVEL C-config, no arquitectura): identificado, medido y con vía de corrección de config lista para decisión owner/Manager (Vía 1) y opción de código acotada para adjudicación del Manager (Vía 2).
- Pendientes no bloqueantes: GUI-vs-CLI formal (procedimiento owner en GUI-VS-CLI.md), integración S02 (fuera de mandato).

## Alcance y honestidad de la evidencia

- Host de medición: Kronos (76 vCPU) — el de mayor core count; Hera/Zeus comparten el mismo contrato de ejecución (S01 demostró pools 63/27 en los mismos términos); NO se repitió el ladder en Hera/Zeus (mismo motor, menos cores: los picos absolutos serán menores, el comportamiento de escalado es el mismo binario).
- Corpus liviano (~2 core-s/estrategia): el objeto medido es el ESCALADO, no el coste absoluto por estrategia.
- Runs invalidados y limitaciones del sampler: CPU-BENCHMARK.md §invalidados e INTERNAL-PARALLELISM-PROOF.md §5.
- Crudo preservado: `/home/echo-dev/forge-multicore-p0/rec/` (Kronos, 15 MB).
