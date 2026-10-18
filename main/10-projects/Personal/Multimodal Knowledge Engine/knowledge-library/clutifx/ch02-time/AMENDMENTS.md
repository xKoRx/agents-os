# AMENDMENTS — ch02-time

Historial **append-only** de correcciones materiales y decisiones semánticas
sobre los claims del capítulo. Formato por entrada: `amendment_id` · `claim_id`
· fecha · motivo · anotación anterior · anotación nueva · evidencia revisada ·
resultado. Los IDs de claim NUNCA se renumeran; si una corrección cambia
materialmente la proposición, se crea un claim nuevo y el anterior queda
superseded (ver contrato en [[CLAIMS]] y en la skill principal).
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
