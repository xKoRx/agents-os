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
updated: "2026-10-07"
---

# Descripción PR — rio-playmaker — Mutaciones configurables

**Identidad:** `melisource/fury_rio-playmaker` · branch `feature/configurable-component-lifecycle-permissions@526c1115cefd6e14079d1f825507063088915b24` · base `develop@a4e2829ad92a9d181e1a728db25e5f7305abab80` · commits `bbd17a616`, `2a097e580`, `1be7fb63b`, `47c2344c3`, `933eeb8d0`, merge `da9bb4312`, fix `0a5a01f76` y merge `526c1115c` · 26 archivos, +2114/-399 · SIG-616 / SIG-621 / D27–D31 · 2026-10-07: 93 selectores y 4.703 tests PASS; cero fallas/errores, dos skips; JaCoCo 97,24% y helper strict-local 97,01% · [PR #1275](https://github.com/melisource/fury_rio-playmaker/pull/1275), OPEN y MERGEABLE; CI #6029: cinco checks SUCCESS; PR coverage 97,72%, helper 97,01% y overall MeliCov 94,92%.

> [!warning] **Validación de stack pendiente**
> El contrato agregado terminó exit 1 en health MySQL por `Connection refused` entre macOS y Colima. Loopback y Kafka no se ejecutaron. Cleanup certificado del proyecto propio `rio-playmaker-agentic-48924`.

> [!info] **Versión de prueba actual**
> [`0.0.2-acme-test3`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.2-acme-test3) terminó `FINISHED` en build #1811 desde `526c1115cefd6e14079d1f825507063088915b24`, con `type=test` y `run_test=true`. Incluye todas las correcciones del PR y el merge actual. Lista para desplegar en test3; sin despliegue ni validación runtime. Sustituye para estas pruebas a `0.0.1-acme-actions-complete`.

## Propósito

Explicar el alcance funcional del PR #1275: permisos faltantes de Fury, política ACME con proyecto/team incompleto y borrado/inactivación configurables; distinguir el alcance adicional de ClickHouse y las validaciones pendientes.

## Contenido

Cuerpo en inglés siguiendo el template del repositorio. Explica el antes/después de autorización y el fix de binding de conectores con el ejemplo A→B. Identifica los tres permisos ClickHouse como alcance adicional, el cambio del controller como documentación y el script como prueba local. No declara resuelto el timeout de importación.

---

## Description

fix: complete action permissions and bind connector targets

Restore authorization for existing Fury start/stop operations that Playmaker rejects because their permissions are missing. Also apply the agreed ownership policy: require ACME team/project permissions only when the Data Product has both values assigned. This PR changes Playmaker authorization and dispatch; it uses the existing Control Plane implementations.

**Test version:** [`0.0.2-acme-test3`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.2-acme-test3) finished successfully in build #1811 from the current HEAD `526c1115cefd6e14079d1f825507063088915b24`, with build tests enabled. Ready to deploy to test3; deployment and runtime validation have not been performed. The local stack check remains blocked at MySQL health.

Main changes:

* **Fury:** allow the existing `start`/`stop` operations for all five Fury pusher types by adding their ten missing permission declarations at `DEV_AND_UP`.
* **Project/team:** skip the additional ACME check when either ownership field is missing or blank. With both assigned, require the configured role on that exact team/project and deny ACME failures. Tiger and business restrictions still apply.
* **Delete/inactivate:** move their roles into the exact `pipeline:delete-component` and `pipeline:inactivate-component` configuration rules, both `DEPLOYER_AND_UP` by default.

**Additional ClickHouse scope:** enable existing connector pause/resume (`DEV_AND_UP`) and materialized-view describe (Tiger-only read). For pause/resume, prevent a request authorized for component A from operating B through client `data`; bind the target and routing to A's persisted deployment before publication. Resolve only the required routing fields, so unrelated Kafka provisioning references no longer block the action when the source is stopped. Missing or conflicting target/routing data is still rejected.

**Supporting changes:** `ActionController` documents the 400/409 errors in Swagger. The script and fixture test serialized messages against actual ClickHouse handlers locally, with fresh fixtures for each run; `scripts/` already existed. These changes do not alter controller routes or execution.

Table-import failures and `Warehouse lookup timed out — please try again` remain unresolved by this PR. No Control Plane code is changed.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — stack checks, independent review and deployed validation are pending.
* [x] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [x] My code follows the style guidelines of this project — changed Java passed formatting, Checkstyle and PMD.
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code
* [x] I have commented portions of my code, particularly in hard-to-understand areas
* [x] I updated the applicable canonical documentation (`docs/architecture.md`, `testing.md`, `testing-scenarios.md`, Swagger, README, or CHANGELOG), or documented why it is unchanged. — architecture, scenarios and Swagger updated.
* [x] After my changes were applied the app is still buildable
* [x] My changes generate no new warnings (linters, code quality) — changed Java passed Checkstyle/PMD and the remote static-analyzer check passed.
* [x] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must
    * Integration testing is recommended
* [x] New and existing unit tests pass locally with my changes
* [ ] Any dependent changes have been merged and published in downstream modules — no new Control Plane code is required; deployed compatibility remains unverified.
* [x] I have updated my current branch with changes made in develop/master previously — merged `develop@b0b076b51`.
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

Evidence from 2026-10-07 for HEAD `526c1115cefd6e14079d1f825507063088915b24`, based on `develop@a4e2829ad92a9d181e1a728db25e5f7305abab80`:

* **L0 / UNIT, H2_INTEGRATION, CONTRACT:** `./scripts/run-agentic-testing-contract.sh` — all 93 focused selectors passed, with no test-cache hits. The two changed suites passed 274 tests, including the stopped unrelated dependency, unresolved required routing, target conflicts, missing ownership, role denial and ACME failure cases.
* **L0 / FULL_REGRESSION, COVERAGE:** `./gradlew test jacocoTestReport --offline --no-daemon` — 4,703 tests, zero failures/errors and two pre-existing skips; global JaCoCo line coverage 97.24%, helper strict-local coverage 97.01% (partial branch lines count as uncovered). All five checks passed in CI #6029 for this HEAD. PR coverage is 97.72%, helper coverage 97.01%, and overall MeliCov coverage 94.92%.
* **L0 / CONSUMER_CONTRACT, prior fix evidence:** `JAVA_HOME=/Users/rjara/Library/Java/JavaVirtualMachines/corretto-25.0.4/Contents/Home ./scripts/run-connector-action-contract-check.sh /Users/rjara/fuentes/rio-controlplane-clickhouse` — 36 HTTP/H2 cases and six actual-handler checks passed using ClickHouse commit `97fcf076152c58711e7c5b483cc58555647e6423`, with mocked SQL/KVS adapters. Confirms bound target selection and no publication for rejected A→B requests. Executed at `0a5a01f76`; producer, fixture and all 21 PR code/config/script files are byte-identical in the current merge. JDK 25 and fresh producer fixture generation are required. Cleanup certified; no deployed DDL is claimed.
* **L0 / REPOSITORY_CONTRACT:** `./scripts/validate-repository-contract.sh`, `./scripts/validate-testing-contract.sh --staged`, `./scripts/run-agentic-testing-contract.sh --plan`, `bash -n scripts/run-connector-action-contract-check.sh` and `git diff --check` passed. `pre-commit run` passed security/PII, Java formatting, Checkstyle and PMD.
* **L0 / LOCAL_STACK, blocked:** `PLAYMAKER_AGENTIC_MYSQL_PORT=33316 PLAYMAKER_AGENTIC_KAFKA_PORT=39093 ./scripts/run-agentic-testing-contract.sh` — aggregate exit 1 at MySQL health (`Connection refused` between macOS and Colima). Loopback/Kafka did not execute. Cleanup verified: no owned containers, networks or volumes remain for `rio-playmaker-agentic-48924`.

The merge incorporates upstream #1270 from develop; its freeze requester controller/DTO are part of the base and are excluded from this PR diff. L1 ecosystem and F1 deployed/runtime validation remain pending. The materialized-view start/stop payload contract is unchanged.

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

- Se completó el PR existente y su rama, preservando los fixes previos de D27–D29. Se agregaron tres reglas ClickHouse y sus pruebas; el source del Control Plane no se modifica.
- Skills canónicas aplicadas: `pr-description`, `human-first-technical-writing` y `agents-os-agent-run-register`. La publicación del PR y creación de la versión están autorizadas por el pedido directo del usuario.
- Control Plane ClickHouse auditado en `53b5c087b21f98e10ca5561c11a823e91e3538b7`, handlers `PauseKafkaConnectorAction`, `ResumeKafkaConnectorAction` y `DescribeMatViewAction`; Control Plane Fury auditado en `e25d37d24464c22ae29440e748ec99567b134f78`. La existencia en source no prueba el comportamiento de un deployment remoto.
- Hooks de seguridad, PII, formato, Checkstyle y PMD PASS para los dos archivos de pruebas modificados. La limpieza del stack se verificó por labels del Compose project propio.
- Evidencia sanitizada: `/private/tmp/playmaker-actions-complete-test-evidence.json`, `/private/tmp/playmaker-actions-complete-pr-status.json` y `/private/tmp/playmaker-actions-complete-version-status.json`; logs en `/private/tmp/playmaker-actions-complete-*.log`.
- Fix de review `47c2344c3`: ID/routing vinculado al target autorizado, 12 archivos del segmento. Push y cuerpo publicados y verificados por lectura en PR #1275; worktree limpio, develop sigue `d99f89fce`. CI 5990 para ese HEAD: tests/dependencies/static/workflow SUCCESS, code-coverage FAILURE (78,82% < 90%). Sin merge ni deploy.
- Seguimiento de código fuente: start/stop de materialized views también usa selectores de data sin vínculo al envelope. Se consultó al usuario si incluirlo; el scope actual son los dos comentarios de PR y no se declara ese caso corregido.
- Evidencia nueva: `/private/tmp/playmaker-pr1275-target-test-evidence.json`; logs `/private/tmp/playmaker-pr1275-*.log`. El consumidor de contrato se fijó en `97fcf076`.

- Cleanup final certificado: stack `rio-playmaker-agentic-22154`, archives del contrato y worktree CP propio limpio eliminado; checkout principal CP preservado. Hooks post-commit PASS.

- Follow-up `933eeb8d0` pusheado: 32 tests unitarios nuevos, sin cambios de producción. 97 selectores y regresión final 4.752 tests PASS; helper strict-local 93,75%, global JaCoCo 97,26%. Hooks pre/post-commit PASS; stack MySQL exit 1 y cleanup certificado para rio-playmaker-agentic-50666. Los cinco checks remotos del nuevo HEAD pasaron en CI 5994; coverage PR 95,29%, helper 93,75% y global MeliCov 94,93%.
- Replies publicadas y verificadas: policy 4208369370 y binding 4208369705. La última quedó actualizada con el resultado remoto del nuevo HEAD; reply y body final del PR verificados por lectura exacta.

- Conflictos: merge `da9bb431289da0d2d5719538ed886dda65e39c35`, padres `933eeb8d0` y `b0b076b51`. Único conflicto en impact.json: conservar pruebas D27/D31 y retirar cuatro suites eliminadas por #1254. 93 selectores y 4.687 tests PASS; cero fallas/errores, dos skips, 97,23% global JaCoCo. Stack exit 1, cleanup certificado de rio-playmaker-agentic-87924. Los cinco checks de CI 6015 SUCCESS; coverage PR 95,29%, helper 93,75% y global MeliCov 94,91%. GitHub MERGEABLE.

- Aclaración ejecutiva del cuerpo por pedido del usuario: foco Fury/ACME/lifecycle, alcance extra de ClickHouse y caso A→B, controller sólo Swagger y script de prueba local. Timeout de importación sin resolver. Sin cambios de código, tests, versión ni HEAD. Cuerpo publicado y verificado; reemplazado por la revisión final que incluye el comentario P2 y el merge más reciente.

- Review nuevo: comentario humano 4209736054 corregido en `0a5a01f76805c82a54d57481a61b9eb942e51640`; sólo resolver los tres campos de routing, conservando binding A y rechazo de B. Regresión roja: pause/resume 409 con Kafka detenido; verde: 274 tests, full 4.700 tests, contrato fresco 36 HTTP/H2 + seis handlers reales. Runner ajustado con `--rerun-tasks` para fixtures por run; JDK 25 requerido. Primeros intentos fallaron por JDK 21 y fixtures ausentes por up-to-date; ambos limpiaron su workspace.
- Replies nuevas publicadas y verificadas: [P2](https://github.com/melisource/fury_rio-playmaker/pull/1275#discussion_r4210096615) y [policy](https://github.com/melisource/fury_rio-playmaker/pull/1275#discussion_r4210097356). La política D27 se conserva, sin cambio de autorización adicional.
- Develop avanzó con #1270 durante el trabajo. Merge `526c1115cefd6e14079d1f825507063088915b24` integra `a4e2829ad92a9d181e1a728db25e5f7305abab80`; sólo impact.json tuvo conflicto, resuelto por unión de escenarios y conservación de 93 selectores. Los 21 archivos de código/config/script propios del PR son byte-identical a 0a5a01f76. El controller/DTO nuevo de freezes pertenece a develop y no aparece en el diff del PR. 93 selectores y 4.703 tests PASS; stack exit 1, cleanup de rio-playmaker-agentic-48924 certificado. Hooks pre/post-commit PASS; push, cuerpo y HEAD verificados; GitHub MERGEABLE. CI #6029: cinco checks SUCCESS; PR coverage 97,72%, helper 97,01% y overall MeliCov 94,92%. Evidencia: `/private/tmp/playmaker-pr1275-routing-merge-evidence.json` y logs `playmaker-pr1275-routing-*`.

- Code Reviewer terminó NEUTRAL y repitió D27 en comentario 4210366310; respondido con la política acordada y link al reply anterior: [4210381147](https://github.com/melisource/fury_rio-playmaker/pull/1275#discussion_r4210381147). No nuevo comentario humano ni cambio de código.

- Versión de prueba nueva por pedido del usuario: `0.0.2-acme-test3`, build #1811 FINISHED desde `526c1115cefd6e14079d1f825507063088915b24`, `type=test`, `run_test=true`. Sin cambios de source ni deploy. Evidencia sanitizada en `/private/tmp/playmaker-pr1275-test3-version-status.json`.
