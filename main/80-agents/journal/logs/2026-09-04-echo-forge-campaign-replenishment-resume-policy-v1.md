---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-CAMPAIGN-REPLENISHMENT-RESUME-POLICY-V1-TOP"
source_feedbacks:
  - "[[2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/memory/public/decision/symphony/2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`
  - `80-agents/journal/sessions/2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1-summary.md`
  - `80-agents/journal/feedback/system-1/2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1-session-feedback.md`

## Motivo

- Cerrar semánticamente Campaign Replenishment / Resume Policy V1 y Builder Budget V1 como un solo contrato, con source read-only sobre `93c6665`.

## Fuentes usadas

- Stop Policy V1 frozen, C3 physical closure, zero-supply closure, `FEAT-SQX-CROSS-FLOWRUN-REUSE` TOP-DECISIONS, `forge_campaign_workflow.go`, `MaterializeForgeCampaignWaveSpec`, `resolveHistoricalSourceCohort`, `AdoptStrategy` v2, `WaveConfig`, example config committed.

## Resolución aplicada

- Contrato: NEW_BUILDER_SUPPLY bounded; partial pipeline reuse POST_V1; Stop Policy intacta; mint wave-scoped de canonical_id REQUIRED; sin Decision nueva.

## Validación

- Baseline git HEAD == origin/master == `93c66651251edefcc65ef183ac9f7b832b4de5de`. Dirty foráneo preservado. Cero source mutation.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, paths absolutos de máquina ni memoria interna

## Rollback

- Revertir las notas de vault de esta sesión; no hay cambio de código que revertir.
