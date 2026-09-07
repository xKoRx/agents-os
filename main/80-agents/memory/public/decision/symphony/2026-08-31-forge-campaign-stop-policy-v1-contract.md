---
type: decision
schema_version: 1
scope: project
created: "2026-08-31"
updated: "2026-08-31"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application:
entities: []
related:
  - "[[2026-08-30-finalist-promotion-v1-core]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-CAMPAIGN-STOP-POLICY-V1-CONTRACT-TOP"
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
---

# Forge Campaign Stop Policy V1 Contract

## Contexto

- Baseline auditado: `xKoRx/symphony@9c90a2f75108c729eaee6a0906eb9b057f3af970` sobre `master`. El pipeline productivo es `GenericSQXWorkflow`; el `CampaignEngine` existente pertenece a Maintenance/ProActiva y Adaptive está deprecated.
- El gap vigente es que cada intake crea un solo FlowRun y no existe una autoridad durable que lance waves adicionales cuando la promoción produce menos finalists únicos que el objetivo.

## Decisión

- La entidad nueva se llama `ForgeCampaign`. Su identidad es `base_config_id + ForgeCampaignIntentToken`; `CampaignRef` y el token son UUID persistidos, mientras RequestID sólo permite recuperar la misma intención en intake. Policy y snapshot son guards inmutables, no componentes de identidad.
- PostgreSQL es la autoridad mediante `sqx.forge_campaigns`, `sqx.forge_campaign_waves`, `sqx.forge_campaign_finalists` y `sqx.forge_campaign_stop_evaluations`; cada wave mapea exactamente a un FlowRun y cada evaluación se escribe una sola vez.
- `ForgeCampaignWorkflow` orquesta child workflows completos `GenericSQXWorkflow`. Cada child conserva un FlowRun normal, un FlowIntentToken propio y un config snapshot inmutable. No se reconstruyen stages ni se usa Adaptive.
- Stop Policy V1 contiene exactamente `target_finalists` y `max_waves`, ambos obligatorios. Tras cada FlowRun COMPLETED se carga la única Decision `FINALIST_PROMOTION`, se deduplica por `StrategyRef` con first-observation-wins y se evalúa en precedencia `TARGET_REACHED`, `MAX_WAVES_REACHED`, `CONTINUE`.
- `max_waves` admite `1..100`; una wave durable consume el bound aunque su FlowRun falle, pero retry de la misma wave no. FlowRun FAILED/CANCELLED, Promotion ausente/inconsistente o conflicto durable fallan cerrado la ForgeCampaign.
- `COMPLETED` representa tanto target alcanzado como hard stop por máximo de waves; `FAILED` y `CANCELLED` no son business stop. Timestamps son informativos y terminal state es inmutable por CAS.
- La entrada productiva mínima extiende `WorkflowSpec` con `forge_campaign:{schema,target_finalists,max_waves}`. Si está ausente, el watcher mantiene el one-shot actual; si está presente, resuelve y despacha la ForgeCampaign.

## Rationale

- Las Promotion Decisions exactas ya son la autoridad congelada de finalists y PostgreSQL ya es el control plane durable; una entidad aggregate separada evita convertir un FlowRun o una Decision stage-bound en una campaña multi-run.
- Un parent Temporal mantiene la autonomía y el replay determinista sin introducir I/O en workflow code. El bound de 100 child workflows hace innecesario Continue-As-New en V1.
- El source rutea `config.cfx` por `Spec.Wave`; waves nuevas no pueden reutilizar físicamente el config base sin una ruta separada. V1 agrega `config_source_wave`, generado internamente e inmutable, para descargar el `.cfx` original mientras `Spec.Wave` y `WaveConfig.WaveKey` identifican la wave nueva.

## Consecuencias

- Migration siguiente: `011_forge_campaign_stop_policy.up.sql` con cuatro tablas, constraints de identidad/lifecycle/precedencia y transacciones atómicas para resolver wave y sellar evaluación.
- Campaign target no reutiliza `WaveConfig.TargetTops`; ese campo sólo tiene semántica Adaptive en el baseline. Pool exhaustion, compute/candidate budget, adaptive batch sizing, duration y gates de calidad MT5 quedan fuera de V1.
- La implementación se divide en C1 Foundation, C2 Orchestration y C3 Intake/Certification, cada slice bajo 14 archivos. El siguiente exacto es `ECHO-FORGE-CAMPAIGN-STOP-POLICY-V1-C1-FOUNDATION-NORMAL`.

## Alternativas descartadas

- Reutilizar `capabilities.Campaign`, `CampaignEngine`, ETCD, `StateStore`, Adaptive, RankingSnapshot directamente, Mongo latest, timestamps, canonical strategy ID o generic Decision para el aggregate.
- Inferir `INSUFFICIENT_SUPPLY` desde 0 finalists o waves vacías, usar `mt5-final-fidelity-ranking` como gate de Strategy Quality, o inventar counters de Builder/compute sin autoridad durable.
- Copiar `config.cfx` para cada wave, usar Temporal history como única persistencia, generar CampaignRef desde RequestID o permitir que implementación elija stop precedence.
