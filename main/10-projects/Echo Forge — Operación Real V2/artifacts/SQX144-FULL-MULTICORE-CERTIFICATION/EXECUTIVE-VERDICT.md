---
type: acceptance
schema_version: 1
status: final
created: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
baseline: "xKoRx/symphony 492a271e (release 0.3.1); SQX 144.2953 (binario SHA 7d312106 idéntico en los 3 hosts); hosts sqx-zeus (27 cores SQX/28 vCPU), sqx-hera (60/64), sqx-kronos (72/76)"
verdict: "SQX144_FULL_MULTICORE_CERTIFIED (motor, con exclusión de alcance original) → CIERRE DE GAPS 2026-10-19: ECHO_FORGE_FULL_CPU_CERTIFICATION = NOT_CERTIFIED (CA del builder de producción FAIL; retest N=10 FAIL; lineage Retester→Optimizer FAIL — ver CPU-GAP-CLOSURE-20261019.md)"
tags:
  - kind/acceptance
  - area/echo
  - tech/performance
---

# EXECUTIVE VERDICT — SQX 144 FULL MULTICORE CERTIFICATION (P0 físico E2E)

## Veredicto global

**`SQX144_FULL_MULTICORE_CERTIFIED`** — con exclusión de alcance explícita: esta certificación cubre el **motor SQX 144** (builder genético, retester N-batch, optimizer WFO) y la **cadena integrada Builder→Retester→Optimizer** en las tres VMs de la flota, con UNA instancia SQX por VM. **NO certifica** la fase CustomAnalysis del builder de producción (overview producer): ningún CFX real con CA habilitada estaba disponible para medirla, y evidencia física previa (2026-10-18, FlowRun 79385c32, `SQX144-CPU-UTILIZATION-20261018/CPU-ROOT-CAUSE.md`) demuestra que esa fase es **secuencial (~1,05 core sostenido, 87% del wall del builder)** — limitación de producto conocida con remediación registrada (REMEDIATION-PLAN.md §4), no de configuración de flota.

## Veredictos separados

| Veredicto | Resultado | Evidencia primaria |
|---|---|---|
| `BUILDER_GENETIC_MULTICORE` | **PASS** | Picos 68,1/72 (Kronos), 51,7/60 (Hera), 26,95/27 (Zeus) en la ventana de cálculo del builder con stop funcional; maratón v2 de ~3 h con carga sostenida 72-75/60-62/24-25 (observación viva); antecedente P0: 68,46 cores × 40 min (Kronos) |
| `BUILDER_CUSTOMANALYSIS_MULTICORE` | **NOT_APPLICABLE** | Builder_G1 y builder_test llevan `CustomAnalysis method="none"`; la CA de producción es inyectada por el flujo en workspace efímero ya limpiado. Evidencia previa: secuencial |
| `BUILDER_END_TO_END_MULTICORE` | **PASS** | Ciclo completo medido por fases (boot/calc/save) con marcadores de consola y stop funcional "Build finished because databank is full"; 20 estrategias auténticas por host |
| `RETESTER_BATCH_MULTICORE` | **PASS** | Ladder N=10/30/90/300/600 × 3 hosts, lote físico en UNA ejecución sqcli ("str to test: N"), throughput monotónico, picos 73,3/61,5/25,2 cores |
| `OPTIMIZER_WFO_MULTICORE` | **PASS** | 30/30 ejecuciones (10 × 3 hosts) con cálculo multicore real: medias calc 57-68 (Kronos), 42-56 (Hera), 19-24 cores (Zeus); contrato 1 estrategia/SQX intacto (10 procesos secuenciales por host) |
| `INTEGRATED_BUILDER_RETESTER_OPTIMIZER` | **PASS** | Sello de continuidad = 0 hashes faltantes en los 3 hosts; cohort de 10 del output del builder → retest batch 10→10 → 10 optimizaciones WFO completas |
| `ZEUS_MULTICORE` | **PASS** | 27 cores: retest pico 25,2; optimizer medio 19-24; builder pico 26,95 (100%) |
| `HERA_MULTICORE` | **PASS** | 60 cores: retest pico 61,5; optimizer medio 42-56; builder pico 51,7 |
| `KRONOS_MULTICORE` | **PASS** | 72 cores: retest pico 73,3; optimizer medio 57-68; builder pico 68,1 |

## Matriz final (datos reales de esta campaña)

| Host | Tarea | Estrategias | Cores medios cálculo | Cores pico | Throughput | Estado |
|---|---|---|---|---|---|---|
| Zeus | Builder | 20 producidas (cohort 10) | 23,8 | 26,95 / 27 | 20 estr / 1,7 s calc | PASS |
| Zeus | Retester (n600 máx) | 600 por lote físico | 24,2 | 25,1 | 52,8 str/s | PASS |
| Zeus | Optimizer (grupo 10) | 10 × 1 por SQX | 19,4-23,6 | 24,8-25,3 | 10/10 multicore | PASS |
| Hera | Builder | 20 producidas (cohort 10) | 40,8 | 51,7 / 60 | 20 estr / ~11 s calc | PASS |
| Hera | Retester (n600 máx) | 600 por lote físico | 53,2 | 61,5 | 42,4 str/s | PASS |
| Hera | Optimizer (grupo 10) | 10 × 1 por SQX | 42,6-56,0 | 61,4-62,7 | 10/10 multicore | PASS |
| Kronos | Builder | 20 producidas (cohort 10) | 49,2 | 68,1 / 72 | 20 estr / 9,9 s calc | PASS |
| Kronos | Retester (n600 máx) | 600 por lote físico | 62,9 | 73,3 | 37,1 str/s | PASS |
| Kronos | Optimizer (grupo 10) | 10 × 1 por SQX | 57,1-67,6 | 73,3-74,4* | 10/10 multicore | PASS |

\* Valores pico >nproc (hasta 106) en Kronos son artefacto de muestreo en VM (jitter de intervalos del sampler + contabilidad del hipervisor); se reportan acotados a nproc. Las medias integrales (jiffies primer→último sample) son la medida de confianza y nunca exceden nproc.

## Gates

1. **Multicore real**: PASS — >1 core simultáneo, múltiples threads con ticks (hasta 148), cálculo real (estrategias/optimizaciones completadas), outputs válidos, throughput monotónico con N.
2. **Aprovechamiento de capacidad**: PASS con matiz — retester/optimizer superan 70% sostenido en los 3 hosts; builder genético alcanza 94-100% pico y 68-88% medio en ventanas de segundos, más la maratón v2 (~3 h a ~100% en 3 hosts) como demostración de capacidad sostenida.
3. **Agrupaciones**: PASS — Retester ≥10 por ejecución (hasta 600); Optimizer grupo de 10 con exactamente 1 upstream por ejecución; Builder 20 estrategias → cohort 10.
4. **Flota**: PASS — evidencia física en Zeus, Hera y Kronos (sin extrapolar).
5. **Integración**: PASS — procedencia auténtica y continuidad verificada por SHA256 en cada salto.

## Alcance, limitaciones y honestidad

- El config builder v2 (Builder_G1 darwinex adaptado a UTC02, islas 8 × pop 400) quedó en rechazo 100% tras ~3 h (957.570 generadas / 0 aceptadas en Kronos): stop funcional inalcanzable; se detuvo (procesos propios, SIGKILL documentado) y se sustituyó por `builder_test.cfx` del repo (el builder de los flujos E2E), que completa con stop funcional. Los CSV crudos del maratón fueron sobrescritos por la re-ejecución con el mismo label; la saturación sostenida del maratón queda como observación viva (loadavg muestreado periódicamente) y los números certificados del builder provienen de los runs v5 + P0.
- El objetivo `passedStrategies=1000` de builder_test no es el limitante real: su `MaxStrategies=20` interno llena el databank y dispara el stop con 20 estrategias (≥10 exigidas).
- peaks >nproc en Kronos: artefacto de VM documentado; medias integrales siempre ≤nproc.
- Un workflow productivo ajeno (wave3f NDX, GenericSQXWorkflow `sqx-main-v1-ab32f685`) lleva atascado a nivel workflow-task desde 2026-10-14; no despacha SQX (0 actividades, 0 procesos) y no fue tocado. Preflight de colisión antes de cada lanzamiento: 0 procesos SQX ajenos en toda la campaña (guard: 0 `FC_PREFLIGHT_FAIL`).
- Crudo preservado por host en `/home/echo-dev/forge-cert-20261018/` (`rec/` ~samplers 200 ms/1 s, `analysis/*.json`, `state/` sellos, `logs/campaign.log`). Referencias exactas en WORKLOAD-PROVENANCE.md.

---

## CIERRE DE GAPS (2026-10-19) — veredicto final de certificación

Los 3 gaps obligatorios se cerraron con medición/verificación física (`CPU-GAP-CLOSURE-20261019.md`):

| Veredicto | Resultado |
|---|---|
| `SQX_ENGINE_MULTICORE` | **PASS** (sin cambios; no re-benchmarked) |
| `PRODUCTION_BUILDER_CUSTOMANALYSIS` | **FAIL** — CA reconstruida con el mecanismo canónico 0.3.1 (funciones verbatim de `steps.go` @ 492a271e) sobre 300 estrategias auténticas: 1,059 cores medios, UN thread con el 96% del CPU, 72 cores disponibles |
| `RETESTER_10_STRATEGIES` | **FAIL** — sin trabajo paralelo real en N=10 (0,05–0,6 CPU-s observados vs ≈4,6 requeridos; ruta `SingleOptims:false` para N ≤ totalCores); la ventana de medición fue adecuada |
| `RETESTER_TO_OPTIMIZER_LINEAGE` | **FAIL** — los 10 optimizers consumieron los bytes PRE-retest del cohort en los 3 hosts; el output real del retester (0/10 bytes coincidentes) nunca entró al optimizer (defecto de seed del harness del cert, `fc-stage.sh` S5) |
| `ECHO_FORGE_FULL_CPU_CERTIFICATION` | **NOT_CERTIFIED** — persisten gaps obligatorios sin aprobar |
