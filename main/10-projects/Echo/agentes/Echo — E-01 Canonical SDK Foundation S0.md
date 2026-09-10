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
start: 2026-09-07
due:
progress: 100
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-01
  - Canonical SDK foundation S0
  - E-01 S0
  - FEAT-SDK-CANONICAL-CONTRACT
tags:
  - kind/project
  - area/echo
  - agent/owner
created: 2026-09-07
updated: 2026-09-10
cssclasses:
  - wide
---

# Echo — E-01 Canonical SDK Foundation S0

%% Naming: Echo — E-01 Canonical SDK Foundation S0 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-01 Canonical SDK Foundation S0
> **Área:** [[Echo]] · **Estado:** closed · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-01 / S0. No extrae ownership de S0 a un tercer producto. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Llevar E-01 desde el baseline Echo autorizado hasta **CONTRACT PASS** del módulo `github.com/xKoRx/echo/v3/sdk/contracts`, sin decisiones semánticas pendientes para NORMAL.

## 📊 Estado actual

- **VERIFIED / CLOSED (2026-09-10):** E-01 S0 obtuvo `CONTRACT_PASS` mediante re-verificación independiente desde `08a0eb9a83813cda2acbd7be5232e9e0370e12ab`. Verification commit `91671f6f46ffa889a79aed0979cb3b4e5821ed33`, publicado fast-forward; `origin/master` coincide. Corpus G01–G36 y write-once PASS; gates test/race-cover/vet/gofmt PASS; coverage contracts `95.1%`, wire `95.6%`, fakeconsumer `95.5%`.
- **IMPLEMENTACIÓN COMPLETA (NORMAL):** T01–T25 `[x]`; gates PASS; commit `f1070bec` sobre `18261429`. La certificación independiente queda pendiente de correcciones contractuales; `VERIFICATION.md` registra `CORRECTION_REQUIRED`.
- **Corrección de frontera decidida (TOP 2026-09-08):** `IMPLEMENTATION_CORRECTION` — la autoridad canónica `C()` opera sobre bytes JSON válidos (opción B); el mirror de internals de `encoding/json` en `wire/canonicalize.go` se elimina vía WP-G (T26–T29), pendiente manager + NORMAL nuevo. Sin cambio de contrato público/frozen; corpus y digests intactos. Estado S0 sigue `implementation complete / verification pending`.
- **WP-G implementado (NORMAL 2026-09-08):** T26–T29 completados en commit `f403e6d7` sobre `2be12e23`, publicado fast-forward a `origin/master`; byte-gate raw estricto, Go-value delegado a `encoding/json`, regresiones de frontera y gates requeridos PASS. Estado S0 sigue `implementation complete / verification pending`.
- **Verificación independiente (2026-09-08):** `CORRECTION_REQUIRED` contra implementation `f403e6d76cf1c2777458cbfcd82ded3c26b7a01d`; verification commit `bd681814b9ec697837360b840d55f659f195ca13`; `origin/master` y árbol limpio verificados. Delta: recipe incorrecta de `requested_keys_digest`, orden canónico de capabilities no impuesto, `record_digest` opcional/no verificado, gramática de metric keys no impuesta y `supersedes_evidence_refs` sin validación. E-01 permanece abierto.
- **Corrección NORMAL (2026-09-09):** contra verification commit `bd681814b9ec697837360b840d55f659f195ca13`, los cinco findings fueron implementados en worktree limpio y publicados en commit `08a0eb9a83813cda2acbd7be5232e9e0370e12ab` (parent exacto, fast-forward a `origin/master`). Gates completos, schema drift NONE, derivación independiente y scope gate PASS; corpus limitado a G27/G28/G30/G32. Estado técnico: `implementation complete / verification pending`; no verified/closed.
- **Re-verificación independiente bloqueada (2026-09-09):** el baseline gate no pudo certificarse: checkout local `HEAD=bd681814b9ec697837360b840d55f659f195ca13`, `origin/master=08a0eb9a83813cda2acbd7be5232e9e0370e12ab` tras fetch, y el árbol contiene cambios locales no commiteados en source/tests/corpus más `verification_findings_test.go`; `git pull --ff-only` se detuvo para no sobrescribirlos. No se ejecutaron gates ni se modificó el repo. E-01 permanece abierto como `verification pending`.
- **Baseline Echo:** `04c16bd2bd7b69725560873950a5d6b067fd3a4f` (`origin/master`).
- **Físico:** módulo parent `github.com/xKoRx/echo/v3/sdk` existe; `v3/sdk/contracts` **no existe**.
- **Contrato WHAT:** repo `xKoRx/echo` path `specs/FEAT-SDK-CANONICAL-CONTRACT/SPEC.md` (no duplicar FR aquí).
- **Checklist atómico:** `specs/FEAT-SDK-CANONICAL-CONTRACT/TASKS.md` (T01–T25).
- **PLAN.md local Echo:** puente obligatorio de gobernanza; no copia esta nota.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `master` (fase E-01) | `04c16bd2bd7b69725560873950a5d6b067fd3a4f` | [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] + freeze [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]] | `specs/FEAT-SDK-CANONICAL-CONTRACT/SPEC.md` @ `182614297138c8c6fa0f02cd6aa8a5decf151479` | TOP READY_FOR_NORMAL |

## 🗺️ Source map (baseline)

- **SDK module:** `github.com/xKoRx/echo/v3/sdk` (`v3/sdk/go.mod`, Go 1.25.5, Kafka/etcd/OTel/postgres).
- **contracts package preexisting:** **no**.
- **Helpers reutilizables:** **ninguno** como autoridad. `v3/sdk/utils/json.go` y `v3/sdk/domain/json.go` usan `encoding/json` stdlib; no implementan `C()`.
- **Collisions (no importar, no migrar):** `v3/sdk/lab/domain.MetricSnapshot` (`ProfitFactorR`/`Money`, `MaxDrawdownR`/`Money`); `v3/sdk/lab/formulas.RBasis` `auto|money|pips`; `CanonicalTrade`. Nombres `Metric`/`Scope` del Lab no son `MetricV1`/`ScopeV1`.
- **Legacy HashIdentity carrier:** Symphony `sqx/core/domain/persistence_identity.go` `HashIdentity` / `hashIdentity` (newline join). `NewEvaluationRef` / `NewMetricSetRef` / `NewTradeSetRef` usan esa receta. **No modificar Symphony.**
- **go.work:** lista `./v3/sdk`; **no** se toca en S0.

## 🎯 Target physical state

```text
v3/sdk/contracts/
  go.mod                 # module github.com/xKoRx/echo/v3/sdk/contracts; go 1.24
  doc.go README.md
  identity.go evidence.go scope.go trading.go analytics.go catalog.go
  promotion.go score.go runtime.go conflict.go status.go
  wire/{canonicalize,validate,hash,unknown}.go + tests
  fakeconsumer/
  schema/                # generado
  testdata/v1/manifest.json + G01–G36 + write-once-conflict
```

Ningún archivo fuera de `v3/sdk/contracts/**`.

## 🕸️ Dependency graph

```text
T01 scaffold
  → T02 C() → T03 validator
  → T02 → T04 H() → T05 D() → T06 ≠ HashIdentity
  → T05 → T07 Scope → T08 identity components
       T08 → T09 Evaluation
       T08 → T10 TradeSet
       T03+T08 → T11 MetricSelector → T12 MetricSet
       T11 → T13 statuses
       T05+T13 → T14 operation_ref → T15 record_digest → T16 supersession
       T02+T03 → T17 unknown fields
       T09+T10+T12 → T18 CONTRACT_CONFLICT
       T04 → T19 StrategyVersion/ArtifactRef
       T08+T19 → T20 remaining types
       T18+T20 → T21 G01–G24 → T22 G25–G36
       T20 → T23 schema
       T21 → T24 fake consumer
       T01–T24 → T25 certification
```

Paralelo seguro tras T08: T09 ∥ T10 ∥ T11. T06 ∥ T07 tras T04/T05.

Fases producto: E-01 no tiene dependencia de E-02. Desbloquea E-03, E-05, F-04. No ejecutar esas fases aquí.

## Allowed scope NORMAL

- **Exact allowed:** `v3/sdk/contracts/**`
- **Parent `v3/sdk/go.mod` / `go.sum`:** no (delta `NONE`)
- **go.work:** no (certificar `GOWORK=off`)
- **Prohibido:** `v3/**` resto, tests existentes, SQL, CI, Symphony, Resources frozen

## 📦 Work packages

WP-A Wire T01–T06. Implicación FR-4: `C()` agnóstico; validador aparte; no exportar HashIdentity.
WP-B Identity T07–T12, T18–T19. Implicación FR-1/FR-3: refs sin digest de resultado; Scope sin valuation.
WP-C Operations T13–T17. Implicación FR-5: `operation_ref` estable; `record_digest` sin sí mismo.
WP-D Surface T20. Tipos Handoff/Score/Coverage; sin HTTP.
WP-E Corpus T21–T24. G01–G36 + write-once; expected bytes no autogenerados en el mismo test.
WP-F Gate T25.
WP-G Corrección frontera canónica (T26–T29, pendiente): `C()` autoridad sobre bytes JSON; eliminar mirror de internals stdlib en `wire/canonicalize.go`. Allowed files: `v3/sdk/contracts/wire/canonicalize.go` + `v3/sdk/contracts/wire/canonicalize_test.go`. Estado no cambia hasta que manager acepte y un NORMAL nuevo implemente.

## TOP / NORMAL boundaries

- TOP: SPEC, esta nota, TASKS, PLAN puente, linkage padre. No source Go.
- NORMAL: T01–T25 mecánicamente. No rediseñar FR. No ampliar allowed files. No “arreglar” failures baseline del parent SDK.
- GOD: NONE.

## Migrations

`NONE`. Si aparece SQL indispensable: **BLOCKED**.

## Dependency delta

`NONE`. Stdlib only. No pin de terceros. No modificar parent require.

## Compatibility strategy

Paths nuevos. No adapters S0. No rehash legacy. Corpus es la superficie de pin para Forge; el **manager** (no NORMAL) decide commit exacto, corpus publicable y mecanismo de versión/pin hacia F-04. No inventar sistema de releases. No tag.

## Test strategy

SPEC define propiedades AC-01…AC-17. TASKS asigna cada propiedad a un test nombrado. Corpus Gxx a nivel contrato; crash físico G35/G35-DB es E-04. Coverage: caminos de receta/conflicto/selector primero, luego piso ≥95% del módulo anidado.

## Certification gates (NORMAL)

```bash
cd v3/sdk/contracts
GOWORK=off go test ./...
GOWORK=off go test -race -cover ./...
GOWORK=off go vet ./...
```

Imports stdlib-only. Golden manifest estable. Fake consumers compilan. Parent `go test ./...` en `v3/sdk` **no** es gate de S0 (fallos preexistentes de infra).

## Baseline tests (parent SDK, registrados)

Comando: `cd v3/sdk && go test ./...` en `04c16bd2`.

**FAIL preexistentes (no S0, no ampliar scope):**

- `etcd` `TestSeedEchoConfig_Production` — `bridge/reference_accounts` key not found (requiere etcd real).
- `postgres` `TestScratch_QueryKafka` y `TestScratch_QueryKafkaCloseResults` — timeout ~25s (Kafka/infra).
- `telemetry` `TestVerifyDevJaegerReceivesTraces` — Jaeger `192.168.31.45:16686` connection refused.

Packages `domain`, `lab/*`, `mm`, `messaging`, `utils`, `kache`, `comment` OK en esa corrida.

## Release / pin expectations

Al cierre de implementación el **manager** determina: commit S0 exacto; corpus publicable; pin real; handoff mínimo a Forge F-04. TOP/NORMAL no taguean ni pushean.

## Blockers

Ninguno material para arrancar NORMAL. No bloquear por Graphify stale ni por ausencia actual de `v3/sdk/contracts`.

## Handoff requirements

NORMAL trabaja contra baseline `04c16bd2` + SPEC + TASKS. Dirty foráneo se preserva. Un commit de implementación aparte del commit SDD TOP. Sin push.

## Closure conditions

T01–T25 `[x]`; gates T25 PASS; allowed files respetados; SPEC AC cubiertos por tests listados; corpus G01–G36 + write-once presente; certificación independiente registrada en `VERIFICATION.md` (fuera de este TOP), actualmente `CORRECTION_REQUIRED`.

## 🧩 Subproyectos

_No aplica — este es el hijo de implementación de E-01; no crea Integration ni más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-SDK-CANONICAL-CONTRACT/TASKS.md`. Aquí sólo work packages.
> - [x] WP-A Wire C/H/D + validator + desigualdad HashIdentity #owner/agent #type/dev #area/echo
> - [x] WP-B Identity FR-1/FR-2/FR-3 + conflicto write-once #owner/agent #type/dev #area/echo
> - [x] WP-C Operations FR-5 + unknown fields #owner/agent #type/dev #area/echo
> - [x] WP-D Handoff/Score/Runtime types puros #owner/agent #type/dev #area/echo
> - [x] WP-E Corpus G01–G36 + fake consumer #owner/agent #type/dev #area/echo
> - [x] WP-F Certification GOWORK=off #owner/agent #type/dev #area/echo
> - [x] WP-G Corrección frontera canónica: C() sobre bytes JSON, eliminar mirror stdlib (T26–T29) #owner/agent #type/dev #area/echo

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

- **2026-09-10 (VERIFIER INDEPENDIENTE — cierre):** `CONTRACT_PASS`. Implementation `08a0eb9a83813cda2acbd7be5232e9e0370e12ab`; verification `91671f6f46ffa889a79aed0979cb3b4e5821ed33`; `origin/master` coincide y el worktree de verificación quedó limpio. Findings requested keys, metric grammar, capabilities, record digest y supersession PASS; FR-1…FR-5 PASS; G01–G36, G27/G28/G30/G32, write-once y schema drift PASS/NONE. E-01 queda `verified / closed`.

- **2026-09-09 (VERIFIER INDEPENDIENTE — re-verificación):** `BLOCKED` antes de source review y gates. El baseline requerido no era reproducible: `HEAD` quedó en `bd681814b9ec697837360b840d55f659f195ca13`, `origin/master` resolvió a `08a0eb9a83813cda2acbd7be5232e9e0370e12ab` y el worktree estaba dirty con cambios productivos posteriores. Se preservaron todos los cambios; no hubo commit/push de verificación. E-01 queda abierto.

- **2026-09-09 (NORMAL — cierre de findings):** requested keys, gramática de metric keys, capabilities canónicas, `record_digest` requerido/verificado y `supersedes_evidence_refs` estructural quedaron PASS. G27/G28/G30/G32 fueron reparados sólo en derivados autorizados; G01–G36 y write-once PASS. Commit `08a0eb9a83813cda2acbd7be5232e9e0370e12ab` publicado y árbol limpio. E-01 sigue `implementation complete / verification pending`.

- **2026-09-08 (TOP — boundary resolution E-01):** resuelve el conflicto del mirror de internals stdlib acumulado por c2472ca9→2be12e23 (el prompt de corrección exigía BLOCKED ante una segunda implementación de `typeFields`; el stop condition no fue respetado). Decisión cerrada: **opción B — `IMPLEMENTATION_CORRECTION`**. La autoridad canónica de `C()` opera sobre bytes JSON válidos: el lane Go-value delega la serialización a `encoding/json` (comportamiento público documentado, incluido reemplazo U+FFFD en strings Go inválidos) y toda la strictness UTF-8 se aplica en el byte-gate único de `canonicalJSON` (inválido, BOM, output de Marshaler inválido — verificado físicamente en go1.25.5). El lane raw (`[]byte`/`RawMessage`) conserva rechazo estricto. Los ciclos los detecta el propio stdlib (`encountered a cycle`). FR-4a frozen intacto ("UTF-8 válido sin BOM" es propiedad del perfil sobre payloads válidos; `C()` debe ser implementable en MQL5/JS, i.e. definido sobre bytes); TASKS T02 sin contradicción (satisfecho verbatim); corpus sin ningún golden dependiente del precheck Go (verificado); callers (`Digest`/`HashTagged`/`PayloadDigest`/`EncodeCanonical`) con outputs byte-idénticos para valores válidos. **WP-G T26–T29 (atómicos, un solo NORMAL):** T26 eliminar en `canonicalize.go` `checkUTF8Value`, `walkUTF8`, `walkUTF8Concrete`, `walkUTF8MapKey`, `replacedByCustomMarshaler`, `jsonField`, `jsonFieldQueueEntry`, `selectJSONFields`, `selectedJSONFields`+cache, `dominantJSONField`, `jsonTagName`, `isValidJSONTagName` e imports muertos; conservar byte-gates, `canonicalJSON`, `emitCanonical`, `appendJSONString`, `sortStrings` y el resto del paquete intacto. T27 doc contract: dos lanes documentados en `Canonicalize` (raw estricto / Go-value con semántica stdlib documentada). T28 tests de regresión: reworked `RejectsInvalidUTF8` (raw rechaza; Go-value pinna U+FFFD documentado del stdlib), U+FFFD legítimo pasa verbatim en ambos lanes, `\xff` vs `\xfe` raw ambos rechazados (no convergen en el wire gate), ciclos fallan vía error stdlib; se eliminan los tests de paridad del mirror (StringKindMapKeyIgnoresMarshalText, AmbiguousPromotedFieldsBothIgnored, DoublyEmbeddedSameTypeDropped, ShallowFieldDominatesDeeper, TaggedFieldDominatesUntagged, JsonDashTagVariants, UnexportedNonStructEmbedIgnored, AnonymousPointerSelectionParity, EmbeddedUnexportedPromotionObserved, ArrayElementsPrevalidated, variantes MarshalerPointerReceiver*/NilPointer); todos los goldens Gxx sin ningún cambio de bytes/digest. T29 gates: `GOWORK=off go test ./...`, `-race -cover` (wire ≥95%), `go vet`, gofmt, test stdlib-only PASS, sin GOEXPERIMENT, commit único sobre allowed files. Ajuste SDD repo: ninguno requerido (opcional y aditivo: manager puede ratificar añadir T26–T29 a TASKS.md al momento de ejecutar).
- **2026-09-08 (NORMAL — WP-G T26–T29):** mirror productivo eliminado; `Canonicalize` documenta y aplica la frontera raw/Go-value sobre bytes JSON. Regresiones comparan Go-value contra la salida física de `encoding/json` para strings inválidas, ciclos, Marshaler, TextMarshaler, embedding, `[]byte` y `json.RawMessage`; raw inválido/BOM/key inválida rechazan. Gates: test PASS; race/cover PASS (contracts 95.1%, wire 95.6%); vet/gofmt/source gate PASS; corpus unchanged; commit `f403e6d7` publicado fast-forward. S0 permanece `implementation complete / verification pending`.

- **2026-09-08 (corrección 4)** — `fix(sdk): match json map-key and field selection` commit `2be12e23` (parent `aafa2f62`, publicado fast-forward): paridad final del precheck UTF-8 con encoding/json de go1.25.5. Map keys siguen la precedencia exacta de `resolveKeyName` — string kind primero, así que un named string con `MarshalText` como key se observa como el string real y su UTF-8 inválido se rechaza; sólo después TextMarshaler y enteros. La selección de struct fields es una reducción fiel de `typeFields`/`dominantField` (promoción, profundidad, tagged domina, aniquilación de conflictos, embed no exportado, pointer anónimo nil sin error artificial, `json:"-,"` observado), sin reimplementar serializer. 8 tests nominales con premisa física `json.Marshal`. Gates PASS: wire 97.5% / contracts 95.1%, race+vet+gofmt limpios. Estado S0: implementation complete / verification pending.
- **2026-09-08 (corrección 3)** — `fix(sdk): align UTF-8 prevalidation with json serialization` commit `aafa2f62` (parent `6cf39edf`, publicado fast-forward): el pre-walk UTF-8 ahora espeja `newTypeEncoder` de encoding/json — Marshaler (value receiver) > TextMarshaler, pointer receivers sólo cuando el valor es addressable (`CanAddr()`, igual que `condAddrEncoder`), method sets promovidos de embebidos, map keys TextMarshaler, promoción de campos exportados de structs embebidos no exportados y caso Array. 13 tests nuevos con `MarshalJSON`/`MarshalText` reales; `[]byte` base64 y `RawMessage` verbatim verificados; semántica stdlib confirmada con probes físicos sobre go1.25.5. Gates PASS; wire 97.0%. Estado S0: implementation complete / verification pending.
- **2026-09-08 (corrección 2)** — `fix(sdk): make UTF-8 prevalidation cycle-safe` commit `6cf39edf` (parent `c2472ca9`, publicado fast-forward): pre-walk UTF-8 con detección de ciclos por camino activo (ptr/map/slice) y salta exactamente lo que encoding/json no serializa (no exportados, `json:"-"`, tipos Marshaler). Referencias compartidas acíclicas siguen válidas. Gates PASS; wire 96.8%. Estado S0: implementation complete / verification pending.
- **2026-09-08 (corrección acotada)** — `fix(sdk): reject invalid UTF-8 in canonical wire` commit `c2472ca9` (parent `f1070bec`): `Canonicalize` y `Validate` rechazan UTF-8 inválido (`INVALID_WIRE`), sin reemplazo U+FFFD; BOM sigue rechazado; no-ASCII válido preservado byte-exacto. Gates PASS, coverage wire 96.9% (piso ≥95 mantenido). Publicado fast-forward a `origin/master`. Estado S0: implementation complete / verification pending (NO certified).
- **2026-09-08 (publicación)** — Cadena `18261429` + `f1070bec` publicada a `origin/master` (fast-forward `04c16bd2..f1070bec`, sin force); remoto verificado `origin/master == HEAD`; árbol limpio. Pendiente: Verifier (VERIFICATION.md) y decisión manager (pin/corpus publicable).
- **2026-09-08** — Implementación NORMAL completada: commit `f1070bec` (152 archivos, sólo `v3/sdk/contracts/**`) sobre `18261429`. Gates: `GOWORK=off go test/-race -cover/vet` PASS; coverage recetas 95.1% / wire 97.0% / fakeconsumer 95.5%; corpus G01–G36 + write-once fixture; schema regenera sin drift; stdlib-only verificado por test. Dirty foráneo inexistente.
- **2026-09-07** — Materializado desde template `project`. Parent [[Echo — Live Platform V1]]. SPEC/TASKS/PLAN puente en `xKoRx/echo` feature `FEAT-SDK-CANONICAL-CONTRACT` commit `18261429`. Baseline `04c16bd2`. No source Go.

## 🧭 Decisiones (ejecución, no semántica)

- Frontera canónica (TOP 2026-09-08): `C()` es autoridad sobre bytes JSON válidos; el lane Go-value no replica internals privados de `encoding/json` (stop condition de corrección restablecido). Strictness UTF-8 en un único byte-gate (`canonicalJSON`); el lane Go depende sólo de comportamiento público documentado del stdlib (U+FFFD, ciclos, errores de Marshaler), no de internals como `typeFields`/`newTypeEncoder`/`resolveKeyName`.

- Hijo de implementación de E-01; S0 sigue siendo del track [[Echo — Live Platform V1]], no Integration.
- `go.work` no se modifica; gate `GOWORK=off`.
- Tag `echo-operation-ref.v1` cerrado en SPEC (freeze exigía hash etiquetado sin string literal).
- Failures parent SDK de etcd/Kafka/Jaeger son preexistentes.

## 🔗 Docs / Links

- [[Echo — Live Platform V1]]
- [[Echo — Producto Integrado]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]
- SPEC técnico: `xKoRx/echo` `specs/FEAT-SDK-CANONICAL-CONTRACT/SPEC.md`
- TASKS: `xKoRx/echo` `specs/FEAT-SDK-CANONICAL-CONTRACT/TASKS.md`
- PLAN puente: `xKoRx/echo` `specs/FEAT-SDK-CANONICAL-CONTRACT/PLAN.md`

## 💡 Ideas

### Backlog de ideas

- Adapters Lab/Forge: post S0 (E-05 / F-04), no este subproyecto.

### Motivos / principios

- Una fuente por hecho: SPEC = contrato; esta nota = ejecución; TASKS = checklist.

### Memoria pública / interna

- **Memoria pública:** Resources frozen enlazadas.
- **Memoria interna:** continuidad en esta nota.
- **Motivo:** no duplicar FR-1…FR-5.
