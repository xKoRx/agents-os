---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[RIO E2E local]]"
  - "[[rio-playmaker]]"
  - "[[Descripción PR — rio-controlplane-clickhouse (E2E local)]]"
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-12"
updated: "2026-10-14"
---

# Descripción PR — rio-playmaker (E2E local ClickHouse)

**Identity:** fury_rio-playmaker · feature/rio-e2e-local-clickhouse-kiss @ 35b52545445fb4de9f01a40c5bc77971e844d0a7 · base origin/feature/rio-e2e-local-kafka @ 1d9ceefd5654575931de884ce18ef3a4daccc551 · 16 commits · 14 files changed, 1062 insertions(+), 6 deletions(-) · validation 2026-10-14.

> [!warning] Physical validation pending
> The shared VM startup command fails while another session owns `rio-local`; this pass claims local checks and documentation publication only.

## Propósito

Keep the PR #1288 body as a resource of [[RIO E2E local]].

## Contenido

Body follows `.github/pull_request_template.md`; unchecked gates are not claimed by this documentation pass.

---

## Description

feat: add Playmaker ClickHouse E2E over local Kafka

The Playmaker ClickHouse suite enters through business APIs and checks correlated CP results, persisted Playmaker status and physical SQL effects. It supports MergeTree provisioning, query actions, MV describe/stop/start, refreshable PROVISION and Kafka-to-ClickHouse ingestion.

- Extend the `local/RIO_E2E.md` hub with the complete manual flow: private four-variable environment file, Kafka/MySQL/ClickHouse startup, host Playmaker JVM, bounded readiness checks, serial suites and teardown.
- Keep the general scenario documentation as a Spanish pointer to the hub under AT-180-S21.
- Supply the legacy data-product fields in action fixtures and use a separate runtime-status listener factory without a circular-reference override.

This PR is stacked on [#1286](https://github.com/melisource/fury_rio-playmaker/pull/1286) through normal merges and depends on ClickHouse CP [#342](https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/342). Connector DEPROVISION is excluded as `develop-gap`; refreshable supports only PROVISION. S3/Iceberg destinations and browser journeys are outside this suite.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done
* [x] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [ ] My code follows the style guidelines of this project
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code
* [ ] I have commented portions of my code, particularly in hard-to-understand areas
* [x] I updated the applicable canonical documentation (`docs/architecture.md`, `testing.md`, `testing-scenarios.md`, Swagger, README, or CHANGELOG), or documented why it is unchanged.
* [x] After my changes were applied the app is still buildable
* [ ] My changes generate no new warnings (linters, code quality)
* [ ] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must
    * Integration testing is recommended
* [ ] New and existing unit tests pass locally with my changes
* [ ] Any dependent changes have been merged and published in downstream modules
* [ ] I have updated my current branch with changes made in develop/master previously
* [ ] I already deployed this branch in the pre-production environment

## Code Review checklist (must be completed by the code reviewer)

* [ ] Is it the issue being completed?
  * Is the Acceptance criteria met?
  * Is the issue ready, according to the project’s Definition Of Done?

* [ ] Is the code good in style? (Easy to read, follows good practices and our style guide)
  * Are linters used?
  * Is it clear what a given class/method/function does?
  * Do names reflect what code does?
  * Are functions elegant?

* [ ] The code runs correctly? (Optional)
  * Have you tried the code locally?
  * Are exceptions handled correctly?
  * Are all corner cases handled correctly?
  * Check Java gotchas.
  * Edge cases for ifs, fors, whiles, dates
  * Are there unnecessary while loops?

* [ ] Is this a good enough implementation?
  * Is every line of code used?
  * Does code have unexpected [side effects](https://medium.com/@ryk.kiel/dont-let-your-code-get-out-of-control-avoiding-side-effects-in-python-d68faf26912)?
  * Check usage of third party libraries (production-ready, copyright, etc.)
  * Is the solution performant? (and avoid early optimization since it is the root of all evil)
  * Could the solution be simpler?
  * Look for vulnerabilities ([OWASP](https://owasp.org/www-project-top-ten/) top 10)
  * Is the code properly modularized and [S.O.L.I.D.](https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/)?
  * Is the code properly tested?
  * Do we have some duplicated code?
  * What is missing (docs, comments, metrics, logs, etc.)?
  * Is there a pre-existing code that already solves our problem?

## How Has This Been Tested?

- Java 25, `./gradlew --offline localTest verifyLocalArtifactIsolation`: PASS; `localTest` UP-TO-DATE with 36 existing tests and zero failures/errors/skips; isolation executed successfully.
- `./scripts/validate-repository-contract.sh`, `git diff --check` and required pre-commit checks on changed Markdown: PASS.
- Literal manual startup in a fresh Bash shell fails before Compose with `rio-local is occupied; wait for its owner to finish`. The generated private file was removed; no owned stack was created. Readiness, `localClickHouseIntegrationTest`, the Kafka regression subset and teardown remain pending until the VM is free.
- Authored documentation commits change only Markdown; the required stacked-base merge inherits an existing launcher fix from #1286. No production regression or physical E2E success is claimed.

## Testing contract

* [ ] I added or updated `.testing/impact.json`, or this PR does not change an observable-behavior surface.
* [ ] The impacted/new AT scenarios and focused tests are declared in the manifest.
* [ ] If behavior is unchanged, the manifest includes the reviewed scenarios and a concrete justification.
* [ ] Evidence distinguishes environment (`L0`, `L1`, `F1`) from layer (`UNIT`, `H2_INTEGRATION`, `CONTRACT`, `LOCAL_STACK`, `ECOSYSTEM_STACK`, `SMOKE`).
* [ ] Any mutable run published cleanup evidence; blocked L1/F1 capabilities are declared rather than replaced with L0 evidence.

## Issue

RIO E2E local. No external issue is supplied; operational instructions are in `local/RIO_E2E.md`.

---

## Notas internas — NO van al PR

- Authored documentation commits change only Markdown. The required stacked-base merge also inherits the existing `local/rio_e2e.py` fix from Playmaker #1286 (+2/−1 against the session baseline); the script matches the stacked base, and no runtime code was edited in this pass.
