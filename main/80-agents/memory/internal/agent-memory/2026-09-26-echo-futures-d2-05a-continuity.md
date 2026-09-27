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

- D2-05A re-derivado por TOP worker independiente (no SUBMANAGER): artefacto `10-projects/Echo Futures/Echo Futures — D2-05A Instrument Contract.md`; v1 @ `68b8e095`, repair A-R1 @ `5459acd0`, **repair A-R2 (calendar seam reconciliation con B-R1) aplicado y en HEAD vía sync @ `1657b7b4`**, estado final `READY_FOR_INTEGRATION`.
- Repair A-R2 (qué cambió): `calendar_ref → ExchangeCalendar.calendar_id` es la ÚNICA referencia runtime para sesión (CalendarResolver consume `(calendar_id, instant)`; sin product_group ni exchange como parámetros; session_id sin product_group; overrides dentro del dataset fechado B-R1; product_group NO es identidad de calendario). `exchange` = metadata/rules/onboarding (C); `product_group` = única autoridad de grouping para C, independiente de session identity. Futures V1 fail-closed: calendar_ref DEBE resolver por Instrument habilitado ⇒ `CALENDAR_UNRESOLVED` bloquea operar (sin default 24x7); nullable sólo conceptual cross-market, no impuesto al legacy Forex/CFD. Caso consistencia A-R2-1 (NQ/MNQ comparten grupo+calendario; X con grupo NQ y CALENDAR_X no colisiona). Cleanup total del wording A-R1 sobre el resolver de B; sin `InstrumentCalendarMappingVersion`/`ProductGroupCalendarRule`/ontology.
- Repair A-R1 (qué cambió): mapping pasa de unicidad `(instrument_id, context)` a identidad `(mapping_context, binding_id, instrument_id)` — varios bindings de feed y varios execution bindings coexisten con Contract corriente propio; cadenas congeladas market: `Instrument+binding→Contract→identifier(source)` y materialización: `Instrument+Account.execution_binding_id→Contract(pin)` + identifier aparte. Seam A↔B↔C cerrado: `exchange` + `product_group` migran a Instrument como única autoridad (Contract pierde `exchange` propio); B keyea `(calendar_ref, exchange, product_group)`, C keyea `(instrument_id, exchange, product_group)`; full-vs-micro NO es campo de dominio (config RuleSet). Casos nuevos A-R1-1..4 en el artefacto.
- Los 4 drafts self-authored previos (D2-05A/B/C e integrado D2-05) siguen física pero invalidados (bloque NON-AUTHORITATIVE); sus conclusiones no son input. El bloque `D2-05 = READY_FOR_MANAGER_REVIEW` dentro de [[Echo Futures]] sigue mostrando estado contaminado — corregir es del SUBMANAGER al integrar, no del TOP.
- Núcleo vigente: Instrument (id + quote_currency + calendar_ref + exchange + product_group) / Contract (expiry-specific; tick_value derivado; sin lifecycle timestamps V1); identifiers por `(source, context)`; resolución única en `echo/operation`; rollover prospectivo; mono-contract; fail-closed sin fallback (`CONTRACT_RESOLUTION_FAILED`).
- Baseline verificada: `xKoRx/echo origin/master = 372af59a` (sin delta). Owner decisions: NONE. Deuda: conversión FX para MM no-USD (seam), resolución histórica por fecha para backtester.

## Señales de carga

- Cargar sólo con [[Echo Futures]] activo (D2-05 en curso). Autoridades del diseño viven en el artefacto D2-05A y en D2-04; esta nota es sólo continuidad de proceso.

## Próxima acción

- SUBMANAGER: re-derivar D2-05B/D2-05C con TOP workers y luego integrar D2-05 respetando los seams §10 del artefacto (calendar_ref nominal hacia B; `source` de identifiers ≠ Provider identity hacia C). Primary Manager review después; no cerrar D2-05 desde este carril.
