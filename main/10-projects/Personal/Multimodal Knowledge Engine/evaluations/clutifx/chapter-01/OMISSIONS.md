# OMISSIONS — candidatos observables

Sólo hechos físicos. El Owner decide viendo el capítulo qué es realmente una omisión.

## Causa raíz del bloqueo (FATAL contractual)

- `00:12` y `00:37` — `cl-chart-instrument-eurusd@1` propuesto por w0002 y w0003 con contenido divergente (statement text + evidence window-local). El engine clasificó **ClassFatal** (`record identity corruption`, contrato Shot 3 S2-B-01) y detuvo el run fail-closed. Ningún record fue committeado; ninguna ventana posterior fue procesada.
- Naturaleza estructural observada: la igualdad de contenido incluye `evidence_ids`; los evidence ids son window-locales; los claim ids son slugs generados por el modelo. Todo hecho visual persistente re-proposto en una ventana posterior diverge al menos en evidencia ⇒ FATAL. Observado en el primer par de ventanas contiguas que comparten un visual persistente (2→3).

## Otros candidatos

- 127 ventanas (w0004–w0130, 00:42–34:03.9) sin procesar: omisión total por el bloqueo anterior.
- pipeline_state quedó `status=RUNNING` en el journal (el fatal no escribió estado terminal; exit code 5 fue el único terminal).
- Ninguna llamada de grounding review llegó a ejecutarse (el fatal precedió a la etapa de reviews).
- El techo de budget `max_vlm_calls=2400` habría detenido el run de todos modos más adelante: 3 ventanas produjeron 56 claims + 4 relations ⇒ proyección ~2.600 provider calls para 130 ventanas (ver SCALE-ESTIMATE.md). Documentado como dato, no como defecto.
