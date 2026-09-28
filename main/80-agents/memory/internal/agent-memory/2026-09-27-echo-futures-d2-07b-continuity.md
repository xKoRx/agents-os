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
  - "[[Echo Futures — D2-07B Transport Selection]]"
  - "[[Echo Futures — D2-07A Execution Adapter Contract]]"
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-07b-worker"
load_policy: when_project_loaded
indexable: false
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/echo
---

# Echo Futures — Continuidad D2-07B

## Continuidad

- D2-07B-R1 corrigió exclusivamente el scope/conclusión de [[Echo Futures — D2-07B Transport Selection]]; status vigente: `READY_FOR_SUBMANAGER_REVIEW`.
- Desvío reparado: `transport certification accidentally promoted from D6 gate to D2 blocker`. D2-07A permanece ACCEPTED y estricto; M1/M2, durable intent, stable client identity, no blind retry, reconciliation, AMBIGUOUS fail-closed y exact Fill identity no se rebajaron.
- `PROJECTX_DIRECT = RECOMMENDED_INITIAL_NON_REAL_MONEY_CANDIDATE`. Es recommendation only; `M2_VENDOR_CERTIFICATION = DEFERRED_TO_D6`, `REAL_MONEY_CERTIFICATION = NOT_DONE`, `OD-D2-07-1 = PROJECTX_DIRECT — CANDIDATE ONLY`.
- ProjectX conserva cinco gates D6: customTag retention, ambiguous-submit retry atomicity, authoritative negative/recovery semantics, Trade id scope/stability e history horizon.
- NinjaTrader Desktop genérico = `NOT_RECOMMENDED_AS_FIRST_GENERIC_V1_PATH`; Tradovate, Rithmic y CQG = `FUTURE_ADAPTER_CANDIDATE` con transport-specific certification si se seleccionan.
- `D2-07C = UNBLOCKED`, pero este worker NO lo abrió. D2-08 tampoco fue iniciado. Transport selection debe permanecer detrás del Bridge/Adapter boundary.
- Próximo paso: SUBMANAGER review de D2-07B-R1 y decisión owner/manager sobre `OD-D2-07-1`; la implementación/certificación física del transport seleccionado pertenece a D6.

## Señales de carga

- Cargar cuando se revise D2-07B, se intente cerrar ProjectX M2 o se integre D2-07.

## Próxima acción

- SUBMANAGER revisa [[Echo Futures — D2-07B Transport Selection]]. Si acepta el repair, puede continuar a D2-07C sin ejecutar certificación ProjectX M2 en D2; los gates físicos quedan reservados para D6.
