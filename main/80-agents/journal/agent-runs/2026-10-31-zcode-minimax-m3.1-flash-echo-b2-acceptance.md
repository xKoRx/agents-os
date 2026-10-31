---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-31"
updated: "2026-10-31"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
application:
entities: []
related:
  - "[[Echo Futures — Runtime Pools]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: minimax/MiniMax-M3.1-Flash
model_source: host
task_type: debugging
task_complexity: high
outcome: partial
verification: passed
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-10-31-zcode-minimax-m3.1-flash-echo-b2-acceptance

## Trabajo

- **Objetivo:** EF-SUN-01 — acceptance verification read-only of the B2 native recovery capsule `e8f6c5ab-f520-4c90-a4b8-9b55b78619a5` on Echo DEV, plus preparation of what can be prepared today for Sim101 and for the release candidate. Recovery Verifier role; the GOD manager was in cloud.
- **Alcance atribuible a esta combinación superficie×modelo:** the whole physical read path (Flink DEV REST, Kafka DEV, ETCD RO, SSH Daedalus/.75, local `echo-core-dev` journal) and the offline analysis of the two real capsules; the repo-comprehension work was delegated to two `code-scout` subagents (dispatch `EF-SUN-01-REPO-A`, `EF-SUN-01-REPO-B`) and the offline release build to a third subagent (`EF-SUN-01-G4`), all on the same surface×model. Zero runtime mutation, zero order, zero PROD touch.
- **Artefactos afectados:** read-only on the product (no commit, no push, no tag, no worktree of others touched). New: mission branch `codex/ef-sun-01-b2-acceptance` at `bf7420d2c5656c09830f427d710142fea6b60735` in worktree `/home/kor/aranea/work/ef-sun-01-20261031/wt`; evidence set under `/home/kor/aranea/work/ef-sun-01-20261031/evidence/` (13 artifacts + `MANIFEST.sha256`); read-only reader `bin/kread` (source `tools/kread/main.go`); release staging under `release/staging-bf7420d2/`.

## Evidencia

- **Validaciones ejecutadas:** `git ls-remote` + `git fetch` (remote `origin/master=bf7420d2`, ancestors `2baf319d`/`64f0853b` confirmed, merge parents confirmed, worktree clean); explicit `read_committed` Kafka reads with a group-free, no-autocommit sarama consumer (`IsolationLevel=ReadCommitted`) over `market-run-journal`, `market-stream-state`, `market-feed-candidates`, `market-run-manifests`, `recovery-attest-report`, `strategy-config`, `pool-config`, `account-configs`; Flink DEV REST (job `0f6901a3` RUNNING 40/40, 562/562 checkpoints, restore from `echo-feed-p0-20261030/savepoint-0f6901-bf5a646f5f8d`, savepoint 2624 = `echo-feed-p0-20261031-b2-replay/savepoint-0f6901-3103d0fa4c4a`); ETCD RO reads; `echo-core-dev` journal; `.75` container/mount inspection for the effective auto-restore reference; an independent grid oracle in Python over the two recovered capsules.
- **Resultado observable:** capsule `e8f6c5ab` (25 094 B, sha256 `49c75a69…`) was **admitted** by the market owner (ingress p4 off 45207237 → journal off 14 → analytics epoch barrier → negative receipt off 15) and **rejected by analytics with `NATIVE_GRID_INVALID`**; 0 of 3 expected positive receipts; durable state `status=INVALIDATED`, `readiness=NOT_READY`, `old_ticks_recovered=false`, `gap_ref_count=2`, `target_count=1`, `receipt_count=1`, `source_epoch=1`, `source_frontier=550236`, `source_gap_open=true`, `freshness=UNKNOWN`. An independent oracle reproduced the rejection cause exactly: **8 H4 bars with `bucket_open_utc=21:00Z`** (CME session close, not a 4h grid open) are present identically in both capsules; the successor corpus differs from the predecessor only in `available_at` and one `volume` value, i.e. the documented native-timestamp correction is **not** in the physically produced bytes. The deployed Core was identified as `64f0853b` (not the integrated `bf7420d2`, not the `current` symlink) and the Gateway as `3eaed4d2`.
- **Limitaciones de la evidencia:** `supersedes_id`/`supersedes_digest` are not exposed on any read_committed Kafka surface (they live in the Flink ValueSpec `futures_ms_run`) — only the supersession *effect* is observable; the NT client profile (`C:\Users\KoR\…`) is access-denied for the MCP identity, so the installed AddOn bytes, the NT lane split and the NT `Account.Name`/`Account.Id` are `NOT_OBSERVED`; FX consumer-group offsets and the effective MM→RiskFinalizer composition were not re-read in this cut; the release candidate was built offline and **has no smoke test**; the C# AddOn was not buildable locally (needs the NT assemblies on .132).

## Evaluación

- **Correctness:** 4
- **Autonomy:** 4
- **Efficiency:** 3
- **Tool use:** 4
- **Overall:** 4

## Resultado

- **Outcome:** `partial` — G1 acceptance **denied** with a located first jump and a specified minimal repair + regression tests; G2/G3/G4 prepared as far as the read-only scope allows. The blocking finding is a **product-side defect in the NT native-bar producer** (one spurious H4 bar per session opened at the session close), not a market-state condition; `WAITING_FRESH_DATA3` alone would have been wrong.
- **Rework posterior:** `unknown`
- **Aprendizaje para comparar herramientas:** the decisive move was reading the *durable server state* (journal + stream-state snapshot) with an explicit `read_committed`, group-free reader instead of trusting the MCP reader or the Core log; the Core log alone would have said "epoch barrier applied" and hidden the rejection entirely.
