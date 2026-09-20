---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
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

# 2026-09-20-f05c-cert-f04-01-rerun5-blocked

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-19/20 — Ejecución CERT-F04-01 RERUN-5 (0.2.102, defecto #5 en read-back SQX del seal)` con veredicto `BLOCKED` + actualización de `Estado de entrada` + actualización de `Próxima tarea única recomendada para NORMAL`; CERT-F04-01 pasa a `BLOCKED` por quinto defecto determinístico)
  - `10-projects/Echo Forge/Echo Forge.md` (entrada de bitácora 2026-09-20)
  - `80-agents/journal/agent-runs/2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-01-rerun5-blocked.md` (creado)
  - Flota/repositorio — campaña real `c42dd637…` sobre release `0.2.102` (allocations `26090011010–012` por Apply y artifacts durables en `sqx-strategies`; efectos documentados aquí, sin cambios de código)

## Motivo

- Ejecución del mandato `CERT-F04-01 RERUN-5` (único gate restante tras C10): re-run físico desde cero sobre `0.2.102`/`66faa42…` con identidades todas nuevas, observando la cadena hasta sellado/entrega o primer fallo causal.

## Contenido

- **G0 PASS:** `release-authority` `0.2.102 CONSISTENT/EXACT_MATCH` (6/6 objetos); flota 4/4 (Zeus 2801657, Hera 1390690, Kronos 1353062, Windows 6648) con SHA instalado == artifact; evidence Windows fresca `partial=false errors=[]` singleton + `MT5_PROCS=0`; `sqx-prop` Running=0.
- **G1 PASS:** request_id `cert-f04-01-rerun5-20260919T211749Z-f69f9f3b` (preimage `c62e0d92…`, 5611 B); diff semántico exacto de 4 paths identidad sobre la receta congelada RERUN-4; VALIDATION_OK contra structs `66faa42` con negativos 3/3 RECHAZADOS; CFX byte-exactos.
- **G2 PASS:** dispatch único 21:23:05Z (watcher 0.2.102 en Zeus, input pre-stageado, pipeline 6/6); CampaignRef `c42dd637-3f5a-4702-b9ff-361acededba0`, FlowRunRef `fbac1286-23a9-4ecb-b483-d31250dc612a`; sin duplicados.
- **G3 PASS:** cohorte honesta de 3 miembros (3da55fda, 847a417b, 8b403f34); 3 compiles físicos Windows SUCCESS + `mt5_compile_persist_v1` ×3; 3 backtests físicos secuenciales COMPLETED (~67/70/54 min) con `LIVE_PHYSICAL_MT5_EXECUTIONS<=1` demostrado en 4 muestras vivas.
- **G4 PASS ×3:** HTM byte-verificados contra durable (6336204 B `19255be8…`; 13966272 B `46a34b31…`; 18424420 B `4ba40a75…`); parser `mt5-report.v1` 6182 con 7/7 crosschecks PASS ×3; `mt5_reconcile_v1` ×3 `structural_identity: MATCH`.
- **G5 PASS:** promote_finalists COMPLETED; DecisionRef `sha256:de5e7acc…`; finalists_v2 ×3 (rank1 847a417b) con warnings `PNL_SIGN_FLIP`.
- **G6 FAIL → defecto #5:** `forge_seal_handoff_v1` CONTRACT_CONFLICT `sqx readback: sqx xml parse: XML syntax error on line 3: illegal character code U+0003` (evento 492, 2026-09-20T00:49:08Z). El fix C9/C9R quedó validado en producción (request con `ApplyEvaluationRef != CompileEvaluationRef` ×3, consumer validó stages/contratos); el fallo es el read-back de magic: `magicreadback.FromSQX` (`sqx/adapters/magic-readback/readback.go:51`) parsea como XML plano un artefacto que el producer Apply emite como contenedor ZIP (`strategy.sqx` 4506976 B `9ac377b9…` byte-verificado; `strategy_Portfolio.xml` interno contiene `<value>26090011010</value>`); repro exacto del error contra el módulo real @ `66faa42`.
- **G7 NO ALCANZADA:** sin seal no hay manifests ni entregas (0 POST; contrato F-04 §11: sin ingest configurado el estado terminal habría sido `HANDOFF_CREATED`).
- **G8/G9:** efectos parciales inventariados — `strategy_versions []` y `handoffs []` ×3 (seal fail-closed sin writes); allocations `26090011010–012` por Apply (write-once, el seal sólo replay-ea); campaña/FlowRun FAILED terminal; `MT5_PROCS=0` final; flota sigue 0.2.102. **`CERT-F04-01 = BLOCKED`**; no se creó RERUN-6.

## Impacto

- Sin cambios de código, SPEC ni releases. Serie de defectos determinísticos demostrados físicamente: #1 deadline, #2 encoding, #3 build 6182, #4 Apply authority (corregido y validado en este run), #5 contenedor SQX vs parser XML — todos con cadena física verde hasta el punto de fallo. Siguiente decisión: manager (fix read-back SQX → release → RERUN-6).
