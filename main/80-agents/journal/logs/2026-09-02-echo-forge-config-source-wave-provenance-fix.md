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
related: []
aliases: []
confidence: verified
source_session: "ECHO-FORGE-CONFIG-SOURCE-WAVE-PROVENANCE-FIX-NORMAL"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-02-echo-forge-config-source-wave-provenance-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `sqx/activities/worker/steps/steps.go`
  - `sqx/activities/worker/steps/steps_test.go`
  - `80-agents/memory/public/decision/symphony/2026-09-02-config-source-wave-identity.md`
  - `80-agents/memory/public/known-error/symphony-config-source-wave-legacy-cfg.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`

## Motivo

- Se corrigió `CONFIG_SOURCE_WAVE_PROVENANCE_VIOLATION` detectado en C3 y se dejó explícito que el FlowRun contaminado no es evidencia de supply.

## Fuentes usadas

- Baseline/HEAD Git, prechange assertions A–G, tests prechange que reprodujeron `_wc3`/`_wforge`, matriz focalizada T1–T8, suite/race/vet y auditoría estática.

## Resolución aplicada

- `dbRegister.Execute` ahora usa `EffectiveConfigSourceWave` para `cfgID` y `configMinioKey`; outputs siguen usando execution Wave. Commit `bac1d6ef93cd4714c1af4f2e44516bea44642e80` fue pushed a `origin/master`.

## Validación

- PASS / CLOSED para source fix; nueva release requerida `0.2.86`. La suite `activities/worker` conserva fallos baseline no causales por fixture MT5 ausente.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No rollback: el cambio es el fix mínimo y no se modificaron watcher, Campaign, generic workflow, DB schema, MinIO adapters ni release scripts.
