---
type: known_error
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-c3-recertification-summary]]"
  - "[[2026-09-04-echo-forge-c3-zero-supply-closure]]"
  - "[[2026-09-04-echo-forge-c3-zero-supply-control-flow]]"
aliases: []
confidence: high
source_session: "[[2026-09-04-echo-forge-c3-recertification-summary]]"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# CERT-A sin survivor de Final Reretester

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- En una wave lean, WFM puede terminar `verdict=FAIL / reason=SEVERE_WARNING`; la cohorte `StrategyArtifacts` queda vacía y la CERT-A no puede alcanzar finalist.

## Causa

- No hubo fallo de build MT5 ni de parser: el `GenericSQXWorkflow` terminó antes de crear stage/child de Final Reretester, con el guard `final reretester requires a non-empty StrategyArtifacts cohort`.

## Impacto

- C3 permanece `BLOCKED / CLOSED`; no se crea CERT-B, no se fabrica candidate/finalist y no se redelivera la identidad fallida.

## Detección

- Lectura verificada por `CampaignRef` exacto: `FAILED / WAVE_FLOW_RUN_FAILED`, `waves_started=1`, `effective_unique_finalists=0`. WFM durable: 55 resultados; optimizer: 1 survivor físico; no Final Reretester/MT5.

## Mitigación

- No recertificar ni aceptar empty Final Reretester aislado. El burn-down TOP clasificó este síntoma como primer choke de [[2026-09-04-echo-forge-c3-zero-supply-control-flow]]. Corrección: sesión `ECHO-FORGE-C3-ZERO-SUPPLY-END-TO-END-CLOSURE-NORMAL` contra [[2026-09-04-echo-forge-c3-zero-supply-closure]].

## Evidencia

- Release `0.2.91` desplegada desde source authority `9641c9f`; CERT-A `097d17c2-d50d-48a4-aa08-3e3426092f1d`; Generic `sqx-main-v1-e064253f-3891-49e8-a26f-6073f4b0f401`; FlowRun `e1a964ac-99ee-48e8-87bf-e34638663735`; observación `2026-09-04`.
