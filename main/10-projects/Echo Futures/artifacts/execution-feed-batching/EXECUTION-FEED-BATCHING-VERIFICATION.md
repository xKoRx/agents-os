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
| AC01 | ALL: reconstruir exactamente todos los eventos capturados y orden por stream con flush1/50/100ms, fragmentación por bytes/eventos y cola concurrente | W2/W3 | Lista de IDs/payload/hash antes-después; cero omitidos/truncados | NOT_RUN |
| AC02 | LAST: conservar representante correcto por clase y ventana, metadatos de omisión y timestamps; QUOTE no borra TRADE; cierre de ventana/config/epoch | W2 | Traza manual con evento en borde, tardío, bid/ask separados y heartbeat; assert ALL incompatible rechazado | NOT_RUN |
| AC03 | Cierres/revisiones de todos los timeframes configurados aunque no haya Strategy suscrita; ninguna vela desde ticks reducidos | W2/W4 | Fuente NT controlada multiTF, oracle OHLCV/revisión/calendario; formando != cerrado | NOT_RUN |
| AC04 | Gap de barra/desconexión: backfill solapado, dedup y barrera de cobertura; no señales retroactivas; ausencia real de historia permanece explícita | W2/W4 | Eliminar un cierre y recuperarlo; calendario pausa/no-trade; READY sólo tras cobertura | NOT_RUN |
| AC05 | ACK durable: caída antes/después de Kafka ACK, perdida de ACK al cliente y publicación parcial conservan/reenvían sin pérdida | W2/W3 | Outbox/disco y producer capturado; ACK de socket no libera; IDs estables a través restart | NOT_RUN |
| AC06 | Backpressure: memoria/disco finitos, sin descarte silencioso, feed no estrella cancel/close/results; identidad por lane | W2/W3 | Límites pequeños, saturación y recuperación; no lote que exceda cap; fallo visible | NOT_RUN |
| AC07 | Procesamiento en lote: misma secuencia dividida 1/2/50/1001 produce mismo estado lógico y efectos por evento, no sólo último estado | W1 | Diferencial engine+RequestReplyHandler reales, JSON canónico cuando mismo encoding; cero alias mutable | NOT_RUN |
| AC08 | Persistencia/retry: fallo a mitad/antes del reply, respuesta perdida, restore en otra instancia, varias keys/requests intercaladas | W1 | Reinicio sin caches; no success parcial, ningún estado no commitado contamina retry; race | NOT_RUN |
| AC09 | Serde grande no escala una vez por tick dentro del lote; estado maduro conserva ventanas/identidad/conflictos y puede migrarse/volver | W1 | Contadores de codec, perfiles y fixtures checkpoint previo/candidato; rollback leído de verdad | NOT_RUN |
| AC10 | Config común: handshake/hot-update/unsupported, feed50ms distinto de SnapshotIntervalMs legacy100ms, configuración recibida vs aplicada | W2/W3 | Fixtures legacy MT4/MT5 y NT; unknown fields/version, config inválida no arma; defaults previos intactos | NOT_RUN |
| AC11 | Bridge dummy: no sampling/bar/indicator/MM logic; routing/idempotencia/Kafka conservan orden y M2/fence intactos | W3 | Pruebas de wrong-account, retries y comandos obsoletos; revisión dependencias + integración M2 anterior | NOT_RUN |
| AC12 | Recorrido real de tipos/rutas: sender cliente→bridge→Kafka→manifiesto→Core→analytics sin desempaquetado que pierda ventaja | W4 | Parser y dispatch productivos; desconectar tipo/topic/target hace fallar test; dos manifiestos fuente | NOT_RUN |
| AC13 | Capacidad ALL50ms con estado maduro, llegada independiente, replay1×/2× y ráfagas, backlog inicial mientras llegan nuevos datos | W1/W4 | Serie tiempo ingress/processed/lag/age, P50/P95/P99, CPU/GC/heap; >=30min y checkpoints aislados; no sampling oculto | NOT_RUN |
| AC14 | Freshness y causalidad: recibir backlog no permite entradas; disponibilidad real del batch, revisiones no miran futuro, skew no se oculta | W1/W4 | Permutaciones eventos/timers/mismo instante, replay y política incompatible; egress desarmado | NOT_RUN |
| AC15 | NT: una definición de clase en instalación aislada, parser válido, native bars API compilada, multi-binding único feed y resultados ejecución | W2/W4 | Hash del conjunto + compile con assemblies reales; callbacks/harness SIM identificados; si falta entorno, NOT_DEMONSTRATED | NOT_RUN |
| AC16 | Integración final: baseline heredado identificado, cero nuevas regresiones, >=95% código nuevo, límites físicos/migración y documentación instalable | Submanager/W4 | Comandos+exit+logs, cobertura denominador completo, SHA exacto, diff y working trees intactos | NOT_RUN |

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
