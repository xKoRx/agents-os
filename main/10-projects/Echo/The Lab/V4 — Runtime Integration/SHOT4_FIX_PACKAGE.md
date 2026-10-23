---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo — Producto Integrado]]", "[[0 — Shot 1 Gate and Baseline]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-23"
updated: "2026-10-23"
---

# SHOT4_FIX_PACKAGE

## Propósito

Único paquete ejecutable para GLM LOCAL Shot4 de THE_LAB_V4_RUNTIME_FORGE_INTEGRATION. Se entrega al Primary Manager; esta auditoría no ejecuta fixes ni inicia Shot4. Exactamente cuatro shots, D24 vigente, criterios originales inalterados.

## Contenido

**SHOT4_FIX_PACKAGE_READY.** 53 findings adjudicados: 22 P0, 30 P1 y 1 P2. H01–H49: 1 PASS, 41 FAIL, 7 NOT_RUN, 0 BLOCKED_EXTERNAL principales.

### Entrada y restricciones

Echo candidato `3b3ae81eb0905286324c899e122737f98dd45303`, Symphony `dd4af7d05c03db9b39b5467b46e2c2c7d0c1fa19`. Usar los repos y procedencias autorizados, documentar delta posterior si existe sin sustituir el baseline auditado ni incorporar ramas históricas. Los repros de Shot3 permanecen independientes y sin alterar; trasladar regresiones revisadas al producto sólo en Shot4. Ningún PASS histórico, mock, fixture visible como real o ACK de transporte acredita el outcome.

Sin trading real, deploy PROD, cambios compartidos, campañas/extracción Forge, backtester legacy, merge/rebase/cherry-pick o migraciones destructivas. Mantener KISS/YAGNI y owners existentes: un motor runtime, un writer journal, un kernel ranking. No nuevo freeze, preguntas de diseño ya resueltas ni quinto shot. Toda revisión independiente final ocurre dentro de Shot4.

### Orden por dependencias

| Etapa | Ownership y salida | Findings/condición para avanzar |
|---|---|---|
| 0 — Harness seguro | QA/launcher: manifest, endpoints resueltos, procesos propios, PG/Hasura aislados, teardown explícito | F-01/F-02 antes de cualquier prueba física; repetir H47/H48 con sentinel/espías y luego recursos propios. No usar rebase.sh stop actual |
| 1 — Identidad y almacenamiento | Registry/history/SQL: crosswalk completo, Magic protegido, revisiones/facts inmutables y permisos mínimos | B-01..B-07; preservar checksums075/070; gates H01–H04/H12/H14/H35 dirigidos |
| 2 — Fuente y readiness | Bridge/Core/StateFun/journal/projector/MM: autoridad real, eventos/ciclo, pending, snapshot/outbox, ACK/incarnation y QI previo a fill | A-01..A-08 y B-05; dependencia de1; H05–H13/H49 sin LAB activo, luego replay LAB |
| 3 — Economía y worker | Analyze/loader/worker: cuatro perfiles, Q/currency, SUMMARY, tiempo, fixed24, lease y publicación vectorial | C-01..C-10/C-12/C-13; source económica fiable de1–2; H15–H23/H26/H34/H46 |
| 4 — Selección/I1 y cohortes | Selection/composition+ranking: AS_KNOWN, D11/copia, muestras/window, MinMax completo, CAS y dependencias de módulos | C-11/C-14, D-01..D-08; mantener H28 y ejecutar H24/H25/H27–H33; sin I2/backtester |
| 5 — API/Hasura/UX | Gateway real, hooks/sesión, metadata aditiva, bundle/pins/score/page, todos paneles y estados | E-01..E-13; probar H36–H43 por REST/action/GraphQL/WS/browser sobre fuentes pinneadas |
| 6 — Escala y certificación final | QA independiente del cambio final, manifest del candidato y datos, perfiles coverage, recuperación, no interferencia y teardown | H01–H49 completos, H44/H45 sin reducir datasets, QA-01; preservar blockers físicos reales con evidencia y no convertirlos en PASS |

P0 de etapas posteriores puede desarrollarse junto a dependencias compatibles, pero no certificar un consumidor antes de que su fuente sea fiel. No publicar cohortes/read bundles sobre economía todavía falseada.

### Migraciones 075 y compatibilidad obligatoria

Inventariar catálogo/owners/grants y ledger del destino autorizado antes de aplicar. 075 existe en el candidato y en el runner, aunque el diseño enumeró067–074 y el comentario dice harness-only. No renumerar ni reescribir070/075 ni regenerar sus checksums para esconder drift. Registrar075 como extensión contractual aditiva. La siguiente migración libre verificada corrige grants, inmutabilidad y scopes; usar076 sólo si no fue ocupada. Ensayar dos estados: catálogo hasta074 sin075 y catálogo con075 aplicada/ledger existente. En ambos, runner checksum/reapply/rollback y compatibilidad de writers/readers deben quedar demostrados. Un surrogate PG o stubs Hasura no prueban preflight real ni event delivery. No aplicar en compartidos durante esta entrega.

### Correcciones individuales y regresiones obligatorias

Cada ficha conserva expected/actual, source exacto, repro, ownership y regresión del auditor. Las notas GOD delimitan contradicciones y severidad definitiva. Los textos técnicos originales se preservan para evitar perder condiciones del repro. Rutas de evidencia relativas al workspace externo `the-lab-v4-shot-3-god`.

### A-01 — P0 — JOURNALED receipt and outbox exist without a canonical journal write

**Tipo/casos:** bug; H07, H10, H11. **Superficie propietaria:** v3/sdk/postgres/master_observation_service.go:72-178.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/master_observation_service.go:72-178.

**Esperado:** TradeJournalFn/SaveOpen or SaveClose must persist actual journal row and emit snapshot outbox atomically with real journal identity.

**Observado:** Accept never invokes its journal repository. Physical surrogate-SQL readback: receipt JOURNALED, trade_journal 0, intake 1, outbox 1. Outbox journal_id is random UUID unrelated to receipt JournalID; snapshot_artifact is a hash without retained artifact content.

**Repro/evidencia:** base `work/shot3/A`; evidence/repro.log; evidence/source-excerpts.txt. Comando/ruta: cd work/shot3/A/repro && GOWORK=off GOMAXPROCS=2 go build -p=2 -o ../repro-bin . && ../repro-bin (requires owned PG55461 initialized; schema.sql resets only owned schemas)

**Corrección concreta:** Route authenticated master through canonical journal owner; persist correlation, monotonic journal revision and complete retained snapshot outbox in that owner transaction.

**Regresión obligatoria:** Stop LAB; OPEN/CLOSE via real ingress; assert owner journal rows and exact journal ID/outbox snapshot; restart LAB and assert one history effect.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### A-02 — P0 — Pending reconciliation irreversibly deletes observations without journalization

**Tipo/casos:** bug; H08, H10. **Superficie propietaria:** v3/sdk/postgres/master_observation_service.go:198-242.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/master_observation_service.go:198-242.

**Esperado:** Reconcile exact mapping, retain full source causal sequence, journal observed facts before deleting/marking processed.

**Observado:** ReconcilePending only checks existence by namespace+binding, then DELETE and COMMIT. Readback pending 0 while intake/journal/outbox unchanged. It never calls Accept or journal writer. Pending also omits account/run/role/magic/version fields needed for exact recovery.

**Repro/evidencia:** base `work/shot3/A`; evidence/repro.log; evidence/source-excerpts.txt. Comando/ruta: cd work/shot3/A/repro && GOWORK=off GOMAXPROCS=2 go build -p=2 -o ../repro-bin . && ../repro-bin (requires owned PG55461 initialized; schema.sql resets only owned schemas)

**Corrección concreta:** Persist full authenticated scope in pending; journal via owner with durable dedupe; mark consumed only in same successful transaction.

**Regresión obligatoria:** OPEN then CLOSE before readiness; enable exact binding, reconcile, crash/retry; actual CLOSED journal row exists once, pending retains failures, zero retroactive opens.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### A-03 — P0 — Journal adapter reverses signed commission and swap

**Tipo/casos:** bug; H11. **Superficie propietaria:** v3/sdk/postgres/master_observation_service.go:260-271; v3/sdk/postgres/migrations/057_fix_trade_journal_profit_net.up.sql:27-34.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/master_observation_service.go:260-271; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/migrations/057_fix_trade_journal_profit_net.up.sql:27-34.

**Esperado:** Net equals gross + signed commission + signed swap as canonical generated profit_net.

**Observado:** Adapter computes gross - commission - swap. E.g. gross120 commission-4 swap-2 yields126 instead of114. Legacy domain tests explicitly use negative signed costs. Source arithmetic proof; no physical V2 ingestion claimed.

**Repro/evidencia:** base `work/shot3/A`; evidence/source-excerpts.txt; evidence/source-excerpts.txt. Comando/ruta: Inspect numbered source-excerpts.txt and complete repository caller searches; source-path proof, not runtime E2E

**Corrección concreta:** Read canonical generated net or add signed costs once; preserve exact decimal values/cost evidence instead of rounding all broker sources to two places.

**Regresión obligatoria:** Real journal row gross120 commission-4 swap-2 -> history net114; positive swap/rebate and null gross preserve source semantics.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### A-04 — P0 — Journal history invents metadata and cannot preserve source scope

**Tipo/casos:** bug; H11. **Superficie propietaria:** v3/sdk/postgres/master_observation_service.go:273-341.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/master_observation_service.go:273-341.

**Esperado:** Preserve source account/run/instruments, proven currency/costs/binding/Qi, actual coverage and authoritative availability/reference-start dates.

**Observado:** Adapter hardcodes instrument set NQ, USD UNPROVEN, coverage2025-01-01..2026-01-01, LIVE and reference dates now; uses trade ID as binding_ref, omits account and source run, discards source currency/Qi by DTO design. Nil gross becomes amount0. Honest UNPROVEN flags alone do not cure fabricated dates/scope.

**Repro/evidencia:** base `work/shot3/A`; evidence/source-excerpts.txt; evidence/source-excerpts.txt. Comando/ruta: Inspect numbered source-excerpts.txt and complete repository caller searches; source-path proof, not runtime E2E

**Corrección concreta:** Extend explicit journal snapshot DTO with owner evidence and crosswalk; preserve UNKNOWN when missing and actual intervals/instruments; resolve stable history identity per source/account/run and append full revisions.

**Regresión obligatoria:** EURUSD/EUR journal with source dates outside2025 and two accounts/runs; no NQ/USD substitution, timestamps never move on replay, unknown gross never yields measured zero.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### A-05 — P0 — Master bridge and native causal Qi integration are absent from production flow

**Tipo/casos:** functional_missing; H07, H09, H10, H11, H49. **Superficie propietaria:** v3/sdk/postgres/master_observation_service.go:58-59; v3/sdk/futures/operation/mm.go:380-397; v3/sdk/futures/operation/engine.go:1864-1889; v3/sdk/futures/operation/engine.go:2083-2115; v3/core/internal/functions/futures_operation.go:439-447.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/master_observation_service.go:58-59; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/futures/operation/mm.go:380-397; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/futures/operation/engine.go:1864-1889; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/futures/operation/engine.go:2083-2115; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/core/internal/functions/futures_operation.go:439-447.

**Esperado:** Real runtime consumers install/checkpoint exact config and emit ACK; owner seals CycleRisk before exposure and emits QI_SEALED; master ingress invokes canonical bridge without native Operation fabrication.

**Observado:** JournalObservationServiceV2/HistoryFromJournal/ReconcilePending have no production callers. Core/bridge have no RuntimeConfigAppliedV1, CycleRiskSeal, QI_SEALED integration. MMDecision lacks CycleRisk; runtime emits original facts rather than new causal Qi facts. H49 missing implementation is FAIL, not external blocker.

**Repro/evidencia:** base `work/shot3/A`; evidence/product-wiring-search.txt; evidence/source-excerpts.txt. Comando/ruta: Inspect numbered source-excerpts.txt and complete repository caller searches; source-path proof, not runtime E2E

**Corrección concreta:** Wire narrow runtime config consumers/ACK and instant NEW OPEN readiness fencing; connect master journal owner and outbox consumer; add immutable MM opening risk seal and effect inside transactional Apply, preserving current engine.

**Regresión obligatoria:** Native s1/s2/tg runner: pre-fill seal with real MM budget, multiple orders/fills/costs, crash/replay exact IDs and independent namespaces; master observe path has zero fabricated Operation.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### A-06 — P0 — Replay loses original receipt and trade lifecycle collides with event dedupe

**Tipo/casos:** bug; H07, H10. **Superficie propietaria:** v3/sdk/postgres/master_observation_service.go:25; v3/sdk/postgres/master_observation_service.go:74-91.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/master_observation_service.go:25; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/master_observation_service.go:74-91.

**Esperado:** Same delivery returns original stable receipt/journal revision; distinct OPEN/CLOSE deliveries of one trade can complete same cycle.

**Observado:** Replay allocates fresh ObservationID and returns DUPLICATE with no JournalID or SourceRevision. SourceEventID is documented trade_id; same trade CLOSE changed payload returns CORRELATION_CONFLICT, physically reproduced. Transport source-event identity and cycle-opening trade identity are conflated.

**Repro/evidencia:** base `work/shot3/A`; evidence/repro.log; evidence/source-excerpts.txt. Comando/ruta: cd work/shot3/A/repro && GOWORK=off GOMAXPROCS=2 go build -p=2 -o ../repro-bin . && ../repro-bin (requires owned PG55461 initialized; schema.sql resets only owned schemas)

**Corrección concreta:** Store receipt identity/revision durably; separate immutable event ID/sequence from trade/cycle identity; duplicate exact event returns persisted original receipt.

**Regresión obligatoria:** OPEN(event1,trade1), CLOSE(event2,trade1), replay after process restart; one CLOSED journal and same original receipts; changed payload for same event still conflicts.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### A-08 — P0 — Readiness cannot invalidate stale consumer incarnation immediately

**Tipo/casos:** bug; H09. **Superficie propietaria:** v3/sdk/postgres/runtime_ack_repository.go:186-290.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/runtime_ack_repository.go:186-290.

**Esperado:** Restart invalidates prior incarnation immediately; re-ACK/checkpoint/lookup current incarnation is required before READY and NEW OPEN.

**Observado:** GetReadiness selects latest applied_at ACK across all incarnations, checking digest/status/lease only; no lookup of currently live incarnation or effective checkpoint. Old ACK remains eligible until lease expiry. Production runtime incarnation invalidation/NEW OPEN gate integration is also absent (A-05). Source-path proof, no full runtime restart run claimed.

**Repro/evidencia:** base `work/shot3/A`; evidence/source-excerpts.txt; evidence/source-excerpts.txt. Comando/ruta: Inspect numbered source-excerpts.txt and complete repository caller searches; source-path proof, not runtime E2E

**Corrección concreta:** Track authoritative active incarnation/recovery state and invalidate old leases atomically on restart; fence NEW OPEN at actual decision against binding/config/current incarnation.

**Regresión obligatoria:** Get old READY, restart consumer to new incarnation within lease15s, NEW OPEN denied until new checkpoint+ACK; existing cycle close retains old binding.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

**Corroboración fusionada:** F-03; reporte F y manifest independiente, sin contar de nuevo.

### B-01 — P0 — App role can forge Magic allocation events and manufacture a successful replay

**Tipo/casos:** bug; H35. **Superficie propietaria:** Echo migration 068 registry grants and fn_v4_assign_magic_allocation..

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/migrations/068_lab_v4_registry_recipes.up.sql:71-90,141-156,181-190,391-403.

**Esperado:** Only the registry function can append the first-assignment event; a replay must also match the mapping's stored Magic tuple.

**Observado:** echo_user has INSERT on the append-only event table. A direct insert succeeds; the function then returns replay=true and Magic 77 while mapping.magic remains NULL.

**Repro/evidencia:** base `work/shot3/B`; evidence/h35_magic_event_poison.log; repro/h35_magic_event_poison.go. Comando/ruta: cd echo/v3/sdk && go run ../../../repro/h35_magic_event_poison.go

**Corrección concreta:** Remove INSERT from echo_user and rely on the SECURITY DEFINER owner; on replay require event tuple and mapping tuple to match. Add a Digest check for allocation_ref at SQL boundary. Do not broaden direct UPDATE permissions.

**Regresión obligatoria:** As echo_user, direct insert into allocation events is denied; function-created first assignment writes event+mapping atomically; identical replay returns existing tuple; conflicting replay and concurrent assignment yield one winner; partial/invalid tuple and event/mapping divergence fail.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### B-02 — P0 — Ingestion auto-aliases external identities onto a canonical strategy

**Tipo/casos:** bug; H01. **Superficie propietaria:** Echo V2 registry identity mapping and ingestion service..

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/strategy_ingestion_v2_registry.go:36-50,51-95; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/strategy_history_v2_service.go:230-242; contract:B — Forge Ingestion Readiness.md:63-74.

**Esperado:** Persist a unique `(namespace, producer_writer, external_strategy_ref)` crosswalk and reject a second external ref unless its complete mapping matches; authenticate producer_ref against the authorized writer.

**Observado:** UpsertStrategyMapping looks up only namespace+canonical ID and returns the existing strategy_ref without checking externalRef, producerWriter, Magic, display name, direction, timeframe or instrument set. The real method returned the same UUID to contradictory refs/writers.

**Repro/evidencia:** base `work/shot3/B`; evidence/h01_external_identity.log; repro/h01_external_identity.go. Comando/ruta: cd echo/v3/sdk && go run ../../../repro/h01_external_identity.go

**Corrección concreta:** Persistir crosswalk inmutable (namespace, writer autorizado, external_strategy_ref); validar producer_ref contra auth.Writer y comparar el mapping íntegro antes de converger. Otra ref externa sólo converge con el mismo mapping íntegro conforme B§3; no rechazar toda ref nueva ni fabricar alias automático.

**Regresión obligatoria:** Mismo mapping completo converge; refs/writers/Magic/definition contradictorios devuelven 409; una ref externa adicional con mapping íntegro idéntico sigue la regla explícita B§3; scope ajeno no obtiene identidad.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### B-05 — P0 — H12 fact persistence has no writer and grants UPDATE over source facts

**Tipo/casos:** functional_missing; H12, H35. **Superficie propietaria:** Echo projector/fact writer and migration 070 grants..

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/migrations/070_lab_v4_execution_projections.up.sql:56-80,278-286; contract:F — SQL Migrations Ownership.md:105; contract:H — Test Matrix Independent Oracles.md:85.

**Esperado:** Same fact key+payload digest is a no-op; conflicting payload is durably quarantined and does not overwrite the prior fact or projection.

**Observado:** No Go source writes operation_facts or fact_conflicts, and the app role can UPDATE the evidence row directly. H12's dedupe/quarantine oracle is not implemented by the SQL table alone.

**Repro/evidencia:** base `work/shot3/B`; REPORT.md#hallazgos-principales; workspace externo Aranea:lab-v4-shot2-impl-20261022/evidence/SHOT2-DELIVERY.md §5. Comando/ruta: Source inventory: `rg -n 'operation_facts|fact_conflicts' echo/v3 --glob '*.go' --glob '*.sql'` returns only migration DDL; `echo_user` receives INSERT, SELECT, UPDATE on operation_facts.

**Corrección concreta:** Implement the source-fact writer plus conflict transaction; keep fact rows immutable after insert and grant only the narrow writer privileges needed. Separate mutable watermarks from immutable facts.

**Regresión obligatoria:** Replay exact fill returns duplicate/no change; same identity with changed quantity creates conflict record and retains existing payload; new late fill preserves cycle and RECONCILIATION_REQUIRED; effect_index permits distinct same-seq effects; direct UPDATE fails.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### B-07 — P0 — 075 master intake is unusable by echo_user and is exposed as a normal migration despite harness-only status

**Tipo/casos:** bug; H35. **Superficie propietaria:** Echo migration 075, migration registry/manifest and master intake service..

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/migrations/075_lab_v4_master_intake.up.sql:1-26; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/master_observation_service.go:79-80,127-130,185-200,232; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/toolkit/cmd/apply-migration/main.go:497-504; contract:F — SQL Migrations Ownership.md:42-55,57; contract:B — Forge Ingestion Readiness.md:177-185,202.

**Esperado:** Service principal can INSERT/SELECT durable intake and perform only the pending-row transitions it owns; migration list matches ratified numbering and byte checksums.

**Observado:** 075 grants no DML to echo_user: both master intake INSERTs fail permission denied. Its own comment says harness-only, while v4EntryDecls exposes it as a regular migration. F's ratified sequence ends at 074.

**Repro/evidencia:** base `work/shot3/B`; evidence/h35_master_intake_privileges.log; repro/h35_master_intake_privileges.go; workspace externo Aranea:lab-v4-shot2-impl-20261022/harness/stubs_inventory.md §Migración 075. Comando/ruta: cd echo/v3/sdk && go run ../../../repro/h35_master_intake_privileges.go

**Corrección concreta:** Preservar bytes y checksums 067–075 existentes. Registrar 075 como delta aditivo soportado; crear la siguiente migración libre verificada (076 sólo si sigue libre) para grants/constraints/reparaciones necesarios. Distinguir DB hasta074 de DB con075 aplicada; comparar catálogo real, owner y ledger antes de toda aplicación autorizada. Nunca consolidar DDL dentro de070 aplicada.

**Regresión obligatoria:** Apply via own least-privilege migration path; connect as echo_user and verify permitted intake/pending transitions plus denied unrelated DML; compare byte checksums and manifest/ledger on replay and checksum conflict.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-05 — P0 — Normalizados sin Q_i se publican READY vacíos

**Tipo/casos:** bug; H16. **Superficie propietaria:** v3/sdk/lab/analyze/timeline.go:279; v3/sdk/lab/analyze/timeline.go:341.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/timeline.go:279; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/timeline.go:341; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:211.

**Esperado:** Sin Q acreditado R y ambos10k INSUFFICIENT_DATA; money50 válido

**Observado:** R insuficiente pero ambos10k READY,0puntos; PG loader acepta FIRST_ENTRY_RISK/FIRST_ENTRY con sealed_at posterior alOPEN como Q100

**Repro/evidencia:** base `work/shot3/C`; evidence/economic-repro.log; evidence/boundary-run.log. Comando/ruta: cd C/echo; GOMAXPROCS=2 go run -p=2 ../repro/economic_repro.go

**Corrección concreta:** Validar acreditación Q_i de ciclo completo, método/basis/currency/source y sello causal antes del primer fill en el loader y frontera de perfiles. FIRST_ENTRY_RISK, monto sin evidencia o sello posterior no acreditan ciclo. Publicar QI_UNPROVEN/INSUFFICIENT para R y normalizados afectados, conservando money independiente y razones explícitas.

**Regresión obligatoria:** Q ausente, cero, posterior apertura y cobertura parcial con estado y razones

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-06 — P0 — NO_FX ignora moneda de Q_i y mezcla netos de movimientos

**Tipo/casos:** bug; H19. **Superficie propietaria:** v3/sdk/lab/analyze/timeline.go:222; v3/sdk/postgres/lab_analysis_service.go:191; v3/sdk/postgres/lab_analysis_service.go:256.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/timeline.go:222; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:191; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:256.

**Esperado:** EUR50/QUSD100 sin FX => NOT_COMPARABLE para R/10k

**Observado:** motor recibe QICurrency USD pero calcula EUR/USD READY; loader no carga moneda Q y suma movimientos sin validar

**Repro/evidencia:** base `work/shot3/C`; evidence/economic-repro.log. Comando/ruta: cd C/echo; GOMAXPROCS=2 go run -p=2 ../repro/economic_repro.go

**Corrección concreta:** Propagar moneda/calidad/Q proof; evaluar por moneda y exigir FX explícito causal

**Regresión obligatoria:** EUR/USD y coste en otra moneda, FX futuro, dos series money

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-07 — P0 — Loader de historia elimina CLOSED_SUMMARY de la curva

**Tipo/casos:** bug; H15, H17. **Superficie propietaria:** v3/sdk/postgres/lab_analysis_service.go:191; v3/sdk/postgres/lab_analysis_service.go:229; v3/sdk/postgres/lab_analysis_service.go:233.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:191; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:229; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:233.

**Esperado:** Summary114 aporta una vez al cierre sin fills inventados

**Observado:** Sólo emite OPEN por operación y MOVEMENT por tabla movimientos; no emite SUMMARY

**Repro/evidencia:** base `work/shot3/C`; evidence/boundary-first-run.log. Comando/ruta: See REPORT.md executable commands and cited source path

**Corrección concreta:** Emitir evento SUMMARY en closed_at con moneda observada/neto único

**Regresión obligatoria:** Ingest summary114 y movimientos120−4−2: ambas curvas114 y no228

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-09 — P0 — Fallo tardío de token viejo borra lease del nuevo; permanent reintentable

**Tipo/casos:** bug; H34. **Superficie propietaria:** v3/sdk/postgres/lab_analysis_service.go:98; v3/sdk/postgres/lab_analysis_service.go:430.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:98; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:430.

**Esperado:** Token viejo no cambia lease nuevo; permanente o5intentos no se reclama

**Observado:** FailAnalysisAttempt actualiza target sólo ns/ref sin owner/token; claim sin filtro status/intentos; backoff2/4/6/8/10

**Repro/evidencia:** base `work/shot3/C`; evidence/boundary-first-run.log. Comando/ruta: See REPORT.md executable commands and cited source path

**Corrección concreta:** CAS owner/token/lease en toda transición; estado retry terminal y backoff1/2/4/8/16 máximo5

**Regresión obligatoria:** Token7 expiry/token8/reporte7; error permanente;5fallos y nueva desired

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

**Corroboración fusionada:** F-04; reporte F y manifest independiente, sin contar de nuevo.

### C-10 — P0 — Publicador no valida vector de heads ni renueva heartbeat

**Tipo/casos:** bug; H34, H44. **Superficie propietaria:** v3/lab-worker/internal/workers/analysis_worker_v4.go:55; v3/sdk/postgres/lab_analysis_service.go:322; v3/sdk/postgres/lab_analysis_service.go:411.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/lab-worker/internal/workers/analysis_worker_v4.go:55; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:322; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:411.

**Esperado:** Locks inputs→target y CAS vector completo con heartbeat20s; lease perdido cancela; pointer RowCount obligatorio

**Observado:** Sin heartbeat; valida desired/token/lease sólo antes de inserts, sin owner/head/spec inputs ni locks compartidos; UPDATE pointer puede afectar0filas y attempt queda PUBLISHED

**Repro/evidencia:** base `work/shot3/C`; evidence/source-inspection.txt. Comando/ruta: See REPORT.md executable commands and cited source path

**Corrección concreta:** Implementar freeze/locks comunes y comparación completa, heartbeat y CAS RowsAffected=1 con reloj DB

**Regresión obligatoria:** HeadN+1 antes relay; expiry durante inserts; token y owner equivocados; pérdida ACK

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### D-04 — P0 — Stale cohort can be promoted after source advances

**Tipo/casos:** bug; H29, H32. **Superficie propietaria:** Ranking publication transaction.

**Fuente exacta:** echo/v3/lab-worker/internal/workers/analysis_worker_v4.go:164-195; echo/v3/lab-worker/internal/workers/lab_ranking_repository.go:237-243.

**Esperado:** Candidate must become obsolete when desired/source vector changes during compute.

**Observado:** Publish sets published_seq to current desired_seq without comparing captured vector.

**Repro/evidencia:** base `work/shot3/D`; source path evidence in REPORT.md §D-04. Comando/ruta: Adversarial interleaving source proof

**Corrección concreta:** Capture source vector/sequence and require transactional CAS before pointer promotion.

**Regresión obligatoria:** Pause after collect, advance source, resume; stale pointer remains unpromoted and dirty.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### D-05 — P0 — Publication error swallowed then dirty state cleared

**Tipo/casos:** bug; H32. **Superficie propietaria:** Ranking worker/repository.

**Fuente exacta:** echo/v3/lab-worker/internal/workers/analysis_worker_v4.go:145-159; echo/v3/lab-worker/internal/workers/lab_ranking_repository.go:72-77.

**Esperado:** Failed publication must keep prior pointer and retry signal.

**Observado:** Errors only logged; MarkClean advances published_seq regardless of snapshot success.

**Repro/evidencia:** base `work/shot3/D`; source path evidence in REPORT.md §D-05. Comando/ruta: Source path proof

**Corrección concreta:** Return errors; update sequence only inside successful snapshot transaction; remove MarkClean behavior.

**Regresión obligatoria:** Inject failures at each write; old pointer visible and desired remains pending.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-03 — P0 — Read bundle binds another strategy history and mixes generations

**Tipo/casos:** bug; H36, H37, H39, H40. **Superficie propietaria:** v3/sdk/postgres/lab_read_bundle_repository.go.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_read_bundle_repository.go:138; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_read_bundle_repository.go:221.

**Esperado:** Every row selects exact strategy/version/history selection and published generation; N metrics and details agree, and pending N+1 is stale metadata.

**Observado:** Synthetic PostgreSQL physical repro: A old net90/current20 gives net90 alongside gen-A-Nplus1/revision2; B net50 is pinned to history-A/gen-A-Nplus1. metrics_f scans all generation members and MAX(text); pin query joins any target to strategy version without linking target/member history to that strategy. is_stale hardcodedfalse.

**Repro/evidencia:** base `work/shot3/E`; logs/readbundle.log; repros/minimal-read-schema.sql; repros/readbundle.go. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Resolve selection/version and published generation once; join metrics and history members by scoped exact refs; persist same pin/vector and derive freshness from desired/head metadata.

**Regresión obligatoria:** Two strategies, each N/N+1; old90->20, B50; reverse insertion order; bundleN retained through publishN+1; all children/counts use same pin.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-08 — P0 — Direct economic children lack bundle owner scope

**Tipo/casos:** bug; H36, H41. **Superficie propietaria:** v3/hasura/metadata/tables/lab_v4_runtime.yaml, v3/sdk/postgres/migrations/074_lab_v4_read_models.up.sql, v3/front/src/components/lab/v4/StrategyDashboardV4.vue.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/hasura/metadata/tables/lab_v4_runtime.yaml:51; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/migrations/074_lab_v4_read_models.up.sql:93; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/components/lab/v4/StrategyDashboardV4.vue:107.

**Esperado:** Economic child reads carry authorized bundle owner+ns+generation/revision pin; knowing generation/history ID grants no access.

**Observado:** Curve/operations/movements/daily/distribution permissions filter namespace only. Views do not expose bundle/owner nor join a scoped bundle, permitting all same-namespace generations/histories by direct query. Frontend bypasses bundle via raw generation/history requests.

**Repro/evidencia:** base `work/shot3/E`; source-evidence.txt. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Expose child views/repository methods joined to owned bundle+row+generation/input refs; enforce session owner for both LAB roles and keep explicit namespace.

**Regresión obligatoria:** Two principals same ns with disjoint owned bundles; direct children, guessed refs, GraphQL/WS/actions must return no foreign bundle children.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-11 — P0 — V4 frontend retains admin-secret and legacy session fallback

**Tipo/casos:** bug; H41, H43. **Superficie propietaria:** v3/front/src/services/graphql/client.js, v3/front/src/services/config.js, v3/front/src/services/session_tokens.js.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/services/graphql/client.js:31; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/services/config.js:34; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/services/session_tokens.js:22.

**Esperado:** V4 HTTP/WS exclusively dedicated scoped LAB bearer; no VITE admin/control credential.

**Observado:** V4 service imports shared GraphQL client which sends admin secret when configured, else read/config legacy actor token. No LAB actor/session flow; prompt fallback repeated across components. Config still exports VITE admin/control variables.

**Repro/evidencia:** base `work/shot3/E`; source-evidence.txt; logs/browser-evidence.txt. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Remove public secret/control fallback for application and add dedicated LAB-scoped session acquisition/logout/cache cleanup.

**Regresión obligatoria:** Inspect built bundle and intercepted HTTP/WS headers with legacy/admin env present; never emit admin/control; scoped role only and logout clears bundles.

**Adjudicación:** CONFIRMED para la ruta frontend que permite credenciales administrativas/control. Presencia de una clave en v2 .env no prueba que esté vigente o haya sido publicada por v3; no se leyó ni usó su valor. Cualquier remediación de credencial compartida corresponde al owner autorizado.

**Corroboración fusionada:** F-05; reporte F y manifest independiente, sin contar de nuevo.

### F-02 — P0 — The documented rebase.sh stop path signals unowned pgboot processes and then restarts the database

**Tipo/casos:** bug; H48. **Superficie propietaria:** Shot2 harness teardown/setup script.

**Fuente exacta:** Shot2 harness/rebase.sh:8-26 (sha256: see evidence-manifest.json); Shot2 evidence/H48-TEARDOWN.md:1-7.

**Esperado:** A repeated cleanup must stop only manifest-owned PIDs, leave data untouched, release owned sockets, and remain stopped; a stop argument must not reset/restart services.

**Observado:** The spy observed pgrep -f pgboot-bin and TERM/KILL decisions for the returned sentinel PID without a manifest ownership check, an rm request for the harness pgdata directory, then setsid/dbexec/applybase calls. The script has no argument parsing, so passing stop still resets and starts PG. A multi-PID spy also showed zsh supplies the newline-joined list as one signal argument; errors are suppressed and reset proceeds.

**Repro/evidencia:** base `work/shot3/F/evidence`; ../work/h48/rebase_spy.sh; ../work/h48/spy-single.log; ../work/h48/run-single.log; ../work/h48/spy.log; ../work/h48/run.log. Comando/ruta: Instrumented copy only: work/h48/rebase_spy.sh stop, with H/MIG redirected into F-owned temp paths and PATH spies replacing pgrep/kill/rm/setsid/sleep; no real PID is signaled and rm is a logger.

**Corrección concreta:** Sustituir pgrep por nombre por PID/identidad/data-dir del manifest propio verificados. Implementar stop explícito sin reset/restart ni borrado; cleanup destructivo de data propia separado y posterior a retención de evidencia, idempotente, sin errores de stop ocultos. Nunca matar residuos ajenos encontrados por el audit.

**Regresión obligatoria:** With fake pgrep returning a foreign sentinel PID, assert no kill intent; run stop twice under spies and assert no rm, setsid, DB initialization, or external PID targeting, with before/after owner inventory unchanged.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### A-07 — P1 — Claimed t+60 test changes a field instead of emitting after a minute

**Tipo/casos:** test_gap; H07. **Superficie propietaria:** v3/sdk/postgres/master_vertical_test.go:77-94; v3/sdk/postgres/master_vertical_test.go:96-101.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/master_vertical_test.go:77-94; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/master_vertical_test.go:96-101.

**Esperado:** Real server first-byte clock; emit through ingress t_first_byte+60s within1s tolerance; readiness precedes emission; journal owner readback while LAB stopped.

**Observado:** Test runs Accept immediately with future ObservedAt and checks elapsed<60. It has no ingestion first-byte/commit/ready clocks, no real ingress, no worker lifecycle and no journal row assertion. Thus H07-nucleo PASS is unsupported even before A-01.

**Repro/evidencia:** base `work/shot3/A`; evidence/source-excerpts.txt; evidence/source-excerpts.txt. Comando/ruta: Inspect numbered source-excerpts.txt and complete repository caller searches; source-path proof, not runtime E2E

**Corrección concreta:** Replace with isolated physical timed ingress scenario; retain monotonic timestamps and source owner readback.

**Regresión obligatoria:** Record first-byte/commit/receipt/ready/master/journal monotonic values; reject early emission or outbox-only proof.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### B-03 — P1 — Parallel POST with the same idempotency key returns a unique violation instead of its receipt

**Tipo/casos:** bug; H02. **Superficie propietaria:** Echo HistoryServiceV2 receipt-first path and gateway POST handler..

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/strategy_history_v2_service.go:160-167,223-228,277-282,560-569; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/migrations/069_lab_v4_runtime_bindings.up.sql:195-210; contract:B — Forge Ingestion Readiness.md:132-138.

**Esperado:** Same scoped key+digest racing requests converge to the same stable receipt; one durable head/job and all callers get replay semantics.

**Observado:** Both txs see zero rows because txReceiptDigestConflict checks only `request_digest<>$4`. The receipt primary key admits one row; the losing INSERT yields 23505 and AcceptIngestionV2 wraps it as UNAVAILABLE/503.

**Repro/evidencia:** base `work/shot3/B`; evidence/h02_receipt_race.log; repro/h02_receipt_race.go. Comando/ruta: cd echo/v3/sdk && go run ../../../repro/h02_receipt_race.go

**Corrección concreta:** Lock on `(namespace, writer, idempotency_key)` or re-read the exact same-digest receipt under the transaction before any mutating work; return its immutable snapshot for a race winner.

**Regresión obligatoria:** 20 synchronized POSTs with same scope/key/body all return the same receipt and one head/outbox; same key/different body returns 409; simulated lost response plus GET-by-key recovers the committed receipt.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### B-04 — P1 — Multi-instrument identity is truncated to the first instrument

**Tipo/casos:** functional_missing; H01. **Superficie propietaria:** Echo V2 ingestion and runtime-definition crosswalk..

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/strategy_history_v2_service.go:238-242; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/strategy_ingestion_v2_registry.go:197-225; contract:B — Forge Ingestion Readiness.md:72,96.

**Esperado:** Persist every validated instrument ID in the version↔instrument relation and preserve exact declared coverage.

**Observado:** Only the first ID is inserted; all later IDs are discarded without error.

**Repro/evidencia:** base `work/shot3/B`; REPORT.md#hallazgos-principales. Comando/ruta: Source trace: AcceptIngestionV2 selects InstrumentIDs[0], passes a scalar `mainInstrument`, and the store inserts only instrumentArrayV2(mainInstrument).

**Corrección concreta:** Pass the complete instrument slice through the service/store and verify the existing normalized relation on replay; avoid inventing a primary symbol.

**Regresión obligatoria:** Ingest a strategy with two or more normalized instruments; direct SQL readback equals the full set; replay preserves it; conflicting or unknown IDs reject atomically.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### B-06 — P1 — History PUT drops correction/retraction temporal evidence

**Tipo/casos:** bug; H14. **Superficie propietaria:** HistoryServiceV2 PUT and history_change_entries persistence..

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/contracts/strategy_history_v2.go:179-193; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/strategy_history_v2_put.go:123-134; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/migrations/071_lab_v4_history_revisions.up.sql:164-186.

**Esperado:** Every correction/retraction revision retains the exact canonical change entry and its effective/known times so N/N+1/N+2 histories remain auditable.

**Observado:** The accepted digest covers the values, but durable history_change_entries loses them; persisted columns remain NULL and canonical_entry is empty.

**Repro/evidencia:** base `work/shot3/B`; REPORT.md#hallazgos-principales. Comando/ruta: Source trace: pass non-empty effective_at/known_at in Retractions; PUT's INSERT omits effective_at_ns/known_at_ns and supplies canonical_entry `{}`.

**Corrección concreta:** Encode the complete canonical ChangeEntryV2 and store exact epoch_ns evidence in the existing columns; keep entry rows append-only.

**Regresión obligatoria:** Correct +40→+30→0 with non-empty temporal evidence; read back all three immutable revisions and exact change entries; artifact/commit failure leaves no head advance or partial entry.

**Adjudicación:** CONFIRMED P1 para omisión de evidencia temporal en history_change_entries. No se demostró pérdida total del artefacto fuente; no se atribuye esa pérdida más amplia ni severidad P0.

### C-01 — P1 — SQN y Sharpe pierden el signo de la media

**Tipo/casos:** bug; H21, H22. **Superficie propietaria:** v3/sdk/lab/analyze/metrics.go:203; v3/sdk/lab/analyze/metrics.go:359.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/metrics.go:203; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/metrics.go:359.

**Esperado:** SQN[-1,-2]=-3 y Sharpe con media negativa <0

**Observado:** SQN=+3; Sharpe[-.01,-.02]=+40.52776825831888809262025

**Repro/evidencia:** base `work/shot3/C`; evidence/economic-repro.log. Comando/ruta: cd C/echo; GOMAXPROCS=2 go run -p=2 ../repro/economic_repro.go

**Corrección concreta:** Conservar signo de media al aplicar raíz y cuantización HE24

**Regresión obligatoria:** Medias negativas/cero/positivas, tanto SQN como Sharpe

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-02 — P1 — DailyBins omite días COMPLETE vacíos y desconoce GAP

**Tipo/casos:** bug; H22. **Superficie propietaria:** v3/sdk/lab/analyze/metrics.go:292; v3/lab-worker/internal/workers/analysis_worker_v4.go:79.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/metrics.go:292; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/lab-worker/internal/workers/analysis_worker_v4.go:79.

**Esperado:** 3 días completos => [.01,-.01,0]; GAP => insuficiente

**Observado:** Sólo2bins, status vacío; API no recibe coverage y worker usa from=0,to=mañana(now)

**Repro/evidencia:** base `work/shot3/C`; evidence/economic-repro.log. Comando/ruta: cd C/echo; GOMAXPROCS=2 go run -p=2 ../repro/economic_repro.go

**Corrección concreta:** Iterar calendario/coverage fijado en manifest y saldo arrastrado en from; publicar bins y razones

**Regresión obligatoria:** COMPLETE vacío/GAP/fin de semana/DST/carry-in; replay idéntico sin reloj actual

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-03 — P1 — Current drawdown CURVE_RUNNING devuelve máximo histórico de ventana

**Tipo/casos:** bug; H21. **Superficie propietaria:** v3/sdk/lab/analyze/metrics.go:117.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/metrics.go:117.

**Esperado:** peak12, ventana8→9: maxDD4/currentDD3

**Observado:** currentDD4

**Repro/evidencia:** base `work/shot3/C`; evidence/economic-repro.log. Comando/ruta: cd C/echo; GOMAXPROCS=2 go run -p=2 ../repro/economic_repro.go

**Corrección concreta:** Calcular current como peak running menos último valor; mantener max aparte

**Regresión obligatoria:** Fixtures D09 con recuperación parcial y total

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-04 — P1 — Batch sin causalidad total crea puntos intermedios y DD ficticio

**Tipo/casos:** bug; H17, H21. **Superficie propietaria:** v3/sdk/lab/analyze/timeline.go:160; v3/sdk/lab/analyze/timeline.go:202; v3/sdk/lab/analyze/oracles_test.go:280.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/timeline.go:160; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/timeline.go:202; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/oracles_test.go:280.

**Esperado:** −100/+100 simultáneos sin total => un punto delta0/DD0

**Observado:** dos puntos y primerDD100; test existente usa && y acepta2puntos

**Repro/evidencia:** base `work/shot3/C`; evidence/economic-repro.log. Comando/ruta: cd C/echo; GOMAXPROCS=2 go run -p=2 ../repro/economic_repro.go

**Corrección concreta:** Agrupar contribuciones por batch antes de actualizar capital/peak/DD y preservar contribuciones explicativas

**Regresión obligatoria:** Permutar IDs y payload: mismo DD/digest; total causal pérdida→ganancia conserva DD100

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-08 — P1 — Métricas del worker usan B inicial constante y exigen Q para money

**Tipo/casos:** bug; H16, H21. **Superficie propietaria:** v3/lab-worker/internal/workers/analysis_worker_v4.go:117; v3/lab-worker/internal/workers/analysis_worker_v4.go:133.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/lab-worker/internal/workers/analysis_worker_v4.go:117; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/lab-worker/internal/workers/analysis_worker_v4.go:133.

**Esperado:** open balance +200/−102 => PF200/102, money sinQ sigue contando terminal

**Observado:** terminalXFor usa B100 para ambos normalizados, constants ignoran C0/r; descarta cualquier operación sinQ incluso money

**Repro/evidencia:** base `work/shot3/C`; evidence/source-inspection.txt. Comando/ruta: See REPORT.md executable commands and cited source path

**Corrección concreta:** Construir terminal contributions con B sellado por perfil y filtrar sólo CLOSED completos; money independiente deQ

**Regresión obligatoria:** D01 PF100/51 vs2, C0/r custom, money sinQ y operaciónOPEN

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-11 — P1 — Composición estática D11 carece de motor/servicio/ruta

**Tipo/casos:** functional_missing; H24. **Superficie propietaria:** v3/gateway/internal/lab_v4_gateway.go:482; v3/lab-worker/internal/workers/analysis_worker_v4.go:55.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:482; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/lab-worker/internal/workers/analysis_worker_v4.go:55.

**Esperado:** D11 .6/.4 =>10018.8, cash residual, flat start, GAP bloquea

**Observado:** Tablas STATIC_COMPOSITION existen; rutas sólo ingestion/readbundles/histories/bindings y worker sólo LoadPinnedHistory

**Repro/evidencia:** base `work/shot3/C`; evidence/source-inspection.txt. Comando/ruta: See REPORT.md executable commands and cited source path

**Corrección concreta:** Servicio CAS composición+target y cálculo por miembro capital/peso/start propios, read model/UI integrado

**Regresión obligatoria:** D16 .6/.4 y .6/.3/.1, prestart,0weight,GAP positivo; no préstamos

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-12 — P1 — Límites de admisión/backpressure/deadlines no implementados

**Tipo/casos:** functional_missing; H46. **Superficie propietaria:** v3/gateway/internal/lab_v4_gateway.go:96; v3/sdk/postgres/strategy_history_v2_service.go:100; v3/lab-worker/internal/workers/analysis_worker_v4.go:35.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:96; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/strategy_history_v2_service.go:100; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/lab-worker/internal/workers/analysis_worker_v4.go:35.

**Esperado:** 1bulk/ns/proceso,4provision,2outbox,2compute;429RetryAfter2s y timeout120s/lock5s

**Observado:** No limiter/admission/Retry-After/deadline en ingreso; claim limitado2 no demuestra todos caps; H44 supera120s sin deadline

**Repro/evidencia:** base `work/shot3/C`; evidence/source-inspection.txt. Comando/ruta: See REPORT.md executable commands and cited source path

**Corrección concreta:** Admission scoped antes work/body y colas separadas; deadlines y receipt recovery explícitos

**Regresión obligatoria:** Saturación real con master/journal activos y commit incierto sin duplicar

**Adjudicación:** CONFIRMED por ausencia de admisión/deadlines en ruta fuente. El timeout H44 afectado por I/O no acredita por sí solo latencia de producto ni causalidad de backpressure.

### C-13 — P1 — Cota fixed24 no propaga error de capital/presupuesto y queda por debajo del error real

**Tipo/casos:** bug; H26, H44. **Superficie propietaria:** v3/sdk/lab/analyze/timeline.go:374; v3/sdk/lab/analyze/timeline.go:380.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/timeline.go:374; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/lab/analyze/timeline.go:380.

**Esperado:** E_delta>=|d/Q|*E_B+epsilon; E_B>=r*E_C+epsilon

**Observado:** C010000,r.01; Q3; ciclos d1 y d3000000: cota4e-24, error1000001/(3*10^24), mucho mayor

**Repro/evidencia:** base `work/shot3/C`; evidence/economic-repro.log. Comando/ruta: cd C/echo; GOMAXPROCS=2 go run -p=2 ../repro/economic_repro.go

**Corrección concreta:** Propagar recurrence conservadora por ciclo y contribución con ceil; razones explícitas de ambigüedad

**Regresión obligatoria:** Comparar racional ideal contra fixed24 y bound bajo ganancias grandes/pérdidas/casi cero y132805pasos

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### C-14 — P1 — Selección temporal AS_KNOWN no tiene servicio ni ejecución analítica

**Tipo/casos:** functional_missing; H20. **Superficie propietaria:** v3/gateway/internal/lab_v4_gateway.go:482; v3/sdk/postgres/lab_analysis_service.go:168; v3/lab-worker/internal/workers/analysis_worker_v4.go:79.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:482; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_analysis_service.go:168; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/lab-worker/internal/workers/analysis_worker_v4.go:79.

**Esperado:** knowledge14h reproduceN100; retrospectivaN+1=80; composición guarda selección revisionada

**Observado:** Gateway no monta selections; loader sólo dependency última revisión y worker todos los tiempos desde0; tablas no ejecutan semántica

**Repro/evidencia:** base `work/shot3/C`; evidence/source-inspection.txt. Comando/ruta: See REPORT.md executable commands and cited source path

**Corrección concreta:** Servicio selección CAS, manifest de knowledge/metadata/revisiones y motor temporal con períodos por apertura

**Regresión obligatoria:** N100known13h,N+1=80known15h/economic12h,cutoff14h y metadata de construcción corregida

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### D-01 — P1 — Invalid metric parse can manufacture zero input

**Tipo/casos:** bug; H30. **Superficie propietaria:** Echo ranking worker adapter.

**Fuente exacta:** echo/v3/lab-worker/internal/workers/analysis_worker_v4.go:175-184; echo/v3/shared-analytics/ranking/ranking.go:150-168.

**Esperado:** Required invalid/nonfinite metric must exclude or fail; never score default zero.

**Observado:** Malformed/nonfinite calc_decimal falls through as DEFINED zero and kernel accepts finite zero.

**Repro/evidencia:** base `work/shot3/D`; REPORT.md, D-01: ruta fuente exacta; el log H30-range sólo acredita D-02. Comando/ruta: Source path proof

**Corrección concreta:** Convert parse failure to typed exclusion/error; do not populate numeric zero.

**Regresión obligatoria:** NaN, overflow, empty and malformed values never produce eligible score.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### D-02 — P1 — Kernel accepts values outside required ranking range

**Tipo/casos:** bug; H30. **Superficie propietaria:** Shared ranking kernel and adapter.

**Fuente exacta:** echo/v3/shared-analytics/ranking/ranking.go; echo/v3/lab-worker/internal/metricinput/metricinput.go.

**Esperado:** abs(x)>1e150 must exclude with SCORE_NUMERIC_RANGE.

**Observado:** 1e151 scores 1.0/rank1 with no exclusion.

**Repro/evidencia:** base `work/shot3/D`; evidence/H30-range-repro.log. Comando/ruta: Independent copied-module repro

**Corrección concreta:** Enforce range at adapter and defensively in kernel.

**Regresión obligatoria:** ±1e150 boundary and immediately out-of-range values, singleton and cohort.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### D-03 — P1 — Eligibility ignores sealed 30x30 sample/window

**Tipo/casos:** functional_missing; H31. **Superficie propietaria:** Ranking collector/worker.

**Fuente exacta:** echo/v3/lab-worker/internal/workers/analysis_worker_v4.go:76-94,164-195; echo/v3/lab-worker/internal/workers/lab_ranking_repository.go:82-115.

**Esperado:** Require sealed context/window and >=30 terminal cycles and 30 full daily bins; exact digest selection.

**Observado:** Collector drops sample counts and metric/window digests; all DEFINED values go to MinMax.

**Repro/evidencia:** base `work/shot3/D`; evidence/H31-metric-subgates.log. Comando/ruta: Source path proof

**Corrección concreta:** Pin exact metric/window/context digests and counts; gate before scoring.

**Regresión obligatoria:** 29/30 and 30/30 cases plus reversed values across distinct windows.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### D-07 — P1 — Echo consumers violate Go 1.24 cold-build contract

**Tipo/casos:** functional_missing; H33. **Superficie propietaria:** Echo SDK/lab-worker module contracts.

**Fuente exacta:** echo/v3/sdk/go.mod:3; echo/v3/lab-worker/go.mod:3.

**Esperado:** H33 contract requires cold build with declared Go 1.24.

**Observado:** Both consumer modules require Go1.25.5.

**Repro/evidencia:** base `work/shot3/D`; evidence/H33-echo-go124.log. Comando/ruta: Cold Go1.24 go list attempt

**Corrección concreta:** Cumplir el gate Go1.24 original de ambos consumidores: identificar dependencias que exigen1.25.5 y hacer la adaptación mínima compatible, probando código y dependencias. Bajar sólo la directiva go sin build no resuelve el finding. No sustituir el criterio por un mínimo nuevo ni abrir una decisión Owner.

**Regresión obligatoria:** Cold-cache GOWORK=off build each consumer with supported version.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### D-08 — P1 — Symphony sqx effective consumer fails cold module resolution

**Tipo/casos:** bug; H33. **Superficie propietaria:** Symphony sqx module, if it remains effective owner.

**Fuente exacta:** symphony/sqx/core/domain/ranking_snapshot_per_type.go:4-5; symphony/sqx/go.mod; symphony/sqx/go.sum.

**Esperado:** Actual owner module must build with GOWORK=off and resolve published import.

**Observado:** go list -mod=readonly reports go.mod updates needed. Distribution tag/checksum PASS; workspace parity NOT_RUN because absent sibling SDK replacement target.

**Repro/evidencia:** base `work/shot3/D`; evidence/H33-symphony-sqx-readonly.log; evidence/H33-module-origin-checksum.json; evidence/H27-symphony-parity.log. Comando/ruta: Cold GOWORK=off readonly module resolution attempt

**Corrección concreta:** Add dependency to effective owner module if ownership is retained; verify cold module provenance.

**Regresión obligatoria:** Cold GOWORK=off compile sqx/core/domain and validate origin/checksum.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-01 — P1 — Gateway executable never supplies V4 configuration

**Tipo/casos:** bug; H36, H37, H41, H43. **Superficie propietaria:** v3/gateway/cmd/echo-gateway/main.go, v3/gateway/internal/server.go.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/cmd/echo-gateway/main.go:80; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/server.go:190.

**Esperado:** Executable loads validated scoped V4 configuration and mounts all I§3 routes; missing config gives503.

**Observado:** main.go omits LabV4 in ServerConfig; only tests inject it. Default executable leaves V2 unmounted, with404 instead of contract fail-closed503.

**Repro/evidencia:** base `work/shot3/E`; source-evidence.txt. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Load V4 config through SDK and pass it to ServerConfig; mount explicit503 handlers for misconfig.

**Regresión obligatoria:** Start actual executable against own ETCD/DB or config adapter; exercise mounted routes and missing-config503.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-02 — P1 — Mounted Hasura hook rejects scoped LAB sessions; helper accepts empty identity

**Tipo/casos:** bug; H41, H43. **Superficie propietaria:** v3/gateway/internal/server.go, v3/gateway/internal/hasura_auth_hook.go.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/server.go:130; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/hasura_auth_hook.go:50.

**Esperado:** Mounted hook emits UUID/ns/V4 role only after complete grant mapping; incomplete mapping503.

**Observado:** NewServer uses legacy hook; scoped LAB token returns401 with configured legacy reader. Unmounted V4 helper emits200 with empty user/ns.

**Repro/evidencia:** base `work/shot3/E`; logs/gateway-repro.log. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Mount validated V4 hook; validate principal UUID, namespace, role, permissions and duplicate tokens before enabling routes.

**Regresión obligatoria:** Actual mounted hook for reader/operator/producer; missing IDs/ns and role spoofing must fail closed.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-04 — P1 — Durable page drops score/rank and economic columns consumed by UI

**Tipo/casos:** bug; H37, H38, H39. **Superficie propietaria:** v3/sdk/postgres/lab_read_bundle_repository.go, v3/front/src/components/lab/v4/StrategyScreenerV4Table.vue.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_read_bundle_repository.go:333; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_read_bundle_repository.go:213; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/components/lab/v4/StrategyScreenerV4Table.vue:58.

**Esperado:** Page readback contains sealed score/rank and visible-profile metric values/status/unit.

**Observado:** Prepare has nonnil score/rank from ranking entries, but INSERT has no score/rank and Page SELECT never reconstructs them. Metrics/name live inside freshness_snapshot whereas table reads top-level row.net_change/name/etc. API page omits scores/ranks; screen renders dashes.

**Repro/evidencia:** base `work/shot3/E`; logs/readbundle.log; source-evidence.txt. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Persist canonical row presentation/pins including score/rank or reconstruct from immutable ranking snapshot; return typed metric columns/status at matching shape.

**Regresión obligatoria:** Compare prepare output, persisted row, first action page and next page against independent score/metric manifest; mount table with actual returned JSON.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-05 — P1 — Search and filters ignored; UI descending sort parsed as ascending

**Tipo/casos:** bug; H37, H42. **Superficie propietaria:** v3/gateway/internal/lab_v4_gateway.go, v3/sdk/postgres/lab_read_bundle_repository.go, v3/front/src/composables/useLabV4Bundle.js.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:194; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_read_bundle_repository.go:96; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/sdk/postgres/lab_read_bundle_repository.go:271; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/composables/useLabV4Bundle.js:33.

**Esperado:** Literal q and all G filters apply globally before ordering and pagination; ASC/DESC exact and unsupported sorts422.

**Observado:** HTTP query does-not-exist with filter{} returns2 rows. Source/run_mode/status IMPOSSIBLE filters each return2. SDK test of exact UI string net_change desc, strategy_ref ASC parses ASC because second token desc, differs from desc. LIKE escaping function unused; unknown sort defaults.

**Repro/evidencia:** base `work/shot3/E`; logs/gateway-repro.log; logs/readbundle.log; logs/sort-repro.log. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** One validated typed query shared REST/action; move q to filter semantics, implement allowlisted filters/literal escaping; structured sort directions or strict canonical parser.

**Regresión obligatoria:** q absent match0, literal%/_; source/mode/status filters; actual UI DESC payload; ties/nulls and20000 concatenation.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-06 — P1 — REST page path broken; Hasura accepts invalid/foreign cursors

**Tipo/casos:** bug; H41, H42. **Superficie propietaria:** v3/gateway/internal/lab_v4_gateway.go.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:232; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:337; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:386.

**Esperado:** Own page200; tampered400; foreign scoped404 or context409; limit1..200 rejected outside range.

**Observado:** Own UUID bundle REST page503: extracts read-bundles as UUID. Physical action returns200 for tampered cursor (ordinal0) and valid foreign owner/ns/bundle cursor (ordinal1), skipping rows. Limits0/201/-1/nonsense become50 and1junk becomes1.

**Repro/evidencia:** base `work/shot3/E`; logs/gateway-repro.log; logs/postgres.log. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Parse path segment4; shared cursor verifier must validate all context before SQL and propagate error; validate strict bounded integer limits.

**Regresión obligatoria:** Actual mounted REST/action with61 rows; own first/next, tampered byte, other bundle/owner/ns/query/sort, all boundary limits; no data or partial skip on invalid.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

**Corroboración fusionada:** F-06; reporte F y manifest independiente, sin contar de nuevo.

### E-07 — P1 — Hasura action transport and response cannot satisfy frontend contract

**Tipo/casos:** functional_missing; H37, H41, H42. **Superficie propietaria:** v3/hasura/metadata/actions.yaml, v3/gateway/internal/lab_v4_gateway.go, v3/hasura/metadata/actions.graphql.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/hasura/metadata/actions.yaml:8; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:356; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/hasura/metadata/actions.graphql:19.

**Esperado:** Assembled valid query action authenticates dedicated service and forwarded human; response supplies required row_count.

**Observado:** Metadata has no dedicated service header injection while handler requires it; human bearer not compared. Action response has no row_count, query_digest or ranking_snapshot_ref (row_count declared Int!). Required metadata builder absent; tracked views lack custom_root_fields lab_v4_* used by frontend. Hasura engine not applied; no claim that stub SQL demonstrates schema validity.

**Repro/evidencia:** base `work/shot3/E`; source-evidence.txt; logs/gateway-repro.log; logs/hasura-capability.log. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Implement additive metadata builder preserving legacy; declare valid action definitions/custom types/root fields and server env headers; validate service+human/session; return complete typed page.

**Regresión obligatoria:** Own Hasura metadata apply+inconsistency check and real scoped query returns row_count and page; no service/no human/mismatch rejected.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-09 — P1 — Curve/ranking selectors relabel unchanged data

**Tipo/casos:** bug; H38. **Superficie propietaria:** v3/front/src/composables/useLabV4Bundle.js, v3/front/src/components/lab/v4/StrategyLabV4Tab.vue, v3/front/src/components/lab/v4/StrategyDashboardV4.vue.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/composables/useLabV4Bundle.js:73; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/composables/useLabV4Bundle.js:34; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/components/lab/v4/StrategyLabV4Tab.vue:82; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/components/lab/v4/StrategyDashboardV4.vue:121.

**Esperado:** Curve choice changes profile columns/chart; ranking choice selects published cohort context independently and URL restores both.

**Observado:** Independent Vitest: Forge selection label changes but request calls1->1 and edge-snapshot retained; money selection sends no money profile. Backend always picks open_balance metrics while default label saysR, detail hardcodesR. No URL persistence for selector state.

**Repro/evidencia:** base `work/shot3/E`; logs/ui-tests.log; repros/ui.test.js. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Registry-backed profile/context selectors; choose immutable data per visible profile, prepare new ranking context bundle on ranking change, route state and explicit ranking input label.

**Regresión obligatoria:** Both rankings×4 profiles, navigate/back/reload; prove curve refs change independently and score bytes stable on curve-only switch.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-10 — P1 — Mandatory detail/selection/composition API and UI surfaces missing

**Tipo/casos:** functional_missing; H36, H37, H39, H40. **Superficie propietaria:** v3/gateway/internal/lab_v4_gateway.go, v3/front/src/components/lab/v4/StrategyDashboardV4.vue, v3/front/src/components/lab/v4/StrategyLabV4Tab.vue.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:474; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/components/lab/v4/StrategyDashboardV4.vue:119; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/components/lab/v4/StrategyLabV4Tab.vue:86.

**Esperado:** I§3 all commands/catalogs, scoped child reads; G dashboard calendar/distribution/DD/day drill; explicit history/version selection and static composition.

**Observado:** Only3 V4 Vue components exist. Detail has simple point/operations table; no daily/calendar/distribution/DD-window/history selector/copy/static composition. Commands/catalog/receipts not mounted; profile/ranking catalog404 and detail child405. Resolution service counts histories, never consults selection; unresolved rows can still get arbitrary generation.

**Repro/evidencia:** base `work/shot3/E`; source-evidence.txt; logs/gateway-repro.log. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Implement missing I§3 services/routes and G components on typed pin; selection version/primary alternatives + CAS+idempotency receipt; daily/distribution/DD use published outputs.

**Regresión obligatoria:** Full browser journey from unresolved->selection->detail->day->operation/movements, all states and command replay/CAS, 60/40 composition as D11.

**Adjudicación:** CONFIRMED, acotado a superficies API/UX, catálogos, receipts, detalle, copias y navegación faltantes. Motor D11 pertenece C-11 y semántica AS_KNOWN C-14; referencias cruzadas no son findings adicionales.

### E-12 — P1 — V2 read parser accepts unknown fields; unsupported encoding wrong status

**Tipo/casos:** bug; H43. **Superficie propietaria:** v3/gateway/internal/lab_v4_gateway.go.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:198; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/gateway/internal/lab_v4_gateway.go:413.

**Esperado:** Strict JSON schema rejects unknown/duplicate/trailing/deep malformed input400; unsupported Content-Encoding415 before processing.

**Observado:** Physical HTTP unknown field injected in read-bundle POST accepted200; gzip ingesta token gets400 INVALID_WIRE instead of415. readLimited never examines encoding; read DTO uses permissive json.Unmarshal.

**Repro/evidencia:** base `work/shot3/E`; logs/gateway-repro.log. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Use shared strict decoder/limits for every V2 DTO and validate encoding/media-type before read; preserve typed status distinctions.

**Regresión obligatoria:** Unknown/duplicate/trailing/depth/invalidUTF8 in real mounted endpoints, gzip415, oversize413, CAS428/412 and no side effects.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### E-13 — P1 — Freshness/error/navigation and detail paging incomplete

**Tipo/casos:** bug; H39, H40. **Superficie propietaria:** v3/front/src/composables/useLabV4Bundle.js, v3/front/src/components/lab/v4/StrategyDashboardV4.vue, v3/front/src/services/graphql/labV4Runtime.js.

**Fuente exacta:** echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/composables/useLabV4Bundle.js:46; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/components/lab/v4/StrategyDashboardV4.vue:131; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/components/lab/v4/StrategyDashboardV4.vue:165; echo@3b3ae81eb0905286324c899e122737f98dd45303:v3/front/src/services/graphql/labV4Runtime.js:51.

**Esperado:** PENDING/STALE/INSUFFICIENT/FAILED distinct; artifact503 preserves pin with error; navigation cancellation clears previous strategy; keysets include tie-breakers.

**Observado:** Composable maps any nonempty result READY regardless published status; fresh flag hardcodedfalse. Dashboard captures route params once in onMounted, swallows movement errors into empty array displayed as CLOSED_SUMMARY, uses opened_at-only pagination request with null comparison and no next-page loading; detail stops at200 ops/200movements/2000points.

**Repro/evidencia:** base `work/shot3/E`; source-evidence.txt; logs/browser-evidence.txt. Comando/ruta: See REPORT.md reproducibility commands

**Corrección concreta:** Model independent freshness/calculation/economic/error states; route watch/cancel and clear; preserve errors; scoped generation keysets+tie refs and actual pagination/downsampling.

**Regresión obligatoria:** PendingN+1, no generation, missing artifact503, empty versus unknown, navigateA->B same component,201same-time ops and movements with no omissions.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### F-01 — P1 — H47 guard allows a declared port already owned by another loopback process

**Tipo/casos:** bug; H47. **Superficie propietaria:** Shot2 harness guard / resource preflight.

**Fuente exacta:** Shot2 harness/guard/guard.go:46-76,85-105 (sha256: see evidence-manifest.json).

**Esperado:** Reject an occupied endpoint before opening a socket or using credentials; H47 explicitly lists an occupied-port negative case.

**Observado:** Guard.Allow returned nil while the sentinel listener still owned the manifest-declared endpoint. The probe opened no client connection and closed the listener on test exit.

**Repro/evidencia:** base `work/shot3/F/evidence`; ../work/h47/guard_test.go; ../work/h47/guard.go; ../work/h47/test.log. Comando/ruta: work/h47: GOWORK=off GOMAXPROCS=2 go test -count=1 -v ./...; test opens a 127.0.0.1 ephemeral sentinel listener, puts its occupied port in a private manifest, and calls Guard.Allow without dialing.

**Corrección concreta:** Separar reserva de puerto propio de permiso de conexión: bind/reserva atómica o prueba equivalente de PID/listener/data-dir/manifest antes de declarar ownership. El launcher QA valida además URLs y variables Vite resueltas, fallando antes de cargar credenciales o abrir browser ante destinos fuera del manifest; no imponer loopback al producto operativo.

**Regresión obligatoria:** Keep a loopback sentinel bound on an ephemeral port, declare it as the harness PG endpoint, and assert startup denies before any dial/credential lookup; assert an available owned ephemeral port passes.

**Adjudicación:** CONFIRMED como defecto de preflight/ownership del harness. F-07 se fusiona sólo como requisito de validar env resuelto del navegador antes del arranque; se rechaza exigir un allowlist loopback global al producto operacional.

**Corroboración fusionada:** F-07; reporte F y manifest independiente, sin contar de nuevo.

### QA-01 — P1 — Cobertura de código nuevo y caminos críticos sin certificación

**Tipo/casos:** test_gap; transversal H§10. **Superficie propietaria:** QA Shot4; paquetes nuevos/cambiados Echo/Symphony y rutas API/UI/SQL.

**Fuente exacta:** Contrato H§10; perfiles y denominadores de A/C/E.

**Esperado:** >=95% de código nuevo/cambiado por paquete y agregado ponderado, después de cubrir rutas críticas.

**Observado:** No hay medición integral del delta. Paquetes seleccionados: execution0%, accounting79.5%, analyze83.9%; pruebas adversariales gateway20.7% y postgres0.2% tienen denominadores de paquete, no del delta. No acreditan95%.

**Repro/evidencia:** base `.`; work/shot3/A/REPORT.md#coverage-and-limits; work/shot3/C/REPORT.md; work/shot3/E/coverage.json. Comando/ruta: Verificar perfiles y totales conservados en A/C/E y contrastarlos con el delta de código nuevo del candidato.

**Corrección concreta:** Medir cobertura sobre archivos/statements del delta exacto, conservar perfiles/denominadores y checklist de auth/CAS/lease/retry/temporal/economía/atomicidad. Corregir primero caminos críticos; después alcanzar95% sin tests espejo ni skips silenciosos.

**Regresión obligatoria:** Tests contractuales deben fallar sobre los SHAs Shot2 y pasar sobre el candidato corregido; race en concurrencia pertinente; cobertura del delta>=95% por paquete y agregado, además de gates físicos.

**Adjudicación:** CONFIRMED como brecha de certificación; no se infiere porcentaje de delta a partir de porcentajes de paquete.

### D-06 — P2 — Published membership omits required provenance vector

**Tipo/casos:** functional_missing; H32. **Superficie propietaria:** Ranking snapshot repository.

**Fuente exacta:** echo/v3/lab-worker/internal/workers/lab_ranking_repository.go:89-99,204-207.

**Esperado:** Each membership row pins run/config/history/input/curve/metric refs.

**Observado:** Insert stores only metric snapshot digest and eligibility/reasons; source query drops revision_no.

**Repro/evidencia:** base `work/shot3/D`; source path evidence in REPORT.md §D-06. Comando/ruta: Source path proof

**Corrección concreta:** Persist and validate per-member pinned generation manifest fields.

**Regresión obligatoria:** Two members with distinct run/config/history refs retain exact values.

**Adjudicación:** CONFIRMED; fuente y límites según evidencia indicada; no implica E2E auténtico.

### Gates residuales que no se pueden omitir

- H03/H04: carreras PUT/replay tras N+2, CAS412/428 y discrepancia header/body400; ocho historias y crash sin head/receipt/outbox parcial. B no los ejecutó completos. Corregir toda divergencia encontrada dentro de Shot4.
- H05: provisión real con profile/accounts propios, readback de StrategyDefinition/crosswalk/desired binding y motivos BLOCKED precisos. Fuente AUTH_FORGE sólo de copia autorizada existente; no generar campaña para conseguir fixture.
- H18/H23: atribución económica desde owner real (B5/A20 versus FIFO15/10) y agotamiento−1000→1000 con budgets previos; un reducer puro verde no prueba integración runtime.
- H27: preparar la dependencia SDK existente en workspace propio con ref verificada y correr builder Forge fijado + módulo + ambos adapters, bits completos. Ningún replace/copias del shared-analytics para evadir distribución; módulo efectivo sqx con requerimientos propios. H28 conserva su oráculo PASS como regresión.
- H44: mantener las132805 operaciones, Q heterogéneos, parciales/concurrencia/multiinstrumento, conteos/digests/extremos y política fixed24; repetir ingest<=120s, compute cuatro perfiles<=300s, worker peakRSS<=2GiB y staging<=2GiB. Medir upload/validate/commit/receipt/compute/publish separadamente con relojes monotónicos y RSS por proceso. Diagnosticar COPY/FK con catálogo/índices/EXPLAIN y storage/hardware declarados; no desactivar constraints para obtenerPASS. No asumir que C-10 explica por sí solo puntos0 de Shot2: inyectar pérdida/renovación de lease y readback de pointer/puntos para demostrar la causa corregida. N+1/replay masivos siguen pendientes.
- H45:20k estrategias, cuatro perfiles/dos cohortes completas, recalcular todos los scores afectados;100requests página50 y10lectores durante corrección1%; page1/50/200 sin omisiones. Cohorte<=30s, read generalp95<=2s, warm<=500ms/cold<=2s, prepare<=2s/response<=1MiB; detalle<=2000points p95<=1s/<=2MiB, límites browser originales. No sustituirlo por catálogo pequeño.
- H46/H49: saturación y backpressure físicos con master/journal preservados; native runner con MM real y sello causal previo al primer fill, recuperación/checkpoint/egress. Sin ETCD compartido ni órdenes económicas.
- Hasura: instalar/ejecutar engine sólo en recurso propio permitido cuando disponible; metadata apply/aditiva e inconsistency check, source login least-privilege, dos roles, dos principals mismo namespace y cross-namespace, acciones/WS/child SELECT y DML denegado. Su falta demostrada deja subgate físico BLOCKED_EXTERNAL, nunca paneles/auth faltantes como blocker.
- AUTH_FORGE/AUTH_ECHO: manifiesto raw/export/build/digests/lineage/identidad/moneda/costes/Q/fechas/cobertura real. NUM/SCALE/NEGATIVE etiquetados y separados, nunca visibles como evidencia de estrategias auténticas. Master simulado por contrato real puede demostrar owner journal; no vuelve auténtico un fixture Forge.
- QA-01: medir>=95% sobre nuevo/cambiado por paquete y ponderado, junto con todos los caminos críticos. Verificación final independiente debe usar source/build exactos, ejecutar regresiones contra el resultado corregido y reportar49 estados exclusivos. Ningún NOT_RUN se convierte por etiqueta en BLOCKED_EXTERNAL oPASS.

### Criterio de salida de Shot4

Todos los53 findings pertinentes corregidos y regresiones guardadas; alcance obligatorio completado; H01–H49 con evidencia owner/readback y una fila principal por ID; source/build/module/migrations/metadata/dataset manifest verificable; revisión independiente final dentro del mismo shot; cleanup físico y no interferencia con excepciones documentadas. Los únicos límites aceptables de certificación son gates físicos externos realmente impedidos y acreditados. Un defecto, implementación ausente, setup propio incompleto, timeout de producto o coverage faltante no es blocker externo. No declarar aceptación total si cualquier criterio obligatorio sigue fallando o sin evidencia.

Este paquete es técnicamente ejecutable pese a los defectos y subgates pendientes. No autoriza operar servicios compartidos, usar credenciales reales ni iniciar un quinto shot. Primary Manager entrega a GLM LOCAL el mandato final; esta sesión permanece abierta.

## Fuentes

[[10-projects/Echo/The Lab/V4 — Runtime Integration/SHOT3_ADVERSARIAL_REPORT|SHOT3_ADVERSARIAL_REPORT]], [[10-projects/Echo/The Lab/V4 — Runtime Integration/SHOT3_COVERAGE_MATRIX|SHOT3_COVERAGE_MATRIX]], contratos A–J y D09/D10/D11/D16–D24; manifests y repros A–F externos. `outputs/SHOT3_EVIDENCE_MANIFEST.json` fija la integridad de la evidencia.
