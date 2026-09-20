---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[Polymarket Engine — MVP]]"
sprint:
start: 2026-09-20
due:
progress: 0
repo: "https://github.com/xKoRx/polymarket-engine"
jira:
prs:
aliases:
  - PE-001
  - Sports Combinatorial
  - POC-S03
  - PE-001 Sports Combinatorial
tags:
  - kind/project
  - area/personal
  - domain/trading
  - tech/polymarket
  - topic/prediction-markets
created: 2026-09-20
updated: 2026-09-20
---

# POC-S03 — Sports Combinatorial

> [!info] Proyecto canónico PE-001 · implementación delegada
> **Padre:** [[Polymarket Engine — MVP]] · **Estado:** `PLAN_DOCUMENTED / LOCAL_GATE_PENDING` · **Progreso implementación:** 0% · **Presupuesto del ejecutor:** 10 horas · **Mecanismo:** basket CLOB sintético de dos compras · **LIVE:** deshabilitado. Esta nota es el único planificador persistente. El documento previo de research es evidencia, no otra fuente de tareas. Los gates y tests NO están aprobados por haber escrito este plan.

## 🎯 Objetivo

Implementar y validar una POC de `PE-001 — Sports Combinatorial` que descubra únicamente relaciones demostrables entre un full-game Moneyline del equipo A y el full-game spread del mismo equipo con handicap negativo `-h`, `h>0`, bajo reglas contractuales equivalentes de periodo y overtime. Demostrar `Cover(A,-h) => Win(A)`, comprar conceptualmente `YES(ML A)` y el outcome exactamente complementario de `YES(Spread A -h)`, construir matriz finita completa de payouts, barrer asks L2 y aplicar fees reales/resueltas. Producir evaluaciones reproducibles `ACCEPT | REJECT | INCONCLUSIVE`, razones, referencias de prueba y revisión, tests adversariales, SCREEN/REPLAY y SHADOW no-live honestos. Un ACCEPT sólo significa que el snapshot y supuestos pasan los filtros; no demuestra fill ni autoriza LIVE.

**Hipótesis falsable:** las reglas dan una cota inferior de payout de una share por par de patas cuando cubren exhaustivamente los estados terminales; algunas cotizaciones pueden tener `worst_payout > acquisition_cost_with_fees` bajo L2 válido. E1 refuta relaciones falsas; E2 rechaza edges inexistentes tras profundidad/fees/legging; E3 observa prospectivamente oportunidades reales sin presuponer rentabilidad. E1/E2 fixture-grade pueden aprobar técnicamente aunque E3 siga `REAL_EXECUTION_DATA_BLOCKED`, que nunca se convierte en PASS económico.

**No hacer:** arbitraje nativo Combinatorial Positions, Combos/RFQ, NegRisk conversion, mercados period/half-time, DSL, solver general, otro book, otra base contable, un `BasketExecution` alternativo, órdenes, wallet, signer, promoción de versiones ni cambios a Echo/Forge. Mecanismo A CLOB exclusivamente. No crear otro proyecto planner PE-001.

## 📊 Estado actual

- **Research:** `PE-001 — Deep Research & Implementation Handoff — 2026-09-19`, adjunto originalmente al encargo. La hipótesis, taxonomía, 22 casos lógicos y experimentos están documentados. Su reporte de remoto atrasado (`a8b2067`) está SUPERSEDIDO por la inspección posterior: engine remoto `main@9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5`, comprobado el 20-09-2026. Investigación del venue no produjo dos books reales L2 contemporáneos con IDs/rules completos; `REAL_EXECUTION_DATA_BLOCKED` es estado vigente, no inferir resultados.
- **Código remotamente inspeccionado:** `internal/strategy/api.go` (`Strategy`, `Factory`, `Frame`, `Opportunity`, `Assessment`, `EvaluationContext`), `internal/economics/economics.go` (`WalkSide`, `BuildQuote`), `internal/frames/dispatcher.go`, `internal/catalog/relationships.go`, `internal/regimes/service.go`, `internal/account/coordinator.go`, `internal/experiment/experiment.go` y `cmd/engine/replay.go`. Esto NO verifica el checkout local ni reejecuta la certificación M4.
- **Seam crítico L2:** `strategy.Frame.Assets` transporta `frames.AssetSnapshot`, actualmente BBO/contador de niveles y revisiones, NO el book completo. `economics.BuildQuote` exige `BookView` con niveles. Strategy no recibe conexiones ni repositorios. Nunca consultar latest/reconstruir L2 dentro de `Detect/Evaluate` ni poner un `BookView` ficticio a partir de BBO. Resolver un proveedor as-of-cut desde el owner que compone el frame; inyección in-memory declarada es válida sólo para fixtures E1/E2. Si no existe seam causal real, E3 queda BLOQUEADO, no inventado.
- **Seam crítico fees:** `regimes.ResolveFee` conserva `POINT/INTERVAL/UNRESOLVED/SUSPECT`; `economics.BuildQuote` hoy aplica coeficiente BPS al `sweep.Notional`. La documentación Polymarket Sports consultada el 20-09-2026 expresa `shares * feeRate * price * (1-price)` con redondeo a 5 decimales y tasa de categoría Sports 0.05, sujeta al feeSchedule vigente de cada market. La equivalencia no está demostrada. Antes de ACCEPT, comparar fórmula con un oracle independiente y resolver el campo semántico/tasa/versiones reales; si la fee no puede demostrarse, `INCONCLUSIVE`, sin fee cero. El `FeeResolver` existente NO convierte fee ausente en cero.
- **SHADOW actual:** `experiment.RunShadow` está asociado a `neutral.Factory`, crea books sintéticos de BBO con 10 shares por lado y fees unresolved; no certifica capacidad, fill ni PnL PE-001. `cmd/engine/replay.go` verifica manifest y ejecuta replay de observación/delivery, no certifica por sí solo evaluations PE-001.
- **Engine seguridad:** parent declara `M4_CERTIFIED_NON_LIVE` para baseline `9ae5dde` y cobertura 95% por paquete; no heredar certificado a PE-001. `main` remoto comprobado, `local HEAD/branch/status = NOT_VERIFIED`. No se ejecutaron build/vet/test/race en esta preparación; ninguna fixture es un test Go materializado todavía.
- **Plan:** SPEC semántica/matemática v1 decidida; integración condicionada al gate P0 y pruebas de seams. `PLAN_DOCUMENTED / LOCAL_GATE_PENDING`; trabajo autorizado sólo en fases y archivos indicados. La presencia de esta nota en `master` no prueba materialización mediante script, lint local, disponibilidad de Graphify ni ausencia de cambios de otros escritores: el ejecutor valida eso una sola vez en P0 y registra el resultado.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/polymarket-engine` | `main` remoto verificado; worktree local de desarrollo por verificar en P0 | Remote inspected `9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5`; pin real local requerido | `## SPEC funcional v1` en esta nota | `## SPEC técnica v1` y `## Integración y data contract` en esta nota | DOCUMENTED; CODE NOT STARTED; local gate pending |
| `xKoRx/agents-os` | `master` remoto; local desconocido | Commit de creación verificable en GitHub; no confundir con HEAD local | Este planner | Schema `project` v1, WPs, fixtures y gates aquí | Planner publicado; lint/Graphify local NOT_RUN |

**Ownership:** el agente de Daedalus usa su mecanismo de escritura/sync local y no usa Git/push en el checkout Agents-OS. Esta restricción NO aplica a esta sesión de preparación, cuyo escritor es la integración GitHub autorizada por el owner. Para el engine, respetar la policy específica del workspace y nunca `reset --hard`, `clean`, `stash`, force-push, cambio de branch o overwrite sobre trabajo de terceros. El padre, Edge Research, otras POCs y certificación M4 son read-only para el coding agent salvo la única tarea puente de supervisión que gestionará el owner de Agents-OS.

## 🧩 Subproyectos

Ninguno. Un único proyecto de agente y una sola tarea puente humana en `[[Polymarket Engine — MVP]]`; el agente jamás marca `[x]` la supervisión. Si el padre ya contiene puente PE-001, reutilizar; no duplicar. El backlink por `parent` ya resuelve la relación de proyecto; el puente se reconcilia con una lectura exacta del padre para no sobrescribir sus ~428 KB o trabajo concurrente.

## ✅ Tareas

- [ ] **P0 / T0.1:** Cold/warm bootstrap Agents-OS una sola vez; verificar identidad de esta nota, checkout/HEAD/branch/status, versiones, writers, schema/lint; fijar allowed files y baseline real. #owner/agent #type/admin #area/personal
- [ ] **P0 / T0.2:** Inspeccionar seams reales `Frame`/L2, `BuildQuote`/fees y `Assessment`/evidence; ejecutar oracle fee independiente y dejar mapping de símbolos/tests/fixtures; sin reabrir arquitectura. #owner/agent #type/research #area/personal
- [ ] **A / T1.1:** Implementar relación RS-ML-SP con proof completo de dos rules, identidad, same full-game period/OT, complemento probado, estados excepcionales y contraejemplos. #owner/agent #type/dev #area/personal
- [ ] **A / T1.2:** Matriz explícita, oracle worst-payout, hashes/provenance, fail-closed unknown, límites y tests F01–F05/F13–F17/F22. #owner/agent #type/dev #area/personal
- [ ] **A / G1:** Tests semánticos críticos PASS; registrar evidence y pasar gate a `review`, nunca autoaceptar. #owner/agent #type/testing #area/personal
- [ ] **B / T2.1:** Factory, params, Universe, `RequiredData`, `Detect` con ordering, dedup, caps e identity pins; test F05/F07/F12/F14/F15. #owner/agent #type/dev #area/personal
- [ ] **B / T2.2:** `Evaluate` consume proof y mismo frame, depth L2, VWAP exacto y fees Sports por nivel/rounding; Risk y residual sequential; tests F06–F12/F18–F21. #owner/agent #type/dev #area/personal
- [ ] **B / G2:** E2 PASS con oracle fee, L2, revisions, partial; evaluación sin evidencia => INCONCLUSIVE. Dejar en review. #owner/agent #type/testing #area/personal
- [ ] **C / T3.1:** Registrar Strategy y conectar SCREEN/REPLAY vía runtime compartido, sin snapshot latest ni dataset fabricado. #owner/agent #type/dev #area/personal
- [ ] **C / T3.2:** Integrar SHADOW/Experiment as-of sólo con captura L2 causal; sin datos, E3=DATA_BLOCKED honesto, exportar scorecard y provenance. #owner/agent #type/dev #area/personal
- [ ] **C / T3.3:** Ejecutar fixtures nativas F01–F22, build/vet/test/race y >=95% por paquete tocado; regresión no-live, auditoría de cambios, reporte verificable. #owner/agent #type/testing #area/personal
- [ ] **C / G3:** Entregar a Review humana; agente no declara GO económico ni activa órdenes. #owner/agent #type/supervision #area/personal

## SPEC funcional v1

### 1. Identidad, mercado, prueba y población

Una relación elegible requiere: `Gamma event_id` exacto que contiene ambos market IDs; `Gamma market_id` distintos; `condition_id` y `CTF asset_id` por outcome, NO intercambiables; evidencia de alineación outcome↔token; reglas completas con source refs, content hashes y known-at; mismo evento deportivo canónico/participantes/score basis/full-game/OT, handicap negativo inequívoco y `h>0`; relation proof `Cover(A,-h) => Win(A)` y complemento del mercado spread basado en el par binario observado. Títulos/fuzzy matching, membership en evento, NegRisk o alineación visual jamás prueban implicación. Si la fuente sólo informa winner o spread text sin rules suficientes, `INCONCLUSIVE`, sin falso ACCEPT. Un contrapayout posible que invalide la implicación => `REJECT/RULES_CONTRADICT`.

`SYNTHETIC` y `OBSERVED_REAL` son orígenes separados. Caso público NFL Bears–Eagles 2025 sirve como ejemplo semántico histórico, NO fixture ejecutable: IDs, L2 simultáneos y fee historical faltan. Caso Commanders–Eagles full-game vs second-half demuestra no equivalencia de periodo/OT. No inventar IDs reales. Para E3 incluir TODOS los eventos full-game elegibles capturados prospectivamente durante ventana preregistrada, con denominadores y missingness, no seleccionar por precio/profit posterior.

### 2. Matriz terminal y fórmula

Sea `Δ = score_A - score_B` bajo la misma convención contractual. Basket de cantidades iguales `q` para `YES(ML A)` y `opposite(YES(Spread A -1.5))`. `S_BIG Δ>=2 => [1,0], total q`; `S_MIDDLE Δ=1 => [1,1], total 2q`; `S_LOSS Δ<=-1 => [0,1], total q`. `S_TIE` se añade con payout contractual cuando el deporte admite empate; `S_CANCEL` es `[0.5,0.5]` únicamente cuando AMBAS reglas concretas prueban resolución 50/50; postponement no equivale a settlement; abandono/forfeit/retirement/dispute/resolution asíncrona se incluyen sólo si rules completas determinan consecuencias. Cualquier rama desconocida `⊥` => assessment INCONCLUSIVE: no eliminarla del min, reemplazarla por 0/1 ni asumir refund. `BasketPayoff(s)=Σ_i q_i*P[i,s]`, `WorstPayoff=min_s BasketPayoff(s)` si y sólo si todos los payouts son conocidos, `WorstNet=WorstPayoff-ΣGrossCosts-ΣFees-CostesExplícitos`; mathematical edge si `WorstNet>min_worst_net` configurado. El estado intermedio después de sólo una pata puede tener pérdida aun si el basket completo tiene floor positivo: ambas propiedades se prueban por separado.

### 3. Límites y decisiones cerradas

Una única family `RS-ML-SP`, exactamente 2 BUY legs, shares iguales por pareja en grid configurado, máximo 8 estados terminales y 1024 pares por evento; duplicados de token prohibidos, ordering por IDs canónicos estable. Si el espacio excede límites, `INCONCLUSIVE/COMPUTE_LIMIT_EXCEEDED` sin evaluación parcial presentada como universo completo. No solver, no derivación automática de proof por título. El grid de research `10/25/50` es orientativo y no ley venue. `max_book_age` y `max_inter_leg_skew` son parámetros de manifest/experiment, no constantes globales de Polymarket; fixtures B0 usan respectivamente 2s y 250ms. El safety margin real debe preregistrarse; fixture B0 usa 0. Live denegado.

### 4. Economía, ejecutabilidad y capital

BUY camina asks de cada token desde el mejor precio hacia arriba; cada nivel aporta `take=min(available,remaining)`, `Gross_i=Σprice_level*take_level`, `VWAP_i=Gross_i/q_i` sólo si profundidad suficiente. Nunca midpoint/last trade/best-ask multiplicado por tamaño como coste ejecutable. Validar tick, min-size, accepting-orders, freshness, cross-book skew, revision vector, quota CPU y cantidad redondeada; un book actual no puede sustituir el book al corte del frame. Fee market-specific vigente: usar oracle independiente `fee_level=shares_level*effective_feeRate*price_level*(1-price_level)`, redondeo de venue 5 dp aplicado conforme contrato observado a unidad de fill/orden; no asumir dónde redondea si esa granularidad no fue validada, en cuyo caso INCONCLUSIVE. Para POINT resuelto calcular exacto; INTERVAL usar upper fee conservadora sólo cuando fórmula y bounds son semánticamente compatibles, registrar incertidumbre; UNRESOLVED/SUSPECT => INCONCLUSIVE. No inferir fee universal por bps nominales. `WorstNet>threshold` no implica fill: someter a partial/leg-reprice stress con `BasketPolicy SEQUENTIAL`, residual worst loss y `risk.Evaluate` existente. FOK evita partial intraleg sólo si la orden individual es fillable; no atomicidad interleg. Capital lock, settlement esperado vs real, release y gap de inventario son métricas/estado, nunca una rentabilidad anualizada inventada.

### 5. Assessment y reason semantics

`ACCEPT` sólo si identidad/proof/matriz completa, libros L2 válidos/as-of, quantity feasible, fee compatible/resuelta, worst-net superior al threshold y política residual/risk pasan. `REJECT` para contradicción demostrada, mercado/amount inválido, depth insuficiente, stale book o coste ejecutable que elimina el margen. `INCONCLUSIVE` para falta de evidencia, payout unknown, fees irresueltas, revisión cambiante, book no causal, límite computacional. Conservar reason model congelado de `strategy.Assessment.ReasonCodes`, no inventar enum core. Razones de SPEC: `RELATION_UNVERIFIED`, `RULES_CONTRADICT`, `TERMINAL_STATE_INCOMPLETE`, `DUPLICATE_INSTRUMENT`, `STALE_BOOK`, `FRAME_INCONSISTENT`, `FEE_UNRESOLVED`, `INSUFFICIENT_DEPTH`, `EXECUTABLE_MARGIN_NON_POSITIVE`, `PARTIAL_FILL_RISK_EXCEEDED`, `CONSTRAINT_REVISION_CHANGED`, `COMPUTE_LIMIT_EXCEEDED`; mapear aliases existentes sin pérdida de semántica. `INCONCLUSIVE` NO se suma a `REJECT` en estadísticas.

## SPEC técnica v1

### 1. Algoritmo acotado

`catalog identity → exact full-game markets → explicit RS-ML-SP proof → finite terminal equivalence classes → complete payout matrix and hash → deterministic candidate → frame/cut/revisions → depth as-of → fee/regime snapshot → economics.WalkSide + correct Sports fee oracle → worst net → partial-fill/Risk → strategy.Assessment and experiment lineage`. No I/O dentro de callbacks Strategy. Reaprovechar actors/runtime y decimal foundation. `Opportunity` sólo admite `ID/Description/Assets`: la prueba estructurada no cabe ahí; diseñar almacenamiento in-memory de evidencia por instancia de Strategy keyed por deterministically unique `opp.ID` y `frame ordinal/revision`, bounded y reseteado por generación; NO consultar repositorio ni serializar proof arbitrario en Description. Si `Evaluate` no encuentra matching pinned proof, `INCONCLUSIVE`. Si el ownership existente proporciona un mejor metadata/evidence seam verificable en P0, usarlo; no modificar Strategy API frozen sin PR/decisión explícita.

### 2. Compatibilidad con HEAD inspeccionado remotamente

| Owner / archivo | Símbolo real | Uso / restricción |
|---|---|---|
| `internal/strategy/api.go` | `Factory.New(map[string]string)`, `Strategy.Describe/Universe/RequiredData/Start/Detect/Evaluate/Observe/Stop`, `Frame`, `Opportunity`, `Assessment`, `EvaluationContext` | Package nuevo implementa API; ninguna conexión, repo, wallet o send callback. `Frame` recibe `Assets/Quality/RevisionVector/VirtualTime`. |
| `internal/catalog/relationships.go` | `Reducer.applyRelationships`, rels containment, NegRisk membership, complement | NO hay `IMPLICATION` intermarket probada. Dejar proof RS-ML-SP en lógica PE001 con rule refs pinneadas. |
| `internal/catalog/inspect.go` | `Service.InspectEntity` / `EntityInspect` revisions, outcomes y relaciones | Resolver identidades y rules desde view ya durable fuera de callbacks; no usar latest en Evaluate. |
| `internal/regimes/service.go` | `Service.Constraint`, `AssetConstraint`, `ConstraintSnapshot`, `FeeResolution` | Constraint revision y fee evidence; no inventar fee unknown=0. |
| `internal/frames/dispatcher.go` | `OwnerState` / `OwnerSnapshot` | BBO/Levels; no full L2 en estado publicado. No derivar tamaño desde Levels. |
| `internal/economics/economics.go` | `WalkSide`, `ExecutableDepth`, `BookView`, `BuildQuote` | Sweep real reusable; fee de BuildQuote necesita oracle/semantics fix comprobado antes de aceptar Sports. |
| `internal/risk/risk.go` | `Policy`, `Snapshot`, `Evaluate` | Pure policy para capital lock; no risk engine duplicado. |
| `internal/account/coordinator.go` | `PlanBasket`, `BasketPolicy SEQUENTIAL`, reserve/reconciliation | Account owner del lifecycle; Strategy sólo declara candidate/policy. Nada de órdenes en esta POC. |
| `cmd/engine/replay.go` | `runManifestBuild`, `runReplay` | Manifest y schedules; para PE001 el test E2E debe probar que Strategy efectivamente se evalúa, no confundir replay de delivery con evaluación. |
| `internal/experiment/experiment.go` | `RunShadow`, `toStrategyFrameSafe` | Neutral-only y 10 shares BBO sintéticas: hay que reemplazar/aislar para PE001, sin false profitability. |

Todos los paths/símbolos anteriores refieren a `xKoRx/polymarket-engine@9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5`, NO garantizan HEAD local en Daedalus. En P0 verificar cambios sobre estas interfaces con `git diff`/lectura focalizada y actualizar esta tabla antes de tocar código. `screen`/`RunShadow` pueden abrir capture con efectos de boot/recovery: correr únicamente contra dataset temporal aislado y pinneado, no RS v0.3 activo; para lectura auténtica priorizar `capture.OpenView` cuando proceda. No afirmar que SHADOW es read-only por nombre.

### 3. Data contract versionado `PE001-INPUT-v1`

Un registro para cada candidato debe poder resolver antes de Detect/Evaluate: `event_id`, `canonical_game_id` o evidencia equivalente de same-score-basis, `market_id[2]`, `condition_id[2]`, `asset_id[2]`, `outcome_index[2]`, `rules_source_ref[2]`, `rules_content_hash[2]`, `rules_known_at[2]`, `relation_template=RS-ML-SP`, `relation_version=1`, `proof_hash`, `state_schema_hash`, `matrix_hash`, `frame_id/run_generation/cut_seq/virtual_time`, `catalog_revision/universe_revision/relationship_revision/regime_revision`, `book_hash[2]/book_source_timestamp[2]/book_known_at[2]/book_epoch[2]`, `L2 asks[2]`, `fee_kind/fee_schedule_source/fee_revision`, `tick/min_size/accepting`, `quantity_grid/min_worst_net/max_age/max_skew/max_residual_loss`, `source_origin=SYNTHETIC|OBSERVED_REAL`. Estos son campos lógicos del input/provenance, NO una promesa de que un struct actual los tenga; mapear al contrato owner actual en P0. La identidad de un book depende de token + hash/epoch/cut, no del título.

**Read consistency:** ambos books y rules deben ser cognoscibles al mismo cut; si `observed_seq>cut`, source timestamp futura, epoch perdió snapshot full, gap sin recuperarse, missing fee revision o cambio de constraints entre Detect/Evaluate, `INCONCLUSIVE/NOT_REPRODUCIBLE` según taxonomy existente. Time skew sólo acota simultaneidad, no crea transacción atómica. Persistencia mínima por opportunity: `template_id/version, proof_hash, state_schema_hash, matrix_hash, market+token IDs, frame/cut/revision vector, quote_inputs_hash, assessment/reasons, run+manifest`. Guardar matriz completa una vez por proof/fixture; no crear tablas propias si Experiment soporta evidence refs. IDs en manifest/evidence, NO etiquetas Prometheus de cardinalidad infinita. En replay: un mismo hash de inputs devuelve ordered IDs/proof/assessments idénticos; ningún lookup a latest state.

### 4. Archivos y fronteras de modificación

**CREATE preferido:** `internal/strategy/sportscombinatorial/` para Strategy/Factory, model/proof, bounded evidence store y tests; fixtures en testdata bajo el ownership existente según P0; un manifest experimental PE001 dentro de ubicación canónica del engine si existe. **MODIFY condicional y mínima, por owner:** composición `cmd/engine/screen.go`/`internal/experiment` para seleccionar factory y dataset; `internal/frames`/`internal/books` únicamente para full L2 as-of-cut con ACK/provenance y tests, aprobado en P0; `internal/economics` únicamente para corrección fee contract con test negativo y regresión de todos los usos. **NO TOUCH por defecto:** Catalog tables/relationships generales, `regimes.FeeResolverV1` a ciegas, `internal/account` state machine, Risk policy, Simulator reducer, `internal/strategy/api.go` frozen, migration DB, web order APIs, wallets, prod config, M4 manifests/certifications, notas de otros POCs. Si un seam exige cambio de interfaz frozen o toca otro writer: `PLAN_CONFLICT`, registrar owner y prueba, no ampliar scope silenciosamente.

### 5. Seguridad, despliegue y reversión

Modo `SCREEN/REPLAY/SHADOW` exclusivamente; `LIVE_DISABLED`, no lease, no real orders, no signer/wallet/order POST, no autenticación trading. Cualquier wiring de nueva factory sin gate de modo se rechaza. No usar capture RS v0.3 activo para tests: copia temporal verificable por SHA/cutoff, sin boot de active store. Rollback = desregistrar PE001 factory/config experimental y revertir exclusivamente commits PE001 autorizados en worktree propio; NO revertir commits ajenos, no borrar journal, no manipular orden/ledger. No migración requerida por diseño; si surge necesidad real de schema, detener phase y registrar impacto antes de modificar.

## Fixture pack reproducible — B0 + F01–F22

**Base B0 100% sintética:** `origin=SYNTHETIC`, event `SYN-EV-001`, game `SYN-GAME-001`, teams A/B full-game incl OT, ML market `SYN-MKT-ML-A`, condition `SYN-COND-ML-A`, token `SYN-TOK-ML-A-Y`; spread A-1.5 market `SYN-MKT-SP-A15`, condition `SYN-COND-SP-A15`, YES `SYN-TOK-SP-A15-Y`, opposite `SYN-TOK-SP-A15-N`; binary complement proven. Rules: ML YES=A wins full-game; spread YES=A wins by >=2 incl OT; cancellation with no makeup resolves 0.5/0.5 on BOTH; postponement remains open. BUY ML YES 20 shares and BUY Spread opposite 20 shares. Matrix states `BIG:[1,0],MIDDLE:[1,1],LOSS:[0,1],CANCEL:[0.5,0.5]`; frame at `2026-09-20T19:00:00.100Z`, both books at `19:00:00.000Z`, each bids `0.44×20`, asks `0.45×20` followed by `0.46×20`, tick `0.01`, min-order amount compatible with q20, accepting=true, fee POINT market rate `0.05` with the documented Sports formula, revisions catalog10/universe20/relationship30/regime40/bookML50/bookSP51, max_age=2s/max_skew=250ms (fixture values), sequential max residual loss=5 pUSD, min_worst_net=0. Expected `WorstPayoff=20`, gross18, fee each `20*0.05*0.45*0.55=0.24750`, total fee0.49500, cost18.49500, WorstNet1.50500, exactly one ACCEPT. Estos números no son cotizaciones del venue. El test exige oracle fee independiente; si fee semantics real no coincide con este fixture, la evaluación productiva debe quedar INCONCLUSIVE hasta corregir.

| ID | Delta exacta respecto de B0 | Expectativa verificable |
|---|---|---|
| F01 | B0 sin cambios | 1 candidate ACCEPT; floor20/cost18.495/net1.505. |
| F02 | Proof HYPOTHESIS sin rules_hash | INCONCLUSIVE RELATION_UNVERIFIED; no economics profit. |
| F03 | Spread FIRST_HALF, ML full-game; contraestado cover H1 y pierde final | REJECT RULES_CONTRADICT. |
| F04 | Matrix omite CANCEL aunque rules la declaran | INCONCLUSIVE TERMINAL_STATE_INCOMPLETE; no min sobre subset. |
| F05 | Segunda pata usa el mismo token/condition que la primera | REJECT DUPLICATE_INSTRUMENT. |
| F06 | Books timestamps 18:59:57.000, frame19:00:00.100 | REJECT STALE_BOOK (age3.1s>2s). |
| F07 | ML book19:00:00.000, spread19:00:00.500, max skew250ms | REJECT FRAME_INCONSISTENT (skew500ms). |
| F08 | Fee unresolved y schedule ausente | INCONCLUSIVE FEE_UNRESOLVED; no fee cero. |
| F09 | Spread asks 0.45×6 + 0.46×4 sin más niveles, q20 | REJECT INSUFFICIENT_DEPTH (10<20). |
| F10 | Por pata bid0.42×20; asks0.44×1,0.52×19; q20 | Midpoint top aparente rentable; gross/pata10.32, fee/pata0.24944, cost basket21.13888, WorstNet -1.13888 => REJECT; oracle calculado con fee formula y regla de redondeo declarada. |
| F11 | ML BUY20@.45 ejecuta primero, segundo ask desaparece, segundo fill0 | Cash spent incl fee9.24750, ML pierde en LOSS, residual worst=-9.24750 < -5 => abort/re-evaluate, REJECT PARTIAL_FILL_RISK_EXCEEDED; NO exposición oculta. |
| F12 | Detect regime40, Evaluate regime41 | INCONCLUSIVE CONSTRAINT_REVISION_CHANGED, no latest silent re-quote. |
| F13 | Terminal CANCEL probado 50/50 en ambos | Basket payout20, permanece cubierto; jamás refund implícito. |
| F14 | 1025 pares con IDs SYN-CAND-0001..1025, cap1024 | INCONCLUSIVE COMPUTE_LIMIT_EXCEEDED; no entregar 1024 como universo completo. |
| F15 | Otro event_id con mismos títulos A vs B | No candidate o INCONCLUSIVE RELATION_UNVERIFIED. |
| F16 | Etiquetar ML/spread relation como equivalencia | Rechazar equivalencia: MIDDLE demuestra payoff [1,1]; relation correcta IMPLICATION. |
| F17 | ML regulation-only y spread incluye OT; regulation draw y luego A cover OT | REJECT RULES_CONTRADICT. |
| F18 | Market resuelto cambia lifecycle revision durante Evaluate | INCONCLUSIVE; no old-book con nuevo settlement. |
| F19 | Spread asks=[] | REJECT INSUFFICIENT_DEPTH. |
| F20 | Fee revision cambia durante evaluación | INCONCLUSIVE; re-quote solo tras new Detect/cut. |
| F21 | Rounding real convierte margen pre-round >0 en feasible WorstNet<=0 | REJECT; el agente materializa vector exacto tras identificar rounding real (no inventar escala interna). |
| F22 | Mismo input hash 2 ejecuciones, schedules {1} y {32}, sin state external | IDs ordenados/proof hash/matrix hash/assessments idénticos, sin latest lookup. |

**Oracle y prioridad de tests:** first critical behavior (unknown proof, incomplete matrix, fee unresolved, stale/invalid L2, partial-fill, revision race, no live) y después coverage. No false ACCEPT permitido, incluso si coverage global es alto. Conservar fixtures válidas/rechazadas/inconclusas como denominadores distintos. Todos los datos SYN- deben ser claramente sintéticos en logs y reports. F21 y tests de integración con file names quedan materializados en B; no afirmar ejecutados durante planificación.

## Experimentos, scorecard y aceptación

| Experimento | Entradas | Gate de PASS técnico | Qué NO prueba |
|---|---|---|---|
| E1 Semantic Correctness | F01–F05,F13,F15–F17 | Identidad y proof/contraejemplo exactos; matriz completa; unknown no ACCEPT; bounded deterministic | Arbitraje presente. |
| E2 Economic Correctness | F06–F12,F14,F18–F22 + F01 | Fee per-level y redondeo con oracle; exact depth/VWAP; revisions/partials; F10/F11 REJECT; F22 replay determinista | Fill real y beneficio neto realizado. |
| E3 Venue Evidence | Prospective raw WS + Gamma rules + market feeSchedule + L2 same cut | IDs/lineage completos, capture coverage y denominadores, episodes, executable capacity, reason breakdown, latency/skew, residual loss/capital lock; sin datos => DATA_BLOCKED declarado | PnL live. |

E3 preregistrable posterior: 14 días como ventana propuesta del research, todos los full-game elegibles del universo fijado antes del inicio, no cherry-pick; reportar eventos descubiertos/elegibles/capturados/candidatos/semánticamente válidos/executable-estimated, incoherentes, sin fee/depth, capacidad por size, lifespan y sesgo de capturas. No afirmar observación de 14 días hoy. E3 NO es requisito para aprobar E1/E2; cualquier afirmación de edge económico requiere E3 y validación separada posterior. Promoción LIVE es otro proyecto/certificación, nunca resultado de esta POC.

## Hoja de ruta 10 horas — fases y gates

**Presupuesto orientativo cerrado para una sesión:** P0 0h45m; A 2h15m; B 3h30m; C 3h; certificación/entrega 0h30m = 10h. No convertir tiempos en garantía ni ocultar bloqueo. Si P0 revela cambio frozen o imposible as-of L2 en las 10h, entregar A+B fixtures y C SCREEN/REPLAY si pueden ser honestos; E3 queda explícitamente DATA_BLOCKED, nunca incluir books inventados. Si falta owner acceptance de un gate, el agente se detiene en `review` y NO inicia fase siguiente autónomamente. El owner puede preautorizar progresión mediante recibos separados; esta nota no la preautoriza.

| Gate | Estado al planificar | Evidencia exigida al agente | Aceptación owner habilita |
|---|---|---|---|
| G0 P0 baseline/seams/schema | pending | HEAD/branch/status, file map real, exact fee oracle, dataset isolation, schema/lint y ownership | A |
| G1 semantic/E1 | pending | fixtures semánticas + proof hash + contraejemplos/unknown, tests y diff | B |
| G2 economic/E2 | pending | fee formula verified, VWAP/depth/revisions, partial risk, F10/11, tests + oracle | C |
| G3 integration/technical | pending | SCREEN/REPLAY run Strategy real, SHADOW real-or-DATA_BLOCKED, all gates/tests, coverage, no LIVE | Owner Review |

El agente escribe sólo `review|blocked|rejected`; el owner escribe `accepted`. Una fase rechazada reabre sólo sus tareas. La nota es la fuente de tareas; no llevar planner persistente paralelo, ni fake agent_run o test receipts. Cada hito deja timestamp, SHA y suite exacta en `## 📆 Bitácora`.

### Paquete autónomo Fase 0 — P0 baseline y seams

**Misión exacta:** verificar checkout y convertir el mapa remoto de contratos en un mapa local pinneado, sin implementar producción. **Precondiciones verificables:** esta nota existe una vez y enlace parent correcto; sync/writers local revisados. **Lectura obligatoria:** secciones Estado/Entrega/SPEC técnica de esta nota; `AGENTS.md`, Strategy API, Frames, Books, Economics, Regimes, Experiment, SCREEN/REPLAY y tests owner relevantes. **Decisiones cerradas:** mecanismo A, family RS-ML-SP, no LIVE, no otra DB/solver. **Implementación paso a paso:** resolver `VAULT_ROOT`; ejecutar bootstrap once y workflow de proyecto; comparar Git remoto `9ae5dde` con HEAD real sin alterar worktree; comprobar writers/capture, elegir área aislada, verificar `git status`; encontrar seams L2 causales y fee market-specific, mapear existing Assessment reason/evidence; fijar branch/base/allowed files y test commands; comprobar schema/lint y Graphify de la nota, registrar diferencias. **Archivos esperados:** MODIFY sólo esta nota para mapping; ningún código. **No tocar:** checkout ajeno, M4, otros proyectos, live. **Spikes permitidos:** inspección read-only focalizada de Frame→Books, fee formula/regime y SHADOW dataset opening; timeout al presupuesto P0, registrar PLAN_CONFLICT si requieren cambio frozen. **Tests y asserts:** correr baseline build/test sólo si aislamiento/runtimes permiten; no declarar PASS no ejecutado; oracle fee contra libro B0. **Entregables/Gate G0:** evidencia exacta y gate review. **Handoff:** contrato local de datos/fees y allowed files, nada de research global.

### Paquete autónomo Fase A — WP-A1 modelo semántico

**Misión exacta:** crear detector semántico y oracle de matrices sin acceso a red. **Precondiciones verificables:** G0 accepted. **Lectura obligatoria:** SPEC funcional y F01–F05,F13–F17,F22; `internal/strategy/api.go`, Catalog identity/relationships y foundation decimal. **Decisiones cerradas:** exactly two legs, explicit template, 8 states, unknown fail-closed. **Implementación paso a paso:** definir typed proof/ref con rule hashes; verificar IDs/event/period/OT/complement; generar estados finitos y exception branches; comprobar completeness y contraejemplos; calcular worst payoff y determinismo; añadir tests. **Archivos esperados:** CREATE `internal/strategy/sportscombinatorial/` model/proof/tests (nombres fijados por agente), testdata scoped. **No tocar:** core Strategy API, Regimes, Economics, Account, DB. **Spikes permitidos:** únicamente mapear fields de rule DTO ya identificados; ausencia => proof INCONCLUSIVE, no parser universal. **Tests y asserts:** F01–F05,F13–F17,F14,F22; nunca false ACCEPT; no overflow. **Entregables/Gate G1:** test receipts E1, diff y proof samples; estado review. **Handoff:** proof/model hash y API Strategy-local estable, sin dependencias arquitectónicas nuevas.

### Paquete autónomo Fase B — WP-B1 Detect + WP-B2 Evaluate/Economics

**Misión exacta:** implementar Strategy real, cuantificar economics sin false profitability y acotar riesgo secuencial. **Precondiciones verificables:** G1 accepted. **Lectura obligatoria:** SPEC funcional/económica, Data Contract, interfaces de Strategy, Frames/Books, Economics/Regimes, Risk, Account/Simulator y F06–F12,F18–F21. **Decisiones cerradas:** cash cost depth/fee por nivel, no latest, no otro executor, no live. **Implementación paso a paso:** Factory valida parámetros; Universe/RequiredData declaran assets y budgets; Detect selecciona pares exactos, dedup/ordering/caps y pin proof+frame; adaptar L2 fixture cut-aligned al quote real; fee oracle y corrección owner Economics mínima aprobada si necesaria; Evaluate prueba revisions/age/skew, WalkSide y rounded cost; risk/residual step1/step2; producir Assessment con bounded ActionCandidate sólo en ACCEPT. **Archivos esperados:** MODIFY/CREATE dentro `internal/strategy/sportscombinatorial/`; MODIFY condicional Economics y seam Frames/Books sólo con evidencia P0; tests/fixtures. **No tocar:** live, Account state machine, Catalog schema, M4 manifests. **Spikes permitidos:** corrección pura de fee por fill + as-of snapshot mínima; si requiere contrato frozen mayor, detener el seam y dejar E3 DATA_BLOCKED. **Tests y asserts:** F01,F05–F12,F14,F18–F21; oracle fee=0.24750 por pata B0 y F10 negativo; F11 residual risk, revision race; regresiones owners afectados. **Entregables/Gate G2:** E2 evidence exacta, diff controlado, estado review. **Handoff:** Factory lista, params/fixtures, fee semantics verificadas o bloqueadas con reasons; no economic GO.

### Paquete autónomo Fase C — WP-C1 SCREEN/REPLAY/SHADOW y aceptación

**Misión exacta:** conectar runtime de PE001 y producir una certificación técnica NO-LIVE honesta. **Precondiciones verificables:** G2 accepted. **Lectura obligatoria:** SPEC, observabilidad/E1–E3 y `cmd/engine/screen.go`, replay/manifest, experiment/shadow, test harness y M4 safety gates. **Decisiones cerradas:** dataset temporal aislado, Strategy seleccionada explícita, no depth sintética como venue. **Implementación paso a paso:** wiring factory selection sin romper neutral; SCREEN evalúa mismo cut con Assessment+reasons; REPLAY reconstruye mismas candidates/evaluations desde manifest pinneado, no solo digest de delivery; SHADOW real usa L2/rules/fee evidence y, si no puede, emite DATA_BLOCKED sin profit; scorecard separa denominadores, capture completeness, costs, capacity y lock; correr tests y verificar safety. **Archivos esperados:** MODIFY mínimo `cmd/engine/screen.go` y `internal/experiment` cuando sus owners lo autorizan; CREATE tests/experiment fixture scoped. **No tocar:** capture activo, órdenes, wallet, live config, otras POCs, M4 certificates. **Spikes permitidos:** composition root selection/data snapshot with proof; si falla E3 no falsificar ni bloquear E1/E2. **Tests y asserts:** F01–F22, two replay schedules deterministic, `go build ./...`, `go vet ./...`, `go test ./...`, `go test -race ./...`, cobertura >=95% por paquete cambiado (calcular denominator real); safety negative capability; fixture dataset es synthetic. **Entregables/Gate G3:** baseline+changed paths+receipts+E1/E2/E3+coverage+SHADOW lineage y estado review. **Handoff:** owner evalúa evidencia y marca bridge Review; nunca agent Done.

## Observabilidad, recuperación y Definition of Done

Registrar `candidates_generated`, `semantic_valid`, `semantic_reject`, `economic_reject`, `inconclusive`, `estimated_executable`, `quantity`, `worst_payoff`, `gross_cost`, `fee_cost/fee_kind`, `worst_net`, `book_age`, `cross_book_skew`, `depth_used`, `residual_worst`, `capital_required`, `settlement/lock` si observado, `run/manifest`, `proof_hash`, `frame_id`, `revision_vector`, `assessment_reason`. IDs de alto cardinal en report/evidence, no labels métricas. Falta real dataset => emitir contador/razón `DATA_BLOCKED` con causa específica. Política de retries sólo para lectura transitoria fuera del hot path Strategy; no reintentar silenciosamente con latest ni mutar la evaluación original.

**DoD técnico:** G0–G3 accepted por owner; E1/E2 todas fixtures pertinentes pasan con razones/cifras; SCREEN y REPLAY realmente invocan PE001; determinismo; SHADOW sólo usa L2 causal o queda BLOCKED sin score ficticio; build/vet/test/race y coverage con paths/baseline; no LIVE capability nueva; planner actualizado y puente parent en Review, nunca Done. **DoD económico separado:** E3 prospectivo completo + investigación posterior; no es parte de esta entrega de 10h.

## 📆 Bitácora

- **2026-09-20 — PLANNING GITHUB:** investigación PE001 integrada con mapa de código `polymarket-engine main@9ae5ddec`, cuatro WP en tres fases más P0, 22 fixtures definidas, 10h, seams L2/fees/SHADOW explícitos, gates 0–3 y mandato de desarrollo. Estado CODE_NOT_STARTED; local engine/vault HEAD, schema materializer/lint, Graphify, pruebas, E3 y parent bridge pendientes de verificación; no se inventa receipt. Esta nota se crea por la conexión GitHub autorizada, no por el agente local Daedalus; el commit GitHub es la evidencia de escritura remota.

## 🧭 Decisiones

| ID | Estado | Resolución | Evidencia/autoridad | Consume |
|---|---|---|---|---|
| ADR-001 | TECHNICAL_RESOLUTION | Basket sintético CLOB; native Combinatorial Positions y Combo RFQ excluidos | Research mecanismo A/B/C y engine account | Todas |
| ADR-002 | TECHNICAL_RESOLUTION | Full-game Moneyline + opposite spread, implication sólo rule-proven | Rules y matriz RS-ML-SP | A |
| ADR-003 | TECHNICAL_RESOLUTION | Templates explícitos+matriz, sin solver/DSL | 2 legs/8 states/1024 pairs | A/B |
| ADR-004 | TECHNICAL_RESOLUTION | Unknown fee/payout/book/revision => INCONCLUSIVE | M1 invariantes y oracle | A–C |
| ADR-005 | TECHNICAL_RESOLUTION | Reutilizar Strategy/Economics/Account/Simulator/Risk/Experiment owners | Engine SHA inspeccionado | B/C |
| ADR-006 | TECHNICAL_RESOLUTION | B0 threshold0, q20, age2s, skew250ms, residual5 son parámetros de fixture, NO policy live | Research B0 | E1/E2 |
| ADR-007 | TECHNICAL_RESOLUTION | E1/E2 fixture-grade separadas de E3 y LIVE | Experimentos | C |
| ADR-008 | BLOCKED_AT_G0 | HEAD/branch/status/writers locales, materializer/lint y mapping final | Sin acceso local | P0 |
| ADR-009 | BLOCKED_E3_ONLY | L2 full as-of-cut y fee Sports fórmula no probados compatibles; no venue-ready sin evidencia | Código Strategy/Quote/Shadow | B/C |

## 🔗 Docs / Links

- Parent: `[[Polymarket Engine — MVP]]`, `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md` relativo a `VAULT_ROOT`.
- Research: `30-resources/polymarket/Polymarket — Edge Research Consolidado 2026-09-16.md`; Technical Platform Map canónico `30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`.
- Deep Research original: `PE-001 — Deep Research & Implementation Handoff — 2026-09-19`, reporte adjunto a la conversación; esta nota incorpora su alcance/fixtures/casos y no exige repetir su investigación.
- Engine code: `https://github.com/xKoRx/polymarket-engine/tree/9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5`.
- Agents-OS: `80-agents/agents-os/agents-os.md`, `80-agents/skills/agents-os-agent-project-workflow/SKILL.md` y `80-agents/skills/agents-os-implementation-planning/SKILL.md` relativos a VAULT_ROOT.
- Docs venue: `https://docs.polymarket.com/market-data/market-details`, `https://docs.polymarket.com/market-data/prices-order-books`, `https://docs.polymarket.com/trading/fees`, `https://docs.polymarket.com/concepts/resolution`, `https://docs.polymarket.com/trading/orders`, `https://docs.polymarket.com/trading/positions/combinatorial`, `https://docs.polymarket.com/trading/combos/overview`.

## 💡 Ideas

POST-POC únicamente: alternative spreads/totals, sport-specific proofs, native Positions/Combos, generic optimizer, capacity sizing, tiny-live certification tras investigación separada.

## MANDATO ÚNICO PARA EL CODING AGENT — 10 HORAS

**PROMPT COMÚN:** Actúa como Principal Go Engineer implementando únicamente `PE-001` en `xKoRx/polymarket-engine`. La autoridad de trabajo es ESTA nota `[[POC-S03 — Sports Combinatorial]]`, no la conversación ni un scratch plan. Tienes 10 horas de trabajo como presupuesto, no como justificación para saltar gates. Resuelve bootstrap Agents-OS y proyecto una vez; verifica local HEAD/status y writers; respeta la policy local: NO usar Git/push para sincronizar Agents-OS desde el agente Daedalus. No interpretes esta regla como prohibición para el planner remoto que ya publicó el documento. No rehagas research ni abras arquitectura. E1/E2 son metas técnicas; E3 real puede quedar DATA_BLOCKED. Implementa sólo fase asignada, actualiza tareas/bitácora tras cada gate real, guarda archivos/tests y evidencia, no inventes PASS, no modifiques otros proyectos/owners, no cambies API frozen sin PLAN_CONFLICT. No ejecutar órdenes, no habilitar live, no usar wallets/secrets ni tocar capture activo. Unknown/fee/as-of falta => INCONCLUSIVE, nunca zero/default/latest; midpoint no es coste ejecutable; FOK no es basket atomic; residual riesgo interleg obligatorio. Trabaja según `## SPEC funcional v1`, `## SPEC técnica v1`, `## Fixture pack reproducible` y el paquete autónomo asignado. Al terminar, deja gate en `review`, no aceptes gate propio ni inicies la siguiente fase sin receipt owner. Si 10h no alcanzan, entrega los caminos críticos cubiertos, fixtures-grade y bloqueo preciso, no silencio.

**DISPATCH P0 — enviar con PROMPT COMÚN y ningún otro dispatch:** `FASE_ASIGNADA=P0; PAQUETE_CANONICO="Paquete autónomo Fase 0 — P0 baseline y seams"; GATE_REQUERIDO=none; TAREAS=T0.1,T0.2; SALIDA=local baseline+seams+lint/ownership+G0 review; STOP=G0 review, no A`.

**DISPATCH A — sólo tras G0 accepted:** `FASE_ASIGNADA=A; PAQUETE_CANONICO="Paquete autónomo Fase A — WP-A1 modelo semántico"; GATE_REQUERIDO=G0 accepted; TAREAS=T1.1,T1.2; SALIDA=proof/matrix/tests+G1 review; STOP=no B`.

**DISPATCH B — sólo tras G1 accepted:** `FASE_ASIGNADA=B; PAQUETE_CANONICO="Paquete autónomo Fase B — WP-B1 Detect + WP-B2 Evaluate/Economics"; GATE_REQUERIDO=G1 accepted; TAREAS=T2.1,T2.2; SALIDA=Strategy+fee/depth/risk tests+G2 review; STOP=no C`.

**DISPATCH C — sólo tras G2 accepted:** `FASE_ASIGNADA=C; PAQUETE_CANONICO="Paquete autónomo Fase C — WP-C1 SCREEN/REPLAY/SHADOW y aceptación"; GATE_REQUERIDO=G2 accepted; TAREAS=T3.1,T3.2,T3.3; SALIDA=integrations+all receipts+G3 review; STOP=no LIVE/no owner acceptance`.

**REPORT CONTRACT:** `STATUS=PE001_TECHNICAL_PASS|PE001_PARTIAL|PLAN_CONFLICT; BASELINE=local sha/branch/status; AGENTS_OS=planner/lint/bridge log; PHASE=tasks+gate; CHANGES=exact files; TESTS=commands/pass-fail/coverage; E1/E2/E3=denominators+results+DATA_BLOCKED reasons; SAFETY=non-live verification; BLOCKERS=owner/seam/proof; NEXT=one action`. No `agents-os-session-close` salvo pedido explícito.