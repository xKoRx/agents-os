---
type: session
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
  - "[[2026-09-12-agents-os-skills-restructure]]"
  - "[[meli-agent-dev]]"
  - "[[aranea-agent-dev]]"
related: []
aliases:
  - "restructura skills agents-os"
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-09-12-agents-os-skills-restructure-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Separar skills de AGENTS OS de skills de dominio/transversales, dar índice wiki a las skills, cargarlo en bootstrap, crear routers de dominio Meli/Aranea y regularizar la ejecución de `graphify-obsidian`.

## Contexto cargado

- Bootstrap cold start: constitución, perfil rjara, continuidad global; INDEX.md (antes del cambio); [[30-resources/00-RESOURCE-WIKI]]; contratos skill/graphify; feedbacks graphify 2026-08/09.

## Trabajo realizado

- Mudanza de 13 skills no-agents-os a `30-resources/agents/skills/` con refs y paths corregidos.
- `80-agents/skills/INDEX.md` reescrito en formato wiki (core + federado enlazado); dominio `agents` con 00-index y log al día.
- Skills nuevas [[meli-agent-dev]] y [[aranea-agent-dev]]; [[aranea-mcps-expert]] subordinada (MCP exclusivo de Aranea).
- Bootstrap carga el registro de skills en cold start; routing con gates de dominio.
- Graphify: modelo de ejecución canónico + diagnóstico delta-vs-deuda-global; cierres sin reindex manual.
- Doctor extiende cobertura a skills federadas; `.graphifyignore` recreado.

## Artifacts creados o modificados

- Inventario completo: [[2026-09-12-agents-os-skills-restructure]] (change_log).

## Memoria propuesta o creada

- Ninguna L3 nueva; las reglas quedaron en artefactos canónicos (contrato, skills, doctor).

## Decisiones

- `INDEX.md` conserva su nombre (doctor y bootstrap lo fijan) y adopta el formato wiki.
- Instalación de `graphify-obsidian` en kor: detenida por falta de fuente local (runbook); queda pendiente.

## Pendiente

- Instalar `graphify-obsidian` en esta máquina (requiere wheel o `AGENTS_OS_GRAPHIFY_SOURCE`) y validar retrieval de las skills movidas.
