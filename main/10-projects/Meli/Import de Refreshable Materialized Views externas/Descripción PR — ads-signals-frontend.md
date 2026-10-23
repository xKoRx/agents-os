---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Import de Refreshable Materialized Views externas]]"
  - "[[ads-signals-frontend]]"
aliases: []
tags:
  - kind/doc
  - project/import-de-refreshable-materialized-views-externas
created: "2026-10-21"
updated: "2026-10-22"
---

# Descripción PR — ads-signals-frontend

## Propósito

Store the reviewable GitHub PR body with its branch, checks and blockers in the project vault.

## Contenido

Repo `ads-signals-frontend` · branch `feature/refreshable-view-import` @ `027d9f10c83b1962ea463c905f17d2de58b291bf` · base `origin/develop` @ `9a70723c96ebd7f7a8e6564988ed4f8e630ea58a` · 4 commits · 20 files, +1309/−276 · SIG-700/SIG-703 · requires the existing Playmaker `describe-materialized-view` action for `clickhouse-ref-view` · 2026-10-22: 502/502 suites, 11710/11710 tests, lint 0 errors/385 warnings, changed-statement coverage 142/144 (98.61%).

> **BLOCKED — typecheck:** `npm run typecheck` exits 2 with 123 inherited errors at the same codes/locations as `origin/develop`; one diagnostic's shortened display changes “31 more” to “32 more” because of the added optional adapter property.
>
> **REVIEWED — Zord:** The owner-authorized earlier-diff review completed 8/8; the accepted frontend Save-path finding was fixed in this candidate. The new SHA has not had a second Zord run; independent local Save/permission probes passed.
>
> **PENDING — physical E2E and rollout:** The latest candidate needs a new physical run. CP and PM must roll out before frontend.

The text after the first separator is the PR body. Internal notes after the second separator are excluded from GitHub.

---

> **BLOCKED — typecheck:** `npm run typecheck` exits 2 with 123 TypeScript errors at the same locations and codes as pristine `origin/develop`, including `CanvasControls.spec.tsx:325` (`TS2345`). One existing diagnostic changes its display from “31 more” to “32 more” because this branch adds an optional adapter property; there are no new errors. This draft does not satisfy the typecheck gate.
>
> **REVIEWED — Zord:** The owner authorized review of the earlier PR diff; all 8 configured reviewers completed. The accepted frontend Save-path finding is fixed in this candidate. This new SHA has not had a second Zord run. An independent local recheck passed the Save-path and permission probes.
>
> **PENDING — physical E2E and rollout:** The ClickHouse 25.8 SHOW CREATE normalization defect and frontend Save-path defect are fixed in this candidate. A new joint run against this SHA remains pending. CP and PM rollout must precede the frontend; the end-to-end outcome is unverified.

[description]: https://img.icons8.com/material-sharp/24/000000/document.png
[checkmark]: https://img.icons8.com/material-sharp/24/000000/checkmark.png
[checklist]: https://img.icons8.com/material-sharp/24/000000/check-all.png
[testing]: https://img.icons8.com/material-sharp/24/000000/test-partial-passed.png

# ![alt text][description] PR Description

## What is the current behavior?

The external ClickHouse import flow accepts incremental materialized views only. A refreshable materialized view found in ClickHouse cannot be attached to a data product through its form, and the existing describe dispatch always requests `clickhouse-mat-view`.

## What is the expected behavior with the new change?

The refreshable view form can describe and import an existing view using the shared ClickHouse import modal and preview, then save that external reference through NodeConfigModal. The describe dispatch accepts only `clickhouse-mat-view` (the backward-compatible default) or `clickhouse-ref-view`; unsupported values return 400 without dispatching. Imported values retain the qualified view, source, destination, write mode and normalized SQL, set `external_reference: true`, and expose no external pipeline relations. Source/destination references, write mode and SQL remain read-only until the first successful deployment, including after a failed deployment. The incremental view form rejects refreshable definitions and directs the user to the refreshable form. Canceling after preview leaves the form unchanged and clears the preview before the modal is reopened. For a ClickHouse 25.8 SHOW CREATE that declares a quoted `window` column but emits bare `window` in the SELECT projection, import normalizes that projection back to a quoted identifier while retaining qualified table references and removing ownership clauses; SQL literals, comments and unsupported WINDOW clauses keep their prior behavior.

# ![alt text][testing] Testing

## How to test the new behavior?

- `npm run test:unit`: 502/502 suites and 11710/11710 tests passed; no snapshots. The permanent integration test covers import → confirm → Save with `external_reference: true`; permission and failed-first-deployment regressions pass.
- `npm run lint`: 0 errors and 385 warnings.
- Fresh coverage report: 142/144 statements touched by the branch diff covered (98.61%).
- Real ClickHouse 25.8 `result.ddl` from the completed describe action (SHA-256 `58ff04c5401c2993357ea63e15b4bc60e234bc87a52626105f745f03fe890fa2`): before the fix the normalizer left bare `window` and validation rejected import; on this SHA the normalized SQL passes validation without changing the literal schema-qualified references.
- `git diff --check`: passed; 20 changed files.
- `npm run typecheck`: BLOCKED by the 123 baseline errors described above.
- The earlier-diff Zord review completed. Independent local recheck on this SHA passed 4 Save/permission probes and 11 real-DDL assertions; physical E2E for this SHA remains pending.

# ![alt text][checkmark] Related Issue

SIG-700 (functional), SIG-703 (technical).

# ![alt text][checklist] PR Checklist

- [x] I carefully reviewed the code before creating this PR.
- [x] I made sure the `diff` clearly represents my changes.
- [x] I made sure this PR doesn't make sense to split into smaller PRs.
- [x] I verified that my code style and scaffolding follow the project standards.
- [x] I made sure my changes don't affect any functionality other than this PR.
- [x] I added/modified the necessary `tests` for the component or functionality I'm implementing.
- [x] I ran the `tests` and made sure they pass.
- [ ] I updated the `CHANGELOG.md` file with the change in the `[Unreleased]` section under `Fixed` or `Added` as appropriate. Out of scope for this 20-file implementation slice.
- [ ] I made sure to update the README with the new behavior, if applicable. No README change is needed for this form behavior.
---

## Notas internas — NO van al PR

- Technical spec references `bd7100809`; current base `9a70723c9` includes #805 changes to the ClickHouse import and canvas connection flow. Implementation builds on the current behavior and does not restore old behavior.
- The project note and log are maintained by the coordinating agent; this worker did not edit them concurrently.
- Typecheck baseline comparison used `git archive origin/develop` in `/tmp` and identical dependency resolution, without modifying the original checkout. The final 123 errors keep the baseline codes and locations. One existing TS2352 diagnostic at `useNodeConfigSubmission.spec.ts:213` shortens the augmented adapter type as “32 more” rather than “31 more”; this is not a new error.
- The one existing CodeQL review thread received an updated reply for `027d9f10c83b1962ea463c905f17d2de58b291bf`: the two-value dispatch allowlist and 400-without-dispatch test remain in place. Reply: https://github.com/melisource/fury_ads-signals-frontend/pull/816#discussion_r4347520487.
- Zord 8/8 review of the prior diff completed after explicit owner authorization. The accepted `FRONT-ZORD-1` Save-path defect is fixed here. The new SHA has not had a second Zord review.
- PT2: decoded Playmaker/ClickHouse 25.8 DDL SHA-256 `58ff04c5401c2993357ea63e15b4bc60e234bc87a52626105f745f03fe890fa2` is retained as the exact permanent fixture; normalization quotes only the declared projection and passes the unchanged validator.
- This candidate's new integration regression uses the actual NodeConfigModal import → confirm → Save flow and asserts `external_reference: true`; explicit read-only, missing save permission, failed first deployment, and classic MV tests pass. Physical E2E on this SHA remains manager-owned and pending.
