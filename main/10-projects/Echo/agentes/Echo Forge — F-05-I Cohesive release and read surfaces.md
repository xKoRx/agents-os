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
start: 2026-09-13
due:
progress: 57
repo: xKoRx/symphony
jira:
prs:
aliases:
  - F-05-I
  - Echo Forge F-05-I
  - release prep read surfaces
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-13"
updated: "2026-09-16"
---

# Echo Forge — F-05-I Cohesive release and read surfaces

%% Naming: Echo Forge — F-05-I Cohesive release and read surfaces es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — F-05-I Cohesive release and read surfaces
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo Forge — Factory V2 Completion]] · **Repo:** `xKoRx/symphony`
> Preparación de implementación de F-05 (split F-05-I desarrollo / F-05-C certificación diferida). SPEC: [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]. Veredicto objetivo: `F-05-I IMPLEMENTED / SOURCE VERIFIED`. Nada físico se marca PASS.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre humano tiene la tarea puente `#type/supervision`. Las fases internas no inundan el cockpit.

## 🎯 Objetivo

Dejar inspectable, sin abrir bases a mano y sin publicar nada: matriz determinística de release por capacidad, read surface CLI JSON (campaña/run/estrategia/matrix) sobre read models existentes, funnel projection honesta, conformance checklist y manifest template para F-05-C. Usar sólo outputs/fixtures existentes; `fixture != authentic physical golden`.

## 📊 Estado actual

- **Planificación TOP completa (2026-09-13):** SPEC frozen, tareas atómicas F05I-T1…T7, allowed files freeze, matriz de tests congelada. NORMAL puede ejecutar sin decisiones arquitectónicas.
- **Baseline:** `xKoRx/symphony@b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` (HEAD `origin/feature/f04-magic-version-handoff`; release `0.2.98`). Branch objetivo `codex/f05-release-prep` desde el SHA exacto. El checkout local puede estar divergido (`9fad768` no contiene C5): siempre fetch + branch por SHA.
- **Decisiones frozen:** `DATABASE MIGRATION: NONE`; arquitectura CLI JSON (sin HTTP); funnel como proyección pura; release matrix = artefacto declarativo validado; sin writes runtime.
- **Implementación T2–T4 (2026-09-16):** T2, T3 y T4 en estado tablero **Review** en `codex/f05-release-prep` (commits `7d073b3`, `65c879a`, `d77342d`; branch publicada en GitHub, HEAD remoto `d77342d`). Distinción de estado: IMPLEMENTATION REPORTED + SOURCE VERIFIED BY AGENT · MANAGER REVIEW PENDING · PHYSICAL CERTIFICATION NOT RUN. Tests enfocados unit + persistencia embedded-postgres PASS, `-race` PASS, vet PASS. Físico: nada certificado. Pendiente: aprobación manager de T2–T4 y ejecución de T1, T5, T6, T7.
- **Corrección T2 (2026-09-16, commit `3da8b47`):** defecto confirmado por manager en la paginación de campañas: el predicado tuple `(created_at, id) < ($1,$2)` compara `id` descendente contra el orden contractual `created_at DESC, id ASC`, perdiendo silenciosamente filas empatadas en `created_at` con `id > cursor.id`. Corregido a `created_at < $1 OR (created_at = $1 AND id > $2)` en `forge_campaign_list.go` (sin tocar orden, cursor, firma, validaciones ni esquema). Test de regresión `TestListForgeCampaignsPersistenceTieTimestampsKeysetTraversal` (embedded-postgres, limit=1, grupo de empate + cruces de timestamp, orden exacto, sin pérdida/duplicados, página final vacía): falla contra el predicado anterior, PASS con la corrección. T2 permanece en Review; manager review pending.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `codex/f05-release-prep` (creada desde SHA; publicada en origin 2026-09-16) | `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` | [[Echo Forge — Factory V2 Completion]] F-05 | [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]] | NORMAL EN CURSO: T2–T4 en Review (manager review pending), T1/T5–T7 pendientes |

## 🧩 Subproyectos

Sin subproyectos; fases internas = tareas F05I-T1…T7 abajo.

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> Este board muestra `#owner/agent`. El humano sigue el curro desde [[Echo — Producto Integrado]].

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [ ] F05I-T1 Release matrix: paquete validador + artefacto `deploy/release-matrix.json` #owner/agent #type/dev #area/echo
> - [r] F05I-T2 Read ports + implementaciones PG (campaign list, stage list, participaciones, versiones/handoff reads) — implementada 2026-09-16 (commit `7d073b3`), corrección de paginación keyset en empates (commit `3da8b47`), manager review pending #owner/agent #type/dev #area/echo
> - [r] F05I-T3 Funnel projection pura (topología dinámica, orden determinístico) — implementada 2026-09-16 (commit `65c879a`), manager review pending #owner/agent #type/dev #area/echo
> - [r] F05I-T4 Read services: strategy inspect + stage timeline + campaign list service (provenance por refs exactos) — implementada 2026-09-16 (commit `d77342d`), manager review pending #owner/agent #type/dev #area/echo
> - [ ] F05I-T5 CLI `sqx-flowkit` subcomandos inspect + wiring (push-output intacto) #owner/agent #type/dev #area/echo
> - [ ] F05I-T6 Handoff F-05-C: read-surface contract doc + conformance checklist + cert manifest template #owner/agent #type/dev #area/echo
> - [ ] F05I-T7 Verificación completa enfocada (build/tests/race/vet/diff-check/BWC/fixtures) + evidencia #owner/agent #type/dev #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label] of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any){dv.paragraph("_Sin tareas._");}}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## 📋 Tareas atómicas (freeze TOP 2026-09-13)

Orden por dependencia. Cada tarea lista objective / allowed files / inputs / requirement / tests / negative assertions / done / stop. Global: repo `xKoRx/symphony`, branch `codex/f05-release-prep` desde `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` (`git fetch origin` y verificar `git rev-parse origin/feature/f04-magic-version-handoff` == baseline; si difiere materialmente o el SHA no existe: `STOP — MANAGER REVIEW — BASELINE_MOVED`). Prohibido: push release, `deploy_release.sh`, stager, writes DB, migrations, tocar `internal/di`, `deployer/`, `deploy/manifest.json`, contratos frozen F-01…F-04/S0/B1A/B1B/B2. Todos los tests usan fixtures sintéticas etiquetadas (`fixture != authentic physical golden`).

### F05I-T1 — Release matrix (validador + artefacto) — contrato corregido Planning C1 2026-09-16

- **Objective:** schema `sqx-release-matrix.v1` en código puro + artefacto declarado con las capacidades y estados de verdad inicial, embebido en el binario.
- **Allowed files:** `sqx/core/releasematrix/releasematrix.go`, `sqx/core/releasematrix/releasematrix_test.go`, `sqx/core/releasematrix/release-matrix.json`. **Prohibido `deploy/`** (C1.1: es el WatchRoot del deploy pipeline).
- **Inputs:** SPEC §Release matrix contract CORREGIDO (ubicación C1.1, carga portable C1.2, dimensiones/estados C1.3/C1.4, autoridades C1.5, contenido de verdad inicial congelado, guard tests); [[Echo Forge — Factory V2 Completion]] y [[Echo + Echo Forge — Deferred Certification Backlog]] como fuente de evidencia.
- **Requirement:** tipos frozen: `Status` (DONE|OPEN|DEFERRED|NOT_APPLICABLE), `Dimension` (implemented|source_verified|released|deployed|physically_certified|cross_lane_certified), `EvidenceKind` (git|tests|release_manifest|deployment_proof|runtime_observation|certification_record|cross_lane_receipt|none), `State {status, evidence, evidence_kind, gate omitempty, as_of omitempty}`, `DeployTarget {target, release, release_present OBSERVED|NOT_OBSERVED, process RUNNING|NOT_OBSERVED, evidence, as_of omitempty}`, `Capability {capability, contract_refs[], producer_paths[], persistence_authority, read_surface, required_refs[], implementation_sha, states map[Dimension]State, deploy_targets[] omitempty}`, `Matrix {schema "sqx-release-matrix.v1", capabilities[] orden ASC}`. API: `Embedded()/LoadEmbedded()/Parse/Load(path)/Validate` + `//go:embed release-matrix.json`; marshal canónico indent-2 + newline (artefacto committed == salida del marshal, test byte a byte). Validaciones: schema exacto; ids únicos y ordenados; refs ≥1; producer_paths sin wildcards; `implementation_sha ^[0-9a-f]{7,64}$` o vacío; evidence siempre no vacío; DONE sin `gate` y sin `evidence_kind=none`; DONE en released/deployed/physical/cross-lane exige `as_of YYYY-MM-DD`; physical DONE exige `certification_record` y cross-lane DONE exige `cross_lane_receipt`; DEFERRED exige `gate ^CERT-[A-Z0-9]+(-[A-Z0-9]+)*$`; `deployed.status=DONE` ⇒ `deploy_targets ≥1`; target OBSERVED ⇒ `release` no vacío; estados jamás derivados entre dimensiones. 17 filas con contenido de verdad inicial tal como lo congela la SPEC (allowlist histórica física DONE: b1a/b1b/b2/f03; F-04/pipeline/release-pipeline/f05i físico ∈ {OPEN,DEFERRED}).
- **Tests:** unit validador ok/corrupt/enum inválido/duplicado/desorden/wildcard/DEFERRED sin gate/DONE con gate/physical DONE sin record o sin as_of/deployed DONE sin targets/target OBSERVED sin release; guard de contenido committed (allowlist histórica; F-04 y f05i sin física DONE; gates CERT-* correctos); determinismo de marshaling (idempotente byte a byte); embebido == artefacto del repo (`LoadEmbedded` vs `Load` del mismo dir en test).
- **Negative assertions:** el validador NO deriva dimensiones entre sí; ninguna fila nueva con física DONE fuera de la allowlist; ningún estado nuevo fuera de los enums frozen.
- **Done:** `go test ./sqx/core/releasematrix/...` PASS; artefacto válido y canónico.
- **Stop:** si el contenido exigiera declarar física DONE fuera de la allowlist histórica para ser coherente → `STOP — MANAGER REVIEW — FROZEN_CONTRACT_COLLISION`; si necesitara un cuarto estado o séptima dimensión → STOP con contradicción concreta (SPEC §Invariantes).

### F05I-T2 — Read ports + PG implementations

- **Objective:** ports read-only nuevos + SELECTs en el adapter existente (archivos nuevos, cero edits a stores existentes).
- **Allowed files:** `sqx/core/capabilities/forge_inspect_query.go` (+ `_test.go`), `sqx/adapters/registry-postgres/forge_campaign_list.go` (+ `_test.go`), `stage_execution_list.go` (+ `_test.go`), `flow_run_strategy_list.go` (+ `_test.go`), `strategy_handoff_reads.go` (+ `_test.go`). Si una fixture brownfield nueva es imprescindible: `sqx/adapters/registry-postgres/postgrestest/testdata/f05i_inspect_synthetic.sql`.
- **Inputs:** SPEC §Read surface contract; schemas migrations 001/011/015 (`flow_run_strategies`, `forge_campaigns`, `stage_executions`, `strategy_versions`, `handoff_manifests`, `handoff_deliveries`).
- **Requirement:** ports: `ForgeCampaignListReader.ListForgeCampaigns(ctx, limit, cursor)` (orden `created_at DESC, id ASC`; cursor opaco `(created_at,id)`); `StageExecutionListReader.ListStageExecutionsByFlowRun(ctx, flowRunRef)` (orden `created_at, stage_instance_key`; expone status/error_code/error_message/started_at/finished_at/subject/generation/temporal cols); `FlowRunParticipationReader.ListParticipationsByFlowRun` + `ByStrategy` (orden `participated_at, flow_run_id`); `StrategyProvenanceReader.ListStrategyVersions(strategyRef)` (orden `sealed_at, version_ref`) + `ListHandoffByStrategy(strategyRef)` (orden `created_at, idempotency_key`, incluye delivery state). Implementaciones sobre `ControlPlane` con `observe(...)` + `requireDB` + `ValidatePersistenceContext` como los reads existentes. Read-only: sin INSERT/UPDATE, sin outcome.
- **Tests:** persistence con harness postgrestest (brownfield + fixture sintética): happy path, ausencia (found=false), orden determinístico, cursor paginación, límites.
- **Negative assertions:** sin writes (assert SQL sólo SELECT en tests de statements si aplica); ref malformado → error invalid arguments sin query.
- **Done:** focused `go test ./sqx/adapters/registry-postgres/... -run 'TestListForgeCampaigns|TestListStageExecutionsByFlowRun|TestListParticipations|TestStrategyProvenanceReads'` PASS.
- **Stop:** si algún listado exige una columna inexistente (schema gap) → `STOP — MANAGER REVIEW — FROZEN_CONTRACT_COLLISION` (migration NONE es frozen).

### F05I-T3 — Funnel projection

- **Objective:** proyección pura `sqx-forge-funnel-projection.v1` desde vistas de stage executions + participaciones.
- **Allowed files:** `sqx/core/forge/funnel.go` (+ `_test.go`).
- **Inputs:** SPEC §Funnel projection; tipos view de T2.
- **Requirement:** función pura `ProjectFunnel(stages []StageExecutionListItem, participations []ParticipationItem) FunnelProjection`; boundaries por `stage_key` observado; orden `(min(created_at), stage_key)`; `by_status` completo; `strategy_subjects_seen/completed` (subject_kind STRATEGY, dedupe por ref); `error_codes` dedup ordenados; sin reloj, sin IO.
- **Tests:** stages repetidos agregan; stage ausente no aparece (no zero-fill); FAILED con error_code visible; orden determinístico estable; input vacío → boundaries vacíos (válido).
- **Negative assertions:** no inventa refs; no hardcodea nombres de stage; no marca "supervivencia" entre boundaries.
- **Done:** `go test ./sqx/core/forge/... -run TestProjectFunnel` PASS.
- **Stop:** si requiere conocer topología estática → mal análisis → replantear sin hardcode (no STOP de manager; corregir en scope).

### F05I-T4 — Read services de inspección

- **Objective:** composición por refs exactos: strategy inspect, run stage timeline (+funnel), campaign list service; clasificación de errores según taxonomía existente.
- **Allowed files:** `sqx/core/forge/inspect.go` (+ `_test.go`).
- **Inputs:** ports T2; `forge.Service` existente (no editar `result.go`); `LoadMagicAllocation`, `LoadStrategyIdentity`/`StrategyManifestIdentityReader`, `ListStrategyVersions`, `ListHandoffByStrategy` (T2).
- **Requirement:** `InspectService` con: `Strategy(ctx, strategyRef)` → documento `sqx-strategy-inspect.v1` (shape exacto SPEC: identity desde fila durable — nunca parse de CanonicalStrategyID —, participation, magic|null, versions, handoff+delivery); `RunStages(ctx, flowRunRef)` → `sqx-run-stage-timeline.v1` + funnel embebido; `Campaigns(ctx, limit, cursor)` → `sqx-campaign-list.v1`. Reuso de `classified(...)`/ErrorKind existente. Ausencia requerida → `ErrNotFound`; opcional → `null`. Deadline default como `Service.Result`.
- **Tests:** unit con fakes de ports: happy, not-found, magic null (pre-F-04), decoy canonical no altera instrument/direction/timeframe, orden determinístico documentos, provenance exacta (refs devueltos = refs persistidos, sin transformación).
- **Negative assertions:** "latest"/ref malformado → INVALID_ARGUMENT; sin Ref por filename/timestamp; incompleto contraditorio → CONTRACT_INCONSISTENCY y no JSON parcial inventado.
- **Done:** `go test ./sqx/core/forge/...` PASS (nuevo subset).
- **Stop:** si el shape exige mutar `ForgeResult`/`ForgeCampaignResult` → `STOP — MANAGER REVIEW — FROZEN_CONTRACT_COLLISION`.

### F05I-T5 — CLI sqx-flowkit inspect — contrato corregido Planning C1 2026-09-16

- **Objective:** subcomandos `campaign get|list`, `run get|stages`, `strategy get`, `release-matrix`; JSON determinístico; exit codes; wiring sin `internal/di`; dispatch primero, boot mínimo por subcomando (SPEC §C1.6).
- **Allowed files:** `sqx/cmd/sqx-flowkit/main.go` (sólo dispatch + boot por subcomando: extraer push-output a archivo propio preservando flags/salida/códigos), `sqx/cmd/sqx-flowkit/push_output.go`, `sqx/cmd/sqx-flowkit/inspect.go` (+ `_test.go`, tests de emisión/exit codes con services fake), `sqx/cmd/sqx-flowkit/testdata/` (fixtures sintéticas pequeñas).
- **Inputs:** T1 (API `releasematrix.LoadEmbedded/Parse/Load`), T3/T4 (funnel + `InspectService` con deps nil fail-closed), SPEC §C1.6 grafo mínimo de inicialización; patrón wiring `sqx/cmd/sqx-worker/persistence.go`.
- **Requirement:** `main()` despacha `os.Args[1]` ANTES de bootear; el `Init()` completo pre-dispatch se elimina. Grafo por subcomando (frozen, ver SPEC): `release-matrix` cero DI (embebido + override `--matrix`; override inválido → exit 2; NUNCA path default relativo al repo ni acceso a `deploy/`); `campaign get|list`/`run stages`/`strategy get` boot PG (`WithEtcd+WithTelemetry(telemetry.Postgres)+WithPostgres` → `NewControlPlaneFromClient(di.Container.Postgres)`, sin Mongo); `run get` boot PG + `sharedmongo.New` → `forge.NewService(control, rankingStore, control)`; `push-output` conserva su boot interno actual. Salida stdout JSON con `schema`, sin timestamps de query; stderr `<code>:<kind>:<mensaje>`; exit codes `0/2/4/10/50` con mapping frozen (INVALID_ARGUMENT→2, NOT_FOUND→4, CONTRACT_INCONSISTENCY/INFRASTRUCTURE/AMBIGUOUS→50, boot DI→10). `run get` cablea `forge.Service` (primer caller productivo); `--ranking` opcional; help por subcomando; unknown subcommand → exit 2 con usage completo.
- **Tests:** unit dispatch (push-output intacto: mismos flags/salida/exit codes vía FlagSet reflection + golden stdout); JSON emitters (golden bytes deterministas); exit code mapping por ErrorKind con fakes; **portabilidad release-matrix**: handler corre con CWD en temp dir vacío sin repo ⇒ bytes idénticos al embebido, y override `--matrix` válido/inválido (missing/corrupt/invalid → 2); **BWC**: `--help`/args/exit codes de push-output no cambian; grafo mínimo: el path de `release-matrix` no invoca `di.InitSelective` (estructura de código + T7 re-verifica).
- **Negative assertions:** `campaign get latest`/ref malformado → exit 2; ausente → exit 4 con mensaje claro; cero writes (sólo readers en el grafo); ningún subcomando de inspección inicializa Mongo/Temporal/MinIO salvo `run get` (Mongo) — y ninguno MinIO/Temporal.
- **Done:** `go test ./sqx/cmd/sqx-flowkit/...` PASS; `go build ./sqx/...` OK.
- **Stop:** si wiring exige modificar `internal/di` o agregar server HTTP, o si un subcomando de inspección necesita un servicio fuera del grafo mínimo → `STOP — MANAGER REVIEW` (arquitectura frozen).

### F05I-T6 — Handoff documental F-05-C

- **Objective:** contrato read-surface + checklist conformance + template manifest certificación.
- **Allowed files:** `docs/echo-forge/f05-read-surface.md`, `docs/echo-forge/f05-conformance-checklist.md`, `docs/echo-forge/f05-certification-manifest-template.json`.
- **Inputs:** SPEC completa; [[Echo + Echo Forge — Deferred Certification Backlog]] CERT-F05-01…03.
- **Requirement:** read-surface doc = esquemas JSON finales, comandos, tabla error/empty, reglas provenance (para el front futuro: consumir CLI/services, nunca DB directa). Checklist = por superficie: qué verificar, con qué refs/evidencia, qué NO valida F-05-I. Template = campos físicos `null` + `"status": "OPEN"`, sin datos inventados.
- **Tests:** validación JSON del template (parse + campos requeridos) dentro de T1 o T4 tests si aplica; consistencia cross-ref con comandos reales de T5.
- **Negative assertions:** ningún campo físico pre-llenado; ninguna promesa PRODUCT CAPABILITY.
- **Done:** docs committed y consistentes con lo implementado.
- **Stop:** n/a (documental). Si descubre gap real de certificación nueva → registrar en [[Echo + Echo Forge — Deferred Certification Backlog]] y avisar en bitácora (no improvisar gates).

### F05I-T7 — Verificación completa + evidencia

- **Objective:** pasar la matriz congelada y capturar evidencia para manager review.
- **Allowed files:** ninguno nuevo (sólo corrección de los anteriores si falla algo).
- **Commands (freeze, desde repo root):**
```text
go build ./sqx/... ./deployer/...
go test ./sqx/core/releasematrix/... ./sqx/core/forge/... ./sqx/core/capabilities/...
go test ./sqx/adapters/registry-postgres/... -run 'TestListForgeCampaigns|TestListStageExecutionsByFlowRun|TestListParticipations|TestStrategyProvenanceReads|TestForgeCampaignResult|TestFlowRunResult'
go test ./sqx/cmd/sqx-flowkit/...
go test -race ./sqx/core/forge/... ./sqx/core/releasematrix/... ./sqx/cmd/sqx-flowkit/...
go vet ./sqx/core/... ./sqx/adapters/registry-postgres/... ./sqx/cmd/sqx-flowkit/...
git diff --check
```
- **Notas:** suite full de registry-postgres tiene timeout conocido de embedded-postgres (preexistente); el subset focused es el gate. `-race` aplica a áreas concurrentes afectadas (read paths paralelos); si no hay concurrencia nueva, `-race` igual corre verde.
- **DEFERRED CERTIFICATION (NO son gates de F-05-I):** T2.11/T2.12/T2.13, E-04 T21/AC-37, físico Windows/MT5, FULL golden, publish/release.
- **Done:** todos verdes + reporte en bitácora (comandos, resultados, SHA branch). Veredicto: `F-05-I IMPLEMENTED / SOURCE VERIFIED` (no CLOSED, no PHYSICAL PASS, no PRODUCT CAPABILITY PASS).
- **Stop:** rojo estructural que exceda allowed files → `STOP — MANAGER REVIEW` con diagnóstico.

## ✅ Completion criteria (F-05-I)

Matriz release + provenance reproducibles (deterministas); read surfaces inspectables vía CLI; tests/source checks del scope PASS; cero cambios a F-01…F-04/S0 frozen; cero publicación desde la branch; ningún gate físico marcado PASS; handoff F-05-C presente.

## 🛑 Stop conditions (globales)

`STOP — MANAGER REVIEW — FROZEN_CONTRACT_COLLISION`: cualquier necesidad de modificar semántica/schema frozen o migration ≠ NONE. `STOP — MANAGER REVIEW — BASELINE_MOVED`: `b57bfb2` inexistente o `origin/feature/f04-magic-version-handoff` movida materialmente. Cualquier presión de publicar release o marcar gates físicos desde esta branch se rechaza y escala a manager.

## 📆 Bitácora

- **2026-09-16 — Corrección F05I-T2 publicada (sesión NORMAL): keyset pagination en empates de `created_at`.** Defecto confirmado por manager: `forge_campaign_list.go` ordenaba `created_at DESC, id ASC` pero filtraba con `(created_at, id) < ($1,$2)` (comparación `id` descendente), excluyendo en cada página las campañas empatadas en `created_at` con `id > cursor.id` — pérdida silenciosa de registros al paginar. Corrección mínima al predicado contractual `created_at < $1 OR (created_at = $1 AND id > $2)`; sin cambios de orden, cursor, firma, validaciones, taxonomía, proyección ni esquema (migration NONE intacto). Commit `3da8b470239a15f62d87f16559feada409e2d611` (solo los 2 archivos autorizados), push normal a `origin/codex/f05-release-prep`, HEAD remoto verificado `3da8b47`, ancestro de `d77342d` verificado, dirty preexistente `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` preservado. Test de regresión nuevo `TestListForgeCampaignsPersistenceTieTimestampsKeysetTraversal` (embedded-postgres aislado + fixture sintética con constraints reales: 3 campañas empatadas en `created_at`, una anterior y una posterior; recorrido completo con `limit=1`): verifica orden contractual exacto, cero pérdidas, cero duplicados y página final vacía; comprobado que FALLA contra el predicado anterior (página vacía donde debía haber fila del empate) y PASS con la corrección. sqlmock de cursor actualizado al SQL nuevo. Validación: gofmt OK · `go test -run 'TestListForgeCampaigns'` PASS · build consumers OK · `-race` PASS · `go vet` PASS · `git diff --check` OK. NOT_RUN: suite completa registry-postgres (timeout preexistente conocido; el gate es el subset enfocado) y suite global (fuera de scope por prompt). T2 permanece en Review; T3/T4 sin cambios de estado; F-05-I/F-05-C no cerradas; ningún gate físico marcado. Siguiente paso: revisión manager del commit `3da8b47` antes de Planning C1.

- **2026-09-16 — T2–T4 publicadas en GitHub y movidas a Review; corrección de trazabilidad L0 (sesión NORMAL, sin tocar source).** Branch `codex/f05-release-prep` publicada en `origin` (push normal, sin force, sin tags, sin PRs): HEAD remoto verificado `d77342d5a49cb393f92e1a85f998c5614a1cd6bb` == HEAD local; baseline `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` ancestro (GitHub compare: 3 commits ahead, 0 behind, 13 archivos); `git diff --check` baseline..HEAD limpio; commits accesibles por SHA. Dirty preexistente `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` preservado sin commitear. Tareas T2/T3/T4 movidas de Done a Review (tablero `[r]`): IMPLEMENTATION REPORTED + SOURCE VERIFIED BY AGENT; MANAGER REVIEW PENDING; PHYSICAL CERTIFICATION NOT RUN. Corrección Agents OS: el L0 `2026-09-16-f05i-t2-t4-implementation-raw.md` era una reconstrucción sin transcript (prohibido por contrato session-close) → hechos operativos únicos fusionados en el L1 existente y L0 eliminado; detalle en `80-agents/journal/logs/2026-09-16-f05i-publication-review-corrections.md`. F-05-I NO cerrada; ningún gate físico marcado PASS. Siguiente paso: revisión manager del diff en GitHub.
- **2026-09-16 — F05I-T2 + T3 + T4 IMPLEMENTED / SOURCE VERIFIED (sesión NORMAL).** Baseline verificado `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` == `origin/feature/f04-magic-version-handoff` tras `git fetch` (sin BASELINE_MOVED); branch `codex/f05-release-prep` creada desde el SHA exacto (HEAD local previo `9fad768`, detrás del baseline; dirty preexistente `specs/.../phase4_performance.json` preservado sin commitear). Commits: `7d073b3` (T2: ports `capabilities/forge_inspect_query.go` + 4 adapters PG read-only con orden/paginación frozen), `65c879a` (T3: `core/forge/funnel.go` proyección pura `sqx-forge-funnel-projection.v1`), `d77342d` (T4: `core/forge/inspect.go` InspectService con `sqx-strategy-inspect.v1` / `sqx-run-stage-timeline.v1` / `sqx-campaign-list.v1`). Diff: 13 archivos nuevos autorizados, 2526 inserciones, 0 modificaciones a archivos existentes; sin migraciones, sin `internal/di`/`deploy`/`deployer`/`cmd`, contratos frozen intactos. Tests: gate enfocado `go test ./sqx/adapters/registry-postgres/ -run 'TestListForgeCampaigns|TestListStageExecutionsByFlowRun|TestListParticipations|TestStrategyProvenanceReads'` PASS (sqlmock + persistencia embedded-postgres aislado, fixtures sintéticas etiquetadas); `go test ./sqx/core/forge/... ./sqx/core/capabilities/...` PASS; `-race` PASS en los tres paquetes; `go vet` PASS; `gofmt` OK; `git diff --check` OK. NOT_RUN: `go build ./sqx/...` completo falló sólo en `sqx/tools` (mains duplicados preexistentes al baseline, fuera de scope); suite completa de registry-postgres no corrida (timeout conocido preexistente, el gate es el subset enfocado); certification física/CLI (T5+) no aplica a esta sesión. Dependencia técnica registrada: `InspectService` define port local `MagicAllocationReader` (consumidor) satisfecho estructuralmente por `ControlPlane.LoadMagicAllocation`; namespace magic se recibe por wiring (`MagicRegistryNamespaceLive`). Sin certificación física: ningún gate T2.11/T2.12/T2.13 ni golden marcado. Siguiente paso: revisión manager del handoff; luego T1/T5/T6/T7 según asignación.
- **2026-09-13 — TOP planificación completa.** Recon source read-only @ `b57bfb2`: read models existentes sin callers (`forge.Service`, `LoadForgeCampaignResult`), cero HTTP/API, tools informales; authorities mapeadas (PG 19 tablas sqx, Mongo 9 colecciones, MinIO, Temporal cols, etcd). SPEC frozen [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]: CLI JSON + release matrix declarativa + funnel proyección pura; `DATABASE MIGRATION: NONE`. Tareas F05I-T1…T7, allowed files y matriz de tests congelados. NORMAL pendiente autorización manager.

## 🧭 Decisiones

- Arquitectura read surface = CLI JSON determinístico sobre ports/services (sin HTTP; front futuro envuelve los mismos services).
- Release matrix vive en repo (`deploy/release-matrix.json`) + validador puro; no es autoridad de release.
- Funnel derivado de stage_executions (topología dinámica), nunca hardcoded.
- `PARTIAL` no se inventa: estados existentes por nivel representan parcialidad.
- Exit code `4` = NOT_FOUND (aditivo).

## 🔗 Docs / Links

- [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]] (SPEC)
- [[Echo Forge — Factory V2 Completion]] (parent/roadmap)
- [[Echo + Echo Forge — Deferred Certification Backlog]] (F-05-C)
- [[echo-forge]] · [[echo-forge-integration-boundary]]

## 💡 Ideas

### Backlog de ideas

- Front métricas/cohorts y SQX viewer `-gui` post-F-05 (no son F-05-I).

### Motivos / principios

- Membership ≠ rank; projection ≠ authority; zero finalists = resultado válido; ausencia ≠ cero.

### Memoria pública / interna

- **Memoria pública:** SPEC/contract docs.
- **Memoria interna:** ninguna nueva (sin delta operativo más allá del proyecto).
- **Motivo:** el estado y la historia viven en el proyecto y las SPECs.
