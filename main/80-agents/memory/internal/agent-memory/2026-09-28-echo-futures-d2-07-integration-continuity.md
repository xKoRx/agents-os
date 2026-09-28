---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-28"
updated: "2026-09-28"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures — D2-07 Execution Runtime]]"
  - "[[Echo Futures — D2-07A Execution Adapter Contract]]"
  - "[[Echo Futures — D2-07B Transport Selection]]"
  - "[[Echo Futures — D2-07C Execution Runtime Topology]]"
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-07-integration-worker"
load_policy: when_project_loaded
indexable: false
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/echo
---

# Echo Futures — Continuidad D2-07 Integration / Repair R1

## Continuidad

- Estado vigente: `D2-07-R1 = READY_FOR_MANAGER_REVIEW`. Integración A+B+C (`READY_FOR_MANAGER_REVIEW` inicial) recibió Primary Manager verdict **CORRECTION REQUIRED** por un único defecto; Architecture Repair Worker ONE-SHOT lo corrigió en [[Echo Futures — D2-07 Execution Runtime]] (§1/§4/§6/§8/§17/Fuentes/Handoff). Children A/B/C (`ACCEPTED_FOR_INTEGRATION`) siguen como evidence/design depth. Handoff agregado a [[Echo Futures]] (sección D2-07-R1).
- **Defecto registrado:** integrated event routing incorrectly promoted non-Operation observations into op-key execution stream — el wording integrado enviaba las cinco familias a `echo.execution-events.v1` key op key → `echo/operation`; `PositionObservation` no porta `operation_id` (es física account+contract) y `ExecutionSessionObservation` es runtime/readiness, no evento del aggregate.
- **Repair congelado (routing de tres caminos, §8/§17):** op-correlated `OrderObservation`/`OrderActionObservation`/`Fill` de Order Echo → `echo.execution-events.v1` (key op key) → `echo/operation`; `PositionObservation` → `echo.position-observations.v1` → physical position/reconciliation (no entra a `echo/operation`, no genera Fill por delta, no fabrica Operation); `ExecutionSessionObservation` → runtime/readiness path account-scoped (naming topic = IMPLEMENTATION DETAIL/D6; jamás `operation_id` fabricado, jamás fact de Operation). Manual/unknown: observación física + reconciliation debt; canonical correlated facts sólo tras correlación demostrada (§14). ARCHITECTURE CHANGES: NONE beyond event-routing clarification.
- Traceability SHA — conceptos distintos, no reemplazables: INTEGRATION BASELINE `b45e9328c0217e77c4f91103bb5f3a422d9cd5b6` (HEAD al inicio del integration worker; el handoff anterior lo reportó como "AGENTS-OS SHA" ambiguo) ≠ persistencia integración `363849568383bda8dddbe9fb6ded447e15590210` ≠ cierre de esa sesión `89120c64cd59719949a7af495b0a75355e18d686` ≠ FINAL AGENTS-OS SHA (HEAD persistido tras el repair, ver handoff de sesión D2-07-R1). Echo `372af59a` sin delta.
- Baselines/decisiones sin cambio: Echo `xKoRx/echo@372af59a` verificada por los children; `FUTURES_BRIDGE_SIBLING` (no depende de ProjectX); journal M2 write-ahead en el side-effect owner, store `DEFERRED_TO_D6`, Core PG/Kafka prohibidos como journal primario; M1/M2 separados; single side-effect authority por `(account, physical binding)`, V1 NO AUTOMATIC CROSS-HOST TAKEOVER; account-isolated command routing con `echo.order-commands.{execution_account_id}.v1` como IMPLEMENTATION CANDIDATE; barrier reconnect antes de `EXECUTION_READY_NEW_RISK`; hot binding pinning; degraded close; SimExecution separation; acceptance A–L intactos.
- Alineaciones de la integración (notas, no defectos) siguen vigentes: (1) identidad física del journal M2 por binding sobre la PK de dedup `(execution_account_id, client_order_id)` de A; (2) `PARTIALLY_FILLED` es status de `OrderObservation` (venue), no del aggregate Order (D2-04 §3.2: partial = WORKING + filled_qty).
- D2-07-R1 (identidad de ejecución) intacta: no heuristic/synthetic execution identity; D2-04 §2.3 NO modificado — aclaración exportada al Primary Manager antes del freeze global de D2.
- Transport: `PROJECTX_DIRECT` = recommended initial non-real-money implementation candidate (recommendation only; M2 NOT_PROVEN con 5 gates D6); NinjaTrader Desktop NOT_RECOMMENDED as first path; Tradovate/Rithmic/CQG certify-if-selected.
- Owner decisions: `OD-D2-07-1 — INITIAL V1 EXECUTION TRANSPORT` sigue siendo la ÚNICA decisión owner pendiente de D2-07 (no bloquea manager review). Ratificación técnica ordinaria: naming físico final de topics (incluido el del session/readiness path, D6).
- No se implementó código, no se tocó Echo, no se cambió la arquitectura Bridge/Adapter, no se reabrieron A/B/C ni M1/M2, no se cerró OD-D2-07-1.
- Siguiente paso: Primary Manager review de [[Echo Futures — D2-07 Execution Runtime]] solamente. NO D2-08. NO cierre global D2.

## Señales de carga

- Cargar cuando se revise D2-07 (o su repair R1), se resuelva OD-D2-07-1, se prepare D4 (SPEC) o D6 (implementación/certificación: store journal, host placement, gates M2 vendor, naming del session/readiness path).
- Detalle completo de constraints/capabilities en los children: A (contrato), B (transports/evidencia), C (topología/reuse map). El routing de retorno vigente es el del artifact integrado §8/§17 (los children C §14 y el diagrama de C conservan wording histórico de un solo stream op-key; ante contradicción manda el artifact).
