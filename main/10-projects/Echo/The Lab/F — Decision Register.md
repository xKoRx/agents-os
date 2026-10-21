---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[A — Product Contract — The Lab]]"
  - "[[B — Architecture Decision Report]]"
  - "[[D — Revised Roadmap]]"
tags: [kind/doc, area/echo]
created: "2026-09-22"
updated: "2026-10-20"
---
# F — Decision Register — owner clarifications and D1 decisions

## V4 — Owner ratifications 2026-10-20 (current product authority)

**Project:** [[Echo — Producto Integrado]] / The LAB V4. **Design evidence:** [[THE_LAB_V4_Diseno_para_revision]] (Shot 1 GOD, 2026-10-20; source artifact preserved). **Authority:** Owner's explicit confirmation on 2026-10-20. These four decisions **supersede conflicting V3 specifications** below; prior ratifications remain historical evidence, not instructions to implement V3 over V4.

| ID | Status | Ratified decision | Required interpretation |
|---|---|---|---|
| D09 | **OWNER_RATIFIED** | Virtual initial capital **10,000** and **1%** risk preset, **configurable**. | `normalized_10k_open_balance.v1`: each operation's virtual risk budget is sealed at opening from the realized virtual balance causally known at that time; no future PnL for sizing. The 1% preset is **not** an operational Echo account/prop risk rule, nor an aggregate exposure cap. Explicitly version the separate initial-balance profile. |
| D10 | **OWNER_RATIFIED** | **Cycle's risk budget proven and sealed when the Operation opens** is the R denominator. | `Q_i > 0` must be source-supported, scoped to the **whole logical cycle**, including possible later adds. Do not infer it from the first entry SL, final SL, realized loss or contemporary MM config; if absent or unsuitable, R and risk-normalized curves are `INSUFFICIENT_DATA`. Do not silently recompute Q_i when exposure changes; any later breach or change in actual risk does not retroactively rewrite its initial normalization basis. |
| D11 | **OWNER_RATIFIED** | **Separate capital per portfolio member**, fixed initial weights, and **flat start**. | No shared financing, loans, margin simulation or implicit rebalance in I1. Initial capital apportioned by member weight; weight sum <= 1, remainder cash. Entries before `composition_start_at` do not earn in a newly flat-initialized portfolio. |
| D16 | **OWNER_RATIFIED** | **Real strategy-version construction date `construction_at`** determines the pre/post construction boundary. | Preserve `construction_data_cutoff` separately as evidence of the last training-data date; do not use it as a substitute for `construction_at`. Preserve `available_at` and `echo_reference_started_at` as distinct time dimensions; never infer unknown timestamps from receipt/import date. |

### V4 authority and conflicts with V3

- **V3 P02/P04 / Echo Integrated Product old "A" boundary**: its cutoff at end of training dataset was the V3 period classifier. **SUPERSEDED for V4 classification** by D16. Training cutoff remains metadata, not the boundary.
- **V3 D1-M01/M07/M08/M09**: one closed trade = one row, no partial fills/OPEN cycles and mandatory TP were V3-scoped constraints. **SUPERSEDED as V4 schema restrictions**. The new model accepts multi-order/partial-fill/movement evidence, open/terminal cycles and different granularity. A CLOSED_SUMMARY remains valid when detailed evidence is absent, but is never added again to its movements.
- **V3 D1-M04/M11**: Echo owns canonical history/identity; Forge supplies a normalized input without writing directly to Echo PG. **RETAIN compatible authority boundary**; V4 extends it to multiple histories, origins and contexts.
- **D09 + D10**: the virtual 1% budget and the Operation's historical `Q_i` have different purposes. The former sizes an *analytical normalized curve*, the latter normalizes the actual cycle's result. Neither authorizes trading or silently enforces prop risk.
- **D11**: static portfolio is retrospective analysis, **not** causal portfolio-selection backtesting, shared capital simulation or live allocation.

### Manager review / freeze gate

- `OWNER_PRODUCT_DECISIONS_D09_D10_D11_D16 = FROZEN` as of 2026-10-20.
- `SHOT1_DESIGN = REVIEWED_WITH_CONDITIONS`; **not** `FROZEN` or `READY_FOR_UNRESTRICTED_IMPLEMENTATION` yet. The Shot 1 source explicitly requires resolution/verification of G.2 technical facts before freezing an implementation-ready contract.
- `D12–D15 = MANAGER_TECHNICAL_DIRECTION_ACCEPTED_FOR_PREFLIGHT`, **not Owner ratifications nor final technical freeze**: PostgreSQL+bounded worker; versioned API/CAS; input-retention and exact revision manifests; explicit-evidence copy comparisons.
- `TECHNICAL_PREFLIGHT_OPEN = U01–U06 + A01/A02`: emitted strategy-version/MM/risk lineage; complete historical retention/rebuild; real history size and delivery shape; numeric SLOs/hardware; consumers of generic naming and migration constraints; real deployment/test posture, source artefact preservation.
- **Gate:** request bounded LOCAL preflight and record evidence plus revised complete SPEC; manager/Owner accept scope and technical freeze before editing dependent production code. No new Owner product interview is required unless a verified material contradiction arises.
- **Source-of-truth status:** original V4 design artifact is kept unchanged as proposed design; this decision register is the ratified Owner delta. Do not mistake the source artifact's `READY_FOR_OWNER_REVIEW` label for freeze approval.

---

## CLOSED — producto confirmado por Rodrigo el 22-09
| ID | Decisión | Alcance |
|---|---|---|
| P01 | The Lab V3 será sección Echo; base única durable de operaciones y N curvas derivadas + métricas/dashboard/screener; luego money management/portfolios | Ratificado; precisión de ownership en D1-M04 |
| P02 | Tres periodos EXACTOS: TRAINING_DATA SQX, PRE_REAL MT5, REAL Echo Reference; DOS fechas configurables en importación Forge→Echo | Ratificado |
| P03 | Clasificar pertenencia exclusivamente por `opened_at` probado. Cierre posiciona realización del resultado, nunca pertenencia | Ratificado; resuelve contradicción A vs D/E/F anterior |
| P04 | Fecha A es última fecha usada por dataset de entrenamiento Forge, NO selección/promotion; si es día civil, include día y convertir al primer instante posterior | Ratificado semánticamente; precisión/timezone en SPEC diaria |
| P05 | Forge inserta/entrega operaciones SQX+MT5 como base histórica; Echo normaliza/persiste/calcula; journal es autoridad FULL ECHO, solo leído por Lab | Ratificado; D1-M04 precisa ingestión como recurso Echo, sin API de escritura Lab |
| P06 | Histórica una sola base oficial; reimport manual destruye/reemplaza dataset analítico tras validación atómica, sin conservar cadena permanente de HistoryRevision/Publication. No borrar originales Forge ni journal | Ratificado; D1-M04 precisa ownership de la base en Echo |
| P07 | Preferencia modelo minimalista canonical operations + curves. TradeSet/HistoryRevision/HistoryPublication NO nuevos objetos de producto obligatorios; evitar dos autoridades persistentes | Ratificado como arquitectura conceptual; D1-M04 desplaza operaciones a Echo y E05 deja de gobernar el nuevo modelo |
| P08 | No BWC ni paridad V1/V2 como razón para conservar legacy; cleanup incluye tablas, código, jobs, vistas y front; journal/runtime intocables | Ratificado |
| P09 | Jornada 23–27: planificación técnica profunda al empezar cada día, luego desarrollo/pruebas/corrección a gate; dashboard auténtico viernes, REAL job sábado, screener E2E domingo | Ratificado como objetivos; no garantías de certificación |
| P10 | N algoritmos Go para curvas y bases R_PIPS/R_MONEY/pips/money según evidencia; detalles de algoritmos a iterar. Riesgo sizing separado de señal entry/SL/TP; candle/intrabar futuro | Ratificado |
| P11 | Uso futuro: money management múltiple, portfolios research y ejecución/asignaciones, dashboard y limpieza legacy explícita en roadmap general | Ratificado |

## CLOSED — decisiones owner D1 23-09, entrevista modelo
| ID | Decisión ratificada | Consecuencia obligatoria |
|---|---|---|
| D1-M01 | Una fila por trade completo (alternativa A), no una fila por deal ni realización parcial | Diseñar identidad de trade estable; si la fuente ofrece deals, agregarlos sólo con evidencia completa y sin PnL duplicado. Política exacta de cierres parciales aún es detalle técnico de SPEC, no licencia para inventarlos. |
| D1-M02 | Dos estrategias distintas son dos historias distintas. En REAL procesar exclusivamente trades REFERENCE; operaciones de cuentas/copy EXECUTION quedan fuera de D1–D4 y servirán después para slippage/fidelidad | Sin merge entre cuentas/copies ni inferir estrategia por cambio de cuenta; identidad StrategyVersion explícita. |
| D1-M03 | Ingesta estricta: trade con error o campos requeridos ausentes falla; no aceptar operaciones degradadas para fabricar curvas. Header de curva debe tener estado ante error | Definir conjunto mínimo de campos efectivamente requeridos según uso. No exigir ni crear columnas especulativas; fuentes incompletas no obtienen PASS; curvas no se calculan sobre input inválido. |
| D1-M04 | Operaciones canónicas y estrategia/historia pertenecen a Echo; The Lab es subproducto consumidor con ownership exclusivo de curvas/derivados | Forge inyecta estrategia con historia mediante servicio Echo, jamás escribe Lab ni PostgreSQL directamente. El nombre lógico `lab_operations` de A/B/D anteriores queda SUPERSEDED: proponer `echo.canonical_operations` o equivalente en SPEC. Una sola autoridad durable de operaciones, no segunda escritura E05 TradeSet. Echo journal continúa autoridad operacional y fuente de Reference. |
| D1-M05 | Modelo canónico S0 debe modificarse/definirse completo desde necesidades de todos los productores (Forge, journal y futuros), sin diseñar alrededor de E05 actual | E05 no gobierna modelo V3 ni se conserva por obligación; preservar sólo datos y consumidores realmente necesarios mientras se hace convergencia segura. S0 se extiende o sustituye versionadamente según contrato aprobado. |
| D1-M06 | KISS: columnas y tablas sólo para atributos realmente usados; provenance/trazabilidad/calidad no son subsistemas por defecto. Modelo consultado y actualizado con frecuencia y volumen creciente | Evitar JSONB como almacenamiento central de campos consultables, evitar tablas de import/calidad/revisiones sin necesidad demostrada; DDL e índices se ratifican en la SPEC. |
| D1-M07 | La base canónica persiste sólo trades CERRADOS (alternativa A). No se almacenan operaciones abiertas en canonical_operations | El worker REAL incorpora Reference sólo después del cierre. No hace falta state/lifecycle en la fila canónica D1. |
| D1-M08 | Cierres parciales no forman parte del modelo V3 inicial (alternativa A): 1 operación = 1 cierre = 1 trade = 1 row | Si una fuente representa un trade mediante más de una realización/fila y no puede producir inequívocamente un único trade cerrado, el ingreso falla. No se agrega tabla de deals ni legs. Curvas no deben calcularse sobre ese input; su header debe reflejar ERROR/INVALID_INPUT. TP y SL forman parte obligatoria del trade canónico. |
| D1-M09 | En V3 inicial `take_profit` es obligatorio aunque el dominio futuro pueda admitir estrategias sin TP | `take_profit NOT NULL` en el contrato/DDL inicial. Si más adelante se habilitan estrategias legítimas sin TP, se versiona el contrato; NULL no se usa como sinónimo de dato faltante. Nota técnica: el cálculo de R depende del riesgo inicial/SL y del resultado realizado, no matemáticamente del TP; TP se conserva porque es parte de la señal y del contrato actual de estrategia. |
| D1-M10 | Echo conoce sólo símbolos canónicos; canonical_operations y Lab heredan esa autoridad | El flujo de ingestión debe resolver/solicitar el símbolo canónico al inicio y persistir sólo ese identificador. No se guardan aliases/broker symbols en canonical_operations ni se crea instrument mapping dentro de Lab. Un símbolo no canónico/no resoluble falla antes de persistir trades. |
| D1-M11 | Forge adapta sus fuentes al contrato canónico de Echo; Echo valida y persiste. Echo NO conoce formatos SQX/MT5 | El SDK/contrato compartido expone el DTO de operación/historia requerido por Echo. Cada productor resuelve internamente cómo obtenerlo. No entran parsers SQX/MT5 al dominio Echo. |
| D1-M12 | D1 es Echo-first. Forge continúa por carril de desarrollo independiente y consume las definiciones publicadas por Echo | El gate D1 no depende de inspeccionar ni corregir implementación Forge. Echo entrega modelo base, contrato, servicio de integración, persistencia y tests de contrato. La certificación física Forge→Echo ocurre al converger ambos carriles, sin trasladar deuda Forge a Echo. |

**Estado de la sesión:** M01–M12 ratificadas y registradas. NO constituyen aprobación del DDL, contrato wire completo, implementación, pruebas o gate D1. La entrevista del modelo sigue abierta. El contenido previo de A/B/D/E que sitúe `lab_operations` bajo Lab o haga de E05 prioridad de reutilización queda superado por D1-M04/M05; actualizar esos documentos al concluir planificación aprobada, no presentarlos como autoridad vigente sobre ownership.

## TECH — concretar en SPEC diaria, no bloquear roadmap completo
| ID | Decisión pendiente puntual | Fecha/hito responsable |
|---|---|---|
| T01 | DDL de `echo.canonical_operations` (nombre sujeto a SPEC), PK/unique, metadata A/B y vínculo a StrategyVersion, tipos mínimos, reemplazo atómico, tratamiento de correcciones journal, disposición de PG063/consumidores E10 sin dual-write; no crear import/quality tables por inercia | D1 23/09 |
| T02 | Input A/B exacto, timezone y evidencia UTC; campos realmente requeridos para trade COMPLETO y curvas previstas; cierres parciales que origen entregue, cruces y comportamiento fail-closed | D1/D2 |
| T03 | Contrato público Echo para historia TRAINING/PRE_REAL: DTO, A/B, counts/digest de dataset, idempotencia/reemplazo y estados de respuesta. Forge implementa su productor en carril independiente; evidencia física SQX/MT5 se exige en el gate de integración, no para cerrar foundation Echo | D1 contrato / D2 integración |
| T04 | Header de curva con estado de error, CurveAlgorithm descriptor/basis, puntos, fingerprint, invalidación y primeras fórmulas demostrables | D3; estado obligatorio D1-M03 |
| T05 | Journal READ ONLY, Reference/version, watermark/correcciones/timer/freshness, sin copies ni mutation | D4 |
| T06 | Screener: misma basis/currency/ventana/fórmula; DQ de conjuntos; gate final E2E y mapa consumidores legacy | D5 |
| T07 | Destrucción legacy: clasificar objetos LAB_ONLY, SHARED, UNKNOWN, DROP autorizado tras V3 usable; no tocar journal/Core | Inventario D1–D5; ejecución L-CLEAN post D5 |

## Evidencia que aún NO está certificada
- La conformidad física de Forge con el nuevo contrato Echo (TRAINING/PRE_REAL auténticos) aún no está certificada. Es riesgo de integración, no bloqueo para diseñar/implementar la foundation Echo.
- No hay nuevo DDL, job V3, curva V3 ni UI V3 implementados o probados por esta sesión.
- E05 PG063 y consumidores E10 deben localizarse antes de retirar datos que pudieran ser su única copia, pero no tienen derecho de veto arquitectónico ni se mantienen como segunda autoridad.
- Branches locales/worktrees y operaciones físicas del candidato aún no verificados.

## Gate
Planificación D1 en curso, decisiones M01–M12 cerradas. `D1_PASS` exige SPEC/contrato Echo aprobados, migración DEV, servicio de ingestión Echo, persistencia/readback mediante tests de contrato y ausencia de impacto trading. La operación auténtica Forge queda para el gate de integración D2; no se usa un productor incompleto para deformar el modelo Echo. Ninguna actividad de código, migración, PROD o trading autorizada durante la entrevista. No cerrar sesión Agents-OS antes del cierre explícito solicitado al terminar planificación aprobada. Roadmap operativo [[D — Revised Roadmap]] sujeto a las precisiones D1 ratificadas.
