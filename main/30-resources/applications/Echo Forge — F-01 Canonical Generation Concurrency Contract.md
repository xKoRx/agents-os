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

Baseline de source: `xKoRx/symphony@db8a022703082fd7ee9d1e15243c5d1b2feaf578`. Agents OS origin/master al diseñar: `83506a14f0b850402fbb61d50e90790662fe19f0`.

## Síntesis vigente

### Problema

`CanonicalStrategyID` no es puro: lee `$HOST_KEY` y recorta sufijos alfanuméricos 3–16 según el entorno. La misma entrada puede producir IDs distintos en Zeus versus Hera. El comentario del helper afirma que no consulta el environment; el código sí lo hace.

`HOST_KEY` no es identidad de negocio. En publication, `legacySQXFileName` aún anexa `.hostKey` cuando el basename local no trae la convención instrumento/estrategia (`TestPublishedSQXFileName_LegacyGenericBasenameCollidesByHost`). Eso evitó colisiones físicas de object key entre workers, y también hace que un retry/recovery en otro host publique otra identity.

F-01 debe retirar `HOST_KEY` de Strategy identity y de publication de outputs GENERATED nuevos, sin reintroducir esa colisión y sin renombrar historia.

### Veredicto central — discriminador durable

No se agrega tabla, UUID ni migration. Las authorities existentes cubren el contrato.

| Rol | Authority existente | Qué discrimina | Puede entrar en CanonicalStrategyID |
|---|---|---|---|
| Productor lógico intra-wave | `StageExecutionRef` + claim `OutputNamespaceOwnership` (FlowRun dueño del namespace MinIO sin filename) | Dos FlowRuns distintos no publican el mismo path; retry del mismo FlowRun ACK sin mutar | No. Es execution/ownership, no business identity |
| Generación Campaign | `BuilderSupplyBatchRef` = `{CampaignRef}:g{NNNNNN}` proyectado al basename publicado | Dos olas/campaigns no colapsan el mismo ResultsGroup SQX | Sí, ya está en el published basename antes de `CanonicalStrategyID` |
| Output dentro del productor | ResultsGroup/cohort token `Strategy_X.Y.Z.zN` del archivo SQX | Varios .sqx del mismo Builder job | Sí, como parte del stem publicado. No es GUID nativo |
| Artifact 1:1 | `ExactOutputName` / `StrategyRef` | Addressing de Retester/Optimizer/FinalReretester | No. Addressing, no identity |
| Bytes / crash | `StageProducerOutput` (singleton 1:1) y `PutObjectIfAbsent` + unique v2 | Replay vs conflicto de contenido | No. Recovery authority |
| Infra | `HOST_KEY` / hostname / PID / attempt | Worker físico | No |

Pregunta G34: el discriminador durable de productores concurrentes intra-wave es el **FlowRun dueño del output namespace**, persistido en `sqx.output_namespace_ownership`, no el host. El discriminador durable de strategies GENERATED distintas es el **published basename** ya namespaced por `BuilderSupplyBatchRef` (Campaign) más el ResultsGroup local. Retry del mismo productor reusa `StageExecutionRef` (generation preservada) y el mismo claim; sin sufijo host, object key y canonical id convergen.

`HOST_KEY` permanece operacional fuera de identity/publication GENERATED: boot del worker, ProActiva `maintenance/state/{host_key}`, telemetría. No se elimina globalmente.

### Identity model

**GENERATED.** Strategy nueva de Builder. Identity = `CanonicalStrategyID(published_basename)` con `identity_model_version=2`, unique global. `StrategyRef` lo minta `AdoptStrategy`. No depende de host, PID, Temporal attempt, WorkflowID, RunID ni WaveKey. Campaign: el basename incorpora `BuilderSupplyBatchRef.FilenameToken()` antes del canonicalizer. Generic Builder: sin batch token; unicidad la da el stem publicado más el unique v2; dos FlowRuns del mismo namespace físico fallan en el claim, no mintando un segundo ID.

**ADOPTED.** Strategy histórica ya persistida. Su `canonical_strategy_id` queda byte-for-byte. F-01 no recanonicaliza registry ni objetos. Un filename histórico que ya trae `.zeus`/`.hera`/`.kronos` se conserva opaco si se vuelve a pasar al helper; no se strippea por entorno.

**RE-GENERATED FROM EXISTING STRATEGY/TEMPLATE.** El origen es input/lineage (`StrategyArtifact` con `StrategyRef` + `CanonicalStrategyID` del template). El origen no se renombra ni se muta. Las nuevas strategies son entidades nuevas: nuevo published basename, nuevo canonical id, nuevo artifact, lineage explícito al origen. `rejectBuilderTemplateCanonicalCollisions` ya fail-closed si el output reusa un canonical del cohort template. Stages siguen desacoplados: identity no hardcodea `stage X → stage Y`.

Downstream (Retester/Optimizer/FinalReretester) adopta el `CanonicalStrategyID` del upstream carrier; no reminta identity por filename físico. `ExactOutputName` permanece addressing.

### CanonicalStrategyID — contrato puro

El helper sólo normaliza wrappers documentados sobre un basename:

1. Trabajar sobre `filepath.Base`.
2. Quitar `.sqx` / `.md`.
3. Quitar prefijos WF (`WF_Matrix_-_`, `WF_Matrix-`, `WF_-_`, `WF-`, `WF Matrix - `) hasta idempotencia.
4. Recortar `_robust` sólo si el nombre contiene `Strategy_`.
5. Recortar sufijos `(N)` de 0 a 9.
6. Devolver el resto intacto.

Prohibido: `os.Getenv("HOST_KEY")`; heurística `isLikelyHostKey` que puede mutilar `Strategy_X.Y.Z.z10`; anexar host; resolver colisiones con `(1)`/`(2)`, sufijo host nuevo o UUID random.

### Publication / addressing

`publishedSQXFileName`:

- Si `ExactOutputName` está seteado: usarlo y ignorar host. Sin cambio de contrato.
- Si hay `BuilderSupplyBatchRef`: namespacing Campaign vigente (`namespaceCampaignBuilderFilename`) sobre el stem legacy **sin** anexar host.
- Legacy generic basename: **dejar de anexar** `.hostKey`. El mismo basename local produce el mismo object key en cualquier worker.
- Path MinIO (`BuildMinIOPath`) sigue siendo routing; Wave en PATH no es identity.

Colisión contractual verdadera (dos productores lógicos, mismo published identity, contenido o intent incompatible) → `CONTRACT_CONFLICT`. No rename.

### Concurrency / retry / recovery

Un Builder durable resuelve `StageExecutionRef` (retry/continue-as-new preservan generation). `claim_output_namespace` reserva `(bucket, namespaceKey)` para un FlowRun; retry del mismo FlowRun ACK; otro FlowRun → conflicto y no ejecuta SQX.

Publication GENERATED nueva es host-independent, así que recovery en otro worker reusa object keys. Campaign cap sigue en batch-preflight antes de PUT.

Builder N-output hoy no usa `RecordStageProducerOutput` (`beforePut=nil`). F-01 no agrega producer-output ni migration para Builder: unique v2 + PutIfAbsent + namespace claim + StageExecution recovery de COMPLETED cubren A–F. Si G34 demuestra un crash window no cubierto, STOP y manager; no inventar token nuevo.

Singleton 1:1 (Retester/Optimizer/FinalReretester) ya tiene record-before-put y `ExactOutputName` host-independent. F-01 no los reabre.

### Crash / retry matrix

Notación: SE = StageExecutionRef, NS = OutputNamespaceOwnership, ID = CanonicalStrategyID, KEY = object key MinIO.

**A — Dos producers distintos, misma wave, mismo basename local.** Estado inicial: dos FlowRuns/SE. Authority: NS unique por path de wave/task. Acción: segundo claim. Retry: no aplica al perdedor. Identity/KEY: no se mintan dos. Outcome: `CONTRACT_CONFLICT`. Error: durable contract conflict / duplicate logical producer.

**B — Replay idéntico del mismo producer.** Estado: mismo SE, mismo NS owner, mismos files locales. Authority: NS ACK; Adopt unique ACK; PutIfAbsent ACK. Acción: retry. Identity/KEY: iguales. Outcome: convergencia. Error: none (valid replay).

**C — Crash antes de durable authority.** Estado: SE puede existir; NS/objects/adopt ausentes. Acción: recovery re-ejecuta claim+publish. Identity: se minta una vez al adoptar. Outcome: una strategy. Si SE no se persistió, el resolve recrea la misma identity de slot+generation.

**D — Authority persistida, crash antes de PUT.** Estado: NS claimed; Builder sin producer-output row; objects ausentes. Acción: retry PUT. Identity: aún no adoptada o adopt se reintenta. KEY: misma. Outcome: PutIfAbsent escribe una vez. No mintar otra identity.

**E — PUT exitoso, respuesta perdida.** Estado: object presente; caller no vio ACK. Acción: PutIfAbsent reconcile; Adopt unique. Identity/KEY: iguales. Outcome: ACK. Unknown commit exige recovery read, no segundo mint.

**F — Recovery en otro worker/host.** Estado: mismo SE/NS. Acción: publication sin host. Identity/KEY: idénticos al primer host. Outcome: replay B. Prohibido divergir por `HOST_KEY`.

**G — Authority existente con contenido incompatible.** Estado: unique v2 o PutIfAbsent ve bytes/atributos distintos. Acción: fail-closed. Identity: no se renombra. Outcome: `CONTRACT_CONFLICT`.

**H — Adopted histórica.** Estado: fila v2 con canonical existente, posiblemente con sufijo host opaco. Acción: F-01 no escribe esa fila. Identity: byte-for-byte. Outcome: intacta.

**I — Builder alimentado desde Finalist/template.** Estado: DurableInputs con canonicales origen. Acción: publish nuevas; `rejectBuilderTemplateCanonicalCollisions`. Identity origen intacta; nuevas IDs. Outcome: si colisiona con template → conflicto antes de Adopt.

### Errors / retries

| Clase | Señales | Retry | Mint identity |
|---|---|---|---|
| valid replay | PersistenceAcknowledged idéntico; PutIfAbsent same digest | sí, no-op | no |
| retryable infrastructure | red, timeout, executor | sí | no |
| unknown commit | PersistenceUnknownCommit / ErrUnknownCommit | recovery read | no |
| durable contract conflict | PersistenceContractConflict / ErrContractConflict | no | no |
| malformed durable state | fila inválida al load | no | no |
| physical object missing after authority | NS/adopt sí, probe no | republicar misma KEY | no |
| duplicate logical producer | NS claim de otro FlowRun | no | no |
| duplicate physical basename | mismo KEY, distinto digest | no | no |
| cancellation | cancel del FlowRun/stage | no continuar el árbol | no |

### BWC

IDs adoptados intactos. Objetos históricos legibles. Wrappers WF/`_robust`/`(N)` siguen tolerados en el helper. No rename masivo. No migration. `BuilderSupplyBatchRef` y unique v2 no se reabren. Identity v2 cutover permanece: `AdoptStrategy` → `upsertStrategyV2`.

### Certification

G34 `concurrent-builder-identity` (SDK §13): workers distintos, misma campaign/wave/grupo/ordinal local; retry/crash/recover; producciones distintas no colisionan; replay mismo token; identidad idéntica al variar `HOST_KEY`.

Nivel: SOURCE PASS + CONTRACT/concurrency PASS. Tests unitarios de purity + publication + `go test -race` sobre `ClaimOutputNamespace` concurrente y Adopt v2. Registry real (`output_namespace_ownership_test`, `adopt_strategy` integration) es la prueba de authority durable; concatenar strings no basta.

No recertificación global MT5. No reabrir B1/B2. Cert física adicional: sólo publication MinIO write-once de GENERATED nuevos (object keys host-independent). No flota MT5.

### Acceptance

- `CanonicalStrategyID` determina el mismo valor con `HOST_KEY` zeus/hera/kronos/vacío.
- Dos producers distintos mismo namespace → un owner, conflicto, no dos IDs.
- Mismo producer replay → mismo ID y misma KEY.
- Recovery cross-host → mismo ID/KEY.
- Adopted IDs relevantes byte-for-byte.
- Regeneración: origen inmutable; output nuevo + lineage; colisión con template fail-closed.
- Historia no renombrada.
- `DATABASE MIGRATION: NONE`.

### Out of scope

Finalist Model V2 / F-02. Promotion V2. Result Surface V2. membership/ranking. F-03 SQX long-running. magic. version seal. handoff. Echo S0. eligibility Echo. nuevo score model. Slot Pool / fencing / takeover / business timeout MT5. Reabrir B1A/B1B/B2. Producer-output token nuevo. Topology fija de pipeline como identity. Retiro global de `HOST_KEY` operacional.

## Evidencia y provenance

Inspección read-only `xKoRx/symphony@db8a022703082fd7ee9d1e15243c5d1b2feaf578`.

- `sqx/core/domain/canonical_strategy_id.go` `CanonicalStrategyID` L86–150: `os.Getenv("HOST_KEY")` y strip `isLikelyHostKey`.
- `sqx/adapters/storage-minio/minio_storage.go` `publishedSQXFileName` / `legacySQXFileName`: ExactOutputName ignora host; batch token Campaign; legacy anexa host en basename genérico. Tests `TestPublishedSQXFileName_LegacyGenericBasenameCollidesByHost` y `TestPublishedSQXFileName_ExactOutputNameIgnoresHostAndLocalBasename`.
- `sqx/core/domain/forge_campaign.go` `BuilderSupplyBatchRef` / `FilenameToken`.
- `sqx/core/capabilities/storage.go` `StrategyMeta.BuilderSupplyBatchRef` / `ExactOutputName`.
- `sqx/core/capabilities/persistence.go` `OutputNamespaceOwnershipStore`, `StageProducerOutput`, `SingletonStageProducerOutputStore` (comenta object keys host-dependent).
- `sqx/adapters/registry-postgres/output_namespace_ownership.go` claim atómico FlowRun-owned; `output_namespace_ownership_test.go` concurrent claims.
- `sqx/activities/worker/steps/steps.go` `claim_output_namespace`, Campaign upload `beforePut=nil`, `dbRegister` `CanonicalStrategyID(filename)`, `rejectBuilderTemplateCanonicalCollisions`.
- `sqx/core/domain/persistence_identity.go` `NewStageExecutionIdentity`: retries preservan generation.
- `sqx/adapters/registry-postgres/adopt_strategy.go` unique v2 `ON CONFLICT (canonical_strategy_id)`.
- Frozen: [[2026-09-04-echo-forge-campaign-builder-supply-identity]] (wikilink resuelto; no reconstruido). [[2026-08-23-durable-strategy-identity-v2-cutover]] no toca CanonicalStrategyID/HOST_KEY. SDK F01/G34 en [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]].

Wikilink esperado del prompt: `[[2026-09-04-echo-forge-campaign-builder-supply-identity]]` resuelve a `80-agents/memory/public/decision/symphony/2026-09-04-echo-forge-campaign-builder-supply-identity.md`.

## Límites y contradicciones

El SDK F01 sugiere un `producer_output_token` si un StageExecution contiene varios Builders paralelos. Source en este baseline: un Builder durable = un StageExecution = N archivos. YAGNI: no hay paralelismo intra-SE que exija token nuevo. Si el source futuro introduce varios Builders por SE, F-01 queda corta y hay que STOP, no ampliar en NORMAL.

Campaign `BuilderSupplyBatchRef` prueba separación entre generaciones, no por sí sola intra-wave (ya dicho en el SDK). Intra-wave lo cubre NS ownership + uniqueness del published stem. No contradice el frozen supply-identity: el batch token sigue en identity Campaign; F-01 no lo sustituye por host ni por WaveKey.

`FormatStrategyName` en `sqx/core/utils` y `pkg/sqxutils` aún anexa host en copies locales legacy. F-01 no los toma como authority de Adopt/MinIO durable; no-touch salvo que un caller productivo de publication los use. Si aparece en el hot path, PLAN_CONFLICT.
