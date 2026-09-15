---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[AGENTS OS - Context Hygiene and Canonical Integrity]]"
related:
  - "[[agents-os-doctor]]"
aliases:
  - Phase 4 Aggregation Specification
tags:
  - kind/doc
  - project/agentsos
  - tech/agents-os
created: "2026-09-13"
updated: "2026-09-14"
---

# AGENTS OS Doctor — Phase 4 Aggregation Specification

## Propósito

Status: **IMPLEMENTED / OWNER REVIEW**

This document is the implementation contract for the Phase 4 evolution of
`agents-os-doctor`. Runtime is implemented at
`80-agents/skills/agents-os-doctor/scripts/doctor.py`; independent adversarial
review closed `READY` and final acceptance remains with the owner. The contract still governs future
changes and does not itself execute checks.

## Contenido

## 1. Goal

Provide one safe, read-only health command for Agents-OS that answers four
independent questions without duplicating the logic that already answers them:

1. **Structural health** — are the core Agents-OS invariants, paths, skill
   registry, always-load club, memory lifecycle and basic installation rules
   internally coherent?
2. **Conformance** — does Agents-OS behave according to its observable
   bootstrap/routing/isolation contracts?
3. **Context efficiency / isolation** — how much context is loaded for
   DEFAULT/MELI/ARANEA and is any domain-specific context or capability leaking
   across scopes?
4. **Canonical knowledge hygiene** — are canonical/deprecated/archive/routing
   relationships internally consistent, and is zombie documentation still in
   the hot path?

The public experience should become conceptually:

```text
agents-os doctor

STRUCTURAL........ PASS
CONFORMANCE....... FAIL   1 fail · 4 warn
CONTEXT............ WARN   DEFAULT≈7.0k · MELI≈9.0k · ARANEA≈8.2k est
CANONICAL.......... FAIL   5 failing checks · 1004 findings

OVERALL............ FAIL
```

The command is an **aggregator**, not a fourth implementation of the same
rules.

## 2. Existing Authorities / Providers

Phase 4 must consume the existing tools as providers:

| Component | Current authority / entrypoint | Responsibility |
|---|---|---|
| structural | `80-agents/skills/agents-os-doctor/scripts/doctor.py` | existing Doctor structural checks |
| conformance | `80-agents/tools/conformance-harness/agents_os_conformance.py` | correctness / contracts |
| context | `80-agents/tools/context-budget/context_budget.py` | context footprint / domain leakage |
| canonical | `80-agents/tools/canonical-linter/canonical_linter.py` | canonicality / deprecation / routing hygiene |

Phase 4 MUST NOT copy their check implementations into the aggregator.

Before implementation, P4-A must inspect the actual current CLI and
machine-readable contracts of all four providers. This specification describes
the desired integration contract; it does not authorize inventing flags or
schemas that the providers do not currently expose.

## 3. Architecture

Target shape:

```text
                     agents-os doctor
                            │
                            ▼
                    thin orchestrator
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
      structural       conformance          context
          │                                   │
          └─────────────────┬─────────────────┘
                            ▼
                        canonical
                            │
                            ▼
                   normalized envelope
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
             human summary           --json
```

Default execution is **sequential**. There is no value in consuming additional
agent/process concurrency merely to make a health command slightly faster.
Sequential execution also produces deterministic ordering and clearer failure
attribution.

Provider isolation is preferred. The aggregator may invoke provider CLIs via
subprocess and consume their JSON output, or use a stable public Python API if
one already exists. It must not import private implementation details solely
for convenience.

## 4. Public Entrypoint

The canonical user-facing entrypoint remains:

```bash
python3 80-agents/skills/agents-os-doctor/scripts/doctor.py
```

Do not create a competing second Doctor CLI unless implementation evidence
shows that preserving this path is materially unsafe.

The existing `agents-os-doctor` skill remains the routing surface.

A shell alias or future packaged `agents-os doctor` command may point to this
entrypoint, but packaging is outside Phase 4.

## 5. Minimal CLI Contract

Target options:

```text
--component structural|conformance|context|canonical|all
--json
--strict
--live
--vault-root PATH
```

Default:

```text
--component all
read-only
non-live
human summary
```

Rules:

- `--component` is for focused diagnosis and development. Default is `all`.
- `--json` returns machine-readable normalized output.
- `--strict` changes exit policy, not the provider findings themselves.
- `--live` enables only the live/exposure checks already supported by
  providers. It never grants mutation authority and never invokes destructive
  MCP/API operations.
- `--vault-root` must be propagated to providers that support it.
- Do not add a broad configuration framework, daemon, database, dashboard,
  remote service or plugin system in Phase 4.

If provider reality makes one of these flags unnecessary or impossible, P4-A
must document the evidence and keep the CLI smaller rather than emulate fake
support.

## 6. Provider Execution Semantics

Default order:

```text
structural
→ conformance
→ context
→ canonical
```

The order is for stable presentation only. Providers are logically
independent.

**A finding or FAIL in one provider MUST NOT prevent the remaining providers
from running.**

This is a hard Phase 4 requirement. The Conformance Harness already proved why
this matters: a legitimate L0 schema failure can gate its own deeper layers,
but must not hide context or canonical diagnostics produced by independent
tools.

Only a truly global precondition failure may prevent all providers, for
example:

- vault root cannot be resolved;
- required Python runtime unavailable;
- the requested vault cannot be read.

A provider-specific crash produces a provider execution error and the Doctor
continues with the other providers where safe.

## 7. Two Different Status Axes

Do not confuse system health with tool execution health.

Each provider result carries:

```text
execution_status: OK | ERROR
verdict: PASS | FAIL | WARN | SKIP
```

Examples:

- canonical linter runs correctly and discovers broken routing →
  `execution_status=OK`, `verdict=FAIL`.
- context auditor cannot parse its own configuration →
  `execution_status=ERROR`; this is NOT proof that Agents-OS itself failed.
- live MCP surface not requested → `execution_status=OK`, relevant live check
  remains `SKIP`.

The aggregator must never convert UNKNOWN/unobservable behavior into PASS.

## 8. Normalized Result Envelope

The three new tools were deliberately built with compatible concepts. Phase 4
should normalize only the small common denominator instead of creating a large
new domain model.

Target top-level shape:

```json
{
  "schema_version": 1,
  "tool": "agents-os-doctor",
  "vault_root": "...",
  "baseline_start": "<git sha or unknown>",
  "baseline_end": "<git sha or unknown>",
  "baseline_stable": true,
  "live": false,
  "strict": false,
  "overall": {
    "execution_status": "OK",
    "verdict": "FAIL"
  },
  "components": []
}
```

Each component should expose, when available:

```text
name
execution_status
verdict
pass_count
fail_count
warn_count
skip_count
finding_count
metrics
source_entrypoint
source_result_path (optional)
```

Individual normalized findings should preserve the provider identity and the
common fields already used by Phase 2/3:

```text
provider
check_id
component/category
scope
status/verdict
severity
observed
expected
evidence
confidence
path/ref when applicable
```

Structural `LOW` findings use normalized `status: INFO`: they remain visible in
records and metrics but do not affect component verdict or strict exit policy.
`INFO` is a finding status, never a provider verdict.

Do not force a provider to invent fields it cannot support. Missing data stays
null/absent/unknown according to the final schema decision.

## 9. Preserve Provider Truth

The aggregator MUST NOT reinterpret provider findings merely to make the final
report uniform.

Examples:

- `estimated_tokens` remains estimated; Doctor must not relabel it `tokens`.
- canonical heuristic WARNs remain WARNs.
- a Conformance Harness SKIP caused by unavailable runtime observability
  remains SKIP.
- a provider's system FAIL must not be changed to WARN because another provider
  passed.

Doctor aggregates. Providers decide their own checks.
This includes Context's `RULES-FIDELITY-ANCHORS`: Context emits the record and
count; Doctor consumes them without inspecting provider-specific gate fields.

## 10. Overall Verdict

Default policy:

```text
if any component execution_status == ERROR:
    overall.execution_status = ERROR
else:
    overall.execution_status = OK

if any successfully executed component has FAIL:
    overall.verdict = FAIL
elif any successfully executed component has WARN:
    overall.verdict = WARN
elif at least one component PASS and the rest PASS/SKIP:
    overall.verdict = PASS
else:
    overall.verdict = SKIP
```

An execution `ERROR` has precedence for the process exit policy because the
health picture is incomplete, but it must remain distinguishable from a real
Agents-OS `FAIL` in the rendered result.

## 11. Exit Codes

Target contract:

```text
0  provider execution succeeded; no FAIL under selected policy
1  real Agents-OS FAIL, or WARN/SKIP promoted by --strict policy
2  Doctor/provider execution error; health result incomplete
```

`--strict` MUST NOT rewrite records from WARN/SKIP to FAIL. It only changes
whether they make the process exit non-zero.

P4-A must reconcile this with the current `doctor.py --strict` behavior before
implementation.

## 12. Human Output

Default output must be short enough to run routinely.

Example:

```text
AGENTS-OS DOCTOR
baseline: a1b2c3d → a1b2c3d (stable)
mode: read-only / non-live

STRUCTURAL   PASS   0 high · 0 medium · 0 low
CONFORMANCE  FAIL   4 pass · 1 fail · 4 warn · 17 skip
CONTEXT      WARN   7 pass · 0 fail · 7 warn · 1 skip
                      DEFAULT≈7.0k · MELI≈9.0k · ARANEA≈8.2k est
CANONICAL    FAIL   6 pass · 5 fail · 9 warn · 1004 findings

OVERALL      FAIL

Top actionable findings:
- <provider/check> ...
- <provider/check> ...

Use --json for machine-readable detail.
```

Default human output MUST NOT print 1004 findings.

Show a bounded actionable summary. Detailed provider output remains available
through `--json`, provider-specific execution, and/or the provider result
artifact.

## 13. Context Metrics

When the Context Budget provider runs, the Doctor summary should surface the
most decision-useful baseline only:

```text
DEFAULT cold estimated tokens
MELI cold estimated tokens
ARANEA cold estimated tokens
observed domain leaks
observed deprecated hot-path count
```

Do not expand the Doctor into a token analytics dashboard.

Do not compare numbers across runs unless the measurement method/confidence is
compatible.

## 14. Canonical Findings

Canonical Linter may return a large corpus finding count. Doctor should render:

- failing check IDs/categories;
- aggregate finding count;
- top bounded actionable examples;
- path to detailed machine/provider result when available.

No auto-remediation.

A large finding count is not justification for truncating or mutating the
source corpus during a Doctor run.

## 15. Conformance Findings

The Conformance Harness remains authority for cold/warm/switch/isolation
semantics.

Doctor MUST NOT create a second routing model.

If the harness gates one of its own layers due to a real earlier failure,
Doctor reports that faithfully and continues the independent context/canonical
providers.

## 16. Existing Structural Doctor

The current Doctor contains useful checks that are not merely obsolete because
new tools exist, including installation/path integrity, always-load club,
skill registry, secret-assignment heuristics and continuity-memory hygiene.

Phase 4 must preserve those capabilities as the **structural provider** unless
P4-A proves an individual check has a stronger canonical owner elsewhere.

When ownership overlaps:

```text
stronger existing provider owns the fact
→ structural Doctor links/aggregates
→ no duplicated business rule
```

Do not silently delete legacy checks during aggregation.

## 17. Baseline Stability

The vault may auto-sync while Doctor is running. Capture revision (when Git is
available) at both start and end:

```text
baseline_start
baseline_end
baseline_stable
```

If they differ:

- do not invalidate the entire run automatically;
- emit a clear baseline warning;
- avoid claiming the aggregate is a single immutable snapshot;
- preserve each provider's own evidence/baseline where exposed.

Do not stash/reset/checkout merely to freeze the vault.

## 18. Safety

Doctor is read-only by default and Phase 4 does not change that.

The unified command MUST NOT:

- mutate canonical notes;
- archive/delete files;
- fix findings automatically;
- invoke write-capable MCP tools;
- modify MELI/Aranea/Echo/Echo Forge systems;
- reset/stash/clean Git state;
- expose bearer/token/password values;
- run remote mutations as a health probe.

`--live` means safe observation/exposure checks only.

Repairs continue to require explicit owner authorization after diagnosis.

## 19. Failure Isolation / Timeouts

One broken provider must not hang the entire Doctor indefinitely.

Phase 4 should use bounded provider execution and report timeout/error as tool
execution failure. P4-A/P4-B should pick the smallest timeout policy compatible
with current real runtimes rather than adding a configuration subsystem.

Do not retry providers blindly. A retry is allowed only for a known transient
failure with bounded semantics.

## 20. No Semantic De-duplication in V1

Different providers may report related symptoms. V1 must preserve provenance.

Allowed:

- exact duplicate suppression when the same provider emits the same record
  twice due to a technical artifact;
- presentation grouping by provider/category.

Not allowed:

- fuzzy/LLM semantic merging of findings;
- deciding that two different check IDs are "the same" and dropping one;
- changing severity to reconcile disagreement.

Cross-provider semantic deduplication is YAGNI until evidence shows it is
needed.

## 21. Phase 4 Implementation Tasks

### P4-0 — Architecture/spec

This document. Defines the target without changing runtime behavior.

### P4-A — Provider Contract Audit

Read-only audit of the four providers. Produce one compact artifact defining:

- real flags;
- JSON/machine output available today;
- exit codes;
- runtime requirements;
- timeout behavior;
- missing integration surfaces;
- ownership overlaps;
- exact minimal adapter changes required.

No implementation before this gate.

### P4-B — Thin Aggregator Implementation

Implement the smallest orchestration layer that:

- executes selected providers sequentially;
- isolates provider crashes;
- normalizes shared fields;
- preserves raw provider semantics;
- renders concise human summary;
- emits JSON;
- preserves the canonical Doctor entrypoint.

### P4-C — Integration Selftests

Must test at least:

- all providers PASS/healthy fixture;
- one real provider FAIL while later providers still run;
- one provider WARN;
- one provider SKIP;
- provider execution ERROR;
- mixed PASS+WARN+SKIP overall semantics;
- `--strict` exit policy without verdict mutation;
- `--component` filtering;
- `--json` valid envelope;
- changing Git baseline warning;
- no canonical mutation.

Use fixtures/mocks for orchestration failure semantics; also run against the
real vault before acceptance.

### P4-D — Adversarial Verification

Status: **DONE — external verdict `READY`**. The verifier independently
reproduced the final fixes, provider selftests, source/export execution,
read-only hash evidence and DEFAULT build. No findings remain open.

Fresh verifier must try to prove:

- Doctor duplicates provider business logic;
- an early FAIL stops later providers;
- UNKNOWN/SKIP becomes PASS;
- provider ERROR is misreported as system FAIL;
- estimated token values become exact;
- canonical 1000+ findings flood default output;
- strict mode mutates records;
- live mode can cause side effects;
- current structural Doctor capabilities were accidentally dropped;
- baseline movement is hidden;
- exit codes are inconsistent with rendered verdict.

Verifier does not auto-fix.

### P4-E — Skill / Docs / Acceptance

After implementation is verified:

- update `agents-os-doctor/SKILL.md` from structural-current to unified Doctor;
- update executable documentation/examples;
- update `BENCHMARK.md` only if benchmark semantics actually change;
- run all provider selftests + Doctor integration tests;
- run Doctor against the real vault;
- update project state and handoff.

## 22. Phase 4 Acceptance Gates

Do not mark Phase 4 DONE until:

```text
[x] P4-A real provider contract audited
[x] no provider business logic duplicated
[x] existing structural Doctor checks preserved or explicitly re-owned
[x] one canonical Doctor entrypoint
[x] sequential execution demonstrated
[x] provider FAIL does not suppress independent providers
[x] provider ERROR distinguishable from Agents-OS FAIL
[x] PASS/FAIL/WARN/SKIP preserved
[x] concise human summary
[x] machine-readable JSON
[x] DEFAULT and installed federated context packs surfaced without false precision
[x] canonical large finding sets bounded in human output
[x] --strict policy verified
[x] --component verified
[x] --live remains read-only
[x] baseline start/end captured where Git is available
[x] no canonical mutations during Doctor run
[x] orchestration selftests green
[x] all provider selftests remain green
[x] real-vault and built-artifact smoke completed
[x] fresh adversarial verifier completed
[x] SKILL.md reflects implemented reality, not planned behavior
```

## 23. Non-goals

Phase 4 does NOT:

- fix Conformance F1;
- clean the 1004 canonical findings;
- optimize the context budget;
- alter DEFAULT/MELI/ARANEA semantics;
- create dashboards;
- schedule periodic runs;
- expose Doctor as MCP;
- add CI/CD unless separately approved;
- perform automatic remediation;
- redesign Agents-OS.

Those are separate decisions after a unified diagnostic surface exists.

## 24. Definition of Done

Phase 4 is done when a fresh operator or agent can run one safe command and
obtain a truthful, bounded, machine-readable health snapshot across structural
integrity, conformance, context efficiency/isolation and canonical knowledge
hygiene — while each underlying provider remains the single source of truth for
its own checks.
