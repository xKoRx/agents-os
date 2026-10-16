---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases:
  - "Echo Futures Runtime Pool Design"
tags:
  - kind/doc
created: "2026-10-16"
updated: "2026-10-16"
---

# ECHO FUTURES — Runtime multiestrategia / multiprop

## Propósito

Diseñar con KoR una extensión pequeña del runtime existente. Estado del diseño: **CANDIDATO_INICIAL / NO_ACEPTADO**. La nota está activa como documento de trabajo; no representa aceptación de arquitectura, autorización LIVE, implementación ni cierre de sesión.

Mandato Owner: `Markdown pegado(3).md`, PROMPT_VERSION 1, 2026-10-16. Producto leído: `xKoRx/echo@0c4aae552176fda005c44766e24dd70e8c48e589`, master resuelto y vuelto a comprobar en esta recepción. Autoridad del proyecto: [[Echo Futures]]. Carril local: [[TRADESGERARD-CONTROL]] y [[TRADESGERARD-CONSOLIDATION]]. No se modificaron producto, campañas ni esos controles.

## Contenido

### 1. Autoridades y alcance

- **CONFIRMADO_OWNER:** dominio único runtime/backtest; NinjaTrader como primer adaptador; Strategy y MM consumen observaciones causales; mercado compartido y economía aislada; Futures-first; no LLM en trading; no implementación ni operación desde este carril.
- **OBSERVADO_EN_CÓDIGO:** hechos de los símbolos citados abajo en el SHA fijado. No equivalen a despliegue o ejecución física.
- **PROBADO_EN_FIXTURE:** únicamente lo reportado por los artefactos de consolidación consultados; no se ejecutaron ni se revalidaron suites en esta sesión.
- **PROBADO_FÍSICAMENTE:** se utiliza evidencia histórica fechada y acotada, no una inspección actual del terminal.
- **PROPUESTA:** todo modelo, tarea y decisión inicial de esta nota, pendiente de aceptación del Owner.
- **DESCONOCIDO:** disponibilidad actual de cuentas/feed, recorrido físico completo de economía/quote, transporte distribuido suficiente para MM y permisos comerciales específicos no recuperados.

La consolidación del 16 de octubre ya publica cierre del backtester para iteración offline y explica la ausencia de operability_policy en el intento anterior. No se usa ese resultado para certificar runtime ni se reabre la campaña. Hay documentación histórica rezagada: el README del bridge se declara D5/SIM, aunque el source actual contiene adaptador y AddOn NinjaTrader; sus límites históricos no describen por sí solos el HEAD.

### 2. AS-IS y delta localizado

| Recorrido | Evidencia material | Dictamen inicial |
|---|---|---|
| Cuenta/conexión | D6 2026-10-05 resuelve `E2T-GAU50-01` contra la cuenta provider cuyo sufijo es 1551 y NT Account.Id `3`. El AddOn usa nombre provider como identidad de negocio y el ID como hint de sesión. | Reutilizar alta explícita; revalidar identidad, conexión, fase y economía en la futura prueba. No descubrir/comprar cuentas por inferencia. |
| Feed y autoridad | `FuturesMarketStreamFn` es keyed por stream; delega canonicalización, dedup, secuencia, epoch y freshness al engine SDK de market. | Reutilizar. Validar feed vivo y recuperación; heartbeat del transporte no basta. |
| Barras/analytics | `FuturesMarketAnalyticsFn` usa engine compartido; TG persiste checkpoint por key y transporta snapshot en BarClosedDelivery. H1/SR live tienen límites de completitud documentados. | Reutilizar kernels/checkpoint. Completar/validar datos causales de arranque y reconexión, sólo para indicadores requeridos. |
| Strategy/fanout | `Compose` resuelve Strategies[]; `FuturesSignalFanoutFn.handleSignal` linealiza targets AccountStrategy y entrega por owner account:binding. | Reutilizar. El fanout existente es distribución, no selección de una cuenta de un pool. |
| MM | Compose resuelve un único MM. `MMConfigSnapshot(account,strategy)` ya permite config por binding. TG Manager mantiene config y usa MMState de operación; no se ha observado aquí un singleton mutable de balances. | Extender resolución/versionado por binding al necesitar distintos MM/configs en una composición. No clonar el proceso. |
| Reglas/riesgo | Provider owner es serializado por account_id. Pero `SnapshotViews.EffectiveRuleSet(accountID)` devuelve el Provider.RuleSet global. | Reutilizar provider engine/reservas; resolver regla efectiva por binding de cuenta/programa/fase. No confundir owner aislado con reglas heterogéneas ya conectadas. |
| Egress físico | `Bridge.Run` crea N sesiones por cuenta. `EchoExecutionAddOn.ExecuteCommand` sólo opera `resolvedAccount` y rechaza provider_ref distinta de expectedAccountName. | Primera cuenta: reutilizar. Pool físico: extender allowlist/routing/subscripciones y protocolo de sesión, preservando M2 por cuenta. No cambiar un puntero global de cuenta mientras quedan órdenes. |
| ACK/fill/acciones | Operation tiene ingress de fills/órdenes y actualizaciones tipadas de quote/economía. Bridge dispone de journal PREPARED/SUBMITTING/BOUND/AMBIGUOUS, reconciliación e identidades por cuenta. | Reutilizar contratos; probar recorrido físico y pérdida de ACK. No deducir exactly-once físico de checkpoint Core. |
| Turnos | El fanout inspeccionado mantiene targets/dedup, no una política de rotación. El turno de campaña pertenece a aquella simulación. | Añadir únicamente selección/turno de runtime acordado, reutilizando criterios puros que encajen, sin compras ni cobros simulados. |

**Límite de una cuenta:** se localiza de forma concreta en el AddOn/config/protocolo de esa integración. No es un límite global del shell Bridge ni prueba de que todo Core sea ya multiprop. NinjaTrader expone Account.All y métodos por cuenta; eso permite plantear el delta de adaptador, no certifica nuestro routing físico.

**Límites adicionales que importan:**

1. `SnapshotViews.AnalyticsView → TGOwnerViewFor` consulta `tgPublished`, un puntero local sin identidad de stream en la firma. La persistencia de checkpoint por key y el transporte de snapshots hacia Strategy no acreditan que MM en otra réplica consulte la publicación correcta. Propuesta: entregar/publicar una observación inmutable acotada por el transporte existente de StateFun, con identidad de stream/epoch/versión y frontera causal; no introducir un bus/RPC nuevo ni recalcular indicadores por cuenta.
2. `SnapshotViews` no implementa en el archivo inspeccionado ExecutableQuoteSource; Market.Mark lee last. La conexión exacta de bid/ask ejecutable y economía account-wide fresca queda por completar/verificar, no declarada inexistente en todo el repo. No sustituirla por last ni offsets OHLC.
3. `tgmm.pending` y `ladderCap` restan GAU50InitialBalance=50000; `config.NewTGMM` restringe payout a 2300/3000. Son límites del escenario actual. Antes de extenderlo a otros programas, utilizar referencias económicas reales explícitas y objetivos versionados sin duplicar fórmulas. La referencia de progreso no se reinicia al arrancar proceso/cambiar turno y no se infiere de una demo.
4. La última certificación física localizada, 2026-10-05, quedó ENVIRONMENTAL_BLOCKED por feed stale y con cero submits/fills. Certificaciones de transporte/reportes de fixtures no completan el ladder físico pendiente. La salud actual no se conoce desde esta sesión cloud.

### 3. Modelo candidato

No elegir entre una cuenta que contiene código de Strategy y una Strategy propietaria de balances: definición reusable + instancia configurada + AccountStrategy existente + cuenta real. Un pool es una lista declarada de candidatas; no posee saldo.

```text
Market compartido por identidad/cálculo
    ├─ Strategy TG@versión → instancia TG-NQ
    └─ Strategy S2@versión → instancia S2-NQ
                         ↓ asociaciones explícitas
        pool A [A-01,A-02]      pool B [B-01,B-02]
               ↓ turno                ↓ turno
        AccountStrategy         AccountStrategy
        Strategy + MM@versión + ExecutionAccount
                                  ↓
            Provider/Program/fase → RuleSet efectivo
            Connection/Adapter → locator físico cuenta/contrato
                                  ↓
                  Operation → provider → M1/M2 → AddOn
```

Ejemplo **enteramente ficticio**, sin cuentas ni permisos inferidos:

| Binding | Instancia | MM/config | Cuenta | Programa |
|---|---|---|---|---|
| BA1 | TG-NQ | TGMM-config-A@1 | A-01 | Empresa A / Programa A |
| BA2 | TG-NQ | TGMM-config-A2@1 | A-02 | Empresa A / Programa A |
| BB1 | S2-NQ | Gerard-config-B@1 | B-01 | Empresa B / Programa B |
| BB2 | S2-NQ | Gerard-config-B@1 | B-02 | Empresa B / Programa B |

Pool A puede mantener A-01/TG mientras pool B mantiene B-01/S2, sólo si los scopes de concurrencia y compatibilidades lo permiten. La misma instancia Strategy puede asociarse explícitamente a otro pool mediante bindings adicionales; no se duplica su cálculo. Más de un binding por cuenta sigue representable aunque la primera entrega proponga exclusividad de turno.

**Dos serializaciones distintas:** el turno debe tener autoridad persistente por scope de selección (inicialmente pool); el owner provider existente arbitra la reclamación de cada cuenta. Un lock por cuenta no evita que dos candidatos diferentes sean activados a la vez dentro de un pool limitado a uno. La extensión de asignación dentro de Core necesita esa clave única de turno, reutilizando StateFun, sin otro servicio ni ledger. Dos pools que comparten cuenta deben obtener el mismo claim account-wide. Un límite común de programa/prop no puede eludirse dividiéndolo en varios pools: comparte scope de turno o la configuración se rechaza hasta soportarlo explícitamente. La política histórica E2T de una cuenta activa no se convierte en mutex de todo Echo.

El claim/version de asignación se valida junto con reservas/admisión y ReservationRevalidate, no mediante un mapa previo a enviar. Ningún TTL libera cuentas con órdenes inciertas. Las gestiones de una Operation conservan su cuenta/contrato original aunque cambie la lista del pool.

### 4. Secuencia mínima propuesta

```text
señal S1 nueva → turno A-01 → binding BA1 → MM/admisión → orden/fills
A-01 llega a pausa → impedir entradas y entrar en drenaje
órdenes/exposición/incertidumbre reconciliadas → liberar turno
señal S2 posterior, misma sesión → turno A-02 → binding BA2
```

S1 permanece consumida; no reiniciar mercado ni enviarla a A-02. Si el ACK se pierde tras SUBMITTING, conservar identidad y estado incierto, consultar/reconciliar usando M2 y seguir atendiendo fills tardíos. No liberar por timeout ni reintentar a ciegas. Intervención manual no reconocida: pausa/exclusión de nueva exposición y reconciliación explícita, no coexistencia automática implícita. Deshabilitar entradas, drenar y flatten autorizado son acciones distintas.

Congelar módulo/config de MM y presupuesto de la operación al abrirla. Una configuración nueva se aplica a próximas operaciones; restricciones oficiales de seguridad efectivas se reevalúan de inmediato por provider y no quedan desactivadas por la versión de entrada. Mantener separadas la configuración fijada y la regla efectiva observada.

### 5. Primera porción útil y pruebas posteriores

| Paso propuesto | Delta implementable | Prueba de aceptación |
|---|---|---|
| Una asociación fija | Conectar Strategy/MM elegidos a una cuenta explícita del adaptador existente; resolver feed, analytics para ambos consumidores, quote y economía reales. No pool requerido. | Fixture de causalidad/restart y ejecución en SIM/demo autorizada: cuenta/contrato, entrada, protección, fill, cancelación y reconexión sin duplicados. Shadow por sí solo no acredita órdenes. |
| Pool mínimo de dos candidatas del mismo programa | Turno persistente/claim account-wide y routing físico multiaccount con sesiones/identidades separadas; ninguna compra ni reset automático. | A-01 pausa y A-02 toma una señal posterior en la misma sesión; atraso de ACK/fill retiene A-01; reinicio no pierde turno ni ejecuta señales anteriores. |
| Segundo boundary | Resolver MM/config por binding, RuleSet por programa/fase y quitar dependencias económicas GAU50 cuando el nuevo caso las ejercite. Incorporar segunda Strategy y luego programa concreto sólo si necesario. | Misma señal/config kernel, dos bindings con MM distintos y dos RuleSets distintos sin contaminar estado; pools independientes concurrentes; incompatibilidad de B no bloquea A. |

Cada oportunidad debe dejar causa trazable: analytics no disponible, señal descartada, binding incompatible, turno ocupado, provider denegado, orden rechazada, orden incierta o fill. No exigir rentabilidad ni 200 cuentas para aceptar el recorrido técnico.

### 6. Permiso comercial y hechos actuales

El Help Center E2T consultado el 2026-10-16 permite varias evaluaciones y prohíbe trade copiers; la recomendación de operar una cuenta no debe presentarse como prohibición universal de multicuenta. No se recuperó una autorización first-party específica para la automatización de Echo: los términos incluyen restricciones generales a bots/acceso automatizado y software que pueda manipular el entorno. Estado de esa compatibilidad: **PENDIENTE_DE_EVIDENCIA**, no permiso presumido ni prohibición inventada. El `entitlement=ALLOWED` documentado en ETCD para D6 no es por sí mismo fuente contractual. Esto limita el armado comercial de E2T, no el diseño ni la prueba en un entorno SIM autorizado. Llamar fanout a la ejecución independiente no concede una excepción al copier policy.

### 7. Decisiones pendientes del Owner

| Decisión | Opción recomendada, aún no acordada | Consecuencia |
|---|---|---|
| Destino de una misma señal | Una cuenta por cada pool expresamente asociado y autorizado, no todas las cuentas ni una global accidental. | Permite programas/pools independientes concurrentes; conserva el scope E2T limitado. |
| Uso inicial de cada cuenta | Un solo binding Strategy/MM propietario durante el turno persistente, sin borrar la cardinalidad multibinding futura. | Reduce arbitraje/gestión concurrente inicial sin rediseñar el dominio. |
| Combinación de primera prueba | TG + TGMM en SIM/demo como integración del camino actual; S2 + GerardMM es alternativa si el Owner prioriza retomar el D6 anterior. | TG ejercita ahora las nuevas dependencias de analytics/economía; no implica escoger estrategia rentable ni heredar importes del backtest. |

No hay aceptación de estas opciones todavía. No se genera prompt LOCAL ni se despachan implementadores. El siguiente turno actualiza esta tabla por delta y resuelve el diseño técnico derivado, sin repetir bootstrap ni auditoría histórica.

### 8. Continuidad y límites de la recepción

Se inspeccionaron los owners/contratos aquí citados, no todo el repo ni el deployment vivo. Quedan por trazar al detalle antes de un handoff: registration/dispatch de producción multikey, productor físico de economía y quote, selección causal multi-réplica de analytics, y protocolo NT multiprop/multiaccount completo. La localización del Environment Contract de Echo/Forge por búsqueda no produjo una fuente utilizable; no se deduce su ausencia. Ninguna operación de infraestructura depende de esa laguna porque no se ejecutó infraestructura.

Releer únicamente los diffs pertinentes de master antes de implementar. Las nuevas decisiones se incorporan aquí; el catálogo de cuentas y control de campañas siguen en sus autoridades existentes. No se cierra sesión ni se registra feedback de cierre.

## Fuentes

### Source de producto, todo en xKoRx/echo@0c4aae552176fda005c44766e24dd70e8c48e589

- `v3/core/internal/futuresruntime/runtime.go`: Compose, WithTGAnalyticsOwner, BridgeCommandEnvelope; blob `f4fdefe7a1efb7fb29fb7593e708e86a2be321e0`.
- `v3/sdk/futures/config/snapshot.go`: ConfigSnapshot, StrategyDef, AccountDef; blob `89c1bf67580555914bdf05f4275d1e2fdb607d92`.
- `v3/sdk/futures/config/views.go`: EffectiveRuleSet, MMConfigSnapshot, AnalyticsView, AccountEconomics, readModelMarket.Mark; blob `3670051e354c3f61e3389ec06691beeb606640de`.
- `v3/sdk/futures/config/composition.go`: ResolveStrategy, ResolveMoneyManager; blob `181b525166c76bebe00a53c62f7748915f6d186b`.
- `v3/sdk/futures/config/tgmm.go`: NewTGMM; blob `4097a5b17093ef39153d596a987ffb43e6a63b4b`.
- `v3/sdk/futures/strategies/tgmm/tgmm.go`: Manager.Evaluate, pending, ladderCap; blob `67016482c344ebae4e7d12d996bf834f91611893`.
- `v3/core/internal/functions/futures_market_stream.go`: FuturesMarketStreamFn; blob `08ccb58b4d3a0021e5adb58abcd5574d65bf06dc`.
- `v3/core/internal/functions/futures_market_analytics.go`: tgIngestAll, TGOwnerViewFor; blob `064824c5631d53265907c2a7d0fbe19339c88174`.
- `v3/core/internal/functions/futures_signal_fanout.go`: handleSignal, handleTargetSet; blob `0201175340f4427875daff372de7cc4aa79b225f`.
- `v3/core/internal/functions/futures_operation.go`: Invoke, typed ingress; blob `7605f4aaff9d54ed9a56cb7fd15827400b8cb78c`.
- `v3/core/internal/functions/futures_provider_rules.go`: Invoke/account owner; blob `e4361f331c511b9f8b5e2caa328e9621b12055c0`.
- `v3/futures-bridge/core/bridge.go`: Bridge.Run; blob `17874301ffd9296a2426806ff5b9c5188904756b`.
- `v3/futures-bridge/addon-ninjatrader/EchoExecutionAddOn.cs`: LoadConfig, ExecuteCommand, ExecuteSubmit; blob `dedd6dcdd14abefee00f087ff23e574ca3cdfd3f`.
- `v3/futures-bridge/README.md`: M2 semantics, documentation drift; blob `350166d5ba49c6c55f61c417306c61272c014dae`.
- `v3/backtester/tools/tradesgerard/TG-FLOW.md`: consumers, completeness, preset; blob `112243641564d372ac0725263f0451ab11365814`.

### Autoridades documentales

- [[10-projects/Echo Futures/Echo Futures|Echo Futures]].
- [[10-projects/Echo Futures/artifacts/tradesgerard/TRADESGERARD-CONTROL|TRADESGERARD-CONTROL]] y [[10-projects/Echo Futures/artifacts/tradesgerard/TRADESGERARD-CONSOLIDATION|TRADESGERARD-CONSOLIDATION]], secciones vigentes del 2026-10-16.
- [[10-projects/Echo Futures/artifacts/d6-final-physical-certification-20261005/D6-FINAL-PHYSICAL-CERTIFICATION|D6 Final Physical Certification 2026-10-05]], blob `6fd72dceb517a730647c5dec27dc714bbb55797c`.
- [E2T: múltiples cuentas](https://help.earn2trade.com/en/articles/5660666-can-i-have-multiple-trader-career-path-gauntlet-mini-and-live-livesim-accounts), consulta 2026-10-16.
- [E2T: trade copiers](https://help.earn2trade.com/en/articles/12034590-am-i-allowed-to-copy-trades-across-multiple-accounts), consulta 2026-10-16.
- [E2T: términos](https://www.earn2trade.com/terms-and-conditions), consulta 2026-10-16.
- [NinjaTrader: Account](https://ninjatrader.com/support/helpGuides/nt8/account_class.htm) y [Account.All](https://ninjatrader.com/support/helpguides/nt8/all.htm), consulta 2026-10-16.
