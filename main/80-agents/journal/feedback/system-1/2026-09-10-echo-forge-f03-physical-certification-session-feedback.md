---
type: feedback
schema_version: 1
scope: session
created: "2026-09-10"
updated: "2026-09-10"
area: "[[Echo]]"
project: "[[Echo Forge]]"
entities: ["[[AGENTS OS]]", "[[Echo Forge]]", "[[Symphony]]"]
related: ["[[2026-09-10-codex-unknown-echo-forge-f03-physical-certification]]"]
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run: "[[2026-09-10-codex-unknown-echo-forge-f03-physical-certification]]"
session_goal: "F-03 resume physical certification"
source_session: F03-PHYSICAL-CERT-2026-09-10
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags: ["kind/feedback", "scope/session", "project/agents-os", "agent/system1"]
---

# Session Feedback — 2026-09-10 — Echo Forge F-03

## Context

- La reanudación requirió separar intentos con contratos legacy inválidos de la evidencia certificable y mantener el lab aislado.
- Se encontró una fricción de operación: Temporal está disponible en Hera, no en el PATH local; el wrapper remoto resolvió la ejecución sin exponer secretos.

## Improvement

- Documentar en el runbook de certificación el binario remoto de Temporal y preferir una superficie SQX live con output durable verificable para P1.
