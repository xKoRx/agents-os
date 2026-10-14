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
updated: "2026-10-13"
---

# TRADESGERARD-OPERABILITY-T2

## Propósito

Tanda F1-TREND × K01–K05 × solicitudes brutas2300/3000. Estado **F1_INDEPENDENT_PASS_OFFLINE_OHLC, lanzamiento T2 en preparación**. El módulo compartido y su preparación causal están congelados y pasaron verificación independiente contra el build exacto. La política común O8 está incorporada. Ninguna campaña económica F1 completa todavía; no es aceptación final del Owner.

## Contenido

### Contrato del experimento

Freeze físico comprobado por manager: source `f4643aefce49876ed40bb4fd1efefe1894cb1520`, árbol limpio `7390209adb42dea4000b5e6750cc0656616376ce`, binario SHA256 `201edd9b22a08b60b9b06b6e7411449e0515eaba48b4be6571d6794c9977a4a6`. Manifiesto `implementer/evidence/f1-freeze-manifest.json` SHA256 `e5d45ebed793c8b53483ebaf7a215920a0fbce7c86401d6497e67a88139a781e`, diez inputs y perfil común O8 `d66bb56b`. Gate independiente `verifier/independent-f1-gate.json` SHA256 `0a876028c0caf8c13a65781d3738d6c24611a76b5921503ec1a19d82a32552ac`, **INDEPENDENT_PASS**, alcance técnico F1/OHLC offline. Manager comprobó el gate y los hashes físicos de sus siete evidencias.

Cobertura300/312=96,1538% de bloques afectados recalculada independientemente, referencia `534ca1c7`, sin cambiar denominadores. Diez inputs idénticos a O8 salvo filtro/prefijo/build/identidades; blobs monetarios comunes byte-identical. El prefijo25H1 fue contrastado directamente con NT: cierres válidos, mismo contrato, epoch0 y as-of causal. SDK PASS y negativos independientes de completitud runtime, seed stale, F0 sin H1 y rechazo explícito de F2/F3 aún no implementados. Pruebas DST31oct/3nov con UTC14/15 y offsetsNY−04/−05 aprobadas. El cotejo de witnesses de las755 señales del productor se hará sobre las campañas completas; el smoke de un día no acredita por sí mismo toda esa ventana.

Smoke del build exacto:23cruces base K/ATR idénticos,14aceptados y9rechazados por dirección,14operaciones cerradas con marca causal correcta al primerfill, UNKNOWN0 y snapshots económicos ausentes0. Caja4640 conciliada con ledger; diagnóstico, no una configuración del ranking. La falta de autoridad H1 del runtime sigue explícita y no queda subsanada por este PASS offline.

SIG-B conserva K lenta20/SMA3 y los cruces causales en cierre1m. F1 admite LONG sólo con SMA24 de cierres H1 actual mayor que anterior, y SHORT sólo con pendiente menor; igualdad no aporta dirección. Se necesitan25 cierres H1 válidos y totalmente publicados. No hay filtro de posición del precio respecto a la media, pendiente mínima ni otra confirmación. F0 no depende del readiness H1. Los indicadores siguen actualizándose cuando la entrada no es admisible.

La ventana, perfil comercial, NQ y economía corresponden a [[TRADESGERARD-OPERABILITY-T1]]. La preparación usa el prefijo H1 necesario del mismo corpus, conservando el warmup1m original para no alterar K/ATR ni las755 identidades base. El prefijo prospectivo se vincula a stream/contrato/época/calendario/fuente y su as-of nunca supera el inicio observado. La época inicial del SDK es0; no debe confundirse con otra autoridad de serving. Una hora parcial conocida del corpus no se completa con precios fabricados.

### Diagnóstico anterior al freeze, fuera del ranking

Smoke con política común O7 afectada:23 cruces base,14 aceptados y9 rechazados por dirección; cero falta de readiness H1. El verificador cotejó23/23 con un oráculo del prefijo largo: SMA anterior/actual y último cierre H1 coinciden, history25 y seed/live epoch0. ATR1m se contrastó con tolerancia1e−12 contra el oráculo de coma flotante; la primera comparación exacta falló por redondeo, sin diferencia de señal. Este smoke no cuenta entre las cuarenta configuraciones ni certifica el futuro build F1 con O8.

Derivado independiente relativo al root `ARANEA_ROOT/work/tradesgerard-operability-20261013`: `verifier/h1-epoch0-diagnostic-independent.json`, SHA256 `feb53f65d4433aa8d52f694581818868cbc4f81747a8850ef83e38018eafa097`. El smoke conserva su clasificación `DIAGNOSTIC_O7_COMMON_POLICY_AFFECTED_NOT_RANKING`.

### Frontera runtime

La ruta actual de ticks `ApplyTrade` no acredita la completitud de la H1 tras inicio o cambio de época. Muchos trades no equivalen a cobertura del intervalo. F1/F3 quedan funcionalmente bloqueados en esa ruta con `H1_LIVE_COMPLETENESS_UNVERIFIED`, incluso si existe una seed histórica válida y luego aparece una H1 nueva sin autoridad. Una snapshot antigua no puede borrar esa frontera. El backtest OHLC con cobertura de minutos fuente verificada sí puede ejecutar el filtro. Compartir matemática y guardas no demuestra que el feed runtime proporcione la autoridad que falta.

El negativo independiente del freeze exacto pasó: una seed válida no permite ignorar la nueva H1 sin autoridad y una snapshot antigua no la restaura. F0 sigue operable sin H1. No se inicia ningún servicio ni operación real para resolver la limitación. Esta dependencia debe mantenerse visible en el informe final.

### Continuidad y recursos

T1 O8 mantiene concurrencia dos. La admisión inicial prevista para T2 era una campaña adicional, máximo global tres. Medición manager23:48Z: load5,67/5,98/5,52 en24CPU, RAMavailable64.265.498.624bytes, disco libre10.196.152.320 y evidencia nueva872.950.013. Con esos recursos se habilitó admisión máxima global cuatro campañas, todas dentro de afinidad6CPU, GOMAXPROCS4 por hijo y presupuesto/reservas previos intactos. F1 podrá lanzar dos junto a las dos F0 sólo tras gate independiente y nueva medición al lanzamiento; no se afirma que ya estén ejecutándose ni un benchmark bajo contención. Fuente F1 aislada del build F0 en uso. El integrador continuará F2 durante T2 y reutilizará ambos filtros para F3; no hay aprobación intermedia pendiente del Owner. Los recibos COMPLETE íntegros y su auditoría determinarán las filas económicas, sin convertir fixtures o diagnósticos en resultados de campaña.

## Fuentes

- [[TRADESGERARD-CONTROL]], [[TRADESGERARD-OPERABILITY-T0]], [[TRADESGERARD-OPERABILITY-T0-VERIFY]], [[TRADESGERARD-OPERABILITY-T1]], [[TRADESGERARD-ENTRY-REPAIR]].
- Root de evidencia `ARANEA_ROOT/work/tradesgerard-operability-20261013`; source candidato en `implementer/echo`, separado del checkout O8 congelado.
- TOP solicitado `gpt-6.1-sol`; modelo servido UNKNOWN. Un integrador y un verificador independiente LOCAL; manager coordina, revisa y documenta.
