---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-CONTROL]]"
  - "[[TRADESGERARD-B-RESULTADO]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-15"
---

# TRADESGERARD-ENTRY-REPAIR

## Propósito

Reparar y verificar el recorrido de oportunidades TradesGerard KISS-1 bajo el mandato del Owner del 2026-10-13. El objetivo es funcionamiento correcto, no rentabilidad. Este es el único informe de reparación; los resultados históricos permanecen conservados.

## Contenido

### Recuperación de archivos y Git — 2026-10-15

Estado de recuperación: **SOURCE_BYTES_VERIFIED / GIT_LINEAGE_RECOVERY_IN_PROGRESS**. Este estado describe la recuperación posterior al borrado del repositorio común, no una repetición de las campañas del13-oct. El resultado funcional histórico siguiente conserva sus recibos y alcance.

El rescate en `/srv/echo-work/rescate-20261014-rootdisk/tradesgerard-entry-repair-20261013` conserva los1848 archivos del scope del manifiesto C4:1848/1848 coinciden físicamente en `implementer/echo-c4`, cero ausentes o diferentes. Binario C4 conservado:15.886.491 bytes, SHA256 `c8849bb6e5523e8625ead8282f0d97f98d8b02e14d72838e3c35de207c6bcd57`. Readback independiente `/srv/echo-work/recovery-verify-20261015/source-integrity.json`. El scope incluye archivos regulares versionados v3 y workspace; por sí solo no acredita aún el tree Git de todo el repositorio ni los objetos commit perdidos.

El árbol Git completo C4 y el objeto commit ya se reconstruyeron exactamente en el repositorio aislado: tree `935e74d6056ffb3593f5a9a5deb8771ea6214bcd`, commit `88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49`. Manager comprobó `git cat-file -t/-p`: objeto commit, padre `26f3459cba47fd05f5ef9aed3d205c3c5bbad81a`, epoch1791913284 y timezone−0300. La coincidencia del hash acredita bytes completos del objeto; la conectividad de padres todavía se reconstruye y no se declara repositorio completo.

Corrección al reporte de reconstrucción recibido: los dos archivos productivos distintos y cuatro tests ausentes describen la comparación entre los dos árboles rescatados, no el delta acumulado B→C4. El handoff original acredita15 archivos productivos acumulados. La metadata de directorio09:31/13:39 no fecha el contenido final de todos sus archivos. Tampoco TASKS pendiente al freeze invalida las tareas5–7 ejecutadas después: existen los recibos de diez campañas finales y su verificación independiente, sin necesidad de repetirlas para recuperar Git.

Se reconstruye en un repositorio nuevo bajo `/srv/echo-work/recovery-entry-20261015`; rescate, repos temporales de otras sesiones y rollouts permanecen sólo lectura. Verificador independiente separado bajo `/srv/echo-work/recovery-verify-20261015`. Prioridad: objetos y árboles exactos, padres/autor/committer/fechas/mensaje; los mensajes y timestamps de rollout por sí solos no garantizan el SHA original. Los bundles downstream requieren ancestros perdidos: no se presentan como autónomos hasta resolverlos. No se ejecuta nuevo tallado del disco ni se afirma imposibilidad universal de recuperación ext4 a partir del intento fallido reportado. Sin push ni mutación de refs ajenas en esta fase.

### Estado vigente

**CORRECTED_AND_VERIFIED — funcionamiento offline.** Fuente congelada `88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49`, binario SHA256 `c8849bb6e5523e8625ead8282f0d97f98d8b02e14d72838e3c35de207c6bcd57`. Las diez configuraciones K01–K05 ×2300/3000 terminaron COMPLETE con exit0 y pasan la auditoría independiente completa sobre esa misma build: indicadores, identidades, particiones, autoridad monetaria contemporánea, ledger/caja, cierres y calendario. Cero oportunidades o cierres C4 UNKNOWN y cero findings monetarios. No se deduplicaron retiros: la igualdad entre cada par se comprobó después de sus ejecuciones y auditorías separadas.

Se reprodujeron y corrigieron pérdidas funcionales por ciclo técnico diario, finalidad incompleta, ATR/readiness, compra/selección y entrega diaria de economía incompleta. El censo independiente contiene42.969 barras físicas,10.850 barras de entrada NY y755 oportunidades en31 fechas. Cada campaña C4 observa las mismas755 identidades; la diferencia entre perfiles queda downstream, explicada por exposición y economía. Las operaciones con fills por retiro pasan de32 a116 (+84): K01–K05 de0/18/7/1/6 a19/24/14/34/25. No se cambiaron R/T, mercado, corpus, fees ni multiplicadores para producir esa recuperación.

Dictamen independiente físico: `verifier/independent-final-progress-summary.json` VERIFIED_TEN y `verifier/final-T1-receipt-readback-final-88ed70d1.json` FULL_GATES_VERIFIED_TEN, receipt_verified=full_verified=10. Matriz de los doce casos, exact gate, recibos y derivados completos enlazados abajo. Los resultados B originales siguen preservados y COMPLETE históricamente; su explicación de frecuencia queda AFFECTED y reemplazada por esta comparación. C3 y anteriores son referencias supersedidas, no resultados finales. Aceptación del Owner separada; no se afirma rentabilidad, broker real, LIVE, release, merge productivo ni despliegue. Dictamen final `verifier/independent-final-dictamen.json`: VERIFIED10/10, cero findings productivos abiertos. Presentación dimensional revisada y procesos propios drenados; límites de evidencia explícitos más abajo.

El emparejamiento causal B→C4 K02/K03 r2300 conserva755 identidades, sin cruces exclusivos de ninguno de los dos lados. En K02:666 evaluaciones recuperadas desde owner abierto sin exposición,36 cruces evaluados por ambos con trayectoria económica distinta,46 admisiones ahora distintas por pausa/exposición histórica,3 recuperadas en la frontera de pausa vencida y4 sin nueva materialización por ocupación actual. K03:705/36/5/3/6 respectivamente. Las categorías son excluyentes; los efectos de latch y finalización no se suman sobre un mismo cruce. Evidencia íntegra: `verifier/causal-full-B-vs-C4-K02-r2300.json.gz` y `...-K03-r2300.json.gz`, leídas físicamente por el manager.

K01 r2300 final verificado: **0→19 operaciones con fills**, 31→750 evaluaciones MM,38 registros de fill,46 órdenes distintas,731 rechazos de tamaño y5 cruces consumidos durante exposición. Sus755 identidades/indicadores y750 snapshots monetarios concilian, cero cierres UNKNOWN:8 por target de ciclo y11 por stop. Cuatro días con entradas (3/2/10/4 operaciones), duración mínima/mediana/máxima17,409/230,547/1449,675 segundos, rachas máximas ganadora5/perdedora9. Fuente: `verifier/independent-final-progress-summary.json`, consolidación10/10.

La baja actividad posterior queda explicada en estas tres campañas, sin ciclo fantasma: K01 encuentra margen EOD15,28 desde21oct18:05Z y vuelve a evaluar619 cruces; K02,10,16 desde20oct15:01Z y658 cruces; K03,0,20 desde20oct15:29Z y655 cruces. Todos esos intentos posteriores dan Q0 por TG_SIZE_BELOW_MINIMUM con autoridad monetaria vigente; ninguno produce fill. Son primeras observaciones MM del límite, no una atribución al tick exacto en que apareció. Evidencia con ledger/pisos/revisión y cuenta: `verifier/persistent-sizing-floor-final-88ed70d1.json.gz`.

El mínimo19,98 se refiere exclusivamente al modelo de geometría positiva de un tick antes del fill (5+4,98+10); no es un mínimo universal de bolsa. K02 conserva otras dos cuentas y K03 otra con margen final1100; el orden de selección contractual vuelve a la primera cuenta elegible. Saltar una cuenta cuyo margen EOD persistente ya no permite el mínimo del sizing vigente es la propuesta separada no aplicada, con efecto sobre selección/caja y sin prometer fills. Ampliar ATR no resuelve esta aritmética.

K04/K05 quedan explicados por la geometría y los límites efectivos de cada cruce, no por estar debajo de19,98. Después de la última entrada K04 (28oct14:30:00,560747663Z) hay500 cruces:1 ocupado y499 reevaluados/Q0. La pérdida geométrica neta de un contrato va de229,98 a2344,98 frente a R efectivo110,82. Después de la última entrada K05 (28oct16:14:01,224489795Z) hay494 cruces, todos reevaluados/Q0: pérdida unitaria entre444,98 y4679,98, R efectivo entre255,04 y460,46. Los extremos de esas series no se comparan entre sí: en el cruce más barato,28oct18:54Z,444,98 excede el R permitido255,04 por remanente diario interno, aunque el Hard Provider contemporáneo era355,04. Cada fila acredita por separado floor(R/pérdida unitaria)=0; no se aplican márgenes dos veces. Evidencia íntegra: `verifier/post-entry-geometry-final-88ed70d1.json.gz`, primera y última decisión conservadas. La propuesta de selección por imposibilidad mínima persistente no se extiende a K04/K05.

### Comparación final verificada de los cinco perfiles, ambos retiros

Cada fila aplica tanto a retiro2300 como a3000, comprobados mediante diez ejecuciones propias. Conserva755 oportunidades NY del mismo mercado e historial. Antes = B físico observado y equivalente a sus resultados históricos; después = C4 exacto. Las operaciones cuentan ciclos con fills, no tickets. Las cantidades entre paréntesis son diferencias absolutas.

| Perfil | Evaluaciones MM antes→después | Rechazos tamaño antes→después | Operaciones antes→después | Fills después | Órdenes después | Ocupados después | Caja antes→después |
|---|---:|---:|---:|---:|---:|---:|---:|
| K01 |31→750|31→731|0→19 (+19)|38|46|5|4760→4760|
| K02 |36→751|18→727|18→24 (+6)|48|61|4|4760→4280|
| K03 |36→749|29→735|7→14 (+7)|28|36|6|4760→4520|
| K04 |31→715|30→681|1→34 (+33)|68|91|40|4760→4760|
| K05 |35→705|29→680|6→25 (+19)|50|71|50|4760→4520|

Particiones exactas por perfil: admisiones MM con entrada + rechazos de tamaño + ocupado consumido =755. No hay UNKNOWN; los permisos Provider son permisos a Operation previos al MM y no equivalen a órdenes. Las755 OPEN se emiten en cada configuración antes y después; el defecto estaba en su recepción/ciclo y en rutas económicas, no en ausencia de cruces de K. Provider denied=0 en las diez; los rechazos consignados son MM. Los cinco pares físicos concuerdan después de verificarlos individualmente: `verifier/C4-retirement-pair-measured-equivalence.json`.

Resumen humano externo `verifier/C4-T1-independent-summary.md`; detalle íntegro por operación, cuenta y día en `verifier/operation-account-day-aggregates-final-88ed70d1.json.gz` y matriz de31 fechas `verifier/complete-NY-entry-day-matrix-final-88ed70d1.json.gz`. Las duraciones van del primer fill al cierre físico; rachas por neto después de fees en orden de cierre, cero reinicia. Día NY de entrada y día contable permanecen separados.

| Perfil | Órdenes B→C4 | Días NY con entrada B→C4 | Duración min/mediana/max s B→C4 | Racha ganadora/perdedora B→C4 | Cierres C4 |
|---|---:|---:|---|---|---|
|K01|0→46|0→4|—→17,41/230,55/1449,67|0/0→5/9|8 target,11 SL|
|K02|45→61|14→5|12,63/259,43/1071,93→14,39/136,81/1294,89|2/3→4/3|11 target,13 SL|
|K03|19→36|5→4|19,47/468,22/800,27→14,39/261,45/1163,77|3/1→3/3|6 target,7 SL,1 cierre NY|
|K04|2→91|1→8|800,27/800,27/800,27→17,41/567,26/7502,26|0/1→8/4|22 target,11 SL,1 cierre NY|
|K05|16→71|2→9|14,93/1486,94/2432,53→59,63/552,43/13558,97|2/1→12/2|18 target,5 SL,2 cierres NY|

El histórico B conserva dos motivos MM CLOSED genéricos por retiro (uno K02 y uno K03); no se inventa TP desde su PnL. Los demás cierres B constan en el resumen independiente. Fill records C4=38/48/28/68/50; unidades ejecutadas=38/54/28/82/54, magnitudes distintas.

| Perfil | Cuentas B→C4 | Neto retenido USD B→C4 | Pausas por sesión B→C4 | Pausas objetivo diario B→C4 |
|---|---:|---:|---:|---:|
|K01|1→1|0→−709,62|32→31|0→0|
|K02|1→3|−1984,64→−729,46|30→91|2→2|
|K03|1→2|690,14→−1624,72|32→61|0→1|
|K04|1→1|−499,98→110,82|32→31|0→0|
|K05|1→2|−979,88→−279,46|32→57|0→1|

Pases y cobros=0 antes/después en los diez: fase EVALUATION, gross_paid cero y ausencia de eventos CREDIT/PAYOUT acreditados; payments:null no es prueba aislada. Pausas son transiciones reales por cuenta, no cantidad de sesiones. B incluye una PAUSED_SESSION adicional durante el prefijo de preparación13oct19:55Z, anterior a trade_start; no es un día extra de entrada ni callback repetido. Referencias `verifier/payout-pause-proof-final-88ed70d1.json.gz` y `verifier/baseline-pause-session-prefix-scope.json`.

| Fecha NY de entrada | K01 | K02 | K03 | K04 | K05 |
|---|---:|---:|---:|---:|---:|
|2025-10-14|3|16|4|3|3|
|2025-10-15|2|4|5|3|3|
|2025-10-16|0|1|0|0|0|
|2025-10-17|0|2|3|0|1|
|2025-10-20|10|1|2|6|6|
|2025-10-21|4|0|0|2|1|
|2025-10-23|0|0|0|3|3|
|2025-10-24|0|0|0|11|2|
|2025-10-27|0|0|0|5|4|
|2025-10-28|0|0|0|1|2|

Los demás días de las31 fechas tienen cero entradas. Todos los nuevos cruces posteriores siguen evaluándose o se consumen por exposición real, sin backlog ni un intento por día.

### Sizing final: primeras decisiones físicas antes/después

Presentación del integrador revisada independientemente: `verifier/sizing-presentation-independent-readback.json`. Fuente íntegra con hashes y las trazas de cada fila: `implementer/evidence/c4-sizing-presentation.md`. Se conserva aquí la tabla de lectura, derivada de los mismos artefactos; el manager no escribió código diagnóstico.

NQZ5: tick 0.25 puntos, 5 USD/tick, 20 USD/punto. Comisión 2.49 USD por lado y contrato; deslizamiento de un tick por lado. Coste de ida y vuelta: 2×2.49 + 2×5 = 14.98 USD/contrato. USD en presupuestos y costes; ATR/distancias en puntos. R=riesgo, T=objetivo, A=primera admisión MM y R en la identidad de fila=primer rechazo MM. Fechas de 2025, hora de Nueva York.

La tabla muestra las primeras decisiones observadas de cada perfil r2300, tomadas de los extractos auditados. B tiene equivalencia histórica 2300/3000 probada en su recibo; C4 ejecuta las diez identidades por separado. Esta presentación no sustituye sus recibos individuales. K01 B no admite ninguna entrada en el horizonte completo observado.

**OHLC y postfill:** los extractos se enriquecen por identidad y timestamp exactos con oráculo físico y trazas originales. No se usa balance final. `mark` es el precio usado por MM; antes se observó después de la evaluación dentro del mismo alcance inmutable de decisión. ATR B y ATR C4 son los valores físicos de cada versión, no un único ATR sustituido.

#### Geometría y múltiplos efectivos

Pérdida SL y ganancia TP son por contrato, netas del coste común. Los múltiplos geométricos mSL=ΔSL/ATR y mTP=ΔSL/(rho×ATR) son aritmética de los campos retenidos; mTP no es una barrera postfill ni una orden de precio acreditada.

| Versión/perfil/caso | NY; dirección; OHLC O/H/L/C | ATR; rho | mark → ancla SL; ΔSL | SL neto / TP neto por contrato | mSL / mTP |
|---|---|---|---|---|---|
| B K01 A | sin admisión en el horizonte B completo | — | — | — | — |
| B K01 R | 10-14 10:33; SHORT; **24684.5/24706.25/24684.5/24697.0** (NT#31732) | 22.75; 1 | 24697 → 24719.75; 22.75 | 469.98 / 440.02 | 1.000000 / 1.000000 |
| C4 K01 A | 10-14 14:12; LONG; **24892.5/24903.5/24891.5/24900.0** (NT#31951) | 11.5891883; 1 | 24900 → 24888.5; 11.5 | 244.98 / 215.02 | 0.992304 / 0.992304 |
| C4 K01 R | 10-14 10:33; SHORT; **24684.5/24706.25/24684.5/24697.0** (NT#31732) | 22.91274922; 1 | 24697 → 24719.75; 22.75 | 469.98 / 440.02 | 0.992897 / 0.992897 |
| B K02 A | 10-14 10:33; SHORT; **24684.5/24706.25/24684.5/24697.0** (NT#31732) | 22.75; 1 | 24697 → 24719.75; 22.75 | 469.98 / 440.02 | 1.000000 / 1.000000 |
| B K02 R | 10-16 10:27; SHORT; **25100.0/25100.5/25046.25/25050.5** (NT#34486) | 24; 1 | 25050.5 → 25074.5; 24 | 494.98 / 465.02 | 1.000000 / 1.000000 |
| C4 K02 A | 10-14 10:33; SHORT; **24684.5/24706.25/24684.5/24697.0** (NT#31732) | 22.91274922; 1 | 24697 → 24719.75; 22.75 | 469.98 / 440.02 | 0.992897 / 0.992897 |
| C4 K02 R | 10-14 12:25; SHORT; **24851.75/24862.25/24848.25/24851.75** (NT#31844) | 17.44378046; 1 | 24851.75 → 24869; 17.25 | 359.98 / 330.02 | 0.988891 / 0.988891 |
| B K03 A | 10-20 10:16; SHORT; **25238.0/25238.75/25219.25/25227.75** (NT#37235) | 14.5; 1.5 | 25227.75 → 25249.5; 21.75 | 449.98 / 275.02 | 1.500000 / 1.000000 |
| B K03 R | 10-14 10:33; SHORT; **24684.5/24706.25/24684.5/24697.0** (NT#31732) | 22.75; 1.5 | 24697 → 24731; 34 | 694.98 / 65753/150 (≈438.353333) | 1.494505 / 0.996337 |
| C4 K03 A | 10-14 12:12; LONG; **24772.75/24796.75/24772.75/24795.5** (NT#31831) | 16.26249087; 1.5 | 24795.5 → 24771.25; 24.25 | 499.98 / 46253/150 (≈308.353333) | 1.491161 / 0.994108 |
| C4 K03 R | 10-14 10:33; SHORT; **24684.5/24706.25/24684.5/24697.0** (NT#31732) | 22.91274922; 1.5 | 24697 → 24731.25; 34.25 | 699.98 / 66253/150 (≈441.686667) | 1.494801 / 0.996534 |
| B K04 A | 10-28 10:28; LONG; **26044.5/26047.0/26033.5/26041.25** (NT#45527) | 12; 2 | 26041.25 → 26017.25; 24 | 494.98 / 225.02 | 2.000000 / 1.000000 |
| B K04 R | 10-14 10:33; SHORT; **24684.5/24706.25/24684.5/24697.0** (NT#31732) | 22.75; 2 | 24697 → 24742.5; 45.5 | 924.98 / 440.02 | 2.000000 / 1.000000 |
| C4 K04 A | 10-14 14:12; LONG; **24892.5/24903.5/24891.5/24900.0** (NT#31951) | 11.5891883; 2 | 24900 → 24877; 23 | 474.98 / 215.02 | 1.984608 / 0.992304 |
| C4 K04 R | 10-14 10:33; SHORT; **24684.5/24706.25/24684.5/24697.0** (NT#31732) | 22.91274922; 2 | 24697 → 24742.75; 45.75 | 929.98 / 442.52 | 1.996705 / 0.998352 |
| B K05 A | 10-28 10:28; LONG; **26044.5/26047.0/26033.5/26041.25** (NT#45527) | 12; 4 | 26041.25 → 25993.25; 48 | 974.98 / 225.02 | 4.000000 / 1.000000 |
| B K05 R | 10-14 10:33; SHORT; **24684.5/24706.25/24684.5/24697.0** (NT#31732) | 22.75; 4 | 24697 → 24788; 91 | 1834.98 / 440.02 | 4.000000 / 1.000000 |
| C4 K05 A | 10-14 14:12; LONG; **24892.5/24903.5/24891.5/24900.0** (NT#31951) | 11.5891883; 4 | 24900 → 24853.75; 46.25 | 939.98 / 216.27 | 3.990789 / 0.997697 |
| C4 K05 R | 10-14 10:33; SHORT; **24684.5/24706.25/24684.5/24697.0** (NT#31732) | 22.91274922; 4 | 24697 → 24788.5; 91.5 | 1844.98 / 442.52 | 3.993410 / 0.998352 |

#### Presupuesto, cociente y cantidad

H dueño es el hard headroom realmente presente en la instantánea; ausencia permanece explícita. H usado es el headroom efectivo del sizing, que incorpora los límites propios de MM. Los cocientes BEFORE se presentan como división exacta de los presupuestos/costes ya auditados, sin ejecutar nuevamente MM; AFTER usa los cocientes reales retenidos. `floor R/T; ladder → Q` muestra ambos floors y el cap. `SL/R ; TP/T` muestra múltiplos monetarios netos por contrato sobre presupuestos efectivos, antes de fills.

| Versión/perfil/caso | R/T preferidos → efectivos | Remanente; H dueño / H usado | R/SL; T/TP → floors; ladder → Q | SL/R; TP/T | Límite prefill retenido; postfill |
|---|---|---|---|---|---|
| B K01 A | — | — | — | — | ninguna entrada; no aplica postfill |
| B K01 R | 250/250 → 250/250 | 870; no retenido / 1000 | 12500/23499 (≈0.531938); 12500/22001 (≈0.568156) → 0/0; 2 → **0** | 1.879920; 1.760080 | TG_SIZE_BELOW_MINIMUM; Q0; sin fill de entrada ni stop postfill |
| C4 K01 A | 250/250 → 250/250 | 870; 1100 / 1000 | 12500/12249 (≈1.020491); 12500/10751 (≈1.162683) → 1/1; 2 → **1** | 0.979920; 0.860080 | TG_ENTRY_SIZED; fill 24901 → stop enviado 24889; proyección SL 249.98 ≤ R 250.00; TP postfill no retenido |
| C4 K01 R | 250/250 → 250/250 | 870; 1100 / 1000 | 12500/23499 (≈0.531938); 12500/22001 (≈0.568156) → 0/0; 2 → **0** | 1.879920; 1.760080 | TG_SIZE_BELOW_MINIMUM; Q0; sin fill de entrada ni stop postfill |
| B K02 A | 500/500 → 500/500 | 870; no retenido / 1000 | 25000/23499 (≈1.063875); 25000/22001 (≈1.136312) → 1/1; 2 → **1** | 0.939960; 0.880040 | TG_ENTRY_SIZED; fill 24696.75 → stop enviado 24721.25; proyección SL 499.98 ≤ R 500.00; TP postfill no retenido |
| B K02 R | 500/500 → 364.98/364.98 | 364.98; 1505.06 / 1000 | 18249/24749 (≈0.737363); 18249/23251 (≈0.784869) → 0/0; 2 → **0** | 1.356184; 1.274097 | TG_SIZE_BELOW_MINIMUM; Q0; sin fill de entrada ni stop postfill |
| C4 K02 A | 500/500 → 500/500 | 870; 1100 / 1000 | 25000/23499 (≈1.063875); 25000/22001 (≈1.136312) → 1/1; 2 → **1** | 0.939960; 0.880040 | TG_ENTRY_SIZED; fill 24696.75 → stop enviado 24721.25; proyección SL 499.98 ≤ R 500.00; TP postfill no retenido |
| C4 K02 R | 500/500 → 349.86/349.86 | 349.86; 1620.14 / 1000 | 17493/17999 (≈0.971887); 17493/16501 (≈1.060118) → 0/1; 2 → **0** | 1.028926; 0.943292 | TG_SIZE_BELOW_MINIMUM; Q0; sin fill de entrada ni stop postfill |
| B K03 A | 500/(1000/3) (T≈333.333333) → 500/(1000/3) (T≈333.333333) | 870; 1100 / 1000 | 25000/22499 (≈1.111160); 50000/41253 (≈1.212033) → 1/1; 2 → **1** | 0.899960; 0.825060 | TG_ENTRY_SIZED; fill 25227.5 → stop enviado 25252; proyección SL 499.98 ≤ R 500.00; TP postfill no retenido |
| B K03 R | 500/(1000/3) (T≈333.333333) → 500/(1000/3) (T≈333.333333) | 870; no retenido / 1000 | 25000/34749 (≈0.719445); 50000/65753 (≈0.760422) → 0/0; 2 → **0** | 1.389960; 1.315060 | TG_SIZE_BELOW_MINIMUM; Q0; sin fill de entrada ni stop postfill |
| C4 K03 A | 500/(1000/3) (T≈333.333333) → 500/(1000/3) (T≈333.333333) | 870; 1100 / 1000 | 25000/24999 (≈1.000040); 50000/46253 (≈1.081011) → 1/1; 2 → **1** | 0.999960; 0.925060 | TG_ENTRY_SIZED; fill 24796 → stop enviado 24771.5; proyección SL 499.98 ≤ R 500.00; TP postfill no retenido |
| C4 K03 R | 500/(1000/3) (T≈333.333333) → 500/(1000/3) (T≈333.333333) | 870; 1100 / 1000 | 25000/34999 (≈0.714306); 50000/66253 (≈0.754683) → 0/0; 2 → **0** | 1.399960; 1.325060 | TG_SIZE_BELOW_MINIMUM; Q0; sin fill de entrada ni stop postfill |
| B K04 A | 500/250 → 500/250 | 870; 1100 / 1000 | 25000/24749 (≈1.010142); 12500/11251 (≈1.111012) → 1/1; 2 → **1** | 0.989960; 0.900080 | TG_ENTRY_SIZED; fill 26042 → stop enviado 26017.5; proyección SL 499.98 ≤ R 500.00; TP postfill no retenido |
| B K04 R | 500/250 → 500/250 | 870; no retenido / 1000 | 25000/46249 (≈0.540552); 12500/22001 (≈0.568156) → 0/0; 2 → **0** | 1.849960; 1.760080 | TG_SIZE_BELOW_MINIMUM; Q0; sin fill de entrada ni stop postfill |
| C4 K04 A | 500/250 → 500/250 | 870; 1100 / 1000 | 25000/23749 (≈1.052676); 12500/10751 (≈1.162683) → 1/1; 2 → **1** | 0.949960; 0.860080 | TG_ENTRY_SIZED; fill 24901 → stop enviado 24876.5; proyección SL 499.98 ≤ R 500.00; TP postfill no retenido |
| C4 K04 R | 500/250 → 500/250 | 870; 1100 / 1000 | 25000/46499 (≈0.537646); 6250/11063 (≈0.564946) → 0/0; 2 → **0** | 1.859960; 1.770080 | TG_SIZE_BELOW_MINIMUM; Q0; sin fill de entrada ni stop postfill |
| B K05 A | 1000/250 → 1000/250 | 870; 1100 / 1000 | 50000/48749 (≈1.025662); 12500/11251 (≈1.111012) → 1/1; 2 → **1** | 0.974980; 0.900080 | TG_ENTRY_SIZED; fill 26042 → stop enviado 25992.5; proyección SL 999.98 ≤ R 1000.00; TP postfill no retenido |
| B K05 R | 1000/250 → 1000/250 | 870; no retenido / 1000 | 50000/91749 (≈0.544965); 12500/22001 (≈0.568156) → 0/0; 2 → **0** | 1.834980; 1.760080 | TG_SIZE_BELOW_MINIMUM; Q0; sin fill de entrada ni stop postfill |
| C4 K05 A | 1000/250 → 1000/250 | 870; 1100 / 1000 | 50000/46999 (≈1.063852); 25000/21627 (≈1.155962) → 1/1; 2 → **1** | 0.939980; 0.865080 | TG_ENTRY_SIZED; fill 24901 → stop enviado 24851.5; proyección SL 999.98 ≤ R 1000.00; TP postfill no retenido |
| C4 K05 R | 1000/250 → 1000/250 | 870; 1100 / 1000 | 50000/92249 (≈0.542011); 6250/11063 (≈0.564946) → 0/0; 2 → **0** | 1.844980; 1.770080 | TG_SIZE_BELOW_MINIMUM; Q0; sin fill de entrada ni stop postfill |

La ancla técnica y los costes de sizing no autorizan forzar Q=1. El caso C4 K02 R reduce R/T de 500/500 a 349.86/349.86 por remanente: el SL neto por contrato es 359.98, su cociente R/SL=17493/17999 y floor=0. El hard headroom dueño de ese caso es 1620.14 y H usado 1000; el rechazo proviene del presupuesto/remanente, no de sustituir headroom por otro campo.

C4 K03 A: prefill SL neto 499.98 y R=500. Fill real 24796 y stop físico enviado 24771.5, distinto de la ancla prefill 24771.25. Su proyección SL neta es 499.98 ≤ R=500. Se usa la protección posterior real, no se conserva por inferencia la ancla inicial.

La proyección posterior al fill usa el precio real de entrada y el primer stop enviado por esa operación: distancia×20 + fees4,98 + slippage de salida5. La entrada ya incorpora su slippage; no se cobra dos veces. Esta proyección no garantiza el precio efectivo del futuro fill SL. El umbral TP posterior al fill no se conserva en estos eventos; no se inventa a partir del rol de la orden de salida. Los presupuestos y resultados netos sí están acreditados por la autoridad y ledger completos.

### Entrega física, recursos y reproducción

Fuente en rama local `codex/tradesgerard-entry-repair-c4-20261013`, checkout `implementer/echo-c4`, commit `88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49`, árbol `935e74d6056ffb3593f5a9a5deb8771ea6214bcd`. Los1848 archivos congelados conservan hashes, árbol limpio. Binario `implementer/bin/echo-backtest-88ed70d1`, Go1.27.1, vcs.modified=false, SHA256 `c8849bb6e5523e8625ead8282f0d97f98d8b02e14d72838e3c35de207c6bcd57`. Fuente de producto local recuperable; no se afirma push de Echo ni integración en rama estable.

Diff y regresiones permanentes: comparar B `10d406b3cddbd9c738dbc64b5db38c16ff7527b9` con ese C4 en el checkout. Los owners y RED/GREEN están en la adjudicación y `verifier/mandate-12-evidence-matrix.json`; TCR en `specs/FEAT-TRADESGERARD-ENTRY-REPAIR/TEST_CHANGE_REQUEST.md`. El TASKS congelado conserva su corte anterior al largo; el estado final externo evita modificar source después de verificarlo.

Entrega del integrador: `implementer/evidence/c4-implementation-handoff.json`; dictamen independiente: `verifier/independent-final-dictamen.json`. Recetas realmente ejecutadas: `implementer/evidence/c4-executed-recipes.json`, con argv/cwd/env de build, vet, tests y diez campañas, source/bin/corpus/planes y exit codes. `implementer/evidence/commands.ndjson` conserva cada invocación de campaña. Controlador ejecutado:

```text
taskset -c 0-5 python3 /home/kor/aranea/work/tradesgerard-entry-repair-20261013/implementer/run_final_c4.py /home/kor/aranea/work/tradesgerard-entry-repair-20261013/implementer/bin/echo-backtest-88ed70d1 88ed70d1 88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49 c8849bb6e5523e8625ead8282f0d97f98d8b02e14d72838e3c35de207c6bcd57
```

Entorno GOMAXPROCS=4, cwd del chat local explicitado en el recibo. El controlador terminó exit0, al igual que watchdog y diez campañas; no relanzar sobre directorios de resultados ya ocupados. Para reproducción, usar los argv de cada receipt con nueva salida propia y los mismos inputs congelados, sin recompilar sobre fuente mutable.

Drenaje físico:20 PIDs wrapper/child de las diez campañas ausentes; cero procesos propios Go/campaña/controlador/watchdog y cero scratch pendiente. Directorios temporales Go autolimpiados; no se borraron corpus, builds, source, resultados, caches ni trabajo ajeno. Medición final de `c4-drain-resource-manifest.json`:770.330.483 bytes durables globales de805.306.368 permitidos; lote62.426.424 de268.435.456; stdio253.065 de16.777.216; disco libre13.405.282.304 por encima de reserva8.589.934.592. Traza máxima observada5.913.207 bytes, límite16MiB. Las mediciones tienen timestamp, no pretenden congelar el tamaño de futuras notas de evidencia.

Máximo observado tres campañas; reserva conservadora redujo a dos las últimas admisiones sin cancelar campañas ni ampliar límites. Afinidad0–5/GOMAXPROCS4 verificados por proceso. GNU time-v conserva CPU/RSS por campaña en el manifiesto; pico RSS simultáneo agregado NO_MEDIDO, no se suma el máximo de cada proceso para inventarlo. No hubo budget stop ni first cause de recursos. Benchmarks de velocidad no reclamados.

### Hipótesis D falsificada durante la revisión final

La sospecha de un suavizado adicional de D en C4 quedó **refutada**, sin modificar fuente, campañas ni admisiones. Los nombres internos indujeron una lectura incorrecta del manager y del integrador: `slowK(state)` devuelve rawK; `State.SlowK` conserva rawK; `State.SlowD` conserva K=SMA3(rawK). El promedio de sus tres valores en `details.slow_d` es precisamente D=SMA3(K), disponible desde la barra24 y ajeno al filtro de entrada.

El verificador calculó D con Fraction desde los OHLC originales: los755 payloads físicos de K02 C4 coinciden exactamente. Primer cruce14oct14:33Z: D esperado/actual `2202652219150/26491928463` (83,14427627). B observado equivalente reportaba `6663741800/61752747` (107,91004650), suma de cuatro rawK dividida por3; sus755 valores difieren. Esa desviación informativa ya está corregida en C4 y no explica la recuperación de entradas. Evidencia: `verifier/informational-D-independent-falsification.json`. No se aplicó la propuesta equivocada de publicar el último State.SlowD, que habría emitido K como D. No hay asserts D en los tests TG permanentes actuales; se conserva el comparador físico independiente como regresión diagnóstica externa, con este límite explícito.

### Identidades comprobadas por el manager

| Elemento | Evidencia física |
|---|---|
| Fuente B | `xKoRx/echo`, rama `codex/tradesgerard-b-glm`, HEAD `10d406b3cddbd9c738dbc64b5db38c16ff7527b9`; `git status --short` vacío al arranque. |
| Checkout B | `ARANEA_ROOT/work/tradesgerard-b-glm-20261012/echo`. |
| Binario B | `ARANEA_ROOT/work/tradesgerard-b-glm-20261012/bin/echo-backtest`, SHA256 `f00efd668eee8b121f7efb65b1b92923620e47beaac650a99491b425027486e8`. |
| Metadata ejecutable | `go version -m`: Go1.27.1, linux/amd64, vcs.revision igual al HEAD B, vcs.modified=false. |
| Evidencia histórica | `work/tradesgerard-b-glm-20261012/{inputs,prepared,runs}`, relativa a ARANEA_ROOT; T0/T1/T1-L/RESULTADO leídos. COMPLETE histórico no prueba corrección de señal. |
| Agents-OS | `xKoRx/agents-os`, checkout local master limpio al arranque. Escritura canónica mediante materializador; último corte remoto comprobado `1784eb39e68244805dcde286655f2910b6f18784`. La sincronización del delta documental final se verifica separadamente por Git, sin atribuir push al archivo local. |

La abreviatura `f00efd66…c4fed` de RESULTADO no es identidad válida del binario T1: el SHA completo físico anterior gobierna. No se ha recompilado ni modificado B.

### Ejecución y aislamiento

Manager: coordinación, inspección, adjudicación y documentación; sin código ni integración. Implementador inicial `/root/entry_repair_implementer`, suspendido en el relevo operativo posterior a vet C4; integrador único vigente `/root/entry_repair_integrator_c4`, con contexto nuevo y continuidad física preservada. Independiente `/root/entry_repair_verifier`. Modelo solicitado para los especialistas `gpt-6.1-sol`; servido UNKNOWN mientras no exista metadata fiable. Primer dispatch inicial falló por capacidad; su reintento con el mismo modelo arrancó correctamente. Sin sustitución de modelo ni integradores concurrentes, sin consumo CLOUD Pro.

Evidencia nueva externa al vault: `ARANEA_ROOT/work/tradesgerard-entry-repair-20261013/{implementer,verifier}`. El implementador posee el carril Go/build/campañas; el verificador puede solapar el oráculo ligero sobre OHLC físico, sin usar `tg` como oráculo. Cada ejecución debe fijar source, build e inputs y drenar sus procesos.

Resolución física LOCAL de esta ejecución: `ARANEA_ROOT=/home/kor/aranea`, `VAULT_ROOT=/home/kor/secondbrain/main`. La raíz de evidencia nueva es `/home/kor/aranea/work/tradesgerard-entry-repair-20261013`; los paths `implementer/...` y `verifier/...` del informe se resuelven desde ella. Recetas realmente ejecutadas, salidas y exit codes: `implementer/evidence/c4-executed-recipes.json` y los recibos individuales de campaña, junto a manifests y recibos de cada corrida. No sustituir esos comandos por una build de HEAD mutable.

Lectura inicial de recursos: disco aproximadamente16GiB disponibles y RAM64GiB available; es observación puntual, no permiso de consumo. Reserva disco≥8GiB, scratch≤2GiB, durable≤256MiB/lote, logs/trazas≤16MiB; el recibo final más abajo acredita presupuesto agregado; pico RSS simultáneo histórico no medido. No borrar corpus, caches, builds o evidencia ajena.

### Matriz de gates vigente

| Gate | Estado y alcance |
|---|---|
| Identidad y conservación B | PASS: source/binario/corpus físicos comprobados y preservados. |
| Censo OHLC→indicadores→cruces | PASS independiente C2:42969 barras/755 oportunidades, tolerancia prospectiva y correspondencia por identidad. |
| Primera pérdida y regresiones | PASS: decline/rearme LONG y SHORT, SL/TP/finality, ocupado sin backlog, warmup y compra/pausa acreditados; fixtures permanentes. |
| Falsificación exacta y cobertura | C4 exacto INDEPENDENT_PASS: regresiones propias, CLI, paridad offline; cobertura346/350 bloques afectados y267/271 inicios AST, cero sin perfil/mapear. Backtester C4 nuevo; SDK reutilizado por identidad de bytes. Comparación larga10/10 independiente PASS. |
| Observabilidad compacta | PASS de retención, extractor y particiones/métricas en10/10 campañas.162/253 histórico no respaldado;338 materializaciones/274 rechazos en diez configuraciones acreditados. |
| Sizing por perfil | PASS: C4 acredita completitud y autoridad de cada snapshot MM. Primera admisión/rechazo de cada perfil, OHLC y unidades en `implementer/evidence/c4-sizing-presentation.md`; readback independiente semántico PASS de20 filas,19 decisiones reales. |
| Comparación T1 final | C4:10/10 COMPLETE y verificadas independientemente (K01–K05 ×2300/3000). C3 supersedido:5 COMPLETE referencia,1FAILED por cancelación,4 no ejecutadas. B observado5/5 COMPLETE y equivalencia íntegra independiente PASS; ambos retiros históricos enlazados por equivalencia comprobada. |
| Casos largos pertinentes | Lifecycle C4 PASS27,411s, AllFourTargets C4 PASS62,528s y CLI singleton C4 PASS122,157s; V-F02 causal cerrado en pagos sin alterar oráculo. Los cuatro targets heredados son regresión, no reactivación del catálogo. |
| Recursos y cierre de procesos | PASS físico:10 campañas, controlador y watchdog exit0;20 PIDs wrapper/child ausentes, jobs propios0, scratch0. Recibo `implementer/evidence/c4-drain-resource-manifest.json`; sin cierre de sesión del manager. |

### Adjudicación

Hechos confirmados: identidad física B, censo independiente completo, before observado equivalente en los cinco perfiles, primera pérdida tras rechazo y regresiones físicas permanentes. Hipótesis refutadas: no faltaban los cruces brutos de K, el primer rechazo por sizing no explicaba el día completo y restaurar una cuenta no reseteaba su piso en V-F03. C4 corrige las causas siguientes y pasa el gate exacto y la comparación larga de diez configuraciones. Una nueva política para cuentas limitadas por el mínimo del sizing vigente y piso EOD permanece como propuesta no aplicada. KISS-1 conserva R/T y geometría; design-2 es histórico.

| Causa confirmada | Primera divergencia / reproducción | Propietario corregido y comprobación |
|---|---|---|
| Ciclo técnico diario | B marca sólo31 NewCycle entre755 cruces; SHORT14oct14:48Z cae en SAME_CYCLE después de un rechazo. | `strategies/tg/tg.go`: cada salida de zona es oportunidad distinta. `TestEntryRepairEveryZoneExitStartsDistinctOpportunity`, tapes LONG/SHORT y comparación por identidad. |
| Finalidad incompleta | El mismo owner queda CREATED, flat y sin claims tras decline; un ciclo ya cerrado por fills tampoco debe permanecer activo. | `strategies/tgmm/tgmm.go` emite terminación física; `operation/engine.go` descarta cruces ocupados sin backlog. Pruebas decline, flat, parciales/cancel y fill tardío preservan los bloqueos reales. |
| ATR y readiness |13oct18:11Z ATR debería estar sembrado8,7875 y B está vacío; luego realimenta valores cuantizados al tick.23 callbacks útiles fallan WARMUP_INCOMPLETE en B. | `strategies/tg/tg.go`: TR inicial, semilla20, Wilder sin feedback al tick y readiness23 sin D. Oráculo independiente y tape warmup23; tolerancia fijada antes de cotejar. |
| Veto global por cuenta pausada | Fixture de dos ganancias435 alcanza pausa870; siguiente demanda no compra en B pese a caja/plaza/flat. | `platform_campaign.go`: compra a demanda con guards efectivos. Mismo test independiente B RED2MM/1cuenta frente C4 GREEN3MM/2cuentas. |
| Compra inicial fuera de demanda | Preparación/escenario quieto compraba cuenta sin OPEN admisible y podía consumir caja antes del horario. | `platform_campaign.go`: primera compra en oportunidad admisible; escenarios quieto/outside conservan caja y no compran anticipadamente. |
| V-F01: refresh posterior a selección | Pausa ya vencida en10NY queda deshabilitada al evaluar el primer cruce; versión intermedia compra otra cuenta indebidamente. | Campaign actualiza elegibilidad antes de seleccionar/entregar. Tape público de frontera acredita misma cuenta y economía preservada, sin reset. |
| V-F02: turno revivido | Al reabrir sesión se retoma una cuenta posterior tras terminar su turno, saltando el orden de creación. | Campaign distingue turno activo de una nueva selección. Regresión pública RED C2/GREEN C4, pausa interna/fallo oficial y pagos largos íntegros. |
| V-F03: economía diaria parcial | Provider/Views tienen5,12, cache diario Fresh omite margen y MM admiteR500/Q1; dos entradas K02 de referencia exceden margen real. | `driver.go` proyecta revisión actual antes de entregar; `projection.go` comparte snapshot completo. RED B/C3, GREEN C4 exacto con margen5,12/Q0/sin órdenes y paridad Core offline. |

Estos efectos no son sumables por separado: latch y finalización pueden afectar el mismo cruce; corregir selección cambia la trayectoria económica posterior. Los fixtures no se usan para fabricar fills en T1. Source C4 y regresiones permanentes están en `implementer/echo-c4` bajo el SHA congelado; los apartados de evidencia precisan cada before, test y límite.

Índice independiente de los doce casos obligatorios: `verifier/mandate-12-evidence-matrix.json`, ligado a source/binario C4. Mapea rechazo LONG/SHORT, SL, TP bajo objetivo, ocupado sin backlog, parciales/cancel/tardíos, pausa/sesión, oráculo K01–K05, sizing330/headroom, compra pausada, métricas compactas y paridad offline a assets permanentes, hashes y recibos. Distingue ejecución exacta de reutilización SDK por bytes idénticos y acredita la comprobación T1 completa10/10. Negativos aislados que inyectan OwnerState/reservas se declaran como tales; el recorrido público positivo usa Run y fills físicos. Core conserva explícitamente su contexto/views simulados y admisión manual; ningún gate certifica broker ni publicador LIVE.

Los apartados siguientes conservan la bitácora de hitos y sus pendientes **al momento de cada corte**. El estado actual lo gobiernan el resumen y la matriz anteriores; un PASS posterior no borra fallos ni intentos supersedidos.

### Censo independiente inicial — readback verificado

`verifier/oracle-summary.json`, `oracle-bars.csv`, `oracle-crosses.csv` y `oracle.py`, relativos a la raíz de evidencia nueva. Archivo físico SHA256 `700579b3b3c78e58ccceb39bd79e8d11aa3efab3e8457d92bee1833ef2686406`; Python stdlib lee filas originales y calcula indicadores sin llamar `tg` ni Echo. Resultado:42969 barras físicas,2959 cruces brutos,755 cruces dentro de la ventana operable del plan en31 fechas NY. Hay350 barras de entrada por fecha:10850 en total. El plan fija `trade_start=2025-10-14T13:30Z` (09:30NY), con entradas desde10:00NY; el prefijo efectivo contiene1118 barras y68 cruces. Quedan2891 cruces brutos posteriores a trade_start. La frontera de fuente es2025-10-13T17:51Z, primera barra cerrada17:52Z; último cierre físico2025-11-25T22:00Z, horizonte del plan23:00Z. Las horas restantes son cierre del calendario, no barras fabricadas.

Tolerancia inicial fijada por el independiente:1e−9 absoluta para K/ATR; no cambia decisiones estrictas20/80. El oráculo se fortaleció con aritmética racional exacta para K y los umbrales: conserva755 oportunidades; ATR usa float64 y tolerancia1e−9. Warmup matemático: rawK desde barra20, K desde22, primer par comparable23; primer TR=H−L si no existe cierre previo entregado, ATR semilla20; D informativa desde24 sin gate. Tabla por sesión conserva preparación y exclusiones.

| Oportunidad inicial | K previa → actual | ATR puntos |
|---|---:|---:|
| SHORT2025-10-14T14:33Z /10:33NY |82,5927452264→75,5520430532|22,9127492199|
| SHORT2025-10-14T14:48Z /10:48NY |82,6870807816→69,1052785069|20,3033672470|
| LONG2025-10-14T14:55Z /10:55NY |11,6913385991→22,8282828283|20,0757086495|

El independiente localizó sólo la primera evaluación MM de K01 en el histórico de esa jornada;14:48Z es la primera oportunidad posterior cuya omisión se investiga. Esto no declara todavía que el primer rechazo debiera haberse admitido ni que la primera divergencia de indicador ocurra en14:48Z.

Inspección de fuente corroborada por manager: `tg/tg.go:242–249` mantiene explícitamente un ciclo técnico por día y deriva `NewCycle` de `CycleOpen`; `tg.go:295/306` realimenta ATR cuantizado al tick; `platform_campaign.go:492` mantiene el veto global de compra por cualquier cuenta pausada. Las tres ramas contradicen aspectos del contrato actual. El implementador debe demostrar cada impacto con input mínimo, primera divergencia y regresión baseline/fix; el independiente conserva su propio oráculo.

TCR adjudicado por manager dentro del mandato del Owner: `specs/FEAT-TRADESGERARD-ENTRY-REPAIR/TEST_CHANGE_REQUEST.md` en el checkout de reparación. Se autoriza sustituir sólo la expectativa de ATR cuantizado por Wilder independiente (semilla20 y tolerancia1e−12), manteniendo asserts de K/replay; y la expectativa de veto por cuenta pausada por admisión con caja/cupo/sesión reales más negativos. El fixture heredado tiene una cuenta, no una quinta; descripción corregida solicitada. No se autoriza saltar tests ni debilitar límites.

### Rectificación I1 — ENTRY-REPAIR-C01

Readback independiente de los diez resultados físicos conservados: `verifier/baseline-reconciliation.json`. Todas las configuraciones emitieron755 señales OPEN, coincidentes en total con las755 oportunidades NY del oráculo. No se acredita todavía identidad uno a uno sólo con ese total; el contraste individual sigue en curso. Los números históricos llamados «cruces» eran intentos materializados, no el censo de cruces de mercado.

| Perfil, por retiro | OPEN emitidas | Operaciones creadas | Con fills | Registros FILL | Rechazos sizing |
|---|---:|---:|---:|---:|---:|
| K01 |755|31|0|0|31|
| K02 |755|36|18|36|18|
| K03 |755|36|7|14|29|
| K04 |755|31|1|2|30|
| K05 |755|35|6|12|29|

La suma es169 operaciones creadas y137 rechazos para cinco perfiles con un retiro;338 y274 al incluir ambos retiros. La cifra162/253 no concilia con esta población. No se publica un porcentaje sustitutivo mezclando cruces, intentos y callbacks. La baja actividad no queda explicada por los31 rechazos K01:724 señales emitidas no llegaron a una nueva materialización; su clasificación causal exacta está en reproducción. Los36 FILL de K02 pertenecen a18 operaciones con fill, no36 operaciones.

T1 conserva estado de ejecución COMPLETE10/10 y contabilidad conciliada. Validez analítica: AFFECTED para frecuencia, denominadores y explicación de oportunidades; reemplazo en este informe todavía IN_PROGRESS. T1-L conserva su selección histórica K01/K02 y COMPLETE4/4; no se reejecuta ni se transfiere automáticamente el nuevo resultado.

Observación adicional para adjudicar: el recibo corto baseline K01 registra compra inicial2025-10-14T13:30Z (09:30NY), anterior a la ventana10:00NY. Se pidió investigar la ruta de bootstrap y probar compra real a demanda/horario, sin dar por suficiente el test aislado de `canPurchase`.

### Reproducción y corrección en curso

El baseline corto K01 ejecutado con el binario B original terminó COMPLETE, intento1, recibo `implementer/evidence/baseline-short-K01/49fee730f22ec7d8545b21be2d3ddb9a9b88b079082fd66dcafcce8967e5c631/receipt.json`; resultado SHA256 `b07197241ce9e65dbe91f1c7e41e1de251936c3c5534a6391b738d15da843249`. Cero fills, una operación materializada y23 callbacks de gestión en esa jornada; caja4880. El baseline permanece sin cambios.

Regresiones nuevas RED sobre fuente defectuosa (`implementer/evidence/red-tg.log`): `TestEntryRepairEveryZoneExitStartsDistinctOpportunity` falla porque la nueva salida de zona no abre nueva oportunidad; `TestEntryRepairWilderSeedAndReadiness` observa19 TR en la barra20. Esto prueba defectos de señal/preparación, aún pendiente del gate físico completo y contraste de ATR por barra.

TCR adicional aprobado tras inspección: en `TestTG_CrossEmissionAndSingleConsumption`, el segundo LONG independiente debe marcar nueva oportunidad; se conservan dirección, cantidad de señales, stop y no duplicación. La supresión por operación ocupada pertenece a la capa que conoce exposición/finality y debe probar ausencia de backlog. El fixture heredado retrocede timestamps tras el segundo cruce; se autorizó corregir sólo su secuencia temporal con evidencia.

La ruta `purchaseInitial()` fue confirmada como bypass que factura a trade_start antes de10NY; la corrección de compra inicial a demanda está en curso. Tests quiet sin oportunidad deben conservar caja5000; los que realmente compran mantienen su débito. Cualquier ajuste heredado adicional requiere TCR concreto y negativos, no sustitución global de expectativas.

El independiente ejecutó por CLI original dos reproducciones sintéticas espejo, LONG y SHORT, con rechazo inicial10:01NY y un nuevo cruce de la misma dirección10:45NY tras descenso de ATR, sin visitar la banda contraria. Resultados baseline en `verifier/synthetic/{long-baseline,short-baseline}`: COMPLETE/conciliados, una operación materializada, cero fills; el segundo cruce llega como gestión. Estas series prueban funcionamiento y no sustituyen el censo real ni una campaña económica. Gate corregido pendiente.

TCR `TestTG_CycleBookkeeping` aprobado: el cruce instantáneo consumido no conserva un ciclo técnico hastaEOD. Se mantiene respuesta conservadora ante estado ilegible y se exige probar que rollover/activación no relajan las barreras de exposición/finality de Operation.

### Primera divergencia acreditada contra módulo público B

El independiente condujo42969 barras originales por `tg.Evaluate` público y las comparó por identidad con su oráculo externo. `verifier/comparison-baseline.json` demuestra cero diferencias de dirección en755 oportunidades; sólo31 se marcan `NewCycle=true`. Primera diferencia absoluta de ATR:2025-10-13T18:11Z, línea física30570; oráculo ya sembrado8,7875 y B aún vacío. Primera diferencia de valor:18:12Z, esperado8,573125 y B8,75. Error absoluto máximo ATR en la muestra:1,35505950137 puntos. Se separan semilla desplazada y cuantización recurrente; no se atribuye toda la desviación a una sola causa.

Primera diferencia de identidad de ciclo: SHORT2025-10-14T14:48Z, línea31747, K69,1052785069 correcto; B entrega `NewCycle=false`, `TG_SIG_B_CROSS_SAME_CYCLE`, ATR20,75 frente20,3033672470 independiente. La hipótesis de que faltaban los cruces brutos o cambiaban entre perfiles queda refutada en el contraste del módulo/mercado; el fallo de recuperación está downstream del cruce. La evolución bajo exposición completa aún se prueba con la cadena integrada.

El probe independiente fuera de horario usa29 barras09:31–09:59NY y trade_start09:58NY, sin OPEN ni operaciones: B igualmente compra por120. Recibo `verifier/synthetic/outside-baseline-v3/c5162363206b6810cceccd934bdb462d2d4c2af99b79b19fb048e1b4bd6df357/receipt.json`. Se confirma defecto de compra inicial fuera de demanda/horario, distinto del veto por cuenta pausada.

TCR ON_DEMAND aprobado para tres fixtures heredados: quiet(Session999 sin OPEN en2sesiones), cancelado antes del primer input y cierre de recorder inyectado sobre quiet. Expected caja5000/cuentas0, preservando primera causa, FAILED/reconciliación y asserts financieros de los fixtures con oportunidades reales. El nuevo seam de compra debe preservar el guard público de frontier y finality; el fallo de esa integración detectado durante desarrollo no es PASS.

### Sizing: rechazo inicial legítimo no equivale a día inviable

`verifier/first-day-sizing-oracle.json` calcula geometría por cruce con headroom fresco explícito; no simula PnL posterior. Para K01, antes del primer fill esa hipótesis corresponde al caso observado sin operaciones previas. NQ: punto20USD, tick0,25=5USD; comisión ida/vuelta4,98USD y slippage modelado ida/vuelta10USD, total14,98USD por contrato. R/T250/250 yρ1 permanecen congelados.

| K01,2025-10-14 | ATR puntos | SL técnico | Distancia puntos | Pérdida estimada1contrato | Q |
|---|---:|---:|---:|---:|---:|
|10:33NY SHORT|22,91274922|24719,75|22,75|469,98USD|0|
|10:48NY SHORT|20,30336725|24719,50|20,25|419,98USD|0|
|14:12NY LONG|11,58918830|24888,50|11,50|244,98USD|1|

El primer rechazo es compatible con R250, pero la señal14:12NY del mismo día tiene cantidad geométrica1 sin cambiar R/T. Admisión/fill físico corregido aún pendiente. Para K02–K05 los cálculos con headroom fresco no sustituyen la trayectoria de pérdidas/pausas de una campaña; deben contrastarse con el estado efectivo.

Ampliar un multiplicador de ATR aumenta distancia y costo por contrato y reduce la cantidad admisible a presupuesto fijo; no resuelve este bloqueo de ciclo. El ejemplo sólo demuestra por qué hay que volver a evaluar nuevas señales cuando ATR cambia, sin recomendar nuevos parámetros.

El independiente observó además K02: fill de SL14:35:26Z deja exposición flat, pero la operación sólo llega a TERMINAL en15:55NY; el nuevo SHORT14:48Z queda afectado. Regresión y finality del candidato siguen pendientes.

### Avance del candidato, todavía sin certificación

Los tests críticos del implementador pasaron en `implementer/evidence/critical-final.log` tras reparar el seam de compra: tg, tgmm, Operation y backtester afectados. Esto no sustituye la falsificación independiente ni una build congelada. La corrida race/cobertura afectada está en curso con fuente quieta; cutoff de compra y observabilidad extendida siguen en revisión antes del freeze.

El independiente aisló el redondeo recurrente de ATR manteniendo la semilla tardía del baseline (`verifier/baseline-rounding-isolation.json`): a18:12Z,8,6375 sin cuantización frente8,75 real; error0,1125. El máximo1,3550595 persiste. Por tanto el defecto de feedback cuantizado no depende de adjudicar la convención del primer TR.

Gates explícitos aún pendientes: build/commit final, pruebas independientes sobre ese delta, short físico corregido y recuperación K01/K02, partición completa de oportunidades, diez campañas, métricas de operación/cuenta/día y cobertura nueva compatible. No se certifica readiness ni resultado económico.

La ampliación race/cobertura encontró una incompatibilidad de la propuesta inicial con el contrato de separación `SignalDetails` (exactamente technical_stop + strategy_details). No se debilita ese assert: el implementador retirará el campo nuevo y expresará la política de descarte por ocupado en el carrier técnico existente con interpretación tipada, ausencia compatible y valor desconocido fail-closed. Los perfiles de esa corrida con fallo no se admitirán como cobertura PASS. Se conserva primera causa en `implementer/evidence/affected-test.log` y se revalida tras el delta.

Actualización: esa corrida fue terminada deliberadamente con SIGTERM, exit143 y drenaje físico confirmado por el implementador; no fue PASS. El carrier booleano adicional fue retirado; el enum técnico vive en StrategyDetails existente y mantiene intacto el assert de separación. `implementer/evidence/carrier-critical.log` pasa tg/tgmm/Operation/domain/backtester afectados. El corte de compra se expresa como máximo(10:00,apertura del perfil) y mínimo(15:50,cierre del perfil), con pruebas de cierre temprano; no se usa resta arbitraria de5minutos.

Precisión de autoridad sobre compra: el Owner exige horario admisible, compra a demanda y no comprar todas las plazas anticipadamente; no fija literalmente si la compra dentro de sesión ocurre a10:00 o al primer cruce. Comprar en la primera OPEN admisible es la resolución técnica elegida y aceptada por el manager para este fix, no una nueva cita atribuida al Owner. El RED contractual inequívoco sigue siendo la compra09:58NY fuera de horario; el tape silencioso verifica el comportamiento elegido sin cobro innecesario.

### Freeze candidato corto C1

Fuente `ba047469513f9120378734b1378352477755c669`, rama `codex/tradesgerard-entry-repair-20261013`, checkout `implementer/echo` limpio al readback manager. Binario `implementer/bin/echo-backtest-ba047469`, SHA256 `72490e8e0399a238865720d396c8deb6e7ced3ddcb0c63a42ca764ac1b2b198f`, metadata VCS idéntica y modified=false (`implementer/evidence/build-ba047469.txt`). B original sigue limpio e intacto. Este freeze tiene gate crítico del implementador PASS; falsificación independiente y cobertura completa pendientes. Campañas finales nuevas:0/10. El independiente recibió el carril Go para verificar este source/build exacto.

### Recuperación corta C1 y falsificación independiente

Contraste independiente C1 (`verifier/comparison-candidate-ba047469.json`):42969 identidades de barra,755 cruces y755 oportunidades nuevas, cero diferencias K/dirección, sin primera divergencia residual y error máximo ATR2,84217094304e−14<1e−9. Baseline tenía31 nuevas oportunidades y ATR incorrecto. E2E CLI independiente LONG/SHORT: rechazo10:01NY sin órdenes/fills→nuevo ciclo10:45NY con fill del mismo lado sin banda contraria, PASS. Fuera de horario y tape silencioso: cero compras/operaciones/fills. Probes públicos y overlays Operation/TGMM propios PASS con los mismos inputs que fallan en B bajo el carrier final. Los probes booleanos previos son REFERENCE_ONLY, no evidencia de la versión final.

Primera jornada física corregida K01:23 OPEN,23 materializaciones,3 operaciones con fills y6 registros FILL, frente a1 materialización y0 operaciones con fills en B. Recibo `implementer/evidence/after-short-K01/bd4877b7e76cb776161c89307fc96b135b63d8407fd744223c8a82d511815899/receipt.json`, COMPLETE/reconciliado. La primera entrada recuperada18:12Z usa Q1, R/T250, distancia11,5 y costo244,98USD; parámetros intactos. Compra a10:33NY en primera OPEN, caja4880. El PnL corto no es criterio de aprobación.

K02 corto autor:23 OPEN,21 materializaciones,16 operaciones con fills y3 cuentas/caja4640. Esta mayor actividad incluye compra de sucesoras tras pausas y aún exige readback independiente de razones de turno, SL/TP y finality; no se presenta como gate aprobado. K03–K05 cortos fueron ejecutados; reconciliación detallada en preparación. La comparación T1 completa de10configuraciones sigue0/10 mientras cierra el gate corto.

Readback agregado independiente de los cinco cortos (`verifier/operations-short-ba047469.json`), todos COMPLETE/reconciliados:

| Perfil | Intentos materializados | Operaciones con fills | Registros FILL | Rechazos sizing | Cuentas | Caja |
|---|---:|---:|---:|---:|---:|---:|
| K01 |23|3|6|20|1|4880|
| K02 |21|16|32|5|3|4640|
| K03 |23|4|8|19|2|4760|
| K04 |23|3|6|20|1|4880|
| K05 |23|3|6|20|1|4880|

El agregado usa todas las operaciones/fills del tape; `execution.summary.economics` corresponde al compartimento final y no debe usarse como total de campaña tras cambiar de cuenta. El extractor conserva duración/rachas y operación/cuenta/día, con fees exactos y slippage ya incorporado en precios físicos, sin restarlo dos veces. La comparación diagnóstica T1×r2300 puede avanzar sobre este freeze; sólo contará como comparación final si supera los gates pendientes sin cambio de fuente.

Readback posterior independiente (`verifier/short-lifecycle-ba047469.json` y `campaign-crosses-short-ba047469.json`): cinco cortos PASS por identidad de las23 oportunidades, error máximo ATR7,11e−15, todos flat, sin solapamiento de exposición ni materialización diferida. K02 descarta explícitamente los cruces17:28Z y17:32Z con exposición1/claim ejecutable1; se conservan como consumidos, no backlog. La matriz restante de finality/adaptadores y promoción de pruebas se mantiene explícita en el handoff independiente.

La comparación diagnóstica C1 de cinco retiros2300 está en ejecución con binario inmutable. Medición del implementador: proceso Go119MB/106%CPU y campaña corta19–30MB/136%CPU, conjunto<3cores/~150MB y disco15,5GiB; se permite ese solapamiento, no benchmark. Fuente C1 permanece quieta durante Go. Tras integrar pruebas permanentes independientes habrá freeze C2 y nueva identidad/build; las diez campañas definitivas se prepararán y ejecutarán contra C2, sin atribuir recibos C1 al nuevo SHA.

Presupuesto agregado fijado prospectivamente por el manager: durable de la iniciativa≤768MiB, incluyendo checkout, builds, probes, inputs y evidencia en ambos carriles; scratch global≤2GiB separado. No reemplaza256MiB por lote,16MiB por traza/log ni reserva≥8GiB. Medición al fijarlo:270MiB total (checkout220MiB, evidencia implementador3MiB, binario16MiB, inputs2,4MiB, independiente30MiB), libres16.092.397.568bytes. Las carpetas nuevas no reinician el contador global. Caches/corpus/históricos ajenos permanecen intactos.

La suite amplia C1 alcanzó el timeout global Go de10minutos en backtester, con378 tests en su selección y sin fallo de assert informado antes del timeout. Estaba ejecutando `TestBTGS04CampaignCollectedTotals` (~1minuto), subcaso `four_collected_then_replacement` (~1segundo), stack en ordenación de fuente sintética9700filas. Evidencia/stack: `implementer/evidence/candidate-ba047469-tests.log`. Estado NOT_PASS, nunca equivalente a378 tests aprobados. Cinco paquetes SDK completaron race PASS, pero la cobertura nueva final se recalculará exclusivamente con perfiles PASS compatibles C2. Se ejecutarán grupos causales acotados; collectedTotals/replacement sigue siendo relevante y no se exime por preexistencia. No se repite una escalera de timeouts sobre el mismo comando.

Sincronización observada de Agents-OS: commit automático `a58ec551187749deaa6d3f0566e1c556d9b456b8`, master remoto igual según `git ls-remote` antes de este delta. No fue un push ejecutado por el manager; los deltas posteriores requieren nueva comprobación.

### Hallazgo independiente V-F01: frontera de reanudación

La falsificación CLI independiente confirma un defecto adicional en C1: `admitOpportunity/selectTurn` decide comprar antes de actualizar una pausa temporal vencida en ese mismo instante. En el tape de1420 barras de dos días, la cuenta válida y flat tenía PAUSED_SESSION hasta2025-10-15T14:00Z (10:00NY). La nueva OPEN exactamente a esa hora compra una segunda cuenta: caja4760 frente a4880 esperada; después el tick administrativo vuelve ELIGIBLE la anterior, cuyo stage190,08 se conserva. Primera divergencia: selección/compra antes de reconciliar elegibilidad temporal. Evidencia `verifier/finding-V-F01.json` y `verifier/synthetic/resume-boundary-candidate-ba047469/`, sobre source/binario C1 ya identificados.

El manager adjudica V-F01 como defecto funcional bloqueante de C1 y autoriza el fix mínimo en Campaign: refrescar elegibilidad vencida antes de seleccionar/comprar, manteniendo ledger, piso y guardas de exposición/claims. Corrección y repetición independiente aún pendientes. El oráculo T1 contiene tres cruces exactamente10:00NY (17oct SHORT,31oct LONG,12nov LONG), por lo que no se considera un borde ajeno al corpus. C1 queda REFERENCE_ONLY para resultados largos; K01 en curso se conservará hasta COMPLETE si sigue sano y las cuatro campañas C1 restantes no se admitirán por supersesión. Si alguna alcanza ejecución/cancelación, se preservará su estado físico real. Las cinco2300 de C2 podrán ser las primeras cinco de las diez definitivas, sin duplicarlas ni reutilizar recibos C1 como si pertenecieran a C2.

### Negativos y paridad independiente C1

El verificador ejecutó `backtest-candidate-ba047469-tests.log`: PASS de caja119,999, cupo5, fronteras horarias, cierre temprano y compra bloqueada por admisión pendiente, owner activo no drenado, QExec ejecutable aun con status terminal o reserva Provider. La expectativa positiva de cuenta pausada válida/flat falla contra B por el veto global y pasa C1 (`backtest-baseline-tests.log` conserva el RED). Se aprueba su promoción como regresiones permanentes; los casos que inyectan estados de owner son fixtures de falla explícitos, no una afirmación sobre observación de broker.

`parity-candidate-ba047469-tests.log`: PASS de `TestIndependent_EntryPolicySharedOwnerLiveAndBacktestParity`, mismos hechos al owner Operation compartido en modos LIVE/BACKTEST. Junto con CLI offline acredita la paridad de software afectada, sin certificar broker real ni composición externa no ejecutada. V-F01 sigue bloqueando el gate final de C1.

La corrida amplia C1 quedó físicamente drenada con exit1: también CLI alcanzó su timeout global600s dentro de `TestLASTPublicExperimentCampaignSealsAndReplaysSingletonCatalog`, que llevaba7m11s, durante verificación de integridad/daily-report. Se preserva el log y no se computa como PASS. Carril Go liberado y consumido por los negativos anteriores; C2 dividirá los grupos largos sin retirar asserts. Medición manager posterior:274MiB de iniciativa y15.987.478.528bytes libres, dentro de los presupuestos vigentes.

### Warmup físico y economía observada

El nuevo tape independiente `verifier/synthetic/warmup23-candidate-ba047469/` prueba por CLI público23 callbacks de warmup, OPEN y fill exactamente10:00NY, COMPLETE/reconciliado. El mismo input contra B (`warmup23-baseline-v3`) falla WARMUP_INCOMPLETE. Se descarta un gate oculto de26 en el wrapper corregido: Requirements.Lookback26 conserva capacidad/preparación conservadora y ReadyFromState23 gobierna elegibilidad. El prefijo histórico T1 no se modifica. Caso autorizado para promoción a regresión permanente.

El independiente encontró que la retención C1 incluía sizing pero no el snapshot económico real recibido por MM. El manager autorizó retener `MMInput.Economics` en la única fila MATERIALIZED de cada intento; sin registrar todos los callbacks/ticks ni alterar decisiones. Este delta observacional entra en C2 para contrastar Balance, día, stage y revisión disponibles sin reconstruirlos como si fueran snapshots. La regeneración final no atribuirá ese detalle a los recibos C1 que no lo guardaban.

Sincronización comprobada posterior: Agents-OS local/remoto master `9458ea52cac539429122881e6e6fa812d26725f1`, árbol limpio antes de este delta. La sincronización fue automática, no push ejecutado por el manager.

### Desarrollo C2 anterior al freeze

V-F01 tiene regresión RED sobre C1 para PAUSED_SESSION, PAUSED_DAILY_GOAL y PAUSED_INTERNAL_LOSS (`implementer/evidence/red-expiry-c1.log`). El delta en desarrollo extrae sólo `resumeExpiredPlatformPause` y lo aplica antes de seleccionar, bajo la guarda de quiescence; no adelanta renovación, pagos ni transición funded. La prueba comprueba un nanosegundo antes y el vencimiento exacto, misma cuenta/caja/ledger/risk/terms. El grupo crítico posterior pasa backtester, Operation, tg y tgmm (`c2-critical-green.log`), todavía sin identidad C2 congelada ni aprobación final independiente.

Las pruebas independientes de Operation, TGMM, public TG y negativos Campaign se han promovido sin cambiar sus asserts. La adaptación portable de seis tapes E2E encontró un error de compilación DatasetManifest→Ref del adaptador de prueba, que el implementador está reparando; no se atribuye a producto ni se llama PASS. Cobertura delta y freeze pendientes. K01 largo C1 sigue RUNNING sano al24nov23:00Z, wall32m47/RSS28,6MB; restantes C1 aún no iniciadas.

Actualización de ejecución: los seis tapes permanentes E2E pasaron en9,841s (`implementer/evidence/permanent-e2e.log`), incluido borde de dos días con una cuenta/caja4880 y neto acumulado450,12 conservado. El error del adaptador quedó resuelto. K01 C1 largo terminó COMPLETE/reconciliado, resultado HORIZON_CENSORED y caja4280; sigue REFERENCE_ONLY por V-F01. El watcher verificó hashes antes de SIGTERM (`c1-supersession-watch.log/json`). K02 alcanzó a iniciar y su recibo real `bd0e53756beccb8e7b33d990711a405db25dc9ca9d4a6e1c12854d95d758ebc3` queda FAILED por `context canceled`, no “no ejecutado”; K03–K05 no admitidos por supersesión. Procesos C1/Go drenados según integrador. Las métricas largas se extraen independientemente antes de atribuir recuperación total.

El host presenta24CPUonline, pero no se toma como permiso de concurrencia. El techo agregado4cores es presupuesto conservador de esta reparación, no una quota kernel demostrada. Se mantiene máximo2campañas concurrentes bajo medición; GOMAXPROCS4 por proceso no equivale a reservar4cores en cada campaña.

### K01 largo C1: partición diagnóstica completa, no resultado final

Extracción independiente `verifier/campaigns-reference-C1-K01.json`, contrastada por el manager:755 cruces de referencia y755 señales físicas, partición sin UNKNOWN =650 rechazos de tamaño +85 operaciones con fills +20 cruces consumidos por exposición.735 operaciones materializadas,735 admisiones Provider,0 rechazos Provider;205 órdenes distintas,170 registros fill y186 contratos ejecutados, con entradas en13 fechas NY. B tenía31 materializaciones,31 rechazos y0 operaciones con fills; la diferencia de operaciones con fill es+85, sin porcentaje sobre cero. Los735 snapshots económicos de MM faltan en C1 y se marcaron ausentes explícitamente.

V-F01 sí afectó este corpus: las tres compras sucesoras coinciden exactamente con los cruces10:00NY del17oct,31oct y12nov. Las cuatro cuentas terminan válidas PAUSED_SESSION; caja4280 incluye compras/renovaciones. Por tanto85 NO se presenta como resultado corregido final ni como promesa para C2: reutilizar la cuenta válida cambia su riesgo y trayectoria posteriores. Esta corrida valida el extractor y demuestra recuperación de recepción, manteniendo el defecto de compra identificado. Diez campañas finales C2 siguen0/10.

Readback corto ampliado (`implementer/evidence/short-comparison.json`): los cinco baselines cortos y cinco C1 cortos están COMPLETE/reconciliados con23 OPEN en cada fila. Operaciones con fills primera jornada B→C1: K01 0→3, K02 1→16, K03 0→4, K04 0→3, K05 0→3. Cada baseline materializó sólo1 intento; C1 materializa23/21/23/23/23, con2 cruces ocupados explicados en K02. Esta comparación sigue siendo corta y C1; no reemplaza la tabla T1 C2 exigida.

### Retención compacta de pausas y cierre

El independiente acreditó otro hueco de observabilidad antes del freeze: `result.accounts` conserva estado final, pero no todas las transiciones de pausa/reanudación. El mandato exige métricas por cuenta/día y no corresponde inferirlas desde PnL. Se autoriza para C2 un registro tipado PLATFORM_ACCOUNT_STATE por cambio causal real, sin filas por tick. El estado de fallo derivado en finish se registrará antes de sellar el recorder, con razón FINAL_RISK_RECONCILIATION y timestamp observado al cierre; no fingirá ser el instante anterior de breach. El seam privado pre-close debe ser idempotente, preservar primera causa si falla el recorder y no mover clocks, selección ni ledger. Integración y pruebas pendientes mientras drena el grupo Go activo.

La selección Go C2 previa a ese delta pasó los cinco paquetes SDK con race; backtester sigue activo bajo límite15min. El patrón amplio incluye lifecycle de Platform/TestF, pero no BTGS04 ni CLI singleton, que permanecen pendientes aislados. No se confunde la ausencia de salida de fallo con PASS ni se mezclan perfiles de distintos bloques de source sin demostrar compatibilidad.

Actualización del grupo Go: timeout900s y exit1, drenado. Primera causa localizada en `TestPlatformPublic_AllFourTargetsCreditWithoutDailyEvalCeiling`, total4m24 y subcaso2300 activo1m22; sin assert previo informado. SDK5 PASS, backtester NOT_PASS. La selección amplia queda descartada para el siguiente intento; casos/targets explícitos y límites propios, sin escalera de paquetes completos. Los valores2250/2500 de compatibilidad en tests heredados no reactivan el catálogo de campañas.

La revisión previa al freeze identificó dos motivos de supresión todavía ambiguos: CAMPAIGN_UNAVAILABLE sin causa específica y absorción stageSettled posterior a CAMPAIGN_ALLOWED. Se autorizó retener la razón decisoria real por OPEN, sin cambiar la decisión ni contar dos veces el cruce. El independiente confirmó que el resto de datos requeridos tiene fuente: sizing, órdenes, fills, finality, cash, pagos y días. Quedan por verificar las retenciones nuevas y su propagación de errores; una hipótesis del manager sobre sobrescritura de closeErr en el seam final se envió a prueba de fallos, todavía no se declara defecto reproducido.

### Delta observacional C2 comprobado antes de freeze

`implementer/evidence/c2-observation.log`: PASS8,575s de transiciones reales sin duplicación, pre-seal idempotente, errores simultáneos observer/cursor/recorder con primera causa conservada, STAGE_SETTLED compacto y los seis tapes E2E permanentes. El integrador corrigió `closeErr` mediante composición de errores y degradación de éxito previo a FAILED cuando corresponde. El caso no se atribuye retrospectivamente a B: era un riesgo introducido en el seam nuevo, cerrado durante revisión.

Falsificación independiente ejecutada sobre ese árbol todavía no congelado (`verifier/delta-C2-tests.log`, exit0,0,144s): ocho negativos de claims tanto antes como exactamente al vencimiento de pausa, caja/cupo/sesión y triple fallo de Finish partiendo de COMPLETE, con observador/cursor idempotentes. PASS de este delta; cobertura nueva y validación sobre SHA/binario final siguen pendientes. No equivale todavía a certificación C2 ni a las diez campañas.

Primer fallo del grupo explícito posterior: panic en `TestCoveragePlatform_CreditRemainsPendingUntilClockAndStopsAtGrossCap`, fixture de reloj/owner puro sin RunState. El setter observacional nuevo intentaba usar recorder/coord ausente. Grupo drenado44s, NOT_PASS conservado. Manager adjudica preservar los asserts heredados y activar retención sólo cuando existe el Run real de campaña; no requerir runtime a una prueba pura de reloj. Corrección y prueba Record-only→FirstCause pendientes. Este fallo pertenece al delta de observabilidad nuevo, no explica las entradas históricas.

Control de cobertura solicitado: inventario completo de archivos productivos cambiados e instrumentables, incluyendo observación/Finish/driver, y perfiles únicamente PASS de fuente compatible. El porcentaje de bloques Go afectados debe nombrar ese denominador; no se presentará como porcentaje exacto de líneas nuevas si no fue medido así. Archivos modificados sin bloques deben justificarse como declaraciones/comentarios o permanecer como cobertura faltante, nunca desaparecer del denominador en silencio.

### Grupo explícito PASS y cobertura pendiente concreta

La incompatibilidad del fixture sin RunState quedó corregida preservando asserts. Grupo explícito C2 race PASS210,352s (`c2-platform-green.log`), más cinco SDK PASS. Auditoría preliminar del integrador (`coverage-delta-working.json`):285/325 sentencias de bloques afectados =87,69%, no gate≥95. Archivos instrumentables ausentes0. Huecos localizados:36 sentencias Campaign (transiciones funding/payout/compra y propagación de error),3 retornos driver y1 error de TR persistido. Se preparan casos puntuales; no se excluye código observacional para subir el porcentaje. Cotejo AST independiente y freeze todavía pendientes.

El independiente alineó las338 materializaciones históricas de las diez configuraciones a timestamps/cruces físicos (`baseline-opportunity-map.json`), sin unmatched. Amplió la conciliación por cuenta usando cashflows aplicados de ACCOUNT_CASHFLOW; cuatro balances C1 K01 concilian. La fórmula documental debe expresar grossFillPnL−fees+cashflows o netFillPnL+cashflows, sin restar fees dos veces; slippage permanece incorporado una vez en fillprice. El seam Finish nuevo se prueba como regresión de C2, no mediante un compile-red atribuido falsamente a B.

### Composición runtime: alcance comprobado

Inspección independiente y readback manager: `v3/core/internal/futuresruntime/runtime.go` resuelve Strategy y MM con CompositionFactories y el RunMode configurado; `v3/sdk/futures/config/composition.go` registra ModuleTG→tg.New y MMModuleTG→NewTGMM→tgmm.New. No hay rama de modo en tg/tgmm ni wiring nuevo pendiente para hacer configurables esos módulos. La prueba de Operation compara hechos iguales LIVE/BACKTEST, las regresiones públicas tg usan ProvenanceLive y se contrastan con CLI OHLC offline/oráculo. Esto acredita módulos compartidos y los puntos de conexión afectados, no feed/red/broker real ni confirmaciones externas. No se arrancó ni desplegó runtime LIVE. El controlador de caja/campaña multiaccount sigue siendo backtester; no se certifica una plataforma runtime real equivalente a esa campaña.

La hipótesis de payload StrategyDetails válido noobjeto no demuestra defecto en consumidores actuales: s1/s2/tg emiten objetos y no se halló fixture legítimo string/array. Se conserva la compatibilidad probada para ausencia y objeto sin política, con política desconocida/malformada fail-closed; no se amplía arquitectura por ese caso hipotético.

Actualización de cobertura previa al freeze:320/325 sentencias de bloques afectados =98,4615% según perfiles PASS (`c2-observation-fault-green.log`,2,729s race,13 fixtures de errores de transición y3 errores de señal/hook/supresión). Inventario14 archivos productivos modificados,11 con bloques ejecutables afectados, ausentes0. Se mantiene etiqueta WORKING_TREE_DIAGNOSTIC_ONLY hasta identidad congelada y cotejo independiente AST. Quedan5 sentencias sin cobertura en ese denominador; no se las oculta.

Vet encontró avisos en tests heredados: literales FixtureSessionStep sin campos nombrados y llamada fmt.Sprint sin consumir resultado. Se verifica preexistencia en B; si el gate requiere vet limpio, el manager autoriza sólo corrección mecánica preservando llamadas, inputs y asserts, nunca flags para ocultar el aviso. Freeze/build final todavía pendientes. Tras gate exacto independiente, los largos pertinentes podrán solaparse con una campaña inmutable dentro del presupuesto; una segunda campaña sólo al liberar el carril Go. Cualquier nuevo defecto funcional que cambie source obliga nueva identidad y comparación correspondiente.

### Freeze C2 comprobado por el manager

Commit `63fb24996d422f3dfee28e706ad1528eb948bff8`, rama de reparación `codex/tradesgerard-entry-repair-20261013`, árbol limpio al readback. Binario `implementer/bin/echo-backtest-63fb2499`, SHA256 `8eff860eca8db7d2aaf84e40903b0de4e03f367aad798a79d2c371bf1ecf8f50`, Go1.27.1, metadata VCS del mismo commit y modified=false. Contiene V-F01, retención económica/estados/supresiones y regresiones independientes permanentes; B y C1 conservados. Los ajustes mecánicos de vet pasaron sus tests afectados (`c2-vet-mechanical-tests.log`,0,091s). El cotejo final independiente sobre este SHA/binario y la procedencia de perfiles PASS están en preparación; freeze no equivale todavía a gate final ni a diez campañas realizadas.

### Gate independiente exacto C2 PASS; comparación final autorizada

El verificador completó sobre `63fb2499`/binario `8eff860e…` los negativos SDK/Campaign/Finish y seis tapes CLI sin regenerar input. V-F01 queda cerrado físicamente: tres operaciones sobre la misma cuenta, caja4880 y snapshot del neto previo190,08 conservado. Censo público independiente `comparison-final-63fb2499.json`:42969 identidades de barras,755 cruces y755 NewCycle, cero divergencias K/dirección/readiness; error ATR máximo2,842e−14<1e−9.

Cobertura independiente validada (`coverage-audit-63fb2499.json`, `coverage-ast-audit-63fb2499.json`):320/325 sentencias de bloques afectados98,4615%; cotejo adicional de sentencias ejecutables nuevas por inicio AST250/255=98,039%, posiciones sin mapear0. Los cinco huecos son retornos de error. Inventario14 archivos productivos: tres contienen sólo campos/enum/mapa estático sin nuevas sentencias y11 tienen bloques afectados. Se verificaron hashes de tres logs/perfiles PASS y14 fuentes; corridas FAIL excluidas. Compatibilidad se acredita por paquetes/dependencias instrumentados, no con una afirmación falsa de ausencia global de ediciones entre productores. SDK productivo no cambió C1→C2. El fallo previo en dos fixtures nuevos era reloj fuera de horario (18:30NY), corregido a10:30NY conservando asserts y producto; se esperaba llegar al fallo de recorder después de admitir una compra.

Diez planes C2 sellados preparados y jobs de build/preparación drenados. Manager comprobó K01r2300 B→C2: perfil, hash de corpus, config, warmup/trade_start/end, modelo de ejecución, rules, contratos/schedule e initial_state idénticos. Autorizado iniciar primera K01r2300 inmutable junto con casos largos aislados; máximo2 campañas al liberar Go, bajo presupuesto. Gate funcional/oráculo/cobertura C2 PASS; entrega global pendiente de casos largos y10/10 campañas con métricas independientes. Recursos al preparar:313MiB durable,15GiB libres.

### Inicio físico de comparación C2

Controlador `implementer/evidence/c2-final-progress.json`: K01r2300 RUNNING, PID/PGID2749037, build C2 inmutable;9 pendientes,0 completas/0 fallidas al primer readback. Afinidad CPU0–3 hace explícito el presupuesto de cuatro cores; archivos/recibos individuales por configuración y ningún retiro deduplicado. Libres14.952.042.496bytes en ese instante. La paridad normativa de los diez planes (`c2-ten-plan-normative-parity.json` y `c2-ten-plan-differences.json`) muestra únicamente diferencias en campaign_id, model_identity y commit/hash de build; todos los demás campos físicos/económicos del request son idénticos a B.

Primer caso largo aislado PASS: `TestBTGS04CampaignCollectedTotals`,12,896s, conserva ambos subcasos collected_without_replacement y four_collected_then_replacement (`c2-btgs04-collected.log`). El timeout anterior del paquete no se borra ni transforma en PASS; este recibo nuevo resuelve ese caso sobre C2. Restantes largos siguen pendientes hasta sus resultados.

### Nuevo fallo del gate largo: entrega todavía abierta

El aislado `TestPlatformCampaign_PublicProofPassFundingAndCashCredit` pasó33,448s (`c2-platform-lifecycle.log`). En cambio `TestPlatformPublic_AllFourTargetsCreditWithoutDailyEvalCeiling` terminó con cuatro subcasos FAIL: esperaba primer pago CREDITED y observó APPROVED (`c2-all-four-targets.log`,80,49s según readback independiente). Este es fallo de assert real, distinto de los timeouts anteriores. No se reduce ni se alarga su fixture por conveniencia; tampoco se exime por posible preexistencia.

Manager pausa nuevas admisiones del controlador final mientras se reproduce con salida persistente. K01 C2 ya iniciado puede seguir como diagnóstico condicional; no se abrirán K02–K05/otros retiros hasta adjudicar. Hipótesis a falsificar: tras pausa/fin de sesión, selectTurn reanuda cuentas y podría mantener una posterior porque vuelve ELIGIBLE antes de revisar prioridad de creación. El contrato conserva turno sólo hasta pausa/fin de sesión y exige orden de creación; esto no autoriza rotar después de cada TP. Todavía no hay primera divergencia física acreditada para esa hipótesis. El fixture de tres ciclos diarios (10:01/10:11/10:21) y pausa EVAL870 hace relevante la interacción multicuenta antes ausente en V-F01 de una sola cuenta.

### V-F02 confirmado: reanudación revive un turno terminado

Falsificación independiente con salida durable: el mismo subcaso2300 y horizonte2oct pasa en B (`verifier/payout-B-2300.log`,19,099s) y falla en C2 (`payout-C2-2300.log`,18,366s), preservando todos los asserts y valores. Primera divergencia contractual9sep14:01Z: ambas cuentas reanudaron14:00Z, están físicamente flat y elegibles, pero Campaign selecciona account/2, creada8sep14:21, antes que fx-acct-1, creada8sep14:01. El turno anterior terminó por PAUSED_SESSION; reanudar su estado no debe revivir su propiedad del turno.

La reproducción pública independiente de dos días (`verifier/turn-order-C2-red.log`,1,722s) falla exactamente al exigir fx-acct-1 en la primera entrada del segundo día. Sus seis materializaciones/dos cuentas y la conservación de turno entre TP del primer día sí cumplen. Se adjudica V-F02 como defecto funcional de Campaign; el manager autoriza reparación mínima por el integrador, conservando turno entre trades sin pausa y sin mover relojes, saldos ni reglas.

El pago de B se solicita17sep y acredita24sep; C2 lo solicita25sep, aprueba28sep y programa procesamiento7oct/crédito8oct, fuera del horizonte2oct. La relación causal completa de ese retraso con V-F02 queda pendiente del rerun corregido: no se altera el assert CREDITED ni se extiende el tape. C2 pasa a diagnóstico supersedido; se ordenó guardar/readback y drenar su K01 condicional y controlador pausado sin admitir las otras nueve campañas. Nuevo freeze C3, cobertura del delta y verificación independiente todavía pendientes.

Actualización V-F02: el integrador añadió estado explícito de turno activo en Campaign; una transición real fuera de ELIGIBLE termina el turno y la mera reanudación no lo restablece. Compra/selección válida lo inician. La reproducción pública de dos días pasa sobre árbol C3 en desarrollo (`implementer/evidence/c3-turn-green.log`,1,59s); no es aún freeze ni validación de los cuatro pagos. Manager inspeccionó el delta. El fixture unitario de vencimiento pedía selección un minuto por delante del frontier/reloj sin avanzar RunState; se autorizó alinear ambos en el instante exacto, preservando asserts de saldo/piso/cuenta y el negativo de selección futura pública. No se debilita el guard de selección físicamente drenada.

Drenaje C2 acreditado en `implementer/evidence/c2-supersession.json`: hijo financiero SIGTERM, exit2, recibo FAILED y primera causa `context canceled`; controlador detenido terminado sólo después de drenar el hijo, exit137. Manager comprobó los tres PID ausentes. Se conserva el estado inicial del controlador y el final; las otras nueve configuraciones no se ejecutaron. No hay campañas C2 activas ni resultados parciales presentados como COMPLETE.

La regresión ampliada C3 pasa5,606s (`c3-turn-and-expiry-green.log`): pausa interna producida por pérdida real, fallo oficial por riesgo real, orden de creación tras reanudar, conservación de turno tras TP y los tres vencimientos de pausa con ledger/risk/terms intactos. También pasa el negativo público de selección futura. El fixture unitario se corrigió sólo en reloj/frontier como se autorizó; pagos largos y validación independiente del freeze siguen pendientes.

### Suficiencia del before histórico y replay observacional acotado

El independiente confirmó que los recibos B permiten reconstruir órdenes/fills/operaciones/días/duración/rachas/cierres/caja/pagos y estado final, pero SearchRecorder excluía SIGNAL/OPERATION_APPLY y transiciones de cuenta; MM_EVALUATION no conservaba sizing ni MMInput.Economics. Por tanto no bastan para atribuir cada supresión ni acreditar snapshots económicos reales de las primeras admisiones. No se rellenarán esos campos con headroom hipotético.

Se autoriza preparar observación equivalente sobre B separado e inmutable, preservando su fuente/binario originales y todas sus decisiones. Alcance propuesto: cinco replays completos, uno por perfil, sólo después de acreditar equivalencia física/económica entre los dos retiros históricos que permanecieron EVAL; si esa equivalencia no se demuestra se ampliará el alcance necesario. Esos cinco replays sustituyen los prefijos de sizing, evitando repetirlos. Las diez campañas corregidas siguen siendo individuales y obligatorias. Las primeras admisiones históricas detectadas son K02 14oct14:33Z, K03 20oct14:16Z, K04/K05 28oct14:28Z; K01 no tiene admisión en T1. Se requieren identidad del build observacional y equivalencia de resultados con B original antes de usar sus métricas como before.

Equivalencia de retiros B comprobada (`verifier/baseline-pair-equivalence.json`): cinco pares PASS, cero diferencias; normalización limitada a referencias tipadas de IDs generados mediante biyección. Importes, timestamps, acciones y contadores se comparan sin normalizar; cuentas/caja/pagos/economía/MM/consumo/residuos coinciden, todas las cuentas permanecen EVAL y pagos0. Manager verificó los cinco resultados. Quedan autorizados cinco replays B observados enlazados a ambos retiros históricos; esto no permite deduplicar las diez ejecuciones corregidas.

### V-F02: pagos largos recuperados sin cambiar el oráculo

`implementer/evidence/c3-four-targets-green.log`: cuatro subcasos2250/2300/2500/3000 PASS74,624s sobre árbol C3 quieto, con los mismos precios, horizonte y asserts. Manager leyó el recibo2300: primer pago solicitado17sep14:15Z, acreditado24sep14:00Z, estado CREDITED y neto1651; recupera el calendario B que C2 había retrasado fuera de la ventana. Esto cierra la relación causal del fallo de pagos con el turno revivido, sin exigir rentabilidad a TradesGerard ni reactivar2250/2500 en su catálogo. Resultados completos en `c3-four-target-results/`.

Cobertura Campaign con race y procedencia nueva está ejecutándose; SDK podrá reutilizarse sólo si los bytes instrumentados/dependencias compatibles coinciden. Lifecycle y CLI singleton aislados todavía pendientes; C3 aún no tiene identidad final ni campañas definitivas.

### Definiciones de métricas finales

La duración de exposición se mide desde el primer fill hasta el último fill que deja residual final cero, con precisión de microsegundos. La demora posterior hasta el último snapshot TERMINAL se informa aparte cuando existe: no se confunde exposición flat con liberación de claims. Rachas incluyen sólo operaciones con fills físicamente cerradas, ordenadas temporalmente; netFillPnL ya descuenta fees una vez y el slippage está embebido en precios. Neto cero reinicia ambas rachas; declines sin fill no cuentan. Se verificará la ausencia de solapamiento que permite ordenar por materialización/cierre sin ambigüedad.

Operaciones por día NY se atribuyen al primer fill de entrada y se separan de account_day_id contable. Los totales de campaña agregan todas las cuentas preservadas, nunca sólo la última summary. Si una campaña termina antes, su horizonte observado se separa del censo completo de755 oportunidades; no se le asignan eventos futuros.

### Métricas históricas recuperadas sin reescribir T1

Readback de `verifier/operations-baseline.json`; pares2300/3000 equivalentes según auditoría anterior. Duración de exposición en segundos, calculada de fills físicos; el archivo conserva cada fecha/operación y valores sin redondear.

| Perfil | Operaciones con fill | Registros fill | Días NY con entrada | Mediana duración s | Máximo duración s | Máxima racha ganadora/perdedora |
|---|---:|---:|---:|---:|---:|---:|
| K01 |0|0|0|N/A|N/A|0/0|
| K02 |18|36|14|259,430|1071,928|2/3|
| K03 |7|14|5|468,220|800,267|3/1|
| K04 |1|2|1|800,267|800,267|0/1|
| K05 |6|12|2|1486,937|2432,534|2/1|

La operación histórica no equivale a un ticket fill. Tampoco se afirma que B prohibiera absolutamente toda segunda operación diaria: K02 llegó a dos y K05 a tres en determinadas fechas. El replay observacional debe explicar esas materializaciones adicionales y el efecto concreto de NewCycle/gestión/finality, sin sustituir una cadena causal por la etiqueta “una operación al día”.

### Cobertura C3 y unidades de presupuesto

Grupo explícito Campaign C3 con race PASS210,441s (`c3-platform-green.log`). Composición provisional: exclusivamente `c3-platform-green.cover` para backtester, más SDK C2 con bytes compatibles; ningún perfil backtester C2 ni remapeo de líneas. Inventario provisional B→C3:329/333 sentencias de bloques afectados=98,7988%, archivos ausentes0; cuatro retornos de error sin cobertura. El cotejo AST independiente y la identidad congelada siguen pendientes.

Se aclaran unidades tras inspeccionar `platform_search.go`: SearchRecorder tiene límite16MiB por campaña/archivo económico, porque se instancia para cada ejecución. Los logs stdout/stderr propios tienen techo agregado16MiB separado. Todas las trazas económicas sí se contabilizan en durable de la iniciativa≤768MiB y por lote/corrida≤256MiB; scratch propio≤2GiB y reserva libre≥8GiB. Crear carpetas no reinicia ningún agregado. Medición del manager en este corte:322.083.467 bytes durables de iniciativa y14.826.213.376 bytes libres; no es un máximo instantáneo. Procesos/servicios ajenos permanecen intactos.

### Freeze C3 comprobado

Source `26f3459cba47fd05f5ef9aed3d205c3c5bbad81a`, rama `codex/tradesgerard-entry-repair-20261013`; manager verificó árbol limpio y commit. Binario `implementer/bin/echo-backtest-26f3459c`, SHA256 `92e27ef71d22bc9897af7f3c26d1fbe980f5f591b749224258747fd40c2584c9`, Go1.27.1, VCS del mismo commit y modified=false. Vet PASS informado por integrador; lifecycle aislado PASS30,937s leído por manager. Cuatro pagos y regresiones de turno pasan sobre los mismos bytes productivos congelados.

Procedencia `implementer/evidence/c3-coverage-provenance.json` leída: productor nuevo backtester PASS210,441s, perfiles/logs con hashes y comando exacto; SDK C2 reutilizado sólo porque el diff SDK C2→C3 está vacío. Perfiles C2 de backtester excluidos. Auditor recibió fuente/build para gate independiente exacto y cotejo AST; diez planes C3 en preparación y CLI singleton pendiente. Freeze no equivale a entrega completa.

### Gate independiente exacto C3 PASS; comparación vuelve a habilitarse

Independiente sobre `26f3459c`/binario `92e27ef7…`: pruebas de pausa por objetivo/sesión/interna, fallo oficial y conservación de turno tras TP PASS3,890s (`verifier/final-26f3459c-backtester-tests.log`); seis tapes CLI exactos PASS y V-F01 permanece cerrado. Cobertura recalculada:329/333 sentencias de bloques afectados98,7988%, AST259/263 sentencias nuevas98,4791%; inventario14 archivos, instrumentables ausentes0 y sentencias sin mapa0. Los resultados/cotejos de perfil tienen procedencia explícita C3 para Campaign y SDK C2 compatible.

El censo completo42969/755 se reutiliza por identidad de bytes del SDK entre C2 y C3; no se afirma una nueva ejecución del oráculo C3. Las diez campañas contrastarán sus señales físicas contra esas identidades. El manager autorizó CLI singleton aislado y, al comprobar inicio sano, K01 C3 inmutable en paralelo; una segunda campaña al drenar Go y medición antes de ampliar concurrencia. Cualquier nuevo fallo funcional mantiene abierta la entrega. B observado se prepara en superficie separada, sin bloquear el freeze ni mutar B.

### Inicio físico de comparación final C3 y CLI completo

Manager leyó `c3-cli-singleton.log`: `TestLASTPublicExperimentCampaignSealsAndReplaysSingletonCatalog` PASS119,736s, incluidos artifact y manifest; resuelve el caso antes interrumpido por timeout sin alterar asserts. `26f3459c-final-progress.json` acredita K01r2300 RUNNING con SHA/binario C3, PID/PGID2765357, afinidad0–3,0 completas/0 fallidas y9 pendientes al corte. Reserva libre14.780.788.736 bytes. Tras drenaje Go puede admitirse segunda campaña; concurrencia superior sigue requiriendo medición, no se deriva de las24CPU del host.

El recibo independiente `verifier/exact-gate-26f3459c.json` y `coverage-provenance-readback-26f3459c.json` quedaron materializados y leídos: FUNCTIONAL_COVERAGE_EXACT_GATE_PASS_FINAL_CAMPAIGNS_PENDING y PASS_READBACK, con hashes físicos de dos perfiles/logs y14 fuentes. Auditorías AST/bloques enlazan ahora esa validación explícita; no conservan una plantilla de compatibilidad sin resolver.

### Paridad de los diez planes C3 y ampliación medida

Readback `c3-ten-plan-normative-parity.json`/`c3-ten-plan-differences.json`: las diez solicitudes difieren de B únicamente en campaign_id, model_identity y commit/hash de build. Corpus, perfil, ventana, historial, contratos, horarios, initial_state, R/T y modelo de ejecución se conservan. K01 y K02 C3 r2300 están RUNNING,0/10 completas al corte; no se deduplican retiros.

Medición manager de los dos hijos financieros a6m33/3m28: CPU acumulada152%/137%, RSS24.140/23.452KiB, read_bytes físico0 en ambos (lectura cacheada), write_bytes2.572.288/1.433.600 y sin estado de espera D. RAM disponible66.192.052.224 bytes y disco libre aproximadamente14,77GB. Se autoriza prospectivamente un tercer slot total para un B observado serial, sólo después de build/equivalencia corta, manteniendo afinidad globalCPU0–3 y presupuesto durable768MiB. El controlador corregido permanece máximo2; no se autorizan cuatro slots ni más cores. Habrá medición bajo tres procesos y menor admisión si aparecen presión/degradación o reservas insuficientes.

Manager inspeccionó manifest/helper B observado: sidecar selectivo, coordenada leída sin incrementar StepSeq, inputs MM reales y errores que invalidan evidencia observacional. Identidad necesaria: SHA B más hashes de overlay/shadows/helper y binario nuevo; metadata VCS de un build con overlay no basta para atribuirlo a B original. Equivalencia corta y completa todavía pendientes.

Primer build B observado NOT_PASS (`implementer/evidence/baseline-observation-build.log`): el helper/overlay intentaba leer `SignalDelivery.NewCycle`, campo inexistente en B. Se corrige el adaptador correlacionando la señal original por SignalID; no es defecto nuevo de B ni cambio a C3. Se conserva el log; se solicitó conservar el manifest del intento y documentar si los shadows ya fueron reemplazados antes de regenerar hashes. Dos campañas C3 continúan sanas; al readback parcial K01 había procesado10nov23:00Z, sin tratar ese avance como resultado final.

Precisiones independientes posteriores: los cuatro pagos C3 acreditan24sep14:00Z. Para2300, C3 solicita17sep14:15Z y B17sep14:25Z: coinciden fechas de procesamiento/crédito, no todos los timestamps ni toda la trayectoria económica. No se afirma equivalencia de resultados B/C3. El cierre causal V-F02 se basa en C2→C3 con el mismo fixture y el delta de turno, que recupera CREDITED dentro de horizonte.

El intento1 del observador quedó preservado íntegro en `verifier/baseline_observation_failed_attempt1/`, incluidos manifest/shadows/helper/generador y hashes en preservation.json. El adaptador corregido retiene StrategyCycleSeq físico; NewCycle existe en el draft público, no en SignalDelivery/canonical, y su correlación desde `tg-baseline-bars.csv` deberá etiquetarse como tal, sin simular un campo observado. Los estados físicos before/after de owner/delivery gobiernan la atribución.

B observado intento2 compiló exit0, binario distinto SHA256 `0d3f09a7469b463d20ca49cf9ea601b985ad8ce1ec69be42bef636fb8e7d502b`. Primera equivalencia corta independiente PASS (`verifier/baseline-observation-short-equivalence.json`), pero sólo cubre dos filas legacy de rechazo/ghost y ocho eventos sidecar, sin órdenes/fills. No basta para habilitar full5: se pidió repetir la jornada K02 histórica que sí contiene ejecución física y pausa, con comparación exacta. Los archivos de este build se identifican mediante manifest de overlay además de metadata B; B original sigue intacto.

### Primera campaña final C3 completa:1/10

K02r2300 terminó COMPLETE, exit0, conciliada y terminal HORIZON_CENSORED. Recibo `implementer/evidence/candidate-26f3459c-t1-K02-r2300/57339452370034ebbe8584c685ecbf1937dc430282bd973bc55f53b2c2624b59/receipt.json`; controlador verificó digests de result/economic. Manager leyó progreso y resultado: caja4400, traza6.463.050 bytes, wall1095,407s. No se interpreta aún su frecuencia/PnL sin extracción independiente de identidades, cuentas y horizonte. K01/K03 siguen RUNNING, cero fallos finales al corte.

Durable agregado informado372.234.504 bytes y libre14,726GB. B observado K02 corto físico está ejecutándose para ampliar la equivalencia; sus cinco planes están preparados pero todavía no admitidos. Se prioriza readback independiente de K02 C3 para comprobar partición completa, sizing y métricas sin esperar las diez corridas.

### K02 final verificada: recuperación18→53 operaciones

`verifier/T1-K02-r2300-exact-receipt.json` leído: VERIFIED_ONE_OF_TEN, build/result/event digests exactos, horizonte íntegro31sesiones.755 cruces =53 admisiones con fills +696 rechazos de tamaño +6 cruces ocupados descartados sin backlog; cero UNKNOWN y cero snapshots económicos ausentes.749 materializaciones,53 operaciones agregadas,106 registros fill y112 unidades ejecutadas. El before comparable tiene18 operaciones: diferencia absoluta+35, sin cambiar parámetros. ATR máximo error2,13e−14 respecto del oráculo.

Métricas independientes K02:12días con entrada, máximo16operaciones/día; duración de exposición mínima0,25s, mediana151,745s, máxima1294,895s; rachas4ganadoras/7perdedoras. Cuatro cuentas, dos FAILED_RULE y dos PAUSED_SESSION;4pausas por objetivo y71 de sesión; cero pases/pagos. Neto fills−1378,88, cuatro balances conciliados; caja4400=5000−4×120−renovación120. Queda por desarrollar la distribución económica de los696 rechazos: no se cierra la explicación con “sizing” genérico.

K01 C3 también terminó COMPLETE, exit0 y traza5.569.417 bytes:2/10 completadas, readback independiente K01 en curso. K03/K04 activos. B observado K02 corto pasó comparación de13filas legacy incluyendo órdenes/fills, finanzas/MM/consumo/residuos; sidecar76eventos completo con23cruces/4transiciones y22 entregas a ciclo abierto sin exposición física. Identidad observacional validada. Se admitió un único B observado serial full5, K01 primero, bajo el tercer slot autorizado. Medición de tres procesos (`three-campaign-resource-snapshot.json`): afinidad0–3 en todos, RSS total≈64MiB, sin espera D, durable380.581.088 bytes y libres14.715.617.280 bytes; sin presión de recursos observada.

### K01 final verificada y límite económico residual acreditado

Readback independiente `verifier/final-T1-receipt-readback-26f3459c.json`: dos configuraciones verificadas, sin extender ese estado a las ocho pendientes. K01:755 cruces =19 operaciones admitidas con fills +731 rechazos MM +5 cruces ocupados.750 materializaciones,38 registros fill, cero UNKNOWN o economía ausente. Before0, after19, diferencia absoluta+19; una cuenta, caja4760=5000−compra120−renovación120. El resultado no se compara como objetivo contra las85 operaciones C1, cuya trayectoria contenía compras indebidas.

K01, `verifier/campaigns-final-26f3459c.json`: cuatro días con entrada (14oct3,15oct2,20oct10,21oct4); duración de exposición mínima17,409327s, mediana230,547369s y máxima1449,674922s; rachas netas ganadora5/perdedora9. Ocho cierres EXIT/MARKET y once PROTECTIVE/STOP_MARKET;31 pausas SESSION, ninguna INTERNAL_LOSS o DAILY_GOAL, cero pases/cobros. Las filas por operación y por día quedan fuera del vault, enlazadas desde ese recibo; no se pierde el detalle por usar observabilidad compacta.

`verifier/sizing-distribution-final-26f3459c.json` descompone las750 materializaciones K01:113 con presupuesto de referencia (19 admisiones/94 rechazos), cinco recortadas por remanente (todas rechazadas) y632 recortadas por headroom (20 por margen interno restante,612 por mínimo monetario Provider; todas rechazadas). K02:87 de referencia (45/42),201 por remanente (8/193),461 por headroom (83 interno/378 Provider, todos rechazos). “Margen interno1000−pérdida realizada” es una restricción de presupuesto, no una transición PAUSED_INTERNAL_LOSS; las pausas físicas se cuentan sólo desde transiciones reales.

La baja actividad posterior de K01 tiene prueba específica en `verifier/headroom-K01-analysis.json`: al cierre contable15oct21:00Z el saldo51275,10 fija piso EOD49275,10 (trailing2000). Después del último fill del21oct17:50:05,882Z queda saldo/equity49290,38; el piso no desciende. El margen EOD es15,28. Al final el límite diario permite1100, pero el mínimo Provider sigue15,28, con posición/reservas cero. Ledger: bruto−615 menos94,62 de comisiones ya debitadas =neto−709,62, sin doble cobro.

El sizing vigente desde referencia **previa al fill**, con SL positivo mínimo de un tick, exige19,98:5 de distancia geométrica +4,98 de comisiones +10 por ambos slippages modelados.15,28 no alcanza bajo ese modelo de admisión, aunque el ATR disminuya. Esto **no es un mínimo universal del exchange ni una imposibilidad física de cualquier política**: desde un fill ya conocido, un SL de un tick con sólo el slippage de salida pendiente costaría14,98 incluyendo fees. Comprimir/reanclar esa geometría antes de admitir Q1 exige resolver una política nueva; no se aplica ni se convierte silenciosamente en Q1 forzado. TechnicalStop sigue siendo referencia: la protección posterior sí se recalcula por presupuesto económico congelado. Aumentar ATR no cura este rechazo. La cuenta sigue formalmente elegible al reanudar sesión y el contrato vigente conserva su turno/selección.

Única decisión nueva propuesta, **NO aplicada**: considerar no seleccionable una cuenta flat, sin claims ejecutables, cuyo margen persistente por piso EOD sea inferior al mínimo Q1 del **sizing prefill vigente**; seleccionar la siguiente elegible o comprar a demanda bajo los mismos controles. Conservar cuenta, saldo, piso y cupos. Esto permitiría superar este bloqueo de selección dentro del modelo vigente; consumiría caja/cupo y cambiaría la trayectoria económica. No se extendería a un rechazo aislado por ATR ni a un margen diario temporal. Es política nueva separada del before/after, no condición para continuar la reparación autorizada.

### Precisiones de admisión y economía efectiva

Los contadores Provider750/749 de K01/K02 son grants para admitir/materializar la Operation **antes** de sizing MM; no significan órdenes ni contratos ejecutables. Las cantidades efectivamente admitidas se cuentan después de MM, y las órdenes/fills físicos se concilian aparte. El extractor conserva esta distinción de alcance.

`verifier/first-closures-K01-arithmetic.json`, cotejado por manager: primer TP LONG compra24901→venta24914,Q1; bruto260 menos fees4,98=neto255,02 frente T250. Proyección desde el fill real reserva sólo costos de salida pendientes: precio bruto24913,999 alineado24914 implica neto proyectado250,02; la salida MARKET física posterior puede superar ese umbral. La referencia de cotización implícita24914,25 se deriva del fill/slippage declarado, no se presenta como quote observado. Primer SL SHORT vende25303,50→compra25315,75: bruto−245 menos4,98=−249,98 frente R250. Stop económico bruto25315,501 se alinea25315,50 y el fill añade0,25 de slippage de salida. Aritmética monetaria/ticks exacta, sin epsilon ni doble descuento; la tolerancia ATR es un asunto separado.

### Baseline K01 observado completo: equivalencia preservada

`verifier/baseline-observed-full-K01-equivalence.json`: PASS independiente. Las138 filas legacy completas coinciden con B original tras normalizar exclusivamente IDs tipados; también coinciden finanzas/MM/daily/cuentas/caja/pagos/consumo/residuos. Sidecar completo:2422 eventos,755 cruces,31 evaluaciones MM y64 transiciones de cuenta. El replay mantiene0 operaciones con fills,31 rechazos y caja4760. Es evidencia observacional de B, con overlay/binario identificados, no una recompilación atribuida al hash binario histórico.

Primera oportunidad posterior al rechazo, SHORT14oct14:48Z: owner físico **CREATED**, no ACTIVE, sin exposición, claims ni admisión pendiente, mismo CycleSeq1. La operación fantasma sin órdenes persiste y el cruce se entrega al mismo ciclo; el defecto queda demostrado en el recorrido físico, además de la regresión aislada. La clasificación causal incluye estados no terminales como CREATED, sin cambiar los hechos ni llamarlos exposición real. C3, sobre los mismos755 cruces K01, llega a750 materializaciones y19 operaciones con fills. La atribución por identidad se completa con la comparación de trayectorias; no se suman por separado los efectos del latch y de la falta de finalización sobre el mismo cruce.

K02 observado continúa bajo equivalencia completa individual obligatoria. C3 mantiene2/10 verificadas y K03/K04 en ejecución en este corte.

Comparación causal K01 completa (`verifier/causal-full-B-vs-C3-K01-r2300.json`):755 identidades alineadas, cero exclusivas de before o after. B particiona31 evaluaciones MM +721 cruces con owner CREATED/flat/sin claims +3 ROLLOVER_GATE_DISABLED en las fronteras exactas10NY. C3 recupera **719 intentos MM adicionales**:716 desde el owner fantasma y tres desde el gate; cinco de aquellos721 se descartan legítimamente por exposición en la nueva trayectoria. De los31 intentos comunes, sólo uno conserva la misma economía y30 tienen trayectoria económica distinta. No es válido atribuir esas30 diferencias exclusivamente al ATR ni sumar latch/finality como recuperaciones independientes. Las19 entradas K01 se acreditan con fills, separadas de los719 intentos recuperados.

### Tercera campaña C3 verificada: K03 de7 a14 operaciones

`verifier/final-T1-receipt-readback-26f3459c.json` acredita 3/10 configuraciones, identidades/digests y conciliación exactos. K03 r2300: 755 cruces = 14 admisiones con fills + 735 rechazos MM + 6 ocupados descartados; 749 materializaciones, cero UNKNOWN o snapshots ausentes. Before 7, after 14, delta +7. Hay 28 registros fill, 36 órdenes distintas y cuatro días con entrada (14oct:4, 15oct:5, 17oct:3, 20oct:2). Duración exposición mínima 14,393939s / mediana 261,445055s / máxima 1163,766233s; rachas 3/3.

Los735 rechazos K03 son55 a presupuesto de referencia,12 por remanente y668 por headroom (15 margen interno/653 Provider). Las14 admisiones se distribuyen11 referencia/1 remanente/2 headroom. Dos cuentas conservadas PAUSED_SESSION, una pausa DAILY_GOAL y61 SESSION; cero pases/cobros. Neto agregado−1624,72, caja4520=5000−dos compras120−dos renovaciones120. Se mantienen R/T500/(1000/3), fuente y ventana: más intentos no eliminan los límites ni garantizan PnL positivo.

### Recursos: ampliación medida del presupuesto agregado

Auditoría física de horario `verifier/physical-session-final-26f3459c.json`: las86 operaciones con fills de las tres configuraciones verificadas entran desde10NY y antes15:50, quedan flat en la misma fecha NY y antes15:55. Último cierre K03 a15:50:00,176991 es confirmación física posterior al acto de liquidación15:50; no es una nueva entrada ni overnight. No se certifica broker/runtime real.

El techo previo de cuatro cores era decisión conservadora del manager, no una cuota externa demostrada. Readback `implementer/evidence/cpu-policy-readback.json`: README pide GOMAXPROCS4 por carril y contempla experimentos independientes con concurrencia medida; ancestros cgroup sin cuota CPU y cpuset0–23. Medición manager `vmstat 1 5`:53–57% idle,15–19% iowait y seis procesos bloqueados ajenos; nuestros tres hijos no estaban en D, su lectura física era cero, RSS conjunto≈80MiB y reserva de disco intacta. No se atribuye el iowait ajeno a estas campañas ni se intervienen procesos ajenos.

Se autoriza prospectivamente afinidad agregada0–5 (seis cores), conservando **tres jobs totales**, GOMAXPROCS4 por proceso, mismos builds/inputs y todos los límites de memoria/disco/trazas. Aplicación en threads propios sin reinicios, con recibo antes/después y medición posterior; volver a0–3 si aparece presión relevante. Esto no es un benchmark de velocidad ni una expansión inferida sólo de las24CPU del host. Las duraciones de pared se conservan como datos de ejecución bajo condiciones distintas, sin compararlas como mejora de performance.

### Cuarta campaña completa; retiro3000 comienza físicamente

Controlador `26f3459c-final-progress.json` acredita K04r2300 COMPLETE, exit0, digests y contabilidad conciliados, wall2332,11s. Censo preliminar del integrador (`c3-K04-r2300-summary.json`):34 operaciones con fills frente1 histórica; verificación independiente pendiente, no elevar todavía esta fila a VERIFIED. K05r2300 y K01r3000 están ejecutándose. El nuevo hijo K01r3000 tiene todos sus threads en0–5 según `future-campaign-affinity-readback.json`; mismo binario/plan sellado. Retiro3000 tiene ejecución propia, no se infiere desde2300.

Medición posterior al cambio de afinidad (`cpu-budget-6cores-measurement.json`): tres hijos consumen4,518 cores agregados en45,004s, RSS conjunto≈70MiB, ninguno en D, lectura física delta0 y escrituras pequeñas. Host42% idle/17% iowait, sin swapin/out, disco libre14,702GB. Sin presión propia o degradación de reserva observada; se conserva presupuesto seis cores/tres jobs. La configuración efectiva por threads, con override fechado, gobierna sobre las plantillas históricas que aún dicen0–3.

### Hallazgo prioritario en auditoría de cierre K02: margen omitido

La reconstrucción de motivos de cierre detectó una Operation K02 el12nov10NY con EXIT neto−34,98 que no podía llamarse TP. El auditor encontró en su MATERIALIZED balance/equity48890,32 y PnL diario0 con PnLFresh=true, pero **HardMonetaryHeadroom ausente**; MM utilizó margen1000/R500/Q1. Un piso EOD48885,20 implicaría5,12 de margen, pendiente confirmar su vigencia temporal exacta y la rama de selección que omite la economía. Hay entrada física y posteriores EXIT cancelados/reemitidos, con fallo de cuenta. Se investiga `SelectPreservedAccount`/reset de riskEval; no se reduce a una etiqueta de cierre.

Manager ordenó detener nuevas admisiones C3 mediante el hold del controlador, conservando las campañas en ejecución y manteniendo B observado. Fuente/build C3 permanecen congelados. Un cierre de esta primera divergencia y un nuevo gate independiente son obligatorios si se confirma defecto; los PASS acotados y resultados físicos anteriores se conservan sin convertirlos en certificación de toda la cadena.

Inspección de fuente concordante manager/implementador: `openAccountDay` entrega ACCOUNT_ECONOMICS antes de `projectEconomics`; `deliverDayEconomics` construye un snapshot con Balance/Equity/PnL pero sin HardMonetaryHeadroom. Operation guarda ese snapshot incluso sin operación activa y `DeliveredEconomics` sustituye íntegramente la economía de Views al decidir. `SelectPreservedAccount` restaura riskEval preservado; no es correcto afirmar que lo resetea. La ruta incompleta está en la entrega/proyección diaria y su cache de owner; falta cerrar el enlace temporal de piso/revisión en la reproducción física antes de adjudicar el parche. PnLFresh=true y snapshot presente no bastan para acreditar que todos sus campos de riesgo están completos.

**V-F03 confirmado y adjudicado después de ese corte**: PROVIDER_FACT físico del11nov22:00Z de la cuenta2 fija EODfloor48885,20, margen5,12 y outcomeOK. DAY_OPEN rev10035 mantiene balance48890,32/PnL diario0; MATERIALIZED usa esa misma revisión pero pierde HardMonetaryHeadroom y admiteR500/Q1. La primera divergencia está en la entrega económica incompleta, no en el precio del fill ni en un supuesto reset de piso. El resultado económico conciliado no valida esa entrada.

Manager autoriza fix mínimo en el owner de entrega/proyección diaria, preservando límite, ledger, cuenta, geometría y estrategia, con RED independiente sobre RunState real estacionado→cambio de día→restauración→nueva señal. C3 queda supersedido para aceptación funcional. Se ordena cancelar sólo K01r3000 por supersesión con drenaje y estado fallido real, conservar K05r2300 si cercano al final y mantener B observado. C4 se prepara en checkout separado, sin compilar sobre C3 mutable ni sobrescribir sus binarios; presupuesto durable agregado768MiB sigue vigente. No se propone compensar esta omisión aumentando riesgo ni forzando cantidad.

RED independiente C3 (`verifier/headroom-C3-red.log`,2,325s): RunState real con cashflow ADJUSTMENT−1994,88 para crear margen5,12 sin breach; estacionamiento, timer real de cambio de día y restauración de propietarios financieros. Provider y Views conservan5,12; DeliveredEconomics tiene Fresh=true pero headroomnil. Primera entrega→grant Provider→MM TG real produce ENTRY_SIZED y una OrderRequest cuando debía declinar. El assert de margen requerido falla por la causa prevista. No se mutaron directamente OwnerState ni riskState. Este cashflow es fixture de regresión, no señal/depósito añadido a las campañas T1. Dos intentos previos con errores de firma/seam se preservan como errores del adaptador, no como RED funcional.

K01r3000 C3 quedó FAILED/context canceled a16:37:34Z, exit2; wrapper2785913/hijo2785914 ausentes comprobados por implementador (`c3-V-F03-supersession.json`). Cuatro retiros3000 restantes no ejecutados por supersesión. K05r2300 seguía en21nov al corte y se conserva para censo intermedio; ninguno sustituirá las diez ejecuciones de la versión reparada.

El mismo probe RED falla sobre **B original** en2,530s (`verifier/headroom-B-red.log`), por la misma pérdida de margen y ENTRY_SIZEDQ1. V-F03 es preexistente, no un efecto creado por la corrección C3. Censo inicial de cuatro campañas C3 completas:14 snapshots MATERIALIZED con HardMonetaryHeadroom ausente pese a existir objeto Economics: K01 uno/rechazado; K02 siete (seis sized/un rechazo); K03 cinco (uno sized/cuatro rechazos); K04 uno/rechazado. Que falte el margen demuestra entrega incompleta; no prueba que todas esas cantidades concretas excedieran el margen real. La atribución por fila debe contrastarlo con su piso/economía temporal. `missing_economic_snapshot=0` se rectifica como presencia del objeto, no completitud de sus campos requeridos.

### C4: parche mínimo aislado y primer GREEN

Checkout nuevo `implementer/echo-c4`, rama `codex/tradesgerard-entry-repair-c4-20261013`, desde C3. Manager inspeccionó el delta productivo: dos archivos,26 inserciones/43 eliminaciones en ese corte. `openAccountDay` proyecta primero el riesgo de la revisión actual y después entrega la economía; un constructor account-wide común sirve Views, entregas diarias y observaciones. Cycle se añade sólo en la observación específica de operación. No se añade un guard MM compensatorio ni se modifica R/T/ATR/límites. C3 permanece intacto.

Implementador ejecutó la regresión independiente promovida: GREEN2,478s, Provider/Views/cache/MM conservan5,12 y TG_SIZE_BELOW_MINIMUM devuelve cero órdenes. Es un GREEN de desarrollo, todavía sin freeze/gate independiente C4 completo. El carril Go está coordinado y la cobertura Backtester se recalculará sobre las líneas C4, sin remapear perfiles C3.

Inspección runtime: los constructores productivos de AccountEconomicsUpdate encontrados en v3 son el diario Backtester afectado y ohlc_driver que usa Views; Core decodifica el tipo compartido completo sin reconstruir ese literal. Se prepara prueba offline de ingreso tipado LIVE/BACKTEST con el mismo snapshot. El publicador externo LIVE no fue ejecutado ni certificado.

C3 termina físicamente con cinco r2300 COMPLETE de referencia, K01r3000 FAILED/context canceled y cuatro r3000 no ejecutadas. Controlador drenado exit2, sin loop hold residual. K05 intermedio reporta25 operaciones frente6 históricas; no se presenta como comparación final reparada. B observado2/5 COMPLETE y K03 activo. Durable agregado con checkout C4≈650MB, bajo techo768MiB; builds/resultados B/C1/C2/C3 preservados.

### Baseline K02: equivalencia y bloqueos separados

`verifier/baseline-observed-full-K02-equivalence.json`: PASS,337 filas legacy completas y economía/cuentas/caja/pagos/revisiones sin diferencias tras normalizar únicamente IDs tipados. Sidecar2427 eventos,755 cruces/36 MM/64 transiciones. Los755 cruces se particionan en36 materializaciones MM,670 owner no terminal sin exposición,44 gate deshabilitado y cinco ocupados físicos.

Los44 gate se desglosan en tres fronteras10NY con pausa vencida antes de su refresh, y41 cruces durante PAUSED_DAILY_GOAL todavía vigente en esa cuenta (18 el21oct después de14:27Z;23 el29oct después de14:45Z). Esas pausas de cuenta son legítimas. El veto global a comprar otra cuenta es una cuestión distinta, que exige caja/cupo/sesión/finality acreditados; no se atribuyen automáticamente41 fills recuperados ni todos los gates al mismo bug. Un cruce admitido después de cambiar la trayectoria económica se etiqueta como tal.

De las36 materializaciones B, ocho corresponden a drafts NewCycle=false: tres primeros intentos diarios desplazados después del gate10NY y cinco reentradas con owner ya TERMINAL/flat/sin claims en el mismo StrategyCycleSeq. La rama de admisión OPEN con owner terminal explica por qué B podía superar una operación diaria aun conservando el latch defectuoso; no existía una prohibición uniforme de un trade al día. Source, estados físicos y conteos se conservan separados de cualquier contrafactual.

### C4: completitud y paridad offline en desarrollo

Readback manager de `implementer/evidence/c4-economics-completeness-green.log`: tres pruebas PASS2,374s, incluida la regresión independiente promovida. Con Provider/Views/cache en5,12, MM rechaza TG_SIZE_BELOW_MINIMUM y emite cero órdenes. La prueba de perfil sin familia monetaria evita convertir un campo condicional en requisito universal. `c4-core-economics-parity-attempt4.log`: PASS0,027s para ingreso tipado LIVE/BACKTEST y TGMM real. Tres intentos anteriores del adaptador quedan documentados en `c4-core-fixture-attempts.json`; no son RED funcionales ni se borraron. Se ejecuta cobertura Backtester fresca sobre C4 antes del freeze; no se remapea cobertura C3.

Auditoría independiente prospectiva `verifier/monetary-authority-final-26f3459c.json` cubre las cinco referencias C3:18 omisiones de margen (K01–K05:1/7/5/1/4). Los campos presentes concuerdan exactamente con ledger, base diaria, piso EOD vigente, cuenta, revisión y as-of aplicables. El gate C4 exigirá importe correcto además de presencia; una fecha previa sigue siendo válida si no cambió la autoridad económica. Omisión no equivale automáticamente a admisión inválida: el caso concreto K02 ya acreditado se mantiene separado.

Agregados recuperados sin trazas nuevas: `verifier/operation-account-day-aggregates-baseline.json` para las diez B y `operation-account-day-aggregates-C3-reference.json` para las cinco referencias, con operaciones, ganancias/pérdidas/cero, neto, duración, rachas, fills/unidades por cuenta, fecha NY y día contable. Los motivos de cierre se auditan aparte; el rol EXIT no demuestra TP. C4 usará el mismo extractor.

Durable medido662.673.149 bytes frente805.306.368 de techo global, incluidos ambos checkouts C3/C4; reserva de disco14,13GB. Se conservan fuentes/builds/evidencia y las nuevas filas machine-readable pueden serializarse compactas sin perder valores ni procedencia. Se medirá por campaña; la holgura es un presupuesto, no autorización para excederlo.

`verifier/nil-headroom-invalid-sizing-C3.json` separa las18 omisiones de las admisiones realmente incompatibles con su margen: dos en K02. El31oct10NY Q1 tiene pérdida geométrica modelada369,98 frente margen real10,16; el12nov10NY439,98 frente5,12. Las demás omisiones no se convierten por inferencia en órdenes inválidas. El primer caso cerró por SAFETY_FLATTEN explícito; el segundo motivó la investigación del cierre inicialmente UNKNOWN. Ambos pertenecen a la misma causa V-F03. No se afirma el PnL contrafactual de haber rechazado correctamente.

B observado K03: `verifier/baseline-observed-full-K03-equivalence.json` PASS,229 filas legacy cotejadas, cero diferencias;755 cruces y36 MM. Se acredita equivalencia de tres de cinco replays. C4 grupo causal Backtester PASS229,159s (`c4-platform-green.log`);45,6% es cobertura del paquete completo durante ese selector, no cobertura del delta. El cálculo nuevo≥95% y su procedencia permanecen pendientes. Readback de sincronización Agents-OS anterior a estas últimas líneas: master local limpio y remoto ambos `f6f44eb804c64b416abf887cfbb3aa3319a321b6`.

### Gate C4 en curso: cobertura provisional y fallo de preparación

Cobertura de desarrollo `c4-coverage-delta-working.json`: CONSERVATIVE_DIFF_BLOCKS_V1,346/350=98,8571%,15 archivos productivos cambiados y12 con bloques instrumentables, cero ausentes. Procedencia `c4-coverage-provenance-working.json`: SDK C2 PASS por identidad de bytes y Backtester C4 nuevo PASS; fuente aún WORKING_TREE_DIAGNOSTIC_ONLY, no aceptación de un SHA C4 congelado.

Primer AllFourTargets C4 terminó NOT_PASS67,522s porque el directorio propio VERIFIER_OUT no existía al guardar los resultados de los cuatro casos. Manager comprobó que `verifierSave` precede los asserts de conciliación/pagos: no pueden darse por pasados esos asserts. Se preservan log/perfil fallido y se corrige la preparación del directorio para un rerun acotado íntegro, sin cambiar producto ni expectativas. No se atribuye este error de ejecución a V-F03 ni se incluye su perfil en cobertura PASS.

Rerun `c4-four-targets-attempt2.log` comprobado por manager: PASS62,528s, incluidos los cuatro objetivos heredados y sus asserts financieros íntegros. Los casos2250/2500 pertenecen exclusivamente a regresiones históricas; las configuraciones activas siguen2300/3000. `c4-lifecycle.log` PASS27,411s acredita pase, funding y crédito físico de caja del fixture original; no es un cobro de T1. Freeze y verificación independiente exacta aún pendientes.

### Compra tras pausa: RED/GREEN público independiente

`verifier/paused-demand-red-green-receipt.json`: el mismo fixture y asserts sobre B producen RED exit1,0,700s, dos materializaciones/una cuenta/caja4880; C4 working tree produce GREEN exit0,0,790s, tres materializaciones/dos cuentas/caja4760. Dos operaciones reales del fixture ganan435 cada una: el primer TP conserva la cuenta, el segundo llega a870 y la pausa; la nueva demanda10:21NY compra una sola sucesora después de finalización física. No hay mutación directa de OwnerState/risk ni estrategia diagnóstica productiva nueva. Asset permanente SHA256 `cc1ceb5b02c522d4f3136c3f74aeebf1d22f1bb112f1c6b65e7c803b256b7d82`, promoción por integrador antes del freeze y gate exacto pendientes.

En B físico, el primer cruce histórico de esta pausa es21oct14:32Z: cuenta pausada DAILY_GOAL desde14:27, caja4880, una plaza EVAL, ninguna cuenta elegible y owner TERMINAL sin exposición/claims/admisión pendiente. La fuente B comprueba caja/horizonte antes del veto por pausa y cupo/horario después. Las reservas Provider exactas de esa barra histórica no quedaron retenidas: no se certifican a partir del owner ni se adjudican41 fills contrafactuales. La prueba pública y los negativos de reserva acreditan el comportamiento requerido; el censo histórico conserva ese límite de observación.

### Baseline observacional completo y drenado

`implementer/evidence/baseline-observation-progress.json` registra5/5 COMPLETE, exit0 cada campaña, último fin2026-10-13T17:23:18Z. Manager comprobó ausencia física del controlador2772595 y último wrapper2799793/hijo2799794. K04 equivalencia independiente PASS:146 registros legacy y economía íntegra,755 cruces=31 MM+719 owner sin exposición+3 expiries+2 ocupados, sin causa UNKNOWN. K05 queda pendiente de cotejo independiente, no de ejecución. Los cinco replays conservan la fuente B y usan el overlay observacional identificado; sus resultados no sustituyen ni borran los originales.

La causa histórica de compra pausada está materializada en `verifier/paused-purchase-first-historical-cause.json`, con los límites de reservas ya indicados. La regresión pública permanece separada de la atribución del cruce físico.

Cotejo K05 posterior PASS:214 registros legacy íntegros, cero diferencias. `verifier/baseline-observed-census-full.json` cierra los cinco perfiles; cada fila suma755 oportunidades, sin desconocidos ni doble conteo:

| Perfil B | Evaluados MM | Owner abierto sin exposición | Gate con pausa vencida | Pausa diaria vigente de cuenta | Ocupado físico/admisión |
|---|---:|---:|---:|---:|---:|
| K01 |31|721|3|0|0|
| K02 |36|670|3|41|5|
| K03 |36|711|3|0|5|
| K04 |31|719|3|0|2|
| K05 |35|711|3|0|6|

La tabla describe disposiciones reales, no fills contrafactuales. Las41 pausas son legítimas para esa cuenta y la compra global se adjudica por separado. `verifier/first-admit-reject-before-observed.json` conserva el primer rechazo y admisión real de cada perfil con snapshot MM; K01 no tiene admisión. Prueba de equivalencia de pares históricos enlaza estos cinco replays2300 con ambos retiros antiguos; las diez campañas corregidas sí requieren ejecuciones propias.

`verifier/baseline-observed-causes-total.json` concilia los cinco universos:3.775 oportunidades =169 MM+3.532 owner abierto flat+15 fronteras de pausa vencida+41 pausas vigentes+18 ocupados. Dentro de los169 MM hay137 rechazos, enlazados a274 en diez configuraciones históricas. No se suman latch y lifecycle como dos pérdidas del mismo cruce ni se confunden169 materializaciones con155 drafts NewCycle.

Continuidad operativa: después de vet se observó ausencia de procesos propios y ningún inicio físico de CLI durante varios avisos. Manager interrumpió y reanudó el turno del mismo integrador desde su estado persistido, sin crear otro especialista ni modificar fuente. Siguiente acción ordenada: CLI, freeze/build, gate independiente exacto. No se registra ese estancamiento de coordinación como fallo de producto ni como una prueba ejecutada.

El intento de reanudación tampoco inició CLI ni produjo un error material comunicado. Se suspendió el worker anterior y se relevó por `/root/entry_repair_integrator_c4`, TOP con contexto nuevo y el mismo modelo solicitado Sol6.1; servido UNKNOWN. Sólo el relevo posee Go/código/integración, el verificador conserva independencia. Se preservan checkout, delta, pruebas, recibos y límites; no se reinicia la investigación ni se crea otro manager. El relevo debe ejecutar CLI y completar freeze/gate/campañas desde ese estado.

### C4: CLI y fuente congelada

Relevo ejecutó físicamente CLI aislado; `implementer/evidence/c4-cli-singleton.log` PASS122,157s, incluidos artifact y manifest, con exit0 persistido. Vet se repitió de forma focalizada porque el exit heredado no estaba acreditado: `c4-vet-verified.exit` contiene0. No se repitió SDK ni se alteraron expectativas. Manager comprobó commit C4 `88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49` y árbol limpio. Build única, procedencia de cobertura y gate independiente exacto en preparación; todavía no se han admitido campañas C4.

Controller nuevo requiere gate independiente con SHA source/bin coincidentes antes de admitir trabajo, conserva los diez pares y tres slots totales con afinidad0–5. Manager revisó los guards globales y pidió reservar también derivados del verificador, además de distinguir una reserva transitoria por concurrencia de un forecast total imposible, sin aumentar ningún techo. No se considera completada una configuración por falta de recursos ni se elimina evidencia anterior.

### C4: gate independiente exacto PASS

Fuente `88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49`, binario `implementer/bin/echo-backtest-88ed70d1`, SHA256 `c8849bb6e5523e8625ead8282f0d97f98d8b02e14d72838e3c35de207c6bcd57`. Manager comprobó hash físico, metadata Go1.27.1/vcs.revision correcto/modified=false y árbol limpio. Manifest `implementer/evidence/c4-freeze-manifest.json`; `verifier/exact-gate-88ed70d1.json` INDEPENDENT_PASS habilita campañas, no aceptación global.

Regresiones propias exactas PASS7,081s; seis tapes CLI públicos PASS (LONG/SHORT/outside/silent/warmup23/resume-boundary); paridad Core tipada PASS0,018s con contexto/views del fixture y admisión manual explícita, sin publicador LIVE/broker certificado. Se cotejaron resultados físicos de cuatro pagos y los gates author lifecycle/CLI/vet/build. Cobertura final:346/350=98,8571% en bloques afectados;267/271=98,5240% en inicios de sentencias AST modificadas;15 archivos productivos, cero sin perfil o sin mapeo. Cada denominador conserva su definición, no es una cifra de cobertura global ni de todas las líneas nuevas. Oracle reutilizado por bytes SDK idénticos, sin inventar un recenso C4; las diez campañas compararán sus observaciones por identidad.

Antes de admitir campañas, el forecast detectó un margen insuficiente: durable postgate703.379.459 bytes; al incluir overhead real de resultados/planes además de trazas y20MB derivados, la previsión supera768MiB en aproximadamente7,8MB. No se lanzó una campaña bajo esa previsión. Se está midiendo retención gzip sin pérdida para **nuevos derivados**, con lectores/manifests resolubles; no se toca evidencia histórica, fuente, límites ni parámetros. El verificador además detectó que20MB de derivados sin compresión era insuficiente y lo rectificó antes de ejecutar. Comparación C4 aún0/10; reserva de disco8GiB y techo por lote256MiB preservados.

Previsión corregida y medida: `verifier/C4-derived-gzip-budget-forecast.json` conserva todos los campos y cubre operaciones, oportunidades, autoridad monetaria, sizing, primeras admisiones/rechazos, cierres, cuenta/día y causalidad. Diez veces el máximo por tipo medido en referencias C3 gzip suma3.814.110 bytes; con50% de crecimiento y1MB de metadata da6.721.165. Se autoriza reserva10.000.000 bytes, incorporada en gates/controller, con medición por campaña y lectores `.json.gz`; ningún techo se amplía. Los doce planes C4 nuevos se compactaron conservando igualdad JSON exacta, ahorrando677.884 bytes, con hashes efectivos y paridad renovados (`c4-ten-plan-compaction.json`). El forecast de campañas usa el directorio completo máximo C3, no sólo su traza. Se habilita admisión cuando la medida global posterior a estas escrituras cumple los guards.

### Diez campañas C4: inicio físico con límites acreditados

Controller `implementer/run_final_c4.py` iniciado, tool sesión86805; manager comprobó `88ed70d1-final-progress.json`: K01/K02/K03 r2300 RUNNING, wrappers2816546/2816559/2816573, tres slots y cero reservas Go/Bobs,0 completas/0 fallidas. `c4-resource-forecast-before-ten.json`: durable702.727.436 bytes +89.756.060 de diez campañas +10.000.000 derivados =802.483.496 frente805.306.368, margen2.822.872; scratch propio0, disco libre13,924GB. La reserva transitoria puede reducir concurrencia mientras se drenan jobs; no cambia los techos ni transforma un pendiente en éxito.

`c4-ten-plan-normative-parity.json` acredita diez planes con mercado, corpus, perfil, ventanas y parámetros idénticos a B; únicamente campaign_id/model_identity/sourceSHA/binSHA excluidos del cotejo. No se deduplican2300/3000. Binario, inputs y fuente permanecen quietos. Los resultados se verificarán por identidad de cruce, autoridad monetaria completa y vigente, órdenes/fills/cierre físico, ledger y métricas; el gate corto no anticipa10/10.

Chequeo temprano `verifier/C4-prefix-first-economics-readback.json`, **PREFIX_ONLY_NOT_CAMPAIGN_PASS**: primeras cuatro materializaciones K01/K02/K03 con margen presente y Fresh; primer snapshot14oct14:33Z conserva1100 en los tres. Primer ciclo con fills queda flat y se observa una nueva materialización posterior: K01 a18:34Z, K02 a14:48Z, K03 a16:25Z. K03 puede rechazar correctamente ese nuevo intento; rearme no implica admisión obligatoria. Sólo se leen filas completas, sin afirmar conciliación final ni extrapolar el censo. Verificador cotejó también los diez planes físicos en `C4-ten-plan-independent-readback.json`.

### V-F03: primera entrada indebida evitada en mercado físico

`verifier/C4-V-F03-first-invalid-entry-prefix.json`: K02,31oct2025 a10NY/14Z, misma identidad de cruce y mismo balance48885,32/PnL diario antes de entrar en C3 y C4. Piso diario47785,32, piso EOD48875,16, margen efectivo10,16. C3 omite ese campo y admiteQ1 con pérdida geométrica modelada369,98; C4 entrega margen10,16 en la misma revisión DAY20534, recorta R/T proporcionalmente a10,16 y rechazaQ0 con TG_SIZE_BELOW_MINIMUM. Cero comandos de entrada, cero fills y owner terminal flat. Primera divergencia económica cerrada con fuente/binario final; estado **PREFIX_ONLY**, sin extrapolar igualdad de trayectorias posteriores ni aceptación de la campaña completa.

## Fuentes

- Mandato del Owner `ECHO FUTURES — GOD LOCAL: DIAGNÓSTICO Y CORRECCIÓN DE ENTRADAS TRADESGERARD`, PROMPT_VERSION1, 2026-10-13.
- [[TRADESGERARD-CONTROL]], [[TRADESGERARD-B-PLAN]], [[TRADESGERARD-B-T0]], [[TRADESGERARD-B-T1]], [[TRADESGERARD-B-T1L]], [[TRADESGERARD-B-RESULTADO]].
- `xKoRx/echo:AGENTS.md` y `v3/backtester/README.md`; `git status --short`, `git rev-parse HEAD`, `git branch --show-current`, `sha256sum` y `go version -m` ejecutados sobre las rutas anteriores.
