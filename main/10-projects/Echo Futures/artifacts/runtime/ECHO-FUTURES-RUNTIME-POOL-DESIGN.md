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

**CANDIDATO_R4 / LISTO_PARA_REVISIÓN_DEL_OWNER.** Diseño de la extensión de asignación y ejecución sobre Echo existente. Las decisiones explícitas del cuarto turno del Owner reemplazan las recomendaciones R1–R3 contradichas. La aceptación final del diseño corresponde al Owner; esta nota no declara implementación, pruebas ejecutadas, despliegue ni cierre de sesión/proyecto.

Mandato inicial: `Markdown pegado(3).md`, PROMPT_VERSION 1, actualizado por los turnos posteriores. Autoridad: [[Echo Futures]]. El carril runtime se implementará en su rama de producto; backtester seguirá investigando/validando en otra y adoptará los cambios gradualmente después. No se exige sincronización inmediata para avanzar. Agents-OS continúa sobre master, sin ramas ni PRs para esta documentación.

**Corte leído R4:** `xKoRx/echo@95e9d105182af99d03700f4b5def24bf9fc6b5fd`, master resuelto nuevamente sin cambio desde R3. Lectura adicional acotada: Signal y fanout, Architecture V2, Technical SPEC V1 y D2-08. Se conserva la inspección R1–R3 de composición, owners, MM y bridge; no se inspeccionó WIP local ni infraestructura viva. No se modifican [[TRADESGERARD-CONTROL]] ni [[TRADESGERARD-CONSOLIDATION]].

## Contenido

### 1. Decisiones de producto vigentes

| Decisión | Opción confirmada | Consecuencia |
|---|---|---|
| Unidad configurable | Pool + Strategy configurada + MM/configuración. | AccountStrategy efectivo automático; no asignación manual de Strategy/MM por cuenta consumible. |
| Concurrencia | Una cuenta activa por asociación; varias asociaciones de un pool y pools independientes simultáneos. | No mutex de trading por pool ni del sistema. |
| Afinidad | Cuenta que operó A seguirá con A, aunque pasen días; nunca B. | Persistir afinidad separada de disponibilidad y turno. No migraciones automáticas de asociación/pool en I1. |
| Permanencia | Operar la cuenta seleccionada hasta que muere o pasa el challenge. | Pausa diaria, fin de sesión, trade cerrado o problema temporal NO liberan la cuenta ni toman una sucesora. Esto sustituye la rotación por pausa de R1–R3 y de la analogía de campaña anterior. |
| Selección | Candidata elegible más antigua por creación real. | Aplicar FIFO al primer destino o después de desenlace definitivo; no interrumpir una cuenta sana porque haya otra disponible. |
| Strategy | Agnóstica a cuenta, MM y pool; produce Signal y lleva su ciclo técnico. | Una evaluación por instancia técnica; la multiplicación comienza en fanout. No nuevo aggregate de operación canónica. |
| MM | Contexto real de la cuenta, programa/fase, economía e indicadores. | Sizing y gestión propios; diferencia challenge/funded sin trasladar economía a Strategy. |
| Indicadores | Calculados en analytics de Echo y publicados a Strategy y MM. | Consumidores sin kernels propios; no cálculos de estrategia en NinjaTrader. |
| Remanente | Presupuesto operativo completo aunque supere el remanente positivo al piso. | No recorte, rechazo o retiro anticipado sólo por esa comparación; el breach real conserva su tratamiento. |
| Cohorte | Soportar las cinco cuentas existentes y la composición/rotación pedidas. | No requisito de que todas generen trades, no señales forzadas ni pools extra para garantizar utilización. El Owner puede operar manualmente las no utilizadas, fuera del ownership automático activo. |
| Paralelismo de desarrollo | Runtime en su rama; backtester en otra, sin detener su avance. | Adaptación progresiva posterior; divergencia temporal identificada no bloquea este diseño ni exige recertificar campañas. |
| NinjaTrader | Feed y gateway físico exclusivamente. | Sin pool, afinidad, MM, selección comercial ni reglas de negocio dentro del AddOn. |

Los módulos/valores definitivos se configurarán con los resultados del Owner. K05/SR sigue siendo candidato, no selección definitiva. No se impone un número fijo de Strategies ni MM por cuenta. Objetivo Owner: domingo 2026-10-18 por la noche; no promesa de entrega ni estimación. Permisos comerciales de automatización quedan fuera de este encargo por instrucción del Owner.

### 2. La definición histórica existe: Signal, no otra entidad

**OBSERVADO_EN_CÓDIGO, no prueba ejecutada:** `v3/sdk/futures/domain/signal.go` define `Signal` como salida canónica inmutable de Strategy. Contiene SignalID, StrategyID, StrategyCycleSeq, Intent, InstrumentID, Direction, Details, CreatedAt, ValidUntil y Provenance. No contiene cuenta, provider, MM ni estado de ejecución. Los intents son OPEN, REDUCE, CLOSE y CLOSE_ALL.

**AUTORIDAD DOCUMENTAL:** Architecture Candidate V2 §2.2 denomina esa salida Signal y establece que `strategy_cycle_seq` identifica el ciclo técnico como escalar, NO como nuevo aggregate. Technical SPEC V1 §9–11 separa Signal, SignalDelivery y Operation. D2-08, fechado 2026-09-28, explicita Strategy account-agnostic, ausencia de feedback físico hacia Strategy y la decisión sin `StrategyTrade`/`operation_key`; documenta también el seam legacy `ReferenceEvent → Signal`. Esa última referencia es evidencia de diseño histórico, no certificación de un adaptador Forex ejecutado en esta sesión.

**Corrección del análisis R2/R3:** tratar el nombre/correlación canónica como algo por inventar fue un error de recuperación del asistente. No hay evidencia de pérdida de esa definición: está tanto en documentación como en el source inspeccionado. No crear CanonicalOperation, StrategyTrade, otra Signal ni un ciclo financiero global.

La lógica ya acordada es:

```text
Strategy → Signal → signal_fanout → SignalDelivery
                               → echo/operation por AccountStrategy
                               → admisión → Operation + MoneyManagement
                               → reserva/revalidación → Order → Fill
```

Operation es la ejecución account-specific: cuenta, AccountStrategy, StrategyCycleSeq, contrato físico pinneado, MMState, órdenes y fills. SignalDelivery conserva la Signal y añade el destino AccountStrategy. La cuenta replica la intención canónica, no copia los fills ni los importes de una cuenta maestra. Una cuenta puede rechazar/cerrar antes sin alterar el ciclo de Strategy ni otras ejecuciones.

**Lectura directa de comportamiento:** `strategy.FanoutState.Linearize` produce deliveries deterministas mediante `domain.DeliveryFromSignal`; filtra OPEN por Enabled/instrumento, pero entrega REDUCE/CLOSE/CLOSE_ALL también a bindings deshabilitados para nuevas entradas. Dedup existente: `(account_strategy_id, signal_id)`. `ApplyTargetSet` aplica versiones prospectivas. Esta mecánica se reutiliza.

Las referencias D2 antiguas sobre indicadores privados en Strategy son históricas en ese aspecto: R4 conserva sus contratos Signal/ciclo/ejecución, pero no reintroduce ese ownership, sustituido por el mandato vigente de analytics compartido y la consolidación TG. No usar una lectura histórica para revertir el cálculo compartido.

### 3. Modelo mínimo e identidades

La configuración humana establece pools y asociaciones; el runtime elige la cuenta concreta y materializa el AccountStrategy existente.

| Elemento | Identidad / datos mínimos | Autoridad |
|---|---|---|
| Strategy configurada | strategy_id, módulo, parámetros técnicos, instrumento/requisitos. | Owner strategy_engine existente; estado técnico, independiente de cuentas. |
| Pool | pool_id + miembros del catálogo de cuentas. | Configuración; no saldos ni fase duplicada. |
| Asociación | ID estable, pool_id, strategy_id, referencia MM/config y enabled. | Configuración; cambiar versión MM no crea otra asociación. |
| Asignación | asociación → cuenta, generación, estado de reclamación/activación. | PoolManager; una reclamación pendiente o cuenta retenida por asociación. |
| Exclusividad/afinidad | cuenta → asociación de origen, Strategy, generación aceptada. | Estado account-wide junto al owner de cuenta; autoridad única de claim. |
| AccountStrategy efectivo | ID estable derivado de cuenta + asociación, configuración MM/contexto. | Materializado/reutilizado automáticamente, sin alta manual del Owner. |

Los nombres nuevos de esta tabla son conceptos del delta, no afirmaciones de structs/flags ya existentes. Reutilizar IDs y mensajes actuales cuando encajen. No derivar IDs de reloj de reinicio ni de nombres efímeros de sesión NT. AccountStrategyID debe respetar la restricción existente de no incluir `:`.

Ejemplo de configuración conceptual, NO un JSON/CLI actualmente soportado:

| Pool | Miembros por creación | Asociaciones |
|---|---|---|
| P | C01, C02, C03, C04, C05 | A: Strategy-A + MM-A; B: Strategy-B + MM-B; C: Strategy-C + MM-C |

A puede retener C01, B C02 y C C03; C04/C05 quedan disponibles. Si A se pausa, C01 sigue en A y C04 sigue libre. Si C01 muere/pasa el challenge y queda drenada, A selecciona la más antigua elegible entre las disponibles. B/C no cambian. La misma Strategy en otro pool tiene otra asociación y puede producir otra ejecución de la misma Signal, sin otra evaluación técnica.

No es obligatorio separar pools por empresa. La compatibilidad se resuelve para la asociación/MM, instrumento, programa/fase y capacidad del adaptador; Strategy no contiene `if providerName`. Una candidata inicialmente no disponible se omite con causa; una cuenta YA asignada temporalmente no disponible se suspende sin reemplazarla.

### 4. PoolManager y proyección sobre el fanout existente

**PROPUESTA TÉCNICA:** un owner pequeño de asignación en Core, key pool_id, conduce los varios turnos de sus asociaciones; el owner account-wide existente confirma la exclusividad de la cuenta. No nuevo microservicio, Redis, lease por TTL ni scheduler de trading paralelo.

Responsabilidades y comunicación:

1. Al habilitar una asociación sin cuenta o finalizar su anterior asignación, PoolManager selecciona por `(account_created_at, account_id)` entre candidatas compatibles, sin otro claim y con afinidad libre/propia. La afinidad de otra Strategy siempre excluye.
2. Persiste una solicitud de claim con asociación, cuenta y generación. No hay dos claims pendientes por asociación. Si dos pools reclaman la misma cuenta, el owner account-wide serializa y sólo uno obtiene confirmación; el perdedor prueba la siguiente candidata elegible.
3. Tras confirmación, instalar/reutilizar AccountStrategy, contexto real y MM de esa asociación. Confirmar esa instalación antes de activar OPEN. Generaciones/solicitudes viejas se absorben idempotentemente.
4. Publicar la proyección de targets mediante `FanoutTargetSet`/`AccountStrategyTarget` existentes, extendidos sólo con la metadata de asociación/asignación que se requiera. Una Strategy tiene UN publicador/versionador del target-set completo: sus cambios de varios pools se combinan en el owner de fanout, no en writers que reemplacen y borren targets ajenos.
5. Fanout sigue produciendo SignalDelivery. Para asociaciones pool-managed, la cuenta debe coincidir con el claim/generación instalados; Operation y Provider comprueban el contexto antes de admisión/nueva exposición y en revalidación. Signal permanece inmutable y sin campos de cuenta/pool/MM; la metadata de routing pertenece al envelope/config de delivery.
6. En pausa se deshabilita OPEN del binding, no su recepción de gestión de operaciones existentes. Al reanudar se activa el MISMO binding/cuenta de forma prospectiva. En desenlace definitivo se bloquean OPEN y se conserva el destino saliente para drenar y reconciliar antes de liberar el turno y activar sucesora.

La publicación de targets es una proyección, no la autoridad económica ni de exclusividad. Un mensaje de target atrasado no puede volver a habilitar una generación revocada. No se supone atomicidad distribuida entre las dos keys: el protocolo confirma pasos y mantiene el destino cerrado hasta que el contexto/claim están instalados. Reintentar la misma solicitud después de un crash consulta/reproduce el mismo resultado; no adjudica otra cuenta silenciosamente.

**Carrera de deduplicación al rotar:** el dedup existente por AccountStrategy no basta POR SÍ SOLO para evitar que una Signal ya consumida por A/C01 vuelva a aparecer en A/C04, porque cambia AccountStrategyID. Conservar en fanout el progreso/decisión de entrega por asociación además del dedup actual, usando las identidades y orden existentes `(run, strategy_eval_seq, signal_seq)`/SignalID. Una Signal ya tratada por una asociación no se remapea a una sucesora; otra asociación expresamente suscrita sí puede recibirla. Persistir destino y progreso con los efectos de fanout. No nueva cola de señales ni replay de OPEN vencidos/descartados durante una pausa.

Mantener el guard de ciclo de Operation por StrategyCycleSeq. Un CLOSE/REDUCE viejo no cierra un nuevo ciclo de la sucesora. Respetar el caso ya contratado de admisión pendiente y siguiente ciclo acotado en Operation; no sustituirlo por otra cola dentro del pool.

### 5. Permanencia hasta pérdida o aprobación

La asignación y la afinidad no terminan al cerrar una operación individual. Para el flujo challenge solicitado:

| Hecho | Acción | ¿Selecciona otra cuenta? |
|---|---|---|
| Trade termina; cuenta sigue apta. | Conservar cuenta y AccountStrategy. | No. |
| Meta/pausa diaria o cierre de sesión. | Impedir entradas según política; gestión/cierre según MM y reglas; conservar asignación. | No. |
| Próxima sesión/fin de pausa. | Revalidar contexto, reanudar misma cuenta sin reset de pisos/historial. | No. |
| Falta temporal de feed/quote/indicador o desconexión. | Suspender nuevas entradas en el scope afectado; recuperar/reconciliar. | No. |
| Cuenta definitivamente perdida/vencida según hecho o regla efectiva. | Bloquear entradas, drenar/reconciliar, preservar historia y afinidad. | Sí, después de drenaje. |
| Challenge completado según sus condiciones y autoridad. | Terminar la ejecución de evaluación, bloquear entradas y drenar; conservar cuenta para su lifecycle posterior. | Sí, después de drenaje. |
| Orden o exposición incierta. | Conservar claim; reconciliación por identidad. | No. |
| No hay candidata al necesitar sucesora. | Asociación esperando disponibilidad/configuración; otras siguen. | No inventa cuentas ni señales. |

Aprobar no equivale a destruir la cuenta ni a inventar credenciales funded. Las condiciones de pase incluyen lo que establezca el contexto del programa, no sólo alcanzar una cifra aislada de PnL. La cuenta pasada conserva A. Si se confirma una fase funded utilizable posteriormente, sólo vuelve a ser candidata de su asociación; no interrumpe otra cuenta que esa asociación ya retiene. En fase funded no existe otro pase de challenge: no crear una rotación por cada payout/pausa; se conserva la cuenta salvo desenlace terminal o control explícito del Owner.

La regla nueva es distinta de la campaña investigativa que rotaba al pausar. No presentar ambas como equivalentes. Tampoco usar una cuenta sucesora durante una pausa de la anterior para forzar utilización de inventario.

**Drenaje:** ningún pending admission, orden pendiente/ejecutable/incierta, exposición ni comando sin resolver que pueda producir efectos sobre la saliente. El owner Operation/M2/Provider certifica su parte por hechos; PoolManager no calcula por su cuenta que estar flat basta. Fills/ACK tardíos siempre conservan cuenta, Operation, orden y contrato originales.

**Paradas e intervención manual:** deshabilitar una asociación/pool no cambia afinidad ni rota; stop-entry, drenaje y flatten son acciones distintas. Para trade manual, la cuenta sale de la autoridad automática activa y se reconcilia antes de reactivarla. No coexistencia automática/manual implícita, ni automatizar el uso de todas las cuentas por esta razón.

### 6. Strategy, analytics, MM y reglas por cuenta

```text
Feed observado → market_stream → barras → kernels de indicadores
                                      → observaciones causales
                                          ├→ Strategy → Signal → fanout
                                          └→ MM según su trigger

PoolManager → proyección de bindings efectivos del fanout
SignalDelivery → owner Operation → admisión → Operation + MM
                                   → Provider/reserva/revalidación
                                   → bridge → NinjaTrader
NinjaTrader → órdenes/fills/posiciones/quotes → owners financieros
```

Strategy comparte su ejecución técnica por strategy_id y no recibe feedback de ninguna cuenta. Una nueva asociación añade deliveries, no otra evaluación del mismo trigger. Parámetros técnicos distintos pueden definir otra instancia. El estado y las señales técnicas siguen avanzando si una o todas las cuentas están pausadas; rotar no hace rewarmup ni reabre un ciclo ya consumido.

Analytics calcula la unión de demandas de Strategy Y MM, incluidos indicadores exclusivos del MM. Mismos kernels para ambos conductores, identidad de cálculo por datos/stream/contrato/timeframe/parámetros/calendario/seed/epoch/versión que realmente cambien resultados. No nuevo indicator service ni imponer TG como API universal. Runtime actualiza incrementalmente; backtester puede usar tablas preparadas sin adelantar disponibilidad.

**Serving de MM:** la referencia Go `tgPublished` observada en R1–R3 no acredita serving distribuido. Completar la publicación de observaciones inmutables a los owners consumidores a través del transporte/estado existente; las vistas locales de cada consumidor son proyecciones recibidas, no otro calculador. Scope de Strategy sigue usando la observación ligada al trigger. MM fija una vista por evaluación con stream/epoch/revisión/frontera causal adecuados y no lee un valor futuro porque el productor avanzó. Conservar orden same-instant; disponibilidad desconocida se identifica con causa y no bloquea reducciones que no requieren ese indicador.

Quote ejecutable y economía son hechos vivos separados de los indicadores: MM puede actuar por quote/fill/contexto económico sin una vela ni Signal nueva. `last` no reemplaza bid/ask observado. SR/H1 requieren autoridad de datos suficiente: el adaptador suministra datos/barras nativas cuando corresponda y Echo calcula indicadores; no rebautizar barras incompletas como completas para armar la Strategy.

**MM/contexto:** resolver módulo/config por asociación y fase a través de la composición compartida, eliminando el supuesto de un único cfg.MM para todos los bindings. Mantener MMState por Operation. La operación abierta conserva módulo/config/presupuesto; configuración nueva es prospectiva. El RuleSet completo efectivo se resuelve por cuenta/programa/fase, no desde el Provider global del snapshot. Límites efectivos de seguridad se reevalúan sin reemplazar en caliente el MM de una operación.

PoolManager sólo consume disponibilidad/fase/desenlace. Provider/contabilidad conservan las fuentes de reglas, economía, pisos y progresos. No otro ledger del pool ni clase de MM por empresa. Sustituir referencias fijas GAU50 donde el programa concreto lo requiera, por términos y referencias económicas explícitas; nunca reiniciar la referencia al arrancar un proceso.

### 7. Presupuesto completo: contrato conservado, integración posterior

Se conserva el mandato R3: si el MM determina presupuesto 300 y quedan 53 al piso, intentar con 300; si determina 1000 y queda 1, intentar con 1000. No bajar presupuesto/cantidad/stop por ese remanente, no rechazar únicamente porque presupuesto > remanente positivo y no declarar pérdida anticipada por ese criterio. Cantidad, ticks, costos y capacidad física siguen siendo reales. Esto no modifica automáticamente la lógica de objetivos del MM ajena al remanente.

El piso y el PnL no se falsean. Cuenta ya bloqueada no abre; si la economía observada alcanza su límite, se aplica el desenlace y la rotación tras drenaje. No garantizar fill ni pérdida exacta: presupuesto, envío, aceptación, fill y PnL son hechos distintos. La política se comprueba end-to-end en elegibilidad, MM, admisión/reserva/revalidación y egress para no esconder el recorte/rechazo en otra capa.

**Antecedente R3 publicado:** en `95e9d10`, EntryBudgetV1 devuelve `TG_ENTRY_BUDGET_EXCEEDS_HEADROOM` y la campaña puede producir `LOST_ENTRY_BUDGET_BY_POLICY`. Es otra semántica, ya identificada; no volver a auditarla en cada turno ni convertirla en bloqueo de runtime. Runtime implementa el contrato aquí fijado en el dominio de SU rama; backtester adopta después los deltas pertinentes en SU rama. No exigir ahora que ambos produzcan el mismo resultado ni afirmar paridad entre cortes diferentes.

En la integración posterior se conserva el mismo propietario SDK/contrato, sin paquetes duplicados LiveMM/BacktestMM ni reinterpretar resultados históricos como si hubieran usado la política nueva. Los fixtures de presupuesto se entregan con el delta para que backtester los consuma al actualizarse.

### 8. Delta de implementación por propietario y compatibilidad

| Bloque | Archivos/superficies existentes afectados | Entrega |
|---|---|---|
| Configuración y composición | `sdk/futures/config/{snapshot,views,composition}.go`, `core/internal/futuresruntime/runtime.go`, config/registro StateFun efectivo. | Pools/asociaciones, MM por asociación, reglas/contexto por cuenta, AccountStrategy automático. Un registro por TypeName con dispatch/config por identidad donde sea necesario; no multiplicar procesos para evitar multikey. |
| Asignación | Nuevo owner mínimo PoolManager dentro de Core, estado/claim account-wide existente en provider y contratos SDK acotados. | Varias asignaciones por pool, FIFO, afinidad, retención durante pausas, liberación sólo tras desenlace/drenaje, generaciones idempotentes. Los nombres de mensajes nuevos siguen las familias existentes; no bus/servicio nuevo. |
| Fanout y deliveries | `sdk/futures/strategy/fanout.go`, `core/internal/functions/futures_signal_fanout.go`, envelope de delivery y contexto de Operation. | Targets efectivos de todas las asociaciones combinados por Strategy; guards de asociación/generación, dedup que sobreviva al cambio de cuenta, gestión de saliente preservada. No modificar Signal para añadir cuenta/MM/pool. |
| MM/Operation/Provider | `sdk/futures/operation`, `provider`, `config`, módulos MM seleccionados; funciones Core correspondientes. | Módulos/contextos por binding, presupuesto completo, reservas/revalidación y lifecycle de cuenta preservados. Pending admission sigue anterior a la materialización, no Operation ficticia anticipada. |
| Analytics/inputs financieros | `core/internal/functions/futures_market_analytics.go`, `sdk/futures/analytics`, serving/Vistas y productores reales de quote/economía. | Unión de demandas, snapshots causales en consumidores distintos y restauración; ciclo técnico no recibe datos de cuenta. |
| Ejecución | `futures-bridge/core/bridge.go`, adaptador NinjaTrader y `addon-ninjatrader/EchoExecutionAddOn.cs`. | Comandos/observaciones multiaccount con referencias exactas y M2 por cuenta; cuenta equivocada rechazada, reconexión sin retry ciego. Ninguna decisión de pool/MM dentro del AddOn. |

**Migración acotada:** mantener compatible el binding fijo existente cuando no tiene asociación de pool. La configuración pool-managed exige metadata completa y guards propios; campos ausentes no pueden degradarla silenciosamente a legacy. No inventar nuevos flags para el usuario antes de implementarlos. Habilitación de analytics/composición y armado de órdenes siguen separados.

Incorporar cuentas al pool se hace desde el catálogo/config actual, no desde Strategy. Conservar saldo/piso/fase reales, fecha real de creación y account locator. No duplicar un inventario editable en esta nota. Para datos históricos/importados sin afinidad demostrable, no inventar historial; alta/ownership se resuelve explícitamente por la autoridad operativa. Cambios con exposición se instalan prospectivamente sin reasignar la saliente.

**Extensibilidad mínima:** una nueva Strategy usa Signal y sus requisitos analíticos; un nuevo MM usa su contrato y estado por Operation; un nuevo programa registra términos/reglas efectivos. Cambiar parámetros no toca scheduler/fanout/bridge ni copia paquetes. Otro adaptador no pertenece a esta entrega.

### 9. Secuencias y pruebas de aceptación

| Prueba | Resultado exigido |
|---|---|
| Signal histórica | Struct/ciclo existentes; variar cuenta/MM no cambia Signal, StrategyEvalSeq ni decisiones técnicas; una evaluación alimenta varias asociaciones. |
| Pool compartido | Tres asociaciones/cinco cuentas: tres destinos distintos; dos libres. Concurrencia entre pools y exclusividad global de cuenta. |
| Retención multiday | C01/A cierra trades, alcanza pausa diaria y vuelve al día siguiente en C01/A; C04 no es tomada por A mientras C01 siga retenida. Afinidad no cambia a B. |
| Rotación por desenlace | C01 muere o pasa evaluación: bloquear nuevas entradas, drenar y seleccionar la siguiente elegible por creación. Nunca usar una pausa temporal como desenlace. |
| Cambio de cuenta y redelivery | Reentregar la Signal consumida por A/C01 después de activar A/C04 no crea otra operación. Otra asociación autorizada conserva su consumo independiente. CLOSE viejo no afecta otro ciclo. |
| Claims/restart | Solicitudes simultáneas, confirmación atrasada, crash entre claim y activación: un único destino válido; generaciones viejas no abren; recuperación no inventa otro claim. |
| Ejecución incierta | ACK perdido/fill tardío/cancel race conservan identidades; ninguna liberación por timeout; M2 reconcilia sin duplicados. Pausas de una cuenta no detienen otras. |
| Economía/fase | Casos53/300 y1/1000 sin adaptación por remanente; breach real vigente; MM distinto challenge/funded sin contexto en Strategy ni mezcla de balances. |
| Observaciones | MM consume indicadores por sus triggers en otra réplica/restart, sin recomputar kernels ni leer futuro; SR/H1 y quote tienen disponibilidad demostrable. |
| Cohorte/configuración | Cinco cuentas soportadas con identidad, configuración, exclusión/afinidad y routing verificables; alta de sucesora sin configurar Strategy/MM manualmente. |

La prueba de dominio y del gateway puede conducir escenarios controlados en SIM/demo equivalente y debe identificarse como tal. Cinco cuentas soportadas NO requiere producir cinco trades reales ni que todas se utilicen esa semana. La comprobación de destinos reales es lectura/configuración/conectividad/correlación según la superficie disponible; no se fabrican órdenes para llenar casillas. Una prueba de una cuenta no acredita la concurrencia, pero tampoco se declara fallida la entrega porque una Strategy no emitió una oportunidad para cada cuenta.

No nuevo objetivo de saturación/utilización, no cinco asociaciones impuestas, no pools adicionales para forzar actividad. La operativa manual de cuentas no utilizadas es decisión del Owner, no responsabilidad del planificador automático.

No reejecutar las40 campañas ni exigir rentabilidad para probar el runtime. Suite pequeña de fronteras y walkthrough del gateway, con resultados físicos claramente separados de fixtures. Diseño es implementable; pruebas y operación no están ejecutadas por este carril.

### 10. Dos ramas de producto y convergencia gradual

**Runtime:** implementar este contrato en su rama; puede modificar el SDK compartido de ese checkout y entregar sus tests de contrato. Su aceptación no espera que el CLI/campaña actual se adapte, ni que los resultados de ambas ramas coincidan antes de integrarlas.

**Backtester:** continuar en otra rama con investigación/validación y sus correcciones actuales. Cada resultado identifica commit, módulos/config/políticas y datos efectivamente utilizados. Incorporar gradualmente los deltas ya estabilizados del runtime cuando corresponda, sin paralizar el trabajo en curso.

**Integración posterior:** el implementador/integrador local incorpora conjuntos coherentes de cambios de SDK y adapta el driver offline al contrato, conservando hashes y políticas históricas. No mezclar binarios/config de cortes incompatibles, no cherry-pick parcial que pierda el contrato y no copiar un segundo motor para resolver conflictos. Comparar paridad sólo sobre el mismo corte integrado e inputs equivalentes. La divergencia temporal de ramas es de evolución, no una decisión de mantener dos dominios permanentes.

Los nombres concretos de las ramas se resuelven sobre las que mantenga el Owner; esta sesión no crea ramas/worktrees/clones. Agents-OS sigue editándose directamente en master y esta nota no se mezcla con el control que el otro carril modifica.

### 11. Estado del candidato y límites de evidencia

No quedan preguntas bloqueantes de producto sobre Signal, Strategy, afinidad, permanencia, FIFO, concurrencia, cohorte o paralelismo. Los módulos/parámetros elegidos por el Owner son datos de configuración, no condición para definir los contratos.

La implementación debe recorrer los puntos físicos ya localizados: registro/dispatch real, serving distribuido, productor quote/economía y multiplexado del AddOn. No se dan por certificados por existir structs o por importar el mismo SDK. La última evidencia D6 consultada (2026-10-05, bloqueada por feed stale, cero órdenes) es historia y no un diagnóstico del terminal de hoy.

Diferido: varias Strategies en una cuenta, MM arbitrario por cuenta, varias cuentas simultáneas por asociación, optimizador/hedging/netting de portfolio, UI nueva y otros adaptadores. Cambios de dinero/gestión ajenos a los MM elegidos tampoco se agregan al pool. No reabrir investigación comercial excluida.

La autoridad Environment Contract no se recuperó en R1; el operador local deberá cargarla antes de instrucciones/mutación de infraestructura según Agents-OS, sin convertir esta laguna de lectura cloud en otro rediseño. Este documento se entrega para revisión del Owner; el prompt LOCAL sólo se emite cuando lo solicite. No código, scripts, despliegues, campañas, órdenes, dispatch de agentes ni cierre de sesión desde este análisis.

## Fuentes

### Recuperación canónica R4

- `xKoRx/echo@95e9d105182af99d03700f4b5def24bf9fc6b5fd/v3/sdk/futures/domain/signal.go`: Signal, SignalDetails, SignalProvenance, StrategyCycleSeq, DeriveSignalID; blob `9cb6d0810fdf5437d5972804e3f015c7514be6f6`.
- Mismo corte, `v3/sdk/futures/strategy/fanout.go`: AccountStrategyTarget, FanoutTargetSet, ApplyTargetSet, Linearize, DeliveryFromSignal; blob `100a9e72b32158d8b87e2521b265d1d4428ead8c`.
- [[Echo Futures Architecture Candidate V2]], §1–2.5: Signal, ciclo escalar, AccountStrategy, MM y Operation; blob `bfccbb8289d8a8896ecbdb921f61cacd5506e95f`.
- [[Echo Futures — Technical SPEC V1]], §3.2–3.4 y §9–11: identidades, SignalDelivery, materialización y estado; blob `a37ba7c2666ecb35ec59da2a8ca9ac48e190e77b`.
- [[Echo Futures — D2-08 Strategy Runtime]], §1–3 y §5, 2026-09-28: ciclo técnico, ausencia de feedback, sin StrategyTrade y seam ReferenceEvent→Signal; blob `ae736caf27cb028b69a1260de8e35cc3fcd03a16`. La sección histórica de indicadores se interpreta con el mandato posterior de analytics compartido.

### Source de los deltas ya inspeccionados

- En `95e9d10`, `sdk/futures/strategies/tgmm/tgmm.go` blob `eb2824a470d27d63d93c856f4a0829d4526d367b`; `backtester/platform_operability.go` blob `52710c0494dd375745aeb8c3dce85386ec36265e`; `strategies/tgmm/minimum_policy.go` blob `9ace5fdbff3f6b2d506c9e769cc29236de9d54cf`; `backtester/tools/tradesgerard/TG-FLOW.md` blob `7af1b9a9fe1a471ebe0f5e048379c8c0400dd7fb`. Prefijo de paths: `v3/` y `v3/sdk/futures/` según paquete. Divergencia económica publicada registrada en R3, adopción posterior según §10.
- Source base R1/R2 `0c4aae552176fda005c44766e24dd70e8c48e589`: `v3/core/internal/futuresruntime/runtime.go` blob `f4fdefe7a1efb7fb29fb7593e708e86a2be321e0`; `v3/sdk/futures/config/views.go` blob `3670051e354c3f61e3389ec06691beeb606640de`; `composition.go` blob `181b525166c76bebe00a53c62f7748915f6d186b`.
- Misma base: funciones Core `futures_market_stream.go` blob `08ccb58b4d3a0021e5adb58abcd5574d65bf06dc`; `futures_market_analytics.go` blob `064824c5631d53265907c2a7d0fbe19339c88174`; `futures_signal_fanout.go` blob `0201175340f4427875daff372de7cc4aa79b225f`; `futures_operation.go` blob `7605f4aaff9d54ed9a56cb7fd15827400b8cb78c`; `futures_provider_rules.go` blob `e4361f331c511b9f8b5e2caa328e9621b12055c0`.
- Misma base: `v3/futures-bridge/core/bridge.go` blob `17874301ffd9296a2426806ff5b9c5188904756b`; `addon-ninjatrader/EchoExecutionAddOn.cs` blob `dedd6dcdd14abefee00f087ff23e574ca3cdfd3f`; README bridge blob `350166d5ba49c6c55f61c417306c61272c014dae` (documentación D5 histórica).
- Base de campaña R2: `v3/backtester/platform_campaign.go` blob `1bdbd20f4abf9aa89d4044fa77332d2a9801d04f`, con selección/pausa anterior. No se transfiere esa política como equivalente a la permanencia R4.

### Autoridades y antecedentes

- [[Echo Futures]], mandato inicial adjunto y cuatro turnos explícitos del Owner del 2026-10-16. El último mandato prevalece sobre propuestas previas contradichas; R1–R3 permanecen en Git.
- [[TRADESGERARD-CONTROL]] y [[TRADESGERARD-CONSOLIDATION]]: autoridades separadas, no modificadas.
- [[10-projects/Echo Futures/artifacts/d6-final-physical-certification-20261005/D6-FINAL-PHYSICAL-CERTIFICATION|D6 físico 2026-10-05]], blob `6fd72dceb517a730647c5dec27dc714bbb55797c`: evidencia histórica, no estado actual.
