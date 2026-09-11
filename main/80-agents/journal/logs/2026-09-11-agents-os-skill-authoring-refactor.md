---
type: change_log
schema_version: 1
scope: session
created: "2026-09-11"
updated: "2026-09-11"
area:
project:
application:
entities: []
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-11-agents-os-skill-authoring-refactor

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `80-agents/skills/agents-os-skill-authoring/SKILL.md` — refinado.
  - `80-agents/memory/public/runbook/agents-os-skill-authoring.md` — creado.

## Motivo

- Separar policy/orchestration de ejecución mecánica: la skill decide clasificación, trigger boundary, contrato y handoffs; el runbook ejecuta materialización, validación, rollback y registro.
- Hacer explícita la frontera de activación y comprobar casos positivo, negativo y adyacente.
- Reducir acoplamiento entre la semántica de authoring y tooling que puede cambiar independientemente.

## Fuentes usadas

- `80-agents/agents-os/agents-os.md`
- `80-agents/skills/_shared/note-types.md`
- `80-agents/skills/_shared/skill-contract.md`
- `80-agents/skills/_shared/schema-contract.md`
- `80-agents/templates/skill.md`
- `80-agents/templates/runbook.md`
- Documento de rediseño entregado por el usuario el 2026-09-11.

## Resolución aplicada

- Se removió de la skill la responsabilidad de ejecutar materialización, validación mecánica, rollback y mecánica del `change_log`.
- Se agregó trigger boundary explícito y gate mínimo de activación positivo/negativo/adyacente.
- Se creó un runbook operacional emparejado con la skill usando el shape canónico vigente del vault.
- No se modificó `templates/runbook.md`: la versión vigente ya contiene `Precondiciones`, `Procedimiento`, `Validación`, `Rollback / recuperación` y `Evidencia`, por lo que el cambio sugerido por el documento adjunto ya estaba absorbido en el repositorio.

## Validación

- Skill mantiene las secciones exigidas por el contrato vigente: `Purpose`, `Procedure`, `Hard Rules`, además de `Minimal Read` y `Output` del template actual.
- Runbook mantiene las secciones del template vigente: `Propósito`, `Precondiciones`, `Procedimiento`, `Validación`, `Rollback / recuperación`, `Evidencia`.
- Trigger positivo: crear/refinar/revisar/deprecar una skill → PASS.
- Trigger negativo: ejecutar un runbook operacional ya definido sin cambiar el contrato de una skill → PASS; no carga esta skill.
- Trigger adyacente: capturar memoria → PASS; handoff a `agents-os-memory-distillation`.
- Separación skill/runbook: PASS.
- Read-back/validación estructural contra fuentes canónicas: PASS.
- `validate_schema_contract.py`: **NOT RUN** — la superficie ChatGPT + GitHub no expone ejecución del runtime del repositorio.
- Graphify targeted reindex: **NOT RUN** — Graphify es estado local y no está expuesto en esta superficie.
- No se declara validación ejecutable ni reindex como realizados; quedan como próximo gate al operar desde el vault local.
- No se modificaron contratos ni templates canónicos fuera del scope.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos.

## Rollback

- Revertir `80-agents/skills/agents-os-skill-authoring/SKILL.md` a su versión anterior y eliminar `80-agents/memory/public/runbook/agents-os-skill-authoring.md` junto con este log si el contrato de authoring se revierte como una sola unidad.
