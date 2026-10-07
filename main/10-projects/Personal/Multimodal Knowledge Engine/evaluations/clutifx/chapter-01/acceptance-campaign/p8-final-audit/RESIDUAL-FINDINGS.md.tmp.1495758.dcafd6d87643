# P8 — RESIDUAL FINDINGS (adjudicación del Manager)

Entrada: 1043/1043 claims + 146/146 relations + 19/19 rechazadas + 64/64 non-supported + 78 casos identidad + 1 composition + journal provider, todo auditado ONE-SHOT sin muestreo (`results/`). Adjudicación por el Primary Manager, 2026-10-04.

## BLOCKER

**B-08 — L2_REACHED = NO en el capítulo: composition fail-closed por-proposición.**
Evidencia: 1 invocación `sko.composition` (7879f510, 16:28:27Z, REJECTED); propuesta de 23 objetos / 164 refs; **7 refs not-exists en 4 objetos** (19 objetos 100% válidos); rechazo atómico → 0 SKOs. El mensaje fail-fast reportó sólo la 1.ª ref y enmascaró el patrón. Timeout NO fue factor (231.5s = 39% de 600s; request 160,575 bytes / 41,972 prompt tokens). Falla directo del gate congelado `L2_REACHED = YES, SKOS_TOTAL > 0` (sin exemption de owner vigente).
**Remediación:** R-M05 (validación por-objeto, pipeline-side, commiteada por owner en `8ae543a` durante la campaña) — expectativa 19/23 objetos publicables, 4 descartados con razón durable por objeto. Requiere validación targeted-live del stage L2 + auditoría de los SKOs producidos.

## MAJOR

**M-07 — Grounding FN rate 25% semántico (16/64) > 10% congelado; 46.9% contando causa-provider (30/64).**
Desglose: 16 semánticos (8 causal/definicional + 5 deixis + 3 garble-identity — los mismos patrones M-01, con la elipse «Felur Swing»≡failure-swing y el caso GIP RE-currente de P1) + 9 malformed-verdict (el reviewer emitió `GROUNDING_SUPPORTED` en el journal y el pipeline lo descartó por schema-id/addressing) + 5 parse-fatal (fuente sostiene, 0 contenido persistido). Falta directo del umbral `grounding false-negative rate ≤ 10%`.
**Remediación:** (a) tolerancia de formato del validador grounding (recupera 9 records determinísticamente desde journal/replay, sin nueva llamada); (b) re-review targeted-live de los 5 parse-fatal (retry contractual, la clase nunca fue evaluada); (c) calibración reviewer v3 (causal/deixis/garble) — requiere **full rerun** para ejercitarse (R5: cambia materialmente el output).

**M-08 — MISSING_MATERIAL = 4 en ventanas aceptadas (umbral congelado = 0).**
w0010 («la vela tampoco tiene que ser negativa como tal» — ausente de todo el store; es la corrección del WRONG baseline `cl-vela-negativa-mayoria` → regression watch = ABSENT_AND_MISSING) · w0036 (vínculo rangos-Libra↔SMT, forward-reference) · w0033 (record existe, sin publicar por malformed-verdict → **recuperable por M-07a**) · w0067 (identidad EURUSD/15M visible desde w0067, canónica recién w0073/77/84 — **cubierto-luego, pérdida neta discutible**; residuo real adjudicado: 2–3 proposiciones).
**Remediación:** calibración recon v3 (negaciones/excepciones + forward-references verbatim) → mismo full rerun de M-07.

**M-09 — Regression watch w0037 = STILL_WRONG publicado.**
`cl-gbpusd-today-target-137489` SUPPORTED con el MISMO error del baseline (objetivo real 1.35843/1.36031 vs 1.37489 dibujado; frames verificados). Además `cl-chart-symbol-gbpusd` (cabecera EURUSD) y `cl-rango-nivel-inferior-112695` (~1.1263 vs 1.12695) WRONG publicados. Total 3 wrong materiales publicados = 0.27% total / ~0.5% material → **el umbral numérico CUMPLE**, pero el caso w0037 repite el error M-04 pese a la regla v3 de verificación de niveles → la regla no bastó; reforzar con el caso concreto en recon v4. Los otros 4 WRONG materiales del audit quedaron fail-closed correctamente (los CONTRADICTED del grounding fueron veredictos correctos).

## MINOR

**MI-05 — Fragmentación del store empeoró: 13 → 77 pares byte-idénticos (29 grupos).**
El ladder une intra-id pero nunca cross-slug; familias «instrumento EURUSD» (13 core + ~18 extendidas), 15m (~12), 8h (~8), FOREX.com (~9). Deuda MI-03 arrastrada (fuera de alcance esta campaña por decisión P2: requiere design change del contrato de identidad). No es corrupción; crece con escala.
**MI-06 — Caché de adjudicaciones sin invocación journalizada (brecha auditabilidad).**
59 adjudicaciones servidas de caché (58 merges + el rechazo DIVERGENT de w0093) no dejan fila en provider_invocations; status_reasons cita «equivalence_review returned DIVERGENT» sin llamada que lo respalde. Registrar cache-hits (response_state=CACHE_HIT o tabla).
**MI-07 — Contadores no reconciliables.**
documentation.md reporta 128 semantic-equivalent / 37 deterministic / 139 reviews vs journal+store 117/36/71+caché; y el flag `applied` del análisis (22) subcuenta los 153 merges reales. Definir fórmulas y documentarlas.
**MI-08 — Parse-fatal sin reissue contractual (5 records, 0.42%).** El mecanismo de reissue existente recuperó 217/227 malformed-verdicts; extenderlo a parse-fatal es la palanca si se exige 0 REVIEW_UNAVAILABLE. (R-M06 añade reissue para recon, no para grounding.)

## NOTE

**N-06 — F-2 (array-content) queda UNKNOWN con exclusión positiva:** ninguno de los 5 fatals persistió contenido; por código, el caso campo-como-array fallaría antes (Op `parse`), no en `parse-structured`. Compatibles: array-como-string, JSON truncado, prosa. Persistir forma+hash del contenido en fatals para adjudicar a futuro (KISS).
**N-07 — B-01 (empty-content retryable) no se ejercitó en vivo:** 0 eventos empty-content en 130 ventanas (vs 2 run-killing en el run viejo). El fix está verificado en-source (`6dec7e5` ancestro; ClassRetryable) pero su camino quedó sin ejercicio live — deuda de cobertura de prueba, no defecto.
**N-08 — Inconsistencia de modalidad en equivalence:** el patrón «hay que ir viendo» vs «observar» mergea en un caso (#11) y rechaza en otro (w0006) — 6 FALSE_DIVERGENT + 1 AMBIGUOUS de 71 reviews (9.9% vs baseline 11.8%). El adjudicador mejoró pero mantiene sobre-rechazo conservador por sinonimia/paráfrasis.
**N-09 — ASR-garble embebido en 2 PARTIAL publicados («Felur Swing» como término)** — deuda N-04 del baseline, sin normalización canónica (pool por-claim).
**N-10 — Gobernanza de commits R-M05/R-M06:** `8ae543a` y `edec9a8` (author git = xKoRx) aparecieron locales durante la sesión de manager, fuera de mandato explícito de esta sesión. Se adoptan como R2 previa revisión adversarial R3 ( tests incluidos: 230+352+275 líneas). Ninguno de los workers ONE-SHOT despachados tenía mandato de escribir código; anotado para el registro de campaña.

## Gates congelados P2 — estado tras P8 (pre-remediación)

| Gate | Estado |
|---|---|
| wrong_claim_rate ≤0.5% / material ≤1% / sin WRONG nuevo en reglas centrales | **PASS** (3 publicados: 0.27%/~0.5%; ningún WRONG en reglas centrales) |
| material precision ≥97% | **PASS** (98.2%) |
| MISSING_MATERIAL = 0 en aceptadas / residuo <19 | **FAIL 4** (residuo 10 ✓) |
| grounding FN ≤10% / non-supported <80 | **FAIL 25–46.9%** (64 < 80 ✓) |
| identity_false_merge = 0 | **PASS** (0) |
| 0 material false merges / 0 corrupción / atomicidad / replay | **PASS** |
| L2_REACHED = YES, SKOS > 0 | **FAIL (0 SKOs)** |
| Escala: 0 babysitting / L2 reliable / replay / 0 BLOCKER | unattended ✓, replay ✓; L2 y B-08 pendientes |

```text
PHASE = P8
STATUS = FINDINGS
CHAPTER_THRESHOLDS_MET = NO
OWNER_DECISION_REQUIRED = NO (todas las reparaciones son técnicas y acotadas; sin choice semántica genuina)
NEXT_PHASE_AUTHORIZED = YES (remediation loop: R1 diseño → R2/R3 → targeted live L2 + re-review → full rerun con v3 → P8 again)
```
