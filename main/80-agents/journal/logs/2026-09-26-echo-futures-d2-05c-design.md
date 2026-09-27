---
type: change_log
schema_version: 1
scope: session
created: "2026-09-26"
updated: "2026-09-26"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-05C Provider Program Rules]]"
related:
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/echo
  - echo-futures
---

# 2026-09-26-echo-futures-d2-05c-design

## Cambio

- **Tipo:** replaced (draft invalidado eliminado) + created (checkpoint interno y feedback)
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures — D2-05C Provider Program Rules.md` (reemplazo completo del draft self-authored invalidado; artefacto durable del workstream D2-05C, commit `4cd85d35`, pin de handoff `af5f8c49`).
  - `80-agents/memory/internal/agent-memory/2026-09-26-echo-futures-d2-05c-continuity.md` (checkpoint `echo-futures/d2-05c-top`).
  - `80-agents/journal/feedback/system-1/2026-09-26-echo-futures-d2-05c-session-feedback.md` (pedido explícito del mandato).
  - Este change_log.

## Motivo

- El SUBMANAGER D2-05 despachó el carril D2-05C a un TOP worker independiente tras invalidar los drafts D2-05\* autoescritos previos. El mandato exige ignorar esos drafts como autoridad y REEMPLAZAR el archivo D2-05C con un diseño re-derivado desde las autoridades congeladas ([[Echo Futures]] D2-01..04, [[Echo Futures — D1 Analysis Pack]], matriz Front C corregida por manager) y el source `xKoRx/echo@372af59a` verificado.

## Contenido del cambio

- Modelo V1: Provider → ProviderProgram → fase (atributo de binding + dimensión de catálogo) → ProviderRuleSet versionado por `(provider, programa, fase)` con provenance obligatoria; `ProviderAccountBinding` fuera de AccountStrategy; entitlement de transporte fail-closed separado de platform support; runtime enforcea sólo ACCOUNT-scoped.
- Enforcement en tres planos reconciliados con D2-04: admisión pre-materialización (guard en `echo/operation` + pre-filtro fanout), order gate post-MM pre-egreso, safety asíncrono por intents (ForceClose != TERMINAL).
- Familias de reglas tipadas clasificadas (HOT-PATH / SAFETY INPUT / CONFIG-ELIGIBILITY / DEFER / NOT RUNTIME), hot-update semantics para 5 casos, provenance `ProviderDecision`, casos C/D/F/G, disposición Echo V3 con blob SHAs (incluye hallazgo `echo.prop_rulesets` legacy como REUSE concepto / REPLACE shape).
- Gate: `D2-05C_READY_FOR_SUBMANAGER_REVIEW`; `OWNER_DECISIONS_REQUIRED = NONE`.

## Verificación

- Baseline Echo: `HEAD = 372af59a7b83604781346613da01e3d510ea1360`, worktree limpio (clon `~/aranea/work/d3-shot3-correction-20260924/echo`); toda la evidencia §13 vía `git show 372af59a:<path>` con blob SHA.
- Sin código productivo; sin operaciones de infraestructura; commits de vault locales según práctica de sesión.

## Notas

- No se crearon L0/L1 (delta = continuidad + feedback, patrón de los carriles hermanos D2-05A/B).
- Graphify: CLI no disponible en PATH de esta superficie; sin query de validación. El índice se refresca con la próxima query disponible.
