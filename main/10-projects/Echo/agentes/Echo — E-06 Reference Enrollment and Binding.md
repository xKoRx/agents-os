---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo — Live Platform V1]]"
sprint:
start: 2026-09-16
due:
progress: 0
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-06
  - Reference enrollment and binding
  - E-06 RuntimeBinding
  - FEAT-REFERENCE-ENROLLMENT-BINDING-E6
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-16"
updated: "2026-09-16"
cssclasses:
  - wide
---

# Echo — E-06 Reference Enrollment and Binding

%% Naming: Echo — E-06 Reference Enrollment and Binding es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-06 Reference Enrollment and Binding
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-06 / Reference enrollment and binding. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Crear `RuntimeBinding` verificable: enrollment canónico por StrategyVersion, mapping observado account+broker+magic, operator ACK, read-back físico, coverage start barrier y attach manual verificado V1. Principio: **INGESTED / CONFIGURED / DB-BOUND ≠ OBSERVING**. Unlock: reloj forward atribuible para E-07/E-10.

## 📊 Estado actual

- **E06_PLANNING_READY_FOR_MANAGER_REVIEW (2026-09-16, docs-only, v1.0.0).** SPEC/PLAN/TASKS/VERIFICATION en `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/` sobre `feature/e06-reference-enrollment-binding` @ `9989f399fd992dc315f2bfe3279bfd862592ccf1` desde `origin/master` `5dd998f16aea7b2821f460188718d7a6d279829c`. **0 líneas en `v3/**`.** Master intacto. NORMAL no lanzado. No E-07. No PR.
- **RuntimeBinding key:** PK `binding_id` UUID; pin S0 `binding_ref = H("echo-reference-binding.v1",[ns,binding_id,version_ref,account_registration_ref,broker_server_ref,platform,magic_decimal,observation_class])`.
- **Lifecycle:** PREPARED → (ACK + matching read-back) → OBSERVING → DRAINING → CLOSED; staleness → SUSPENDED + UNKNOWN. PREPARED/ACK solos ≠ OBSERVING.
- **Read-back authority:** Bridge emite `REFERENCE_READBACK.v1`; Gateway persiste y transiciona. Operator ACK es CONFIG, no suficiente.
- **Coverage barrier:** `coverage_started_at = max(proof.recorded_at, capture_barrier_at)`. Prohibido created_at/ingestion/ACK clocks.
- **CANONICAL/SHADOW:** 1 CANONICAL OPEN-admitting por Version; SHADOW no suma. Duplicate collector y same-account overlap fail-closed.
- **Migración:** `064_reference_enrollment_binding` exclusiva E-06; FK a 061; SHARED DEV apply gated por 061 APPLIED (hoy NOT_APPLIED). 062/063 no-touch.
- **PHYSICAL:** matriz AC-01…15 sin órdenes; mocks ≠ OBSERVING. GAP-ECHO-006 terminal opcional extra.
- **Hipótesis accounts/policies solos:** REFUTADA en source/PG. Bastan accounts/policies (intent) + `reference_bindings` (hecho). No `deployments`.
- **AUTHORITY_CONFLICT:** ninguno. S0 ACTIVE/CLOSED = envelope de pin; lifecycle operacional = Live Authority §5. O1/O3 technical default Fable.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e06-reference-enrollment-binding` | `5dd998f16aea7b2821f460188718d7a6d279829c` | [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] §§5–6; O1/O3 Fable | `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/SPEC.md` v1.0.0 @ `9989f399` | E06_PLANNING_READY_FOR_MANAGER_REVIEW · 0 source · NORMAL no lanzado |

## 🗺️ Source map (baseline `5dd998f1` + PG/Hasura)

- Accounts/policies: intent mutable; sin version/hash/terminal/read-back.
- ClientConfig/Kafka/handshake: config delivery; sin ACK de EA.
- Bridge heartbeat + UnifiedBatch.magic: liveness/inventario; AccountRegistry no es unique físico.
- 061 source sí / SHARED DEV no. 062+063 DEV sí. `reference_bindings` ausente.
- S0 `RuntimeBinding` READ ONLY. E-04 INGESTED no-touch. E-02 CONFIG REUSE. MQL OUT_OF_SCOPE (C-3).

## 🎯 Target physical state

```text
v3/sdk/postgres/migrations/064_reference_enrollment_binding.{up,down}.sql
echo.reference_bindings + reference_readbacks + binding_transitions
echo.v_reference_bindings
POST /api/v1/reference/bindings[+ /ack /drain /suspend /close]
echo.reference-readback.v1   # Bridge → Gateway
ClientConfig additive pin fields
v3/hasura/metadata/tables/reference_bindings.yaml  # SELECT only
```

Ningún cambio a `v3/sdk/contracts/**`. Ningún MQL. Ningún E-07 DEAL. Ningún apply 061/064 a Aranea en NORMAL.

## 🕸️ Dependency graph

Ver TASKS.md. T01 persistencia → T05 HTTP → T11 OBSERVING. Emitter T10 ∥ HTTP. PHYSICAL T21 al final.

No ejecutar E-07…E-13. No reabrir E-01…E-05. E-04 T21 no bloquea. 061 DEV NOT_APPLIED no bloquea development (descartable); bloquea apply 064 SHARED DEV.

## Allowed scope NORMAL

Exacto PLAN.md. Development en `feature/e06-reference-enrollment-binding` desde `5dd998f1`. Worktree dedicado; no reutilizar checkout de otra fase. Prohibido `origin/master` push/merge. Prohibido `v3/sdk/contracts/**`. Prohibido 061/062/063. 064 exclusiva. Prohibido MQL. Prohibido Aranea PROD. Prohibido apply 064 SHARED DEV hasta 061 APPLIED (ops aparte).

## 📦 Work packages

- **WP-A Persistencia** T01–T03. 064 + stores + UNIQUEs.
- **WP-B Enrollment HTTP** T04–T07. PREPARED/ACK/drain + ClientConfig.
- **WP-C Read-back** T08–T11. Envelope, Bridge emitter, Gateway consumer, OBSERVING.
- **WP-D Gates negativos** T12–T15. Duplicate, overlap, mismatch, stale, DB-only.
- **WP-E READ/BWC/cert** T16–T22. Hasura, widen, SOURCE, coverage, PHYSICAL.

## TOP / NORMAL boundaries

- TOP: SPEC, esta nota, TASKS, PLAN puente, linkage padre. No source Go/SQL/HTTP productivo (cumplido).
- NORMAL: T01–T22 mecánicamente. No elegir recetas, no sintetizar OBSERVING, no hook EA, no E-07, no apply 061.
- GOD: NONE.

## Frozen decisions

1. `reference_bindings` es el hecho; accounts/policies son intent; no `deployments`.
2. OBSERVING exige ACK CONFIG **y** read-back Bridge matching.
3. Un CANONICAL OPEN-admitting por Version; SHADOW no suma.
4. Duplicate collector: UNIQUE physical key + epoch; segundo 409.
5. Same-account overlap magic prohibido hasta CLOSED+inventario vacío.
6. Pin Version write-once en PREPARED; config posterior no reinterpreta.
7. `coverage_started_at = max(proof.recorded_at, capture_barrier_at)`.
8. Stale > 15000ms persistidos → SUSPENDED + UNKNOWN.
9. Migración 064; FK 061; interlock SHARED DEV explícito.
10. Certificación sin órdenes. Mocks ≠ PHYSICAL OBSERVING.

## Migrations

Una: `064_reference_enrollment_binding` (exclusiva E-06). Depende de 061 **para apply**. Independiente de 062/063 semánticamente. 065+ fuera. Gate up/down/up en PG descartable 061→062→063→064. No apply PROD. No apply SHARED DEV sin 061.

## Dependency delta

NONE de terceros. `v3/sdk` importa contracts (mismo parent). Kafka topic nuevo sobre producer existente.

## Compatibility strategy

HTTP nuevo. ClientConfig additive. Hasura SELECT nueva. EA/journal legacy intactos. `active_positions.strategy_id` → text (deuda E-03).

## Testing / gates

SPEC AC-01…AC-25. SOURCE + CONTRACT + PG REAL + HTTP + PHYSICAL fixture zero-order + HASURA yaml. Ver VERIFICATION.md stub.

## Prohibited files

`v3/sdk/contracts/**`, `migrations/061-063_*`, `v3/clients/**`, `v3/front/**`, `v3/core/**`, Docker/Compose/deploy/workflows, Forge, `sync.sh`.

## Blockers

Ninguno para **planning**. Development: ninguno (PG descartable incluye 061). SHARED DEV 064 apply: **061 NOT_APPLIED** (ops/E-03). PHYSICAL terminal MT5: GAP-ECHO-006 opcional extra, no bloquea CONTRACT. E-04 T21 no bloquea.

## Handoff requirements

Manager aprueba planning v1.0.0 → **siguiente agente NORMAL** implementa T01–T22 en worktree dedicado de `feature/e06-reference-enrollment-binding` desde `5dd998f1`. No reutilizar checkout de otra fase. No merge/deploy. No E-07. No apply 061/064 Aranea.

## Closure conditions

Esta sesión TOP **no** cierra E-06. Cierre futuro: T01–T22 `[x]`; AC-01…AC-25; independent verifier; Manager; controlled integration. PHYSICAL SHARED DEV/PROD son gates aparte.

## 🧩 Subproyectos

_No aplica — hijo de implementación de E-06; no crea Integration ni más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/TASKS.md`. Aquí sólo work packages. NORMAL no arranca hasta manager review.
> - [x] TOP planning SPEC/PLAN/TASKS/VERIFICATION v1.0.0 → Manager Review #owner/agent #type/docs #area/echo
> - [ ] WP-A Persistencia 064 + stores + UNIQUEs #owner/agent #type/dev #area/echo
> - [ ] WP-B Enrollment HTTP PREPARED/ACK/drain + ClientConfig #owner/agent #type/dev #area/echo
> - [ ] WP-C Read-back Bridge→Gateway y transición OBSERVING #owner/agent #type/dev #area/echo
> - [ ] WP-D Gates negativos duplicate/overlap/mismatch/stale/DB-only #owner/agent #type/dev #area/echo
> - [ ] WP-E Hasura/BWC/SOURCE/PHYSICAL no-trading #owner/agent #type/dev #area/echo

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

## 📆 Bitácora

- **2026-09-16 (TOP planning one-shot)** — SPEC/PLAN/TASKS/VERIFICATION v1.0.0 @ `9989f399`. Hipótesis accounts/policies solos refutada; `reference_bindings` + intent. O1/O3 applied. 064 reservada. 0 source. Estado `E06_PLANNING_READY_FOR_MANAGER_REVIEW`. Puente padre → Review.

## 🧭 Decisiones (ejecución, no semántica nueva)

- Hijo de implementación de E-06; ownership sigue en [[Echo — Live Platform V1]], no Integration.
- OBSERVING nunca se sintetiza desde SQL/ACK/config.
- Apply 064 SHARED DEV es ops gated por 061, no NORMAL.
- PHYSICAL V1 usa collector fixture zero-order; terminal MT5 real es extra.

## 🔗 Docs / Links

- [[Echo — Live Platform V1]]
- [[Echo — E-04 Forge Ingestion E1]]
- [[Echo — E-03 Identity and BWC Foundation E0]]
- [[Echo — E-02 Control Safety, Auth and Journal Recovery]]
- [[Echo — E-05 Analytics Convergence A0]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]
- [[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]]
- [[Echo — Access & Physical Capability Matrix]]
- [[Echo — Producto Integrado]]

## 💡 Ideas

### Backlog de ideas

- Hook EA exportado: DEFER (C-3), no V1.

### Motivos / principios

- Ingestion no inicia el reloj. Una fila SQL no observa.

### Memoria pública / interna

- **Memoria pública:** contratos enlazados + SPEC del repo.
- **Memoria interna:** continuidad en esta nota.
- **Motivo:** el padre conserva el roadmap; este hijo conserva HOW/GATES.
