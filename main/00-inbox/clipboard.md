# MANDATO MAESTRO — M2 / TOP

## Polymarket Engine MVP · Implementation Plan sobre diseño frozen

### ROL

Actúa como **Technical Lead / Implementation Planner** especializado en Go, sistemas event-driven, persistencia, testing y delivery incremental.

M1 está cerrado y congelado.

Tu misión es transformar la arquitectura frozen del **Polymarket Engine MVP** en un **plan de implementación completo, ordenado, verificable y ejecutable por agentes NORMAL**.

No rediseñes.

No hagas Deep Research.

No implementes código.

No crees documentos nuevos.

No abras decisiones arquitectónicas cerradas.

Tu resultado debe permitir entregar slices cerrados a agentes NORMAL sin que tengan que interpretar arquitectura ni inventar contratos.

---

# 0. ENTORNO Y AUTORIDAD

Trabajas sobre Agents-OS local.

La sincronización externa ocurre automáticamente fuera de tu responsabilidad.

No necesitas GitHub, commits remotos, PRs ni APIs de GitHub.

Resuelve el root local mediante el bootstrap canónico mínimo de Agents-OS.

## Único archivo de escritura

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

## Fuentes autorizadas

### Autoridad principal

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

Debes leer completamente:

- decisiones frozen D-*;
    
- M0/M1 status;
    
- M1 ASTRA architecture;
    
- FABLE challenge;
    
- ASTRA-2 reconciliation;
    
- ASTRA-3 freeze;
    
- A-* frozen;
    
- U-*;
    
- gates G-*;
    
- `FOUNDATIONAL NOW`;
    
- `IMPLEMENT LATER WITHOUT REDESIGN`.
    

### Technical contracts

Índice:

`main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`

Consulta selectivamente sólo las partes necesarias para definir schemas, fixtures, adapters y tests de cada slice.

No repitas M0.

### Edge requirements

`main/30-resources/polymarket/Polymarket — Edge Research Consolidado 2026-09-16.md`

Úsalo únicamente cuando sea necesario confirmar que un contrato del engine sirve a los consumidores iniciales Sports/NegRisk.

No diseñes esas estrategias.

## Scope prohibido

No explores otros proyectos.

No abras Echo, Echo Forge, Hermes ni memorias externas.

No navegues Internet.

No investigues nuevamente Polymarket.

---

# 1. BASELINE FROZEN

Estado:

`M1_DESIGN_FROZEN`

Owner decisions:

```text
OD-1 APPROVED
OD-2 APPROVED
OD-3 APPROVED
```

No quedan blockers para M2.

Physical gates:

`NOT_RUN`

Live:

`NOT_CERTIFIED / LIVE_DISABLED`

El plan debe preservar esto.

---

# 2. OBJETIVO DE M2

Producir un plan que permita a agentes NORMAL implementar **FOUNDATIONAL NOW** mediante slices pequeños, acumulativos y certificables.

Cada slice debe:

1. partir de un baseline explícito;
    
2. tener scope cerrado;
    
3. definir archivos/packages permitidos;
    
4. establecer contratos exactos;
    
5. contener tests requeridos;
    
6. tener failure/recovery behaviour;
    
7. terminar en un estado funcional verificable;
    
8. no depender de decisiones futuras no necesarias;
    
9. no habilitar accidentalmente live.
    

La prioridad es entregar un engine usable para:

```text
READ-ONLY
SCREEN
REPLAY
SHADOW
```

antes de capacidades live.

---

# 3. FOUNDATIONAL NOW — DEBE PLANIFICARSE

El plan debe cubrir al menos:

## Foundation

- módulo Go;
    
- dependency direction;
    
- config versionada;
    
- IDs nominales;
    
- decimal exacto / cantidades tipadas;
    
- clocks/timestamps;
    
- error taxonomy;
    
- capability registry fail-closed.
    

## Protocol / schemas

- wire DTOs separados de dominio;
    
- Gamma;
    
- CLOB REST read-only;
    
- Market WS;
    
- Data v2 necesario;
    
- protocol/version identity;
    
- schemas y parsers;
    
- fixtures versionados.
    

## Catalog / Universe

- Event;
    
- Market;
    
- Outcome;
    
- Asset;
    
- Condition;
    
- relationships;
    
- known-at revisions;
    
- pagination;
    
- refresh;
    
- universe selection;
    
- quarantine.
    

## Regimes / Resolution

- tick size;
    
- min size;
    
- fees;
    
- market lifecycle;
    
- resolution observations;
    
- provenance/revisions.
    

## Market data

- transport;
    
- subscriptions;
    
- epochs;
    
- full snapshots;
    
- book shards;
    
- quality states;
    
- staleness;
    
- reconnect;
    
- fencing;
    
- Frame Builder;
    
- multiasset cut;
    
- backpressure.
    

## Capture

- journal;
    
- `capture_seq`;
    
- `durable_seq`;
    
- envelopes;
    
- segments;
    
- checksums;
    
- EVIDENCE/RUNTIME lanes;
    
- crash recovery;
    
- discontinuities;
    
- redaction.
    

## Persistence

- SQLite;
    
- migrations;
    
- owners/repositories;
    
- `applied_seq` by reducer;
    
- ACCOUNT_FACT vs RESEARCH_EVIDENCE;
    
- private account evidence;
    
- backup/restore local;
    
- integrity checks.
    

## Replay

- observation replay;
    
- delivery replay;
    
- virtual clock;
    
- manifests;
    
- deterministic normalization/reducers;
    
- reproducibility states;
    
- `NOT_REPRODUCIBLE`.
    

## Strategy runtime

- Strategy interface frozen;
    
- lifecycle;
    
- Frame;
    
- EvaluationContext;
    
- isolated instance execution;
    
- SCREEN;
    
- REPLAY;
    
- SHADOW;
    
- failure isolation;
    
- slow callback policy.
    

## Experiments

- hypothesis registry;
    
- experiment manifests;
    
- scorecards;
    
- dataset lineage;
    
- GO / ITERATE / NO_GO / INCONCLUSIVE;
    
- diagnostics.
    

## Simulator / Economics

- executable depth;
    
- VWAP;
    
- optimistic/base/stress;
    
- fill simulation;
    
- fees;
    
- partials;
    
- virtual liquidity isolated by experiment;
    
- optional explicit portfolio-shared mode;
    
- multi-leg simulation;
    
- BasketPolicy.
    

## Account Coordinator — non-live foundation

Aunque live esté deshabilitado, implementar los contratos internos que necesitan simulator y futura ejecución:

- ledger;
    
- reservations;
    
- AccountView revisions;
    
- attribution;
    
- BasketExecution state;
    
- conservation invariants;
    
- UNKNOWN model;
    
- intent lifecycle contracts where needed for tests;
    
- no actual venue writes.
    

## Observability

- metrics;
    
- structured logs;
    
- readiness by capability;
    
- five diagnostics:
    
    - NO EDGE;
        
    - BAD DATA;
        
    - BAD FILL MODEL;
        
    - SYSTEM FAILURE;
        
    - EXECUTION FAILURE;
        
- pipeline timings;
    
- resource pressure.
    

## Local recovery

- clean shutdown;
    
- crash recovery;
    
- local backup;
    
- local restore;
    
- integrity verification.
    

---

# 4. EXPLICITLY NOT IMPLEMENTED IN THIS M2

Do not plan coding of:

- real live order submission;
    
- operational ActivationLease for real trading;
    
- production wallet/signing;
    
- User WS execution reconciliation unless strictly needed as fixture/interface;
    
- on-chain writes;
    
- CTF live position operations;
    
- NegRisk conversion;
    
- Protocol-v2 unverified codecs;
    
- `deferExec=true`;
    
- Builder modes;
    
- Session Keys;
    
- auto-wallet;
    
- auto-approvals;
    
- Combo/RFQ;
    
- Bridge/funding automation;
    
- real Sports strategy;
    
- real NegRisk strategy;
    
- disaster recovery off-host;
    
- remote backup infrastructure;
    
- dashboards/UI;
    
- Kubernetes;
    
- Kafka/Flink;
    
- microservices.
    

Interfaces/contracts frozen for future live may be represented, but implementations remain absent or explicit stubs returning:

`DISABLED`

Do not create fake implementations.

---

# 5. PACKAGE / MODULE PLAN

Define a proposed Go package structure.

For every package state:

```text
package path
responsibility
owns
may depend on
must not depend on
public contracts
persistence ownership
concurrency ownership
```

Avoid a generic:

`utils`

Avoid a giant:

`common`

Avoid circular imports.

Adapters depend inward.

Domain must not depend on transports/storage.

Composition root performs wiring.

Do not over-fragment into dozens of micro-packages without reason.

The package structure is now an implementation decision derived from frozen boundaries, not an opportunity to redesign them.

---

# 6. IMPLEMENTATION SLICES

Design the implementation as an ordered sequence of independently verifiable slices.

Target approximately **8–15 major slices**, subdivided only where useful.

Each slice must use this template:

```text
M2-SXX — Name

Goal:
Why this slice exists.

Depends on:
Previous slices.

Allowed scope:
Packages/files/directories the NORMAL agent may modify.

Forbidden:
Explicit things it must not touch.

Contracts:
Exact frozen contracts implemented.

Persistence:
Schemas/migrations/state ownership.

Concurrency:
Goroutines/channels/locks/ownership if applicable.

Failure behaviour:
What happens on error/crash/partial progress.

Tests:
Unit/property/contract/integration/fault tests.

Gates:
Exact G-* or derived gates exercised.

Physical verification:
Commands or observable checks.

Definition of Done:
Binary PASS/FAIL criteria.

Handoff:
What next slice can safely assume.
```

No slice may say:

`implement as appropriate`

or:

`handle errors`

Specify behaviour.

---

# 7. DEPENDENCY ORDER

Choose the order to minimize rework.

Expected dependency shape should roughly follow:

```text
Foundation
    ↓
Protocol DTOs + fixtures
    ↓
Catalog / Regimes
    ↓
Capture + persistence
    ↓
Market data / books
    ↓
Frames
    ↓
Replay
    ↓
Strategy runtime
    ↓
Economics / Simulator
    ↓
Account Coordinator / Basket contracts
    ↓
Experiments / Shadow
    ↓
Observability / recovery / certification
```

You may alter that order where dependencies require it, but explain why.

Avoid building horizontal layers that produce no runnable capability for many slices.

Prefer vertical checkpoints where possible.

---

# 8. TEST STRATEGY

Map every physical gate relevant to FOUNDATIONAL NOW to implementation slices.

At minimum include:

```text
G-01…G-15
G-02b
G-05b
G-06b
G-07b
G-09b
G-10b
G-10c
G-11b
G-12b
G-13b
G-15b
```

G-16…G-19 remain future live gates.

For each implemented gate define:

- fixture/input;
    
- action;
    
- expected output;
    
- expected failure;
    
- evidence produced.
    

Property tests must include seeds/counterexamples persisted when failures occur.

Fault injection must include:

- partial journal write;
    
- crash before/after fsync;
    
- invalid segment;
    
- reducer behind journal;
    
- WS overflow;
    
- stale epochs;
    
- slow strategy;
    
- callback panic;
    
- missing revision;
    
- SQLite failure;
    
- disk pressure;
    
- restore;
    
- incomplete experiment.
    

Do not use coverage percentage as substitute for invariants.

Agents-OS 95% coverage remains complementary.

---

# 9. DELIVERY POLICY FOR NORMAL AGENTS

Plan each NORMAL assignment so the coding agent receives:

- one slice;
    
- exact project path;
    
- baseline assumptions;
    
- allowed files/packages;
    
- forbidden scope;
    
- relevant M1 sections;
    
- relevant TPM sections;
    
- tests to implement;
    
- gates to execute;
    
- expected commits/checkpoints if Agents-OS workflow requires them;
    
- DoD.
    

NORMAL must not read the whole vault.

NORMAL must not reinterpret architecture.

NORMAL must not decide another database, runtime model, error policy or package direction.

If implementation proves architecture impossible:

`BLOCKED — DESIGN ISSUE`

Do not let NORMAL improvise around it.

---

# 10. PARALLELISM

Identify which slices can safely run in parallel.

For every parallel group define ownership boundaries so two agents do not modify the same files or schemas.

Prefer sequential execution when contracts are still being materialized.

Do not parallelize migrations or shared-domain primitives without a strong reason.

Output:

```text
PARALLEL GROUP A
- ...
- ...

SEQUENTIAL BARRIER
- ...

PARALLEL GROUP B
- ...
```

The goal is to speed implementation without creating merge/reconciliation debt.

---

# 11. REPO BOOTSTRAP

The implementation repository may not yet exist.

If repo/name/path is still undecided, M2 must make the minimum operational proposal and mark it:

`REQUIRES_OWNER — REPO LOCATION ONLY`

This is not an architectural blocker.

Do not invent a large monorepo structure.

Recommended baseline if nothing else exists:

```text
Go module
cmd/
internal/
migrations/
testdata/
```

Adapt only if the project already defines the implementation location.

Do not create the repository during M2 unless explicitly instructed by the owner.

---

# 12. MILESTONES

Group slices into meaningful implementation milestones.

Suggested semantic milestones:

```text
M3-A — Protocol & Durable Data Foundation
M3-B — Market Data + Recorder + Replay
M3-C — Strategy Runtime + Simulator
M3-D — Shadow Research Engine
M3-E — Engine Certification
```

Do not force these names if a better grouping emerges.

For each milestone define what becomes usable.

Example:

`After M3-B we can capture a real market and deterministically replay our own observation.`

That kind of concrete capability is required.

---

# 13. COMPLETION / M4 BOUNDARY

Define exactly when implementation can advance from M3 to M4 certification.

The implementation plan must produce:

- buildable executable;
    
- migrations;
    
- fixtures;
    
- deterministic tests;
    
- capture;
    
- replay;
    
- strategy fixture;
    
- shadow;
    
- simulator;
    
- account/risk invariants;
    
- observability;
    
- local restore.
    

No live capital required.

M4 evaluates the resulting engine.

M2 does not mark M4 PASS.

---

# 14. OUTPUT LOCATION

Edit exclusively:

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

Add:

`## M2 — TOP Implementation Plan`

Do not rewrite M1.

Do not create another plan document.

Do not create SPEC files yet.

Do not implement code.

Update project state to:

`M2_PLAN_READY_FOR_MANAGER_REVIEW`

Do not mark M2 frozen until owner/manager review.

---

# 15. QUALITY CHECK BEFORE FINISHING

Before completing, verify:

1. Every FOUNDATIONAL NOW capability appears in at least one slice.
    
2. Every package has a clear owner.
    
3. Every persistence schema has one writer.
    
4. Every concurrency boundary is explicit.
    
5. Every critical failure path has a test.
    
6. Every M4 non-live gate maps to implementation work.
    
7. No slice requires a live-disabled capability.
    
8. No NORMAL agent must invent architecture.
    
9. No two parallel slices own the same mutable contract.
    
10. Implementation order can produce useful intermediate capabilities.
    
11. Local restore is testable.
    
12. Sports and NegRisk can later consume the result without modifying engine fundamentals.
    

If any answer is no, fix the plan before finishing.

---

# 16. RESPUESTA FINAL

No pegues el plan completo en chat.

Responde solamente:

STATUS: `M2_PLAN_READY_FOR_MANAGER_REVIEW | PARTIAL | BLOCKED`

PLAN:

- major slices:
    
- milestones:
    
- parallel groups:
    
- estimated critical path in slices:
    

COVERAGE:

- FOUNDATIONAL NOW:
    
- deferred:
    
- gates mapped:
    

OWNER:

- repo/path decision if required:
    
- other decisions required:
    

RISKS:

- implementation risks that TOP identified:
    
- any `BLOCKED — DESIGN ISSUE`:
    

NEXT:

- manager review → M2 freeze → NORMAL implementation