---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[D — Revised Roadmap]]"
  - "[[F — Decision Register]]"
tags: [kind/doc, area/echo]
created: "2026-09-22"
updated: "2026-09-22"
---
# A — Product Contract — The Lab V3

**Contrato de producto ratificado por Rodrigo el 22-09-2026.** Las elecciones internas de SQL/API/algoritmos son propuestas técnicas y se concretan en la planificación diaria; no hay código, migración ni despliegue autorizado por este documento. The Lab es una sección de Echo, no otro proyecto. Roadmap operativo [[D — Revised Roadmap]].

## Resultado
Una estrategia/versión tiene UNA base oficial de operaciones normalizadas, durable y consistente, consumida por N curvas derivadas con algoritmos versionados, métricas, calendario, dashboard y screener. Luego se aplican diferentes gestiones monetarias a señales/operaciones y se crean portfolios dinámicos descorrelacionados para investigación y asignación a cuentas. No prometer rentabilidad ni automatizar decisiones de capital desde un ranking.

## Exactamente tres períodos, dos fechas
- A configurable en la importación = última fecha usada por dataset de entrenamiento Forge; ejemplo entrenamiento hasta 01-12-2024 inclusive. Si se ingresa una fecha civil, declarar timezone del dataset y convertir A al inicio del día siguiente UTC; también aceptar instante exacto con semántica explícita. A NO es necesariamente selección/promoción.
- B configurable = fecha de puesta en marcha/observación; puede ser PENDING hasta que se conozca. B NO se inventa por ingestión.
- Períodos según **opened_at_event** probado: TRAINING_DATA si apertura < A, fuente Forge SQX; PRE_REAL si A <= apertura < B, fuente Forge MT5; REAL si apertura >= B, fuente Reference Echo vía journal. Si B pendiente, PRE_REAL usa los datos MT5 disponibles, REAL está sin iniciar. IS/OOS/WFM viven dentro de TRAINING_DATA y conservan su proveniencia.
- Operación abierta antes del corte que cierra después: pertenece por apertura, se conserva íntegra, su resultado se dibuja al cierre y se hace visible el cruce; no se divide PnL. Definir exclusión de métricas de segmento afectado sin excluir silenciosamente de vista longitudinal.
- Una sola historia seleccionada, ningún merge de series alternativas superpuestas: cortar fuera de ventana; excluir con razón. No fabricar fechas UTC a partir de clock broker no probado. Reference/Execution y cambio de cuenta conservan identidad distinta; Execution no sustituye Reference por defecto.

## Ownership estricto
- Forge: produce dos listas reales de operaciones SQX y MT5, versión/identidad, artefactos originales y evidencia/hash, sin computar curvas oficiales Lab ni escribir PG Echo.
- Echo `trade_journal`: autoridad operacional independiente; NO se migra destructivamente, NO se reemplaza, NO se elimina. Lab consume sus filas Reference mediante lectura y job periódico. El journal no pertenece a Lab.
- Lab: UNA base activa `lab_operations` (nombre lógico sujeto a SPEC) con operaciones individuales normalizadas. Campos esenciales: identidad de fuente+operación y StrategyVersion, fecha apertura/cierre event con evidencia, fuente, instrumento/spec y dirección, entrada/salida, SL/TP iniciales y valores observados cuando existan, tamaño, pips/ticks, PnL bruto/neto, comisiones/swap/moneda, riesgo inicial en pips/dinero cuando esté probado, marca de ausencia, origen/hash, versión de import y período derivable. No inventar campos faltantes, no money default USD.
- Fechas A/B son configuración por StrategyVersion, NO duplicación de reglas almacenadas en cada fila. Dataset puede reemplazarse manualmente: cargar staging, validar y comparar conteos/hash/identidad, swap transaccional de filas visibles, invalidar derivados; si falla, base anterior sigue disponible. No crear HistoryRevision/HistoryPublication persistentes por obligación. Originales Forge y journal permiten reconstrucción; no crear almacenamiento permanente de revisiones anteriores en Lab.
- Curvas son DERIVADOS: algoritmo id/versión, configuración digest, basis/unidad, fingerprint exacto del dataset, operaciones incluidas/excluidas y puntos/contribuciones. Métricas derivadas con fórmula y basis declaradas; screener sólo consume datos compatibles. Puntos pueden tener tabla física propia sin representar nueva autoridad.

## Actualización REAL
Lab worker existente lee journal periódicamente con checkpoint por incorporación/actualización, no sólo opened_at; idempotencia por identidad estable, corrección bajo reinserción validada, journal inalterado; nuevas operaciones modifican la base durable y disparan actualización/reconstrucción de curvas afectadas. Sin resultados observados suficientes se muestra UNKNOWN, no cero. No automatizar recuperación extraordinaria: owner la encargará manualmente a un agente si sucede. Incorporación continua no depende de finalizar elegibilidad E10.

## Calidad de estrategia y políticas monetarias
N curvas: R_PIPS, R_MONEY, pips/ticks, dinero y capital virtual según algoritmos disponibles y evidencia. R depende del stop/riesgo original de la estrategia, pero no debe heredar silenciosamente lotaje de una cuenta si la curva declara calidad normalizada. Señal original Echo = entrada/SL/TP; aplicar sizing/risk policy en segunda capa. Cambiar stop/reglas reales puede cambiar identidad/versión; simulación futura de stops/entradas/salidas alternativas requiere datos de velas, NO se hace con resultado cerrado solamente. No cerrar catálogo definitivo de algoritmos en este roadmap.

## Primera experiencia y futuro
En esta semana: selector de estrategia/versión, fuente/cobertura, línea temporal por apertura/cierre con A/B, una o más curvas reales, bases R/pips cuando inputs basten, métricas mínimas, trades, calendario, screener, job REAL probado en DEV. Fecha y estado REAL visibles aun si no hay operaciones auténticas de la estrategia piloto; una operación journal existente atribuible basta para demostrar el job sin inventar flujo nuevo. Posteriormente: múltiples money management policies, curvas comparables, ranking, correlación con solapamiento temporal, PortfolioVersion/weights/constraints, assignment autorizado, ejecución/rebalance/retire, dashboard portfolio, simulación por velas futura.

## Legacy
V1/V2 NO son interfaz ni cálculo a preservar. Inventariar consumidores, cortar rutas Lab viejas, eliminar código/tablas/vistas/jobs exclusivos una vez desvinculados y resguardados los datos fuente; jamás usar limpieza de Lab para tocar trade_journal ni el runtime. La paridad con fórmulas rotas no es aceptación. Limpieza tiene hito explícito posdashboard, no deuda indefinida.
