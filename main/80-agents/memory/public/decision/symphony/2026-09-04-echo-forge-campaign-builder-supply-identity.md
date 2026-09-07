---
type: decision
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1]]"
  - "[[2026-08-23-durable-strategy-identity-v2-cutover]]"
  - "[[2026-08-23-durable-strategy-identity-v2-storage-support]]"
aliases:
  - BuilderSupplyBatchRef
  - NEW_BUILDER_SUPPLY identity
confidence: verified
source_session: "ECHO-FORGE-CAMPAIGN-REPLENISHMENT-BUILDER-SUPPLY-IDENTITY-CORRECTION-TOP"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-echo-forge-campaign-builder-supply-identity

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Baseline read-only: symphony `93c66651251edefcc65ef183ac9f7b832b4de5de` == HEAD == origin/master. Dirty foráneo preservado. Cero source mutation.
- Replenishment V1 ([[2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1]]) permanece frozen excepto el mint `wNNNNNN_` al stem de Builder PRODUCED.
- Identity v2 frozen: `identity_model_version=2`, unique global `ON CONFLICT (canonical_strategy_id)`, `config_id` provenance, MODEL 1 GENERATED_STRATEGY generation-batch-scoped; cross-generación semántica fuera de contrato v2.
- Graphify symphony stale (graph.json 2026-09-03); vault `graphify-obsidian` hung en filter. Orientación por graphify-personal + source.
- Recertificación independiente de esta sesión: `go test ./sqx/core/domain -run TestCanonicalStrategyID_` PASS; probe `/tmp/canonical-probe-recert-20260904` (copia byte-a-byte de `canonical_strategy_id.go`) demuestra `same_canonical=true` entre keys `wave_forge-<CampaignRef>-w000001/…/Strategy_2.1.15.z0.sqx` y `…-w000002/…` del mismo stem; path con WorkflowID ignorado; retry misma ola = mismo id.

## Decisión

- `canonical_strategy_id` v2 significa **identidad de GeneratedStrategy observada en un generation batch**, no identidad semántica de trading, no hash de bytes, y no UUID de ejecución. Fórmula vigente: `CanonicalStrategyID(published_basename)`; no se reabre `CanonicalStrategyID()` ni el upsert v2.
- `Strategy_X.Y.Z` es ResultsGroup/cohort token del run SQX Builder. Reinicia por build. Es input de correlación Overview↔archivo, no GUID nativo. Código: `builderResultsGroupPattern` en `sqx/activities/worker/steps/steps.go` («correlation input, not Strategy identity»).
- Colisión real = **CASE 2**. Grado de evidencia: **STEM COLLISION PROVEN** (`CanonicalStrategyID` usa basename; `db_register` llama `CanonicalStrategyID(filename)`; `BuildMinIOPath` pone WaveKey en PATH, no en filename; probe recert `same_canonical=true`). **CONTENT DIVERGENCE INFERRED** (no byte-compare de dos olas Campaign físicas: C3 `max_waves=1`): CFX Builder `generationType=genetic-evolution` sin `RandomSeed`; `Strategy_X.Y.Z` reinicia por build (G2B); databanks se limpian (`CleanupDatabanksHook`); Overview `strategy_id = rg.getName()`. No es CASE 1: el slot local no es identidad de contenido. No es CASE 3: no hay GUID nativo SQX. `AdoptStrategy` v2 devolvería `REPROCESSED` sobre el mismo canonical.
- OPTION A (`wNNNNNN_` execution Wave en identity) = **REJECT**. WaveKey de código: `forge-%s-w%06d` (`ForgeCampaignWaveKey`). RequestID de código: `forge-campaign-%s-wave-%06d`. Ambos son execution namespace del child. Meter `wNNNNNN` en identity viola IDENTITY != EXECUTION aunque el ordinal coincida con la ola. El probe muestra que el prefix `w000002_` sí cambiaría el canonical — eso es el hack, no la autoridad.
- OPTION B+E = **ACCEPT V1**. Autoridad de novedad: `BuilderSupplyBatchRef` durable de política de replenishment, no Temporal. Derivación determinista: `BuilderSupplyBatchRef(campaignRef, waveNumber) = campaignRef + ":g" + NNNNNN`. En V1 `waveNumber` ≡ `supplyGenerationOrdinal` porque cada CONTINUE es NEW_BUILDER_SUPPLY y `ResolveWave` persiste la fila **antes** del child. `CampaignRef` entra como **dueño del generation batch** (entity `forge_campaigns.id`), no como WaveKey/RequestID/Temporal. El invariante «MUST NOT silently depend on CampaignRef» queda satisfecho: la dependencia es explícita y es la llave del batch, no correlación de ejecución. POST_V1 no hereda 1:1 wave→batch si una ola puede saltar Builder: entonces persistir batch sólo en NEW_BUILDER_SUPPLY. No UUID random. No WorkflowID/RunID/host/activity/attempt.
- Publicación Campaign Builder PRODUCED (todas las olas, incluida 1): el basename publicado incorpora el namespace de supply **antes** de `CanonicalStrategyID`: `{INSTR}_{DIR}_{TF}_{strategy}_{version}_{CampaignRef}_g{NNNNNN}_{ResultsGroup}.{hostToken}`. `CampaignRef` entra como dueño de negocio del generation batch, no como WaveKey. Generic (no Campaign) no cambia.
- Provenance vs identity: `BuilderSupplyBatchRef` es **IDENTITY** del GeneratedStrategy (generation-batch-scoped, alineado a v2 G2/G2B) y también se proyecta como campo de provenance en Wave/child. `config_id`, WorkflowID, RunID, FlowRunRef, RequestID, WaveKey, host siguen provenance/compatibilidad y **no** entran al stem.
- Novelty predicate (única autoridad V1, machine-testable): un candidato NEW_BUILDER_SUPPLY es NEW iff `AdoptStrategy` crea origin `PRODUCED` para el `canonical_strategy_id` publicado namespaced por `BuilderSupplyBatchRef`. Equivale a: `(CampaignRef, supplyGenerationOrdinal, producer ResultsGroup token, worker cohort suffix)` no existía en `identity_model_version=2`.
- Retry/redelivery: mismo `CampaignRef` + mismo `waveNumber` → mismo `BuilderSupplyBatchRef` → mismos stems si StageExecution recovery reusa los mismos `.sqx`. Prohibido mint random. Un rerun genético sin recovery ya puede cambiar `Strategy_X.Y.Z` hoy; V1 no introduce ese fallo ni lo “arregla” con UUID.
- Wave N+1: nuevo `waveNumber` → nuevo `BuilderSupplyBatchRef` → nuevos `canonical_strategy_id` aunque SQX reemita `Strategy_2.1.15`. Membership origin `PRODUCED`. Dedupe Campaign sigue `StrategyRef` first-observation-wins; no dedupe extra por `canonical_strategy_id`.
- Idempotency: `ResolveWave` persiste wave row antes del child; mint lee esa autoridad. ExactOutputName/publication path debe usar `BuilderSupplyBatchRef`, nunca `materialized.Wave`.

## Consecuencias

- AMENDMENT al CHALLENGE de [[2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1]]: mint REQUIRED permanece; el token de mint es `BuilderSupplyBatchRef` (`{CampaignRef}_g{NNNNNN}_`), no prefix `wNNNNNN_`.
- Tests: R2/R11/R13 se reinterpretan con supply-batch mint. R11: same ResultsGroup across waves without namespace → REPROCESSED (test negativo del defecto); with namespace → PRODUCED distinct StrategyRefs. Nuevo R2b: retry same wave → same StrategyRefs. Nuevo R2c: identity invariant frente a WorkflowID/RunID/host/attempt. R7/R12 intactos. No R extra de contenido SHA.
- FIX CONTRACT NORMAL: mismo `ECHO_FORGE_CAMPAIGN_REPLENISHMENT_RESUME_POLICY_V1`. (a) cap `max_builder_candidates_per_wave`; (b) child `Input` vacío + `ConfigSourceWave=base.Wave`; (c) post-Builder cap fail-closed; (d) **mint por BuilderSupplyBatchRef en publicación Builder Campaign**, no WaveKey; (e) tests R1–R14 + R2b/R2c.
- Files ≤14: `sqx/core/domain/forge_campaign.go`+test (BuilderSupplyBatchRef); `sqx/core/runtime/config.go`+test (cap); postgres `forge_campaign.go` + migration `013` (cap/guard, batch derivable sin columna si se prefiere KISS); `forge_campaign_activity.go`+test; `sqx/adapters/mt5/binding/intake.go`+test (inyectar batch al child, no al WaveKey); publicación `steps.go` y/o `minio_storage.go`+test; `forge_campaign_workflow_test.go`. Si ExactOutputName exige archivo extra: split técnico Campaign contract vs Builder publication mint.
- Migration: YES para cap/ReplenishmentPolicy guard. NO para `CanonicalStrategyID()`, unique v2, ni backfill de strategies. No SDK entity nueva.
- Product Ready de fábrica queryable: sí después del NORMAL, ahora sin colapsar supply nuevo a REPROCESSED.
- NEXT EXACT: `ECHO-FORGE-CAMPAIGN-REPLENISHMENT-RESUME-POLICY-V1-NORMAL`.

## Alternativas descartadas

- OPTION A — prefix execution Wave `wNNNNNN_`: resuelve colisión numérica pero convierte identity en execution-scoped. REJECT.
- OPTION C — GUID SQX nativo: no existe. `ResultsGroup.getName()` / `strategy_id` Overview = cohort token. REJECT.
- OPTION D — identity por contenido/SHA: v2 lo dejó en hook v3; bytes no canónicos; metadata incidental. REJECT. No raw artifact SHA.
- OPTION E pura (seed SQX): no hay RandomSeed en CFX Builder; genetic-evolution no garantiza nombres distintos ni retry-stable. REJECT como autoridad sola; la publicación namespaced (B+E) es el contrato KISS.
- Prefix sólo `gNNNNNN_` sin CampaignRef: dos Campaigns del mismo program colisionan. REJECT.
- UUID random en workflow: viola idempotencia de redelivery. FORBIDDEN.
- Reabrir Identity v2 / semantic digest / StrategyVariant. FORBIDDEN.
