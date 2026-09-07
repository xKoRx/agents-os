---
type: change_log
schema_version: 1
scope: session
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-09-02-echo-forge-c3-adaptive-workflow-registration]]"
  - "[[2026-09-02-echo-forge-c3-mt5-fidelity-period-mismatch]]"
  - "[[2026-09-02-echo-forge-c3-cert-a-supply-via-aligned-mt5-window]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-C3-PHYSICAL-BLOCKERS-FIX-NORMAL
source_feedbacks:
  - "[[2026-09-02-echo-forge-c3-physical-blockers-fix-normal-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge C3 physical blockers source fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `xKoRx/symphony/sqx/cmd/sqx-worker/main.go`
  - `xKoRx/symphony/input/example/config.json`
  - `xKoRx/symphony/sqx/core/runtime/mt5_task_config_test.go`

## Motivo

- C3 B1 production registration gate and B2 MT5 fidelity configuration were blocked by source/config defects identified in the frozen RCA.

## Fuentes usadas

- Frozen RCA notes, the aligned-window decision, source gate output and targeted test output.

## Resolución aplicada

- Removed only the two Adaptive production registrations; aligned `mt5-final` to `2016.01.04` → `2026.06.05`; added exact `promotion` binding to the unique `mt5-final-fidelity-ranking`; added minimal assertions to the existing example-config runtime test.

## Validación

- `jq`, targeted/full runtime tests, worker tests and race, worker/runtime vet, static contract assertions and diff checks PASS; broad workflows failure classified as preexisting WFM test registration baseline.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revert commit `48997d7` if the owner rejects the source fix; physical release and certification remain separate future operations.
