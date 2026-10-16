---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[TRADESGERARD-CONTROL]]"
  - "[[TRADESGERARD-PERFORMANCE-MEMORY]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-15"
updated: "2026-10-16"
---

# TRADESGERARD-CONSOLIDATION

## Propósito

Terminar un refactor mantenible de Echo: analytics compartido, responsabilidades claras, composición modular, aislamiento y causalidad; estructura mínima para continuar iterando (SOLID/clean, KISS/YAGNI). Una campaña prueba el candidato final. El delta explícito del Owner del 16-oct elimina la certificación de campañas históricas como requisito; los resultados anteriores quedan como referencia.

## Contenido

**Estado vigente — C1–C4 cerrados y campaña funcional COMPLETE (2026-10-16, GLM one-shot).** El cierre de las cuatro fronteras y la campaña autorizada se ejecutaron sobre el mismo checkout en la rama `glm/tradesgerard-c1c4-closure-20261016` @ `7f7d4953ddd585d1f6f3b228ce04ef89bb9aab13` (base `e0e67f8c`, fast-forward). Resultado: **CORRECTED_AND_FUNCTIONALLY_VALIDATED** dentro del alcance declarado; publicación a master verificada por `git ls-remote`. Presupuesto histórico (intento 91fe559f 1/1) se conserva como antecedente; el encargo del Owner autorizó UN intento financiero nuevo (consumido 1/1, exit0) y máximo dos preparaciones (1/2 usada).

### Cierre C1–C4 (commit 7f7d4953)

- **C1** — la entrega H1 declarada (F1/F3) es no-decisional: el gate de timeframe precede a la consulta de analytics en `tg.Evaluate`; sin snapshot no aborta ni falsea el espejo de readiness, y el corte 1m sigue fail-closed estricto. RED→GREEN (`TestEvaluate_H1DeliveryWithoutSnapshotDoesNotAbort`, `TestEvaluate_H1DeliveryAfterReadyMirrorKeepsMirror`, `TestEvaluate_1mDeliveryWithoutViewStillFailsClosed`, orden causal en frontera compartida).
- **C2** — Operation/MM accede a las MISMAS observaciones vía la extensión opcional `operation.AnalyticsViewSource`; el engine pinza UNA vista congelada por decisión (`buildMMInput`). El runtime publica el owner persistido en el bar seam (`TGOwnerViewFor` en `echo/market_analytics`, atado al switch `WithTGAnalyticsOwner`); el backtest sirve cortes de la tabla preparada (`Table.FrontierSeqAt` conserva el orden same-instant) o del owner. Pruebas de pinning por el Apply público, congelación (nueva observación visible sólo en la siguiente decisión), ausencia que no bloquea reducciones y wiring de composición.
- **C3** — `Table.lookupH1` sustituye el barrido hacia atrás por búsqueda binaria sobre el prefijo de visibilidad monótono (Seq estrictamente creciente, PublishedAt no decreciente); la metadata de indisponibilidad viaja con la snapshot visible más nueva; benchmark del peor caso 87 ns/op sobre 8760 snapshots; equivalencia contra el algoritmo de referencia en grillas de cortes.
- **C4** — la key de preparación (schema `echo.tg.prepared.v2`) lleva sólo identidad de CÁLCULO: rho/tick quedan en el manifiesto del experimento y dos perfiles que sólo cambian riesgo:beneficio comparten UNA preparación. Evidencia de contadores en el lote CLI: 3 items (gemelo risk-90 y variante rho-2 con demanda F1 idéntica) → `tg_preparations=1`. Negativos intactos: fuente/semilla/calendario/demanda/ventana dividen la key.

Fallos preexistentes contrastados en la BASE limpia (no introducidos, no tocados): 5×BTG-S05 y `TestTGWiring_OwnerFeedsAtSeamAndViewPerTrigger` (dependencia de orden del contador global) en la suite completa del backtester; `TestTGFilterSharedTypedLiveBacktestFactoryParity` (config) y `TestEconomicMinimumCoreTypedConfigAndProtectionParity/LIVE` (el guard OHLC-only-BACKTEST de `cb9cc0cd` vs el fixture cross-mode) — ambos reproducen en `e0e67f8c`.

### Campaña funcional del candidato corregido

**COMPLETE exit0, reconciled=true** — F1/K05/2300, NQZ5, ventana O11 2025-10-14→2025-11-25, un item, intento financiero 1/1. Directorio `/srv/echo-work/runs/consolidation-20261015/campaign-f1-k05-2300-7f7d4953/` (binario `1dc82bd0…`, plan `d630e36c…`, recibo `campaign-result.md`). Operaciones reales: 329 operaciones, 362 señales (331 OPEN + 31 CLOSE_ALL), 12 fills (6 entradas 2025-10-14/15 con sus cierres), 18 comandos. Cuenta `btg-functional`: compra 120 (14-oct) + renovación 120 (13-nov), 48000.12/50000 (neto −1999.88 = bruto −1970 − costos 29.88 exactos), pausa interna activa al horizonte (`HORIZON_CENSORED`), 0 retiros/0 pases/**0 cobros**; caja 5000→4760. Contadores: `tg_preparations=1`, `tg_kernel_feeds_runtime=0` (cero feeds de kernels durante la simulación). Wall 10m41s, CPU 1366.4s, RSS máx 372 MiB (proceso completo). La caja O11 5091 y el cobro 1651 siguen siendo antecedentes, no aserciones.

### Cambios implementados

- Kernels TG fuera de Strategy/MM; propietario analytics compartido. Batch prepara una tabla inmutable por identidad completa antes de cualquier campaña; runtime alimenta el mismo owner y publica snapshots vinculados a stream, cierre, revisión, epoch y disponibilidad.
- Fuente NT preparada en un escaneo, con metadata y registros vinculados; vistas defensivas. Datos/analytics se comparten; decisiones, cuentas y estado financiero permanecen aislados.
- Clonación profunda de Operation, snapshots defensivos de Ledger y memos inseguros retirados. Runtime registra las 14 ValueSpecs actuales y rechaza checkpoint vacío/ajeno cuando contiene estado.
- Manual de flujo/composición y catálogo compacto de 40 referencias en el producto. Comparador histórico marcado NO CERTIFICADOR y fuera de aceptación. Ideas K06/B2/BE/30m siguen pendientes, sin implementación.
- Binario generado `echo-backtest` retirado del repo; cinco binarios preexistentes de otros componentes restaurados sin cambios respecto de master.

### Prueba funcional y corrección posterior

La única invocación autorizada, F1/K05/2300 del candidato 91fe559f, terminó **FAILED/exit2** el 16-oct a 08:06:32UTC: `SOURCE_AGGREGATE_CLOSED` durante TGPrepare. Un item, un intento, ningún retry; no se llamó al motor financiero. Wall 3,39 s, CPU user 4,08 s/system 0,64 s, RSS máximo 292620 KiB. Son medidas de un fallo de preparación, no de rendimiento del refactor completo. Contadores: un archivo abierto, 90589 filas, 193 feeds en preparación, cero feeds runtime, cero tablas terminadas.

Causa: el precálculo cerraba analytics en fase 3 antes de incorporar el último minuto, mientras el driver OHLCV2 reserva ese finalizador para fase 5. `2c318dcf` alinea ese orden y reutiliza la elegibilidad `completeNativeBar` para excluir agregados incompletos. `e0e67f8c` corrige los fixtures para derivar horarios de America/Chicago y probar cierre en invierno/verano, pausa/reanudación, V1 y prefijo parcial.

**Evidencia:** RED exit1 sobre tg_prepare.go de 91fe559f reproduce SOURCE_AGGREGATE_CLOSED; GREEN exit0 con el fix en la suite TG. El log RED preservado muestra el caso de invierno; el require aborta antes del verano. GREEN sí recorre ambos. BreakStart es cobertura de preservación, no un segundo fallo RED demostrado. Las afirmaciones más amplias del informe autor se acotan en `refactor-review-adjudication.md`. La prueba fallida no valida el commit corregido.

También pasaron build/vet y pruebas focalizadas de kernels, Strategy, fuente, CLI, composición y restauración; evidencia externa conserva comandos/exits, errores previos y correcciones. No se afirma suite global verde ni equivalencia histórica completa. El test de registro enumera el conjunto actual; no descubre automáticamente cualquier campo futuro.

### Candidato e0e67f8c (antecedente)

Directorio `/srv/echo-work/runs/consolidation-20261015/campaign-f1-k05-2300-e0e67f8c/` quedó **sin ejecutar** (out vacío; su presupuesto de campaña no se consumió). Tras la solicitud de una invocación adicional, el Owner ordenó publicar de inmediato el candidato corregido sin validación funcional; esa instrucción no autorizaba otra campaña. Recibo: `publication-result.md`. El encargo del 16-oct (sección anterior) consumió después el único intento financiero nuevo sobre `7f7d4953`.

### Límites y conservación

Runtime queda desactivado por defecto; no LIVE/deploy. SR necesita autoridad OHLC1m completa; trades no certificados conservan SR_LIVE_COMPLETENESS_UNVERIFIED. Prefijo offline no se inventa en runtime: F1 espera historia propia suficiente. La campaña nueva debe ejercitar operaciones/cuentas realmente; una ejecución vacía no basta. La instrumentación actual ofrece contadores agregados y tiempo total/CPU/RSS; no se inventan subfases de simulación/finalización.

Un GLM-5.3-Flash implementador real mediante ZCode, mismo checkout `/home/kor/aranea/work/tradesgerard-perf-memory-20261015/echo`, rama `codex/tradesgerard-consolidation-20261015`. Un contexto GLM independiente revisó alcance acotado; GOD verificó/corrigió límites de sus afirmaciones. Sin nuevos clones/worktrees ni implementación personal de GOD. La cuota GLM que bloqueó la sesión previa volvió a permitir ejecución; no hubo sustitución de modelo/cuenta. El Owner advirtió cuota semanal: se suprimieron reconstrucción de preimágenes, certificación de ocho pares, relecturas amplias y auditorías históricas como gates.

Origin del escritor apunta a GitHub xKoRx/echo; master avanzó por fast-forward de 372af59a a e0e67f8c. Ruta canónica `/home/kor/go`, vault y procesos ajenos preservados. Copias retiradas 0, bytes liberados 0; dependencias y refs locales conservadas.

Respaldo actual verificado: `/srv/echo-work/runs/consolidation-20261015/recovery-refactor-20261016/README.md`, bundle incremental hasta e0e67f8c con base autónoma previamente comprobada; hashes de evidencia y checkout limpio. El respaldo de WIP anterior sigue como historia. No se hizo restauración destructiva de prueba. Los informes de cierre/cuota anteriores son estados históricos, no sustituyen este estado vigente.

## Fuentes

Directorio durable `/srv/echo-work/runs/consolidation-20261015/`: `owner-refactor-priority-20261016.md`, `refactor-final-tests.log`, `one-campaign-result.md`, `preparation-boundary-red.log`, `preparation-boundary-green.log`, `preparation-boundary-fix.md`, `refactor-review-adjudication.md`, `campaign-budget.json` y respaldos. Históricos y sus límites: [[TRADESGERARD-OPERABILITY-RESULTADO]], [[TRADESGERARD-PERFORMANCE-MEMORY]]. Continuidad: [[TRADESGERARD-CONTROL]].
