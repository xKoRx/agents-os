# P6 — ERRATA DE REPORTING (resuelta contra journal durable)

**Adjudicado por:** Primary Manager, 2026-10-04, antes de usar P6 como evidencia de P8/P9.
**Fuente de verdad:** `~/mke/clutifx-ch01-p6-gate-20261003/run-p6/run.db` (journal durable, terminal) + `../p6-live-gates/P6-LIVE-GATES.md` (reporte canónico).

## Errata A — «0 identity collisions» vs «w0078 → equivalence_review EQUIVALENT»

Las dos afirmaciones refieren a métricas DISTINTAS; no se contradicen:

| Métrica (journal P6) | Valor |
|---|---|
| Ventanas rechazadas por colisión de identidad (determinista) | **0** |
| Reviews semánticos de equivalencia (`claims.equivalence_review`) | **8** |
| — EQUIVALENT (VALIDATED → merge/acumulación) | **8** |
| — DIVERGENT | **0** |
| Reviews de equivalencia por ventana | 19 ventanas → 8 reviews |

El evento de w0078 (`claims-equivalence:cl-cierre-fuera-deja-de-ser-rango@1:w0077->w0078` VALIDATED, 2026-10-04T00:14:52Z) es un **review semántico de equivalencia** (el camino de acumulación que repara el falso split N-01), NO una colisión de identidad. La narrativa correcta: «0 colisiones de identidad deterministas; 8 reviews de equivalencia semántica, todos EQUIVALENT, 0 DIVERGENT». Clasificación humana de los 8 (del reporte P6): 7 OBVIOUSLY_EQUIVALENT + 1 plausible (w0011→w0051, re-verificación en P8).

## Errata B — «3/3 bad-ref windows cured» vs «w0003 rejected (ñ)»

| Pregunta | Veredicto (journal) |
|---|---|
| ORIGINAL_BAD_REF_DEFECT_FIXED | **YES** — w0005, w0043, w0110 (las 3 ventanas con refs inventadas del run viejo, `asr-NNNNN [range]` / `transcript asr-`) terminaron VALIDATED con refs válidas. El patrón no se reprodujo (0/19). |
| WINDOW_RECOVERED (w0003) | **NO** — w0003 fue RECHAZADA por una causa nueva y no relacionada: claim id `cl-vista-desplazada-a-mañana-24-junio` con charset inválido (`ñ`), familia formato, fail-closed benigno (journal 2026-10-03T23:11:51Z). |
| NEW_UNRELATED_REJECTION | **YES** — 1/19 ventanas en esta noche; 0/130 en el run viejo. Transiente aceptado por adjudicación P6, sin fix de producto (normalizar slugs tocaría identidad; deuda documentada). |

No se llama «recovered» a w0003: la ventana se perdió por un slip distinto; el DEFECTO bad-ref sí está curado.

## Registros contables P6 (para trazabilidad P8)

19 reconstrucciones · 8 equivalence (8 VALIDATED) · 207 grounding (170 VALIDATED / 37 REJECTED) · 1 composition + 25 composition reviews → 19 SKOs publicados (19/19 SUPPORTED) · 1 ventana REJECTED (w0003, charset).
