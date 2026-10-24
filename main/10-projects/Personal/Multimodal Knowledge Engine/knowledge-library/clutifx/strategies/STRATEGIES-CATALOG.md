---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/README|Clutifx compiled]]"
aliases:
  - clutifx strategies master
  - catálogo estrategias clutifx
tags:
  - kind/doc
  - area/echo
  - tech/strategy-research
created: "2026-10-23"
updated: "2026-10-23"
---

# CLUTIFX-STRATEGIES-MASTER — Catálogo exhaustivo de estrategias del curso Clutifx

**Documento maestro de la misión GOD (Clutifx Strategy Extraction & Objective Formalization, 2026-10-23).** Superficie DERIVADA de investigación: vive en Echo Futures y NO modifica la biblioteca canónica de MKE. Fuente de autoridad: la biblioteca por capítulos (`10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/`), snapshot verificado `7fdaac6b` (12 capítulos · 1.608 claims = 1.584 SUPPORTED consumibles + 15 UNCERTAIN + 9 superseded · 1.033 frames · 19 docs compilados).

**Contrato de este catálogo**: sólo conocimiento `ACTIVE ∧ SUPPORTED ∧ evidencia resuelta` del curso. Se preservan los modalizadores dichos («normalmente», «yo creo», «a lo mejor»): una regla [probabilística] NO es una regla [dicha]. Las promesas del instructor («no falla», «imparables») son frases dichas, no validaciones. **El curso no aporta backtests ni winrates medidos**: este catálogo especifica; no valida. Nada de lo aquí atribuido a Clutifx puede presentar parámetros inventados como enseñados.

**Cómo resolver citas**: `chNN c-XXXX` = claim del capítulo, resoluble en `…/clutifx/chNN-*/CLAIMS.md#c-XXXX`; `q-chNN-YYY` = pregunta abierta en `…/clutifx/chNN-*/OPEN-QUESTIONS.md#q-chNN-YYY`. Los wikilinks completos viven en los docs compilados de la biblioteca; aquí se usa la forma corta por legibilidad.

---

## 0. El sistema en una página

El curso enseña **UN sistema de trading** con variantes de entrada y de sesión, no una lista de patrones independientes. La mecánica causal única:

```text
(1) BIAS      : procedimiento top-down marcando RANGOS desde TF alta (años → días)
                hasta TF de sesión; el bias "normalmente" lo dan 6h–3D (ch03 c-0050)
(2) DOL       : objetivo de liquidez = extremo de rango(s) pendiente(s) hacia el bias
                ("en rangos de TF más alta, vela de la izquierda predominando e ir
                para allí" ch03 c-0070). DOL ≠ DXY (resolución q-ch03-001).
(3) ESPERA    : TURTLE SOUP a favor (toma de liquidez + reacción) y RANGOS A FAVOR
                (sin reiniciados en contra). Sin rango a favor no hay entrada
                (ch04 c-0044). Red flags excluyen (ch09).
(4) ENTRADA   : ideal = manipulación (Power of 3) de la vela clave de la sesión,
                refinando por temporalidades hasta 15m; alternativas = Turtle Soup
                directo, PDM/order block confirmado, rango pendiente hacia DOL.
(5) GESTIÓN   : stop bajo el Turtle Soup; parciales 50/80% + break even ESTRUCTURAL
                (nunca "en tal R"); salida por objetivo o por tiempo (vela de las 5).
(6) SALIDA    : al DOL; o vela de las 5 cercana al target; o red flags en pleno trade.
```

Todo lo demás del curso son: los **componentes** que detectan cada pieza (§2), las **estrategias completas** que los combinan en sesiones/escenarios (§3), los **setups parciales** y matices (§4), las **reglas de gestión** (§5), los **filtros/red flags** (§6) y el **procedimiento de análisis** (§7). La tabla de correspondencia claim → destino está en `CLUTIFX-SOURCE-COVERAGE.md`.

**§0.1 — El checklist de 4 preguntas del propio curso** (ch07 c-0229, síntesis oficial del instructor): antes de operar una vela preguntar — **(1) ¿Está el Turtle Soup ya hecho? (2) ¿Está el DOL tomado? (3) ¿Tengo rangos a favor? (4) ¿Hay noticias en la vela que opero?** — "yo creo que solo haciéndoos estas cuatro preguntas podéis determinar ya si vuestra vela va a ser la que manipula, va a ser la que distribuye, va a ser un reversal o va a ser una continuación" (c-0230, criterio creído dicho); mejor "antes de tomar el trade o mientras estáis analizando" (c-0231). En el catálogo: (1)→CMP-005, (2)→CMP-017, (3)→CMP-003/004, (4)→CMP-021/STR-008.

---

## 1. Glosario operativo literal (definiciones del instructor)

| Término | Definición dicha (fuente) | Estado |
|---|---|---|
| **Rango (base)** | Una vela —"no tiene por qué ser la siguiente"— **toma un extremo de la vela anterior y cierra dentro** de la vela anterior (ch01 c-0005/c-0006/c-0009). Rango alcista = toma low y cierra adentro; bajista = espejo. Pasa en todas las temporalidades (ch01 c-0012). | Regla dicha |
| **Cadena de rangos** | El precio "actúa como una cadena": forma un rango y va a completarlo; crear rangos en dirección opuesta y completarlos "es literalmente la manera en que funciona el precio" (ch01 c-0016/c-0017; ch02 c-0041). Negación preservada: se completan "siempre — no siempre" (ch01 c-0031). | Regla dicha con negación |
| **Rango pendiente** | Vela que abre por debajo (con objetivo arriba), toma el low y cierra adentro **o reacciona**; "se forma a favor de nuestra tendencia" (ch01 c-0041/c-0042). | Regla dicha |
| **Rango reiniciado** | La siguiente vela abre por arriba y toma el high (con objetivo arriba); si cierra adentro se forma rango bajista: "reiniciar antes de ir hacia el objetivo" (ch01 c-0044/c-0045/c-0047). Bloquea la entrada hasta eliminarse (ch03 c-0029). | Regla dicha |
| **Rangos a favor / en contra** | "A favor" = sin reiniciados formándose contra tu dirección (ch03 c-0029/c-0030). Con rango en contra delante no hay operación (ch03 c-0056). Invalidación dura acotada: con rangos en contra activos "no podemos estar tomando longs" (ch09 c-0007/c-0012). | Regla dura acotada |
| **Turtle Soup (TS)** | **Tomar el alto (o bajo) para crear/completar un rango y tener la reacción después de tomarlo** (ch01 c-0059). Condición necesaria: "si sigue bajando, no es ningún Turtle Soup; tiene que ser toma de liquidez **y** reacción" (ch01 c-0063). "Si no es Turtle Soup + reacción, no es Turtle Soup". Marca que el inicio del movimiento puede darse ya (ch01 c-0066). Nombres dichos: "toma de liquidez", "toma del [extremo]". | Regla dicha |
| **Intra-Turtle Soup** | TS extra dentro del mismo rango tras un TS previo: "tomar y reacción y cerrar dentro del mismo rango" (ch01 c-0068/c-0075). "¿Pasa muchas veces? — No. Algunas veces" (ch01 c-0073). Si la vela sigue cerrando dentro, el rango sigue operativo (ch01 c-0070). | Regla dicha, frecuencia baja dicha |
| **DOL** | Objetivo/liquidez hacia donde va el precio (garble "el doble/doll"; literal en ch03). "En rangos de temporalidad más alta, vela de la izquierda predominando e ir para allí" (ch03 c-0070). Jerarquía de pizarra: mensual/semanal = contexto; 3D/2D/1D = DOL medio plazo; 12h–4h = DOL de sesión; <4h = entradas (ch03 c-0206–c-0209). **DOL ≠ DXY** (q-ch03-001 resuelta; 8 claims superseded por confusión histórica). | Regla dicha |
| **PDM** | "La reacción en el alto del rango" (ch04 c-0017); en ch03: el precio se apoya en el low del rango sin romperlo y lo usa de soporte real (ch03 c-0092). Con PDM + reacción no se vende aunque el DOL esté abajo (ch03 c-0213). Expansión de la sigla NO dicha (q-ch03-004). | Concepto dicho, sigla sin expandir |
| **Order block (OB)** | Vela cuyo **cierre por fuera** confirma el cambio: "se considera una vez que el precio HA CERRADO POR FUERA de esa vela" (ch04 c-0034); "asegurar que la tendencia ya ha cambiado" (ch04 c-0039). En failure swing: "lo que podría ser el cambio de tendencia" (ch06 c-0038). | Regla dicha |
| **Power of 3 (P3)** | "Cómo se forma una vela": **apertura, manipulación, distribución y cierre** (ch01 c-0116/c-0117). Regla de compras: "las compras ideales siempre, siempre, siempre van a estar en esta etapa de manipulación de la vela" (ch01 c-0121). Procedimiento: esperar la apertura de la vela clave (p.ej. 4h a las 5) y entrar en su P3 (ch01 c-0122). | Regla dicha con énfasis |
| **Failure swing (FS)** | El precio **no puede hacer el nuevo extremo**: falla al intentarlo y va directo al otro lado sin romperlo (ch06 c-0004, espejo c-0044/c-0046; ch01 c-0098/c-0101). El rango "se puede considerar activado" aunque no tomó el extremo (ch06 c-0028, "en algunos casos"). NO predecible: "hay que ver cómo pasa y luego identificarlo" (ch06 c-0016). Negación: un extremo al final de la hora NO obliga a FS (ch06 c-0011/c-0015). | Regla dicha con límites |
| **SMT** | Divergencia de extremos entre pares correlacionados (ch05 c-0004). Redefinida para esta estrategia: detectar "rangos que ya pueden estar completados y no nos hemos enterado" (ch05 c-0002). Esencia: "se tendría que haber hecho el nuevo bajo y eso no ha pasado" (ch05 c-0089). No implica reversión necesaria (ch05 c-0012). | Regla dicha |
| **DXY** | Índice dólar, correlación −1 con euro/libra (ch05 c-0085); "funciona igual que en euro y libra — como otro par igual" (ch05 c-0091). | Concepto dicho |
| **Expansión** | Movimiento direccional hacia el objetivo; "se trata de intentar coger la expansión, no de forzar que en tu sesión pasen las cosas" (ch02 c-0080). "Normalmente la expansión se va a dar o en London o en New York" (ch07 c-0137). Mercado con "tres momentos: consolidación, expansión y reversa" (ch09 c-0062). | Regla probabilística dicha |
| **Red flag** | "Señales negativas que nos pueden indicar que no tenemos que operar" (ch09 c-0001) — definición probabilística; sólo 2 son pausas duras acotadas (rangos en contra; velas inside). Ver §6. | Definición dicha |

**Horario del curso**: todo en **hora New York (UTC-4 dicho)**, "que quede clarísimo" (ch02 c-0012). La implementación debe anclar a `America/New_York` IANA y manejar DST (el UTC-4 dicho del material es un supuesto didáctico de verano). Horas clave: **3, 5, 9** (±8 con duda, q-ch09-001); aperturas de velas 4h: 17/21/01/05/09/13; 8h: 17/01/09; 12h: 17/05; 6h: 23/11/05…; sesiones como velas 4h: London = vela de la **1**, NY arranca en la vela de las **5**, expansión NY = vela de las **9**; marco alternativo 6h: 23/17/11 (ch02 c-0011–c-0024, c-0062–c-0077; ch07 c-0002–c-0009). Precaución en el minuto 59 de horas clave (ch02 c-0064, probabilística).

**Lista base de temporalidades** (ch02 c-0003, "para dar una base y limitar"): 3M, 1M, 6M, 3S, 2S, 1S, 3D, 2D, 1D, 12h, 8h, 6h, 5h, 4h, 3h, 2h, 1h, 90m, 144m, 45m, 30m, 15m. Cualquier TF vale ("es un algoritmo", ch02 c-0008); el instructor "nunca baja de 15" (límite personal, ch02 c-0009/ch04 c-0011). 12 meses "pocas veces rentable" (ch02 c-0002).

---

## 2. Componentes técnicos (CLF-CMP) — piezas detectables

Cada componente es una condición aislada (Nivel 1-2 del curso). La objetivización computable completa (alternativas de detector, fórmulas, causalidad) está en `CLUTIFX-OBJECTIVE-DETECTORS.md`; aquí va la definición fuente + su rol.

| ID | Componente | Definición fuente | Rol en el sistema |
|---|---|---|---|
| CLF-CMP-001 | **Rango formado** | Vela toma extremo de la anterior y cierra dentro (ch01 c-0005+). Borde: cierre "apenas fuera" que con zoom parece dentro se considera rango (ch07 c-0065); tras TS+reacción no se exige cierre (ch02 c-0035); el rango de FS cuenta sin toma (ch06 c-0028). | Átomo de toda la lectura |
| CLF-CMP-002 | **Cadena de rangos por TF** | Marcar rangos bajando temporalidades; rangos en dirección al mismo sitio = narrativa (ch08 c-0022/c-0069; ch02 c-0054) | Derivación del bias (§7) |
| CLF-CMP-003 | **Rango pendiente a favor** | ch01 c-0041/c-0042 | Habilita entrada; 3ª entrada del esquema (con P3) |
| CLF-CMP-004 | **Rango reiniciado en contra** | ch01 c-0044/c-0045; dura "hasta que reinicia o crea pendiente" (ch09 c-0011) | Bloqueo de entrada (red flag 1) |
| CLF-CMP-005 | **Turtle Soup** | ch01 c-0059/c-0063 | Trigger ideal de entrada; requisito "siempre a favor de tu tendencia" (ch02 c-0081) |
| CLF-CMP-006 | **Intra-Turtle Soup** | ch01 c-0068/c-0075 | Reentrada (§5) |
| CLF-CMP-007 | **DOL identificado** | ch03 c-0070 + jerarquía c-0206+ | Objetivo; "lo más importante no es la entrada sino saber dónde está el DOL" (ch04 c-0058) |
| CLF-CMP-008 | **PDM** | ch04 c-0017; ch03 c-0092/c-0213 | Entrada 2ª del esquema; filtro de no-venta |
| CLF-CMP-009 | **Order block (cierre fuera)** | ch04 c-0034/c-0039 | Confirmación de cambio de tendencia |
| CLF-CMP-010 | **Power of 3 de vela clave** | ch01 c-0116–c-0124 | Ventana temporal de entrada ideal |
| CLF-CMP-011 | **Failure swing** | ch06 c-0004/c-0028 | Rango activado sin toma; objetivo inalcanzable sin el concepto (ch06 c-0057) |
| CLF-CMP-012 | **SMT caso 1** (par crea rango y el otro no) | ch05 c-0069–c-0072 | Entrada sin esperar completación propia (ch05 c-0017) |
| CLF-CMP-013 | **SMT caso 2** (completación asimétrica del objetivo) | ch05 c-0074/c-0075; negación c-0076 | Reversal temprano / gestión |
| CLF-CMP-014 | **SMT caso 3** (pendiente que el otro par no crea) | ch05 c-0078–c-0083 | Entrada anticipada por rango del correlacionado |
| CLF-CMP-015 | **DXY simétrico** | ch05 c-0085–c-0097 | Confirmación/salida anticipada |
| CLF-CMP-016 | **Vela inside** | No toma low ni high de la anterior (ch09 c-0025–c-0037) | Pausa dura hasta tomar extremo (ch09 c-0084/c-0085) |
| CLF-CMP-017 | **Objetivo tomado** | Precio llegó al objetivo (ch09 c-0040+); variante de sesión: levantarse con objetivo 1D/2D/1S ya tomado (ch09 c-0051/c-0053) | Red flag 3 (probabilística + riesgo consciente c-0107) |
| CLF-CMP-018 | **Par correlacionado completó** | ch09 c-0126–c-0131 | Red flag 4; mitigación parciales/BE (c-0129) |
| CLF-CMP-019 | **Apertura de vela tomando extremo** | "Abrir por arriba es que la vela tome el high de la vela anterior" (ch09 c-0020/c-0023); el mismo hecho a favor crea el rango a favor (c-0021/c-0022) | Lectura direccional de aperturas |
| CLF-CMP-020 | **Secuencia 1-5-9** | Operar la 5 con TS en la 1; si expande la 1, la 5 puede ser TS de reversal y la expansión va a la 9; "expansión, expansión, expansión" no (ch09 c-0057–c-0059, alcance del "normalmente" UNCERTAIN c-0063/q-ch09-010) | Timing de sesión |
| CLF-CMP-021 | **Vela clave de noticia** | La noticia marca qué vela desplaza (ch10 c-0023/c-0024) | Selección de vela operable |
| CLF-CMP-022 | **Cuerpos cierran hacia el rango** | "Los cuerpos respetan brutalmente el rango" (ch03 c-0108, ejemplo); "todas las velas cierran con el cuerpo ahí… porque va a ir a completarlo" (ch07 c-0218, ejemplo) | Confirmación [ejemplo] |
| CLF-CMP-023 | **Vela de la izquierda manda** | Entre rangos/velas simultáneos, la de la izquierda predomina (ch03 c-0059/c-0112/c-0163; ch03 c-0070) | Desempate de rangos |
| CLF-CMP-024 | **High Time Frame manda** | "Porque High Time Frame manda" (ch02 c-0088); TS en TF baja ⇒ "es más probable que el precio cree los rangos en las grandes" (ch07 c-0233) | Jerarquía entre TFs |

---

## 3. Familias y estrategias completas (CLF-FAM / CLF-STR)

Nivel 3 = conjunto implementable (contexto + activación + entrada + invalidación + salida + reglas temporales). Cada ficha sigue el contrato de la misión; campos no definidos por el instructor se marcan `[PROPUESTA]` o `[PENDIENTE]` — nunca como enseñados.

### CLF-FAM-001 — Continuación expansiva hacia el DOL (el sistema base)

Mecanismo causal: el precio completa cadenas de rangos en dirección a objetivos de liquidez (DOL); el trader se monta en la expansión cuando la estructura de rangos está a favor, con Turtle Soup como detonante de liquidez. Todas las estrategias de esta familia comparten: derivación de bias (§7), DOL identificado, rangos a favor, stop bajo TS, gestión de §5.

---

#### CLF-STR-001 — London ideal: P3 de la vela de la 1 tras Turtle Soup hecho

- **STRATEGY_ID**: CLF-STR-001 · **FAMILY_ID**: CLF-FAM-001 · **STATUS**: `EXTRAIDA_COMPLETA`
- **SOURCE**: ch07 §3 (c-0010, c-0005–c-0007, c-0030/c-0031/c-0038, c-0214); ch02 c-0081; ch01 c-0121/c-0122; atlas ch07 E1–E3.
- **Concepto original**: "El escenario ideal: tener el target sub [TS] ya hecho con un rango claro para ir para allí… la meta es intentar entrar en el power 3 de esta vela" (la vela de la 1, "la vela que operamos nosotros en London"). Preferencia declarada del instructor: "lo que más nos gusta es que en London sea el Tartel Soup, o la vela siguiente al Tartel Soup" (ch07 c-0038).
- **Setup claro**:
  1. *Contexto*: bias derivado (ch03); DOL de sesión claro e intacto (12h–4h); TS a favor YA hecho (a menudo en la vela diaria o de la 21/1); ningún rango reiniciado en contra en las TFs de sesión.
  2. *Vela operable*: la vela 4h de la **1 NY** (marco 21/17/1); el instructor entra al gráfico "a las 2:30 normalmente" (ch07 c-0006) — si la vela ya hizo un pequeño P3, se entra en el tramo en curso.
  3. *Entrada*: en la **manipulación del Power of 3** de esa vela (compras en contexto alcista); refinando por temporalidades (STR-005) hasta rangos a favor en 1h→15m.
  4. *Confirmación deseada*: velas que abren tomando el extremo **en tu dirección** (CLF-CMP-019); cuerpos cerrando hacia el rango objetivo [ejemplo].
  5. *Invalidación*: cierre fuera del rango base (ch01 c-0076); completitud low+alto del rango (ch01 c-0078); formación de rango en contra (ch09).
  6. *Stop*: debajo del Turtle Soup (ch01 c-0067; ch11 c-0021/c-0023). *Salida*: DOL o vela de las 5 (§5).
- **Señal LONG/SHORT**: la simetría del RANGO base está dicha ("lo mismo pero al revés", ch01 c-0007) y el TS tiene su enunciado espejo (ch01 c-0065); los ejemplos cubren ambos lados (GBPJPY long, EUR continuación, venta contra tendencia). **Matiz de asimetría**: pendiente/reiniciado y PDM-soporte se DEFINEN sólo en lado alcista en ch01/ch03 (c-0041/c-0044/c-0092); el uso bajista existe por espejo en la práctica (ch03 c-0182 abrir-por-arriba→bearish; ch04 PDM en el alto como lectura contextual q-ch04-002) — la simetría SHORT es fuente-por-uso, no definición literal.
- **Temporalidades**: análisis 1 año→15m (§7); ejecución 4h→1h→15m. **Sesión**: London (vela de la 1). **Instrumentos enseñados**: Forex mayor (EURUSD/GBPUSD/GBPJPY).
- **Adaptación NQ**: `NQ_ADAPTATION_HYPOTHESIS` — mecánica genérica aplicable, pero el ancla de sesión London-1-NY es de mercado FX; para NQ el ancla debe redefinirse a sesiones CME (Asia/London/NY como velas de contexto) como hipótesis explícita. Datos: 1m suficiente para todo el pipeline.
- **Parámetros taught vs propuestos**: taught = horas 1/2:30/5, marcos 4h/6h, TFs de refinado, stop bajo TS. `[PROPUESTA]`: tolerancia del "cierra dentro" (ε de borde ch07 c-0065), definición intrabar de "reacción", ventana máx de espera del refinado.
- **Tests mínimos**: no-lookahead del rango (¿extremo y cierre conocidos al momento de decisión?), causalidad del TS intrabar, sesión/DST, LONG/SHORT simetría, reproducibilidad.

---

#### CLF-STR-002 — Rango pendiente hacia el DOL ("precisión máxima")

- **STRATEGY_ID**: CLF-STR-002 · **FAMILY_ID**: CLF-FAM-001 · **STATUS**: `EXTRAIDA_COMPLETA`
- **SOURCE**: ch07 c-0024/c-0032 (escenario 3), c-0091/c-0113/c-0114 ("a esto es lo que os va a dar la precisión máxima"), c-0038 (preferencia); ch04 c-0021/c-0023 (3ª entrada del esquema: P3 + rango pendiente); ch03 c-0087/c-0012.
- **Concepto**: el TS ya pasó (a menudo en la vela diaria: "la activamos aquí por debajo, hacemos el tarde sub, esto se convierte en el dol") y se llega a la sesión ya desplazados: "esperar un rango a favor nuestro para llegar hasta el gol".
- **Setup claro**:
  1. *Contexto*: bias + DOL claro; una primera expansión ya ocurrió (la zona óptima quedó lejos).
  2. *Espera*: un **rango pendiente a favor** (CLF-CMP-003) formándose en dirección al DOL — típicamente pullback en TF de sesión (4h/1h). El pendiente puede ahorrar la espera del reiniciado (ch03 c-0087).
  3. *Entrada*: al crearse el rango a favor, en su manipulación/P3 (si la vela es de 8h, el P3 de una 4h — ch04 c-0021/c-0023); refinado opcional a 15m.
  4. *Invalidación*: el pendiente se convierte en reiniciado en contra (cierra al otro lado); objetivo ya tomado antes de entrar (red flag 3).
  5. *Stop*: bajo el TS/pendiente; *salida*: DOL o vela de las 5.
- **Adaptación NQ**: `NQ_DIRECTLY_TESTABLE` (mecánica pullback-hacia-objetivo puramente estructural, sin ancla FX específica; el "objetivo" se deriva del propio NQ). `[PROPUESTA]`: qué TF define el objetivo (4h/1D) como eje experimental.

---

#### CLF-STR-003 — New York continuación: la vela de las 9

- **STRATEGY_ID**: CLF-STR-003 · **FAMILY_ID**: CLF-FAM-001 · **STATUS**: `EXTRAIDA_COMPLETA`
- **SOURCE**: ch07 §5 (c-0134–c-0146); ch09 c-0057–c-0059 (secuencia 1-5-9).
- **Concepto**: "En New York normalmente lo que vamos a encontrar es reversal o continuación" (c-0134). Caso continuación: los rangos ya creados y "la vela anterior es la que nos crea el Tartle Soup" → en la vela de NY "ya es subarnos al movimiento" — esa vela es la de las **9** (c-0145). "No lo llamaría reversal… sería como buscar la vela que tiene la expansión" (c-0146).
- **Setup claro**:
  1. *Contexto*: bias + DOL no tomado; TS creado por la vela previa (la de las 5); rangos a favor.
  2. *Vela operable*: 4h de las **9 NY** (apertura USA 8:00–8:30, noticias 8:30 — ver STR-009).
  3. *Entrada*: en el P3/manipulación de la vela de las 9 en la dirección de continuación; "estar posicionados en la mejor zona" porque es incierto si expande esta o la siguiente (c-0160/c-0161).
  4. *Invalidaciones*: cierre de la vela de las 5 en contra que "completa el rango" y se lleva la expansión (c-0166–c-0168: "cómo abren las velas" es la clave); si expandió la 1, la 5 puede ser TS de reversal y la expansión pasar a la 9 (ch09 c-0058) — ese día la 9 ES la continuación pero tras TS en la 5.
  5. *Stop/salida*: ídem familia.
- **Adaptación NQ**: `NQ_ADAPTATION_HYPOTHESIS` (ancla 9:00 FX-NY ≈ pre-open NQ 9:30 CT; la vela de las 9 NY del curso solapa la apertura cash USA — para NQ el eje natural es la apertura 9:30 ET; propuesta experimental: anclar a 9:30-9:45 ET).

---

#### CLF-STR-004 — New York reversal: la vela de las 5 tras objetivo completado

- **STRATEGY_ID**: CLF-STR-004 · **FAMILY_ID**: CLF-FAM-001 · **STATUS**: `EXTRAIDA_COMPLETA`
- **SOURCE**: ch07 c-0147/c-0148/c-0150; ch02 c-0068/c-0076; ch08 c-0084/c-0085 (vender mientras se forman rangos alcistas: prohibido; vender arriba mientras se forman los bajistas).
- **Concepto**: yendo a por el objetivo bajista, London lo completa durante London → "en la vela de las 5 [tomamos] el low de la vela anterior y crear un rango bullish después de completar un rango bearish, pues lo que vamos a esperar para este día en New York es una reversión" — al menos hasta donde marquen rangos de 6–8h (c-0147/c-0148/c-0150). Antecedente ch02: completado el objetivo, "en la vela de las 5 tomar el low, formar un nuevo rango y en NY la reversión" (c-0068); "si ya completó el objetivo bajista, hace nuevo low y ves reacción, esta vela va a ser la que vas a querer operar para NY" (c-0076).
- **Setup claro**:
  1. *Contexto*: objetivo (DOL de sesión o intermedio) completado durante London; bias de reversión acotado por los rangos 6–8h.
  2. *Trigger*: vela 4h de las **5** toma el low de la vela anterior (CLF-CMP-019) y crea rango alcista tras el rango bajista completado; reacción visible.
  3. *Entrada*: P3 de la vela de las 5 dirección reversión; o esperando TS del rango nuevo.
  4. *Invalidación*: la vela de las 5 cierra alcista completando el rango previo → sin expansión hoy, esperar al día siguiente (ch07 c-0166–c-0168); nuevo objetivo tomado inmediatamente.
  5. *Stop*: bajo el low del reversal; *salida*: extremo de los rangos 6–8h (objetivo acotado dicho).
- **Regla negativa asociada** [dura acotada]: "Nunca vendáis mientras se forman rangos alcistas; tiene que ser aquí arriba, mientras se están formando los rangos bajistas" (ch08 c-0084/c-0085).
- **Adaptación NQ**: `NQ_ADAPTATION_HYPOTHESIS` (ancla vela de las 5 = 5:00 NY FX; para NQ propuesta: vela 4h de 5:00 ET como ancla de sesión NY futura + open cash como alternativa).

---

#### CLF-STR-005 — El refinado multi-temporalidad (entrada comprimida)

- **STRATEGY_ID**: CLF-STR-005 · **FAMILY_ID**: CLF-FAM-001 · **STATUS**: `EXTRAIDA_COMPLETA` (como procedimiento de entrada transversal)
- **SOURCE**: ch04 §2 (c-0007–c-0014, c-0063–c-0069); ch08 c-0022/c-0069; ch07 c-0214.
- **Concepto**: "ir bajando de temporalidad para ir comprimiendo el precio — lo que llamamos refinar la entrada" (ch04 c-0013). 8h→4h→1h→15m "va a pasar lo mismo" (fractalidad). Entradas ideales "bien dentro de un rango de 15 minutos" (c-0063); límite personal dicho: "yo ya nunca bajo de 15" (c-0011). Matiz honesto: su win rate es mejor "si no intenta llegar tan a la perfección" (c-0069).
- **Setup claro (procedimiento)**:
  1. Identificada la entrada en TF de sesión (STR-001..004), bajar una TF y buscar el mismo fenómeno (rango a favor + TS) en la TF siguiente.
  2. Repetir hasta 15m (o parar antes si el rango está claro).
  3. Entrar cuando "lo has comprimido tanto que no puede hacerlo más" (c-0067), con el precio a favor ("yo siempre entro con el precio a favor mío ya", c-0040 [personal]).
  4. Stop bajo el TS de la TF de entrada; el resto del plan hereda de la estrategia padre.
- **Regla clave del refinado**: "cómo sabías que en London no tenías que comprar: porque tú siempre quieres esperar a tener los rangos activos a tu favor antes del trato sub" (ch07 c-0214, "súper clave").
- **Adaptación NQ**: `NQ_DIRECTLY_TESTABLE` (procedimiento estructural puro). `[PROPUESTA]`: escalón exacto de TFs (8h→4h→1h→15m vs 4h→1h→30m→15m) como eje experimental. **Tensión fuente no resuelta**: "yo ya nunca bajo de 15" (ch04 c-0011, límite personal) vs "hasta 5 minutos para la entrada más perfecta" (ch04 c-0067/c-0068) — el propio capítulo deja ambas dichas; el eje experimental del refinado incluye 15m como piso conservador y la tensión queda declarada.

---

### CLF-FAM-002 — Failure swing: rango activado sin toma del extremo

#### CLF-STR-006 — Entrada por failure swing identificado

- **STRATEGY_ID**: CLF-STR-006 · **FAMILY_ID**: CLF-FAM-002 · **STATUS**: `EXTRAIDA_COMPLETA`
- **SOURCE**: ch06 completo (c-0004–c-0063); ch07 c-0197–c-0206 (resolución NY); ch01 c-0098/c-0101.
- **Concepto**: el precio falla al intentar el nuevo extremo y "va directo al otro lado" sin romperlo; el rango "se puede considerar activado" aunque no tomó el high (ch06 c-0028, "en algunos casos"). Targets que sin este concepto no se podrían marcar (c-0057).
- **Setup claro**:
  1. *Contexto*: vela subiendo hacia un high esperado (o bajando hacia un low), con alguno de los **3 motivos**: (a) SMT — el par correlacionado sí hizo el nuevo extremo (c-0008/c-0009); (b) final de vela — el extremo se hizo en el tramo final de la vela previa (2:55/4:15/"15% final de la vela", c-0010/c-0014, ch07 c-0202); (c) feeds distintos de brokers — nivel tocado "prácticamente al nivel" en otro feed (c-0021/c-0023, "muy pocas veces").
  2. *Identificación* (en vivo, nunca anticipada — c-0016/c-0030): la vela nueva **reacciona ya en la dirección contraria creando rango bajista** (o alcista en espejo) + un motivo presente.
  3. *Entrada*: al crear ese rango de reacción — "se puede vender sin esperar que ese rango se abra por arriba: ya está activado" (c-0019). Refinado: "en 30 en 15 seguramente ya hay rangos que os permitan vender" (c-0013).
  4. *Invalidación*: el precio finalmente hace el nuevo extremo (el FS no era); el rango de reacción cierra fuera.
  5. *Stop*: `[PROPUESTA]` sobre el extremo fallido (el curso no fija stop del FS; el SL general va bajo/ sobre el TS o el rango). *Objetivo*: el rango activado sirve de target (c-0007/c-0063).
- **Negación preservada**: ver un extremo al final de hora NO obliga a FS (c-0011/c-0015) — el motivo es contexto, no señal.
- **Adaptación NQ**: `NQ_DIRECTLY_TESTABLE` para motivos (b) y (c es inaplicable: un solo feed — documentar); motivo (a) requiere correlacionado ⇒ `MULTI_INSTRUMENT_DATA_REQUIRED` (p.ej. ES/NQ, no en corpus). `[PROPUESTA]`: umbral "prácticamente al nivel" (ε en ticks/ATR) y fracción final de vela (15% dicho en un ejemplo) como parámetros.

---

### CLF-FAM-003 — SMT: divergencia con pares correlacionados

#### CLF-STR-007 — Entrada anticipada por rango del par correlacionado (SMT casos 1 y 3)

- **STRATEGY_ID**: CLF-STR-007 · **FAMILY_ID**: CLF-FAM-003 · **STATUS**: `EXTRAIDA_COMPLETA` (con dependencia de datos multi-instrumento)
- **SOURCE**: ch05 completo; ch01 c-0081–c-0097 (anuncio y 2 tipos); ch06 c-0008 (motivo 1).
- **Concepto**: la SMT redefinida: "no es más por ver si se lleva un alto o un bajo y puede haber una reversión, sino para ver **rangos que ya pueden estar completados** y no nos hemos enterado" (ch05 c-0002). Caso 1: un par crea el rango y el otro no (c-0069–c-0072). Caso 3: rango pendiente que el otro par no crea (c-0078–c-0083). Esencia: "se tendría que haber hecho el nuevo bajo y eso no ha pasado" (c-0089).
- **Setup claro**:
  1. *Contexto*: pares correlacionados (EURUSD/GBPUSD; DXY como simétrico; correlaciones consultadas en Myfxbook — herramienta dicha c-0006/c-0007). Sesgo de régimen: la completación asimétrica ocurre "normalmente cuando el precio va contra tendencia"; bearish ⇒ "más probable que solo se complete en uno de los dos" (c-0022–c-0024).
  2. *Trigger*: en el par A el rango (o pendiente) se crea/completa; en el par B el extremo correspondiente NO se hizo.
  3. *Entrada*: en B "sin la necesidad de que [B] llegara aquí arriba" (c-0017), con los rangos a favor de B; o con el rango bajista de A formado, "ya podías vender [A/B]" (c-0018). "No hay preferencia" del par débil: "a veces se cumple y a veces no" (c-0019); el instructor reparte riesgo y elige el par con objetivos más claros (c-0020).
  4. *Invalidación (negación clave)*: "si el objetivo siguiera estando más abajo, lo normal es que esto cree un pendiente y la siguiente vela complete — **no sería SMT**" (c-0076); con DXY: si DXY continúa tras retracement hay objetivo superior y "esta SMT no va a ser válida" (c-0098/c-0099).
  5. *Gestión*: si DXY toma su objetivo antes que tu par, "a lo mejor puedes salirte del trade ya" / parciales (c-0096/c-0097). Red flag 4 de ch09 = la cara preventiva.
- **Clasificación para NQ**: `MULTI_INSTRUMENT_DATA_REQUIRED` — el corpus actual es NQ only. Traducción honesta: NO trasladar EUR/GBP a NQ. Hipótesis de adaptación futura (no enseñada): SMT NQ↔ES o NQ↔YM con los mismos 3 casos. `[PROPUESTA]`: tolerancia temporal de sincronización de extremos entre pares.

---

### CLF-FAM-004 — Noticias: aceleración hacia el objetivo

#### CLF-STR-008 — Operar la vela que contiene la noticia

- **STRATEGY_ID**: CLF-STR-008 · **FAMILY_ID**: CLF-FAM-004 · **STATUS**: `EXTRAIDA_COMPLETA`
- **SOURCE**: ch10 completo (especialmente c-0023–c-0026, c-0058–c-0062, c-0100–c-0116, c-0152–c-0162, c-0185–c-0198); ch03 c-0189/c-0215.
- **Concepto**: "el resultado de la noticia no importa, solo importa lo que estamos viendo en el gráfico" (c-0025); la noticia "va a acelerar el precio hacia el doble [DOL]" (c-0026). "Nosotros vamos a querer operar siempre las velas" — la vela que contiene la noticia es la que desplaza (c-0023).
- **Setup claro (variante A — entrada en el P3 de la vela de la noticia)**:
  1. *Contexto*: noticia clasificable (Excel "NEWS - ONE TO ONE ENG": clarity/difficulty/whipsaw/blow-acc; mejores = más claridad, menos dificultad, menos whipsaw, c-0011; FOMC = evitar, c-0015); calendario Forex Factory rojas/naranjas (c-0017/c-0018); **dolls intactos** — "queréis los dolls intactos" (c-0193); TS preferiblemente ya hecho (sin TS pre-noticia = red flag de whipsaw, c-0062); mismos filtros que trading normal (c-0189–c-0191).
  2. *Confirmaciones por pares*: según la divisa de la noticia (dólar: EURUSD/JPUSD[NZDUSD?]/NCTDUSD[NZDUSD?]/AUTUSD[AUDUSD?] mismo lado; USDCHF etc. lado contrario — garbles preservados q-ch10-005; c-0027–c-0037); DXY simétrico (c-0186/c-0187).
  3. *Entrada*: en el **Power of 3 de la vela de la noticia** (ejemplo CPI 8:30: "a las 8 abre, baja un poco y podemos colocar nuestra operación aquí, dejando espacio para que una pequeña manipulación no nos saque", c-0107/c-0116); alternativa apurada: 5m antes en la vela de 40 (ch10 c-0058).
  4. *Gestión*: al llegar la noticia con posición, "poner tu posición en break-even" (c-0097). Prop firms fondeadas: margen ±5/2 min sin operar alrededor (c-0176).
  5. *Invalidación*: doll ya completado ⇒ "a lo mejor la noticia no trae casi volatilidad o es reversal" (c-0194); vela inside en noticia = posible whipsaw (c-0192).
- **Variante B — posicionarse ANTES (STR-008b, enseñada)**: con TS hecho a la 1 (noticia a las 2: "podemos entrar al gráfico a la 1", c-0039–c-0043; nota del propio Excel "We can enter charts at 1:00"), estar posicionados antes y proteger en BE al llegar (c-0097/c-0100). Dos noticias el mismo día: decidir si la primera es manipulación o movimiento real según TS hecho (c-0141/c-0160/c-0161).
- **Clasificación NQ**: `NQ_ADAPTATION_HYPOTHESIS` — las noticias USA (CPI/NFP/FOMC/ISM) mueven NQ; falta calendario económico en el runtime (`RUNTIME_GAP` menor: la Strategy no consume noticias hoy; un filtro de calendario es dato externo a incorporar). Los pares de confirmación FX NO trasladables; análogo propuesto (no enseñado): ES/YM/DXY-futuro.

---

### CLF-FAM-005 — Reentrada intra-Turtle Soup

#### CLF-STR-009 — Reentrada tras stop si la vela vuelve a cerrar dentro

- **STRATEGY_ID**: CLF-STR-009 · **FAMILY_ID**: CLF-FAM-005 · **STATUS**: `EXTRAIDA_COMPLETA` (regla puntual, riesgo definido)
- **SOURCE**: ch11 c-0024/c-0025; ch01 c-0068–c-0077.
- **Concepto**: el intra-TS da el stop, el precio reacciona y la vela vuelve a cerrar dentro del mismo rango: "tú aquí vuelves a entrar. Tienes un menos uno R ahí y un más cuatro R aquí" (c-0024). Condicional del instructor: "si el bias es correcto, por mucho que falles alguna entrada por timing, siempre vas a acabar siendo rentable" (c-0025 — condicional dicho, no validación). "Si la vela sigue cerrando dentro, este rango sigue estando operativo" (ch01 c-0070).
- **Setup claro**: (1) trade tomado con bias correcto y rango identificado; (2) stop (bajo TS) golpeado por intra-TS; (3) la vela vuelve a cerrar dentro del rango original ⇒ reentrada con el mismo plan; stop idéntico; límite de reentradas `[PENDIENTE: no enseñado]`.
- **Adaptación NQ**: `NQ_DIRECTLY_TESTABLE`.

---

### Resumen de conteos (Nivel 1-4)

| Nivel | Conteo | Ítems |
|---|---|---|
| Familias (N4) | 5 | FAM-001 continuación hacia DOL · FAM-002 failure swing · FAM-003 SMT · FAM-004 noticias · FAM-005 reentrada intra-TS |
| Estrategias completas (N3) | 9 + 1 variante | STR-001..009 (+STR-008b) |
| Setups parciales (N2) | 7 | Ver §4 |
| Componentes (N1) | 24 | CLF-CMP-001..024 (§2) |
| Reglas de gestión (transversales) | 13 | §5 (la nº 12 agrega las reglas de conducta operativa de ch12) |
| Red flags | 4 | §6 |

**Por qué no más**: cada combinación enseñada de los componentes cae en una de las 9 estrategias (las variaciones enseñadas son de sesión/escenario dentro de FAM-001, o de gestión en §5). El curso NO enseña: estrategias de escala intradía pura,网格/grid, momentum-indicadores, ni ningún setup con indicadores técnicos (el curso no usa ningún indicador — véase §8 exclusión "NOT_OBSERVABLE"). Inflar el conteo dividendo ejemplos LONG/SHORT o TFs sería artificio: la simetría y la multi-TF son dimensiones, no estrategias (ver `CLUTIFX-EXPERIMENT-MATRIX.md`).

---

## 4. Setups parciales y escenarios enseñados (Nivel 2 — no elevables a estrategia solos)

| ID | Setup/escenario | Fuente | Por qué no es estrategia completa |
|---|---|---|---|
| CLF-SET-001 | Escenario 2 de London (TS por hacer, día no ideal → evitar London, ir a NY o esperar el rango y posicionarse para NY) | ch07 c-0013–c-0019 | Es una regla de DERIVACIÓN entre estrategias (skip/redirect), no un conjunto de entrada propio |
| CLF-SET-002 | Entrada por order block confirmado (cierre fuera de la vela OB, stop bajo TS, "menos ideal pero confirma") | ch04 c-0034/c-0036/c-0039 | Trigger de confirmación que se monta sobre FAM-001 (es la entrada 2 del esquema) |
| CLF-SET-003 | PDM espejo en el alto (short) con confirmación por temporalidad (M30 si 4h aún no cierra) | ch04 c-0096–c-0101 | Variante direccional del CMP-008; el curso no la desarrolla como pipeline completo |
| CLF-SET-004 | Entradas de continuación en trade abierto (stop más ancho, "esperar rangos a favor" para refinar) | ch04 c-0051/c-0052/c-0055 | Gestión de añadir/seguir, no nueva tesis |
| CLF-SET-005 | Espera a completitud del rango contrario y reversión ("esperar a que se complete el bajista y luego al alza") | ch04 c-0089/c-0090/c-0092/c-0095 | Condición de sincronización para STR-002/004 |
| CLF-SET-006 | Salir "en el alto de la nueva vela" por seguridad en vivo (para que no se cree rango en contra) | ch04 c-0091 | Micro-gestión dicha en vivo [personal] |
| CLF-SET-007 | Vela de las 12h como vela clave condicional (reacciona y cierra dentro ⇒ targets más bajos; cierra fuera sin rango bajista ⇒ esperar recorrido) | ch08 c-0019/c-0020 | Plan condicional de ejemplo, sin parámetros completos |

---

## 5. Gestión y salidas (transversal a FAM-001; clasificable como reglas de MoneyManagement en la frontera Strategy/MM de Echo)

El curso pone la gestión del lado humano; para Echo Futures estas reglas son **candidatas de MM/policy** (la Strategy emite el setup técnico; el sizing/protección vive en MM):

1. **Stop inicial**: debajo/sobre el Turtle Soup (ch01 c-0067; ch11 c-0021/c-0023). "El stop-loss no se mueve" (ch11 c-0020). Margen por expansión: con movimientos de 60-80 pips/día, un stop de 25 pips "a lo mejor está bien" (ch11 c-0022, ejemplo).
2. **Break even ESTRUCTURAL**: en puntos donde, si estás equivocado, el precio puede girarse (rangos que retoma, objetivos tomados, "a la que ves que se te puede estar girando") — "yo NUNCA lo pongo estilo en tal R" (ch11 c-0013/c-0014/c-0028/c-0031/c-0032). Displacement 5m "volando" ⇒ BE no sobra (c-0041). Tensión no resuelta por el curso entre "stop no se mueve" y BE (q-ch11-012 PARTIAL).
3. **Regla de coherencia**: "si tomas parciales, tienes que poner break-even" (ch11 c-0019, truncada en fuente q-ch11-007).
4. **Parciales**: primer parcial >50% con margen; 80% cerca del TP con ~14 pips restantes (ch11 c-0015/c-0017); esquema señalado 50/20/10/10/10 sin etiquetas de nivel (c-0052, duda); por tiempo: cerrar 80-90% y dejar correr un simbólico (c-0030). Parcial = reducción de riesgo: 1% → 0.5% (c-0046).
5. **Salida por tiempo**: objetivo o "nueva vela de las 5" (ch04 c-0113/c-0114; ch07 c-0075–c-0077: salir en la vela de las 5 "muy cerca del target", último parcial "si te gira ya no pasa nada"); salida basada en tiempo con rangos en contra formándose cerca de la hora clave = "otra buena salida" (ch11 c-0029).
6. **Salida por reacción contraria**: dos velas de 15m fuertes en contra ⇒ "yo me saldría ya por precaución" (ch08 c-0066–c-0068 [probabilística/personal]).
7. **Minuto 59 de horas clave**: salir con precaución y asegurar (ch02 c-0063/c-0064 [probabilística]).
8. **Rango en contra en pleno trade**: parciales primero + BE (o cerrar y reentrar cuando vuelvan los rangos a favor) (ch09 c-0015/c-0078; q-ch09-002 lectura candidata de "tarjeta breakable").
9. **Reentrada intra-TS**: STR-009.
10. **Pirámides (challenge only)**: primera protegida (BE) siempre (ch11 c-0055/c-0060); test contrafáctico load-bearing: "si no estuviera el trade inicial, ¿tomaría este segundo trade? Si sí, pirámide; si no, no" (c-0059; c-0057/c-058); "en la fondeada no lo hago NUNCA" (c-0061); con objetivo ya tomado, mucho cuidado (c-0070); excepción drawdown con aritmética UNCERTAIN (c-0067/c-0068).
11. **Riesgo por etapa** [ejemplos hipotéticos, capital de referencia no dicho q-ch11-001]: challenge f1 1% hasta 4% profit luego 2%/1.5%; f2 1% hasta 2.5%; fondeada 1% (o 0.5%) (ch11 c-0003–c-0006).
12. **Tope y límite diario (ch12 — reglas de conducta operativa, extraídas por el minero del capítulo)**: tope de riesgo 1% por trade (ch12 c-0008, c-0019, c-0073 "buenos setups de 1%"); límite del día perdedor "2R máximo… dos operaciones de 1 y 1" (ch12 c-0010, parámetro dicho); protocolo de retirada: al alcanzar "lo máximo que pudiese perder, cerrar el gráfico" (c-0057, umbral no explicitado q-ch12-010), y ante descontrol "cierra el Ctrader, cierra el gráfico y vete" (c-0070); check de estado: "si ves que estás muy nervioso, también no operar" (c-0124); journal por trade: "lo revisas, lo apuntas… te olvidas" (c-0023). Aritmética de expectativa dicha (hipotética, no validación): 5-6/10 aciertos a 1% ratio 2 ⇒ +8R neto "el challenge pasado" (c-0015/c-0016); 100 trades 60/40 ⇒ "80R" (c-0119). Estos son refinamientos de MM/plan de conta — ningún indicador de entrada.
13. **Payouts/challenges**: retirar 1-2% de fondeadas y recomprar challenges (ch11 c-0007/c-0008) — política de cartera humana, fuera de scope de una Strategy.

---

## 6. Red flags (filtros booleanos objetivos de entrada)

| # | Red flag | Enunciado y fuerza | Excepción dicha | Predicado objetivo (ver detectores) |
|---|---|---|---|---|
| 1 | Rangos en contra / velas que abren tomando el extremo contrario | Advertencia probabilística + **invalidación dura acotada** al escenario (ch09 c-0009, c-0007, c-0012); dura "hasta que reinicia o crea pendiente" (c-0011) | El mismo hecho en tu dirección es confirmación (c-0021/c-0022) | Rango detectado de dirección contraria activo en TFs de sesión |
| 2 | Inside candles | **Pausa dura en su escenario**: "no compras, no vendes" (ch09 c-0084); probabilidad baja (c-0026) | Habilitada al tomar el extremo (c-0085); ideal: siguiente vela toma extremo + TS (+FS o SMT ideal, c-0027/c-0028) | H < H_prev ∧ L > L_prev |
| 3 | Objetivo ya tomado | Probabilística (c-0045: "se podría, pero la probabilidad es mucho más baja"); variante sesión (c-0051/c-0053) | Riesgo consciente permitido (c-0107/c-0108); reversales claras existieron (c-0124) | Precio alcanzó el nivel DOL/objetivo declarado |
| 4 | Par correlacionado completó su target | "Es red flag también" (ch09 c-0126–c-0131) | Mitigación: parciales/BE (c-0129); el objetivo mayor puede sostener (c-0136) | Extremo del instrumento correlacionado alcanzado (requiere 2º instrumento) |

Contexto temporal de las flags: horas clave 3/5/(8?)/9 (q-ch09-001). En noticias se añaden: dolls intactos, no-vela-inside, TS previo preferente (§3 STR-008).

---

## 7. El procedimiento de análisis completo (ch08 — la receta de derivación del bias)

1. Empezar "como si no tuviera ni idea" por 1 año (sólo para análisis desde cero; "no lo tenéis que hacer cada día", ch08 c-0002/c-0048).
2. Bajar TF por TF marcando TODOS los rangos (orden dicho: 1 año → 6M → 1M → 3S → 2S → 1S → 5d → 4d → 3d → 2d → 1d → 12h → 8h → 6h → 4h → 3h → 1h), "construyendo una narrativa" (c-0022).
3. REGLA-RESUMEN: "ir bajando de tonalidad, marcando todos los rangos, construyendo narrativa, y a la que la tienes, bajas más y buscas el trade" (c-0069).
4. Rangos enfrentados en un TF ⇒ "es mejor no adivinar": ignorar ese TF y seguir bajando (c-0050/c-0052/c-0053).
5. Ventana ideal: entrar ANTES de que los rangos estén completados (mejor ratio + BE protege; ch08 c-0016); tarde = más riesgo y menos ratio (c-0017); llegado tarde: "trade más arriesgado esperando rango pendiente a favor" (c-0013).
6. "El long gratis no se opera": el tramo ya recorrido hacia un objetivo tomado (c-0027/c-0028).
7. Anti-regla de venta: "nunca vendáis mientras se forman rangos alcistas" (c-0084/c-0085).
8. Si en 8h/6h no hay nada: "os marcháis" (ch03 c-0119).
9. Sesgo de horas: el bias "normalmente" lo dan 6h–3D (ch03 c-0050); los meses "dan contexto y nada más" (ch08 c-0004).

Para el backtester, este procedimiento es el **pipeline de contexto** (CMP-002 + CMP-007 + CMP-024) que alimenta a todas las estrategias de FAM-001.

---

## 8. Clasificación NQ / datos / runtime (resumen de D2-D3)

| Estrategia | Clasificación | Detalle |
|---|---|---|
| STR-001 London ideal | `NQ_ADAPTATION_HYPOTHESIS` | Ancla de sesión FX (vela de la 1) debe mapearse a sesiones CME como hipótesis |
| STR-002 Pendiente a DOL | `NQ_DIRECTLY_TESTABLE` | Estructural; único eje a fijar: TF del objetivo |
| STR-003 NY continuación | `NQ_ADAPTATION_HYPOTHESIS` | Ancla 9:00 NY → propuesta NQ 9:30 ET open |
| STR-004 NY reversal | `NQ_ADAPTATION_HYPOTHESIS` | Ancla vela de las 5 |
| STR-005 Refinado | `NQ_DIRECTLY_TESTABLE` | Procedimiento estructural; escala de TFs = eje |
| STR-006 Failure swing | `NQ_DIRECTLY_TESTABLE` (motivos b; a multi-instrumento; c inaplicable single-feed) | ε de nivel y fracción final de vela = parámetros |
| STR-007 SMT | `MULTI_INSTRUMENT_DATA_REQUIRED` + `FX_NATIVE` fiel | Sin 2º instrumento en corpus; NO trasladar EUR/GBP |
| STR-008 Noticias | `NQ_ADAPTATION_HYPOTHESIS` + `RUNTIME_GAP` (calendario) | Noticias USA mueven NQ; falta feed de calendario |
| STR-009 Reentrada intra-TS | `NQ_DIRECTLY_TESTABLE` | Requiere intrabar (1m mínimo) |

Datos disponibles (auditados en `HEFESTO-BASELINE-AUDIT.md`): NQ físico 2023-10→2026-10, barras 1m Last, 672 sesiones elegibles; **sin ticks**; sesiones CME America/Chicago 17:00→16:00; fees 2.49/lado, slippage 1 tick. Consecuencias: (a) todo lo intrabar se resuelve a 1m como máximo (la "reacción" del TS y el P3 intrabar se aproximan por velas 1m — el curso opera visualmente intrabar; la fidelidad es una cota, declarar); (b) horas FX del curso (UTC-4 NY) se anclan a `America/New_York` con DST real, no offset fijo; (c) velas 3h/5h/etc. off-grid se componen desde 1m con anclaje a la hora NY dicha.

**Frontera Strategy/MM de Echo**: toda la §5 (parciales/BE/pirámides/riesgo%) pertenece al plano MM/policy (tgmm/gerardmm hoy: `NO_ADDS`, `STRATEGIC_ENTRY_BUDGET_V1`); las estrategias Clutifx emiten señales + stop técnico + objetivo estructural (DOL), igual que ORB emite su evento de add técnico que el MM decide económicamente. Sin gaps de runtime para STR-002/005/006/009; STR-008 requiere feed de calendario (gap declarado).

---

## 9. Exclusiones y contenido no estratégico (clasificación honesta)

| Clase | Contenido | Ejemplos |
|---|---|---|
| `NON_TRADING_CONTENT` | Psicología pura (revenge, miedo, disciplina, anécdotas) | ch12 MAYORMENTE (135 claims: psicología + catálogo de errores); **excepción**: sus reglas de conducta operativa (1%/trade, 2R/día perdedor, protocolo de retirada, journal, no-operar-nervioso) SÍ fueron extraídas a §5.12 |
| `META` | Aperturas, temarios, recaps, anuncios de vídeo siguiente | 18 claims META + 1 ANUNCIO clasificados por COVERAGE (categorías separadas) |
| `EXAMPLE_ONLY` | Observaciones de un caso sin enunciado general | "cuerpos respetan brutalmente el rango" (ch03 c-0108); ratio 12,34 (ch04 c-0079); -164 vs -100 pips (ch05) |
| `DUPLICATE_SEMANTICS` | Repeticiones del instructor con otras palabras | 20 claims EQUIV clasificados por COVERAGE |
| `INSUFFICIENT_SPECIFICATION` | "Entry Model" (ch04 c-0110, término sin definición); vídeo "extras" del reiniciado anunciado y no procesado (ch03 c-0013); capital de referencia de los % (q-ch11-001); R:R objetivo anunciado pero NUNCA cifrado en audio (frames de ch08 muestran 2,34/2,68/2,76/2,46 — dato visual no verbalizado); distancia numérica del stop (mostrada 0.00209 en herramienta, no dicha); límite de reentradas; umbral de "lo máximo que pudiese perder" (q-ch12-010) | Huecos declarados de la biblioteca |
| `NOT_OBSERVABLE_WITH_AVAILABLE_DATA` | SMT multi-par (sin 2º instrumento); motivo FS "feeds de brokers"; DXY (sin índice) | Ver §8 |
| `UNCERTAIN` | 15 claims (garbles/deícticos) + contradicción MATERIAL q-ch07-019 (hora de la noticia del ejemplo NY-EUR: 10 vs 8 — ninguna adjudicable) | Nunca consumibles como hechos |

El curso **no usa indicadores técnicos** (ni medias, ni osciladores, ni ADX): toda detección fuente es estructural (extremos, cierres, velas, horas). Los detectores con indicadores del documento `CLUTIFX-OBJECTIVE-DETECTORS.md` son **hipótesis de operacionalización del agente** para condiciones visuales no formalizadas por el instructor (ej. "reacción", "movimiento alcista", "expansión fuerte"), siempre etiquetadas RESEARCH HYPOTHESIS.

---

## 10. Gate B y estado

```text
CLUTIFX_STRATEGY_DISCOVERY = COMPLETE
```

Justificación: los 12 capítulos fueron revisados (reglas, ejemplos, excepciones, negaciones y dudas) vía la compilación certificada (cobertura 1.388 directos + 152 vía atlas + 44 clasificados = 1.584 consumibles) más minería por capítulo de reglas/ejemplos/claims (extractos de verificación en `/tmp/clf-god/` y re-verificación adversarial FASE H). Toda oportunidad reconstruible fue evaluada: 5 familias, 9+1 estrategias completas, 7 setups parciales, 24 componentes, 12 reglas de gestión, 4 red flags. La exhaustividad NO fabricó combinaciones: cada ítem tiene fuente; cada fusión/división está justificada arriba. Las únicas omisiones posibles son contenido de los vídeos NO procesados del curso (declarado: extras del reiniciado, Entry Model, PDFs ch12) — ausencia documentada, no vacío rellenable.

**Veredictos de la misión** (detallados en `HANDOFF.md`): `CLUTIFX_STRATEGY_CATALOG = COMPLETE` · `HEFESTO_BACKTESTER_BASELINE = PARTIAL` (23 filas R02 pendientes del ciclo R03 ajeno; sin ticks) · `READY_FOR_CLUTIFX_IMPLEMENTATION = NO` (requiere encargo y aprobación Owner de la matriz) · `EXPERIMENT_MATRIX_OWNER_APPROVAL = PENDING` · `CLUTIFX_BACKTEST_EXECUTED = NO` · `LIVE_TRADING_CHANGED = NO`.
