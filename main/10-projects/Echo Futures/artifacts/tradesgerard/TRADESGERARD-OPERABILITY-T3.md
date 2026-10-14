---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[TRADESGERARD-CONTROL]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-14"
---

# TRADESGERARD-OPERABILITY-T3

## Propósito

**Estado vigente: HOLD_STALE_FUNDED_AUTHORITY / AFFECTED / SIN CAMPAÑAS ACTIVAS.** Defecto común de autoridad O10 demostrado en K04 F0 afecta el corte compartido. T3 conserva dos COMPLETE auditadas, dos CANCELLED_DRAINEDexit2 y seis no lanzadas en este intento. Sus saldos, costos y faltante4,76 se preservan como observación conciliada, fuera del ranking definitivo hasta corrección y repetición. Prueba SHA256 `5d6dda573a84bf7832cc55738f4c81853938974ca68a997264788d9908a15e88`, parada y alcance en CONTROL. Los estados RUNNING/PASS siguientes son históricos.

**Estado actual: RESOURCE_RETRY1_RUNNING,2/10 COMPLETE auditadas.** K01/K02-r2300 pasaron recibos/censo/oráculos/ledger/caja; caja4760/4520 y cero créditos. K03/K04 continúan. F2 jobs2 CPU6–8, sesión70412, mismo source/bin/gate/inputs, `retry1-F2-*` y `T3-f2-resource-retry1-progress.json`. Ocho campañas globales con T1/T2/T4; admisión y forecast en CONTROL. El intento anterior permanece preservado: a01:53:42Z el supervisor drenó K01/K02-r2300 por reserva física inferior8GiB; ambos exit2/FAILED, ocho no lanzados. Gate F2 conserva validez técnica; parciales no son pérdidas de trading ni filas del ranking. El lanzamiento original descrito abajo es histórico.

Ejecutar F2-SR × K01–K05 × retiro bruto2300/3000: diez campañas de la misma ventana C4, con política económica común corregida O10. Estado **INDEPENDENT_PASS_OFFLINE / RUNNING_0_OF_10** al lanzamiento. No hay resultados económicos finales todavía; el smoke sin actividad no es candidata ni fila del ranking.

## Contenido

### Primeras dos filas completas

Misma ventana C4: warmup2025-10-13T17:51Z, trade_start2025-10-14T13:30Z, fin exclusivo2025-11-25T23Z; datos NQ y perfil comercial C4 versionado conservados. Source/binario/configuración y diez inputs ligados por el freeze F2 descrito abajo. Cada campaña observa755cruces base:65pasan SR,690rechazados por zona. De las65aceptadas,59operaciones y6ocupadas;29días con entrada, cero Q0/UNKNOWN. Oráculo independiente60velas previas/K/ATR, marca real previa al fill y conciliación por cuenta/caja PASS.

| Configuración | Fallback | Compradas / fallidas / retiradas / pasadas | Pausadas únicas | Retiros solicitados / acreditados / neto | Compras / renovación / otros costos de caja | Caja inicial / mínima / final | Cambio caja | Ledger realizado global, NO caja |
|---|---:|---|---:|---|---|---|---:|---:|
| F2–K01–2300 | 42 | 1 /0 /0 /0 | 1 | 0 /0 /0 | 120 /120 /0 | 5000 /4760 /4760 | −240 | +91,22 |
| F2–K02–2300 | 17 | 4 /0 /0 /2 | 4 | 0 /0 /0 | 480 /0 /0 | 5000 /4520 /4520 | −480 | +8836,52 |

Ambas sin cobro y caja negativa en esta muestra; ranking40 todavía abierto. La renovación K01 está contabilizada, no se elimina por conservar una cuenta. Evaluación K01 termina con saldo50091,22/progreso91,22, faltan2908,78 al target3000; mejor día cerrado765,06. K02 termina con dos funded: progreso2295,24/faltante4,76 y520,12/faltante1779,88; las dos evaluaciones conservan progreso−494,94/+505,02. No pagos pendientes. Se preservan saldo, ledger, piso y plaza; beneficios retenidos no se añaden a caja.

| Configuración | R/T solicitados y admitidos | R/T proyectados efectivos | q | SL / TP puntos | SL / TP múltiplos ATR | Duración min / mediana / max segundos |
|---|---|---|---|---|---|---|
| F2–K01–2300 | ambos104,94–250 | 99,98–249,98 /105,02–250,04 | 1–2 | 4,5–12 /5,75–13 | ≈0,1684–2,2157 /0,2152–2,4003 | 3,982 /69,280 /4492,667 |
| F2–K02–2300 | ambos39,82–500 | 34,98–499,98 /40,02–500,08 | 1–4 | 1,25–24,5 /2,5–25,5 | ≈0,0655–2,9840 /0,1309–3,2327 | 4,364 /258,331 /2478,901 |

Rangos de campos, no una orden que combine extremos. Racha campaña K01:4ganadoras/net1020,08 y6perdedoras/net−1499,88; cuenta/fase coincide porque sólo existe una evaluación. K02:campaña8ganadoras/net3760,20 y3perdedoras/net−1429,90; máximo dentro de cuenta/fase4ganadoras/net1885,10 en cuenta2/EVALUATION. Cero neto reinicia y sin fill se excluye. K02 pasó tras20/19operaciones en las respectivas cuentas; primer pase≈16,221días desde trade_start. Pausas por870:0/3eventos K01/K02. Detalle completo de todas las rachas/cuentas/días, remanentes y R/T por operación en los derivados independientes.

### Por qué faltaron4,76USD a K02

Última operación de la primera cuenta funded: SHORT q1, entrada7nov2025 19:26:00.560747663Z SELL24948,25, progreso previo2155,22. Solicitud y admisión R/T144,78/144,78; SL24954,75 proyecta pérdida139,98≤R y TP24940,50 proyecta ganancia145,02≥T, exceso realizable0,24. A19:26:19.626168224Z, step35/106, mark24940,25/ask24940,50 alcanza145,02 y emite MARKET EXIT. En el siguiente step36,19:26:20.186915887Z, mark sube0,25 a24940,50; ask24940,75 más slippage0,25 produce BUY24941. Realizado140,02, fees4,98 una sola vez/slippage embebido. Resultado2155,22+140,02=2295,24; faltante144,78−140,02=4,76.

Fue cierre por objetivo a14:26NY, no liquidación de sesión. Es movimiento causal entre trigger y fill; no prueba defecto de pase, pago ni redondeo. La siguiente solicitud R/T4,76/4,76 no permite protección mínima24,98 bajo estos descriptores: estado `BLOCKED_OBJECTIVE_CAPACITY`, sin retiro de política EOD, infracción artificial ni cobro menor2300. La comparación de rutas intrabar en finalistas es pertinente; no se rebobina este fill ni se modifica la trayectoria publicada.

Evidencia: `verifier/f2-K02-funded-4p76-last-operation-proof.json` SHA256 `cb078424683f482d1421171abcd9d70ead4e1bd3dfe584a99c34923a85d5c9df`. Auditorías `campaigns-F2-FINAL-K01-r2300.json` SHA256 `4f05ee4af8c7e50f4e40be1189747b9ea4c257d0309fe38127ff021258b48b9c`, K02 SHA256 `49d2a2ca1474453162d221cc586179111cffad5003a7b855c07d408b258d0306`; recibos, operaciones completas, censo y métricasV3 referenciados allí. Identidades de campaña K01 `25b60540fb2c8bf33550222cd41c9d6f86d67a2251c190389fac5209a94590cc`, K02 `d7fa8974b2db1329fae0920eacc17ceab8689db0fd4987073e8e23194397846d`, bajo `implementer/evidence/retry1-F2-a9c45059-K0{1,2}-r2300/`. No fixtures en ranking.

### Lanzamiento real

T3 inició2026-10-14T01:31:52Z, supervisor `run_t3_f2.py`, sesión6868; K01/K02-r2300 PID/PGID3021107/3021155, comprobados por manager. Dos campañas en CPU6–8/GOMAXPROCS4; máximo global6 con F0/F1. Admisión libre9,656GB/owned976MB/forecast40≈1,211GB/scratch620KB, conservando≥8GiB y presupuesto nuevo1,5GiB. Progreso `implementer/evidence/T3-f2-progress.json`; ninguna fila económica definitiva al lanzamiento. F3 queda en cola durable y sólo usará plazas libres bajo el mismo máximo.

### Gate independiente

`verifier/independent-f2-gate.json` SHA256 físico `8350ac5f9095de2b22d37bad996cb8c8d61ef837ae0a88a4bcd00d35a7fa7a59`, INDEPENDENT_PASS OFFLINE_OHLC_F2. Source/binario/10inputs íntegros, paridad normativa respecto O10/F0 con delta sólo filtro/identidades/build; dinero común comprobado por blobs conserva gate O10. Coverage104/104 recalculada, oráculo136fronteras variables/exclusión propia y futura PASS0,422s; calendario/DST/gaps/contrato/epoch/readiness PASS0,053s. Smoke23base coincide con oráculo K/ATR/SR60previas,23rechazos de zona/0operaciones/caja5000; receipt sealed COMPLETE e identidad/digests verificados. Manager comprobó hash del gate y sus identidades. Permite iniciar sólo con admisión de recursos global; no certifica runtime ni rentabilidad.

### Freeze y semántica

Source `a9c4505914e897bd3587e3158a3ff9f205dd4948`, árbol `ab0da96849a55c7a15eadc20c8c5a4f712215c97`, checkout `implementer/echo` limpio comprobado por manager. Binario `implementer/bin/echo-backtest-f2` SHA256 físico `4fe35ce7d3e868c34cd48fa808bf7a007fee412bf1bec288350a83d96d71c785`. Manifiesto `implementer/evidence/f2-freeze-manifest.json` SHA256 físico `73ae942c80202a53023cd7df5030cf23ac1dac612c3946a07590004db9aadafa`, diez inputs. Paths de evidencia relativos a `ARANEA_ROOT/work/tradesgerard-operability-20261013`.

SIG-B se conserva. En señal t, S=min(low t−60…t−1), U=max(high t−60…t−1), ancho=ATR20 conocido en t; LONG S≤close≤S+ancho, SHORT U−ancho≤close≤U. La barra propia queda excluida. Epoch/contrato/huecos no explicados reinician disponibilidad; sólo el calendario SDK puede explicar cierre diario, fin de semana o DST. ATR no válido produce causa explícita. No convierte niveles SR en stops ni cambia los SL/TP económicos. F0 no depende de readiness SR.

Integrador reportó blobs monetarios idénticos a O10, suite TG PASS0,158s, delta104/104 y regresión CLI/prefijo3,226s; el gate independiente posterior se registra arriba, separado del gate monetario O10.

### Smoke del productor

Recibo `implementer/evidence/f2-frozen-smoke-receipt.json`: primera sesión,23 cruces base,0 aprobados,23 rechazados por zona con filtro disponible,0 cuentas/operaciones, caja5000. Resultado COMPLETE de diagnóstico, no ranking ni prueba de ausencia de oportunidades en las31 sesiones. No se selecciona una configuración sin actividad por conservar caja.

### Recursos y continuación

Medición inicial del integrador:958.281.533B de evidencia nueva total incluyendo cortes afectados,9.736.310.784B libres, forecast1.193.162.557B≤1,5GiB. Conserva reserva≥8GiB, traza/log≤16MiB, lote≤256MiB y presupuesto agregado sin reinicio por carpeta. Revalidar en cada admisión. F0/F1 pasaron gate e iniciaron antes; T3 se incorporó después del gate propio y de la expansión medida4→6 global descrita en CONTROL. F3 es la conjunción y no añade parámetros.

## Fuentes

- Mandato GOD LOCAL del Owner, PROMPT_VERSION1,2026-10-13.
- [[TRADESGERARD-OPERABILITY-T0]]: política económica y hallazgos técnicos; O10 pendiente de gate al redactar este freeze.
- [[TRADESGERARD-OPERABILITY-T1]] y [[TRADESGERARD-OPERABILITY-T2]]: campañas anteriores preservadas AFFECTED; sus resultados no se reutilizan para representar T3.
