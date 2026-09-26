---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
aliases:
  - Echo Futures Front E
  - Contract and Session Semantics Evidence
  - Futures Contract Session Evidence
tags:
  - kind/resource
  - area/echo
  - echo-futures
  - futures
  - contracts
  - trading-session
  - market-structure
  - research
created: "2026-09-26"
updated: "2026-09-26"
---

# CONTRACT + SESSION SEMANTICS — AUTHORITATIVE EVIDENCE

> [!important]+ Estado
> **Front:** D1 / Front E — Contract + Session Semantics  
> **Resultado:** `READY_FOR_PRIMARY_MANAGER_REVIEW`  
> **Q6 Contract mapping:** `D1_INPUT_SUFFICIENT_FOR_D2`  
> **Q7 Session semantics:** `D1_INPUT_SUFFICIENT_FOR_D2`  
> **D1 completo:** sigue `IN_PROGRESS`; este recurso NO cierra D1 ni congela arquitectura D2.

## 1. Propósito

Este recurso preserva la investigación y revisión completa realizada para resolver las preguntas D1:

- **Q6 — Contract mapping:** qué diferencia existe entre el producto económico/canonical root y el contrato futures expiry-specific realmente ejecutable; qué identidad y specs necesita Echo; cómo deben entenderse continuous/current mappings; y qué evidencia existe para pinnear el Contract en una Operation.
- **Q7 — Session semantics:** qué significa una TradingSession de futures; cómo se relacionan trade date, timezone, DST, maintenance breaks, holidays/early closes, ventanas de provider/prop y el DayBoundary de cuenta; y qué inputs necesita Echo para reproducir exactamente la misma semántica LIVE/REPLAY/BACKTEST.

El objetivo de Front E **no era diseñar las structs/APIs finales**, sino producir evidencia suficientemente fuerte para que D2 pueda tomar esas decisiones sin inventar semántica de mercado.

## 2. Contexto canónico previo

Autoridades internas de esta iteración:

- [[Echo Futures]]
- [[Echo Futures — D1 Analysis Pack]]

Baseline de trabajo al iniciar Front E:

- Agents-OS: `master@17902b44669fb13db14399a9461377236bd34df1`
- Echo: `master@372af59a7b83604781346613da01e3d510ea1360`

Decisiones/restricciones ya existentes y no reabiertas:

- Echo Futures extiende Echo; no nace un Core Futures separado.
- Echo trabaja con un **canonical Instrument/root** y requiere mapping hot hacia un contrato futures específico.
- El rollover V1 es **manual por owner**; automatic rollover queda fuera de V1.
- Una nueva Signal/Operation posterior a un mapping change debe poder resolver al nuevo Contract sin redeploy.
- El candidato de diseño era que una Operation ya materializada conservara el Contract resuelto y no fuera retargeteada retroactivamente.
- TradingSession es un concepto distinto de Account DayBoundary.
- LIVE/REPLAY/BACKTEST deben compartir la misma semántica de runtime.
- Futures no puede usar pips como unidad universal; el cálculo monetario debe apoyarse en contract/instrument specs.

## 3. Cómo se investigó

La iteración tuvo dos pasos deliberados.

### 3.1 Deep Research inicial

Se pidió evidencia formal sobre:

1. root/product vs expiry-specific contract;
2. contract identity/lifecycle;
3. physical/orderable contract;
4. continuous/current/mapped contract;
5. remap/rollover behavior;
6. money-management specs;
7. feed/execution/provider identifiers;
8. trade/session date;
9. timezone y DST;
10. maintenance breaks;
11. holidays/early closes;
12. diferencias por producto;
13. exchange hours vs ProviderProgram windows;
14. forced-flat;
15. deterministic session/bar semantics.

Fuentes prioritarias requeridas:

- **CME Group first-party** como autoridad de mercado;
- **ProjectX first-party** como evidencia de contract identity y execution API;
- **QuantConnect LEAN** sólo como patrón de diseño para continuous/mapped futures;
- **Topstep first-party** sólo para demostrar overlay ProviderProgram sobre el exchange.

### 3.2 Revisión adversarial y repair

El primer artifact no fue aceptado directamente. Se detectaron defects materiales:

- uso de **ClusterDelta** cuando existía evidencia first-party;
- ProjectX estaba prácticamente omitido;
- contradicción en el maintenance break de NQ;
- `physical Contract` podía confundirse con physical delivery;
- LEAN estaba demasiado cerca de elevarse a market authority;
- “continuous no tradable” estaba formulado de forma absoluta;
- el remap podía interpretarse como migración automática de posición;
- expiry estaba mezclada con Money Management monetario;
- faltaba demostrar el ProviderProgram overlay;
- trade date y DST necesitaban clasificación más precisa entre FACT e INFERENCE.

Se ejecutó un **targeted evidence repair**, no un research general nuevo. El resultado reparado fue aceptado sustantivamente.

## 4. Jerarquía de evidencia

### Tier 1 — Market / venue authority

**CME Group**:
- contract codes;
- NQ contract specs;
- settlement;
- regular trading hours;
- maintenance period;
- Globex holiday schedules;
- early closes;
- notices que vinculan Sunday session con siguiente trade date.

### Tier 1 — Execution/platform contract identity

**ProjectX Gateway**:
- Contract search/searchById;
- `contractId`;
- `symbolId`;
- `tickSize`;
- `tickValue`;
- `activeContract`;
- Order/place;
- Order/Position/Trade runtime identity;
- close/partial-close behavior.

### Tier 2 — Engine pattern, no market authority

**QuantConnect LEAN**:
- continuous Symbol;
- `Mapped`;
- `contractDepthOffset`;
- mapping events;
- explicit rollover example.

### ProviderProgram overlay

**Topstep**:
- forced-flat;
- allowed resume time;
- product-specific close precedence;
- holiday early-close offset.

No se conserva ClusterDelta como autoridad normativa de Front E.

---

# Q6 — CONTRACT MAPPING

## 5. Terminología aceptada

### Instrument / product root

Representa la identidad económica/canónica que Echo quiere operar.

Ejemplo conceptual:

```text
Instrument = NQ
```

No debe confundirse con una expiración concreta ni con un ID de una plataforma determinada.

### Contract

Para este proyecto, `Contract` significa:

> **expiry-specific listed/tradable futures contract**

Ejemplos humanos/plataforma: `NQH5`, `NQZ6`.

Importante: “physical Contract” en conversaciones previas de Echo significaba **binding físico/ejecutable hacia un contrato específico**, NO “physically delivered future”.

NQ es financially/cash settled; settlement method y contract identity son ejes distintos.

## 6. Matriz de evidencia canónica Q6

| ID | Clasificación | Conclusión soportada |
| --- | --- | --- |
| **C-E01** | FACT | El product/root económico y el expiry-specific listed Contract son capas de identidad distintas. Los contract codes futures incorporan product code + expiration month/year y el display puede variar por plataforma. |
| **C-E02** | FACT | Un Contract posee identidad/lifecycle ligado a su vencimiento. NQ como producto tiene specs económicas comunes, mientras cada contrato listado representa una expiración concreta. |
| **C-E03** | FACT | La ejecución puede requerir identidad contract-specific. ProjectX exige explícitamente `contractId` para `Order/place`. |
| **C-E04** | PATTERN | Un continuous/current representation puede mapear a distintos expiry contracts con el tiempo. LEAN materializa esto mediante continuous Symbol + `Mapped` + mapping events. |
| **C-E05** | PATTERN → INFERENCE_FOR_ECHO | El mapping change no demuestra migración automática de una posición. El ejemplo LEAN realiza explícitamente old liquidation + new order. Para Echo, esto soporta fuertemente pinnear el Contract de una Operation. |
| **C-E06** | FACT | Los inputs monetarios demostrados para NQ incluyen tick size/value, contract unit/multiplier, currency/price denomination y quantity semantics del provider. |
| **C-E07** | FACT + UNKNOWN | Expiration/month/last-trade/active pertenecen al lifecycle del Contract. ProjectX expone `activeContract`, pero no en el payload inspeccionado un `expirationAt`/ `lastTradeAt` estructurado; D2 debe escoger autoridad para esos timestamps si los necesita. |
| **C-E08** | FACT | Feed/execution/platform IDs no deben tratarse como universal economic identity. CME codes, ProjectX `contractId`/`symbolId` y LEAN Symbol son capas distintas. |

## 7. ProjectX — evidencia de contract-bound execution

ProjectX aporta la evidencia externa más útil para el boundary que Echo necesita.

`Contract/search("NQ")` puede devolver, para un contrato concreto:

- `id` — usado como contract identity;
- `name` — por ejemplo `NQU5`;
- `description`;
- `tickSize`;
- `tickValue`;
- `activeContract`;
- `symbolId`.

`Contract/searchById` denomina al argumento **`contractId`**.

Ejemplo documentado por ProjectX:

```text
contractId = CON.F.US.ENQ.H25
name       = NQH5
symbolId   = F.US.ENQ
```

Conclusión válida:

- `contractId` y `symbolId` son identifiers distintos;
- ProjectX NO documenta en esta evidencia que `symbolId` sea una universal/economic family identity;
- no debemos promover semántica adicional por intuición.

### Order identity

`POST /api/Order/place` requiere:

- `accountId`;
- `contractId`;
- `type`;
- `side`;
- `size`.

Por tanto es válido afirmar:

> **ProjectX submits/routes an order against an expiry-specific `contractId` supplied by the caller.**

No se infieren detalles internos de routing no documentados.

### Runtime identity persistence

La identidad contractual continúa después de submit:

- **Order:** order `id`, `contractId`, `symbolId`;
- **Position:** position `id`, `contractId`;
- **Trade:** trade `id`, `contractId`, `orderId`;
- realtime conserva estas capas;
- close/partial-close APIs también utilizan contract identity.

Esto demuestra que la resolución previa a ejecución **no elimina el expiry-specific contract identity** cuando comienza el lifecycle físico.

## 8. Continuous / current / mapped contracts

LEAN se usa únicamente como **PATTERN**.

Patrón demostrado:

```text
continuous Symbol
      |
      +--> Mapped expiry Contract A

mapping event

continuous Symbol
      |
      +--> Mapped expiry Contract B
```

`contractDepthOffset` participa en la selección del contrato dentro de la serie y `SymbolChangedEvent` expone old/new mapping.

Corrección importante respecto del primer research:

- no mantener la afirmación absoluta “continuous Future is non-tradable”;
- la documentación vigente permite operar el continuous en ciertos contexts, pero recomienda el `Mapped` underlying para live;
- lo importante para Echo es el patrón **economic/continuous abstraction → expiry-specific execution identity**.

### Rollover

El ejemplo oficial de LEAN ante mapping change:

1. recibe old/new symbols;
2. obtiene quantity del old;
3. ejecuta `Liquidate(old)`;
4. ejecuta `MarketOrder(new, quantity)`.

Por tanto:

> **PATTERN:** mapping change itself does not constitute an automatic migration of an existing position; rollover is explicit algorithm behavior in the documented LEAN example.

Esto NO se eleva a ley universal de todos los futures engines.

## 9. Operation → Contract pinning

La evidencia conjunta favorece fuertemente el candidato original de Echo.

Cadena:

```text
canonical Instrument
      |
      +--> contract resolution
              |
              +--> expiry-specific contractId
                       |
                       +--> Order
                       +--> Position
                       +--> Trade
```

ProjectX preserva contract identity a lo largo del lifecycle ejecutado.

LEAN demuestra de forma independiente que un mapping event puede cambiar el current/mapped contract sin convertir por sí mismo la exposición previa en la nueva expiración.

### Conclusión

`OPERATION_CONTRACT_PINNING = STRONGLY_SUPPORTED_INFERENCE`

Inferencia para D2:

> Una Operation debe conservar el Contract que resolvió al materializarse, salvo que exista una acción explícita de rollover/migration.

Esto **no** significa que el mercado obligue a modelarlo exactamente así; significa que es la interpretación de dominio más consistente con la evidencia y con el requisito owner de hot mapping manual sin retarget retroactivo.

## 10. Money Management — minimum monetary specs

Separar dos planos.

### MONETARY SPECS

Para NQ quedaron sustentados:

- `tickSize / minimum price fluctuation`;
- `tickValue`;
- `contractMultiplier / contractUnit`;
- currency / price denomination;
- quantity/contracts semantics del provider.

Ejemplo NQ:

- CME contract unit: **$20 × Nasdaq-100 Index**;
- ProjectX `tickSize = 0.25`;
- ProjectX `tickValue = 5`;
- ProjectX order `size` es integer en la API inspeccionada.

Estos datos permiten convertir price movement × quantity a exposición/P&L monetario sin usar pips como unidad universal.

### CONTRACT LIFECYCLE SPECS

Separados del cálculo monetario directo:

- contract month;
- expiration;
- last trading day/time;
- active/inactive;
- execution eligibility.

Expiry puede ser crítica para mapping, rollover y eligibility, pero **no es un multiplicador monetario**.

## 11. Identifier layers

Front E no soporta un “global future contract ID” universal.

Capas observadas:

1. **Echo canonical Instrument** — por ejemplo `NQ`;
2. **CME product/contract display code** — product + month/year;
3. **ProjectX symbolId**;
4. **ProjectX contractId**;
5. **ProjectX human name** — por ejemplo `NQH5`;
6. **LEAN continuous Symbol**;
7. **LEAN Mapped expiry Symbol**.

D2 debe diseñar mapping/provenance entre capas, no colapsarlas.

---

# Q7 — TRADING SESSION / CALENDAR

## 12. Semánticas que deben permanecer separadas

Front E confirmó que al menos estos conceptos NO son equivalentes:

### ExchangeSession

Cuándo el exchange/product acepta negociación según su calendario.

### Session / trade date

La fecha operativa a la que el exchange atribuye una sesión, que puede diferir de la fecha civil cuando la sesión comienza la tarde anterior.

### ProviderProgram allowed window

Ventana adicional impuesta por prop/provider/programa, potencialmente más restrictiva que el exchange.

### Forced-flat boundary

Hora límite en que un ProviderProgram exige estar flat, aunque el exchange siga abierto.

### Account DayBoundary

Boundary interno/contractual de una Account para resets, drawdown, HWM u otras reglas diarias.

Echo ya tiene DayBoundary para cuentas; Front E **no lo convierte en TradingSession**.

## 13. Matriz de evidencia canónica Q7

| ID | Clasificación | Conclusión soportada |
| --- | --- | --- |
| **S-E01** | FACT | Una sesión futures puede comenzar el día civil anterior a su trade date. CME publica notices con `Sunday ... (trade date Monday ...)`. |
| **S-E02** | FACT → INFERENCE_FOR_ECHO | La autoridad temporal debe conservar timezone semantics; NQ se publica en CT/ET. Hardcodear un offset UTC fijo es incorrecto para una timezone que cambia con DST. |
| **S-E03** | FACT | El schedule incluye maintenance/intraday closed windows recurrentes. NQ tiene maintenance diario 4:00–5:00 PM CT. |
| **S-E04** | FACT | Holidays y early closes pueden overridear el horario regular; CME publica calendario separado y advierte que puede modificarse/finalizarse cerca del feriado. |
| **S-E05** | FACT | Holiday/trading schedules pueden diferir por product group/product. No asumir un calendario idéntico para todos los futures. |
| **S-E06** | FACT | Exchange availability y ProviderProgram allowed window son autoridades distintas. |
| **S-E07** | FACT | Un provider puede imponer forced-flat antes del exchange close; Topstep exige flat 3:10 PM CT donde NQ CME normalmente sigue disponible hasta 4:00 PM CT. |
| **S-E08** | INTERNAL AUTHORITY / EXTERNAL UNKNOWN | Account DayBoundary debe permanecer separado de ExchangeSession por la arquitectura y source Echo existentes; este Front no pretende demostrar una regla universal externa para resets de cuenta. |
| **S-E09** | INFERENCE_FOR_ECHO | LIVE/REPLAY/BACKTEST deterministas necesitan aplicar la misma calendar/session semantics al ordenar/bucketear market events y session transitions. |

## 14. NQ session authority

CME publica para NQ:

- **Sunday 5:00 PM CT → Friday 4:00 PM CT**;
- equivalente publicado: 6:00 PM → 5:00 PM ET;
- **maintenance break diario: 4:00 PM–5:00 PM CT**.

Este dato corrige el primer artifact, que había derivado indirectamente horas desde GMT+2 y terminó con una contradicción.

### Autoridad temporal

Echo no debe almacenar la sesión como “UTC-6”.

La regla se expresa en la timezone de autoridad —CT/Chicago semantics— y luego se transforma a instantes concretos.

Razón:

- Central Time usa CST en standard time y CDT en daylight time;
- por lo tanto su offset UTC cambia a lo largo del año.

Front E clasifica esto correctamente:

- **FACT:** CME expresa el schedule NQ en CT/ET;
- **INFERENCE_FOR_ECHO:** una implementación con offset UTC fijo no reproduce fielmente la regla anual.

## 15. Trade date

CME demuestra explícitamente casos del tipo:

```text
Sunday session
    -> trade date Monday
```

y holiday cases donde un pre-open dominical se asigna a un trade date posterior.

Conclusión soportada:

> trade date no puede derivarse simplemente desde la fecha civil del timestamp.

No se demostró ni se necesita para D1 una fórmula universal:

```text
every CME future after 5 PM CT = next trade date
```

Eso queda como `UNKNOWN_GENERALIZATION`.

D2 necesita consumir una autoridad calendar/session válida para el producto, no inventar una regla global.

## 16. Holidays / early close

CME mantiene un holiday calendar separado del regular schedule.

La evidencia demuestra:

- puede existir early close;
- el override puede variar por product group;
- el schedule puede cambiar;
- CME indica que normalmente se finaliza aproximadamente dos semanas antes del holiday.

Implicación de diseño:

> regular weekly schedule por sí solo no basta para resolver session state.

No se requiere en D1 construir un calendario universal ni precargar décadas de expirations/holidays.

## 17. ProviderProgram overlay — Topstep

Topstep se utilizó únicamente para demostrar que las reglas operacionales del programa pueden ser más restrictivas que la sesión del exchange.

Evidencia:

- posiciones deben estar flat a **3:10 PM CT**;
- trading puede reanudarse a **5:00 PM CT**;
- si el producto cierra antes de 3:10 PM, manda el close propio del producto;
- en early close, Topstep exige cerrar **15 minutos antes** y auto-liquida exposición que permanezca abierta.

Comparación:

```text
NQ CME normal availability: ... -> 4:00 PM CT
Topstep forced flat:              -> 3:10 PM CT
```

Por tanto:

> **FACT:** Topstep allowed-trading window is more restrictive than CME exchange availability.

> **INFERENCE_FOR_ECHO:** ExchangeSession y ProviderProgram allowed window son autoridades distintas y no deben representarse como el mismo dato.

## 18. Session/calendar inputs mínimos para D2

La evidencia soporta que D2 pueda diseñar un modelo con capacidad para expresar, sin congelar todavía su forma física:

- timezone authority;
- recurring weekly open/close windows;
- maintenance/intraday breaks;
- product/family applicability;
- trade/session date assignment;
- holiday closures;
- early-close overrides;
- effective calendar/versioning cuando cambian reglas;
- ProviderProgram allowed windows;
- ProviderProgram forced-flat boundaries;
- relación separada con Account DayBoundary.

Esto NO obliga a crear un “universal calendar engine” complejo.

## 19. LIVE / REPLAY / BACKTEST y bar boundaries

Front E no rediseña Front B, pero sí establece una dependencia clara.

Para que LIVE y REPLAY/BACKTEST produzcan la misma interpretación temporal, el mismo event stream debe atravesar las mismas reglas de:

1. timezone;
2. session open/close;
3. maintenance breaks;
4. holiday overrides;
5. early closes;
6. trade/session-date assignment;
7. product applicability;
8. ProviderProgram boundaries cuando formen parte de la decisión;
9. calendar/ruleset version aplicable al instante histórico.

Implicación:

> bucketear barras futures por medianoche UTC o por civil date sin session context puede producir boundaries distintos a los usados por la estrategia live.

La decisión exacta de cómo se almacenan/resuelven esos calendarios pertenece a D2.

---

# 20. Claims corregidos/rechazados durante esta iteración

| Claim anterior | Disposición final |
| --- | --- |
| ClusterDelta como autoridad de specs/horarios | **REJECTED** — sustituido por CME first-party. |
| “physical Contract” = physically delivered | **REJECTED** — aquí significa expiry-specific tradable/executable identity. |
| `symbolId` ProjectX = economic family ID | **UNSUPPORTED** — sólo se sabe que es distinto de `contractId` y corresponde al contract según docs. |
| `NQZ6` como universal ID | **REJECTED** — códigos/display/IDs dependen de sistema/plataforma. |
| LEAN continuous/mapped = market fact | **REJECTED** — se conserva sólo como PATTERN. |
| continuous future universalmente non-tradable | **REJECTED AS ABSOLUTE** — docs actuales permiten contexts de trading; mapped underlying sigue siendo el patrón útil para live. |
| mapping change migra automáticamente posición | **REJECTED** — LEAN example hace rollover explícito old→new. |
| NQ maintenance 5–6 PM CT | **REJECTED** — CME current first-party publica 4–5 PM CT. |
| CME “ajusta NQ por DST” como claim textual | **NOT CLAIMED** — FACT es CT/ET; fixed UTC prohibition es inference de implementación. |
| expiry como input monetario de MM | **REJECTED** — pertenece a contract lifecycle, no al multiplicador monetario directo. |
| ExchangeSession = ProviderProgram window | **REJECTED** — Topstep demuestra boundary distinto. |
| ExchangeSession = Account DayBoundary | **REJECTED** — son conceptos/autoridades diferentes. |

# 21. Qué quedó suficientemente demostrado

## Q6

Queda suficientemente sustentado para D2:

- Instrument/root y Contract expiry-specific deben poder existir como conceptos distintos.
- El destino final de ejecución puede estar ligado a un `contractId` expiry-specific.
- Mapping/root/continuous identity no debe confundirse con runtime contract identity.
- El hot mapping requerido por Echo puede cambiar para nuevas Operations sin justificar retarget retroactivo.
- Operation→Contract pinning es una **strongly supported inference**.
- Money Management debe recibir specs monetarios del Contract/Instrument y abandonar pips como universal unit.
- lifecycle metadata es distinta de monetary specs.
- IDs externos deben conservar provenance/layer.

`Q6_EVIDENCE = SUFFICIENT`

## Q7

Queda suficientemente sustentado para D2:

- session date puede diferir de civil date;
- timezone authority es semántica y no un fixed UTC offset;
- maintenance breaks forman parte del calendario;
- holidays/early closes overridean el schedule regular;
- product schedules pueden variar;
- ProviderProgram windows/forced-flat son overlays distintos al exchange;
- Account DayBoundary no debe absorber TradingSession;
- deterministic replay/bar bucketing requiere aplicar el mismo calendario/session semantics.

`Q7_EVIDENCE = SUFFICIENT`

# 22. Remaining unknowns — NO bloqueantes para D1

1. **Lifecycle metadata authority:** ProjectX no expone en el Contract payload inspeccionado `expirationAt`, `firstTradeAt` o `lastTradeAt`. D2 debe decidir qué fuente/API será autoridad si V1 necesita esos timestamps.
2. **ProjectX stale-contract close edge:** `partialCloseContract` documenta `ContractNotActive` como error posible. No se investigó exhaustivamente cada variante de cierre después de contract deactivation.
3. **Universal CME trade-date rule:** se demostraron Sunday→Monday y casos holiday concretos, no una única regla textual para todos los productos.
4. **Continuous tradability semantics:** depende del engine/plataforma; no debe formar parte del domain core de Echo.

Ninguno exige otro discovery general para Q6/Q7.

# 23. Decisiones técnicas habilitadas para D2

Front E no resuelve estas decisiones; entrega evidencia para resolverlas:

1. forma exacta de `Instrument`;
2. forma exacta de `Contract`;
3. Contract Resolver / hot mapping;
4. momento exacto de Contract resolution;
5. dónde persistir/pinnear Contract identity;
6. mappings separados feed/execution si aplica;
7. authority/cache de lifecycle metadata;
8. minimum monetary specs contract;
9. forma exacta de `TradingSession`;
10. calendar/ruleset effective version;
11. product/family schedule binding;
12. holiday/early-close override model;
13. ProviderProgram overlay model;
14. relación con Account DayBoundary;
15. integración deterministic session→bar boundaries;
16. behavior explícito si en una iteración futura se implementa rollover automático.

# 24. Owner questions

`NONE`

No apareció un nuevo trade-off de producto que requiera decisión inmediata del owner.

Lo restante es diseño técnico D2 bajo requisitos ya existentes.

# 25. Readiness / handoff

```text
SUBTASK = E_CONTRACT_SESSION_SEMANTICS
STATUS = READY_FOR_PRIMARY_MANAGER_REVIEW

Q6_EVIDENCE = SUFFICIENT
Q7_EVIDENCE = SUFFICIENT

OPERATION_CONTRACT_PINNING = STRONGLY_SUPPORTED_INFERENCE

FRONT_E_RESEARCH = ACCEPTED_WITH_MANAGER_NORMALIZATION
D1 = IN_PROGRESS
```

El Primary Manager debe integrar este recurso con los demás fronts D1. Front E por sí solo **no habilita cerrar D1**.

---

# 26. Fuentes first-party / patrón utilizadas

## CME Group

- Contract trading codes:  
  https://www.cmegroup.com/education/courses/introduction-to-futures/understanding-contract-trading-codes
- E-mini Nasdaq-100 / NQ specs and hours:  
  https://www.cmegroup.com/markets/equities/nasdaq/e-mini-nasdaq-100.timeAndSales.html
- Physical delivery vs cash settlement:  
  https://www.cmegroup.com/education/courses/master-the-trade-futures/expanding-your-futures-knowledge/master-the-trade-physical-delivery-vs-cash-settlement.hideSubnav.educationIframe.html
- Globex trading hours / holiday calendar:  
  https://www.cmegroup.com/trading-hours.html
- CME Globex 2026 electronic-trading notice used for Sunday/trade-date evidence:  
  https://www.cmegroup.com/notices/electronic-trading/2026/04/20260420.html

## ProjectX Gateway

- Search contracts:  
  https://gateway.docs.projectx.com/docs/api-reference/market-data/search-contracts/
- Search contract by ID:  
  https://gateway.docs.projectx.com/docs/api-reference/market-data/search-contracts-by-id/
- Place order:  
  https://gateway.docs.projectx.com/docs/api-reference/order/order-place/
- Search orders:  
  https://gateway.docs.projectx.com/docs/api-reference/order/order-search/
- Realtime API:  
  https://gateway.docs.projectx.com/docs/realtime/
- Partial close edge:  
  https://gateway.docs.projectx.com/docs/api-reference/positions/close-positions-partial/

## QuantConnect LEAN — PATTERN only

- US Futures Security Master / continuous mapping:  
  https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/quantconnect/us-futures-security-master
- Futures data / mapping-change handling:  
  https://www.quantconnect.com/docs/v2/writing-algorithms/securities/asset-classes/futures/handling-data

## Topstep — ProviderProgram overlay

- Trading times / forced flat:  
  https://help.topstep.com/en/articles/8284206-when-and-what-products-can-i-trade
- Holiday trading hours:  
  https://help.topstep.com/en/articles/13350348-topstep-holiday-trading-hours
