---
type: change_log
schema_version: 1
scope: session
created: "2026-08-21"
updated: "2026-08-21"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[Echo Forge]]"
related:
  - "[[2026-08-19-echo-forge-a6-big-bang-supersedes-a5]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-21-echo-forge-sparse-checkout-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge classification evidence TOP blocked

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):** repo `xKoRx/symphony` commit `4125800f432b72d1de071e5b19e0a028da45a571`; `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`

## Motivo

Se cerró el TOP de evidencia durable de clasificación solicitado para desbloquear ranking per-logical-type sin convertir `StrategyMetadata.LogicalType`, `UpdateStrategiesLogicalType` ni `type_rankings.logical_type` en autoridad.

## Fuentes usadas

- `sqx/activities/worker/classify_and_rank.go`, `sqx/core/classification/`, domain metadata, capabilities metadata store, Mongo brownfield contracts, Builder overview binding/evidence, StrategyArtifact, example config y RankingSnapshot TOP/SPEC en baseline `ffa33545be88d00306ffcb0c6104206d9c6e70b7`.

## Resolución aplicada

Se congeló `ClassificationSnapshot` de cohorte, `indicator_signature.v1@1.0.0`, logical type canónico, identidad Foundation, Mongo `classification_snapshots`, carrier batch-level y consumo exact-ref por ranking per-type. El resultado queda `BLOCKED_BY_UPSTREAM_EVIDENCE`: Builder debe persistir los tres arrays estructurales en payload immutable cubierto por digest antes de autorizar Classification NORMAL.

## Validación

Símbolos referenciados verificados; docs consistentes; `git diff --cached --check` PASS; push PASS; `HEAD == origin/master == 4125800f432b72d1de071e5b19e0a028da45a571`; tres foreign dirty preservados; Graphify no ejecutado por scope explícito.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

Revertir el commit `4125800f432b72d1de071e5b19e0a028da45a571` en Symphony y retirar sólo el checkpoint CLASSIFICATION-EVIDENCE-TOP append-only si el owner invalida este contrato; no modificar los cierres RankingSnapshot ya publicados.
