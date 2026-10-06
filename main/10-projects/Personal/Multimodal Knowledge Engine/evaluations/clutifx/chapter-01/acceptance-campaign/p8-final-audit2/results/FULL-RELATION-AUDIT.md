# FULL RELATION AUDIT — P8 final · MKE V2 Clutifx Ch01 · run P7b (`e7bc387`)

- **Auditor:** relations-auditor, one-shot, sesión fresca. Fecha: 2026-10-05.
- **Alcance:** las 104 `claim_relation` del candidato (header de `claims.jsonl`: `relation_count: 104`). Sin muestreo: 104/104 auditadas.
- **Entradas:** `/home/kor/mke/clutifx-ch01-rerun2-20261004/run-rerun2/claims.jsonl`; corpus por ventana `p8-final-audit2/corpus/wNNNN.json` (transcript + frames); mapeo `coverage.json` (`records_introduced`).
- **Verificación de fuente:** transcript completo (`asr-00001`–`asr-00200`) y **12 frames visualizados directamente** (p9360000, p9720000, p45180000, p45270000, p45360000, p46170000, p60480000, p64800000, p105390000, p108630000, p112320000/1, p18990000/1).
- **Detalle fila a fila:** `FULL-RELATION-AUDIT.jsonl` (104 filas).

## 1. Distribución de veredictos

| Label | n | % |
|---|---|---|
| CORRECT | 99 | 95.2% |
| UNSUPPORTED | 2 | 1.9% |
| WRONG_TYPE | 2 | 1.9% |
| WRONG_ENDPOINT | 1 | 1.0% |

Por tipo: `DEPENDS_ON` 91 (88 CORRECT), `EXCEPTION_TO` 6 (6 CORRECT), `CONTRADICTS` 4 (4 CORRECT), `EQUIVALENT_TO` 3 (**solo 1 CORRECT**, 2 WRONG_TYPE).
Por epistemic: `INSTRUCTOR_SAID` 96, `VIDEO_OBSERVED` 6 (6 CORRECT, frames verificados), `MODEL_INFERRED` 2 (2 CORRECT).

### Matriz decisión del reviewer × veredicto del auditor

| Decisión del run | CORRECT | No-CORRECT | Total |
|---|---|---|---|
| Publicada (`SUPPORTED_BY_AUTOMATED_REVIEW`) | 78 | **4 (FP)** | 82 |
| Rechazada (`UNSUPPORTED_INSUFFICIENT`) | **16 (FN)** | 1 (TN) | 17 |
| `UNSUPPORTED_REVIEW_UNAVAILABLE` | 5 | 0 | 5 |

- **Precisión de lo aceptado (safety): 78/82 = 95.1%.**
- **Justificación de los rechazos: 1/17 = 5.9%** (16 de 17 rechazos son falsos negativos).
- Las 5 relaciones bloqueadas por caída del reviewer son las 5 CORRECT (pérdida 100% evitable).

## 2. Old vs new (P7 `19b44c1` → P7b `e7bc387`, reviewer v3)

| Métrica | P7 (19b44c1) | P7b (e7bc387) | Δ |
|---|---|---|---|
| Relations totales | 146 | 104 | −29% |
| Rechazadas | 18 (12.3%) | **17 (16.3%)** | **sube** |
| Rechazos = FN | 11/18 (61%) | **16/17 (94%)** | **empeora** |
| Precisión al aceptar | 128/128 (100%) | **78/82 (95.1%)** | **baja (nuevos FP)** |
| Relations CORRECT totales | 139/146 (95.2%) | 99/104 (95.2%) | = |

**Respuestas a las dos preguntas del encargo:**
1. **¿Bajaron los rechazos de relaciones?** No. En absoluto se mantienen (17 vs 18) y la tasa de rechazo sube (12.3% → 16.3%) sobre un conjunto un 29% menor. La calibración v3 **no recuperó los 8 FN causales**: siguen rechazadas `rel-formacion-bajista-depende-cierre`, `rel-no-turtle-soup-depende-de-no-reaccion`, `rel-no-turtlesoup-depende-bajista`, `rel-continuacion-cierra-fuera`, `rel-smt-superior-depande-eur-objetivos`, `rel-toma-low-requiere-apertura`, más la familia causal afín (condiciones de formación, cadena eliminar→reanalizar, dependencia definicional→instancia). Solo 1 rechazo de 17 está bien fundado.
2. **¿Aparecen falsos positivos nuevos?** Sí — **4 FP (P7 tuvo 0)**. Es la regresión relevante de esta rama: el reviewer ahora acepta relaciones que antes no habría publicado (2× EQUIVALENT_TO indebido, 1 endpoint invertido, 1 yuxtaposición).

## 3. Falsos negativos (16): relaciones CORRECT rechazadas

Grupo A — **causales/condicionales** (los FN que v3 debía recuperar):
`rel-formacion-bajista-depende-cierre` (asr-00106 «si… cierra adentro… se está formando un rango bajista»), `rel-continuacion-cierra-fuera` (asr-00063/64), `rel-no-turtle-soup-depende-de-no-reaccion` y `rel-no-turtlesoup-depende-bajista` (asr-00130/31), `rel-eliminacion-rango-requiere-invalidez` (asr-00161/62), `rel-smt-superior-depande-eur-objetivos` (asr-00196), `rel-toma-low-requiere-apertura` (asr-00169), `rel-falso-turtle-soup-depende-de-reaccion-real` (asr-00131-33, MODEL_INFERRED).

Grupo B — **deixis-anáfora / dependencia-enunciada** (blanco declarado de la calibración v3):
`rel-llegada-directa-definida-por-objetivo` («este objetivo para hoy» ≡ borde 1,35843; **frame p46170000 verificado**), `rel-borde-superior-bearish-depends-rango` (**frame p45270000 verificado**: 3.394,75 borde superior de la caja bearish), `rel-bullish-range-depends-on-timeframes` («todo esto basado en las temporalidades»), `rel-busqueda-rango-usa-temporal-12h` («que ya recuerdo que lo tenemos en 12 horas»), `rel-pendiente-8h-continua-pendiente-12h` («es este, pendiente también»), `rel-reanalizacion-tras-eliminacion`, `rel-reanalizacion-tras-olvido` (asr-00173), `rel-bearish-completion-depends-on-formation` («forma uno bearish, completa el bearish»).

**Evidencia de inconsistencia interna del reviewer v3** (mismo contenido, decisiones opuestas):
| Aceptada | Rechazada (gemela) | Evidencia común |
|---|---|---|
| `rel-toma-low-tras-apertura-nueva-vela` (w0078) | `rel-toma-low-requiere-apertura` (w0079) | asr-00169 |
| `rel-bearish-completion-depends-on-timeframes` (w0040) | `rel-bullish-range-depends-on-timeframes` (w0040) | asr-00083/84 |
| `rel-busqueda-objetivo-tras-reanalisis` (w0080) | `rel-reanalizacion-tras-eliminacion/olvido` (w0080) | asr-00173 |
| `rel-formacion-bajista-depende-apertura/-high` (w0050) | `rel-formacion-bajista-depende-cierre` (w0050) | asr-00105/06 |
| `rel-reiniciado-referente-rango-12h` (w0057) | `rel-busqueda-rango-usa-temporal-12h` (w0057) | asr-00114 |
| `rel-continuacion-sin-rango` (w0036) | `rel-continuacion-cierra-fuera` (w0036) | asr-00063/64 |
| `rel-borde-inferior-bearish-depends-rango` (w0037) | `rel-borde-superior-bearish-depends-rango` (w0037) | asr-00068 + frame p45270000 |
| `rel-copia-depende-seleccion-velas` (w0048, aceptada = FP) | `rel-copia-depende-seleccion-d` (w0048, rechazada = correcto) | asr-00104 + frame p60480000 |

Único rechazo justificado: `rel-copia-depende-seleccion-d` (yuxtaposición sin dependencia; TN).

## 4. Falsos positivos (4): publicadas y no correctas (safety)

1. **`rel-copia-depende-seleccion-velas` — UNSUPPORTED.** «Podemos copiar la selección» no depende de «tres velas blancas seleccionadas»: observaciones coordinadas del mismo estado de pantalla. Gemelo aceptado del único rechazo correcto del run.
2. **`rel-cierre-fuera-rango-candidato` — WRONG_ENDPOINT (orientación invertida).** La dependencia enactada corre del candidato de nuevo rango hacia el cierre fuera (asr-00163/165: el rango viejo se elimina *porque* la vela cierra fuera y *entonces* surge el candidato); el run invierte subject/object bajo la convención subject DEPENDS_ON object.
3. **`rel-rango-reiniciado-rango-pendiente` — WRONG_TYPE.** EQUIVALENT_TO entre «se denominará reiniciado» y «aparece etiquetado RANGO PENDIENTE» (frame p64800000): el video introduce «reiniciado» como caso **distinto/contrastante** del pendiente; es reclasificación, no sinonimia (CONTRADICTS o reetiquetado sería lo propio).
4. **`rel-toma-liquidez-equivalente-tartel-sub` — WRONG_TYPE.** EQUIVALENT_TO entre un alias (metalingüístico, asr-00128) y una definición funcional (asr-00124): enunciados no equivalentes. Con estos endpoints cabía DEPENDS_ON; para EQUIVALENT_TO existía el endpoint correcto (`cl-turtle-soup-requiere-toma-liquidez`, asr-00131). Nota: en el run hay dos claims duplicados con ese mismo enunciado (`cl-turtle-soup-requiere-toma-liquidez` / `cl-turtlesoup-toma-liquidez`), lo que delata falta de dedup aguas arriba.

Además: `rel-correccion-clasificacion-turtle-soup` (CONTRADICTS) y `rel-closes-outside-exception` son CORRECT aunque funcionalmente duplican `rel-not-always-contradicts-always`-style pares de w0075/w0076 y w0029/w0030 — sin coste de precisión, pero sugieren revisitación de la política de duplicados entre ventanas contiguas.

## 5. Relations bloqueadas por caída de reviewer (5) — todas CORRECT

`rel-no-turtlesoup-depende-no-reaccion`, `rel-objetivo-tras-nuevo-rango` (frame p108630000 verificado: objetivo 1,13871), `rel-rango-alcista-depende-condicion`, `rel-rango-alcista-depende-de-vela-baja` (asr-00028, «porque» explícito; frames verificados), `rel-rango-bajista-completa-tras-formarse`. Publicación perdida por `REVIEW_UNAVAILABLE` con evidencia suficiente en los 5 casos.

## FEEDBACK (Agents-OS)

1. **La calibración v3 de la rama relations NO recuperó los 8 FN causales**: 16/17 rechazos siguen siendo FN (94%, peor que el 61% de P7) y la tasa de rechazo sube. El patrón de fallo no es de criterio sino de **consistencia intra-run**: 8 pares gemelos recibieron decisiones opuestas con la misma evidencia (tabla §3). Recomendación: reglas de decisión deterministas y auditables — aceptar DEPENDS_ON ante (a) conectores explícitos (`porque`, `si`, `por lo tanto`, `pues`, subordinadas justificativas «que ya recuerdo…»), (b) anáfora/deixis resoluble en transcript o frame («todo esto», «este objetivo», «una vez pasa esto», «pendiente también»), (c) secuencias presuposicionales enactadas (forma→completa, abre→toma low, copia→mueve, elimina→reanaliza) — y añadir un paso de **chequeo de consistencia entre relations casi-duplicadas** (misma evidencia/ventana contigua) antes de fijar veredictos.
2. **Nueva inestabilidad en EQUIVALENT_TO (2/3 mal usadas)** — es la fuente principal de los FP nuevos. Recomendación: restringir EQUIVALENT_TO a pares de enunciados con el mismo contenido proposicional; enrutar alias/etiquetas a DEPENDS_ON (alias←definición) o CONTRADICTS (reetiquetado), exigiendo que el endpoint del alias sea el claim nominativo correspondiente si existe.
3. **Chequeo de orientación de endpoints**: al menos 1 relación publicada con subject/object intercambiados (`rel-cierre-fuera-rango-candidato`). Un validador barato (la evidencia del object no debe preceder-temporalmente a la del subject en cadenas «condición→consecuencia») lo habría cazado.
4. **`REVIEW_UNAVAILABLE` bloquea 5 relations CORRECT** (4.8% del total) por timeout del proveedor VLM. Recomendación: cola de reintento para relations pendientes antes del cierre del run; con la evidencia citada, las 5 habrían salido SUPPORTED.
5. **Dedup de claims antes del pase de relations**: el par duplicado `cl-turtle-soup-requiere-toma-liquidez` / `cl-turtlesoup-toma-liquidez` (enunciado idéntico) introduce ambigüedad de endpoints y contribuyó al error de tipo §4.4.
6. Nota de proceso de auditoría: los frames del corpus (`media-run/evidence/objects/*.png`) están accesibles y permiten verificación directa — las 6 relations VIDEO_OBSERVED aceptadas y las 2 con frame rechazadas se verificaron visualmente sin ambigüedad (3.394,75/3.388,10 y 1,35843/1,34155 legibles en los bordes de las cajas dibujadas).

---

*Fila a fila: `FULL-RELATION-AUDIT.jsonl` (104 registros: relation_id, endpoints, tipo, label, evidencia chequeada, cita de fuente, justificación).*
