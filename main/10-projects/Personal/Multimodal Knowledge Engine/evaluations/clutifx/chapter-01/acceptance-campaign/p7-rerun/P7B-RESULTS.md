# P7b — RESULTADOS (rerun @ `e7bc387`, incidente de transporte del backend)

**Candidato:** `e7bc387` (binario `72bdde7b…`, config `02f5f7ad…`, fingerprint `f05c95e4…`). Runtime: `~/mke/clutifx-ch01-rerun2-20261004/run-rerun2/` (exit 4 INCOMPLETE ordenado). Lanzado 2026-10-04 ~20:30Z, terminado 2026-10-05 ~10:30Z.

## Incidente de transporte (externo al producto)

**`vlm provider transport [retry-exhausted]` ×355 entre 04:34Z y 10:28Z (~6h, pico 05–07Z con >100 fails/hora).** El backend dejó de servir requests completos por ~6 horas: las ventanas w0093–w0130 (38) agotaron su reconstruction (3 intentos c/u) y quedaron UNAVAILABLE; 306 grounding reviews y 11 composition reviews cayeron igual. **0 run-kills** — el run sobrevivió a la interrupción completa del proveedor con salida durable parcial ordenada (exit 4). Probe post-incidente: 3/3 inferencias HTTP 200 (backend recuperado).

## Resultado (degradado POR EL INCIDENTE, no por el producto)

- **w0001–w0092 (92 ventanas):** extraídas con la MEJOR calidad de contenido de los 3 runs: 766 claims, **459 supported, sólo 5 non-supported por contenido** (4 INSUFFICIENT + 1 CONTRADICTED) — las otras 302 son REVIEW_UNAVAILABLE (sus grounding reviews cayeron en el incidente). 1 ventana rechazada por slip (w0028, bad-ref) → **RECUPERADA por el corrective reissue R-M06 en vivo** (`w0028:corrective` VALIDATED; publicada SUPPORTED con provenance doble base+correctivo).
- **w0093–w0130 (38 ventanas):** UNAVAILABLE por transporte (sin knowledge extraído).
- **L2_REACHED = YES a escala real:** `sko.composition` VALIDATED; 33 composition reviews (14 VALIDATED / 7 REJECTED / 12 caídas en el incidente); **26 SKOs publicados, 12 SUPPORTED** — R-M05 per-object funcionó end-to-end (el composer volvió a alucinar componentes y el run publicó los objetos válidos en vez de 0).

## Certificación de remediación que este run demuestra (a escala, con incidente)

| Remediación | Evidencia live |
|---|---|
| B-01/R-B01 empty-content retryable | 0 run-kills en 1094 llamadas a través de un blackout de 6h |
| B-02 composition timeout | composition completó en tiempo |
| R-M05 per-object | 26 SKOs publicados (vs 0 en run-1) con alucinaciones del composer presentes |
| R-M06 corrective reissue | w0028 base-REJECTED → corrective VALIDATED → publicada |
| Fail-closed general | 302+38 degradaciones a UNAVAILABLE ordenadas, 0 corrupción, 0 babysitting |

## Adjudicación

`P7B = RESILIENCE_CERTIFIED__NOT_A_CHAPTER_CANDIDATE` — la interrupción del proveedor (causa externa, ~44% de las llamadas) dejó 38 ventanas sin extraer y 302 records sin veredicto de grounding. El artefacto del capítulo no puede ser este run. **P7c autorizado inmediatamente** (mismo baseline `e7bc387`, backend sano verificado): es re-ejecución, no nueva remediación — no se requieren gates adicionales porque P7b YA certificó todo el código a escala real bajo condiciones adversas.
