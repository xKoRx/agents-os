---
type: feedback
schema_version: 1
scope: session
created: 2026-10-06
updated: 2026-10-06
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[BTG-S03-IMPLEMENTATION]]"
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

# Session Feedback - 2026-10-06 - Echo Futures BTG-S03

## Context

- Superficie: ZCode LOCAL (GLM); mandato Owner TOP implementation lead ONE-SHOT. Un especialista Explore read-only y resto ejecutado por el lead.
- Objetivo: [[BTG-S03-IMPLEMENTATION]] — motor fiel, Strategy/MM intercambiables, BASIC+CAMPAIGN reales, candidato S04.

## Scores

Escala 1–5 sobre esta sesión, no sobre la corrección del producto: startup 4; utilidad retrieval 4; ajuste skills 4; template 3; facilidad de cierre 3; confianza documental 4.

## What Complicated The Session Most

- El timeout por defecto de 10m de `go test` abortó la suite completa del backtester (test lento a52); se re-ran con `-timeout 40m`. Fricción menor, workaround trivial.
- La herramienta de tareas de fondo del harness limita cada espera a 10 minutos: las corridas largas (7–9 min por run) exigieron esperas encadenadas; sin pérdida de datos.
- `SpoolDir` genera un attempt-dir aleatorio por llamada: el hook de cierre de campaña debe capturar el path en el primer uso (bug corrijo, costo bajo).

## What Helped

- Reutilizar el workspace S01 (spec preparado, source-derived, input JSON) hizo las corridas reales directas; el golden byte-idéntico sirvió de regresión fuerte del refactor de readiness.
