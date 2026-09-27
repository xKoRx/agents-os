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
  - "[[Echo Futures — D2-07A Execution Adapter Contract]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-06 Market Runtime]]"
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-07a-worker"
load_policy: when_project_loaded
indexable: false
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/echo
---

# Echo Futures — Continuidad D2-07A

## Continuidad

- One-shot D2-07A completado: `READY_FOR_SUBMANAGER_REVIEW`. Artifact: [[Echo Futures — D2-07A Execution Adapter Contract]].
- Echo baseline contrastado: `372af59a7b83604781346613da01e3d510ea1360`, sin delta material.
- Freeze central: M1 = StateFun/Kafka EXACTLY_ONCE; M2 = venue side-effect idempotency/reconciliation. No mezclar garantías.
- M2 candidate: durable write-ahead intent antes del point-of-no-return + stable `client_order_id` + native idempotency y/o authoritative lookup/history. Después de uncertainty, nunca blind retry.
- Journal mínimo: PREPARED / SUBMITTING / VENUE_BOUND / TERMINAL / AMBIGUOUS. Store/topology no decididos.
- Readiness: socket != execution-ready. NEW_RISK requiere static entitlement/capability + auth/binding + event stream + reconciliation authority + fresh position + cero ambiguity.
- Finality: cancel/modify request ACK no es execution finality; late fills se preservan; reservations/Operation terminality dependen de venue evidence.
- Fill: provider execution identity estable requerida; este worker aplica la regla estricta de no inventar dedup identity. Contradicción con wording D2-04 §2.3 exportada al SUBMANAGER.
- Echo V3 debt material: MT4/MT5 persisten command journal después de `OrderSend/CTrade`, por lo que crash post-side-effect/pre-journal puede duplicar ejecución. No reusable como M2.
- D2-07B debe probar claim-level first-party: client-order round-trip, authoritative negative lookup, native idempotency scope/retention, execution history/cursor, stable execution id, terminal history/finality, snapshot completeness y direct entitlement.
- D2-07C constraints: single side-effect authority, durable shared journal for any takeover, session generation/fencing semantics, original binding pinned for live Orders, reconnect barrier before new risk.
- No iniciar D2-07B/D2-07C/D2-08 desde este worker. Siguiente paso: SUBMANAGER review only.

## Señales de carga

- Cargar cuando se revise D2-07A, se integre D2-07 o se prepare D2-07B/D2-07C.
