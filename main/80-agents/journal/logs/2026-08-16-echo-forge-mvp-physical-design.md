---
type: change_log
schema_version: 1
scope: session
created: "2026-08-16"
updated: "2026-08-16"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
related:
  - "[[2026-08-16-echo-forge-g0p-mvp-physical-design]]"
  - "[[2026-08-16-echo-forge-physical-design-session-feedback]]"
  - "[[2026-08-16-codex-unknown-echo-forge-mvp-physical-design]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-16-echo-forge-physical-design-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge — Diseño físico MVP G0-P

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Reconciliación y Scoring MT5.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - `80-agents/memory/public/decision/symphony/2026-08-16-echo-forge-g0p-mvp-physical-design.md`

## Motivo

- Corregir un cierre inválido de A1, completar una forma física realmente implementable, sincronizar gates/tareas/proyectos y dejar continuidad verificable para foundation y MT5.

## Fuentes usadas

- Modelo lógico y `Strategy-MT5 Binding v1` aprobados en [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]].
- Checkout `xKoRx/symphony` en `b5c71d5`, incluyendo `GenericSQXWorkflow`, `sqx.strategies`, `strategy_evaluations`, `trade_lists`, `mt5_backtest_results`, `type_rankings` y ArtifactRef.
- Checkout separado `xKoRx/sdk` en `0751c47`, inspeccionado solo para delimitar contrato público; sus cambios locales preexistentes se preservaron y no se modificó el repo.

## Resolución aplicada

- La primera marca `CLOSED` se revirtió temporalmente al comprobar que faltaban frontera SDK/Core/adapter y recovery suficiente; esa versión queda supersedida.
- `A1 — PHYSICAL MODEL v1` fija tabla maestra; UUID + intent keys para control; refs SHA-256 deterministas para evidence; cuatro tablas/relaciones de control nuevas; cuatro collections Mongo inmutables; TradeSet externalizado; ArtifactRef completo; shapes, constraints, índices, packages, assumptions y matriz final de once casos de recovery.
- RankingSnapshot/Decision quedan fuera de G1-MT5/M4; `type_rankings` y decisiones legacy no cambian. Los contratos nuevos quedan en Core/adapters Symphony y SDK permanece sin cambios.
- Los amendments finales owner cierran: formulas StageExecution con unique por generation; `flow_intent_token` atestado; Mongo `majority+journal` + recovery `majority/primary`; imported origin mediante `is_origin`; y rollback bloqueado hasta cero projection gaps.
- Se corrigieron 9 residuos current-state anteriores al blueprint: StageExecution físico, FlowRun UUID, origin/import, `logical_type`/PK, fila Strategy/veredicto, mutabilidad Strategy, Temporal first-run, contrato FlowRunStrategy y storage ranking marcado `FUERA_G1`. Ocurrencias históricas y el role funcional `candidate` se conservaron y clasificaron.
- Limpieza final `ARCHITECTURE FREEZE`: `flow_intent_token` queda globalmente unique con conflicto cross-config, se eliminó el último texto stale `PRODUCED`-only/`IMPORTED` posterior, se sanearon enums con pipes dentro de tablas Markdown y se revalidó A0/A1 Done con `progress=47`.
- La decisión reusable quedó promovida en [[2026-08-16-echo-forge-g0p-mvp-physical-design]]; el proyecto conserva el detalle implementable y el ADR conserva rationale/alternativas.
- `G0-P` y `G1-MT5` quedaron cerrados; A1.1–A1.5 quedaron Done. El próximo paso transversal es A2-TOP y el vertical continúa M0N.2–M0N.3 antes de adoptar M4.
- El progreso se recalculó contra tareas cerradas: Arquitectura `7/15 = 47%`, MT5 `1/16 = 6%` y Echo Forge `14/34 = 41%`; WIP/Review no se contaron como Done.

## Validación

- Contrato de schema: PASS; lint estricto de los siete artefactos de sesión: `ERROR=0 WARN=0`; tag lint de los cuatro artefactos canónicos proyecto/ADR: `errors=0`.
- Conformance G1-MT5 final: 19/19 invariantes PASS, incluidos los seis amendments explícitos; checkout Symphony `b5c71d5` limpio y sin cambios productivos. SDK no se modificó; sus cambios preexistentes permanecen fuera del alcance.
- Graphify: `DEGRADED`. El único intento de esta corrección final completó AST `4.630/4.630`, quedó 30 segundos adicionales sin output en `_disambiguate_colliding_node_ids` y se interrumpió de forma controlada; no se reintentó. El índice anterior sigue consultable y Markdown/lint permanecen autoritativos, por lo que no bloquea el cierre documental.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sí; no se persistieron credenciales, paths absolutos ni dumps.

## Rollback

- `SQX_PERSISTENCE_MODEL=legacy` detiene writers/readers v1 sin borrar datos. Las migrations son aditivas y las colecciones brownfield permanecen intactas; esta entrada conserva además la trazabilidad del cierre inicial invalidado y su corrección.
