---
type: feedback
schema_version: 1
scope: session
created: "2026-09-27"
updated: "2026-09-27"
area: "[[Echo]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures — D2-07C Execution Runtime Topology]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
session_goal: "D2-07C Execution Runtime Topology / Bridge vs Sibling / Sessions / M2 Journal Placement"
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

# Session Feedback — 2026-09-27 — Echo Futures D2-07C

## Context

- One-shot TOP Architecture Worker bajo SUBMANAGER D2.
- Goal: decidir extend V3 bridge vs futures-bridge sibling, topología runtime, sesiones, side-effect authority, colocación journal M2 y routing Kafka.
- Baselines verificados: Agents-OS `9f3c950bd86e5a83f9af1fbeec841888c0898ebf`; Echo `372af59a7b83604781346613da01e3d510ea1360` sin delta.
- Trabajo documental/arquitectónico sobre source local; sin implementación productiva ni mutación de infra; sin agent_run.
- Artifact producido: [[Echo Futures — D2-07C Execution Runtime Topology]].

## Friction / Pain Pattern Candidate

- La nota planificadora [[Echo Futures]] superó el límite de lectura de una pasada (~40k tokens estimados; el Read truncó a 950/1729 líneas y exigió segunda lectura). Cada worker D2 lee la nota completa como autoridad. **Candidate:** cuando D2 se integre, mover las secciones de gate ya congeladas (D2-04..07) a sus artefactos propios y dejar en la nota planificadora sólo estado/decisiones owner vigentes, para mantener el hot path de lectura bajo el techo.
- Ninguna otra fricción: bootstrap, retrieval por lista de autoridades del mandato, inspección git y escritura funcionaron sin degradación; no hubo fallbacks ni reintentos de herramientas.

## What Complicated The Session Most

- Mantener la decisión de bridge honesta ante el mandato: la tentación natural era extender `v3/bridge` porque su sesión per-account ya resuelve el 80% del problema; el gate físico (`//go:build windows` + Named Pipes + constraint Topstep de dispositivo personal) fue lo que cerró `FUTURES_BRIDGE_SIBLING` por host/OS y no por gusto arquitectónico.
- Formular side-effect authority sin prometer HA falsa: Kafka ownership no es fencing y un fencing token no detiene a un proceso particionado que aún alcanza al venue; la conclusión honesta V1 fue `NO AUTOMATIC CROSS-HOST TAKEOVER` + fail-closed.
