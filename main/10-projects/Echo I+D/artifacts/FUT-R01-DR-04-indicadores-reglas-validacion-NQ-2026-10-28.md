# FUT-R01 / DR-04 — Indicadores, reglas simples y validación orientada a campañas NQ

> **Tipo:** artefacto documental de investigación recibida (no Strategy/RuleSet canónico, no validación técnica). **Fecha de recepción:** 2026-10-28. **Fuente:** retorno DR-04 facilitado por el Owner, adjunto «Texto pegado(9).txt» (128 líneas). **Estado autodeclarado por la investigación:** `DR-04 | RESPONDIDO`. **Estado de registro:** `RECEIVED_WITH_MATERIAL_FINDINGS / OWNER_REVIEW_PENDING`. **Proyecto:** [[Echo I+D — Futures]]. **Mandato:** [[FUT-R01-RESEARCH-MANDATE]] v4.

## Control de uso por otros agentes

- **Preservación:** el texto original se reproduce íntegro después de este control; no se corrigen silenciosamente sus resultados, fórmulas ni afirmaciones. No se ha hecho verificación primaria ni revisión independiente de RV-01.
- **F1 — UNIDADES Y FICHAS:** la sección «Ficha Trend-Breakout» ejemplifica stop = 0,5 × ATR como 0,5 puntos pero target = 1 × ATR como 0,25 puntos, inconsistente para un mismo ATR; otros parámetros `x`/`umbral` quedan sin definición. La desviación típica de retornos logarítmicos es adimensional, no «puntos NQ» sin transformación.
- **F2 — SEÑAL VS MM:** «0,5 NQ» y «1 NQ mínimo de riesgo» mezclan fracción de contrato con presupuesto de riesgo; para NQ se necesitan contratos enteros y riesgo `distancia stop (puntos) × USD 20/punto × contratos` más costes. No reducir stop técnico ni sustituir MNQ.
- **F3 — OBSERVABILIDAD DE FILLS:** el tratamiento de stop/target y trailing con OHLC M1 no permite certificar el orden intrabar ni precios ejecutados. Los «bounds» y los stops expresados como extremos favorables/adversos no constituyen un recorrido observado.
- **F4 — VALIDACIÓN / TRAZABILIDAD:** el retorno no proporciona el diccionario completo con denominadores y decisiones, matriz de observabilidad, inventario de intentos ni evidencia bibliográfica primaria reproducible exigidos por DR-04; usa referencias secundarias y afirma `PF>2` como criterio institucional sin base universal. El estado «RESPONDIDO» no implica contrato satisfecho.
- **F5 — GEOMETRÍA / MM:** proponer «stops más amplios» como variación solo de sizing/MM altera la geometría Strategy y exige recalcular trayectorias; es distinto de comparar MM con señal/geometría congeladas.
- **USO PERMITIDO:** servir como insumo provisional para consolidación de FUT-R01, reparación focal y revisión adversarial `RV-01`. **NO** validar estrategias, alterar G0–G5, declarar edge/pases/payouts, publicar RuleSets ni ejecutar campañas. El frente 1 Backtester–runtime mantiene autoridad independiente.

## Informe recibido — transcripción íntegra

# Indicadores mínimos  

Clasificamos indicadores clave en *dirección/tendencia*, *extensión/rango*, *volatilidad*, *volumen/actividad* y *contexto temporal*. Por ejemplo:  
- **Direccionalidad (Tendencia):** e.g. cruce de medias (MA corto cruzando MA largo) o momentum de precio (`Δ`). Fórmula: diferencia (%) de precio (puntos NQ) en periodo (ej. cierre–apertura). Disponible al cierre de cada vela M1. Warm-up = período de MA; lag = 0. Responde “¿hay sesgo alcista o bajista?”. Redundancia posible con momentum. _(HECHO; fuente de categorías)_.  
- **Extensión/Rango:** e.g. *Average True Range (ATR)* o (High–Low) de la barra. ATR de N días: ATR = media móvil de max(high−low, |high-prevClose|, |low-prevClose|). Medida en puntos de NQ (tick=0.25p=$5). Warm-up = N velas; responde “¿qué tan lejos podría moverse el precio?”. Limitada en rangos muy laterales. _(PROPUESTA)_  
- **Volatilidad:** e.g. desviación estándar de retornos recientes o bandas de Bollinger. Por ejemplo, σ sobre retornos logarítmicos de 10 velas (sincrónico hasta vela previa). Unidad en puntos NQ. Disponible al cierre. Warm-up según ventana; alta latencia ante shocks. Responde “riesgo del movimiento” y ayuda a ajustar stops. _(PROPUESTA)_  
- **Volumen/Actividad:** e.g. volumen de contratos (trades) totales por vela o *On-Balance Volume*. El volumen real de NQ (contratos negociados) se suma minuto a minuto. Disponible con latencia ~1 min. Warm-up = 1 vela; sin retraso. Responde “hay interés en el movimiento actual”. Ayuda a filtrar rupturas con bajo volumen. _(HECHO/PROPUESTA)_  
- **Contexto temporal:** p.ej. hora del día o día de la semana. Variables binarias o categóricas (sesión, weekday) disponibles por adelantado, sin warm-up. Permiten modelar patrones intradía (p.ej. baja actividad medio día) o estacionalidad. _(PROPUESTA)_  

Cada indicador tiene *disponibilidad causal* sólo al cierre de vela (o antes, si es intrabar). Sus **unidades** deben ser consistentes: puntos de índice NQ (no “pips”). Ej. 1 punto NQ = $20, 1 tick = $5. Se debe anotar su *lookback* (warm-up) para iniciar valores creíbles. Por ejemplo, σ[10] requiere 10 velas M1. Responde a preguntas distintas: e.g. ATR a “¿puede moverse tanto?”, MA-ADX a “¿hay tendencia fuerte?”. Algunos indicadores redundan (p.ej. ATR y bandas) – elegir el esencial por pársimony (KISS). 

# Combinaciones e hipótesis (filtro y ablation)  

Proponemos **combinaciones basadas en hipótesis**: partimos de un setup básico (baseline) y aplicamos filtros orientados, luego retiramos uno a la vez (*ablación*) para medir aportes marginales. Por ejemplo:  
- *Basal:* cruce de EMA(50)>EMA(200) ⇒ señal de compra en cierre de vela.  
- *Filtro vol:* solo operar si ATR(14) > umbral (i.e. mercado suficientemente agitado).  
- *Filtro horario:* solo en primeras 2h de mercado (alta liquidez).  

Para cada combinación medimos: frecuencia de señales (p.ej. % días con señal), eventos perdidos (señales vetadas por filtros) y cambios en la distribución de PnL (media, varianza). Por ejemplo, añadir filtro horario reducirá trades totales (disminuye frecuencia) pero puede concentrar operaciones en velas con bajo slippage. Un filtro *útil* puede bajar el profit conventional pero mejorar medidas de riesgo (p.ej. menor Máx Drawdown) – no lo descartamos automáticamente. Se debe evaluar su aporte *incremental*: comparar equity con y sin filtro usando métricas de campaña (p.ej. % de passes, drawdown) en lugar de solo PnL por trade.

Esta validación debe evitar *sobreajuste*: no ajustar filtros tras ver resultados (no “inventar fills” arbitrariamente). Usar múltiples periodos de train/test, controles por permutaciones y corregir por pruebas múltiples (p.ej. Probabilidad de Overfitting). 

# Fichas de estrategia (3 ejemplos)  

Definimos tres *estrategias de tres bloques* (Setup + [Filtro] + Objetivo/Riesgo) fácilmente programables:  

1. **Ficha Trend-Breakout:**  
   - **Setup:** Si cierra Vela M1 > SMA(20) y SMA(20) > SMA(50) (tendencia alcista), preparar compra.  
   - **Filtro:** ATR(14) > x (mercado activo) y horario 09:30–11:00 (liquidez alta).  
   - **Entrada:** Abrir posición larga al abrir siguiente vela M1 tras cierre que cumple Setup+Filtro.  
   - **Stop/Objetivo:** Stop = 0.5×ATR (por ejemplo, 0.5 pts=2 ticks ~$10) bajo precio de entrada; Target = 1×ATR (0.25 pts=$5). Unidades = 1 contrato NQ.  
   - **Reentrada/duplicado:** No duplicar posiciones; esperar nueva señal tras nueva Vela M1 que cumpla Setup.  
   - *Nota:* Todos los cálculos se basan en precio de cierre/anterior; no dependemos de “ojimetría”. _(PROPUESTA)_  

2. **Ficha ORB + Momentum:**  
   - **Setup:** Definir rango de apertura (ORB): máximo y mínimo de primeras 15 velas M1 (9:30–9:45).  
   - **Filtros:** Si rompe ORB superior (cierre vela 16 > máximo ORB) con Volumen(15)<umbral (poca operación inicial), señal *alcista*. Si rompe inferior con condiciones similares, señal *bajista*.  
   - **Entrada:** Tras vela de ruptura, entrar en la siguiente vela.  
   - **Stop/Objetivo:** Stop a la brecha anterior del ORB o fijo 2 ticks, target a 2×stop. Riesgo fijo 1 contrato NQ.  
   - **Reentrada:** Si se cierra posición (stop o target), esperar nuevo ORB para próxima sesión. _(PROPUESTA)_  

3. **Ficha Mean Reversion Intradía:**  
   - **Setup:** En vela M1, precio desvía ≥ 0.75×ATR(14) *sobre* o *bajo* el VWAP del día.  
   - **Filtro:** Hora de bajo volumen (12:00–13:30); asegurar mayor probabilidad de rebote.  
   - **Entrada:** Si precio cae ≥0.75 ATR bajo VWAP, entrar largo; si sube ≥0.75 ATR sobre VWAP, entrar corto.  
   - **Stop/Objetivo:** Stop = 1.0×ATR lejos de entrada; Target = vuelta al VWAP (fácilmente verificable).  
   - **Reentrada:** No reentrar en misma sesión al alcanzar target; perma-stop hasta siguiente señal (nueva desviación). _(PROPUESTA)_  

Cada ficha expresa condiciones formales (no visuales). Producen una secuencia de señales “señal=1 compra, -1 venta, 0 sin trade”. La gestión de tamaño y vetos (MM actual) se aplica después, no como parte de la señal.

# Métricas definidas  

Definimos métricas en cuatro niveles: trade, cuenta, campaña, cartera:  

- **Por trade:**  
  - Expectancy `E = P(win)×AW – P(loss)×AL`, con *AW* y *AL* como ganancias/pérdidas medias. Indica edge financiero. (HECHO)  
  - *Profit Factor* `PF = \tfrac{\text{Beneficio bruto}}{\text{Pérdida bruta}}`. PF>1 indica ganancia neta, PF>2 estilo institucional. (HECHO)  
  - Win rate (%W) y Asimetría `AW/AL`. (HECHO)  
  - *MAE (Max Adverse Excursion):* desviación máxima en contra antes de cierre. Mide precisión de entrada. (HECHO)  
  - *Trade Duration:* tiempo (minutos) hasta target o stop. Muestra capital inmovilizado. _(PROPUESTA)_  

- **Por cuenta:**  
  - *Retorno CAGR / Máx Drawdown (Calmar)*: Calmar = CAGR / MaxDD. Enfoca sobre riesgos de drawdown (útil en challenges) (HECHO).  
  - *Sharpe Ratio:* media de retornos/(desv. stándar), cuidado con colas pesadas (REFERENCIA). (HECHO)  
  - *Drawdown máximo (%):* diferencia pico-valle de equity. (HECHO)  
  - *Solidez de la distribución:* curtosis, VaR 5% (cola). (PROPUESTA)  

- **Por campaña:**  
  - *Pase (%)*: proporción de cuentas simuladas que cumplen objetivo sin estallar la pérdida máxima. (PROPUESTA)  
  - *Retiro neto esperado:* media de retiro tras pagar cuotas. (PROPUESTA)  
  - *Costo por pase:* suma de cuotas gastadas / no. pases (incluye reintentos fallidos). (PROPUESTA)  

- **Por banca/global:**  
  - *Drawdown de banca:* flujo neto de caja (contratos y retiros). (PROPUESTA)  
  - *Probabilidad financiar próximo intento:* función estadística de PnL neto tras N reintentos fallidos. (PROPUESTA)  
  - *Exposición simultánea:* exposición combinada de estrategias por dirección/región (ej. sumatoria de riesgos activos). (PROPUESTA)  

Para cada métrica definimos fórmula, denominador y umbral aceptable. Por ejemplo, *PF* usa dólares ganados/perdidos; *Expectancy* mezcla % y montos. Separaremos métricas puramente de trade vs de cuenta/campaña (p.ej. Pass Rate) vs de cartera (correlación, pérdida agregada). 

# Comparación señal vs MM/RuleSets  

Para probar configuraciones de MM, congelamos la señal “pura” (los puntos de entrada posibles sin MM) y luego aplicamos distintas gestiones de riesgo. Esto preserva las oportunidades originales: no eliminamos una señal como "absorbida", sino que la registramos como veto o cambio de contrato. Por ejemplo, si la regla actual exige **1 NQ mínimo** de riesgo, una señal de 0.5 NQ se marca como *vetada* (conversión implícita a no trade). No modificamos stops internos ni cambiamos a MNQ “silenciosamente”; debemos probar escenarios con y sin la restricción de 1 NQ. Se compara el resultado (p.ej. equity, pases) manteniendo la cantidad original de operaciones vetadas vs activadas. 

Registramos: señales originarias, cierres pedidos, fills reales según ordenes, y salida del MM (posición o rebote por regla). No tratamos la muestra filtrada por MM como señales independientes: las referimos como subset condicionado. Esto mantiene consistencia en métricas de frecuencia y evita sesgo de selección.

# Validación temporal y selección  

Proponemos una validación *walk-forward* con bloqueo temporal para evitar fuga de datos: se divide la historia en Periodos de Descubrimiento (para hipotetizar y calibrar reglas), Selección (para filtrar parámetros y reglas), y Confirmación Out-Of-Sample (para evaluar performance final). Cada tramo debe simular un intento de challenge nuevo. No reutilizar datos seleccionados para testing posterior (protección de datos futuros). 

Además se controla el *sobreajuste* por múltiples pruebas. Se registra cada combinación probada (*trial*), tal como en “Probability of Backtest Overfitting”. Un aumento no moderado en pruebas aumenta la probabilidad de un hallazgo espurio. Podemos aplicar métodos de ajuste estadístico (p.ej. Sharpe deflacionado) o tests robustos (cross-validation aleatorio de parámetros). Si el muestreo es escaso (pocos trades), declaramos resultados *condicionales* – no usamos “cocientes mágicos” de trades mínimos ni relajamos requisitos G0–G5 por rareza. 

# Límites de datos (OHLC M1)  

Trabajando con velas de 1 minuto, ciertas órdenes son ambiguas: un stop o target puede invocarse cualquier momento intravela. Por ello, al simular:  
- **Fill de stops/targets:** Si un stop (=nivel X) queda entre `Low` y `High` de la vela, asumimos fills al nivel extremo de la vela (pesimista o conservador). No hay garantía intrabar de ejecución exacta.  
- **Spreads y slippage:** Se deben incluir *estimaciones* de spread/latencia. Un *retardo de mercado* puede hacer que órdenes ejecuten al siguiente precio de oferta. Este costo (espera, slippage) “come” el edge real.  
- **Gaps:** Entre cierres diarios puede haber salto de precio; sin datos tick, no simulamos órdenes abriendo por gap (caso ambiguo). Se podría descartar o imputar conservadoramente al nivel abierto.  
- **Trailing stops:** Usar el máximo previo de equity se complica sin datos tick. Podríamos usar `High` intravela, pero reconocer que picos reales podrían haber sido mayores; así tratamos trailing equity de forma conservadora.  

Clasificamos casos resolubles (ambos stop y target fuera del rango [High,Low]) y ambiguos (atravesando). Para lo último, usamos bounds conservadores: asumir la peor ejecución (stop al máximo Favorable, target al mínimo Adverso, etc). En resumen, usar M1 introduce error; idealmente se necesitaría tick o un modelo de mercado micro para mayor exactitud. Hasta ese nivel, trabajamos con supuestos realistas y señalamos la incertidumbre de simulación (desconocido preciso). (INFERENCIA/PROPUESTA)  

# Medidas de cartera y riesgo conjunto  

Finalmente, definimos métricas de portafolio:  
- **Señales comunes:** Porcentaje de veces que dos estrategias emiten señales simultáneas o de misma dirección.  
- **Pérdidas combinadas:** Max Drawdown conjunto de la cartera (mismo drawdown en varias estrategias).  
- **Exposición direccional:** tiempo activo neto por dirección (longs vs shorts totales).  
- **Dependencia de colas:** cuán correlados son los eventos extremos (p.ej. VaR conjunto). Podemos usar copulas o medidas de *copdep* entre P&Ls.  
- **Sequías sincronizadas:** probabilidad de que todas (o N de M) estrategias fallen consecutivamente en un período. Esto afecta tiros de capital.  
- **Simultaneidad de retiros:** potencial de necesitar efectivo simultáneo (ej. varias estrategias exigen retirada en similar timeframe).  

Recordar que **dos firmes con mismo subyacente NQ** no son independientes: las colas se pegan. Se debe incluir cualquier restricción de hedge (p.ej. límites del desafío sobre correlaciones) que dicten contratos, no asumir libre combinación. (PROPUESTA)  

# Protocolo comparativo futuro  

Proponemos un protocolo de comparación: mantener señal base fija, probar distintos *políticas agresivas* (e.g. apalancamiento 2x, stops más amplios) frente a la base. Sin optimizar parámetros, simplemente variar agresividad de sizing/MM en paralelo. Registrar resultados de campañas hipotéticas. Cualquier conclusión será de hipótesis ("si esto, entonces aquello"), no definitiva.  

**No ejecutamos** simulaciones reales ni modificamos Engines existentes. En esta etapa elaboramos solo esquema: definir rangos de parámetros (p.ej. % riesgo por trade: 1% vs 2% vs 0.5%) y diseños de experimentos. Compararemos resultados por métricas definidas y aplicaremos tests de refutación (por ejemplo, haríamos pruebas de permutación de señales para calibrar PBO). Todo quedaría listo para el siguiente paso (DR-05). (PROPUESTA)  

# Límites pendientes y próximas decisiones  

Lo anterior es realizable *sin* esperar los resultados de DR-01/02/03 en cuanto a la señal base y datos: podemos definir indicadores, estrategias y métricas generales. Sin embargo, el **ajuste fino** de parámetros, niveles de filtro y licencias de riesgo queda condicionado a esos reportes. No bloqueará el avance conceptual, pero la validación práctica requiere los datos ahí obtenidos (p.ej. probar qué filtros brindan probabilidad de pase rentable).  

**Siguiente paso investigable:** realizar un primer experimento piloto con una estrategia de ejemplo (p.ej. Trend-Breakout) usando datos históricos OHLC 1m NQ, aplicar MM básico (1% riesgo) y comparar con una política agresiva (2% riesgo) para observar diferencias de métricas de campaña (pase, drawdown, retiros). Esto nos permitirá calibrar expectativas sin optimizar parámetros. 

**Fuentes:** referencias técnicas y académicas se citan arriba. Cada fórmula o afirmación marcada (HECHO/INFERENCIA/PROPUESTA/DESCONOCIDO) refleja si está directamente sustentada o propuesta de forma razonada. En particular, las fórmulas de *Expectancy* y *Profit Factor* se tomaron de la literatura de prop traders; la necesidad de validación cruzada y cuidado con backtests se sustenta en estudios de *overfitting*; los límites de simulación emulan recomendaciones de manejo de costos y latencia. 

**Retorno:** DR-04 | RESPONDIDO | protocolo | métricas | fichas | límites de datos | interfaces | próxima decisión.
