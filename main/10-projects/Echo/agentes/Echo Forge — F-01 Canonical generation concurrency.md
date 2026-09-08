---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge — Factory V2 Completion]]"
sprint:
start: 2026-09-07
due:
progress: 0
repo: xKoRx/symphony
jira:
prs:
aliases:
  - F-01 Canonical generation concurrency
  - Echo Forge F-01 implementation
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-07"
updated: "2026-09-07"
---

# Echo Forge — F-01 Canonical generation concurrency

%% Naming: Echo Forge — F-01 Canonical generation concurrency es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — F-01 Canonical generation concurrency
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo Forge — Factory V2 Completion]] · **Repo:** `xKoRx/symphony`
> Subproyecto de implementación de la fase F-01. No es un roadmap independiente. Contrato: [[Echo Forge — F-01 Canonical Generation Concurrency Contract]].

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo Forge — Factory V2 Completion]] enlaza esta fase. El humano sigue el track desde [[Echo — Producto Integrado]].

## 🎯 Objetivo

Hacer `CanonicalStrategyID` puro y la publication GENERATED con **durable producer discrimination** (`ExecutionIntentKey` → producer filename token), cableando Builder a `StageProducerOutput` existente antes del PUT, para que sibling producers intra-wave y retry/recovery cross-host no colisionen ni minten otra strategy. Desbloquea IDs estables para F-04/F-05 sin reabrir B1/B2 ni retirar `HOST_KEY` operacional.

## 📊 Estado actual

- **PLAN READY FOR MANAGER RE-REVIEW.** SPEC corregida in-place (retirado FlowRun/NS como discriminator). TASKS T1.1–T1.4 ajustadas, no duplicadas. Implementación NORMAL **no autorizada**.
- Baseline source: `xKoRx/symphony@db8a022703082fd7ee9d1e15243c5d1b2feaf578` = HEAD = origin/master al diseñar. Foreign dirty de symphony preservado, no tocado.
- Agents OS origin/master analizado: `83506a14f0b850402fbb61d50e90790662fe19f0`. Corrección encima de `419c64084459c9c903061cad0ecf900f33313b09`.
- `DATABASE MIGRATION: NONE`. `GOD REQUIRED: NONE`. Modelo por task: NORMAL.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | feature a fijar por NORMAL desde `master` | `db8a022703082fd7ee9d1e15243c5d1b2feaf578` | [[Echo Forge — Factory V2 Completion]] F-01 | [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] | SPEC corregida; implementación bloqueada a re-review |

## Parent / SPEC / baselines

- Parent: [[Echo Forge — Factory V2 Completion]]
- SPEC: [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] — `VAULT_ROOT/30-resources/applications/Echo Forge — F-01 Canonical Generation Concurrency Contract.md`
- Frozen: [[2026-09-04-echo-forge-campaign-builder-supply-identity]]; [[2026-08-23-durable-strategy-identity-v2-cutover]]; SDK G34/F01 en [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]

## Source map

Identity de producer: `sqx/core/domain/persistence_identity.go` (`NewStageExecutionIdentity`, `ExecutionIntentKey`); `sqx/core/runtime/task_path.go` (`StructuralTaskPath`); `sqx/adapters/overview/binding/subject.go` (`NewStageIntent`, `NewStageIntentWithInputs`); `sqx/adapters/registry-postgres/stage_execution.go` (`ResolveStageExecution`, `convergeStageExecution`).

Publication: `sqx/core/domain/canonical_strategy_id.go`; `sqx/core/capabilities/storage.go` (`StrategyMeta`); `sqx/adapters/storage-minio/minio_storage.go` (`publishedSQXFileName`, `legacySQXFileName`, `namespaceCampaignBuilderFilename`); `sqx/activities/worker/steps/steps.go` (`resolve_stage_execution`, `uploadStrategyResults`, `dbRegister`); `sqx/activities/worker/project_activity.go` (pipeline resolve/claim; fail-closed de ports); `sqx/activities/worker/pipeline/step.go` (`Capabilities`).

Recovery/authority: `sqx/core/capabilities/persistence.go` (`StageProducerOutputStore`, `OutputNamespaceOwnershipStore`); `sqx/adapters/registry-postgres/stage_producer_output.go`; `sqx/adapters/registry-postgres/output_namespace_ownership.go` (T7 = no uniqueness de producer); `sqx/adapters/registry-postgres/adopt_strategy.go`; `sqx/core/domain/forge_campaign.go` (`BuilderSupplyBatchRef`, wave namespace only).

## Planned diff

Modificar:

- `sqx/core/domain/canonical_strategy_id.go`
- `sqx/core/domain/canonical_strategy_id_test.go`
- `sqx/core/domain/persistence_identity.go` (helper puro `ProducerFilenameToken` desde `ExecutionIntentKey`; no nueva entity)
- `sqx/core/domain/persistence_identity_test.go` (dos TaskPaths → EIK distintos; retry same EIK; token determinista)
- `sqx/core/capabilities/storage.go` (`StrategyMeta` producer filename token)
- `sqx/adapters/storage-minio/minio_storage.go`
- `sqx/adapters/storage-minio/minio_storage_test.go`
- `sqx/activities/worker/steps/steps.go` (poblar token desde el mismo intent de resolve; Builder `beforePut=RecordStageProducerOutput`; Campaign conserva cap)
- `sqx/activities/worker/steps/steps_test.go` y/o tests Builder de publication existentes (no debilitar)
- `sqx/activities/worker/project_activity.go` (durable Builder fail-closed si falta `StageProducerOutputStore`)
- `sqx/activities/worker/pipeline/step.go` (port genérico o type-assert documentado; el comentario actual «Builder never requires them» queda falso)
- `sqx/activities/worker/steps/steps_builder_template_test.go` (si el fixture de colisión depende del helper/nombre publicado)

Crear sólo si hace falta cohesión de tests (no production nueva):

- `sqx/adapters/storage-minio/published_generation_concurrency_test.go`

No crear paquetes, entities SDK ni migrations. No tocar fórmula `BuilderSupplyBatchRef`. No cambiar semántica T7 de ownership.

Motivo de ampliar el diff respecto de `canonical_strategy_id.go` + `minio_storage.go`: sin `steps.go` / `storage.go` / activity ports el token no llega al publication path (`beforePut` sigue `nil` y `StrategyMeta` no transporta el discriminator).

## No-touch

B1A/B1B/B2; Slot Pool; fencing; takeover; magic; seal; handoff; Finalist V2; Result V2; F-03 timeouts SQX; Echo S0; `ExactOutputName` singleton salvo regresiones; fórmula `BuilderSupplyBatchRef`; unique v2 schema; tabla `stage_producer_outputs` / migration 008; semántica `ClaimOutputNamespace`; `FormatStrategyName` legacy salvo PLAN_CONFLICT; HOST_KEY de boot/ProActiva/telemetry; foreign dirty symphony.

## Execution sequence

T1.1 primitive (purity + token helper) → T1.2 publication GENERATED con durable producer discrimination y record-before-put → T1.3 adoption/regeneration bajo la identidad corregida → T1.4 G34 P1–P8. No implementar T1.2 sin T1.1 verde.

## Dependencies

Ninguna fase Echo/Forge posterior. Independiente de F-02/F-03/E-01. Reusa B2 CLOSED sólo como freeze: no reabrir.

## ✅ Tareas

> [!note]+ Ownership
> Board `#owner/agent`. Cada ítem es una TASK atómica para NORMAL tras autorización del manager.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [ ] T1.1 CanonicalStrategyID puro y ProducerFilenameToken #owner/agent #type/dev #area/echo
> - [ ] T1.2 Publication GENERATED con durable producer discrimination #owner/agent #type/dev #area/echo
> - [ ] T1.3 Adopted BWC y regeneración template #owner/agent #type/dev #area/echo
> - [ ] T1.4 G34 P1–P8 concurrency/crash certification #owner/agent #type/dev #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## Atomic tasks

Contrato de cada TASK: objetivo, archivos, entrada, cambio, invariantes, tests, DONE, deps, stop. Decisiones de diseño: solo la SPEC. Se conservan cuatro tasks: T1.2 deja de ser «quitar HOST_KEY» y pasa a implementar publication con discrimination; T1.4 certifica P1 sibling producers, no sólo cross-host.

### T1.1 CanonicalStrategyID puro y ProducerFilenameToken

- **Modelo:** NORMAL
- **Objetivo:** `CanonicalStrategyID` / `CanonicalStrategyFilename` deterministas e independientes de `$HOST_KEY`; helper puro que deriva el producer filename token de `ExecutionIntentKey`.
- **Archivos/símbolos:** `sqx/core/domain/canonical_strategy_id.go` (`CanonicalStrategyID`, `isLikelyHostKey`); `canonical_strategy_id_test.go`; `sqx/core/domain/persistence_identity.go` (`ProducerFilenameToken` o nombre equivalente junto a `ExecutionIntentKey`); `persistence_identity_test.go`.
- **Entrada:** helper actual env-dependiente; `ExecutionIntentKey` ya durable; wrappers WF/`_robust`/`(N)` vigentes.
- **Cambio:** eliminar lectura de environment y el strip heurístico de host. Conservar wrappers documentados. Preservar el resto del basename, incluidos sufijos históricos. Añadir token `p`+hex(64) desde `ExecutionIntentKey` canónico; rechazar keys no canónicas. No I/O.
- **Invariantes:** idempotencia; no anexar host; no mutilar `Strategy_X.Y.Z.z10`; adopted filenames con `.zeus` opaco se re-leen iguales; dos `TaskPath` → EIK/token distintos; mismo slot+generation → mismo token.
- **Tests:** misma entrada con HOST_KEY zeus/hera/empty/otro → mismo ID; z0 vs z10; WF/_robust/(N); path completo; empty; dos TaskPaths same FlowRun; retry same generation.
- **DONE:** tests del paquete `sqx/core/domain` verdes; cero `os.Getenv` en `canonical_strategy_id.go`; token puro cubierto.
- **Deps:** ninguna.
- **Stop:** si se necesita persistir un UUID/tabla para el token → BLOCKED manager.

### T1.2 Publication GENERATED con durable producer discrimination

- **Modelo:** NORMAL
- **Objetivo:** publication GENERATED usa el producer token de T1.1; deja de anexar HOST_KEY; cablea Builder a `StageProducerOutputStore` existente antes del PUT.
- **Archivos/símbolos:** `sqx/core/capabilities/storage.go` (`StrategyMeta`); `sqx/adapters/storage-minio/minio_storage.go`; `minio_storage_test.go`; `sqx/activities/worker/steps/steps.go` (`uploadStrategyResults`, meta population); `project_activity.go`; `pipeline/step.go`; tests de steps de upload/Builder.
- **Entrada:** T1.1 DONE. `TestPublishedSQXFileName_LegacyGenericBasenameCollidesByHost` hoy exige KEY distintas por host. Campaign `beforePut=nil`. Generic durable Builder usa `UploadFromDiskExact` sin pre-put.
- **Cambio:** poblar producer token recomputando el mismo `NewStageIntent`/`NewStageIntentWithInputs` del resolve. Namespacing producer en `publishedSQXFileName` (mismo insertion point que batch). Dejar de anexar `.hostKey`. Durable Builder (Campaign y generic): `beforePut=RecordStageProducerOutput` genérico, no singleton. Campaign conserva `beforeBatch` cap. Fail-closed sin store. `ProducerContextDigest` según SPEC. ExactOutputName intacto.
- **Invariantes:** `BuilderSupplyBatchRef` sigue namespacing Campaign; PutIfAbsent write-once; no `(N)` como resolver de retry; mismo EIK × hosts → mismo published name; distinct EIK × same local basename → names distintos; sin token resoluble → `CONTRACT_CONFLICT`.
- **Tests:** table-driven hosts h0/z0/k0 convergentes; dos tokens + mismo basename; batch token diferencia olas y convive con producer token; ExactOutputName sigue ignorando host y token; beforePut llamado por candidato Builder; replay SPO ACK / conflicto de digest.
- **DONE:** publication GENERATED host-independent y producer-discriminated; Builder record-before-put verde; tests MinIO+steps verdes.
- **Deps:** T1.1.
- **Stop:** si publication productiva aún sale de `FormatStrategyName` → PLAN_CONFLICT. Si el enlace exige tabla nueva → BLOCKED.

### T1.3 Adopted BWC y regeneración template

- **Modelo:** NORMAL
- **Objetivo:** db_register/Adopt siguen identity = canonical del published basename **con** producer token en GENERATED nuevos; adopted intactos; regeneración (P8) no reusa ID del origen.
- **Archivos/símbolos:** `steps.go` `dbRegister`, `rejectBuilderTemplateCanonicalCollisions` — modificar production **sólo** si un caller viola la SPEC; `steps_builder_template_test.go`; tests Adopt v2 existentes no se debilitan.
- **Entrada:** T1.2 DONE. Collision template ya fail-closed. Template inputs ya entran en `StageInstanceKey`.
- **Cambio:** tests de regeneración (origen inmutable, output nuevo, EIK/token distintos del source); adopted byte-for-byte; no cambiar unique v2; no recanonicalizar historia sin token.
- **Invariantes:** identity v2; lineage en `StrategyArtifact`; no topology stage X→Y en el ID.
- **Tests:** `TestDBRegister_BuilderTemplateCollisionFailsBeforeAdopt` sigue fail-closed; caso feliz de template con IDs distintos bajo la fórmula corregida; no rename histórico.
- **DONE:** regeneración y BWC cubiertos; production de steps sin rediseño de Adopt.
- **Deps:** T1.2.
- **Stop:** si hace falta mutation de filas históricas o migration → BLOCKED.

### T1.4 G34 P1–P8 concurrency/crash certification

- **Modelo:** NORMAL
- **Objetivo:** certificar P1–P8 de la SPEC contra authorities reales. P1 (`same FlowRun + distinct producers + same basename`) es obligatorio; cross-host (P2) no basta.
- **Archivos/símbolos:** tests T1.1–T1.3; `output_namespace_ownership_test.go` T7 como evidencia negativa (NS no es uniqueness); `stage_producer_output_test.go`; Adopt concurrency; `go test -race` en esos paquetes.
- **Entrada:** T1.3 DONE.
- **Cambio:** tests/cert only salvo bug de T1.1–T1.3. Ejercitar: P1 two TaskPaths same FlowRun same basename; P2 same EIK different HOST_KEY; P3 no usa sibling NS ACK como unique; P4–P5 same address after crash/lost PUT; P6 conflict; P7 adopted; P8 regeneration. Batch refs distintos → IDs distintos (wave namespace).
- **Invariantes:** no skip/masking; no recert MT5; no tocar B1/B2; no “arreglar” T7 para que siblings CONFLICT.
- **Tests:** `go test -race` `./sqx/adapters/registry-postgres` (ownership + producer-output + adopt) y `./sqx/adapters/storage-minio` / `./sqx/core/domain` / steps filtrados a estas superficies. Registry embebido cuando el harness exista; si Maven/DNS blocked, documentar DEGRADED como el cutover v2, no fingir PASS.
- **DONE:** G34 CONTRACT/concurrency PASS o evidencia DEGRADED infra explícita. SOURCE PASS de T1.1–T1.3. P1 explícito.
- **Deps:** T1.1–T1.3.
- **Stop:** crash window que exija UUID/tabla nueva → BLOCKED manager, no implementar.

## Gates

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G1 | pending | Ejecutar T1.1–T1.4 según SPEC; dejar review | Manager acepta SPEC+diff+tests G34/P1–P8 | F-01 DONE; desbloquea sellado F-04 sobre IDs estables |

## Tests / certification

Suite por task arriba. Suite final: purity + token + publication P1/P2 + Builder beforePut + NS T7 negativo + Adopt unique + template collision + `go test -race`. Cert: SOURCE + G34 unit/registry. PHYSICAL MinIO write-once de GENERATED si los tests de storage cubren PutIfAbsent; no flota MT5.

## Risks

- Tests actuales de `legacySQXFileName` fallarán al quitar host: hay que invertir el assert, no skip.
- Harness Postgres embebido puede degradar G34 registry: no declarar PRODUCT PASS con mocks de unique.
- `isLikelyHostKey` ya puede romper `.z10`: T1.1 debe cubrirlo.
- Fakes de `Control` en tests de Builder deberán implementar `StageProducerOutputStore` o el fail-closed es correcto.

## Definition of Done

SPEC cumplida. `DATABASE MIGRATION: NONE`. HOST_KEY fuera de CanonicalStrategyID y de publication GENERATED. Producer token derivado de `ExecutionIntentKey` en published GENERATED nuevos. Builder record-before-put sobre store existente. HOST_KEY operacional intacto. Adopted intactos. P1–P8 PASS o DEGRADED infra explícito. Foreign dirty symphony intacto. Sin prompt NORMAL ejecutado antes del re-review.

## Unlocks

F-04 puede sellar versiones sobre IDs estables. F-05 golden no depende de retirar sufijos adoptados. F-02/F-03 no bloquean ni quedan bloqueados.

### Paquete autónomo Fase 1 — Canonical generation concurrency

**Misión exacta**

Implementar T1.1–T1.4 contra [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] en baseline `db8a022703082fd7ee9d1e15243c5d1b2feaf578`, sin decisiones de identity abiertas.

**Precondiciones verificables**

Manager aceptó esta nota + SPEC corregida. Symphony HEAD revalidado = baseline o STOP. Foreign dirty preservado. NORMAL autorizado explícitamente. Hoy: **no autorizado**.

**Lectura obligatoria**

`VAULT_ROOT/30-resources/applications/Echo Forge — F-01 Canonical Generation Concurrency Contract.md`

`VAULT_ROOT/10-projects/Echo/agentes/Echo Forge — F-01 Canonical generation concurrency.md`

SPEC frozen [[2026-09-04-echo-forge-campaign-builder-supply-identity]]. Source map de esta nota. No redescubrir discriminador. No usar OutputNamespaceOwnership como uniqueness de producer.

**Decisiones cerradas**

Logical producer = Builder StageExecution. Discriminador durable = `ExecutionIntentKey`. Token filename = `p`+hex. Identity GENERATED = `CanonicalStrategyID(published basename)` con batch Campaign + producer token. HOST_KEY no es identity. Builder publication cablea `StageProducerOutputStore` existente. Sin migration. Sin UUID/tabla nueva. Sin topology en identity. Ver SPEC.

**Implementación paso a paso**

Ejecutar T1.1, gate tests helper+token; T1.2, gate publication+beforePut; T1.3, gate BWC/template; T1.4, gate P1–P8. Actualizar esta nota al avanzar. No despachar F-02.

**Archivos esperados**

modify: lista Planned diff. create: test file opcional de publication. no-touch: lista No-touch.

**No tocar**

B1/B2, Finalist, magic, seal, handoff, F-03, Echo S0, migrations, HOST_KEY operacional, foreign dirty, fórmula batch, semántica NS T7.

**Spikes permitidos**

Ninguno de arquitectura. Si FormatStrategyName está en hot path: PLAN_CONFLICT y parar.

**Tests y asserts**

Los de T1.1–T1.4 y P1–P8 de la SPEC. Prohibido t.Skip de G34/P1.

**Entregables/Gate G1**

Diff acotado, tests, evidencia G34/P1–P8, nota actualizada a review. Gate G1 → review.

**Handoff a Fase N+1**

No hay fase 2 en este subproyecto. Handoff: F-01 DONE hacia el padre Factory V2.

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — Canonical generation concurrency
GATE_REQUERIDO=none
TAREAS=T1.1-T1.4
SALIDA=source diff F-01 + G34/P1-P8 evidence + nota en review
STOP=NO NORMAL IMPLEMENTATION AUTHORIZED YET
```

El bloque de despacho no sustituye la SPEC ni autoriza ejecución.

## 📆 Bitácora

- **2026-09-07** — TOP diseñó F-01 contra symphony `db8a022` y Agents OS `83506a14`. SPEC + TASKS persistidas. Discriminador entonces: OutputNamespaceOwnership. NORMAL no autorizado.
- **2026-09-07** — Corrección TOP in-place tras manager `CORRECTION REQUIRED`. Discriminador = `ExecutionIntentKey`. FlowRun/NS ownership insuficiente (T7). T1.2/T1.4 reabiertos. Planned diff ampliado a publication path. NORMAL no autorizado.

## 🧭 Decisiones

- Ver [[Echo Forge — F-01 Canonical Generation Concurrency Contract]]. Esta nota no duplica la matriz.

## 🔗 Docs / Links

- [[Echo Forge — Factory V2 Completion]]
- [[Echo Forge — F-01 Canonical Generation Concurrency Contract]]
- [[Echo — Producto Integrado]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[2026-09-04-echo-forge-campaign-builder-supply-identity]]

## 💡 Ideas

### Backlog de ideas

- Ninguna dentro de F-01.

### Motivos / principios

- KISS/YAGNI: reusar `ExecutionIntentKey` y `StageProducerOutput`. Fail-closed en conflictos. Identity ≠ host. Producer ≠ FlowRun.

### Memoria pública / interna

- **Memoria pública:** SPEC Resource + decisión supply-identity.
- **Memoria interna:** no duplicar checkpoint.
- **Motivo:** el padre conserva el roadmap F-01…F-05.
