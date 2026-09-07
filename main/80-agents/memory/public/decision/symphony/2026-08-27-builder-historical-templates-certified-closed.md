---
type: decision
schema_version: 1
scope: public
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-27-historical-cohort-resolution-at-group-boundary]]"
  - "[[2026-08-27-codex-unknown-sqx-cross-flowrun-builder-templates-e2e-normal]]"
aliases: []
confidence: verified
source_session: SQX-CROSS-FLOWRUN-BUILDER-TEMPLATES-E2E-NORMAL
load_policy:
indexable: true
index_priority: high
tags:
  - kind/decision
  - tech/sqx
  - tech/temporal
  - scope/public
---

# Builder histórico cross-FlowRun certificado

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- En el baseline `7d2199a55a844a1bf83c04c27a9fe9ebc0754587`, el Builder debe consumir un cohort histórico durable sin listar estrategias por legacy ni mutar el source.
- La corrida operacional se ejecutó con release `0.2.76`, source `02_retester` COMPLETED y 12 templates exactos.

## Decisión

- `BUILDER_HISTORICAL_TEMPLATES` queda `CERTIFIED_CLOSED`.
- La resolución ocurre exactamente una vez; los 12 miembros se registran como `REUSED/is_origin=false`; los 12 `StageInputs` canónicos son los pares exactos `template:StrategyRef → EvaluationRef`.
- CFX conserva un único binding Build `value="input"`; SQX observó `input (12)` antes del Build y produjo 20 outputs. Los outputs fueron 20 identidades canónicas nuevas `k0`, `PRODUCED/is_origin=true`, sin heredar StrategyRefs del template.

## Rationale

- La evidencia cruzada de Temporal, Postgres, Mongo, MinIO y logs SQX demuestra resolución, descarga física, consumo real, ownership de target, nuevas Evaluations y aislamiento/immutabilidad del source.

## Consecuencias

- El contrato histórico de Builder se considera cerrado para este alcance. Permanecen fuera de alcance: pre-007 backfill, Final Reretester direct sourcing, MinIO write-once físico, Retester recovery técnico, lineage individual template→candidate y Artifact Role=INPUT hardening.
- El siguiente track exacto es `SQX-CROSS-FLOWRUN-REUSE-FINAL-CLOSURE-TOP`.

## Alternativas descartadas

- No se modificó código, no se reutilizó el CFX compartido, no se copió template `.sqx` manualmente, no se usó reset Temporal y no se reabrieron contratos ya certificados.
