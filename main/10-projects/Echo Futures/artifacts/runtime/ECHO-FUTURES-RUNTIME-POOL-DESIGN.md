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

Diseñar con KoR una extensión acotada del runtime existente. Estado: **CANDIDATO_R3 / DISEÑO_NO_ACEPTADO**. R3 incorpora el tercer turno explícito del Owner del 2026-10-16 y reemplaza las propuestas R2 contradichas. Las decisiones de producto confirmadas no equivalen a aceptación del diseño técnico completo, implementación ni autorización de ejecución. No se cierra sesión/proyecto.

Mandato inicial: `Markdown pegado(3).md`, PROMPT_VERSION 1, actualizado por los turnos posteriores del Owner. Autoridad del proyecto: [[Echo Futures]]. Este carril lee producto y documenta diseño; no modifica [[TRADESGERARD-CONTROL]], [[TRADESGERARD-CONSOLIDATION]] ni el trabajo GLM LOCAL.

**Cortes de lectura:** R1/R2 inspeccionaron `xKoRx/echo@0c4aae552176fda005c44766e24dd70e8c48e589`. R3 resolvió master en `95e9d105182af99d03700f4b5def24bf9fc6b5fd`, dos commits por delante, y leyó sólo el delta material de presupuesto/operabilidad y su documentación. No se afirma inspección del WIP local ni del terminal físico.

## Contenido

### 1. Decisiones Owner vigentes

| Decisión | Opción confirmada | Consecuencia |
|---|---|---|
| Unidad de configuración | Pool de cuentas + Strategy configurada + MM/configuración. | Sin asignación/configuración manual Strategy/MM por cuenta consumible; AccountStrategy efectivo se resuelve automáticamente. |
| Concurrencia | Una cuenta por asociación pool–Strategy; varias asociaciones del mismo pool y pools independientes simultáneos. | No mutex global ni límite de una cuenta por pool. |
| Afinidad permanente | Una cuenta que operó A sólo podrá operar A, aunque pasen días; nunca pasa a B. | Afinidad durable separada del turno activo; reinicio, pausa y reanudación no la borran. |
| Turno | Persistente entre operaciones; cambiar por objetivo, pausa o desenlace aplicable tras drenaje. | No round-robin por trade, no migración de exposición, no señal consumida reutilizada. |
| Selección | Elegibles más antiguas primero por creación real. | Filtrar disponibilidad/compatibilidad/afinidad y ordenar; no ranking de rendimiento ni reasignación de cuentas ya vinculadas. |
| Strategy | Agnóstica a cuenta, pool ejecutor y MM; trabaja con indicadores, decisiones e intenciones/ciclos técnicos canónicos. | Se retira el acceso a contexto de cuenta propuesto en R2; una instancia técnica puede abastecer varias asociaciones. |
| MM | Consume indicadores y contexto económico de la cuenta; diferencia challenge/funded. | La cuenta/programa/fase participa en MM/Provider/elegibilidad, no en el algoritmo de Strategy. |
| Analytics | Echo calcula indicadores entre barras y consumidores; Strategy y MM leen observaciones causales. | Observación es resultado publicado, no el calculador; misma lógica de cálculo offline/runtime. |
| Remanente insuficiente | Mantener el presupuesto de la operación y permitir el intento aunque supere el remanente al piso, mientras la cuenta no haya alcanzado un bloqueo vigente real. | No achicar tamaño/SL/TP por ese remanente, no rechazar sólo por esa comparación ni declarar pérdida anticipada por presupuesto. Véase §6. |
| NinjaTrader | Feed y gateway de operaciones exclusivamente. | Sin selección de turno/cuenta, indicadores de estrategia, MM ni reglas de negocio en AddOn. |
| Primera entrega | Cohorte de CINCO cuentas del Owner, pools/asociaciones, rotación y concurrencia funcionales. | Una demostración con una cuenta no satisface la entrega. Objetivo Owner: domingo 2026-10-18 por la noche, sin promesa de plazo. |
| Módulos iniciales | Los decide el Owner con sus resultados; K05/SR es candidato y habrá otros Strategy/MM. | No congelar la entrega en TG/TGMM ni exigir cinco algoritmos diferentes. |
| Permisos comerciales | Excluidos de este análisis por el Owner. | No nueva investigación ni gate documental de permisos; identidad y restricciones técnicas/económicas configuradas conservan su autoridad. |

Los montos 300/53/1000/1 son ejemplos del tercer turno; no parámetros universales ni selección de un perfil definitivo.

### 2. AS-IS y divergencia material recién publicada

**OBSERVADO_EN_CÓDIGO** no implica prueba ejecutada ni operación física. La tabla conserva los owners inspeccionados; el compare R3 no reporta cambios en Core, bridge o Provider. Sí cambia el SDK TGMM/config y la política de campaña: las conclusiones económicas de R2 requieren el delta siguiente.

| Recorrido | Base inspeccionada | Delta localizado |
|---|---|---|
| Mercado | `FuturesMarketStreamFn`, keyed por stream, delega canonicalización/dedup/orden/epoch/freshness al SDK. | Reutilizar y validar alimentación/restauración del camino real. |
| Barras e indicadores | `FuturesMarketAnalyticsFn` usa engine compartido; kernels TG, checkpoint y snapshots por delivery. | Completar demanda de ambos consumidores y transporte causal, no otro motor de indicadores. |
| Strategy/distribución | `Compose` resuelve Strategies[]; `FuturesSignalFanoutFn` entrega por AccountStrategy. | Una evaluación por instancia técnica; distribuir a asociaciones y a su cuenta efectiva, no a todas las candidatas. |
| MM | Compose resuelve un MM desde cfg.MM; MMConfigSnapshot admite config por cuenta/Strategy; TGMM conserva ciclo en MMState. | Resolver módulo/config por asociación/fase; no singleton de estado monetario compartido. |
| Reglas | Provider owner account-wide; SnapshotViews.EffectiveRuleSet devuelve el RuleSet global del snapshot. | Resolución por cuenta/programa/fase; preservar admisión, reservas y revalidación. |
| Ejecución | Bridge.Run crea N sesiones; EchoExecutionAddOn configura una sola cuenta/resolvedAccount. | Multiplexar routing/observaciones por cuenta, conservando M2 y correlación; sin lógica de pool en NinjaTrader. |
| Economía de vuelta | Operation admite execution/quote/economics tipados y bridge dispone de M2/reconciliación. | Trazar productor físico y entrega causal; los tipos no certifican recorrido completo. |
| Turnos campaña | platformCampaign mantiene accounts/selected/turnActive; selectTurn conserva elegible y cambia sólo tras quiescencia. | Extraer sólo selección/turno realmente comunes; el pool añade competencia entre asociaciones. |

**Divergencia confirmada contra el nuevo mandato, no contra un WIP no observado:** en `95e9d10`, `tgmm.Manager.entry` con `STRATEGIC_ENTRY_BUDGET_V1` devuelve `TG_ENTRY_BUDGET_EXCEEDS_HEADROOM` cuando riesgo > headroom. No reduce el presupuesto, pero tampoco emite la orden. Además, `platformCampaign.retireUntradeableAccounts` compara margen permanente con RiskRef y declara `LOST_ENTRY_BUDGET_BY_POLICY` si no alcanza. Por tanto, este corte publicado implementa rechazar/retirar, NO entrar completo y observar el desenlace pedido ahora. `TG-FLOW.md` describe precisamente ese comportamiento. No se atribuye esta divergencia al trabajo local posterior ni se detiene/reproduce ese trabajo.

**Punto de integración:** incorporar la corrección final de la semántica del §6 en el dominio compartido y su política de selección. No etiquetar como equivalente una política que rechaza o retira; no arreglar sólo LIVE ni copiar fórmulas al runtime. Conservar provenance de las versiones históricas de campaña.

Gaps conservados: MM consulta TG por `SnapshotViews.AnalyticsView → TGOwnerViewFor → tgPublished`, publicación Go local cuya firma no identifica stream; falta acreditar serving distribuido correcto. `readModelMarket.Mark` lee last: no acredita bid/ask ejecutable. Economía física/quote siguen por trazar. TGMM mantiene referencias GAU50 y objetivos restringidos del escenario: no generalizarlos a otros programas. El último D6 físico localizado del 2026-10-05 quedó bloqueado por feed stale, sin órdenes; es historia, no diagnóstico actual.

### 3. Modelo y fronteras canónicas

**PROPUESTA técnica que implementa las decisiones:** catálogo existente de cuentas, pool como inventario y asociación estable pool–Strategy–MM como consumidor de cuentas. No nuevo ledger ni cuenta sintética.

```text
Feed → mercado canónico → barras → indicadores compartidos
                                      ├→ Strategy configurada → intenciones técnicas
                                      └→ observaciones para MM según su trigger

Intención técnica de Strategy A
    ├→ asociación P1–A–MM1 → turno/cuenta C01 → Operation + MM1 + Provider
    └→ asociación P2–A–MM2 → turno/cuenta C04 → Operation + MM2 + Provider

Órdenes autorizadas → bridge → NinjaTrader gateway
Hechos de cuenta/órdenes/fills → owners de ejecución, economía, MM y Provider
```

Strategy recibe mercado/indicadores/config técnica y mantiene su ciclo técnico. No recibe balances, fase, pérdidas de una cuenta, MM seleccionado ni resultado particular de su ejecución como input para cambiar la señal. Sus señales/gestiones canónicas se consumen independientemente por asociación. Agregar otro pool no obliga a reevaluar la misma instancia técnica; parámetros técnicos diferentes sí definen instancias distintas.

**Operación canónica no es una segunda Operation financiera:** usar el vocabulario Signal/intención/ciclo técnico existente donde encaje. La Operation de ejecución sigue teniendo cuenta, binding, órdenes y fills propios. Antes del handoff se mapea la correlación de ciclo/gestión a los campos existentes; no crear por rutina un nuevo aggregate CanonicalOperation. Una reducción/cierre técnico se aplica a las ejecuciones correspondientes a su intención original, no a cualquier posición actual del pool. Si MM cerró una ejecución antes, la gestión técnica posterior no vuelve a abrirla ni cambia la Strategy compartida.

Asociación: ID estable, pool, referencia de instancia/config Strategy, referencia de módulo/config MM y enabled. Cambiar versión/config MM no cambia su identidad ni crea otro turno. I1 conserva una asociación por pareja pool–instancia Strategy; otro MM simultáneo para esa misma Strategy se expresa en otro pool, como pidió el Owner.

`AccountStrategy` es el binding efectivo que el runtime materializa/reutiliza al adjudicar una cuenta, vinculado a asociación y generación de asignación. El Owner da de alta la identidad/programa/fase/conexión de una cuenta y la incorpora al pool; no vuelve a configurar Strategy/MM en ella. La creación real determina FIFO, no la fecha de discovery ni la sesión NinjaTrader.

### 4. Afinidad, selección y persistencia

**Afinidad CONFIRMADA_OWNER:** C01 que operó A no pasa a B, aunque termine su turno o transcurran días. I1 conserva la vinculación estable a su asociación de origen, sin migraciones automáticas entre pools. El módulo/config de MM es versionable dentro de la asociación, no una excusa para borrar afinidad. Una Strategy técnicamente diferente no adopta una cuenta como si fuera la misma por conservar un alias.

Afinidad y turno son estados distintos: A puede conservar cuentas pausadas propias mientras opera otra. Al recuperarse una antigua, vuelve a ser candidata de A; no preempta un turno elegible vigente. FIFO se aplica sólo al seleccionar otro turno.

Selección: conservar turno utilizable; sin turno, filtrar candidatas por afinidad/disponibilidad/contexto vigente, ordenar `(account_created_at, account_id)` y reclamar la primera. Bajo §6, remanente positivo menor que riesgo no es por sí solo incompatibilidad, muerte ni motivo para saltarla.

Arbitraje mínimo: orden durable de solicitudes y desempate estable en un mismo lote. El PoolManager mantiene varios turnos, uno por asociación; serializar adjudicación no serializa ejecución. El owner account-wide confirma el claim exclusivo incluso con pools solapados. Como mínimo: un claim pendiente por asociación, generación persistida y confirmación idempotente antes de nueva exposición. Una respuesta tardía de otra generación no habilita órdenes. No TTL que libere incertidumbre ni transacción cross-key inventada.

Antes del primer envío que pueda producir efectos, la reclamación debe estar fijada durablemente; un intento incierto conserva ownership. La afinidad definitiva debe sobrevivir a toda cuenta efectivamente operada. Sólo una reserva provisional con ausencia demostrada de efectos y sin operación previa puede volver al conjunto libre. Una cuenta temporalmente flat no pierde automáticamente afinidad ni turno.

### 5. Gestión, rotación y analytics

| Situación | Resultado de diseño |
|---|---|
| Objetivo o pausa efectivamente alcanzados | Bloquear nuevas aperturas, gestionar/drenar según política y terminar turno al confirmar; cuenta pausada o en transición con causa. |
| Remanente positivo < presupuesto MM | Mantener elegibilidad por este concepto e intentar nueva oportunidad con presupuesto completo; no retirada anticipada. |
| Breach/expiración/inoperabilidad real confirmada | Excluir nuevas entradas y preservar historia/obligaciones; rotar al quedar drenada. |
| Funding/review/pago pendientes | Fase/estado confirmados gobiernan elegibilidad; no fabricar transición por PnL. |
| Indicador/quote no disponible o setup inválido | Rechazo acotado de la oportunidad; no declarar la cuenta muerta. |
| Orden/exposición incierta | Retener claim y bloquear avance de esa asociación hasta reconciliar; las demás siguen. |
| Sin candidatas | Esperar cambios relevantes, sin compras ni señales vencidas en cola. |

PoolManager no gestiona exposición: selecciona, cierra admisión de nuevas entradas y espera drenaje. MM decide sizing, stop, target y gestiones que implemente; Operation/Provider mantienen ejecución/riesgo. Una parada que exige cierre utiliza la intención existente de cierre/seguridad, no órdenes directas del pool ni flatten implícito para toda pausa. La cuenta saliente conserva sus fills/órdenes/ciclo financiero; no se trasladan al reemplazo.

Una señal consumida en C01 no se reusa en C04. Rotar no convierte una gestión técnica antigua en nueva entrada ni reinicia Strategy/analytics. Nuevas oportunidades posteriores pueden usar C04.

**Barras → cálculo → observaciones:** mercado/barras compartidos alimentan kernels que publican observaciones inmutables. Strategy y MM declaran sus demandas; se calcula su unión, incluyendo indicadores exclusivos de MM. Reutilización por identidad que cambie cálculo: stream/contrato/timeframe/parámetros/calendario/seed/epoch/versión. No imponer TG como API universal ni crear una DSL. Backtest puede preparar tablas; runtime actualiza los mismos kernels incrementalmente. Ambos respetan disponibilidad causal y orden de publicaciones del mismo instante.

El MM puede reaccionar a quotes/fills/contexto económico sin nueva señal ni nueva vela. Su acceso a analytics no depende sólo del indicador enviado al abrir. Servir observaciones mediante mensajes/estado existentes de StateFun con corte e identidad comprobables; el puntero Go local no acredita producción distribuida. Una cuenta pausada no congela mercado ni indicadores.

### 6. Presupuesto completo aunque el remanente sea inferior

**CONFIRMADO_OWNER:** no adaptar presupuesto ni cantidad para sobrevivir con el remanente al piso. Ejemplo ilustrativo: saldo 48053, piso supuesto 48000, remanente 53 y presupuesto operativo MM 300. La orden conserva el presupuesto 300; no se transforma en 53 ni se rechaza/retira sólo porque 300 > 53. Lo mismo con remanente 1 y presupuesto 1000. Son remanentes al límite de pérdida, no afirmaciones sobre el margen de compra exigido por el destino físico.

Separar tres conceptos:

1. **Presupuesto/intención MM:** se calcula desde su configuración y lógica de objetivo/fase, sin truncarlo al remanente al piso. La precisión real de contratos/ticks y el modelo de costos sigue aplicándose al presupuesto solicitado. Este mandato no autoriza cambiar otros cálculos MM no relacionados con ese remanente, como reglas de objetivo ya acordadas.
2. **Admisión actual:** comprobar cuenta correcta, estado vigente, quote/datos, contratos/capacidad técnica y ausencia de bloqueos ya activos. Para esta política, comparar riesgo propuesto > remanente positivo NO basta para reducir, rechazar ni retirar. Auditar el recorrido completo: elegibilidad de pool/campaña, MM, reserva/revalidación y guards pre-egress, para que el recorte no reaparezca en otra capa. No falsificar headroom ni esconder piso real para conseguir ALLOW.
3. **Desenlace observado:** el RuleSet sigue vigilando el balance/equity y umbral que realmente defina. Si se produce breach, se aplica el tratamiento vigente y la rotación tras drenaje. El stop estratégico puede quedar más allá del piso y el cierre por regla ocurrir antes. No asegurar pérdida exacta de 300, 53 o 1, ni inventar un fill perfecto en el piso. El nuevo contrato no borra un bloqueo ya alcanzado.

Para el ejemplo, 48053 es el saldo actual y 48000 el piso asumido; no se declara perdida por cualquier retroceso desde 48053. Un rechazo real del destino es un hecho a registrar y tratar sin reintentos ciegos; no se presenta submit como fill. El resto de las restricciones de formato/capacidad y seguridad de ejecución no desaparece.

**Integración R3:** el corte publicado `95e9d10` NO satisface esta semántica. `tgmm.Manager.entry` aplica rechazo por headroom y `platform_operability.go` aplica pérdida anticipada por R_ref. Conservar políticas históricas identificables; implementar/consumir el contrato correcto en la lógica común, no un parche exclusivamente runtime. El nombre final/versionado se define con el delta local integrado; no reutilizar un identificador histórico como garantía de comportamiento diferente. No ejecutar ni recertificar las40 campañas desde este carril.

**Oráculo pequeño obligatorio para implementación posterior:** con datos/costos y límites de cantidad válidos, remanente53/R300 y remanente1/R1000 emiten la intención de orden con el presupuesto completo; pool no retira; mermar el remanente no reduce cantidad por sí solo; ganancia sin breach mantiene la cuenta, cruce real del umbral activa su desenlace; cuenta ya bloqueada no abre. Presupuesto, orden aceptada, fill y PnL son salidas separadas. Variantes runtime/backtest producen la misma decisión de dominio para entradas equivalentes.

### 7. Programas/fases y contexto económico

Cuenta/Provider posee programa, fase, RuleSet, términos, economía y pisos reales. PoolManager consume ese estado para selección/turno; no mantiene otra fase editable ni recalcula PnL. MM recibe el contexto de la cuenta efectiva y decide challenge/funded con su configuración. Strategy no conoce esas diferencias.

Resolver RuleSet por referencia y versión de cada cuenta, no desde un Provider global. El pool puede mezclar programas si los contratos necesarios están soportados; no es obligatorio separar por empresa. No clase MM por empresa ni if providerName dentro de Strategy. Reemplazar constantes GAU50 por datos de contexto cuando el programa real lo requiera; no duplicar fórmulas.

Operación abierta conserva módulo/config MM y presupuesto aplicables; cambios normales aplican a próximas operaciones. Las restricciones efectivas de seguridad siguen reevaluándose. Una transición confirmada challenge→funded se instala con contexto y límites correctos, sin fingir nuevo saldo ni reiniciar piso por reinicio/cambio de turno. No reemplazar MM en caliente de una operación existente para aparentar transición completada.

### 8. Cohorte de cinco cuentas y prueba de aceptación

**Entrega de producto:** las CINCO cuentas del Owner deben formar parte de la puesta en marcha, con identidad/destino/programa y retorno de eventos verificados, composición de asociaciones y rotación funcionales. No declarar entrega concluida por una cuenta, dos cuentas ni sólo listar cinco en config. Los IDs actuales de la cohorte aún no se inspeccionaron aquí; C01..C05 son alias ficticios para especificar pruebas, no inventario afirmado.

Distinguir cinco candidatas utilizables de cinco turnos simultáneos. Con tres asociaciones, como máximo tres cuentas operan a la vez y las otras esperan rotación. FIFO/afinidad/turno persistente no garantizan por sí solos que las cinco reciban una operación durante una semana si ningún turno termina. No resolverlo introduciendo una rotación por trade/plazo que el Owner no pidió.

**Configuración de arranque propuesta, no acordada automáticamente:** si sólo están listas tres Strategies y se necesita dar capacidad inicial a cinco cuentas sin esperar rotaciones, usar cinco asociaciones con Strategies reutilizadas en pools distintos, tal como permite el modelo. Ejemplo: pool P1 con C01/C02/C03 y A/B/C; pool P2 con C04/C05 y A/B. Cada asociación tiene su MM, un turno y cuenta exclusiva. Dos pools con inventarios disjuntos evitan competencia innecesaria en esa configuración; no son una limitación del modelo general de pools solapados. No crear cinco algoritmos ni overrides MM manuales por cuenta. Esto habilita cinco turnos, no fabrica oportunidades si Strategy no emite señales.

**Pruebas propuestas para la entrega (ninguna ejecutada en este turno):**

- Cohorte 5/5: routing de comando y evento por cuenta/contrato, retorno de economía/órdenes/fills, protección y gestión; distinguir prueba en SIM/demo equivalente de aceptación observada en cada destino real, sin inferir la segunda de la primera.
- Dominio: tres asociaciones compitiendo por cinco candidatas; turnos paralelos, FIFO, pausa/reemplazo y afinidad A durante varios días. También cinco asociaciones concurrentes, sin límite oculto de uno/tres ni cruces de cuenta.
- Riesgo: casos completos53/300 y1/1000 del §6, sin reducción/rechazo/retirada por remanente; breach real conserva respuesta y trazabilidad.
- Recuperación: reinicio, reclamaciones pendientes/generaciones viejas, ACK incierto, fill tardío y drenaje; ningún duplicado ni reatribución de un hecho de C01 a C04.
- Independencia: misma Strategy/indicadores producen las mismas señales al variar cuenta/MM; esas ejecuciones pueden tener tamaños/desenlaces distintos. MM obtiene indicadores actualizados y contexto challenge/funded correctos, incluso en consumidores separados.

La prueba individual puede formar parte del diagnóstico, nunca sustituye el criterio de cinco. Pruebas de plumbing con órdenes controladas deben identificarse como tales; no certifican por sí solas señales reales. No exigir rentabilidad, un mes de histórico ni200cuentas para validar este alcance. No falsificar fills/órdenes en las cuentas reales para completar una casilla.

### 9. Delta implementable y cierre técnico pendiente

| Bloque | Propietarios | Cambio y límite |
|---|---|---|
| Composición | Catálogo/config Views + runtime + fanout | Pools/asociaciones y MM por asociación; AccountStrategy automático; Strategy técnica compartible sin contexto de cuenta. Registro/dispatch multikey real, no duplicar procesos por estrategia. |
| PoolManager | Owner pequeño de asignación en Core + owner account-wide existente | Turnos por asociación, FIFO, afinidad durable, claim/generación e idempotencia. Sin microservicio/Redis/lease/optimizador nuevos. |
| Presupuesto/fases | SDK MM/Provider/contexto + adaptadores de campaña/runtime | Contrato §6 común sin recorte/rechazo/retirada por remanente, reglas efectivas por cuenta y fase; integrar delta local sin interferir ni divergir. |
| Observaciones | Market/analytics y serving hacia MM | Unión de demanda, publicación causal distribuida, completitud SR/H1, quote y economía del camino real; mismos kernels. |
| Ejecución | Bridge/adaptador/ExecutionAddOn | Routing/observaciones de las cinco cuentas, correlación y M2, sin dominio financiero en NinjaTrader. |

**Evaluación arquitectónica:** implementable como extensión del modelo de asignación/ejecución, no reescritura. Strategy agnóstica reduce acoplamiento respecto de R2. Pero cambiar de rechazar/retirar a admitir riesgo completo es semántica de dominio adicional, no sólo wiring del pool. El mayor riesgo de integración queda en serving causal real, economía/quote y routing/recuperación multiaccount; no en ordenar una lista de cinco elementos.

Objetivo de uso: domingo 2026-10-18 noche según Owner. No promesa ni estimación de horas; la entrega requiere resultados observados de los recorridos anteriores, no sólo build verde o fixture. Reusar source y evidencias relevantes sin otra auditoría histórica. La cuenta que se observa llena en un test no se convierte en autorización genérica de operación.

Diferido: MM arbitrario por cuenta, varias Strategies dentro de la misma cuenta, varias cuentas simultáneas por asociación, optimización/ranking, netting/hedging de portfolio entre cuentas, UI nueva, otros adaptadores y nuevas gestiones no pertenecientes a los MM elegidos. Reutilizar una Strategy en varios pools sí es alcance actual.

Pendientes técnicos concretos antes del handoff: mapeo de intenciones/gestiones canónicas a identidades existentes; registro/dispatch multikey; serving distribuido de analytics; productor real de quote/economía; protocolo y configuración de cinco cuentas; integración del nuevo presupuesto común. La Strategy/config final sigue siendo decisión del Owner, no excusa para demorar el contrato de composición. No volver a preguntar FIFO, afinidad, turno, concurrencia, ausencia de cuenta en Strategy ni gateway-only.

La autoridad Environment Contract no se recuperó en R1; no se deduce ausencia. Resolverla antes de instrucciones operativas, sin reabrir ahora discovery de infraestructura. Este turno sólo leyó y documentó: no código, scripts, pruebas, campañas, deploy, órdenes ni dispatch de agentes. La aceptación del diseño y el pedido de prompt LOCAL siguen siendo del Owner.

## Fuentes

### Delta R3 en xKoRx/echo@95e9d105182af99d03700f4b5def24bf9fc6b5fd

- `v3/sdk/futures/strategies/tgmm/tgmm.go`: EntryBudgetV1, Manager.entry; blob `eb2824a470d27d63d93c856f4a0829d4526d367b`. Rechazo TG_ENTRY_BUDGET_EXCEEDS_HEADROOM observado.
- `v3/backtester/platform_operability.go`: StrategicEntryBudgetV1, LostEntryBudgetByPolicy, retireUntradeableAccounts; blob `52710c0494dd375745aeb8c3dce85386ec36265e`. Pérdida anticipada por presupuesto observada.
- `v3/sdk/futures/strategies/tgmm/minimum_policy.go`: MinimumExecutableRisk, economicQuantity; blob `9ace5fdbff3f6b2d506c9e769cc29236de9d54cf`. Cantidad/ticks/costos no equivalen a remanente al piso.
- `v3/backtester/tools/tradesgerard/TG-FLOW.md`: política publicada y flujo; blob `7af1b9a9fe1a471ebe0f5e048379c8c0400dd7fb`.
- Compare `0c4aae55...95e9d10`: dos commits; cambios en backtester, presets y SDK TGMM/config, no en Core/bridge/Provider. No acredita WIP local.

### Source base R1/R2 en xKoRx/echo@0c4aae552176fda005c44766e24dd70e8c48e589

- `v3/backtester/platform_campaign.go`: Validate, selectTurn, admitOpportunity, checkpoint, tickAccount, purchase; blob `1bdbd20f4abf9aa89d4044fa77332d2a9801d04f`. Cambiado en R3: no transferir como vigente su política anterior.
- `v3/core/internal/futuresruntime/runtime.go`: Compose, WithTGAnalyticsOwner, BridgeCommandEnvelope; blob `f4fdefe7a1efb7fb29fb7593e708e86a2be321e0`.
- `v3/sdk/futures/config/snapshot.go`: ConfigSnapshot, StrategyDef, AccountDef; blob base `89c1bf67580555914bdf05f4275d1e2fdb607d92`; ampliado por el delta R3.
- `v3/sdk/futures/config/views.go`: EffectiveRuleSet, MMConfigSnapshot, AnalyticsView, AccountEconomics, readModelMarket.Mark; blob `3670051e354c3f61e3389ec06691beeb606640de`.
- `v3/sdk/futures/config/composition.go`: ResolveStrategy, ResolveMoneyManager; blob `181b525166c76bebe00a53c62f7748915f6d186b`.
- `v3/sdk/futures/config/tgmm.go`: NewTGMM; blob base `4097a5b17093ef39153d596a987ffb43e6a63b4b`; ampliado por el delta R3.
- `v3/core/internal/functions/futures_market_stream.go`: FuturesMarketStreamFn; blob `08ccb58b4d3a0021e5adb58abcd5574d65bf06dc`.
- `v3/core/internal/functions/futures_market_analytics.go`: tgIngestAll, TGOwnerViewFor; blob `064824c5631d53265907c2a7d0fbe19339c88174`.
- `v3/core/internal/functions/futures_signal_fanout.go`: handleSignal, handleTargetSet; blob `0201175340f4427875daff372de7cc4aa79b225f`.
- `v3/core/internal/functions/futures_operation.go`: Invoke, typed ingress; blob `7605f4aaff9d54ed9a56cb7fd15827400b8cb78c`.
- `v3/core/internal/functions/futures_provider_rules.go`: Invoke/account owner; blob `e4361f331c511b9f8b5e2caa328e9621b12055c0`.
- `v3/futures-bridge/core/bridge.go`: Bridge.Run; blob `17874301ffd9296a2426806ff5b9c5188904756b`.
- `v3/futures-bridge/addon-ninjatrader/EchoExecutionAddOn.cs`: LoadConfig, ExecuteCommand, ExecuteSubmit; blob `dedd6dcdd14abefee00f087ff23e574ca3cdfd3f`.
- `v3/futures-bridge/README.md`: M2 y documentación histórica D5; blob `350166d5ba49c6c55f61c417306c61272c014dae`.

### Autoridades documentales

- [[10-projects/Echo Futures/Echo Futures|Echo Futures]].
- [[10-projects/Echo Futures/artifacts/tradesgerard/TRADESGERARD-CONTROL|TRADESGERARD-CONTROL]] y [[10-projects/Echo Futures/artifacts/tradesgerard/TRADESGERARD-CONSOLIDATION|TRADESGERARD-CONSOLIDATION]], sin cambios desde este carril.
- [[10-projects/Echo Futures/artifacts/d6-final-physical-certification-20261005/D6-FINAL-PHYSICAL-CERTIFICATION|D6 Final Physical Certification 2026-10-05]], blob `6fd72dceb517a730647c5dec27dc714bbb55797c`, evidencia histórica únicamente.
- Mandato adjunto y tres turnos explícitos del Owner del 2026-10-16. R3 prevalece sobre R2/R1 contradichas; historial conservado en Git.
- Referencias Apache de R2 sobre owners/direcciones de StateFun conservadas como fundamento histórico, no verificación del wiring actual.
- NinjaTrader, `OnOrderUpdate()`, documentación oficial consultada 2026-10-16: distingue Submitted/Accepted/Rejected/Filled y errores OrderRejected/OrderRejectedByRisk. Fuente para distinguir envío de ejecución real, no recomendación de ejecutar Strategy dentro de NinjaTrader ni investigación de permisos comerciales.
