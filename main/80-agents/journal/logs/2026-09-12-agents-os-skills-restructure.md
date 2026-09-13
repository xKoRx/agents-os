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
  - "[[30-resources/agents/00-index]]"
  - "[[aranea-agent-dev]]"
  - "[[meli-agent-dev]]"
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

# 2026-09-12-agents-os-skills-restructure

%% Routing: area/project/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `git mv` de 13 skills no-agents-os: `80-agents/skills/<name>/` → `30-resources/agents/skills/<name>/` (deployment-proof, distributed-incident-triage, e2e-gated-validation, evidence-channel-discovery, human-first-technical-writing, operational-healthcheck-policy, pr-description, readonly-production-probe, release-certification, signals-code-review, signals-func-spec-authoring, signals-tech-spec-authoring, write-once-conflict-triage).
  - `30-resources/agents/skills/signals-code-review/SKILL.md` — refs relativas reescritas desde la nueva ubicación (`../../../../80-agents/...`, `../../../tools/...`).
  - `30-resources/agents/skills/meli-agent-dev/SKILL.md` — creada (router dominio Meli).
  - `30-resources/agents/skills/aranea-agent-dev/SKILL.md` — creada (router dominio Aranea; puerta única del acceso MCP).
  - `30-resources/agents/skills/aranea-mcps-expert/SKILL.md` — subordinada a `aranea-agent-dev` (description, Purpose, Hard Rules).
  - `30-resources/agents/skills/{sdd-workflow,sync-local-branch}/SKILL.md` — frontmatter completado (`schema_version`, `load_policy`, `indexable`, `index_priority`).
  - `80-agents/skills/INDEX.md` — reescrito en formato índice wiki: core (28 skills agents-os) + registro federado enlazado (19 vault + 3 app-owned).
  - `30-resources/agents/00-index.md` + `log.md` — catálogo del dominio con las 18 skills y registro de la operación.
  - `80-agents/skills/agents-os-bootstrap/SKILL.md` — cold start carga el registro de skills (paso 3); routing con gates de dominio.
  - `80-agents/agents-os/agents-os.md` — base always-load incluye el índice de skills.
  - `80-agents/skills/agents-os-graphify-maintenance/SKILL.md` — modelo de ejecución canónico (auto-refresh default, `update` sólo mantenimiento) + diagnóstico delta-vs-deuda-global.
  - `80-agents/skills/_shared/graphify-contract.md` — cláusula "update bloqueado no bloquea retrieval" + atribución delta/global.
  - `80-agents/skills/agents-os-session-close/SKILL.md` — "targeted Graphify reindex" reemplazado por validación con query focalizada; sección Graphify Freshness.
  - `80-agents/skills/agents-os-agent-run-register/SKILL.md` — ya no sugiere reindex manual por run.
  - `80-agents/skills/agents-os-doctor/SKILL.md` + `scripts/doctor.py` — output "Graphify freshness"; doctor extiende frontmatter/refs a skills federadas.
  - `80-agents/skills/agents-os-install/SKILL.md` + `scripts/configure-agent-surfaces.py` — reglas de superficies reconocen las dos ubicaciones físicas canónicas.
  - `80-agents/crew/Ariadna.md`, `30-resources/tools/ads-signals-skills-marketplace.md` — paths actualizados a la nueva ubicación.
  - `.graphifyignore` — recreado con las exclusiones canónicas (contrato graphify + purga 2026-07-02 + requisitos del doctor); estaba ausente del vault y del historial git.

## Motivo

- El core `80-agents/skills/` mezclaba comportamientos de AGENTS OS con skills de dominio (Signals/Meli) y transversales; el usuario pidió separar lugares, índice wiki para skills, carga del índice en bootstrap, routers de dominio Meli/Aranea y regularizar la ejecución de `graphify-obsidian`.

## Fuentes usadas

- `80-agents/skills/_shared/skill-contract.md`, `../_shared/graphify-contract.md`, `30-resources/00-RESOURCE-WIKI.md`, feedbacks graphify 2026-08-19/08-25/09-03/09-10 (update bloqueado por deuda global).

## Resolución aplicada

- Core = sólo comportamientos de AGENTS OS; dominio/transversales = `30-resources/agents/skills/` (curadas, con índice wiki de dominio); app-owned = repo dueño. `INDEX.md` mantiene su nombre (el doctor y el bootstrap lo referencian) pero adopta el formato wiki.
- Dominios excluyentes: `meli-agent-dev` ↔ `aranea-agent-dev`; las capabilities MCP `aranea-*` son exclusivas de Aranea y entran sólo vía `aranea-mcps-expert` bajo `aranea-agent-dev`.
- Graphify: las queries auto-refrescan (default); `update` explícito es mantenimiento con gate estricto; un update bloqueado por deuda fuera del delta no bloquea la sesión — se clasifica y se deriva a higiene.

## Validación

- `doctor.py --strict`: HIGH=0, MEDIUM=0, LOW=0, startup ≈5193 tokens (antes HIGH=1 por `.graphifyignore` ausente).
- Instalación de `graphify-obsidian` en esta máquina (kor): NO ejecutada — sin wheel en `~/.local/share/graphify-obsidian/dist/` ni `AGENTS_OS_GRAPHIFY_SOURCE`; el runbook prohíbe fuentes improvisadas. Queda como instalación pendiente por máquina.
- Validación de retrieval Graphify (explain/query sobre las skills movidas): pendiente hasta instalar el binario; las rutas y aliases son resuolubles por nombre canónico.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert` del commit de esta iteración, o `git mv` inverso de los 13 directorios + restaurar `INDEX.md`, `00-index.md`, bootstrap y scripts desde el commit previo. `.graphifyignore` recreado: borrar el archivo si se quiere el estado anterior.
