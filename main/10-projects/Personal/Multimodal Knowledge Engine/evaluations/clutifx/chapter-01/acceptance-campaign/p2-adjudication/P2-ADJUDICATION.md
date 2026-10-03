# P2 — PRIMARY MANAGER ADJUDICATION

**Entrada:** P1 exhaustive audit (`../p1-audit/`), 2026-10-04.
**Rol:** Primary Technical Manager / Acceptance Lead. Clasificación: BLOCKER (impide extracción confiable u operación no atendida a escala) / MAJOR / MINOR / NOTE.

## Veredicto P1→P2

`P1_ACCEPTANCE_AUDIT = COMPLETE` (130/130, 803/803, 130/130, 26/26, 80/80, 38/38, todo auditado con fuente). El contenido material del capítulo es correcto en un 98.0% de sus claims materiales y no pierde ninguna ventana material completa. Los defectos reales son de clasificación, citación de evidencia y operación de proveedor — todos reparables dentro de las superficies acotadas del mandato.

## Findings

### BLOCKER

**B-01 — Provider fatal mal clasificado: `assistant content is empty` mata el run.** (`p1-audit/results/PROVIDER-FAILURE-AUDIT.md`)
2 eventos en 130 ventanas (~1/36), ambos no persistentes (replay directo → VALIDATED), clasificados `parse-structured [fatal]` en `openrouter.go:420-423` que agrupa sin distinción los errores de `extractJSONObject`; el caso hermano (200 sin choices) ya es retryable con rationale explícito de transiente. Violación directa del requisito de escala: «unattended run must tolerate normal transient provider failures». Categoría: provider reliability + operational durability.

**B-02 — L2 composition estrangulado por timeout por intento: `L2_REACHED = NO` en el capítulo.** (`p1-audit/results/L2-FAILURE-AUDIT.md`)
Catálogo de 853 records (request 121,155 bytes ≈ 30k tokens) bajo `Limits.Timeout=120s`; los 3 intentos HTTP consumieron cada uno su deadline (361.9s journal ≈ 3×120s+1.5s) muriendo en lectura de body; el mismo backend completó outputs de esa escala bajo el timeout de 600s de reconstruction. No es transitorio ni rechazo por tamaño. El criterio duro de aceptación exige «L2 completes successfully OR explicit accepted chapter-level reason» — con fix acotado disponible, la razón aceptada no existe todavía. Categoría: L2 availability.

### MAJOR

**M-01 — Masa de fallo de grounding: 66/80 records non-supported recuperables.** (`GROUNDING-AUDIT.md`)
48 EVIDENCE_SELECTION_PROBLEM (la reconstrucción cita el segmento con las palabras de contenido y omite el adyacente con antecedente/causa/continuación) + 14 FALSE_NEGATIVE del reviewer (garbles de ASR sin equivalencia —«Tartel Sub»≡Turtle Soup, «GIP»≡GBP—, deixis del discurso, cláusulas causales). El reviewer fue estrictamente correcto sólo en 13/80. Categoría: semantic correctness + coverage.

**M-02 — Inestabilidad de clasificación de identidad: 15/16 divergencias deterministas son ruido del modelo.** (`IDENTITY-AUDIT.md`)
Patrón dominante: flip observation↔parameter sobre metadatos del gráfico, incluyendo 4 ventanas con statement byte-idéntico al canónico (sólo cambia `kind`); flips epistémicos por deixis dual-fuente; 2 re-renders de slug en divergencia estructural de relation. Consecuencia: 11/26 rechazos por re-declarar contexto ya en store + fragmentación (13 pares con statement byte-idéntico). El ladder se comportó contract-correctamente; el ruido es upstream. Categoría: semantic correctness + coverage.

**M-03 — Bad evidence refs: 4/130 ventanas (3.1%) perdidas por formateo.** (`REJECTED-WINDOW-AUDIT.md`)
`asr-NNNNN [range]` ×3 y `transcript asr-NNNNN` ×1 con JSON válido; la reconstrucción semántica era correcta en 4/4 → hardening de prompt/schema es suficiente por evidencia. Categoría: coverage.

**M-04 — 4 claims WRONG materiales (0.5%) + 2 PARTIAL contaminados.** (`FULL-CLAIM-AUDIT.jsonl`)
`cl-vela-negativa-mayoria` (w0009, polaridad invertida), `cl-entradas-sirven-para-encontrar-bias` (w0011, relación invertida), `cl-objetivo-hoy-rango-bullish-libra` (w0037, objetivo 1.37489 vs 1.35843 dibujado), `cl-cambio-oferta-demanda-termino-ingles` (w0106, ASR «change instead of delivery» convertido en término inexistente; contamina w0106 ×2 como PARTIAL). Causas: lectura visual fina de niveles dibujados y garble de ASR; las reglas centrales de trading (rangos, SMT, Turtle Soup, Power 3) resultaron 100% correctas. Categoría: semantic correctness.

### MINOR

**MI-01 — COMPOSITE over-strict: 3/5 degradaciones injustificadas** (oración con «porque», valor+hint de un estado de UI, cita literal de una cláusula). 2/5 justificadas. Categoría: semantic correctness (atomicity reviewer calibration).

**MI-02 — Relations: 15/18 rechazos son falsas negativas** (misma causa de citación truncada de M-01) + 2 WRONG_TYPE (`rel-*`). Precision del engine al aceptar: 111/112. Categoría: coverage.

**MI-03 — Fragmentación del store: 13 pares de records con statement byte-idéntico** (slugs distintos evaden la identidad por record_id; ~12 records para «el gráfico es EURUSD»). Contenido correcto, cero corrupción; crece linealmente con la escala. Categoría: operational durability.

**MI-04 — Reporting:** `window-coverage.json` marca 3 bad-refs como categoría «other» (artefacto de resume: la razón de re-validación sobrescribe la original — ya documentado en replay-comparison); `equivalenceReviews` cuenta re-veredictos del journal, no sólo llamadas live (NOTE conocido del adversarial 2026-10-01). Categoría: reporting.

### NOTE

**N-01 —** 2 falsos splits confirmados (w0028 modalidad «Hay que ir viendo/Observar», w0094 definitez «La/Una SMT») + 2 AMBIGUOUS resueltos DIVERGENT: contract-consistente fail-closed; mejora del adjudicador (criterio de sinonimia superficial vs proposición) reduce el costo sin tocar la política.
**N-02 —** Falsos positivos raros: 1/30 en muestra de grounding, 1/112 en relations; asimetría aceptable, monitorear en rerun.
**N-03 —** Cadena definicional del Turtle Soup bajista huérfana (claims sin relations conectándolas, a diferencia del análogo alcista); enriquecimiento, no error de extracción.
**N-04 —** Garbles de ASR heredados fielmente («Tartel», «DXI», «GIP», «change instead of delivery»): los claims que citan garble heredan el error (causa de parte de M-04/M-01); la normalización pertenece a un pool canónico, no por-claim.
**N-05 —** w0081 divergencia speech/pantalla («la libra» vs etiqueta XAUUSD) capturada correctamente como dos claims separados: comportamiento deseable verificado.

## Owner decision check (regla del mandato)

- ¿kind=parameter u observation para identidad visual de instrumentos? **No es decisión de owner:** la evidencia P1 muestra que son la MISMA proposición con `kind` flippante = ruido de clasificación (M-02); el congelado ya define los kinds; el fix es estabilidad del prompt, no redefinición de política.
- ¿Cuándo dos statements son la misma proposición? La política frozen ya responde (fail-closed DIVERGENT; guardas deterministas). Los 2 falsos splits se tratan con precisión del adjudicador (N-01), sin tocar la política.
- Ningún finding requiere elegir entre semánticas múltiples razonables. `OWNER_DECISION_REQUIRED = NO`.

## Umbrales numéricos de aceptación (definidos post-P1 sobre materialidad observada)

Para `CHAPTER_01_ACCEPTED = YES` tras remediation + rerun (P7/P8), sobre la distribución observada:

1. wrong_claim_rate ≤ 0.5% de claims totales y ≤ 1% de materiales (baseline: 4/803 = 0.50%), sin WRONG nuevo en reglas centrales.
2. material precision (CORRECT+DUPLICATE sobre MATERIAL=YES) ≥ 97% (baseline 98.0%).
3. MISSING_MATERIAL = 0 en ventanas aceptadas (baseline ya 0/104) y residuo material de rechazadas < 19 proposiciones (estrictamente menor).
4. grounding false-negative rate sobre records non-supported ≤ 10% (baseline 17.5%) y non-supported total < 80 (estrictamente menor).
5. identity_false_merge_count = 0 (duro, invariante).
6. Requisitos duros invariables: 0 material false merges, 0 corrupción durable, atomicidad whole-window PASS, omisiones materiales conocidas explícitamente, replay PASS sin divergencia inexplicada.
7. L2: SKOs compuestos y soportados (>0), o razón chapter-level aceptada por Owner — con B-02 reparado se exige L2_REACHED = YES.

Para `READY_TO_SCALE_CORPUS = YES`: además B-01 reparado y certificado (0 runs matados por empty-content en transientes normales; retry contractual), MI-04 category fix, y 0 babysitting en el rerun completo.

## Disposición de remediación (entrada a P3)

| Finding | Superficie acotada | Remediación mínima |
|---|---|---|
| B-01 | provider retry classification | clasificar empty-content como retryable (hermano ya lo es), budget existente |
| B-02 | composition transport resilience | timeout por intento de composition al nivel de reconstruction (600s), config-contract |
| M-01 | grounding request quality + prompt contracts | citación del segmento adyacente en reconstruction; tolerancia reviewer a garble-identity/deixis/causal |
| M-02 | identity classification stability (prompt) | definiciones de kind/epistemic con ejemplos anti-flip; guardas frozen intactas |
| M-03 | prompt contract + schema validation | anti-patrones de refs + validación con reissue correctivo acotado |
| M-04 | prompt contracts (visual reading) | regla de verificación de niveles contra labels del frame; prohibición de objetivos no dibujados/dichos |
| MI-01 | atomicity guidance (prompt) | cláusula causal adjunta calificando la misma proposición = 1 claim |
| MI-02 | incluido en M-01 | — |
| MI-03 | sin cambio de producto esta campaña | deuda documentada (requiere design change del contrato de identidad) |
| MI-04 | reporting | propagación correcta de rejection_category en resume |

`STATUS = FINDINGS` · `OWNER_DECISION_REQUIRED = NO` · `NEXT_PHASE_AUTHORIZED = YES` (P3).
