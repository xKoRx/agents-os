---
type: agent_memory
scope: project
created: 2026-07-14
updated: 2026-09-09
memory_state: archived
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Beta y Hardening]]"
  - "[[Skills de AGENTS OS viven en una única fuente canónica]]"
aliases: []
confidence: high
load_policy: manual
indexable: false
index_priority: never
tags:
  - agent/internal
  - kind/agentmemory
  - scope/project
  - project/agentsos
---

# AGENTS OS team distribution continuity — 2026-07-14

- El scaffolding compartible está en
  `/Users/rjara/obsidian/SecondBrain/agents-os`; no contiene memorias ni
  sesiones personales y el proyecto de instalación conserva todos sus checks
  abiertos.
- Invariante vigente: skills físicas sólo en `80-agents/skills/`. No recrear
  `.agents/skills`, `.claude/skills`, symlinks ni adapters.
- Smoke read-only por nombre pasó en procesos frescos de Codex y Claude. La
  sesión Codex ya abierta conservó un catálogo con la ruta anterior: reiniciar
  antes de evaluar discovery nativo.
- Pendiente real en [[AGENTS OS - Beta y Hardening]]: ejecución completa y
  benchmark rule-routing vs path explícito vs discovery nativo, midiendo
  tokens, latencia y tasa de éxito.
- Graphify fue reindexado después de la corrección; `agents-os-install` resuelve
  al `SKILL.md` canónico y el generador de adapters ya no aparece.
- El Grid de evaluación quedó publicado como versión 2 en
  `01KXGAY6QKSZWEBR5SCY5JSWCE`: score 7,0, 26 skills, 122 feedbacks y estado
  de distribución al 2026-07-14. El ZIP no quedó embebido por decisión del
  owner; se comparte aparte por Slack. El HTML se regenera con el builder del
  proyecto para evitar drift entre JSON, portada SVG y presentación.
