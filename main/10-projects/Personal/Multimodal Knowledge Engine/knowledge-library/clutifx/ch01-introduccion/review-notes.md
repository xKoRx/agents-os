# ch01-introduccion — Notas de revisión (run V1.2 2026-10-22)

Notas operativas del run de reconstrucción V1.2 (run dir `/home/kor/mke/clutifx-ch01-v12-20261022/`). El reporting distingue lo medido de lo estimado.

## Flujo y throughput

| Fase | Valor |
|---|---|
| ASR | **REUTILIZADO** del run MKE V2 original (`clutifx-ch01-agent-20261015/transcript.json`, schema `mke.transcript.v1`, 323 segmentos): identidad verificada por `source_sha256` = SHA del ep01 (`4de8f12d…`), tiempos monótonos sin solapamientos, cobertura 5,8 s → 2033,2 s con la despedida incluida, 0 segmentos vacíos. Sin re-ejecutar Whisper (contrato B2: no relanzar ASR si el transcript existente es válido). 0 min de ASR. |
| Frames base | 35 (fin de minuto por fórmula + fin real del video f-003403) extraídos con ffmpeg por el Manager, con manifiesto `frames/.base_frames` (stems sin `.png`). |
| Extracción | 6 EXTRACTORs **SECUENCIALES** (bloques 0–6–12–18–24–30–34:04), 132 claims, ~34 min de wall de workers (~61 min/h-video). |
| Revisión | 35 payloads con contexto de frontera (`make_minute_payload.py`); **34 MINUTE_REVIEWERs** (minutos 0–33; el 34 no tiene claims), olas de 5 con 0–2 muertes [1210] por ola, todas recuperadas con retry completo del minuto (protocolo ch08). makespan por ola 3–10 min. |
| Integración | `integrate_reviews.py` 132/132 aplicados, 0 inválidos, cobertura completa (dry-run previo PASS). IDs `c-0001..c-0132` asignados post-integración (patrón ch10). |
| Checkpoint | Tras extracción completa + revisión de minutos 0–4: extracción ≈61 min/h-video, revisión ≈120 min/h-video (olas de 5) → proyección ~200 min/h-video, <2× objetivo; continuado con registro (mismo criterio que ch04–ch12). |

## Incidentes y correcciones

1. **[1210] "Invalid API parameter"**: 6 muertes de worker (min06, min08, min13, min19, min23, min28, min30 — el 30 murió 2 veces), todas TRANSITORIAS y recuperadas con retry completo del minuto; 0 pérdida de datos. Coincide con el patrón ch08–ch12.
2. **Naming de frames por segundos crudos (4ª recurrencia, cazada por el Manager)**: 7 frames de 3 revisores (min04 ×2, min09, min10, min32 ×3) usaron el segundo crudo como HHMMSS (p.ej. el segundo 241 escrito como HHMMSS crudo en vez de por fórmula). Detección: chequeo decode(distancia del minuto) post-olas. Adjudicación con **sonda byte-idéntica** (lección ch12: la sonda prueba el INSTANTE): extracción ffmpeg fresca al segundo declarado → 7/7 idénticas → renombrados por fórmula + reviews re-normalizados. Lección reforzada: generar SIEMPRE las rutas del pack por código; el revisor no debe escribir nombres a mano.
3. **Formatos heterogéneos de `verified_evidence`** en los reviewers (ids desnudos, dicts `{segment,timestamp,quote}`, strings en prosa con varios ids): el normalizador del Manager (no canónico) los unificó a ids desnuros para `validate_review.py`. Defecto de paquete, no de contrato: los prompts no fijaron el formato de la lista de evidencia.
4. **`.base_frames` con sufijo `.png`**: el renderer falla cerrado esperando stems (correcto); corregido el manifiesto.
5. **Residuo estilo frame-final mal nombrado (cf. ch10)**: aquí no ocurrió; el frame final se nombró por fórmula (f-003403) desde el principio (lección ch10 #1 aplicada en el setup del Manager).

## Veredictos y honestidad epistémica

- 132/132 SUPPORTED, 0 UNCERTAIN, 0 UNVERIFIED: capítulo introductorio sin contradicciones internas; las dudas (garbles, deícticos, ambigüedades) viven como **78 unresolved_questions** agrupadas en 15 q-ch01-* ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/OPEN-QUESTIONS|OPEN-QUESTIONS]]), 4 de ellas RESOLVED con evidencia adjudicada.
- Adjudicaciones del Manager post-review (13 notas + 7 adds de evidencia + 3 visual_hints re-fijados) en `<run>/evidence-adjudications.json`; **ninguna reescritura de statement** (contrato SOURCE-FIRST).
- Epistemic final: 114 instructor_statement + 18 visual_observation, 0 model_inference.

## Cobertura conceptual (mandato B4)

Los 7 conceptos de la documentación legacy verificados contra el vídeo: rango y criterio de formación (c-0005), pendiente/reiniciado con dirección (c-0041..c-0055), Turtle Soup + intra (c-0058..c-0075), SMT clásica y dos tipos (c-0081..c-0097), failure swing + 3 casos + "rango por creado" (c-0098..c-0103), order block definición ≠ uso (c-0105..c-0113), Power of 3 con horarios (c-0115..c-0130). Diferencias críticas preservadas: tomar high/low ≠ cerrar dentro/fuera; negación "no todos se completan"; DOL vs DXY (garbles preservados); SMT clásica ≠ SMT de rangos; failure swing ≠ caso normal; horarios del P3; promesas del instructor registradas como declaraciones, no garantías.

## Incidente de frames durante la publicación (2026-10-22 18:5x)

6 frames bajo demanda citados (f-001145, f-001801, f-002751, f-002830, f-002855, f-002915) desaparecieron del directorio frames/ entre dos lecturas separadas por ~1 minuto (presentes en un listado, ausentes en el validador inmediato), **sin commit de borrado en git** (el autosync de la ventana no los registró: se borraron antes del tick). Los 5 con copia en spool se repusieron con `cp -p`; f-002915 se re-extrajo fresco del video (1755 s, mismos parámetros) y persistió. El patrón es consistente con la reconciliación en reversa del mismo mecanismo LiveSync identificado en FRAME-RECONCILIATION-2026-10-22.md (propaga estado de su DB, esta vez borrados). Tras la reposición: 5/5 persistieron >75 s y el validador pasó 0 findings. Monitoreo de persistencia delegado al gate final de la misión.
