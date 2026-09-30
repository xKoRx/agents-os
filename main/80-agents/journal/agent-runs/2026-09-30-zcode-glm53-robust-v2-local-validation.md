---
type: agent_run
schema_version: 1
scope: session
created: "2026-09-30"
updated: "2026-09-30"
area: "[[Echo]]"
project: "[[Echo Forge — Robust Run Selection V2]]"
application:
entities:
  - "[[Echo Forge — Robust Run Selection V2]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
model_source: plan
task_type: testing
task_complexity: high
outcome: success
verification: run
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-09-30-zcode-glm53-robust-v2-local-validation

## Trabajo

- **Objetivo:** mandato "ROBUST RUN SELECTION V2 — LOCAL REAL-DATA VALIDATION": ejecutar V1 vs V2 sobre exactamente los mismos datos reales de la cohorte wave2a y reportar qué cambia (picks, rejections, cliff/bandas, aggregate, sanity), con veredicto `LOCAL_VALIDATION_PASS|FOUND_IMPLEMENTATION_DEFECT|BLOCKED`; sin cambiar product code ni tunear parámetros (trial 0.35/0.01/0.01 tal cual).
- **Alcance atribuible a esta combinación superficie×modelo:** verificación del worktree limpio @ `bc50bbb` sobre `origin/feature/robust-selection-v2-shot1` (con sdk sibling symlink); reconstrucción del execution path canónico (`evaluateNeighborhoods` → picks → rank1, `wfm.SelectRobustV2`); localización y verificación SHA256 del corpus wave2a (`cells.tsv` 1.836 cells, hash `3e0dac…` == manifest — refutando en esta máquina el finding "zero bytes"); captura del V1 config efectivo (spec wave2a sin `wfm_params` → defaults durables frozen); probe temporal no-commiteado en el binding que ejecuta el evaluador durable real + telemetría por-vecindario con `SelectRobustV2` permisivo; análisis Python de cambios/rejections/aggregate/5 casos; artefactos CSV+MD en el proyecto; limpieza (probe eliminado, worktree removido, tree limpio, regresiones V1/V2 re-verde).
- **Artefactos afectados:** `10-projects/Echo Forge — Robust Run Selection V2/ROBUST-V2-LOCAL-VALIDATION.csv` y `ROBUST-V2-LOCAL-VALIDATION.md` (nuevos); `artifacts/local-validation-20260930/` (6 archivos crudos); nota de proyecto (bitácora/estado); este agent-run. Repo `xKoRx/symphony`: cero cambios.

## Evidencia

- **Validaciones ejecutadas:** SHA256 de `cells.tsv` contra manifest y contra la copia original del workspace de recovery (match exacto); `go vet` limpio del paquete binding con el probe; probe PASS con asertos internos (sets de sobrevivientes == picks reales de V2 en 34/34, TopN prefix order); regresiones post-limpieza `go test -count=1 ./sqx/core/wfm/... ./sqx/adapters/wfm/binding/...` PASS; `git status` limpio en worktree y clon base; `git worktree list` sin restos.
- **Resultado observable:** `LOCAL_VALIDATION_PASS`. 34 estrategias; V1 18 con picks (12 WARN + 6 FAIL-SEVERE) / V2 18 (18 WARN); mismo set exacto de 16 rechazadas (`NO_ACCEPTABLE_NEIGHBORHOOD`, sin 3×3 completo — V2 no rechaza nada extra); 13/18 rank1 cambiados, todos hacia menor `R_retdd` (12/13 también menor `R_aux`); 7 sacrifican mediana Ret/DD (mediana −1,24, peor −2,18), 5 mejoran, 1 empata; cliff 0,35 corta 26/214 vecindarios (12,15%, idéntico al adversarial de diseño) y rechaza 3 centers de V1 que estaban sobre acantilados; las 6 FAIL-SEVERE de V1 (pico aislado 2,0–3,1σ auto-gateado) pasan a WARN en V2. Sin defecto de implementación; sin rechazos excesivos.
- **Limitaciones de la evidencia:** la comparación no reclama identidad histórica byte a byte: los `aggregates.tsv`/`picks.tsv` del bundle corresponden a otra materialización (discrepancia Optimizer-vs-WFM registrada el 2026-09-29); el input único real y autoconsistente es `cells.tsv`. El probe fue temporal y se eliminó; sus construcciones/resultados quedan en los artefactos. Sin Stores/PG/Temporal (frontera durable fuera del alcance declarado del mandato).

## Evaluación

%% Scores opcionales 1–5: agregar al frontmatter sólo cuando exista evidencia suficiente. Si son autoevaluados, conservar evaluator: agent. %%

- **Correctness:** 5 — cross-validation temprana contra los outputs de referencia del bundle atrapó 3 problemas (parseo de keys, slicing TopN vs sobrevivientes, filas fantasma con floats cero) antes del análisis; el hallazgo se resolvió como discrepancia de materialización documentada, no silenciada.
- **Autonomy:** 5 — cadena completa dataset→config→ejecución→análisis→artefactos→cleanup sin bloqueos, incluyendo descarte de vías muertas (Mongo legacy, PG sin schema sqx) por evidencia.
- **Efficiency:** 4 — el forense de lineage del bundle consumió varios pasos antes de decidir "mismo input, sin reclamo histórico" (el mandato ya lo había eximido del replay histórico).
- **Tool use:** 5 — reutilización del evaluador durable real vía probe en-paquete (patrón Shot-2), MCP RO (Mongo/etcd) sólo para descarte, `materialize_schema_note.py` para esta nota.
- **Overall:** 5

## Resultado

- **Outcome:** `LOCAL_VALIDATION_PASS` — ejecución auditable sobre datos reales, sin defecto material; resultados entregados al Primary Technical Manager + Owner (parámetros trial sin tuning, decisión de moverlos es del Owner).
- **Rework posterior:** unknown.
- **Aprendizaje para comparar herramientas:** cuando un bundle contiene outputs de referencia y el input materializado, validar temprano la reproducibilidad de los reference outputs: aquí eso convirtió una falsa "no reproducción" en el hallazgo correcto (dos materializaciones del mismo cohort) en lugar de un falso defecto del algoritmo.
