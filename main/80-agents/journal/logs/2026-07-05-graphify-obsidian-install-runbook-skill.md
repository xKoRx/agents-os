---
type: change_log
scope: session
created: 2026-07-05
updated: 2026-07-05
area:
project:
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Graphify-Obsidian: compilado + runbook + skill de instalación

%% Routing: entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `95-graphify/dist/graphifyy-0.9.5-py3-none-any.whl` — compilado (wheel) del fork vault-aware.
  - `95-graphify/dist/graphify-obsidian` — copia canónica del wrapper.
  - `95-graphify/dist/BUILD.md` — manifiesto (commit `9c393b7`, rama `feat/obsidian-vault-wikilinks`).
  - `80-agents/memory/public/runbook/graphify-obsidian-install.md` — runbook de instalación.
  - `80-agents/skills/agents-os-graphify-install/SKILL.md` — skill que ejecuta el runbook.
  - `80-agents/skills/INDEX.md` — registro de la nueva skill (updated).
  - `30-resources/tools/graphify.md` — Sistema 2: subsección "Instalar en otra máquina (solo comparte el vault)".
  - `80-agents/memory/internal/agent-memory/2026-07-04-graphify-obsidian-build-continuity.md` — continuidad interna (update 2026-07-05).

## Motivo

- El vault se comparte con varios agentes/máquinas, pero solo la máquina origen tenía la app (fork
  con resolución de wikilinks vault-wide). Se necesitaba un compilado portable que viaje con el vault
  y un procedimiento repetible para instalarlo en máquinas sin la app.

## Fuentes usadas

- Wrapper vivo `~/bin/graphify-obsidian` (paths de venv/vault/OUT_DIR).
- Fork `/Users/rjara/fuentes/graphify` (rama `feat/obsidian-vault-wikilinks`), `uv build --wheel`.
- `80-agents/skills/_shared/graphify-contract.md`, `note-types.md`, `skill-contract.md`.

## Resolución aplicada

- Compilado = wheel `py3-none-any` (portable) dejado en `95-graphify/dist/` (viaja con el vault y queda
  fuera del índice: la carpeta `95-graphify/` la excluye el propio wrapper).
- Runbook creado desde template; referencia el compilado, instala venv aislado + wrapper, y documenta
  que la salida cae en `95-graphify/` (fijado por `OUT_DIR` dentro del wrapper).
- Skill lean (no duplica pasos): referencia el runbook dentro del vault y decide cuándo ejecutarlo.

## Validación

- `uv build --wheel` exitoso; `graphify-obsidian --help` y `explain "AGENTS OS"` funcionan en la máquina origen.
- Pendiente de reindex tras estos cambios: `graphify-obsidian update` para indexar el nuevo runbook/skill.
