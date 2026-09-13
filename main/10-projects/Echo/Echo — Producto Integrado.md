---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Echo]]"
parent:
sprint:
start: 2026-09-07
due:
progress: 5
repo:
jira:
prs:
aliases:
  - Echo Producto Integrado
  - Echo + Echo Forge
  - Echo as product
  - Echo integrated product
tags:
  - kind/project
  - area/echo
created: 2026-09-07
updated: 2026-09-12
cssclasses:
  - wide
---

# Echo — Producto Integrado

%% Naming: Echo — Producto Integrado es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — Producto Integrado
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Inicio:** 2026-09-07
> Proyecto padre de producto. Exactamente dos subproyectos de agente: [[Echo Forge — Factory V2 Completion]] y [[Echo — Live Platform V1]]. El contrato compartido es Resource + Echo SDK, no un tercer proyecto.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cada subproyecto de agente se representa aquí con UNA sola tarea humana `#type/supervision`. El detalle de fases vive en el hijo.

## 🎯 Objetivo

Echo es la plataforma integrada de trading algorítmico personal del owner: volver a trabajar **en trading** con un sistema usable, no pasar el resto del año perfeccionando infraestructura.

Echo Forge fabrica y reduce estrategias con evidencia reproducible. Echo recibe estrategias promovidas, observa una Reference, copia/ejecuta bajo políticas, mide comportamiento real, construye portfolios y administra capital de forma durable, explicable y segura.

La función de optimización es **TIME_TO_USABLE_TRADING_SYSTEM**, sujeta a correctness, execution safety, identity integrity, data integrity, recoverability, auditability y reasonable scalability. Valores técnicos: SCALABILITY / ROBUSTNESS / CLEAN / SOLID, simultáneamente KISS / YAGNI / BOUNDED TECHNICAL DEBT.

## 📊 Estado actual

- **Roadmaps operativos congelados 2026-09-07.** Este padre es la visión de producto. La ejecución vive en los dos subproyectos de agente. No hay implementación, SPEC de fase ni mutación de source en esta sesión.
- **Contrato compartido:** [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] con freeze review [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]] en disposición **B — FREEZE AFTER BOUNDED CORRECTIONS**. FR-1…FR-5 entran en E-01/S0. **GOD REQUIRED NOW: NONE.** No queda TOP de arquitectura para este contrato.
- **Forge checkpoint:** B1A `185825c`, B1B `ef65dd1`, B2 `db8a022` son **PASS / CLOSED**. No reabrir ownership global, wall-clock MT5 ni lifetime Temporal. Siguiente Forge: F-01/F-02 en paralelo con Echo S0. Control histórico: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] y [[Echo Forge]].
- **Echo checkpoint:** core productivo reportado `e25165ba`; ingestión canónica ausente; Lab/journal/copia existen con deuda P0 de auth/journal. Discovery histórico: [[Echo - Discovery y Estado]].
- **Usable V1 ≠ cartera financiada.** Software puede completar con CASH/INSUFFICIENT_EVIDENCE. Dinero real es gate owner aparte (O-01).

## 🧱 Entrega de desarrollo

_No aplica — este proyecto es visión/gobernanza de producto; no entrega código. Las tablas repo/branch/SPEC viven en los subproyectos de agente y se fijan al crear cada SPEC de fase._

## Visión, capacidades y fronteras

### Tesis

Forge termina en `FINALIST_PROMOTION V2`, `StrategyVersion` sellada, evidencia/artefactos verificables y `HandoffManifestV1`. Echo empieza en **validated ingestion** (`PromotionRecord` INGESTED). Provisionar, observar, habilitar elegibilidad, asignar capital y activar son transiciones posteriores independientes.

### Capacidades actuales (cualitativas)

- Forge V1 factory durable: Builder/replenishment, classify, retest/optimize/WFM/robust/Apply, export/compile/backtest físico, SQX↔MT5 fidelity analítica, Campaign/Result V1, Slot Pool V2, ownership/long-running/cancel lifetime MT5 **source closed**.
- Echo: runtime de copiado, journal y Lab Clean; catálogo descriptivo; no ingestión canónica, no enrollment versionado, no portfolio de estrategias productivo.

### Capacidades target V1

Ver DoD acotado en [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026#16. Definition of Done 2026: bounded Product Complete V1]] y mínimo usable en [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan#5. Minimum Usable Trading System V1]]. En corto: generar→reducir→validar físicamente→inspeccionar→ingestar→observar→comparar→seleccionar→asignar riesgo acotado→aplicar→pausar/reemplazar→explicar, Forex/MT5-first, un owner.

### Fronteras Forge vs Echo

| Posee Forge | Posee Echo | No es de ninguno ahora |
|---|---|---|
| GeneratedStrategy, StrategyRef/canonical, magic allocation, StrategyVersion seal, Evaluation/evidence Forge, FINALIST_PROMOTION, Handoff | Validated ingestion, RuntimeBinding/Reference, facts/DEAL, Coverage, EconomicCommand, Execution Fidelity, Strategy Quality, eligibility, PortfolioVersion, risk/apply | Eligibility recalculada en Forge; escritura Forge sobre DB Echo; SDK gobernando autoridades de dominio |

Echo SDK gobierna el **lenguaje contractual compartido**. No gobierna autoridades de dominio. Dirección owner: Forge convergerá/migrará hacia Echo en el futuro; eso no autoriza un tercer proyecto Integration.

Preservar: INGESTION ≠ PROVISIONING ≠ OBSERVING ≠ ELIGIBILITY ≠ CAPITAL ≠ ACTIVATION.

### Lenguaje canónico

Única autoridad de wire/tipos/fixtures: Echo SDK nested `v3/sdk/contracts`. S0 pertenece al subproyecto Echo. Forge consume el pin. Fixtures/gates se referencian por ambos. Cambio contractual: PR en Echo SDK → review cruzado → pins secuenciales.

### Invariantes globales (no reabrir)

IDENTITY ≠ EXECUTION ≠ EVALUATION ≠ METRICS ≠ TRADES ≠ ARTIFACTS ≠ SCORE ≠ RANKING ≠ DECISION. Strategy Quality ≠ Execution Fidelity ≠ Forge SQX↔MT5 Fidelity. Finalist ≠ Top N. Ranking ≠ membership. Warning ≠ invalid strategy. Reference = operación observada en broker Reference, no señal ideal pre-broker. DEAL = hecho económico irreducible. StrategyVersion ≠ Strategy ≠ RuntimeBinding.

## Ciclo de producto

Reference path integrado. **Forge sigue siendo un pipeline secuencial, pero su topología es dinámica y no está congelada**: cada run compone stages desacoplados por contratos; puede omitir/repetir stages y usar outputs previos como input de nuevas generaciones. Cada generación produce estrategias/artefactos nuevos con identidad y lineage propios; nunca muta la estrategia/template origen. Lo frozen son contratos, invariantes, semántica de artefactos y boundary Forge→Echo. `FINALIST` sólo se emite cuando satisface su contrato canónico, independientemente del camino recorrido.

GENERATION → CLASSIFICATION / EARLY REDUCTION → RETESTER → OPTIMIZER → WFM → ROBUST SELECTION → FINAL RETEST → MT5 CONVERSION → PHYSICAL MT5 VALIDATION → FORGE FIDELITY → FINALIST → HANDOFF → ECHO INGESTION → REFERENCE ENROLLMENT → REFERENCE OBSERVATION → EXECUTION → STRATEGY QUALITY + EXECUTION FIDELITY → ELIGIBILITY → PORTFOLIO → RISK → CAPITAL ALLOCATION → APPLY → MONITORING → REBALANCE / REPLACEMENT / RETIREMENT.

### Estado de éxito usable

Escalera [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan#8. Product Usability Ladder]]: V1 apunta a nivel 4 DEMO automático con CASH válido y nivel 5 REAL sólo con aprobación owner. Nivel 6 autonomía amplia está **fuera** del compromiso V1.

### Fuera de scope ahora

Netting implementation; MT4 nuevo al estándar 64-bit; Futures; multi-tenant; generic provisioning framework; batch ingestion; ML; advanced optimizer; generic event sourcing; complete UI rewrite; historical perfect backfill; editor de estrategias en front; reejecución GUI completa; auto-takeover MT5 no-TTL.

Front V1: **READ / OBSERVE**. Viewer SQX en VM dedicada es SHOULD, no edición. Reexecution from UI es later.

## 🧩 Subproyectos

Exactamente dos, ambos `owner: agent` bajo `10-projects/Echo/agentes/`:

1. [[Echo Forge — Factory V2 Completion]] — 5 Agent Tasks (F-01…F-05).
2. [[Echo — Live Platform V1]] — 13 Agent Tasks (E-01…E-13). S0 vive aquí.

[[Echo Forge]] permanece como programa histórico operativo; su roadmap restante de factory se ejecuta en el subproyecto Factory V2, no como tercer hijo de producto. [[Echo - Discovery y Estado]] permanece como proyecto de comprensión, no de delivery.

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## Mapa de dependencias cruzadas

```mermaid
flowchart LR
  subgraph forge [Forge Factory V2]
    F01[F-01 Canonical generation]
    F02[F-02 Finalist V2]
    F03[F-03 SQX long-running]
    F04[F-04 Magic seal handoff]
    F05[F-05 Release FULL golden]
  end
  subgraph echo [Echo Live V1]
    E01[E-01 S0 SDK]
    E02[E-02 Control safety]
    E03[E-03 Identity BWC]
    E04[E-04 Ingestion]
    E05[E-05 Analytics A0]
    E06[E-06 Reference enrollment]
    E07[E-07 Raw facts coverage]
    E08[E-08 Routing commands]
    E09[E-09 Execution fidelity]
    E10[E-10 Quality eligibility]
    E11[E-11 Portfolio shadow]
    E12[E-12 Apply lifecycle]
    E13[E-13 Front ops V1 cert]
  end
  F01 --> F04
  F02 --> F04
  F03 --> F05
  F01 --> F05
  F02 --> F05
  F04 --> F05
  E01 --> E03
  E01 --> E05
  E01 --> F04
  E02 --> E06
  E03 --> E04
  E04 --> E06
  E04 --> F05
  E06 --> E07
  E07 --> E08
  E08 --> E09
  E09 --> E10
  E10 --> E11
  E11 --> E12
  E12 --> E13
  E05 --> E10
```

| Fase Forge | Dependencia Echo | Puede correr en paralelo con | Join gate |
|---|---|---|---|
| F-01 Canonical generation | ninguna | E-01, E-02, F-02, F-03 | ninguna |
| F-02 Finalist V2 | ninguna | E-01, E-02, F-01, F-03 | ninguna |
| F-03 SQX long-running | ninguna | F-01, F-02, E-01 | entra a F-05 |
| F-04 Magic/seal/handoff | **pin S0 (E-01)**; catálogo CC owner antes allocation real | E-03, E-04, E-05 | Integration: mismo corpus/pin; manifest fixture aceptado por E-04 |
| F-05 Release + FULL golden | pin S0; smoke real de ingestión espera E-04 certificado | cadena live Echo posterior a E-04 | Physical integration / PRODUCT CAPABILITY cuando ambos tracks certifican handoff→receipt |

| Fase Echo | Dependencia Forge | Puede correr en paralelo con | Join gate |
|---|---|---|---|
| E-01 S0 SDK | ninguna | F-01, F-02, F-03, E-02 | pin publicado; Forge F-04 lo consume |
| E-02 Control safety | ninguna | E-01 y todo Forge interno | antes de confiar captura live |
| E-03 Identity/BWC | E-01 | F-04, E-05 | implementation closed habilita **development** E-04; CONTRACT_PASS habilita **integration** E-04 |
| E-04 Ingestion | E-01 + E-03 implementation (dev); E-03 CONTRACT_PASS (integrate); producer fake basta | F-04 tras pin | INTEGRATION PASS handoff↔receipt gated; development paralelo permitido |
| E-05 Analytics A0 | E-01 | E-03/E-04 | planning v1.0.1 @ `dd1f2da9`; alimenta E-10; no espera E-02 PHYSICAL para development/implementation/verification; merge/deploy 063 espera 062 E-02 en master |
| E-06…E-13 live | E-04; supply físico Forge ayuda pero fixtures permiten diseño | según DAG interno | PHYSICAL PASS no se certifica con mocks |

**Arranque inmediato recomendado (no lanzar implementación aquí):** Forge **F-01 + F-02** en paralelo con Echo **E-01**. E-02 y F-03 también pueden partir sin esperar S0.

## Gobernanza

Metodología: **TOP planea → crea SPEC(s) → NORMAL implementa.** NORMAL no rediseña contratos/decisiones frozen; si aparece contradicción material, STOP / escalate.

Clases de modelo: NORMAL (Luna / GLM 5.3 Flash) implementa SPECs congeladas. TOP (Grok 4.5 / GLM 5.3) planifica fases, SPECs y RCA acotada. GOD (Fable 5.1 / Astra) sólo decisiones estructurales caras de revertir. RESERVE: DeepSeek V4. Escalation por riesgo de decisión, no por tamaño de codebase ni incertidumbre del agente previo.

Una Agent Task **no es** la SPEC de implementación. Cuando una fase se activa, TOP lee este padre + el subproyecto + la Agent Task + contratos frozen, revalida baseline, y escribe SPECs con baseline, scope, allowed files, autoridades, identity/data, error/retry/terminal, tests, release/deploy permissions, gates, certificación y stop conditions. Sin contratos de coding ambiguos.

Certificación no es “code merged”. Distinguir SOURCE PASS / CONTRACT PASS / INTEGRATION PASS / PHYSICAL PASS / PRODUCT CAPABILITY PASS. No certificar capacidad física con mocks.

Release: burn-down amplio → matriz determinística → un release cohesivo → certificación física. No churn de release-por-fix. No empaquetar sistemas de alto riesgo no relacionados.

Roadmaps **secuencian trabajo**; no redefinen verdad de dominio. No promover sequencing a Decisions.

## Deuda aceptada

Deuda acotada es herramienta. No convertirla en blocker sin impacto material. Cleanup sólo cuando desbloquea capacidad o corrige correctness.

Puede vivir: legacy Lab projections; legacy journal rows; legacy MT4 cohort; legacy Forge HashIdentity (newline, nombre distinto de `H()`); old MetricSets/Scope JSON; host-suffixed adopted IDs hasta proof F-01; external SDK adapters; algunos read models mutables; attach Reference manual verificado donde V1 lo permite.

## Cerrado — no reabrir en backlog

B1A global fleet ownership / durable MT5 reuse. B1B long-running MT5 (elapsed wall-clock ≠ failure; campaign count ≠ physical concurrency). B2 Temporal activity lifetime ≠ physical MT5 lifetime; cancel explícito mata Job Object propio. Arquitectura global de ownership / fencing V3. Slot Pool V2 local. Finalist Factory V1 contractual (no V2). Modelo semántico StrategyVersion (no implementación). Arquitectura del contrato SDK (FR-1…FR-5 se **implementan** en S0, no se rediseñan). Identity graph Forge. Three purposes SQ/EF/Forge fidelity. Membership ≠ rank. Ingestion ≠ activation/capital.

## Riesgos / unresolved reales

| Ítem | Clase |
|---|---|
| Catálogo magic `CC` / `YYMMCCQQQQ` antes de allocation física | PRODUCT DECISION |
| O-01 aceptación 2026 plataforma vs cartera financiada | PRODUCT DECISION |
| O-02 mandato V1 cuentas/moneda/capital | PRODUCT DECISION |
| Evidence Gate por cohorte (O-03) | PRODUCT DECISION |
| Discriminador durable intra-wave antes de retirar HOST_KEY | TOP BEFORE PHASE F-01 |
| Pin S0 publicado antes de F-04/E-03 | DEPENDENCY |
| Certificación física singleton Windows / drain Kronos | PHYSICAL CERTIFICATION |
| Attach/enrollment físico y clocks broker | PHYSICAL CERTIFICATION |
| Recuperación histórica Reference (ahorro calendario, no blocker de captura nueva) | DEFERRED / timebox |
| Netting, Futures, ML, editor UI, batch ingestion | DEFERRED |

## Balance de fases

Forge: 5 Agent Tasks, mayoría MEDIUM; F-02 y F-04 LARGE-acotados con sub-SPECs internos (C1/C2 y allocation→seal→adapter), no mega-fases distintas. Echo: el antiguo bloque live/E2 se descompuso en E-06…E-13; E-02 extraído de “live” porque H1/P0 es capacidad propia; E-11/E-12 separan shadow vs effects. Ninguna micro-fase. GOD no asignado a ninguna fase.

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> Este proyecto humano muestra sólo puentes de supervisión. Las fases `#owner/agent` viven en los subproyectos.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [ ] [[Echo Forge — Factory V2 Completion]] arrancar + seguimiento #owner/me #type/supervision #area/echo
> - [ ] [[Echo — Live Platform V1]] arrancar + seguimiento #owner/me #type/supervision #area/echo
> - [r] [[Echo — Knowledge Base Consolidation]] campaña documental: cartografía Echo/Forge, wiki canónica, AGENTS.md routers, higiene context budget #owner/me #type/supervision #area/echo
> - [ ] Ratificar catálogo magic CC antes de allocation física F-04 #owner/me #type/admin #area/echo
> - [ ] Confirmar O-01/O-02/O-03 de mandato 2026 cuando el track live lo necesite #owner/me #type/admin #area/echo

## 📆 Bitácora

- **2026-09-13** — Campaña [[Echo — Knowledge Base Consolidation]] COMPLETE (fases A–K): subdominio `30-resources/applications/echo/` publicado y verificado adversarialmente (frontera Forge→Echo rota en producción documentada con gaps G1–G7); AGENTS.md de repos como patches propuestos; 2 hallazgos de seguridad escalados al owner (credenciales `30-resources/APIs.md` y contraseña SSH en symphony tracked). Puente → Review.
- **2026-09-11** — E-04 TOP: hijo [[Echo — E-04 Forge Ingestion E1]]. Development E-04 puede partir en paralelo con verification E-03; integration/merge gated por E-03 CONTRACT_PASS. `origin/master` no se mueve. Join Forge no closed.
- **2026-09-07** — Roadmaps operativos congelados. Dos subproyectos de agente. Sin implementación en esta nota.