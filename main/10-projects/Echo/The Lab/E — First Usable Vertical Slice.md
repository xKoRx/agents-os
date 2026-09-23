---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[D — Revised Roadmap]]"
  - "[[A — Product Contract — The Lab]]"
  - "[[B — Architecture Decision Report]]"
tags: [kind/doc, area/echo]
created: "2026-09-22"
updated: "2026-09-22"
---
# E — First Usable Vertical Slice — daily execution contract

**Implementación planeada 23–27/09/2026; aún NO realizada.** Una estrategia auténtica Forge debe atravesar el E04 existente con dos listas por trade y terminar con curva visible en DEV; REAL se incorpora en la MISMA semana desde el journal Echo, no como etapa distante. Autoridad de producto [[A — Product Contract — The Lab]], plan por día [[D — Revised Roadmap]], gaps [[C — Reality and Gap Matrix]].

## Alcance fijo y responsabilidades
- Forge: recuperar un finalista auténtico FULL, SQX per-operation training, MT5 per-operation pre-real, refs/hash/rangos, versión, timezone y metadata IS/OOS. Ajustar exporter y handoff F04 en paralelo si la forma actual no entrega listas; no volver a investigar todo Forge. No calcular curvas Lab.
- Echo: extender el ingreso E04 existente, normalizar en `lab_operations` PG como UNA autoridad, aplicar A/B por `opened_at_event`, servir lectura, algoritmo Go de curvas, job periódico Reference del journal con SELECT, UI, calendario y screener. Ningún otro servicio, mongo mirror o write directo Forge→Echo.
- Owner: decide A/B para cada importación y acepta gate de experiencia DEV. No activar Reference/trading automáticamente por import. PROD necesita autorización adicional.

## D1 contrato y persistencia (MIÉ)
Al inicio: pin Git heads y revisar exclusivamente rutas E04/S0/E05, Forge exporter real, PG ordinal migraciones, source fields de journal. Ratificar SPEC/DDL mínimo: config A/B, `lab_operations`, `lab_curves`, point storage y job checkpoint (la estructura de curvas puede migrarse D3); qué contratos TradeSet E05 quedan wire-only/transitorios y qué consumidores se adaptan; no doble authority. Corte A fecha civil inclusive transformada a frontera exclusiva con timezone declarado; B instante de inicio. D1 gate: fila auténtica Forge insert/read, migración DEV y esquema compartido pinneado. Faltan dos listas? registrar ID/ref/formato exacto y continuar trabajo independiente; no fake PASS.

## D2 ingestión dual (JUE)
Forge expone ambas listas trade-level. Echo verifica bytes/hash y metadatos contra versión, parsers de frontera, extrae operaciones completas y selecciona SQX opened_at<A, MT5 A<=opened_at<B. Descarta/excluye fuera de rango con conteo, no los duplica. Pipeline de reemplazo: stage→validate→short transaction visible replace→dirty curves; si error previo/commit, lectura anterior intacta. Identidad stabile y mismo import replay idempotente. D2 gate: exact counts y dos fuentes con operaciones reales, consulta calendario/open-close por estrategia, no modificación del journal ni trading, E04 original PASS.

## D3 curva visible (VIE)
Interfaz simple compilada `CurveAlgorithm` y registry por id/version, config/basis explícita, inputs fingerprint, puntos con tiempo de cierre y contribution refs; primero R_PIPS/R_MONEY o pips según evidencia, no forzar valores desconocidos. Calcular desde dataset seleccionado y guardar derivados reconstruibles; pruebas determinismo y change-config invalidation. Front reutiliza sólo contenedor útil y chart con eje temporal real, A/B, versión/estrategia, fuente y métricas mínimas. D3 gate: visualización real en DEV, dos puntos rastreables a operaciones y recálculo idéntico sin reimport; no gráfico fake de fixture agregado.

## D4 actualización desde journal (SÁB)
Revisar job actual read-only antes de tocar: `recompute.go` antiguo borra canonical/outcomes y usa recorded time + R AUTO; `materialize_curves.go` reemplaza puntos legacy; `canonical_a0.go` crea Scope BACKTEST/SQX sobre filas Reference. No usar lógica vieja como V3. Worker reusa CLI/timer/log `lab_job_runs` sólo; job nuevo SELECT journal Reference→map version/time provenance→UPSERT lab_operations REAL→recalc affected curves→metrics; checkpoint por updated/recorded e ID, idempotencia y recuperación tras crash. Data gaps UNKNOWN, B pendiente implica REAL no iniciado. UI calendario/trade detail y freshness. D4 gate: operación existente auténtica Reference aparece una vez; replay idem, journal checksum/rows sin cambio, curvas actualizadas y timer sin silencio.

## D5 producto y housekeeping inicial (DOM)
Dashboard integrado, screener con bases comparables, fechas, filtros/trades/calendar, DQ y errores, cobertura, sin win_rate mal mostrado ni USD inventado. E2E una estrategia FULL dual history, job REAL verificable, E04 original no regresión, import fallido conserva histórico anterior, mismo digest no duplica, algo nuevo invalida curvas, no activa trading. Medir import/recompute/UI, guardar refs/hash/SQL count/SHAs y estado. Inventariar todas las rutas legacy para L-CLEAN, retirar shell/components no usados V3 durante semana; limpieza SQL final después con mapa de consumidores y migración DEV. No declarar PROD desplegado ni datos reales de un finalista no revisado.

## Reglas de pruebas y fallos
- Datos reales obligatorios para aceptación E2E; tests sintéticos sólo unit/negativos. Con fuentes incompletas un gate es BLOCKED con pregunta/evidencia exacta, no reemplazar por datos generados.
- Tiempos: pertenencia OPEN, posición de punto CLOSE, `[start,end)` y timezone probado, crossing marcado y never PnL split. Sin timezone verificable no imputar EventTime UTC ni publicar historia como exacta.
- Curvas se recalculan desde `lab_operations`; fingerprint completo de inputs. Algoritmos declararán status INSUFFICIENT cuando risk/pip/currency falta. No mezclan Execution con Reference ni performance de cuenta con estrategia.
- Una única migración owner por rango, evitar colisiones de E04 recovery/E10 068/069. DEV aislado; migraciones y tests jamás escriben ETCD PROD; backup/export de fuentes originales requerido para cleanup, no fake paridad legacy.

## Cierre por jornada
Plan acotado mañana→implementación→tests→corrección→gate→evidencia→session close y feedback. Si falla un hito, no marcar PASS; plan de día siguiente reubica el gap crítico sin terminar en auditoría general. Los siguientes módulos están en [[D — Revised Roadmap]]: L-CLEAN, money management, portfolio research/apply/monitoring y candle replay futuro.
