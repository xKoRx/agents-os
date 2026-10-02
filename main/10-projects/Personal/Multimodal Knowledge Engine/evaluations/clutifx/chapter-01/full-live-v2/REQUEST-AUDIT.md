# REQUEST-AUDIT — métricas del provider (journal durable)

| Métrica | Valor |
|---|---|
| Llamadas (filas de journal) | 1196 = 1194 cobradas + 2 filas de error sin cargo (grounding fatal, composition transport) |
| Cobradas por ledger | 1194 consumed + 4 released (reservas huérfanas de los 2 crashes) |
| claims.reconstruction | 130 (126 VALIDATED + 4 REJECTED por evidence refs inventadas — validación de propuesta, no JSON malformado; +2 intentos fatales re-invocados por resume, filas actualizadas in-place por identidad content-addressed) |
| claims.equivalence_review | 17 VALIDATED |
| claims.grounding_review | 1048 (932 VALIDATED + 115 REJECTED→reissue correctivo + 1 fatal) |
| sko.composition | 1 (transport retry-exhausted) |
| Respuestas malformadas iniciales (correctivos) | 115 (todos con reissue VALIDADO salvo 1: el parse fatal) |
| Transport failures / timeouts | 1 retry-exhausted (composition); 0 timeouts |
| Fatales de parse en reconstruction (run-killing) | 2 (w0057, w0093: `assistant content is empty` del backend; recuperados por resume contractual) |
| Prompt tokens | 6,293,102 |
| Completion tokens | 2,307,301 |
| Total tokens | 8,600,403 |
| Reported cost | null (el adapter no expone costo; no se inventa) |

Presupuesto canónico: vlm_call 1194/2400, vlm_image 1941/8000, vlm_token 8,600,403/60,000,000 (línea durable de documentation.md). Modelo observado en todas las responses: `stealth/space-bunny-alpha`.

El detalle por invocación (request/response/usage/error) queda en el run.db local (`run-live/run.db`, snapshots de crashes incluidos); no se sube al vault por peso. `replay-script.json` permite reproducir todo el run sin red.
