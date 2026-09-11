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
start: 2026-09-11
due:
progress: 0
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-04
  - Forge ingestion E1
  - E-04 E1
  - FEAT-FORGE-INGESTION-E1
tags:
  - kind/project
  - area/echo
  - agent/owner
created: 2026-09-11
updated: 2026-09-11
cssclasses:
  - wide
---

# Echo — E-04 Forge Ingestion E1

%% Naming: Echo — E-04 Forge Ingestion E1 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-04 Forge Ingestion E1
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-04 / Forge ingestion E1. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Dejar el boundary Forge → Echo listo para aceptar un `HandoffManifestV1` autenticado, persistir mapping/version/promotion sobre foundations E-03, copiar artefactos operativos verificados y devolver receipt `INGESTED`, sin activation/provisioning/capital y sin decisiones críticas pendientes para NORMAL.

## 📊 Estado actual

- **TOP PLANNING READY FOR MANAGER REVIEW (2026-09-11).** Planning ejecutable creado desde cero: no existía proyecto Agents OS E-04 ni SPEC/PLAN/TASKS; sólo la Agent Task To Do en [[Echo — Live Platform V1]] y el join F-04 esperando endpoint. Feature ID canónico: `FEAT-FORGE-INGESTION-E1`.
- **Development MAY START** en paralelo con la verification independiente de E-03. **Integration NO:** gate `E03_CONTRACT_PASS_REQUIRED_FOR_INTEGRATION`.
- E-03 permanece `IMPLEMENTATION CLOSED / VERIFICATION PENDING` en `c408a12fe36643129a2ae3c3dfa69727b593ba76`. No se marca E-03 closed. No se marca E-04 implementing. No se marca Forge join closed.
- Baseline de development: `origin/master` = `c408a12f` (parent `233ec89c`). Branch `feature/e04-forge-ingestion-e1` worktree separado. Push a master prohibido.
- Contrato WHAT: `specs/FEAT-FORGE-INGESTION-E1/SPEC.md` v1.0.0. TASKS T01–T20. AC-01…AC-36.
- S0 certified READ ONLY @ `91671f6f`. Stores E-03 (mapping/version/promotion) se consumen, no se rediseñan.
- Carril Forge bloqueado en INTEGRATION: [[Echo Forge — F-04 Magic allocation, version seal and handoff]] (CONTRACT con `fakeconsumer`; no URL provisional). F-05 smoke de ingestión real espera este endpoint certificado.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e04-forge-ingestion-e1` | `c408a12fe36643129a2ae3c3dfa69727b593ba76` | [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] §4 + [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] (join) | `specs/FEAT-FORGE-INGESTION-E1/SPEC.md` v1.0.0 @ `618607f81a42c5234f5df31c69978489a6a0d764` | TOP READY_FOR_MANAGER_REVIEW · NORMAL no autorizado |

## 🗺️ Source map (baseline `c408a12f`)

- Gateway: `v3/gateway/internal/server.go` sin rutas `/api/v1/forge/promotions`.
- Auth ingest: ausente; no reutilizar Hasura admin secret.
- Blob/MinIO Echo: ausente → filesystem `artifact_root` + FixtureArtifactSource.
- Repos E-03: `strategy_{identity,version}_repository.go`, `promotion_record_repository.go` sobre `*sql.DB` (DBTX mecánico permitido).
- Schema 061: UNIQUE/FK write-once. E-04 no crea 062 de identidad.
- S0: `HandoffManifestV1`, `IdempotencyKey`, `fakeconsumer` (Forge CONTRACT, no sustituye PG).

## 🎯 Target physical state

```text
v3/gateway/internal/forge_ingest_{auth,handler}.go
POST /api/v1/forge/promotions
GET  /api/v1/forge/promotions/by-key/{key}
v3/sdk/postgres/ingestion_service.go
v3/sdk/postgres/ingestion_artifact.go
v3/sdk/postgres/dbtx.go
echo.strategy_identity_mappings + strategy_versions + promotion_records  # E-03, no nuevas tablas de receipt
artifact_root/sha256/<hex>   # copias operativas
```

Ningún cambio a `v3/sdk/contracts/**`. Ningún MQL. Ningún merge a master.

## 🕸️ Dependency graph

Ver TASKS.md. Paralelo inicial: T01 DBTX ∥ T02 artifacts ∥ T09 auth. T03 service. T10–T11 HTTP. T12–T15 gates. T20 cert.

No ejecutar E-02/E-05/E-06/F-05 aquí. No alterar E-03 para acomodar semántica.

## Allowed scope NORMAL

Exacto PLAN.md. Development en feature branch desde `c408a12f`. Prohibido `origin/master` push/merge. Prohibido `v3/sdk/contracts/**`. Prohibido 061/062 identidad. Prohibido allocator/activation.

## 📦 Work packages

- **WP-A Stores adapter** T01 (AC-33). DBTX.
- **WP-B Ingestion core** T02–T08. Service + artifacts + mapping/version/promotion tx + non-effects.
- **WP-C Gateway HTTP** T09–T13, T16. Auth, POST, GET, timeout, concurrency.
- **WP-D Corpus / SQL** T14–T15, T17. Golden S0 + SQL-direct + HandoffIngress test client.
- **WP-E Cert** T18–T20. SOURCE greps, coverage, governance interlock.

## TOP / NORMAL boundaries

- TOP: SPEC, esta nota, TASKS, PLAN puente, linkage padres, gobernanza de paralelismo. No source Go/SQL/HTTP productivo.
- NORMAL: T01–T20 mecánicamente. No elegir URL, codes, recetas S0, ni “arreglar” E-03/S0.
- GOD: NONE.

## Migrations

**Ninguna.** 061 no-touch. Mock SQL ≠ PASS.

## Dependency delta

```text
development dependency:  E-03 IMPLEMENTATION CLOSED @ c408a12f  (satisfecha)
integration dependency:  E-03 CONTRACT_PASS                     (NO satisfecha)
```

F-04 real opcional para tests; fixtures S0 primero. CROSS_LANE con Symphony espera integrate gate.

## Compatibility strategy

HTTP nuevo. Stores E-03 write-once. Webhooks Gateway intactos. Forge CONTRACT permanece en fakeconsumer hasta CROSS_LANE.

## Test strategy

AC-01…AC-36 ↔ TASKS. Corpus G01–G25/G31/G35 reusado. PG real obligatorio para CONTRACT/INTEGRATION/PHYSICAL. PHYSICAL E-04 = PG+HTTP+filesystem, no MetaTrader.

## Certification gates (NORMAL)

Ver PLAN.md. Clases: SOURCE, CONTRACT, INTEGRATION, PHYSICAL, MIGRATION=N/A, CROSS_LANE (gated), GOVERNANCE (`E03_CONTRACT_PASS_REQUIRED_FOR_INTEGRATION`).

## Branch strategy

- Crear/usar `feature/e04-forge-ingestion-e1` desde **exactamente** `c408a12f`.
- Worktree separado. Fetch OK. Feature push OK.
- Master push prohibido. Merge a master prohibido.
- Rebase sobre master cambiado por verification E-03 prohibido hasta manager review de incorporación.
- Tras E-03 CONTRACT_PASS: incorporar base, demostrar ancestry, rerun gates, entonces integrate review.

Si Verifier E-03 FAIL: `BLOCKED_PENDING_E03_CORRECTION`.

## Blockers

Ninguno para **development**. Integrate/CLOSED bloqueado por E-03 verification. F-04 PHYSICAL/CC no bloquea E-04 CONTRACT.

## Handoff requirements

Manager aprueba planning → NORMAL implementa T01–T20 en el worktree de esta branch. No usar el checkout `master` local behind. No cerrar E-03. No declarar join Forge CLOSED.

## Closure conditions

T01–T20 `[x]`; AC-01…AC-36; allowed files; 061 intacto; non-effects; E-03 identity tests PASS; `VERIFICATION.md` con evidencia; **y** `E-03 CONTRACT_PASS` antes de merge/CLOSED. Este TOP no cierra E-04.

## 🧩 Subproyectos

_No aplica — hijo de implementación de E-04; no crea Integration ni más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-FORGE-INGESTION-E1/TASKS.md`. Aquí sólo work packages. NORMAL no arranca hasta manager review.
> - [ ] WP-A DBTX adapter sobre repos E-03 #owner/agent #type/dev #area/echo
> - [ ] WP-B Ingestion service + artifacts + tx + non-effects #owner/agent #type/dev #area/echo
> - [ ] WP-C Gateway POST/GET + auth + timeout/concurrency #owner/agent #type/dev #area/echo
> - [ ] WP-D Corpus S0 HTTP + SQL-direct + HandoffIngress test client #owner/agent #type/dev #area/echo
> - [ ] WP-E SOURCE/coverage/governance cert pack #owner/agent #type/dev #area/echo

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

- **2026-09-11 (TOP)** — Recovery: no había proyecto E-04 ni SPEC ejecutable. Se materializa este hijo, SPEC/PLAN/TASKS `FEAT-FORGE-INGESTION-E1` en branch `feature/e04-forge-ingestion-e1` desde `c408a12f` (planning SHA `618607f8`, pushed; `origin/master` intacto). Gobernanza: development paralelo a verification E-03; integrate gated por CONTRACT_PASS. Join F-04 congelado (HTTP + S0 + receipt). Estado `READY FOR MANAGER REVIEW`. No NORMAL. No master push. No session close.

## 🧭 Decisiones (ejecución, no semántica nueva)

- Hijo de implementación de E-04; ownership sigue en [[Echo — Live Platform V1]], no Integration.
- `development dependency` ≠ `integration dependency`.
- Conflicting replay usa code S0 `CONTRACT_CONFLICT`; no se añade code rival en `v3/sdk/contracts/wire`.
- Filesystem artifact store V1; corpus `minio` se resuelve por fixture allowlisted.
- DBTX es el único retoque mecánico permitido a repos E-03.

## 🔗 Docs / Links

- [[Echo — Live Platform V1]]
- [[Echo — Producto Integrado]]
- [[Echo — E-03 Identity and BWC Foundation E0]]
- [[Echo — E-01 Canonical SDK Foundation S0]]
- [[Echo Forge — F-04 Magic allocation, version seal and handoff]]
- [[Echo Forge — Factory V2 Completion]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]
- [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]
- SPEC: `xKoRx/echo` `specs/FEAT-FORGE-INGESTION-E1/SPEC.md`
- TASKS: `xKoRx/echo` `specs/FEAT-FORGE-INGESTION-E1/TASKS.md`
- PLAN puente: `xKoRx/echo` `specs/FEAT-FORGE-INGESTION-E1/PLAN.md`

## 💡 Ideas

### Backlog de ideas

- Hasura tracking de promotions: E-13, no aquí.
- Cliente HTTP productivo en Symphony: F-04 INTEGRATION tras E-03 CONTRACT_PASS, no este TOP.

### Motivos / principios

- Una fuente por hecho: SPEC = contrato; esta nota = ejecución; TASKS = checklist.
- `INGESTED` es receipt, no live.

### Memoria pública / interna

- **Memoria pública:** Resources frozen enlazadas.
- **Memoria interna:** continuidad en esta nota.
- **Motivo:** no duplicar FR-1…FR-5 ni rediseñar E-03.
