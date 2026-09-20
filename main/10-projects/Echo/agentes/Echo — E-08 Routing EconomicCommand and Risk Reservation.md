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
start: 2026-09-20
due:
progress: 0
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-08
  - Routing EconomicCommand risk reservation
  - E-08 Routing
  - FEAT-ROUTING-ECONOMIC-COMMAND-RISK-RESERVATION-E8
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-20"
updated: "2026-09-20"
cssclasses:
  - wide
---

# Echo — E-08 Routing EconomicCommand and Risk Reservation

%% Naming: Echo — E-08 Routing EconomicCommand and Risk Reservation es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-08 Routing EconomicCommand and Risk Reservation
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-08 / Routing, EconomicCommand and risk reservation. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Persistir la decisión económica como hecho durable: universo expected/excluded congelado por decisión, EconomicCommand con identidad determinística, snapshot inmutable de policy/risk, reserva de presupuesto por cuenta conservada frente a crash y UNKNOWN, outbox idempotente y recovery sin reenvío ciego. Principios: `RAW_DURABLE_BEFORE_ROUTE` (gate E-07 §17.4); `UNKNOWN != ZERO`; raw fact ≠ economic command; replay de hechos ≠ replay de órdenes; Strategy ≠ Version ≠ RuntimeBinding. Sin optimizador de routing, sin multi-broker abstracto, sin netting. Unlock: denominador de routing + comando económico recuperable para E-09/E-12.

## 📊 Estado actual

- **E08_PLANNING_FROZEN v1.0.0 (2026-09-20):** SPEC/PLAN/TASKS/VERIFICATION + NORMAL-PROMPT @ `fe5c9de0` en branch `feature/e08-routing-economic-command-risk-reservation` (base `3765f2ba` = HEAD E-07 C3; master `5dd998f1` intacto). Migración `066` reservada (exclusiva E-08; 066 libre verificada). Gate RAW-BEFORE-ROUTE como boundary RG-1…RG-6 (sólo hechos `PROCESSED` commiteados + pin OBSERVING válido; PublishSync ≠ commit durable; UNKNOWN/SHADOW/sin coverage jamás elegibilidad; replay jamás genera segundo comando; dispatch jamás adelanta al commit). CommandID determinístico resuelto por regla (`command_unique_key` UNIQUE + `content_digest`; UUIDv7 minteado una vez; misma key+digest ⇒ mismo comando; key+digest distinto ⇒ `COMMAND_CONFLICT` cuarentenado) — consume el defer de E-02 §1.0.1. Snapshot inmutable content-addressed de policy/sizing/SLTP/destination/delay/account/instrument/decision (fila mutable jamás es autoridad histórica). Reserva integrada al command con headroom serializado por cuenta (`SELECT … FOR UPDATE`), `UNKNOWN_HELD` sin auto-release. Outbox monotónico en la propia fila del comando; sweepers SKIP LOCKED; reconciliación sin reenvío. Separación frozen: clase A (persistencia/identidad, PG hoy, cero órdenes) / clase C (activación económica condicionada: wiring vivo + dispatcher + E2E; prerrequisitos E-07 PHYSICAL, E-06 G1/T21, MQL_COMPILE, corrección `EchoPersistence.mqh`, E-02 AC-18). No reabre E-01…E-07 ni el roadmap. Next = NORMAL (`NORMAL-PROMPT.md`).

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e08-routing-economic-command-risk-reservation` | `3765f2ba` (E-07 HEAD C3; master `5dd998f1` intacto) | `specs/FEAT-ROUTING-ECONOMIC-COMMAND-RISK-RESERVATION-E8/SPEC.md` v1.0.0 @ `fe5c9de0` | `.../PLAN.md` + `.../TASKS.md` + `.../VERIFICATION.md` + `.../NORMAL-PROMPT.md` | E08_PLANNING_FROZEN v1.0.0 · NORMAL PENDING · gates objetivo: SOURCE/CONTRACT/PG PASS + PHYSICAL_PENDING + ECONOMIC_ACTIVATION_PENDING + FINAL_CLOSED=NO |

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [ ] E-08 T00–T02: baseline + failing sets, dominio E-08, migración 066 + harness #owner/agent #type/dev #area/echo
> - [ ] E-08 T03–T07: stores snapshots/routing/comandos/reservas + RoutingGate RG-1…RG-4 #owner/agent #type/dev #area/echo
> - [ ] E-08 T08–T10: router durable (default OFF), sweepers recovery/reconciliation, driver + wiring apagado #owner/agent #type/dev #area/echo
> - [ ] E-08 T11–T14: matriz MT-01…MT-18, gates SOURCE/BWC, VERIFICATION con evidencia, handoff Manager #owner/agent #type/dev #area/echo

## 🗺️ Roadmap (padre)

- [[Echo — Live Platform V1]] § Roadmap → «E-08 Routing, EconomicCommand and risk reservation». Dependencias: E-07 identidad raw (interfaces verificadas @ `3765f2ba`, consumidas como base). Parallel: guards de E-12 en shadow (E-12 decides).
- Preservaciones: UNKNOWN ≠ ZERO · raw fact ≠ economic command · replay de hechos ≠ replay de órdenes · Strategy ≠ Version ≠ RuntimeBinding · routing legacy intacto en clase A/B.

## 📆 Bitácora

- **2026-09-20 — E-08 TOP planning one-shot:** SPEC/PLAN/TASKS/VERIFICATION + NORMAL-PROMPT v1.0.0 @ `fe5c9de0` en `origin/feature/e08-routing-economic-command-risk-reservation` (docs-only; base `3765f2ba` E-07 C3; master intacto `5dd998f1`). Baseline resuelto contra repos reales (ramas E-06 `b66dc5ff` / E-07 `3765f2ba` local=origin; migración 066 libre). Diseño frozen: gate RG-1…RG-6 sobre E-07 §17.4; identidad comando por `command_unique_key`+`content_digest` (UUIDv7 mint once; resuelve defer E-02); snapshots content-addressed inmutables; reservas con lock por cuenta y `UNKNOWN_HELD` conservador; outbox monotónico con claims SKIP LOCKED; errores permanentes/transitorios/desconocidos con fail-closed; recovery sin resend ciego; reconciliación como superficie para E-09. Separación clase A (desarrollable hoy, cero órdenes) vs clase C (activación condicionada, prerrequisitos declarados). Worktree `/tmp/echo-e08-routing-economic-command-risk-reservation`. E-01…E-07 no reabiertos; defecto `EchoPersistence.mqh` intocado (carril Manager). Next = NORMAL.

## 🧭 Decisiones

- Boundary RAW-BEFORE-ROUTE es **gate estructural** (`RoutingGate` SELECT transaccional RG-1…RG-4 + RG-5/RG-6 por diseño transaccional): la única prueba de aceptación durable es la fila `echo.raw_trade_events` con `processing_status='PROCESSED'` commiteada (E-07 §17.4); Kafka/coordenadas jamás prueban durabilidad.
- CommandID determinístico **por regla, no por UUID**: `UNIQUE(command_unique_key)` + `content_digest`; mismo key+digest ⇒ mismo comando (`REPLAY_CONVERGED`); key+digest distinto ⇒ `COMMAND_CONFLICT` cuarentenado; UUIDv7 se mintea una vez y jamás se remintea (Live Authority §7 + invariante 12; defer E-02 consumido).
- Snapshots inmutables **content-addressed con contenido embebido**: las filas mutables de catálogo se leen UNA vez con marca de revisión; los valores aplicados viajan embebidos; policy mutation posterior no toca histórico (invariante 16).
- Reserva **integrada al comando** (sin servicio de riesgo distribuido): lock de fila de presupuesto por cuenta serializa OPENs concurrentes; `UNKNOWN_HELD` jamás auto-release; reconciliación (superficie para E-09) resuelve con evidencia.
- Outbox **es la fila del comando** (sin tabla outbox separada): estados monotónicos protegidos; dispatch sólo de `READY` commiteada; el dispatcher real es clase C y no existe en el delta NORMAL.
- Activación económica **separada** del desarrollo: clase A/B PG con cero órdenes; clase C (router vivo + dispatcher + CLOSE durable + E2E) requiere prerrequisitos externos y decisión Manager/owner; router default OFF fail-closed.

## 🔗 Docs / Links

- `specs/FEAT-ROUTING-ECONOMIC-COMMAND-RISK-RESERVATION-E8/` (SPEC/PLAN/TASKS/VERIFICATION/NORMAL-PROMPT) en `xKoRx/echo`.
- [[Echo — Live Platform V1]] · [[Echo — E-07 Raw Facts DEAL Coverage Trade Lifecycle]] · [[Echo — E-06 Reference Enrollment and Binding]] · [[Echo — E-02 Control Safety, Auth and Journal Recovery]] · [[Echo — Producto Integrado]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] (§§7–8 autoridad de routing/comandos; invariante 16/17/18)
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo + Echo Forge — Deferred Certification Backlog]]
