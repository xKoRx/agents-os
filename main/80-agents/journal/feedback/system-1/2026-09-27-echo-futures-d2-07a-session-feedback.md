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
  - "[[Echo Futures — D2-07A Execution Adapter Contract]]"
aliases: []
agent_surface: "[[ChatGPT]]"
agent_model: GPT-5.6 Sol
session_goal: "D2-07A Generic Execution Adapter Contract / Idempotency / Finality"
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

# Session Feedback — 2026-09-27 — Echo Futures D2-07A

## Context

- One-shot TOP Architecture Worker bajo SUBMANAGER D2.
- Goal: definir contrato genérico de execution adapter, M1/M2, submission journal, finality, readiness y recovery sin seleccionar transport ni diseñar D2-07C.
- Baselines verificados: Agents-OS master al bootstrap `e90aeed...`; Echo `372af59a7b83604781346613da01e3d510ea1360` sin delta.
- Trabajo documental/arquitectónico; no hubo implementación de código productivo ni agent_run.
- Artifact producido: [[Echo Futures — D2-07A Execution Adapter Contract]].

## Friction / Pain Pattern Candidate

- El research D1 de transport contiene afirmaciones worker antiguas que son más optimistas que las manager corrections posteriores (p. ej. idempotency/client IDs/history). Para D2-07A fue necesario tratar el research como corpus candidato y usar las correcciones del D1 Analysis Pack como autoridad. **Candidate:** los reports aceptados deberían llevar una cabecera visible de supersession/corrections cuando el manager los acepta con correcciones, para reducir el riesgo de reusar claims stale.
- El contrato D2-04 §2.3 aún permite wording de execution-id sintético determinístico, mientras el mandato D2-07A prohíbe inventar dedup identity si el provider no entrega identity material. Se exportó como contradicción a integrar por SUBMANAGER; no se editó D2-04 desde este worker.

## What Complicated The Session Most

- Separar tres verdades que en Echo V3 están mezcladas: command delivery, local result journal y physical venue finality. El source actual ayuda como contraejemplo: `OrderSend/CTrade` precede a `g_Journal.Add`, dejando la crash window que M2 debe eliminar.
- Mantener KISS sin degradar correctness: cinco estados semánticos de submission journal bastan; el vendor status detallado queda como evidence/observation, no como FSM paralela.
