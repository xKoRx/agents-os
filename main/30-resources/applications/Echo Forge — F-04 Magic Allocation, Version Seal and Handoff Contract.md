---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo — E-01 Canonical SDK Foundation S0]]"
  - "[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]"
  - "[[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]"
  - "[[Echo Forge — F-01 Canonical Generation Concurrency Contract]]"
  - "[[Echo Forge — F-02 Finalist Model V2 Contract]]"
  - "[[Echo Forge — F-03 SQX Long-Running Contract]]"
last_verified: "2026-09-12"
confidence: verified
aliases:
  - F-04 SPEC
  - Magic allocation version seal handoff
  - Echo Forge F-04
  - HandoffManifestV1 producer
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo — Live Platform V1]]"
entities:
  - "[[Echo Forge]]"
  - "[[xKoRx/symphony]]"
  - "[[xKoRx/echo]]"
tags:
  - kind/resource
  - area/echo
  - project/echo-forge
created: "2026-09-10"
updated: "2026-09-12"
---

# Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract

Esta Resource es el contrato técnico de `F-04 — Magic Allocation, Version Seal and Handoff`. Define qué debe quedar cierto. La ejecución vive en [[Echo Forge — F-04 Magic allocation, version seal and handoff]]. No es un tutorial. No crea un tercer dominio Integration.

Baseline de source F-04: `xKoRx/symphony@d645ed6c2f438995d636a8213b1e4a3f5f26cbea` (`feature/f04-magic-version-handoff`; T2.1–T2.10 implementados; PHYSICAL 0.2.97 reveló C4). F-01 implementation authority: `0509342439cfbaa048839088787458dde1ed1b05`. Magic V1 ancestor: `ea8be76c4587b2d00e4cad8cf2a67c4fd8e6680f`. Dirty foráneo `phase4_performance.json` preservado. S0 certificado: `xKoRx/echo@91671f6f46ffa889a79aed0979cb3b4e5821ed33`. Consumer E-04: `xKoRx/echo@a99f9a63354bbe72219d1e590bb93757ed08e45e`. Agents OS: vault local **sin** `.git`; lookup de SHA live **degraded**; última authority durable de journal: `f1070bec27db3ca415fe24f3c3576139674b7e09`. No se inventa SHA de vault.

`DATABASE MIGRATION: 015_strategy_magic_version_seal_handoff`. Tablas nuevas write-once; cero reescritura destructiva de historia. No backfill de magic `888111`/`11111`.

## Síntesis vigente

### Problema

T1 entregó allocator Magic V1, StrategyVersion, `HandoffManifestV1` producer y fakeconsumer. T2 cerró compile EvaluationRef, caller Magic durable y HTTP E-04. **C4 (2026-09-12):** el PHYSICAL `0.2.97` / FlowRun `eb2ebaa0-3056-445a-9d46-0953c25b2516` falló las 4 Apply attempts en `ParseMagicV1AllocationIdentity` porque Magic V1 parseaba `CanonicalStrategyID` como `<INSTRUMENT>_<D>_...` y F-01 emite una identidad opaca. Cero filas `strategy_magic`, cero seals, cero manifests — sin data repair. C4 congela autoridades explícitas de instrument/direction y separa Magic legado de allocated. T2.11–T2.13 siguen OPEN. E-04 runtime/deploy/join es one-shot separado después del golden Forge.

### Veredicto central

Un único pipeline contractual, con dos puertas distintas:

```text
robust selection
→ ALLOCATE (CAS, 1:1 StrategyRef↔magic, no recycle)
→ APPLY/STAMP (allocated magic)
→ READBACK SQX XML + MQ5
→ VERIFY (readback == allocated)
→ COMPILE + VERIFY ARTIFACT BYTES
→ SEAL StrategyVersion (S0 recipe)
→ [solo Finalist V2] HandoffManifestV1 write-once
→ thin delivery adapter
```

**Finalist V2 es admisión a SEAL/HANDOFF, no a allocation.** Allocation ocurre **antes de Apply** para la cohorte Apply (Live Authority §3 + hipótesis frozen del padre). Reservar magic y no usarlo (no-finalista) es válido; no se libera.

S0 es autoridad de wire. Forge consume `github.com/xKoRx/echo/v3/sdk/contracts` pin `91671f6f`. No copiar tipos parecidos. `C()`, `H()`, tagged digests y legacy Forge `HashIdentity` (newline) permanecen estrictamente separados. **HashIdentity legacy con newline NO equivale a `H()`.**

`HANDOFF_CREATED ≠ INGESTED ≠ PROVISIONED ≠ ACTIVE`.

### CC owner gate

**`CC_MISSING_OWNER_GATE`.** O2 catálogo CC sigue OWNER PRODUCT DECISION ([[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]] C-7; SDK § Magic semántico CC). No existe authority canónica aprobada. TOP **no** inventa rangos.

| Antes de CC | Después de CC |
|---|---|
| Store/CAS/replay/unicidad, stamp/readback, seal, manifest, adapter+fakeconsumer, CONTRACT/CONCURRENCY, SOURCE | PHYSICAL allocation real de magics de producción desde el catálogo |
| `MagicCandidateSource` de test/fixture | `MagicCandidateSource` de catálogo CC; fail-closed si el instrumento no tiene código |
| Production `Allocate()` físico retorna `CC_MISSING_OWNER_GATE` | Allocation real + stamp/compile/readback/seal físicos |

NORMAL puede dejar el source listo sin efectuar allocation física de producción.

## Ownership (no se rediseña)

Forge posee: Finalist membership, magic allocation, artefactos, StrategyVersion sealing, handoff production, delivery status durable.

Echo posee: validated ingestion, PromotionRecord, RuntimeBinding, provisioning, eligibility, capital, activation.

Forge **NO**: escribe DB Echo; calcula eligibility; asigna capital; activa estrategias; recalcula membership en Echo.

No-touch: F-01 (`ExecutionIntentKey`, HOST_KEY, adopted IDs, StrategyRef UUID); F-02 (membership ≠ Top N); B1/B2 (MT5 ownership, Slot Pool, fencing, takeover); F-03 Temporal lifetime / SQX long-running.

## Source map @ `382f4ba`

### Magic hoy — NO durable allocator

| Superficie | Authority actual |
|---|---|
| TaskSpec `ApplySelectedRunTaskConfig.MagicNumber` | `sqx/core/runtime/config.go`; required en `mt5_task_config.go` |
| Apply durable | `ApplicationConfig.MagicNumber` → `automator.properties` `strategy.magic_number=` (`durable_apply_selected_run_physical.go`) |
| Java stamp | `EchoForgeRobustRunExporter` parchea XML `MagicNumber` |
| Legacy | ETCD `strategy/magic_number` default `"888111"` (`robust_activity.go`) |
| PostgreSQL | **cero** columnas/constraints de magic (migrations 001–014) |
| Unicidad | **no existe**; N estrategias pueden compartir `888111` |
| Readback | **no existe**; se asume requested==applied |
| MT5 compiler | no toca magic; `.mq5` hereda Variables del `.sqx` vía `SourceCode.generate` |

Constantes históricas: template SQX `11111`; convención Symphony `888111`; stubs `12345`. **BWC: no reciclar ni unique-allocate `11111` ni `888111`.**

### Artefactos / compile

Apply output: `durable/apply-selected-run/v1/{flow}/{strategy}/{stage}/strategy.sqx` + SHA-256. Compile: `.mq5` → `.ex5` + `.compile.log` (`artifact_compiler.go`). `DurableArtifactRef` existe. **Compile EvaluationRef no existe todavía en runtime** (T2); el producer S0 ya exige el campo.

`CanonicalConfig` hoy usa `domain.HashIdentity` (newline). Eso **no** entra al seal S0.

### Handoff hoy

`adapters/echo-api` ausente. `ActEchoIngest` stub sin artefactos. FEAT-SQX-ECHO-INGESTION BLOQ. Durable paths ya prohíben latest; legacy Apply elige último `.sqx` por mtime — F-04 no usa ese path.

E-04 ([[Echo — E-04 Forge Ingestion E1]]): **INTEGRATED** `@ a99f9a63354bbe72219d1e590bb93757ed08e45e`. T21/AC-37 POST-INTEGRATION espera golden auténtico de Forge. CONTRACT Forge permanece en `fakeconsumer`. HTTP client real es T2.9; no inventar path distinto de `POST /api/v1/forge/promotions` + GET by-key.

## Contratos S0 (consumo, no copia)

Pin: `xKoRx/echo/v3/sdk/contracts@91671f6f`.

| Receta | Tag / forma | Uso F-04 |
|---|---|---|
| `H()` | `wire.HashTagged` = SHA-256 de JSON array `[tag,...fields]` → `sha256:`+64hex | refs nuevas |
| `D()` | `Digest(tag, x) = H(tag, Canonicalize(x))` | payload |
| `C()` | `wire.Canonicalize` / `EncodeCanonical` | body |
| `HashIdentity` | `namespace + "\n" + join(parts, "\n")` | **solo** Apply Evaluation legacy; **nunca** seal/handoff |
| `StrategyVersionRef` | `H("echo-strategy-version.v1", [canonical, platform, exec_sha, inputs_sha, runtime_sha, deps_sha])` | seal identity |
| `allocation_ref` | `H("forge-magic-allocation.v1", [registry_namespace, canonical, magic_decimal])` | identidad de allocation |
| `IdempotencyKey` | `H("forge-echo-ingest.v1", [ns, wave_key, canonical, version_ref])` | write-once ingest |
| `payload_digest` | `H("forge-echo-payload.v1", [canonical_body])` | write-once content |
| Write-once | `DetectSealedConflict(ref, digestA, digestB)` | same digest converge; distinct → `CONTRACT_CONFLICT` |

Magic wire: **string decimal** positivo signed int64 (`1..9223372036854775807`). G20: valores >int32 válidos en ingestión. G21: token JSON number inseguro = INVALID_WIRE. Binding MT4 (rango) no es F-04.

`required_capabilities` del manifest incluye `forge-echo-ingestion.v1`. Producer: `{id: "echo-forge-handoff", version: "1.0.0"}`. Registry namespace autenticado: `forge-live` (fixtures S0; no es campo del body).

`ArtifactRef` S0: `{store_id, bucket, key, kind, schema_version?, size, sha256, platform?, producer_ref?}`. Integridad = sha256+size+kind/schema/platform; locator no es identidad.

## Magic allocation contract

### Identidad

| Campo | Valor frozen |
|---|---|
| Namespace | `forge-live` (S0 `registry_namespace`) |
| Key lógica | `(registry_namespace, strategy_ref)` — UUID F-01 |
| Mapping | **1:1 StrategyRef ↔ magic**; 1:N StrategyVersion sobre el mismo magic |
| Owner | Forge registry PostgreSQL |
| Store | `sqx.strategy_magic` (migration 015) |
| `allocation_ref` | `H("forge-magic-allocation.v1", [ns, canonical_strategy_id, magic_decimal])` |
| `assigned_at` | audit only, never identity |

### Constraints

- `UNIQUE (registry_namespace, strategy_ref)`
- `UNIQUE (registry_namespace, magic_decimal)`
- `UNIQUE (allocation_ref)`
- `CHECK` magic decimal positivo que cabe en int64
- FK `strategy_ref` → `sqx.strategies` (identidad F-01)
- **No recycle.** DELETE prohibido en hot path. Reserva sin uso permanece.

Reserved non-allocatable (históricos compartidos, no únicos): `11111`, `888111`. El candidate source **nunca** los entrega.

### Transacción / CAS / replay

```text
AllocateMagicV1(ns, strategy_ref, canonical):
  0. SELECT canonical_strategy_id, instrument, direction FROM sqx.strategies WHERE id = strategy_ref.
     Missing/empty → FAIL CLOSED. canonical row ≠ argument → CONTRACT_CONFLICT.
     Never parse CanonicalStrategyID for instrument/direction.
  1. Map instrument via sqx.magic_instruments (exact instrument_id). Unknown → INSTRUMENT_CODE_MISSING.
     Map direction via MagicV1DirectionFromStrategy. Unknown/ambiguous → FAIL CLOSED.
  2. SELECT existing by (ns, strategy_ref).
     If found: DecodeMagicV1(existing.magic); if III or D ≠ current inputs → CONTRACT_CONFLICT;
     if existing.canonical ≠ argument → CONTRACT_CONFLICT; else return existing (no counter increment).
  3. candidate = Magic V1 Next(YYMM UTC, instrument_code, D, shared sequence). Never reserved 11111/888111.
  4. INSERT row. allocation_ref = H("forge-magic-allocation.v1",[ns,canonical,magic])
  5. ON CONFLICT (ns, strategy_ref) → reread winner and apply step 2 conflict checks.
  6. ON CONFLICT (ns, magic) → next candidate, bounded retries (N=32) then MAGIC_EXHAUSTED.
  7. Never random. Never MAX+1. Never hostname/worker identity. Never wrap/recycle.
```

| Crash | Authority | Retry |
|---|---|---|
| Before commit | no row | sí: Allocate de nuevo |
| After commit | row visible | replay step 1 |
| Outcome unknown | SELECT first; INSERT only if absent; UNIQUE es la prueba | sí, idempotente |

Dos identidades distintas **nunca** reciben el mismo magic en el namespace. El mismo `(ns, strategy_ref)` converge al mismo magic.

`MagicCandidateSource` de producción **es** el catálogo Magic V1 (`sqx.magic_instruments` + counter mensual). Tests inyectan enteros fixture sólo en el allocator genérico pre-V1. El path F-04 productivo es `AllocateMagicV1`.

## F-04 C4 — Explicit Magic Allocation Semantics

Defecto: `ParseMagicV1AllocationIdentity` en `sqx/core/domain/magic_v1.go` extrae instrument/direction desde `CanonicalStrategyID` como `<INSTRUMENT>_<D>_...`. F-01 CLOSED mantiene ese ID opaco (`<token>_<token>` Base64URL). PHYSICAL `0.2.97` → `unknown direction token` → fail closed antes de INSERT. F-01 no se reabre. El layout Magic V1 `YYMMIIIDSSS` no cambia. PostgreSQL sigue siendo la única autoridad de concurrencia.

`DATABASE MIGRATION: NONE` para C4. 015 ya tiene `strategy_ref` FK + `canonical_strategy_id` + `magic_decimal` (encodes III+D). 016 ya tiene catálogo + counter `(YYMM, instrument_code)`. Instrument/direction durables ya viven en `sqx.strategies`. No hay `CC_MISSING_PERSISTENCE_AUTHORITY`. No inventar migration 017.

### Q1 — Instrument authority

| Slot | Frozen |
|---|---|
| Type | `text` NOT NULL en `sqx.strategies.instrument`; domain `domain.Instrument` |
| Field | `sqx.strategies.instrument` |
| Producer | `AdoptStrategy` ← `StrategyIntent.Instrument` ← `WorkflowSpec.Instrument` (`json:"instrument"`) en `steps.go` db_register |
| Persistence | PostgreSQL `sqx.strategies`; inmutable en replay: `strategyV2AttributeConflict` si cambia |
| Consumer | `ControlPlane.AllocateMagicV1` via SELECT by `strategy_ref`; luego `InstrumentCode` → `sqx.magic_instruments.instrument_id` exacto |
| Normalization | `TrimSpace` only; catalog lookup exacto; sin case-fold, sin alias GOLD/XAU, sin regex de filename |
| Errors | empty/missing row → FAIL CLOSED (`ErrInvalidArguments` / `ErrContractConflict`); unknown id → `ErrInstrumentCodeMissing`; XAUUSD → code `001` |

No usar FlowRun intent, EvaluationEvidence scope, Apply input ni MemberProof como autoridad de allocation. Esas superficies copian el mismo `WorkflowSpec.Instrument` pero no son el store 1:1 StrategyRef.

### Q2 — Direction authority

| Slot | Frozen |
|---|---|
| Source | `sqx.strategies.direction` (`text` NOT NULL), mismo producer que instrument (`WorkflowSpec.Direction` json `"direction"`, productively `L`/`S`) |
| Representation | token de estrategia, no digit Magic V1, no `CanonicalStrategyID`, no `contracts.OperationSide` (S0 sólo LONG/SHORT; BOTH no es wire S0) |
| Mapper | `domain.MagicV1DirectionFromStrategy(string)` after TrimSpace+ToUpper: `L`\|`LONG` → 1; `S`\|`SHORT` → 2; `B`\|`BOTH` → 3 |
| Unknown | empty, `LS`, `LONG/SHORT`, lowercase leftovers, any other token → FAIL CLOSED `ErrInvalidMagicNumber`; never default LONG |
| BOTH | codec V1 digit 3 reserved; tests may persist `B`; no productive flow is required to emit BOTH |

`MagicV1DirectionCode` (LONG/SHORT/BOTH only) se unifica o delega al mapper; no se deja un segundo vocabulario productivo.

### Q3 — Allocation API

Signature vigente se conserva:

```text
MagicAllocatorV1.AllocateMagicV1(ctx, registryNamespace, strategyRef, canonicalStrategyID) (MagicAllocationRecord, error)
```

| Slot | Frozen |
|---|---|
| Producer | `DurableApplySelectedRunActivity.resolveEffectiveConfig` cuando `UseDurableMagicAllocation=true`; caller `runDurableApplySelectedRun` ya setea el flag |
| Consumer | `ControlPlane.AllocateMagicV1` (`sqx/adapters/registry-postgres/magic_v1.go`) |
| Boundary | activity `apply_selected_run`; request actual `DurableApplySelectedRunRequest` (StrategyRef + CanonicalStrategyID; **no** se agregan instrument/direction al request para no duplicar la fila durable) |
| Fields used | ns `forge-live`; `strategy_ref`; `canonical_strategy_id` (allocation_ref recipe + conflict vs row, **never parsed**); instrument/direction from `sqx.strategies` |
| Persistence | INSERT `sqx.strategy_magic` (015); counter `sqx.magic_monthly_counters` (016) only on first commit |
| Errors | `ErrInvalidArguments`, `ErrInstrumentCodeMissing`, `ErrMagicMonthlyCapacityExhausted`, `ErrReservedMagic`, `ErrMagicExhausted`, `ErrContractConflict` (canonical/instrument/direction mismatch on replay), `ErrUnknownCommit` unchanged |
| Retry | UNKNOWN_COMMIT: SELECT only, no second Next/INSERT in the same invocation (G1 C1 frozen) |
| Card | N StrategyRefs → N allocations; shared counter `(YYMM, instrument_code)`; direction does not partition sequence |

Retirar `ParseMagicV1AllocationIdentity` del path productivo. Tests que fabrican canonical `XAUUSD_L_H1_...` dejan de ser authority.

> [!note]+ Implementation evidence (NORMAL C4, 2026-09-12)
> Implementado en `xKoRx/symphony@bba833d` sobre `d645ed6` (pushed fast-forward). Q1–Q4 implementados tal cual se congelaron: step 0 SELECT `sqx.strategies` por StrategyRef (missing row → `ErrInvalidArguments`; canonical ≠ argumento → `ErrContractConflict`), mapper `MagicV1DirectionFromStrategy`, catálogo exacto TrimSpace-only, replay/conflict gate `DecodeMagicV1` III+D tras `AllocateMagic` (cubre replay, identity-race y UNKNOWN_COMMIT reconciliation), sin migration. **Residual flaggeado al manager:** el parser retirado del allocation path conserva un único consumer no-allocation — `forge_seal_handoff.go` `strategyIdentityFromCanonicalID` (bloque de identidad del manifest, fuera del scope C4 autorizado); con un ID F-01 opaco ese bloque falla cerrado en seal time, sin corromper datos; su corrección exige decidir la fuente durable del observed timeframe/side del manifest.

### Q4 — Replay / conflict

same StrategyRef + same instrument/direction (row) → same magic, no sequence increment, month-boundary replay preserves prior magic.

same StrategyRef + existing row + different instrument and/or direction vs `DecodeMagicV1(existing.magic)` III/D → `CONTRACT_CONFLICT` terminal, no Next, no UPDATE of `magic_decimal`.

Verificación en `AllocateMagicV1` **antes** de devolver replay y tras identity-race reread. 015 no guarda instrument/direction en `strategy_magic`; III+D del magic + catálogo inmutable 016 bastan. No nueva columna.

Canonical argument ≠ row `canonical_strategy_id` o ≠ existing allocation canonical → `CONTRACT_CONFLICT`.

### Requested vs legacy vs allocated

Tres conceptos, nunca colapsados:

| Nombre | Campo | Rol F-04 |
|---|---|---|
| Allocated | `sqx.strategy_magic.magic_decimal` | única autoridad de stamp F-04 |
| Legacy/template TaskSpec | `ApplySelectedRunTaskConfig.MagicNumber` (`json:"magic_number"`) | input de stamp del path **legacy** (`EffectiveConfig`); `ValidateWorkflowSpec` lo exige hoy; valores históricos `888111`/`11111` son defaults compartidos **no unique** |
| Source SQX XML MagicNumber | bytes del artefacto/template | sobrescrito por Apply; nunca requested; nunca allocated |
| Requested contractual | **no existe** como campo distinto en source actual | D9 se corrige: no promover `magic_number` a request |

`AllocatedEffectiveConfig` **deja de comparar** TaskSpec.MagicNumber contra allocated. Stamp = allocated siempre en path F-04. `888111` en el example flow se sobrescribe; no es `CONTRACT_CONFLICT` de request. El guard `requested ≠ allocated → FAIL CLOSED` permanece como invariante **si** un owner introduce después un campo explícito distinto; C4 no inventa ese campo.

Legacy `EffectiveConfig` (flag off) no se toca.

### Multi-strategy

Producto: N StrategyRefs en la misma Apply cohort reciben N allocations independientes. Un `magic_number` compartido en el TaskSpec del flow **no** fuerza el mismo allocated. Robust selection = 1 es **solo** receta de certificación física futura, no límite de arquitectura.

### Example flow / physical fixture (no se arregla en esta sesión)

`input/example/config.json` con `magic_number: 888111` no es candidato F-04 por sí solo (también puede traer promotion 1.0.0). Futuro PHYSICAL: XAUUSD, dirección única conocida (`L` o `S`), promotion `2.0.0`, robust selection = 1, sin requested contractual. No fabricar golden en C4/NORMAL.

### E-04 (bloque aparte)

T2.13 OPEN. Tras golden Forge auténtico: one-shot separado Echo E-04 runtime config/deploy + join real. No mezclar con C4. No modificar Echo ahora.

## Stamp + readback contract

Cuatro valores, nunca colapsados:

| Nombre | Fuente |
|---|---|
| requested | **ausente en C4**; no es TaskSpec `magic_number` |
| allocated | `sqx.strategy_magic.magic_decimal` |
| legacy TaskSpec magic | `ApplySelectedRunTaskConfig.MagicNumber` — stamp del path legacy; en F-04 se ignora como request y se sobrescribe |
| applied/effective | **solo** readback, nunca TaskSpec ni requested |
| readback sources | (1) XML `MagicNumber` del `.sqx` de output Apply; (2) `input … MagicNumber` del `.mq5` exportado |

Secuencia:

```text
ALLOCATE → APPLY/STAMP allocated (TaskSpec magic_number is not a request gate)
→ READBACK SQX XML
→ VERIFY == allocated
→ EXPORT MQ5
→ READBACK MQ5
→ VERIFY == allocated
→ COMPILE
→ VERIFY bytes (size+sha, compile 0 errors, source mq5 sha match)
→ SEAL
```

`.ex5` no se parsea para magic. La prueba de magic compilado es: el `.mq5` readback-igual fue el source del compile (SHA match) y el compile log es `Result: 0 errors`.

Mismatch readback ≠ allocated: **FAIL CLOSED. NO SEAL. NO HANDOFF.** No crear StrategyVersion sobre valores sólo solicitados.

Retry stamp: solo recovery Apply ya existente (RUNNING sin producer sellado). Tras producer sellado con mismatch: `CONTRACT_CONFLICT` terminal. No reseal.

## Compile Evaluation contract (frozen 2026-09-12)

`compile_evaluation_ref` **no** es SHA de EX5, key de log, request/workflow ID, `ExecutionIntentKey` ni HashIdentity. Es un `domain.EvaluationRef` producido por Durable Foundation.

Fuente: compile físico (`ArtifactCompiler.Compile` / `mt5_compile_artifact` en `sqx-mt5-queue`) ya publica EX5+log durables pero **no** abre StageExecution ni `PutEvaluation`. El patrón vivo a reusar es `persistMT5ReconcileV1` en el worker padre.

| Campo | Frozen |
|---|---|
| StageKey | `mt5_compiler@mt5-compile.v1` (`CanonicalStageKey` sobre TaskSpec.Type vivo) |
| Subject | STRATEGY / StrategyRef UUID; digest de `{schema:mt5-compile-strategy-subject.v1, strategy_ref}` — artifact SHA no entra |
| InputEvaluationRefs | role `source_evaluation` = carrier `EvaluationRef` exacto (Evaluation SQX que el exporter ya cargó). Compile persist no busca Apply. El assembler F-04 exige `Stage.Key=apply_selected_run` |
| Scope | `{schema:mt5-compile-scope.v1, platform:MetaTrader5, compiler:"MetaEditor64 /portable"}` |
| Producer | component `sqx-mt5-compile`; contract_version y build_ref `mt5-compile.v1` |
| Artifacts | INPUT `STRATEGY_MQ5`; OUTPUT `EX5`; EVIDENCE `LOG` |
| Payload | `{schema:mt5-compile-payload.v1, result:success, error_count:0}` |
| ConfigurationSnapshot | `{schema:mt5-compile-config.v1, compiler:"MetaEditor64 /portable", platform:MetaTrader5}` — no `{}` |
| Variant | `{schema:mt5-compile-variant.v1, operation:compile}` |
| EvaluationRef | `domain.NewEvaluationRef(stageRef, subject.Digest, scopeDigest, "mt5-compile.v1")` |
| Cardinality | 1 success StageExecution → 1 EvaluationRef; 0 → no seal; >1 → CONTRACT_CONFLICT |
| Persist seam | `executeMT5ArtifactTask` after V1 compile success → `mt5_compile_persist_v1` on **sqx-worker**, never mt5-queue |
| Consume seam | `runFinalistPromotion` → `forge_seal_handoff_v1` with exact refs |
| MIGRATION 017 | **NO** |

Success: `VerifyCompiledArtifactForSeal` before `ResolveStageExecution`. Functional failure: no StageExecution, no success Evaluation. Infra/cancel: retry, no fake success. UNKNOWN_COMMIT: exact `LoadEvaluation` recovery. Temporal retry no crea otro compile semántico.

`UseDurableMagicAllocation` debe activarse en `runDurableApplySelectedRun`; el flag existe y el caller productivo hoy lo deja false.

## StrategyVersion seal

Seal **sólo** con bytes/evidencias S0:

- `canonical_strategy_id` (F-01, sin HOST_KEY)
- `target_platform` = `MetaTrader5` (V1; MT4 binding range no es ingestión)
- `executable_sha256` = digest de bytes `.ex5`
- `effective_inputs_sha256` = digest S0 del **artefacto de inputs efectivos** (JSON canónico `C()` de `{allocated_magic, readback_magic, runs_count, oos_percent, symmetric_variables, apply_config_schema}` **después** de readback). **Prohibido** usar `HashIdentity` de Apply como este campo.
- `runtime_context_sha256` = digest S0 del contexto de runtime declarado (platform + compiler/producer refs exactos, sin host/worker)
- `dependencies_sha256` = digest S0 del set ordenado de `ArtifactIdentity` de dependencias (source `.sqx`/`.mq5` roles)

`StrategyVersionRef = H("echo-strategy-version.v1", [those six strings])`.

Store: `sqx.strategy_versions` PK `version_ref`, write-once. Same-input replay: same ref, `DetectSealedConflict` nil. Distinct content ⇒ distinct ref (content-addressed). Intentar persistir otro `payload` bajo el mismo ref → `CONTRACT_CONFLICT`. Inmutable. No apunta a “latest”. Rank/score/broker/account/locator **no** entran a la identidad (S0).

Seal puede ocurrir cuando bytes+readback pasan; **handoff** exige además membership Finalist V2. Un sellado no-finalista no se entrega.

## HandoffManifestV1

Producer Forge **después** de seal + membership V2. Usa tipos S0 exactos (`HandoffManifestV1.Validate`).

Inputs: StrategyVersion sealed, `MagicAllocation`, Finalist V2 Decision + `MemberProof` (requested/observed instrument/timeframe == Strategy; tested executable/inputs == version), `ArtifactRef`s, build lineage (Apply/Compile EvaluationRef, DecisionRef, source artifact). Score/rank **nunca** redefinen membership (G02).

Write-once key = `IdempotencyKey`. Payload digest = `PayloadDigest`. Replay mismo key+digest → converge. Distinct digest → `CONTRACT_CONFLICT` (G07). G23: otra Decision bajo conflicto de contenido. G24: otro `wave_key` para el mismo `(ns, decision, version)` → `SOURCE_BINDING_CONFLICT`. G22: membership vacío → **cero** manifests y **cero** deliveries (indelegable). G04: segunda promoción reusa version/magic. G05: mismos Strategy/magic, bytes nuevos → nuevo VersionRef.

El manifest **no** activa Echo.

Forge persiste el body canónico write-once (`sqx.handoff_manifests`) para que un retry no regenere bytes distintos.

## Thin Forge → Echo adapter

Puerto de aplicación (Forge):

```text
HandoffIngress.Deliver(ctx, ns, *HandoffManifestV1) (PromotionRecord, httpStatus, error)
```

- Un handoff individual explícito. Cero latest/folder query. Cero writes a DB Echo. Cero provisioning.
- CONTRACT: `fakeconsumer.Consumer.Ingest` del pin S0.
- INTEGRATION: cliente E-04 del **mismo** pin, cuando E-04 certifique endpoint. No inventar URL/schema provisional.

Estados durables Forge (`sqx.handoff_deliveries`):

| Estado | Significado |
|---|---|
| `HANDOFF_CREATED` | manifest write-once local |
| `INGESTED` | receipt S0 `status=INGESTED` |
| `CONTRACT_CONFLICT` / `SOURCE_BINDING_CONFLICT` | 409, sin mutar el sellado |
| `UNAVAILABLE` | Echo down, pre-commit |
| `UNKNOWN_RECEIPT` | timeout post-commit / outcome unknown |

Retry: `UNAVAILABLE` / timeout **pre-commit** sí. Timeout **post-commit**: **no** re-POST ambiguo; quedar `UNKNOWN_RECEIPT` hasta lectura idempotente (GET-by-key) cuando E-04 la ofrezca. Si E-04 aún no tiene read: no fingir INTEGRATION PASS.

## Failure / retry matrix

| Caso | STATE | RETRY? | AUTHORITY | Terminal? | Side effects |
|---|---|---|---|---|---|
| Magic already allocated same identity | ALLOCATED | no-op replay | `strategy_magic` row | no | none |
| Magic UNIQUE conflict (other identity) | allocating | yes, next candidate | UNIQUE magic | `MAGIC_EXHAUSTED` after N | none until commit |
| CC missing (production physical) | unallocated | no physical | CC gate | non-terminal for CONTRACT; terminal for PHYSICAL | none |
| DB outage | any | yes (transient) | no commit | no | none |
| Commit outcome unknown | allocating/sealing/handoff | yes after SELECT | UNIQUE + DetectSealedConflict | no | none extra |
| Stamp failure (SQX/Java) | APPLY RUNNING | yes via existing Apply recovery | StageExecution | no until sealed mismatch | no seal |
| Stamp/readback mismatch | APPLY produced | no reseal | XML/MQ5 vs allocated | **yes** `CONTRACT_CONFLICT` | no seal, no handoff |
| Compile failure | compile | yes technical; no if source sha already sealed mismatch | compile log | yes if 0-errors required and missing | no seal |
| Artifact missing | pre-seal | yes fetch durable | `DurableArtifactRef` | yes if authority says present | no seal |
| Digest mismatch (bytes vs declared) | pre-seal | no | ArtifactRef.Identity | **yes** | no seal |
| Seal replay same content | SEALED | no-op | version_ref + digest | no | none |
| Seal conflict different content same ref | SEALED | no | DetectSealedConflict | **yes** | no mutate |
| Handoff replay same digest | HANDOFF_CREATED/INGESTED | no-op | IdempotencyKey | no | none |
| Handoff conflict different digest | HANDOFF_CREATED | no | DetectSealedConflict | **yes** 409 | no mutate |
| Echo unavailable | HANDOFF_CREATED | yes | adapter | no | none |
| Echo timeout pre-commit | HANDOFF_CREATED | yes | no receipt | no | none |
| Echo timeout post-commit / unknown | `UNKNOWN_RECEIPT` | **no re-POST** | wait idempotent read | no until read | do not double-ingest |

## BWC

| Historia | Acción F-04 |
|---|---|
| Estrategias con magic `888111`/`11111` compartido | no unique-allocate esos valores; no reciclar; no backfill masivo |
| StrategyVersion inexistente | no backfill; seal solo path nuevo con readback |
| Manifests antiguos | no existen; no adapter V1 disfrazado (G03 es corpus S0, no Forge history rewrite) |
| F-02 V1 history | readable; handoff **nuevo** solo membership V2 |
| Old Apply outputs | SHA Apply sigue authority de stage; no se reinterpreta como StrategyVersion |

Dual path: Apply legacy (TaskSpec magic, sin unique) permanece ejecutable hasta que el flow F-04 esté cableado. El path F-04 **no** sella ni entrega magics compartidos. Campaigns nuevas en F-04 no tratan `888111` como requested. El path F-04 **sobrescribe** `magic_number` legado con allocated.

## DATABASE MIGRATION: `015_strategy_magic_version_seal_handoff`

Next after `014_finalist_promotion_v2`. Up only adds tables. Down drops only those tables.

### `sqx.strategy_magic`

Columns: `registry_namespace TEXT NOT NULL`, `strategy_ref UUID NOT NULL`, `canonical_strategy_id TEXT NOT NULL`, `magic_decimal TEXT NOT NULL`, `allocation_ref TEXT NOT NULL`, `assigned_at TIMESTAMPTZ NOT NULL`.
UNIQUE: `(registry_namespace, strategy_ref)`, `(registry_namespace, magic_decimal)`, `(allocation_ref)`.
CHECK: magic decimal positivo int64. FK strategy_ref. **No UPDATE** de magic_decimal/allocation_ref.

### `sqx.strategy_versions`

PK `version_ref TEXT`. Columns: strategy_ref, canonical_strategy_id, target_platform, executable_sha256, effective_inputs_sha256, runtime_context_sha256, dependencies_sha256, payload_digest, sealed_at, execution_manifest TEXT. Write-once. UNIQUE natural key of the six identity fields (redundant with content-addressed PK).

### `sqx.handoff_manifests`

PK `idempotency_key TEXT`. payload_digest, canonical_body JSONB, wave_key, strategy_ref, version_ref, decision_ref, created_at. Write-once.

### `sqx.handoff_deliveries`

PK `idempotency_key` FK. state CHECK (`HANDOFF_CREATED|INGESTED|CONTRACT_CONFLICT|SOURCE_BINDING_CONFLICT|UNAVAILABLE|UNKNOWN_RECEIPT`), receipt JSONB, last_error, updated_at.

Brownfield test: strategies preexistentes **sin** fila magic; Apply legacy sigue; F-04 Allocate sobre ellas crea fila nueva **distinta** de `888111`. Rollback: down.sql. Restart: UNIQUE hace el replay. **C4: ninguna migration nueva.** 015/016 no-touch.

## Certificación

### SOURCE

- Ownership: cero writes Echo DB; cero eligibility/capital/activation.
- Cero latest/folder query como autoridad.
- Cero ranking-as-membership (F-02).
- Cero `HashIdentity` en recetas S0 (`H`/`D`/`StrategyVersionRef`/`allocation_ref`/`payload_digest`).
- Test de desigualdad: mismo payload `HashIdentity` ≠ `H()`.
- C4: cero parse de `CanonicalStrategyID` para instrument/direction; `ParseMagicV1AllocationIdentity` ausente del path productivo.

### CONTRACT

- Allocation uniqueness + CAS + replay (same identity converges; different unique).
- Stamp/readback exacto; mismatch no sella.
- Seal determinista + conflict.
- Manifest write-once.
- Corpus S0 G04–G10 y G19–G25. **G22:** producer 0 POST / 0 manifests si membership vacío (indelegable).
- `fakeconsumer` pin `91671f6f`: G06 201→200, G07 409, G24 SOURCE_BINDING_CONFLICT, G35 crash replay.
- Non-effects: provisioning/activation/capital = false.
- **C4 gates** (NORMAL, `-race` where allocation/concurrency): opaque F-01 CanonicalStrategyID does not parse and still allocates; XAUUSD→001; unknown instrument fail closed; alias GOLD/xauusd fail closed; L→1 S→2 B→3; unknown direction fail closed; same StrategyRef replay same magic without sequence increment; month-boundary replay preserves magic; changed instrument → CONTRACT_CONFLICT; changed direction → CONTRACT_CONFLICT; concurrent distinct refs unique magics sharing `(YYMM,instrument)` counter; TaskSpec nil/888111/11111 does not become requested and allocated proceeds; reserved never allocated; N StrategyRefs → N allocations; Apply/readback SQX+MQ5 exact; UNKNOWN_COMMIT semantics preserved.

### CONCURRENCY

- Concurrent Allocate distinct StrategyRefs → magics distintos.
- Concurrent Allocate same StrategyRef → mismo magic.
- Crash/unknown commit: SELECT-then-INSERT.
- G34 identity tuples del corpus donde aplique a refs S0 (no reabrir F-01).
- C4: direction does not partition the monthly sequence; N concurrent distinct refs share `(YYMM, instrument_code)`.

### PHYSICAL

Tras NORMAL C4 + review de source, un one-shot physical **nuevo** publica release Symphony por `release-authority → deploy_release.sh --release-only → deployer-watcher → MinIO → Stager`. Candidato mínimo: XAUUSD, dirección única conocida, promotion `2.0.0`, robust selection = 1 (receta de certificación, no límite de producto), sin requested contractual. Probar Magic allocation → Apply → SQX/MQ5 readback → compile → EvaluationRef → StrategyVersion → Finalist V2 → HandoffManifest. Materializar golden auténtico. **No ejecutar PHYSICAL en C4.** E-04 runtime/deploy/join es one-shot posterior (T2.13).

Host mínimo: (1) SQX/sqcli con licencia válida — expired → STOP owner, sin trial-key; (2) MetaEditor64 `/portable` en worker `sqx-mt5-queue`; (3) PG control plane + Mongo evidence + object store. No convertir viewers read-only en workers. Lab con magic fixture no es PHYSICAL PASS.

### INTEGRATION

E-04 consumer READY `@ a99f9a6`. T21/AC-37 y T2.13 esperan golden auténtico **después** de C4+PHYSICAL Forge. No mezclar E-04 runtime config/ETCD/gateway con C4. **No fingir INTEGRATION PASS con mock.**

## Invariantes / STOP

NORMAL no decide architecture. STOP/PLAN_CONFLICT si: se pretende que Echo posea magic; se cambie S0; se invente endpoint incompatible con S0; se reabran F-01/F-02/B1/B2; se use MAX+1/random/hostname; se selle sin readback; se use HashIdentity como `H()`; se parseé CanonicalStrategyID para instrument/direction; se vuelva el ID parseable; se limite cardinality de selection a 1; se cree migration 017; se debilite UNKNOWN_COMMIT o readback.

`GOD REQUIRED: NONE`.

## Evidencia y provenance

- Symphony C4 baseline `d645ed6c2f438995d636a8213b1e4a3f5f26cbea`; **C4 implementation `bba833d7b57c767d6ce5ebfeae7a7b71b5785782` (2026-09-12, pushed, `-race` PASS, sets rojos idénticos a baseline)**; F-01 `0509342`; Magic V1 `ea8be76`; `origin/master` `0b9742b` ancestro; dirty foráneo `phase4_performance.json` preservado.
- PHYSICAL trigger: release `0.2.97`, FlowRun `eb2ebaa0-3056-445a-9d46-0953c25b2516`, workflow `sqx-main-v1-6c30394a`, 4 Apply fail `ParseMagicV1AllocationIdentity`, 0 allocations/seals/manifests.
- S0 `91671f6f`; E-04 consumer `a99f9a6` (T2.13 blocked by runtime/config, out of C4).
- D16 compile Evaluation frozen 2026-09-12; D17 C4 explicit allocation inputs frozen 2026-09-12; MIGRATION 017 NO; C4 migration NONE.

## Límites y contradicciones

- El one-liner de producto `FINALIST → ALLOCATE → STAMP` se interpreta como **capacidad de entrega** (solo un Finalist sale hacia Echo). La secuencia técnica frozen es allocation-before-Apply. No contradice S0.
- CC ausente no bloquea CONTRACT; bloquea PHYSICAL de allocation de producción.
- E-04 INTEGRATED `@ a99f9a6`: CONTRACT ≠ INTEGRATION. T21 espera golden auténtico de Forge **después** de C4. Runtime ETCD/gateway E-04 es blocker separado (T2.13).
- Echo local checkout puede no estar en el pin S0; el pin se lee por `git show` sin modificar echo.
