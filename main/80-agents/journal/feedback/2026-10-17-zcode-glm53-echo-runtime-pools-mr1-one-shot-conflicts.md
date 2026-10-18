---
type: feedback
schema_version: 1
scope: session
created: 2026-10-18
updated: 2026-10-18
area: "[[Echo]]" "[[Personal]]"
project: "[[Echo Futures — Runtime Pools]]" "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-agent-project-workflow]]"
  - "[[2026-10-17-zcode-glm53-echo-runtime-pools-mr1-repair]]"
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run:
session_goal:
source_session:
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


# Feedback — mandatos one-shot sin autoridad de adjudicación de conflictos

## Observación

En MR1, los mandatos one-shot con allowlist de archivos estricta produjeron dos fricciones recurrentes: (1) MR-A se encontró un conflicto real mandato-vs-código (la política TGMM congelada exigía un campo que el allowlist no cubría) y quedó bloqueado intentando preguntar (AskUserQuestion sin usuario disponible) — acabó decidiendo "por mejor juicio" y declarando PLAN_CONFLICT a posteriori; (2) la misma estructura obligó a retornos acotados adicionales (MR-B-R1 serving faltante, MR-C-R1 regresión H1, MR-B-R2 código muerto) que el diseño de un solo pase no contemplaba.

## Por qué importa

Un mandato que dice "otro archivo ⇒ STOP + PLAN_CONFLICT" sin declarar QUIÉN resuelve el conflicto y con qué autoridad deja al worker sin camino legítimo en un entorno no interactivo: o se detiene (pérdida de un pase completo) o desvía sin autoridad (riesgo de sobre-alcance). En S02/MR1 la práctica que funcionó fue: el worker declara la desviación con evidencia y el submanager la ratifica o revierte antes de integrar.

## Sugerencia

En la plantilla de mandato one-shot (skill technical-project-manager §"Build the one-shot master mandate", y el patrón del proyecto Echo Futures), añadir una sección explícita `/conflicts`: el worker clasifica el conflicto (wiring mínimo vs rediseño vs contrato congelado), aplica el wiring mínimo con evidencia cuando sea reversible y trazable, y reporta la desviación como campo obligatorio del handoff; el submanager ratifica/revierte antes de integrar. Dejar de depender de AskUserQuestion en contextos desatendidos.

## Evidencia

- MR-A handoff: PLAN_CONFLICT declarado con 6 desviaciones, todas ratificadas por el submanager (registro en el planner).
- MR-E detectó la regresión H1 (el oráculo existente sí la cazó — la defensa funcionó) y MR-C-R1 la cerró en el mismo encargo.
- Registro completo: [[Echo Futures — Runtime Pools]], sección «Registro MR1».
