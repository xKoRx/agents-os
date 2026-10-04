---
type: change_log
schema_version: 1
scope: session
created: "2026-10-03"
updated: "2026-10-03"
area:
project:
application:
entities: []
related:
  - "[[technical-project-manager]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Technical Project Manager — OpenAI Pro quota tracker

## Cambio

- **Tipo:** updated / created
- **Archivo(s):**
  - `30-resources/agents/skills/technical-project-manager/SKILL.md`
  - `80-agents/memory/public/openai-pro-chat-quota.md`

## Motivo

- Incorporar un contador canónico del pool semanal de ChatGPT Pro usado por CLOUD GOD/otros modos Pro-pool.
- Hacer a Manager/SUBMANAGER responsables de reconciliar cada consumo confirmado.
- Mantener UNKNOWN/PARTIAL hasta disponer de una frontera real de reset, sin inventar mensajes restantes.

## Fuentes usadas

- Decisión explícita del Owner, 2026-10-03.
- OpenAI Help — GPT-5.6 and GPT-6 Pro in ChatGPT: Pro $100 comparte 50 mensajes/semana entre GPT-6 Pro y GPT-5.6 Sol Pro; Work/Codex tienen allowances separados.
- `80-agents/skills/agents-os-skill-authoring/SKILL.md`.
- `80-agents/skills/_shared/schema-contract.md`.

## Resolución aplicada

- Estado canónico: `80-agents/memory/public/openai-pro-chat-quota.md`.
- Cada worker que consume el pool retorna `PRO_CHAT_POOL_DELTA: n`.
- El Manager/SUBMANAGER dueño del dispatch reconcilia el delta antes del siguiente uso Pro-pool.
- Coordinadores CLOUD que usan Pro cuentan cada respuesta; si no pueden persistir, mantienen `PRO_CHAT_POOL_PENDING_DELTA` hasta reconciliación.
- El contador inicia `PARTIAL` porque el consumo anterior a 2026-10-03 no es observable.
- Tras el primer reset confirmado pasa a `EXACT` si no se pierden receipts.

## Validación

- Skill referencia explícitamente el archivo de quota en Minimal Read.
- Skill define accounting, receipt, conflict handling y reset evidence-driven.
- Agent-memory usa schema v1, scope global, continuity_key único y secciones requeridas.
- Estado inicial no afirma remaining exacto.
- Commits:
  - skill: `627a448a48681e6b3c679978f7be3b2310d4a3fa`
  - quota tracker: `5bf194468e35cc37f5b328cae79b21a607abfe83`

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni paths de máquina.

## Rollback

- Revertir los dos commits anteriores y retirar la referencia de Minimal Read si el tracking se reemplaza por telemetría nativa de ChatGPT.
