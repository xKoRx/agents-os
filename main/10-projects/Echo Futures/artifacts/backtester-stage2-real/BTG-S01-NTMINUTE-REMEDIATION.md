---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[2026-10-06-codex-gpt-6-luna-btg-s01-ntminute-remediation]]"
aliases: []
tags:
  - kind/doc
  - project/echo-futures
  - topic/backtester
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-NTMINUTE-REMEDIATION

## Propósito

Record the bounded NT-minute source remediation for BTG-S01, its local verification evidence, and its evidence limits.

## Contenido

### Resultado

Product commit `e44b741e0a6c32d39326b46738dc70565db4759c` was pushed to `codex/btg-s01-ntminute-remediation` from the authorized starting point `54698cb0bbd870c942e3ccc010f1a12127684c01`. It implements the R01 immutable per-cursor source snapshot and R02 same-inode alias rejection, with no public API, schema, or identity changes. The frozen SPEC, PLAN, and TASKS were left unchanged; the coordinator-approved test change is recorded in the commit.

At `Open`, each binding is streamed to a private temporary snapshot and checked against its constructor receipt (size and digest) before the cursor can expose rows. The cursor reads only that snapshot, so later changes to the original cannot change its rows. Physical aliases are rejected with `os.SameFile` before source scanning; separate files with equal bytes remain admissible. Cleanup covers close and error paths, with disk-backed streaming rather than whole-corpus RAM buffering.

### Evidencia

- Offline adapter suite passed under `unshare --user --map-root-user --net`: `go test -race -coverprofile=... ./internal/datasets/ntminute -count=1`; package coverage was 96.0%.
- `go vet ./internal/datasets/ntminute`, the anti-test-masking check, and `git diff --check` passed in the same network-isolated environment.
- A local synthetic benchmark passed for 5,000 rows / 250,000 bytes: 1,357,895 ns/op, 184.11 MB/s, 42,992 B/op, 156 allocs/op (3 iterations; Linux/amd64 Xeon E5-2697 v4).
- Coverage review reported 56/63 changed statements covered (about 88.9%) before proposed exclusions. Seven OS failure-handler statements were not induced by these tests; their exclusion is not evidence that they are unreachable. Independent final review was still pending when this record was written.
- The permanent regression tests cover pre-Open mutation, post-Open mutation, short-consumer/tail mutation, symlink and hard-link aliases, equal-byte distinct files, and cleanup/error behavior. The separate regex probe was not counted as an executed test.

### Límites

The original 13-file SFTP corpus was not read or transferred in full, and this work makes no claim about historical corpus contents. No remote source access, corpus rewrite, deployment, merge, or owner acceptance was performed. `staticcheck` was unavailable. This worker record does not declare the independent review, owner acceptance, or root closure complete.

## Fuentes

- Product repository: `echo-ntminute-remediation`, branch `codex/btg-s01-ntminute-remediation`, commit `e44b741e0a6c32d39326b46738dc70565db4759c`.
- Product verification record: `specs/btg-s01-ntminute-remediation/VERIFICATION.md`.
- Coverage profile: BTG-S01 workspace `reports/ntminute-remediation/adapter.cover`.
- Agent run: [[2026-10-06-codex-gpt-6-luna-btg-s01-ntminute-remediation]].
