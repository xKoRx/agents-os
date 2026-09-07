---
type: change_log
schema_version: 1
scope: session
created: "2026-08-16"
updated: "2026-08-16"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
  - "[[Echo Forge]]"
related:
  - "[[2026-08-16-echo-forge-a2-foundation-closed]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge MT5 — M0 completo + M1 SDDs + M2T PLAN

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created (repo) + updated (vault)
- **Archivo(s):**
  - Repo `xKoRx/symphony` @ `0b96e63`: `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/` (CORPUS, INVENTORY, METRIC-MATRIX, SPEC-PARSER, SPEC-NORMALIZATION, PLAN, fixtures ×2) + fila en `specs/SPECS.md`
  - Vault: notas de proyecto [[Echo Forge - Reconciliación y Scoring MT5]] y padre [[Echo Forge]] (tareas/estado/bitácora/progress 6→38)

## Motivo

- Ejecutar M0N.2, M0N.3, M0T.1, M1.1 y M2T.1 del proyecto MT5 (pedido explícito del owner: avanzar hasta M2-TOP).

## Fuentes usadas

- Binding y A1 PHYSICAL MODEL v1 de [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]; tipos domain de la Foundation A2 (`8336122`).
- Fixtures reales: `mt5-export.htm` (trackeado), evidence zero-trade de `FEAT-SQX-MT5-PIPELINE-ARTIFACTS`, y 2 HTM de `example_flow_4` hallados en `~/Downloads` (copiados al repo; ambos zero-trade pre-hotfix).
- Código: `sqx/adapters/mt5/parser.go` (legacy fail-open), `sqx/core/evaluation/{catalog_core,risk_adjusted_delta,comparison}.go`.

## Resolución aplicada

- Corpus de 4 fixtures build 6090 con checksums/provenance/expectativas; gaps mixed y locale/build quedan como aporte owner sin bloquear M3.
- Inventario mecánico campo HTM→typed con gramáticas de formatos compuestos y crosschecks (`-441.40 + -63.15 + 0 = -504.55` verificado contra totales y balance).
- Matriz semántica: `net_profit` COMPARABLE; DD/PF/win_rate/expectancy COMPARABLE_CONDICIONAL (basis SQX a verificar en M5); `ret_dd/sharpe/sqn/stagnation` NO_COMPARABLE_V1; `risk_adjusted_delta.v1` no reutilizable (predicado same-stage); proposal `mt5_validation_delta.v1` PENDING_OWNER; `FEAT-SQX-DEVIATION-FILTER` declarado consumidor enforce futuro para evitar drift.
- SDDs parser y normalización fail-closed sin persistencia; PLAN slices 1–6 (M3→M6) con rollback y gates.
- Proyecto queda con próximo paso exacto M2N.1; tarea puente permanece WIP (el proyecto continúa).
