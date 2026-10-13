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

# TRADESGERARD-OPERABILITY-T1

## Propósito

Ejecutar F0 sin filtros con mínimos económicos, retiro EOD, pausa temporal y autoridad monetaria corregidos. Diez configuraciones: K01–K05 × solicitudes brutas2300/3000, misma ventana y perfil C4. Estado vigente **O8_RERUN_RUNNING, 0/10 completas**. O8 corrigió el bloqueo efectivo y pasó verificación independiente; se relanzaron las diez configuraciones. O7 conserva sus observaciones AFFECTED fuera del ranking definitivo. No es aceptación final del Owner.

## Contenido

### Relanzamiento vigente O8

Source `d66bb56bccd053305c1c7dac0dc51aa292745504`, árbol limpio `0083e0d0d9854779c240971d17749593755413a8`; binario SHA256 `a70ac11e481109b036f4a7d792c9594f8c8a73c97eb7c72cd35f2c0c025de8ce`. Manifiesto `implementer/evidence/o8-freeze-manifest.json` SHA256 `9d2623df4cec968a21ab9e761f56dece0160b44e2e671dcf3532628e47795d18`, diez inputs con paridad normativa C4. Gate `verifier/independent-o8-gate.json` SHA256 `0afa455654df3a7362dc1c6e0c8a24a4e871af3e3490f24a71a348ed6f376de0`, INDEPENDENT_PASS técnico, cobertura53/54=98,1481% de bloques del deltaO7→O8. Perfil/datos/ventana C4 permanecen los descritos abajo, sin elegir otra muestra por PnL.

Lanzamiento real2026-10-13T23:26Z: K01–r2300 PID/PGID2963265 y K02–r2300 PID/PGID2963280, concurrencia2; ocho en cola. Harness supervisado session36796, progreso versionado `implementer/evidence/T1-o8-progress.json`. Snapshot O7 inmutable `implementer/evidence/T1-o7-progress-frozen.json` SHA256 `bb86933efb6036d15321e8ae13d661bcd2c524ba8c0c5ade659b0b335901524b`. No se sobrescriben ni se cuentan COMPLETE de otra política/source.

Admisión nueva observada: disco libre10.317.283.328bytes, RAM available64.096.010.240, load1,23/2,47/3,31, evidencia nueva867.852.790bytes y forecast agregado1.102.717.430≤1.610.612.736. La reserva física8GiB, scratch global2GiB, lote256MiB y traza/log16MiB continúan. Recursos incluyen la evidencia O7 retenida; cambiar de directorio no reinicia presupuesto. Concurrencia2 es admisión medida, no benchmark de velocidad bajo contención. Desarrollo H1 aislado continúa y heredará O8 antes de su gate/ejecuciones definitivas.

### Hallazgo posterior: bloqueo efectivo de otras cuentas

La cuenta3 conservó el turno en los seis Q0 del23oct2025 con R/T9,60/9,60, inferior al mínimo ejecutable24,98 de estos descriptores. La auditoría posterior probó que cuentas4 y5 estaban ELIGIBLE desde el reset23oct14Z, flat y drenadas, con q_exec_max0 y sin obligaciones financieras pendientes que lo impidieran. Cuenta4 tenía saldo48385,52; su pausa por capacidad del22oct había vencido. Cuenta5 tenía50100,10; su pausa de sesión también había vencido. Ambas tenían capacidad EOD y diaria restablecida y remanentes de evaluación amplios. La primera cuenta bloqueó a las otras por orden de creación, sin clasificación de pausa por remanente diario ni liberación del turno por bloqueo efectivo.

Esto contradice el mandato vigente de turno hasta bloqueo efectivo y de no permitir que una cuenta inoperable bloquee globalmente a otra utilizable. No invalida la conciliación de la corrida antigua, pero sí su uso como control definitivo de la política autorizada. Corrección requerida: pausa/clasificación temporal por objetivo diario incompatible con la operación mínima, selección causal de otra cuenta, recuperación de la primera cuando corresponda; nunca retiro EOD por ese motivo, incremento de R/T ni reutilización retrospectiva de un cruce ya consumido. Diferenciar remanente diario de remanente real del pase y usar rho/costos/metadata vigentes.

Finding durable `verifier/turn-block-daily-remainder-T1-first.json`, SHA256 `93432c641f2eefb550fcb2d9e49b093df12245e2b51480e46588b91d87ab5bf0`: contiene los seis cruces y MM exactos, estados al primer bloqueo, transiciones ELIGIBLE de cuentas4/5, últimos fills flat y TERMINAL/qmax0, balances/headroom, ausencia de trades/cashflows posteriores y caja4400 en ese momento. Un remanente de pase demasiado pequeño no se clasifica automáticamente como temporal diario ni como ruina EOD; la corrección debe mantener esa distinción.

Dictamen independiente exacto vigente para O7: `verifier/o7-objective-selection-HOLD.json`, SHA256 `804087dff9c8b0ceafc632ae9ec8e71ec30e3f2da2cf746166001b58f9aa3b50`, **INDEPENDENT_HOLD**, source/bin O7 enlazados. Incluye evidencia física y RED del selector. Conserva los checks técnicos/I/O anteriores como evidencia de esos caminos, pero bloquea el ranking económico O7.

Parada efectiva verificada2026-10-13T23:11Z: manager confirmó identidad del supervisor2924335 y grupo K03 propio2949893 y envió un único SIGINT a este último. El harness drenó, registró exit2/FAILED y bloqueó la cola; supervisor y child ya no existen. K01 y K02 conservan COMPLETEexit0, cajas del productor3200/1520 y clasificación externa AFFECTED_NOT_RANKING. K03 conserva reciboFAILED, resultado parcial durable y log `context canceled`, sin imputarlo como pérdida de trading; siete configuraciones no se lanzaron y scratch propio0B. El siguiente freeze repetirá F0×10 tras RED/GREEN y gate independiente; la concurrencia podrá ser2 sólo con medición y presupuesto global. El trabajo H1 aislado no convierte O7 en válida para ranking.

Recibos de parada: `implementer/evidence/T1-o7-invalidation.json`; resultado parcial K03 `implementer/evidence/F0-4f759451-K03-r2300/bce7df396944eb76267d2314599d73f0f9d7f3b828cc1cb82114f6432857cc59/attempt-000001-result.json` SHA256 `58f0fc797bed0b46d8bc0056994e2f45d9ef2a799d7027f2053876e7e214ef50` y `receipt.json` del mismo directorio SHA256 `a29695c99f3e8aa53d4d3c037e9d11a9bebf41e82f93a05d7ee94635efa4b440`. Los COMPLETE anteriores no se sobrescriben ni se cuentan entre las cuarenta definitivas.

### Ejecución O7 anterior, preservada y AFFECTED

Lanzamiento histórico supervisado con concurrencia1. Primer proceso PID/PGID2924374, F0–K01–r2300, terminó exit0 y COMPLETE íntegro; `implementer/inputs/o7-F0-K01-r2300-plan.json`. K02 PID/PGID2933506 también terminó COMPLETEexit0. K03 se canceló después por el hallazgo posterior y las siete pendientes quedaron sin lanzar, como se detalla arriba. Harness del integrador conservó grupos, exit codes, recibos y límites; sin daemon ni promesa de ejecución fuera de esta sesión. Desarrollo H1 en checkout distinto del source/build congelado de T1; auditor consume únicamente COMPLETE íntegros con escritores drenados.

### Primera entrega económica observada, AFFECTED

| Configuración | Base / pasan filtro | Ocupadas / materializadas | Operaciones cerradas / días | Fallback mínimo / rechazos | Compradas / fallidas / retiradas / pasadas | Solicitudes / créditos | Cobrado neto / costos de caja | Caja inicial / mínima / final |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F0–K01–r2300 | 755 / 755 | 36 / 719 | 713 / 31 | 549 / 6 | 15 / 0 / 13 / 0 | 0 / 0 | 0 / 1800 | 5000 / 3200 / 3200 |

Clasificación vigente: **evidencia técnica afectada**, fuera del ranking definitivo. En esta versión se observaron caja neta−1800USD y cero cobros; la clasificación económica inicial «ninguna útil en esta muestra» queda subordinada al hallazgo de selección posterior. Las otras nueve configuraciones aún no se clasifican. Los1800USD son quince compras de120, sin renovaciones, activaciones ni otros débitos de caja observados. El ledger realizado agregado de las quince cuentas es−18825,32USD; no se suma a caja ni se debita otra vez. Dos cuentas quedan preservadas al horizonte: cuenta14 PAUSED_DAILY_GOAL, saldo51130,16 y remanente de evaluación1869,84; cuenta15 PAUSED_SESSION, saldo49250,06 y remanente3749,94. No hay pagos pendientes. Terminal HORIZON_CENSORED; residual nominal de prop no es caja.

Los seis rechazos Q0 son cuenta3 el23oct2025 entre18:51–19:46Z: remanente diario9,60USD, R/T admitidos9,60/9,60, inferior al mínimo ejecutable24,98 de estos descriptores; headroom interno1000 y progreso de evaluación1531,86. Es un objetivo diario temporalmente incómodo, no ruina EOD ni dato faltante. La cuenta se preservó. Las36 oportunidades ocupadas se consumen causalmente por exposición/órdenes sin drenar. UNKNOWN0; no se reutilizan esos cruces.

Hubo312 ganancias netas entre713 operaciones; motivos de orden al cierre397 PROTECTIVE y316 EXIT no equivalen a pérdidas y TP netos. Trece cierres disparados por target realizaron240,04–245,02, por debajo del objetivo250 al fill causal posterior: no se corrige el PnL ni se declara target conseguido por el motivo de salida. Racha máxima ganadora agregada7, neto1665,16; la misma máxima7 pertenece a cuenta3 en EVALUATION. Racha perdedora de campaña12, neto−2784,76; máximos por cuenta/fase permanecen separados en el derivado, sin resets sintéticos. Duraciones: mínimo0,408163s, mediana44,210527s, máximo3187,330827s. Pausas son eventos, no cuentas únicas:19 por capacidad temporal,49 sesión,13 objetivo diario y1 pérdida interna. Los R/T solicitados/admitidos, q, costos, geometría pre/postfill, distancias ATR y progresos por operación están conservados en los derivados auditados.

Antes/después K01–r2300: C4 tuvo19 operaciones y caja4760; O7 tuvo713 y caja3200, ambos sin pase ni cobro. Aumentar operabilidad no demuestra rentabilidad. O7 incluye además la reparación de valoración causal, por lo que no se atribuye toda la diferencia exclusivamente al fallback/retiro. Los713 primeros MM_FILL se contrastaron contra marca actual y autoridad monetaria. Se conservarán análisis de sensibilidad intrabar para los finalistas, sin certificar fills de broker.

La auditoría de progresos encontró máximo2251,84USD en cuenta10: faltaron al menos748,16 al target3000, por lo que no hubo transición omitida por cumplir el importe. Los13 cierres por target inferiores quedaron reconstruidos13/13: submit y fill son cursors adyacentes del modelo causal C4; CycleNet al submit≥250 y el siguiente cursor adverso reduce5USD×q. Ejemplo SHORT: submit con marca25333,25/ask25333,50 y net250,02; siguiente fill25334 y net realizado245,02. Evidencia `verifier/target-exit-cursors-T1-first.json.gz`, SHA256 `5d8721dfe53e75fc46d405a671045fa2f5e4aae4d593623510dd38fa56589be1`. Este resultado no permite garantizar una pérdida física máxima ni certificar ejecución real.

Consistencia al horizonte: el campo `result.accounts.best_day` resume días contables cerrados, no siempre el mayor día efectivo de elegibilidad. Cuenta14 tiene255,02 cerrado y875,14 en el día aún abierto; la autoridad de elegibilidad usa875,14. Su exigencia por consistencia875,14/0,30=2917,1333 sigue por debajo del target3000, por lo que remanente1869,84 es correcto. No se utiliza sólo el campo consolidado para inferir pase.

Esta distinción se añadió sin sobrescribir el derivado ya citado: `verifier/campaign-metrics-T1-first-v2.json.gz`, SHA256 `93276a57121dbf161ded002dbd71740982c65d69442056c4d53f29c2bf485e49`, conserva economía por cuenta/fase y mayor día cerrado, efectivo y actual separados. El archivo original mantiene su hash.

Autoridad vigente de columnas económicas: `verifier/campaign-metrics-T1-first-v3.json.gz`, SHA256 `3285898194fce9d64b2968f7fd8bdd064f5a8e355c0ed245edfdb833244f2aa6`. Distingue R/T de referencia del perfil, solicitud limitada por pendiente antes del headroom, importe admitido después del headroom y proyección efectiva de órdenes. Conserva también las distinciones de mayor día de V2; V1/V2 quedan como derivados anteriores intactos. `tg_preferred_risk/target` son referencias, no solicitudes reducidas por remanente.

Retiro lógico y plaza comercial se auditaron por separado13/13: `policy_retired_at==commercial_slot_released_at`, después del último fill flat y snapshot TERMINAL con `q_exec_max=0`; residual de las operaciones0. Escenario explícito `DESIGN_SCENARIO_LOGICAL_CLOSE_IMMEDIATE_FLAT_DRAINED_NO_REFUND_NO_EXTRA_FEE`. Todas se retiraron antes de `next_renewal`: el escenario evita esas renovaciones futuras, libera plazas y permite nuevas compras, sin reembolso ni cargo de cierre ni segundo débito del costo original. Se preservan saldos/pisos. No se atribuye cancelación real de suscripción. Prueba `verifier/retirement-slot-proof-T1-first.json`, SHA256 `d3e8b7c87cb04f6849ce2b4680490153d67bb08b2dd3308cdfa66141fad2cf18`.

Evidencia física relativa al root nuevo: `verifier/campaigns-T1-first.json` SHA256 `89b1f28675acb484f8babc8c9bc7674286bf7295615cd8a9c5cd81a8bf1b63bd`; `verifier/campaign-metrics-T1-first.json.gz` SHA256 `80668ad69039db97604beac22cd6e5c451e5d8907157fc929a41fbfea9fd467d`; `verifier/receipt-F0-K01-r2300-verified.json` SHA256 `55498c0fa84576c770dc6bf254fbb12be862afd8d587c42326153520d2933ea5`. Operaciones y censo completos en `verifier/operations-K01-r2300-T1-first.json.gz` y `verifier/opportunities-K01-r2300-T1-first.json.gz`. Resultado fuente SHA256 `3a05d7a1ec8faabf93ee25ec2e9b0ed43895d8f3635ad3ab23a2d9fa65bd3381`; traza comprimida1118797bytes SHA256 `a98b5951f5bf4379b617d6905a4f5a35c8530bc49e0b79960b60a54313b1acb3`. Identidad de campaña `8a1d77c82c5d19f1837ae3c4fe8e09ab10e12a05150f2b87eeead51bc5784d48`.

Identidad común: source `4f7594511d381483a161fc59cf0ae7ba00e2cbd1`, binario SHA256 `4ea8b12f3ea0a9ab2b47f5cbb173fb71b424d70cefde004ad82f9df6948ff9ac`, árbol limpio. Gate `verifier/independent-o7-gate.json` SHA256 `6a47a4fad3b5bc7cab8082f879ae180a6d596e98beb160ba41b4c5b4592d236b`, INDEPENDENT_PASS exacto; cobertura299/312=95,8333% de bloques afectados. Perfil `E2T_GAU50_PURCHASE_GE_20260706_OBS_20261012_SCENARIO_V1`. Warmup2025-10-13T17:51Z, trade_start2025-10-14T13:30Z, end_exclusive2025-11-25T23Z; entradas10:00–15:50NY por contrato. Inputs NQZ5 y sus hashes están congelados en `implementer/evidence/o7-freeze-manifest.json`; no MNQ, calendario alternativo ni reoptimización.

El control C4 conserva755cruces base en31fechas y caja final K01/K04=4760,K02=4280,K03/K05=4520 para cada retiro. Comparar después de auditoría completa: C4 permanece como observado, y el nuevo F0 incluye también reparación de valoración stale probada en C4, de modo que no se atribuirá toda diferencia al fallback o al retiro de cuentas. Rachas de campaña y cuenta/fase se conservarán separadas, con caja y ledger conciliados.

Admisión de recursos:792.200.724bytes nuevos existentes +40×4MiB reserva de trazas +64MiB de resultados/logs/filas =1.027.081.748bytes previstos, inferior al agregado1.610.612.736. Los4MiB por traza son reserva, no tamaño prometido: smoke gzip34708bytes/23operaciones, extrapolación755≈1,14MB. Disco libre10.961.649.664bytes y memoria available64.815.595.520bytes observados en admisión; load2,52. Se mantienen8GiB de reserva física,16MiB por traza/log físico,256MiB por lote y expansión de lectura, y scratch global≤2GiB. Medición continua puede detener un lote por límite real, que se reportará como fallo técnico y no pérdida de trading.

La salida NDJSON_GZIP_V1 preserva dinero, operaciones, cuentas, días y causas; recibo incluye encoding/path y hash de bytes cerrados. Decodificación streaming y reconstrucción MM_SIZING_ANCHOR_DELTA_V1 verificadas independientemente. Primer corte económico auditado sin retiros; la clasificación de toda T1 y el ranking de cuarenta siguen pendientes de sus ejecuciones.

## Fuentes

- [[TRADESGERARD-OPERABILITY-T0]], [[TRADESGERARD-OPERABILITY-T0-VERIFY]], [[TRADESGERARD-OPERABILITY-K05-STREAK]], [[TRADESGERARD-ENTRY-REPAIR]].
- Evidencia relativa a ARANEA_ROOT: `work/tradesgerard-operability-20261013/implementer/evidence/T1-progress.json`, `T1-harness.log`, `o7-freeze-manifest.json`; planes individuales bajo `implementer/inputs/` y gate independiente bajo `verifier/` del mismo root.
- Requested TOP model `gpt-6.1-sol`, served UNKNOWN; integrador único y verificador independiente LOCAL. Manager coordina y documenta, no escribe producto/tests/scripts.
