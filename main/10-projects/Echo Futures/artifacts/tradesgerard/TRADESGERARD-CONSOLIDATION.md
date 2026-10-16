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

Terminar un refactor mantenible de Echo: analytics compartido, responsabilidades claras, composición modular, aislamiento y causalidad; estructura mínima para continuar iterando (SOLID/clean, KISS/YAGNI). Una campaña prueba el candidato final. El delta explícito del Owner del16-oct elimina la certificación de campañas históricas como requisito; los resultados anteriores quedan como referencia.

## Contenido

**Estado: refactor corregido y probado con fixtures; validación funcional pendiente de autorización adicional.** Candidato `e0e67f8c8a115aa2cbd0944ab0d614de85a07df6`, árbol limpio `0cd0ef93432a90389c74c1281be3c07f65b2370a`. Presupuesto **1/1 consumido**: el intento de `91fe559f` falló en preparación, antes del motor financiero. Sin merge/push de Echo ni eliminación de copias. Proyecto abierto.

### Cambios implementados

- Kernels TG fuera de Strategy/MM; propietario analytics compartido. Batch prepara una tabla inmutable por identidad completa antes de cualquier campaña; runtime alimenta el mismo owner y publica snapshots vinculados a stream, cierre, revisión, epoch y disponibilidad.
- Fuente NT preparada en un escaneo, con metadata y registros vinculados; vistas defensivas. Datos/analytics se comparten; decisiones, cuentas y estado financiero permanecen aislados.
- Clonación profunda de Operation, snapshots defensivos de Ledger y memos inseguros retirados. Runtime registra las14 ValueSpecs actuales y rechaza checkpoint vacío/ajeno cuando contiene estado.
- Manual de flujo/composición y catálogo compacto de40 referencias en el producto. Comparador histórico marcado NO CERTIFICADOR y fuera de aceptación. Ideas K06/B2/BE/30m siguen pendientes, sin implementación.
- Binario generado `echo-backtest` retirado del repo; cinco binarios preexistentes de otros componentes restaurados sin cambios respecto de master.

### Prueba funcional y corrección posterior

La única invocación autorizada, F1/K05/2300 del candidato91fe559f, terminó **FAILED/exit2** el16-oct a08:06:32UTC: `SOURCE_AGGREGATE_CLOSED` durante TGPrepare. Un item, un intento, ningún retry; no se llamó al motor financiero. Wall3,39s, CPU user4,08s/system0,64s, RSS máximo292620KiB. Son medidas de un fallo de preparación, no de rendimiento del refactor completo. Contadores: un archivo abierto,90589filas,193feeds en preparación, cero feeds runtime, cero tablas terminadas.

Causa: el precálculo cerraba analytics en fase3 antes de incorporar el último minuto, mientras el driver OHLCV2 reserva ese finalizador para fase5. `2c318dcf` alinea ese orden y reutiliza la elegibilidad `completeNativeBar` para excluir agregados incompletos. `e0e67f8c` corrige los fixtures para derivar horarios de America/Chicago y probar cierre en invierno/verano, pausa/reanudación, V1 y prefijo parcial.

**Evidencia:** RED exit1 sobre tg_prepare.go de91fe559f reproduce SOURCE_AGGREGATE_CLOSED; GREEN exit0 con el fix en la suite TG. El log RED preservado muestra el caso de invierno; el require aborta antes del verano. GREEN sí recorre ambos. BreakStart es cobertura de preservación, no un segundo fallo RED demostrado. Las afirmaciones más amplias del informe autor se acotan en `refactor-review-adjudication.md`. La prueba fallida no valida el commit corregido.

También pasaron build/vet y pruebas focalizadas de kernels, Strategy, fuente, CLI, composición y restauración; evidencia externa conserva comandos/exits, errores previos y correcciones. No se afirma suite global verde ni equivalencia histórica completa. El test de registro enumera el conjunto actual; no descubre automáticamente cualquier campo futuro.

### Candidato concreto para autorizar

Directorio `/srv/echo-work/runs/consolidation-20261015/campaign-f1-k05-2300-e0e67f8c/`: binario Go1.27.1 vinculado al commit limpio, SHA256 `b4b76c0ad4ed340e0abf42648604510e8cbc40ebd75d30abf2706d441af897e4`; plan de EXACTAMENTE un item, SHA256 `33c90684c2a4ba907536407cd0ead3feacd7f7bed56f0dfc0c3fa95f46567648`. Out vacío. Preparado, **no ejecutado**.

Se solicitó al Owner UNA invocación adicional sólo después de tener fix, pruebas, build y plan verificables. El mandato original limita invocaciones y prohíbe relanzar tras fallo: silencio o tiempo transcurrido no autorizan otra. Si la autoriza, registrar el nuevo máximo/consumo antes de lanzar, comprobar funcionamiento y contabilidad sin forzar cifras antiguas; publicar sólo el árbol validado. Si mantiene el límite, conservar PARTIAL_VALIDATION y no mergear como verificado.

### Límites y conservación

Runtime queda desactivado por defecto; no LIVE/deploy. SR necesita autoridad OHLC1m completa; trades no certificados conservan SR_LIVE_COMPLETENESS_UNVERIFIED. Prefijo offline no se inventa en runtime: F1 espera historia propia suficiente. La campaña nueva debe ejercitar operaciones/cuentas realmente; una ejecución vacía no basta. La instrumentación actual ofrece contadores agregados y tiempo total/CPU/RSS; no se inventan subfases de simulación/finalización.

Un GLM-5.3-Flash implementador real mediante ZCode, mismo checkout `/home/kor/aranea/work/tradesgerard-perf-memory-20261015/echo`, rama `codex/tradesgerard-consolidation-20261015`. Un contexto GLM independiente revisó alcance acotado; GOD verificó/corrigió límites de sus afirmaciones. Sin nuevos clones/worktrees ni implementación personal de GOD. La cuota GLM que bloqueó la sesión previa volvió a permitir ejecución; no hubo sustitución de modelo/cuenta. El Owner advirtió cuota semanal: se suprimieron reconstrucción de preimágenes, certificación de ocho pares, relecturas amplias y auditorías históricas como gates.

Origin del escritor ahora apunta a GitHub xKoRx/echo; master372af59a fue comprobado ancestro. Revalidar antes de publicar. Ruta canónica `/home/kor/go`, vault y procesos ajenos preservados. Copias retiradas0, bytes liberados0: publicación no realizada y dependencias/refs locales conservadas.

Respaldo actual verificado: `/srv/echo-work/runs/consolidation-20261015/recovery-refactor-20261016/README.md`, bundle incremental hastae0e67f8c con base autónoma previamente comprobada; hashes de evidencia y checkout limpio. El respaldo de WIP anterior sigue como historia. No se hizo restauración destructiva de prueba. Los informes de cierre/cuota anteriores son estados históricos, no sustituyen este estado vigente.

## Fuentes

Directorio durable `/srv/echo-work/runs/consolidation-20261015/`: `owner-refactor-priority-20261016.md`, `refactor-final-tests.log`, `one-campaign-result.md`, `preparation-boundary-red.log`, `preparation-boundary-green.log`, `preparation-boundary-fix.md`, `refactor-review-adjudication.md`, `campaign-budget.json` y respaldos. Históricos y sus límites: [[TRADESGERARD-OPERABILITY-RESULTADO]], [[TRADESGERARD-PERFORMANCE-MEMORY]]. Continuidad: [[TRADESGERARD-CONTROL]].
