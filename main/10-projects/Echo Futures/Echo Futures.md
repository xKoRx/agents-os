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
updated: "2026-09-25"
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

La V1 live **no implementa todavía el módulo completo de backtesting**, pero la arquitectura debe quedar preparada para construirlo inmediatamente después del primer vertical multi-prop/shadow sin reescribir Strategy ni CapitalManagement.

Objetivo posterior inmediato a V1:
- operar una primera cohorte pequeña de cuentas en shadow/demo;
- estabilizar runtime live;
- construir un módulo independiente de backtesting/replay reutilizando las mismas abstracciones;
- reutilizar sus outputs posteriormente en The Lab y en futuros workflows de construcción/selección de portfolios.

### Restricción de diseño

Las siguientes piezas deben ser reutilizables fuera del proceso live:

- Strategy;
- Signal;
- CapitalManagement;
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
    -> same CapitalManagement
    -> SimExecution
    -> Order/Fills
    -> Operation
    -> Trade
    -> Research/Lab outputs
```

No se permite crear una segunda implementación tipo:
- `strategy_live` vs `strategy_backtest`;
- `capital_management_live` vs `capital_management_backtest`.

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

### Requisitos/decisiones del owner ya establecidos

- Futures V1 corre sobre/extendiendo Echo; no crear un segundo sistema independiente.
- Strategy vive lógicamente en Core y emite Signal.
- Signal incluye direction + entry type `MARKET|LIMIT|STOP` + entry/trigger cuando corresponda + SL + TP.
- Signal no define sizing ni provider/account.
- Strategy se asocia a cuentas mediante AccountStrategy.
- Una Signal fan-out a todas las AccountStrategy habilitadas que referencian esa Strategy.
- Echo no corrige automáticamente duplicados/conflictos causados por una mala configuración de estrategias.
- AccountStrategy V1 selecciona un CapitalManagement.
- CapitalManagement administra la Operation completa, no sólo sizing inicial, y puede reaccionar a market bars/events.
- V1 debe poder expresar hardscalping Gerard negativo y positivo.
- Trade continúa siendo el resultado cerrado consumido por `trade_journal` / The Lab.
- Escala de arquitectura V1: 100–200 cuentas sin rediseño.
- Símbolos internos canónicos + mapping físico actualizable hot.
- Rollover automático fuera de V1; lo administra manualmente el owner.
- Sesiones deben ser configurables y consistentes entre live/replay/backtest.
- La arquitectura debe permitir un módulo independiente de backtesting posterior reutilizando Strategy + CapitalManagement.
- V1 debe demostrar al menos un execution transport real.
- Dynamic portfolios, smallcaps y multi-CapitalManagement por AccountStrategy quedan fuera de V1.

### Propuestas fuertes a validar en D1/D2

- `Operation = Signal × Account`.
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
| Q11 | **Strategy runtime:** cuándo corren Strategy y CapitalManagement (tick, forming bar, closed bar, other events), state ownership e interfaces. | **D2** | Interfaces/event model/state ownership definidos. |
| Q12 | **S2:** confirmar o reemplazar H4 trend + 5m Bollinger pullback. | **D4** | Segunda estrategia mecánica exacta incluida en SPEC de desarrollo. |
| Q13 | **Gerard +/- exacto:** parámetros/config/state transitions necesarios para una primera implementación determinista. | **D4** | CapitalManagement V1 completamente mecanizable; cero decisión humana ambigua requerida para desarrollo. |
| Q14 | **Backtest boundary:** qué paquetes/contratos deben quedar libres de dependencias live para que el runner independiente sea barato de construir. | **D2** | Boundary explícito que permite reutilizar Strategy/CapitalManagement/domain sin Core live. |
| Q15 | **Trade/Lab compatibility:** qué campos existentes se preservan, cuáles se extienden y cómo se distinguen live vs simulated. | **D2** | Contrato Trade→trade_journal→Lab y provenance/mode resueltos. |
| Q16 | **Blocking refactor:** si Echo actual impide alguna capacidad, ¿se resuelve ahora o queda DT/Core V3? | **D2** | Cada gap de D1 queda clasificado como adaptación/refactor <=1 día o DT no bloqueante con impacto explícito. |

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
  capital_management_id
  enabled
  config
```

V1: una relación AccountStrategy usa un CapitalManagement.

Múltiples CapitalManagement simultáneos por relación quedan YAGNI/futuro.

### CapitalManagement

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

> realización de una Signal concreta sobre una Account concreta.

Se crea aunque una orden de entrada quede pendiente, por ejemplo una LIMIT aún sin fill.

Una Operation:
- pertenece a Signal + Account + AccountStrategy;
- mantiene lifecycle propio;
- es administrada por CapitalManagement;
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
- cómo acceden Strategy y CapitalManagement a ellas por tick/bar sin latencia de segundos;
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

Trabajo coordinado:
- recuperar en detalle dominio/source de Echo actual;
- contrastar Strategy/Signal/Operation/Order/Fill/Position/Trade con contratos físicos;
- recuperar S1/S2 y Gerard +/- desde evidencia previa;
- iniciar/ejecutar census Prop Universe;
- research dirigido de market-data/bar-state implementations;
- inventario de feeds/execution technologies existentes;
- feasibility de al menos un execution transport real;
- contract identity/mapping hot y semántica manual de rollover;
- trading sessions/timezone/DST/calendar;
- blocker discovery explícito para Position attribution, Order lifecycle y backtest reuse boundary;
- registrar gaps y contradicciones, no diseñar aún alrededor de supuestos.

Deliverable:
`D1 Analysis Pack`.

Gate:
`EF_D1_ANALYSIS_PASS = REVIEW`.

No código productivo.

### D2 — DESIGN / Domain + Technical Architecture

**Manager goal:** convertir D1 en una arquitectura candidata completa y simple.

Debe producir primero un **Domain & Data Model Candidate** (identities, cardinalities, lifecycle, authority, persistence/hot/derived) y luego congelar como candidato:
- domain model;
- entity lifecycles/cardinalities;
- Strategy/Signal contract;
- AccountStrategy;
- CapitalManagement contract;
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
- imposibilidad de reutilizar Strategy/CapitalManagement en un backtester independiente;
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
- CapitalManagement Gerard +/-;
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
- mismo CapitalManagement;
- mismas Signal/Operation/Order/Fill/Trade semantics;
- SimExecution determinista;
- outputs utilizables por The Lab;
- base futura para research y construcción de portfolios.

El coste esperado debe ser bajo precisamente porque V1 habrá preservado estas abstracciones. Si después de V1 el backtester exige reescribir Strategy o CapitalManagement, se considera un defecto de arquitectura de V1.

## ✅ Definition of Done V1

V1 no termina porque compile.

Debe demostrar, según SPEC congelada:
- dos estrategias V1 ejecutables;
- Signal sin sizing/provider;
- Strategy→Signal→todas las AccountStrategy asociadas;
- CapitalManagement stateful incluyendo Gerard +/- congelado;
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
- múltiples CapitalManagement simultáneos por AccountStrategy;
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

Estado al cierre:
- proyecto canónico nuevo [[Echo Futures]] creado y reencuadrado;
- experimento económico anterior preservado como [[Echo Futures — Prop Economics Experiment]];
- modelo de dominio actual registrado como propuesta, no freeze;
- Critical Design Register activo;
- todas las preguntas abiertas tienen día máximo obligatorio;
- ningún research/desarrollo de D1 ejecutado todavía.

**Next exact milestone:** D1 — ANALYSIS / Problem & Domain Discovery.

**Urgencia owner:** `EF_D1_ANALYSIS_PASS` debe cerrarse **hoy 2026-09-25**.

D1 debe ser dirigido por un Manager Agent usando la skill `technical-project-manager`. No comenzar D2 ni implementación antes de que el owner/manager acepte el gate D1.
