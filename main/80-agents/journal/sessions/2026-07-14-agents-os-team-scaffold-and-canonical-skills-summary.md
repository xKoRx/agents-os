---
type: session
scope: session
created: 2026-07-14
updated: 2026-07-14
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[2026-07-14-agents-os-team-scaffold-and-canonical-skills-raw]]"
  - "[[Skills de AGENTS OS viven en una única fuente canónica]]"
  - "[[AGENTS OS - Beta y Hardening]]"
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
  - project/agentsos
---

# AGENTS OS team scaffold and canonical skills — session summary

> [!info]+ Session summary L1
> Resumen operativo fuera del corpus normal de Graphify.

## Objetivo

- Preparar una versión compartible de AGENTS OS y un onboarding ejecutable por
  agentes para cada integrante del equipo.

## Contexto cargado

- Guía, constitución, perfil, skills de instalación/cierre/feedback y contratos
  de Graphify, metadata y tipos.

## Trabajo realizado

- Se alinearon scaffolding, README, prompt maestro, perfil seed, aplicaciones,
  Graphify, higiene y proyecto de instalación.
- Se fijó `80-agents/skills/` como única ubicación física y se removieron los
  adapters por cliente.
- Codex y Claude aprobaron smoke tests read-only por nombre contra la fuente
  canónica; el benchmark real quedó en [[AGENTS OS - Beta y Hardening]].

## Artifacts creados o modificados

- [[Instalación de AGENTS OS]], [[agents-os-install]], reglas de Codex/Claude,
  README, changelogs y scaffolding compartible.

## Memoria propuesta o creada

- [[Skills de AGENTS OS viven en una única fuente canónica]].

## Decisiones

- Las capacidades nativas de discovery son optimizaciones por superficie, no
  autorización para duplicar skills.

## Pendiente

- Forward-test real en Codex y Claude desde procesos reiniciados.
- Comparar rule-routing, path explícito y discovery nativo por costo y éxito.
