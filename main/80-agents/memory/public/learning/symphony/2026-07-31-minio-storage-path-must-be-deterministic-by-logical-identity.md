---
type: learning
scope: application
created: 2026-07-31
updated: 2026-07-31
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[EchoForgeTradeListExporter]]"
entities:
  - "[[BuildMinIOPath]]"
  - "[[EchoForgeTradeListExporter]]"
related:
  - "[[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]]"
  - "[[2026-07-31-storage-path-deterministic-by-logical-identity]]"
aliases:
  - storage-path-no-execution-id
  - minio-path-deterministic
  - buildminiopath-anti-pattern
confidence: verified
source_session: cursor-2026-07-31-trade-list-path-rollback
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/application
  - app/echo-forge
  - tech/minio
  - tech/storage
  - priority/high
  - anti-pattern
---

# Storage paths compartidos deben ser determinísticos por identidad lógica

## Aprendizaje

El path de un objeto en storage compartido (MinIO/S3) NO debe incluir
segmentos que varían por ejecución: `request_id`, `run_id`, `trace_id`,
ni siquiera un `cfgID` derivado. Debe ser **función pura de la identidad
lógica del contenido** (instrumento/dirección/timeframe/estrategia/versión/stage).

Si dos productores legítimos del mismo artefacto pueden generar IDs de
ejecución distintos (y casi siempre pueden: watcher vs worker, RunID de
Temporal vs cfgID derivado), entonces **el path deja de ser el punto de
acuerdo** entre productor y consumidor. Cada uno escribirá bajo su propio
segmento y el downstream no encontrará el artefacto, o peor, encontrará
uno residual de una corrida previa.

## Anti-patrón observado

```go
// PROHIBIDO: requestID como segmento del path
path := BuildMinIOPath(ctx, wave, inst, dir, tf, strat, ver, requestID, folder, file)
// donde requestID se resuelve desde context (RunID Temporal) o cfgID
```

El `ctx` termina siendo fuente de indeterminación: el mismo artefacto
lógico produce paths distintos en el watcher (cfgID), en el worker
(RunID) y en el uploader (meta.RunID). Bucket queda con N carpetas
duplicadas del mismo proyecto; downstream baja cualquier cosa.

## Patrón correcto

```go
// OK: path = identidad lógica pura
path := BuildMinIOPath(wave, inst, dir, tf, strat, ver, folder, file)
```

El `request_id`/`run_id` pueden persistirse en MongoDB o en atributos de
telemetría/observabilidad, **nunca** como segmento del key de storage.

## Cuándo aplicar

- Cualquier helper tipo `BuildPath`/`ObjectKey` para storage compartido.
- APIs de upload/download donde productor y consumidor son procesos
  potencialmente distintos (orchestrator vs worker, watcher vs runtime).
- Refactor defensivo: si ves un `ctx` o `requestID` en la firma de un
  constructor de paths de storage, alarma.

## No aplicar a

- Paths de staging/temporal local (`os.CreateTemp`): ahí el ID de
  ejecución es correcto.
- Trace IDs como atributos de logs/métricas/spans: ortogonal al path.

## Trazabilidad

- Bug concreto: [[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]] (EF-G27).
- Decisión arquitectónica: [[2026-07-31-storage-path-deterministic-by-logical-identity]].
- Fix en código: `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.3.
