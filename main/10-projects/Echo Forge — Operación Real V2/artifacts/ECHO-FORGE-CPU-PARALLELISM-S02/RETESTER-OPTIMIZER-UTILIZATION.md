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

# RETESTER-OPTIMIZER-UTILIZATION — baja utilización de CPU y batching (sólo análisis)

Investigación read-only sobre `symphony` @ `perf/overview-s02` (evidencia `archivo:línea` del repo). No se modificó código ni se rompió el contrato de una instancia sqcli por host.

## 1. Cómo despacha Forge los retests y el optimizer

- **Retest durable (batch contract)**: un run físico de SQX retestea el databank upstream COMPLETO — "one physical SQX run retests the whole upstream databank and SQX parallelizes it across cores" (`sqx/activities/worker/steps/steps.go:377-379`); descarga N `.str` y corre 1 sqcli por lote (`steps.go:513-537`).
- **Chunking**: `handleGroupTask` parte claves en lotes de `groupTask.BatchSize`; sin `batch_size` el default es TODO el cohort en 1 lote (`sqx/workflows/generic_workflow.go:1632-1648`).
- **Paralelismo entre lotes**: por defecto los children se esperan UNO A UNO (`generic_workflow.go:1674-1747`); el fan-out paralelo con ventana deslizante K sólo activa si `max_parallel>1` Y el group NO tiene `source` (`generic_workflow.go:1790-1834`) — **los groups con `source` van fail-closed al camino secuencial** (`sqx/core/runtime/config.go:268-271`, `generic_workflow.go:1799`).
- **Optimizer**: contrato exactly-1-upstream por corrida (`steps.go:467-468`, `sqx-optimizer.v1`); el WFO ocurre dentro de esa única corrida sqcli.
- **Final reretester**: exactamente 1 estrategia por invocación, activities serializadas por host (`steps.go:403-427`, `generic_workflow.go:2203-2228`).
- **Entre hosts**: task queue única compartida (`sqx-main-queue`); el paralelismo de flota = nº de hosts pollerando.

## 2. Dónde se enforcea "1 sqcli por host"

1. `MaxConcurrentActivityExecutionSize: 1` en el worker Temporal (`sqx/cmd/sqx-worker/main.go:468-478`), protegido por test (`worker_options_test.go:7-16`) — no es knob de ETCD.
2. Lock single-instance SQX GUI/CLI por host (`config.go:273-276`): "sqcli es single-instance POR HOST (la GUI bloquea el CLI por el mismo lock)". **Observado en vivo en esta sesión**: un sqcli huérfano bloqueó 3 boots con "It seems another instance of StrategyQuant X is running".
3. Preflight operativo `pgrep -af sqcli` vacío (skill `forge-wave-dispatch`).
4. `K = min(max_parallel, len(slices))` en código; el clamp a hosts vivos es guía operacional, no computado.

## 3. Causa raíz de la baja utilización observada

- **El funnel actual anida retester+optimizer en un group con `source` y `batch_size: 1`** (corrección owner 2026-10-16; `input/example/config.json:58-81`): 1 estrategia por corrida sqcli, secuencial dentro del host, con `max_parallel` ignorado fail-closed ⇒ 1 core por host durante retest de finalists y optimizer.
- Contraste: con batch 90, SQX reparte entre estrategias y se midió "~4000% CPU, ~40 cores reales en Kronos" (skill `forge-wave-dispatch` §28) — la capacidad multi-core intra-SQX EXISTE y está demostrada para el retest por databank.
- La afirmación "el optimizer de 1 estrategia satura los cores por sí solo" (owner claim en SKILL.md:34) no tiene medición en el repo y es inconsistente con la baja CPU observada: estado DESCONOCIDO, a verificar con per-PID sampling durante un stage optimizer.
- Semántica canónica congelada por owner 2026-09-28 (`specs/FEAT-SQX-WORKFLOWS-GENERIC/SPEC.md:88-107`): `batch_size` = paralelismo interno SQX por host; `max_parallel` = sqcli concurrentes ENTRE hosts.

## 4. Opciones (evidencia / riesgo / aprobación)

| # | Opción | Riesgo | ¿Aprobación arquitectónica? |
|---|---|---|---|
| A | **Subir `batch_size` del retester** (10→90; SQX reparte cores internamente; ~4000% CPU medido con 90) | Memoria JVM (cap 4g); blast radius del reintento por lote | **NO** — dimensión declarada "iterable por campaña" |
| B | **Fan-out multi-host `max_parallel: 3`** en groups durables SIN `source` (mecanismo ya congelado y certificado) | El funnel actual con `source` lo ignora ⇒ exige partir el funnel en 2 FlowRuns (seal de cohort → re-despacho) | **NO** para el mecanismo; el re-shape del funnel es decisión de despacho |
| C | Optimizer en paralelo entre hosts, batch 1 (baseline declarado ya) | Acotado a K≤hosts; utilidad depende de si el WFO mono-estrategia usa >1 core (medir) | **NO** |
| D | N sqcli concurrentes por host particionando el databank | VIOLA el contrato (lock + worker options + "tumba la campaña") | **SÍ — explícitamente prohibido sin aprobación** |
| E | Reducir el costo no-genético interno (S01+S02 del overview producer, esta sesión) | Bajo | **NO** |
| F | K>3 o más hosts SQX | Infra/presupuesto | **SÍ** (decisión de flota) |
| G | Batching del optimizer >1 estrategia | Contraría `sqx-optimizer.v1` exactly-1-upstream; sin evidencia de que SQX paralice WFO multi-estrategia | **SÍ** (cambio de contrato durable) |

## 5. Telemetría para cuantificar el gap (existe, falta extraer)

`symphony.sqx.sqcli.duration_ms` (`sqx_executor.go:73-75`), `duration_per_batch` con attrs `sqx.keys_count` (emisión hoy sólo en worker legacy `internal/tasks/sqx_worker_refactored.go:866-871`), y `sqx.stage_execution` en PG. PRÓXIMO PASO sugerido: extraer duración por stage del funnel actual y la curva batch vs duración antes de decidir A/B.
