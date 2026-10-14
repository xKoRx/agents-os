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
updated: "2026-10-14"
---

# Descripción PR — rio-controlplane-flink (E2E local)

**Identity:** fury_rio-controlplane-flink · feature/rio-e2e-local-flink-kiss @ c0cabe7213461793bf1382c4e2816dea258361fd · base origin/develop @ 002920440a1c4b16867a8fe8f6f8035c18f2a3a4 · 18 commits · 23 files changed, 2274 insertions(+) · validation 2026-10-14.

> [!warning] Physical validation pending
> The shared VM startup command fails while another session owns `rio-local`; this pass claims local checks and documentation publication only.

## Propósito

Keep the PR #209 body as a resource of [[RIO E2E local]].

## Contenido

This repository has no PR template under `.github`; the body uses the minimal pr-description sections.

---

## What changes

Adds standalone SQL lifecycle tests with Kafka, Flink SQL Gateway and JobManager under `local,compose,local-kafka`. Local adapters replace AWS KDA operations while existing controllers, services, handlers and publishers run against the real local runtime.

`local/README.md` explains the broker/stack commands, topics, suite assertions, teardown, event multicaster and two state views: `describeApp` reports activity so FAILED+RUNNING can stop and FAILED+CANCELED becomes READY; `describeAll` retains FAILED for health/runtime status. It links to the Playmaker hub and explicitly states that this CP is not integrated with Playmaker.

The local multicaster snapshots each publication step to prevent create/start double dispatch. Submitted job IDs are retained for rollback and cancellation retries. If Gateway launches a job but its ID lookup fails with 503/timeout, that job can remain unregistered and uncanceled; recovery/reconciliation is a code follow-up, documented in this README. Production sources remain unchanged.

## Why

Make the local test path and its boundaries understandable without reading source code, while preserving the integration model in the Playmaker hub.

## How this was tested

- Java 25, `./gradlew --offline localBootJar localTest` in a fresh Bash shell: PASS; 11 local tests, zero failures/errors/skips.
- Literal standalone startup stops before resource creation with `rio-local is occupied; wait for its owner to finish`; `python3 local/e2e.py` and teardown remain pending until the shared VM is free.
- `git diff --check` and required pre-commit checks on changed Markdown: PASS.
- The job-ID failure thread is answered with the documentation SHA and resolved under the documentation-only scope; the runtime code change remains pending.
- This pass changes only Markdown. The separate Flink integration delivery is untouched.

## Issue / specification

RIO E2E local. Operational instructions: `local/README.md`; integration source: `fury_rio-playmaker/local/RIO_E2E.md`.

---

## Notas internas — NO van al PR

- Documentation-only delta; runtime sources, build files, Compose, scripts and Dockerfiles are unchanged.
