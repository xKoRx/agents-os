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
updated: "2026-09-23"
---
# F — Decision Register — owner clarifications and D1 decisions

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
| D1-M06 | KISS: columnas y tablas sólo para atributos realmente usados; provenance/trazabilidad/calidad no son subsistemas por defecto. Modelo consultado y actualizado con frecuencia y volumen creciente | Evitar JSONB como almacenamiento central de campos consultables, evitar tablas de import/calidad/revisiones sin necesidad demostrada; DDL e índices se ratifican en la SPEC. |\n| D1-M07 | La base canónica persiste sólo trades CERRADOS (alternativa A). No se almacenan operaciones abiertas en canonical_operations | El worker REAL incorpora Reference sólo después del cierre. No hace falta state/lifecycle en la fila canónica D1. |\n| D1-M08 | Cierres parciales no forman parte del modelo V3 inicial (alternativa A): 1 operación = 1 cierre = 1 trade = 1 row | Si una fuente representa un trade mediante más de una realización/fila y no puede producir inequívocamente un único trade cerrado, el ingreso falla. No se agrega tabla de deals ni legs. Curvas no deben calcularse sobre ese input; su header debe reflejar ERROR/INVALID_INPUT. TP y SL forman parte obligatoria del trade canónico. |

**Estado de la sesión:** M01–M08 ratificadas y registradas. NO constituyen aprobación del DDL, contrato wire completo, implementación, pruebas o gate D1. La entrevista del modelo sigue abierta. El contenido previo de A/B/D/E que sitúe `lab_operations` bajo Lab o haga de E05 prioridad de reutilización queda superado por D1-M04/M05; actualizar esos documentos al concluir planificación aprobada, no presentarlos como autoridad vigente sobre ownership.

## TECH — concretar en SPEC diaria, no bloquear roadmap completo
| ID | Decisión pendiente puntual | Fecha/hito responsable |
|---|---|---|
| T01 | DDL de `echo.canonical_operations` (nombre sujeto a SPEC), PK/unique, metadata A/B y vínculo a StrategyVersion, tipos mínimos, reemplazo atómico, tratamiento de correcciones journal, disposición de PG063/consumidores E10 sin dual-write; no crear import/quality tables por inercia | D1 23/09 |
| T02 | Input A/B exacto, timezone y evidencia UTC; campos realmente requeridos para trade COMPLETO y curvas previstas; cierres parciales que origen entregue, cruces y comportamiento fail-closed | D1/D2 |
| T03 | Dos listas individuales reales SQX/MT5 F04/E04, versión wire, digests/counts y ventanas; receipt operativo separado de estado de historia | D1/D2 |
| T04 | Header de curva con estado de error, CurveAlgorithm descriptor/basis, puntos, fingerprint, invalidación y primeras fórmulas demostrables | D3; estado obligatorio D1-M03 |
| T05 | Journal READ ONLY, Reference/version, watermark/correcciones/timer/freshness, sin copies ni mutation | D4 |
| T06 | Screener: misma basis/currency/ventana/fórmula; DQ de conjuntos; gate final E2E y mapa consumidores legacy | D5 |
| T07 | Destrucción legacy: clasificar objetos LAB_ONLY, SHARED, UNKNOWN, DROP autorizado tras V3 usable; no tocar journal/Core | Inventario D1–D5; ejecución L-CLEAN post D5 |

## Evidencia que aún NO está certificada
- Dos listas individuales SQX/MT5 con ventanas correctas del MISMO finalista F05-C: certificación Forge FULL + cinco E04 handoffs auténticos NO lo prueban.
- No hay nuevo DDL, job V3, curva V3 ni UI V3 implementados o probados por esta sesión.
- E05 PG063 y consumidores E10 deben localizarse antes de retirar datos que pudieran ser su única copia, pero no tienen derecho de veto arquitectónico ni se mantienen como segunda autoridad.
- Branches locales/worktrees y operaciones físicas del candidato aún no verificados.

## Gate
Planificación D1 en curso, decisiones M01–M08 cerradas. `D1_PASS` exige aprobación de SPEC y contrato más migración DEV y operación auténtica persistida/recuperada, identidad/provenance, veredicto sobre dual source y ausencia de impacto trading. Ninguna actividad de código, migración, PROD o trading autorizada durante la entrevista. No cerrar sesión Agents-OS antes del cierre explícito solicitado al terminar planificación aprobada. Roadmap operativo [[D — Revised Roadmap]] sujeto a las precisiones D1 ratificadas.
