---
type: raw_session
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
  - "[[2026-09-12-agents-os-skills-restructure-summary]]"
related: []
aliases:
  - "restructura skills agents-os"
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-09-12-agents-os-skills-restructure-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: [[ZCode]] × GLM-5.3-Flash (run: [[2026-09-12-zcode-glm-5.3-flash-agents-os-skills-restructure]])
- Proyecto o entidad: [[AGENTS OS]]
- Objetivo de la sesión: revisión integral de skills de AGENTS OS pedida por el usuario: lugares correctos, índice wiki, índice en bootstrap, routers meli/aranea, regularizar graphify-obsidian; cierre con feedback.

## Transcript

```
Usuario: necesito que revises las skills de agents os: (1) que estén en el lugar correcto — skills de agents os sólo para comportamientos de agents os, y un index con formato llm wiki igual que las skills de resources; (2) que el bootstrap cargue los índices de skills al iniciar; (3) skills meli-agent-dev y aranea-agent-dev con dominios distintos, p.ej. los servicios mcp de aranea sólo para aranea agent dev; (4) regularizar la ejecución de graphify obsidian. Luego cierra sesión y deja feedback.

Agente (síntesis de acciones; detalle en [[2026-09-12-agents-os-skills-restructure]]):
- git mv de 13 skills no-agents-os a 30-resources/agents/skills/; refs de signals-code-review reescritas; paths en crew/Ariadna y ads-signals-skills-marketplace actualizados.
- INDEX.md reescrito en formato wiki (core 28 + federado 19 + app-owned 3); 00-index y log del dominio agents actualizados.
- meli-agent-dev y aranea-agent-dev creadas; aranea-mcps-expert subordinada a aranea-agent-dev.
- bootstrap: cold start carga INDEX.md; routing con gates de dominio; agents-os.md actualizado.
- graphify: modelo de ejecución + diagnóstico delta-vs-deuda-global en graphify-maintenance y graphify-contract; session-close/run-register sin reindex manual; doctor output "Graphify freshness".
- doctor.py: cobertura extendida a skills federadas; sdd-workflow y sync-local-branch completaron frontmatter.
- .graphifyignore recreado (ausente del vault y del historial git; doctor HIGH).
- graphify-obsidian NO instalable en kor: sin wheel local ni AGENTS_OS_GRAPHIFY_SOURCE; runbook prohíbe fuentes improvisadas → pendiente.
- Validación: doctor --strict HIGH=0 MEDIUM=0 LOW=0, startup ≈5193 tokens.
```

## Evidencia externa

- Ninguna; trabajo íntegro sobre el vault.
