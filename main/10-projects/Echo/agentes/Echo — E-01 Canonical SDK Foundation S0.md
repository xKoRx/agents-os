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
updated: 2026-09-07
cssclasses:
  - wide
---

# Echo — E-01 Canonical SDK Foundation S0

%% Naming: Echo — E-01 Canonical SDK Foundation S0 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-01 Canonical SDK Foundation S0
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-01 / S0. No extrae ownership de S0 a un tercer producto. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Llevar E-01 desde el baseline Echo autorizado hasta **CONTRACT PASS** del módulo `github.com/xKoRx/echo/v3/sdk/contracts`, sin decisiones semánticas pendientes para NORMAL.

## 📊 Estado actual

- **IMPLEMENTACIÓN COMPLETA (NORMAL):** T01–T25 `[x]`; gates PASS; commit `f1070bec` sobre `18261429`. CONTRACT PASS formal lo declara el Verifier en VERIFICATION.md (fuera de este TOP).
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

T01–T25 `[x]`; gates T25 PASS; allowed files respetados; SPEC AC cubiertos por tests listados; corpus G01–G36 + write-once presente; `CONTRACT PASS` declarado por Verifier en `VERIFICATION.md` (fuera de este TOP).

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

- **2026-09-08 (corrección 3)** — `fix(sdk): align UTF-8 prevalidation with json serialization` commit `aafa2f62` (parent `6cf39edf`, publicado fast-forward): el pre-walk UTF-8 ahora espeja `newTypeEncoder` de encoding/json — Marshaler (value receiver) > TextMarshaler, pointer receivers sólo cuando el valor es addressable (`CanAddr()`, igual que `condAddrEncoder`), method sets promovidos de embebidos, map keys TextMarshaler, promoción de campos exportados de structs embebidos no exportados y caso Array. 13 tests nuevos con `MarshalJSON`/`MarshalText` reales; `[]byte` base64 y `RawMessage` verbatim verificados; semántica stdlib confirmada con probes físicos sobre go1.25.5. Gates PASS; wire 97.0%. Estado S0: implementation complete / verification pending.
- **2026-09-08 (corrección 2)** — `fix(sdk): make UTF-8 prevalidation cycle-safe` commit `6cf39edf` (parent `c2472ca9`, publicado fast-forward): pre-walk UTF-8 con detección de ciclos por camino activo (ptr/map/slice) y salta exactamente lo que encoding/json no serializa (no exportados, `json:"-"`, tipos Marshaler). Referencias compartidas acíclicas siguen válidas. Gates PASS; wire 96.8%. Estado S0: implementation complete / verification pending.
- **2026-09-08 (corrección acotada)** — `fix(sdk): reject invalid UTF-8 in canonical wire` commit `c2472ca9` (parent `f1070bec`): `Canonicalize` y `Validate` rechazan UTF-8 inválido (`INVALID_WIRE`), sin reemplazo U+FFFD; BOM sigue rechazado; no-ASCII válido preservado byte-exacto. Gates PASS, coverage wire 96.9% (piso ≥95 mantenido). Publicado fast-forward a `origin/master`. Estado S0: implementation complete / verification pending (NO certified).
- **2026-09-08 (publicación)** — Cadena `18261429` + `f1070bec` publicada a `origin/master` (fast-forward `04c16bd2..f1070bec`, sin force); remoto verificado `origin/master == HEAD`; árbol limpio. Pendiente: Verifier (VERIFICATION.md) y decisión manager (pin/corpus publicable).
- **2026-09-08** — Implementación NORMAL completada: commit `f1070bec` (152 archivos, sólo `v3/sdk/contracts/**`) sobre `18261429`. Gates: `GOWORK=off go test/-race -cover/vet` PASS; coverage recetas 95.1% / wire 97.0% / fakeconsumer 95.5%; corpus G01–G36 + write-once fixture; schema regenera sin drift; stdlib-only verificado por test. Dirty foráneo inexistente.
- **2026-09-07** — Materializado desde template `project`. Parent [[Echo — Live Platform V1]]. SPEC/TASKS/PLAN puente en `xKoRx/echo` feature `FEAT-SDK-CANONICAL-CONTRACT` commit `18261429`. Baseline `04c16bd2`. No source Go.

## 🧭 Decisiones (ejecución, no semántica)

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
