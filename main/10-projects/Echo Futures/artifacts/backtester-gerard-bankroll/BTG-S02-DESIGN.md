---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S02 — Dos simulaciones, un dominio y paridad runtime

## Propósito

Entregar al Primary Manager un diseño candidato implementable dentro de S03–S05. **READY_FOR_PRIMARY_MANAGER_REVIEW; no es un freeze ni un gate aceptado.** Fecha: 2026-10-06, America/Santiago. Rol: GOD / arquitectura acotada, CLOUD, ONE-SHOT, sin subdelegación. No se ejecutó código de producto, trading físico, compras ni retiros reales.

**Arquitectura recomendada:** extender el driver y SimExecution existentes con observaciones intrabar causales; conservar Strategy, GerardMM, Operation, Provider y accounting SDK; añadir un orquestador secuencial de campaña con caja personal separada. BASIC/CAMPAIGN y OHLC/TICKS/MIXED son dos ejes independientes, no motores distintos.

**Enmienda acotada del Manager, dentro de S02:** corrige continuidad de Strategy, costo de expansión intrabar y dimensión del barrido monetario. CURRENT_TASK_STATE=REPAIR_OF_EXISTING_DESIGN; ACCEPTED_DIRECTION / NOT_FROZEN. Conserva S03 implementación, S04 adversarial LOCAL independiente y S05 corrección/resultados dentro de la ventana Owner del 6–7 de octubre de 2026, America/Santiago. No añade shot, prompt S03 ni funcionalidad diferida a V3. [A5]

## Contenido

### 1. Autoridad, baseline y límites

| Campo | Estado leído, no inferido |
|---|---|
| Agents-OS master leído para la enmienda | `fdff61691805608d2b84c5e0fc637ff433f0197c`; publicación sólo sobre master actual, con control de concurrencia |
| Candidato del Manager | `00514fe65d0b4a06975096de17a3c2246d573c92`, blob `fada3d677d57e134910ef2e210da943e7a425a73`; rama `codex/btg-s02-design-cloud-20261006` sólo como autoridad de lectura |
| Evidencia S01 | `codex/btg-s01-evidence`, `e4a177ebca60c95062fbc30bc8a97ceb3be31c04` |
| Echo inspeccionado | `77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626`, `codex/btg-s01-real-diagnostics` |
| Source ejecutado por LOCAL | `d69d03eceeac1495522473a95baf08087f5c28b3` |
| Integración | PR4 apilado sobre PR3 / `fb210ac4`; este shot no mergea ni rebasea |
| Verificación física CLOUD | NOT_RUN; lectura de source y evidencia LOCAL solamente |
| Estado de diseño | Candidato reparado para review final; sin freeze, implementación ni certificación propia |
| HEAD producto refrescado | `codex/btg-s01-real-diagnostics` permanece en `77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626`; master Echo permanece en `372af59a7b83604781346613da01e3d510ea1360` |

S01 aporta un baseline acotado: cuenta continua NQZ3, trading 2023-10-29→2023-11-23 UTC; 113 operaciones materializadas, 39 con fills, 78 fills; neto −USD34.293,32, drawdown USD35.225,55; reproducción fresca reportada IDENTICAL; 6m47s y aproximadamente528MiB. Son resultados de trabajadores LOCAL, **no ejecutados por este arquitecto**. No certifican LIVE, scaling, una prop real ni continuidad de los13 contratos. [A2]

`functional_profile.go` configura NQ físico, tick0,25, multiplicador20 USD/punto, SIM/GENERIC100K, S2 y GerardMM compartidos, SL2000/TP1500 por account-day, NO_ADDS por ausencia de scaling, fee USD2,49 por contrato/fill, slippage1tick y offsets bid/ask modelados1/1. El calendario semanal Chicago17:00→16:00 no incluye overrides históricos de feriados. Conservar esta receta V1 sin convertirla en términos de Earn2Trade. [E5]

Forensics reporta1.096.336 filas RAW,226 fuera del calendario semanal y24.831 minutos esperados abiertos ausentes. El derivado autorizado conserva byte por byte las filas retenidas, excluye sólo esas226 y mantiene los huecos. Los13 derivados tienen algún segmento con warmup suficiente: **no** implica una cuenta continua por todos ellos. Los conteos son relativos al calendario configurado, no prueba del horario histórico oficial ni de la causa de cada hueco. [A4]

Los originales de `daedalus:/home/hermes-ops/echo-dev/history/nq/` permanecen inmutables. Reutilizar inventario, manifest, exclusiones y derivados; no solicitar otra exportación Windows. Este diseño incorpora los pendientes S01 a S03–S05; no los da por resueltos.

El candidato aún no estaba en master al leer el destino y su directorio; se recuperó desde el SHA explícito, no se declaró inexistente. BTG-PLAN en master contiene estados/instrucciones históricos: para F1–F3 y política de escritura prevalece el mandato de enmienda [A5]; no se reescribe el plan ni se mezcla trabajo ajeno. El baseline S01 se relee desde su autoridad publicada y no se reconstruyen D1–D6.

### 2. Decisiones y propuestas de producto

Owner ya fijó: BASIC100k; CAMPAIGN caja5000/costo120/máximo4 retiros; una cuenta operando a la vez; S2 cerrada5m/H4; resolución fuente1m; adds adversos y pyramiding; OHLC utilizable sin ticks; mismo dominio y seguridad. No se reabre la selección de S2 ni el significado de120.

Decisiones técnicas del candidato: fuente por minuto completo, calendario/analytics SDK, causalidad versionada, modelado OHLC explícito, controles existentes y runner de campaña secuencial. No hay UI, DSL, servicios adicionales, event sourcing, sequencer global, checkpoints generales ni framework de optimización.

| Propuesta no aprobada por Owner | Perfil funcional recomendado | Efecto |
|---|---|---|
| Compra | ON_DEMAND | Cobra120 al necesitar cuenta, no inmoviliza4920 inicialmente |
| Stages | EVAL_THEN_FUNDED_FUNCTIONAL_V1 | Evaluación y funded simulados, sin nombre de empresa |
| Payout | `payout_chunk=1500` bruto; split100%; fee0 | Neto igual al bruto; importe configurable y reportado, fijo en el barrido principal |
| Cobro | Próxima apertura negociable estrictamente posterior a solicitud | Pausa la cuenta; solicitud no financia compras |
| Cuarto cobro | Retirar la cuenta; beneficio residual no cobrado forfeited | Sin quinto retiro ni conversión del nominal en caja |
| Búsqueda principal | `mm_profit_objective ∈ {1000,1500,2000}` USD por account-day | SL2000 y `payout_chunk=1500` fijos; cambia la configuración de plan MM, no fórmulas ni señales |

No se recuperó una decisión que obligue a comprar de inmediato un lote de41. ON_DEMAND y el perfil económico se mantienen como **FUNCTIONAL_ASSUMPTIONS configurables**, nunca términos verificados de una prop ni configuración LIVE autorizada. El Primary revisa estas propuestas sin nueva investigación de empresas ni bloqueo por ajuste fino de cifras. Los tres objetivos MM son candidatos funcionales de investigación solicitados por la enmienda, no tres importes de retiro.

#### Adjudicación de F1–F3

| Finding | Adjudicación del diseño, no gate | Reparación y evidencia LOCAL exigida |
|---|---|---|
| F1 — continuidad | ACEPTADO: NewRun con estado vacío más warmup no reconstruye el ciclo técnico | §§3/6.4/9: Strategy y mercado persistentes, cuenta reemplazable; T02/T06/T17/T33/T34 después del reemplazo |
| F2 — costo intrabar | ACEPTADO como riesgo, sin lentitud V2 medida | §7.1 y §11: generador lazy, referencia correcta, atajo sólo probado y gate físico previo al lote; T35–T37 |
| F3 — objetivo vs retiro | ACEPTADO: el barrido anterior optimizaba payout_chunk, no el MM | §§2/4/8/9.2/11: tres objetivos MM, SL/chunk fijos, reruns/holdout y tabla separada; T30/T38 |

### 3. Reutilización y ownership del delta

| Superficie | Reutilizar | Delta S03 |
|---|---|---|
| `sdk/futures/strategies/s2` | Señal, indicadores, ciclos, warmup, CLOSE_ALL y elegibilidad | Sin cambio de estrategia; aclarar comentarios temporales contradictorios |
| `sdk/futures/config/mm.go`, `gerardmm/config.go` | Plan rows, fórmulas y Manager | Modo de scaling explícito común |
| `core/internal/futuresruntime/mm.go`, `runtime.go` | Composición y adapters | Consumir config común y exponer seams a harness LOCAL; no desplegar |
| `backtester/compose_account.go` | Strategy runtime, Operation, Provider, ledger SDK y venue | Separar inicialización única de Strategy de composición de cuenta; ambos modos usan los mismos owners y constructors |
| `ohlc_driver.go`, `ohlc_market_context.go` | Cursor, clocks, guards, analytics, mark fallback y drain | Lane temporal persistente; pasos lazy y atajo inerte probado; V1 preservado |
| `internal/simexecution/ohlc.go`, venue ticks | Órdenes, fills sellados, IDs y accounting hooks | Matching por observación y callbacks entre fills |
| `spec.go`, `controls.go` | RunSpec, AdvanceUntil, controles y outcomes | Versiones/fidelidad explícitas; no scheduler genérico nuevo |
| CLI/result writer/exporters | Entradas, formatos y recorridos actuales | Selector BASIC/CAMPAIGN, perfil resuelto, caja y cobertura |
| Módulo campaign pequeño en backtester | NewRun como entrada única del experimento y controles existentes | Lifecycle/caja y reemplazo del compartimento de cuenta; no recrear Strategy ni duplicar trading/sizing |

La composición ya usa `config.NewGerardMM`, `operation.NewEngine`, `provider.NewEngine`, `accounting.NewLedger` y SimExecution. El wrapper runtime delega al mismo constructor SDK. `ACCOUNT_CONTEXT_TRANSITION` y `ACCOUNT_CASHFLOW` ya tienen effective time, ordinal, contexto esperado y deduplicación. Se extienden esos seams, no se sustituyen. [E2–E4,E7–E8]

**Seam mínimo F1:** `runtime.Compose` crea StrategyFns por `def.ID`, un read model compartido y fanout separado de Provider por cuenta. `composeAccount` actualmente también crea `strategy.OwnerState` vacío y aplica configuración, por lo que repetir esa composición entera no conserva Strategy. S03 extrae esa inicialización a la composición única del experimento: mantiene `strategyEngines`/`strategyStates`, mercado/analítica, fanout y driver/clock durante toda la campaña; recompone únicamente el compartimento Account/Operation/MM/Provider/ledger/venue al reemplazar. Es una separación de responsabilidades en la composición existente, no un nuevo motor. [E4,E10]

`strategy.OwnerState` es la unidad completa de continuidad: ModuleState opaco, OwnerKey, OwnerInputSeq/RuntimeTs, StrategyEvalSeq/StrategyCycleSeq, TriggerDedup/LastBarBucket, Config efectiva/pendiente, readiness/counters y slots/campos de rollover. No basta guardar Cycle ni las ventanas H4/BB. Su estado no contiene cuenta/MM/Provider. La campaña no decodifica ModuleState ni interpreta ARMED/OPEN_CYCLE para fabricar, suprimir o reintentar señales; sólo el Engine compartido gobierna ese lifecycle. [E1,E10]

NewRun se conserva como constructor de un experimento independiente, **no como reinicio por compra**. Si S03 conserva un wrapper NewRun por compatibilidad interna, el único seam admisible es inyectar/reutilizar in-memory esos mismos owners y la lane temporal existente antes de consumir entradas: mismo StrategyID/run provenance semántico, mismo frontier, bindings prospectivos y ningún ApplyConfig sobre estado vacío ni replay de prefix. Preferir referencias de ownership único, sin copia parcial ni dos writers; clocks/views del compartimento nuevo se conectan a la lane vigente. No export/import durable, snapshots generales ni checkpoints. La cuenta nueva se abre a su activación causal, no en el WarmupStart histórico de la campaña.

S03 es dueño de implementación y pruebas iniciales; S04 LOCAL independiente es dueño de falsificación; S05 corrige y produce resultados. Primary adjudica. Ningún PASS se deriva de esta lectura CLOUD.

### 4. Configuración MM común y funcional

Agregar `scaling_mode = NO_ADDS | CONFIGURED` a configuración SDK y trasladarlo hasta GerardMM. Es el mismo Manager, no otro algoritmo.

| Entrada | Resolución |
|---|---|
| NO_ADDS sin bloque | Construir también en LIVE, adds deshabilitados explícitamente |
| NO_ADDS con bloque | Rechazar conflicto, incluso máximos cero |
| CONFIGURED con bloque válido | Usar fórmulas y límites existentes |
| CONFIGURED sin bloque | Rechazar |
| Modo ausente con bloque válido existente | Compatibilidad: normalizar a CONFIGURED y registrar |
| Modo ausente sin bloque en LIVE | Seguir rechazando; no aplicar seeds |
| Modo ausente sin bloque en receta V1 | Compatibilidad histórica solamente; nuevos perfiles siempre explícitos |

CONFIGURED permite desactivar una sola familia con máximo0; exige al menos una activa, conservando validación existente. Seeds funcionales explícitos de `ResearchScaling()`: adverso0,25R,2adds,ratio1,0; favorable0,50R,1add,ratio0,5. No son defaults LIVE. [E3]

Mantener `q_exec_max`, exposición account-wide, capacidad, reservas, ReservationRevalidate, egress one-shot, pending admission y protección. Alcanzar un umbral no obliga a admitir el add: reportar rechazo. No cambiar fórmulas para producir más operaciones.

Materializar `SL=2000` y `TP=mm_profit_objective` mediante el materializer de planes existente y el constructor `config.NewGerardMM`/EconomicPlanRowSet compartido. Baseline V2: `mm_profit_objective=1500`; barrido principal:1000/1500/2000. El parámetro se aplica a **todas las rows EVALUATION/account-day incluidas en cada experimento y a FUNDED INITIAL y STEADY**, también después de transiciones, cambios de día y reemplazos. Exportar claves/valores resueltos; no dejar FUNDED o días tardíos accidentalmente en1500. Rows ausentes siguen denegando nuevo riesgo, no reciben un fallback. BASIC conserva la clave técnica EVALUATION para seleccionar plan, sin pass/fail ni lifecycle de prop. [E2]

`mm_profit_objective` es objetivo monetario diario del MM; `payout_chunk` es retiro bruto solicitado por Campaign. Ninguno sobrescribe al otro. `payout_chunk=1500`, SL2000, pass target funcional3000, scaling, capacidad, costos y demás reglas quedan fijos en el barrido de §11. Todos son configuración explícita de investigación; no cambia la fórmula GerardMM ni se añade target a S2.

### 5. Contrato de mercado y fidelidad

#### 5.1 Vista acotada por contrato

Usar proyecciones SDK con rings limitados de barras cerradas1m/5m/H4, una forming por timeframe y últimos TRADE/QUOTE con timestamps, calidad y provenance. No copiar el histórico completo por tick. Separar contratos físicos: un alias no comparte inventario ni barras entre expiries.

S2 ya declara lookback64, SMA50/H4, Bollinger20/2 poblacional/5m y warmup51H4+20M5. Reutilizar esas ventanas, no recalcular indicadores por otra ruta. Forming nunca reemplaza silenciosamente una barra cerrada. MarketContext permanece decision-scoped, con versiones y `context_reads[]`; conservar `canonical_event_id` separado de `stream_seq`. [E1]

| Causa | Actualiza y dispara |
|---|---|
| TRADE/Last | OHLCV de trades, forming y último precio; analytics, MM/riesgo y matching declarado |
| QUOTE/Bid/Ask | Lados/freshness/valoración y referencias de ejecución; no volumen ni OHLCV TRADE |
| BAR_CLOSE | Barra cerrada elegible; S2 sólo en5m/H4 |
| Fill/ACK/cancel/reject | Órdenes, exposure, ledger, Provider, reservas y reacción inmediata MM |
| Account/provider/control/timer | Autoridades, día y restricciones; no señal artificial S2 |
| Paso OHLC modelado | Mark/forming modelados para venue/ledger/MM; no aparenta trade ni BBO observado |

El OHLC actual ya utiliza mark fallback sin `ExecutableQuoteSource`: conservarlo. Offsets de spread son datos de ejecución/valoración modelada, no QUOTE falsa. `analytics.Input{SourceBar:...}` permite señales sin ticks. [E6]

#### 5.2 Selección de fuente

OHLC1M consume SourceBars válidas y modela intrabar. TICKS respeta secuencia observada TRADE/QUOTE; spread y fills siguen modelados donde falta información. MIXED_MINUTE fija en manifest una autoridad por contrato/minuto completo: ticks íntegros válidos o SourceBar íntegra. LIVE usa eventos reales; jamás genera ticks sintéticos por ausencia/staleness del feed.

Completitud de ticks necesita evidencia de cobertura/captura, continuidad de secuencia cuando exista y reconciliación. Unos ticks cerca de ambos bordes no la prueban. No deduplicar trades legítimos por timestamp+precio; usar identidad/secuencia de origen.

En fallback, excluir los ticks y quotes parciales de todas las mutaciones de ese minuto, preservando refs de lo descartado. No mezclar quotes parciales con trayectoria sintética en esta versión. No contar volumen de barra y ticks dos veces. Sin ninguna fuente completa válida, hay un problema de cobertura, no permiso para inventar observaciones.

En TICKS/MIXED, las barras derivadas de ticks completos son autoridad. Comparar con OHLC sólo cuando coinciden contrato, fuente, timezone y calendario. Clasificar diferencias de identidad, grid, calendario, cobertura, revisión, precios o volumen. Una contradicción no explicada bloquea el comparativo estricto hasta fijar manifest coherente; no autocorregir ni escoger la fuente de mayor PnL.

Last-only produce barras TRADE, no BBO observado. Quote-only puede valorar, pero no crea señales S2 sin barras TRADE. Reportar coberturas TRADE y QUOTE separadas.

### 6. Tiempo, causalidad y warmup

#### 6.1 Buckets y disponibilidad

Reloj lógico UTC; timezone y significado del timestamp de origen quedan fijados en manifest. Una SourceBar ocupa `[IntervalStart,IntervalEnd)`; HLCV completo está disponible en AvailableAt. El perfil leído exige AvailableAt=IntervalEnd. No admitir retrospectivamente barras demoradas bajo esa misma versión. [E6]

Calendar resolver y SessionGrid SDK definen sesiones, breaks, regiones truncadas, trade-date y DST. Agregar directamente cada timeframe desde su fuente elemental compatible, no H4 desde5m ni un grid distinto para LIVE. Fuente1m no cambia señal5m. Un prefix/hueco/tail incompleto no se vuelve elegible por tener OHLC; truncación legítima de calendario no equivale a missing data. Las correcciones posteriores son revisiones de proyección, nunca reevaluación del pasado.

#### 6.2 Frontera H4 efectiva de S2

Para trigger5m `[b,b+5m)`, al cierre elegir la última H4 disponible con `CloseBoundary <= b`. La5m11:55–12:00 no ve laH4 que cierra12:00; la12:00–12:05 sí puede verla al cerrar12:05. Es `eligibleTrend` y el caso concreto de `TestS2_S203_SameBoundaryH4Visibility`. [E1]

Hay comentarios que describen mal la igualdad con apertura. S03 corrige prosa, no el comparador ni la señal. No usar orden incidental de entrega H4/5m como sustituto de elegibilidad explícita.

#### 6.3 Orden V2 explícito, no dos órdenes incompatibles

El driver de ticks define recovery1, controls2, boundaries3, market4 y ordinary timers5; OHLC V1 usa close1 y Open/gap6. **V2 adopta el orden del driver de ticks**, preservando V1. Se selecciona en los perfiles BTG/S2, sin migrar silenciosamente S1 ni otros perfiles. No exige un sequencer global. [E6,E9]

| Fase V2, mismo instante | Contrato |
|---|---|
| 1 | Recovery/callbacks ya recibidos pendientes; drenar ledger y efectos, sin adelantar callbacks futuros |
| 2 | Controles admisibles por `(effective_at,ordinal,control_id)`; expected-context y dedup intactos |
| 3 | Sesión/ventana/account-day/Provider/selección: cerrar período previo con estado disponible y aplicar nuevas restricciones antes de nuevo riesgo |
| 4 | TRADE/QUOTE u observación OHLC, incluido Open/pasos; mark/economics, órdenes previamente aceptadas y drain entre fills |
| 5 | Finalización de SourceBars y timers ordinarios de cierre/expiry; publicar barras cerradas y evaluar S2 |

`rootOHLCOpen/rootOHLCStep` son fase4; `rootOHLCClose` fase5. Finalizar fuentes terminadas antes de notificar BAR_CLOSE y deduplicar el timer equivalente. Publicar H4 antes de5m en empate, sin sobrepasar §6.2. Otros timers usan owner/kind/id/generation estable. Cada causa drena efectos antes de la siguiente. El fill fase4 gana a expiry fase5 como en el driver existente.

**Consecuencia visible:** un Open con mismo UTC que BAR_CLOSE ya ocurrió en fase4 cuando S2 emite en fase5. La nueva orden no llena retrospectivamente allí: usa el siguiente tick, paso modelado u Open posterior. V1 conserva señal→next-Open; V2 no promete su PnL. Un doji sin pasos posteriores al Open espera otra observación, sin inventar trades para llenar.

En cambio de día, el estado previo a frontera pertenece al período saliente; nuevo mark fase4 y decisiones fase5 usan el nuevo contexto. El intervalo del trigger no se retaggea. No resetear balance. Probar atribución diaria y expiraciones en ambas rutas.

Runtime aplica prioridad sólo a causas independientes disponibles en el mismo frontier local. Orden observado y disponibilidad prevalecen: jamás deshacer un callback entregado para acomodarlo en otra fase. Registrar event-time, recepción/disponibilidad y ordinal. Un cierre retrasado se evalúa al llegar, sin backdating. Paridad exacta compara esos mismos inputs, no borra latencias.

En timestamp igual, respetar secuencia de origen. Sin orden global entre canales, desempate stream/canal/ordinal declarado `CROSS_CHANNEL_ORDER_MODELED`, no observado. Regla de ejecución: **accepted_coordinate < executable_observation_coordinate**. No basta comparar timestamps. ACK/protección pueden instalarse después de un fill; nueva orden necesita observación posterior y nunca visita un extremo pasado.

`EnqueueControl` sigue exigiendo effective_at>completed_frontier. La campaña no cuela controles retroactivos con ordinales. Ninguna modificación de despliegues LIVE/D6 forma parte de S02. [E7–E9]

#### 6.4 Warmup y readiness

Distinguir tres escenarios, sin convertir la disponibilidad de cuenta en `in.Warmup`:

| Escenario | Mercado/Strategy | Cuenta/ejecución |
|---|---|---|
| Inicio único del experimento | Owner nuevo una vez, prefix con `Warmup=true`; absorbe51H4/20M5 y tendencia elegible; no abre/cierra ciclos durante ese prefix | Sin compras ni órdenes previas a TradeStart; sin resultados económicos retrospectivos |
| Pausa temporal sin cuenta admisible, después de TradeStart | Mismos owners y reloj; todos los cierres válidos siguen por Engine normal, `Warmup=false`, con readiness real | Fanout vacío o bindings deshabilitados para nuevo riesgo; mantener management/cierre a owners todavía responsables de obligaciones |
| Reemplazo o cambio de etapa/cobro | No releer prefix ni resetear módulo, dedup, ciclo, config, analytics o secuencias por account_id/stage_id | Sólo estado propio nuevo de cuenta o transición del mismo account según §§9.1–9.3; no heredar exposición/PnL |

En source, `DecodeState` vacío arma S2, `CycleActive` depende sólo del módulo y `onEntryBar` retorna ante `in.Warmup` antes de abrir/cerrar ciclos. Recalentar indicadores desde cero no reproduce el estado técnico a mitad de campaña. Por ello el warmup inicial no sirve como recuperación del owner perdido: si ese owner se pierde, declarar error y rerun del experimento desde sus inputs, no reconstruirlo parcialmente. [E1]

Cuando no hay cuenta operable, S2 puede emitir OPEN y quedar en ciclo aunque nadie reciba/admitiera la señal; un rechazo de Operation/Provider tampoco la rearma. Fanout no reevalúa Strategy: target vacío produce cero entregas; deshabilitar nuevo riesgo no suprime REDUCE/CLOSE/CLOSE_ALL hacia targets aún visibles. Una cuenta activada posteriormente recibe sólo señales futuras linearizadas contra su binding efectivo, nunca señales acumuladas durante la pausa. La vuelta a basis/invalidation sigue cerrando el ciclo mediante S2 normal, y esa barra de re-arm no abre. No confundir cero entregas con cero señales. [E1,E10]

Feed-ready, analytical-ready, mark/quote vigente y autorización son distintos. LIVE stale bloquea nuevo riesgo aunque haya barras calientes. Recuperación requiere datos frescos reales, continuidad/clasificación del hueco, ventanas cubiertas y reconciliación de órdenes/posiciones; el reloj solo no rearma. Reconstruir analítica después de un gap no autoriza resetear el ciclo técnico: aplicar exclusivamente la misma política del runtime con los mismos inputs/estado. Si su continuidad no puede demostrarse, conservar estado/bloqueo STRICT; no sustituirlo por ARMED ni por un prefix que sólo actualiza indicadores.

### 7. Ejecución OHLC V2 y scaling intrabar

Mantener OHLC_V1 y fixtures/receta anteriores. V2=`OHLC_CAUSAL_PATH_V2`; incluir versiones de fases, path, tiempos, offsets, fees, slippage, fuentes, calendario, MM y campaña en digest. Build/manifests originales prueban replay V1; no declarar byte-identidad borrando cambios semánticos de una nueva build.

Al Open revelar sólo O; procesar gaps/stops/markets elegibles y callbacks. Elegir una vez referencia según exposición neta tras Open; si no existe, dirección de entrada aceptada pendiente; sin ambas, LONG fijo. Registrar, sin mirar resultado final.

- LONG: O→L→H→C.
- SHORT: O→H→L→C.
- Sensibilidad: invertir orden de extremos, resto idéntico.

Definir la ruta de referencia por segmentos dentro del minuto en lattice de tick size, un tick por paso, omitiendo vértices repetidos. Generarla incrementalmente/lazy; sólo omitir despacho de pasos bajo §7.1, sin cambiar el recorrido modelado. No recorrer distancia Close anterior→Open siguiente ni interpolar gaps, breaks o rollovers. Precio fuera de lattice se rechaza, no se redondea source.

Open tiene tiempo modelado start. Para K pasos posteriores, paso i ocurre en `start + floor(i*duration_ns/(K+1))`, i=1..K; Close se alcanza antes de publicar barra en end. Rechazar si no permite tiempos estrictamente crecientes; no recortar pasos silenciosamente. Timers se intercalan. Son tiempos modelados, no trades observados.

El generador puede conocer HLCV; Strategy/MM sólo ven precio actual y forming acumulado. Caminar lattice evita duplicar umbrales/fórmulas Gerard en el simulador. Volumen fuente se publica una vez al cierre; forming volume desconocido si no inferible. Los pasos no crean otra señal S2. Medir costo de esta expansión: no asumir throughput V1.

**SL-first:** para protecciones estáticas activas desde Open y salidas aún no resueltas allí, el recorrido adverso alcanza primero SL cuando admite SL/TP. Un gap observable en Open se resuelve allí, no se ignora por pesimismo retrospectivo. Protección creada después sólo opera sobre recorrido restante; etiquetar `POST_ACTIVATION_PATH_ASSUMPTION`. No imponer SL-first a ticks que demuestren TP antes, ni afirmar peor PnL global con adds/protección dinámica.

Por observación, priorizar protección reductora frente a entradas simultáneamente elegibles y desempatar órdenes establemente. **Un fill a la vez:** ledger/fees→economics→Provider/capacidad→Operation/MM→ACK/cancel/reservas. Reconsiderar órdenes restantes tras cada callback. No precomputar un batch contra estado viejo que ignore cancel o exposición nueva.

Adds adversos/pyramiding son GerardMM compartido. Tras cada fill, revisar exposición agregada, q_exec_max, protección y headroom antes del siguiente add. Probar add→stop, add→nuevo target, fill parcial, rechazo y CLOSE con add pendiente. Stop-market con gap ejecuta al primer precio posterior disponible+costos, no stop ideal. MARKET nuevo espera siguiente observación. LIMIT, sólo si soportado/emisión real del dominio, respeta límite incluso con slippage; no agregar tipos accesorios.

Sin libro/queue/depth, ticks no certifican liquidez/fills. Conservar y exportar hipótesis de llenado; volumen de minuto no garantiza capacidad de una orden. No exigir igualdad PnL OHLC/ticks.

**Paridad exigible:** mismos config/estado/calendario/reloj/inputs normalizados→mismas barras elegibles, señales, decisiones MM, órdenes/rechazos y accounting. Para comparar dominio, inyectar mismos fills en ambos adapters. Normalizar sólo IDs/provenance no semánticos con mapeo1:1; no borrar contrato, orden, precio, cantidad, fee, tiempos causales, versiones ni razones. Mismas barras con recorrido distinto pueden producir distinta economía/campaña; comparar señales sólo con estado equivalente.

#### 7.1 Generación lazy y omisión demostrablemente inerte

La ruta `REFERENCE_EVERY_STEP` es el oráculo correcto: iterator con una SourceBar, vértices, índice de segmento/paso y próximo root, intercalado con el scheduler existente. No crear arrays por minuto, por archivo ni por los13 archivos. Fuente/cursors, rings analíticos, buffers de export acotados y un lookahead por stream activo bastan; resultados se escriben incrementalmente sin replicar histórico ni acumular cada paso en RAM. El espacio del **generador** es O(streams activos + ventanas/buffers configurados), independiente de filas, duración y amplitud de vela. Las retenciones propias de owners/resultados existentes se miden por separado, no se ocultan dentro de esa cota.

`SKIP_PROVEN_INERT` puede evitar llamadas por pasos sintéticos intermedios, no fuentes ni causas semánticas. Condición suficiente conservadora: cero exposición, órdenes/protecciones/reservas/pending admission o trabajo de Operation/MM que pueda reaccionar a mercado, callbacks pendientes con efecto, ni otro consumidor intrabar activo. Warmup inicial sin obligaciones es un caso típico; ausencia temporal de cuenta con Strategy bars-only puede ser otro. **Flat al Open no demuestra inercia del resto del minuto.** Usar estado/demanda estructural de los owners existentes, no copiar fórmulas, targets o umbrales Gerard en el generador. Consumidor desconocido o prueba insuficiente ⇒ referencia.

Nunca omitir Open, cierre/finalización de SourceBar, cierres5m/H4, controles, timers, callbacks ni fronteras. S2 sigue recibiendo exactamente cada cierre elegible y avanza sus ciclos también durante pausas. El siguiente evento material en el scheduler limita el salto: antes de entregarlo, establecer la proyección causal del **último paso de referencia anterior según la coordenada completa** (tiempo/fase/ordinal), no según sólo timestamp. Conservar precio/fecha del mark, freshness, forming del prefijo ya recorrido, readiness, versiones/canonical IDs y orden lógico que un consumidor posterior podría leer. Se puede calcular geometría/ordinal del prefijo del path conocido, nunca exponer extremos aún futuros, recalcular economía por otra ruta ni rejuvenecer marks. Si una mutación intermedia de ledger/Provider/analítica o su versión es observable y no se preserva exactamente sin ejecutar al owner, ese tramo no es elegible para el atajo.

Reevaluar la condición tras **cada** causa y su drain. Una señal al BAR_CLOSE, orden recién creada, callback, control, timer intraminuto o protección activada obliga a procesar desde el siguiente paso de referencia posterior que corresponda, sin saltar umbrales ni visitar precios pasados. En empate conservar §6.3: un Open/paso fase4 ya pasado no llena una orden creada en fase5. No recomputar K, dirección de path, tiempos ni ordinales al reactivarse; el iterator continúa el recorrido original. Puede reentrar al atajo sólo después de probar nuevamente ausencia de consumidores, no por haber quedado flat a simple vista.

La optimización no concede permiso para omitir TRADE/QUOTE reales, tolerar missing-open ni cruzar gaps/rollovers. En MIXED sólo afecta minutos cuya autoridad sea OHLC completa. La ruta de referencia queda seleccionable para fixtures y segmentos comparativos; se exige equivalencia en todos los eventos materiales de OwnerState Strategy, barras/MarketContext, señales/entregas, decisiones MM/Provider, órdenes/fills/rechazos, ledger, curvas/economía de cuenta y caja/lifecycle. Sólo pueden diferir contadores de trabajo/tiempo/memoria y registros explícitos de rangos inertes no despachados, nunca IDs/versiones semánticas ni resultados. T35/T36 localizan primera divergencia; una divergencia desactiva el atajo afectado hasta reparación en S03, no se normaliza para aprobar un benchmark.

### 8. BASIC_100K_V2

Una cuenta con saldo100000, S2 vigente, SL2000 y `mm_profit_objective=1500` baseline para horizonte completo y Provider SIM sin términos de aprobación/terminación de prop. El objetivo MM es configurable mediante §4; la única corrida BASIC extensa presupuestada conserva1500, no añade tres BASIC al barrido CAMPAIGN. Sin compras, retiros, reset o reemplazo. Variante NO_ADDS comparativa y variante CONFIGURED con seeds explícitos; costos y calendario fijados.

Todas las oportunidades significa las admitidas por Strategy/MM/Provider/seguridad. No fuerza fills, borra límites diarios o rearma ciclos rechazados. Capital/headroom insuficiente impide nuevo riesgo, sin inventar fondos para seguir.

Separar evaluaciones elegibles, señales, operaciones materializadas/sin fills/con fills, fills, rechazos de admisión/órdenes, readiness y daily limits.113 operaciones no equivalen a113 trades.

Exportar gross/net realized PnL, fees, slippage respecto a referencia, unrealized, balance/equity, drawdown de ambas, exposición máxima/temporal y resultados por día/mes/contrato/segmento. Slippage ya incluido en precio no se resta otra vez. Invariante: balance=initial+realized_net+non_trading_cashflows; en BASIC estos cashflows son0. No reiniciar balance por mes/expiry.

REPORT_RESIDUALS es default: posiciones/órdenes y freshness explícitos al horizonte. REQUIRE_FLAT necesita causa y precio ejecutable dentro del horizonte; nunca rellena con último Close elegido retrospectivamente. Equity stale/no valuada se etiqueta.

### 9. CAMPAIGN: caja personal y lifecycle

#### 9.1 Invariantes y compra

Ledger SDK es autoridad única de trading. Caja personal sólo registra compras, costos personales explícitos y cobros netos:

`cash = 5000 − 120*purchases_applied − explicit_extra_cash_costs + collected_net_payouts`.

Sin extras,41 compras financiables y80 remanentes. No significa simultaneidad ni compra obligatoria del lote.

**Ejemplo obligatorio:** caja5000→comprar cuenta por120→4880. Cuenta nominal100000 pierde2000 y puede quemarse: **caja sigue4880**. Sin segundo débito120, sin débito2000 ni100000. Otra compra posterior cobra120 una vez→4760.

Un payout bruto1500, split100%,fee0 cobrado después de primera compra deja6380. Split90% explícito produce1350 netos y caja6230; la cuenta debita1500. No descontar split ni comisiones de trading otra vez de caja.

IDs: campaign/purchase/account/stage/context/payout/ordinal/control/cashflow. Mismo ID/payload es no-op; payload divergente es FAILED. USD exactos SDK, sin floats. Neto positivo redondeado hacia abajo a centavo, política identificada; rechazar split fuera[0,1], fees negativos o neto no positivo. Cobro0 no es retiro exitoso.

ON_DEMAND compra al necesitar cuenta, caja≥120, sin obligaciones/payout anterior irresuelto y con siguiente intervalo admisible antes de horizonte. No compra durante warmup. Activación no cobra nuevamente.

Alternativa Owner lote41: débito4920 al comprar, caja80 e inventario con activación gratuita; nunca cobrarlo otra vez ON_DEMAND. No construir almacén genérico de precompradas; mantener recomendación ON_DEMAND hasta decisión distinta.

Reemplazar burned/retired sólo tras quiescencia: posiciones0, órdenes terminales, reservas/pending admission liberadas y callbacks drenados. Operation terminal retenida para auditoría no es exposición activa. Retirar el binding de A sólo tras drenar sus obligaciones; conservar sus resultados, no transportar su estado operativo a B. Nueva cuenta con `account_id` y binding/account_strategy_id propios, balance inicial declarado, Operation/MM/Provider/ledger/venue nuevos y cero exposición, órdenes, reservas, PnL o contadores económicos heredados de A. Identidades nuevas no colisionan con las archivadas. La compra cobra120 una vez; activación y burn no cobran nuevamente.

La activación de B es prospectiva, posterior al frontier completado, en el siguiente Open1m admisible antes del horizonte. Sólo se sustituye el compartimento de cuenta de §3: **mercado/analítica, Strategy, fanout y reloj continúan**; el TradeStart inicial de Strategy no se redefine. No reingestar prefix ni aplicar warmup a una cuenta nueva. El target set se actualiza por el seam compartido con versión monótona; no relinearizar señales históricas al añadir B. Entre cuentas, seguir §6.4 sin permitir nuevo riesgo a targets deshabilitados. No operar varias cuentas a la vez ni reutilizar listado fijo de trades.

Falsificador normativo: si A se quema o se retira mientras S2 está `OPEN_CYCLE_LONG`, B comienza con ese mismo ciclo Strategy; no obtiene un OPEN adicional sólo porque cambió account_id. Si el ciclo se cierra durante la pausa por basis/invalidation, B observa el resultado de esos cierres reales, no un reset administrativo. Burn, retiro, compra, cobro y transición de etapa no son causas de re-arm. Igual para SHORT. T33/T34 comparan contra una Strategy runtime mantenida viva, antes/durante/después del primer reemplazo.

#### 9.2 Stages funcionales explícitos, no reglas comerciales

| Parámetro | EVALUATION | FUNDED |
|---|---|---|
| Nominal |100000|100000 tras transición explícita|
| Gerard account-day |SL2000/TP=`mm_profit_objective` en todas las rows/account-days; baseline1500|INITIAL y STEADY con el mismo objetivo candidato y SL2000|
| Scaling |CONFIGURED seeds §4; NO_ADDS comparativo|Igual|
| Riesgo total |Piso equity absoluto98000, touch/below breach|Piso estático98000, payout no lo baja|
| Pass |Realized net≥3000 y mínimo2 días con fills|Sin target de aprobación|
| Retiro |No permitido|Profit realizado disponible sobre100000, flat/quiescent|
| Plazo/consistencia/fees periódicos/activación |OFF/0 explícito|OFF/0 explícito|
| Trading fees/modelo |2,49 contrato/fill,slip1,offsets1/1|Igual|
| Retiros |0|Máximo4 cobros exitosos; `payout_chunk=1500` fijo en barrido principal|

Materializar en RuleSet/ProgramTerms Provider existentes. Provider decide pass/breach con accounting real; Campaign no compara equity por otra fórmula ni calcula sizing/headroom. Mantener límites de instrumento/capacidad y entitlement SIM; exportar perfil resuelto y digest. El runner acepta inicio FUNDED como escenario alternativo declarado para probar payouts; principal recomendado EVALUATION→FUNDED.

#### 9.3 Transición y retiros

Pass usa outcome y OutcomeAwaitContext. Cerrar/cancelar y esperar quiescencia. En frontera futura, aplicar RESET_ADJUSTMENT firmado para llevar saldo a100000, después AccountContextTransition con expected balance/context, START_NEW_STAGE, día nuevo explícito y risk seed98000. CLOSE_ONLY entre controles; error impide riesgo. Ajuste es cashflow no-trading de cuenta y cero para caja; conservar PnL de evaluación y puente contable. Mismo purchase_id, activación0, sin segunda compra. START_NEW_STAGE cambia sólo el contexto económico de cuenta y sus planes declarados; no reinicializa el owner Strategy de §§3/6.4.

Payout elegible: FUNDED sin breach, flat/quiescent, profit realizado disponible≥chunk, saldo posterior respeta piso/buffer, menos de4 cobros y ninguna solicitud pendiente. Leer estado/autoridades del motor; la campaña sólo ejecuta su política de retiro declarada.

Solicitar registra payout_id,gross,net previsto,economics/context y fecha; caja no cambia. Pausar con AccountContextTransition del mismo stage, PRESERVE_STAGE/CONTINUE_CURRENT_DAY/PRESERVE_RISK_STATE, contexto nuevo y binding Enabled=false. Solicitar sólo desde frontier completado quiescent; pausa en frontier+1ns antes de próxima observación posterior. Motor sigue ingiriendo mercado/calendario y entregando cierres al mismo owner Strategy con Warmup=false. El binding limita nuevo riesgo, no el ciclo técnico; rechazos y señales sin destinatario siguen §6.4. Probar que deshabilitar binding no crea breach ni resetea estado. No sistema general de reservas de retiro.

En siguiente apertura negociable estrictamente posterior, revalidar contexto/importe/estado y encolar ACCOUNT_CASHFLOW(PAYOUT_DEBIT=-gross), tratamiento EXCLUDE_PERFORMANCE_PRESERVE_ABSOLUTE_RISK_V1. Sólo con disposición APPLIED y recibo simulado de cobro: acreditar neto y contar retiro una vez. Rechazo/conflicto no acredita. Compartir payout_id entre débito, settlement y caja; mantener RECEIVABLE distinto de PAID. Si falla consistencia/escritura, FAILED y replay desde inputs, no checkpoint inventado.

Después de cobrar, otra transición preserva estado y habilita binding, salvo cuarto cobro: latch RETIRED_PAYOUT_LIMIT antes de riesgo nuevo. Nunca quinta solicitud exitosa. Reportar saldo/beneficio residual no cobrado como forfeited según propuesta, no caja ni retiro extraordinario. El nominal100000 no es riqueza personal.

Al horizonte, listar requests,debits,receivables y controles PENDING_AT_HORIZON por ID. No ejecutar fuera de EndExclusive. PnL no retirado y solicitudes no financian compras.

BANKROLL_EXHAUSTED requiere caja<120, sin cuenta operable ni cobro pendiente capaz de financiar otra dentro del horizonte. Cuenta viva sigue; sólo receivable implica WAITING_SETTLEMENT hasta fecha/horizonte. Exportar curva cash, purchases, funded,burned,retired,activas,requested/collected gross/net,extras,forfeited,agotamiento,drawdown caja,días activos/inactivos y PnL nominal separado. Métrica principal: `cash_final−cash_initial`, sin nominales/pendientes.

### 10. Gaps, cobertura y rollover

| Caso | Evidencia y conducta |
|---|---|
| Cierre/break/feriado |Calendario u override fechado con fuente; hueco no prueba feriado; sin velas sintéticas|
| Minuto sin trades |Cobertura/captura íntegra o confirmación proveedor; Last ausente no basta; intervalo vacío explícito sin OHLC inventado|
| Missing-open desconocido |Strict detiene antes de atravesarlo, conserva estado y refs|
| Fuente fuera de sesión |Contradicción visible o exclusiones derivadas ya autorizadas; sin cambiar calendario silenciosamente|
| Prefix/tail |Agregado incompleto no elegible; sin extrapolar final|
| LIVE missing/stale |Sin nuevo riesgo ni ticks/ACK/fills sintéticos; exposición/órdenes conservadas|
| Rollover |Schedule físico explícito, no salto de precio de una posición trasladada|

**Principal: STRICT**, conservando FAIL_VISIBLE_GAPS_V1/errores reales. Sin precio después de CLOSE, no fill ni mark viejo ejecutable. Gap con obligaciones conserva residuales; no quemar/recomprar porque el futuro sea desconocido.

Un reporte exploratorio SEGMENTED_FLAT_ONLY es opcional de segunda prioridad, no requisito para dos modos: saltar sólo flat/quiescent con pausa explícita y rewarmup; conservar caja/balance si se trata de misma cuenta. Sigue PARTIAL por abstención y oportunidades omitidas; no participa en selección principal. No reanudar aproximadamente con exposición abierta ni sumar cuentas reseteadas como continuidad. Si no cabe, strict y segmentos independientes rotulados, sin fase adicional.

Vacío confirmado no genera vela plana al precio anterior. Reutilizar representación SDK de intervalos vacíos; si SourceBar no puede expresarla sin inventar precio, implementar/probar el delta acotado o error visible. Coverage completo no rejuvenece mark/quote.

Rollover reutiliza catálogo/schedule/preparation/retirement. Contrato viejo mantiene órdenes, inventario, fees y marks hasta liquidación; nuevo tiene barras/warmup/snapshot propios. Solicitar liquidación causalmente antes de precio ejecutable dentro de horizonte, no elegir retrospectivamente última vela buena. Viejo sin datos y con obligaciones falla OLD_CONTRACT_DATA_UNAVAILABLE o guard equivalente. Cuenta/caja/account-day continúan; ningún PnL del salto entre expiries. No back-adjustment para fills ni indicadores mezclados sin autoridad existente.

STRICT termina ante indeterminación; corregir cobertura implica manifest nuevo y replay desde inicio, no checkpoint. Pausa flat autorizada sólo reconstruye analítica bajo la política equivalente del runtime, no dinero/contadores ni ciclos técnicos (§6.4). SEGMENTED_FLAT_ONLY no autoriza una política nueva para cruzar gaps y nunca certifica continuidad Strategy que no pueda demostrarse. Recuperación LIVE exige datos reales y reconciliación; este shot no la ejecuta.

Separar execution_state,coverage_status,fidelity,economic_terminal_reason:

- COMPLETE: horizonte o terminal económico legítimo, cobertura requerida resuelta y política final cumplida; REPORT_RESIDUALS permite posiciones/órdenes expresamente listadas, no afirma liquidación.
- PARTIAL: prefijo/subhorizonte/segmentos válidos frente a horizonte solicitado incompleto o modo aproximado. Child strict puede conservar execution_state=FAILED y coverage_status=PARTIAL; no maquillar error.
- FAILED: config/identidad/secuencia/ledger/control/replay inválidos o contrato strict incumplido; cifras sólo del prefijo confiable.

Campaña atravesando gap con exposición, payout irresuelto, reemplazo artificial o reset de bankroll no tiene cifras finales defendibles: UNKNOWN, no0. Sumar segmentos completos no demuestra campaña continua ni probabilidad de ruina.

Los dos modos funcionales son BASIC y CAMPAIGN; demostrar su funcionamiento sobre cobertura validada es distinto de certificar una trayectoria continua por13 contratos. Un prefijo COMPLETE a su horizonte acotado no concede gate integral: reportar horizonte solicitado/validado, primer bloqueo y cobertura integral no demostrada. Ambos modos se ejecutan realmente y gaps/rollover se adversarializan en S03–S05; UNKNOWN no se convierte en0.

### 11. Targets, holdout y presupuesto finito

#### 11.1 Barrido principal: objetivo MM, retiro fijo

Tres candidatos de `mm_profit_objective` diario: USD1000,1500,2000. Mantener SL2000, `payout_chunk=1500`, S2, fórmulas Gerard, scaling CONFIGURED de §4, costo120, split/delays, pass target, demás reglas/costos, datos, calendario y modelo de ejecución idénticos. Aplicar el objetivo a las rows incluidas en §4 para EVALUATION y FUNDED INITIAL/STEADY, también al reemplazar cuentas. Baseline1500 preservado; receta V1 aparte, intacta. Cada candidato requiere **rerun real completo del motor compartido y la campaña** desde sus propios inputs/estado inicial: el objetivo puede cambiar sizing, adds, stops, duración, headroom, quema y cobros. Prohibido transformar una lista fija de trades.

`payout_chunk` se mantiene configurable/reportado. Su optimización queda fuera del primer barrido principal; una exploración secundaria sólo puede ocupar un cupo ya existente y libre de sensibilidad, después de cubrir los casos obligatorios, identificada como exploratoria y sin entrar a selección/holdout principal. No crear9 combinaciones ni aumentar corridas extensas.

Orden de selección: mayor cash_final−cash_initial después de compras/costos y sólo cobros netos; luego menos compras; luego mayor caja mínima; empate restante conserva `mm_profit_objective=1500` baseline. Medir agotamiento, cuentas consumidas, inactividad, pendientes/residuales y sensibilidad, no sólo PnL nominal.

Antes del PnL, fijar manifest por calidad/cobertura: mayor tramo continuo validado con warmup, account-days completos divididos cronológicamente70% selección/30% reservado. Registrar fechas/digests antes de primera corrida. El amplio NQ09-26 reportado S01 es candidato de cobertura, no ganador por rentabilidad. Holdout es experimento separado con caja5000 y warmup previo, no hereda tres balances de entrenamiento. [A4]

Holdout evalúa una vez el objetivo MM ganador congelado y el objetivo baseline1500, ambos con `payout_chunk=1500`; deduplicar cuando coinciden. Sin cobertura suficiente o evidencia de lifecycle, NO_DEFENSIBLE_TARGET_SELECTION; no retocar targets por holdout. Reportar muestra y limitación; cero retiros puede ser resultado válido, no robustez estadística.

Máximo10 corridas extensas V2:3 selección, hasta2 holdout,1 BASIC,2 reproducciones BASIC/CAMPAIGN y hasta2 sensibilidades; deduplicar si ganador=baseline. Más2 compatibilidad V1 cuando corresponda. Smokes13 contratos y E2E no son combinaciones de optimización.

#### 11.2 Censo y gate de costo antes del lote

Los6m47s/~528MiB reportados en S01 pertenecen a V1; no estiman V2 ni fijan un presupuesto por multiplicación. **Antes de corridas extensas, S03 LOCAL debe censar el corpus disponible y medir V2.** El censo streaming no ejecuta trading ni cambia datos: para cada SourceBar válida contar source rows y pasos geométricos posibles por ruta, `K_LONG=(|O−L|+|L−H|+|H−C|)/tick_size` y `K_SHORT=(|O−H|+|H−L|+|L−C|)/tick_size`, más un Open; finalizaciones/timers van separados. Usar aritmética exacta y el mismo lattice del modelo. Como la dirección al Open depende del estado, reportar ambas sumas y límites por minuto/archivo, no presentar una elección desconocida como censo exacto del run. El run registra K seleccionado y suma real, aun cuando parte no se despache. Desglosar RAW/derivado/exclusiones y ventanas warmup/trading del manifest; no contar los13 smokes como una trayectoria continua.

Medir antes del lote un tramo real representativo preregistrado por cobertura y distribución de amplitud, con warmup, cierres y actividad intrabar CONFIGURED; añadir fixtures dirigidos si el histórico no ejercita adds/protección/pausa. Comparar referencia y atajo sobre el mismo tramo manejable. No elegir sólo flat/warmup para obtener un número favorable. Evidencia: commit/build/comando/hardware, manifest/digest, intervalo, source rows, K potencial/seleccionado, pasos realmente procesados y omitidos con razón, causas/timers/fills, tiempo de warmup y trading por separado, peakRSS por fase y máximo del proceso, bytes de resultados y curva de crecimiento. S03 puede añadir instrumentación focalizada; si una métrica no fue capturada, reportar UNKNOWN y medirla, no inferir0.

S03 declara antes de medir los límites disponibles de tiempo/memoria/disco para la ventana Owner y evalúa el lote usando ese censo y medición V2, con incertidumbre explícita. **No lanzar el lote sin evidencia de corrección del atajo y ajuste a esos límites.** Si aparece un cuello de CPU/retención/resultados, corregirlo y repetir equivalencia/benchmark dentro de S03; no degradar causalidad, saltar controles ni trasladar esa reparación a S05. Se pueden reducir sensibilidades secundarias, nunca sustituir las tres selecciones MM, ambos modos, replay o adversarial por un PASS retórico. Si aun así no cabe, reportar gate de costo BLOCKED con medición concreta al Primary; no inventar throughput. Esta es una precondición LOCAL de lanzamiento, no un gate cerrado por CLOUD.

#### 11.3 Tabla de resultados requerida

Una fila por ejecución, sin mezclar configuración con outcome. Todas las cifras están pendientes de ejecución LOCAL en esta enmienda.

| Candidato / partición | Modalidad | mm_profit_objective USD/account-day | SL USD | payout_chunk USD bruto | Rows MM efectivamente resueltas | Resultado |
|---|---|---:|---:|---:|---|---|
| MM1000 / selección | CAMPAIGN |1000|2000|1500|EVALUATION + FUNDED INITIAL/STEADY; IDs/digest|NOT_RUN|
| MM1500 / selección baseline | CAMPAIGN |1500|2000|1500|Mismas claves y horizonte|NOT_RUN|
| MM2000 / selección | CAMPAIGN |2000|2000|1500|Mismas claves y horizonte|NOT_RUN|
| Ganador congelado / holdout | CAMPAIGN |Pendiente de selección|2000|1500|Perfil congelado, sin retuning|NOT_RUN|
| MM1500 / holdout baseline | CAMPAIGN |1500|2000|1500|Deduplicar si ganador1500|NOT_RUN|
| BASIC baseline / horizonte validado | BASIC |1500|2000|N/A — sin retiros|EVALUATION técnica, todos los días|NOT_RUN|

Cada fila exporta run/build/config/manifest/seed/versions y fechas; estado de ejecución/cobertura/fidelidad; señales/entregas/rechazos, operaciones con/sin fills, fills, gross/net/fees/DD y residuales; para CAMPAIGN compras/burns/retired, requested/collected gross/net, cash inicial/final/mínima, cash_final−cash_initial, pendientes e inactividad. Añadir métricas de §11.2 y referencias de replay. Un objetivo distinto puede legítimamente producir los mismos trades en un tramo; probar que llegó al MM real, no exigir diferencias artificiales ni prometer ganador rentable.

### 12. Matriz de aceptación S03–S05

**Todas NOT_RUN_BY_CLOUD.** Cada evidencia LOCAL necesita comando, commit/build, inputs, salida y artefacto. S04 independiente crea ataques, no sólo ejecuta tests del implementador.

| ID | Falsificación | Resultado exigido | Shot |
|---|---|---|---|
|T01|Golden S01 V1 y fresh process|Baseline reproducible, V2 separado|S03/S05|
|T02|Mismos config/estado/eventos vía ambos adapters, incluidos owners tras reemplazo|Decisiones, OwnerState, señales/entregas, órdenes/rechazos y economics iguales; normalización sólo no semántica y bijectiva|S03–S05|
|T03|TRADE/QUOTE y barras1m/5m/H4|Quotes no contaminan OHLCV ni volumen; una fuente una vez|S03/S04|
|T04|Forming con extremos futuros tentadores|Sin leakage a closed/indicadores/señales|S03/S04|
|T05|H4 y trigger en frontera12:00/12:05|CloseBoundary<=entryOpen exacto|S03–S05|
|T06|Inicio único con prefix51H4/20M5 vs pausa/reemplazo|Sólo inicio usa Warmup; después siguen ciclos y cierres; cuenta nueva no rewarmup ni trading retrospectivo|S03/S04|
|T07|Cierre/Open con UTC igual; V1/V2 distintos|Regla causal posterior; V2 no rellena Open fase4 desde señal fase5|S03/S04|
|T08|SL/TP mismo minuto LONG/SHORT y ticks ordenados|SL-first estático declarado; secuencia observada prevalece|S03–S05|
|T09|Stop gap Open|Precio posterior+costos, no stop ideal ni interpolación|S03/S04|
|T10|Orden/protección después del extremo|Sin fill retroactivo; sólo recorrido restante|S03/S04|
|T11|Fill→cancel→otro fill en misma observación|Ledger/Provider/MM actualizados entre eventos|S03/S04|
|T12|NO_ADDS LIVE/BACKTEST y missing config LIVE|Mismo perfil explícito; ausencia LIVE sigue rechazando|S03–S05|
|T13|Adverse solos, pyramiding solo, ambos|Casos con fills de cada familia y límites/rechazos probados|S03–S05|
|T14|Add pendiente al CLOSE, partial fill, q_exec_max/headroom|Sin doble riesgo, bypass de reservas ni protección perdida|S04/S05|
|T15|Ticks completos, OHLC-only, parcial fallback|Minuto único, sin duplicados ni BBO falso|S03–S05|
|T16|LIVE stale vs sin ticks históricos|LIVE sin sintéticos; OHLC conserva señales válidas|S03/S04|
|T17|BASIC/CAMPAIGN misma cuenta/config inicial y continuidad posterior contrastada con runtime|Trading igual hasta primer control; después paridad de Strategy con mismos inputs/estado, sin exigir economics iguales entre modos|S03/S04|
|T18|Caja5000→compra120→pérdida cuenta2000|Caja4880 sin débito al burn|S03–S05|
|T19|Purchase/payout duplicado y payload divergente|No-op exacto o conflicto fatal, nunca doble dinero|S03/S04|
|T20|Solicitud/pausa/cobro tardío,split90%,fee|Caja sólo al cobro; pausa preserva estado/no breach; sin doble descuento|S03/S04|
|T21|Cuarto/quinto payout y horizon pendiente|Retirada al cuarto, quinto imposible, pending fuera de caja|S03–S05|
|T22|Eval→funded/reset/context con ciclo Strategy abierto y objetivo candidato|Cashflow no-PnL, quiescencia, planes correctos; costo total120; Strategy no se reinicia|S03/S04|
|T23|Caja<120 con cuenta viva/receivable, compra al final|Sin falso agotamiento ni compra fuera horizonte|S03/S04|
|T24|Gap con exposición/órdenes y salto flat|Fail/residuales visibles, sin fill/burn/dinero inventados|S03–S05|
|T25|Chicago day/DST/break/H4 truncada legítima|Mismas barras/días, sin reset doble ni atribución arbitraria|S03–S05|
|T26|Roll salto grande/viejo sin datos|Sin PnL del salto; estados preservados/fail-visible|S03–S05|
|T27|Gross/net/fees/slippage/cashflow/DD|Ledger/caja exactos; retiro/reset no trading PnL|S03/S04|
|T28|Real extenso ambos modos con scaling y fresh replay|Exports auditables y dos reproducciones|S05|
|T29|Inventario13, warmup/guards/roll|Pendientes S01 probados o explícitos; archivo no certifica continuidad|S03–S05|
|T30|Barrido objetivo MM1000/1500/2000, chunk fijo, selección/holdout|Reruns reales independientes, tres perfiles de plan/digests; SL2000/chunk1500/resto fijo; baseline/ties y preregistro sin cherry-picking|S03/S05|
|T31|Ticks→bars frente a SourceBars coherentes/incoherentes|Igualdad debida o diferencia clasificada, sin autocorrección|S03/S04|
|T32|S1 y regresiones existentes|Sin cambio de señales/timeframes por modalidad BTG|S04/S05|
|T33|Burn de A y, en otro caso, retiro de A/cuarto cobro; activar B durante OPEN_CYCLE_LONG y SHORT|Mismo owner Strategy completo antes/durante/después del primer reemplazo y al siguiente re-arm/OPEN; ninguna señal extra/omitida; B sin exposición/PnL/órdenes/reservas de A|S03–S05|
|T34|OPEN rechazado por Provider/Operation, target vacío, binding disabled y pausa entre cuentas con OPEN/CLOSE durante ella|Strategy normal avanza; cero entregas no rearma; management drena A; B sólo recibe señales posteriores, nunca backlog; dedup/config/rollover/seq intactos|S03–S05|
|T35|Referencia vs atajo: warmup/flat, frontera H4/5m y Open, orden creada dentro de minuto, K=0|Barras/OwnerState/señales/decisiones/economía/curvas iguales; ningún fill retroactivo ni causa omitida; reactivación en el siguiente paso original|S03–S05|
|T36|Referencia vs atajo: timer intraminuto, control y callback; fill instala protección, add→stop, cierre parcial|Mismo orden causal y estados/fills/economía; no saltar umbral ni extremo tras activación; clocks/marks/freshness/context versions iguales|S03–S05|
|T37|Censo13 archivos y benchmark V2; vela de amplitud creciente y streams/buffers fijos|Sin materialización O(K/filas); generador acotado; rows/K/procesados/omitidos, warmup/trading, tiempos/peakRSS/bytes registrados; gate previo al lote y reparación de cuello en S03|S03/S04|
|T38|Tres objetivos materializados en EVALUATION y FUNDED INITIAL/STEADY, días posteriores y B; caso sensible al objetivo MM|MM compartido consume1000/1500/2000, SL2000/chunk1500 inmutables; traza de plan/decisión y efectos reruneados, no simple cambio de etiqueta/export|S03–S05|

T33/T34 usan el harness runtime existente con mercado/Strategy vivos y la misma secuencia controlada de bindings, admisiones y causas de cuenta. Capturar OwnerState y traza semántica antes del retiro/burn, al activar B y tras el primer cierre/re-arm/OPEN posterior; incluir un rechazo y una pausa que atraviese varias5m/H4. La ausencia de destinatario no permite ocultar señales emitidas. Normalizar sólo identidades no semánticas con mapeo1:1; conservar secuencias, estado técnico, contrato, causalidad, configuración, precio/cantidad y razones. Para economics comparar contra la misma secuencia de cuentas/controles, no contra una BASIC sin lifecycle.

T35/T36 corren ambos paths con idénticos inputs/estado/config/fills donde corresponda y comparan en cada causa material, no sólo cash final. Incluir consumidor activo desde Open y consumidor que aparece dentro del minuto; inyectar timer que crea/activa orden y callback que instala protección. La activación debe deshabilitar el atajo antes del siguiente paso requerido. T37 registra por separado memoria del generador y peakRSS global; muestras pequeñas no prueban memoria total acotada de la aplicación. T38 debe observar el plan realmente seleccionado por GerardMM, no únicamente tres valores escritos en JSON.

MaxAdds>0 no demuestra scaling: T13/T14 exigen eventos/fills y rechazos. Tampoco exigir cuatro retiros en un tramo real arbitrario: E2E controlados prueban lifecycle; el resultado histórico, incluso0retiros, se informa como ocurrió.

### 13. Trabajo ejecutable sin fases adicionales

**S03 LOCAL, después de review Primary:** configuración común; perfiles BASIC/stages/campaña; V2 causal y selección por minuto; runner/caja sobre controles; exports y parity harness. Implementar T01–T27/T30–T31/T33–T38, continuidad por composición y path lazy con equivalencia; smokes13 y censo/benchmark V2 con gate previo a todo lote extenso. Corregir cualquier cuello demostrado en este mismo S03. Entregar commit, perfiles/digests, comparación V1, primer BASIC/CAMPAIGN real, pendientes de cobertura y comandos reproducibles. No egress real, D6, PROD, ETCD, permisos ni merges preventivos. No se crea aquí prompt de implementación: corresponde al Primary tras review.

**S04 LOCAL independiente:** crear E2E para romper continuidad tras reemplazo/rechazo/pausa, equivalencia del atajo/reactivación y parametrización MM, además de causalidad, fills/adds/cancel, doble gasto, payout anticipado, frontier, boundaries, roll y métricas. Conservar RED; distinguir bug, incumplimiento de diseño, cobertura e incertidumbre. CLOUD no sustituye esta ejecución.

**S05 LOCAL:** corregir findings sin cambiar señales/fórmulas silenciosamente; rerun ataques/regresiones; ambos modos reales extensos, reproducciones frescas y exports; búsqueda/sensibilidad sólo con cobertura/presupuesto. Informar también intento/horizonte integral y límites, sin sumar slices. Matriz final PASS/FAIL/NOT_RUN/BLOCKED con evidencia; Primary acepta, no implementer ni arquitecto.

Sin S06 ni otra plataforma. Falta de ticks adquiridos permite fixtures para ruta y REAL_TICK_COMPARISON_NOT_RUN_DATA_UNAVAILABLE; no bloquea OHLC. Si no existe cobertura continua3años, entregar ambos modos utilizables y resultados del alcance verificable, con integral PARTIAL/FAILED. No prometer reconstruir observaciones inexistentes.

### 14. Cierre y continuidad

Enmienda del mismo S02 entregada para revisión final Primary, sin freeze ni gate propio. **AGENTS-OS se trabaja directamente sobre master.** La instrucción anterior de crear rama documental queda corregida; `codex/btg-s02-design-cloud-20261006` se conserva sólo como referencia de lectura. No crear rama/PR, borrarla, mergearla ni cerrar PRs. Esto no cambia la política de ramas de Echo; no se modifica producto, infraestructura, D6/PROD/ETCD ni ACL.

Publicar únicamente este diseño y registro mínimo del delta sobre master actual. Antes de escribir, releer HEAD/destino y preservar intersecciones ajenas; update con blob SHA esperado si existe, create sin overwrite si sigue ausente. Un conflicto requiere relectura/reconciliación, nunca force-push. Una denegación de herramienta detiene esa persistencia: entregar archivo completo y declarar PERSISTENCE_PENDING, sin buscar otra ruta ni bloquear el diseño. Resultado efectivo de publicación/readback y SHA se informa en el handoff, no se presume aquí.

`agents-os-agent-run-register = SKIPPED_DOCS_ONLY`: inspección y reparación documental, sin producto ni pruebas físicas. Modelo solicitado Owner GPT-6 Astra, superficie CLOUD; `PRO_CHAT_POOL_DELTA=UNKNOWN`, sin incremento inferido. `PHYSICAL_TESTS=NOT_RUN`; benchmark/censo del corpus y gates LOCAL=NOT_RUN. Validación de Markdown y control del delta no equivalen a ejecutar Echo.

Cerrar este worker ONE-SHOT por delta: change_log consolidado y feedback breve sólo por fricción concreta; sin editar skills/normas, sin L0 porque no se recibió transcript completo ni L1 duplicado. Graphify/MCP/SSH no ejecutados desde CLOUD. La continuidad suficiente está en este diseño y el registro; no reconstruir D1–D6 ni abrir otro roadmap. Próximo paso único: revisión final Primary → S03, sin shot adicional.

## Fuentes

Referencias A: autoridades/documentos; resultados físicos atribuidos LOCAL. Referencias E: source leído, no tests ejecutados.

- [A1] Mandato Owner BTG-S02 de la sesión original del candidato, preservado como antecedente; la enmienda vigente es [A5]. Bootstrap, constitución, perfil público, continuidad interna, skills INDEX, technical-project-manager, Echo Futures y BTG-PLAN leídos desde `xKoRx/agents-os`; master de referencia `2e6c75e8f425be43fedbfe76d280dd92f38b76ed`.
- [A2] [BTG-S01-REAL-GERARD-RESULT](https://github.com/xKoRx/agents-os/blob/e4a177ebca60c95062fbc30bc8a97ceb3be31c04/main/10-projects/Echo%20Futures/artifacts/backtester-stage2-real/BTG-S01-REAL-GERARD-RESULT.md) y [FUNCTIONAL-BASELINE-PROFILE](https://github.com/xKoRx/agents-os/blob/e4a177ebca60c95062fbc30bc8a97ceb3be31c04/main/10-projects/Echo%20Futures/artifacts/backtester-stage2-real/BTG-S01-FUNCTIONAL-BASELINE-PROFILE.md).
- [A3] [BTG-S01-OWNER-S2-BARS-AUTHORITY](https://github.com/xKoRx/agents-os/blob/e4a177ebca60c95062fbc30bc8a97ceb3be31c04/main/10-projects/Echo%20Futures/artifacts/backtester-stage2-real/BTG-S01-OWNER-S2-BARS-AUTHORITY.md).
- [A4] [BTG-S01-REAL-GAP-FORENSICS](https://github.com/xKoRx/agents-os/blob/e4a177ebca60c95062fbc30bc8a97ceb3be31c04/main/10-projects/Echo%20Futures/artifacts/backtester-stage2-real/BTG-S01-REAL-GAP-FORENSICS.md).
- [A5] Owner, mandato “ECHO FUTURES — BTG-S02 — ENMIENDA ACOTADA DEL MANAGER: CONTINUIDAD, COSTO INTRABAR Y OBJETIVOS”, sesión2026-10-06; candidato base `00514fe65d0b4a06975096de17a3c2246d573c92`, F1–F3 y escritura directa master. [BTG-PLAN leído](https://github.com/xKoRx/agents-os/blob/fdff61691805608d2b84c5e0fc637ff433f0197c/main/10-projects/Echo%20Futures/artifacts/backtester-gerard-bankroll/BTG-PLAN.md); estados históricos no sustituyen este mandato.
- [E1] [s2.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/sdk/futures/strategies/s2/s2.go) y [s2_test.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/sdk/futures/strategies/s2/s2_test.go): eligibleTrend, onEntryBar y frontera temporal.
- [E2] [config/mm.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/sdk/futures/config/mm.go).
- [E3] [gerardmm/config.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/sdk/futures/gerardmm/config.go).
- [E4] [compose_account.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/backtester/compose_account.go), [runtime MM wrapper](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/core/internal/futuresruntime/mm.go) y runtime.go inspeccionado.
- [E5] [functional_profile.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/backtester/functional_profile.go).
- [E6] [ohlc_driver.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/backtester/ohlc_driver.go), [ohlc_market_context.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/backtester/ohlc_market_context.go), [venue OHLC](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/backtester/internal/simexecution/ohlc.go).
- [E7] [controls.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/backtester/controls.go), [spec.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/backtester/spec.go).
- [E8] [a57_controls_test.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/backtester/a57_controls_test.go).
- [E9] [driver.go](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/backtester/driver.go): fases, nextRoot, fireTimer, market/expiry.

- [E10] Source F1 leído en `77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626`: [runtime.Compose](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/core/internal/futuresruntime/runtime.go#L108-L190), [OwnerState/Engine](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/sdk/futures/strategy/engine.go#L13-L105), [FanoutState/Linearize](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/sdk/futures/strategy/fanout.go#L12-L175); [DecodeState/CycleActive](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/sdk/futures/strategies/s2/s2.go#L206-L252), [onEntryBar/Warmup/cycle](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/sdk/futures/strategies/s2/s2.go#L346-L465) y [composeAccount](https://github.com/xKoRx/echo/blob/77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626/v3/backtester/compose_account.go#L22-L202). Son pruebas de contrato source, no de ejecución física.

Orientación externa primaria heredada del candidato original (consulta allí atribuida a2026-10-06); no releída ni usada para modificar autoridades en esta enmienda:

- [NinjaTrader — Historical Fill Processing](https://ninjatrader.com/support/helpGuides/nt8/understanding_historical_fill_.htm): modelado histórico frente a granularidad; no equivalencia con Echo.
- [MetaQuotes — Testing Trading Strategies](https://www.mql5.com/en/docs/runtime/testing): distinguir ticks/recorridos generados y observados.
- [QuantConnect — Time Period Consolidators](https://www.quantconnect.com/docs/v2/writing-algorithms/consolidating-data/consolidator-types/time-period-consolidators): barras y fronteras; Echo mantiene Calendar/SessionGrid.
- [QuantConnect — Live Trading / Reconciliation](https://www.quantconnect.com/docs/v2/writing-algorithms/live-trading/reconciliation): reconciliación y diferencias históricas/LIVE; paridad de dominio no obliga igualdad de fills/PnL.
