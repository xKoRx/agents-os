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

- D2-05C re-derivado por TOP worker independiente (no SUBMANAGER): artefacto `10-projects/Echo Futures/Echo Futures — D2-05C Provider Program Rules.md` committeado en vault `4cd85d357e395eb36f62ef3123b8898d7b6844d9` (SHA pin en `af5f8c49`), estado `READY_FOR_SUBMANAGER_REVIEW`, `OWNER_DECISIONS_REQUIRED = NONE`. El draft self-authored previo fue eliminado y reemplazado completo (ninguna conclusión proviene de él; los drafts D2-05\* previos se ignoraron como autoridad según mandato).
- Núcleo del diseño: Provider (policy owner, `provider_id` canónico) 1→0..N ProviderProgram (producto real, sin enums de negocio) → fase = atributo del binding + dimensión del catálogo (NO aggregate) → ProviderRuleSet versionado por `(provider, programa, fase)` con `version/effective_at/source_refs` obligatorias; ≤1 versión efectiva; cero autoridad ⇒ fail-closed `NO_RULESET_AUTHORITY`. Account 1→0..1 `ProviderAccountBinding` (programa, fase, RuleSet resuelto, transport entitlement `ALLOWED|CONDITIONAL|FORBIDDEN|UNKNOWN` fail-closed separado de platform support, day_boundary por referencia); AccountStrategy intacta. Runtime enforcea sólo reglas ACCOUNT-scoped; trader/household/cross = eligibility.
- Enforcement reconciliado con D2-04: (1) admisión pre-materialización = guard dentro de `echo/operation` (autoritativo, kache-fed, fail-closed stale) + pre-filtro en `signal_fanout`; `ALLOW | DENY_NEW_RISK` antes de crear Operation; (2) order gate entre decisión MM y egreso transaccional de comandos (max/order, max exposure account/instrument/grupo; exposición propia exacta + agregado cross-key mantenido por `echo/provider_rules` vía Sends checkpoint-atómicos, eventualmente consistente + fail-visible); DENY_ORDER ⇒ sin egress, entradas todas denegadas ⇒ `TERMINAL(ENTRY_REJECTED)` con provenance, sin delete silencioso; salidas jamás bloqueadas; (3) safety asíncrono: `echo/provider_rules` (StateFun keyed account_id, patrón RFC-005) emite `ProviderForceClose` como intent SAFETY_PLANE; `TERMINAL(SAFETY_FLATTEN)` sólo por guards R3. Familias tipadas + params + excepciones provider-specific registradas; sin DSL; valores comerciales = config onboarding con provenance, no congelados.
- Hot update prospectivo: cutoff adelantado ⇒ deny+flatten inmediatos sin retroactivo; cap bajo exposición ⇒ adds denegados sin liquidación inventada (flatten sólo si regla tipada lo declara); instrumento prohibido ⇒ deny new risk, cierres pasan; entitlement revocado ⇒ deny permanente + ForceClose de vivas + re-habilitación manual; daily-loss cambia ⇒ recálculo prospectivo.
- Baseline verificada: `xKoRx/echo HEAD = 372af59a` (worktree limpio, clon `~/aranea/work/d3-shot3-correction-20260924/echo`). Source audit acotado con blob SHAs en §13 del artefacto. Hallazgos clave: `echo.prop_rulesets` legacy ya existe (valida familias: daily loss DAY_HIGH/PREV_CLOSE, total loss static/trailing, news windows, overnight/weekend/hedging, reset tz) pero es REUSE concepto / REPLACE shape (identity por nombre de firma + enum de fase = anti-patrones); no existe concepto Provider en V3 (grep verificado); `AccountState` (ACTIVE/CLOSE_ONLY) y `TradingWhitelist` son inputs directos del gate; familia news tiene precedente directo en `NEWS_BLACKOUT` RFC-007.
- Escalados al SUBMANAGER (seams §14): TOP A debe exponer `Instrument.exchange` + `product_group` (caps por grupo); TOP B debe mantener provider overlay (ventanas/cutoffs) como autoridad DISTINTA de ExchangeSession y exponer provider-clock/timezone + holiday feed; ownership del calendar/holiday feed abierto; Account DayBoundary es autoridad del workstream cuenta/sesión (C sólo la consume).

## Señales de carga

- Cargar sólo con [[Echo Futures]] activo (D2-05 en curso). La autoridad del diseño vive en el artefacto D2-05C (§1–§17 + Handoff); esta nota es sólo continuidad de proceso.

## Próxima acción

- SUBMANAGER: con A/B/C re-derivados, ejecutar la integración D2-05 con pasada explícita de consistencia de seams A↔B↔C (incluidos los tres puntos escalados de §14) y recién entonces Primary Manager review. No cerrar D2-05 desde los carriles TOP.
