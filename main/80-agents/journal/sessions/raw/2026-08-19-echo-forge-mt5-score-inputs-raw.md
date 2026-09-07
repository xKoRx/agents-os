---
type: raw_session
schema_version: 1
scope: session
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
related:
  - "[[2026-08-19-1010-cursor-grok-4.6-echo-forge-mt5-score-inputs]]"
  - "[[2026-08-19-echo-forge-mt5-score-inputs-config-driven]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

# echo-forge-mt5-score-inputs-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: [[Cursor]] / Cursor Grok 4.6
- Proyecto o entidad: [[Echo Forge - Reconciliación y Scoring MT5]]
- Objetivo de la sesión: corregir resolución implícita del Score baseline; inputs config-driven.

## Transcript

No se pega el transcript completo (cadena de herramientas). Resumen durable:

- Problema: `FindTradeListExporter` tomaba el primer exporter; `FindProjectTaskByFolder` se quedaba con el último match.
- Decisión: `scores[].inputs[]` con `role`/`task`/`metric_set`; identidad = `TaskSpec.Name`; folders solo routing.
- Entrega: `eba11f0` en `master`. Tests/vet/race PASS en packages afectados.
- Gate: M6-NORMAL/M6-TOP/M6 CLOSED; M7 BLOCKED.
