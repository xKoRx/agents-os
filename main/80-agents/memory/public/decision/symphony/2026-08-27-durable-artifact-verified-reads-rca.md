---
type: decision
schema_version: 1
scope: project
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-27-durable-artifact-plane-write-once-final-e2e]]"
aliases:
  - verified reads rca
  - durable verified read invariants
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-RCA-TOP
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/symphony
  - project/echo-forge
  - tech/durable-pipeline
  - scope/project
---

# 2026-08-27-durable-artifact-verified-reads-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- RCA/DESIGN read-only sobre `xKoRx/symphony` @ `5e3c2b3` (write-once CERTIFIED_CLOSED 0.2.77) + `xKoRx/sdk` @ `ea09cc1`. Próximo track tras el cierre write-once: demostrar que todo consumer durable verifica bytes físicos contra el ArtifactRef sellado en Evidence ANTES de usarlos.
- Hallazgo central: Mongo YA persiste `size`+`sha256` en `evaluations.artifacts[].artifact_ref` y `trade_sets.payload_artifact` (`evidence_documents.go:20-28`); el resolver histórico lee el ref completo pero el carrier `runtime.StrategyArtifact` (`config.go:457-468`) descarta Size/SHA en `historical_cohort_activity.go:162`; `DownloadToCustom`/`DownloadObjectToPath`/`DownloadArtifactToPath` descargan key-only sin verificación y sin temp+rename. Payloads (FetchDurable), TradeSet, WFM seal, apply y MT5 exporter YA verifican vía `VerifyArtifactStream`.

## Decisión

- Autoridad durable de lectura: Evidence → `DurableArtifactRef{Store,Bucket,ObjectKey,Size,SHA256}` exacto. Nunca key a secas, list, ETag, path derivado, filename o «latest». List puede descubrir candidatos sólo donde el contrato lo permita; antes de usar, cada artifact resuelve a ref exacto de Evidence.
- Carrier: extender `runtime.StrategyArtifact` con `Artifact *domain.DurableArtifactRef` (opcional; fail-closed si falta en path durable). No duplicar Size/SHA sueltos ni crear un tercer carrier.
- Primitiva única `FetchDurableToPath(ctx, ref, destPath)` en el adapter Symphony `storage-minio` (NO en SDK): GET exacto → temp oculto hermano `.<base>.partial-<rand>` (sin extensión consumible) → `io.MultiWriter(file, sha256)` streaming con conteo → comparar n==Size y SHA → `os.Rename` atómico ONLY tras verificación; mismatch borra temp, destino NO publicado, `ErrContractConflict`. `DownloadDurableToCustom(ctx, project, artifacts)` delega por objeto y rechaza colisión de basename duplicado en el batch (fail-closed).
- Política destino existente: siempre sobrescribir vía temp+rename verificado (los bytes locales no tienen autoridad; evita envenenar retries). Política fallo de cohort: publish por archivo verificado + cleanup obligatorio del batch al fallar; la corrección NO depende del cleanup porque execute_sqx está secuenciado tras el batch completo y el overwrite verificado desactiva residuos.
- Taxonomía: size/SHA mismatch y objeto sellado ausente → `ErrContractConflict` NON-RETRYABLE (ya mapeado NonRetryable en todos los boundaries de activity); timeout/red/5xx/disco → retriable crudo. Sin centinelas nuevos (`ErrArtifactIntegrity`/`ErrArtifactMissing` no mejoran materialmente la retry policy). Access denied → terminal no-retriable. Stat remoto: precheck OPCIONAL, nunca autoridad; ETag jamás digest.
- Normalización refs: conviven `domain.ArtifactRef` (legacy hex sin prefijo, MT5 portable) y `DurableArtifactRef` (`sha256:<hex>`); el boundary verified-read acepta SÓLO `DurableArtifactRef`; puente único sancionado `DurableArtifactRefFromLegacy`. Sin migración de dominio en este track.
- Gap material MT5: `ExportMT5EAResult` sólo retorna `ObjectKey` (digest computado en PutPayload se pierde) → extender el result carrier con el ref completo (persiste en historial Temporal; sin cambio Mongo). `ArtifactTaskRequest` gana `ExpectedSource *ArtifactRef` (EX5 disponible en `ArtifactTaskResult.Primary` del compile). Legacy MT5Compiler/MT5Runner (`mt5_compile`/`mt5_backtest`, AdaptiveSQXWorkflow sin dispatcher en repo) y modo listing legacy: clasificados legacy/no-durable, fuera del contrato verified-read, sin garantías forzadas; deprecación diferida.
- Slicing SEQUENTIAL_SLICES: S1 carrier+primitiva+migración steps/WFM-physical (~10 archivos), S2 MT5 portable (~8), S3 E2E físico desechable (~4). Payload/TradeSet/WFM-seal/apply NO se refactorizan (ya verificados). Technical recovery de Retester/Optimizer queda bloqueado hasta cerrar verified reads.

## Rationale

- La verificación debe ser streaming O(1) (`VerifyArtifactStream` ya lo es) y publicar el archivo final sólo tras verificar; escribir-destino-then-hash puede exponer bytes corruptos al camino canónico del consumer antes de fallar.
- `ErrContractConflict` ya fluye NonRetryable vía `temporalNonRetryable`/classify* en project/wfm/apply/reconcile/trade-list; reintegrity mismatch en objeto inmutable no sana con retry — reusar el sentinel evita taxonomía paralela sin beneficio de retry policy.
- sobrescribir-verificado vence a «verificar existente y ACK»: ahorra una sola GET en retries raros a costa de un path de hash local sin autoridad (KISS).
- El digest MQ5 existe en el momento del PutPayload del exporter; perderlo en el result carrier es el único hueco de modelo (todo lo demás es carrier/API); el historial event-sourced de Temporal basta como persistencia intra-FlowRun.

## Consecuencias

- Toda lectura durable Evidence-backed queda ref-exacta y verificada antes del uso; SQX nunca arranca con inputs parcial-inválidos; el consumer jamás observa archivos finales no verificados.
- `DownloadToCustom(ctx, project, keys)` queda como API legacy (callers legacy/config); los callers durables migran a `DownloadDurableToCustom`.
- Sin schema Mongo nuevo, sin índice nuevo, sin tipo de dominio nuevo, sin cambio SDK.
- Closure gate (12 puntos) y REQUIRED_BEFORE_PROD congelados en el checkpoint del proyecto; NEXT EXACT `DURABLE-ARTIFACT-VERIFIED-READS-SLICE1-NORMAL`.

## Alternativas descartadas

- Romper/reemplazar `DownloadToCustom` globalmente: obliga a callers legacy a inventar digests falsos.
- Extender `StrategyArtifact` con `Size`+`SHA256` planos: duplica campos que pueden divergir del ref canónico (esto ES el ref aplanado).
- Verificar-existente-y-ACK en destino local: bytes locales sin autoridad; complejidad extra sin beneficio material.
- Sentinels `ErrArtifactIntegrity`/`ErrArtifactMissing`: ambos mapean al mismo comportamiento NonRetryable; no mejoran la retry policy de Temporal.
- Refactor de `FetchDurable` a streaming: correcto hoy para payloads en memoria (bounded por ref.Size); el primitivo nuevo a archivo cubre el caso grande.
- Primitiva verified-read en SDK: el contrato durable (refs de Evidence) es de Symphony; el wrapper SDK es transporte genérico.

## Slice 1 — implementación cerrada

- `runtime.StrategyArtifact` ahora transporta `Artifact *domain.DurableArtifactRef` como autoridad física única; `Key` se conserva como mirror y exige `Key == Artifact.ObjectKey` en consumers durables. No se agregaron campos paralelos, tipos de dominio, schema, migration ni cambios al SDK.
- Historical Builder templates, Retester y Optimizer preservan el `DurableArtifactRef` exacto desde Evidence; Builder recovery y los outputs Builder/Retester/Optimizer/FinalReretester copian el ref exacto, y FinalReretester reemplaza cualquier ref de input stale por el ref nuevo de output.
- `FetchDurableToPath` ejecuta GET exacto, temp oculto en el mismo directorio, hash/tamaño streaming y rename atómico sólo tras verificación. `DownloadDurableToCustom` preflighta refs y basenames, rechaza colisiones y limpia todos los finales publicados por su batch ante fallo. Missing sellado, size mismatch y SHA mismatch son `ErrContractConflict`; fallos transitorios permanecen crudos/retryable.
- `downloadStrategies` usa la frontera durable additive para Builder template, Retester y Optimizer sin fallback key-only; ProjectActivity convierte sólo `ErrContractConflict` a Temporal non-retryable `PersistenceContractConflict`. Final Reretester input, WFM physical input y MT5 portable quedan explícitamente en Slice 1B/2.
