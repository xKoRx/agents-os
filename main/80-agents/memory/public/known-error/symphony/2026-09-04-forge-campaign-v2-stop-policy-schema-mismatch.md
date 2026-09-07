---
type: known_error
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1]]"
  - "[[2026-09-04-echo-forge-c3-lean-recert-blocked]]"
aliases:
  - FORGE_CAMPAIGN_V2_STOP_POLICY_SCHEMA_MISMATCH
  - resolve ForgeCampaign v2 contract conflict
confidence: verified
source_session: "ECHO-FORGE-RELEASE-0.2.93-AND-FINALIST-FACTORY-V1-PHYSICAL-CERT-NORMAL"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# 2026-09-04-forge-campaign-v2-stop-policy-schema-mismatch

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- La solicitud v2 pasa `validate_spec`, `validate_configs`, upload y `save_config`, pero `dispatch_workflow` falla con `resolve ForgeCampaign: invalid ForgeCampaign StopPolicy schema "sqx-forge-campaign.v2": contract_conflict`.
- El fallo ocurre antes de crear `CampaignRef`, workflow padre, wave o FlowRun; el watcher reintenta mientras el archivo permanece en input.

## Causa

- `sqx/activities/watcher/intake.go:73-75` copia `st.Spec.ForgeCampaign.Schema` directamente a `domain.ForgeCampaignStopPolicy.Schema`.
- Para una solicitud `sqx-forge-campaign.v2`, el runtime acepta el wrapper v2 y la política de replenishment, pero `domain.ForgeCampaignStopSchema` sigue siendo `sqx-forge-campaign.v1`; la resolución no proyecta el schema wrapper v2 al StopPolicy v1 antes de validar.

## Impacto

- Bloquea la certificación física de Replenishment V1 antes de la primera wave y hace inalcanzables CONTINUE, `BuilderSupplyBatchRef`, new supply, redelivery y replay.
- No existe workaround de configuración compatible: bajar a v1 eliminaría el contrato `max_builder_candidates_per_wave` exigido por esta certificación.

## Detección

- Release exacta `0.2.93` en source `ab2152632a63b3352cffd8a21b54a54affc4a11d`; el watcher recompilado desde ese source reproduce el error a las `2026-09-04T23:23:06Z` y posteriores.
- La configuración física `schema=sqx-forge-campaign.v2`, `target_finalists=2`, `max_waves=2`, cap `20` fue aceptada hasta `save_config`; el error se observó sólo al resolver intake.

## Mitigación

- Clasificación: **A. PRODUCT DEFECT**. Detener el watcher de certificación y no reintentar, no parchear source, no cambiar identity/thresholds y no iniciar otra Campaign.
- Preservar release, fleet, migración y logs como evidencia; volver a Lead para corregir la proyección de contrato, publicar una nueva release y repetir con identidades nuevas.
- Resolución source: `resolveForgeCampaignIntake` ahora construye `ForgeCampaignStopPolicy.Schema` desde `domain.ForgeCampaignStopSchema`, independientemente de `ForgeCampaignSpec.Schema`; commit `9ef5549da3308b286ecff52f2d825af8024c27fe` pushed a `origin/master`.
- Resolución verificada: T1–T5 PASS y el subconjunto `./sqx/workflows/... -run ForgeCampaign` PASS; la suite completa conserva únicamente fallos baseline por `flow_run_start` no registrado. La recertificación física queda después de crear la release candidata.

## Evidencia

- Gate 0 PASS: `HEAD`, `master` y `origin/master` = `ab2152632a63b3352cffd8a21b54a54affc4a11d`; SDK pin `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`.
- Gate 1 PASS: migración canónica `013_forge_campaign_replenishment_policy.up.sql` aplicada por startup; no hubo SQL ad-hoc.
- Gate 2/3/4/5 PASS: authority `0.2.93` disponible, release-only publicada; manifest `4f5037fc837b851bca349aac8c6f283b179d0b3b37afeaaa61e697fb04e6e86b`, Symphony `14fd9f20c9fa17ef927fc4d0d400eef9f3a450bb455a920ef6d62343299007c9`, Windows `67f87a25c24b95a043743ecea2deb238ace9e4cbe35e63e8c47fa4a67d9add71`, fleet 4/4, MT5 6140 permitido.
- No hubo `CampaignRef`, `CampaignIntentToken`, workflow, wave, Builder supply, StrategyRef, promoción, stop evaluation ni resultado; por tanto no se ejecutaron gates físicos posteriores.
