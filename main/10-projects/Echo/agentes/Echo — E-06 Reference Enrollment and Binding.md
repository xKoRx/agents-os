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
updated: "2026-09-17"
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

- **E06_FORGE_PRODUCER_IMPLEMENTED_PHYSICAL_PENDING (2026-09-17, lane A NORMAL).** Producer atestación §7.2a inyectado en `EchoForgeMT5Exporter.java` (Forge `feature/e06-runtime-attestation-exporter` @ `508b4a2` desde `3d0e8c9` F-05-I; push FF; sin merge). Contract §17 A–O PASS, build plugin PASS, idempotencia byte-stable, MagicNumber/mmLots intactos. PHYSICAL_PENDING (sin terminal MT5/SQX aquí; AC-34/AC-35 esperan físico). Gate Manager del lane pendiente; E-06 NO CLOSED; NORMAL Echo (WP-A…WP-E) no lanzado.
- **E06_PLANNING_READY_FOR_IMPLEMENTATION_REVIEW (2026-09-16, docs-only, SPEC v1.2.2).** Erratum de liveness del refresh §7.2a.4: MQL5 no garantiza ticks cada 5 s ⇒ el `MUST` de republicación vía `OnTick` era garantía irrealizable. Decisión Manager frozen: `OnTimer` existente realmente activado con período ≤5 s **preferido** (prohibido modificar `EventSetTimer`/crear timer); si sólo `OnTick`, renovación **oportunista** — 5 s = intervalo mínimo entre publicaciones, no frecuencia; sin tick ni timer compatible **sin promesa de liveness continua** (expiración 15 s fail-closed `SUSPENDED + UNKNOWN`; recovery §6 con nueva atestación matching; ninguna actualización de `ts` desde Echo/Bridge/Gateway/config). Tests AC-37a…d. CASE B **intacto**; encoding v1 intacto. Corrección previa del transporte §7.2a: encoding `echo.attest.v1.<acct16>.<chart16>.<field>` con `mh`/`ml` uint32 exactos, commit par, `ts` escrito (nunca `GlobalVariableTime`), `chart_ref` obligatorio, FNV-1a32 de `ACCOUNT_SERVER`. Inyección Forge: post-`generate`+`assertNonZeroLots` en `EchoForgeMT5Exporter.java`, scanner estructural, fail-closed, **no implementada**. Branch Forge observada `codex/f05-release-prep` @ `0ddd4db` (blob `cfbd5b78`); `master` `0b9742b` no es la de desarrollo. HEAD Echo `acf996ad043f87d6bbe6ae7b6190d1eb801e908a` (contrato `28afc47faf72b70e67b141b39224b8674f98458b`; old `336c723b`; push FF). Baseline `origin/master` `5dd998f16aea7b2821f460188718d7a6d279829c`. **0 líneas productivas en `v3/**`; 0 bytes Forge mutados.** Master intacto. NORMAL no lanzado. No E-07. No PR. Next gate = IMPLEMENTATION REVIEW.
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
| xKoRx/echo | `feature/e06-reference-enrollment-binding` | `5dd998f16aea7b2821f460188718d7a6d279829c` | [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] §§5–6; O1/O3 Fable; C-3 collector + excepción Manager §7.2a | `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/SPEC.md` v1.2.2 (encoding v1 + erratum liveness refresh; HEAD `acf996ad`, contrato `28afc47f`; previo `336c723b`) | E06_PLANNING_READY_FOR_IMPLEMENTATION_REVIEW · 0 source · NORMAL no lanzado |
| xKoRx/symphony (Forge) | `feature/e06-runtime-attestation-exporter` @ `508b4a2` (parent `3d0e8c9` = cierre F-05-I; push FF; base `codex/f05-release-prep`) | `3d0e8c958765da23840e00bf1a0ac017fc47597a` (blob exporter `cfbd5b78` verificado pre-write) | F-04 sello/readback magic | SPEC §7.2a v1.2.2 implementada: inyección post-`generate`+`assertNonZeroLots` en `EchoForgeMT5Exporter.java` (scanner estructural no-regex, fail-closed, idempotente `ECHO_ATTEST_V1_*`, encoding v1, refresh §7.2a.4). Tests §17 A–O contract PASS; build plugin PASS; **PHYSICAL_PENDING** (sin terminal MT5/SQX) | E06_FORGE_PRODUCER_IMPLEMENTED_PHYSICAL_PENDING · lane propio, gate Manager pendiente |

## 🗺️ Source map (baseline `5dd998f1` + PG/Hasura)

- Accounts/policies: intent mutable; sin version/hash/terminal/read-back.
- ClientConfig/Kafka/handshake: config delivery; login+company; **sin** ACCOUNT_SERVER; **sin** ACK de EA.
- Bridge heartbeat: liveness vestigial; MQL Reference **no emite** heartbeat; payload ignorado. UnifiedBatch = Execution-only. AccountRegistry no es unique físico.
- 061 source sí / SHARED DEV no. 062+063 DEV sí. `reference_bindings` ausente.
- S0 `RuntimeBinding` READ ONLY. E-04 INGESTED no-touch. E-02 CONFIG REUSE. Hook SQX de coverage OUT_OF_SCOPE (C-3 DEFER). Echo collector `reference_status` + relay de atestaciones IN SCOPE (§7.2a). Producer del strategy EA = Forge exporter (`EchoForgeRobustRunExporter` estampa `MagicNumber` input; `EchoForgeMT5Exporter` genera; `magic-readback` verifica; sello F-04 exige allocated==readback).
- `reference_v3.mq{4,5}`: sin magic input propio; `GetEffectiveMagicNumber` = POSITION_MAGIC o fallback ClientConfig (prohibido como atestación). Cero `GlobalVariable*`/`ACCOUNT_SERVER`/`CHART_EXPERT_NAME` hoy: helpers net-new T09b (reconstrucción encoding v1, sólo lectura).

## 🎯 Target physical state

```text
v3/sdk/postgres/migrations/064_reference_enrollment_binding.{up,down}.sql
echo.reference_bindings + reference_readbacks + binding_transitions
echo.v_reference_bindings
POST /api/v1/reference/bindings[+ /ack /drain /suspend /close]
echo.reference-readback.v1   # Bridge → Gateway, solo desde reference_status
ClientConfig additive pin fields
v3/clients/mt{4,5}/reference_v3.mq{4,5}  # reference_status mínimo + relay verbatim atestaciones §7.2a (NORMAL futuro)
v3/hasura/metadata/tables/reference_bindings.yaml  # SELECT only
(xKoRx/symphony) EchoForgeMT5Exporter.java  # inyección atestación §7.2a — lane Forge, un archivo
```

Ningún cambio a `v3/sdk/contracts/**`. MQL sólo el delta collector T09b. Ningún E-07 DEAL. Ningún apply 061/064 a Aranea en NORMAL. Resto de Forge intocado.

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

- TOP: SPEC, esta nota, TASKS, PLAN puente, linkage padre. No source Go/SQL/HTTP productivo (cumplido). Corrigió el transporte §7.2a a encoding v1 (sin cambiar CASE B). No implementó la inyección.
- NORMAL: **no lanzado** (gate Manager). T01–T22+T09b desbloqueados por v1.2.0: zero-order = atestación runtime §7.2a + KNOWN_EMPTY; fail-closed `RUNTIME_ATTESTATION_ABSENT`/`MISMATCH`. No sintetizar OBSERVING, no hook SQX de coverage, no E-07, no apply 061. La inyección Forge (un archivo) corre en lane Forge con gate propio.
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
10. Certificación sin órdenes. Unit fakes ≠ PHYSICAL OBSERVING. PHYSICAL exige producer `reference_status` + Version con inyección §7.2a.
11. `observed_magic` = inventario broker; `runtime_attestations` = reconstrucción lossless encoding v1 §7.2a; sin backfill/mint desde config/PG/Version. **Zero-order (Manager CASE B): `effective_magic == binding.magic_decimal` atestiguado por la instancia EA strategy; ausente/mismatch ⇒ fail-closed. Nunca trade/pending/DEAL artificial.** `chart_ref` obligatorio. Vigencia = `ts` escrito, nunca `GlobalVariableTime`.
12. `*_trade_allowed` se capturan; no gatean OBSERVING. VALID_NO_SIGNAL es E-07.
13. C-3: hook SQX de **coverage** DEFER; excepción §7.2a = **sólo** atestación de identidad runtime mínima (sin signals/deals/coverage/métricas/lifecycle/telemetría/estado). Echo collector status + relay IN SCOPE.
14. Identidad de Version: inyectar atestación cambia bytes ⇒ **nuevo** `strategy_version_ref` (canonical_strategy_id estable). Versions históricos nunca se mutan; fail-closed `RUNTIME_ATTESTATION_ABSENT`. Re-enroll = nueva exportación + ingestion + nuevo `binding_id`.

## Migrations

Una: `064_reference_enrollment_binding` (exclusiva E-06). Depende de 061 **para apply**. Independiente de 062/063 semánticamente. 065+ fuera. Gate up/down/up en PG descartable 061→062→063→064. No apply PROD. No apply SHARED DEV sin 061.

## Dependency delta

NONE de terceros. `v3/sdk` importa contracts (mismo parent). Kafka topic nuevo sobre producer existente.

## Compatibility strategy

HTTP nuevo. ClientConfig additive. Hasura SELECT nueva. EA/journal legacy intactos. `active_positions.strategy_id` → text (deuda E-03).

## Testing / gates

SPEC AC-01…AC-25 + AC-26…AC-33. SOURCE + CONTRACT + PG REAL + HTTP + PHYSICAL producer `reference_status` zero-order + HASURA yaml. Ver VERIFICATION.md stub.

## Prohibited files

`v3/sdk/contracts/**`, `migrations/061-063_*`, `v3/clients/**` salvo collector `reference_status`+relay §7.2a, `v3/front/**`, `v3/core/**`, Docker/Compose/deploy/workflows, Forge/symphony **salvo la inyección de un archivo §7.2a en lane Forge propio**, `sync.sh`.

## Blockers

**Planning: ninguno** (transporte v1.2.1 cerrado; CASE B intacto). Development: ninguno adicional (PG descartable incluye 061). SHARED DEV 064 apply: **061 NOT_APPLIED** (ops/E-03). PHYSICAL producer real: GAP-ECHO-006 si no hay terminal collector **y/o** Version Forge con inyección §7.2a.5; **no** se sustituye por fake. E-04 T21 no bloquea. La inyección Forge requiere lane/gate Forge propio **y** reidentificar branch de WRITE (`codex/f05-release-prep` observada; `master` no autorizada por el hecho de ser master) — bloquea sólo los AC PHYSICAL de atestación, no CONTRACT.

## Handoff requirements

Implementation review de v1.2.2 (erratum liveness + encoding v1 + CASE B intacto) → autoriza NORMAL. **NORMAL no arranca antes.** No merge/deploy. No E-07. Hook SQX de coverage sigue DEFER. No apply 061/064 Aranea. La inyección Forge se ejecuta como expansión de borde de un archivo con gate Manager/Forge **después** de reidentificar la branch autorizada.

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
> - [x] TOP planning correction #2 v1.2.0 Manager CASE B + producer discovery §7.2a → Manager Review #owner/agent #type/docs #area/echo
> - [x] TOP transport contract correction v1.2.1 encoding GV lossless → Manager Review #owner/agent #type/docs #area/echo
> - [x] TOP refresh liveness erratum v1.2.2 (OnTimer compatible / OnTick oportunista / sin liveness continua prometida) → Implementation Review #owner/agent #type/docs #area/echo
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

- **2026-09-17 (NORMAL Forge lane A — producer atestación §7.2a)** — Implementada la inyección del producer `echo.attest.v1` en `EchoForgeMT5Exporter.java` (único archivo productivo, repo `xKoRx/symphony`). Baseline verificado pre-write: `origin/codex/f05-release-prep` @ `3d0e8c958765da23840e00bf1a0ac017fc47597a` (parent `0ddd4db`), blob exporter `cfbd5b78` exacto; worktree dedicado limpio (el worktree principal tenía un fixture de benchmark ajeno modificado, preservado sin tocar). Branch `feature/e06-runtime-attestation-exporter` @ `508b4a253dfb6cf6419dc5fc3f1be94801745a93`, push FF, sin merge/PR/master. Implementación: inserción por offsets tras `generate`+`assertNonZeroLots` (no movido), scanner estructural state-machine (comentarios/strings/chars/preprocessor, braces, duplicados), helper MQL5 `EchoAttestV1_*` con encoding v1 congelado (split mh/ml uint32 exactos — roundtrip max int64 verificado, `ts` escrito con `TimeGMT`, commit par ≥2, invalidación c=0, cleanup residual n(K+1)..n15, FNV-1a32 UTF-8 de ACCOUNT_SERVER con goldens, chunking big-endian n0..n15, límites nl 1..63), publish sólo en `return INIT_SUCCEEDED` literal (returns no literales o fall-through ⇒ fail-closed export), revoke primera sentencia de OnDeinit (append mínimo si falta), refresh §7.2a.4 v1.2.2 (OnTimer compatible preferido: `EventSetTimer(P)` único literal, statement top-level de OnInit, 0<P≤5, sin tocar EventSetTimer/EventKillTimer; si no OnTick oportunista; sin sitio exporta sin liveness prometida), idempotencia byte-stable por marcadores, post-condiciones byte-level (readback FromMQ5 espejo, línea MagicNumber y mmLots idénticas), cero llamadas de trading en el bloque. Contract tests §17 A–O + missing-OnInit PASS (22/22 suite), JUnit trades 13/13, RobustRun/WFM OK; build.sh PASS; `verify_build.sh` FAIL_BASELINE_KNOWN (carrera SIGPIPE `grep -q`+`pipefail`, falla igual en baseline puro 3/3; verificación semántica equivalente a mano: 5/5 exporters, 0 test-support). PHYSICAL_PENDING: sin terminal MT5 ni SQX Build 142 en esta máquina (no compile MQ5, no export real; AC-34/AC-35 esperan entorno físico; JDK portable Temurin 17 en /tmp fue requerido). Echo repo y resto de Forge intactos; Versions históricos intactos (identidad nueva por export futuro). Estado del lane: `IMPLEMENTED` + `SOURCE_VERIFIED` + `PHYSICAL_PENDING`. **E-06 NO CLOSED**; handoff al Manager.

- **2026-09-16 (TOP refresh liveness erratum — v1.2.2)** — Defecto: §7.2a.4 v1.2.1 exigía «MUST republicar al menos cada 5 s» con sitio `OnTick`; MQL5 no garantiza ticks cada 5 s ⇒ garantía temporal irrealizable. Decisión Manager frozen (sólo semántica de refresh): `OnTimer` existente realmente activado con período ≤5 s preferido; prohibido modificar `EventSetTimer` existente ni crear timer; si sólo `OnTick`, renovación oportunista — 5 s = intervalo mínimo entre publicaciones, no frecuencia garantizada; sin tick ni timer compatible nunca se promete liveness continua; expiración 15 s fail-closed `SUSPENDED + UNKNOWN`; recovery exige nueva atestación física matching con las transiciones §6 congeladas; ninguna actualización de `ts` desde Echo/Bridge/Gateway/config; cero cambios de trading. Tests AC-37a…d (contractual+físico; PHYSICAL gated por Version con inyección §7.2a.5). Scanner §7.2a.5: ausencia de sitio de refresh deja de ser fail-closed en export. CASE B, encoding v1 y resto de gates intactos. Source mutations 0 (Echo y Forge). HEAD `acf996ad043f87d6bbe6ae7b6190d1eb801e908a` (contrato `28afc47faf72b70e67b141b39224b8674f98458b`; old `336c723b`); push FF. Estado `E06_PLANNING_READY_FOR_IMPLEMENTATION_REVIEW`.
- **2026-09-16 (TOP transport contract correction — encoding v1)** — Defecto: `GlobalVariableSet` no transporta `{program_name, chart_ref, magic}` ni int64 magic sin pérdida; `GlobalVariableTime` no es publicación. SPEC v1.2.1 cierra encoding fragmentado lossless, vigencia `ts`, correlación chart/cuenta, inyección estructural Forge (no implementada). CASE B intacto. Source mutations 0 (Echo y Forge). HEAD `336c723ba46a7c04a1a6cc4390c6d5a4f15b56d7` (contrato `662c0dcef9fb17a5308ddcb974eabb6074c748aa`; old `e8fba410`); push FF. Estado `E06_TRANSPORT_CONTRACT_READY_FOR_MANAGER_REVIEW`.
- **2026-09-16 (TOP planning correction #2 — Manager CASE B)** — Manager resolvió CASE C: zero-order exige `effective_magic` físicamente atestiguado por la instancia strategy EA (excepción C-3 §7.2a: bootstrap runtime identity attestation, sin signals/deals/coverage/métricas/lifecycle/telemetría/estado). Discovery físico READ ONLY: producer = exporter Forge `EchoForgeMT5Exporter.java` (stamp `MagicNumber` input por `EchoForgeRobustRunExporter`; verificado por `magic-readback`; sello F-04). Transporte: variables globales terminal → relay verbatim collector `reference_status`. Identidad: bytes cambian ⇒ nuevo `strategy_version_ref`; históricos intactos fail-closed. SPEC v1.2.0; caso AC-26a/b/c; bloque CASE-C removido; reconciliación preservada en VERIFICATION.md. AutoTrading B2 intacto; coverage hook sigue DEFER. Source mutations 0 (Echo y Forge). HEAD `e8fba410347f6c60d036f9d03b2d0b1946d53e28` (contrato `3d5a5d627f5ed66e48479e24f6b664c5a973899b`; old `349b6ac8`); push FF. Estado `E06_PLANNING_V1_2_READY_FOR_MANAGER_REVIEW`.
- **2026-09-16 (TOP authority reconciliation)** — CASE C. Live Authority §5 vs Fable C-3 no cierran si zero-order exige echo físico de magic. SPEC v1.1.0 sin bump; §7.3 KNOWN_EMPTY no es implementable. AutoTrading B2 intacto. C-3 DEFER intacto. HEAD `349b6ac8` (contrato `1c794d5a`; old `3e190d86`). Source delta `v3/` = 0. Estado `E06_PLANNING_BLOCKED — MANAGER_DECISION_REQUIRED`. *(Resuelto después por Manager CASE B; ver entrada superior.)*
- **2026-09-16 (TOP planning correction #1)** — v1.1.0 @ `3e190d86` (contrato `ef8a96f3`; old `9989f399`). Heartbeat/UnifiedBatch no son autoridad zero-order. Producer congelado: `reference_status` Echo collector. Magic = inventario; KNOWN_EMPTY no se fabrica. AutoTrading = capability (B2). C-3 DEFER SQX conservado. Source mutations 0. Estado `E06_PLANNING_CORRECTED_READY_FOR_MANAGER_REVIEW`.
- **2026-09-16 (TOP planning one-shot)** — SPEC/PLAN/TASKS/VERIFICATION v1.0.0 @ `9989f399`. Hipótesis accounts/policies solos refutada; `reference_bindings` + intent. O1/O3 applied. 064 reservada. 0 source. Estado `E06_PLANNING_READY_FOR_MANAGER_REVIEW`. Puente padre → Review.

## 🧭 Decisiones (ejecución, no semántica nueva)

- Hijo de implementación de E-06; ownership sigue en [[Echo — Live Platform V1]], no Integration.
- OBSERVING nunca se sintetiza desde SQL/ACK/config/heartbeat/UnifiedBatch.
- Apply 064 SHARED DEV es ops gated por 061, no NORMAL.
- PHYSICAL V1 exige producer `reference_status`; fake ≠ PHYSICAL. Terminal MT5 real GAP-ECHO-006 pendiente no se disfraza de PASS.
- Hook SQX de coverage **no** se abre (C-3 DEFER). La excepción §7.2a es identidad runtime mínima, registrada como decisión Manager posterior explícita (2026-09-16), no reescritura del freeze C-3.
- Zero-order magic = fail-closed congelado (CASE B): atestación runtime == pin o no hay OBSERVING.
- Transporte §7.2a = encoding v1 sobre GVs del mismo terminal; magic nunca viaja como `double`; una GV existente no es instancia viva.
- Liveness §7.2a.4 (erratum v1.2.2): refresh = `OnTimer` compatible preferido sin tocar `EventSetTimer` / `OnTick` oportunista (5 s = intervalo mínimo entre publicaciones); sin sitio ⇒ sin liveness continua prometida; la expiración de 15 s es la autoridad fail-closed.

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

- Hook EA SQX exportado de **coverage**: DEFER (C-3), no V1. La excepción §7.2a (identidad runtime mínima) NO es ese hook y no lo preimplementa.

### Motivos / principios

- Ingestion no inicia el reloj. Una fila SQL no observa.

### Memoria pública / interna

- **Memoria pública:** contratos enlazados + SPEC del repo.
- **Memoria interna:** continuidad en esta nota.
- **Motivo:** el padre conserva el roadmap; este hijo conserva HOW/GATES.
