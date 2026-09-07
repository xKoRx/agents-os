---
type: decision
schema_version: 1
scope: application
created: "2026-08-15"
updated: "2026-08-15"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
related:
  - "[[2026-08-15-mt5-html-parser-fail-open-signed-costs]]"
aliases:
  - Echo Forge G0-L approved amendments
  - Echo Forge logical model owner decision
confidence: verified
source_session: owner-confirmation-2026-08-15
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - app/echo-forge
  - application/echoforge
  - area/echo
  - project/echo-forge
  - tech/symphony
---

# Decision: Echo Forge G0-L aprobado con amendments del owner

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- La revisión challenge-first definió el modelo lógico transversal y dejó G0-L pendiente de owner.
- El owner aprobó el modelo con cuatro correcciones vinculantes y reemplazó el gate de medición previa por un diseño físico MVP seguido de validación real.

## Decisión

1. Reutilizar `logical_type` como atributo estructural estable, versionado e indexable de identidad descriptiva; no renombrarlo ni inferir que pertenece a la PK física.
2. Modelar FlowRun↔Strategy N:M mediante origin + participation: una Strategy tiene un FlowRun de origen y puede reutilizarse/reprocesarse en otros sin duplicarse.
3. Mantener Evaluation immutable: MetricSet y TradeSet referencian `evaluation_ref`; Evaluation no posee arrays autoritativos mutables de children.
4. Persistir RankingSnapshot cuando una policy necesita cohorte/orden, manteniendo abierto el storage físico de entries.
5. Cerrar `G0-L = APPROVED_BY_OWNER`; convertir G0-P en diseño físico MVP y mover medición real a `G2-REAL-WORKLOAD` después de waves shadow.

## Rationale

- `StrategyMetadata.LogicalType`, `BuildSignature` y ranking ya materializan la semántica de agrupación; otra abstracción sería duplicación estética.
- Origin y participaciones posteriores responden queries distintas y evitan confundir reuse con nueva identidad.
- La dirección children→Evaluation permite recalcular MetricSets desde TradeSet sin mutar evidence de ejecución.
- Exigir métricas del sistema todavía inexistente para autorizar su diseño crea una dependencia circular; assumptions explícitas permiten construir y G2 permite corregir.

## Consecuencias

- [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] es la fuente operativa del contrato y debe usar fases A0–A5 con capacidad TOP/NORMAL explícita.
- [[Echo Forge - Reconciliación y Scoring MT5]] consume el binding y usa fases M0–M7; writers esperan G1-MT5, mientras corpus/parser pueden avanzar.
- Reabrir G0-L exige evidencia concreta de implementación, contradicción funcional, impacto real y contrapropuesta compatible.

## Alternativas descartadas

- Renombrar `logical_type` por una abstracción arquitectónica nueva.
- Mantener origen solo como atributo implícito o reducir FlowRun→Strategy a 1:N global.
- Mantener índices bidireccionales autoritativos Evaluation↔MetricSet/TradeSet.
- Fijar entries embedded/bounded antes del diseño físico.
- Bloquear G0-P esperando p95/p99, cardinalidades o index utilization del sistema futuro.
