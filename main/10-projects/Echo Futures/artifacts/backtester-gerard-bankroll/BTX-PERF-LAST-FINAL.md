---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
  - "[[BTX-PERF-DESIGN]]"
  - "[[BTX-PERF-ADVERSARIAL]]"
  - "[[BTX-PERF-FINAL]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-10"
updated: "2026-10-10"
---

# BTX-PERF-LAST-FINAL

## Propósito

**NOT_READY.** Se reparó el backtester y se obtuvieron cuatro resultados financieros acotados, con dinero, actividad diaria y ciclos S2 conciliados independientemente en la build final. La entrega no cumple la aceptación integral: el catálogo de trece contratos no permite una trayectoria continua, no se acreditó ningún rollover real, las metas de rendimiento fallan y la cobertura del desarrollo alcanza 94,2016 % frente a 95 %. También persisten límites explícitos de telemetría para expiraciones y duración continua sin readiness.

El rechazo correcto por datos no se presenta como ejecución multianual. BASIC termina los casos NQZ5/NQU6 con 70.307,92/78.200,92 USD; CAMPAIGN conserva cajas de 4.400/4.880 USD, separadas de sus saldos nominales. Son resultados procesados útiles para evaluar S2, con pérdidas visibles y alcance delimitado.

`FINAL_OWNER_ACCEPTANCE=NOT_GRANTED`. `PHYSICAL_RUNTIME_READINESS` permanece separado: esta entrega no certifica ni habilita ejecución LIVE, órdenes reales, cuentas, broker, ETCD/PROD o permisos. No autoriza otro shot automático.

## Contenido

Este dictamen contiene identidad verificable, cambios, cobertura histórica, actividad y economía, rendimiento, matriz de obligaciones y receta reproducible. El manual único del producto sigue siendo `v3/backtester/README.md`; los inputs y resultados íntegros permanecen en el paquete privado fuera del vault.

### Autoridad y responsabilidades

El corte Owner fue fijo: `2026-10-10T13:09:16Z → 2026-10-11T13:09:16Z`, correspondiente a 10:09:16 America/Santiago. El primer reloj observado fue `2026-10-10T13:30:13Z`, con 23 h 39 min 03 s restantes. No se reinició el plazo por worker, contexto o medición. Cierre técnico, publicación del paquete y cierre de TOPs observados a `2026-10-11T02:45:10Z`, con 10 h 24 min 06 s restantes; después sólo se materializó este cierre documental.

GOD coordinó, adjudicó evidencia y escribió documentación; no escribió producto, tests, parsers, instrumentación ni fixtures, no compiló ni ejecutó backtests. TOP INTEGRADOR fue el único propietario de la rama integrada; DATA produjo catálogo, análisis S04 y oráculo externo; PERFORMANCE produjo optimizaciones y mediciones asignadas; VERIFICADOR no tuvo autoría de producto y comunicó defectos durante su encargo. Se respetaron propietarios disjuntos y exclusividad para los procesos financieros medidos.

Los cuatro TOPs se despacharon con contexto fresco y selector explícito `gpt-6.1-sol`. Modelo servido: `UNKNOWN`, porque el harness no expuso ese recibo. GOD tuvo rol solicitado GPT-6 Astra, también sin comprobante independiente de modelo servido. No se inventan tokens ni cuota. Los TOPs GLM-5.3-Flash despachados directamente por Owner no se consideran un incumplimiento.

### Identidad final

| Elemento | Identidad |
|---|---|
| Base autorizada | `ed31156fe251a053241044f7659c078424667348` |
| Rama y remoto real | `codex/btx-perf-last`, `github.com/xKoRx/echo` |
| Commit limpio | [`873f5f1c7df25086271af1de1896095f1cade2a9`](https://github.com/xKoRx/echo/commit/873f5f1c7df25086271af1de1896095f1cade2a9) |
| Binario normal SHA256 | `0320b80e78fbf12821eda4004c68c96175f770dedaac747dc306604e9280d83b`, 15.375.418 bytes |
| Construcción | Go 1.27.1 linux/amd64, build normal, CGO 1, GOAMD64 v1, sin cover/race/overlay/trimpath ni ldflags especiales; `vcs.modified=false` |
| Core final privado | `btx-perf-last-core-873f5f1c-final.tar.gz`, 140.991.710 bytes, SHA256 `0ab9e4a762f3791618b384a0f0cf499d7c595fddc0bfc603eb4f36149defd1b9` |
| Resultados financieros | `btx-perf-last-financial-873f5f1c.tar.gz`, 1.174.828.373 bytes, SHA256 `2cb3422d86da2bba124f926c4aef6e54ed65f8fc6fa36523a50f5ff723cc92f2` |
| Evidencia final | `btx-perf-last-evidence-873f5f1c-final.tar.gz`, 12.022.316 bytes, SHA256 `97856b69c52c462c6525704fe0544f103ac1f01275a99e04d14011db326d88cf` |
| Manifiesto de la unión | `SHA256SUMS`, 3.494 archivos, SHA256 `42dc7d1946d6f5dda68481dae68a2938918c892ad2bc87b2a1c37300d01e5a76`; sin autorreferencia |
| Catálogo común all13 | SHA256 `93ea652be950a4372cc5017d077eaef77e6fe68197706a70494d98fc2d9c3184` |
| Ejecución | `OHLC_CAUSAL_PATH_V2`, `CONFIGURED`, S2 y GerardMM por fábrica pública; fee 2,49 USD por unidad con fill, slippage 1 tick, offsets bid/ask 1 tick, SL_FIRST |

El remoto GitHub de rama y tag fue contrastado por GOD y coincide con el commit completo. La prerelease privada se publicó a `2026-10-11T02:38:54Z`, sin latest ni force. El preflight independiente de core y financial verificó 3.003/99 checksums, 2.975 archivos tracked iguales al checkout 873 limpio, binario y cuatro aliases exactos. Después, una descarga nueva de los tres assets finales y extracción limpia pasó literalmente `sha256sum -c SHA256SUMS`: **3.494/3.494 correctos**. También se comprobaron los cuatro payloads W1, dependencias de herramientas, rutas del fixture held, certificados y notas. No fue necesaria otra corrida financiera.

Recibo externo independiente: `FINAL-873-INDEPENDENT-REMOTE-READBACK.json`, emitido `2026-10-11T02:43:13.972905Z`, SHA256 `4fad106de0266e1d796c903b906aead1a1f320c5da8041b86d719c0eb0b99c61`. Su PASS acredita descarga y ensamblado de los tres archivos; el dictamen técnico sigue NOT_READY. El recibo resuelve los campos pendientes de publicación que los certificados tenían al emitirse, sin modificar sus bytes ni los assets verificados.

El primer freeze 486 se retiró al confirmar un defecto de entrega CLI: una corrida CAMPAIGN COMPLETE podía devolver exit0 después de fallar stdout. La corrección 873 propaga el error de `fmt.Println`; conserva los bytes de éxito y el artefacto financiero. Los negativos independientes sobre el binario normal 873 devuelven exit2/ENOSPC. Se conservaron los resultados 486 como históricos y se ejecutaron originales nuevos 873; ninguna firma 486 se transfiere al delta.

### Reparaciones entregadas

- Pool acotado con progreso de 3 y 13 streams largos, workers 1/2, orden de IDs inverso al tiempo; cierre drenado, cancelación bajo backpressure y primera causa frente a EOF.
- Selección inicial conforme al horizonte, preparación causal, overrides y ReadPlan para contratos activos/retirados. El último minuto admitido se drena antes de Release; posición, orden o claim mantienen sus precios y obligaciones propios. Planes vacíos, bindings ausentes y prefijos/sufijos incompletos ya no pueden producir COMPLETE silencioso.
- Día contable CAMPAIGN correctamente contenido respecto de Chicago 17:00 y reset después de reemplazo intradía. Esta reparación cambia legítimamente la economía respecto de S04.
- Reporte diario público con poblaciones y causas `ENTRY_GUARD`, identidad del contexto técnico correcto y observaciones de posición por valor. Se mantienen UNKNOWN donde la evidencia no alcanza.
- Getters y evidencia aislados, enteros opacos precisos, ownership del recorder explícito, errores de writer/Close y fuente pre-drive correctamente propagados, sin footer aceptado falso ni impedir reintentos legítimos anteriores a escritura.
- Consultas del ledger que evitan snapshots descartados y copias equivalentes mediante `maps.Clone`. No se alteraron señales, SL/TP/BB/SMA/sizing/adds/fees ni callbacks para ganar rendimiento.
- Requests relativos, aliases de resultados íntegros y recetas públicas reproducibles. No se añadió otra Strategy para forzar entradas diarias.

### Horizonte y cobertura causal

La extensión física es `2023-10-01T22:00Z → 2026-10-06T03:50Z`; no equivale a continuidad. Los trece hashes y los derivados calendar-filtered v1 se contrastaron con recibos y fuentes originales autorizadas, sin regenerarlos. Ambos requests all13 piden warmup desde `2023-10-01T22:00:00Z`, trading desde `2023-10-12T10:00:00Z` y fin exclusivo `2026-10-06T03:50:00Z`.

La política prospectiva es `FUNCTIONAL_ASSUMPTION_V1`: primera sesión efectiva del mes de expiración saliente, con `BTG_FUNCTIONAL_NQ_WEEKLY_V1` v1 y sus autoridades declaradas. No constituye certificación de un calendario oficial del exchange. Los doce entrantes tienen cero prefijo antes de selección, frente al mínimo técnico de 51 H4/11.700 minutos de ese calendario. En NQZ3→NQH4, selección `2023-12-03T23:00Z`, preparación requerida a más tardar `2023-11-21T11:00Z`, primera barra entrante termina `2023-12-07T03:01Z`. Los originales disponibles comienzan igual; no recuperan el prefijo faltante.

Los intentos finales 873 all13 terminaron exit2, sin censura: BASIC 46,083710 s y CAMPAIGN 44,721070 s. Ambos rechazaron `SOURCE_COVERAGE_INCOMPLETE`, contrato `NQ:NQZ3`, primer minuto requerido ausente `2023-10-10T00:16:00Z`, durante warmup. No existe estado financiero ni resultado COMPLETE de esos intentos. Sus tiempos no aprueban los objetivos multianuales 3600/3900 s.

**Rollovers reales acreditados: 0.** La transición pública con tres contratos y dos cruces sintéticos demuestra funcionamiento de identidades y obligaciones, con alcance distinto del corpus real. No se ajustaron rollovers mirando PnL, fabricaron barras, rellenaron gaps ni sumaron trece economías independientes.

| Caso procesado | Warmup desde | Trading | Streams financieros |
|---|---|---|---|
| NQZ5 BASIC/CAMPAIGN | 2025-10-13T17:52Z | 2025-10-27T17:52Z → 2025-11-27T18:00Z | NQZ5; NQH6 futuro no requerido, consumo 0 |
| NQU6 BASIC/CAMPAIGN | 2026-07-05T22:01Z | 2026-07-19T22:01Z → 2026-09-07T17:00Z | NQU6 |

NQZ5 consume 45.488 minutos físicos: 13.800 de warmup y 31.688 de trading. NQU6 consume 63.239 frente a 94.568 filas inventariadas. Inventario, consumo de fuente, inputs raíz, records de evidencia y días contables tienen denominadores distintos. El paquete conserva matriz por transición, catálogo, ReadPlan, gaps y recibos de fuente.

El ancla NQU6 conserva la fuente física SHA256 `d4cbbdcdbe7bcb2932f1fbfb1418e8f12a52ef3305df29d5619a19cef6112be3`. Su lineage parte del request Owner `66dcc481372e047c893fc54bc65a88dd7a77d20ad97d9f4720b74697792eefef`; la versión flat portable `9594865ef35189c49230c79cfe4670c41666168410e5a93167d3f5d9c15a7ddd` sólo cambia el localizador del descriptor. La materialización como catálogo singleton conserva configuración económica, estado inicial, planes económicos y modelo, pero sí materializa catálogo/schedule/ReadPlan: no se afirma igualdad literal de todos los campos flat→catálogo. CAMPAIGN tiene adaptación de modalidad explícita. Ningún ancla se sustituyó por un segmento con otro estado inicial.

| Request final relativo | SHA256 |
|---|---|
|`requests/basic-all13.json`|`2b1eba62672c64982c995ec39fd52b70884caf3fe5faefea7620bb92b31cf6bd`|
|`requests/campaign-all13.json`|`140a9f7ff7f3921f1f4ce8f9aa22b5046b9406176bea6eeb3db007e1a197bfb7`|
|`requests/basic-NQZ5.json`|`b4a4095d344ea7418abe60345507ce7adbf7e9a7884cf19f16b4d6014ea3875d`|
|`requests/campaign-NQZ5.json`|`9575ef9f48a5b6c4c9306fd8368058d48f03fcd5768e3063f83aacb3b8f063ca`|
|`requests/basic-NQU6.json`|`b0a2da75b1640353bb6d8582b08ad1f14e2e25345998f235bfb075c1177c160c`|
|`requests/campaign-NQU6.json`|`cf9bd0c7569882bcab1feae40413d8f21bd883ccb8cc50cf6adedff4990ae773`|

Un request CAMPAIGN all13 preliminar del freeze histórico 486 omitió el bloque campaign y fue rechazado por configuración antes de validar datos. Se preservó el intento y sólo se añadió la política ya autorizada; el verificador confirmó que el resto no cambió. La corrida final 873 usa exclusivamente el request corregido de la tabla. No se cuenta aquel rechazo como prueba de cobertura del catálogo.

### Economía conciliada en873

El verificador recorrió una vez cada artefacto final completo y concilió FIFO exacto, fees contractuales, revisiones comprometidas y controlador. En CAMPAIGN gross/fees/net agregan trading de todas las generaciones; nominal corresponde sólo a la última cuenta y caja al controlador. Fills y unidades incluyen ambos sentidos. Compras no son trades.

| Caso | Operaciones creadas/con fills | Fills/unidades | Gross USD | Fees USD | Net USD | Último nominal USD | Caja/compras/burns |
|---|---:|---:|---:|---:|---:|---:|---|
| BASIC NQZ5 |146/39|170/1792|−25.230,00|4.462,08|−29.692,08|70.307,92|No aplica|
| CAMPAIGN NQZ5 |146/15|70/372|−9.650,00|926,28|−10.576,28|98.000,12|4.400/5/4|
| BASIC NQU6 |222/65|258/2092|−16.590,00|5.209,08|−21.799,08|78.200,92|No aplica|
| CAMPAIGN NQU6 |222/1|6/18|−1.935,00|44,82|−1.979,82|98.020,18|4.880/1/0|

| Cuenta CAMPAIGN NQZ5 | Gross USD | Fees USD | Net USD | Nominal USD | Fills | Estado |
|---|---:|---:|---:|---:|---:|---|
|1|−1.775,00|224,10|−1.999,10|98.000,90|10|BURNED_RISK_BREACH|
|2|−1.710,00|428,28|−2.138,28|97.861,72|32|BURNED_RISK_BREACH|
|3|−2.170,00|104,58|−2.274,58|97.725,42|6|BURNED_RISK_BREACH|
|4|−2.025,00|139,44|−2.164,44|97.835,56|10|BURNED_RISK_BREACH|
|5|−1.970,00|29,88|−1.999,88|98.000,12|12|ACTIVE_AT_HORIZON|

Todas esas cuentas son EVALUATION; las operaciones creadas por generación son 88/19/1/2/36. El burn se comprueba por evento nativo de riesgo, no sólo por el saldo final. Caja NQZ5 = 5.000 − 5×120 = 4.400 USD; NQU6 = 5.000 − 120 = 4.880 USD, con una cuenta activa. No se suman saldos nominales como caja.

Los cuatro casos tienen cero PASS, cero solicitudes/admisiones/aplicaciones FUNDED, cero solicitudes/cobros y cero inventario físico residual. Se comprobó el censo completo de records y los ledgers de controles, cuentas y controlador. Estos ceros no demuestran el lifecycle de cobros; ese requisito se prueba separadamente con el fixture de cuarto cobro.

### Actividad diaria y S2

**¿Cuántos días pudo entrar, cuántos entró y qué ocurrió en los demás?** Disponibilidad técnica y admisión económica son poblaciones distintas: S2 lista no garantiza capacidad de riesgo de la cuenta.

| Caso | Días técnicos elegibles | Días OPEN | Días fill inicial | OPEN/elegibles | Entrada/elegibles | Otros días elegibles sin entrada |
|---|---:|---:|---:|---:|---:|---|
|BASIC NQZ5|24|22|22|91,67 %|91,67 %|2 sin setup|
|CAMPAIGN NQZ5|24|22|6|91,67 %|25,00 %|16 sin capacidad para un contrato; 2 sin setup|
|BASIC NQU6|36|35|35|97,22 %|97,22 %|1 sin setup|
|CAMPAIGN NQU6|36|35|1|97,22 %|2,78 %|34 sin capacidad para un contrato; 1 sin setup|

NQZ5 comprende 46 ventanas comunes: 10 de warmup, 12 cerradas y 24 elegibles; NQU6 comprende 64: 10 de warmup, 18 cerradas y 36 elegibles. Los CSV diarios y por cuenta conservan causa principal, coordenada causal, primera/última operación, ENTRY y exposición. Las causas financieras 873 provienen de declaraciones nativas `PROVIDER_HEADROOM_BELOW_ONE_CONTRACT`, sin reasignar UNKNOWN silenciosamente. Los días comunes no se duplican al reemplazar cuenta.

Operaciones se cuentan por cohorte de creación; fills por ejecución. El escáner873 retuvo la primera coordenada `OPERATION_SNAPSHOT` de cada operación y emisiones de órdenes: los cuatro casos observan cero órdenes cuya emisión cruce de día respecto de su cohorte. No se inventó un evento CREATED. Los CSV por cuenta declaran `day_start_balance` y revisiones observadas.

Las 46 filas futuras de NQH6 se clasifican `NOT_REQUIRED_BY_MINIMUM_PLAN`/`NOT_SELECTED`, con consumo y elegibilidad 0. El bruto NOT_READY se preserva; no se confunde con bloqueo financiero. Warmup calendario es la intersección de cada ventana con [WarmupStart,TradeStart), separada de minutos consumidos. En un contrato no requerido, warmup global no implica lectura de su fuente.

El diagnóstico no cubre toda la exigencia A: duración continua sin readiness queda `UNKNOWN_COUNTS_ONLY_NO_DURATION_ACCUMULATOR` cuando sólo existen evaluaciones; expiraciones de señales quedan `UNKNOWN_OPERATION_TELEMETRY_NOT_RUN_EVIDENCE`. La telemetría Operation de expiración no se conserva en evidencia de run. Igualdad OPEN/operaciones no prueba biyección ni cero expiraciones; Provider tiene población separada. No se fabrican contadores por resta.

El oráculo S2 independiente usa Fraction exacta, mismas barras causales y convenciones: 5m BAR_CLOSE, H4/SMA50, BB20/2 poblacional, pullback y ciclo ARMED/OPEN. NQZ5 concilia 292 señales = 146 OPEN + 146 CLOSE_ALL y 1.022 campos de provenance; NQU6 concilia 444 = 222 + 222 y 1.554 campos. Barras 5m/H4 y callbacks: 9.097/197/9.359 en NQZ5; 12.647/273/13.009 en NQU6. Son poblaciones diferentes.

Un rechazo financiero o un cierre físico no rearma por sí solo S2. BASIC NQZ5 conserva 107 contextos de operación sin fills hasta CLOSE_ALL y 388 callbacks TECHNICAL_CYCLE_OPEN mientras el inventario está plano; no son 388 ciclos. Se contrastaron los cuatro informes de ciclos sin forzar una entrada diaria ni cambiar reglas de trading.

Los checkpoints del parser son exclusivamente forenses: enlazan físicamente artefacto/request/source y herramienta antes de deserializar; no reanudan una trayectoria financiera. Se preservan 4 positivos y 3 negativos físicos, separados de los negativos de metadata. El escáner prospectivo 873 tiene SHA256 `bd61020a6df9cb086b1f510b1d7fb40f4d1165f784bea9b747872fbaf87ea6b9`; el oráculo conserva `52747ea627c1a657d1363482a12d1df55b7ed095ecc11e496b2b7ee98e03ef38`. Se corrigió únicamente un párrafo heredado del renderer que todavía decía UNKNOWN para órdenes cruzadas de BASIC NQZ5, aunque el nuevo escáner ya había retenido cero. Los ocho CSV y el resumen JSON permanecen byte a byte idénticos; no hubo nueva lectura ni cambio matemático. Renderer final SHA256 `1f7c83ca168907f068c84c4e9098e03db31502409f5567c5e5c043f529ff6b1c`.

### Identidades de resultados finales

| Caso | RunID completo | Artifact SHA256 | Records/inputs raíz |
|---|---|---|---|
|BASIC NQZ5|`bt-b8a466fa12383e7e336937c73eaca888063d43d6a048e79b3adcbaed1d6cfdb5`|`e769c317aa92fb3ab2a9ed3b3fe34624c30d02ec8d10baa3e2bdb1f1e4f82659`|3.214.512/3.949.131|
|CAMPAIGN NQZ5|`bt-c-f5592f9ae4479b2afa928fa462f94cb7c66db038d23311acc6bb764f44655e39`|`0e0a9eb6040ee4e6387d1cb21e19f0a187026a026d85d29438442568a73b0019`|3.124.951/3.949.525|
|BASIC NQU6|`bt-3e5fb2fce9d7525229885486901c08059d85f16342f4ca988caa5bdd435174bf`|`9a49b3c381ebde87d7ce0a453e6baeeb2148fe62d4082230029227518b194723`|5.172.230/6.464.027|
|CAMPAIGN NQU6|`bt-c-77f5d68c70995c3a375c379329291b3ec4bb6b923cb5c9540f853529d123c711`|`5045104aa0a3e37c9a3848e345891e350e12e1bb99e46fbdf4ab6b7286e3c257`|5.126.269/6.463.361|

Los replays oficiales usan el binario normal 0320 descargado del core final, source 873 limpio y las identidades anteriores. Se ejecutan serialmente con GOMAXPROCS=4, sin cargas técnicas propias simultáneas. Igualdad oficial compara los records originales completos con identidad exacta; no normaliza IDs. Wall de replay y RSS tienen recibos separados del original. El wall de replay incluye su comparación oficial; las subfases internas sin instrumentación separada quedan UNKNOWN, no se estiman restando tiempos de otra corrida.

| Replay | Ruta pública | Records | Wall s | Peak RSS bytes | Resultado |
|---|---|---:|---:|---:|---|
|BASIC NQZ5|`--result`|3.214.512|1.065,948701|110.731.264|IDENTICAL, exit0, sin censura|
|CAMPAIGN NQZ5|`--result`|3.124.951|979,714989|112.476.160|IDENTICAL, exit0, sin censura|
|BASIC NQU6|`--result`|5.172.230|1.706,104888|134.619.136|IDENTICAL, exit0, sin censura|
|CAMPAIGN NQU6|`--experiment`|5.126.269|1.511,706179|127.746.048|IDENTICAL, exit0, sin censura|

El primer chequeo auxiliar terminal esperaba una key `status`; la respuesta pública usa `verdict`/`identical`. Se conserva el KeyError del harness y su corrección de lectura, sin cambio de producto ni oráculo. El resultado público de BASIC NQZ5 es efectivamente IDENTICAL.

El caso held positivo de la misma build normal terminó COMPLETE en 4,484770 s; ambas rutas oficiales pasaron IDENTICAL sobre 18.088 records, `--result` en 10,053654 s y `--experiment` en 9,811655 s. Su manifiesto es `campaign-manifest.json`. Se conservó un intento anterior rechazado antes del drive por usar `experiment` con esquema campaign: exit2 en 0,011412 s, sin estado financiero. La corrección fue del comando del harness, sin cambiar inputs, producto ni oráculo.

### Rendimiento observado

Un solo proceso financiero medido a la vez; builds, tests, coverage, replays, análisis y empaquetado propios pausados durante cada lease. GOMAXPROCS=4, hashes y readwarm previos al proceso. Host Xeon E5-2697 v4 a 2,30 GHz, afinidad 0–23, MemTotal 96.506.996 KiB; cuota/cpuset leaf UNKNOWN, ancestor cpu.max=max100000. Se registró carga ajena; el host no era dedicado. Los PIDs del wrapper y del hijo se identifican por separado; no se ajusta wall por cores ni CPU ajena.

| Caso873 | Wall proceso s | Peak RSS bytes | Resultado | Meta |
|---|---:|---:|---|---|
|BASIC NQZ5|797,508908|109.432.832|COMPLETE|RSS≤512 MiB PASS; no sustituye multianual|
|CAMPAIGN NQZ5|548,694028|108.924.928|COMPLETE|RSS PASS; no sustituye multianual|
|BASIC NQU6|1.217,135029|131.055.616|COMPLETE|FAIL 180 s; RSS PASS|
|CAMPAIGN NQU6|876,057182|128.057.344|COMPLETE|FAIL 220 s; RSS PASS|

Los cruces de 180/220 s se registraron en los procesos originales; se continuaron una sola vez para obtener evidencia útil, sin reiniciar. Caps de seguridad no son targets. Todos terminaron sin censura y con Close correcto.

| Caso | Preparación s | Run s | Outputs s | Finish s | Source Close s | Total externo s |
|---|---:|---:|---:|---:|---:|---:|
|BASIC NQZ5|5,462546|667,105483|124,883660|0,013829|0,001896|797,707712|
|CAMPAIGN NQZ5|5,526953|464,166238|78,928618|0,011757|0,001863|548,900284|
|BASIC NQU6|3,952227|1.019,984471|193,137898|0,017513|0,002007|1.217,323206|
|CAMPAIGN NQU6|4,027091|746,173537|125,806480|0,019717|0,002168|876,236932|

El total externo y las fases tienen fronteras distintas y conservan recibos propios; no se suman como coeficiente de proyección. La reconciliación del controlador consume 0,000012069/0,000030856 s en CZ/CU. La extracción, comparación y replay independientes se informan aparte.

La comparación funcional W1 conserva baseline `e00d3d136daa8590c3754d4a29ab99474b7a1df7`, bin `9ef9ff871af75971dfd7eb71140cb02e147f2f8763c1357133888a359a5ac35a`. No usa d609 como oráculo de fronteras monetarias rotas. Workload, criterio e inputs se sellaron antes del cambio de performance.

| W1 | Baseline s | Candidato873 s | Speedup observado | Meta1,5× |
|---|---:|---:|---:|---|
|BASIC|366,474253|246,068060|1,4893206913×|FAIL|
|CAMPAIGN|530,577700|378,236126|1,4027684390×|FAIL|

La paridad completa independiente W1 pasó: BASIC 1.269.950 records/44.183 referencias/1 generación/12 negativos; CAMPAIGN 2.145.868/5.509/2 generaciones y reemplazo real/13 negativos. Sólo build.commit es variable declarada, con biyección tipada por namespace/generación/causa. Se conservan framing, secuencia de inputs, preimágenes provider/config/model/logical, campos opacos y MMActivity. Los negativos incluyen precio, cantidad, tiempo, campo omitido, orden, huérfano, colisión, swap referencial monetariamente neutro, cross-generation y build no declarado. No se borran IDs ni hashes. Recibo combinado SHA256 `e1dcf09526c08c9665ce4512f64d8ee2af1cdbbe0b032c092160c30c9049721d`; comparación externa 75,999493/115,765674 s, separada del wall financiero.

El paquete incluye los cuatro artefactos W1 completos de baseline/candidato y su receta relativa; se verificaron por descarga real. Los profiles históricos de CPU/allocations sobre muestras activas con adds/protección/reemplazo identificaron copias de mapas y getters del ledger; describen esos síntomas y no son un profile nuevo 873 ni una medición aislada del overhead del diagnóstico. Los tiempos finales 873 incluyen ese diagnóstico. Las carencias temporales de S02 y la competencia propia del NQU6 S04 no se rehabilitan con estos recibos.

### Pruebas, cobertura y obligaciones

Alcance prospectivo: 124 funciones completas nuevas/modificadas en 41 archivos desde ed311, incluyendo printJSON; SHA256 `c813b253dbb904b2552371ad3a70a5b9c74a72a8187e9da924c01efc7a09eb46`. Cobertura exacta 873 **3.233/3.432 = 94,2016317016 %, FAIL95**, sin bloques ausentes ni waiver; faltan 28 statements para el umbral. El agregado heredado instrumentado es 14.531/18.495 = 78,56718 %, separado del desarrollo y de repositorios no instrumentados.

CLI pertinente ALL pasó en 646,817 s. La biblioteca inicial falló por ausencia de `INDEPENDENT_HELD_INPUTS` del harness; ese fallo se preserva. El focal corregido sólo por entorno/locator pasó 4,105 s con perfil suplementario 873. No se afirma que la suite inicial fuera toda verde. Las exclusiones declaradas son `TestLargeCorpusStreamingMetrics` y `TestResultWriterStreaming50kBoundedMemory`; no recortan el denominador de producción. Un primer regex stdout ejecutó cero tests y no recibe crédito; los dos regresores nombrados correctos sí pasaron con race en 6,227 s.

Los 199 statements residuales se clasificaron entre guardas dominadas, errores de IO posteriores al check y fronteras UNKNOWN; no se modificó el denominador ni se forzaron estados privados para alcanzar 95 %. No hubo un barrido cosmético final.

| Obligación | Resultado y límite de873 |
|---|---|
|C01 continuidad física|Prueba sintética pública funcional; catálogo real all13 rechazado por falta causal. Continuidad multianual y rollover real incumplidos.|
|C02/L1–L2 pool|3/13 streams de 513 filas, workers 1/2, orden inverso, progreso/cancelación, primera causa/error-EOF y Close bajo backpressure; race independiente PASS.|
|C03 controlador CAMPAIGN|NQZ5 con 4 reemplazos y replay `--result` IDENTICAL; NQU6 `--experiment` IDENTICAL. El caso held de la misma build ejercita reemplazo y ambas rutas con 18.088 records idénticos. PASS dentro de esos alcances.|
|C04 portabilidad/salida|Tres assets descargados a raíz nueva, unión literal 3.494/3.494 y recetas relativas comprobadas. Stdout fallido devuelve error con artefacto íntegro. PASS en estos alcances; diagnóstico UNKNOWN explícito.|
|C05 performance/recibos|Medición exclusiva y W1 equivalente; FAIL 1,5×, FAIL 180/220 s; RSS 512 MiB PASS. Metas 3600/3900 s multianuales no demostradas.|
|C06 oráculo legacy|Comparación completa con identidades distintas y negativos ejecutados; no éxito por cambiar RunID.|
|C07 fronteras/cobertura|MM público stateful, eventos/timers, LONG/SHORT, cuarto cobro, reemplazo y secuencia de inputs ejercidos; cobertura 94,2016 % FAIL95. Rollover real permanece abierto.|
|C08 admisión|Cuerpo admitido inmutable: USD1 sigue USD1; disposiciones y una aplicación monetaria, PASS.|
|C09 getters|Aislamiento antes/después de Finish, nested maps y enteros opacos precisos, PASS.|
|C10 compra|119 no compra; 120 compra una vez sin sobregiro, PASS.|
|C11 provider/referencias|Preimágenes tipadas/digests/estado final y mapa causal en pares nativos de 1/3 generaciones, ALL/SKIP y negativos PASS; W1 cross-build completo PASS. Los cuatro replays oficiales 873 son IDENTICAL con identidad exacta, sin normalización.|
|C12 causalidad fixtures|ADD fill posterior al submit y sin stop anterior; casos elegible 17 min y cancelación terminal 17 min separados. No se exige ADD después de CANCEL. Adjudicaciones y modelo explícito preservados.|
|L3 schedule/ReadPlan|Horizonte medio, 3 expiries, overrides, prefijo/sufijo/default warmup, planes vacíos/recortados, obligaciones del retirado; regresores/race PASS.|
|L4 transición pública real|Dos cruces sintéticos funcionales; cero cruces reales. Requisito real incumplido.|
|L5/A actividad/S2|Dinero, ciclos, oportunidades y días conciliados; causas exportables. Expiración y duración no-ready continua permanecen UNKNOWN.|

El cuarto cobro efectivo se ejercita con fixture **OHLCV1**, 4×1.500 USD, residual 2.253 forfeited, 2 compras×120, caja 10.760 y sucesora 100.000; no se transfiere como prueba V2. El caso held sintético de la build normal 873 acredita precios propios 150,25/250,25/350,25, cantidades 50/62/62, dos cuentas y caja 4.760 USD, Stop→drain→Release sin dominio posterior y exposición conciliada hasta terminal plano. Las auditorías independientes de dominio, señales, exposición y preimágenes completas pasaron. Ningún fixture sintético acredita datos reales faltantes.

Certificado técnico independiente SHA256 `698c8be87ccce00aa40c3e517702869f3e35c212ae0b89026a8dafc82dead4d5`; matriz final SHA256 `99f16afe2008cb71fc19c56a1c4ab12e0f9887e33c445901152e5344edc982f1`. Ambos dictaminan NOT_READY y separan la verificación técnica del recibo externo de publicación. Las suites de fuente utilizan binarios instrumentados atribuidos; no se presentan como ejecuciones del binario normal. Los tests de timers elegibles públicos no acreditan una API custom de timer-token no demostrada. Las pruebas de claims retirados tienen alcance parcial de fuente; el wire público no contiene un censo del ledger de claims. No se deduce ese censo de los fills ni del cierre plano.

### S04 preservado como regresión histórica

Se extrajeron los outputs íntegros S04 sin repetir el backtest: 3.214.366 records BASIC y 3.127.905 CAMPAIGN; trading 2025-10-27T17:52Z→2025-11-27T18:00Z, warmup 2025-10-13T17:52Z. No fueron tres años. Source medido resuelto en DAG: `0a6a0763dbdfc7bb3db93b873d59686d6577fcfa`, binario `f80d8974157452f0e7ac0d757b8815a37d0a259e222d132a69321a196010f69e`. El binario ed311 reportado después, `068a854802c29a6dcb69b949d8c70882101452fc1fa2db0939d6cae60216edd6`, es otro corte.

S04 tenía 24 días técnicos elegibles y 22 con OPEN. BASIC entró 22, con 39 operaciones con fills de 146 creadas; 2 días sin setup. CAMPAIGN entró 7, con 18 operaciones con fills de 140 creadas; los 17 restantes se reconstruyeron como 13 headroom, 2 objetivo diario y 2 sin setup. Las subcausas financieras históricas llevan `INFERRED_ORACLE`, porque el evento antiguo no declaraba esas ramas.

S04 BASIC: saldo 70.307,92 USD, net −29.692,08. CAMPAIGN: gross −3.605, fees 996, net −4.601, 6 compras, 5 burns, 1 cobro neto 1.500, caja 5.780 y saldo activo 101.500,12. No se impuso esa economía a la reparación del reset diario. NQH6 consumió 0/no requerido; no fue rollover. El wall NQU6 S04 de 1.741,82 s estuvo contaminado por competencia propia y conserva FAIL, sin speedup inferido.

### Reproducción y paquete privado

Paquete privado: [prerelease BTX-PERF-LAST — NOT_READY](https://github.com/xKoRx/echo/releases/tag/btx-perf-last-20261010). Requiere el acceso autenticado ya existente a `xKoRx/echo`. Desde un directorio limpio autorizado, descargar sólo los tres assets actuales y sus índices; los cortes 486 y el core 873 preliminar permanecen históricos y no se mezclan:

```sh
mkdir download-final unpack-final
cd download-final
gh release download btx-perf-last-20261010 --repo xKoRx/echo --pattern 'btx-perf-last-core-873f5f1c-final.tar.gz' --pattern 'btx-perf-last-financial-873f5f1c.tar.gz' --pattern 'btx-perf-last-evidence-873f5f1c-final.tar.gz' --pattern 'FINAL-ASSET-SHA256SUMS' --pattern 'FINAL-ASSET-INDEX.json'
sha256sum -c FINAL-ASSET-SHA256SUMS
tar -xzf btx-perf-last-core-873f5f1c-final.tar.gz -C ../unpack-final
tar -xzf btx-perf-last-financial-873f5f1c.tar.gz -C ../unpack-final
tar -xzf btx-perf-last-evidence-873f5f1c-final.tar.gz -C ../unpack-final
cd ../unpack-final
sha256sum -c SHA256SUMS
sha256sum bin/echo-backtest
```

El último hash debe ser `0320b80e78fbf12821eda4004c68c96175f770dedaac747dc306604e9280d83b`. El README raíz es copia del manual único de `source/v3/backtester/README.md`; no reemplaza su autoridad. Los resultados íntegros, ocho CSV, requests, bindings, corpus, matriz de transiciones, ReadPlan y scripts de oráculos se incluyen. El recibo independiente de readback es externo al tar para evitar certificar sus propios bytes. No se distribuyen checkpoints pickle ni transcripts.

Desde la raíz ensamblada del paquete, un comando público por modalidad para el catálogo común:

```sh
GOMAXPROCS=4 bin/echo-backtest experiment --input requests/basic-all13.json --out reproduced-runs/basic-all13
GOMAXPROCS=4 bin/echo-backtest experiment --input requests/campaign-all13.json --out reproduced-runs/campaign-all13
```

Ambos requests reproducen el rechazo de cobertura descrito; no producen un histórico multianual válido. Los cuatro resultados acotados se ejecutan individualmente:

```sh
GOMAXPROCS=4 bin/echo-backtest experiment --input requests/basic-NQZ5.json --out reproduced-runs/basic-NQZ5
GOMAXPROCS=4 bin/echo-backtest experiment --input requests/campaign-NQZ5.json --out reproduced-runs/campaign-NQZ5
GOMAXPROCS=4 bin/echo-backtest experiment --input requests/basic-NQU6.json --out reproduced-runs/basic-NQU6
GOMAXPROCS=4 bin/echo-backtest experiment --input requests/campaign-NQU6.json --out reproduced-runs/campaign-NQU6
```

Replays oficiales de resultados sellados, seriales:

```sh
GOMAXPROCS=4 bin/echo-backtest reproduce --result results/basic-NQZ5/result.json.gz --nt-source-config corpus/nt-source-NQZ5-NQH6.json --out reproduced-replay/basic-NQZ5-result
GOMAXPROCS=4 bin/echo-backtest reproduce --result results/campaign-NQZ5/result.json.gz --nt-source-config corpus/nt-source-NQZ5-NQH6.json --out reproduced-replay/campaign-NQZ5-result
GOMAXPROCS=4 bin/echo-backtest reproduce --result results/basic-NQU6/result.json.gz --nt-source-config corpus/nt-source-NQU6.json --out reproduced-replay/basic-NQU6-result
GOMAXPROCS=4 bin/echo-backtest reproduce --experiment runs/campaign-NQU6/experiment-manifest.json --nt-source-config corpus/nt-source-NQU6.json --out reproduced-replay/campaign-NQU6-experiment
```

Los destinos nuevos preservan originales. La ruta pública de manifiesto es `--experiment`, nunca `--manifest`. El caso sintético held ejercita dos transiciones y reemplazo de cuenta, con ambas rutas del controlador:

```sh
GOMAXPROCS=4 bin/echo-backtest campaign --input evidence/verifier/fixtures/held-synthetic/campaign-input-873.json --nt-source-config evidence/verifier/fixtures/held-synthetic/source.json --out reproduced-held
GOMAXPROCS=4 bin/echo-backtest reproduce --result reproduced-held/bt-c-8fb142d46ee3e047c56a32cf1876d6447a89599cb36ec641bcb0616ac3f9ed9a/result.json.gz --nt-source-config evidence/verifier/fixtures/held-synthetic/source.json --out reproduced-held-result
GOMAXPROCS=4 bin/echo-backtest reproduce --experiment reproduced-held/campaign-manifest.json --nt-source-config evidence/verifier/fixtures/held-synthetic/source.json --out reproduced-held-experiment
```

Los requests y bindings están completos; no requieren programar un wrapper ni elegir topologías. Los scripts forenses y sus instrucciones relativas permiten reconstruir las tablas desde los resultados íntegros; no son un requisito para leer los CSV ya entregados.

El producto también expone validación de catálogo y reporte reutilizable:

```sh
GOMAXPROCS=4 bin/echo-backtest validate-catalog --input requests/basic-all13.json --out recomputed-checks/basic-all13-catalog.json
bin/echo-backtest daily-report --result results/basic-NQZ5/result.json.gz --catalog-validation runs/basic-NQZ5/catalog-validation.json --out recomputed-checks/basic-NQZ5-daily.json
bin/echo-backtest daily-report --result results/campaign-NQZ5/result.json.gz --catalog-validation runs/campaign-NQZ5/catalog-validation.json --out recomputed-checks/campaign-NQZ5-daily.json
bin/echo-backtest daily-report --result results/basic-NQU6/result.json.gz --catalog-validation runs/basic-NQU6/catalog-validation.json --out recomputed-checks/basic-NQU6-daily.json
bin/echo-backtest daily-report --result results/campaign-NQU6/result.json.gz --catalog-validation runs/campaign-NQU6/catalog-validation.json --out recomputed-checks/campaign-NQU6-daily.json
```

### Cierre y delta para Primary

Los cuatro TOPs cerraron una sola vez, con feedback y agent-run atribuibles. Todas las ejecuciones propias terminaron; no quedan procesos financieros, tests, builds o replays abandonados. Fuente, binario y los tres assets permanecen inmutables, con readback independiente completo y recibo externo publicado y vuelto a descargar byte a byte. Agents-OS exclusivamente master; un único change_log. No se modifica BTG-PLAN ni informes previos. Las notas históricas del TOP PERFORMANCE usan la palabra «global» para 3.171/3.427; corresponde al alcance de desarrollo de 486 y no al agregado heredado. Se preserva el recibo original con esta aclaración, sin reescribir al TOP cerrado.

Delta reutilizable: producto reparado, diagnóstico diario y validación causal públicos, inputs y evidencia íntegros, pérdidas y frecuencia explicadas, tests críticos y paridad bajo identidad explícita. Siguen incumplidos continuidad y rollover reales, performance exigida, cobertura95 y las fronteras de diagnóstico declaradas. El Primary conserva control del plan y Owner conserva la aceptación humana; no se propone ni autoriza otra continuación automática.

## Fuentes

- [[BTG-PLAN]]: control exclusivo del Primary, sin modificación por este encargo.
- [[BTX-PERF-DESIGN]]: diseño y adenda vigente, blob `1cedf2e4c66886079a04d18dd60216b423316b42`.
- [[BTX-PERF-ADVERSARIAL]]: obligaciones C01–C12 y matrices, blob `45fa5af308a9999f24c1028684b3eceadf448c95`.
- [[BTX-PERF-FINAL]]: evidencia histórica S04, blob `9b68ea4eb3627d020cef97b79c1fe21681537181`.
- Mandato Owner LAST y recibos sellados de la build873 en el paquete privado: fuentes físicas, requests, resultados íntegros, cobertura, negativos, paridad, actividad y replays.
- DATA: [[2026-10-10-codex-unknown-btx-perf-last-data]] y [[2026-10-10-btx-perf-last-data-session-feedback]].
- PERFORMANCE: [[2026-10-10-codex-gpt-6-1-sol-btx-perf-last-top-performance]] y [[2026-10-10-btx-perf-last-top-performance-session-feedback]]. Su evidencia corresponde al corte histórico declarado.
- INTEGRADOR: [[2026-10-11-codex-unknown-btx-perf-last-integrator]] y [[2026-10-11-btx-perf-last-integrator-session-feedback]], master `61cb9e92c165dfa2b9aae33aede4861df5074c96`.
- VERIFICADOR: [[2026-10-11-codex-unknown-btx-perf-last-top-verifier]] y [[2026-10-11-btx-perf-last-top-verifier-session-feedback]], master `4f4cdc1f847416d5f4af215f55e341b168952a0a`. Las notas delimitan el certificado técnico; el readback posterior tiene recibo externo propio.
- GOD: [[2026-10-10-codex-unknown-btx-perf-last-god]] y [[2026-10-10-btx-perf-last-god-session-feedback]]. Change_log único: [[2026-10-10-btx-perf-last]].
