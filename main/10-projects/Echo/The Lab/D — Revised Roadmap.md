---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[A — Product Contract — The Lab]]"
  - "[[B — Architecture Decision Report]]"
  - "[[E — First Usable Vertical Slice]]"
  - "[[F — Decision Register]]"
tags: [kind/doc, area/echo]
created: "2026-09-22"
updated: "2026-09-23"
---
# D — Revised Roadmap — The Lab V3 / Echo-first

**PLAN VIGENTE (owner 2026-09-23).**

> **Estado D1 — Echo Foundation = PASS (2026-09-23, HEAD `64b616ff` en `feature/d1-echo-foundation-final`).** Gate final 18 criterios + G19/G20 en [[K — Final Correction and Gate D1 (Shot 3)]]; verde salvo 2 regresiones preexistentes certificadas ajenas a D1.
>
> **D1 SOURCE CLOSED / INTEGRATED TO MASTER (2026-09-23): `master@8adce7ec`** en `xKoRx/echo` (remoto). Integración conservadora sin history rewrite del harvest certificado `22b26716` (implementación + Shot 3 + regresiones + E2E por SPEC) junto al fix Bridge vigente; gates G1–G10 verdes sobre el SHA exacto pusheado. Cierre y handoff en [[O — D1 Closure and D2 Handoff]]. **No marcado:** deployed, runtime DEV verificado, PROD, migración 064 aplicada a bases reales, ni D2 PASS. D2 parte explícitamente desde este baseline y no hereda PASS.

The Lab es un subproducto analítico de Echo. La autoridad durable de estrategia e historia pertenece a Echo; Lab consume operaciones canónicas y posee únicamente curvas, puntos, métricas, dashboard/screener y derivados posteriores.

La integración con Forge es **contract-first y desacoplada de implementación**: Echo define el modelo canónico y el servicio de ingestión; Forge y cualquier productor futuro implementan por su carril cómo obtener/adaptar sus datos a ese contrato. El track Echo no inspecciona ni rediseña internals Forge salvo durante una prueba explícita de integración.

North star de la semana: **foundation Echo sólida el miércoles 23, historia auténtica integrada cuando el productor esté conforme, dashboard con curva real el viernes 25, REAL desde journal el sábado 26 y V3 usable con screener/calendario el domingo 27**. Los gates separan capacidad Echo de disponibilidad de productores externos.

## Paquete de ejecución D1 — autoridad para desarrollo

La implementación de D1 se ejecuta contra el paquete congelado en `main/10-projects/Echo/The Lab/D1 — Echo Foundation/`:

- `A — Technical SPEC D1.md`
- `B — Implementation Plan D1.md`
- `C — Test Plan D1.md`
- `D — Acceptance Gate D1.md`
- `E — Architectural Impact D1.md`
- `F — Continuity D1.md`

Para D1, este paquete tiene prioridad sobre descripciones más antiguas del roadmap cuando exista una diferencia de detalle. Las decisiones M01-M12 siguen siendo autoridad de producto/arquitectura.

## Principios operativos ratificados

- Una sola autoridad durable de operaciones: Echo.
- Una operación canónica = un trade cerrado = un cierre = una fila.
- Sólo trades cerrados; sin lifecycle/deals/legs/partial closes en V3 inicial.
- REAL inicial consume sólo operaciones Reference; copies/Execution quedan fuera.
- Símbolos exclusivamente canónicos Echo.
- SL y TP iniciales obligatorios en V3 inicial.
- Ingesta fail-closed: dato obligatorio ausente/incoherente => dataset rechazado; no degradar filas para generar curvas.
- TRAINING_DATA / PRE_REAL / REAL se derivan desde source + opened_at + A/B; no son segunda autoridad persistida por trade.
- Forge nunca escribe PostgreSQL Echo ni Lab directamente.
- Echo no conoce formatos SQX/MT5; productores adaptan al DTO canónico.
- E05/TradeSet no gobierna V3. Reutilización sólo si ayuda; nunca conservar deuda por BWC.
- trade_journal permanece autoridad operacional Echo y READ ONLY desde Lab.

## Regla operativa 23–27 septiembre 2026

Cada día inicia cerrando únicamente las decisiones del hito diario: modelo/interfaces, ownership, DDL/migración, tests, rollback y gate. Luego implementación y validación DEV. No se recorre Forge ni infraestructura por inercia.

Los productores externos avanzan en paralelo usando contratos publicados por Echo. Un productor atrasado puede bloquear un **gate de integración**, pero no bloquea terminar correctamente la capability Echo correspondiente.

Cada cierre diario registra PASS/BLOCKED/FAIL, evidencia DEV, commits, SQL counts, contratos versionados, tests y próxima acción. No declarar integración auténtica con fixtures.

## Calendario operativo

| Día | Hito principal | Echo / Lab — diseño | Desarrollo y pruebas | Gate EOD | Dependencias |
|---|---|---|---|---|---|
| **D1 MIÉ 23 — ECHO FOUNDATION** | Echo sabe representar y recibir una StrategyVersion con historia canónica | Cerrar modelo `canonical_operations`; configuración A/B por StrategyVersion; contrato `CanonicalOperationInputV1`/history; servicio de ingestión; identidad/idempotencia/reemplazo atómico; símbolos canónicos; restricciones/índices; disposición de S0/E05 sin deuda obligatoria | Implementar migración DEV, dominio/DTO SDK, validadores, repository/service y endpoint/boundary; unit + PG integration + contract tests; readback de operaciones válidas; negativos completos | **D1_PASS:** modelo y SPEC aprobados, migración DEV, servicio Echo funcional, operación/historia persistible y recuperable mediante contrato, replay/conflict/rollback probados, 0 efectos trading. **NO requiere Forge implementado** | Sólo dependencias internas Echo/SDK/Postgres. Forge recibe contrato al quedar estable |
| **D2 JUE 24 — HISTORY INGESTION / INTEGRATION** | Una StrategyVersion puede recibir TRAINING + PRE_REAL de un productor conforme | Afinar request de dataset, A/B/timezone, counts/digests, validación de ventanas, atomic replace, estados de response y separación ingestion receipt vs history readiness | Hardening del servicio Echo; pruebas E2E con productor externo cuando esté disponible; si Forge ya cumple contrato, certificar Forge→Echo con historia auténtica; si no, Echo permanece PASS y **integration BLOCKED_EXTERNAL** con requerimiento incumplido exacto | **D2_ECHO_PASS:** ingestión dual-source soportada y probada por contrato/PG. **D2_INTEGRATION_PASS:** productor real entrega TRAINING/PRE_REAL auténticos, counts/digests/rangos reconciliados, reimport idempotente/atómico. Ambos estados se reportan por separado | Carril Forge independiente. Echo no cambia modelo para acomodar limitaciones internas del productor |
| **D3 VIE 25 — FIRST CURVE** | Lab genera curvas reales desde operaciones Echo | Definir `CurveAlgorithm`, header/status, dataset fingerprint, `lab_curves` + points, bases iniciales disponibles, invalidación y métricas mínimas | Implementar al menos una curva útil (prioridad R_PIPS si inputs completos), persistencia, API/UI dashboard, selector estrategia/fechas, A/B visibles; usar historia auténtica ya integrada si existe | **D3_PASS:** estrategia real con operaciones canónicas produce curva visible; 2 puntos rastreables a trades; recálculo determinista; input insuficiente => `ERROR/INSUFFICIENT_INPUT`, nunca datos inventados | Requiere historia real para gate auténtico; capability de cálculo puede avanzar con fixtures antes |
| **D4 SÁB 26 — REAL / JOURNAL** | Echo alimenta historia REAL desde Reference | Definir mapping journal→canonical operation, watermark/correcciones, sólo cerrados, Reference/version, invalidación de curvas, scheduler/freshness | Worker READ ONLY sobre trade_journal; upsert/corrección canónica; dirty/recompute de curvas; calendario/trade detail y freshness | **D4_PASS:** operación Reference auténtica aparece una vez, replay no duplica, corrección válida converge, curvas cambian cuando corresponde, journal intacto | Si no existe Reference atribuible, reportar bloqueo físico; no usar copies como sustituto |
| **D5 DOM 27 — V3 USABLE** | Dashboard + calendario + screener sobre autoridad única | Cerrar comparabilidad de métricas, filtros, readiness y cleanup ledger | Screener, errores/estados de datos, E2E historia+REAL+recompute, regresión operacional Echo; retirar rutas Lab legacy que interfieran | **D5_PASS:** Echo canonical operations → Lab curves/metrics → dashboard/calendar/screener; REAL periódico probado; sin segunda autoridad ni side effects trading | Integración Forge auténtica se muestra si su carril alcanzó conformidad; ausencia externa no se disfraza |

## D1 — alcance exacto de foundation Echo

D1 se centra en **Echo**, no en resolver Forge.

### Modelo durable

Entidad principal conceptual: `echo.canonical_operations`.

Semántica cerrada:
- 1 fila por trade completo y cerrado.
- StrategyVersion explícita.
- `source`: SQX | MT5 | REFERENCE.
- `source_trade_id` estable.
- símbolo canónico Echo.
- side, opened_at, closed_at.
- entry_price, exit_price, stop_loss inicial, take_profit inicial.
- volume + volume_unit.
- gross_pnl, commission, swap, net_pnl, currency.
- initial_risk_money sólo cuando conocido de forma inequívoca.
- record_digest.
- timestamps técnicos mínimos de persistencia.

No almacenar en V3 inicial: account/copy identity, state lifecycle, deals, legs, partial closes, period derivado, pips/ticks/R derivados, aliases de símbolos, payload JSONB genérico, quality/provenance subsystems.

### Configuración temporal de historia

Una configuración mínima por StrategyVersion mantiene:
- A = training end, normalizado como frontera exclusiva.
- B = live start, nullable mientras no entra REAL.
- timezone usada para resolver input civil.

Periodos:
- SQX antes de A => TRAINING_DATA.
- MT5 desde A y antes de B (o sin B todavía) => PRE_REAL.
- REFERENCE desde B => REAL.

Combinaciones incoherentes se rechazan.

### Servicio de integración Echo

Echo expone un único boundary para **StrategyVersion + historia canónica**. El contrato debe cubrir:
- identity Strategy/StrategyVersion.
- canonical symbol solicitado/resuelto antes de las operaciones.
- A/B/timezone.
- datasets TRAINING y PRE_REAL independientes.
- lista de `CanonicalOperationInputV1`.
- count y digest por dataset.
- idempotency key/request identity.
- validación completa antes de commit.
- replace atómico por `strategy_version + source`.
- replay exacto => no-op.
- mismo identity/digest distinto fuera de replace explícito => conflict.
- error en cualquier operación => dataset rechazado completo.
- respuesta distingue recepción de strategy/version e historia lista para analytics.

**Echo no acepta formatos SQX/MT5 ni paths/artefactos específicos de Forge como modelo de dominio.**

### Símbolos

El request trabaja con el identificador canónico Echo. No se diseña mapping dentro de Lab ni se persiste broker symbol en canonical_operations. El productor puede necesitar resolver aliases, pero eso queda fuera del servicio canónico.

### D1 tests obligatorios

- operación válida cerrada.
- campo obligatorio faltante.
- TP/SL inválido/ausente.
- source/StrategyVersion/source_trade_id identity.
- símbolo no canónico.
- timestamp inválido y close < open.
- monetary decimal exacto.
- replay mismo digest.
- replay conflictivo.
- duplicate dentro del dataset.
- reemplazo atómico.
- fallo en mitad del replace => dataset anterior intacto.
- aislamiento por source: reemplazar SQX no toca MT5/REFERENCE.
- lectura/rango por StrategyVersion + opened_at/closed_at.
- cero activación/provisioning/trading.

Fixtures sirven para contract/unit/integration de Echo; **no certifican Forge**.

## Carril Forge — relación contractual, no scope Echo D1

Cuando el contrato Echo D1 queda congelado, Forge recibe:
- esquema DTO/wire versionado;
- campos obligatorios;
- definición canonical symbol;
- reglas temporales A/B;
- reglas económicas;
- count/digest;
- idempotencia y replace;
- códigos de error;
- contract tests/golden vectors si corresponde.

Forge decide por su lado cómo obtener SQX/MT5, cómo parsear, transformar o almacenar temporalmente. El equipo Echo sólo vuelve a mirar Forge en una sesión/gate explícito de integración.

El criterio de integración no es "Forge hizo X internamente"; es: **produce requests conformes y Echo persiste exactamente la historia esperada**.

## D3+ — ownership Lab

Sólo después de canonical_operations:
- `lab_curves`: header, algoritmo/version, basis, status, fingerprint, range, métricas.
- `lab_curve_points`: puntos reconstruibles cuando la UX/query lo justifique.
- algoritmos N versionados en Go.
- status obligatorio: READY / ERROR / INSUFFICIENT_INPUT (nombres finales en SPEC D3).
- ninguna curva es nueva autoridad de trades.

Money management, portfolio research y execution/application siguen fuera de esta semana salvo datos mínimos ya requeridos por curvas.

## Convergencia con S0 / E05 / legacy

- S0: modificar/versionar el modelo compartido para representar el contrato nuevo; no conservar shape viejo si contradice el dominio.
- E05: no es autoridad de diseño. Reusar calculator/código sólo si encaja sin dual-write ni TradeSet obligatorio.
- PG063/TradeSet: identificar consumidores antes de retirar, pero no alimentar una segunda autoridad para BWC.
- E04: puede aportar infraestructura de transporte/idempotencia si resulta limpio, pero el diseño no presupone extenderlo. El servicio de historia se define por necesidad Echo.
- Lab V1/V2: reemplazar/remover en L-CLEAN; trade_journal/Core/runtime se preservan.

## Roadmap posterior

| Fase | Alcance | Gate |
|---|---|---|
| **L-CLEAN — DEUDA V1/V2** | Retirar tablas/vistas/jobs/SDK/front/Hasura/timers exclusivos Lab legacy tras V3 usable, sin BWC artificial | 0 consumidores Lab legacy y V3 E2E PASS |
| **L5 — MONEY MANAGEMENT LAB** | N políticas de sizing sobre señales/trades canónicos, separadas de calidad de estrategia | Dos gestiones reconstruibles sobre mismos trades |
| **L6 — PORTFOLIO RESEARCH** | PortfolioVersion, miembros, pesos, curvas/DD/correlación con ventanas comparables | Portfolio reproducible sin órdenes |
| **L7 — PORTFOLIO APPLICATION** | Asignación a cuentas, políticas monetarias, reservas/comandos seguros y gate humano | DEV físico + rollback + autorización capital |
| **L8 — MONITORING & OPERATIONS** | Strategy/portfolio/account state, Reference vs Execution, freshness/gaps/alerts | Estado operacional explicable |
| **L9 — CANDLE/TICK SIMULATION** | Simular cambios de entrada/SL/TP/salidas con datos de mercado suficientes | Simulación claramente separada de observación real |

## Evidencia y cierre

D1 evidencia Echo: SPEC aprobada, migración DEV, contrato versionado, tests unit/PG/contract, SQL counts/readback y regresión de seguridad operacional.

D2 evidencia integración: request real del productor, dataset counts/digests/rangos, rows Echo y replay/reimport. Si el productor no está listo, reportar `INTEGRATION_BLOCKED_EXTERNAL` sin rebajar el gate Echo.

No cerrar sesión Agents-OS hasta que la planificación completa D1 (SPEC + implementation plan + test plan + acceptance gate + impacto + continuidad) quede aprobada por owner.
