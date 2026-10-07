---
type: feedback
schema_version: 1
scope: session
created: 2026-10-07
updated: 2026-10-07
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[BTG-S03-REMEDIATION]]"
aliases: []
agent_model: GLM (ZCode; host no expone identificador exacto)
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/echo-futures
  - agent/system1
---

# Session Feedback - 2026-10-07 - Echo Futures BTG-S03 remediation

## Context

- Superficie: ZCode LOCAL (GLM); devolución correctiva ONE-SHOT R1–R5 sin subagentes de código.

## Scores

Startup 4; utilidad retrieval 4; ajuste skills 4; template 3; facilidad de cierre 3; confianza documental 4.

## What Complicated The Session Most

- El costo de cómputo del modelo V2 por paso (~140x V1) obligó a re-bordear las corridas dos veces antes de implementar el inert-skip del diseño; la lección es medir el gate T37 ANTES de lanzar la ventana larga.
- go test timeout por defecto (10m) aborta la suite del backtester; usar -timeout explícito.
- Un refactor por parches sucesivos enredó compose_account.go y costó una reescritura completa; cambios estructurales grandes conviene hacerlos como reescritura de archivo desde el inicio.
