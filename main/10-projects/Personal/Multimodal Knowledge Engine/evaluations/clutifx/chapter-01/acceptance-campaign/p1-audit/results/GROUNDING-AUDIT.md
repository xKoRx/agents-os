# GROUNDING-AUDIT — Capítulo 01 Clutifx (acceptance-campaign / p1)

**Auditoría fuente-grounded del grounding reviewer (stateless, automated) del run L1.**
Fecha: 2026-10-03. Ámbito: 80 records non-supported (100 %) + muestra de 30 supported + 5 claims COMPOSITE degradados.
Salida detallada: `grounding-audit.jsonl` (110 líneas únicas).

> Nota de alcance: los 5 records del fixture `composite-degraded.jsonl` son **subconjunto de los 80 non-supported** (ids verificados: `cl-comparacion-diaria-eurusd-gbpusd`, `cl-dialogo-muestra-un-minuto`, `cl-linea-une-maximos-eurusd-gbpusd`, `cl-rango-se-puede-eliminar-por-cierre-fuera`, `cl-vela-abre-toma-high-cierra-adentro`). Por eso el JSONL tiene 110 líneas y no 115: cada record aparece una sola vez, con el análisis de atomicidad integrado en los 5 casos ATOMICITY_PROBLEM.

Método: para cada record se comparó (1) el request del invocation (la evidencia que el reviewer vio), (2) el veredicto y razones del reviewer, y (3) la fuente real: `full-live-v2/transcript.json` (segmentos citados y su contexto inmediato) y los PNG de `~/mke/clutifx-ch01-20260930/media-run/evidence/objects/` para todo claim visual. Criterio de &quot;disponible&quot;: evidencia del mismo trozo de discurso o frames de la misma sección temporal.

## 1. Distribución de clasificaciones de los 80 non-supported

| Clasificación | n | % |
|---|---|---|
| EVIDENCE_SELECTION_PROBLEM | 48 | 60,0 % |
| FALSE_NEGATIVE | 14 | 17,5 % |
| CORRECT_REJECTION | 8 | 10,0 % |
| ATOMICITY_PROBLEM | 5 | 6,3 % |
| ACTUALLY_CONTRADICTED | 4 | 5,0 % |
| PROVIDER_FAILURE | 1 | 1,3 % |

- **Tasa de falsos negativos (errores materiales del reviewer sobre lo que vio): 14/80 = 17,5 %.**
- **Impacto de no-publicación (records cuya proposición es verdadera y soportada en la fuente): 66/80 = 82,5 %.** La diferencia entre 66 y 14 es la cuota atribuible a la reconstrucción (citas de evidencia incompletas o equivocadas), no al reviewer: en esos 48 casos el reviewer rechazó correctamente el paquete de evidencia que recibió.
- El reviewer acertó al rechazar en 13/80 (8 CORRECT_REJECTION + 4 ACTUALLY_CONTRADICTED + 1 sin contenido por parse fatal) y acertó el grounding (SUPPORTED) pero la publicación degradó por atomicidad en 5.

## 2. Detalle de los 14 FALSE_NEGATIVE

| record_id | Qué vio el reviewer | Por qué es falso negativo |
|---|---|---|
| `cl-intervalo-inicial-15m` | 1 frame (778s) EURUSD 15M | «Inicialmente» = estado al inicio de la sección de ejemplos; frames 774-778s confirman 15M antes del salto a 1D (783s). |
| `cl-introduccion-pequena-smt` | 2 fragmentos SMT + «pequeña introducción» | Las dos citas + el contraste inmediato con el capítulo futuro soportan la proposición; «Esta» es deixis trivial. |
| `cl-no-dejar-nada-fuera` | «no me quiero dejar nada» | «Fuera» es el complemento idiomático de «dejarse nada»; sentido íntegro en la cita. |
| `cl-nueva-vela-marcada-en-el-grafico` | «la dejo aquí marcada» | Núcleo proposicional completo; «en el gráfico» es deixis forzada por el discurso. |
| `cl-objetivo-libra-zona-superior` | «el objetivo de libra estaba ahí arriba» | «Parte superior del gráfico» es la resolución forzada del señalamiento (el sample acepta el patrón idéntico cuando hay frame: `cl-objetivo-parte-superior-rango`). |
| `cl-pintar-vela-en-grafico` | «voy a pintar la vela ahora» | Dicho dibujando sobre el gráfico (frames 61-98s); «en el gráfico» es deixis forzada. |
| `cl-primer-capitulo` | «Este va a ser el primer capítulo...» | «Del curso» está pragmáticamente forzado («introducción», «vamos a cubrir todo»). |
| `cl-seleccion-vela-blanca-grande` | frame 332s | **Error de percepción del reviewer**: los tiradores rodean la vela blanca central-alta (la selección desaparece en 333s), no la vela negra superior derecha. |
| `cl-turtle-soup-extra-ocurre-a-veces` | «Intra Tartel Sub... Tartel Sub extra... hay veces que puede pasar» | «Tartel Sub/Tartle Sup» es el garble ASR de «Turtle Soup»; el contenido («a veces hay un extra») está citado. |
| `cl-turtle-soup-indicia-inicio-movimiento` | «el Tartle Sup es lo que marca...» | Cita literal salvo la variante ASR del nombre. |
| `cl-vela-izquierda-bajista-probable` | «Esta sería una vela bajista» + frame 83s | El frame citado muestra el rectángulo izquierdo seleccionado en el momento del enunciado; en 88s (p7920000) está pintado de negro, resolviendo la deixis. |
| `rel-rango-gbpusd-depende-de-smt` | «esto es una SMT que nos indica que esto de GIP es un rango también» | La dependencia está enunciada verbatim («que nos indica que»); «GIP» = garble ASR de GBP/libra. |
| `rel-rr-final-depende-del-objetivo` | frame con Objetivo 88,1 (0,00881), Stop 8,4, R:B 10,49 | 88,1 / 8,4 = 10,49: la dependencia es aritméticamente demostrable desde la propia evidencia. |
| `rel-subida-directa-depende-sin-nuevo-bajo` | 5 segmentos contiguos completos | «Felur Swing es cuando el precio no consigue hacer el nuevo bajo, pero... empieza a ir arriba directamente»: la definición con «es cuando... pero» enuncia la dependencia. |

Sub-patrones de los 14: (a) **equivalencia de identidad no aplicada** al garble ASR (3: Turtle Soup ×2, GBP «GIP» ×1); (b) **deixis de pantalla/discurso considerada no resuelta** (7); (c) **error de percepción visual** (1: `cl-seleccion-vela-blanca-grande`); (d) **exigencia de literalidad donde hay implication fuerte** (3: intervalo inicial, definición Felur Swing, aritmética del R:B).

## 3. Falsos positivos de la muestra de 30 supported

**1/30 (3,3 %): `cl-rangos-bajistas-otra-vez`.** La cita («bearish otra vez, que en Libra están formados») no contiene «se nos forman rangos», que está en asr-00066, no citado. La proposición es verdadera en la fuente, pero no derivable de la evidencia citada; es exactamente la misma forma que `cl-forma-rango-bearish`, que fue rechazado. Indica un criterio inconsistente frente a elisiones contextuales (más tolerante cuando el veredicto es SUPPORTED que cuando es INSUFFICIENT). Los otros 29 son correctos, incluidas las verificaciones visuales de transiciones de temporalidad y del panel de posición.

## 4. Los 5 COMPOSITE degradados

| record_id | ¿Debía dividirse la reconstrucción o el reviewer de atomicidad es sobre-estricto? |
|---|---|
| `cl-comparacion-diaria-eurusd-gbpusd` | **División correcta.** Dos aserciones independientes (gráfico 1D de EURUSD; gráfico 1D de GBPUSD). La reconstrucción debió emitir 2 claims. |
| `cl-linea-une-maximos-eurusd-gbpusd` | **División correcta.** Una comprobación por símbolo (EURUSD y GBPUSD), evaluable por separado. |
| `cl-dialogo-muestra-un-minuto` | **Sobre-estricto.** Valor «1» e indicación «1 minuto» son un único estado de UI: el hint es la renderización del valor introducido. Un hecho, no dos. |
| `cl-rango-se-puede-eliminar-por-cierre-fuera` | **Sobre-estricto.** «este lo podríamos ya eliminar porque la vela cierra fuera» es una sola oración hablada; la cláusula causal es la justificación del mismo aserto, no una segunda proposición. |
| `cl-vela-abre-toma-high-cierra-adentro` | **Sobre-estricto.** Cita literal de una sola cláusula que describe la forma de una vela; separar «abre»/«toma el high»/«cierra adentro» es granularidad absurda (cada trozo aislado carece de valor). |

Balance: 2/5 degradaciones justificadas (falta de split en reconstrucción), 3/5 sobre-estrictas (pérdida neta de 3 records soportados). Regla sugerida: los pares simétricos «X y Y» con entidades paralelas sí se dividen; las cláusulas causales («porque») y las descripciones multi-verbo de un mismo objeto visual no cuentan como proposiciones independientes.

## 5. Patrones sistemáticos

1. **El defecto dominante está en la selección de evidencia de la reconstrucción (48/80 = 60 %), no en el reviewer.** Forma recurrente: el claim reconstruye la frase completa del instructor pero cita solo los segmentos que contienen las palabras de contenido, dejando fuera el segmento adyacente con el antecedente o la continuación:
   - frases partidas por el segmentador ASR («se nos forma | [esto que lo llamamos orden]», «es un poco | [exagerado porque está cerrado muy fuera]», «donde el precio | forma un rango»): ~15 casos;
   - anafra/pronominalización con antecedente en el segmento previo («uno bajista», «forma uno bearish», «es muy importante...», «el formato que voy a seguir»): ~20 casos;
   - frames equivocados o ausentes para claims visuales/deícticos (R50 salvo error de percepción, R60 sin estado previo, R65/69/75 con el frame de 2 s antes del quiebre, R61 sin ancla textual): ~8 casos.
2. **El reviewer es sobre-estricto con deixis y con la implicación fuerte (14 FN).** Exige que cada palabra del statement esté en la cita («fuera», «del curso», «en el gráfico», «1 minuto») o que la dependencia esté enunciada con un conector, incluso cuando la definición («es cuando... pero»), la aritmética del propio frame (R:B = objetivo/stop) o la selección visual en curso la establecen.
3. **El contrato de review no aplica normalización de identidad sobre el garble ASR** (Tartel Sub/Tartle Sup ≡ Turtle Soup; GIP ≡ GBP). Provocó al menos 3 falsos negativos; el pipeline ya tiene una capa de equivalencia de identidad (`identity-equivalence-live.jsonl`) pero no alimenta al prompt de grounding.
4. **Consistencia asimétrica:** el mismo patrón evidencial se acepta en el lado supported y se rechaza en el non-supported (`cl-rangos-bajistas-otra-vez` aceptado vs `cl-forma-rango-bearish` rechazado; `cl-objetivo-parte-superior-rango` aceptado con frame vs `cl-objetivo-libra-zona-superior` rechazado sin frame). El criterio real parece ser «¿venía el frame/el segmento completo en la cita?», lo que confirma que la palanca de mejora está en la reconstrucción, no en el prompt del reviewer.
5. **El reviewer es fiable en lo literal y en lo visual verificable:** 4/4 contradicciones detectadas son reales (valores de objetivo 1,15067/1,15728 y no 1,15052/1,15695; la línea asciende desde 00:00, no desde 22:30; el estado previo a 1D no era 4H sino 15M; las reglas de cierre dentro/fuera no se contradicen), y la muestra supported solo arroja 1 falso positivo indulgente. El único caso de percepción visual errónea es `cl-seleccion-vela-blanca-grande`.
6. **1 provider failure** (`cl-rango-rectangular-vertical`, REVIEW_UNAVAILABLE por parse fatal): los frames muestran claramente el rectángulo vertical; requiere replay, no re-prompt.

## 6. Recomendaciones (por impacto)

1. **Reconstrucción:** al citar evidencia, incluir siempre el segmento anterior y posterior inmediato cuando el statement contenga deixis («esto», «una», «ese») o cuando la oración quede colgada en el borde de segmento. Resolvería ~48 de los 66 records perdidos.
2. **Grounding review:** añadir al contrato (a) equivalencia de identidad ASR→canónico, (b) regla de deixis forzada por discurso en screencast («el gráfico», «arriba/abajo»), (c) permitividad con cláusulas causales y descripciones multi-verbo de un mismo objeto (atomicidad).
3. **Replay** del parse fatal de `cl-rango-rectangular-vertical`.
4. Re-publicar tras fixes: 66 de los 80 records son recuperables (14 FN + 48 EVIDENCE_SELECTION + 3 composite sobre-estrictos + 1 provider failure).
