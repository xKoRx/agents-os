# P1-SUMMARY — Exhaustive Source-Grounded Acceptance Audit

**Campaña:** Clutifx Chapter 01 — Full Acceptance + Remediation.
**Baseline auditada:** producto `ef53530756a27009517030a1bd29f0472bb3ad48`, source SHA `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b`, bundle `full-live-v2/` (reconciliado 2026-10-03), run durable `~/mke/clutifx-ch01-full-live-20261001/run-live/run.db`.
**Fecha:** 2026-10-03/04. **Método:** sin muestreo — 9 auditores independientes, separación real de responsabilidades (4 claims A1–A4, rechazadas B, grounding C, identidad D, relations E, forense L2/provider F).

## Cobertura física (completa)

| Población | Auditado | Método |
|---|---|---|
| 130/130 ventanas | ✔ | tabla por ventana en `FULL-WINDOW-AUDIT.md` |
| 803/803 claims | ✔ | 1 a 1 contra transcript y/o frames (`FULL-CLAIM-AUDIT.jsonl`, 803 líneas, IDs únicos, 0 solape entre auditores) |
| 130/130 relations | ✔ | endpoints+tipo+orientación contra fuente (`FULL-RELATION-AUDIT.jsonl`) |
| 26/26 ventanas rechazadas | ✔ | intervalo, razón, material, solape probado por record IDs, residuo (`REJECTED-WINDOW-AUDIT.md`) |
| 80/80 records non-supported | ✔ | + muestra 30 supported + 5 COMPOSITE (`GROUNDING-AUDIT.md`) |
| 38/38 colisiones identidad | ✔ | agrupadas en 27 clústeres que cubren las 22 ventanas rechazadas + 15 merges + 1 det-equivalent (`IDENTITY-AUDIT.md`) |
| 17 adjudicaciones live + 4 re-veredictos + 12 acumulaciones/7 records | ✔ | veredicto por caso + verificación física post-merge |
| 2 fatales provider + 1 fallo L2 | ✔ | forense con código citado (`L2-FAILURE-AUDIT.md`, `PROVIDER-FAILURE-AUDIT.md`) |
| Frames | ✔ | ~250 PNG leídos por los auditores; cada claim VIDEO_OBSERVED juzgado con ≥1 frame citado |

## Resultado por dimensión

### Claims (803)
CORRECT 692 (86.2%) · DUPLICATE 97 (12.1%) · PARTIAL 10 (1.2%) · WRONG 4 (0.5%) · OVERGENERALIZED 0 · UNVERIFIABLE 0.
MATERIAL=YES 548 / NO 255. De los materiales: CORRECT 463 + DUPLICATE 74 (correctos) · PARTIAL 7 · **WRONG 4**.

**Los 4 WRONG (todos MATERIAL=YES):**
1. `cl-vela-negativa-mayoria` (w0009) — invierte polaridad: la fuente dice que la vela suele ser positiva.
2. `cl-entradas-sirven-para-encontrar-bias` (w0011) — invierte la relación (los rangos sirven para encontrar entradas y bias, no al revés).
3. `cl-objetivo-hoy-rango-bullish-libra` (w0037) — asigna objetivo 1.37489 cuando el objetivo pronunciado/dibujado es 1.35843.
4. `cl-cambio-oferta-demanda-termino-ingles` (w0106) — ASR "change instead of delivery" (por *change in state of delivery*) mal transcrito y bautizado como término inexistente; contamina 2 claims vecinos como PARTIAL.

**Distribución temporal de errores (WRONG+PARTIAL=14):** 1/3 del capítulo: 6 (3 en w0001–w0002, zona de bienvenida/UI); 2/3: 1; 3/3: 7 (concentrados en la demo de la herramienta de posición y el esquema Power 3). Patrón: los errores se concentran en claims de lectura visual fina (niveles/objetivos dibujados) y terminología con garble de ASR — no en las reglas de trading centrales, que resultaron correctas (todas las reglas rango/SMT/Turtle Soup/Power 3 auditadas CORRECT).

### Missing knowledge
- **0/104 ventanas aceptadas con MISSING_MATERIAL** (6 con MISSING_NON_MATERIAL).
- Rechazadas: MATERIAL_LOSS=0, PARTIAL_MATERIAL_LOSS=10, NO_MATERIAL_LOSS=16 → **19 proposiciones materiales residuales** en 10 ventanas (mayormente: narración en tiempo real, regla de re-entrada w0074, parámetros del short w0116, punteros "más adelante"/"capítulo de entradas", vigilancia de dos pares w0092).
- 11/26 rechazos fueron por re-declarar parámetros de contexto con `kind` distinto — contenido que ya vivía en el store.

### Grounding (80 non-supported + 30 sample + 5 COMPOSITE)
CORRECT_REJECTION 8 · ACTUALLY_CONTRADICTED 4 (todas correctas) · FALSE_NEGATIVE **14** (17.5%) · EVIDENCE_SELECTION_PROBLEM **48** (60%) · ATOMICITY_PROBLEM 5 · PROVIDER_FAILURE 1. El reviewer fue estrictamente correcto en 13/80; **66/80 records son recuperables** (proposición verdadera y soportada en la fuente).
- Causa dominante: la reconstrucción cita el segmento con las palabras de contenido y deja fuera el segmento adyacente con el antecedente/continuación; el reviewer rechaza correctamente ese paquete incompleto. Segunda causa: garbles de ASR sin equivalencia de identidad («Tartel Sub»≡Turtle Soup, «GIP»≡GBP) y deixis del discurso.
- Falsos positivos: 1/30 en la muestra (`cl-rangos-bajistas-otra-vez`); 1/112 en relations aceptadas (`rel-reiniciado-pendiente-mismo-esquema`). Contradicciones: 4/4 veredictos correctos.
- COMPOSITE: 2/5 divisiones justificadas, **3/5 sobre-estrictas** (perdieron records soportados).

### Identidad (38 colisiones, 21 adjudicaciones, 12 acumulaciones)
- **0 falsos merges.** 11 EQUIVALENT live + 4 re-veredictos = CORRECT_EQUIVALENT; 7/7 acumulaciones CORRECT (statement first-observed, unión sorted-unique, sin cambio de significado).
- Divergencias deterministas: **15/16 MODEL_CLASSIFICATION_INSTABILITY, 1 TRUE_DIVERGENCE** (w0118). Patrón dominante: flip observation↔parameter sobre metadatos del gráfico (4 ventanas con statement byte-idéntico al canónico, sólo cambia el `kind`); flips epistémicos por deixis dual-fuente; 2 divergencias estructurales de relation con re-render del slug del endpoint.
- Falsos splits: **2 confirmados** (w0028 modalidad, w0094 definitez) + 2 AMBIGUOUS resueltos DIVERGENT fail-closed (contract-consistente).
- Consecuencia de cobertura de los 22 rechazos por ladder: ~85–90% re-cubierto por vecinas; costo real = fragmentación (13 pares de records con statement byte-idéntico en el store por slugs distintos; ~12 records para «el gráfico es EURUSD»), no vacíos.

### Relations (130)
CORRECT 126 (96.9%) · WRONG_TYPE 2 · UNSUPPORTED 2 (rechazos correctos) · WRONG_ENDPOINT 0. Integridad: 130/130 endpoints resuelven; 0 refs colgantes. Falsas negativas del reviewer: 15/18 rechazos (83%), misma causa de citación truncada. Ausente material: cadena definicional del Turtle Soup bajista huérfana (sin relations).

### L2 (composición)
Causa raíz medida: **timeout por intento estructuralmente insuficiente** — catálogo de 853 records (request 121,155 bytes ≈ 30k tokens cota) bajo `Limits.Timeout=120s`; 3 intentos HTTP consumieron cada uno su deadline completo muriendo en lectura de body (361.9s journal ≈ 3×120s+1.5s); el mismo backend completó outputs de esa escala bajo el timeout de 600s de reconstruction. NO fue transitorio puro, ni rechazo por tamaño, ni el timeout del pipeline. 1 solo intento lógico en todo el run; tras exit 4 (INCOMPLETE) el contrato no permite adoptar el run para retry.

### Provider fatales (`assistant content is empty` ×2)
Clasificados fatal por `openrouter.go:420-423` (agrupa sin distinción los 3 errores de `extractJSONObject`); el caso hermano (200 sin choices) ya es retryable con rationale explícito de transiente. Ambos fatales: replay directo → VALIDATED (no persistentes), recurrencia ~1/36 ventanas. **Según la semántica existente del propio adapter, debían ser retryable.** Costo operacional del crash/resume contractual verificado: replay de ventanas validadas sin nuevas llamadas, exactamente 2 re-invocaciones, 0 babysitting de ventanas ya validadas.

## Métricas P1 (denominadores documentados)

| Métrica | Valor | Definición/denominador |
|---|---|---|
| material_claim_precision | **98.0%** (537/548) | claims MATERIAL=YES con contenido correcto (CORRECT + DUPLICATE) / todos los MATERIAL=YES. Vista estricta first-observation: 463/548 = 84.5% |
| material_claim_coverage | **0 omisiones materiales en 104/104 ventanas aceptadas**; a nivel capítulo 19 proposiciones residuales de ventanas rechazadas (537 capturadas / 556 identificadas por la auditoría = 96.6%; denominador = población identificada por auditoría, no el total del source) |
| wrong_claim_rate | **0.50%** (4/803) | labels WRONG / claims auditados |
| overgeneralized_rate | **0%** (0/803) | |
| material_missing_count | **19 proposiciones** (10 ventanas rechazadas; 0 en aceptadas) | |
| rejected_windows_with_material_loss | **10/26** (38.5%) — todas PARCIAL; 0 MATERIAL_LOSS | |
| grounding_false_negative_rate | **17.5%** (14/80 non-supported); recuperable total 66/80 | |
| grounding_false_positive_findings | 2: 1/30 en muestra de claims + 1/112 en relations aceptadas | |
| identity_false_merge_count | **0** | |
| identity_false_split_count | **2 confirmados** (+2 AMBIGUOUS fail-closed contractuales) | |
| relation_correct_rate | **96.9%** (126/130) | |

## Conclusión P1

El conocimiento canónico del capítulo es de alta calidad material: las reglas de trading centrales están 100% correctas y el capítulo no pierde ninguna ventana material completa. Los defectos reales son de **plomería semántica y operación**, no de correctitud del contenido: (1) 66/80 records no-soportados recuperables por citación de evidencia truncada y garbles de ASR; (2) inestabilidad de clasificación (kind/epistemic) que produce rechazos de ventanas byte-idénticas y fragmentación del store; (3) 4 claims WRONG materiales (0.5%) con causa ASR/lectura visual fina; (4) 2 fatales de provider mal clasificados que matan el run; (5) L2 estrangulado por timeout de 120s en catálogo de ~30k tokens; (6) 3/5 degradaciones COMPOSITE sobre-estrictas; (7) 19 proposiciones materiales residuales en 10 ventanas rechazadas.

STATUS = FINDINGS (sin stop conditions). NEXT_PHASE_AUTHORIZED = YES.
