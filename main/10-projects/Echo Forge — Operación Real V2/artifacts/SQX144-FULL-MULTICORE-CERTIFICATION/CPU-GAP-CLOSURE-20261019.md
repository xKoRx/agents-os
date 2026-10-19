---
type: acceptance
schema_version: 1
status: final
created: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
baseline: "xKoRx/symphony 492a271e (release 0.3.1); SQX 144.2953 (sqcli SHA 7d312106, idéntico a la campaña del cert); Snippets.jar flota SHA aac0e8f2…; hosts sqx-kronos (medición GAP 1) y sqx-zeus/sqx-hera/sqx-kronos (verificación GAP 2, crudos GAP 3)"
verdict: "ECHO_FORGE_FULL_CPU_CERTIFICATION = NOT_CERTIFIED (SQX_ENGINE_MULTICORE: PASS; PRODUCTION_BUILDER_CUSTOMANALYSIS: FAIL; RETESTER_10_STRATEGIES: FAIL; RETESTER_TO_OPTIMIZER_LINEAGE: FAIL)"
tags:
  - kind/acceptance
  - area/echo
  - tech/performance
---

# CPU GAP CLOSURE — cierre de los 3 gaps de la certificación SQX144 FULL MULTICORE (2026-10-19)

## Veredictos separados (mandato Top Local Physical Verifier, ONE-SHOT)

| Veredicto | Resultado |
|---|---|
| `SQX_ENGINE_MULTICORE` | **PASS** (sin cambios: builder genético + retester N-batch + optimizer WFO certificados en flota; no re-benchmarked) |
| `PRODUCTION_BUILDER_CUSTOMANALYSIS` | **FAIL** — secuencial: 1,059 cores medios en la ventana CA con UN solo thread trabajando (96% del CPU), sobre host de 72 cores |
| `RETESTER_10_STRATEGIES` | **FAIL** — sin cómputo paralelo real en N=10; NO fue un artefacto de ventana de medición |
| `RETESTER_TO_OPTIMIZER_LINEAGE` | **FAIL** — el Optimizer consumió los bytes PRE-retest del cohort en los 3 hosts, no el output del Retester |
| `ECHO_FORGE_FULL_CPU_CERTIFICATION` | **NOT_CERTIFIED** — quedan gaps obligatorios sin aprobar |

---

## GAP 1 — BUILDER PRODUCTIVO REAL (CustomAnalysis inyectada por Forge): FAIL

### Reconstrucción de la configuración efectiva (mecanismo canónico 0.3.1)

Las funciones `postProcessCFX` / `ensureProjectOverviewProducer` / `overviewCustomAnalysisTaskXML` / `bindOverviewProducerInputDatabank` / `overviewProducerInputDatabank` / `cfxProject` se extrajeron **verbatim** de `git show 492a271e:sqx/activities/worker/steps/steps.go` (extracción programática, sin re-transcripción; bloque preservado en `gap-closure-evidence/verbatim-extracted-from-492a271e.go.txt`). Un harness Go (`gap-closure-evidence/gap1-harness-main.go`; únicas desviaciones: sentinel local de `ErrContractConflict` y stub de `IsWatcherImportCohortHop`, ruta builder bajo prueba) ejecutó `ensureProjectOverviewProducer` con `plugin="EchoForgeOverviewExporter"` (constante `durableBuilderOverviewPlugin` de `project_activity.go`) y `inputDatabank="output"` (`overviewProducerInputDatabank` de durable builder). Producto:

- `config.xml`: `<Project name="custom" version="142.2399">` con la tarea inyectada `<Task name="Custom analysis" type="CustomAnalysis" taskXMLFile="CustomAnalysis-Task1.xml" active="true"/>` y la sección `<Databanks>` verbatim del wrapper del worker (Results/input/output). SHA256 `781715db11507c74…`.
- `CustomAnalysis-Task1.xml`: byte-exacto del template — `<FullDatabank1>EchoForgeOverviewExporter</FullDatabank1>`, databank mapeado `Input databank → output`. SHA256 (dentro del cfx) verificado por despliegue.
- `project.cfx` (zip): SHA256 `7b9564a82e5c18b1741e038ebf4a1cbcb7f803d9a038eed8d8de7d0564827b45` — idéntico local → Kronos (verificado por SHA tras staging HTTP).

Desviación documentada y acotada: la tarea Build se omitió en la copia aislada (mandato: no repetir generación genética extensa); el databank `output` se sembró con **300 estrategias auténticas** (prefijo ordenado del corpus de campaña `overview1117`, las mismas ResultGroups que la CA de producción consume tras un build). Sello de entrada: `rec/g1-ca-input.sha256` (Kronos). Todo lo demás es bits de producción: sqcli 144 `7d312106…` idéntico a la campaña, `Snippets.jar` de flota (SHA `aac0e8f2…`, 5 clases `EchoForgeOverview*`, 1 referencia en `snippets.txt`) montado vía symlink de la instalación candidate-local, `Using: 72 cores`. `PRODUCT_MUTATIONS: NONE`; `builder_test.cfx` y todo CFX original intactos.

### Ejecución y medición (Kronos, 1 SQX/VM, guard singleton)

Run `g1-ca` con el harness del cert (`fc-run.sh`): samplers 200 ms (group jiffies) + per-tid 1 s + `time -v`. La tarea CA no escribe progreso en consola (buffering de SQX) — la ventana se dató por perfil CPU (boot asentado ≈38 s; cola de save/exit desde ≈268 s; save de databank 11,25 s al final).

| Métrica | Valor |
|---|---|
| Ventana CA | 229,5 s (38,2 s → 267,8 s del proceso) |
| CPU total en ventana | 243,1 core-s |
| **Cores medios en ventana** | **1,059** (perfil estable 1,01–1,08 por buckets de 10 s) |
| Threads vivos en ventana | 175–178 (pool de 72 executors idle) |
| Threads con ≥1 CPU-s | **2** (worker + GC) |
| Thread trabajador (tid 481118) | **221,6 de 231,2 CPU-s = 96%** del total; segundo thread (GC) 5,6 CPU-s |
| Throughput | 300 estrategias / 229,5 s = **1,31 str/s** (0,76 s/estr) |
| Efecto del exporter | **300/300 estrategias re-serializadas** (0/300 bytes preservados vs sello de entrada) — la firma documentada de la tarea CA en S01 |
| Wall total / MaxRSS | 4:28,4 / 14,17 GB; exit 0 |

### Aplicación del criterio

El criterio original (gate 1 del cert: >1 core simultáneo, múltiples threads con ticks, cálculo real, outputs válidos) NO se cumple: el cálculo real existió (300/300) pero en **un solo thread** a ~1 core constante con 72 cores disponibles. Resultado consistente con la evidencia previa del 2026-10-18 (~1,05 core / 87% del wall del builder, FlowRun 79385c32), ahora medido **bajo el mecanismo canónico de inyección de producción** que la certificación no pudo observar. La remediación registrada (REMEDIATION-PLAN §4; candidato S01/S02 en ramas `perf/overview-*`) queda fuera de este mandato: no se instaló nada en producción ni se modificó el exporter.

---

## GAP 2 — INTEGRATED LINEAGE: FAIL (el eslabón Retester→Optimizer no demuestra continuidad de bytes)

Verificación con los outputs ya generados por la campaña del cert (crudo `/home/echo-dev/forge-cert-20261018/` por host), hop por hop:

| Hop | Evidencia | Resultado |
|---|---|---|
| Builder → cohort | `state/builder-output.sha256` ⊇ `state/cohort.sha256` | OK — 10/10 hashes del cohort presentes en el output del builder (sello del cert, 0 faltantes ×3 hosts) |
| Cohort → Retester INPUT | `rec/integ-retest-input.sha256` vs `state/cohort.sha256` | OK — byte-idéntico ×3 hosts |
| Retester INPUT → Retester OUTPUT | databanks `fc-retest/{input,output}` post-run | El retest SÍ re-escribió las estrategias: **0/10** archivos coinciden con los bytes pre-retest (verificado físicamente en Kronos y Zeus; input y output banks) |
| **Retester OUTPUT → Optimizer INPUT** | `rec/integ-opt-XX-source.sha256` vs retester output | **FAIL** — los sellos de fuente de los 10 optimizers son **idénticos al cohort pre-retest** en los 3 hosts (diff vacío cohort.sha256 vs Σ opt-source.sha256 en Kronos, Zeus y Hera). El Optimizer consumió los bytes del builder ANTES del retest, no el resultado del Retester |

Causa raíz (harness del cert, `fc-stage.sh` S5): `seed_one "$COHORT" $I fc-opt …` siembra el databank "Strategies to optimize" desde el directorio `cohort/` (copiado ANTES del retest) en vez del databank de salida del retest. La afirmación del cert "las mismas 10 estrategias (por SHA256 de bytes del .sqx) atraviesan Builder→Retester→Optimizer" queda **refutada en el tercer salto**: la identidad lógica (nombres, 10/10 estrategias, sin cruces) sí atraviesa, pero los bytes retesteados no. Semántica de producción (`steps.go` @ 492a271e): el retester publica los .sqx retesteados como durable artifacts por estrategia y la etapa siguiente los consume como upstream — el seam productivo NO fue demostrado por la cadena integrada del cert. Impacto funcional probablemente nulo para el WFO (re-ejecuta sus propios backtests), pero el reclamo de lineage del cert es falso tal como está escrito.

No se repitió la cadena ni se canceló trabajo sano: verificación read-only sobre los outputs existentes.

---

## GAP 3 — RETESTER N=10 EN ZEUS: FAIL (faltó trabajo paralelo real; la ventana NO fue el problema)

Pregunta: ¿ventana demasiado corta para medir, o realmente sin trabajo paralelo? **Respuesta: realmente sin trabajo paralelo.**

Evidencia de los crudos existentes (Zeus, sin re-ejecutar el ladder):

1. **Energía**: en el retest integrado (10 del cohort), SQX reporta `Task finished in 0.93 s` y el contador de jiffies del proceso queda **plano durante la ventana** (Δ≈5 ticks = 0,05 CPU-s; perfil de 10 s: fase calc 0,03 cores, 0,1 core-s, 0 threads activos, median RUNNABLE 0). En el ladder n10: calc 1,72 s con 0,37 cores mean=peak5 y 0,6 CPU-s. Diez retests completos del mismo tipo costaron ~458 ms CPU/estrategia en el n600 del mismo host (275 core-s/600): hacerlos de verdad habría requerido **≈4,6 CPU-s ≫ 0,05–0,6 observados** — no hay cómputo paralelo oculto que el muestreo haya perdido.
2. **Resolución**: sampler de 200 ms sobre ventanas de 0,93–1,72 s = 5–9 muestras por ventana, con hot_fraction, per-tid (estados S, 0 ticks) y marcador propio de SQX — la medición fue suficiente; no es un artefacto de granularidad.
3. **Mecanismo**: la línea de batch revela el selector de ruta — `SingleOptims: false` exactamente cuando N ≤ totalCores (Zeus n10 con 24 cores; Kronos n10/n30 con 72) y `SingleOptims: true` recién con N > totalCores (Zeus n30, Kronos n90). El motor sólo engancha su grilla paralela de retest por encima de ese umbral; con N=10 corre una ruta liviana que casi no quema CPU. Los ~2,25–2,35 cores que muestra Kronos en n10 son overhead del pool/GC (median RUNNABLE 0–1), no retesteo paralelo.
4. **Capacidad intacta**: el escalado del ladder (Zeus 11,9→52,8 str/s hasta 25,1 cores en n600) ya certificado permanece; el veredicto FAIL es del punto de operación N=10 (el que usa la cadena integrada), no del motor.

---

## Crudo y reproducibilidad

- GAP 1 (nuevo): Kronos `/home/echo-dev/forge-cert-20261018/rec/g1-ca-*` (console, cpu/threads/size CSV, snaps jcmd, time.txt, driver log, `g1-ca-input.sha256`), proyecto `sqx144-cert/user/projects/fc-g1ca/` (project.cfx `7b9564a8…`, log SQX `global_log_20261019_111452.log`). Reconstrucción en vault: `gap-closure-evidence/` (harness Go, verbatim block, config.xml `781715db…`, CustomAnalysis-Task1.xml, scripts de análisis de ventana/per-tid).
- GAP 2/3: crudos preexistentes por host `/home/echo-dev/forge-cert-20261018/{rec,analysis,state}` (sellos y bancos citados arriba); sin mutaciones.
- 1 SQX por VM en todo momento (guard singleton; Kronos verificado idle antes y después; `NO_SQX_RUNNING` al cierre). Sin E2E, sin deploy, sin Temporal, sin campañas nuevas, sin CFX originales modificados, sin cancelar trabajo sano.

## Gotchas que costaron (para el próximo verificador)

- La tarea CustomAnalysis de SQX **buferea su salida de consola**: "Starting…" y "Task finished" aparecen pegados al flush final y el poller de consola no puede datar la ventana — datar por landmarks del perfil CPU (asentamiento post-boot y cola de save) y atribuir CPU por per-tid dentro de la ventana.
- Los sellos de lineage deben encadenar **todos** los saltos contra el banco físico de salida de cada etapa: el cert selló cohort↔builder-output y las fuentes del optimizer, pero nunca comparó esas fuentes contra el databank de salida del retester — ahí se coló el FAIL.
- `SingleOptims` en la línea "Batch size computed to:" es el marcador de ruta del retester: `false` para N ≤ totalCores (ruta liviana, sub-core), `true` recién con N > totalCores.
