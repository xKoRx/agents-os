---
type: change_log
schema_version: 1
scope: session
created: "2026-09-28"
updated: "2026-09-28"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures — D2-07 Execution Runtime]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-28-echo-futures-d2-07-r1-routing-repair-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/echo
---

# Echo Futures — D2-07-R1 Routing Repair — Change Log

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - main/10-projects/Echo Futures/Echo Futures — D2-07 Execution Runtime.md (§1 status/nota de corrección/baselines; §4 diagrama de retorno y correlación; §6 cola de topología; §8 routing por familia; §17 freeze de tres caminos; Fuentes; Handoff D2-07-R1)
  - main/10-projects/Echo Futures/Echo Futures.md (bullet Target architecture y wording de baseline corregidos; sección D2-07-R1 añadida; frontmatter `updated`)
  - main/80-agents/memory/internal/agent-memory/2026-09-28-echo-futures-d2-07-integration-continuity.md (actualizada in-place al estado post-repair; mismo continuity_key)
  - main/80-agents/journal/feedback/system-1/2026-09-28-echo-futures-d2-07-r1-routing-repair-session-feedback.md (nuevo)

## Motivo

- Primary Manager verdict sobre la integración D2-07: arquitectónicamente aceptable salvo un defecto de routing — integrated event routing incorrectly promoted non-Operation observations into op-key execution stream. Además, el handoff anterior reportó el baseline inicial como "AGENTS-OS SHA" sin distinguirlo del estado final persistido.

## Fuentes usadas

- [[Echo Futures — D2-07 Execution Runtime]] (artifact reparado), [[Echo Futures]] (estado D2).
- Contraste puntual: [[Echo Futures — D2-04 Operation Order Fill Position]] §7/§8.2/§8.3 (correlación obligatoria + topics de observación), [[Echo Futures — D2-07A Execution Adapter Contract]] §9 (familias), [[Echo Futures — D2-07C Execution Runtime Topology]] (wording histórico del defecto).
- Historia real de persistencia verificada en git: `b45e9328` (baseline inicio integration worker) → `36384956` (persistencia integración) → `89120c64` (cierre, HEAD al iniciar este repair).

## Resolución aplicada

- Routing congelado en tres caminos (artifact §8/§17): op-correlated `OrderObservation`/`OrderActionObservation`/`Fill` → `echo.execution-events.v1` (key op key) → `echo/operation`; `PositionObservation` (sin `operation_id`) → `echo.position-observations.v1` → physical position/reconciliation; `ExecutionSessionObservation` → runtime/readiness path account-scoped (naming topic = IMPLEMENTATION DETAIL/D6; jamás `operation_id` fabricado, jamás fact de Operation). Manual/unknown: observación física + reconciliation debt; canonical correlated facts sólo tras correlación demostrada. Sin fabricar `operation_id`; sin otros cambios arquitectónicos.
- Traceability: el artifact distingue INTEGRATION BASELINE (`b45e9328…`, inicio del worker) de los SHA persistidos posteriores (`36384956…`, `89120c64…`) y del FINAL AGENTS-OS SHA (HEAD post-repair, registrado en handoff de sesión).
- Estado: `D2-07-R1 = READY_FOR_MANAGER_REVIEW`. Nada reabierto de lo ACCEPTED; `OD-D2-07-1` sigue pendiente; sin D2-08; sin cierre D2.

## Validación

- Grep de coherencia del artifact: sin wording residual de stream único op-key para las cinco familias; menciones restantes son el texto de la corrección o el lado producción del adapter.
- Read-back de secciones editadas post-commit (ver handoff de sesión).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert` del commit de persistencia de esta sesión (sync D2-07-R1); sin efectos fuera del vault.
