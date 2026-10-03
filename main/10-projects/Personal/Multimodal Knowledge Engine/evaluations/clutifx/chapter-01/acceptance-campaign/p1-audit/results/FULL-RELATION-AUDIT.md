# FULL RELATION AUDIT — Capítulo 01 Clutifx (full-live-v2)

Auditoría source-grounded de las **130 RELATIONS canónicas** (`claim_relation`) del store
`full-live-v2/claims.jsonl`, verificadas contra transcript completo (`transcript.json`),
ventanas del corpus (`corpus/wNNNN.json`) y frames (`media-run/evidence/objects/*.png`).

- Fuente auditada: `evaluations/clutifx/chapter-01/full-live-v2/claims.jsonl` (130 `claim_relation` + 803 claims)
- Veredictos del engine auditados: 112 GROUNDING_SUPPORTED / 17 GROUNDING_INSUFFICIENT / 1 GROUNDING_CONTRADICTED
- Detalle por relation: `relations-audit.jsonl` (una línea por relation)

## 1. Distribución de etiquetas

| Label | N | % |
|---|---|---|
| CORRECT | 126 | 96,9 % |
| WRONG_TYPE | 2 | 1,5 % |
| WRONG_ENDPOINT | 0 | 0,0 % |
| UNSUPPORTED | 2 | 1,5 % |
| **Total** | **130** | 100 % |

**Correct rate: 126/130 = 96,9 %.**

Distribución cruzada con el veredicto del engine:

| Engine | N | CORRECT | WRONG_TYPE | UNSUPPORTED |
|---|---|---|---|---|
| GROUNDING_SUPPORTED | 112 | 111 | 1 | 0 |
| GROUNDING_INSUFFICIENT | 17 | 15 | 1 | 1 |
| GROUNDING_CONTRADICTED | 1 | 0 | 0 | 1 |

- Precisión de las aceptaciones del engine: **111/112 = 99,1 %** (un único falso positivo de tipo).
- De los 18 rechazos del engine, **15 eran falsas negativas** (83 %): la fuente sí soporta la relación
  y el rechazo proviene casi siempre de **citación de evidencia truncada** o de un criterio
  inconsistente entre relations gemelas.

Materialidad: **MATERIAL=YES 108 / MATERIAL=NO 22** (metadidáctica del curso, acciones de
dibujo/diagrama, resolución deíctica de ejemplos, promo y aritmética de la herramienta de posición).

## 2. Relations no CORRECT (4)

### 2.1 WRONG_TYPE

1. **`rel-reiniciado-pendiente-mismo-esquema`** (EQUIVALENT_TO, engine SUPPORTED) —
   `cl-esquema-mostrado-rango-reiniciado` EQUIVALENT_TO `cl-rango-pendiente-esquema-mostrado`.
   «Rango reiniciado» y «rango pendiente» son **tipos distintos** en el propio capítulo (contra
   tendencia vs a favor). El frame `p64800000` rotula el esquema como RANGO PENDIENTE y asr-00108
   nombra «rango reiniciado» al esquema bajista; la co-clusiva de asr-00109 («rango reiniciado o
   rango pendiente... se refiere a esto») no hace semánticamente equivalentes las dos claims (una
   asigna etiqueta, la otra asigna referencia). Único falso positivo de las 112 aceptadas.

2. **`rel-rango-abajo-depende-rango-contra`** (DEPENDS_ON, engine INSUFFICIENT) —
   `cl-rango-para-abajo` DEPENDS_ON `cl-rango-en-contra`.
   El rechazo del DEPENDS_ON es acertado, pero la conexión existe: «se te forma un rango en contra
   y para abajo» es una única mención con dos descripciones coordinadas del mismo rango. El tipo
   adecuado sería de equivalencia/co-referencia, no de dependencia (sin marcador direccional).

### 2.2 UNSUPPORTED

3. **`rel-cierre-fuera-contradice-cierre-dentro`** (CONTRADICTS, engine CONTRADICTED) —
   Rechazo **correcto**. La fuente presenta dos reglas complementarias (cierre dentro = requisito
   del intrabar Turtle Soup, asr-00159/00160; cierre fuera = el rango deja de valer,
   asr-00161/00162). Ninguna contradice a la otra ni el discurso declara esa oposición.

4. **`rel-toma-low-requiere-apertura`** (DEPENDS_ON, engine INSUFFICIENT) —
   Rechazo **correcto**. «Que la nueva vela abra, tome el low, así, forme nuevo rango»: entre
   abrir y tomar el low hay sola yuxtaposición temporal, sin marcador de dependencia (a diferencia
   del «así» que sí marca tome-low→forme-rango en la misma frase).

## 3. Falsas negativas del engine (15 rechazos que la fuente sí soporta)

Patrón dominante: **la evidencia citada en la relation estaba truncada** y el segmento/continuación
— o el frame citado a nivel de claim — completa el soporte. En varios casos además hay
**inconsistencia de criterio** con relations gemelas aceptadas.

| Relation | Endpoints (subj → obj) | Soporte encontrado |
|---|---|---|
| `rel-caso-bajista-depende-toma-maximo` | caso tartel sub bajista → toma máximo anterior | Definición en la misma ventana (asr-00124: «tartel sub se refiere básicamente a tomar el alto... y tener la reacción») + frame `p84240000` con el máximo previo marcado antes del giro bajista. |
| `rel-eliminar-rango-tras-supera-rango` | eliminar rango → precio supera borde superior | Frame `p110520000`: la vela blanca supera claramente el borde superior del rango resaltado; «Una vez pasa esto, ya puedes eliminar este rango» (deixis resuelta por el vídeo). |
| `rel-olvidar-rango-tras-supera-rango` | olvidar rango → precio supera borde superior | Ídem. |
| `rel-reanalizar-tras-supera-rango` | reanalizar → precio supera borde superior | Ídem. |
| `rel-exageracion-depende-cierre-lejano` | order block exagerado → vela cerrada muy fuera | asr-00248 (no citado): «es un poco **exagerado porque está cerrado muy fuera**»; causal explícito. |
| `rel-longs-dependen-de-vela-alcista` | longs brutales → anticipas vela alcista | asr-00292 (no citado): «**Por lo tanto**, tú aquí tienes unos longs brutales...». |
| `rel-objetivo-depende-rango-bullish-libra` | objetivo 1,37489 hoy → rango bullish en Libra | asr-00069 asocia ambos («rango bullish en Libra, teníamos este objetivo para hoy»); frame `p45810000` con la línea en 1,37489 sobre GBPUSD. Presuposición anafórica, mismo criterio que `rel-completar-rango-depende-formacion` (aceptada). |
| `rel-rango-bearish-completo-requiere-formado` | completa el bearish → forma un rango bearish | «forma uno bearish, **completa el bearish**»: anáfora + presuposición; mismo criterio que la gemela aceptada. |
| `rel-rango-gbpusd-depende-de-smt` | GBPUSD es rango → esto es una SMT | «esto es una SMT **que nos indica que** esto de GIP es un rango también»; «GIP» = transcripción de GBP; frame `p132480000` muestra el rango dibujado en GBPUSD y la claim sujeto está SUPPORTED con ese frame. |
| `rel-rangos-antes-de-subir-en-rango-contrario` | completar rangos antes de subir → rango contrario en 4h | asr-00156 (no citado): «se nos forma un rango contrario a nuestra dirección, **puede pasar que** el precio vaya a completar rangos antes de subir». |
| `rel-rr-final-depende-del-objetivo` | R/R 10,49 → objetivo 0,00881 | Frame `p177480000`: mismo panel con Objetivo 0,00881, Stop 0,00084 y R/R 10,49; 0,00881/0,00084 ≈ 10,49. Criterio inconsistente: la gemela `rel-rr-final-depende-del-stop` fue aceptada con el mismo argumento aritmético. |
| `rel-smt-requiere-fallo-objetivo-correlado` | formación es SMT → par correlacionado (GBPUSD) no llega a objetivo | asr-00194 define el caso («que euro pueda llegar a completar y el par correlacionado... no llegue a su objetivo»); frames `p125550000`/`p125640000` identifican a GBPUSD quedándose bajo la línea. |
| `rel-smt-requiere-reversal-directo` | formación es SMT → par correlacionado (GBPUSD) pasa reversal | Ídem («...y pase el reversal directamente»). |
| `rel-subida-directa-depende-sin-nuevo-bajo` | Felur Swing subida directa → definición (no nuevo bajo) | «Felur Swing es cuando el precio no consigue hacer el nuevo bajo, **pero** el rango se daría por creado y empieza a ir arriba directamente»: misma estructura definición+consecuencia que la gemela aceptada `rel-rango-creado-depende-sin-nuevo-bajo`. |
| `rel-pintado-negro-debajo-de-bajista` | pintar negro vela izquierda → vela izquierda bajista | Frames `p7470000`→`p7650000`: la vela rectangular izquierda (blanca, seleccionada) queda pintada de negro; el «así que» marca la dependencia y la deixis se resuelve visualmente. (Materialidad baja: acción de dibujo.) |

Nota a nivel claim detectada durante la auditoría: `cl-vela-cerrada-muy-fuera` y
`cl-vela-izquierda-bajista-probable` quedaron GROUNDING_INSUFFICIENT por las mismas citaciones
truncadas/deixis que los frames resuelven; conviene revisarlas en la auditoría de claims.

## 4. Relaciones materiales ausentes detectadas

1. **Cadena definicional del «tartel sub» bajista huérfana.** El store contiene claims
   definicionales soportadas (`cl-tartel-sub-toma-alto`, `cl-toma-alto-crea-rango`,
   `cl-toma-alto-completa-rango`, `cl-reaccion-tras-toma-alto`), pero **ninguna relation** las
   conecta entre sí ni con `cl-caso-tartel-sub-bajista`. En la fuente (w0064, asr-00121–00126) la
   definición precede inmediatamente a la clasificación del caso («Tartel sub básicamente se
   refiere a tomar el alto para crear un rango o para completarlo y tener la reacción después de
   tomar este alto hacia el otro lado. → En este caso, esto sería un tartel sub bajista»). El
   análogo alcista (Turtle Soup) sí tiene su red (`rel-indicio-inicio-movimiento-requiere-patron`,
   `rel-turtle-soup-pattern-depends-on-liquidity`, etc.). Relación material faltante sugerida:
   `cl-caso-tartel-sub-bajista` DEPENDS_ON `cl-tartel-sub-toma-alto` (+ `cl-reaccion-tras-toma-alto`).

2. **Etapa de manipulación ↔ Power 3 (menor).** Claims soportadas `cl-etapa-manipulacion-vela`,
   `cl-vela-manipulacion`, `cl-power-3-forma-vela` y `cl-power3-0100-0500-vela-4h` no tienen
   relation directa entre sí; el único enlace del clúster es `rel-compras-ideales-en-power3`
   (anafórico, «esta etapa»). El transcript («A las 5. Esto es el concepto de Power 3... las
   compras ideales... van a estar en esta etapa de manipulación de la vela») soportaría una
   relación explícita manipulación↔tramo 01:00–05:00. Parcialmente cubierta por anáfora; prioridad baja.

3. **Redundancia (no es error):** `rel-no-visible-depende-datos-ocultos` y
   `rel-visibilidad-smt-depende-ocultamiento` duplican contenido con pares de claims distintos
   (`cl-smt-no-visible-sin-estrategia` vs `cl-smt-no-visible-sin-conocer-estrategia`;
   `cl-datos-smt-ocultos` vs `cl-datos-smt-ocultos-a-veces`); ambas CORRECT. A nivel de store
   también existen claims duplicadas (`cl-compras-ideales-manipulacion-alcista` vs
   `...-contexto-alcista`). Sin efecto en el correct rate, relevante para deduplicación.

## 5. Integridad de endpoints y evidencia

- **130/130 relations** con `subject_id` y `object_id` resueltos a claims del store: 0 endpoints colgantes.
- **130/130** `evidence_ids` de tipo ASR resueltos a segmentos del transcript: 0 IDs inexistentes.
- Los 20 frames citados por relations existen en `media-run/evidence/objects/` (verificado en disco;
  17 frames clave inspeccionados visualmente).
- Sin relaciones con type fuera del vocabulario (DEPENDS_ON 117, EXCEPTION_TO 7, EQUIVALENT_TO 2, CONTRADICTS 4).

## 6. Veredicto

- **126/130 CORRECT (96,9 %)**. El capítulo 01 supera holgadamente el umbral de aceptación en relations.
- Los 4 defectos: 2 de tipo (1 falso positivo EQUIVALENT_TO aceptado por el engine, 1 DEPENDS_ON
  que debía ser equivalencia), 2 rechazos correctos (CONTRADICTS sin soporte; dependencia trivial sin marcador).
- El principal problema de calidad no es el ruido sino el **recall de las relations rechazadas**:
  15/18 rechazos eran falsas negativas causadas por citación de evidencia truncada y por criterio
  inconsistente entre relations gemelas (presuposición formación→completación, aritmética del R/R,
  estructura definición+consecuencia). Recomendación: re-auditar los UNSUPPORTED_INSUFFICIENT
  incluyendo el segmento siguiente al citado y la evidencia de las claims endpoint.
