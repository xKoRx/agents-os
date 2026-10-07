# REQUEST-AUDIT

Auditoría de muestras reales del journal (`provider_invocations.request_json`) por clase de task. Las 5 clases pedidas: `claims.reconstruction`, `claims.equivalence_review`, `claims.grounding_review`, `sko.composition`, `sko.composition_review`.

## claims.reconstruction (10 llamadas; muestra w0002 inspeccionada completa)

- `task_contract: claims.reconstruction vmke.claims-recon.v2` ✓ (prompt v2, la versión con regla de idioma)
- `evidence_of_this_window` con 8 frames, cada uno con `kind frame`, `pts`, `rel_ns`, `sha256` y artifact path ✓
- Regla de idioma presente: `Preserve the source language in canonical claim statements.` ✓
- Guidance `EQUIVALENT_TO` presente ✓
- Sin claim slugs pre-sembrados; sólo el `target: w0002` de la ventana

## claims.equivalence_review (0 llamadas)

**No alcanzada en este gate** (0 colisiones de identidad). Nada que auditar. El contrato de request queda verificado por la suite permanente (`v2_identity_remediation_test.go`, incluye probe de request: sin slug, ambas statements, kind+epistemic, schema y prompt version congelados).

## claims.grounding_review (81 llamadas; muestra `cl-bearish-range-to-be-shown-next` inspeccionada)

- `target: cl-bearish-range-to-be-shown-next@1` (marker id@version) ✓
- `review_contract: claims.grounding_review vmke.claims-ground.v1` ✓
- `record: … version 1 kind procedure_step` + `epistemic_class: INSTRUCTOR_SAID` ✓
- `statement_under_review` en español ✓
- `cited_evidence` con el texto del transcript citado (`transcript asr-00012 […] text: …`) ✓

6 de las 81 fueron respuestas malformadas con corrective reissue exitoso (inicial REJECTED → reissue VALIDATED); los 75 records revisados quedaron cada uno con exactamente un outcome duradero.

## sko.composition (1 llamada)

- `task_contract: sko.composition vmke.sko-compose.v1` ✓
- `supported_claims_catalog` con claims soportados (id@version, kind, epistemic, statement) ✓
- **Sin respuesta**: fallo de transporte del provider (`read-body` retryable; budget de reintentos 2 agotado en el adapter live) → `composition_unavailable: true` en la proyección; run terminal INCOMPLETE honesto, 0 SKOs fabricados.

## sko.composition_review (0 llamadas)

No alcanzada: depende de una composición exitosa.

## Higiene

- Ningún secreto/API key en requests ni responses persistidos (el transport de openrouter no persiste headers).
- 9 invocations sin fixture de replay (2 recon REJECTED conservadas como fixture en el script de replay; 6 grounding REJECTED subsumidas por su correctivo VALIDATED; 1 composition sin respuesta reproducida como transport-error entry).
