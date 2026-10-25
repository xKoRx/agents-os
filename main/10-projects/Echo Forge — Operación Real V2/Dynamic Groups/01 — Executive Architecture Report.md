---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-25"
updated: "2026-10-25"
---

# 01 — Executive Architecture Report

## Propósito

Explicar la evolución necesaria de Forge y sus límites verificables.

## Contenido

Forge ya posee el intérprete Temporal, ejecución declarativa, grupos, particiones por tipo, evidencias inmutables, ranking, selección y recuperación de tareas. **No posee todavía el contrato completo solicitado:** el group de ranking actual recorre una selección previa; otros caminos cuentan salidas y pueden cortar sin ordenar el acumulado. Extender ese contador sería insuficiente.

La propuesta hace que el mismo group administre un universo congelado por `logical_type`. Toma Y candidatas distintas, ejecuta todas las tareas configuradas para ellas, verifica los resultados y vuelve a rankear todas las elegibles acumuladas. Si al cerrar esa iteración hay al menos X, publica exactamente X; si no, consume el siguiente lote. No evalúa todo el universo una vez cumplido X: el Top X es sobre las candidatas evaluadas hasta ese punto, según el mandato, no una promesa de óptimo global sobre candidatas aún desconocidas.

Cada partición avanza independientemente y utiliza un presupuesto compartido de children. X e Y no dependen entre sí. Un lote final menor que Y es válido. Cero sobrevivientes no es error si existen descartes analíticos explícitos; una pérdida de resultados sin explicación sí lo es. Sólo el agotamiento demostrado habilita UNDERFILLED, incluso con cero resultados. Esa salida conserva el mismo `StratBatch`, sus bindings y su SelectionSnapshot; un segundo group la consume normalmente.

El algoritmo y sus entradas se declaran por tarea identificada y evidencia exacta. Se reutiliza el kernel `weighted_combination_minmax.v1` ya incorporado en master y el ordenamiento `score_descending.v1`. Ninguno se convierte en fórmula obligatoria. La política elige métricas, elegibilidad y comparabilidad de ventanas. No se confunde Fidelity con rentabilidad ni con ranking obligatorio.

Los bindings son opt-in por instancia. El resolver convierte una referencia exacta y un selector tipado en configuración efectiva inmutable antes de ejecutar. WFM es una implementación específica de ese contrato: selecciona el último período aplicable de la celda robusta, congela IS y digest de parámetros, Apply verifica que aplicó esos parámetros, y SQX/MT5 consumen el mismo período. Las métricas del IS son baseline optimizado de alta precisión, nunca OOS independiente.

En SQX se copia la CFX congelada, se modifican sólo los atributos `dateFrom`/`dateTo` del Setup declarado, se valida el diff, se persiste SHA y se ejecuta. Y es el lote lógico; para fechas por estrategia, la primera implementación usa ejecuciones físicas de una estrategia, secuenciales por host y distribuidas entre hosts. Conserva un worker/una activity SQX por VM; no añade locks para permitir concurrencia dentro de un host. La agrupación física compatible puede optimizarse después con pruebas, sin cambiar X/Y.

### Refactor que se justifica

1. Extraer un despachador compartido para raíz y groups: la duplicación actual explica diferencias observables, como `selection` y groups anidados que no pasan por el mismo handler.
2. Separar control del objetivo, fuente congelada y publicación de ranking: hoy source, recorte y ejecución están acoplados. No se crea otro workflow engine.
3. Evolucionar envelopes de RankingSnapshot/SelectionSnapshot a V2 para fuentes genéricas y ejecución de group. Se mantiene el kernel existente y lectura V1; cada ejecución escribe una sola versión.
4. Propagar un ledger tipado de resultados por tarea/estrategia y una configuración efectiva persistida: el carrier actual reemplaza `EvaluationRef` y no basta para recuperar cualquier productor anterior.
5. Fijar la selección de período antes de Apply y hacer readback del resultado aplicado. Evita que fechas y parámetros pertenezcan a períodos distintos.

### Riesgos y decisiones de coste

Una tabla de control por partición se justifica por CAS, cursor y recuperación; no se añade un servicio. Evidencia y listas grandes se guardan por ref en Mongo/MinIO, no en el historial Temporal. Re-rankear el acumulado evita errores con minmax cuando cambian extremos, a cambio de coste proporcional a lo ya evaluado. Date-only exige rechazar intervalos que no puedan representarse exactamente: no truncar silenciosamente horas/DST. El resultado de campañas históricas y las fórmulas V1 se preservan; las ejecuciones nuevas son opt-in y versionadas. Un presupuesto interrumpido es PAUSED/FAILED/CANCELLED, nunca UNDERFILLED.

## Fuentes

[[00 — Design Gate]], [[02 — Capability Inventory]], [[03 — Target Architecture and Decisions]], [[05 — Technical Specification]].
