---
type: change_log
schema_version: 1
scope: session
created: "2026-10-03"
updated: "2026-10-03"
area:
project:
application:
entities: []
related:
  - "[[technical-project-manager]]"
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

# Technical Project Manager — role × surface policy

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `30-resources/agents/skills/technical-project-manager/SKILL.md`

## Motivo

- Formalizar tres capability roles: GOD, TOP y NORMAL.
- Separar capability role, work function y execution surface.
- Hacer explícito el sweet spot CLOUD vs LOCAL para aprovechar capacidad cloud abundante sin desperdiciar cuota local con MCP/SSH.
- Hacer esta política visible para Primary Managers y SUBMANAGERS.

## Fuentes usadas

- Decisión explícita del Owner, 2026-10-03.
- `80-agents/agents-os/agents-os.md`
- `80-agents/skills/agents-os-skill-authoring/SKILL.md`
- `80-agents/memory/public/runbook/agents-os-skill-authoring.md`
- `80-agents/skills/_shared/skill-contract.md`
- `80-agents/skills/_shared/schema-contract.md`

## Resolución aplicada

- GOD = GPT-6 Astra, CLOUD o LOCAL.
- TOP = GPT-5.6 Sol, CLOUD o LOCAL.
- NORMAL = GLM-5.3-Flash, LOCAL.
- CLOUD: sin MCP/SSH; puede usar DEEPRESEARCH y deriva otros especialistas mediante master prompts Owner-mediated.
- LOCAL: MCP/SSH cuando el harness los expone; subagentes directos cuando están disponibles y autorizados.
- Preferencia por CLOUD para reasoning/review/research y por LOCAL para ejecución física/evidencia.
- Política temporal de capacidad: consumir agresivamente OpenAI Pro CLOUD en Echo Futures, backtesting/historical-data readiness y Echo Forge; preservar cuota LOCAL para tooling.

## Validación

- Inspección post-write de las secciones role mapping, surface selection, SUBMANAGER orchestration, mandate contract y Hard Rules.
- Frontmatter de la skill mantiene `type: skill`, `schema_version: 1`, `scope: global` y tags requeridos.
- Trigger positivo: gestión técnica multi-agente con selección de surface/role.
- Trigger negativo: tarea de implementación aislada sin función de manager.
- Trigger adyacente: deep research puro sigue perteneciendo al especialista DEEPRESEARCH; la skill sólo lo orquesta.
- Validación ejecutable local del repositorio no disponible desde esta superficie GitHub; queda pendiente de `agents-os-doctor`/lint local si se requiere gate mecánico completo.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni paths de máquina.

## Rollback

- Revertir commit `4b63df1a76c7c09a217709ed47d851c433b7ff92` si la política de roles/surfaces se reemplaza por otra decisión canónica.
