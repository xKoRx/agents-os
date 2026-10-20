---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — Execution Client y Feed Batching]]"
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-20"
updated: "2026-10-20"
---

# EXECUTION-FEED-BATCHING-DESIGN

## Propósito

**FEFB V1 — IMPLEMENTATION_READY, 2026-10-20.** Mandato de KoR: resolver conjuntamente el costo de serialización del runtime y el cliente Execution NinjaTrader con capabilities/colas compartidas conceptualmente con MT4/MT5. Esta especificación es funcional y técnica; el planificador es [[Echo Futures — Execution Client y Feed Batching]]. Autoriza el alcance de implementación, no aceptación de producto, deploy ni órdenes. Sustituye la propuesta aislada de RESUME-06 para estas dos fronteras; no reabre el dominio de Runtime Pools ni sus gates históricos.

## Contenido

### 1. Hechos, límites y resultado requerido

Corte de lectura: `xKoRx/echo@112ccccdbbf32bc3ca486fd04a28ab0afa0451a4`, rama `feature/ef-runtime-pools`. RESUME-05 reportó 46,1 registros/s entrantes y 20,5 procesados; estabilidad sin timeouts pero datos stale. La captura de prueba contenía 925 QUOTE y 76 TRADE, no 1001 velas. El perfil local atribuyó el costo al bundle JSON de estado, cuyo sequencer maduro pesa aproximadamente 2,1 MB. Son mediciones del frente LOCAL, no reejecuciones del diseñador CLOUD.

Lectura de source: `market_stream` conserva un store completo por envelope y memo de load por storage/request; MT5 tiene `SendUnifiedBatch`, `MessageQueue` y configuración dinámica; MT4/MT5 comparten el blob de `EchoQueue.mqh`. `ClientConfig.SnapshotIntervalMs` valida 100–10000 ms: **no reutilizar ese campo para imponer 50 ms y romper legacy**. El `ClearSent` visto depende de una escritura al pipe, no prueba un ACK durable de Kafka. La nueva fiabilidad no se presume heredada.

Resultado: todos los ticks por defecto y todas las barras configuradas llegan por lotes ordenados; el Bridge no interpreta economía ni selecciona muestras; Core aplica todos los eventos sin pagar la serialización grande por cada uno. Un modo explícito de último tick por ventana también queda implementado y probado. Reutilizar módulos existentes; no comprar infraestructura para esconder el costo.

### 2. Decisiones congeladas

| ID | Contrato |
|---|---|
| D1 | Strategy, MM, indicadores y política de cuentas conservan su dominio. Strategy nunca depende de cuentas ni se pausa por ellas. |
| D2 | Batch es agrupación SIN pérdida. Sampling es otro contrato opcional. Default de feed = ALL. |
| D3 | Barras cerradas y correcciones de TODOS los timeframes suscritos se entregan siempre, aunque ninguna Strategy los consuma. |
| D4 | Configuración Echo decide suscripciones, intervalos y modo; cliente los ejecuta; Bridge transporta, no decide. |
| D5 | Un solo productor autorizado por stream/fuente/epoch. Feed independiente del número de cuentas/pools. |
| D6 | Cola durable del cliente para entrega; estado de Core sigue bajo la transacción request/reply de StateFun. Prohibido ACK de procesamiento con persistencia en una cola no coordinada. |
| D7 | Una autoridad de orden por stream. Conservar secuencias/epochs; no dividir artificialmente una misma key para ganar rendimiento. |
| D8 | Reutilizar ClientConfig, negociación, sesión, mensajes y sender existentes donde encajen; extensiones aditivas y versionadas, sin reescribir MT4/MT5. |
| D9 | Bridge dummy en negocio, no en garantías: conserva autenticación, routing, M2, fencing, journal y reconciliación. |
| D10 | Tres shots: implementar, auditar independiente, corregir. Manager acepta gates; ninguna sesión autoacepta o despliega. |

### 3. Arquitectura y responsables

```text
Configuración Echo versionada / catálogo de capabilities
                       ↓ handshake/config aplicada y confirmada
Execution Client NinjaTrader (única instancia)
  capabilities: feed ticks, feed bars, estado/ejecución, control
       ↓ colas por capability + identidad/orden al capturar
  sender común: límites + flush configurable + outbox/retry/ACK
                       ↓ transporte negociado existente
Bridge/adaptador: autenticar → validar envelope → routing → Kafka
                       ↓ batch de feed preservado por stream
market_stream: cargar → aplicar TODOS en orden → sellar estado/efectos
                       ↓
market_analytics: barras nativas completas / indicadores compartidos
                       ↓
Strategy → Signal → ejecución por cuenta/MM → Bridge → Ninja
```

| Owner | Hace | No hace |
|---|---|---|
| Config/control Echo | Contrato versionado, suscripciones, política ticks, límites, resolución física | No lo decide el Bridge por presión de carga |
| Capability de feed NT | Captura datos nativos, normaliza representación, recupera barras, aplica reducción configurada | No indicadores, señales, targets/DD ni asignación de cuentas |
| Transporte cliente | Colas, orden, lotes, disco/reintentos, negociación y ACK | No decisiones de trading |
| Bridge | Validación técnica, identidad, routing, publicación durable y retorno de ACK; ejecución M2 existente | No calcular barras/indicadores, no sampling, no selección económica |
| Market/Core | Canonicalización, integridad, dedup, frescura y persistencia por lote | No volver a confirmar datos que no quedaron bajo autoridad durable |
| Analytics | Cálculo único por demanda; barra/observación y corte causal | No saldo ni pool |

Compartir capabilities significa un contrato común y adaptación de terminal, no prometer reutilización binaria entre MQL/C#/Go. Se mantiene el transporte NT actual y su adaptador salvo incompatibilidad demostrada: no imponer Named Pipes ni crear un tercer bridge. El módulo común de configuración/decodificación puede ser reutilizado por los binarios existentes; no un nuevo framework de plugins.

### 4. Configuración y negociación

Extensión nueva propuesta del contrato común: perfil `feed` versionado, separado del intervalo legacy de snapshots. Nombres de campos siguientes son contrato de este diseño a implementar, no flags CLI ya disponibles. Reutilizar los nombres equivalentes existentes encontrados en el source y registrar el mapeo exacto en T1.1; no inventar dos autoridades.

| Campo | Semántica V1 |
|---|---|
| `config_version` | Aplicación prospectiva; config recibida no equivale a aplicada; ACK con versión efectiva |
| `feed.subscriptions` | Fuente/símbolo canónico/contrato físico/calendario y lista explícita de timeframes; soporte nativo anunciado |
| `transport.flush_interval_ms` | Default 50 ms; rango técnico validado 1–1000; es edad máxima objetivo de espera de cola, no sleep por evento |
| `transport.max_batch_events` | Default 256; límite validado positivo |
| `transport.max_batch_bytes` | Default 1 MiB; mensaje individual excesivo falla visible, jamás truncado |
| `transport.outbox_max_bytes` | Límite finito explícito de despliegue; pruebas con límite pequeño para forzar backpressure; sin crecimiento ilimitado |
| `feed.ticks.mode` | ALL o LAST_PER_WINDOW; default ALL; valor desconocido se rechaza |
| `feed.ticks.window_ms` | Sólo LAST_PER_WINDOW; default 50 ms; independiente del flush; validado positivo |
| `feed.bars` | Cierres y revisiones lossless para cada suscripción; NO tiene sampling |

Los valores de transporte son defaults técnicos nuevos y tuneables, no parámetros financieros. Validar límites coherentes y configuración completa antes de activar. Los controles de ejecución/allowlist actuales siguen siendo condición separada; conectar feed no arma trading. Un cliente sin la capability nueva mantiene wire/semántica legacy; solicitarle un feed que no soporta produce UNSUPPORTED, no degradación silenciosa. Nueva capacidad de batch confiable y feed se negocia; no afirmar que MT antiguo ya produce ticks nativos o ACK de broker.

Config de ticks ALL y LAST no puede alternar sin barrera/versiones. Vaciar pendientes de versión anterior antes de confirmar la nueva, o rechazar actualización temporalmente con causa. Cada registro lleva su versión; no reetiquetar datos históricos.

### 5. Colas, orden, lote y entrega

Cada capability encola sin bloquear trabajo del terminal con una escritura de red. En captura se asignan `source_epoch`, `stream_seq` y timestamps de evento/observación. Un stream de feed agrupa ticks y barras del mismo símbolo/contrato/fuente; una lane de ejecución usa su identidad de cuenta. El sender mezcla colas por secuencia dentro del mismo ámbito, no por orden arbitrario de las listas ni ordenando timestamps retrospectivamente. No se promete orden total entre streams/cuentas independientes.

Envelope compartido v1, añadido al mecanismo de batch existente: versión, producer/session/epoch, config_version y grupos ordenados. Cada grupo tiene stream/lane, rango de secuencias, identidad/digest estable e items tipados con event_id, event_ts, captured_at, payload y provenance. El mapping exacto reutiliza tipos ya existentes. El Bridge agrupa/ruta mecánicamente por el stream declarado; no cambia orden ni payload económico. Un grupo market-data se conserva como mensaje de lote hasta `market_stream`; no deshacerlo en Kafka en miles de invocaciones costosas.

Flush al primer límite: tiempo, cantidad o bytes. Una ráfaga genera sublotes contiguos limitados; nunca sleeps acumulativos. Una sola escritura activa por lane evita interleaving. Datos de ejecución/control no quedan detrás de una cola ilimitada de quotes: usar lanes existentes y dispatch inmediato para comandos/protección/fencing y resultados críticos. No convertir la capacidad de tick sampling en pérdida de órdenes o fills.

La outbox usa un registro append-only local acotado y cursor ACK; reutilizar la persistencia existente cuando cumpla el contrato. No copiar el límite fijo de 64 mensajes ni la reescritura completa de archivo de MT para el hot path de ticks. Un lote entregable se sella durable antes de enviarlo. Hasta su ACK durable se conserva byte-idéntico para retry. El Bridge envía ACK sólo cuando todos los grupos cubiertos quedaron confirmados por Kafka o la autoridad durable existente documentada; éxito de socket no basta. Publicación parcial o ACK perdido produce reentrega, no omisión: identidades internas estables permiten dedup. No se promete transacción global entre varios topics ni exactly-once de un terminal físico.

Dos fronteras distintas: ACK Kafka permite retirar la outbox del cliente; checkpoint StateFun controla el procesamiento. Ninguno implica que hubo trade. Que el cliente confirme un snapshot de cuenta tampoco confirma una orden.

Ante saturación: detener la aceptación en la cola afectada o pasar al spool acotado; error/counter y estado incompleto, nunca descartar silenciosamente barras/fills. Ante crash antes de captura durable o pérdida de ticks no recuperables del proveedor, registrar gap/epoch y degradar readiness; ALL significa no descartar deliberadamente los ticks disponibles, no inventar una garantía sobre datos que el terminal/proveedor nunca entregó. Cierres de barras deben recuperarse desde historia nativa cuando esté disponible.

### 6. Política de ticks

ALL conserva todos los QUOTE/TRADE recibidos. En cada ventana se despachan todos en orden. El formato distingue cambios bid/ask de trades y conserva timestamp/volumen: Last no es precio ejecutable.

LAST_PER_WINDOW retiene la última observación por `(fuente, contrato, clase)` en ventanas event-time semiabiertas `[inicio, fin)`, duración configurada, emitidas sólo cuando finalizan y hay datos. QUOTE reconstruye el último estado bid/ask con timestamps de cada lado; TRADE retiene el último trade, sin fingir volumen agregado. Metadatos de ventana: cobertura, rango de secuencias de origen y cantidad intencionalmente omitida. Late event fuera de la ventana cerrada no reabre una decisión: se etiqueta y trata por el contrato de correcciones. Epoch/cambio de config cierra la ventana previa explícitamente. Reloj desconocido/skew fuera de bounds impide una muestra declarada fresca.

Ordenar los representantes retenidos por su secuencia; la proyección reducida tiene secuencia propia y conserva rangos de origen para distinguir sampling de pérdida. No dejar que el último QUOTE suprima un TRADE de otra clase. Heartbeat no renueva event_ts de un precio viejo.

La política se configura por suscripción de feed, nunca por cuenta. Strategy/MM que exigen todos los cruces no son compatibles con LAST; la composición rechaza la combinación o usa la fuente ALL existente, sin multiplexar políticas improvisadas. En esta entrega no se declara por defecto que S1 o los MM actuales toleran LAST. Se implementa el modo y se prueba; sólo consumidores que lo declaren explícitamente pueden utilizarlo. Backtest/replay registra versión y resolución recibida; resultados de ALL y LAST no se presentan como equivalentes.

### 7. Barras nativas y recuperación

La capability NT utiliza la API nativa de barras (validada contra las assemblies instaladas) para todas las suscripciones/timeframes declarados. No recalcula indicadores en el terminal. Timeframes configurados y anunciados, no una lista infinita implícita; timeframe no soportado se rechaza durante negociación. Ninguna barra se elimina porque la Strategy actual no la consume.

Identidad: fuente/contrato/calendario/timeframe/bucket de apertura; cierre, OHLCV, revisión, estado forming/closed, event_ts y available_at observados. Un cierre o corrección no se sobrescribe en la cola como si fuera una quote. Forming es opcional, separado del contrato obligatorio de cierre. No fabricar un cierre basado solamente en el reloj cuando la fuente no lo acredita.

Bootstrap/reconexión: anunciar cobertura y último cierre confirmado → solicitar intervalo faltante → solapar historia y live con dedup/revisiones → emitir barrera de cobertura → declarar serie utilizable. Un silencio durante pausa/sesión o ausencia de trades se evalúa con calendario y semántica nativa, no se rellena automáticamente. Si la historia no está disponible, gap persistente y causa visible; sólo decisiones que dependan del dato incompleto permanecen bloqueadas.

No construir OHLC desde ticks LAST. Una barra nativa y otra agregada internamente no compiten con la misma identidad. Configurar origen NATIVE frente a TRADE_AGGREGATED y mantener el camino legacy intacto. La activación del camino nuevo requiere coherencia de calendario y comparación golden; backfill/correcciones no reejecutan señales antiguas. La entrega de datos y la decisión técnica siguen en sus propietarios existentes.

### 8. Serialización y persistencia: solución concreta

No se crea una cola asíncrona de persistencia de Core ni se responde éxito antes de sellar su resultado. `Storage.Set` prepara las mutaciones que viajan en la respuesta al runtime; StateFun sigue siendo la autoridad de checkpoint y retry. Serializar no es sinónimo de fsync a disco por tick.

**Camino principal V1 sin fork de SDK:** `market_stream.Invoke` admite un lote canónico de eventos de UNA key, además del envelope singleton legacy. Valida estructura/identidad, carga el estado una vez, aplica secuencialmente cada entrada al mismo engine y encola sus efectos inmutables; serializa únicamente el estado final sucio una vez antes de devolver éxito. Cada evento conserva secuencia, causalidad y journal/efectos; no sólo el último evento. Un error no deja una respuesta exitosa parcial ni un estado mutable que sobreviva para contaminar el retry. El batch original reentregado converge a las mismas identidades.

Esto establece una frontera real implementable con los APIs actuales, sin suponer un hook de fin de request que no se ha inspeccionado. La agrupación adicional de StateFun puede agrupar varios lotes en su request HTTP. Durante T1.1 el implementador inspecciona el SDK pinneado v3.3.0: sólo se permite ampliar la coalescencia a toda esa request si existe un punto soportado y probado ANTES de construir su respuesta. No sustituir el dispatcher completo ni forkar SDK. Sin ese punto, se mantiene la transacción del lote de aplicación; no se llama al estado «persistido al final de request» por conveniencia.

**Condición de capacidad obligatoria:** reducir llamadas no basta. Medir con flush 50 ms real, estados maduros, carga open-loop y recuperación de backlog. Si el lote de aplicación aún queda corto, está autorizado compactar/versionar la representación del sequencer dentro del MISMO owner y sus ventanas lógicas, con lector de estado anterior, pruebas de migración y rollback seguro. Elegir una única representación mínima, no un sistema de sharding. No reducir ventanas, ignorar conflictos ni aumentar timeout/freshness. Conservar el singleton legacy para compatibilidad y demostrar recuperación de su backlog sin saltos; no basta medir sólo lotes nuevos vacíos.

Snapshots y efectos por evento se copian/sellan cuando se generan: nunca apuntan a un bundle que continúa mutando. Comparación de lotes 1/2/50/1001 sobre la misma secuencia exige mismo estado lógico, identidades, efectos y orden. Tiempo de llegada/availability se mantiene real: el batch añade latencia de transporte, no autoriza backdating para simular disponibilidad anterior. Failure/retry/restore deben probarse usando el RequestReplyHandler real, no sólo un mock que guarda punteros.

### 9. Bridge y compatibilidad

Primero mapear source real: ClientConfig, negociación, batch unificado, registros de tipos y Kafka producer. Extender esos contratos; no un segundo catálogo independiente para NT. El adaptador C# ejecuta las capabilities que soporte y anuncia las que no. Mantener snapshot_interval_ms legacy y agregar flush de transporte negociado; 50 ms no se introduce eludiendo el validador de 100 ms existente.

Bridge no muestrea ticks ni decide targets/DD; valida envelope, publica por key y devuelve ACK. Productor Kafka debe preservar orden por lane/partición también bajo retry; configuración efectiva e idempotencia verificadas. El control de secuencia en Core detecta anomalías que no soluciona un simple array ordenado. Nuevos tipos de lote deben quedar consumidos por rutas reales declaradas; tests dependientes de ambos manifiestos, no enqueue directo en harness.

No retirar M2, fencing o evidencia de drenaje: son garantías de ejecución/transporte, no MM. No hacer merge de los binarios Forex/Futures en este alcance. Fixtures comunes prueban capacidades/mensajes compartidos; contratos específicos de futuros continúan donde pertenecen. MT4/MT5 y clientes antiguos deben producir el mismo comportamiento anterior cuando no negocian v1.

### 10. Implementación por superficie

| Superficie existente | Acción autorizada |
|---|---|
| `v3/core/internal/functions/futures_market_stream.go`, types y tests | Entrada de lote, estado y efectos; compatibilidad singleton; costo de serialización |
| `v3/sdk/futures/market`, `analytics`, `bars`, `marketctx` | Contratos mínimos de batch/barra nativa/política y lectores; no cambiar kernels matemáticos |
| `v3/core/internal/functions/futures_market_analytics.go`, strategy serving | Conectar cierres nativos, coverage/revisión y consumidores; no dominio financiero nuevo |
| `v3/sdk/domain/client_config.go`, `v3/sdk/ipc`, `v3/sdk/messaging` | Extensión negociada/configuración/fixtures comunes; preservar legacy |
| `v3/clients/mt4`, `v3/clients/mt5` | Referencia y pruebas de compatibilidad; sólo cambios aditivos imprescindibles, no reescritura |
| `v3/bridge/internal` y `v3/futures-bridge` | Reutilizar decoder/routing y adaptar transporte NT/outbox ACK, preservar M2 |
| AddOn C# y tests de plataforma en el árbol actual de futures-bridge | Capabilities, cola/sender, ticks, barras/backfill y configuración; una definición instalada |
| `futuresruntime`, `echo-core`, `sdk/statefun`, module.yaml source | Registro/dispatch/tipos y composición; no aplicación a clúster |
| Testkit/harness existentes | Pruebas Kafka/StateFun aisladas, NT compilación aislada y rendimiento |

Nombres de archivos nuevos se fijan en T1.1 junto al propietario existente; eso es una decisión técnica ordinaria, no permiso para expandir arquitectura. El inventario de interfaces es un anexo en este diseño, no otra SPEC. Dos workers nunca escriben simultáneamente el mismo archivo.

### 11. Pruebas y aceptación

La matriz ejecutable y evidencias viven en [[EXECUTION-FEED-BATCHING-VERIFICATION]]. Se exige: lote lossless, modo reducido explícito, barra perdida recuperable, persistencia/dedup ante caída, old-client compatibility, efectos inmutables y medición real de capacidad. Porcentajes de coverage no reemplazan oráculos funcionales; >=95% del código nuevo después de cubrir fallos críticos. Baselines históricos se identifican por caso/causa.

Capacidad objetivo: carga capturada de un símbolo en ALL con flush50ms, estado maduro y productor open-loop; recuperación de backlog mientras continúa la llegada. Incluir replay 2× como headroom de laboratorio y ráfagas capturadas, sin repartir la misma key. Prueba sostenida aislada >=30min, >=3 checkpoints reales si hay runtime aislado, sin timeouts/restarts y sin edad sostenida fuera del bound existente. Repetir con varios streams/cuentas para confirmar que feed/analytics no crecen por cuenta. Un test in-proc no certifica el runtime Java ni un terminal instalado.

La compilación C# debe comprobar el conjunto completo en perfil/staging aislado contra assemblies reales cuando estén disponibles; una compilación de archivo aislado no acredita instalación. Si faltan toolchain/assemblies/entorno aislado, explicitar PHYSICAL_NOT_DEMONSTRATED y el gate correspondiente; no modificar el terminal del Owner. No se disparan órdenes reales ni SIM compartidas en estos tres shots.

### 12. Migración, rollout y fuera de alcance

Desarrollo en la rama runtime vigente con worktree dedicado y commits atribuibles; no master de producto ni rama backtester. Agents-OS directo a master. La base congelada se verifica antes de escribir; avances ajenos se concilian, nunca reset.

Migración aditiva: negociación v1 antes de publicar lotes; consumidor batch-ready antes que productor; backfill/corte prospectivo con egress desarmado; confirmar única autoridad por stream; instalación del único AddOn in-place, respaldo fuera de Custom. No reemplazar checks físicos por logs «config loaded». Cerrar tarea de documentación con procedimiento exacto de copia/carga/rollback. Sin despliegue automático al cerrar G3: después se retoma CERT-NT-01 bajo un mandato operativo separado.

Defer: topic compactado latest como optimización de vistas, reducción de ticks por defecto, order book/DOM nuevos, portfolio optimizer, migración masiva de MT, servicios/DSL nuevos, SDK fork, infra extra y trading en cuentas del Owner. No modificar el backtester en paralelo; sí entregar fixtures/contratos para su convergencia posterior. No relajar las responsabilidades de R6.

## Fuentes

- Mandato explícito KoR 2026-10-20: dos frentes, cliente Execution NT con capabilities/colas existentes, Bridge dummy, barras completas y ticks configurables; tres shots.
- [[Echo Futures]], [[Echo Futures — Runtime Pools]] (RESUME-05) y [[ECHO-FUTURES-RUNTIME-POOL-DESIGN]] (R6): autoridades relacionadas; sus mediciones son reportes locales fechados, no ejecución de esta sesión.
- Source `xKoRx/echo@112ccccdbbf32bc3ca486fd04a28ab0afa0451a4`: `v3/core/internal/functions/futures_market_stream.go`; commit 112ccccd; `v3/clients/mt5/execution_agent_v3.mq5` (SendUnifiedBatch/BatchIntervalMs), `mt4`/`mt5/EchoQueue.mqh` (blob común 2c899ce1d06281adbc16aa9b9895222b5f4d5d36); `v3/sdk/domain/client_config.go` (blob 587eb5c4db63b101c9f6b672230a4a7769d4e02a); `v3/bridge/internal/pipe_handler.go`; `v3/futures-bridge/addon-ninjatrader/EchoExecutionAddOn.cs`; `v3/core/go.mod` (Go SDK StateFun v3.3.0).
- [Apache StateFun Go SDK](https://nightlies.apache.org/flink/flink-statefun-docs-release-3.2/docs/sdk/golang/) y [HTTP endpoint](https://nightlies.apache.org/flink/flink-statefun-docs-release-3.2/docs/modules/http-endpoint/): modelo de state y request/reply; comprobar detalles de SDK pinneado localmente, no inventar hooks.
- [NinjaTrader BarsRequest](https://ninjatrader.com/support/helpguides/nt8/barsrequest.htm): API de datos nativos, no lógica de indicadores.

Las secciones 2–12 son decisiones de diseño a implementar y probar, no afirmaciones de capacidades ya disponibles. No se ejecutó código de producto ni se certificó infraestructura desde CLOUD.
