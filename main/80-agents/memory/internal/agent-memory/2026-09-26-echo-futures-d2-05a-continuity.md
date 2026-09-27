---
type: agent_memory
schema_version: 1
scope: "project"
created: "2026-09-26"
updated: "2026-09-26"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities: ["[[Echo Futures]]"]
related: ["[[Echo Futures — D2-05A Instrument Contract]]", "[[Echo Futures — D2-04 Operation Order Fill Position]]"]
aliases: []
confidence: "high"
memory_state: active
continuity_key: "echo-futures/d2-05a-top"
load_policy: "when_project_loaded"
indexable: false
index_priority: "high"
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/echo
---

# Echo Futures — Continuidad D2-05A (TOP worker Instrument/Contract)

## Continuidad

- D2-05A re-derivado por TOP worker independiente (no SUBMANAGER): artefacto `10-projects/Echo Futures/Echo Futures — D2-05A Instrument Contract.md` committeado en vault `68b8e0951deecbb1efdeb47588ef340d368897ba`, estado `READY_FOR_SUBMANAGER_REVIEW`.
- Los 4 drafts self-authored previos (D2-05A/B/C e integrado D2-05) siguen física pero invalidados (bloque NON-AUTHORITATIVE); sus conclusiones no son input. El bloque `D2-05 = READY_FOR_MANAGER_REVIEW` dentro de [[Echo Futures]] sigue mostrando estado contaminado — corregir es del SUBMANAGER al integrar, no del TOP.
- Núcleo del diseño: Instrument (root económico: id+quote_currency+calendar_ref) / Contract (expiry-specific: contract_id, year+month, tick_size, point_value, tick_value derivado, qty_min/step, exchange, active; sin lifecycle timestamps en V1). External identifiers por `(source, context)` con unicidad inversa; mapping hot por `(instrument_id, context)` MARKET_DATA|EXECUTION; resolución única en `echo/operation` al materializar (guard D2-04) + specs embebidas en snapshot; rollover owner-manual estrictamente prospectivo; mono-contract por Operation; fail-closed en toda resolución faltante (`CONTRACT_RESOLUTION_FAILED`, sin fallback).
- Baseline verificada: `xKoRx/echo origin/master = 372af59a` (sin delta; fetch re-hecho). Owner decisions del TOP: NONE. Deuda declarada: conversión FX para MM en cuentas no-USD (seam), resolución histórica por fecha para backtester (lifecycle timestamps), unificación mapping Forex (DT-EF-CROSS-MARKET-INSTRUMENT-02).

## Señales de carga

- Cargar sólo con [[Echo Futures]] activo (D2-05 en curso). Autoridades del diseño viven en el artefacto D2-05A y en D2-04; esta nota es sólo continuidad de proceso.

## Próxima acción

- SUBMANAGER: re-derivar D2-05B/D2-05C con TOP workers y luego integrar D2-05 respetando los seams §10 del artefacto (calendar_ref nominal hacia B; `source` de identifiers ≠ Provider identity hacia C). Primary Manager review después; no cerrar D2-05 desde este carril.
