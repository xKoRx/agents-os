---
type: decision
schema_version: 1
scope: project
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-09-02-echo-forge-c3-mt5-fidelity-period-mismatch]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-C3-PHYSICAL-BLOCKERS-RCA-TOP
load_policy: when_relevant
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# CERT-A supply via CFX-aligned MT5 tester window

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Campaign C3 CERT-A exige `FINALIST_PROMOTION` con `finalists >= 1`.
- Qualification `forge-c3-supply-20260902T0302Z-1B7C` y golden `c7eb6b3b-95ec-4088-aba5-2d5db6906e4c` producen TOP vacío por mismatch de periodo MT5 vs CFX.
- No existe Decision nonempty ni RankingSnapshot `mt5-final-fidelity-ranking` con `effective_top_n>0`.
- `builder-early-per-type` sí tiene tops nonempty, pero no es el ranking de Finalist Promotion.

## Decisión

- CERT-A conserva `source_ranking=mt5-final-fidelity-ranking`, `finalist_promotion@1.0.0`, `example_flow_23`.
- El único delta de config es alinear `mt5.from=2016.01.04` y `mt5.to=2026.06.05` con el periodo CFX del TradeSet.
- No rebind de ranking, no relajar predicates de fidelity, no Decision/score sintéticos.

## Rationale

- Los demás predicates de `MT5FidelityComparabilityReasons` ya PASS en los scores físicos; las métricas existen.
- Promotion proyectó vacío de forma contractual; el defecto es selección de ventana MT5, no ranking ni Promotion.

## Consecuencias

- El próximo ciclo de implementación puede incluir `input/example/config.json` junto al unregister Adaptive en `0.2.85`.
- CERT-A sigue requiriendo un run físico nuevo tras el align; no hay supply histórico nonempty reusable.
- Riesgo operativo: historia MT5 2016–2026 en Darwinex-Demo no está demostrada ni refutada.

## Alternativas descartadas

- Rebind promotion a `builder-early-per-type`: cheat de CERT-A.
- Quitar period predicates: viola fidelity congelada.
- Encoger CFX a julio 2026: cambia la cohorte SQX, no es un delta mínimo.
- Tratar FINAL-E2E Attempt 17 (`sha256:314f4344…`) como supply nonempty: el documento físico tiene `ordered=0`.
