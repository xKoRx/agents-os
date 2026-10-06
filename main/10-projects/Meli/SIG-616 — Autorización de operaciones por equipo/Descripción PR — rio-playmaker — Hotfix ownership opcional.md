---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
  - "[[rio-playmaker]]"
aliases: []
tags:
  - kind/doc
  - project/sig-616-operation-authorization
created: "2026-10-06"
updated: "2026-10-06"
---

# Descripción PR — rio-playmaker — Hotfix ownership opcional

**Identidad:** `melisource/fury_rio-playmaker` · branch `hotfix/optional-dp-owner-permissions@d0135ae67c7054419a9fefb1ae2cd41040656405` · base `master@5e4e2089b9973785097a91daaf507516aff6bfc0` · dos commits · siete archivos, +237/-50 · SIG-616 / decisión D27 · sin dependencias downstream · 2026-10-06: once selectores y stack MySQL PASS; 4.453 tests, cero fallas/errores, dos skips, 97,21% de líneas; cleanup PASS · [PR #1273](https://github.com/melisource/fury_rio-playmaker/pull/1273), cinco checks obligatorios PASS; CI #5924 completada y versión 202610.5.2-hotfix-1 FINISHED.

## Propósito

Conservar la descripción del hotfix y su evidencia junto al proyecto SIG-616.

## Contenido

Cuerpo del PR hacia master, basado en el template del repositorio.

---

## Description

fix: skip configured permissions for incomplete data product ownership

Configured mutations currently return 403 before calling ACME when a persisted Data Product lacks a team or project. This hotfix applies the additional project permission check only when both values are present, as requested by the owner. It is a self-contained fix targeting `master`.

Changes:

* Skip the configured project permission check when `teamName` or `projectCode` is null or blank; complete ownership still requires the configured ACME role.
* Route declared mutating Action dispatch through the same applicability condition. Tiger authentication, unknown Action rejection, precreation restrictions, and existing operation-specific checks remain in place.
* Add unit and HTTP/H2 regressions for incomplete ownership, including both reported PATCH paths, and update architecture, scenarios, and the testing manifest.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — independent review and remote smoke are pending.
* [x] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) 
* [x] My code follows the style guidelines of this project
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code — implementation and compatibility were reviewed locally; independent review is pending.
* [x] I have commented portions of my code, particularly in hard-to-understand areas
* [x] I updated the applicable canonical documentation (`docs/architecture.md`, `testing.md`, `testing-scenarios.md`, Swagger, README, or CHANGELOG), or documented why it is unchanged.
* [x] After my changes were applied the app is still buildable 
* [ ] My changes generate no new warnings (linters, code quality) — baseline warning counts were not compared.
* [x] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must
    * Integration testing is recommended
* [x] New and existing unit tests pass locally with my changes
* [x] Any dependent changes have been merged and published in downstream modules — self-contained; no downstream change is required.
* [x] I have updated my current branch with changes made in develop/master previously
* [ ] I already deployed this branch in the pre-production environment — no deployment was performed.

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

Verified on 2026-10-06 for HEAD `d0135ae67c7054419a9fefb1ae2cd41040656405`, after merging `master@5e4e2089b9973785097a91daaf507516aff6bfc0`.

* `./scripts/run-agentic-testing-contract.sh --plan`: PASS; eleven focused selectors and one capability check.
* `./scripts/run-agentic-testing-contract.sh`: PASS for all eleven selectors (L0/UNIT, H2_INTEGRATION, CONTRACT) and `AT-000-S01:L0-LOCAL_STACK` with isolated MySQL.
* `./gradlew test jacocoTestReport --offline --no-daemon`: PASS; 4,453 tests, 381 suites, zero failures/errors, two existing skips (L0/FULL_REGRESSION). Global line coverage 97.21%; `ActionAuthorizationService` line and branch coverage 100%.
* `./scripts/validate-repository-contract.sh` and `./scripts/validate-repository-contract.sh --staged`: PASS; `./scripts/validate-testing-contract.sh --staged`: PASS.
* `git diff master...HEAD --check`: PASS; working tree clean.
* Cleanup PASS: owned Compose project `rio-playmaker-agentic-49666` removed; no containers, networks, or volumes remain for that project.
* Limits: no L1 ecosystem runner, F1 smoke, or deployment was executed. Remote CI is tracked on this PR; its results do not imply a remote smoke.

* Remote CI: [Fury pipeline #5924](https://rp-ci-java.furycloud.io/job/rio-playmaker/5924/) completed; all five required checks passed on this HEAD: `continuous-integration`, `code-coverage`, `dependencies`, `static-analyzer`, and `workflow`. Verified in GitHub on 2026-10-06.
* Fury automatically built `202610.5.2-hotfix-1` for this exact HEAD and reports `FINISHED` ([build #1793](https://rp-builds-java.furycloud.io/blue/organizations/jenkins/rio-playmaker/detail/rio-playmaker/1793/pipeline/)). No deployment was performed.
* [Code Scanning run #5944](https://github.com/melisource/fury_rio-playmaker/actions/runs/37527255642) failed at startup because enterprise policy blocks `actions/github-script@v7`. This workflow is unchanged from `master`; no scan was executed.

## Testing contract

* [x] I added or updated `.testing/impact.json`, or this PR does not change an observable-behavior surface.
* [x] The impacted/new AT scenarios and focused tests are declared in the manifest.
* [ ] If behavior is unchanged, the manifest includes the reviewed scenarios and a concrete justification. — not applicable: this hotfix changes behavior.
* [x] Evidence distinguishes environment (`L0`, `L1`, `F1`) from layer (`UNIT`, `H2_INTEGRATION`, `CONTRACT`, `LOCAL_STACK`, `ECOSYSTEM_STACK`, `SMOKE`).
* [x] Any mutable run published cleanup evidence; blocked L1/F1 capabilities are declared rather than replaced with L0 evidence.

## Issue

[SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616). Hotfix requested by the owner after the failed component update.
---

## Notas internas — NO van al PR

- El owner autorizó explícitamente omitir sólo el guard adicional ante equipo o proyecto ausente. Esta decisión D27 reemplaza la exigencia de ownership completo de los slices afectados; los checks independientes conservan su flujo.
- El hotfix integra master por merge conservador y mantiene la unión de escenarios del manifiesto. No hay cambios de dependencias, versión ni despliegue.
- PR #1273 creado no draft con base master y HEAD d0135ae67c7054419a9fefb1ae2cd41040656405. Los cinco checks obligatorios pasaron en CI #5924; la versión automática 202610.5.2-hotfix-1 está FINISHED para el mismo HEAD. Code Scanning #5944 falló al arrancar porque la política corporativa bloquea actions/github-script@v7; el workflow es idéntico a master. Aprobación humana requerida por GitHub; sin merge ni deploy.
