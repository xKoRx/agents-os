---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[RIO E2E local]]"
  - "[[rio-controlplane-clickhouse]]"
  - "[[Descripción PR — rio-playmaker (E2E local ClickHouse)]]"
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-12"
updated: "2026-10-14"
---

# Descripción PR — rio-controlplane-clickhouse (E2E local)

**Identity:** fury_rio-controlplane-clickhouse · feature/rio-e2e-local-clickhouse-kiss @ dc956a08124a9196c98007e28ce3525b4d3350e1 · base origin/develop @ 3d4a4014f2c73bd8e0ee62a236043d64ec7e5ed3 · 17 commits · 14 files changed, 2021 insertions(+) · validation 2026-10-14.

> [!warning] Physical validation pending
> The shared VM startup command fails while another session owns `rio-local`; this pass claims local checks and documentation publication only.

## Propósito

Keep the PR #342 body as a resource of [[RIO E2E local]].

## Contenido

Body follows `.github/pull_request_template.md`; unchecked gates are not claimed by this documentation pass.

---

## Description

feat: add embedded local Kafka transport for ClickHouse

The local ClickHouse CP uses the existing controllers, services, guards and clients with embedded Kafka delivery. Compose adds ClickHouse 25.8.33.6, Keeper, a single-node cluster and an nginx gateway. The gateway rewrites `format` to `default_format`, which the unchanged CP client needs because direct ClickHouse rejects `format`.

- Explain the CP's port, topics, dedicated SQL account, proxy and substitutions in `local/README.md`.
- Link the complete startup/test/teardown flow to Playmaker's `local/RIO_E2E.md` hub instead of duplicating it.
- State the test boundary: this CP has local adapter tests but no standalone E2E; physical validation is Playmaker's `localClickHouseIntegrationTest` in [#1288](https://github.com/melisource/fury_rio-playmaker/pull/1288).

Supported flows are MergeTree, query actions, MV describe/stop/start with runtime status, refreshable PROVISION and Kafka connector rows. Undeploy is excluded as Playmaker `develop-gap`; S3/Iceberg destinations and MV redeploy parsing are outside this suite. The existing generated-password validation mismatch remains visible.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done
* [x] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [ ] My code follows the style guidelines of this project
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code
* [ ] I have commented portions of my code, particularly in hard-to-understand areas
* [x] I have made corresponding changes to the documentation (`README.md`, `DEV.md`, `CHANGELOG.md`).
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

- Java 25, the README block `./gradlew --offline localBootJar localTest` in a fresh Bash shell: PASS; 57 local tests, zero failures/errors/skips.
- Physical ClickHouse validation is pending: the companion Playmaker manual startup fails before Compose with `rio-local is occupied; wait for its owner to finish`. No owned stack was created.
- `git diff --check` and required pre-commit checks on changed Markdown: PASS.
- This documentation pass changes only Markdown and creates no additional verification/evidence/receipt files.

## Issue

RIO E2E local. No external issue is supplied; the CP guide is `local/README.md`.

---

## Notas internas — NO van al PR

- Documentation-only delta; runtime sources, build files, Compose, scripts and Dockerfiles are unchanged.
