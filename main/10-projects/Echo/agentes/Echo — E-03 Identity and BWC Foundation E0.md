---
type: project
schema_version: 1
owner: agent
root: false
status: closed
priority: P1
area: "[[Echo]]"
parent: "[[Echo — Live Platform V1]]"
sprint:
start: 2026-09-10
due:
progress: 100
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
updated: 2026-09-12
cssclasses:
  - wide
---

# Echo — E-03 Identity and BWC Foundation E0

%% Naming: Echo — E-03 Identity and BWC Foundation E0 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-03 Identity and BWC Foundation E0
> **Área:** [[Echo]] · **Estado:** closed · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-03 / E0. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES. **FINAL CLOSED 2026-09-12: CONTRACT_PASS certificado por el manager e integrado FF a `origin/master` @ `fac48051`.**

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Dejar persistence/protocol groundwork para StrategyVersion, PromotionRecord, wide IDs, magic int64, legacy dispatch, inmutabilidad, schema protection y BWC, sin decisiones críticas pendientes para NORMAL.

## 📊 Estado actual

- **CONTRACT_PASS / FINAL CLOSED (2026-09-12, ONE-SHOT FINAL INTEGRATION):** el manager certificó CONTRACT_PASS en `fac4805185eb586bb73c3df0c0ccc20d1377099c` sobre la rama `fix/e03-verification-correction-1`. Pre-integración verificado: `origin/master == c408a12fe36643129a2ae3c3dfa69727b593ba76` (SHA esperado exacto), `fac4805` existe, `git merge-base --is-ancestor origin/master fac4805` OK (FF puro, 6 commits `c408a12f..fac48051`). Integración por `git push origin fac4805…:master` sin merge commit, sin rebase, sin force (rango FF `c408a12f..fac48051`). Post-integración verificado: `origin/master == fac4805185eb586bb73c3df0c0ccc20d1377099c`, checkout local `master` en FF limpio (`git status` vacío), scope del delta de corrección = 6 archivos autorizados (`specs/FEAT-CROSS-IDENTITY-BWC-E0/VERIFICATION.md`, `v3/clients/mt4/EchoPersistence.mqh`, probes `E03_AddWithOrigin_V1RejectProbe.mq4` / `E03_AddWithOrigin_V1PhysicalProbe.mq5`, `v3/sdk/contracts/wire/canonicalize_test.go`, `v3/sdk/go.sum`); cero rutas E-04, Forge, `go.work`, `active_positions` o contracts source. Evidencia de certificación reside en `VERIFICATION.md` @ `fac4805` (T01–T23 PASS, AC-01…AC-18 PASS, S0 FULL PASS, PG harness PASS, MT5 PHYSICAL PASS artifact `e03_mt5_correction_map.bin` SHA256 `FA7A0A949DAE054A618AD9D144C6B828145191B8B902A016CAC6892D4367D007`, MT4 N/A por decisión del manager). E-04 y Forge intactos. Condición de cierre de E-04 (`E03_CONTRACT_PASS_REQUIRED_FOR_INTEGRATION`) queda satisfecha; transición de E-04 es trabajo propio de ese proyecto, no de éste.
- **CORRECTION COMPLETE / READY FOR MANAGER FINAL REVIEW (2026-09-12):** sobre baseline `5c126e5c16a17b14d57b062907d4ccacdc7143a9`, se corrigió mínimamente la expectativa stale de `encoding/json` para U+FFFD. S0 FULL PASS (incluye `GOWORK=off`, corpus, race/vet y resolución `contracts v0.0.0 => ./contracts`); T01–T23 y AC-01…AC-18 PASS; harness PostgreSQL local/efímero PASS; verificación MCP PostgreSQL real no destructiva PASS (pre-061, `active_positions.strategy_id` intacto); MT5 físico PASS en tester frozen 6182 con ejecución de `OnInit` y artifact v1 verificable. MT4 `N/A — OUT OF SCOPE`. Branch `fix/e03-verification-correction-1`, pendiente sólo revisión final del manager.
- **VERIFIER INDEPENDIENTE 2026-09-11 (FAIL):** ejecución nueva y aislada sobre `c408a12fe36643129a2ae3c3dfa69727b593ba76` confirmó `origin/master` exacto, parent `233ec89ce3868b414d63856c683a1fdd469c58bb`, worktree limpio y scope sin rutas prohibidas. MCP Aranea SSH fue descubierto y usado: compilación real MT4/MetaEditor 5.0.0.2418 y MT5/MetaEditor 5.0.0.6090 produjo 0 errores, pero los testers no devolvieron artefactos runtime nuevos; no hubo PostgreSQL MCP ni cluster descartable disponible. Razones materiales de `FAIL`: `v3/clients/mt4/EchoPersistence.mqh` no aplica `IsUnsupportedFile()` en `AddWithOrigin` y puede reinterpretar/escribir sobre V1; 061/`21_revoke.sql` omiten roles ausentes pese al hard gate de `mcp_echo_dev_ro`; `go test` bridge limpio falla por el módulo `contracts`/go-sqlmock y baseline bridge pasa. No se modificó product source, no se hizo commit/push ni se actualizó `VERIFICATION.md`; no se marca closed ni se inicia E-04.
- **NORMAL 2026-09-11 (implementation complete / verification pending):** baseline `233ec89ce3868b414d63856c683a1fdd469c58bb` validado; rescue `origin/rescue/e03-uncommitted-20260911-175842` (`ce9ee11d`, parent == baseline) inspeccionado, clasificado scope-correct y aplicado con `cherry-pick -n` sin commit sobre worktree limpio `/tmp/echo-e03-daedalus-4woBaW` (TASKS state-only excluido). Commit canónico único `c408a12fe36643129a2ae3c3dfa69727b593ba76` (`feat(identity): implement E-03 identity and BWC foundation`, parent `233ec89c`) pusheado FF a `origin/master` tras pre-push race check. T01–T23 `[x]` revalidados en sesión; AC-01…AC-18 PASS (AC-14 vía gate dedicado `TestNoEchoMagicAllocator` PASS; el skip del subtest del pack es by-design). **MT4 PHYSICAL cerrado en Windows nativo** (host Aranea `mt5-kronos`, Windows 10 IoT Enterprise LTSC 2024 x64; MT4 Darwinex terminal build 4.0.0.1470 con MetaEditor 5.0.0.2418; instancia dedicada `C:\MT4\e03-evidence` copia de `reference_001` en `/portable`, sin tocar agents existentes; transferencias por HTTP con SHA256 verificado ambos lados): **T01** `sizeof(TradeMapRecord)=144` packed (EA MQL4 real sobre `EchoPersistence.mqh` productivo), offsets 0/4/44/52/56/120/124/132/140 derivados por markers (coinciden con `LayoutV0MT4` frozen; sin corrección de decoder); **T02** fixture `v3/clients/mt4/testdata/trademap/v0.bin` 432 bytes = 3×144 por `FileWriteStruct` real, sha256 `13cb5e6216c507913fd6065c59bafae732f95389f9b949ea6ef989b1f0fa6ba8`, ejecutado como EA sobre chart EURUSD M1 (ini `[Tester]` relativo consumido; `metaeditor /compile` 0 errors); **T07** compile productivo con MetaEditor 4 real: el compile físico atrapó un bug real del candidate (`SlaveCommandJournal::Add` invocaba `IsUnsupportedFile` indefinido en su scope, error 168) — corregido mecánicamente añadiendo el guard fail-closed v1-cookie propio de esa clase sobre su archivo (mqh sha256 `3e4d331ff89c1494ab7f47d7c474a4d387b8b3abce93f17f7dd7a9855bca8e0a`); ticket/magic `int` frozen, v0-only (sin writes v1), canonical >64 rechazado sin truncar. **T03** cross-check Go PASS con fixture físico MT4 (`TestDecodeV0_PhysicalFixtureMT4`). **T06/MT5**: fixtures revalidados por hash (`v0.bin` 444=3×148 `d3496bfa…63dea9e`; `v1.bin` `b0e03e31…06aa3a4c`) + recompile productivo del mqh MT5 (`d5a6669b…`) en MetaEditor 5 nativo Windows (6182): 0 errors, 1 warning preexistente benigno. **PG real 17.5 local** (cluster portátil descartable port 5561, DBs `e03_harness`/`e03_integration`): harness `tests/identity_bwc/run.sh` PASS íntegro (rebuild 060 → interrupt → up → idempotencia → typmods → FK tuple INSERT directo → write-once → REVOKE → down fail-closed umbral 64/magic int32 → re-up); **T21 REVOKE PASS con roles productivos reales**: `echo_user` (app role, migration 048) y `mcp_echo_dev_ro` (049) creados pre-061 con default privileges DML amplios, REVOKE de 061 los strippea, `21_revoke.sql` ejecuta asserts con roles presentes y UPDATE vivo como `echo_user` → `permission denied` (la sesión previa lo omitió por roles ausentes — ya no). **T14** cerrado reusando corpus S0 autorizado `contracts/testdata/v1/G21/g21-unsafe-number-token.json` (sin fixture nuevo fuera de scope; la copia local rechazada fue eliminada del candidate). S0 edge PASS (`GOWORK=off` → `v0.0.0 => ./contracts`; `go.sum`/`go.work` intactos). Race acotado PASS (eapersist, postgres E-03, bridge `Identity|Pipe` y paquete bridge completo `-race` en 1.8s con timeout 400s — el hang previo §21 no reproduce; sin skip/masking). Non-gates preexistentes demostrados contra baseline probe: `TestScratch_QueryKafka/QueryKafkaCloseResults` (infra externa), gap `go-sqlmock` en `go.sum` con `GOWORK=off` (falla idéntico en baseline), gofmt `v3/sdk/domain/trade_journal.go` (preexistente). Rescue NO eliminado (provenance hasta cierre E-03). Pendiente: **Verifier independiente** (CONTRACT_PASS); no verified, no closed.
- **NORMAL 2026-09-10 (fresh finalization attempt, BLOCKED):** baseline `233ec89ce3868b414d63856c683a1fdd469c58bb` y candidate HEAD `576bf1f49f116826a8141126fbb520b80a7d1a3c` revalidados; candidate inspeccionado y dejado intacto; worktree final limpio creado y sólo deltas productivos autorizados trasladados, sin importar TASKS state-only. MT5 físico revalidado por hashes (`v0.bin` 444 bytes = 3×148; `v1.bin` 343 bytes), codec Go PASS y S0 `GOWORK=off` PASS (`v0.0.0 => ./contracts`, importer `contracts.StrategyVersionRef`). PG real SQL PASS para up/idempotencia/rollback/typmods/FK directos/write-once/down; el assertion REVOKE quedó omitido porque `mcp_echo_dev_ro` no existe en la base. Blockers exactos: no hay Windows + MetaEditor 4 funcional en esta sesión; candidate carece de `mt4/testdata/trademap/*`, por lo que T01/T02/T07 y certificación física MT4 no pueden PASS; además candidate contiene `v3/sdk/postgres/testdata/identity_bwc_g21_unsafe_number.json` fuera de Allowed Files y al rechazarlo falla el test final que lo referencia. No commit/push; estado permanece `active / blocked partial`, abierto para una sesión con Windows/MT4 y resolución de scope.
- **NORMAL 2026-09-10 (sesión E-03, verdict BLOCKED parcial):** implementación T01–T23 realizada en worktree temporal `/tmp/echo-e03-normal-hy8uJD` (baseline `576bf1f4`, dirty, **sin commit**: §32 prohíbe commit con gates PHYSICAL abiertos). Gates PASS: migración 061 up/down/up en PG 16 real (harness `tests/identity_bwc/run.sh`: interrupt/idempotencia/typmods/FK identidad por INSERT directo/write-once/revoke/down fail-closed umbral 64), repos identity/version/promotion/aliases INTEGRATION PASS, wire pipe + ticket int64 PASS, no-allocator PASS, cert pack AC-01…AC-18 PASS con skips físicos. **PHYSICAL MT5 completo**: sizeof=148 + offsets medidos en MetaEditor real (build 6190/Wine 9), fixture `v0.bin` (444=3×148) por `FileWriteStruct`, fixture `v1.bin` escrito por el EA + conversión v0→v1 validada contra codec Go (el runtime físico atrapó 2 bugs reales del writer MQL). **PHYSICAL MT4 bloqueado**: setup MT4 rechazado por MetaQuotes de forma persistente ("something went wrong") — T01/T02/T07(compile) quedan abiertos. Desviación de scope documentada: `v3/sdk/go.mod` require+replace del módulo S0 `contracts` (exigido por T12 "consumir S0, no copiar receta"). FAIL preexistentes no-gate: `TestScratch_QueryKafka*` (§27). Reintentar MT4 físico desde otro entorno (Windows/MetaQuotes habilitado) para cerrar y commitir.
- **TOP PLANNING READY_FOR_MANAGER_REVIEW (2026-09-10 S0 module consumption):** parent `576bf1f49f116826a8141126fbb520b80a7d1a3c`. Correction SHA `233ec89ce3868b414d63856c683a1fdd469c58bb` (FF `origin/master`). Edge certificado: `require github.com/xKoRx/echo/v3/sdk/contracts v0.0.0` + `replace => ./contracts` en `v3/sdk/go.mod`. `go.sum` no delta. `go.work` intocado. `GOWORK=off` resolution PASS. Sin source Go/SQL en este TOP. Candidate previo no commiteado. MT4 PHYSICAL sigue blocker. Implementación todavía NO committed/certified.
- **TOP PLANNING READY_FOR_MANAGER_REVIEW (2026-09-10 relational integrity):** SPEC v1.1.1 cierra UNIQUE + FK compuestos Mapping→Version→Promotion. Parent `45a59fca1058203df6baf20c3cfe1d000251159d`. Correction SHA `576bf1f49f116826a8141126fbb520b80a7d1a3c` (FF `origin/master`). Sin source Go/SQL en TOP. No implementation complete. No closed.
- **E-01:** certified S0; no reabrir.
- **Contrato WHAT:** `specs/FEAT-CROSS-IDENTITY-BWC-E0/SPEC.md` v1.1.1.
- **Checklist:** `specs/FEAT-CROSS-IDENTITY-BWC-E0/TASKS.md` (T01–T23; ACs AC-01…AC-18). T08/T10/T12/T13 cierran constraints y INSERT SQL directo.
- **PLAN.md local Echo:** puente de gobernanza; no copia esta nota.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `master` (fase E-03) | `c22fe218127c7e97fb40951ddcafc13d80ede152` | [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] §§2–3, 9 + SDK Canonical V1 (S0 certified) | `specs/FEAT-CROSS-IDENTITY-BWC-E0/SPEC.md` v1.1.1 @ `233ec89ce3868b414d63856c683a1fdd469c58bb` | CONTRACT_PASS / FINAL CLOSED (`fac4805185eb586bb73c3df0c0ccc20d1377099c` en `origin/master`) |

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

Exacto PLAN.md. Incluye `v3/sdk/go.mod` (edge S0). Prohibido `v3/sdk/go.sum`, root `go.work`, contracts S0 source, Gateway ingestion, Symphony, allocator, tests ajenos sin `TEST_CHANGE_REQUEST`.

## 📦 Work packages

- **WP-A Layout EA** T01–T07. v0 medido; v1 SPEC §10.6 (cookie 9, LE, CRC IEEE, framing); MT4 no int64.
- **WP-B Schema 061** T08–T10, T18, T19, T21. Widen V2_CANONICAL techo 64; no `active_positions`; down umbral 64; UNIQUE identity tuple + FK compuestos; `15_identity_tuple_fk.sql` INSERT directo.
- **WP-C Stores** T11–T15, T22. Mapping PK `(ns, canonical)` + UNIQUE identity tuple; Version PK `(ns, version_ref)` + FK 3-col; Promotion FK 4-col. Repository no es la única autoridad.
- **WP-D Wire** T16–T17, T14. String decimal; ticket 1..MaxInt64; G20/G21.
- **WP-E Cert** T20, T23. No allocator; AC-01…AC-18.

## TOP / NORMAL boundaries

- TOP: SPEC, esta nota, TASKS, PLAN puente, linkage padre. No source Go/SQL.
- NORMAL: T01–T23 mecánicamente. No elegir semántica de identidad, política de migración, ni “arreglar” S0.
- GOD: NONE.

## Migrations

**061** obligatoria. Motor golang-migrate. Transacción única + backup de relaciones modificadas (no `active_positions`). Interrupt = ROLLBACK. Down aborta si `octet_length > 64` en columnas ex-64 o magic >int32. No umbral 50. Mock SQL ≠ PASS.

## Dependency delta

Parent SDK declara consumo in-repo de S0: `require github.com/xKoRx/echo/v3/sdk/contracts v0.0.0` + `replace github.com/xKoRx/echo/v3/sdk/contracts => ./contracts` en `v3/sdk/go.mod`. No es tag/release ni pin Forge. `go.sum` no se toca. `go.work` no se modifica y no es autoridad. `eapersist` es paquete nuevo bajo `v3/sdk`. No pin de terceros. Stdlib para codec.

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

```bash
# S0 nested-module consumption (GOWORK=off)
cd v3/sdk
GOWORK=off go list -m all
GOWORK=off go test ./postgres
GOWORK=off go list -m github.com/xKoRx/echo/v3/sdk/contracts
```

El `go list -m` de contracts debe resolver `v0.0.0 => ./contracts`. `go list -m all` y `go test ./postgres` con `GOWORK=off` pueden fallar únicamente por el hueco preexistente `go-sqlmock` `/go.mod` hash en `go.sum`; no rellenar `go.sum` en E-03.

## Baseline tests (registrados, no ampliar)

Mismos FAIL de infra que E-01 (etcd/Kafka/Jaeger). No “arreglarlos” en E-03.

## Release / pin expectations

Manager acepta planning. NORMAL implementa. Verifier independiente escribe `VERIFICATION.md`. No tag. Push de implementación sólo si el manager lo pide; este TOP sí publica planning FF a `master`.

## Blockers

No hay blocker vigente de E-03. MT4 queda fuera de alcance de certificación por decisión del manager. Graphify stale y autenticación MCP de Agents OS no afectan este cierre; el vault se actualizó por filesystem.

## Handoff requirements

FINAL CLOSED ejecutado 2026-09-12 por orden one-shot del manager: CONTRACT_PASS certificado en `fac48051` e integrado FF a `origin/master` (sin merge commit, rebase ni force); verificación pre/post y evidencia en `📊 Estado actual` y `📆 Bitácora`.

## Closure conditions

T01–T23 `[x]`; gates T23 PASS; allowed files respetados; AC-01…AC-18 cubiertos; no allocator; layouts v0 addressable; 061 idempotente; FKs de identidad DB-enforced; certificación en `VERIFICATION.md` (fuera de este TOP).

## 🧩 Subproyectos

_No aplica — hijo de implementación de E-03; no crea Integration ni más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-CROSS-IDENTITY-BWC-E0/TASKS.md`. Aquí sólo work packages.
> - [x] WP-A Layout EA v0/v1 + MT4 legacy #owner/agent #type/dev #area/echo
> - [x] WP-B Schema 061 widen/protection/migration gates #owner/agent #type/dev #area/echo
> - [x] WP-C Stores identity/version/promotion/aliases #owner/agent #type/dev #area/echo
> - [x] WP-D Wire string magic + ticket 1..MaxInt64 #owner/agent #type/dev #area/echo
> - [x] WP-E Certification AC-01…AC-18 + no allocator #owner/agent #type/dev #area/echo

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

- **2026-09-12 (ONE-SHOT FINAL INTEGRATION, CONTRACT_PASS / FINAL CLOSED):** fetch + verificación de `c408a12f` (origin/master exacto) y `fac48051` (existe, descendiente FF: `merge-base --is-ancestor` OK; 6 commits de corrección, rama `fix/e03-verification-correction-1`). Push FF `c408a12f..fac48051` a `master` sin merge commit/rebase/force; post: `origin/master == fac4805185eb586bb73c3df0c0ccc20d1377099c`, checkout local limpio, scope de 6 archivos de corrección sin E-04/Forge. `status: closed`, `progress: 100`. Tarea puente queda en `[r]` en el padre (cierre de puente es decisión humana, precedente E-01). E-04 y Forge no tocados; su gate `E03_CONTRACT_PASS_REQUIRED_FOR_INTEGRATION` queda satisfecho.
- **2026-09-12 (ONE-SHOT CORRECTION COMPLETE):** baseline `5c126e5c` verificado sin merge/rebase; se resolvió el finding S0 real de expectativa stale frente a `encoding/json` Go 1.27. S0 FULL PASS, T01–T23/AC-01…AC-18 PASS, harness PostgreSQL efímero PASS, PostgreSQL MCP real no destructivo PASS y MT5 PHYSICAL PASS en build/tester 6182 con artifact `e03_mt5_correction_map.bin` (207 bytes, SHA256 `FA7A0A949DAE054A618AD9D144C6B828145191B8B902A016CAC6892D4367D007`). MT4 N/A por decisión del manager. Branch `fix/e03-verification-correction-1`; estado `review`, `progress: 100`, no FINAL CLOSED.
- **2026-09-11 (VERIFIER INDEPENDIENTE, FAIL):** exact SHA `c408a12f` re-audit completed with MCP-first discovery and fresh worktrees. Source FAILs: MT4 V1 fail-closed missing from `AddWithOrigin`; REVOKE harness skips missing roles; bridge clean test setup is not baseline-identical. MT4/MT5 runtime artifact and disposable PostgreSQL gates remain individually `BLOCKED` after documented MCP attempts. No product fix, certification commit, push, or E-04 transition.
- **2026-09-11 (TOP E-04 interlock)** — E-04 planning autoriza **development** paralelo sobre `c408a12f` (`feature/e04-forge-ingestion-e1`) mientras este proyecto sigue `IMPLEMENTATION CLOSED / VERIFICATION PENDING`. E-04 **no** se integra ni declara CLOSED hasta CONTRACT_PASS de E-03. Este proyecto no se marca closed. `origin/master` no se mueve desde aquí.
- **2026-09-10 (TOP correction)** — Gaps A–D cerrados en SPEC v1.1.0. Cookie `ECHO-TMAP` = 9 bytes; v1 §10.6 LE+CRC-32/IEEE; ticket Option 2 `1..MaxInt64`; Version PK `(registry_namespace, version_ref)` + FK mapping; `active_positions.strategy_id` DEFERRED. SHA `45a59fca1058203df6baf20c3cfe1d000251159d`. Estado `READY_FOR_MANAGER_REVIEW`. No NORMAL.
- **2026-09-10 (TOP relational integrity)** — CHECK cross-table reemplazado por UNIQUE + FK compuestos. Mapping UNIQUE identity tuple; Version FK 3-col + UNIQUE 4-col; Promotion FK Version 4-col + FK mapping 3-col. T08/T10/T12/T13. SHA `576bf1f49f116826a8141126fbb520b80a7d1a3c`. Estado `READY_FOR_MANAGER_REVIEW`. No implementation complete. No closed. No NORMAL.
- **2026-09-10 (NORMAL, BLOCKED parcial)** — One-shot NORMAL sobre worktree limpio `576bf1f4` (`/tmp/echo-e03-normal-hy8uJD`, sin commit). Implementado: 061 up/down (backup §7.1, widen 13 columnas + override bigint, tablas §6 con UNIQUE/FK compuestos exactos, triggers write-once, REVOKE, vistas recreadas sin typmod), harness SQL `tests/identity_bwc/` PASS íntegro en PG 16.15 real, repos identity/version/promotion/aliases write-once con IDENTITY_CONFLICT/CONTRACT_CONFLICT (tests INTEGRATION PASS contra PG), pipe `echo-identity-wire.v1` dual encode + `ReferenceTicket int64` (1..MaxInt64), T18 width gate, T20 no-allocator, T23 cert pack. PHYSICAL MT5: MetaEditor real compiló la .mqh reescrita (0 errores tras corregir 52 del primer intento), sizeof=148 sin padding, fixtures `v0.bin`/`v1.bin` + conversión validados contra codec Go. PHYSICAL MT4: setup rechazado por MetaQuotes (persistente) → T01/T02/T07-compile abiertos → BLOCKED, sin commit por §32. Desviación scope: `v3/sdk/go.mod` (contracts require+replace, exigido T12). Tooling creado: PG16 local (brew), colima VM + Wine + MetaTrader 5 con cuenta demo sintética (login 112457778) para evidencia MQL headless.
- **2026-09-10 (TOP S0 module consumption)** — Edge in-repo certificado: `require github.com/xKoRx/echo/v3/sdk/contracts v0.0.0` + `replace => ./contracts`. `v0.0.0` válido. `go.sum` no delta. `go.work` intocado. `GOWORK=off` resolution PASS. Allowed Files suma `v3/sdk/go.mod`; T12 actualizado. SHA `233ec89ce3868b414d63856c683a1fdd469c58bb`. Estado `active / blocked partial`. Candidate `/tmp/echo-e03-normal-hy8uJD` no tocado. Implementación no committed. MT4 PHYSICAL sigue blocker. No NORMAL.

## 🧭 Decisiones (ejecución, no semántica nueva)

- Hijo de implementación de E-03; ownership sigue en [[Echo — Live Platform V1]], no Integration.
- `v3/sdk/contracts` es autoridad de recetas, no de schema PG. Consumo in-repo E-03: `require v0.0.0` + `replace => ./contracts` en `v3/sdk/go.mod`; no tag; no `go.work` como autoridad; no `go.sum` por este edge.
- Cookie v1 `ECHO-TMAP` **9 bytes** (`45 43 48 4F 2D 54 4D 41 50`); header 32; CRC-32/IEEE LE sobre Header\|\|Records; v0 = ausencia de cookie + múltiplo de sizeof medido.
- Ticket Echo: `1..MaxInt64`; no full MT5 `ulong`; PG `bigint`; Go `int64`.
- Mapping PK `(registry_namespace, canonical_strategy_id)`; UNIQUEs `(ns, strategy_ref)`, `(ns, magic)`, `uq_strategy_identity_mappings_identity_tuple`. Version PK `(registry_namespace, version_ref)`; FK `fk_strategy_versions_identity_tuple`; UNIQUE `uq_strategy_versions_identity_tuple`. Promotion FK `fk_promotion_records_version_identity` + FK mapping identity. `StrategyVersionRef` S0 sin namespace. Repository no es la única autoridad.
- `active_positions.strategy_id varchar(50)` DEFERRED a E-06.
- SQL eager; EA lazy-on-open con backup.
- Down 061 fail-closed si `octet_length > 64` en columnas ensanchadas desde 64.

## 🔗 Docs / Links

- [[Echo — Live Platform V1]]
- [[Echo — E-04 Forge Ingestion E1]]
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
