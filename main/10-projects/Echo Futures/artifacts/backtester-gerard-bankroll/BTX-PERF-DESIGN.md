---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-09"
updated: "2026-10-09"
---

# BTX-PERF-DESIGN

## Propósito

Materializar la entrega técnica S01 recibida y aprobada por Owner, sin otra investigación ni rediseño. La autoridad operativa vigente es la adenda Owner «CIERRE TÉCNICO S01 Y AUTORIZACIÓN ACOTADA DE SHOT 2», incorporada en [[BTG-PLAN]]. El texto del especialista conservado abajo corresponde a su corte histórico, anterior a esa aceptación y al probe E1.

## Contenido

### Autoridad vigente — adenda Owner, 2026-10-09

```text
S01_TECHNICAL_DESIGN = ACCEPTED_FOR_IMPLEMENTATION_WITH_EXPLICIT_PERF_EXCEPTION
E1 = PARTIAL_WITH_EVIDENCE
S02 = AUTHORIZED_REPAIR_AND_INTEGRATION
PERF_TARGET_FREEZE = REQUIRED_BEFORE_OPTIMIZATIONS
FINAL_OWNER_ACCEPTANCE = NOT_GRANTED
```

La arquitectura y los contratos técnicos de esta entrega quedan aceptados para implementación con las precisiones Owner. No constituye aceptación del producto. Prevalece la secuencia S02: recuperar E1 y capturar CPU del R sellado con timeout120s → reparar correctness, entrada integrada y replay → congelar build de control corregida sin optimizaciones → fijar y sellar contrato numérico comparable → optimizar únicamente mecanismos sustentados y contrastar contra ese control. Ningún objetivo se fija o mueve después del primer cambio de rendimiento. Sin evidencia suficiente para el contrato completo, entregar repairs/integración verificados y bloqueo preciso; no otro GOD/probe exploratorio ni optimización ciega.

La superficie S02 es un único TOP LOCAL fresh-context ONE-SHOT en el workspace Daedalus utilizado por E1. Primary coordina, no implementa ni acepta su gate. La ventana histórica terminó el2026-10-09T00:00:00-03:00; esta adenda autoriza continuar el alcance, no reinicia180min ni aprueba las4h sugeridas por E1. S03 independiente con pruebas ejecutadas y S04 corrección/validación siguen vigentes.

La cápsula E1 ya existe localmente y debe verificarse/consumirse, no reconstruirse. Registro remoto `52d17ce92321fe0673eeaf1ed59d7e8753d47af7`: no contiene la cápsula. Binario E1 `66657a99384ff6e622da15cd6953ea34621edc35100b536f118d1ff3918a89fb`. R BASIC89,64s/73,3MiB y CAMPAIGN90,04s/73,5MiB son observaciones de prefijos con warmup, no horizonte completo ni speedup. CPU no capturada por E1; no inferir coste dominante.

Precisiones vinculantes: conservar todas las revisiones comprometidas de SetAccountContext(k)→CloseStage(k+1)→OpenStage(k+2), publicar autoridad final coherente y liberar sólo evidencia poseída del ledger correcto, manteniendo el guard corriente. Nunca registrar sólo LatestRevision, sustituir igualdad por<= ni ignorar errores. Sellar cuerpo tipado y digest al admitir, también con disposición REJECTED/CONFLICT/pendiente; APPLIED no determina disponibilidad del cuerpo. CAMPAIGN replay recompone su controlador y no readmite como externos sus controles regenerados. Divergencia original: esperaba ACCOUNT_REPLACEMENT, reproducción produjo OPERATION_APPLY. Selección futura no equivale a obligación corriente; binding seleccionado conserva su propio año/mes. No inventar calendario/rollover, precios/fills o continuidad. Comparación tipada estricta; cualquier mapeo de IDs es uno-a-uno y conserva referencias. Sin cambios de Strategy/MM/SL/TP/sizing/adds/señales para acelerar.

Estas disposiciones superseden exclusivamente los bloqueos de autorización previa, instrucciones de nuevo E-01, acceso/cápsula pendientes y secuencia de rendimiento del texto histórico siguiente. La primera nueva ejecución NQZ5 verifica el repair, no vuelve a descubrir la causa. Separar PASS de lifecycle, solicitud/admisión/aplicación FUNDED y cobros. El resto del diseño conserva autoridad técnica. Los campos de performance siguen sin números aprobados; las propuestas53,5µs/root-input,180/220s NQU6,2× y512MiB no se convierten en contrato ni evidencia demostrada.

### Entrega original S01 — corte histórico preservado

Origen: Library `BTX-PERF-DESIGN.md`, backing `file_000000009700820e8a3386507c9564dc`, versión1; SHA256 de los bytes recibidos `a792532bdaead5589aa05721369f5861c1807c7989dc4b048e5b59664bde9262`. Las citas y estados internos del siguiente texto pertenecen a la entrega original; no son pruebas nuevas ejecutadas por Primary. Los permisos/estados contradictorios con la adenda anterior son históricos, no instrucciones activas.

# ECHO FUTURES — BTX-PERF-DESIGN

SHOT: BTX-PERF-S01  
STATUS: CANDIDATE_BLOCKED_EVIDENCE  
ROLE: especialista de arquitectura CLOUD; no Primary Manager ni certificador  
DATE: 2026-10-08 · America/Santiago  
CANONICAL_DESTINATION: `10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BTX-PERF-DESIGN.md`  
PERSISTENCE: PENDING_WRITER; este contenido es la entrega de transporte, no una nota canónica materializada.

## 1. Dictamen y decisión

La decisión es **preparación/lectura concurrentes por stream físico, merge causal estable y una sola evolución financiera por modalidad**. Sobre ese motor se corrigen las transiciones contables y el replay de campaña; el hot path activo se optimiza mediante valuación exacta incremental, consultas estrechas, índices mantenidos y compresión rápida sin pérdida. No se paralelizan cuentas completas por contrato ni se reinician Strategy, MM, riesgo o caja para juntar resultados después.

El diseño **no está listo para autorizar implementación**: faltan los recibos físicos que permiten congelar objetivos numéricos de rendimiento. No presento minutos, speedup o RSS inventados. La arquitectura queda decidida; su aceptación y su contrato numérico quedan bloqueados por una sola dependencia de evidencia, E-01. No hay quinto shot ni reapertura de este especialista.

El mandato vigente permite precisamente `CANDIDATE_BLOCKED_EVIDENCE` cuando no se pueden fundamentar los números antes de implementar. Los cuatro gates siguen sin aprobarse por esta entrega. fileciteturn0file0L165-L175

## 2. Acceso, baseline y reloj

| Superficie | Acceso efectivo y límite |
|---|---|
| Source Echo | GitHub autenticado; archivos/rangos leídos en `50250a2b0df6106943108bf6bfe57552409f3d13`. |
| Agents-OS | Bootstrap y control leídos en master `e9a9287ef2804a12519134d7d786868bb41cf417`. No modifiqué el control del manager. |
| Delta de producto | Compare d1b1446d→50250a2b: dos commits, únicamente `AGENTS.md` y `v3/backtester/README.md`. Producto equivalente al baseline d1b1446d; documentación posterior. |
| Evaluación multianual | Recuperado en Library `Texto pegado(20261008-200718).txt`; es relato del evaluador, no recibos originales. |
| Informes y corpus | Los informes originales, los RunSpecs consumidos, los 13 derivados y sus hashes no fueron recuperados. Búsqueda por título, reintento corto y listado reciente de Library no los localizaron; el listado es parcial, no prueba de inexistencia global. |
| Release S05 | Metadata autenticada del prerelease `btg-s05-id-invariance-d1b1446d`, release ID 406837231. Assets no descargados ni analizados; no acredita la evaluación nueva. |
| Runner / TOP | No hay runner conectado ni herramienta efectiva de despacho acreditados. La búsqueda de integraciones no descubrió una conexión utilizable; no se instaló nada. |
| Sandbox | Sólo el mandato estaba montado en `/mnt/data`. Los tres directorios conocidos de evaluación, originales y vault no están montados. No ejecuté builds, tests, backtests ni perfiles. |

Identidades separadas: source de producto `d1b1446d401f88cfa42dee2eb959120305f5a372`; lectura de source/documentación `50250a2b0df6106943108bf6bfe57552409f3d13`; binario histórico S05 documentado `520d5343a1171796b67daa43875ac71ebeb9ce2c5ad39f84737c7adba44a84f1`; binario propio de la evaluación nueva `UNKNOWN`; corpus físico utilizado por este especialista `NONE`. No atribuyo el hash S05 a la compilación posterior ni certifico su estado dirty mediante un relato.

Última comprobación temporal para el diseño: `2026-10-08T22:35:13-03:00`. `OWNER_WINDOW_T0`, `OWNER_DEADLINE_180M` y `OWNER_REMAINING_180M` siguen `UNKNOWN`. El techo calendario permanece `2026-10-09T00:00:00-03:00`; no es una ventana nueva ni evidencia de minutos disponibles. No se encontró un recibo que sustituya los UNKNOWN.

## 3. Hallazgos que determinan el delta

### 3.1 Fallo de revisiones: mecanismo localizado, atribución física pendiente

En `v3/backtester/run.go`, `applyContextTransition` obtiene `led` de `SetAccountContext`. Después ejecuta `CloseStage` y `OpenStage` para `START_NEW_STAGE`, ignorando sus revisiones devueltas; eventualmente también abre un día. Sólo después llama `recordEconomics(led, ...)`.

En `driver.go`, `recordEconomics` entrega esa revisión al recorder y luego pide a **`r.ledger`** liberar historial con su número. En `sdk/futures/accounting/ledger.go`, `ReleaseRecordedHistory` exige que ese número sea la autoridad corriente. Por lectura de source, una transición con dos commits posteriores intenta liberar R mientras la autoridad es R+2. Además, una reentrada que sustituya `r.ledger` durante `Record` podría desviar la liberación al ledger equivocado.

Esto es una **explicación estática concreta compatible con 4870→4872**, no una reproducción de NQZ5. La primera causa física debe conciliar cuenta, generación del ledger, contexto, causa y las revisiones 4869–4872. No declarar simplemente «el reset» como causa: `RESET_ADJUSTMENT` y la transición `pass-funded` son controles diferentes. fileciteturn26file0 fileciteturn39file0 fileciteturn24file0

### 3.2 Replay: hay dos carencias distintas

`cmd/echo-backtest/reproduce.go` recoge payloads de `ACCOUNT_CASHFLOW` y `ACCOUNT_CONTEXT_TRANSITION`, más controles pendientes del resolved spec. No reconstruye el reemplazo del compartimento ni el libro de caja de `campaignDriver`.

`RunState.EnqueueControl` registra metadatos/digest de admisión, no su payload tipado completo en ese punto. Una transición que ya salió de pendientes y falla antes de emitir su registro aplicado puede quedar sin payload recuperable. Es consistente con el error de readmisión reportado; hace falta el artefacto original para confirmar ese recorrido.

Por lo tanto, ni borrar `ACCOUNT_REPLACEMENT` del comparador ni conservar sólo las admisiones exitosas constituye un repair. fileciteturn40file0 fileciteturn29file0

### 3.3 Multicontrato: no basta quitar dos validaciones del CLI

`spec.go` ya tiene `ContractCatalogEntry`, `ContractScheduleEntry`, `PrepareAt`, `EffectiveAt` y refs de configuración. `run.go` ya prepara candidatos y hace selección prospectiva. La interfaz de campaña inspeccionada exige un stream.

Hay otros puntos materiales: `applyContextTransition` considera cualquier selección futura pendiente como falta de quiescencia; los helpers de sesión de campaña usan `catalog[0]`; `applySelection` conserva año/mes del contrato original al instalar el nuevo. El delta debe separar una obligación vigente de una selección futura declarada, resolver la sesión del contrato pertinente y transportar identidad física completa. Estos son hallazgos de source, no resultados de tests. fileciteturn26file0 fileciteturn27file0 fileciteturn32file0 fileciteturn54file0

### 3.4 Coste activo: qué está observado y qué no

| Ruta inspeccionada | Observación de source | Hipótesis que debe medir el probe |
|---|---|---|
| `ohlc_scheduler.go` | Un paso por tick de lattice; cálculo temporal con `big.Int`, conversión de precio con racionales, mark, venue, callbacks, escaneo y ordenamiento de owners. | Multiplicación importante de trabajo activo por amplitud intraminuto. |
| `accounting/ledger.go` | Valuación recorre lotes; `Snapshot()` vuelve a valorar y ordena contratos y días. | Valuaciones y allocations repetidas para consultas pequeñas. |
| `projection.go` | Se usan snapshots completos para obtener inventario, día o cantidad de días; se proyecta riesgo en revisiones materiales. | Coste evitable de lectura, no licencia para omitir riesgo. |
| `resultwriter.go` | Serializa payload y wire record; gzip usa `BestCompression`; digests y escritura son síncronos. | CPU de serialización/compresión material durante trading, además de I/O. |
| `ntminute.go` | Escaneo inicial por archivo; snapshot privado copiado y verificado al abrir; merge por heap y clon defensivo en `Peek`. | Preparación repetida e I/O; no se presume que dominen al trading. |

**CPU dominante, porcentajes, allocations por evento, volumen de salida y speedup alcanzable: NOT_DEMONSTRATED.** Los 88/67 minutos bajo 13–14 procesos no sirven de baseline aislado. fileciteturn16file0 fileciteturn19file0 fileciteturn41file0 fileciteturn53file0

## 4. Contrato de experimento e identidad

Se incorpora `ExperimentRequest`, versión propuesta `echo.backtest.experiment.v1`, como entrada única de la operación integrada. Cada petición lleva una modalidad, una referencia sellada al descriptor común del corpus y un único catálogo/schedule; no una lista adicional de contratos para un orquestador.

El descriptor común contiene binding físico completo —instrumento, contrato, año/mes, stream, snapshot económico, referencia externa—, identidad lógica del dataset, SHA256/bytes por archivo y su convención temporal. Las rutas de lectura son localizadores privados, separados de la identidad semántica. No se derivan contratos desde nombres de archivo.

La petición fija horizonte solicitado, prefijo de warmup, política de primera elegibilidad, módulos/configuraciones públicos, fidelidad OHLC V2/CONFIGURED, valuación, costos, calendario/versiones, tratamiento de gaps, end policy y política de rollover. BASIC y CAMPAIGN comparten las autoridades de mercado y Strategy/MM; difieren sólo en su contrato económico declarado.

BASIC tiene USD100.000 iniciales y ningún programa prop, compra o cobro. CAMPAIGN tiene caja5000, costo120 ON_DEMAND, una cuenta operando y límite de cuatro cobros efectivos; conserva los demás parámetros funcionales recibidos. Una pérdida nominal no vuelve a debitar la caja.

`experiment_id` deriva del contenido semántico canónico de la petición: incluye modalidad, autoridades, datos, tiempos y políticas; excluye label, rutas locales, workers y nombre de ejecución. `attempt_id` identifica una ejecución física y nunca ordena dinero. `RunID`, commit, patch digest, estado dirty, binario y toolchain se conservan como identidades de ejecución, sin alterar artificialmente las reglas existentes de integridad de RunID. fileciteturn48file0

Una build distinta puede ejecutar la misma petición; eso no acredita equivalencia. Se compara con contrato explícito y se conserva su provenance. Los IDs económicos se derivan de causas y ordinales semánticos, nunca de rutas ni llegada de workers. Los empates físicos conservan la secuencia de aceptación del venue, no el orden lexicográfico de IDs.

`ExperimentManifest` materializa la petición resuelta, entradas efectivamente consumidas, schedule, capacidades de módulos, build real, perfiles de ejecución/evidencia, rutas relativas y digests de outputs. Las admisiones dinámicas completan un registro append-only tipado y un sello final; no reescriben silenciosamente la petición inicial.

## 5. Partición elegida y prueba de continuidad

### 5.1 Comparación y elección

| Alternativa | Coste / equivalencia | Decisión |
|---|---|---|
| Preparar, validar y leer streams concurrentemente; merge antes de decisiones | O(N) de parsing/validación y O(N log K) de merge; memoria acotada. Equivalencia demostrable por prefijos y orden estable. No elimina el coste financiero activo. | **Elegida.** |
| Calcular cada contrato independientemente | Barras y transformaciones puras sólo son independientes con entradas físicas, parámetros y prefijo idénticos. Strategy stateful, cuenta/MM/provider/campaña no lo son. | Permitidas sólo transformaciones de fuente puras dentro de la primera opción; no se añade otro motor de indicadores ni Strategy por worker. |
| Segmentos financieros con checkpoint o resumen composable | Deben transferir Strategy/ciclos, órdenes, claims, dedup, timers, día/contexto, ledger, provider, caja y cursor intrabar. No se encontró un contrato de restauración completa certificado. | Rechazada para BTX-PERF: coste de prueba y mantenimiento no justificado frente al delta local. |

Se usa un solo integrador de producto. Topología decidida: **una modalidad financiera a la vez**, un pool de preparación de **hasta dos workers**, y el driver causal existente como único escritor del estado financiero. Con menos de tres CPUs efectivas o memoria insuficiente, el pool cae a uno; esto es política de admisión de recursos, no promesa de aceleración. Los valores efectivos y su razón se registran. No se relanza el lote de 13 simulaciones financieras.

### 5.2 Merge, fases y futuro

El adapter conserva la clave existente `(AvailableAt, StreamID, SourceOrder)` para barras homogéneas de un minuto. El driver mantiene su orden causal real: controles, fronteras, mercado y timers; en V2 los cierres OHLC tienen su fase específica y precedencia respecto del timer de cierre. No se reemplaza esto por un único sort de timestamps. fileciteturn33file0 fileciteturn36file0 fileciteturn49file0

Cada stream requerido ofrece su siguiente registro o un watermark acreditado hasta el cual no puede aportar otro. No se avanza por encima del mínimo seguro porque otro worker terminó primero. Dentro de cada fase se conserva el orden de la implementación secuencial, incluido el drenaje completo de consecuencias antes de otra raíz.

Los workers no publican HLCV antes de `AvailableAt`, no deciden LONG/SHORT del camino intrabar y no evalúan módulos. La orientación del lattice se decide en el driver con su estado al Open, como en la referencia. Se pueden preparar datos privados futuros; no pueden aparecer en `MarketContext`, readiness, marks o señales antes de su causa.

### 5.3 Buffers, fallos y memoria

Cada tarea entrega chunks inmutables limitados por registros y bytes; se propone un máximo de 256 registros o 1MiB serializado por chunk, lo primero que ocurra. Hay una entrega pendiente por worker, una cabecera por stream requerido y backpressure global. El consumo real de objetos decodificados/GC se mide aparte: esos 1MiB no son una promesa de RSS.

La agenda prioriza el stream que bloquea el watermark. No permite que candidatos futuros ocupen todas las plazas mientras el stream indispensable espera, evitando deadlock por backpressure. Los pools no reutilizan buffers hasta que su consumidor los libera. Se conserva copia defensiva en las fronteras públicas; dentro del pipeline se transfieren objetos inmutables de propietario único.

Errores de validación encontrados durante preparación se adjudican en orden canónico, no por el primer worker que responde. Errores de datos en el consumo conservan coordenada y primera causa. Un fallo de I/O, timeout, cancelación o escritura invalida la ejecución; puede existir evidencia de prefijo, jamás un resultado financiero completo. Se cierran workers, readers y writer; un fallo de Close también impide aceptar el sello.

El espacio crece con buffers, streams requeridos, estado vivo y dedup permanente, no con todas las barras/resultados retenidos en RAM. Dedup no se expulsa para cumplir RSS. El espacio temporal, las snapshots privadas y la expansión potencial del gzip rápido deben caber en el disco realmente disponible antes del lanzamiento.

### 5.4 Contraejemplo A→B

Ejemplo de prueba, no resultado real: A compra la cuenta1, por lo que caja5000→4880. A la quema y se aplica la segunda compra antes de entrar a B: caja4760. B debe comenzar con esa caja, la cuenta2 y la continuidad técnica resultante. Un backtest independiente de B empezaría con caja5000 y, tras su propia compra,4880: ya inventó USD120 y borró la historia.

En BASIC, una pérdida hipotética de600 en A deja99400 en B, no100000. Estar flat no borra el día, los watermarks de riesgo ni el estado de la Strategy.

La solución elegida transmite la autoridad por el mismo estado vivo del driver, no por una suma de reportes. El oráculo exige identidad semántica con workers1/2, entrega invertida, worker lento y buffers saturados; con fallo de worker exige fallo íntegro, no un subconjunto agregado como éxito.

## 6. Optimización del hot path sin cambiar las decisiones

### 6.1 Valuación exacta incremental y read models estrechos

El ledger mantiene por contrato cantidad firmada, base económica remanente y contribución a unrealized, actualizadas sólo por fills, cambios de mark y mutaciones que realmente las afecten. Los lotes FIFO siguen siendo la autoridad de realized y dedup. Para un inventario de una dirección, la identidad exacta es:

`unrealized_c = mark_liquidación_c × cantidad_firmada_c × point_value_c − base_firmada_c`.

La base agrega entradas remanentes con signo y point value. Un parcial elimina exactamente su porción FIFO; una reversa cierra lotes reales y crea el residual. Cambiar el mark de C recalcula C, no todos sus lotes ni los contratos intactos. El agregado por cuenta se actualiza por diferencia exacta. Marcas ausentes mantienen la misma condición unresolved y la misma política fail-closed.

Se agregan consultas observacionales estrechas: día actual/abierto, cantidad de días, net por contrato y revisión publicada. `Snapshot()` completo queda para exportar o cuando sea necesario. Ninguna lectura crea revisiones, refresca relojes ni modifica riesgo. La publicación se versiona por generación de ledger y revisión; el préstamo de maps/punteros mutables no cruza el API.

Se preservan ambas fórmulas de AccountDayPnL y su comprobación de igualdad exacta. No se cambia a floats ni a «centavos» que no representen todos los importes. Fast paths enteros exigen representabilidad y operaciones chequeadas; el fallback exacto se conserva antes de cualquier mutación. Casos inválidos deben fallar en la misma causa observable; no se mueve un overflow fuera del horizonte porque un worker precalculó un resultado.

### 6.2 Invariantes, índices y pasos intrabar

Se preparan una vez por contrato los invariantes de tick/point value/modelo. Se evita ordenar todos los owners en cada paso mediante un índice por contrato actualizado cuando cambia la pertenencia; su iteración conserva el orden de referencia. El índice no debe excluir un owner terminal, pendiente o con callback sólo por parecer flat: debe representar exactamente los destinatarios del algoritmo anterior.

El cálculo de `floor(duration_ns × step / (total+1))` puede tener un fast path entero con producto ancho o división segura, conservando exactamente los timestamps y el fallback. Igualdad de endpoints no autoriza fusionar observaciones intermedias.

No se acepta como dogma un callback caro por tick: se abarata su preparación y la economía que observa. Sin embargo, **no se omiten callbacks activos de un MM desconocido**. Pueden actualizar máximos, timers, contadores o emitir órdenes. Una orden nacida de un callback entra al drain y sólo es elegible en una observación posterior según la autoridad existente.

Se conserva `INERT_SKIP` únicamente bajo prueba de ausencia de consumidores/obligaciones. Para omitir un intervalo activo se necesitaría un contrato público que, para TODOS los consumidores —Operation, MM, Provider/riesgo, venue, timers, Strategy y evidencia—, demuestre un avance equivalente, su siguiente causa y las observaciones reconstruibles. Ese contrato no está demostrado en el source leído; **no se introduce un framework de saltos activos en estos cuatro shots**. No hay `if Gerard`, búsqueda exclusiva de SL/TP/add ni saltos por estar flat. Una mejora sólo de warmup tampoco aprueba performance.

### 6.3 Evidencia e I/O

El perfil nuevo fija gzip **BestSpeed** con metadata determinista y cierre completo, en vez de BestCompression. Es compresión sin pérdida: se preserva el contenido lógico, registros tipados, orden y digests; puede aumentar el tamaño físico. La mejora de CPU es una hipótesis medible, no una cifra comprometida. La documentación oficial de Go permite seleccionar niveles y advierte que los bytes comprimidos no son garantía de compatibilidad entre versiones del toolchain; por ello toolchain y codec se fijan y el oráculo principal es lógico/tipado, además del hash físico por archivo. fileciteturn53file0 citeturn245394search1

No se cambia a recorder descartable, no se muestrean revisiones y no se omiten MM evaluations. Serialización/buffering pueden reutilizar almacenamiento sólo después de capturar propiedad de los bytes; `Record` exitoso significa evidencia poseída síncronamente por el sink. `Close`, checksum y finalización permanecen obligatorios. No se añaden writer asíncrono, nuevo formato columnar ni caché de resultados financieros.

El adapter mantiene la comprobación de bytes y protección de snapshot privada frente a cambios de fuente. Una cache caliente no evita verificar identidad ni confía en mtime. Se paralelizan scans/snapshots por stream, sin declarar eliminados costes que aún son necesarios para integridad.

## 7. Contratos físicos, rollover, warmup y gaps

### 7.1 Rollover decidido

El schedule es explícito e inmutable al empezar. Para construirlo desde las entradas monostream sin pedir al operador trece invocaciones, el preparador integrado aplica una regla funcional única: **seleccionar el siguiente vencimiento en la primera apertura de sesión del mes de vencimiento del contrato saliente**, usando año/mes físicos declarados y el calendario/versiones de la petición. La primera selección usa el primer contrato del horizonte con identidad validada. Se materializan los instantes y refs; el runtime no recalcula el schedule según resultados.

Esta regla es una **FUNCTIONAL_ASSUMPTION de este experimento**, no una afirmación sobre el rollover oficial del exchange ni la liquidez real. No usa precios, volumen futuro, PnL o el «segmento que salió mejor». Un schedule ya sellado como autoridad de la petición no se reemplaza por esta generación. Faltas de identidad o de capacidad del calendario para resolver una apertura producen error explícito, no fechas adivinadas.

No se backadjustan expiries ni se transforma una posición de A en una de B. Cada fill y mark conserva su contrato. Una diferencia de precio A/B no genera PnL. En la selección, A puede quedar RETIRING: sus órdenes, protección, finality y ciclo técnico siguen requiriendo A. B sólo admite riesgo después de su activación/readiness legítimas. Alcanzar una fecha de último trading sin poder resolver obligaciones deja INCOMPLETE, no un cierre sintético.

### 7.2 Warmup y fuentes requeridas

El prefijo necesario proviene de los requisitos públicos de los módulos y del calendario/stream, no de14d ni de un número H4 incrustado en el driver. `strategy.WarmupReadiness` ya se consulta desde `requireNativeWarmup`; los módulos sin esa capacidad conservan el gate genérico, no una aprobación implícita. fileciteturn49file0

El preparador deriva `PrepareAt` y las refs por candidato sin evaluar señales. La primera elegibilidad y la política de horizonte quedan selladas. Si el prefijo disponible no satisface el requisito, se informa WARMUP_INCOMPLETE; no se acorta el lookback ni se reinicia dinero para poder avanzar. En una sustitución de cuenta sólo se crea el compartimento financiero definido por campaña; no se repite el warmup técnico de todo el experimento.

Se preparan únicamente slots necesarios, respetando el límite existente de tres por Strategy —activo drenando, seleccionado y próximo candidato—. Las fuentes retiradas se liberan sólo cuando ya no hay posiciones, órdenes, claims, timers o ciclo que las requieran. Una selección futura por sí sola no bloquea un cambio de contexto financiero presente.

El manifest distingue inventario validado del corpus y `ReadPlan` consumible: unión de intervalos por obligación/stream, con sus conteos y digests esperados. Los chequeos de finalización contrastan consumo contra ese plan, sin exigir actividad de contratos todavía no requeridos ni borrar omisiones reales. Deben conservarse los bordes temporales del runtime, especialmente la diferencia entre intervalo de una barra y su disponibilidad al cierre; el último cierre y `EndExclusive` tienen regresor explícito. No se introduce una búsqueda retrospectiva del mejor intervalo.

### 7.3 Cobertura y recuperación

La cobertura no se calcula sumando la duración nominal de trece archivos. Se informa por stream y por obligación, con intervalos esperados, presentes, acreditadamente cerrados, desconocidos y no requeridos. Los labels `MissingOpenMinutes`/`ClosedMinutes` del modelo semanal del evaluador no son por sí solos prueba histórica del exchange.

| Intervalo | Tratamiento |
|---|---|
| Cierre acreditado por autoridad aplicable | Avanzan reloj y timers que correspondan, sin fabricar barras/fills. Se conservan freshness y obligaciones. |
| Stream no requerido | No fuerza decisiones ni contabilidad. Sigue existiendo en inventario de cobertura; no se le inventan observaciones. |
| Gap de candidato aún no necesario | Se invalida su preparación/readiness; puede continuar el contrato actual mientras sus obligaciones sean resolubles. Al necesitar ese candidato se hace visible el bloqueo. |
| Gap desconocido del stream requerido por decisiones o ejecución | `INCOMPLETE / SOURCE_COVERAGE_INCOMPLETE` en la primera frontera afectada, incluso estando flat si el módulo requiere ese pasado. |
| Obligación de posición/orden imposible de valorar o ejecutar | INCOMPLETE con contrato, causa, intervalo, exposición y última autoridad válida; no burn, balance ni fill inventados. |

No se demostró un contrato compartido que restaure el estado arbitrario de una Strategy tras omitir mercado desconocido. Por eso este diseño no salta gaps y llama continua a la trayectoria resultante. La recuperación es reejecución desde entradas verificadas, o un nuevo experimento con una autoridad de datos corregida; no resume por detrás del hueco ni borra el estado. No se abre una investigación indiscriminada del calendario.

El producto debe aceptar la petición integrada y explicar su primera frontera real aunque los datos no permitan completar el horizonte. Ese estado no convierte un bug o el CLI monostream en falta externa de datos; tampoco equivale a cobertura aprobada.

## 8. Repairs contables y de campaña

### 8.1 Batch de revisiones y ownership

Se introduce un batch acotado de transición en el owner contable compartido. Prevalida el cambio completo y prepara las revisiones ordenadas que producen contexto, cierre/apertura de stage y día. No copia todo el historial o dedup: prepara el pequeño delta de autoridad afectado y sus snapshots de evidencia.

El driver instala/publica la autoridad coherente como una unidad causal; no entrega callbacks financieros durante un estado mixto. Cada revisión comprometida se captura en orden, incluyendo seed/apertura del nuevo ledger. La evidencia de una transición no se reduce a «la última» descartando las intermedias. La proyección pública final corresponde a la revisión final y a sus términos/seed, nunca a `led` antiguo.

La liberación lleva un recibo interno `(ledger_generation, account_id, through_revision, contiguous_capture)` emitido después de que el sink posea el batch. Sólo se llama `ReleaseRecordedHistory` sobre **el ledger capturado**, con el high-water corriente y toda la evidencia previa requerida capturada. Se conserva la comprobación de autoridad corriente. Si la autoridad avanzó sin captura, no se cambia el número para hacerla pasar: se retiene el sufijo y se falla o termina el batch pendiente de forma explícita.

Los mutadores públicos rechazan reentrada desde un callback de recorder antes de modificar estado. Las lecturas públicas ven la última publicación coherente. Esto no prohíbe los callbacks legítimos de Strategy/MM que generan efectos: siguen pasando por el drain existente. Ante `Record`/`Close` fallido se conserva primera causa y evidencia pendiente; ninguna vista/ACK declara finalización aceptada. Un sink que retenga referencias prestadas no puede habilitar liberación de historial.

### 8.2 Controles y reemplazos completos

Se sella el payload tipado e inmutable de cada admisión aceptada: clase, ID, ordinal, cuenta/generación, contexto esperado, frontera de admisión, effective_at y digest del contenido. Su retención no depende de llegar a APPLIED. Una transición fallida o pendiente sigue siendo reconstruible; payload ausente o discordante es un error de integridad.

El reemplazo registra petición y resultado: identidad previa esperada, cuenta sucesora completa, snapshot/configuración, términos, risk seed, importe nominal, instante y secuencia. Se prepara el compartimento sucesor antes de retirar el anterior. `ACCOUNT_REPLACEMENT` aplicado significa swap exitoso; un fallo de composición tiene disposición propia, no una activación fingida. Antes del swap se resuelven las obligaciones del viejo compartimento y su evidencia retenida.

La nueva generación no hereda PnL, órdenes o MM del compartimento viejo; conserva mercado, analytics, Strategy, schedule y cursor intrabar tal como exige campaña. Rev1 de una nueva cuenta no colisiona con rev1 de otra. Se cercan timers antiguos y se conserva la autoridad de orden/eligibilidad del seed nativo.

### 8.3 Libro de caja, términos y resultados

Se separan las disposiciones PURCHASE_REQUESTED, PURCHASE_APPLIED y ACCOUNT_ACTIVATED. La compra debitada y una activación fallida no son el mismo hecho: el reporte conserva ese prefijo y no simula una cuenta operando. No se añade devolución automática. La primera compra también valida caja suficiente antes del débito; las duplicadas con igual identidad no cobran de nuevo y un payload distinto falla.

El perfil mantiene su semántica ON_DEMAND: un débito efectivamente aplicado se cuenta aunque la posterior ejecución técnica fracase. La caja sólo cambia con esos débitos y cobros netos realmente aplicados:

`caja_final = caja_inicial − Σ compras_aplicadas + Σ retiros_netos_cobrados`.

Los registros de caja tienen identidad, causalidad y enlace al control/disposición. EVALUATION→FUNDED no compra otra cuenta. Los términos y selectors nuevos pertenecen al nuevo contexto. La cuarta solicitud pendiente no retira ni acredita; el cuarto cobro sí dispara retiro, con residual separado y no reinvertible. Caja insuficiente es un término de negocio explícito, no un genérico STOP que sobrescribe la primera causa.

La contabilidad de pases queda desagregada: outcome de evaluación latched, solicitud pass-funded, aplicación de transición y funded activo. **PASES de la evaluación histórica = UNRESOLVED** hasta conciliar los cuatro; no se adopta «0» del resumen.

Estos repairs corrigen causalidad, aplicación o exportación de la economía estipulada. No cambian targets, SL/TP, adds, sizing, payout chunk, split, floor ni reglas para obtener rentabilidad.

## 9. Replay oficial y esquema

La operación oficial reproduce **el experimento completo**, no sólo `RunState`: vuelve a componer BASIC o el mismo driver de CAMPAIGN desde la petición sellada. Las decisiones deterministas de campaña se recalculan y se comparan antes de aplicar con su traza esperada; no se fuerzan desde un resultado para ocultar una política divergente. Controles externos admitidos se readmiten en su frontera sellada.

El registro tipado cubre admisiones, compras, reemplazos, contexto, retiros, cobros y término. La caja se reconstruye desde eventos efectivamente aplicados y se concilia contra el resumen, no desde `cash_final` como seed. Se comparan además señales, decisiones/MM, órdenes, fills, reservas, claims, estados públicos, requisitos, revisiones, errores y residual final.

Se propone `echo.backtest.result.v2` para las nuevas familias/disposiciones, más el manifest de experimento v1. Reader y comparator aceptan sólo variantes conocidas y payloads válidos; no se normalizan globalmente IDs, account contexts, dinero, tiempos o kinds. Los resultados v1 siguen legibles con sus reglas, pero un v1 que perdió el payload no se «repara» inventándolo.

Diferencias legítimas enumeradas: contenedor gzip y su hash físico; provenance de build/attempt; nuevos registros de admisión/ownership expresamente tipados; revisiones añadidas por el repair documentado. Un mapeo de compatibilidad no elimina revisiones o controles para tapar divergencias.

Se distinguen dos comparaciones. En caminos no afectados, baseline50250a2b versus candidato con equivalencia semántica estricta. En los caminos reparados, referencia corregida sin optimizaciones versus optimizado, con la misma configuración y el mismo esquema. El defecto original se prueba contra un oráculo independiente de revisiones/efectos; no se exige reproducir un bug como «paridad» ni se usa un aborto viejo como denominador de speedup.

## 10. Superficie pública

Se agrega `experiment` al CLI, con una sola entrada por modalidad y sin repetir `--nt-source-config`. La petición resuelve todas las rutas relativas desde su raíz declarada y verifica sus digests; una flag externa conflictiva se rechaza. `prepare-functional-nt`, `run` y `campaign` pueden mantenerse como compatibilidad, pero el flujo integrado no depende de scripts del operador.

Ejemplos **PROPUESTOS, no comandos ejecutados ni flags existentes acreditados**:

```text
echo-backtest experiment --input basic-experiment.json --out outputs/basic
echo-backtest experiment --input campaign-experiment.json --out outputs/campaign
echo-backtest reproduce --experiment outputs/campaign/experiment-manifest.json --out replay/campaign
```

Las dos peticiones referencian el mismo descriptor común sellado; no duplican una lista de trece contratos. El preparador integrado genera esos inputs desde una única especificación de fuentes, identidad y calendario, no desde arrays de un orquestador.

Help y README documentan modalidad, preparación integrada, replay, fidelidad efectiva y fallos. Stdout devuelve JSON con estado de ejecución, completion, modalidad, experiment/attempt/run IDs, frontier, primera causa, manifest, artefacto causal, reporte financiero y coverage report. No obliga a adivinar `causal-artifact/` ni una carpeta bt-c.

Códigos propuestos: 0 para operación completa con artefacto íntegro y criterio de completion explícito; 1 para INCOMPLETE o replay divergente; 2 para entrada inválida/fallo técnico. Una campaña puede terminar válidamente por bankroll insuficiente sólo si esa absorción queda declarada y sellada; no se presenta como mercado simulado hasta el horizonte. `cash_reconciled=true` de un prefijo abortado nunca determina exit0 por sí solo.

`v3/backtester/README.md` sigue siendo el único manual del producto. Este artefacto no crea una segunda guía de operación.

## 11. Contrato de rendimiento y único probe E-01

### 11.1 Estado de los valores obligatorios

| Campo | Estado al entregar |
|---|---|
| MAX_WALL_PER_MODE, horizonte completo | NOT_DEMONSTRATED; no valor numérico congelado. |
| MIN_SPEEDUP_TARGET | NOT_DEMONSTRATED; falta baseline aislado y fracción de coste atribuible. |
| MAX_RSS | NOT_DEMONSTRATED; faltan cuotas/memoria/carga actuales y medición del workload. |
| Throughput objetivo | NOT_DEMONSTRATED; concurrencia financiera decidida C=1, pool máximo2 sujeto a admisión. |
| Presupuestos por preparación/warmup/activo/evidencia/finalización | NOT_DEMONSTRATED; no porcentajes de CPU inventados. |
| Hashes de workload y binario medido | No recuperados; source sí resuelto. |

**Estos UNKNOWN bloquean la aceptación previa a Shot2.** La topología y los límites de buffers son decisiones de diseño, no un contrato numérico de performance disfrazado. No se fija un objetivo cómodo para después de ver el resultado.

### 11.2 E-01: BTX-PERF-INPUT-CAPSULE + recibo único de probe

Un único bloqueo reúne lo que falta: cápsula verificable y ejecución aislada por un TOP en runner ya autorizado. La cápsula no ha sido construida ni transferida.

Su raíz privada, fuera del vault, contiene un manifest con ruta relativa, tamaño, SHA256, tipo/procedencia y relaciones entre informe, spec, output y comando. Debe incluir los dos informes originales; descriptores y RunSpecs realmente consumidos; recibos de build/comandos/rc/wall/concurrencia; los13 derivados autorizados con conteos/exclusiones/gaps; y artefactos mínimos completos de NQZ5, BASIC equivalente y replays NQZ3/NQZ4. Un texto de error no reemplaza payloads, footer ni digests.

Los localizadores se resuelven desde los descriptores S01. Si el runner ya tiene bytes idénticos por hash sólo se transfieren recibos y delta. Se referencia source50250a2b; no otro clon completo. El path histórico aportado por Owner es un localizador externo, no una ruta montada demostrada ni otro shot.

### 11.3 Probe cerrado para el manager

Responsable: un TOP mecánico, sin modificar producto, ejecutado únicamente por herramienta real. Este especialista no lo ha despachado.

**Precondición de lanzamiento:** manifest de cápsula íntegro; binary SHA/clean status reales; comandos existentes comprobados; permiso/capacidad de perf ya disponible; y un presupuesto de tiempo expresamente adjudicado por el manager. Se registran CPU efectiva/cpuset/cuota/cgroup, GOMAXPROCS, límites de memoria, carga ajena, RAM y disco disponibles, filesystem y cache. No se mata carga ajena, se vacía la cache global, amplían cuotas ni instalan profilers.

**Workloads:** W0 es el prefijo causal del BASIC NQZ5 realmente consumido, desde su WarmupStart hasta la primera hora completa de trading elegible; W1 es un prefijo activo difícil: se elige el primer día contable completo con fills/exposición CONFIGURED situado en el cuartil superior de pasos de lattice por minuto con exposición entre los días completos de ese tramo, según sus artefactos; el prefijo llega hasta su cierre. Se preserva todo el estado anterior; no se empieza en la revisión4870 ni se crea una cuenta nueva al comienzo del día activo. Si W1 no existe en esos recibos, se toma con la misma regla el BASIC NQU6 realmente consumido. La selección usa actividad para medir coste, no PnL para mejorar resultados.

El TOP resuelve y sella fechas/hashes a partir de esos specs y recibos antes de ejecutar. Hoy esos hashes **no están resueltos**: por tanto el probe está especificado pero **NO ES LANZABLE** desde esta entrega. No sustituyo ese requisito con una ruta adivinada.

**Ejecución acotada:** una modalidad/proceso a la vez; dos mediciones normales del mismo W0 y dos del mismo W1 —primera apertura con estado de cache declarado y repetición caliente—; como máximo una captura CPU adicional de W1. Límite de seguridad: el menor entre600s totales y el presupuesto real adjudicado. Si el presupuesto es UNKNOWN, no lanzar. Un timeout conserva métricas y primera causa, pero no se convierte en tiempo de un workload completado ni se acorta retroactivamente para favorecer el ratio. No se lanzan13 full-extents ni la ventana dorada completa por rutina.

La perfilación sólo utiliza una capacidad existente y comprobada. Si no está disponible sin instrumentar producto o instalar herramientas, se registra esa carencia y E-01 sigue abierto. El overhead del perfil no entra al wall comparable. La documentación oficial de Go advierte que los perfiles pueden interferir entre sí; se toma CPU separado y se distinguen heap vivo, allocations y GC. citeturn245394search0

**Recibo obligatorio:** comando real, rc, build/binario, spec y hashes, horizonte pedido/alcanzado, preparación, warmup, activo, escritura/finalización, wall/user/sys, RSS máximo, allocations/GC obtenibles, filas/bytes, pasos despachados/omitidos, callbacks, revisiones, fills y tiempo con exposición, registros/bytes comprimidos, I/O/esperas/errores. Una métrica no expuesta se marca UNKNOWN; si es material para decidir, no se aprueba el contrato.

**Interpretación sin otra ronda GOD:** el manager contrasta la hipótesis de valuación/copias/compresión con el perfil y registra en BTG-PLAN los números previos a Shot2. La proyección se descompone por volumen de fuentes, warmup, pasos activos, revisiones y bytes de evidencia; no se extrapola sólo por «días» ni por filas. Los13 archivos se escanean mecánicamente para volumen y cotas de lattice, no como13 backtests. Las frecuencias financieras futuras no se inventan: se explicitan las cotas y supuestos de ocupación.

El tiempo end-to-end incluye todas las fases. El throughput del lote C=1 se expresa como dos modalidades completadas sobre su wall conjunto, separado del tiempo de sus replays y de la verificación total. Los presupuestos de RAM/disco deben contener estado vivo, dedup, buffers y expansión de salida. El objetivo se congela con sus supuestos y mecanismo falsificable; si el perfil o el reloj real no lo justifican, se conserva BLOCKED, no se inicia implementación con una promesa abierta.

Para performance final se exige un caso activo completo comparable y ambas modalidades integradas con la política de completion declarada. Un fallo temprano por coverage no acredita una latencia para el horizonte completo; sus timings son sólo preparación/prefijo. No se usa el aborto original de NQZ5 contra el candidato terminado.

## 12. Owners y paquete de implementación

Todos los paths Echo siguientes se inspeccionaron en50250a2b; los rangos indican lectura efectiva, no una auditoría total. Un integrador TOP es dueño de Shot2 y otro fresco de Shot4. La referencia corregida y el candidato optimizado se identifican por SHAs/builds reales en su entrega, no por nombres inventados aquí.

| Owner / archivos exactos | Lectura efectiva / delta |
|---|---|
| `v3/backtester/spec.go` | 1–250: catálogo, schedule, build, schemas; contrato de experimento/resolución y versionado. |
| `v3/backtester/internal/datasets/ntminute/ntminute.go` | 1–650: validación, receipts, snapshots, cursor/merge; pool y read-ahead acotados, sin perder integridad. |
| `v3/backtester/driver.go` | 1–280 y600–910: fases, scheduler, recordEconomics; batch capturado, reentrancia, índices y publicación. |
| `v3/backtester/run.go` | 1–520 y610–840: contexto, selección, preparación, admisiones/lifecycle; repairs de revisiones, schedule y payloads. |
| `v3/backtester/compose_account.go` | 1–480/EOF: seed y ReplaceAccount; generación/ownership, swap y evidencia íntegros. |
| `v3/backtester/ohlc_scheduler.go` | 1–260: lattice, skip y callbacks; invariantes/fast paths exactos y fallback. |
| `v3/backtester/ohlc_driver.go` | 1–250: fases V2, validación y WarmupReadiness; readiness/obligaciones por stream. |
| `v3/backtester/projection.go` | 1–280: snapshots, freshness, riesgo y vistas; consultas estrechas y coherentes. |
| `v3/sdk/futures/accounting/ledger.go` | 1–250,270–390,700–1125/EOF: valuación, revisiones, release y Snapshot; agregados exactos y batch de transición. |
| `v3/backtester/effects.go` | 1–230: drain y Apply compartidos; conservar orden, safety y reentrancia legítima. |
| `v3/backtester/campaign.go` | 1–900/EOF: caja/lifecycle/reemplazos/sesiones; acciones tipadas, sesiones pertinentes, primeras causas. |
| `v3/backtester/recorder.go`, `resultwriter.go` | Recorder completo; writer1–225: ownership, schema, compresión rápida y sellado. |
| `v3/backtester/cmd/echo-backtest/campaign.go` | 1–210: input monostream, composición/provenance/stdout; adaptador a entrada integrada. |
| `v3/backtester/cmd/echo-backtest/reproduce.go` | 1–290: recuperación de controles y comparador; replay de experimento/campaña. |
| `AGENTS.md`, `v3/backtester/README.md` | Routing y guía canónica; actualizar sólo README como manual. |

Owners adicionales localizados por el mapa del README, **no inspeccionados en cuerpo aquí**: `cmd/echo-backtest/main.go`, `prepare_nt.go`, `run.go`, `provenance.go`, `nt_source.go`; `finish.go`, `artifactstore.go`; `campaign_profile.go`, `functional_profile.go`; SDK `config/composition.go` y runtime público. El TOP abre únicamente sus deltas materiales; no se declara cobertura de lectura inexistente.

Archivo nuevo propuesto: `v3/backtester/experiment.go` para contrato/orquestación común y `cmd/echo-backtest/experiment.go` para parsing/reporting. Sin otro framework, servicio o ejecutable. Las transformaciones de dataset permanecen en el adapter; contabilidad en accounting; controles en runtime; el CLI no decide trades ni dinero.

Dependencias de trabajo: cerrar E-01/aceptación por manager → reparar baseline y congelar referencia comparable → integrar petición/replay y pipeline/hot path en el mismo Shot2 → falsificación independiente Shot3 → repairs y freeze/run/replay final Shot4. Es el programa autorizado, no fases o shots adicionales. No se paralelizan ediciones de los mismos owners para simular velocidad de entrega.

## 13. Matriz de falsificación y aceptación

P2 = integrador Shot2; T3 = TOP falsificador independiente; G3 = GOD adversarial; P4 = integrador fresco; V4 = TOP comprobación acotada. Ninguna fila está ejecutada por este especialista. Cada finding debe aportar SHA/binario, input/hash, reproducción mínima, impacto y expectativa independiente.

| Requisito → delta | Evidencia actual | Falsificador / oráculo | Criterio | Responsable |
|---|---|---|---|---|
| Dinero exacto → agregado incremental | Source de valuación por lotes | FIFO independiente; LONG/SHORT, parcial/reversa, fees, cashflows y marcas ausentes | Cada revisión y ambas fórmulas de día exactas; mismos errores observables | P2/T3 |
| Lecturas observacionales → APIs estrechas | Snapshot revalora/ordena | Repetir/permutar lecturas antes/después de cada causa | Cero cambio de revisiones, estado, clock, decisiones o dinero | T3 |
| Activo CONFIGURED → hot path más barato | Lattice/callbacks visibles | Referencia corregida vs optimizado en workload idéntico | Misma traza semántica completa; beneficio activo medido, no sólo warmup | T3/P4/V4 |
| Workers → merge estable | Heap `(AvailableAt,stream,ordinal)` existente | Workers1/2, entrega inversa, empates | Identidad semántica; llegada no cambia orden | T3 |
| Backpressure/cancelación | Diseño, no ejecución | Worker lento/fallido; llenar buffers y fallar Close | Progreso o fallo íntegro; sin deadlock ni resultado parcial COMPLETE | T3 |
| IDs/rutas → identidad no financiera | Venue/README documentan invariancia | Renombrar paths/labels/attempt; colisión controlada de IDs | Dinero/eligibilidad iguales o conflicto tipado explícito; no sort por IDs de orden | T3 |
| Rollover con posición → mantener A | APIs prepare/select inspeccionadas | A con posición, órdenes, claim y ciclo cuando B se selecciona | Sin migración de fill/mark/PnL ni habilitación prematura de B | T3 |
| Contraejemplo A→B → un estado vivo | Contrato financiero del mandato | Compra/burn/recompra en A antes de B; pérdida BASIC en A | Caja4760 en ejemplo de campaña; BASIC99400; contexto/técnica correctos | T3 |
| Warmup por módulo → preparación causal | WarmupReadiness inspeccionado | Modificar OHLC futuro, entrega candidata temprana y lookback distinto | No futuro; readiness legítima; cero warmup financiero duplicado | T3 |
| Gap requerido/no requerido | Fallos reportados; autoridades históricas pendientes | Hueco con posición, flat stateful, candidato futuro y cierre acreditado | Primera frontera INCOMPLETE correcta; cero datos o closures inventados | T3/P4 |
| Timers y órdenes intraminuto | Driver/fases y drain inspeccionados | Timer entre pasos; callback emite ADD/stop; empate fill/expiry | Mismo orden causal y elegibilidad posterior; no fill retrospectivo | T3 |
| Protección/adds/finality | Regresores S05 localizados por README | LONG/SHORT, tramos, parciales/duplicados, cancel/ACK/finality y pending ADD tras stop completo | Sin posición huérfana, riesgo duplicado ni claims liberados antes de finality | T3 |
| Revision batch → guard preservado | Secuencia R→R+2 localizada | Transición START_NEW_STAGE con sink propietario y no propietario | Revisiones capturadas contiguas, autoridad final correcta, sin liberar sufijo no escrito | P2/T3 |
| Reentrancia/ownership → ledger capturado | recordEconomics usa r.ledger tras callback | Recorder intenta reemplazar/admitir y retiene/muta referencias | Mutación reentrante rechazada; ninguna liberación cruzada; payload inmutable | T3 |
| Writer/Close fallido → no éxito | Contrato Recorder/Release inspeccionado | Fallar en primer/intermedio/último registro y gzip/file Close | Primera causa preservada; evidencia no perdida ni sello exitoso | T3/V4 |
| NQZ5 real → repair causal | Sólo relato de4870/4872 | Reconstruir4869–4872 y controles/cuenta2 desde cápsula; repetir con candidato | Causa física conciliada; tramo completa sólo si las fuentes lo permiten; replay íntegro | T3/G3/P4 |
| Pass-funded y nuevos términos | Fuente genera reset+transición separados | Pass latched, transición fallida, aplicada y contexto nuevo | Conteos distintos; mismas reglas; payload disponible en todos los estados | T3 |
| Cobros → libro tipado | Política requested≠collected inspeccionado | Cuarto solicitado fuera del horizonte vs cuarto APPLIED/collected; duplicado | No retiro/crédito prematuro; ecuación de caja exacta; residual separado | T3 |
| Compra/caja insuficiente | Primera compra sin chequeo visible | Caja119 y120; reintento de compra; activación que falla | Sin sobregiro inicial; débito una vez; compra≠activación | T3 |
| Replay completo → mismo driver | Reproducer actual sólo readmite controles | Burn/recompra, pass, payouts y replacement; proceso fresco | Caja/lifecycle/estados/records idénticos, no dos campañas manuales | T3/V4 |
| Composición pública → sin nombres especiales | Factories y fallback referenciados por source | Sustituir Strategy/MM; MM que cuenta cada evento/guarda máximos | Correctness preservada; fallback denso; ninguna condición por nombre | T3 |
| Usabilidad integrada → una petición | CLI monostream inspeccionado | BASIC/CAMPAIGN desde manifiesto; paths movidos; input stale/hash conflictivo | Help/stdout suficientes; rechazo preciso; cero listas paralelas/guesses | P4/V4 |
| Performance → contrato previo | Medición aislada ausente | Medir mismo workload/build/caches/recorder; contar fases y replays | Cumplir valores congelados tras E-01; no comparar aborto vs completo | P4/V4 |
| Cobertura total → reporte por obligaciones | Segmentos15,6% reportados | Contrastar expected/observed/unknown con corpus/autoridades | Ningún agregado de segmentos se llama trayectoria continua | G3/P4 |

Se reutilizan los regresores causales, de invariancia de IDs, read models, campaña, composición pública y protección enumerados en README. El TOP valida sus nombres/fixtures exactos antes de ejecutarlos. No se reaudita D1–D6 entero ni se confunde lectura de tests con ejecución.

## 14. Gates, delta del manager y cierre del especialista

| Gate del programa | Estado de entrada/conclusión disponible |
|---|---|
| Correctness | FAIL en baseline por fallos comunicados y mecanismo estático localizado; candidato NOT_DEMONSTRATED, sin pruebas ejecutadas. |
| Performance | NOT_DEMONSTRATED; E-01 impide congelar números defendibles. |
| Usabilidad integrada | FAIL en baseline: CLI monostream y replay incompleto; candidato NOT_DEMONSTRATED. |
| Cobertura | FAIL respecto del objetivo reportado de horizonte completo; no verificado físicamente aquí. Cobertura alcanzable bajo schedule nuevo NOT_DEMONSTRATED. |

`PHYSICAL_RUNTIME_READINESS` queda fuera. No hay certificación LIVE, D6, broker, ejecución real, despliegue o cambios de permisos.

### Delta compacto propuesto para BTG-PLAN.md

BTX-PERF-S01 devuelto como CANDIDATE_BLOCKED_EVIDENCE. Partición decidida: preparación/lectura por stream con pool máximo2, C_modalidades=1, merge causal y estado financiero continuo. Repairs: batch de revisiones/ownership, payloads de admisión, reemplazos/caja y replay de experimento; multicontrato requiere además corregir quiescencia frente a schedule futuro y sesiones/identidad del contrato seleccionado. Hot path: valuación exacta incremental, consultas estrechas, índices y gzip BestSpeed. E-01: faltan cápsula/recibos y probe aislado; MAX_WALL/MIN_SPEEDUP/MAX_RSS/throughput no congelados. Shot2 NO autorizado por este diseño. Próximo paso único: manager obtiene la cápsula mediante acceso ya autorizado, adjudica el probe y congela el contrato o mantiene bloqueo dentro de los cuatro shots. PASES=UNRESOLVED. Reloj180m=UNKNOWN; techo calendario original intacto. Primary session permanece abierta.

### Feedback y cierre por delta

Feedback preparado para `80-agents/journal/feedback/system-1/2026-10-08-echo-futures-btx-perf-session-feedback.md`, PENDING_WRITER. Lo útil fue el mapa del README y el acceso a source fijado: permitieron localizar la secuencia de revisiones y dos defectos de replay sin inventar ejecuciones. La fricción fue el despacho de un diseño con contrato numérico sin cápsula/perfiles ni runner acreditado. El relato de evaluación no puede suplir hashes y outputs. La memoria interna no aportó autoridad física adicional y no se promovieron sus contenidos a evidencia de producto.

Pain pattern candidate único: entregar una cápsula mínima verificable y un recibo de capacidad del runner antes de solicitar objetivos numéricos a un especialista CLOUD. Promoción L3: diferida al manager; no se cambian skills ni políticas globales. Evaluación propia: utilidad de source4/5, preparación del handoff de evidencia2/5; son scores operativos del agente, no benchmark ni evaluación del producto. Eficiencia de contexto REVIEW: varias respuestas de source llegan como JSON de una línea y obligan a lecturas por rango; preferir extracción por símbolo cuando la superficie la permita, sin recortar evidencia necesaria. Tokens/high-water/cache metrics UNKNOWN.

Agent-run: existe un segmento atribuible de revisión estática de source y diseño correctivo, no generación ni ejecución de código. Registro preparado para el escritor conforme a la skill: superficie canónica `[[ChatGPT]]`, tarea source-review/design, outcome CANDIDATE_BLOCKED_EVIDENCE, verification STATIC_SOURCE_ONLY, user_rework UNKNOWN; un solo segmento, sin inventar tests o TOP. Identidad comunicada por la superficie: GPT-6 Astra Pro; identificador de ejecución auditado/tokens/consumo no expuestos: UNKNOWN. PRO_CHAT_POOL_DELTA=UNKNOWN; no se suma1 por el rol GOD.

El vault/materializador no está montado ni se ejecutó la materialización canónica. Se entrega contenido completo y delta al escritor del manager; no se copió frontmatter manualmente, no se escribió en otra rama, no se hizo commit ni se declaró sincronización del vault. El feedback y el agent-run canónicos quedan PENDING_WRITER. No se crea L0/L1/L3 ni un nuevo plan por rutina. Esta devolución termina la sesión ONE-SHOT del especialista; el cierre persistido en Agents-OS queda pendiente del escritor y no cierra al Primary Manager.

por favor gracias

## Fuentes

- Adenda Owner de esta sesión,2026-10-09: aceptación técnica S01 y autorización S02 TOP LOCAL con excepción de secuencia de performance; autoridad vigente sobre estados históricos del especialista.
- Entrega original S01 recuperada de Library, identidad y SHA256 arriba. Original de transporte preservado sin sobrescritura.
- Registro remoto E1 `52d17ce92321fe0673eeaf1ed59d7e8753d47af7`, `main/80-agents/journal/logs/2026-10-08-btx-perf-s01-e1-local-probe.md`; no contiene la cápsula física.
- [[BTG-PLAN]]: control único y mandato activo.

Materialización documental: envelope generado con materialize_schema_note.py original, blob067dbef8afca0f3918b1435b83267f547f462bc4; validador original blob7f6e9227ab11f2aac8a1bec135775bbd852d016c y template doc blobc0f0aa58e007fcca52591cabcb32e091297ff437. Ejecución en copia documental sandbox sobre proyección exacta de los campos consumidos para type=doc del contrato27e59b8b1e9044ded50e5cfef4474c6e3ed59b95; no lint global ni sincronización física de Daedalus. No cambios al materializador, templates o contrato remotos; no ejecución de producto por Primary.
