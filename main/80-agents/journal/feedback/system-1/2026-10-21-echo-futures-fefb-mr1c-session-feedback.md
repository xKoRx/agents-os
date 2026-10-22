---
type: session_feedback
schema_version: 1
scope: project
created: "2026-10-21"
updated: "2026-10-21"
area: "[[Echo]]"
project: "[[Echo Futures — Execution Client y Feed Batching]]"
entities:
  - "[[Echo Futures — Execution Client y Feed Batching]]"
related: []
aliases: []
confidence: verified
load_policy: manual
indexable: true
index_priority: low
tags:
  - kind/session-feedback
  - area/echo
---

# Feedback — FEFB S01 MR1c (wiring bars.origin; worker muerto por inactividad)

- **Pain pattern candidate (worker ONE-SHOT muerto por inactividad del harness, no por fallo de trabajo):** el especialista B fue terminado por el timeout de inactividad de ZCode (600s) mientras una suite larga (futuresvertical ~15min) corría sin emitir salida — el trabajo durable quedó completo en el worktree (código+tests+evidencia roja/verde) pero sin commit ni reporte. El submanager recuperó verificando el estado git durable y ejecutando él mismo la aceptación, en vez de re-despachar (que habría duplicado/contradicho). En briefs de workers con suites >9min: exigir lanzar en background (`nohup`+sondeo con salidas intermedias) o partir en tramos; y ante "subagent inactive", leer el worktree ANTES de reintentar.
- **Transferible:** `go tool cover -func` sobre el perfil dedicado da cobertura por función del código nuevo al instante; el agregado manual por bloques (suma de hitCount) es incorrecto y sobreestima caídas.
