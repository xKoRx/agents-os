---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[2026-09-04-echo-forge-campaign-builder-supply-identity]]"
  - "[[2026-08-23-durable-strategy-identity-v2-cutover]]"
  - "[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]"
  - "[[Echo Forge — Factory V2 Completion]]"
last_verified: "2026-09-07"
confidence: verified
aliases:
  - F-01 SPEC
  - Canonical generation concurrency contract
  - Echo Forge F-01
related:
  - "[[Echo Forge — F-01 Canonical generation concurrency]]"
  - "[[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]"
entities:
  - "[[Echo Forge]]"
  - "[[xKoRx/symphony]]"
tags:
  - kind/resource
  - area/echo
  - project/echo-forge
created: "2026-09-07"
updated: "2026-09-07"
---

# Echo Forge — F-01 Canonical Generation Concurrency Contract

Esta Resource es el contrato técnico de `F-01 — Canonical generation concurrency`. Define qué debe quedar cierto. La ejecución vive en [[Echo Forge — F-01 Canonical generation concurrency]]. No es un tutorial de implementación.

Baseline de source: `xKoRx/symphony@db8a022703082fd7ee9d1e15243c5d1b2feaf578`. Agents OS origin/master al diseñar: `83506a14f0b850402fbb61d50e90790662fe19f0`. Corrección in-place sobre el commit Agents OS `419c64084459c9c903061cad0ecf900f33313b09`.

## Síntesis vigente

### Problema

`CanonicalStrategyID` no es puro: lee `$HOST_KEY` y recorta sufijos alfanuméricos 3–16 según el entorno. La misma entrada puede producir IDs distintos en Zeus versus Hera.

`HOST_KEY` no es identidad de negocio. En publication, `legacySQXFileName` aún anexa `.hostKey` cuando el basename local no trae la convención instrumento/estrategia (`TestPublishedSQXFileName_LegacyGenericBasenameCollidesByHost`). Eso evitó colisiones físicas entre workers y también hace que un retry/recovery en otro host publique otra identity.

Retirar `HOST_KEY` sin un discriminator durable de **logical producer** recrea colisión intra-wave: `BuildMinIOPath` no incluye producer; `BuilderSupplyBatchRef` namespacía la wave, no el producer; el basename SQX local puede repetirse.

### Qué no es el discriminador

La decisión anterior (`OutputNamespaceOwnership` / FlowRun dueño del namespace = discriminator intra-wave) queda **retirada**. Es falsa contra source.

`OutputNamespaceOwnership` unique es `(bucket, namespaceKey)` owned by **FlowRun**. El `StageExecutionRef` de la claim es provenance del initial claimant, no producer ownership (`OutputNamespaceOwnershipStore`, `output_namespace_ownership.go`). Test PostgreSQL `T7 concurrent same flow sibling claims`: StageExecution C y D, mismo FlowRun, mismo bucket, mismo namespace → **ambas claims ACKNOWLEDGED**. Protege `FlowRun A vs FlowRun B`. No discrimina `producer A vs producer B` dentro del mismo FlowRun.

`BuilderSupplyBatchRef` = `{CampaignRef}:g{NNNNNN}` se deriva de Campaign + wave. Todos los producers de esa supply wave comparten el batch. Su `FilenameToken` namespacía la wave, no el producer.

Campaign Builder publica con `UploadFromDiskExactWithBatchPreflight(..., beforeBatch=cap, beforePut=nil)`. Singleton stages sí sellan `StageProducerOutput` antes del PUT. **No existe hoy** el enlace `logical producer → durable producer authority → publication naming/address → retry/recovery` en el path Builder. F-01 debe construirlo sobre authorities ya persistidas, sin tabla nueva.

### Veredicto central — logical producer y discriminator durable

No se agrega tabla, UUID por attempt, ni migration.

**Logical producer (Builder GENERATED):** exactamente una `StageExecution` de Builder. Un slot durable `(FlowRunRef, TaskPath, StageKey, Subject, CanonicalInputs, Generation)` identificado por `ExecutionIntentKey`.

No es FlowRun. No es wave. No es host. No es worker. No es proceso SQX. No es Temporal Activity attempt. No es `StageExecutionRef` UUID (surrogate PK asignado al INSERT).

**Durable discriminator:** `ExecutionIntentKey` (`hashIdentity("stage-execution.v1", FlowRunID, StageInstanceKey, Generation)`). Cardinalidad: **exactamente una vez por logical Builder producer**.

**Producer filename token:** representación determinista, filename-safe y **biyectiva** del digest de 32 bytes de `ExecutionIntentKey`: `base64.RawURLEncoding` (43 chars, charset `A-Za-z0-9-_`, permitido por `sanitizeFileName`). No es `p`+hex(64). No es truncación. No es HOST_KEY. No es Temporal ID.

Retry técnico (mismo slot, misma generation, otro host, otro attempt Temporal, crash recovery) → mismo `ExecutionIntentKey` → mismo token → mismos Strategy IDs → mismas artifact keys.

Dos logical producers intra-wave (mismo FlowRun, misma Campaign, misma wave, mismo `BuilderSupplyBatchRef`, mismo basename SQX local) → `TaskPath` (o inputs de template) distintos → `StageInstanceKey` distintos → `ExecutionIntentKey` distintos → tokens, IDs y keys distintos. Ambos válidos.

`HOST_KEY` permanece operacional fuera de identity/publication GENERATED: boot del worker, ProActiva `maintenance/state/{host_key}`, telemetría. No se elimina globalmente.

## Definición: logical producer

F-01 permitirá ejecutar concurrentemente **dos StageExecutions de Builder** que pertenecen a la misma Campaign/wave/FlowRun y publican strategies GENERATED.

Esa unidad ya existe en source. `runtime.StructuralTaskPath(indexes...)` identifica el TaskSpec por índice estructural (`root/0`, `root/1`, …), nunca por display name. `NewStageIntent` / `NewStageExecutionIdentity` materializan un slot por `TaskPath`. Dos tasks Builder en el mismo spec obtienen StageExecutions distintas. Un retry del mismo `TaskPath` reconverge.

El modelo actual es `1 Builder StageExecution → N strategies` (N archivos SQX del mismo job). F-01 no inventa topología fija ni exige N hosts. El modelo concurrente futuro/legítimo es `N logical producers = N StageExecutions` (típicamente N `TaskPath` en el mismo FlowRun). Cada producer sigue pudiendo emitir N strategies; el token de producer es constante para esos N archivos; el stem SQX local (`Strategy_X.Y.Z.zN`) distingue archivos dentro del producer.

F-01 no asume `producer == host` ni `producer == Temporal attempt`. `StageExecutionTemporalCorrelation` (WorkflowID/RunID/ActivityID) es provenance y **no participa** en identity (`StageExecutionIntent.Temporal`).

Si el source futuro introduce varios Builders paralelos **dentro de una sola StageExecution**, esta SPEC queda corta: STOP, no ampliar en NORMAL.

## Evaluación de candidatos

| Candidate | Cardinality | Stable across retry | Distinguishes sibling producers | Survives new host | Durable before physical production | Business/operational meaning |
| --- | --- | --- | --- | --- | --- | --- |
| `FlowRunRef` | 1 por invocación de negocio | sí | no (siblings comparten FlowRun) | sí | sí | invocación de flow; demasiado grueso |
| `OutputNamespaceOwnership` | 1 por `(bucket, namespaceKey)` owned by FlowRun | sí (ACK same FlowRun) | **no** (T7: siblings ACK) | sí | sí, claim pre-SQX | mutex de namespace físico entre FlowRuns |
| `BuilderSupplyBatchRef` | 1 por Campaign+wave | sí | **no** (todos los producers de la wave lo comparten) | sí | sí | namespace de generación de negocio |
| `TaskPath` | 1 por índice estructural del spec | sí | sí intra-spec; no único cross-FlowRun | sí | sí | posición del task; incompleto solo |
| `StageKey` | 1 por `taskType@contractVersion` | sí | no (todos los Builder del mismo tipo) | sí | sí | contrato de stage |
| `Generation` | N reevaluaciones deliberadas del slot | retry técnico la preserva; reevaluación la incrementa | no solo | sí | sí | versión del intento durable del slot |
| `StageInstanceKey` | 1 por slot `(TaskPath, StageKey, Subject, inputs)` | sí | sí intra-FlowRun; excluye Generation | sí | sí | slot estable; reevaluación deliberada reusa slot y cambia execution |
| `ExecutionIntentKey` | **1 por logical producer** `(FlowRun + slot + Generation)` | sí (lookup unique; retry preserva Generation) | sí (TaskPath/inputs/Generation) | sí | sí (computable antes del INSERT y del PUT) | identidad durable del producer |
| `StageExecutionRef` UUID | 1:1 con `ExecutionIntentKey` **después** del resolve | sí post-insert (`uuid.NewString` una vez; unique por intent key) | sí, pero es surrogate | sí post-insert | no antes del INSERT; sí antes del PUT | PK de recovery; no fórmula de identity |
| `ProducerContextDigest` | 1 por contexto de bytes/replay | sí si el contexto es el mismo | no es identity | sí | en record-before-put, no nombra archivos | replay de bytes/contexto |
| `StageProducerOutput` | 1 por `(StageExecutionRef, object_key)` | sí (insert-once; ACK identical) | no nombra; convalida address+digest | sí | **antes del PUT si se cablea**; hoy Builder `beforePut=nil` | recovery authority de publicación |
| `HOST_KEY` / hostname / PID / Temporal attempt / UUID random | por worker/attempt | **no** cross-host | accidentalmente sí, rompe retry | **no** | n/a | infra; prohibido en F-01 |

Pregunta clave: ¿qué durable identity existe exactamente una vez por logical Builder producer? **`ExecutionIntentKey`.**

## StageExecution — respuestas

1. ¿Una StageExecution corresponde exactamente a un logical producer? **Sí** en Builder durable actual y en el modelo concurrente que F-01 habilita.
2. ¿Dos producers intra-wave legítimos obtienen StageExecutions distintas? **Sí**, vía `TaskPath` estructural distinto (o `CanonicalInputs` de template distintos → `StageInstanceKey` distinto). No hace falta topología hardcodeada.
3. ¿Retry/recovery obtiene la misma StageExecution? **Sí.** `ResolveStageExecution` lookup por `ExecutionIntentKey`; unique en PostgreSQL; `convergeStageExecution` ACK si la fila coincide. Retry técnico preserva `Generation`. Reevaluación deliberada incrementa `Generation` → nuevo producer generation (nuevo token, nuevas strategies).
4. ¿El ref/key está disponible antes de publication? **Sí.** Pipeline durable: `resolve_stage_execution` → `claim_output_namespace` → `execute_sqx` → upload. `ExecutionIntentKey` es computable incluso antes del INSERT.
5. ¿Puede producir un producer token determinista sin identity de infraestructura? **Sí:** `Base64URLNoPad` del digest completo de `ExecutionIntentKey` (43 chars). No UUID, no host, no Temporal, no truncación.

`StageExecutionIdentityView` hoy **omite** `ExecutionIntentKey` y `TaskPath`. Publication no debe depender de ampliar esa vista: recomputar el mismo `NewStageIntent` / `NewStageIntentWithInputs` ya usado en resolve (mismos `FlowRunRef`, `TaskPath`, task, inputs). El UUID `StageExecutionRef` queda como FK de `StageProducerOutput`, no como filename token.

## Cuatro conceptos separados

### Producer identity

`ExecutionIntentKey` del Builder StageExecution. Distingue dos producers legítimos intra-wave. No es Strategy ID.

### Campaign wave namespace

`BuilderSupplyBatchRef` sigue siendo la identity de negocio de la ola (`{CampaignRef}:g{NNNNNN}`). F-01 **no** cambia su fórmula ni `FilenameToken()` ([[2026-09-04-echo-forge-campaign-builder-supply-identity]]). Sigue en `StrategyMeta` para cap/replenishment.

**Nuevos durable GENERATED:** no se proyecta `FilenameToken()` al published basename. Es redundante: `ExecutionIntentKey` ya incorpora `FlowRunRef`, y cada ola Campaign materializa un FlowRun hijo distinto. Apilar `FilenameToken` (~45 chars) + producer token revienta el presupuesto de 128 (`sanitizeFileName`). Historia que ya trae batch token no se renombra.

### SQX strategy-local identity

Stem canónico local = `CanonicalStrategyFilename(local_sqx_basename)`. Distingue N outputs **dentro** de un producer. No es único intra-wave entre producers. En el filename físico se publica su digest completo (no el stem humano), para caber siempre en 128.

### Strategy identity y artifact addressing

**GENERATED Strategy ID** = `CanonicalStrategyID(published_basename)` con `identity_model_version=2`, unique global. `StrategyRef` lo minta `AdoptStrategy`.

**Artifact address** = `BuildMinIOPath(wave, instrument, direction, timeframe, strategy, version, taskFolder, published_basename)`. Wave en PATH es routing, no identity.

### Fórmula conceptual (nuevos durable GENERATED)

```text
producerTok = Base64URLNoPad( bytes(ExecutionIntentKey.digest) )     // 43, biyectivo
localTok    = Base64URLNoPad( SHA256( CanonicalStrategyFilename(local_basename) ) )  // 43, biyectivo

published_basename = producerTok + "_" + localTok + ".sqx"          // 91 ≤ 128 siempre

CanonicalStrategyID(published_basename)  → generated Strategy identity
BuildMinIOPath(..., published_basename)  → artifact object key
```

No se concatena `BuilderSupplyBatchRef.FilenameToken`, `HOST_KEY`, convención `legacySQXFileName` ni `p`+hex. `ExactOutputName` sigue ganando (singletons). Si `ExecutionIntentKey` no es canónico → `CONTRACT_CONFLICT`. Si `len(published_basename) > 128` → `CONTRACT_CONFLICT` (no truncar). El encoding fijo de 91 chars hace ese branch inalcanzable salvo bug.

Presupuesto (source `sanitizeFileName`, máximo 128): Campaign `FilenameToken` ≈ 45; `p`+64 hex = 65; juntos no dejan stem real. Truncar el digest está prohibido. Compactar el digest **entero** a Base64URL no es truncación.

**ADOPTED.** `canonical_strategy_id` histórico byte-for-byte. F-01 no recanonicaliza registry ni objetos. Un filename con `.zeus`/`.hera` opaco se re-lee igual; el helper ya no strippea por entorno.

**RE-GENERATED FROM EXISTING STRATEGY/TEMPLATE.** El origen es input/lineage. No se renombra. Template mode incluye inputs en `StageInstanceKey` (`NewStageIntentWithInputs`). Cohort distinto → producer nuevo → token nuevo → Strategies nuevas → IDs nuevos → artifacts nuevos → lineage al source. `rejectBuilderTemplateCanonicalCollisions` fail-closed si el output reusa un canonical del template.

Downstream adopta el `CanonicalStrategyID` del upstream carrier. No reminta identity por filename físico.

## CanonicalStrategyID — contrato puro

El helper sólo normaliza wrappers documentados sobre un basename:

1. Trabajar sobre `filepath.Base`.
2. Quitar `.sqx` / `.md`.
3. Quitar prefijos WF (`WF_Matrix_-_`, `WF_Matrix-`, `WF_-_`, `WF-`, `WF Matrix - `) hasta idempotencia.
4. Recortar `_robust` sólo si el nombre contiene `Strategy_`.
5. Recortar sufijos `(N)` de 0 a 9.
6. Devolver el resto intacto (incluye tokens compactos nuevos y batch/host históricos ya presentes; no strippear encoding Base64URL).

Prohibido: `os.Getenv("HOST_KEY")`; heurística `isLikelyHostKey` (puede mutilar `Strategy_X.Y.Z.z10`); anexar host; resolver colisiones con `(1)`/`(2)`, sufijo host nuevo o UUID random.

## Publication / addressing / producer-output

`publishedSQXFileName`:

- Si `ExactOutputName` está seteado: usarlo y ignorar host, batch token y producer encoding. Sin cambio de contrato.
- Durable Builder GENERATED: **no** `legacySQXFileName`+host; **no** `namespaceCampaignBuilderFilename`. Usar la fórmula compacta de 91 chars. `BuilderSupplyBatchRef` en meta sigue alimentando sólo el cap `beforeBatch`.
- Path MinIO sigue siendo routing (instrument/wave/taskFolder).

`StrategyMeta` transporta el producer filename token ya compacto (o el `ExecutionIntentKey` para derivarlo en el adapter). Publicar Builder durable sin EIK canónico → `CONTRACT_CONFLICT`.

**Por qué `beforePut=nil` hoy:** Campaign usa batch-preflight sólo para cap de candidatos. El comentario de `SingletonStageProducerOutputStore` explica que object keys host-dependent impedían serializar producers competidores con el store genérico `(stage_execution_id, object_key)`. Tras F-01 las keys son host-independent y stage-scoped; el store genérico `RecordStageProducerOutput` (PK ya existente, migration 008) cubre Builder N-output. No se usa el store singleton (ese es 1:1). No hay tabla nueva.

F-01 cablea Builder (Campaign y generic durable) a `UploadFromDiskExactWithBatchPreflight` / pre-put: `beforePut = RecordStageProducerOutput`. Campaign conserva `beforeBatch` cap. Durable Builder fail-closed si `Control` no implementa `StageProducerOutputStore` (mismo patrón que singletons con su port). `ProducerContextDigest` de Builder se deriva de `ExecutionIntentKey` + identidad SQX-local del candidato; excluye host, Temporal, PID y reloj.

Colisión contractual (mismo logical producer/address, bytes o contexto incompatibles) → `CONTRACT_CONFLICT`. Nunca otro filename.

`claim_output_namespace` **permanece** como mutex FlowRun sobre el path sin filename (inputs históricos / `LoadOutputNamespaceOwner`). No es uniqueness de producer. P3 prohíbe usar `same FlowRun sibling OutputNamespaceOwnership ACK` como supuesto de uniqueness.

## Proofs P1–P8

### P1 — SAME FLOW / DISTINCT PRODUCERS

Dos logical producers: mismo FlowRun, misma Campaign, misma wave, mismo `BuilderSupplyBatchRef`, mismo SQX basename local. Distinct `TaskPath` (p.ej. `root/0` vs `root/1`). Expected: distinct `ExecutionIntentKey`, distinct producerTok, distinct generated identity, distinct artifact key, `len(published_basename)=91≤128`, **sin** Campaign `FilenameToken` en el nombre nuevo. Ambos válidos.

### P2 — SAME PRODUCER / DIFFERENT HOST

Mismo logical producer en host A, recuperado/reintentado en host B. Expected: same `ExecutionIntentKey`, same token, same Strategy identity, same artifact key. Cero dependencia de `HOST_KEY`.

### P3 — CONCURRENT CLAIM

Dos producers P1/P2 concurrentes materializan outputs sin depender de la semántica `same FlowRun sibling OutputNamespaceOwnership ACK` como uniqueness. Uniqueness = token en published name + unique v2 + `StageProducerOutput` por `(stage, object_key)` + PutIfAbsent.

### P4 — CRASH BEFORE PUBLICATION

`ExecutionIntentKey` durable (y StageExecution resuelta) antes de PUT. Crash. Recovery recomputa el mismo token y la misma address. No mint another producer identity. Si `StageProducerOutput` ya se persistió, retry ACK identical / CONFLICT distinct; PUT usa la misma key.

### P5 — LOST PUT RESPONSE

PUT pudo ocurrir. Recovery reconcilia exact same address/digest (`PutIfAbsent`, producer-output ACK, Adopt unique). Nunca mint another producer identity ni otro filename.

### P6 — CONTENT CONFLICT

Mismo logical producer/address, bytes o `ProducerContextDigest` incompatibles. Expected: `CONTRACT_CONFLICT`. Nunca otro filename.

### P7 — ADOPTED

Sin cambio de ID. Filas v2 e objetos históricos intactos, incluidos sufijos host opacos.

### P8 — REGENERATION

Existing strategy/template como input. Producer nuevo cuando el contrato lo exige (inputs de template en identity → nuevo `ExecutionIntentKey`). Strategies nuevas, IDs nuevos, artifacts nuevos, lineage al source, source immutable.

## Crash / retry matrix

Notación: EIK = ExecutionIntentKey; TOK = producer filename token; ID = CanonicalStrategyID; KEY = object key; NS = OutputNamespaceOwnership; SPO = StageProducerOutput.

**A — P1 distinct producers, same wave, same local basename.** Dos EIK. TOK distintos. ID/KEY distintos. NS puede ACK ambos. Outcome: ambos válidos.

**B — P2 replay mismo producer, otro host/attempt.** Mismo EIK/TOK/ID/KEY. SPO ACK. PutIfAbsent ACK. Outcome: convergencia.

**C — Crash antes de durable StageExecution.** Resolve recrea el mismo EIK. Outcome: una identity.

**D — P4 authority resuelta, crash antes de PUT.** EIK estable; SPO puede estar ausente o persistido. Retry misma KEY. Outcome: una publicación.

**E — P5 PUT, respuesta perdida.** Reconcile same KEY/digest. Outcome: ACK. Unknown commit → recovery read, no segundo mint.

**F — Recovery en otro worker.** Igual a B. Prohibido divergir por HOST_KEY.

**G — P6 contenido incompatible.** SPO o PutIfAbsent o unique v2. Outcome: `CONTRACT_CONFLICT`.

**H — P7 adopted.** F-01 no escribe esa fila. Outcome: intacta.

**I — P8 template/regeneration.** Nuevo EIK cuando inputs cambian. `rejectBuilderTemplateCanonicalCollisions`. Origen intacto.

## Errors / retries

| Clase | Señales | Retry | Mint identity |
|---|---|---|---|
| valid replay | PersistenceAcknowledged idéntico; PutIfAbsent same digest | sí, no-op | no |
| retryable infrastructure | red, timeout, executor | sí | no |
| unknown commit | PersistenceUnknownCommit / ErrUnknownCommit | recovery read | no |
| durable contract conflict | PersistenceContractConflict / ErrContractConflict | no | no |
| malformed durable state | fila inválida al load | no | no |
| physical object missing after authority | SPO/adopt sí, probe no | republicar misma KEY | no |
| duplicate FlowRun namespace | NS claim de otro FlowRun | no | no |
| duplicate physical basename | mismo KEY, distinto digest | no | no |
| sibling producers same basename local | TOK distintos | n/a | sí, dos IDs válidos |
| cancellation | cancel del FlowRun/stage | no continuar el árbol | no |

## BWC

IDs adoptados intactos. Objetos históricos legibles (incluidos los que ya traen `FilenameToken` de Campaign o sufijo host). Wrappers WF/`_robust`/`(N)` siguen tolerados. No rename masivo. `DATABASE MIGRATION: NONE`. `BuilderSupplyBatchRef` y unique v2 no se reabren. Identity v2 cutover permanece: `AdoptStrategy` → `upsertStrategyV2`. Archivos **nuevos** GENERATED usan la fórmula compacta de 91 chars **sin** batch token en el basename; historia no se recanonicaliza.

## Certification

G34 `concurrent-builder-identity` (SDK §13) más P1–P8. Nivel: SOURCE PASS + CONTRACT/concurrency PASS. Tests: purity; encoding Base64URL biyectivo (43 chars, no truncación); publication P1 dos EIK + mismo local stem → names distintos de 91 chars **sin** Campaign FilenameToken; P2 mismo EIK × hosts → mismo name; stem local largo (≥80 chars humanos) sigue ≤128; `go test -race` sobre Adopt v2 y producer-output; NS T7 como evidencia negativa.

No recertificación global MT5. No reabrir B1/B2. Cert física adicional: sólo publication MinIO write-once de GENERATED nuevos. No flota MT5.

## Acceptance

- `CanonicalStrategyID` determina el mismo valor con `HOST_KEY` zeus/hera/kronos/vacío.
- P1: same FlowRun + distinct producers + same basename → distinct ID/KEY de 91 chars, sin Campaign FilenameToken, ambos válidos.
- Published GENERATED nuevo siempre `len≤128`; nunca truncar.
- P2: same producer + different host → same ID/KEY.
- P3: publicación concurrente no usa sibling NS ACK como uniqueness.
- P4–P5: crash/lost PUT reconcilian la misma address; no segundo producer.
- P6: conflicto de contenido → `CONTRACT_CONFLICT`, no rename.
- P7: adopted byte-for-byte.
- P8: regeneración con lineage; origen inmutable.
- Historia no renombrada.
- `DATABASE MIGRATION: NONE`.

## Out of scope

Finalist Model V2 / F-02. Promotion V2. Result Surface V2. membership/ranking. F-03 SQX long-running. magic. version seal. handoff. Echo S0. eligibility Echo. nuevo score model. Slot Pool / fencing / takeover / business timeout MT5. Reabrir B1A/B1B/B2. Tabla o token UUID nuevo. Topology fija de pipeline como identity. Reabrir fórmula `BuilderSupplyBatchRef`. Retiro global de `HOST_KEY` operacional. Ampliar `StageExecutionIdentityView` salvo que NORMAL demuestre que recompute del intent es insuficiente (entonces STOP, no improvisar).

## Evidencia y provenance

Inspección read-only `xKoRx/symphony@db8a022703082fd7ee9d1e15243c5d1b2feaf578`.

- `sqx/core/domain/persistence_identity.go` `NewStageExecutionIdentity`: `StageInstanceKey = hash("stage-instance.v1", TaskPath, StageKey, subject, inputsDigest)`; `ExecutionIntentKey = hash("stage-execution.v1", FlowRunID, slot, Generation)`.
- `sqx/core/runtime/task_path.go` `StructuralTaskPath`: identidad por índices, no nombres.
- `sqx/adapters/overview/binding/subject.go` `NewStageIntent` / `NewStageIntentWithInputs`: Builder generation=1; template mete inputs en identity.
- `sqx/adapters/registry-postgres/stage_execution.go` `ResolveStageExecution` lookup por `execution_intent_key`; INSERT `id := uuid.NewString()`; `convergeStageExecution`. Unique `001_durable_persistence_foundation.up.sql`.
- `sqx/activities/worker/project_activity.go` inserta `resolve_stage_execution` y `claim_output_namespace` antes de `execute_sqx`.
- `sqx/activities/worker/steps/steps.go` resolve Builder; Campaign upload `beforePut=nil`; `dbRegister` `CanonicalStrategyID(filename)`; `rejectBuilderTemplateCanonicalCollisions`.
- `sqx/core/capabilities/persistence.go` `OutputNamespaceOwnershipStore` (owner FlowRun; stage = initial claimant provenance); `StageProducerOutputStore` PK `(stage_execution_id, object_key)`; `SingletonStageProducerOutputStore` comenta keys host-dependent.
- `sqx/adapters/registry-postgres/output_namespace_ownership_test.go` T3/T4/T7 sibling ACK; T8 cross-flow conflict.
- `sqx/adapters/registry-postgres/stage_producer_output.go` insert-once genérico; migration 008 ya existe.
- `sqx/core/domain/canonical_strategy_id.go` `os.Getenv("HOST_KEY")` + `isLikelyHostKey`.
- `sqx/adapters/storage-minio/minio_storage.go` `publishedSQXFileName` / `legacySQXFileName` / `namespaceCampaignBuilderFilename`; `BuildMinIOPath` sin producer.
- `sqx/core/domain/forge_campaign.go` `BuilderSupplyBatchRef`.
- `sqx/core/capabilities/storage.go` `StrategyMeta` hoy: batch + ExactOutputName; sin producer token.
- Frozen: [[2026-09-04-echo-forge-campaign-builder-supply-identity]]. [[2026-08-23-durable-strategy-identity-v2-cutover]]. SDK F01/G34 en [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]].

Wikilink `[[2026-09-04-echo-forge-campaign-builder-supply-identity]]` resuelve a `80-agents/memory/public/decision/symphony/2026-09-04-echo-forge-campaign-builder-supply-identity.md`.

## Límites y contradicciones

Meter FlowRun dentro de `ExecutionIntentKey` no viola el freeze de WaveKey: WaveKey sigue fuera de identity; el token proyectado es el slot durable del producer, no la ola. Si el manager considera que hashear FlowRun en el published basename es OPTION A (execution en identity) prohibida, F-01 queda `BLOCKED — MANAGER DECISION REQUIRED` sin inventar tabla.

`FormatStrategyName` en `sqx/core/utils` y `pkg/sqxutils` aún anexa host en copies locales legacy. F-01 no los toma como authority de Adopt/MinIO durable; no-touch salvo que un caller productivo de publication los use. Si aparece en el hot path, PLAN_CONFLICT.

Builder N-output no usa hoy skip-SQX recovery de singleton (`ExpectedProducerOutput`). F-01 no lo inventa: retry RUNNING re-ejecuta SQX; convergencia la dan EIK + token + SPO + PutIfAbsent. Bytes distintos → P6.
