---
type: evidence_pack
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
baseline: "xKoRx/symphony 492a271e (0.3.1); funnel actual (input/example/config.json @ 0.3.1)"
tags:
  - kind/evidence-pack
  - area/echo
  - tech/performance
---

# WORKLOAD-AND-BATCHING-ANALYSIS — cómo Forge entrega trabajo a SQX y qué cuesta en CPU

Base: lectura de source @ 0.3.1 (evidencia archivo:línea) + medición física de esta sesión. NO se propone rediseño de Temporal ni división del FlowRun; las vías de corrección viven en REMEDIATION.md con sus gates.

## 1. El funnel actual, stage por stage

| stage del funnel (config 0.3.1) | corridas sqcli | estrategias por corrida | cores medidos por corrida |
|---|---|---:|---|
| 01 robust group (`source`, `batch_size:1`, `max_parallel:3` ignorado fail-closed) | 1 por chunk, SECUENCIAL dentro del host | 1 | ~1-2 |
| retester durable (lotes) | 1 por chunk de `batch_size` | = batch_size | N≈10→3-5; N≥450→72+ |
| final reretester (contrato) | 1 por estrategia, serializada | 1 (fidelidad) | ~1-3 (boot domina) |
| optimizer (contrato exactly-1-upstream) | 1 por estrategia | 1 (WFO interno) | pico 72,6; media 20,6 |
| builder | 1 por proyecto | generación genética | 68,5 sostenidos |

## 2. Defecto de suministro identificado (con la fuente exacta)

- `sqx/workflows/generic_workflow.go:1632-1648` — chunks de `batch_size` (default: todo el cohort en 1 lote cuando no se declara).
- `generic_workflow.go:1674-1747` — children se esperan UNO A UNO por defecto.
- `generic_workflow.go:1790-1834` + `core/runtime/config.go:268-271` — el fan-out paralelo K sólo activa si `max_parallel>1` Y el group NO tiene `source`; **groups con `source` van fail-closed al camino secuencial**. El funnel actual anida el retester bajo un group con `source` y `batch_size:1` ⇒ 1 estrategia por sqcli, secuencial, 1 core-ish por host.
- `sqx/cmd/sqx-worker/main.go:468-478` — 1 actividad por host simultánea (refuerza el tope).

Efecto medido: con N=10-30 por corrida SQX usa 3-9 cores pico; con N≥450 usa 72-74. El mismo motor, la diferencia es el lote.

## 3. Contratos que NO se tocan

- **Optimizer exactly-1-upstream** (`sqx-optimizer.v1`): intacto; además ya paraleliza internamente (pico 72,6 medido con UNA estrategia), así que el contrato no cuesta CPU de motor.
- **Final reretester 1-estrategia**: intacto (stage de fidelidad; su coste dominante es boot JVM ~10-15 s, reconocido en S01 como no amortizable sin modo residente).
- **1 sqcli por VM** (lock + worker options): intacto en toda la batería física.
- **S01/S02 (overview exporter)**: fuera de este mandato; su CustomAnalysis secuencial sigue siendo el 87 % del wall del builder de Forge y ya tiene candidato `perf/overview-s02` no fusionado.

## 4. Cuantificación del gap (estimación con medidas propias + w10)

E2E w10 Kronos: builder 69,2 min (3 % genético multihilo + 87 % CustomAnalysis secuencial + sync). Fases de retest del funnel: 1 estrategia por corrida ⇒ 2-3 cores/host observados en los 3 hosts (sar S01). Con la palanca de lote en el retester (p.ej. batch 90-300 en los groups de retest durables, ya con datos en esta sesión: 20,7-29,4 str/s/host con 5-59 cores), las fases de retest de cohortes grandes pasarían de ~1 core a decenas por host con CERO cambio de arquitectura: es la dimensión que el owner declaró "iterable por campaña" el 2026-09-28.

## 5. Preguntas del mandato cerradas con números

- ¿SQX inicializa el pool sin recibir trabajo? SÍ (caso batch 1; "Preparing thread executors: 72" con 1 estrategia en el databank).
- ¿Tiene restricciones internas de scheduling? Ninguna medida con trabajo suficiente (throughput aún creciendo a N=600).
- ¿Fragmenta Forge lo que SQX procesaría junto? SÍ — lote 1 + source secuencial (defecto de suministro).
- ¿El CLI difiere de GUI? No por medición CLI; GUI formal bloqueada por infra (GUI-VS-CLI.md).
- ¿Regresión 144? No (SQX142-VS-144.md).
- ¿Contención interna serializante? No medida con trabajo suficiente; la secuencialidad está aguas arriba de SQX.
