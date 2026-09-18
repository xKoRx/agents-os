---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Personal]]"
parent:
sprint:
start: 2026-09-15
due:
progress: 25
repo:
jira:
prs:
aliases:
  - Polymarket Engine MVP
  - Polymarket Arbitrage MVP
  - Prediction Market Engine
tags:
  - kind/project
  - area/personal
  - domain/trading
  - tech/polymarket
  - topic/prediction-markets
created: 2026-09-15
updated: 2026-09-17
---

# Polymarket Engine — MVP

> [!info]+ Polymarket Engine — MVP
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Engine:** MVP durable · **Strategies:** POCs · **Tiny-live inicial:** US$300 totales

## 🎯 Objetivo

Construir un **engine Polymarket-native, agnóstico de estrategia**, robusto y reusable, que permita investigar, medir, simular y eventualmente ejecutar múltiples estrategias sin rehacer market-data, replay, risk, execution ni observabilidad para cada hipótesis.

La distinción es estructural:

- **Polymarket Engine = MVP durable.** No es una POC ni código descartable.
- **Strategies = POCs.** Cada estrategia puede ser promovida, iterada o eliminada sin erosionar el engine.
- El engine es **agnóstico de estrategia, no agnóstico de venue**. Debe modelar bien Polymarket y evitar abstracciones prematuras para Kalshi/sportsbooks/otros venues.
- Echo y Echo Forge continúan en paralelo y quedan fuera del hot path y del alcance del MVP.

North star del producto de research:

`TIME_TO_VALIDATED_HYPOTHESIS`

Una vez establecido el engine, el coste marginal de probar una hipótesis nueva debe caer materialmente.

## 📊 Estado actual

- Greenfield; repo de implementación pendiente.
- Arquitectura frozen a nivel macro: **Go + modular monolith + single deployable + single large host**.
- Primero se construye el Engine MVP; Sports y NegRisk dejan de ser “el MVP” y pasan a ser **POC-S01** y **POC-S02**, primeros consumidores del engine.
- Backlog research: 30 familias canónicas `PE-001…PE-030` en [[Polymarket — Edge Research Consolidado 2026-09-16]].
- Contexto económico/estratégico: [[Polymarket Engine — Opportunity Context]].
- **M0 DESIGN_READY (documental, 2026-09-17):** Technical Platform Map canónico indexado en `30-resources/polymarket/`, con 11 partes, 7/7 OpenAPI (163 operaciones) y siete RG resueltos para diseño con exclusiones; no habilita live ni NegRisk conversion.
- **M1_DESIGN_FROZEN (2026-09-17):** ASTRA-1 proposal → FABLE challenge → ASTRA-2 reconciliation → OD-1/OD-2/OD-3 `APPROVED` → auditoría final ASTRA-3 `PASSED` documental. M1 cerrado, sin blockers arquitectónicos materiales restantes. Contratos congelados en M1.1–M1.17; registro de cierre e historial al final de esta nota.
- **M2_TOP_PLAN_READY (2026-09-17):** TOP produjo `## M2 — TOP Implementation Plan` (13 slices sobre FOUNDATIONAL NOW de M1.15, hitos M3-A…M3-E, mapa de gates G-01…G-15+extensiones b con fault injection, grupos de paralelismo y política de entrega NORMAL); estado `M2_PLAN_READY_FOR_MANAGER_REVIEW`. Pendiente revisión manager/owner → M2 freeze → M3/NORMAL. Gates físicos `NOT_RUN`; live `NOT_CERTIFIED / LIVE_DISABLED`; ninguna capability live/optional habilitada.
- **M2_FROZEN — M3-A S01 DONE (2026-09-17):** el owner congeló el plan y mandató M3/NORMAL; NORMAL implementó **M2-S01 Foundation** en `~/go/src/github.com/xKoRx/polymarket-engine` (module `github.com/xKoRx/polymarket-engine`, Go `1.27.0`/toolchain `1.27.1`). Foundation contracts v1 (IDs nominales, `ProtocolIdentity`, decimal exacto encapsulado, unidades, `RevisionRef`, `Clock`/tiempos, error taxonomy, capability registry fail-closed, `ExecutionMode`/`ActivationLease` contrato), config TOML estricta versionada con `config_revision`, archtest con gate de imports y `cmd/engine version`. Calidad: build/vet/test verde, `-race` verde, coverage 95.1% total. Gates: **G-01 PASS en su porción foundation completa** (`S01_G01_FOUNDATION = PASS`: 62 vectores base + 60 vectores del boundary numérico P03 §5 tras la corrección M2-S01-C1; `G01_REGIME_INTEGRATION` queda `NOT_RUN` para S05 como única integración tick/regime pendiente, sin primitivas numéricas) y **G-15b base mecánica PASS** (probe unsafe/net/goroutine en rojo, fixture neutral en verde); G-02/G-03+ `NOT_RUN`; live `LIVE_DISABLED` deny-all verificado por tests; leaseline `DISABLED`. Sin blockers. Siguiente: barrera M2 → S02 (protocolo) ∥ S03 (capture+persist).
- El código del engine se implementa slice a slice según M2 frozen; nada fuera del slice asignado.
- **M2-BARRIER-A → `M2_S02_S03_INTEGRATION_PASS` — M3-A CERRADO (2026-09-17):** barrera de integración S02×S03 certificada por mandato owner sobre árbol estable (snapshot SHA-256 del baseline verificado antes y después; sin escritores concurrentes). Seam verificado en imports y símbolos: capture consume exclusivamente `Identify/Redact/PolicyV1/ParseSurface` de S02, sin DTOs; redacción aplicada en admisión antes de cualquier byte persistido, con escaneo de todos los bytes del journal por marcadores sintéticos y cero secretos reales en repo/evidencias/logs; envelope conserva policy/versiones/hash del payload sanitizado y el round-trip mantiene la sanitización. Durabilidad: `durable_seq` avanza sólo tras fsync (faults before/after cubiertos), `Records` clampea al frontier, saturación EVIDENCE declara `evidence_gap` durable con `after_seq/resumed_at/refusal_events` exactos vía reserva de control sin presupuesto, saturación RUNTIME pausa sin tocar reserva EVIDENCE ni revocar epochs, y recovery sella el boot muerto, abre boot nuevo y persiste `boot_start` + anomalías de control por cada discontinuidad antes de retornar — la pérdida no persistida queda declarada, jamás cuantificada. SQLite×recovery reejecutado verde (cursors, regresión→CONTRACT_DRIFT, `applied_seq > durable_seq` imposible, rollback, replay de prefijo, manifest corrupto fail-closed, huérfanos adoptados, sufijo preservado, checksums de migraciones). Regresión global: build/vet/test/race verdes, tidy sin diff, diff-check limpio; CLI `journal verify` verificado físicamente (limpio exit 0; byte corrupto exit 1 FAIL explicado). Coverage: módulo 95.4% (capture 95.7/persist 95.5/protocol 95.3/cmd 91.6 por seam os.Exit; combinado S03 95.3%); defecto de coverage de persist (92.8% por paquete) corregido dentro del ownership S03 con 13 tests útiles; 12 statements defensivos inalcanzables por API quedan como excepción técnica registrada pendiente de aprobación manager (no bloquea). Gates: G-03 PASS, G-01 porción wire PASS, G-06 y G-02b PARTIAL (cierres S06/S11), G-14 insumos (S12), G-15b porciones. Checkpoints `af77074` (S02) y `2ac8985` (barrera) en `main` sin push. **M2-S04 habilitado, no iniciado.**
- **`M2_S04_PARTIAL` — M2-S04 implementado y certificado en su alcance (2026-09-18):** primer checkpoint vertical operativo (`catalog sync → captura durable → revisiones persistidas → catalog inspect`) con G-04 PASS 16/16 sobre fixtures deterministas; 1 blocker upstream documentado con contraejemplo (parser de fechas Gamma de S02) que deja la proyección real en cuarentena honesta hasta su corrección. Detalle completo en la bitácora de abajo y en el agent run registrado.
- **`M2_S04_PASS` — M2-S04-C1 cierre correctivo (2026-09-18):** FASE A corrigió el parser de fechas Gamma de S02 (`internal/protocol`, checkpoint `81aadb5`) con gramática cerrada Gamma-scoped (separador espacio, offsets ±HH, fracciones 1–9 dígitos exactas; zona explícita obligatoria; G-03 PASS 47 fixtures). FASE B re-ejecutó el sync real read-only en 3 pasadas — sin cuarentenas por el defecto temporal, idempotencia demostrada sobre datos vivos (pass 3 de markets: 0 revisiones nuevas; las revisiones nuevas restantes atribuidas a cambio real vía `updatedAt`/precios con diff completo), known-at sin regresión (0 en 83,956 entidades), G-04 PASS 20/20 con 4 escenarios correctivos nuevos, coverage catalog 95.0–95.1/gamma 97.5/cmd 89.6 (excepción heredada)/módulo 95.1, regresión global build/vet/test/race/tidy/diff-check verde. Techo upstream no documentado: Gamma rechaza `offset > 2000` (HTTP 422) — caminata del universo activo queda partial honesta; gap documentado. Cinco defectos demostrados por el wire vivo fueron corregidos y probados durante el cierre (oscilación de dedup en revisiones y relaciones, corte de `source_at` por bytes, reporte de drain fallido oculto, record cap de capture para `/events`, y `segPaths` de capture tras sellado — única desviación del scope nominal, root-cause de 1 línea, disclosed para revisión manager). Checkpoints `81aadb5` + `527dc73` en `main` sin push. G-06 sigue PARTIAL hasta S06; `LIVE_DISABLED` sin cambios. Detalle en bitácora y agent run.

## 🧭 Autoridad documental y economía de tokens

### Regla principal

**Este archivo es la autoridad operativa única del proyecto.**

Astra, Fable, TOP y NORMAL deben trabajar contra este archivo y actualizar aquí sus decisiones/handoffs relevantes. No crear ADRs, design docs, plans ni SPECs fragmentados salvo que exista una razón material que el owner apruebe.

Separación permitida:

- `Polymarket Engine — MVP.md` → producto, arquitectura vigente, decisiones, gates, plan de implementación y handoffs.
- `Polymarket Engine — Opportunity Context.md` → contexto de oportunidad, bankroll, criterios económicos y familias de estrategias.
- `30-resources/polymarket/` → conocimiento externo compilado: API/protocolo, Deep Research, papers, fuentes y contradicciones.
- repo de código → documentación estrictamente necesaria para operar/desarrollar el software.

**Anti-bloat:** ningún agente crea “un documento por pensamiento”. Si una decisión cabe aquí, se actualiza aquí.

## 🧱 Producto — Polymarket Engine MVP

### Principio arquitectónico

```text
                     POLYMARKET ENGINE
                Go · modular monolith · 1 host
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
 market/protocol        research runtime      trading runtime
        │                     │                     │
 discovery              recorder/replay        auth/orders
 metadata/rules         experiment runner      reconciliation
 CLOB REST/WS           screen/shadow          capital/risk
 local books            datasets/metrics       kill switch
 positions/tokens       external-data hooks    live execution
 fees/incentives
 NegRisk primitives
 resolution lifecycle
        │
        └─────────────────────┬─────────────────────┘
                              ▼
                      STRATEGY CONTRACT
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
          POC-S01         POC-S02         POC-Sxx
          NegRisk         Sports          futuras
```

### Capabilities objetivo del Engine MVP

El Deep Research técnico debe confirmar nombres, contratos y autoridad exacta; esta lista define **capability intent**, no endpoint contracts todavía.

**Protocol / market model**
- Event / Market / Outcome / Token / Condition / parent-child relationships.
- Market lifecycle y estado operacional.
- Rules y resolution source versionadas cuando sea posible.
- NegRisk/Augmented NegRisk semantics.
- Positions/tokens, split/merge/redeem/conversion primitives relevantes.
- Combos/RFQ sólo si el research demuestra que son materialmente útiles al producto; no asumir.

**Market data**
- market discovery/catálogo;
- CLOB REST snapshots;
- market WebSocket y recovery;
- canonical in-memory order books;
- best bid/ask, midpoint, last trade y full depth separados;
- timestamps exchange/source/receive;
- gap, staleness y reconnect detection;
- metadata updates/new-market lifecycle.

**Recorder / datasets / replay**
- raw event recording;
- normalized events;
- deterministic replay;
- versionado de fee/rebate/reward/rules regimes por timestamp cuando aplique;
- reproducibilidad de un experimento;
- datasets derivados sin contaminar raw evidence.

**Research / hypothesis runtime**
- strategy/hypothesis registry;
- common experiment metadata;
- screen/read-only mode;
- replay mode;
- shadow mode;
- comparison scorecards;
- optimistic/base/stress fill models;
- executable-depth/VWAP primitives;
- latency sensitivity.

**Trading / execution**
- wallets/auth/session model exacto según docs;
- order create/cancel/manage lifecycle;
- real-time user/order updates;
- idempotency/retry/recovery semantics;
- reconciliation entre local state, CLOB y chain/account state;
- sizing, bankroll/exposure accounting, local risk;
- kill switch/cancel-all;
- live mode sólo después de certificación.

**Economics / incentives**
- fees como parámetros dinámicos, nunca constantes globales;
- maker/taker rebates;
- liquidity rewards;
- market competitiveness/eligibility cuando esté expuesto;
- capital lock y settlement timing como datos económicos.

**External data seam**
- el Engine debe admitir que una strategy consuma una fuente externa sincronizada (weather, sports, macro, crypto) sin convertir hoy esa posibilidad en un framework universal.
- primera implementación concreta sólo cuando una POC promovida la necesite.

**Observability**
- p50/p95/p99 del pipeline `receive → book → strategy → decision → send → ack/fill`;
- CPU/RAM/GC/disk I/O/queue depth;
- WS gaps/reconnects/staleness;
- strategy/opportunity/fill/reconciliation metrics;
- evidencia suficiente para distinguir fallo de infraestructura de ausencia de edge.

### Deliberadamente fuera del MVP del engine

- venue-agnostic abstractions;
- Kafka/Flink;
- microservicios por estrategia;
- Kubernetes por defecto;
- multi-region/co-location/HFT infra sin evidencia;
- Echo integration;
- UI compleja;
- LLM en el hot path;
- modelos ML específicos de estrategia;
- cualquier capability cuyo único argumento sea “quizás algún día”.

## 🖥️ Topología inicial

**Una máquina grande, con holgura deliberada.**

Objetivo: durante discovery/validación no introducir como variables independientes problemas de scheduling, service discovery, cross-host latency, consistencia distribuida o starvation de recursos.

Principios:

- hot state local;
- suficiente CPU/RAM/NVMe para recorder + replay + múltiples screeners;
- persistencia/analytics fuera del hot path;
- medir antes de optimizar coste;
- extraer proceso/host sólo por profiling, aislamiento real o recurso especializado.

## 🧩 Strategy POC contract

Una POC implementa **sólo lo que la hace distinta**. Conceptualmente:

```text
strategy
  ├── universe / eligibility
  ├── required data
  ├── relationship | fair-value model
  ├── opportunity detector
  ├── strategy-specific feasibility
  └── strategy-specific metrics
```

El engine conserva:

```text
market-data
books
recorder/replay
datasets
fees/incentives
full-depth execution model
shadow lifecycle
capital/risk
orders/reconciliation
observability
```

Una strategy no implementa su propio WebSocket, wallet, risk engine o replay si la capability ya pertenece al core.

## 🧪 Hypothesis lifecycle

Backlog objetivo: **20–30 hipótesis**, no 20–30 bots.

```text
IDEA / PE-xxx
    ↓
CHEAP TRIAGE
    ├── NO_SIGNAL / NO_DATA / BAD_ECONOMICS → REJECTED
    └── SURVIVES
          ↓
STRATEGY-SPECIFIC DEEP RESEARCH
          ↓
POC DESIGN / ASTRA WEEK si lo justifica
          ↓
SCREEN
          ↓
REPLAY
          ↓
SHADOW
          ↓
TINY_LIVE
          ↓
PROMOTED

cualquier etapa → ITERATING → nueva revisión
```

**Regla:** no gastar Deep Research grande ni Astra en una hipótesis que un cheap triage pueda matar.

Cada hipótesis conserva:

```text
id
mechanism
universe
required data
signal/detector
capital lock
capacity
latency sensitivity
competition
supporting evidence
contrary evidence
minimum experiment
GO / NO_GO
status
parent iteration
```

## 🧠 Uso de modelos premium — workflow frozen

### Principio

Astra y Fable **no descubren la API ni navegan documentación básica durante el diseño**. Toda información técnica vigente debe estar preparada antes en `30-resources/polymarket/`.

### Fase de diseño

```text
TECHNICAL RESOURCE PACK
        ↓
ASTRA — propuesta completa
        ↓
FABLE — adversarial challenge
        ↓
ASTRA — reconcile / segunda pasada
        ↓
FABLE — challenge final acotado si quedan findings materiales
        ↓
DESIGN FROZEN EN ESTE ARCHIVO
```

No hacer ping-pong infinito. Máximo esperado: **2 pasadas Astra + 1–2 Fable** para converger, salvo blocker material.

### Economía de Astra

Astra tiene cuota escasa (~3–4 shots/semana). Cada shot debe recibir un `CONTEXT PACK` cerrado y usar su ventana larga para trabajo estructural, no tareas pequeñas.

Uso preferente por fase:

1. propuesta/diseño completo;
2. reconciliación tras challenge;
3. auditoría de implementación o issue crítico;
4. shot de reserva si existe.

No usar Astra para collectors, structs, queries, boilerplate o bugs normales.

### Ventana Fable — antecedente de M1

La ventana hasta 2026-09-20 se consideró para el challenge de M1. FABLE completó F.1–F.9 y ASTRA-2 reconcilió sus doce findings; ASTRA-3 cerró la auditoría final. No queda otra ronda de arquitectura pendiente para este freeze.

## 🏗️ Delivery workflow del Engine

### M0 — Technical Knowledge Pack

**Objetivo:** mapear Polymarket técnico antes de diseño.

Entregable canónico en `30-resources/polymarket/`:

`Polymarket — Technical Platform Map — synced YYYY-MM-DD`

Debe incluir como mínimo:

- docs index/llms.txt y changelogs;
- hosts/base URLs;
- Gamma/market discovery;
- Data API;
- CLOB REST;
- WebSockets públicos y autenticados;
- RTDS/sports/Chainlink feeds si aplican;
- entities/IDs y relaciones;
- order book semantics;
- auth/wallet/session keys/signatures;
- order types/lifecycle/status/error/retry semantics;
- positions/tokens/CTF actions;
- NegRisk/Augmented NegRisk;
- resolution/UMA/redeem;
- fees/rebates/rewards;
- rate limits;
- contracts/addresses/audits;
- matching-engine restart semantics;
- OpenAPI/AsyncAPI artifacts;
- official SDKs y qué esconden vs API directa;
- historical-data availability/retention;
- deprecated/migrated endpoints;
- known ambiguities/contradictions;
- sync timestamp y source URLs por sección.

**Gate M0: PASS — DESIGN_READY documental (2026-09-17).** Astra/Fable pueden diseñar sin descubrir contratos básicos. Ver [[Polymarket — Technical Platform Map — synced 2026-09-17]] y §24 de part-10. Límites frozen de M0: CTF/v2 conversion LIVE DISABLED; L2 historical backfill DISABLED; RFQ/Combos OUT_OF_SCOPE inicial; `deferExec=true`/Builder optional DISABLED; trading live sujeto a pruebas posteriores de auth, execution y reconciliación bajo mandato de activación, fuera de M4 no-live según OD-2. Este gate NO constituye design freeze ni certificación live.

### M1 — Astra/Fable Engine Design

**Input:** este proyecto + Technical Platform Map + Edge Research Consolidado + restricciones del owner.

**Output:** actualización de ESTE archivo con:

- architecture boundaries;
- canonical domain model;
- data flows;
- state ownership;
- interfaces/contracts internos;
- persistence model;
- concurrency/backpressure model;
- error/retry/reconnect semantics;
- recorder/replay determinism;
- strategy contract;
- shadow/live lifecycle;
- security/secrets boundary;
- observability;
- test/certification strategy;
- explicit non-goals;
- decisiones arquitectónicas materiales sin resolver = 0 para pasar M2; políticas exclusivas de live pueden quedar `DEFERRED_LIVE_DECISION`, con `LIVE_DISABLED`.

**Gate M1: PASSED documental — `M1_DESIGN_FROZEN` (ASTRA-3, 2026-09-17).** Astra/Fable convergieron mediante la reconciliación, OD-1/2/3 están aprobadas y la auditoría final no deja findings arquitectónicos materiales abiertos. Ningún gate físico recibe PASS por este cierre.

### M2 — TOP Implementation Plan

Un agente TOP recibe exclusivamente este proyecto frozen y [[Polymarket — Technical Platform Map — synced 2026-09-17]]; consulta [[Polymarket — Edge Research Consolidado 2026-09-16]] sólo cuando una decisión de implementación necesite requirements transversales. Transforma FOUNDATIONAL NOW de M1.15 en el plan ejecutable **dentro de este archivo**:

- dependency order;
- slices/commits;
- allowed files/packages;
- contracts to implement;
- schemas y migration/storage setup;
- unit/integration/property/replay tests;
- physical gates;
- rollback/recovery;
- exact definition of done.

El TOP **no rediseña**. Si encuentra una contradicción arquitectónica material, detiene el trabajo afectado con `BLOCKED — DESIGN ISSUE` y la devuelve al manager. No debe inventar ownership, dominio, Strategy API, persistencia ni permisos para resolverla. Las políticas live pendientes no bloquean M2; ASTRA-3 sólo deja este handoff, sin escribir el plan.

### M3 — NORMAL Engine Implementation

Un agente NORMAL implementa el plan completo, preferentemente en una pasada coherente, con commits/gates definidos por M2.

- no inventar arquitectura;
- no expandir scope;
- failures/retries cerrados;
- tests obligatorios;
- actualizar este archivo al terminar;
- Agents-OS session close + feedback.

### M4 — Engine Certification

Antes de POC strategies:

- market discovery correcto;
- books/reconnect/recovery certificados;
- recorder/replay determinístico;
- regimes/metadata preservados;
- strategy test fixture funciona;
- shadow runtime funciona;
- auth/order plumbing puede permanecer disabled si live todavía no es necesario, pero interfaces/recovery deben estar diseñados;
- observability y resource headroom verificados;
- failure injection básica;
- backup/restore local consistente y medido según G-06b/G-14, sin depender de infraestructura remota;
- no critical/open architecture debt.

**Engine MVP CLOSED** cuando la plataforma puede consumir una strategy POC sin alterar fundamentos del core.

## 🎯 Primeras Strategy POCs

### POC-S01 — NegRisk

Primera POC estructural. Antes de implementación:

1. cheap triage usando capabilities del engine;
2. Deep Research específico y actualizado de NegRisk/Augmented NegRisk, conversions, `Other`, placeholders, execution/capital semantics, proyectos/papers y failure modes;
3. Astra week sólo si el triage sigue vivo;
4. implementar strategy module;
5. screen → replay → shadow → `GO | ITERATE | NO_GO`;
6. tiny-live sólo si supera gates.

### POC-S02 — Sports Combinatorial

Segunda POC estructural. Mismo pipeline:

1. cheap triage;
2. Deep Research específico de combinatorial sports, event grouping, payoff-state modelling, live vs pregame, latency/capacity, evidence/failures;
3. Astra review week;
4. strategy module;
5. screen → replay → shadow;
6. tiny-live si GO.

El orden S01/S02 puede invertirse por evidencia o calendario, pero ambos son consumidores del mismo engine y ninguno redefine el core por conveniencia local.

## 💰 Capital y live

Bankroll tiny-live inicial total: **US$300**.

Aplica a strategies promovidas, no al Engine MVP. Reglas:

- el engine puede existir y cerrar MVP sin arriesgar capital;
- POC strategy no necesita tiny-live para demostrar NO_GO;
- estrategias GO compiten por el mismo bankroll;
- diversificar entre eventos independientes cuando existe edge;
- capital ocioso es válido;
- caps por event/strategy derivados de shadow/stress, no inventados antes de datos.

## ✅ Tareas

### M0 — cerrado documentalmente
- [x] Ejecutar Deep Research técnico oficial de Polymarket #owner/me #type/research #area/personal
- [x] Ingerir resultado como `Polymarket — Technical Platform Map — synced YYYY-MM-DD` en `30-resources/polymarket/` #owner/me #type/research #area/personal
- [x] Reconciliar contradicciones con docs oficiales/changelog/OpenAPI/AsyncAPI #owner/me #type/research #area/personal
- [x] Confirmar nombre de repo de implementación Go: `xKoRx/polymarket-engine` (nombre acordado; verificar creación por separado) #owner/me #type/dev #area/personal

### M1 — cerrado: M1_DESIGN_FROZEN
- [x] Conservar M0 DESIGN_READY y boundaries disabled en el cierre aprobado por el owner; sin reapertura de research general #owner/me #type/research #area/personal
- [x] Context pack único utilizado por Astra/Fable, registrado en M1.0/F.1 #owner/me #type/research #area/personal
- [x] ASTRA-1: diseño completo Engine MVP #owner/me #type/dev #area/personal
- [x] FABLE: adversarial challenge, FBL-001…012 #owner/me #type/dev #area/personal
- [x] ASTRA-2: reconciliación de los doce findings #owner/me #type/dev #area/personal
- [x] Owner: OD-1/OD-2/OD-3 APPROVED por mandato ASTRA-3 #owner/me #type/dev #area/personal
- [x] ASTRA-3: auditoría final de consistencia y design freeze; challenge adicional no requerido al no quedar blocker material #owner/me #type/dev #area/personal

### Siguiente — M3/NORMAL en ejecución; M4 pendiente
- [x] TOP: implementation plan frozen en este archivo — plan entregado en `## M2 — TOP Implementation Plan`; freeze decretado por el owner al mandatar S01 (2026-09-17) #owner/me #type/dev #area/personal
- [/] NORMAL: implementar Engine MVP — **S01 Foundation DONE (2026-09-17):** repo `~/go/src/github.com/xKoRx/polymarket-engine`; foundation contracts v1, config estricta, archtest, `cmd/engine version`; build/vet/test/race verdes; coverage 95.2%; G-01 porción foundation completa (`S01_G01_FOUNDATION = PASS`, 62+60 vectores incl. boundary P03 §5 tras corrección M2-S01-C1; `G01_REGIME_INTEGRATION` NOT_RUN → S05) + G-15b base mecánica PASS con evidencia física en `testdata/foundation/evidence/`; G-02/G-03+ NOT_RUN; siguiente S02 ∥ S03 (barrera M2.2) #owner/me #type/dev #area/personal
- [x] NORMAL: M2-S02 Protocolo wire — **DONE, certificado por barrera M2-BARRIER-A (2026-09-17), checkpoint `af77074` en `main` sin push:** seam estable consumido por S03 (`protocol.Redact`/`SurfaceIdentity`/`PolicyV1`/versiones por superficie; archtest cero imports de red), parsers totales por superficie (Gamma con string-arrays y keyset/fallback offset, CLOB REST read-only, Market WS, Data v2 con sentinels, `ProtocolContext` CTF/V2/UNKNOWN), redaction schema v1 de 8 reglas frozen con validación recursiva y drop de `POLY_*`, fixtures versionadas con manifest SHA (44 archivos bajo `testdata/protocol/`), parsers fail-closed (JSON malformado, trailing data, profundidad excesiva); coverage protocol 95.3% en la regresión global; evidencia `g03.json` PASS + `g01_wire.json` PASS (extensión G-01 wire→decimal) + `s02_seam.json` #owner/me #type/dev #area/personal
- [x] NORMAL: M2-S03 Capture+Persist — **implementado e integrado (2026-09-17), checkpoints `2daaebc` (slice) y `2ac8985` (barrera M2-BARRIER-A) en `main` sin push:** `internal/capture` (envelope M1.6 completo, carriles EVIDENCE/RUNTIME con cuotas count/bytes y reserva, journal segmentado length-prefixed CRC32 + footer SHA-256, seal inmutable fsync+rename+dirsync+manifest atómico, recovery con sufijo inválido preservado como evidencia y discontinuidades durables, integridad por clase ACCOUNT_FACT/RESEARCH_EVIDENCE, vista consumer clamppeada a `durable_seq`), `internal/persist` (SQLite WAL synchronous FULL busy deadline vía modernc encapsulado, migraciones embebidas 0001–0003 forward-only con checksum y rechazo explícito de schema futuro, single writer serial con transacciones breves y timeout, cursors por reducer/namespace con regresión y `applied_seq > durable_seq` imposibles, outbox primitive idempotente sin sender, witness `capture_frontiers`), `cmd/engine journal verify` (segmentos/rangos/frontera/holes/tails/clases/checks explicados, exit 0/1/2, cross-check cursors↔journal); barrera certificó redacción-antes-de-persist, gap EVIDENCE durable y coverage persist 92.8→95.5% (13 tests de superficies de falla en `internal/persist/faultsurfaces_test.go`); evidencia `testdata/capture/evidence/g06.json` (8 escenarios G-06 parcial, cierre S06) + `g02b.json` (4 escenarios G-02b parcial, cierre S11) + insumos G-14 #owner/me #type/dev #area/personal
- [x] NORMAL: M2-S04 Catalog/Universe + Gamma read-only — **implementado y certificado en su alcance; estado `M2_S04_PARTIAL` (2026-09-18), checkpoint `fc26c35` en `main` sin push:** `internal/transport/gamma` (GET-only `/events`+`/markets` sin auth, offset pagination documentada ≤100, retries acotados con sleep inyectable), `internal/catalog` (reducer durable-before-projection con cursor propio sobre el journal EVIDENCE, revisiones inmutables dedup por content_hash con known_at = primera observación sin look-ahead, outcomes/tokens alineados por posición, quarantine para conflictos de identidad —arrays inconsistentes, condiciones no-bytes32, flips de condición, tokens/labels duplicados—, relaciones tipadas UNKNOWN/VERIFIED/INVALIDATED con evidencia —containment por anidamiento, membresía NegRisk VERIFIED con exhaustividad UNKNOWN, flag negRiskOther UNKNOWN, contradicciones INVALIDAN, complemento binario VERIFIED—, scans con fingerprint de filtros, anomalías declaradas y coverage complete sólo tras caminata limpia, UniverseSpec→UniverseRevision con UniverseChanged sólo material e historia consultable, Subscription Planner con refcount por owner y hook de retención stub explícito hasta S11), migraciones 0010–0016, CLI `catalog sync|inspect` con adaptadores capture→catalog y gamma→catalog en el composition root; G-04 PASS 16/16 con evidencia física `testdata/catalog/evidence/g04.json` + property rapid + sweep semilla 20260917 + verificación física del binario (segunda pasada idéntica: 0 revisiones nuevas; `journal verify` consistente); coverage catalog 95.0/gamma 97.5/cmd 89.6 (seam os.Exit, excepción heredada)/módulo 94.9; prueba real read-only contra `gamma-api.polymarket.com` ejecutada y registrada — reveló **`UPSTREAM_CONTRACT_ISSUE` del parser de fechas Gamma de S02** (rechaza `2021-12-05 20:37:01+00` y fracciones ≠0/3/6/9 como `.88434Z`; contraejemplo mínimo pineado en `testdata/catalog/fixtures/` con manifest SHA): mientras S02 no corrija, el sync real cuarentena páginas y marca partial (comportamiento honesto por diseño); la corrección es exclusivamente de S02 y no bloquea S05 → **cerrado por M2-S04-C1: `M2_S04_PASS` (2026-09-18, checkpoints `81aadb5` + `527dc73`), ver entrada de bitácora del cierre correctivo** #owner/me #type/dev #area/personal
- [ ] Certificar Engine MVP #owner/me #type/dev #area/personal

### Strategy pipeline
- [ ] POC-S01 NegRisk: triage → DR → design/review → implementation → shadow #owner/me #type/research #area/personal
- [ ] POC-S02 Sports: triage → DR → design/review → implementation → shadow #owner/me #type/research #area/personal
- [ ] Mantener backlog PE-001…PE-030 priorizado por coste de falsación #owner/me #type/research #area/personal

## 📆 Bitácora

- **2026-09-15** — Inicio como proyecto de arbitraje Sports + NegRisk.
- **2026-09-16** — Se consolida research en 30 hipótesis y se adopta modular monolith / single large host.
- **2026-09-16** — Reframing canónico: **Engine = MVP durable; strategies = POCs**. Se define M0 Technical Knowledge Pack antes de Astra/Fable y delivery `Astra → Fable challenge → Astra reconcile → TOP plan → NORMAL implementation`.
- **2026-09-17** — M0 DESIGN_READY documental: 11 partes del Technical Map; 7 OpenAPI/163 operaciones, RFQ AsyncAPI 13/13, Data v2 y NegRisk CTF investigados. Sin certificación live; conversion CTF/v2, historical L2 backfill y modos opt-in deshabilitados. Paso siguiente: revisión conjunta → ASTRA-1.
- **2026-09-17** — ASTRA-1 propuso M1, FABLE produjo doce findings y ASTRA-2 los reconcilió en `M1_RECONCILED_PENDING_OWNER_REVIEW`; sus registros se conservan abajo. El mandato ASTRA-3 aprueba OD-1/2/3; auditoría estructural final y correcciones normativas registradas en el cierre ASTRA-3 → `M1_DESIGN_FROZEN`. M1 cerrado; siguiente M2/TOP. Gates físicos NOT_RUN y live no certificado/deshabilitado; sin implementación, research adicional ni sincronización remota.
- **2026-09-17** — M2/TOP: plan de implementación producido dentro de este archivo (`## M2 — TOP Implementation Plan`): 13 slices sobre FOUNDATIONAL NOW, hitos M3-A…M3-E, mapa de gates no-live con fault injection, grupos de paralelismo con barreras y rangos de migraciones, política de entrega NORMAL, decisiones operativas (driver SQLite, decimal, librerías, toolchain) y `REQUIRES_OWNER — REPO LOCATION ONLY` para el path local de `xKoRx/polymarket-engine`. Estado `M2_PLAN_READY_FOR_MANAGER_REVIEW`; sin implementación ni rediseño; gates físicos NOT_RUN; live deshabilitado. Único archivo modificado: este proyecto.
- **2026-09-17** — **M2 freeze + M2-S01 PASS (mandato owner):** se resolvió el repo location (`~/go/src/github.com/xKoRx/polymarket-engine`, checkout existente) y se fijó baseline Go `1.27.0`/toolchain `1.27.1` (corrige `go 1.23` histórico). NORMAL implementó la foundation: IDs nominales por namespace (`GammaEventID/GammaMarketID/IntentID/FillKey/RunID/StrategyID/ExperimentID/VenueTradeID`), `AssetKey`/`ConditionRef`, `ProtocolIdentity` CTF/V2/UNKNOWN, decimal exacto coefficient+scale desde lexema JSON encapsulando shopspring (sin float64 ni `*big.Int` expuesto), unidades `Price/Shares/CollateralAmount/BasisPoints/FeeCoefficient`, `RevisionRef` con 9 owners cerrados, `Clock` wall+mono con fake clock, error taxonomy tipada (11 kinds), capability registry v1 deny-all (8 capabilities frozen no habilitables), `ExecutionMode` (default `LIVE_DISABLED`), `ActivationLease` contrato con request → `DISABLED`; config TOML estricta (unknown fields rechazados, schema v1 obligatorio, `LIVE_ENABLED` → FAIL/DISABLED, revision hash determinista); archtest (dirección de imports, sin `utils/common`, ciclos, gate de estrategias con probe unsafe/net/goroutine/clock/random en rojo y fixture neutral en verde); `cmd/engine version` sin networking ni negocio. Calidad: `go build/vet/test` verde, `-race` verde (property seed 20260917 registrada), coverage 95.1% total (foundation 95.0/config 97.8/archtest 97.1; cmd 83.9 por el seam `os.Exit` de main). Evidencia física: `testdata/foundation/evidence/g01.json` (62 vectores, hash de fixture `f6c2796f…`, expected/actual, build) y `g15b-base.json`. Verificación física: `go build` con stamp de commit imprime module/commit/toolchain/config schema. Deferred por mandato: tabla ticks/redondeos P03 §5 → S05 (rounding de órdenes = S02/protocol); migraciones/SQLite no creadas (S03). Repos modificado únicamente el proyecto + repo; sin push.
- **2026-09-17** — **M2-S01-C1 Numeric Boundary Completion (mandato correctivo owner):** cierra el único gap del S01 — el boundary numérico puro de órdenes P03 §5 que el plan frozen exigía. `internal/foundation/orders.go`: tabla de precisión documentada por tick (0.1/0.01/0.005/0.0025/0.001/0.0001 → 1-4/2/3-6 decimales; tick no documentado = escala desconocida → `UNSUPPORTED`), `ValidatePrice` (precio en (0,1) exclusivo, decimales ≤ máximo del tick, múltiplo exacto del tick vía coeficientes enteros alineados), `FloorSize` (size hacia abajo a 2 decimales), `RoundAmountUSD` (cláusula exacta ceil(A+4)→floor(A) sólo cuando excede los decimales de amount), `E6Amount` (enteros E6 con dominio uint256; conversiones units↔atomic exactas), `ComputeOrderNumbers` (secuencia oficial (1)-(6) sin sustituciones, revalidación de min_order_size después del rounding y revalidación final de invariantes sobre el propio resultado) y `OrderNumbers.Validate` (detecta tampering: roles maker/taker por BUY/SELL — BUY de NO sigue siendo BUY —, size sin floor, USD inconsistente con price×size, off-grid, overflow E6/uint256). Sin float64, sin tick hardcodeado: tick y min_order_size son value inputs; S05 conserva únicamente la integración de obtención/versionado del Regime. G-01 cerrado en su porción foundation: evidencia `testdata/foundation/evidence/g01.json` reestructurada con porciones explícitas — `S01_G01_FOUNDATION = PASS` (62 vectores base + 60 vectores P03 §5: ejemplo canónico BUY/SELL 0.52×10 con min 5 → maker/taker 5200000/10000000, todos los grids documentados, límites inmediatos dentro/fuera del grid, floor/ceil, E6, cero, 2^256-1 representable, overflow, escalas inválidas, negativos y casos donde el floor posterior invalida la operación por min-size) y `G01_REGIME_INTEGRATION = NOT_RUN` (owner M2-S05, extiende sin reescribir). Calidad: build/vet/test/race verdes, property seed 20260917 verde, coverage 95.2% total (foundation 95.1/config 97.8/archtest 97.1; cmd 83.9 por el seam `os.Exit`). Gates previos no degradados; sin scope creep (sin wire DTOs, REST, FeeResolver, Regimes ni SQLite).
- **2026-09-17** — **M2-S03 Capture Journal + Persistence implementado (mandato NORMAL, en paralelo con S02):** consumido exclusivamente el seam S02 declarado estable (`S02_SEAM_READY_FOR_S03` PASS: `protocol.Redact` + `SurfaceIdentity` + versiones; sin DTOs en construcción, sin tocar `internal/protocol`). `internal/capture`: envelope M1.6 completo con clases congeladas, un admisor con `capture_seq` como orden total local sin holes (toda validación antes de consumir secuencia), carriles EVIDENCE/RUNTIME hacia un secuenciador lógico con cuotas count/bytes independientes — saturación RUNTIME devuelve error tipado y pausa del run sin revocar epochs ni tocar la reserva EVIDENCE, overflow EVIDENCE real se declara con un control record `evidence_gap` duradero (intervalo exacto y refusal events conocidos; conteo de frames perdidos jamás inventado), sin drop-oldest ni colas ilimitadas; redacción S02 aplicada antes de escribir payload (test prueba que secretos no existen en ningún byte del journal); writer secuencial único con group commit configurable y acotado, `durable_seq` avanza sólo tras fsync (fault points before/after), locks que nunca abarcan fsync; journal segmentado append-only length-prefixed con CRC32 por record, footer con range/count/SHA-256 de región, seal inmutable vía fsync+rename+dirsync+manifest atómico (temp+fsync+rename+dirsync), segmentos acotados por bytes/edad; recovery escanea hasta el último record completo y checksum-válido, preserva el sufijo inválido como `.tail.bin` sin contarlo, no usa "latest file size" como frontera, reconstruye el índice derivado, sella/adopta lo que el crash dejó, abre boot nuevo y registra discontinuidades como control records durables; `durable_seq` = prefijo contiguo verificable (huecos congelan la frontera; bytes posteriores quedan como evidencia recuperable, nunca publishable). `internal/persist`: SQLite WAL synchronous FULL busy deadline foreign_keys vía modernc.org/sqlite encapsulado; migraciones embebidas (`migrations/embed.go`, 0001 schema_migrations, 0002 reducer_cursors, 0003 capture_frontiers) forward-only, una transacción cada una, checksum SHA-256 por archivo, app antigua contra schema futuro → FAIL tipado UNSUPPORTED, tampering de checksum → CONTRACT_DRIFT, rollback jamás automático; single writer goroutine con transacciones breves acotadas por write timeout (roll back + writer sobrevive), panic de job → error tipado; `reducer_cursors` por (reducer_id, namespace) con regresión → CONTRACT_DRIFT y `applied_seq > durable_seq` → INVARIANT_VIOLATION (provider de frontera inyectado; sin provider → fail closed); `capture_frontiers` como witness `(boot_id, durable_seq)` para G-14; outbox primitive (DDL canónico, enqueue idempotente por event_id, pending, mark-exported con stamp inmutable) sin ningún sender genérico. `cmd/engine journal verify`: inspecciona data-dir y explica segmentos/rangos/frontera durable/holes/discontinuities/tails preservados/clases con rangos/checks nombrados (manifest, segments, record_crc, contiguity, durable_frontier, integrity_classes), cross-check opcional de cursors contra la frontera del journal (`applied_seq > durable` → FAIL), exit 0 limpio / 1 integridad / 2 uso; verificación física ejecutada sobre fixture real. Quality: `go build/vet/test ./...` verdes, `-race` verde (admisión concurrente 8×25 mixta en ambos carriles sin race), `go mod tidy`, coverage total módulo 95.2% (capture 95.7/persist 93.2/cmd 91.6 con seam os.Exit heredado). Fault injection G-06: falla before/after fsync (frontera congelada, record invisible), write parcial (torn record preservado, jamás contado), seal en footer/rename/dirsync/manifest (prefijo intacto, daño declarado sólo si hubo pérdida real), manifest corrupto (fail closed CONTRACT_DRIFT), segmento faltante (hole declarado + frontera congelada), property rapid + sweep determinista (consumo sólo hasta `durable_seq` en cada quiescencia; durabilidad monótona post-crash). Evidencia: `testdata/capture/evidence/g06.json` (8 escenarios PASS) y `g02b.json` (4 escenarios PASS, journal×persist integrados), patrón `PM_ENGINE_EMIT_EVIDENCE` con re-check del registro commiteado. Checkpoint único del slice: commit `2daaebc` en `main`, selectivo sobre los archivos de S03, sin push y sin tocar los archivos en progreso de S02 (mismo árbol compartido). Migraciones usadas: 0001–0003 de la banda 0001–0009 (banda completa asignada a S03; sin GC, compresión ni backup).
- **2026-09-17** — **M2-BARRIER-A: integración S02×S03 certificada — `M2_S02_S03_INTEGRATION_PASS`, M3-A cerrado (mandato owner):** preflight: sin writer concurrente (sin procesos Go, mtimes quietos >9 min), snapshot SHA-256 del baseline (`91051d64…`, 153 archivos) verificado idéntico antes de ejecutar; S02 llegó como working tree sin commitear con `S02_SEAM_READY_FOR_S03` declarado — se verificó su contenido y se materializó su checkpoint `af77074`. **Seam (§2 del mandato):** imports de protocol desde capture/persist/cmd auditados — producción usa sólo `Identify/Redact/PolicyV1().Version()/ParseSurface/Surface` (archtest global sin imports de red fuera de paquetes archtest); camino `input→Identify/Validate→Redact→Admit→journal→fsync→durable_seq→Records` trazado en código y pruebas: toda validación precede al consumo de `capture_seq` (orden total sin holes), `sanitize()` corre el seam S02 antes de `encodeRecord` (sólo bytes sanitizados entran al journal), identidad inválida (`SurfaceUnknown`) y JSON malformado fallan cerrados antes de admisión (QUARANTINED, frontera intacta), el envelope conserva `redaction_policy/schema_version/normalizer_version/content_hash` del sanitizado y el round-trip mantiene `[REDACTED:*]`; `TestAdmitRedactsBeforePersistenceAndRoundTrips` escanea todos los bytes del journal con cuatro marcadores sintéticos; grep del repo sin secretos reales; detalles de control/anomalía son cadenas estructurales + SHA-256 (sin filtración de payload posible); fixtures de redacción 100% `SYNTHETIC-*`. **Durabilidad (§3):** `durable_seq` avanza en un único punto (`advance`) estrictamente tras el fsync del batch; `Ack.Wait`/`Records` clampean y rechazan lo no durable; saturación EVIDENCE fija `gapOpen=lastAdmitted` y el marcador `evidence_gap` viaja por el carril EVIDENCE con reserva de control (bypass de presupuestos en `enqueueLocked`) declarando `after_seq/resumed_at_seq/refusal_events` exactos antes del siguiente record de evidencia, jamás conteos inventados; saturación RUNTIME devuelve `ErrRuntimeSaturated` (pausa del run) sin tocar presupuestos EVIDENCE ni revocar epochs (la revocación es responsabilidad del consumer, según contrato S03→S06); fallo de escritura del marcador → writer falla terminal, `admitGate` bloquea toda admisión, `Ready()=false`, publicación detenida hasta recovery; recovery detecta la pérdida no persistida estructuralmente: sella el boot muerto, abre boot nuevo y persiste `boot_start` + una anomalía de control por discontinuidad (`recovered_tail/adopted_orphan/hole/missing_segment/overlap/unreadable`) con `awaitDurable` antes de retornar — el intervalo entre boots queda declarado, no cuantificado, y exige nueva sincronización. **SQLite×recovery (§4):** suite de persist reejecutada verde (cursors por reducer/namespace, regresión → CONTRACT_DRIFT, `applied_seq > durable_seq` → INVARIANT_VIOLATION con provider inyectado y fail-closed sin provider, rollback ante timeout/panic con writer sobreviviente, migraciones 0001–0003 forward-only con checksum/tampering→CONTRACT_DRIFT y rechazo de schema futuro, replay de prefijo tras crash, manifest corrupto fail-closed, segmentos huérfanos adoptados, sufijo parcial preservado como `.tail.bin`). **Coverage (§5):** discrepancia persist resuelta — 93.2% correspondía a la corrida aislada del paquete y 92.8% a la global con covermode atomic; ambos bajo el piso 95% por paquete → defecto corregido dentro del ownership S03 con `internal/persist/faultsurfaces_test.go` (13 tests útiles: cursors/witness/ledger/outbox ilegibles o corruptos nunca se reportan como sanos ni exportables; stamp de export inmutable → CONTRACT_DRIFT; commit disuelto nunca reporta éxito; snapshot contra schema extraño falla tipado) → persist 95.5% por paquete sin tests artificiales ni cambios de lógica; 12 statements restantes inalcanzables por API (migrate.go 47/55/59/70/85/118/152/157: embedded FS build-time, `INTEGER PRIMARY KEY` no seedable con texto, `rows.Err` post-iteración local; outbox.go 84: `RowsAffected` de modernc; 143: UPDATE fallando tras SELECT exitoso en misma tx; persist.go 110: driver fijo registrado; 176: rollback no-ErrTxDone sobre conexión muerta) → excepción técnica registrada con identificación de líneas, pendiente aprobación manager, no bloqueante. **Regresión global (§6) sobre árbol estable:** `go build ./...` OK, `go vet ./...` OK, `go test ./...` OK, `go test -race ./...` OK (incl. admisión concurrente 8×25), `go mod tidy` sin diff, `git diff --check` limpio; coverage final: módulo 95.4%, capture 95.7%, persist 95.5%, protocol 95.3%, cmd 91.6% (seam `os.Exit`, excepción heredada de S01), combinado S03 95.3%; evidencias S01/S02/S03 verificadas en PASS (g01, g15b-base, g03, g01_wire, s02_seam, g06, g02b; manifest SHA de fixtures validado por tests) sin regeneración. **Verificación física:** CLI `journal verify` sobre fixture generado con Capture (5 records + boot marker) → exit 0 con clases/rangos/frontera explicados; byte corrompido en segmento sellado → FAIL explicado, exit 1. **Gates (§7):** S01 G-01 foundation PASS (intacto); S02 G-03 PASS y G-01 porción wire PASS tras regresión global; S03 G-06 PARTIAL (cierre S06) y G-02b PARTIAL (cierre S11); G-14 insumos disponibles (ejecución S12); G-15b porciones comprobadas (cierre global posterior); G-02/G-04…G-13/G-16…G-19/G-14b NOT_RUN por diseño. Live permanece `LIVE_DISABLED`. Checkpoints locales `af77074` + `2ac8985` en `main`, sin push. **Siguiente: `M2-S04` habilitado; no iniciado.** Registro de run: `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-pm-engine-m2-barrier-a-s02-s03-integration.md`.
- **2026-09-18** — **M2-S04 Catalog/Universe + Gamma read-only implementado — `M2_S04_PARTIAL` (mandato NORMAL):** preflight sobre baseline estable (suite global verde, sin escritores concurrentes); APIs reales de S01–S03 inspeccionadas y consumidas sin reinventar nada. **Transport (`internal/transport/gamma`):** cliente HTTP exclusivamente GET contra `/events` y `/markets` (sin auth, sin wallet, sin POST/DELETE; test prueba que ninguna credencial viaja), paginación offset documentada del TPM (limit ≤100 P08 §21, bare JSON array; keyset NO inventado), retries acotados (429/5xx y errores de red, MaxRetry default 2, backoff exponencial acotado con sleep inyectable para determinismo, 4xx definitivos sin retry), page con evidencia de tiempos y retries. **Catalog (`internal/catalog`):** flujo `Gamma HTTP → Protocol → Capture → durable_seq → reducer → SQLite` con el composition root adaptando capture→`DurableSink` y gamma→`PageSource` (catalog no importa capture ni transport, según M2.1); el scan admite cada página cruda y espera durabilidad antes de continuar; el reducer consume sólo `Records` clampeadas a la frontera durable, proyecta en transacciones breves y avanza su cursor `("catalog","gamma")` en la misma transacción (`applied_seq > durable_seq` imposible); dedup por `content_hash` canónico — **dos pasadas idénticas producen cero revisiones nuevas** (probado en test, property y binario real); revisiones inmutables con `known_at` = receive wall de la primera observación (jamás derivado de fechas de fuente; source_at conserva la declaración del source como evidencia separada), `source_ref` por página/elemento y `capture_ref` completo (capture_id/seq/segmento/offset/crc); outcome rows alineadas por posición con AssetKey canónico; identidad por namespaces separados (gamma / ctf.137 / condition) sin conversiones; quarantine declarado con razón y detalle por: arrays Gamma inconsistentes (página falla cerrada, evidencia preservada, cursor avanza), condiciones no-bytes32 (protocol UNKNOWN → entidad condición en cuarentena + market marcado no elegible, jamás cast), flip de condición sobre el mismo Gamma ID (sin revisión nueva), tokens/labels duplicados, token inválido; relaciones tipadas con evidencia: containment VERIFIED sólo por anidamiento observado, membresía NegRisk VERIFIED con exhaustividad UNKNOWN (membresía jamás prueba equivalencia de payouts), flag `negRiskOther` sola → UNKNOWN, contradicciones (otro contexto, flag limpiado) → revisión INVALIDATED preservando la historia, complemento VERIFIED sólo con estructura binaria (2 pares alineados, endpoints normalizados); dedup de relaciones por (tipo, endpoints, estado, basis) — timestamps fuera del hash; scans con fingerprint SHA de filtros, progreso persistido por página, anomalías declaradas (`page_budget_exhausted`, `request_budget_exhausted`, `fetch_error`, `page_parse_failed`, `page_exceeds_limit`, `repeated_page_content`, `capture_failed`, `drain_failed`, `scan_interrupted_by_restart`), status complete sólo tras caminata monotónica limpia que agota el stream; scans stale de procesos interrumpidos se cierran partial; **nada se borra por pasada parcial**. **Universe:** `UniverseSpec` declarativo (name validado, hash canónico como identidad) → `UniverseRevision` determinista sobre el estado durable (members desde el catálogo con `RevisionRef` del dueño, exclusiones con razón: quarantined/not_active/closed/archived/condition_not_ctf), coverage complete sólo si las últimas scans de ambos kinds completaron, dedup por content hash (recompilar lo inmutable es no-op), `UniverseChanged` sólo por cambio material (miembros o coverage), revisiones previas consultables. **Subscription Planner:** unión de demandas con refcount por owner (re-set reemplaza, release elimina), plan determinista ordenado por forma canónica, hook de retención para assets con órdenes/posiciones con stub explícito que inventa cero estado de cuenta (S11 lo reemplaza). **Migraciones 0010–0016** (banda 0010–0019): entidades, revisiones, outcomes, relaciones+revisiones, scans, quarantine, universe revisions; ajuste mínimo y justificado a `internal/persist/persist_test.go` (el conteo fijo "3 migraciones" de S03 fue reemplazado por el modelo de bandas M2.4: prefijo S03 1–3 pineado, versiones estrictamente crecientes, checksums y no-op de re-migrate intactos — sin debilitar ninguna invariante). **CLI:** `catalog sync` (--data-dir/--base-url/--kind both|--events|--markets/--limit/--max-pages/--closed/--active/--archived/--json; resumen con observadas/nuevas/revisiones/duplicados/cuarentena/coverage/estado; partial es outcome honesto exit 0) y `catalog inspect` (entidad con revisiones/provenance/capture_ref/outcomes/quarantines/relaciones, --universe, --scans; ausencia declarada, jamás inventada). **G-04 (16/16 PASS, evidencia física `testdata/catalog/evidence/g04.json` con build, expected/actual y manifest de fixtures reales):** paginación multipágina, duplicados entre páginas, altas entre pasadas, paginación inválida (páginas idénticas consecutivas → partial), timeout a mitad de scan, 5xx con exactamente 1+1+2 requests, entidad ausente en pasada parcial preservada, reingesta idéntica cero revisiones, cambio de contenido → revisión 2 con revisión 1 intacta (known_at inmutable), arrays inconsistentes → cuarentena de página, identidades cruzadas rechazadas (no-bytes32 y flip), relaciones sin evidencia UNKNOWN, known_at sin look-ahead (source declara 2030, known_at = receive), crash + reproceso idempotente (recovery drena exactamente una vez; rollback de cursor → re-drenaje no-op), UniverseChanged sólo material, retención por hook sin estado de cuenta. **Property:** rapid (seeds frescos, contraejemplos auto-persistidos) + sweep determinista semilla registrada 20260917. **Cobertura de fallas:** DDL transaccional de SQLite (DROP TABLE dentro de la escritura → statement falla real → rollback restaura schema), colisiones UNIQUE/FK deterministas, stores cerrados, contenido corrupto declarado unreadable, sink que falla admisión/espera/lectura, storage muerto a mitad de scan. **Quality:** build/vet/test/race verdes, tidy sin diff, diff-check limpio; coverage catalog 95.0%, gamma 97.5%, cmd 89.6% (seam `os.Exit` + build-info + paths heredados — excepción técnica continuadora de S01/S03), módulo 94.9%, slice combinado 93.2%. **Prueba real read-only contra Gamma (HTTP 200, ejecutada):** el engine se comportó honestamente — bytes durables, páginas en cuarentena, scans partial con el error exacto — y **reveló `UPSTREAM_CONTRACT_ISSUE` del parser S02**: `TimeFieldGammaDate` rechaza `2021-12-05 20:37:01+00` (separador espacio + offset de 2 dígitos) y fracciones ≠0/3/6/9 como `.88434Z` (5 dígitos); contraejemplo mínimo pineado en `testdata/catalog/fixtures/` (páginas reales + manifest SHA-256 + propósito) con test que documenta las variantes por forma y queda verde antes y después de la corrección upstream. **Verificación física del binario:** sync doble contra fixture server estático → segunda pasada 0 nuevas revisiones/entidades, 2 duplicados por kind; `catalog inspect` muestra known_at/observed_at/source_at/source_ref/capture_ref/outcomes; `journal verify` cross-check consistente. **Estado: `M2_S04_PARTIAL`** — completo y certificado en fixtures; la proyección contra el servicio real queda bloqueada exclusivamente por la corrección S02 (fuera de este ownership; no invadido). Checkpoint `fc26c35` en `main` sin push. Live permanece `LIVE_DISABLED`; G-05+ NOT_RUN; siguiente S05 (Regimes/Resolution), que puede partir de las identidades frozen de Catalog en paralelo a la corrección del parser. Registro de run: `80-agents/journal/agent-runs/2026-09-18-zcode-glm-5.3-flash-pm-engine-m2-s04-catalog-universe-gamma.md`.
- **2026-09-18** — **M2-S04-C1: Gamma Date Contract + cierre de S04 — `M2_S04_PASS` (mandato correctivo owner, dos fases secuenciales):** preflight sobre baseline `fc26c35` (árbol limpio, sin otros writers, `.tmp.*` ajenos del vault intactos). **FASE A — corrección upstream S02 (checkpoint `81aadb5`, exclusivamente `internal/protocol` + sus tests/fixtures):** `TimeFieldGammaDate` pasó de RFC3339 estricto a una gramática cerrada Gamma-scoped — strict RFC3339 primero; separador espacio y offsets `±HH` de 2 dígitos (las variantes demostradas por el contraejemplo pineado de S04); fracciones de 1–9 dígitos aceptadas con precisión declarada como la unidad power-of-thousand más gruesa que representa el instante exacto (1–3→ms, 4–6→µs, 7–9→ns — reduce exactamente al mapping frozen 3/6/9; cero redondeo, la resolución declarada de la fuente sobrevive verbatim en el lexema raw, autoridad del content hash); zona explícita obligatoria (Z/±HH:MM/±HH — una fecha sin zona es ambigua y se rechaza, jamás se adivina como UTC/local); offsets validados ≤23h/≤59m explícitamente (la stdlib acepta `+24:00` y `+00:60` en layouts no-RFC3339 — verificado con probe); >9 dígitos, `±HHMM`, date-only, basura y trailing garbage rechazados; el lexema raw y la zona se preservan; date-only nunca se vuelve medianoche; ausente queda absent; sin `time.Now()`. Sin parser global permisivo: Data v2 (`TimeFieldDataV2ResolvedAt`, `...ConditionLastUpdate`) sigue rechazando las variantes nuevas (test de scoping). 6 fixtures nuevas (positiva con los lexemas demostrados verbatim `2021-12-05 20:37:01+00`, `2025-07-03T20:36:58.88434Z` + equivalentes inequívocos; negativas: fracción >9 dígitos, sin zona, offset +99, `±HHMM` no demostrado, fecha imposible) con provenance y date override en el manifest; manifest + G-03 + G-01-wire re-emitidos con el mecanismo existente (47 fixtures); probe G-03 nuevo `gamma_date_variants_counterexample` pinea la corrección y conserva el fallo anterior en el registro (`sin ocultar fallos anteriores`). G-03 PASS; protocol test/race/vet verdes. **FASE B — cierre S04 (checkpoint `527dc73`):** la primera pasada real falsó de inmediato la gramática inicial — Gamma emite también fracciones de **2 dígitos** (`2024-12-31T19:05:03.54Z`, `2025-07-11T18:36:03.15Z`), demostración que extendió la aceptación a la clase exacta 1–9 dígitos (documentada en el probe G-03 como historial, no oculta); además las páginas `/events` reales (limit 100, mercados anidados) miden ~4.5 MiB y exceden el record cap default de capture — el composition root (`cmd/engine`, wiring estrictamente necesario) fijó `MaxRecordBytes=16 MiB` para el path catalog y `WriteTimeout=30s` (el drain usa sub-batches acotados por bytes de payload, 1 MiB, para mantener las transacciones breves del contrato persist). **Sync real read-only ×3 pasadas** (`closed=false`, budgets default): pasada 1 — 2,100 eventos + 2,100 mercados observados, 23,966 revisiones nuevas, 54 cuarentenas genuinas (`outcome_arrays_missing`: mercados reales de Gamma sin arrays de outcomes/tokens; re-declaradas por pasada como auditoría con capture_seq propio, intactas y explicadas; **cero cuarentenas por el defecto temporal**); pasadas 2–3 — 0 entidades nuevas, duplicados idénticos 18,388+2,001+2,100 y revisiones nuevas (1,913/3,202/99) **todas atribuidas a cambio real del servicio** (diff campo a campo sobre 4,264 pares consecutivos: `updatedAt` del servidor Gamma en el 100% + `prices` 315 + `unknown_fields` 245; pass 3 de markets: **0 revisiones nuevas** — idempotencia exacta demostrada; la pasada parcial histórica no se reescribe: sigue partial con su `fetch_error`); `catalog inspect` con known_at/observed_at/source_at UTF-8 válido/source_ref/capture_ref/outcomes; `journal verify` exit 0 post-rotación (16 segmentos, ~197 MB, contigüidad + frontera durable + cross-check cursors); known-at sin regresión verificada por SQL (first_known_at == revisión 1 en 83,956 entidades). **Defectos demostrados por el wire vivo, corregidos con test de regresión cada uno:** (1) dedup de revisiones sólo contra la última → oscilación A→B→A de datos vivos violaba `UNIQUE(entity_id, content_hash)` y mataba el drain (ahora la historia es conjunto de contenido: retorno = duplicado, current pointer permanece en la última revisión; semántica impuesta por la UNIQUE del schema frozen); (2) mismo defecto en relaciones (`UNIQUE(relationship_id, content_hash)`, VERIFIED→INVALIDATED→VERIFIED); (3) `source_at` cortaba la flecha `→` por bytes dejando UTF-8 inválido en la columna (corte por rune completo); (4) un drain fallido tras otro error del walk se ocultaba (ahora `drain_failed` se declara siempre y los contadores drenados en cero lo evidencian); (5) **desviación única del scope nominal de FASE B, disclosed:** `internal/capture/writer.go` — `segPaths` no seguía el rename active→sealed al rotar/sellar, todo lector en el mismo proceso perdía los segmentos sellados (el doc de `segmentPath` declara ese cambio de path; recovery repoblaba el mapa y por eso los tests S03 no lo vieron); fix root-cause de 1 línea + comentario en rotate/finalSeal, sin cambio de contrato, blocker demostrado del sync real — sometida a revisión manager, revertible en un commit. **G-04 re-emitido: PASS 20/20** (16 originales + 4 correctivos: oscilación de contenido, oscilación de relación, source_at rune exacto, declaración combinada fetch_error+drain_failed) con Portion actualizada al cierre. **Techo upstream no documentado:** Gamma responde HTTP 422 a `offset > 2000` en `/events` y `/markets` (sondeado read-only: 2000→200, 2050/2100/2150→422) — la caminata del universo activo es upstream-imposible de completar vía offset pagination; queda partial honesto con `fetch_error` exacto y el gap documentado como el keyset ya declarado. **Quality:** build/vet/test/race globales verdes, tidy sin diff, diff-check limpio; coverage módulo 95.1% (catalog 95.1 aislado / 95.0 global, gamma 97.5, cmd 89.6 — excepción os.Exit heredada no extendida; slice S04 combinado 93.9%, composición catalog+gamma+cmd). Gates: G-03 PASS (S02-C1), G-04 PASS 20/20, G-06 PARTIAL hasta S06, G-01 wire porción PASS re-emitida; `LIVE_DISABLED` sin cambios; G-05+ NOT_RUN. Sin push. Registro de run: `80-agents/journal/agent-runs/2026-09-18-zcode-glm-5.3-flash-pm-engine-m2-s04-c1-gamma-date-contract.md`. **Siguiente: `M2-S05` (autorizado por el mandato al cerrar PASS).**

- **`S04_BASELINE_ACCEPTED_FOR_S05` — preflight del mandato S05–S13+M4 (2026-09-18, checkpoint `e28c7eb`):** baseline verificado (`527dc73` HEAD, árbol limpio, ambos SHAs esperados presentes); regresión global verde (build/vet/test/race/tidy/diff-check). Parche fuera de scope `internal/capture/writer.go` RATIFICADO: causa raíz correcta (mapa `segPaths` no seguía el rename active→sealed; recovery repoblaba el mapa y por eso los tests de re-apertura no lo veían), fix de 2 líneas coherente con `recover.go` — y ahora con test de regresión dedicado en ownership de Capture que falla pre-fix (apuntando al path `.active` retirado) y pasa post-fix; la excepción de cobertura cmd/engine 89.6% queda confirmada como seam `os.Exit` heredado (main/exitWith, sin lógica nueva oculta). Gofmt aplicado a 12 archivos S04 (higiene mecánica). Cobertura módulo 95.1%. Gamma `offset>2000` permanece documentado como partial honesto. S05 autorizado a comenzar. #owner/agent #type/dev #area/personal

## 🧭 Decisiones frozen

- `D-001` — Producto canónico: **Polymarket Engine — MVP**.
- `D-002` — Engine agnóstico de estrategia, deliberadamente Polymarket-specific.
- `D-003` — Go + modular monolith + un deployable + un host grande inicialmente.
- `D-004` — Engine no es POC; strategy modules sí lo son y pueden descartarse.
- `D-005` — Un solo archivo de proyecto como autoridad operativa; evitar proliferación documental.
- `D-006` — Antes del diseño, crear mapa técnico completo de la plataforma desde fuentes oficiales.
- `D-007` — Astra/Fable no gastan contexto descubriendo endpoints básicos.
- `D-008` — Diseño: Astra propone, Fable challengea, Astra reconcilia; ping-pong acotado.
- `D-009` — TOP planifica implementación después del design freeze; NORMAL implementa sin rediseñar.
- `D-010` — NegRisk y Sports son POC-S01/S02, primeros consumidores del Engine.
- `D-011` — Cada estrategia posterior pasa cheap triage antes de Deep Research/Astra.
- `D-012` — Bankroll tiny-live US$300 total aplica a strategies promovidas; no define éxito del Engine MVP.
- `D-013` — Echo/Echo Forge siguen separados hasta evidencia posterior de integración útil.
- `D-014` — No Kafka/Flink/K8s/microservices salvo necesidad demostrada.

## 🔗 Docs / Links

- [[Polymarket Engine — Opportunity Context]]
- [[Research — Merge de cuatro Deep Research]]
- [[Polymarket — Edge Research Consolidado 2026-09-16]]
- [[Polymarket — Technical Platform Map — synced 2026-09-17]] — índice canónico y 11 partes, knowledge pack M0 DESIGN_READY.
- [[polymarket/00-index]]
- Polymarket official docs: https://docs.polymarket.com/
- Polymarket official docs index: https://docs.polymarket.com/llms.txt

## 💡 Principios

- El engine se optimiza para **falsar hipótesis rápido y de forma reproducible**, no para demostrar que una estrategia favorita funciona.
- `net executable edge > theoretical edge`.
- observabilidad suficiente para separar “no hay edge” de “nuestro sistema midió mal”.
- lo común se promueve al core sólo cuando es verdaderamente común o es capability fundamental de Polymarket.
- una strategy no deforma el core para facilitar su propia POC.
- ninguna IA premium debe gastar una ventana larga en información que pudimos preparar previamente.

## M1 — ASTRA Architecture Proposal

**Estado del shot:** `M1_ASTRA_PROPOSAL_READY_FOR_FABLE` · **Etiqueta:** `M1 — ASTRA PROPOSAL — READY FOR FABLE` · **Autor:** ASTRA-1 · **Fecha:** 2026-09-17. Esta sección propone arquitectura; no congela M1, no aprueba gates físicos, no implementa estrategias y no contiene el plan de coding de M2. Las decisiones `D-001…D-014` y el gate documental M0 permanecen vigentes. Todas las decisiones nuevas requieren challenge de FABLE y reconciliación antes del freeze.

**Precedencia normativa ASTRA-3 · 2026-09-17:** estado vigente `M1_DESIGN_FROZEN`. ASTRA-1 produjo la propuesta y ASTRA-2 la llevó a `M1_RECONCILED_PENDING_OWNER_REVIEW`; se conservan sus registros y F.1–F.9 como historia. OD-1/2/3 están `APPROVED`. M1.1–M1.17, reconciliadas por ASTRA-2 y corregidas por ASTRA-3, son el contrato frozen; las recomendaciones incompatibles y handoffs de los shots históricos no son instrucciones vigentes. M1.15 gobierna el alcance de implementación y sus gates. El cierre ASTRA-3 registra la auditoría final y el handoff M2/TOP. M0 permanece cerrado para diseño; ningún gate físico fue ejecutado ni capability live activada. Único archivo modificado: este proyecto.

### M1.0 — Base documental, autoridad y criterio de éxito

**Baseline leído antes de editar:** `xKoRx/agents-os`, `master`, HEAD local y remoto `822d6241de37628dfe04ab1683fbb3e79b899dd6`, worktree limpio; blob original del proyecto `10f2c8df0b95e5147aef5457e80ef4cb721de054`. Bootstrap mínimo de Agents-OS aplicado; ninguna fuente técnica ajena al context pack fue consultada. No se abrieron Internet, SDKs, contratos externos, investigaciones originales ni otros proyectos.

| Referencia interna de esta propuesta | Fuente leída íntegramente | Uso y autoridad |
|---|---|---|
| Proyecto | Este archivo, contenido anterior a M1 | Producto, macroarquitectura, capabilities, capital y workflow frozen |
| TPM / manifiesto | [[30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17]] | Once partes verificadas individualmente y concatenadas: **287930 bytes**, SHA-256 `ca7e3329b39f666fa0d383ffae194e6aa09f2e741b31cea61a4dc72136be8938`, manifiesto 2026-09-17 15:35 UTC |
| P01, §§1–2 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-01-foundations]] | Superficies e identidades |
| P02, §3 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-02-rest-catalog]] | REST y DTO Data v2 |
| P03, §§4–6 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-03-auth-precision-time]] | Auth, precisión y relojes |
| P04, §§7–8 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-04-orders-lifecycle]] | Firma/DTO/wrapper, órdenes y ambigüedad |
| P05, §§9–11 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-05-market-data-positions-contracts]] | WS, books, posiciones y contratos |
| P06, §§12–13 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-06-negrisk-combos]] | CTF/v2, NegRisk, exclusión Combo/RFQ |
| P07, §§14–18 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-07-economics-resolution-history-limits]] | Fees, incentivos, resolución, históricos y cuotas |
| P08, §§19–21 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-08-specs-sdks-changelog]] | Extracciones posteriores, schemas, versiones y discrepancias |
| P09, §§22–23 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-09-security-workflows]] | Seguridad y flujos de protocolo |
| P10, §§24–25 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-10-gaps-recovery]] | Estado vigente M0, límites y recovery |
| P11, §26 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-11-sources]] | Provenance y snapshots; sus URLs no se visitaron en este shot |
| ERC, §§2–8 | [[30-resources/polymarket/Polymarket — Edge Research Consolidado 2026-09-16]] | Requisitos transversales de falsación, costes, sesgos y evidencia; no autoridad de protocolo ni estrategia implementada |

**Precedencia acotada:** el cierre fechado de P10 §24 gobierna el estado de M0 sobre encabezados históricos que todavía dicen “RG pendiente”; los DTO expandidos de P02 §3.4.1 y P08 §19.1.1 precisan tablas anteriores. Una contradicción técnica que esas ampliaciones no resuelven se conserva como incertidumbre. Ejemplos: fees Sports del ERC no se convierten en configuración; §25.2 rotula keyset como CLOB, mientras el inventario S39 lo ubica en Gamma: este diseño usa el host Gamma del inventario de operaciones. `GET /markets/{conditionId}` de §25.1 no reemplaza el contrato explícito CLOB `/clob-markets/{condition_id}`. No se corrige ni se modifica el pack en M1.

**Éxito del engine:** un consumidor nuevo declara universo, datos y lógica diferenciadora; obtiene captura, replay, economics, shadow, risk y métricas comunes sin construir infraestructura paralela. Medir `TIME_TO_VALIDATED_HYPOTHESIS` desde registro aceptado hasta scorecard revisable `GO / ITERATE / NO_GO`, incluyendo tiempos de espera por datos y separando horas humanas, cómputo y coste. No se promete rentabilidad ni se exige desplegar los US$300 para cerrar el MVP.

### M1.1 — Matriz contractual y superficie activable

Los estados siguientes no son sinónimos. `SUPPORTED FOR DESIGN` admite modelar una capability; `IMPLEMENTABLE FROM DOCUMENTED CONTRACT` permite construir la ruta descrita, sin certificarla; `REQUIRES INTEGRATION VALIDATION` bloquea su activación live hasta evidencia; `DISABLED` impide construir/enrutar una operación ejecutable; `OUT_OF_SCOPE` excluye la implementación inicial. Una fila puede tener estado documental y estado operativo distintos.

| Capability | Suficiencia documental | Estado operativo propuesto y condición |
|---|---|---|
| Discovery Gamma, snapshots REST, Market WS básico | IMPLEMENTABLE FROM DOCUMENTED CONTRACT | Read-only tras gates de parsing/recovery; continuidad siempre observada, nunca garantizada |
| Lifecycle `new_market`, resolución WS y Sports | SUPPORTED FOR DESIGN; campos críticos descritos | Parsing conservador; variantes no expandidas quedan como observación raw y disparan refresh, no inferencias de fields ausentes |
| Recorder, replay de captura, datasets, SCREEN, SHADOW | SUPPORTED FOR DESIGN | Implementables como contrato interno; gates M1.15 pendientes |
| Data v2 posiciones/trades/activity/resolutions | IMPLEMENTABLE FROM DOCUMENTED CONTRACT | Lecturas agregadas; no sustituyen el ledger privado ni la cadena |
| Auth L1/L2 y órdenes CTF sobre CLOB v2, User WS, cancel/reconcile | IMPLEMENTABLE FROM DOCUMENTED CONTRACT + REQUIRES INTEGRATION VALIDATION | `LIVE_DISABLED` por defecto; aprobación independiente por wallet, protocolo y operación |
| Fee inputs y cálculo publicado | IMPLEMENTABLE FROM DOCUMENTED CONTRACT en el alcance de P03/P07 | Mapping de parámetros y redondeo no totalmente resueltos: economics intervalar; live taker bloqueado donde no exista cota certificada |
| CTF split/merge/redeem | IMPLEMENTABLE FROM DOCUMENTED CONTRACT + REQUIRES INTEGRATION VALIDATION | Capability modelada; dispatch de transacción deshabilitado inicialmente; no es prerequisito de M4 read-only/shadow |
| Protocol-v2 posiciones, rutas Router/PositionManager | SUPPORTED FOR DESIGN | Observación/identidad versionada; encoding y ejecución de cada operación requieren contrato y certificación adicionales |
| NegRisk conversión CTF | SUPPORTED FOR DESIGN; ABI fuente documentada | **DISABLED live**: deployment, mapping, permisos y ruta sin certificación; simulación sólo bajo supuestos explícitos |
| NegRisk conversión Protocol-v2 | SUPPORTED FOR DESIGN como capability ausente | **DISABLED**, ABI/selector y flujo de assets no verificados; no se prepara calldata |
| Backfill L2 vía `/orderbook-history` | No hay contrato de completitud | **DISABLED**; no reemplaza recorder ni rellena silenciosamente gaps |
| `deferExec=true`; Builder optional/CRUD/atribución | Fuera del contrato certificado | **DISABLED**; `deferExec=false`, builder cero y sin opciones para activarlos por estrategia |
| Combo/RFQ/Exchange-v3; Bridge/funding automático | Documentados parcialmente, sin necesidad inicial | **OUT_OF_SCOPE**; Sports combinatorial es relación entre mercados, no autorización de Combo/RFQ |
| Session Keys beta, auto-deploy de wallet, auto-approvals | SUPPORTED FOR DESIGN en su scope documentado | **DISABLED inicialmente** por propuesta de seguridad; owner puede promover una ruta después, nunca heredar permiso del SDK |
| External-data seam | SUPPORTED FOR DESIGN | Envelope, calidad y replay comunes; adaptador externo concreto sólo al promover una POC que lo requiera |

**Invariante:** el registro de capabilities es una allowlist versionada y cerrada. Una capability ausente, desconocida o deshabilitada no produce un comando de ejecución. Un flag de configuración no puede crear un adapter que el registro no ofrece. `LIVE_ENABLED` jamás levanta en bloque los bloqueos de conversión, v2 o modos opcionales.

### M1.2 — Arquitectura, responsabilidades y ownership

**Contrato frozen (OD-2):** un binario Go, un proceso de servicio, módulos internos con puertos estrechos, SQLite embebido para estado transaccional, journal raw segmentado en NVMe y datasets derivados con manifest/lineage en SQLite/JSONL inicialmente; Parquet queda diferido detrás del mismo schema lógico. El mismo binario puede correr el modo offline de replay; no se agrega un servicio por estrategia, una cola distribuida ni una segunda base operativa. Analytics/exportación y replay usan presupuestos de recursos independientes del servicio activo.

```text
CONTROL: config versionada + capability registry + supervisor + control local
                         │ inicia y revoca permisos
Gamma / CLOB / WS / Data / chain reads / external seam
                         │ adapters de transporte (sin dominio mutable)
                         ▼
Ingress → Capture Journal → watermark durable → normalizadores versionados
                                                   │
              ┌─────────────────┬──────────────────┼──────────────────┐
              ▼                 ▼                  ▼                  ▼
        Catalog/Universe    Book shards       Regime/Resolution   Account observations
              └─────────────────┴─────────┬────────┘                  │
                                  immutable frames                   ▼
                                         │                  Account Coordinator
                                  Strategy Runtime             orders/fills/ledger
                                         │                           ▲
                                   Opportunity                       │
                                         ▼                           │
                                Economics/Evaluator                  │
                                         │                           │
                               candidate action                      │
                                         ▼                           │
                           Risk + atomic reservation ────────────────┤
                                         │                           │
                         SCREEN | Simulator | Live gateway ──────────┘
                                              │
                                 Credential boundary → CLOB

Journal + versioned state → Replay/Experiments → scorecards/datasets
Observability recibe métricas de todos; nunca controla dominio por logging.
```

| Módulo | Responsabilidad y único estado del que es owner | Puertos/dependencias permitidos |
|---|---|---|
| Composition / Supervisor | Ciclo del proceso, capability registry, leases de activación, config revision, fallos y readiness | Construye adapters y módulos; puede detenerlos, no modificar sus proyecciones directamente |
| Transport / Venue adapters | Conexiones REST/WS, subscriptions deseadas, epochs, rate budgets IP/signer, parsing de envelope y auth de transporte | Escribe en Ingress; recibe comandos de Catalog/Execution por puertos; no escribe books ni posiciones |
| Capture | Orden local de admisión, journal, watermarks durables, manifests de captura/segmentos y bundle de backup, integridad y discontinuidades | Recibe evidencia/control; entrega offsets; no conoce fórmulas de estrategias ni decide órdenes |
| Catalog / Universe | Revisiones Event/Market/Outcome/Asset/Condition, relaciones documentales, reglas y membership por consumidor | Lee observaciones normalizadas; publica revisiones inmutables y subscription demand; consulta REST mediante adapter |
| Market Data | Books por asset, revisión, epoch, calidad; proyecciones BBO/midpoint/trade separadas | Consume catálogo/WS; publica snapshots inmutables; no llama estrategias ni REST desde el reducer |
| Regimes / Resolution | Versiones de tick/min-size/fee/reward/delay y observaciones de resolución con provenance | Consume REST/WS/chain; publica constraints y lifecycle; cambios de régimen invalidan frames y candidatos |
| Frame Builder / Runtime | Suscripciones de consumidores, frames consistentes localmente, secuencia de delivery, estado de cada instancia Go | Lee snapshots; invoca estrategia serialmente; publica resultados; no conoce credenciales |
| Economics / Simulator | Economics: funciones puras de VWAP/costes/capital. Simulator: estado del fill model, agenda de eventos sintéticos y liquidity ledger por namespace del experimento | Recibe frame+candidato+modelo; propone observaciones sintéticas al Coordinator virtual. Órdenes/fills contables, reservas y BasketExecution simulados tienen como único writer ese Coordinator; nunca actualiza cuenta real |
| Risk | Reglas versionadas de límites, eligibility y sizing, evaluador puro sobre snapshot de cuenta | Devuelve decisión acotada al Account Coordinator; no mantiene una segunda copia de balance disponible |
| Account Coordinator | **Único writer de cuenta real:** órdenes/intents, fills, reservas, posiciones contables, balances observados, atribución, dedup, `BasketExecution` y reconciliación | Ejecuta reducers Risk/Orders/Ledger/Basket dentro de la transacción de cuenta; autoriza cada leg, recibe observaciones Reconciler/resultados Execution. Mismo reducer en namespaces de cuenta simulada; nunca mezcla sus stores con cuenta real |
| Execution / Reconciler | Execution posee workers y estado transitorio del I/O, no el registro durable del attempt; Reconciler posee jobs/cursors de consulta/observaciones pendientes, no ledger alternativo | Coordinator persiste y reclama el attempt antes del I/O; Capture conserva evidencia durable; Reconciler consulta REST/User WS/chain y propone hechos al mismo Coordinator, sin mutar su cuenta ni su applied_seq |
| Credentials / Signing | Material secreto y sesión autenticada, perfil wallet y permisos; firma sólo payload tipado ya autorizado | Sólo Execution autorizado puede solicitar firma/envío; no puerto genérico `sign(bytes)` a estrategias |
| Experiment / Dataset | Registry de hipótesis, manifests de experimento inmutables, parámetros, versiones, scorecards, pins de retención, artefactos derivados | Referencia manifests de captura sin mutarlos; consume projections/runtime; no toca tablas privadas de ejecución ni reescribe raw |
| Operations / Telemetry | Logs, métricas, alertas y comandos locales autenticados | Kill/control por Supervisor; consultas de snapshots; no SQL arbitrario ni callbacks de estrategia |

**Regla de acoplamiento:** domain values y contratos públicos no importan adapters. Un módulo no importa implementaciones/repositorios de otro ni consulta sus tablas; solicita una vista o emite un comando tipado. No hay “event bus de cualquier cosa” ni service locator global. Los eventos de observación y comandos de efecto son tipos distintos. El composition root es el único lugar que conecta puertos. Los reducers de cuenta comparten una transacción porque reserva, intent y exposición forman una sola unidad de consistencia; esta dependencia es deliberada y no se extiende a catálogo, books o analytics. Contratos, dependencias y ownership se verifican en revisión y pruebas de imports de M2, sin inventar hoy un árbol de paquetes definitivo.

**Enmienda de ownership ASTRA-2, FBL-006/009:** Basket es estado del Coordinator, no otro servicio ni scheduler de la POC. Execution sólo realiza I/O autorizado; Simulator produce observaciones sintéticas para los mismos reducers y tiene su liquidity ledger aislado. Capture posee ambos carriles de admisión y el secuenciador; Runtime puede pausar runs, nunca invalidar un epoch por saturación propia. Supervisor posee `DEGRADED_AUDIT`/leases; Reconciler propone evidencia y Coordinator decide sus efectos contables.

**Precisión ASTRA-3 de owner único:** Catalog posee identidad/relaciones/membership de Universe; Runtime posee demanda y delivery por consumidor; Transport posee subscriptions/epochs de conexión y cada Book shard su proyección/quality asociada a ese epoch. Regimes/Resolution posee constraints y lifecycle observado, sin reescribir identidad de Catalog. Capture posee bytes/manifests de captura; Experiment posee manifests/pins de runs que los referencian. En cuenta real o virtual, Coordinator es el único writer de intents/attempts, órdenes/fills contables, reservas/atribución y BasketExecution; Simulator sólo posee liquidez/modelo/eventos sintéticos. Observaciones pendientes de Reconciler y evidencia inmutable de Capture no son otra cuenta. G-02b/G-08/G-10c verifican estos límites.

**Hot path:** admisión/captura durable → normalización → book/quality → frame → detector/evaluator → decisión; en live agrega reserva/intent durable → firma/envío. No LLM, consultas analíticas, exportación, metadata REST síncrona ni llamadas arbitrarias de estrategia. La latencia de fsync es parte del coste elegido y debe medirse. **Cold path:** discovery/refresh, compactación, SQL de reporting, extracción Parquet, backups, fixtures, replay y scorecards. Reconciliación, heartbeat y cancelación son un carril operacional prioritario; no compiten detrás de screener/replay.

**Inicio:** lock exclusivo de cuenta/estado local → validar config/schema/manifests/capabilities → recuperar journal y transacciones → iniciar captura y observabilidad → adapters públicos/catálogo/constraints → suscripciones y books nuevos → admitir runtimes elegibles. Un perfil live agrega carga explícita de identidad, check de restricciones/clock, User WS, reconciliación completa y resolución de intents ambiguos; siempre arranca `LIVE_DISABLED/RECOVERING`, nunca retoma permiso previo por persistencia de un booleano. Fallar startup de un writer no impide exponer health y diagnóstico read-only.

**Shutdown:** cerrar admisión de nuevas oportunidades/órdenes → revocar lease de envío → cancelar remanentes según política de cuenta → mantener User WS/REST y recorder mientras se concilia → detener estrategias cooperativamente → sellar journal/watermark y cerrar stores. Deadline agotado deja `UNCLEAN/UNRESOLVED` durable y alerta; no registra shutdown limpio ni “sin órdenes” sin prueba. SIGKILL/power loss se trata como recovery, no como ejecución de este protocolo.

### M1.3 — Dominio canónico, unidades y temporalidad

Clases: **E** entidad con identidad estable y estado mutable bajo owner; **S** snapshot inmutable con revisión; **D** derivación reproducible; **O** evento observado con provenance. Toda revisión conserva `observed_at`, `source_at?`, `source_ref`, `capture_ref`, versión del normalizador y payload hash. `effective_from` sólo existe si la fuente lo establece; ausencia significa “conocido desde observación”, no vigencia histórica inventada. Dos tiempos separados evitan usar metadata futura en replay.

| Modelo | Identidad interna y relaciones obligatorias | Clase / autoridad |
|---|---|---|
| Event | `GammaEventID` decimal canónico como string; slugs son atributos; contiene relaciones hacia markets y, cuando documentado, parent/subevents | E + S; Catalog, Gamma |
| Market | `GammaMarketID` independiente; links `ConditionRef?`, Event IDs, outcomes ordenados, reglas/source y operational flags | E + S; Catalog; trading eligibility derivada cruza CLOB/constraints |
| Outcome | `(GammaMarketID, outcome_index)` y label versionado; rol YES/NO validado por mapping, no por BUY/SELL | S; array de outcomes alineado con IDs, nunca join sólo por etiqueta |
| Asset / Token / Position instrument | `AssetKey{chain_id, protocol, token_contract?, wire_asset_id}`; variante CTF con token uint256; variante ProtocolV2 con position ID opaco validado por su contrato | E + S; Catalog. `AssetID` CLOB es identificador wire dentro de contexto, no wallet holding |
| Condition | `ConditionRef{protocol, raw_id}`, CTF bytes32; `QuestionID` separado; oracle/payout refs si conocidos | E + S; Catalog posee identidad/relaciones; Resolution posee observaciones de lifecycle/payout referenciadas, sin writer compartido ni derivación especulativa v2 |
| Market relationship | `RelationshipID` local + revisión, endpoints tipados y tipo: containment, complement, documented NegRisk membership, semantic relation propuesta | S + D; fuente/evidencia, exhaustividad y exclusividad `UNKNOWN/VERIFIED/INVALIDATED`; compartir Event no prueba equivalencia de payouts |
| NegRisk context | Gamma Event, `NegRiskMarketID` contractual bytes32 separado, question indices/bitmasks, CTF/v2, augmented slots, `Other` y revisión de membresía | S; mapping sólo con evidencia; no cast desde Event ID o condition ID |
| Order | `IntentID` local estable + `OrderHash?` venue; cuenta/scope, AssetKey, BUY/SELL, size/price, policy, reserva, revisiones de frame/config; placement, estado REST y envío separados | E + S + O; Account Coordinator |
| Trade / Fill | `VenueTradeID` opaco por servicio; `FillKey=(account_scope, service, trade_id, order_hash, AssetKey)` para el aporte propio de cada orden/asset; IDs de maker/taker y tx/settlement independientes | O + S; reducer de cuenta; varias actualizaciones de un trade no son fills nuevos; entradas repetidas contradictorias de la misma clave quedan en quarantine, no se suman por índice de array |
| Position holding | `(AccountID, AssetKey)`; cantidades settled, matched-pending, reservadas y disponibles por separado; lotes/cost basis y atribución por estrategia | E + S + D; Coordinator; Data v2 es observación, balances chain son hechos por bloque |
| Resolution | `ConditionRef/QuestionID`, reporter, proposal/dispute/finality, payout vector, block/hash/log index, raw status | O + S; Resolution. `end/closed/proposed/resolved/redeemable/redeemed` no colapsan |
| Fee configuration | `RegimeID/revision`, market/asset, campos raw `feesEnabled/base_fee/fd/mbf/tbf`, unidades y parser; curva/calculador aprobado aparte | S; Regimes. maker rebate, taker rebate, reward y builder fee son ledgers/configs distintos |
| Opportunity | `OpportunityID` local determinista por run/delivery/ordinal; estrategia, assets/relaciones, frame vector, assumptions, expiry y candidato de acciones | D inmutable, no orden ni reserva; múltiples revisiones no autorizan duplicación de intent |
| Strategy | `StrategyID` estable, versión de código/config/schema, requisitos, instancia y estado runtime | E + S; registry/runtime; POC-S01 NegRisk y POC-S02 Sports según este proyecto |
| Experiment | `ExperimentID`, revision/parent, hypothesis ID PE-xxx, manifest de datos/modelos, modo/seed, política de evaluación y scorecard | E durante ejecución; manifest y resultado sellados S; Experiment owner |

**Identidad de revisión y dedup — ASTRA-2, FBL-008/010:** `RevisionRef=(owner, namespace, entity_id, generation, revision, schema_version, content_hash)` identifica un snapshot inmutable; contador y generación sobreviven vía persistencia o cambian inequívocamente al reconstruir. `capture_ref=(capture_id, capture_seq, segment_id, offset, checksum)` es provenance, no identidad de fill. `FillKey.service=CLOB` representa al emisor: REST y User WS comparten clave; Data v2 nunca acuña fills privados. Updates de estado guardan su propia observación/versionado y dedup por identidad del hecho, sin sumar cantidad otra vez. Si falta trade ID/order/asset verificable, quarantine, nunca inventar ID con timestamp o índice de transporte.

**Precisión Go propuesta:** tipos nominales distintos para cada ID; bytes32/address validados en sus namespaces. `uint256` se valida con enteros de precisión arbitraria, nunca `float64`. Precios/size/fees se parsean desde el lexema JSON (`json.Number` cuando wire es number) hacia decimal exacto `coefficient + scale`, con operaciones de enteros/racionales acotadas y copias defensivas; no exponer `*big.Int` mutable a consumidores. PnL admite signo; balances on-chain no. Unidades en tipos (`CollateralAmount`, `Shares`, `Price`, `BasisPoints`, `FeeCoefficient`), currency/contract/scale explícitos: pUSD E6 no se llama USDC.e por equivalencia supuesta. Internamente los niveles usan precio decimal normalizado, no tick index que cambie al cambiar el tick.

El boundary de órdenes aplica exactamente P03 §5: verificar grid/decimales de precio, size hacia abajo a dos decimales, amount con la secuencia publicada ceil/floor cuando corresponda, revalidar min-size y convertir a E6 según BUY/SELL. Desbordes, escalas desconocidas, amounts negativos y mapping ambiguo se rechazan. Adoptar salt seguro representable según el contrato documentado de DTO y conservarlo; nunca regenerarlo para ocultar un duplicate. Estadísticas/gráficas pueden usar floats con etiqueta de aproximación; decisiones monetarias y hash de resultados no.

**Tiempo:** conservar string/entero raw y unidad por campo; normalizar a instante UTC y precisión conocida sin inventar nanosegundos de fuente. Receive wall-time + offset monotónico por boot miden tiempos locales; monotónico no se compara entre reinicios. Order timestamp v2 ms, expiration/auth seconds, User WS seconds, Market WS ms y resolution Data v2 según tipo de lookup. Sentinel `69` en proposed price, outcome index `999`, fechas `1970-01-01` y timestamps `0` se preservan raw y normalizan a unknown en su contexto. Ni un cursor ni un timestamp es una secuencia global.

### M1.4 — Discovery, lifecycle y universos

| Etapa | Contrato propuesto | Invalidación / evidencia |
|---|---|---|
| Bootstrap catálogo | Gamma `/events/keyset` y `/markets/keyset`, `after_cursor` opaco, filtros explícitos y páginas capturadas; límite markets conservador ≤100 conforme P08 §21 | Persistir inicio/fin de scan y fingerprint de filtros/cursor. No afirmar snapshot atómico del catálogo |
| Campos de respuesta no expandidos | Usar sólo envelope/fields documentados; si la forma keyset no es suficiente para implementar desde el pack, fallback explícito a `/events` y `/markets` limit/offset de P02 | No inventar envelope keyset. Fallback conserva misma semántica de coverage parcial y validación de integración de U-03 |
| Refresh periódico | Nueva pasada desde primera página con dedup por ID; refrescar por ID markets activos, demandados, con posiciones o con órdenes; separar frecuencia activa/archivada | No borrar entidades porque no aparecieron en una pasada incompleta. Marcar ausencia/coverage y confirmar por lectura individual |
| Nuevos mercados | `new_market` WS es hint temprano hacia Catalog; realizar fetch Gamma/CLOB y validar antes de admitir | No depender de WS como índice exhaustivo; polling recupera altas no observadas |
| Identity join | Parsear arrays Gamma aunque vengan codificados como string; comprobar longitud, índices, unicidad y condición/asset en CLOB | Incompletitud o conflicto → `QUARANTINED`, sin book elegible ni firma |
| Rules/source/relaciones | Guardar cada versión observada de reglas, fuente, naming/Other y membresía; relink mediante IDs con evidencia | Cambio semántico invalida relaciones verificadas y oportunidades pendientes; no reetiquetar retrospectivamente datasets |
| Constraints | Capturar `/book`, `/clob-markets/{condition_id}`, fee lookup, tick lookup y updates WS; ASTRA-2 agrega fee trade-observed con identidad/known-at y alcance limitado al trade (M1.10) | Tick/min-size/fees/status nuevo invalida evaluaciones; discrepancia de fee → REGIME_SUSPECT/refresh, nunca tarifa universal ni “última respuesta gana” |
| Lifecycle | Flags editoriales, CLOB accepting/enabled, resolution observada, payout final y redención se conservan por separado | Cerrado/resuelto/pending deployment/identidad desconocida bloquea nuevos intents; órdenes existentes siguen en conciliación |

`UniverseSpec` es un selector declarativo sobre tags, tipos de mercado, Event/Market IDs, fechas, protocol y relationship requirements. Catalog devuelve `UniverseRevision{members, exclusions_with_reason, coverage, observed_at}` y `UniverseChanged` al runtime. La estrategia puede filtrar elegibilidad semántica sobre esa vista; no pagina Gamma ni maneja subscriptions. El Subscription Planner une/refcuenta las demandas de estrategias, recorder y cuentas; retiene assets con órdenes/posiciones aunque salgan del universo. Un scan incompleto puede servir investigación marcada parcial, pero no probar “no existen oportunidades”.

Sports consume eventos/markets/line/rules, books multiasset y, si declara necesidad, Sports WS con matching de `slug/gameId/team` versionado y verificado; un score sin join verificable no se asigna por similitud de título. NegRisk consume membresía/exhaustividad/Other versionados y protocol context. Ninguno necesita redefinir discovery. RTDS y proveedores futuros entran por `ExternalObservation{source, source_key, event_time, receive_time, payload_version, quality}` y el mismo recorder; el cálculo de fair value/payoff particular permanece en la estrategia.

### M1.5 — Market data, books y cutover sin garantías inventadas

**Unidad de ownership:** un asset pertenece a un solo book shard y a una sola conexión/epoch autora en cada momento. Un reader por conexión conserva orden de frames recibidos; los arrays/mensajes multiasset conservan ordinal interno. La serialización local por asset no prueba orden de generación del exchange. No se mezclan deltas de sockets distintos durante una migración: el nuevo epoch espera snapshot completo y el anterior queda fenced. Heartbeats: Market/User PING cada 10 s; Sports responde al ping del servidor de 5 s dentro del límite documentado de 10 s; RTDS PING 5 s si ese adapter se activa. Son contratos de transporte, no prueba de frescura del book.

| Estado de book | Significado interno | Uso autorizado |
|---|---|---|
| `UNINITIALIZED` | Sin full snapshot de epoch actual | Sólo diagnóstico |
| `SYNCING` | Subscription enviada; esperando `book`, constraints y mapping válidos | Sin oportunidades elegibles |
| `OBSERVED_USABLE` | Snapshot completo y updates admitidos, sin anomalía conocida, requisitos de freshness cubiertos | SCREEN/SHADOW y LIVE sólo con política certificada; calidad **best-effort observada**, nunca garantía lossless |
| `REST_OBSERVATION` | Foto REST independiente sin continuidad WS asociada | Triage/read-only o experimento explícito de snapshots; no baseline para mezclar deltas WS |
| `STALE` | Venció presupuesto de frescura de observación/check, source time o transporte | Bloquea evaluación ejecutable; puede reportar diagnóstico |
| `SUSPECT` | Overflow, regresión temporal significativa, crossed book, schema/ID conflict, control perdido o discrepancia de comprobación | Invalidación inmediata; nueva sincronización requerida |
| `HALTED` | Cierre/estado de mercado incompatible, protocolo no admitido o shutdown | Sin nuevos intents; no elimina posiciones ni cancela hechos de fills |

**Bootstrap normal:** suscribir Market WS con `initial_dump=true` y esperar `book` completo por asset (P05 §9). REST puede obtener constraints y una foto independiente durante ese período. Deltas anteriores al primer `book` se capturan pero no se aplican a una base REST ni se guardan para “replay después”: carecen de frontera comparable. El `book` inaugura el epoch local; sólo los mensajes recibidos después alimentan esa proyección. Timeout de initial book → renovar conexión/suscripción con backoff y permanecer bloqueado. Un book WS posterior sustituye niveles completos y aumenta revisión; no implica sanear incertidumbre de metadata/protocolo.

**REST → WS:** no existe operación de merge certificable entre ambas superficies. La foto REST se mantiene en su namespace; el primer full WS la reemplaza como fuente de continuidad, sin pegar deltas buffered por timestamp. **WS → REST:** tras gap, REST permite observar estado actual o comparar niveles; no reconstruye el intervalo perdido. Para reanudar updates se crea epoch nuevo con snapshot WS. Un modo degradado exclusivamente REST puede producir estudios de snapshots con disclosure, pero no habilita live ni completa un dataset L2. El precio de esta decisión es menor disponibilidad, elegido sobre una sincronización ficticia.

**Aplicación:** `book` reemplaza; `price_change` asigna size absoluto en lado/precio y size cero elimina; `last_trade_price` no muta niveles; BBO extendido no sustituye profundidad; tick change invalida constraints y candidatos, sin reescalar niveles antiguos. Books REST se reordenan canónicamente bids descendentes/asks ascendentes al normalizar (wire REST tiene best al final). Validar precios/rangos/unidades, sizes no negativos, asset/condition, duplicados de nivel, grid y BBO; un book vacío válido no equivale a error, pero no tiene profundidad ejecutable. Hash se conserva opaco, nunca se usa como cadena/checksum probado. No deduplicar mensajes de mercado sólo por timestamp/hash: dos observaciones iguales pueden ser legítimas; un delta size absoluto repetido no suma volumen.

**Orden y comprobaciones:** no ordenar deltas por timestamp de fuente ni retrasar mensajes para inventar una secuencia. El orden de recepción capturado manda para reproducir nuestro estado. Una regresión/dato incompatible se registra y vuelve `SUSPECT`; igualdad de timestamps no permite conocer causalidad. Comprobación REST periódica por sample/universo activo captura intervalo request→response y revisiones WS a ambos extremos; diferencias con tráfico concurrente son `INCONCLUSIVE`, no prueba de corrupción. Coincidencia de niveles/hash aporta evidencia limitada; ni siquiera una coincidencia demuestra ausencia de gaps. Una discrepancia no explicada dispara nueva sincronización, sin parche selectivo de niveles. Conservar métricas de falsos bloqueos para ajustar políticas con evidencia.

**Frame multiasset — ASTRA-2, FBL-008:** corte forward, nunca consulta arbitraria del pasado. El dispatcher único admite la solicitud de corte entre dos despachos, reserva slots en los owners requeridos y fija `C=dispatched_seq` de ese instante (≤ durable_seq); encola `Barrier(cut_id,C,generation)` en cada inbox FIFO antes de cualquier record >C. Alternativamente puede programar un C futuro, pero debe reservar/registrar la barrera antes de despachar >C. La admisión/barreras no compite con acceso libre a punteros latest. Al llegar la barrera, cada owner ya examinó todos sus records ≤C y publica su snapshot, incluso si no mutó desde 900 y C=1000; el dispatcher le certifica el avance por no-ops/watermarks ordenados. Nunca usa `dispatched_seq` global aislado como prueba de que un inbox pendiente fue procesado.

Retener sólo snapshots de cortes admitidos: máximo K por owner y presupuesto total de bytes/config; assets/niveles y tamaño de snapshot también acotados. Sin slot/bytes, barrera que no puede admitirse, deadline, generation inválida o shard que ya pasó C sin snapshot → frame `INELIGIBLE`, nunca latest como sustituto. Al completar/abortar se liberan refs/slots; coalescing puede unir solicitudes del mismo corte. Reserva/timeout de un frame no bloquea capture ni obliga a acumular historia; ante backlog del propio reducer aplica su política de calidad. Corte pasado se reconstruye offline desde checkpoint+journal, fuera de memoria del hot path. La antigüedad, skew, incertidumbre y revisiones de metadata/regime/relaciones viajan en el frame; es coherencia local, **no snapshot simultáneo del venue**. G-05b verifica ausencia de omisiones ≤C y revisiones >C con scheduling adverso.

`DataRequirements` fija máxima edad desde observación/check de book, edad de metadata/fees, clock uncertainty y skew entre assets; silence budget y edad desde último cambio son métricas separadas para no tratar automáticamente un mercado quieto como desconectado. En ausencia de criterio aprobado, live falla cerrado. Antes de emitir intent se revalida el frame y, antes de enviar, la lease de calidad/constraint revision; un cambio lo invalida y exige una nueva evaluación. Ni esto ni la firma limit price garantizan fills múltiples ni cancelan una race posterior al último check.

### M1.6 — Recorder, evidencia durable y replay

**Contrato de captura:** se registra cada frame entrante y respuesta REST relevante antes de publicar su efecto, más solicitudes públicas, subscription/control events, errores, clock samples, config/universe changes, admission/quality transitions y decisiones. Capturar el payload wire disponible con envelope versionado y redacción previa de secretos. **ASTRA-2, FBL-011:** excluir `owner` (API key en wrapper CLOB), `signature`, claves/secret/passphrase, cookies, auth User WS y todos los headers `POLY_*`/HMAC; validación recursiva por schema para payloads/logs/traces/errores, no regex sobre un dump ya persistido. El artefacto exacto firmado sólo existe en store privado cifrado de ejecución futura, nunca raw/log público. Payload sanitizado, identidad/hash y provenance permiten replay sin claves ni firma reutilizable; discrepancias de redacción se ponen en quarantine. Payloads privados de cuenta tienen storage/ACL separados.

| Campo de envelope | Semántica |
|---|---|
| `capture_id`, `boot_id`, `capture_seq` | Identidad única del journal y orden total local asignado por un único admisor; no orden global Polymarket |
| `surface`, `connection_id`, `epoch`, `frame_ordinal`, `request_id` | Fuente, fencing y correlación; una respuesta REST conserva tiempos de inicio/fin de su request |
| `received_wall`, `received_mono_offset`, `source_time_raw`, `source_unit`, `source_time?` | Hora local vs fuente y precisión; source time puede faltar o ser inválido sin reemplazo silencioso |
| `schema_version`, `normalizer_version`, `config_revision`, `content_hash` | Interpretación reproducible y trazabilidad |
| `payload_bytes`, `redaction_policy`, `quality/control_kind` | Evidencia raw permitida o control explícito de pérdida/cambio |
| `segment_id`, `offset`, `length`, `checksum` | Ubicación y detección de escritura parcial/corrupción |

**Formato frozen (OD-2):** journal append-only de records length-prefixed con versión, envelope, bytes y CRC por record; segmentos acotados por bytes/tiempo y footer con rango/count/SHA-256. Un writer secuencial, batch/group commit configurable y `fsync` antes de avanzar `durable_seq`. Segmentos sellados inmutables; rename/manifest y directorio se sincronizan al sellar. Compresión y encadenado entre segmentos quedan IMPLEMENT LATER; al incorporarlos deben preservar identidad lógica y registrar checksum lógico/físico sin cambiar referencias. Checksums detectan corrupción; no prueban que el proveedor envió todo ni protegen contra un administrador malicioso que reescriba toda la cadena de hashes.

**Política por defecto: durable-before-publish — ASTRA-2, FBL-009.** Books y callbacks consumen observaciones hasta `durable_seq`. Dos carriles con colas/count/bytes y cuotas separados alimentan el mismo secuenciador lógico: `EVIDENCE` (mercado/cuenta/control de transporte, capacidad reservada para cuenta) y `RUNTIME` (deliveries/resultados/control experimental). Admission asigna un orden total; los manifests conservan rangos por clase privada/pública aunque el storage esté separado. RUNTIME se limita antes de saturar writer/CPU/I/O: se pausa el run y no se invoca otro callback sin capacidad para su descriptor y resultado acotado. No roba la reserva de EVIDENCE ni revoca epochs por desbordar su propia cola. Group commit y admisión prioritaria mantienen progreso de evidencia dentro del perfil medido; no es garantía frente a fallo físico o código hostil in-process.

Sólo overflow real de EVIDENCE, pérdida de transporte o imposibilidad de capturar evidencia revoca el epoch por señal de seguridad fuera de cola, corta/reconecta y declara discontinuidad. Si no puede persistirse, readiness cae y el boot no cerrado deja intervalo desconocido. No drop-oldest de L2 ni conteo inventado de mensajes perdidos antes de admisión. Resultado/feedback/intent no se publica hasta que descriptor, resultado e inputs efectivos sean durables; la ejecución interna especulativa del callback no es publicación.

**Crash:** escanear último segmento hasta el último record completo y checksum válido, preservar evidencia del sufijo inválido, recuperar manifest y watermarks; nada posterior a la frontera demostrable se considera capturado. Registros físicamente presentes después del último watermark publicado pueden conservarse como evidencia recuperada, pero no se afirma que hayan sido vistos por estrategias. Reinicio abre boot/epoch nuevos, marca intervalo entre última evidencia y nuevos snapshots como discontinuidad y reconcilia cuenta antes de live. Un crash puede perder frames en kernel/cola/no-fsync; el diseño hace esa pérdida visible, no imposible. Un fallo de NVMe/host puede perder todo lo no respaldado fuera de él.

**Productos de replay y auditoría — ASTRA-2, FBL-004, sin conflación:**

1. **Replay de observación:** reconstruye reducers/books a partir de exactamente los records durables seleccionados, incluidos gaps, snapshots y cambios conocidos a cada `capture_seq`. Determinista para el mismo manifest, código, parámetros y seed; no reconstruye cotizaciones que no se capturaron ni valida orden remoto.
2. **Replay de decisiones entregadas:** además usa el journal de `DeliveryFrame{run_id, ordinal, trigger, cut_seq, revision_vector, quality, virtual_time}` y resultados/controles de runtime. Reproduce coalescing, skips y el input exacto de la estrategia. Un delivery sin resultado durable al crash queda `INCOMPLETE`; no se atribuye una decisión o efecto live por reejecutarlo.

3. **Auditoría de decisiones reales:** compara outputs registrados con los inputs efectivos de cada fase, decisión Risk, reserva/intent y attempt; demuestra lo registrado, no efectos no observados. No reenvía ni reejecuta una decisión como mandato real. Hueco de auditoría se conserva como tal.
4. **Simulación contrafactual:** cambia política/modelo/latencia/orden de decisiones sobre datos declarados; tiene manifest/run/namespace nuevos y etiqueta contrafactual. No sustituye el replay ni certifica qué habría hecho el venue.

**Durabilidad de delivery — ASTRA-2, FBL-009:** el scheduler obtiene confirmación de append ordenado del descriptor antes de invocar el callback; group commit puede ocurrir durante el cálculo. Espera durabilidad del descriptor, sus inputs y resultado antes de publicar resultado/feedback, aplicar un fill simulado visible o autorizar intent. No exige fsync individual por callback. Mientras no termine esa frontera, no entrega el siguiente callback que dependa del estado especulativo; fallo implica fencing/reconstrucción de la instancia desde último delivery completo. Descriptor perdido/resultado no durable es `INCOMPLETE`; checkpoint virtual no puede adelantar evidencia durable. SQLite de cuenta/metadata mantiene FULL; simulación puede reconstruirse con checkpoints periódicos en su namespace sin rebajar durabilidad de cuenta real.

El corte C precede al descriptor y no espera procesar el propio delivery. Replay no carga credenciales ni envía; clocks, timers, seed/posición RNG, feedbacks, coalescing y orden canónico se fijan por manifest. Un corte pasado sólo se recupera offline por checkpoint+journal; nunca con latest.

**Inputs completos por fase — ASTRA-2, FBL-004:** `revision_vector` contiene refs verificables (identidad de M1.3, hash y localizador durable) o snapshots serializados, con `known_at`/coverage. Ningún hash sin bytes recuperables satisface el contrato:

| Fase | Dependencias obligatorias adicionales al run/build/params/schema/normalizador |
|---|---|
| Detect / Frame | book y quality por asset/epoch; `universe_rev`, `relationship_rev`, rules/resolution/protocol, `regime_rev` (tick/min-size/fees/delay/incentivos), observaciones externas, config/capability revision, trigger/timer/coalescing, clock/uncertainty, estado de estrategia vía prefijo de deliveries o checkpoint verificado |
| Economics / Evaluate | Frame exacto, Opportunity/ActionCandidate, `account_view_rev` del namespace/modo, `risk_policy_rev`, `liquidity_ledger_rev` y política de replenishment (o NONE explícito en live), `quote_inputs_hash` resoluble con size grid/side/depth/fee inputs, versión de calculadores/fill/cost/payoff models, escenarios y supuestos, Quote/CostEnvelope completo |
| Risk / reserva | Assessment/candidato cuantizado, snapshot exacto de AccountView (balances/inclusión/reservas/obligaciones/atribución), RiskPolicy/caps, basket/policy y residual, calidad/eligibility/lease o permiso simulado, clocks y revisiones revalidadas, competencia/admisión y motivo de decisión |

Coordinator publica AccountView inmutable con revision+hash; Regimes/Risk/Simulator publican sus snapshots bajo el mismo contrato. `EvaluationRecord` y `RiskDecisionRecord` enlazan delivery y vector efectivo propio con outputs (Assessment, sizing, decisión, reason codes). Si Risk o compare-and-check usa una cuenta/constraint posterior a Evaluate, debe registrar ese nuevo input y reevaluación; no atribuirlo al vector antiguo. Intent referencia todos los records durables usados. El manifest pinea sus dependencias completas. Falta de cualquier input efectivo o mismatch de hash → `NOT_REPRODUCIBLE` de esa fase/decisión; jamás usar estado actual ni reconstruir a partir del output deseado. Una fuente posterior puede servir auditoría como evidencia nueva, no alterar lo conocido por la decisión original.

**Manifest de experimento:** hashes/rangos de segmentos, coverage por stream/asset/epoch, holes, checkpoints, revisiones metadata/rules/fees/relationships y su disponibilidad temporal, normalizador, estrategia/binario/Go toolchain/dependencies, parámetros, seed, clocks, fill/cost/risk models, delivery policy, sample split y política de censura. Inputs posteriores al cutoff nunca rellenan retroactivamente metadata “conocida”. Dataset parcial permanece parcial; un estudio que cruza una discontinuidad termina ese episodio o lo etiqueta no evaluable según regla ex ante. Cada exclusión se cuenta en denominadores para evitar selección de sólo episodios limpios rentables.

### M1.7 — Persistencia, datasets, retención y recuperación

| Store propuesto | Qué guarda / owner | Garantía, índices y límites |
|---|---|---|
| SQLite embebido, WAL, synchronous FULL | Metadata versionada, registry/manifests, órdenes/intents/reservas/fills/ledger y checkpoints, vía owners | Transacción ACID local; writer serial con transacciones breves. Índices ID/protocol/account/status/event y known-at; raw stream no se inserta fila por fila aquí |
| Capture journal segmentado | Raw sanitizado y eventos de control/delivery; Capture | Append secuencial durable; índice reconstruible `(surface, asset/condition, receive-range, seq-range)→segment/offset`; el índice no es autoridad |
| Tablas privadas de ejecución en el mismo SQLite | Payload preparado, order hash, intent, attempt y referencia de auth profile **sin credenciales**; Coordinator | Mismo boundary transaccional de cuenta, no otra DB. Artefacto firmado exacto sólo en implementación live futura, cifrado y durable antes del intento; fuera de la evidencia permanente OD-3. Headers HMAC/owner API key no se persisten; wrapper autenticado se completa desde Credentials. Clave de cifrado externa a DB/backups |
| Datasets derivados SQLite/JSONL; Parquet diferido | Datasets normalizados/episodios/metrics/scorecards, derivados de manifests | Lineage/schema version y dinero decimal/int exacto desde el inicio. Parquet posterior conserva ese contrato y particiona por dataset/date/surface/rangos sin exigir cambio de dominio |
| In-memory | Books, snapshots, caches, colas y runtimes | Reconstruibles; nunca única prueba de intent enviado, fill o saldo disponible |

**Justificación y reversibilidad:** SQLite evita servidor/operación adicional y permite atomicidad de cuenta en un host. El writer único puede convertirse en límite; analytics pesado no lee la base operacional durante transacciones críticas. PostgreSQL sería alternativa si profiling muestra contención, múltiples writers inevitables o consultas operativas incompatibles; no está descartado para siempre. Repositorios por owner y schemas de exportación lógicos aíslan el motor; una migración requerirá reconciliación y prueba de equivalencia, nunca doble escritura live sin diseño. Schemas de datasets y journal versionado permiten añadir Parquet/cambiar motor analítico sin alterar el dominio. La elección concreta de driver Go, librería decimal y versiones corresponde a M2 bajo estos contratos; Parquet no es una dependencia de M2–M4 ni abre investigación de protocolo.

**Consistencia entre journal y DB — ASTRA-2, FBL-003/010:** no hay transacción atómica filesystem+SQLite. Para observaciones externas, Capture hace durable el record antes de aplicar su efecto (no exige sellar el segmento por cada record). Cada reducer/owner confirma proyección y `applied_seq{capture_id, reducer_id, reducer_version, namespace}` en la misma transacción; ningún owner adelanta el cursor de otro. El dispatcher entrega watermarks ordenados para demostrar hasta dónde se examinaron records sin mutación relevante. Reprocesar desde el cursor propio, con identidad estable y dedup; un cambio de reducer exige reconstrucción/versionado, no reutilizar un cursor incompatible. Segmentos durables huérfanos se verifican e indexan.

Las decisiones locales de cuenta nacen en DB: reserva+intent+evento outbox en una transacción. La outbox durable conserva el hecho hasta exportación/verificación por `event_id`; no requiere una referencia circular a un journal aún inexistente. Nadie envía desde la outbox genérica. Sólo Execution puede reclamar una autorización vigente del Coordinator. Integridad se reporta por clase y rango, no como un único PASS que oculte evidencia ausente.

| Clase / frontera | Evidencia requerida y recuperación | GC / resultado si falta |
|---|---|---|
| `ACCOUNT_FACT` | Intents, attempts, decisiones de reserva, fills/updates, observaciones privadas de órdenes/balances/chain, reconciliación/recovery, atribución y correcciones; payload sanitizado y provenance suficiente para rehacer reducers, no sólo hashes. DB/outbox y journal privado tienen autoridad según origen del hecho | OD-3 APPROVED: retención durante la vida del proyecto, fuera del GC de mercado. ACL mínima y cifrado cuando corresponda; sin claves privadas, HMAC secrets ni secretos reutilizables. Falta requerida → `ACCOUNT_INTEGRITY_FAILED / RECOVER_FROM_VENUE`, cuenta bloqueada para nueva exposición; conservar reservas y evidencia recuperable |
| `RESEARCH_EVIDENCE` | Mercado, metadata, inputs de decisiones, deliveries y modelos; referencias resolubles por hash y versión o snapshots completos | Falta → runs/deliveries dependientes `NOT_REPRODUCIBLE`, integridad de ese conjunto `FAIL/MISSING`; no bloquear health/read-only ni cuenta independiente sana. Si también prueba un hecho de cuenta, rige la clase más fuerte |
| Segmento activo | Prefijo durable con records/CRC y watermark; sólo esta frontera es recuperable por crash local | Nunca GC ni backup por copia parcial sin frontera verificable; bytes RAM/kernel/no-fsync no son evidencia garantizada |
| Segmento sellado | Rango/count/checksum y manifest durable, inmutable; compresión y encadenado posterior conservan identidad lógica | Sólo candidato a GC después de demostrar ausencia de dependencias requeridas; no confundir checksum con completitud del venue |
| Snapshot / checkpoint | SQLite backup consistente incluye WAL por API del motor, outbox pendiente, versiones y vector de cursores; snapshots de reducers son derivados verificables | No reemplaza raw privado requerido. El snapshot aislado no es un punto de backup consistente |

**Frontera recuperada:** pérdida de evidencia privada puede permitir reconstruir estado actual mediante venue/chain, pero la cuenta permanece degradada hasta reconciliación documentada de scopes, órdenes, fills, obligaciones e inventario. Si no se reconstruye la historia necesaria, queda `UNRESOLVED` y su integridad histórica no recibe PASS. La disponibilidad read-only no prueba integridad de cuenta; la ausencia de evidencia de research nunca se disfraza como reproducción exitosa.

**Retención frozen — ASTRA-3 / OD-3 APPROVED:** `ACCOUNT_FACT` y la evidencia privada mínima necesaria para reconstrucción, auditoría, reconciliación y recovery se conservan durante la vida del proyecto. ACL mínima, cifrado según sensibilidad del diseño y ausencia de claves privadas, HMAC secrets, identificadores de credencial y secretos reutilizables. La evidencia permanente conserva campos sanitizados, identidades/hashes y lineage; el artefacto firmado operativo futuro de M1.11 tiene custodia separada y no se incorpora como firma reutilizable a esta evidencia. Archivar/compactar debe conservar semántica, provenance y dependencias resolubles; eliminar exige una política explícita de cierre/archivo del proyecto, nunca TTL accidental.

Raw de mercado y derivados mantienen políticas separadas: 30/90 días no pineados son propuestas operacionales, no cifras aprobadas por OD-3 ni requisitos de borrado de M4. Manifests/scorecards/config/rules se conservan durante la vida del proyecto. Inputs necesarios para decisiones auditables y experimentos revisados quedan pineados, incluyendo snapshots account/risk/liquidity y quotes; si prueban un hecho de cuenta heredan ACCOUNT_FACT. Un segmento mixto hereda la retención más fuerte; separación física privada evita que GC público arrastre cuenta. No hay GC automático inicial.

GC opera sólo sobre segmentos sellados, con comprobación transaccional de pins/dependencias y tombstone durable de rangos/hashes retirados. Referencias históricas a datos voluntariamente expirados se marcan `EXPIRED/NOT_REPRODUCIBLE`, no se tratan como refs recuperables; refs requeridas nunca expiran automáticamente. Tener una copia externa no autoriza borrar la única copia resoluble por el manifest: registrar y verificar su nueva ubicación. En FOUNDATIONAL NOW se implementan clases, pins/manifest y validación de retención; no hay borrado automático. GC automatizado y compresión quedan diferidos. Capacidad se calcula con bytes/s medidos, ventanas y overhead; presión de disco pausa research, nunca elimina evidencia privada/pineada.

**Disco:** budgets separados para raw, DB, derivados y reserva operacional. Low-watermark frena replay/export y nuevas suscripciones; critical-watermark bloquea oportunidades/nuevos sends, mantiene reconciliación/cancel mientras sea posible y alerta. No borrar raw pineado para sostener live ni llenar el volumen hasta que SQLite falle. Tamaño/tiempo de segmento, batch fsync, headroom y retention son configuración validada y capturada.

**Migraciones:** schema version y compatibilidad explícitos, backup previo y writer detenido; transacción cuando sea posible. App antigua rechaza schema futuro; rollback restaura sólo bajo reconcile, porque restaurar DB vieja no deshace órdenes externas. Raw nunca se reescribe por migración; nuevo normalizador genera dataset nuevo.

**Punto consistente de backup — ASTRA-2/3, FBL-003:** el Supervisor coordina una barrera de writers/reducers; Capture fija el corte durable `B` y sella sus prefijos activos de todas las clases, mientras cada owner drena efectos hasta él y conserva sus cursores DB sin avanzar más allá de `B` hasta fijar la vista del snapshot SQLite. Supervisor no muta proyecciones ni cursores ajenos. Captura posterior puede continuar en segmentos nuevos; no se incorpora al snapshot anterior. Capture posee el manifest/bundle de backup e incorpora el snapshot por API del motor, outbox todavía no exportada, todos los segmentos/dependencias requeridos por sus cursores y pins, manifests y referencias de claves. Un simple «sellar y después copiar DB mientras sigue avanzando» no cumple. Manifest registra `B`, rangos/hash por clase, `applied_seq` por reducer/namespace, versiones y IDs outbox; debe demostrar cobertura de dependencias, además de `journal_seq ≥ applied_seq`. Capture publica `BACKUP_COMPLETE` sólo tras verificar todos los componentes; un bundle interrumpido queda incompleto.

**Restore local exigido para M4:** producir un bundle consistente sin capital real, restaurarlo en directorio limpio del host, verificar hashes, referencias, outbox/cursors por owner, reconstruir proyecciones y comparar hashes/ledger. Medir duración y frontera de pérdida observada del fixture, sin adjudicarle un SLA de DR. Probar además crash/truncamiento del activo y bundle que perdió evidencia requerida: este último debe degradar, no PASS. Cuenta simulada/fault fixtures bastan; adapters live ausentes. G-06b/G-14 son fundamentales y no se postergan con F.7.

**Fuera del host diferido:** copia cifrada a destino independiente, custodia/recuperación de claves, pérdida total del host y RPO/RTO bajo presupuesto owner requieren G-14b posterior, separado de crash y restore local. Cadencia horaria/copia al sello/verificación diaria son propuestas operacionales. Antes de nuevo lease en host restaurado se debe cercar la instancia antigua y reconciliar todos los scopes; rotación/revocación L2 es parte de esa operación, no prueba por sí sola que murió el host previo, canceló órdenes o revocó permisos on-chain. Si no puede demostrarse exclusividad, live sigue bloqueado. No se declara disaster recovery certificado con tests locales.

### M1.8 — Contrato Go de estrategia y modos

Interfaces **de diseño**, deliberadamente sin implementación. El engine entrega todos los servicios comunes; la estrategia calcula elegibilidad, detecta oportunidades y evalúa su lógica particular. No recibe conexiones, repositorios, signer, wallet ni un callback de envío.

```go
type Strategy interface {
    Describe() Descriptor
    Universe() UniverseSpec
    RequiredData() DataRequirements
    Start(context.Context, RunContext) error
    Detect(context.Context, Frame) ([]Opportunity, error)
    Evaluate(context.Context, Opportunity, EvaluationContext) (Assessment, error)
    Observe(context.Context, Feedback) error
    Stop(context.Context, StopReason) error
}

type Factory interface {
    New(Parameters) (Strategy, error)
}

// Contratos conceptuales: todos los valores entregados son inmutables.
// RunContext: run/strategy IDs, versions, virtual clock, seeded RNG,
//             parameters, declared metric sink; sin acceso a red/secretos.
// Frame: delivery ordinal + cut seq + UniverseRevision + BookSnapshots +
//        RegimeSnapshots + RelationshipSnapshots + ExternalObservations + quality.
// EvaluationContext: mismo frame + DepthQuote/CostEnvelope + AccountView
//                    del modo + RiskPolicyView; nunca objetos mutables.
// Assessment: ACCEPT | REJECT | INCONCLUSIVE, reason codes, differentiated
//             metrics, bounded ActionCandidate y supuestos explícitos.
// Feedback: UniverseChanged | QualityChanged | EvaluationResult |
//           SimulatedExecution | LiveExecution | Timer | StopRequested.
```

`Descriptor` exige ID, versión de código/schema, hipótesis asociada, descripción de mecanismo y metric definitions. `UniverseSpec` y `DataRequirements` se validan antes de arrancar; una estrategia que requiere dato no disponible queda `WAITING_DATA/UNSUPPORTED`, no recibe campos cero sustitutos. `Start` se ejecuta una vez por instancia; `Observe(UniverseChanged)` permite incorporar/excluir miembros antes de `Detect` sobre esa revisión. `Detect` sólo produce candidatos no vinculantes; Economics construye cotizaciones y costes comunes; `Evaluate` aplica factibilidad/modelo particular sobre el mismo frame. Risk siempre revisa el resultado después. `Observe` recibe resultados posteriores sin convertirlos en prueba de fill si son simulados. `Stop` es idempotente desde la perspectiva del runtime y no coloca ni cancela órdenes.

`ActionCandidate` contiene una o varias legs tipadas de asset, side, limit/size o presupuesto, prioridad, vigencia y, si es multi-leg, `BasketPolicy` versionada de M1.11. Sin política válida se rechaza antes de reservar. Para posiciones sólo referencia capability e inputs tipados, nunca dirección/calldata arbitrarios. Economics retorna quantities cuantizadas y coste por escenario. La estrategia aporta payoff/model outputs auditables y restricciones de parcialidad/residual; no secuencia órdenes, autoriza compensaciones ni implementa recovery. Bounds de oportunidades/legs/payloads impiden resultados ilimitados. `EvaluationContext` y feedback usan las refs completas de M1.6; cualquier input efectivo nuevo debe incorporarse al contrato de evidencia antes de usarse.

| Modo | Fuente / misma lógica Strategy | Destino y permiso |
|---|---|---|
| `SCREEN` | Datos actuales o dataset declarado, universe/Detect/Evaluate idénticos | Reporta candidatos/costes; no abre orden real ni simulada por defecto; no secrets |
| `REPLAY` | Manifest cerrado, reloj virtual, mismos reducers y estrategia | Simulator bajo optimistic/base/stress; cuenta virtual y resultados reproducibles; red bloqueada |
| `SHADOW` | Datos actuales capturados, reloj de delivery y misma estrategia | Simulator con órdenes/fills sintéticos; cuenta y liquidez virtual aisladas por experimento/instancia por defecto; `PORTFOLIO_SHARED` sólo explícito en manifest; cero envío venue |
| `LIVE` | Datos actuales y feedback de cuenta real | ExecutionMode comienza `LIVE_DISABLED`; sólo un lease central certificado habilita el gateway real; no estrategia “live especial” |

Factory crea instancias aisladas por experimento; no hot-load de plugins Go ni swaps de código sobre órdenes abiertas. Cada instancia procesa un callback a la vez. Estado propio sólo en su actor; reinicio conservador crea instancia nueva desde manifest y replay de inputs, o checkpoint versionado validado contra replay. No se promete que un checkpoint arbitrario escrito por la POC sea confiable. Para reproducibilidad no usar I/O, reloj global, goroutines propias, random global ni iteración de maps sin orden dentro de callbacks; se verifica en revisión/fixtures y comparación de replay.

**Errores y aislamiento realista — OD-1 APPROVED:** error tipado distingue `NO_SIGNAL`, `INSUFFICIENT_DATA`, `INVALID_MODEL`, `TRANSIENT_INPUT` y fallo de software. Panic recuperable en callback → instancia `FAILED`, retiro de sus candidatos y política de cancel de sus remanentes a través del Coordinator; no se recupera balance inventándolo. Deadline cancela contexto; resultado tardío se descarta mediante run generation. **Go en un proceso no ofrece sandbox de memoria, bloqueo de syscalls ni kill seguro de goroutine**: sólo se admite código confiable revisado, sin plugins arbitrarios ni código no confiable. Si un callback ignora cancelación, no se inicia otro callback/instancia que acumule goroutines; se cerca la instancia, se revoca live y se reinicia el proceso de forma controlada si no drena. Imports/lint/API restringida/ausencia de secrets son defense-in-depth; no constituyen sandbox. Aislamiento por proceso sería una evolución futura, no requisito del MVP; Credentials/Signing conserva su puerto externalizable sin cambiar dominio ni Strategy API.

### M1.9 — Hypotheses, experimentos y simulación

Registry guarda `PE-xxx`, mecanismo, evidencia pro/contra, required data, universo/exclusiones, capacidad/lock/latency, experimento mínimo y parent revision. No convierte las 30 familias del ERC en 30 módulos. Cheap triage consulta catálogo/datos disponibles y cotización de costes antes de activar captura amplia: `NO_DATA` es bloqueo/inconclusión, `NO_SIGNAL` es evidencia sólo si coverage suficiente y `BAD_ECONOMICS` requiere modelo/coste explícitos.

| Artefacto lógico dentro del framework | Contenido mínimo |
|---|---|
| Protocol de experimento | Hipótesis falsable, estimando/unidad estadística, baseline/negative controls, exclusiones, stopping rule, sample requirement, GO/ITERATE/NO_GO ex ante |
| Run manifest | M1.6 + versiones parámetros/calculadores, universo conocido-a-fecha, escenarios, estado de datos, gastos de cómputo/humanos, bankroll virtual |
| Scorecard | Cobertura y discontinuidades; señales totales/independientes; lifetime; net edge por depth/fee/latency; fill/partial/legging rates; capacity; PnL bruto/neto/realizado/no realizado; lock/capital-turns; drawdown y worst loss; markouts/adverse selection; sensitivity y caveats |
| Statistical view | Separar calibración Brier/log-loss, retorno de regla y ponderación de flujo. Splits temporales y por parent event, OOS, censura por mercados sin resolver y múltiples tests declarados; no holdout reciclado sin nueva revisión |
| Outcome | `GO` al siguiente gate, no permiso live; `ITERATE` con cambio falsable; `NO_GO` con evidencia suficiente; `INCONCLUSIVE` cuando datos/modelo/sistema impiden concluir |

**Fill engine común:** órdenes virtuales con submit-time, delay, limit/policy, remanente, cancel-latency y fill events. BUY barre asks y SELL bids al tiempo simulado de llegada, integra niveles para VWAP y rechaza cantidad no cubierta; FOK exige total y FAK admite parcial. En snapshots discretos no se interpola liquidez no observada. Un book agregado no revela FIFO, prioridad individual ni nuestra queue: resting/touch no es fill probado. Last trade y BBO no bastan para asignar todos los fills. El modelo maker estima/boundea queue y fill usando evidencia disponible y declara su incertidumbre; no certifica price-time priority.

| Escenario | Liquidez/latencia/fills | Interpretación |
|---|---|---|
| Optimistic | Profundidad observada disponible, latencia baja parametrizada, queue favorable bajo evidencia mínima declarada | Cota exploratoria, nunca evidencia suficiente de promoción |
| Base | Delays/latencia medidos o supuestos explícitos, haircut de profundidad y queue conservadora calibrable, partials y cancel races | Resultado candidato sujeto a sensibilidad; si faltan datos de calibración se etiqueta `UNCALIBRATED` |
| Stress | Mayor delay, reducción de depth, adverse selection, patas incompletas, fallo de cancel, settlement/dispute lock prolongado y costes altos | Riesgo residual y fragilidad; magnitudes preregistradas por experimento, no constantes universales |

**Aislamiento experimental — ASTRA-2, FBL-005:** modo default `INDEPENDENT`: cuenta/reservas/inventario y ledger de liquidez virtual por `(ExperimentID, RunID, instance, scenario)`, con saldo inicial y modelos en manifest. POCs independientes pueden evaluar la misma profundidad cada una en su contrafactual; nunca reciben rechazo por consumo virtual accidental de otro run. Cada namespace impide doble consumo propio por asset/lado/precio/RevisionRef. En `PORTFOLIO_SHARED`, cuenta y liquidez pertenecen a un `PortfolioRunID` explícito, con participantes/versiones/asignaciones, orden determinista de admisión, seed y policy de competencia preregistrados. Cambiar participantes crea manifest nuevo; no afecta runs independientes.

Scorecard compartido atribuye por oportunidad y peer `PEER_CONSUMED_DEPTH`, `PEER_RESERVED_CAPITAL` y otros límites compartidos, conservando denominadores y baseline aislado. Esa competencia puede evaluar un portfolio, pero no convertir por sí sola una POC independiente en `NO_GO`. Revisiones de cuenta/liquidez y cada consumo se capturan para replay completo. Replenishment conservador se versiona: updates posteriores no prueban reposición causada por nosotros. Fills simulados, órdenes observadas y settlement real se etiquetan inequívocamente; impacto/reacción contrafactual del mercado siguen siendo límites del modelo.

Baskets son multi-leg no atómicos: Simulator alimenta el mismo reducer `BasketExecution`/`BasketPolicy` de M1.11 con latencia/partials/cancel/UNKNOWN sintéticos; drawdown y lock intermedios forman parte del scorecard. No implementa una segunda política de secuenciación por POC. Si la tesis exige conversión deshabilitada o atomicidad no disponible, queda `CONDITIONAL_UNEXECUTABLE`; puede falsarse económicamente, pero no obtener GO live. El payoff específico sigue en Sports/NegRisk. `GO` depende de datos/modelos aptos y criterios del experimento, no de un umbral universal inventado.

### M1.10 — Economics, capital y risk compartidos

**Cost quote común:** `Quote{frame_id, size_grid, executable_depth, VWAP, worst_price, platform_fee_interval, expected_incentives, slippage_scenarios, cash_required, token_required, capital_lock, validity, assumptions}`. Una cotización no reserva el book ni garantiza que siga disponible. BUY consume collateral+costes; SELL requiere tokens disponibles; no asumir short sintético mediante saldo negativo. Para baskets valorar todos los estados declarados, los fills parciales y costes de liquidación; la desigualdad de precios sólo establece un candidato matemático bajo sus supuestos.

**Fees dinámicas:** conservar `feesEnabled`, `base_fee` bps, `fd.r/e/to`, `mbf/tbf`, category source y fecha como inputs distintos; un `FeeResolver` versionado selecciona sólo una fórmula con evidencia aplicable al mercado. La fórmula publicada `shares × feeRate × p × (1-p)` no autoriza sustituir `feeRate=base_fee/10000`. Rounding de cinco decimales/mínimo y empate no definido producen intervalo de coste o estado `UNRESOLVED`; no elegir silenciosamente un desempate como contrato. Múltiples fills pueden tener costes/rounding diferentes; estimar por fill/escenario y reconciliar fee efectiva. Donde no exista cota superior defendible, no sizing live. En SCREEN/SHADOW puede mostrarse sensibilidad con supuestos nombrados, pero no “net edge certificado”. Datos actuales jamás se aplican por defecto a toda la historia.

**Fee observada — ASTRA-2, FBL-012:** Regimes ingiere `fee_rate_bps` de `last_trade_price` y trades privados con identidad/provenance, asset, precio/size/rol si disponibles, raw source time/unidad propia y `known_at=capture_seq`. Es evidencia del trade observado; en Market WS sin trade ID no inventa uno ni enlaza sólo por timestamp/tx. Dedup privado usa FillKey; observaciones públicas repetidas no se suman como fee de cuenta. Discrepancia contra el modelo marca `REGIME_SUSPECT`, invalida quotes afectados, solicita refresh y etiqueta `fee_regime_uncertain_interval`; no prueba por sí sola un cambio universal de tarifa. Sólo revalorar ese trade cuando mapping de unidades/fórmula/rol esté verificado; el bps solo no es necesariamente importe pagado. Para otros trades/simulaciones usar régimen aplicable conocido en ese instante o intervalo/sensibilidad explícitos; sin cota, `INCONCLUSIVE` y live bloqueado. No usar «último fee observado ≤t» como ley para el siguiente trade ni backfill retroactivo de decisiones con datos conocidos después. Contrafactual con otra hipótesis de fee requiere manifest nuevo.

**Incentivos:** separar fee pagada, maker rebate devengado estimado, taker rebate/tier estimado, liquidity reward esperado y pago observado en cuatro ledgers/modelos. La estimación no es cash disponible ni reduce el coste necesario para financiar una orden. Base risk no cuenta rewards futuros; scorecard muestra neto sin incentivos, con estimación y realizado tras pago. Eligibility instantánea/scoring, categoría y tamaño del pool no son entitlement final. Builder cero implica sin atribución opcional; jamás habilitar fees Builder mediante Opportunity.

**Ledger de cuenta:** saldo collateral confirmado observado por bloque, obligaciones matched-pending, inventario por asset, reservas por intent/remanente, fees buffer y capital inmovilizado. `available` deriva una sola vez dentro del Coordinator: fondos confirmados utilizables menos reservas/obligaciones que todavía no estén reflejadas en ese balance. Cada obligación conserva qué snapshot/block la incluye; un fill no se descuenta dos veces al llegar chain y no se libera antes de confirmación. Para SELL, tokens reservados y pending-sold reducen disponibles. Discrepancia o incertidumbre de inclusión reduce disponibilidad conservadoramente y congela incrementos de exposición. Proceeds pendientes no financian nuevas órdenes por defecto.

**Atribución — ASTRA-2, FBL-010:** inventario de cuenta `(AccountID, AssetKey)` se concilia con chain; subledger `(AccountID, StrategyInstanceID, AssetKey)` asigna lotes/obligaciones/reservas sin crear tokens. Suma de atribuciones más `UNATTRIBUTED` debe igualar inventario de cuenta en cada categoría contable. SELL exige disponibilidad tanto de cuenta como de la estrategia; B no vende los tokens de A por compartir wallet. Transferencia entre estrategias es asiento explícito autorizado del Coordinator, doble entrada con ID idempotente, cantidades, motivo y revisiones; nunca reclasificación tácita. Fills heredados conservan atribución del intent, y fondos externos desconocidos permanecen no gastables hasta clasificación. Replay y reinicio preservan estas identidades, correcciones y ecuaciones.

| Control | Evaluación / condición de bloqueo |
|---|---|
| Eligibility | Capability, cuenta/scope, protocol, restricciones, fresh frame/fees/rules, markets operables, datos y ledger sanos; cualquier unknown requerido rechaza |
| Sizing | Cantidad mínima entre límites de presupuesto, inventario, profundidad y pérdida aprobada; cuantizar y revalidar economics/min-size después del rounding |
| Reserva | Transacción única de reserva + IntentID + versión de risk/account + outbox; compare-and-check de revisión evita que dos estrategias gasten el mismo saldo |
| Bankroll | US$300 es techo total tiny-live previsto, no asignación automática ni cash garantizado; estrategias reales compiten por ese bankroll. Cuenta virtual aislada por default; compartir en simulación exige `PORTFOLIO_SHARED` |
| Exposición | Caps globales, por cuenta, estrategia, mercado, Event/relationship group, posiciones abiertas y número de órdenes; contar pending/UNKNOWN como exposición posible |
| Concentración | Agrupar eventos relacionados/correlacionados con evidencia; no asumir independencia por distinto MarketID/EventID. Si no hay modelo, sumar pérdidas conservadoras |
| Baskets | Coordinator reserva coste/exposición de conjunto y parciales factibles antes de primera leg; Risk valida `BasketPolicy`/residual por transición (M1.11). No netear payouts sin relación vigente ni habilitar unwind por flag |
| Reutilización de capital | Liberar sólo por cancel/remanente conciliado, fill settled, venta/merge/redeem confirmado o rechazo inequívoco; `market_resolved` no devuelve cash |
| Kill / breach | Latch global o scoped revoca nuevos sends, inicia cancel remanente y reconciliation, alerta; no coloca una liquidación agresiva automática salvo mandato y política específicos |

Límites monetarios, worst-loss/lock máximo, tolerancias live de fee/data y reparto de bankroll quedan `DEFERRED_LIVE_DECISION`; deben derivarse de shadow/stress. Ausencia de configuración válida mantiene live cerrado y no bloquea M2–M4; simulaciones declaran sus parámetros en el manifest sin aprobar números live. La aprobación de un candidato es efímera y ligada a input revisions: no se reutiliza al cambiar precio, fee, book, account o config. Competencia entre estrategias se resuelve por política registrada y orden de admisión determinista, no por velocidad accidental de goroutines; reportar rechazados por capital para no confundirlos con ausencia de señal.

### M1.11 — Execution, reconciliation y crash con órdenes abiertas

**Boundary de identidad:** `AccountProfile` versionado une chain 137, wallet type, maker/funder, EOA autorizada, signer del Order, credencial L2/scope y ruta de contratos. Tipo 3 Deposit usa maker/signer de contrato y EOA externa para TypedDataSign/ERC-7739; no tratarlo como EOA tipo 0. Tipos 0/1/2/3 se modelan, pero live sólo certifica el perfil realmente elegido. L1 ClobAuth, L2 HMAC, Order EIP-712 y allowances son permisos separados (P03 §4, P04 §7). Ningún helper puede auto-crear wallet, aprobar spenders ni desplegar por side effect de startup.

```text
Opportunity → Evaluation → Risk decision
    → atomic [reserve + PREPARED intent + payload identity]
    → construct/validate/sign exact order + persist protected payload/hash
    → durable SEND_ATTEMPT_STARTED (one attempt token)
    → single HTTP write
       ├─ definitive reject → record → release only unused reservation
       ├─ accepted evidence → order tracking + trade reconciliation
       └─ timeout/contradiction/crash → UNKNOWN → reconcile, never auto-new-salt

User WS / REST / chain observations → dedup + evidence reducer
    → order remaining + fills pending/settled + reservation/position update
    → reconciliation case closed only when invariants and sources agree
```

**Construcción:** separar objetos `SignedOrderFields`, `OrderDTO` y `SubmissionPolicy`; sólo los once campos de P04 §7A entran al Order EIP-712 CLOB v2. `expiration/orderType/postOnly/deferExec/owner` pertenecen al transporte/política según contrato, no a la firma Order. `owner` es API key, no dirección de wallet. DTO BUY/SELL y signed side uint8 se validan en correspondencia. Serialization exacta del body se prepara una sola vez por intento y los mismos bytes alimentan HMAC y HTTP. Secret se decodifica base64 para HMAC, URL path sin query, timestamp seconds, firma URL-safe con padding conforme P03; no copiar headers del raw journal. Cualquier discrepancia firma/DTO/hash/perfil detiene envío.

**Estados internos en ejes distintos — ASTRA-2, FBL-001/002/010:** intent `PREPARED/SEND_ATTEMPT_STARTED/VOID/UNKNOWN/REJECTED/ACK_OBSERVED`; orden `OPEN/PARTIAL/TERMINAL/UNKNOWN` con estado remoto raw; ejecución `NONE_PROVEN/EXECUTION_PROVEN/UNDETERMINED`; settlement por trade `MATCHED/MINED/CONFIRMED/RETRYING/FAILED/UNKNOWN`; reserva `HELD/PARTIALLY_CONSUMED/RELEASABLE/RELEASED`; caso operacional `RECONCILING/HUMAN_REVIEW_REQUIRED/CLOSED`. `NONE_PROVEN` sólo existe bajo prueba positiva de no ejecución; ausencia de trades es `UNDETERMINED`. Cancel/remanente terminal puede coexistir con fills pendientes. Mantener variantes `TRADE_STATUS_*` y enums cortos como mappings explícitos versionados. Contradicción relevante abre caso y congela exposición; no borrar evidencia anterior ni ordenar por último timestamp.

| Transición / evidencia suficiente | Efecto permitido del Coordinator | Lo que no demuestra |
|---|---|---|
| `PREPARED` sin attempt iniciado en store íntegro al recuperar | Atómicamente `VOID`, payload permanentemente no enviable y reserva no consumida `RELEASABLE`; revocar tokens/boot previos | Una ausencia de marker en backup incompleto no prueba que no hubo send |
| Rechazo inequívoco de la operación exacta, semántica de no aceptación verificada y sin hechos contradictorios | `REJECTED`, `NONE_PROVEN`, liberar sólo reserva sin otra obligación | Error genérico, HTTP status o JSON parseable no prueban rechazo |
| ACK válido o lookup positivo de la identidad preparada | `ACK_OBSERVED`, tracking del remanente; conservar cobertura de exposición | Aceptación no prueba fill ni settlement |
| Trade propio identificado, incluidos mensajes tardíos | `EXECUTION_PROVEN`; dedup/atribuir cantidad y pasar reserva a obligación sin crear disponible intermedio | Match no es saldo confirmado; status update no es nuevo fill |
| Cancel/expiry terminal demostrado y total ejecutado conciliado con trades | `REMAINDER_RECONCILED`; liberar únicamente remanente no ejecutado cuya imposibilidad de match posterior está probada | Un `canceled` aislado o último `size_matched` local no prueba total histórico final |
| Transporte/timeout/respuesta ambigua, datos incompletos o contradictorios | `UNKNOWN`, reserva y exposición posible retenidas, caso `RECONCILING`; bloquear incremento en cuenta afectada | Tiempo, balance igual o ausencia REST no convierten el caso en no ejecutado |
| Budget temporal/intentos de lectura agotado o cobertura no demostrable | Mantener `UNKNOWN`, caso `HUMAN_REVIEW_REQUIRED`, alerta y nueva exposición congelada; lecturas/cancel conocidas siguen permitidas | Escalación humana no es terminalidad contable ni autorización para liberar por conveniencia |

**Convergencia operacional:** Reconciler consulta por hash, scopes/órdenes y trades paginados con overlap, sigue fills/receipts y registra cada intento/cobertura. Jobs tienen backoff y budget finito; al agotarlo el caso se entrega a revisión humana, sin polling intensivo infinito. Una observación positiva posterior puede resolver el estado aunque el caso haya escalado. El operador puede aportar evidencia verificable, conciliar correcciones explícitas o mantener la cuenta deshabilitada; no declarar «no ejecutado» por aceptación verbal del riesgo. `reconcile_deadline`, `settlement_window` como horizonte de observación, alertas y máximo de casos son políticas futuras de live (U-06), no condiciones de liberación. La máquina queda definida sin valores financieros hoy.

**Contraejemplo a la terminalización propuesta en FABLE:** después de un match cuyo settlement sigue pendiente, balances confirmados aún iguales y orden ya expirada/ausente pueden coexistir con trade todavía no visible; P04 §8.1–8.3 y P05 §9.3 separan matching/settlement y no garantizan exhaustividad/replay. Por tanto expiry + ausencia REST + balances iguales, aun con overlap y WS disponible, no prueba ausencia histórica. FOK/FAK/GTD acotan vida del remanente, no borran ejecución anterior; GTC tampoco termina por tiempo. Sin prueba de rechazo/no-send o contabilidad terminal completa, permanece `UNKNOWN`. La liveness exigible es llegar a evidencia o escalación explícita; no se promete liberar toda reserva en tiempo finito bajo un protocolo que no permite demostrarlo.

**Acknowledgement y clasificación de writes — ASTRA-2:** adapter produce `WriteObservation{operation, intent/attempt_id, request_hash, account_scope, response_ref, classifier_version, evidence_class}`; Coordinator decide transición/reserva. La tabla tiene precedencia sobre heurísticas HTTP; conflicto entre fuentes domina como `UNKNOWN` hasta reconciliar. No se considera todo `success:false` un rechazo inequívoco.

| Respuesta / evidencia | Clasificación y acción |
|---|---|
| Rechazo CLOB tipado de validación/auth/policy | `DEFINITIVE_REJECT` sólo si perfil/operación/body/correlación corresponden a un contrato verificado que excluye aceptación. Allowlist del classifier versionada y probada G-03/G-12/G-16; código desconocido o contradicción → `UNKNOWN`. 400/401/403 y `success:false` por sí solos no bastan |
| ACK `success:true`, ID válido igual al hash esperado, sin error contradictorio y vocabulario admitido | `ACK_VALID` → `ACK_OBSERVED`; preservar `live/matched/delayed/unmatched` y su incertidumbre. No settlement supuesto |
| `success:true` sin ID, hash distinto, error contradictorio, body truncado/HTML/malformado o enum crítico desconocido | `AMBIGUOUS_RESPONSE` → `UNKNOWN`, no liberar ni reenviar |
| Error de transporte o timeout después de `SEND_ATTEMPT_STARTED` | `UNKNOWN`, incluso si el cliente cree no haber escrito bytes; sólo no-send probado por fencing local previo al intento permite VOID |
| 425/429/503/5xx | Por defecto `UNKNOWN` después de iniciar write. Respetar cooldown/Retry-After para futuras operaciones/lecturas; no retry automático. `post_only_mode` sólo definitivo bajo rechazo de operación exacta verificado, nunca por 503 aislado |
| `order timed out` literal en envelope CLOB | P04 §8.4 documenta rechazo previo al book: puede clasificarse definitivo sólo al verificar esa ruta/envelope/versión y correlación; antes, `UNKNOWN`. No habilita resubmisión automática en este diseño |
| `Duplicated` | Identidad posiblemente aceptada antes: lookup/trades y reconciliar; no liberar, reenviar ni regenerar firma/salt |
| Batch mixto / cancel parcial | Reducir por identidad de cada elemento; elemento faltante/ambiguo sigue `UNKNOWN`. `not_canceled` no prueba remanente vivo ni ausencia de fill |
| Fill tardío tras cancel/reject aparente | Incorporar una vez, mantener obligación y abrir contradicción si corresponde; nunca descartar por estado local terminal |

Batch place hasta 15 sólo con certificación independiente; no atomicidad multiorden. La propuesta inicial usa submit individual y cada leg tiene identidad/reserva propia.

**Retries — ASTRA-2:** lecturas idempotentes usan timeout/backoff+jitter, budgets y scopes IP/signer. Writes no tienen middleware automático de retry; en el baseline cada attempt produce como máximo una invocación de submit. Hash determinista, bytes idénticos, un único retry o HMAC nuevo no demuestran idempotencia remota. Toda resubmisión automática permanece deshabilitada: una futura excepción requeriría contrato verificado de la operación exacta, classifier versionado, revalidación de permisos/riesgo y G-12/G-17 específico, sin rediseñar estados. No volver a firmar un intent ambiguo ni usar salt/timestamp nuevo para recuperarlo. Tras rechazo realmente terminal, un candidato posterior es otra evaluación/intent, no un retry encubierto; mientras siga `UNKNOWN` no se reemplaza su exposición.

**Cancelación — ASTRA-2:** comando durable con `cancel_id`, hashes y scope autorizado; `canceled/not_canceled` se reduce por elemento. Timeout/ambigüedad conserva obligación y remanente posible. No retransmitir automáticamente el request ambiguo: observar la orden y, ante evidencia actual de remanente vivo, el Coordinator puede autorizar un nuevo comando de reducción específico; cada comando tiene su propio attempt y una sola invocación. Batch cancel ≤1000 según pack; no completar IDs faltantes como cancelados ni ampliar scope.

`REMAINDER_RECONCILED` exige evidencia terminal de esa orden y total ejecutado consistente con trades identificados. Un lookup `CANCELED` con `size_matched` aparentemente final sirve como control, pero si no hay garantía de finalización/cobertura suficiente se retiene la diferencia posible y el caso sigue abierto. La liberación sólo afecta cantidad probadamente no ejecutada; obligación de fills matched/pending, fees y diferencias no conciliadas permanece hasta `CONFIRMED` o `FAILED` con efectos conciliados. Actualización de reserva→obligación es atómica, nunca libera y vuelve a reservar entre transacciones. Fill tardío se deduplica y concilia aunque llegó después de cancel. Cancel-all está limitado al scope certificado, no prueba global de cuenta; prioridad/budget de cancel y reconcile separados de nuevos orders y research.

**Dedup y contabilización:** `trade.id` identifica el trade; aportes maker propios se separan por order hash/leg validada, incluso si varias órdenes nuestras participan. Actualizaciones de status no suman otra cantidad. WS/REST del mismo trade actualizan la misma evidencia; payload conflictivo se conserva y bloquea reconciliación, no sobrescribe sin rastro. Tx hash no es clave única de fill: una transacción puede liquidar varios. Data públicos con maker/taker rows no se suman como fills privados adicionales; no siempre ofrecen trade ID homologable. `size_matched` sirve como control de total, no como segundo asiento además de fills. Asientos correctivos referencian los anteriores; no borrar una ejecución porque un source llegó tarde.

**Reconciliación por evidencia, no “último timestamp gana”:**

| Fuente | Autoridad acotada / tratamiento |
|---|---|
| User WS | Aviso rápido de order/trade; sin snapshot total ni replay. Su caída invalida readiness live y dispara recuperación REST |
| CLOB REST | Estado de órdenes/ledger de matching; recuperar todos los pages y cada intent/order conocido; `/data/trades` con maker_address explícito y scope correcto, overlap temporal y dedup por IDs |
| Chain/RPC | Receipt, block/hash/log index, ERC20/1155 balances y payouts de contrato correcto. `MINED` no es finality; profundidad de confirmación configurable/certificada, reorg conserva incertidumbre |
| Data v2 | Corroboración eventual de posiciones/activity/resolution; `OPEN` incluye redeemable, filtros de dust/archive/inactive limitan visibilidad. Ausencia no prueba cero; no usar `total_size` lifetime como saldo actual |
| Ledger local | Intents, intentos, reservas y atribución que venue no conoce. Se reconcilia, no impone realidad a fuentes externas |

Reconciler conserva por run límites de consulta/cursor/filtros y cobertura. Captura User WS mientras recorre REST; aplica union deduplicada y revisita órdenes mutadas/ambiguas hasta converger, sin declarar snapshot atómico de REST+WS+chain. Una discrepancia persistente abre caso `UNRESOLVED`, congela nueva exposición y mantiene cancelación/lectura. Balance chain a bloque confirmado junto a transfers/fills pendientes evita doble contabilización; atribución a estrategia de transferencias externas desconocidas queda `UNATTRIBUTED`, bloquea presupuesto hasta clasificación. Failed/retrying no equivale automáticamente a saldo restaurado: revisar order, chain e inventario.

**Muere el proceso con órdenes abiertas:** el exchange puede mantener GTC/restantes y llenarlas durante la caída. No existe garantía de cancel-on-disconnect certificada; los heartbeats HTTP de P08 no se usarán como dead-man switch supuesto. Propuesta tiny-live: permitir inicialmente FOK/FAK y GTD con duración finita aprobada; GTC requiere permiso adicional del owner y prueba operacional específica. GTD respeta expiry declarada ≥ server-now+180 s y expiración efectiva 60 s antes, pero no cierra por sí solo una cuenta durante una caída ni cubre fills ya matched. El monitor de servicio del host puede reiniciar el **mismo** binario; no garantiza continuidad si el host muere.

Al recuperar — **ASTRA-2:** tomar lock exclusivo → verificar integridad/boot/audit gap → en store completo, `PREPARED` sin attempt iniciado pasa atómicamente a `VOID`, payload no enviable y reserva no consumida liberable → todo `SEND_ATTEMPT_STARTED` sin resultado queda `UNKNOWN` → cargar perfiles/scope → reconciliar órdenes/trades/balances/receipts y órdenes externas → cancelar remanentes conocidos conforme política → converger o escalar → mantener `LIVE_DISABLED` hasta nuevo lease. Un restore anterior al último send no prueba ausencia de attempt: M1.7 obliga recovery, nunca VOID por ausencia en copia atrasada. Gateway exige intento reclamado una sola vez, boot y generation actuales; no consume payload VOID ni reanuda intentos de boots anteriores. Sin cobertura no libera reservas. En cuenta compartida sólo cancela IDs propios y riesgo no atribuible bloquea disponibilidad.

**Kill y `DEGRADED_AUDIT` — ASTRA-2, FBL-007:** Supervisor revoca generation/leases de nuevos sends inmediatamente en memoria; persiste latch si puede. Gateway verifica revocación antes de firma y socket; solicitudes ya in-flight siguen inciertas. Fallo de auditoría durable entra en modo explícito `DEGRADED_AUDIT`, con allowlist cerrada:

- Lecturas de reconciliación y cancel de remanentes conocidos: `DELETE /order` por hash propio validado; `DELETE /orders` sólo conjunto de hashes propios conocidos y scope previamente autorizado. Credencial ya cargada y autorizada; ningún scope nuevo.
- `DELETE /cancel-all` sólo si cuenta dedicada y exclusividad/scope documentados antes del incidente, sin posibilidad de cancelar órdenes ajenas y con remanentes conocidos. Si no puede demostrarse ese límite, usar hashes individuales o bloquear. La respuesta tampoco libera capital.
- Cancel commands de emergencia llevan ID/tiempo/boot/scope/hashes/respuesta, ring buffer acotado y sink secundario sanitizado de mejor esfuerzo (stderr/syslog); si se satura, contar pérdida cuando sea posible. Escribir `AUDIT_GAP{boot_id,since,scopes}` en el primer store autorizado escribible (DB/journal/marcador del directorio de estado). No se promete persistencia si todos los dispositivos/sinks fallaron.

Prohibidos: nuevos orders/firma de órdenes, ampliación de exposición/scope, approvals, conversiones, transferencias de atribución y liberación de capital. Al recuperar storage, volcar buffer con provenance y marcar intervalos no recuperados, nunca reconstruir acciones inventadas. Antes de admitir live cada boot registra durablemente `BOOT_OPEN`; sólo shutdown completo reconciliado puede escribir `BOOT_CLEAN`. Marker ausente/inconsistente, boot sin cierre o restore atrasado se interpreta como continuidad desconocida, no como limpio aunque no sobrevivió `AUDIT_GAP`. Todo arranque live exige reconcile; uno con audit incompleto exige además cierre explícito del caso por operador con evidencia y registro de huecos históricos. Nuevos leases bloqueados hasta esa recuperación; un hueco irrecuperable requerido mantiene bloqueo, no PASS de auditoría. La excepción sólo reduce remanentes conocidos; `kill activo` no significa `órdenes canceladas`.

**Basket ownership y contrato — ASTRA-2, FBL-006:** Account Coordinator posee `BasketExecution{basket_id, namespace, policy_revision, candidate_ref, legs/IntentIDs, reservations, state, residual, evidence_refs}` y serializa sus transiciones junto al ledger. Execution sólo consume autorizaciones de leg; Reconciler aporta hechos; Risk evalúa cada transición con cuenta/frame actuales. Simulator reutiliza el reducer en cuenta virtual y publica feedback de basket. La estrategia declara política/modelo económico, sin callbacks de envío ni lógica de recovery.

`BasketPolicy` declara `legs_order` (SEQUENTIAL con orden total de leg IDs; PARALLEL sólo capability futura certificada), `advance_when` (cantidad mínima ejecutada/estado requerido por leg), `max_leg_skew`, deadline/TTL, tamaños/partial bounds, `max_residual_risk` y `on_partial=HOLD_AND_CANCEL_REMAINDER | REQUEST_REEVALUATION`. `UNWIND_FILLED` y `COMPLETE_IF_BUDGET` no son permisos ejecutables; una propuesta de completar/compensar debe volver como candidato nuevo al circuito Economics→Risk→Coordinator. Parámetros ausentes, cuantías ilimitadas o modelo incapaz de acotar parciales → rechazo. FOUNDATIONAL NOW simula secuencial; PARALLEL devuelve `UNSUPPORTED` hasta pruebas de todas las combinaciones de partials, sin cambiar API.

| Estado / trigger | Transición normativa y reserva |
|---|---|
| `PLANNED` → `RESERVED` o `REJECTED` | Validar política, payoff/constraints y presupuesto para conjunto y escenarios parciales; reservar atómicamente antes del primer send; sin aprobación no hay leg |
| `RESERVED` → `EXECUTING` | Autorizar una leg secuencial identificada tras revalidar revisiones/lease/Risk; misma leg no obtiene segundo attempt para recuperar ambigüedad |
| `EXECUTING` → `WAITING_LEG` / próxima leg | Avanzar sólo con evidencia que satisface `advance_when`, riesgo residual actual y budget; ACK sin fill no satisface cantidad ejecutada. Parcial conocido fuera de bounds activa política de abandono/reevaluación |
| Cualquier attempt ambiguo → `BLOCKED_UNKNOWN` | No enviar legs restantes ni compensaciones; congelar exposición posible, conservar reservas y escalar según M1.11. Se permiten lecturas y cancel de remanentes conocidos |
| Deadline, rechazo o invalidación → `ABANDONING` | Revocar legs no enviadas (VOID sólo con no-send probado), solicitar cancel de remanentes conocidos; no liberar lo incierto/ejecutado. `REQUEST_REEVALUATION` sólo emite solicitud no vinculante, no orden |
| Cancel y hechos conciliados → `RESIDUAL_HELD` o `COMPLETED` | Parciales dejan inventario/obligaciones residuales atribuidos al basket/estrategia y consumen caps. `COMPLETED` exige objetivo satisfecho, remanentes cerrados y obligaciones conciliadas; no basta último ACK |
| Abandono conciliado → `CLOSED_WITH_RESIDUAL` o `CLOSED_NO_EXPOSURE` | Cierre del workflow no borra inventario ni libera obligaciones; residual sigue en ledger/Risk. Si persiste UNKNOWN, no usar estado CLOSED |

Compensar residual es otra operación: candidato vinculado por `parent_basket_id`, autorización explícita para ese propósito/capability, presupuesto propio sin gastar fondos retenidos, quotes y evaluación actual de Risk y nuevo intent. Default no hay unwind automático; no se infiere autorización de la selección declarativa. El usuario podrá habilitar una política compensatoria sólo con mandato/gates específicos futuros. Fixture de tres legs: primera llena, segunda UNKNOWN, tercera invalidada → `BLOCKED_UNKNOWN`, tercera jamás enviada, primera sigue atribuida, segunda retenida; no unwind ni cierre ficticio. Live basket y PARALLEL siguen deshabilitados; fijar el contrato ahora no los activa.

### M1.12 — NegRisk y dispatch de protocolo versionado

`ProtocolContext` es una unión cerrada `CTF / PROTOCOL_V2 / UNKNOWN` más evidence revision, chain, contratos y mapping de outcomes. `negRisk` es otra dimensión, no el discriminador de protocolo. Un par completo de CTF token IDs y versión/contexto coherentes permite modelar la ruta CTF; position IDs v2 no se castean a token CTF aunque ambos se vean como números. Si versión, flags, pares de IDs y deployment se contradicen, `UNKNOWN/QUARANTINED`; no fallback al adapter que “funcione”. El comportamiento preferente del SDK no se convierte en garantía de wire universal (P06 §12).

| Operación tipada | Inputs/outputs que el dominio admite | Gate de dispatch |
|---|---|---|
| CTF split / merge | ConditionRef CTF, complete set, collateral/amount E6; balance deltas tipados | Contrato/ruta/allowances y receipt cert; inicialmente sin ejecutor activado |
| CTF redeem | Condition, payout final, indexSets y saldo elegible; no amount inexistente en ABI | Certificar efecto sobre todo saldo elegible: no permitir que una estrategia redima saldo de otras sin mandato de cuenta |
| CTF NegRisk convert | `NegRiskMarketID`, question indices/indexSet, amount por NO, feeBips y outcome-set revision; output esperado sólo bajo reglas documentadas | **LIVE DISABLED**, sin registro de handler ejecutable; no invocar legacy Relayer retirado |
| Protocol-v2 split/merge/redeem | Condition/position refs v2 y operación nombrada, capability unavailable si falta encoding | No reutilizar calldata CTF; certificar cada ABI/route futura |
| Protocol-v2 NegRisk convert | Intent semántico sólo para expresar requisito de investigación | **LIVE DISABLED / BLOCKED_BY_PROTOCOL**; sin ABI, selector, calldata ni resultado calculado como contrato |

CTF convert puede consumir varios NO y devolver YES complementarios y collateral con fee; el simple ejemplo NO(A)→otros YES no define el caso general ni una operación v2. `Other`/placeholders son slots con semántica versionada: nombrar un placeholder cambia interpretación del residual y exige revalidar exhaustive/mutually-exclusive antes de evaluar baskets. Gamma `negRiskMarketID` es evidencia de mapping, no certificación final de on-chain marketId; índices y feeBips deben corroborarse para activar una futura ruta.

La incorporación posterior agrega una capability concreta `protocol × operation × contract revision`, su typed codec y pruebas receipt/balance; no exige cambiar Order/Position/Relationship ni introducir una interfaz universal de smart contracts. Los adapters de posición aceptan operaciones conocidas, nunca `target+data` arbitrario de una estrategia. Un resultado simulado de conversión se etiqueta supuesto y no aumenta saldo disponible real. Reabrir la capability live exige ABI oficial, runtime/proxy codehash actual, mapping exacto event→contract IDs, permisos y test autorizado; haber documentado la función CTF o la dirección del módulo v2 no satisface ese gate.

### M1.13 — Concurrencia, backpressure y límites configurables

| Unidad | Goroutines/ownership y comunicación | Saturación / orden |
|---|---|---|
| Connection manager | Supervisor por superficie; un reader y un writer de control por conexión; heartbeat con prioridad | Bounded frames/bytes; overflow cierra epoch y bloquea assets. Limitar sockets/assets por conexión según pruebas, no asumir cap remoto no documentado |
| Ingress/Capture | Dos carriles EVIDENCE/RUNTIME y un secuenciador lógico, budgets de bytes/count/CPU/I/O y group commit (M1.6) | Overflow RUNTIME pausa runs; no revoca epochs ni ocupa reserva de evidencia. Sólo fallo/overflow de captura de evidencia declara discontinuidad |
| Book shards | N owners, partición estable por AssetKey, inbox FIFO con barreras/watermarks; N cambia con nuevo epoch/rebootstrap | Snapshot al cruzar barrera forward; máximo K refs y bytes acotados (M1.5), sin historial ilimitado |
| Frame builder | Scheduler por run, corte admitido atómicamente por dispatcher y prioridades deterministas | Sin slot/deadline → INELIGIBLE y liberar refs; nunca latest sustituto, espera de su propio descriptor ni bloqueo de capture |
| Strategy actors | Una ejecución serial por instancia, mailbox acotado | Coalescing a latest frame sólo si `DataRequirements` permite snapshots; gap control nunca omitido. Consumidor every-event desborda → pausa/invalida run, no drop |
| Cuenta real | Un Coordinator por cuenta exclusiva; transacciones y reducers seriales | Reservas/intents/fills nunca dependen de orden de callbacks concurrentes; locks no abarcan red ni fsync de raw |
| I/O ejecución/reconcile | Workers acotados, per-intent attempt fencing y jobs deduplicados | Cancel/lectura de riesgo tienen capacidad reservada. No múltiples sends del mismo attempt por timeout de worker |
| Offline / derivados | Pool de CPU/I/O/memoria limitado; misma lógica de replay con clock virtual | Pausar primero replay/compaction/export bajo presión; no competir libremente con capture/cancel |

Snapshots se exponen mediante copias/value objects o buffers con lifetime seguro y sin acceso mutable. Locks sólo para publicación breve/registry y coordinación de lifecycle; no un mutex global del monolito. `context.Context` propaga cancelación; espera de workers termina con deadline, pero no finge detener una goroutine que ignora contexto. Epoch/run generation invalida respuestas tardías. Al shutdown no se cierran channels que todavía tienen productores activos; Supervisor detiene productores, drena hasta frontera registrada y después cierra consumers.

**Configuración obligatoria y validada — ASTRA-2:** límites por cantidad **y bytes** de carriles/resultados/barreras, reserva EVIDENCE y cuotas RUNTIME, mensaje/body máximo, assets/niveles/universo/conexión, shards/estrategias, callback timeout, stale/check/skew, goroutines/jobs, K y bytes de snapshots, replay, fsync batch bytes/time, segmentos, disk watermarks, DB busy/deadline y rate budgets. `intent TTL` sólo invalida autorización de un intent no enviado; para attempt iniciado jamás libera capital. Basket TTL abandona legs no enviadas pero conserva exposición; deadlines de reconcile/settlement disparan escalación, no terminalidad remota. No infinito/0 ambiguo; valores ausentes bloquean sólo el modo dependiente. M2 puede elegir defaults no financieros conservadores con fixtures; M4 certifica workload/host. Parámetros live quedan pendientes owner, no obstáculo para read-only/shadow.

Medir receive→durable→normalize→book→frame→strategy→decision→reserve→send→ack/fill, p50/p95/p99 y máximos/queue lag, duración callback, bytes/s, fsync tail, GC, alloc, lock contention y saturación. Source→receive incorpora clock uncertainty y no se reporta como latencia exacta de red. Perf gate se define por workload/capacidad aprobados y headroom medido; cambiar universo/concurrency por encima del perfil certificado invalida readiness live hasta revalidar.

### M1.14 — Operación, observabilidad y seguridad

**Interfaces operativas — ASTRA-2:** CLI local del mismo binario primero; endpoint administrativo protegido (socket/loopback autenticado) diferido detrás del mismo puerto de comandos tipados: estado, start/stop run, inspect quality/reconcile, export, revoke lease, kill/cancel. No UI compleja. `liveness` prueba proceso/event loop, `readiness_public` catálogo/capture/datos, `readiness_strategy` requisitos y `readiness_live` lease+auth+account+data+audit; HTTP 200 no habilita live. Estado `DEGRADED_AUDIT`, scopes afectados, boot sin cierre, evidence holes y casos HUMAN_REVIEW_REQUIRED son visibles sin secretos (M1.11).

| Señal | Métricas/evidencia | Acción |
|---|---|---|
| Data | Book states/ages/skew, malformed/unknown variants, REST discrepancies/inconclusive checks, reconnect/epoch count, heartbeat age, missing initial books, catalog coverage | Bloquear universo afectado, resincronizar y mostrar denominadores excluidos |
| Recorder | admitted/durable/applied seq, fsync lag, queue bytes, lost/unknown intervals, corrupt segments, free disk, backup age/pins | Invalidar run afectado; critical disk/integrity → global live disabled |
| Cuenta/Execution | UNKNOWN intents/edad, open remanente, reservas, unmatched fills, balance discrepancies, settlement lag, cancel outcomes, scope coverage | Congelar incremento, conciliar/cancelar y alertar |
| Runtime | Strategy state, callbacks/errors/panics/deadlines, queue/coalescing, opportunity acceptance/rejection reasons | Cercar instancia y distinguir ausencia de señal de fallo |
| Economics/experimentos | Fee unresolved, model scenario spread, simulated-vs-observed fill/markout, coverage/sample/holdout, capital utilisation/lock | Invalidar conclusión o iterar modelo antes de promover |
| Recursos | CPU/RAM/GC, I/O tail, goroutines, DB WAL/checkpoint lag, workers y quota/429/warnings | Reducir trabajo cold; no degradar raw silenciosamente |

Logs estructurados correlacionan `run/experiment/strategy`, `capture/epoch/frame`, `asset/condition/event`, `intent/order/trade/tx`, `config/capability revision` y reason code. No incluir payloads sensibles completos ni IDs de alta cardinalidad como labels de métricas; los IDs viven en logs/index y, cuando se implemente, tracing. FOUNDATIONAL NOW exige métricas, diagnósticos/readiness y audit records durables; tracing live completo y alertas externas quedan diferidos por OD-2. Sus futuros budgets/destino son políticas posteriores; que falle telemetry no habilita operaciones ni bloquea cancel bajo su contrato autorizado.

| Diagnóstico de resultado | Condición observable para usar la etiqueta |
|---|---|
| `NO EDGE` | Datos aptos/cobertura suficiente, sistema sano y modelo de costes/fills aceptado; la hipótesis no cumple criterios preregistrados |
| `BAD DATA` | Gaps, metadata/fees unknown, joins inconsistentes, staleness o coverage insuficiente; resultado económico no concluyente |
| `BAD FILL MODEL` | Oportunidades dependen de queue/fills no respaldados, sensibilidad domina conclusión o calibración contradice observación |
| `SYSTEM FAILURE` | Crash, pérdida/corrupción raw, saturación, bug/timeout de callback, schema incompatible o fallo de persistence |
| `EXECUTION FAILURE` | Firma/rechazo/cancel/settlement/reconcile falla o outcome permanece ambiguo; puede coexistir con edge teórico |

Se permiten varios diagnósticos simultáneos; una clasificación no oculta fallos de otra capa. Un screen sin oportunidades durante feed caído no es NO EDGE.

**Secrets y scopes:** perfiles públicos (`SCREEN/REPLAY/SHADOW`) no cargan archivos secretos ni credenciales L2. Secrets fuera del repo, configs de research, raw, backups comunes y logs; acceso de OS mínimo al usuario del servicio, archivos/descriptor protegido o secret provider local aprobado, cifrado de artefactos privados y backups, sin asumir borrado perfecto de claves de memoria Go. EOA key, L2 triple y eventuales Relayer/Builder keys se gestionan separadamente. Allowlist de hosts TLS y chain/contract registry; no enviar credenciales a redirects/URLs arbitrarias. Rotación conserva scope/continuidad y se prueba mediante reconcile antes de retirar identidad vieja; revocar L2 no revoca allowances on-chain ni garantiza cancelar todo.

**Controles verificables in-process — ASTRA-2/3, FBL-011 / OD-1 APPROVED:** gate de imports de estrategias y dependencias revisadas: prohibir acceso directo a `unsafe`, `reflect`, `os/exec`, `net` y subpaquetes, `syscall`, `plugin`, cgo y OS/archivos; rechazar dependencias que expongan indirectamente esas capacidades. La allowlist delimita explícitamente la base confiable de Go/toolchain y puertos del engine con versión/dependencias registradas: sus internals transitivos necesarios (por ejemplo runtime/sync/unsafe bajo `context.Context`) no se tratan como imports escritos por la strategy. Sin esta delimitación, prohibir toda ocurrencia transitiva impediría implementar la propia API Go. No se permite usar esa excepción para importar internals ni envolver red/signer/I/O en una librería de estrategia. Lint rechaza goroutines propias, reloj/random global y callbacks con I/O; fixtures/race/replay verifican no mutación y determinismo. Son defense-in-depth, no aislamiento fuerte de memoria/syscalls ni sandbox. Redacción de M1.6 se verifica también en errores/fixtures centinela de `owner`, `signature` y `POLY_*`. Credentials/Signing conserva puerto tipado externalizable sin cambiar dominio ni Strategy API; no se agrega proceso ahora. Sólo código confiable revisado; aislamiento por proceso es evolución futura.

**Control único de habilitación:** `ExecutionMode = SHADOW | LIVE_DISABLED | LIVE_ENABLED` lo posee Supervisor; el gateway live sólo se construye con un `ActivationLease` no fabricable por estrategia. El lease liga account/scope, chain/protocol/operation allowlist, estrategia/binario/config hashes, evidence bundle de gates, límite de bankroll/exposición, mercados admitidos, expiración y aprobación de owner. Controlador verifica todos esos campos, readiness actual y generation en cada send; expiry/kill/restart/config drift lo revoca. `LIVE_DISABLED` puede reconciliar/cancelar órdenes existentes bajo recovery scope, pero no crear órdenes. No hay `live=true` disperso ni promoción automática desde un scorecard GO. Se propone aprobación local explícita de la configuración exacta; no un servicio remoto de autorización nuevo.

Credenciales no bastan para habilitar trading. Validar geoblock/account restrictions desde host real según ruta del pack, sin evadirlas; closed-only admite únicamente reducciones demostrables por risk y contrato certificado, no un intento de sortear el bloqueo. Read-only REST autenticado para recovery también usa scopes mínimos disponibles, sin inventar que la clave CLOB ofrece un scope read-only nativo. La separación se logra en los puertos/ejecutores y el perfil operacional. La cuenta dedicada y el código confiable son supuestos explícitos de seguridad del monolito.

### M1.15 — Testing y certificación verificable

**Estado de todos los gates físicos siguientes: `NOT_RUN`.** Sus contratos quedan FROZEN; el alcance distingue M4 no-live de IMPLEMENT LATER. La auditoría ASTRA-3 es documental y no ejecutó tests ni revalidó externamente el pack. PASS físico se emite por capability/perfil/versiones/workload probado, nunca por haber escrito el test. Cada evidencia debe registrar fixture/input hash, expected/actual, build/config y ambiente; un mock no prueba auth/settlement reales. No se requiere gastar los US$300 ni activar live para certificar el MVP read-only/shadow.

| Gate | Prueba / condición observable de PASS | FAIL / bloqueo |
|---|---|---|
| G-01 Domain/numeric unit | Vectores de IDs distintos, parsing decimal exacto y tabla completa de ticks/redondeos de P03; amounts/digests reproducen valores esperados, sin overflow ni float monetario | Namespace conflado, rounding diferente, unknown aceptado como cero o precisión perdida |
| G-02 Properties | Secuencias generadas verifican conservación de reservas/balances, no gasto doble, actualización size absoluta, IDs estables, no doble fill y no emisión sin capability; seeds de fallos retenidos | Cualquier contraejemplo a invariantes; coverage alto no lo compensa |
| G-03 Contract/fixtures | Fixtures sanitizados versionados de REST/WS/errores cubren envelopes, auth/DTO separados, arrays-string Gamma, tiempos/sentinels Data, enums divergentes y unknown fields críticos | Parser acepta contradicción como éxito o depende de camelCase SDK no wire |
| G-04 Discovery/lifecycle | Pagination repetida con altas/duplicados/cursor inválido, cambios de rules/Other/tick/fees y desaparición parcial producen revisiones/coverage correctas y bloquean candidatos viejos | Se borra mercado por scan parcial, se pierde join o se usan metadatos futuros |
| G-05 Books/reconnect | Fault injection de delta antes de snapshot, socket handover, overflow, timestamps regresivos, crossed books y REST concurrente: no frame elegible hasta nueva base y constraints | Mezcla REST+deltas WS, reutiliza epoch viejo o declara gap remoto reparado sin evidencia |
| G-06 Recorder/crash | Cortar proceso/energía simulada en write/fsync/seal/manifest; recovery valida prefijo, detecta corrupción/sufijo y marca holes; ninguna decisión confirmada depende de raw no durable | Pérdida silenciosa, manifest falso, registro parcial aceptado o tail desconocido presentado íntegro |
| G-07 Deterministic replay | Misma captura/manifests/seed/build, distinta concurrencia de ingestión offline: hashes de frames/reducers/oportunidades/scorecard iguales; replay de delivery concuerda con outputs completados | Diferencia no explicada, look-ahead de metadata o reproducción afirmada para episodio incompleto |
| G-08 Strategy contract | Fixture neutral, sin estrategia Sports/NegRisk, declara universos single/multiasset, timers/external input sintético y produce resultados consistentes en SCREEN/REPLAY/SHADOW; sin acceso de API a red, secrets, signer, wallet, repositorios ni execution ports. Revisión/gate de dependencias verifica el owner de M1.2 para cada estado mutable | Necesita implementar discovery/WS/books/recorder/replay/economics/account/risk/basket infrastructure/observability; writers duplicados o resultados mezclan simulación y live |
| G-09 Slow/failing strategy | Callback lento/panic/no cooperativo: otros consumidores mantienen progreso dentro del perfil certificado, instancia fenced, no leaks acumulativos, reinicio segura y cancel/reconcile prioritarios | Bloqueo global, callback tardío ejecuta, reintentos crean goroutines ilimitadas o shutdown falso |
| G-10 Simulation/economics | Fixtures de sweep/VWAP/fees/partials/GTD/FOK/FAK/cancel race/multi-leg/virtual liquidity: resultados exactos; missing fee/queue bounds quedan inconclusos; escenarios trazables | Touch=fill sin modelo, doble uso de depth, rewards futuros gastables o conversión disabled presentada ejecutable |
| G-11 Account/reconcile | WS duplicado/fuera de orden, REST paginado concurrente, multiple maker orders, settlement FAILED/reorg y transfers externos convergen o abren caso; no liberación doble/prematura | Balance creado, fill duplicado, 404 tratado como no-send o scope omitido |
| G-12 Ambiguous writes/recovery | Crash antes/después de marker durable, después de socket y antes de ACK; timeout/duplicate/batch mixto/cancel timeout no causan un segundo submit automático ni salt nuevo | Blind retry, reserva liberada sin prueba, intento UNKNOWN olvidado al reiniciar |
| G-13 Shadow/operación | Ventana/workload preregistrados con capture+runtime+replay limitado, sin pérdidas no declaradas; todos los skips/UNKNOWN explicables, budgets/headroom y métricas medidos | Resultado sólo favorable en optimistic, pipeline sin cobertura/recursos, readiness engañosa o monitor sin distinguir diagnósticos |
| G-14 Backup/restore local | Bundle consistente M1.7 restaurado en directorio limpio del host, hashes/refs/outbox/cursors por owner verificados, proyecciones/ledger reproducidos; duración y frontera de pérdida medidas con fixtures sin capital | Bundle incompleto presentado completo, evidencia requerida ausente con integridad PASS, cursores adelantados o liberación por restore atrasado; no certifica DR |
| G-15 Security/disabled | Intentos de pedir `deferExec=true`, builder, convert CTF/v2, protocol UNKNOWN y calldata arbitraria fallan antes de signing; perfiles read-only sin secrets; lease expirado/revocado impide nuevos sends | Un simple config flag abre ruta disabled, secreto en raw/log o capability omitida cae a ejecutor genérico |
| G-16 Auth/order integration | Ambiente autorizado y perfil wallet concreto: vectores EIP-712/HMAC/DTO correctos, body firmado=enviado, identidad/domain/hash verificados, auth real válida; resolver divergencia L1/L2 sin fallback ciego | Sólo mocks, signer/maker incorrectos, clock fuera de presupuesto o contrato no verificable; live sigue cerrado |
| G-17 Live plumbing cert | Con mandato separado y alcance acotado: place/lookup/fill o cancel según caso, recuperación de respuesta perdida, órdenes abiertas al restart, receipt/balances y kill verificados por IDs/scope; evidencia de fondos/ruta/allowances | ACK tomado como settlement, remanente desconocido, cancel-all sin proof, heartbeat asumido dead-man o test con scope distinto al lease |
| G-18 Live activation | G-01…G-17 aplicables PASS para build/config/cuenta/ruta, sin findings materiales, data/risk/fees aceptados, owner aprueba límites y lease vigente | Cualquier certificado stale, incertidumbre crítica abierta o ausencia de aprobación mantiene LIVE_DISABLED |
| G-19 Future position routes | Por operación: ABI/codehash/proxy/context/IDs/permisos+test autorizado con receipt/deltas correctos; v2 exige ABI oficial aún ausente | No habilita ninguna conversión en este shot. Sin evidencia requerida, DISABLED permanente para esa versión |

Unit/property/contract cubren primero invariantes críticos y ramas de falla. Para implementación futura aplica el piso de coverage de Agents-OS (95%) como condición complementaria, nunca como sustituto de las pruebas críticas. Fixtures negativas deben demostrar que el diseño rechaza rutas inseguras, además de aceptar happy paths. Staging mencionado en OpenAPI no demuestra sandbox funcional ni equivalencia de producción; G-16/G-17 documentarán el ambiente que realmente se autorice. Integración que implique órdenes/transacciones reales requiere mandato específico posterior; no se ejecuta por consecuencia de M1 ni para declarar cerrado M4.

**Tests de cierre ASTRA-2 — todos `NOT_RUN`:** esta matriz precisa/sustituye los criterios históricos F.4/F.6 cuando excedían la evidencia. Son tests futuros, no resultados de esta edición.

| Gate / finding | Condición verificable de cierre | Alcance |
|---|---|---|
| G-02b / FBL-010 | PREPARED sin attempt en store íntegro → VOID y payload no enviable; snapshot atrasado no permite VOID por ausencia. Cursors de dos reducers con lag no se adelantan mutuamente; mismo fill CLOB WS/REST se aplica una vez; SELL B con tokens de A falla hasta transferencia explícita idempotente | M4 fixtures/replay/restart |
| G-05b / FBL-008 | Scheduling aleatorio, shard adelantado y shard sin mutaciones: barreras no omiten records ≤C ni incluyen revisiones >C; K y bytes nunca excedidos; sin slot/snapshot → INELIGIBLE, sin bloquear captura | M4 property tests |
| G-06b / FBL-003 | Cortar seal/snapshot/export: bundle completo cubre cada cursor/dependencia/outbox, incluso con writers concurrentes; DB adelantada al journal nunca recibe PASS | M4 local |
| G-07b / FBL-004 | Replay SHADOW iguala Assessment, sizing y Risk con account/risk/liquidity/quote refs completos; borrar/alterar uno produce NOT_REPRODUCIBLE; estado actual disponible no se sustituye. Live audit se verifica con fixture, sin send | M4 |
| G-09b / FBL-009 | Saturar sólo RUNTIME bajo carga de EVIDENCE certificada: runs pausados, cero epochs revocados/holes de mercado por esa saturación; group commit sin fsync por callback, latencias medidas; crash antes de durable no publica feedback/intent | M4 workload acotado |
| G-10b / FBL-005/012 | Dos runs independientes idénticos igualan el individual; portfolio compartido manifiesta peers y atribuye competencia. Cambio de fee entre polls marca intervalo incierto; fee de trade A no se aplica universalmente a B ni antes de known_at | M4 |
| G-10c / FBL-006 | Tres legs, primera llena, segunda UNKNOWN, tercera invalidada: tercera no enviada, reservas/residual conservados, sin unwind; misma secuencia de hechos produce mismo estado en Simulator y gateway fixture. Compensación sin nueva autorización/budget/Risk rechazada | M4 reducer/fixtures; live diferido |
| G-11b / FBL-001 | ACK/fill tardíos conservan reserva y convergen por evidencia; expiry+REST ausente+balances iguales con match pendiente sigue UNKNOWN y escala. Caso sin prueba nunca libera por tiempo; rechazo inequívoco sí libera sólo obligación inexistente | M4 fixtures; evidencia venue real G-17 |
| G-12b / FBL-002/010 | 425/429/503/500/HTML, success ambiguo, duplicate y order timed out no verificado → sin segundo submit/re-firma. Cancel parcial/trade tardío no libera obligación pendiente; bytes/hash iguales no habilitan retry. Contador de sends por attempt ≤1, sin exposición duplicada tras crash | M4 fixtures; classifier real G-16/G-17 |
| G-13b / FBL-007 | DB caída → sólo cancel conocido/scoped, sin nuevos sends antes de firma ni liberación; sink/marker cuando escribibles, buffer recuperado con gaps. Todos los sinks fallan + restart → BOOT_OPEN/no cierre impide continuidad limpia y lease hasta reconcile/cierre explícito | M4 fault fixtures, no cancel real |
| G-14 / FBL-003 | Restore local completo y GC simulado día 31: ACCOUNT_FACT/evidencia privada intacta y fuera del TTL; research expirado declarado no reproducible. Archivo/compactación conserva semántica/lineage y no permite borrado sin política explícita de cierre/archivo. Eliminar activo requerido del bundle → integridad FAIL/degradada, no PASS hasta reconstruir evidencia; health read-only puede funcionar | M4; TTL sólo fixture, GC automatizado diferido |
| G-15b / FBL-011 | Strategy neutral con context/puertos revisados pasa el gate de imports; import directo prohibido o dependencia que exponga capacidades prohibidas, goroutine propia o cgo → falla. La base Go confiable está delimitada/versionada según M1.14. Fixtures de body/error/headers/evidencia ACCOUNT_FACT y restore no filtran owner/signature/POLY_*/secretos reutilizables; ACL mínima verificable y read-only sin secrets. No afirmar sandbox por pasar lint | M4 con fixtures sintéticos; cifrado/custodia reales antes de persistir evidencia privada real |
| G-14b / recuperación fuera del host | Host perdido, bundle externo cifrado y claves recuperables, exclusividad/fencing de instancia previa, rotación y reconcile; RPO/RTO medidos bajo presupuesto owner. Falla cualquier dependencia → sin lease ni DR PASS | IMPLEMENT LATER, mandato separado |

**Cierre M4 sin live — ASTRA-2/3, OD-2 APPROVED:** G-01…G-15 y extensiones anteriores, salvo G-14b, son fundamentales en su alcance no-live. Estados de intents/cancel/basket/audit y permisos se prueban con reducers, stubs deny-all y fault fixtures; no exigen implementar HTTP live/User WS privado/Reconciler live completo/RPC/signer/ActivationLease operativo/cifrado de payload firmado para pasar M4. El alcance de G-03/G-15 sobre auth/firmas es schema, rechazo de rutas y sanitización de fixtures, no integración criptográfica real. Datos privados sintéticos bastan para estos fixtures; no se autoriza captar evidencia privada real antes de cumplir su custodia/cifrado aplicable. G-16…G-19, G-14b y mediciones operacionales live tienen alcance IMPLEMENT LATER y estado físico `NOT_RUN`; sólo las rutas posteriormente autorizadas deben ejecutarlos. G-18 sigue siendo aprobación de activación live, separado de G-19 por operación futura. M4 certifica núcleo durable read-only/shadow y restore local, nunca trading, DR ni capacidades diferidas.

**Partición normativa OD-2 APPROVED — FROZEN por ASTRA-3:**

| FOUNDATIONAL NOW | IMPLEMENT LATER WITHOUT REDESIGN |
|---|---|
| Journal con CRC/checksum por segmento, dos carriles, clases de evidencia, manifests/pins básicos, prefijo de crash y bundle/restore local consistente G-14 | Compresión/encadenado entre segmentos, GC/pins automatizados, copias fuera del host, DR/RPO/RTO G-14b y rotación real |
| Dominio e IDs tipados/decimal exacto; Catalog/Universe known-at; Regimes/Resolution necesarios; market-data adapters read-only; Book shards/quality y Frame Builder con corte forward acotado; replay determinista dentro de M1.6; Strategy API y SCREEN/REPLAY/SHADOW | Sports WS/adapters externos concretos hasta requerimiento de POC; Protocol-v2 codecs no certificados; operaciones on-chain activas y conversiones NegRisk detrás de contratos/allowlist, sin ejecutor habilitado |
| Account Coordinator/reducers/ledger/reservas/atribución; BasketPolicy/BasketExecution secuencial común; Simulator multi-leg con liquidity ledger aislado por experimento y portfolio explícito, optimistic/base/stress; gates y fault fixtures de ambigüedad/DEGRADED_AUDIT | Trading live; Execution HTTP real/User WS y Reconciler live completo cuando sólo sirvan ejecución real/RPC; signer/perfil LIVE/ActivationLease operativo/cifrado de payload firmado; basket live/PARALLEL/compensación autorizada; resubmisión automática sigue disabled |
| Experiment/Hypothesis framework; SQLite operacional WAL FULL para cuenta/metadata; datasets/scorecards con manifest/lineage en SQLite/JSONL; CLI, observabilidad/readiness, diagnósticos y métricas | Parquet si hace falta mediante mismo manifest/schema lógico; endpoint admin mediante mismos comandos; alertas externas, tracing live completo y dashboards/UI; maker queue calibrado |

También quedan IMPLEMENT LATER y sin permiso de activación: `deferExec=true`, Builder modes, Session Keys, auto-wallet/auto-approvals, Combo/RFQ y Bridge/funding automático. Conservan las exclusiones de M1.1/M1.12; diferir no equivale a prometer contrato externo disponible ni a habilitarlos. Restore desde infraestructura remota, disaster recovery off-host y rotación operacional de credenciales live quedan en G-14b/fases live; el backup/restore **local consistente y medido** es foundational.

Los puertos/identidades/revisiones, ownership, dominio, Strategy API, persistencia, policy schemas y gates ya definidos son contratos FROZEN ahora; diferir implementación no autoriza dejarlos abiertos ni exigir rediseño posterior. Los componentes diferidos añaden adapters/implementaciones detrás de esos contratos; una ABI ausente sigue BLOCKED_BY_PROTOCOL. No se requieren 35 subsistemas para 35 decisiones. Esta partición sustituye F.7: bundle/restore local medido es FOUNDATIONAL NOW; restauración fuera del host sigue diferida. Compresión/encadenado/Parquet son evoluciones compatibles, no requisitos de primera certificación. No hay plan M2 en esta partición.

### M1.16 — Registro de decisiones arquitectónicas FROZEN

Registro de ASTRA-1 reconciliado por ASTRA-2 y congelado por ASTRA-3; se conservan alternativas/riesgos y la trazabilidad de enmiendas. OD-1/OD-2/OD-3 están `APPROVED`; los contratos reconciliados pasan de `PROPOSED` a `FROZEN`. `DEFERRED_LIVE_DECISION` reserva políticas/valores exclusivos de live sin bloquear M2; `BLOCKED_BY_PROTOCOL` conserva las rutas sin contrato disponible. FROZEN no certifica implementación ni congela cifras operacionales propuestas. M1.2–M1.15 y las enmiendas siguientes definen el alcance vigente.

| ID | Decisión vigente | Alternativas históricas | Rationale | Tradeoff | Riesgo | Estado |
|---|---|---|---|---|---|---|
| A-01 | Módulos/puertos y reducers de M1.2, domain libre de adapters | Shared services con acceso a tablas; bus genérico | Ownership y dependencias auditables sin distribuir el sistema | Más contratos y composition explícitos | Erosión de boundaries si se aceptan shortcuts | FROZEN |
| A-02 | Account Coordinator único writer y transacción de reserva+intent+ledger (M1.10–11) | Writers separados de risk/orders/positions | Evitar doble gasto y contradicciones de cuenta | Serializa cuenta; reduce throughput máximo | Transacción demasiado larga o reducer incorrecto | FROZEN |
| A-03 | Tipos nominales, decimal exacto/enteros, schemas wire separados (M1.3) | float64 monetario; tipos SDK como wire | Precisión y namespaces de protocolo verificables | Más conversiones/control de overflow | Drift de schema/rounding | FROZEN |
| A-04 | Catálogo versionado conocido-a-fecha y Universe central (M1.4) | Discovery por estrategia; sólo estado latest | Reutilización y replay sin look-ahead | Storage/captura de metadata | Páginas no atómicas; relaciones incompletas | FROZEN |
| A-05 | Bootstrap WS full por epoch; REST como observación independiente (M1.5) | Stitch REST+deltas por timestamp; sólo polling | No existe barrera común; no fabricar continuidad | Bloqueos y menor disponibilidad | Gaps remotos silenciosos siguen indetectables | FROZEN |
| A-06 | `OBSERVED_USABLE` con quality budgets y aprobación de riesgo residual para live | Declarar book perfecto; prohibir todo live indefinidamente | Expresar límites reales de feed sin falsear garantías | Aceptar incertidumbre residual explícita | Decisión con book remoto stale no detectable | FROZEN: quality contract; DEFERRED_LIVE_DECISION: aceptación residual |
| A-07 | Frame local por corte/revision vector y freshness multiasset (M1.5) | Leer latest de cada shard sin corte; serializar todos los books | Coherencia local/replay, sin fingir simultaneidad venue | Barreras locales/retención de revisiones | Shard lento y skews entre assets | FROZEN |
| A-08 | Capture durable-before-publish con journal segmentado (M1.6) | Best-effort async recorder; base SQL de todo raw | Evidencia durable antes de decidir; recuperación de prefijo | Latencia/fsync y menor disponibilidad | Disco/host único y pérdida antes de admisión | FROZEN |
| A-09 | Observación y delivery replay, auditoría de decisiones y simulación contrafactual separados (M1.6) | Reproducir scheduling Go; prometer historia completa | Determinismo sobre evidencia efectivamente capturada | Registrar frames/control y mantener lineage | Confundir replay propio con verdad del mercado | FROZEN |
| A-10 | SQLite WAL FULL + journal; derivados SQLite/JSONL con lineage y Parquet diferido (M1.7/15; OD-2 APPROVED) | PostgreSQL local; todo en una DB; TSDB | Un host/binario, transacciones y raw secuencial | Writer único y formato de journal a mantener | Contención, driver o restore no probado | FROZEN |
| A-11 | ACCOUNT_FACT/evidencia privada vida del proyecto, ACL/cifrado aplicable y pins; raw/derivados separados, TTL aún propuesto (M1.7; OD-3 APPROVED) | Retener todo; borrar por edad sin refs | Control de NVMe preservando experimentos | Coste de pins y GC seguro | Capacidad insuficiente / reproducibilidad perdida | FROZEN; OD-3 APPROVED; TTL raw/derivados posterior, sin GC inicial |
| A-12 | Bundle consistente + restore local medido M4 (OD-2 APPROVED); DR off-host/destino/cadencia/RPO/RTO diferidos | Sólo NVMe local; plataforma replicada | Certificar crash/restore local; cobertura de pérdida física sólo con G-14b posterior | Coste externo y restore/key management | Copia atrasada o llave irrecuperable | FROZEN; OD-2 APPROVED; DR off-host diferido |
| A-13 | applied_seq por owner + outbox idempotente DB/journal; integridad por clase y evidencia ACCOUNT_FACT retenida (M1.7; OD-3 APPROVED) | Pretender atomicidad de dos stores; doble escritura naive | Fronteras de crash/recovery demostrables | Reducers idempotentes y repair de índices | Referencias huérfanas si invariantes se rompen | FROZEN |
| A-14 | Strategy API pura/serial, misma lógica en cuatro modos (M1.8) | Bot por estrategia; API de envío directa | Reducir coste marginal de hipótesis | Restricciones a código POC y snapshots | POC introduce I/O/no determinismo | FROZEN |
| A-15 | Código Go confiable revisado in-process, defense-in-depth sin sandbox, fencing/restart y Credentials/Signing externalizable (M1.8/14; OD-1 APPROVED) | Sandbox por proceso/VM; hot plugin arbitrario | Baseline un proceso, límite honesto de Go | No aislamiento físico entre estrategias | Panic fatal/OOM/código malicioso afecta todo | FROZEN; OD-1 APPROVED |
| A-16 | Simulator común con liquidity ledger por run y optimistic/base/stress (M1.9) | Touch=fill; simulador por POC | Comparabilidad, costes y parcialidad compartidos | Mayor modelado y límites contrafactuales | Queue/impacto no observables | FROZEN |
| A-17 | Experimentos preregistrados/versionados, GO no equivale a live (M1.9) | Threshold económico universal; optimizar hasta beneficio | Falsación/OOS y control de selección | Más disciplina de metadata | Holdout contaminado o muestra insuficiente | FROZEN |
| A-18 | FeeResolver por régimen; missing mapping → intervalo/inconcluso/live bloqueado (M1.10) | Tabla global de categoría; base_fee convertido sin prueba | P07 no unifica todas las superficies | Puede bloquear mercados fee-enabled | Fee efectiva subestimada | FROZEN |
| A-19 | Incentivos estimados separados de cash/payout realizado (M1.10) | Financiar sizing con rewards esperados | Evitar capital ficticio y doble contar fees | Menor capital desplegable | Forecast de programa inestable | FROZEN |
| A-20 | Cuenta real compartida y simulación aislada por default; límites/reparto/lock/worst-loss live posteriores (M1.9/10) | US$300 por estrategia; asignación arbitraria fija | El capital total es del proyecto | Rechazos por capital y coste de oportunidad | Exposición correlacionada/unknown | FROZEN: contrato de cuenta; DEFERRED_LIVE_DECISION: caps/reparto |
| A-21 | Journal de intent/attempt; ningún blind retry ni salt nuevo automático (M1.11) | Retry HTTP genérico; “exactly once” vía hash | No hay Idempotency-Key universal documentado | Fondos bloqueados en UNKNOWN | Incertidumbre prolongada sin retención venue | FROZEN |
| A-22 | Reconcile REST/WS/chain por autoridad, overlap/dedup y corrections (M1.11) | WS solamente; Data PnL como ledger | Matching y settlement son estados distintos | Múltiples observaciones eventualmente consistentes | Scope/retención/reorg impiden cierre | FROZEN |
| A-23 | Cuenta dedicada, perfil wallet elegido/certificado y sin session keys beta iniciales | Wallet compartida; auto-setup SDK/session | Simplifica permisos, cancel y attribution | Operación de funding/permisos fuera del engine | AccountProfile mal configurado | FROZEN: boundary/permisos disabled; DEFERRED_LIVE_DECISION: cuenta/perfil real |
| A-24 | FOK/FAK/GTD iniciales; GTC sólo autorización adicional; restart cancela remanente (M1.11) | GTC default; heartbeat asumido cancel-on-death | Acotar exposición tras caída sin inventar dead-man switch | Ventanas GTD limitan ciertas POCs | Host muerto no puede cancelar; fills en caída | DEFERRED_LIVE_DECISION: selección/política; recovery FROZEN en M1.11 |
| A-25 | Kill revoca nuevos sends, cancel/reconcile por carril reservado; cancel defensivo si storage falla (M1.11) | Esperar recorder/DB para todo; liquidación agresiva automática | Priorizar reducción de órdenes remanentes bajo incidente | Audit parcial en emergencia, alerta obligatoria | Cancel falla o llega tras match | FROZEN |
| A-26 | Protocol union CTF/v2/unknown y operaciones tipadas (M1.12) | tokenId universal; smart-contract framework genérico | Versiones no equivalentes, evolución acotada | Más validación por ruta | ID/ABI de generación incorrecta | FROZEN |
| A-27 | Conversión NegRisk CTF y v2 sin handler live; v2 sin calldata (M1.12) | Activar por flag negRisk/dirección conocida | Preservar gates M0 y ABI/deployment no certificados | POCs pueden concluir sólo condicionalmente | Extrapolación indebida de conversión CTF | BLOCKED_BY_PROTOCOL |
| A-28 | CTF position ops modeladas; v2 encoding no inferido (M1.1/12) | Implementar calls de SDK por semejanza; omitir dominio de posiciones | Evolución sin reescribir dominio ni inventar ABI | Postergación de activación de rutas | Permisos/payout/ABI incompletos | FROZEN |
| A-29 | Buffers por bytes/count, single-owner shards y slow-strategy policy (M1.13) | Goroutine por evento; colas ilimitadas; lock global | Backpressure visible y orden local | Complejidad de epochs/cancel/drain | Saturación shared host | FROZEN |
| A-30 | Sin límites arbitrarios de latencia; perf por perfil medido (M1.13) | Objetivos HFT inventados; no medir | North star es validación, no benchmarks aislados | Requiere workload/medición para live | Universo supera perfil certificado | FROZEN |
| A-31 | ActivationLease central por build/config/scope/capability, no bool (M1.14) | Flag live global; permisos dentro de estrategia | Autorización y revocación auditables | Gestión de evidence bundles/expiry | Lease obsoleto o validación incompleta | FROZEN |
| A-32 | Observabilidad con cinco diagnósticos y readiness por capability (M1.14) | Health único; PnL como señal de salud | Separar NO EDGE de errores de datos/sistema | Métricas/labels y operación a mantener | Falsa clasificación o cardinalidad alta | FROZEN |
| A-33 | External seam capturable; Sports feed sólo si requerido; sin proveedores especulativos (M1.4/8) | Framework externo universal; cada POC hace I/O | Dos consumidores reales y datos fundamentales | Integración específica posterior | Joins deportivos/source freshness incompletos | FROZEN |
| A-34 | Gates físicos por capability y M4 sin live posible (M1.15) | Certificar todo por smoke test; exigir capital para MVP | Respeta M0/M4 y autorización posterior | Estados/gates más explícitos | Confundir MVP certificado con trading listo | FROZEN |
| A-35 | Mantener backfill L2, deferExec true y Builder disabled; Combo/RFQ fuera (M1.1) | Activarlos desde esquemas parciales | Conserva exclusiones M0 sin expandir core | Capabilities diferidas | Ruta accidental por config/adapter genérico | FROZEN |

**Enmiendas normativas ASTRA-2, ratificadas y congeladas por ASTRA-3 — sustituyen el alcance histórico incompatible; OD-1/2/3 APPROVED:**

| ID afectado | Decisión normativa reconciliada / finding | Coste o riesgo residual | Estado |
|---|---|---|---|
| A-02 / A-13 | Cursors por reducer/namespace, VOID con no-send probado, FillKey CLOB común WS/REST y atribución explícita (M1.3/7/10/11; FBL-010) | Restore atrasado exige reconcile, no VOID por ausencia | FROZEN |
| A-07 | Corte forward con barrera FIFO admitida antes de >C, K+bytes acotados (M1.5/13; FBL-008) | Frame inelegible si no hay capacidad; no historial ilimitado | FROZEN |
| A-08 / A-29 | EVIDENCE/RUNTIME separados; descriptor appended antes del callback, inputs/resultado durables antes de efectos (M1.6/13; FBL-009) | Callback incompleto debe reconstruirse; host compartido conserva límites | FROZEN |
| A-09 | Observación, decisiones, auditoría real y contrafactual separados; vector efectivo por fase recuperable (M1.6; FBL-004) | Storage/pins; faltante da NOT_REPRODUCIBLE | FROZEN |
| A-10 | SQLite/journal fundamentales; SQLite/JSONL derivados primero, Parquet diferido (M1.15) | Exportación posterior conserva schema/lineage | FROZEN; OD-2 APPROVED |
| A-11 | ACCOUNT_FACT y evidencia privada fuera de GC 30d, retención vida del proyecto; research expirado explícito (M1.7; FBL-003) | Privacidad/capacidad/custodia, sin borrado de requeridos | FROZEN; OD-3 APPROVED; TTL raw/derivados posteriores |
| A-12 | Bundle consistente y restore local M4; backup/DR fuera del host y SLA posterior G-14b (M1.7/15; FBL-003) | Local no cubre pérdida física; claves/fencing necesarios después | FROZEN; OD-2 APPROVED; destino/RPO/RTO off-host posteriores |
| A-14 / A-16 | Strategy declara BasketPolicy; Coordinator posee BasketExecution, Execution I/O, Simulator mismo reducer; sin unwind declarativo (M1.8/11; FBL-006) | Residual puede mantenerse; basket live deshabilitado | FROZEN |
| A-16 / A-17 / A-20 | Simulación aislada por experimento/scenario; portfolio compartido explícito y competencia atribuida; bankroll real sigue compartido (M1.9/10; FBL-005) | Comparabilidad depende de manifest, no mezcla accidental | FROZEN; caps live DEFERRED_LIVE_DECISION |
| A-15 | Código confiable in-process con imports/lint/fixtures y límites explícitos, no sandbox (M1.14; FBL-011) | Código malicioso/OOM puede afectar todo; signer separado no aísla estrategias | FROZEN; OD-1 APPROVED |
| A-18 | Fee observada sólo evidencia del trade; conflicto marca REGIME_SUSPECT, sin tarifa universal (M1.10; FBL-012) | Mapping y cota siguen U-02 | FROZEN |
| A-21 / A-22 | Clasificador por evidencia exacta; UNKNOWN converge a prueba o revisión, sin timeout-release ni resubmit automático/re-firma (M1.11; FBL-001/002) | Puede quedar capital retenido indefinidamente sin prueba remota | FROZEN; thresholds DEFERRED_LIVE_DECISION |
| A-25 / A-31 | DEGRADED_AUDIT sólo cancel conocido/scoped, best-effort secondary sink, boot desconocido/reconcile bloquean lease (M1.11/14; FBL-007) | Persistencia imposible si todos los sinks fallan; audit gap explícito | FROZEN |
| A-32 / A-34 | M4 núcleo/CLI/diagnósticos y fault fixtures; G-14 local obligatorio, G-14b/16…19 posteriores (M1.15) | M4 no certifica live ni disaster recovery | FROZEN; OD-2 APPROVED |

### M1.17 — Incertidumbres acotadas y handoff vigente M2/TOP

**Incertidumbres de implementación/protocolo y políticas posteriores:** fail-closed define el comportamiento seguro sin inventar evidencia. ASTRA-3 no investigó nuevamente estos puntos. OD-1/2/3 están aprobadas; no quedan decisiones arquitectónicas materiales pendientes para M2. Políticas exclusivas de live quedan DEFERRED_LIVE_DECISION y no congelan valores aún desconocidos.

| ID | Incertidumbre / aprobación pendiente | Mecanismo seguro actual | Evidencia/decisión necesaria posteriormente |
|---|---|---|---|
| U-01 | Orden/gaps silenciosos WS, inexistencia de barrera REST/WS y retención no garantizada (P10 §24A) | Epochs/quality y captura propia; sin replay completo de mercado; live necesita aceptación A-06 | Certificación empírica acotada y política owner; pruebas no crean garantía global |
| U-02 | Mapping fees efectivos `base_fee/fd/category`, empate rounding, delay por mercado | Fee interval/inconcluso; no live sin cota aprobada; snapshot de inputs | Contract fixture/integración de mercado concreto; no despejar mediante constante Sports del ERC |
| U-03 | Envelope keyset y variantes auxiliares WS no expandidas íntegramente; contradicciones de host/ruta en tablas resumen | Usar contratos explícitos; fallback offset capturado y raw+refresh ante evento desconocido | Validación de integración de los campos usados; un missing field requerido bloquea esa ruta |
| U-04 | Auth list-keys L1 OpenAPI vs L2 SDK, enum placement/trade y clock tolerance | Auth adapter limitado al perfil; no fallback automático de firma/headers; unknown estados bloquean | G-03/G-16 y fixtures de wire; evidencia específica para equivalencias de enum |
| U-05 | ABI v2 de posición/conversión, CTF convert deployment/mapping/approvals/route | Todos los convert live disabled y codec v2 no supuesto | G-19 por operación con ABI/version/runtime/payout/balances; no basta dirección conocida |
| U-06 | Finality/reorg policy, latencia/indexing/retención REST terminales, fees efectivas de fill | Reservas conservadoras, estados pending/UNKNOWN y casos sin cerrar | Política de confirmación por chain/ruta y pruebas de settlement/recovery |
| U-07 | Owner: wallet/account scope, US$300 efectivo, caps, capital lock, GTC/GTD, residual book risk | LIVE_DISABLED, sin funding/autorizaciones on-chain automáticas | A-06/A-20/A-23/A-24 resueltas con configuración revisable y lease posterior |
| U-08 | OD-3 APPROVED: ACCOUNT_FACT/evidencia privada vida del proyecto; OD-2 APPROVED: backup/restore local medido foundational. TTL raw/derivados, presupuesto y operación off-host posteriores | ACL mínima/cifrado aplicable, sin secretos reutilizables; pins, sin TTL privado ni borrado sin política de cierre/archivo; disco crítico fail-closed | A-11/A-12/A-13 FROZEN; G-06b/G-14 local NOT_RUN para M4. Destino/claves/RPO/RTO off-host y canal externo quedan diferidos; no bloquean M2 |
| U-09 | Throughput/fsync/GC y queue/fill realism todavía sin mediciones | Buffers acotados, escenarios explícitos, no SLO inventado ni fill garantizado | G-09/G-10/G-13 con workload/host; bounds y latencia calibrados por experimento |
| U-10 | APPROVED — OD-1: estrategias Go confiables/revisadas in-process, sin aislamiento fuerte de memoria/syscalls | API sin red/signer/wallet/repositorios/execution ports; imports/lint/ausencia de secrets como defense-in-depth, sin plugins arbitrarios | A-15 FROZEN; G-15b NOT_RUN. Credentials/Signing externalizable sin cambiar dominio/Strategy API; aislamiento por proceso futuro, no requisito M2 |

**Enmiendas ASTRA-2 a U, ratificadas por ASTRA-3:** U-02 incluye fee trade-observed sin extrapolación (Regimes/Economics; G-10b, integración futura). U-04 incluye verificación por operación del classifier: hash/JSON/status no son idempotencia ni prueba genérica de rechazo (Execution; G-12b/G-16/G-17). U-06 conserva ausencia de garantía de terminalidad/exhaustividad: Coordinator/Reconciler mantienen UNKNOWN y escalan, nunca liberan por expiry/balances; owner fija después deadlines/settlement_window de observación, finality y caps de casos para live. U-08 registra OD-3/OD-2 APPROVED y separa retención privada/restore local fundamental de destinos/claves/RPO/RTO off-host/alertas futuros; G-14 local obligatorio, G-14b diferido. U-10 registra OD-1 APPROVED con controles G-15b y límite no-sandbox.

M1 está cerrado como **M1_DESIGN_FROZEN**: OD-1/2/3 APPROVED y auditoría final documental PASSED. Los doce findings tienen contrato y gate observable, todos los gates físicos siguen NOT_RUN. Bankroll/caps/worst-loss, settlement window/máximo de UNKNOWN, GTC/book residual, wallet/cuenta real/finality/allowances/live NegRisk, credenciales y RPO/RTO off-host/alertas son decisiones posteriores de activación live; conservan LIVE_DISABLED y no bloquean M2. TOP recibe el proyecto frozen y Technical Platform Map; Edge Research sólo si necesita requirements transversales. Debe planificar FOUNDATIONAL NOW sin rediseñar ni inventar estados/stores/permisos; contradicción material → BLOCKED — DESIGN ISSUE al manager. M2 no se desarrolla en ASTRA-3.

**Control de completitud de ASTRA-1 — revisión documental realizada, no certificación del software:**

| Pregunta exigida | Respuesta trazable y límite |
|---|---|
| 1. ¿Toda capability tiene responsable? | M1.1/M1.2 cubren market/protocol, data, recorder, research, economics, trading, external seam y observability; las excluidas tienen bloqueo explícito |
| 2. ¿Límites de módulos explícitos? | M1.2: puertos, imports permitidos, comandos/eventos distintos y transacción de cuenta como boundary deliberado |
| 3. ¿Un owner por dato? | Catalog, Book shards, Regimes/Resolution, Capture, Runtime y Account Coordinator; simulador y observaciones externas no son ledgers reales alternativos |
| 4. ¿Recorder sobrevive fallos? | M1.6–7: prefijo durable verificable, seal/recovery, pérdidas visibles y backups; no sobrevive pérdida del host sin copia externa |
| 5. ¿Replay honesto? | M1.6: determinismo de captura/delivery; huecos y contrafactuales explícitos; sin reconstrucción universal L2 |
| 6. ¿Book inconsistente bloquea? | M1.5: SUSPECT/STALE/HALTED no producen candidato ejecutable; riesgo de gap no observable permanece U-01 |
| 7. ¿Estrategia lenta bloquea? | M1.8/13: actor/mailbox/deadline/fencing, sin bloqueo síncrono del book; no-cooperación puede requerir restart del proceso |
| 8. ¿Estrategia ejecuta sin permiso? | No recibe signer/send; M1.14 registry+lease+gateway. Seguridad contra código hostil in-process no prometida |
| 9. ¿Timeout duplica órdenes? | M1.11: attempt durable, UNKNOWN, reserva retenida, ningún retry ciego/salt nuevo; no se promete exactly-once del exchange |
| 10. ¿Disabled es fail-closed? | M1.1/12/14 y G-15: sin handler/calldata genérica, allowlist cerrada y pruebas negativas |
| 11. ¿Sports/NegRisk consumen sin deformar? | Universe/relationship revisions, frames multiasset, depth/costs/partials comunes y external seam; semántica particular/payoff en POC |
| 12. ¿TOP puede planificar sin inventar arquitectura? | Ownership/contratos/stores/recovery/estados/gates definidos; A/U pendientes visibles para reconciliación. M2 sólo después de aprobación/freeze, no en este shot |

**FABLE HANDOFF histórico de ASTRA-1 — conservado como antecedente, cumplido por F.1–F.9; no es el próximo paso vigente:**

| Prioridad | Qué debe cuestionar FABLE | Criterio de finding accionable |
|---|---|---|
| P0 | ¿Alguna ruta REST/WS/cutover declara consistencia que no puede demostrar? ¿Puede una lease de datos sobrevivir un overflow/tick change? | Contraejemplo de oportunidad o send sobre epoch/constraints inválidos; distinguir incoherencia detectada de riesgo remoto no detectable |
| P0 | ¿Crash entre reserva/firma/attempt/send/ACK permite duplicar orden o liberar capital? | Timeline con dos efectos externos o gasto doble; comprobar shutdown y recuperación bajo retención insuficiente |
| P0 | ¿Disabled/conversion/v2/Builder puede llegar a un signer por camino alternativo? | Ruta de permiso o payload capaz de eludir capability registry; revisar account signer/type/domain |
| P0 | ¿Conciliación duplica fills, descuenta dos veces settlement o olvida scopes/órdenes externas? | Fixture maker/taker/partial/cancel/reorg que viole conservation o deje exposición no contabilizada |
| P1 | ¿Durable-before-publish y delivery journal son sostenibles con fsync/SQLite/un host? | Punto de saturación/ciclo de espera, boundary de recovery no cubierto o claim de determinismo falso |
| P1 | ¿Frames multiasset/metadata conocida-a-fecha y fill model introducen look-ahead, liquidez reutilizada o queue ficticia? | Dataset mínimo donde cambie conclusión por error del engine y no por hipótesis |
| P1 | ¿Strategy API obliga a la POC a rehacer una capability o introduce abstracción especulativa? | Consumidor S01/S02 con requisito transversal concreto que el contrato no cubre |
| P1 | ¿Aislamiento cooperativo/kill/host único ofrece menos protección de la que el owner cree? | Modo de fallo que escape fencing/restart o suponga cancelación venue no documentada |
| P1 | ¿Fees, rewards, finality y lock desconocidos pueden presentarse como net edge/available capital válido? | Caso con costes no acotados o ingreso esperado usado como saldo |
| P2 | ¿Retención/pins/backups y gates permiten auditar el resultado sin repetir research? | Evidencia no reproducible, fuente/versión sin provenance o PASS imposible de observar |

El mandato histórico pidió findings por sección/A-ID/U-ID, evidencia, contraejemplo y cierre, sin reemplazar TPM. FABLE lo completó en F.1–F.9 y ASTRA-2 reconcilió sus doce findings. **NEXT vigente: M2 — TOP IMPLEMENTATION PLAN**, autorizado por el cierre ASTRA-3. Los bloques FABLE y ASTRA-2 siguientes se preservan íntegros como historial: sus estados, REQUIRES_OWNER y próximos pasos describen esos shots, no el estado vigente. La autoridad frozen es M1.1–M1.17 con el registro final ASTRA-3.

## M1 — FABLE Adversarial Challenge

**Estado del shot:** `M1_FABLE_CHALLENGE_COMPLETE` · **Autor:** FABLE-1 · **Fecha:** 2026-09-17 · **Resultado:** `MATERIAL_FINDINGS_REQUIRE_RECONCILIATION`. Esta sección audita la propuesta ASTRA-1; no la reemplaza, no congela M1, no implementa código y no ejecuta gates físicos. Toda corrección indicada es una resolución mínima propuesta que ASTRA-2 integra durante la reconciliación preservando autoría.

### F.1 — Alcance y baseline auditado

- **Baseline:** `xKoRx/agents-os` · `master` · commit ASTRA-1 `4e95dcd1a7a605c210e7f421933d48b3477451f9` · blob del proyecto `b78142b34a88bf9afa398ca32be281ca71f224e1` (idéntico en HEAD local al iniciar; sin cambios concurrentes sobre el archivo).
- **Leído íntegramente:** objetivos, capabilities, gates M0–M4, M1.0–M1.17, A-01…A-35, U-01…U-10 y handoff FABLE.
- **TPM consultado selectivamente para verificar findings:** P10 §24–25 (estado M0, recovery matrix, dinámicos); P04 §7A–E y §8.1–8.4 (Order firmado, DTO, wrapper, estados, writes ambiguas, matriz de errores); P05 §9.1–9.5 y §10–11 (books, Market/User WS, CTF, contratos, allowances); P03 §4 y §6 (identidades, L1/L2, tiempo); P07 §18 (rate limits y buckets por signer). ERC §2–4 sólo para requisitos transversales de baskets/relaciones. No se abrió Internet, SDKs, investigaciones originales ni otros proyectos; no se modificó el TPM.
- **Criterio:** se buscaron contraejemplos reproducibles sobre pérdida de datos, capital incorrecto, duplicación de efectos, falso resultado experimental, deadlock, recuperación imposible o complejidad innecesaria. Las decisiones macro frozen `D-001…D-014` no se reabren. Ningún finding exige otro engine.
- **Veredicto agregado:** la propuesta es conservadora y coherente en sus invariantes principales; **no se demostró ningún P0**. Se demuestran **7 P1** (contradicciones internas, reglas de convergencia ausentes y ownership indefinido que TOP no puede resolver sin inventar arquitectura) y **5 P2** (precisiones y simplificaciones que no exigen rediseño). Ninguno reabre el baseline macro.

### F.2 — Hallazgos materiales

#### FBL-001 · P1 · Intents `UNKNOWN` sin regla de convergencia terminal: capital congelado indefinidamente

- **Affects:** M1.11 (Retries, Al recuperar), M1.13 (config `intent TTL` sin semántica), A-21, U-06.
- **Claim:** timeout/5xx tras iniciar el intento deja el intent `UNKNOWN` con fondos retenidos; «un 404/ausencia actual no prueba no aceptación»; nunca salt nuevo.
- **Counterexample:** intent I1 GTD (expiry +180 s) → `SEND_ATTEMPT_STARTED` durable → HTTP timeout. Reconcile: `/data/order/{hash}` 404, `/data/orders` no lo lista, `/data/trades` sin trade. Según M1.11 la ausencia no prueba nada, por lo que la reserva permanece `HELD`. Nada en M1 define cuándo `UNKNOWN` se vuelve terminal. Repetir con 3–5 timeouts en una sesión y el bankroll tiny-live completo (US$300) queda reservado sin ningún hecho externo que lo justifique; el siguiente arranque tampoco lo libera («sin visibilidad… no liberar reservas»).
- **Violated invariant:** liveness del ledger: toda reserva debe alcanzar `RELEASABLE` o `CONSUMED` en tiempo finito bajo evidencia definible ex ante.
- **Impact:** capital incorrecto por defecto (disponible artificialmente cero), rechazos por capital confundidos con ausencia de señal, operación live inviable con bankroll pequeño.
- **Evidence:** M1.11 «Timeout/red cortada/5xx genérico… → UNKNOWN, con fondos retenidos» y «un 404/ausencia actual no prueba no aceptación»; A-21 tradeoff «Fondos bloqueados en UNKNOWN»; P04 §8.3 sin Idempotency-Key HTTP; P04 §7D GTD vence 60 s antes de `expiration`, FOK/FAK sin resto abierto; P05 §10 balances ERC1155/ERC20 on-chain como hechos por bloque.
- **Minimal correction:** definir en M1.11 la regla de terminalización por evidencia, sin usar ausencia REST como prueba: un `UNKNOWN` pasa a `RESOLVED_NOT_FILLED` (reserva `RELEASABLE`) sólo cuando se cumplen todas: (a) la orden es de tipo con vencimiento propio (FOK/FAK inmediato, GTD por `expiration`) y `now_server ≥ expiration + settlement_window`; (b) lookups por hash, órdenes abiertas y trades con overlap desde antes del intento no muestran la orden ni un trade que la referencie; (c) balance collateral y saldo ERC1155 del asset a bloque confirmado coinciden con el ledger sin ese fill; (d) User WS estuvo conectado o su hueco fue cubierto por REST. GTC `UNKNOWN` no terminaliza por tiempo: exige cancel por hash exitoso o evidencia terminal. `settlement_window` y el máximo de `UNKNOWN` simultáneos que bloquean nuevos sends son parámetros `REQUIRES_OWNER` para live; el mecanismo es contrato de diseño ahora.
- **Closure test:** fixture G-11/G-12 con timeout tras aceptación real (orden visible después) → permanece `HELD` y converge a `ACK_OBSERVED`; timeout sin aceptación (nunca visible, balances intactos, expiry vencido) → `RELEASABLE` exactamente tras (a)–(d); 404 aislado sin (a)/(c) → sigue `HELD`.
- **Disposition:** `BLOCKING_BEFORE_FREEZE` (regla); valores numéricos `OWNER_DECISION` para live activation.

#### FBL-002 · P1 · Clasificación incompleta de respuestas de escritura y resubmisión `order timed out`

- **Affects:** M1.11 (Acknowledgement, Retries, Cancelación), A-21, U-04.
- **Claim:** 5xx genérico/red → `UNKNOWN`; sólo el error literal `order timed out` habilita «resubmisión del mismo intent»; cancel `canceled` libera remanente.
- **Counterexample:** (1) `POST /order` responde HTTP 425 (matching engine restart) o 429 de bucket signer, ambos ausentes de la clasificación de M1.11; TOP puede implementarlos como rechazo definitivo y liberar la reserva, mientras P04 §8.4 exige «para write ambiguo consultar estado» en 425. (2) `order timed out`: si «mismo intent» se implementa re-firmando (nuevo `timestamp` ms firmado → nuevo hash, P04 §7A), y la primera orden sí entró pese al error, existen dos órdenes vivas del mismo intent: doble exposición sin salt nuevo. (3) Cancel `canceled` recibido, reserva del remanente liberada con `size_matched` conocido localmente; llega trade tardío del mismo order hash con match previo al cancel → obligación mayor que la reserva retenida → `available` sobreestimado para el siguiente intent.
- **Violated invariant:** un intent produce como máximo un efecto externo; la reserva cubre toda obligación posible hasta terminalidad probada.
- **Impact:** doble exposición o doble gasto de bajo volumen pero real; violación de conservación en ledger.
- **Evidence:** M1.11 párrafos «Retries» y «Cancelación»; P04 §8.4 filas 425, 429, 503, `order timed out`, HTTP 500 genérico; P04 §7A `timestamp` uint256 ms es campo firmado; P04 §8.3 `POST /order` «orden firmada tiene identidad/hash determinista».
- **Minimal correction:** tabla normativa en M1.11: `DEFINITIVE_REJECT` = body JSON CLOB parseable con `success:false` y `errorMsg` no vacío, o HTTP 400/401/403 con body CLOB; `UNKNOWN` = 425, 429, 5xx, 503 sin body parseable, timeout, red cortada, body no parseable o `success:true` sin `orderID`. Resubmisión por `order timed out` exige: body JSON del envelope CLOB con `errorMsg == "order timed out"` exacto, **mismos bytes firmados y mismo hash** (jamás re-firmar), un solo reintento, ruta certificada en G-12/G-17; cualquier re-firma es un intent nuevo con nueva decisión de Risk. Liberación tras `canceled`: sólo con `GET /data/order/{hash}` en estado terminal y `size_matched` final; obligaciones por trades permanecen hasta `CONFIRMED` o `FAILED` conciliado.
- **Closure test:** fixtures G-12: 425/429/503/500 genérico/body HTML → `UNKNOWN` y reserva `HELD`; `order timed out` exacto → segundo envío con bytes idénticos y hash igual, `Duplicated` → lookup sin tercer envío; variante `upstream timed out` → `UNKNOWN`; cancel con trade tardío → reserva cubre obligación, `available` no negativo.
- **Disposition:** `BLOCKING_BEFORE_FREEZE`.

#### FBL-003 · P1 · Contradicción entre integridad DB↔journal, retención 30 d y conjunto de backup

- **Affects:** M1.6 (Crash), M1.7 (Consistencia, Retención, Backups), A-11, A-12, A-13, U-08.
- **Claim:** «referencias DB a evidencia ausente invalidan integridad»; raw no pineado se elimina a 30 días; backup = snapshot DB horario + segmentos copiados al sellar; «restore valida esos vínculos».
- **Counterexample A:** fill F (día 1) queda en DB con `capture_ref` al segmento S. Día 31 GC borra S (no pineado, ledger de cuenta se retiene «vida del proyecto»). Día 32 el arranque valida referencias: por la regla literal la integridad es inválida → o bloquea el writer de cuenta (recuperación imposible con hechos externos verdaderos) o la regla se ignora (invariante vacío). **Counterexample B:** snapshot DB a T1 registra `applied_seq=N` en el segmento activo S_k (no sellado, no copiado). Host muere en T2 < sellado. Restore en directorio limpio: DB referencia evidencia inexistente → mismo dilema; además el conjunto restaurado tiene DB **por delante** del journal, invirtiendo la frontera de crash asumida en M1.7 (journal sella primero).
- **Violated invariant:** integridad referencial definible y recovery siempre posible para hechos de cuenta.
- **Impact:** recuperación imposible o invariante ficticio; backup no restaurable según G-14.
- **Evidence:** M1.7 «Consistencia entre journal y DB», «Retención propuesta», «Backups»; A-11; A-12; G-14.
- **Minimal correction:** (1) dos clases de referencia en M1.7: `ACCOUNT_FACT` (intents, attempts, fills, reservas, observaciones de cuenta) es autoridad local reconciliable con venue/chain y su evidencia privada se retiene vida del proyecto en el storage privado ya previsto en M1.6, fuera del GC de 30 d; `RESEARCH_EVIDENCE` ausente marca proyecciones/experimentos `NOT_REPRODUCIBLE`, nunca bloquea startup ni cuenta. (2) Punto de consistencia de backup: cada snapshot DB fuerza sello del segmento activo (o copia el prefijo durable ≤ `durable_seq` con su checksum) antes de copiarse, y registra `(durable_seq, applied_seq por reducer)`; restore exige `journal_seq ≥ applied_seq` para toda clase o degrada a `RECOVER_FROM_VENUE` sólo para `ACCOUNT_FACT`. (3) Restore en host nuevo exige rotación de credencial L2 antes de cualquier lease (evita instancia antigua viva con la misma identidad).
- **Closure test:** G-14 extendido: restaurar snapshot con segmento activo perdido → cuenta recupera y reconcilia, experimentos afectados `NOT_REPRODUCIBLE`, sin bloqueo; GC simulado a día 31 → arranque limpio, integridad `PASS`, evidencia privada de cuenta intacta.
- **Disposition:** `BLOCKING_BEFORE_FREEZE`.

#### FBL-004 · P1 · Replay de decisiones no reproducible: `EvaluationContext` fuera del `revision_vector`

- **Affects:** M1.6 (Replay de decisiones entregadas), M1.8 (`EvaluationContext`), M1.10, A-09, G-07.
- **Claim:** `DeliveryFrame{run_id, ordinal, trigger, cut_seq, revision_vector, quality, virtual_time}` permite reproducir «el input exacto de la estrategia».
- **Counterexample:** en SHADOW/LIVE, `Evaluate` recibe `AccountView del modo + RiskPolicyView + DepthQuote/CostEnvelope`. `AccountView` real depende de fills/settlement externos con timing propio (no derivable del journal de mercado); `RiskPolicyView` cambia por config revision; el ledger de liquidez virtual depende de órdenes simuladas previas. Ninguno figura en `revision_vector`. Reejecutar la delivery reproduce `Detect` pero no `Evaluate` ni la decisión de Risk: mismo frame, distinto `Assessment`/sizing → G-07 no puede pasar para deliveries live/shadow y la auditoría de una decisión real es imposible.
- **Violated invariant:** determinismo del replay de decisiones entregadas sobre la evidencia capturada.
- **Impact:** falso resultado experimental, imposibilidad de auditar una orden real, G-07 inalcanzable.
- **Evidence:** M1.6 definición de `DeliveryFrame`; M1.8 comentario `EvaluationContext`; M1.9 ledger de liquidez virtual; G-07.
- **Minimal correction:** `revision_vector` incluye obligatoriamente `account_view_rev`, `risk_policy_rev`, `regime_rev`, `universe_rev`, `relationship_rev`, `liquidity_ledger_rev` (SHADOW/REPLAY) y `quote_inputs_hash`; el Coordinator publica `AccountView` como snapshot inmutable versionado (ya lo es «snapshot de cuenta» para Risk) y el descriptor lo referencia; el resultado registra `Assessment` y decisión de Risk con esas revisiones. Un descriptor con revisión de cuenta no recuperable marca la delivery `NOT_REPRODUCIBLE`, nunca reproduce con estado actual.
- **Closure test:** G-07 con corrida SHADOW: replay de deliveries iguala hashes de `Assessment`, sizing y decisión de Risk; alterar `AccountView` fuera del descriptor debe producir `NOT_REPRODUCIBLE`, no una diferencia silenciosa.
- **Disposition:** `BLOCKING_BEFORE_FREEZE`.

#### FBL-005 · P1 · Ledger virtual compartido entre estrategias contamina el scorecard por POC

- **Affects:** M1.8 (fila `SHADOW`: «cuenta virtual compartida»), M1.9 (ledger de liquidez por run), A-16, A-17.
- **Claim:** «dos estrategias no pueden reutilizar la misma profundidad en el mismo escenario como si ambas fueran primeras»; SHADOW usa cuenta virtual compartida.
- **Counterexample:** POC-S01 y POC-S02 corren en SHADOW sobre el mismo asset. S01 (admitida primero por orden determinista) consume el ask de 500 shares. S02 detecta la misma oportunidad; su `Evaluate` ve profundidad virtual cero → `REJECT`. Scorecard S02 registra señal sin fill/edge. El protocolo preregistrado de S02 concluye `NO_GO` por capacidad, cuando aislada habría llenado. El resultado depende de qué otras POCs corrían, no de la hipótesis.
- **Violated invariant:** un scorecard mide la hipótesis, no la composición accidental del portafolio de experimentos (`NO EDGE` sólo con sistema/modelo aptos).
- **Impact:** falso `NO_GO`/falso edge, north star degradado; irreproducible sin listar todas las POCs coetáneas.
- **Evidence:** M1.8 tabla de modos; M1.9 «Cada run simulado posee un ledger de liquidez virtual consumida… dos estrategias no pueden reutilizar…»; M1.14 diagnóstico `NO EDGE`.
- **Minimal correction:** default = ledger virtual de liquidez y cuenta **aislado por experimento/instancia**; modo `PORTFOLIO_SHARED` explícito en manifest, con contador `PEER_CONSUMED_DEPTH` en denominadores del scorecard y lista de peers en el manifest. El recorder ya captura ambos; no hay coste de datos.
- **Closure test:** G-10: dos fixtures idénticas en paralelo aisladas → scorecards iguales entre sí y al run individual; en `PORTFOLIO_SHARED` → diferencia explicada íntegramente por `PEER_CONSUMED_DEPTH`.
- **Disposition:** `BLOCKING_BEFORE_FREEZE` (cambio de texto/contrato; sin rediseño).

#### FBL-006 · P1 · Ejecución multi-leg live sin owner: la política de basket no tiene máquina de estados

- **Affects:** M1.8 (`ActionCandidate`), M1.9 (Baskets), M1.10 (fila Baskets), M1.11 (submit individual), A-14, A-16.
- **Claim:** el engine provee «ejecución/coste de legs», reserva todo el conjunto antes de la primera leg y «limita riesgo residual si sólo parte llena»; la estrategia no recibe callback de envío; diseño favorece submit individual.
- **Counterexample:** candidato S01 con 3 legs. Leg 1 llena, leg 2 `UNKNOWN`, leg 3 rechazada por tick change. ¿Quién decide esperar, abandonar o deshacer leg 1? La estrategia sólo puede reaccionar en `Observe(LiveExecution)` y emitir otro candidato, es decir, reimplementar la secuenciación y el unwind en cada POC (viola «una strategy no implementa… risk engine»). Execution «posee intentos de I/O, no balance» y Risk es «evaluador puro»: ningún módulo posee el estado del basket. En simulación M1.9 sí modela «condiciones de abandono», luego SHADOW y LIVE divergen de contrato.
- **Violated invariant:** un owner por estado; misma lógica en los cuatro modos; POC sólo implementa lo diferenciador.
- **Impact:** POCs S01/S02 (ambas baskets según ERC §2–3) deformarían el core o producirían legging risk no gobernado en live; resultados SHADOW no comparables con LIVE.
- **Evidence:** M1.8 «ActionCandidate contiene una o varias legs… restricciones de parcialidad y máximo riesgo residual»; M1.9 «Baskets son multi-leg no atómicos: simular orden/tiempos de legs… condiciones de abandono»; M1.10 fila Baskets; M1.11 «submit individual».
- **Minimal correction:** tipo `BasketPolicy` declarativo en `ActionCandidate` (`legs_order: PARALLEL|SEQUENTIAL`, `max_leg_skew`, `on_partial: HOLD|UNWIND_FILLED|COMPLETE_IF_BUDGET`, `max_residual_risk`, `ttl`), interpretado por una máquina de estados `BasketExecution` propiedad del Account Coordinator (estado) y ejecutada por Execution (I/O); el Simulator implementa la misma política. La estrategia sólo declara. Sin política válida → candidato rechazado. Implementación live diferida; el contrato se fija ahora.
- **Closure test:** G-10/G-12: fixture 3 legs con leg 2 `UNKNOWN` y leg 3 rechazada → `on_partial` aplicado por el engine, resultado idéntico en SHADOW y en fault-fixture live, sin código de secuenciación en la estrategia neutral de G-08.
- **Disposition:** `BLOCKING_BEFORE_FREEZE` (contrato); implementación `DEFER_TO_M2_WITH_FIXED_CONTRACT`.

#### FBL-007 · P1 · Cancelación defensiva sin audit: frontera operativa no contractual

- **Affects:** M1.11 (Kill switch operativo), M1.14, A-25.
- **Claim:** con disco lleno/DB caída se permiten cancelaciones defensivas de IDs/scope conocidos sin persistir audit; alerta operacional; el siguiente arranque fuerza reconcile.
- **Counterexample:** DB caída; cancel-all emitido; proceso reiniciado por el supervisor con disco parcialmente liberado. Nada durable indica que hubo acciones sin audit: la «alerta» es efímera y `LIVE_DISABLED/RECOVERING` es el arranque normal, no una señal de audit gap. El operador humano revisa después el ledger y no encuentra rastro del cancel; la secuencia de decisiones live queda incompleta sin marca. Además el texto no acota qué es «defensivo»: un `DELETE /orders` con IDs en memoria potencialmente stale o un cancel-all sobre scope compartido cabrían en la excepción.
- **Violated invariant:** trazabilidad degradada declarada, no silenciosa; excepción de emergencia acotada por allowlist.
- **Impact:** auditoría incompleta de acciones con credencial real; riesgo de ampliación de la excepción en implementación.
- **Evidence:** M1.11 último párrafo; A-25 tradeoff «Audit parcial en emergencia».
- **Minimal correction:** definir `DEGRADED_AUDIT` como modo explícito del Supervisor: allowlist = {`DELETE /order` por hash conocido, `DELETE /orders` por hashes conocidos, `DELETE /cancel-all` sólo si cuenta dedicada (A-23)}; cada acción se escribe en un ring buffer en memoria y en un sink secundario mínimo (stderr/syslog del servicio, ya fuera del journal) con timestamp, hashes y respuesta; flag `AUDIT_GAP{boot_id, since}` se persiste en el primer store escribible disponible (DB, journal o archivo marcador en el directorio de estado) y bloquea cualquier `ActivationLease` hasta que un reconcile completo lo cierre con firma del operador. Prohibido en este modo: nuevos orders, approvals, conversión, liberación de reservas.
- **Closure test:** drill G-13/G-14: DB inaccesible → cancel permitido, `AUDIT_GAP` presente tras reinicio, lease denegada hasta cierre explícito, ring buffer volcado al journal al recuperar storage; intento de `POST /order` en el modo → rechazado antes de firmar.
- **Disposition:** `BLOCKING_BEFORE_FREEZE`.

#### FBL-008 · P2 · Semántica del corte `C` del Frame Builder subespecificada

- **Affects:** M1.5 (Frame multiasset), M1.13 (Book shards, Frame builder), A-07.
- **Claim:** el builder «solicita a los owners un corte local `capture_seq=C` y conserva la revisión de cada book… disponible a ese corte; los shards confirman un watermark procesado (también para posiciones sin mutación)».
- **Counterexample:** shard A ya aplicó seq 1.050 cuando llega la solicitud `C=1.000`; sólo mantiene la última revisión → no puede servir la revisión ≤1.000 sin historial. Shard B, sin eventos de su asset desde 900, no sabe si «procesó hasta 1.000» salvo que observe el avance global del dispatcher. Sin especificación, TOP elige entre retención ilimitada de revisiones (memoria) o lecturas «latest» disfrazadas de corte (viola coherencia local).
- **Violated invariant:** coherencia local del frame sin retención ilimitada.
- **Impact:** implementación con memoria no acotada o frames incoherentes; no afecta capital.
- **Evidence:** M1.5 párrafo «Frame multiasset»; A-07 tradeoff «retención de revisiones».
- **Minimal correction:** fijar el contrato: el corte es **forward**: `C` se elige ≥ `dispatched_seq` actual; cada shard emite snapshot al cruzar `C` (o inmediatamente si su inbox no contiene records ≤ `C` y `dispatched_seq ≥ C`); retención por shard de revisiones acotada a `K` (config) sólo para cortes ya solicitados; si un shard ya superó `C` sin snapshot retenido, el frame es `INELIGIBLE`; el dispatcher mantiene `dispatched_seq` monotónico observable por todos los shards.
- **Closure test:** property test G-05/G-07: bajo scheduling aleatorio ningún frame contiene revisión con seq > `C` ni omite records ≤ `C`; memoria por shard ≤ `K` snapshots.
- **Disposition:** `DEFER_TO_M2_WITH_FIXED_CONTRACT`.

#### FBL-009 · P2 · Carril único de admisión: carga de research puede revocar epochs de mercado; fsync por callback evitable

- **Affects:** M1.6 (Política durable-before-publish, scheduler), M1.13 (Ingress/Capture), A-08, A-29.
- **Claim:** registros de control/delivery/resultados van al mismo journal secuencial; si la cola no admite un frame se revoca el epoch y se reconecta; el scheduler «registra durablemente el descriptor antes de invocarlo».
- **Counterexample:** 20 estrategias SCREEN generan descriptores+resultados a alta tasa; la cola acotada se llena por registros de runtime; un frame de Market WS no es admitido → epoch revocado y discontinuidad L2 causada por research, no por el mercado. Además cada callback espera un group commit aunque su resultado no tenga efecto externo.
- **Violated invariant:** research no degrada captura; latencia del hot path proporcional a efectos reales.
- **Impact:** discontinuidades autoinfligidas en datasets; latencia añadida sin beneficio.
- **Evidence:** M1.6 «Política por defecto» y «El scheduler registra durablemente el descriptor del frame antes de invocarlo»; M1.13 fila Ingress/Capture.
- **Minimal correction:** dos carriles hacia el mismo secuenciador único: `EVIDENCE` (mercado/cuenta/control de transporte) y `RUNTIME` (descriptores/resultados/control de experimentos) con presupuestos separados; saturación de `RUNTIME` pausa runs (política ya prevista para consumidores), nunca revoca epochs. Relajar a «descriptor **añadido** antes de invocar; **durable** antes de publicar resultado, feedback o intent dependiente»: la lineage se conserva porque el resultado sigue al descriptor en el journal y el intent referencia un descriptor ya durable. El Simulator no requiere `synchronous=FULL`: su estado es reconstruible por replay; puede usar checkpoints periódicos.
- **Closure test:** G-09/G-13: saturar `RUNTIME` con estrategias lentas → cero epochs revocados y cero holes de mercado; p99 receive→decision sin fsync por callback medido y documentado.
- **Disposition:** `DEFER_TO_M2_WITH_FIXED_CONTRACT`.

#### FBL-010 · P2 · Precisiones de recovery y ledger que TOP no debe inferir

- **Affects:** M1.3 (Trade/Fill), M1.7 (`applied_seq`), M1.10 (Ledger), M1.11 (Al recuperar), A-02, A-13.
- **Claim:** al recuperar se marcan `SEND_ATTEMPT_STARTED` sin resultado como `UNKNOWN`; DB confirma «`applied_seq`» en una transacción; `FillKey=(account_scope, service, trade_id, order_hash, AssetKey)`; SELL requiere tokens disponibles.
- **Counterexample:** (1) intent `PREPARED` con payload firmado persistido y sin attempt al crash: el texto no lo clasifica; el payload firmado no expira por sí solo (P03 §6) y podría enviarse después por error. (2) `applied_seq` singular con reducers Catalog/Regimes/Account independientes → un reducer lento retrasa o adelanta el checkpoint de otro. (3) `service` en `FillKey` interpretado como transporte (WS vs REST) duplica el mismo `trade.id`. (4) Estrategia B vende tokens comprados por A: elegible a nivel cuenta, atribución rota.
- **Violated invariant:** recuperación cerrada; dedup por identidad; atribución por estrategia.
- **Impact:** envío tardío de payload obsoleto, doble fill contable, atribución incorrecta; todos evitables con texto explícito.
- **Evidence:** M1.11 «Al recuperar»; M1.7 «DB confirma proyección y `applied_seq`»; M1.3 fila Trade/Fill; M1.10 «Para SELL, tokens reservados…».
- **Minimal correction:** (1) `PREPARED` sin `SEND_ATTEMPT_STARTED` al arranque → `VOID` + reserva `RELEASABLE` + payload marcado no enviable; el gateway sólo envía payloads cuyo intent esté en `SEND_ATTEMPT_STARTED` del boot actual. (2) `applied_seq` por reducer/owner. (3) `service` = namespace emisor (`CLOB`); WS y REST del CLOB comparten clave; Data v2 nunca produce `FillKey`. (4) Elegibilidad SELL usa inventario atribuido a la estrategia; conciliación chain usa inventario de cuenta; transferencias entre estrategias son asiento explícito.
- **Closure test:** G-02/G-11/G-12 con estos cuatro casos como fixtures negativas.
- **Disposition:** `DEFER_TO_M2_WITH_FIXED_CONTRACT`.

#### FBL-011 · P2 · Seguridad in-process: controles baratos no enumerados

- **Affects:** M1.6 (redacción), M1.8 (aislamiento), M1.14, A-15, U-10, G-15.
- **Claim:** código de estrategia confiable; API sin secretos; redacción de auth antes del journal; imports verificados en M2.
- **Counterexample:** el DTO `order` lleva `owner` = API key (P04 §7C) y el body se captura como «solicitud»; sin listarlo en la política de redacción, el identificador de credencial termina en journal/logs. Una estrategia con `import "unsafe"` o `reflect` lee memoria del signer sin violar ningún puerto; la revisión humana es el único control.
- **Violated invariant:** secretos e identificadores de credencial fuera del journal; aislamiento verificado mecánicamente en la medida posible.
- **Impact:** fuga de identificador de credencial; ninguna pérdida directa de capital.
- **Evidence:** M1.6 «redacción tiene versión y lista de campos»; M1.8 «Go en un proceso no ofrece sandbox»; P04 §7C `owner` es API key.
- **Minimal correction:** añadir `owner`, `signature` y headers `POLY_*` a la lista de redacción; G-15 incluye gate de imports para paquetes de estrategia (prohibidos `unsafe`, `reflect`, `os/exec`, `net`, `syscall`, `plugin`) y prohibición de goroutines propias por lint; opcional sin rediseño: Credentials/Signing detrás de su puerto ya definido puede moverse a proceso separado más adelante (`IMPLEMENT LATER`), no requerido para MVP.
- **Closure test:** G-15: fixture con `import "unsafe"` en estrategia → build/gate falla; journal de captura de `POST /order` no contiene `owner` ni `signature`.
- **Disposition:** `DEFER_TO_M2_WITH_FIXED_CONTRACT`.

#### FBL-012 · P2 · `fee_rate_bps` observado por trade no se usa como evidencia de régimen

- **Affects:** M1.4 (Constraints), M1.10 (Fees dinámicas), A-18, U-02.
- **Claim:** fees se conocen por REST (`/fee-rate`, market-info) con `known-at` de polling; simulación usa el régimen conocido a la fecha.
- **Counterexample:** cambio de fee en t0; próximo poll en t1 = t0+10 min. Replay simula fills en (t0,t1) con fee antigua; en realidad el matching cobró la nueva. Scorecard sobreestima edge neto en ese intervalo y nadie lo detecta, aunque `last_trade_price` (P05 §9.2) y `trade` User WS (P05 §9.3) llevan `fee_rate_bps` con resolución ms.
- **Violated invariant:** economics sobre régimen efectivo observable, no sólo sobre polling.
- **Impact:** falso edge acotado; calibración de `FeeResolver` sin la mejor evidencia disponible.
- **Evidence:** P05 §9.2 fila `last_trade_price`; P05 §9.3 fila `trade`; M1.10 «Fees dinámicas».
- **Minimal correction:** Regimes ingiere `fee_rate_bps` de `last_trade_price` y de trades propios como observación de régimen (`source=trade_observed`) con `source_time`; discrepancia con el régimen vigente marca `REGIME_SUSPECT` y el Simulator usa la fee observada más reciente ≤ t para trades en ese asset; scorecard reporta `fee_regime_uncertain_interval`.
- **Closure test:** G-10: fixture con cambio de fee entre polls → coste simulado usa fee observada por trade y el intervalo queda etiquetado.
- **Disposition:** `DEFER_TO_M2_WITH_FIXED_CONTRACT`.

### F.3 — Invariantes auditadas sin defecto demostrado (PASS razonado)

| Área | Escenario atacado | Por qué resiste (referencia) |
|---|---|---|
| Books | Merge REST+deltas WS; delta de epoch previo tras nuevo snapshot; overflow con calidad elegible | Namespaces separados, fencing por conexión/epoch, revocación fuera de la cola saturada (M1.5, M1.6, A-05); coherente con P05 §9.2/9.5 y P10 §24A |
| Books | Tick/fee/rules cambian tras evaluar | Invalidación de constraints/candidatos y revalidación antes de intent y de envío; race posterior reconocida como residual (M1.5, M1.10) |
| Frames | Shard lento bloquea todo; `C` espera su propio delivery | Deadline por run y `C` fijado antes del descriptor (M1.5, M1.6); semántica pendiente sólo en FBL-008 |
| Journal | Frame publicado con evidencia no durable | Consumo sólo ≤ `durable_seq`; frame ≤ `C` ≤ `durable_seq` (M1.6) |
| Journal→DB | Fill reprocesado tras crash entre journal y DB | Reproceso desde `applied_seq+1` con `FillKey` única; sin dependencia circular (M1.7, A-13); precisión en FBL-010 |
| Intent | Crash entre reserva, firma, attempt y envío | Orden reserva→payload→`SEND_ATTEMPT_STARTED` durable→un solo write; nada se envía antes del marcador (M1.11); VOID explícito en FBL-010 |
| Cuenta | Fills concurrentes con cancel; múltiples maker propias; updates duplicados/fuera de orden; matched sin settlement; transferencia externa | Ejes de estado separados, `maker_orders[].order_id`, quarantine ante contradicción, `UNATTRIBUTED` bloquea presupuesto (M1.11, A-22) |
| Cuenta | Reorg; balance discrepante | `MINED≠finality`, profundidad configurable, discrepancia congela exposición (M1.11, U-06) |
| Cuenta | Reinicio con GTC/GTD abiertas; cancel-all sobre scope incompleto | Arranque `LIVE_DISABLED`, cancel de remanente, sin dead-man asumido, cuenta dedicada (A-23, A-24); coherente con P04 §8.3 y P07 §18 |
| Seguridad | Alcanzar signer por Strategy API, config, adapters, recovery, cambio de perfil, lease ajena/expirada | Allowlist cerrada, operaciones tipadas sin `target+data`, lease ligada a build/config/cuenta verificada por send, recovery cancel-only (M1.1, M1.12, M1.14, G-15) |
| Disabled | Conversión CTF/v2, backfill L2, `deferExec=true`, Builder, Combo/RFQ | Sin handler, sin calldata, `LIVE_ENABLED` no los levanta (M1.1, A-27, A-35); coherente con P10 §24B |
| Replay | Scheduling, maps, timers, coalescing, metadata tardía, snapshots perdidos | Reducers single-owner, orden canónico, timers/coalescing registrados, `known-at`, holes explícitos (M1.6, M1.8, A-09); excepción sólo FBL-004/005 |
| Diagnóstico | `NO EDGE` desde pérdida de datos | Cinco diagnósticos coexistentes y coverage en denominadores (M1.9, M1.14, A-32) |
| Discovery | Keyset Gamma vs CLOB (§25.2 vs inventario) | Registrado por ASTRA como U-03 con fallback offset capturado; no se resuelve en este pack |

### F.4 — Freeze blockers

| Finding | Sev | Corrección mínima que ASTRA-2 debe integrar | Test de cierre |
|---|---|---|---|
| FBL-001 | P1 | Regla de terminalización de `UNKNOWN` por evidencia (a)–(d); GTC excluido del cierre por tiempo | G-11/G-12 fixtures aceptación tardía vs nunca aceptada |
| FBL-002 | P1 | Tabla `DEFINITIVE_REJECT`/`UNKNOWN`; resubmisión sólo bytes idénticos; liberación tras `canceled` con `size_matched` final | G-12 fixtures 425/429/503/500/HTML/`order timed out`/cancel con trade tardío |
| FBL-003 | P1 | Clases `ACCOUNT_FACT`/`RESEARCH_EVIDENCE`; seal-then-snapshot; rotación de credencial en restore | G-14 extendido con segmento activo perdido y GC día 31 |
| FBL-004 | P1 | `revision_vector` con account/risk/regime/universe/relationship/liquidity + `quote_inputs_hash`; `NOT_REPRODUCIBLE` explícito | G-07 sobre corrida SHADOW |
| FBL-005 | P1 | Ledger virtual aislado por defecto; `PORTFOLIO_SHARED` explícito con `PEER_CONSUMED_DEPTH` | G-10 pares idénticos aislados vs compartidos |
| FBL-006 | P1 | `BasketPolicy` declarativo + `BasketExecution` owner Coordinator/Execution; misma política en Simulator | G-10/G-12 basket 3 legs con `UNKNOWN` y rechazo |
| FBL-007 | P1 | Modo `DEGRADED_AUDIT` con allowlist, sink secundario, flag `AUDIT_GAP` persistido y bloqueo de lease | Drill G-13/G-14 con DB inaccesible |

### F.5 — Decisiones del owner

**Necesarias para `M1 DESIGN FREEZE`:**

- `OD-1` — Aceptar el modelo de confianza in-process (A-15/U-10): estrategias son código revisado; sin sandbox de proceso en MVP; Credentials permanece como puerto que puede externalizarse después sin rediseño (FBL-011). Rechazarlo obliga a rediseñar el runtime antes de M2.
- `OD-2` — Aprobar la partición de alcance `FOUNDATIONAL NOW` / `IMPLEMENT LATER WITHOUT REDESIGN` de F.7, que define lo que TOP planifica en M2 y lo que queda como contrato con adapter sin permiso.
- `OD-3` — Retener evidencia privada de cuenta (`ACCOUNT_FACT`) durante la vida del proyecto fuera del GC de 30 d (FBL-003); coste de storage marginal frente a raw de mercado.

**Necesarias después, para `LIVE ACTIVATION` (pueden permanecer deshabilitadas hoy):** A-06 riesgo residual de book; A-20 caps/worst-loss/reparto de bankroll; A-23 wallet/cuenta dedicada y perfil; A-24 GTC vs GTD/FOK/FAK; parámetros de FBL-001 (`settlement_window`, máximo de `UNKNOWN` simultáneos); profundidad de confirmación (U-06); A-11/A-12 retención de raw no pineado, destino cifrado, RPO/RTO y canal de alertas (U-08).

### F.6 — Gates diferidos para TOP/NORMAL (verificables sin inventar arquitectura; ninguno ejecutado)

- `G-05b` property test del corte forward y retención `K` (FBL-008).
- `G-06b` consistencia del conjunto de backup: seal-then-snapshot y `journal_seq ≥ applied_seq` por reducer (FBL-003).
- `G-07b` replay de deliveries SHADOW con `revision_vector` completo y detección `NOT_REPRODUCIBLE` (FBL-004).
- `G-09b` saturación del carril `RUNTIME` sin epochs revocados; medición de latencia sin fsync por callback (FBL-009).
- `G-10b` ledger aislado vs `PORTFOLIO_SHARED`; fee observada por trade en simulación (FBL-005, FBL-012).
- `G-11b` terminalización de `UNKNOWN` con evidencia chain/REST y GTC excluido (FBL-001).
- `G-12b` tabla de clasificación de writes y resubmisión bytes-idénticos; `VOID` de `PREPARED` (FBL-002, FBL-010).
- `G-13b` drill `DEGRADED_AUDIT` con `AUDIT_GAP` y lease bloqueada (FBL-007).
- `G-15b` gate de imports de estrategia y redacción de `owner`/`signature`/`POLY_*` (FBL-011).

### F.7 — Alcance: FOUNDATIONAL NOW vs IMPLEMENT LATER WITHOUT REDESIGN

| FOUNDATIONAL NOW (M2–M4 sin live) | IMPLEMENT LATER WITHOUT REDESIGN (contrato fijo, adapter sin permiso o ausente) |
|---|---|
| Capture journal durable-before-publish, dos carriles, manifests, crash recovery de prefijo | Compresión de segmentos, encadenado de hashes entre segmentos, GC/pins automatizados |
| Dominio/tipos nominales/decimal exacto; Catalog known-at; Regimes; Book shards; Frame Builder con corte forward | Sports WS y cualquier adapter externo concreto; Protocol-v2 codecs |
| Strategy API completa y fixture neutral G-08; SCREEN/REPLAY/SHADOW | Perfil LIVE, `ActivationLease` operativo, Execution HTTP/User WS, Reconciler chain/RPC, cifrado de payloads firmados |
| Account Coordinator ledger + reservas + `BasketPolicy` + property tests G-02 (usado por Simulator y por live futuro) | Backups fuera del host, restore medido, rotación de credenciales (contrato en FBL-003) |
| Simulator con ledger de liquidez aislado, optimistic/base/stress, multi-leg | Modelo maker de queue calibrado (etiquetado `UNCALIBRATED` mientras falte) |
| SQLite WAL FULL para cuenta/metadata; scorecards y datasets derivados con manifest/lineage (formato inicial libre: SQLite/JSONL) | Exportación Parquet particionada; endpoint admin HTTP autenticado (CLI primero); alertas externas |
| Observabilidad de los cinco diagnósticos, readiness por capability, métricas de pipeline | Tracing completo de transiciones live; dashboards |

Ningún elemento de la columna derecha altera puertos, ownership, replay ni el Strategy API definidos en M1; sólo agrega implementaciones detrás de contratos ya fijados. Las 35 decisiones y 19 gates no se reducen; TOP debe tratar G-16…G-19 como mandato separado posterior (ya previsto en M1.15).

### F.8 — Handoff cerrado para ASTRA-2

**Orden de reconciliación por dependencia:**

1. FBL-003 (clases de integridad, consistencia de backup, retención privada) → fija las fronteras de stores que usan los siguientes.
2. FBL-010 (VOID de `PREPARED`, `applied_seq` por reducer, `FillKey.service`, inventario atribuido) → precisa el ledger.
3. FBL-001 y FBL-002 (terminalización `UNKNOWN`, clasificación de writes, resubmisión bytes-idénticos, liberación tras cancel) → cierran el ciclo de intent sobre 1–2.
4. FBL-007 (`DEGRADED_AUDIT`) → excepción acotada sobre el ciclo cerrado.
5. FBL-004 (`revision_vector` completo) y FBL-009 (carriles, durabilidad del descriptor) → contrato de delivery/replay.
6. FBL-006 (`BasketPolicy`/`BasketExecution`) y FBL-005 (ledger aislado por defecto) → contrato Strategy API/Simulator.
7. FBL-008, FBL-011, FBL-012 → precisiones M1.5/M1.14/M1.10.
8. Actualizar M1.16 (nuevas filas o enmiendas de A-02, A-07, A-08, A-09, A-11, A-12, A-13, A-16, A-21, A-25), M1.17 (U-06/U-08 con parámetros de FBL-001/003) y M1.15 (gates `*b` de F.6).

**Criterio de aceptación de la reconciliación:** cada FBL-001…007 tiene texto normativo integrado en la sección afectada, fila en M1.16 y test de cierre en M1.15; ningún finding queda como «pendiente vago»; las decisiones OD-1…OD-3 quedan registradas como `REQUIRES_OWNER` con su impacto explícito; no se introduce ninguna capability deshabilitada por M0; M1.0–M1.17 originales conservan autoría con enmiendas marcadas. Donde FABLE ofreció dos soluciones, la recomendación técnica es: FBL-009 → descriptor añadido antes de invocar y durable antes de publicar resultado/intent (menor latencia, misma lineage; la alternativa «durable antes de invocar» es válida si la medición de G-09b muestra coste despreciable); FBL-011 → signer in-process con gate de imports en MVP (la alternativa de proceso separado queda como evolución detrás del mismo puerto). La elección final se registra en M1.16, sin congelarla por cuenta de FABLE.

### F.9 — Estado

`M1_FABLE_CHALLENGE_COMPLETE` · Resultado: `MATERIAL_FINDINGS_REQUIRE_RECONCILIATION` · P0: 0 · P1: 7 · P2: 5. No se declara `M1_DESIGN_FROZEN`. **NEXT: ASTRA-2 reconcile** conforme a F.8; el owner revisa OD-1…OD-3 antes del freeze.

## M1 — ASTRA-2 Reconciliation

**Estado:** `M1_RECONCILED_PENDING_OWNER_REVIEW` · 2026-09-17. Una pasada siguiendo F.8; sin implementación ni M2. F.1–F.9 permanece como evidencia original, no se altera su recomendación histórica. M0 DESIGN_READY permanece cerrado; no se habilita ninguna ruta live.

| Finding | Resolución | Verificación del defecto / ajuste mínimo y riesgo evitado | Ubicación normativa / cierre |
|---|---|---|---|
| FBL-001 | MODIFIED_AND_INTEGRATED | Retención sin convergencia operacional demostrada. Expiry+ausencia+balances iguales admite match pendiente no visible; no prueba terminalidad. UNKNOWN conserva exposición y escala, sin liberar por timeout | M1.11; A-21/22, U-06; G-11b |
| FBL-002 | MODIFIED_AND_INTEGRATED | HTTP/re-firma/cancel tardío sí crean riesgo. JSON genérico y hash idéntico no bastan; classifier por operación, sin resubmit automático, obligaciones de fills separadas del remanente | M1.11; A-21/22, U-04; G-12b |
| FBL-003 | MODIFIED_AND_INTEGRATED | GC/segmento activo pueden romper referencias. Clases privadas/research, barrera de backup y restore local obligatorio; pérdida requerida nunca recibe PASS ni recuperación garantizada por venue | M1.6–7/15; A-11/12/13, U-08; G-06b/G-14, G-14b posterior |
| FBL-004 | ACCEPTED_AND_INTEGRATED | Frame solo no reconstruye Evaluate/Risk. Inputs por fase recuperables/pineados, snapshots y NOT_REPRODUCIBLE sin estado actual sustituto | M1.6/8/10; A-09; G-07b |
| FBL-005 | ACCEPTED_AND_INTEGRATED | Consumo virtual accidental contamina POC. Cuenta/liquidez aisladas, portfolio explícito y competencia atribuida | M1.8–10; A-16/17/20; G-10b |
| FBL-006 | MODIFIED_AND_INTEGRATED | Basket carecía de owner. Coordinator/reducer común y política secuencial; se elimina permiso implícito de unwind, compensación exige autorización/budget/Risk nuevos | M1.2/8–11; A-14/16; G-10c/G-12b |
| FBL-007 | MODIFIED_AND_INTEGRATED | Emergencia podía perder rastro/scope. Allowlist, boot abierto, sink/marker best-effort y reconcile; no promesa de persistencia con todos los dispositivos caídos | M1.11/14; A-25/31; G-13b/G-14 |
| FBL-008 | MODIFIED_AND_INTEGRATED | Shard adelantado/sin eventos no sirve corte pasado. Barrera atómica FIFO y K+bytes; watermark global aislado no prueba inbox procesado | M1.3/5/13; A-07; G-05b |
| FBL-009 | ACCEPTED_AND_INTEGRATED | Runtime puede saturar captura. Carriles/presupuestos y append antes de callback, durabilidad antes de efectos; no rebajar SQLite real ni prometer aislamiento físico | M1.2/6/13; A-08/29; G-09b |
| FBL-010 | ACCEPTED_AND_INTEGRATED | Cuatro ambigüedades cerradas: VOID condicionado a no-send probado, cursors por owner, FillKey por servicio y subledger atribuido | M1.3/7/10/11; A-02/13; G-02b/G-12b |
| FBL-011 | ACCEPTED_AND_INTEGRATED | Credencial en owner/imports peligrosos son rutas reales. Redacción y gates automáticos con límites explícitos, estrategias confiables sujetas OD-1 | M1.6/8/14; A-15, U-10; G-15b |
| FBL-012 | MODIFIED_AND_INTEGRATED | Polling puede ignorar evidencia de fee. Se incorpora trade observado; extrapolar su bps a otro rol/trade/período carece de prueba y queda prohibido | M1.4/10; A-18, U-02; G-10b |

Ningún finding se rechaza íntegramente: cinco aceptados y siete modificados. Los contraejemplos a correcciones inseguras se registran en M1.7/10/11; no se desecha el defecto original.

| Decisión owner | Propuesta concreta (`REQUIRES_OWNER`, ninguna aprobada) | Consecuencia de aceptar / rechazar |
|---|---|---|
| OD-1 | Estrategias confiables/revisadas in-process con controles G-15b; puerto de Credentials externalizable después | Aceptar mantiene monolito con riesgo compartido de memoria/CPU. Rechazar exige definir aislamiento por proceso antes de M2; separar signer solo no resuelve aislamiento de estrategias |
| OD-2 | Aprobar partición M1.15 basada en F.7, con restore local consistente y medido ahora; DR/adapters live y optimizaciones después | Aceptar permite certificar núcleo durable sin capital. Rechazar requiere acordar otra partición y ajustar gates antes de M2, no imponer silenciosamente implementaciones diferidas |
| OD-3 | Retener ACCOUNT_FACT y evidencia privada necesaria durante vida del proyecto, fuera del GC raw, con ACL y custodia previstas | Aceptar preserva recovery/auditoría con coste de storage/privacidad. Rechazar exige una frontera de retención/recuperación alternativa verificable antes de captar cuenta real; no autoriza borrar ni declarar íntegro lo irrecuperable; research público puede continuar |

**Capabilities deshabilitadas:** LIVE/order gateway/leases operativos, basket live/PARALLEL y compensación automática, resubmisión automática, CTF position ops inicialmente, conversiones NegRisk CTF/v2 y codecs v2 no verificados, backfill L2, deferExec=true, Builder opcional, Session Keys/auto-wallet/auto-approvals. Combo/RFQ/Exchange-v3 y Bridge/funding automático siguen fuera del MVP inicial; M1.1/M1.12 conservan la allowlist.

**Gates diferidos sin ejecutar:** todos los tests G-01…G-19 y extensiones están NOT_RUN. Para M4 se ejecutarán G-01…G-15 y G-02b/05b/06b/07b/09b/10b/10c/11b/12b/13b/15b en alcance no-live; G-14b fuera del host y G-16…G-19 reales requieren fase/mandato posterior. Claims de integridad/DR/live nunca se infieren de esta revisión documental.

**Pendientes materiales:** aprobación OD-1…OD-3; implementación y pruebas futuras. Exclusivos de activación live: caps/worst-loss/lock/reparto, wallet/scope, políticas GTC/GTD y book residual, deadlines/escalación/finality, contratos específicos de classifier, costes verificados, destino/claves/RPO/RTO/alertas. Sin configurar hoy toda la operación financiera; esos pendientes conservan live bloqueado y no reabren M0 ni el contrato read-only/shadow.

**Handoff:** Owner + manager design review de OD-1…OD-3, partición/gates M1.15 y disposición de findings. La propuesta está reconciliada para aprobar o ajustar explícitamente; no se declara DESIGN_FROZEN. El entregable es este archivo local; FABLE no necesita otro challenge para completar esta reconciliación.

**Validación documental local:** se conservaron las secciones originales M1.0–M1.17 y F.1–F.9. Comparación SHA-256 verificó intactos el contenido anterior a M1 (incluido M0) y los bytes originales del challenge FABLE. Doce disposiciones con ubicación normativa/gate, A/U enmendadas y partición M4 explícita; no hubo tests físicos, cambios al TPM ni activación de capabilities. Este registro corresponde a edición documental, no certificación del engine.

## M1 — ASTRA-3 Owner Decisions + Final Design Freeze

**Estado vigente:** `M1_DESIGN_FROZEN` · **Autor:** ASTRA-3 · **Fecha:** 2026-09-17 · **Final consistency audit:** `PASSED` documental. **M1 cerrado.** Secuencia completada: ASTRA-1 proposal → FABLE challenge (FBL-001…012) → ASTRA-2 reconciliation → OD-1/OD-2/OD-3 approved por mandato del owner → auditoría final acotada y arquitectura frozen. No hubo otra ronda adversarial, Deep Research, implementación ni plan M2.

| Owner decision | Estado | Contrato aprobado / registro afectado |
|---|---|---|
| OD-1 | APPROVED | Go confiable/revisado in-process, sin sandbox ni plugins arbitrarios; imports/lint/API restringida/ausencia de secrets como defense-in-depth. Credentials/Signing externalizable sin cambiar dominio ni Strategy API; sin proceso extra ahora. A-15/U-10; M1.8/14; G-15b |
| OD-2 | APPROVED | Partición M1.15: núcleo read-only/replay/shadow certificable M2–M4 y backup/restore local consistente/medido foundational; implementaciones live/optional y DR off-host diferidas detrás de contratos definidos. A-10/A-12/A-32/A-34; M1.2/6/7/15 |
| OD-3 | APPROVED | ACCOUNT_FACT y evidencia privada mínima durante vida del proyecto, ACL mínima/cifrado aplicable, sin claves privadas/HMAC secrets/secretos reutilizables; lineage de cuenta/recovery y archivo sin pérdida semántica. Sin GC de raw ni TTL accidental; eliminación requiere política explícita de cierre/archivo. A-11/A-12/A-13/U-08; M1.6–7; G-14/G-15b |

**Contradicciones materiales corregidas:** (1) M1.2 aún atribuía estado de órdenes/fills simulados al Simulator mientras la reconciliación asignaba ese ledger/BasketExecution al Coordinator; se fijó el único writer por namespace y se distinguieron estado de I/O, observaciones pendientes, manifests y coordinación de backup de sus respectivos owners. (2) La prohibición transitiva literal de imports en G-15b podía rechazar los internals de Go necesarios para la propia Strategy API; M1.14/G-15b ahora delimita la base confiable revisada/versionada y prueba tanto el caso neutral permitido como acceso directo/indirecto prohibido. No se agrega aislamiento ni se amplía la API.

**Alineaciones finales por aprobación:** retención privada y custodia separadas del artefacto firmado operativo futuro; TTL raw/derivados sigue propuesto, sin GC inicial; Parquet/compresión/tracing live y restores remotos dejan de aparecer como dependencias iniciales en las secciones normativas. Restore local G-06b/G-14 permanece obligatorio en M4. A/U, estado/tareas y handoff ya reflejan las aprobaciones; cifras y políticas exclusivas de live no se congelan.

| Eje auditado | Resultado documental y evidencia normativa | Gate físico observable (NOT_RUN) |
|---|---|---|
| Ownership | PASSED: Catalog, Books, Capture, Runtime, Coordinator/BasketExecution, Simulator y observaciones Reconciler tienen dueño único; M1.2/3/7/9/11/13 | G-02b/G-08/G-10b/G-10c y G-06b para barrera/bundle |
| Persistencia / doce findings | PASSED: journal → durable_seq → applied_seq por owner → frame → decisión; reserva+intent/outbox → attempt durable → único I/O → reconciliación. ASTRA-2 resolvió FBL-001…012 y M1.15 conserva cierre observable para cada uno; recomendaciones históricas incompatibles no gobiernan | G-02b/G-05b/G-06b/G-09b/G-11b/G-12b/G-13b/G-14; resto en filas siguientes |
| Replay | PASSED: observación, delivery, decision audit y contrafactual separados; inputs efectivos por fase recuperables, sin latest ante revisión faltante; M1.5–6/8–10 | G-07/G-07b/G-10b (FBL-004/005/012) |
| Strategies | PASSED: discovery/WS/books/recorder/replay/economics/account/risk/basket infrastructure/observability comunes; Sports/NegRisk conservan lógica particular; M1.4/8–12 | G-08/G-10c (FBL-006) |
| Scope | PASSED: FOUNDATIONAL NOW no exige adapters live, credenciales reales ni infraestructura remota; componentes posteriores conservan ownership/dominio/API/persistencia y gates; M1.15 | G-01…G-15 y extensiones no-live, incluyendo G-06b/G-14 |
| Security | PASSED: disabled fail-closed, Strategy sin signer/red/ejecución vía API, sin calldata arbitrario ni retries ambiguos; OD aprobadas no otorgan lease ni capacidad live; M1.1/8/11/12/14 | G-12b/G-13b/G-15/G-15b (FBL-002/007/011) |
| Gates / freeze | PASSED: contratos arquitectónicos FROZEN con pruebas y condiciones de fallo definidas; BLOCKED_BY_PROTOCOL preservado y políticas live DEFERRED_LIVE_DECISION. Diseño escrito no equivale a prueba pasada | Todos NOT_RUN; G-14b/G-16…G-19 en alcance IMPLEMENT LATER |

**Blockers materiales restantes:** ninguno para M1/M2. **Gates físicos:** todos `NOT_RUN`, sin PASS físico. **Live:** `NOT_CERTIFIED / LIVE_DISABLED`. Capabilities live/optional de M1.1/12 permanecen disabled o fuera de la implementación inicial; OD-1/2/3 no cambian esos permisos. Los límites financieros, wallet/account real, finality/allowances, credenciales, GTC/residual books, settlement/UNKNOWN y políticas de DR off-host/alertas esperan sus gates de activación posteriores.

**Handoff inequívoco — NEXT: M2 — TOP IMPLEMENTATION PLAN.** Inputs exclusivos: este proyecto frozen y Technical Platform Map; Edge Research Consolidado sólo cuando una decisión de implementación necesite requirements transversales. TOP transforma FOUNDATIONAL NOW en dependency order, slices, packages/files permitidos, schemas/storage setup, tests/gates, failure/recovery y definition of done. No rediseña. Una contradicción arquitectónica material se devuelve al manager como `BLOCKED — DESIGN ISSUE`; no se resuelve inventando arquitectura ni activando capacidades diferidas. El plan se escribirá en este mismo proyecto durante M2, no en este shot.

**Persistencia y trazabilidad:** sólo esta nota fue editada; F.1–F.9 y el registro completo ASTRA-2 conservan los mismos bytes del baseline local, verificados por SHA-256. La propuesta ASTRA-1 mantiene autoría, estructura, alternativas/riesgos e historial, con correcciones normativas identificadas. No se modificó el Technical Platform Map ni se usó GitHub/sincronización remota como autoridad. Este cierre es el registro de cambio local del mandato ASTRA-3.

## M2 — TOP Implementation Plan

**Estado:** `M2_FROZEN — S01 IMPLEMENTADO` · **Autor:** TOP · **Fecha:** 2026-09-17. Este bloque transforma la partición `FOUNDATIONAL NOW` de M1.15 en un plan de implementación ordenado, verificable y ejecutable por agentes NORMAL. No rediseña: cada contrato citado ya está FROZEN en M1.1–M1.17 y este plan sólo decide estructura de paquetes Go, orden de slices, tests y verificación física. Freeze y arranque de S01 por mandato del owner (2026-09-17); las decisiones operativas citadas (repo local, Go 1.27) quedan resueltas en M2.1/M2.9. Gates físicos: G-01/G-15b-base PASS con evidencia física; el resto `NOT_RUN`; live sigue `NOT_CERTIFIED / LIVE_DISABLED`; ninguna capability live queda habilitada.

### M2.0 — Baseline, autoridad y alcance del plan

| Fuente | Uso en este plan |
|---|---|
| Este archivo, contenido previo a M2 | Autoridad principal: D-001…D-014, M1.1–M1.17, A-01…A-35, U-01…U-10, G-01…G-19, partición FOUNDATIONAL NOW de M1.15 |
| [[Polymarket — Technical Platform Map — synced 2026-09-17]] y sus partes P01…P11 (notación de M1.0) | Contratos wire citados por slice (schemas, endpoints, units, rate limits, recovery); consulta selectiva por parte de NORMAL |
| [[Polymarket — Edge Research Consolidado 2026-09-16]] | Sólo como requisito transversal de consumidores (baskets/relaciones); ya absorbido en M1.4/M1.9; NORMAL no lo necesita para estos slices |

**Alcance = FOUNDATIONAL NOW exclusivamente** (partición M1.15, OD-2 APPROVED). Prohibido planificar implementación de: órdenes live reales, ActivationLease operativo de trading, wallet/signing productivo, User WS de ejecución (sólo fixture/interfaz si un test lo exige), writes on-chain, CTF position ops con ejecutor, conversión NegRisk CTF/v2, codecs Protocol-v2, `deferExec=true`, Builder modes, Session Keys, auto-wallet/auto-approvals, Combo/RFQ, Bridge/funding, estrategias Sports/NegRisk reales, DR off-host, dashboards/UI, Kubernetes, Kafka/Flink, microservicios. Las interfaces frozen para live futuro se representan como contratos + stubs que retornan `DISABLED` (deny-all) verificados por tests negativos; prohibido crear fake implementations que simulen éxito. Toda la evidencia privada de cuenta usada en tests es sintética (M1.15).

**Escalamiento:** si un agente (TOP o NORMAL) demuestra una contradicción arquitectónica material entre este plan y M1 frozen, detiene el slice afectado con `BLOCKED — DESIGN ISSUE` hacia el manager; no improvisa, no inventa ownership ni activa capabilities diferidas. Decisiones operativas permitidas a M2 (driver SQLite, librería decimal, librerías auxiliares, versiones, ubicación local del repo) se registran en M2.9 y son reversibles sin tocar dominio.

### M2.1 — Estructura de paquetes Go (decisión operativa M2)

**Repo:** `xKoRx/polymarket-engine` (nombre acordado en M0; la creación del repo es paso posterior separado). **Ubicación local del clone: `~/go/src/github.com/xKoRx/polymarket-engine`** — resuelta al iniciar S01 (checkout existente con remote `origin` y commit inicial; fuera del vault, conforme a la regla de repos externos de Agents-OS). Layout baseline (sin monorepo grande):

```text
go.mod                          module github.com/xKoRx/polymarket-engine
cmd/engine/                     composition root + CLI local (mismo binario)
internal/
  foundation/  config/  protocol/  capture/  persist/
  catalog/  regimes/  transport/  books/  frames/
  strategy/  economics/  simulator/  account/  risk/
  experiment/  replay/  obs/  supervisor/  archtest/
migrations/                     SQLite embebido, forward-only, rangos por slice
testdata/                       fixtures versionadas + evidencia de gates + property-failures
```

| Paquete | Responsabilidad | Owns | Puede depender de | No debe depender de | Contratos públicos | Persistencia | Concurrencia |
|---|---|---|---|---|---|---|---|
| `cmd/engine` | Composition root y CLI local (run/screen/record/replay/backup/restore/verify/certify) | wiring exclusivo de puertos/adapters; sin dominio propio | todos los `internal/` sólo para construir | nadie lo importa | subcomandos CLI | ninguna (delega) | arranca/detiene Supervisor |
| `internal/foundation` | Primitivas transversales: IDs nominales, `RevisionRef`, `AssetKey`, `ConditionRef`, decimal exacto `coefficient+scale`, unidades (`Price/Shares/CollateralAmount/BasisPoints/FeeCoefficient`), `Clock` wall+mono, error taxonomy, capability registry fail-closed, `ExecutionMode`/`ActivationLease` (contrato, no constructor) | tipos value inmutables y sus invariants | nada interno | todo lo demás (es la base) | tipos, errores, registry API | ninguna | tipos value; sin goroutines |
| `internal/config` | Schema versionado, carga/validación estricta, `config_revision` hash | schema de configuración | foundation | paquetes de dominio | `Config` validada + revision | archivo config versionado | lectura única al boot |
| `internal/protocol` | DTOs y parsers wire por superficie (`gamma`, `clobrest`, `marketws`, `datav2`), version identity, redaction schema, unión `ProtocolContext` CTF/V2/UNKNOWN | interpretación wire→tipos | foundation | transporte I/O, dominio, persistencia | `Parse(surface, bytes)` total; listas de redacción; version identity | fixtures versionadas en `testdata/` | parsers puros, sin estado |
| `internal/persist` | Framework SQLite: open WAL synchronous FULL, migraciones embebidas forward-only, single writer, `applied_seq` por reducer/namespace, outbox pattern, chequeo `journal_seq ≥ applied_seq` | runner de migraciones, `reducer_cursors`, convención de cursores | foundation | tablas concretas de owners (las crea cada slice) | Open/Migrate/Writer/Cursor/Outbox API | `schema_migrations`, `reducer_cursors` (0001–0009) | un writer goroutine serial, transacciones breves |
| `internal/capture` | Admisión durable-before-publish, journal segmentado con CRC y footer, `capture_seq`/`durable_seq`, carriles EVIDENCE/RUNTIME con cuotas, recovery de prefijo, manifests/bundle, integridad por clase (`ACCOUNT_FACT`/`RESEARCH_EVIDENCE`), redacción aplicada | bytes/manifests de captura y watermarks | foundation, protocol (redacción/identidad) | reducers de dominio; decisiones de negocio | Admit/Seal/Recover/Iterate/Verify API; envelope M1.6 | archivos journal + manifests | admisor único + writer secuencial + group commit |
| `internal/catalog` | Event/Market/Outcome/Asset/Condition/relationships versionadas conocidas-a-fecha, `UniverseSpec`→`UniverseRevision`+`UniverseChanged`, Subscription Planner, quarantine | identidad, relaciones y membership de Universe | foundation, persist, protocol(gamma) | books/frames/estrategias; borrar por scan parcial | revisiones inmutables + `UniverseChanged` | tablas 0010–0019 + cursor propio | reducer serial single-owner |
| `internal/regimes` | Tick/min-size/fees/lifecycle/resolution observations con provenance, `FeeResolver` versionado, `REGIME_SUSPECT`, fee trade-observed | constraints y lifecycle observado | foundation, persist, protocol | reescribir identidad de Catalog; quotes; fee universal | `RegimeID` revisions + invalidaciones | tablas 0020–0029 + cursor propio | reducer serial propio |
| `internal/transport` | Adapters read-only REST/WS (`gamma`, `clob`, `datav2`, `marketws`): conexiones, subscriptions, epochs, rate budgets, heartbeats; escriben evidencia en Capture | conexiones y epochs de transporte | foundation, protocol, capture (admisión) | escribir proyecciones (books/catálogo); signer; dominio mutable | clientes por superficie | ninguna (evidencia vía Capture) | connection manager por superficie; un reader + un writer de control por conexión |
| `internal/books` | Book shards por `AssetKey`, epochs/fencing, bootstrap WS full, calidad M1.5, namespace `REST_OBSERVATION` | proyección y calidad por epoch | foundation, capture, protocol(marketws), catalog (IDs), regimes (constraints) | frames/estrategias; mezclar REST+deltas; backfill L2 | `BookSnapshot` + `QualityState` | in-memory + `applied_seq` cursor por shard | N shards single-owner con inbox FIFO |
| `internal/frames` | Dispatcher único, cortes forward con barreras FIFO, `revision_vector`, `DeliveryFrame` en carril RUNTIME, presupuestos K/bytes | demanda y delivery por consumidor | books, catalog, regimes, capture, foundation | estrategias concretas; cuenta (refs opacos); latest como sustituto | `DeliveryFrame` + API de barrera | RUNTIME journal + snapshots ≤K/bytes | dispatcher único + scheduler por run |
| `internal/strategy` | Strategy API frozen M1.8 materializada en Go, runtime de actores, lifecycle, modo SCREEN, gate de imports/lint | instancias y estado runtime por estrategia | frames, foundation, catalog (vistas), obs | red/secrets/signer/wallet/repos/execution; goroutines propias en callbacks | `Strategy/Factory` + tipos M1.8 | RUNTIME journal; estado reconstruible | actor serial por instancia, mailbox acotado |
| `internal/economics` | `Quote`/`CostEnvelope`, executable depth, VWAP, fees por escenario vía FeeResolver, incentivos estimados separados | funciones puras de economics | foundation, regimes, strategy (tipos), frames | simulator/account; mutar books | `Quote`/`CostEnvelope` | ninguna (pura) | sin estado |
| `internal/simulator` | Fill engine determinista, escenarios optimistic/base/stress, liquidity ledger por namespace, `PORTFOLIO_SHARED`, eventos sintéticos para account | liquidez, modelo y eventos sintéticos | economics, strategy (tipos), frames, foundation | cuenta real; books; transport | FillModel API + ledger namespace | checkpoints reconstruibles por namespace | serial por run |
| `internal/account` | Account Coordinator único writer (real y virtual): ledger, reservas, intents, fills, atribución, `BasketExecution`, `AccountView` revisions, classifier de writes, recovery, outbox | todo lo contable por namespace | foundation, persist, protocol(clobrest) | transport/signer; quotes (es consumidor); otra cuenta | comandos tipados + `AccountView` + classifier allowlist | tablas 0030–0044 (`ACCOUNT_FACT`) | un Coordinator por cuenta/namespace; reducers seriales |
| `internal/risk` | Reglas versionadas, eligibility/sizing, evaluador puro sobre snapshot de cuenta | políticas de riesgo y sus snapshots | foundation, account (vistas) | ledger propio; transport | `RiskPolicyView` + decisión tipada | tablas de policy en rango 0030–0044 | sin estado |
| `internal/replay` | Manifests, virtual clock, replay de observación y delivery, auditoría, `NOT_REPRODUCIBLE` | runs offline reproducibles | capture, catalog, regimes, books, account (reducers), strategy (fixture) | transport/red; estado actual como sustituto | manifest schema + replay API | manifests versionados | pool offline acotado |
| `internal/experiment` | Registry de hipótesis `PE-xxx`, protocolo preregistrado, run manifests, scorecards, datasets con lineage, outcomes | manifests/pins de experimentos | persist, strategy (tipos), simulator, replay (manifests), foundation | tablas privadas de account; reescribir raw | registry/scorecard/outcome schemas | tablas 0045–0054 + derivados SQLite/JSONL | offline serial por experimento |
| `internal/obs` | Métricas, logs estructurados con correlación, readiness por capability, cinco diagnósticos, pipeline timings, resource pressure | instrumentación | foundation | controlar dominio por logging | registro de métricas + readiness API | ninguna (exposición local) | collectors sin locks largos |
| `internal/supervisor` | Lifecycle del proceso, lock exclusivo, boot markers, shutdown con deadline, `ExecutionMode`/`ActivationLease` validator, `DEGRADED_AUDIT`, disk watermarks, barrera de backup | ciclo del proceso y leases | construido por cmd sobre todos los módulos | mutar proyecciones o cursores ajenos | Supervisor + lease validator + markers | markers/`AUDIT_GAP` en store escribible | orquesta start/drain/stop |
| `internal/archtest` | Test de arquitectura: dirección de imports, allowlist de estrategias (sin `unsafe/reflect/os/exec/net/syscall/plugin/cgo`), sin `utils/common` | sólo tests | nada (análisis AST) | runtime | go tests | ninguna | n/a |

Reglas estructurales frozen que este árbol materializa: adapters dependen hacia adentro; dominio no importa transports ni storage de otros módulos; el composition root es el único que conecta puertos; no hay `utils` ni `common`; un paquete = un owner. Todo paquete nuevo requiere slice propio y actualización de esta tabla. Los árboles de paquetes son derivados de los límites frozen de M1.2; reorganizarlos sin cambiar ownership no requiere reapertura arquitectónica, pero sí revisión de manager.

**Elección de dependencias third-party (operativa M2, reversible):** SQLite driver `modernc.org/sqlite` (pure Go, sin cgo; performance se mide en G-09b/G-13 y `mattn/go-sqlite3` es reemplazo encapsulado si hiciera falta); decimal `shopspring/decimal` encapsulado detrás de los tipos de `foundation` (nunca expuesto tal cual); property testing `pgregory.net/rapid` con seeds persistidas; WebSocket `gorilla/websocket` encapsulado en adapter; métricas `prometheus/client_golang` con exposición local; logs `log/slog`; config TOML estricta (`BurntSushi/toml`); HTTP/CLI stdlib. Go toolchain: baseline del proyecto `go 1.27.0` con `toolchain go1.27.1` (decisión operativa cerrada por el owner al iniciar S01; corrige la propuesta histórica `go 1.23`).

### M2.2 — Orden de dependencia y checkpoints verticales

```text
S01 Foundation
   ↓
S02 Protocol ∥ S03 Capture + Persist          ← PARALLEL GROUP A
   ↓ barrera
S04 Catalog → S05 Regimes
   ↓ barrera
S06 WS+Books → S07 Frames → S08 Replay → S09 Strategy → S10 Economics+Simulator   ← GROUP B1
S11 Account+Risk                                                                    ← GROUP B2 (∥ B1)
   ↓ barrera (integración B1×B2)
S12 Supervisor / Observability / Backup-Restore
   ↓
S13 Experiments / Shadow E2E / Certificación
```

Justificación del orden: Capture+Persist preceden a todo reducer porque `durable-before-publish` y `applied_seq` son prerequisito de catálogo, books y cuenta (M1.6/M1.7); Regimes precede a Books porque salir de `SYNCING` exige constraints válidos (M1.5); Frames preceden a Strategy porque el runtime entrega `Frame`; Strategy precede a Simulator porque los tipos de candidatos viven en la API frozen; Account puede correr en paralelo con la cadena B1 porque su seam (comandos tipados, `FillKey`, `AccountView`, estados M1.11) está congelado y su ownership de paquetes/migraciones es disjunto; Supervisor/Certificación van al final porque necesitan el wire completo. Se eligió esta forma para producir capacidades útiles temprano (checkpoints verticales) en vez de capas horizontales sin valor: tras S04 existe `catalog sync` real; tras S06 existe `record` de un mercado real; tras S08 existe replay determinista de la propia observación; tras S09 existe SCREEN end-to-end; tras S13 existe un experimento SHADOW con scorecard. Cada slice usa la plantilla de M2.3; M2.4–M2.10 completan paralelismo, tests, entrega a NORMAL, hitos, frontera M4, decisiones operativas y verificación de calidad.

### M2.3 — Slices de implementación

Convenciones comunes a todos los slices: cada slice es una asignación NORMAL cerrada (un paquete de trabajo, un commit range, un DoD binario); todo slice ejecuta `go build ./... && go vet ./... && go test ./... -race` como verificación mecánica mínima; fixtures nuevas llevan header de provenance (fuente TPM parte/sección, fecha, SHA de la parte); fallos de property testing persisten seed + contraejemplo mínimo en `testdata/property-failures/<gate>/<fecha>/`; ningún slice usa coverage como sustituto de invariants; ningún slice toca archivos de otro slice ni migraciones fuera de su rango.

#### M2-S01 — Repositorio y Foundation

**Goal:** materializar el baseline del repo y las primitivas transversales con las que todo lo demás compila: IDs nominales, decimal exacto, unidades, relojes, taxonomía de errores, capability registry fail-closed, config versionada y gates mecánicos (build/vet/imports/arquitectura).

**Depends on:** ninguno (primer slice).

**Allowed scope:** crear el repo según M2.1; `go.mod` con toolchain pinned; `internal/foundation/**`; `internal/config/**`; `internal/archtest/**`; `cmd/engine` con main mínimo y subcomando `version`; `testdata/foundation/**`; Makefile opcional.

**Forbidden:** cualquier paquete de dominio/transport/persistencia; dependencias third-party fuera de la lista M2.1; I/O de red; crear migraciones; tocar TPM/vault; implementar tipos de Strategy API (S09).

**Contracts:** M1.3 completo: IDs tipados por namespace (`GammaEventID`, `GammaMarketID`, `ConditionRef`, `AssetKey{chain_id, protocol, token_contract?, wire_asset_id}`, `IntentID`, `FillKey`, `RevisionRef{owner, namespace, entity_id, generation, revision, schema_version, content_hash}`); decimal exacto coefficient+scale desde lexema JSON (`json.Number`), sin `float64` monetario ni `*big.Int` mutable expuesto; unidades en tipos; boundary numérico de órdenes P03 §5 como funciones puras (grid/decimales de precio, size floor 2dp, amount ceil/floor, conversión E6 por BUY/SELL, rechazo de desbordes/escalas desconocidas/negativos); sentinel handling (69/999/1970-01-01/0 → unknown en contexto); `Clock` wall + monotonic-offset por boot; error taxonomy tipada (`TRANSIENT/INVALID/UNSUPPORTED/DISABLED/QUARANTINED/UNKNOWN`, jamás strings libres); capability registry allowlist versionada y cerrada (M1.1: capability ausente/deshabilitada no produce ruta; `ExecutionMode` default `LIVE_DISABLED`; `ActivationLease` tipo no fabricable sin emisión); config strict con `config_revision` hash.

**Persistence:** ninguna (sin DB en este slice).

**Concurrency:** tipos value inmutables con copias defensivas; cero goroutines en foundation.

**Failure behaviour:** parsing inválido, desborde o escala desconocida → error tipado con contexto, jamás clamp/cero/defaults; capability desconocida o deshabilitada → `DISABLED` antes de cualquier ruta; config inválida → abort de startup con diagnóstico exacto del campo.

**Tests:** G-01 unit vectors (IDs distintos por namespace; tabla completa de ticks/redondeos P03 §5; amounts/digests reproducibles); property tests decimal (round-trip lexema→decimal→string, sin overflow, asociatividad acotada); matriz de capabilities (ninguna ruta ejecutable para disabled/unknown — semilla de G-15); archtest: dirección de imports y probe negativo (paquete strategy-fake que importa `unsafe` falla el gate; la base confiable Go queda delimitada y versionada según M1.14); fixtures negativas de config.

**Gates:** G-01; base mecánica de G-15b.

**Physical verification:** `go build ./... && go vet ./... && go test ./... -race`; `go run ./cmd/engine version` imprime module/commit/toolchain/config schema; demostración del gate de imports con probe `unsafe` en rojo y luego revertida.

**Definition of Done:** build/vet/tests verdes con `-race`; G-01 PASS con evidencia en `testdata/foundation/evidence/g01.json` (fixture hash, expected/actual, build); fallos de property con seed persistida = FAIL del slice.

**Handoff:** la API de foundation queda v1 estable; todos los slices posteriores importan IDs/unidades/errores/registry desde aquí; agregar un ID o unidad nuevo exige slice propio.

#### M2-S02 — Protocolo wire: DTOs, parsers y fixtures

**Goal:** contratos wire versionados y parsers totales por superficie, separados del dominio, con fixtures sanitizados versionados y redaction schema; sin I/O.

**Depends on:** M2-S01.

**Allowed scope:** `internal/protocol/**`; `testdata/protocol/**`; tests de protocolo.

**Forbidden:** dial HTTP/WS de cualquier tipo; tipos de dominio de catálogo/books/cuenta; migraciones; fixtures con secretos reales; modificar el TPM.

**Contracts:** DTOs wire exactos: Gamma events/markets con arrays codificados como string, keyset `after_cursor` + fallback explícito a `/events`//`/markets` offset (M1.4/U-03); CLOB REST read-only shapes (`/book` con best al final, `/clob-markets/{condition_id}`, tick y fee lookups); Market WS mensajes (`book`, `price_change`, `last_trade_price`, tick-size change, BBO extendido, variante `initial_dump=true`); Data v2 subset (trades, order/orders, positions, activity, resolution) con sentinels y units por campo; `ProtocolContext` unión cerrada `CTF/PROTOCOL_V2/UNKNOWN` como identidad tipada, sin codecs v2 (UNKNOWN → quarantine en consumers); version identity por superficie (`schema_version` + `normalizer_version`); tabla de unidades de tiempo (Order v2 ms, expiration/auth s, User WS s, Market WS ms, Data v2 según lookup) con normalización UTC sin inventar precisión; redaction schema versionado por superficie: `owner`, `signature`, cookies, auth, todos los headers `POLY_*`/HMAC, validación recursiva por schema (M1.6/FBL-011); parsers totales: campo crítico desconocido o enum divergente → raw preservado + flag, nunca drop silencioso.

**Persistence:** fixtures bajo `testdata/protocol/<surface>/<version>/` con manifest SHA en `testdata/protocol/manifest.json`.

**Concurrency:** parsers puros; sin estado global.

**Failure behaviour:** JSON malformado, tipo inesperado o enum crítico desconocido → error tipado con raw adjunto; arrays Gamma con longitudes/índices inconsistentes → error de identidad (Catalog decidirá `QUARANTINED`); ninguna superficie "normaliza lo mejor posible".

**Tests:** G-03 (fixtures por envelope: happy path, unknown-field, enum divergente, string-arrays, sentinels, multi-unit timestamps, `success:false`/errores CLOB tipados para classifier futuro); fuzz/property no-panic sobre bytes corruptos con seeds persistidas; round-trip decimal desde lexema; fixtures centinela que prueban que la redacción elimina `owner/signature/POLY_*` recursivamente.

**Gates:** G-03; extensión G-01 (lexema wire→decimal, unidades).

**Physical verification:** `go test ./internal/protocol/... -race`; `go test ./internal/protocol -run TestFixturesManifest` valida SHA de cada fixture contra el manifest.

**Definition of Done:** todas las superficies parsean sus fixtures (positivas y negativas) verdes; manifest de fixtures con SHA; archtest confirma cero imports de red en `internal/protocol`; evidencia G-03 emitida.

**Handoff:** S03 consume el redaction schema; S04/S05/S06 consumen DTOs/parsers por superficie; agregar una superficie nueva = slice nuevo; los parsers son la única autoridad de interpretación wire.

#### M2-S03 — Capture journal, carriles y framework de persistencia

**Goal:** admisión durable-before-publish con carriles EVIDENCE/RUNTIME, journal segmentado con CRC y recovery de prefijo, y el framework SQLite (migraciones, single writer, `applied_seq`, outbox pattern, integridad por clase) que usarán todos los owners.

**Depends on:** M2-S01, M2-S02 (redaction schema + surface identity).

**Allowed scope:** `internal/capture/**`; `internal/persist/**`; `migrations/0001–0009_*`; `testdata/capture/**`; `cmd/engine` subcomando `journal verify`.

**Forbidden:** reducers de dominio (catalog/books/account); dial de red; migraciones fuera de 0001–0009; lógica de retención/GC/borrado (no hay GC inicial); cifrado; tocar paquetes de S02.

**Contracts:** envelope M1.6 completo (`capture_id/boot_id/capture_seq`, `surface/connection_id/epoch/frame_ordinal/request_id`, tiempos `received_wall/received_mono_offset/source_time_raw/source_unit`, `schema_version/normalizer_version/config_revision/content_hash`, `payload_bytes/redaction_policy/quality-control_kind`, `segment_id/offset/length/checksum`); `capture_seq` como orden total local asignada por un único admisor; `durable_seq` avanza sólo tras fsync (batch/group commit configurable); carriles EVIDENCE y RUNTIME hacia un secuenciador lógico con cuotas separadas por count/bytes y reserva EVIDENCE (overflow RUNTIME pausa runs, nunca revoca epochs ni roba reserva — contrato que S06/S07 consumen); segmentos acotados por bytes/tiempo con footer range/count/SHA-256; seal inmutable con rename + dir sync; recovery: escanear hasta el último record completo y checksum válido, preservar el sufijo inválido como evidencia, marcar discontinuidad, abrir boot nuevo; clasificación `ACCOUNT_FACT` vs `RESEARCH_EVIDENCE` como API de integridad por clase/rango (sin GC); framework persist: SQLite WAL synchronous FULL con busy deadline, migraciones embebidas forward-only (app antigua rechaza schema futuro; rollback sólo por restore), single writer goroutine, `reducer_cursors(reducer_id, namespace, …)`, helpers transaccionales, outbox pattern (la tabla la crea cada owner), check `journal_seq ≥ applied_seq`.

**Persistence:** journal bajo el data dir configurado; migraciones 0001–0009 (`schema_migrations`, `reducer_cursors`).

**Concurrency:** un admisor único + un writer secuencial; dos colas acotadas por count/bytes; locks que nunca abarquen fsync ni red.

**Failure behaviour:** write parcial o CRC inválido → el record no contabiliza y el sufijo se preserva como evidencia; fallo de fsync → `durable_seq` no avanza, readiness de capture cae y el intervalo queda como discontinuidad; overflow EVIDENCE real → discontinuidad declarada (revocar epoch es responsabilidad del consumer); overflow RUNTIME → pausa de runs; SQLite caída → errores tipados a owners; jamás drop-oldest ni conteos inventados de mensajes perdidos antes de admisión.

**Tests:** G-06 fault fixtures (corte en write/fsync/seal/manifest mediante inyección de writer/filesystem; prefijo recuperado íntegro; sufijo corrupto preservado; manifest falso detectado); G-02b parcial (dos reducers con lag; cursores que no se adelantan mutuamente; check `journal_seq ≥ applied_seq`); property: ningún consumer confirma una decisión sobre raw no durable (consumo sólo hasta `durable_seq`); matriz de crash determinista con seeds.

**Gates:** G-06 (parcial: cierre con consumidores reales en S06), G-02b (parcial: cierre en S11), insumos de G-14.

**Physical verification:** `go test ./internal/capture/... ./internal/persist/... -race`; `go run ./cmd/engine journal verify --data-dir …` reporta clases/rangos/holes por clase, no un PASS único.

**Definition of Done:** cada fault fixture produce prefijo íntegro + discontinuidad marcada + cero decisiones sobre no durable; migraciones aplican y una DB "futura" es rechazada (fixture); evidencia parcial G-06/G-02b en `testdata/capture/evidence/`.

**Handoff:** API de capture/persist v1 estable; los owners posteriores crean sólo sus tablas dentro de su rango de migraciones y filas en `reducer_cursors`; S04 construye Catalog sobre este framework.

#### M2-S04 — Catalog/Universe + adapter Gamma read-only

**Goal:** identidad y relaciones versionadas conocidas-a-fecha con ingest REST real read-only; primer checkpoint vertical (`catalog sync`).

**Depends on:** M2-S01, M2-S02, M2-S03.

**Allowed scope:** `internal/catalog/**`; `internal/transport/gamma/**`; `migrations/0010–0019_*`; `testdata/catalog/**`; `cmd/engine` subcomandos `catalog sync|inspect`.

**Forbidden:** books/frames/estrategias/cuenta; writes contra Gamma; inferir `effective_from` histórico; borrar entidades por pasada parcial; inventar envelope keyset (usar fallback offset documentado); Sports WS; tocar paquetes de S05+.

**Contracts:** entidades y revisiones Event/Market/Outcome/Asset/Condition/Relationship con `RevisionRef` + content_hash + `observed_at/source_at?/source_ref/capture_ref`; relationships tipadas con exhaustividad/evidencia `UNKNOWN/VERIFIED/INVALIDATED` (compartir Event no prueba equivalencia de payouts); contexto de membresía NegRisk como evidencia de mapping (sin cast desde IDs); `UniverseSpec` declarativo → `UniverseRevision{members, exclusions_with_reason, coverage, observed_at}` + `UniverseChanged`; Subscription Planner con unión/refcount de demandas y retención de assets con órdenes/posiciones vía hook opcional (stub hasta S11); quarantine `QUARANTINED` → sin book elegible ni firma; estado de scan (fingerprint de filtros/cursor, inicio/fin, coverage parcial marcado); refresh con dedup por ID y frecuencias separadas activa/archivada; identity join validado entre arrays Gamma y CLOB.

**Persistence:** tablas 0010–0019; reducer con `applied_seq` propio sobre journal EVIDENCE; raw nunca se reescribe.

**Concurrency:** reducer serial single-owner; adapter con rate budget, timeout/backoff de lecturas; sin goroutines compartidas con books.

**Failure behaviour:** pasada parcial o cursor inválido → pasada marcada parcial, nada se borra; conflicto de identidad → `QUARANTINED`; 5xx/timeout del adapter → backoff con budget y pasada inconclusa marcada; crash → reproceso desde el cursor propio con dedup por identidad.

**Tests:** G-04 (pagination con altas/duplicados/cursor inválido; cambios de rules/Other/tick/fees → revisiones nuevas; desaparición parcial → coverage, candidatos viejos bloqueados); propiedades: revisiones inmutables, known-at sin look-ahead, ID estable bajo reingesta (idempotencia de dos pasadas); fixtures REST versionadas (grabadas read-only) + fixture server.

**Gates:** G-04.

**Physical verification:** `go run ./cmd/engine catalog sync` (read-only, config de test contra host real o fixture server); `go run ./cmd/engine catalog inspect --event …` muestra revisiones/coverage; `go test ./internal/catalog/... -race`.

**Definition of Done:** dos pasadas consecutivas de sync producen cero diffs de contenido (idempotentes); fixture de desaparición parcial conserva la entidad y marca coverage; evidencia G-04 emitida.

**Handoff:** S05 referencia identidades de Catalog; S06 obtiene elegibilidad vía `UniverseRevision`; la API de relationships queda lista para Sports/NegRisk sin cambios de dominio.

#### M2-S05 — Regimes/Resolution + constraints CLOB + Data v2 read-only

**Goal:** tick/min-size/fees/lifecycle/resolution como revisiones versionadas con provenance y `FeeResolver` intervalar; constraints que gobiernan la elegibilidad de frames.

**Depends on:** M2-S04 (identidades), M2-S01–S03.

**Allowed scope:** `internal/regimes/**`; `internal/transport/clob/**` (REST read-only); `internal/transport/datav2/**`; `migrations/0020–0029_*`; `testdata/regimes/**`; `cmd/engine` subcomando `regimes inspect`.

**Forbidden:** cálculo de quotes (S10); aplicar régimen actual a la historia; constante universal de fee; desempatar rounding por conveniencia; User WS privado; conversions; tocar paquetes de S06+.

**Contracts:** `RegimeID/revision` por market/asset con raw fields separados (`feesEnabled`, `base_fee` bps, `fd.r/e/to`, `mbf/tbf`, tick, min size, category source + fecha); lifecycle observado con estados que no colapsan (`end/closed/proposed/resolved/redeemable/redeemed` por separado); resolution observations (`ConditionRef`, reporter, proposal/dispute/finality, payout vector raw, block/hash/log index); `FeeResolver` versionado que selecciona una sola fórmula con evidencia aplicable o devuelve intervalo/`UNRESOLVED` (la fórmula publicada no autoriza `feeRate=base_fee/10000` sin prueba); ingestion de `fee_rate_bps` trade-observed con `known_at=capture_seq` como reducer disponible (el wiring desde Market WS lo conecta S06); discrepancia fee → `REGIME_SUSPECT` + refresh + `fee_regime_uncertain_interval`, nunca tarifa universal; invalidación: nuevo tick/min-size/fee/status produce revision bump que invalida evaluaciones y candidatos vigentes.

**Persistence:** tablas 0020–0029 con provenance completo por revisión.

**Concurrency:** reducer serial propio; adapters read-only con rate budgets separados por signer/IP.

**Failure behaviour:** fee sin mapping o con empate no definido → intervalo/`UNRESOLVED` (jamás punto medio silencioso); discrepancia → `REGIME_SUSPECT` y refresh del mercado afectado; crash → reproceso desde cursor propio.

**Tests:** G-01 extendido (grids de tick P03 §5 completos); fixtures de intervalo de fee (U-02); fixture `REGIME_SUSPECT` con cambio de fee entre polls y fee observada por trade (semilla de G-10b/FBL-012); fixtures de lifecycle no-collapse; propiedades known-at.

**Gates:** G-01 (fee/tick vectors); insumos de G-10b.

**Physical verification:** `go test ./internal/regimes/... -race`; `go run ./cmd/engine regimes inspect --market …` lista revisiones y estado de fee con `known_at`.

**Definition of Done:** fixtures fee/tick verdes con evidencia; ningún código retorna fee puntual sin revisión de régimen; invalidación observable por revision bump en test.

**Handoff:** Books (S06) exigirá constraints válidos para salir de `SYNCING`; Economics (S10) consume `FeeResolver`; Regimes expone el reducer de fee trade-observed que S06 conecta al WS.

#### M2-S06 — Market WS + book shards + quality

**Goal:** capturar y proyectar books reales con epochs fencing y estados de calidad honestos; checkpoint vertical `record` de un mercado real.

**Depends on:** M2-S05 (constraints), M2-S01–S03.

**Allowed scope:** `internal/transport/marketws/**`; `internal/books/**`; `testdata/books/**`; `cmd/engine` subcomandos `record` y `books inspect`; wiring de fee trade-observed hacia el reducer de Regimes.

**Forbidden:** mezclar REST+deltas WS; reordenar deltas por timestamp de fuente; backfill L2; Sports WS/RTDS; User WS; revocar epoch por saturación RUNTIME (sólo por fallo real de EVIDENCE); "reparar" gaps con REST; tocar paquetes de S07+.

**Contracts:** unidad de ownership (un asset → un shard → una conexión/epoch autora en cada momento); bootstrap `initial_dump=true` esperando `book` completo por asset (timeout → renovar conexión/suscripción con backoff, permanecer bloqueado); deltas previos al primer `book` se capturan pero no se aplican; aplicación exacta M1.5 (`book` reemplaza niveles; `price_change` asigna size absoluto y cero elimina; `last_trade_price` no muta niveles; tick change invalida constraints sin reescalar niveles); namespace separado `REST_OBSERVATION` sin mezcla; tras gap → epoch nuevo con snapshot WS (nunca reconstrucción del intervalo perdido); estados de calidad y uso autorizado exactamente como la tabla M1.5 (`UNINITIALIZED/SYNCING/OBSERVED_USABLE/REST_OBSERVATION/STALE/SUSPECT/HALTED`); budgets de freshness y checks periódicos REST con resultado `INCONCLUSIVE` ante tráfico concurrente; heartbeat PING 10 s; reorden canónico de books REST; book vacío válido sin profundidad ejecutable; hash opaco; no deduplicar mensajes de mercado por timestamp/hash.

**Persistence:** raw WS al journal EVIDENCE (S03); proyecciones in-memory + `applied_seq` cursor por shard en `reducer_cursors`.

**Concurrency:** un reader por conexión; N shards single-owner con inbox FIFO y barreras (S07); overflow real de EVIDENCE → discontinuidad + epoch revocado + reconexión; overflow RUNTIME nunca revoca.

**Failure behaviour:** delta antes de snapshot → no aplica; timestamp regresivo, crossed book o conflicto schema/ID → `SUSPECT` + nueva sincronización (sin parche selectivo de niveles); staleness → `STALE` bloquea evaluación; desconexión → fencing del epoch y discontinuidad marcada en Capture.

**Tests:** G-05 fault injection (delta antes de snapshot; handover de socket; overflow; timestamps regresivos; crossed books; REST concurrente → sin frame elegible hasta nueva base y constraints); propiedades de aplicación (size absoluto, cero elimina, no doble suma, orden de recepción manda); fixtures WS versionadas de S02 reutilizadas; property con seeds.

**Gates:** G-05; cierre de G-06 con consumidores reales (books y decisiones sólo hasta `durable_seq`).

**Physical verification:** `go run ./cmd/engine record --assets <…>` suscribe, construye book y captura al journal; `go run ./cmd/engine books inspect --asset …` muestra estado/epoch/calidad; `go test ./internal/books/... -race`.

**Definition of Done:** sesión de record sin estados `OBSERVED_USABLE` falsos (transiciones de calidad registradas y explicables); G-05 verde con evidencia; toda reconexión produce epoch nuevo y cero mezclas cross-epoch demostradas por property.

**Handoff:** S07 construye frames sobre shards+quality; los datasets heredan discontinuidades explícitas; quality API congelada para SHADOW.

#### M2-S07 — Frame Builder y delivery runtime

**Goal:** cortes forward multi-asset con barreras FIFO, `revision_vector` y journaling de `DeliveryFrame` en RUNTIME — la unidad de entrega reproducible.

**Depends on:** M2-S06 (shards/quality), M2-S04/S05 (revisiones universe/regimes), M2-S03.

**Allowed scope:** `internal/frames/**`; `testdata/frames/**`; sin CLI nueva (consumo vía tests y S09).

**Forbidden:** consultas arbitrarias del pasado; latest como sustituto de corte; retención ilimitada de revisiones; bloquear Capture; usar `dispatched_seq` global aislado como prueba de inbox procesado; tocar paquetes de S08+.

**Contracts:** corte forward exacto de FBL-008: `C=dispatched_seq` fijado entre despachos; `Barrier(cut_id, C, generation)` encolada en cada inbox FIFO antes de cualquier record >C (o C futuro con barrera reservada antes de despachar >C); al cruzar la barrera cada owner publica su snapshot incluso sin mutación, con avance certificado por watermarks; `INELIGIBLE` ante falta de slot/bytes/deadline/generation inválida/shard pasado de C sin snapshot (jamás latest); presupuestos K snapshots por owner + bytes totales; coalescing de solicitudes del mismo corte; `DeliveryFrame{run_id, ordinal, trigger, cut_seq, revision_vector, quality, virtual_time}` journaleado en RUNTIME con descriptor append antes de invocar y durabilidad antes de publicar resultado/feedback; `revision_vector` con `RevisionRef` verificables (universe/relationship/regime/quality/clock/config + slots para account/risk/liquidity que S11/S13 completan); antigüedad, skew e incertidumbre viajan en el frame (coherencia local, no snapshot simultáneo del venue).

**Persistence:** delivery frames en journal RUNTIME; snapshots retenidos ≤K/bytes con liberación al completar/abortar.

**Concurrency:** dispatcher único + scheduler por run con prioridades deterministas; barreras con prioridad en inboxes; pausa de runs bajo presión sin revocar epochs ni bloquear Capture.

**Failure behaviour:** sin slot/bytes o deadline → frame `INELIGIBLE` y refs liberadas; crash → frames válidos sólo ≤ `durable_seq`; descriptor no durable → no se publica feedback ni se invoca el siguiente callback dependiente; reserva/timeout de un frame no acumula historia.

**Tests:** G-05b property (scheduling aleatorio: ningún record ≤C omitido y ninguna revisión >C incluida; K/bytes nunca excedidos; shard adelantado y shard sin eventos → snapshot o `INELIGIBLE`, jamás latest; sin bloqueo de Capture); invariants G-02 de frames; determinismo del ordinal.

**Gates:** G-05b.

**Physical verification:** `go test ./internal/frames/... -race`; harness de scheduling con ≥100 seeds registrados en evidencia.

**Definition of Done:** property G-05b verde con seeds registrados; cualquier contraejemplo persiste seed + traza y es FAIL del slice; schema de `DeliveryFrame` emitido y congelado en test de compatibilidad.

**Handoff:** S09 entrega `Frame` a estrategias; S13 reutiliza barreras para SHADOW; la semántica de corte queda cerrada para always.

#### M2-S08 — Replay de observación y manifests

**Goal:** reproducibilidad demostrable de la propia observación: replay determinista desde journal + manifest con lineage y `NOT_REPRODUCIBLE` explícito.

**Depends on:** M2-S07 (schema DeliveryFrame), M2-S04–S06 (reducers), M2-S03.

**Allowed scope:** `internal/replay/**`; `testdata/replay/**`; `cmd/engine` subcomandos `manifest build` y `replay`.

**Forbidden:** red y wall-clock en replay; usar estado actual para rellenar revisión faltante; reconstruir cotizaciones no capturadas; backfill L2; prometer replay de episodios incompletos; tocar paquetes de S09+.

**Contracts:** manifest M1.6/M1.9 (hashes/rangos de segmentos, coverage por stream/asset/epoch, holes, checkpoints, revisiones metadata/rules/fees/relationships y su disponibilidad temporal, normalizador, parámetros, seed, clocks, delivery policy, política de censura/exclusiones con denominadores); replay de observación (reducers sobre exactamente los records durables del manifest, determinista por manifest+código+params+seed); replay de delivery (inputs exactos por fase vía `DeliveryFrame`; delivery sin resultado durable al crash → `INCOMPLETE`); auditoría de decisiones (compara outputs registrados con inputs efectivos; no reenvía ni reejecuta como mandato); resolución de `revision_vector`: sólo ref resoluble por hash+localizador o snapshot pineado; falta o mismatch → `NOT_REPRODUCIBLE` de esa fase/decisión, nunca estado actual; virtual clock y RNG seeded por manifest; simulación contrafactual sólo con manifest/namespace nuevos y etiqueta explícita.

**Persistence:** manifests como artefactos versionados (JSON + hashes); replay es read-only sobre journal.

**Concurrency:** pool offline acotado; pausa bajo presión de disco (critical watermark bloquea nuevos replays antes que evidencia).

**Failure behaviour:** segmento faltante o alterado → integridad `FAIL/MISSING` + run `NOT_REPRODUCIBLE`; episodio que cruza discontinuidad → termina ese episodio o queda etiquetado no evaluable según regla ex ante; exclusiones contadas en denominadores.

**Tests:** G-07 (misma captura/manifest/seed/build con ≥3 concurrencias de ingestión offline → hashes de frames/reducers/oportunidades iguales; delivery replay concuerda con outputs completados); borrar/alterar un input pineado → `NOT_REPRODUCIBLE` detectado (semilla G-07b); property de determinismo con seeds.

**Gates:** G-07 (parcial: cierre completo con estrategia y account refs en S09/S13).

**Physical verification:** `record` → `manifest build` → dos `replay` con schedules distintos → reporte de igualdad de hashes; manipular un segmento del fixture → detección documentada.

**Definition of Done:** replay bit-a-bit igual para ≥3 schedules; manifest manipulado detectado con evidencia; evidencia parcial G-07 emitida.

**Handoff:** S09 corre REPLAY con virtual clock; S13 completa `revision_vector` con account/risk/liquidity/quote refs y cierra G-07/G-07b.

#### M2-S09 — Strategy runtime y modo SCREEN

**Goal:** materializar la Strategy API frozen (M1.8) con runtime aislado, deadlines y fencing; fixture neutral corriendo SCREEN end-to-end sobre frames reales.

**Depends on:** M2-S07/M2-S08 (frames + delivery + virtual clock), M2-S01–S03.

**Allowed scope:** `internal/strategy/**`; extensión de `internal/archtest` (imports gate de estrategias); `testdata/strategy/**` (fixture neutral); `cmd/engine` subcomando `screen`.

**Forbidden:** signer/wallet/secrets/red en la API; goroutines propias, reloj global, random global o I/O en callbacks; plugins; pipeline completo REPLAY/SHADOW (S13); estrategias Sports/NegRisk reales; tocar `internal/account` (sólo consume tipos públicos cuando existan); paquetes de S10+.

**Contracts:** tipos Go exactos de M1.8 (`Strategy`, `Factory`, `Descriptor`, `RunContext`, `Frame`, `EvaluationContext`, `Opportunity`, `ActionCandidate`, `Assessment`, `Feedback`), todos los valores inmutables, bounds en legs/payloads/oportunidades; lifecycle (`WAITING_DATA/UNSUPPORTED` sin campos cero sustitutos; `Start` una vez; `Observe(UniverseChanged)` antes de `Detect` sobre esa revisión; `Stop` idempotente sin colocar/cancelar órdenes); actor serial por instancia con mailbox acotado, coalescing sólo si `DataRequirements` lo permite, deadline con cancelación de contexto y descarte de resultados tardíos por run generation; panic recuperable → instancia `FAILED`, retiro de candidatos y política de cancel de remanentes vía Coordinator (stub deny-all en este slice); callback no cooperativo → cierre de instancia y restart controlado del proceso si no drena, sin acumular goroutines; descriptor journaleado en RUNTIME (append antes de invocar, durable antes de publicar); gate de imports (prohibidos `unsafe/reflect/os/exec/net/syscall/plugin/cgo` para paquetes de estrategia; base confiable delimitada) + lint (sin goroutines propias/I/O/reloj global); modo SCREEN: reporta candidatos/costes sin abrir orden real ni simulada y sin secrets.

**Persistence:** runtime journal en RUNTIME; estado de instancia reconstruible desde manifest + deliveries.

**Concurrency:** una ejecución por instancia; orden de mailbox determinista y registrado.

**Failure behaviour:** errores tipados (`NO_SIGNAL/INSUFFICIENT_DATA/INVALID_MODEL/TRANSIENT_INPUT/fallo de software`); resultado tardío descartado por generation; instancia fallada no reinicia en el mismo proceso sin fencing; `INSUFFICIENT_DATA` nunca se convierte en señal.

**Tests:** G-08 (fixture neutral single/multiasset con timers y external input sintético, resultados consistentes en SCREEN; cero acceso por API a red/secrets/signer/wallet/repos/execution ports; ownership de cada estado mutable verificado); G-09 (callback lento/panic/no cooperativo: otros consumidores mantienen progreso dentro del perfil, instancia fenced, sin leaks acumulativos, cancel/reconcile prioritarios); G-15b parcial (probe con import prohibido falla el gate; neutral pasa; sin afirmar sandbox); propiedades de no-mutación de inputs.

**Gates:** G-08, G-09, G-15b (parcial: cierre en S12).

**Physical verification:** `go run ./cmd/engine screen --strategy fixture-neutral …` produce reporte de oportunidades/costes sobre datos reales sin envíos; `go test ./internal/strategy/... -race`.

**Definition of Done:** fixture neutral estable en corrida mixta wall+virtual; evidencia G-08/G-09 emitida; imports gate demostrado en ambas direcciones (acepta neutral, rechaza probe).

**Handoff:** S10 consume los tipos `Frame/Opportunity/ActionCandidate/EvaluationContext`; S13 monta REPLAY/SHADOW sobre este runtime sin cambiar la API.

#### M2-S10 — Economics y Simulator

**Goal:** cotización/costes comunes y fill engine determinista con escenarios y liquidity ledger aislado por experimento; decisiones monetarias en decimal exacto.

**Depends on:** M2-S09 (tipos), M2-S05 (FeeResolver), M2-S07 (frame refs).

**Allowed scope:** `internal/economics/**`; `internal/simulator/**`; `testdata/economics/**`; `cmd/engine` subcomando `quote` (diagnóstico puro opcional).

**Forbidden:** reservar el book real; short sintético vía saldo negativo; interpolar liquidez no observada; modelo maker calibrado (etiqueta `UNCALIBRATED` mientras falte); convertir rewards estimados en cash; touch=fill; tocar `internal/account` (integración en S13).

**Contracts:** `Quote{frame_id, size_grid, executable_depth, VWAP, worst_price, platform_fee_interval, expected_incentives, slippage_scenarios, cash_required, token_required, capital_lock, validity, assumptions}` y `CostEnvelope` completos; BUY consume collateral+costes y SELL exige tokens disponibles (sin corto sintético); fee por escenario con intervalo del FeeResolver (múltiples fills pueden tener costes distintos; reconciliar fee efectiva por fill); fill engine M1.9 (submit-time, delay, limit/policy, remanente, cancel-latency; BUY barre asks / SELL bids al tiempo simulado de llegada integrando niveles para VWAP; FOK exige total, FAK admite parcial; rechaza cantidad no cubierta; sin interpolación entre snapshots; resting/touch no es fill probado); escenarios optimistic/base/stress con parámetros por manifest y `UNCALIBRATED` donde falte calibración; liquidity ledger por `(ExperimentID, RunID, instance, scenario)` sin doble consumo por asset/side/precio/`RevisionRef`; modo `PORTFOLIO_SHARED` explícito con `PortfolioRunID`, participantes/orden de admisión/seed preregistrados y atribución `PEER_CONSUMED_DEPTH`/`PEER_RESERVED_CAPITAL` (FBL-005); modelo maker acotado con incertidumbre declarada; eventos sintéticos de basket que alimentan el mismo contrato de reducer `BasketExecution` de M1.11 (wiring en S13, sin segunda política de secuenciación local).

**Persistence:** ledger de liquidez por namespace reconstruible por replay (checkpoints periódicos permitidos; nunca cuenta real ni `synchronous=FULL` requerido).

**Concurrency:** simulación serial por run; offline pool acotado.

**Failure behaviour:** profundidad insuficiente → rechazo de cantidad (sin fill parcial inventado); fee `UNRESOLVED` → coste inconcluso; depth doble-usada → property failure con seed.

**Tests:** G-10 (fixtures exactas de sweep/VWAP/fees/partials/GTD/FOK/FAK/cancel race/multi-leg/virtual liquidity; missing fee/queue bounds → inconcluso; escenarios trazables); G-10b (dos runs independientes idénticos igualan al individual; portfolio compartido atribuye peers y conserva denominadores; cambio de fee entre polls marca intervalo; fee del trade A no se aplica a B ni antes de `known_at`); propiedades de conservación de depth con seeds.

**Gates:** G-10, G-10b.

**Physical verification:** `go test ./internal/economics/... ./internal/simulator/... -race`; reporte de escenarios por fixture con labels de calibración.

**Definition of Done:** fixtures exactas verdes; todos los escenarios etiquetados; evidencia G-10/G-10b emitida.

**Handoff:** S13 integra simulator→account en namespace virtual y construye scorecards; los contratos de `Quote`/escenarios quedan congelados.

#### M2-S11 — Account Coordinator (no-live) + Risk

**Goal:** único writer de cuenta (real y virtual) con ledger, reservas, intents, fills, atribución, baskets secuenciales y recovery reducers; Risk puro; Execution/Reconciler/Credentials como stubs `DISABLED` deny-all detrás de los puertos frozen.

**Depends on:** M2-S01–S03, M2-S02 (DTOs para classifier), M2-S05 (referencias de quantization/regimes). Paralelizable con la cadena B1 (grupo B2).

**Allowed scope:** `internal/account/**`; `internal/risk/**`; `migrations/0030–0044_*`; `testdata/account/**`. Prohibido tocar `cmd/` (el wiring lo hace S12/S13) y cualquier paquete del grupo B1.

**Forbidden:** HTTP write real; User WS; RPC/chain reads reales; resubmisión automática; salt/timestamp nuevo para recuperar un intent; liberar por tiempo/expiry/balances iguales; unwind automático; cifrado de payload firmado; fake success en stubs (retornan `DISABLED`); fake implementations de venue.

**Contracts:** estados internos en ejes distintos de M1.11 exactos (intent `PREPARED/SEND_ATTEMPT_STARTED/VOID/UNKNOWN/REJECTED/ACK_OBSERVED`; orden `OPEN/PARTIAL/TERMINAL/UNKNOWN` con raw remoto; ejecución `NONE_PROVEN/EXECUTION_PROVEN/UNDETERMINED`; settlement `MATCHED/MINED/CONFIRMED/RETRYING/FAILED/UNKNOWN`; reserva `HELD/PARTIALLY_CONSUMED/RELEASABLE/RELEASED`; caso `RECONCILING/HUMAN_REVIEW_REQUIRED/CLOSED`); transacción atómica reserva + intent `PREPARED` + outbox; `WriteObservation` → classifier versionado con allowlist exacta de M1.11 (`DEFINITIVE_REJECT` sólo con contrato verificado; 400/401/403 y `success:false` por sí solos no bastan; 425/429/5xx/HTML/ambiguo → `UNKNOWN`); un attempt = máximo un submit (contador verificado); recovery de boot (`PREPARED` sin attempt en store íntegro → `VOID` + payload no enviable + reserva `RELEASABLE`; `SEND_ATTEMPT_STARTED` sin resultado → `UNKNOWN`; restore atrasado jamás permite VOID por ausencia); convergencia de `UNKNOWN` por evidencia (a)–(d) de M1.11 evaluada sobre observaciones aportadas (Reconciler stub `DISABLED`); dedup `FillKey` con `service=CLOB` (WS y REST comparten clave; status update no suma; Data v2 nunca acuña fills); atribución: subledger `(AccountID, StrategyInstanceID, AssetKey)` con `UNATTRIBUTED` bloqueante, transferencias como asiento explícito idempotente, `Σ atribuciones + UNATTRIBUTED = inventario` por categoría; `available` derivada una sola vez dentro del Coordinator; SELL exige disponibilidad de cuenta y de estrategia; `BasketPolicy` validada (SEQUENTIAL; PARALLEL → `UNSUPPORTED`) + máquina `BasketExecution` con transiciones exactas M1.11 (`PLANNED→RESERVED→EXECUTING→WAITING_LEG→BLOCKED_UNKNOWN→ABANDONING→RESIDUAL_HELD/COMPLETED→CLOSED_*`), sin unwind; compensación = candidato nuevo con autorización/budget/Risk propios; `AccountView` inmutable con revision+hash publicada; Risk: policy schema versionada, eligibility/sizing/reserva como evaluador puro, compare-and-check de revisión; tablas account clasificadas `ACCOUNT_FACT` (retención vida del proyecto, sin TTL).

**Persistence:** migraciones 0030–0044 (intents, attempts, orders, fills, reservas, inventario, subledger, baskets, outbox, observaciones privadas sintéticas, policies); `applied_seq` por reducer/namespace.

**Concurrency:** un Coordinator por cuenta/namespace con transacciones breves y reducers seriales; locks que nunca abarcan red ni fsync de raw; namespaces virtuales aislados por `(ExperimentID, RunID, instance, scenario)`.

**Failure behaviour:** fallo de SQLite → rollback completo de la transacción atómica (sin estados intermedios); contradicción de fuentes → caso `RECONCILING` y exposición congelada; presupuesto de lectura agotado → `HUMAN_REVIEW_REQUIRED` + alerta; jamás liberación sin prueba positiva; `market_resolved` no devuelve cash.

**Tests:** G-02 properties (conservación de reservas/balances, no doble gasto, no doble fill, actualización size absoluta donde aplique); G-02b (VOID de `PREPARED`; cursors con lag; mismo fill CLOB WS/REST aplicado una vez; SELL de B con tokens de A falla hasta transferencia explícita); G-10c (3 legs: primera llena, segunda UNKNOWN, tercera invalidada → `BLOCKED_UNKNOWN`, tercera jamás enviada, primera atribuida, segunda retenida, sin unwind; misma secuencia de hechos produce el mismo estado en el reducer de Simulator y en el gateway fixture; compensación sin nueva autorización rechazada); G-11b (ACK/fill tardíos convergen conservando reserva; expiry + REST ausente + balances iguales con match pendiente → `UNKNOWN` y escala; caso sin prueba nunca libera por tiempo; rechazo inequívoco libera sólo obligación inexistente); G-12b (425/429/503/500/HTML/success ambiguo/duplicate/`order timed out` no verificado → sin segundo submit ni re-firma; sends/attempt ≤1; crash sin exposición duplicada); G-15 parcial (intentos de `deferExec=true`, builder, convert CTF/v2, protocol UNKNOWN, calldata arbitraria → rechazo antes de firma vía stubs deny-all).

**Gates:** G-02, G-02b (cierre), G-10c, G-11b, G-12b, G-15 (parcial).

**Physical verification:** `go test ./internal/account/... ./internal/risk/... -race`; fixtures de fault con seeds persistidas; test negativo que prueba que cada stub retorna `DISABLED`.

**Definition of Done:** todas las propiedades/fixtures verdes con evidencia; esquema con un writer por tabla y `applied_seq` por reducer; stubs `DISABLED` verificados; evidencia G-02b/G-10c/G-11b/G-12b emitida.

**Handoff:** S12 arranca y wirea el Coordinator en Supervisor y en la barrera de backup; S13 conecta simulator→Coordinator virtual y ejecuta los fault fixtures integrados; los puertos de Execution/Reconciler/Credentials quedan listos para implementación live futura sin rediseño.

#### M2-S12 — Supervisor, CLI, observabilidad y backup/restore local

**Goal:** ciclo de vida del proceso con markers/leases fail-closed, observabilidad de los cinco diagnósticos y backup/restore local consistente y medido.

**Depends on:** M2-S09, M2-S10, M2-S11 (wire completo), M2-S03 (bundle primitives).

**Allowed scope:** `internal/supervisor/**`; `internal/obs/**`; `cmd/engine` (subcomandos `run/backup/restore/verify/inspect/kill`); `testdata/supervisor/**`; `testdata/obs/**`.

**Forbidden:** endpoint admin HTTP autenticado (CLI primero); dashboards/alertas externas/tracing live completo; DR off-host; emitir ActivationLease live; borrar evidencia para liberar disco; terminar canales con productores activos.

**Contracts:** orden de startup M1.2 (lock exclusivo → validar config/schema/manifests/capabilities → recovery journal y transacciones → captura + observabilidad → adapters públicos/catálogo/constraints → suscripciones/books → runtimes elegibles); fallo de startup de un writer no impide health/diagnóstico read-only; shutdown con deadline → `UNCLEAN/UNRESOLVED` durable y alerta; markers `BOOT_OPEN`/`BOOT_CLEAN` (arranque live exige reconcile; boot desconocido no es limpio); `ExecutionMode` poseído por Supervisor; `ActivationLease` validator completo con emisión disabled (default `LIVE_DISABLED`; lease expirada/revocada/desalineada en build/config → sin sends; `LIVE_DISABLED` puede reconciliar/cancelar bajo recovery scope, nunca crear órdenes); modo `DEGRADED_AUDIT` con allowlist cerrada aplicada sobre stubs deny-all (ring buffer + sink secundario stderr/syslog + `AUDIT_GAP{boot_id, since}` persistido en primer store escribible; lease bloqueada hasta cierre explícito con evidencia; prohibido nuevo order/liberación); disk watermarks low/critical (low frena replay/export/suscripciones; critical bloquea oportunidades/nuevos sends y mantiene reconcile/cancel, sin borrar raw pineado); observabilidad: pipeline timings `receive→durable→normalize→book→frame→strategy→decision→reserve→send→ack/fill` p50/p95/p99 + queue lag + fsync tail + GC/alloc/lock contention; readiness `liveness/readiness_public/readiness_strategy/readiness_live` (HTTP 200 no habilita live); logs estructurados con correlación `run/experiment/strategy`, `capture/epoch/frame`, `asset/condition/event`, `intent/order/trade/tx`, `config/capability revision` y reason codes, sin payloads sensibles; cinco diagnósticos con condiciones observables de M1.14, coexistentes; backup consistente: barrera de Supervisor → Capture fija corte durable `B` y sella prefijos → owners drenan hasta B sin avanzar cursores → SQLite backup por API del motor (incluye WAL) + outbox pendiente + versiones → manifest con `B`, rangos/hashes por clase, `applied_seq` por reducer/namespace y check `journal_seq ≥ applied_seq` → `BACKUP_COMPLETE` sólo tras verificación; restore: directorio limpio, verificación de hashes/refs/outbox/cursors por owner, reconstrucción de proyecciones y comparación de ledger; evidencia requerida faltante → degradado, jamás PASS; medición de duración y frontera de pérdida del fixture sin adjudicar SLA de DR.

**Persistence:** bundle local completo; markers/`AUDIT_GAP` en store escribible; ningún GC.

**Concurrency:** Supervisor detiene productores → drena hasta frontera registrada → cierra consumers; barrera de writers coordinada sin mutar proyecciones ajenas.

**Failure behaviour:** backup interrumpido → bundle incompleto, jamás `BACKUP_COMPLETE`; restore con bundle que perdió evidencia requerida → degradado explícito; todos los sinks caídos → `BOOT_OPEN` sin cierre limpio y lease bloqueada hasta reconcile.

**Tests:** G-14 (restore completo en directorio limpio con hashes/refs/outbox/cursors verificados y proyecciones reproducidas; GC simulado día 31 con `ACCOUNT_FACT` intacto y fuera de TTL; eliminar un activo requerido del bundle → integridad FAIL/degradada, health read-only puede funcionar); G-06b (bundle cubre cada cursor/dependencia/outbox incluso con writers concurrentes; DB adelantada al journal nunca recibe PASS); G-13b (DB caída → sólo cancel conocido/scoped vía stubs, marker/sink cuando escribibles, buffer recuperado con gaps documentados; todos los sinks fallan + restart → `BOOT_OPEN`, lease bloqueada hasta cierre explícito); G-13 parcial (workload preregistrado con capture+runtime+replay limitado; skips/UNKNOWN explicables; budgets/headroom medidos); tests de honestidad de readiness; cierre de G-15b (fixtures de body/error/headers y evidencia/restore sin filtrar `owner/signature/POLY_*`/secretos; ACL mínima verificable).

**Gates:** G-14, G-06b, G-13b, G-13 (parcial: cierre en S13), G-15b (cierre).

**Physical verification:** `go run ./cmd/engine backup|restore|verify` con fixture de cuenta simulada; drills G-06b/G-13b/G-14 ejecutados con evidencia (duración y frontera de pérdida medidas en el reporte).

**Definition of Done:** ciclo backup→restore produce hashes/ledger idénticos en fixture; los tres drills verdes con evidencia; readiness/diagnósticos visibles sin secretos; sistema arrancable como proceso único con todos los modos.

**Handoff:** base operativa completa para S13; los puertos de lease/`DEGRADED_AUDIT` quedan listos para live futuro sin rediseño.

#### M2-S13 — Experiments, Shadow E2E y harness de certificación

**Goal:** pipeline SHADOW completo preregistrado con scorecards honestos y la ejecución documentada de la matriz de gates no-live (readiness M4).

**Depends on:** M2-S10, M2-S11, M2-S12.

**Allowed scope:** `internal/experiment/**`; `cmd/engine` (subcomandos `experiment|shadow|certify`); `migrations/0045–0054_*`; `testdata/experiment/**`; `testdata/certification/**`.

**Forbidden:** promover `GO` a live; holdout reciclado; mezclar resultados simulados con reales; capturar evidencia privada real (sólo sintética); crear módulos Sports/NegRisk; deniminadores que excluyan episodios sucios sin contarlos.

**Contracts:** hypothesis registry `PE-xxx` con campos M1.9; protocolo de experimento preregistrado (hipótesis falsable, unidad estadística, baseline/controles negativos, exclusiones, stopping rule, sample requirement, `GO/ITERATE/NO_GO` ex ante); run manifest con pins completos de M1.6 + versiones de parámetros/calculadores + universo known-at + escenarios + bankroll virtual; scorecard M1.9 (coverage y discontinuidades; señales totales/independientes; lifetime; net edge por depth/fee/latency; fill/partial/legging rates; capacity; PnL bruto/neto/realizado/no realizado; lock/capital-turns; drawdown y worst loss; markouts/adverse selection; sensitivity y caveats; denominadores con `PEER_*`); outcome `GO|ITERATE|NO_GO|INCONCLUSIVE` con `GO` ≠ permiso live; `INCOMPLETE` explícito para runs interrumpidos; vista estadística mínima (splits temporales/por parent event, OOS, censura por mercados sin resolver, múltiples tests declarados); datasets derivados SQLite/JSONL con lineage y dinero en decimal/int exacto; pipeline SHADOW E2E: capture actual + runtime + simulator + Coordinator virtual con default `INDEPENDENT` y `PORTFOLIO_SHARED` sólo explícito en manifest; parity REPLAY/SHADOW: mismo `Assessment`/sizing/decisión Risk con `revision_vector` completo (account/risk/liquidity/quote refs); harness de certificación: runner que ejecuta cada gate no-live con evidencia (fixture hash, expected/actual, build/config/ambiente) y emite resumen `PASS/FAIL/NOT_RUN` por gate.

**Persistence:** migraciones 0045–0054; manifests/scorecards versionados; datasets con lineage.

**Concurrency:** offline pool para experiments; shadow en vivo respetando cuotas RUNTIME (pausa de runs, nunca revocación de epochs).

**Failure behaviour:** experimento incompleto → `INCOMPLETE/INCONCLUSIVE`, jamás `GO`; replay con ref faltante → `NOT_REPRODUCIBLE`; saturación RUNTIME → runs pausados (contrato G-09b); resultados sólo-optimistic no promueven.

**Tests:** G-07b (replay SHADOW iguala `Assessment`, sizing y Risk con refs completos; borrar/alterar un input → `NOT_REPRODUCIBLE`, nunca diferencia silenciosa); G-09b (saturar RUNTIME con EVIDENCE certificada: runs pausados, cero epochs revocados y cero holes de mercado por esa saturación; group commit sin fsync por callback con latencias medidas; crash antes de durable no publica feedback/intent); G-10b integrado con account; G-13 (ventana shadow preregistrada con capture+runtime+replay limitado y sin pérdidas no declaradas; todos los skips/UNKNOWN explicables; budgets/headroom y métricas medidos); re-ejecución de G-08 en SCREEN/REPLAY/SHADOW; fault fixtures G-10c/G-11b/G-12b integradas al pipeline.

**Gates:** G-07b, G-09b, G-10b (cierre), G-13 (cierre); consolidación de evidencia G-01…G-15 + extensiones b para M4.

**Physical verification:** `go run ./cmd/engine shadow --manifest …` produce scorecard + dataset con lineage; `go run ./cmd/engine certify --profile no-live` ejecuta la matriz y emite bundle de evidencia + resumen por gate; G-16…G-19 y G-14b aparecen explícitos como `NOT_RUN / IMPLEMENT LATER`.

**Definition of Done:** un experimento shadow real (fixture strategy) con scorecard revisable y diagnósticos correctos; matriz no-live con evidencia completa; resumen entregado en este archivo para revisión manager/owner → abre la frontera M4.

**Handoff:** M4 evalúa el engine resultante; Sports/NegRisk pueden consumir Universe/frames/economics/account sin modificar fundamentos (verificado por G-08 y por la estabilidad de los contratos publicados).

### M2.4 — Paralelismo y fronteras de ownership

```text
SEQUENTIAL BASE
- M2-S01 (Foundation; nadie más compila sin esto)

PARALLEL GROUP A (tras S01)
- M2-S02 (internal/protocol + testdata/protocol)
- M2-S03 (internal/capture + internal/persist + migrations 0001–0009)

SEQUENTIAL BARRIER
- Integración S02×S03 (redaction aplicada en admisión) y verificación de archtest global

PARALLEL GROUP B (tras S04→S05)
- B1: M2-S06 → M2-S07 → M2-S08 → M2-S09 → M2-S10 (cadena secuencial; migrations: ninguna nueva)
- B2: M2-S11 (internal/account + internal/risk + migrations 0030–0044; sin cmd/)

SEQUENTIAL BARRIER
- Integración B1×B2: adapter simulator→Coordinator virtual + E2E de namespace virtual

SEQUENTIAL FINAL
- M2-S12 → M2-S13
```

Fronteras que hacen seguro el paralelismo: en Group A, S02 y S03 no comparten archivos y su único seam (redaction schema) está definido contractualmente en M1.6; en Group B, B2 no toca paquetes de B1 ni `cmd/`, sus migraciones (0030–0044) son disjuntas de todo B1 (que no crea migraciones) y su seam con B1 (comandos tipados, `FillKey`, `AccountView`, estados de M1.11) está congelado en M1. Los rangos de migraciones son: S03 0001–0009, S04 0010–0019, S05 0020–0029, S11 0030–0044, S13 0045–0054. Regla dura: no se paralelizan slices que compartan migraciones, primitivas de dominio compartidas o el mismo contrato mutable; ante duda, secuencial. `S04→S05` es secuencial porque Regimes referencia identidades de Catalog; `S12→S13` es secuencial porque la certificación usa CLI/backup/readiness de S12.

**Critical path estimado:** S01 → S03 → S04 → S05 → S06 → S07 → S08 → S09 → S10 → S12 → S13 = **11 slices** (B2/S11 corre en paralelo con holgura; la barrera B1×B2 y S12 lo incorporan).

### M2.5 — Estrategia de pruebas y mapa de gates

Principios: primero invariantes críticos y ramas de falla; coverage (piso Agents-OS 95%) es condición complementaria, nunca sustituto; fixtures negativas deben demostrar que el diseño rechaza rutas inseguras, no sólo que acepta happy paths; toda evidencia de gate registra fixture/input hash, expected/actual, build/config y ambiente; PASS físico se emite por capability/perfil/versiones/workload probado, nunca por haber escrito el test (M1.15).

| Gate | Slice(s) | Fixture / input | Acción | Output esperado | Fallo que hace FAIL | Evidencia |
|---|---|---|---|---|---|---|
| G-01 | S01, S05 | IDs por namespace; tabla ticks/redondeos P03 §5; lexemas wire | parsear/redondear/convertir | valores exactos sin overflow ni float | conflación de namespace, rounding distinto, unknown→cero | `g01.json` expected/actual |
| G-02 | S10, S11 | secuencias generadas (rapid) | aplicar fills/reservas/sizes | conservación, no doble gasto/fill, IDs estables | cualquier contraejemplo | seed+contraejemplo persistidos |
| G-02b | S03, S11 | stores íntegros/atraserados; fills WS+REST | recovery/dedup/cursors | VOID correcto; un fill una vez; cursors sin adelantarse | VOID por ausencia en copia atrasada; fill duplicado | fixtures + reporte |
| G-03 | S02 | fixtures REST/WS/errores versionadas | parsear todo envelope | accept/reject exactos por contrato | parser acepta contradicción o depende de SDK | manifest SHA + evidencia |
| G-04 | S04 | paginaciones con altas/duplicados/cursor inválido; desaparición parcial | sync + refresh | revisiones/coverage correctos; nada borrado | borra por scan parcial; pierde join; look-ahead | evidencia g04 |
| G-05 | S06 | delta pre-snapshot; handover; overflow; timestamps regresivos; crossed; REST concurrente | aplicar/fencing | sin frame elegible hasta nueva base+constraints; SUSPECT/STALE correctos | mezcla REST+deltas; epoch viejo reutilizado | evidencia g05 |
| G-05b | S07 | scheduling aleatorio con seeds | cortes forward | cero omisiones ≤C, cero inclusiones >C; K/bytes respetados; INELIGIBLE sin slot | contraejemplo de barrera | seeds + traza |
| G-06 | S03, S06 | corte en write/fsync/seal/manifest | recovery | prefijo íntegro; sufijo preservado; discontinuidad | pérdida silenciosa; manifest falso; tail presentado íntegro | evidencia g06 |
| G-06b | S12 | writers concurrentes + seal/snapshot/export interrumpidos | armar bundle | cobertura de cursores/dependencias/outbox; `journal_seq ≥ applied_seq` | DB adelantada al journal con PASS | bundle + manifiesto |
| G-07 | S08 | misma captura/manifest/seed, ≥3 schedules | replay observación/delivery | hashes idénticos; INCOMPLETE explícito | diferencia no explicada; episodio incompleto reproducido | reporte de hashes |
| G-07b | S13 | corrida SHADOW con revision_vector completo | replay delivery | iguala Assessment/sizing/Risk; tamper → `NOT_REPRODUCIBLE` | reproduce con estado actual | evidencia g07b |
| G-08 | S09, S13 | fixture neutral single/multiasset + timers + external sintético | correr en SCREEN/REPLAY/SHADOW | resultados consistentes; cero acceso API prohibido | estrategia necesita infra del core; writers duplicados | evidencia g08 |
| G-09 | S09 | callback lento/panic/no cooperativo | ejecutar runtime | progreso de otros; fencing; sin leaks | bloqueo global; callback tardío ejecuta; goroutines ilimitadas | evidencia g09 |
| G-09b | S13 | saturación RUNTIME con EVIDENCE certificada | cargar carriles | runs pausados; cero epochs revocados/holes; latencias medidas | epoch revocado por research | evidencia g09b |
| G-10 | S10 | sweep/VWAP/fees/partials/GTD/FOK/FAK/cancel race/multi-leg/liquidez virtual | simular | resultados exactos; missing fee/queue → inconcluso | touch=fill; depth doble-usada; rewards gastables | evidencia g10 |
| G-10b | S10, S13 | dos runs idénticos; portfolio compartido; fee entre polls | comparar/atrbuir | aislados iguales; peers atribuidos; intervalo marcado | contaminación cross-run; fee extrapolada | evidencia g10b |
| G-10c | S11 | 3 legs: llena+UNKNOWN+invalidada | reducer basket | `BLOCKED_UNKNOWN`; tercera jamás enviada; sin unwind; mismo estado en Simulator y gateway fixture | unwind; cierre ficticio | fixtures |
| G-11 | S11 | WS duplicado/fuera de orden; REST paginado concurrente; settlement FAILED/reorg; transfers externos | reconciliar | converge o abre caso; nunca liberación doble/prematura | balance creado; fill duplicado; 404→no-send | fixtures |
| G-11b | S11, S13 | ACK/fill tardíos; expiry+ausencia+balances iguales con match pendiente | terminalizar UNKNOWN | converge por evidencia o escala; jamás libera por tiempo | liberación por timeout | fixtures |
| G-12 | S11 | crash antes/después de marker; post-socket pre-ACK; timeout/duplicate/batch mixto | clasificar writes | UNKNOWN retenido; sin segundo submit ni salt nuevo | blind retry; reserva liberada sin prueba | fixtures |
| G-12b | S11, S13 | 425/429/503/500/HTML/ambiguo/duplicate/`order timed out` no verificado | classifier | sin resubmit; sends/attempt ≤1; sin exposición duplicada | segundo submit; re-firma | fixtures + contador |
| G-13 | S12, S13 | ventana preregistrada capture+runtime+replay | operar | skips/UNKNOWN explicables; budgets/headroom medidos | sólo favorable en optimistic; readiness engañosa | reporte |
| G-13b | S12 | DB caída; todos los sinks caídos + restart | drill | cancel conocido/scoped; `AUDIT_GAP`; lease bloqueada hasta cierre | nuevos sends; liberación; cierre limpio falso | drill + marker |
| G-14 | S12 | bundle consistente + GC simulado día 31 + bundle incompleto | restore/verificar | restore íntegro; ACCOUNT_FACT intacto; incompleto degrada | bundle incompleto con PASS; cursores adelantados | drill + hashes |
| G-15 | S11, S12 | pedidos deferExec/builder/convert/calldata; perfiles sin secrets; lease revocada | intentar ruta | rechazo antes de signing; flag no abre ruta disabled | config abre ruta; capability omitida cae a genérico | fixtures negativas |
| G-15b | S01, S09, S12 | probe imports prohibidos; fixtures con `owner/signature/POLY_*` | gate de imports + redacción | falla prohibido; neutral pasa; cero filtración en journal/logs/restore | import pasa; secreto en raw | evidencia g15b |
| G-16…G-19, G-14b | — | — | — | `NOT_RUN` / `IMPLEMENT LATER` (mandato live separado) | — | — |

**Fault injection obligatoria (mapa completo):** partial journal write → S03/G-06; crash before/after fsync → S03/G-06; invalid segment → S03/G-06; reducer behind journal → S03+S11/G-02b; WS overflow → S06/G-05; stale epochs → S06–S07/G-05+G-05b; slow strategy → S09/G-09; callback panic → S09/G-09; missing revision → S08+S13/G-07+G-07b; SQLite failure → S11 (rollback atómico) + S12/G-13b; disk pressure → S12 (watermarks low/critical); restore → S12/G-14; incomplete experiment → S13 (`INCOMPLETE/INCONCLUSIVE`).

**Property testing:** todo property usa `pgregory.net/rapid` con seed registrada en la evidencia; ante falla, el runner persiste seed + contraejemplo mínimo en `testdata/property-failures/<gate>/<fecha>/` y el slice queda FAIL hasta reproducir/fix. Los seeds de corridas verdes se conservan por gate para regresión.

### M2.6 — Política de entrega a agentes NORMAL

Cada asignación NORMAL contiene exactamente: (1) un slice de M2.3 (copiado tal cual, es autocontenido); (2) el path del repo (`REQUIRES_OWNER — REPO LOCATION ONLY` resuelto por el owner antes de la primera asignación); (3) baseline assumptions: S01–previos en `[x]` con sus gates verdes, branch de trabajo sobre el estado congelado del slice anterior; (4) allowed/forbidden scope del slice (sin expansiones); (5) refs M1/TPM citadas dentro del slice; (6) tests y gates a implementar/ejecutar; (7) commit/checkpoint único por DoD; (8) DoD binario. NORMAL no lee el vault completo, no reinterpreta arquitectura, no elige DB/runtime/error policy/dirección de paquetes, no marca gates PASS sin evidencia y no toca este proyecto salvo actualizar su tarea y bitácora al terminar. Si la implementación prueba la arquitectura imposible: parar con `BLOCKED — DESIGN ISSUE`, evidencia del contraejemplo y vuelta al manager; prohibido improvisar alrededor. Toda ejecución material de coding deja registro en `agents-os-agent-run-register` (superficie×modelo, evidencia, outcome).

### M2.7 — Hitos de implementación

| Hito | Slices | Capacidad utilizable al cerrarlo |
|---|---|---|
| M3-A — Protocol & Durable Data Foundation | S01–S03 | Todo el wire parsea con fixtures versionadas; journal durable con recovery de prefijo; framework SQLite con `applied_seq`; G-01/G-03 con evidencia |
| M3-B — Market Data + Recorder + Replay | S04–S08 | **Podemos sincronizar catálogo, capturar un mercado real con books de calidad honesta y reproducir determinísticamente nuestra propia observación** (`record` → `manifest` → `replay` bit-a-bit) |
| M3-C — Strategy Runtime + Simulator + Account + Ops | S09–S12 | Fixture neutral corre en SCREEN sobre datos reales; quotes/simulación exactas; cuenta virtual con invariants demostradas; proceso único arrancable con backup/restore local verificado y observabilidad de diagnósticos |
| M3-D — Shadow Research Engine | S13 | **Podemos registrar una hipótesis, correrla en SCREEN/REPLAY/SHADOW y obtener un scorecard reproducible `GO/ITERATE/NO_GO/INCONCLUSIVE`** |
| M3-E — Engine Certification readiness | S13 (matriz) | Matriz G-01…G-15+extensiones b ejecutada con evidencia; G-16…G-19/G-14b explícitos `NOT_RUN`; revisión manager/owner → M4 |

### M2.8 — Frontera de completitud / M4

La implementación puede avanzar a M4 cuando existan, todos verificables sin capital: binario buildable con CLI completa (S12); migraciones aplicables y forward-only (S03–S13); fixtures versionadas por superficie (S02+); tests deterministas con evidencia (todos); captura real (S06); replay determinista (S08); strategy fixture en los tres modos (S09/S13); shadow end-to-end con scorecard (S13); simulator con escenarios (S10); invariants de cuenta/risk demostradas (S11); observabilidad con cinco diagnósticos y readiness honestos (S12); restore local consistente y medido (S12). M2 no marca M4 PASS: M4 es la certificación separada que ejecuta la matriz completa. Live permanece `NOT_CERTIFIED / LIVE_DISABLED`; G-16…G-19 y G-14b requieren mandato posterior.

### M2.9 — Decisiones operativas M2 y pendientes de owner

`REPO LOCATION — RESUELTO`: el clone local de `xKoRx/polymarket-engine` vive en `~/go/src/github.com/xKoRx/polymarket-engine` (checkout existente registrado al iniciar S01; fuera del vault). Ya no es decisión bloqueante.

Decisiones operativas tomadas por TOP bajo contratos frozen (reversibles sin tocar dominio; el owner puede objetar en la revisión): module path `github.com/xKoRx/polymarket-engine`; layout `cmd/ internal/ migrations/ testdata/`; driver SQLite `modernc.org/sqlite`; decimal `shopspring/decimal` encapsulado en foundation; property `pgregory.net/rapid`; WS `gorilla/websocket` en adapter; métricas `prometheus/client_golang` local; logs `log/slog`; config TOML estricta; toolchain baseline `go 1.27.0` / `toolchain go1.27.1` (decisión del owner al iniciar S01; sustituye la propuesta `go 1.23`); migraciones forward-only con rangos por slice (M2.4). El driver SQLite y la latencia de fsync se re-evalúan con mediciones de G-09b/G-13; cambiarlos es cambio encapsulado en `internal/persist`/`internal/capture`, no rediseño.

### M2.10 — Verificación de calidad del plan (§15 del mandato)

1. Toda capability FOUNDATIONAL NOW aparece en ≥1 slice: sí — mapeo completo en M2.3/M2.7 (foundation S01; protocol S02; capture S03; catalog S04; regimes S05; market data S06–S07; replay S08; strategy runtime S09; economics/simulator S10; account/basket S11; observability/recovery/backup S12; experiments/shadow/certificación S13). 2. Todo paquete tiene owner: tabla M2.1. 3. Todo schema tiene un writer: rangos de migraciones M2.4 + ownership por paquete (único writer contable = Coordinator; cursores por reducer). 4. Toda frontera de concurrencia explícita: columna Concurrencia de M2.1 + contratos por slice. 5. Toda ruta crítica de falla tiene test: M2.5 (mapa de fault injection completo). 6. Todo gate no-live de M4 mapea a trabajo: tabla M2.5 (G-16…G-19/G-14b explícitamente fuera). 7. Ningún slice requiere capability live-disabled: stubs `DISABLED` deny-all verificados por G-15/G-12b. 8. Ningún NORMAL inventa arquitectura: M2.6 (paquete cerrado + `BLOCKED — DESIGN ISSUE`). 9. Ningún par comparte contrato mutable: fronteras M2.4 (seams frozen, migraciones disjuntas, sin `cmd/` compartido). 10. El orden produce capacidades intermedias útiles: checkpoints M2.2/M2.7. 11. Local restore testable: S12/G-14/G-06b obligatorios. 12. Sports/NegRisk consumen sin modificar fundamentos: contratos congelados y verificados por G-08; relationships/universe/frames/economics/account publicados como APIs estables.

**Estado del plan:** `M2_FROZEN` — revisión manager/owner cerrada y S01 autorizado/implementado por mandato del owner (2026-09-17). Siguiente: asignaciones NORMAL por slice según M2.4/M2.6 (S02 ∥ S03 tras la barrera de S01).
