# AMENDMENTS — ch11-riesgo (Clutifx · Chapter 11)

Registro append-only de correcciones materiales post-publicación. Capítulo publicado 2026-10-22. Las 26 correcciones de literalidad/evidencia adjudicadas durante la integración (ANTES de la publicación) están documentadas en review-notes y no generan amendments (no cambiaron proposiciones publicadas: restauraron el literal, completaron evidencia de frontera o corrigieron visual_hints antes de que existiera versión pública).

## am-ch11-doc-001 — Referencia intercapítulo mal clasificada bajo CH07 (2026-10-22, closeout targeted)

- **Claim(es)**: ninguno modificado — corrección clasificatoria documental sobre [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/CLAIMS#c-0012|c-0012]] y [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/CLAIMS#c-0070|c-0070]] (statements y evidencia intactos).
- **Motivo**: documentation.md §16 y study-guide §6 atribuían bajo «CH07 (setups/checklist)» dos conexiones que la fuente remite al vídeo de NOTICIAS (ch10): c-0012 («he explicado antes con el vídeo de noticias», s-000410) y c-0070 («lo que os decía en el capítulo de noticias también», s-002310/s-002313). El transcript de ch11 contiene exactamente dos referencias intercapítulo dichas y ambas son a ch10; ninguna referencia a setups/checklist de ch07 existe en la fuente.
- **Antes**: bullet CH07 en §16 y study-guide §6 con c-0012/c-0070; README Prerrequisitos/Referencias y COURSE-INDEX listaban ch07.
- **Después**: bullet CH07 eliminado; c-0070 incorporada al bullet CH10 (que ya documentaba c-0012/c-0042); README y COURSE-INDEX sin ch07 en prerrequisitos/referencias, con nota de la corrección.
- **Evidencia**: s-000410, s-000415 (vídeo de noticias), s-002310+s-002313 (capítulo de noticias); búsqueda sobre claims.jsonl (0 menciones de setups ni del checklist de 4 preguntas — ese claim pertenece a ch07) y transcript.
- **Resultado**: clasificación documental corregida; conexiones conservadas sólo donde la fuente las respalda (ch10). q-ch11-012 no afectada (duda de alcance preservada, PARTIAL).

## am-ch11-doc-002 — Errata de métricas del run (2026-10-22, reconciliación contra epochs/spools/commits)

- **Claim(es)**: ninguno — corrección de reporting.
- **Motivo**: el handoff publicó TOTAL_WALL ≈ 190 min (3h10m) y REVIEW_WALL ≈ 42,9 min / INTEGRATION ≈ 40 min sin respaldo de epochs; el ASR arrancó 23:17:43 y la publicación remota (commit 5c81a66e, push a GitHub) ocurrió 03:37:37 = 259,9 min. La reconciliación por epochs/spools/mtimes (run dir `clutifx-ch11-20261021/`) y su errata completa viven en el README (§ Throughput, «Errata de métricas») y en METHODOLOGY-FEEDBACK (CH11 CLOSEOUT).
- **Resultado**: ASR_WALL 96,1 min y EXTRACTION pura ~50,6 min CONFIRMADOS; REVIEW puro ≈ 48 min (no 42,9); INTEGRACIÓN 48,3 min (no ~40); TOTAL_WALL a publicación remota ≈ 4h20m (no 3h10m). Las cifras originales se conservan en el README como historia.
- **Resultado**: REPORTING_RECONCILED = PASS.
