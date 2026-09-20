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

- **E07_IMPLEMENTATION_COMPLETE v1.0.0 + CORRECCIÓN MANAGER C3 CONSUMIDA (2026-09-20):** defecto demostrado corregido @ `3765f2ba` (push FF `28213bbc..3765f2ba`, HEAD == origin). El CLOSE del productor MT5 alimentaba `HistorySelectByPosition` con el POSITION_TICKET (la API exige POSITION_IDENTIFIER; ambos pueden diferir) ⇒ `position_identifier` §17.1 podía quedar ausente incorrectamente y el origin key §5.1 del CLOSE divergía del OPEN. Fix: resolver `ResolvePositionIdentifier` (posición viva → `POSITION_IDENTIFIER`; relación durable historial `HistoryOrderSelect` → `ORDER_POSITION_ID`, posición cerrada OK; contradicción ⇒ 0 fail-closed §17.3) y `HistorySelectByPosition` exclusivamente con el identificador resuelto; `DEAL_POSITION_ID` de los deals sigue siendo la provenance (C4). Sitios: `SendTradeCloseImmediate`, `CheckForClosedOrders` (razón + precio/profit), guard `DetectCloseReasonFromDeals`; offline y reenvíos confluyen al mismo path. Contrato mínimo: sin extensión del binario `TradeMapper` (§10.6 E-03). Tests A–H rojo→verde (pines SOURCE MQL + espejo Go). Gates: SOURCE/CONTRACT PASS; PG SIN CAMBIO (delta sin impacto PG); **MQL_COMPILE_PENDING** (sin compilador real en el entorno). **Hallazgo sin retoque:** `EchoPersistence.mqh` repite el patrón en la detección de cierres offline (fuera del delta autorizado §17.1, compartido con execution_agent) — decisión Manager pendiente. Contrato: SPEC §17.6; evidencia: VERIFICATION §10. PHYSICAL_PENDING y FINAL_CLOSED=NO sin cambio; siguiente acción única: review Manager del delta C3 + decisión del hallazgo.
- **E07_IMPLEMENTATION_COMPLETE v1.0.0 + DECISIÓN MANAGER C2 CONSUMIDA (2026-09-20):** C4 y C5 quedaron implementados @ `28213bbc` (push FF `a7a61875..28213bbc`, HEAD == origin; commits atómicos `33730d4e` código + `28213bbc` erratum). **C4:** productor real resuelto EN el repo echo (`v3/clients/mt5/reference_v3.mq5`, `v3/clients/mt4/reference_v3.mq4`) ⇒ protocolo pipe **V1.1 aditivo** con identidad física auténtica (`position_identifier` OPEN=POSITION_IDENTIFIER / CLOSE=DEAL_POSITION_ID de la relación durable deal↔posición, posición cerrada OK; MT4: ticket = identificador durable; `account_server` = ACCOUNT_SERVER observado; `platform` atestada); Bridge en carril E-07 exclusivo publica SÓLO con identidad completa observada (`h.broker` jamás sustituye al ACCOUNT_SERVER; contradicciones/ausencias fail-closed sólo en E-07; legacy byte-idéntico). **C5:** receta `echo-trade-fact-ref.v1` FROZEN por el Manager (raw_payload_sha256 sobre bytes ORIGINALES; `fact_digest` §5.1 y `source_event_id` intactos). **Gate RAW-BEFORE-ROUTE registrado** (PublishSync ≠ commit durable PG; obligatorio para integración E-08). Gates: 5 rojos exactos @ `a7a61875` → verde; SOURCE/CONTRACT/PG PASS (harness 065 PASS PG 17.11 descartable; failing sets equivalentes por nombre apples-to-apples vs `a7a61875`, cero nombres E-07). Contrato: SPEC ERRATUM-A §17; evidencia: VERIFICATION §9. PHYSICAL_PENDING (falta emisión física real del EA enriquecido) y FINAL_CLOSED=NO sin cambio. Estado previo: E07_IMPLEMENTATION_COMPLETE v1.0.0 + CORRECCIÓN MANAGER C1 (2026-09-20) @ `a7a61875`: C1–C3 corregidos, C4 STOP `E07_ORIGIN_IDENTITY_CONTRACT_CONFLICT`, C5 a ratificación, aceptación RETENIDA. los 5 defectos/conflictos demostrados por la revisión de source quedaron tratados @ `a7a61875` (push FF `7c836619..a7a61875`, HEAD == origin). C1–C3 corregidos rojo→verde sobre PG 17.11 descartable (9 rojos exactos; `-race`; failing sets idénticos por nombre vs baseline sin/con PG: 4 y 55; harness 061→065 PASS). **C4 = STOP `E07_ORIGIN_IDENTITY_CONTRACT_CONFLICT`:** el protocolo pipe Reference V1 no porta `position_identifier` físico (sólo `reference_ticket`, prohibido por SPEC §5.1) ⇒ el emitter quedó fail-closed (`ErrOriginIdentityUnavailable`) SIN publicar hechos desde ese productor, con el flujo legacy intacto; entrega exacta (campo/productor/contrato/cambio mínimo) en VERIFICATION §8.2. **C5:** la receta `echo-trade-fact-ref.v1` no tiene autoridad S0 (exige opaque ref sin receta) y viaja a ratificación del Manager. **Aceptación Manager RETENIDA** (mandato: no declarar PG_PASS de Manager sin autoridad contractual en C4/C5); PHYSICAL_PENDING y FINAL_CLOSED=NO sin cambio. Siguiente acción única: decisión Manager sobre §8.2 + ratificación C5. Estado previo: E07_IMPLEMENTATION_COMPLETE v1.0.0 NORMAL (2026-09-19, @ `7c836619`, gates SOURCE/CONTRACT/PG PASS; evidencia VERIFICATION §1–§7 conservada).

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e07-raw-facts-deal-lifecycle` | `b66dc5ff` (E-06 HEAD; master `5dd998f1` intacto) | `specs/FEAT-RAW-FACTS-DEAL-COVERAGE-LIFECYCLE-E7/SPEC.md` v1.0.0 + ERRATUM-A §17 + §17.6 C3 @ `3765f2ba` | `.../PLAN.md` + `.../TASKS.md` + `.../VERIFICATION.md` (§1–§7 NORMAL + §8 C1 + §9 C2 + §10 C3) | E07_IMPLEMENTATION_COMPLETE v1.0.0 + C3 consumido · SOURCE/CONTRACT PASS · MQL_COMPILE_PENDING · PHYSICAL_PENDING · FINAL_CLOSED=NO |

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [ ] E-07 WP0–WP2: baseline, dominio (envelope+topics), migración 065 + harness #owner/agent #type/dev #area/echo
> - [ ] E-07 WP3–WP5: stores, emitter Bridge + hooks, consumer echo-core (ingesta/atribución/coverage/driver) #owner/agent #type/dev #area/echo
> - [ ] E-07 WP6–WP7: regresión BWC, SOURCE gates, VERIFICATION con evidencia y handoff Manager #owner/agent #type/dev #area/echo

## 🗺️ Roadmap (padre)

- [[Echo — Live Platform V1]] § Roadmap → «E-07 Raw facts, DEAL, coverage and trade lifecycle». Dependencias: E-06 (interfaces; source consumido), E-03 (identidad). Parallel: diseño E-08.
- Preservaciones: UNKNOWN ≠ ZERO · DEAL ≠ JOURNAL · Strategy ≠ Version ≠ RuntimeBinding · Strategy Quality ≠ Execution Fidelity · event time ≠ recorded time.

## 📆 Bitácora

- **2026-09-20 — Corrección Manager C3 consumida (una sesión autónoma):** ticket ≠ position_identifier en CLOSE MT5 resuelto @ `3765f2ba` (push FF `28213bbc..3765f2ba`). Defecto: `HistorySelectByPosition(ticket)` con el POSITION_TICKET (la API exige el identificador; pueden diferir) ⇒ `position_identifier` §17.1 ausente incorrectamente y origin key §5.1 del CLOSE divergente del OPEN. Fix: resolver `ResolvePositionIdentifier` (1. posición viva `POSITION_IDENTIFIER`; 2. relación durable historial `HistoryOrderSelect`→`ORDER_POSITION_ID` con posición cerrada OK; contradicción ⇒ 0 fail-closed §17.3, jamás fabricar) + `HistorySelectByPosition` exclusivamente con el identificador resuelto; `DEAL_POSITION_ID` de los deals sigue siendo la provenance; sitios `SendTradeCloseImmediate` + `CheckForClosedOrders` + guard `DetectCloseReasonFromDeals`; offline/reenvíos confluyen al mismo path; MT4 diff 0. Contrato mínimo: sin extensión del binario TradeMapper (§10.6 E-03). Tests A–H rojo→verde (pines SOURCE MQL + espejo Go en `v3/sdk/domain/position_identifier_resolution_test.go`): 2 rojos exactos @ `28213bbc` → verde; suites domain/bridge/tradefacts `-race` + vet/build 4 módulos PASS; S0/065/go.mod/mt4 diff 0; PG sin impacto (harness 065 no re-ejecutado). MQL_COMPILE_PENDING (sin compilador real en el entorno). Hallazgo registrado sin retoque: `EchoPersistence.mqh` detección offline con el mismo patrón (fuera del delta autorizado §17.1, compartido con execution_agent) — decisión Manager pendiente. SPEC §17.6; VERIFICATION §10.
- **2026-09-20 — Decisión Manager C2 consumida (una sesión autónoma):** C4+C5 implementados @ `28213bbc` (push FF `a7a61875..28213bbc`). C4: productor MQL del pipe Reference identificado en el repo echo y enriquecido con protocolo V1.1 aditivo (position_identifier/account_server/platform en 6 sitios; CLOSE resuelve el identificador desde la historia deal↔posición sin exigir posición abierta; MT4 usa el ticket como identificador durable del modelo, atestado por platform); Bridge parsea la identidad en carril E-07 separado (structs legacy intactos) y publica el hecho E-07 sólo con identidad completa observada — sin fallback a h.broker, sin defaults, fail-closed sólo en el flujo E-07, legacy byte-idéntico (probado content-idéntico ante productor enriquecido y legacy). C5: receta `fact_ref` frozen del Manager implementada (`H("echo-trade-fact-ref.v1",[contract_version,kind,source_key,broker_server_ref,account_registration_ref,platform,origin_position_id,trade_id,raw_payload_sha256])`, hash de bytes originales; tests obligatorios A–F, con F registrando el límite de bytes idénticos sin discriminador físico). Gate RAW-BEFORE-ROUTE documentado (PublishSync ≠ commit durable; gate E-08: durable+pin antes de routing). Evidencia: 5 rojos exactos @ `a7a61875` → verde; SOURCE/CONTRACT/PG PASS (harness 065 PASS; failing sets equivalentes por nombre apples-to-apples con DBs frescas equivalentes; cero nombres E-07; 4 canónicos sin PG); go.mod/S0/migraciones diff 0. SPEC ERRATUM-A §17 (original preservado), VERIFICATION §9, PLAN/TASKS delta. PHYSICAL_PENDING: siguiente acción única = desplegar EA enriquecido en terminal real y demostrar identidad end-to-end sobre binding OBSERVING real.
- **2026-09-20 — Corrección Manager C1 ejecutada (una sesión autónoma):** defectos demostrados por revisión de source corregidos @ `a7a61875` (push FF desde `7c836619`). C1: `raw_payload` persiste los bytes ORIGINALES decodificados (no el texto base64); digest y payload contractual intactos. C2: `Service.RecoverPendingFact` — recuperación transaccional explícita (claim `FOR UPDATE SKIP LOCKED`, proyección completa + PROCESSED en la misma transacción, rollback ante fallo, replay/concurrencia idempotentes); el sweep ya no re-invoca el consumo ordinario (que convergía D1 sin proyectar y dejaba PENDING perpetuo); D1 ordinario intacto. C3: lookup de binding sobre la transacción y sólo para OPEN; fallo SQL ⇒ rollback + redelivery; ErrNoRows ⇒ UNKNOWN contractual; `UNKNOWN/LOOKUP_ERROR` commiteado eliminado. C4: sin `position_identifier` físico en el source del pipe Reference ⇒ emitter fail-closed sin publicar el ticket como origin_position_id; STOP `E07_ORIGIN_IDENTITY_CONTRACT_CONFLICT` entregado (VERIFICATION §8.2); flujo legacy intacto. C5: receta `echo-trade-fact-ref.v1` clasificada sin autoridad S0 → ratificación Manager. Evidencia: 9 rojos exactos → verde `-race`; failing sets idénticos por nombre (4 sin PG / 55 con PG vs `7c836619`==baseline); harness 061→065 PASS; go.mod/migraciones/S0 diff 0. Aceptación Manager RETENIDA hasta decisión C4 + ratificación C5.
- **2026-09-19 — NORMAL ejecutado (una sesión autónoma):** implementación completa WP0–WP7 / T00–T17 @ `7c836619` (push FF desde `59338a64`; base histórica `b66dc5ff` intacta). Gates: SOURCE (delta ⊆ autorizados, 39 archivos, go.mod delta 0, tokens 0), CONTRACT (dominio 13 tests + bridge `-race` PASS, MT-17/21–23 dual-publish byte-idéntico y legacy sin degradar), PG (19 tests stores + 8 consumer `-race` + harness `trade_facts_e7` PASS: interlock 064→065, up/down/up, matriz D1/C1–C4/D2/Q1, guardas lifecycle, REVOKEs, dedupe dual coverage) sobre PG 17.11 descartable. Failing set idéntico por nombre vs `b66dc5ff` sin y con PG (4 y 55 preexistentes; 0 nuevos). PHYSICAL_PENDING declarado con 5 deudas listadas (VERIFICATION §7.5). Migración 065 exclusiva E-07; cero ALTER a 001–064; cero Forge/Hasura/MQL; cero órdenes (consumer sin producer: replay sin dispatch estructural).
- **2026-09-19 — E-07 TOP planning one-shot:** SPEC/PLAN/TASKS/VERIFICATION/NORMAL-PROMPT v1.0.0 @ `59338a64` en `origin/feature/e07-raw-facts-deal-lifecycle` (docs-only; 4 archivos + prompt; base `b66dc5ff`; master intacto). Migración 065 reservada (exclusiva E-07). Worktree `/tmp/echo-e07-raw-facts-deal-lifecycle`. Gates CONTRACT/PG sin Forge; PHYSICAL diferido explícito. E-01…E-06 no reabiertos; E-06 T21 sigue blocked (G1 `PROMOTION_SEAL_MISSING`) sin cambio.

## 🧭 Decisiones

- Raw-before-route vive en **Core** (`echo-core`, consumer dedicado, mismo proceso que TradeJournalFn) — no Flink, no Gateway, no servicio nuevo (Live Authority §6 opción I; patrón T11 E-06).
- Reuse `echo.raw_trade_events` (029) con extensión aditiva; **no** segundo registro de trades.
- Atribución resuelta **al OPEN** con SELECT read-only de 064; pin write-once; sin re-resolución ni retro-atribución.
- Topics nuevos `echo.trade-facts.v1` / `echo.reference-coverage.v1` con Bridge dual-publish paralelo; legacy intacto.
- MQL/collector (emisión física de DEAL/coverage) **fuera** de E-07 V1: shapes por fixtures; PHYSICAL diferido.
- Mapeo V1 del envelope Bridge: envelope porta `trade_id` + `origin_position_id` (§5.1 los exige y S0 no los tiene); `source_key` = `trade_id`. **[Ampliado por C2]** `broker_server_ref`/`platform`/`origin_position_id` ahora son valores OBSERVADOS del productor V1.1 (VERIFICATION §7.4 queda superseded en su parte de broker de sesión/UNKNOWN; sólo vigente para productores legacy sin identidad ⇒ fail-closed sin publicar).
- **C2 (2026-09-20):** protocolo pipe Reference V1.1 aditivo autorizado por el Manager con identidad física auténtica (provenance observada; sin ClientConfig/Forge; ticket y login por separado); receta `echo-trade-fact-ref.v1` FROZEN por el Manager (raw_payload_sha256 de bytes originales; límite de bytes idénticos registrado); gate RAW-BEFORE-ROUTE: PublishSync ≠ commit durable, E-08 exige aceptación durable + pin válido antes de routing, sin reenvíos ciegos (SPEC §17).
- **C3 (2026-09-20):** la búsqueda histórica del CLOSE (`HistorySelectByPosition`) recibe exclusivamente el POSITION_IDENTIFIER resuelto de la relación física MT5 (posición viva / orden en historial), jamás el ticket crudo; no demostrable ⇒ campo ausente fail-closed (§17.3); la relación durable vive en el historial del broker, no en persistencia local (sin extensión del binario §10.6).

## 🔗 Docs / Links

- `specs/FEAT-RAW-FACTS-DEAL-COVERAGE-LIFECYCLE-E7/` (SPEC/PLAN/TASKS/VERIFICATION/NORMAL-PROMPT) en `xKoRx/echo`.
- [[Echo — Live Platform V1]] · [[Echo — E-06 Reference Enrollment and Binding]] · [[Echo — Producto Integrado]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] (§6 autoridad de hechos)
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo + Echo Forge — Deferred Certification Backlog]]
