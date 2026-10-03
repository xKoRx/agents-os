# Resumen de auditoría A2 — Capítulo 01 Clutifx, PARTE 2 (w0034–w0066)

Auditor: A2. Ventanas aceptadas auditadas: 24 (w0035–w0066 salvo rechazadas). Nota: w0034 también figura como `rejected` (identity divergence, 0 claims) en el corpus, además de las 8 comunicadas (w0043, w0045, w0049, w0054, w0058, w0059, w0062, w0065); quedó fuera por no tener claims.
Claims auditados: 194. Verificación: claims hablados (INSTRUCTOR_SAID) contra transcript (asr-NNNNN); claims visuales (VIDEO_OBSERVED) contra al menos un frame PNG citado por claim (se leyeron ~35 frames del corpus y 2 frames extraídos con ffmpeg a 510,5s y 512,5s); MODEL_INFERRED contra su evidencia combinada (transcript + frame).

## Tabla por ventana

| Ventana | Claims | CORRECT | PARTIAL | WRONG | OVERGEN | DUP | UNVER | MATERIAL=YES | Missing |
|---|---|---|---|---|---|---|---|---|---|
| w0035 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 6 | NONE |
| w0036 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 9 | NONE |
| w0037 | 6 | 5 | 0 | 1 | 0 | 0 | 0 | 5 | NONE |
| w0038 | 6 | 5 | 0 | 0 | 0 | 1 | 0 | 6 | NONE |
| w0039 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 8 | MISSING_NON_MATERIAL |
| w0040 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 6 | NONE |
| w0041 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 3 | MISSING_NON_MATERIAL |
| w0042 | 9 | 8 | 0 | 0 | 0 | 1 | 0 | 2 | NONE |
| w0044 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 6 | NONE |
| w0046 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 8 | NONE |
| w0047 | 3 | 2 | 0 | 0 | 0 | 1 | 0 | 3 | NONE |
| w0048 | 4 | 3 | 0 | 0 | 0 | 1 | 0 | 2 | NONE |
| w0050 | 9 | 8 | 0 | 0 | 0 | 1 | 0 | 9 | NONE |
| w0051 | 5 | 3 | 0 | 0 | 0 | 2 | 0 | 4 | NONE |
| w0052 | 8 | 7 | 0 | 0 | 0 | 1 | 0 | 7 | NONE |
| w0053 | 13 | 9 | 0 | 0 | 0 | 4 | 0 | 13 | NONE |
| w0055 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 6 | NONE |
| w0056 | 5 | 4 | 0 | 0 | 0 | 1 | 0 | 5 | NONE |
| w0057 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 8 | NONE |
| w0060 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 11 | NONE |
| w0061 | 10 | 7 | 0 | 0 | 0 | 3 | 0 | 10 | NONE |
| w0063 | 9 | 8 | 1 | 0 | 0 | 0 | 0 | 3 | NONE |
| w0064 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 10 | NONE |
| w0066 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 7 | NONE |

## Conteo total

- **194 claims**: CORRECT **176** (90,7%) · PARTIAL **1** (0,5%) · WRONG **1** (0,5%) · OVERGENERALIZED **0** · DUPLICATE **16** (8,2%) · UNVERIFIABLE **0**.
- Materialidad: MATERIAL=YES **158** · MATERIAL=NO **36**.
- Missing: 2 × MISSING_NON_MATERIAL (w0039, w0041). **Ninguna ventana con MISSING_MATERIAL.**

## Hallazgos notables (errores)

### WRONG (1, MATERIAL=YES)

1. **w0037 `cl-objetivo-hoy-rango-bullish-libra`** — "El rango bullish en Libra tenía como objetivo para hoy el nivel 1.37489."
   Al decir «teníamos este objetivo para hoy» (asr-00069) el instructor está dibujando el rango bullish en GBPUSD cuya caja tiene el techo en **1,35843** (frames extraídos a 512,5s y 514s: selección con borde superior 1,35843/1,35841; cierre 1,36028 por encima; «la libra fue directamente hasta su objetivo»). La línea **1,37489** es un nivel preexistente en lo alto del gráfico, ajeno a ese rango. El claim vinculó «este objetivo» con el nivel equivocado (el nivel correcto sí fue extraído en w0038 `cl-objetivo-libra-135843`, etiquetado CORRECT).

### PARTIAL (1, MATERIAL=YES)

- **w0063 `cl-grafico-muestra-rangos-rectangulares`**: en los tres frames citados (p80820000, p81000000, p81360000) solo se aprecia **un** rectángulo delimitando un rango (22-23 jun en EURUSD·8h) más líneas horizontales de niveles (1,15803 / 1,13572); el plural «varios rangos... delimitados por rectángulos» exagera lo visible.

### DUPLICATE (16, 8,2%)

Concentrados en la zona de re-narración y re-observación de etiquetas: re-observaciones del rótulo «RANGO PENDIENTE» (w0050, w0052, w0053, todas contra la primera de w0048), re-extracciones literales de la misma frase en ventanas contiguas (w0038→w0037, w0047→w0046, w0048→w0047, w0051→w0050/w0046, w0052→w0053 en tres casos, w0056→w0055, w0061→w0060/w0061) y la equivalencia interna «a favor = alcista» de w0061 que la propia fuente iguala con «o sea». Ningún duplicado degrada contenido: la primera aparición siempre quedó CORRECT.

## Missing knowledge

- **w0039 MISSING_NON_MATERIAL**: «el precio funciona de esta manera» (asr-00081), coletilla genérica no capturada.
- **w0041 MISSING_NON_MATERIAL**: «para qué van a ser importantes en esta mentoría» (asr-00088), meta-afirmación sobre la relevancia de los rangos.
- Resto: NONE. No se detectó ninguna proposición material de trading (mecánica de rangos pendiente/reiniciado, objetivos, TURTLESOUP/toma de liquidez, cadena de rangos) ausente del L1 local.

## Observaciones de calidad (no afectan etiquetas)

- **ASR «tartel sub» = TURTLESOUP**: el rótulo dibujado en pantalla en 975s/983s (frames p87750000/p88470000) reza «TURTLESOUP»; las claims de w0063/w0064/w0066 conservan la grafía fonética del ASR pero el concepto está correctamente identificado (la normalización a "TURTLESOUP" en w0066 es correcta).
- Niveles de precio verificados en frames: 1,16148 (EURUSD objetivo), 1,35843/1,35841 (techo rango bullish GBPUSD), 1,37489 (línea ajena mal atribuida por w0037), 1,35874, 1,34155, 1,14565/1,15325 (límites rango 8h), 1,15803 y 1,13572 (líneas diarias/4h/8h), 1,15136/1,14413 (caja del ejemplo 15m). Todos coinciden con los rótulos de los frames; sin referencias rotas de evidence_ids en el rango.
- Los claims visuales de transición de temporalidad (15m→1h→4h→1D→12h→8h) y de manipulación de UI (diálogo «Cambiar intervalo», opacidad 83%, selector de color) son MATERIAL=NO y conviven con el contenido material sin desplazarlo; los parámetros de gráfico suponen ~18% de los claims del rango, concentrados en w0042 y w0055.
- Dos claims con `publication: UNSUPPORTED_*` por parseo del reviewer resultaron correctos al auditarlos contra fuente (w0041 `cl-rango-rectangular-vertical`, REVIEW_UNAVAILABLE; w0064 `cl-tartel-sub-toma-de-liquidez`, cuya equivalencia «otros nombres como toma de liquidez» sí es el sentido del transcript).
- Un caso límite resuelto con extracción ffmpeg: el referente de «este objetivo para hoy» (asr-00069), que separó el WRONG de w0037 del CORRECT de w0038.
