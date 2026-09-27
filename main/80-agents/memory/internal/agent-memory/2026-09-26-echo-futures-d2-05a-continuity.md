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

- D2-05A re-derivado por TOP worker independiente (no SUBMANAGER): artefacto `10-projects/Echo Futures/Echo Futures — D2-05A Instrument Contract.md`; v1 @ vault `68b8e095`, **repair A-R1 dirigido por SUBMANAGER aplicado @ `5459acd0bd8c944c564e52ba5dc8852cd07d238a`**, estado `READY_FOR_SUBMANAGER_REREVIEW`.
- Repair A-R1 (qué cambió): mapping pasa de unicidad `(instrument_id, context)` a identidad `(mapping_context, binding_id, instrument_id)` — varios bindings de feed y varios execution bindings coexisten con Contract corriente propio; cadenas congeladas market: `Instrument+binding→Contract→identifier(source)` y materialización: `Instrument+Account.execution_binding_id→Contract(pin)` + identifier aparte. Seam A↔B↔C cerrado: `exchange` + `product_group` migran a Instrument como única autoridad (Contract pierde `exchange` propio); B keyea `(calendar_ref, exchange, product_group)`, C keyea `(instrument_id, exchange, product_group)`; full-vs-micro NO es campo de dominio (config RuleSet). Casos nuevos A-R1-1..4 en el artefacto.
- Los 4 drafts self-authored previos (D2-05A/B/C e integrado D2-05) siguen física pero invalidados (bloque NON-AUTHORITATIVE); sus conclusiones no son input. El bloque `D2-05 = READY_FOR_MANAGER_REVIEW` dentro de [[Echo Futures]] sigue mostrando estado contaminado — corregir es del SUBMANAGER al integrar, no del TOP.
- Núcleo vigente: Instrument (id + quote_currency + calendar_ref + exchange + product_group) / Contract (expiry-specific; tick_value derivado; sin lifecycle timestamps V1); identifiers por `(source, context)`; resolución única en `echo/operation`; rollover prospectivo; mono-contract; fail-closed sin fallback (`CONTRACT_RESOLUTION_FAILED`).
- Baseline verificada: `xKoRx/echo origin/master = 372af59a` (sin delta). Owner decisions: NONE. Deuda: conversión FX para MM no-USD (seam), resolución histórica por fecha para backtester.

## Señales de carga

- Cargar sólo con [[Echo Futures]] activo (D2-05 en curso). Autoridades del diseño viven en el artefacto D2-05A y en D2-04; esta nota es sólo continuidad de proceso.

## Próxima acción

- SUBMANAGER: re-derivar D2-05B/D2-05C con TOP workers y luego integrar D2-05 respetando los seams §10 del artefacto (calendar_ref nominal hacia B; `source` de identifiers ≠ Provider identity hacia C). Primary Manager review después; no cerrar D2-05 desde este carril.
