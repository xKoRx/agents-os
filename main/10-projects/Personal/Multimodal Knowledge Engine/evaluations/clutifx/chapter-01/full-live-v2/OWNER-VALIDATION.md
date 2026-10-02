# OWNER-VALIDATION — checklist de validación humana

Objetivo: que el Owner compare el video contra el conocimiento extraído y califique la fidelidad. **Este archivo no está rellenado: cada marca la pone el Owner.**

## Cómo calificar

Para cada knowledge relevante del intervalo, marcar una de:

```text
CORRECT          — el statement representa fielmente lo dicho/mostrado en ese tramo
PARTIAL          — captura parte; falta matiz, condición o excepción
MISSING          — el tramo contenía conocimiento relevante que MKE no extrajo
WRONG            — el statement contradice lo dicho/mostrado
DUPLICATE        — conocimiento repetido sin valor agregado
OVERGENERALIZED  — pierde condiciones/alcance del original
```

Referencias: intervalo + topic en REVIEW-INDEX.md; statements completos en documentation.md; evidencia por statement en claims.jsonl (`evidence_ids` → transcript.json / frames).

## Checklist por intervalos (13 bloques × 10 ventanas)

| Bloque | Time | Ventanas (disp.) | Marca del Owner | Notas |
|---|---|---|---|---|
| 01 | 00:00–02:28 | w0001✓, w0002✓, w0003✗, w0004✓, w0005✗, w0006✓, w0007✓, w0008✓, w0009✓, w0010✓ (8/10 aceptadas) | ☐ | |
| 02 | 02:29–04:37 | w0011✓, w0012✓, w0013✓, w0014✓, w0015✓, w0016✓, w0017✓, w0018✓, w0019✓, w0020✓ (10/10 aceptadas) | ☐ | |
| 03 | 04:40–06:48 | w0021✓, w0022✓, w0023✓, w0024✓, w0025✓, w0026✓, w0027✓, w0028✗, w0029✓, w0030✓ (9/10 aceptadas) | ☐ | |
| 04 | 06:52–09:10 | w0031✓, w0032✓, w0033✓, w0034✗, w0035✓, w0036✓, w0037✓, w0038✓, w0039✓, w0040✓ (9/10 aceptadas) | ☐ | |
| 05 | 09:11–11:43 | w0041✓, w0042✓, w0043✗, w0044✓, w0045✗, w0046✓, w0047✓, w0048✓, w0049✗, w0050✓ (7/10 aceptadas) | ☐ | |
| 06 | 11:44–14:29 | w0051✓, w0052✓, w0053✓, w0054✗, w0055✓, w0056✓, w0057✓, w0058✗, w0059✗, w0060✓ (7/10 aceptadas) | ☐ | |
| 07 | 14:30–17:32 | w0061✓, w0062✗, w0063✓, w0064✓, w0065✗, w0066✓, w0067✓, w0068✓, w0069✓, w0070✓ (8/10 aceptadas) | ☐ | |
| 08 | 17:33–20:38 | w0071✓, w0072✗, w0073✓, w0074✗, w0075✓, w0076✓, w0077✓, w0078✗, w0079✓, w0080✓ (7/10 aceptadas) | ☐ | |
| 09 | 20:40–23:04 | w0081✓, w0082✓, w0083✓, w0084✓, w0085✓, w0086✓, w0087✓, w0088✗, w0089✓, w0090✓ (9/10 aceptadas) | ☐ | |
| 10 | 23:07–26:05 | w0091✓, w0092✗, w0093✓, w0094✗, w0095✓, w0096✓, w0097✓, w0098✗, w0099✓, w0100✓ (7/10 aceptadas) | ☐ | |
| 11 | 26:06–28:28 | w0101✓, w0102✗, w0103✓, w0104✓, w0105✓, w0106✓, w0107✓, w0108✓, w0109✗, w0110✗ (7/10 aceptadas) | ☐ | |
| 12 | 28:32–30:40 | w0111✓, w0112✓, w0113✓, w0114✓, w0115✓, w0116✗, w0117✗, w0118✗, w0119✓, w0120✓ (7/10 aceptadas) | ☐ | |
| 13 | 30:42–34:02 | w0121✓, w0122✗, w0123✓, w0124✓, w0125✓, w0126✓, w0127✓, w0128✓, w0129✓, w0130✓ (9/10 aceptadas) | ☐ | |

## Muestra de calidad (5 tramos distribuidos — revisión detallada sugerida)

### w0002 · 00:09–00:36 · «Hola, bienvenido al curso completo. Aquí vas a descubrir la estrategia en profun…» · 24/26 supported

| Record | Statement | Grounding | Marca |
|---|---|---|---|
| cl-audiencia-procedente-intermedio | El instructor considera probable que la audiencia proceda de su curso intermedio. | SUPPORTED | ☐ |
| cl-capitulo-cubre-bias | El primer capítulo cubrirá el BIAS. | SUPPORTED | ☐ |
| cl-capitulo-cubre-entradas | El primer capítulo cubrirá las entradas. | SUPPORTED | ☐ |
| cl-capitulo-cubre-estrategia | El primer capítulo cubrirá la estrategia. | SUPPORTED | ☐ |
| cl-capitulo-cubre-riesgo | El primer capítulo cubrirá el riesgo. | SUPPORTED | ☐ |
| cl-capitulo-explica-noticias | El primer capítulo explicará cómo operar noticias. | SUPPORTED | ☐ |
| cl-capitulo-incluye-conceptos-desconocidos | El primer capítulo incluye conceptos que la audiencia todavía no conoce. | SUPPORTED | ☐ |
| cl-curso-completo-amplia-intermedio | El curso completo amplía el contenido del curso intermedio. | SUPPORTED | ☐ |
| cl-curso-completo | Este contenido es el curso completo. | SUPPORTED | ☐ |
| cl-curso-intermedio-sienta-base | El curso intermedio sirvió para sentar la base. | SUPPORTED | ☐ |
| cl-descenso-reciente-eurusd | En el tramo más reciente de la gráfica, el precio desciende desde aproximadamente 1.16220 hasta a… | SUPPORTED | ☐ |
| cl-dos-bandas-azules | La parte derecha de la gráfica contiene dos bandas horizontales azules. | SUPPORTED | ☐ |
| rel-continuidad-sin-curso-intermedio | DEPENDS_ON: no-requiere-curso-intermedio → info-intermedio-no-totalmente-relevante | SUPPORTED | ☐ |

### w0037 · 08:22–08:33 · «bearish otra vez, que en Libra están formados, ya lo vais a ver en el tema de la…» · 6/8 supported

| Record | Statement | Grounding | Marca |
|---|---|---|---|
| cl-comparacion-diaria-eurusd-gbpusd | La vista muestra los gráficos diarios de EURUSD y GBPUSD. | SUPPORTED | ☐ |
| cl-gbpusd-seleccionado | Se seleccionó el símbolo GBPUSD. | SUPPORTED | ☐ |
| cl-objetivo-hoy-rango-bullish-libra | El rango bullish en Libra tenía como objetivo para hoy el nivel 1.37489. | SUPPORTED | ☐ |
| cl-rango-bearish-libra-formado | Se formó un rango bearish arriba en Libra. | SUPPORTED | ☐ |
| cl-rango-bullish-libra-formado | Otra vez, se formó un rango bullish en Libra. | SUPPORTED | ☐ |
| cl-reversion-tras-rango-bearish-libra | El precio empezó a revertir cuando se formó el rango bearish arriba en Libra. | SUPPORTED | ☐ |
| rel-objetivo-depende-rango-bullish-libra | DEPENDS_ON: objetivo-hoy-rango-bullish-libra → rango-bullish-libra-formado | INSUFFICIENT | ☐ |
| rel-reversion-depende-rango-bearish-libra | DEPENDS_ON: reversion-tras-rango-bearish-libra → rango-bearish-libra-formado | SUPPORTED | ☐ |

### w0068 · 16:47–17:00 · «Pero la idea es esta, ¿vale? Toma del bajo, reacción bullish, pues tenemos Tartl…» · 5/6 supported

| Record | Statement | Grounding | Marca |
|---|---|---|---|
| cl-stop-loss-long-debajo-turtle-soup | Si aquí estás buscando ya para tomar longs, tu stop loss tendría que estar seguro debajo del Turt… | SUPPORTED | ☐ |
| cl-turtle-soup-concepto-importante | El Turtle Soup es un concepto muy importante. | SUPPORTED | ☐ |
| cl-turtle-soup-indicia-inicio-movimiento | El Turtle Soup marca que el inicio del movimiento se puede dar ya. | INSUFFICIENT | ☐ |
| cl-turtle-soup-tras-toma-bajo-bullish | La toma del bajo seguida de una reacción bullish se identifica como un Turtle Soup. | SUPPORTED | ☐ |
| rel-indicio-inicio-movimiento-requiere-patron | DEPENDS_ON: turtle-soup-indicia-inicio-movimiento → turtle-soup-tras-toma-bajo-bullish | SUPPORTED | ☐ |
| rel-stop-loss-long-requiere-patron | DEPENDS_ON: stop-loss-long-debajo-turtle-soup → turtle-soup-tras-toma-bajo-bullish | SUPPORTED | ☐ |

### w0099 · 25:39–25:48 · «Luego, concepto de failure swing, ya lo visteis también un poco en el curso inte…» · 3/3 supported

| Record | Statement | Grounding | Marca |
|---|---|---|---|
| cl-failure-swing-definition | El failure swing es cuando el precio no consigue hacer un nuevo bajo. | SUPPORTED | ☐ |
| cl-failure-swing-has-multiple-cases | El failure swing puede darse en varios casos. | SUPPORTED | ☐ |
| cl-failure-swing-seen-in-intermediate-course | El concepto de failure swing ya se había visto parcialmente en el curso intermedio. | SUPPORTED | ☐ |

### w0128 · 32:55–33:12 · «un poco esto la lógica. También importante para saber un poco de noción de qué e…» · 6/7 supported

| Record | Statement | Grounding | Marca |
|---|---|---|---|
| cl-alejar-vista-de-temporalidad-baja | Aleja la vista de la temporalidad más baja. | SUPPORTED | ☐ |
| cl-focar-lo-que-pasa-en-4h | Pon el foco en lo que está pasando en 4 horas. | SUPPORTED | ☐ |
| cl-foco-temporalidad-baja-puede-liar | La lectura de la bajada en la temporalidad más baja puede liar mucho cuando el foco está en ella. | INSUFFICIENT | ☐ |
| cl-ir-a-15m-para-vela-4h | Si esto es una vela de 4 horas, ve a 15 minutos. | SUPPORTED | ☐ |
| cl-nocion-importante-sobre-que-pasa | Es importante tener una noción de qué está pasando. | SUPPORTED | ☐ |
| cl-vela-4h-aparece-como-bajada-agresiva-en-15m | Una vela de 4 horas aparece como una bajada muy agresiva en la temporalidad de 15 minutos. | SUPPORTED | ☐ |
| rel-apariencia-agresiva-depende-vista-15m | DEPENDS_ON: vela-4h-aparece-como-bajada-agresiva-en-15m → ir-a-15m-para-vela-4h | SUPPORTED | ☐ |

