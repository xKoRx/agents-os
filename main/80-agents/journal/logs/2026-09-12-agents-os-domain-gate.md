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
  - "[[meli-agent-dev]]"
  - "[[aranea-agent-dev]]"
  - "[[context-router]]"
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

# 2026-09-12-agents-os-domain-gate

%% Routing: area/project/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + conflict-resolution
- **Archivo(s):**
  - `80-agents/skills/agents-os-bootstrap/SKILL.md` — nuevo paso 6 del cold start: domain gate a partir del `area` de la entidad activa (`[[Meli]]` → `meli-agent-dev`; `[[Echo]]`/`[[Aranea]]` → `aranea-agent-dev`; otra área o sin entidad → sin router; evidencia ambigua o en conflicto falla cerrada). Entity swap re-aplica el gate y reemplaza el pack de dominio; nunca dos packs a la vez. Lazy Skill Routing actualizado con el mapeo por área.
  - `80-agents/agents-os/context-router.md` — línea conceptual: la selección de dominio ocurre en el startup (bootstrap, por `area`); el context router decide la profundidad dentro del dominio.
  - `30-resources/agents/skills/aranea-agent-dev/SKILL.md` — `related` incorpora `[[Echo]]` y `[[Echo Forge]]` (el router cubre ambas áreas del homelab).
  - `10-projects/Echo Forge/agentes/echo-forge-wfm-troubleshooting.md` — `area: [[Symphony]]` → `[[Echo]]` (Symphony es el repo, no un área).

## Motivo

- El usuario pidió carga inteligente por dominio: según el prompt inicial, el agente debe saber si la tarea es Meli o Aranea sin mezclar dominios. La señal canónica es el `area` obligatorio de las notas (proyectos: Echo 33, Meli 32, Aranea 11, Personal 3; aplicaciones: Echo 17, Meli 14, Personal 1), no heurísticas de keywords.

## Fuentes usadas

- Conteo de `area` en `10-projects/` y `30-resources/applications/`; routers existentes; constitución (bootstrap dueño único del startup).

## Resolución aplicada

- Gate de evidencia con 3 salidas: dominio demostrado por área → router correspondiente; sin entidad pero con evidencia de superficie (`mcp__aranea-*`, tooling corporativo Zord/Fury/Spellbook) → router; ambigüedad o áreas ajenas → sin router (fail-closed). La defensa queda en profundidad: gate → router (re-chequea boundary) → skill especializada con su propio gate (ej. Meli en `signals-code-review`).

## Validación

- `doctor.py --strict`: HIGH=0 MEDIUM=0 LOW=0.
- Cobertura de `area` verificada por conteo; anomalía `[[Symphony]]` corregida (única ocurrencia).

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert` del commit, o restaurar bootstrap/context-router/anomalía desde el commit previo.
