---
type: feedback
schema_version: 1
scope: session
created: "2026-09-28"
updated: "2026-09-28"
area: "[[Echo]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures — D2-07 Execution Runtime]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
session_goal: "D2-07 SUBMANAGER Integration Worker / A+B+C -> integrated candidate authority"
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

# Session Feedback — 2026-09-28 — Echo Futures D2-07 Integration

## Context

- One-shot SUBMANAGER INTEGRATION WORKER bajo D2: integrar children D2-07A/B/C (ya `ACCEPTED_FOR_INTEGRATION`) en la autoridad candidata única [[Echo Futures — D2-07 Execution Runtime]] + handoff en [[Echo Futures]].
- Baselines verificados: Agents-OS `b45e9328c0217e77c4f91103bb5f3a422d9cd5b6` (HEAD real); Echo `372af59a` declarada verificada por los children sin delta (regla de integración: no re-auditar salvo contradicción — no surgió ninguna).
- Trabajo documental puro: 6 autoridades leídas completas, 1 artifact nuevo, 1 sección de handoff, continuidad + feedback. Sin implementación, sin infra, sin agent_run.

## Friction / Pain Pattern Candidate

- **Confirmación de patrón (2.ª ocurrencia consecutiva; ver feedback D2-07C 2026-09-27):** [[Echo Futures]] volvió a superar el techo de una pasada de lectura (~42k tokens; el Read truncó a 950/1745 líneas y exigió segunda lectura) y creció otra vez con el handoff D2-07. La nota planificadora acumula cada gate/review/handoff D2 y cada worker D2 debe leerla completa. **Candidate reiterado:** al integrar D2, mover el historial de reviews/gates ya congelados a un log complementario (o confiar en los artifacts de cada workstream) y dejar en la nota planificadora sólo decisiones owner vigentes + estado del gate activo.
- Ninguna otra fricción: bootstrap, carga de autoridades por lista del mandato, edición y persistencia funcionaron sin degradación; sin fallbacks ni reintentos.

## What Complicated The Session Most

- Mantener el scope de integración honesto: la tentación natural era "mejorar" el contrato de los children durante la integración; el mandato exige congelar A/B/C tal cual y registrar alineaciones como notas de integración (journal-per-binding, observation-status vs aggregate-status) sin convertirlas en re-aperturas.
- Registrar D2-07-R1 sin tocar D2-04: la contradicción de wording (§2.3 permisivo) se documenta y exporta al Primary Manager, no se corrige en el documento padre desde un worker hijo.
