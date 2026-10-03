# Auditoría de aceptación A3 — Capítulo 01 Clutifx, Parte 3/4 (w0067–w0099)

Auditor: A3 (fuente-grounded). Rango: w0067–w0099, 26 ventanas aceptadas (se saltaron las rechazadas w0072, w0074, w0078, w0088, w0092, w0094, w0098). Se auditó el 100% de los claims (190), sin muestreo.

Autoridades usadas: `full-live-v2/transcript.json` (hablado) y los PNG 1920×1080 del corpus en `/home/kor/mke/clutifx-ch01-20260930/media-run/evidence/objects/` (visual). Se leyeron 48 frames; todos los claims VIDEO_OBSERVED fueron juzgados con al menos un frame citado leído. Reglas de materialidad: reglas/observaciones de estrategia y estructura = MATERIAL=YES; lecturas de parámetros de UI de la herramienta de posición, temporalidades, estilo de dibujos y metacomentarios de curso/audiencia = MATERIAL=NO.

## Totales

| Métrica | Valor |
|---|---|
| Claims auditados | 190 |
| CORRECT | 167 |
| DUPLICATE | 23 |
| PARTIAL / WRONG / OVERGENERALIZED / UNVERIFIABLE | 0 / 0 / 0 / 0 |
| MATERIAL=YES | 130 |
| MATERIAL=NO | 60 |
| Ventanas MISSING_MATERIAL | 0 |
| Ventanas MISSING_NON_MATERIAL | 1 (w0073) |
| Ventanas NONE (missing) | 25 |

## Tabla por ventana

| Ventana | Claims | CORRECT | DUPLICATE | Otros | MATERIAL=YES | Missing |
|---|---|---|---|---|---|---|
| w0067 | 7 | 7 | 0 | 0 | 7 | NONE |
| w0068 | 4 | 3 | 1 | 0 | 3 | NONE |
| w0069 | 2 | 2 | 0 | 0 | 1 | NONE |
| w0070 | 14 | 14 | 0 | 0 | 6 | NONE |
| w0071 | 4 | 4 | 0 | 0 | 3 | NONE |
| w0073 | 4 | 4 | 0 | 0 | 4 | MISSING_NON_MATERIAL |
| w0075 | 6 | 6 | 0 | 0 | 6 | NONE |
| w0076 | 10 | 9 | 1 | 0 | 8 | NONE |
| w0077 | 4 | 2 | 2 | 0 | 3 | NONE |
| w0079 | 9 | 9 | 0 | 0 | 5 | NONE |
| w0080 | 7 | 7 | 0 | 0 | 5 | NONE |
| w0081 | 11 | 7 | 4 | 0 | 7 | NONE |
| w0082 | 9 | 7 | 2 | 0 | 3 | NONE |
| w0083 | 6 | 4 | 2 | 0 | 3 | NONE |
| w0084 | 9 | 9 | 0 | 0 | 5 | NONE |
| w0085 | 11 | 10 | 1 | 0 | 5 | NONE |
| w0086 | 8 | 6 | 2 | 0 | 4 | NONE |
| w0087 | 8 | 2 | 6 | 0 | 3 | NONE |
| w0089 | 4 | 4 | 0 | 0 | 2 | NONE |
| w0090 | 7 | 7 | 0 | 0 | 7 | NONE |
| w0091 | 7 | 5 | 2 | 0 | 7 | NONE |
| w0093 | 12 | 12 | 0 | 0 | 11 | NONE |
| w0095 | 6 | 6 | 0 | 0 | 6 | NONE |
| w0096 | 7 | 7 | 0 | 0 | 6 | NONE |
| w0097 | 11 | 11 | 0 | 0 | 8 | NONE |
| w0099 | 3 | 3 | 0 | 0 | 2 | NONE |

## Hallazgos notables

1. **Cero errores materiales.** No hay ningún claim WRONG, PARTIAL ni OVERGENERALIZED. Todas las reglas (Turtle Soup, Intra Turtle Soup, ciclo de vida del rango, SMT clásico vs SMT de estrategia, failure swing) coinciden literalmente con el transcript, y todas las observaciones visuales fueron verificadas contra frames y resultaron exactas (p. ej., parámetros de la herramienta de posición en w0070: Cantidad 1550387, Objetivo 0,00834 (0,73%), PyG 0,01497, R/B 3,23, Stop 0,00258 (0,23%)).

2. **Divergencia fuente speech-vs-pantalla en w0081 (no es un error de claim).** El instructor dice «esto es el euro... y esto es la libra» (asr-00174), pero el panel derecho muestra la etiqueta **XAUUSD · 8h · FOREXCOM** (oro), no GBPUSD. El motor registró ambos hechos como claims separados y correctly etiquetados (`cl-grafico-derecho-libra` INSTRUCTOR_SAID, fiel al habla; `cl-grafico-derecho-xauusd` VIDEO_OBSERVED, fiel a pantalla). Recomendación: revisar a nivel de producto si la identidad «libra» debe validarse contra la etiqueta del gráfico.

3. **Garbles de ASR heredados a claims, fielmente reproducidos:** «S&T» por SMT (w0097, `cl-caso-st-actual`, `cl-casos-st-no-visibles-simple-vista`), «DXI» por DXY (w0085), «JP» por JPY (w0091), «GIP» por GBP (w0095), «Muchos venís a SMT» (w0083, probablemente «venís de»). Al juzgar solo contra la fuente son CORRECT; para el producto canónico (L2) convendría normalizar estos términos.

4. **Duplicación cross-window (23 DUPLICATE).** Concentrada en las reapariciones del texto: la regla «cierra fuera → ya no es rango» se re-extrae en w0076 y w0077 tras introducirse en w0075; los metacomentarios del curso SMT se repiten en w0082/w0083 (curso intermedio, audiencia), w0085–w0087 (capítulo aparte, zonas euro/libra, temporalidad 8h, posible SMT) y w0091 (datos ocultos, no visible sin estrategia). Todas marcadas DUPLICATE solo cuando la proposición es idéntica; las variantes con contenido distinto (p. ej., «inválido» vs «eliminable» en w0075) se mantienen CORRECT.

5. **Claims deícticos de baja densidad.** Varias observaciones tipo «esto», «aquí» (w0079 objetivo ya no aquí/este, w0093 rango de libra «así», w0069 «aquí abajo») son CORRECT pero MATERIAL=NO; el contenido material equivalente está capturado en claims de regla/procedimiento de la misma ventana.

6. **Evidencia con anomalías menores (sin impacto en etiquetas):** `cl-temporalidad-grafico-8h` (w0082) cita además el frame p134640000, que pertenece temporalmente a w0097 (24:56); el claim sigue verificado por dos frames de su propia ventana. En w0085, `cl-smt-forma-posible-esquema` cita frames donde el nuevo esquema solo está iniciándose (una línea descendente); el claim es hablado y fiel, y el esquema completo aparece en frames de w0086.

## Missing knowledge

- **MISSING_MATERIAL: ninguna ventana.**
- **MISSING_NON_MATERIAL: w0073** — el matiz de frecuencia «¿pasa muchas veces? No. Algunas veces pasa» (asr-00155) sobre el rango contrario en 4H no está en el L1; es secundario y el carácter ocasional del fenómeno análogo ya está en w0070 («a veces»).
- Resto (25 ventanas): NONE. El L1 cubre el contenido material hablado y mostrado de cada ventana.

## Veredicto

La Parte 3 (w0067–w0099) del L1 **aprueba la auditoría de aceptación**: 190/190 claims juzgados, 0 errores materiales, cobertura de contenido material completa salvo un matiz no material en w0073. Los únicos puntos de mejora son la normalización de garbles de ASR y la gestión de la divergencia speech/pantalla del par correlacionado del ejemplo SMT.
