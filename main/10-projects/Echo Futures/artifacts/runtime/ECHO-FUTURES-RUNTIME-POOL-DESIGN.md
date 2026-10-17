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

**CANDIDATO_R6_S01 / G1_REVIEW_MANAGER.** Delta implementable vigente en §12–18; R5 se conserva como antecedente y decisiones compatibles. **Antecedente R5:** Diseño de asignación y ejecución sobre Echo existente. R5 corrige un error del asistente en R4: una pausa por daily DD o daily target SÍ termina el turno de esa cuenta y activa otra para la MISMA Strategy en la MISMA sesión. Al siguiente día operativo se vuelve a la cuenta elegible más antigua ya asignada a esa Strategy. Afinidad permanente NO significa retención del turno durante una pausa. La aceptación del diseño corresponde al Owner; esta nota no declara implementación, pruebas ejecutadas, despliegue ni cierre de sesión/proyecto.

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

Integración local posterior conserva commit/config/datos/política de cada resultado, evita cherry-picks parciales incompatibles y mantiene un dominio compartido objetivo, no dos motores permanentes. Paridad sólo sobre mismo corte integrado e inputs equivalentes. R5 no creó ramas/worktrees; S01 sí prepara la rama/worktree descrita en §12. Agents-OS sigue sobre master y no se editan controles del otro carril.

### 11. Estado del candidato y límites de evidencia

**Corrección R5 prioritaria:** son incorrectas las afirmaciones R4 que retenían el turno durante daily pause, impedían tomar otra cuenta en la misma sesión o mantenían por inercia la última cuenta al día siguiente. No deben implementarse. La aclaración del Owner restaura el flujo de campañas: pausa de cuenta → siguiente cuenta de ESA Strategy; próximo día → más antigua propia elegible. La pausa pertenece a la cuenta; la Strategy no se detiene.

Lectura documental actual y corrección no son pruebas de producto. Serving distribuido, dispatch, quote/economía y AddOn multiaccount requieren las pruebas listadas; el histórico D6 stale del5-oct no describe el terminal actual. No se afirman ejecuciones ni operación real desde esta sesión.

Diferido: varias Strategies dentro de una cuenta, MM arbitrario por cuenta, varias cuentas simultáneas por asociación, optimizador/netting/hedging, UI nueva y otros adaptadores. Módulos/parámetros seleccionados por Owner son configuración, no excusa para demorar el contrato.

Environment Contract se carga por operador local antes de infraestructura según Agents-OS; no nueva investigación aquí. S01 está solicitado explícitamente: sólo rama/diseño/plan y cierre de su propia sesión; sin código, scripts de producto, campañas, despliegue, órdenes ni activación S02.

### 12. R6 — contrato cerrado candidato S01 (2026-10-16)

**Autoridad vigente:** mandato Owner RUNTIME-POOL-S01 sobre R5; G1 `review`, aceptación exclusiva del Manager. Las secciones 12–20 precisan y prevalecen sobre las propuestas R1–R5 anteriores; no crean otra SPEC. Planificador único: [[Echo Futures — Runtime Pools]]. Evidencia de producto `HEAD` en `xKoRx/echo@d74b652500e673fc2bf4289f9f195f11960ba26e`; revisión localizada, sin ejecución de tests de producto ni certificación física. Rama `feature/ef-runtime-pools`, worktree externo `echo-runtime-pools` relativo a [[echo-go-workspace]]. Local bootstrap comparado sin delta con `origin/master` de xKoRx/agents-os después de fetch. No subagentes.

**Corrección expresa de responsabilidad:** ni Runtime ni PoolManager deciden si Strategy genera señales, llegó a target o alcanzó daily DD. PoolManager no recibe balances ni importa kernels financieros; consume hechos versionados de las autoridades económicas. `strategy_engine(strategy_id)` sólo recibe triggers técnicos y observaciones analíticas. Una pausa por cuenta nunca cambia `enabled`, readiness técnico, timers, ciclo ni config de Strategy. El gate de entradas pertenece a ejecución, no al productor de Signal.

#### A. Arquitectura y propietarios

| Propietario StateFun | Key | Responsabilidad definitiva |
|---|---|---|
| `echo/market_stream` y `echo/market_analytics` existentes | stream canónico | Feed, barras, unión de demandas, cálculo único y observaciones causales serializables para Strategy/MM. Sin economía compartida. |
| `echo/strategy_engine` existente | strategy_id | Evaluación única de Strategy configurada; Signal y strategy_cycle_seq intactos. Misma Strategy en dos pools = una evaluación, dos decisiones de entrega. |
| `echo/signal_fanout` existente, extendido | strategy_id | Único serializador de targets combinados, configuración fija + proyecciones por asociación, cursor de señales y decisiones de delivery/no-destino. No selecciona cuentas. |
| `echo/pool_manager` **nuevo** | pool_id | Estado de turnos por asociación, FIFO, solicitudes claim/release, retorno diario y proyección de destino. Función Core del mismo deployment; reducer puro en SDK, sin daemon/servicio nuevo. |
| `echo/provider_rules` existente, extendido | execution_account_id canónico | Exclusividad global de cuenta, afinidad durable, fencing, admisión/reservas, riesgos y lifecycle de Provider; consume política diaria MM y hechos contables. Único lugar que confirma claim y liberación. |
| `echo/operation` existente | account_id:account_strategy_id | Admission/pending-next-cycle existente, Operation/MMState aislados, órdenes/fills y evidencia de drenaje. Resuelve MM por binding/config sellada. |
| Futures bridge / M2 existentes | execution_account_id + physical_binding | Gateway físico, journal/reconciliación, barrera de comandos y correlación original; no policy económica. AddOn sólo multiplexa conexiones físicas por binding. |

Cuenta física no es el nombre de pool ni la sesión NT: catálogo canónico `ExecutionAccountID` → `ProviderAccountBinding` → `(transport_id, provider_account_ref, physical_binding)`. Validar unicidad de este mapping en la configuración agregada. Dos aliases lógicos hacia la misma cuenta física son inválidos; no se crea un owner distinto por pool. La misma cuenta puede aparecer en dos pools; sus claims llegan a la misma key. La exclusividad requiere un único runtime StateFun autorizado por cuenta física; despliegues separados con catálogos disjuntos no se coordinan mágicamente. El gate de egress exige comprobar esa unicidad operativa.

#### B. Configuración y estado persistido (adiciones explícitas)

Se conserva `Signal` exactamente. Todo nombre de la tabla marcado NEW es contrato a implementar, no struct existente en HEAD. Los mensajes nuevos llevan `schema_version:1`, IDs estables y validación estructural; no usar reloj, random ni session_id NT como identidad lógica. `RunProvenance`, `AccountSnapshot`, `AccountContextUpdate`, `EconomicsObservation`, `ProviderAccountBinding`, `ProviderRuleSet`, `AccountStrategyTarget`, `FanoutTargetSet`, `SignalDelivery`, `Operation` y reservas se reutilizan.

| Contrato | Campos/delta obligatorio | Owner / semántica |
|---|---|---|
| `ConfigSnapshot` EXTEND | `pools[]`, `pool_associations[]`, `money_managers{id:GerardMMDef}`, `provider_rulesets{ruleset_id@version:ProviderDef}`; `AccountDef.created_at`, `created_at_source_ref`, `program_terms` cuando la fase lo requiera. | Catálogo único de Accounts existente. Fecha real de creación verificable, no fecha de ingestión, ordinal, nombre ni compra simulada. Ausente ⇒ `ACCOUNT_CREATION_UNKNOWN`, inelegible; no fabricar antigüedad. |
| `PoolDef` NEW | `id`, `account_ids[]`. | No duplica saldo, fase, economics ni credenciales. |
| `PoolAssociationDef` NEW | `id`, `pool_id`, `strategy_id`, `mm_config_id`, `config_version`, `enabled`. | ID inmutable. Cambiar pool/Strategy bajo mismo ID es error; MM nuevo sólo prospectivo, conservando versiones antiguas referidas por Operation. |
| `PoolState` NEW | config version; mapa por asociación: `assignment_generation`, fase, candidata/activa, `request_id`, `claim_epoch`, última revisión de hechos por cuenta, fronteras account-day ya procesadas, causa de espera. | Fases `IDLE → CLAIMING → INSTALLING → ACTIVE → DRAINING → RELEASING → IDLE`. Una candidata pendiente y una cuenta activa como máximo; ninguna segunda activa mientras drena. |
| `provider.OwnerState` EXTEND | `AffinityStrategyID`, `OriginAssociationID` auditivo, `Claim{pool_id,association_id,strategy_id,account_strategy_id,request_id,assignment_generation,claim_epoch,phase}`, contador `ClaimEpoch`, `AccountAvailability`, evidencias de drenaje/fence. | Affinity se fija atómicamente al primer permiso de nueva exposición; no desaparece por release/día/phase/reset normal. Claim provisional excluye competidores aunque aún no haya afinidad. OriginAssociationID no es una segunda regla de afinidad. |
| AccountStrategy efectivo EXTEND | ID derivado por hash length-prefixed `(account_id,association_id)` sin `:`; `association_id`, `claim_epoch`, `assignment_generation`, referencia MM/version/contexto. | No se configura manualmente. ID estable entre turnos de esa cuenta/asociación. No mover Operation/MMState al siguiente ID. |
| `AccountAvailability` NEW | account/context IDs, `revision_seq`, `source_ref`, `account_day_id`, estado `ELIGIBLE/PAUSED/TERMINAL/UNKNOWN`, reason, autoridad, decision_id, resume boundary opcional, observed_at; sin montos para PoolManager. | Agregado por Provider de hechos económicos, reglas, trust/readiness y política MM. Revisión monotónica por cuenta/contexto, payload diferente con mismo ID ⇒ conflicto. Stale/ausente ⇒ UNKNOWN para nueva exposición, gestión física continúa. |
| `AccountTurnClaim/Result`, `AccountTurnRelease/Result`, `AssignmentControl/Ack` NEW | cuenta/asociación/pool/Strategy, request_id, generation, expected claim epoch, contexto; resultado explícito. | Mensajes idempotentes; provider incrementa epoch durable por nuevo claim. Repetición exacta devuelve resultado anterior; generación obsoleta no revive turno. Abort de claim provisional necesita ACK de provider antes de probar otra cuenta. |
| `AssociationTargetUpdate/Ack` NEW | asociación, generation, claim epoch, target, modo `OPEN_ENABLED/MANAGE_ONLY/NO_TARGET`, MM/config ref. | Fanout aplica por asociación, rechaza versión vieja y versiona internamente el set completo. Ningún pool envía un FanoutTargetSet parcial que borre a otros. |
| `SignalDelivery` y `AccountStrategyTarget` EXTEND | routing opcional `association_id`, `assignment_generation`, `claim_epoch`; ausencia significa binding legacy, nunca pool fallback. | Account-specific, sin alterar Signal. Destino sellado por delivery; copy de una signal antigua no cambia generación. |
| `DrainEvidence` / `PhysicalDrainEvidence` NEW | cuenta/contexto/epoch, operation owner seq, command frontier, bridge barrier ID, reconciliation generation, unresolved counts, evidence refs. | No basta un booleano flat ni timeout. Reducer provider verifica conjunción de evidencias actuales, sin netear operaciones entre cuentas. |

Afinidad es por Strategy configurada (ID), no por nombre de módulo, programa, día o MM. Una cuenta ya afiliada a A puede abastecer otra asociación de A sólo si pertenece a su pool, está libre y el claim global lo confirma; no puede abastecer B. Es una resolución técnica compatible con la cardinalidad Owner, sin añadir afinidad permanente al MM/pool. Para selección: propias elegibles de ESA Strategy por `(created_at, execution_account_id)`; si ninguna, sin afinidad compatibles por la misma ordenación. Desempate lexicográfico estable. Asociaciones del mismo pool compiten por orden de sus eventos; en bootstrap se recorren por ID. No promete fairness global entre pools; un rechazo vuelve a probar la siguiente candidata, sin starvation por retry ciego.

#### C. Autoridad económica y día comercial

HEAD posee kernels `accounting.Ledger`, `provider.EvaluateEconomicRisk`, `provider.EvaluateLifecycle`, `gerardmm.Manager.computeEconomics`, `tgmm.Manager.pending` y `requestedBudget`; no se copian sus fórmulas al PoolManager. `AccountSnapshot.DailyLossBreached` solo NO distingue pausa interna diaria de breach terminal de programa; no interpretarlo automáticamente como reanudable al día siguiente.

**Wiring cerrado:** extender `FuturesProviderRulesFn` y `provider.Input` con ingestión de una revisión contable autorizada (`accounting.Revision` + identidad causal/contexto, proyectada a `provider.EconomicObservation`) y fronteras de día/calendario. El productor de contabilidad conserva su ledger actual; Provider persiste `RiskState` y consume esa revisión una vez, invoca los kernels existentes y emite `AccountSnapshot`/economics y `AccountAvailability`. No reconstruir PnL desde el neto de posiciones ni crear ledger en PoolManager. El source contable debe registrar productor/revisión/covers-through; snapshot de saldo NT sin atribución completa no equivale a revisión contable. Ante ausencia del productor, `ECONOMICS_UNAVAILABLE` explícito y ninguna nueva exposición. El seam admite el productor existente o el adaptador de su revisión; S02 prueba el input serializado real del contrato, no presume conexión LIVE.

**Política MM diaria:** añadir en SDK un contrato puro `AccountPolicy` implementado por cada MM soportado en pool, con `EvaluateAccount(AccountPolicyInput) → AccountPolicyDecision`. Input: cuenta/contexto, AccountEconomics, RuleSet/terms, config MM sellada, account-day/frontera y observaciones analíticas requeridas; salida tipada `ALLOW/PAUSE_UNTIL_BOUNDARY/COMPLETE/UNAVAILABLE`, reason/decision_id y boundary explícita. Se invoca dentro del owner provider, por revisión contable/frontera, aun sin Operation activa; su estado diario vive por cuenta/contexto/config, separado de MMState de Operation. Extraer/reutilizar los helpers puros de economics de GerardMM/TGMM sin cambiar fórmulas de objetivos, sizing no relacionado ni indicadores. Cuando MM dentro de Operation descubre una pausa, publica la misma decisión tipada/revisión al provider; éste deduplica contra el mismo policy evaluation, nunca deduce daily target desde `TerminationIntent` genérico. `TG_CYCLE_OBJECTIVE_OR_SIGNAL`, un cierre técnico y MM_NO_ACTION NO significan daily pause.

Provider combina hechos: terminal de reglas/programa domina; pause económica efectiva impide nuevas entradas; falta de trust/readiness da UNKNOWN; ALLOW sólo cuando todas las autoridades necesarias están disponibles. Reglas de daily DD terminal siguen sus términos reales; pausa interna o daily target se reanuda sólo con nuevo hecho positivo de la autoridad tras SU frontera. No limpiar `RiskState.Breached` por reloj. PoolManager puede pedir refresh al alcanzar resume boundary, pero jamás convertir timestamp en ALLOW. Cambio de contexto/programa usa `AccountContextUpdate` atómico y no borra afinidad ni historia.

En cada cambio `account_day_id` autorizado de una cuenta, PoolManager reevalúa sus asociaciones afectadas. Si reaparece una propia más antigua que la activa, solicita MANAGE_ONLY y drenaje a la activa; ésta termina según sus órdenes de gestión/MM/Provider vigentes. Sin política autorizada de flatten, espera la convergencia y no fuerza cierre por reloj. Al ACK de drenaje, reclama la más antigua elegible. La frontera procesada se persiste por cuenta; nada de medianoche global ni `nextNYOpen` hardcodeado. Posiciones legítimamente abiertas pueden demorar el retorno: estado `DAILY_RETURN_PENDING_DRAIN`, Strategy sigue avanzando.

#### D. Protocolo de claim, activación y drenaje

1. Provider recibe claim en key de cuenta canónica; compara config/contexto y elegibilidad, afinidad y cualquier claim previo (incluido legacy fixed). Persiste claim/epoch y respuesta atómicamente con egress StateFun. Un loser recibe `ACCOUNT_ALREADY_CLAIMED`/`AFFINITY_MISMATCH`; retry de la misma solicitud no crea otro epoch.
2. PoolManager persiste resultado y solicita instalar binding efectivo, MM y AssignmentControl en Operation. Operation ACK incluye config/contexto/generación. Provider recibe confirmación de instalación; sólo entonces habilita new-risk para ese claim. Fanout recibe proyección OPEN_ENABLED después de estos ACK. Reordenamiento cross-key no se interpreta como transacción global.
3. Nueva exposición valida el tuple completo en entrega, AdmissionRequest, ExposureReservationRequest y ReservationRevalidate. Provider fija afinidad al primer permiso de exposición y conserva esa identidad aunque el submit sea rechazado o no produzca fill: la cuenta ya fue comprometida para A. MMState y contrato se sellan en la Operation existente. Gestión/reducción usa la correlación original y no exige que ese epoch sea el nuevo turno activo.
4. Ante PAUSED/TERMINAL/UNKNOWN que impida continuar, provider cierra new-risk primero y notifica. PoolManager solicita MANAGE_ONLY al fanout y revocación a Operation. Operation invalida admissions y deferred OPEN del epoch; no los retargetea. Se mantienen REDUCE/CLOSE/CLOSE_ALL aplicables al ciclo original, cancel/replace reductivos y fills.
5. **Barrera física obligatoria:** Operation publica fence en su stream M1 ordenado por cuenta, después de todos sus comandos previos; bridge persiste el máximo epoch revocado antes de ACK. Cualquier comando expansivo viejo recibido después se absorbe con causa, aunque tuviera revalidación anterior. Un write ya iniciado entra en M2 y debe reconciliarse. La barrera no cancela órdenes por sí sola ni decide economía. Cancel/replace reductivos válidos del epoch saliente siguen permitidos.
6. Operation emite DrainEvidence sólo sin admission/deferred entry, sin órdenes con efecto posible, sin exposición lógica ni acciones pendientes. Bridge emite PhysicalDrainEvidence sólo después del fence, recovery barrier vigente, journal sin SUBMITTING/AMBIGUOUS/pendiente, reconciliación sin órdenes ajenas no resueltas ni posición pendiente y frontier completo. Provider verifica además reservas/finalidad/capacity y facts causales que cubren el fence. Cualquier UNKNOWN o discrepancia mantiene DRAINING. No TTL liberador, no inferencia de cancel ACK como finality.
7. Provider confirma release del claim exacto; conserva epoch tombstone y afinidad. Sólo tras ese ACK PoolManager inicia otro claim y vuelve al paso 1. Crash en cualquier fase reenvía/consulta la MISMA solicitud pendiente; jamás abandona una cuenta incierta para abrir la sucesora. Las otras asociaciones continúan.

Fill tardío se atribuye por `(execution_account_id, physical_binding, operation_id, order_id, execution_id)` retenido en M2/Operation, no por turno actual. Tras aparente release, un fill que refuta drenaje reabre reconciliación de la cuenta original, bloquea nuevas entradas de la asociación y solicita drenaje de su turno actual si corresponde a la misma asociación; no se carga a la sucesora ni se borra la evidencia contradictoria. Ninguna promesa de exactly-once física más allá de M2 + reconciliación. Eventos sin correlación se conservan en cuarentena, nunca se adoptan como operación de la sucesora.

#### E. Fanout, historia y analytics distribuido

`FanoutState.Linearize` conserva deliveries deterministas y gestión de targets deshabilitados. Persistir además tombstones de generaciones y asociaciones retiradas; antes de responder un Admission/ReservationRevalidate deduplicado, verificar el fence vigente: resultado histórico no es autorización nueva. Añadir cursor durable del stream ordenado `(run_id, strategy_eval_seq, signal_seq)` y decisiones por asociación; preservar run IDs retirados, watermark de activación y tombstones de asociaciones, sin TTL que permita replay histórico. Ingress de Signal particionado por strategy_id y ordenado; una regresión fuera de protocolo se registra `SIGNAL_ORDER_VIOLATION`, no se ejecuta como nueva. El cursor avanza también cuando no hay target. Un cambio de run requiere control explícito de lineage, no reset por restart.

Primera admisión de una Signal fija para CADA asociación habilitada: destino/generación o `NO_ELIGIBLE_ACCOUNT`, `ASSIGNMENT_DRAINING`, `ACCOUNT_FACTS_UNAVAILABLE` o `ASSOCIATION_DISABLED`. Se journaliza con señal/ciclo/versión de targets y se emite junto al checkpoint. Redelivery se absorbe antes de aplicar targets nuevos; no escanear nuevas cuentas para repetir la Signal. El resultado detallado puede proyectarse al journal durable; el guard de replay no depende de un cache de 1024 keys evictable. Asociación creada después inicia desde el cursor actual y no recibe señales viejas.

Para REDUCE/CLOSE, congelar el conjunto de destinos históricos con operaciones del mismo ciclo; conservar targets MANAGE_ONLY hasta drenaje final. CLOSE_ALL usa la semántica vigente de la Strategy sobre esos destinos; no interpreta cierre como apertura en otra cuenta. Si C01 recibió OPEN(k) y C02 no, REDUCE(k) en C02 es no-op auditable; no se sintetiza una entrada para reconstruir el ciclo. Un nuevo OPEN posterior, aun de mismo ciclo técnico, sólo se procesa como contrato vigente permita; guards de Operation evitan mezclar ciclos. No cola de oportunidades en PoolManager.

Analytics reutiliza `TGSnapshot` y `SnapshotViewForTrigger` ya transportados con BarClosed hacia Strategy. El puntero `TGOwnerViewFor` de Compose no sirve como evidencia distribuida: se reemplaza en el camino pool por snapshots persistidos en owners consumidores. Demandas = unión de requisitos declarados de todas las Strategies y MMs, deduplicadas por stream/contrato/timeframe/parámetros/calendario/seed/epoch/versión de kernel. No se multiplican por cuenta.

Añadir `AnalyticsObservation` tipada con observation ID, stream, contract, requirement key, close boundary, revision, authority epoch, published-at y frontier, payload calculado/availability. `market_analytics` emite actualizaciones hacia Operation/provider subscribers; consumidores sólo guardan read models. En cada Signal/quote/fill/economics decision se fija cut causal y sólo observaciones publicadas y cubiertas por ese cut. No elegir automáticamente la última después de un retry: persistir el observation ID del input admitido. Fill y capacidad se aplican siempre; si falta analytics, MM inhibe únicamente las acciones que lo requieran y conserva reducciones independientes. Ausencia no se convierte en indicador cero ni espera ilimitada bloqueando fills.

S2 todavía calcula SMA/Bollinger dentro de `strategies/s2/indicators.go`: trasladar ejecución de esos kernels a analytics y consumir observaciones en S2, preservando exactamente resultados y state técnico. Otros cálculos técnicos propios del algoritmo (comparar precio con un nivel, decidir un setup) siguen en Strategy; no son un indicador duplicado. Runtime y backtester comparten kernels SDK; compatibilidad de wrappers legacy sólo para drivers antiguos, nunca cálculo desde Strategy pool. Prueba de equivalencia de observaciones y señales sobre mismos inputs antes/después, sin modificar fórmulas ni parámetros.

#### F. Presupuesto completo y compatibilidad económica

Agregar `GerardMMDef.entry_budget_policy` con política explícita `MM_ENTRY_BUDGET_UNCLIPPED_V1` para asociaciones pool; en TG proyectarla a TGMMDef.EntryBudgetPolicy validando que ambos valores no contradigan. Campo ausente conserva legacy fuera de pools; pool exige esta política explícita. No cambiar el significado publicado de `STRATEGIC_ENTRY_BUDGET_V1` ni sus campañas. En TGMM, `requestedBudget(pending)` sigue determinando R/T; con política nueva se omite exclusivamente la rama que compara con `headroom` para recortar/rechazar. En GerardMM separar el presupuesto elegido por MM de `min(... provider hard headroom ...)`; la política nueva elimina exclusivamente ese clamp por piso externo, conservando la fórmula MM de presupuesto/objetivo, discretización, costes y reglas no relacionadas. `R=300, floor_remaining=53` conserva R=300; `R=1000, floor_remaining=1` conserva R=1000. No implica que una cantidad fraccionaria sea ejecutable ni que venue admita tamaño superior a sus límites.

Si queda remanente positivo, ni PoolManager, provider admission/reservation/revalidation ni bridge deben traducir `R > remaining` a pausa/retirada. Cantidad máxima física, horario, breach efectivo, trust y rechazos reales siguen independientes. Al cruzar piso real, provider aplica sus reglas vigentes. Daily pause económica ya efectiva sigue vigente aunque hubiese presupuesto. Pruebas deben mostrar el presupuesto exacto solicitado y ausencia del rechazo por comparación, no exigir fill ficticio. Una política MM desconocida o un módulo sin soporte explícito falla composición.

Seam posterior backtester: `platform_operability.go` (`StrategicEntryBudgetV1`, retiro `LOST_ENTRY_BUDGET_BY_POLICY`) y `platformCampaign.selectTurn`. Reutilizar sólo la idea conservar turno entre trades, terminar turno por pause/lifecycle y seleccionar elegible tras quiescencia; NO importar `retireUntradeableAccounts`, `admitOpportunity`, thresholds, `nextNYOpen`, compras/funding ni contabilidad de campaña al PoolManager. Adaptación del driver y resultados históricos diferida explícitamente fuera de S01–S04; runtime sí entrega política/kernel/fixtures comunes. No declarar paridad con otra rama.

### 13. Secuencias de aceptación S01

| Caso | Secuencia y resultado observable |
|---|---|
| 1. Tres Strategies/cinco cuentas | Config ilustrativa P={C01…C05} ordenadas por fechas reales; asociaciones A/B/C habilitadas en orden. Claims serializados: A→C01, B→C02, C→C03; C04/C05 disponibles. Tres owners Operation y tres MM aislados; sin mutex de pool. |
| 2. Continuidad misma sesión | C01 daily target confirmado por MM → provider PAUSED, fence/drenaje/release → A reclama C04; C02 daily DD reanudable confirmado por autoridad → B reclama C05. A/B siguen produciendo Signals durante el intervalo; se audita NO_TARGET y las siguientes van a sucesoras. Trade normal cerrado sin pausa no rota. |
| 3. Regreso día siguiente | Hecho ELIGIBLE(C01, nuevo account_day_id) provoca reevaluación A; C04 pasa MANAGE_ONLY, drena y libera; A→C01 por antigüedad. Luego C04 al pausar C01. Si sus calendarios difieren, sólo la cuenta cuya autoridad cambió está reanudada. Terminal de programa no vuelve por día nuevo. |
| 4. Pools solapados | P1 y P2 solicitan C01: mismo provider owner admite uno; otro recibe rechazo y busca siguiente. Claim repetido idéntico devuelve mismo epoch. Dos aliases físicos fallan validación antes de habilitar ejecución. |
| 5. Crash/ACK/fill tardío | Crash después del claim antes de ACK: recuperar request_id, consultar/repetir. Crash tras SUBMITTING: M2 recovery sin resubmit ciego. Fill durante drain se aplica a C01 y sus reservas; release espera convergencia. Fill posterior contradictorio conserva C01, cuarentena/fence; nunca cambia cuenta/Operation a C04. |
| 6. Misma Strategy/dos MM | S en P1/A con MM-X y P2/B con MM-Y: una Signal(s,k), dos decisiones por asociación, distintas cuentas/Operation/MMState, módulos/configs sellados. Target update de P1 no elimina B. Replay de s no ejecuta otra vez tras rotación de A; B tampoco pierde su delivery original. |
| 7. Sin elegibles | Fanout persiste decisión sin destino/cause por asociación y señal; Strategy y analytics conservan progreso. Llegada de cuenta elegible habilita sólo señales futuras. Ningún backfill, reset técnico ni ejecución sintética. |

### 14. Configuración mínima ilustrativa

Fragmento del futuro `ConfigSnapshot`, **ilustrativo y no desplegable**: C01…C05/S-A…/MM-A… son aliases, no inventario real ni selección económica. `accounts` se resuelve del catálogo existente con sus fechas reales, bindings, RuleSets/program terms y economía; no volver a copiar las cinco cuentas en esta nota. `money_managers` referencia objetos GerardMMDef íntegros aprobados por Owner, sin valores de ejemplo convertidos en defaults.

```json
{
  "pools": [{"id":"P","account_ids":["C01","C02","C03","C04","C05"]}],
  "pool_associations": [
    {"id":"A","pool_id":"P","strategy_id":"S-A","mm_config_id":"MM-A","config_version":1,"enabled":true},
    {"id":"B","pool_id":"P","strategy_id":"S-B","mm_config_id":"MM-B","config_version":1,"enabled":true},
    {"id":"C","pool_id":"P","strategy_id":"S-C","mm_config_id":"MM-C","config_version":1,"enabled":true}
  ]
}
```

No `AccountStrategyIDs` ni MMConfigPerStrategy manuales para estas asociaciones; runtime deriva ambos. La misma Strategy puede repetirse en otra asociación. Config valida referencias, identidades únicas, capacidades de módulo/indicadores, compatibilidad instrumento/phase, fechas, moneda y RuleSet exacto. Defecto estructural impide composición; indisponibilidad runtime de una cuenta impide reclamar sólo esa cuenta. Legacy sin pools conserva cfg.MM/cfg.Provider; no mapear silenciosamente pool incompleto a esos globals.

### 15. Auditoría de boundaries y mapa exacto de cambios

Todas las rutas de producto de esta tabla son relativas a `xKoRx/echo` en el SHA S01; **HEAD** indica inspección de fuente, **TEST** sólo existencia de tests leídos/buscados, no ejecución. Los símbolos nuevos se nombran como create. El mapa es allowlist de S02/S04; adición ajena requiere `PLAN_CONFLICT` al Manager, no expansión unilateral.

| Boundary / clase | Evidencia HEAD y símbolo | Acción obligatoria / gap |
|---|---|---|
| Signal / REUSE | `v3/sdk/futures/domain/signal.go`: Signal, SignalProvenance, DeriveSignalID | Sin cambio funcional; Signal conserva intents/ciclo e independencia. |
| Fanout / EXTEND | `v3/sdk/futures/strategy/fanout.go`: FanoutState.Linearize, ApplyTargetSet, AccountStrategyTarget; `v3/sdk/futures/domain/fanout.go`: SignalDelivery; `v3/core/internal/functions/futures_signal_fanout.go`: handleSignal/handleTargetSet | Cursor global, decisiones por asociación/no-destino, updates por asociación y ACK; targets históricos, generation, dedup a través de rotación. |
| Account owner / EXTEND | `v3/sdk/futures/provider/{state.go,state_clone.go,input.go,effects.go,engine.go,admission.go,reservation.go}`: OwnerState, Apply, handleAdmission, handleRevalidate; `v3/core/internal/functions/futures_provider_rules.go`: decodeInput/Invoke | Claim/affinity/fence/drain y proyección de availability, MM account policy y revisión contable causal. No owner paralelo de capacidad. |
| Riesgo/lifecycle / REUSE + WIRING | `v3/sdk/futures/provider/risk_eval.go`: EvaluateEconomicRisk, EvaluateLifecycle; `v3/sdk/futures/accounting/ledger.go`: Revision, Ledger.ApplyFill | Reusar kernels sin duplicar fórmulas; integrar revisión autorizada y program terms. Ledger no se modifica en S02 salvo prueba que demuestre contrato insuficiente → Manager. |
| Operation / EXTEND | `v3/sdk/futures/operation/{engine.go,engine_inputs.go,runtime.go,provider.go,wire.go,mm.go}`: OwnerState, Engine, MMDecision, MoneyManager; `v3/sdk/futures/domain/{admission.go,reservation.go,operation.go}`; `v3/core/internal/functions/futures_operation.go`: decodeInput/emitEffects | Resolver/pin MM por binding, AssignmentControl, propagation epoch, no-risk fence, cancel pendientes y drain evidence. Gestión vieja siempre correlacionada. |
| Config / EXTEND | `v3/sdk/futures/config/{snapshot.go,composition.go,views.go,mm.go}`: ConfigSnapshot.Validate, ResolveMoneyManager, EffectiveRuleSet, MMConfigSnapshot | Pools/asociaciones, fechas de catálogo, MM registry por asociación/version, RuleSet por binding/contexto, persistir configs referidas por operaciones. |
| Composición / WIRING | `v3/core/internal/futuresruntime/{runtime.go,snapshot.go,recovery.go}`: Compose/Registrations/BridgeCommandEnvelope; `v3/core/cmd/echo-core/main.go`: registerFuturesIfConfigured | Una sola WithSpec por TypeName con dispatcher por ctx.Self().Id. HEAD repite registrations por Strategy/cuenta y bucle de Strategy en main; no asumir multi-instancia funcional. Registrar nuevo owner/ValueSpecs y bootstrap idempotente de config; activar analytics requerido. Config bootstrap: dispatcher instala snapshot validado idempotente en primera invocación de key; main publica PoolConfigUpdate/config de Strategies por ingress existente SDK messaging con config_version, nunca escribe keyed state desde Go local. Reintentos no resetean turns/cursos. |
| Analytics / REUSE + EXTEND | `v3/core/internal/functions/futures_market_analytics.go`: tgIngestAll/TGOwnerViewFor/delegate; `v3/sdk/futures/analytics/engine.go`: OwnerState/Input/Effect; `v3/sdk/futures/analytics/tg/{view.go,owner.go}`: TGSnapshot/SnapshotViewForTrigger; `v3/core/internal/functions/futures_strategy_engine.go`: tgScopeForTrigger; `v3/sdk/futures/marketctx/views.go` | Transporte causal para MM, demands comunes, owner state serializable; vistas locales no son autoridad distribuida. Crear `v3/sdk/futures/analytics/observations.go` y `v3/core/internal/functions/futures_analytics_observations.go`. |
| S2 indicadores / WIRING | `v3/sdk/futures/strategies/s2/{s2.go,indicators.go,warmup_requirements.go}` | Mover kernels preservando fórmulas a create `v3/sdk/futures/analytics/s2/indicators.go`; Strategy consume snapshot; preservar build SDK y golden outputs. El driver histórico que aún no transporta observaciones no certifica el nuevo camino; su adopción sigue diferida con error explícito, sin fallback de cálculo dentro de Strategy pool. |
| MM / EXTEND | `v3/sdk/futures/gerardmm/{gerardmm.go,config.go}`; `v3/sdk/futures/strategies/tgmm/{tgmm.go,minimum_policy.go}` | Nueva política de presupuesto; extracción/reuso de policy por cuenta. Crear `v3/sdk/futures/operation/account_policy.go`, `v3/sdk/futures/gerardmm/account_policy.go`, `v3/sdk/futures/strategies/tgmm/account_policy.go`; no tocar fórmulas ajenas. |
| Bridge / REUSE + EXTEND + VERIFY | `v3/futures-bridge/core/bridge.go`: Run/Snapshot; `internal/session/{session.go,gate.go}`: RunRecoveryBarrier/handleSubmit/JournalCorrelationResolver; `core/config/options.go`; `core/capabilities/{adapter.go,reconciliation.go,journal.go}`; `adapters/journalfs/journal.go`; `adapters/kafka/command_consumer.go`; `adapters/ninjatrader/{adapter.go,helpers.go}`; `v3/futures-bridge/cmd/futures-bridge/main.go`: buildNinjaTraderAdapter | Sesiones/journal per account ya existen; añadir fence/generation y drain snapshots, validar dispatch sin cruzar cuentas. Paths internal/core/adapters bajo `v3/futures-bridge/`. |
| NT wire/AddOn / EXTEND + VERIFY | `v3/futures-bridge/core/ntx/{frame.go,server.go,observations.go}`: Frame/Server.ActiveConn; `v3/futures-bridge/addon-ninjatrader/EchoExecutionAddOn.cs`: OnTimerSnapshot/ExecuteCommand | HEAD single resolvedAccount/ActiveConn. Multiplexar con una lane lógica/conexión por cuenta, mismas familias ntx.v1; AddOn array de bindings y contexto per binding. Cada lane autentica provider ref exacta; un supervisor NT sin dominio. Reusar Server single-connection por lane con listener exclusivo resuelto por binding; main deja de reutilizar un único listen-addr global para todas las cuentas. No multiplexar eventos sin identidad en un socket compartido. El feed de mercado canónico sigue único, no una copia por lane. No un proceso NT por Strategy/pool. |
| Campaña / REUSE conceptual + DEFER | `v3/backtester/platform_campaign.go`: selectTurn/resumeExpiredPlatformPause; `v3/backtester/platform_operability.go`: StrategicEntryBudgetV1 | Read-only. Convergencia futura del driver, no importar paquete backtester a Core/SDK. |
| Pool / NEW | create `v3/sdk/futures/pool/{contracts.go,state.go,engine.go}`; create `v3/core/internal/functions/futures_pool_manager.go` | Reducer puro + wrapper StateFun mínimo, selección sin tipos monetarios, snapshot/restart. |
| Wiring schemas / EXTEND | `v3/sdk/statefun/futures_constants.go`; `v3/core/internal/functions/{futures_strategy_types.go,futures_market_types.go}`; `v3/core/deploy/flink-statefun/{develop,production}/module.yaml` | S02 puede modificar declaraciones del source para nuevos mensajes/ValueSpecs/owner y egress; no aplicar manifests ni tocar infraestructura. S01 no los cambia. |
| Pruebas / NEW | create `runtime_pool_test.go` en paquetes pool, strategy, provider, operation, config, gerardmm, tgmm, analytics, futuresruntime, functions, futuresvertical, bridge/core, bridge/internal/session, bridge/adapters/ninjatrader, bridge/core/ntx; create `v3/futures-bridge/addon-ninjatrader/tests/RuntimePoolContractTests.cs` | Fixtures aislados y sin egress real. En rutas bridge usar prefijo `v3/futures-bridge`; en SDK `v3/sdk/futures`; en Core `v3/core/internal`. Tests existentes se conservan; modify permitido de `v3/sdk/futures/strategies/s2/{fixtures_test.go,s2_test.go}` exclusivamente para suministrar las nuevas observaciones con resultados golden idénticos. Si más fixtures requieren cambiarse, presentar la lista al Manager; nunca borrar asserts ni ajustar resultados para ocultar diferencias. |

**VERIFY físico acotado, dentro de S02:** spike P0-NT de compilación del AddOn contra assemblies NT de versión autorizada o inspección del contrato de API disponible y harness de dos/cinco lanes. Entregar matriz command→account→ACK/fill→M2 y cancel/replace/restart. No abrir/cerrar operaciones reales ni desplegar. Si faltan assemblies/terminal autorizado, declarar `PHYSICAL_NOT_DEMONSTRATED`, conservar ese bloqueo de certificación/egress en G2/G4; no afirmar que SIM prueba NT. El diseño no depende de una API financiera nueva: reutiliza Account.All/Submit/Cancel/Change existentes; capacidad concurrente de eventos/callbacks/reconnect es incertidumbre física a verificar. No quinto shot: S02 implementa y documenta lo verificable, S03 audita, S04 corrige; eventual certificación física Owner-gated es obligación de rollout externa, explícita, no una fase inventada ni aceptación tácita.

### 16. Pruebas y criterios de aceptación

Prioridad funcional antes de cobertura. Nuevos desarrollos ≥95% según perfil global vigente, con reporte por paquete/archivos afectados; no cobertura global inventada ni exclusión del código difícil. No ejecutar `go test ./...` desde repo/SDK sin verificar tests con efectos externos (Environment Contract registra seeds ETCD peligrosos). S02 usa paquetes SDK futures/Core futures/bridge locales y harness sin red; S03 repite sobre SHA exacto, S04 prueba regresiones específicas más suite acordada.

1. Pool reducer: cinco cuentas/tres asociaciones, FIFO real con fechas desordenadas y empates, ausencia de fecha, afinidad multiday, misma Strategy/dos asociaciones, claims simultáneos/reordenados, no doble ownership, no cambio por cierre individual, retorno por calendarios distintos, disabled/config update prospectivo.
2. Model checking pequeño por permutación de mensajes y serialización/restart tras CADA transición claim/install/activate/pause/fence/drain/release. Assert máximo un claim activo por cuenta y un ACTIVE por asociación; no liberación con admission, reserva, posición, órdenes inciertas o fence pendiente. Epoch antiguo nunca habilita new-risk.
3. Fanout: replay de OPEN consumido en C01 después de C04; signal con NO_TARGET seguido de cuenta elegible; asociación agregada después; replay después de evicción del cache; reinicio con otro proceso; target partial updates cruzados; cero duplicados y gestión por ciclo a cuentas originales. Historial Signal byte-identical.
4. Provider/MM: revisión contable monotónica/contexto, PAUSE distinto de terminal breach, day reset no borra latches, mismas políticas evaluadas sin Operation activa; 53/300 y 1/1000 sin clamp/retirada, control positivo con breach real/rechazo venue. No modificar resultados técnicos de Strategy por economía.
5. Analytics: procesos distintos sin puntero compartido, out-of-order/future snapshot, epoch/revisión incorrectos, demanda sólo MM, missing analytics, quote/fill/economics antes/después del corte, crash/restart y equivalencia de kernels extraídos. Consumers nunca recalculan indicadores; misma Strategy/dos pools emite una vez.
6. Registro real del builder: tres Strategies/cinco cuentas, un spec por TypeName y dispatch correcto. Roundtrip todos los ValueSpecs declarados en source manifests; bootstrap idempotente no requiere harness in-process para distribuir targets/config.
7. Bridge: cinco sesiones/config bindings, tuple account/physical immutable en submit/cancel/replace y observaciones; M2 redelivery/ACK incierto/crash antes/después de SUBMITTING; acción reductiva mientras fence corta add; snapshot flat con orden viva NO drena; late fill nunca llega al sucesor; lane reconnection no adopta cuenta por runtime ID cambiado. SIM y API compile se reportan separados de físico real.
8. Integración: siete secuencias §13, tráfico continuo de Strategy durante rotación y sin elegibles, restart con intents en tránsito, dos pools solapados, observabilidad de cada oportunidad. Carga sintética de 200 cuentas y conjunto de 256 targets sin retener historial vivo ilimitado; ninguna campaña económica completa ni señales forzadas en cuentas reales.

### 17. Migración, observabilidad y rollback

Config pools es opt-in validado antes de habilitar ejecución. Fixed bindings existentes conservan shape sin metadata pool, pero participan de la exclusividad account-wide como propietario fijo mientras están habilitados o drenan. Cuenta fija y pool simultáneos ⇒ error de config/claim; no bypass por metadata ausente. Para migrar: stop-entry del binding fijo, drenar y certificar barrera, preservar historia y afinidad verificada de executions previas, instalar asociación/binding derivado. Afinidad histórica desconocida ⇒ `MIGRATION_AFFINITY_UNRESOLVED`; no asumir libre. No reapuntar IDs de operations antiguas ni resetear cursores.

Config MM nueva sólo para próximas Operations; Operation viva mantiene módulo/config exactos aun si se deshabilita asociación. El MoneyManager inyectado es un dispatcher sin estado económico: elige implementación por MMConfigSnapshot sellado, no por cfg.MM vigente; el catálogo versionado vive en la composición/estado de binding. Conservar materializaciones/versiones requeridas por keyed state; módulo ausente durante recovery falla visible antes de nuevas entradas. Startup config desde ETCD existente; los ejemplos no autorizan escribir ETCD. Datos operacionales de asignación/analytics son mensajes de dominio, no overrides de config por archivo.

Egress auditable en canales existentes: claim outcome, affinity fixed, assignment phase/epoch, pause reason/authority/account-day/revision, target revision, delivery/no-target, drain barriers, stale/identity conflict y late fact. OTel contadores de decisiones/rotaciones/bloqueos con etiquetas acotadas; IDs de señal/orden/cuenta como campos de evento/traza, no labels sin límite. Journal + cursores/tombstones guardan corrección; dashboards/proyecciones no autorizan trading.

Rollout propuesto, no ejecutado: tras G4 y autorización Owner independiente, verificar runtime único y cuentas/lane autorizadas, snapshot/savepoint compatible, carga config pools inicialmente disabled, reconcile/readiness, habilitar asociaciones prospectivamente y observar las siete secuencias cuando ocurran. Rollback: deshabilitar nuevas entradas, conservar owners extendidos hasta drenaje, restaurar configuración fixed sólo tras release confirmado. Nunca cargar binary anterior sobre state nuevo ni borrar affinity/dedup. Si hay exposición/ambigüedad, rollback de ejecución queda bloqueado hasta reconciliación; Strategy puede continuar en shadow.

### 18. Límites y resultado S01

Diseño implementable candidato; no business decision abierta. S01 resolvió arquitectura y protocolo, no ha probado código nuevo. Las capacidades físicas NT y el productor LIVE de revisión contable no quedan certificadas por interfaces/tests históricos. S02 debe demostrar contratos y cableado local con fuentes causales; una falta de evidencia física se reporta en G2/G4 y bloquea egress, no se oculta como PASS. Si el spike revela que la API no soporta la lane diseñada o falta un dato semántico imprescindible, G2 `blocked`/PLAN_CONFLICT al Manager dentro de los cuatro shots.

Diferidos explícitos: driver backtester en su otra rama, permisos comerciales, rentabilidad, UI, otros adaptadores, multi-Strategy por cuenta, múltiples cuentas activas por asociación, netting/portfolio, hot-swap arbitrario de MM en Operation viva. No cambios en controles TradesGerard. Manager acepta gates; cada agente entrega sólo review/blocked y STOP.

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
