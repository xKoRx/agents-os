# OWNER-REVIEW-GUIDE — CLUTIFX CH01 full-live-v2

Guía para la revisión humana del Owner. El Owner mira el video original (`~/mke/course/ep01-intro.mp4`, 34:03.9, SHA `4de8f12d…`) y califica la fidelidad del conocimiento extraído. **Este documento no contiene ninguna calificación rellenada y no dice al Owner si la extracción es correcta.**

## Cómo calificar (etiquetas del Owner — nunca auto-rellenar)

```text
CORRECT          — el statement representa fielmente lo dicho/mostrado en ese tramo
PARTIAL          — captura parte; falta matiz, condición o excepción
MISSING          — el tramo contenía conocimiento relevante que MKE no extrajo
WRONG            — el statement contradice lo dicho/mostrado
DUPLICATE        — conocimiento repetido sin valor agregado
OVERGENERALIZED  — pierde condiciones/alcance del original
```

Reglas de contexto:

- `SUPPORTED_BY_AUTOMATED_REVIEW` **no significa correcto**: es el veredicto del reviewer automático, no verdad externa ni humana. Igualmente, `UNSUPPORTED_*` no significa falso. El Owner decide con el video en la mano.
- Cada statement se puede rastrear: `claims.jsonl` (statement + `evidence_ids`), `transcript.json` (texto asr-*), timestamps de frames (PTS).
- Los timestamps de frames de esta guía están convertidos a mm:ss del video.

---

## 1. Cinco muestras distribuidas (revisión detallada sugerida)

### 1.1 · w0002 · 00:09–00:36

- **Transcripción real del tramo**: asr-00001 (00:05–00:19) «Hola, bienvenido al curso completo. Aquí vas a descubrir la estrategia en profundidad…»; asr-00002 (00:19–00:34) «Este va a ser el primer capítulo, un poco así introducción, pero vamos a cubrir todo…»; asr-00003 (00:34–00:49) «Así que nada, vamos directamente al grano. El formato… similar al del curso intermedio…».
- **Claims extraídas (25)** — veredicto del reviewer automático entre corchetes, no verdad:
  - `cl-audiencia-procedente-intermedio` «El instructor considera probable que la audiencia proceda de su curso intermedio.» [SUPPORTED]
  - `cl-curso-completo` «Este contenido es el curso completo.» · `cl-curso-completo-amplia-intermedio` · `cl-curso-intermedio-sienta-base` · `cl-estrategia-en-profundidad` [SUPPORTED]
  - `cl-capitulo-cubre-bias / -entradas / -estrategia / -riesgo` · `cl-capitulo-explica-noticias` · `cl-capitulo-incluye-conceptos-desconocidos` · `cl-primer-capitulo-introduccion` [SUPPORTED]
  - `cl-no-requiere-curso-intermedio` (rule) · `cl-info-intermedio-no-totalmente-relevante` [SUPPORTED]
  - Observaciones visuales (VIDEO_OBSERVED, frame @00:12): `cl-grafica-eurusd` (acumulada con w0130, 2 refs) · `cl-dos-bandas-azules` · `cl-fecha-grafica` «fecha 24/6/2025» · `cl-descenso-reciente-eurusd` «desciende desde ≈1.16220…» · `cl-temporalidad-cinco-minutos` · parámetros `cl-nivel-1-15728`, `cl-nivel-1-15744`, `cl-nivel-1-15797`, `cl-nivel-1-16148` [todos SUPPORTED]
  - **No soportadas (automático)**: `cl-formato-similar-intermedio` «El formato del curso completo será parecido al formato del curso intermedio.» [INSUFFICIENT] · `cl-primer-capitulo` «Este es el primer capítulo del curso.» [INSUFFICIENT]
- **Relations (1)**: `rel-continuidad-sin-curso-intermedio` DEPENDS_ON [SUPPORTED].
- **Qué mirar específicamente**: (a) en el frame de 00:12, verificar los cuatro niveles rotulados (1.15728 / 1.15744 / 1.15797 / 1.16148), la fecha 24/6/2025, las dos bandas azules y el tramo de descenso desde ≈1.16220; (b) las dos claims marcadas INSUFFICIENT citan un transcript que enuncia literalmente el contenido («vamos a cubrir todo», «formato… similar al del curso intermedio») — el Owner decide si el reviewer fue demasiado estricto o apropiadamente conservador aquí.

### 1.2 · w0037 · 08:22–08:33

- **Transcripción**: asr-00067 (08:17–08:23) «bearish otra vez, que en Libra están formados…»; asr-00068 (08:23–08:28) «que se formó el rango bearish aquí arriba, es cuando el precio empezó a revertir»; asr-00069 (08:29–08:34) «Otra vez, rango bullish en Libra, teníamos este objetivo para hoy…».
- **Claims (6)**: `cl-comparacion-diaria-eurusd-gbpusd` [grounding SUPPORTED → publicada INSUFFICIENT por atomicidad COMPOSITE, 2 frames 08:24/08:25] · `cl-gbpusd-seleccionado` (procedure_step, 3 frames 08:22–08:24) · `cl-objetivo-hoy-rango-bullish-libra` «objetivo para hoy el nivel 1.37489» [SUPPORTED] · `cl-rango-bearish-libra-formado` · `cl-rango-bullish-libra-formado` · `cl-reversion-tras-rango-bearish-libra` [SUPPORTED].
- **Relations (2)**: `rel-reversion-depende-rango-bearish-libra` [SUPPORTED] · `rel-objetivo-depende-rango-bullish-libra` [INSUFFICIENT].
- **Qué mirar específicamente**: (a) en 08:22–08:33, confirmar los dos paneles diarios EURUSD/GBPUSD y el objetivo 1.37489 en pantalla; (b) `cl-comparacion-diaria-eurusd-gbpusd` es una de las 5 degradadas COMPOSITE: el reviewer la dio por soportada pero la política de atomicidad la publica como no soportada — el Owner decide si esa política de publicación le parece correcta viendo este caso concreto.

### 1.3 · w0068 · 16:47–17:00

- **Transcripción**: asr-00134 (16:39–16:47) «Toma del bajo, reacción bullish, pues tenemos Tartle Sup.»; asr-00135 (16:47–16:53) «Concepto muy importante porque el Tartle Sup es lo que marca que el inicio del movimiento se puede dar ya.»; asr-00136 (16:53–17:02) «si aquí estás buscando ya para tomar longs, tu stop loss tendría que estar seguro debajo del Tartle…».
- **Claims (4)**: `cl-stop-loss-long-debajo-turtle-soup` (rule; acumulada con w0069 — unión de 3 refs) · `cl-turtle-soup-concepto-importante` · `cl-turtle-soup-tras-toma-bajo-bullish` [SUPPORTED] · `cl-turtle-soup-indicia-inicio-movimiento` [INSUFFICIENT].
- **Relations (2)**: `rel-indicio-inicio-movimiento-requiere-patron`, `rel-stop-loss-long-requiere-patron` [SUPPORTED].
- **Qué mirar específicamente**: (a) verificar la regla del stop loss bajo el Turtle Soup contra lo dicho en 16:53–17:02; (b) la claim INSUFFICIENT tiene la razón «la evidencia dice "Tartle Sup", pero no establece que se refiera a "Turtle Soup"» — es la misma expresión oral del instructor (variante del ASR); el Owner decide si ese criterio de equivalencia léxica es demasiado estricto para calibrar grounding.

### 1.4 · w0099 · 25:39–25:48

- **Transcripción**: asr-00207 (25:35–25:52) «Luego, concepto de failure swing, ya lo visteis también un poco en el curso intermedio. El failure swing es cu…».
- **Claims (3, todas SUPPORTED)**: `cl-failure-swing-definition` «El failure swing es cuando el precio no consigue hacer un nuevo bajo.» · `cl-failure-swing-has-multiple-cases` «puede darse en varios casos.» · `cl-failure-swing-seen-in-intermediate-course` «ya se había visto parcialmente en el curso intermedio.»
- **Relations**: 0.
- **Qué mirar específicamente**: (a) si la definición captura la condición completa dicha en el tramo o pierde matices (marca PARTIAL/OVERGENERALIZED si aplica); (b) si «varios casos» corresponde a lo dicho o es una generalización; (c) si faltó conocimiento relevante en 25:39–25:48 (marca MISSING).

### 1.5 · w0128 · 32:55–33:12

- **Transcripción**: asr-00296–00304 (32:55–33:14, segmentos cortos) «También importante para saber / un poco de noción de qué está pasando. / Si esto es una vela de 4 horas, tú vas / a ir a 15 minutos y esto / lo vas a ver como una bajada así, muy / agresiva. ¿Vale? Esto te puede / liar mucho si tienes el foco en la / temporalidad más baja. Si tú te alejas / y pones el foco en lo que está pasando en 4 horas…».
- **Claims (6)**: `cl-ir-a-15m-para-vela-4h` · `cl-vela-4h-aparece-como-bajada-agresiva-en-15m` · `cl-nocion-importante-sobre-que-pasa` · `cl-alejar-vista-de-temporalidad-baja` · `cl-focar-lo-que-pasa-en-4h` [SUPPORTED] · `cl-foco-temporalidad-baja-puede-liar` [INSUFFICIENT — evidencia partida en 3 micro-segmentos; razón: «no identifica explícitamente "esto"»].
- **Relations (1)**: `rel-apariencia-agresiva-depende-vista-15m` [SUPPORTED].
- **Qué mirar específicamente**: (a) escuchar 33:02–33:12 completo y decidir si la claim INSUFFICIENT sí está dicha (el referente de «esto» es explícito al oír el tramo) — sonda directa de la severidad del reviewer con segmentación fina del ASR; (b) verificar la fidelidad de «bajada muy agresiva en 15m».

---

## 2. Ventanas rechazadas — riesgo de cobertura (muestras representativas)

Una ventana rechazada = ese tramo no aportó conocimiento de ESA ventana (decisión contractual fail-closed). Que una ventana vecina se acepte **no prueba** que la cobertura se recuperó; abajo se indica el hecho verificable (solape de evidencia) o UNPROVEN.

| Window | Time | Categoría | Razón (durable) | Vecinos | Conocimiento del tramo |
|---|---|---|---|---|---|
| w0003 | 00:37–00:44 | bad evidence ref | `record cl-ir-directamente-al-grano cites unknown evidence ref "asr-00003 [34850-49400]"` (razón original duró en el journal REJECTED; el live la mostró como «rejected in a previous attempt» por el resume) | w0002✓ w0004✓ | **Solape existe**: 8 records canónicos citan asr-00003 (00:34–00:49) — p.ej. `cl-formato-similar-intermedio`, `cl-curso-intermedio-no-supone-problema`, `cl-no-requiere-curso-intermedio`, `rel-continuidad-sin-curso-intermedio`. El Owner decide si ese solape cubre lo dicho en 00:37–00:44. |
| w0034 | 07:32–07:42 | identity divergence determinista (kind: observation vs parameter en `cl-grafico-eurusd`) | w0031 propuso observation, w0034 parameter | w0031✓ w0032✓ w0033✓ w0035✓ | **Solape parcial**: 3 records citan asr-00059/61 dentro del tramo (`cl-observar-completado-rangos` — publicada INSUFFICIENT, `cl-importancia-rangos-navegar-precio`, `cl-objetivo-conocer-direccion-precio`). |
| w0054 | 12:45–12:57 | structural relation divergence (`rel-rango-bajista-depende-apertura-arriba`: subject endpoint difiere entre w0053 y w0054) | sin equivalence review (divergencia estructural) | w0053✓ w0055✓ | **Solape fuerte**: 15 records citan asr-00110/111 (00:12:31–13:08), incluida `rel-rango-bajista-depende-apertura-arriba@1` (versión de w0053, la que sobrevivió). La variante de w0054 fue descartada. |
| w0058 | 13:39–13:56 | epistemic divergence (`cl-rango-pendiente`: VIDEO_OBSERVED vs INSTRUCTOR_SAID; w0059 rechazada por la misma colisión) | dos ventanas consecutivas perdidas (13:39–14:12) | w0057✓ w0059✗ w0060✓ | **UNPROVEN**: ningún record canónico tiene evidencia dentro de 13:39–13:56. El concepto `cl-rango-pendiente` existe (primero observado en w0051) pero la re-observación de este tramo se perdió íntegra. Caso concreto de pérdida de cobertura para evaluar. |
| w0094 | 23:56–24:12 | semantic DIVERGENT — **el Owner clasificó OBVIOUSLY_EQUIVALENT** («La SMT» vs «Una SMT»): sobre-rechazo conservador, costo de cobertura | adjudicación #8 | w0093✓ w0095✓ | **Solape fuerte**: 13 records citan asr-00197 (23:42–24:11) propuestos por w0093 (aceptada), incluida `cl-smt-no-requerida-entre-dos-velas@1` — la claim misma en disputa quedó canónica por w0093. |
| w0122 | 30:56–31:16 | semantic DIVERGENT (taxonómica «la apertura es una de las partes de la vela» vs evento «la vela abre») — humano OBVIOUSLY_DIVERGENT, engine de acuerdo | adjudicación #16 | w0120✓ w0123✓ | **Solape existe**: 7 records citan asr-00266/270 (líneas de sesión 1h/5h NY, comportamiento de la vela); la versión taxonómica de w0120 quedó canónica. |

Resto de rechazadas (20): mismas familias — 10 kind parameter-vs-observation más (w0045, w0049, w0062, w0065, w0072, w0074, w0102, w0116, w0117, w0118), 2 semánticas AMBIGUOUS→DIVERGENT (w0028, w0078, w0109), 1 semántica con condición añadida (w0098), 1 bad-ref (w0110), 1 kind procedure_step (w0088). Detalle completo en WINDOWS.md y EQUIVALENCE-DECISIONS.md.

---

## 3. Muestra de calibración de grounding (statement + evidencia; sin adjudicar)

El Owner determina si el reviewer automático fue demasiado estricto o apropiadamente conservador. Selección distribuida a lo largo del capítulo.

### 3.1 Cinco SUPPORTED (automático)

| # | Record (ventana 1.ª obs.) | Statement | Evidencia citada |
|---|---|---|---|
| S1 | `cl-formato-parecido-curso-intermedio` (w0004) | «El formato que se seguirá será un poco parecido al del curso intermedio.» | asr-00003 [00:34–00:49] «…El formato que voy a seguir va a ser un poco similar al del curso i…» |
| S2 | `cl-precio-actua-como-una-cadena` (w0020) | «El precio actúa como una cadena.» | asr-00037 [04:35–04:41] «…el precio actúa como una cadena donde el precio…» |
| S3 | `cl-rango-reiniciado-apertura-arriba` (w0053, rule) | «En el rango reiniciado, "en contra" significa que se abre por arriba del doble.» | asr-00110 [12:31–12:48] «En resumen, rango reiniciado nos abre en contra de nuestro doble, en contra significa que abre por arriba…» |
| S4 | `cl-presentar-concepto-smt` (w0082) | «A continuación se presenta el concepto SMT.» | asr-00174 [20:45–21:23] «Vamos a seguir. Concepto SMT. Ya está explicado también en el curso intermedio…» |
| S5 | `cl-m15-facilita-encontrar-order-blocks` (w0111, rule) | «Si vamos a M15, va a ser mucho más fácil encontrar order blocks.» | asr-00249 [28:37–28:43] «M15 va a ser mucho más fácil encontrar order blocks…» |

### 3.2 Cinco INSUFFICIENT (automático)

| # | Record (ventana) | Statement | Evidencia citada |
|---|---|---|---|
| I1 | `cl-price-completes-ranges` (w0032) | «El precio va completando los rangos.» | asr-00056 [07:09–07:17] «…va formando rangos los va completando y va como haciendo sus sus cosas…» |
| I2 | `cl-intervalo-inicial-15m` (w0055) | «El gráfico de EURUSD se muestra inicialmente con un intervalo de 15 minutos.» | frame @12:58 (único) |
| I3 | `cl-turtle-soup-indicia-inicio-movimiento` (w0068) | «El Turtle Soup marca que el inicio del movimiento se puede dar ya.» | asr-00135 [16:47–16:53] «…el Tartle Sup es lo que marca que el inicio del movimiento se puede dar ya.» |
| I4 | `cl-revision-order-block-m10` (w0112) | «Vamos a revisar el gráfico de 10 minutos para comprobar si allí se ve el order block de esa venta.» | asr-00250 [28:43–28:55] «hoy, 15 no se ve, a ver si en 10, no se ve muy claro…» + frames @28:46/@28:47 |
| I5 | `cl-foco-temporalidad-baja-puede-liar` (w0128) | «La lectura de la bajada en la temporalidad más baja puede liar mucho cuando el foco está en ella.» | asr-00301–00303 [33:05–33:11] «agresiva. ¿Vale? Esto te puede / liar mucho si tienes el foco en la / temporalidad más baja…» |

### 3.3 Contradicted (4 claims + 1 relation — todas las que existen)

| # | Record (ventana) | Statement | Evidencia citada |
|---|---|---|---|
| C1 | `cl-seleccion-vela-blanca-grande` (w0025) | «La vela blanca grande de la zona central aparece seleccionada.» | frame @05:32 |
| C2 | `rel-cierre-fuera-contradice-cierre-dentro` (w0075, CONTRADICTS) | `cl-cierre-fuera-rango-invalida` CONTRADICTS `cl-intrabar-turtle-soup-requiere-cierre-rango` | asr-00160–00162 [18:56–19:17] (reglas complementarias según el reviewer) |
| C3 | `cl-objetivo-inicial-1-15052` (w0127) | «El precio objetivo inicial es 1,15052.» | frame @32:50 |
| C4 | `cl-objetivo-intermedio-1-15695` (w0127) | «Durante el ajuste, el precio objetivo se sitúa en 1,15695.» | frame @32:51 |
| C5 | `cl-linea-ascendente-2230-0115` (w0129) | «Se añade una línea ascendente desde ≈22:30 hasta ≈01:15.» | frames @33:36/@33:40 |

### 3.4 REVIEW_UNAVAILABLE (la única)

| Record (ventana) | Statement | Evidencia | Estado |
|---|---|---|---|
| `cl-rango-rectangular-vertical` (w0041) | «El rango está representado mediante un rectángulo vertical.» | frames @09:17/@09:19/@09:20 | el reviewer falló por parse fatal del backend (`assistant content is not a valid JSON object`); publicada UNSUPPORTED_REVIEW_UNAVAILABLE |

### 3.5 Degradadas COMPOSITE (las 5 — grounding SUPPORTED, publicadas no soportadas por atomicidad)

| Record (ventana) | Statement | Evidencia |
|---|---|---|
| `cl-dialogo-muestra-un-minuto` (w0019) | «El diálogo "Cambiar intervalo" muestra el valor 1 y la indicación "1 minuto".» | frame @04:21 |
| `cl-comparacion-diaria-eurusd-gbpusd` (w0037) | «La vista muestra los gráficos diarios de EURUSD y GBPUSD.» | frames @08:24/@08:25 |
| `cl-vela-abre-toma-high-cierra-adentro` (w0051) | «Esta vela abre, toma el high y cierra adentro.» | asr-00106 [11:36–11:51] «…esta vela abre, toma el high y nos cierra adentro…» + frames @11:48/@11:50/@11:59 |
| `cl-rango-se-puede-eliminar-por-cierre-fuera` (w0076) | «Este rango se puede eliminar porque la vela cierra fuera.» | asr-00165 [19:26–19:30] «…este lo podríamos ya eliminar porque la vela cierra fuera…» + frames @19:24/@19:28 |
| `cl-linea-une-maximos-eurusd-gbpusd` (w0096) | «Una línea horizontal pasa por máximos de velas de EURUSD y de GBPUSD.» | frames @24:36/@24:48 |

---

## 4. Muestra de identidad (política, sin rediseño)

Casos que el Owner debe ver para decidir si las decisiones del ladder a escala dañan materialmente la fidelidad del conocimiento:

1. **Humano OBVIOUSLY_EQUIVALENT → engine DIVERGENT (sobre-rechazo, costo de cobertura)**: adjudicación #8, w0093→w0094, `cl-smt-no-requerida-entre-dos-velas`: «La SMT no tiene que aparecer entre estas dos velas.» vs «Una SMT no tiene que ser entre estas dos velas.» — única diferencia definiteness; w0094 completa rechazada. Consecuencia de cobertura en §2 (w0094).
2. **AMBIGUOUS → DIVERGENT (fail-closed según prompt congelado)**, 3 casos: #2 w0028 («hay que ir viendo» vs «observar» — modalidad); #6 w0078 («vela… deja de ser un rango» vs «precio… deja de ser válido» — sujeto+predicado); #12 w0109 («ahora un momento» vs «para verlo claro» — calificadores).
3. **Kind divergente recurrente (12 de las 16 deterministas)**: el modelo alterna kind para el mismo hecho — en 8 casos es parameter-vs-observation sobre el hecho visual recurrente instrumento/temporalidad: `cl-instrumento-eurusd` (w0062, w0074, w0116, w0117), `cl-grafico-eurusd` (w0034, w0065), `cl-grafico-temporalidad-15m` (w0072), `cl-activo-eurusd` (w0102); las otras 4 son otros pares de kind (w0045 observation/claim, w0049 claim/observation, w0088 claim/procedure_step, w0118 procedure_step/claim). Cada ocurrencia cuesta la ventana completa (pérdida estructural de cobertura; el ladder evita corrupción, no pérdida).
4. **VIDEO_OBSERVED vs INSTRUCTOR_SAID**: w0058 y w0059 rechazadas por la misma colisión con `cl-rango-pendiente` de w0051 (epistemic difiere) — dos ventanas consecutivas perdidas, tramo sin solape (§2).
5. **Divergencia estructural de relations**: w0054 y w0092 — mismo relation id con subject endpoint distinto; la versión del primer proponente queda canónica y la variante se descarta con la ventana.
6. **EQUIVALENT → APPLY correcto (para contrastar)**: #5 w0068→w0069 `cl-stop-loss-long-debajo-turtle-soup` — unión aplicada: statement first-observed preservado, 3 evidence refs, 2 invocations en provenance, verificado en auditoría física.
7. **Deterministic-equivalent sin crecimiento**: w0011 re-propuso idéntico (tras normalización conservativa) `cl-estrategia-se-basa-principalmente-en-rangos` con evidencia ya contenida → registro de ladder sin nueva unión.

---

## Recordatorio de límites

- Las etiquetas del Owner (CORRECT/PARTIAL/MISSING/WRONG/DUPLICATE/OVERGENERALIZED) las pone exclusivamente el Owner.
- `CHAPTER_01_ACCEPTED` y `READY_TO_SCALE_CORPUS` siguen `PENDING_OWNER_REVIEW` / `NO` hasta la decisión.
- Este pack no autoriza fixes de producto, prompts nuevos, rerun ni capítulo 02; las deudas técnicas señaladas (fragilidad L2 al transporte, fatal transiente mata el run, bad refs 3.1%, severidad INSUFFICIENT, parameter-vs-observation recurrente) quedan para adjudicación posterior.
