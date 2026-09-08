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

- **TOP persistió SPEC + TASKS (2026-09-08).** NORMAL **no autorizado**. `GOD REQUIRED: NONE`.
- Baseline symphony `e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48` == `origin/master`, worktree CLEAN al abrir y al cerrar TOP.
- `DATABASE MIGRATION: NONE`.
- Agents OS vault sin `.git` (degraded); última SHA durable de journal `f1070bec27db3ca415fe24f3c3576139674b7e09`.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | _no abierta_ | `e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48` | [[Echo Forge — Factory V2 Completion]] F-03 | [[Echo Forge — F-03 SQX Long-Running Contract]] | TOP done; NORMAL no autorizado |

## Parent / SPEC / baselines

- Parent: [[Echo Forge — Factory V2 Completion]]
- SPEC: [[Echo Forge — F-03 SQX Long-Running Contract]] — `VAULT_ROOT/30-resources/applications/Echo Forge — F-03 SQX Long-Running Contract.md`
- Frozen: principio B1B [[2026-09-06-echo-forge-mt5-execution-model-v2]] (elapsed ≠ failure) **sin** copiar slots. F-01/F-02 CLOSED no se reabren.

## Source map

Temporal compute: `sqx/workflows/generic_workflow.go` (`genericActivityOptions`, ActivityOptions en `runGenericSQXWorkflow` y `GroupSQXWorkflow`, child `WorkflowRunTimeout` 30d). Adaptive: `mainActivityOptions`. Campaign control: `forgeCampaignActivityOptions` 30s (KEEP). Worker: `sqx/cmd/sqx-worker/main.go` `cmdexecutor.New` sin timeout. CLI: `sqx/adapters/executor-sqx/sqx_executor.go`, `cmd-executor` `Execute`/`classifyError`/`process_nonwindows.go`. WFM 10m: `wfm_durable_export_activity.go`. Apply 10m: `ensureApplyDeadline`. Heartbeat: `sqx/core/instrumentation/heartbeat.go`. Recovery: `project_stage_recovery.go`, `BuilderRecovered`. Legado: `internal/workflows/main.go`, `pkg/sqxutils/executor.go` `Timeout reached`.

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
| D2 ceiling | TECHNICAL_RESOLUTION | `sqxActivityTechnicalCeiling` = max Temporal duration; no importar MT5 | `mt5ActivityTechnicalCeiling` como hecho API | 1 |
| D3 schedule-to-close | TECHNICAL_RESOLUTION | 0 en compute SQX | B1B test Zero ScheduleToClose, no slots | 1 |
| D4 heartbeat | TECHNICAL_RESOLUTION | KEEP 2m / 6s; retry infinito transiente | genericActivityOptions + heartbeat.go | 1 |
| D5 cancel | TECHNICAL_RESOLUTION | Canceled no es Timeout; process group del sqcli del job; Group children REQUEST_CANCEL | cmd_executor classifyError; Campaign child policy | 1 |
| D6 recovery | TECHNICAL_RESOLUTION | Autoridades existentes; no reattach; sealed skip; RUNNING sin sello reinicia | project_stage_recovery.go | 1 |
| D7 campaign | TECHNICAL_RESOLUTION | 30s KEEP; stop ≠ kill compute | forge_campaign_workflow.go | 1 |
| D8 migration | TECHNICAL_RESOLUTION | NONE | no timeout en 001–014 | 1 |
| D9 serial | TECHNICAL_RESOLUTION | No paralelizar; no MaxConcurrent allocator | sqx-worker Options | 1 |

## Planned diff

Ver SPEC. NORMAL no toca MT5 workflows productivos, F-01 identity, F-02 promotion, migrations SQL, Campaign stop policy.

## No-touch

F-01 identity/publication. F-02 Finalist V2. F-04 magic/seal/handoff. F-05. S0 Echo. B1A/B1B/B2. Slot Pool/fencing/takeover/allocator. Campaign MaxWaves/stop evaluation. `ranking-snapshot.v1`. Foreign dirty symphony. `mt5_artifact_workflow.go` salvo no-import.

## Execution sequence

T1.1 Temporal Generic/Group options → T1.2 Adaptive + legado internal/workflows → T1.3 child WorkflowRunTimeout + ParentClosePolicy → T1.4 WFM 10m → T1.5 apply 10m → T1.6 cmd-executor cancel/process group/no WithTimeout compute → T1.7 heartbeat details + duration hot path → T1.8 tests SOURCE/CONTRACT/CANCEL/LIVENESS. PHYSICAL en certificación, no en estas tasks de código. T1.4 y T1.5 paralelos a T1.1. No T1.8 sin T1.1+T1.6.

## Dependencies

B1B/B2 CLOSED freeze (principio only). Independiente de F-01/F-02/E-01. No S0.

## ✅ Tareas

> [!note]+ Ownership
> Board `#owner/agent`. Cada ítem es una TASK atómica para NORMAL tras autorización del manager.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [ ] T1.1 genericActivityOptions + duplicados Generic/Group → ceiling + ScheduleToClose 0 #owner/agent #type/dev #area/echo
> - [ ] T1.2 Adaptive mainActivityOptions + internal/workflows 10d/20d → misma regla #owner/agent #type/dev #area/echo
> - [ ] T1.3 Group child WorkflowRunTimeout 30d → 0; ParentClosePolicy REQUEST_CANCEL #owner/agent #type/dev #area/echo
> - [ ] T1.4 WFMDurableExportActivity WithTimeout 10m → eliminar #owner/agent #type/dev #area/echo
> - [ ] T1.5 ensureApplyDeadline 10m → eliminar #owner/agent #type/dev #area/echo
> - [ ] T1.6 cmd-executor Canceled≠Timeout + process group; New() sin WithTimeout #owner/agent #type/dev #area/echo
> - [ ] T1.7 HeartbeatDetails elapsed en project + duration_ms hot path executor-sqx #owner/agent #type/dev #area/echo
> - [ ] T1.8 Tests SOURCE/CONTRACT/CANCEL/LIVENESS + no-regresión F-01/F-02/B1/B2 #owner/agent #type/dev #area/echo

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
- **Cambio:** `HeartbeatTimeout` 2m KEEP; `StartToCloseTimeout=sqxActivityTechnicalCeiling`; `ScheduleToCloseTimeout=0`; `WaitForCancellation` true KEEP; `RetryPolicy` KEEP.
- **Tests/certificación:** test de options: ceiling exacto, ScheduleToClose 0, Heartbeat 2m, retry MaximumAttempts 0. Ningún assert residual de 10d/20d. Gate SOURCE #1.
- **DONE:** `go test` paquete `sqx/workflows` verde en tests de options Generic/Group.
- **Deps:** ninguna.
- **Stop:** si Temporal rechaza ceiling → PLAN_CONFLICT, no bajar a 365d.

### T1.2 Adaptive + legado internal/workflows

- **Modelo:** NORMAL
- **Objetivo:** no dejar killer 5d/10d/20d latente.
- **Archivos/símbolos:** `sqx/workflows/adaptive_workflow.go` `mainActivityOptions`; `internal/workflows/main.go` ActivityOptions de `SQXJobWorkflow`/`SQXGroupWorkflow`.
- **Cambio:** misma regla T1.1. Adaptive TaskQueue KEEP. No registrar Adaptive si no lo estaba.
- **Tests/certificación:** options test Adaptive; legado: assert options si hay test, o test mínimo nuevo. SOURCE incluye estos literales ausentes.
- **DONE:** grep 5d/10d/20d de StartToClose/ScheduleToClose en esos archivos = 0.
- **Deps:** T1.1 (constante ceiling).
- **Stop:** reescribir el intérprete legado entero → fuera de alcance.

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

### T1.6 cmd-executor cancel y process group

- **Modelo:** NORMAL
- **Objetivo:** cancel mata árbol del sqcli de este Execute; no se reintenta como timeout.
- **Archivos/símbolos:** `cmd_executor.go` `classifyError`; `process_nonwindows.go` `startManagedProcess` (Setpgid / process group); `Terminate` al grupo; `sqx/cmd/sqx-worker/main.go` permanece `New` **sin** `WithTimeout`; test `sqcli_executor_*`.
- **Cambio:** `context.Canceled` → error de cancelación, no `ErrorTypeTimeout`. Process group Unix del hijo. Windows: kill del proceso iniciado por este Execute (sin Job Object MT5). Prohibido `WithTimeout` en wiring de compute.
- **Tests/certificación:** cancel ctx → error cancel, no timeout; segundo Execute de otro binary no es killado; `New()` configuredTimeoutMs==0. Gate CANCEL #3 físico + CONTRACT retry.
- **DONE:** tests cmd-executor verdes; worker main sin WithTimeout.
- **Deps:** ninguna (paralelo). T1.8 consume este comportamiento.
- **Stop:** Importar slot/Job Object MT5 → PLAN_CONFLICT.

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
- **Archivos/símbolos:** tests nuevos en `sqx/workflows`, `cmd-executor`, WFM/apply; no tocar tests F-02/F-01/MT5 slot salvo que un pin 10d rompa — entonces actualizar el pin, no el negocio MT5.
- **Cambio:** cobertura de options, cancel≠timeout, heartbeat retry, recovery unchanged by duration. `go test -race` paquetes tocados. Grep SOURCE de literales prohibidos.
- **Tests/certificación:** lista de gates SPEC 1–4 y 7 PASS. PHYSICAL 5 queda procedimiento en SPEC para cert posterior. Anti-test-masking: no `t.Skip` del killer.
- **DONE:** CI verde; grep BUSINESS_DEADLINE literales = 0 en hot path; F-01/F-02/B1/B2 tests existentes verdes.
- **Deps:** T1.1–T1.7.
- **Stop:** fingir PHYSICAL con mock de 10m.

## Gates

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G1 | planned | T1.1–T1.8 según SPEC; diff acotado + tests + grep SOURCE | Manager review; no auto-merge | F-03 implementation review; no F-04 |
| PHYSICAL | deferred | procedimiento SPEC §Certification #5 | Lab SQX job >10m COMPLETED + cancel árbol | F-05 cómputos largos |

## Tests / certification

Suite por task. Final: options ceiling; WFM/apply sin 10m; cancel≠timeout; process group; heartbeat analog; recovery tests existentes. Cert: SOURCE + CONTRACT ahora; PHYSICAL en lab post-merge. No flota MT5.

## Risks

- `classifyError` Canceled→Timeout reanuda jobs cancelados con retry infinito.
- Process group mal aplicado mata sibling en el mismo worker si comparten pgid 0.
- Dejar 10d en `internal/workflows` mientras `sqx-worker` está limpio = killer dual.
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

Ver SPEC y decision register. Ceiling Temporal local. ScheduleToClose 0. Heartbeat KEEP. Cancel ≠ timeout. Recovery existente. Migration NONE.

**Implementación paso a paso**

Ejecutar T1.1 → T1.2 → T1.3; T1.4/T1.5/T1.6/T1.7 paralelos a T1.1 cuando no compartan el mismo hunk; T1.8 al final. Actualizar esta nota al avanzar. No despachar F-04.

**Archivos esperados**

modify: Planned diff SPEC. no-touch: lista No-touch.

**No tocar**

F-01, F-02, F-04, F-05, S0, B1/B2, Slot Pool, Campaign stop policy, foreign dirty, migrations SQL.

**Spikes permitidos**

Ninguno de arquitectura. Si el ceiling Temporal no es aceptado por el SDK: PLAN_CONFLICT y parar.

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
TAREAS=T1.1-T1.8
SALIDA=source diff F-03 + grep SOURCE + tests cancel/liveness + nota en review
STOP=NO NORMAL IMPLEMENTATION AUTHORIZED YET
```

El bloque de despacho no sustituye la SPEC ni autoriza ejecución.

## 📆 Bitácora

- **2026-09-08** — TOP diseñó F-03 contra symphony `e50cb7e`. SPEC + TASKS persistidas. `DATABASE MIGRATION: NONE`. NORMAL no autorizado.

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

