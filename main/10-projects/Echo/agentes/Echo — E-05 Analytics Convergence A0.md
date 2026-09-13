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
start: 2026-09-12
due:
progress: 70
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-05
  - Analytics convergence A0
  - E-05 A0
  - FEAT-ANALYTICS-CONVERGENCE-A0
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-12"
updated: "2026-09-13"
cssclasses:
  - wide
---

# Echo — E-05 Analytics Convergence A0

%% Naming: Echo — E-05 Analytics Convergence A0 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-05 Analytics Convergence A0
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-05 / Analytics convergence A0. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Dejar la foundation analítica canónica lista: paths nuevos para Operation/Scope/TradeSet/MetricSet, adapters Lab, calculator Go con `key+basis+unit+formula`, persistencia PG write-once 063 y Hasura SELECT, sin big-bang Lab, sin Strategy Quality y sin Execution Fidelity.

## 📊 Estado actual

- **FULL INDEPENDENT VERIFIER #3 — PREFLIGHT PASS (2026-09-13).** El checkout inicial bajo `~/go/src/github.com/xKoRx/echo` era E-02 y fue descartado; el worktree canónico documentado `/tmp/echo-e05-analytics-a0` está limpio en `feature/e05-analytics-convergence-a0` con `HEAD == origin/feature == e917e25ad4b1ce4a7148229f1da3bf804c3a1cff`. `master`/`origin/master` permanecen en `a99f9a63354bbe72219d1e590bb93757ed08e45e`; la certificación continúa sobre el worktree correcto.
- **IMPLEMENTATION CORRECTED — READY FOR FULL RE-VERIFICATION #3 (2026-09-13).** Correction #2 `233e22bfb56879cee42926f08230ca4ce4eebde9` corrige el redondeo decimal half-even negativo a 12 dígitos en `v3/sdk/analytics/formulas/closed_ops.go`: `big.Rat` exacto, paridad sobre magnitud retenida y ajuste explícito según el signo del numerador, incluido `q == 0`; evidencia `e917e25ad4b1ce4a7148229f1da3bf804c3a1cff`. Matriz A–N, simetría, `pnl.total`/`return.total`/`return.expectancy` negativos, digest/ref/bytes deterministas y regresiones currency/builders/repo/stores/SOURCE E-04 PASS. No verifier relanzado, no merge, no DONE; falta full re-verification #3.
- **IMPLEMENTATION CORRECTED — READY FOR FULL RE-VERIFICATION (2026-09-13).** Post-verifier correction `eb3cebf0a24e1ebe1dc8883b65644052b01f72f5`: `CanonicalA0Params.Currency` es la única autoridad para `MetricDefaults.Currency`; la currency Lab uniforme o mixed no se infiere y `CURRENCY_UNPROVEN` permanece marcado. Tests focalizados A–E, analytics, builders/repo, writer/stores, PG 17.11 físico y gates históricos E-04 PASS. No verifier relanzado, no merge, no DONE; falta reverificación completa.
- **FULL RE-VERIFICATION #2 FAIL (2026-09-13).** Target exacto `d40153f38101febf381b2a3fb9abf6f6834ebdc0` pasa el pre-flight Git y las suites Go ejecutadas, pero `v3/sdk/analytics/formulas/DecimalString` redondea mal un half-tie negativo (`-1.2345678901235` → `-1.234567890122` en vez de `-1.234567890124`). La matriz completa se detuvo fail-closed en este defecto material; no se ejecutaron gates PG/Hasura/BWC/coverage posteriores, no se aplicaron fixes, y el interlock 062 sigue vigente.
- **INDEPENDENT VERIFIER FAIL (2026-09-13).** Target `baa2e305` no pasa AC-04: `lab-canonical-a0` infiere `MetricDefaults.Currency` desde la única moneda de filas Lab cuando el parámetro es vacío, pudiendo convertir el default USD ambiguo en `pnl.total` canónico COMPUTED pese a `CURRENCY_UNPROVEN`. Requerido: no inferir moneda Lab; exigir moneda explícitamente probada o fallar cerrado. PG/Hasura/BWC restantes no se ejecutaron tras el defecto. No fix, no merge, no deploy; interlock 062 sigue vigente.
- **MANAGER SOURCE REVIEW PASS FUNCIONAL (2026-09-13).** No se detectó defecto material en analytics, migration 063, writer transaccional, stores, adapters/BWC ni Hasura gate; `HASURA_DEV_APPLY=NOT_RUN` sigue cubierto por la variante yaml+PG local de T19.
- **IMPLEMENTATION READY FOR INDEPENDENT VERIFIER (2026-09-13, corrección pre-verifier).** Implementación completa @ `baa2e305` en `origin/feature/e05-analytics-convergence-a0`; gates E-04 SOURCE corregidos por scoping histórico E-03 `fac48051` → E-04 `a99f9a63`, sin ampliar allowlist ni tocar semántica productiva. SOURCE E-05 y regresión Go relevantes PASS; `identity_bwc/run.sh` no ejecutable por ausencia de `psql` en PATH; no verifier lanzado, no merge, no CLOSED. Interlock: 063 sin merge/deploy hasta 062 de E-02 en `master`. Detalle en `specs/FEAT-ANALYTICS-CONVERGENCE-A0/VERIFICATION.md`.
- **TOP CORRECTION READY FOR MANAGER REVIEW (2026-09-12, docs-only, v1.0.1).** SPEC/PLAN/TASKS/VERIFICATION @ `dd1f2da9a630bb3b6f49e585b7b433f05c841ef9` en `origin/feature/e05-analytics-convergence-a0` (base `origin/master` `a99f9a63354bbe72219d1e590bb93757ed08e45e`). Cero líneas en `v3/**`. Master intacto. NORMAL no lanzado.
- **Reserva de migración:** E-02 owner de `062_journal_quarantine`. E-05 owner exclusivo de `063_analytics_convergence_a0`. 062 prohibida para E-05. 064+ fuera de scope. E-02 **no** bloquea development/implementation/verification. Merge/deploy de 063 espera 062 integrado en `master`.
- **Baseline verificado:** `origin/master` no avanzó respecto a `a99f9a63`. S0 READ ONLY @ `91671f6f`. E-03 CONTRACT_PASS en master; tablas 061 **NOT_APPLIED** en Aranea PG. E-04 INTEGRATED; T21 no bloquea E-05.
- **Autoridad física Lab:** PG 17.6 PROD `echo` + DEV `echo-develop`. Snapshots 10932, win_rate RATIO 0..1, version NULL, outcomes REFERENCE-only, `v_trade_execution_delta` INNER JOIN, R AUTO en source. Hasura DEV/PROD v2.38.0 consistent.
- **Contrato WHAT:** `specs/FEAT-ANALYTICS-CONVERGENCE-A0/SPEC.md` v1.0.1. TASKS T01–T21. AC-01…AC-23.
- **AUTHORITY_CONFLICT:** ninguno. S0 ya tiene tipos/catálogo/recetas; Lab es proyección mutable; A0 persiste sets nuevos sin duplicar S0. Semántica analítica 1.0.0 intacta.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e05-analytics-convergence-a0` | `a99f9a63354bbe72219d1e590bb93757ed08e45e` | [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] §§4–8 FR-2/FR-3 | `specs/FEAT-ANALYTICS-CONVERGENCE-A0/SPEC.md` v1.0.1 @ `dd1f2da9` | IMPLEMENTATION READY FOR INDEPENDENT VERIFIER @ `baa2e305` · no verifier · no merge |

## 🗺️ Source map (baseline `a99f9a63` + PG/Hasura)

- S0: `v3/sdk/contracts/{analytics,catalog,scope,trading,conflict}.go` — READ ONLY.
- Lab: `v3/sdk/lab/{domain,formulas,metrics}` + `lab-worker` recompute/materialize — BWC, no autoridad A0.
- PG: `lab_canonical_trades` / `lab_strategy_outcomes` / `lab_strategy_metric_snapshots` / `trade_journal` / `v_lab_strategy_screener` / `v_trade_execution_delta`.
- Identity 061: source sí, Aranea no. A0 sin FK SQL.
- Front GraphQL Lab: display only; win_rate RATIO mostrado a veces con `%`.
- Kafka/Flink/GitHub MCP: NOT_OBSERVED.

## 🎯 Target physical state

```text
v3/sdk/analytics/{adapter,calculator,formulas}
v3/sdk/postgres/canonical_{scope,tradeset,metricset}_store.go
v3/sdk/postgres/canonical_writer.go
v3/sdk/postgres/migrations/063_analytics_convergence_a0.{up,down}.sql
echo.canonical_scopes + canonical_trade_sets + canonical_metric_sets
echo.v_canonical_{trade,metric}_sets
v3/lab-worker/cmd/lab-canonical-a0
v3/hasura/metadata/tables/canonical_analytics.yaml   # SELECT only
```

Ningún cambio a `v3/sdk/contracts/**`. Ningún rewrite Lab. Ningún score/ranking.

## 🕸️ Dependency graph

Ver TASKS.md. Paralelo: T01 ∥ T05 ∥ T06. Writer T13 tras stores+calculator. T21 cert.

No ejecutar E-02/E-04/E-06/E-09/E-10 aquí. E-02 no bloquea development/implementation/verification. Merge/deploy de 063 espera 062 de E-02 en `master`.

## Allowed scope NORMAL

Exacto PLAN.md. Development en `feature/e05-analytics-convergence-a0` desde `a99f9a63`. Worktree `/tmp/echo-e05-analytics-a0` (no el checkout E-02). Prohibido `origin/master` push/merge de 063 mientras 062 de E-02 no esté en `master`. Prohibido `v3/sdk/contracts/**`. Prohibido 061. Prohibido 062 (reserva E-02). 063 exclusiva E-05. 064+ fuera de scope. Prohibido Aranea PROD como DB de test.

## 📦 Work packages

- **WP-A Persistencia** T01–T04, T16. Migración 063 + stores write-once.
- **WP-B Adapters** T05, T11, T12. Lab operations/snapshots + journal provenance.
- **WP-C Calculator** T06–T10, T20. Fórmulas §9; E-09 keys fail-closed.
- **WP-D Writer/job** T13–T14. Dual-run; no ReplaceByScope.
- **WP-E Hasura READ** T15, T19. SELECT vistas. No PROD apply.
- **WP-F Cert** T17, T18, T21. SOURCE/BWC/coverage.

## TOP / NORMAL boundaries

- TOP: SPEC, esta nota, TASKS, PLAN puente, linkage padre. No source Go/SQL productivo (cumplido).
- NORMAL: T01–T21 mecánicamente. No elegir catálogo, AUTO, ni backfill masivo. No SQ/EF.
- GOD: NONE.

## Migrations

Una: `063_analytics_convergence_a0` (exclusiva E-05). Independiente de 061. `062_journal_quarantine` es owner/reserva de E-02; E-05 no la toca. 064+ fuera de scope. Gate up/down/up en PG descartable. No apply PROD. Merge/deploy de 063 espera 062 de E-02 en `master`.

## Dependency delta

NONE de terceros. `v3/sdk/analytics` importa contracts (mismo parent module).

## Compatibility strategy

Paths y tablas nuevas. Lab jobs/vistas/Hasura legacy intactos. Dual-run. UI E-13.

## Testing / gates

SPEC AC-01…AC-23. SOURCE + CONTRACT + PG REAL + HASURA DEV + BWC. Ver VERIFICATION.md stub.

## Blockers

Ninguno para development, implementation ni verification. E-02 no bloquea esos tres. E-04 T21 no bloquea. 061 NOT_APPLIED en Aranea no bloquea (A0 sin FK). Kafka NOT_OBSERVED no bloquea. Apply 063 a Aranea es deuda ops, no gate CONTRACT. **Integration/deploy interlock:** no mergear/deployar 063 mientras 062 de E-02 no esté integrado en `master`.

## Handoff requirements

Manager aprueba planning v1.0.1 → NORMAL implementa T01–T21 en worktree de esta branch desde `a99f9a63`. No usar checkout `feature/e02-control-safety-journal-recovery`. Development no espera E-02. No merge/deploy 063 sin 062 de E-02 en `master`. No E-06.

## Closure conditions

T01–T21 `[x]`; AC-01…AC-23; independent verifier PASS; S0 intacto; Lab BWC; no SQ/EF. E-05 CLOSED es sesión posterior al verifier. Este TOP no cierra E-05 ni lanza NORMAL.

## 🧩 Subproyectos

_No aplica — hijo de implementación de E-05; no crea Integration ni más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-ANALYTICS-CONVERGENCE-A0/TASKS.md`. Aquí sólo work packages. NORMAL no arranca hasta manager review.
> - [r] WP-TOP SPEC/PLAN/TASKS/VERIFICATION v1.0.1 + branch docs-only (reserva 063) #owner/agent #type/dev #area/echo
> - [x] WP-A Persistencia 063 + stores write-once (T01-T04, T16 PASS) #owner/agent #type/dev #area/echo
> - [x] WP-B Adapters Lab/journal (T05, T11, T12 PASS) #owner/agent #type/dev #area/echo
> - [x] WP-C Calculator fórmulas A0 (T06-T10, T20 PASS; 95.6% cov) #owner/agent #type/dev #area/echo
> - [x] WP-D Writer + lab-canonical-a0 (T13-T14 PASS PG real) #owner/agent #type/dev #area/echo
> - [x] WP-E Hasura SELECT (T15, T19; apply NOT_RUN flag) #owner/agent #type/dev #area/echo
> - [x] WP-F SOURCE/BWC/coverage cert (T17-T18, T21; 2 gates E-04 en TCR) #owner/agent #type/dev #area/echo

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

- **2026-09-13** — FULL INDEPENDENT VERIFIER #3 resolvió un checkout inicial incorrecto (E-02) y continuó tras validar el worktree canónico `/tmp/echo-e05-analytics-a0`: `HEAD == origin/feature == e917e25a`, worktree limpio, ancestry y master correctos. El checkout E-02 no fue modificado ni usado como evidencia.
- **2026-09-13** — Correction #2 posterior a `FULL RE-VERIFICATION #2`: `DecimalString` tenía ajuste `q+1` incondicional tras `QuoRem`, invirtiendo el signo en negativos y fallando `-1.2345678901235` → `-1.234567890122` en vez de `-1.234567890124`; tests previos carecían de boundary cases negativos de below-half, above-half, ties y tiny `q==0`. Se corrigió en `233e22bf` y se documentó en `e917e25a`; fórmulas y precisión intactas. Queda `IMPLEMENTATION CORRECTED — READY FOR FULL RE-VERIFICATION #3`; no verifier, no merge/deploy. Interlock 063 espera 062 de E-02 integrado en `master`.
- **2026-09-13** — Corrección focalizada post-`VERIFICATION_FAIL`: se eliminó la inferencia de currency Lab del builder `canonical_a0.go` y se agregaron casos A–E en `canonical_a0_test.go`. PG 17.11 físico, analytics, writer/stores, builders/repo y gates históricos E-04 PASS. Correction SHA `eb3cebf0`; estado: READY FOR FULL RE-VERIFICATION. Ver `specs/FEAT-ANALYTICS-CONVERGENCE-A0/VERIFICATION.md`; no verifier relanzado.
- **2026-09-13** — FULL RE-VERIFICATION #2 independiente contra `d40153f3`: pre-flight exacto y source scope PASS; suites Go relevantes PASS; adversarial `DecimalString` negativo FAIL por ajuste de signo en redondeo half-even. Se actualizó `VERIFICATION.md` con repro, severidad, alcance, corrección requerida y matriz AC al stop; E-05 no es certificable, no está READY FOR INTEGRATION y no se tocó product source.
- **2026-09-13** — Independent verifier one-shot sobre `baa2e305` detuvo en source: `RunCanonicalA0` copia la única moneda de filas Lab a `MetricDefaults.Currency` aunque USD puede ser default no probado y el adapter marca `CURRENCY_UNPROVEN`. Ver `specs/FEAT-ANALYTICS-CONVERGENCE-A0/VERIFICATION.md` sección `INDEPENDENT VERIFIER`. Verdict `VERIFICATION_FAIL`; no se aplicaron fixes ni se ejecutaron gates físicos posteriores.
- **2026-09-13** — Manager source review PASS funcional; se encontró stale E-04 SOURCE gate medido contra HEAD actual. Corrección focalizada: `e03DevelopmentBaseline` `fac48051` → `e04IntegratedBaseline` `a99f9a63` en `ingestion_noneffects_test.go`; `NoContractsDelta`, `NoMigrationDelta` y `AllowedFilesOnly` auditan E-03→E-04. Los dos gates originalmente fallidos PASS, anti-masking PASS y allowlist histórico sin paths E-05. Regresión Go E-04 PASS; SQL BWC no ejecutable por falta de `psql`; Hasura sin apply 063. Estado: IMPLEMENTATION READY FOR INDEPENDENT VERIFIER; E-04 no se reabre como desarrollo activo.
- **2026-09-12** — TOP CORRECTION v1.0.1 reserva de migración @ `dd1f2da9`: E-02 owner de `062_journal_quarantine`; E-05 cambia a `063_analytics_convergence_a0` exclusiva; 064+ fuera de scope. E-02 no bloquea development/implementation/verification. Merge/deploy de 063 serializa tras 062 en `master`. Semántica analítica 1.0.0 intacta. Docs-only; master intacto `a99f9a63`. Puente E-05 permanece Review.
- **2026-09-12** — TOP planning one-shot: subproyecto materializado; SPEC/PLAN/TASKS/VERIFICATION v1.0.0 @ `be87f11e` pusheados a `origin/feature/e05-analytics-convergence-a0` desde `a99f9a63` (docs-only; master intacto). Source Lab + S0 + Hasura/PG Aranea READ reconciliados. A0 = paths nuevos + adapters; no big bang; no SQ/EF. Puente E-05 → Review. No NORMAL.

## 🧭 Decisiones (ejecución, no semántica nueva)

- Hijo de implementación de E-05; ownership sigue en [[Echo — Live Platform V1]], no Integration.
- Persistencia mínima: 3 tablas + 2 vistas; Metric no es entidad global. Migración `063_analytics_convergence_a0` exclusiva E-05; `062_journal_quarantine` reserva E-02; 064+ fuera de scope.
- Sin FK a 061; refs S0 en JSON.
- Calculator Go; no SQL como autoridad de fórmula; no frontend.
- R AUTO / edge_score / INNER JOIN / version NULL → adapter-only.
- `execution.missing_ratio` COMPUTED es E-09.

## 🔗 Docs / Links

- [[Echo — Live Platform V1]]
- [[Echo — Producto Integrado]]
- [[Echo — E-01 Canonical SDK Foundation S0]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]
- [[echo-core]]

## 💡 Ideas

### Backlog de ideas

- Apply 063 a Aranea DEV es deuda ops post-verifier, no gate de CONTRACT; el apply/deploy real espera 062 de E-02 en `master`.

### Motivos / principios

- Mismo nombre ≠ misma métrica. Lab se proyecta; no se canoniza por intuición.

### Memoria pública / interna

- **Memoria pública:** contratos enlazados + SPEC del repo.
- **Memoria interna:** continuidad en esta nota.
- **Motivo:** Discovery conserva historia; este hijo es HOW/ORDER/GATES.
