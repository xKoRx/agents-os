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

Diseñar con KoR una extensión pequeña del runtime existente. Estado: **CANDIDATO_R2 / DISEÑO_NO_ACEPTADO**. R2 incorpora las decisiones explícitas del segundo turno del Owner del 2026-10-16; las recomendaciones técnicas y las interpretaciones señaladas siguen como propuestas. No representa implementación, autorización de ejecución ni cierre de sesión/proyecto.

Mandato inicial: `Markdown pegado(3).md`, PROMPT_VERSION 1. Sus propuestas se actualizan por las decisiones posteriores del Owner. Producto leído: `xKoRx/echo@0c4aae552176fda005c44766e24dd70e8c48e589`; master revalidado sin delta en el segundo turno. Autoridad del proyecto: [[Echo Futures]]. Carril local: [[TRADESGERARD-CONTROL]] y [[TRADESGERARD-CONSOLIDATION]], sin modificaciones desde este análisis.

## Contenido

### 1. Decisiones Owner y correcciones a R1

| Decisión | Opción acordada | Consecuencia / pendiente real |
|---|---|---|
| Unidad de configuración | Tripleta pool de cuentas + Strategy configurada + MM/configuración. | No asignación manual Strategy/MM a cada cuenta consumible. La cuenta concreta se resuelve en runtime. |
| Concurrencia | Una cuenta por asociación pool–Strategy; varias asociaciones del mismo pool y pools independientes pueden operar simultáneamente. | Se descarta el límite R1 de una cuenta por pool. Un pool con tres asociaciones puede mantener tres cuentas distintas. |
| Exclusividad | Una cuenta no puede operar simultáneamente para dos asociaciones/pools; una cuenta que ya operó con una Strategy no debe pasar automáticamente a otra. | La afinidad después de terminar un turno se precisa en §4 como interpretación conservadora, no queda escondida en un lock temporal. |
| Turno | Persistente entre operaciones, como campañas; rotar por objetivo, pausa o desenlace aplicable tras drenaje. | No round-robin por trade, no rewarmup del mercado ni reproducción de una señal consumida. |
| Orden de selección | Cuenta más antigua primero. | Ordenar por creación real y desempatar por identidad estable; filtrar compatibilidad/disponibilidad antes. No priorizar por rentabilidad. |
| Analytics | Echo calcula indicadores entre barras y consumidores; Strategy y MM los consultan. | Observación causal es el resultado publicado, no el componente que calcula. |
| Cuenta/fase | Strategy y MM deben disponer del contexto de la cuenta; MM diferencia challenge/funded y PoolManager utiliza fase/estado para elegibilidad. | Reglas, fase y economía mantienen una autoridad por hecho; ningún if por nombre de empresa en Strategy. |
| NinjaTrader | Feed y gateway de operaciones exclusivamente. | Sin selección de cuentas, turnos, indicadores de estrategia, MM ni reglas en el AddOn. |
| Primera entrega útil | Pool compartido con varias Strategies/MM y rotación automática, no sólo una asociación fija. | Una cuenta sirve como paso de prueba, no como sustituto del producto pedido. Objetivo Owner: domingo 2026-10-18; no es promesa de plazo. |
| Estrategias iniciales | Se decidirán con resultados de hoy/mañana; K05 con soportes/resistencias es candidato, no selección final. Se esperan nuevos módulos Strategy/MM. | No congelar S2/Gerard ni TG/TGMM como única combinación; no hardcodear tres/cinco en producto. |
| Permisos comerciales de automatización | Fuera de este análisis por instrucción explícita del Owner; los gestiona el Owner. | Se retira la investigación/gate documental R1 de ese asunto. Se mantienen identidad, reglas económicas configuradas y seguridad técnica del envío. |

### 2. AS-IS conservado y delta observado de campañas

**Clasificación:** OBSERVADO_EN_CÓDIGO no significa probado físicamente. Los tests/fixtures históricos se reportan como antecedentes, no ejecutados en este turno. La salud actual de terminal, feed y cuentas es DESCONOCIDA desde esta lectura cloud.

| Recorrido | Evidencia material en el SHA fijado | Delta localizado |
|---|---|---|
| Mercado | `FuturesMarketStreamFn`, keyed por stream, delega canonicalización/dedup/orden/epoch/freshness al SDK. | Reutilizar y validar alimentación/restauración del camino real. |
| Barras e indicadores | `FuturesMarketAnalyticsFn` usa engine compartido; TG tiene kernels en `sdk/futures/analytics/tg`, checkpoint y snapshots por delivery. | Completar demanda y publicación a ambos consumidores, no crear otro motor de indicadores. |
| Strategy y distribución | `Compose` resuelve Strategies[]; `FuturesSignalFanoutFn` linealiza targets AccountStrategy y entrega por owner account:binding. | Separar asociaciones de pool de bindings efectivos; entrega de OPEN sólo a la cuenta seleccionada de cada asociación. No broadcast a todas las cuentas del pool. |
| MM | Compose resuelve un único MM desde cfg.MM. `MMConfigSnapshot` ya permite configuración por cuenta/Strategy. TGMM conserva configuración; estado de ciclo en MMState. | Resolver módulo/config por asociación y fase; pin de configuración por operación. No afirmar contaminación de balances por un singleton no demostrada. |
| Reglas | Provider owner serializado por account_id; `SnapshotViews.EffectiveRuleSet(accountID)` devuelve Provider.RuleSet global. | Resolver RuleSet efectivo según cuenta/programa/fase y binding real; preservar reservas/revalidación account-wide. |
| Ejecución | `Bridge.Run` crea N sesiones; `EchoExecutionAddOn` configura una cuenta y ejecuta sobre resolvedAccount. | Extender routing/observaciones multiaccount del AddOn y wiring del bridge, conservando M2 y correlación. No poner PoolManager en NinjaTrader. |
| Economía y ejecución de vuelta | Operation admite fill/order/quote/economics tipados; bridge tiene journal M2 y reconciliación. | Trazar productor físico y entrega causal; APIs presentes no prueban recorrido físico completo. |
| Campañas | `platformCampaign` contiene accounts[], selected y turnActive. `selectTurn` exige quiescencia para cambiar, conserva selected elegible y luego recorre cuentas elegibles por orden del slice. `purchase` añade al final. | Reutilizar semántica de turno/selección, no copiar el driver financiero completo. El pool compartido añade competencia entre asociaciones ausente del caso de una campaña. |

**Lectura adicional R2:** `v3/backtester/platform_campaign.go`, blob `1bdbd20f4abf9aa89d4044fa77332d2a9801d04f`, símbolos `PlatformCampaignRequest.Validate`, `platformCampaign.selectTurn`, `admitOpportunity`, `checkpoint`, `tickAccount`, `purchase`. Validate requiere una cuenta inicial con un AccountStrategy y el escenario GAU50; el driver también simula compras, pagos y transiciones. Nada de eso se transforma en compras o funding reales por reutilizar su selección.

**Gaps materiales conservados, sin nueva certificación:** (a) MM obtiene TG por `SnapshotViews.AnalyticsView → TGOwnerViewFor → tgPublished`, publicación Go local sin stream en la firma; checkpoint por key no acredita entrega a otra réplica. (b) `readModelMarket.Mark` consulta last, no demuestra bid/ask ejecutable; wiring físico de ExecutableQuoteSource y economía debe trazarse. (c) TGMM `pending`/`ladderCap` usan GAU50InitialBalance=50000 y `NewTGMM` restringe payouts2300/3000; no generalizar esos números a otros programas. (d) D6 físico localizado del 2026-10-05 quedó bloqueado por feed stale y sin órdenes; su interrupción histórica no es un nuevo diagnóstico de producto ni estado actual.

### 3. Modelo R2: pool compartido, asociación persistente, cuenta automática

**PROPUESTA técnica derivada de las decisiones Owner:** mantener el catálogo de cuentas existente y añadir la asociación durable pool–Strategy–MM. El pool sólo agrupa recursos; cada asociación se comporta como una campaña en cuanto a turno, no como un segundo ledger ni como propietario de todas las cuentas.

```text
Pool P: C01, C02, C03, C04, C05 (antiguas primero)
    A = P + Strategy-A@config + MM-A@config  → turno C01
    B = P + Strategy-B@config + MM-B@config  → turno C02
    C = P + Strategy-C@config + MM-C@config  → turno C03
    C04/C05 quedan disponibles para cualquiera de A/B/C compatible

A pausa/drena C01 → A toma C04
B/C mantienen sus cuentas; ninguna opera C01
```

Ejemplo ficticio, no inventario real. Con tres asociaciones y cinco cuentas, como máximo tres cuentas en operación simultánea por esta regla, no cinco ni una. Incorporar dos asociaciones más puede utilizar las restantes si están elegibles. La misma Strategy en otro pool tiene su propia asociación y turno; no reparte cada OPEN entre todas las candidatas.

Una asociación tiene ID estable, pool, referencia de instancia/config de Strategy, referencia de módulo/config MM y control enabled. MM/version son configuración, no parte cambiante de una clave primaria que cree otra asociación al actualizar parámetros. Para I1, una asociación por pareja pool–instancia de Strategy; otro MM simultáneo de la misma Strategy se expresa mediante otro pool, como indicó el Owner.

`AccountStrategy` continúa siendo el binding efectivo consumido por Operation. El runtime lo materializa/reutiliza automáticamente al adjudicar una cuenta; no obliga al Owner a mantenerlos manualmente y no reinventa otra entidad equivalente de cuenta→estrategia. Guarda vínculo a la asociación y la generación de asignación. IDs deterministas/idempotentes permiten restaurar el mismo binding, no duplicarlo al reiniciar.

El alta de una cuenta sigue necesitando su identidad, programa/fase, creación/vencimiento cuando corresponda, economía/pisos y conexión real. El catálogo entrega estos datos; el Owner sólo incorpora la cuenta al pool o usa un criterio de pertenencia explícito existente. No reconfigura Strategy/MM ni parámetros financieros en cada alta.

### 4. Selección, afinidad y concurrencia

**Selección propuesta:** al habilitar una asociación o quedar sin cuenta, solicitar una candidata; mantener turno si sigue elegible. En ausencia de turno, filtrar estado/compatibilidad/fase/destino y afinidad, ordenar por `(account_created_at, account_id)` y reclamar la primera. La fecha es de la cuenta real, no de descubrimiento ni de una sesión de NinjaTrader. FIFO no equivale a vencimiento más cercano: se aplica la prioridad por creación pedida por el Owner, excluyendo cuentas ya vencidas.

**Arbitraje mínimo:** orden durable de recepción de solicitudes; desempate estable en activaciones admitidas como un mismo lote. No optimización, ranking de Strategies ni preasignación manual. Serializar brevemente la adjudicación no serializa la operativa: el PoolManager puede conservar simultáneamente varios turnos, uno por asociación. El owner existente de cuenta valida/rechaza el claim exclusivo global, también cuando dos pools comparten candidatas. Como mínimo, un claim pendiente por asociación y una generación de asignación validada antes de nueva exposición; guardar solicitudes pendientes y respuestas de forma idempotente. Una respuesta tardía de otra generación no autoriza órdenes. No TTL que libere una cuenta incierta, ni transacción cross-key inventada.

**Interpretación propuesta explícita de “una vez que una estrategia opera una cuenta ninguna otra debería poder operarla”:** separar afinidad de cuenta y turno activo. Cuando empieza un intento real de operación, fijar afinidad a la asociación pool–Strategy; conservarla al pausar y al rotar. Una cuenta recuperada vuelve a ser candidata sólo para su asociación, no para otra Strategy. La reclamación provisional anterior a toda orden puede liberarse cuando está probado que no produjo efectos; un envío incierto ya retiene identidad/claim. No hay mecanismo de reasignación automática de afinidad en I1. Esta interpretación estricta no se presenta como una decisión adicional confirmada por el Owner.

Una cuenta temporalmente pausada puede seguir retenida por afinidad, mientras otra de esa misma asociación mantiene el turno activo. Al reabrir la primera no se interrumpe un turno vigente elegible: FIFO se aplica a la siguiente selección. Esto evita tanto robar cuentas como rotaciones sorpresivas al cambiar el día.

| Situación | Acción propuesta |
|---|---|
| Objetivo/pausa diaria | Bloquear nueva exposición según política, gestionar/drenar órdenes y posición; terminar turno después de confirmar drenaje. Cuenta pausada con condición de reanudación. |
| Inoperabilidad económica permanente / desenlace terminal | Excluir de nuevas selecciones con causa; conservar historia/identidades. La asociación pide otra cuenta. |
| Funding/review/pago pendientes | Cuenta no elegible según estado; no inferir transición real por PnL. Confirmación real habilita contexto/fase posteriores. |
| Setup rechazado, quote temporalmente inválida o indicador no listo | Rechazo de oportunidad o suspensión acotada, no jubilación permanente de la cuenta por defecto. |
| Orden o exposición incierta | Conservar claim/turno bloqueado de esa asociación hasta reconciliar; otros turnos independientes continúan. |
| Sin candidatas | Asociación sin cuenta con motivo y reintento de selección ante cambios relevantes; ninguna compra ni cola de señales caducadas. |

El paso de C01 a C04 nunca migra posición, órdenes, PnL ni MMState financiero. Una nueva señal posterior puede usar C04; gestiones/fills de C01 siempre se resuelven por su identidad original. El MM decide sizing/SL/TP/reducciones/adds que implemente; Provider conserva los límites obligatorios. PoolManager selecciona, bloquea entradas y espera resultado de drenaje, sin calcular cierres ni enviar directamente órdenes. Una parada operativa que exija cerrar invoca el mecanismo existente de intención de cierre/seguridad; no redefine cada pausa como flatten implícito.

### 5. Barras → indicadores → observaciones para Strategy y MM

```text
NinjaTrader: feed observado
  → mercado canónico / orden / epochs
  → barras compartidas
  → analytics: kernels incrementales de indicadores requeridos
  → observaciones versionadas y causales
       ├─ Strategy de asociación: señal y estado técnico
       └─ MM de cuenta/operación: gestión según sus triggers
  → Operation / Provider → bridge → gateway NinjaTrader
  ← quotes, órdenes, fills, posiciones y economía por cuenta
```

Calculador y publicación son responsabilidades distintas, aunque puedan vivir en el mismo owner `market_analytics`. Strategy/MM declaran dependencias y leen resultados: no contienen kernels. Reutilizar el motor actual y compartir cálculos por stream/contrato/timeframe/parámetros/calendario/seed/epoch/versión efectiva. El siguiente módulo real determina nuevos indicadores necesarios; no imponer TG como API universal ni crear una DSL.

Backtest prepara/consulta tablas causales; runtime avanza los mismos kernels incrementalmente. Ambas rutas conservan disponibilidad temporal y orden same-instant. Quote cambia aunque el último indicador de barra cerrada no cambie: MM puede gestionar sin esperar una señal nueva.

**Contexto de cuenta:** read-only para los dos consumidores cuando lo necesiten, con identidad, programa/fase, referencias a reglas, economía y generación del turno disponibles causalmente. Strategy no elige otra cuenta ni asume cálculo de riesgo por recibir contexto. Si ese contexto afecta su decisión o estado, su instancia lógica debe aislarse por asociación. Compartir código e indicadores no permite compartir ciegamente una sola ejecución/OwnerState entre dos pools con economías distintas. Mantener el estado técnico/mercado al rotar; contexto y estado monetario permanecen por cuenta/operación. Un cambio de cuenta es un hecho explícito, no un reset global de Strategy.

Distribución requerida: observaciones/referencias resolubles mediante mensajes/estado existente de StateFun, no lectura de un puntero local como garantía de producción. Cada consumidor debe poder identificar el corte servido y rechazar ausencia con motivo; no recalcular el indicador para cubrir un hueco de transporte.

### 6. Programas y challenge/funded: tres responsabilidades

**Cuenta/Provider:** fuente de programa, fase, límites, términos y estado económico reales. Resolver reglas por referencia/version efectiva, nunca desde el único Provider global para cuentas heterogéneas. El pool puede mezclar programas si los contratos requeridos están soportados y la asociación es compatible.

**MM de la asociación:** un módulo con configuración/contexto por fase; decide cómo operar challenge frente a funded. Recibe objetivos, progreso, margen y términos aplicables. No necesita una clase por empresa ni overrides manuales por cuenta. Quitar las constantes GAU50 sólo donde el nuevo programa las ejercite, reemplazándolas por datos de la autoridad existente; no copiar una segunda fórmula.

**PoolManager:** utiliza fase/estado y resultado de operabilidad para seleccionar, pausar o rotar. No calcula drawdown ni determina por sí mismo un pase/payout. El rechazo de un setup no significa que ningún setup futuro sea ejecutable; distinguir denegación local de incapacidad permanente. Políticas internas de turno pertenecen a la asociación, con el pool como inventario; no duplicar la fase de cuenta en otra autoridad editable.

Configuración nueva de MM aplica a próximas operaciones; operación abierta conserva módulo/config y presupuesto aplicables. Las actualizaciones efectivas de seguridad del Provider siguen reevaluándose. Tras funding confirmado en flat se resuelve el perfil funded. Si hay operaciones vivas durante un cambio de fase/config, bloquear nuevas entradas y procesar la transición de contexto sin reemplazar el MM de una operación en caliente.

### 7. Cambios implementables y primera aceptación funcional

| Bloque | Propietarios afectados | Cambio necesario y prueba |
|---|---|---|
| Configuración | Catálogo/config Views + runtime composition | Asociaciones pool–Strategy–MM; binding AccountStrategy automático; RuleSet por cuenta/programa/fase; IDs estables. Añadir una cuenta no exige configurar Strategy/MM y actualizar MM no crea otro turno. |
| Turnos compartidos | Pequeño owner PoolManager en Core + owner de cuenta existente | Turnos por asociación, FIFO elegible, claim/generación/idempotencia y afinidad propuesta. Tres asociaciones/cinco cuentas toman tres distintas; una rota sin mover las otras; pools solapados no duplican claim. |
| Dominio reutilizable | SDK de selección/operabilidad que se extraiga sólo donde encaje + adaptador de campaña | Extraer lógica pura mínima de turno/selección, sin importar cashBook ni driver de simulación en Core. Fixture de la campaña actual conserva turno, orden y drenaje; no reejecutar las40. |
| Strategy/MM/Provider | Owners existentes + factories/View/contexto | MM por asociación/fase, contexto causal de cuenta y estado de Strategy aislado cuando corresponda, economía/quote por cuenta. Dos programas y dos MM distintos no comparten estado; nueva Strategy no modifica scheduler/bridge. |
| Analytics | market_analytics + serving de Strategy/Operation | Reutilizar kernels, demanda y publicación causal a ambos consumidores, incluida otra réplica/restart. H1/SR y quotes reales cubiertos por los datos requeridos. |
| Ejecución | Bridge/adaptador/ExecutionAddOn | Multiplexar comandos y hechos por cuenta/contrato con M2 independiente. Probar dos cuentas simultáneas, fill tardío, ACK perdido, cancelación y reconexión sin cruces ni duplicados. |

Estos son bloques de cambio, no seis servicios ni un calendario de shots. Lo nuevo central es asignación/turnos; las dependencias de analytics, economía y routing físico existen como gaps independientemente del pool. La primera entrega útil debe demostrar pool compartido y módulos intercambiables. La prueba empieza por una cuenta para localizar fallos y luego ejercita concurrencia/rotación: no se declara terminado al pasar únicamente la primera cuenta.

**Suite pequeña propuesta:** tres asociaciones/cinco cuentas; empate por creación; incompatibilidad de una candidata sin bloquear las otras; pausa y rotación en la misma sesión; recuperación de pausada sin robo ni preemption; invariantes de cuenta única incluso en pools solapados; rechazo de generaciones viejas; reinicio/ACK incierto/fill tardío; profiles challenge/funded; Strategy/MM en consumidores distintos; indicadores compartidos sin estado monetario compartido; alta de nueva cuenta sin binding manual. Verificar caminos críticos antes de cobertura numérica; no declarar PASS por mera existencia del fixture.

**Diferido:** MM arbitrario por cuenta, varias Strategies dentro de una misma cuenta, dos cuentas simultáneas de una asociación, optimizador/asignación por rendimiento, presupuesto/hedging/netting de portfolio entre cuentas, UI nueva, más adaptadores, nuevas modalidades de gestión de exposición ajenas a los MM elegidos. La misma Strategy en pools distintos sí pertenece al modelo actual.

### 8. Límites de la asociación y continuidad

`1 campaña–1 Strategy–N cuentas` representa bien el consumo secuencial individual. No representa por sí sola tres campañas compitiendo por un catálogo común: falta la adjudicación compartida. R2 conserva la campaña como analogía de asociación/turno y agrega el pool como inventario compartido, sin copiar el controlador financiero offline.

Una cuenta es consumible comercialmente, no una identidad desechable: excluirla del pool no elimina journal/fills/economía ni permite aceptar comandos viejos contra otra cuenta. No se persigue proteger indefinidamente cuentas inoperables; se clasifica el desenlace y se rota.

Pendientes reales: parámetros y módulos ganadores los resolverá el Owner; alcance técnico exacto del transporte de contexto/analytics distribuido, wiring económico/quote, registration/dispatch de múltiples instancias y protocolo multiaccount deben cerrarse al escribir el contrato técnico. Afinidad persistente entre turnos y orden determinista de adjudicación son propuestas R2 explícitas; no fingir aprobación final. No volver a preguntar concurrencia, turno, FIFO ni gateway-only ya confirmados.

La autoridad Environment Contract no se recuperó en R1; no se deduce ausencia y no hubo infraestructura. Antes de un handoff que emita instrucciones de operación se debe resolver esa autoridad, sin reiniciar ahora discovery general. No se ejecutó producto, campañas, scripts, despliegues ni órdenes en R2. No se genera prompt LOCAL, no se despachan agentes y no se cierra sesión.

## Fuentes

### Source de producto en xKoRx/echo@0c4aae552176fda005c44766e24dd70e8c48e589

- `v3/backtester/platform_campaign.go`: PlatformCampaignRequest.Validate, selectTurn, admitOpportunity, checkpoint, tickAccount, purchase; blob `1bdbd20f4abf9aa89d4044fa77332d2a9801d04f`. Lectura adicional R2.
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
- `v3/futures-bridge/README.md`: M2 semantics y documentación histórica D5; blob `350166d5ba49c6c55f61c417306c61272c014dae`.
- `v3/backtester/tools/tradesgerard/TG-FLOW.md`: kernels, consumidores y completitud; blob `112243641564d372ac0725263f0451ab11365814`.

### Autoridades documentales

- [[10-projects/Echo Futures/Echo Futures|Echo Futures]].
- [[10-projects/Echo Futures/artifacts/tradesgerard/TRADESGERARD-CONTROL|TRADESGERARD-CONTROL]] y [[10-projects/Echo Futures/artifacts/tradesgerard/TRADESGERARD-CONSOLIDATION|TRADESGERARD-CONSOLIDATION]], secciones vigentes consultadas del 2026-10-16.
- [[10-projects/Echo Futures/artifacts/d6-final-physical-certification-20261005/D6-FINAL-PHYSICAL-CERTIFICATION|D6 Final Physical Certification 2026-10-05]], blob `6fd72dceb517a730647c5dec27dc714bbb55797c`, sólo evidencia histórica.
- Mandato inicial adjunto y decisiones explícitas del segundo turno del Owner del 2026-10-16; R2 prevalece sobre las propuestas R1 contradichas. Se retiran de este documento operativo las fuentes de permisos comerciales excluidas por el Owner; la versión anterior permanece en Git.
- Apache Flink, `Monitoring and Controlling Networks of IoT Devices with Flink Stateful Functions`, 2020-08-18: invocaciones serializables por dirección. Apache Flink, `Logical Functions`: direcciones e independencia de estado lógico. Consulta 2026-10-16; fundamento del uso de owners existentes, no prueba del wiring de Echo.
