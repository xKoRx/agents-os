# LIVE EQUIVALENCE STRESS GATE — Clutifx ep01 (4 ventanas solapadas)

```text
LIVE_EQUIVALENCE_STRESS_GATE = PASS_WITH_FINDINGS
```

Pregunta que responde este gate: ¿la identity remediation realmente funciona con `claims.equivalence_review` usando el provider live cuando el mismo conocimiento reaparece en ventanas consecutivas? El gate natural anterior de 10 ventanas produjo `identity_collisions = 0` y `semantic_equivalence_reviews = 0`, así que la pieza central de la remediation no tenía evidencia live.

Respuesta: **SÍ — el ladder se ejercitó live de punta a punta.** 4 colisiones de identidad reales, 3 adjudicaciones semánticas live (`claims.equivalence_review`) con veredicto durable y auditable (2 EQUIVALENT + 1 DIVERGENT), 2 ventanas rechazadas closed con cero residuo físico (atomicidad whole-window demostrada), 0 ClassFatal, y —novedad frente al gate 10W— **L2 alcanzado: 5 SKOs publicados supported** vía composition + composition review live.

## Veredicto y hallazgos

- **PASS_WITH_FINDINGS** (no PASS plano): hay dos findings operacionales no bloqueantes.
- **F-1 (cobertura):** las 2 adjudicaciones EQUIVALENT fueron decididas pero nunca aplicadas — la tercera colisión de la misma ventana devolvió DIVERGENT y la rechazó completa antes del APPLY (atomicidad whole-window por diseño). Consecuencia física: `EVIDENCE_ACCUMULATED = 0` filas y 0 provenance multi-invocación, así que la mitad de acumulación del ladder sigue sin evidencia live de aplicación (la mitad de decisión sí quedó demostrada).
- **F-2 (review humano):** el veredicto EQUIVALENT de `cl-eurusd-subida-previa` se clasifica AMBIGUOUS (el entrante añade el ancla "antes de la caída reciente" que el canónico no afirma); se juzgó defensible como misma proposición material y no llegó a fusionarse en el store, pero queda marcado para revisión humana. Sin ningún caso OBVIOUSLY_DIVERGENT aceptado como EQUIVALENT.

## Contenido del bundle

| Archivo | Contenido |
|---|---|
| [SOURCE.md](SOURCE.md) | Identidad física del source y del L0 reutilizado |
| [RUN.md](RUN.md) | Precondiciones, ejecución live, terminal, replay |
| [WINDOWS.md](WINDOWS.md) | Diseño de las 4 ventanas (fijado antes del live) y resultado por ventana |
| [METRICS.json](METRICS.json) | Métricas completas extraídas del journal durable |
| [EQUIVALENCE-DECISIONS.md](EQUIVALENCE-DECISIONS.md) | Tabla obligatoria de las 3 decisiones live + clasificación para review humano |
| [REQUEST-AUDIT.md](REQUEST-AUDIT.md) | Auditoría de los 3 RequestJSON (copias sanitizadas en `request-audit/`) |
| [PROVENANCE.md](PROVENANCE.md) | Cadena de custodia, fingerprints, budget, tokens |
| [MANAGER-REVIEW.md](MANAGER-REVIEW.md) | Sólo facts para el Primary Manager |
| `claims.jsonl` / `skos.jsonl` / `documentation.md` | Salidas canónicas del live (47 claims + 1 relation + 5 SKOs) |

Runtime local: `~/mke/clutifx-ch01-equiv-stress-20261001/` (`run-live`, `run-replay`, `replay/`, `logs/`, `configs/`, `bin/`).

## Handoff

```text
LIVE_EQUIVALENCE_STRESS_GATE = PASS_WITH_FINDINGS
MKE_SHA = ef53530756a27009517030a1bd29f0472bb3ad48
SOURCE_SHA = 4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b
WINDOWS = 4
WINDOWS_ACCEPTED = 2
WINDOWS_REJECTED = 2
IDENTITY_COLLISIONS = 4
EQUIVALENCE_REVIEWS_LIVE = 3
EQUIVALENT = 2
DIVERGENT = 1
EVIDENCE_ACCUMULATIONS = 0
PROVENANCE_ACCUMULATIONS = 0
BAD_EVIDENCE_REF_WINDOWS = 0
L2_REACHED = YES
PROVIDER_CALLS = 66
TOTAL_TOKENS = 312000
WALL_TIME = 27m53s
PROJECT_BUNDLE_PATH = 10-projects/Personal/Multimodal Knowledge Engine/evaluations/clutifx/chapter-01/equivalence-stress-gate/
LOCAL_RUN_PATH = ~/mke/clutifx-ch01-equiv-stress-20261001/

NO_IDENTITY_CLASSFATAL = YES
NO_FALSE_EQUIVALENT_OBSERVED = YES
WHOLE_WINDOW_ATOMICITY = PASS
EVIDENCE_ACCUMULATION = NOT_EXERCISED
PROVENANCE_ACCUMULATION = NOT_EXERCISED
SOURCE_LANGUAGE = PASS
REPLAY = PASS
```

Este gate NO decide el capítulo completo. El Primary Manager revisa y decide el siguiente paso.
