---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
project: "[[SIG-600 — Borrado seguro de Data Products]]"
related: ["[[SIG-600 — Borrado seguro de Data Products]]", "[[rio-playmaker]]", "[[Hotfix — Borrado de DP con componentes eliminados]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# Descripción PR — rio-playmaker — Hotfix componentes eliminados

Repo `melisource/fury_rio-playmaker` · branch `hotfix/dp-delete-ignore-deleted-components-master@9118cbe7f953a446b83432a410933ccf89cee0e2` · base `master@7dbc49ccf8bb49a6998f94a55da011e54c53f661` · 1 commit · 5 archivos, +115/−193 · validación sobre master 2026-10-06: 4.400 tests, 0 fallas/errores, 2 skips; 97,21% line coverage.

> [!info] Destino autorizado
> El owner autorizó publicar el hotfix y abrir el PR draft contra master. Preparación original sobre develop conservada localmente; entrega final portada y validada sobre master.

PR remoto: [#1267 — draft contra master](https://github.com/melisource/fury_rio-playmaker/pull/1267).

Versión solicitada por el owner: [0.0.1-delete-dp-fix](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.1-delete-dp-fix), `FINISHED` desde el HEAD exacto de esta rama; [build #1788](https://rp-builds-java.furycloud.io/blue/organizations/jenkins/rio-playmaker/detail/rio-playmaker/1788/pipeline/). Fury registra `run_test=false` pese a la solicitud normal sin `--no-tests`; la evidencia de 4.400 tests corresponde a la suite local. Esta referencia se conserva en la nota; no se editó el cuerpo remoto del PR ni se publicó un comentario. Sin deploy.

## Propósito

Conservar la descripción del hotfix como recurso de [[SIG-600 — Borrado seguro de Data Products]].

## Contenido

Cuerpo del PR con el template de Playmaker, aceptación autorizada por el owner y evidencia local del commit.

---

## Description

fix(data-products): ignore deleted components in delete blockers

Deleting a Data Product can return HTTP 409 after its components have been logically deleted because the deployment blocker still includes their historical rows. The query now excludes components with `deleted_at` set or status `Deleted`, ignoring case, so those rows no longer prevent the Data Product soft delete.

* Keep HTTP 409 for a live component with `deploy_requested` or `deploy_completed`, including Data Products that also contain deleted components. `Inactive` without `deleted_at` remains a live component for this guard.
* Add 17 controller/H2 regression cases that observe the DELETE outcome, unchanged state on conflict and retained deployment history; document AT-010-S19 and scope the testing manifest to this fix.

This is a self-contained Playmaker hotfix. It preserves authorization, ownership locking, cascade, imported-component handling and deployment records; no migration or downstream change is required. Branch: `hotfix/dp-delete-ignore-deleted-components-master`; base: `master@7dbc49ccf8bb49a6998f94a55da011e54c53f661`; commit: `9118cbe7f953a446b83432a410933ccf89cee0e2`.

<details>
<summary>Developer checklist</summary>

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — human review and deployed validation remain pending.
* [x] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [x] My code follows the style guidelines of this project
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code
* [x] I have commented portions of my code, particularly in hard-to-understand areas — the repository method documents deletion semantics.
* [x] I updated the applicable canonical documentation (`docs/architecture.md`, `testing.md`, `testing-scenarios.md`, Swagger, README, or CHANGELOG), or documented why it is unchanged — architecture and scenarios updated; API shape and test environment are unchanged.
* [x] After my changes were applied the app is still buildable
* [ ] My changes generate no new warnings (linters, code quality) — remote analysis pending; local compilation passed with existing runtime/Gradle deprecation warnings.
* [x] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must — existing DataProductServiceImplTest passes; the new native SQL predicates are exercised through Spring/H2 rather than repository mocks.
    * Integration testing is recommended — 17 new controller/H2 cases.
* [x] New and existing unit tests pass locally with my changes
* [x] Any dependent changes have been merged and published in downstream modules — no downstream dependency.
* [x] I have updated my current branch with changes made in develop/master previously
* [ ] I already deployed this branch in the pre-production environment — no deploy was performed.

</details>

<details>
<summary>Code Review checklist</summary>

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

</details>

## How Has This Been Tested?

Validation was rerun on the master-based hotfix. All runs used L0 with Java 25; the native query was exercised through controller/Spring/H2 integration. The tested source was committed unchanged as `9118cbe7f953a446b83432a410933ccf89cee0e2`.

* Baseline reproduction on the initial develop base (the original blocker query is identical on master): the 17 new cases produced eight expected failures (`200` expected, `409` received), with no errors or skips; the live-component controls already passed.
* `./scripts/validate-repository-contract.sh` and `git diff --check`: PASS.
* `./scripts/run-agentic-testing-contract.sh --plan` and `./scripts/run-agentic-testing-contract.sh`: PASS for both declared selectors, including DataProductControllerIntegrationTest and DataProductServiceImplTest.
* `./gradlew test jacocoTestReport`: 4,400 tests, zero failures/errors and two pre-existing skips. JaCoCo line coverage: 97.21% (15,240/15,677).

Each H2 case runs in a transaction that rolls back its fixture changes. No remote resources were created or mutated. MySQL/Fury execution and deployment remain unverified. Full regression regenerates the OpenAPI mirror with only an EOF newline difference; that formatting difference was restored, leaving no API diff.

## Testing contract

* [x] I added or updated `.testing/impact.json`, or this PR does not change an observable-behavior surface.
* [x] The impacted/new AT scenarios and focused tests are declared in the manifest.
* [ ] If behavior is unchanged, the manifest includes the reviewed scenarios and a concrete justification — not applicable: deletion behavior changes for logically deleted components.
* [x] Evidence distinguishes environment (`L0`, `L1`, `F1`) from layer (`UNIT`, `H2_INTEGRATION`, `CONTRACT`, `LOCAL_STACK`, `ECOSYSTEM_STACK`, `SMOKE`).
* [x] Any mutable run published cleanup evidence; blocked L1/F1 capabilities are declared rather than replaced with L0 evidence.

## Issue

[SIG-600 — Delete Data Products](https://spellbook.adminml.com/projects/SIG/specs/SIG-600). This hotfix addresses the owner's reported 409 after component logical deletion; it does not complete the additional blockers tracked by SIG-600/SIG-643.

---

## Notas internas — NO van al PR

- Scope autorizado: excluir componentes Deleted o con deleted_at del blocker de deployments. No cambia filtros de is_active/deleted_at del deployment ni interpreta Inactive sin timestamp como Deleted.
- `.testing/impact.json` se reemplaza por el manifiesto de este diff; las selecciones acumuladas del baseline no pertenecen a esta entrega. Regresión completa ejecutada por tratarse de un repository compartido.
- Auditoría de tono antes de publicar: texto causal, concreto, profesional y sin lenguaje confrontacional; la evidencia distingue source/local de runtime remoto.
- La revisión automática bloqueó la publicación inicial; el owner autorizó después explícitamente push y PR contra master. Publicado PR draft #1267 con HEAD `9118cbe7f953a446b83432a410933ccf89cee0e2`; la rama preparatoria sobre develop se conserva local.
- Review externa/Zord no ejecutada: el entregable es implementación con self-review y PR draft, no una revisión formal del PR. No se publican comentarios de review.
