---
type: decision
schema_version: 1
scope: project
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-reretester-single-artifact-contract]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-RELEASE-0.2.89-CONTAIN-BLOCKED-CAMPAIGN-AND-C3-LEAN-RECERT-NORMAL
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-echo-forge-c3-lean-0289-blocked-reretester

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Corrección de autoridad C0: el primer `CancelWorkflow` se emitió contra namespace `sqx`, mientras la autoridad efectiva del watcher era `sqx-prop`; en `sqx-prop` la Campaign contaminada `592944e2-1a30-426c-93c6-ebba351dc786` quedó sin contener antes del rollout y posteriormente avanzó a una wave. Se detectó como `OLD_CAMPAIGN_ALREADY_ADVANCED`; no se ejecutará cancelación de child ni otra mutación.
- `0.2.89` fue publicada con `./deploy_release.sh --release-only 0.2.89`, con aislamiento de `input/example/config.json`; fleet 4/4 convergió. Las cuatro CFX efímeras pasaron autoridad byte-identical, `ValidateWorkflowSpec` y `ParseCFXConfiguredPeriod` (`2026-05-04..2026-06-05`).

## Decisión

- **VEREDICTO:** `ECHO_FORGE_CAMPAIGN_STOP_POLICY_V1_C3: BLOCKED / CLOSED`; C3 no queda físicamente certificada.
- **Hard gate C0 fallido:** en `sqx-prop`, la Campaign vieja ahora está `FAILED` con `waves=1`, FlowRun `c0bea232-cce6-42b4-8509-b01c1970a798` `FAILED`, child `sqx-main-v1-9090e773-f2aa-4f00-b6df-3651e774cd15`, RunID `01a06a56-0bb5-7d7d-bb10-52b1daa2f01d`; PG confirmó `finalists=0`, `stop_evaluations=0`. Esto invalida la secuencia C0→release y por sí solo cierra la misión.
- CERT-A nueva materializó exactamente una wave y un Generic child: CampaignRef `11741c54-e068-4e60-adf3-bc5ffecf680c`, token `87d1378f-edd9-4a5b-9e3f-8ece00733db6`, parent `sqx-forge-campaign-v1-87d1378f-edd9-4a5b-9e3f-8ece00733db6`, RunID `01a06a61-0120-7ae2-8b33-5971926037ec`.
- El child `sqx-main-v1-82543151-dc53-46fd-9c5b-51188f232713` terminó `FAILED` en `05_reretester` con `final reretester activity must return exactly one key and one StrategyArtifact`; PG selló `WAVE_FLOW_RUN_FAILED`, con 0 finalists, 0 FINALIST_PROMOTION y 0 stop evaluations.
- Se detuvo la misión: CERT-B, redelivery, verified reads terminales y replay matrix C3 no se ejecutaron. No hubo source patch, DB write, ranking/promotion injection, commit o push.

## Rationale

- La autoridad namespace incorrecta permitió que 0.2.89 recogiera la Campaign contaminada; además, el primer defecto de producto observable posterior fue la violación de cardinalidad en final reretester. Continuar ocultaría dos fallos de seguridad y produciría evidencia no certificable.

## Consecuencias

- La release y fleet quedan operativas, pero la certificación C3 permanece bloqueada por `OLD_CAMPAIGN_ALREADY_ADVANCED` y el fallo de reretester. El PG residue ya no es sólo pre-wave: la Campaign vieja tiene una wave fallida y no debe contarse como C3.
- Se preservan `CAMPAIGN_PARTIAL_PIPELINE_REUSE` (CAPABILITY GAP / OPTIONAL) y `MT5_COMPILE_RETRY_POLICY_AUTHORITY_DRIFT` (OPEN / NON-BLOCKING).

## Alternativas descartadas

- Iniciar CERT-B o redeliver A: descartado por hard gate.
- Parchear source, editar PG/MinIO o inyectar promoción: prohibido por la misión.
