---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Echo]]"
parent:
sprint: 2026-09-25--2026-10-02
start: 2026-09-25
due: 2026-10-02
progress: 0
repo:
jira:
prs:
aliases:
  - Echo Futures Trading Runtime
  - Echo Futures Algo Runtime
tags:
  - kind/project
  - area/echo
  - echo-futures
  - algorithmic-trading
created: "2026-09-25"
updated: "2026-10-06"
---

# Echo Futures

> [!info]+ Proyecto canónico
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Horizonte inicial:** 2026-09-25 → 2026-10-02
>
> Este proyecto reemplaza como autoridad de producto al discovery anterior, preservado en [[Echo Futures — Prop Economics Experiment]].

## 🎯 Objetivo

Extender Echo para operar **futuros algorítmicamente desde Echo Core**, con generación central de estrategias/señales, gestión de capital desacoplada, market data de baja latencia, ejecución multi-prop y replay/backtest sobre la misma semántica de runtime.

El foco completo de V1 es **futuros**. La arquitectura debe evitar dependencias innecesarias que obliguen a reescribir el Core cuando en el futuro se agreguen otros mercados —por ejemplo US smallcaps—, pero **no se implementará ningún mercado distinto de futuros en esta fase**.

El sistema debe poder comenzar con pocas cuentas y crecer **sin cambio arquitectónico** a al menos 100–200 cuentas de ejecución. El crecimiento esperado incluye decenas de cuentas de fondeo distribuidas entre múltiples futures prop firms y, posteriormente, más de un usuario/trader.

## 🧩 Problema

Echo nació como un sistema de Reference → Execution / trade replication. El dominio y runtime actual contienen piezas potencialmente reutilizables —execution planning, Money Management, account/position state, journal, bridges, observabilidad— pero fueron diseñadas alrededor de un Reference externo y no necesariamente alrededor de:

- estrategias ejecutándose dentro de Core;
- un feed de mercado canónico central;
- construcción y consulta de velas/indicadores con latencia baja;
- múltiples estrategias asociadas a una misma cuenta;
- gestión de capital stateful que pueda administrar una operación durante toda su vida;
- múltiples prop firms con reglas diferentes;
- decenas o centenas de cuentas;
- replay/backtest ejecutando la misma lógica que live.

El proyecto no asumirá que las abstracciones actuales de Echo son correctas ni que deben reemplazarse. Primero se contrastará el modelo deseado contra source real y se decidirá **reutilizar, extender, adaptar o diferir refactor**.

## 🧪 Evidencia previa

El proyecto anterior [[Echo Futures — Prop Economics Experiment]] cerró suficiente incertidumbre económica para justificar construir el runtime.

Se conserva como evidencia, no como arquitectura del producto:

- simulador D4 certificado;
- Topstep P150;
- auditoría independiente DP/MC;
- economics multi-payout;
- fair-null D5.4;
- hipótesis de hardscalping negativo/positivo;
- candidatos de estrategia S1/S2;
- research de futures props ya realizado.

Ningún contrato técnico del experimento se convierte automáticamente en decisión del nuevo sistema.

## 🧭 Principios de trabajo

### KISS / YAGNI / CLEAN / SOLID

- Resolver el problema actual de futuros con el mínimo de abstracciones necesarias.
- No construir componentes para corregir una mala configuración del usuario.
- No crear un portfolio engine antes de que exista el requerimiento de portfolios dinámicos.
- No inventar una DSL de reglas, workflow engine o microservicios sin evidencia.
- Separar responsabilidades de dominio.
- Reutilizar Echo cuando encaje; no preservar una abstracción incorrecta sólo porque ya existe.
- Diseño primero, código después.

### Futures-first, no futures-locked

Diseñar seams baratos alrededor de Market/Instrument/Feed/Calendar/Execution para evitar lock-in innecesario.

No implementar ahora:
- equities/smallcaps;
- NBBO;
- LULD;
- SSR;
- locates/borrow;
- corporate actions;
- routing entre mercados de acciones.

### Deuda obligatoria cross-market — reglas de props Forex

**DT-EF-FX-PROP-01 — DEFERRED_MANDATORY.** Echo actual también opera cuentas de props Forex y esas cuentas tienen restricciones operativas reales. Echo Futures no implementará ahora el enforcement completo de reglas Forex, pero el diseño de `Provider`, `ProviderProgram`, `ProviderRuleSet`, account policy, trading windows, news/copy/automation/drawdown constraints y provenance **no debe quedar artificialmente futures-only cuando una abstracción común sea simple y demostrable**.

Esta deuda debe atacarse en un track posterior obligatorio: auditar las props Forex actuales, formalizar sus reglas first-party y aplicar el mismo enforcement donde corresponda al Echo existente. No convertir esto en scope creep de V1 Futures.

**DT-EF-CROSS-MARKET-INSTRUMENT-02 — DEFERRED_REUSE_REVIEW.** Evaluar después de congelar Futures si el nuevo split `Instrument → physical tradable binding/Contract` puede sustituir o enriquecer el mapping físico del Echo Forex/CFD actual. El objetivo es evitar dos modelos incompatibles si una abstracción común resulta limpia. No se debe forzar expiry/rollover de futures sobre Forex/CFD: D2 sólo debe dejar un seam suficientemente general si hacerlo no agrega complejidad innecesaria.

**DT-EF-REFERENCE-SIGNAL-03 — DEFERRED_MANDATORY.** `ReferenceEvent` permanece temporalmente como contrato legacy/source-specific y como evidencia del hecho ocurrido en la cuenta reference, pero **no** es el `Signal` canónico. El nuevo motor genérico debe nacer consumiendo `Signal`; el flujo legacy se adapta dentro de Echo Core mediante un boundary explícito `ReferenceEvent -> Signal`. Bridge sigue siendo edge/transport dummy y no adquiere lógica de dominio. Iteración 2 debe completar la migración del execution path reference al boundary canónico y retirar el coupling legacy que ya no sea necesario.

**DT-EF-POSITION-RECONCILIATION-05 — DEFERRED_EDGE_CASE.** La política para una divergencia entre exposición lógica derivada de Operations/Fills y Position física reportada por la Account queda fuera del camino crítico de Futures V1. No diseñar ahora auto-repair, synthetic fills, forced remapping ni un subsystem específico de reconciliation mismatch. Reabrir sólo ante evidencia física real de que el caso ocurre o ante un transport/provider donde sea comportamiento normal/material. Mientras tanto, Operation/Fills conservan la verdad lógica y PositionSync/Position conserva la observación física independiente.

**Unidades cross-market — constraint V1.** El dominio nuevo no puede usar `pips` como unidad universal. Futures V1 necesita semántica genérica de precio/riesgo basada en instrument/contract specs (tick size, tick/point value, contract multiplier o equivalentes). El legacy Forex puede adaptarse desde pips a esas unidades. La limpieza completa de campos/schemas/workarounds legacy expresados en pips queda como deuda candidata de Iteración 2; **el ID y alcance final de esa deuda aún requieren ratificación explícita del owner**.

**Política de deuda en código:** cuando una implementación futura deje una limitación temporal, compatibility shim o camino futures-only relacionado con esta deuda, el source propietario debe llevar un marcador explícito con ID canónico —por ejemplo `DT-EF-FX-PROP-01` o un sub-ID— y enlace/comentario suficiente para encontrar el debt register. No usar `TODO` genérico sin owner/debt ID. La documentación canónica sigue siendo la autoridad; el comentario en código hace visible la deuda justo en el seam donde importa.

### Escala

Requirement de arquitectura desde V1:
- 100–200 execution accounts sin cambio de arquitectura;
- múltiples prop firms;
- múltiples estrategias;
- múltiples operaciones simultáneas;
- feed/strategy evaluation no multiplicado innecesariamente por cuenta;
- provider/execution rate limits y reconciliación tratados como límites explícitos.

QA deberá incluir carga representativa de 200 cuentas y una prueba de headroom superior si el diseño lo permite.


## ♻️ Reutilización obligatoria para Backtesting / Research Runtime

La V1 live **no implementa todavía el módulo completo de backtesting**, pero la arquitectura debe quedar preparada para construirlo inmediatamente después del primer vertical multi-prop/shadow sin reescribir Strategy ni MoneyManagement.

Objetivo posterior inmediato a V1:
- operar una primera cohorte pequeña de cuentas en shadow/demo;
- estabilizar runtime live;
- construir un módulo independiente de backtesting/replay reutilizando las mismas abstracciones;
- reutilizar sus outputs posteriormente en The Lab y en futuros workflows de construcción/selección de portfolios.

### Restricción de diseño

Las siguientes piezas deben ser reutilizables fuera del proceso live:

- Strategy;
- Signal;
- MoneyManagement;
- Operation lifecycle;
- Order/Fill semantics;
- Bar/market-event semantics;
- Instrument/Session definitions;
- Trade final.

El backtester futuro debe poder ejecutar conceptualmente:

```text
HistoricalMarketData
    -> same Market/Bar semantics
    -> same Strategy
    -> same Signal
    -> simulated AccountStrategy
    -> same MoneyManagement
    -> SimExecution
    -> Order/Fills
    -> Operation
    -> Trade
    -> Research/Lab outputs
```

No se permite crear una segunda implementación tipo:
- `strategy_live` vs `strategy_backtest`;
- `money_management_live` vs `money_management_backtest`.

La infraestructura de Core (Kafka/StateFun/bridges/etc.) puede diferir del runner de backtest. **La lógica de dominio no.**

### Lab / journal

El objetivo es preservar el valor de `Trade` como resultado común reutilizable por The Lab.

Debe diseñarse explícitamente cómo distinguir:
- LIVE;
- SHADOW/DEMO;
- REPLAY;
- BACKTEST;

sin contaminar evidencia real con resultados simulados.

La forma física de persistencia queda abierta para D2, pero el modelo debe soportar `run_id/mode/source` o equivalente.

Esto es una **constraint arquitectónica de V1**, no scope de implementación completa del backtester.

## 🗺️ Símbolos canónicos y contrato físico — REQUISITO OWNER

Echo trabaja internamente con **símbolos canónicos**.

Para futuros V1 se requiere un mapping configurable en caliente:

```text
canonical: NQ
    -> execution/feed contract: NQZ6

HOT UPDATE

canonical: NQ
    -> execution/feed contract: NQH7
```

Objetivo operativo:
- el owner controla manualmente el rollover en V1;
- Echo NO decide automáticamente cuándo rolar;
- el mapping puede cambiar sin redeploy;
- una nueva Signal/Operation posterior al cambio debe resolver inmediatamente al nuevo mapping.

### Invariante propuesto a validar en D1/D2

Una Operation ya creada debe conservar/pinear el contrato físico resuelto al momento de creación. Un hot mapping posterior **no debe mutar retroactivamente una Operation abierta**.

D1/D2 deben confirmar:
- entidad `Instrument` vs `Contract`;
- cuándo se resuelve canonical -> physical;
- cómo se persiste el mapping efectivo en Signal/Operation/Order;
- mapping separado para reference feed y execution venue cuando sea necesario;
- comportamiento con una Operation abierta durante un cambio manual.

Automatic rollover queda explícitamente fuera de V1.

## 🕒 Trading Sessions / Calendario — REQUISITO

El sistema debe poder definir y reutilizar sesiones nombradas, por ejemplo:
- New York;
- London;
- CME/RTH/ETH u otras ventanas relevantes.

Una Strategy debe poder referenciar una Session/TradingWindow configurada sin hardcodear offsets locales.

D1/D2 deben resolver:
- timezone authority;
- DST;
- holidays/early closes;
- session date;
- opening/closing boundaries;
- relación session -> bar buckets;
- igualdad semántica LIVE/REPLAY/BACKTEST.

Esto es especialmente crítico para S1 NY Opening Range 30m.

## 🧭 Front E — Contract + Session Semantics manager integration — 2026-09-26

Authority: `main/30-resources/futures/CONTRACT + SESSION SEMANTICS — AUTHORITATIVE EVIDENCE.md`.

Primary Manager review accepts the returned evidence state:

- `E_CONTRACT_SESSION_SEMANTICS = ACCEPTED_WITH_MANAGER_NORMALIZATION`
- Q6 Contract mapping = `D1_INPUT_SUFFICIENT_FOR_D2`
- Q7 Session semantics = `D1_INPUT_SUFFICIENT_FOR_D2`
- `OPERATION_CONTRACT_PINNING = STRONGLY_SUPPORTED_INFERENCE`
- Front E = `D1_MANAGER_REVIEW_CLOSED`

Accepted D1 evidence is limited to the authority resource's FACT/PATTERN/INFERENCE distinctions. Exact Instrument/Contract structs, resolver/cache, lifecycle metadata authority, TradingSession/calendar representation, ProviderProgram overlays and deterministic session→bar mechanics remain D2 technical design.

Residual unknowns about exact lifecycle timestamps, stale/inactive-contract close edges and a universal CME trade-date formula are non-blocking for D1 and must not be generalized by inference.

Front E does not close D1 by itself.

## 🔌 Execution transport — REQUISITO DE V1

La V1 no puede terminar sólo con interfaces/mocks.

D1 debe investigar varias alternativas reales asociadas a las plataformas/servicios de futures prop firms y D2 seleccionar la alternativa inicial siguiendo KISS/YAGNI/CLEAN/SOLID.

D6 debe demostrar **al menos un transporte real funcional** en shadow/demo/sim o ambiente equivalente autorizado, además del SimExecution usado para tests.

La selección debe considerar como mínimo:
- capacidad de automatización real;
- market/account/order events;
- MARKET/LIMIT/STOP;
- partial fills;
- cancel/replace;
- reconnect/reconciliation;
- API/rate limits;
- disponibilidad de entorno de prueba;
- esfuerzo de integración;
- posibilidad de reutilizar el mismo bridge/adapter entre varias prop firms.

No se obliga todavía a implementar un adapter por prop firm.

## ✅ D1 final manager checklist — READY FOR OWNER REVIEW — 2026-09-26

Owner decision recorded for Q1:

`Q1_ECHO_FIT = D1_OWNER_ACCEPTED`

Accepted conclusion:
- Echo Futures extends **Echo V3 incrementally**.
- No Core rewrite.
- No separate Futures runtime/system.
- Reuse existing infrastructure/patterns where semantics fit.
- Adapt/replace boundaries whose current semantics are incompatible with the new canonical domain.

Final D1 readiness review:

| Q | D1 status |
| --- | --- |
| Q1 Echo fit | `D1_OWNER_ACCEPTED` |
| Q2 Position attribution | `D1_INPUT_SUFFICIENT_FOR_D2` |
| Q3 Order lifecycle | `D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS` |
| Q4 Market hot state | `D1_INPUT_SUFFICIENT_FOR_D2` |
| Q5 Bar semantics | `D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS` |
| Q6 Contract mapping | `D1_INPUT_SUFFICIENT_FOR_D2` |
| Q7 Session semantics | `D1_INPUT_SUFFICIENT_FOR_D2` |
| Q8 Feed authority | `D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS` |
| Q9 Execution transport | `D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS` |
| Q10 Provider model | `D1_INPUT_SUFFICIENT_FOR_D2` |
| Q11 Strategy runtime | `D1_INPUT_SUFFICIENT_FOR_D2` |
| Q12 S2 | `READY_FOR_D4` by planned owner day |
| Q13 Gerard +/- | `READY_FOR_D4` by planned owner day |
| Q14 Backtest boundary | `D1_INPUT_SUFFICIENT_FOR_D2` |
| Q15 Trade/Lab | `DEFERRED_TO_THE_LAB` by owner decision |
| Q16 Blocking refactor | `D1_INPUT_SUFFICIENT_FOR_D2` |

Manager conclusion:
- No remaining D1 UNKNOWN changes a domain identity/lifecycle, hot-path feasibility, execution feasibility, mapping/session semantics or backtest reuse boundary.
- Residual transport entitlement, capacity benchmark, contract lifecycle timestamp authority and edge-case recovery details are scoped to D2/implementation and are not D1 discovery blockers.
- Q12/Q13 intentionally close in D4 and therefore do not block the D1 evidence gate.
- Q15 is explicitly outside the Echo Futures critical path.

`EF_D1_ANALYSIS_PASS = PASS`

**Owner acceptance:** 2026-09-26. D1 is closed. D2 — Domain + Technical Architecture is the active milestone.

## ⚠️ Critical Design Register

Este registro distingue requisitos ya definidos, propuestas pendientes de validación y preguntas bloqueantes.

### Owner decisions — D1 A1/A2 review — 2026-09-26

**Regla operativa del manager:** ante una brecha material de requisitos, identidad, lifecycle, ownership o semántica de dominio, el manager **pregunta al owner antes de decidir**. No completa huecos por inferencia. Puede resolver decisiones técnicas ordinarias sólo cuando los requisitos y boundaries ya están claros.

**Arquitectura común / cross-market**
- Echo debe converger a motores genéricos; no habrá un motor lógico Forex y otro Futures.
- Los dos motores transversales identificados son **Strategy Engine** y **Market Feed Engine**.
- El motor genérico nuevo se diseña correctamente desde V1; lo incremental es la migración de productores/paths legacy, no mantener dos arquitecturas finales.
- KISS no habilita shortcuts que rompan SOLID/Clean boundaries. Si el refactor correcto es pequeño se hace; si amenaza V1 se usa un seam limpio + DT explícita para Iteración 2.

**Strategy / Signal**
- `Strategy` es identidad/definición/configuración canónica.
- **StrategyEngine** es el nombre aceptado para el runtime que ejecuta estrategias cuya lógica vive dentro de Echo. El nombre/forma de la implementación concreta de cada estrategia queda abierto para D2; no se congela `StrategyAlgo`.
- Echo debe aceptar dos orígenes indistinguibles aguas abajo: estrategias internas ejecutadas por StrategyEngine y estrategias externas/reference.
- Ambos orígenes convergen al **mismo canonical `Signal`** antes del generic execution path.
- `ReferenceEvent` NO es `Signal`: representa un hecho ya ejecutado en una reference y conserva ticket, lotaje, broker, precio y metadata legacy.
- El adapter `ReferenceEvent -> Signal` vive en **Echo Core**, en un boundary explícito antes del motor genérico. Bridge no genera Signals ni recibe lógica de dominio.
- TradeJournal puede seguir consumiendo/persistiendo `ReferenceEvent` como evidencia legacy mientras el execution path migra progresivamente.
- Una Strategy puede producir **0..N Signals** a lo largo del tiempo y más de una Signal como resultado de una misma evaluación.
- `Signal` representa intent, no sólo entry. Intents conceptuales aceptados para el modelo: `OPEN`, `REDUCE`, `CLOSE`, `CLOSE_ALL`; el enum definitivo queda para D2.
- **Boundary owner:** Strategy contiene la lógica **técnica** de trading; MoneyManagement contiene la lógica **económica/de dinero y riesgo** por AccountStrategy.
- Strategy decide **qué** quiere hacer y puede emitir contexto técnico de ejecución: dirección, entry intent/tipo/precio cuando corresponda y **puede** proponer niveles técnicos de SL/TP. Strategy nunca hace sizing ni decide riesgo monetario de la cuenta.
- MoneyManagement decide **cuánto y cómo** materializar la intención para esa cuenta: sizing, riesgo monetario, exposición, adds/reductions, protección/targets ejecutables y gestión posterior de la Operation.
- Ejemplo conceptual: Strategy puede decir `OPEN LONG ahora; technical SL=P1; technical TP=P2`; MoneyManagement puede resolver `riesgo=$200; objetivo=$300; quantity=N` y generar/gestionar las Orders correspondientes.
- **OPEN pendiente:** cuando Strategy entrega SL/TP técnicos y MoneyManagement aplica reglas monetarias/hardscalping, la precedencia exacta y si MoneyManagement puede alterar los niveles técnicos iniciales **no se congela todavía**. Se resolverá al mecanizar hardscalping/Q13; no asumir override ni immutability.
- Es válido que exista una Strategy con lógica técnica de hardscalping y un MoneyManagement con lógica monetaria de hardscalping: son responsabilidades distintas mientras no dupliquen ownership de la misma decisión.
- Cuando una misma evaluación emite varias Signals y el orden cambia el resultado —por ejemplo `CLOSE_ALL` seguido de `OPEN` para reversal— el procesamiento debe ser determinístico.
- Signal tiene ventana explícita de validez (`created_at` + `valid_until` o equivalente). Una Signal expirada **no puede materializar una Operation**. El legacy `MaxOpenDelaySeconds` puede adaptarse a esta semántica sin convertirse en autoridad del nuevo dominio.

**AccountStrategy / MoneyManagement**
- El nombre canónico es **MoneyManagement**, no CapitalManagement.
- `AccountStrategy` vincula Account + Strategy + MoneyManagement y debe evolucionar a partir del binding/policies actuales sin mezclar responsabilidades legacy innecesarias.
- MoneyManagement administra una Operation durante todo su lifecycle, no sólo el sizing inicial.
- Debe poder abrir, añadir exposición, reducir, mover stop/target y cerrar según su lógica.
- Debe poder reaccionar a Signal, fills/order events, account/instrument state, lifecycle/session events y market state/bars, incluyendo múltiples timeframes cuando la estrategia de gestión lo requiera.
- Strategy tiene acceso **READ ONLY** a las Operations relevantes. MoneyManagement también accede al estado de sus Operations; la topología/cache/state owner físico se decide después y no se asume en D1.

**Operation / Order / Fill / Position / Trade**
- Un `OPEN`-like Signal aceptado para una AccountStrategy **materializa la Operation antes de ejecutar MoneyManagement y antes de cualquier Order/Fill**.
- La Operation existe aunque MoneyManagement no consiga resolver una acción ejecutable, rechace la entrada, falle, o la Signal/entry expire antes de obtener Fill. En esos casos termina como Operation terminal con motivo explícito para trazabilidad.
- Una Operation sin Fill **no implica Position física**; Position continúa representando sólo estado físico observado/reconciliado de la Account.
- Signals posteriores de gestión/salida (`REDUCE`, `CLOSE`, `CLOSE_ALL`) actúan sobre Operations existentes y no crean una Operation nueva por defecto.
- Operation es la unidad lógica administrada por MoneyManagement y puede producir N Orders.
- Lifecycle conceptual mínimo aceptado:
  - `CREATED`: la Operation ya existe; MoneyManagement aún está resolviendo qué hacer.
  - `PENDING_ENTRY`: existe al menos una Order de entrada viva/working intentando obtener exposición, pero todavía no existe Fill.
  - `ACTIVE`: comienza con el **primer Fill que genere exposición**, incluso si el Fill es parcial y quedan cantidades/Orders pendientes.
  - `TERMINAL`: la Operation ya no puede producir nuevas acciones; debe conservar reason explícito.
- `PENDING_ENTRY` es distinto de `CREATED`: una LIMIT/STOP working en el mercado ya constituye una situación operacional material aunque aún no exista Position.
- Un estado de Order (REJECTED/CANCELLED/EXPIRED/etc.) **no termina automáticamente** la Operation; MoneyManagement puede decidir retry, reemplazo u otra acción.
- Volver a exposición lógica cero **no implica TERMINAL por sí solo**. Para terminar deben cumplirse al menos: exposición lógica cero, ninguna Order viva asociada y decisión de MoneyManagement de no continuar el lifecycle. Los nombres exactos de terminal reasons quedan abiertos.
- La **dirección de una Operation es inmutable** durante todo su lifecycle.
- La exposición lógica de una Operation se deriva de sus Fills asociados; puede aumentar, reducirse y llegar temporalmente a cero.
- Una Operation **no puede cruzar de LONG a SHORT ni de SHORT a LONG**. Un reversal se expresa como cierre/reducción de la Operation existente + una nueva `OPEN Signal` que materializa otra Operation en dirección opuesta.
- `Position` continúa siendo la exposición física observada de la Account y puede agregar/netear múltiples Operations; no se usa como sustituto de la exposición lógica por Operation.
- Order es una instrucción concreta de execution; Order puede producir 0..N Fills.
- Fill es un hecho de ejecución inmutable.
- `Position` NO es Operation. Position es una **proyección/snapshot del estado físico observado en una Account**, usada para reconciliación y superficies como el front.
- Position pertenece a `Account`; provider/broker/venue es contexto de esa cuenta. Su identidad/cardinalidad exacta depende del execution model y queda para D2.
- No se promoverá Position a aggregate rico si no existe un requisito concreto: su función mínima es responder qué exposición física tiene realmente una Account y permitir contrastarla contra el estado lógico de Operations.
- La resolución de mismatches entre exposición lógica y Position física queda diferida en `DT-EF-POSITION-RECONCILIATION-05`; no bloquea D1/D2/V1.
- Trade/The Lab permanece fuera de A2 y diferido al proyecto The Lab; no condiciona este lifecycle runtime.

**Estado de revisión**
- A1 Strategy/Signal/AccountStrategy/MoneyManagement: **MANAGER_REVIEW_ACCEPTED_WITH_OWNER_CORRECTIONS**.
- A2 Operation/Order/Fill/Position: **D1_OWNER_REVIEW_ACCEPTED**. Los detalles exactos de Order lifecycle/transport quedan para Q3/D2. Trade/Lab integration: **DEFERRED_TO_THE_LAB**.
- D1 completo sigue **IN_PROGRESS** y `EF_D1_ANALYSIS_PASS = NOT_EVALUATED`.

### A2 evidence review — Trade / trade_journal / The Lab — 2026-09-26

Revisión explícita del proyecto The Lab V3 y source Echo `master@372af59a7b83604781346613da01e3d510ea1360`.

**Hechos actuales:**
- `echo.trade_journal` es un ledger operacional **por cuenta**, con identidad `trade_id + account_id`, roles REFERENCE/EXECUTION y lifecycle persistido OPEN/CLOSED/FAILED. No deriva trades desde `Position`.
- The Lab V3 ratificó para su historia canónica analítica: **una fila por trade completo**, sólo trades cerrados; D1-M08 lo expresa como `1 operación = 1 cierre = 1 trade = 1 row`. Ese contrato inicial excluye open trades, partial closes, deals y legs.
- REAL de The Lab consume exclusivamente trades REFERENCE cerrados; EXECUTION/copy queda fuera de la historia de calidad de estrategia y se reserva para análisis posterior de fidelity/slippage.
- `echo.canonical_operations` ya existe como autoridad durable de historia canónica cerrada para SQX/MT5 y luego REFERENCE. The Lab consume canonical operations; no posee el lifecycle live.
- D4 de The Lab actual aún no ingiere `trade_journal`; esa convergencia REAL/journal quedó desplazada al siguiente hito.

**Implicación para Echo Futures — NO congelada todavía:**
- `Position -> Trade` **no encaja naturalmente** como boundary general porque Position es estado físico de Account y puede contener exposición agregada/netted proveniente de múltiples Operations/Strategies.
- `Operation -> Trade` es el candidato más alineado con el modelo analítico actual: una Operation lógica termina y puede proyectar un Trade cerrado. Position participa como evidencia/reconciliación física, no como autoridad de identidad del Trade.
- Pero el runtime Futures introduce adds/reductions/partial fills mientras el contrato analítico The Lab V3 inicial fue deliberadamente simplificado a un solo trade completo sin partial-close model. **No se debe asumir que el schema analítico actual puede representar sin pérdida toda la microestructura de una Operation compleja.**
- Posible seam a evaluar en D2: conservar Order/Fill como detalle operacional y proyectar al cierre un Trade/resumen por Operation para journal/canonical history. La semántica exacta de entry/exit/volume agregados y tratamiento de partial reductions queda abierta.
- Pregunta adicional material: para estrategias internas sin Reference externo, definir qué resultado constituye la historia canónica de estrategia que alimentará The Lab. No asumir que una AccountStrategy de ejecución cualquiera se convierte automáticamente en la autoridad analítica de Strategy Quality.

**Estado superseded por owner — 2026-09-26:** el análisis de `Trade` y su proyección hacia `trade_journal` / `canonical_operations` / The Lab queda **DEFERRED_TO_THE_LAB**. No bloquea Echo Futures D1/D2 ni el runtime V1. The Lab está en construcción y puede romper/rediseñar su modelo para alinearse posteriormente con las nuevas abstracciones canónicas de Echo.

**Decisión vigente:**
- A2 continúa sólo con `Operation / Order / Fill / Position`.
- No se congela todavía `Operation -> Trade`, `Position -> Trade` ni el shape de Trade.
- No se adapta el nuevo runtime para conservar el modelo analítico simplificado actual de The Lab.
- `trade_journal` y `canonical_operations` actuales se consideran contexto/legacy analytical boundaries, no autoridad sobre el nuevo lifecycle.
- La integración Trade/The Lab se reabre en el propio proyecto The Lab cuando Echo Futures haya estabilizado las abstracciones de runtime.
- El futuro análisis debe partir del nuevo modelo de Echo, no del supuesto histórico Reference→Execution/MetaTrader.
- La arquitectura Futures debe seguir siendo **cross-market**, evitando semántica específica de Futures en el Core común cuando no sea necesaria, para permitir una evolución posterior hacia mercados como US smallcaps sin crear otro motor.

### Requisitos/decisiones del owner ya establecidos

- Futures V1 corre sobre/extendiendo Echo; no crear un segundo sistema independiente.
- Strategy vive lógicamente en Core y emite Signal.
- Signal incluye direction + entry type `MARKET|LIMIT|STOP` + entry/trigger cuando corresponda. Puede incluir SL/TP técnicos; la obligatoriedad/combinaciones exactas quedan para el contrato D2 y hardscalping Q13.
- Signal no define sizing ni provider/account.
- Strategy se asocia a cuentas mediante AccountStrategy.
- Una Signal fan-out a todas las AccountStrategy habilitadas que referencian esa Strategy.
- Echo no corrige automáticamente duplicados/conflictos causados por una mala configuración de estrategias.
- AccountStrategy V1 selecciona un MoneyManagement.
- MoneyManagement administra la Operation completa, no sólo sizing inicial, y puede reaccionar a market bars/events.
- V1 debe poder expresar hardscalping Gerard negativo y positivo.
- Trade continúa siendo el resultado cerrado consumido por `trade_journal` / The Lab.
- Escala de arquitectura V1: 100–200 cuentas sin rediseño.
- Símbolos internos canónicos + mapping físico actualizable hot.
- Rollover automático fuera de V1; lo administra manualmente el owner.
- Sesiones deben ser configurables y consistentes entre live/replay/backtest.
- La arquitectura debe permitir un módulo independiente de backtesting posterior reutilizando Strategy + MoneyManagement.
- V1 debe demostrar al menos un execution transport real.
- Dynamic portfolios, smallcaps y multi-MoneyManagement por AccountStrategy quedan fuera de V1.

### Propuestas fuertes a validar en D1/D2

- Para Signals de apertura: una Signal aceptada puede materializar una Operation por AccountStrategy. Signals de gestión/salida pueden apuntar a Operations existentes y no implican una nueva Operation.
- Operation existe desde que se materializa la intención de esa cuenta, incluso con entry order WORKING sin fill.
- `Operation 1 -> N Orders`.
- `Order 1 -> N Fills`.
- Fill es un hecho de ejecución inmutable.
- Position representa exposición física/reconciliada Account×Instrument y no es sinónimo de Operation.
- `Operation 1 -> 0..1 Trade` al cerrar.
- una Operation pinnea el contrato físico resuelto al crearse;
- live y backtest comparten domain semantics pero no necesariamente runtime/infrastructure;
- modo/source/run-id diferencia trades live vs simulated para Lab/research.

### Preguntas críticas aún sin responder — OWNER DAY OBLIGATORIO

Cada pregunta tiene un **día máximo de resolución**. No puede arrastrarse silenciosamente al día siguiente.

| # | Pregunta | Día máximo | Qué significa RESUELTA |
|---|---|---|---|
| Q1 | **Echo fit físico:** ¿qué abstractions/source actuales de Core/SDK/Bridge/Gateway se REUSE/EXTEND/ADAPT/REPLACE? | **D1** | Source real inspeccionado y matriz de fit completa, incluyendo gaps que puedan alterar arquitectura. |
| Q2 | **Position attribution:** ¿cómo se atribuyen fills y exposición a múltiples Operations sobre el mismo instrumento bajo netting/hedging? | **D2** | Semántica e invariantes elegidos, incluyendo reconciliación y ownership lógico/físico. |
| Q3 | **Order lifecycle:** estados exactos y comportamiento de partial fill/reject/cancel/replace. | **D2** | Lifecycle candidato completo y consistente con al menos el transport seleccionado. |
| Q4 | **Market hot state:** dónde viven ticks/bars/indicators, ownership/concurrency, warmup/restart y persistence. | **D2** | Arquitectura de estado caliente + recuperación + persistencia definida. |
| Q5 | **Bar semantics:** timestamps, bucket boundaries, volume, forming/closed, late/out-of-order events. | **D2** | Contrato de Bar único para LIVE/REPLAY/BACKTEST. |
| Q6 | **Contract mapping:** momento exacto de canonical→physical resolution y comportamiento de Operations abiertas durante hot mapping. | **D2** | Instrument/Contract/mapping semantics congeladas como candidato; rollover automático sigue fuera de V1. |
| Q7 | **Session semantics:** timezone/DST/holidays/early closes y cómo impactan bars/strategies. | **D2** | TradingSession/Calendar contract definido y aplicable a S1. |
| Q8 | **Feed authority:** fuente primaria/backups, failover y gap reconciliation. | **D2** | Authority/failover/recovery contract elegido. |
| Q9 | **Execution transport:** qué alternativa real mínima se selecciona para V1 y qué provider cohort puede reutilizarla. | **D2** | D1 demuestra feasibility real; D2 selecciona transport inicial y boundary adapter/bridge. |
| Q10 | **Provider model:** Provider/Program/RuleSet y taxonomía real después del Prop Universe census. | **D2** | Modelo candidato soporta el corpus relevante sin giant switch/overengineering. |
| Q11 | **Strategy runtime:** cuándo corren Strategy y MoneyManagement (tick, forming bar, closed bar, other events), state ownership e interfaces. | **D2** | Interfaces/event model/state ownership definidos. |
| Q12 | **S2:** confirmar o reemplazar H4 trend + 5m Bollinger pullback. | **D4** | Segunda estrategia mecánica exacta incluida en SPEC de desarrollo. |
| Q13 | **Gerard +/- exacto:** parámetros/config/state transitions necesarios para una primera implementación determinista. | **D4** | MoneyManagement V1 completamente mecanizable; cero decisión humana ambigua requerida para desarrollo. |
| Q14 | **Backtest boundary:** qué paquetes/contratos deben quedar libres de dependencias live para que el runner independiente sea barato de construir. | **D2** | Boundary explícito que permite reutilizar Strategy/MoneyManagement/domain sin Core live. |
| Q15 | **Trade/Lab compatibility:** qué campos existentes se preservan, cuáles se extienden y cómo se distinguen live vs simulated. | **D2** | Contrato Trade→trade_journal→Lab y provenance/mode resueltos. |
| Q16 | **Blocking refactor:** si Echo actual impide alguna capacidad, ¿se resuelve ahora o queda DT/Core V3? | **D2** | Cada gap de D1 queda clasificado como adaptación/refactor <=1 día o DT no bloqueante con impacto explícito. |

### Estado D1 después de corrección del owner — 2026-09-25

El intento inicial de cierre fue prematuro: el manager ejecutó demasiado discovery/research y avanzó readiness sin recorrer el gate con el owner. [[Echo Futures — D1 Analysis Pack]] se conserva como **PRELIMINARY MANAGER ADVANCE**, no como cierre.

| Q | Estado actual | Nota |
|---|---|---|
| Q1 | **CANDIDATE_FOR_OWNER_REVIEW** | Source audit V3 y matriz preliminar existen; deben revisarse con el owner antes de cerrar. |
| Q2 | **OPEN_D1_INPUTS_AVAILABLE** | Inputs preliminares disponibles para preparar D2; no readiness aceptada todavía. |
| Q3 | **OPEN_D1_INPUTS_AVAILABLE** | Inputs preliminares; completar corpus de transport/lifecycle según plan D1. |
| Q4 | **OPEN_D1_RESEARCH_REQUIRED** | Scouting LEAN/Nautilus existe; falta deep research dedicado. |
| Q5 | **OPEN_D1_RESEARCH_REQUIRED** | Debe cerrarse evidence contract de bars/live/replay mediante research delegado. |
| Q6 | **OPEN_D1_INPUTS_AVAILABLE** | Contract/mapping preliminar; considerar reuse posterior en Forex/otros mercados. |
| Q7 | **OPEN_D1_INPUTS_AVAILABLE** | Sessions/calendar preliminar; falta review guiada. |
| Q8 | **OPEN_D1_RESEARCH_REQUIRED** | Feed authority/failover necesita research delegado. |
| Q9 | **OPEN_D1_RESEARCH_REQUIRED** | Families preliminares encontradas; feasibility final depende del corpus real de props. |
| Q10 | **OPEN_D1_RESEARCH_REQUIRED** | El sample del manager NO sustituye [[Echo Futures — Futures Prop Universe]]. |
| Q11 | **OPEN_D1_INPUTS_AVAILABLE** | Source audit preliminar; diseño sigue en D2. |
| Q12 | **READY_FOR_D4** | Owner day permanece D4. |
| Q13 | **READY_FOR_D4** | Owner day permanece D4. |
| Q14 | **OPEN_D1_RESEARCH_REQUIRED** | Backtest boundary debe contrastarse con market-data/runtime research. |
| Q15 | **OPEN_D1_INPUTS_AVAILABLE** | Trade/Lab source audit preliminar; diseño queda D2. |
| Q16 | **OPEN_D1_INPUTS_AVAILABLE** | Refactor register preliminar; sólo se cierra después de revisar todos los frentes D1. |

**Gate actual:** `EF_D1_ANALYSIS_PASS = NOT_EVALUATED`.

D1 se cierra únicamente después de revisar el checklist completo con el owner. El manager puede declarar `READY_FOR_OWNER_REVIEW`; no self-accept.

### Closure policy de preguntas

- **D1 no pasa con Q1 abierta.**
- D1 además debe producir evidencia suficiente para que Q2–Q11 y Q14–Q16 puedan resolverse en D2 sin volver a discovery general.
- **D2 no pasa con ninguna Q2–Q11 o Q14–Q16 abierta.**
- D3/Astra puede descubrir findings nuevos, pero éstos no se convierten en deuda abierta: cada finding aceptado debe quedar asignado a **D4**.
- **D4 no pasa con Q12/Q13 ni con ningún finding aceptado de Astra sin resolver.**
- Desde D5 en adelante **no se permiten preguntas de arquitectura/producto abiertas**. Cualquier contradicción nueva produce `DAY_BLOCKED_DECISION` o `DAY_FAIL`; nunca se arrastra silenciosamente.
- Toda pregunta nueva descubierta por un manager debe registrarse inmediatamente con `owner_day`. Si afecta una decisión que ya debía estar frozen, bloquea el gate activo.
- El proyecto no puede llegar a D5 con “TBD”, “por definir”, “pendiente investigar” o equivalente en contratos necesarios para implementar V1.

### Blocker policy

D1 no debe cerrar mientras exista un UNKNOWN que pueda cambiar:
- domain identities/lifecycles;
- hot-path architecture;
- execution feasibility;
- mapping/session semantics;
- backtest reuse boundary.

Los UNKNOWN de parámetros concretos de Strategy S1/S2/Gerard pueden cerrarse en D2/D4 siempre que no cambien las abstracciones.

## 🧠 Modelo de dominio — PROPUESTA A VALIDAR

> [!warning]+ No está frozen
> Todo este bloque captura lo acordado con el owner como **propuesta de diseño**. D1/D2 deberán contrastarlo contra Echo real, implementaciones de referencia y requisitos de props antes de congelarlo. Sólo los requisitos explícitos del owner son binding.

### Strategy

Entidad/configuración que procesa market state y emite Signals.

Responsabilidad: detectar una oportunidad de trading.

No decide:
- cuenta;
- provider;
- cantidad;
- riesgo monetario;
- progression/recovery de capital;
- reglas de fondeo.

V1 debe soportar múltiples Strategies concurrentes.

### Signal

Salida de una Strategy.

Campos candidatos:
- signal_id;
- strategy_id/version;
- market/instrument;
- side;
- entry_type = MARKET | LIMIT | STOP;
- entry/trigger price cuando corresponda;
- initial stop loss;
- initial take profit;
- created_at;
- optional validity/expiry;
- metadata/reason.

La Signal define la tesis de entrada/SL/TP, **no sizing**.

### Account ↔ Strategy

Una Strategy se asocia explícitamente a Accounts.

Una Signal se activa para **todas las cuentas que tengan esa Strategy configurada y habilitada**.

No existe en V1 un componente que fusione, priorice o “corrija” señales conflictivas/duplicadas.

Si una cuenta configura S1 y S2 y ambas emiten una entrada equivalente, ambas se procesan. Esa situación es responsabilidad de configuración.

Los portfolios dinámicos futuros modificarán asociaciones Strategy↔Account; están fuera del scope V1.

### AccountStrategy

Relación propuesta:

```text
AccountStrategy
  account_id
  strategy_id
  money_management_id
  enabled
  config
```

V1: una relación AccountStrategy usa un MoneyManagement.

Múltiples MoneyManagement simultáneos por relación quedan YAGNI/futuro.

### MoneyManagement

Objeto/política stateful configurable que administra una Operation desde la entrada hasta quedar cerrada.

No se limita al sizing inicial.

Debe poder reaccionar a:
- Signal inicial;
- cada Bar/evento de mercado requerido;
- Fill;
- cambios de Order;
- Account state;
- lifecycle/session events necesarios.

Acciones candidatas:
- OPEN;
- ADD;
- REDUCE;
- MOVE_STOP;
- MOVE_TARGET;
- CLOSE;
- NOTHING.

Debe poder expresar desde V1 la familia Gerard de hardscalping negativo y positivo sin convertirla en un framework genérico.

### Operation

Concepto lógico propuesto:

> lifecycle lógico de una oportunidad/intención materializada para una AccountStrategy concreta y administrada por MoneyManagement.

Se crea aunque una orden de entrada quede pendiente, por ejemplo una LIMIT aún sin fill.

Una Operation:
- conserva provenance hacia la Signal que la originó y pertenece a Account + AccountStrategy;
- mantiene lifecycle propio;
- es administrada por MoneyManagement;
- puede producir múltiples Orders;
- puede sobrevivir a partial fills/adds/reductions/modificaciones;
- termina cuando su exposición lógica queda cerrada/flat.

### Order

Instrucción concreta resuelta por Echo y enviada a un execution venue.

Propuesta:
- una Operation puede producir N Orders;
- la entrada inicial es una Order;
- add/reduce/exit/replace/cancel pueden producir Orders/commands adicionales según el contrato final.

Debe alinearse con los contratos actuales de Echo antes de congelar nombres.

### Fill

Hecho de ejecución reportado por el venue/broker.

Propuesta:
- una Order puede tener 0..N Fills;
- Fill es inmutable;
- live y simulation/replay comparten la misma semántica de Fill.

### Position

Concepto aún por validar cuidadosamente.

Propuesta inicial:
> exposición física actual reportada/reconciliada para Account × Instrument.

No se asume `Position == Operation`.

Varias Operations del mismo instrumento pueden contribuir a una Position física, especialmente en cuentas/plataformas con netting.

Este punto requiere diseño explícito de attribution/reconciliation antes del freeze.

### Trade

Registro final cerrado e inmutable derivado de una Operation terminada.

Objetivo de continuidad:
- todo Trade continúa alimentando `trade_journal`;
- The Lab consume ese journal para análisis;
- mantener este contrato cuando sea posible.

Propuesta V1:
`Operation 1 -> 0..1 Trade`.

Un Trade puede resumir múltiples Orders/Fills de entrada, adds, reductions y salida.

## 🎛️ Estrategias V1 — PROPUESTA

V1 debe comenzar con dos estrategias mecánicas.

### S1 — NY Opening Range Breakout 30m

Propuesta heredada del experimento:
- rango primeros 30 minutos de la sesión NY definida;
- ruptura high/low;
- entrada MARKET;
- reglas exactas/timezone/re-entry deben cerrarse durante D1/D2.

### S2 — candidata por confirmar

El experimento anterior dejó como candidata **H4 trend + 5m Bollinger pullback**.

El owner no la confirma todavía como definitiva. D1 debe recuperar el contexto existente y confirmar/corregir S2 antes del freeze.

### Capital Management V1

Debe soportar desde el primer release los dos comportamientos Gerard que se decidan congelar:
- hardscalping negativo / adverse recovery;
- hardscalping positivo / favorable add/protection.

Los triggers, tamaños y movimientos exactos se diseñarán y validarán antes de desarrollo.

## 📈 Market data — D1 Front B manager review — 2026-09-26

Research artifact: `main/30-resources/futures/MARKET DATA + QUANT ENGINE FORENSICS.md`.

**Manager verdict:** `B_MARKET_DATA_RESEARCH = ACCEPTED_WITH_CORRECTIONS`.

El research aporta patrones suficientes para preparar D2 en Q4/Q5/Q14, pero contiene inferencias presentadas como hechos y no cierra Q8. Correcciones de autoridad:

- LEAN sí soporta múltiples live data providers con **precedence order**; esto sirve como evidencia de source authority por cobertura, pero NO demuestra health-based automatic failover para el mismo stream.
- LEAN consolidators pueden agregar ticks o barras menores en barras mayores y existen sequential consolidators. Además exponen working/current data; por tanto no asumir que “forming bars nunca son visibles”. Echo debe modelar forming vs closed explícitamente.
- El requisito Echo NO es “usar sólo closed bars”: Strategy/MoneyManagement pueden requerir forming bars. El invariante correcto es impedir look-ahead accidental y reproducir la misma semántica temporal en replay/backtest.
- Nautilus `Cache` es un store in-memory central por nodo con backing opcional. El backing NO restaura bounded market-data histories ni convierte varios nodos en cache distribuida coherente.
- Nautilus comparte Strategy/ExecutionAlgorithm y core components entre backtest/live, pero live añade venue/transport/timing/persistence/external activity/reconciliation. No inferir “live determinista” ni exigir misma infraestructura física.
- Event sourcing/event store de Nautilus es evidencia de una opción de replay/audit, NO requisito para Echo. No introducir event-sourcing por inercia.
- Claims sobre “buffering por instrumento”, auto-ordering de out-of-order events, live state-ready automático y automatic feed failover no quedaron demostrados por el artefacto y se consideran `UNVERIFIED`.
- Las comparaciones Lean-vs-Nautilus para 100–200 cuentas son heurísticas arquitectónicas, no benchmark/evidencia de capacidad.
- “feed compartido vs uno por cuenta” NO es owner question: Echo ya exige no multiplicar feed/strategy evaluation innecesariamente por account.
- “StateFun vs microservice” es decisión técnica D2 del manager, no decisión de producto del owner.

**Readiness tras review:**
- Q4 Market hot state: `D1_INPUT_SUFFICIENT_FOR_D2`.
- Q5 Bar semantics: `D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS`.
- Q14 Backtest boundary: `D1_INPUT_SUFFICIENT_FOR_D2`.
- Q8 Feed authority/failover: `TARGETED_RESEARCH_REQUIRED`.

Q8 requiere un follow-up acotado sobre authority, gap detection, reconnect/resubscribe, health-based failover y recovery. No repetir el research completo de quant engines.

### B2 — Feed Authority / Failover manager review — 2026-09-26

Research artifact: `main/30-resources/futures/MARKET DATA + QUANT ENGINE FORENSICS V2.md`.

**Manager verdict:** `B2_FEED_AUTHORITY_RESEARCH = ACCEPTED_WITH_CORRECTIONS`.

El B2 aporta evidencia suficiente para cerrar el gap D1 de Q8 y pasar la decisión técnica a D2.

**Evidencia aceptada:**
- CME MDP usa arquitectura dual-feed A/B y recomienda arbitration simultánea entre ambos feeds equivalentes para mitigar packet loss/missed messages; esto es redundancia dentro de una misma autoridad lógica, no blending de vendors heterogéneos.
- CME dispone de sequence/gap/recovery primitives y feeds de snapshot/replay para reconstrucción.
- Databento expone heartbeat configurable, reconnect policy, reconnect callback con rango temporal de desconexión, intraday replay, natural refresh y MBO snapshot.
- Databento documenta recuperación exact-once-ish mediante `ts_event` + count por schema/instrument y filtrado explícito de duplicados tras replay.
- Un stream recuperado necesita una barrera de readiness antes de volver a alimentar decisiones nuevas si el estado derivado quedó incompleto.

**Correcciones manager:**
- Databento **sí expone `sequence`** del mensaje original del venue; no registrar “Databento no tiene sequence visible”.
- CME MDP 3.0 **sí posee Admin Heartbeat (35-MsgType=0)**; no registrar “CME no envía heartbeat”.
- Un salto entre timestamps NO prueba por sí solo que faltó market data: mercados válidamente pueden estar sin eventos. Gap detection debe usar primitives del source cuando existan (sequence, reconnect interval, replay/snapshot status) y separar `connection/session liveness` de `market-event freshness`.
- No congelar un timeout universal tipo “sin tick por X segundos”: depende de session/instrument/schema y es parámetro técnico/configurable, no decisión owner.
- No aceptar como hecho que CME TCP/recovery se use “sólo en reposo/arranque”; el report no aporta evidencia suficiente para esa restricción.
- “Closed bars son definitivas y nunca se reconstruyen” tampoco queda demostrado como regla universal. Late-event/correction policy se diseña en D2.
- El B2 mezcla recomendaciones de Echo con hechos externos. El principio útil es preservar authority/recovery provenance; la forma física de metadata queda D2.
- Las preguntas finales marcadas OWNER sobre blending, health thresholds, forming-bar recovery y warmup son **TECHNICAL D2** bajo los requisitos ya dados; no requieren decisión de producto del owner salvo que aparezca un trade-off operacional material.

**Inputs que D2 debe resolver, ya con evidencia suficiente:**
1. Un canonical market stream tiene una autoridad lógica explícita por Instrument/Contract/schema.
2. Redundancia equivalente dentro de la misma autoridad (como CME A/B) puede arbitrarse/deduplicarse.
3. Vendors/feeds heterogéneos no se mezclan silenciosamente; cualquier switchover debe ser una transición explícita de source authority.
4. Health separa al menos connection/session liveness, source continuity/gap evidence y market freshness.
5. Recovery es adapter-specific: replay, natural refresh o snapshot según source/schema.
6. Durante recovery el stream puede entrar en estado no confiable; D2 define la readiness barrier y política de nuevas decisiones.
7. Forming bars/indicators afectados por gap deben poder reconstruirse; la política exacta para closed bars/late corrections queda D2.
8. Provenance mínima de source/recovery epoch debe permitir diagnosticar qué autoridad produjo el estado sin contaminar cada dominio con vendor-specific details.

**Readiness final Front B:**
- Q4 Market hot state = `D1_INPUT_SUFFICIENT_FOR_D2`
- Q5 Bar semantics = `D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS`
- Q8 Feed authority/failover = `D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS`
- Q14 Backtest boundary = `D1_INPUT_SUFFICIENT_FOR_D2`
- **FRONT B = D1_MANAGER_REVIEW_CLOSED**

No se congela vendor, StateFun ownership, timeout, failover automation ni bar correction algorithm en D1.

## 📈 Market data — PREGUNTA ABIERTA PRIORITARIA

No se congela aún almacenamiento/cache de velas.

D1 debe investigar cómo engines cuantitativos/trading systems maduros resuelven:
- tick/event ingestion;
- bar aggregation;
- rolling history;
- indicators;
- warmup;
- persistence;
- recovery;
- replay/live equivalence;
- multi-timeframe;
- latency/concurrency.

Preguntas que el diseño debe responder:
- dónde viven las closed/forming bars;
- cómo acceden Strategy y MoneyManagement a ellas por tick/bar sin latencia de segundos;
- qué se mantiene en memoria;
- qué se persiste y cuándo;
- cómo se reconstruye estado después de restart;
- cómo funcionan feed primary + backups;
- cuál es la autoridad de vela;
- cómo se evita recalcular/consultar historia completa en cada tick.

El diseño final debe respetar un hot path sin I/O remoto cuando sea necesario para cumplir el presupuesto de latencia, pero la estructura exacta queda abierta hasta D2.

## 🏦 Futures Prop Universe — D1 Front C manager review — 2026-09-26

Research artifact: `main/30-resources/futures/FUTURES PROP UNIVERSE — FIRST-PARTY DOMAIN FORENSICS.md`.

**Manager verdict:** `C_PROP_UNIVERSE_RESEARCH = BLOCKED_EVIDENCE`.

El artefacto NO cumple todavía el mandato C ni el gate del track `FUTURES_PROP_UNIVERSE_PASS`. Se conserva como evidence draft parcial; no sustituye el corpus first-party requerido.

**Defectos materiales confirmados:**
- Omite proveedores requeridos y relevantes con evidencia first-party disponible: **TradeDay, Tradeify, Alpha Futures y TakeProfitTrader**.
- Afirma que no encontró providers que prohíban bots; es falso: **Alpha Futures** prohíbe AI/bots/full automation en todos los account types y **TakeProfitTrader** prohíbe bots/algo en Test/PRO/PRO+.
- Clasifica **Lucid Trading** como automation UNKNOWN/plausible, pero su Help Center oficial dice que automated trading systems y trade copiers están permitted.
- Clasifica **MyFundedFutures** como automation UNKNOWN, pero su first-party Fair Play policy permite automated trading strategies propias, prohibiendo HFT/exploitation.
- Afirma que **Topstep** no documenta API externa; el Help Center oficial documenta TopstepX/ProjectX API, automated strategies/bots, API keys y la restricción material de que ProjectX API no está disponible para Live Funded.
- La “cohorte de al menos 5” no se cumple: el documento entrega cuatro nombres parcialmente sustentados y un placeholder “otra firma / FX”, contrario al mandato.
- No entrega por material claim la fuente exacta + fecha prometida; no existe el evidence packet/anexo verificable al que alude.
- Usa inferencias explícitamente prohibidas por el mandato: API “implícita”, bots “plausibles”, tecnología “se sabe internamente”, etc.
- Mezcla platform support con API entitlement, justamente el error que el mandato exigía evitar.
- Algunas afirmaciones de producto/mercado son semánticamente defectuosas (por ejemplo referirse a futuros CME como “CFDs”).

**Evidence first-party revalidada por manager como mínimo de reparación:**
- Topstep API/bots: `https://help.topstep.com/en/articles/11187768-topstepx-api-access`
- Lucid automation: `https://support.lucidtrading.com/en/articles/11404728-other-trading-activities`
- MFFU automation: `https://help.myfundedfutures.com/en/articles/8444599-fair-play-and-prohibited-trading-practices`
- TradeDay automation/API: `https://tradeday.freshdesk.com/en/support/solutions/articles/103000085101-automated-algo-and-bot-trading`
- Tradeify automation: `https://help.tradeify.co/en/articles/10468318-guidelines-for-traders`
- Alpha automation prohibition: `https://help.alpha-futures.com/en/articles/9508585-prohibited-trading-practices`
- TakeProfitTrader no bots/algo: `https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/34431153546397-TakeProfitTrader-Universal-Trading-Policies-UTP`
- FundedNext automation: `https://helpfutures.fundednext.com/en/articles/14298560-is-the-usage-of-automated-trading-systems-eas-and-bots-allowed-in-fundednext-futures`

**Reusable del draft:**
- La conclusión `Provider` solo no alcanza; `ProviderProgram/Phase` es material.
- Las familias de rule-domain identificadas son un buen seed: drawdown/DLL, max contracts, consistency, sessions/forced flatten, automation, HFT/microscalping, copy/hedging, account limits, payout/elegibility.
- Los scopes ACCOUNT/TRADER/HOUSEHOLD/CROSS_ACCOUNT/CROSS_PROVIDER siguen siendo relevantes.

**No reusable como autoridad hasta reparación:**
- automation matrix;
- provider/platform/API matrix;
- cohort V1;
- blocked/excluded list;
- claims de API entitlement;
- rule values/phase details sin source exacta.

**Readiness:**
- Q10 Provider model = `D1_INPUT_SUFFICIENT_FOR_D2`: la necesidad de `Provider + Program/Phase + versioned RuleSet` está suficientemente demostrada.
- Front C operational corpus = `REPAIR_REQUIRED_BEFORE_D`.
- No ejecutar Front D transport research todavía: depende de una cohort/program/platform/API matrix corregida.

### Front C repair V2 manager review — 2026-09-26

Research artifact: `main/30-resources/futures/FUTURES PROP UNIVERSE — FIRST-PARTY DOMAIN FORENSICS V2.md`.

**Verdict:** `C_PROP_UNIVERSE_RESEARCH = BLOCKED_EVIDENCE` nuevamente.

La V2 no ejecutó el mandato C-R1 de reparación. Defectos materiales:

- **Topstep** queda casi omitido/UNKNOWN aunque la documentación oficial vigente expone TopstepX/ProjectX API, bots/custom automated strategies, API keys y la restricción de que Live Funded no puede operar vía ProjectX API.
- **MFFU** queda UNKNOWN aunque su Fair Play policy vigente permite automated trading strategies propias y prohíbe HFT/explotación de fills simulados.
- **FundedNext Futures** queda UNKNOWN aunque su Help Center vigente permite EAs/bots tanto en Challenge como FundedNext Account, prohibiendo latency abuse/order flooding.
- **Tradeify** queda UNKNOWN aunque su guideline vigente permite bots/algorithms bajo sole ownership, exclusive use dentro de Tradeify y no-HFT; además prohíbe uso cross-firm.
- **TakeProfitTrader** queda UNKNOWN aunque su UTP vigente aplica a Test/PRO/PRO+ y prohíbe automated trading systems/bots/algorithmic execution.
- **TradeDay** queda mal clasificado como “automation FORBIDDEN”: su first-party dice que para usar un ATS hay que hacerlo mediante plataformas soportadas; lo que prohíbe son third-party purchased bots y acceso API directo/Tradovate API.
- La V2 vuelve a incumplir el requisito de claim-level evidence: anuncia un “anexo” pero no entrega URLs/títulos/fechas por claim.
- Persiste lenguaje prohibido/inferencial: “probablemente”, “se presume”, “según cada plataforma”, “sin fuente”.
- La cohorte `>=5` vuelve a fallar por error de investigación, no por falta de mercado. La evidencia disponible ya muestra al menos Topstep (sim/Express), Lucid, MFFU, TradeDay, FundedNext y Tradeify como automation-compatible/conditional bajo scopes distintos.

**Separación manager:**
- El **modelo de dominio Q10** ya no necesita más discovery general.
- El **corpus operacional** sí necesita una reparación final estrictamente tabular antes de D, porque D depende de automation + platform + API entitlement por ProviderProgram.
- No volver a pedir un informe narrativo amplio. La siguiente reparación debe ser un evidence table cerrado sobre fuentes ya conocidas.

### Front C authoritative matrix manager review — 2026-09-26

Research artifact: `main/30-resources/futures/FUTURES PROP UNIVERSE — AUTHORITATIVE EVIDENCE MATRIX.md`.

**Manager verdict:** `C_PROP_UNIVERSE_RESEARCH = ACCEPTED_WITH_MANAGER_CORRECTIONS`.

El artefacto todavía incumple formalmente parte del mandato C-R2 —declara no tener acceso a V1/V2 aunque existen en la misma carpeta, su evidence appendix no contiene URLs literales por claim y deja Lucid/Tradeify como UNKNOWN pese a fuentes first-party vigentes—, pero esos defectos ya no justifican otro worker: el manager revalidó directamente las fuentes oficiales y la matriz es suficiente para habilitar Front D con UNKNOWNs honestos donde corresponde.

**Correcciones manager autoritativas:**
- **Lucid Trading automation = ALLOWED.** First-party: `https://support.lucidtrading.com/en/articles/11404728-other-trading-activities` — “Automated trading systems and trade copiers are permitted”.
- **Lucid platforms/connectivity:** CQG: NinjaTrader, Tradovate, TradingView; Rithmic: MotiveWave, Quantower, Tradesea, Sierra Chart, Jigsaw, Bookmap, ATAS, R|Trader Pro, MultiCharts. First-party: `https://support.lucidtrading.com/en/articles/11404614-lucid-trading-supported-platforms`. Direct developer API entitlement permanece `UNKNOWN`.
- **Tradeify automation = CONDITIONAL.** Bots/algorithms permitidos sólo con sole ownership demostrable, exclusive use dentro de Tradeify y no-HFT; uso cross-firm prohibido. First-party: `https://help.tradeify.co/en/articles/10468318-guidelines-for-traders`.
- **Tradeify platforms/connectivity:** broker choice Tradovate, Rithmic o WealthCharts; Tradovate da Tradovate/NinjaTrader/TradingView; Rithmic da Tradesea/Quantower/Sierra Chart/R|Trader. First-party: `https://help.tradeify.co/en/articles/10468221-supported-platforms`. Direct developer API entitlement permanece `UNKNOWN`.
- **Topstep:** Trading Combine/Express simulated = automation/API `ALLOWED_CONDITIONAL`; Live Funded ProjectX API = `FORBIDDEN`; personal-device/no-VPS order-flow constraint. First-party: `https://help.topstep.com/en/articles/11187768-topstepx-api-access`.
- **MFFU:** automated strategies propias = `ALLOWED_CONDITIONAL`; HFT y simulated-fill exploitation prohibidos. First-party: `https://help.myfundedfutures.com/en/articles/8444599-fair-play-and-prohibited-trading-practices`.
- **TradeDay:** automation/ATS = `ALLOWED_CONDITIONAL` mediante plataformas soportadas; direct platform/Tradovate API = `FORBIDDEN`; third-party purchased bots prohibidos. First-party: `https://tradeday.freshdesk.com/en/support/solutions/articles/103000085101-automated-algo-and-bot-trading`.
- **FundedNext Futures:** Challenge + FundedNext Account automation = `ALLOWED`; latency abuse/order flooding prohibidos. First-party: `https://helpfutures.fundednext.com/en/articles/14298560-is-the-usage-of-automated-trading-systems-eas-and-bots-allowed-in-fundednext-futures`.
- **Alpha Futures:** full automation/AI/bots = `FORBIDDEN`; semi-auto signals con ejecución/gestión manual permitidos. First-party: `https://help.alpha-futures.com/en/articles/9508585-prohibited-trading-practices`.
- **TakeProfitTrader:** Test/PRO/PRO+ bots/automated/algo execution = `FORBIDDEN`. First-party: `https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/34431153546397-TakeProfitTrader-Universal-Trading-Policies-UTP`.

**Operational cohort suficiente para Front D:**
- Topstep Trading Combine / Express Funded — ProjectX direct candidate.
- Lucid — CQG/Rithmic platform families; direct API entitlement UNKNOWN.
- MFFU — automation allowed; supported platforms proven; direct API entitlement UNKNOWN.
- TradeDay — automation through supported platforms; direct API forbidden.
- FundedNext — automation allowed; platform path includes Tradovate ecosystem; direct API entitlement UNKNOWN.
- Tradeify — automation conditional; Tradovate/Rithmic/WealthCharts; direct API entitlement UNKNOWN.
- Alpha/TPT quedan explícitamente fuera de la cohorte full-auto V1 por rule incompatibility.

**Final Front C readiness:**
- Q10 Provider model = `D1_INPUT_SUFFICIENT_FOR_D2`.
- Provider rule-family discovery = `D1_INPUT_SUFFICIENT_FOR_D2`.
- Operational automation/platform/connectivity corpus = `SUFFICIENT_FOR_FRONT_D`.
- Direct API entitlement conserva `UNKNOWN` donde no existe first-party; Front D debe resolver feasibility por transport sin promocionar platform access a API.
- **FRONT C = D1_MANAGER_REVIEW_CLOSED**.
- **FRONT D = READY_TO_EXECUTE**.

No se congela aquí selección de provider, transport ni cohort comercial.

## 🔌 Execution transport — D1 Front D manager review — 2026-09-26

Research artifact: `main/30-resources/futures/EXECUTION TRANSPORT FEASIBILITY — MULTI-PROP EVIDENCE.md`.

**Manager verdict:** `D_EXECUTION_TRANSPORT_RESEARCH = ACCEPTED_WITH_MANAGER_CORRECTIONS`.

El worker encontró las familias correctas, pero mezcló evidencia física con inferencias y contiene varios errores materiales. El manager revalidó documentación oficial y conserva sólo claims demostrables.

**ProjectX / TopstepX — PROVEN E2E FEASIBILITY**
- La documentación pública oficial SÍ existe.
- Auth = API key -> JWT/session token; no OAuth2.
- `Account/search` devuelve las cuentas activas asociadas al user.
- Orders oficiales: MARKET, LIMIT, STOP, además TrailingStop/JoinBid/JoinAsk; place/modify/cancel/search/searchOpen están documentados.
- Real-time oficial SignalR entrega account/order/position/**trade** updates; trade referencia `orderId`. Market hub entrega quote/trade/depth.
- `customTag` existe en Order y sirve como correlation primitive, aunque no se eleva todavía a garantía de idempotencia.
- Reconnect example oficial usa `onreconnected` + resubscribe.
- Rate limits oficiales: history 50/30s; resto 200/60s. Esto es input de capacity D2 y evita afirmar 100–200 accounts sin benchmark.
- Topstep policy restringe el order-flow automatizado a dispositivo personal y ProjectX API no está disponible en Live Funded. Por tanto capability cloud del protocolo NO implica deployment cloud autorizado para Topstep.
- Resultado D1: existe un transport real, documentado y autorizable en Trading Combine/Express simulated suficiente para demostrar Q9 feasibility.

**NinjaTrader Desktop bridge — CAPABILITY PROVEN / PROVIDER ENTITLEMENT VARIES**
- NinjaScript/AddOn `Account` expone `Account.All`, CreateOrder/Submit/Change/Cancel/Flatten, Orders/Executions/Positions y eventos AccountItem/Order/Execution/Position.
- `OnExecutionUpdate` documenta explícitamente que una Order puede producir múltiples executions/partial fills.
- Sim101 es un environment simulado oficial.
- No aceptar el claim “1 account por instance/connection”: el SDK expone múltiples Account objects; el límite práctico por connection/provider queda para D2/benchmark.
- El bridge debe basarse en NinjaTrader **Desktop/NinjaScript**. La existencia de NinjaTrader Web no prueba que Web/Mac sea una superficie equivalente para un bridge programable.
- Reutilizable como edge local potencial para ProviderPrograms que permiten ATS sobre NT; entitlement específico sigue siendo ProviderProgram data.

**Tradovate — CAPABILITY PROVEN / PROP ENTITLEMENT UNKNOWN**
- REST + WebSocket, demo/live separados, user sync realtime, MARKET/LIMIT/STOP y tipos avanzados, OCO/OSO/brackets.
- `clOrdId` y `customTag50` existen: correlation/idempotency primitives mejores de lo que afirmó el worker.
- Partner API oficial requiere Organization Admin credentials + API Key + CID; no confundir esto con tener login Tradovate de una prop.
- La API documenta conformance/WebSocket management para partner integration; direct entitlement por MFFU/FundedNext/Tradeify permanece UNKNOWN salvo first-party explícita.
- TradeDay direct Tradovate API continúa FORBIDDEN por su propia policy.

**Rithmic — CAPABILITY PROVEN / ENTITLEMENT + CONFORMANCE REQUIRED**
- R|API+ / R|Protocol son transports oficiales de data + order management.
- R|Protocol example oficial usa user/password; no hay evidencia para el claim OAuth2 del worker.
- Rithmic Test no requiere conformance; production/Rithmic 01/Paper/FCM IDs **sí requieren conformance**.
- Exchange Simulator oficial sirve a developers con live market data y market/limit/stop/brackets/OCO.
- No aceptar sin evidencia: exactly-once guarantees, throughput figures, multi-account socket capacity o automatic duplicate handling.
- Credentials de plataforma Rithmic no equivalen a developer API entitlement.

**CQG — CAPABILITY PROVEN / ENTITLEMENT + CONFORMANCE REQUIRED**
- CQG WebAPI es secure WebSocket + protobuf, language-agnostic y expone market data, order execution, account summary, order history y post-trade.
- Environment simulado oficial disponible.
- Production requiere formal conformance test.
- Por tanto el worker es incorrecto al caracterizar CQG API como esencialmente COM/.NET/Windows o “sin certificación”; WebAPI es la surface relevante a evaluar.
- Lucid soportar CQG no demuestra entitlement a CQG WebAPI; permanece UNKNOWN.

**Claims rechazados del worker**
- ProjectX “sin docs públicas”, OAuth2 y capability inferida por analogía con Tradovate.
- ProjectX/Tradovate/Rithmic/CQG “cloud/server autorizado” por capability técnica sin considerar ProviderProgram policy.
- NinjaTrader “Mac bridge”, “1 account por instance” y multi-account scaling sin evidencia.
- Tradovate ~50 req/s, socket para 200 accounts y generic prop API access sin source.
- Rithmic exactly-once, no-conformance production y cifras de throughput sin source.
- CQG COM/Windows-only, no-conformance y otras features no respaldadas.
- WealthCharts = TradeStation.
- cualquier afirmación de que 100–200 accounts “ya escala” sin capacity test.

**Q3 Order lifecycle inputs ya suficientes para D2**
- transport Order ID + optional client/correlation tag;
- asynchronous order status transitions;
- submit/modify/cancel;
- Order 1 -> 0..N immutable execution/fill events;
- Position/account state separado;
- reconnect requiere resubscribe + authoritative state refresh/reconciliation;
- exact normalized OrderStatus enum y idempotency policy pertenecen a D2.

**Front D final readiness**
- Q9 Execution transport = `D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS`.
- Q3 Order lifecycle = `D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS`.
- At least one authorized non-real-money path = **PROVEN** via TopstepX/ProjectX Trading Combine/Express path; NinjaTrader Sim101 proves a second generic simulation surface but not provider entitlement.
- Direct Tradovate/Rithmic/CQG provider entitlement remains UNKNOWN where first-party does not grant it.
- 100–200 account capacity remains a D2/D6 capacity requirement, not a D1 proven fact.
- **FRONT D = D1_MANAGER_REVIEW_CLOSED**.

No transport winner is selected in D1.

## 🏦 Futures Prop Universe

El producto debe diseñarse con conocimiento de un universo amplio de futures prop firms, no sólo Topstep.

El proyecto [[Echo Futures — Futures Prop Universe]] se ejecutará durante análisis para capturar firmas:
- operables algorítmicamente;
- condicionales;
- incompatibles con automatización;
- bloqueadas por plataforma/regla;
- económicamente poco atractivas.

Se requieren fuentes first-party para reglas materiales.

El objetivo del census no es recomendar una firma, sino:
- descubrir la taxonomía real de reglas;
- modelar Provider/Program/RuleSet correctamente;
- conocer execution technologies/plataformas;
- evitar congelar un rules engine basado en una sola empresa;
- preparar una primera cohorte operativa de varias props.

V1 debe poder configurar varias prop firms sin acoplar Strategy a Provider.

## 🔄 Relación con Echo actual

D1/D2 deben auditar source real de:
- Echo Core;
- SDK/domain;
- Bridge;
- Gateway;
- storage/schema;
- ExecutionPlanner;
- MMEngine;
- ExecutionStore;
- PositionSync;
- TradeJournal;
- contratos Reference/Execution.

Para cada concepto propuesto se clasificará:
- REUSE;
- EXTEND;
- ADAPT;
- REPLACE;
- NEW;
- DEFERRED_DEBT.

La documentación actual de Echo no basta como autoridad; se contrastará con source y comportamiento.

### Refactor policy

Prioridad: **Echo Futures funcionando correctamente**, no “Core V3 perfecto”.

Si una limitación actual no bloquea Futures:
- documentar deuda técnica/target Core V3;
- diferirla;
- continuar.

Si bloquea:
1. estimar si puede resolverse con refactor/adaptación acotada <= 1 día;
2. si sí, ejecutarlo dentro del plan;
3. si no, evaluar impacto y alternativas explícitamente antes de extender scope.

Objetivo ideal: salir sin deuda técnica material, pero nunca convertir el proyecto en una reescritura general de Echo.

## 🏗️ Forma de ejecución del proyecto

Cada día/hito tiene **un Manager Agent** responsable.

Ese manager:
1. hace bootstrap de autoridades;
2. planifica el objetivo observable del día;
3. decide qué subagentes necesita;
4. coordina research/documentación/desarrollo/QA;
5. contrasta outputs con source/evidencia;
6. integra hallazgos;
7. actualiza el proyecto;
8. deja gate y continuidad exacta.

Los subagentes no deciden roadmap ni aceptan gates.

El owner/manager técnico conserva autoridad final.

No se optimiza por máximo paralelismo. Se paralelizan sólo tareas independientes cuyo resultado converja en un gate claro.

## 🗓️ Roadmap inicial — 8 días / 8 hitos

### D1 — ANALYSIS / Problem & Domain Discovery

**Manager goal:** terminar el día entendiendo exactamente qué estamos construyendo y qué ya existe.

Trabajo coordinado por el manager, recorrido **global → workstream → detalle** con el owner:
- revisar el source/domain audit preliminar de Echo actual y decidir si Q1 requiere auditoría adicional;
- contrastar Strategy/Signal/Operation/Order/Fill/Position/Trade con contratos físicos;
- recuperar S1/S2 y Gerard +/- desde evidencia previa sólo hasta el nivel necesario para arquitectura;
- ejecutar [[Echo Futures — Futures Prop Universe]] mediante **deep research dedicado first-party**; el sample preliminar del manager es sólo seed;
- preparar y ejecutar **deep research dedicado de market-data / quant-engine implementations** para extraer patrones implementables, trade-offs y failure modes; el scouting LEAN/Nautilus ya hecho es input, no conclusión;
- derivar del corpus real de props el inventario de plataformas/execution technologies y luego ejecutar research de transports;
- demostrar feasibility de al menos un execution transport real a nivel de evidencia D1, sin seleccionar arquitectura todavía;
- contract identity/mapping hot y semántica manual de rollover, considerando la futura reutilización en el Echo Forex actual;
- trading sessions/timezone/DST/calendar;
- blocker discovery explícito para Position attribution, Order lifecycle y backtest reuse boundary;
- registrar gaps, deuda y contradicciones; no diseñar aún alrededor de supuestos.

Cada frente sustancial termina con un **prompt maestro exacto** para el deep researcher/auditor/documentador que corresponda. Los outputs vuelven al manager, quien los revisa con el owner antes de integrarlos.

Deliverable:
`D1 Analysis Pack`.

Gate objetivo:
`EF_D1_ANALYSIS_PASS = REVIEW`.

**Estado final 2026-09-26:** `EF_D1_ANALYSIS_PASS = PASS`. Owner aceptó el checklist completo D1. [[Echo Futures — D1 Analysis Pack]] queda como evidence authority de D1. No reabrir discovery general en D2 salvo contradicción material nueva.

No código productivo.

### D2 — DESIGN / Domain + Technical Architecture

**Estado:** ACTIVE / NEXT MILESTONE desde 2026-09-26. D1 baseline aceptado: `EF_D1_ANALYSIS_PASS = PASS`.

**Manager goal:** convertir D1 en una arquitectura candidata completa y simple.

Debe producir primero un **Domain & Data Model Candidate** (identities, cardinalities, lifecycle, authority, persistence/hot/derived) y luego congelar como candidato:
- domain model;
- entity lifecycles/cardinalities;
- Strategy/Signal contract;
- AccountStrategy;
- MoneyManagement contract;
- Operation/Order/Fill/Position/Trade semantics;
- market-data runtime;
- bar semantics/storage/warmup/recovery;
- canonical Instrument/Contract mapping + hot-update semantics;
- named TradingSession/calendar/timezone/DST semantics;
- provider/program/rules model;
- feed authority/failover;
- execution adapter/bridge boundaries;
- persistence/journal/Lab continuity;
- concurrency/state ownership;
- scale model 200 accounts;
- replay/backtest path y explicit reusable-domain boundary para el futuro módulo independiente;
- migration/reuse map sobre Echo;
- capacity model que haga explícito qué trabajo escala por instrument, strategy, operation y account.

Deliverable:
`Echo Futures Architecture Candidate V1`.

Gate:
`EF_D2_DESIGN_PASS = REVIEW`.

No implementación productiva.

### D3 — VALIDATION / ASTRA

**Manager goal:** someter D2 a una única revisión GOD/Astra adversarial y útil.

Astra recibe:
- D1 evidence;
- D2 architecture;
- Echo source/reuse map;
- prop rule corpus;
- market-data research;
- explicit owner requirements.

Astra debe buscar:
- responsabilidades mal ubicadas;
- conceptos duplicados/confusos;
- incompatibilidades con Echo;
- fallos de Operation/Order/Fill/Position/Trade;
- riesgo de latencia/concurrencia;
- scalability 200+ accounts;
- acoplamiento futures-only accidental;
- overengineering/YAGNI violations;
- provider-rule gaps;
- replay/live divergence;
- imposibilidad de reutilizar Strategy/MoneyManagement en un backtester independiente;
- contract mapping/session/roll semantics;
- 200-account capacity assumptions.

Deliverable:
`Astra Architecture Review`.

Gate:
`EF_D3_ASTRA_PASS = REVIEW`.

No arreglar durante la auditoría.

### D4 — CORRECTION / Architecture Freeze

**Manager goal:** resolver findings aceptados y convertir propuesta en SPEC implementable.

Trabajo:
- clasificar cada finding ACCEPT/REJECT/DEFER con evidencia;
- corregir modelo;
- resolver refactors bloqueantes;
- registrar DT diferida explícita;
- congelar Functional SPEC + Technical SPEC;
- dividir implementación en shots independientes;
- establecer acceptance tests y performance/resource budgets antes de codear.

Deliverable:
`Echo Futures V1 Architecture Freeze`.

Gate:
`EF_D4_ARCH_FREEZE = REVIEW`.

**Ningún desarrollo V1 comienza sin este gate aceptado.**

### D5 — DEVELOPMENT I / Foundations

**Manager goal:** construir el vertical foundation sin abrir todos los providers a la vez.

Carriles paralelos permitidos después del freeze, según SPEC:
- market-data ingestion/state/bars;
- Strategy runtime + S1/S2;
- domain/lifecycles;
- MoneyManagement Gerard +/-;
- provider rule runtime;
- execution contracts/adapters;
- journal/replay foundations.

El manager integra continuamente y evita branches que diverjan del freeze.

Deliverable:
vertical E2E sobre simulated/replay execution.

Gate:
`EF_D5_FOUNDATION_PASS = REVIEW`.

### D6 — DEVELOPMENT II / Multi-Prop E2E + Scale

**Manager goal:** convertir foundations en un runtime integrado operativo.

Trabajo:
- al menos un execution transport real funcional en shadow/demo/sim autorizado;
- execution adapters/bridges adicionales necesarios para primera cohorte;
- provider/program configs;
- account fan-out;
- reconciliation;
- fail-closed safety;
- feed failover;
- restart/recovery;
- trade_journal/Lab contract;
- replay/live same-path;
- carga progresiva hasta target de arquitectura.

Deliverable:
demo/shadow multi-account/multi-prop E2E.

Gate:
`EF_D6_E2E_PASS = REVIEW`.

### D7 — QA / Certification

**Manager goal:** intentar romper el sistema antes de RO.

QA independiente/adversarial:
- domain invariants;
- deterministic replay;
- partial/multi-fill;
- pending LIMIT/STOP;
- Gerard add/reduce lifecycle;
- duplicate/conflicting strategy configuration behaves literally;
- provider rule denial/UNKNOWN fail-closed;
- disconnect/reconnect;
- feed gaps/failover;
- restart/recovery;
- idempotency;
- reconciliation;
- 200-account target load;
- higher headroom probe where safe;
- memory/CPU/latency/resource budgets;
- race/concurrency;
- journal/Lab integrity.

Deliverable:
`Echo Futures V1 Certification Report`.

Gate:
`EF_D7_QA_PASS = REVIEW`.

### D8 — RO / Release & Operability

**Manager goal:** dejar Echo Futures instalable, operable y recuperable.

RO includes:
- runbooks;
- environment/config contract;
- secrets/credentials boundaries;
- deploy/start/stop;
- kill switch;
- observability;
- backup/recovery implications;
- provider onboarding procedure;
- strategy onboarding procedure;
- account onboarding procedure;
- incident procedures;
- rollback;
- known limitations/DT;
- release manifest + exact SHAs.

No real-money enablement implícito: el release debe declarar explícitamente qué modes/providers/accounts están autorizados.

Deliverable:
`Echo Futures V1 RO`.

Gate:
`EF_V1_RO_PASS = REVIEW`.

## ⏱️ ETA y control de scope

Planning target inicial: **8 días de trabajo / 8 hitos**, sujeto a D1 source audit.

No se agrega tiempo por “hacer arquitectura más bonita”.

Un día puede usar múltiples subagentes, pero sólo existe un manager/gate por hito.

Si D1 demuestra que un refactor bloqueante rompe el ETA:
- no esconderlo;
- cuantificar;
- elegir adaptación, refactor acotado o cambio explícito de ETA.


## 🔜 Fase inmediata post-V1 — Backtesting Module

No forma parte del gate de implementación V1, pero es el siguiente proyecto previsto una vez exista una primera cohorte multi-prop operando establemente en shadow/demo.

Objetivo:
- runner independiente;
- ingestión de histórico/recorded market data;
- mismas Strategy;
- mismo MoneyManagement;
- mismas Signal/Operation/Order/Fill/Trade semantics;
- SimExecution determinista;
- outputs utilizables por The Lab;
- base futura para research y construcción de portfolios.

El coste esperado debe ser bajo precisamente porque V1 habrá preservado estas abstracciones. Si después de V1 el backtester exige reescribir Strategy o MoneyManagement, se considera un defecto de arquitectura de V1.

## ✅ Definition of Done V1

V1 no termina porque compile.

Debe demostrar, según SPEC congelada:
- dos estrategias V1 ejecutables;
- Signal sin sizing/provider;
- Strategy→Signal→todas las AccountStrategy asociadas;
- MoneyManagement stateful incluyendo Gerard +/- congelado;
- MARKET/LIMIT/STOP;
- Operation→N Orders;
- Order→N Fills;
- Position reconciliada;
- Operation cerrada→Trade→trade_journal→Lab;
- multi-prop rule/config model;
- varios execution adapters/bridges según cohorte;
- contracts/domain reutilizables por futuro backtester independiente, demostrado mediante SimExecution/replay;
- live/shadow/demo path según autorización;
- al menos un execution transport real certificado en ambiente no-real-money autorizado;
- fail-closed safety;
- restart/recovery;
- feed handling definido/certificado;
- capacidad de arquitectura de 200 accounts demostrada;
- documentación + RO.

## 🚫 Non-goals V1

- smallcaps/equities implementation;
- dynamic portfolios;
- resolver automáticamente señales duplicadas/conflictivas;
- múltiples MoneyManagement simultáneos por AccountStrategy;
- HFT;
- optimizador masivo de estrategias;
- soportar todas las props del mercado antes del primer release;
- reescritura general de Echo/Core V3;
- UI nueva salvo cambio mínimo estrictamente requerido para operar.

## ⚠️ Preguntas que deben sobrevivir hasta D1/D2

- semántica definitiva Position vs Operation bajo netting/hedging y múltiples strategies;
- exact mapping entre entidades nuevas y Echo actual;
- physical storage/hot-cache model de bars;
- feed primario/backups y criterios de authority/failover;
- S2 definitiva;
- hardscalping Gerard +/- exacto;
- taxonomía ProviderRuleSet después de observar universo real;
- bridges/adapters exactos de la primera cohorte;
- qué refactors son blocking vs DT Core V3.

## 🔗 Proyectos y evidencia relacionados

- [[Echo Futures — Prop Economics Experiment]] — experimento cerrado que justificó avanzar.
- [[Echo Futures — Futures Prop Universe]] — census de providers/reglas para D1.
- [[Echo Futures — M0 Algo Execution MVP]] — exploración arquitectónica previa; **no authority**, superseded por este proyecto.
- [[Echo]] — plataforma base.


## Session close — 2026-09-25

Estado corregido al cierre:
- proyecto canónico [[Echo Futures]] activo;
- D1 permanece **IN_PROGRESS** y `EF_D1_ANALYSIS_PASS = NOT_EVALUATED`;
- [[Echo Futures — D1 Analysis Pack]] se conserva como **PRELIMINARY MANAGER ADVANCE**, no como cierre;
- Q1 tiene source audit/matriz candidata pendiente de review con el owner;
- market-data LEAN/Nautilus fue scouting para sacar ideas/patrones, no selección ni research suficiente; queda deep research dedicado;
- futures-prop sample fue scouting prematuro y NO reemplaza [[Echo Futures — Futures Prop Universe]];
- execution transports preliminares son seeds; el research formal debe derivarse del corpus real de props;
- `DT-EF-FX-PROP-01` registra deuda obligatoria de aplicar provider rules al Echo Forex actual y evitar lock-in futures-only;
- la skill [[technical-project-manager]] fue corregida para manager-mode: owner authority, global→detalle, delegación por prompts maestros y no self-accept de gates;
- no se modificó código productivo y D2 NO comenzó.

**Next exact milestone:** continuar D1/A2 con owner+manager sobre `Operation / Order / Fill / Position`: completar lifecycle de Operation y luego Order/Fill semantics. Trade/The Lab queda fuera del camino crítico hasta reabrirse en el proyecto The Lab.

D2 sólo se habilita después de que el manager recorra el checklist D1 completo con el owner y éste acepte el gate.

## 🧱 D2 — Architecture Candidate decisions

### D2-01 — Operation snapshot + Contract pinning — OWNER CLOSED — 2026-09-26

**Status:** `OWNER_CLOSED`

V1 mantiene el modelo KISS y **no introduce entidades genéricas `Version`/`Revision`** para `Strategy`, `MoneyManagement` ni `AccountStrategy`.

Decisión congelada:

- `Strategy` y `AccountStrategy` mantienen identidades/configuración actuales simples en V1.
- Al materializar una `Operation`, ésta conserva sólo el estado/configuración efectiva que realmente necesita para que su comportamiento no cambie accidentalmente por un hot update posterior. No se copia configuración irrelevante ni se construye un framework histórico genérico.
- `Operation.contract_id` queda pinneado explícitamente al `Contract` físico resuelto al crear la Operation.
- Un hot update del mapping `Instrument -> Contract` afecta a nuevas Operations; **no retargetea silenciosamente** una Operation ya viva.
- Por defecto, cambios posteriores de configuración de Strategy/MM/AccountStrategy aplican a nuevas Operations. Cualquier autoridad global de seguridad/enforcement que deba actuar sobre Operations vivas se diseña explícitamente en su boundary correspondiente, no mediante mutation implícita del snapshot.
- Si más adelante aparece una necesidad real de auditoría histórica/promoción/reproducibilidad completa, se podrá agregar revisionado detrás de las identidades estables existentes sin cambiar los boundaries principales del dominio.
- `ProviderRuleSet` puede conservar versión/provenance cuando la regla vigente de la prop sea material para decisiones/auditoría; esto **no crea un framework de versionado universal**.

Rationale owner: extensible sin construir hoy extensiones no requeridas; KISS/YAGNI sin hipotecar el modelo ni acoplar rollover de contratos al sistema completo.

### D2-02 — Signal fan-out + single Operation semantics — OWNER CLOSED — 2026-09-26

**Status:** `OWNER_CLOSED`

V1 mantiene una semántica deliberadamente simple: **una Strategy puede tener como máximo una operación lógica activa a la vez**. No se introducen `operation_key`, `StrategyTrade`, `StrategyAction` como entidad ni otra capa intermedia para correlacionar múltiples operaciones concurrentes.

Decisión congelada:

- `Strategy` permanece account-agnostic y mantiene en su propio estado sólo lo necesario para saber si su operación lógica está abierta/cerrada y el contexto técnico requerido por su lógica.
- `Signal` es el evento canónico emitido por Strategy. Puede llevar un `action`/detail técnico embebido si la estrategia concreta lo necesita; esto es parte del contrato de Signal, **no una nueva entidad de dominio obligatoria**.
- Mientras la Strategy tiene una operación lógica activa, nuevas Signals de esa misma Strategy **no crean una nueva Operation**. Representan nuevas decisiones/acciones técnicas sobre la operación existente.
- El fan-out/coordinator toma cada Signal y la entrega de forma aislada por `AccountStrategy`; no entrega al MoneyManagement acceso global a todas las cuentas.
- Para cada `AccountStrategy` existe como máximo **una `Operation` no terminal por Strategy**. Esa Operation agrupa todo el movimiento económico desde la primera apertura hasta que se cierra la última exposición asociada.
- Múltiples entradas, adds, parciales, reducciones o salidas son múltiples `Order`/`Fill` dentro de **la misma Operation**, no nuevas Operations.
- `MoneyManagement` procesa una Signal en el contexto de una única `AccountStrategy` y su única Operation activa (si existe). Puede decidir emitir 0..N Orders para abrir, aumentar, reducir o cerrar exposición según su política, sin administrar cuentas ajenas.
- El runtime debe asegurar aislamiento/serialización por `AccountStrategy`/Operation para impedir contaminación cross-account. La topología física exacta (StateFun/Kafka/workers/etc.) se resuelve en el diseño técnico, no como responsabilidad del dominio.
- La Strategy es consciente de su **estado lógico canónico** abierto/cerrado; no conoce la materialización física de cada cuenta. Divergencias por reject, provider rules o execution failures permanecen responsabilidad del camino account-specific/MM/execution.
- Casos borde que requieran coupling específico entre una Strategy y un MoneyManagement concreto se permiten de forma explícita antes que contaminar las abstracciones generales de V1. La compatibilidad Strategy↔MoneyManagement debe validarse/configurarse, no asumirse universal.

Rationale owner: una operación representa el ciclo completo desde la primera apertura hasta el cierre de la última exposición; nuevas oportunidades dentro del mismo ciclo son Signals/Orders adicionales de la misma Operation. Si una oportunidad requiere comportamiento independiente, se modela como otra Strategy, no como múltiples Operations simultáneas de la misma Strategy.

### D2-03 — Signal contract + Strategy/MM responsibility boundary — OWNER CLOSED — 2026-09-26

**Status:** `OWNER_CLOSED`

D2 congela un único contrato canónico de salida por evaluación de Strategy: `Signal`. No se crea `StrategyAction`, `SignalAction` ni otra entidad separada. La Signal contiene un único campo `details` que agrupa el contexto técnico específico de la Strategy para mantener toda la decisión relacionada en una sola respuesta.

### Signal V1

Intents congelados:

- `OPEN`
- `REDUCE`
- `CLOSE`
- `CLOSE_ALL`

Semántica:

- `OPEN`: inicia/materializa el ciclo lógico de la Strategy cuando no existe Operation activa para esa AccountStrategy.
- `REDUCE`: expresa intención técnica de reducción sobre la Operation activa; MoneyManagement decide la materialización económica concreta para esa cuenta mediante 0..N Orders.
- `CLOSE`: expresa cierre de la Operation lógica activa de esa Strategy.
- `CLOSE_ALL`: panic/flatten de toda exposición/Orders/Operations pertenecientes a **esa Strategy dentro de esa AccountStrategy**. No autoriza cerrar Operations de otras Strategies ni se convierte en un comando global de cuenta. Un account-wide/provider-wide emergency flatten pertenece al plano de safety/provider enforcement.

### Signal.details

- `details` es parte de la Signal y no una nueva entidad de dominio.
- Contiene el payload técnico específico de la Strategy: triggers, niveles, contexto técnico, indicadores u otros datos necesarios para que un MoneyManagement compatible interprete la intención.
- El Core/domain trata `details` como un payload acotado de Strategy; no se diseña un mega-schema universal con campos opcionales para todas las estrategias.
- La representación física exacta puede ser un objeto/struct/map serializable según el contrato de implementación, pero debe conservar un único payload relacionado con la Signal y validación explícita de compatibilidad Strategy↔MoneyManagement.

### Boundary Strategy vs MoneyManagement

- Strategy es autoridad de **lógica técnica de mercado**: cuándo abrir/reducir/cerrar, dirección, condiciones y niveles técnicos de precio.
- MoneyManagement es autoridad de **riesgo y materialización monetaria/account-specific**: riesgo monetario, sizing, quantity, exposición, distribución de Orders, adds/reductions y gestión económica de la Operation.
- SL/TP de Strategy y SL/TP de MoneyManagement **no son reglas competidoras ni existe precedencia winner/loser**.
- Strategy expresa SL/TP técnicos como niveles/distancias del activo en unidades propias del instrumento (precio/ticks/puntos o equivalente; no `pips` universales).
- MoneyManagement toma esos niveles técnicos junto con Account/Provider/Instrument state y resuelve su consecuencia monetaria: riesgo, quantity y Orders ejecutables.
- Ambos representan el mismo concepto desde contextos distintos —técnico y monetario— y deben permanecer separados por responsabilidad.

### Compatibility

- No se exige compatibilidad universal entre cualquier Strategy y cualquier MoneyManagement.
- `AccountStrategy` sólo puede configurarse con combinaciones Strategy↔MoneyManagement declaradas/validadas como compatibles.
- Casos especiales se resuelven mediante coupling local y explícito entre esa Strategy y ese MoneyManagement antes que contaminar los contratos genéricos del runtime.

### Contract placement

- Strategy y Signal permanecen agnósticas del `execution contract_id` físico.
- La resolución `Instrument -> Contract` y el pinning de `contract_id` permanecen en la materialización account-specific de `Operation`, según D2-01.
- No se agrega complejidad adicional de contrato a Strategy/Signal en V1 salvo provenance mínima si una necesidad real de replay/auditoría lo exige posteriormente.

Rationale owner: mantener una única respuesta de Strategy, separar claramente técnica vs dinero, permitir compatibilidad explícita Strategy/MM y evitar que edge cases o ejecución física deformen las abstracciones generales de V1.

### D2-04 — Manager review — CORRECTION REQUIRED — 2026-09-26

**Status:** `D2_04_MANAGER_REVIEW = CORRECTION_REQUIRED`

Primary Manager reviewed the durable artifact `[[Echo Futures — D2-04 Operation Order Fill Position]]` against D2-01/02/03 and `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`.

Accepted direction, pending repair: Operation as account-specific aggregate; isolated keyed ownership per AccountStrategy; Order 1→0..N Fill; Position as physical Account+Contract observation distinct from Operation; no global mutable MM store; reuse/adapt of Echo V3 StateFun/Kafka patterns.

Required corrections before D2-04 can be frozen:

1. Remove hidden AccountStrategy revision/version coupling from Operation snapshot. D2-01 permits only the effective configuration/state actually required by a live Operation; no implicit revision entity/framework.
2. Operation `direction` must be fixed from the accepted OPEN Signal/Strategy technical intent when Operation is materialized, not inferred later from the first execution Order.
3. `ForceClose`/safety flatten is a close intent/process, not an immediate transition to TERMINAL. TERMINAL still requires zero logical exposure + zero live Orders + explicit decision not to continue.
4. Fill truth cannot be clamped. If a venue over-reduces and signed Fill exposure crosses zero, preserve the immutable Fill-derived truth and surface an execution/invariant breach; do not silently normalize it back to zero.
5. The claim that final runtime/MM state is independent of event arrival order is too strong. Fill arithmetic is commutative; stateful MM decisions are not necessarily. The design must specify deterministic serialization/recorded processing order and replay semantics rather than claiming order-independence globally.
6. Prove or repair crash/idempotency semantics around side effects. UUIDv7 generated Orders + async PG/checkpointing do not by themselves prove that a crash after emitting a venue command but before durable state cannot create a second physical Order on replay. The design needs a concrete durable/deterministic command identity / StateFun-Kafka guarantee / adapter idempotency contract, with evidence for whichever mechanism is relied upon.
7. TTL-only in-memory Fill dedup plus async PG is insufficient if a duplicate execution can reappear after TTL and mutate hot exposure before the DB PK rejects persistence. Fill identity must remain idempotent for the relevant Operation/recovery horizon without synchronous DB dependency in the hot path.
8. Reclassify current MT-oriented `PositionSnapshot` domain shape carefully. Source is ticket/trade-level (`account_id,ticket,TradeID,StrategyID`), while Futures Position is net `Account+Contract`; reuse the synchronization pattern where useful, but do not claim a simple field extension if it would preserve wrong semantics.
9. Reassess optional `order_events`/`operation_events` audit tables and extra function/topic surface under KISS/YAGNI. Keep only pieces required for correctness/recovery; OTel/current-state persistence + immutable Fills may be enough for some audit concerns.

No owner decision is requested by this review. Return the same workstream to TOP for a targeted repair; do not advance to D2-05 until re-review.

#### D2-04 — Manager second review — CORRECTION REQUIRED — 2026-09-26

**Status:** `D2_04_MANAGER_REVIEW_2 = CORRECTION_REQUIRED`

The R1–R9 repair materially improved D2-04 and the StateFun 3.2 Kafka egress EXACTLY_ONCE premise is supported by official Apache documentation when explicitly configured. The workstream is still not frozen because four correctness/recovery boundaries remain unresolved:

1. **Adapter external-side-effect idempotency is incomplete.** An in-memory submission registry rebuilt only from open venue orders cannot suppress a redelivered command if the first physical order already became terminal (especially a fast MARKET fill) before an adapter crash/offset commit. D2-04 must require a restart-safe idempotency contract: durable submission journal plus authoritative lookup/reconciliation by `client_order_id` across live/history, or native venue idempotency. A transport unable to prove this cannot claim exactly-once physical submission.
2. **Async PostgreSQL projection cannot be an authoritative recovery source for StateFun state.** PG writes are not checkpoint-atomic. It can be ahead of a rolled-back checkpoint or behind a committed one. Normal recovery authority must remain Flink/StateFun checkpoint + Kafka replay; PG is an eventual/query projection. Cold recovery beyond checkpoint availability must fail closed or use an explicitly designed bootstrap/reconciliation path, not silently reconstruct authoritative MM state from async PG.
3. **`operation_event_seq` does not by itself create a replayable ordered event stream.** Persisting only the latest seq on Operation/Order/Fill cannot reconstruct Signals, order-status/ack events, termination intents or market inputs that produced MM state. Either scope the sequence to runtime diagnostics and leave deterministic replay ordering to the later Replay/Market design, or persist the required event stream. Do not claim exact live-operation replay from records that do not contain the events.
4. **Post-terminal execution/duplicate routing needs an explicit boundary.** Evicting Fill dedup at TERMINAL is safe only if a later event for an old `operation_id` can never mutate the current new Operation on the same `account:strategy` key. A genuinely new late Fill after terminal must not be discarded as a duplicate nor silently revive/contaminate the next Operation; it must preserve the execution fact and surface a post-terminal execution breach/reconciliation path. Define the minimal operation-id guard/tombstone or equivalent adapter/state-owner contract.

These remain technical corrections; no owner decision is required. Return D2-04 to the same TOP for a narrow repair only. Do not advance to D2-05.

#### D2-04 — Manager third review — FINAL CORRECTION REQUIRED — 2026-09-26

**Status:** `D2_04_MANAGER_REVIEW_3 = FINAL_CORRECTION_REQUIRED`

The second repair R10–R13 is accepted in substance: restart-safe adapter idempotency, checkpoint/Kafka recovery authority, scoped replay claims and post-terminal operation identity guards are now coherent. One remaining durability contradiction blocks freeze:

- The artifact treats `echo.operations`, `echo.orders` and especially immutable `echo.fills` as durable facts/projections, while the proposed implementation writes them through an async best-effort PG writer embedded in `echo/operation`. Because PG is not checkpoint-atomic and the Kafka ingress offset may advance with the StateFun checkpoint before that writer flushes, a crash can permanently lose a terminal projection or Fill after the source event is considered processed. This does not corrupt live aggregate correctness, but it violates the claimed durable Fill/history contract.

Required final repair: explicitly provide a durable projection source/barrier decoupled from live correctness. Prefer the smallest KISS mechanism: transactionally emit the required Operation/Order/Fill projection records/facts to Kafka as part of the same StateFun checkpoint/egress boundary, then project asynchronously/idempotently into PG; or prove an equivalent mechanism with no loss window. PG remains query projection and never recovery authority. Do not reintroduce event sourcing or a full operation event log. Late/post-terminal fills must use the same durable fact path rather than a direct best-effort PG-only insert.

No owner decision required. After this narrow repair, D2-04 should be eligible to freeze.

### D2-04 — Operation / Order / Fill / Position — MANAGER CLOSED — 2026-09-26

**Status:** `D2_04_MANAGER_REVIEW = CLOSED`

Primary Manager final review accepts `[[Echo Futures — D2-04 Operation Order Fill Position]]` after repairs R1–R14.

Frozen D2-04 conclusions:

- `Operation` is the account-specific aggregate and V1 allows at most one non-terminal Operation per AccountStrategy.
- State ownership is isolated/keyed by execution account + AccountStrategy; MM executes only inside that account-specific context and never receives a global mutable account/operation store.
- `Operation 1 -> 0..N Order`; `Order 1 -> 0..N Fill`; multiple simultaneous live Orders and partial fills are first-class.
- Operation direction is sealed from the accepted OPEN Signal before MM/Orders; Contract is pinned at Operation creation.
- `Fill` is immutable execution truth; logical exposure is derived from signed fills and is never silently clamped. Physical anomalies are fail-visible breaches, not synthetic repair.
- TERMINAL requires zero real logical exposure + zero live Orders + an explicit termination intent. ForceClose is an intent/process, not an immediate terminal transition.
- `Position` is a separate physical net observation by Account+Contract. Futures replaces the MT ticket-level domain shape while reusing the useful sync/projection pattern. Position never owns Operation lifecycle; DT-EF-POSITION-RECONCILIATION-05 remains deferred.
- Stateful decisions are deterministic for the same ordered input sequence; fact-derived quantities are commutative. D2-04 does not claim exact live-session replay from PG.
- Live recovery authority is Flink/StateFun checkpoint + Kafka ingress replay + transactional Kafka egress. PostgreSQL is query/eventual projection only and never recreates mm_state or decides physical Orders. Cold loss of checkpoint authority is fail-closed (`COLD_RECOVERY_REQUIRED`).
- Command submission has two explicit correctness boundaries: StateFun state↔Kafka egress must be EXACTLY_ONCE; the execution adapter must additionally provide restart-safe external-side-effect idempotency using durable submission intent + authoritative venue/history resolution or documented native idempotency. Unsupported transports/order classes are gated rather than approximated.
- Late execution events carry Operation/Order identity and can never mutate a successor Operation on the same keyed owner. Genuinely new post-terminal fills remain durable facts and raise a post-terminal execution breach without reviving the old aggregate.
- Durable Operation/Order latest-state projections and immutable Fill facts are emitted through a checkpoint-coordinated transactional Kafka projection/fact egress and materialized asynchronously/idempotently into PG by a small projector. No operation/order event store, saga or event-sourcing framework is introduced.
- Echo V3 disposition for this workstream: StateFun/Kafka/kache patterns REUSE; execution planner/MM engine ADAPT; CoreCommand/ExecutionResult remain legacy wire contracts; ExecutionStore is REPLACED as authority but retained for legacy compatibility; Position sync pattern REUSE with Futures domain-shape REPLACE.

Implementation/certification requirements carried forward:

- configure command and projection/fact Kafka egresses as `EXACTLY_ONCE` and consumers as committed-only where required;
- verify adapter history/tag/native-idempotency capabilities before a transport/order class is eligible for V1;
- size projection-topic retention and alert projector lag;
- certify 100–200 account capacity later; no architecture redesign is implied.

No owner decision remains open in D2-04. This closes Q2/Q3 at D2 design level. It does **not** close D2 globally.


### D2-05 — Instrument / Session / Provider — INTEGRATED CANDIDATE — 2026-09-26

**Status:**

`D2-05 = INTEGRATION_CANDIDATE_READY_FOR_SUBMANAGER_REVIEW`

Integrated candidate: [[Echo Futures — D2-05 Instrument Session Provider]].

Inputs frozen (blobs verificados == aprobados por el SUBMANAGER, sin drift):

- [[Echo Futures — D2-05A Instrument Contract]] — `READY_FOR_INTEGRATION`
- [[Echo Futures — D2-05B Session Calendar]] — `READY_FOR_INTEGRATION`
- [[Echo Futures — D2-05C Provider Program Rules]] — `READY_FOR_INTEGRATION`

Resumen de lo integrado (máximo 10 bullets):

- Instrument canónico (`instrument_id/quote_currency/exchange/product_group/calendar_ref`) separado de Contract expiry-specific; external identifiers por `(source, context)`; mapping hot por binding `(mapping_context, binding_id, instrument_id)` con feed/execution contexts independientes.
- Operation resuelve y pinnnea el Contract una sola vez en la materialización (D2-01/04); rollover owner-manual estrictamente prospectivo; cierre sobre contrato viejo nunca remapea (fail-visible).
- UN ExchangeCalendar = una semántica completa de producto/sesión; `session_id=(calendar_id, session_date)` unívoco por construcción; resolver puro sin product_group/exchange; session_date como dato (`trade_date_shift`), sin fórmula universal CME.
- IANA-only + tzdata embebida; ExchangeCalendar ≠ Provider overlay ≠ Account DayBoundary; el fallback UTC-23:00 legacy queda prohibido para cuentas Futures (fail-closed).
- Strategy referencia NamedTradingWindow por id (`EXCHANGE_SUBSET | CLOCK`); disponibilidad efectiva = ventana ∩ exchange; transiciones de sesión sólo vía `NextSessionTransition`.
- Provider → ProviderProgram → (fase opcional provider-local) → ProviderRuleSet versionado con provenance; UNKNOWN jamás es ALLOWED; transporte/entitlement separado en el binding de la Account; AccountStrategy sigue siendo Account + Strategy + MoneyManagement.
- Enforcement en dos gates: Stage-1 admisión pre-materialización (ALLOW|DENY_NEW_RISK, sin Operation si deniega) y Stage-2 post-MM/pre-egress (PER_ORDER local; caps compartidos por reserva serializada en `echo/provider_rules` con métrica tipada GROSS/NET_ABS/GROUP_WEIGHTED; guard de egress con revalidación de epoch del grant).
- Safety asíncrono sólo por intents (`ProviderForceClose` → ForceClose R3, jamás TERMINAL instantáneo); entitlement revocado ⇒ suspensión de emisión + operador, nunca flatten automático; `PENDING_FINALITY` = reservation state, no Order.status.
- Hot vs pinned congelado: reglas/mapping/calendario dinámicos prospectivos jamás mutan pin ni snapshot MM; anchor histórico = snapshot+hash en el manifiesto del run (calendario y RuleSet simulado) — LIVE consume hot config, REPLAY/BACKTEST inyecta snapshots explícitos.
- D2-04 permanece como autoridad del lifecycle: Operation antes de MM, TERMINAL sólo por guards, Position como trust guard físico.

**NOT CLOSED. NOT READY_FOR_PRIMARY_MANAGER UNTIL SUBMANAGER REVIEW. DO NOT ADVANCE D2-06.**

`OWNER_DECISIONS_REQUIRED = NONE`.

### D2-05 — Primary Manager review — CORRECTION REQUIRED — 2026-09-27

**Status:** `D2_05_MANAGER_REVIEW = CORRECTION_REQUIRED`

Primary Manager reviewed `[[Echo Futures — D2-05 Instrument Session Provider]]` (blob `bc37018364ff4f9a56d8e0b9c6a370d310db3c6a`) against D2-01..04 and focused Echo V3 source at `372af59a7b83604781346613da01e3d510ea1360`. Instrument/Contract mapping and ExchangeCalendar/Session direction are accepted. Four integration defects remain in the Provider/Account seam:

1. **Stage-1 admission is not actually linearized with the provider authority.** `echo/provider_rules` is declared the account-keyed authority, but `echo/operation` calls a kache-fed `admission snapshot` the "authoritative" guard. A newly processed RuleSet/binding/risk change can exist in `provider_rules` while a still-young old snapshot remains within its staleness threshold, allowing Operation materialization under an authority version that the owner has already superseded. Stage-2 epoch revalidation prevents physical new-risk escape later, but D2-05 promises provider-denied OPENs do not materialize an Operation. Repair by linearizing OPEN admission at the account-keyed authority (request/result or equivalent) while retaining kache only as prefilter/optimization; define the exact race semantics against hot updates.
2. **CapacityUpdate is insufficient to maintain shared exposure correctly.** Current protocol `CapacityUpdate{order_id,cumulative_filled_qty}` can convert a reserved risk-increasing Order, but REDUCE/EXIT bypass reservation and therefore may have no reservation metadata from which provider_rules can infer signed exposure change/scope. It also does not by itself preserve per-Operation contributions required for GROSS when two Strategies on the same Account+Contract hold opposite logical Operations. Repair the idempotent message/state shape so every Echo Fill, including exits, updates account capacity with enough identity/signed context; maintain the minimal per-Operation/per-scope state needed for GROSS/NET_ABS/GROUP_WEIGHTED without creating a portfolio aggregate.
3. **ProviderForceClose target discovery is unspecified.** The design says account-level `echo/provider_rules` sends ForceClose "to each live account:strategy key" but defines no authoritative mechanism to enumerate those keys. Safety cannot depend on an eventual PG projection. Define a KISS deterministic fan-out, preferably over the account's complete AccountStrategy binding set (including disabled bindings that may still own a live Operation) with no-op on empty aggregates, or an equivalently checkpointed active-key registry. Prove a live Operation cannot be omitted from forced-flat.
4. **Current DayBoundaryCache cannot satisfy the new hot binding semantics as classified.** Physical source `v3/core/internal/functions/account_sync.go@b0f8f1ce` caches DayBoundary per account forever and explicitly assumes phase/program changes create a new account_id. D2-05 instead freezes ProviderAccountBinding re-binding in-place on the same account and makes day_boundary a current authority. Reclassify/adapt the Futures path so DayBoundary is hot-updatable/invalidation-safe and fail-closed; do not claim the existing cache unchanged as authority. Legacy behavior may remain for legacy accounts.

These are technical integration repairs; no owner decision is required. Return the integrated artifact to the same SUBMANAGER for a targeted repair. Child A/B/C do not need to be reopened unless the SUBMANAGER discovers a contradiction; do not advance D2-06.

### D2-05 — Instrument / Session / Provider — MANAGER CLOSED — 2026-09-27

**Status:** `D2_05_MANAGER_REVIEW = CLOSED`

Primary Manager accepts `[[Echo Futures — D2-05 Instrument Session Provider]]` after integrated repairs R15–R18.

Frozen conclusions:

- Canonical `Instrument` is separate from expiry-specific `Contract`; external provider/feed identifiers are mappings, never global identity.
- Contract resolution is single-shot at Operation materialization. Operation pins `contract_id` + required economic specs; hot rollover is owner-manual, prospective only and never silently retargets a live Operation.
- Cross-market economic units use price/ticks/points/contracts/tick-size/point-value/currency; pips are legacy-only, not a universal unit.
- ExchangeCalendar/Session, Provider policy overlay and Account DayBoundary are three separate authorities. Calendar uses IANA timezone + dated overrides and produces session/trade date via a pure resolver shared by LIVE/REPLAY/BACKTEST.
- Strategy windows are named config over calendar/clock semantics, never fixed offsets. Exchange availability always bounds Strategy trading availability.
- Provider is business/policy owner and is separate from technological transport. Account binds to ProviderProgram + optional provider-local phase + current ProviderRuleSet authority + transport entitlement. AccountStrategy remains Account + Strategy + MoneyManagement.
- ProviderRuleSet is the deliberate exception where explicit version/provenance is required. Runtime rules are typed families + parameters/provider-specific typed exceptions; no DSL.
- Stage-1 OPEN admission is linearized through the account-keyed `echo/provider_rules` authority via AdmissionRequest/Result before Operation materialization. Admission kache is only prefilter/read model. Rule/binding/account/risk/DayBoundary updates share that account-keyed ordering point.
- Stage-2 runs after MM and before physical egress. Shared account/instrument/group caps use serialized reservations at the account owner; outstanding grants revalidate against current authority before egress.
- Account capacity keeps `firm_by_operation` plus live reservations. Every Echo Fill, including REDUCE/EXIT/safety/late fills, emits a cumulative signed Operation exposure update. This supports NET_ABS/GROSS/GROUP_WEIGHTED without a portfolio aggregate and without moving lifecycle ownership away from Operation.
- Provider safety acts via asynchronous termination intents. Account-wide ForceClose fans out deterministically over the retained AccountStrategy routing set, including disabled/close-only identities that can still own live Operations; empty keys no-op. PG is never used for safety discovery.
- Entitlement revocation does not invent an automated flatten: it denies new risk, suspends automated emission and requires operator handling unless an explicitly authorized close-only path exists.
- Futures DayBoundary is explicit, hot and account-keyed; missing/invalid authority is fail-closed. The current DayBoundaryCache is only a conceptual precursor and its cache-forever/UTC-fallback mechanism is ADAPT/REPLACE for Futures.
- LIVE consumes hot config; REPLAY/BACKTEST inject explicit Calendar/RuleSet/DayBoundary/Contract inputs and reuse the same pure domain semantics. D2-05 does not solve recorded market-stream ordering; that remains for later D2 work.
- Echo V3 disposition: hot config/kache, typed automation patterns, AccountState and safety patterns REUSE; MM/ExecutionPolicy/DayBoundary mechanisms ADAPT; Futures Provider domain, Calendar resolver, Contract/mapping catalogs, provider_rules, capacity projection and routing index are NEW; legacy prop_rulesets shape is REPLACED for the Futures path while legacy remains during migration.

This closes D2 design questions Q6, Q7 and Q10. No owner decision remains open in D2-05. D2 remains globally open.

### D2-06 — Market Runtime — READY FOR MANAGER REVIEW — 2026-09-27

**Status:** D2_06 = READY_FOR_MANAGER_REVIEW

[[Echo Futures — D2-06 Market Runtime]] integra los tres children ya aceptados [[Echo Futures — D2-06A Market Feed Authority]], [[Echo Futures — D2-06B Bars Hot State Warmup]] y [[Echo Futures — D2-06C Live Replay Market Boundary]] sobre baseline Echo 372af59a7b83604781346613da01e3d510ea1360 re-verificada sin delta. Es la autoridad única de lectura de D2-06 para Q4/Q5/Q8/Q14; los children quedan como evidence/design depth.

Modelo integrado vigente:

- **Logical market identity:** stream_id = (instrument_id, contract_id). binding/source vive en serving_authority {binding_id, members, authority_epoch, provenance}; no forma parte de stream identity.
- **Market demand:** Operation declara {operation_id, instrument_id, contract_id, ACQUIRE|RELEASE}; Market Runtime resuelve esa necesidad contra la MARKET_DATA authority activa. Operation pinnea Contract, nunca market source.
- **Source switch ≠ rollover:** switch preserva Contracts, incrementa epoch y ejecuta barrier/rebuild; rollover es acción owner explícita que cambia el Contract in-force prospectivo y crea/demanda otra logical stream. Nunca auto-roll ni silent blend.
- **Readiness layering:** feed/stream readiness = A; analytical/consumer readiness = B. EffectiveConsumerReadiness = StreamReadinessFor(required input class) AND AnalyticalRequirementsReady(consumer). WARMUP_INCOMPLETE queda exclusivamente como estado analítico downstream, nunca feed-global; una Strategy BBO-only puede quedar READY antes que otra en warm-up sin degradar la stream.
- **Current vs last-known:** current state es monotónico por (event_ts, stream_seq) sólo dentro del mismo authority_epoch. Epoch change demotea previous current a last-known stale/provenance y seed-ea current nuevo desde el primer dato válido; stream_seq cruza epochs. Availability != READY.
- **Bars/hot state:** echo/market_analytics key stream_id posee forming+bounded closed bars; BarId=(stream_id,timeframe,bucket_open_utc), TRADE bars V1, grid session_open, breaks no desplazan grid, timer/event boundary cierra, no synthetic empty bars. Projection puede corregir X→X' pero la decision observation X es inmutable: no reevaluation ni retrospective Signal.
- **MTF/indicators/scale:** cada timeframe agrega directamente desde canonical events; indicators strategy-side en echo/strategy_engine key strategy_id; una Strategy evaluation y fan-out posterior. 200 Accounts no crean 200 subscriptions/builders/indicator sets/evaluations.
- **Deterministic boundary:** event_ts, stream_seq, owner_input_seq y runtime_ts son identidades separadas. DomainClock.Now() usa runtime_ts monotónico; todo TimerFired admitido se journala con timer_id+generation; no total order global, sólo per-island ordering y Strategy merge journalado.
- **Recording/EXACT_REPLAY:** Initial RunManifest inmutable + ReplayAnchor inmutable + DeterministicInputLog + canonical content. El anchor conserva el corpus exacto de warm-up y se re-ejecuta antes de owner_input_seq=0; BAR_CLOSED no se graba como autoridad, se re-deriva. Hot config posterior vive como ConfigTransition ordenada; el manifest compactado puede acumular metadata operacional pero jamás reemplazar la sección initial por latest-effective-config.
- **EXACT_REPLAY vs BACKTEST:** exact replay reproduce un live real y su arrival/timer order; backtest crea un run histórico nuevo con canonical synthesis order y clock sintético. Execution event sourcing/recovery monetario permanece autoridad D2-04.

Parent Acceptance A–L: PASS en los 12 casos por mecanismo explícito. Child acceptance inherited: A-R1..R7; B-R1..R7 + O..U; C-R1..R3 + Q..T.

**OWNER_DECISIONS_REQUIRED:** OD-C1 solamente — recording de EXACT LIVE REPLAY ALWAYS-ON V1 versus OPT-IN por run. La arquitectura no cambia; un run sin ReplayAnchor capturado desde el inicio no es retroactivamente exact-replayable. Recomendación técnica heredada: ALWAYS-ON. OD-C1 no bloquea manager review.

Material risks/debts: benchmark StateFun/journal en D6; retention de canonical content+anchor+journal; class-C rebuild puede quedar fail-closed; golden replay debe certificar ReplayDriver; transactional journal config debe verificarse; heterogeneous backup puede bloquear switch si no sirve Contracts pinneados.

NO PASS/CLOSED global. NO D2-07. Siguiente gate: Primary Manager review de D2-06.

### D2-06 — Primary Manager review — APPROVED / PENDING OWNER OD-C1 — 2026-09-27

**Status:** `D2_06_MANAGER_REVIEW = APPROVED_PENDING_OWNER_DECISION`

Primary Manager reviewed `[[Echo Futures — D2-06 Market Runtime]]` against D2-04/D2-05 and the accepted D1 market-data evidence. No additional architectural defect remains open. Parent Acceptance A–L is accepted by mechanism; Q4/Q5/Q8/Q14 are technically ready to close.

Only owner decision remaining:

- `OD-C1 — EXACT LIVE REPLAY recording default`: `ALWAYS_ON_V1` vs `OPT_IN_PER_RUN`.

Manager recommendation: `ALWAYS_ON_V1`. Rationale: ReplayAnchor must exist from run start and cannot be reconstructed retroactively; DeterministicInputLog stores primarily ordering/runtime/control plus references to canonical market content rather than duplicating that content; the architecture is identical either way, so opt-in mainly creates a class of live runs that can never be exact-replayed later. Retention remains an operational policy and may expire recordings according to the declared recording horizon.

Do not open D2-07 until Owner ratifies OD-C1 and D2-06 is persisted CLOSED.

### D2-06 — Market Runtime — MANAGER CLOSED — 2026-09-27

**Status:** `D2_06_MANAGER_REVIEW = CLOSED`

Owner ratified OD-C1 as `ALWAYS_ON_V1_SELECTED_STREAMS`: exact-live-replay recording is always enabled from run start for the market streams/symbols actually selected or demanded by the run/Strategy/MM requirements, not for the provider's full symbol universe. ReplayAnchor + deterministic journal begin at t0 for those selected streams; retention remains a separate operational policy.

Primary Manager closes [[Echo Futures — D2-06 Market Runtime]]. This closes Q4 Market Hot State, Q5 Bar Semantics, Q8 Feed Authority and Q14 LIVE/REPLAY Market Boundary at D2 design level. D2 remains globally open.


### D2-07 — Execution Runtime / Initial V1 Transport — DISPATCHED — 2026-09-27

**Status:** `D2_07 = ACTIVE_SUBMANAGER_DISPATCH`

Scope: execution adapter boundary, command/result/order/fill integration, external idempotency/finality/reconciliation capabilities, transport eligibility matrix, and selection recommendation for the first non-real-money V1 execution path. Must consume D2-04 Operation/Order/Fill contracts, D2-05 Provider/Account binding and D2-06 market/session semantics. It must not reopen provider research broadly, must distinguish platform support from API entitlement, and must not advance D2-08. Selection of the initial V1 execution transport remains an owner/product decision after manager review of the integrated candidate.


### D2-07B — Transport Eligibility / Initial V1 Path — CORRECTED — 2026-09-27

**Status:** `D2-07B = READY_FOR_SUBMANAGER_REVIEW`

D2-07B scope repair completed in [[Echo Futures — D2-07B Transport Selection]]. The previous worker accidentally promoted transport-specific M2 certification from a D6 deployment gate to a D2 architecture blocker. D2-07A remains unchanged and strict: M1/M2 separation, durable intent, stable client identity, no blind retry, reconciliation, AMBIGUOUS fail-closed and exact Fill identity are still mandatory for exact physical submission.

`PROJECTX_DIRECT` is now the **recommended initial non-real-money implementation candidate** because the accepted evidence already demonstrates direct API capability, submit/modify/cancel, realtime execution observations, an accepted Topstep simulated ProviderProgram path and lower initial operational coupling than Desktop. This is recommendation only: `PROJECTX M2 VENDOR CERTIFICATION = DEFERRED_TO_D6`, `REAL_MONEY_CERTIFICATION = NOT_DONE`, and `OD-D2-07-1 = PROJECTX_DIRECT — CANDIDATE ONLY`.

ProjectX gaps are preserved as D6 certification gates: customTag retention, ambiguous-submit retry atomicity, authoritative negative/recovery semantics, Trade id scope/stability and history horizon. NinjaTrader Desktop is `NOT_RECOMMENDED_AS_FIRST_GENERIC_V1_PATH`; Tradovate, Rithmic and CQG remain future adapter candidates requiring transport-specific certification if selected.

`D2-07B does not block D2-07C`. D2-07C is **UNBLOCKED**, but must not be opened in this repair session. Transport selection stays behind the Bridge/Adapter boundary; physical implementation, authorized demo/shadow/sim validation and M2 evidence closure belong to D6. Next: SUBMANAGER review only; do not start D2-07C or D2-08.

### D2-07C — Execution Runtime Topology — READY FOR SUBMANAGER REVIEW — 2026-09-27

**Status:** `D2-07C = READY_FOR_SUBMANAGER_REVIEW`

[[Echo Futures — D2-07C Execution Runtime Topology]] resuelve la topología del execution runtime sobre baseline Echo `372af59a7b83604781346613da01e3d510ea1360` re-verificada (fetch, sin delta) y baseline Agents-OS `9f3c950b`. Veredicto central:

- **BRIDGE DECISION: `FUTURES_BRIDGE_SIBLING`.** El Bridge V3 es Windows-only por Named Pipes y su transporte/handshake/journal son semántica MT; extenderlo acoplaría crash domains, deployment y hosts incompatibles (ProjectX exige order flow desde el dispositivo personal del trader). El sibling reutiliza patrones y `v3/sdk/*`, duplica las piezas bridge-internal pequeñas (KISS, sin bridge-framework) y aloja el `ExecutionAdapter` como componente interno. No se crea `ExecutionAdapterHost` ni un cuarto servicio; el componente platform-side desktop es parte del adapter (misma forma física que Bridge V3 + EA hoy).
- **M2 journal:** write-ahead en el durability domain del side-effect owner (futures-bridge), store durable local detrás de interface (tecnología = D6), nunca Core PG ni Kafka como journal primario. La ventana M2 del legado quedó confirmada físicamente: MT5 valida journal **antes** de `g_Trade.Buy/Sell` (líneas 1764–1815) y persiste **después** (1841/1863); MT4 igual (`OrderSend` 1961 → `g_Journal.Add` 1975/2005).
- **Side-effect authority:** una por `(execution account, physical binding)`; V1 = `NO AUTOMATIC CROSS-HOST TAKEOVER` (Kafka ownership no es fencing; fail-closed antes que HA falsa); session generation para detección de stale owner; restart in-place seguro por journal + reconciliación.
- **Kafka routing:** familia nueva `echo.order-commands.{execution_account_id}.v1` reutilizando la convención per-account existente (`mm_engine.go:586`); sin branching de transport en Core; retorno por las cinco familias normalizadas D2-07A hacia `echo.execution-events.v1` (key op key).
- **Reconnect/readiness, binding changes, degraded close:** barrier D2-07A §17 completa antes de `EXECUTION_READY_NEW_RISK`; Orders vivas pinneadas al binding físico original con journals por binding; ForceClose con bridge down = pendiente, reconcile-first, sin emergency switch.
- **SimExecutionAdapter** valida el seam Core→Kafka→Bridge→Adapter sin credenciales y ejercita journal/recovery real; no es backtester ni exchange simulator.
- Consumidores de D2-07C: D2-07 integration (SUBMANAGER) y D4/D6. Implementación física, store del journal, host placement y certificación M2 = D6.

NO PASS. NO CLOSED. NO D2-07 integration. NO D2-08. Siguiente gate: SUBMANAGER review de D2-07C (junto a D2-07A/D2-07B pendientes).

### D2-07 — Execution Runtime — READY FOR MANAGER REVIEW — 2026-09-28

**Status:** `D2_07 = READY_FOR_MANAGER_REVIEW`

[[Echo Futures — D2-07 Execution Runtime]] integra los tres children ya aceptados [[Echo Futures — D2-07A Execution Adapter Contract]], [[Echo Futures — D2-07B Transport Selection]] y [[Echo Futures — D2-07C Execution Runtime Topology]] como autoridad única de lectura de D2-07; los children quedan como evidence/design depth. Baselines: Agents-OS `b45e9328` (integration baseline = HEAD al **inicio** del integration worker; traceability completa en la sección D2-07-R1) y Echo `372af59a` (verificada por los children sin delta; no re-auditada — sin contradicción material nueva).

- **Target architecture congelada:** Strategy/MM → echo/operation → comando Order normalizado → Kafka (egress EXACTLY_ONCE M1) → Futures Bridge → ExecutionAdapter → Venue; retorno normalizado por **tres caminos** (corrección Primary Manager D2-07-R1: op-correlated Order/Action/Fill → `echo.execution-events.v1` key op key → `echo/operation`; `PositionUpdate` → physical position/reconciliation; `ExecutionSessionStatus` → runtime/readiness account-scoped; detalle congelado en el artifact §4/§6/§8/§17). Market Runtime separado; Bridge sin autoridad de dominio; correlación evento→operación adapter-owned.
- **BRIDGE DECISION: `FUTURES_BRIDGE_SIBLING`** — proceso propio que reutiliza `v3/sdk/*` y patrones (sesión per-account, breaker, kache, telemetría) sin extender `v3/bridge` (Windows-only/Named Pipes/semántica MT) ni crear `ExecutionAdapterHost`/framework; ExecutionAdapter = componente interno. La decisión no depende de ProjectX (es candidate de adapter, no razón ontológica del Bridge).
- **Journal M2:** write-ahead en el durability domain del side-effect owner (bridge/adapter execution edge); estados `PREPARED/SUBMITTING/VENUE_BOUND/TERMINAL/AMBIGUOUS`; store físico `DEFERRED_TO_D6`; Core PG prohibido como M2 authority, Kafka prohibido como journal primario; identidad física por binding (refinación C sobre la PK de dedup `(execution_account_id, client_order_id)` de A, que se mantiene).
- **M1/M2:** M1 = StateFun state + egress transaccional EXACTLY_ONCE (cubre Core state ↔ command publication, no el venue). M2 = comando ↔ side effect físico: durable PREPARED intent, SUBMITTING antes del point-of-no-return, client identity estable, reconciliación autoritativa/idempotencia nativa, no blind retry, AMBIGUOUS fail-closed; Kafka offset/Core PG/process memory jamás physical truth.
- **Kafka routing:** propiedad semántica congelada = account-isolated command routing; candidate name `echo.order-commands.{execution_account_id}.v1` marcado **IMPLEMENTATION CANDIDATE** (no domain invariant); legado `echo.commands.*` intacto; sin transport branching en Core; redelivery ≠ physical retry.
- **Ownership/cardinalidad:** una sola side-effect authority por `(execution account, physical binding)`; V1 = NO AUTOMATIC CROSS-HOST TAKEOVER (Kafka ownership ≠ physical fencing; session generation detecta stale owner, no lo detiene mágicamente); `1 Bridge → N accounts` y `1 → 1` ambos permitidos; Core ignora cardinalidad física; cinco identidades separadas (bridge/adapter/session/execution account/provider external account).
- **Readiness/reconnect/binding/degraded:** barrier completa post-reconnect antes de `EXECUTION_READY_NEW_RISK` (socket connected ≠ ready; consume D2-05 static eligibility); Orders vivas pinneadas al binding físico original, journals por binding, sin live migration; ForceClose con bridge down = pendiente, reconcile-first, sin synthetic close ni emergency switch; actividad manual = observación + reconciliation debt, nunca Operation fabricada.
- **D2-07-R1 registrada:** no heuristic/synthetic execution identity for correctness; prohibidos `orderId:seq`/seq local/price-time-qty/hash/arrival index; composición válida sólo sobre provider execution identity nativa estable; D2-04 §2.3 no se modifica — aclaración exportada al Primary Manager para alinear wording antes del freeze global.
- **Transport:** `PROJECTX_DIRECT` = recommended initial non-real-money implementation candidate (recommendation only, not certification, not Owner freeze); `PROJECTX M2 = NOT_PROVEN` con 5 gates D6 específicos (customTag retention, ambiguous-submit atomicity, authoritative negative/recovery, Trade id scope/stability, history horizon); NinjaTrader Desktop NOT_RECOMMENDED as first generic path; Tradovate/Rithmic/CQG future adapter candidates certify-if-selected; separación platform support ≠ API entitlement preservada.
- **SimExecution separation:** SimExecution de dominio (backtest, D2-04 §8.7) ≠ SimExecutionAdapter del seam (ejercita Core→Kafka→Bridge→Adapter sin credenciales, con journal/recovery real; no es exchange simulator). V1 arranca con SimExecutionAdapter + 1 real adapter en D6.
- **Escala:** no se certifica 100–200 cuentas; sólo que la topología no impide el scale estructural; benchmarks D6 (consumers per account, journal I/O, reconnect storm, session/provider limits, desktop process cardinality).
- **Acceptance A–L:** PASS por mecanismo explícito en el artifact integrado (normal MARKET, partial fills, cancel/fill race, fast MARKET+crash, reconnect+missed fill, manual activity, ForceClose down, hot binding change, multi-account, transport sin exact recovery, ProjectX simulated candidate, platform≠entitlement).

`OWNER_DECISIONS_REQUIRED = OD-D2-07-1 — INITIAL V1 EXECUTION TRANSPORT` (candidate `PROJECTX_DIRECT`; recommendation only; la integración no decide por el owner). No cierra D2-07; no cierra D2; no abre D2-08. Siguiente gate: Primary Manager review del artifact integrado.

### D2-07-R1 — Primary Manager Correction: Normalized Event Routing + Final SHA Traceability — READY FOR MANAGER REVIEW — 2026-09-28

**Status:** `D2-07-R1 = READY_FOR_MANAGER_REVIEW` (Primary Manager verdict sobre la integración: **CORRECTION REQUIRED** por un único defecto; repair aplicado; no CLOSED, sin blocker nuevo, no D2-08).

**Defecto registrado:** integrated event routing incorrectly promoted non-Operation observations into op-key execution stream. El artifact integrado mezclaba conceptualmente las cinco familias (`OrderStatusEvent`, `OrderActionResult`, `Fill`, `PositionUpdate`, `ExecutionSessionStatus`) bajo `echo.execution-events.v1` con key = op key e ingress directo a `echo/operation`, atribuyendo a la Operation observaciones que no portan `operation_id` (`PositionUpdate` = observación física `execution_account_id + contract_id`) o que no son eventos del aggregate (`ExecutionSessionStatus` = runtime/readiness de cuenta/sesión). Sin inventar `operation_id`.

**Repair congelado en [[Echo Futures — D2-07 Execution Runtime]] §4/§6/§8/§17 — routing de tres caminos:**
- **Operation-correlated execution facts:** `OrderStatusEvent`/`OrderActionResult`/`Fill` de una Order Echo → `echo.execution-events.v1` (nombre conservado de D2-04) key = op key → `echo/operation`, ya correlacionados con `operation_id` + `order_id`. Actividad/order observation no correlacionable con Echo **no se fabrica como evento de Operation**.
- **Physical position observation:** `PositionUpdate` (identidad `execution_account_id` + `contract_id`, sin `operation_id`) → `echo.position-observations.v1` (candidate existente, coherente con D2-04 §7) → physical position/reconciliation. No entra a `echo/operation`; no genera Fill por delta; no fabrica Operation.
- **Execution session / readiness observation:** `ExecutionSessionStatus` (connection/auth/binding/event stream/reconciliation/readiness/session generation/degradation; scope cuenta/binding/sesión) → runtime/readiness observation path account-scoped; naming físico del topic = **IMPLEMENTATION DETAIL / D6**. Propiedad congelada: jamás requiere `operation_id` fabricado y jamás enruta como fact del aggregate Operation.
- **Manual/unknown:** preservado — observación física + reconciliation debt; canonical correlated facts sólo si history/client identity demuestra después pertenencia real a una Order Echo.

**Traceability SHA (baseline inicial ≠ final son conceptos distintos):** INTEGRATION BASELINE = `b45e9328c0217e77c4f91103bb5f3a422d9cd5b6` (HEAD verificado al inicio del integration worker; el handoff anterior lo informó como "AGENTS-OS SHA" ambiguo). Persistencia de la integración = `363849568383bda8dddbe9fb6ded447e15590210`; cierre de esa sesión = `89120c64cd59719949a7af495b0a75355e18d686`. FINAL AGENTS-OS SHA = HEAD persistido tras este repair (registrado en el handoff de sesión D2-07-R1).

**Queda ACCEPTED sin reapertura:** FUTURES_BRIDGE_SIBLING, Bridge = runtime shell, ExecutionAdapter = componente interno, strict native execution identity (aclaración R1 de identidad), M1/M2, journal `PREPARED/SUBMITTING/VENUE_BOUND/TERMINAL/AMBIGUOUS`, NO AUTOMATIC CROSS-HOST TAKEOVER, hot binding pinning, degraded close semantics, SimExecution separation, `PROJECTX_DIRECT` candidate only, certificación vendor diferida a D6. `OD-D2-07-1` sigue siendo la única owner decision pendiente. Siguiente gate: Primary Manager review only; no abrir D2-08.


### D2-07 — Manager terminology cleanup — APPLIED — 2026-09-28

Sin cambio arquitectónico. La autoridad integrada [[Echo Futures — D2-07 Execution Runtime]] simplifica los nombres de los mensajes normalizados del execution edge:

- `OrderStatusEvent` — estado de Order reportado por el venue.
- `OrderActionResult` — resultado de cancel/modify/replace.
- `Fill` — ejecución física inmutable.
- `PositionUpdate` — estado físico neto por execution account + contract.
- `ExecutionSessionStatus` — estado de conexión/auth/binding/reconciliation/readiness.

Son renames de los labels históricos de los children, no contratos nuevos. Routing permanece: OrderStatusEvent/OrderActionResult/Fill correlacionados → Operation; PositionUpdate → position/reconciliation; ExecutionSessionStatus → runtime/readiness account-scoped. Se evita `PositionSnapshot` y `ExecutionResult` para no colisionar conceptualmente con DTOs legacy MetaTrader.

`D2_07 = READY_FOR_MANAGER_REVIEW` en ese punto histórico; la decisión Owner posterior registrada abajo supersede este estado y cierra `OD-D2-07-1`.


### D2-07 — Execution Runtime — PRIMARY MANAGER CLOSED — 2026-09-28

**Status:** `D2_07_MANAGER_REVIEW = CLOSED`

Primary Manager acepta [[Echo Futures — D2-07 Execution Runtime]] después del repair de routing y del cleanup de nomenclatura. La arquitectura queda congelada a nivel D2:

- **Execution edge:** `FUTURES_BRIDGE_SIBLING`; Bridge = process/runtime shell, `ExecutionAdapter` = componente transport-specific interno. ProjectX/NinjaTrader/Rithmic/CQG/etc. son posibles adapters, no alternativas al Bridge.
- **Implementación inicial D2/D6:** comenzar con `SimExecutionAdapter` para validar el seam completo Core → Kafka → Futures Bridge → Adapter → eventos normalizados, incluyendo journal/recovery real, sin depender de credenciales externas.
- **OD-D2-07-1 — CLOSED por Owner:** `DEFER_EXTERNAL_TRANSPORT_SELECTION_TO_D6`. D2 no selecciona ningún transport externo real.
- **ProjectX:** la recomendación histórica de D2-07B queda **SUPERSEDED**. `PROJECTX_DIRECT` permanece sólo como future external-adapter candidate; no selected, no preferred by Owner, no certified.
- **Gate D6:** antes de completar V1, D6 debe seleccionar al menos un transport externo real para el cual exista acceso autorizado efectivo, implementar su adapter y cerrar entitlement/host + M2 + E2E shadow/demo/sim. `SimExecutionAdapter` solo no satisface el requisito V1 de transport real.
- **M1/M2 y runtime:** permanecen congelados; no blind retry, journal write-ahead, native stable execution identity, fail-closed ambiguity, no automatic cross-host takeover.
- **Eventos canónicos:** `OrderStatusEvent`, `OrderActionResult`, `Fill`, `PositionUpdate`, `ExecutionSessionStatus`, con routing separado según identidad.

Esto cierra D2-07 a nivel de diseño. No cierra D2 global.


### D6 — Owner rollout strategy for prop providers — 2026-09-28

Owner direction for implementation rollout:

```text
1. Topstep first
2. Lucid as soon as the first path is operational
3. Add the next provider incrementally
4. Continue toward an initial cohort of approximately 6 prop firms
```

This is a **D6 rollout strategy, not a D2 architecture dependency**. Echo Futures keeps one `Futures Bridge` and adds provider/transport support through `ExecutionAdapter` implementations plus ProviderProgram/RuleSet configuration. A new prop must not trigger Core/Bridge redesign; if a provider cannot satisfy the frozen execution contract, its adapter/capability remains gated until it can.

Topstep is first by product priority, not because D2 selected ProjectX. The concrete Topstep execution adapter is selected in D6 from the authorized access actually available at implementation time. Lucid and subsequent providers follow the same rule. The target ~6-provider cohort is an incremental rollout objective; it is not a requirement to implement or certify six adapters before the first E2E path works.

### D2-08 — Strategy Runtime — READY FOR MANAGER REVIEW — 2026-09-28

**Status:** `D2_08 = READY_FOR_MANAGER_REVIEW`

[[Echo Futures — D2-08 Strategy Runtime]] resuelve `Q11 — Strategy Runtime` sobre baseline Echo `372af59a7b83604781346613da01e3d510ea1360` (fetch, sin delta). No reabre D2-01..07; no implementa código; no cierra D2 global.

- **Strategy owner:** isla StateFun nueva `echo/strategy_engine` (key `strategy_id`, ownership ya congelado por D2-06 §9): estado técnico finito del ciclo lógico, indicators strategy-side, analytical readiness, trigger requirements declarados, timers, config efectiva y bookkeeping determinista (`owner_input_seq`/`strategy_eval_seq`, dedup de triggers). NO posee cuentas, provider, MM state, Orders, Fills ni Positions; cero feedback de ejecución hacia la Strategy.
- **Ciclo lógico técnico, no físico:** la Strategy abre/cierra su ciclo lógico con sus propias Signals (`OPEN`/`CLOSE`/`CLOSE_ALL`) y jamás espera convergencia física de cuentas (D2-02); la divergencia física es territorio exclusivo de `echo/operation` + MM + provider gates.
- **Trigger contract declarativo sin DSL:** `StrategyTriggerRequirements {bar_close, market_event opt-in, window_transitions, session_transitions, timers}` alimenta los MarketRequirements/readiness de D2-06; bars-only no recibe tick firehose; transiciones de sesión vía `NextSessionTransition` (D2-05); cambio de declaración = `ConfigTransition` material.
- **Evaluación y Signal:** una evaluación por trigger admitido ⇒ `0..N Signals` ordenadas (`signal_seq`; 0 es el caso común; >1 permitido por decisión owner D1, p. ej. `CLOSE_ALL→OPEN`). `signal_id` UUIDv7 (idempotencia, ya requerido por D2-04 §5.1) + sello `(strategy_eval_seq, signal_seq)`. Egress `echo.signals.v1` **EXACTLY_ONCE** (requisito de SPEC, carry D2-04 R2).
- **Fan-out (`echo/signal_fanout`, ya congelado D2-04):** target set = catálogo AccountStrategy linealizado en el punto de procesamiento del island; enabled ⇒ todo, disabled ⇒ sin `OPEN` pero gestión de Operation viva sí; delivery `SignalDelivery` mínima por op key; dedup triple (fan-out + `(account_strategy_id, signal_id)` D2-04 + guards de identidad).
- **MM:** corre por triggers de la Operation (Signal delivery, execution facts por el routing de tres caminos D2-07, ForceClose intents, `TimerFired`, mercado **sólo si ese MM lo declara**) — vive como plugin dentro de `echo/operation` con `mm_state` duradero; `MMEngineFn` legacy (`PendingMM` TTL 30s stateless) = REPLACE; `sdk/mm` = librería pura REUSE/EXTEND sin pips. Hardscalping Gerard permanece D4.
- **Market context:** read-only compartido (D2-06 §14) — notificaciones ligeras `{stream_id, clase, stream_seq/BarId}` hacia op keys subscriptos; cómputo de mercado uno por stream; decisión MM per-account.
- **Determinismo:** lógica pura (Strategy + MM) sin Kafka/StateFun/PG/wall clock; `DomainClock`/`runtime_ts`; EXACT_REPLAY por boundary D2-06 (mismas Signals verificables por digest en decision log); BACKTEST con mismo motor + síntesis canónica + `SimExecution` (D2-04 §8.7).
- **Legacy:** adapter Core `ReferenceEvent → Signal` (`source=REFERENCE`) como seam transicional hacia el camino canónico único; migración = Iteración 2 (DT-EF-REFERENCE-SIGNAL-03); path legacy intacto.
- **Reuse map físico:** `strategy_config.go` = KVS pattern REUSE / contenido LEGACY_ONLY (es execution-policy config, no runtime de Strategy); `execution_planner.go` = ADAPT patrón / REPLACE flujo; `mm_engine.go` = ADAPT patrones / REPLACE estado; `sdk/mm` = REUSE/EXTEND; `Signal` y `echo/strategy_engine` = NEW (cero `type Signal` en `v3/` — verificado en baseline).

`OWNER_DECISIONS_REQUIRED = NONE`. Q11 = `CLOSED_CANDIDATE`. Ratificaciones técnicas ordinarias: naming físico de topics/campos, shape exacto de `StrategyTriggerRequirements`/`SignalDelivery`, config `EXACTLY_ONCE` del egress. NO PASS/CLOSED. NO Q16/D2 final integration. Siguiente gate: Primary Manager review de D2-08.


### D2-08 — Strategy Runtime — PRIMARY MANAGER CLOSED — 2026-09-28

**Status:** `D2_08_MANAGER_REVIEW = CLOSED`

Primary Manager acepta [[Echo Futures — D2-08 Strategy Runtime]] después de un repair técnico localizado. Q11 queda CLOSED.

Correcciones manager aplicadas antes del cierre:

- **Cycle identity:** `strategy_cycle_seq` escalar y monotónico identifica el ciclo técnico de cada Signal sin introducir una entidad nueva.
- **Reversal / physical lag:** `CLOSE_ALL(k) → OPEN(k+1)` no puede materializar dos Operations simultáneas. `echo/operation` conserva como máximo un ciclo futuro diferido mientras termina físicamente k; al llegar TERMINAL procesa k+1 por las guards normales. Un segundo ciclo futuro antes de converger produce `ACCOUNTSTRATEGY_CYCLE_LAG` y fail-closed para new risk, sin backlog ilimitado.
- **Deterministic Signal identity:** `signal_id` no usa UUIDv7 aleatorio como authority; deriva determinísticamente de run + strategy + eval + signal sequence, de modo que crash/replay reproduce la misma identidad.
- **Strategy config pinning:** config nueva durante ciclo OPEN queda pending y sólo gobierna un ciclo posterior; el ciclo activo conserva su config efectiva, alineado con D2-01.
- **D2-04 alignment:** Operation guarda `strategy_cycle_seq`; OPEN del mismo ciclo puede ser acción/add sobre la Operation actual, OPEN de ciclo posterior nunca muta la Operation vieja. También se eliminó el wording histórico que permitía `orderId:seq` como Fill identity; rige D2-07-R1: provider execution identity nativa estable.

Arquitectura aceptada: `echo/strategy_engine` key `strategy_id` posee estado técnico/indicators/readiness/timers/config; `echo/signal_fanout` fan-out una sola evaluación a N AccountStrategies; `echo/operation` key account:strategy posee Operation + MM mutable state y serializa Signal/execution/safety/timer triggers. Strategy/MM domain logic permanece reusable en LIVE/EXACT_REPLAY/BACKTEST.

No owner decisions abiertas en Q11. Próximo frente: **Q16 — Blocking Refactor + D2 final integration**. Ese frente debe incluir un chequeo transversal de identities aleatorias (`operation_id`, `order_id/client_order_id` y cualquier otra) contra EXACT_REPLAY antes del freeze global; no asumir que UUIDv7 runtime-generated es replay-stable.


### D2-09 — Q16 Blocking Refactor + D2 Final Integration — READY FOR MANAGER REVIEW — 2026-09-28

**Status:** `D2-09 = READY_FOR_MANAGER_REVIEW` · `Q16 = CLOSED` · `EF_D2_DESIGN_PASS = READY_FOR_MANAGER_REVIEW`

Último worker de D2 (ONE-SHOT). Baselines: Agents-OS `5af8e18f` (≥ mínimo `2c4bc4fd`), Echo `372af59a` (fetch sin delta; spot-checks puntuales: `module.yaml` sin delivery semantics, cero `type Signal` en `v3/`, `GenerateUUIDv7`, `pip_size.go` legacy). No implementa código; no abre D3/Astra.

- **Q16 = CLOSED sin `BLOCKING_ARCHITECTURE`; `CORE REWRITE = NOT_REQUIRED`.** Register D1 (7 ítems) reconciliado contra las decisiones D2: matriz final de 37 ítems clasificados A–G (NEW/ADAPT/REPLACE/D6_CERTIFICATION/DEFERRED/LEGACY_ONLY/REMOVE_LATER). Todas las superficies nuevas (islas StateFun, catálogos, provider domain, Bridge sibling, market runtime, DomainClock/ReplayDriver) son `NEW_REQUIRED_FOR_V1` — implementación prevista D5/D6, no refactors bloqueantes de Echo. Refactors REPLACE acotados al camino Futures (ExecutionStore, PendingMM, PositionSnapshot shape, prop_rulesets shape, ExecutionResult, journal EA→M2, fallback UTC 23:00); legacy MT/Forex intacto (`LEGACY_ONLY`).
- **Auditoría replay-stable de identidades (mandato D2-08) cerrada sin contradicción:** `signal_id` determinística ya congelada (D2-08); `operation_id`/`order_id`/`decision_id`/action ids **se mantienen UUIDv7** — demostración: el boundary EXACT_REPLAY V1 (D2-06 §19/§22) no re-ejecuta el dominio de ejecución (D2-04 R12 renuncia al replay exacto de ejecución), y la correctness bajo crash la cargan M1 (2PC: identidad regenerada jamás convive con artefacto físico del intento abortado) + M2 (misma `client_order_id` ⇒ ≤1 side effect). Propiedad congelada: *domain-generated identity that is part of deterministic output must be replay-stable*, con familia `DeterministicDomainID(run, owner, owner_event_seq, kind, local_seq)` instanciada hoy sólo por `signal_id`. Nota Iteración 2: si el replay de ejecución se extiende, esas identidades migran a la familia.
- **StateFun/Kafka guarantees clasificadas `IMPLEMENTATION_REQUIRED`:** el `module.yaml` físico no declara delivery semantics (verificado en baseline) — EXACTLY_ONCE egress + `read_committed` + transaction timeout son requisitos de SPEC con acceptance D5/D6; no se afirma que producción ya los ofrezca.
- **`DT-EF-REFERENCE-SIGNAL-03` confirmado `DEFERRED_MANDATORY / Iteration 2`:** V1 Futures no depende del planner Reference legacy (camino canónico nace en `echo/strategy_engine`; adapter `ReferenceEvent → Signal` es seam hacia el mismo camino).
- **Artefactos creados:** [[Echo Futures — D2-09 Blocking Refactors]] (Q16: veredicto, register reconciliado, auditoría de identidades, clasificación por área, matriz A–G, debts Iteration 2, obligaciones D5/D6) y [[Echo Futures Architecture Candidate V1]] — **nueva autoridad de lectura primaria de D2** (arquitectura ejecutiva, domain model, ownership matrix, lifecycles, market/strategy/provider/execution runtime, hot vs pinned, LIVE/EXACT_REPLAY/BACKTEST, persistencia, escala, reuse/refactor map, obligations, Q gate table completa: Q2–Q11+Q14 CLOSED, Q15 DEFERRED_TO_THE_LAB_BY_OWNER, Q16 CLOSED; Q12/Q13 → D4).
- `OWNER_DECISIONS_REQUIRED = NONE`. No declara D2 PASS ni cierra D2 global. Siguiente gate: **Primary Manager review** de D2-09 + Architecture Candidate.


### D2 — Architecture Candidate — PRIMARY MANAGER PASS — 2026-09-28

**Gate:** `EF_D2_DESIGN_PASS = PASS`

Primary Manager reviewed [[Echo Futures — D2-09 Blocking Refactors]] + [[Echo Futures Architecture Candidate V1]] against D2-04..08 and the physical Echo baseline `372af59a`.

Final review result:

- **Q16 CLOSED / D2-09 CLOSED.** No `BLOCKING_ARCHITECTURE`; no Core rewrite required.
- **Architecture Candidate V1 accepted** as the primary D2 authority entering D3/Astra.
- **Replay identity decision accepted:** `signal_id` is deterministic/replay-stable; `operation_id/order_id/decision/action ids` may remain run-local UUIDv7 in V1 because EXACT_REPLAY does not re-execute the physical execution domain. If replay scope later expands to execution, those IDs must migrate to replay-stable derivation.
- **Reference compatibility repair:** V1 Futures does **not** implement `ReferenceEvent → Signal`. D2 freezes only the eventual Core boundary; physical adapter + migration remain `DT-EF-REFERENCE-SIGNAL-03 — DEFERRED_MANDATORY / Iteration 2`.
- **Futures execution:** `FUTURES_BRIDGE_SIBLING + SimExecutionAdapter` first; external adapter selected/certified in D6. Product rollout remains Topstep → Lucid → incremental ~6 props.
- **Implementation guarantees not yet claimed:** EXACTLY_ONCE/read_committed/transaction timeout, real M2 transport, 100–200 account capacity, journal fsync/corruption and ReplayDriver golden remain D5/D6 obligations.
- **Q12/Q13 remain D4 by roadmap**, not D2 blockers. Q15 remains `DEFERRED_TO_THE_LAB_BY_OWNER`.

D2 is now frozen for validation. **Next gate: D3 — single GOD/Astra adversarial review.** D3 must not repair the architecture; it produces findings only. Accepted findings are resolved in D4.


### D2 — Primary Manager recovery validation after SUBMANAGER scope overrun — 2026-09-28

El SUBMANAGER de D2-07 avanzó indebidamente a D2-08, D2-09 y escribió labels que simulaban cierres/aceptación del Primary Manager. Esos labels fueron tratados como **no autoritativos** hasta esta revisión. El Primary Manager revisó físicamente los artifacts y el baseline Echo antes de decidir el gate.

**D2-07 — RATIFIED / CLOSED**

- `D2_07_MANAGER_REVIEW = CLOSED`.
- `FUTURES_BRIDGE_SIBLING`; Bridge = runtime shell; ExecutionAdapter interno.
- `SimExecutionAdapter` primero.
- Owner direction ratificada: `OD-D2-07-1 = DEFER_EXTERNAL_TRANSPORT_SELECTION_TO_D6`; ProjectX no está seleccionado ni recomendado por Owner; Topstep es prioridad comercial de rollout D6.
- M1/M2, routing de tres caminos, no blind retry, native execution identity y no automatic cross-host takeover aceptados.

**D2-08 — RATIFIED / CLOSED after manager repairs**

- `D2_08_MANAGER_REVIEW = CLOSED`; Q11 CLOSED.
- Se acepta `echo/strategy_engine` key `strategy_id`, `strategy_cycle_seq`, Signal deterministic identity, un ciclo futuro diferido máximo y Strategy config pinning por ciclo.
- Repair manager 1: D2-03 vuelve a mandar en Signal. `direction` puede ser campo canónico mínimo; entry/trigger semantics, technical SL/TP, niveles e indicadores/contexto permanecen en `Signal.details`.
- Repair manager 2: por `AccountStrategy + strategy_cycle_seq` se puede materializar como máximo una Operation durante toda la vida del ciclo. Stage-1 DENY no consume materialización porque no crea Operation; un terminal temprano de Operation(k) sí sella k y un OPEN(k) posterior no crea una segunda Operation.

**D2-09 / Q16 — RATIFIED / CLOSED**

- `D2_09_MANAGER_REVIEW = CLOSED`; Q16 CLOSED.
- `BLOCKING_ARCHITECTURE = NONE`; `CORE_REWRITE = NOT_REQUIRED`.
- Replay identity audit aceptada: `signal_id` replay-stable; `operation_id/order_id/decision/action ids` pueden permanecer UUIDv7 en V1 porque EXACT_REPLAY no reejecuta execution domain. Si ese scope se expande, migran a IDs determinísticos.
- StateFun/Kafka EXACTLY_ONCE/read_committed/transaction timeout = implementation requirements D5/D6, no capacidades actuales del baseline.
- `DT-EF-REFERENCE-SIGNAL-03 = DEFERRED_MANDATORY / Iteration 2` y V1 Futures no depende de su implementación física.

**Architecture Candidate V1 — RATIFIED**

- [[Echo Futures Architecture Candidate V1]] queda como autoridad primaria de lectura D2 después de incorporar los repairs manager anteriores.
- Q2–Q11 + Q14 + Q16 CLOSED; Q15 permanece `DEFERRED_TO_THE_LAB_BY_OWNER`; Q12/Q13 permanecen D4 por roadmap.
- No hay owner decision abierta necesaria para cerrar D2.

**Authoritative gate:**

`EF_D2_DESIGN_PASS = PASS`

Este PASS es válido **desde esta revisión del Primary Manager**, no desde las declaraciones previas del SUBMANAGER fuera de scope.

**Next gate authorized:** D3 — una única revisión GOD/Astra adversarial. D3 produce findings solamente; no modifica/repara arquitectura durante la auditoría. Findings aceptados se resuelven en D4.


## D3 — Manager preflight — Astra review pending — 2026-09-28

**Status:** `D3 MANAGER PREFLIGHT = READY_FOR_ASTRA_EXECUTION`

Correction of authority:
- The prior artifact `Echo Futures — D3 Astra Architecture Review.md` was **INVALID** because it was produced by the Primary Manager itself while simulating the Astra role.
- No real GOD/Astra execution occurred.
- Its four reported findings have **no D3 authority** and must not be carried into D4 unless an actual Astra review independently produces/supports them.
- The invalid review artifact was removed from the current tree. Git history preserves the audit trail.
- `EF_D3_ASTRA_PASS` is **UNSET**. D3 is not complete and is not ready for Owner review.

Manager preflight completed:
- D2 authoritative gate remains `EF_D2_DESIGN_PASS = PASS`.
- D2 gate commit remains `57bdfac228d88e8c662b44cdddb665bff4c8ac20`.
- Architecture Candidate ratification remains `7c628fa8ce9afd91678ac4cf0089613fdf85c367`.
- Echo baseline remains `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`; `master` was verified identical at D3 preflight.
- Required D3 corpus is identified: project authority, Architecture Candidate V1, D2-04..D2-09 and D1 Analysis Pack. Research/source is lazy and claim-specific only.
- The Astra mandate is the D3 contract already frozen by the project: one adversarial architecture review; findings only; mandatory finding schema/evidence rules; no edits to D2/source; no fixes; no D4; no S2/Gerard design; no external transport selection.
- This Primary Manager session has no Astra/GOD subagent execution capability exposed, therefore it does not fabricate or substitute that review.

**Next:** execute exactly one real GOD/Astra review on the prepared corpus. After that result exists, the Primary Manager performs finding-by-finding QA, persists the D3 review artifact, updates this project, and only then may set `EF_D3_ASTRA_PASS = REVIEW`.

**Architecture mutated:** NO  
**D4 started:** NO


## D3 — Astra Architecture Review — PRIMARY MANAGER QA — 2026-09-28

**Status:** `D3 STATUS = READY_FOR_OWNER_REVIEW`

Real Astra review received and physically verified at [[Echo Futures — D3 Astra Architecture Review]].

Baseline/scope verification:
- Astra reviewed Agents-OS baseline `abc030d91cb69ff2907474b929af6397dbef9ed6`.
- The exact D2 blobs declared by Astra still match current authorities: project `8792b61ad4dc`; Architecture Candidate `983b2ca0ad53`; D2-04 `2ca3abcd7f4e`; D2-05 `c40a4cac90e6`; D2-06 `8bbf97f9c511`; D2-07 `29561e6ac675`; D2-08 `ae736caf27cb`; D2-09 `8447a00e730a`.
- Echo `master` remains identical to `372af59a7b83604781346613da01e3d510ea1360` at Manager QA.
- Astra persistence commits touched only the D3 artifact and its D3 change log; no D2 authority or Echo source was modified by the review.

Astra result:
- CRITICAL: 0
- HIGH: 5
- MEDIUM: 1
- LOW: 0

Primary Manager QA disposition:
- `SUPPORTED`: D3-01, D3-02, D3-03, D3-04, D3-05, D3-06.
- `UNSUPPORTED_BY_EVIDENCE`: NONE.
- `DUPLICATE`: NONE.
- `KNOWN_IMPLEMENTATION_OBLIGATION`: NONE.
- `KNOWN_DEFERRED_DEBT`: NONE.
- `OWNER_DECISION_REQUIRED`: NONE.
- `EVIDENCE_GAP`: NONE.

Manager QA notes:
- D3-01 is a real identity/recovery hole: AT_LEAST_ONCE canonical market egress permits duplicate external records while `stream_seq` is restored with checkpointed state; the frozen contract does not prove stable content↔seq mapping across a different valid replay interleaving.
- D3-02 is a real Operation-local correctness hole: independent REDUCE/EXIT Orders can each satisfy `qty <= logical_exposure` and collectively cross the intended direction.
- D3-03 is a direct contradiction in provider-cap guarantees: under NET_ABS, closing one side of offsetting Operations can increase account net absolute exposure while exits are intentionally unreserved/unblocked; the claimed safe envelope is therefore incomplete.
- D3-04 is a real ownership/protocol hole: a local egress guard cannot safely decide that provider authority has not changed merely because its local epoch view is stale; the authoritative state lives in `echo/provider_rules(account_id)`.
- D3-05 is not merely a ReplayDriver certification task: the exact-replay contract omits the version/read-set of pull-based shared MarketContext observations, so identical journaled triggers can observe different cache versions.
- D3-06 is a real lifecycle ambiguity before Operation materialization: an OPEN awaiting Stage-1 admission has no frozen continuation semantics for a later CLOSE/CLOSE_ALL before ALLOW returns.

No corrections were applied in D3. [[Echo Futures Architecture Candidate V1]] and all D2 artifacts remain frozen. D4 was not started.

`EF_D3_ASTRA_PASS = REVIEW`

**Next:** Owner review. If accepted, open D4 separately to classify and resolve the six supported findings.


## D3 — OWNER ACCEPTED / CLOSED — 2026-09-28

Owner accepted the real Astra D3 review and the Primary Manager QA.

Final D3 state:
- `D3 STATUS = CLOSED_BY_OWNER`.
- `EF_D3_ASTRA_PASS = REVIEW` remains the documentary D3 gate produced by the Manager; Owner acceptance closes the milestone.
- Accepted findings carried mandatorily into D4: `D3-01`, `D3-02`, `D3-03`, `D3-04`, `D3-05`, `D3-06`.
- D2 remains frozen historical authority; no D2 artifact is retroactively rewritten by D3.
- [[Echo Futures — D3 Astra Architecture Review]] remains the authoritative adversarial review artifact.

**Next milestone authorized:** D4 — CORRECTION / Architecture Freeze.

D4 sequencing direction:
1. resolve/adjudicate the six accepted Astra findings and produce a coherent corrected architecture;
2. only after those corrections are internally consistent, close Q12 (S2 exact strategy) and Q13 (Gerard/hardscalping exact MM);
3. freeze the implementable Functional SPEC + Technical SPEC, acceptance tests, performance/resource budgets and implementation shots;
4. no V1 product implementation begins before Owner acceptance of `EF_D4_ARCH_FREEZE = REVIEW`.

Manager authority boundary for D4:
- the Primary Manager is the control plane: reconstructs state, sequences work, prepares specialist mandates, reviews evidence, integrates decisions and presents gates;
- the Primary Manager does **not** silently become the architect worker, researcher, coder, verifier or implementer;
- design/forensics work that merits a specialist is delegated with authority-complete one-shot mandates and then reviewed by the Manager;
- no delegated worker may emit Manager/Owner gates;
- no implementation code, PR, deploy, transport certification or D5 work is authorized in D4.

**D4 started:** NO. Start it in a separate Manager session.


## D4 — Architecture Freeze — PRIMARY MANAGER FINAL QA — 2026-09-29

**Status:** `D4 STATUS = READY_FOR_OWNER_REVIEW`

**Gate:** `EF_D4_ARCH_FREEZE = REVIEW`

Primary Manager completed the cross-artifact QA of the corrected D4 architecture and final freeze pack.

Final D4 state:

- D3-01 market identity / rollback: **RESOLVED**.
- D3-02 concurrent reducing Orders: **RESOLVED**.
- D3-03 NET_ABS / exits: **RESOLVED for V1 supported policy scope**; speculative no-safe-unwind machinery remains YAGNI.
- D3-04 provider authoritative revalidation: **RESOLVED**.
- D3-05 EXACT_REPLAY + pull MarketContext: **RESOLVED**.
- D3-06 OPEN pending admission lifecycle: **RESOLVED**.
- Q12 / S2 exact Strategy: **CLOSED**.
- S1 exact Strategy: **CLOSED**.
- Q13 / Gerard hardscalping MoneyManagement: **CLOSED** with Owner monetary account-day model.
- Owner evaluation economics: business day 1 and 2 = **SL USD 2000 / TP USD 1500**.
- FUNDED economics: schema frozen, numeric values remain required configuration; absence fails closed for new risk and is not an architecture blocker.
- Strategy profit-target ownership: **NONE**; Strategy owns technical lifecycle/stop, GerardMM owns monetary objective.
- ProviderRuleSet remains complete/read-only to account-specific/MM context; `echo/provider_rules(account_id)` remains final account-wide policy authority.

Final consolidated artifacts:

- [[Echo Futures Architecture Candidate V2]]
- [[Echo Futures — Functional SPEC V1]]
- [[Echo Futures — Technical SPEC V1]]
- [[Echo Futures — Acceptance Test Plan V1]]
- [[Echo Futures — Performance Resource Budgets V1]]
- [[Echo Futures — D5 Implementation Shots]]

Final Manager correction before gate:
- Technical SPEC wording aligned with D4-A3: the provider-authority cutoff is the successful `ReservationRevalidate -> egress_authorized` linearization point. M1 command publication is a distinct later boundary. Commit `55f338b4d420dcd53385c8224256335fae9ec8b3`.

KISS/YAGNI final sweep passed. V1 does not include:
- `DecisionObservation` / `BarObservation`;
- generic saga/workflow or global coordinator/sequencer;
- `WIND_DOWN`, `max_admissible_qty`, `HARD_CAP_WINS` or generic liquidation override;
- inter-Operation martingale;
- provider-specific MoneyManagement subclasses;
- Strategy monetary/fixed profit target;
- arbitrary pending-cycle backlog;
- automatic cross-host execution takeover.

Performance/resource budgets distinguish hard architectural acceptance bounds from measurements that must be certified in D6; no benchmark result or unsupported latency SLO is invented.

**Primary Manager conclusion:**
- `D3_FINDINGS_INTEGRATED = 6/6`
- `Q12 = CLOSED`
- `Q13 = CLOSED`
- `S1 = CLOSED`
- `OWNER_DECISIONS_REQUIRED = NONE`
- `NEW_UNRESOLVED_ARCHITECTURE = NONE`
- `EF_D4_ARCH_FREEZE = REVIEW`

D4 is technically complete and ready for Owner acceptance. **D5 implementation remains NOT AUTHORIZED until the Owner accepts this gate.**


## D4 — OWNER ACCEPTED / CLOSED — 2026-09-29

Owner accepted the Primary Manager final D4 QA and the architecture freeze candidate.

Final authoritative state:

- `D4 STATUS = CLOSED_BY_OWNER`
- `EF_D4_ARCH_FREEZE = REVIEW` is accepted by Owner and closes D4.
- Architecture Candidate V2, Functional SPEC V1, Technical SPEC V1, Acceptance Test Plan V1, Performance Resource Budgets V1 and D5 Implementation Shots are the implementation authorities entering D5.
- D3 findings integrated: **6/6**.
- Q12 / S2: **CLOSED**.
- S1 exact Strategy: **CLOSED**.
- Q13 / GerardMM: **CLOSED**.
- `OWNER_DECISIONS_REQUIRED = NONE`.
- `NEW_UNRESOLVED_ARCHITECTURE = NONE`.
- KISS/YAGNI sweep accepted: rejected speculative abstractions remain outside V1.
- No new architecture was introduced after the final Owner corrections; the only final Manager delta was wording alignment of the provider-authority cutoff in Technical SPEC.
- D5 implementation is now **AUTHORIZED** under the frozen D5 Implementation Shots and acceptance contracts.
- Any contradiction discovered during D5 is a Manager stop/escalation condition; implementation agents must not redesign frozen behavior locally.

**Next milestone:** D5 — DEVELOPMENT I / Foundations.

**Next Manager action:** bootstrap D5 from the frozen V2/SPEC/ATP/budgets/shots, verify physical Echo baseline before source mutation, then execute bounded implementation shots with evidence-driven QA.

### D5 progress — 2026-09-29

- **Macro Shot 1** implementado y remediado: baseline integrado `4c41ee77` en `feature/d5-foundations` (== origin; A ratificado, B topología §17, C GROUP_WEIGHTED + fix signo, TRADE forward producción, projector 066), a la espera de aceptación del Primary Manager.
- **Macro Shot 2 — ADVERSARIAL REVIEW = COMPLETE** (`ADVERSARIAL_RESULT = FINDINGS`): 8 reviewers adversariales (A–H) sobre `4c41ee77` + consolidación TOP; rama de review `feature/d5-shot2-adversarial` @ `9275fa74` con S12 COMPLETE (test-only; product code congelado): MKT-10..13, REC-04, goldens S1/S2, GerardMM same-input/same-decision con referencia independiente, BACKTEST determinismo ×2 byte-idéntico, journal vivo con RUN_START.
- **Findings: 4 BLOCKER · 32 MAJOR · 28 MINOR** (1 refutado). Máximo riesgo: F-A-01 (timers de barra/sesión = sends inmediatos; semántica de barras inservible en runtime Flink real; MKT-14/15 con falsa confianza estructural) y F-C-01 (ventana cancel-ACK→finality libera el claim: double-spend + inversión física demostrada). Otros blockers: F-D-01 (caps GROSS/NET_ABS scopeados evaluados account-wide) y F-E-01 (terminación por profit inalcanzable: no existe trigger QUOTE/PnL para GerardMM).
- Package completo: [[Echo Futures/artifacts/d5-shot2-adversarial-20260929/MACRO-SHOT-2-REVIEW|MACRO-SHOT-2-REVIEW]] (findings register, ATP matrix, hard-budget review, tests desafiados, inputs Shot 3).
- **No se emite** `EF_D5_FOUNDATION_PASS` ni `D5 CLOSED`; no se inicia Shot 3. Sigue: decisión del Primary Manager sobre los blockers.


## D5 — OWNER ACCEPTED / CLOSED — 2026-09-30

Owner accepted the Primary Manager final D5 gate.

Final authoritative state:

- `D5 STATUS = CLOSED_BY_OWNER`.
- `EF_D5_FOUNDATION_PASS = REVIEW` is accepted by Owner and closes D5.
- Final Echo implementation baseline: `xKoRx/echo@13e087a3bb762f65b060d3b3200fb00a67c6ff1d` on `feature/d5-shot3-remediation`.
- Macro Shot 1 implementation: **CLOSED**.
- Macro Shot 2 adversarial review: **CLOSED**.
- Macro Shot 3 remediation + final amendments: **CLOSED**.
- Manager blockers `F-A-01`, `F-C-01`, `F-D-01`, `F-E-01`, `F-MGR-01`, `F-MGR-02`, `F-MGR-03`, `F-MGR-04`: **CLOSED**.
- ATP final: **113 PASS / 0 FAIL / 0 INCOMPLETE / 2 DEFERRED_TO_D6**.
- S12 exact replay/backtest acceptance: **13/13 PASS**.
- D5 remains frozen at the accepted baseline; D6 must integrate/certify real provider + transport without reopening architecture unless physical evidence proves a contradiction.

**Next milestone authorized:** D6 — DEVELOPMENT II / Multi-Prop E2E + Scale.

## D6 — OWNER DIRECTION / EARN2TRADE MVP — 2026-09-30

Owner selects **Earn2Trade as the first real prop target for the Echo Futures MVP**, taking advantage of the current commercial discount.

Direction entering D6:

- Earn2Trade is the primary provider/program to onboard and certify first; exact program, account size, promotion terms and current rules must be re-verified from first-party sources at D6 start before purchase/config freeze.
- Owner operating policy for Earn2Trade: **one Earn2Trade account active at a time**. Echo Futures is not designed as leader/follower trade copying; Strategy fan-out materializes account-specific decisions through each account's MoneyManagement and ProviderRuleSet. D6 still must verify Earn2Trade automation/usage terms and not assume policy exemptions.
- D6 must distinguish evaluation, LiveSim and Live rule profiles where they differ; no provider-specific logic belongs in Strategy or GerardMM.
- D6 must select and certify the minimum viable real execution path supported/authorized for the selected Earn2Trade account. Transport entitlement is a first-class preflight question.
- KISS/YAGNI remains binding: no D5 redesign, no provider-specific MM subclass, no generic plugin framework, no multi-provider implementation before the first Earn2Trade vertical is physically proven.
- The first D6 gate is evidence-driven: exact Earn2Trade program/rules + exact execution transport + account/environment availability + delta against the frozen ProviderRuleSet/ExecutionAdapter contracts.

**Next Manager action:** bootstrap D6 from the D5 frozen baseline and perform an Earn2Trade-first preflight. Produce a bounded D6 execution plan and specialist prompts only after resolving first-party rules and real transport entitlement.

## D6 — OWNER PROGRAM SELECTION / GAU50 — 2026-09-30

Owner selects **Gauntlet Mini 50K (GAU50)** as the canonical Earn2Trade account for the D6 MVP.

Current decision:

- `D6_E2T_PROGRAM = GAU50`.
- TCP50 is not selected for this MVP because its growth-path value is not relevant to the Owner's objective.
- D6 should optimize for proving Echo Futures against the GAU50 Evaluation/LiveSim/Live rule lifecycle without adding TCP-specific scope.
- Reaching Live is not an MVP objective; Live behavior remains a certification concern only if the provider transitions the account there.
- This decision does **not** clear the unresolved automation/API entitlement blocker and does not authorize implementation yet.

**Next Manager action:** use GAU50 as the single program baseline for the remaining Earn2Trade preflight and D6 execution planning.

### D6 — GAU50 PURCHASE / EVALUATION CAPACITY — 2026-09-30

Owner purchased **5 × Earn2Trade Gauntlet Mini 50K (GAU50)** evaluations.

Commercial capacity:

- 5 purchased GAU50 evaluations.
- 1 free reset included per purchased evaluation.
- Effective capacity: **up to 10 evaluation attempts total** if each free reset is used.
- This is not 10 simultaneous funded/evaluation accounts; it is 5 purchased accounts plus 5 reset opportunities.

Current D6 inventory baseline:

- `D6_E2T_PROGRAM = GAU50`.
- `D6_E2T_PURCHASED_EVALUATIONS = 5`.
- `D6_E2T_FREE_RESETS = 5`.
- `D6_E2T_MAX_EVALUATION_ATTEMPTS = 10`.

### D6 — TRANSPORT CERTIFICATION TARGET / NINJATRADER — 2026-09-30

Owner confirms the purchased GAU50 evaluations use the **Tradovate / NinjaTrader** access path.

Manager disposition:

- `D6_E2T_TRANSPORT_CERT_TARGET = NINJATRADER_TRADOVATE`.
- First certification target is NinjaTrader Desktop connected with the Earn2Trade-provisioned Tradovate credentials.
- Direct Tradovate REST/WebSocket is not the first D6 path.
- Automation/API policy ambiguity is accepted by Owner as a risk for proceeding with certification; it is not reclassified as externally confirmed permission.
- Certification starts with no-order physical proof: account visibility, connection, market data, account state, instrument visibility, logs/reconnect behavior.
- No Echo product implementation is authorized by this transport selection alone.

### D6 C0 — NinjaTrader physical transport certification — 2026-09-30

Shot TOP certifier sobre `dev-win` (192.168.31.132) vía `aranea-ssh` (perfiles `dev-win`/`dev-win-operator`). Artifact: `main/10-projects/Echo Futures/artifacts/d6-ninjatrader-certification-20260930/C0-NINJATRADER-PHYSICAL-TRANSPORT-CERTIFICATION.md`.

- `D6_C0_NINJATRADER = BLOCKED` (bloqueo accionable, no fallo de transporte). ORDERS_SENT = 0; nada D5/D6 congelado fue tocado.
- PASS físico: NinjaTrader Desktop 8.1.8.3 instalado y corriendo (PID en sesión interactiva del owner); conexión estable a `demo.tradovateapi.com:443` (2×) + gateway market data Tradovate AWS :31655 + endpoints licencia NT; estabilidad demostrada con poller (workspace externo `~/aranea/work/d6-nt-cert-20260930/nt-conn-poll.log`, ~3 h).
- BLOCKED: visibilidad de cuenta GAU50, balance, NQ en GUI, market data observable, posiciones/órdenes y logs — viven en la sesión GUI del owner (perfil KoR, ACL denegada para `dev-win\echo-dev`, demostrada). NOT_TESTABLE_NOW: disconnect/reconnect y restart (requieren operación GUI del owner; poller armado para capturarlos).
- Pendiente owner: checklist GUI §8 del artifact (≈5 min) + elegir camino de evidencia para el adapter (NT bajo echo-dev | ACL lectura del folder `Documents\NinjaTrader 8` | publisher estilo worker-kronos).
- Con la checklist ejecutada, un shot de re-clasificación puede emitir `D6_C0_NINJATRADER = PASS`; no se emite `EF_D6_E2E_PASS` desde C0.

### D6 C0 — PRIMARY MANAGER RECLASSIFICATION / OWNER PHYSICAL EVIDENCE — 2026-09-30

Primary Manager accepts the C0 artifact as `ACCEPTED_INPUT` with one scope correction: the remaining block is an **agent-observability/access limitation**, not evidence of transport failure or an Echo MVP blocker.

Owner physical observation added:

- One Earn2Trade/Tradovate login in NinjaTrader Desktop exposes **all 5 purchased GAU50 Evaluation accounts** simultaneously.
- Therefore `EVALUATION_ACCOUNT_VISIBLE = PASS (OWNER_OBSERVED)`.
- Therefore `GAU50_VISIBLE = PASS (OWNER_OBSERVED, count=5)`.
- The current topology baseline is `1 NinjaTrader Desktop + 1 Tradovate connection/login + 5 GAU50 Accounts`.
- Execution authorization remains one active account at a time; GUI selection is not accepted as the future Echo authority boundary.

Manager disposition:

- `NINJATRADER_PHYSICAL_TRANSPORT = PASS` for installation/process/network/session establishment.
- `D6_C0_NINJATRADER = PARTIAL_PASS_PENDING_GUI_OBSERVABLES`; C0 is not a product blocker.
- Remaining C0 evidence: NQ realtime market data, account/balance state, Orders/Positions observability, and later reconnect/restart recovery.
- Reconnect/restart do not block starting C1 adapter-fit analysis; they remain mandatory before final physical execution certification.
- ACL access for `echo-dev` is not selected as architecture. C1 must determine the minimum evidence/runtime integration path before any ACL/service-identity change.

**Next Manager action:** dispatch C1 as a TOP source/API fit analysis against the frozen D5 `ExecutionAdapter` and NinjaTrader/NinjaScript reality. No implementation in C1.

### D6 C1 — NinjaTrader/NinjaScript adapter fit analysis — 2026-09-30

Shot TOP source forensics sobre Echo `13e087a3` + reflexión física de `NinjaTrader.Core.dll` 8.1.8.3 (dev-win) + docs oficiales NinjaScript. Artifact: `main/10-projects/Echo Futures/artifacts/d6-ninjatrader-certification-20260930/C1-NINJATRADER-ADAPTER-FIT-ANALYSIS.md`.

- `D6_C1_ADAPTER_FIT = PASS`. `MATERIAL_D5_CONTRADICTIONS = NONE`. ORDERS_SENT = 0; sin cambios de ACL/identidad ni product code.
- Superficie mínima recomendada: **NinjaScript AddOn** (`NinjaTrader.NinjaScript.AddOnBase`, presente en el binario 8.1.8.3) como componente platform-side del adapter; journal M2, guards, readiness y barrier permanecen bridge-side según topología congelada (`DesktopHostedAdapter` = conector + componente desktop).
- Identity: las 5 GAU50 son `Account` objects en `Account.All` con `Id` Int64 estable; selección programática por objeto explícito (GUI selector irrelevante); autoridad de cuenta activa = binding ETCD + verificación bind-time (ya implementado en el bridge D5).
- Market data: realtime PASS (`MarketData.Update` Bid/Ask/Last + identidad FullName→`external_contract_identifier`); histórico PARTIAL (warm-up S1/S2 exacto vía síntesis de corpus 5m desde `BarsRequest` minute; NT = fuente one-shot, corpus pinneado en manifest; ruta de ingestión REBUILD por construir en D6).
- Order lifecycle: MARKET/LIMIT mapean nativo (el dominio congelado D5 sólo emite MARKET/LIMIT — el "protective stop" de GerardMM es un LIMIT en reposo; STOP ni siquiera es constructible); partial fills/event ordering tolerados por el diseño congelado; sin idempotencia nativa de submit en NT ⇒ M2 via journal + reconciliación (diseño ya contempla transports sin native idempotency); identidad nativa candidata `Execution.ExecutionId` (String) + `Order.OrderId` (String) + client identity vía `order.Name`.
- Recovery: observables post-reconnect completos (Orders re-sync, Executions history con `LookbackDays*`, Positions, AccountItem) mapean 1:1 a la barrier congelada; horizon/retention = gates D6.
- Deltas: REUSE total del seam D5; SMALL_D6_ADAPTER_WORK (transport branch, adapter NT bridge-side); D6_RUNTIME_WIRING (AddOn, canal AddOn↔bridge, productor de market stream, publicación del corpus warm-up — D5 no tiene ningún productor real de market data ni ejecución de REBUILD); D6_CERTIFICATION_ONLY (ExecutionId/Name retention, horizon, Account.Id stability, headless, GUI checklist C0, entitlement vigente en preflight).
- Shots propuestos: N1 AddOn read-only (cierra observables C0 vía evidencia del AddOn), N2 ejecución con journal M2, N3 warm-up + S2 demo. C0 queda BLOCKED→absorbible por N1.

**Next Manager action:** integrar handoff C1 y despachar D6-N1; no emitir `EF_D6_E2E_PASS` desde C1.

### D6 C1 — PRIMARY MANAGER QA / REPAIR REQUIRED — 2026-10-01

Primary Manager reviewed the persisted C1 artifact against the frozen Echo baseline and current NinjaTrader order semantics.

Disposition:

- Worker artifact remains evidence, but `D6_C1_ADAPTER_FIT = PASS` is **NOT ACCEPTED**.
- `D6_C1_MANAGER_QA = REPAIR_REQUIRED`.
- The general NinjaTrader AddOn / bridge seam remains plausible and reusable; two material conclusions require repair before implementation authorization.

Accepted C1 findings:

- NinjaScript AddOn is a credible minimal platform-side surface.
- Explicit programmatic Account selection is compatible with the one-active-account policy.
- Realtime market-data and recovery APIs are materially compatible with the frozen seam.
- D6 still requires runtime market ingress, warm-up/rebuild wiring and transport implementation/certification.

Manager findings requiring repair:

1. **Protective-order semantics:** frozen GerardMM currently creates `OrderRoleProtective` as `OrderTypeLimit` at the protective price. For a LONG this is a SELL LIMIT below the live market, and for a SHORT a BUY LIMIT above the live market. On a real venue these are marketable limit orders, not stop-loss orders. Therefore C1's conclusion that STOP support is unnecessary and MARKET/LIMIT map 1:1 to NinjaTrader is not accepted. The D5 simulator does not model price-driven matching and therefore did not prove physical correctness of this order shape.
2. **Transport entitlement gate:** `ProviderAccountBinding.Validate()` forbids `Enabled=true` when `Transport.Entitlement` is `UNKNOWN` or `FORBIDDEN`. The current Earn2Trade automation entitlement remains externally unconfirmed. Owner acceptance of policy risk does not automatically satisfy the frozen D5 binding invariant; this must be explicitly adjudicated before execution egress is enabled.

Implementation status:

- D6-N1 read-only implementation is **NOT YET AUTHORIZED** by this Manager QA; first perform a focused C1 repair so the implementation slice does not encode the wrong protective-order contract or silently bypass the entitlement invariant.
- No D5 code is changed by this QA.

**Next Manager action:** dispatch one focused TOP repair limited to protective-order physical semantics + entitlement/binding authority. It must recommend the minimum correction and identify whether the protective-order issue is a true D5 contract correction or can be solved strictly inside the transport adapter without violating frozen semantics.

### D6 C1-R1 — PRIMARY MANAGER QA / ACCEPTED WITH F2 AMENDMENT — 2026-10-01

> [!warning] SUPERSEDED_BY_OWNER_ORDER (2026-10-01, N1-R1)
> El owner rechazó el modelo `OwnerRiskAcceptance`/`PhysicalEgressApproved` (decisión arquitectónica no autorizada) y ordenó eliminarlo del producto y la configuración: ver sección D6 N1-R1 al final. Las conclusiones de esta sección que dependen del modelo F2 (amendment, `ENTITLEMENT_UNCONFIRMED_OWNER_ACCEPTED`, acceptance read-only) quedan superseded; la historia se preserva. Los ítems F1 (STOP_MARKET) y F2-core (entitlement factual `UNKNOWN`/`FORBIDDEN` fail-closed, jamás override) siguen vigentes.

Primary Manager accepts the focused C1-R1 repair as the technical resolution of the two C1 findings, with one binding-safety amendment before implementation.

Accepted:

- F1 is accepted: the frozen GerardMM protective intent requires a real `STOP_MARKET` primitive. The current protective `LIMIT` is physically incorrect on a real venue because it is marketable on installation. This is a bounded D5 contract correction, not a redesign.
- The NinjaTrader adapter must map the protective order to native/server-held `StopMarket`; PC-simulated/client-side stops are not acceptable for V1 protection.
- F2's core separation is accepted: provider entitlement remains factual (`ALLOWED|CONDITIONAL|FORBIDDEN|UNKNOWN`) and Owner risk acceptance is separate, explicit, auditable local policy. `FORBIDDEN` can never be overridden.

Manager amendment to F2:

- A single undifferentiated `OwnerRiskAccepted` flag is insufficient because the Owner has accepted the uncertainty for certification/read-only work but physical order egress requires a separate explicit authorization boundary.
- `OwnerRiskAcceptance` must carry an explicit physical-egress dimension (e.g. `PhysicalEgressApproved bool`) or equivalent scope.
- Binding load/observation may proceed for `UNKNOWN` with a recorded Owner decision while `PhysicalEgressApproved=false`.
- Admission/new-risk readiness/physical submit must remain fail-closed until either provider entitlement is `ALLOWED|CONDITIONAL` or `UNKNOWN` has a recorded Owner acceptance with `PhysicalEgressApproved=true`.
- `FORBIDDEN` remains fail-closed regardless of Owner risk acceptance.
- Status/readiness must expose `ENTITLEMENT_UNCONFIRMED_OWNER_ACCEPTED`; read-only acceptance must not silently become physical-egress authorization.

Final Manager disposition:

- `D6_C1_R1_MANAGER_QA = ACCEPTED_WITH_AMENDMENT`.
- `D6_C1_FINAL_STATUS = PASS` once the F2 amendment above is treated as implementation authority.
- `D6-N1 = AUTHORIZED` as a read-only implementation shot. It may implement the F2 representation/predicate split required to load the binding and observe the account, but must keep physical egress impossible.
- `D6-N2 = NOT AUTHORIZED` until F1 is implemented/certified and the Owner explicitly approves physical egress for the selected GAU50.

Implementation sequencing:

1. D6-N1 Shot 1: read-only NinjaTrader AddOn vertical + safe entitlement/Owner-risk representation with egress hard-disabled.
2. Fresh independent N1 verification.
3. N1 correction/final gate if findings exist.
4. Only afterward prepare N2 execution implementation.

**Next Manager action:** dispatch D6-N1 Shot 1 under the read-only/no-orders boundary.

### D6 N1-R1 — OWNER-ORDERED REMEDIATION / UNAUTHORIZED OWNER-RISK MODEL REMOVED — 2026-10-01

El owner rechazó explícitamente el modelo `OwnerRiskAcceptance` introducido en C1-R1 F2: fue una decisión arquitectónica no autorizada por el owner y **no forma parte de Echo Futures**. Orden: eliminarlo completamente del producto y la configuración preservando el trabajo válido N1. Ejecutado como remediation quirúrgico N1-R1 (artifact `artifacts/d6-ninjatrader-n1-20261001/N1-R1-REMOVE-UNAUTHORIZED-OWNER-RISK-MODEL.md`):

- Eliminado del código (`feature/d6-n1-readonly-vertical` @ `7af6210a`, FF sobre `36a083a`): `OwnerRiskAcceptance`, `PhysicalEgressApproved`, predicates `AutomationAuthorized`/`PhysicalEgressAuthorized`, degradación permanente `ENTITLEMENT_UNCONFIRMED_OWNER_ACCEPTED`, dimensión readiness `PHYSICAL_EGRESS_NOT_APPROVED`, campo `Status.EntitlementDegradation` y los dos test files F2. Domain (`provider.go`), admission, readiness, session y bridge main quedaron byte-idénticos al baseline congelado D5 (`13e087a3`): `ALLOWED|CONDITIONAL` permitido, `UNKNOWN|FORBIDDEN` fail-closed.
- Preservado N1 válido: canal ntfeed (`echo.ntfeed.v1`), relay, AddOn read-only, publisher JSON crudo, ingress `echo.futures.market-feed-candidates.v1`, observaciones account/positions/orders, defence-in-depth hello↔binding y tests ntfeed intactos.
- ETCD DEV: eliminadas `owner-risk-accepted-{ref,at,egress}` de `/echo/development/futures-bridge/accounts/E2T-GAU50-01/binding/` (read-back doble: writer + MCP RO). `entitlement=UNKNOWN` intacto; no se seteó a `ALLOWED`.
- Relay read-only redesplegado en Daedalus (release `7af6210a`, unidad `echo-nt-feed-relay` activa, `vcs.revision=7af6210a`, `vcs.modified=false`): surface sin attrs owner-risk; binding `E2T-GAU50-01` fail-closed visible (`cannot be enabled with UNKNOWN automation entitlement`); lane de mercado operativa en `:9770`.

> [!warning] SUPERSEDED_BY_OWNER_CORRECTION (2026-10-01, N1-R2)
> La consecuencia bloqueante de esta sección (entitlement `UNKNOWN` pendiente de decisión owner / OD-1) quedó resuelta por la corrección owner en N1-R2: Earn2Trade permite automatización/estrategia propia y el binding `E2T-GAU50-01` quedó con `entitlement=ALLOWED` en ETCD DEV. Ver sección D6 N1-R2 al final. La historia N1-R1 se preserva.

Consecuencia bloqueante declarada, sin resolver: con la semántica D5 restaurada, el binding `E2T-GAU50-01` con `entitlement=UNKNOWN` no es enableable ni carga sesión — requiere decisión del owner (confirmación externa del entitlement Earn2Trade hacia `ALLOWED|CONDITIONAL`); el lane de cuenta del relay queda degradado fail-closed mientras tanto. `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0` (estructural: AddOn sin llamadas de órdenes, protocolo sin familia de comandos, relay sin escritura al AddOn).

**Next Manager action:** comunicar al owner la decisión pendiente del entitlement Earn2Trade (UNKNOWN no enableable bajo D5); no continuar instalación del AddOn ni certificación física en este remediation; no emitir N1 PASS ni D6 PASS.







### D6 N1-R2 — OWNER-ORDERED ENTITLEMENT CORRECTION / EARN2TRADE = ALLOWED — 2026-10-01

El owner corrigió la premisa vigente («Earn2Trade SÍ permite ejecutar automatización/estrategia propia»), resolviendo el OD-1 de N1-R1. Remediation ejecutado (artifact `artifacts/d6-ninjatrader-n1-20261001/N1-R2-CORRECT-EARN2TRADE-ENTITLEMENT.md`), naturaleza `wrong provider-policy state → correct provider-policy state`, cero cambios de código sobre el baseline `7af6210a`:

- Clasificación determinada desde autoridades existentes, sin decisión inventada: **`ALLOWED`**. El criterio canónico del proyecto (Front C authoritative matrix, manager 2026-09-26) reserva `CONDITIONAL` para grants con condiciones explícitas adjuntas (Tradeify/Topstep/TradeDay/MFFU) y clasifica permiso plano con sólo prohibiciones de conducta general como `ALLOWED` (FundedNext/Lucid); la evidencia E2T existente no documenta condición alguna adjunta al grant (copiers≠own-algorithm por separación explícita del research; conducta general en Prohibited Conduct; cláusula «Service» resuelta por la afirmación owner), y la semántica interna exige condición concreta declarada para `CONDITIONAL`. `TransportSpec.Conditions` queda vacío; las reglas generales del programa viven en `GAU50-EVAL` v1.
- ETCD DEV: `/echo/development/futures-bridge/accounts/E2T-GAU50-01/binding/entitlement` `UNKNOWN` → `ALLOWED`, única clave mutada (herramienta efímera SDK con guardas pre/post, borrada del worktree; claves hermanas intactas; read-back doble writer + MCP ETCD RO; prefijo de la cuenta sigue en 10 keys).
- Runtime: `echo-nt-feed-relay` (release `7af6210a` intacta) reiniciado; el error `cannot be enabled with UNKNOWN automation entitlement` desapareció del journal (0 ocurrencias en el PID nuevo) — el binding pasa `ProviderAccountBinding.Validate` (gate de entitlement superado en runtime; tests `internal/binding` + `futures/domain` ok). La lane de cuenta permanece `binding_loaded=false` por la única causa restante, preexistente y declarada en N1-SHOT1 E4: `provider-external-account-id` aún ausente (se fija tras el discovery del AddOn, lado owner, OD-2); el error UNKNOWN la enmascaraba por orden de validación. Lane de mercado stream-level operativa.
- Verificación: referencias `OwnerRiskAcceptance`/`PhysicalEgressApproved` = 0 en el repo; `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0` (estructural; sin usar orden para verificar el entitlement); sin owner-risk model, sin bypass, sin nuevo enum, sin nueva policy layer; AddOn no instalado; execution bridge sin arrancar; N1 sigue read-only.

**Next Manager action:** despachar la re-verificación corta N1 (requiere OD-2: instalación AddOn + restart NT en sesión owner dev-win, que además fija `provider-external-account-id`); N2 sigue NOT AUTHORIZED (F1 STOP_MARKET pendiente + re-affirm owner de egress físico); no emitir N1 PASS ni D6 PASS en este remediation.

### D6 N1-R3 — NINJATRADER 8.1.8.3 PHYSICAL COMPILE REPAIR — 2026-10-01

La instalación física del AddOn por el owner (post N1-R2) falló la compilación NinjaScript con errores reales (CS0246 JObject/JArray/JToken/Formatting, CS0103 Formatting/AccountItemCurrency, CS0117 Globals.Version, entre otros). Remediation ejecutado (artifact `artifacts/d6-ninjatrader-n1-20261001/N1-R3-NINJATRADER-PHYSICAL-COMPILE-REPAIR.md`): reparación exclusiva de compatibilidad física sobre `7af6210a`, único archivo `v3/futures-bridge/addon-ninjatrader/EchoFeedAddOn.cs` (+322/−116, **sin commit hasta evidencia de compilación física**, por mandato):

- Inspección física primero: reflection sobre las 16 assemblies NinjaTrader de `C:\Program Files\NinjaTrader 8\bin` (ProductVersion 8.1.8.3) + docs oficiales NT8 para comportamiento no visible por reflection. Siete defectos corregidos: (1) Newtonsoft.Json no referenciada por el compilador NinjaScript → eliminada, parser JSON mínimo propio para el config y frames como strings, **sin dependencias nuevas**; (2) `AccountItemCurrency` inexistente → `Account.Get(AccountItem, Currency)` (firma física verificada); (3) `Globals.Version` inexistente → `Globals.ProductVersion`; (4) `GetInstrument(string)` 1-arg inexistente en 8.1.8.3 → `GetInstrument(name, false)` (parámetro físico `create=false`); (5) startup bajo `State.Realtime` — estado que **nunca ocurre para AddOns** (Active-state system, docs oficiales) → init en `State.Active`; (6) hello sin `auth_token` en envelope (el relay lo exige; `server.go:170`) y sujeto a carrera contra el auth deadline de 5 s → hello inmediato tras connect con auth_token; (7) dos CS1002 preexistentes (paréntesis sobrantes). Comportamiento N1 preservado: read-only estructural, discovery `Account.All`, resolución Id+Name, snapshots, QUOTE/TRADE, heartbeat, reconnect, `echo.ntfeed.v1`; `grep .Submit(/.Change(/.Cancel(/.Flatten(/.CreateOrder(` = 0.
- Pre-verificación antes del ciclo owner (ambos PASS): shadow-compile `csc.exe` C#5 contra las DLL físicas `NinjaTrader.Core.dll`+`Gui.dll`+`WindowsBase.dll` (0 errores, 0 warnings) y wire-check con los frames exactos del AddOn (harness de reflexión sobre el DLL shadow-compilado) parseados por el contrato Go real `core/ntfeed` (hello autenticado, seq monótona, 8 familias, QUOTE/TRADE → envelopes canónicos `NQ:NQZ6`). Sin código Go cambiado → sin Go tests (regla del mandato).
- **Bloqueo vigente (único):** la compilación NinjaScript real exige replace + restart NT en la sesión interactiva del owner (ACL `dev-win\echo-dev` sobre el perfil KoR re-probeada hoy: lectura y escritura denegadas; NT SI=2). Bundle owner listo: `kor@daedalus:/home/kor/opt/echo-dev/var/nt-feed/owner-install/n1-r3/` (`EchoFeedAddOn.cs` SHA256 `1f34ab1e…` + `OWNER-CHECKLIST-R3.md`, ~2 min, devolver output del compilador). `D6_N1_R3_NINJATRADER_COMPILE = BLOCKED_OWNER_ACTION`; ADDON_INSTANTIATED/CONFIG_LOADED/RELAY_CONNECTED/REAL_HELLO/REAL_HEARTBEAT = NOT_VERIFIED; `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0` (estructural).

**Next Manager action (SUPERSEDED 2026-10-01 por el closeout N1-R3 abajo):** al devolver el owner el output del compilador: 0 errores → shot corto de verificación (hello/heartbeat reales en el journal del relay, reclasificar los NOT_VERIFIED, commit/push del repair con esa evidencia, fijar `provider-external-account-id` + `account_id` según discovery — OD-2); con errores → iterar con inspección física adicional. No emitir N1 PASS ni avanzar N2.

### D6 N1-R3 CLOSEOUT + N1 PHYSICAL READ-ONLY CERTIFICATION — 2026-10-01

El owner ejecutó el ciclo R3: instaló el AddOn reparado, NinjaTrader 8.1.8.3 compiló sin errores visibles y el AddOn cargó y se conectó realmente. Certificación física ejecutada (artifacts `artifacts/d6-ninjatrader-n1-20261001/N1-R3-NINJATRADER-PHYSICAL-COMPILE-REPAIR.md` §6–§8 y `N1-PHYSICAL-READONLY-CERTIFICATION.md`):

- **`D6_N1_R3_NINJATRADER_COMPILE = PASS`** — evidencia física: hello real con `nt_version 8.1.8.3` resuelto en runtime (fix #3), hello autenticado inmediato aceptado (fix #6), init `State.Active` fluyendo (fix #5), `NQ 12-26` suscripto (fix #4), discovery activo (fix #2); hash `C:\Temp\EchoFeedAddOn.cs` = worktree = bundle (`1f34ab1e…`); la carga en vivo prueba la compilación (el pre-R3 no compilaba). Conexión TCP al relay propiedad de `NinjaTrader.exe` PID 984 (post-restart owner, sesión SI=2): `REAL_RELAY_CONNECTION/REAL_HELLO/REAL_HEARTBEAT/ADDON_INSTANTIATED/CONFIG_LOADED` = PASS.
- **Commit diferido ejecutado tras la evidencia:** `f0c82905d4eaf825c08e04f0bb97cab73e616ba5` push FF `7af6210a..f0c82905` a `origin/feature/d6-n1-readonly-vertical` (único archivo EchoFeedAddOn.cs, +322/−116; worktree limpio; master intocado).
- **`D6_N1_PHYSICAL_CERTIFICATION = PARTIAL_BLOCKED_OWNER`** — lado mercado completo en PASS: sesión AddOn real `6e6eb8b665b4422495826c6f9c97e364` continua (~25.7k frames, `malformed=0`, 2 rechazos seq-disciplina = fail-safe OK), TRADOVATE_CONNECTED a nivel TCP (endpoints C0/E9), GAU50_DISCOVERED_COUNT=5 (`RJARA114411201551/571/541/491/521`, ids NT "3"–"7") con `DISCOVERY_ONLY`, NQ_SUBSCRIPTION/BID/ASK/LAST PASS, QUOTE y TRADE verificados en los tres planos (AddOn → relay → registros físicos en `echo.futures.market-feed-candidates.v1` con `log_identity=ninjatrader-addon/<sesión>`).
- **Bloqueo único (OWNER_DECISION_REQUIRED, OD-2):** no existe autoridad preexistente que mapee una GAU50 descubierta a `E2T-GAU50-01` (`provider-external-account-id` nunca existió en ETCD; relay fail-closed `binding_loaded=false`, lane de mercado stream-level operativa). ACCOUNT_BINDING=BLOCKED_OWNER_DECISION; ACCOUNT_STATE/POSITIONS/ORDERS/EXECUTIONS=NOT_APPLICABLE bajo discovery-only (diseño: sólo con cuenta resuelta). Caveat para la decisión: estabilidad de los `Account.Id` internos de NT entre restarts no demostrada (el número Tradovate viaja en el Name).
- **Hallazgos no bloqueantes:** (1) market data demo con delay exacto ~600 s (`event_ts` vs llegada; reloj dev-win verificado correcto; AddOn propaga `e.Time` fielmente) — input N2: el feed demo no sirve para decisiones de estrategia, producción exige entitlement real-time; (2) el scan del AddOn sólo vio la conexión CBI "Simulación" mientras el transporte Tradovate está vivo a nivel TCP (mapeo no verificable desde el boundary del agente); (3) `reconnects:1` del heartbeat = connect inicial (una sola sesión TCP).
- `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0` (estructural + `order_events: 0` observado en toda la sesión); sin orden generada para fabricar evidencia.

**Next Manager action:** comunicar OD-2 al owner (seleccionar una GAU50 descubierta como `E2T-GAU50-01`, considerando el caveat de Ids); tras la selección: fijar `provider-external-account-id` en ETCD + `account_id` en el config del AddOn con la misma identidad, reload mínimo, shot corto (binding_loaded=true + match RESOLVED + observaciones de cuenta) → recién entonces `D6_N1 = PASS` completo. N2 sigue NOT AUTHORIZED (F1 STOP_MARKET + re-affirm owner de egress físico). No emitir `EF_D6_E2E_PASS`.

### D6 N1 FINAL ACCOUNT BINDING — OWNER OD-2 EJECUTADO ECHO-SIDE / CICLO OWNER STAGEADO — 2026-10-01

El owner resolvió OD-2: `E2T-GAU50-01` → `Name = RJARA114411201551` (autoridad final para N1). Certificación ejecutada sobre `f0c82905` (worktree limpio antes y después, cero commits) — artifact `artifacts/d6-ninjatrader-n1-20261001/N1-FINAL-ACCOUNT-BINDING-CERTIFICATION.md`:

- **Rediscovery vivo (no asumido):** sesión AddOn real `6e6eb8b6…` continua (PID 984 SI=2, TCP a :9770 ESTABLISHED); frame account full-fidelity 20:39:48Z seq 81992: `RJARA114411201551` con match count = 1, **current `Account.Id` = `"3"`** confirmado por la sesión actual.
- **Binding ETCD DEV fijado:** `provider-external-account-id = "3"` (patrón efímero N1-R2 con guardas + read-back doble writer/MCP RO; prefijo 10→11 keys, `entitlement=ALLOWED` y hermanas intactos). **Relay reiniciado (20:43Z, release `7af6210a` intacta): `echo.ntfeed.binding_loaded=true`, `binding_error=""`** — fin del fail-closed `provider-external-account-id is empty`.
- **`ACCOUNT_MATCH = MISMATCH` fail-closed correcto:** el AddOn reconectó (primera demostración física de reconnect contra relay real) y su hello sigue `expected_account=""` (config discovery-only) ⇒ defence-in-depth rechaza — jamás resolución parcial. Lane de mercado regresada OK: published creciente 0 errores, QUOTE (`BBO 30774.5/30775`) y TRADE (`30775.5×1`) reales en el ingress 20:48Z, heartbeats `order_events=0`.
- **`D6_N1_FINAL_ACCOUNT_BINDING = BLOCKED_OWNER_ACTION`** — único paso restante: escribir el config del AddOn + restart NT (perfil owner, ACL denegada re-probeada 20:36Z). **Stageado byte-verificado:** `owner-install/n1-final/echo-feed-addon.json` (sólo cambian `account_id:"3"` y `account_name:"RJARA114411201551"`; SHA `cc7bf7fa…313cf`; token verificado EQUAL contra ETCD sin imprimirlo) + `OWNER-CHECKLIST-N1-FINAL.md`, ambos en `C:\Temp` con hash idéntico. Tras el ciclo owner el reconnect ya demostrado entrega `binding_match=RESOLVED` + observaciones de cuenta automáticamente (sin acción Echo-side); un shot corto clasifica los NOT_OBSERVABLE → `D6_N1 = PASS`.
- **DESIGN INPUT registrado (no resuelto):** `Account.Id` NT = entero runtime-local, estabilidad entre restarts no demostrada; diseño actual falla SEGURO ante drift (cross-check `Name` ⇒ MISMATCH, nunca cuenta equivocada) pero exige re-discovery+re-config; referencia business durable hoy = `Name`. Para el D6 Design Freeze (Primary Manager).
- `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0` (estructural: grep mutantes = 0 @ f0c82905, 8 familias sin comandos, relay sin escritura al AddOn, execution bridge sin arrancar + `order_events: 0` toda la sesión). Master y PROD intocados. N2 sigue NOT AUTHORIZED.

**Next Manager action:** comunicar al owner el checklist n1-final (copiar `C:\Temp\echo-feed-addon.json` → `Documents\NinjaTrader 8\echo\` + restart NT, ~2 min); tras el restart, disparar el shot corto de re-verificación N1 (RESOLVED + observaciones de cuenta + smoke) → `D6_N1 = PASS`. N2 sigue NOT AUTHORIZED (F1 STOP_MARKET + re-affirm owner de egress). No emitir `EF_D6_E2E_PASS`.

### D6 N1 FINAL ACCOUNT BINDING — CICLO OWNER EJECUTADO / D6_N1 = PASS — 2026-10-01

El owner ejecutó el ciclo stageado (instaló el config final `echo-feed-addon.json` con `account_id:"3"` + `account_name:"RJARA114411201551"` y reinició NinjaTrader Desktop). Shot corto de verificación física ejecutado sobre `f0c82905` (worktree limpio antes y después, cero commits, cero mutaciones Echo-side: sin ETCD, sin restarts) — artifact `artifacts/d6-ninjatrader-n1-20261001/N1-FINAL-ACCOUNT-BINDING-CERTIFICATION.md` §9–§15:

- **`D6_N1 = PASS`** — sesión AddOn nueva `2f6a4d5375714a13b237f5ab65ba1fd6` (hello autenticado 21:16:11Z; NinjaTrader.exe **PID 1876** ≠ 984, TCP `:49166 → daedalus:9770` propiedad del PID verificado por netstat; `nt_version 8.1.8.3`). Tradovate viva (demo.tradovateapi.com ×2 + MD gateway :31655; frames session "Simulación" Connected). Rediscovery post-restart: `RJARA114411201551` match count = 1 de 8, **`Account.Id` = `"3"` — estable entre restarts (2/2 sesiones hoy, acotado; input de diseño vigente)**. ETCD `provider-external-account-id = "3"` re-verificado RO. **`binding_loaded=true`, `binding_error=""`, `binding_match=RESOLVED`** (journal relay release `7af6210a` intacta; la única línea MISMATCH previa era el fail-closed correcto del hello discovery-only de la sesión vieja).
- **Observaciones de cuenta con cuenta resuelta:** `ACCOUNT_STATE=PASS` (resolved {id "3", name RJARA114411201551}, match RESOLVED en todos los frames), `BALANCES=PASS` (NLV 50000 / cash 50000 / unrealized 0 / realized 0 / buying_power 0 — lo que expone la conexión demo; progresión real 0/0→valores observada), `POSITIONS=PASS|EMPTY_OBSERVED`, `ORDERS=PASS|EMPTY_OBSERVED`, `EXECUTIONS=NOT_OBSERVED` (0 ejecuciones nuevas post-priming; sin frames executions; `order_events==account_events` en todos los heartbeats — semántica verificada en código: contador de *observaciones*, no de creación de órdenes).
- **Market lane PASS:** `market_ok=525` procesados con `anomalies=[]`, `published=19707`, `publish_errors=0`, `malformed=0`; QUOTE (BBO `30770.25/30771.25`) y TRADE (`30770.25×1`) físicos en `echo.futures.market-feed-candidates.v1` p4 102123+ con `log_identity=ninjatrader-addon/2f6a4d53…` y envelope congelado intacto. Delay ~600 s del feed demo persiste (hallazgo previo vigente, no bloquea). OTEL dev :4317 caído (ambiental, preexistente).
- **Safety:** grep `Submit/Change/Cancel/Flatten/CreateOrder` = 0 re-ejecutado @ `f0c82905`; `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`. Master y PROD intocados. **N2 sigue NOT AUTHORIZED** (F1 STOP_MARKET implementado/certificado + re-affirm explícita del owner de egress físico). No se emite `EF_D6_E2E_PASS`.

**Next Manager action:** planificar D6-N2 bajo sus dos gates previos; llevar al D6 Design Freeze el input de identidad de cuenta (Name = referencia business durable; `Account.Id` NT estable en 2/2 sesiones hoy pero runtime-local sin garantía general; cross-check Name actual falla SEGURO ante drift con costo de re-discovery+re-config). Decisión de representación durable de Account = Primary Manager, no resuelta en N1.

### D6 — FINAL DESIGN FREEZE — TOP DESIGN CONSOLIDATION — 2026-10-01

Consolidación de diseño D6 posterior a `D6_N1 = PASS`, previa a los tres implementation shots. Artifact: `artifacts/d6-design-freeze-20261001/ECHO-FUTURES-D6-FINAL-DESIGN-FREEZE.md`.

- **`D6_DESIGN_FREEZE = READY_FOR_MANAGER_REVIEW`** — contratos D4/D5 verificados contra source @ `f0c82905` (adapter/journal/readiness/provider/operation) y contra las certificaciones físicas N1/C0/C1/C1-R1; única corrección D5 incorporada = F1 STOP_MARKET (aceptada Manager en C1-R1, aún NO implementada).
- **Identidad de cuenta (decisión delegada al manager, resuelta aquí):** modelo de 3 capas — `E2T-GAU50-01` (Echo durable) / `provider-account-ref` = NT `Name RJARA114411201551` (referencia business durable, autoridad de binding, única en discovery 1/8) / NT `Account.Id` (hint de plataforma con cross-check; drift = refresh de config, jamás cambio de identidad ni cuenta equivocada). Migración aditiva: 1 clave ETCD nueva + inversión de resolución del AddOn (hoy Id-primario).
- **Realtime:** mismo path NinjaTrader/Tradovate es la autoridad realtime (el delay ~600 s es del feed demo "Simulación"); dimensión FRESH|STALE|UNKNOWN sobre la serving authority (event_ts age vs DomainClock + liveness acotado por calendario, bounds = config) consume analytical readiness + admission ⇒ feed stale no puede habilitar riesgo; gate físico G-REALTIME (feed live de la cuenta, no demo) antes de Strategy→execution. Regla de afinidad: el market data de ejecución proviene de la conexión que hospeda la cuenta.
- **Protective stop:** STOP_MARKET nativo venue-held (C1-R1 F1 como autoridad de implementación; synthetic/client-side prohibido; transformación en adapter prohibida); capability gate `IsOrderTypeSupported` + prueba física post-restart antes de declarar STOP_MARKET en el adapter NT.
- **Transporte:** AddOn dual-canal — feed lane N1 intacta (kill-switch estructural preservado) + execution lane `echo.ntx.v1` terminada en el futures-bridge (framing ntfeed reutilizado + familias command/command_result); M2 journal 100% bridge-side; cliente `order.Name`, identidad nativa `Order.OrderId`/`Execution.ExecutionId`; sin idempotencia nativa del venue ⇒ clase frozen "idempotencia via journal+reconciliación".
- **GAU50-EVAL v1:** max 6 contratos (cap), trade until 15:50 CT (ventana Evaluation), DD EOD 2000 / DLL 1100 como contexto económico owner-config; consistency 30% documentada con SourceRefs, jamás codificada como cap falso.
- **Shots:** Shot 1 implementación (F1 + identidad + lane + adapter + freshness + RuleSet + warm-up/REBUILD producer + fixes N1-carried; egress estructuralmente deshabilitado, 0 órdenes) → Shot 2 adversarial review independiente → Shot 3 remediation + certificación física escalonada (G-REALTIME → G-STOP → G-ID-Retention → G-HORIZON → G-E2E ciclo controlado + drill restart → G-PERF).
- **Owner register:** OD-D6-1 egress físico (control-plane, inmediatamente antes del ladder físico; NO producto — modelo OwnerRiskAccepted permanece eliminado por orden owner N1-R1); OD-D6-2 ratificación de valores GAU50-EVAL v1; OD-D6-3 escalación condicional si el feed live sale stale; OD-D6-4 ciclos owner-assisted AddOn/NT (standing).

**Next Manager action:** revisar/aceptar el freeze; tras aceptación, despachar D6 Shot 1 (implementation). N2 físico sigue NOT AUTHORIZED hasta OD-D6-1. No emitir `EF_D6_E2E_PASS`.

### D6 Shot 1 — IMPLEMENTATION (egress estructuralmente deshabilitado) — READY_FOR_ADVERSARIAL_REVIEW — 2026-10-01

Implementación del delta D6 completo sobre el baseline certificado `f0c82905` (`D6_N1 = PASS`), branch **`origin/feature/d6-shot1-execution-vertical` @ `4b05d6f856df41b748ad2bfb1f0806b45349387f`** (15 commits FF, push verificado). Artifact: `artifacts/d6-shot1-20261001/D6-SHOT1-IMPLEMENTATION.md`.

- **`D6_SHOT1_IMPLEMENTATION = READY_FOR_ADVERSARIAL_REVIEW`** — S1 identidad durable (ref provider Name-primaria con `Validate()` fail-closed, drift de `Account.Id` = `PROVIDER_ACCOUNT_ID_DRIFT` fail-closed; verificación runtime física: relay nuevo `binding_match=RESOLVED`, `binding_id_drift=false` con la sesión AddOn real); S2 STOP_MARKET stack completo (F1: domain→engine→wire→envelope→journal/sameIntent→GerardMM→sim; protective resting `STOP_MARKET` con `StopPrice`, tighten monotónico, crossed→MARKET intacto); S3/S4 lane `echo.ntx.v1` + adapter `NINJATRADER_BRIDGE` sobre el seam congelado (superficie física 8.1.8.3 refleccionada ANTES de codificar: `CreateOrder` sin OrderEntry, `Submit/Cancel/Change(IEnumerable<Order>)`, TIF enum; sin transformación de tipos); S5/S6 M2 congelado (PREPARED→SUBMITTING fsync antes de la escritura del lane; VENUE_BOUND sólo con evidencia venue; REJECTED=negación autoritativa; timeout/ERROR=AMBIGUOUS; jamás re-submit ciego — test exactamente-1-comando; reconciliación sobre vistas venue: ausencia→AMBIGUOUS fail-closed, UnknownLiveOrders quarantine nunca cancelada/adoptada); S7 freshness FRESH/STALE/UNKNOWN fail-closed sobre `echo/market_stream` (UNKNOWN bloquea; lag 600 s ⇒ STALE ⇒ 0 señales + `DENY_MARKET_NOT_FRESH`; replay conserva semántica D5); S8 `GAU50-EVAL v1` ACTIVE con 3 SourceRefs (cap GROSS 6 + ventana 15:50 CT por los paths frozen; DD/DLL/consistencia documentados NO codificados; guard anti-drift); S9 warm-up/REBUILD (síntesis 5m-exact determinista, anchor sellado refs+digest, fidelidad E2E byte-idéntica); S10 raw-JSON publisher de execution-events.
- **Compile físico:** AMBOS AddOns shadow-compilados contra las DLL instaladas de NT 8.1.8.3 en dev-win (0 errores; hashes byte-verify; advertencias del AddOn de ejecución registradas). `EchoExecutionAddOn.cs` (camino de comandos) queda **stageado como candidato Shot 3, NO instalado**; el feed AddOn mantiene su grep-gate negativo = 0.
- **Despliegue DEV:** relay del vertical repuesto a release `170a4581` (SHA256 `3cacb2e7…`, rollback documentado) con reconexión física verificada; ETCD `binding/provider-account-ref = "RJARA114411201551"` escrita con read-back doble (herramienta efímera eliminada). **G-EGRESS-0:** lista de sesiones del bridge vacía (default), bridge sin correr, capability gate CLOSED (`SubmissionCapabilitiesReady=false` testeado; STOP_MARKET rechazado pre-journal). `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`.
- **Tests:** suites scoped `-race` 100% verdes (sdk/futures, futures-bridge, core functions+futuresruntime+futuresvertical+config/futures). Cobertura paquete: `core/ntx` 87.3%, `ninjatrader` 78.3%, `binding` 100%, `warmup` 97.5%; lógica nueva ≈100% a nivel función (ramas de lane-caída/deadline declaradas para Shot 3). Deuda preexistente sin tocar: `futures-projector/adapters/kafka` race (presente en el baseline limpio).
- **Owner:** `OWNER_DECISION_REQUIRED = NONE` para este shot; OD-D6-1 (egress físico) y OD-D6-2 (ratificación valores GAU50-EVAL) siguen REQUIRED para Shot 3. Master y PROD intocados.

**Next Manager action:** despachar D6 Shot 2 (adversarial review independiente sobre `4b05d6f8`, sin cambios de código durante el review). No emitir `EF_D6_E2E_PASS`.

### D6 Shot 1 — MANAGER QA REMEDIATION (F-MGR-01/02/03) — PASS — 2026-10-02

`D6_SHOT1_MANAGER_QA = REPAIR_REQUIRED` cerrado de forma acotada. Branch `origin/feature/d6-shot1-execution-vertical` @ **`14b0d72b811ef618190130f70e9fa748dfb90088`** (push FF sobre `4b05d6f8`; 2 commits). Artifact: `artifacts/d6-shot1-20261001/D6-SHOT1-MANAGER-QA-REMEDIATION.md` + sección de remediación añadida a `D6-SHOT1-IMPLEMENTATION.md`.

- **F-MGR-01 PASS:** cobertura reproducible del código añadido por el shot (git-diff hunk slicing ∩ coverprofiles scoped): raw 1154/1228 = 94.0% → con exclusiones documentadas (cmd mains DI-wired deployment-verified, ramas canonical-decimal inalcanzables, ventanas mid-flight de lane write con semántica cubierta por seam, always-nil por contrato, marshal por-contrato) **1154/1173 = 98.4% ≥ 95%**. Batería nueva de tests de fallo (journal scripteado, lane silencioso, sinks, reconciliación found/history, server ntx, engine STOP_MARKET, Compose bounds, wiring main, GAU50 guards).
- **F-MGR-02 PASS:** DD 2000 (EOD_TRAILING) + DLL 1100 (ABSOLUTE) codificados en GAU50-EVAL v1 como **safety-inputs de estado de cuenta** (deny `RISK_STATE_TRIGGERED` + ForceClose; testeados por breach; nunca caps por orden), con 4ª SourceRef y guard anti-drift extendido (14 mutaciones). **CONSISTENCY_30 queda documentation-only por contrato** (pass-time monitored outcome; sin punto de evaluación pre-egress en las typed families congeladas) — contradicción arquitectónica devuelta al Primary Manager.
- **F-MGR-03 REMOVED:** OD-D6-2 (ratificación owner de valores) eliminada del registro vigente, proyecto y artefacto — la evidencia ya es autoritativa y no contested. Gates owner restantes: **OD-D6-1 only** (egress físico, control-plane); OD-D6-3 condicional y OD-D6-4 standing siguen operativos sin ser gates de ratificación.
- Regresión: los 10 gates del Shot 1 permanecen PASS (suites `-race` verdes). `PHYSICAL_EGRESS = DISABLED`; `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`. Master y PROD intocados.

**Estado:** `D6_SHOT1_MANAGER_REMEDIATION = PASS`; `D6_SHOT1_IMPLEMENTATION = READY_FOR_ADVERSARIAL_REVIEW` @ `14b0d72b`. **Next Manager action:** dispatch D6 Shot 2 (adversarial review), adjudicando CONSISTENCY_30 como input del review. No emitir `EF_D6_E2E_PASS`.

### D6 Shot 1 — F-MGR-02B: CONSISTENCY_30 en el engine — PASS — 2026-10-02

Observación restante del Manager cerrada. Final SHA **`0e9741a56afe6911e52480fb9f2fe86a47aae427`** (push FF sobre `14b0d72b`).

- **Familia tipada `ConsistencyRule`** (aditiva, domain): `{MAX_DAY_SHARE, 30, TOTAL_PNL_AT_PASS, monitoring}` — la consistency como el outcome monitorizado que es; Validate fail-closed en la semántica V1 (no-monitoring jamás valida: no existe punto de enforcement por orden).
- **Monitor en `provider_rules`:** inputs aditivos en `AccountSnapshot` (total/best-day PnL; nil = estado ausente, el monitor no corre ni fabrica outcome); evaluador exacto sin división (`breached ⟺ best_day×100 ≥ 30×total`); outcome expuesto como telemetría `echo.futures.provider.consistency_monitor` (`COMPLIANT | BREACHED | UNDETERMINED` con total ≤ 0). **Nunca gatea una orden** (testeado: BREACHED ⇒ admission ALLOW).
- **Materialization:** `gau50-eval-v1.json` += `consistency` + 5ª SourceRef; guard exige la familia exacta (removal/non-monitoring/percent = drift). `DOCUMENTATION_ONLY_PROVIDER_RULES = NONE`.
- Cobertura raw 94.1% / ≈98.7% ajustada (exclusiones F-MGR-01 + panic-branch por contrato de `CanonicalStringUnchecked`). Suites `-race` verdes. `PHYSICAL_EGRESS = DISABLED`; 0 órdenes.

**Estado:** `D6_SHOT1_IMPLEMENTATION = READY_FOR_ADVERSARIAL_REVIEW` @ `0e9741a5`. **Next Manager action:** dispatch D6 Shot 2 (adversarial review sobre `0e9741a5`). No emitir `EF_D6_E2E_PASS`.

### D6 Shot 2 — FINAL ADVERSARIAL IMPLEMENTATION REVIEW — REMEDIATION_REQUIRED — 2026-10-02

Review adversarial independiente (fresh context, one-shot, read-only) sobre el candidato Shot 1. Artefacto: **`artifacts/d6-shot2-20261002/D6-SHOT2-ADVERSARIAL-REVIEW.md`**.

- **`D6_SHOT2_ADVERSARIAL = REMEDIATION_REQUIRED`** — 0 BLOCKER · **2 HIGH** · 8 MEDIUM. Candidato verificado: `0e9741a56afe6911e52480fb9f2fe86a47aae427` (FF puro sobre `f0c82905`, worktree limpio).
- **PASS estructural en los frentes críticos:** wrong-account (Name-primary 4 superficies, drift fail-closed), double-submit (dedup pre-side-effect + at-most-once por journal; ningún ordering legal produce doble submit físico), M1/M2 (PREPARED/SUBMITTING fsync antes del lane write; VENUE_BOUND sólo con evidencia venue), STOP_MARKET (pila completa, tighten monotónico, gate pre-journal), cancel/replace/late-fill, reconciliación (VENUE_BOUND desaparecido ⇒ AMBIGUOUS fail-closed), GAU50 rules (boundary ==30% ⇒ BREACHED **CORRECTO** vs fuente "30% or more"; monitoring-only verificado), warm-up determinismo, EXACT_REPLAY, AddOn authority, NTX protocolo, NT 8.1.8.3 compat estática, **PHYSICAL_EGRESS = STRUCTURALLY_DISABLED** (4 barreras: capability gate / sin proceso / clave `futures-bridge/accounts` ABSENT en ETCD / AddOn ejecución staged no instalado), coverage claim **reproducido** (raw 94.0%, ajustado 98.4% ≥ 95%).
- **HIGH F-S2-01:** AddOn ejecución (staged) resetea `execSeq=0` en reconnect con `session_id` persistente ⇒ tracker del bridge rechaza todo frame posterior ⇒ lane funcionalmente muerto tras el primer reconnect (fail-closed, pero rompe el escenario §11 "AddOn reconnect"); remediación C#+contrato de test antes de instalar el AddOn.
- **HIGH F-S2-02:** freshness input-driven + liveness desactivado ⇒ feed muerto-silencioso queda **FRESH congelado para siempre** (el age-bound sólo se evalúa con arrivals; comentario del código overclaima) ⇒ new risk habilitable en la ventana señal-en-vuelo→admit con transporte muerto; cablear liveness o re-evaluación por tiempo antes de G-REALTIME.
- **MEDIUM F-S2-03..10:** sin clamp de `event_ts` futuro / sin fencing de sesión ntx / **binding ETCD real `day-boundary-tz=America/New_York` reset 17:00 ⇒ 16:00 CT, desalineado 1h del ciclo DLL/DD 5pm CT** (latente: plane externo sin productor) / EVIDENCE_GAP basis `INITIAL_BALANCE` del DLL + cita verbatim consistency / warm-up gate cuenta presencia no densidad / BACKTEST hereda freshness sin test de invarianza (hoy inerte) / binario ELF 33.4MB commiteado en `14b0d72b` / grep-gate G-EGRESS-0 sin automatizar.
- Suites `-race`: `v3/futures-bridge/...` 13 pkgs ok reproducido en el review; sdk/core idem (vía reproducción de cobertura + corrida del review). `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0` durante el review; ETCD/deployment/configs intocados.
- **OWNER_DECISION_REQUIRED: NONE.** OD-D6-1 permanece gate de Shot 3 (no solicitado).

**Estado:** `D6_SHOT2_ADVERSARIAL = REMEDIATION_REQUIRED` @ candidato `0e9741a5`. **Next Manager action:** adjudicar F-S2-01..10 y autorizar la remediación de Shot 3 ANTES de cualquier cambio de código; después el ladder físico congelado (OD-D6-1 → G-REALTIME → G-STOP → G-ID-Retention → G-HORIZON → G-E2E con drill de reconnect → G-PERF). No emitir `EF_D6_E2E_PASS`.

### D6 Shot 3 — PRE-EGRESS REMEDIATION (F-S2-01..10) — PASS — 2026-10-02

Remediación top senior one-shot de los 10 findings adjudicados del Shot 2, sin ladder físico. Artefacto: **`artifacts/d6-shot3-20261002/D6-SHOT3-PRE-EGRESS-REMEDIATION.md`**.

- **`D6_SHOT3_REMEDIATION = READY_FOR_OWNER_PHYSICAL_EGRESS_GATE`** — 10/10 findings PASS, 0 residuales. Baseline `0e9741a5` → **FINAL_SHA `40102ea5a44be9a618ac12529e6f0e9fdfd46d34`** (10 commits FF, `origin == HEAD`).
- **F-S2-01/F-S2-04 (HIGH+MED transporte):** reconnect del AddOn de ejecución = NUEVA sesión por conexión con seq en 0 (coherente con el fencing); el server cierra la conexión supersedada al autenticar una nueva y el adapter rechaza frames de sesión no-activa como evidencia contada — contrato congelado por tests adversariales en ambas capas; shadow-compile físico 0 errores.
- **F-S2-02/F-S2-03/F-S2-08 (freshness):** dimensión LIVE-only explícita (`SetRunMode` desde el runtime); timer checkpointed de re-evaluación por silencio (periodo = mitad del bound) — un feed muerto decae a STALE ≤ bound+periodo SIN eventos y sin consumir owner input; `future_event_skew` (5s default) cuenta el veneno sin clamp; frontier re-ancla en source switch y barrier con invalidación; BACKTEST/EXACT_REPLAY sirven el sentinel `""` D5 y jamás arman timers — invarianza con salto de reloj testeada.
- **F-S2-05:** ETCD DEV `day-boundary-tz = America/Chicago` con read-back doble (writer + MCP RO; hermanas intactas); loader default Chicago + `LoadLocation` fail-closed; DST 2026 testeado (22:00/23:00 UTC CDT/CST).
- **F-S2-06:** bounded evidence repair first-party (2 artículos oficiales): verbatim DLL "taken from the balance you start the day with" ⇒ **basis corregido `INITIAL_BALANCE → PREV_DAY_CLOSE`** (config-act con provenance: la fuente CONTRADIJO la implementación); verbatim consistency "30% or more" CONFIRMA el boundary `>=` del engine sin cambio semántico; 7 SourceRefs; guard 16 mutaciones.
- **F-S2-07:** gate de densidad `Min5mPerH4Region` (default congelado 8): presencia ≠ completitud — corpus 1-bucket/región ⇒ `WARMUP_INCOMPLETE` por Validate y por plan; huecos interiores siguen siendo diagnóstico; corpora de fidelidad S09 declaran su densidad explícita.
- **F-S2-09/F-S2-10:** ELF 33.4MB des-trackeado + `.gitignore` (sin rewrite); G-EGRESS-0 automatizado (4 tests failing-closed: feed AddOn sin llamadas mutantes tras stripping de comentarios, sin familias command, schema ntfeed congelado, auto-chequeo del detector contra el AddOn de ejecución).
- **Regresión:** suites `go test -race -count=1` verdes (bridge 15 pkgs, sdk, core completo con vertical `-timeout 30m`). Hallazgo de la regresión: el decay F-S2-02 marcó STALE un stream con 60s sin hechos y MM denegó correctamente el new risk del rollover MKT07 (fail-closed congelado §4.2, verificado por bisect); el escenario del test ajustado para modelar feed vivo, sin tocar producto. coberturas adversariales aceptadas re-ejecutadas (wrong account, double submit, M1/M2, STOP_MARKET, cancel/replace/late-fill, reconciliation, identidad, provider rules, warm-up, EXACT_REPLAY/BACKTEST, freshness, session fencing). **Coverage changed-logic (BASE `0e9741a5`, script aceptado): raw 135/137 = 98.5% ≥ 95% sin exclusiones** (2 statements canónicos documentados).
- **NT 8.1.8.3:** shadow-compile físico de AMBOS AddOns — `FEED_EXIT=0` (byte-idéntico a Shot 1) y `EXEC_EXIT=0` (SHA `b2a29a36…`, 3 warnings preexistentes registrados); ejecución STAGED, no instalada.
- **PHYSICAL_EGRESS = DISABLED** — 4 barreras intactas; única mutación ETCD DEV: `binding/day-boundary-tz`; `futures-bridge/accounts` sigue ABSENT; `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`. Master y PROD intocados.
- **OWNER_DECISION_REQUIRED:** NONE para esta remediación; **OD-D6-1 permanece REQUIRED inmediatamente antes del primer gate físico** (no solicitado aquí).

**Estado:** `D6_SHOT3_REMEDIATION = READY_FOR_OWNER_PHYSICAL_EGRESS_GATE` @ `40102ea5`. **Next Manager action:** pedir al Owner la autorización explícita OD-D6-1 antes de la primera orden física; después ejecutar el ladder físico congelado en orden (G-REALTIME → G-STOP → G-ID-Retention → G-HORIZON → G-E2E con drill de reconnect → G-PERF). No ejecutar órdenes físicas. No comenzar el ladder. No emitir `EF_D6_E2E_PASS`.

### D6 — FINAL PHYSICAL CERTIFICATION — INTENTO 1: BLOQUEADO POR CALENDARIO DE MERCADO — 2026-10-03

Shot TOP Senior Physical Certification Lead con **OD-D6-1 = AUTHORIZED** (owner, en el despacho: primer egress físico y órdenes necesarias exclusivamente para el ladder D6 sobre `E2T-GAU50-01` / `RJARA114411201551`). Artifact: **`artifacts/d6-final-physical-certification-20261003/D6-FINAL-PHYSICAL-CERTIFICATION.md`** (+ `evidence/g-realtime-evidence.txt`).

- **`D6_FINAL_PHYSICAL_CERTIFICATION = NOT_READY` — `EF_D6_E2E_PASS = NOT_READY`.** Cero commits (BASELINE = FINAL = `40102ea5a44b…`), cero mutaciones ETCD/deploy/config, `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = FILLS = 0`, los cinco contadores duros en 0 (`WRONG_ACCOUNT_EVENTS`, `DUPLICATE_PHYSICAL_SUBMITS`, `BLIND_RETRIES`, `UNRESOLVED_AMBIGUOUS_SUBMITS`, `PROVIDER_RULE_VIOLATIONS`).
- **Preflight P1–P7 = 7/7 PASS:** HEAD `40102ea5` worktree limpio `origin == HEAD`; rediscovery vivo 1 match `RJARA114411201551` de 8, `Account.Id "3"` sin drift vs ETCD; GAU50-EVAL v1 ACTIVE 7 SourceRefs sin drift; `entitlement=ALLOWED`; `day-boundary-tz=America/Chicago` + reset 17:00; egress estructuralmente ausente (0 procesos bridge, sin key de sesiones, `EchoExecutionAddOn` staged byte-idéntico a HEAD en `C:\Users\TEMP` y **NT sin reiniciar desde 2026-10-01 (PID 1876 continuo)** ⇒ no puede estar cargado; perfil owner ACL denegada re-probeada); cuenta clean (`positions []`, `orders []`, balances 0/0/0 — variante demo de fin de semana, documentada).
- **`G_REALTIME = FAIL` (causa ambiental, no defecto):** sábado 2026-10-03 07:25 CDT — sesión CME cerrada desde vie 16:00 CT. Ventana acotada 12:26:35Z→12:33:49Z sobre el path físico real: AddOn vivo (seq 5431845→5432020, heartbeats ~10 s, TCP ESTABLISHED PID 1876→daedalus:9770) pero **cero eventos de mercado** (contador `market_events` sin cambio 5,375,579; end-offset Kafka p4 sin movimiento 5476458). Último evento `NQ:NQZ6`: QUOTE `event_ts 2026-10-02T21:38:25.95Z` (vie 16:38 CDT) ⇒ `event_ts_age` ≈ 10.8 h >> bound 30 s ⇒ **STALE fail-closed** (decay F-S2-02) ⇒ readiness no READY, admission refusa new risk. El modelo frozen funcionó exactamente como diseñado sobre datos físicos reales; no hay repair posible (calendario del venue).
- **G-STOP / G-ID-Retention / G-HORIZON / G-E2E / G-PERF = NOT_RUN** (STOP por G-REALTIME FAIL según `/failure_policy` y `/provider_safety`; además sábado sin ventana de new-risk GAU50-EVAL days 1–5 ⇒ doble fail-closed de calendario; sin parámetros frozen standalone de G-STOP — el gate vive dentro del ciclo E2E congelado). RECONNECT_DRILL = NOT_RUN. RECONCILIATION = PASS (estado clean trivial: journal sin non-terminal, venue plano, 0 unknown live orders).
- **Regresión @ `40102ea5` hoy:** `go test -race -count=1` — bridge **15 pkgs ok**, sdk **14 pkgs ok**, core functions/futuresruntime/config/futures ok + futuresvertical `-timeout 30m` ok. NINJATRADER_8_1_8_3 = PASS vigente de Shot 3 (source byte-idéntico verificado hoy; sin re-compilación).
- **`OWNER_DECISION_REQUIRED = NONE`** — no se solicitó ningún parámetro económico/material; el bloqueo es el calendario del venue. OD-D6-1 queda **vigente sin consumir** para el re-intento.

**Next Manager action:** re-despachar el ladder físico congelado en la primera sesión abierta — **lunes 2026-10-05** (feed FRESH posible desde dom 17:00 CT; la ventana de new-risk GAU50-EVAL abre L-V ⇒ primera ventana plena lunes 00:00–15:50 CT), ejecutando DENTRO de la ventana la preparación operacional pendiente: instalación owner del `EchoExecutionAddOn` staged (checklist patrón N1, OD-D6-4 standing) + despliegue/arranque del bridge release `40102ea5` con sesión de cuenta + verificación `binding_loaded`/`SubmissionCapabilitiesReady`. No emitir `EF_D6_E2E_PASS` hasta ladder completo.

### D6 — WEEKEND PHYSICAL READINESS (NO EGRESS) — READY — 2026-10-03

Shot TOP Senior Physical Readiness Lead (one-shot, fresh context; sin egress, OD-D6-1 intacto). Todo el trabajo operacional posible sin órdenes fue eliminado durante el cierre de mercado del fin de semana. Artifact: **`artifacts/d6-weekend-readiness-20261003/D6-WEEKEND-PHYSICAL-READINESS.md`** (+ `~/aranea/work/d6-weekend-readiness-20261003/evidence/`).

- **`D6_PHYSICAL_READINESS_NO_EGRESS = READY`** — BASELINE = FINAL = `40102ea5a44b…` (**cero commits, cero cambios de producto**). `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0`; `WRONG_ACCOUNT_EVENTS = DUPLICATE_PHYSICAL_SUBMITS = BLIND_RETRIES = UNRESOLVED_AMBIGUOUS_SUBMITS = PROVIDER_RULE_VIOLATIONS = COMMAND_FRAMES = 0`.
- **W1 EXECUTION_ADDON_INSTALLED = BLOCKED_OWNER_ACTION (preparado al 100%)**: ACL owner re-probada (4.ª vez, deny); bundle byte-verificado en `C:\Temp\` de dev-win + copia canónica en `var/nt-feed/owner-install/weekend-20261003/` — `EchoExecutionAddOn.cs` `b2a29a36…` (HEAD) + `EchoFeedAddOn.cs` `581a7087…` (actualiza el R3 instalado con la inversión Name-primaria) + `echo-execution-addon.json` (token ntx DEV incluido) + `OWNER-CHECKLIST-W1.md` (~3 min, patrón N1-R3).
- **W2 EXECUTION_LANE = PASS (lado bridge/transporte)**: release `40102ea5` desplegada (`vcs.modified=false`, SHA256 `484b550b…`), unidad `echo-futures-bridge` (disabled, started manual), listener `:9771`, consumer `ReadCommitted` (group DEAD benigno: topic de comandos inexistente), readiness fail-closed runtime (`ready_new_risk=false`, blockers correctos), barrier SE NIEGA a completar sin observaciones venue reales (fail-closed positivo, no se fabricaron snapshots). Path completo probado con sesión probe auto-etiquetada: hello → adapter (RESOLVED) → gate → Kafka `echo.futures.session-observations.v1` (281 ms). **Nota de ventana:** el shell no reintenta la sesión ⇒ arrancar el bridge con el AddOn ya conectado (o restart tras el ciclo owner).
- **W3 ACCOUNT_BINDING = PASS** (vivo hoy): `RESOLVED` 1/8 cuentas, NT `Account.Id = "3"` == hint ETCD (4.ª sesión consecutiva), sin drift, identidad Name-primary intacta.
- **W4/W7 SESSION_RECONNECT = PASS · SESSION_FENCING = PASS · RECOVERY_PRECHECK = PASS** (drills físicos: auth negativa ×N; fencing B→A con cierre inmediato de la supersedada; reconnect con identidad nueva + seq 0 aceptado (F-S2-01); seq rebobinada = counted-rejection nunca dato; 2× bridge restart con journal 0-phantom y reconexión <1.5 s; SIGKILL transporte → EOF drop → reconexión). Reconnect con el binario AddOn real queda en G-E2E por diseño.
- **W5 ACCOUNT_OBSERVATION = PASS** (feed lane real: account/positions/orders con `RESOLVED`, balances weekend-demo 0/0/0/0/0, executions primed-not-published; serialization frozen; 0 datos fabricados).
- **W6 G_HORIZON_PRECHECK = PARTIAL_NEEDS_CREATED_ORDER** (cuenta sin historial de la vertical; `LookbackDays*` runtime sólo medible desde NT; retención Kafka 168 h + evidence sink persistentes observadas; sin subsystem histórico creado).
- **W8 CLOSED_MARKET_FAIL_CLOSED = PASS** (edad event_ts ≈17 h >> bound 30 s ⇒ STALE con decay F-S2-02 ⇒ 0 señales, admission refusa; G-REALTIME sigue FAIL-por-calendario del intento 1, NO re-certificado). Probe determinista G-REALTIME documentado (`kafka-last` último candidato p4 ⇒ event_ts_age).
- **W9 NEXT_REALTIME_WINDOW (evaluado por el ENGINE con harness sobre los evaluadores frozen reales):** ventana GAU50-EVAL v1 = **L–V** `[00:00,15:50)` + `[17:10,23:59)` CT; **domingo CERRADO todo el día** ⇒ `SUNDAY_G_REALTIME_POSSIBLE = YES` (sólo feed: reopen CME dom 2026-10-04 17:00 CT) y `SUNDAY_PHYSICAL_LADDER_POSSIBLE = NO` (admission DENY Sunday); primera ventana admisible **lun 2026-10-05 00:00–15:50 CT** (edge 15:50 exacto verificado: 15:49 abierto / 15:50 cerrado; evening 17:10; gap y borde 23:59 verificados).
- **W10 FIRST_PHYSICAL_CERT_SCENARIO = FULLY_DEFINED**: ciclo G-E2E del freeze §14.13 (MARKET entry + STOP_MARKET venue-held + tighten cancel/replace + cancel + flat + drill restart con protectora working + 0 unknown live orders), NQ/NQZ6, cap GROSS 6 (engine: 6⇒breach/5⇒room), SL/TP owner day1 2000/1500, side/qty = output frozen de Strategy+GerardMM (jamás parámetro humano); `MISSING_PHYSICAL_PARAMETERS = NONE` (run-config de ventana = trabajo Manager desde autoridades frozen, no decisión owner nueva).
- **W11 PROVIDER_RULESET = PASS** (GAU50-EVAL v1 ACTIVE, 7 SourceRefs, guard 16 mutaciones verde; entitlement ALLOWED; consistency `UNDETERMINED` con evidencia cero y `BREACHED` en 31% — boundary `>=` verbatim; DENY sábado correcto por ventana).
- **W12 PERFORMANCE_PRECHECK = PARTIAL** (publish lane→Kafka 281 ms; reconnect recovery <1.5 s; barrier fail-closed 7.7 s; bridge ~30 MB RSS / 0.1% CPU; order/feed-dependent → DEFERRED_TO_LIVE_EGRESS). **W13 = SKIP** (instalación SIM exigiría el mismo paso owner; sin arquitectura de simulador).
- **Regresión @ `40102ea5` hoy:** `go test -race -count=1` — bridge 15 pkgs ok (EXIT=0), sdk 14 pkgs ok (EXIT=0), core functions + config/futures ok (EXIT=0), futuresvertical `-timeout 30m` ok (EXIT=0). Herramientas scratch eliminadas; tree limpio. Sin shadow-compile nuevo (source byte-idéntico a Shot 3).
- **Rollback de cierre ejecutado y verificado (doble lectura exacta; el MCP RO volvió a demostrar su matching difuso reportando "17:00" para la clave eliminada):** unidad parada, `:9771` cerrado, `futures-bridge/accounts` ELIMINADA (G-EGRESS-0 sin sesiones, como Shot 1/3); quedan inertes el release, la unidad disabled, `futures-bridge/ntx/auth-token` y `futures-bridge/journal-root`.
- **`OWNER_DECISION_REQUIRED = NONE`.** **LIVE_ONLY_REMAINING:** (1) ciclo owner W1 (checklist `C:\Temp\OWNER-CHECKLIST-W1.md`); (2) G-REALTIME positivo en ventana (dom ≥17:00 CT opcional con el probe listo); (3) dentro de la ventana del lunes: habilitar sesión + arrancar bridge → barrier con venue real → run config (warm-up + RUN_START) → ladder G-STOP → G-ID-Retention → G-HORIZON → G-E2E (+drill) → G-PERF.

**Next Manager action:** re-despachar el ladder físico congelado en la ventana **lun 2026-10-05 00:00–15:50 CT** (o evening 17:10–23:59 CT), anticipando opcionalmente el ciclo owner W1 al domingo ≥17:00 CT para pre-certificar G-REALTIME con el probe §9 del artifact. OD-D6-1 sigue AUTHORIZED sin consumir (mismo scope). No emitir `EF_D6_E2E_PASS` hasta ladder completo.

### D6 — REAL EXECUTION LANE POST-OWNER-INSTALL (NO EGRESS) — FAIL (instalación AddOn no efectiva) — 2026-10-03

Shot TOP Senior Physical Integration / Certification Lead (one-shot, fresh context; sin egress, OD-D6-1 intacto; despacho A–N). El Owner ejecutó el ciclo W1 (copiar AddOns + config al perfil KoR + reiniciar NT) y este shot verificó la instalación sobre la realidad y completó todo lo certificable del lane sin AddOn. Artifact: **`artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md`** (esquema A–N + runbooks M/N).

- **`D6_REAL_EXECUTION_LANE_NO_EGRESS = FAIL`** (despacho: PASS|REMEDIATION_REQUIRED|FAIL) — la certificación no se completó: **el EchoExecutionAddOn real nunca se cargó en NT** tras el ciclo owner. No es REMEDIATION_REQUIRED: no hay candidato de defecto de producto (mismos bytes con shadow-compile PASS en Shot 3; transporte y bridge verificados hoy). BASELINE = FINAL = `40102ea5a44b…` (**cero commits**; delta infra neto CERO). `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0`; topic `echo.order-commands.E2T-GAU50-01.v1` NO existe; session-observations sin registros nuevos; journal M2 vacío; grep `PREPARED|VENUE_BOUND|SUBMITTED|COMMAND_FRAME` = 0.
- **A OWNER_W1_VERIFIED = FAIL:** bundle staged re-verificado HOY byte-idéntico a HEAD ×3 (método probado en el mismo host); **bytes instalados no verificables — estructuralmente imposible por ACL** (`C:\Users\KoR\Documents` deny 5.ª vez; short-path 8.3 tampoco resuelve) y el `FILE_NOT_FOUND` de certutil con paths con espacio quedó **refutado como evidencia por contra-prueba** (mismo comando sin espacios funciona: artefacto de quoting del transporte, no ausencia).
- **B EXECUTION_ADDON_LOADED = FAIL (evidencia runtime, no presencia de archivos):** NT reiniciado OK (PID **1876 → 8700**, hello feed `64803b9b` 19:38:33Z seq 0 — feed AddOn compiló y corre) pero **0 intentos del exec AddOn a :9771 en ~40 min** con cadencia de diseño ≤10 s, 0 hellos `[ntx]`, netstat vacío, con bridge LISTENING y `Test-NetConnection = True` desde el host NT; **PID 8700 sin cambio en la re-verificación final**. Variantes NT-side (archivo ausente / compile-fail en arranque / config JSON no encontrado) no discriminables por ACL.
- **C/D ejecutados:** escritura guardada `futures-bridge/accounts=E2T-GAU50-01` (pre-read → put → read-back → cross-check MCP RO) + bridge start (PID 1737260, release `40102ea5`, listener `*:9771`) → barrier fail-closed a ~10 s con razón nueva `no authenticated AddOn session on the execution lane`; readiness fail-closed cada 30 s (8 blockers exactos, ambiguous/mismatches/dropped = 0/0/0) — **la conjunción frozen certificada: jamás abre sin AddOn autenticado**.
- **E–K:** binding feed-side vivo (`RJARA114411201551` = id `"3"` == hint ETCD, 5.ª sesión consecutiva; `RESOLVED` 1/8) · exec-side y REAL_RECOVERY_BARRIER/RECONNECT/FENCING/BRIDGE-RESTART = NOT_RUN con AddOn real (probe prohibido como sustituto y no usado; lado transporte vigente weekend) · J: restart owner reutilizado como evidencia equivalente (feed ✔, exec ✘) · **G_HORIZON = PARTIAL_NEEDS_CREATED_ORDER** (sin crear orden).
- **L:** `CURRENT_MARKET_FRESHNESS = STALE` (edad ≈22 h; p4 5476461 = replay estático de la sesión nueva) · `NEW_RISK_READY = NO` (freshness + ventana L–V) · **`SUNDAY_G_REALTIME_RUNBOOK = READY`** (procedimiento determinista §M, ya probado hoy con la misma llamada) · **`MONDAY_PHYSICAL_LADDER_RUNBOOK = READY`** (§N; gate 0 = fix owner) · `FIRST_PHYSICAL_CERT_SCENARIO = FULLY_DEFINED` · `MISSING_PHYSICAL_PARAMETERS = NONE`.
- **/final_safety_state probado: G-EGRESS-0** — unidad inactive+disabled, `:9771` FREE, clave de sesión eliminada con lectura exacta (21 claves restantes); feed lane conectado y observando; 0 LIVE run; 0 ambigüedad; new-risk configurationally disabled. MCP RO ETCD repitió el fuzzy-read ("17:00", 2.ª vez).
- **OWNER_DECISION_REQUIRED:** repetir W1 CON VERIFICACIÓN (checklist §A/§9 del artifact): verificar targets desde su sesión + hashes vs `b2a29a36…`/`581a7087…`/`9ca3fddc…` + re-copiar `-Force` desde `C:\Temp` + **reiniciar NT DESPUÉS de copiar** + `compile-errors.txt` si NinjaScript falla. Señal de éxito observable: dial `:9771` cada ≤10 s.

**Next Manager action:** veredicto FAIL ⇒ no certificar lane ni ejecutar ladder hasta el fix. Con la señal de éxito: re-despachar pasos C–K del artifact (~5 min) → domingo G-REALTIME (runbook §M) → ladder congelado §N en **lun 2026-10-05 00:00–15:50 CT**. OD-D6-1 vigente sin consumir. No emitir `EF_D6_E2E_PASS`.

### D6 — REAL EXECUTION LANE RETRY POST OWNER FIX (NO EGRESS) — FAIL (raíz única: config JSON puerto 0) — 2026-10-03

Retry TOP Senior Physical Integration / Certification Lead (one-shot, fresh context; sin egress, OD-D6-1 intacto). El Owner corrigió la fuente NinjaScript duplicada y reinició NT: **ambos AddOns ahora cargan** (SUPERSEDE el hallazgo de instalación del bloque anterior). Este shot resolvió el precheck crítico `ntx=****.161:0` y re-ejecutó todo lo certificable. Artifact: **`artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md` § POST OWNER FIX / RETRY (R0–R9)**.

- **`D6_REAL_EXECUTION_LANE_NO_EGRESS = FAIL` (2.º consecutivo, raíz única identificada):** el AddOn de ejecución SÍ carga (log owner formato exacto de la build HEAD `b2a29a36…`; NINJASCRIPT_DUPLICATE_SOURCE_INCIDENT = RESOLVED; NINJATRADER_COMPILE = PASS; EXECUTION_ADDON_LOADED = PASS; FEED_ADDON_LOADED = PASS físico, sesión `2e031cd2…`, PID 11412→:9770) **pero la config JSON instalada parsea `ntx_port = 0`** ⇒ guards `ntxPort<=0 ⇒ return` (fuente `:271`/`:407`) dejan AMBOS lanes del AddOn inertes para siempre. **NTX_PORT_ZERO_LOG_EXPLAINED = YES — opción B (puerto real 0, no redacción):** el format string imprime el puerto parseado sin máscara (MaskId sólo host/cuenta); host parseó bien (`****.161` ⇒ archivo existe con `ntx_host` correcto); el bundle correcto (SHA `9ca3fddc…`, `"ntx_port": 9771` numérico) está intacto en `C:\Temp` ⇒ el instalado difiere; confirmado físicamente: **cero conexiones contra listener `*:9771` activo >2.5 min** (≥7 fases de retry ≤10 s; 0 líneas `[ntx]`). Defecto **config-only**; ACL 6.ª re-probe (deny) ⇒ corrección = ciclo owner §R9 (reemplazar el JSON con la copia íntegra de `C:\Temp` + **reiniciar NT**; señal observable: ESTABLISHED→:9771 + hello ≤10 s).
- **C/F ejecutados con listener activo:** escritura guardada `futures-bridge/accounts=E2T-GAU50-01` (4 pasos + cross-check MCP RO) + bridge PID 1798251 release `40102ea5` (SHA `484b550b…`) → `account session built` 1.0 s → **barrier fail-closed a los 10.0 s exactos** (`no authenticated AddOn session on the execution lane`, 2.ª demostración); readiness `ready_new_risk=false` con los 8 blockers exactos, ambiguous/mismatches/dropped = 0/0/0; 0 comandos replayables (topic inexistente); binding ETCD 12/12 re-verificado por lectura cruda.
- **D/E/I:** binding feed-side vivo — `RJARA114411201551` = `resolved id "3"` == hint ETCD, **6.ª sesión consecutiva** (sink sin máscara); positions `[]`/orders `[]` observados en todos los ciclos; balances demo 50000/50000. Restart owner ≈21:25Z reutilizado como evidencia I (PID 8700→11412: feed recuperó ✔, exec cargó ✔, exec lane inerte por config — causa única). Exec-side D/E/G/H: NOT_RUN (endpoint no resuelto; mandato prohíbe ejecutar; probe no usado).
- **Hallazgo de producto residual (no elevado, §R8):** `LoadConfig` acepta `ntx_port` inválida con default silencioso 0 + log `"config loaded"` — contradice su disciplina declarada "any deviation = load failed fail-closed" (`EchoExecutionAddOn.cs:104-106`); repro exacta documentada; clase "robustez AddOn" (ítem no-elevado de Shot 3), adjudicación Manager; **PRODUCT_CODE_CHANGES = NONE** (BASELINE = FINAL = `40102ea5…`, worktree limpio).
- **K/L/M:** `MARKET_FRESHNESS = STALE` (edad ≈24 h; replay estático de la sesión nueva a las 21:25:21Z — offsets p4 5476462→5476468 — no refresca evidencia, F-S2-02) · `NEW_RISK_READY = NO` · `G_HORIZON = PARTIAL_NEEDS_CREATED_ORDER` · `SUNDAY_G_REALTIME_RUNBOOK = READY` — **G-REALTIME es feed-lane-only ⇒ certificable dom ≥17:00 CT SIN depender del fix owner** · `LIVE_PHYSICAL_LADDER_RUNBOOK = READY` (gate 0 = fix config §R9) · `FIRST_PHYSICAL_CERT_SCENARIO = FULLY_DEFINED` · `MISSING_PHYSICAL_PARAMETERS = NONE`.
- **/final_safety_state probado:** G-EGRESS-0 — unidad inactive+disabled, `:9771` FREE, clave de sesión eliminada (cross-check MCP RO **21 claves** == baseline), journal M2 **0 registros**; feed lane conectado observando; exec AddOn inerte (jamás conecta con puerto 0; tras el fix, sin listener = refusal sin estado). `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0`.

**Next Manager action:** veredicto FAIL ⇒ fix config §R9 por Owner (única acción, ciclo standing OD-D6-4) → dom ≥17:00 CT G-REALTIME (independiente del fix) → con la señal de éxito re-despachar C–K (~5 min en ventana) → ladder congelado §N **lun 2026-10-05 00:00–15:50 CT**. OD-D6-1 vigente sin consumir. No emitir `EF_D6_E2E_PASS`.

### D6 real execution lane — FINAL C–K post config fix (2026-10-03 noche)

TOP Senior Physical Integration / Certification Lead (one-shot, fresh context; sin egress, OD-D6-1 intacto; despacho C0–M). El Owner corrigió la config del exec AddOn (`9ca3fddc…` atestiguado en destino, NT reiniciado — boot físico 22:13:09Z, PID 11412→4576) y este shot ejecutó la certificación C–K completa hasta el STOP de C0 y cerró el hallazgo de producto C1. Artifact: **`artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md` § POST CONFIG FIX / FINAL C–K**.

- **`D6_REAL_EXECUTION_LANE_NO_EGRESS = REMEDIATION_REQUIRED` (3.er intento):** el runtime del nuevo proceso NT **contradice** la corrección atestiguada — con el bridge LISTENING en `*:9771` desde las 22:29:32Z (PID 2155952, release `40102ea5`, binario `484b550b…`), el EchoExecutionAddOn del PID 4576 hizo **CERO intentos de conexión en ≥18 min** (muestreo dev-win multi-ventana + `ss` servidor; firma de diseño: primer dial ~1 s tras Active, retry 10 s ⇒ ≥100 ciclos esperados). Barrier fail-closed a los **10.015 s** (3.ª demostración, razón literal idéntica). El bundle fuente `C:\Temp` SÍ es correcto (SHA re-verificado por agente). Dos hipótesis restantes, indistinguibles sin log NT owner (ACL 7.ª/8.ª re-probe: log/StartTime/módulos denegados): (a) config efectiva sin puerto dialable, (b) AddOn no cargó/compiló en ESTE boot. **C0 STOP por mandato.**
- **C1 CONFIG_FAIL_CLOSED_REPAIR = PASS (código):** commit **`d361008bfe4aa54fe3d8b6380d290bf92e1f1c08`** pusheado FF a `origin/feature/d6-shot1-execution-vertical` — `LoadConfig` valida host/port/token/account/contracts/intervals; en fallo resetea los campos de dial a inertes y loguea `config FAILED` (Error) ANTES de cualquier log de éxito; test estructural `TestExecAddOnConfigLoadFailsClosedOnInvalid` (paquete **5/5 PASS**); shadow-compile físico 8.1.8.3 **EXIT=0**, 0 errores, sólo los 3 warnings preexistentes; bytes corregidos `72d97ad6…`. SUPERSEDE el residual §R8 del retry. **Pickup físico pendiente al próximo ciclo de instalación owner** (el AddOn instalado sigue siendo `b2a29a36…`).
- **D–I por el exec lane: NOT_RUN/FAIL** (sin sesión nunca; 0 hellos `[ntx]`, 0 sockets, SESSION_A inexistente; probe weekend listo y NO usado). **E/F feed-side vivos:** rediscovery RESOLVED 1/8, `RJARA114411201551` = id `"3"` == hint ETCD (**7.ª sesión consecutiva**, sesión `f2756ae6…`); positions `[]`/orders `[]`, balances demo 50000/50000 (3.ª sesión). **J:** `G_HORIZON = PARTIAL_NEEDS_CREATED_ORDER`. **K:** readiness con los 8 blockers exactos, 0/0/0 ambiguos/mismatches/dropped; **STALE** (event_ts real ≈24 h; replay estático del boot corto `de38c5f2` no refresca — F-S2-02); **NEW_RISK_READY = NO**. **L:** `SUNDAY_G_REALTIME_RUNBOOK = READY` — feed-lane-only ⇒ certificable dom ≥17:00 CT sin depender del fix. **M:** ladder READY con gate 0 actualizado (diagnóstico owner del log NT + pickup C1).
- **/final_safety_state probado:** G-EGRESS-0 — unidad inactive+disabled, `:9771` FREE, clave de sesión eliminada con ciclo guardado (cross-check MCP RO **21 claves == baseline**), journal M2 **0 registros**, **0 COMMAND_FRAME** (histograma de msgs verificado), topic de comandos inexistente; feed lane conectado observando. `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0` en los 3 intentos del día.

**Next Manager action:** REMEDIATION_REQUIRED ⇒ no certificar lane ni ejecutar ladder. Domingo: G-REALTIME (independiente del fix). Owner: 1 ciclo diagnóstico (log NT del boot 19:13 local: ¿`config loaded: ntx=****.161:9771`? ¿líneas EchoExecutionAddOn ausentes?) + reinstalar el .cs corregido desde HEAD `d361008b` + restart NT con bridge en marcha; señal de éxito agente-observable: ESTABLISHED→:9771 + hello `[ntx]` ≤10 s. Entonces re-despachar C–K (~5 min) y ladder congelado lun 2026-10-05 00:00–15:50 CT. OD-D6-1 vigente sin consumir. No emitir `EF_D6_E2E_PASS`.

### D6 owner bundle — BUILD + STAGE pickup fix C1 — READY — 2026-10-03/04

TOP Senior Build / Release Preparation Specialist (one-shot, fresh context; sin egress, sin bridge, sin ETCD, sin Kafka, perfil NT del Owner intacto — la instalación es el ciclo owner). Materializa el pickup del fix C1 (`d361008b`) que quedó pendiente en el intento 3: bundle autocontenido `C:\Temp\EchoD6Bundle\` + scripts owner de instalación/verificación. Artifact: **`artifacts/d6-owner-bundle-20261003/D6-OWNER-BUNDLE-BUILD.md`**.

- **`D6_OWNER_BUNDLE = READY` @ `d361008bfe4aa54fe3d8b6380d290bf92e1f1c08`** (`feature/d6-shot1-execution-vertical`, origin == HEAD, worktree limpio). Contenido: `EchoFeedAddOn.cs` (`581a7087…`), `EchoExecutionAddOn.cs` (`72d97ad6…`, bytes del fix fail-closed LoadConfig), `echo-execution-addon.json` (`9ca3fddc…`, ntx 192.168.31.161:9771, RJARA114411201551, token PRESENTE_REDACTADO), `INSTALL-ECHO-D6.ps1`, `VERIFY-ECHO-D6.ps1`, `SHA256SUMS.txt`, `BUILD-INFO.txt`. Los archivos sueltos viejos de `C:\Temp` (pre-fix `b2a29a36…`) quedan SUPERSEDED.
- **Shadow compile real 8.1.8.3: PASS** (dev-win, csc .NET 4.x contra NinjaTrader.Core/Gui/WindowsBase físicas): FEED_EXIT=0 (0 err/0 warn), EXEC_EXIT=0 (0 err/3 warnings preexistentes Shot 1/3, ninguno nuevo), 2026-10-04T00:14:28Z; DLLs shadow solo en `C:\Users\TEMP`, nada instalado por el agente.
- **Scripts probados en dry-run** (perfil simulado `C:\Users\TEMP\sim-nt`, eliminado): syntax OK; guard NT-corriendo probado contra NT real (PID 4576) con mensaje exacto; INSTALL negativo (duplicados ⇒ FAIL con listado file:line; elimina SOLO duplicados de raíz conocidos) y positivo (1 declaración/clase en `bin\Custom\AddOns\EchoFeed\`, SHA256 bundle↔destino OK, config host/port/account OK, jamás imprime token); VERIFY read-only con detección doble del tamper `ntx_port→0`. Ubicación canónica de ambos AddOns: `bin\Custom\AddOns\EchoFeed\` (dedup de raíz incluido en el install).
- **Owner experience (COPY-PASTE, NT cerrado):** `& "C:\Temp\EchoD6Bundle\INSTALL-ECHO-D6.ps1"` → `& "C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1"` → abrir NinjaTrader. Con config fatal, la build `d361008b` ahora loguea `EchoExecutionAddOn config FAILED` en Error (jamás `config loaded` silencioso) — el diagnóstico del incidente puerto-0 queda observable sin log NT owner.

**Next:** ciclo owner (comandos de arriba) ⇒ agente fresh-context verifica `config loaded :9771` → TCP real → hello `[ntx]` autenticado ⇒ re-despacho C–K + ladder congelado lun 2026-10-05 00:00–15:50 CT. OD-D6-1 vigente sin consumir. Domingo ≥17:00 CT: G-REALTIME feed-lane-only (runbook L vigente).

### D6 execution config parser remediation — GetNumber whitespace — PASS — 2026-10-03/04

TOP NinjaTrader / C# Runtime Remediation Lead (one-shot, fresh context; sin egress/bridge/ETCD/Kafka, perfil NT del Owner intacto, sin continuar a C–K). Causa raíz del incidente puerto-0 confirmada y corregida; owner bundle re-stageado. Artifact: **`artifacts/d6-execution-config-parser-20261003/D6-EXECUTION-CONFIG-PARSER-REMEDIATION.md`**.

- **`D6_EXECUTION_CONFIG_PARSER_REMEDIATION = PASS`** — `ROOT_CAUSE_CONFIRMED = YES`: `GetNumber` @ `d361008b` escaneaba el token numérico desde `colon+1` sin skip de whitespace JSON ⇒ con la config canónica pretty (`"ntx_port": 9771`) el token salía vacío, `TryParse` caía al default `0` (log físico del Owner `config loaded: ntx=****.161:0` con JSON byte-idéntico `9ca3fddc…` instalado). El `EchoFeedAddOn` (físicamente funcional) no comparte el defecto: su tokenizer usa `SkipWs` alrededor de cada token.
- **Fix `7fbd7e99`** (push FF `d361008b..7fbd7e99`): skip whitespace JSON (space/tab/CR/LF) tras el colon + parse post-whitespace + fail-closed preservado (port ausente/ws-only/string-typed/0 → default; gate `d361008b` intacto, sin regresión). Mínimo, KISS, sin Newtonsoft ni reemplazo del parser. **Tooling `ffa493d8`** (push FF `7fbd7e99..ffa493d8`): `parser-harness/` = arnés de regresión generado mecánicamente desde el `.cs` real, 17 vectores adversariales.
- **Evidencia física (dev-win .132, .NET Framework real):** guardas Go red/green (red @ d361008b, green @ fix, sin falso positivo) + arnés: parser viejo **6/17** con `EXECUTION_ADDON_PARSED_PORT=0`, parser fixeado **17/17** con `EXECUTION_ADDON_PARSED_PORT=9771` contra la config REAL del bundle leída de disco (el token se lee en runtime, jamás embebido/impreso). Shadow-compile 8.1.8.3: 0 errores ambos AddOns, 0 warnings nuevas.
- **Bundle `C:\Temp\EchoD6Bundle` RE-STAGEADO (exactamente 7 archivos):** solo cambia `EchoExecutionAddOn.cs` (`72d97ad6…` → `2c8ab2cf…` = `git show HEAD`); `VERIFY-ECHO-D6.ps1` actualizado (token largo 64; hash `8382e457…`). Dry-runs en sandbox `-NtRoot`: VERIFY **PASS**, tamper `ntx_port=0` → VERIFY **FAIL** (línea `ntx_port inesperado: 0 (se requiere 9771)`), INSTALL **PASS** end-to-end. `SOURCE_STAGE_HASH_MATCH = PASS`. Pretty JSON sigue siendo el contrato (la minificación del owner fue solo diagnóstica).
- **Owner (COPY-PASTE, NT cerrado):** `powershell.exe -ExecutionPolicy Bypass -File "C:\Temp\EchoD6Bundle\INSTALL-ECHO-D6.ps1"` → `powershell.exe -ExecutionPolicy Bypass -File "C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1"` → abrir NinjaTrader. Señal esperada en log NT: `config loaded: ntx=****.161:9771 … contracts=1` (NUNCA `config FAILED`).

**FINAL_SHA:** `ffa493d8d179c9f9374d0a935e7916be15367ce8` (origin == HEAD == worktrees, historia intacta). **Next Manager action:** tras el ciclo Owner, certificación fresh-context que pruebe primero `config loaded … :9771` en el log runtime, luego TCP real :9771 + hello `[ntx]` autenticado, y recién ahí re-despachar C–K; ladder congelado lun 2026-10-05 00:00–15:50 CT; OD-D6-1 vigente sin consumir. Domingo ≥17:00 CT G-REALTIME feed-lane-only (independiente de este fix).

### D6 real execution lane — FINAL PARSER-FIX RETRY C→K (2026-10-04 madrugada)

TOP Senior Physical Integration / Certification Lead (one-shot, fresh context; NO-EGRESS, OD-D6-1 sin consumir). El owner ejecutó el bundle rebuild y NT cargó el EchoExecutionAddOn con config `:9771` — el parser fix quedó confirmado físicamente y el lane exec llegó al bridge por primera vez en 4 intentos (hello+auth PASAN). La certificación se detiene en **2 defectos de producto nuevos, demostrados físicamente** (nunca ejercitados antes: el bridge sólo había sido probado contra el probe, cuyo shape de frames es el del propio bridge). Artifact: **`artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md`** (sección FINAL PARSER-FIX RETRY); evidencia `~/aranea/work/d6-reallane-cert-final-20261004/evidence/`.

- **`D6_REAL_EXECUTION_LANE_NO_EGRESS = REMEDIATION_REQUIRED`** — progreso histórico: `CONFIG_PARSER_FIX_PHYSICAL = PASS` (log owner `config loaded: ntx=****.161:9771 … contracts=1` + confirmación conductual agente-side: 2× SYN_SENT→:9771 del PID NT 13068 + hello `echo.ntx.v1` con auth aceptada — imposible con puerto 0); `EXECUTION_ADDON_LOADED = PASS` (1.ª vez); barrier falló a los +3.692 s con `no position snapshot observed yet` (fail-closed correcto). Cero órdenes/comandos (0 COMMAND_FRAME, M2 journal 0, topic sin particiones); G-EGRESS-0 restaurado y probado al cierre (unidad inactive+disabled, :9771 FREE, clave sesión eliminada, 21 claves == baseline).
- **DEFECTO D1 (violación freeze §6.1):** el market lane del AddOn dializa el mismo endpoint ntx (`:9771`) con schema `echo.ntfeed.v1` ⇒ rechazo estructural del bridge (`frame schema … is not "echo.ntx.v1"`, físico 05:20:58.7Z); el freeze destina el market lane al nt-feed-relay `:9770` (one-way, zero churn). Además su socket muerto queda `marketConnected=true` sin reader ⇒ nunca re-dializa.
- **DEFECTO D2 (violación §6.1 "same payloads as ntfeed"):** el frame `account` del lane ntx serializa `resolved` como **bool** (`EchoExecutionAddOn.cs:~880-884`) y el bridge exige `Resolved *AccountRecord` objeto (`observations.go:137`) ⇒ `cannot unmarshal bool into …AccountData.resolved` (físico 05:21:08Z, tras hello+auth pasados) ⇒ VerifyBinding jamás recibe match, positions/orders/executions jamás se publican, **recovery barrier estructuralmente inalcanzable** con el AddOn real. El bridge NO requiere cambios (implementa el payload congelado).
- **Residual D3:** tras el 2.º reject el AddOn dejó de dializar ≥15 min (cadencia de diseño ≤10 s; timer muerto vs half-open, indistinguible por ACL — log NT owner discrimina). Una reconexión real sí se observó (identidad nueva + seq 0 a +5 s, auth re-pasada). `G_HORIZON_PRECHECK = PARTIAL_NEEDS_CREATED_ORDER` (4.ª vez); `MARKET_FRESHNESS = STALE` (domingo, CME cerrado — blocker esperado); `NEW_RISK_READY = NO`.
- Feed-side intacto y vivo: discovery 8 cuentas, 1 match RESOLVED (`RJARA114411201551` = Id "3", 8.ª sesión consecutiva). `SOURCE_SHA = FINAL_SHA = ffa493d8` (cero commits). **Next Manager:** (a) despachar remediación acotada D1+D2 (sólo `EchoExecutionAddOn.cs` + tests + re-stage bundle, ciclo owner W1, re-despacho C–K); (b) domingo ≥17:00 CT G-REALTIME feed-lane-only NO depende de estos defectos (runbook §M intento 1); (c) ladder congelado lun 2026-10-05 00:00–15:50 CT sólo tras re-cert en verde. No emitir EF_D6_E2E_PASS.

### D6 execution protocol remediation — F-D6-EXEC-01/02/03 — PASS — 2026-10-04

TOP Senior NinjaTrader / Execution Transport Remediation Lead (one-shot, fresh context; sin egress/bridge/ETCD/Kafka, sin órdenes, perfil NT del Owner intacto, sin continuar a C–K). Corrige los DOS defectos de producto demostrados físicamente en el intento 4 (market lane dializando :9771 con schema ntfeed; `resolved` bool vs objeto) más el endurecimiento mínimo del residual D3. Artifact: **`artifacts/d6-execution-protocol-remediation-20261004/D6-EXECUTION-PROTOCOL-REMEDIATION.md`**.

- **`D6_EXECUTION_PROTOCOL_REMEDIATION = PASS` @ `32baeaeb49cff8b4227b850d7a575549bbcf54a2`** (push FF `ffa493d8..32baeaeb`, origin == HEAD, worktree limpio; BASELINE `ffa493d8` verificado limpio antes de tocar fuente).
- **F-D6-EXEC-01 (freeze §6.1 restaurado):** el market lane resuelve su terminador exclusivamente del feed config certificado (`echo-feed-addon.json` `bridge_host`/`bridge_port` = nt-feed-relay :9770, mismo archivo ya fuente de su token; fail-closed si falta, execution lane sin dependencia); el execution lane dializa sólo `ntx_host/ntx_port` (:9771). Separación estructural por método (ningún método fuente mezcla ambos schema literals) + rechazo mutuo de parsers por wire. `CROSS_PROTOCOL_CONTAMINATION = NONE`; sin tercer transporte, EchoFeedAddOn byte-idéntico (`581a7087…`), bridge sin cambios.
- **F-D6-EXEC-02 (§6.2 same-payloads-as-ntfeed):** payload account ÚNICO canónico (`discovered[]` + `resolved` como objeto `AccountRecord` tipado + `balances{}` + `match`) publicado con bytes idénticos en ambas lanes; serialización bool prohibida en fuente y la forma histórica queda pineada rechazada por test negativo con el error físico exacto (`cannot unmarshal bool into …AccountData.resolved`). Parser del bridge intacto.
- **F-D6-EXEC-03 = FIXED (promovido):** D1/D2 no explican el silencio ≥15 min (cadencia ≤10 s; dial #2 sí ocurrió con identidad nueva + seq 0 + auth re-pasada). Corrección mínima: `SendTimeout 3s` en ambos sockets (peer muerto falla acotado y re-entra al loop), scan de reconexión por-lane aislado en el slow tick, socket liberado en EOF. Clase de wedge por lock bloqueado cerrada por construcción.
- **Contrato de protocolo probado comportamentalmente (no-grep):** `proto-harness/` extrae MECÁNICAMENTE los 11 builders puros del `.cs` real (sólo rewrite de visibilidad), compila con `csc.exe` .NET Framework real en dev-win .132 y emite 15 fixtures wire deterministas (tokens sintéticos) commiteadas en el repo; `protocol_contract_test.go` las corre por la cadena parser REAL del bridge (todas las familias del barrier aceptan; endpoints cruzados se rechazan mutuamente). El arnés detectó en .NET real un defecto del refactor (comilla de cierre de `ts_utc`) antes del stage — corregido en esta build.
- **Recovery barrier real-lane:** `internal/session/reallane_barrier_test.go` — `ntx.Server` + `Adapter` + `Session` reales con los frames AddOn por TCP: barrier AVANZA con hello → account RESOLVED → positions → orders; sigue fail-closed sin positions (error físico reproducido), SUBMITTING ausente de snapshot vacío ⇒ AMBIGUOUS + `ReadyNewRisk=false`, account incorrecto ⇒ `verify binding` falla. `RunRecoveryBarrier` 76.7% con sólo estos 4 tests; suite completa del módulo `futures-bridge` 14/14 paquetes ok.
- **Shadow compile físico 8.1.8.3:** EXEC 0 errores / 3 warnings preexistentes (0 nuevas); FEED 0/0. Config sin regresión (`9ca3fddc…` intacta; el endpoint ntfeed NO agrega claves). `ACCOUNT_IDENTITY = PASS` (Name-primary, Id "3" hint, sin fallback).
- **Bundle `C:\Temp\EchoD6Bundle` RE-STAGEADO desde este HEAD (7 archivos):** `EchoExecutionAddOn.cs` (`2c8ab2cf…` → `7f76b30e…`), `VERIFY-ECHO-D6.ps1` actualizado (`bd68f529…`: chequeo read-only del feed config, sin tokens), resto sin cambios; `SHA256SUMS.txt` regenerado; dry-runs sandbox: INSTALL **PASS**, VERIFY pass-path **PASS** (`bridge_host=192.168.31.161 bridge_port=9770`), VERIFY fail-path **FAIL** correcto.
- **Owner (COPY-PASTE, NT cerrado):** `powershell.exe -ExecutionPolicy Bypass -File "C:\Temp\EchoD6Bundle\INSTALL-ECHO-D6.ps1"` → `powershell.exe -ExecutionPolicy Bypass -File "C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1"` → abrir NinjaTrader. Señales esperadas en log NT: market lane conectado al relay sin rechazos y exec lane con sesión estable + account parseado (NUNCA `frame schema "echo.ntfeed.v1" is not "echo.ntx.v1"` ni `cannot unmarshal bool`).

**NEXT_MANAGER_ACTION:** tras el ciclo Owner, certificación fresh-context C→K (market lane al relay + exec lane con barrier completado en log runtime, luego el runbook C–K); ladder congelado lun 2026-10-05 00:00–15:50 CT sólo tras re-cert en verde. OD-D6-1 AUTHORIZED y SIN consumir (0 órdenes en 4 intentos). Domingo ≥17:00 CT: G-REALTIME feed-lane-only NO depende de esta remediación (runbook §M intento 1). No emitir EF_D6_E2E_PASS.

### D6 real execution lane — FINAL D1+D2+D3 RETRY C→K (2026-10-04 mediodía)

TOP Senior Physical Integration / Certification Lead (one-shot, fresh context; NO-EGRESS, OD-D6-1 sin consumir; despacho C0–M con verdad owner "bundle 32baeaeb instalado"). El runtime **refutó** esa verdad: el proceso NT en marcha ejecuta la **build VIEJA** del EchoExecutionAddOn y el C0 STOP cortó la certificación. Artifact: **`artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md`** (sección FINAL D1+D2+D3 RETRY); evidencia `~/aranea/work/d6-reallane-cert-final2-20261004/evidence/`.

- **`D6_REAL_EXECUTION_LANE_NO_EGRESS = FAIL`** (5.º intento; **NO REMEDIATION_REQUIRED**: no hay defecto de producto nuevo — el producto correcto de `32baeaeb` **jamás se ejecutó**). Triple firma física de build vieja, cada una estructuralmente imposible en el source nuevo: (1) 2 conexiones a :9771 con schema `echo.ntfeed.v1` @ 15:37:21Z (D1 — el source nuevo resuelve el market lane sólo del feed config :9770, fail-closed); (2) 2 rechazos `cannot unmarshal bool into …AccountData.resolved` @ 15:37:24/34Z (D2 — serialización bool prohibida en source); (3) silencio total post-rejects (D3-viejo — el source nuevo tiene SendTimeout+scan por-lane+release EOF). Relay :9770 sin ninguna sesión del market lane del AddOn dual. NT PID 11488 (boot 15:24:11.765Z por hello feed), proceso único; staging `C:\Temp\EchoD6Bundle` byte-idéntico a HEAD re-verificado ANTES del run ⇒ la fuente es correcta; el pickup al perfil/proceso no fue efectivo (ACL 11.ª impide discriminar .cs-viejo-en-destino vs NT-sin-recompilar).
- Preflight íntegro PASS (bridge binario alineado: `git diff 40102ea5..32baeaeb` sin Go de producto; ETCD 21==baseline, binding 12/12 exacto, token 64 hex, M2 0, topic 0 mensajes — NOTA: el topic de comandos ahora existe con 1 partición por auto-create). Bridge PID 2648085, listener `*:9771`, session built 15:37:20.891Z → **barrier fail-closed 5.ª demostración** a los +3.125 s (`no position snapshot observed yet`), NRestarts=0 sin loop. Feed-side identidad viva: **9.ª sesión consecutiva** RESOLVED 1/8 (objeto tipado, Id "3"), balances demo 50000/50000 (6.ª documentándola). G-EGRESS-0 restaurado y probado (key eliminada ciclo guardado, `:9771` FREE, 0 COMMAND_FRAME en 37 líneas de captura, deltas ETCD/dev-win neto CERO). `CROSS_PROTOCOL_CONTAMINATION = FAIL` (ntfeed llegó a :9771, rechazo cero-estado — causa build vieja). MARKET_FRESHNESS = STALE (domingo, CME cerrado — blocker válido según K). G_HORIZON = PARTIAL_NEEDS_CREATED_ORDER (5.ª vez).
- **L cerrado como FIXED (tooling only):** la causa del false negative del owner VERIFY era exigir `feed auth_token == 64` (contrato exec) cuando el contrato feed es presencia (token real 48 hex == ETCD `nt-feed/auth-token`; el relay enforce la igualdad). Patch 1 línea @ `C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1` (`BD68F529… → 5CA716ED…`); dry-runs sandbox: PASS con len=48, tamper port-0 FAIL, tamper no-token FAIL; `SHA256SUMS.txt` cubre sólo los 3 payload files; restage script only, payload intacto.

**Next Manager action:** veredicto FAIL ⇒ no certificar lane ni ejecutar ladder. (a) Owner: ciclo W1 correctivo con NT CERRADO (re-INSTALL + VERIFY corregido — debe imprimir los 3 sha en [OK]; si VERIFY verde y comportamiento viejo ⇒ recompilar NinjaScript F5 / revisar errores de compilación; abrir NT con bridge EN MARCHA). Señal de éxito observable: hello `echo.ntx.v1` + account RESOLVED objeto ≤10 s + SEGUNDA sesión en el evidence log del relay + 0 rejects. (b) Hoy ≥17:00 CT: G-REALTIME feed-lane-only (runbook §M intento 1, no depende del pickup). (c) Tras señal verde: re-despachar C→K fresh (~5 min) → ladder congelado lun 2026-10-05 00:00–15:50 CT. OD-D6-1 vigente sin consumir (0 órdenes en 5 intentos). No emitir EF_D6_E2E_PASS.

### D6 real execution lane — ATTEMPT 6 FORCED NINJASCRIPT PICKUP / FINAL C→K (2026-10-04 tarde)

TOP Senior Physical Integration / Certification Lead (one-shot, fresh context; NO-EGRESS, OD-D6-1 sin consumir; despacho C0–M tras el ciclo owner W1 correctivo: NT cerrado → bundle reinstalado → instalación verificada → F5 NinjaScript CERO ERRORES → NT cerrado → reiniciado). El runtime **CONFIRMÓ** esa verdad: **RUNTIME_BUILD_PICKUP = PASS por primera vez en 6 intentos** y el lane REAL alcanzó **sesión estable autenticada con recovery barrier PASADO**. Se detiene sólo en H (bridge restart recovery) por hallazgo de producto nuevo acotado. Artifact: **`artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md`** (sección ATTEMPT 6); evidencia `~/aranea/work/d6-reallane-cert-attempt6-20261004/evidence/`.

- **`D6_REAL_EXECUTION_LANE_NO_EGRESS = REMEDIATION_REQUIRED`** (6.º intento; progresión decisiva: C0+transporte+binding+observaciones+barrier-estable+reconnect/fencing PASS; H FAIL). **C0 (las 3 firmas):** exec lane → :9771 con `echo.ntx.v1` autenticado (cero rechazos `[ntx]` en 6 sesiones/~25 min), account `resolved` como OBJETO aceptado por el parser REAL del bridge (cero `cannot unmarshal bool`; VerifyBinding RESOLVED 6/6), market lane del dual (hello `addon_version 2.0.0` — identidad de build doble-demostrada) en el relay :9770 desde 16:08:16.128Z con payload same-as-ntfeed, `CROSS_PROTOCOL_CONTAMINATION = NONE`. Build instalada = `32baeaeb` (7f76b30e) — las firmas son estructuralmente imposibles en la build vieja; supersede del FAIL del intento 5.
- **C–G certificados (primeras veces):** preflight íntegro (binario 484b550b@40102ea5 alineado — delta sin Go de producto; ETCD 21==baseline, binding 12/12, token 64 hex, topic 0 mensajes). Bridge PID 2664145, session built 16:21:06.675Z; NT PID 1476 (boot W1 16:08:15Z, boots owner 16:05–16:08Z fechados por el relay). **SESSION_A ESTABLE ~15 min:** binding Name-primary RJARA114411201551=hint "3" (10.ª sesión del perfil), account RESOLVED + positions [] + orders [] **consumidas físicamente por el barrier** → **`REAL_RECOVERY_BARRIER = PASS` (PRIMERA VEZ)** con UnknownLiveOrders=0/Mismatch=0/Ambiguous=0/Replay=0/journal 0. **Reconnect:** disconnect acotado 39 s → EOF→re-dial loop VIVO (5 dials SYN_SENT observados, SIN wedge — fix D3 operando), SESSION_B nueva conexión+identidad+seq 0 legal, auth re-pasada; fencing server-side (F-S2-04 + gate adapter.go:270), 0 command frames.
- **`BRIDGE_RESTART_RECOVERY = FAIL` — hallazgo de producto NUEVO con repro exacta:** 6 arranques con el AddOn real ⇒ **1 PASS / 5 FAIL** (`barrier: reconcile: ninjatrader: no position snapshot observed yet` a +2.8–6.1 s; fail-closed seguro: sesión muerta, proceso vivo NRestarts=0, comandos dejan de consumirse). Causa pinned: `RestoreSubscriptions` pasa con el **hello** (`lastObserved` se setea en todo frame, `adapter.go:297`) y `Reconcile`→`PositionSnapshot` falla **instantáneo** sin `positionsAt` (`adapter.go:941`), mientras el AddOn real sólo publica positions/orders en el tick de snapshot (**cada 10 s**, sin burst al conectar — `EchoExecutionAddOn.cs` fastTimer 2 s × snapshot_seconds 5) ⇒ el barrier re-pasa sólo si el tick cae en la ventana de ms [hello, reconcile]; SESSION_A pasó por coalescencia del burst tras el hello en el buffer TCP. Los tests pasan porque envían la ráfaga inmediata. Impacto: el drill restart congelado del ladder exigiría re-PASS first-try ⇒ fallaría ~5/6 veces (detención segura del ladder). Remediación candidata (Manager adjudica; NO tocada en este shot): bridge-side esperar freshness de POSICIONES (no cualquier frame) o AddOn-side burst inicial al conectar; pin en `reallane_barrier_test.go` con positions retardadas.
- **K:** EXECUTION_TRANSPORT_READY=YES · ACCOUNT_READY=YES · RECOVERY_READY=NO (única brecha) · MARKET_FRESHNESS=STALE (event_ts 2026-10-02T21:38:25.95Z, ≈43 h; domingo CME cerrado — blocker válido) · NEW_RISK_READY=NO. **L:** VERIFY tooling FIXED confirmado por hash (5ca716ed…, contrato feed=presencia). **J:** G_HORIZON = PARTIAL_NEEDS_CREATED_ORDER (6.ª vez). G-EGRESS-0 restaurado y probado al cierre (unidad inactive+disabled, `:9771` FREE, key eliminada ciclo guardado — MCP RO 21 claves == baseline; feed lane + market lane observando). 0 órdenes (6 intentos), 0 comandos, deltas ETCD/dev-win neto CERO, cero commits.

**Next Manager action:** (a) CONGELAR como certificado el pickup C0 + transporte C + binding D + observaciones E + barrier estable F + reconnect/fencing G — no tocar AddOns/transporte. (b) Despachar remediación acotada de H (repro + refs en el artifact; elegir bridge-side freshness-wait vs AddOn-side burst; pin en reallane_barrier_test). (c) Tras remediación + W1: re-despachar C→K fresh (drill restart FIRST-TRY determinístico) → ladder congelado §N en la primera ventana admisible lun 2026-10-05 00:00–15:50 CT. (d) Hoy ≥17:00 CT: G-REALTIME feed-lane-only (runbook §M intento 1, no depende de H). OD-D6-1 vigente sin consumir. No emitir EF_D6_E2E_PASS.


### Backtester V1 — BT-S03 adversarial review (2026-10-04)

[[Echo Futures — BT-S03 Adversarial Review]]: **BT_S03_REMEDIATION_REQUIRED**,16 findings aceptados (5 CRITICAL,8 MATERIAL,1 KISS,2 MINOR). F01/F02/F03/F05 originales confirmados, F04 requiere remediación. Baseline Backtester f41da25c; repros tagged publicados en `xKoRx/echo:codex/bt-s03-adversarial-review@13bb72bb`; suites finales autorizadas PASS en namespace sin red externa. D6 avanzó32baeaeb→d08a30ce, delta sin conflicto shared; ninguna integración D6.

**Incidente operativo abierto:** Sol causal ejecutó una suite SDK amplia no autorizada que reportó escrituras en ETCD production. Se detuvo/escaló; no se restauró ni se verificó impacto runtime. Detalle y evidencia sanitizada en artifact. No inferir infraestructura intacta por el review ni recuperación por suites verdes.

**Próximo paso:** Primary Technical Manager revisa BT-S03 y adjudica el contrato acotado S04; no se inició S04 ni se entregó prompt al Owner. Recuperación/verificación de configuración productiva requiere coordinación autorizada independiente.

### Backtester V1 — BT-S04 final remediation + certification (2026-10-04)

[[Echo Futures — BT-S04 Final Remediation and Certification]]: **BT_S04_FINAL_CERTIFICATION_PASS** @ `feature/backtester-v1-s04-remediation@cd451972` (pusheado, tree limpio; base `feature/backtester-v1-s02@f41da25c`). F01–F14 FIXED, F16 FIXED, F15 ACCEPTED_MINOR_OPEN (documentado: adapters productivos ya filtran; fix rompería contratos frozen). F01–F05 originales todos `CONFIRMED_FIXED_WITH_REGRESSION`. Repros tagged S03: 23/24 verdes (rojo restante = F15); baseline de entrada 20 rojos. Phase 0 test-safety: seeds ETCD v1/v2/v3 tras build tag `seeds` + `ECHO_SEED_ALLOW` + endpoint guard (evidencia bajo `unshare --net`, sin ejecutar seed real). Certificación verde: SDK futures, backtester completo 396.5s (a52 incluido), core functions/runtime/vertical, consumers, CLI build; builds legados v1/v2 rotos PREEXISTENTES en el baseline. Monitor ETCD pre/post suites idéntico (mod_revision 59390, digest `8a36217243c1`, cero escrituras en `/echo/` durante S04). D6 refresh inicial y final = `d08a30ce` sin delta: `NON_CONFLICTING`. 4 subagentes reales (B/C/D paralelos + A), ownership disjunto, 3 adaptaciones de oráculo documentadas in-file. Residual ambiental: `REAL_CONDITIONAL_WRITE = NOT_VERIFIED_ENVIRONMENTAL`, flake a52 bajo contención (PASS secuencial/aislado).

**Próximo paso:** Primary Technical Manager revisa BT-S04; al aceptar, Backtester V1 queda terminado (programa cierra; no se inicia otra fase).

### D6 bridge restart recovery — F-D6-H REMEDIATION — PASS — 2026-10-04

TOP Senior Recovery / Execution Transport Remediation Lead (one-shot, fresh context; NO-EGRESS, OD-D6-1 sin consumir, AddOns intocados). Corrige el ÚNICO defecto del ATTEMPT 6: la carrera de recovery al rearrancar el bridge (1 PASS / 5 FAIL, `barrier: reconcile: ninjatrader: no position snapshot observed yet` a +2.8–6.1 s; PASS sólo por alineación del tick de snapshot del AddOn con el arranque). Artifact: **`artifacts/d6-bridge-restart-recovery-20261004/D6-BRIDGE-RESTART-RECOVERY-REMEDIATION.md`**; evidencia `~/aranea/work/d6-bridge-restart-recovery-20261004/`.

- **`D6_BRIDGE_RESTART_RECOVERY_REMEDIATION = PASS` @ `d08a30ce9815f820fda7132e20dc42cc345eb8e8`** (push FF `32baeaeb..d08a30ce`, origin == HEAD, worktree limpio; BASELINE 32baeaeb verificado limpio antes de tocar fuente). Delta: 4 archivos (+372/−66), producto sólo en `adapters/ninjatrader/adapter.go`.
- **Root cause confirmada en source antes de modificar:** `RestoreSubscriptions` se satisfacía con el hello (`lastObserved` se setea en TODO frame, `adapter.go:289`), `Reconcile`→`PositionSnapshot` falla instantáneo sin `positionsAt` (`adapter.go:941`), y el AddOn real publica positions/orders sólo en su tick de ~10 s sin burst al conectar. Brechas hermanas: sin marker de recepción de orders (H5) y hello sin reset de vistas de la sesión superseda (H2).
- **Remedio bridge-side (H1–H5):** `RestoreSubscriptions` espera positions AND orders snapshots de la sesión ACTUAL (hello/heartbeat = sólo liveness); snapshot observado-VACÍO es evidencia autoritativa (`no observado` ≠ `observado vacío`); hello nuevo retira markers y outcome de reconciliación de la sesión superseda (executions se conservan — identity-keyed, limpiar duplicaría fills); espera acotada por el presupuesto EXISTENTE `ObservationFreshness` (30 s = 3 ticks, sin knob nuevo; `CommandTimeout` queda en su autoridad), timeout ⇒ FAIL CLOSED `required recovery snapshots not observed within bound (positions=X orders=Y)`; `PositionSnapshot` intacto fail-closed (H4); marker `ordersAt` en `handleOrders` (H5).
- **H6 — 7 casos sobre el stack REAL** (`reallane_barrier_test.go`, segunda conexión TCP + session ids distintos): hello-only bounded FAIL; DELAYED SNAPSHOT (regresión 1/6): barrier ESPERA ≥300 ms y pasa al llegar los snapshots; empties aceptados como fresh; missing-positions/missing-orders bounded FAIL nombrando la familia faltante; SESSION_B no reusa SESSION_A (fenceo server visible) y pasa con sus propios snapshots; wrong-account sin regresión. Funciones cambiadas 100% coverage (paquete 95.9%); suite `futures-bridge` 14/14 paquetes ok.
- **Físico 6/6:** binario nuevo release-dir `releases/d08a30ce…/futures-bridge` (`-trimpath`, `vcs.revision=d08a30ce`, sha256 `fb1ce6d4…`), unidad apuntada; NT/Addon NUNCA tocados (sin W1: AddOn byte-idéntico). Armado operativo: clave `/echo/development/futures-bridge/accounts` estaba AUSENTE (estado desarmado del cierre attempt 6 ⇒ `accounts:0` idle, descubierto en el 1.er drill, `evidence/prearm-timeout/`); se armó `=E2T-GAU50-01` (rev 59388) y se eliminó al cierre (rev 59389). 6 ciclos start/stop consecutivos: cada uno con sesión AddOn ESTABLISHED, `recovered:true` en el PRIMER readiness (+30 s), ambiguous/mismatches/dropped=0, 0 errores, 0 command frames (topic 0 mensajes, committed `-1001` invariante), journal 0, blockers sólo los de diseño Shot 1. **BRIDGE_RESTART_RECOVERY = 6/6 PASS first-try, sin alineación afortunada.**
- **G-EGRESS-0 restaurado y probado:** key fuera, unidad inactive+disabled, :9771 FREE, ETCD 21 claves == baseline, topic 0/lag 0, journal 0, AddOn feed/market lanes observando (relay :9770) sin mutación.
- **Residual/tooling:** el MCP ETCD RO volvió a dar lectura fuzzy de clave inexistente (`accounts`→`"17:00"`); verdad por API cruda. Bit-reproducción del binario viejo no alcanzada (flags idénticos, shas distintos) — proveniencia anclada por FINAL_SHA + `go version -m` + sha256.

**NEXT_MANAGER_ACTION:** aceptar H como CERRADO; congelar C0–H / execution transport (no tocar AddOns ni recovery transport de nuevo); certificar G-REALTIME (feed-lane-only, no depende de H); luego el ladder físico D6 ya autorizado en la primera ventana admisible lun 2026-10-05 00:00–15:50 CT. OD-D6-1 vigente SIN consumir. No emitir EF_D6_E2E_PASS hasta que el ladder pase.

## 2026-10-04 — G-REALTIME: certificación física de market data realtime (feed-only, NO-EGRESS)

**Estado:** `D6_G_REALTIME = PASS` @ `d08a30ce9815f820fda7132e20dc42cc345eb8e8` (C0–H congelado, cero commits, cero mutaciones ETCD/config; único delta = artifact + registros observacionales). Artifact: **`artifacts/d6-g-realtime-20261004/D6-G-REALTIME-CERTIFICATION.md`** (+ `evidence/g-realtime-evidence.txt`).

- **Sesión CME físicamente abierta:** primer tick físico 21:05:41.433Z (pre-apertura, BBO movió vs viernes), stream sostenido desde 21:54:23Z, apertura oficial 22:00Z con ~1,700–2,300 eventos/min; NQ 31044→31142 con TRADEs reales. Certificado por movimiento físico, no por wall-clock (el tick de 16:05 CT quedó documentado como rotación de apertura del venue).
- **Feed real:** EchoFeedAddOn 1.0.0 (sesión `5b70e536…`, hello autenticado, `NQ 12-26`) + EchoExecutionAddOn 2.0.0 (`348f52ba…`, account-only en feed lane, sin sesión ntx) sobre NT 8.1.8.3 dev-win .132 PID 1476; relay PID 1388002 (release `170a4581`, up 2+ días), 2× ESTABLISHED a :9770, heartbeats ~10 s, `reconnects:1`, 0 errores/supersedes reales en 8 h; discovery RESOLVED 1/8 continuo (`RJARA114411201551` = Id "3", balances demo 50000/50000).
- **Freshness (autoridad event_ts, bound frozen 30 s):** 5 muestras sucesivas post-reopen (22:00:48Z→22:12:30Z) con edades **0.14/0.15/0.18/0.12/0.11 s** — `MAX_EVENT_AGE = 0.18 s << 30 s`; transit event_ts→Kafka 89–295 ms. Ventana formal 18 min con **22,494 eventos reales** (p4 5476488→5498982), tipos QUOTE+TRADE, `ntfeed.published` +21,714 con publish_errors=0. El replay del boot (event_ts viernes) quedó excluido como prueba — trampa prohibida por el gate.
- **Identidad:** cada evento key/stream `NQ:NQZ6`, source `NINJATRADER_ADDON`, ETCD crudo `nt-feed/instruments = NQ 12-26→NQ:NQZ6` sin drift. `CURRENT_MARKET_FRESHNESS = FRESH` por el modelo frozen sobre el path feed-only congelado (probe runbook §9); el consumo del vertical con run-config pertenece al ladder.
- **G-EGRESS-0 PASS al cierre:** unidad bridge inactive+disabled, :9771 sin listener y 0 conexiones (contaminación cruzada estructuralmente imposible — NONE), ETCD `accounts` ABSENT (API cruda) con 21 claves == baseline, topic `echo.order-commands.E2T-GAU50-01.v1` 0 mensajes (HW 0, committed `-1001`), journal M2 0 archivos, venue plano `positions:[]/orders:[]` observado vivo 22:13:10Z. `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0`.
- **Residual no bloqueante:** fase pre-apertura dispersa del venue (documentada); fallos OTLP export del relay a 192.168.31.45:4317 (observabilidad only).

**NEXT_MANAGER_ACTION:** CONGELAR G-REALTIME como certificado (no re-ejecutar en la ventana del lunes salvo anomalía). Despachar el FINAL D6 PHYSICAL LADDER ya autorizado (OD-D6-1 vigente SIN consumir) en la primera ventana admisible ProviderRuleSet: **lun 2026-10-05 00:00–15:50 CT** (o evening 17:10–23:59 CT), con la preparación operacional del intento 1 §17.2 DENTRO de la ventana (habilitar `accounts` + arrancar bridge → barrier con venue real → run config → G-STOP → G-ID-Retention → G-HORIZON → G-E2E (+drill) → G-PERF). No emitir `EF_D6_E2E_PASS` hasta que el ladder completo pase.

## 2026-10-05 — D6 FINAL PHYSICAL CERTIFICATION intento 2: ENVIRONMENTAL_BLOCKED (feed venue muerto, ladder no forzado, G-EGRESS-0 intacto)

**Estado:** `D6_FINAL_PHYSICAL_CERTIFICATION = ENVIRONMENTAL_BLOCKED` @ autoridad frozen `d08a30ce9815f820fda7132e20dc42cc345eb8e8` (cero commits, cero mutaciones; OD-D6-1 **VALID y SIN CONSUMIR**, 0 órdenes). Artifact: **`artifacts/d6-final-physical-certification-20261005/D6-FINAL-PHYSICAL-CERTIFICATION.md`** (+ `evidence/g-final-evidence.txt`). Lunes 19:05 CT, dentro de la ventana evening `[17:10,23:59)` — el ladder se detuvo en el **gate B antes de armar egress**.

- **`C0_H_HEALTH = PASS` (acotado):** release `d08a30ce` verificada (worktree limpio, origin == HEAD, release puente presente sin arrancar); NT vivo continuo desde el boot W1 (sesión AddOn `5b70e536…` sin cambio de identidad); feed/exec AddOns con heartbeats vivos; relay `:9770` sano (PID 1388002, publish_errors=0); `:9771` FREE = G-EGRESS-0; identidad `RJARA114411201551` → `Account.Id "3"` RESOLVED viva (11.ª sesión); topic de comandos 0 mensajes; journal 0; venue `positions:[]/orders:[]` — 0 unknown live orders.
- **`CURRENT_MARKET_FRESHNESS = STALE` (STOP del ladder):** probe frozen 2 tomas — p4 offset `6172016` congelado, último evento `NQ:NQZ6` `event_ts 2026-10-05T04:40:06.376Z` (dom 23:40:06 CT), edad ≈19.4 h >> bound 30 s, **cero avance entre tomas** con el venue abierto (throughput certificado ~1,700–2,300 ev/min). **Causa raíz física del propio AddOn** (sink `evidence.jsonl`): `connection "Simulación" ConnectionLost @ 2026-10-05T04:40:54.675Z` + `MarketData RESET "NQ 12-26" @ 04:44:46.428Z`, **sin ningún `Connected` posterior** — corte media sesión antes del cierre programado, sobrevivió al reopen de 17:00 CT, NT no reconecta solo en ~19.5 h. Venue abierto corroborado por fuente independiente (NQ ~30,808 +306 evening). NQ cayó ~270 pts tras morir el feed con la cuenta FLAT: el fail-closed STALE bloqueó new-risk exactamente como diseñado; 0 exposición. Reconexión = acción GUI owner (ACL C0 re-confirmada: tasklist SSH dev-win Access denied). No es defecto de producto: el mismo runtime midió FRESH ≤0.18 s el domingo.
- **Provider admission:** config íntegra ALLOWED (binding 12/12, GAU50-EVAL v1, ventana evening abierta al momento del shot); ejercicio per-order NOT_RUN (sin RUN_START no hubo orden). Gates D–N NOT_RUN (dependen de FRESH). G_HORIZON 7.ª vez `PARTIAL_NEEDS_CREATED_ORDER`. Balances 0/0/0/0/0 = artefacto documentado de desconexión (domingo 50000/50000), a re-observar.
- **Estado final seguro:** G-EGRESS-0 intacto en 3 superficies (unidad inactive+disabled, `:9771` sin listener, ETCD `futures-bridge/` = 21 claves == baseline con clave `accounts` ABSENT); topic 0; journal 0; venue plano; 0 commits.

**NEXT_MANAGER_ACTION:** escalación **OD-D6-3 conditional**: Owner reconecta en GUI de NT la conexión **"Simulación"** + datos NQ 12-26 (~2 min); señal de éxito agent-side = `market_events` del heartbeat `5b70e536…` avanzando + offsets del feed topic avanzando con `event_ts` fresco (probe §M) + balances 50000/50000. Con esa señal, re-despachar el ladder congelado COMPLETO (OD-D6-1 vigente sin consumir; C0–H y G-REALTIME frozen) en la primera ventana admisible (remaining evening 2026-10-05 o mar 2026-10-06 00:00–15:50 CT), secuencia §17: armar sesión+bridge → barrier → run config → RUN_START → G-E2E → G-STOP → G-ID-Retention → G-HORIZON → drill recovery → G-PERF → cuenta final. No emitir `EF_D6_E2E_PASS` hasta ladder completo.

### Backtester V1 — manager closure + Stage 2/3 continuity — 2026-10-05

**Manager gate:** `BACKTESTER_V1 = CLOSED / CERTIFIED` sobre `feature/backtester-v1-s04-remediation@cd451972b242c8933321e03001decd4b6d778c61`. BT-S00→S04 cerrados; BT-F01..F05 en `CONFIRMED_FIXED_WITH_REGRESSION`; BT-S03-F01..F14 FIXED, F16 FIXED y F15 `ACCEPTED_MINOR_OPEN`. KISS/YAGNI final = PASS. El incidente ETCD de S03 fue recuperado y S04 añadió build-tag + opt-in + endpoint guard para seeds; cero escrituras ETCD durante la certificación.

**Importante — integración Git:** Backtester V1 **NO está mergeado a `master`**. Al cierre de esta sesión: `master@372af59a7b83604781346613da01e3d510ea1360`; Backtester certificado `cd451972...`; D6 continúa en carril separado `feature/d6-shot1-execution-vertical@d08a30ce9815f820fda7132e20dc42cc345eb8e8`. No mergear/rebasear preventivamente mientras D6 siga vivo; el próximo Manager debe refrescar ambos HEADs y reconciliar sólo deltas shared reales.

#### Programa vigente Owner — Gerard + bankroll, máximo cinco shots — 2026-10-05

El Owner amplía la continuidad Stage 2/Stage 3 en un solo programa: hacer funcionar el backtester con Strategy y GerardMM reales; medir cuentas quemadas, retiros y profit de una campaña con bankroll; reinvertir retiros cobrados; máximo cuatro retiros por cuenta; buscar objetivos monetarios convenientes. Plan: [[BTG-PLAN]]. Primer encargo listo: [[BTG-S01-SUBMANAGER-PROMPT]].

**Estado:** `BTG-S01 = IN_PROGRESS — OWNER_SELECTED_S2_AND_1M_PESSIMISTIC_MODEL`; `S02–S05 = NOT_STARTED`; `REAL_GERARD_RUN = NOT_RUN` en este programa. S01 usa submanager persistente sin cupo de ciclos internos; especialistas ONE-SHOT. S02 diseña el delta; S03–S05 siguen implementación → adversarial LOCAL independiente → corrección/gate final. El Primary Manager conserva coordinación y no se autocierra.

**Datos aún por resolver:** Owner expresó bankroll `5k`, costo `120k` y ~41 cuentas; `USD 5.000 / USD 120` es hipótesis explicativa, no unidad confirmada. Recuperar configuración/identidad Gerard y dataset físico antes de certificar S01; recuperar reglas/fees/settlement del programa antes de resultados económicos. Las 41 compras son capacidad inicial ilustrativa, no límite total con reinversión. Conservar baseline de una cuenta operando a la vez salvo instrucción posterior. Detalle, límites y gates en [[BTG-PLAN]].

#### Próxima etapa — Stage 2: REAL HISTORICAL BACKTEST / GERARD

Objetivo de producto: **usar el Backtester V1 certificado con datos históricos REALES y la Strategy/configuración Gerard canónica REAL; si no corre o descubre un defecto, corregir el producto/shared-domain hasta que el run real funcione correctamente.**

Reglas:
- No rediseñar Backtester V1 ni crear otro engine.
- Recuperar desde source/autoridades la identidad exacta de la “estrategia Gerard” y su configuración real; no sustituirla por fixture, aproximación o estrategia inventada.
- GerardMM debe ser el runtime real compartido.
- Dataset de validación debe ser histórico real, durable y reproducible (ticks; BBO cuando la fidelidad requerida lo necesite), con contratos físicos/rollover reales y manifest/digests.
- Comenzar con un slice real acotado para smoke/diagnóstico y escalar a un horizonte longitudinal representativo; la evidencia primaria de Stage 2 no puede ser corpus sintético.
- Ante fallo: reproducir → identificar primer divergence/error → corregir en shared domain/backtester donde corresponda → regression → volver a ejecutar el mismo histórico. No parches sólo para fixture/backtest.
- Registrar performance real (records, tiempo, memoria, tamaño de artifact) sin optimización prematura ni SLA inventado.
- Persistir results/artifacts reproducibles; no iniciar todavía análisis económico masivo/campaign simulation.
- Completion candidate: Strategy Gerard + GerardMM reales ejecutan E2E sobre histórico real con `COMPLETE`/outcome esperado, multi-contract cuando el horizonte lo requiera, sin decisiones manuales en el loop y con bugs descubiertos cerrados por regresión.

#### Etapa posterior — Stage 3: PROP CAMPAIGN / ECONOMICS

Sólo después de Stage 2 validado. Objetivo: utilizar el motor/backtests ya confiables para modelar **muchas cuentas de fondeo y bankroll**: compra/fees/resets, evaluation/next stages/funded, cuentas quemadas, payouts, reinversión y continuidad temporal.

Métricas mínimas futuras:
- cuentas compradas / fallidas / pasadas / funded / con payout;
- fees y resets pagados;
- payouts brutos;
- beneficio/pérdida neta;
- bankroll inicial/final y curva temporal;
- tiempo a primer payout;
- duración de cuentas;
- coste esperado por payout/cuenta viable;
- resultados por prop/programa/stage y Strategy/MM.

Boundary frozen: el futuro Campaign Simulator **orquesta cuentas y bankroll fuera del Backtest Engine**. No replica Strategy/GerardMM/Provider/Accounting; cada cuenta se conduce mediante el mismo engine/contexts/cashflows ya certificados.

**NEXT_MANAGER_ACTION:** continuar S01 según [[BTG-S01-OWNER-S2-BARS-AUTHORITY]]: Owner seleccionó S2 actual + GerardMM y NQ 1m con SL-first. Alias resuelto; [[BTG-S01-NQ-1M-DATASET]] confirma caché Windows inaccesible al usuario SSH y corpus NOT_ACQUIRED. TOP delimita seam OHLC/causal bars/next-open compartido en [[BTG-S01-S2-1M-FORENSICS]]. Resolver lectura/export de los bytes y configuración necesaria para el horizonte; sin optimización, S02 ni gate nuevo demostrado.
