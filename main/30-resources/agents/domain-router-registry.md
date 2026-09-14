---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[meli-agent-dev]]"
  - "[[aranea-agent-dev]]"
aliases:
  - domain router registry
  - registro de routers de dominio
tags:
  - kind/doc
  - tech/agents-os
  - action/domain-routing
created: "2026-09-14"
updated: "2026-09-14"
---

# Domain Router Registry

## Propósito

Declarar fuera del core qué router corresponde a cada área y qué evidencia de
tarea puede resolverlo cuando no existe una entidad. El bootstrap consume este
registro de forma opcional y fail-closed; no contiene lógica de startup.

## Contenido

| Domain | Areas | Router | Evidence markers |
|---|---|---|---|
| `meli` | `[[Meli]]` | `30-resources/agents/skills/meli-agent-dev/SKILL.md` | `meli`, `zord`, `fury`, `spellbook` |
| `aranea` | `[[Aranea]]`, `[[Echo]]` | `30-resources/agents/skills/aranea-agent-dev/SKILL.md` | `aranea`, `mcp__aranea-` |

Contrato:

- El match de área es exacto después de normalizar el wikilink.
- La evidencia sólo cuenta si pertenece a la tarea; la mera disponibilidad de
  una herramienta en la máquina no activa un dominio.
- Cero matches significa DEFAULT sin router; un match carga exactamente ese
  router; más de un match falla cerrado y no carga ninguno.
- Cada router posee sus preferencias, skills y runbooks scoped. Este registro
  no los enumera ni permite fallback hacia otro dominio.
- El archivo puede faltar o contener cero filas en una distribución nueva; ese
  estado es DEFAULT válido.

## Fuentes

- `80-agents/skills/agents-os-bootstrap/SKILL.md` — consumidor ejecutable.
- `30-resources/agents/skills/*-agent-dev/SKILL.md` — routers registrados.
