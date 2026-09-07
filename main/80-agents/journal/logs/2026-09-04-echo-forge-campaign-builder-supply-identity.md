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
  - "[[2026-09-04-echo-forge-campaign-builder-supply-identity]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-CAMPAIGN-REPLENISHMENT-BUILDER-SUPPLY-IDENTITY-CORRECTION-TOP"
source_feedbacks:
  - "[[2026-09-04-echo-forge-campaign-builder-supply-identity-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04-echo-forge-campaign-builder-supply-identity

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/memory/public/decision/symphony/2026-09-04-echo-forge-campaign-builder-supply-identity.md`
  - `80-agents/memory/public/decision/symphony/2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`
  - `80-agents/journal/sessions/2026-09-04-echo-forge-campaign-builder-supply-identity-summary.md`
  - `80-agents/journal/feedback/system-1/2026-09-04-echo-forge-campaign-builder-supply-identity-session-feedback.md`
  - `80-agents/journal/agent-runs/2026-09-04-cursor-grok-4-6-echo-forge-campaign-builder-supply-identity.md`

## Motivo

- Corregir el mint de Replenishment V1: no inyectar execution Wave en `canonical_strategy_id`; usar `BuilderSupplyBatchRef` generation-batch-scoped.

## Fuentes usadas

- Identity v2 cutover/storage decisions; G2/G2B checkpoints; `canonical_strategy_id.go`; `adopt_strategy.go` upsert v2; `steps.go` Overview correlation; Builder CFX genetic-evolution; `MaterializeForgeCampaignWaveSpec`; `ForgeCampaignWaveKey`/`ForgeCampaignWaveRequestID`; probe recert `/tmp/canonical-probe-recert-20260904`.

## Resolución aplicada

- OPTION A REJECT. OPTION B+E ACCEPT. Novelty predicate y FIX CONTRACT revisados. Cero source symphony.

## Validación

- `git rev-parse HEAD` == `origin/master` == `93c6665`. `go test ./sqx/core/domain -run TestCanonicalStrategyID_` PASS. Probe recert: same stem across w000001/w000002 → `same_canonical=true`; WaveKey/WorkflowID fuera de identity.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de máquina, memoria interna ni secretos

## Rollback

- Retirar esta decisión y restaurar el CHALLENGE wave-prefix del TOP previo no es válido: ese mint queda REJECT. El Replenishment V1 resto permanece frozen.
