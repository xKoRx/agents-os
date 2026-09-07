---
type: decision
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application:
entities:
  - "[[Echo Forge]]"
related:
  - "[[Campaign Stop Policy]]"
aliases: []
confidence: verified
source_session: "[[2026-09-04-echo-forge-c3-final-recert-summary]]"
load_policy: always
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-release-0-2-92-physical-c3-closure

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- La implementación `ZERO_SUPPLY_CONTROL_FLOW_CLOSURE` ya estaba cerrada determinísticamente en `93c66651251edefcc65ef183ac9f7b832b4de5de`; esta sesión debía publicar `0.2.92` y ejecutar una sola Campaign física nueva.
- La certificación física produjo Branch A con supply real; no se usó producción para redescubrir T1–T12 ni se creó una segunda Campaign.

## Decisión

- Congelar `ECHO_FORGE_CAMPAIGN_STOP_POLICY_V1` como `PHYSICALLY_CERTIFIED / FROZEN` y cerrar `ZERO_SUPPLY_CONTROL_FLOW_CLOSURE` como `PHYSICALLY_CERTIFIED / CLOSED`; C3 queda `PASS / CLOSED`.
- La prueba física válida es una convergencia real de una sola Campaign: release exacta `0.2.92`, fleet 4/4, Campaign `a9e73e66-5062-44d7-b665-22740383c676`, FlowRun `4f135030-ad0c-4b41-9e32-f2f8c466c50b`, Branch A `TARGET_REACHED`, wave única y redelivery exacta idempotente.

## Rationale

- Supply es un outcome físico, no una precondición de C3; una futura certificación zero-supply también sería PASS si materializa Promotion empty válida y `MAX_WAVES_REACHED`.
- La evidencia durable y la superficie de resultado coincidieron: RankingSnapshot exacto `sha256:8061dda6a4d8faedb331cadd5ebc92c320d1d6d2470f9b131729bdaadcd24f2f`, Promotion exacta, un finalist y precedencia de `TARGET_REACHED`.

## Consecuencias

- No iniciar automáticamente Builder Budget, Campaign Replenishment ni A0 Live Validation; el siguiente paso exacto es `RETURN_TO_LEAD_AFTER_C3`.
- Campaigns históricas y sus graph edges stale permanecen documentadas e inmutables; no se redeliveran, cancelan, reparan ni reutilizan.

## Alternativas descartadas

- No se repitió la Campaign para forzar zero-supply o una rama distinta y no se modificaron thresholds, estrategia ni configuración durante la ejecución.
