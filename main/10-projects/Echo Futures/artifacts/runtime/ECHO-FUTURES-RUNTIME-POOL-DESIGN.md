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

**CANDIDATO_R5 / LISTO_PARA_REVISIÓN_DEL_OWNER.** Diseño de asignación y ejecución sobre Echo existente. R5 corrige un error del asistente en R4: una pausa por daily DD o daily target SÍ termina el turno de esa cuenta y activa otra para la MISMA Strategy en la MISMA sesión. Al siguiente día operativo se vuelve a la cuenta elegible más antigua ya asignada a esa Strategy. Afinidad permanente NO significa retención del turno durante una pausa. La aceptación del diseño corresponde al Owner; esta nota no declara implementación, pruebas ejecutadas, despliegue ni cierre de sesión/proyecto.

Mandato inicial: `Markdown pegado(3).md`, PROMPT_VERSION 1, actualizado por los turnos posteriores. Autoridad: [[Echo Futures]]. Runtime se implementará en su rama de producto; backtester seguirá investigando/validando en otra y adoptará los cambios gradualmente después. No se exige sincronización inmediata para avanzar. Agents-OS continúa sobre master, sin ramas ni PRs para esta documentación.

**Cortes de evidencia:** última lectura de producto en R4: `xKoRx/echo@95e9d105182af99d03700f4b5def24bf9fc6b5fd`. Se conservan las lecturas R1–R4 de Signal, fanout, arquitectura, composición, owners, MM y bridge. R5 sólo incorpora la aclaración explícita del Owner y corrige documentación; no nueva inspección de producto/WIP/infraestructura ni modificación de [[TRADESGERARD-CONTROL]] o [[TRADESGERARD-CONSOLIDATION]].

## Contenido

### 1. Decisiones de producto vigentes

| Decisión | Opción confirmada | Consecuencia |
|---|---|---|
| Unidad configurable | Pool + Strategy configurada + MM/configuración. | AccountStrategy efectivo automático; no asignación manual de Strategy/MM por cuenta consumible. |
| Concurrencia | Una cuenta activa por asociación; varias asociaciones de un pool y pools independientes simultáneos. | No mutex de trading por pool ni del sistema. |
| Afinidad permanente | Cuenta que operó A seguirá con A, aunque pasen días; nunca B. | Conserva asociación de origen durante pausa, rotación, recuperación y reinicio. Una Strategy puede acumular varias cuentas propias, con sólo una activa por asociación. |
| Turno intradía | Conservar la cuenta entre trades mientras esté operable; al daily DD/daily target, pausar esa cuenta y continuar con la siguiente elegible para ESA Strategy. | Rotar en la misma sesión tras drenaje, sin esperar al día siguiente y sin pausar la Strategy. También rotar por pérdida/pase u otro desenlace que retire la cuenta de la ejecución actual. |
| Reinicio diario | Al siguiente día operativo volver a la cuenta elegible más antigua ya asignada a la Strategy; recorrer de nuevo sus cuentas según se vayan pausando. | Sustituye expresamente la retención R4 y la no-preemption diaria R2/R3. No mantener por inercia la última cuenta del día anterior. El cambio de destino respeta órdenes/exposición pendientes. |
| Selección | Antiguas primero, respetando elegibilidad y afinidad. | Usar cuentas propias elegibles; cuando no queden, reclamar la libre compatible más antigua del pool. Nunca una asignada a otra Strategy. |
| Strategy | Agnóstica a cuenta, MM y pool; produce Signal y lleva su ciclo técnico. | Nunca se pausa por el estado de una cuenta. Sigue evaluando sus triggers y emitiendo señales independientemente de qué cuenta replica. |
| MM | Contexto real de cuenta, programa/fase, economía e indicadores. | Sizing y gestión propios; diferencia challenge/funded sin trasladar economía a Strategy. |
| Indicadores | Calculados en analytics de Echo y publicados a Strategy y MM. | Consumidores sin kernels propios; analytics no se congela por pausas de cuentas. |
| Remanente | Presupuesto operativo completo aunque supere el remanente positivo al piso. | No recorte, rechazo o retiro anticipado sólo por esa comparación; el breach real conserva su tratamiento. |
| Cohorte | Soportar las cinco cuentas existentes y la composición/rotación pedidas. | No obligación de cinco trades, señales forzadas ni pools extra para garantizar utilización. |
| Desarrollo | Runtime en su rama; backtester en otra, sin detenerlo. | Adaptación progresiva posterior; divergencia temporal identificada no bloquea el avance. |
| NinjaTrader | Feed y gateway físico exclusivamente. | Sin pool, afinidad, indicadores de estrategia, MM ni reglas de negocio en el AddOn. |

Módulos/valores definitivos: configuración según resultados del Owner. K05/SR es candidato, no decisión definitiva. Objetivo Owner: domingo 2026-10-18 por la noche, sin promesa de entrega. Permisos comerciales de automatización excluidos por el Owner. La continuidad de señales es requisito funcional; no una garantía de retiros o rentabilidad.

### 2. La definición histórica existe: Signal, no otra entidad

**OBSERVADO_EN_CÓDIGO en las lecturas anteriores:** `v3/sdk/futures/domain/signal.go` define Signal como salida canónica inmutable de Strategy. Contiene SignalID, StrategyID, StrategyCycleSeq, Intent, InstrumentID, Direction, Details, CreatedAt, ValidUntil y Provenance; no cuenta, provider, MM ni estado de ejecución. Intents: OPEN, REDUCE, CLOSE y CLOSE_ALL.

**AUTORIDAD DOCUMENTAL:** Architecture Candidate V2 §2.2 denomina esa salida Signal y define strategy_cycle_seq como identificador escalar del ciclo técnico, no nuevo aggregate. Technical SPEC V1 §9–11 separa Signal, SignalDelivery y Operation. D2-08, 2026-09-28, explicita Strategy account-agnostic, sin feedback físico hacia Strategy, sin StrategyTrade/operation_key, y documenta el seam legacy ReferenceEvent→Signal. Esto último es evidencia de diseño histórico, no prueba nueva del adaptador Forex.

El término no se perdió: el análisis R2/R3 no lo recuperó oportunamente. No crear CanonicalOperation, StrategyTrade, otra Signal ni un ciclo financiero global.

```text
Strategy → Signal → signal_fanout → SignalDelivery
                               → echo/operation por AccountStrategy
                               → admisión → Operation + MoneyManagement
                               → reserva/revalidación → Order → Fill
```

Operation es ejecución account-specific: cuenta, AccountStrategy, StrategyCycleSeq, contrato fijado, MMState, órdenes y fills. SignalDelivery añade el destino a la intención técnica. Se replica la intención, no fills/importes de una cuenta maestra. Una cuenta puede cerrar/rechazar antes sin alterar Strategy ni otras ejecuciones.

`strategy.FanoutState.Linearize` genera deliveries deterministas con DeliveryFromSignal; filtra OPEN por Enabled/instrumento y entrega REDUCE/CLOSE/CLOSE_ALL también a bindings deshabilitados para nuevas entradas. Dedup actual: `(account_strategy_id, signal_id)`. ApplyTargetSet aplica versiones prospectivas. Se reutiliza esta mecánica.

Las referencias D2 sobre indicadores privados de Strategy son históricas en ese aspecto: se conservan sus contratos Signal/ciclo/ejecución, no se reintroduce el cálculo en consumidores, sustituido por el mandato de analytics compartido.

### 3. Modelo mínimo e identidades

La configuración humana define pools/asociaciones; el runtime selecciona la cuenta y materializa AccountStrategy.

| Elemento | Identidad / datos | Autoridad |
|---|---|---|
| Strategy configurada | strategy_id, módulo, parámetros técnicos, instrumento/requisitos. | strategy_engine existente; estado técnico compartido, independiente de cuentas. |
| Pool | pool_id + miembros del catálogo. | Configuración; sin saldo ni fase duplicados. |
| Asociación | ID estable, pool_id, strategy_id, MM/config, enabled. | Configuración; versión MM no crea otra asociación. |
| Turno activo | asociación → cuenta, generación, reclamación/activación. | PoolManager; máximo un destino activo y una reclamación pendiente por asociación. |
| Exclusividad/afinidad | cuenta → asociación/Strategy de origen; claim/generación de ejecución. | Owner account-wide; afinidad no desaparece al liberar turno. |
| AccountStrategy | ID estable de cuenta + asociación, MM/contexto. | Binding existente, materializado/reutilizado automáticamente. |

Conceptos nuevos del delta no implican structs/flags existentes. Reutilizar IDs/mensajes cuando encajen; no IDs de reloj de reinicio o de sesión NT. AccountStrategyID conserva su restricción de no incluir `:`.

Ejemplo conceptual con cinco cuentas y tres asociaciones:

| Pool | Cuentas por antigüedad | Asociaciones |
|---|---|---|
| P | C01, C02, C03, C04, C05 | A: Strategy-A + MM-A; B: Strategy-B + MM-B; C: Strategy-C + MM-C |

A toma C01, B C02 y C C03. C01 alcanza daily target: C01 pausa, termina su ejecución pendiente y A toma C04. C02 alcanza daily DD: B toma C05 tras drenaje. A/B/C no dejan de evaluar ni emitir señales por esas pausas. Al siguiente día elegible A vuelve a C01 y B a C02; C04 sigue siendo de A y C05 de B, esperando sus próximos turnos. Una cuenta propia perdida o pasada deja de participar en esa ejecución/etapa y se omite.

Pools pueden mezclar programas si sus contratos están soportados. Compatibilidad corresponde a asociación/MM, instrumento, programa/fase y adaptador; nunca a un if providerName de Strategy. Pausar una cuenta no elimina su afinidad ni bloquea las otras de la misma Strategy.

### 4. PoolManager y proyección sobre el fanout existente

**PROPUESTA TÉCNICA:** owner de asignación en Core por pool_id para varios turnos; owner account-wide existente confirma exclusividad. Sin microservicio, Redis, TTL de ownership ni scheduler de Strategy adicional.

1. Al habilitar asociación, terminar turno por pausa/desenlace o llegar la frontera diaria aplicable, reevaluar selección. Primero cuentas propias elegibles por creación; si ninguna, reclamar libre compatible más antigua. Afinidad de otra Strategy siempre excluye. No se cambia tras cada trade ni se espera al próximo día para sustituir una cuenta pausada.
2. Persistir una solicitud de claim por asociación con cuenta/generación. Claims concurrentes de pools solapados se serializan en owner account-wide; sólo uno se confirma y el perdedor prueba la siguiente candidata.
3. Confirmado claim, instalar/reutilizar AccountStrategy, contexto y MM antes de habilitar OPEN. Respuestas de generaciones antiguas se absorben idempotentemente.
4. Proyectar destinos mediante FanoutTargetSet/AccountStrategyTarget existentes y metadata mínima de asociación/generación. Un solo versionador del conjunto completo por Strategy combina cambios de varios pools: listas parciales no deben borrar destinos ajenos.
5. Signal permanece inmutable y sin campos de cuenta/pool/MM. El envelope/config de delivery transporta routing; Operation/Provider comprueban claim/generación antes de nueva exposición y durante revalidación.
6. Daily pause: cerrar OPEN sólo para la cuenta saliente, conservar gestiones/fills mientras drena, liberar su turno y activar sucesora en la misma sesión. La afinidad de la pausada permanece y su reanudación tiene frontera diaria explícita. Strategy y analytics siguen avanzando durante toda transición.
7. Inicio de nuevo día operativo: volver a seleccionar desde la más antigua propia elegible, sin conservar automáticamente la última cuenta usada ayer. No forzar cancelaciones por reloj ni migrar exposición: resolver/drenar el destino anterior antes de activar otro, según política de cierre ya aplicable. Persistir frontera procesada para que un reinicio no duplique el cambio diario.

La proyección de targets no posee economía ni exclusividad. Actualizaciones atrasadas no reactivan generaciones revocadas. El protocolo confirma pasos, sin presumir atomicidad entre keys; un crash repite consulta/resultado de la misma solicitud, no asigna otra cuenta a ciegas.

Dedup al rotar: el guard por AccountStrategy no basta para impedir que una Signal consumida por A/C01 se entregue otra vez a A/C04. Conservar progreso/decisión por asociación con identidades existentes `(run, strategy_eval_seq, signal_seq)`/SignalID y destino fijado. Otra asociación autorizada conserva su entrega independiente. No reciclar señales para llenar sucesoras ni reproducir OPEN vencidos.

La continuidad busca que las señales posteriores tengan una sucesora disponible, no rellenar huecos con señales antiguas. Registrar el destino o causa de no ejecución de cada oportunidad; una transición no puede descartar silenciosamente entradas. Conservar el guard StrategyCycleSeq y el comportamiento existente de admisión pendiente/siguiente ciclo acotado; no otra cola en PoolManager.

### 5. Afinidad de largo plazo y rotación diaria

**Regla prioritaria R5:** una cuenta permanece ligada a A durante toda su vida, pero A usa otras cuentas propias/nuevas cuando aquélla se pausa. «Hasta que muere o pasa» describía la vida de la cuenta en la operativa de A, no la retención exclusiva de su turno diario. La interpretación contraria en R4 queda descartada.

| Hecho | Acción | ¿Continúa en otra cuenta? |
|---|---|---|
| Trade termina y cuenta sigue operable. | Conservar turno actual. | No cambia por ese solo hecho. |
| Daily DD o daily target alcanzado. | Pausar cuenta, cerrar nuevas entradas y drenar; seleccionar siguiente propia elegible o libre compatible por antigüedad. | Sí, en la misma sesión. |
| Siguiente día operativo. | Rehabilitar cuentas cuya pausa terminó; volver a la propia elegible más antigua y repetir secuencia diaria. | Se selecciona de nuevo desde la más antigua; no se conserva por inercia la última de ayer. |
| Cuenta perdida/vencida definitivamente. | Excluir nuevas entradas, resolver pendientes, preservar historia/afinidad. | Sí tras drenaje. |
| Challenge completado. | Cerrar etapa de evaluación, resolver pendientes; mantener identidad/afinidad para su lifecycle posterior. | Sí tras drenaje. |
| Funding/review/payout pendiente que impide operar. | Mantener estado y afinidad, retirar del conjunto actualmente elegible. | Usar otra elegible; no inventar aprobación/pago. |
| Orden/exposición incierta. | Conservar reclamación de la saliente y reconciliar; no activar exposición adicional en esa asociación por timeout. | No saltarse recuperación; Strategy y otras asociaciones siguen. |
| No queda cuenta elegible. | Registrar falta de destino; mantener Strategy/analytics generando sus señales. | No inventar cuentas, señales o fills. |

Las pausas se levantan según día operativo/timezone/config aplicable, no según medianoche del servidor ni un contador reiniciado por el proceso. El reset diario de selección NO resetea balances, pisos permanentes, historial o afinidad. En pools heterogéneos cada cuenta recupera elegibilidad por su propio calendario efectivo; la selección respeta la frontera operativa configurada, sin inventar un UTC global.

Challenge pasado no equivale a cuenta destruida ni credenciales funded creadas. Su posterior activación confirmada conserva A y utiliza MM/contexto funded. Las pausas diarias de una funded también rotan a otra cuenta; no congelar esa asociación por distinguir challenge/funded.

Drenaje: resolver admisión pendiente, órdenes ejecutables/inciertas, exposición y comandos que aún puedan producir efectos. Estar flat por sí solo no acredita ausencia de órdenes pendientes. Operation/M2/Provider aportan sus hechos; PoolManager no fabrica finalidades. ACK/fills tardíos conservan cuenta/Operation/orden/contrato originales.

Un stop explícito del Owner es diferente de daily pause de una cuenta. Stop-entry, drenaje y flatten siguen separados. Trade manual requiere ausencia de ownership automático activo de esa cuenta y reconciliación antes de volver; no es un objetivo adicional del planificador.

### 6. Strategy, analytics, MM y reglas por cuenta

```text
Feed observado → market_stream → barras → cálculo de indicadores
                                      → observaciones causales
                                          ├→ Strategy → Signal → fanout
                                          └→ MM según su trigger

PoolManager → cuenta activa de cada asociación / targets efectivos
SignalDelivery → Operation + MM → Provider/reserva/revalidación
                                   → bridge → NinjaTrader
NinjaTrader → órdenes/fills/posiciones/quotes → owners financieros
```

Strategy comparte evaluación/estado técnico por strategy_id, sin datos ni feedback de cuenta. Otra asociación añade deliveries, no reevaluaciones técnicas. Parámetros técnicos diferentes pueden definir otra instancia. Todas las cuentas pausadas tampoco pausan Strategy/analytics; si falta destino elegible sólo falta ejecución física, con causa visible. Rotar no hace rewarmup ni reinicia el ciclo técnico.

Analytics calcula la unión de demandas de Strategy y MM, incluidos indicadores exclusivos del MM. Mismos kernels e identidad de cálculo por stream/contrato/timeframe/parámetros/calendario/seed/epoch/versión relevante. Sin servicio extra, DSL ni TG convertido por rutina en API universal. Runtime incremental; backtester puede preparar tablas respetando causalidad.

El puntero Go tgPublished de las lecturas anteriores no acredita serving distribuido. Completar observaciones inmutables hacia owners consumidores mediante transporte/estado existentes; proyecciones locales no son otro calculador. Strategy recibe el snapshot ligado a su trigger; MM fija una vista causal por evaluación, nunca un valor futuro porque el productor avanzó. Ausencia identificada no bloquea reducciones que no dependen del indicador.

Quote ejecutable y economía son hechos vivos distintos de indicadores. MM actúa también por quote/fill/economía sin esperar una Signal nueva. Last no reemplaza bid/ask. SR/H1 requieren datos con completitud demostrable; NinjaTrader puede aportar observaciones/barras, pero Echo calcula los indicadores.

Resolver MM/config por asociación/fase, no un único cfg.MM para todos. MMState aislado por Operation; parámetros normales nuevos son prospectivos. RuleSet por cuenta/programa/fase; restricciones efectivas mantienen su evaluación. PoolManager consume estado/disponibilidad, no recalcula PnL ni mantiene otro ledger. Sustituir referencias GAU50 donde corresponda por términos reales, nunca por reinicio de cuenta/proceso.

### 7. Presupuesto completo: contrato conservado, integración posterior

Presupuesto MM300 con remanente53: intentar con300. Presupuesto1000 con remanente1: intentar con1000. No reducir cantidad/presupuesto/stop, rechazar o retirar únicamente por la comparación con remanente positivo. Cantidad, ticks, costos, capacidad física y bloqueos ya alcanzados siguen siendo reales. Este mandato no cambia otros cálculos de objetivo/fase del MM.

No falsear piso ni PnL. Si ocurre breach real se aplica su desenlace y rotación tras drenaje. Presupuesto, submit, aceptación, fill y PnL son hechos diferentes. Comprobar el contrato end-to-end para que un guard de pool/admisión/reserva/revalidación no reintroduzca la misma retirada o recorte.

Antecedente publicado R3 en95e9d10: EntryBudgetV1 rechaza por TG_ENTRY_BUDGET_EXCEEDS_HEADROOM y campaña puede perder por LOST_ENTRY_BUDGET_BY_POLICY. Semántica diferente, registrada sin reauditarla ni bloquear trabajo paralelo. Runtime modifica dominio de SU rama; backtester incorpora después los cambios estabilizados. No afirmar paridad entre cortes diferentes ni reinterpretar resultados históricos con política posterior. Entregar los fixtures de presupuesto junto al delta común, sin paquetes LiveMM/BacktestMM duplicados.

### 8. Delta de implementación por propietario y compatibilidad

| Bloque | Superficies existentes | Entrega |
|---|---|---|
| Composición | sdk/futures/config, core/internal/futuresruntime y registro StateFun. | Pools/asociaciones, MM por asociación, reglas/contexto por cuenta, AccountStrategy automático y dispatch por identidad. |
| Asignación | Owner mínimo PoolManager en Core + claim account-wide existente. | Turnos concurrentes por asociación, FIFO, afinidad permanente, rotación por daily pause y retorno diario a más antigua propia. |
| Fanout | sdk/futures/strategy/fanout.go, función Core correspondiente, envelope/contexto de delivery. | Targets combinados por Strategy, generaciones y dedup por asociación al cambiar de cuenta, sin modificar Signal canónica. |
| Ejecución económica | SDK Operation/MM/Provider/config y funciones Core. | Contexto por binding, presupuesto completo, estados diarios/desenlaces reales, reservas/revalidación. |
| Observaciones | market_analytics, analytics SDK, serving y productores quote/economía. | Unión de demandas, causalidad distribuida/restart, completitud de indicadores, independencia de pausas de cuentas. |
| Gateway | futures-bridge, adaptador y EchoExecutionAddOn.cs. | Routing multiaccount, M2/correlación y recuperación; sin decisiones del pool/MM en NinjaTrader. |

Los bindings fijos existentes siguen compatibles cuando no son pool-managed. Pool-managed exige metadata/guards completos, no fallback silencioso a legacy. Habilitar analytics/composición no arma órdenes por sí mismo. Nuevas cuentas se incorporan al catálogo/pool, sin replicar configuración Strategy/MM. Afinidad histórica desconocida no se inventa; se resuelve por autoridad operativa.

Una nueva Strategy usa Signal/requisitos analíticos; un nuevo MM usa su contrato/estado por operación; un programa registra términos efectivos. No modificar scheduler/bridge por un cambio de parámetros ni duplicar procesos para ocultar límites multikey.

### 9. Secuencias y pruebas de aceptación

| Prueba | Resultado exigido |
|---|---|
| Strategy independiente | Cuenta pausada, perdida o sustituida no pausa ni cambia la generación de Signal. Variar cuenta/MM no altera sus decisiones técnicas. |
| Daily target/DD | C01/A pausa, drena y A toma C04 en la misma sesión; C04 recibe oportunidades posteriores mientras C01 sigue pausada y ligada a A. Probar ambos motivos. |
| Reinicio diario | C01/C04 propias de A recuperan elegibilidad; A empieza por C01 (más antigua), no conserva C04 por ser la última de ayer; después rota otra vez al pausar. |
| Afinidad multiday | C01 usada por A nunca se entrega a B, ni libre de exposición ni tras pausa/restart. |
| Concurrencia | Tres asociaciones/cinco candidatas, cuentas activas distintas; pools independientes concurrentes y solapados sin doble claim. |
| Pérdida/pase | Cuenta deja etapa actual, drena y se selecciona sucesora. No usar remanente pequeño como pérdida inventada. |
| Señal durante rotación | No pausa del cálculo ni descarte silencioso; destino/cause trazables. Redelivery consumida en C01 no ejecuta de nuevo en C04. Gestión vieja no afecta otro ciclo. |
| Recuperación | Crash entre claim/activación, respuesta vieja, ACK perdido/fill tardío: ownership correcto, no retry ciego ni liberación por TTL. |
| Economía | 53/300 y1/1000 sin ajuste/rechazo/retirada por remanente; breach observado con respuesta; fase y saldos aislados. |
| Analytics | MM recibe observaciones causales por sus triggers en otro proceso/restart; no recomputa kernels ni espera exclusivamente Signal inicial. |
| Cohorte | Cinco cuentas soportadas con identidades/routing/config correctos; alta de sucesora sin binding manual. No cinco trades exigidos. |

Fixtures/SIM y observaciones del destino real son evidencias distintas. No fabricar señales/fills para completar uso de cinco cuentas. La prueba individual no demuestra concurrencia, pero ausencia de oportunidades en una cuenta no falla la entrega. No objetivo de saturación/utilización, cinco asociaciones impuestas ni pools extra para forzar actividad. No repetir las40 campañas ni exigir rentabilidad para aceptar el alcance técnico.

### 10. Dos ramas de producto y convergencia gradual

Runtime implementa este contrato en su rama y puede modificar el SDK allí, sin esperar adaptación del CLI/campañas. Backtester continúa investigación/validación en otra rama con sus políticas y correcciones identificadas. Adopta posteriormente conjuntos coherentes de deltas estabilizados del runtime, incluidos rotación diaria/presupuesto y sus fixtures.

Integración local posterior conserva commit/config/datos/política de cada resultado, evita cherry-picks parciales incompatibles y mantiene un dominio compartido objetivo, no dos motores permanentes. Paridad sólo sobre mismo corte integrado e inputs equivalentes. No se crean ramas/worktrees/clones en este análisis. Agents-OS sigue sobre master y no se editan controles del otro carril.

### 11. Estado del candidato y límites de evidencia

**Corrección R5 prioritaria:** son incorrectas las afirmaciones R4 que retenían el turno durante daily pause, impedían tomar otra cuenta en la misma sesión o mantenían por inercia la última cuenta al día siguiente. No deben implementarse. La aclaración del Owner restaura el flujo de campañas: pausa de cuenta → siguiente cuenta de ESA Strategy; próximo día → más antigua propia elegible. La pausa pertenece a la cuenta; la Strategy no se detiene.

Lectura documental actual y corrección no son pruebas de producto. Serving distribuido, dispatch, quote/economía y AddOn multiaccount requieren las pruebas listadas; el histórico D6 stale del5-oct no describe el terminal actual. No se afirman ejecuciones ni operación real desde esta sesión.

Diferido: varias Strategies dentro de una cuenta, MM arbitrario por cuenta, varias cuentas simultáneas por asociación, optimizador/netting/hedging, UI nueva y otros adaptadores. Módulos/parámetros seleccionados por Owner son configuración, no excusa para demorar el contrato.

Environment Contract se carga por operador local antes de infraestructura según Agents-OS; no nueva investigación aquí. Prompt LOCAL sólo a pedido del Owner. No código, scripts, campañas, despliegue, órdenes, dispatch ni cierre automático.

## Fuentes

### Corrección R5

- Aclaración explícita del Owner en esta conversación: daily DD/daily target hacen rotar a la siguiente cuenta para la misma Strategy; al siguiente día se vuelve a la más antigua asignada. Strategy nunca se pausa por cuentas.
- Mandato inicial PROMPT_VERSION1 del2026-10-16: requisitos analytics/Strategy/MM; sección de campaña con rotación en la misma sesión; secuencia1 de escenarios operativos. La interpretación R4 fue del asistente, no una pérdida del contrato histórico.
- R5 no ejecuta ni inspecciona nuevo código; conserva cortes de evidencia anteriores. R1–R4 en Git son historia, no políticas paralelas vigentes.

### Recuperación canónica R4

- xKoRx/echo@95e9d105182af99d03700f4b5def24bf9fc6b5fd, `v3/sdk/futures/domain/signal.go`: blob9cb6d0810fdf5437d5972804e3f015c7514be6f6.
- Mismo corte, `v3/sdk/futures/strategy/fanout.go`: blob100a9e72b32158d8b87e2521b265d1d4428ead8c.
- [[Echo Futures Architecture Candidate V2]], §1–2.5: blobbfccbb8289d8a8896ecbdb921f61cacd5506e95f.
- [[Echo Futures — Technical SPEC V1]], §3 y§9–11: bloba37ba7c2666ecb35ec59da2a8ca9ac48e190e77b.
- [[Echo Futures — D2-08 Strategy Runtime]], 2026-09-28, §1–3/5: blobae736caf27cb028b69a1260de8e35cc3fcd03a16; vocabulario/ciclo/account-agnostic, no reintroducción de indicadores en Strategy.

### Deltas ya inspeccionados

- En95e9d10: `v3/sdk/futures/strategies/tgmm/tgmm.go` blobeb2824a470d27d63d93c856f4a0829d4526d367b; `v3/backtester/platform_operability.go` blob52710c0494dd375745aeb8c3dce85386ec36265e; `v3/sdk/futures/strategies/tgmm/minimum_policy.go` blob9ace5fdbff3f6b2d506c9e769cc29236de9d54cf; `v3/backtester/tools/tradesgerard/TG-FLOW.md` blob7af1b9a9fe1a471ebe0f5e048379c8c0400dd7fb.
- Base R1/R2 0c4aae552176fda005c44766e24dd70e8c48e589: runtime.go blobf4fdefe7a1efb7fb29fb7593e708e86a2be321e0; config/views.go blob3670051e354c3f61e3389ec06691beeb606640de; config/composition.go blob181b525166c76bebe00a53c62f7748915f6d186b.
- Misma base funciones Core: futures_market_stream.go blob08ccb58b4d3a0021e5adb58abcd5574d65bf06dc; futures_market_analytics.go blob064824c5631d53265907c2a7d0fbe19339c88174; futures_signal_fanout.go blob0201175340f4427875daff372de7cc4aa79b225f; futures_operation.go blob7605f4aaff9d54ed9a56cb7fd15827400b8cb78c; futures_provider_rules.go blobe4361f331c511b9f8b5e2caa328e9621b12055c0.
- Misma base bridge/core/bridge.go blob17874301ffd9296a2426806ff5b9c5188904756b; EchoExecutionAddOn.cs blobdedd6dcdd14abefee00f087ff23e574ca3cdfd3f; README bridge blob350166d5ba49c6c55f61c417306c61272c014dae.
- Campaña R2 platform_campaign.go blob1bdbd20f4abf9aa89d4044fa77332d2a9801d04f: selección/pausa observadas, no certificación de paridad con el nuevo runtime.

### Autoridades separadas

- [[Echo Futures]], mandato inicial y aclaraciones posteriores del Owner.
- [[TRADESGERARD-CONTROL]] y [[TRADESGERARD-CONSOLIDATION]], no modificadas.
- [[10-projects/Echo Futures/artifacts/d6-final-physical-certification-20261005/D6-FINAL-PHYSICAL-CERTIFICATION|D6 físico 2026-10-05]], blob6fd72dceb517a730647c5dec27dc714bbb55797c: sólo evidencia histórica.
