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
updated: "2026-09-22"
---
# F — Decision Register — 22-09-2026 final owner clarifications

## CLOSED — producto confirmado por Rodrigo
| ID | Decisión | Alcance |
|---|---|---|
| P01 | The Lab V3 será sección Echo; base única durable de operaciones y N curvas derivadas + métricas/dashboard/screener; luego money management/portfolios | Ratificado |
| P02 | Tres periodos EXACTOS: TRAINING_DATA SQX, PRE_REAL MT5, REAL Echo Reference; DOS fechas configurables en importación Forge→Echo | Ratificado |
| P03 | Clasificar pertenencia exclusivamente por `opened_at` probado. Cierre posiciona realización del resultado, nunca pertenencia | Ratificado; resuelve contradicción A vs D/E/F anterior |
| P04 | Fecha A es última fecha usada por dataset de entrenamiento Forge, NO selección/promotion; si es día civil, include día y convertir al primer instante posterior | Ratificado semánticamente; precisión/timezone en SPEC diaria |
| P05 | Forge inserta/entrega operaciones SQX+MT5 como base histórica; Echo normaliza/persiste/calcula; journal es autoridad FULL ECHO, solo leído por Lab | Ratificado |
| P06 | Histórica una sola base oficial; reimport manual destruye/reemplaza dataset analítico tras validación atómica, sin conservar cadena permanente de HistoryRevision/Publication. No borrar originales Forge ni journal | Ratificado |
| P07 | Preferencia modelo minimalista canonical operations + curves. TradeSet/HistoryRevision/HistoryPublication NO nuevos objetos de producto obligatorios; evitar dos autoridades persistentes | Ratificado como arquitectura conceptual; compatibilidad específica E05 en SPEC |
| P08 | No BWC ni paridad V1/V2 como razón para conservar legacy; cleanup incluye tablas, código, jobs, vistas y front; journal/runtime intocables | Ratificado |
| P09 | Jornada 23–27: planificación técnica profunda al empezar cada día, luego desarrollo/pruebas/corrección a gate; dashboard auténtico viernes, REAL job sábado, screener E2E domingo | Ratificado como objetivos; no garantías de certificación |
| P10 | N algoritmos Go para curvas y bases R_PIPS/R_MONEY/pips/money según evidencia; detalles de algoritmos a iterar. Riesgo sizing separado de señal entry/SL/TP; candle/intrabar futuro | Ratificado |
| P11 | Uso futuro: money management múltiple, portfolios research y ejecución/asignaciones, dashboard y limpieza legacy explícita en roadmap general | Ratificado |

## TECH — concretar en SPEC diaria, no bloquear roadmap completo
| ID | Decisión pendiente puntual | Fecha/hito responsable |
|---|---|---|
| T01 | DDL, PK/unique, metadata de import/StrategyVersion A/B, source payload y checksum, treatment de corrected journal rows; disposición efectiva E05 PG063 y consumidores E10 para UNA autoridad, sin dual write | D1 23/09 |
| T02 | Fecha input A/B exacta (date inclusive vs timestamp), timezone y evidencia UTC; SL/TP/pips/risk/currency disponibles de candidato real, reglas de crossing para métricas segmentadas | D1/D2 |
| T03 | Forma de exponer listas individuales reales SQX/MT5 en F04/E04 versión wire/capability, original hashes/counts, partición temporal cuando fuentes no cubran PRE_REAL | D1/D2 |
| T04 | CurveAlgorithm descriptor, basis, storage points, fingerprint/invalidation, primeras fórmulas verificables R_PIPS/R_MONEY; no modelar todas las gestiones monetarias | D3 |
| T05 | Journal watermark y detección corrección/timer/freshness, mapping Reference/version, prueba no mutation; ausencia de Reference real => bloqueo físico honesto | D4 |
| T06 | Screener: misma basis, currency, ventana y fórmula; DQ de conjuntos; gate final E2E y mapa de consumidores legacy para cleanup | D5 |
| T07 | Plan de destrucción legacy: objetos LAB_ONLY, SHARED, UNKNOWN y DROP autorizado después de V3 usable; exportar única evidencia si existe, journal/Core preservados | Inventario D1–D5; ejecución L-CLEAN inmediata post D5 |

## Evidencia que aún NO está certificada
- Dos listas individuales SQX/MT5 con ventanas correctas del MISMO finalista F05-C: certificación Forge FULL + 5 E04 handoffs auténticos NO lo prueban. D1 lee una muestra y D2 verifica productor/consumer.
- Nuevos DDL, job V3, curva V3 y UI V3 NO implementados por esta sesión. No confundir documentos, source, DEV, PROD y capital.
- La arquitectura E05 S0/TradeSet actual es distinta del modelo operativo simple: adaptación/migración de autoridad, no borrar PG063 antes de localizar consumidores y recuperar bytes necesarios.
- E10 M7 pendiente revisión separada; no avanzar T06–T10 por inercia ni bloquear Lab.

## Gate
Owner ratificó producto, fechas/apertura y estrategia anti-legacy. No esperar otra aprobación global antes de planificación D1; decisiones técnicas exactas las toma manager+owner en la apertura diaria y se documentan en SPEC. No requiere GOD ni nueva auditoría integral. Roadmap operativo [[D — Revised Roadmap]].
