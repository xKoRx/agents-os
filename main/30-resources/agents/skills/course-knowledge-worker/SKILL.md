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
  resultados a un spool y terminan. v1.2: reviewer entrega unresolved_questions,
  modalidad targeted para aclaraciones puntuales y verificación de navegación.
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
- El transcript llega con segmentos ya direccionables (anchor `^s-` por segmento,
  cada uno bloque Obsidian independiente); los workers CITAN ids `s-`, jamás
  reescriben ni re-anchorean transcript.
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
lo visual es load-bearing — `second` es SIEMPRE segundos reales del video por
fórmula desde el timestamp (16:35 → 995), JAMÁS HHMMSS pegado (defecto real
ch05, cazado por V08) —, `unresolved_questions`.

Hard rules: separar correctamente las tres epistemic; no microfragmentar
(~10-25 claims/min denso como techo, menos en pausas); no convertir secuencia
temporal en causalidad (nexo explícito requerido). **Términos especializados**:
si un garble del ASR admite dos términos con significados distintos
(TERM_DISAMBIGUATION_REQUIRED, p.ej. "el doble" → DOL objetivo vs DXY índice),
preserva la PALABRA DICHA en el statement (marca `[ASR]`), anota los candidatos
en notes/unresolved_questions y NUNCA sustituyas por el término del glosario:
el glosario es contexto, no permiso de normalización.

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
`verified_evidence`. **Normalizaciones de términos**: contrasta el término
publicado en el statement contra el segmento citado y los frames — que el
glosario liste una equivalencia NO la respalda; si la fuente dice otra palabra
o el referente es ambiguo, corrige (`corrections_suggested` con el texto
literal) o marca UNCERTAIN. Cada resultado incluye `unresolved_questions` (deícticos,
datos visuales no resueltos, dudas concretas — vacío si no hay). Las
contradicciones se señalan con razón y referencia (UNCERTAIN +
"CONTRADICTION:"), nunca se disfrazan de duda simple.

**Modalidad targeted**: para aclaraciones puntuales (post-publicación), el mismo
contrato de MINUTE_REVIEWER con UN claim o un conjunto pequeño explícito del
Manager — sin recrear la revisión del capítulo ni crear una skill nueva. La
salida alimenta AMENDMENTS/OPEN-QUESTIONS en manos del integrador.

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
contradictorias, **lifecycle de supersession** (un claim con `superseded_by`
es historia, no conocimiento vigente: los docs pedagógicos no pueden
wikilinkearlo como evidencia — ACTIVE KNOWLEDGE = claims sin `superseded_by`),
e **integridad de navegación** (wikilinks a archivos,
headings y block ids reales; CLAIMS.md/FRAMES.md sincronizadas con
claims.jsonl; sin enlaces ambiguos entre capítulos). **Chequeo SOURCE-FIRST
semántico (obligatorio)**: para claims con términos especializados normalizados
o glosas de interpretación, abrir la EVIDENCIA ORIGINAL citada (segmento de
transcript, frame) y contrastar el término publicado contra el término
realmente dicho/escrito — que documentation.md concuerde con claims.jsonl NO
basta, porque ambos pueden contener el mismo error (defecto real ch03:
"al DOL" publicado como "al DXY"). Ejecutar también
`scripts/check_term_sources.py <lib>`. **Chequeo de ambigüedades resueltas
(obligatorio; regresión ch09 DV09-001, 2026-10-21): una síntesis no puede
resolver categóricamente una ambigüedad material que el claim citado mantiene
abierta, salvo que aporte evidencia adicional adjudicada.** Cuando el claim
publica un garble con marca [ASR], un TERM_DISAMBIGUATION_REQUIRED o una
q-\<curso\>-NNN OPEN, la documentación que lo cita debe preservar la duda
(palabra dicha + interpretación como candidata no confirmada + referencia a la
pregunta abierta); sustituirla por la lectura «natural» o por la práctica
habitual del dominio es hallazgo MATERIAL. Caso real: la documentation de ch09
publicaba «mover el stop a break even» citando c-0015, cuyo statement
preservaba «mover tu tarjeta breakable» [ASR] con q-ch09-002 OPEN — y el
DOCVERIFY que lo detectó lo registró como corregido sin que el fix llegara al
árbol publicado: auditar el árbol físico final, no el registro de intenciones.
No es un detector regex ni una ontología: exige contrastar cada cita de una
duda abierta contra su claim. **Vínculo estructural de dudas materiales**
(hardening 2026-10-23, defecto real q-ch07-019): una q-\<curso\>-NNN OPEN con
`**Materialidad: MATERIAL**` debe estar referenciada en el
`unresolved_questions` de TODOS los claims que su entrada enlaza — señalizarla
sólo en documentación narrativa es hallazgo MATERIAL (la señal vía
`scripts/check_consumption_contract.py <curso>/` es determinista). NO
auto-corregir la biblioteca. NO declarar PASS sin haber ejecutado las
verificaciones. Los workers NUNCA inventan links a recursos inexistentes.

## Output

Cada worker devuelve su spool y un resumen final de ≤10 líneas (conteos,
clasificaciones, frames creados, cambios propuestos). El integrador:
verifica cardinalidad/unicidad → aplica a los archivos canónicos → ejecuta
`validate_library.py` hasta `PASS`.
