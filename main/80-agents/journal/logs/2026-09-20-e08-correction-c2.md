---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Aranea]]"
project: "[[Echo]]"
application:
entities:
  - "[[Echo]]"
related:
  - "[[aranea-agent-dev]]"
aliases:
  - "E-08 corrección C2 2026-09-20"
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/aranea
---

# 2026-09-20-e08-correction-c2

%% Mandato Manager «E-08 Manager Correction C2 — Identidad, coverage y replay determinístico»: cuatro defectos demostrados por revisión de source, corregidos con tests rojo→verde y gates completos sobre el worktree E-08. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):** repo `xKoRx/echo`, rama `feature/e08-routing-economic-command-risk-reservation` (push FF `53d42615..c2e88a0d`, 5 commits atómicos):
  - `v3/sdk/postgres/routing_gate.go` + `routing_gate_test.go` — C2-1 (clase de observación write-once: evidencia del raw jamás reemplazada; raw = resolución = CANONICAL), C2-2 (strategy_ref/canonical_strategy_id exigidos contra BindingResolution), C2-3 (RG-4.1 por intervalos concretos de `intervals` + contradicciones ⇒ COVERAGE_UNKNOWN, evidencia durable).
  - `v3/core/internal/econroute/router.go` — C2-2 (gate recibe identidad de estrategia) + payload DECISION con `coverage_evidence`/`resolved_observation_class` + `routing_input_schema=2` en ROUTING_INPUT (C2-4).
  - `v3/core/internal/econroute/universe.go` — C2-4 (candidateRevisionView congela magic override/offsets/delays; único constructor `revisionView`).
  - `v3/core/internal/econroute/recovery.go` — C2-4 (redrive fail-closed sobre snapshots sin freeze completo; reconstrucción completa sin defaults).
  - `specs/FEAT-ROUTING-ECONOMIC-COMMAND-RISK-RESERVATION-E8/{SPEC,VERIFICATION}.md` — ERRATUM C2 (§19) y registro §11 con evidencia y gates.
  - Vault: `10-projects/Echo/agentes/Echo — E-08 Routing EconomicCommand and Risk Reservation.md` (Estado actual + tabla de entrega + tarea C1/C2 marcada + bitácora 2026-09-20) y las notas de journal `80-agents/journal/agent-runs/2026-09-20-zcode-glm-5.3-flash-e08-correction-c2.md` y esta change_log (creadas).

## Motivo

- Corrección Manager C2 sobre E-08: `RoutingGate.Evaluate` sobrescribía la clase de observación del raw antes de comparar (un raw SHADOW con lookup CANONICAL quedaba elegible); `RouteRequest.StrategyRef`/`CanonicalStrategyID` no se validaban contra el binding vivo E-06; la consulta de coverage usaba extremos agregados con "latest wins" (huecos y contradicciones pasaban); el snapshot ROUTING_INPUT omitía cinco inputs económicos y el redrive reconstruía candidatos incompletos.

## Fuentes usadas

- SPEC E-08 v1.0.0 + ERRATUM C1 §18 (baseline `53d42615`), E-07 SPEC + ERRATUM-A (esquema `echo.reference_coverage`: `intervals` jsonb vs extremos agregados), Live Authority §§6–8, VERIFICATION §2 (failing set T00) y §10 (metodología C1), source/tests E-08 en el worktree.

## Resolución aplicada

- Cuatro correcciones quirúrgicas con rojo semántico demostrado por caso (reinyección del defecto / query vieja), commits atómicos `ea8b8fa1` (C2-1), `5c7a6b90` (C2-2), `3146c0ec` (C2-3), `9743bd60` (C2-4) y `c2e88a0d` (docs). Sin tocar 001–066, E-06, E-07, Forge, S0, master, legacy ni MQL; sin escritor de `economic_copy_authorizations`; sin dispatcher ni activación.

## Validación

- Suites `-race -count=1` por paquete (PG 17.11 portable descartable localhost:15432): domain ok, econroute ok, postgres failing set 53 nombres idéntico al T00 (diff por nombre vacío), etcd/telemetry fallos preexistentes de infra; harness 066 re-ejecutado: `economic_commands_e8: PASS`; vet/build PASS; delta = 7 archivos autorizados + docs; `git diff --check` limpio; COVERAGE_GATE_PENDING declarado con rutas exactas (VERIFICATION §11.4); HEAD == origin tras push FF.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Repo: `git revert c2e88a0d^..c2e88a0d` (o reset de la rama a `53d42615` y push forzado sólo con autorización del owner — los 5 commits son exclusivamente de esta corrección). Vault: eliminar las dos notas de journal creadas. Nada más: ninguna mutación productiva ni de esquema.
