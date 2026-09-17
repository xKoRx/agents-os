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

- **E06_PLANNING_BLOCKED — MANAGER_DECISION_REQUIRED (2026-09-16, docs-only, SPEC v1.1.0 sin bump).** Reconciliación de autoridad zero-order magic = **CASE C**. Live Authority §5 exige inputs/readback observed-equality; C-3 defiere el hook SQX y no autoriza inequívocamente pin+KNOWN_EMPTY; collector no puede leer MagicNumber SQX. AutoTrading B2 intacto. C-3 DEFER intacto. Branch `feature/e06-reference-enrollment-binding` HEAD `349b6ac8bc4ef6701f20dd654ecbf796d406ba74` (contrato `1c794d5a`; old `3e190d86467a0c51bbe96afd1fad3d814117997d`). Baseline `origin/master` `5dd998f16aea7b2821f460188718d7a6d279829c`. **0 líneas productivas en `v3/**`.** Master intacto. NORMAL no lanzado. No E-07. No PR. Next gate = MANAGER REVIEW.
- **RuntimeBinding key:** PK `binding_id` UUID; pin S0 `binding_ref = H("echo-reference-binding.v1",[ns,binding_id,version_ref,account_registration_ref,broker_server_ref,platform,magic_decimal,observation_class])`.
- **Lifecycle:** PREPARED → (ACK + matching read-back) → OBSERVING → DRAINING → CLOSED; staleness → SUSPENDED + UNKNOWN. PREPARED/ACK solos ≠ OBSERVING.
- **Read-back authority:** Echo collector `reference_status` → Bridge `REFERENCE_READBACK.v1` → Gateway. Operator ACK es CONFIG, no suficiente. Heartbeat/UnifiedBatch/config **no** son OBSERVING.
- **Coverage barrier:** `coverage_started_at = max(proof.recorded_at, capture_barrier_at)`. Prohibido created_at/ingestion/ACK clocks.
- **CANONICAL/SHADOW:** 1 CANONICAL OPEN-admitting por Version; SHADOW no suma. Duplicate collector y same-account overlap fail-closed.
- **Migración:** `064_reference_enrollment_binding` exclusiva E-06; FK a 061; SHARED DEV apply gated por 061 APPLIED (hoy NOT_APPLIED). 062/063 no-touch.
- **PHYSICAL:** AC-01…15 + AC-26…32; producer real `reference_status`; fakes ≠ OBSERVING. GAP-ECHO-006 = PHYSICAL_PENDING, no PASS.
- **Hipótesis accounts/policies solos:** REFUTADA en source/PG. Bastan accounts/policies (intent) + `reference_bindings` (hecho). No `deployments`.
- **AUTHORITY_CONFLICT:** ninguno. S0 ACTIVE/CLOSED = envelope de pin; lifecycle operacional = Live Authority §5. O1/O3 technical default Fable.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e06-reference-enrollment-binding` | `5dd998f16aea7b2821f460188718d7a6d279829c` | [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] §§5–6; O1/O3 Fable; C-3 collector | `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/SPEC.md` v1.1.0 (CASE C blocked; HEAD `349b6ac8`; contrato `1c794d5a`; old `3e190d86`) | E06_PLANNING_BLOCKED — MANAGER_DECISION_REQUIRED · 0 source · NORMAL no lanzado |

## 🗺️ Source map (baseline `5dd998f1` + PG/Hasura)

- Accounts/policies: intent mutable; sin version/hash/terminal/read-back.
- ClientConfig/Kafka/handshake: config delivery; login+company; **sin** ACCOUNT_SERVER; **sin** ACK de EA.
- Bridge heartbeat: liveness vestigial; MQL Reference **no emite** heartbeat; payload ignorado. UnifiedBatch = Execution-only. AccountRegistry no es unique físico.
- 061 source sí / SHARED DEV no. 062+063 DEV sí. `reference_bindings` ausente.
- S0 `RuntimeBinding` READ ONLY. E-04 INGESTED no-touch. E-02 CONFIG REUSE. Hook SQX exportado OUT_OF_SCOPE (C-3 DEFER). Echo collector `reference_status` **IN SCOPE** (corrección 1.1.0).

## 🎯 Target physical state

```text
v3/sdk/postgres/migrations/064_reference_enrollment_binding.{up,down}.sql
echo.reference_bindings + reference_readbacks + binding_transitions
echo.v_reference_bindings
POST /api/v1/reference/bindings[+ /ack /drain /suspend /close]
echo.reference-readback.v1   # Bridge → Gateway, solo desde reference_status
ClientConfig additive pin fields
v3/clients/mt{4,5}/reference_v3.mq{4,5}  # reference_status mínimo (NORMAL futuro)
v3/hasura/metadata/tables/reference_bindings.yaml  # SELECT only
```

Ningún cambio a `v3/sdk/contracts/**`. Ningún MQL. Ningún E-07 DEAL. Ningún apply 061/064 a Aranea en NORMAL.

## 🕸️ Dependency graph

Ver TASKS.md. T01 persistencia → T05 HTTP → T09b collector status → T11 OBSERVING. Emitter T10 ∥ HTTP. PHYSICAL T21 al final con producer real.

No ejecutar E-07…E-13. No reabrir E-01…E-05. E-04 T21 no bloquea. 061 DEV NOT_APPLIED no bloquea development (descartable); bloquea apply 064 SHARED DEV. No abrir hook SQX.

## Allowed scope NORMAL

Exacto PLAN.md. Development en `feature/e06-reference-enrollment-binding` desde `5dd998f1`. Worktree dedicado; no reutilizar checkout de otra fase. Prohibido `origin/master` push/merge. Prohibido `v3/sdk/contracts/**`. Prohibido 061/062/063. 064 exclusiva. Prohibido hook SQX exportado. Permitido `reference_status` en Echo collector. Prohibido Aranea PROD. Prohibido apply 064 SHARED DEV hasta 061 APPLIED (ops aparte).

## 📦 Work packages

- **WP-A Persistencia** T01–T03. 064 + stores + UNIQUEs.
- **WP-B Enrollment HTTP** T04–T07. PREPARED/ACK/drain + ClientConfig.
- **WP-C Read-back** T08–T11 + T09b. Envelope, collector `reference_status`, Bridge emitter, Gateway consumer, OBSERVING.
- **WP-D Gates negativos** T12–T15. Duplicate, overlap, mismatch, stale, DB-only.
- **WP-E READ/BWC/cert** T16–T22. Hasura, widen, SOURCE, coverage, PHYSICAL.

## TOP / NORMAL boundaries

- TOP: SPEC, esta nota, TASKS, PLAN puente, linkage padre. No source Go/SQL/HTTP productivo (cumplido). Authority reconciliation CASE C docs-only. No eligió A ni B.
- NORMAL: **no lanzado**. T01–T22+T09b permanecen en el plan; T09b/T11 magic-match están gated por Manager. No elegir CASE A/B, no sintetizar OBSERVING, no hook SQX, no E-07, no apply 061.
- GOD: NONE.

## Frozen decisions

1. `reference_bindings` es el hecho; accounts/policies son intent; no `deployments`.
2. OBSERVING exige ACK CONFIG **y** `reference_status` matching. Heartbeat/UnifiedBatch/config/PG no bastan.
3. Un CANONICAL OPEN-admitting por Version; SHADOW no suma.
4. Duplicate collector: UNIQUE physical key + epoch **del producer EA**; segundo 409. Gateway no mint identity.
5. Same-account overlap magic prohibido hasta CLOSED+inventario vacío.
6. Pin Version write-once en PREPARED; config posterior no reinterpreta.
7. `coverage_started_at = max(proof.recorded_at, capture_barrier_at)`.
8. Stale > 15000ms sin `reference_status` → SUSPENDED + UNKNOWN.
9. Migración 064; FK 061; interlock SHARED DEV explícito.
10. Certificación sin órdenes. Unit fakes ≠ PHYSICAL OBSERVING. PHYSICAL exige producer `reference_status`.
11. `observed_magic` = inventario broker; KNOWN_EMPTY no se rellena desde config. **Si KNOWN_EMPTY basta para OBSERVING = CASE C, no frozen.**
12. `*_trade_allowed` se capturan; no gatean OBSERVING. VALID_NO_SIGNAL es E-07.
13. C-3: hook SQX DEFER; Echo collector status IN SCOPE.

## Migrations

Una: `064_reference_enrollment_binding` (exclusiva E-06). Depende de 061 **para apply**. Independiente de 062/063 semánticamente. 065+ fuera. Gate up/down/up en PG descartable 061→062→063→064. No apply PROD. No apply SHARED DEV sin 061.

## Dependency delta

NONE de terceros. `v3/sdk` importa contracts (mismo parent). Kafka topic nuevo sobre producer existente.

## Compatibility strategy

HTTP nuevo. ClientConfig additive. Hasura SELECT nueva. EA/journal legacy intactos. `active_positions.strategy_id` → text (deuda E-03).

## Testing / gates

SPEC AC-01…AC-25 + AC-26…AC-33. SOURCE + CONTRACT + PG REAL + HTTP + PHYSICAL producer `reference_status` zero-order + HASURA yaml. Ver VERIFICATION.md stub.

## Prohibited files

`v3/sdk/contracts/**`, `migrations/061-063_*`, `v3/clients/**` salvo collector `reference_status`, `v3/front/**`, `v3/core/**`, Docker/Compose/deploy/workflows, Forge, `sync.sh`.

## Blockers

**Zero-order magic = CASE C.** Manager debe elegir A, B o alternativa acotada antes de NORMAL. Development: ninguno adicional (PG descartable incluye 061). SHARED DEV 064 apply: **061 NOT_APPLIED** (ops/E-03). PHYSICAL producer real: GAP-ECHO-006 si no hay terminal collector; **no** se sustituye por fake. E-04 T21 no bloquea. C-3 DEFER del hook SQX conservado; status Echo collector compatible con C-3 y no puede afirmar MagicNumber SQX.

## Handoff requirements

Manager resuelve CASE C (A vs B vs alternativa) → sólo entonces planning puede relanzarse. **NORMAL no arranca.** No merge/deploy. No E-07. No hook SQX sin decisión. No apply 061/064 Aranea.

## Closure conditions

Esta sesión TOP **no** cierra E-06. Cierre futuro: T01–T22 `[x]`; AC-01…AC-25; independent verifier; Manager; controlled integration. PHYSICAL SHARED DEV/PROD son gates aparte.

## 🧩 Subproyectos

_No aplica — hijo de implementación de E-06; no crea Integration ni más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/TASKS.md`. Aquí sólo work packages. NORMAL no arranca hasta manager review.
> - [x] TOP planning SPEC/PLAN/TASKS/VERIFICATION v1.0.0 → Manager Review #owner/agent #type/docs #area/echo
> - [x] TOP planning correction #1 v1.1.0 zero-order physical authority → Manager Review #owner/agent #type/docs #area/echo
> - [x] TOP authority reconciliation zero-order magic → CASE C blocked #owner/agent #type/docs #area/echo
> - [ ] WP-A Persistencia 064 + stores + UNIQUEs #owner/agent #type/dev #area/echo
> - [ ] WP-B Enrollment HTTP PREPARED/ACK/drain + ClientConfig #owner/agent #type/dev #area/echo
> - [ ] WP-C Read-back Bridge→Gateway desde `reference_status` y transición OBSERVING #owner/agent #type/dev #area/echo
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

- **2026-09-16 (TOP authority reconciliation)** — CASE C. Live Authority §5 vs Fable C-3 no cierran si zero-order exige echo físico de magic. SPEC v1.1.0 sin bump; §7.3 KNOWN_EMPTY no es implementable. AutoTrading B2 intacto. C-3 DEFER intacto. HEAD `349b6ac8` (contrato `1c794d5a`; old `3e190d86`). Source delta `v3/` = 0. Estado `E06_PLANNING_BLOCKED — MANAGER_DECISION_REQUIRED`.
- **2026-09-16 (TOP planning correction #1)** — v1.1.0 @ `3e190d86` (contrato `ef8a96f3`; old `9989f399`). Heartbeat/UnifiedBatch no son autoridad zero-order. Producer congelado: `reference_status` Echo collector. Magic = inventario; KNOWN_EMPTY no se fabrica. AutoTrading = capability (B2). C-3 DEFER SQX conservado. Source mutations 0. Estado `E06_PLANNING_CORRECTED_READY_FOR_MANAGER_REVIEW`.
- **2026-09-16 (TOP planning one-shot)** — SPEC/PLAN/TASKS/VERIFICATION v1.0.0 @ `9989f399`. Hipótesis accounts/policies solos refutada; `reference_bindings` + intent. O1/O3 applied. 064 reservada. 0 source. Estado `E06_PLANNING_READY_FOR_MANAGER_REVIEW`. Puente padre → Review.

## 🧭 Decisiones (ejecución, no semántica nueva)

- Hijo de implementación de E-06; ownership sigue en [[Echo — Live Platform V1]], no Integration.
- OBSERVING nunca se sintetiza desde SQL/ACK/config/heartbeat/UnifiedBatch.
- Apply 064 SHARED DEV es ops gated por 061, no NORMAL.
- PHYSICAL V1 exige producer `reference_status`; fake ≠ PHYSICAL. Terminal MT5 real GAP-ECHO-006 pendiente no se disfraza de PASS.
- Residual C-3 (SQX input magic) **no** se abre. Status Echo collector ≠ hook C-3. Zero-order magic matching no es fail-closed congelado: es CASE C para Manager.

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

- Hook EA SQX exportado: DEFER (C-3), no V1. Echo collector `reference_status` no es ese hook.

### Motivos / principios

- Ingestion no inicia el reloj. Una fila SQL no observa.

### Memoria pública / interna

- **Memoria pública:** contratos enlazados + SPEC del repo.
- **Memoria interna:** continuidad en esta nota.
- **Motivo:** el padre conserva el roadmap; este hijo conserva HOW/GATES.
