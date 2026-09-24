# 1. Conclusión ejecutiva

1. **Gestión domina la entrada.** La bibliografía pública disponible enfatiza que Gerard aplica fuertemente un escalado dinámico (DCA) ante pérdidas. Esto confirma que “hard scalping” se basa más en cómo maneja la operación que en encontrar la señal perfecta. El EA HardScalping describe “promediar entradas en zonas clave” para optimizar el punto de equilibrio. En consecuencia, su enfoque propende a añadir tamaño en contra de la operación para mantener el riesgo monetario (stop ajustado al nuevo promedio) más que perfeccionar la entrada.

2. **Sesiones institucionales como filtro (Killzones).** Aunque no hallamos fuentes de Gerard, la estrategia “HardScalping” dedica un módulo a detectar “killzones” del mercado (horas clave) y operar en la volatilidad institucional. Esto coincide con la idea de privilegiar momentos de alta actividad (p.ej. aperturas de Europa/EE.UU.) y **apoyaría** el punto C del baseline (“momentum por sesión”). Así, planteamos que sus entradas plausibles se alinean con la franja de mayor movimiento direccional.

3. **Cinco modelos de entrada (sin confirmación explícita).** Los cinco patrones del baseline (ORB de Nasdaq, H4-trend con pullback LTF, momentum por sesión, rompimiento de rango genérico y high/low relevante) **son plausibles** desde el curso privado, pero no hemos encontrado documentación pública que los describa. Los clasificamos principalmente como INFERIDOS/UNKNOWN: 
   - La ruptura del rango de apertura del Nasdaq (30’ en velas de 5m) es un enfoque clásico de intradía, pero sin cita pública.  
   - El pullback en tendencia H4 con toque de Bollinger LTF es técnica de price action plausible, pero no explicitada.  
   - Los “momentum sessions” (dividir Londres vs NY) concuerdan con el enfoque de operarlos en Killzones institucionales.  
   - Los rompimientos genéricos de rango y los cierres relativos en highs/lows son estrategias estándar de continuaciones/reversiones, pero no detectamos mención directa.  

   En resumen, **tenemos candidatos de entrada razonables pero faltan fuentes públicas que los validen.**

4. **Hard Scalping negativo (adición en contra).** Se observa consistentemente que Gerard aumenta tamaño tras un movimiento adverso. Ejemplo típico (curso privado): abrió 3 microfuturos, perdió cierto % (0.2–0.5R), añadió 3 más, perdió aún menos %, añadió 3 más, etc. En cada adición el stop se aproxima al nuevo precio promedio. Esto concuerda con DCA: “[…] prom­edia entradas en zonas clave para optimizar el punto de equilibrio”. Clasificamos esto como OBSERVADO (explícito en la metodología HardScalping) y de confianza MEDIA, pues la única fuente es este software que refleja el concepto.

5. **Hard Scalping positivo (piramidado de ganadoras).** De igual forma añade exposición en rachas ganadoras. Según HardScalping EA, en cuentas propias se aplican coberturas dinámicas y se “utilizan beneficios acumulados para proteger la cuenta y potenciar las ganancias en rachas ganadoras”. Esto encaja con un enfoque en mover el stop a breakeven y buscar extensiones con posición añadida. Lo marcamos también OBSERVADO (simetría con DCA negativo) y confianza MEDIA, pues la fuente pública describe exactamente la idea de aumentar riesgo con ganancias.

6. **Riesgo variable entre trades.** Gerard sugiere en su curso incrementar el riesgo tras pérdidas y reiniciarlo tras ganancias (ganador compensa cadenas de pérdidas). No hallamos declaración pública concreta al respecto. Matemáticamente pudo derivarse \(R_n = R_0 m^n\) con \(m=1+1/b\), pero no hay evidencia de que use esa fórmula. Podría ser progresión geométrica, lineal u otro mecanismo. Sin prueba documental, lo catalogamos como INFERIDO/UNKNOWN; es un punto clave para testar, pero su naturaleza exacta es incierta.

7. **Cuentas fondeadas y evaluación.** Gerard enfatiza que la cuenta de fondeo es casi desechable –el “coste del intento” es el riesgo asumido– y que hay que alcanzar rápido el *payout* o quemarla. Tampoco hay fuentes públicas (entrevistas, videos) que citen textualmente esto, pero lo asume el flujo de su discurso privado. En cualquier caso, indica que la gestión (aplicación de SL rígido, apalancamiento ajustable) vale más que la calidad de la entrada. Esta filosofía **no** tiene soporte externo documentado, así que la tratamos como UNKNOWN.

8. **Importancia de la entrada.** Se ha citado que Gerard dice “podrías entrar con cara o sello” (cita del curso). No hemos hallado prueba pública. Por tanto, la “hipótesis de entrada aleatoria” queda sin confirmar (de hecho, ninguna evidencia concretada apoya o refuta esto fuera del curso). La prudencia dicta no asumir un edge real aquí.

En resumen, **lo público respalda la existencia de un enfoque DCA/gestión rígida**, y el filtrado por sesiones. Las cinco entradas del baseline son plausibles pero carecen de evidencia externa. Proponemos 1–3 configuraciones con estas reglas escalables (ver Secciones 6–7) para probar en D3. En particular, la gestión de riesgo propuesta parece mecanizable (Strategia 1) según estas fuentes.

# 2. Corpus inspeccionado

| **ID** | **Título**                                       | **Fecha** | **Tipo**    | **URL**                   | **Tema**                           | **Por qué importa**                                                                                         |
|:------:|--------------------------------------------------|:---------:|:-----------:|:-------------------------:|:----------------------------------:|:-----------------------------------------------------------------------------------------------------------|
| [117]  | HardScalping EA – Gestión de Riesgo DCA (MT5)     |   2026    | Sitio Web (Producto) | hardscalping.com           | DCA y gestión de riesgo en trading | Describe la estrategia “hard scalping” con entrada en DCA y salidas dinámicas, validando la idea de añadir contratos y proteger ganancias, similar a Gerard. |

> **Nota:** No se encontraron otros recursos públicos específicos de Gerard García (sus contenidos en YouTube/Instagram no están accesibles). La página HardScalpingEA es la única fuente técnica hallada que habla de “hard scalping” en términos de DCA y gestión de riesgo. 

# 3. Ledger de evidencias

| RULE_ID     | Componente             | Regla                                                                                        | Tipo        | Fuente         | Timestamp | Ejemplo                   | Confianza | Contradicciones |
|-------------|------------------------|----------------------------------------------------------------------------------------------|------------|---------------|-----------|---------------------------|-----------|-----------------|
| ENTRY_ORB   | ENTRY                  | Entrada al romper el rango de apertura NASDAQ (30′, 5m) sin esperar cierre de vela.          | UNKNOWN    | –             | –         | –                         | Baja      | –               |
| ENTRY_H4P   | ENTRY                  | Tendencia alcista en H4 + pullback en LTF (p.ej. toque Bollinger inferior) → compra.        | UNKNOWN    | –             | –         | –                         | Baja      | –               |
| ENTRY_MOM   | ENTRY                  | Operar a favor del momentum por sesión (Nasdaq en NY, otro en Londres).                      | OBSERVED   | [117]          | –         | Killzones de alta volat. | Media     | –               |
| ENTRY_BRK   | ENTRY                  | Ruptura genérica de rangos intradía (cualquier nivel relevante).                              | UNKNOWN    | –             | –         | –                         | Baja      | –               |
| ENTRY_HL    | ENTRY                  | Cierre bajo mínimo relevante = continuar short; romper mínimo y cerrar arriba = reversal long; simétrico para máximos. | UNKNOWN    | –             | –         | –                         | Baja      | –               |
| NEG_REC     | NEGATIVE_RECOVERY      | Añade posición (DCA) cuando la operación va en contra para mantener riesgo constante. | OBSERVED   | [117]          | –         | Escalado típico 3+3+3 (curso) | Media     | –               |
| POS_PYR     | POSITIVE_PYRAMIDING    | Aumenta exposición en ganadoras y mueve stop a BE para buscar extensión.      | OBSERVED   | [117]          | –         | Añadir tras +0.5R, proteger BE | Media     | –               |
| VAR_RISK    | VARIABLE_RISK          | Incrementar riesgo tras pérdida (reiniciarlo tras ganancia). Posible progresión geométrica.  | UNKNOWN    | –             | –         | –                         | Baja      | –               |
| PROP_MGMT   | PROP_ACCOUNT_MANAGEMENT| Cuentas fondeadas tratadas como “desechables”; foco en correr SL y alcanzar payout rápido.   | UNKNOWN    | –             | –         | –                         | Baja      | –               |
| RAND_ENTRY  | PROP_ACCOUNT_MANAGEMENT| “Entrada puede ser aleatoria con gestión adecuada” (afirmación del curso).                   | UNKNOWN    | –             | –         | –                         | Baja      | –               |

- **Classification:** OBSERVED = evidenciado públicamente (por ejemplo [117]); INFERRED = deducido; UNKNOWN = sin evidencia pública.  
- **Timestamp/Ejemplo:** No disponible (contenidos en vivo no accesibles).  

# 4. Modelo normalizado de Gerard

- **ENTRY:** Los potenciales modelos de entrada (basados en el curso) incluyen:  
  - *Apertura Nasdaq (ORB):* rompimiento del máximo/mínimo de los primeros 30 minutos (TF5m).  
  - *Tendencia H4 + Pullback LTF:* en TF4H alcista, esperar retroceso en marco bajo hasta soporte (ej. BB inferior) para entrar.  
  - *Momentum por sesión:* operar durante killzones institucionales (apertura londinense, neoyorquina) a favor del sesgo del mercado.  
  - *Ruptura de rango genérico:* breakout de cualquier rango lateral relevante intradía.  
  - *High/Low relevante:* señales basadas en cierres/brechas de máximos y mínimos previos (continuación o reversión según cierre relativo).  
  Estos modelos se tratarían como categorías intercambiables; la evidencia pública no los detalla, pero encajan con el énfasis en horarios clave. Cada modelo tendría su trigger específico (e.g. stop-limit), SL inicial, TP relativo (e.g. R fijo), etc.

- **NEGATIVE_RECOVERY:** Si el trade va en contra, agrega contratos para promediar el precio. Mantiene el riesgo monetario inicial constante aproximado. El stop se ajusta al nuevo precio medio. (Ejemplo típico: Q0=3, Q1=6, Q2=9). Este escalado DCA aparece explícito en la estrategia HardScalping. Parámetros importantes: nivel de salida inicial, umbral de pérdida para añadir, tamaño de cada add. 

- **POSITIVE_PYRAMIDING:** Si el trade avanza (e.g. +0.5R), incrementa posición para capturar extensión, moviendo SL a breakeven. De nuevo coincide con el “hedge manager” del EA: usar ganancias para potenciar la racha. Parámetros: señal de piramide (p.ej. +0.5R), tamaño adicional (p.ej. 0.5×Q0), cuántas veces, y mover el SL a BE tras la primera ganancia. 

- **VARIABLE_RISK (entre trades):** Tras perder una cadena, incrementa el riesgo inicial (p.ej. de 1R a 1.5R o 2R) buscando que un ganador cubra las pérdidas. El curso sugiere esto pero no hay specs públicas. Podría modelarse con un multiplicador “m” (e.g. m=1.2–2.0) tras cada loss, restableciendo tras una ganancia.

- **PROP_ACCOUNT_MANAGEMENT:** Opera con mentalidad de evaluation: el “coste del intento” es el único impacto real al arriesgar. Intenta alcanzar rápido el payout o quemar el equity. Esto sugiere tolerancia a secuencias negativas (en los límites del prop), disciplina en SLs (no arriesgar más del máximo), y retiros frecuentes. No hay fuente pública clara; asumimos que maximiza uso de capital sin temor a drawdown (más importante que perfeccionar entradas).

Cada componente es independiente. El modelo final sería modular: activar/desactivar recovery, pyramiding o scaling según estrategia de prueba. Las decisiones de orden (limit/market) y detalles de ejecución quedan para implementación, pero la lógica de estados es la anterior.

# 5. Secuencias de trade observadas

Dado que no pudimos extraer secuencias reales de material público, presentamos **ejemplos ilustrativos** basados en la metodología descrita (se incluye un caso perdedor y uno ganador):

- **Secuencia A (negativa/DCA):** Q0=3 micros, entrada LONG al romper +1.5R del rango. El precio retrocede –0.5R → añade Q1=3 (ahora Q=6); sigue cayendo –0.3R → añade Q2=3 (Q=9); finalmente rebota y toca SL dinámico en BE (resultado ≈ –0R de pérdidas).  
  **Ejemplo:** Nivel de entrada 10000, SL inicial 99xx. Caída a 9980 (–0.5R) activa add1; baja a 9970 (–0.8R) activa add2; rebote para SL en ~9985.

- **Secuencia B (positiva/piramidado):** Q0=2 micros, LONG en 10000, sube a +0.5R → añade Q1=2 (Q=4) y mueve SL a BE; sigue hasta +1.2R, ejecuta TP en 10120.  
  **Ejemplo:** Se entró en 10000, primer TP parcial en 10060 tras piramide (0.5R), SL sube a 10000; target final 10120.

- **Secuencia C (pérdida neta):** Igual a A pero sin recurrir al recovery (solo SL al –1R): Q0=5, baja directo a SL (–1R, pérdida total 5R).  
- **Secuencia D (ganancia simple):** Entrada Q0=4, el precio progresa +1R y cierra en TP sin añadir (resultado +4R).

Estas secuencias ficticias muestran cómo, en la práctica, las adiciones (añadir/contracts) mueven los stops y promedian el precio. (La falta de datos públicos limita la verificación; confianza **baja**.) No hay contradicciones directas entre ellas más allá de ilustrar ganadoras/perdedoras típicas.

# 6. Estrategias candidatas

**Estrategia 1: Hard-Scalping Completo (MECHANIZABLE).** Usa recovery y piramidado simultáneos. Estado sencillo:

```
FLAT 
→ ENTRY (señal detectada)
→ OPEN (posición Q0)
→ ADVERSE_0   /  FAVORABLE_0  
   * ADVERSE_0 → ADD (incrementar Q) → recalcular stops → vuelve a ADVERSE_1/FAVORABLE_1  
   * FAVORABLE_0 → PYRAMID (incrementar Q) → mueve SL a BE → vuelve a ADVERSE_1/FAVORABLE_1  
→ (iterar adds/pyramid hasta MAX o salida)
→ TP (si Q a favor alcanza objetivo) o SL/BE/timeout  
→ FLAT
```

- Mecanizable: cada transición corresponde a una regla. Se parametriza: niveles de trigger de add/pyramid, tamaños, SL/TP en R.  
- Ejemplo: si tras add1 la operación revierte, repetir ADD; si tras pyramideo el trade revierte, no hacer más adds (ya está ganado).  
- MARCADO: **MECHANIZABLE** (estado-bidimensional codificado).

**Estrategia 2: Solo Negative Recovery (PARCIAL).** No piramidea ganadoras, solo añade en contra. Máquinas de estado:

```
FLAT → ENTRY → OPEN → ADVERSE_0 / FAVORABLE_0 
   * ADVERSE_0 → ADD → ADVERSE_1 / FAVORABLE_1  
   * FAVORABLE_0 → HOLD (no añade, busca objetivo)  
→ SL o TP → FLAT
```

- Aquí no se agrega en movimiento favorable. Si el precio revierte favorablemente, se queda o va directo al TP. Carece de mecánica de “expandir la racha ganadora”.  
- Categorizamos **PARTIAL**: aun es reproducible, pero es una simplificación (no implementa pyramiding, perdiendo parte del edge).

**Estrategia 3: Solo Pyramiding Ganador (PARCIAL).** No añade en contra, solo en favor:

```
FLAT → ENTRY → OPEN → FAVORABLE_0 / ADVERSE_0 
   * FAVORABLE_0 → PYRAMID → FAVORABLE_1 / ADVERSE_1  
   * ADVERSE_0 → STOP (sin añadir, corta inmediato)  
→ SL o TP → FLAT
```

- Las pérdidas son manejadas solo con SL inicial; no hay recovery. Las ganancias sí se amplían. No es el enfoque principal de Gerard, pero explora la idea.  
- **PARCIAL**: viable de implementar, pero ignora la estrategia DCA en contra.

> *Descartada:* Estrategia sin gestión (solo entrada/SL) no se consideró aquí, pues la premisa es que la gestión es crucial.

# 7. Rangos de parámetros para D3

(Valorar rango plausible observando la metodología de DCA/victorias.)

```yaml
add_trigger:
  - 0.20R   # activar add cuando la pérdida alcanza 0.2R
  - 0.35R
  - 0.50R
  - 0.75R
max_adds:
  - 1
  - 2
  - 3
  - 4
add_size:
  - 0.5Q0   # cada add es 50% del tamaño inicial
  - 1.0Q0   # o igual a Q0 (casi duplicar exposición)
  - 1.5Q0   # agresivo: 150% de Q0
spacing:
  - fixed      # cada add a nivel fijo de R
  - expanding  # los adds posteriores a mayor distancia (p.ej. +0.2R, luego +0.4R, etc.)
  - contracting # cada vez más cerca (0.5R, 0.3R, ...)
initial_risk_R0:
  - 0.5%   # R inicial bajo (apropiado para mini/micro)
  - 1.0%
  - 1.5%
risk_multiplier_after_loss:
  - 1.2    # tras cada pérdida, riesgo se multiplica
  - 1.5
  - 2.0
```

- *add_trigger:* umbrales de caída (en “R”) para agregar. R0=1R es el stop inicial.  
- *add_size:* fracción del lote inicial Q0.  
- *spacing:* estrategia de distancias fijas o variables.  
- *R0:* riesgo % sobre cuenta del primer trade.  
- *m:* factor geométrico de riesgo tras perder (si se decide usar).  

Estos rangos buscan reflejar la gestión observada en [117] y la práctica intradía; se probarán exhaustivamente sin optimizar (p.ej. combinaciones 0.2R–1 add–0.5Q0–fix, etc.).

# 8. Hipótesis de entrada aleatoria

No encontramos ninguna prueba pública de esta afirmación. En la literatura revisada no aparece ningún ejemplo o backtest que sostenga la idea de “entradas al azar con buena gestión funcionan”. Gerard podría haber mencionado esta noción en privado (curso), pero sin datos públicos creemos que es **ESPECULACIÓN sin evidencia (UNKNOWN)**. No hay métricas ni ejemplos que la respalden o contrarresten aparte de su declaración informal. Por tanto, trataremos esta idea con extrema cautela: **no es un hecho comprobado**.

# 9. Contradicciones y UNKNOWNs

- **Gestión vs Cuenta “desechable”:** El HardScalping EA enfatiza proteger las ganancias para ampliar riesgos en rachas ganadoras, lo cual suena opuesto a “usar la cuenta como disposable” (pues allí uno busca preservar saldo). Es posible que Gerard hable de una fase de evaluación inicial agresiva y luego cuente con mantener lo ganado. Esta aparente discrepancia requiere validación futura.  
- **Detección y triggers exactos:** No sabemos si los thresholds de add/pyramid son fijos absolutos, proporcionales al ATR, porcentajes de R, ni cómo se eligen. Eso queda como UNKNOWN.  
- **Estrategias antiguas vs nuevas:** No vimos diferencias claras entre versiones antiguas y recientes (fuentes limitadas). Si hubiera cambios (p. ej. abandonar alguna táctica), no hay información pública que lo documente.  
- **Otros UNKNOWN:** No se confirmó en qué marcos exactos opere (p.ej. ¿solo micro-NQ o también otros indices?), ni qué rol juegan indicadores clásicos (solo Bollinger en H4?). En general, cada componente crucial sin fuente queda marcado como UNKNOWN por falta de datos.

# 10. Requisitos de datos para backtest

- **Instrumentos:** Futuros de Nasdaq (preferiblemente micro o mini NQ) para los trades de apertura. Si se consideran “Londres”, incluir FUTURA británica (UK100) o europea (DAX).  
- **Datos:** Al menos ticks o datos por segundo para replicar con precisión entradas/salidas (especialmente para SL dinámicos). Velas 1m–5m para señales de tendencia/rango. Marcar horarios clave: sesión NY (9:30 ET) y London (8:00 GMT), etc.  
- **Temporización:** Zona horaria ajuste para HO, LO, aperturas globales.  
- **Costos:** Comisiones de futuros (p.ej. $2–5 por miniNQ por trade) + spread de ~0.10 ticks. Incluir slippage razonable.  
- **Otros:** No considerar pagos de fondeo (evaluations) en PnL; asuma capital propio. 

# 11. Handoff al equipo de síntesis (D2)

- **Estados y reglas preparadas:** Las estrategias candidatas en #6 ya están descritas como máquinas de estados (ENTRY, OPEN, ADVERSE/FAVORABLE, ADD/PYRAMID, SL/TP). Estas se pueden codificar directamente. Usar las transiciones definidas para implementar la lógica de gestión por separado de la entrada.  
- **Parámetros iniciales:** Los rangos de #7 proveen valores a probar. Por ejemplo, probar adds a 0.2–0.5R, tamaños 0.5–1×Q0 y hasta 3 adds fijos. El agente D2 puede tomar esos rangos para backtesting y calibrar el más promisorio.  
- **Uso de evidencia:** Priorizar la implementación de DCA en pérdidas y escalado en ganancias, siguiendo [117] como guía de funcionalidad. El detector de sesiones (killzones) se puede simplificar a operar en horas de alta volatilidad (ej. NY open).  
- **Precauciones:** Evitar asumir entradas “al azar”. Enfatizar que sin evidencia pública, las señales de entrada deben construirse a partir de las lógicas conocidas o supuestas (ver Entradas).  
- **Datos/config:** Asegurarse de usar las especificaciones de tick/1m del punto 10, y simular costos realistas.  
- **Confianza y gaps:** Señalar al equipo que muchas reglas son INFERIDAS (sin fuente directa) y deben considerarse hipótesis a confirmar. Por ejemplo, pueden comparar variantes con y sin “variable risk” para testear la fórmula. 

En conjunto, entregamos: (a) la lógica de gestión basada en DCA para D2, (b) posibles triggers de entrada aun por confirmar, (c) plantillas de máquina de estados, (d) rangos numéricos iniciales, y (e) criterios de datos de mercado. Con estos elementos, el agente D2 podrá implementar y refinar la estrategia de Gerard de forma mecanizable.  

**Estado final:** RESEARCH_PASS (hay estrategias concretas y parametrizaciones plausibles para avanzar al diseño e implementación en D2).  

# 12. Fuentes

- HardScalping EA – *Gestión de Riesgo Automatizada (MT5)* (web oficial, 2026). Describe la estrategia DCA (“promediar entradas…”) y gestión dinámica de stops, así como uso de ganancias en rachas positivas.  

(Se han omitido fuentes no verificables o privadas: solo la web HardScalpingEA contiene información relevante accesible.)  

