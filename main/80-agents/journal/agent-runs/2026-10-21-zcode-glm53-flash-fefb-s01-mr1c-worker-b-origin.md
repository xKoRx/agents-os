---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-21"
updated: "2026-10-21"
area: "[[Echo]]"
project: "[[Echo Futures — Execution Client y Feed Batching]]"
application:
entities: []
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
model_source: host
task_type: coding
task_complexity: high
outcome: success
verification: tests
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# FEFB MR1c (B) — bars.origin plomeado de config efectiva a analytics

- **Objetivo:** reparar G1 BAR_ORIGIN_NOT_WIRED: el origen configurado (`feed.bars.origin` C3) decide la autoridad de barras por serie; eliminar la elección por arrival-order (FEFB §7).
- **Evidencia:** commit `d99e5108` (integrado por submanager tras revisión; worker murió por inactividad ZCode en suite larga dejando trabajo durable, ver [[worker-shared-worktree-untracked-files]] y bitácora) — ruta declarada `echo.futures.bars-origin.v1` (AMBOS module.yaml) → `market.BarsOriginUpdate` (validate fail-closed) → decode productivo del shell → `analytics.applyBarsOrigin` + ValueSpec durable `futures_ma_bars_origin` registrado en runtime (sobrevive restart/requisitos); NATIVE suprime agregación/cierres TRADE desde config (sin vela competidora, sin fallback por hueco, TRADE forward intacto); TRADE_AGGREGATED rechaza nativa inesperada (contador visible, serie sin mutar); hot-change rechazado explícito; legacy sin origen = byte-exacto (pin SHA-256 serialización certificada).
- **Reproductores:** 6 rojos sobre `82335b34` (scratch detached, vocabulario wire del baseline) → verdes en `d99e5108` + pin de paridad legacy; ruta REAL (raw JSON→decode productivo, sin asignación directa de InputMode).
- **Verificación:** comandos+exits en `mr1c-red/`, `mr1c-green/`; cobertura código nuevo B 100% por función; builds 4 módulos + race limpios; verificación independiente de C (agente hermano, run aparte).
