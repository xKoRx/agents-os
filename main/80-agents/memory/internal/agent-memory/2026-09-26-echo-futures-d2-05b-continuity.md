---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-26"
updated: "2026-09-26"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities: ["[[Echo Futures]]"]
related: ["[[Echo Futures — D2-05B Session Calendar]]", "[[Echo Futures — D2-04 Operation Order Fill Position]]", "[[Echo Futures — D2-05A Instrument Contract]]"]
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-05b-top"
supersedes:
superseded_by:
load_policy: when_project_loaded
indexable: false
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/echo
---

# Echo Futures — Continuidad D2-05B (TOP worker Session/Calendar)

## Continuidad

- D2-05B re-derivado por TOP worker independiente (no SUBMANAGER): artefacto `10-projects/Echo Futures/Echo Futures — D2-05B Session Calendar.md` committeado en vault `3409fff0f12195f5b6440a8efa3cca2b9457a427`, estado `READY_FOR_SUBMANAGER_REVIEW`. El draft self-authored previo fue reemplazado completo (ninguna conclusión proviene de él).
- Núcleo del diseño: calendario = dataset owner-managed (`echo.exchange_calendars`: `weekly_base` recurrente + overrides fechados `HOLIDAY_CLOSED|EARLY_CLOSE|SPECIAL_SESSION` con `applicable_groups`; precedencia override > base > CLOSED fail-closed) + resolver puro `sdk/calendar` sin I/O. Time authority IANA-only con tzdata embebida por release; instants UTC RFC3339Nano; `session_date` es dato de la sesión (`trade_date_shift`, sin fórmula universal CME); una sesión por trade date en V1. `NamedTradingWindow` config (`EXCHANGE_SUBSET | CLOCK`) referenciada por `window_id`; disponibilidad efectiva = ventana ∩ exchange (exchange cerrado gana). Provider seam read-only (SessionState/SessionDate/SessionBoundaries/NextSessionTransition); forced-flat = intent ForceClose D2-04 (R3). Account DayBoundary permanece en ruleset/DayBoundaryCache; fallback UTC-23:00 prohibido para cuentas Futures (fail-closed `ACCOUNT_DAYBOUNDARY_REQUIRED`). Bar contract D2-06: session-scoped usa `session_id=(calendar_id, session_date)`, ningún bucket cruza open/close/break, transiciones sólo vía `next_transition_utc`. Determinismo: dataset append-fechado + run anchor `{calendar_id → revision_hash}` en manifiesto de replay/backtest (corrección posterior visible, nunca silenciosa). Sin microservice, sin segundo runtime, sin Revision framework.
- Baseline verificada: `xKoRx/echo origin/master = 372af59a` (fetch re-hecho, sin delta). Source audit: calendario/sesión/ventanas NO existen en V3 (NEW); DayBoundaryCache/kache/ConfigCache/symbol-mapping/strategy-history clasificados REUSE con blobs en §11 del artefacto. `OWNER_DECISIONS_REQUIRED = NONE`.
- Punto de reconciliación de seams para el SUBMANAGER: D2-05A dejó `calendar_ref` nominal en Instrument; D2-05B §12 pide binding `(exchange, product_group) → calendar_id` "o equivalente resoluble" — ambas formas son equivalentes; elegir una canónica al integrar D2-05.

## Señales de carga

- Cargar sólo con [[Echo Futures]] activo (D2-05 en curso). La autoridad del diseño vive en el artefacto D2-05B (§1–§15 + Handoff) y en la evidencia Front E (`30-resources/futures/CONTRACT + SESSION SEMANTICS — AUTHORITATIVE EVIDENCE.md`); esta nota es sólo continuidad de proceso.

## Próxima acción

- SUBMANAGER: re-derivar D2-05C con TOP worker (seam §7 de D2-05B fija las primitivas que C debe consumir), luego integrar D2-05 con pasada explícita de consistencia de seams A↔B↔C (incluida la elección canónica del binding calendario↔Instrument) y recién entonces Primary Manager review. No cerrar D2-05 desde los carriles TOP.
