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
start: 2026-09-08
due:
progress: 0
repo: xKoRx/symphony
jira:
prs:
aliases:
  - F-03 SQX long-running
  - Echo Forge F-03 implementation
  - SQX elapsed not failure
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-08"
updated: "2026-09-08"
---

# Echo Forge — F-03 SQX long-running

%% Naming: Echo Forge — F-03 SQX long-running es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — F-03 SQX long-running
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo Forge — Factory V2 Completion]] · **Repo:** `xKoRx/symphony`
> Subproyecto de implementación de la fase F-03. Contrato: [[Echo Forge — F-03 SQX Long-Running Contract]].

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo Forge — Factory V2 Completion]] enlaza esta fase. El humano sigue el track desde [[Echo — Producto Integrado]].

## 🎯 Objetivo

Elapsed wall-clock ≠ failure de negocio en cómputos SQX largos (Builder / Optimizer / WFM y superficies equivalentes). Quitar deadlines de negocio; conservar liveness, heartbeat, recovery/retry, cancel cooperativo árbol-scoped y serialización por máquina/databank. No copiar MT5 Slot Pool/allocator/takeover/fencing.

## 📊 Estado actual

- **PHYSICAL CERT ATTEMPT 2026-09-10 → `BLOCKED` (licencia SQX expirada).** Lab aprovisionado y tibio en Hera: binarios `sqx-worker`+`sqx-watcher` construidos desde tree limpio `382f4ba` (sha256 worker `410040b1…`, watcher `04cdac76…`), scopes ETCD aislados `/sqx-{worker,watcher}/f03cert/` con cola dedicada `f03-cert-queue` (ns `sqx-prop`), worker corriendo como proceso ad-hoc `/tmp/f03-cert/` (sin tocar flota `0.2.96` ni manifests). Job real despachado (`sqx-main-v1-d917aa11…`); `sqcli` murió en el license check (`Trial license expired`, exit 1) en Hera y Zeus; claves históricas 869A77/5F89F5/71CE83 rechazadas. Cancel por CLI verificado (`CANCELED`, sin reanudación). P1/P2/P3 no ejecutables → veredicto `BLOCKED / CLOSED`. Requiere: owner restaura licencia SQX → relanzar con `request_id` nuevo. Ver [[2026-09-10-symphony-sqx-trial-license-fleet-expired]].
- **IMPLEMENTACIÓN T1.1–T1.8 EXECUTED 2026-09-09.** Branch `feature/f03-sqx-long-running` commit `a382470` pusheado desde baseline `e50cb7e`. Tests/race/vet verdes; SOURCE LIVE-scoped sin business deadlines; PHYSICAL BLOCKED (sin lab SQX). Pendiente: manager review G1.
- **TOP CORRECTION 2026-09-08 (C1–C3).** Ceiling fijado `MaxInt64ns−1s`. Adaptive `INACTIVE/DEPRECATED — NO CHANGE`. Process-tree obligatorio. NORMAL **no autorizado**. `GOD REQUIRED: NONE`.
- Baseline symphony `e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48` == `origin/master`, worktree CLEAN al abrir y al cerrar TOP.
- `DATABASE MIGRATION: NONE`.
- Agents OS vault sin `.git` (degraded); última SHA durable de journal `f1070bec27db3ca415fe24f3c3576139674b7e09`.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `feature/f03-sqx-long-running` (`a382470`, pushed; HEAD local `382f4ba` bajo certificación) | `e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48` | [[Echo Forge — Factory V2 Completion]] F-03 | [[Echo Forge — F-03 SQX Long-Running Contract]] | T1.1–T1.8 executed; G1 review pendiente; PHYSICAL `BLOCKED` por licencia SQX (lab aprovisionado) |

## Parent / SPEC / baselines

- Parent: [[Echo Forge — Factory V2 Completion]]
- SPEC: [[Echo Forge — F-03 SQX Long-Running Contract]] — `VAULT_ROOT/30-resources/applications/Echo Forge — F-03 SQX Long-Running Contract.md`
- Frozen: principio B1B [[2026-09-06-echo-forge-mt5-execution-model-v2]] (elapsed ≠ failure) **sin** copiar slots. F-01/F-02 CLOSED no se reabren.

## Source map

Temporal compute LIVE: `sqx/workflows/generic_workflow.go` (`genericActivityOptions`, ActivityOptions en `runGenericSQXWorkflow` y `GroupSQXWorkflow`, child `WorkflowRunTimeout` 30d). Adaptive: `INACTIVE/DEPRECATED — NO CHANGE` (`adaptive_workflow.go` DEPRECATED; `sqx-worker` no lo registra). Campaign control: `forgeCampaignActivityOptions` 30s (KEEP). Worker: `sqx/cmd/sqx-worker/main.go` `cmdexecutor.New` sin timeout; RegisterWorkflow Generic/Group/MT5/Campaign. CLI: `sqx/adapters/executor-sqx/sqx_executor.go`, `cmd-executor` `Execute`/`classifyError`/`process_nonwindows.go`. WFM 10m: `wfm_durable_export_activity.go`. Apply 10m: `ensureApplyDeadline`. Heartbeat: `sqx/core/instrumentation/heartbeat.go`. Recovery: `project_stage_recovery.go`, `BuilderRecovered`. Legado LIVE: `cmd/symphony sqx-worker-minio` → `internal/workflows/main.go`. `pkg/sqxutils/executor.go` `Timeout reached`.

## Requirement-to-evidence

| Req | State | Evidence |
|---|---|---|
| Elapsed ≠ FAILED Generic/Group | missing | StartToClose 10d + ScheduleToClose 20d |
| Elapsed ≠ FAILED WFM físico | missing | WithTimeout 10m |
| Elapsed ≠ FAILED apply SQX | missing | ensureApplyDeadline 10m |
| Heartbeat liveness 2m | done | HeartbeatTimeout + StartHeartbeat 6s |
| Cancel ≠ timeout retry | missing | classifyError Canceled→ErrorTypeTimeout |
| Cancel mata sólo árbol | partial | WaitForCancellation true; Group child sin REQUEST_CANCEL; terminate sólo PID sqcli |
| Recovery independiente de duration | done | StageExecution sealed skip |
| Duration observable sin gate | partial | histogram en utils legado; project heartbeat string estático |
| Campaign budget ≠ kill | done | 30s activities; stop policy aparte |
| Migration | done | NONE — no hay timeout en SQL |

## Decision register

| ID | status | resolution | source | phase |
|---|---|---|---|---|
| D1 elapsed | TECHNICAL_RESOLUTION | Wall-clock sano no es FAILED | SPEC + B1B principio | 1 |
| D2 ceiling | TECHNICAL_RESOLUTION | `sqxActivityTechnicalCeiling = time.Duration(1<<63-1) - time.Second` (MaxInt64ns−1s). Platform safety Temporal/Go, no SLA. LOCAL, no import MT5. NORMAL no elige el número | [[2026-09-06-echo-forge-temporal-activity-ceiling-clamp]]; SDK exige StartToClose finito si ScheduleToClose=0 | 1 |
| D3 schedule-to-close | TECHNICAL_RESOLUTION | `ScheduleToCloseTimeout=0` (unset): sin presupuesto calendario sobre la suma de attempts; el 20d actual es BUSINESS_DEADLINE de retry | SDK Temporal: 0 = no set; MaximumAttempts=0 | 1 |
| D4 heartbeat | TECHNICAL_RESOLUTION | KEEP 2m / 6s; retry infinito transiente | genericActivityOptions + heartbeat.go | 1 |
| D5 cancel | TECHNICAL_RESOLUTION | Canceled no es Timeout; process-group propio del sqcli del Execute (padre+hijo+nieto); jamás pgid del worker | cmd_executor classifyError L379–380; process_nonwindows sin Setpgid | 1 |
| D6 recovery | TECHNICAL_RESOLUTION | Autoridades existentes; no reattach; sealed skip; RUNNING sin sello reinicia | project_stage_recovery.go | 1 |
| D7 campaign | TECHNICAL_RESOLUTION | 30s KEEP; stop ≠ kill compute | forge_campaign_workflow.go | 1 |
| D8 migration | TECHNICAL_RESOLUTION | NONE | no timeout en 001–014 | 1 |
| D9 serial | TECHNICAL_RESOLUTION | No paralelizar; no MaxConcurrent allocator | sqx-worker Options | 1 |
| D10 adaptive | TECHNICAL_RESOLUTION | `INACTIVE/DEPRECATED — NO CHANGE`. No está en `sqx-worker`. Fuera de Allowed Files | DEPRECATED L22–23; RegisterWorkflow sqx-worker L329–333 | 1 |

## Planned diff

Ver SPEC. NORMAL no toca MT5 workflows productivos, F-01 identity, F-02 promotion, migrations SQL, Campaign stop policy.

## No-touch

F-01 identity/publication. F-02 Finalist V2. F-04 magic/seal/handoff. F-05. S0 Echo. B1A/B1B/B2. Slot Pool/fencing/takeover/allocator. Campaign MaxWaves/stop evaluation. `ranking-snapshot.v1`. Foreign dirty symphony. `mt5_artifact_workflow.go` (no-import). `adaptive_workflow.go` (INACTIVE/DEPRECATED — NO CHANGE).

## Execution sequence

T1.1 Temporal Generic/Group options → T1.2 legado `SQXJobWorkflow` (`sqx-worker-minio`) → T1.3 child WorkflowRunTimeout + ParentClosePolicy → T1.4 WFM 10m → T1.5 apply 10m → T1.6 cmd-executor cancel/process-tree/no WithTimeout compute → T1.7 heartbeat details + duration hot path → T1.8 tests SOURCE/CONTRACT/CANCEL/LIVENESS. Adaptive **no** entra. PHYSICAL en certificación, no en estas tasks de código. T1.4 y T1.5 paralelos a T1.1. No T1.8 sin T1.1+T1.6.

## Dependencies

B1B/B2 CLOSED freeze (principio only). Independiente de F-01/F-02/E-01. No S0.

## ✅ Tareas

> [!note]+ Ownership
> Board `#owner/agent`. Cada ítem es una TASK atómica para NORMAL tras autorización del manager.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] T1.1 genericActivityOptions + duplicados Generic/Group → ceiling MaxInt64ns−1s + ScheduleToClose 0 #owner/agent #type/dev #area/echo
> - [-] T1.2-adaptive AdaptiveSQXWorkflow INACTIVE/DEPRECATED — NO CHANGE #owner/agent #type/dev #area/echo
> - [x] T1.2 legado SQXJobWorkflow/SQXGroupWorkflow 10d/20d (`sqx-worker-minio`) → misma regla T1.1 #owner/agent #type/dev #area/echo
> - [x] T1.3 Group child WorkflowRunTimeout 30d → 0; ParentClosePolicy REQUEST_CANCEL #owner/agent #type/dev #area/echo
> - [x] T1.4 WFMDurableExportActivity WithTimeout 10m → eliminar #owner/agent #type/dev #area/echo
> - [x] T1.5 ensureApplyDeadline 10m → eliminar #owner/agent #type/dev #area/echo
> - [x] T1.6 cmd-executor Canceled≠Timeout + process-tree propio (padre+hijo+nieto); New() sin WithTimeout #owner/agent #type/dev #area/echo
> - [x] T1.7 HeartbeatDetails elapsed en project + duration_ms hot path executor-sqx #owner/agent #type/dev #area/echo
> - [x] T1.8 Tests SOURCE/CONTRACT/CANCEL/LIVENESS + no-regresión F-01/F-02/B1/B2 #owner/agent #type/dev #area/echo

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

Contrato de cada TASK: `archivo/símbolo → cambio exacto → tests/certificación → DONE`. Sin decisiones arquitectónicas en NORMAL.

### T1.1 genericActivityOptions + duplicados Generic/Group

- **Modelo:** NORMAL
- **Objetivo:** retirar 10d/20d de compute Generic/Group.
- **Archivos/símbolos:** `sqx/workflows/generic_workflow.go` `genericActivityOptions`, ActivityOptions en `runGenericSQXWorkflow`, ActivityOptions en `GroupSQXWorkflow`; introducir `sqxActivityTechnicalCeiling` local (no import MT5).
- **Cambio:** `HeartbeatTimeout` 2m KEEP; `StartToCloseTimeout=sqxActivityTechnicalCeiling` donde `sqxActivityTechnicalCeiling = time.Duration(1<<63-1) - time.Second` (constante local; valor fijado en SPEC; NORMAL no lo cambia); `ScheduleToCloseTimeout=0`; `WaitForCancellation` true KEEP; `RetryPolicy` KEEP.
- **Tests/certificación:** `StartToCloseTimeout == sqxActivityTechnicalCeiling` igualdad exacta; `ScheduleToCloseTimeout == 0`; Heartbeat 2m; MaximumAttempts 0; `activity.Info.StartToCloseTimeout > 0 && <= ceiling` (no asertar 87600h). Ningún assert residual de 10d/20d. Gate SOURCE #1 scoped LIVE.
- **DONE:** `go test` paquete `sqx/workflows` verde en tests de options Generic/Group.
- **Deps:** ninguna.
- **Stop:** si Temporal rechaza ceiling → PLAN_CONFLICT, no bajar a 365d ni otro número de negocio.

### T1.2-adaptive INACTIVE — NO CHANGE

- **Modelo:** n/a (fuera de NORMAL)
- **Clasificación:** `INACTIVE/DEPRECATED — NO CHANGE`.
- **Evidencia runtime:** `AdaptiveSQXWorkflow` / `AdaptiveTypeWorkflow` marcados DEPRECATED; `sqx-worker` registra Generic, Group, MT5, Campaign — no Adaptive; solo tests llaman `RegisterWorkflow(AdaptiveSQXWorkflow)`. Docs/FEAT históricas no cuentan.
- **Archivos:** `adaptive_workflow.go` **prohibido** en Allowed Files. No alinear `mainActivityOptions` 5d/10d.
- **SOURCE:** grep de certificación **excluye** este archivo. 5d/10d residuales no fallan F-03.
- **DONE:** no hay diff. Tarea marcada `[-]`.
- **Stop:** incluirlo “por simetría” → viola C2.

### T1.2 legado SQXJobWorkflow (`sqx-worker-minio`)

- **Modelo:** NORMAL
- **Objetivo:** el binario `cmd/symphony sqx-worker-minio` sigue registrando `SQXJobWorkflow`/`SQXGroupWorkflow`; no dejar killer 10d/20d en esa superficie LIVE.
- **Archivos/símbolos:** `internal/workflows/main.go` ActivityOptions de `SQXJobWorkflow`/`SQXGroupWorkflow`. **No** `adaptive_workflow.go`.
- **Cambio:** misma regla T1.1 (ceiling local o reuso de la constante de `sqx/workflows` si el paquete lo permite sin importar MT5; si el módulo internal no puede importar `sqx/workflows`, duplicar el literal `time.Duration(1<<63-1) - time.Second` con el mismo nombre local).
- **Tests/certificación:** assert options legado; SOURCE incluye 10d/20d ausentes en `internal/workflows/main.go`.
- **DONE:** grep 10d/20d StartToClose/ScheduleToClose en `internal/workflows/main.go` = 0.
- **Deps:** T1.1 (valor del ceiling ya fijado en SPEC).
- **Stop:** reescribir el intérprete legado entero → fuera de alcance. Registrar Adaptive → fuera de alcance.

### T1.3 Group child run timeout + cancel policy

- **Modelo:** NORMAL
- **Objetivo:** child group no muere a 30d; cancel cooperativo.
- **Archivos/símbolos:** `generic_workflow.go` `ChildWorkflowOptions` (lote L1338 y fan-in L1535): `WorkflowRunTimeout`, `ParentClosePolicy`, `WaitForCancellation`.
- **Cambio:** `WorkflowRunTimeout` unset/0; `PARENT_CLOSE_POLICY_REQUEST_CANCEL`; `WaitForCancellation=true`. No copiar collector MT5.
- **Tests/certificación:** test child options; cancel parent Generic → child canceled no terminate-as-success. Gate CANCEL #3 (workflow tree).
- **DONE:** 30d ausente; test de policy verde.
- **Deps:** T1.1.
- **Stop:** Terminate “por si acaso” → viola cancel cooperativo.

### T1.4 WFM 10m WithTimeout

- **Modelo:** NORMAL
- **Objetivo:** export WFM físico no muere a 10m.
- **Archivos/símbolos:** `sqx/activities/worker/wfm_durable_export_activity.go` bloque `hasDeadline` / `WithTimeout(10*time.Minute)`; tests heartbeat existentes **no** relajar.
- **Cambio:** eliminar timeout sintético. Heartbeat details KEEP. Physical exporter KEEP.
- **Tests/certificación:** test que Execute no añade deadline si ctx no tiene; analogía heartbeat 2s vs 2m sigue PASS. PHYSICAL #5 usa este límite viejo.
- **DONE:** `go test` `wfm_durable_export_activity_test.go` verde; 10m ausente.
- **Deps:** ninguna (paralelo a T1.1).
- **Stop:** alargar a 24h en vez de quitar → BUSINESS_DEADLINE residual.

### T1.5 ensureApplyDeadline 10m

- **Modelo:** NORMAL
- **Objetivo:** apply selected run (CLI SQX) no muere a 10m.
- **Archivos/símbolos:** `durable_apply_selected_run.go` `ensureApplyDeadline`; callers; tests de apply.
- **Cambio:** no inyectar timeout; usar ctx de activity (heartbeat + cancel). File lock KEEP.
- **Tests/certificación:** test sin DeadlineExceeded a > analogía corta; recovery RUNNING KEEP. Gate SOURCE/CONTRACT.
- **DONE:** 10m ausente en apply; tests apply verdes.
- **Deps:** ninguna (paralelo a T1.1).
- **Stop:** cablear SQCLITimeoutMs → prohibido.

### T1.6 cmd-executor cancel y process-tree

- **Modelo:** NORMAL
- **Objetivo:** cancel/deadline técnico mata el process-group **propio** del `sqcli` de este Execute (padre+hijo+nieto); `context.Canceled` no se reintenta como timeout.
- **Archivos/símbolos:** `cmd_executor.go` `classifyError`; `process_nonwindows.go` `startManagedProcess` (`SysProcAttr.Setpgid=true` en el hijo); terminate con `-pgid`; `sqx/cmd/sqx-worker/main.go` permanece `New` **sin** `WithTimeout`; opcional `sqx/core/domain` `ErrorTypeCanceled` no-transiente; tests `sqcli_executor_*`.
- **Cambio:** `context.Canceled` → cancel (errors.Is / Temporal CanceledError), **nunca** `ErrorTypeTimeout`. Non-Windows: process-group cuyo líder es el `sqcli` de **este** Execute; SIGTERM+SIGKILL acotados a `-pgid`. Jamás Setpgid/kill del worker ni pgid 0. Windows: kill del proceso iniciado por este Execute (sin Job Object MT5). Prohibido `WithTimeout` en wiring de compute. No copiar semántica MT5.
- **Tests/certificación:** cancel ctx → `Canceled` no timeout; proceso padre + hijo + nieto gone; worker PID vivo; segundo Execute sibling vivo; `New()` configuredTimeoutMs==0. Gate CANCEL #3 físico + CONTRACT retry.
- **DONE:** tests cmd-executor verdes; worker main sin WithTimeout; demostración parent+child+grandchild.
- **Deps:** ninguna (paralelo). T1.8 consume este comportamiento.
- **Stop:** Importar slot/Job Object MT5, o matar el process-group del worker → PLAN_CONFLICT.

### T1.7 Observabilidad duration sin gate

- **Modelo:** NORMAL
- **Objetivo:** medir elapsed; no fallar por él.
- **Archivos/símbolos:** `project_activity.go` `StartHeartbeat` → `StartHeartbeatWithDetails` (ElapsedMs); `executor-sqx.go` ya loguea `duration_ms` — asegurar histogram `symphony.sqx.sqcli.duration_ms` en hot path (o reusar RecordHistogram del ctx).
- **Cambio:** details de heartbeat; métrica de duration. Cero branches `if duration > X { fail }`.
- **Tests/certificación:** heartbeat test project no usa elapsed para error; Gate #6 duration observable.
- **DONE:** test project heartbeat details; métrica emitida en ExecuteAndWait productivo.
- **Deps:** T1.1 no estricta.
- **Stop:** métrica con RequestID en el nombre.

### T1.8 Tests de certificación SOURCE/CONTRACT/CANCEL/LIVENESS

- **Modelo:** NORMAL
- **Objetivo:** gates 1–4 y 7 en CI; procedimiento PHYSICAL escrito (no ejecutado aquí).
- **Archivos/símbolos:** tests nuevos en `sqx/workflows`, `cmd-executor`, WFM/apply; no tocar `adaptive_workflow.go` ni sus tests salvo que un grep SOURCE mal scoped los rompa — entonces **estrechar el grep**, no “arreglar” Adaptive. No tocar tests F-02/F-01/MT5 slot salvo pin 10d de compute SQX.
- **Cambio:** cobertura de options (ceiling exacto + ScheduleToClose 0), cancel≠timeout, process-tree parent+child+grandchild, heartbeat retry, recovery unchanged by duration. `go test -race` paquetes tocados. Grep SOURCE **LIVE-scoped**.
- **Tests/certificación:** lista de gates SPEC 1–4 y 7 PASS. PHYSICAL 5 queda procedimiento en SPEC para cert posterior. Anti-test-masking: no `t.Skip` del killer.
- **DONE:** CI verde; grep BUSINESS_DEADLINE literales = 0 en hot path LIVE; Adaptive 5d/10d pueden permanecer; F-01/F-02/B1/B2 tests existentes verdes.
- **Deps:** T1.1–T1.7 (T1.2-adaptive no es dep).
- **Stop:** fingir PHYSICAL con mock de 10m; fallar SOURCE por Adaptive.

## Gates

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G1 | planned | T1.1–T1.8 según SPEC; diff acotado + tests + grep SOURCE | Manager review; no auto-merge | F-03 implementation review; no F-04 |
| PHYSICAL | deferred | procedimiento SPEC §Certification #5 | Lab SQX job >10m COMPLETED + cancel árbol | F-05 cómputos largos |

## Tests / certification

Suite por task. Final: options ceiling exacto + ScheduleToClose 0; WFM/apply sin 10m; cancel≠timeout; process-tree parent+child+grandchild; heartbeat analog; recovery tests existentes. Cert: SOURCE LIVE-scoped + CONTRACT ahora; PHYSICAL en lab post-merge. No flota MT5. Adaptive fuera.

## Risks

- `classifyError` Canceled→Timeout reanuda jobs cancelados con retry infinito.
- Process-group mal aplicado (pgid del worker / `kill(0)`) mata sibling y el worker.
- Tests que no demuestran nieto Java/grandchild dejan huérfanos.
- SOURCE que incluye `adaptive_workflow.go` exige un diff de arquitectura muerta.
- Dejar 10d en `internal/workflows` mientras `sqx-worker` está limpio = killer dual del comando `sqx-worker-minio`.
- PHYSICAL de 10d; el procedimiento usa 10m WFM/apply.

## Definition of Done

SPEC cumplida. Sin business deadline en Builder/Optimizer/WFM/apply. Heartbeat/recovery intactos. Cancel árbol-scoped. Migration NONE. Duration observable. Sin NORMAL antes de autorización. PHYSICAL según procedimiento, no en TOP.

## Unlocks

F-05 puede incluir cómputos largos en golden. F-01/F-02 no bloquean ni quedan bloqueados.

### Paquete autónomo Fase 1 — SQX Long-Running Contract

**Misión exacta**

Implementar T1.1–T1.8 contra [[Echo Forge — F-03 SQX Long-Running Contract]] en baseline `e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48`, sin copiar MT5 slots ni reabrir F-01/F-02/B1/B2.

**Precondiciones verificables**

Manager aceptó esta nota + SPEC. Symphony `origin/master` revalidado = baseline o STOP. Worktree CLEAN salvo el diff F-03. NORMAL autorizado explícitamente. Hoy: **no autorizado**.

**Lectura obligatoria**

`VAULT_ROOT/30-resources/applications/Echo Forge — F-03 SQX Long-Running Contract.md`

`VAULT_ROOT/10-projects/Echo/agentes/Echo Forge — F-03 SQX long-running.md`

`VAULT_ROOT/80-agents/memory/public/decision/symphony/2026-09-06-echo-forge-mt5-execution-model-v2.md`

Source map de esta nota. No redescubrir Slot Pool para SQX.

**Decisiones cerradas**

Ver SPEC y decision register. Ceiling = `time.Duration(1<<63-1) - time.Second` (NORMAL no lo cambia). ScheduleToClose 0. Heartbeat KEEP. Cancel ≠ timeout. Process-tree propio del sqcli. Adaptive NO CHANGE. Recovery existente. Migration NONE.

**Implementación paso a paso**

Ejecutar T1.1 → T1.2 (legado only) → T1.3; T1.4/T1.5/T1.6/T1.7 paralelos a T1.1 cuando no compartan el mismo hunk; T1.8 al final. **No** T1.2-adaptive. Actualizar esta nota al avanzar. No despachar F-04.

**Archivos esperados**

modify: Planned diff SPEC. no-touch: lista No-touch.

**No tocar**

F-01, F-02, F-04, F-05, S0, B1/B2, Slot Pool, Campaign stop policy, foreign dirty, migrations SQL, `adaptive_workflow.go`.

**Spikes permitidos**

Ninguno de arquitectura. Si el ceiling Temporal (`MaxInt64ns−1s`) no es aceptado por el SDK: PLAN_CONFLICT y parar. No inventar otro número.

**Tests y asserts**

Los de T1.1–T1.8. Anti-test-masking. PHYSICAL no se finge.

**Entregables/Gate**

G1 review. `DATABASE MIGRATION: NONE`. `NO NORMAL IMPLEMENTATION AUTHORIZED YET` hasta orden del manager.

**Handoff**

Ver comentario de cierre TOP. Próximo: autorización NORMAL.

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — SQX Long-Running Contract
GATE_REQUERIDO=none
TAREAS=T1.1,T1.2-legado,T1.3-T1.8 (T1.2-adaptive NO CHANGE)
SALIDA=source diff F-03 + grep SOURCE + tests cancel/liveness + nota en review
STOP=NO NORMAL IMPLEMENTATION AUTHORIZED YET
```

El bloque de despacho no sustituye la SPEC ni autoriza ejecución.

## 📆 Bitácora

- **2026-09-10** — PHYSICAL CERT attempt sobre HEAD `382f4ba` (tree CLEAN, 2 ahead/0 behind de master): `BLOCKED` por licencia SQX trial expirada en Hera y Zeus (`C0CCF0856B2C`; 869A77/5F89F5/71CE83 rechazadas; última aplicación vigente z0 2026-08-24). Lab aprovisionado sin tocar flota ni manifests: binarios linux/amd64 del commit (worker `410040b1…` / watcher `04cdac76…`) en Hera `/tmp/f03-cert/`, scopes ETCD `/sqx-{worker,watcher}/f03cert/` espejo de producción salvo cola `f03-cert-queue` y `version=f03-cert-382f4ba`; worker+watcher candidatos vivos (worker registrado en `f03-cert-queue`, ns `sqx-prop`, WorkerID `1155192@sqx-ulab-hera-0@`). Job real: watcher V1 despachó `sqx-main-v1-d917aa11-ad27-49a5-bebd-cfd142c2e6ad` (builder XAUUSD H1); el CommandExecutor del worker candidato lanzó `sqcli -project action=start name=custom` → exit 1 en 3.2 s en el license check; retry transiente infinito (diseño F-03) detenido con `temporal workflow cancel` → `CANCELED`, run único, sin reanudación (semántica cancel≠timeout observada a nivel workflow). Efecto de laboratorio a nota: el arranque del worker aplicó la migración pre-existente `014_finalist_promotion_v2` (F-02, ya en master) sobre la DB de test `trading_systems_test`. Veredicto `BLOCKED / CLOSED`: P1 requiere sqcli compute >10m real — imposible sin licencia; no mocks. Reintento: owner restaura licencia → reusar lab tibio, `request_id` nuevo. Detalles: [[2026-09-10-symphony-sqx-trial-license-fleet-expired]] · run: [[2026-09-10-zcode-glm-5.3-flash-f03-physical-cert]].

- **2026-09-09** — T1.1–T1.8 ejecutados en `feature/f03-sqx-long-running` (`a382470`, pushed). Ceiling local en `sqx/workflows` + duplicado legado; duplicados Generic/Group consolidados en `genericActivityOptions()`; child Group con helper `groupChildWorkflowOptions` (REQUEST_CANCEL + sin run timeout); WFM/apply sin 10m; `classifyError` Canceled→`ErrorTypeCanceled` no-transiente (nuevo en domain); process-group Setpgid + SIGTERM/SIGKILL `-pgid` en `process_nonwindows.go` (Windows intacto); project heartbeat details; histograma `duration_ms` en executor-sqx. Tests: options ceiling exacto, SOURCE certification LIVE-scoped (Adaptive excluido), cancel≠timeout, process-tree parent+child+grandchild + sibling vivo, heartbeat details. `go test`/`-race`/`vet` verdes en paquetes tocados; fallos pre-existentes de entorno idénticos a baseline (verificados por diff de sets). PHYSICAL BLOCKED: sin lab SQX (Hera/Zeus) en este host → `READY FOR MANAGER REVIEW — PHYSICAL BLOCKED`. Delegación a subagentes no disponible (límite Token Plan): ejecutado por agente primario, sin desviaciones del contrato frozen salvo actualización del test que pineaba heartbeat string estático (contrato T1.7 lo reemplaza).
- **2026-09-08** — TOP diseñó F-03 contra symphony `e50cb7e`. SPEC + TASKS persistidas. `DATABASE MIGRATION: NONE`. NORMAL no autorizado.
- **2026-09-08** — TOP CORRECTION C1–C3: ceiling = `MaxInt64ns−1s` (platform safety, no SLA); Adaptive `INACTIVE/DEPRECATED — NO CHANGE`; process-tree parent+child+grandchild + `Canceled`≠Timeout. TASKS: T1.2-adaptive `[-]`; T1.2 legado only; T1.6 process-tree. `NO NORMAL IMPLEMENTATION AUTHORIZED YET`.

## 🧭 Decisiones

- Ver [[Echo Forge — F-03 SQX Long-Running Contract]]. Esta nota no duplica la matriz de kill paths.

## 🔗 Docs / Links

- [[Echo Forge — Factory V2 Completion]]
- [[Echo Forge — F-03 SQX Long-Running Contract]]
- [[Echo — Producto Integrado]]
- [[2026-09-06-echo-forge-mt5-execution-model-v2]]

## 💡 Ideas

### Backlog de ideas

- Ninguna dentro de F-03.

### Motivos / principios

- Elapsed sano ≠ FAILED. Heartbeat = liveness. Cancel cooperativo árbol-scoped. No copiar MT5 slots.

