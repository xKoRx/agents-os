---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-27"
updated: "2026-09-27"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures — D2-07C Execution Runtime Topology]]"
  - "[[Echo Futures — D2-07A Execution Adapter Contract]]"
  - "[[Echo Futures — D2-07B Transport Selection]]"
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-07c-worker"
load_policy: when_project_loaded
indexable: false
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/echo
---

# Echo Futures — Continuidad D2-07C

## Continuidad

- One-shot D2-07C completado: `READY_FOR_SUBMANAGER_REVIEW`. Artifact: [[Echo Futures — D2-07C Execution Runtime Topology]].
- Baselines contrastados: Agents-OS `9f3c950bd86e5a83f9af1fbeec841888c0898ebf`; Echo `origin/master = 372af59a7b83604781346613da01e3d510ea1360` (fetch, sin delta).
- BRIDGE DECISION congelada como candidate: `FUTURES_BRIDGE_SIBLING` — reutiliza patrones + `v3/sdk/*`, duplica piezas bridge-internal pequeñas, sin bridge-framework ni cuarto servicio. `v3/bridge` es Windows-only (`//go:build windows`) por Named Pipes; la carga decisiva fue OS/host: ProjectX exige order flow desde dispositivo personal del trader.
- Journal M2: write-ahead en el durability domain del side-effect owner (futures-bridge), store durable local detrás de interface, tecnología = D6; prohibido Core PG y Kafka como journal primario. PK conceptual D2-07A `(execution_account_id, client_order_id)` intacta; pin de transporte dentro del record; durabilities coexisten por binding (hot rebind prospectivo, Orders vivas pinneadas).
- Side-effect authority: una por `(account, physical binding)`; V1 = NO AUTOMATIC CROSS-HOST TAKEOVER; Kafka consumer ownership NO es fencing (detección por session generation + telemetría doble-owner, no kill físico).
- Routing: familia nueva `echo.order-commands.{execution_account_id}.v1` reutilizando convención per-account legada (`mm_engine.go:586`/`close_handler.go:369`); retorno por cinco familias D2-07A hacia `echo.execution-events.v1` key op key; DTOs legacy no promovidos.
- Ventana M2 legado confirmada físicamente en baseline: MT5 `FindByCommandId` antes de `g_Trade.Buy/Sell` (1764–1815) y `g_Journal.Add` después (1841/1863); MT4 `OrderSend` 1961 → `Add` 1975/2005. No se arregló el legado (fuera de scope).
- Reconnect barrier D2-07A §17 completa antes de `EXECUTION_READY_NEW_RISK`; ForceClose con bridge down = pendiente + reconcile-first; SimExecutionAdapter ejercita journal/recovery real sin credenciales.
- No se abrió D2-07 integration ni D2-08. Siguiente paso: SUBMANAGER review de D2-07C (con D2-07A/D2-07B pendientes).

## Señales de carga

- Cargar cuando se revise D2-07C, se integre D2-07 o se prepare D4/D6 (host placement, store del journal, certificación M2).
