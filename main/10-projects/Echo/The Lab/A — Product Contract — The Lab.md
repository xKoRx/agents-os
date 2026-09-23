---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[Echo — Live Platform V1]]"
  - "[[Echo Forge — Factory V2 Completion]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-09-22"
updated: "2026-09-22"
---

# A — Product Contract — The Lab

> **Estado: PROPUESTA PARA RATIFICACIÓN DEL OWNER, 2026-09-22.** Este documento no sustituye las autoridades frozen ni autoriza implementación o trading. Es un entregable de [[Echo — Producto Integrado]]; no crea un tercer proyecto. Documento complementario: [[B — Architecture Decision Report]], [[C — Reality and Gap Matrix]], [[D — Revised Roadmap]], [[E — First Usable Vertical Slice]] y [[F — Decision Register]].

## Propósito y resultado observable

The Lab es la superficie analítica central de Echo. Permite elegir una StrategyVersion, reconstruir una historia publicada única desde operaciones originales de Forge SQX, Forge MT5 y hechos observados en Echo, derivar N curvas reproducibles, calcular métricas compatibles y ofrecer un screener comparable. Los portfolios versionados y su asignación a cuentas son un endgame separado, nunca prerrequisito del primer producto. Su objetivo medible es reducir TIME_TO_USABLE_TRADING_SYSTEM, no incrementar el número de componentes. La capacidad de Forge para generar/promover y la aceptación E-04 no equivalen a historia analítica lista.

## Decisiones de producto RATIFICADAS por el mandato del owner

- Una estrategia se analiza con identidad de estrategia y versión explícitas; cambiar de cuenta no crea nueva StrategyVersion. Cambios efectivos de reglas, código, parámetros o stops que alteren la lógica requieren versionado apropiado. Una vista familiar longitudinal puede reunir versiones SOLO etiquetada como proyección multi-versión; nunca atribuye sus operaciones a una versión individual.
- Exactamente dos fechas A y B y tres períodos principales. SQX y MT5 son dos evidencias históricas Forge diferentes; IS/OOS/WFM son etiquetas internas al TRAINING_DATA, no períodos principales. Desde B, REAL se nutre de operaciones Reference efectivamente observadas por Echo. Execution es otra serie atribuible por cuenta, separada de Strategy Quality.
- Las operaciones individuales y hechos son la autoridad; curvas, métricas y rankings son derivados versionados. Fuentes originales se preservan aunque se rechacen o no seleccionen. No concatenar trade lists superpuestas ni inferir operaciones desde un reporte agregado.
- Forge produce evidencia, versiones selladas y handoffs; Echo acepta, valida, normaliza, selecciona y persiste analítica. Forge no escribe en PostgreSQL Echo ni posee curvas finales, elegibilidad, capital o activación. INGESTION ≠ disponibilidad analítica ≠ enrollment ≠ observación ≠ activación.
- No construir backtester OHLC, intrabar, recuperación histórica automática, motor genérico de portfolios, framework de plugins/DSL, microservicio analítico nuevo o ingesta macroeconómica genérica en este ciclo.

## Semántica propuesta de historia única: requiere ratificación técnica

Todas las fronteras son instantes UTC ISO-8601, no fechas locales sin offset: `TRAINING_DATA = [−∞, A)`, `PRE_REAL = [A, B)`, `REAL = [B, +∞)`, con A < B. Las horas visualizadas en America/Santiago no cambian pertenencia ni identidad. `history_revision_ref` selecciona la publicación inmutable única para `(strategy_version_ref, A, B, selection_policy_version)`; sólo una revisión tiene estado PUBLICADA para esta selección, y las anteriores permanecen consultables como auditoría, no como historias oficiales paralelas.

La operación pertenece al período determinado por `opened_at` observado, nunca por hora de importación, de recepción o por el cierre utilizado para graficar. Orden cronológico de puntos de curvas de operaciones cerradas: `(closed_at UTC, operation_ref)` estable; eje X = tiempo real. Para una operación que atraviese A o B, se conserva íntegra y se marca `CROSSES_BOUNDARY`; permanece visible en la historia longitudinal, pero se excluye de métricas estrictamente segmentadas si su realización posterior genera fuga temporal o existe evidencia parcial. No fragmentar arbitrariamente su PnL ni asumir rentabilidad cero. En B, una posición carry-in anterior a REAL no se certifica como performance REAL completa sin hechos de ciclo íntegro; la primera muestra REAL certificable comienza con entradas observadas desde B. Este es un criterio conservador propuesto, no un hecho ya ratificado.

La asignación por fuente es estricta y configurable SOLO mediante nueva versión explícita de política de selección: SQX para TRAINING_DATA con validación de límites/IS/OOS; MT5 para PRE_REAL sólo si existe lista de operaciones individuales genuina; hechos Reference Echo para REAL y `strategy_version_ref` pineada al OPEN. Solapamientos de fuentes se conservan como evidencia, nunca se suman. En caso de colisión de identidad o match económico ambiguo, cuarentena sin elegir arbitrariamente. La clave de deduplicación exige identidad nativa estable + namespace de fuente y reconciliación identificada al evento económico; coincidencia aproximada por timestamp/precio no es prueba de igualdad. Una ausencia de MT5 no permite que SQX rellene PRE_REAL por defecto.

## Contrato mínimo de operación

`NormalizedOperationV1` de Echo SDK es el wire canónico inicial; extender únicamente campos/capabilities demostrablemente ausentes y de manera aditiva, nunca fabricar defaults. Para cada operación se necesita: `operation_ref`, `strategy_ref`, `strategy_version_ref`, `economic_event_ref`/linaje nativo, `source_ref`/digest y fuente, `opened_at`, `closed_at` cuando exista, estado abierta/cerrada/parcial, instrumento y especificación de pip, side, entrada/salida, riesgo inicial documentado (distancia y/o moneda con FX documentado), PnL bruto/neto, comisiones/swap/spread si existen, moneda, volumen observado y calidad/ausencias tipadas. Señal original (entry/SL/TP) se preserva como objeto separado de la operación ejecutada si existe; SL observado no equivale necesariamente al SL inicial. `DEAL` es hecho operacional irreducible; una operación analítica reconstruida puede tener N DEALs y no los reemplaza.

Una importación tiene estados independientes: `EVIDENCE_VERIFIED` (bytes y contenido original), `INGESTED` (receipt E-04 operativo), `ANALYTICAL_HISTORY_READY` (historia publicada completa o explícitamente parcial con matriz de coverage) y `REFERENCE_OBSERVING` (hechos físicos Reference con evidencia). Estos nombres describen capacidades y no introducen enums si los estados E-04/E-06 existentes bastan. `READY` no se adjudica a un período sin trade list comprobable, cobertura ni digests. Interrupción excepcional de Echo: registrar `OBSERVATION_GAP`, conciliar manualmente con broker e incorporar corrección auditada en nueva revisión, jamás interpretar silencio como cero.

## Curvas, money management y métricas

Cada curva = `(published_history_revision, ordered operations digest, period selection, algorithm id/version, config digest, basis, unit, inputs auxiliares verificados)`; misma pregunta produce la misma referencia y el mismo content digest, o conflicto de determinismo. Los algoritmos iniciales son acumulado R, pips, equity virtual con capital inicial explícito y políticas monetarias calculables con evidencia suficiente. La curva real de cuenta usa sus deals/equity propios, no se etiqueta curva de calidad normalizada. R exige riesgo inicial probado, pips exige definición de pip/instrumento y precios/dirección, equity virtual exige capital y política de escalado; `R`, `pips`, `money` y `percent` nunca son intercambiables. Reescalar resultados cerrados sólo sirve para políticas que no alteran camino, señal, entrada/salida, costos ni restricciones de capital no modeladas; trailing, SL dinámico y salidas alternativas requieren simulación futura con mercado/path, NO disponible aquí.

MetricSet conserva identidad semántica `(key, basis, unit, formula id/version/digest, sample/window, frequency, currency cuando aplica)`, input exacto de curva + operaciones si la métrica es trade-based. Métricas candidatas: retorno, drawdown, Return/DD, PF, Sharpe, expectancy, SQN, win rate, recovery, DD actual, duración, frecuencia y cobertura. `INSUFFICIENT/UNKNOWN` son resultados explícitos; jamás convertir divisiones indefinidas, cero pérdidas, FX ausente o ventana insuficiente en cero numérico. El screener sólo ordena valores bajo mismo período, algoritmo/configuración, unidad, ventana y política de inclusión; rankings Forge/finalistas/analítica son autoridades distintas, y no predicen rentabilidad futura.

## Primer front usable y endgame

Una pantalla READ selecciona estrategia/versión, A/B y tres bandas; escoge curva, muestra puntos en tiempo real, métricas y procedencia, tabla individual, calendario por fecha de cierre y screener de cohorte comparable. Marcar creación/promoción, cambio cuenta/versión, inicio real y gaps sólo con evidencia; macroeventos contextuales únicamente si se dispone de referencia fechada comprobable. Un gap se visualiza como gap, no como línea horizontal de retorno cero.

El modelo de identidad y series temporales debe admitir después `PortfolioVersion` con miembros versionados, pesos, superposición temporal, correlaciones sobre ventanas comunes, restricciones/riesgo agregado, curvas de cartera, rebalanceo y mapping de ejecución por cuenta. Ni ranking individual ni suma ingenua de curvas no alineadas constituye cartera elegible.

## Criterios de aceptación de producto

Primer hito: una StrategyVersion auténtica de la campaña FULL pasa de SQX+MT5 con dos listas de operaciones y digest hasta Echo; una única historia A/B selecciona cada evento como máximo una vez, conserva exclusiones, produce R/pips/virtual sólo donde los inputs lo permiten, muestra curva temporal y operaciones, métricas y una comparación básica en screener. Cuando aún no hay Reference REAL, REAL aparece sin datos/UNKNOWN, nunca cero ni serie sintética. Replay conserva refs/filas, conflicto no altera datos, cambiar algoritmo recalcula sin reimportar. La certificación es física en DEV con esa misma estrategia; `SOURCE_PASS` no satisface el gate. Activar dinero real exige decisión humana independiente.

## Fuentes y límites de evidencia

- [[Echo — Producto Integrado]]; [[Echo — Live Platform V1]]; [[Echo Forge — Factory V2 Completion]]; [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] y freeze review Fable; [[Echo — E-04 Forge Ingestion E1]]; [[Echo — E-05 Analytics Convergence A0]]; [[Echo — E-10 Strategy Quality and Eligibility]].
- `xKoRx/echo@5dd998f16aea7b2821f460188718d7a6d279829c`: `specs/FEAT-FORGE-INGESTION-E1/SPEC.md`, `specs/FEAT-ANALYTICS-CONVERGENCE-A0/SPEC.md`, `v3/sdk/contracts/analytics.go`, `v3/sdk/analytics/calculator/calculator.go`. `xKoRx/symphony@745bc8b94e1f6148ddc16c02eb86a755088c2666`: factory F-05-C certificada según nota canónica fechada, NO prueba aún dual trade list por versión. Baselines son SHA de master consultados, no HEAD de features.
- No se accedió a broker, bases físicas, MinIO ni flota. La prueba de operaciones auténticas duales se planifica como primer gate, no se declara superada. Graphify no disponible en esta superficie; Markdown vía GitHub y documentos disponibles en Library. Todas las extensiones y políticas no ratificadas son propuestas.
