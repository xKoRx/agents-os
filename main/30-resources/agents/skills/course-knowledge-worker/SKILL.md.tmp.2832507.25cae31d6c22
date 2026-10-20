---
type: skill
schema_version: 1
name: course-knowledge-worker
description: >
  Contrato operativo para los subagentes ONE-SHOT de course-knowledge-extraction
  (EXTRACTOR, MINUTE_REVIEWER, DOCUMENTATION_VERIFIER). Define paquete de entrada,
  invariantes comunes y contrato de salida de cada rol. La metodología y las
  decisiones canónicas viven en la skill principal; esta skill gobierna sólo el
  comportamiento de los workers. Los workers no editan archivos canónicos: escriben
  resultados a un spool y terminan.
scope: global
created: "2026-10-18"
updated: "2026-10-18"
entities: []
related:
  - "[[course-knowledge-extraction]]"
aliases:
  - worker de extraccion de cursos
load_policy: manual
indexable: true
index_priority: medium
tags:
  - kind/skill
  - scope/global
  - action/extract
  - action/verify
  - domain/knowledge
---

# course-knowledge-worker

## Purpose

Estandarizar el comportamiento de los subagentes que ejecutan un capítulo de
`course-knowledge-extraction`, para que 200 videos no dependan de cómo se
redacte cada subprompt. El Manager (orquestador) pasa: esta skill, el ROLE, los
recursos concretos y el contrato de salida. El worker ejecuta UNA tarea y
termina.

## Common worker contract (los tres modos)

Cada paquete de entrada declara:

```text
task_id, role, source_sha, chapter_id, time_interval
transcript_segments        # los del intervalo UNIÓN los citados por sus claims
available_frames           # rutas reales
glossary_context           # garbles y términos del curso (GLOSSARY.md)
output_contract            # ruta de spool + esquema esperado
```

Invariantes (nunca negociables):

- ONE-SHOT, FRESH CONTEXT: una tarea, sin conversación posterior.
- NO editar archivos canónicos (claims.jsonl, transcript.md, documentación): el
  worker escribe SOLO en su spool. Sólo el integrador aplica cambios.
- NO asignar IDs globales `c-NNNN` (los pone el integrador); usar claves locales.
- NO inventar evidence ids, frames ni contenido; NO crear causalidad no dicha.
- NO marcar SUPPORTED sin respaldo suficiente; NO silenciar contradicciones.
- NO ampliar el alcance (otras ventanas, otros archivos) sin autorización.
- NO convertir la explicación del instructor en verdad universal.
- Frames: nombres SIEMPRE por fórmula desde segundos reales —
  `f-{h:02d}{m:02d}{s:02d}.png` (00:07:16 → `f-000716.png`); jamás concatenar a
  mano. Extraer sólo lo necesario y haberlo VERIFICADO visualmente antes de
  citarlo. Separar `instructor_statement` / `visual_observation` /
  `model_inference`: la inferencia propia no es conocimiento del curso.

## EXTRACTOR mode

Input: transcript de 5–10 min, glosario, contexto cercano, frames si existen.
Output (spool, JSONL): propuestas con `local_source_key`, `minute`, `kind`
(concept|rule|parameter|procedure|observation|example|warning), `statement`
fiel (negaciones, números, condiciones, excepciones), `epistemic`, `evidence`
(s-ids reales del transcript), `visual_hint` opcional `{second, what}` sólo si
lo visual es load-bearing, `unresolved_questions`.

Hard rules: separar correctamente las tres epistemic; no microfragmentar
(~10-25 claims/min denso como techo, menos en pausas); no convertir secuencia
temporal en causalidad (nexo explícito requerido).

## MINUTE_REVIEWER mode

Input: transcript del minuto UNIÓN segmentos citados (frontera incluida),
frame base, frames bajo demanda disponibles, TODOS los claims propuestos del
minuto.
Output (spool, JSON): **exactamente un resultado por claim recibido**:

```json
{"claim_key": "...", "verdict": "SUPPORTED|UNCERTAIN|UNVERIFIED",
 "verified_evidence": ["s-...", "f-..."],
 "reason": "...", "corrections_suggested": "...", "additional_frame_needed": null}
```

Hard rules: no inventar evidencia; no aceptar un frame que no muestre lo
afirmado; no sustituir un id de transcript por texto aproximado; no devolver
menos resultados que claims; todo frame citado debe existir como archivo real
con nombre canónico; toda evidencia que sustente el veredicto va en
`verified_evidence`. Las contradicciones se señalan con razón y referencia
(UNCERTAIN + "CONTRADICTION:"), nunca se disfrazan de duda simple.

El integrador verifica cardinalidad y unicidad (`scripts/validate_review.py`);
si no coincide: `MINUTE_REVIEW = INVALID`, el minuto no se publica como
validado.

## DOCUMENTATION_VERIFIER mode

Input: documentación, claims, transcript relevante, frames relevantes, manifiesto
de recursos.
Output (spool): findings verificables:

```json
{"finding_id": "...", "severity": "MATERIAL|MENOR", "location": "doc §sección",
 "violated_invariant": "...", "evidence": "claim/s-/f-", "expected": "...",
 "observed": "...", "recommended_correction": "..."}
```

Verificar: afirmaciones sin soporte, claims mal citados, imágenes faltantes,
condiciones eliminadas, números cambiados, causalidad inventada, decir más que
el instructor, nombres históricos tratados como vigentes, métricas
contradictorias. NO auto-corregir la biblioteca. NO declarar PASS sin haber
ejecutado las verificaciones.

## Output

Cada worker devuelve su spool y un resumen final de ≤10 líneas (conteos,
clasificaciones, frames creados, cambios propuestos). El integrador:
verifica cardinalidad/unicidad → aplica a los archivos canónicos → ejecuta
`validate_library.py` hasta `PASS`.
