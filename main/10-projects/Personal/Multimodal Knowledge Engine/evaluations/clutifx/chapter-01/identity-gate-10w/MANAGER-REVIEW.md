# MANAGER-REVIEW — facts para adjudicación

Sin recomendación final. Sólo hechos observados del gate.

## Run health

- Terminación **ordenada** INCOMPLETE (exit 4): composition unavailable + 9 records non-supported. Cero FATAL, cero ClassFatal de identidad, cero crash.
- `NO_IDENTITY_CLASSFATAL = YES` (no se ejercitó: 0 colisiones — el contrato anti-corrupción no fue estresado en este gate).
- `WHOLE_WINDOW_ATOMICITY_OBSERVED = PASS` — auditado físicamente, no por tests: w0001/w0003 REJECTED con `records_committed: 0`, cero stage rows, cero records canónicos de sus proposals, 111/111 dependency edges resueltos, invocations durables preservadas como auditoría.
- `EVIDENCE_ACCUMULATION = NOT_EXERCISED` (0 re-observaciones equivalentes).
- `PROVENANCE_ACCUMULATION = NOT_EXERCISED` (ídem).

## 10-window completion

8/10 aceptadas. Las 2 rechazadas lo fueron por **output inválido del modelo live** (proposals citando evidence refs inexistentes con formato inventado `asr-NNNNN [rango]`) — fail-closed determinista, sin adjudicación, sin daño canónico. Tasa de rechazo por ruido de provider: 20% de ventanas en esta muestra.

## Colisiones y equivalence verdicts

**0 colisiones de identidad de cualquier clase** (exact duplicate / deterministic equivalent / semantic review / EQUIVALENT / DIVERGENT / structural). La máquina `claims.equivalence_review` no fue ejercitada live. El incidente original w0002×w0003 no se reprodujo: w0003 murió antes del ladder y el espacio de slugs cambió (statements ahora en español). **Esta es la principal limitación del gate: el mecanismo central de la remediation sigue sin evidencia live.**

## Canonical compression ratio (esta muestra)

- `canonicalization_ratio = 75/75 = 1.0` (todo lo propuesto por ventanas validadas commiteó).
- `raw_to_canonical_reduction = 0.0`.
- La reducción real vino de otras capas: 2/10 ventanas perdidas antes del ladder y grounding honesto (56 claims + 10 relations supported de 75 records = 88%).

## Lenguaje

64/64 claims en español (heuristic stopword/ñ, aproximada). El contrato de idioma del prompt v2 (`Preserve the source language`) se observó estrictamente; en la corrida original (prompt v1) las statements eran mayoritariamente inglés. `SOURCE_LANGUAGE_CONTRACT_OBSERVED = PASS`.

## Provider failures

1 evento: composition `read-body` retryable, budget de 2 reintentos del adapter agotado → composition unavailable → 0 SKOs. También 8 respuestas malformadas en un solo run (2 recon + 6 grounding inicial) — todas correctamente contenidas (2 rechazos de ventana, 6 correctivos). El modelo live mostró alta variabilidad de calidad de output.

## Budget / tokens / costo

91 llamadas con usage de 92 invocations; 419,758 prompt + 163,555 completion = 583,313 tokens. Costo: `null` (el adapter no lo expone). Extrapolación cruda NO autoritativa: 5.8k tokens promedio/record canónico; el capítulo completo (130 ventanas × ~7.5 records/ventana validada) quedaría ~1.5-2M tokens, dentro del techo 60M — sólo como orden de magnitud, sujeto a la varianza de rechazos observada.

## L2 reached?

`L2_REACHED = NO`. Composition no completó por fallo de transporte del provider (no por defecto del pipeline ni presupuesto). La única fase L2 ejecutada fue el intento de composición; composition_review no se alcanzó.

## Replay status

`REPLAY = PASS` (contenido idéntico; deltas = identidad del adapter + contadores de budget por correctivos, ambos explicados en RUN.md). `RESUME_NO_RECHARGE = NOT_EXERCISED` (run terminal; el contrato de adopción es RUNNING-only).

## Hotspots potenciales para el Primary Manager

1. **Equivalence review sin ejercicio live** — decidir si se requiere un gate dedicado que garantice colisiones (p.ej. mayor solapamiento entre ventanas) antes de liberar el capítulo completo.
2. **Tasa de output inválido del modelo** (2 recon + 6 grounding + 1 transport failure en 92 llamadas ≈ 10%) — impacto directo en throughput real y estimación de presupuesto del capítulo completo.
3. **Composition frágil ante transport errors** — el catálogo grande puede exceder el tamaño de respuesta estable del modelo; una única unavailable mata todo L2 del run (por diseño actual).
4. **Claims COMPOSITE degradadas por atomicidad** (1 caso observado) — comportamiento contractual, pero sugiere que el reviewer de grounding y el atomicity check pueden discrepar; ver frecuencia en el capítulo completo.
