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
start: 2026-09-10
due:
progress: 0
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-03
  - Identity and BWC foundation E0
  - E-03 E0
  - FEAT-CROSS-IDENTITY-BWC-E0
tags:
  - kind/project
  - area/echo
  - agent/owner
created: 2026-09-10
updated: 2026-09-10
cssclasses:
  - wide
---

# Echo — E-03 Identity and BWC Foundation E0

%% Naming: Echo — E-03 Identity and BWC Foundation E0 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-03 Identity and BWC Foundation E0
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-03 / E0. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Dejar persistence/protocol groundwork para StrategyVersion, PromotionRecord, wide IDs, magic int64, legacy dispatch, inmutabilidad, schema protection y BWC, sin decisiones críticas pendientes para NORMAL.

## 📊 Estado actual

- **TOP PLANNING READY_FOR_MANAGER_REVIEW (2026-09-10 relational integrity):** SPEC v1.1.1 cierra UNIQUE + FK compuestos Mapping→Version→Promotion. Parent `45a59fca1058203df6baf20c3cfe1d000251159d`. Correction SHA `576bf1f49f116826a8141126fbb520b80a7d1a3c` (FF `origin/master`). Sin source Go/SQL. No implementation complete. No closed.
- **E-01:** certified S0; no reabrir.
- **Contrato WHAT:** `specs/FEAT-CROSS-IDENTITY-BWC-E0/SPEC.md` v1.1.1.
- **Checklist:** `specs/FEAT-CROSS-IDENTITY-BWC-E0/TASKS.md` (T01–T23; ACs AC-01…AC-18). T08/T10/T12/T13 cierran constraints y INSERT SQL directo.
- **PLAN.md local Echo:** puente de gobernanza; no copia esta nota.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `master` (fase E-03) | `c22fe218127c7e97fb40951ddcafc13d80ede152` | [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] §§2–3, 9 + SDK Canonical V1 (S0 certified) | `specs/FEAT-CROSS-IDENTITY-BWC-E0/SPEC.md` v1.1.1 @ `576bf1f49f116826a8141126fbb520b80a7d1a3c` | TOP READY_FOR_MANAGER_REVIEW |

## 🗺️ Source map (baseline planning `c22fe218`; source físico = E-01 certified `91671f6f`)

- `echo.strategy_definitions.id varchar(64)` — V2_CANONICAL; 061 → text.
- `trade_journal`/`lab_*`/`lab_api_*` `strategy_id varchar(64)` — V2_CANONICAL; 061 → text. Policy `strategy_id` ya `text`.
- `echo.active_positions.strategy_id varchar(50)` — **DEFERRED** E-06; 061 no ALTER. Gate: identity repos no escriben posiciones.
- `magic_number` journal canónico `bigint`; leftover `magic_number_override int4`.
- Tickets PG ya `int8`/`bigint`. `ReferenceTicket int32` → `int64` **acotado** `1..MaxInt64` (no uint64). MT5 `ulong > MaxInt64` → UNSUPPORTED.
- EA `TradeMapRecord` sin header: MT5 `ulong ticket` + `uchar[64]` + `int magic`; MT4 `int ticket`. v1 cookie **9** bytes `ECHO-TMAP` + CRC-32/IEEE LE.
- `ensureJournalParentRows` autoprovisiona descriptor; no mapping V2.
- S0: `contracts.StrategyVersionRef`, `MagicAllocation.magic_decimal` string, G19–G21 corpus. **No editar contracts.**
- Migrator golang-migrate; última `060`; siguiente **061**.
- Hasura yaml **no** trackea `strategy_definitions`; protección = REVOKE/trigger SQL.
- **No** existe `strategy_versions` / `promotion_records` / allocator Echo.

## 🎯 Target physical state

```text
v3/sdk/postgres/migrations/061_identity_bwc_foundation.{up,down}.sql
v3/sdk/postgres/strategy_{identity,version}_repository.go
v3/sdk/postgres/promotion_record_repository.go
v3/sdk/postgres/tests/identity_bwc/**
v3/sdk/eapersist/**          # codec v0/v1 medido
v3/clients/mt{4,5}/EchoPersistence.mqh
v3/clients/mt{4,5}/testdata/trademap/**
v3/bridge/internal/pipe_handler.go   # echo-identity-wire.v1
v3/sdk/domain/reference_event.go     # ReferenceTicket int64 (1..MaxInt64)
```

Ningún HTTP Forge. Ningún cambio a `v3/sdk/contracts/**`.

## 🕸️ Dependency graph

Ver `TASKS.md`. Paralelo inicial: T01–T07 (EA) ∥ T08–T10 (SQL). T11–T13 repos. T16–T17 wire. T23 cert.

No ejecutar E-02/E-04/E-05/F-04 aquí.

## Allowed scope NORMAL

Exacto PLAN.md. Prohibido contracts S0, Gateway ingestion, Symphony, allocator, tests ajenos sin `TEST_CHANGE_REQUEST`.

## 📦 Work packages

- **WP-A Layout EA** T01–T07. v0 medido; v1 SPEC §10.6 (cookie 9, LE, CRC IEEE, framing); MT4 no int64.
- **WP-B Schema 061** T08–T10, T18, T19, T21. Widen V2_CANONICAL techo 64; no `active_positions`; down umbral 64; UNIQUE identity tuple + FK compuestos; `15_identity_tuple_fk.sql` INSERT directo.
- **WP-C Stores** T11–T15, T22. Mapping PK `(ns, canonical)` + UNIQUE identity tuple; Version PK `(ns, version_ref)` + FK 3-col; Promotion FK 4-col. Repository no es la única autoridad.
- **WP-D Wire** T16–T17, T14. String decimal; ticket 1..MaxInt64; G20/G21.
- **WP-E Cert** T20, T23. No allocator; AC-01…AC-17.

## TOP / NORMAL boundaries

- TOP: SPEC, esta nota, TASKS, PLAN puente, linkage padre. No source Go/SQL.
- NORMAL: T01–T23 mecánicamente. No elegir semántica de identidad, política de migración, ni “arreglar” S0.
- GOD: NONE.

## Migrations

**061** obligatoria. Motor golang-migrate. Transacción única + backup de relaciones modificadas (no `active_positions`). Interrupt = ROLLBACK. Down aborta si `octet_length > 64` en columnas ex-64 o magic >int32. No umbral 50. Mock SQL ≠ PASS.

## Dependency delta

Parent SDK puede seguir igual. `eapersist` es paquete nuevo bajo `v3/sdk`. No pin de terceros salvo el migrator ya usado. Stdlib para codec.

## Compatibility strategy

Paths nuevos para identity/version/promotion. Dual-read TradeMap y pipe. Legacy `magic_*` scoped. No recanonicalizar. No backfill Version sobre journal.

## Test strategy

SPEC AC-01…AC-18 mapeados 1:1 a TASKS. G19–G21 S0 se reusan como inputs de persistencia, no se regeneran. PHYSICAL: binarios `FileWriteStruct` + PG real + INSERT SQL directo de identidad. INTEGRATION: repos. SOURCE: codec/grep. Schema, no mock.

## Certification gates (NORMAL)

```bash
# SOURCE
go test ./v3/sdk/eapersist ./v3/sdk/postgres ./v3/sdk/domain
go vet ./v3/sdk/eapersist ./v3/sdk/postgres ./v3/sdk/domain

# MIGRATION + PHYSICAL PG (harness existente de postgres tests)
# aplicar 061 sobre clone de schema 060; 10_migrate_up.sql; 11_migrate_idempotent.sql; 12_migrate_interrupt.sql; 14_width_classification.sql

# INTEGRATION
go test ./v3/sdk/postgres -run 'Identity|Version|Promotion|Magic|Alias|Pipe'

# PHYSICAL EA
# fixtures v0.bin deben coincidir con sizeof frozen; convert interrupt restore
```

Parent `go test ./...` de etcd/Kafka/Jaeger **no** es gate (fallos preexistentes E-01).

## Baseline tests (registrados, no ampliar)

Mismos FAIL de infra que E-01 (etcd/Kafka/Jaeger). No “arreglarlos” en E-03.

## Release / pin expectations

Manager acepta planning. NORMAL implementa. Verifier independiente escribe `VERIFICATION.md`. No tag. Push de implementación sólo si el manager lo pide; este TOP sí publica planning FF a `master`.

## Blockers

Ninguno material para arrancar NORMAL tras aceptación manager. Graphify del repo Echo está stale (v1): no bloquear. MCP Agents OS no autenticado en esta sesión: vault escrito por filesystem.

## Handoff requirements

NORMAL trabaja contra `576bf1f4` + SPEC v1.1.1 + TASKS **después** de aceptación manager. Dirty foráneo del checkout habitual se preserva (worktree). Un commit de implementación aparte de los commits SDD TOP.

## Closure conditions

T01–T23 `[x]`; gates T23 PASS; allowed files respetados; AC-01…AC-18 cubiertos; no allocator; layouts v0 addressable; 061 idempotente; FKs de identidad DB-enforced; certificación en `VERIFICATION.md` (fuera de este TOP).

## 🧩 Subproyectos

_No aplica — hijo de implementación de E-03; no crea Integration ni más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-CROSS-IDENTITY-BWC-E0/TASKS.md`. Aquí sólo work packages.
> - [ ] WP-A Layout EA v0/v1 + MT4 legacy #owner/agent #type/dev #area/echo
> - [ ] WP-B Schema 061 widen/protection/migration gates #owner/agent #type/dev #area/echo
> - [ ] WP-C Stores identity/version/promotion/aliases #owner/agent #type/dev #area/echo
> - [ ] WP-D Wire string magic + ticket 1..MaxInt64 #owner/agent #type/dev #area/echo
> - [ ] WP-E Certification AC-01…AC-17 + no allocator #owner/agent #type/dev #area/echo

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

- **2026-09-10 (TOP)** — Discovery en worktree limpio `origin/master`=`91671f6f`. SPEC/PLAN/TASKS `FEAT-CROSS-IDENTITY-BWC-E0`. Decisiones: mapping V2 separado del descriptor Lab; 1024 bytes freeze; magic bigint + string wire; TradeMap v0 medido/v1 header; 061 transaccional; MT4 no int64; RuntimeBinding table diferida a E-06. Planning SHA `c22fe218127c7e97fb40951ddcafc13d80ede152` publicado FF a `origin/master`.
- **2026-09-10 (TOP correction)** — Gaps A–D cerrados en SPEC v1.1.0. Cookie `ECHO-TMAP` = 9 bytes; v1 §10.6 LE+CRC-32/IEEE; ticket Option 2 `1..MaxInt64`; Version PK `(registry_namespace, version_ref)` + FK mapping; `active_positions.strategy_id` DEFERRED. SHA `45a59fca1058203df6baf20c3cfe1d000251159d`. Estado `READY_FOR_MANAGER_REVIEW`. No NORMAL.

## 🧭 Decisiones (ejecución, no semántica nueva)

- Hijo de implementación de E-03; ownership sigue en [[Echo — Live Platform V1]], no Integration.
- `v3/sdk/contracts` es autoridad de recetas, no de schema PG.
- Cookie v1 `ECHO-TMAP` **9 bytes** (`45 43 48 4F 2D 54 4D 41 50`); header 32; CRC-32/IEEE LE sobre Header\|\|Records; v0 = ausencia de cookie + múltiplo de sizeof medido.
- Ticket Echo: `1..MaxInt64`; no full MT5 `ulong`; PG `bigint`; Go `int64`.
- Mapping PK `(registry_namespace, canonical_strategy_id)`; Version PK `(registry_namespace, version_ref)`; Promotion FKs a ambas. `StrategyVersionRef` S0 sin namespace.
- `active_positions.strategy_id varchar(50)` DEFERRED a E-06.
- SQL eager; EA lazy-on-open con backup.
- Down 061 fail-closed si `octet_length > 64` en columnas ensanchadas desde 64.

## 🔗 Docs / Links

- [[Echo — Live Platform V1]]
- [[Echo — Producto Integrado]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]
- SPEC: `xKoRx/echo` `specs/FEAT-CROSS-IDENTITY-BWC-E0/SPEC.md`
- TASKS: `xKoRx/echo` `specs/FEAT-CROSS-IDENTITY-BWC-E0/TASKS.md`
- PLAN puente: `xKoRx/echo` `specs/FEAT-CROSS-IDENTITY-BWC-E0/PLAN.md`

## 💡 Ideas

### Backlog de ideas

- Hasura tracking de las tablas nuevas: E-04/E-13, no aquí (REVOKE basta).

### Motivos / principios

- Una fuente por hecho: SPEC = contrato; esta nota = ejecución; TASKS = checklist.

### Memoria pública / interna

- **Memoria pública:** Resources frozen enlazadas.
- **Memoria interna:** continuidad en esta nota.
- **Motivo:** no duplicar FR-1…FR-5 ni el roadmap E-04.
