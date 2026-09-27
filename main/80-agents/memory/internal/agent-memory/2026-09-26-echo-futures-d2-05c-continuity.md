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
related: ["[[Echo Futures — D2-05C Provider Program Rules]]", "[[Echo Futures — D2-04 Operation Order Fill Position]]", "[[Echo Futures — D2-05A Instrument Contract]]", "[[Echo Futures — D2-05B Session Calendar]]"]
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-05c-top"
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

# Echo Futures — Continuidad D2-05C (TOP worker Provider/Program/RuleSet)

## Continuidad

- **Estado final: `READY_FOR_INTEGRATION` @ vault `f7539709` (pin handoff `0295daca`) tras repair C-R3; evidence hygiene C-R5 @ `7d0fd120` (pin `c3aa8a72`: retirada evidencia Lucid no autorizada — allowed trading times y cutoff 4:45 PM ET; matriz deja Lucid UNKNOWN y V2 sin reglas forced-flat/session observadas; se conservan claims Lucid estructurales y con soporte específico: news por plan, platform support). Previamente cleanup normativo C-R4 @ `5da3eefc` (pin `e3f750b0`): §6 sin provider-clock/holiday de B (autoridad RuleSet, relación opcional con SessionBoundaries), Tradeify automation = UNKNOWN, corpus §2 con UNKNOWN en enumeración, Caso G separado con/sin safety intent (entitlement ⇒ suspensión, nunca intent), ProviderDecision{phase?} nullable como contrato único.** Artefacto: `10-projects/Echo Futures/Echo Futures — D2-05C Provider Program Rules.md`. `OWNER_DECISIONS_REQUIRED = NONE`. El draft self-authored previo fue eliminado y reemplazado completo (los drafts D2-05\* previos se ignoraron como autoridad según mandato).
- Núcleo del diseño (estable desde el artefacto original `4cd85d35`): Provider (policy owner, `provider_id` canónico) 1→0..N ProviderProgram (producto real, sin enums de negocio) → fase opcional provider-local (NO aggregate) → ProviderRuleSet versionado por `(provider, programa[, fase])` con `version/effective_at/source_refs` obligatorias; ≤1 versión efectiva; cero autoridad ⇒ fail-closed `NO_RULESET_AUTHORITY`. Account 1→0..1 `ProviderAccountBinding` (programa, fase opcional, RuleSet resuelto, transport entitlement fail-closed separado de platform support, day_boundary por referencia); AccountStrategy intacta. Runtime enforcea sólo reglas ACCOUNT-scoped + cross-cuenta Echo-observables con soporte de matriz.
- Enforcement (modelo final post C-R1/C-R2/C-R3): (1) admisión pre-materialización = guard en `echo/operation` (autoritativo, kache-fed, fail-closed stale) + pre-filtro en `signal_fanout`; ALLOW | DENY_NEW_RISK antes de crear Operation. (2) order gate post-MM/pre-egreso: max contracts/order = chequeo local `PER_ORDER`; caps compartidos = **reserva serializada** en `echo/provider_rules` (key `account_id`, único authority owner) en la **métrica tipada** (`GROSS` / `NET_ABS` intervalo `max(n+R⁺,R⁻−n)≤cap` / `GROUP_WEIGHTED`); release **sólo por finalidad venue-autoritativa** (`VENUE_FINAL` vía history-by-tag R10, `reservation.finality_state=PENDING_FINALITY` — no `Order.status`, sin estados nuevos); modify-increase reserva antes de emitir, decrease libera tras ACK, replace = reserva nueva + vieja hasta finalidad; **outstanding grants se revalidan** (`ReservationRevalidate`; GRANT porta epoch `{rule_set_id, rule_set_version, cap_family, scope}`) — INVALID ⇒ `REJECTED{PROVIDER_GATE}` + release + sin egress (una Order no emitida no es exposición existente); linearization point = cola serializada por key del authority owner; DENY_ORDER ⇒ MM decide, entradas todas denegadas ⇒ `TERMINAL(ENTRY_REJECTED)` con provenance; Order denegada = `REJECTED{rejection{source: PROVIDER_GATE, decision_id}}` durable; salidas jamás bloqueadas. (3) safety asíncrono por intents (ForceClose≠TERMINAL, `TERMINAL(SAFETY_FLATTEN)` por guards R3); revocación de entitlement NO genera intents: ⇒ DENY_NEW_RISK + **suspensión de TODA emisión automatizada** + flag `SUSPENDED_ENTITLEMENT` (condición operacional, no status) + operador (attestation `operator_authorized_close_only` o flatten manual con divergencia fail-visible). Fail-closed físico: `PHYSICAL_STATE_UNTRUSTED` (POSITION_MISMATCH/stale/breach) ⇒ DENY_NEW_RISK; contadores lógicos Echo-attributables con Position física como trust guard. Familias tipadas + params + excepciones registradas; sin DSL; valores = onboarding con provenance.
- Seams finales congelados: **A (A-R2)** — C scopea por `instrument_id`, `exchange`, `product_group` (campos definitivos de Instrument; `GROUP_WEIGHTED` opcional por RuleSet); **B (B-R1)** — C consume de B sólo `SessionState/SessionDate/SessionBoundaries/NextSessionTransition(calendar_id, instant)` vía `calendar_ref→calendar_id`; provider timezone IANA/windows/cutoff/holiday-policy son autoridad de ProviderRuleSet/ProviderProgram (C puede combinar SessionBoundaries con policy; B jamás publica provider policy). Account DayBoundary = tercera autoridad (reset diario del estado provider se ancla a ella; fallback UTC heredado prohibido). Linearization: cola serializada del authority owner (v6 procesado antes del egress-check ⇒ DENY; no llegado ⇒ v5 correcta por orden serializado).
- Evidencia copy alineada a matriz autoritativa: MFFU/TradeDay/Topstep soportados (MFFU copy prohibido y TradeDay no-duplicación = HARD BINDING INCOMPATIBILITY Echo-observable; Topstep no-VPS = owner check/D6); Tradeify cross-firm y FundedNext copy = **UNKNOWN** (no activables como hard rules sin evidence authority).
- Historia de repairs: C-R1 @ `c7fc38e9` (reserva serializada + carrera, revocación sin flatten, fase colapsada, copy claim-by-claim, binding sin versiones); C-R2 @ `49b76f33` (finalidad venue-autoritativa, modify/replace, métricas tipadas, PHYSICAL_STATE_UNTRUSTED, dos state owners + protocolo, Orders denegadas REJECTED durables, Tradeify/FundedNext UNKNOWN, guard de egress); C-R3 @ `f7539709` (§9 modelo final, namespace finality, seams A/B finales, entitlement sweep, revalidación de grants — reemplaza el honramiento de C-R2, sweep normativo limpio).

## Señales de carga

- Cargar sólo con [[Echo Futures]] activo (D2-05 en curso). La autoridad del diseño vive en el artefacto D2-05C (secciones + repairs + Handoff); esta nota es sólo continuidad de proceso.

## Próxima acción

- SUBMANAGER: D2-05C en `READY_FOR_INTEGRATION` — integrar D2-05 con A y B (ambos READY_FOR_INTEGRATION), pasada de consistencia de seams (A-R2/B-R1 ya consumidos por C) y recién entonces Primary Manager review. No cerrar D2-05 desde los carriles TOP.
