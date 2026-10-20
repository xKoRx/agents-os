# AMENDMENTS — Clutifx Chapter 07 (Setups)

Registro append-only de correcciones materiales post-publicación (amendment_id, claim_id, fecha, motivo, antes/después, evidencia, resultado). Reservado para correcciones materiales posteriores a la publicación; los ajustes aplicados ANTES de publicar (vía pool, durante la integración) se documentan en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/review-notes|review-notes]].

## am-ch07-001

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0230|c-0230]]
- **Fecha:** 2026-10-20
- **Motivo:** fidelidad al instructor — el statement omitía el hedge literal (regla predictiva publicada sin modalización).
- **Antes:** «Solo haciéndote estas cuatro preguntas puedes determinar ya si tu vela va a ser la que manipula, la que distribuye, un reversal o una continuación.»
- **Después:** «'Yo creo que' solo haciéndote estas cuatro preguntas puedes determinar ya si tu vela va a ser la que manipula, la que distribuye, un reversal o una continuación.»
- **Evidencia:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/transcript#^s-004404|s-004404]] («Yo creo que solo haciéndoos estas cuatro preguntas podéis determinar…») · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/transcript#^s-004410|s-004410]]. Propagado a rules R27, concepts C12, documentation §7 y study-guide §5 para no presentarlo como clasificación garantizada.
- **Resultado:** CORREGIDO — misma proposición con hedge restaurado; verdict SUPPORTED conservado.

## am-ch07-002

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0170|c-0170]]
- **Fecha:** 2026-10-20
- **Motivo:** evidencia incompleta por timeframe — f-003328 es EURUSD 12H (sostiene «objetivos en 12 horas») pero faltaba el frame del «gráfico de 4 horas de euro».
- **Antes:** `evidence = ["s-003302","s-003328","f-003328"]`
- **Después:** `evidence = ["s-003302","s-003328","s-003336","f-003328","f-003336"]` con review_reason documentando qué parte del statement sostiene cada frame.
- **Evidencia:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/frames/f-003336.png|f-003336]] verificado como EURUSD 4H con niveles horizontales abajo (sostiene «4 horas de euro» + «el doble está claro aquí abajo»); [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/frames/f-003328.png|f-003328]] verificado como EURUSD 12H con caja de rango bajo el precio (sostiene «este en 12 horas»). Verificación VLM de ambos PNG.
- **Resultado:** CORREGIDO — statement intacto, evidencia completa y adjudicada por frame.

## am-ch07-003

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0187|c-0187]]
- **Fecha:** 2026-10-20
- **Motivo:** verificación visual antes sólo parcial (la apertura de la vela de la 1 no quedaba plenamente corroborada por el still).
- **Verificación nueva (completa):** crop ampliado 2× del borde derecho + análisis visual de [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/frames/f-003551.png|f-003551]]: EURUSD 8H con rectángulo de rango bajista dibujado; la última vela (01:00) abre por ENCIMA del cuerpo de la vela 13:00 anterior — corroboración visual completa.
- **Evidencia:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/transcript#^s-003551|s-003551]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/transcript#^s-003557|s-003557]] («a la una lo que nos hace es abrir por encima de esta vela lo que nos está creando un rango bajista de 8 horas»).
- **Resultado:** VERIFICADO — sin cambio de proposición; epistemic `visual_observation` se mantiene (la imagen SÍ demuestra el detalle ahora).

## am-ch07-004

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0188|c-0188]]
- **Fecha:** 2026-10-20
- **Motivo:** la verificación previa de f-003603 devolvió error de ejecución con resultado parcial.
- **Verificación nueva (completa):** crop ampliado 2× del borde derecho + análisis visual de [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/frames/f-003603.png|f-003603]]: EURUSD 4H con rectángulo de rango dibujado bajo las velas recientes; la vela 05:00 abre por ARRIBA del cuerpo de la vela 01:00 anterior (gap al alza) — corroborado sin errores.
- **Evidencia:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/transcript#^s-003603|s-003603]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/transcript#^s-003608|s-003608]] («A las 5 nos abre esta vela por arriba, lo que significa que estamos creando un rango de 4 horas veris»).
- **Resultado:** VERIFICADO — sin cambio de proposición; verdict SUPPORTED y epistemic conservados.
