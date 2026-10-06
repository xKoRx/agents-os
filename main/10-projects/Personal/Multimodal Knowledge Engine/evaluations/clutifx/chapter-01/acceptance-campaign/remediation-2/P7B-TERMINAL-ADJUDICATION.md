# P7b — ADJUDICACIÓN DE TERMINALIDAD + CRITERIO DE VALIDEZ DE RUN (pre-registrado)

Manager: Primary Technical Manager (track P8/P9) · 2026-10-06 (post-terminalidad, previo a P7c).

## Terminalidad P7b (`~/mke/clutifx-ch01-rerun2-20261004/run-rerun2/`)

```text
EXIT_CODE = 4 (INCOMPLETE ordenado) · 2026-10-04T20:03Z → 2026-10-05T10:30Z (~14.5h, unattended, 0 manual resumes)
ventanas: 82 aceptadas / 49 rechazadas (38 por TRANSPORTE w0093+, 11 por identidad: 5 divergent + 3 epistemic + 2 kind + 1 otro; 0 bad-refs, 0 relation-id)
records: 766 claims + 104 relations · 553 supported / 343 non-supported (de los cuales ~306 = REVIEW_UNAVAILABLE por TRANSPORTE + 2 parse-fatal; sin malformed-verdict)
L2: composition VALIDATED 10:25Z · 28 objetos propuestos · 2 DESCARTADOS por-objeto con razón durable (R-M05: sko-range-chain-strategy c9, sko-turtle-soup c4 — refs not-exists) · 26 SKOs publicados (auditar)
1 correctivo recon (R-M06 ejercitado 1×) · atomicity PASS · 1094 calls / 6.69M tokens
fatals: 2 per-record fail-closed (1 grounding parse-fatal, 1 composition_review parse-fatal) · 0 run-killing
```

**Causa del daño de cobertura: TORMENTA DE TRANSPORTE EXTERNA 04:34–10:28Z (pico 05–08Z), 355 invocaciones `transport [retry-exhausted] request timed out` (budget 2 agotado; requests colgaban a 600s).** El mismo backend en P7 (run-1) tuvo 0 errores de transporte; las ventanas w0001–w0092 con los MISMOS prompts v4/v3 corrieron a ritmo normal (~92 ventanas en 8.5h) → no es efecto de prompt. El backend se recuperó y el propio run terminó L2-VALIDADO a las 10:25Z.

## Estado de las remediaciones (evidencia parcial, a certificar por auditoría R6)

| Remediación | Evidencia P7b |
|---|---|
| R-M05 (composition por-objeto) | **FUNCIONA**: 26/28 publicados; el objeto que mató P7 completo se descartó solo, con razón durable |
| Tolerancia validador grounding | **FUNCIONA**: 0 «malformed verdict» en status_reasons (vs 9 fail-closed en P7) |
| R-M06 (reissue recon) + recon v4 | **FUNCIONA**: 0 bad-refs, 0 relation-id (vs 2 en P7); 1 correctivo ejercitado |
| Reviewer v3 / anti-rubber-stamp | A certificar por auditoría semántica de los 553 supported y los non-supported semánticos |
| Identidad (M-02) | Colisiones 17→11; a clasificar |

## CRITERIO DE VALIDEZ DE RUN PARA ACEPTACIÓN (pre-registrado ANTES de P7c)

Un run live 130 ventanas es **VÁLIDO como vehículo de aceptación** sii:

1. **0 ventanas muertas por transporte** (`transport retry-exhausted` en recon) — cada una de las 130 debe haber ejercitado su recon semántico.
2. **≤ 2% de records** non-supported por causa transporte (`REVIEW_UNAVAILABLE` con root transport).
3. El resto de las clases (parse-fatal, formato, identidad, veredictos semánticos) se auditan con los umbrales P2 intactos — son semántica/contrato, no entorno.

Si el run no cumple 1–2: es **diagnóstico, no aceptación** → se repite el full rerun bajo condiciones sanas. Si DOS runs consecutivos son invalidados por tormenta de transporte: `OWNER_DECISION_REQUIRED = YES` (bloqueo ambiental, 2 datos).

**Justificación:** los umbrales P2 miden calidad semántica de extracción; un run en que ~25% de los records nunca fueron revisados mide el backend, no el producto. Fail-closed de transporte es contrato (correcto); re-ejecutar bajo condiciones sanas es la única forma honesta de medir los gates. Este criterio queda fijado ANTES de ver cualquier resultado de P7c (sin outcome-shopping).

## Decisión

```text
P7B_RUN_VALID_FOR_ACCEPTANCE = NO (criterio 1 y 2 violados: 38 ventanas + ~306 records por transporte)
PRODUCT_REMEDIATIONS_EXERCISED = YES (L2 per-object, tolerancia, R-M06, v4: todas con evidencia positiva)
NEXT = P7c full rerun (mismo bundle e7bc387, backend sano desde 10:30Z Oct 5) + auditoría R6 de P7b en paralelo
```
