---
type: agent_memory
schema_version: 1
scope: global
created: "2026-10-03"
updated: "2026-10-03"
area:
project:
application:
entities: []
related:
  - "[[technical-project-manager]]"
aliases:
  - openai pro quota
  - astra weekly pool
confidence: verified
memory_state: active
continuity_key: openai-pro-chat-quota
supersedes:
superseded_by:
load_policy: load when a manager/submanager selects or reconciles ChatGPT CLOUD Pro-pool usage
indexable: true
index_priority: critical
tags:
  - kind/agent-memory
  - scope/global
  - tech/agents-os
  - tech/openai
  - action/quota-tracking
---

# OpenAI Pro Chat — Weekly Pool

## Continuidad

Canonical mutable counter for the Owner's ChatGPT Pro Chat shared weekly Pro-model allowance.

Vendor rule last verified: **2026-10-03**.

Source:
- OpenAI Help — GPT-5.6 and GPT-6 Pro in ChatGPT.
- Current documented Pro $100 Chat allowance: **50 messages/week shared across GPT-6 Pro and GPT-5.6 Sol Pro**.
- ChatGPT Work and Codex use separate allowances and MUST NOT be charged to this counter.

### Current period

```yaml
plan: ChatGPT Pro $100
pool: chat-pro-shared-weekly
limit: 50
tracking_started_at: 2026-10-03
reset_at: UNKNOWN
state: PARTIAL
used_before_tracking: UNKNOWN
used_tracked_since_start: 0
used_exact_this_period: UNKNOWN
remaining_exact: UNKNOWN
remaining_upper_bound_from_tracked_usage: 50
pending_unreconciled_delta: 0
last_reconciled_at: 2026-10-03
```

`PARTIAL` is intentional: usage before this tracker was created is unknown. Do not convert it to an exact remaining count until a real ChatGPT reset has been observed.

### Current-period ledger

| At | Delta | Role | Surface | Project/workstream | Evidence | Reconciled by |
|---|---:|---|---|---|---|---|
| 2026-10-03 | 0 | bootstrap | n/a | tracker creation | pre-tracking usage unknown | system |

### Accounting contract

- Count only confirmed Chat responses that actually draw from the shared Pro pool.
- Do not count `Latest + High/Extra High` or other non-Pro modes merely because they run in ChatGPT.
- Do not count Work/Codex usage.
- A consuming ONE-SHOT worker returns `PRO_CHAT_POOL_DELTA: n` in its handoff.
- A consuming CLOUD Manager/SUBMANAGER counts each Pro-pool response even though its coordinator session remains open.
- The owning Manager/SUBMANAGER reconciles pending deltas before the next consuming dispatch.
- On concurrent edit conflict: refetch, merge unrecorded ledger events, recompute, retry. Never blind-overwrite.
- No negative deltas except explicit reconciliation backed by evidence.
- Never infer a reset date. Persist the reset time only when ChatGPT exposes it or the Owner supplies it.
- On a confirmed reset:
  1. replace the current ledger with a new-period bootstrap row;
  2. set `used_before_tracking: 0`;
  3. set `used_tracked_since_start: 0`;
  4. set `used_exact_this_period: 0`;
  5. set `remaining_exact: limit`;
  6. set `state: EXACT`;
  7. preserve only a compact previous-period summary if useful.
- If any consuming run is known to have happened without a reliable delta, set `state: PARTIAL` and `remaining_exact: UNKNOWN`.

## Señales de carga

Load this note when:

- PRIMARY MANAGER or SUBMANAGER is considering a CLOUD GOD / Pro-pool run;
- a returned worker includes `PRO_CHAT_POOL_DELTA`;
- a CLOUD coordinator itself is running in a Pro-pool mode;
- the Owner asks how much Pro/Astra weekly capacity remains;
- ChatGPT exposes a new reset time;
- the Pro plan or documented allowance changes.

Do not load it for LOCAL-only work or CLOUD High/Extra-High work that does not consume the shared Pro pool.

## Próxima acción

- Reconcile every future confirmed Pro-pool message.
- Ask the Owner for the reset timestamp only when it becomes visible in ChatGPT; until then keep the current period `PARTIAL`.
