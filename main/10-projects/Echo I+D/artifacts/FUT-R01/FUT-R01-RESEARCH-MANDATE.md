---
type: prompt
schema_version: 1
status: active
area: "[[Trading]]"
target: "Workers externos Deep Research y revisor independiente; consolida el submanager Futures"
prompt_version: 4
inputs:
  - "Cápsula Owner: campañas prop NQ, capital finito y Strategy/MM separados"
  - "Adjuntos efectivamente suministrados y fuentes primarias externas"
outputs:
  - "DR-01 matemática de campañas y MM"
  - "DR-02 contratos y costes actuales"
  - "DR-03 mecanismos y cobertura NQ"
  - "DR-04 indicadores, reglas y validación"
  - "RV-01 revisión independiente y consolidación posterior del submanager"
project: "[[Echo I+D — Futures]]"
aliases:
  - "FUT-R01 — Prompt maestro de investigación"
  - "Frente 2 — informe exploratorio y paquete Deep Research"
related:
  - "[[Echo — I+D de Estrategias]]"
  - "[[Echo I+D — Cobertura Futures]]"
  - "[[Echo I+D — Mapa de capacidades]]"
tags:
  - kind/prompt
  - area/trading
  - project/echo-rnd
created: "2026-10-27"
updated: "2026-10-28"
---

# FUT-R01 — Frente 2: campañas prop, informe exploratorio y mandatos Deep Research

## Propósito

**Versión 4 del mandato. Estado actualizado 2026-10-28: DR-01 RECIBIDO, CON HALLAZGOS MATERIALES; DR-02/03/04 y RV-01 NO EJECUTADOS.** Sustituye el prompt monolítico v3 para nuevos encargos externos. El Owner solicita persistir el informe anterior y recibir mandatos ONE-SHOT separados; el submanager consolida los retornos después de recibirlos. Esta actualización no ejecuta investigación autónoma ni promete trabajo en background.

**Corrección Owner vigente, 28-10-2026:** el objetivo es economía de campañas prop, no rentabilidad convencional de una cuenta propia. No imponer esperanza positiva por trade como requisito universal. Estudiar riesgo alto y resolución rápida de evaluaciones con matemática, contratos y posterior simulación autorizada. La referencia USD 400/funded es un supuesto por contrastar, no un coste agregado verificado. Strategy conserva tres bloques y MM sigue separado. Capital Futures USD 4.000 sin nuevos aportes; Forex no respalda este presupuesto.

No se seleccionan aún estrategias, firmas, reservas o políticas de riesgo. El informe inicial conserva valor como guía y no como certificación; las afirmaciones comerciales se deben revalidar. La historia de v3 permanece en Git. El frente 1 y sus autoridades no cambian.

## Contrato de entrada

Cada DR de la sección Prompt es autocontenido: copiar sólo el encargo correspondiente a una sesión nueva con navegación de investigación. Adjuntar únicamente fuentes realmente disponibles y relevantes. No distribuir por defecto todo este documento a todos los workers. No presuponer acceso al vault, Hefesto, cuentas, otros chats ni retornos de otros DR.

El manager conserva recuperación interna, lectura de autoridades G0–G5, integración de resultados y decisión de producto. El Owner conserva decisiones materiales, gasto y operación. En la plataforma actual no se acredita despacho de agentes externos; estos son mandatos preparados para ejecutarlos en sesiones separadas.

## Contrato de salida

| Encargo | Pregunta propia | Estado |
|---|---|---|
| DR-01 | Cuándo riesgo alto/resolución rápida mejora campaña y caja | RECEIVED_WITH_MATERIAL_FINDINGS; ver [[Echo Futures — DR-01 matemática de campañas prop]] |
| DR-02 | Qué contratos/rutas/costes reales permiten la campaña | READY_TO_DISPATCH; NOT_EXECUTED |
| DR-03 | Qué mecanismos NQ aportan propiedades/cobertura investigables | READY_TO_DISPATCH; NOT_EXECUTED |
| DR-04 | Cómo definir reglas y validar señal/MM/campaña sin sobreajuste | READY_TO_DISPATCH; NOT_EXECUTED |
| RV-01 | Si los cuatro retornos son coherentes y suficientes | WAITING_FOR_DR_RETURNS; NOT_EXECUTED |

Primero recomendado: **DR-01**. DR-02/03/04 pueden investigar en paralelo porque sus mandatos aceptan parámetros desconocidos y explicitan interfaces. No necesitan inventar resultados de otro worker. RV-01 se ejecuta sólo cuando se adjunten los retornos; no es una quinta investigación amplia.

Consolidación del submanager: registrar claims y fuentes; reconciliar supuestos/reglas/denominadores; separar dictámenes matemáticos, evidencia de mercado, elegibilidad comercial y evidencia propia; revisar contradicciones; presentar primer experimento y alternativa; decidir con el Owner sin votación entre IAs. Ningún retorno mueve G0–G5 por sí solo. Una autorrevisión nunca se etiqueta como revisión independiente.

## Contenido

El informe siguiente es una edición documental del antecedente completo por temas, con corrección económica explícita y trazabilidad limitada. Sus tablas comerciales no son RuleSets ejecutables.

# Echo Futures — Frente 2: informe exploratorio y rectificación económica

Fecha: 28-10-2026. Autoridad: instrucciones del Owner en esta conversación. Estado: ANTECEDENTE EXPLORATORIO, NO CERTIFICACIÓN DE INVESTIGACIÓN, COMERCIO NI EJECUCIÓN. Esta es una edición documental del informe anterior, con sus hipótesis, tablas, cálculos, referencias y limitaciones; no una transcripción literal. La corrección siguiente prevalece sobre sus recomendaciones previas.

## 1. Corrección del marco: campañas prop, no una cuenta propia convencional

El Owner aclaró que el objetivo no es maximizar la rentabilidad de una cuenta propia ni preservar cada evaluación. Es explotar de forma investigable la asimetría entre los costes reales de adquirir oportunidades prop y los retiros posibles. Las evaluaciones pueden pasarse o perderse rápidamente con políticas agresivas. Esa agresividad es parte del espacio de investigación, no un defecto que deba eliminarse por doctrina.

No se exige esperanza positiva por trade, profit factor mayor que uno, Sharpe positivo ni una curva ascendente como condición universal de admisión. Son descriptores de la señal y pueden importar al resultado; no sustituyen la valoración del ciclo completo. Una señal no positiva por trade no se descarta automáticamente, pero tampoco se demuestra útil por decir que la funded tiene un potencial grande.

La unidad económica de decisión es la campaña: compra → pase/pérdida → activación → funded → elegibilidad/solicitud/aprobación → dinero recibido → cobros siguientes o cierre/reemplazo. El PnL simulado y las barreras pertenecen al proceso; los desembolsos y cobros reales determinan la caja del Owner.

La referencia del Owner de aproximadamente USD 400 por funded es un supuesto para contrastar. Debe distinguirse precio de compra, coste de la trayectoria que pasó y coste agregado de adquisición incluyendo intentos fallidos, resets, renovaciones y activación. No es un precio universal ni una media demostrada.

Resolver rápido tampoco sustituye el objetivo económico: hay que estudiar el trade-off entre tiempo, importe/probabilidad de cobro, coste por intento, financiación del siguiente intento y agotamiento de USD 4.000. La agresividad óptima puede diferir entre evaluación y funded; no se presupone ni arriesgar máximo siempre ni conservar la funded indefinidamente.

### Correcciones explícitas al informe anterior

| Criterio anterior | Estado y sustitución |
|---|---|
| Exigir expectativa neta positiva por trade antes de admitir una Strategy | SUPERSEDED como filtro universal. Evaluar la contribución de la combinación señal × MM × RuleSet a campaña y caja. |
| Refutar toda candidata si su expectativa por trade no es positiva | SUPERSEDED como descarte global. Puede refutar una hipótesis que específicamente prometía esa expectativa, no demostrar inutilidad prop universal. |
| Perfil conservador o supervivencia prolongada de cuenta como referencia preferida | No aceptado. Riesgo alto y resolución rápida deben investigarse seriamente bajo restricciones y capital finito. |
| Reservas del 50%, 60% y 75% | Ejemplos anteriores no aceptados. No fijan presupuesto ni reserva; su utilidad deberá salir del modelo de caja y decisión Owner. |
| Dar prioridad definitiva a bandas intradía y ruptura fallida | Eran propuestas exploratorias, no selección aceptada. DR-03 debe contrastar alternativas, evidencia y cobertura. |
| MFFU/Lucid como elegibles y Topstep como descarte comercial establecido | No certificado. DR-02 revalida programas, fechas, rutas de automatización y live sin heredar conclusiones. |
| Informe presentado como investigación completada con fuentes oficiales vigentes verificadas | Se conserva como guía exploratoria. Esta entrega no acredita trazabilidad suficiente para certificar esos claims comerciales. |
| Lectura íntegra de PDFs y revisión independiente de varios agentes | No acreditadas por esta entrega. No se declara que hayan ocurrido. Una autorrevisión no es una revisión independiente. |

## 2. Cápsula vigente y fronteras

NQ es el único instrumento ejecutable autorizado; MNQ y otros instrumentos no están autorizados. Capital inicial Futures USD 4.000 sin aportes previstos. Forex conserva aproximadamente USD 2.000 separados, no transferibles por inferencia.

Meta táctica al 31-12-2026: cinco estrategias challenge y cinco funded produciendo retiros en al menos dos firmas. Pueden coincidir, diferir o mezclarse. No está demostrada la factibilidad. Variantes, timeframes y MM no suman automáticamente estrategias independientes.

Aspiraciones: al menos una cuenta con cobro por diez evaluaciones compradas; pase 1/3 y cobro de 1/3–1/2 de las funded activadas. No son probabilidades estimadas. Primer retiro objetivo USD 3.000: bruto previo al split y neto recibido se estudian por separado, con splits 90% y 80%. Ninguna prop, programa, plataforma o reserva está elegida.

Inventario conocido: TG/TradesGerard; FBC/NY First Candle, que sigue dirección de una primera vela cerrada; ORB, que rompe un rango; MR01–MR10, de las cuales sólo se conoce aquí que MR08 combina recuperación local con tendencia H1. No inferir otras reglas por el nombre. R03 es evidencia histórica simulada y confirmación temporal retrospectiva, no OOS virgen, producción o retiros. ClutiFX y E2T/GAU50 siguen históricos; no se reabren ni convierten en elección actual.

OHLCV 1m es baseline mencionado, no cobertura física certificada. Frente 1 gestiona Backtester–runtime. G0–G5 conservan sus autoridades: no se redefinen ni se declaran superados. No código de producto, campañas, pruebas físicas, compras, operaciones ni cierre formal de sesión en esta entrega.

## 3. Alcance y calidad del informe inicial

El informe previo separaba A) reglas/indicadores/métricas, B) mecanismos/cobertura y C) props/economía. No hubo ejecuciones acreditadas de workers independientes de Deep Research. La separación analítica no equivale a tres investigaciones autónomas.

El retorno anterior contenía marcadores de citas sin un registro reproducible adjunto a esta entrega. Se conservan los enlaces explícitos como semillas, no como confirmación de que cada página fue accesible, leída o vigente. Las cifras comerciales siguientes están en cuarentena hasta DR-02. No se certifica lectura completa de los PDFs. No se atribuyen resultados ajenos a Echo.

Jerarquía propuesta: fuente primaria con metodología/datos accesibles; abstract declarado como lectura parcial; preprint/working paper con estatus claro; libro/curso como descripción de mecanismos; documentación oficial por programa/fase para contratos. Ningún nivel equivale a evidencia propia NQ.

### Registro de literatura del informe previo

| Fuente | Alcance mencionado | Uso y limitación |
|---|---|---|
| Zarattini, Aziz y Barbon, Beat the Market, SSRN 4824172; adjunto con versión 03-02-2025 | SPY y extensión declarada a futuros | Semilla de bandas dependientes de la hora, salidas y sizing. No certifica Echo. |
| Gao et al., Market Intraday Momentum, 2018 | ETFs, principalmente S&P 500 | Continuación entre ventanas del día. El informe declaró lectura de abstract. |
| Baltussen et al., Hedging Demand and Market Intraday Momentum, 2021 | Más de 60 futuros según el informe | Cobertura gamma y continuación/reversión. Lectura declarada parcial. |
| Rosa, Understanding Intraday Momentum Strategies, 2022 | Incluye índices futuros | Contraevidencia de deterioro OOS de una señal relacionada; no refuta automáticamente toda implementación. |
| Yu, Rentzler y Wolf, Nasdaq-100 Index Futures, 2005 | Futuros Nasdaq-100 | Continuación y reversión condicionadas según abstract referido. |
| Grant, Wolf y Yu, Intraday Price Reversals, 2005 | Futuros de índices estadounidenses | Costes pueden reducir la utilidad económica observada de reversión. |
| Kakushadze y Serur, 151 Estrategias de Trading, SSRN 3402665 | Múltiples activos | Catálogo descriptivo, no prueba de rentabilidad de sus recetas. |
| LÓGICA PRICE ACTION.txt, VTALGO, 2017 | Predicados de velas | Normalizar precedencia AND/OR y unidades; no demuestra utilidad económica. |
| Almazov, Una Teoría Fractal | Principalmente Forex | No trasladar afirmaciones visuales a NQ ni tratarlas como evidencia predictiva. |
| Kaufman, Nuevos sistemas y métodos de trading, PDF escaneado adjunto | Sistemas y métodos | Extracción textual insuficiente en el contexto suministrado; no atribuir reglas específicas no verificadas. |

El informe citó para SPY un Sharpe 0,61 de la versión base, 1,24 tras modificar salidas con banda/VWAP y 1,33 al añadir sizing dinámico; DD de 12% a 25% entre las últimas versiones. Esas cifras describen configuraciones ajenas diferentes: no prueban un setup aislado ni una campaña prop. La FAQ del adjunto incluye una fila Nasdaq en una extensión a futuros, que tampoco certifica NQ de Echo. Los investigadores deben verificar versión, período, costes y metodología antes de reutilizar números.

Una referencia del informe a un preprint MNQ de 2026 carece aquí de identificación/URL recuperable suficiente. Se conserva como incidencia de trazabilidad, NO como evidencia ni refutación de NQ.

## 4. Anatomía simple, medidas y unidades

Strategy: SETUP, FILTRO opcional, OBJETIVO/RIESGO o RR técnico. Identidad y versión acompañan. MM es otra entidad por prop/programa/etapa: contratos, riesgo monetario, bloqueos y controles. Evidencia, fuentes, validación, cuenta/cartera y arquitectura no son bloques adicionales de Strategy.

Referencia de especificaciones para verificar en CME: NQ USD 20 por punto; tick 0,25 puntos = USD 5. Ejemplos dimensionales para 1 NQ: 5 puntos/20 ticks = USD 100; 10/40 = USD 200; 15/60 = USD 300; 25/100 = USD 500 antes de costes. En un límite ilustrativo USD 2.000, USD 500 equivalen a 25%; eso describe la exposición, no la descalifica por ser alta.

Si una política de MM no admite 1 NQ, puede vetar la ejecución. No se reduce silenciosamente el stop técnico ni se cambia a MNQ. El experimento puede comparar otras políticas autorizables, no fingir contratos fraccionarios.

| Función | Medidas candidatas | Datos/disponibilidad | Pregunta y limitación |
|---|---|---|---|
| Dirección | Retorno, EMA, pendiente | Cierres completos | Dirección persistente o ruido; lag y reversals. |
| Intensidad | ROC, pendiente/ATR | Cierres y ATR causales | Magnitud del impulso; posible redundancia con EMA. |
| Extensión | Distancia a apertura, máximo previo, VWAP | Referencia ya conocida | Desplazamiento relativo; extensión no implica reversión. |
| Rango | High/Low, NR4/NR7, compresión | Ventanas completas | Amplitud previa; máximo intrabar no implica fill. |
| Volatilidad | ATR, desviación de retornos | OHLC/cierres completos | Escala de variación, no dirección. |
| Actividad | Volumen, RVOL por slot | Volumen cerrado e historia del mismo horario | Participación anormal; no revela agresor. |
| Referencia | VWAP de sesión | Precio×volumen desde un ancla | Coste medio; con OHLCV es aproximación respecto de datos transaccionales. |
| Tiempo | Hora NY, apertura/cierre, calendario | Calendario causal con DST | Contexto; no crea edge por sí mismo. |
| Microestructura | Delta agresor, imbalance, profundidad | Trades clasificados/quotes/L2 | No reconstruible causalmente desde OHLCV M1. |

No agregar RSI/MACD/ADX/Bollinger/EMA juntos como ritual. Comparar baseline, adición de un filtro y ablación, conservando universo de oportunidades. ΔE por trade es un descriptor útil, pero también se deben medir frecuencia perdida, distribución/tiempo de trayectorias y efecto sobre campaña. Un mejor win rate no prueba mejora de cobros, y menor PnL convencional no demuestra por sí solo inutilidad prop.

## 5. Fichas ilustrativas preservadas del informe

Estas fichas NO son estrategias aceptadas ni especificaciones certificadas. Los parámetros fueron ejemplos iniciales, no óptimos. DR-03/DR-04 pueden refutarlas o reemplazarlas. Debe cerrarse cualquier ambigüedad de warm-up, ATR, cruce, sesión, rollover y ejecución antes de implementar.

### EF-NB-01 v0.1 — continuación por banda temporal

**SETUP:** M5 NQ sobre RTH Nueva York 09:30–16:00. Para cada horario t, promedio de 14 sesiones previas del valor absoluto del retorno apertura→t, r̄_t. U_t=max(apertura RTH actual, cierre RTH previo)×(1+r̄_t); L_t=min(apertura RTH actual, cierre RTH previo)×(1−r̄_t). En observaciones de cierres 10:00, 10:30, …, 15:00, LONG al cruce de dentro hacia encima de U; SHORT simétrico bajo L. Primera señal, máximo una entrada por sesión, ejecución posterior a la confirmación.

**FILTRO:** ninguno en v0.1. Variante ilustrativa v0.2: RVOL M5 del slot ≥1,2 frente a media de las 20 sesiones anteriores.

**OBJETIVO/RIESGO:** stop inicial 1 ATR(14) M5 cerrado, redondeado hacia arriba al tick; objetivo 1,5R. MM determina contratos y salidas reglamentarias. Ejemplo dimensional, NO ATR actual: ATR 8 puntos → riesgo USD 160/NQ, objetivo 12 puntos/USD 240, antes de costes.

Las reglas de Zarattini no son estas reglas: el original usa controles semihorarios y salidas de banda/VWAP. Su rendimiento no se hereda al cambiar stop, target, universo, sizing o instrumento.

### EF-FBR-01 v0.1 — ruptura fallida del extremo previo

**SETUP:** H/L de RTH anterior. Entre 10:00 y 15:30 ET, barra M5 cerrada que negoció encima de H_previo+1 tick y cierra debajo de H_previo−1 tick genera SHORT; regla simétrica LONG en L_previo. Primera señal válida por sesión; entrada después del cierre que confirma.

**FILTRO:** ninguno en v0.1. Variante v0.2: volumen de barra de rechazo ≤media de su mismo slot en 20 sesiones anteriores; hipótesis de participación débil, no condición acreditada.

**OBJETIVO/RIESGO:** SHORT stop máximo de barra+1 tick; LONG stop mínimo−1 tick; objetivo 1,25R desde fill real. MM puede vetar exposición. Ejemplo: stop 10 puntos = USD 200/NQ; target 12,5 puntos = USD 250 brutos. Gaps entre señal y fill pueden cambiar geometría; no inventar una ejecución favorable.

## 6. Métricas y RR: conservar lo descriptivo, corregir la decisión

| Métrica | Fórmula/denominador | Datos y decisión |
|---|---|---|
| Frecuencia | Señales/ejecuciones por sesiones elegibles | Oportunidades y calendario; actividad y exposición. |
| Sequía | Sesiones consecutivas sin trades; mediana/p95/máximo | Riesgo de plazos/inactividad y tiempo de campaña. |
| Expectativa neta por trade | ΣPnL_neto/N_trades | Descriptor de señal, NO gate universal. |
| Productividad diaria | ΣPnL_neto/D_sesiones, incluyendo ceros | Progreso bajo política fija; no sustituye cash. |
| Payoff | Media ganancia / magnitud media pérdida, junto a win rate | Diferencia entre RR planeado y realizado. |
| Colas | Cuantil 5%, pérdida media de cola y peor día | Exposición a fallos conjuntos y barreras. |
| DD | Caída desde pico, EOD e intradía separados | Compatibilidad con el suelo real y actualización. |
| Recuperación | Tiempo a recuperar pico, censurando no recuperados | Descriptor, no obligación de conservar cada cuenta. |
| Robustez | Variación entre épocas, parámetros vecinos y costes | Sensibilidad y dependencia de resultados extremos. |
| Filtro | Cambio de distribución, frecuencia, PnL y resultados de campaña | Información incremental frente a pérdida de oportunidades. |

PnL_neto de un trade = 20×contratos×signo×(salida−entrada)−costes, sujeto a verificar especificación y modelo de costes. Métricas de campaña obligatorias adicionales: coste por cuenta activada/pagadora; pase/pérdida/pendientes; tiempos a barrera y cobro; cantidades netas recibidas; máximo déficit de caja; capacidad de financiar próximos intentos y dependencia entre cuentas.

RR planeado no equivale a payoff realizado. Stop, target, cierre reglamentario y salida de MM deben identificarse por separado. Cambiar geometría modifica duración, acierto, secuencias y fricciones: no multiplicar una curva por el RR nuevo. Si stop y target caen dentro de una misma M1, el orden es desconocido sin más datos. Lo mismo puede impedir reconstruir un trailing intradía dependiente del pico de equity; usar límites/modelos explícitos, no fills “observados”.

## 7. Mecanismos y cobertura provisional

| Mecanismo | Medición/regla | Evidencia propuesta y límite | Prioridad anterior, no aceptada |
|---|---|---|---|
| Persistencia de presión | Bandas temporales, posible RVOL | Momentum en ETFs/futuros; transferencia NQ y campaign pendiente | Alta |
| Continuación tras pullback | Tendencia causal+retroceso+recuperación | Plausibilidad; solapamiento con TG/MR08 desconocido | Media-baja |
| Ruptura aceptada | Cierre fuera de rango | ORB/continuación; probablemente ya cubierta en parte | Baja hasta mapear |
| Ruptura fallida | Cruce y retorno al rango | Reversión de futuros; costes y MR pendientes | Alta alternativa |
| Reversión de extensión | Distancia a apertura/VWAP+recuperación | Presión transitoria; riesgo de confundir bid-ask bounce | Media |
| Estacionalidad | Ventanas | Condiciona mecanismos; no familia automáticamente | Filtro/contexto |
| Eventos macro | Reacción postanuncio | Datos, contratos y fricciones adicionales | Diferida |
| Intermercado | Relaciones usadas como contexto | Datos/autorización y hedge entre firmas | Diferida |
| Microestructura | Delta/imbalance/absorción | OHLCV M1 insuficiente | No habilitada |

| Trabajo | Cobertura probable | Solapamiento/desconocido |
|---|---|---|
| FBC | Dirección de primera vela | Momentum/apertura; no failed breakout. |
| ORB | Ruptura de rango | Aceptación y continuación; FBR no certificada como brecha. |
| MR01–MR10 | Reglas completas desconocidas | No afirmar cobertura por prefijo MR. |
| MR08 | Recuperación local con tendencia H1 | Puede solapar pullback/FBR según reglas. |
| TG | Desconocida en cápsula | Recuperar reglas/señales; no inferir. |
| R03 | Evidencia retrospectiva simulada | No independencia, producción, payout ni OOS virgen. |

Una celda vacía no obliga a desarrollarla. Priorizar por valor de información, reutilización, aporte de trayectorias diferentes y coste de refutación. No poblar el catálogo con clones de ORB/EMA/RR sólo para alcanzar cinco más cinco.

Contraevidencia relevante: Gao y Rosa investigan implementaciones relacionadas pero no idénticas; deterioro de una no refuta todas. Una explicación de cobertura gamma en Baltussen no autoriza tratar RSI como inventario gamma observado. Reversiones brutas pueden desaparecer con costes. Cada hipótesis debe declarar qué evidencia transferir y qué falta probar, tanto a NQ como a una campaña.

## 8. Tabla comercial del informe anterior — NO VERIFICADA

Todos los campos de esta sección son afirmaciones preservadas del informe previo, no condiciones vigentes certificadas. DR-02 debe comprobar cada combinación, fecha y fuente. No usar estos números para comprar, dimensionar, bloquear definitivamente una firma ni construir un RuleSet ejecutable.

| Firma/programa/tamaño referido | Evaluación afirmada | Funded/payout afirmado | Precio afirmado |
|---|---|---|---|
| MFFU Rapid EOD 50K | Target 3.000; MLL 2.000 EOD; consistencia 30%; 4 días | EOD; sin consistencia/DLL; buffer 2.100; 90%; mínimo 500; sin cap | 135 promo / 225 lista; único; activación cero |
| LucidFlex 50K | Target 3.000; MLL 2.000; consistencia 40% o add-on50%; DLL opcional | EOD; sin consistencia/buffer; 5 días ≥150; 90%; payout50% con cap2.000 | Único; sin activación; precio exacto no recuperado |
| Tradeify Select 50K→Flex | Target3.000; MLL2.000 EOD; consistencia40%; 3 días; sin DLL | EOD; sin consistencia/DLL; 5 días ≥150; 90%; 50% con cap2.500 para cohortes nuevas | 165; reset109; sin activación |
| Topstep Combine50K→XFA | Target3.000; MLL2.000 EOD; mejor día55% objetivo | Standard: 5 días ≥150,90%,50% saldo,cap5.000; Consistency:3 días,40%,cap6.000 | 49/mes+149 activación o95/mes sin activación; API aparte |

Configuración de Lucid con DLL/add-ons y sus precios no deben cruzarse entre filas. Las presuntas actualizaciones Topstep de septiembre/octubre y Tradeify desde septiembre de 2026 requieren prueba oficial específica y versión de cohorte.

### Restricciones técnicas/comerciales afirmadas previamente

| Dimensión | MFFU | Lucid | Tradeify | Topstep |
|---|---|---|---|---|
| Bots | Permitidos con exclusiones SIM/HFT | Bots y copiers permitidos | Permitidos con revisión | Permitidos por TopstepX API |
| API directa para cuentas prop | No confirmada | No confirmada | API genérica Tradovate no habilitaría prop/eval | Disponible |
| Órdenes remotas | No confirmado | No confirmado | No confirmado | Informe afirmó prohibición VPS/VPN/servidor |
| Automatización Live | En principio permitida, sin ruta certificada | Pendiente | Pendiente | Informe afirmó API no disponible |
| Noticias | Eval sí; Rapid EOD funded no tier1 | Permitidas Flex | Pendiente | Informe afirmó veto ±5min tier1 |
| Hedge/copia entre firmas | Pendiente | Informe afirmó prohibición hedge interfirmas | Informe afirmó prohibición mismo bot en varias firmas | Hedge entre cuentas prohibido según informe |
| Horarios | Pendiente perfil | Pendiente corte | Pendiente corte | Informe afirmó flat15:10CT |
| Migración | Consolidación Rapid posible | Cierre de otras SIM posible | Elite Live distinto | Contrato distinto |

Estas afirmaciones no prueban compatibilidad o incompatibilidad del runtime de Echo. Bots=yes no certifica autenticación/origen/hosting. API directa no disponible tampoco prueba que un bridge permitido sea imposible. No construir un descarte definitivo con un claim pendiente.

Comisiones NQ round trip citadas: MFFU4,68; Lucid3,50 (1,75/lado); Tradeify5,76; Topstep pendiente modalidad. Todo por revalidar, incluida composición de fees. Ejemplo condicional: stop10p×20=200, más4,68 y dos ticks de slippage total10, da214,68. Es un escenario algebraico, no un fill esperado ni cotización vigente.

El informe afirmó que Chile no figuraba en listas restringidas de MFFU/Lucid/Tradeify. No se certifica esa afirmación ni el KYC del titular. Residencia, nacionalidad, pagos y elegibilidad Live requieren comprobación independiente.

## 9. Caja, embudo y primer retiro

| Objetivo | Split90% | Split80% |
|---|---|---|
| Payout bruto3.000 | Neto del split2.700 | Neto del split2.400 |
| Recibir3.000 netos del split | Bruto3.333,34, redondeado a centavos | Bruto3.750 |

Esto no incluye cargos de transferencia/cambio/impuestos ni confirma que la firma permita ese primer pago.

| Restricción preservada del informe, por verificar | Consecuencia algebraica condicionada |
|---|---|
| MFFU Rapid EOD50K sin cap y buffer2.100 | Retiro grande potencial; conservar2.100 después de sacar3.333,34 exigiría5.433,34 de beneficio. Conservar ese buffer completo es supuesto prudencial del ejemplo, no obligación certificada. |
| LucidFlex50K cap2.000,90% | Máximo1.800 netos del split por pago; no primer neto3.000. |
| LucidFlex150K cap3.000,90% | Máximo2.700 netos del split. |
| Tradeify SelectFlex50K cap2.500,90% | Máximo2.250 netos. |
| Tradeify SelectFlex100K cap3.500 y50% | Bruto3.333,34 necesitaría al menos6.666,68 de beneficio elegible si esa base del50% fuese correcta. |
| Topstep XFA Standard50K cap5.000 y50% | Mismo umbral6.666,68 para bruto3.333,34 bajo esa base; además días/restricciones. Suelo postretiro0 fue afirmado, no verificado aquí. |

Caja disponible B_t = 4.000 − desembolsos externos acumulados + retiros netos efectivamente recibidos. El nominal funded y PnL no cobrado no son caja. No descontar otra vez comisiones ya descontadas del beneficio que financia el payout. Distinguir coste de una fase de coste completo y de capacidad de financiar el siguiente lote antes del primer cobro.

Cohortes: compras nuevas, resets y renovaciones identificados; cuentas evaluando, pasadas, fallidas, activadas y esperando cobro no desaparecen del denominador. Campos de investigación sugeridos: fecha compra; Provider/Program/tamaño/RuleSet; costes; estado evaluación; pase; funded; payout solicitado/aprobado/recibido; caja neta. Esto no ordena modificar código o DB.

Ejemplos de desembolso del informe, condicionados a precios sin verificar: diez MFFU a135=1.350; a225=2.250; diez Tradeify a165=1.650; diez Topstep Standard un mes a49=490; activar tres a149=447 adicionales. No incluyen costes faltantes ni prometen éxito. API Topstep29/mes y supuesto descuento50% aparecieron en el informe, no se certifican. La mención Tradeify sobre clasificación de datos no profesionales/cargos adicionales también requiere verificación.

Cadena de objetivos: q=P(pase)×P(activación|pase)×P(cobro|activación), usando definiciones y horizonte compatibles. No requiere independencia entre etapas. Con activación de todos los pases, objetivos1/3×1/3=1/9 y1/3×1/2=1/6 son aritmética aspiracional, no estimaciones.

Si por hipótesis q=0,1 y cobro neto medio W=3.000, qW=300 por evaluación es sólo ingreso medio hipotético, no autosostenimiento: faltan costes, tiempo, censura, dependencia y acceso al próximo intento. La referencia400/funded debe analizarse en DR-01/02 con todos los fallos previos, no extrapolando sólo casos que pasaron.

Reservas50/60/75% del informe significaban2.000/2.400/3.000, pero ninguna está aprobada ni recomendada por defecto tras la corrección. Compras escalonadas, WIP y paradas deben surgir del modelo de caja y preferencias Owner, no de un reflejo de “trading conservador”.

Condiciones a estudiar, no políticas operativas nuevas: bloqueo contractual/técnico, incoherencia entre riesgos y modelo de ejecución, gasto agregado incompatible con caja/horizonte elegido y dependencia de supuestos refutados. No convertir pérdida frecuente de evaluaciones en fracaso por sí sola: puede pertenecer a la política ensayada.

## 10. Dos hipótesis anteriores y sus ocho puntos

### H1 — bandas de desequilibrio intradía

1. Hipótesis original: superar una banda temporal de variación normal permitiría continuación con expectativa positiva bajo stop1ATR/target1,5R. Eso es una hipótesis particular a contrastar, no requisito universal de campaña. La contribución a distribución/tiempo de barreras requiere análisis separado.
2. Mecanismo: presión persistente, reacción incompleta o cobertura que amplifica dirección; explicación propuesta, no identificación causal con OHLCV.
3. Evidencia: Zarattini/Gao/Baltussen; contraevidencia Rosa sobre otra señal relacionada. No evidencia propia Echo NQ.
4. Datos: NQ M1, RTH completa,14 sesiones previas por slot,20 para variante RVOL, calendario/roll/versiones. Disponibilidad no certificada.
5. Ejecución: entrada después de cierreM5, costes y slippage; stop/target y trailing pueden no resolverse dentro deM1.
6. Controles: baseline sin filtro, RVOL y ablación, universo temporal compartido; refutar mecanismo o utilidad según hipótesis predeclarada. Rentabilidad por trade≤0 no es rechazo económico global automático.
7. Coste: lógica simple/media, series por horario y auditoría de datos. Sin horas, throughput o coste físico inventados.
8. Cobertura: posible diferencia frente a ORB/FBC por referencia temporal, independencia pendiente de señales reales TG/ORB/FBC/MR.

Primer experimento sugerido originalmente: congelar v0.1 y comparar un solo filtro/ablación, sin buscar retrospectivamente el mejor parámetro. Frecuencia insuficiente puede hacer inviable un horizonte particular, no declarar universalmente inviable la señal. Prioridad final pendiente de los cuatro DR.

### H2 — ruptura fallida de extremo RTH previo

1. Hipótesis: barrer extremo previo y cerrar dentro puede cambiar la distribución del movimiento siguiente de manera útil para una campaña. La versión anterior lo formuló como reversión rentable tras costes; esa propiedad puede estudiarse sin imponerla a todo el programa.
2. Mecanismo: presión transitoria y falta de aceptación; traders de ruptura posicionados adversamente. No afirmar absorción observada sin datos adecuados.
3. Evidencia: Yu/Rentzler/Wolf y Grant/Wolf/Yu; ninguna valida esta regla exacta, y los costes pueden anular un efecto bruto.
4. Datos: OHLCV NQ con extremos RTH previos, M5 cerradas, calendario y rollover causales.
5. Ejecución: confirmación antes de entrada, stop fuera del rechazo, target1,25R, gap y ambigüedadM1 explícitos.
6. Control: sin filtro, RVOL bajo y ablación; ruptura aceptada de la misma referencia/universo como contraste, sin seleccionar luego sólo días favorables. Refutador estadístico/económico declarado antes del test.
7. Coste: lógica simple; validación de extremos y posible adquisición de datos finos no cuantificada.
8. Cobertura: podría complementar pérdidas breakout, pero MR01–MR10/MR08 pueden ya capturarlo. No implementar como familia nueva sin revisar equivalencia.

La coincidencia con MR no es automáticamente inutilidad: podría justificar variante o filtro, pero no diversidad nueva. Comparar señales congeladas y MM distintos sin alterar la señal silenciosamente.

## 11. MM y cartera

Propuesta algebraica de máximo por una política con presupuesto monetario R: q_max=floor[R/(20×distancia_stop+coste_RT+slippage_modelado)], sujeto a límites de contratos, suelo, otras posiciones y reglas. R es parámetro de política, no porcentaje aprobado. Un slippage medio no es garantía de límite de pérdida.

El informe ilustró riesgos5%,7,5% y10% de MLL inicial2.000 (100/150/200). No son asignaciones recomendadas ni una frontera que prohíba políticas más agresivas. El modelo deberá comparar distancias a target/suelo y caja real, sin confundir MLL con bankroll pagado.

| Medida de cartera | Definición útil |
|---|---|
| Señales | Intersección/unión de eventos con tolerancia temporal explícita. |
| Posiciones | Tiempo simultáneo expuesto / tiempo total expuesto; especificar universo. |
| Dirección | Tiempo con exposición NQ del mismo signo y magnitud conjunta. |
| Pérdidas conjuntas | Días con pérdidas de ambas / días comparables en que operaron, más versión sobre todo calendario. |
| DD simultáneo | Sesiones en drawdown de ambas / sesiones evaluables. |
| Colas | Peores pérdidas conjuntas y contribuciones, no sólo correlación media. |
| Sequía conjunta | Tiempo sin oportunidades/ejecuciones del conjunto. |
| Sesión/régimen | Exposición por horario, dirección y volatilidad definida causalmente. |
| Caja | Simultaneidad de compras, activaciones, fallos, renovaciones y cobros. |

Dos firmas diversifican algunas dependencias de proveedor, no la exposición de NQ replicada. Diez variantes que abren LONG al mismo tiempo pueden representar una apuesta económica concentrada. Restricciones interfirmas de hedge/copy deben modelarse desde contratos verificados, sin suponerlas ni eludirlas.

## 12. Revisión adversarial del antecedente

| Riesgo | Tratamiento |
|---|---|
| SPY/otros activos→NQ | Transferir hipótesis, no retornos, Sharpe, slippage ni campañas. |
| Señales de momentum distintas mezcladas | Identificar versión, horizonte y reglas antes de afirmar corroboración/refutación. |
| EOD confundido con enforcement al cierre | Separar actualización del suelo y control intradía. |
| Bots=yes confundido con integración | Certificar plataforma, origen de órdenes y fase; explorar rutas permitidas. |
| Precios y payout caps cambiantes | DR-02 por programa/configuración/cohorte/fecha; no usar cifras archivadas. |
| Neto de split confundido con dinero final | Desglosar transferencias/cambio/impuestos pendientes. |
| Funded tomada como cobro | Modelar toda la cadena y caja recibida. |
| Selección condicionada al pase | No asumir distribución funded independiente del proceso previo. |
| Réplicas contadas como independientes | Medir posiciones/pérdidas/colas/caja conjunta. |
| Datos seleccionados llamados OOS | Conservar trazabilidad de todos los intentos. |
| Orden intrabar supuesto | Declarar ambigüedad y sensibilidad/datos necesarios. |
| Meta31-12 convertida en promesa | Mantener objetivo; no alterar evidencia para alcanzarlo. |
| Expectativa positiva por trade como filtro universal | Corregido por mandato Owner: decisión por campaña/caja. |
| Riesgo alto aceptado como óptimo por intuición | Investigar condiciones y refutadores; no garantía. |
| Citas sin trazabilidad o “PDF completo leído” | No certificado; el antecedente es guía, no autoridad probatoria. |

## 13. Decisiones y recuperación interna pendientes

Sin selección aprobada de props, primera estrategia, reserva, gasto o MM. El orden operativo actual es DR-01 (matemática de campañas), DR-02 (contratos), DR-03 (mecanismos/cobertura) y DR-04 (reglas/validación), con una revisión independiente posterior y consolidación del submanager.

Recuperación interna por el manager: reglas y señales TG/FBC/ORB/MR; inventario de datos/roll/sesiones/volumen; autoridades y evidencias G0–G5; estado real de frente1; rutas de integración permitidas; definición de cohortes e intentos; KYC y condiciones de programas. No delegar a workers externos inferir estos datos de repositorios privados no suministrados.

La existencia de este informe y de los prompts no demuestra estrategia rentable, campaña viable, readiness runtime ni payout. Estado: DR-01 recibido y curado con contradicciones materiales; DR-02/03/04 preparados y no ejecutados. La revisión RV-01 tampoco se ha ejecutado. No se cierra sesión ni se reabre ClutiFX.

## 14. URLs preservadas como semillas de verificación

Fecha de captura documental de este listado: 28-10-2026. Las fechas publicadas/efectivas y accesibilidad deben validarse por los workers. Para claims sin URL recuperable, usar DESCONOCIDO; no inventar soporte. Los títulos siguientes son identificadores de búsqueda, no certificación de contenido actual.

### Literatura y especificaciones

- Zarattini/Aziz/Barbon: https://ssrn.com/abstract=4824172
- Gao et al.: https://doi.org/10.1016/j.jfineco.2018.05.009
- Baltussen et al.: https://doi.org/10.1016/j.jfineco.2021.04.029
- Rosa: https://doi.org/10.1002/fut.22375
- Yu/Rentzler/Wolf: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=712168
- Grant/Wolf/Yu: https://doi.org/10.1016/j.jbankfin.2004.04.006
- Kakushadze/Serur: https://ssrn.com/abstract=3402665
- CME NQ: https://www.cmegroup.com/markets/equities/nasdaq/e-mini-nasdaq-100.html

### Programas y costes comerciales del antecedente

- MFFU Rapid EOD50K: https://help.myfundedfutures.com/en/articles/16158363-rapid-eod-50k-a-comprehensive-look
- MFFU precio: https://myfundedfutures.com/?account=myfundedfutures-rapid-eod-50000
- MFFU instrumentos/fees: https://help.myfundedfutures.com/en/articles/9735811-futures-instrument-list
- MFFU países: https://help.myfundedfutures.com/en/articles/8229993-restricted-countries-policy
- LucidFlex evaluación: https://support.lucidtrading.com/en/articles/12945790-lucidflex-evaluation-account
- LucidFlex funded: https://support.lucidtrading.com/en/articles/12945795-lucidflex-funded-account
- LucidFlex payouts: https://support.lucidtrading.com/en/articles/12945796-lucidflex-payouts
- Lucid comisiones: https://support.lucidtrading.com/en/articles/11508978-approved-products-and-commissions
- Lucid países: https://support.lucidtrading.com/en/articles/11404636-restricted-countries
- Tradeify Select: https://help.tradeify.co/en/articles/12853921-select-evaluation-accounts
- Tradeify payouts: https://help.tradeify.co/en/articles/12853966-select-flex-and-select-daily-payout-policies
- Tradeify precios: https://help.tradeify.co/en/articles/14369021-tradeify-pricing-reference
- Tradeify países: https://help.tradeify.co/en/articles/10495888-rules-restricted-countries
- Topstep parámetros: https://help.topstep.com/en/articles/8284197-trading-combine-parameters
- Topstep payouts: https://help.topstep.com/en/articles/8284233-topstep-payout-policy
- Topstep precios: https://help.topstep.com/en/articles/14289835-topstep-pricing-and-payment-questions

Las afirmaciones sobre bots, acceso API, servidores remotos, noticias, horarios, hedge interfirmas y migración no contaban todas con URL explícita recuperable en el informe. Deben localizarse y contrastarse en fuentes oficiales antes de convertirse en hechos. No usar IDs de citas de chat como URLs de evidencia.

## Prompt

Copiar cada bloque íntegro por separado. No ejecutar RV-01 sin los retornos requeridos.

### DR-01

```text
# ECHO FUTURES — DR-01
## Matemática de campañas prop, resolución rápida y MM por etapa

Actúa como investigador principal de probabilidad aplicada, optimización bajo barreras y economía de campañas prop. Modalidad Deep Research ONE-SHOT. Eres un worker del submanager de investigación, no el manager del producto ni un ejecutor de cuentas.

## Pregunta única

¿Cuándo y bajo qué condiciones una política agresiva que resuelve evaluaciones rápidamente —pase o pérdida— mejora la economía de una campaña prop con capital finito, aunque la señal negociada no tenga esperanza positiva por trade?

## Cápsula autoritativa

- NQ es el único instrumento ejecutable autorizado. MNQ y otros instrumentos no están autorizados.
- Bankroll inicial Futures: USD 4.000, sin nuevos aportes previstos. Los aproximadamente USD 2.000 de Forex están separados y no respaldan Futures.
- El Owner NO plantea gestionar una cuenta propia con objetivo de rentabilidad convencional. Plantea comprar evaluaciones, resolverlas rápidamente, activar funded y extraer retiros bajo una asimetría entre desembolso real y cobro potencial. Arriesgar fuerte es una política a estudiar seriamente, no un error que deba corregirse por defecto. Tampoco es un óptimo demostrado.
- El Owner usa aproximadamente USD 400 por funded como referencia. Es un supuesto por contrastar: distingue precio comercial, coste de la trayectoria que pasó y coste agregado de adquisición incluyendo fallos, resets, renovaciones y activación. No conviertas USD 400 en precio oficial ni en coste esperado verificado.
- La expectativa positiva por trade, profit factor mayor que uno, Sharpe positivo o una curva creciente NO son requisitos universales de admisión. Debes estudiar utilidad económica de campaña. No afirmes tampoco que la asimetría garantice valor favorable.
- Aspiraciones, NO probabilidades estimadas: una cuenta con cobro por cada diez evaluaciones compradas; pase de 1/3 y cobro de 1/3–1/2 de funded activadas.
- Objetivo táctico al 31-12-2026: cinco estrategias challenge y cinco funded produciendo retiros en al menos dos firmas. Pueden coincidir, diferir o mezclarse. No es factibilidad demostrada ni obligación de inventar diez sistemas.
- Primer retiro objetivo USD 3.000: estudiar tanto bruto antes del split como neto recibido, con splits 90% y 80%. Ninguna firma/programa está seleccionado.
- Strategy tiene exactamente SETUP, FILTRO opcional y OBJETIVO/RIESGO o RR técnico, con identidad y versión. MM por prop/programa/etapa es otra entidad. No cambies señales para compensar silenciosamente un problema de MM.
- G0–G5 ya existen: no redefinirlos ni declarar que se superaron. Frente 1 se encarga del motor/runtime. No diseñes otro motor.

## Investigación acotada

1. Separa cuatro objetos: distribución de trades; resultado de una cuenta/etapa; campaña completa compra→pase→activación→cobro(s); caja del Owner. Formaliza estados, horizontes, pendientes y denominadores.
2. Estudia first-passage/hitting probabilities, tiempos de absorción, gambler's ruin y optimal stopping/control donde realmente apliquen. Da supuestos y límites: barreras fijas frente a trailing intradía/EOD, incrementos discretos, overshoot, saltos, dependencia temporal, comisiones y restricciones comerciales. No transfieras una fórmula de random walk a un RuleSet path-dependent sin justificación.
3. Compara conceptualmente riesgo bajo, riesgo alto constante, políticas por distancia al target/límite, por tiempo disponible, y cambios entre challenge y funded. Riesgo alto no equivale necesariamente a martingala. No impongas un porcentaje conservador ni maximización de duración de cuenta.
4. Examina si señales con esperanza por trade positiva, nula o negativa pueden generar valor de campaña favorable bajo contratos explícitos. Incluye un caso algebraico donde la asimetría ayude y otro donde costes, payout caps o fase funded la destruyan. Distingue resultados matemáticos bajo supuestos de evidencia empírica sobre NQ. No prometas estrategias “probadas” universalmente.
5. Explica selección condicionada al pase: una funded no es una cuenta tomada al azar. Evalúa dependencia entre éxito de evaluación y cobro funded, cambio de régimen, MM, tamaño y reglas. Usa probabilidades condicionales; no presupongas independencia entre etapas o cuentas.
6. Modela retiros netos efectivamente recibidos menos desembolsos externos, tiempo hasta cobro, probabilidad de financiar el siguiente intento, déficit máximo de caja y agotamiento antes del horizonte. Beneficio SIM, saldo nominal y pago aprobado pero no recibido no son caja disponible. No dupliques comisiones/slippage ya descontados del PnL que origina un payout.
7. Analiza el coste agregado por funded activada y por cuenta que paga. Explica censura de cohortes abiertas. El objetivo 1/10 no prueba autosostenimiento. Dos props con las mismas señales NQ no vuelven independientes los fallos.
8. Define una frontera de decisión entre velocidad de resolución, probabilidad/importe de cobro, caja y riesgo de agotamiento. No combines todo en un score con pesos inventados; entrega alternativas para decisión Owner. Considera primeros y posteriores retiros, pérdida/cierre de funded y reemplazo, sin asumir supervivencia indefinida como objetivo.
9. Propón la especificación mínima de experimentos de campaña que el frente interno podría ejecutar después: señales congeladas × MM × RuleSet × condiciones iniciales × horizonte. Incluye controles y contraejemplos. No ejecutes esos experimentos.

## Fuentes y entrega

Usa fuentes primarias de probabilidad/control/finanzas y contratos oficiales sólo para ilustraciones verificadas. No hagas aquí una criba comercial: eso pertenece a DR-02. Puedes trabajar con un vector abstracto de reglas, marcándolo como supuesto, sin esperar su resultado.

Entrega: síntesis; modelo matemático con variables/unidades; tabla de políticas y condiciones de utilidad/refutación; ejemplos algebraicos transparentes; métricas de campaña/caja; requisitos de datos; dos experimentos priorizados; decisiones Owner; limitaciones; fuentes con URL, autor, fecha de publicación/consulta, alcance y sección realmente leída. Etiqueta HECHO, INFERENCIA, PROPUESTA y DESCONOCIDO.

Retorno: `DR-01 | RESPONDIDO / PARCIAL / DEPENDENCIA | conclusión | condiciones que la invalidan | interfaces para DR-02/03/04 | próxima decisión`. Una respuesta negativa o condicionada es válida.

## Autoridad y parada

Sólo investigación externa y cálculo algebraico. No código, backtests, Monte Carlo, compras, órdenes, mensajes a soporte, cambios de cuenta, acceso a repositorios/Hefesto ni escritura/cierre en Agents-OS. No asumas otros chats o archivos no adjuntos. Estudia cumplimiento de contratos; no propongas ocultar automatización, hedge prohibido ni evadir reglas de alto riesgo.

Presupuesto: una entrega, una revisión adversarial interna identificada como tal y una reparación focal si una contradicción material impide decidir. Detente con una decisión investigable o dependencia indispensable explícita. No preguntes para prolongar el encargo ni busques hasta obtener una conclusión favorable.
```

### DR-02

```text
# ECHO FUTURES — DR-02
## Contratos prop actuales, automatización y economía comercial completa

Actúa como investigador principal de programas prop de futuros, restricciones contractuales y costes de adquisición/cobro. Modalidad Deep Research ONE-SHOT. Reportas al submanager; no seleccionas ni compras cuentas.

## Pregunta única

¿Qué programas concretos permiten investigar y eventualmente ejecutar campañas algorítmicas NQ, incluidas políticas de riesgo alto y resolución rápida, con USD 4.000 de caja y posibilidad efectiva de retiros útiles?

## Cápsula autoritativa

- NQ exclusivamente; no MNQ ni sustitución por otro instrumento.
- USD 4.000 de capital Futures, sin nuevos aportes; Forex tiene aproximadamente USD 2.000 separados e indisponibles para este encargo.
- El objetivo es economía de campañas prop, no rentabilidad convencional por trade. No exijas expectativa positiva de la señal para admitir un programa. Riesgo alto y resolución rápida son políticas que investigar; su admisibilidad contractual debe verificarse, no suponerse.
- Aproximadamente USD 400 por funded es una referencia del Owner, NO precio oficial ni coste esperado certificado. Distingue coste de un pase afortunado y adquisición agregada incluyendo intentos fallidos.
- Objetivos, no tasas observadas: al menos una cuenta que cobra por diez evaluaciones; pase 1/3 y cobro 1/3–1/2 de funded activadas. Hito 31-12-2026: cinco estrategias challenge y cinco funded produciendo retiros en al menos dos firmas, con superposición libre.
- Primer retiro USD 3.000: analizar bruto previo al split y neto recibido, para 90% y 80%. No hay prop, programa, plataforma ni reserva elegidos.
- Strategy y MM por prop/programa/etapa son entidades distintas. No modificar reglas de señal para hacer cuadrar silenciosamente un programa.
- No presumas disponibilidad técnica de Echo, un adaptador o una API. La residencia/nacionalidad y KYC del titular no están certificados en esta cápsula; deja elegibilidad condicionada cuando sea necesario.
- La búsqueda previa mencionó MyFundedFutures, Lucid Trading, Tradeify y Topstep. Son semillas de búsqueda sin prioridad aceptada. Sus precios, restricciones y supuestas incompatibilidades NO están certificados por ese antecedente.

## Alcance y método

Criba como máximo cuatro firmas y dos programas concretos por firma. Puedes reemplazar semillas con fundamento. Amplía sólo si es necesario para encontrar dos alternativas elegibles y explica el motivo. No gastes el cupo estudiando exhaustivamente una firma que incumpla un requisito duro inequívoco.

Para cada alternativa identifica Provider / Program / tamaño / fase / plataforma / fecha y versión de RuleSet. Separa evaluación, simulated funded y live, incluyendo cambios al migrar; evita combinar el precio barato de una configuración con reglas de otra más cara.

Verifica en fuentes oficiales:

- Fees de compra, resets, renovaciones, plazos, cancelación, activación, datos, plataforma, API, comisiones NQ por lado y round trip, extras obligatorios, transferencia, conversión y cualquier cargo relevante. Separa precios de lista, promociones, condiciones y caducidad. No presupongas que una promo se repite.
- Target, MLL, trailing intradía o EOD, tratamiento de unrealized/realized, momento de actualización del suelo y momento de enforcement. EOD no implica que la cuenta sólo pueda fallar al cierre.
- Consistencia por etapa, días mínimos/ganadores, inactividad, horarios, noticias, contrato máximo/escalado y límites por operación/día. Busca cláusulas contra all-in, overleveraging, gambling, account flipping, uso asimétrico y explotación de fills. Cita redacción y alcance; no equipares automáticamente toda política de riesgo alto con una prohibición.
- Bots propios, API/origen de órdenes, bridge o plataforma autorizada, ejecución local/remota, VPS/VPN, distribución/copia, ownership del sistema, simultaneidad, posiciones contrarias entre cuentas y entre firmas. “Bots permitidos” no acredita una integración específica. “API preferida no disponible” tampoco descarta una ruta alternativa realmente permitida.
- Payouts: split, cap bruto/neto, porcentaje retirable, buffers antes/después, mínimos, cadence, revisión/discreción, forma de pago, plazos, balances tras cobro, cierre/transición a live y continuidad de automatización. Cuenta fondeada, elegible, pago aprobado y dinero recibido son estados distintos.
- Multicuentas, máximos por persona/hogar y consolidación/cierre al migrar. Reglas relevantes entre firmas. Elegibilidad territorial y diferencias SIM/live.

## Análisis comercial requerido

1. Entrega una matriz comparable y una fila explícita por cada campo desconocido. No conviertas ausencia de prohibición encontrada en permiso certificado.
2. Clasifica cada ruta: ELEGIBLE DOCUMENTALMENTE; CONDICIONADA A CONFIRMACIÓN; INCOMPATIBLE CON REQUISITO EXPLÍCITO; NO VERIFICADA. La integración física sigue pendiente aunque el contrato permita automatización.
3. Calcula, sólo algebraicamente, el beneficio/saldo y requisitos para solicitar USD 3.000 brutos o recibir USD 3.000 tras split. No confundas payout cap, beneficio disponible y buffer. Incluye recepción efectiva y costes pendientes; distingue neto de split de neto final de cargos/impuestos.
4. Presenta desembolsos de una evaluación que falla, una que pasa, una funded que falla antes de cobrar, un primer cobro y cobros posteriores. No estimes probabilidades de éxito desde testimonios ni marketing.
5. Contrasta la referencia USD 400/funded con costes verificables y con el coste agregado de intentos. No fijes reserva ni autorices compras.
6. Entrega un vector de RuleSet y costes utilizable por DR-01/DR-04, sin diseñar código ni otro motor. Señala campos que cambian la matemática de barreras, duración, sizing o distribución de retiros.
7. Identifica riesgos de contraparte, discrecionalidad y cambios de condiciones sin certificar solvencia por número de reviews o pagos publicitados. Diferencia límites objetivos de incertidumbre contractual.

## Fuentes, retorno y parada

Fecha de referencia del mandato: 28-10-2026; usa la fecha real de consulta y no la inventes. Por cada afirmación material entrega URL oficial exacta, título, fecha publicada/efectiva/consulta (o “no informada”), extracto breve y fase/programa al que aplica. Contrasta términos y help center; reporta contradicciones, páginas inaccesibles y condiciones de cohortes antiguas. No uses afiliados o comparadores como autoridad de reglas.

Entrega resumen, matriz completa, lista de alternativas y bloqueos, cálculo de retiros/caja, preguntas cerradas para soporte que el Owner podría enviar y fuentes. Etiquetas HECHO / INFERENCIA / PROPUESTA / DESCONOCIDO.

Retorno: `DR-02 | RESPONDIDO / PARCIAL / DEPENDENCIA | alternativas elegibles/condicionadas | RuleSets | costes | bloqueos | próxima decisión`.

No backtests, Monte Carlo, compras, órdenes, contacto con firmas, alta de cuentas, escritura de repositorios ni cierre de Agents-OS. No asumas otros chats o adjuntos no recibidos. Una entrega y una reparación focal sólo si una contradicción impide decidir. Detente al lograr una comparación investigable o identificar una dependencia indispensable; no amplíes la búsqueda para forzar dos firmas “aprobadas”.
```

### DR-03

```text
# ECHO FUTURES — DR-03
## Mecanismos NQ, evidencia, contraevidencia y cobertura de estrategias

Actúa como investigador cuantitativo de mecanismos de precio y selección de hipótesis. Modalidad Deep Research ONE-SHOT. Eres un worker especializado; no eliges MM, props ni despliegues.

## Pregunta única

¿Qué mecanismos objetivos merece investigar Echo Futures para modificar favorablemente la distribución de resultados y trayectorias de campañas prop NQ, aportando cobertura respecto del trabajo existente, sin confundir indicadores, variantes o ganancias de mercado con utilidad de campaña?

## Cápsula autoritativa

- Sólo NQ está autorizado para ejecución. Otros activos pueden aportar literatura comparativa, no propuestas de operación. No MNQ.
- Bankroll USD 4.000 Futures sin aportes adicionales; aproximadamente USD 2.000 Forex separados. Referencia Owner USD 400/funded no verificada como coste agregado.
- El negocio buscado es compra→pase/pérdida rápida→funded→retiros. No se impone expectativa positiva por trade como gate universal. Tampoco se presupone que una señal mala sea útil por la sola existencia de payouts. Investiga propiedades verificables de distribuciones y trayectorias; la valoración de campaña corresponde al modelo económico.
- Se estudian políticas agresivas, sin imponer conservación de cuenta ni riesgo bajo como doctrina. No autorices ninguna política ni eludas contratos.
- Aspiraciones no estimadas: una cuenta que cobra por diez evaluaciones; pase 1/3 y cobro 1/3–1/2 de funded activadas. Meta 31-12-2026: cinco estrategias challenge y cinco funded con retiros en al menos dos firmas; pueden ser las mismas, diferentes o una mezcla.
- Primer retiro USD 3.000 bruto/neto y split 90%/80% son escenarios. Ninguna prop está seleccionada.
- Trabajo existente: TG/TradesGerard, FBC/NY First Candle, ORB y MR01–MR10. FBC sigue dirección de una primera vela cerrada; NO significa failed breakout. ORB usa ruptura de rango. MR08 incluye recuperación local condicionada a tendencia H1. Las otras reglas son desconocidas: no las inventes desde nombres.
- R03 aporta historia simulada y confirmación temporal retrospectiva, no OOS virgen, producción ni retiros. ClutiFX queda como histórico y no se reabre. Earn2Trade/GAU50 no es elección comercial actual.
- El baseline menciona OHLCV 1m, con disponibilidad/cobertura física NO certificadas. No asumas trades, quotes, L2, datos de opciones o intermercado.
- Cada Strategy tiene sólo SETUP, FILTRO opcional y OBJETIVO/RIESGO o RR técnico, más identidad/versión. MM por cuenta/programa/etapa es otra entidad. G0–G5 se conservan sin reinterpretación.

## Investigación acotada

1. Construye una taxonomía económica pequeña: persistencia/continuación/pullback; reversión de presión transitoria/exceso; rupturas aceptadas frente a fallidas/recuperaciones. Apertura, sesión, volatilidad y VWAP pueden ser contexto, medida o parte de un mecanismo, no familias automáticamente independientes.
2. Busca evidencia y contraevidencia primaria. Declara instrumento, mercado, horizonte, período, diseño, costes, ejecución, revisión por pares/preprint y si leíste texto completo o sólo abstract. Evidencia SPY/QQQ, otros futuros, Forex o acciones no equivale a evidencia propia NQ.
3. Examina decay post-publicación, selección, variación de régimen, dependencia de unas pocas sesiones y sensibilidad a fricciones. No conviertas una explicación de microestructura en un dato observable con OHLCV.
4. Relaciona provisionalmente los mecanismos con TG/FBC/ORB/MR. Separa cobertura probable, redundancia sospechada, equivalencia demostrada y desconocido. No declares diversificación por nombres o por usar distintos timeframes, indicadores, RR o MM.
5. Prioriza aprendizaje útil para campañas, plausibilidad, datos requeridos, reutilización y coste de refutación. Considera asimetría de payoff, concentración de movimientos, secuencias adversas, frecuencia/sequías, duración y facilidad de alcanzar barreras. No clasifiques únicamente por Sharpe, beneficio bruto o rentabilidad de una cuenta propia.
6. Selecciona como máximo cuatro líneas investigables; recomienda una primera y una alternativa con mecanismo distinto. Una celda vacía no obliga a crear una estrategia. No aceptes por inercia las prioridades de una revisión exploratoria anterior.
7. Deja eventos, intermercado y microestructura como líneas condicionadas cuando exijan datos/autorización no disponibles. No inventes “liquidez barrida”, “absorción” o “gamma de dealers” como hechos medidos por una vela o RSI.

## Ocho puntos obligatorios por línea recomendada

1. Hipótesis falsable, incluyendo qué propiedad medible cambiaría y por qué podría importar a una campaña.
2. Mecanismo económico propuesto o regularidad empírica, sin confundir narración con identificación causal.
3. Evidencia, fuente verificable y contraevidencia; alcance de transferencia a NQ.
4. Datos mínimos y disponibilidad causal de cada observación.
5. Modelo de ejecución y límites de observabilidad; no inferir orden intrabar desde OHLCV 1m.
6. Control comparable y criterio de refutación propio. Expectativa negativa por trade no es descarte automático: explica cuándo sí refuta la hipótesis formulada y cuándo exige valoración de campaña.
7. Coste relativo de implementación/validación, supuestos y desconocidos, sin inventar horas ni throughput.
8. Cobertura esperada y prueba pendiente de independencia frente al inventario existente.

Estos ocho puntos van en fichas de investigación separadas, no como bloques nuevos de Strategy. Puedes incluir hasta tres fichas ilustrativas deterministas de tres bloques; parámetros explícitos, sin presentarlos como óptimos. DR-04 desarrolla la anatomía de medidas y el protocolo; evita duplicarlo.

## Fuentes y entrega

Semillas opcionales, no evidencia aceptada: Zarattini/Aziz/Barbon, SSRN 4824172; Gao et al., Market Intraday Momentum; Baltussen et al., Hedging Demand and Market Intraday Momentum; Rosa, Understanding Intraday Momentum Strategies; estudios de Yu/Rentzler/Wolf y Grant/Wolf/Yu. Contrástalos y amplía sólo donde cambie una decisión. No des por leído un adjunto no recibido.

Entrega síntesis, mapa mecanismo→medida→regla→evidencia→limitación, tabla de cobertura provisional, fichas de hasta cuatro líneas, primer experimento y alternativa, descartes/diferidos y fuentes con URL/autor/fechas/alcance. Etiqueta HECHO / INFERENCIA / PROPUESTA / DESCONOCIDO. No hagas una criba comercial ni calcules probabilidades propias de pase/cobro.

Retorno: `DR-03 | RESPONDIDO / PARCIAL / DEPENDENCIA | líneas priorizadas | evidencia/contraevidencia | cobertura desconocida | datos | próxima decisión`.

Sólo investigación. No código, backtests, simulaciones Monte Carlo, compras, órdenes, acceso a repositorios/Hefesto, cambios de gates ni registros/cierre en Agents-OS. Presupuesto: una entrega, revisión adversarial interna y una reparación focal si una contradicción bloquea la decisión. Detente con hipótesis refutables o una dependencia indispensable; no generes una lista interminable de recetas.
```

### DR-04

```text
# ECHO FUTURES — DR-04
## Indicadores, reglas simples y validación orientada a campañas

Actúa como investigador de diseño experimental cuantitativo, indicadores causales y validación de estrategias de campaña prop. Deep Research ONE-SHOT. No eres arquitecto de otro backtester ni implementador.

## Pregunta única

¿Cómo convertir hipótesis NQ en reglas reproducibles de tres bloques y compararlas bajo MM/RuleSets de campaña sin sobreajuste, sin inventar fills y sin imponer rentabilidad positiva por trade como requisito universal?

## Cápsula autoritativa

- Ejecución autorizada sólo NQ; no MNQ. Verifica en CME unidades de precio y multiplicador: expresar puntos/ticks/dólares explícitos, no “pips”.
- USD 4.000 Futures sin nuevos aportes; aproximadamente USD 2.000 Forex separados. Aproximadamente USD 400/funded es referencia Owner no validada como coste completo.
- Objetivo económico: comprar evaluaciones, resolver pase/pérdida rápidamente, activar funded y obtener retiros. Riesgo alto puede ser deliberado; no es un defecto por definición. Señal, MM, cuenta, campaña y caja son niveles diferentes.
- Expectativa por trade, profit factor o Sharpe son descriptores posibles, no gates universales de promoción. La utilidad se juzga por campaña y caja. No prometas utilidad de campaña sólo porque existe asimetría contractual.
- Aspiraciones no medidas: una cuenta que paga por diez evaluaciones; pase 1/3 y cobro 1/3–1/2 de funded activadas. Hito 31-12-2026: cinco estrategias challenge y cinco funded con retiros en dos firmas, con superposición libre. Primer retiro USD 3.000 bruto/neto con split90%/80% se analiza por escenarios.
- Baseline: OHLCV 1m mencionado, cobertura física no certificada. TG, FBC, ORB y MR01–MR10 existen, sin reglas completas suministradas; FBC sigue primera vela cerrada, ORB rompe rango, MR08 recupera localmente con tendencia H1. R03 es retrospectivo, no OOS virgen. ClutiFX histórico, no reabrir; E2T/GAU50 histórico, no programa elegido.
- Strategy tiene únicamente SETUP, FILTRO opcional y OBJETIVO/RIESGO o RR técnico. Identidad y versión acompañan. MM dimensiona y controla por prop/programa/etapa. No meter gobierno, cuentas, cartera, validación ni arquitectura como bloques extra.
- G0–G5 existen: conservar autoridades y definiciones, no reemplazarlas ni declararlas superadas. Frente 1 gestiona motor/runtime. Entrega requisitos de evidencia y experimentos, no diseño de otro motor.

## Investigación acotada

1. Clasifica un conjunto mínimo de medidas por dirección, extensión, rango, volatilidad, actividad/volumen y contexto temporal. Para cada candidata: fórmula/unidades, datos, instante causal de disponibilidad, warm-up, lag, límites, pregunta que responde y redundancias. No catálogo de indicadores por popularidad.
2. Propón combinaciones motivadas por hipótesis y tests baseline→un filtro→ablación. Mide frecuencia perdida, cambios de distribución, duración y valor incremental de campaña; no declares inútil un filtro sólo porque baja el PnL convencional, ni útil porque sube win rate.
3. Define hasta tres fichas Strategy ilustrativas de tres bloques y fáciles de programar posteriormente. Especifica cierres de barra, dirección, condiciones, entrada posterior, referencias, parámetros, timeframes, reentrada/duplicados, stop/target y unidades. Todo visual debe convertirse en predicado o excluirse. Declara qué salidas provienen del MM vigente, sin inventarlas como reglas de señal.
4. Separa RR planeado de payoff realizado. Cambiar stop/objetivo requiere recalcular trayectorias; no multiplicar una curva anterior. Estudia cómo geometría y frecuencia pueden cambiar tiempos a target/límite, overshoot, costes, posiciones concurrentes y payout. Distingue un cambio de Strategy de otro sólo de sizing/MM.
5. Define un conjunto mínimo de métricas, cada una con fórmula, denominador, datos y decisión: oportunidades/frecuencia/sequía; distribución de PnL y excursiones; dependencia/colas; tiempo a barrera; pase, pérdida y pendientes; activación y cobro condicionales; retiros netos; coste por funded/pagadora; máximo déficit de caja y probabilidad de financiar el siguiente intento. Separa métricas de trade, cuenta, campaña y bankroll.
6. Especifica comparación de señales congeladas contra MM y RuleSets diferentes. Conserva oportunidades originales y registra vetos, cambios de contratos y salidas de MM. No trates muestras filtradas por el MM como si fueran señales independientes. Riesgo mínimo de 1 NQ puede vetar operaciones; no reduzcas el stop técnico ni cambies a MNQ silenciosamente.
7. Diseña validación temporal y de selección: inventario de intentos, elección de parámetros, bloques de descubrimiento/selección/confirmación, protección de datos futuros, multiple testing, controles y sensibilidad. No reutilices datos elegidos como OOS virgen. Explica cuándo escasez impide concluir; no uses cuotas mágicas de trades ni rebajes G0–G5 por rareza o destino funded.
8. Explica límites de OHLCV M1: orden stop/target, picos de equity para trailing, quotes/spread, gaps, fills, latencia, límites y tamaño. Propón clasificación de casos resolubles/ambiguos, bounds conservadores y datos adicionales necesarios. No presentar un recorrido supuesto como ejecución observada.
9. Define medidas de cartera: coincidencia de señales y posiciones; pérdidas conjuntas; drawdowns simultáneos; exposición por dirección/sesión/régimen; dependencia de cola; sequías conjuntas y sincronización de desembolsos. Dos firms no independizan el mismo NQ; estrategias con poco solapamiento también pueden fallar en el mismo régimen. Revisar restricciones de hedge/copy provistas por contratos, no presumirlas.
10. Entrega un protocolo futuro acotado para comparar políticas agresivas y otras alternativas. No optimices parámetros ni ejecutes simulaciones. No inventes la capacidad de Hefesto, tiempos, costes de datos ni una arquitectura nueva.

## Entrega y límites

Entrega tabla funcional de indicadores; fichas ilustrativas; diccionario mínimo de métricas; diseño experimental señal→MM→RuleSet→campaña/caja; matriz de observabilidad; control de múltiples intentos; requisitos de datos; una primera prueba y alternativa con refutadores. Explica qué puede evaluarse sin retorno de DR-01/02/03 y qué queda condicionado a sus resultados, sin bloquear el resto.

Usa documentación técnica y papers primarios, con URL, fecha, alcance y declaración de texto completo/abstract. Marca HECHO, INFERENCIA, PROPUESTA y DESCONOCIDO. Un indicador no demuestra edge ni un teorema bajo supuestos prueba una campaña real.

Retorno: `DR-04 | RESPONDIDO / PARCIAL / DEPENDENCIA | protocolo | métricas | fichas | límites de datos | interfaces | próxima decisión`.

No código, backtests, Monte Carlo, compras, órdenes, accesos a repositorios/Hefesto, modificaciones de producto/gates ni escritura o cierre de Agents-OS. Sólo cápsula y adjuntos recibidos. Una entrega, revisión adversarial interna identificada como tal y una reparación focal si una contradicción material impide decidir. Termina con una decisión investigable o dependencia indispensable, no con más investigación indefinida.
```

### RV-01

```text
# ECHO FUTURES — RV-01
## Revisión adversarial independiente de los cuatro retornos

Actúa como revisor independiente. Este encargo NO es una quinta investigación amplia. Entradas requeridas: retornos completos DR-01, DR-02, DR-03 y DR-04, sus fuentes y la cápsula/corrección económica Owner incluida en esos mandatos. No asumas que los recibiste: identifica cualquier ausencia y revisa lo disponible sin inventar resultados.

Pregunta: ¿los cuatro retornos sustentan una decisión investigable coherente para campañas prop NQ con USD 4.000, o siguen conteniendo una contradicción/dependencia que la invalide?

Marco obligatorio: la unidad económica es campaña/caja, no rentabilidad convencional por trade. Expectativa por trade no positiva NO es descarte universal. La asimetría contractual NO prueba utilidad automáticamente. USD 400/funded y tasas 1/3, 1/3–1/2 y 1/10 son referencia/aspiraciones Owner, no estimaciones. NQ exclusivo, tres bloques Strategy, MM separado, cero aportes, Forex separado, G0–G5 sin redefinir.

Audita especialmente:

1. Barreras fijas vs trailing y enforcement intradía, overshoot, discretización, dependencia, funded condicionada al pase y supuestos de los teoremas.
2. Coste de una funded ganadora vs adquisición agregada; pérdidas pendientes; doble descuento de fees/comisiones; neto de split vs dinero recibido; beneficio SIM contado como caja; cap/buffer/porcentaje retirable; cohortes y horizonte.
3. Confusión entre resolver rápido y optimizar campaña; riesgo alto permitido vs prohibido; agresividad convertida en garantía; conservación de cuenta impuesta por defecto.
4. Fuentes de firmas por programa/fase/fecha/plataforma; API propia vs plataforma compatible; bots permitidos vs origen de órdenes confirmado; live, hedge y copy entre firmas; contradicciones documentales.
5. Evidencia de otro activo transferida a NQ; resúmenes que sólo leyeron abstract; mecanismos narrativos tratados como observados; falsa independencia por variantes/MM/firms; atribución de resultados de un paper a reglas adaptadas.
6. Leakage, múltiples intentos, confirmación retrospectiva llamada OOS virgen, filtros/parametrización sin control, datos intrabar inventados y puertas de cualificación debilitadas.

Verifica directamente sólo las fuentes críticas que puedan cambiar el dictamen. Una búsqueda focal para resolver una contradicción material está permitida; no rehagas las cuatro investigaciones ni votes por mayoría de IAs.

Devuelve tabla de hallazgos con severidad BLOQUEANTE/MATERIAL/MENOR, claim exacto, evidencia, impacto y reparación mínima. Luego: coincidencias sólidas; contradicciones entre módulos; dependencias; decisiones Owner; propuesta de siguiente experimento y alternativa. Dictamen `APTO_PARA_DECIDIR_INVESTIGACION`, `APTO_CON_CONDICIONES` o `NO_APTO_AUN`, sin convertirlo en autorización de gasto/operación o G0–G5.

No implementación, código, simulaciones, compras, contacto con terceros, cuentas ni edición/cierre de Agents-OS. Una entrega y una reparación focal, nunca investigación indefinida. Declara independencia efectiva respecto de los autores; si no existe, llámalo autorrevisión y no revisión independiente.
```

## Límites

Sólo documentación y preparación de mandatos en esta actualización. No código de producto, ejecución de backtests/Monte Carlo, compras, órdenes, modificaciones de cuenta, aceptación de entregas/gates, cambio del frente 1 ni cierre formal de sesión. Publicación documental sobre master, sin ramas/PRs ni force. El próximo paso es ejecutar DR-01 en una sesión externa y retornar el informe; el submanager consolida cuando reciba los resultados, no de forma asíncrona.
