---
type: feedback
schema_version: 1
scope: session
created: 2026-10-12
updated: 2026-10-12
area: "[[Meli]]"
project: "[[RIO E2E local]]"
entities:
  - "[[RIO E2E local]]"
  - "[[rio-controlplane-clickhouse]]"
related: []
aliases: []
agent_surface: "[[Claude Code]]"
agent_model: claude-opus-5-5
agent_run: "[[2026-10-12-claude-code-claude-opus-5-5-rio-e2e-clickhouse-kiss-guidance]]"
session_goal: "Guiar al implementador del E2E local ClickHouse hacia una entrega KISS y publicable"
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/rio-e2e-local
  - agent/system1
---

# Session Feedback - 2026-10-12 - RIO E2E local ClickHouse

## Context

- Agent surface: [[Claude Code]] (guía y revisión); implementador: otro agente en sesión aparte.
- Agent model: claude-opus-5-5
- Agent run: [[2026-10-12-claude-code-claude-opus-5-5-rio-e2e-clickhouse-kiss-guidance]]
- Main entity: [[RIO E2E local]]
- Artifacts changed: sección «F2 ClickHouse KISS» en la nota del proyecto.

## What Complicated The Session Most

- Observation: el implementador previo acumuló 221 archivos (125 de evidencia/docs, receipts SHA-256, ledgers, harness de "ownership") y se detuvo varias veces por bloqueos inventados (credenciales de testing, VM "no autorizada", aprobación de grants).
- Why it was hard: el owner pedía "alcance completo" y el agente lo tradujo en certificación y evidencia, no en un E2E verde; cada restricción ambigua se convertía en un stop.
- Proposed improvement: los prompts de implementación llevan (1) patrón de referencia concreto con su tamaño, (2) presupuesto duro de archivos, (3) infraestructura autorizada con comandos exactos, (4) regla «un dato que no tienes no es un bloqueo; detente sólo ante un comando rechazado y muestra el error textual».

## Most Useful Part Of Sistema 1

- What helped: la memoria del perfil Colima `rio` (cómo arrancar con `limactl`, nunca `colima stop --profile rio`) resolvió el falso bloqueo de la VM sin investigar.
- Keep/change: keep.

## Least Useful Or Noisy Part

- What did not help: la nota [[RIO E2E local]] quedó saturada por el agente previo (párrafos de evidencia ilegibles, SHA, PIDs); el estado real costaba encontrarlo.
- Proposed cleanup: higiene de la nota: comprimir las secciones «F2 FULL local» a un enlace histórico.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: high
- Candidate owner: prompts maestros de implementación (RIO E2E local, Flink).
- Promote to L3 memory? yes — guía de prompts para agentes implementadores (presupuesto, referencia, regla de bloqueos; no condicionar avance a datos inaccesibles).

## One Next Improvement

- Aplicar la misma plantilla KISS al prompt maestro del CP Flink antes de lanzarlo.
