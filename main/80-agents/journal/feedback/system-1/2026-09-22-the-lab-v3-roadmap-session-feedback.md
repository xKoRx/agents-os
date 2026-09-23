---
type: feedback
schema_version: 1
scope: session
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Echo]]"
project: "[[Echo — Producto Integrado]]"
entities:
  - "[[Echo — Producto Integrado]]"
related:
  - "[[D — Revised Roadmap]]"
  - "[[2026-09-22-the-lab-v3-roadmap-closure]]"
agent_surface: "[[ChatGPT]]"
agent_model: GPT-5.6 Sol
session_goal: "Ratify The Lab V3 simplified architecture and create 5-day executable roadmap"
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags: [kind/feedback, scope/session, project/agents-os, agent/system1]
---
# Session feedback — The Lab V3 roadmap / 2026-09-22

## What worked
Product owner clarification resolved the earlier open-vs-close contradiction; retained proven S0/worker foundations selectively without forcing legacy architecture; focused GitHub review prevented another MCP/history rabbit hole. Comprehensive roadmap separates day-by-day product acceptance from longer-term money management, portfolio and debt elimination; source hashes and availability are not mistaken for E2E certification.

## Friction and failure mode
Previous proposals overmodeled the user need (`TradeSet`, `HistoryRevision`, `HistoryPublication`) and defended Lab legacy beyond its value. Legacy `recompute` is destructive toward Lab tables and `canonical_a0` mislabels Reference as SQX BACKTEST: never transplant as V3. Work is dependent on authentic SQX+MT5 per-trade lists not yet proven. Daily plans must not repeat a global audit or burn quota on MCP repair.

## Improvement
One authoritative active analytic operation base in PG; avoid dual write-masters with E05 until consumer map resolved. Date partition at OPEN, plots at CLOSE. Keep operational journal untouched; V3 lab job only reads. Before claiming daily PASS require concrete DEV provenance/count/digest, UI and negative tests. Legacy retirement should be explicit with measured zero references and a bounded post-V3 cleanup stage; never delete unrelated trading data. At end of day close session with next action, evidence and blockers rather than new master prompts.
