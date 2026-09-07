---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related: []
aliases: []
confidence: verified
source_session: ECHO-FORGE-CAMPAIGN-V2-STOP-POLICY-SCHEMA-BOUNDARY-FIX-NORMAL
source_feedbacks:
  - "[[2026-09-04-forge-campaign-schema-boundary-fix-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04-forge-campaign-v2-stop-policy-schema-boundary-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `sqx/activities/watcher/intake.go`
  - `sqx/activities/watcher/intake_test.go`

## Motivo

- El intake copiaba el schema de `ForgeCampaignSpec` a `ForgeCampaignStopPolicy`, rompiendo Campaign v2 porque ambos contratos tienen authorities independientes.

## Fuentes usadas

- [[2026-09-04-forge-campaign-v2-stop-policy-schema-mismatch]] · baseline/source authority `ab2152632a63b3352cffd8a21b54a54affc4a11d` · StopPolicy authority `domain.ForgeCampaignStopSchema`.

## Resolución aplicada

- Se reemplazó el mapping por `Schema: domain.ForgeCampaignStopSchema` y se agregaron pruebas T1–T5 dirigidas. No se modificaron schemas, Replenishment, Identity v2, migration 013, release/deploy ni Campaign física.

## Validación

- T1–T5 PASS; watcher normal/race, runtime, capabilities y vet PASS; Campaign workflows PASS. La suite completa de workflows conserva baseline failures por `flow_run_start` no registrado. Commit `9ef5549da3308b286ecff52f2d825af8024c27fe` pushed; `HEAD == origin/master`.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit `9ef5549da3308b286ecff52f2d825af8024c27fe` si se requiere volver al source anterior; no ejecutar rollback destructivo sobre el checkout ni sobre datos físicos.
