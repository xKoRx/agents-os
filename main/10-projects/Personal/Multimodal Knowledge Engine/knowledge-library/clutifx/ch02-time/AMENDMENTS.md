# AMENDMENTS — ch02-time

Historial **append-only** de correcciones materiales y decisiones semánticas
sobre los claims del capítulo. Formato por entrada: `amendment_id` · `claim_id`
· fecha · motivo · anotación anterior · anotación nueva · evidencia revisada ·
resultado. Los IDs de claim NUNCA se renumeran; si una corrección cambia
materialmente la proposición, se crea un claim nuevo y el anterior queda
superseded (ver contrato en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS.md|CLAIMS]] y en la skill principal).
Regeneraciones cosméticas de proyecciones NO se registran aquí (para eso está
git).

---

## amend-0001

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0056|c-0056]]
- **Fecha:** 2026-10-18
- **Motivo:** contradicción entre capas de notas acumuladas — la capa del review M8 original leía "descartado = rango grande 1,4748–1,5803 / válido = inferior ~1,4565–1,4748", mientras la capa P4 (remediación) leía lo contrario; la pila de notas anidadas era ilegible y autocompetente.
- **Anotación anterior:** tres capas append-only sin reconciliar (M8: lectura invertida + "no concluyente"; P1: "no adjudicable en still"; P4: "resuelto, válido = 1,4748–1,5803").
- **Anotación nueva:** nota estructurada en capas — HECHOS CONFIRMADOS (regla textual; niveles 1,5803/1,4748 dibujados) · INTERPRETACIÓN VIGENTE (válido = 1,4748–1,5803) · INTERPRETACIÓN DESCARTADA (lectura M8 invertida, refutada por el estado posterior en f-000806) · INCERTIDUMBRE RESIDUAL (referente del rectángulo descartado no probado). Estado del deíctico: PARTIALLY_RESOLVED.
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/frames/f-000758.png|f-000758]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/frames/f-000806.png|f-000806]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/transcript#^s-000758|s-000758]]–[[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/transcript#^s-000802|s-000802]]
- **Resultado:** regla general SUPPORTED se conserva (soporte independiente); deíctico abierto en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/OPEN-QUESTIONS#q-ch02-001|q-ch02-001]]; sin cambio de statement, verdict ni epistemic.

## amend-0002

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0066|c-0066]]
- **Fecha:** 2026-10-18
- **Motivo:** `epistemic` era `model_inference` con `SUPPORTED` — inaceptable sin adjudicación (un claim de inferencia del modelo no es conocimiento del curso).
- **Anotación anterior:** `epistemic: model_inference` (proyección del precio leída como inferencia del extractor).
- **Anotación nueva:** `epistemic: instructor_statement` — adjudicación A: el condicional "si el DXY está bearish… si está bullish…" es textual del instructor (s-001005/s-001010); el frame adjunto es contexto del low candidato, no prueba de la proyección.
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/transcript#^s-001005|s-001005]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/transcript#^s-001010|s-001010]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/frames/f-001030.png|f-001030]]
- **Resultado:** reclasificación (una de las 5 del diff pre/post; ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/repair/REPAIR-LOG|repair/REPAIR-LOG]] errata B3); statement y verdict intactos.

## amend-0003

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0066|c-0066]] → sustituido por [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0099|c-0099]] (supersession, contrato V1.2)
- **Fecha:** 2026-10-19
- **Motivo:** normalización terminológica materialmente equivocada — el statement publicaba "el DXY" donde la fuente dice "el doble" (s-001005) y "dol" (s-001010). Mismo defecto de clase que la remediation DOL/DXY de ch03 (2026-10-18): el glosario mapeaba el garble a DXY globalmente y se trató como permiso de sustitución. Adjudicación: DOL_CONFIRMED.
- **Anotación anterior:** "si el DXY está bearish, va a seguir para abajo; si el DXY está bullish, va a tomar el low, crear un rango bullish y subir" (dos normalizaciones a DXY).
- **Anotación nueva:** "si el DOL [ASR: 'el doble'/'dol'] está bearish, va a seguir para abajo; si el DOL está bullish, va a tomar el low, crear un rango bullish y subir" (c-0099).
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/transcript#^s-001005|s-001005]] ("el doble") · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/transcript#^s-001010|s-001010]] ("dol", palabra literal) · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/transcript#^s-001401|s-001401]] (autocorrección "a por tu dol, perdón, a por tu objetivo") · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/frames/f-001030.png|f-001030]] (sólo gráfico EURUSD 1h, rama alcista dibujada desde el low candidato, sin panel de índice).
- **Resultado:** c-0066 queda SUPERSEDED (preserva ID, evidencia y adjudicación histórica; marcado y navegable en CLAIMS); c-0099 publicado como instructor_statement/SUPPORTED con la palabra dicha preservada. La lectura DXY no tiene ningún respaldo textual en ch02 (cero menciones de DXY/índice/dólar en el transcript completo); la semántica del draw (DOL bearish → abajo; DOL bullish → toma el low y sube) y la correlación EURUSD/DXY descartan la lectura de índice en la rama bearish.

## amend-0004

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0089|c-0089]] → sustituido por [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0100|c-0100]] (supersession, contrato V1.2)
- **Fecha:** 2026-10-19
- **Motivo:** normalización terminológica materialmente equivocada — el statement publicaba "a por tu DXY" donde la fuente dice "a por tu dol, perdón, a por tu objetivo": el instructor dice "dol" y se autocorrige a "objetivo"; DXY no aparece en la fuente. Adjudicación: DOL_CONFIRMED.
- **Anotación anterior:** "un rango a favor para ir a por tu tendencia —a por tu DXY, perdón, a por tu objetivo—".
- **Anotación nueva:** "un rango a favor para ir a por tu tendencia —a por tu DOL [ASR: 'dol'], perdón, a por tu objetivo—" (c-0100).
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/transcript#^s-001401|s-001401]] (literal, con la autocorrección del instructor).
- **Resultado:** c-0089 queda SUPERSEDED (preserva ID, evidencia e historia); c-0100 publicado como instructor_statement/SUPPORTED. No modifica la definición de DOL ni ningún claim de ch03.
