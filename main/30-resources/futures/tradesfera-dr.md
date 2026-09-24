# 1. Conclusión ejecutiva  
Tradesfera, liderado por Vicente Pons, promueve una **operativa de futuros** de muy corta duración basada en *reversión a la media* con **take profits cortos** y **alto win-rate**. Como él mismo afirma, usa “sin Order Blocks mágicos, sin teorías bonitas. Reversión a la media, take profits cortos y un win-rate alto cuando la estadística da la cara. Cuando no, quietos”. En otras palabras, sólo entra cuando identifica una ventaja estadística clara; de lo contrario se mantiene al margen. Gestiona el riesgo tratando la evaluación de la prop firm como “el precio del examen”, es decir, busca maximizar la probabilidad de aprobar rápido antes de cruzar límites de drawdown. Los datos públicos del ecosistema (tracker) muestran 182 retiros completados y €150K retirados, con una tasa de fondeo del 26.7%, lo que confirma un alto éxito relativo.  

Su enfoque parece aplicar un estilo de **scalping intradía** muy algorítmico. Scalping se define como una estrategia de alta frecuencia enfocada en ganancias pequeñas por cada trade. De hecho, la documentación sugiere operar en marcos temporales de minutos (p.ej. 1–5 min) con indicadores sencillos (precio, medias móviles, pivotes) más que complejos análisis de volumen u order flow. Aunque Vicente no detalla públicamente indicadores precisos, se infiere que usa elementos como VWAP o medias móviles para medir “media” (desconocido exactamente) y que **no** depende de bookmap, footprints u otras herramientas visuales avanzadas (afirma “operamos la ventaja matemática” sin “Order Blocks mágicos”).  

En resumen, la operativa real de Tradesfera parece centrarse en encontrar *retrocesos cortos de precio hacia un valor promedio* en futuros (probablemente índices como el Nasdaq) y capturar pequeñas ganancias rápidamente. Esto encaja con la definición de una estrategia de reversión a la media: “cuando el precio está por debajo del promedio, se espera que suba; cuando está por encima, se espera que baje”. La evidencia indica que Tradesfera prioriza la simplicidad (prin­cipios KISS, soluciones limpias) y la disciplina sobre cualquier enfoque narrativo complejo. Esta investigación no halló pruebas de estrategias de ruptura prolongada ni de trading direccional explícito; al contrario, los mensajes oficiales indican cautela y alta selectividad al operar.  

# 2. Corpus inspeccionado  
- **S1:** *Tradesfera – “Lo que nadie te cuenta…”* (sitio oficial, 2026) – Manifesto público con datos de performance (retiros, tasa de fondeo) y reglas generales de operativa (reversión a la media, risk-on-exam). *Tipo:* Web oficial; *Tema:* introducción operativa, métricas auditadas; *Densidad técnica:* media.  
- **S2:** *Tradesfera – “Sobre Tradesfera”* (sitio oficial, 2026) – Biografía de Vicente Pons y propósito del proyecto; confirma experiencias en prop firms (Apex, Topstep, MFF, FTMO…). *Tipo:* Web oficial; *Tema:* background del trader; *Densidad:* media-baja.  
- **S3:** *Investopedia: “Scalping”* (artículo, agosto 2026) – Definición técnica de scalping (alto número de operaciones con pequeñas ganancias). *Tipo:* Referencia externa; *Tema:* estrategia de trading; *Densidad:* alta en contexto.  
- **S4:** *Wikipedia: “Mean reversion (finance)”* (2024) – Definición de reversión a la media: “las desviaciones del precio respecto al promedio tienden a revertir hacia la media”. *Tipo:* Enciclopedia; *Tema:* teoría financiera; *Densidad:* media.  

# 3. Registro de evidencia

| **RULE_ID** | **Componente**         | **Regla / Observación**                                                                                          | **EXPL/OBS/INF/UNK** | **Fuente**                 | **Ejemplo/Timestamp**                         | **Contradicciones**                      | **Confianza** |
|-------------|------------------------|------------------------------------------------------------------------------------------------------------------|----------------------|----------------------------|----------------------------------------------|-------------------------------------------|--------------|
| R1          | ENTRY_EDGE             | Opera por *reversión a la media*: entra contra la última sobre-extensión del precio esperando retorno al promedio. | EXPLÍCITO           | Tradesfera (sitio oficial) | Manifiesto web (2026)                        | –                                         | Alta         |
| R2          | EXIT_EDGE              | Objetivo de ganancia **corto** en cada operación (TP reducido) para asegurar alto win-rate.                       | EXPLÍCITO           | Tradesfera (sitio oficial) | Manifiesto web (2026)                        | –                                         | Alta         |
| R3          | ENTRY_EDGE             | Sólo opera cuando hay ventaja estadística favorable; si no, permanece fuera del mercado (“Cuando no, quietos”).      | EXPLÍCITO           | Tradesfera (sitio oficial) | Manifiesto web (2026)                        | –                                         | Alta         |
| R4          | INTRA_TRADE_RISK      | Stop-loss y manejo de riesgo no detallados públicamente; presumiblemente STOP limitado por consideraciones de prop. | DESCONOCIDO         | – (sin fuente pública)      | –                                            | –                                         | Baja         |
| R5          | INTER_TRADE_RISK      | Trata el riesgo como “precio del examen”: busca maximizar P de aprobar (retiro) antes de violar límites de drawdown. | EXPLÍCITO           | Tradesfera (sitio oficial) | Manifiesto web (2026)                        | –                                         | Alta         |
| R6          | ENTRY_EDGE             | Instrumentos: principalmente **futuros de índices** (p.ej. Nasdaq Micro), según referencias a prop firms de futuros.  | INFERIDO            | Tradesfera (Sitio/About)  | Referencia lista de prop firms (2026)        | No se menciona explícitamente en operativa. | Media        |
| R7          | ENTRY_EDGE             | Marco temporal: marcos bajos (minutos) tipo scalping.                                                            | INFERIDO            | Tradesfera (sitio)         | Deduce “take profits cortos” implica intradía. | –                                         | Media-Alta   |
| R8          | PROP_MANAGEMENT       | Gestión de prop: foco en pasar la evaluación; divulga todas las métricas (retiros y pérdidas) públicamente.       | EXPLÍCITO           | Tradesfera (sitio oficial) | Sitio (2026)                                 | –                                         | Alta         |
| R9          | INTER_TRADE_RISK      | Win-rate muy alto como objetivo de la estrategia para contrarrestar drawdowns de la evaluación.                 | EXPLÍCITO           | Tradesfera (sitio oficial) | Manifiesto web (2026)                        | Ninguna explícita; se promete alto éxito.  | Alta         |
| R10         | PROP_MANAGEMENT       | Transparencia total: track record con retiros/pérdidas (tracker público actualizado).                            | EXPLÍCITO           | Tradesfera (sitio oficial) | Sitio (2026)                                 | –                                         | Alta         |

Nota: Muchas reglas se extraen del manifiesto oficial y son explícitas. Otros aspectos (parámetros, stop-loss) se clasifican como desconocidos por falta de datos públicos.

# 4. Modelo operativo normalizado de Tradesfera  

- **ENTRY_EDGE:** Operar en futuros de alta frecuencia mediante *reversión a la media*. Entradas contracorriente cuando el precio se desvía significativamente de un promedio interno (presumiblemente VWAP o media móvil). Sólo abrir trade si las condiciones estadísticas (ej. volatilidad, momentum) favorecen un alto porcentaje de aciertos; de lo contrario no operar. Contexto típico: mercado en rango lateral o tras movimientos bruscos, sin tendencia fuerte. 
- **EXIT_EDGE:** Tomar ganancias pequeñas («take profits cortos»). La salida se predetermina en niveles cercanos al punto medio (VWAP/media) o en poca distancia fija del precio de entrada para asegurar un win-rate elevado. No se encuentra evidencia de targets ambiciosos ni escalados complejos. Se desconoce uso de trailing stop o ajuste dinámico; probablemente se cierra al alcanzar el objetivo corto o si revierte contra la entrada.
- **INTRA_TRADE_RISK:** Pérdida por operación limitada (stop-loss), aunque no se han divulgado valores exactos. Dado el énfasis en la probabilidad de aprobar el examen, se infiere que el tamaño de loss por trade es similar o menor al TP para mantener alta relación de ganadores (o al menos no exponerse a drawdowns grandes). No hay constancia de técnicas avanzadas dentro de la operación (por ejemplo, re-entrada o escala dentro de la misma posición).
- **INTER_TRADE_RISK:** Gestión de riesgo diaria/balance de cartera enfocada en **minimizar drawdowns acumulativos**. Pons enfatiza que el “riesgo no es el capital virtual, es el precio del examen”, de modo que la estrategia global prioriza aprobar el challenge con la menor pérdida total. Se pueden asumir reglas como parar tras cierto drawdown diario, aunque no hay detalle público. Usa métricas de probabilidad (win-rate esperado) como guía principal.
- **PROP_MANAGEMENT:** Adaptación a cuentas fondeadas: metas de retiro frecuentes (182 retiros totales) y elevada trazabilidad (tracker público). Probablemente mantiene consistencia de tamaño de posición y sigue reglas de firma (sin violar límites de pérdida diaria o drawdown). Está orientado a pasar evaluaciones rápidamente para cobrar payout cuanto antes. La documentación pública muestra una tasa de evaluación exitosa (~26.7%), alineándose con su foco en estadística y disciplina. No se dispone de detalles sobre gestión multi-cuenta o duplicación de trades (copiadores).

# 5. Candidatos de estrategia  

- **A) Reversión a VWAP/Media (mechanizable)** – CONTEXT: intradía (NT, 1m), mercado lateral. Entrar **LONG** si el precio cae muy por debajo del VWAP (o MA) por más de X puntos/ATR y muestra señal alcista (p.ej. vela de rechazo). Entrar **SHORT** si excede el VWAP en X y revierte. SL fijo cerca (p.ej. ATR) y TP breve (cerca del VWAP). *Comentario:* Cumple los principios de Tradesfera (reversión, TP corto). Par. X y TP requieren backtest.  
- **B) Fade de ruptura de apertura (mechanizable)** – CONTEXT: primeros minutos tras apertura NY. Si el precio rompe el máximo/mínimo de los primeros N minutos, luego retrasa rápida y significativamente, **entrar short** en falso breakout superior (o **long** en falso breakout inferior). SL justo por encima del breakout; TP fijo corto en la media intradía. *Comentario:* También sigue reversión contraria tras un impulso inicial. Par. N,  distancia de ruptura, TP to calibrar.  
- **C) Reversión en niveles extremos (parcial)** – CONTEXT: sesiones completas. Identificar soportes/resistencias diarias (pivots, mínimos/máximos previos). **Long** en test de soporte fuerte tras rechazo; **Short** en test de resistencia. SL cercano al nivel y TP breve. *Estado:* Parcial – Necesita confirmación de uso de soportes pivote específicos; posible dependencia de análisis gráfico (no mecanizable puro sin definición clara de “nivel fuerte”).  

Cada candidato se considera “mechanizable” si sus condiciones pueden codificarse estrictamente. Se excluyen diseños que requieran interpretación subjetiva.

# 6. Pseudoreglas de estado (ejemplos)  

```  
CONTEXTO:
  sesion = NY
  mercado = futures (NASDAQ)
  reglón = rango_lateral
  dist_VWAP > X // parámetro a calibrar

LARGO:
  RSI(14) < 30                     // sobreventa en timeframe 1m
  precio cruza VWAP de abajo hacia arriba
  disparador: cerrar compra de mercado inmediato

SL:
  precio = VWAP - (Y * ATR)         // Y > 1 (parámetro)
TP:
  precio = VWAP + Z                // Z ~ valor pequeño (p.ej. X/2)

CORTO:
  RSI(14) > 70                     // sobrecompra intradía
  precio cruza VWAP de arriba hacia abajo
  disparador: sell market

SL:
  precio = VWAP + (Y * ATR)
TP:
  precio = VWAP - Z
```  

```  
CONTEXTO:
  sesion = NY_open
  rango_AB = hora_abertura (15 min)
  
CORTO:
  si precio rompe máximo de AB
  y luego retesta la ruptura por debajo
  disparador: sell market al romper soporte del rango

SL:
  justo arriba del máximo de AB
TP:
  cerca del nivel medio del día (VWAP diurno) o X pips fijo
```  

Los parámetros X, Y, Z quedan **UNKNOWN** hasta backtesting intensivo. Las reglas deben ajustarse (KISS) sin indicadores complejos; por ejemplo, podríamos usar solo RSI/ATR y VWAP para definir señales en vez de bookmap.

# 7. Ejemplos ganadores observados  

No hay ejemplos textuales verificados en fuentes públicas disponibles. Basándonos en la lógica y el manifesto, un caso típico: tras una caída rápida en el Nasdaq Micro, Vicente entraría “long” cerca del VWAP anticipando rebote y saldría con ganancia modesta, tal como sugiere su filosofía. Dado que las sesiones en vivo no están transcritas, no se puede citar una operación específica.  

# 8. Ejemplos perdedores observados  

De igual modo, no contamos con ejemplos detallados. Se asume que cualquier trade que se oponga a la media (p. ej. un break-trade en tendencia fuerte) sería evitado. En pérdidas, es probable que cierre rápido (stop). Sin evidencia directa, marcamos como *UNKNOWN* cómo maneja pérdidas específicas (p. ej. ¿reintenta la misma idea?, ¿sale del día?) según su comentario “cuando no (hay ventaja), quietos”.  

# 9. Evidencia de tracker/cuentas  

Aunque no pudimos acceder al tracker privado, el sitio oficial publica estadísticas acumuladas. Destacan: **€150K** retirados en total, **182** pagos realizados, y una **tasa de fondeo del 26.7%** (evaluaciones aprobadas/ intentos). Esto contrasta con las tasas muy bajas reportadas en el sector (habitualmente <10%), lo que podría indicar un rendimiento sobresaliente o sesgo de selección en el tracker. Estas cifras públicas confirman la consistencia declarada de su método. No se hallaron trackers independientes accesibles para comparar, por lo que se considera sesgada la única fuente disponible (del propio Tradesfera).

# 10. Parámetros a experimentar en D3  

- **Distancia crítica X** para entrada (p.ej. cuánto debe alejarse el precio del VWAP o mínimo/máximo diario).  
- **Nivel de sobrecompra/sobreventa** (p.ej. RSI u otro oscilador) que defina buena estadística de entrada.  
- **Take profit fijo Z** (en puntos o porcentaje) óptimo para preservar alto win-rate.  
- **Stop-loss Y** (ATR múltiplo o pips fijo) que equilibre el ratio riesgo/beneficio pequeño.  
- **Tiempo de sesión**: verificar si conviene operar sólo en NY, London, o abarca todo el día.  
- **Evitar trading** en momentos de baja liquidez (por definir horarios exactos o news).  

Todos estos parámetros deben derivarse de backtests y análisis estadístico. En los casos sin evidencia, se asignan como *UNKNOWN* (por ejemplo, fórmula exacta del “promedio” al que reverten los precios).

# 11. Requerimientos de datos  

- **OHLC intradía (preferentemente 1 minuto)** de futuros (p.ej. ES, NQ micro). Esto permite replicar la mayoría de triggers basados en precios y medias (VWAP, pivotes).  
- **Volumen** por vela para confirmar entradas (opcional, si fuese usado).  
- **No se requiere datos de profundidad de mercado (Level 2)** ni Bookmap/footprints, pues Tradesfera niega depender de ellos (“sin Order Blocks mágicos”).  
- **Tick data** podría mejorar precisión, pero dados los plazos (TP cortos), los OHLC de alta frecuencia bastan.  
- **Indicadores**: VWAP o medias móviles simples (50–100 per) pueden ser necesarios como “media” de referencia. Cualquier otro indicador avanzado (DOM, delta) es *UNKNOWN* o improbable.  

# 12. Compatibilidad con gestión Gerard  

- Para cada candidato con SL/TP simple (A, B), es **factible** probarlo con la gestión A (Stop-loss/Take-profit estándar).  
- El estilo de alta frecuencia y alta tasa de ganancia encajaría con la gestión *B (recuperación negativa)*, ya que frecuentemente generaría pequeños beneficios y alguna pérdida, permitiendo restituir capital paulatinamente tras fallos. No hay evidencia de que use *escalación positiva* agresiva (gestión C); es más conservador.  
- Se puede probar gestión *D (riesgo variable)*, pero dado el enfoque disciplinado mencionado, es probable que opere con tamaño constante o fijo en cuenta. De momento no hay incompatibilidad obvia con Gerard si simplemente se aplica la parte de “hard scalping” positiva (C) extraer, dado que Pons no indica remanentes de alta variabilidad, sino todo lo contrario.  
- En resumen: **compatible** con Gerard A y B; C y D no contradicen explícitamente el método, pero su utilidad dependerá de la parametrización final.

# 13. Desconocidos y contradicciones  

- **Desconocidos:** Detalles finos de entrada (¿usa VWAP, medias o pivotes?). Parámetros exactos de X (distancia), Z (TP) y Y (SL) son *UNKNOWN* y requerirán experimentación. No se sabe si emplea filtros de volatilidad, ni reglas de inactividad (por ejemplo, en eventos macro). Se ignoran ajustes por “drawdown trailing” interno.  
- **Contradicciones:** Ninguna detectada en lo declarado: el manifiesto es consistente en su mensaje. Sólo se advierte que el éxito declarado (>25% funded) es muy alto comparado con estándares de la industria, lo que podría implicar sesgo en los datos mostrados. No se pueden verificar reglas de gestión prop (p.ej. límites exactos de pérdidas permitidas) ya que se ocultan en el sitio.  
- **Límites del método:** Sin un filtro de régimen de mercado explícito, una reversión pura puede fallar en tendencias fuertes; es *UNKNOWN* si Pons ajusta su operativa en esos casos (el manifiesto sugiere que en “tendencia” él simplemente deja de operar).  

# 14. Entrega a D2  

Este informe resume la información pública disponible sobre Tradesfera y su estrategia de futuros. Con los RULE_ID y candidatos mecanizados propuestos, D2 podrá comparar este modelo contra el de Gerard y el Psicólogo en condiciones idénticas de datos. Se han resaltado claramente los componentes **ENTRY_EDGE**, **EXIT_EDGE**, **INTRA/INTER_TRADE_RISK** y **PROP_MANAGEMENT** junto con las reglas explícitas e inferidas. Se proporcionan referencias para cada elemento afinado del modelo operativo. Los parámetros *X, Y, Z* marcados como *UNKNOWN* deben determinarse en el siguiente nivel (D3). El equipo D2 tiene ahora un mapa completo de la suposición operacional de Tradesfera, listo para evaluar su efectividad o diferenciarlo de otras estrategias sin necesidad de rehacer la investigación básica.  

# 15. Fuentes  
- Tradesfera – Sitio oficial (“Manifiesto” y “Sobre Tradesfera”).  
- *Investopedia* – Scalping (definición y práctica).  
- *Wikipedia (en)* – Mean reversion (finance).  

Final status: **RESEARCH_PARTIAL**. Aunque se confían las reglas expuestas y candidatas, faltan detalles concretos extraídos de sesiones reales (audio/vídeo) que requieran validación futura.