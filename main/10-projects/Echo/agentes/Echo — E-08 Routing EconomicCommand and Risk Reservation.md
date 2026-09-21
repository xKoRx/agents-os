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
progress: 60
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

- **E08_SOURCE_C3_APPROVED (2026-09-21):** Manager aprobó el SOURCE review del delta C3 @ `28db61b2` en `origin/feature/e08-routing-economic-command-risk-reservation` (C3-A precedencia durable del replay RG-5 + C3-B tiempo de decisión congelado; sin observaciones que reabrir). Gates vigentes: `SOURCE_VERIFIED · CONTRACT_PASS · PG_PASS · COVERAGE_GATE_PENDING (§12.4) · PHYSICAL_PENDING · ECONOMIC_ACTIVATION_PENDING · FINAL_CLOSED=NO`. El único gate de software restante del carril es **COVERAGE_GATE §12.4** (router 91.2% / recovery 81.0% / universe 92.3% / driver 87.8% por funciones; `Route` 79.8%, `fanoutCandidates` 68.1%, `SweepExpiredClaims` 72.0%; residuo declarado = colas de error de infra, ramas defensivas y colas transitorias preexistentes C1). La clase C permanece congelada por prerrequisitos externos §14 sin cambio (E-07 PHYSICAL, E-06 G1/T21, MQL_COMPILE, corrección `EchoPersistence.mqh`, E-02 AC-18) — no es trabajo NORMAL. **Ownership `economic_copy_authorizations` ratificado:** E-08 sólo LEE (SPEC §18.5); el plano de configuración es su dueño y no existe en este carril (Live Authority §7: campo aditivo de policy/assignment existente, explícitamente no Portfolio design ⇒ tampoco E-11); SPEC §19 reconfirma "sin escritor"; verificado en source `28db61b2`: cero INSERT productivo, sólo fixture de test. No se autoriza productor en este carril. Next = **NORMAL: cierre COVERAGE_GATE §12.4** (mandato TOP emitido 2026-09-21).
- **E08_CORRECTION_C3_COMPLETA (2026-09-21):** corrección Manager C3 (C3-A precedencia durable del replay RG-5 — `Route` consulta la decisión durable por routing_key ANTES de todo re-evalúo, identidad inmutable congelada contra el pin del replay ⇒ `ROUTING_IDENTITY_CONFLICT` fail-closed sin mutación, recuperación desde el snapshot sellado sin evaluar gate ni config, carrera de creación resuelta con la identidad del snapshot ganador; C3-B tiempo de decisión — decision_at congelado en ROUTING_INPUT schema 2→3 y restaurado en el re-drive, `classifyCandidate` evalúa ValidUntil contra el reloj congelado jamás `time.Now()`, evidencia temporal ausente ⇒ fail-closed sin inventar timestamp) @ `28db61b2` pushed FF `c2e88a0d..28db61b2` (HEAD == origin; worktree `/tmp/echo-e08-routing-economic-command-risk-reservation`). 3 commits atómicos (`8fe7e5b2` C3-A, `b7c9adbe` C3-B, `28db61b2` docs) con rojos capturados contra el código sin corregir; delta = 5 archivos Go/tests en econroute + SPEC §20 (ERRATUM C3) + VERIFICATION §12. Gates: econroute -race verde 6/6 (31 tests = 25 + 6 nuevos), failing set 53 idéntico al T00, harness 066 PASS (PG descartable dedicada :15444), vet/build PASS, COVERAGE_GATE_PENDING declarado (§12.4). Estado: `SOURCE_VERIFIED · CONTRACT_PASS · PG_PASS · COVERAGE_GATE_PENDING · PHYSICAL_PENDING · ECONOMIC_ACTIVATION_PENDING · FINAL_CLOSED=NO`. Next = **Manager review del delta C3**.
- **E08_CORRECTION_C2_COMPLETA (2026-09-20):** corrección Manager C2 (C2-1 clase de observación write-once, C2-2 identidad de estrategia contra el binding vivo E-06, C2-3 coverage por intervalos reales con contradicciones fail-closed, C2-4 snapshot ROUTING_INPUT con freeze económico completo + redrive fail-closed schema v2) @ `c2e88a0d` pushed FF `53d42615..c2e88a0d` (HEAD == origin; worktree `/tmp/echo-e08-routing-economic-command-risk-reservation`). 5 commits atómicos con rojos semánticos demostrados por caso; delta = 7 archivos autorizados + SPEC §19 (ERRATUM C2) + VERIFICATION §11. Gates: suites -race por paquete con failing set 53 idéntico al T00 (diff por nombre vacío), harness 066 PASS, vet/build PASS, COVERAGE_GATE_PENDING declarado con rutas exactas (§11.4). Consumía el baseline C1 `53d42615` (VERIFICATION §10, correcciones C1-A…C1-F @ `977e4fde`…`5ddfb471`). Estado: `SOURCE_VERIFIED · CONTRACT_PASS · PG_PASS · COVERAGE_GATE_PENDING · PHYSICAL_PENDING · ECONOMIC_ACTIVATION_PENDING · FINAL_CLOSED=NO`.
- **E08_IMPLEMENTED clase A v1.0.0 (2026-09-20):** NORMAL T00–T14 ejecutado; `SOURCE_VERIFIED · CONTRACT_PASS · PG_PASS · PHYSICAL_PENDING · ECONOMIC_ACTIVATION_PENDING · FINAL_CLOSED=NO`. Push FF `fe5c9de0..b0012909` en `origin/feature/e08-routing-economic-command-risk-reservation` (HEAD == origin; master `5dd998f1` intacto). 13 commits: dominio §5/§6 (identidad S0-validada sin truncar), migración 066 con SIETE tablas (corrección Manager #2) + harness up/down/up, stores snapshots/routing/comandos/reservas, RoutingGate RG-1…RG-4, router durable con transacción única y re-drive desde snapshot congelado (corrección Manager #3), recovery sweepers §12, driver `ECHO_E8_DURABLE_ROUTING=false` default fail-closed. Matriz MT-01…MT-18 PASS sobre PG 17.11 descartable; failing sets 55=55 vs T00 (cero nuevos/cambiados); delta ⊆ PLAN §2 (gofmt accidental de 8 archivos E-07 revertido en `dff46409`). Cobertura: críticos (identidad/reservas/outbox/gate) 100%; residuo declarado = wrappers de error de infra no inyectables sin mocks. VERIFICATION §2–§9 con evidencia real. Next = **Manager review** de la implementación (decisión: aceptar CONTRACT/PG y programar clase C con prerrequisitos §14).
- **E08_PLANNING_FROZEN v1.0.0 (2026-09-20): SPEC/PLAN/TASKS/VERIFICATION + NORMAL-PROMPT @ `fe5c9de0` en branch `feature/e08-routing-economic-command-risk-reservation` (base `3765f2ba` = HEAD E-07 C3; master `5dd998f1` intacto). Migración `066` reservada (exclusiva E-08; 066 libre verificada). Gate RAW-BEFORE-ROUTE como boundary RG-1…RG-6 (sólo hechos `PROCESSED` commiteados + pin OBSERVING válido; PublishSync ≠ commit durable; UNKNOWN/SHADOW/sin coverage jamás elegibilidad; replay jamás genera segundo comando; dispatch jamás adelanta al commit). CommandID determinístico resuelto por regla (`command_unique_key` UNIQUE + `content_digest`; UUIDv7 minteado una vez; misma key+digest ⇒ mismo comando; key+digest distinto ⇒ `COMMAND_CONFLICT` cuarentenado) — consume el defer de E-02 §1.0.1. Snapshot inmutable content-addressed de policy/sizing/SLTP/destination/delay/account/instrument/decision (fila mutable jamás es autoridad histórica). Reserva integrada al command con headroom serializado por cuenta (`SELECT … FOR UPDATE`), `UNKNOWN_HELD` sin auto-release. Outbox monotónico en la propia fila del comando; sweepers SKIP LOCKED; reconciliación sin reenvío. Separación frozen: clase A (persistencia/identidad, PG hoy, cero órdenes) / clase C (activación económica condicionada: wiring vivo + dispatcher + E2E; prerrequisitos E-07 PHYSICAL, E-06 G1/T21, MQL_COMPILE, corrección `EchoPersistence.mqh`, E-02 AC-18). No reabre E-01…E-07 ni el roadmap. Next = NORMAL (`NORMAL-PROMPT.md`).

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e08-routing-economic-command-risk-reservation` | `3765f2ba` (E-07 HEAD C3; master `5dd998f1` intacto) | `specs/FEAT-ROUTING-ECONOMIC-COMMAND-RISK-RESERVATION-E8/SPEC.md` v1.0.0 + ERRATUM C1 §18 + ERRATUM C2 §19 + ERRATUM C3 §20 @ `28db61b2` | `.../PLAN.md` + `.../TASKS.md` + `.../VERIFICATION.md` (§10 C1, §11 C2, §12 C3) + `.../NORMAL-PROMPT.md` | E08_SOURCE_C3_APPROVED @ `28db61b2` · SOURCE/CONTRACT/PG PASS + COVERAGE_GATE_PENDING (§12.4) + PHYSICAL_PENDING + ECONOMIC_ACTIVATION_PENDING + FINAL_CLOSED=NO · Next: NORMAL cierre COVERAGE_GATE §12.4 |

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [x] E-08 T00–T02: baseline + failing sets, dominio E-08, migración 066 + harness #owner/agent #type/dev #area/echo
> - [x] E-08 T03–T07: stores snapshots/routing/comandos/reservas + RoutingGate RG-1…RG-4 #owner/agent #type/dev #area/echo
> - [x] E-08 T08–T10: router durable (default OFF), sweepers recovery/reconciliation, driver + wiring apagado #owner/agent #type/dev #area/echo
> - [x] E-08 T11–T14: matriz MT-01…MT-18, gates SOURCE/BWC, VERIFICATION con evidencia, handoff Manager #owner/agent #type/dev #area/echo
> - [x] E-08 corrección Manager C1 (C1-A…C1-F) + corrección C2 (C2-1…C2-4) @ `c2e88a0d` + corrección C3 (C3-A/C3-B) @ `28db61b2` #owner/agent #type/dev #area/echo
> - [x] E-08 Manager review delta C3: SOURCE APPROVED @ `28db61b2` (2026-09-21) #owner/human #type/review #area/echo
> - [ ] E-08 NORMAL cierre COVERAGE_GATE §12.4 (≥95% sobre archivos nuevos; suites reales sin mocks; rama inalcanzable con entrada real se borra con justificación por ruta) #owner/agent #type/dev #area/echo
> - [ ] E-08 clase C: wiring vivo + dispatcher + CLOSE durable + E2E (gate Manager/owner; prerrequisitos SPEC §14) #owner/agent #type/dev #area/echo

## 🗺️ Roadmap (padre)

- [[Echo — Live Platform V1]] § Roadmap → «E-08 Routing, EconomicCommand and risk reservation». Dependencias: E-07 identidad raw (interfaces verificadas @ `3765f2ba`, consumidas como base). Parallel: guards de E-12 en shadow (E-12 decides).
- Preservaciones: UNKNOWN ≠ ZERO · raw fact ≠ economic command · replay de hechos ≠ replay de órdenes · Strategy ≠ Version ≠ RuntimeBinding · routing legacy intacto en clase A/B.

## 📆 Bitácora

- **2026-09-21 — Manager aprueba SOURCE C3 y emite mandato siguiente (sesión TOP):** review del delta C3 @ `28db61b2` APROBADA (sin observaciones; no se repiten reviews C1/C2). Gates físicos/económicos siguen pendientes y externos: PHYSICAL_PENDING, ECONOMIC_ACTIVATION_PENDING, FINAL_CLOSED=NO; clase C congelada por prerrequisitos §14. Resolución de ownership `economic_copy_authorizations`: dueño = plano de configuración operado por owner (Live Authority §7, campo aditivo de policy/assignment existente, no Portfolio design ⇒ fuera de E-08 y fuera de E-11); E-08 permanece lector exclusivo (SPEC §18.5/§19; verificado cero escritor productivo en `28db61b2`) — no se autoriza productor en este carril. Siguiente tarea autorizada por el DAG: **NORMAL cierre COVERAGE_GATE §12.4** sobre la misma rama `28db61b2` (≥95% archivos nuevos; fallos reales de PG como entrada legítima, sin mocks de stores; ramas inalcanzables con toda entrada real se borran con justificación por ruta, sin debilitar fail-closed); E-09 coverage §6 queda encolado como siguiente mandato independiente. E-08/E-09 permanecen FINAL_CLOSED=NO; sin merge a master; sin flags.
- **2026-09-20 — Corrección Manager C2 (C2-1…C2-4) una sesión:** identidad, coverage y replay determinístico @ `c2e88a0d` pushed FF desde baseline C1 `53d42615`. C2-1: el gate ya no sobrescribe la clase del raw antes de `pinMismatch` (raw SHADOW + lookup CANONICAL era elegible); raw y lookup preservados separados, exigido raw = resolución = CANONICAL. C2-2: `StrategyRef`/`CanonicalStrategyID` del request exigidos idénticos a `BindingResolution` (antes se minteaba comando con identidad ajena a E-06). C2-3: RG-4.1 decide por intervalos `[from,to)` concretos de `intervals` (los extremos agregados aceptaban huecos) y TODOS los reportes cubrientes participan: KC+PARTIAL/UNKNOWN ⇒ CONTRADICTED ⇒ COVERAGE_UNKNOWN (el "latest wins" quedó eliminado); evidencia durable en GateInputs y snapshot DECISION. C2-4: ROUTING_INPUT congela magic override/offsets SL-TP/delays con schema v2; redrive fail-closed sobre snapshots sin freeze completo, reconstrucción sin config mutable ni defaults, sin remint de command_ref. Rojos semánticos demostrados reinyectando cada defecto. Gates: failing set 53=53 T00, harness 066 PASS, vet/build PASS, COVERAGE_GATE_PENDING (§11.4). VERIFICATION §10 registra la corrección C1 (C1-A…C1-F) consumida como baseline. Next = Manager review del delta C2.
- **2026-09-20 — NORMAL T00–T14 una sesión:** implementación clase A completa @ `b0012909` pushed. Gates: SOURCE (delta ⊆ PLAN §2; tokens 0; contracts/001–065/go.mod/legacy diff 0), CONTRACT (`-race` domain/postgres/econroute), PG (harness 066 up/down/up + suites PG REAL con DATABASE_URL). Failing sets 55=55 idénticos vs T00. Correcciones Manager aplicadas: HEAD `fe5c9de0` (#1), SIETE tablas (#2), re-drive desde snapshot congelado (#3), S0 real validado sin truncamiento (#4 — `Validate()` del envelope construye el S0 `EconomicCommand` y propaga su rechazo exacto; claves no representables (>128 bytes) fallan cerradas). Decisiones de ejecución en VERIFICATION §8: gates Go en modo workspace (GOWORK=off imposible para v3/core sin editar go.sum), `routing_universe_ref` en 066 como fuente del re-drive §12a, `IN_FLIGHT` expirado dual (reclaim §9 / sweeper §12c con SKIP LOCKED), CREATED sin headroom ⇒ BLOCKED_AFTER_DECISION + EXCLUDED(INSUFFICIENT_RESERVATION). Cobertura: críticos 100%, residuo declarado (wrappers de error de infra; repo prohíbe mocks de stores). Next = Manager review.
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
