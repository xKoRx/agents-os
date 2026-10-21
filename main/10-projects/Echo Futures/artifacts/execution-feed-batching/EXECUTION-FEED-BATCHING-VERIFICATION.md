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

# EXECUTION-FEED-BATCHING-VERIFICATION

## Propósito

Matriz de aceptación FEFB V1, no planificador alternativo. Tareas/gates en [[Echo Futures — Execution Client y Feed Batching]]; contrato en [[EXECUTION-FEED-BATCHING-DESIGN]]. Estado inicial de TODAS las pruebas: **NOT_RUN**. Ningún PASS se infiere de la existencia de una interfaz o de una suite histórica.

## Contenido

| AC | Invariante / prueba con oráculo independiente | Owner S1 | Evidencia mínima | Estado |
|---|---|---|---|---|
| AC01 | ALL: reconstruir exactamente todos los eventos capturados y orden por stream con flush1/50/100ms, fragmentación por bytes/eventos y cola concurrente | W2/W3 | Lista de IDs/payload/hash antes-después; cero omitidos/truncados | PASS_S1 |
| AC02 | LAST: conservar representante correcto por clase y ventana, metadatos de omisión y timestamps; QUOTE no borra TRADE; cierre de ventana/config/epoch | W2 | Traza manual con evento en borde, tardío, bid/ask separados y heartbeat; assert ALL incompatible rechazado | PASS_S1 |
| AC03 | Cierres/revisiones de todos los timeframes configurados aunque no haya Strategy suscrita; ninguna vela desde ticks reducidos | W2/W4 | Fuente NT controlada multiTF, oracle OHLCV/revisión/calendario; formando != cerrado | REOPENED_MR1 (Manager: JSON-parseable ≠ AC03; era PASS_CONTRATO_S1) |
| AC04 | Gap de barra/desconexión: backfill solapado, dedup y barrera de cobertura; no señales retroactivas; ausencia real de historia permanece explícita | W2/W4 | Eliminar un cierre y recuperarlo; calendario pausa/no-trade; READY sólo tras cobertura | REOPENED_MR1 (Manager: era PASS_CONTRATO_S1) |
| AC05 | ACK durable: caída antes/después de Kafka ACK, perdida de ACK al cliente y publicación parcial conservan/reenvían sin pérdida | W2/W3 | Outbox/disco y producer capturado; ACK de socket no libera; IDs estables a través restart | REOPENED_MR1 (Manager: PublishSync sin reiniciar cliente no cierra; era PASS_S1) |
| AC06 | Backpressure: memoria/disco finitos, sin descarte silencioso, feed no estrella cancel/close/results; identidad por lane | W2/W3 | Límites pequeños, saturación y recuperación; no lote que exceda cap; fallo visible | PASS_S1 |
| AC07 | Procesamiento en lote: misma secuencia dividida 1/2/50/1001 produce mismo estado lógico y efectos por evento, no sólo último estado | W1 | Diferencial engine+RequestReplyHandler reales, JSON canónico cuando mismo encoding; cero alias mutable | PASS_S1 |
| AC08 | Persistencia/retry: fallo a mitad/antes del reply, respuesta perdida, restore en otra instancia, varias keys/requests intercaladas | W1 | Reinicio sin caches; no success parcial, ningún estado no commitado contamina retry; race | PASS_S1 |
| AC09 | Serde grande no escala una vez por tick dentro del lote; estado maduro conserva ventanas/identidad/conflictos y puede migrarse/volver | W1 | Contadores de codec, perfiles y fixtures checkpoint previo/candidato; rollback leído de verdad | PASS_S1 |
| AC10 | Config común: handshake/hot-update/unsupported, feed50ms distinto de SnapshotIntervalMs legacy100ms, configuración recibida vs aplicada | W2/W3 | Fixtures legacy MT4/MT5 y NT; unknown fields/version, config inválida no arma; defaults previos intactos | PASS_S1 |
| AC11 | Bridge dummy: no sampling/bar/indicator/MM logic; routing/idempotencia/Kafka conservan orden y M2/fence intactos | W3 | Pruebas de wrong-account, retries y comandos obsoletos; revisión dependencias + integración M2 anterior | PASS_S1 |
| AC12 | Recorrido real de tipos/rutas: sender cliente→bridge→Kafka→manifiesto→Core→analytics sin desempaquetado que pierda ventaja | W4 | Parser y dispatch productivos; desconectar tipo/topic/target hace fallar test; dos manifiestos fuente | REOPENED_MR1 (Manager: tramo Core→analytics sólo no cierra; era PASS_S1) |
| AC13 | Capacidad ALL50ms con estado maduro, llegada independiente, replay1×/2× y ráfagas, backlog inicial mientras llegan nuevos datos | W1/W4 | Serie tiempo ingress/processed/lag/age, P50/P95/P99, CPU/GC/heap; >=30min y checkpoints aislados; no sampling oculto | PASS_S1_INPROC (checkpoints runtime aislado NOT_RUN) |
| AC14 | Freshness y causalidad: recibir backlog no permite entradas; disponibilidad real del batch, revisiones no miran futuro, skew no se oculta | W1/W4 | Permutaciones eventos/timers/mismo instante, replay y política incompatible; egress desarmado | PASS_S1 |
| AC15 | NT: una definición de clase en instalación aislada, parser válido, native bars API compilada, multi-binding único feed y resultados ejecución | W2/W4 | Hash del conjunto + compile con assemblies reales; callbacks/harness SIM identificados; si falta entorno, NOT_DEMONSTRATED | PHYSICAL_NOT_DEMONSTRATED (compile) |
| AC16 | Integración final: baseline heredado identificado, cero nuevas regresiones, >=95% código nuevo, límites físicos/migración y documentación instalable | Submanager/W4 | Comandos+exit+logs, cobertura denominador completo, SHA exacto, diff y working trees intactos | PASS_S1 |

### Registro de una ejecución

Cada fila requiere SHA de código/config, dataset/captura/clock, comando, exit, fecha, operador/modelo, artefactos durables y resultado observado. No registrar PASS por texto del worker sin revisión. El conteo de mensajes Kafka no equivale a eventos procesados: separar registros/lotes/items/admitidos/dedup/rechazados/corregidos. Comparar lag y event age, no sólo RUNNING.

La emisión no se confirma al cliente por el progreso de Core: son ACKs distintos. Incluir pruebas que rompen deliberadamente cada confirmación en un sandbox desechable. Nunca ejecutar esas mutaciones contra DEV compartido.

### Evidencia por gate

G1: implementación y matriz completa para review; requisitos críticos faltantes = blocked, no se patean a S3. G2: auditoría fresca crea reproductores y distingue DEFECTO_CONFIRMADO / GAP_DE_VERIFICACION / LIMITACION_FISICA. G3: fixes adjudicados más regresiones, mismo universo de cobertura y restore; manager acepta, no el ejecutor.

Cada hallazgo Fxx incluye requisito, severidad, SHA, archivo/símbolo, expected/actual, repro rojo en candidato y escenario corregido. Cambiar fixture interno puede justificarse cuando el comportamiento nuevo lo exige; el oráculo de usuario no se debilita.

### Certificación operacional posterior

Estos tres shots no aplican manifiestos, reinician el terminal del Owner ni operan Sim101/props. Laboratorio Kafka/StateFun aislado y compilación real aislada no equivalen a integración física certificada. Tras G3 accepted, CERT-NT-01 necesitará identidad de release/config, única instalación del AddOn, consumo de mercado fresco, productor económico, gateway NT y recuperación observados. Toda autorización de armado sigue separada; C2 no acepta datos stale.

## Fuentes

[[EXECUTION-FEED-BATCHING-DESIGN]] §§2–12; experiencia de [[Echo Futures — Runtime Pools]] S02–S04/CERT-NT-01 y mandato Owner. Esta matriz contiene oráculos futuros, no resultados heredados elevados a PASS.

## Evidencia S1 — G1 (2026-10-21, submanager GLM-5.3-Flash)

SHA integrado y publicado: `1af0352f8cbd4e33f28cc1b194283fe77112b9d4` (`origin/feature/ef-runtime-pools`, FF desde `112ccccd`, sin force; worktree limpio). Commits: W1 `b3e3190a` (core batch), W2 `7c34f840` (contratos cliente), W3 `90b23ffb` (bridge + reparación W3-R), W4 `1af0352f` (integración). Todas las suites re-corridas por el submanager antes de integrar; ningún PASS aceptado por reporte verbal.

| AC | Evidencia principal (test → qué prueba) |
|---|---|
| AC01 | W1 `TestFEFBAC07BatchEquivalenceOverRealHandler` (1200 eventos, lotes 1/2/50/1001, handler SDK real con checkpoint-restore: cero omitidos, orden por stream) + W3 relay AC01 (1000 ítems → reconstrucción exacta por stream, sublotes contiguos) |
| AC02 | W2 `TickWindower` tests + fixtures `feed_profile_last.json`/`market_batch_ticks.json` (representante por clase, BBO con timestamps por lado, metadata de omisión C6, QUOTE no borra TRADE, cierre por config/epoch, late etiquetado) + guard estático D3 |
| AC03 | W2 fixtures `market_batch_bars.json` + `BarNativePayload` tests (OHLCV/revisión/forming separado) + `EchoNativeBars.cs` guards (multi-TF declarado); superficie física BarsRequest = PHYSICAL_NOT_DEMONSTRATED (AC15) |
| AC04 | W2: coverage barrier + HISTORY_UNAVAILABLE visible + cursor de último cierre (diseño C# guardado); sin física NT |
| AC05 | W3: publish falla → `feed_nack` sin ACK; ACK sólo tras PublishSync de TODOS los grupos; retransmisión byte-idéntica absorbida por identidad (frame seq + posición); M2 byte-identity pins |
| AC06 | W3: cola in-flight acotada → `OUTBOX_FULL` (un nack por episodio verificado, TOCTOU corregido en W3-R), sin descarte, reanudación tras drenaje; ítem sobredimensionado = error visible |
| AC07 | W1 sobre `RequestReplyHandler` real (proto ToFunction/FromFunction, mutaciones realimentadas como checkpoint): estado final byte/JSON-igual, journal/egress idénticos, forward C2 == envíos singleton |
| AC08 | W1: veneno a mitad de lote → request completa aborta sin comitear; retry reconverge; 2 keys intercaladas aisladas; restore en handler fresco (memo por identidad de storage) |
| AC09 | W1 `TestFEFBMarketStreamBatchSerdeDoesNotScaleWithN` (lote N=25 = mismos 9 Set+1 Remove que 1 singleton) + campaña W4: 10.435 requests, 1 serde de sequencer por request (~2,08 MB) amortizado |
| AC10 | W2 `client_config_feed_test.go` (wire legacy byte-idéntico, 28 formas inválidas rechazadas, flush 1-1000 ≠ SnapshotIntervalMs 100-10000 intacto, recibida≠aplicada) + W3 negotiation (v1 hello → applied-config ack; unsupported = UNSUPPORTED explícito) |
| AC11 | W3 `m2_pin_test.go` (sha256 de fence/journal/ntx pinados) + suites session/ntx/journalfs verdes sin modificación + `legacy_feed_compat_test.go` (v3/bridge, sólo tests) |
| AC12 | W4 verticales: `TestFuturesVertical_FEFB_BatchRoute*` (ruta real bus→market_stream→1 forward C2→analytics == referencia singleton) + 4 negativos de desconexión (analytics sin C2, target inerte, pins de manifiesto en ambos module.yaml, batch_kind desconocido) |
| AC13 | Campaña 30min (`fefb_w4_campaign_run_1800.log`, artifact `fefb_w4_capacity_campaign_1800.txt`): 258.437 ítems procesados==ingress, 0 errores, edad capturada P50 241ms/P95 2,27s/P99 7,27s/max 10,66s vs cota 30s, replay 2× max 4,45s, ráfagas 256 máx 1,1s, estrés 5.120/s max 20,6s (headroom), recuperación de backlog 23,0s con llegadas continuas, sin muestreo oculto, RSS estable; checkpoints de runtime aislado NOT_RUN (no hay runtime aislado en S1) |
| AC14 | Edad evento real de la campaña (disponibilidad no retroactiva) + suites de frescura existentes verdes; egress desarmado por scope; sin backdating (reloj real) |
| AC15 | `ac15_nt_compile.md`: probe `dotnet/csc/mcs/mono/msbuild/nuget` ausente; guards estáticos Go en verde; `tests/FeedV1ContractTests.cs` sin compilar; una definición de instalación documentada (README-INSTALL). Compile con assemblies reales = gate físico pendiente |
| AC16 | Sweep: builds 4 módulos verdes; suites verde salvo 5 fallos preexistentes verificados en worktree limpio `90b23ffb` (`TestBTGS05PublicFiniteExecutionDifferential`, `TestFuturesVertical_UnknownManualPosition`, `TestFuturesVertical_ThreePathSplitAtTheHarnessSeam`, `TestEconomicMinimumCoreTypedConfigAndProtectionParity`, `TestTGFilterSharedTypedLiveBacktestFactoryParity`) — regresión nueva: cero; race limpio; cobertura código nuevo: batch.go 100%, client_config feed 100%, feed.go 98%, relay_batch 98,2%, relay 97,7%, bars/payload 94,1%, analytics nuevo 94,3% (2 retornos defensivos no alcanzables vía API pública), shell batch 92,1% (2 defensivos, mismo patrón que el path singleton); remote verificado |

Hallazgos registrados para G1: (1) techo in-proc por key acotado por serde del sequencer (~2 MB/aplicación) — palanca autorizada §8 (compactación de representación, owner W1/market), no defecto del consumidor; (2) artefacto de capacidad original sobrescrito por una smoke posterior — restaurado desde el log de la corrida de 1800s con procedencia; (3) latencia de campaña no ejecutable bajo -race (documentado; race corrido en suites excluyendo campaña). W4 claim honesto: sin runtime StateFun aislado, los checkpoints reales quedan para la certificación operativa (CERT-NT-01), no transferidos como PASS.

## Decisión Manager sobre G1 — REPAIR_REQUIRED_BY_MANAGER (2026-10-21)

**G1 = BLOCKED.** El Primary Manager (GPT-6) rechaza el cierre de S1 con cinco fallos nombrados (verificados en source por el submanager sobre `1af0352f`): **F1** `analytics/engine.go applyCanonicalEvent` sólo procesa TRADE/QUOTE — BAR_CLOSED/BAR_REVISED llegan como CanonicalEvent y caen sin ingestión; **F2** `ntfeed/market_batch.go` BAR_COVERAGE/BAR_GAP consumidos en el relay sin ruta a Core; **F3** outbox: GUID nuevo por proceso + archivo sólo de la sesión nueva + cursor global de la sesión anterior — pendientes durables previos jamás recuperados; **F4** EchoExecutionAddOn duplica la lane de mercado legacy en vez de integrar EchoFeedV1/EchoNativeBars (capabilities); **F5** README-INSTALL no identifica la fuente activa del camino FEFB (duplicidad EchoFeedAddOn/EchoExecutionAddOn). La evidencia S1 anterior se conserva como registro histórico; los estados REOPENED_MR1 de arriba se re-cierran sólo con evidencia nueva sobre el SHA reparado. Ejecución: MR1 (especialistas ONE-SHOT A/B + verificación fresca C), mismos D1–D10, sin deploy. AC13/AC15/AC16 se re-ejecutan/re-concilien sobre el SHA final.

## Evidencia MR1 — en curso (2026-10-21)

(Pendiente: se registra al cierre de MR1 con SHA_BASE_REPAIR, SHA_FINAL, reproductores rojo→verde por fallo, cobertura delta desde 112ccccd, campaña de capacidad y verificación fresca C.)
