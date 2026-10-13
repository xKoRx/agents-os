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

Tanda F1-TREND × K01–K05 × solicitudes brutas2300/3000. Estado **F1_PRE_FREEZE, 0/10 campañas definitivas lanzadas**. El módulo compartido y su preparación causal están en verificación; no hay todavía un gate independiente del build final F1. La política común debe incorporar O8 antes de ejecutar T2. No es aceptación final del Owner.

## Contenido

### Contrato del experimento

SIG-B conserva K lenta20/SMA3 y los cruces causales en cierre1m. F1 admite LONG sólo con SMA24 de cierres H1 actual mayor que anterior, y SHORT sólo con pendiente menor; igualdad no aporta dirección. Se necesitan25 cierres H1 válidos y totalmente publicados. No hay filtro de posición del precio respecto a la media, pendiente mínima ni otra confirmación. F0 no depende del readiness H1. Los indicadores siguen actualizándose cuando la entrada no es admisible.

La ventana, perfil comercial, NQ y economía corresponden a [[TRADESGERARD-OPERABILITY-T1]]. La preparación usa el prefijo H1 necesario del mismo corpus, conservando el warmup1m original para no alterar K/ATR ni las755 identidades base. El prefijo prospectivo se vincula a stream/contrato/época/calendario/fuente y su as-of nunca supera el inicio observado. La época inicial del SDK es0; no debe confundirse con otra autoridad de serving. Una hora parcial conocida del corpus no se completa con precios fabricados.

### Diagnóstico anterior al freeze, fuera del ranking

Smoke con política común O7 afectada:23 cruces base,14 aceptados y9 rechazados por dirección; cero falta de readiness H1. El verificador cotejó23/23 con un oráculo del prefijo largo: SMA anterior/actual y último cierre H1 coinciden, history25 y seed/live epoch0. ATR1m se contrastó con tolerancia1e−12 contra el oráculo de coma flotante; la primera comparación exacta falló por redondeo, sin diferencia de señal. Este smoke no cuenta entre las cuarenta configuraciones ni certifica el futuro build F1 con O8.

Derivado independiente relativo al root `ARANEA_ROOT/work/tradesgerard-operability-20261013`: `verifier/h1-epoch0-diagnostic-independent.json`, SHA256 `feb53f65d4433aa8d52f694581818868cbc4f81747a8850ef83e38018eafa097`. El smoke conserva su clasificación `DIAGNOSTIC_O7_COMMON_POLICY_AFFECTED_NOT_RANKING`.

### Frontera runtime

La ruta actual de ticks `ApplyTrade` no acredita la completitud de la H1 tras inicio o cambio de época. Muchos trades no equivalen a cobertura del intervalo. F1/F3 quedan funcionalmente bloqueados en esa ruta con `H1_LIVE_COMPLETENESS_UNVERIFIED`, incluso si existe una seed histórica válida y luego aparece una H1 nueva sin autoridad. Una snapshot antigua no puede borrar esa frontera. El backtest OHLC con cobertura de minutos fuente verificada sí puede ejecutar el filtro. Compartir matemática y guardas no demuestra que el feed runtime proporcione la autoridad que falta.

El negativo independiente está preparado para el freeze exacto; su preparación no es todavía un PASS de ese build. No se inicia ningún servicio ni operación real para resolver la limitación. Esta dependencia debe mantenerse visible en el informe final.

### Continuidad y recursos

T1 O8 ejecuta dos campañas. Al habilitarse F1 por gate independiente, admisión inicial T2 de una campaña adicional, máximo global tres, con nueva medición de disco/RAM/CPU y presupuesto agregado. Fuente F1 aislada del build F0 en uso. El integrador continuará F2 durante T2 y reutilizará ambos filtros para F3; no hay aprobación intermedia pendiente del Owner. Los recibos COMPLETE íntegros y su auditoría determinarán las filas económicas, sin convertir fixtures o diagnósticos en resultados de campaña.

## Fuentes

- [[TRADESGERARD-CONTROL]], [[TRADESGERARD-OPERABILITY-T0]], [[TRADESGERARD-OPERABILITY-T0-VERIFY]], [[TRADESGERARD-OPERABILITY-T1]], [[TRADESGERARD-ENTRY-REPAIR]].
- Root de evidencia `ARANEA_ROOT/work/tradesgerard-operability-20261013`; source candidato en `implementer/echo`, separado del checkout O8 congelado.
- TOP solicitado `gpt-6.1-sol`; modelo servido UNKNOWN. Un integrador y un verificador independiente LOCAL; manager coordina, revisa y documenta.
