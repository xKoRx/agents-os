---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[A — Product Contract — The Lab]]"
  - "[[B — Architecture Decision Report]]"
  - "[[C — Reality and Gap Matrix]]"
  - "[[D — Revised Roadmap]]"
  - "[[E — First Usable Vertical Slice]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-09-22"
updated: "2026-09-22"
---

# F — Decision Register

> **PROPOSAL / OWNER RATIFICATION REQUIRED, 2026-09-22.** Registrar decisión ≠ ratificarla. No sobrescribe frozen Echo SDK/E04/E05/E10 ni autoriza código, migración, deploy o órdenes. Producto [[Echo — Producto Integrado]], plan [[D — Revised Roadmap]], primer slice [[E — First Usable Vertical Slice]].

## A. Decisiones de producto ya expresadas por Rodrigo — preservadas

| ID | Decisión / alcance expresado | Estado |
|---|---|---|
| P01 | The Lab = historia individual por estrategia, N curvas, métricas/screener, posteriormente portfolios; TIME_TO_USABLE_TRADING_SYSTEM | OWNER REQUIREMENT en mandato 22-09. |
| P02 | Dos fronteras A/B y tres períodos principales TRAINING_DATA/PRE_REAL/REAL; IS/OOS solo subtipo training | OWNER REQUIREMENT; detalles de inclusividad/crossing requieren ratificación técnica T02. |
| P03 | Forge aporta históricos SQX y MT5 auténticos y evidencia, Echo recibe/normaliza y posee analytics; no Forge→PG Echo, no segunda ingestion | OWNER REQUIREMENT; disponibilidad física de dos listas aún no demostrada, gate H0. |
| P04 | REAL = Reference Echo observada, Execution account separada, versionado de estrategia sin fragmentación por cambio de cuenta | OWNER REQUIREMENT; política de proyección longitudinal T03. |
| P05 | Operaciones y raw evidence preservadas, curvas derivadas, métrica/ranking nunca autoridad factual; no concatenar superposición arbitraria | OWNER REQUIREMENT; identity/dedup method T04. |
| P06 | No candle/intrabar backtesting ni automatización de broker gap recovery; no activar trading, no PROD/DEV shared mutations durante review | OWNER REQUIREMENT, CLOSED scope. |
| P07 | Primera certificación producto sobre una estrategia auténtica Forge; el chequeo físico va en primer hito y no bloquea documentación arquitectónica | OWNER REQUIREMENT, roadmap H0. |

## B. Propuestas técnicas con aprobación explícita necesaria

| ID | Propuesta exacta | Motivo/evidencia | Consecuencia si no se aprueba |
|---|---|---|---|
| T01 | Mantener Echo SDK/E05/E04; extender mismos boundaries de forma aditiva; detener temporalmente E10 T06–T10 mientras se entrega V0 y política sample no ratificada | E05 SPEC dice foundation y no curve product; E10 M7 proyecta `UNRATIFIED_PROVISIONAL` en policy, no autoriza T06…; F04/E04 join ya PASS | Replan debe declarar prioridad alternativa y su costo en tiempo usable; no mutar E10 por esta nota. |
| T02 | Usar UTC instantes y `[−∞,A)`, `[A,B)`, `[B,+∞)`; pertenencia al abrir, puntos al cerrar, cruzadas visibles longitudinales pero excluidas de métricas estrictas de segmentos contaminados | Evita pertenencia doble y leakage posterior a frontera; precio/PnL no spliteable sin mercado | Definir nueva convención con mismas garantías y fixtures de crossing antes del primer sellado. |
| T03 | Una `HistoryRevision` publicada por StrategyVersion y selección A/B/política; versiones múltiples solo en proyección family longitudinal rotulada, no quality de una versión | Inmutabilidad, version reset E10, cambio cuenta no puede partir la historia | Riesgo de mezclar versiones o perder continuidad; ratificar scope alternativo explícito. |
| T04 | SQX tiene autoridad TRAINING, MT5 PRE_REAL, Reference REAL, pero sólo después de verificar rangos/individual trades; native IDs dedupe local, match cross-source por referencia económica evidenciada; ambigüedad cuarentena | F05 HTM verified no prueba dual trade lists, E04 receipt no valida analytics | Definir otra política versionada con prueba de equivalencia, jamás fallback heurístico silencioso. |
| T05 | E05 immutable TradeSet/NDJSON remains authority for selected operation set; PG relational `canonical_operation_index` is rebuildable, digest-checked read projection, same PG, no Mongo mirror; history publication CAS | E05 stores sealed sets and metric writer, no indexed operation/time queries demonstrated; report/source gap | Si se elige autoridad por filas en vez de sellos, SPEC debe definir una sola fuente y atomic sealing, nunca dos write masters. |
| T06 | Static in-process Go CurveCalculator registry ID/version/config/definition digest with CurveRun+CurvePoints; MetricCalculator E05 reuse, path metrics additive one semantic catalog; first R/pips/conditional equity | E05 calculator computes metrics, not temporal curves; no path data for alternative stops | Provide equally simple extension with deterministic input identity, no second engine. |
| T07 | E04 existing INGESTED stays operative acceptance; append independent analytics readiness/provenance and durable retry; missing MT5 never downgraded operational truth nor made ready | E04 SPEC acceptance copies operational artifact and three DB objects, 201 not analytics permission | Owner must define different non-destructive status split, tests for replay/partial failure. |
| T08 | Preserve F01…F05, E01…E09 verified scope; E10 M7 manager re-review and sample policy separate ratification; E11…E13 defer/split UI first | Sep21 Factory V2 FULL 3 finalists/E04 golden, E10 Sep22 T05 pending review | Alternative work order must demonstrate earlier complete usable strategy than H0–H4. |
| T09 | First screen/metric comparison cohorts must share exact strategy version selection policy/period/calendar/basis/currency/formula; no cross-basis rankings; gaps unknown vs zero | E05 SPEC §3 existing Lab AUTO and UI win_rate mismatch, reference coverage unknown | Explicit other comparison semantics with provenance and warnings; not silent mixing. |
| T10 | Virtual curves from observed operations only where transformation preserves entry/exit and sufficient capital/cost/exposure evidence; policies altering stops/exits require future path model | End result trades do not contain intrabar path or counterfactual fills | Mark any expanded simulation as separately modeled/hypothetical, not certified by this iteration. |
| T11 | No early PG partition/cache/incremental compute; index projection + immutable batch jobs, benchmark thresholds; old read path rollback and legacy retirement only after parity | 063+Hasura DEV verified but zero rows on Sep16, no measured current workloads | Require measured workload justification and migration plan before optimizations/retirement. |

## C. Frozen contracts eligible for bounded reopening, NOT already reopened

- `Echo SDK — Canonical Forge Integration and Analytics Contract V1` / Fable FR-1…FR-5: preserve `NormalizedOperationV1`, TradeSet ID from question/input, content digest outside identity, metric `(key,basis,unit,formula)` semantics, no identity rewrite. Bounded proposal only dual-source history evidence descriptor/curve schema or missing fields **after** H0 proves what source contains. S0 new version/capability and backward compatibility fixture needed if wire changes; previous byte corpus unchanged. Source `xKoRx/echo@5dd998f1:v3/sdk/contracts/analytics.go`.
- `E-04/F-04 HandoffManifestV1`: existing operative receipt and certified golden remain correct but do NOT satisfy requirement for two operation lists or analytical readiness. A compatible additive manifest evidence extension (or companion referenced by existing manifest if contract permits) is material defect fix, owner review before wire freeze; no duplicate POST and no second ingestion authority. Source `specs/FEAT-FORGE-INGESTION-E1/SPEC.md`, [[Echo — E-04 Forge Ingestion E1]].
- `E-05 A0`: current scope deliberately excludes curves/ranking and stores NDJSON; new product requires queried operations and temporal curves. Extend E05 ownership/read model and calculator via new capability, not redefine existing MetricSet, erase 063 or claim E05 initial SPEC was wrong for its original narrower scope. Source `specs/FEAT-ANALYTICS-CONVERGENCE-A0/SPEC.md`, `v3/sdk/analytics/calculator/calculator.go`.
- `E-10`: preserve T05 M7 real integrity source, coverage/expectation and policy pin semantics. Reopen only dependency/read integration and `sample_policy_ref` provisional semantics via separate owner policy ratification. Do not promote unratified sample policy into current frozen contract or force E09→E10 source dependency. Source [[Echo — E-10 Strategy Quality and Eligibility]] Sep22.

## D. Material blockers, optional unknowns and ownership

| ID | State | Exact evidence/action | Blocks |
|---|---|---|---|
| B01 | MATERIAL: NOT DEMONSTRATED | Authentic SQX and MT5 individual trade lists, date ranges/cost/risk and source/report reconciliation for SAME certified FULL finalist: H0 owner Forge READ ONLY, candidate exact IDs from F05-I. FULL HTM byte verification alone insufficient. | Certifying dual-history V0 and PRE_REAL only; architecture document done. |
| B02 | MATERIAL when H0 reveals absent row-level detail | If SQX/MT5 exports only aggregate, add narrowly bounded extraction using actual recorded artifacts without manufacturing trades; if unavailable label period INSUFFICIENT. | Specific unavailable history period/curve; not whole Echo code. |
| B03 | OWNER decision T02–T07 pending | Boundary, version projection, duplicate authority, PG projection, curve/metric and readiness contracts; explicit ratification before freezing new SPEC. | Implementing immutable published history and API semantics. |
| B04 | E10 independent owner gate | Manager must review M7 `1485baa4` T05 and ratify sample policy; E10 T06–T10 not authorized. | Eligibility, not V0 history/curves. |
| B05 | PHYSICAL/ECONOMIC not redone | Reference E06/E07 and E08/E09 product gates historical pending; AC18 owner remains gate. | REAL certified, account execution/portfolio apply and PROD capital, not V0 read-only. |
| U01 | SECONDARY | Exact frontend/worker/Forge exporter symbols beyond scoped docs not inspected this session; inspect only touched paths when implementing. | No decision blocker; affects file-level plan, not chosen architecture. |
| U02 | SECONDARY | Actual current PROD status/DB volumes not read per explicit restriction, legacy data migration safety cannot be certified. | No backfill/legacy retirement/rollout until separate authorized gate. |
| U03 | SECONDARY | Graphify unavailable in this surface; used focused Agents-OS Markdown/GitHub plus prior certified notes. | No architecture blocker; index refresh deferred, not repaired. |

## E. Decision gate for Rodrigo

Approval is for **architecture and roadmap only**, not risk policy, trading, deployments or migrations. Ratify or amend T01–T11, particularly T02 boundary/crossing, T03 version scope, T04 provenance/period authority, T05 source-of-truth and index, T06 calculator split and T07 availability state. If approved, H0 verifies first true finalist and fixes exact source format before H1–H4. If no approval yet, docs remain proposed, earlier authority untouched, and H0 READ ONLY may still establish evidence without adopting new semantics. Source SHA snapshot: Echo master `5dd998f16aea7b2821f460188718d7a6d279829c`, Symphony master `745bc8b94e1f6148ddc16c02eb86a755088c2666`, E10 M7 reported feature `1485baa4574b3a65fa97cf0be842ca8ac581097a`; latest branch SHAs should be pinned at execution.
