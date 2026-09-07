---
type: agent_run
schema_version: 1
scope: session
created: "2026-08-28"
updated: "2026-08-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-28-durable-artifact-verified-reads-final-e2e-normal]]"
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
model_source: unknown
task_type: testing
task_complexity: high
outcome: partial
verification: verified
evaluator: agent
user_rework: unknown
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-08-28-codex-durable-artifact-verified-reads-certification

## Trabajo

- **Objetivo:** Certificar en runtime real que artifacts durables evidence-backed se verifican por Size+SHA256 antes de consumo.
- **Alcance atribuible a esta combinación superficie×modelo:** Release/deploy `0.2.78`, auditoría final de readers, intake normal y harness físico disposable; cierre sin cambios de producto.
- **Artefactos afectados:** Evidencia operacional y notas Agents OS; no source code.

## Evidencia

- **Validaciones ejecutadas:** Tests dirigidos de storage boundary, WFM físico, MT5 y carriers; deploy/matriz de workers; intake `example_flow_23`; harness MinIO real para valid/mismatch/missing/cohort.
- **Resultado observable:** Boundary de descarga rechazó corrupción same-size y objeto faltante antes de publicación; workers compartieron release; auditoría detectó blocker en `ReconcileApplySelectedRun`.
- **Limitaciones de la evidencia:** Cadena completa Builder→WFM→Apply→FinalReretester→MQ5→EX5→HTM no se certifica como PASS porque el blocker apareció antes del cierre. Suite SDK completa con fallos de dependencias privadas y drift preexistente.

## Evaluación

%% Scores opcionales 1–5: agregar al frontmatter sólo cuando exista evidencia suficiente. Si son autoevaluados, conservar evaluator: agent. %%

- **Correctness:**
- **Autonomy:**
- **Efficiency:**
- **Tool use:**
- **Overall:**

## Resultado

- **Outcome:** BLOCKED / CLOSED; defecto reusable identificado.
- **Rework posterior:** Requiere `DURABLE-ARTIFACT-VERIFIED-READS-APPLY-RCA-TOP`; no se hizo fix aquí.
- **Aprendizaje para comparar herramientas:** Un GET que calcula su propio SHA no es verified read; debe conservarse separada la autoridad del carrier y la prueba física.
