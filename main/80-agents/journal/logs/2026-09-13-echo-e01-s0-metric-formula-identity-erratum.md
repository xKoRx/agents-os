---
type: change_log
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Echo]]"
project: "[[Echo — E-01 Canonical SDK Foundation S0]]"
application: "[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]"
entities:
  - "[[Echo — E-01 Canonical SDK Foundation S0]]"
related:
  - "[[Echo — E-05 Analytics Convergence A0]]"
aliases: []
confidence: verified
source_session: 2026-09-13-echo-s0-metric-formula-identity-erratum
source_feedbacks:
  - "[[2026-09-13-echo-s0-metric-formula-identity-erratum-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo E-01 — S0 metric formula identity erratum

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated / conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-01 Canonical SDK Foundation S0.md`
  - `10-projects/Echo/agentes/Echo — E-05 Analytics Convergence A0.md`
  - `xKoRx/echo` `v3/sdk/contracts/analytics.go`
  - `xKoRx/echo` `v3/sdk/contracts/analytics_test.go`
  - `xKoRx/echo` `specs/FEAT-SDK-CANONICAL-CONTRACT/VERIFICATION.md`

## Motivo

- Registrar el erratum post-certificación activado por E-05 V3-006 sin reabrir el SPEC frozen ni mezclar ownership con E-05.

## Fuentes usadas

- `origin/master` `a99f9a63354bbe72219d1e590bb93757ed08e45e`, S0 certified pin `91671f6f46ffa889a79aed0979cb3b4e5821ed33`, E-05 verifier #3 evidence and the separate certified-pin repro.

## Resolución aplicada

- La implementación `8a979fb5bf218abed5f5c352896b727303dbf65f` unifica duplicate detection y ResultsDigest ordering sobre los seis campos frozen. Se registró BWC literal, corpus G01–G36, race, coverage, vet y el non-effect E-04/F-04. E-05 quedó referenciado como `BLOCKED_BY_S0_ERRATUM` con la branch/SHA y no se marcó VERIFIED.

## Validación

- Tests y gates PASS; no goldens existentes, SPEC, schema, FormulaSetDigest, ref recipe, E-05 source, Symphony, tag, release, merge ni master fueron modificados.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Reversión técnica: revertir el commit focalizado en la branch; la evidencia histórica y el erratum documental quedan separados para revisión del Manager.
