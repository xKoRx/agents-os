---
type: session_feedback
schema_version: 1
scope: session
created: "2026-10-16"
updated: "2026-10-16"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities: []
related:
  - "[[TRADESGERARD-CONSOLIDATION]]"
aliases: []
source_session: "sess_6c1f4cfa-01c8-424a-bbb1-0540e9d3b818"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
---

# Session Feedback — 2026-10-16-echo-c1c4-closure

## Pain Pattern Candidate

- **Master publicado con tests rojos no contrastados:** `e0e67f8c` llevaba 2 fixtures de paridad rojos (config/functions) y 1 test de wiring dependiente del orden de un contador global; la afirmación «pruebas pequeñas verdes» no distinguió suites focalizadas de suite completa. Costó dos corridas completas (~13 min c/u) + stash/unstash para demostrar que el delta nuevo no introducía fallos. Sugerencia: registrar la lista de fallos conocidos por baseline en el control del proyecto antes de publicar.

## What Worked

- El contraste RED→GREEN por defecto (C1) y los contadores de preparación (C4/CLI) dieron evidencia directa sin campañas extra: presupuesto financiero 1/1 sin necesidad de reintento.

## Tooling Notes

- `go test ./backtester/` con timeout por defecto (10m) aborta por agotamiento; necesita `-timeout 30m` (quirk ya conocido del repo, confirmado de nuevo).
