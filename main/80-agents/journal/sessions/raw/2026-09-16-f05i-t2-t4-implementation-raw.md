---
type: raw_session
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Echo]]"
project: "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-09-16-f05i-t2-t4-implementation-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: [[ZCode]] / `builtin:zai-coding-plan/GLM-5.3-Flash`.
- Proyecto o entidad: [[Echo Forge — F-05-I Cohesive release and read surfaces]].
- Objetivo de la sesión: prompt maestro F-05-I T2–T4 — implementar read ports + adapters PG, funnel projection e InspectService en `xKoRx/symphony` sin infraestructura remota ni certificación física.

## Transcript

```
No se conserva el transcript completo del host. Contenido operativo reconstruible:

1. Bootstrap Agents OS (constitución, perfil, continuidad, INDEX) + retrieval de las 5 notas de contexto F-05-I.
2. Git: fetch origin; origin/feature/f04-magic-version-handoff == b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43; HEAD local 9fad768 detrás del baseline; branch codex/f05-release-prep creada desde el SHA exacto; dirty preexistente specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json preservado.
3. Recon: esquemas reales (migrations 001/011/015/016), ports existentes (forge_result_query, persistence, strategy_manifest_identity, magic_allocation), forge.Service y taxonomía de errores, harness postgrestest.
4. Implementación T2: sqx/core/capabilities/forge_inspect_query.go + 4 adapters registry-postgres (forge_campaign_list, stage_execution_list, flow_run_strategy_list, strategy_handoff_reads) con tests sqlmock + persistencia OpenIsolatedDB. Commit 7d073b3.
5. Correcciones de fixtures contra constraints reales: consistency_status NOT NULL, ck_stage_executions_durable_subject_ref (FLOW exige subject_ref), uq_strategy_version_identity, uq_handoff_manifest_binding, configs_pkey (contador global de UUIDs).
6. Implementación T3: sqx/core/forge/funnel.go ProjectFunnel pura + 9 tests. Commit 65c879a. Decisión: shape exacto de la SPEC (sin first_observed_at expuesto); participaciones recibidas por contrato frozen y documentadas como no-evidencia del funnel.
7. Implementación T4: sqx/core/forge/inspect.go InspectService (Strategy/RunStages/Campaigns) + 9 tests con fakes. Commit d77342d. Decisiones: port local MagicAllocationReader satisfecho por ControlPlane; namespace magic por wiring; presencia de flow run vía FlowRunResultReader para NOT_FOUND; check de identidad cruzada identity vs manifest → CONTRACT_INCONSISTENCY.
8. Validación: build paquetes afectados OK; gate enfocado adapters PASS (14.5s); forge+capabilities PASS; race PASS (adapters focused 118s); vet PASS; gofmt OK; git diff --check OK. NOT_RUN: build ./sqx/... falla sólo en sqx/tools (preexistente al baseline); suite completa registry-postgres no corrida (timeout preexistente documentado).
9. Agents OS: nota proyecto actualizada (tareas Done, estado, bitácora), change_log, agent_run, L0+L1. Sin feedback (sin fricción real del sistema). F-05-I NO cerrada.
```

## Evidencia externa

- Commits `7d073b3`, `65c879a`, `d77342d` en `xKoRx/symphony` branch `codex/f05-release-prep` (base `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`).
