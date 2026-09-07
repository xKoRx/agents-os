---
type: known_error
schema_version: 1
scope: project
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related: ["[[2026-09-01-release-authority-stale-manifest-rollback]]", "[[2026-09-02-echo-forge-release-wrapper-inflight-preflight-fix-normal]]"]
aliases: ["release preflight in-flight manifest race"]
confidence: verified
source_session: ECHO-FORGE-C3-RELEASE-AND-CERT-RETRY-NORMAL
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# Echo Forge release wrapper in-flight manifest preflight race

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `deploy_release.sh` reports target `0.2.85` as `DIVERGENT` after versioned artifacts are visible remotely but before the deployer publishes the new manifest.

## Causa

- The second preflight reads two asynchronous publication phases: remote prefix artifact upload and manifest publication. The authority is correct to reject a settled mismatch, but the wrapper does not distinguish an in-flight publication from a settled divergent release.

## Impacto

- The wrapper exits non-zero even though the same target can become `EXACT_MATCH` moments later; automatic rollout/input continuation is skipped and an operator must decide whether to resume.

## Detección

- Compare authority JSON and deployer events; if `published_version` is old while `remote_line_max` equals the target, wait only under an explicit release procedure, then re-read target and verify exact hashes.

## Mitigación

- Do not delete or overwrite the target prefix, do not republish another version, and do not run certification until `--target <version>` returns `EXACT_MATCH` and an explicit resume decision exists. During the post-build second preflight, accept `PARTIAL_EXACT_MATCH` only when the initial state was `AVAILABLE`; keep `DIVERGENT` fail-closed.

## Evidencia

- On 2026-09-02, canonical `./deploy_release.sh` built `0.2.85`; the deployer uploaded six target artifacts at 15:05:28–15:05:31Z and published the manifest at 15:05:31Z. The wrapper's second preflight at the transition returned `DIVERGENT`; a later read returned published/remote/local/max `0.2.85`, `CONSISTENT`, candidate `0.2.86`, `EXACT_MATCH`. No source, DB or historical artifact mutation was performed.

## Resolución

- Commit `2b4dff61bc0597204e6eeb1c920882cd5b77cd59` adds exact subset verification in `release-authority` and the state-aware second-preflight matrix in `deploy_release.sh`; wrong bytes, wrong size, foreign keys, unknown states, and published partial targets remain divergent or rejected.
- Unit, race, vet, shell syntax, wrapper S1–S17, `internal/di`, diff-check, and real read-only authority checks passed. The fix does not publish or alter an existing release.
- Independent revalidation from `2b4dff61bc0597204e6eeb1c920882cd5b77cd59` confirmed the same evidence: `0.2.85` is `EXACT_MATCH`, `0.2.86` is `AVAILABLE`, and the authority remains `CONSISTENT`; no release-side effect occurred.
