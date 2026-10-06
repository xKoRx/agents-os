# P8 Final Audit 2 — A1 · FULL CLAIM AUDIT (w0001–w0033) · run P7b

- Run auditado: **candidato P7b @ e7bc387** (`/home/kor/mke/clutifx-ch01-rerun2-20261004/run-rerun2/claims.jsonl`), corpus por ventana `p8-final-audit2/corpus/`.
- Alcance: **30 ventanas aceptadas** de w0001–w0033 (rechazadas y sin claims: w0006, w0008, w0023 — cubiertas por otro worker). Población completa: **267 claims**, sin muestreo.
- Método: cada claim verificado contra transcript (cita textual) y, para claims visuales (niveles, colores, rectángulos, rótulos UI, temporalidad, OHLC), lectura directa del PNG citado (**~45 frames** leídos, agrupados por ventana). Recon v4 (`mke.claims-recon.v4`) confirmado en provenance.

## Cifras

| Métrica | Valor |
|---|---|
| Claims auditados | **267** |
| CORRECT | **240** (89.9%) |
| DUPLICATE | **27** (10.1%) |
| WRONG / PARTIAL / OVERGENERALIZED / UNVERIFIABLE | **0 / 0 / 0 / 0** |
| MATERIAL=YES | 124 |
| **Precisión material parcial** (CORRECT+DUPLICATE sobre MATERIAL=YES) | **124/124 = 100%** |
| Publicados (SUPPORTED_BY_AUTOMATED_REVIEW) | 157 (58.8%) |
| Precisión material sobre publicados | 86/86 = **100%** |
| MISSING_MATERIAL | **0** (P7: 2) |
| MISSING_NON_MATERIAL | 1 (w0004, logística «empezar desde cero») |

Criterio de materialidad: proposiciones de dominio trading (definición y tipos de rango, polaridad de velas, reglas completar/objetivo-contrario, cadenas precio-rangos, niveles de precio dibujados, forward-references operativos). Metadatos de UI (símbolo, TF, fuente, fecha, OHLC de cabecera, acciones de dibujo) = NO.

## Claims no perfectos

- **WRONG/PARTIAL: ninguno.** Primer rango auditado de la campaña sin ningún error material publicado (P7 tenía 1 WRONG retenido + 1 PARTIAL publicado).
- **Nota menor (CORRECT con caveat):** `cl-limite-superior-rango-1-15867` (w0015) — p18630000 muestra 1,15867; en p18720000 el asa movida marca 1,15869. La evidencia citada sostiene la cifra.
- **DUPLICATE (27):** repeticiones por solape de segmentos ASR entre ventanas contiguas — w0002×2 (→w0001), w0003×3 (→w0002), w0005×2 (→w0004), w0011×1 y w0012×1 (→w0010/w0011), w0027×4 (→w0026), w0028×5 (→w0027), w0029×3 (→w0027), w0030×4 (→w0029/w0030), w0031×2 (→w0030). Todas benignas; subió vs P7 (10) porque v4 re-emite más restatements.
- **`cl-valor-dialogo-un-minuto` (w0019, UNSUPPORTED_INSUFFICIENT):** el statement es fiel al frame («1» / «1 minuto»); el reviewer lo retuvo de forma conservadora. Correcto que no se publique sin soporte, pero es un falso negativo de contenido.

## Hallazgo principal: 110/267 claims (41.2%) sin publicar por reviewer degradado

- 109 `UNSUPPORTED_REVIEW_UNAVAILABLE` + 1 `UNSUPPORTED_INSUFFICIENT`. En `grounding.reasons` de w0001–w0005 ya aparece `vlm provider transport [retry-exhausted]`: **la tormenta de transporte golpeó al REVIEWER desde el inicio del run**, no solo al recon de las ventanas tardías (w0034+). El recon v4 sí produjo claims correctos en todo mi rango.
- **38 claims MATERIALES correctos quedaron fuera del store publicado**; descontando duplicados y cobertura cruzada, **~25 proposiciones materiales ausentes del store publicado**, entre ellas: los 4 niveles de w0002 (1,15728/1,15744/1,15797/1,16148), los bordes del rectángulo-plantilla de w0004 (1,15389/1,15006), `cl-estrategia-basa-rangos`+`cl-estrategia-se-basa-principalmente-en-rangos`+`cl-estrategia-rangos-no-mencionada-curso-intermedio` (w0010/w0011), `cl-binding-video-bias` (w0018), `cl-alto-vela-referencia-bajista` (w0022), los 3 «comprender qué rangos se completan» (w0025), el bloque failure-swing (w0027–w0029) y «el ejemplo no basta para operar» (w0032). Es el mayor gap del run P7b y es de disponibilidad (transporte), no de extracción.

## REGRESSION WATCH

1. **`cl-vela-negativa-mayoria` (baseline viejo w0009, polaridad invertida) → FIXED (con recovery completo).** w0009 vuelve a estar aceptada en P7b. `cl-vela-negativa-frecuente` («lo que se ve en la mayoría de las ocasiones es una vela negativa») es CORRECTO sin inversión: el antecedente de asr-00015/16 dentro de la ventana es la vela negativa, confirmado por el dibujo que el instructor pinta de negro (frame p12600000). La proposición correctiva «tampoco tiene que ser negativa como tal» (asr-00017) está ahora capturada DOS veces y ambas publicadas: `cl-vela-no-necesariamente-negativa` (w0009) y `cl-no-tiene-que-ser-negativo` (w0010). w0036 (rango A2) no contiene claims de polaridad; no hay dependencia entre workers.
2. **`cl-entradas-sirven-para-encontrar-bias` (baseline viejo w0011, relación invertida) → FIXED y PUBLISHED.** `cl-rangos-importantes-para-encontrar-entradas` y `cl-rangos-importantes-para-encontrar-bias-general` (w0011): sujeto «los rangos», relación correcta; ambos SUPPORTED (en P7 la variante «entradas» quedó sin publicar por crash del reviewer — aquí sí está en el store).
3. **Residuo P7 `cl-campo-cambiar-intervalo-15` (PARTIAL, w0019) → RESUELTO por descomposición.** P7b ya no afirma «15»: separa `cl-dialogo-cambiar-intervalo` (abierto) de `cl-valor-dialogo-un-minuto` («1»/«1 minuto», retenido INSUFFICIENT). Ninguna cifra falsa publicada.
4. **Residuo P7 `cl-nivel-eurusd-1-15067` (WRONG retenido): sin reincidencia.** No se emitió ningún claim de línea inexistente; las etiquetas de eje 1,04880/1,04760 de w0030–w0031 se citan como etiquetas, no como líneas dibujadas.

## Calidad de evidencia

- **Niveles verificados al dígito (17):** 1,15728 · 1,15744 · 1,15797 · 1,16148 (×2 ventanas) · 1,15006 · 1,15389 · 1,15142 · 1,15867 · 1,14748 · 1,15803 · 1,14968 · 1,15352 · 1,14973 · 1,15179 · 1,15160 · 1,15611 — todos coinciden con los dibujos/etiquetas; cero errores de dígito.
- **Drift temporal ventana↔frames:** los timestamps de los frames citados preceden sistemáticamente al `start_ms` de su ventana y el offset crece con el vídeo (~1–3 s en w0002; ~12–16 s en w0009–w0011). El contenido semántico corresponde siempre a la secuencia correcta (orden relativo preservado), pero la trazabilidad por ventana queda debilitada; sugiere bases de tiempo distintas (ASR/audio vs frames VFR).
- Otros frames fuera de ventana aislados (p.ej. w0005 cita p29610000; w0018/w0021/w0024 citan frames de minutos posteriores para parámetros constantes). No afecta verdad.

## Veredicto A1

Extracción impecable en mi rango: **0 WRONG, 0 PARTIAL, 0 missing material**, 100% de precisión material (parcial y sobre publicados), y las dos regresiones del baseline están FIXED con el conocimiento correctivo no solo capturado sino publicado. El riesgo real de P7b en w0001–w0033 no es de exactitud sino de **cobertura de publicación**: el reviewer VLM estuvo degradado desde la primera ventana y deja fuera del store 41% de los claims (incluidas ~25 proposiciones materiales), un problema de transporte/resiliencia y no de recon.

## FEEDBACK (Agents-OS)

- El corpus por ventana (claims+transcript+frames con paths absolutos) y el digest por script hicieron viable una pasada exhaustiva de 267 claims con ~45 lecturas de frame; mantener ese formato tal cual.
- Fricción 1 (la importante): `UNSUPPORTED_REVIEW_UNAVAILABLE` pasó de ~3.6% (P7) a 41.2% (P7b) en ventanas tempranas — el retry budget de 2 del reviewer agota con una tormenta larga y silencia claims correctos, incluidos 2 fixes de regresión parcialmente afectados. Sugerencias: (a) reintento diferido/post-storm de los claims en `REVIEW_UNAVAILABLE` (el recon ya pagó el coste; solo falta la pasada de review), (b) distinguir en `publication` «reviewer malfunction» de «insufficient evidence» para poder reprocessar selectivamente.
- Fricción 2: duplicados por solape ASR subieron a 27/267 (10%): un dedup por hash (utterance_id + normalización del statement) en el extractor eliminaría la clase completa sin tocar ventanas.
- Fricción 3: drift entre la base de tiempo de ventanas/ASR y la de los frames (offset creciente hasta ~16 s). Alinear el sampling de frames al reloj de `start_ms` o guardar el mapeo en el corpus evitaría que «evidencia fuera de ventana» sea ruido permanente en las auditorías.
- Positivo: la descomposición de claims compuestos en v4 (diálogo «Cambiar intervalo») eliminó el único PARTIAL publicado de P7; patrón a conservar para valores de UI editables.
