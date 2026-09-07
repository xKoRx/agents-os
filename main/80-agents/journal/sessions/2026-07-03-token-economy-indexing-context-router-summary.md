---
type: session
scope: session
created: 2026-07-03
updated: 2026-07-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Economía de Tokens]]"
related:
  - "[[token-economy-indexing-architecture]]"
  - "[[context-router]]"
  - "[[graphify]]"
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-07-03 — Economía de tokens: LLM Wiki + Graphify + Context Router

> [!info]+ Session summary L1

## Objetivo

- Integrar el patrón LLM Wiki en `30-resources/`, evaluar Graphify, y diseñar un sistema de indexación/tageo óptimo en tokens para agentes (a evangelizar en un equipo de TI).

## Contexto cargado

- AGENTS OS (constitución, perfil, memoria interna), Resource Wiki, doc de Graphify, repo completo de Graphify en `/Users/rjara/fuentes/graphify`.

## Trabajo realizado

- Formalizada la wiki de recursos (piloto `applications/`), depurado Graphify (`.graphifyignore`), descartada la semántica LLM (deepseek-r1 pobre, Gemini free tier insuficiente).
- Definida arquitectura de 4 capas (ADR) y el concepto Context Router.
- Evaluado el repo de Graphify: fuerte en código, sin extractor estructural de markdown/wikilinks; schema enchufable → builder propio.
- Principio global "una fuente canónica por hecho" + skill de autoría de skills.

## Artifacts creados o modificados

- ADR `token-economy-indexing-architecture`; concepto `context-router`; proyecto `Economía de Tokens`; skills `agents-os-resource-wiki`, `agents-os-skill-authoring`; runbook `resource-wiki-lint-reindex`; `00-RESOURCE-WIKI.md`; template `index.md`; piloto `applications/00-index.md`+`log.md`; idea de experimentos; constitución (mandamiento 16 + regla de wiki + regla "una fuente por hecho"); `skill-contract.md` (Audience Split); varios changelogs.

## Memoria propuesta o creada

- Known-error: gaps de Graphify en markdown/wikilinks + pitfalls de backend.
- Continuidad interna actualizada; feedbacks de sesión y de Graphify.

## Decisiones

- Vault opera con índices (curado + AST), no con semántica LLM. Graphify semántico solo para código vía API paga.
- Builder propio de wikilinks que emite schema de Graphify (no reemplazar, alimentar).

## Pendiente

- PoC del builder (otra IA), corregir token budget del Context Router, auditoría de consistencia, adelgazar `agents-os.md` (solo diseño).
