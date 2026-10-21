# AMENDMENTS — ch09-red-flags (Clutifx · Chapter 09)

Registro append-only de correcciones materiales post-publicación. Capítulo publicado 2026-10-21. Cierre semántico el mismo día (2026-10-21): 3 correcciones documentales/métricas registradas abajo, originadas en una auditoría que halló 2 de las 8 correcciones del DOCVERIFY in-mission sin aplicar en el árbol publicado. Las 12 correcciones de literalidad aplicadas en integración (antes de la publicación) están documentadas en review-notes y no generan amendments (no cambiaron proposiciones publicadas).

### am-ch09-doc-001 — DV09-001 re-aplicada: proyecciones resolvían el garble «tarjeta breakable» (c-0015 / q-ch09-002)

- **Fecha:** 2026-10-21 · **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/CLAIMS#c-0015|c-0015]] (sin cambio de statement ni de veredicto)
- **Motivo:** documentation.md §2 («mover el stop a break even») y study-guide.md §2 («parciales + break even») resolvían categóricamente la ambigüedad que el claim mantiene abierta (TERM_DISAMBIGUATION_REQUIRED; q-ch09-002 OPEN). El DOCVERIFY in-mission la adjudicó (DV09-001, MATERIAL) pero la corrección no llegó al árbol publicado pese a estar registrada como aplicada.
- **Antes → después:** «…y mover el stop a break even [c-0015]» → «…y, segundo, "mover tu tarjeta breakable" [ASR — la lectura "mover el stop (o el target) a break even" es candidata NO confirmada; ver q-ch09-002, audio s-000426] [c-0015]»; «→ parciales + break even [c-0015]» → «→ parciales + "mover tu tarjeta breakable" [ASR; la lectura "break even" es candidata NO confirmada — q-ch09-002] [c-0015]».
- **Evidencia:** s-000426 (transcript); claims.jsonl c-0015 (garble preservado); spool del run `docverify/findings.json` DV09-001.
- **Resultado:** duda preservada en todas las proyecciones; q-ch09-002 sigue OPEN (sin confirmación de audio no se adjudica); las afirmaciones de break even con respaldo propio (c-0071, c-0129) quedan intactas.

### am-ch09-doc-002 — DV09-006 re-aplicada: adyacencia claim-frame en examples E5

- **Fecha:** 2026-10-21 · **Claims:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/CLAIMS#c-0026|c-0026]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/CLAIMS#c-0032|c-0032]] (sin cambio de statements)
- **Motivo:** examples.md E5 listaba f-000856/f-000859 (evidencia de c-0032) adyacentes a c-0026, cuyo frame propio es f-000706; inducía asociación errónea. Corrección adjudicada in-mission (DV09-006, MENOR) sin aplicar.
- **Antes → después:** frames f-000856/f-000859 junto a c-0026 → f-000706 junto a c-0026 y f-000856/f-000859 tras c-0032 (coherente con FRAMES.md).
- **Resultado:** navegación coherente; sin cambio de proposiciones.

### am-ch09-doc-003 — Errata de métricas: agent wall sin respaldo de epochs + unidades de rate mezcladas

- **Fecha:** 2026-10-21
- **Motivo:** (a) el agent wall «~109 min» publicado no es reconstruible de los epochs/spools del run (extracción ~51 min + revisión ~75 min = ~127 min; ventana 11:20:33→13:30:11 = 129,6 min; el handoff había reportado ~119 min como suma de estimaciones 49+70); (b) «0,27× realtime — el peor rate del curso» mezclaba velocidad (video/wall) con multiplicador de costo (wall/video): en unidades homogéneas de costo ch09 = 3,72× NO es el peor del curso (ch04 = 9,06×).
- **Después:** README reconciliado con valores respaldados por asr.log/epochs/spools, nomenclatura normalizada (ASR_SPEED = video_duration/ASR_wall; ASR_COST_MULTIPLIER = ASR_wall/video_duration) y tabla homogénea entre capítulos. Los valores OBSERVED originales se preservan en la sección de reconciliación del README; los README de ch02–ch08 no se retocan (fuera de alcance).
- **Resultado:** métricas reconciliadas (METRICS_RECONCILED = PASS); historia observada intacta.
