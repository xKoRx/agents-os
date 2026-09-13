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
  - "[[2026-09-12-agents-os-runbooks-restructure]]"
  - "[[2026-09-12-agents-os-domain-gate]]"
  - "[[30-resources/runbooks/00-index]]"
related: []
aliases:
  - "runbooks y domain gate"
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

# 2026-09-12-agents-os-runbooks-domain-gate-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Verificar la mudanza de skills, replicarla en runbooks e implementar la carga inteligente por dominio (area → router), con cierre y feedback.

## Contexto cargado

- Warm turn sobre [[AGENTS OS]]; base ya cargada (constitución, perfil, continuidad, INDEX.md). Sin Graphify (binario ausente en kor).

## Trabajo realizado

- Runbooks: 10 archivos + `symphony/` movidos a `30-resources/runbooks/`; 5 agents-os quedaron en `80-agents/memory/public/runbook/`; índice wiki + log del dominio; duplicado `signals-code-review.md` marcado superseded; refs corregidas.
- Domain gate: paso 6 del cold start de bootstrap mapea `area` → router (`[[Meli]]`; `[[Echo]]`/`[[Aranea]]`); fail-closed; swap reemplaza pack; anomalía `area: [[Symphony]]` corregida; línea conceptual en context-router.

## Artifacts creados o modificados

- [[2026-09-12-agents-os-runbooks-restructure]] y [[2026-09-12-agents-os-domain-gate]] (change_logs); `30-resources/runbooks/00-index.md` + `log.md`; bootstrap, context-router, aranea-agent-dev, nota del proyecto Echo Forge.

## Memoria propuesta o creada

- Ninguna L3 nueva; reglas en artefactos canónicos.

## Decisiones

- Detección de dominio por `area` canónica (propuesta del usuario), keywords/MCP prefixes sólo como fallback; ambigüedad falla cerrada.
- Runbooks de AGENTS OS no entran al índice de `30-resources/runbooks/` (las skills del core los referencian por path).

## Pendiente

- Instalar `graphify-obsidian` en kor (wheel o `AGENTS_OS_GRAPHIFY_SOURCE`) y validar retrieval de skills/runbooks movidos.
