---
type: change_log
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-c3-lean-0289-blocked-reretester]]"
  - "[[2026-09-04-reretester-single-artifact-contract]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-RELEASE-0.2.89-CONTAIN-BLOCKED-CAMPAIGN-AND-C3-LEAN-RECERT-NORMAL
source_feedbacks:
  - "[[2026-09-04-echo-forge-c3-lean-0289-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04-echo-forge-c3-lean-0289

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated / conflict-resolution
- **Archivo(s):** decision, known-error, feedback, agent_run y checkpoint del proyecto Echo Forge.

## Motivo

- La misión exige detenerse ante un defecto nuevo. CERT-A 0.2.89 alcanzó una wave física y falló en `05_reretester` por el contrato exacto de un key y un `StrategyArtifact`.

## Fuentes usadas

- Source/SDK authorities, release manifest, CFX MinIO/local, Temporal Describe/History y PostgreSQL campaign/flow/decision rows.

## Resolución aplicada

- Se intentó C0 antes del rollout, pero el `CancelWorkflow` se dirigió al namespace `sqx`; la autoridad efectiva era `sqx-prop`. Lectura posterior detectó que la Campaign vieja avanzó a una wave fallida (`OLD_CAMPAIGN_ALREADY_ADVANCED`). Luego se detuvo la misión; no se hizo otra mutación sobre la Campaign vieja.

## Validación

- Campaign vieja: `FAILED`, una wave/FlowRun/Generic child, cero finalists y cero stop evaluations. Campaign A nueva: `FAILED` en final reretester, una wave/Generic child, cero finalists/promotion/evaluations. C3 no certificada. Deudas conocidas preservadas.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No revertir source ni release manifest. No redeliver la identidad A. El lead debe resolver el contrato reretester y repetir con identidad nueva.
