---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[2026-09-06-echo-forge-finalist-model-v2]]"
  - "[[2026-08-30-finalist-promotion-v1-core]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
  - "[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]"
  - "[[Echo Forge — Factory V2 Completion]]"
last_verified: "2026-09-08"
confidence: verified
aliases:
  - F-02 SPEC
  - Finalist Model V2 contract
  - Echo Forge F-02
  - C1 C2 Finalist V2
related:
  - "[[Echo Forge — F-02 Finalist Model V2]]"
  - "[[2026-08-30-echo-forge-finalist-promotion-v1]]"
entities:
  - "[[Echo Forge]]"
  - "[[xKoRx/symphony]]"
tags:
  - kind/resource
  - area/echo
  - project/echo-forge
created: "2026-09-08"
updated: "2026-09-08"
---

# Echo Forge — F-02 Finalist Model V2 Contract

Esta Resource es el contrato técnico de `F-02 — Finalist Model V2 (C1+C2)`. Define qué debe quedar cierto. La ejecución vive en [[Echo Forge — F-02 Finalist Model V2]]. No es un tutorial de implementación. C1 (membership/Promotion/result) y C2 (Campaign BWC/nullable rank) son milestones internos de una sola capacidad.

Baseline de source: `xKoRx/symphony@0509342439cfbaa048839088787458dde1ed1b05` (`origin/master` verificado 2026-09-08). Agents OS: fetch de `origin/master` no disponible en este workstation (vault sin `.git`, `gh` sin auth); último SHA durable registrado en vault: `f1070bec27db3ca415fe24f3c3576139674b7e09` (E-01 S0, 2026-09-08).

## Síntesis vigente

### Problema

`FinalistPromotionActivity.promotionFinalists` copia `RankingSnapshot.TopProjection.Entries`. Membresía V1 = ranking eligible (`ScoreComputed`) truncado por `top_n`. `ScoreNotComparable` / `ScoreInvalidInput` quedan en `Candidates` inelegibles y no entran a Promotion. Evidence C3/M6: periodos SQX vs MT5 distintos producen `NOT_COMPARABLE` y Promotion vacía `TOP_PROJECTION_EMPTY` pese a backtest físico válido.

`validatePromotion` exige `finalist_promotion@1.0.0` y `ranking.top_n`. `crossCheckPromotion` exige `Finalists ≡ TopProjection`. `ck_decisions_policy_v1` sólo admite `policy_version = 1.0.0`. `forge_campaign_finalists.first_rank` / `first_score_ref` son `NOT NULL` con `first_rank > 0`.

### Veredicto central

**Finalist V2 = membership estructural**, no Top N. Ranking ordena. `top_n` proyecta display. Warnings no admiten ni rechazan. `NOT_COMPARABLE` analítico puede seguir Finalist. Mismatch requested vs observed instrument/timeframe bloquea esa candidata y no es warning.

Autoridad de membership que lee Campaign: la Decision `FINALIST_PROMOTION` del FlowRun hijo (`output.Finalists`, unique `StrategyRef`, first-observation-wins). El productor de ese set en flujos nuevos es `promotionFinalistsV2` sobre el cohort estructural, no `TopProjection`.

## Cuatro conceptos separados

### Evaluation

Persistencia post-HTM: parse + normalize + reconcile con `NativeMetricSetRef` + lineage `StrategyRef`/`EX5`. No decide membresía de campaña. Identity requested vs observed se evalúa aquí.

### Score

Evidencia analítica `mt5_fidelity_shadow.v1`. Status `COMPUTED` | `NOT_COMPARABLE` | `INVALID_INPUT`. No muta lifecycle. No admite Finalist.

### Ranking

`RankingSnapshot.v1` intacto. `Candidates` = cohort scored. `Eligible=true` sólo `COMPUTED` finito. `OrderedEntries` / `TopProjection` = corte comparable. No se muta `Eligible` para `NOT_COMPARABLE`. Ranking ≠ membership.

### Finalist

Set de `StrategyRef` únicos que completan el boundary estructural y pasan el gate requested==observed. Persistido en Decision output v2. Campaign cuenta ese set.

## Membership V2 — include / exclude

**INCLUDE** (todos, conjunción):

1. Child MT5 backtest `ArtifactStatusSuccess` con HTM primary.
2. Reconcile ACK: parser HTM + normalize + Evaluation persistida + `NativeMetricSetRef` no vacío + lineage `StrategyRef`/`EX5` del carrier.
3. Requested `WorkflowSpec.Instrument` == observed HTM symbol tras `evaluation.CanonicalSymbol`.
4. Requested `WorkflowSpec.Timeframe` == observed HTM period/timeframe tras `evaluation.CanonicalTimeframe`.
5. Observed no missing en esas dos dimensiones.

**EXCLUDE (blocking, no warning, no Finalist):**

- Backtest child no-success (ya se dropea hoy en `collectMT5ArtifactChildren`).
- Parser/normalize/persist reconcile infra o contrato (HTM success sin primary, EX5 ausente, timezone vacía, PersistenceContractConflict, digest mismatch): aborta el Generic entero, igual que hoy. No es drop per-candidate.
- Requested vs observed instrument mismatch (`STRUCTURAL_MISMATCH` / G11).
- Requested vs observed timeframe mismatch (`STRUCTURAL_MISMATCH` / G12).
- Observed instrument o timeframe missing tras parse.

**NO EXCLUDE (siguen Finalist si el include estructural pasó):**

- Score `NOT_COMPARABLE` (period mismatch, sample/pnl_basis, metric_missing, fidelity SQX↔MT5 distinto de requested-vs-HTM).
- Score `INVALID_INPUT` (NaN/Inf) — ranking exclusion only; NativeMetricSet existe.
- Score `COMPUTED` bajo, `PNL_SIGN_FLIP`, ausencia de rank, `top_n` que los deja fuera de `TopProjection`.

`instrument_mismatch` / `timeframe_mismatch` **entre baseline SQX y candidate MT5** en `MT5FidelityComparabilityReasons` siguen siendo Score `NOT_COMPARABLE`, no el gate requested-vs-HTM. El gate estructural compara `req.Spec` vs HTM parsed (`report.Settings.Symbol` / `Timeframe`), no vs MetricSet SQX.

## Relación Evaluation / Score / Ranking / Finalist

```text
backtest success → reconcile persist → identity gate
  MATCH → score shadow → RankingSnapshot.Candidates
  MISMATCH → persist Evaluation (evidencia) → DROP de cohort de ranking (no ScoreBinding) → no Finalist
Ranking: COMPUTED → OrderedEntries + TopProjection; NOT_COMPARABLE/INVALID → Candidates ineligible
Promotion V2: Finalists = Candidates que pasaron identity (todo el cohort scored restante), no TopProjection
Campaign: unique StrategyRef(Finalists) first-wins; rank/score nullable
```

Zero-supply (batch vacío antes de ranking) permanece: Decision COMPLETED, finalists `[]`, reason estructural empty, sin RankingSnapshotRef.

## Requested instrument/timeframe validation

Dónde: `MT5ReconcileActivity.Execute` después de `report.Parse` y antes de Score. Comparar `CanonicalSymbol(parsed.Settings.Symbol.Text)` vs `CanonicalSymbol(req.Spec.Instrument)` y `CanonicalTimeframe(parsed.Settings.Timeframe.Text)` vs `CanonicalTimeframe(req.Spec.Timeframe)`. Missing observed o desigual → `StructuralIdentity = InstrumentMismatch | TimeframeMismatch` en `MT5ReconcileResult`. Persist Evaluation/NativeMetricSet igual (evidencia de lo ejecutado). Activity **no** retorna error de identity: un error abortaría Generic (`persistMT5ReconcileV1` hoy `return current, err`).

Workflow (`generic_workflow.go` loop sobre `preserved` success): si `StructuralIdentity != Match`, no llamar `scoreMT5ShadowV1`; no dejar ScoreBinding; esa Strategy no entra a `runGlobalRankingSnapshots`. Fail-closed per-candidate, simétrico al drop de child backtest.

Case D cerrado: identity mismatch = drop per-candidate. Reconcile/score **infra/contrato** = abort Generic. Child backtest failure = drop (ya existe).

## Warning vs invalid / blocking

Warnings: diagnósticos tipados, deterministas, no destructivos, bound a `StrategyRef` + Score/comparability. No cambian membership.

| Code | Cuándo | Membership |
|---|---|---|
| `PERIOD_MISMATCH` | Score reasons contienen `period_start_utc_mismatch` o `period_end_utc_mismatch` | INCLUDE |
| `FIDELITY_NOT_COMPARABLE` | Score `NOT_COMPARABLE` por otra reason de comparability (no period, no requested-vs-HTM) | INCLUDE |
| `PNL_SIGN_FLIP` | ambos `net_profit` finitos y signos distintos (COMPUTED o componentes finitos) | INCLUDE |

Prohibido inventar `FIDELITY_SCORE_LOW` o umbrales de desviación. `PNL_SIGN_FLIP` no existe en source; F-02 lo añade en Promotion V2 leyendo componentes/valores de Score, no en el algoritmo de fidelidad (ese algoritmo no se reabre).

Blocking ≠ warning: identity requested-vs-HTM, parser fail, persist conflict, missing NativeMetricSetRef en un success path, abort infra.

## NOT_COMPARABLE

Puede ser Finalist. Sin rank numérico. `ScoreRef` se conserva (evidencia). `RankingCandidate.Eligible` permanece `false`. No dummy rank 0. No mutar snapshot. Reason de Promotion nonempty si hay ≥1 Finalist estructural, incluso si `TopProjection.Effective=0`.

## Idempotencia y retries

Igual que V1 sobre authorities nuevas:

- Unique `FINALIST_PROMOTION` per FlowRun.
- `PutDecision` ACK identical digest; CONFLICT distinct.
- Stage COMPLETED: `LoadFinalistPromotion` debe coincidir Ref/ContentDigest/StageExecutionRef; si no, `PersistenceContractConflict` non-retryable.
- `PersistenceUnknownCommit` → recovery read, retryable, no segundo mint.
- Retry técnico mismo `ExecutionIntentKey` (Generation 1, TaskPath estructural). Producer contract V2 cambia StageInstanceKey vs V1: flujos nuevos no reconvergen con stages V1.
- Identity drop no mint Score ni Promotion entry. Replay del mismo HTM mismatch converge al mismo drop.
- Temporal retry no reconstruye Decision con timestamps distintos: ContentDigest V2 excluye `CreatedAt` igual que V1.

## Persistencia y BWC V1/V2

| Superficie | V1 (histórico) | V2 (flujos nuevos) |
|---|---|---|
| Policy | `finalist_promotion@1.0.0` `TOP_PROJECTION` | `finalist_promotion@2.0.0` `STRUCTURAL_MEMBERSHIP` |
| Output schema | `sqx-finalist-promotion-output.v1` | `sqx-finalist-promotion-output.v2` |
| Stage producer | `sqx-finalist-promotion.v1` | `sqx-finalist-promotion.v2` |
| Reasons | `TOP_PROJECTION_EMPTY` / `TOP_PROJECTION_PROMOTED` | `STRUCTURAL_EMPTY` / `STRUCTURAL_PROMOTED` |
| Rank | `uint64` > 0 obligatorio | omit/null si no comparable |
| ScoreRef | SHA obligatorio por entry | omit/null si no hay Score (zero-supply); presente si hay Candidate scored |
| Result | `forge-result.v1` + `crossCheckPromotion` igualdad | `forge-result.v2`; binding snapshot sí; igualdad membresía↔TopProjection no |
| Constantes Go | `FinalistPromotionPolicyVersion` permanece `"1.0.0"` | añadir `FinalistPromotionPolicyVersionV2 = "2.0.0"`; no reasignar la V1 |

`Decision.Validate()`: `PolicyVersion==1.0.0` → `validateFinalistPromotionV1` byte-compatible; `2.0.0` → `validateFinalistPromotionV2`. Histórico no se reescribe. Un flow nuevo no puede etiquetarse 1.0.0 para “downgrade”: configs productivas nuevas emiten 2.0.0. Activity acepta ambas versiones y despacha membership V1 o V2 según `PromotionSpec.Version`.

`ranking-snapshot.v1` no se muta. `finalist_promotion@1.0.0` / output v1 / result v1 permanecen legibles.

## Qué lee Campaign para contar finalists

Sin reabrir Stop Policy:

1. Tras cada child COMPLETED, `LoadFinalistPromotion` + `validateForgeCampaignPromotion` (acepta output v1 y v2).
2. `firstObservedFinalists`: unique `StrategyRef` de `output.Finalists`, first-wave-wins.
3. `effective_unique_finalists = len(that set)`.
4. `BuildForgeCampaignStopEvaluation` compara contra `target_finalists` / `max_waves` (precedencia TARGET_REACHED > MAX_WAVES_REACHED > CONTINUE).

NOT_COMPARABLE estructuralmente incluido **cuenta** para `target_finalists`. Top N / comparable count no. `first_rank` / `first_score_ref` nullable en filas nuevas; first-observation no se actualiza si una wave posterior trae rank.

## Failure / conflict semantics

| Clase | Señal | Retry | Membership |
|---|---|---|---|
| valid replay Promotion | ACK identical Decision | sí, no-op | misma |
| unknown commit | PersistenceUnknownCommit | recovery read | no mint |
| contract conflict Decision | digest/evidence distinct | no | no |
| identity mismatch | StructuralIdentity ≠ Match | n/a per candidate | exclude |
| backtest child fail | ArtifactStatus ≠ Success | no (child policy) | exclude |
| reconcile/score infra | activity error | Temporal retry / abort Generic | n/a |
| Score NOT_COMPARABLE | status durable | n/a | include |
| zero Finalists honest | STRUCTURAL_EMPTY | n/a | `[]`; Campaign CONTINUE si max_waves no alcanzado |
| Promotion missing/inconsistent | Campaign failure codes actuales | no | Campaign FAILED (no reabrir) |
| cancellation | cancel árbol | no | no |

## Migración — `014_finalist_promotion_v2`

**No es NONE.** Source frontier: última migration `013_forge_campaign_replenishment_policy.up.sql`. `011` crea `forge_campaign_finalists` con `first_rank integer NOT NULL CHECK (first_rank > 0)` y `first_score_ref text NOT NULL`. `009` `ck_decisions_policy_v1` exige `FINALIST_PROMOTION` → `policy_version = '1.0.0'`. Sin SQL, V2 no puede persistir Decision 2.0.0 ni Campaign finalists sin rank.

Archivo: `sqx/adapters/registry-postgres/migrations/014_finalist_promotion_v2.up.sql`. Registrar en `ordered` de `runner.go`.

Propósito exacto (aditivo, sin rewrite de filas V1):

1. Reemplazar `ck_decisions_policy_v1` para permitir `policy_version IN ('1.0.0','2.0.0')` en `FINALIST_PROMOTION`; optimizer intacto.
2. `ALTER sqx.forge_campaign_finalists ALTER COLUMN first_rank DROP NOT NULL`, drop check `first_rank > 0`, add `CHECK (first_rank IS NULL OR first_rank > 0)`.
3. `ALTER first_score_ref DROP NOT NULL`; conservar regex cuando `NOT NULL`.
4. Recrear `idx_forge_campaign_finalists_first` con `NULLS LAST` en `first_rank`.

Filas V1 existentes quedan con rank/score NOT NULL de hecho. No backfill. No touch `supersedes`, unique flow_run, stop_evaluations.

## Output v2 (shape)

```text
schema: sqx-finalist-promotion-output.v2
source_ranking_snapshot_ref?: sha256 (ausente en zero-supply)
source_ranking_name
requested_top_n?: uint64  // display; omit si ranking no configuró top_n
effective_promoted_count: uint64  // == len(finalists), estructural, no EffectiveTopN
finalists: [{strategy_ref, rank?: uint64>0, score_ref?: sha256, warnings?: [PERIOD_MISMATCH|FIDELITY_NOT_COMPARABLE|PNL_SIGN_FLIP]}]
```

Orden canónico de `finalists`: `StrategyRef` ascendente. Rank, si presente, no define orden de membership.

`validatePromotionSnapshot` V2: binding FlowRun/name/ref + `snapshot.Validate()`. **No** exigir `TopProjection.Configured`. V1 activity path conserva la exigencia de TopProjection.

`validatePromotion` (config): versión `1.0.0` sigue exigiendo `top_n`; versión `2.0.0` exige source ranking exacto **sin** exigir `top_n`. Productive `mt5_task_config` / intake de Campaign nueva emite `2.0.0`.

Result v2: `ForgeResultSchemaVersionV2 = "forge-result.v2"`. `ForgeFinalist.Rank *uint64` omitempty; `ScoreRef` omitempty; `Warnings []string`. `crossCheckPromotion` sólo si `PolicyVersion==1.0.0`. V2: mismatch de `RankingSnapshotRef` sigue `INCONSISTENT_RESULT`; cardinalidad/entries vs TopProjection no.

## Certification

SDK G01 `promotion-v2-valid`, G02 `finalist-not-comparable`, G03 `historical-v1-adapter`, G11 `requested-instrument-mismatch`, G12 `requested-timeframe-mismatch`, G22 `zero-finalists`. Nivel: SOURCE + CONTRACT. PHYSICAL recert sólo del path de promotion/reconcile identity tocado, no auditoría nueva de ownership MT5 ni F-01/F-03/F-04/F-05.

## Acceptance

- Flujos nuevos: membership = cohort estructural, no Top N.
- `NOT_COMPARABLE` por period mismatch es Finalist sin rank; warning `PERIOD_MISMATCH`.
- Requested≠observed instrument/TF: no Finalist, no warning, Evaluation persistida, Generic no aborta por esa candidata sola.
- Campaign `target_finalists` cuenta unique StrategyRef estructurales (incluye NOT_COMPARABLE).
- Historia V1 readable; `validateFinalistPromotionV1` intacto; result v1 igualdad TopProjection sólo en policy 1.0.0.
- `DATABASE MIGRATION: 014_finalist_promotion_v2`.
- Zero finalists honesto; G22 cero dummy.

## Out of scope

F-03 SQX long-running. F-04 magic/seal/handoff. F-05 golden/release. F-01 identity. S0 Echo. Eligibility/capital Echo. Nuevo modelo de score. Mutar `Eligible` en RankingSnapshot. Reescribir Decisions V1. Umbrales `FIDELITY_SCORE_LOW`. Slot Pool / fencing / takeover. Reabrir Stop Policy fields. B1A/B1B/B2.

## Evidencia y provenance

Inspección read-only `xKoRx/symphony@0509342439cfbaa048839088787458dde1ed1b05`.

- `sqx/activities/worker/rank_snapshot_activity.go` `promotionFinalists` copia `TopProjection.Entries`; `validatePromotionSnapshot` exige TopProjection configured; `validateFinalistPromotionRequest` pin `FinalistPromotionPolicyVersion` 1.0.0.
- `sqx/core/domain/decision.go` policy/output/reasons V1; `validateFinalistPromotionV1` rank==0 inválido; `Decision.Validate` despacha sólo V1.
- `sqx/core/domain/ranking_snapshot.go` `Eligible` sólo COMPUTED; exclusions `SCORE_NOT_COMPARABLE` / `SCORE_INVALID_INPUT`.
- `sqx/core/forge/result.go` `crossCheckPromotion` igualdad Finalists↔TopProjection.
- `sqx/core/runtime/mt5_task_config.go` `validatePromotion` pin 1.0.0 + `top_n` required.
- `sqx/workflows/generic_workflow.go` `persistMT5ReconcileV1` error aborta Generic; `collectMT5ArtifactChildren` dropea child no-success; `runFinalistPromotion` binding GLOBAL snapshot.
- `sqx/activities/worker/mt5_reconcile_activity.go` parse HTM, no compara Spec vs Symbol/Timeframe.
- `sqx/adapters/mt5/report/parse.go` Settings.Symbol / Timeframe observed.
- `sqx/core/evaluation/mt5_fidelity.go` `instrument_mismatch` es Score comparability SQX↔MT5.
- `sqx/adapters/registry-postgres/migrations/009_finalist_promotion_decisions.up.sql` `ck_decisions_policy_v1` 1.0.0.
- `sqx/adapters/registry-postgres/migrations/011_forge_campaign_stop_policy.up.sql` `first_rank NOT NULL CHECK > 0`, `first_score_ref NOT NULL`.
- `sqx/adapters/registry-postgres/forge_campaign.go` `firstObservedFinalists` / `reconcileCampaignFinalists`.
- Frozen: [[2026-09-06-echo-forge-finalist-model-v2]]. SDK §§ membership G01–03/G11–12/G22.

## Límites y contradicciones

Si un caller productivo nuevo sigue emitiendo `promotion.version=1.0.0`, membership V1 (TopProjection) permanece; F-02 obliga configs nuevas a 2.0.0. Si identity mismatch se implementara como error de activity, Generic abortaría: eso viola Case D y está prohibido. `PNL_SIGN_FLIP` no está en el scorer; se deriva en Promotion. Ranking `instrument_mismatch` SQX↔MT5 no sustituye el gate requested-vs-HTM.
