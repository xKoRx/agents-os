---
type: decision
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-04-forge-campaign-v2-stop-policy-schema-mismatch]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-CAMPAIGN-V2-STOP-POLICY-SCHEMA-BOUNDARY-FIX-NORMAL
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-forge-campaign-stop-policy-schema-ownership

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Campaign v1 y v2 son wrappers distintos, mientras que `ForgeCampaignStopPolicy` mantiene autoridad propia en `domain.ForgeCampaignStopSchema` (`sqx-forge-campaign.v1`). Copiar `ForgeCampaignSpec.Schema` al StopPolicy hacía fallar el intake v2 con `contract_conflict` antes de materializar cualquier Campaign.

## Decisión

- El intake debe construir siempre `ForgeCampaignStopPolicy.Schema` con `domain.ForgeCampaignStopSchema`. Campaign version sólo selecciona la forma de `ForgeCampaignSpec`, `RequestContractVersion` y la presencia/validación de `ReplenishmentPolicy`.

## Rationale

- Un discriminator de versión del contrato padre no es autoridad de un contrato anidado independiente. La proyección explícita conserva Stop Policy v1 congelada y permite Campaign v2 sin crear `sqx-forge-campaign-stop.v2`.

## Consecuencias

- V1 mantiene intent v1 y replenishment ausente; V2 usa intent v2, StopPolicy v1 y ReplenishmentPolicy v1 obligatoria. La semántica de `TARGET_REACHED`, `MAX_WAVES_REACHED` y `CONTINUE` permanece intacta.

## Alternativas descartadas

- Copiar `st.Spec.ForgeCampaign.Schema`, versionar StopPolicy por Campaign o modificar `ForgeCampaignStopSchema`.
