# SQX — BR H1 LONG — Grupos reutilizables, builders existentes y continuidad Forge/Echo

> [!info] Referencia técnica del proyecto
> **Proyecto:** [[Estrategias IMOX — Forex y CFD con Echo Forge]] · **Fecha de documentación:** 2026-10-24 · **Alcance:** Breakout H1 LONG (BR H1 LONG), StrategyQuant X v136/v14x · **Tipo de entrega:** documentación técnica de apoyo, no reemplaza la nota canónica del proyecto.
>
> **Fuente de la arquitectura:** documento consensuado `sqx_br_h1_long_grupos_reusable.md`, con inventario de opciones aportado por el owner. **Alcance de la evidencia:** las selecciones descritas son las definiciones aprobadas para el espacio de búsqueda, no una auditoría de lo realmente habilitado en cada archivo Builder.

## Propósito y estado de esta documentación

Esta referencia conserva las seis tesis de breakout y sus elecciones exactas por categoría de SQX; permite inventariar los builders y las estrategias optimizadas que el owner ya tiene, y prepara la continuidad operativa con [[Echo Forge — Operación Real V2]] y [[Echo — Producto Integrado]]. El objetivo inmediato es recuperar trabajo previo antes de construir nuevas estrategias. La documentación no equivale a certificar ni importar automáticamente ninguna estrategia.

- **Arquitectura cerrada:** G1 compresión→expansión, G2 estructura horizontal y G4 tendencia alineada = core; G3 sesión/día/semana y G5 continuación/re-break = secundarios; G6 post-pullback/reset = experimental.
- **Evidencia aportada por el owner:** existen algunos Builders ya configurados y estrategias optimizadas. No se han aportado aquí sus identificadores, ficheros, conteos, fechas, configuraciones exactas ni resultados. **No marcarlos como auditados o completados.**
- **Continuidad operacional:** revisar artefactos originales de SQX, incorporarlos a Forge por un flujo existente y verificable, validar el resultado y gestionar la posterior ingesta en Echo conforme al contrato realmente vigente. No declarar la integración Forge→Echo realizada para este corpus sin evidencia.
- **Instrumentos:** los grupos son reutilizables para GBPJPY H1 y NDX H1; la documentación previa sobre GBPJPY no convierte estos grupos en exclusivos del par. **Las calibraciones, umbrales numéricos, unidades, sesiones y costes NO se trasladan automáticamente entre instrumentos.**
- **Regla de ingeniería:** un representante por subfamilia como núcleo por regla; un trigger de ruptura identificable; filtros no redundantes; pocos grados de libertad. **No asumir que seleccionar bloques en Builder impone por sí solo todas estas restricciones de combinación:** verificar el resultado generado o las plantillas efectivas.
- **Separación de ámbitos:** este material es documentación privada del proyecto de trabajo personal. No constituye material que deba publicarse ni compartirse en la comunidad IMOX ni incorpora acceso a implementación privada de Echo/Forge.

## Resumen ejecutivo G1–G6

| Grupo | Jerarquía | Tesis a descubrir | Señal de entrada que se esperaba | Guardarraíl principal |
|---|---|---|---|---|
| **G1 — Compresión → Expansión** | Core | Ruptura tras baja volatilidad seguida de expansión | Salida por BB/KC/Highest con contexto de compresión | 1 compresión + 1 expansión + 1 nivel, no tres proxies equivalentes |
| **G2 — Ruptura de estructura horizontal** | Core | Superación de un techo identificable | Highest, Highest in range, Fractal, DH/WH/SH | Un nivel dominante y buffer; sin multiplicar techos |
| **G3 — Breakout de sesión / día / semana** | Secundario/contextual | Ruptura de nivel temporal en ventana relevante | DH/SH/WH condicionado por hora o día | 1 gate temporal + 1 nivel; timezone/DST del símbolo |
| **G4 — Breakout alineado con tendencia** | Core | Ruptura o recuperación de rail dinámica con tendencia favorable | EMA/SMA/HMA/KAMA/ST/GHL/Ichimoku/LinReg con fuerza | 1 rail + 1 filtro; ADX/Directional Index/Vortex no triples |
| **G5 — Continuación por impulso / re-break** | Secundario fuerte | Segunda pata tras impulso y pausa breve | H/Highest/Highest in range con Momentum/ROC u otra familia | Re-break estructural, no cambio de rail como gatillo |
| **G6 — Breakout post-pullback / reset** | Experimental controlado | Respiro interno y re-break a favor del movimiento | Highest/Highest in range o rail recuperada tras reset | Oscilador nunca es entrada standalone |

## Qué significa «seleccionado» en esta referencia

Las tablas siguientes son el **catálogo prescrito** por el diseño consensuado (Signals, Indicators, Stop/Limit Price Levels, Stop/Limit Price Ranges y Operators). Todavía falta demostrar en cada Builder concreto: qué checkbox/variante/operador quedó activado, rangos `Min/Max/Step`, pesos, plantillas, órdenes, historial, datos y comportamiento real de las estrategias construidas. La regla de no redundancia es una **intención de arquitectura**, no una garantía de ejecución automática del algoritmo genético.

## Precauciones obligatorias al reutilizar para NDX H1

- Mantener las seis tesis; **recalibrar indicadores dependientes de magnitud de precio**, entre ellos ATR, MTATR, TR, STDDEV, MACD/OSMA/AWO/Bulls Power, BB Range y BarRange. No reutilizar límites absolutos de GBPJPY.
- Revisar `Fixed pips`, buffers, point/tick size, moneda de P&L, comisiones, spreads, swaps/financiación y política de gaps contra el histórico y contrato del instrumento.
- En G3, comprobar el huso de la serie, apertura/cierre de la sesión y cambios DST antes de interpretar `Bar Hour`/`Current Hour`, DH/SH/WH y referencias temporales.
- Verificar que los niveles de ruptura no toman el máximo de una barra no cerrada o del futuro por configuración incorrecta de desplazamientos/series; auditar ejemplos de señales exportadas.
- Validar en muestras separadas y con costes realistas; no atribuir una rentabilidad superior a un grupo sin comparar Builder/Retester/robustez por cohortes equivalentes.

---

## Estado del documento

**Versión cerrada y operativa.**

Este documento deja la arquitectura final en formato reutilizable, aterrizada a las categorías reales de SQX y lista para usarse como referencia de implementación en Builder.

No redefine la arquitectura. No crea grupos nuevos. No inventa bloques fuera del listado real entregado.

---

## Jerarquía final

### Core reusable
- **Grupo 1 — Compresión → Expansión**
- **Grupo 2 — Ruptura de estructura horizontal**
- **Grupo 4 — Breakout alineado con tendencia**

### Secundario / contextual
- **Grupo 3 — Breakout de sesión / día / semana**
- **Grupo 5 — Continuación por impulso / re-break**

### Experimental controlado
- **Grupo 6 — Breakout post-pullback / reset**

---

## Reglas operativas globales del set

### 1) Regla de subfamilia
Usar **máximo 1 representante por subfamilia como núcleo** dentro de una misma regla.

Ejemplos de duplicación a evitar:
- `ADX + Directional Index + Vortex`
- `Momentum + ROC`
- `MACD + OSMA`
- `RSI + QQE + Stochastic + Williams PR`

### 2) El trigger final debe seguir siendo breakout
El trigger final debe salir de una de estas familias:
- ruptura de `Highest`
- ruptura de `Highest in range`
- ruptura de `(DH) Daily High / (WH) Weekly High / (SH) Session High`
- ruptura o recuperación sobre:
  - `(EMA) Exponential Moving Average`
  - `(SMA) Simple Moving Average`
  - `(HMA) Hull Moving Average`
  - `(KAMA) Kaufman’s Adaptive Moving Average`
  - `(ST) SuperTrend`
  - `(GHL) GannHiLo`
  - `Ichimoku`
  - `(LinReg) Linear Regression`

### 3) Signal e Indicator no son lo mismo
Normalización importante para SQX:
- `Directional Index` = **Signal**
- `Trend` = **Signal**
- `Kelner Channel` = **Signal**
- `(KC) Keltner Channel` / `(MTKC) MT Keltner Channel` = **Indicators / Price Levels**
- `Williams PR` = **Signal**
- `(WILL%R) Williams Percent Range` = **Indicator**

### 4) Secundario válido no significa obligatorio
Que un bloque tenga parking formal significa que **puede entrar sin romper la arquitectura**. No significa que deba entrar siempre.

### 5) Estructura ideal de una regla
En general, una regla sana debería verse así:
- **1 trigger breakout**
- **1 filtro principal**
- **0 o 1 confirmación**
- **0 o 1 buffer/range auxiliar**

Cuando te pasas de eso, normalmente no estás agregando edge: estás agregando combinatoria.

---

# Grupo 1 — Compresión → Expansión

**Jerarquía:** Core reusable

## Intención operativa
Buscar breakouts que nacen desde compresión y salen con expansión real.

Este grupo no busca solo que el precio suba. Busca esta secuencia:
1. mercado apretado
2. rango/volatilidad empiezan a expandirse
3. el precio rompe una referencia válida
4. la entrada LONG intenta montarse en esa expansión

## Signals a incluir
- `ATR`
- `Bollinger Bands`
- `Kelner Channel`
- `Std Dev`

## Indicators a incluir
- `(ATR) Average True Range`
- `(MTATR) Average True Range`
- `(STDDEV) Standard Deviation`
- `(TR) TrueRange`
- `(KC) Keltner Channel`
- `(MTKC) MT Keltner Channel`
- `Highest`
- `Highest in range`

## Stop/Limit Price Levels a incluir
- `(BB) Bollinger Bands`
- `(KC) Keltner Channel`
- `(MTKC) MT Keltner Channel`
- `Highest`
- `Highest in range`
- `(H) High` como secundario

## Stop/Limit Price Ranges a incluir
- `(ATR) Average True Range`
- `(MTATR) Average True Range`
- `(BBR) BB Range`
- `(BBWR) BB Width Ratio`
- `(BR) BarRange`
- `(TR) TrueRange`
- `Biggest Range` solo experimental
- `Smallest Range` solo experimental

## Operators recomendados
- `Crosses Above`
- `(>) Is greater`
- `(>=) Is greater or equal`
- `Is rising`
- `(> X) Is greater for X bars`

## Núcleo implementable
La regla base de este grupo debería tomar:
- **1 proxy de compresión**
- **1 proxy de expansión**
- **1 familia de entry / ruptura**

Ejemplo de estructura válida:
- compresión: `(BBWR) BB Width Ratio`
- expansión: `(ATR) Average True Range`
- trigger: `Highest`

## Secundarios válidos
- `(H) High`
- `(FP) Fixed pips` como buffer
- `Biggest Range`
- `Smallest Range`

## Equivalentes que no deben coexistir
No meter juntos como núcleo:
- `(BBWR) BB Width Ratio + (BBR) BB Range + (STDDEV) Standard Deviation`
- `(ATR) Average True Range + (TR) TrueRange`
- `(KC) Keltner Channel + (MTKC) MT Keltner Channel`
- `Highest + Highest in range`
- `(BR) BarRange` como compresión **y** expansión en la misma regla

## Qué busca realmente el Builder
- mercado comprimido
- expansión incipiente de rango/volatilidad
- ruptura que no sea un toque marginal
- breakout con contexto, no puro azar

## Mezclas a evitar
- meter osciladores de reset
- usar tres proxies de compresión “por si acaso”
- convertir el grupo en estructura horizontal pura
- duplicar el rol de `(BR) BarRange`

---

# Grupo 2 — Ruptura de estructura horizontal

**Jerarquía:** Core reusable

## Intención operativa
Buscar quiebres de techos horizontales claros.

Es el grupo más universal y más limpio para BR H1 LONG.

## Signals a incluir
- `Highest Lowest`
- `Fractal`

## Indicators a incluir
- `Highest`
- `Highest in range`
- `Fractal`
- `(Pivots) Pivots` solo secundario

## Stop/Limit Price Levels a incluir
- `Highest`
- `Highest in range`
- `Fractal`
- `(DH) Daily High`
- `(WH) Weekly High`
- `(SH) Session High`
- `(H) High`
- `(Pivots) Pivots` solo secundario

## Stop/Limit Price Ranges a incluir
- `(FP) Fixed pips`
- `(ATR) Average True Range`
- `(BR) BarRange`

## Operators recomendados
- `Crosses Above`
- `(>) Is greater`
- `(>=) Is greater or equal`
- `(> X) Is greater for X bars`

## Núcleo implementable
La regla base de este grupo debería tomar:
- **1 fuente estructural de techo**
- **1 buffer de entrada**
- opcionalmente **1 confirmación de permanencia**

Ejemplo:
- nivel principal: `Highest in range`
- buffer: `(ATR) Average True Range`
- confirmación opcional: `(> X) Is greater for X bars`

## Secundarios válidos
- `(H) High`
- `(Pivots) Pivots`
- `(DO) Daily Open`, `(WO) Weekly Open` como contexto, no como trigger principal

## Equivalentes que no deben coexistir
No meter juntos como núcleo:
- `Highest + Highest in range`
- `(DH) Daily High + (WH) Weekly High + (SH) Session High`
- `(FP) Fixed pips + (ATR) Average True Range` como doble buffer base

## Qué busca realmente el Builder
- un techo identificable
- ruptura válida de ese techo
- entrada LONG sobre el quiebre, no sobre una interpretación rebuscada

## Mezclas a evitar
- usar demasiados niveles equivalentes a la vez
- poner `(Pivots) Pivots` al mismo nivel que `Highest` o `Fractal`
- llenar el grupo de contexto y quitarle simplicidad estructural

---

# Grupo 4 — Breakout alineado con tendencia

**Jerarquía:** Core reusable

## Intención operativa
Buscar breakout a favor de una estructura tendencial ya existente, normalmente apoyado en una rail dinámica y validado por fuerza direccional o calidad tendencial.

## Signals a incluir
- `ADX`
- `Aroon`
- `Directional Index`
- `Gann Hi Lo`
- `Hull Moving Average`
- `Ichimoku`
- `KAMA`
- `Kaufman Efficiency Ratio`
- `Lin Reg`
- `Moving Average`
- `Super Trend`
- `Trend`
- `Vortex`

**Nota importante:**
- `Directional Index` es **Signal**
- `Trend` es **Signal**
- no tratarlos como Indicators

## Indicators a incluir
- `(ADX) Average Directional Movement Index`
- `(ARO) Aroon`
- `(EMA) Exponential Moving Average`
- `(SMA) Simple Moving Average`
- `(SMMA) Smoothed Moving Average`
- `(LWMA) Linear Weighted Moving Average`
- `(HMA) Hull Moving Average`
- `(KAMA) Kaufman’s Adaptive Moving Average`
- `(KER) Kaufman Efficiency Ratio`
- `(LinReg) Linear Regression`
- `(ST) SuperTrend`
- `(VRX) Vortex`
- `(GHL) GannHiLo`
- `Ichimoku`

## Stop/Limit Price Levels a incluir
- `(EMA) Exponential Moving Average`
- `(SMA) Simple Moving Average`
- `(SMMA) Smoothed Moving Average`
- `(LWMA) Linear Weighted Moving Average`
- `(HMA) Hull Moving Average`
- `(KAMA) Kaufman's Adaptive Moving Average`
- `(LinReg) Linear Regression`
- `(ST) SuperTrend`
- `(GHL) GannHiLo`
- `Ichimoku`

## Stop/Limit Price Ranges a incluir
- `(ATR) Average True Range`
- `(MTATR) Average True Range`
- `(TR) TrueRange`

## Operators recomendados
- `Crosses Above`
- `(>) Is greater`
- `(>=) Is greater or equal`
- `Is rising`
- `(| > MA) Indicator Above MA`
- `(| > MA) Indicator Crosses Above MA`

## Núcleo implementable
La regla base de este grupo debería tomar:
- **1 rail dinámica**
- **1 filtro de fuerza o calidad tendencial**
- **0 o 1 confirmación**

Ejemplo:
- rail: `(ST) SuperTrend`
- filtro de fuerza: `(ADX) Average Directional Movement Index`
- confirmación opcional: `Is rising`

## Secundarios válidos
- `Directional Index` como Signal de fuerza direccional
- `Trend` como Signal de estructura / dirección
- `(SMMA) Smoothed Moving Average`
- `(LWMA) Linear Weighted Moving Average`
- `(ATR) Average True Range` o `(TR) TrueRange` como filtro de entorno

## Equivalentes que no deben coexistir
No meter juntos como núcleo:
- `(ADX) Average Directional Movement Index + Directional Index + (VRX) Vortex`
- `(ARO) Aroon + Trend + (KER) Kaufman Efficiency Ratio`
- varias rails a la vez:
  - `(EMA) Exponential Moving Average + (SMA) Simple Moving Average + (HMA) Hull Moving Average`
  - `(ST) SuperTrend + (GHL) GannHiLo + Ichimoku + (LinReg) Linear Regression`

## Qué busca realmente el Builder
- contexto tendencial ya existente
- precio rompe o recupera rail dinámica
- breakout a favor del flujo, no contra él

## Mezclas a evitar
- tratar `Directional Index` como Indicator
- tratar `Trend` como Indicator
- devolver `MACD` o `OSMA` al núcleo de este grupo
- apilar varios filtros de fuerza como si fueran ortogonales
- convertir este grupo en trend-following genérico sin breakout claro

---

# Grupo 3 — Breakout de sesión / día / semana

**Jerarquía:** Secundario / contextual

## Intención operativa
Agregar timing contextual al breakout.

El breakout importa no solo por el nivel, sino por **cuándo** ocurre.

## Signals a incluir
- `Bar And Time`
- `Highest Lowest`
- `ATR`
- `VWAP` solo experimental

## Indicators a incluir
- `Bar Hour`
- `Current Hour`
- `Bar Day Of Week`
- `Current Day Of Week`
- `Bar Minute` solo secundario
- `Current Minute` solo secundario
- `(VWAP) Volume Weighted Average Price - VWAP` solo experimental

## Stop/Limit Price Levels a incluir
- `(DH) Daily High`
- `(SH) Session High`
- `(WH) Weekly High`
- `(DO) Daily Open`
- `(WO) Weekly Open`
- `(DC) Daily Close`
- `(WC) Weekly Close`
- `(SC) Session Close`
- `(VWAP) Volume Weighted Average Price - VWAP` solo experimental

## Stop/Limit Price Ranges a incluir
- `(FP) Fixed pips`
- `(ATR) Average True Range`
- `(BR) BarRange`

## Operators recomendados
- `(=) Equals` solo para tiempo
- `Crosses Above`
- `(>) Is greater`
- `(>=) Is greater or equal`

## Núcleo implementable
La regla base de este grupo debería tomar:
- **1 gate temporal**
- **1 nivel temporal principal**
- **0 o 1 confirmación**

Ejemplo:
- gate: `Bar Hour`
- nivel: `(SH) Session High`
- confirmación opcional: `(ATR) Average True Range`

## Secundarios válidos
- `(DO) Daily Open`
- `(WO) Weekly Open`
- `(DC) Daily Close`
- `(WC) Weekly Close`
- `(SC) Session Close`
- `(VWAP) Volume Weighted Average Price - VWAP`

## Equivalentes que no deben coexistir
No meter juntos como núcleo:
- `Bar Hour + Current Hour`
- `Bar Day Of Week + Current Day Of Week`
- `(DH) Daily High + (SH) Session High + (WH) Weekly High`
- demasiados opens/closes compitiendo con highs como trigger principal

## Qué busca realmente el Builder
- breakout en ventana horaria o semanal útil
- nivel temporal con contexto real
- timing no aleatorio

## Mezclas a evitar
- usar `(=) Equals` fuera del gating temporal
- dejar que `(DO) Daily Open` o `(WO) Weekly Open` compitan con highs como trigger principal
- tratar este grupo como core universal
- meter demasiado calendario y demasiados niveles a la vez

---

# Grupo 5 — Continuación por impulso / re-break

**Jerarquía:** Secundario fuerte

## Intención operativa
Capturar continuación cuando el movimiento ya partió, hizo pausa corta y vuelve a romper high.

No busca compresión previa. No usa rail dinámica como corazón. Vive de **re-break + impulso desplegado**.

## Signals a incluir
- `Awesome Oscillator`
- `Bulls Power`
- `MACD`
- `Momentum`
- `OSMA`
- `ROC`
- `Schaff Trend Cycle`
- `Super Trend` solo secundario
- `Parabolic SAR` solo secundario
- `Bears Power` solo experimental

## Indicators a incluir
- `(AWO) Awesome Oscillator`
- `(BUP) Bulls Power`
- `(MACD) MACD`
- `(MO) Momentum`
- `(OSMA) Moving Average Of Oscillator`
- `(ROC) ROC`
- `(SCHTC) Schaff Trend Cycle`
- `(ST) SuperTrend`
- `(PSAR) Parabolic SAR`

## Stop/Limit Price Levels a incluir
- `(H) High`
- `Highest`
- `Highest in range`
- `(ST) SuperTrend` solo secundario
- `(PSAR) Parabolic SAR` solo secundario

## Stop/Limit Price Ranges a incluir
- `(ATR) Average True Range`
- `(MTATR) Average True Range`
- `(TR) TrueRange`
- `(BR) BarRange`

## Operators recomendados
- `Crosses Above`
- `(>) Is greater`
- `(>=) Is greater or equal`
- `Is rising`
- `(> X) Is greater for X bars`

## Núcleo implementable
La regla base de este grupo debería tomar:
- **1 trigger estructural**
- **1 familia de impulso**
- **0 o 1 confirmación**

Ejemplo:
- trigger: `Highest`
- impulso: `(MO) Momentum`
- confirmación opcional: `(SCHTC) Schaff Trend Cycle`

## Secundarios válidos
- `(ST) SuperTrend`
- `(PSAR) Parabolic SAR`
- `(ATR) Average True Range`
- `(TR) TrueRange`
- `(BR) BarRange`
- `Bears Power` solo experimental

## Equivalentes que no deben coexistir
No meter juntos como núcleo:
- `(MO) Momentum + (ROC) ROC`
- `(MACD) MACD + (OSMA) Moving Average Of Oscillator`
- `(AWO) Awesome Oscillator + (MACD) MACD + (OSMA) Moving Average Of Oscillator`
- `(BUP) Bulls Power + Bears Power`
- `(ST) SuperTrend + (PSAR) Parabolic SAR` como corazón del gatillo

## Qué busca realmente el Builder
- hubo impulso real
- el precio solo respiró, no se revirtió de verdad
- vuelve a romper high
- la entrada LONG intenta montarse en la segunda pata

## Mezclas a evitar
- devolver `(BB) Bollinger Bands` o `(KC) Keltner Channel` al núcleo
- hacer que `(ST) SuperTrend` o `(PSAR) Parabolic SAR` sean el gatillo central
- llenarlo de confirmadores y convertirlo en pseudo Grupo 4
- usar `Momentum` y `ROC` juntos por defecto

---

# Grupo 6 — Breakout post-pullback / reset

**Jerarquía:** Experimental controlado

## Intención operativa
Detectar un reset o pullback dentro de una estructura de breakout, pero entrar solo cuando hay **re-break explícito**.

Este grupo no compra sobreventa por sí sola.

## Signals a incluir
- `CCI`
- `De Marker`
- `Kaufman Efficiency Ratio`
- `Laguerre RSI`
- `QQE`
- `Reflex`
- `RSI`
- `SR Percent Rank`
- `Stochastic`
- `Williams PR`

## Indicators a incluir
### Trigger de re-break
- `Highest`
- `Highest in range`
- `(EMA) Exponential Moving Average`
- `(SMA) Simple Moving Average`
- `(HMA) Hull Moving Average`
- `(KAMA) Kaufman’s Adaptive Moving Average`
- `(ST) SuperTrend`

### Reset / contexto
- `(CCI) Commodity Channel Index`
- `(DE) DeMarker`
- `(KER) Kaufman Efficiency Ratio`
- `(LRSI) Laguerre RSI`
- `(QQE) Quantitative Qualitative Estimation`
- `(RFX) Reflex`
- `(RSI) Relative Strength Index`
- `(SRPC) SRPercRank`
- `(STOCH) Stochastic`
- `(WILL%R) Williams Percent Range`
- `(UI) Ulcer Index` solo experimental

## Stop/Limit Price Levels a incluir
- `Highest`
- `Highest in range`
- `(EMA) Exponential Moving Average`
- `(SMA) Simple Moving Average`
- `(HMA) Hull Moving Average`
- `(KAMA) Kaufman's Adaptive Moving Average`
- `(ST) SuperTrend`

## Stop/Limit Price Ranges a incluir
- `(ATR) Average True Range`
- `(FP) Fixed pips`
- `(BR) BarRange`

## Operators recomendados
- `Crosses Above`
- `(>) Is greater`
- `(>=) Is greater or equal`
- `Is rising`
- `(| > MA) Indicator Above MA`
- `(| > MA) Indicator Crosses Above MA`
- `(< % Rank) Is Lower or Equal Percent Rank` solo si entra `(SRPC) SRPercRank`
- `(> % Rank) Is Greater or Equal Percent Rank` solo si entra `(SRPC) SRPercRank`

## Núcleo implementable
La regla base de este grupo debería tomar:
- **1 trigger explícito de re-break**
- **1 resetter núcleo**
- **0 o 1 secundario**
- **0 o 1 filtro de calidad**

Ejemplo:
- trigger: `Highest`
- resetter: `(RSI) Relative Strength Index`
- secundario: `(SRPC) SRPercRank`
- calidad: `(KER) Kaufman Efficiency Ratio`

## Secundarios válidos
- `(DE) DeMarker`
- `(SRPC) SRPercRank`
- `(LRSI) Laguerre RSI`
- `(KER) Kaufman Efficiency Ratio`
- `(RFX) Reflex`
- `(UI) Ulcer Index` solo filtro experimental

## Equivalentes que no deben coexistir
No meter juntos como núcleo:
- `(RSI) Relative Strength Index + (QQE) Quantitative Qualitative Estimation + (STOCH) Stochastic + (WILL%R) Williams Percent Range`
- `(DE) DeMarker + (SRPC) SRPercRank + (LRSI) Laguerre RSI`
- `(KER) Kaufman Efficiency Ratio + (RFX) Reflex`
- varios triggers de re-break a la vez

## Qué busca realmente el Builder
- hubo pullback o reset
- ese reset no destruyó la estructura
- el precio vuelve a romper una referencia útil
- la entrada LONG se activa recién en la retomada

## Mezclas a evitar
- dejar que el oscilador sea trigger final
- usar operadores de percent rank sin `(SRPC) SRPercRank`
- meter muchos resetters juntos
- transformar el grupo en mean reversion pura

---

# Parking formal normalizado a SQX

## Quedan dentro del universo, pero no como core reusable
- `Directional Index` → Grupo 4 → **Signal**
- `Trend` → Grupo 4 → **Signal**
- `(SRPC) SRPercRank` → Grupo 6 → **Indicator**
- `Bears Power` → Grupo 5 / Grupo 6 → **Signal experimental**
- `(UI) Ulcer Index` → Grupo 1 / Grupo 6 → **Indicator experimental**
- `(VWAP) Volume Weighted Average Price - VWAP` → Grupo 3 → **Indicator / Price Level experimental**
- `(Pivots) Pivots` → Grupo 2 → **Indicator / Price Level secundario**
- `Biggest Range` → Grupo 1 → **Price Range experimental**
- `Smallest Range` → Grupo 1 → **Price Range experimental**

## Quedan fuera del set reusable
- `Candle Patterns`
- `(FIB) Fibo`
- `(HA C) Heiken Ashi Close`
- `(HA H) Heiken Ashi High`
- `(HA L) Heiken Ashi Low`
- `(HA O) Heiken Ashi Open`
- `(MC) Monthly Close`
- `(MH) Monthly High`
- `(ML) Monthly Low`
- `(MO) Monthly Open`

---

# Resumen final de implementación

## Core reusable
Trabajar primero con:
- **Grupo 1**
- **Grupo 2**
- **Grupo 4**

## Secundario / contextual
Agregar después, con disciplina:
- **Grupo 3**
- **Grupo 5**

## Experimental controlado
Solo si quieres explorar más fino:
- **Grupo 6**

## Norma práctica para no inflar search space
Cada regla idealmente debería tener:
- **1 trigger breakout**
- **1 filtro principal**
- **0 o 1 confirmación**
- **0 o 1 buffer/range auxiliar**

Cuando pasas de eso, normalmente ya no estás agregando edge: estás agregando combinatoria con terno.
---

# Inventario pendiente — Builders y estrategias optimizadas existentes

> [!warning] Estado de evidencia
> El owner indicó que ya existen algunos builders asociados a estos grupos y estrategias optimizadas. **No conocemos cuáles, cuántos, dónde están guardados ni sus métricas.** Esta tabla NO afirma que exista al menos un builder por cada grupo, y no es evidencia de que hayan pasado los filtros. Registrar desde los archivos originales antes de marcar un resultado como verificado.

## Registro por grupo (rellenar únicamente con evidencia)

| Grupo | Builder(s) reales / IDs | Instrumento y TF | Versión SQX | Estrategias y optimizaciones | Referencias de archivos / evidencia | Estado |
|---|---|---|---|---|---|---|
| G1 | Pendiente de inventario | Por verificar | Por verificar | Por verificar | Por verificar | **Sin auditar** |
| G2 | Pendiente de inventario | Por verificar | Por verificar | Por verificar | Por verificar | **Sin auditar** |
| G3 | Pendiente de inventario | Por verificar | Por verificar | Por verificar | Por verificar | **Sin auditar** |
| G4 | Pendiente de inventario | Por verificar | Por verificar | Por verificar | Por verificar | **Sin auditar** |
| G5 | Pendiente de inventario | Por verificar | Por verificar | Por verificar | Por verificar | **Sin auditar** |
| G6 | Pendiente de inventario | Por verificar | Por verificar | Por verificar | Por verificar | **Sin auditar** |

## Ficha mínima por Builder real

Registrar una ficha por Builder/campaña que aparezca en el inventario; usar identificadores reales, sin suponer un Builder por grupo.

| Campo | Qué recuperar |
|---|---|
| Identidad | ID/nombre exacto en SQX, grupo lógico G1–G6, ubicación de `.cfx` o configuración exportada, responsable y fecha |
| Entorno | SQX build exacto (136/142/144), máquina o worker, dataset/proveedor, símbolo real, H1, LONG |
| Datos de mercado | Zona horaria/DST, sesión, rango histórico, precisión y versión/snapshot del histórico, costes de ejecución |
| Search space | Signals, Indicators, Price Levels, Price Ranges, Operators activos; parámetros `Min/Max/Step`, pesos, condiciones permitidas y exclusiones |
| Generación | Modo de búsqueda, configuración genética, fechas, universo de estrategias y criterios de ranking/aceptación |
| Evidencia | Configuración, logs o reportes exportados, snapshots, databank y referencias con checksums cuando existan |
| Resultado | Cantidad construida/aceptada, causa de descartes, estrategias candidatas; desconocido hasta respaldo verificable |

## Ficha mínima por estrategia optimizada

| Campo | Qué recuperar |
|---|---|
| Identidad y linaje | Referencia y nombre exactos de la estrategia, Builder/grupo de origen, versión de parámetros, hashes/artefactos SQX disponibles |
| Mercado y lógica | Símbolo, timeframe, LONG, entrada real (trigger/filtro/confirmación), gestión de salida y dinero, parámetros finales |
| Histórico | IS/OOS, fecha efectiva de construcción, feed y cortes temporales; no confundir período de entrenamiento con pre-Echo |
| Métricas comparables | Trades, Net Profit, Profit Factor, Drawdown, Return/DD, estabilidad por períodos, exposición y costes, según reportes disponibles |
| Robustez y optimización | Evidencias de Retester, SPP, Monte Carlo, Walk-Forward/Optimizer si realmente se ejecutaron; distinguir de simple optimización IS |
| Estado de selección | Candidata / en validación / descartada / ratificada por owner; nunca marcar ratificada por rendimiento aislado |
| Forge y Echo | ID real de import/FlowRun/SelectionSnapshot si existe, resultados SQX/MT5 y eventual ID de estrategia ingerida en Echo; vacío hasta demostrarse |

## Regla de trazabilidad

**Una estrategia optimizada no es automáticamente una estrategia finalista ni una estrategia inyectada.** Mantener las etapas separadas: artefacto SQX encontrado → configuración reconstruida → resultados históricos corroborados → elegibilidad y aprobación → importación/ejecución en Forge → evidencia y reconciliación SQX/MT5 cuando aplique → integración/ingesta Echo con contratos vigentes → verificación en Echo/The Lab. Anotar fallos y desviaciones por artefacto exacto, no solo por nombre humano.

## Próximo trabajo sobre lo ya construido (orden práctico)

1. **Inventariar sin ejecutar campañas nuevas:** localizar los Builders existentes, los datasets/cfgs y las estrategias optimizadas; clasificarlos por G1–G6 y símbolo sin inferir ausencias.
2. **Congelar evidencia reproducible de cada Builder:** export/config de SQX, calibración por símbolo, series/sesiones, coste y ranking; contrastar contra el set que se documenta aquí para distinguir intención y ejecución real.
3. **Reconciliar estrategias ya optimizadas:** obtener refs de SQX, archivos de estrategia, parámetros, operaciones y reportes; identificar cuál optimización se realizó realmente y qué tests siguen pendientes.
4. **Seleccionar una cohorte pequeña de prueba:** comenzar por una estrategia con artefactos completos, no por la mejor curva aislada; validación y aprobación humana antes de ampliar.
5. **Usar el intake realmente vigente de Forge:** confirmar formato y contrato con [[Echo Forge — Operación Real V2]] y [[Echo Forge — Campaign 001]] antes de alimentar el watcher o lanzar importaciones; no reutilizar nombres de ficheros ni convenciones de campañas antiguas sin verificar.
6. **Verificar toda la cadena antes de Echo:** importación, IDs/linaje, fidelidad entre resultados SQX/MT5 cuando corresponda, artefactos y manifiestos durables; no dar por completado el handoff por un FlowRun terminal aislado.
7. **Integrar/injectar en Echo solo cuando el contrato esté disponible:** comprobar idempotencia y unicidad de identidad, historia pre-Echo, estrategia registrada, habilitación operacional y visualización en [[Echo — Producto Integrado]] / The Lab. El estado real de la integración debe verificarse en las autoridades de Echo y Forge.
8. **Recién después explorar nuevas búsquedas:** medir rendimiento de cada grupo y decidir ajustes basados en yield y supervivencia OOS/robustez, no por preferencia estética de indicadores.

## Dependencias y límites actuales

- La nota [[Echo Forge — Operación Real V2]] registra certificación técnica E2E de Forge 0.3.2 al 2026-10-19 y una fase de operación real/Integration V2. **Eso no verifica importación ni ingesta Echo de las estrategias descritas aquí.**
- [[Echo — Producto Integrado]] documenta la evolución de The Lab y el vínculo Forge→Echo, pero la disponibilidad del contrato específico de ingesta y su despliegue físico deben confirmarse con evidencia actual antes de ejecutar.
- El material IMOX debe conservar su procedencia y separación respecto de desarrollos propios Echo/Forge conforme a las restricciones vigentes del owner. No compartir la implementación privada fuera del entorno autorizado.

## Fuente y enlaces

- **Definición de grupos:** `sqx_br_h1_long_grupos_reusable.md` (material fuente recibido en la conversación del proyecto StrategyQuant, transcrito íntegramente en la sección central de esta nota).
- **Proyecto:** [[Estrategias IMOX — Forex y CFD con Echo Forge]].
- **Factory/ingesta:** [[Echo Forge — Operación Real V2]], [[Echo Forge — Campaign 001]].
- **Producto receptor:** [[Echo — Producto Integrado]].
- **Límite documental:** la nota principal del proyecto no fue modificada aquí; este documento complementario evita sobrescribir contenido existente aún no recuperado del vault.
