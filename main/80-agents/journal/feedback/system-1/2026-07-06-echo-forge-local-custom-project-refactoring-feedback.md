---
type: feedback
scope: session
created: 2026-07-06
updated: 2026-07-06
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[2026-07-06-echo-forge-local-custom-project-refactoring-summary]]"
aliases: []
agent: Antigravity
session_goal: "Refactor local project name to 'custom' and fix non-determinism map iterations in Temporal workflows"
source_session: "241add91-8048-41f7-b2cd-87470b589ef0"
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-07-06 - Local Custom Project Refactoring

## Context

- Agent: Antigravity
- Session goal: Local project custom folder refactoring and fixing replay non-determinism.
- Main entity: `[[symphony]]`
- Skills used: `agents-os-default`, `agents-os-bootstrap`
- Retrieval mode: Graphify
- Artifacts changed: `config.go`, `steps.go`, `generic_workflow.go`, `README.md`, `manifest.json`

## Scores

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 5
- Template fit: 5
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: Race condition in watcher upload during version bumps. Changing `manifest.json` first triggers the stager to download the versioned binary from MinIO before the local compiler finishes producing and uploading it.
- Why it was hard: It resulted in a mismatch between compiled local binary and what stager fetched, leading to runtime discrepancies.
- Proposed improvement: Document/automate that `./deploy_sqx.sh <version>` MUST compile and organize files first, and only update `manifest.json` after compilation completes.

## Most Useful Part Of Sistema 1

- What helped: Graphify query and AST analysis.
- Why it helped: Located files and definitions very fast without expensive directory walkings.
- Keep/change: Keep.

## Least Useful Or Noisy Part

- What did not help: Standard screen captures (hardcopy) from detached screen sessions.
- Why it was weak/noisy: Return 0-byte logs.
- Proposed cleanup: Check unit logs via journalctl instead.

## Missing Support

- Problem not solved by Sistema 1: Finding/terminating orphan Temporal workflows without CLI utilities on the server.
- How Sistema 1 could help next time: We wrote and executed a transient Go script using Temporal client API.
- Suggested artifact type: Transient helper scripts in `scratch/`.

## Retrieval Feedback

- Useful query or source: Graphify references to config and steps.
- Missing context: None.
- Duplicate/noisy result: None.
- Better future query: N/A.

## Skill Feedback

- Skill that worked well: `agents-os-default`
- Skill that was confusing: None.
- Trigger/routing gap: None.
- Suggested contract change: None.

## Template Feedback

- Template used: `session-feedback`
- Field that helped: "What Complicated The Session Most"
- Field that felt redundant: None.
- Missing field: None.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí.
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? Contexto total de los runs anteriores y la persistencia de las tablas.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? Sí, agregamos notas en la bitácora de la sesión.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 5. Es vital para no saturar al usuario con pánicos de replay intermedios.

## Pain Pattern Candidate

- Is this likely to repeat? yes (map iteration non-determinism in Temporal is a classic Go workflow bug).
- Suggested severity: high
- Candidate owner: Antigravity
- Promote to L3 memory? yes (add a rule about Go Temporal Workflow Determinism).

## One Next Improvement

- Sort Go map keys before iterating or spawning subworkflows/activities in Temporal to ensure replay determinism.
