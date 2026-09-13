---
type: change_log
schema_version: 1
scope: session
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[zcode-custom-subagent-definition-format]]"
  - "[[2026-09-12-zcode-subagent-factory-session-feedback]]"
aliases: []
confidence: verified
source_session: sesión ZCode 2026-09-12 (fábrica de subagents campaña Echo + Echo Forge)
source_feedbacks:
  - "[[2026-09-12-zcode-subagent-factory-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-12-zcode-custom-subagent-learning

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/learning/agents-os/zcode-custom-subagent-definition-format.md`

## Motivo

- La sesión invirtió esfuerzo material en reverse-engineering del parser de custom subagents del binario ZCode 3.11.2 porque ni la guía instalada ni Sistema 1 documentan el formato (frontmatter válido, model ref `custom:builtin:<provider>:<model>`, `thoughtLevel` con variants `low|high|max`, directorios user/project scope). Ese conocimiento es reusable y evita reinventarlo o inventar campos inválidos en futuras creaciones/auditorías de agentes.

## Fuentes usadas

- Parser real `parseAgentProfileFromMarkdown` y helpers de model ref en `/opt/ZCode/resources/glm/zcode.cjs` (binario instalado, leído read-only).
- `~/.zcode/v2/config.json` (providers, variants de reasoning) y `~/.zcode/v2/agents-state.json` (formato de overrides).
- Agente existente de referencia `judge.md` del plugin document-skills.
- Duplicate check: grep enfocado en `80-agents/memory/` y `30-resources/` — existe el runbook conductual [[delegacion-a-subagentes]] y el known error de reporte vacío, pero ningún artifact documenta el formato de definición; el learning es complementario, no duplicado.

## Resolución aplicada

- Learning nuevo `verified` bajo `learning/agents-os/`, scope global, load_policy manual, enlazado a [[AGENTS OS]] y al runbook de delegación.

## Validación

- 10 definiciones en `~/.zcode/agents/` validadas con script contra las reglas extraídas del parser (frontmatter requerido, model ref exacto, thoughtLevel ∈ {low,high,max}, tools, secciones del contrato): 10/10 PASS.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, sin secretos; menciona paths de instalación estándar de la superficie (`/opt/ZCode`, `~/.zcode`), no paths de negocio.

## Rollback

- Eliminar el archivo del learning; no hay referentes que dependan de él salvo la feedback y el checkpoint interno de la campaña.
