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
updated: "2026-09-26"
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

**Estado actual 2026-09-25:** `EF_D1_ANALYSIS_PASS = NOT_EVALUATED`. Existe [[Echo Futures — D1 Analysis Pack]] como adelanto preliminar generado por el manager, incluyendo source audit y scouting útil, pero el owner corrigió explícitamente que D1 **no está cerrado**. Debe continuarse workstream por workstream, delegando deep research/auditorías y revisando los resultados con el owner.

No código productivo.

### D2 — DESIGN / Domain + Technical Architecture

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
