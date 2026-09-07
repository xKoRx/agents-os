---
type: feedback
scope: session
created: 2026-07-31
updated: 2026-07-31
area: "[[Echo]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge - Cierre de Etapa 4]]"
related:
  - "[[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]]"
  - "[[2026-07-31-minio-storage-path-must-be-deterministic-by-logical-identity]]"
aliases:
  - ef-g27-wrong-root-cause-feedback
agent: cursor
session_goal: reevaluar RCA del agente auditor y fix definitivo
source_session: cursor-2026-07-31-trade-list-path-rollback
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/echo-forge
  - agent/system1
---

# Session Feedback - 2026-07-31 - echo-forge-wrong-rca-from-auditor

## Context

- Agent: Cursor (agente principal) evaluando output de un agente auditor previo.
- Session goal: reevaluar RCA entregada y aplicar fix real al bug que bloquea Etapa 4.
- Main entity: [[Echo Forge - Cierre de Etapa 4]]
- Skills used: agents-os-session-close, graphify (query/explain), go-static-validation.
- Retrieval mode: evidencia del auditor + código Symphony.

## What Complicated The Session Most

- Observation: el agente auditor entregó una RCA convincente pero **incorrecta**
  (apuntaba al plugin Java como raíz); su evidencia era extensa y bien estructurada,
  lo que hacía difícil cuestionarla sin re-trazar todo.
- Why it was hard: la RCA previa "encajaba" con el síntoma visible (el plugin
  reportaba `source_order_count=0`) y proponía fixes plausibles downstream.
- Proposed improvement: las RCAs de agentes auditores deben exigir un
  **contraste contra la traza de correcciones previas** antes de aceptarse
  como raíz. Si el bug mutó en N releases, casi siempre la causa está upstream
  de todos los parches intentados.

## Most Useful Part Of Sistema 1

- What helped: el known-error previo ([[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]])
  estaba indexado, lo que permitió comparar "causa vieja" vs "causa nueva" en
  una sola pasada.
- Keep/change: keep. Promover el patrón "reescribe la causa raíz cuando se
  invalida, no crees un known-error paralelo".

## Pain Pattern Candidate

- Agentes auditores confunden "evidencia abundante" con "causa raíz
  identificada". Especialmente peligroso cuando el síntoma es real (el plugin
  sí reportó `source_order_count=0`) pero la causa está más arriba en el stack.
