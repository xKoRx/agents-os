# Auditoría de aceptación A4 — Capítulo 01 Clutifx, Parte 4/4 (w0100–w0130)

Auditor: A4 (fuente-grounded). Rango: w0100–w0130, 24 ventanas aceptadas (se saltaron las rechazadas w0102, w0109, w0110, w0116, w0117, w0118, w0122). Se auditó el 100% de los claims (194), sin muestreo.

Autoridades usadas: `full-live-v2/transcript.json` (hablado) y los PNG 1920×1080 del corpus en `/home/kor/mke/clutifx-ch01-20260930/media-run/evidence/objects/` (visual). Se leyeron 55 frames; todos los claims VIDEO_OBSERVED fueron juzgados con al menos un frame citado leído (incluidas todas las lecturas numéricas de las herramientas de posición en w0115 y w0127, verificadas tooltip a tooltip). Convenciones de materialidad heredadas de A1/A3: reglas/observaciones de estrategia y estructura del esquema = MATERIAL=YES; lecturas de parámetros de UI de la herramienta de posición, símbolo/temporalidad/fuente, estilo de dibujos y metacomentarios de curso/audiencia = MATERIAL=NO.

## Totales

| Métrica | Valor |
|---|---|
| Claims auditados | 194 |
| CORRECT | 171 |
| DUPLICATE | 16 |
| PARTIAL | 6 |
| WRONG | 1 |
| OVERGENERALIZED / UNVERIFIABLE | 0 / 0 |
| MATERIAL=YES | 130 |
| MATERIAL=NO | 64 |
| Ventanas MISSING_MATERIAL | 0 |
| Ventanas MISSING_NON_MATERIAL | 0 |
| Ventanas NONE (missing) | 24 |

## Tabla por ventana

| Ventana | Claims | CORRECT | DUPLICATE | PARTIAL | WRONG | MATERIAL=YES | Missing |
|---|---|---|---|---|---|---|---|
| w0100 | 7 | 7 | 0 | 0 | 0 | 5 | NONE |
| w0101 | 9 | 6 | 2 | 0 | 0 | 6 | NONE |
| w0103 | 8 | 7 | 0 | 1 | 0 | 8 | NONE |
| w0104 | 5 | 3 | 2 | 0 | 0 | 5 | NONE |
| w0105 | 12 | 11 | 1 | 0 | 0 | 7 | NONE |
| w0106 | 8 | 5 | 0 | 2 | 1 | 4 | NONE |
| w0107 | 4 | 4 | 0 | 0 | 0 | 4 | NONE |
| w0108 | 6 | 6 | 0 | 0 | 0 | 3 | NONE |
| w0111 | 7 | 7 | 0 | 0 | 0 | 5 | NONE |
| w0112 | 9 | 6 | 2 | 0 | 0 | 7 | NONE |
| w0113 | 3 | 1 | 1 | 1 | 0 | 3 | NONE |
| w0114 | 4 | 3 | 1 | 0 | 0 | 4 | NONE |
| w0115 | 13 | 12 | 1 | 0 | 0 | 5 | NONE |
| w0119 | 8 | 8 | 0 | 0 | 0 | 2 | NONE |
| w0120 | 8 | 8 | 0 | 0 | 0 | 8 | NONE |
| w0121 | 5 | 2 | 3 | 0 | 0 | 5 | NONE |
| w0123 | 9 | 9 | 0 | 0 | 0 | 9 | NONE |
| w0124 | 7 | 6 | 1 | 0 | 0 | 7 | NONE |
| w0125 | 7 | 6 | 1 | 0 | 0 | 6 | NONE |
| w0126 | 5 | 5 | 0 | 0 | 0 | 5 | NONE |
| w0127 | 23 | 19 | 1 | 0 | 0 | 7 | NONE |
| w0128 | 6 | 6 | 0 | 0 | 0 | 6 | NONE |
| w0129 | 11 | 9 | 0 | 2 | 0 | 6 | NONE |
| w0130 | 10 | 10 | 0 | 0 | 0 | 3 | NONE |

## Hallazgos notables

1. **Un único error material (WRONG), en w0106, por renombrado del término CISD.** El instructor dice «en inglés se llama change instead of delivery» (asr-00233, ASR de *change in state of delivery*). El claim `cl-cambio-oferta-demanda-termino-ingles` cita como término «change in supply and demand» y bautiza el concepto en español como «cambio de oferta y demanda»: ni el término inglés citado ni el nombre español existen en la fuente. Los otros dos claims que heredan ese nombre inventado (`cl-cambio-oferta-demanda-parecido-cambio-tendencia`, `cl-order-block-importante-cambio-oferta-demanda`, ambos w0106) se etiquetan PARTIAL: la relación está dicha, el nombre no. Recomendación: normalizar el concepto a su forma dicha («change in state of delivery») antes de L2.

2. **Seis PARTIAL, ninguno grave.**
   - w0103 `cl-alto-a-final-de-vela`: la figura dibuja solo el caso del bajo (mechas inferiores + línea de lows); «ALTO» aparece únicamente dentro del rótulo textual.
   - w0113 `cl-15-no-se-ve-muy-claro`: el calificador «no se ve muy claro» pertenece al gráfico de 10m (asr-00250); del de 15m dijo «no se ve».
   - w0129 `cl-linea-descendente-2000-2230` y `cl-linea-ascendente-2230-0115`: las dos líneas del zigzag (manipulación→expansión) existen y la ascendente termina en ~01:15, pero los rangos horarios del claim no cuadran con el eje del esquema (la descendente baja de ~22:30 a ~23:30; la ascendente arranca ~00:45).

3. **Cero errores en las lecturas visuales numéricas.** Los 19 claims de parámetros (w0106 límites 1,13089/1,13978; w0115 entrada 1,14697 / objetivo 1,15034 / stop 1,14521 / stop 0,00337→0,00200 / R:B 1→1,91; w0127 apertura 1,14968, objetivos 1,15052→1,15695→1,15849 con diferencias 0,00084 (0,07%)→0,00727 (0,63%)→0,00881 (0,77%), importes 104000/134619.05/141952.38/96000, cantidad 4761904, R:B 8,65/10,49) coinciden exactamente con los tooltips y marcas de eje de los frames. También exactos: cambios de temporalidad 8h→15m (w0111), 15m→10m→30m (w0112), línea 1,15803 (w0119) y todos los rótulos del esquema Power 3 (0100/0500/4 HORAS).

4. **Garble de ASR heredado fielmente, sin error del extractor.** «Felur Swing» por failure swing (w0100/w0101, normalizado correctamente en w0100), «lo llamamos orden» por order block (w0108 `cl-cierre-fuera-forma-orden`, CORRECT contra la fuente; el término completo se confirma en w0111). En w0106 el garble «change instead of delivery» sí degeneró en el término inventado del punto 1.

5. **Duplicación cross-window (16 DUPLICATE).** Concentrada en: definición de failure swing y anuncio de capítulo (w0101↔w0100), comparación de lows entre brokers (w0104↔w0103, w0105↔w0104), «M15 más fácil para order blocks» y «venta de hoy» (w0112↔w0111), regla del long tras cierre por fuera (w0114↔w0113↔w0115), esquema = vela de 4h (w0121↔w0120), compras ideales en manipulación (w0124↔w0123), pregunta arriba/abajo (w0125↔w0124) y rango alcista en formación (w0127↔w0126). Todas con proposición idéntica o virtualmente idéntica; las paráfrasis con matiz distinto se mantuvieron CORRECT.

6. **Missing knowledge: sin huecos materiales.** Las 24 ventanas cierran en NONE: el transcript hablado está cubierto por los claims y los elementos visuales relevantes (rótulos SMT/BAJO-ALTO/OTRO BROKER, rectángulos, esquema Power 3 con 0100/0500/4 HORAS, herramienta de posición, pantalla final) están todos representados. El único fragmento no extraído con valor narrativo («Y falta el último [caso]», w0103) es navegación del temario ya implícita en la enumeración de casos de failure swing.

## Veredicto

La Parte 4 es de alta calidad: 171/194 CORRECT (88%), sin huecos de conocimiento material y con un solo error material (el renombrado CISD de w0106, que arrastra dos PARTIAL). Los 16 DUPLICATE y los 64 MATERIAL=NO son cosméticos para L2. Acción recomendada: corregir/normalizar el término «change in state of delivery» en el pool canónico antes de la fase L2.
