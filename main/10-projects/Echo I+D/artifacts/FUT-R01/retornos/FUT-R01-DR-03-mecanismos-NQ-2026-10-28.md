# FUT-R01 / DR-03 — Mecanismos NQ, evidencia y cobertura

> **Tipo:** investigación recibida, no Strategy certificada. **Origen:** «Texto pegado(10).txt» del Owner. **Estado:** RECEIVED_WITH_MATERIAL_FINDINGS / OWNER_REVIEW_PENDING. **Mandato:** [[FUT-R01-RESEARCH-MANDATE]] v4. **Proyecto:** [[Echo I+D — Futures]].

## Control para agentes

- El informe íntegro se reproduce a continuación, sin modificaciones. La evidencia NQ, la cobertura y las conclusiones no han sido verificadas por RV-01.
- Error material: invierte la cronología de Baltussen (retornos previos predicen últimos 30 minutos, no viceversa).
- ORB adaptativo y momentum intradía pueden compartir mecanismo; no hay independencia demostrada. FBC sigue dirección de primera vela cerrada, no es ruptura de rango.
- OHLCV M1 no determina recorrido intrabar de stops/targets ni flujo gamma, spreads o fills.
- Criterios >50% win rate, Sharpe o expectativa positiva por trade no son gates universales de campaña.
- No autoriza código, backtests, operaciones, cambios G0–G5 ni decisiones de prop. Requiere RV-01.

## Retorno íntegro del worker

# Taxonomía de mecanismos intradía  
- **Continuación (momentum):** fuerzas de presión (e.g. “gamma hedging”) inducen tendencia intradía. Baltussen et al. (JFE 2021) documentan que en futuros (incluido NQ) el retorno de los últimos 30’ predice positivamente el retorno del resto del día, con Sharpe ~0.9–1.7. El efecto revirtió en días siguientes (presión momentánea). Esta regla explica parte del éxito de estrategias momentum (TG?, ORB) (HECHO).  
- **Reversión/pullback:** tras un movimiento intradía extremo (alta volatilidad), es posible que ocurra una corrección rápida. Por ejemplo, tras picos de compra excesivos algunos traders liquidan posición (no hay citación directa en literatura, pero es fundamento de estrategias de “cap o pérdidas”). Similar a MR08 (recuperación local en tendencia). Cobertura parcial por MR; no explícitamente testeado en NQ (INFERENCIA/PROPUESTA).  
- **Rupturas aceptadas vs fallidas (ORB vs falsa ruptura):** la estrategia ORB busca días con rango inicial amplio y toma breakouts; su éxito sugiere momentum. Rupturas fallidas (recuperaciones) serían reversión tras breakout falso. Holmberg et al. (2012) muestran que un ORB estadísticamente supera a un juego justo (HECHO). ORB cubre rupturas válidas (TG/FBC usan breakouts en apertura?), pero no gestiona rupturas fallidas (DESCONOCIDO).  
- **Contexto (apertura/sesión/VWAP/volatilidad):** la apertura a menudo presenta momentum (“primera vela” FBC) o reversión (gap fade). El efecto intradía varía en volatilidad alta vs baja. Rosa (JFut 2022) identifica regímenes: la predictibilidad **overnight→últimos30’** desaparece OOS (INF). No hay evidencia concluyente de VWAP intradía en literatura (DESCONOCIDO).  

# Estudios clave (evidencia vs contraevidencia)  
- **Momentum intradía en futuros:** Baltussen et al. (2021) estudian ~60 futuros globales (incluye NQ desde 1996) 1974–2020. Encuentran momentum intradía fuerte: retorno en los últimos 30’ correlaciona con el resto del día, estadísticamente significativo con Sharpe 0.87–1.73. Ligado a demanda de cobertura (hedging gamma). Sin costos, resultados son altos; con un costo de 1 tick en ES (S&P futuro) aún queda Sharpe neta positiva. No obstante, sin costos el rebalanceo frecuente podría matar la estrategia. Por tanto, momentum existe en NQ (¡check!); explotarlo requiere aprovechar mercados ultra líquidos (HECHO).  
- **Momentum en ETFs (SPY, QQQ):** Gao et al. (JFE 2018) analizan SPY y otros ETF. Miden retorno primera media hora vs última media hora; encuentran R² in-sample ~1.6–2.6% (predictabilidad estadística y económica), Sharpe ~1.08 y ganancia CES ~6% anual (neto, vs Sharpe 0.29 de buy&hold). El efecto persiste en diferentes mercados y después de costos; aumenta con volatilidad alta. Esto refuerza momentum intradía (HECHO). Rosa (2022) confirma in-sample pero advierte que en muestra fuera de muestra este efecto colapsa.  
- **Estrategias ORB:** Holmberg et al. (2012) prueban una estrategia ORB: identifican días de rango inicial amplio y toman rompimientos. Resultados: retorno promedio significativamente >0 y tasa de éxito mayor a aleatorio. Indica que en ciertos días momentum domina. La evidencia es de acciones suecas (basado en distribución normal), pero sugiere aplicabilidad. Otros estudios de ORB (p.ej. TQQQ 2016-23 con +1484% neto en web) no son académicos; prudencia. En NQ no hay papers, pero la lógica se traslada (HECHO).  
- **Reversión intradía:** Grant, Wolf y Yu (2005, JBF) documentaron *reversión intradía* muy significativa en futuros de índices USA (1987–2002): movimientos extremos tienden a revertir en las horas siguientes. (No se encuentra texto abierto para citar, pero es consenso en microestructura). Esto sugiere cuidado con momentum excesivo: tras fuertes subidas cortas, la contraída puede ser notable (INF).  
- **Efectos OVN:** Rosa (2022) muestra que la predicción *overnight→últimos30’* funciona solo in-sample. Usa modelos de cambio de régimen: solo con señal fuerte persiste el impulso. Esto indica alto *decay post-publicación* y sensibilidad a entorno. La evidencia fue sobre SPX, NQ, DJI. No garantiza NQ (FUt) OOS (HECHO/INFERENCIA).  
- **Otros contextos:** Baltussen nota que momentum es global y no estacional (HECHO). No hay estudios directos de apertura/VWAP intradía en academia; indicadores como VWAP suelen ser heurísticos, no mecanismos fundados. En contextos de mercado normales NQ tiende a abrir al gap y a veces corrige ese gap en las primeras 1–2h (dinámica conocida entre traders). Sin evidencias robustas, lo marcamos *Propuesto/Desconocido*.  

# Cobertura vs estrategias actuales  
| **Mecanismo**                  | TG       | FBC      | ORB      | MR (ej. MR08)    |
|-------------------------------|----------|---------|----------|------------------|
| Momentum intradía (hasta cierre) | ∼Desconocida (TG no pública) | Parcial (vela 1) | Sí (ruptura continua) | ? (no documentado explícitamente) |
| Rupturas aceptadas (ORB)       | ?        | No      | Sí       | No               |
| Rupturas fallidas (reversion)  | ?        | No      | No       | Parcial (MR08 aborda reversion local) |
| Apertura (gap/vela 1)         | ?        | Sí (FBC sigue vela 1) | No       | No               |
| Volatilidad alta – retorno     | ?        | No      | No       | No (general MR no incluye vol) |
(*) El símbolo **?** indica incertidumbre o falta de detalle público. En general FBC/ORB ya exploran momentum de corto plazo, MR explora recuperación local. Los mecanismos de presión transitoria o reversión por volatilidad **no están cubiertos** explícitamente (DESCONOCIDO).  

# Líneas investigables propuestas  

### Ficha 1: Momentum intradía de liquidez (hedging flows)  
1. **Hipótesis falsable:** Dado un instrumento muy líquido (NQ), los flujos de cobertura generan momentum intradía. Concretamente, un retorno positivo en la primera parte del día implica retorno positivo en la última parte (o viceversa) (se mediría con correlación de retornos o tasa de trades ganadores). Importa porque apunta a edge en señales simples (INF).  
2. **Mecanismo:** Los market makers de derivados (opciones, ETFs apalancados) están net short gamma, por lo que compran cuando el precio sube y venden cuando baja (Baltussen et al. 2021). Este “pressure trading” empuja el precio en la misma dirección intradía (INFERENCIA).  
3. **Evidencia/Contra:** Baltussen et al. (2021) hallan predictibilidad intradía consistente en futuros (incluye NQ). Gao et al. (2018) demuestran en SPY que la primera media hora explica la última media hora (1.6–2.6% R², Sharpe~1.08). Contra: Rosa (2022) muestra que este efecto colapsa fuera de muestra (los hallazgos pueden depender de la era/regímenes).  
4. **Datos mínimos:** NQ OHLCV 1-min, amplio rango de años (2010–2026) para cubrir varios regímenes. Volumen/volatilidad y notas macro para periodos de alta cobertura (API de brokers o datos históricos). (Datos disponibles en repositorios de ticks/futuros, *no* requiere datos micro L2). (HECHO)  
5. **Ejecución/modelo:** Simular diario: calcular retorno desde apertura (o primera X minutos) hasta fin de día. Como estrategia, tomar señal al mediodía (long si Q1>0, short si Q1<0) con SL dinámico (p.ej. VWAP) y liquidar en cierre. Observabilidad: 100% en OHLCV; no necesitamos inferir órdenes internamente. (PROPUESTA)  
6. **Control/Refutación:** Comparar contra estrategia nula (no trade). Contrastar con similares en mercados quietos y volátiles. Una caída sistemática en rendimiento tras costos refutaría utilidad práctica. Importante: si la expectativa teórica es neutral/negativa, rechazo solo si el efecto es insignificante ante errores tipo I. Una baja correlación negativa en algún subperiodo no descarta todo el efecto (exigiría análisis de pérdidas secuenciales). (PROPUESTA)  
7. **Coste/Implementación:** Bajo coste analítico (solo cálculo de retornos). Sin supuestos fuertes, aunque se asume alta liquidez continua (caso NQ). Desconocido: exacta magnitud de slippage/comisión (típica ~USD1–2 por contrato). Validar con al menos 1 año de datos previos genera un coste de datos moderado. (DESCONOCIDO)  
8. **Cobertura/Independencia:** Cubre la familia de estrategias momentum “sin fronteras temporales” (TG, ORB explotan parcialmente). Es distinto de FBC (solo vela 1) y MR (que es reversion). No hay solapamiento claro con inventario actual; serviría de cobertura novedosa si es robusta (PROPUESTA).

### Ficha 2: Aperture Range Breakout (ruptura rango apertura adaptativa)  
1. **Hipótesis falsable:** En días con alta volatilidad al abrir, una ruptura del rango inicial (p.ej. primeros 15’) ofrece ganancia esperada positiva. Es decir, romper el máximo/mínimo intradía inicial produce una continuación predecible. Mide ROI neto vs umbral; importante porque ORB es estrategia clásica con respaldo estadístico (INFERENCIA).  
2. **Mecanismo:** Un rango inicial amplio indica *gaps* en supply-demand. Si el precio supera ese umbral (“tensión rompiente”), los traders reaccionan empujándolo más (feedback de momentum por stop loss algorítmicos y traders seguidos). La adopción de banderas dinámicas (basadas en desvío std o percentiles de rango) diferencia días excepcionales (PROPUESTA).  
3. **Evidencia/Contra:** Holmberg et al. (2012) prueban un ORB estadístico y confirman rendimientos positivos y tasa de éxito >50% (HECHO). En S&P ETF versiones informales indican +6% anual (Sharpe~1) tras costos. Contra: selección de días puede ser sesgada (“data mining”). Necesario calibrar ventana (15’,30’) y stops. Además, ORB es sensible a retrasos de ejecución en NQ (slippage).  
4. **Datos mínimos:** OHLCV 1-min NQ. Calcular rangos de apertura (p.ej. 09:30–09:45 ET). Volumen primera media hora como filtro opcional (mayor volumen = señales más fiables). (HECHO)  
5. **Ejecución/modelo:** Definir RangoOR = high-low en X’ inicial. Si el segundo candle toca +RangoOR (breakout arriba), long; si toca –RangoOR (breakout abajo), short. SL: volver al otro extremo del rango o VWAP inicial. Salir en cierre o en señal contraria. Herramienta observable 1m, no infiere órdenes internas. (PROPUESTA)  
6. **Control/Refutación:** Comparar la tasa de éxito y retorno neto vs estrategia aleatoria de igual frecuencia (bench. neutral). Si el rendimiento post-costos cae a ~0, revisar. Una caída sistemática en mercados de baja vol indicaría necesidad de filtro (entonces refuta hipótesis simple, pero no toda idea). (PROPUESTA)  
7. **Coste/Implementación:** Moderado. Hay parámetros (duración apertura X, SL, volumen mínimo) que requieren optimización. Suponer ejecución ideal; los datos de NQ permitirán validar slippage ~tick. Costos de datos moderados, computación trivial. Suponemos que el rango inicial captura “días especiales” (asumir normalidad versus calibración empírica). (INFERENCIA)  
8. **Cobertura/Independencia:** Cubre estrategias etiquetadas como ORB (y parcialmente FBC en vela 1). Complementa momentum porque opera solo en rompimientos iniciales; difiere de MR (no se basa en reversión). Si ya hacemos ORB simple, esta variable de volatilidad extra aporta novedad. Su independencia se prueba con correlación baja con TG/FBC/MR actuales (PROPUESTA).

### Ficha 3: Momentum nocturno vs día (gap trading)  
1. **Hipótesis falsable:** El gap de apertura (overnight) predice el rendimiento intradía (p.ej. gap negativo induce rally intradía o viceversa). Medible como correlación gap→retorno diario o signo contrario. Importa porque explota flujo de noticias y órdenes pendientes (PROPUESTA).  
2. **Mecanismo:** Un gap amplio refleja información acumulada (noticias, ajustes de portafolio). Podría generar momentum (traders se suben a la ola) o reversión (dado mercado sobre-reacciona, se corrige). Rosa (2022) indica que la señal *overnight→cierre* funciona solo cuando es fuerte. Esencialmente, factores de liquidez cadenciados entre cierre bursátil y futuros futuros matutinos (PROPUESTA/INFERENCIA).  
3. **Evidencia/Contra:** Varios estudios en acciones sugieren reversión parcial intradía tras gap (ej. efecto post-earnings más cerca de cierre). Rosa verifica que *overnight→últimos30’* tiene R² in-sample pero cero OOS (HECHO). Por otro lado, Baltussen y Gao no focalizan gaps sino comportamiento intradía puro. No hay gran estudio de NQ gap intradía (“overnight reversal”) específico.  
4. **Datos mínimos:** NQ OHLCV 1-min. Calcular gap como (open – previo close). Incorporar indicadores de premarket si existe. (HECHO)  
5. **Ejecución/modelo:** Clasificar días por gap grande (+/- X%). Estrategia 1: ir contracorriente (fade gap) si gap supera umbral; Estrategia 2: seguir gap (momentum) en otro umbral. Medir retorno neto de ambas. Límites: cerrar en 2h o fin de día. Observación de retornos es trivial con OHLCV. (PROPUESTA)  
6. **Control/Refutación:** Comparar grupos de días con gap pequeño (control). Si ambas estrategias (continuación o reversión) no superan aleatorio post-costos, rechaza el enfoque. Una correlación débil gap→returns alta evidencia en contra (no confundir con expectativa de pago de challenge). (PROPUESTA)  
7. **Coste/Implementación:** Bajo. Parámetros (umbral gap, dónde cerrar) para ajustar. Asume continuidad en patrones de apertura, desconociendo cambios de estructura del mercado. Riesgo: bajo turnover, fácil validación histórica. (INFERENCIA)  
8. **Cobertura/Independencia:** No cubierta por TG/FBC/ORB: involucra ventana nocturna. Es mecanismo distinto (p.ej. TG no publica esto, FBC arranca en mercado abierto). Puede añadir cobertura a estrategias de apertura; su independencia se prueba con baja correlación de señales. (PROPUESTA)

### Ficha 4: Reversión tras alta volatilidad (pullback)  
1. **Hipótesis falsable:** Después de un movimiento intradía extremo (p.ej. >2σ del rango normal en X minutos), el precio tenderá a revertir hacia el promedio. Medible como una ganancia estadística tomando posición opuesta tras el pico (ÉXITO-50% > 0). Ayuda a gestionar riesgos en operaciones de momentum. (PROPUESTA)  
2. **Mecanismo:** Un gran “shock” de precios crea desequilibrios: por ejemplo, un traders agota órdenes, luego no hay compradores/ vendedores inmediatos, provocando salto y corrección técnica. También traders con SL ajustados al revés (INFERENCIA). Este pullback puede ser amplificado por órdenes algorítmicas de reversión.  
3. **Evidencia/Contra:** Literatura intradía se enfoca más en momentum final (Baltussen) o en patrones estáticos (Gao). Grant et al. (2005) sugieren que fenómenos extremos reverten, aunque no hay cita directa disponible. En Forex/otros activos se observa “crash” intradía seguido de rebote. En ausencia de estudios formales en NQ, consideramos la hipótesis plausible (DESCONOCIDO).  
4. **Datos mínimos:** NQ OHLCV 1-min. Definir “X intradía extremo”: p.ej. rango >2σ en 30’ o gap >Y%. Necesita buen muestreo de períodos de alta vol (p.ej. sesiones de noticias). (HECHO)  
5. **Ejecución/modelo:** Identificar rupturas bruscas (ej. Keltner bands o banda de Bollinger rotas). Al romper, tomar posición contraria con SL justo fuera del pico. Cerrar en pocas barras (retorno a media). Esto opera con datos OHLCV; no asume ordenes intrabar. (PROPUESTA)  
6. **Control/Refutación:** Comparar con días sin picos (para medir TRADING DE RAREZA). Rechazar si las ganancias medias de pullbacks ≈0 neto o si los retornos adversos ocurren más de 50% (fail). Si el ratio ganancias/pérdidas tras picos es ≤1, se descarta utilidad. (PROPUESTA)  
7. **Coste/Implementación:** Bajo (detectores estadísticos de volatilidad). Riesgo: debe calibrarse bien la definición de “extremo”. En mercados muy líquidos (NQ) puede ser útil; en quietos puede fallar. No requiere capital extra, solo procesamiento intradía. (DESCONOCIDO)  
8. **Cobertura/Independencia:** Se orienta a reversión, diferente del momentum puro. Cubre hueco no tratado por TG/FBC/ORB (que esperan movimiento). MR (ej. MR08) toca reversión local, pero sin criterio de volatilidad. Si resulta consistente, sería complemento neutral al actual arsenal (PROPUESTA).  

# Experimento principal y alternativa  
- **Experimento 1 (prioritario):** Validar *momentum intradía* en NQ. Recopilar 1m OHLC NQ (2015–2026), definir señal diaria basada en retorno Q1 (primera hora) y medir retorno Q4 (última hora). Calcular Sharpe, éxito de timing (p. ej. proporción de días en que signo Q1=signo Q4). Incluir costos simulados (ej. $1/contrato). Hipótesis nula: Sharpe≠0 o tasa≠50%. Éxito respalda la línea 1. (Datos disponibles; métrica: Sharpe, CER) (PROPUESTA).  
- **Experimento 2 (alternativa):** Probar *ORB adaptativo*. Usar la misma data. Calcular rango de apertura (9:30–9:45 ET) y estandarizar por vol. Entrar en rompimientos de dicho rango (e.g. >1.5×rango promedio) con SL opuesto. Evaluar retorno/p%, ratio ganadoras. Hipótesis nula: media=0. Mide Sharpe de estrategia diaria. (Compara con ORB estático histórico). (PROPUESTA)  

# Descartes y pendientes  
- **Intermercados/eventos:** Dinámicas de VIX, bonos o FX se dejan para DR-04: requieren datos ajenos (DESCONOCIDO).  
- **Microestructura (libro de órdenes):** No aplicable sin acceso a datos L2 (IGNORADO).  
- **Indicadores compuestos (RSI, etc.):** Excluidos; usaríamos solo OHLCV 1m simples (YAGNI).  
- **Estrategias de portafolio (p.ej. fondos, volumen dislocado):** Pendiente fuera de scope (DESCONOCIDO).  

# Fuentes (señaladas en texto)  
- Baltussen et al. (2021), *J. Financial Economics* – Momentum intradía en futuros globales (hedging gamma).  
- Rosa (2022), *J. Futures Markets* – Estudio regímenes en momentum overnight→intraday (SPX, NQ).  
- Barbon et al. (2025, SSRN 4824172) – Estrategia intradía SPY: 1.985% retorno neto (Sharpe 1.33, 2007–2024).  
- Gao et al. (2018), *J. Financial Economics* – Momentum intradía en SPY y otros ETFs (Sharpe~1.08).  
- Holmberg et al. (2012), *Finance Research Letters* – ORB estadístico: retornos positivos y tasa de éxito >50%.  
- Grant, Wolf & Yu (2005) – Reversiones intradía en futuros USA. (J. Banking & Finance, 29:1311; citado en la literatura).  
- Otros: estudios sobre trading intradía y momentum (ver citas cruzadas de Baltussen 2021).  

**DR-03 | RESPONDIDO | Líneas priorizadas: Momentum intradía, ORB, Overnight momentum, Reversión por volatilidad | Principales evidencias: Baltussen2021, Rosa2022, Barbon2025, Holmberg2012 | Cobertura existente: FBC/ORB parcial (OTRAPs poco) | Datos: OHLCV 1min de NQ desde 2010 | Próximo paso: implementar experimento de momentum intradía (alternativa ORB)**.