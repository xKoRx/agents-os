# P8 Final Audit — A2 (ventanas w0034–w0066, run candidato rerun @ 19b44c1)

Auditoría fuente-grounded, sin muestreo, de la población COMPLETA de claims del candidato en las
ventanas w0034–w0066. Ventanas rechazadas excluidas según REJECTED-WINDOWS.json: **w0035, w0054,
w0058, w0066** (las cubre otro worker). Ventanas aceptadas auditadas: **29**.

## Alcance y método
- 282 claims auditados (uno a uno), contra transcript textual del corpus y, para claims visuales
  (niveles, colores, rectángulos, velas, etiquetas de UI, instrumento/temporalidad), lectura directa
  de los frames PNG citados: **~75 frames abiertos** en cobertura por clúster (al menos un frame
  leído por clúster visual; niveles finos verificados en el frame específico).
- Cada claim emitió una fila en `FULL-CLAIM-AUDIT-A2.jsonl` (claim_id, window, kind normalizado a
  observation|parameter|claim, epistemic, label, material, evidence_checked, source_quote, justification).

## Distribución de labels (n=282)
| Label | n |
|---|---|
| CORRECT | 253 |
| DUPLICATE | 21 |
| WRONG | 6 |
| PARTIAL | 2 |
| OVERGENERALIZED | 0 |
| UNVERIFIABLE_FROM_AVAILABLE_EVIDENCE | 0 |

**Precisión material parcial (CORRECT+DUPLICATE sobre MATERIAL=YES): 139/144 = 96.5 %.**

### WRONG (6)
| Window | Claim_id | Material | Motivo |
|---|---|---|---|
| w0037 | cl-gbpusd-today-target-137489 | **YES** | «Objetivo de hoy = 1,37489»: la línea 1.37489 existe dibujada, pero el objetivo que el transcript dice alcanzado («ir directamente hasta su objetivo», «llegó») es la zona 1,35843/1,36031 (máx. del día 1,36035). Lectura visual fina incorrecta. |
| w0059 | cl-limites-rango-mostrado | **YES** | Límites reales ≈1,15214/1,14565 (frames p76140000/p76320000); el statement da 1,15231 (etiqueta de rejilla) y 1,14650. |
| w0061 | cl-rango-borde-superior-1-15325 | **YES** | 1,15325 fue valor transitorio del ajuste (p78930000); el rango final (p79110000) queda con borde superior ≈1,15231. |
| w0063 | cl-nivel-horizontal-1-15728 | **YES** | La línea horizontal está etiquetada 1,15803; 1,15728 es una marca azul de la escala, no la etiqueta de la línea. |
| w0046 | cl-segunda-vela-seleccionada | NO | La vela seleccionada con tiradores es la primera vela blanca visible, no la segunda. |
| w0063 | cl-fuente-cambia-a-oanda | NO | Ambos frames citados muestran FOREX.com; no hay OANDA. |

### PARTIAL (2)
- w0042 cl-color-linea-azul (NO material): línea confirmada; el color «azul» no verificable en el frame citado (se percibe oscura).
- w0057 cl-limite-superior-rango-115803 (YES material): la línea 1.15803 es real en 12h pero es el objetivo diario previo; los frames no establecen que sea el «borde superior del rango de 12h» (el rango pendiente 12h dibujado en w0059 tiene tope ≈1,15214).

## MISSING-KNOWLEDGE (4 filas; 1 MATERIAL, 3 NON_MATERIAL)
Archivo: `MISSING-KNOWLEDGE-A2.jsonl`
- **w0036 MISSING_MATERIAL**: referencia forward a SMT («ya lo vais a ver en el tema de la SMT», asr-00067) que vincula los rangos bearish de Libra con la divergencia SMT; no existe record que capture ese vínculo.
- w0039 MISSING_NON_MATERIAL: «llegó antes de que pudiésemos entrar en la sesión» (narrativa del caso).
- w0041 MISSING_NON_MATERIAL: «para qué van a ser importantes en esta mentoría» (meta del curso).
- w0042 MISSING_NON_MATERIAL: «esto ya vamos a llegar más adelante» (referencia forward pedagógica).

Conteo por ventana sin omisiones materiales: 28 de 29 ventanas aceptadas sin MISSING_MATERIAL.

## REGRESSION WATCH (obligatorio)
Claim del run viejo (@ ef53530): `cl-objetivo-hoy-rango-bullish-libra` (w0037, objetivo 1.37489 vs 1.35843 dibujado — lectura visual fina de nivel).

**Veredicto: STILL_WRONG.**

- El candidato re-emite la misma proposición errónea como `cl-gbpusd-today-target-137489` (w0037): «El objetivo de hoy del rango bullish de GBPUSD está en 1,37489», con GROUNDING_SUPPORTED del propio run.
- Evidencia (frames leídos p46080000 y p46170000, GBPUSD·1D): SÍ existe una línea horizontal etiquetada **1,37489** en la parte alta del gráfico, y el rango dibujado queda en **1,34155–1,35843**; el cierre del día mostrado (24/6/2025) es **1,36031** (máximo 1,36035). El transcript (asr-00069/00072/00073 y asr-00076) dice que el objetivo de hoy **fue alcanzado** («ha hecho a la libra ir directamente hasta su objetivo», «llegó»), algo imposible con 1.37489. Por tanto la identificación del «objetivo de hoy» con 1.37489 sigue siendo un error de nivel fino.
- Matiz: el conocimiento correcto SÍ está representado en otros records del candidato — `cl-gbpusd-objetivo-hoy-136031` (w0038, objetivo de hoy = 1,36031, verificado contra frame p46710000 y los ejes de p46980000 donde 1,36031 es línea+close) y `cl-gbpusd-bullish-range-upper-135843` (w0037/w0038, borde superior 1,35843 verificado). Es decir, hay recuperación parcial del conocimiento en otros records, pero el record erróneo permanece canónico y coexiste con el correcto, creando contradicción interna (dos «objetivo de hoy» distintos en w0037 y w0038). No se acepta «borrado» como fix; aquí ni siquiera fue borrado.
- Los otros 3 WRONG materiales (w0059 límites del rango, w0061 borde superior final, w0063 nivel 1.15728) son lecturas finas nuevas; en los tres casos el propio candidato los marcó GROUNDING_CONTRADICTED (autodetección funcionando), pero siguen publicados como records WRONG.

## Hallazgos notables
1. **Duplicación sistemática intra-run**: 21 DUPLICATE, incluyendo 8 pares exactos dentro del rango (w0045↔w0046 con 5 pares; w0052↔w0053; w0055↔w0056; w0050↔w0057; w0061↔w0062 con 3 pares; w0062↔w0063 con 2 pares; w0043↔w0062) y duplicados contra ventanas fuera de rango (w0002, w0021, w0022, w0067). El segmento asr-00101/00119, que abarca varias ventanas, genera la misma proposición en cada ventana que toca.
2. **Evidencia fuera de ventana**: varios claims citan frames de minutos o decenas de minutos después (p. ej. `cl-marco-temporal-15m` en w0047 cita un frame de 30:42; `cl-instrument-eurusd` en w0062 cita 6 frames de 17:00-29:52; `cl-symbol-search-opened` en w0036 cita un frame de 25:40). El contenido suele ser correcto, pero la práctica debilita la trazabilidad local.
3. **Autodetección de contradicciones funciona a medias**: los 4 errores de nivel fino WRONG ya estaban marcados GROUNDING_CONTRADICTED/INSUFFICIENT por el revisor del candidato, pero se publican igualmente; en cambio el error del objetivo 1.37489 (w0037) pasó el review como GROUNDING_SUPPORTED — el review automático no resolvió la deíxis «este objetivo para hoy».
4. **Grounding conservador correcto en contenido**: 4 claims marcados INSUFFICIENT por el candidato resultaron CORRECTOS al verificarlos contra frames/transcript (fecha 24/6/2025 en w0042, vela blanca seleccionada en w0049, «completa el bearish» en w0040, alias «toma de liquidez» en w0064); 1 INSUFFICIENT era además duplicado (w0046).
5. Cobertura de conceptos del bloque muy buena: tipos de rango (pendiente/reiniciado), reglas de formación (toma low/high + cierre adentro), tartel sub y alias, cadena de rangos, y los niveles clave (1.34155/1.35843/1.36031/1.15803/1.15214/1.14565) están capturados y verificados.

## Conteos clave
- Claims auditados: **282** (29 ventanas aceptadas; 4 rechazadas excluidas).
- Labels: CORRECT 253 · DUPLICATE 21 · WRONG 6 · PARTIAL 2.
- Material precision parcial: **139/144 = 96.5 %** (CORRECT+DUPLICATE sobre MATERIAL=YES).
- WRONG material: **4** (w0037, w0059, w0061, w0063) · WRONG no-material: 2 · PARTIAL material: 1.
- MISSING_MATERIAL: **1** (w0036, SMT) · MISSING_NON_MATERIAL: 3.

## FEEDBACK (Agents-OS)
- Fricción principal: el patrón «ventanas que comparten un segmento ASR largo» produce duplicados multi-ventana que el store no deduplica (21 en solo 33 ventanas); convendría una regla de dedup por proposición a nivel de segmento compartido, o marcar la ventana canónica.
- El corpus por ventana (formato P1) y el digest de frames funcionaron muy bien; los paths absolutos de frames en `corpus.frames` permitieron verificación directa sin cazar rutas.
- Gap: `grounding.status` y el veredicto de fuente a veces divergen en ambas direcciones (INSUFFICIENT correctos; SUPPORTED erróneo en deíxis «este objetivo»). Sugerencia: cuando la evidencia clave es deíctica («este», «aquí arriba»), exigir frame citado como evidencia primaria, no solo ASR.
- Gap menor: claims con evidencia de frames fuera de la ventana (minutos después) no generan ningún warning; un check de `frame.pts_ms ∈ [start_ms, end_ms + margen]` sería barato y útil.
- Sin problemas de herramientas ni de permisos en la corrida; el único coste fue el volumen de lecturas de PNG (~75), mitigado agrupando por clúster visual.
