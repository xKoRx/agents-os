---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related: ["[[CP Flink local]]", "[[RIO E2E local]]", "[[rio-controlplane-flink]]", "[[Descripción PR — rio-controlplane-clickhouse (E2E local)]]"]
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-13"
updated: "2026-10-19"
---

# Descripción PR — rio-controlplane-flink (E2E local)

**Identity:** fury_rio-controlplane-flink · feature/rio-e2e-local-flink-kiss @ 05d46cfd6f50f6c320d21df80bd778f73d91d9f4 · base origin/develop @ 002920440a1c4b16867a8fe8f6f8035c18f2a3a4 · 23 commits · 29 files changed, 2743 insertions(+), 11 deletions(-) · validation 2026-10-19.

> [!info] Validation scope
> Java suites and the Fury pipeline passed on `05d46cfd`; physical standalone E2E was not rerun during this CI recovery session.

## Propósito

Keep the PR #209 body as a resource of [[RIO E2E local]].

## Contenido

This repository has no PR template under `.github`; the body uses the minimal pr-description sections.

---

## What changes

Adds standalone SQL lifecycle tests with Kafka, Flink SQL Gateway and JobManager under `local,compose,local-kafka`. Local adapters replace AWS KDA operations while existing controllers, services, handlers and publishers run against the real local runtime.

`local/README.md` explains the broker/stack commands, topics, suite assertions, teardown and the event multicaster. Provision/start and runtime monitoring use the health view and retain FAILED; stop/deletion use the activity view so FAILED+RUNNING can stop and FAILED+CANCELED becomes READY. The README links to the Playmaker hub and explicitly states that this CP is not integrated with Playmaker.

The local multicaster snapshots each publication step to prevent create/start double dispatch. Submitted job IDs and pending SQL operations are retained for rollback and cancellation retries; later cleanup retries the lookup to register and cancel any recovered job. Terminal ERROR/FAILED/CANCELED operations close without fetching results. Repeated create preserves the registered application, and restart retains the original state until session replacement succeeds. The production action processor and poller accept an optional activity query for stop; existing queries remain the default without a local override.

Optional follow-up in [PR 2 (#211)](https://github.com/melisource/fury_rio-controlplane-flink/pull/211#issuecomment-6276874011): retain replacement-session cleanup handles and retry their closure when both the previous-session DELETE and the compensating DELETE fail, as suggested in [Karla's review](https://github.com/melisource/fury_rio-controlplane-flink/pull/209#discussion_r4318564696).

## Why

Provide a standalone local Flink SQL lifecycle test path through the existing control-plane flows, while preserving the integration model and boundaries in the Playmaker hub.

## How this was tested

- Java 25, `./gradlew --offline test jacocoTestReport localTest`: PASS; 1937 production tests and 19 local tests, zero failures/errors/skips; line coverage 96.06%.
- Physical standalone E2E was not rerun during this CI recovery session.
- `git diff --check`: PASS; required pre-commit checks passed before the CI retry commit.
- [Fury pipeline / Jenkins #1356](https://web.furycloud.io/engineering/applications/rio-controlplane-flink/executions/a72444eb-2e18-42ca-8f9e-6fb0643a287a): PASS on `05d46cfd`; continuous integration, coverage, dependencies, static analyzer and workflow are green. CodeQL also passed.
- CI was restarted with empty commit `05d46cfd`; it changes no files. The optional session-cleanup improvement is tracked in PR 2.

## Issue / specification

RIO E2E local. Branch `feature/rio-e2e-local-flink-kiss` → `develop`. Operational instructions: `local/README.md`; integration source: `fury_rio-playmaker/local/RIO_E2E.md`.
---

## Notas internas — NO van al PR

- CI recovery added only empty commit `05d46cfd`. The PR includes the existing runtime fixes and optional production stop-query wiring described above; its body is no longer scoped to a documentation-only pass.
- Optional replacement-session cleanup remains pending in [PR 2 (#211)](https://github.com/melisource/fury_rio-controlplane-flink/pull/211#issuecomment-6276874011); [Karla was answered in the source thread](https://github.com/melisource/fury_rio-controlplane-flink/pull/209#discussion_r4318662950).
