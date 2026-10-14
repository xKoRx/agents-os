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
created: "2026-10-14"
updated: "2026-10-14"
---

# TRADESGERARD-OPERABILITY-RESULTADO

## Propósito

**La racha C4 de12 ganancias no aprobó una cuenta:** las primeras11 fueron de la cuenta1/EVALUATION y sumaron2495,22USD; faltaban504,78 para3000. La operación12 ganó260,04 en la cuenta2/EVALUATION. La racha agregada sumó2755,26, pero ninguna cuenta alcanzó su objetivo. No hubo pérdidas anteriores a la racha; las pérdidas13/14 ocurrieron después. Nueve ganancias255,02, un cierre NY90,02 y un parcial110,02 explican los importes de cuenta1. El mayor día875,08 habría sido29,17% de3000: la consistencia no exigía elevar ese objetivo. La cuenta1 quedó pausada tras cumplir el objetivo diario y la cuenta2 se compró en un cruce posterior, sin reutilizar retrospectivamente la señal. Reconstrucción de las12 filas, pisos, R/T y estados: [[TRADESGERARD-OPERABILITY-K05-STREAK]].

**Estado del alcance: EVIDENCIA TÉCNICA E HISTÓRICA INCOMPLETA POR RECURSOS.** Producto O11 y los cuatro filtros están implementados y verificados offline; sólo6 de40 campañas tienen resultado económico completo auditado. Cuatro intentos F0 adicionales fueron drenados por el guard físico de disco y30 configuraciones permanecen sin ejecutar. No se presenta un ranking final de40, no se seleccionan finalistas y no se declara aceptación del Owner ni cierre del proyecto.

## Contenido

### Identidades y alcance técnico

Fuente común `5de33134311f3a23a306d12d1c8fabbf5222c502`, árbol `1f5ade0301125728bbfcc368cdce858956a5f371`; branch local `codex/tradesgerard-authority-handover-20261014`. Binario O11 SHA256 `734c923804fff719b1037953a387b715cc57e41f988775970b48038cea1b55a7`; manifiesto40 SHA256 `60bf4e0a62ca6704a88a3d55f025c2cfce36ae1a8fcc0e0d05b30998bac03098`. Gate independiente `ecb199bad5e32eefcfa87fa7cf73e72ed10451aedf0a106f2b8447d002dddd87`:29pruebas independientes, cobertura delta36/37=97,2973%, denominador/baseline466e4f17 y perfil de cobertura conservados. Cobertura no sustituye auditoría económica. Integrador y verificador LOCAL solicitados Sol6.1; modelo servido UNKNOWN.

Políticas nuevas comunes: q de referencia ATR cuando es válido, fallback exacto q_min con SL/TP económicos legales sin aumentar R/T, redondeo y costos causales; retiro lógico `RETIRED_UNTRADEABLE_BY_POLICY` sólo por insuficiencia EOD permanente, flat y órdenes/claims drenados. Pausa diaria temporal y error técnico de autoridad se distinguen del retiro. Liberación inmediata de plaza tras retiro lógico es DESIGN_SCENARIO, sin devolución ni cargo extra, no una afirmación comercial de Earn2Trade. C4 permanece preservado; sus rechazos por la política antigua no se reclasifican retrospectivamente como bugs.

O11 también corrige autoridad monetaria tras transición de fase: se instala contexto antes de proyectar economía, se exige frescura de cuenta/revisión/contexto y se drena antes del handover. El contraejemplo K04 ahora entra con LIVESIM/balance50000/revisión27403 vigente. Fuente/build/planes permanecieron inmutables durante las campañas. F0 sin filtro; F1 SMA24 de H1 cerradas; F2 extremos de las60 velas previas con zona1ATR; F3 conjunción exacta. Los oráculos causales y negativos no se cuentan como campañas ni ingresos.

Perfil común `E2T_GAU50_PURCHASE_GE_20260706_OBS_20261012_SCENARIO_V1`. NQ, contratos enteros, tick0,25,20USD/punto; costos y modelo OHLC causales conservados. Ventana económica C4: warmup1m2025-10-13T17:51Z, trading desde2025-10-14T13:30Z, fin exclusivo2025-11-25T23Z;31fechas y755cruces NY auditados en cada campaña completa. El prefijo H1 causal se vincula en los planes F1/F3; no altera el inicio de trading. Caja5000, compra120 a demanda, renovación120/30días donde corresponde; retiros brutos2300/3000, split80%, fee50 y primer fee139 cuando aplican. No se utilizó el escenario personal de cinco cuentas/diez intentos/dos semanas.

### Resultado económico observado, sin extrapolar las34 pendientes

| Filtro/perfil/retiro | Ops | Fallback | Compradas / retiradas / fallidas / pases | Solicitudes / créditos | Neto acreditado | Costos compra / renovación | Caja mínima / final | Cambio de caja |
|---|---:|---:|---|---|---:|---|---|---:|
| F0/K01/2300 |719|550|15 /13 /0 /0|0 /0|0|1800 /0|3200 /3200|−1800|
| F0/K01/3000 |719|550|15 /13 /0 /0|0 /0|0|1800 /0|3200 /3200|−1800|
| F0/K02/2300 |618|215|29 /26 /0 /4|0 /0|0|3480 /0|1520 /1520|−3480|
| F0/K03/2300 |647|442|26 /20 /1 /5|1 /1|1651|3120 /0|2240 /3531|−1469|
| F0/K04/2300 |651|525|18 /14 /0 /2|0 /0|0|2160 /0|2840 /2840|−2160|
| F0/K05/2300 |543|471|24 /17 /1 /4|2 /1|1651|2880 /0|2480 /3771|−1229|

Cada fila es una trayectoria independiente con caja inicial5000. No se suman sus cajas, pagos o señales como una campaña ni como ensayos independientes de mercado. Los seis cambios de caja son negativos. K03/K05 **cobraron en la muestra, pero no tuvieron caja neta positiva**. K05 conserva una segunda solicitud2300 aprobada para crédito28nov, fuera del fin25nov23Z: no se acredita anticipadamente. Los créditos observados fueron el20nov2025 15Z, cuenta11/LIVESIM en sus respectivas trayectorias:2300×80%−50−139=1651. Primer crédito37,0625días calendario desde trade_start; no dos semanas. Fees se descuentan una vez, no nuevamente de caja.

El snapshot económico completo `verifier/notes/F0-5de33134-audited-6-rows-v2.json` SHA256 `f9d7c147ff6293dbeb710ff73a7dc8df7e2345334a00f560695e11fcec3a5005` conserva señales/ocupación/rechazos,31días con entrada, cuentas y pausas, ledger/pisos/remanentes, tiempos hasta pase, R/T efectivos, q, geometría ATR, duraciones y rachas por cuenta/fase y campaña. [[TRADESGERARD-OPERABILITY-T1]] publica esas columnas y recibos por fila. UNKNOWN0 en las seis campañas. El par K01 tiene trayectoria completa idéntica porque nunca llegó a funded; los cuatro pares restantes todavía carecen de resultado completo para3000. Ningún saldo nominal retenido se incorpora a caja.

Orden provisional de las seis por caja final: K05/2300(3771), K03/2300(3531), K01/2300 y3000(3200), K04/2300(2840), K02/2300(1520). **No es selección final de pares:** faltan todas las campañas F1/F2/F3 y cuatro F0. No se profundiza un candidato por ganar un empate sin actividad ni se recomienda operar con estos datos.

### Cobertura exacta de las40 configuraciones

Tabla y métricas completas en `verifier/final-comparison-o11-incomplete-40.json.gz`, SHA256 `959ce944b20c838c9d5deab35c25d4150d11f6551f768aec9914b4c1e5fe1af0`,41.762B, readback40/40. Estados:6 `AUDITED_COMPLETE`,4 `FAILED_TECHNICAL_RESOURCE`,30 `NOT_RUN_RESOURCE`. Las34incompletas tienen economía NA, no ceros fabricados. Recibo independiente de los cuatro fallos `verifier/o11-four-failed-independent-final.json.gz`, SHA256 `cb6146eec4ca69a778272caccf5c5cc06f1dbd616c62c8462d451875eb5ed086`: identidad/request/source/binario/exit2/context canceled y ausencia de PID comprobados; no certifica PnL parcial.

F1/F2/F3 abrevían F1-TREND/F2-SR/F3-TREND-SR. Compras en USD; NA significa evidencia económica incompleta. Los costos restantes y el censo completo de las seis filas están en T1 y en el JSON vinculado.

| Filtro | Perfil | Retiro bruto | Estado técnico | Ops | Neto acreditado | Compras USD | Caja final | Neto caja |
|---|---|---:|---|---:|---:|---:|---:|---:|
| F0 | K01 |2300|AUDITED_COMPLETE|719|0|1800|3200|−1800|
| F0 | K02 |2300|AUDITED_COMPLETE|618|0|3480|1520|−3480|
| F0 | K03 |2300|AUDITED_COMPLETE|647|1651|3120|3531|−1469|
| F0 | K04 |2300|AUDITED_COMPLETE|651|0|2160|2840|−2160|
| F0 | K05 |2300|AUDITED_COMPLETE|543|1651|2880|3771|−1229|
| F0 | K01 |3000|AUDITED_COMPLETE|719|0|1800|3200|−1800|
| F0 | K02 |3000|FAILED_TECHNICAL_RESOURCE|NA|NA|NA|NA|NA|
| F0 | K03 |3000|FAILED_TECHNICAL_RESOURCE|NA|NA|NA|NA|NA|
| F0 | K04 |3000|FAILED_TECHNICAL_RESOURCE|NA|NA|NA|NA|NA|
| F0 | K05 |3000|FAILED_TECHNICAL_RESOURCE|NA|NA|NA|NA|NA|
| F1 | K01 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F1 | K02 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F1 | K03 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F1 | K04 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F1 | K05 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F1 | K01 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F1 | K02 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F1 | K03 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F1 | K04 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F1 | K05 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F2 | K01 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F2 | K02 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F2 | K03 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F2 | K04 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F2 | K05 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F2 | K01 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F2 | K02 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F2 | K03 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F2 | K04 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F2 | K05 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F3 | K01 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F3 | K02 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F3 | K03 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F3 | K04 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F3 | K05 |2300|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F3 | K01 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F3 | K02 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F3 | K03 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F3 | K04 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|
| F3 | K05 |3000|NOT_RUN_RESOURCE|NA|NA|NA|NA|NA|

### Antes y después de operabilidad

| Perfil, retiro2300 | Operaciones C4 → O11 | Caja final C4 → O11 |
|---|---|---|
| K01 |19 →719|4760 →3200|
| K02 |24 →618|4280 →1520|
| K03 |14 →647|4520 →3531|
| K04 |34 →651|4760 →2840|
| K05 |25 →543|4520 →3771|

Mayor operabilidad no produjo caja neta positiva en estas cinco comparaciones. Incluyen las nuevas políticas y correcciones causales comunes, por lo que no aíslan el efecto de una única política. Las cuentas que quedan bajo el mínimo legal permanente se retiran sin falsa infracción ni doble débito; geometría ATR insuficiente por sí sola no implica ruina. El mínimo depende de tick/costos/ejecución: no se reutiliza19,98 como constante universal. Remanente330 con perfil500/500 solicita330/330; K05 mantiene T≤250. Conservación económica, límite diario y protección legal verificados en positivos/negativos.

En C4, el ledger final de las dos cuentas K05 fue+460,46 y−739,92, total−279,46; caja externa4520=5000−240compras−240renovaciones, sin crédito. Esta conciliación es distinta de los resultados O11 y del saldo de un último compartimento.

### Bloqueo físico, integridad y reanudación

El intento F0 `f0-stage3`, supervisor3118487/sesión87792, arrancó con seis COMPLETE exactos y cuatro hijos K02–K05/r3000. A26min43s el guard registró `RUNTIME_RESOURCE_LIMIT`: supervisor e hijos exit2, recibos FAILED/context canceled, todos los PID drenados y ausentes. No se interpreta cancelación técnica como pérdida de trading ni se usa un ledger parcial en el ranking. Snapshot SHA256 `57d9b0a09ef8d8e84c92c62122255af23cd22787d40811790c35a2f1af2c81ca`; recibo `implementer/evidence/o11-F0-stage3-resource-drain-receipt.json`.

La lectura posterior al drenaje fue8.553.541.632B libres, bajo el piso8.589.934.592B. Una lectura posterior del manager fue8.607.608.832B: el espacio fluctúa, pero tampoco admite el presupuesto vigente F0 de60.817.408B adicionales. Ese contrato requiere al menos8.650.752.000B libres en el momento de admisión, además de caps agregados/RAM/CPU válidos. No se atribuye el consumo externo a un proceso específico ni se alteran servicios, permisos, corpus, caches o archivos ajenos. Una reserva adicional de4MiB fue propuesta por solapamiento de temporales ya incluidos en configTOTAL, pero no se aplicó al intento ni se usa como autorización retrospectiva.

La recuperación propia ya ejecutada preserva todo: archivos históricos gzip, cuatro fuentes anteriores y fuente O11 archivadas con bundles/refs/mapas, y16binarios históricos en archivo durable64.492.288B SHA256 `5b086b7fe334478fe97fdef7bf4775c714b42015140064a4f8a6a7b857b946fc`. Este último ahorró70.902.742B netos una sola vez tras fsync/readback16/16. C4, O11 activo y planes40 intactos. No se inicia otra escalera de reintentos sin recuperación real y admisión nueva.

Reejecución verificable: `implementer/evidence/REEXECUTION-O10-FILTERS.md` comienza por O11 vigente; su sección posterior O10/F2/F3 es historia AFFECTED. Usar el binario O11 retenido y gate exacto, un attempt-id nuevo y el supervisor parametrizable `run_o11_scoped.py`; hacer dry-run con medición actual, luego ejecución sólo si pasa. Reanuda únicamente COMPLETE con identidad/request/digests/CRC íntegros; conserva los FAILED anteriores. El source está archivado, no hace falta restaurarlo para correr el binario. Recompilar produciría otra identidad y requeriría nueva verificación; no se hizo durante esta tanda. Las recetas y mapas están en workspace, con referencias y hashes en Agents-OS.

### Datos adicionales y límite de runtime

Inventario físico:13contratos NQZ3…NQZ6, alrededor de1,2millones de barras1m,2023-10-01…2026-10-06. No equivale a un año listo para backtest. El preflight anual fijado2025-10-02…2026-10-02 falló `ANNUAL_NOT_READY_UNDER_PINNED_MODEL_CALENDAR`: hueco físico NQZ5 del13oct2025 y calendario semanal sin overrides suficientes de festivos/cierres. No se rellenaron precios ni se inventó una corrección de calendario; no se probó rentabilidad anual ni de tres años.

Intervalo adicional reservado antes del ranking: NQZ6, warmup2026-09-21T00Z, trading2026-09-22T14Z…2026-10-02T21Z exclusivo.13680minutos esperados, cero faltantes en esa comprobación, prefijo37H1 completas. Fuente SHA256 `2176dce88405aee7fe5383cf1244330ad83fe0b0f1105abe9c7b198a30555141`. Es exploratorio; uso previo desconocido, no holdout intacto certificado. Las hasta cuatro campañas adicionales y la sensibilidad intrabar permanecen **NOT_RUN_RESOURCE**, sin selección de finalistas de una matriz incompleta. El WIP de sensibilidad no tiene gate/binario independiente sobre O11: no se certifica robustez al orden intrabar con stops cercanos.

Runtime sigue **FUNCTIONALLY_BLOCKED** para mínimos económicos F0–F3: falta `ExecutableQuoteSource` fresco en SnapshotViews/readModelMarket; offsets OHLC sólo son válidos en BACKTEST. F1/F3 además requieren autoridad de completitud H1 en startup/reconexión/epoch; F2/F3, minutos cerrados válidos. No se iniciaron ni certificaron quote/fill/cancel/finality/márgenes de NinjaTrader/broker. Compartir matemática no demuestra operabilidad LIVE. No órdenes, compras/resets reales, deploy, permisos, servicios, merge ni release.

La siguiente acción queda limitada a recuperar capacidad y completar la matriz definida. No hay evidencia suficiente para añadir otra hipótesis de trading o más indicadores, ni para declarar ninguna variante generalmente rentable. Quedan diferidos sin implementar addsB2, martingala, aumento deR tras ganancias, BE, extensión, nuevos ratios/horarios y selección de cuentas por rendimiento. No se reactivó el catálogo15.168.

## Fuentes

- [[TRADESGERARD-OPERABILITY-K05-STREAK]], [[TRADESGERARD-OPERABILITY-T0]], [[TRADESGERARD-OPERABILITY-T0-VERIFY]], [[TRADESGERARD-OPERABILITY-T1]], [[TRADESGERARD-CONTROL]], [[TRADESGERARD-ENTRY-REPAIR]].
- Workspace `/home/kor/aranea/work/tradesgerard-operability-20261013/`: manifiestos/inputs/build en implementer; recibos/oráculos/filas económicas en verifier. Datos pesados permanecen allí; este informe no reemplaza su evidencia.
