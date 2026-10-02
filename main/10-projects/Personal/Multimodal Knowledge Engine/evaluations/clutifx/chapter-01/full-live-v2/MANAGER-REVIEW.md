# MANAGER-REVIEW — facts para adjudicación (sin decisión)

## Terminal state

- Status **INCOMPLETE** (exit 4, terminal ordenado), producto `ef53530` intacto (`PRODUCT_CODE_CHANGED = NO`, `PROMPTS_CHANGED = NO`, `D4_TOUCHED = NO`, `V3_SCOPE_ADDED = NO`).
- 130/130 ventanas intentadas: 104 aceptadas, 26 rechazadas, 0 unavailable.
- Wall 9h27m17s en 3 tramos; 2 crashes por `assistant content is empty` (w0057, w0093) recuperados por crash/resume contractual sin pérdida de trabajo y sin re-llamadas de ventanas validadas.

## Conocimiento

- Propuestos: 1039 claims + 168 relations. Canónicos: **803 claims + 130 relations** (integrity 933/933 PASS).
- Publicación: **853 supported (741 claims + 112 relations)** / 80 non-supported (62 claims + 18 relations: 74 INSUFFICIENT + 5 CONTRADICTED + 1 REVIEW_UNAVAILABLE). Nota COMPOSITE: 5 claims con grounding SUPPORTED quedaron publicadas UNSUPPORTED_INSUFFICIENT por atomicidad COMPOSITE (degradación contractual multi-evidencia, ver reasons de documentation.md). La descomposición por kind/epistemic/idioma está en METRICS.json.
- No soportados: 80 (74 INSUFFICIENT, 5 CONTRADICTED, 1 REVIEW_UNAVAILABLE). Están publicados y marcados, no ocultos.
- **L2_REACHED = NO**: 0 SKOs; única llamada de composition con transport failure (`read-body retry-exhausted`), razón durable persistida. El mismo modo de fallo del gate 10W; en el stress gate el transporte sí funcionó → transiente de backend, pero es la 2.ª vez en 3 corridas live.

## Identity ladder (primera vez a escala)

- 38 colisiones: 1 deterministic-equivalent, 15 semantic-equivalent merges, 22 divergent (16 deterministas kind/epistemic/structural + 6 semánticas).
- `claims.equivalence_review` ejercitado **live 17 veces** (+4 re-verdictos content-addressed = 21 adjudicaciones): 11 EQUIVALENT / 6 DIVERGENT.
- **Acumulación live ejercitada y auditada: LIVE_ACCUMULATION_AUDIT = PASS** — 12 merges aplicados sobre 7 records (primera evidencia live de EQUIVALENT→APPLY→unión de EvidenceIDs/InvocationIDs); 3 merges decididos no aplicados por atomicidad whole-window de ventanas con otra colisión.
- **WHOLE_WINDOW_ATOMICITY = PASS** (0 records/stages/edges residuales de las 26 ventanas rechazadas).
- Clasificación humana del operador (17/17): 12 OBVIOUSLY_EQUIVALENT, 3 AMBIGUOUS, 2 OBVIOUSLY_DIVERGENT. **POTENTIAL_FALSE_SEMANTIC_MERGE = NO** (ningún DIVERGENTE-obvio mergeado). En dirección inversa: 1 sobre-rechazo conservador (#8, humano OBVIOUSLY_EQUIVALENT → engine DIVERGENT; costo de cobertura de w0094) y 3 AMBIGUOUS resueltos DIVERGENT (fail-closed conforme al prompt congelado).
- Hotspot de ladder: `cl-grafico-eurusd`/`cl-instrumento-eurusd` y las divergencias deterministas kind parameter-vs-observation sobre el mismo hecho visual recurrente (EURUSD/temporalidad) — 16 de las 22 divergencias son de este tipo.

## Provider reliability

- 1196 filas de journal (1194 cobradas); 115 correctivos de grounding con reissue exitoso (1 parse fatal → REVIEW_UNAVAILABLE).
- **Bad evidence refs: 4/130 ventanas (3.1%)** — el defecto del gate 10W (`asr-NNNNN [range]`) se reproduce a baja frecuencia; 0 decode fallidos.
- 2 run-killing fatals por contenido vacío del backend (transiente, recuperable por resume); 1 transport failure en composition.
- Presupuesto: vlm_call 1194/2400, vlm_image 1941/8000, vlm_token 8.6M/60M — sin omisiones de budget.

## Idioma

- Claims canónicas: 803 es / 0 en / 0 other (el prompt v2 de la remediation fijó idioma fuente; vs inglés mayoritario del run pre-remediation).

## Tokens / performance (insumo para proyección 200 h, sin capacity architecture)

- Total 8,600,403 tokens (6.29M prompt / 2.31M completion); 1196 llamadas.
- Por ventana (130): ~4.4 min wall, ~9.2 llamadas, ~66k tokens, ~8.0 claims propuestos, ~6.2 claims canónicos, ~6.6 supported.
- Proyección aritmética cruda para 200 h ≈ 353 capítulos equivalentes × 9.5 h ≈ 139 días de cómputo secuencial — SOLO como dato; no es una declaración de capacidad (L2 falló en 2/3 corridas live; el fat transiente del backend mata el run sin resume).

## Replay

- **REPLAY = PASS**: outcome funcional idéntico (853/80, mismas 26 ventanas, ladder line byte-idéntica); deltas enumerados y explicados en RUN.md §REPLAY (texto de razones con historia de resume/wrapping de error; 1 fila de claims con texto de error adicional; Δbudget 0.03%).

## Deudas/hallazgos para adjudicación (sin fix en esta misión)

1. **L2 frágil al transporte**: 1 error read-body → 0 SKOs para todo el capítulo (composición all-or-nothing contractual). 2.ª vez en 3 corridas live.
2. **Fatal por contenido vacío del backend** mata el run (2 veces en 130 ventanas); el resume contractual lo recupera pero requiere intervención operador → candidata a retry-clase-retryable en el adapter (cambio de producto, FUERA de esta misión).
3. **Bad evidence refs 3.1%**: persiste el patrón del 10W a baja frecuencia; cada ocurrencia cuesta la ventana completa.
4. **INSUFFICIENT masivo en grounding** (74 claims + 17 relations): revisar si el reviewer es demasiado estricto con evidencia de segmento único — requiere decisión con el Owner mirando muestras (OWNER-VALIDATION.md).
5. **Divergencias deterministas recurrentes** (16): el modelo alterna kind parameter/observation para el mismo hecho visual; cada una cuesta la ventana. Ladder los captura sin corrupción (correcto), pero es pérdida de cobertura estructural.
6. Contador `equivalenceReviews` cuenta adjudicaciones incl. replays (NOTE conocido del adversarial review, confirmado: 21 vs 17 llamadas).

## Boundary

No se declara `MKE COURSE PIPELINE = READY`; no se autorizan otros capítulos; no se extrapola a 200 h. Sigue: Owner manual review (OWNER-VALIDATION.md) + Primary Manager review + decisión `CHAPTER_01_ACCEPTED` / `READY_TO_SCALE_CORPUS`.
