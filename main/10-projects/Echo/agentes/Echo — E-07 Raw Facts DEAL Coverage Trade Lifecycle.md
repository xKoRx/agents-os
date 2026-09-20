---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo — Live Platform V1]]"
sprint:
start: 2026-09-19
due:
progress: 10
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-07
  - Raw facts DEAL coverage trade lifecycle
  - E-07 Raw Facts
  - FEAT-RAW-FACTS-DEAL-COVERAGE-LIFECYCLE-E7
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-19"
updated: "2026-09-19"
cssclasses:
  - wide
---

# Echo — E-07 Raw Facts DEAL Coverage Trade Lifecycle

%% Naming: Echo — E-07 Raw Facts DEAL Coverage Trade Lifecycle es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-07 Raw Facts DEAL Coverage Trade Lifecycle
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-07 / Raw facts, DEAL, coverage and trade lifecycle. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Persistir hechos raw inmutables **antes** de routing, el DEAL económico irreducible, el lifecycle OPEN/MODIFY/CLOSE y la cobertura que distingue observación válida, silencio válido y UNKNOWN. Principios: `RAW_DURABLE_BEFORE_ROUTE`; `UNKNOWN != ZERO`; `DEAL != JOURNAL`; Version pineada al OPEN; replay sin dispatch. Unlock: hechos recuperables y coverage honesta para E-08/E-09/E-10.

## 📊 Estado actual

- **E07_PLANNING_FROZEN v1.0.0 (2026-09-19, TOP planning one-shot; docs-only, cero código E-07).** SPEC/PLAN/TASKS/VERIFICATION + NORMAL-PROMPT en `specs/FEAT-RAW-FACTS-DEAL-COVERAGE-LIFECYCLE-E7/` @ branch `feature/e07-raw-facts-deal-lifecycle` (commits `0091af43` planning + `59338a64` prompt; push FF desde `b66dc5ff` = HEAD de E-06). Baseline reconciliado sin drift: `origin/master` `5dd998f1` (igual al mandato) y E-06 `b66dc5ff` == origin. Interfaces verificadas en source: S0 `TradingFactV1`/`CoverageRecord` (READ ONLY), E-06 migration 064 (`binding_ref`, `coverage_started_at`, `accepts_opens_from/to`, `observation_class`), stores y patrón consumer T11 + fix messaging. Migración **065** reservada para E-07 (E-06 SPEC §16 dejó 065+ libre; exclusiva E-07, 066+ fuera). Diseño frozen: consumer dedicado en `echo-core` (raw-before-route, Live Authority §6 opción I), envelope Bridge paralelo (topics nuevos `echo.trade-facts.v1`/`echo.reference-coverage.v1`) sin tocar legacy, extensión aditiva de `echo.raw_trade_events` (029) sin ALTER a 001–064, atribución pineada al OPEN vía SELECT read-only de 064, matriz dedupe D1/C1–C4/D2/Q1 con quarantine. Estados: `IMPLEMENTATION_READY` vigente; gates CONTRACT/PG ejecutables con fixtures + PG descartable **sin Forge ni terminal**; `PHYSICAL_PENDING` declarado (productor MQL real, outage real, E-06 OBSERVING real — desacoplado por Manager 2026-09-19); `FINAL_CLOSED=NO`. **Siguiente acción única: lanzar NORMAL con `NORMAL-PROMPT.md`.**

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e07-raw-facts-deal-lifecycle` | `b66dc5ff` (E-06 HEAD; master `5dd998f1` intacto) | `specs/FEAT-RAW-FACTS-DEAL-COVERAGE-LIFECYCLE-E7/SPEC.md` v1.0.0 | `.../PLAN.md` + `.../TASKS.md` + `.../VERIFICATION.md` + `.../NORMAL-PROMPT.md` @ `59338a64` | E07_PLANNING_FROZEN v1.0.0 · NORMAL no lanzado |

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [ ] E-07 WP0–WP2: baseline, dominio (envelope+topics), migración 065 + harness #owner/agent #type/dev #area/echo
> - [ ] E-07 WP3–WP5: stores, emitter Bridge + hooks, consumer echo-core (ingesta/atribución/coverage/driver) #owner/agent #type/dev #area/echo
> - [ ] E-07 WP6–WP7: regresión BWC, SOURCE gates, VERIFICATION con evidencia y handoff Manager #owner/agent #type/dev #area/echo

## 🗺️ Roadmap (padre)

- [[Echo — Live Platform V1]] § Roadmap → «E-07 Raw facts, DEAL, coverage and trade lifecycle». Dependencias: E-06 (interfaces; source consumido), E-03 (identidad). Parallel: diseño E-08.
- Preservaciones: UNKNOWN ≠ ZERO · DEAL ≠ JOURNAL · Strategy ≠ Version ≠ RuntimeBinding · Strategy Quality ≠ Execution Fidelity · event time ≠ recorded time.

## 📆 Bitácora

- **2026-09-19 — E-07 TOP planning one-shot:** SPEC/PLAN/TASKS/VERIFICATION/NORMAL-PROMPT v1.0.0 @ `59338a64` en `origin/feature/e07-raw-facts-deal-lifecycle` (docs-only; 4 archivos + prompt; base `b66dc5ff`; master intacto). Migración 065 reservada (exclusiva E-07). Worktree `/tmp/echo-e07-raw-facts-deal-lifecycle`. Gates CONTRACT/PG sin Forge; PHYSICAL diferido explícito. E-01…E-06 no reabiertos; E-06 T21 sigue blocked (G1 `PROMOTION_SEAL_MISSING`) sin cambio.

## 🧭 Decisiones

- Raw-before-route vive en **Core** (`echo-core`, consumer dedicado, mismo proceso que TradeJournalFn) — no Flink, no Gateway, no servicio nuevo (Live Authority §6 opción I; patrón T11 E-06).
- Reuse `echo.raw_trade_events` (029) con extensión aditiva; **no** segundo registro de trades.
- Atribución resuelta **al OPEN** con SELECT read-only de 064; pin write-once; sin re-resolución ni retro-atribución.
- Topics nuevos `echo.trade-facts.v1` / `echo.reference-coverage.v1` con Bridge dual-publish paralelo; legacy intacto.
- MQL/collector (emisión física de DEAL/coverage) **fuera** de E-07 V1: shapes por fixtures; PHYSICAL diferido.
- Sin Hasura en E-07 (read surfaces E-13); sin EconomicCommand (E-08); cero órdenes.

## 🔗 Docs / Links

- `specs/FEAT-RAW-FACTS-DEAL-COVERAGE-LIFECYCLE-E7/` (SPEC/PLAN/TASKS/VERIFICATION/NORMAL-PROMPT) en `xKoRx/echo`.
- [[Echo — Live Platform V1]] · [[Echo — E-06 Reference Enrollment and Binding]] · [[Echo — Producto Integrado]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] (§6 autoridad de hechos)
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo + Echo Forge — Deferred Certification Backlog]]
