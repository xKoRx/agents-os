---
type: project
schema_version: 1
owner: agent
root: false
status: done
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge — Factory V2 Completion]]"
sprint:
start: 2026-09-08
due:
progress: 100
repo: xKoRx/symphony
jira:
prs:
aliases:
  - F-02 Finalist Model V2
  - Echo Forge F-02 implementation
  - C1 C2 Finalist V2
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-08"
updated: "2026-09-08"
---

# Echo Forge — F-02 Finalist Model V2

%% Naming: Echo Forge — F-02 Finalist Model V2 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — F-02 Finalist Model V2
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo Forge — Factory V2 Completion]] · **Repo:** `xKoRx/symphony`
> Subproyecto de implementación de la fase F-02 (C1+C2). No es un roadmap independiente. Contrato: [[Echo Forge — F-02 Finalist Model V2 Contract]].

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo Forge — Factory V2 Completion]] enlaza esta fase. El humano sigue el track desde [[Echo — Producto Integrado]].

## 🎯 Objetivo

Reemplazar membresía V1 (copia de `TopProjection`) por membership estructural V2: Promotion `finalist_promotion@2.0.0`, warnings no destructivos, gate requested vs HTM, Campaign BWC con rank/score nullable, Result v2, historia V1 readable. C1 y C2 en un solo paquete. Desbloquea F-04/F-05 membership exacta sin reabrir F-01/F-03/S0/B1/B2.

## 📊 Estado actual

- **PASS / CLOSED (2026-09-08).** Manager ordenó integración: `feature/f02-finalist-model-v2` mergeada ff-only a `master`; F-02 commit final `c3b7ede4da5caa5f3294533b0dcf5e8570369c38` == `origin/master` en el momento del merge, pushed. Gate G1 cerrado. T1.1→T1.6 DONE.
- Tras la integración, `master` avanzó a `e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48` con un commit separado `chore(deploy)` que registra el manifest de release `0.2.96` publicado (rescate del dirty tree local, sin mezclar con `c3b7ede`).
- Verificación de integración: `go test -count=1` `sqx/core/domain` + `sqx/core/forge` PASS; build `./sqx/...` OK excluyendo baseline preexistente (`sqx/tools` multi-main, zmq4 sin libzmq del entorno).
- Baseline source: `xKoRx/symphony@0509342439cfbaa048839088787458dde1ed1b05` == `origin/master` (fetch verificado pre-merge). Dirty foráneo clasificado y limpiado en la misma sesión de integración.
- `DATABASE MIGRATION: 014_finalist_promotion_v2` (policy 2.0.0 + first_rank/first_score_ref nullable). `GOD REQUIRED: NONE`.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `feature/f02-finalist-model-v2` (integrada) | `0509342439cfbaa048839088787458dde1ed1b05` | [[Echo Forge — Factory V2 Completion]] F-02 | [[Echo Forge — F-02 Finalist Model V2 Contract]] | **PASS / CLOSED** — F-02 commit `c3b7ede4da5caa5f3294533b0dcf5e8570369c38` mergeado ff-only y pushed |

## Parent / SPEC / baselines

- Parent: [[Echo Forge — Factory V2 Completion]]
- SPEC: [[Echo Forge — F-02 Finalist Model V2 Contract]] — `VAULT_ROOT/30-resources/applications/Echo Forge — F-02 Finalist Model V2 Contract.md`
- Frozen: [[2026-09-06-echo-forge-finalist-model-v2]]; V1 [[2026-08-30-finalist-promotion-v1-core]]; Campaign [[2026-08-31-forge-campaign-stop-policy-v1-contract]]; SDK G01–03/G11–12/G22

## Source map

Promotion V1: `sqx/activities/worker/rank_snapshot_activity.go` (`FinalistPromotionActivity.Execute`, `promotionFinalists`, `validatePromotionSnapshot`, `buildFinalistPromotionDecision`); `sqx/core/domain/decision.go` (`FinalistPromotionPolicyVersion`, `validateFinalistPromotionV1`, `FinalistPromotionOutput`).

Ranking: `sqx/core/domain/ranking_snapshot.go` (`BuildRankingSnapshot`, `Eligible`, `TopProjection`). Score: `sqx/core/evaluation/mt5_fidelity.go` (`instrument_mismatch` SQX↔MT5); `sqx/activities/worker/mt5_score_shadow_activity.go`.

Identity HTM: `sqx/activities/worker/mt5_reconcile_activity.go`; `sqx/adapters/mt5/report/parse.go` (`Settings.Symbol`, `Timeframe`); `sqx/workflows/generic_workflow.go` (`persistMT5ReconcileV1` aborta Generic; `collectMT5ArtifactChildren` dropea child fail; `runFinalistPromotion`).

Campaign: `sqx/core/domain/forge_campaign.go` (`first_rank` int; `BuildForgeCampaignStopEvaluation`); `sqx/adapters/registry-postgres/forge_campaign.go` (`firstObservedFinalists`, `reconcileCampaignFinalists`); `sqx/adapters/registry-postgres/forge_campaign_result.go`; migrations `009`, `011`, `013` last.

Result: `sqx/core/forge/result.go` (`crossCheckPromotion`); `sqx/core/domain/forge_result.go`. Config: `sqx/core/runtime/mt5_task_config.go` (`validatePromotion` pin 1.0.0 + `top_n`).

## Requirement-to-evidence

| Req | State | Evidence |
|---|---|---|
| Membership ≠ Top N | missing | `promotionFinalists` copies TopProjection |
| NOT_COMPARABLE can be Finalist | missing | ranking Eligible=false → no Top entry |
| requested vs HTM gate | missing | reconcile no Spec vs Symbol compare; fidelity mismatch is Score |
| V1 history readable | done | `validateFinalistPromotionV1`; unique flow_run |
| Campaign unique StrategyRef | partial | counts Finalists; cannot store null rank |
| Result V1 equality | done for V1 / blocked for V2 | `crossCheckPromotion` |
| Nullable rank SQL | missing | `011` NOT NULL |
| Policy 2.0.0 SQL | missing | `009` ck 1.0.0 only |

## Decision register

| ID | status | resolution | source | phase |
|---|---|---|---|---|
| D1 membership authority | TECHNICAL_RESOLUTION | Decision FINALIST_PROMOTION output.Finalists; producer V2 = structural cohort not TopProjection | SPEC + `firstObservedFinalists` | 1 |
| D2 include/exclude | TECHNICAL_RESOLUTION | include: success HTM+reconcile+NativeMetricSet+lineage+requested==observed; exclude identity mismatch/missing observed/child fail; NOT_COMPARABLE/INVALID_INPUT include | SPEC | 1 |
| D3 identity vs Generic abort | TECHNICAL_RESOLUTION | mismatch = typed result + per-candidate drop; infra reconcile/score error still aborts Generic | `persistMT5ReconcileV1` vs `collectMT5ArtifactChildren` | 1 |
| D4 warnings | TECHNICAL_RESOLUTION | PERIOD_MISMATCH, FIDELITY_NOT_COMPARABLE, PNL_SIGN_FLIP; no FIDELITY_SCORE_LOW | frozen V2 | 1 |
| D5 NOT_COMPARABLE | TECHNICAL_RESOLUTION | Finalist, no rank, keep ScoreRef, Eligible stays false | ranking_snapshot.go + SPEC | 1 |
| D6 Campaign read | TECHNICAL_RESOLUTION | unique StrategyRef of Decision Finalists; counts NOT_COMPARABLE; Stop Policy fields untouched | forge_campaign.go | 1 |
| D7 BWC | TECHNICAL_RESOLUTION | Validate V1 intact; activity dual-dispatch by PolicyVersion; new configs emit 2.0.0 | decision.go | 1 |
| D8 migration | TECHNICAL_RESOLUTION | `014_finalist_promotion_v2` not NONE | 009/011 frontier | 1 |

## Planned diff

Modificar C1: `sqx/core/domain/decision.go`; `decision_test.go`; `rank_snapshot_activity.go`; `rank_snapshot_activity_test.go`; `sqx/core/domain/forge_result.go`; `sqx/core/forge/result.go`; `result_test.go`; `sqx/core/runtime/mt5_task_config.go`; `mt5_task_config_test.go`; `sqx/workflows/generic_workflow.go`; `sqx/activities/worker/mt5_reconcile_activity.go`; `mt5_reconcile_activity_test.go`.

Modificar C2: `sqx/core/domain/forge_campaign.go`; `forge_campaign_test.go`; `sqx/adapters/registry-postgres/forge_campaign.go`; `forge_campaign_result.go`; `migrations/runner.go`; `forge_campaign_integration_test.go`.

Crear: `sqx/adapters/registry-postgres/migrations/014_finalist_promotion_v2.up.sql`; `014_finalist_promotion_v2_test.go`; tests V2 nuevos en paquetes anteriores (no debilitar asserts V1). `TEST_CHANGE_REQUEST` si un test V1 existente pinnea igualdad membership↔TopProjection sobre el path productivo 2.0.0.

## No-touch

F-01 identity/publication. F-03 SQX timeouts. F-04 magic/seal/handoff. F-05. S0 Echo. B1A/B1B/B2. Slot Pool/fencing. `ranking-snapshot.v1` schema/`Eligible` semantics. Stop Policy fields. Rewrites de Decisions históricas. `FIDELITY_SCORE_LOW`. Score algorithm weights. Foreign dirty symphony.

## Execution sequence

T1.1 domain V2 → T1.2 identity gate drop → T1.3 promotionFinalistsV2 + warnings → T1.4 result v2 → T1.5 config 2.0.0 without top_n → T1.6 Campaign nullable + 014. No T1.3 sin T1.1. No T1.6 sin T1.3.

## Dependencies

B2 CLOSED freeze. Independiente de F-01/F-03/E-01. No S0.

## ✅ Tareas

> [!note]+ Ownership
> Board `#owner/agent`. Cada ítem es una TASK atómica para NORMAL tras autorización del manager.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] T1.1 Domain Decision/output V2 y Validate dual #owner/agent #type/dev #area/echo
> - [x] T1.2 Reconcile requested vs HTM + drop per-candidate #owner/agent #type/dev #area/echo
> - [x] T1.3 Promotion V2 membership y warnings #owner/agent #type/dev #area/echo
> - [x] T1.4 Result Surface v2 sin igualdad TopProjection #owner/agent #type/dev #area/echo
> - [x] T1.5 Config/workflow 2.0.0 sin exigir top_n #owner/agent #type/dev #area/echo
> - [x] T1.6 Campaign nullable rank/score y migration 014 #owner/agent #type/dev #area/echo

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

## Atomic tasks

Contrato de cada TASK: objetivo, archivos, entrada, cambio, invariantes, tests, DONE, deps, stop. Diseño: sólo la SPEC.

### T1.1 Domain Decision/output V2 y Validate dual

- **Modelo:** NORMAL
- **Objetivo:** tipos y Validate V2 sin romper Validate V1.
- **Archivos/símbolos:** `sqx/core/domain/decision.go` (`FinalistPromotionPolicyVersion` intacta; añadir `FinalistPromotionPolicyVersionV2`, `FinalistPromotionModeV2`, `FinalistPromotionOutputSchemaV2`, `FinalistPromotionStageProducerV2`, reasons `STRUCTURAL_EMPTY`/`STRUCTURAL_PROMOTED`, `FinalistPromotionOutputV2`, `FinalistPromotionEntry` V2 con `Rank *uint64`, `ScoreRef` opcional, `Warnings []string`; `Decision.Validate` branch 1.0.0 vs 2.0.0; `FinalistPromotionPolicyConfigDigestV2`/`PolicyRefV2`/`ContentDigestV2`/`NewFinalistPromotionDecisionRef` reusa fórmula con policy 2.0.0); `decision_test.go` tests nuevos V2 + existentes V1 verdes.
- **Entrada:** V1 rank==0 inválido; policy pin 1.0.0.
- **Cambio:** dual Validate. JSON v2 omitempty rank/score. Rank presente implica >0. Warnings sólo del enum SPEC. Zero-supply v2: sin evidence snapshot, STRUCTURAL_EMPTY, finalists `[]`.
- **Invariantes:** bytes V1 ContentDigest/Ref inalterados para fixtures 1.0.0.
- **Tests:** `TestValidate_FinalistPromotionV1_Unchanged`; V2 NOT_COMPARABLE entry sin rank; V2 rank 0 inválido si pointer a 0; V2 warnings ilegales rechazados; dual policy digest distinto 1 vs 2.
- **DONE:** `go test ./sqx/core/domain` verde; V1 tests sin asserts relajados.
- **Deps:** ninguna.
- **Stop:** si hace falta mutar RankingSnapshot schema → BLOCKED.

### T1.2 Reconcile requested vs HTM + drop per-candidate

- **Modelo:** NORMAL
- **Objetivo:** gate estructural requested==observed; mismatch no aborta Generic.
- **Archivos/símbolos:** `mt5_reconcile_activity.go` (`Execute` post-`report.Parse`; `MT5ReconcileResult.StructuralIdentity`); `mt5_reconcile_activity_test.go`; `generic_workflow.go` loop `persistMT5ReconcileV1`/`scoreMT5ShadowV1` (si identity ≠ Match: no score, no ScoreBinding, continuar cohort); tests workflow del drop si ya hay harness; si no, unit activity + función extraída testeable.
- **Entrada:** Spec.Instrument/Timeframe vs `Settings.Symbol`/`Timeframe` + `CanonicalSymbol`/`CanonicalTimeframe`.
- **Cambio:** persist Evaluation igual. Result typed Match/InstrumentMismatch/TimeframeMismatch/ObservedMissing. Activity error **prohibido** para identity. Missing observed = exclude.
- **Invariantes:** parser/store errors siguen abortando. Child backtest fail sigue drop. Identity mismatch no es warning.
- **Tests:** XAUUSD/H1 requested vs EURUSD HTM → Identity InstrumentMismatch, Evaluation persistida, Execute err==nil; vs M15 → TimeframeMismatch; match → Score path; Generic con 2 success HTM y 1 mismatch → 1 scored candidate, workflow COMPLETED.
- **DONE:** identity drop cubierto; ningún test convierte mismatch en `t.Skip`.
- **Deps:** ninguna (puede paralelo a T1.1).
- **Stop:** si identity exige error Temporal non-retryable → PLAN_CONFLICT.

### T1.3 Promotion V2 membership y warnings

- **Modelo:** NORMAL
- **Objetivo:** `promotionFinalistsV2` = Candidates del snapshot (cohort scored post-gate), no TopProjection; warnings SPEC; activity dual 1.0.0/2.0.0.
- **Archivos/símbolos:** `rank_snapshot_activity.go` (`promotionFinalists` V1 intacta; añadir `promotionFinalistsV2`; `validatePromotionSnapshot` V2 sin exigir TopProjection.Configured; `validateFinalistPromotionRequest` acepta 1.0.0 y 2.0.0; `buildFinalistPromotionDecision` branch; replay COMPLETED usa la misma función de version); `rank_snapshot_activity_test.go`.
- **Entrada:** T1.1 DONE. Snapshot.Candidates incluye NOT_COMPARABLE.
- **Cambio:** V2 Finalists = todos Candidates ordenados por StrategyRef; Rank/ScoreRef desde OrderedEntries si Eligible COMPUTED; si no, rank omitido y ScoreRef del candidate. Warnings: period_* → PERIOD_MISMATCH; otros NOT_COMPARABLE → FIDELITY_NOT_COMPARABLE; ambos net_profit finitos signos distintos → PNL_SIGN_FLIP (leer Score evidence ya cargada para ranking, no recompute fidelity). Reason STRUCTURAL_PROMOTED si len>0 aunque TopProjection.Effective=0. Zero-supply V2 STRUCTURAL_EMPTY. Producer contract V2 en stage intent.
- **Invariantes:** path 1.0.0 sigue copiando TopProjection y exigiendo configured top_n. Ranking Eligible no se muta.
- **Tests:** 3 Candidates (2 NOT_COMPARABLE period, 1 COMPUTED fuera de top_n=1) → 3 Finalists V2, 1 con rank, 2 con PERIOD_MISMATCH; V1 mismo snapshot → 1 Finalist; replay ACK; G02 no rank dummy.
- **DONE:** membership V2 ≠ Top N; V1 tests de promotion existentes verdes o TEST_CHANGE_REQUEST explícito.
- **Deps:** T1.1.
- **Stop:** si hay que setear Eligible=true → BLOCKED.

### T1.4 Result Surface v2 sin igualdad TopProjection

- **Modelo:** NORMAL
- **Objetivo:** result v2 proyecta membership estructural; V1 `crossCheckPromotion` sólo policy 1.0.0.
- **Archivos/símbolos:** `sqx/core/domain/forge_result.go` (`ForgeResultSchemaVersionV2`, `ForgeFinalist` rank/score/warnings opcionales); `sqx/core/forge/result.go` (`applyPromotion`, `crossCheckPromotion` guard PolicyVersion, decode output v1 vs v2); `result_test.go` casos V2 + V1 igualdad intacta.
- **Entrada:** T1.3 DONE.
- **Cambio:** selector schema por PolicyVersion. V2 INCONSISTENT sólo si snapshot binding diverge, no si len(Finalists)!=len(TopProjection).
- **Invariantes:** query V1 histórico sigue v1 + igualdad.
- **Tests:** snapshot TopN=1 / 3 Finalists V2 → AVAILABLE no INCONSISTENT; V1 mismatch sigue INCONSISTENT; zero-supply v2 empty.
- **DONE:** G01/G02/G22 surface; V1 result_test de igualdad verde.
- **Deps:** T1.3.
- **Stop:** si GetResult reescribe Decision → BLOCKED.

### T1.5 Config/workflow 2.0.0 sin exigir top_n

- **Modelo:** NORMAL
- **Objetivo:** configs nuevas emiten y validan `finalist_promotion@2.0.0` sin `ranking.top_n`; 1.0.0 conserva top_n.
- **Archivos/símbolos:** `mt5_task_config.go` `validatePromotion`; emisores productivos de `PromotionSpec.Version` (el constructor/intake que hoy asigna `FinalistPromotionPolicyVersion`, no fixtures de test); `generic_workflow.go` `runFinalistPromotion` ya transporta spec.Version; tests `mt5_task_config_test.go` / intake Campaign.
- **Entrada:** T1.3. Hoy pin 1.0.0 + top_n required.
- **Cambio:** 2.0.0: source ranking exacto, top_n opcional. 1.0.0: comportamiento actual. Productive new Campaign/MT5 spec → 2.0.0. Stage producer V2 ya en T1.3.
- **Invariantes:** configs históricas 1.0.0 siguen válidas.
- **Tests:** 2.0.0 sin top_n Validate OK; 1.0.0 sin top_n sigue error; 2.0.0 policy id distinta rechazada.
- **DONE:** intake nueva no puede crear 1.0.0 por default.
- **Deps:** T1.3.
- **Stop:** si el único emisor es un test helper → PLAN_CONFLICT, no “arreglar” tests para emitir V1 como productivo.

### T1.6 Campaign nullable rank/score y migration 014

- **Modelo:** NORMAL
- **Objetivo:** Campaign cuenta unique StrategyRef estructurales; persiste rank/score null; Stop Policy intacta.
- **Archivos/símbolos:** `014_finalist_promotion_v2.up.sql`; `migrations/runner.go` `ordered`; `014_finalist_promotion_v2_test.go`; `forge_campaign.go` domain `FirstRank *int` / `FirstScoreRef` opcional y result JSON omitempty; `registry-postgres/forge_campaign.go` `firstObservedFinalists`, Scan NULL, INSERT NULL; `forge_campaign_result.go`; `forge_campaign_integration_test.go`; `validateForgeCampaignPromotion` acepta output v2.
- **Entrada:** T1.3 DONE. `011` NOT NULL.
- **Cambio:** SQL SPEC. first-wins no pisa null con rank posterior. ORDER BY `first_rank NULLS LAST`. effective_unique incluye NOT_COMPARABLE. Policy SQL 2.0.0. No rewrite filas V1.
- **Invariantes:** Stop evaluation formula intacta. Failure codes Promotion missing intactos.
- **Tests:** insert finalist sin rank; target_finalists=1 con un NOT_COMPARABLE STRUCTURAL_PROMOTED → STOP TARGET_REACHED; V1 row rank>0 roundtrip; ck policy 2.0.0 insert Decision; 3.0.0 rechazado; G22 zero POST no aplica aquí — Campaign empty CONTINUE/MAX_WAVES.
- **DONE:** `go test` registry-postgres migrations + forge_campaign (+ integration si harness; si initdb DEGRADED, documentar como F-01, no fingir PASS).
- **Deps:** T1.3.
- **Stop:** si 014 exige rewrite de Decisions V1 → BLOCKED.

## Gates

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G1 | review | T1.1–T1.6 según SPEC; diff acotado + tests G01–03/G11–12/G22 + 014 | Manager review; no auto-merge | F-02 implementation review; no F-03/F-04 |

## Tests / certification

Suite por task. Final: domain dual Validate; identity drop; promotion V2 vs V1 mismo snapshot; result v2 no igualdad; config 2.0.0; campaign null rank + stop count; `go test -race` paquetes tocados. Cert: SOURCE + CONTRACT G01–03/G11–12/G22. PHYSICAL recert sólo promotion/reconcile identity. No flota MT5 ownership.

## Risks

- Tests V1 de result/promotion fallarán si el default productivo cambia a 2.0.0 sin dual-dispatch: T1.3/T1.5 deben preservar path 1.0.0.
- Harness Postgres puede degradar 014 integration: no PRODUCT PASS con mocks de CHECK.
- Confundir `instrument_mismatch` de Score con gate requested-vs-HTM.
- `PNL_SIGN_FLIP` requiere leer Score evidence en Promotion; si el ranking activity no carga Value/components, T1.3 debe LoadScore no inferir.

## Definition of Done

SPEC cumplida. Migration 014 aplicada en runner. Flujos nuevos 2.0.0 estructurales. V1 history readable. Zero finalists honesto. NOT_COMPARABLE no expulsa. Identity mismatch no aborta Generic. Foreign dirty intacto. Sin NORMAL antes de autorización.

## Unlocks

F-04 membership exacta en handoff. F-05 golden nonempty estructural. F-03 no bloquea.

### Paquete autónomo Fase 1 — Finalist Model V2 (C1+C2)

**Misión exacta**

Implementar T1.1–T1.6 contra [[Echo Forge — F-02 Finalist Model V2 Contract]] en baseline `0509342439cfbaa048839088787458dde1ed1b05`, sin reabrir ranking Eligible ni Stop Policy.

**Precondiciones verificables**

Manager aceptó esta nota + SPEC. Symphony `origin/master` revalidado = baseline o STOP. Foreign dirty preservado. NORMAL autorizado explícitamente. Hoy: **no autorizado**.

**Lectura obligatoria**

`VAULT_ROOT/30-resources/applications/Echo Forge — F-02 Finalist Model V2 Contract.md`

`VAULT_ROOT/10-projects/Echo/agentes/Echo Forge — F-02 Finalist Model V2.md`

`VAULT_ROOT/80-agents/memory/public/decision/symphony/2026-09-06-echo-forge-finalist-model-v2.md`

Source map de esta nota. No redescubrir membership como Top N.

**Decisiones cerradas**

Ver SPEC y decision register. Membership = Decision Finalists estructurales. Identity gate en reconcile con drop per-candidate. Migration 014. Dual policy 1.0.0/2.0.0.

**Implementación paso a paso**

Ejecutar T1.1 → T1.2 (paralelo a T1.1 permitido) → T1.3 → T1.4 y T1.5 → T1.6. Actualizar esta nota al avanzar. No despachar F-03/F-04.

**Archivos esperados**

modify/create: Planned diff. no-touch: lista No-touch.

**No tocar**

F-01, F-03, F-04, F-05, S0, B1/B2, RankingSnapshot Eligible, Stop Policy fields, Decisions históricas, foreign dirty.

**Spikes permitidos**

Ninguno de arquitectura. Si identity mismatch no puede expresarse sin error de activity: PLAN_CONFLICT y parar.

**Tests y asserts**

Los de T1.1–T1.6 y G01–03/G11–12/G22 de la SPEC. Prohibido t.Skip de G02/G11/G12.

**Entregables/Gate G1**

Diff acotado, tests, 014, nota en review. Gate G1 → review manager. No merge.

**Handoff a Fase N+1**

No hay fase 2 en este subproyecto. Handoff: F-02 DONE hacia el padre Factory V2.

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — Finalist Model V2 (C1+C2)
GATE_REQUERIDO=none
TAREAS=T1.1-T1.6
SALIDA=source diff F-02 + G01-03/G11-12/G22 + migration 014 + nota en review
STOP=NO NORMAL IMPLEMENTATION AUTHORIZED YET
```

El bloque de despacho no sustituye la SPEC ni autoriza ejecución.

## 📆 Bitácora

- **2026-09-08** — TOP diseñó F-02 contra symphony `0509342`. SPEC + TASKS persistidas. Migration 014 cerrada. NORMAL autorizado por manager.
- **2026-09-08** — Codex completó T1.1→T1.6 en `feature/f02-finalist-model-v2`, commit `c3b7ede`, push para manager review. Gates F-02 y migration brownfield PASS; sweep completo conserva fallos preexistentes fuera de scope (`sqx/tools`, workflow harness y algunos registry tests).
- **2026-09-08** — **PASS/CLOSED.** Manager ordenó integración: merge ff-only a `master` (`c3b7ede`) y push; worktree de symphony quedó limpio tras clasificar el dirty foráneo (5 restaurados, 4 RCA/CHANGE de la campaña C3 eliminados ya materializados/superseded en Agents OS, manifest `0.2.96` rescatado como commit separado `e50cb7e`). Desbloquea F-04 (membership exacta en handoff) y F-05 (golden nonempty estructural).

## 🧭 Decisiones

- Ver [[Echo Forge — F-02 Finalist Model V2 Contract]]. Esta nota no duplica la matriz.

## 🔗 Docs / Links

- [[Echo Forge — Factory V2 Completion]]
- [[Echo Forge — F-02 Finalist Model V2 Contract]]
- [[Echo — Producto Integrado]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[2026-09-06-echo-forge-finalist-model-v2]]

## 💡 Ideas

### Backlog de ideas

- Ninguna dentro de F-02.

### Motivos / principios

- Membership ≠ rank. Warning ≠ invalid. Fail-closed identity. V1 immutable.

### Memoria pública / interna

- **Memoria pública:** SPEC Resource + decisión finalist-model-v2.
- **Memoria interna:** no duplicar checkpoint.
- **Motivo:** el padre conserva el roadmap F-01…F-05.
