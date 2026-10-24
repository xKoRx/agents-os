---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/strategies/STRATEGIES-CATALOG|STRATEGIES-CATALOG (canónico)]]
aliases:
  - clutifx strategies master
  - investigación estrategias clutifx
tags:
  - kind/doc
  - area/echo
  - tech/strategy-research
created: "2026-10-23"
updated: "2026-10-24"
---

# CLUTIFX-STRATEGIES-MASTER — Vista de investigación backtester (Clutifx)

**El catálogo canónico e interable de las estrategias del curso vive EN la biblioteca de conocimiento**: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/strategies/STRATEGIES-CATALOG|clutifx/strategies/STRATEGIES-CATALOG.md]] (re-domiciliado ahí el 2026-10-24 por decisión del Owner: el knowledge es la superficie que mejora con el tiempo y el catálogo evoluciona con ella; contrato de iteración en su encabezado). Ese catálogo contiene: el sistema en una página + checklist de 4 preguntas, glosario literal, 24 componentes, 5 familias con 9+1 estrategias completas (fichas con setup claro), 7 setups parciales, 13 reglas de gestión, 4 red flags, el procedimiento de análisis, exclusiones honestas y los casos límite de clasificación documentados.

**Este documento es la capa de investigación del backtester** que consume ese catálogo: objetivización, clasificación NQ, matriz experimental y evidencia. Nada de esta capa modifica el conocimiento del curso; los detectores `[OP]/[HIP]` son operacionalizaciones e hipótesis propias, nunca enseñanzas Clutifx.

## 1. Clasificación NQ / datos / runtime (autoridad de esta capa)

| Estrategia | Clasificación | Detalle |
|---|---|---|
| STR-001 London ideal | `NQ_ADAPTATION_HYPOTHESIS` | Ancla de sesión FX (vela de la 1) debe mapearse a sesiones CME como hipótesis |
| STR-002 Pendiente a DOL | `NQ_DIRECTLY_TESTABLE` | Estructural; único eje a fijar: TF del objetivo |
| STR-003 NY continuación | `NQ_ADAPTATION_HYPOTHESIS` | Ancla 9:00 NY → propuesta NQ 9:30 ET open |
| STR-004 NY reversal | `NQ_ADAPTATION_HYPOTHESIS` | Ancla vela de las 5 |
| STR-005 Refinado | `NQ_DIRECTLY_TESTABLE` | Procedimiento estructural; escala de TFs = eje (tensión fuente 15m vs 5m declarada en el catálogo) |
| STR-006 Failure swing | `NQ_DIRECTLY_TESTABLE` (motivos b; a multi-instrumento; c inaplicable single-feed) | ε de nivel y fracción final de vela = parámetros |
| STR-007 SMT | `MULTI_INSTRUMENT_DATA_REQUIRED` + `FX_NATIVE` fiel | Sin 2º instrumento en corpus; NO trasladar EUR/GBP |
| STR-008 Noticias | `NQ_ADAPTATION_HYPOTHESIS` + `RUNTIME_GAP` (calendario) | Noticias USA mueven NQ; falta feed de calendario |
| STR-009 Reentrada intra-TS | `NQ_DIRECTLY_TESTABLE` | Requiere intrabar (1m mínimo) |

Datos disponibles (auditados en `HEFESTO-BASELINE-AUDIT.md`): NQ físico 2023-10→2026-10, barras 1m Last, 672 sesiones elegibles; **sin ticks**; sesiones CME America/Chicago 17:00→16:00; fees 2.49/lado, slippage 1 tick. Consecuencias: (a) todo lo intrabar se resuelve a 1m como máximo (la "reacción" del TS y el P3 intrabar se aproximan por velas 1m — cota de fidelidad declarada); (b) horas FX del curso (UTC-4 NY) se anclan a `America/New_York` con DST real, no offset fijo; (c) velas 3h/5h/etc. off-grid se componen desde 1m con anclaje a la hora NY dicha.

**Frontera Strategy/MM de Echo**: toda la gestión del catálogo §5 (parciales/BE/pirámides/riesgo%) pertenece al plano MM/policy (tgmm/gerardmm hoy: `NO_ADDS`, `STRATEGIC_ENTRY_BUDGET_V1`); las estrategias Clutifx emiten señales + stop técnico + objetivo estructural (DOL), igual que ORB emite su evento de add técnico que el MM decide económicamente. Sin gaps de runtime para STR-002/005/006/009; STR-008 requiere feed de calendario (gap declarado).

**Nota de taxonomía** (decisión Owner 2026-10-24): PDM/OB podrían elevarse a familia propia bajo una taxonomía por detonante; el catálogo canónico documenta el caso límite en su §10.1 — sin pérdida de información en ninguna de las dos formas.

## 2. Documentos de esta capa

- `CLUTIFX-OBJECTIVE-DETECTORS.md` — 16 familias de detectores (NATIVO/[OP]/[HIP]) con fórmulas, causalidad, lookahead, parámetros.
- `CLUTIFX-EXPERIMENT-MATRIX.md` — 34 IDs / 35 sustituciones en 3 tiers, equivalencias, plan de validación F (correctness-first), bloqueos.
- `CLUTIFX-SOURCE-COVERAGE.md` — mapa capítulo→catálogo + exclusiones consolidadas (la cadena de trazabilidad fina vive en `compiled/COVERAGE.md` de la biblioteca).
- `HEFESTO-BASELINE-AUDIT.md` — estado físico del backtester, inventario 89, recibos, datos, Gate A.
- `QA-VERIFICATION.md` — revisión adversarial independiente de la misión (80 claims materiales: 74 PASS / 1 FAIL recalificado y corregido / 5 UNKNOWN; H1–H7 PASS; 0 defectos MATERIALES, 8 MENOR corregidos). Nota: el QA verificó el contenido del catálogo cuando vivía en este directorio; ese contenido se movió íntegro a la biblioteca — los hallazgos y correcciones aplican igual.
- `HANDOFF.md` — estado final, estadísticas, cosas vivas, próximos pasos.
- `mining/` — 12 extractos por capítulo (evidencia de segunda capa de la extracción).

## 3. Estado

`READY_FOR_CLUTIFX_IMPLEMENTATION = NO` (requiere encargo explícito + aprobación Owner de la matriz) · `EXPERIMENT_MATRIX_OWNER_APPROVAL = PENDING` · `CLUTIFX_BACKTEST_EXECUTED = NO` · `LIVE_TRADING_CHANGED = NO`.
