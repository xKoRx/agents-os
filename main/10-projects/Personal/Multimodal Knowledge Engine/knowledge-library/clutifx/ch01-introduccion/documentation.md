# Clutifx — Capítulo 1: Introducción (Conocimiento extraído)

> Source: `ep01-intro.mp4` (sha256 `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b`, ~34 min).
> Extraído con MKE V2, branch `feature/agent-vlm-provider` @ `5ebc066`, proveedor de subagentes (sin API pagada).
> 130 ventanas · 1.527 claims + 367 relaciones reconstruidos · 1.140 con grounding SUPPORTED (ver `claims.jsonl`).

## 0. Qué es este capítulo

Capítulo de introducción del curso completo. El instructor anuncia el temario: estrategia, BIAS, entradas, riesgo, conceptos nuevos y cómo operar noticias. Continúa el curso intermedio (que "sirvió para sentar la base"); aquí "va a ampliar ya todo" [w0001–w0002]. El capítulo presenta los 7 conceptos base de la estrategia: **rango**, rango pendiente/reiniciado, Turtle Soup, SMT, failure swing, order block y Power of 3.

## 1. El rango (concepto central)

**Definición**: un rango se forma cuando una vela toma un extremo (high o low) de la vela anterior y cierra dentro de esa vela anterior [w0006–w0007]. No tiene por qué ser la vela inmediatamente siguiente: cualquier vela posterior que tome el extremo y cierre adentro forma el rango [w0006]. La vela que toma el extremo no necesita ser de un tipo concreto (bajista/alcista): "no tiene por qué ser así", aunque la mayoría de las veces lo es [w0009–w0010].

**Propiedad clave**: cuando el precio forma un rango (toma un extremo y cierra adentro), el precio **va a ir a completarlo**, es decir, a buscar el otro extremo [w0021, w0025, w0030]. Un rango se considera completo cuando toma tanto el low como el alto [w0076].

**Por qué importa**: "la importancia de los rangos es como la base de la estrategia" [w0021–w0022]. El precio se mueve "en función de rangos", "como una cadena" [w0021–w0022, w0062–w0063]: forma un rango → lo completa → a partir del extremo completado se forma el siguiente rango → así se navega el precio en dirección a los objetivos. Los rangos "normalmente nos van a decir hacia dónde va el precio" [w0026, w0035].

**Matices**: los rangos **no siempre** se completan (el instructor corrige explícitamente el "siempre") [w0033–w0034]; qué rangos se completan y cuáles no se ve en el capítulo de bias/estrategia [w0025]. La lógica de rangos sola "no es suficiente para operar" [w0032]. El comportamiento se repite en todas las temporalidades [w0017, w0030–w0031]; con los rangos bien pintados "podrías hasta operar solo viendo el gráfico diario" [w0033].

Ejemplo real citado en el capítulo: rango bullish de GBPUSD con objetivo en 1,35843; el precio lo completó antes de la sesión [w0037, w0039].

## 2. Rango pendiente y rango reiniciado

Dos nombres para casos concretos de rango (los nombres solo sirven para referirse a ellos con precisión; "la idea viene a ser lo mismo" [w0062]):

- **Rango pendiente**: la nueva vela toma el **low** de la vela anterior (abre por debajo) y cierra adentro, o reacciona hacia arriba tras tomarlo [w0044–w0046]. Es el rango que se forma **a favor** del objetivo/tendencia [w0045–w0047].
- **Rango reiniciado**: la siguiente vela **abre por arriba** y toma el **high** [w0049–w0050]. Es el rango que se forma **en contra** de la tendencia [w0054, w0061–w0062].

Correspondencia direccional [w0060–w0062]:
- Rango bajista con objetivo bullish → **reiniciado** (en contra).
- Rango alcista con objetivo bullish → **pendiente** (a favor).

En ejemplo diario: objetivo diario en 1,15803 (EURUSD); el precio toma el low del rango diario, reacciona, y se forma un rango pendiente en 4h a favor del objetivo [w0042–w0047, w0055, w0058]. Anticipar en tiempo real la creación de un rango antes del cierre de la vela "es un poco ya más avanzado" [w0058–w0059]; en 8 horas el mismo caso se ve como rango pendiente también [w0059].

Uso operativo: si en 4h se forma un rango **en contra** de tu dirección (ej. comprado), puede que el precio vaya a completar esos rangos antes de subir; una opción es poner break even y re-entrar cuando el precio vuelva a reaccionar [w0073–w0074].

Ciclo de vida: el rango superado (ya completado/superado por el precio) "ya no importa" y se elimina; si tras tomar un extremo se forma un nuevo rango, el objetivo se recalcula al nuevo nivel [w0076–w0080].

**Regla de invalidación**: si la vela **cierra afuera** del rango, "esto ya no es un rango" [w0076–w0078]. Con idea alcista, hay que esperar a que se forme una nueva vela/rango [w0076–w0078].

## 3. Turtle Soup ("tartle sub")

Toma de liquidez: se toma el alto (o el bajo) para crear o completar un rango y se busca la **reacción hacia el otro lado** [w0063–w0064]. Otros nombres equivalentes: "toma de liquidez", "toma del alto del bajo" [w0065].

- Toma del **bajo** seguida de reacción bullish → **Turtle Soup alcista** [w0066, w0068].
- Si la vela siguiente sigue bajando (no reacciona), **no es** Turtle Soup [w0066].
- El Turtle Soup debe ser una **toma de liquidez** [w0066] y marca que el inicio del movimiento puede darse ya [w0068].
- Entrada long en Turtle Soup: **stop loss seguro por debajo** del low del Turtle Soup [w0068–w0069].

Variante intra: el **intra turtle soup** es un turtle soup dentro de otro turtle soup ya hecho; "no pasa muchas veces" [w0072, w0076]. Si estos casos no existieran, "tendríamos un 100% de winrate" — de ahí que el winrate no sea 100% [w0072].

## 4. SMT (Smart Money Technique)

La SMT "clásica" que los alumnos conocían del curso intermedio: divergencia zigzag entre pares correlacionados (EURUSD vs GBPUSD, o vs DXY) donde uno hace nuevo alto y el otro no — señal de reversión [w0082–w0084]. Habrá un capítulo dedicado [w0084].

**La SMT bajo esta estrategia** (lo nuevo): además de la divergencia clásica, la SMT aparece en la relación con los **objetivos de rango** [w0090–w0093]:

- El euro completa su objetivo de rango, pero el par correlacionado (JPY o DXY) **no llega a su objetivo** y pasa directamente al reversal → SMT [w0091–w0092].
- Estando en long en libra: si el euro llega a objetivos y se forma esa SMT arriba, el precio puede girarse directamente [w0092–w0093].
- La SMT también puede darse **para crear el rango**: el par correlacionado (libra) crea el rango y el euro no necesita crearlo, pudiendo llegar directo hasta arriba [w0096–w0098].
- No tiene que ser necesariamente entre dos velas contiguas [w0093–w0094].

Estos casos son SMT que "no vas a poder ver de ningún modo" sin conocer la estrategia de rangos [w0090–w0091]; "a veces estos datos están un poco ocultos" [w0090–w0091].

## 5. Failure swing

"El failure swing es cuando el precio no consigue hacer un nuevo bajo" [w0098–w0100]. Concepto ya tocado en el curso intermedio; habrá capítulo propio [w0099–w0100]. Puede darse por varios casos [w0098]:

1. Por una SMT [w0100].
2. Por que el **alto se ha hecho al final de la vela** [w0100].
3. Por que el **bajo se ha hecho al final de la vela** [w0100].

Caso práctico: aunque no se llegue a tomar el low (porque en otro broker sí se lleva el low — diferencias de feed entre brokers como FXCM), se puede dar como rango igualmente [w0102–w0103, w0105]. El caso se anota en el propio gráfico como "BAJO/ALTO A FINAL DE VELA" [w0102].

## 6. Order block ("orden")

- Definición operativa: cuando el precio **cierra por fuera de la última vela bajista** (en contexto de giro alcista), se forma lo que el instructor llama "orden"/order block [w0107–w0108].
- El order block es importante para el **cambio de tendencia** ("change in state of delivery") [w0106].
- Uso: el instructor lo usa para sus **entradas** y para **confirmaciones en temporalidad más baja** [w0107, w0109].
- Entrada: una vez esa vela cierra por fuera, "ya puedes tomar tu long" [w0113, w0115–w0116]; se espera a que se forme el order block y se opera su confirmación [w0116].
- En M15 es "mucho más fácil encontrar order blocks" [w0112]; en 10 minutos no siempre se ve claro [w0112–w0113].
- Se detalla en el capítulo de entradas [w0109–w0110].

## 7. Power of 3

Modelo de la vela de 4 horas (o del período elegido) dividida en fases horarias (hora de New York) [w0121, w0129]:

1. **Apertura** (ej. 01:00 NY): la vela abre.
2. **Manipulación**: tras abrir, la vela se manipula (sube y baja) [w0123].
3. **Cierre/distribución** (ej. 05:00 NY): la vela cierra dejando la mecha del lado manipulado [w0123].

Aplicación operativa: esperar a que abra la nueva vela de 4 horas a las 5 permite **entrar en el punto óptimo** dentro del Power of 3 [w0124]. Si es solo la naturaleza de la vela la que tiene que manipular para luego ir a tu dirección, el movimiento se ve "de un modo mucho más calmado" [w0129]. El Power 3 se usará tanto en entradas como en salidas (incluidas salidas basadas en tiempo) [w0129]. Queda pendiente determinar qué es mejor: entrar arriba o abajo en la vela [w0124].

## 8. Notas de contexto del capítulo

- Prerrequisitos: no hace falta el curso intermedio; "no hay información previa totalmente relevante" [w0002].
- El formato replica el del curso intermedio [w0002].
- Los conceptos SMT, failure swing y power of three ya fueron explicados en el curso intermedio; aquí se re-introducen bajo la nueva estrategia [w0081, w0099, w0119].
- Cierre: este es el primer capítulo; el resto de temas se desarrolla en los siguientes [w0130].

---

## Estado de la extracción (honesto)

| Métrica | Valor |
|---|---|
| Ventanas L0 | 130 |
| Claims reconstruidos | 1.527 |
| Relaciones reconstruidas | 367 |
| Grounding SUPPORTED | 1.140 |
| Grounding INSUFFICIENT | 38 |
| Grounding CONTRADICTED | 22 |
| Sin revisar (run abortado) | 694 |
| Equivalence: EQUIVALENT / DIVERGENT | 18 / 24 |

Fases del motor ejecutadas: L0 media ✓, windows ✓, reconstruction 130/130 ✓, grounding 1.200/1.894 ✓ (abortado por el owner), composition ✗, publication ✗. Este `documentation.md` fue sintetizado directamente del subconjunto validado (SUPPORTED) sin pasar por la fase SKO del motor. Los 694 sin revisar permanecen en `claims.jsonl` marcados `UNREVIEWED` (la mayoría son `parameter` — niveles/puas numéricos citados en pantalla — y observaciones de ventana ya cubiertas en este documento). Las relaciones con veredicto CONTRADICTED (22) están así marcadas en `claims.jsonl`: no usarlas como conocimiento.
