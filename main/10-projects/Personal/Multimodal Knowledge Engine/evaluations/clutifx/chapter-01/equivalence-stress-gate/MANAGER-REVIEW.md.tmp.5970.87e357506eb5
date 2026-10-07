# MANAGER-REVIEW — sólo facts

## Pregunta del gate

¿Funciona `claims.equivalence_review` live cuando el mismo conocimiento reaparece en ventanas consecutivas?

## Facts

- **¿Ejecutó equivalence review live?** SÍ. 3 invocaciones live de `claims.equivalence_review` (task journalado, modelo observado `stealth/space-bunny-alpha`, response_ids durables, usage por invocación). 0 reissues, 0 timeouts, 0 errores de provider en esta tarea.
- **¿Cuántas veces?** 3 adjudicaciones sobre 3 colisiones semánticas reales (todas w0002-o1 → w0002-o4). Hubo además 1 colisión determinista (kind parameter vs observation, o1→o2) que por contrato NO se adjudica, y 1 duplicado exacto idempotente decidido sin llamada.
- **¿Qué statements?** Los 3 pares están íntegros en EQUIVALENCE-DECISIONS.md y los RequestJSON completos en `request-audit/`.
- **¿Qué veredictos?** 2 EQUIVALENT + 1 DIVERGENT. Clasificación para review humano: 1 OBVIOUSLY_EQUIVALENT, 1 AMBIGUOUS (`cl-eurusd-subida-previa`: el entrante añade el ancla "antes de la caída reciente"; juzgada misma proposición material defendible), 1 OBVIOUSLY_DIVERGENT (scope "curso completo" vs "capítulo").
- **¿Algún merge sospechoso?** Ningún merge entró al store: la ventana o4 fue rechazada completa por el DIVERGENT antes del APPLY, así que ni siquiera los 2 EQUIVALENT se aplicaron. El store canónico (47 claims + 1 relation) contiene sólo first-observations de o1/o3.
- **¿Acumulación de evidencia/provenance?** Decidida 2 veces (EQUIVALENT), aplicada 0 veces. Físicamente: 0 filas `EVIDENCE_ACCUMULATED`, 0 provenance multi-invocación. La semántica de rechazo sí quedó demostrada físicamente (atomicidad whole-window: o2 y o4 con 0 records, 0 stage rows, 0 edges; run continuó; terminal INCOMPLETE ordenado exit 4).
- **¿Algún ClassFatal?** NO. 0 fatales de identidad; 0 `error_class` en las 66 invocaciones; el run terminó INCOMPLETE ordenado (exit 4), no fatal (exit 5).
- **¿Bad evidence refs?** 0. Las 4 propuestas pasaron `ValidateProposal` citando sólo IDs exactos existentes; 90/90 dependency edges resuelven. El defecto del gate 10W (refs `asr-NNNNN [rango]`) no se reprodujo.
- **¿Lenguaje?** 47/47 claims en español (heurística de stopwords; fuente en español). SOURCE_LANGUAGE = PASS.
- **¿L2 alcanzado?** SÍ — primera vez live: composition (1 llamada) + composition review (5 llamadas) todas VALIDATED; 5 SKOs publicados, 5/5 `SUPPORTED_BY_AUTOMATED_REVIEW`. En el gate 10W esta fase había fallado por transporte (`read-body`); aquí 0 fallos de transporte en todo el run.
- **¿Fallos de provider?** 0. (5 primeros intentos de grounding review fueron rechazados por output malformado y reissue correctivo exitoso en los 5 — comportamiento contractual existente, no fallo de provider.)
- **¿Tokens / costo?** 66 calls / 312,000 tokens (recon 151,661; equivalence 1,506; grounding 146,660; composition 7,504; composition review 4,669). Budget 66/2400 calls, 68/8000 imágenes, 312,000/60M tokens. Costo `null` (no expuesto por el adapter).
- **¿Wall time?** 27m53s (18:31:14Z → ~18:59:07Z).
- **¿Replay?** PASS: claims.jsonl / skos.jsonl / documentation.md semánticamente idénticos tras normalizar identidad de ejecución; razones de rechazo y contadores del ladder byte-idénticos; delta de budget explicado (5 correctivos no representables con 1 fixture por (task,target)); adjudicaciones reusadas del journal sin nuevas llamadas.

## Limitaciones de alcance de este gate

- 4 ventanas sobre 39 s de un capítulo de 34 min; máximo de la misión cumplido (no se corrieron ventanas extra).
- La mitad de ACUMULACIÓN del ladder (union de evidencia + provenance multi-invocación aplicados) sigue sin evidencia live de aplicación: requeriría una ventana entrante con colisiones EQUIVALENT y ninguna DIVERGENT en la misma propuesta.
- El veredicto EQUIVALENT de `cl-eurusd-subida-previa` queda clasificado AMBIGUOUS para revisión humana; no afectó al store.

## NO decidido aquí

El capítulo completo, la configuración del próximo run y cualquier remediation: decisión del Primary Manager + Owner.
