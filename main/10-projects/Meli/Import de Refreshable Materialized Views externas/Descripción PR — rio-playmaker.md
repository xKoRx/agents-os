---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Import de Refreshable Materialized Views externas]]"
  - "[[rio-playmaker]]"
aliases: []
tags:
  - kind/doc
  - project/import-de-refreshable-materialized-views-externas
created: "2026-10-21"
updated: "2026-10-21"
---

# Descripción PR — rio-playmaker

rio-playmaker · `feature/refreshable-view-import` @ `74bcdde08a1dce9ec3000db1588ad464f439d5c3` · base `origin/develop` @ `f1a4b246d74e679dd81718513b50b56818bd1deb` · [PR draft #1328](https://github.com/melisource/fury_rio-playmaker/pull/1328) · 5 files, 92 insertions, 28 deletions · SIG-700 / SIG-702 · `./scripts/run-agentic-testing-contract.sh` PASS; `./gradlew test jacocoTestReport` PASS (4,933 tests, 0 failures, 2 skipped) on 2026-10-21.

## Propósito

Preparar el texto del PR de rio-playmaker para el slice de import de refreshable views, con la evidencia del gate final local y los pendientes de E2E conjunto y revisión del owner.

## Contenido

El cuerpo siguiente sigue el template de `.github/pull_request_template.md` y es el texto publicado en el PR draft #1328.

---

## Description

feat(actions): allow refreshable view description before component creation

The refreshable import form needs to inspect an external view before it creates a component. Allow the exact `clickhouse-ref-view` / `describe-materialized-view` read pair while keeping warehouse and database listing on the existing `clickhouse-mergetree` pair. This is the rio-playmaker portion of SIG-700; control plane and frontend changes remain separate.

* Add the refreshable description pair to the reviewed read-action configuration and declare AT-100-S09 in the testing manifest.
* Cover pre-creation dispatch with the real application YAML and authorization provider, rejected read and mutation pairs, and the existing imported-reference rename guard.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — this slice awaits cross-app verification and owner review.
* [x] I have used conventional commits.
* [x] My code follows the style guidelines of this project.
* [x] I have performed a self-review of my own code.
* [ ] I have commented portions of my code, particularly in hard-to-understand areas — the configuration and tests need no new comment.
* [x] I updated the applicable canonical documentation, or documented why it is unchanged — AT-100-S09 already describes declared read pairs; its manifest is updated.
* [x] After my changes were applied the app is still buildable.
* [ ] My changes generate no new warnings (linters, code quality) — Gradle emitted deprecation and Unsafe warnings; their baseline provenance was not rechecked.
* [x] I have added tests that prove my fix is effective or that my feature works.
  * [x] Unit testing is a must.
  * [ ] Integration testing is recommended — existing tests cover the service and provider; no new integration case was added.
* [x] New and existing unit tests pass locally with my changes.
* [ ] Any dependent changes have been merged and published in downstream modules — other app slices are in progress.
* [x] I have updated my current branch with changes made in develop/master previously — the worktree starts at the current `origin/develop` baseline.
* [ ] I already deployed this branch in the pre-production environment — no deployment was requested.

## Code Review checklist (must be completed by the code reviewer)

* [ ] Is it the issue being completed?
  * [ ] Is the Acceptance criteria met?
  * [ ] Is the issue ready, according to the project’s Definition Of Done?
* [ ] Is the code good in style?
  * [ ] Are linters used?
  * [ ] Is it clear what a given class/method/function does?
  * [ ] Do names reflect what code does?
  * [ ] Are functions elegant?
* [ ] The code runs correctly? (Optional)
  * [ ] Have you tried the code locally?
  * [ ] Are exceptions handled correctly?
  * [ ] Are all corner cases handled correctly?
  * [ ] Check Java gotchas.
  * [ ] Edge cases for ifs, fors, whiles, dates.
  * [ ] Are there unnecessary while loops?
* [ ] Is this a good enough implementation?
  * [ ] Is every line of code used?
  * [ ] Does code have unexpected side effects?
  * [ ] Is the solution performant?
  * [ ] Could the solution be simpler?
  * [ ] Are there vulnerabilities?
  * [ ] Is the code properly modularized?
  * [ ] Is the code properly tested?
  * [ ] Is there duplicate code?
  * [ ] What is missing?
  * [ ] Is pre-existing code reused?

## How Has This Been Tested?

* `./scripts/validate-repository-contract.sh` — PASS (7 sources, 12 commands, 8 documents).
* `./scripts/run-agentic-testing-contract.sh --plan` — PASS on the final test-only staged delta; no observable-behavior surface changed. The original feature manifest declares 3 focused selectors.
* `./scripts/run-agentic-testing-contract.sh` — PASS on the final test-only staged delta; the 3 declared selectors passed separately (236 tests, 0 failures, 0 skipped).
* `JAVA_HOME=<Java 25> ./gradlew test jacocoTestReport --rerun-tasks` — PASS, 4,933 tests, 0 failures, 0 errors, 2 skipped, JaCoCo generated. Independent YAML/auth/dispatch probe: 4/4 PASS. L0 unit/H2 only; no mutable resources or cleanup needed. Cross-app physical E2E remains pending.
* HEAD is `74bcdde08a1dce9ec3000db1588ad464f439d5c3`, based on `f1a4b246d74e679dd81718513b50b56818bd1deb`; commit pushed to `feature/refreshable-view-import`.

## Testing contract

* [x] I updated `.testing/impact.json` for the observable read-action change.
* [x] The impacted/new AT scenarios and focused tests are declared in the manifest — AT-100-S09 and the three changed test classes.
* [x] The manifest marks behaviorChange true and describes the new read pair.
* [x] Evidence distinguishes L0 from integration and remote layers; L1/F1 were not run.
* [x] No mutable run was executed; there are no cleanup artifacts.

## Issue

SIG-700: https://spellbook.adminml.com/projects/SIG/specs/SIG-700

SIG-702: https://spellbook.adminml.com/projects/SIG/specs/SIG-702

---

## Notas internas — NO van al PR

Shot3 promovió el probe de YAML/autorización/dispatch al test existente sin agregar un sexto archivo; no se aplicaron sugerencias de estilo de Zord sin defecto material. La técnica cita `develop@20f81fb5c`, mientras la base efectiva es `f1a4b246d74e679dd81718513b50b56818bd1deb`. La configuración y el guard vigentes mantienen el diseño del slice. El owner autorizó explícitamente el quinto archivo `.testing/impact.json`; no se ampliaron cambios de producto ni se editaron las specs.
