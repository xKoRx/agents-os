---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Import de Refreshable Materialized Views externas]]"
  - "[[rio-controlplane-clickhouse]]"
  - "[[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — rio-playmaker]]"
  - "[[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — ads-signals-frontend]]"
  - "[[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — lore]]"
aliases: []
tags:
  - kind/doc
  - project/import-refreshable-materialized-views-externas
created: "2026-10-21"
updated: "2026-10-24"
---

# Descripción PR — rio-controlplane-clickhouse

rio-controlplane-clickhouse · `feature/refreshable-view-import` @ `852628c008ab2953675e2135393bc11e03b77e99` · base `origin/develop` @ `9d7d7a08dacf17ad237e56fc730198febca4bb0f` · 14 commits · 22 files changed, 747 insertions(+), 38 deletions(-) · [draft #362](https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/362) · SIG-700 / SIG-701 · `./gradlew test` 4783 tests, 0 failures, 1 skipped (2026-10-24) · versión de prueba `0.0.2-import-ref-view-ch`.

> [!warning] Bloqueantes
> **Orden de rollout:** CP y Playmaker deben estar desplegados antes del frontend; el frontend llama al describe/import que este PR habilita.
> **Hermano sin push:** el PR de Playmaker #1328 tiene commits locales sin publicar por el gate Cleric del repo; la versión de prueba de Playmaker vigente es `0.0.1-import-ref-view-ch`, que ya contiene el permiso de runtime.

## Propósito

Conservar el cuerpo verificable del PR junto al proyecto, con el template del repo y enlazado a los PRs hermanos.

## Contenido

Cuerpo del PR listo para pegar, seguido de notas internas que no van al PR.

---

## Description

`feat(clickhouse): import external refreshable views` lets the ClickHouse control plane adopt a refreshable materialized view that already exists in ClickHouse instead of recreating it. When a `clickhouse-ref-view` deployment carries `externalReference=true`, the control plane reconciles the view, marks it as imported by Rio and returns the credential preloaded for its owner; the view, its target table and their data are left untouched. This PR is one part of SIG-700: the full flow also needs [Playmaker #1328](https://github.com/melisource/fury_rio-playmaker/pull/1328) and [frontend #816](https://github.com/melisource/fury_ads-signals-frontend/pull/816).

The feature was developed together with the local RIO ecosystem E2E ([Playmaker #1332](https://github.com/melisource/fury_rio-playmaker/pull/1332)): the whole import journey runs in Lore against local Playmaker, this control plane and the frontend, using the browser drag-and-drop tool added in [Lore #21](https://github.com/melisource/fury_lore/pull/21).

Changes:
*  `DeployRefreshableView`: for an existing view, reconcile SQL drift first (same order as `DeployMaterializedView`) and import it when Rio does not manage it yet. An external reference whose view no longer exists fails instead of being recreated.
*  `AlterMvRefreshCommand`: extract the query only from the top-level `AS`, respecting strings, identifiers, comments and parenthesis depth. An optional literal `COMMENT` may follow the body; CTE capture, unbalanced parentheses and trailing text are rejected.
*  `ImportMatViewCommand.executeStrict`: the refreshable path fails if the import marker cannot be persisted. The classic materialized view import keeps best-effort marking and logs the cause.
*  `MatViewImportController` accepts the documented `plaintextPassword` field.
*  Local scope only: `LocalCkaasEncryptionKey` (AES-GCM) and an in-memory ciphertext store let the local stack preload import credentials without KVS or CKAAS. Deployed scopes keep KVS and CKAAS unchanged.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — pending owner review of SIG-700 open questions PA-1 to PA-5
* [x] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [x] My code follows the style guidelines of this project
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code
* [x] I have commented portions of my code, particularly in hard-to-understand areas
* [x] I have made corresponding changes to the documentation (`README.md`, `DEV.md`, `CHANGELOG.md`). — `local/README.md` documents the local credential store
* [x] After my changes were applied the app is still buildable
* [ ] My changes generate no new warnings (linters, code quality) — not measured separately from the build
* [x] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must
    * Integration testing is recommended
* [x] New and existing unit tests pass locally with my changes
* [ ] Any dependent changes have been merged and published in downstream modules — sibling PRs #1328 and #816 are open
* [x] I have updated my current branch with changes made in develop/master previously
* [ ] I already deployed this branch in the pre-production environment — test version created, not deployed

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

* `./gradlew test` (JDK 25): 4783 tests, 0 failures, 1 skipped (`HYDRA_STACK_EXPORT_DIR`-gated export).
* Local E2E with the Playmaker runner, `.lore/ecosystem/rio-ecosystem all clickhouse-refreshable-view-import`: Lore run `run_mvmmx1oa2d7d9a404d` passed 5/5 scenarios (smoke, import and save, first deploy, reprovision, read-only after deploy) and 8/8 backend checks. View, source and target UUIDs are unchanged, the DDL is preserved except for the import comment, the target sentinel row and the owner user are kept, the first deploy returns the owner credential and the reprovision returns `ALTER_MV` without altering the table.
* Test version [0.0.2-import-ref-view-ch](https://web.furycloud.io/rio-controlplane-clickhouse/versions/detail/0.0.2-import-ref-view-ch) from `852628c0`. Deploy this control plane and Playmaker before the frontend.

## Issue

[SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700) · [SIG-701](https://spellbook.adminml.com/projects/SIG/specs/SIG-701)

---

## Notas internas — NO van al PR

- PA-1 a PA-5 siguen abiertas; PA-2 está fijada sólo por el test de paridad (reconciliar antes del ownership).
- Riesgo de diseño heredado, con paridad en el camino clásico: la marca se persiste antes de entregar las credenciales; si el resultado se reintenta, el segundo intento devuelve `ALTER_MV` sin credenciales. Decisión del owner.
- La forma sin paréntesis acepta texto residual después del `COMMENT` (comportamiento igual a develop; no se cambió por no ser regresión).
- Correcciones de la auditoría del 2026-10-24: tests que matan los mutantes de profundidad del `AS` y de balance del SELECT (`6ed1adb5`), y el warn de la marca clásica vuelve a registrar la excepción (`852628c0`).
