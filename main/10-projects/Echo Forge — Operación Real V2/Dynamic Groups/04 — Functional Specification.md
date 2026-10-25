---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-25"
updated: "2026-10-25"
---

# 04 — Functional Specification

## Propósito

Comportamientos observables de Dynamic Groups V1, sin imponer un pipeline concreto.

## Contenido

### Requisitos funcionales

| ID | Comportamiento exigido |
|---|---|
| R01 | Workflow y group aceptan una o más tareas soportadas, ordenadas por configuración; groups anidados usan el mismo contrato donde la capacidad exista. |
| R02 | `target.top_n=X>0` por logical_type y `batch_size=Y>0` se configuran independientemente. |
| R03 | Fuente única y partición exacta desde ClassificationSnapshot; todas las candidatas tienen un único logical_type congelado. |
| R04 | Cada iteración consume hasta Y candidatas nuevas, sin repeticiones, en orden congelado. |
| R05 | Cada candidata recorre el subflujo desde su primera task; sólo un descarte explícito permite omitir las siguientes para esa candidata. |
| R06 | Acumular todos los survivors con evidencia válida, mantenerlos sin reejecutar y rerankear el acumulado completo al terminar la iteración. |
| R07 | Al alcanzar >=X, publicar exactamente las X mejores del acumulado y detener esa partición. No prometer óptimo global del universo no evaluado. |
| R08 | Si cursor llega al final verificado y quedan <X, publicar UNDERFILLED con requested/effective/exhaustion_ref; ninguna sustitución de otro tipo. |
| R09 | UNDERFILLED, incluyendo 0/X, conserva salida normal y composición con una task/group siguiente; vacío explícito no activa listado global. |
| R10 | Algoritmo/version/params, task fuente, evidence selector y elegibilidad son declarados; sin métricas financieras predeterminadas. |
| R11 | Toda métrica conserva StrategyRef, producer task instance, EvaluationRef, MetricSetRef, scope temporal, calculador y versión. |
| R12 | Comparabilidad de distintas ventanas es política explícita; Fidelity, métricas económicas y warnings son dimensiones separadas. |
| R13 | Particiones independientes con límite global K; una terminada no espera nuevos candidatos ni consume más presupuesto. |
| R14 | Retry/restart/ACK perdido reusan identidad, batch, cursor, refs y configuración; no duplican members/resultados/selección. |
| R15 | Bindings opt-in por instancia, productor inequívoco y selector tipado; validar dependencia, orden, tipo, rango y capability. |
| R16 | Resolver el último período no future de la celda WFM elegida con IS exacto y parámetros verificables; ausencia/ambigüedad falla. |
| R17 | Apply y consumidores dinámicos comparten período y digest de parámetros; IS full-tick etiquetado OPTIMIZED_IS_BASELINE, OOS original preservado. |
| R18 | SQX crea copia CFX y modifica sólo fechas del Setup exacto; fuente congelada intacta, config efectiva durable y hash. |
| R19 | Distinguir lote lógico Y y ejecución física por estrategia, sin dos SQX concurrentes en host compartido. |
| R20 | MT5 puede resolver por sí mismo la misma autoridad WFM; mismo artifact lineage/intervalo/calendario y datos; INI/readback/report verificables. |
| R21 | Contrato, infraestructura y descarte analítico se distinguen; no ocultar fallos con UNDERFILLED. |
| R22 | Sin opt-in, semántica histórica y contratos V1 conservados; tareas dinámicas y estáticas del mismo tipo coexisten. |
| R23 | Campaign mantiene target global/Builder supply/waves; group maneja su supply finita. |
| R24 | Observabilidad expone por partición cursor, universo, procesadas, descartadas, elegibles, X, iteración, estado, snapshots y errores exactos. |
| R25 | Recuperación con release nueva exige compatibilidad y replay; no dual-write ni segundo engine. |

### Acumulación y reinicio

Identidad del acumulador = FlowRunRef + task estructural del group + scope padre + generación deliberada + logical_type. Restart técnico conserva todo. Nueva invocación intencional (nuevo FlowRun/intent) comienza vacía; una nueva wave de Campaign no hereda acumulador silenciosamente. Nested group recibe sólo la salida exacta de su padre; sus snapshots tienen scope propio. No reabrir una partición terminal para agregar supply tardía.

Ejemplo ilustrativo, no defaults de producto: X=5, Y=20. La iteración 1 produce 4 elegibles; la 2 produce 5 nuevas: se rankean las 9 y se devuelven 5. Una partición con 12 candidatas y una elegible devuelve effective=1/requested=5, UNDERFILLED tras consumir 12. Si otra partición alcanzó X, permanece completa. Si un retry devuelve las mismas 5 refs, su digest coincide y no se incorporan por segunda vez.

### Selección y fallos

El ranking consume las métricas de la tarea declarada de las estrategias que sobrevivieron **todo** el subflujo. Un SQX exitoso y MT5 fallido no constituye un survivor del group configurado con ambos: reintento operacional o fallo, aunque el ranking use SQX. Una evaluación económica válida pero negativa se excluye sólo por política declarada. Si una task filtra N→M, debe entregar M outputs + N−M descartes con motivo; output parcial sin accounting es CONTRACT_CONFLICT.

Universo vacío es una fuente válida sellada, con cero particiones o particiones declaradas vacías. Un array de entrada vacío explícito nunca implica “buscar más en storage”. Límite operacional, data unavailable o falta de métricas no prueban agotamiento. Cancelar conserva evidencia y espera drenaje; no fabrica selección terminal.

## Fuentes

Mandato owner 2026-10-25; [[03 — Target Architecture and Decisions]], [[05 — Technical Specification]], [[09 — Traceability Matrix]].
