---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-14"
---

# TRADESGERARD-OPERABILITY-T2

## Propósito

**Estado vigente: O11 verificada; F1×10 en cola autorizada del supervisor común.** Source `5de33134311f3a23a306d12d1c8fabbf5222c502`, binario `734c923804fff719b1037953a387b715cc57e41f988775970b48038cea1b55a7`; gate independiente `ecb199bad5e32eefcfa87fa7cf73e72ed10451aedf0a106f2b8447d002dddd87`. Inputs sin cambios normativos y smoke F1 14ops/caja4640 auditado; cero campañas completas nuevas por ahora. CONTROL registra lanzamiento real cuando ocurra, recursos y dependencias runtime.

Antecedente AFFECTED preservado: defecto común O10 probado en K04 F0, SHA256 `5d6dda573a84bf7832cc55738f4c81853938974ca68a997264788d9908a15e88`. T2 anterior conserva cero COMPLETE, dos CANCELLED_DRAINEDexit2 y ocho no lanzadas; cancelación técnica, no pérdida económica. Las ejecuciones/PASS siguientes son historia anterior a O11.

**Estado actual: RESOURCE_RETRY1_RUNNING,0/10COMPLETE al lanzamiento02:29Z.** Mismos O10/inputs/gate; sesión82581, K01/K02-r2300 PID/PGID3053759/3053765, salidas nuevas `retry1-F1-*` y progreso `T2-o10-resource-retry1-progress.json`. Cuatro campañas globales con T1, admisión y forecast en CONTROL. El intento anterior permanece preservado: a01:53:43Z el supervisor drenó K01/K02-r2300 por reserva física inferior8GiB; ambos exit2/FAILED, ocho no lanzados. Cancelación técnica, no resultado económico ni invalidación del gate O10/F1. La descripción del lanzamiento original siguiente es histórica.

Tanda F1-TREND × K01–K05 × solicitudes brutas2300/3000. Estado **O10_INDEPENDENT_PASS / RUNNING_0_OF_10** al relanzamiento. Se ejecutan diez trayectorias nuevas con política económica O10 verificada. El gate original de matemática/causalidad F1 OHLC conserva su evidencia; las dos campañas de la política O8 canceladas y ocho no lanzadas permanecen AFFECTED, fuera del ranking. No es aceptación final del Owner.

## Contenido

### Ejecución vigente O10

Source `76a1e69e5a0a67b94b920e2ffb983fd226eb127a`, binario `3c66a1b091fde81a7804e38eb265f16078005c1fc211db46e62f690cb04426bf`, gate `verifier/independent-o10-gate.json` SHA256 `2155593e9eca093126c579bb34ab67c3b3c904b0b91da55ed3664ada93414693`, INDEPENDENT_PASS OFFLINE_OHLC. Mismo request C4, prefijo25H1 separado idéntico F1, perfil comercial y diez configuraciones; sólo software/política común corregidos. Smoke independiente23base/14operaciones/9rechazos filtro/caja4640, UNKNOWN0; no fila de ranking.

Supervisor `run_t2_o10.py`, sesión57628, jobs2; primeros K01/K02-r2300 PID/PGID3018587/3018601 comprobados por manager. Lanzamiento01:26:51Z, progreso `implementer/evidence/T2-o10-progress.json`; comparte máximo4 procesos globales con T1, presupuesto agregado y reserva≥8GiB. Cero COMPLETE al lanzamiento. Se auditarán las755 identidades base y el oráculo F1 sobre resultados durables, sin equiparar fills de trayectorias con exposición distinta.

Los siguientes párrafos registran el corte histórico F1/O8 afectado; no representan la política vigente ni resultados reutilizables.

### Contrato del experimento

HOLD posterior común O8: una cuenta funded con objetivo alcanzado seguía consumiendo cruces mientras esperaba fecha de cumplimiento, bloqueando alternativas operables. Prueba SHA256 `8adeca2cfa8dd5207cf6256677773aba222cdb7f01b5e54130d98f5743e4efd1`, [[TRADESGERARD-OPERABILITY-T0]]/[[TRADESGERARD-OPERABILITY-T1]]. Parada00:22:07Z por SIGINT del manager al supervisor propio2979615, que drenó K01/K02–r2300 con exit2 y preservó resultados parciales; los tres procesos están ausentes. La nueva tanda F1×10 usará la corrección común O9 después del gate. No se invalida el oráculo H1 ni se cambia SMA24; sí se retira cualquier resultado de esta política del ranking económico.

Freeze físico comprobado por manager: source `f4643aefce49876ed40bb4fd1efefe1894cb1520`, árbol limpio `7390209adb42dea4000b5e6750cc0656616376ce`, binario SHA256 `201edd9b22a08b60b9b06b6e7411449e0515eaba48b4be6571d6794c9977a4a6`. Manifiesto `implementer/evidence/f1-freeze-manifest.json` SHA256 `e5d45ebed793c8b53483ebaf7a215920a0fbce7c86401d6497e67a88139a781e`, diez inputs y perfil común O8 `d66bb56b`. Gate independiente `verifier/independent-f1-gate.json` SHA256 `0a876028c0caf8c13a65781d3738d6c24611a76b5921503ec1a19d82a32552ac`, **INDEPENDENT_PASS**, alcance técnico F1/OHLC offline. Manager comprobó el gate y los hashes físicos de sus siete evidencias.

Cobertura300/312=96,1538% de bloques afectados recalculada independientemente, referencia `534ca1c7`, sin cambiar denominadores. Diez inputs idénticos a O8 salvo filtro/prefijo/build/identidades; blobs monetarios comunes byte-identical. El prefijo25H1 fue contrastado directamente con NT: cierres válidos, mismo contrato, epoch0 y as-of causal. SDK PASS y negativos independientes de completitud runtime, seed stale, F0 sin H1 y rechazo explícito de F2/F3 aún no implementados. Pruebas DST31oct/3nov con UTC14/15 y offsetsNY−04/−05 aprobadas. El cotejo de witnesses de las755 señales del productor se hará sobre las campañas completas; el smoke de un día no acredita por sí mismo toda esa ventana.

Smoke del build exacto:23cruces base K/ATR idénticos,14aceptados y9rechazados por dirección,14operaciones cerradas con marca causal correcta al primerfill, UNKNOWN0 y snapshots económicos ausentes0. Caja4640 conciliada con ledger; diagnóstico, no una configuración del ranking. La falta de autoridad H1 del runtime sigue explícita y no queda subsanada por este PASS offline.

SIG-B conserva K lenta20/SMA3 y los cruces causales en cierre1m. F1 admite LONG sólo con SMA24 de cierres H1 actual mayor que anterior, y SHORT sólo con pendiente menor; igualdad no aporta dirección. Se necesitan25 cierres H1 válidos y totalmente publicados. No hay filtro de posición del precio respecto a la media, pendiente mínima ni otra confirmación. F0 no depende del readiness H1. Los indicadores siguen actualizándose cuando la entrada no es admisible.

La ventana, perfil comercial, NQ y economía corresponden a [[TRADESGERARD-OPERABILITY-T1]]. La preparación usa el prefijo H1 necesario del mismo corpus, conservando el warmup1m original para no alterar K/ATR ni las755 identidades base. El prefijo prospectivo se vincula a stream/contrato/época/calendario/fuente y su as-of nunca supera el inicio observado. La época inicial del SDK es0; no debe confundirse con otra autoridad de serving. Una hora parcial conocida del corpus no se completa con precios fabricados.

### Diagnóstico anterior al freeze, fuera del ranking

Smoke con política común O7 afectada:23 cruces base,14 aceptados y9 rechazados por dirección; cero falta de readiness H1. El verificador cotejó23/23 con un oráculo del prefijo largo: SMA anterior/actual y último cierre H1 coinciden, history25 y seed/live epoch0. ATR1m se contrastó con tolerancia1e−12 contra el oráculo de coma flotante; la primera comparación exacta falló por redondeo, sin diferencia de señal. Este smoke no cuenta entre las cuarenta configuraciones ni certifica el futuro build F1 con O8.

Derivado independiente relativo al root `ARANEA_ROOT/work/tradesgerard-operability-20261013`: `verifier/h1-epoch0-diagnostic-independent.json`, SHA256 `feb53f65d4433aa8d52f694581818868cbc4f81747a8850ef83e38018eafa097`. El smoke conserva su clasificación `DIAGNOSTIC_O7_COMMON_POLICY_AFFECTED_NOT_RANKING`.

### Frontera runtime

La política común de mínimo económico requiere además una quote ejecutable fresca. `SnapshotViews.Market()` no implementa `ExecutableQuoteSource` en la ruta runtime actual: todas las versiones F0–F3 de la nueva política quedan funcionalmente bloqueadas allí, y F1/F3 tienen el bloqueo H1 adicional. No se confunde esta ausencia concreta con falta de todos los datos del adapter. Un RED independiente mostró que la factory admitía offsets de simulación fuera de BACKTEST; el integrador corregirá esa admisión en F2 sin alterar el camino offline. [[TRADESGERARD-OPERABILITY-T0]] y [[TRADESGERARD-OPERABILITY-T0-VERIFY]] conservan evidencia y adjudicación. El gate F1 sigue limitado a OHLC offline.

La ruta actual de ticks `ApplyTrade` no acredita la completitud de la H1 tras inicio o cambio de época. Muchos trades no equivalen a cobertura del intervalo. F1/F3 quedan funcionalmente bloqueados en esa ruta con `H1_LIVE_COMPLETENESS_UNVERIFIED`, incluso si existe una seed histórica válida y luego aparece una H1 nueva sin autoridad. Una snapshot antigua no puede borrar esa frontera. El backtest OHLC con cobertura de minutos fuente verificada sí puede ejecutar el filtro. Compartir matemática y guardas no demuestra que el feed runtime proporcione la autoridad que falta.

El negativo independiente del freeze exacto pasó: una seed válida no permite ignorar la nueva H1 sin autoridad y una snapshot antigua no la restaura. F0 sigue operable sin H1. No se inicia ningún servicio ni operación real para resolver la limitación. Esta dependencia debe mantenerse visible en el informe final.

### Continuidad y recursos

Lanzamiento comprobado2026-10-13T23:58:59Z: harness session26817, K01–r2300 PID/PGID2979660 y K02–r2300 PID/PGID2979671; ocho pendientes. Progreso durable `implementer/evidence/T2-f1-progress.json`, jobs2. Junto con T1 O8 jobs2 son cuatro campañas activas supervisadas; no daemon ni promesa fuera de la sesión. Source/bin/inputs F1 quedan inmutables. El integrador reutiliza el checkout antiguo cb9 ya quieto y preservado para F2, evitando otra copia del repo.

Admisión real T2: disco libre10.155.454.464bytes, RAMavailable63.409.938.432, load8,02/6,98/6,05; evidencia nueva897.204.353, scratch propio agregado1.017.476 y forecast1.132.068.993≤1.610.612.736bytes. Reserva física8.589.934.592, scratch global2GiB, lote256MiB y traza/log16MiB permanecen vigentes. Cambio de concurrencia3→4 documentado por medición, no benchmark bajo contención. PIDs de T1 y T2 verificados vivos por manager después del lanzamiento.

T1 O8 mantiene concurrencia dos. La admisión inicial prevista para T2 era una campaña adicional, máximo global tres. Medición manager23:48Z: load5,67/5,98/5,52 en24CPU, RAMavailable64.265.498.624bytes, disco libre10.196.152.320 y evidencia nueva872.950.013. Con esos recursos se habilitó admisión máxima global cuatro campañas, todas dentro de afinidad6CPU, GOMAXPROCS4 por hijo y presupuesto/reservas previos intactos. F1 podrá lanzar dos junto a las dos F0 sólo tras gate independiente y nueva medición al lanzamiento; no se afirma que ya estén ejecutándose ni un benchmark bajo contención. Fuente F1 aislada del build F0 en uso. El integrador continuará F2 durante T2 y reutilizará ambos filtros para F3; no hay aprobación intermedia pendiente del Owner. Los recibos COMPLETE íntegros y su auditoría determinarán las filas económicas, sin convertir fixtures o diagnósticos en resultados de campaña.

## Fuentes

- [[TRADESGERARD-CONTROL]], [[TRADESGERARD-OPERABILITY-T0]], [[TRADESGERARD-OPERABILITY-T0-VERIFY]], [[TRADESGERARD-OPERABILITY-T1]], [[TRADESGERARD-ENTRY-REPAIR]].
- Root de evidencia `ARANEA_ROOT/work/tradesgerard-operability-20261013`; source candidato en `implementer/echo`, separado del checkout O8 congelado.
- TOP solicitado `gpt-6.1-sol`; modelo servido UNKNOWN. Un integrador y un verificador independiente LOCAL; manager coordina, revisa y documenta.
