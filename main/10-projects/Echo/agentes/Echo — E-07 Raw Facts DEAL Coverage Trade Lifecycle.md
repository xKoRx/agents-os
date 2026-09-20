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
progress: 85
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
updated: "2026-09-20"
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

- **E07_IMPLEMENTATION_COMPLETE v1.0.0 + CORRECCIÓN MANAGER C1 (2026-09-20):** los 5 defectos/conflictos demostrados por la revisión de source quedaron tratados @ `a7a61875` (push FF `7c836619..a7a61875`, HEAD == origin). C1–C3 corregidos rojo→verde sobre PG 17.11 descartable (9 rojos exactos; `-race`; failing sets idénticos por nombre vs baseline sin/con PG: 4 y 55; harness 061→065 PASS). **C4 = STOP `E07_ORIGIN_IDENTITY_CONTRACT_CONFLICT`:** el protocolo pipe Reference V1 no porta `position_identifier` físico (sólo `reference_ticket`, prohibido por SPEC §5.1) ⇒ el emitter quedó fail-closed (`ErrOriginIdentityUnavailable`) SIN publicar hechos desde ese productor, con el flujo legacy intacto; entrega exacta (campo/productor/contrato/cambio mínimo) en VERIFICATION §8.2. **C5:** la receta `echo-trade-fact-ref.v1` no tiene autoridad S0 (exige opaque ref sin receta) y viaja a ratificación del Manager. **Aceptación Manager RETENIDA** (mandato: no declarar PG_PASS de Manager sin autoridad contractual en C4/C5); PHYSICAL_PENDING y FINAL_CLOSED=NO sin cambio. Siguiente acción única: decisión Manager sobre §8.2 + ratificación C5. Estado previo: E07_IMPLEMENTATION_COMPLETE v1.0.0 NORMAL (2026-09-19, @ `7c836619`, gates SOURCE/CONTRACT/PG PASS; evidencia VERIFICATION §1–§7 conservada).

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

- **2026-09-20 — Corrección Manager C1 ejecutada (una sesión autónoma):** defectos demostrados por revisión de source corregidos @ `a7a61875` (push FF desde `7c836619`). C1: `raw_payload` persiste los bytes ORIGINALES decodificados (no el texto base64); digest y payload contractual intactos. C2: `Service.RecoverPendingFact` — recuperación transaccional explícita (claim `FOR UPDATE SKIP LOCKED`, proyección completa + PROCESSED en la misma transacción, rollback ante fallo, replay/concurrencia idempotentes); el sweep ya no re-invoca el consumo ordinario (que convergía D1 sin proyectar y dejaba PENDING perpetuo); D1 ordinario intacto. C3: lookup de binding sobre la transacción y sólo para OPEN; fallo SQL ⇒ rollback + redelivery; ErrNoRows ⇒ UNKNOWN contractual; `UNKNOWN/LOOKUP_ERROR` commiteado eliminado. C4: sin `position_identifier` físico en el source del pipe Reference ⇒ emitter fail-closed sin publicar el ticket como origin_position_id; STOP `E07_ORIGIN_IDENTITY_CONTRACT_CONFLICT` entregado (VERIFICATION §8.2); flujo legacy intacto. C5: receta `echo-trade-fact-ref.v1` clasificada sin autoridad S0 → ratificación Manager. Evidencia: 9 rojos exactos → verde `-race`; failing sets idénticos por nombre (4 sin PG / 55 con PG vs `7c836619`==baseline); harness 061→065 PASS; go.mod/migraciones/S0 diff 0. Aceptación Manager RETENIDA hasta decisión C4 + ratificación C5.
- **2026-09-19 — NORMAL ejecutado (una sesión autónoma):** implementación completa WP0–WP7 / T00–T17 @ `7c836619` (push FF desde `59338a64`; base histórica `b66dc5ff` intacta). Gates: SOURCE (delta ⊆ autorizados, 39 archivos, go.mod delta 0, tokens 0), CONTRACT (dominio 13 tests + bridge `-race` PASS, MT-17/21–23 dual-publish byte-idéntico y legacy sin degradar), PG (19 tests stores + 8 consumer `-race` + harness `trade_facts_e7` PASS: interlock 064→065, up/down/up, matriz D1/C1–C4/D2/Q1, guardas lifecycle, REVOKEs, dedupe dual coverage) sobre PG 17.11 descartable. Failing set idéntico por nombre vs `b66dc5ff` sin y con PG (4 y 55 preexistentes; 0 nuevos). PHYSICAL_PENDING declarado con 5 deudas listadas (VERIFICATION §7.5). Migración 065 exclusiva E-07; cero ALTER a 001–064; cero Forge/Hasura/MQL; cero órdenes (consumer sin producer: replay sin dispatch estructural).
- **2026-09-19 — E-07 TOP planning one-shot:** SPEC/PLAN/TASKS/VERIFICATION/NORMAL-PROMPT v1.0.0 @ `59338a64` en `origin/feature/e07-raw-facts-deal-lifecycle` (docs-only; 4 archivos + prompt; base `b66dc5ff`; master intacto). Migración 065 reservada (exclusiva E-07). Worktree `/tmp/echo-e07-raw-facts-deal-lifecycle`. Gates CONTRACT/PG sin Forge; PHYSICAL diferido explícito. E-01…E-06 no reabiertos; E-06 T21 sigue blocked (G1 `PROMOTION_SEAL_MISSING`) sin cambio.

## 🧭 Decisiones

- Raw-before-route vive en **Core** (`echo-core`, consumer dedicado, mismo proceso que TradeJournalFn) — no Flink, no Gateway, no servicio nuevo (Live Authority §6 opción I; patrón T11 E-06).
- Reuse `echo.raw_trade_events` (029) con extensión aditiva; **no** segundo registro de trades.
- Atribución resuelta **al OPEN** con SELECT read-only de 064; pin write-once; sin re-resolución ni retro-atribución.
- Topics nuevos `echo.trade-facts.v1` / `echo.reference-coverage.v1` con Bridge dual-publish paralelo; legacy intacto.
- MQL/collector (emisión física de DEAL/coverage) **fuera** de E-07 V1: shapes por fixtures; PHYSICAL diferido.
- Mapeo V1 del envelope Bridge (derivación documentada en VERIFICATION §7.4): envelope porta `trade_id` + `origin_position_id` (§5.1 los exige y S0 no los tiene); `source_key` = `trade_id`; `fact_ref` = receta propia sobre ingredientes §5.1; `broker_server_ref` = broker de sesión Bridge y `platform` = UNKNOWN (el pipe no observa identidad física ⇒ atribución UNKNOWN honesta §6.3).
- Sin Hasura en E-07 (read surfaces E-13); sin EconomicCommand (E-08); cero órdenes.

## 🔗 Docs / Links

- `specs/FEAT-RAW-FACTS-DEAL-COVERAGE-LIFECYCLE-E7/` (SPEC/PLAN/TASKS/VERIFICATION/NORMAL-PROMPT) en `xKoRx/echo`.
- [[Echo — Live Platform V1]] · [[Echo — E-06 Reference Enrollment and Binding]] · [[Echo — Producto Integrado]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] (§6 autoridad de hechos)
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo + Echo Forge — Deferred Certification Backlog]]
