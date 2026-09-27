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

- D2-05B re-derivado por TOP worker independiente y **reparado por mandato SUBMANAGER (repair B-R1/B-R2)**: artefacto `10-projects/Echo Futures/Echo Futures — D2-05B Session Calendar.md` en vault `f579418319265e253943453df359a172a72c8c93`, estado `READY_FOR_SUBMANAGER_REREVIEW`. Partes aceptadas del review no reabiertas.
- Repair B-R1: cardinalidad congelada **un ExchangeCalendar = un grupo producto/sesión semántico**; la dimensión `product_group` desapareció del shape, de los overrides y del API (`ResolvedSession/SessionState/...` ya no reciben `group`); dos semánticas distintas = dos `calendar_id`; `session_id = (calendar_id, session_date)` queda unívoco por construcción (caso B-R1-CASE-1 demuestra no-colisión con early closes distintos).
- Repair B-R2: el anchor de run **NO es un puntero** — es `{calendar_id → (revision_hash, snapshot_payload)}` (+ secuencia de transiciones con `effective_from` si el run consumió >1 versión) grabado **obligatoriamente en el manifiesto del run** (offline al inyectar; live al arrancar y en cada hot update consumida). El resolver recibe un **dataset inyectado**, nunca un anchor (no existe `resolver(anchor)`). Garantía exacta: re-inyectar el snapshot grabado = boundaries byte-idénticos; NO garantiza procesos sin provenance, tzdata entre releases (visible por identifier en manifiesto), ni persistencia más allá del retention del run artifact (caso B-R2-CASE-2).
- Núcleo vigente del diseño: calendario = dataset owner-managed (`weekly_base` + overrides fechados `HOLIDAY_CLOSED|EARLY_CLOSE|SPECIAL_SESSION`; precedencia override > base > CLOSED fail-closed) + resolver puro `sdk/calendar` sin I/O; IANA-only + tzdata embebida por release; `session_date` es dato (`trade_date_shift`); `NamedTradingWindow` (`EXCHANGE_SUBSET | CLOCK`) con disponibilidad = ventana ∩ exchange; provider seam read-only (forced-flat = intent ForceClose D2-04 R3); account_day separado (fallback UTC-23:00 prohibido en Futures); bar contract D2-06 intacto (session-scoped por session_id; sin cambios por el repair salvo identidad ya colisión-free).
- Baseline verificada: `xKoRx/echo origin/master = 372af59a` (sin delta). `OWNER_DECISIONS_REQUIRED = NONE`.
- Seam con TOP A cerrado semánticamente (post-repair): binding resoluble **1:1 Instrument → calendar_id** (forma del campo la fija TOP A: `calendar_ref` directo o `(exchange, product_group) → calendar_id` mapeado son equivalentes); prohibido re-introducir dimensión de grupo dentro del calendario.

## Señales de carga

- Cargar sólo con [[Echo Futures]] activo (D2-05 en curso). La autoridad del diseño vive en el artefacto D2-05B (repair section + §1–§15 + Handoff) y en la evidencia Front E (`30-resources/futures/CONTRACT + SESSION SEMANTICS — AUTHORITATIVE EVIDENCE.md`); esta nota es sólo continuidad de proceso.

## Próxima acción

- D2-05 INTEGRATION repair I-R1 aplicado (2026-09-27, mandato SUBMANAGER): §14 reescrito con resolución ÚNICA de Contract (`ResolveExecutionContract` = validación+resolución en una llamada, sin pre-check+lookup/TOCTOU; Stage-1 provider admission consume llaves de Instrument + primitivas de sesión, jamás resuelve Contract) y §15 con semántica de DOS owners (Fill + emisión de CapacityUpdate atómicos sólo en la frontera del operation owner; provider_rules aplica después idempotentemente; skew fail-safe: false DENY posible, over-GRANT imposible). Casos I-R1-A/B añadidos; A-H PASS-BY-DESIGN sin cambios; children intactos; project note intocada (0 hits de las fórmulas defectuosas). Estado: `READY_FOR_SUBMANAGER_REREVIEW` @ vault `f4293a52` (blob artefacto `bc370183`; parte de las ediciones barrida por sync `f8bfaefe`/`4b7258b6`). Sigue: SUBMANAGER final gate; no promover a manager review ni avanzar D2-06 desde este carril.
