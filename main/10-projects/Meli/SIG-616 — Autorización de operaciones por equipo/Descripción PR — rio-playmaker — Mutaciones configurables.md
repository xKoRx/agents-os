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

# Descripción PR — rio-playmaker — Mutaciones configurables

**Identidad:** `melisource/fury_rio-playmaker` · branch `feature/configurable-component-lifecycle-permissions@2a097e580eab451e85fc749adc83d0c3c1d218ea` · base `develop@d99f89fced9d624c6ae1d9cd8248b03a1e478830` · commits `bbd17a616` y `2a097e580` · 18 archivos, +879/-269 · SIG-616 / SIG-621 / D27–D29 · sin dependencia nueva de otro repo · 2026-10-06: 439 tests focalizados, 96 selectores y regresión de 4.666 tests PASS; cero fallas/errores, dos skips preexistentes en regresión; 97,24% de líneas · [PR #1275](https://github.com/melisource/fury_rio-playmaker/pull/1275), Draft OPEN hacia develop.

> [!warning] **Validación de stack pendiente**
> El contrato agregado terminó exit 1 en health MySQL por `Connection refused` entre macOS y Colima. Loopback y Kafka no se ejecutaron. Cleanup certificado del proyecto propio `rio-playmaker-agentic-17202`.

> [!warning] **Gates remotos y validación desplegada pendientes**
> CI no verificada; sin L1 de ecosistema, deploy de esta rama ni smoke F1/convergencia Fury. No se presenta la evidencia local como validación de runtime.

## Propósito

Conservar junto a SIG-616 la descripción del PR de mutaciones configurables hacia develop, basada en su diff y evidencia real.

## Contenido

Cuerpo en inglés siguiendo las secciones y checklists del template del repositorio. Incluye permisos start/stop de los cinco pushers Fury, permisos configurables de borrado por nombre e inactivación, y aplicabilidad común de ACME cuando existe team y proyecto.

---

## Description

feat: configure pipeline component lifecycle permissions

Playmaker rejects Fury pusher `start`/`stop` requests with 403 because their component/action pairs are missing from the permission configuration. Deletion by component name and inactivation also use hardcoded ACME roles. This PR completes those declarations in `application.yml` and applies one shared rule for Data Products with incomplete ownership. The implementation is self-contained in Playmaker and uses the existing Control Plane Actions.

**Validation pending:** the local testing contract passed all 96 focused selectors, then failed its MySQL health check with `Connection refused` between macOS and Colima. Loopback and Kafka checks did not execute. CI, pre-production deployment, and Fury runtime validation remain unverified; the PR remains a draft.

Changes:

* Add the `fury-pusher` family with `start` and `stop` permissions at `DEV_AND_UP` for `kafka-fury-streams`, `fury-streams-kafka`, `kafka-fury-bigqueue`, `fury-bigqueue-kafka`, and `kafka-fury-kvs`.
* Resolve deletion by name and inactivation through the exact `pipeline:delete-component` and `pipeline:inactivate-component` rules, both `DEPLOYER_AND_UP` by default. Exact lookup keeps these operations independently configurable from component wildcard rules.
* Centralize ACME applicability in `OperationAuthorizationService`: if **either** persisted `teamName` or `projectCode` is null, empty, or whitespace, skip the ACME check. When both are present, require the configured role on the exact team/project and deny requests when ACME cannot be verified. Remove the team/project precheck from deletion and inactivation so they follow the same rule.
* Add unit and HTTP/H2 regressions and update architecture, verification notes, scenarios, and `.testing/impact.json`.

| Configuration scope | Actions | Default access level |
|---|---|---|
| `fury-pusher` family | `start`, `stop` | `DEV_AND_UP` |
| `pipeline` | `delete-component` | `DEPLOYER_AND_UP` |
| `pipeline` | `inactivate-component` | `DEPLOYER_AND_UP` |

Tiger authentication, legacy `systemId` eligibility, lifecycle blockers, locks, audit, and execution/publication checks continue to apply. Removing an exact pipeline lifecycle rule skips its additional ACME check; removing a Fury Action declaration makes that pair unknown and therefore rejected. The ownership exception applies only after a requested Action is recognized.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — stack checks, independent review, CI, and pre-production validation are pending.
* [x] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [x] My code follows the style guidelines of this project — changed Java files passed Google Java Format validation.
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code
* [x] I have commented portions of my code, particularly in hard-to-understand areas
* [x] I updated the applicable canonical documentation (`docs/architecture.md`, `testing.md`, `testing-scenarios.md`, Swagger, README, or CHANGELOG), or documented why it is unchanged. — Architecture and scenarios updated; generated Swagger has no diff because routes and schemas are unchanged.
* [x] After my changes were applied the app is still buildable
* [ ] My changes generate no new warnings (linters, code quality) — full linter and remote code-quality results have not been verified.
* [x] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must
    * Integration testing is recommended
* [x] New and existing unit tests pass locally with my changes
* [x] Any dependent changes have been merged and published in downstream modules — no new downstream change is required; Fury handlers already implement both Actions.
* [x] I have updated my current branch with changes made in develop/master previously — based on `develop@d99f89fce`, verified against the remote.
* [ ] I already deployed this branch in the pre-production environment — deployment has not been performed.

## Code Review checklist (must be completed by the code reviewer)

* [ ] Is it the issue being completed? — independent review pending.
  * Is the Acceptance criteria met?
  * Is the issue ready, according to the project’s Definition Of Done?

* [ ] Is the code good in style? (Easy to read, follows good practices and our style guide) — independent review pending.
  * Are linters used?
  * Is it clear what a given class/method/function does?
  * Do names reflect what code does?
  * Are functions elegant?

* [ ] The code runs correctly? (Optional) — independent review pending; local results and gaps are listed below.
  * Have you tried the code locally?
  * Are exceptions handled correctly?
  * Are all corner cases handled correctly?
  * Check Java gotchas.
  * Edge cases for ifs, fors, whiles, dates
  * Are there unnecessary while loops?

* [ ] Is this a good enough implementation? — independent review pending.
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

Local evidence from 2026-10-06 for HEAD `2a097e580eab451e85fc749adc83d0c3c1d218ea`, based on `develop@d99f89fced9d624c6ae1d9cd8248b03a1e478830`:

* **L0 / UNIT, H2_INTEGRATION:** `./gradlew test --offline --no-daemon --tests 'com.mercadolibre.rio.playmaker.config.ConfiguredActionPermissionProviderTest' --tests 'com.mercadolibre.rio.playmaker.integration.ComponentAuthorizationIntegrationTest' --tests 'com.mercadolibre.rio.playmaker.service.ActionAuthorizationServiceTest' --tests 'com.mercadolibre.rio.playmaker.service.impl.ActionServiceImplTest' --tests 'com.mercadolibre.rio.playmaker.unit.service.OperationAuthorizationServiceTest'` — PASS: 439 tests across five suites, zero failures/errors/skips.
* **L0 / regression:** `./gradlew test jacocoTestReport --offline --no-daemon` — PASS: 4,666 tests across 383 suites, zero failures/errors, two pre-existing skips; 97.24% global line coverage (15,223 covered / 432 missed).
* **L0 / CONTRACT:** `./scripts/validate-repository-contract.sh` and `./scripts/validate-testing-contract.sh --staged` — PASS.
* **L0 / UNIT, H2_INTEGRATION, LOCAL_STACK:** `PLAYMAKER_AGENTIC_MYSQL_PORT=33306 PLAYMAKER_AGENTIC_KAFKA_PORT=39093 ./scripts/run-agentic-testing-contract.sh` — all 96 focused selectors passed; aggregate exit code 1 at `AT-000-S01:L0-LOCAL_STACK` due to MySQL connection refusal. Loopback and Kafka checks did not execute.

HTTP/H2 tests reproduce all ten Fury component/action pairs returning 403 before the configuration change, then 202/PENDING with one stored Action and one published trigger after the fix. They also cover role allow/deny, ACME failure, either ownership field missing, unknown Actions, and configurable lifecycle roles.

Cleanup was certified for Compose project `rio-playmaker-agentic-17202`: no owned containers, networks, or volumes remain. L1 ecosystem and F1 deployed/runtime validation were not performed; local dispatch tests do not establish Fury runtime convergence.

## Testing contract

* [x] I added or updated `.testing/impact.json`, or this PR does not change an observable-behavior surface.
* [x] The impacted/new AT scenarios and focused tests are declared in the manifest.
* [ ] If behavior is unchanged, the manifest includes the reviewed scenarios and a concrete justification. — Not applicable: authorization behavior changes.
* [x] Evidence distinguishes environment (`L0`, `L1`, `F1`) from layer (`UNIT`, `H2_INTEGRATION`, `CONTRACT`, `LOCAL_STACK`, `ECOSYSTEM_STACK`, `SMOKE`).
* [x] Any mutable run published cleanup evidence; blocked L1/F1 capabilities are declared rather than replaced with L0 evidence.

## Issue

[SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616) · [SIG-621 — Authorization by team](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)

---

## Notas internas — NO van al PR

- La autorización explícita del usuario del 2026-10-06 para agregar esta descripción reemplaza la reserva anterior de redactarla personalmente. La restricción de la skill a producir texto no limita esta acción expresamente autorizada sobre el PR existente.
- Skills aplicadas: `human-first-technical-writing` y `pr-description` canónicas. El cuerpo sigue el inglés del template y omite historia de investigación, atribuciones al usuario o conversación con otros desarrolladores.
- El addendum de Slice 5 y D27–D29 registran las decisiones vigentes: ownership opcional con condición OR, lookup exacto para lifecycle por nombre, y familia Fury. Las afirmaciones históricas de cobertura completa anteriores a D29 no describen este HEAD.
- La política OR se decide en `OperationAuthorizationService`; el wrapper resuelve configuración y delega. `AuthorizationUtils` conserva la elegibilidad legacy por `systemId`. Las solicitudes de excepción de freeze conservan sus reglas propias; el PR no cambia su configuración.
- La descripción no implica merge, deploy, cambios de datos ni modificación del Control Plane. No se corrieron nuevas suites para este pedido de documentación; se usó la evidencia ya ejecutada para el mismo diff publicado.
- Evidencia local: `/private/tmp/rio-fury-actions-config-focused-evidence.json`, `/private/tmp/rio-fury-actions-config-regression-evidence.json`, `/private/tmp/rio-fury-actions-config-contract-evidence.json` y `/private/tmp/rio-fury-actions-config-cleanup-evidence.json`; logs correspondientes en `/private/tmp`.
- Worktree limpio. Remoto verificado: develop `d99f89fced9d624c6ae1d9cd8248b03a1e478830` y rama del PR `2a097e580eab451e85fc749adc83d0c3c1d218ea`. El cuerpo vacío se verificó nuevamente antes de escribir. Descripción publicada y lectura posterior idéntica al texto preparado; HEAD/base sin cambios y PR Draft OPEN. Evidencia de publicación: `/private/tmp/rio-playmaker-pr-1275-description-publication.json`.
- La reproducción HTTP/H2 demuestra autorización y dispatch de Playmaker. La ejecución real de stop en Fury requiere validación desplegada posterior.
