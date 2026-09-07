---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
  - "[[Descripción PR — rio-sdk-events]]"
  - "[[Documento técnico — rio-playmaker — visión general]]"
aliases:
  - PR rio-playmaker Crear Context generado por Zord
  - descripción PR Playmaker zord authoring
tags:
  - kind/doc
  - project/crear-context
  - application/rio-playmaker
created: "2026-08-27"
updated: "2026-08-27"
---

# Descripción PR — rio-playmaker — Crear Context (zord authoring)

**PR:** [#1068](https://github.com/melisource/fury_rio-playmaker/pull/1068) (draft) · **Repo:** `rio-playmaker` · **Branch:** `feature/new-component-context` @ `658f8f6153eb5249749b8b004f500e38450aa86d` · **Base:** `develop` @ `28b929c9e48a49c2d207bb2c05d2e7c0dd8b61d7` · **Commits:** 17 · **Diff:** 29 archivos, +3808/−27 · **Specs:** SIG-573 funcional y SIG-590 técnica en `.sdd/features/new-component-context/` · **Dependencia:** `rio-sdk-events:1.4.0` · **Suite Playmaker:** no ejecutada en esta sesión; la suite validada fue la del zord authoring, 458 tests PASS.

> [!warning] Bloqueante de alcance — el diff incluye cambios ajenos a Crear Context
> La branch agrega el script de importación de tablas externas de ClickHouse, su harness de pruebas y cambios en `docs/specs/swagger.yaml`, además del Context. Revisar si esos cambios deben separarse antes del merge.

> [!warning] Higiene de working tree — hay salida local sin trackear
> `graphify-out/` aparece como `??` en el repo y no forma parte del diff. Limpiarlo o dejarlo fuera antes de preparar el PR final.

> [!note] Evidencia de validación
> El zord generó esta descripción leyendo diff, commits, specs, tasks y progreso. No se ejecutó `./gradlew test` en esta sesión; por eso la sección de pruebas sólo afirma lo observable en el diff y deja visible la ausencia de output de comandos.

## Propósito

Descripción nueva del Pull Request de `rio-playmaker` para [[Crear Context]], generada mediante la recipe `zord author pr-description` sobre la branch vigente y lista para revisión humana antes de copiarla a GitHub.

## Contenido

Identidad verificable de la branch · bloqueantes de alcance e higiene · cuerpo del PR siguiendo el template `.github/pull_request_template.md` · foco de revisión · evidencia disponible y límites epistemológicos.

## Fuentes

- `rio-playmaker/.sdd/features/new-component-context/1-functional/spec.md` — SIG-573.
- `rio-playmaker/.sdd/features/new-component-context/2-technical/spec.md` — SIG-590.
- `rio-playmaker/.sdd/features/new-component-context/3-tasks/tasks.md` — plan de implementación.
- `rio-playmaker/.sdd/features/new-component-context/progress.md` — estado declarado de tasks y gates.
- `rio-playmaker` — diff y commits de `develop...HEAD`, además de `.github/pull_request_template.md`.

---

## Description

feat: add component deployment context

Pipeline BigQueue deployment triggers now carry an ephemeral `context` snapshot. The SDK field remains optional for compatibility with older producers, but Playmaker requires and validates a complete context before publishing each trigger. It gives control planes the deploying data product and component, the component’s last completed deployment, and its active upstream/downstream topology without changing `params`.

The snapshot separates user configuration (`inputs`) from control-plane-produced values (`outputs`). For each related component, both maps are resolved from the same service slot; unresolved or unauthorized values are published as empty maps while preserving the neighbour’s identity and topology.

Cross-data-product values are fail-closed: Playmaker reads an original component only when an approved authorization binds the imported-copy/original pair to the deploying data product. Missing values preserve the neighbour with empty maps, but a structural or derivation failure that prevents a valid context marks only that component’s deployment as failed and suppresses its trigger; other components in the batch continue.

Changes:

* Upgrades `rio-sdk-events` from `1.3.1` to `1.4.0` and attaches optional context to `DeploymentTriggerMessage`.
* Adds context derivation, input/output resolution, authorization gating, deterministic environment matching, complete trigger validation, and bounded metrics for derivation and suppressed values.
* Adds repository queries for active relations, completed deployments, service slots, environments, and approved import pairs.
* Adds an external ClickHouse-table import script, its isolated fake-`curl` test harness, and usage documentation.
* Updates Swagger documentation for component-catalog filters and migration prerequisites.

Behavior that does not change:

* Existing `params` remain unchanged.
* Control planes that do not consume `context` can continue processing the optional field.
* A context-derivation or contract-validation failure fails only the affected component’s deployment and prevents its trigger from being published; it does not stop the remaining batch.
* Context is calculated at dispatch time; it is not persisted or refreshed when the consumer receives the message.

Risks and review focus:

* Context can carry configuration and deployment outputs to deployment-trigger consumers. Review the cross-data-product authorization gate and ensure consumers do not log context values.
* Related-component values may be empty when a slot, matching environment, authorization, or resolvable persisted document is unavailable.
* The implementation uses `component.componentTemplateCode` for `context.component.type`; the technical design states this should match the trigger routing type. Review whether these can diverge.
* This diff includes the ClickHouse import utility and Swagger changes in addition to the component-context feature; review their scope and release intent independently.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done
* [ ] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [ ] My code follows the style guidelines of this project
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [ ] I have performed a self-review of my own code
* [ ] I have commented portions of my code, particularly in hard-to-understand areas
* [ ] I have made corresponding changes to the documentation (`README.md`, `DEV.md`, `CHANGELOG.md`).
* [ ] After my changes were applied the app is still buildable
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
  * Look for vulnerabilities ([OWASP](https://owasp.org/www-project-top-ten/) top 10
  * Is the code properly modularized and [S.O.L.I.D.](https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/)?
  * Is the code properly tested?
  * Do we have some duplicated code?
  * What is missing (docs, comments, metrics, logs, etc.)?
  * Is there a pre-existing code that already solves our problem?

## How Has This Been Tested?

Validation evidence in the diff:

* Added unit tests for context metrics, value resolution, context derivation, dispatch propagation, and BigQueue message publication.
* Updated an orchestration integration test to assert that the published trigger contains data-product and component context.
* Added isolated shell tests for the ClickHouse import script, including input validation, allowlisted hosts, dry-run behavior, idempotency, deployment polling, rollback, and type normalization.

No test-command output or completed Playmaker test run was provided with the sources.

## Issue

SIG-573 / SIG-590

---

## Notas internas — NO van al PR

- La branch está limpia respecto de cambios tracked, pero `graphify-out/` es un directorio no trackeado que debe permanecer fuera del PR.
- El diff real es de 29 archivos y +3808/−27, no de la identidad histórica registrada en notas anteriores; esta nota usa los SHAs y la base observados el 2026-08-27.
- La spec técnica describe que `context.component.type` debe usar la misma clave de routing del trigger, mientras el diff usa `componentTemplateCode`; la discrepancia requiere revisión.
- El zord no ejecuta tests ni publica el PR; la frase de validación distingue los tests agregados visibles en el diff de una corrida efectiva de `./gradlew test`.
- La salida fue producida por `zord author pr-description` desde `feature/zords-technical-authoring`, con el writer `human-first-technical-writing` y modelo `gpt-5.6-terra` en reasoning effort `high`.
