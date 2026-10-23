---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Import de Refreshable Materialized Views externas]]"
  - "[[rio-controlplane-clickhouse]]"
aliases: []
tags:
  - kind/doc
  - project/import-refreshable-materialized-views-externas
created: "2026-10-21"
updated: "2026-10-21"
---

# Descripción PR — rio-controlplane-clickhouse

Repo `fury_rio-controlplane-clickhouse` · branch `feature/refreshable-view-import` @ `b23862238960773fa965681e95180ad44754ae3c` · base `develop` @ `4b16f7c2721e0e3c30cd5e020f627cad78040d7f` · 2 commits · 9 files, +179/-15 · SIG-700/SIG-701 · `./gradlew test jacocoTestReport`: 3,949 tests, 1 skipped, 0 failures/errors; 26/26 new executable lines covered (2026-10-21).

PR draft: https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/362

> [!warning] **Cross-app delivery:** The Playmaker and frontend portions of SIG-700 require separate PRs; this PR supplies the control-plane behavior only.

## Propósito

Keep the reviewable PR body beside the project and its implementation evidence.

## Contenido

The following sections follow this repository's `.github/pull_request_template.md`.

---

## Description

feat(clickhouse): import external refreshable views

A `clickhouse-ref-view` that already exists outside Rio previously completed a no-op provision without returning its `DEFINER` credential. This change reuses the classic MV import path when reconciliation makes no change: it reads the preloaded credential, marks the view as imported, and returns the encrypted credential in the existing view response. If a component marked `external_reference=true` points to a missing view, provision fails before creating a view or user, protecting the existing target data. This PR covers the control plane portion of SIG-700; Playmaker and frontend PRs are still required.

* Read the external reference flag from the trigger's actual flat, camel-cased event data; regression tests cover the real trigger mapper and the missing-view command path for boolean `true` and string `"true"`.
* Require the import marker for both refreshable and classic MV imports, and report the existing credential preload endpoint when the credential is absent.
* Preserve the current Rio-managed second-provision behavior: it returns `ALTER_MV` without rereading KVS.

The existing publish sequence has a known delivery gap: if the import marker is written but the terminal result is lost, a later provision sees the view as Rio-managed and does not resend the encrypted credential. This behavior also exists in the classic MV flow and is outside this bounded change; the cross-app E2E and owner review should account for it.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — cross-app delivery, physical E2E, and owner acceptance remain.
* [x] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [x] My code follows the style guidelines of this project
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code
* [ ] I have commented portions of my code, particularly in hard-to-understand areas — the new branches are direct and need no new comments.
* [ ] I have made corresponding changes to the documentation (`README.md`, `DEV.md`, `CHANGELOG.md`) — no repository documentation is part of this bounded control plane change.
* [x] After my changes were applied the app is still buildable
* [ ] My changes generate no new warnings (linters, code quality) — no linter gate was run; the test compiler emitted an existing deprecation warning.
* [x] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must
    * Integration testing is recommended
* [x] New and existing unit tests pass locally with my changes
* [ ] Any dependent changes have been merged and published in downstream modules — Playmaker and frontend changes remain.
* [x] I have updated my current branch with changes made in develop/master previously — the branch base is `origin/develop` at `4b16f7c2`.
* [ ] I already deployed this branch in the pre-production environment — no deployment was performed.

## Code Review checklist (must be completed by the code reviewer)

* [ ] Is it the issue being completed?
* [ ] Is the code good in style?
* [ ] The code runs correctly? (Optional)
* [ ] Is this a good enough implementation?

## How Has This Been Tested?

* `JAVA_HOME=$(/usr/libexec/java_home -v 25) ./gradlew test jacocoTestReport --no-daemon --quiet` — 3,949 tests, 1 skipped, 0 failures/errors; 26/26 new executable lines covered.
* Five independent critical probes passed for missing external view, mapper normalization, missing credential, second provision, and incremental-view rejection.
* Zord complete: eight standard and RIO checks. Physical cross-app E2E remains pending.

## Issue

SIG-700: https://spellbook.adminml.com/projects/SIG/specs/SIG-700 · SIG-701: https://spellbook.adminml.com/projects/SIG/specs/SIG-701
---

## Notas internas — NO van al PR

- The SIG-701 base (`75869083`) and nested `parameters.external_reference` example differ from the current `develop` base (`4b16f7c2`) and actual flat trigger mapper; current source and the real trigger contract were authoritative. The credential error still pointed to `/internal/...`, although the existing controller maps `/clickhouse/...`.
- The three tracked `graphify-out/` files were modified by worktree setup and refresh but deliberately excluded from both product commits. The existing publisher can lose terminal credential output after the import marker is written; the verifier reproduced this inherited parity risk, and owner/cross-app E2E review remains pending.
- PA-1 through PA-5 remain open; implementation follows the SIG-475 parity stated in the technical spec.
