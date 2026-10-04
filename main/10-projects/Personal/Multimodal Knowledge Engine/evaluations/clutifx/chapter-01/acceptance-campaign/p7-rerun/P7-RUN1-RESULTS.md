# P7 RUN-1 — RESULTADOS Y ADJUDICACIÓN POST-RERUN

**Candidato:** `19b44c1` (pushed), prompts v3/v2, cts=600. Runtime: `~/mke/clutifx-ch01-rerun-20261003/run-rerun/` (exit 4 INCOMPLETE ordenado, ~13h wall).

## Resultado

- **128/130 intents de reconstruction sin run-kill** (R-B01 probado en escala: 0 fatales `assistant content is empty` en reconstruction; en el run viejo 2 mataban el run).
- **111/130 ventanas aceptadas, 19 rechazadas** (17 ladder fail-closed: 10 DIVERGENT semánticos + 7 deterministas kind/epistemic; w0058 bad-ref con rango; w0075 rel-id con prefijo cl-) — vs 26/130 del run viejo.
- **1043 claims + 146 relations**: 997/1043 claims SUPPORTED (**95.6%** vs 92.9% old), 128/146 relations (87.7% vs 86.2%); non-supported total 64 (46 claims + 18 relations) vs 80.
- Ladder mucho más sano: **182 colisiones → 128 merges EQUIVALENT + 37 deterministic-equivalent accumulations + 17 divergentes** (old: 38 colisiones/15 merges/22 divergentes); 139 reviews semánticas (71 invocaciones live: 61 EQUIVALENT + 10 DIVERGENT).
- Lenguaje 1043/1043 español (14 sin marcadores verificadas 1 a 1: español con términos técnicos en inglés citados por el instructor).
- Integridad 1043/1043 PASS. MODEL_INFERRED 3 (old 22).
- Grounding: 5 claims UNSUPPORTED_REVIEW_UNAVAILABLE por JSON malformado real del reviewer (fatal record-scoped contract-consistente; 0.4%; old 1).
- **L2: `sko.composition` completó EN TIEMPO (B-02 FIXED: 65,894 tokens, 24k completion) pero el proposal fue REJECTED closed**: el composer alucinó 7 componentes fuera de catálogo en 4 de 23 objetos (ej. `cl-estrategy-chain-of-ranges`@1, `cl-reinizado-*` por `reiniciado`) sobre el catálogo de 41,972 tokens ⇒ 0 SKOs.

## Adjudicación post-P7 (Primary Manager)

**M-05 (NUEVO, MAJOR — bloquea el gate L2):** la fidelidad del composer a 41.9k tokens de catálogo es el nuevo boundary: 7/196 componentes (3.6%) alucinados ⇒ rechazo atómico del proposal ⇒ 0 SKOs. Fail-closed funcionó (0 SKOs falsos). El transporte/timeout quedó descartado como causa.
**R-M05 (diseño):** validación de composición por-objeto: los objetos con componentes inválidos se descartan con razón durable por-objeto; los objetos válidos se publican. Determinista, sin llamadas extra, fail-closed a granularidad objeto. (Descartada la alternativa de corrective reissue: recovery incierto para fallo de recall a escala, costo extra, YAGNI. El contenido de los objetos descartados vive en los claims L1.)
**M-06 (residuo M-03, MAJOR):** 2/130 ventanas (1.5%) perdidas por slips de formato (w0058 ref con rango — la misma ventana del run viejo; w0075 rel-id mal prefijada).
**R-M06 (diseño):** 1 corrective reissue en reconstruction ante fallo de validación de proposal (decode/ValidateProposal), reusando el patrón de correctivos de grounding (115 usos probados): re-invocación con el error de validación nombrado; 2º fallo ⇒ rechazado closed como hoy.
**Sin fix:** 5 REVIEW_UNAVAILABLE (contenido malformado real, fatal contract-correcto); 17 rechazos ladder (contrato).

## Disposición

`P7_RUN1 = INCOMPLETE_USEFUL (fuerte)` · `REMEDIATION_ROUND_2_AUTHORIZED = YES` (R-M05 + R-M06) · después: gate R-M05 por harness live sobre el catálogo P7 → **P7b full rerun** como candidato final del capítulo → P8/P9.
