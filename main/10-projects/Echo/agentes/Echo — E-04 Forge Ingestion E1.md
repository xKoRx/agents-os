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
progress: 95
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
updated: 2026-09-12
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

- **NORMAL CORRECTION COMPLETE — TEST-ONLY (2026-09-12).** La corrección del Source Review quedó aplicada y pusheada FF a `origin/feature/e04-forge-ingestion-e1` en `4aef2958ea444002b3ddb2d53f909f42b0c79921`, con base exacta `bfc0bc4b5db94c8d5c18e146b4ba14d75464cf93`. Sólo se modificaron tests y evidencia (`TASKS.md`, `VERIFICATION.md`, tests SDK/gateway); no hubo cambios productivos, E-03/S0, migrations ni Symphony. AC-10 ahora usa magic no conflictivo `2147483649`, alcanza el INSERT de promotion y prueba SQLSTATE `23505` más ausencia física de mapping, version y promotion. Se añadieron acceptance+copy/integrity de `dependency_artifacts`, conflicto de `strategy_ref` y `assigned_at` inválido contractual. Gates: identity_bwc PG17.5 PASS; E-03 34 PASS; SDK/gateway relevantes serializados con `-race` PASS; PHYSICAL HTTP+PG PASS; coverage exacto svc 82.2% / artifact 76.7% / handler 92.0% / auth 100%; SOURCE/contracts diff/migrations PASS. La ejecución combinada de paquetes contra una misma DB tuvo contaminación por TRUNCATE concurrente y se corrigió reejecutando serialmente. La suite completa de contracts conserva un fallo preexistente en `wire` por expectativa de `\\ufffd` vs `�` bajo Go 1.25.5. T21/AC-37 sigue PENDING; no verifier, no merge, no READY/CLOSED.
- **MANAGER SOURCE REVIEW DONE — CORRECTION (test-only) (2026-09-12).** Source review one-shot @ `bfc0bc4b`: git/ancestry/source/auth/failure-mapping/non-effects/replay/concurrency **sin defectos materiales**; gates reproducidos por el reviewer (identity_bwc PASS, E-03 34 PASS, E-04 `-race` 69 PASS/0 skip contra PG 17.5 descartable; coverage exacto: svc 77.6% / artifact 76.7% / handler 92% / auth 100%). Clasificaciones: `ARTIFACT_FIXTURE_OK` (preimages negativas verificadas por escaneo echo+symphony+sdk; sólo G10 tiene bytes; separación synthetic/raw permitida por SPEC §4.1; byte-authority sigue para Manager), `TRANSACTION_ADAPTER_OK`, `COVERAGE_CORRECTION_REQUIRED` acotado. **Correction scope (test-only, sin tocar source productivo):** (1) `TestIngest_RollbackOnPromotionFailure` usa magic 2147483648 duplicado y sale por IDENTITY_CONFLICT de pre-lookup sin llegar al INSERT de promotion — el rollback de transacción de AC-10 no está demostrado (verificado con coverage focalizado); dar magic distinto al segundo manifest; (2) añadir test de `dependency_artifacts` (SPEC §8) en accept e integridad; (3) cubrir IDENTITY_CONFLICT por `strategy_ref` ajeno y `assigned_at` no-RFC3339 (ramas alcanzables sin test). Tras correction: re-run gates PLAN + actualizar VERIFICATION.md (AC-10 y AC-36), recién ahí Independent Verifier. `FORGE_GOLDEN_FIXTURE_PENDING` intacto (T21/AC-37 PENDING); `E03_CONTRACT_PASS_REQUIRED_FOR_INTEGRATION=NOT_MET`; NO READY_FOR_INTEGRATION; NO CLOSED; master intacto `c408a12f`.
- **IMPLEMENTATION READY FOR MANAGER SOURCE REVIEW (2026-09-12).** NORMAL completó T01–T20 `[x]` (T21 `[ ]`): 3 commits (`03b20abd` ingestion core, `fc590b31` gateway boundary, `bfc0bc4b` SDD evidence) pusheados FF a `origin/feature/e04-forge-ingestion-e1` tras race gate (`6beac29f` ancestro exacto; master `c408a12f` intacto). Gates: MIGRATION (identity_bwc PASS, 061 diff 0), E-03 regression 34 PASS (DBTX mecánico, sin editar tests), CONTRACT/PG REAL/PHYSICAL HTTP+PG/CONCURRENCY `-race` PASS (PG 17.5 local port 5561), SOURCE greps vacíos, contracts diff 0. AC-01…AC-36 cubiertos (detalle en VERIFICATION.md); AC-37/T21 **PENDING** (`FORGE_GOLDEN_FIXTURE_PENDING=YES`). Coverage: gateway 92%, sdk ingestion ~77% (delta documentado: plumbing defensivo + fault-injection). **Gap registrado para Manager:** el corpus S0 no embarca los bytes de artefacto que sus refs declaran (sólo G10 trae bytes; shas de G01 sin preimage) → los AC de aceptación se demostraron con builders sintéticos S0-API autorizados (SPEC §4.1) + corpus literal en rechazos y matriz G10; `TestCorpus_G01_ArtifactPreimages` documenta el 422 honesto. `E03_CONTRACT_PASS_REQUIRED_FOR_INTEGRATION=NOT_MET`. NO READY_FOR_INTEGRATION. NO CLOSED.
- **NORMAL IMPLEMENTING (2026-09-12).** Manager aprobó el planning → NORMAL ejecuta T01–T20 mecánicamente contra TASKS/PLAN/SPEC v1.0.1. Worktree de ejecución `/tmp/echo-e04-normal-impl`, branch local `impl/e04-forge-ingestion-e1-normal` anclada exactamente a `origin/feature/e04-forge-ingestion-e1` @ `6beac29f` (push final FF a la feature; jamás master). `FORGE_GOLDEN_FIXTURE_PENDING` intacto; T21 fail-closed; E-03 no tocado (`IMPLEMENTATION CLOSED / CONTRACT_PASS NOT ESTABLISHED`); no Integration; no E-04 CLOSED. PG real: harness local descartable PG 17.5 port 5561 (`e04_ingestion`), `tests/identity_bwc/run.sh` PASS en el branch (061 intacto) y suite E-03 `Identity|Version|Promotion|Magic|Alias` PASS baseline.
- **TOP PLANNING READY FOR MANAGER REVIEW (2026-09-11, corrección T17).** TASKS T17 alineado a `Deliver(ctx, ns, *HandoffManifestV1, payloadDigest) (PromotionRecord, httpStatus, error)` @ `6beac29f`. SPEC v1.0.1 §6.1 intacto. `payloadDigest` no es segunda autoridad HTTP. Gates 1.0.1 intactos (`FORGE_GOLDEN_FIXTURE_PENDING`; CROSS_LANE development no espera E-03 CONTRACT_PASS). No implementing. No CLOSED.
- **Development MAY START** (T01–T20) en paralelo con verification E-03. **CROSS_LANE GOLDEN** puede correr antes de E-03 CONTRACT_PASS **si** existiera fixture Forge auténtica; hoy pending. **Integration/merge/close NO:** gate `E03_CONTRACT_PASS_REQUIRED_FOR_INTEGRATION`.
- E-03 permanece `IMPLEMENTATION CLOSED / CONTRACT_PASS NOT ESTABLISHED` @ `c408a12fe36643129a2ae3c3dfa69727b593ba76`. No se marca E-03 closed/PASS/FAIL. No se marca E-04 implementing. No se marca Forge join closed.
- Baseline de development: `origin/master` = `c408a12f` (parent `233ec89c`). Branch `feature/e04-forge-ingestion-e1` @ `6beac29f9b6daa5a3d935b7074de3bb2b2098014` (parent `c8e68538`). Push a master prohibido.
- Contrato WHAT: `specs/FEAT-FORGE-INGESTION-E1/SPEC.md` v1.0.1. TASKS T01–T20 NORMAL; T21 golden (blocked). AC-01…AC-37.
- S0 certified READ ONLY @ `91671f6f`. Stores E-03 se consumen, no se rediseñan.
- Búsqueda física Symphony: golden Forge **NOT FOUND**. `echo-handoff` testdata = copia S0. `ea8be76` no es authority de master. Dependency `FORGE_GOLDEN_FIXTURE_PENDING`.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e04-forge-ingestion-e1` | `c408a12fe36643129a2ae3c3dfa69727b593ba76` | [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] §4 + [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] (join) | `specs/FEAT-FORGE-INGESTION-E1/SPEC.md` v1.0.1 @ `c8e68538`; TASKS T17 @ `6beac29f9b6daa5a3d935b7074de3bb2b2098014` | TOP READY_FOR_MANAGER_REVIEW · NORMAL no autorizado |

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

Ver TASKS.md. Paralelo inicial: T01 DBTX ∥ T02 artifacts ∥ T09 auth. T03 service. T10–T11 HTTP. T12–T15 gates. T20 cert. T21 CROSS_LANE GOLDEN blocked by `FORGE_GOLDEN_FIXTURE_PENDING`.

No ejecutar E-02/E-05/E-06/F-05 aquí. No alterar E-03 para acomodar semántica.

## Allowed scope NORMAL

Exacto PLAN.md. Development en feature branch desde `c408a12f`. Prohibido `origin/master` push/merge. Prohibido `v3/sdk/contracts/**`. Prohibido 061/062 identidad. Prohibido allocator/activation.

## 📦 Work packages

- **WP-A Stores adapter** T01 (AC-33). DBTX.
- **WP-B Ingestion core** T02–T08. Service + artifacts + mapping/version/promotion tx + non-effects.
- **WP-C Gateway HTTP** T09–T13, T16. Auth, POST, GET, timeout, concurrency.
- **WP-D Corpus / SQL** T14–T15, T17. Synthetic S0 HTTP + SQL-direct + HandoffIngress test client. No es CROSS_LANE GOLDEN.
- **WP-E Cert** T18–T20. SOURCE greps, coverage, governance interlock.
- **WP-F Golden** T21. Authentic Forge fixture. Pending. No bloquea NORMAL.

## TOP / NORMAL boundaries

- TOP: SPEC, esta nota, TASKS, PLAN puente, linkage padres, gobernanza de paralelismo y golden. No source Go/SQL/HTTP productivo.
- NORMAL: T01–T20 mecánicamente. T21 fail-closed mientras `FORGE_GOLDEN_FIXTURE_PENDING`. No elegir URL, codes, recetas S0, ni “arreglar” E-03/S0, ni inventar fixture Forge.
- GOD: NONE.

## Migrations

**Ninguna.** 061 no-touch. Mock SQL ≠ PASS.

## Dependency delta

```text
development dependency:     E-03 IMPLEMENTATION CLOSED @ c408a12f  (satisfecha)
golden dependency:          FORGE_GOLDEN_FIXTURE_PENDING          (NO satisfecha; no bloquea NORMAL)
integration dependency:     E-03 CONTRACT_PASS                    (NO satisfecha; merge/close only)
```

Corpus S0 / fakeconsumer / builders = CONTRACT/SYNTHETIC. CROSS_LANE GOLDEN exige fixture Forge auténtica; hoy pending. CROSS_LANE development **no** espera E-03 CONTRACT_PASS.

## Compatibility strategy

HTTP nuevo. Stores E-03 write-once. Webhooks Gateway intactos. Forge CONTRACT permanece en fakeconsumer. Echo SYNTHETIC usa S0. CROSS_LANE GOLDEN espera fixture auténtica, no E-03 CONTRACT_PASS.

## Test strategy

AC-01…AC-37 ↔ TASKS. Corpus G01–G25/G31/G35 = SYNTHETIC/CONTRACT. PG real obligatorio para CONTRACT/PG/PHYSICAL HTTP+PG. PHYSICAL E-04 = PG+HTTP+filesystem, no MetaTrader. CROSS_LANE GOLDEN = T21/AC-37.

## Certification gates (NORMAL)

Ver PLAN.md. Clases: SOURCE, CONTRACT, PG REAL, PHYSICAL HTTP+PG, SYNTHETIC CONTRACT INTEGRATION, MIGRATION=N/A, CROSS_LANE GOLDEN (`FORGE_GOLDEN_FIXTURE_PENDING`), GOVERNANCE (`E03_CONTRACT_PASS_REQUIRED_FOR_INTEGRATION`), CONTROLLED INTEGRATION (no esta fase).

## Branch strategy

- Crear/usar `feature/e04-forge-ingestion-e1` desde **exactamente** `c408a12f`.
- Worktree separado. Fetch OK. Feature push OK.
- Master push prohibido. Merge a master prohibido.
- Rebase sobre master cambiado por verification E-03 prohibido hasta manager review de incorporación.
- Tras E-03 CONTRACT_PASS: incorporar base, demostrar ancestry, rerun gates, entonces integrate review.

Si Verifier E-03 FAIL: `BLOCKED_PENDING_E03_CORRECTION`.

## Blockers

Ninguno para **development** T01–T20. `FORGE_GOLDEN_FIXTURE_PENDING` bloquea T21 / CROSS_LANE GOLDEN PASS / Verifier golden / READY_FOR_INTEGRATION. Integrate/merge/CLOSED bloqueado por E-03 CONTRACT_PASS. F-04 PHYSICAL/CC no bloquea E-04 CONTRACT.

## Handoff requirements

Manager aprueba planning → NORMAL implementa T01–T20 en el worktree de esta branch. No usar el checkout `master` local behind. No cerrar E-03. No declarar join Forge CLOSED.

## Closure conditions

T01–T20 `[x]`; AC-01…AC-36; allowed files; 061 intacto; non-effects; E-03 identity tests PASS. READY_FOR_INTEGRATION exige además AC-37/T21 (hoy pending). Merge/CLOSED exige `E-03 CONTRACT_PASS`. Este TOP no cierra E-04.

## 🧩 Subproyectos

_No aplica — hijo de implementación de E-04; no crea Integration ni más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-FORGE-INGESTION-E1/TASKS.md`. Aquí sólo work packages. NORMAL no arranca hasta manager review.
> - [x] WP-A DBTX adapter sobre repos E-03 #owner/agent #type/dev #area/echo
> - [x] WP-B Ingestion service + artifacts + tx + non-effects #owner/agent #type/dev #area/echo
> - [x] WP-C Gateway POST/GET + auth + timeout/concurrency #owner/agent #type/dev #area/echo
> - [x] WP-D Corpus S0 HTTP + SQL-direct + HandoffIngress test client (SYNTHETIC; no golden) #owner/agent #type/dev #area/echo
> - [x] WP-E SOURCE/coverage/governance cert pack #owner/agent #type/dev #area/echo
> - [ ] WP-F CROSS_LANE GOLDEN authentic Forge fixture (T21; FORGE_GOLDEN_FIXTURE_PENDING) #owner/agent #type/dev #area/echo

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

- **2026-09-12 (NORMAL correction complete)** — Desde la base exacta del Source Review `bfc0bc4b`, NORMAL corrigió sólo tests/evidencia y pusheó `4aef2958` a la branch feature. AC-10 alcanza el INSERT de promotion con SQLSTATE `23505` y verifica rollback de mapping/version/promotion; también quedaron cubiertos dependency artifacts (copy + integrity), strategy_ref conflict y assigned_at inválido. Reejecución real: identity_bwc PASS, E-03 34 PASS, SDK/gateway `-race` serial PASS, HTTP+PG PASS y coverage svc 82.2% / artifact 76.7% / handler 92% / auth 100%. Se documentó fricción del harness por DB compartida/TRUNCATE concurrente y el fallo preexistente de `contracts/wire` bajo Go 1.25.5. T21/AC-37 PENDING; sesión cerrada, sin verifier/merge/close.
- **2026-09-12 (Manager source review → CORRECTION test-only)** — Reviewer one-shot ([[2026-09-12-zcode-glm-5.3-flash-e04-manager-source-review]]): ancestry FF verificado (`6beac29f..bfc0bc4b`, 3 commits, 0 merges, delta ⊆ PLAN Allowed Files, master `c408a12f` intacto, contracts/061 diff 0). Repos E-03 = DBTX mecánico puro; pre-lookups de ingestion reusan `identitySealedEqual`/`versionSealedEqual` y quedan respaldados por UNIQUEs 061 (`TRANSACTION_ADAPTER_OK`). P0 corpus: escaneo sha256 exhaustivo de echo+symphony+sdk confirma que los 3 SHAs de G01 (y los de inputs/source de G10) no tienen preimage en ninguna authority; sólo `G10/g10-bytes.bin` existe; `ARTIFACT_FIXTURE_OK` con PASS* documentados y byte-authority pendiente de Manager. Gates reproducidos con PG 17.5 descartable (mismo harness portable E-03): identity_bwc PASS, E-03 34 PASS, E-04 `-race` 69 PASS/0 skip, coverage clavado al declarado. Finding material único: `TestIngest_RollbackOnPromotionFailure` no demuestra AC-10 (magic repetido dispara IDENTITY_CONFLICT de pre-lookup antes del INSERT de promotion; bloque de error del INSERT con count=0 en coverage focalizado) + huecos de cobertura alcanzables (`dependency_artifacts`, `strategy_ref` conflict, `assigned_at`) → CORRECTION test-only; sin cambios al source productivo. T21/AC-37 PENDING; no verifier lanzado; no CLOSED.
- **2026-09-12 (NORMAL done → READY FOR MANAGER SOURCE REVIEW)** — T01–T20 `[x]`, T21 `[ ]`. Commits `03b20abd`/`fc590b31`/`bfc0bc4b` pushed FF `6beac29f..bfc0bc4b` a `feature/e04-forge-ingestion-e1` tras pre-push race OK; `origin/master` intacto `c408a12f`. Gates: MIGRATION PASS (061 diff 0, identity_bwc PASS), E-03 regression 34 PASS, E-04 `-race` PASS contra PG 17.5 (5561), SOURCE greps vacíos, contracts diff 0. Coverage gateway 92% / sdk ingestion ~77% (delta documentado en VERIFICATION). Gap registrado: corpus S0 sin bytes de artefacto para sus propios refs (sólo G10); AC de aceptación demostrados con builders sintéticos S0-API + matriz G10 literal; `TestCorpus_G01_ArtifactPreimages` documenta el 422 físico; authority pin de bytes = decisión Manager. MCPs Aranea aplicados vía [[aranea-mcps-expert]] (DEV `echo-develop` sin tablas 061; Forge Mongo sin manifest handoff dedicado → `FORGE_GOLDEN_FIXTURE_PENDING` sin cambio). Estado `IMPLEMENTATION READY FOR MANAGER SOURCE REVIEW`. No verifier lanzado. No integrado. No E-04 CLOSED.

- **2026-09-12 (NORMAL start)** — Manager review superado; NORMAL arranca T01–T20. Verificación git fail-closed: `origin/feature/e04-forge-ingestion-e1` = `6beac29f`, `origin/master` = `c408a12f`, ancestros `c8e68538 <- 618607f8 <- c408a12f` OK, S0 `91671f6f` presente. Worktree exclusivo `impl/e04-forge-ingestion-e1-normal` @ `6beac29f` (la feature estaba checkout en `/tmp/echo-e04-forge-ingestion-e1`; no se reutiliza ni destruye). PG real: cluster portátil 17.5 (5561, DB `e04_ingestion`), harness identity_bwc PASS, baseline E-03 PASS. MCPs Aranea verificados vía [[aranea-mcps-expert]]: DEV `echo-develop` SIN tablas 061 (contexto, no mutado); Forge Mongo PROD plano F-02/F-04 sin manifest handoff dedicado → `FORGE_GOLDEN_FIXTURE_PENDING` sin cambio. Estado `IMPLEMENTING`. No master push. No E-03 touched.

- **2026-09-11 (TOP corrección T17)** — TASKS T17 alineado a `Deliver(ctx, ns, *HandoffManifestV1, payloadDigest)`. `payloadDigest` no es segunda autoridad HTTP (Echo sigue computando digest server-side). SPEC/PLAN/VERIFICATION no tocados. AC-34 sigue SYNTHETIC CONTRACT INTEGRATION. T21/`FORGE_GOLDEN_FIXTURE_PENDING` y E-03 interlock intactos. `6beac29f` pushed a `feature/e04-forge-ingestion-e1`. Master intacto. Estado `READY FOR MANAGER REVIEW`. No NORMAL.
- **2026-09-11 (TOP corrección 1.0.1)** — Manager findings: (1) S0/fakeconsumer no es CROSS_LANE GOLDEN; inspección Symphony → `FORGE_GOLDEN_FIXTURE_PENDING`; (2) CROSS_LANE development desacoplado de E-03 CONTRACT_PASS; integrate/close sigue gated. SPEC v1.0.1 @ `c8e68538` pushed a `feature/e04-forge-ingestion-e1`. T21/AC-37 añadidos. E-03 no tocado. Symphony no tocado. Master intacto. Estado `READY FOR MANAGER REVIEW`. No NORMAL.
- **2026-09-11 (TOP)** — Recovery: no había proyecto E-04 ni SPEC ejecutable. Se materializa este hijo, SPEC/PLAN/TASKS `FEAT-FORGE-INGESTION-E1` en branch `feature/e04-forge-ingestion-e1` desde `c408a12f` (planning SHA `618607f8`, pushed; `origin/master` intacto). Gobernanza: development paralelo a verification E-03; integrate gated por CONTRACT_PASS. Join F-04 congelado (HTTP + S0 + receipt). Estado `READY FOR MANAGER REVIEW`. No NORMAL. No master push. No session close.

## 🧭 Decisiones (ejecución, no semántica nueva)

- Hijo de implementación de E-04; ownership sigue en [[Echo — Live Platform V1]], no Integration.
- `development dependency` ≠ `golden dependency` ≠ `integration dependency`.
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
