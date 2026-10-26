---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[RIO E2E local]]"
  - "[[RIO E2E local — Integración Flink Playmaker]]"
  - "[[rio-playmaker]]"
  - "[[Descripción PR — rio-controlplane-flink (E2E local Playmaker)]]"
  - "[[Descripción PR — ads-signals-frontend (RIO ecosistema local)]]"
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-23"
updated: "2026-10-23"
---

# Descripción PR — rio-playmaker (E2E local Flink)

Repo fury_rio-playmaker · [PR #1332](https://github.com/melisource/fury_rio-playmaker/pull/1332) (listo para review) · rama `feature/rio-e2e-local-flink` @ `a753673a3` · base `develop` @ `ca4fe6bef` (al día, sin conflictos) · 17 commits · 51 archivos/+3693/−248 · `src/main` y `src/test` sin diff · depende de CP Flink [#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218) · hermano front [#824](https://github.com/melisource/fury_ads-signals-frontend/pull/824) · `./gradlew test` 5184/0/3 skips heredados, `localTest` 55/0, contratos PASS · `rio-ecosystem all` desde workspace vacío: 12 corridas Lore, 28/28 escenarios, 48/48 oráculos · verificado 2026-10-23.

> [!warning] Bloqueantes antes del merge
> **PR dependiente sin mergear:** el journey Flink desde el front y `localFlinkIntegrationTest` necesitan el CP Flink de [#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218); mergear ese primero.

## Propósito

Recurso del proyecto con la descripción del PR de Playmaker: integración local con el CP Flink, el front y Lore, más el runner del ecosistema. Vive en el vault, no en el repo, según [[pr-description]].

## Contenido

Título del PR: `test(local): add RIO ecosystem E2E with Flink, frontend and Lore`.

Cuerpo publicado en GitHub entre los separadores, con el template `.github/pull_request_template.md` del repo, en inglés, precedido por la evidencia Lore y la tabla de la iniciativa.

---

## ✅ Lore end-to-end evidence

`rio-ecosystem setup` followed by `rio-ecosystem all` on 2026-10-23, from an empty workspace (`setup` cloned every application below) and an empty Docker context. Lore (Claude driving Chromium) ran the browser journeys through `ads-signals-frontend`; after each run, backend oracles checked the physical effect in Playmaker, Kafka, Flink and ClickHouse.

**Result: 12 Lore runs, 28 of 28 scenarios passed (0 failed, 0 blocked), 48 of 48 backend oracles passed; teardown left 0 containers and 0 networks.** Lore time 31 min, cost US$ 9.00.

| Case | Lore run | Scenarios | Backend oracles | What the oracles prove |
|---|---|---|---|---|
| `kafka-topic` | `run_mvl0hlo8bf000bfec5` | 2/2 | 3/3 | Deployment and peek COMPLETED; topic created with replication factor 2 |
| `kafka-topic-update` | `run_mvl0jpc35d5341495d` | 2/2 | 2/2 | Redeploy COMPLETED; partitions raised to 2 |
| `clickhouse-mergetree` | `run_mvkzhmpfaa209d6a55` | 2/2 | 2/2 | Deployment COMPLETED; MergeTree engine and sorting key |
| `clickhouse-run-query` | `run_mvkzohdg99119c6de6` | 2/2 | 3/3 | `execute-query` COMPLETED; the 3 rows were read |
| `clickhouse-mv` | `run_mvkzjykef7432d7255` | 3/3 | 6/6 | Three deployments, stop and start COMPLETED; MaterializedView engine |
| `clickhouse-refreshable-view` | `run_mvkzmxib6a508f5596` | 2/2 | 4/4 | Three deployments COMPLETED; `REFRESH EVERY` view |
| `kafka-clickhouse-connector` | `run_mvl0fudrdb10127e3c` | 2/2 | 5/5 | Three deployments COMPLETED; records produced to the topic reach the table |
| `flink-sql` | `run_mvl05m7jb7cb7d7272` | 3/3 | 5/5 | Deploy, stop and start COMPLETED; job RUNNING; a record is transformed by the job |
| `flink-sql-invalid` | `run_mvl0c3kc170b08c649` | 2/2 | 2/2 | Deployment FAILED and shown in the UI; no running job |
| `flink-jar` | `run_mvkzuwyhfd93e78394` | 3/3 | 4/4 | Deploy, stop and start COMPLETED; TopSpeedWindowing job RUNNING |
| `flink-python` | `run_mvl00gqn3193cc669e` | 3/3 | 4/4 | Deploy, stop and start COMPLETED; a record is transformed by the Python UDF |
| `cross-cp-pipeline` | `run_mvkzqdmec9c228ae8a` | 2/2 | 8/8 | Five components deployed at once; a record crosses Kafka → Flink → Kafka → ClickHouse |

Every run also includes the shared `smoke` scenario (authenticated data product list and pipeline editor). Checkouts: Playmaker `feature/rio-e2e-local-flink` @ `bc5e283fe`, Flink control plane `feature/rio-e2e-local-flink-playmaker` @ `da3e33c6`, Kafka control plane `develop` @ `f4b5701`, ClickHouse control plane `develop` @ `126633f0`, `ads-signals-frontend` `develop` @ `4e7b95cbe` (no code changes), Lore `develop` @ `e1c05ef`. The Lore run reports stay on the local Lore instance; to reproduce, run `.lore/ecosystem/rio-ecosystem setup` and then `.lore/ecosystem/rio-ecosystem all` from the Playmaker branch.

## 🧭 RIO local E2E initiative

Goal: run the RIO ecosystem locally with real engines (`ads-signals-frontend` → Playmaker → Kafka topics → Kafka, ClickHouse and Flink control planes), so any developer or agent can verify a feature from the UI down to its physical effect with one command and without production code changes.

| Step | Pull requests | Status |
|---|---|---|
| Kafka control plane local stack and Playmaker E2E | [rio-controlplane-kafka#85](https://github.com/melisource/fury_rio-controlplane-kafka/pull/85), [rio-controlplane-kafka#86](https://github.com/melisource/fury_rio-controlplane-kafka/pull/86), [rio-playmaker#1286](https://github.com/melisource/fury_rio-playmaker/pull/1286) | Merged |
| ClickHouse control plane and Playmaker E2E | [rio-controlplane-clickhouse#342](https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/342), [rio-playmaker#1288](https://github.com/melisource/fury_rio-playmaker/pull/1288) | Merged |
| Flink control plane local stack | [rio-controlplane-flink#209](https://github.com/melisource/fury_rio-controlplane-flink/pull/209), [rio-controlplane-flink#211](https://github.com/melisource/fury_rio-controlplane-flink/pull/211), [rio-controlplane-flink#213](https://github.com/melisource/fury_rio-controlplane-flink/pull/213) | Merged |
| **Flink ↔ Playmaker, frontend and Lore ecosystem cases (this round)** | Flink control plane: [rio-controlplane-flink#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218) · Playmaker: [rio-playmaker#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332) · Frontend docs: [ads-signals-frontend#824](https://github.com/melisource/fury_ads-signals-frontend/pull/824) | Open |

Merge order for this round: the Flink control plane PR first, then Playmaker; the frontend README PR can merge any time after Playmaker, since it links to Playmaker's runbook. Start reading at Playmaker's [`.lore/ecosystem/README.md`](https://github.com/melisource/fury_rio-playmaker/blob/feature/rio-e2e-local-flink/.lore/ecosystem/README.md). Related: [rio-playmaker#1327](https://github.com/melisource/fury_rio-playmaker/pull/1327) adds the Playmaker-owned Lore suite in `.lore/scenarios/`; the ecosystem cases live apart from it.


## Description

test(local): add RIO ecosystem E2E with Flink, frontend and Lore

Playmaker's local E2E stack already ran the Kafka and ClickHouse control planes. This PR adds the Flink control plane and proves the full path from Playmaker's APIs, and from `ads-signals-frontend`, to real Kafka topics, Flink jobs and ClickHouse tables and back to Playmaker's state. It also ships the runner that installs, updates and runs that ecosystem from zero, its cases and the agent skills to run and extend them. Production code is unchanged: `src/main` and `src/test` have no diff against `develop`.

Playmaker needed no new transport: `flink-sql` and `aws-flink-job` already dispatch through the local Kafka producer, actions already publish to `rio-action-trigger-local`, and the deployment, action and runtime-status listeners already consume the Flink results. The work is verification, local identity, tooling and documentation. The Flink control plane side is [rio-controlplane-flink#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218).

Changes:
* `PlaymakerFlinkE2ETest` (`@Tag("flink")`, task `localFlinkIntegrationTest`) enters only through Playmaker APIs and checks four layers per case: Playmaker state, keyed Kafka triggers and results, Flink JobManager job state and transformed records in `rio-flink-output-local`. It covers SQL provisioning, stop/start, redeploy as PROVISION, invalid SQL, a JAR job, a Python job and unsupported action types; undeploy is tagged `develop-gap` because Playmaker discards the DEPROVISION result with `terminal_component_run`. `localIntegrationTest` excludes the new tag.
* `KafkaE2EContext` gains a Flink mode (Flink readiness, the `rio-cp-flink-local` group and the Flink data topics) and a configurable deadline (`rio.e2e.deadline.seconds`, 240 s for Flink cold starts, 90 s by default). `FlinkJobManagerClient` is a read-only JobManager REST client for the assertions.
* `LocalAcmeGrantsFixtureServer` reads the token it expects from `RIO_LOCAL_TIGER_TOKEN` (default `Bearer local-e2e`, blank rejected), so the frontend can call Playmaker with the Tiger mock token whose user (`example`) is the identity the fixture grants.
* `.lore/ecosystem/rio-ecosystem` installs, updates and runs the ecosystem. `apps.json` lists the six applications with their Git repository, expected branch and local guide. `setup` creates the `rio` Colima profile, clones what is missing into `~/.rio-ecosystem/repos`, installs dependencies, writes `~/.config/rio-ecosystem/env` and runs `doctor`; `update` fast-forwards clean managed clones and reinstalls dependencies whose lockfile changed; `doctor` validates tools, the Docker context, every checkout and its branch. `up`, `seed`, `run`, `verify`, `down` and `all` start the stack, the frontend (no code changes: recorded Kraken mocks and the Tiger mock token through environment variables) and Lore, seed each case through Playmaker, run one Lore run per case, verify backend oracles and always tear down. `lore` opens the Lore web alone to browse stored runs after the stack is down.
* `.lore/ecosystem/cases/` holds 13 cases, each a folder with Lore scenarios and a `case.json` (seed, pipeline relations and oracles); `new <case>` scaffolds one from `templates/case`. The cases sit outside `.lore/scenarios/`, the Playmaker-owned suite enforced by the Cleric pre-push gate in [#1327](https://github.com/melisource/fury_rio-playmaker/pull/1327), because they need the frontend and the three control planes.
* Agent skills `rio-ecosystem-e2e` (install, update, run, read failures) and `rio-ecosystem-scenario-authoring` (write cases, Lore limits, done checklist, adding a technology or control plane) live in `.lore/ecosystem/skills/`; `AGENTS.md` points to them because `.agents/skills` and `.claude/` are generated and ignored by Git.
* Documentation: `.lore/ecosystem/README.md` is the installation and update runbook (applications, machine requirements, commands, configuration, troubleshooting); `local/RIO_E2E.md` documents the three-control-plane stack and links to it.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — depends on [rio-controlplane-flink#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218) merging first.
* [ ] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) — five of the 17 commits use a conventional prefix (`test(local):`, `chore(local):`); the others use plain imperative subjects, including the `merge develop` synchronization.
* [x] My code follows the style guidelines of this project
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code
* [x] I have commented portions of my code, particularly in hard-to-understand areas
* [x] I updated the applicable canonical documentation (`docs/architecture.md`, `testing.md`, `testing-scenarios.md`, Swagger, README, or CHANGELOG), or documented why it is unchanged. — `local/RIO_E2E.md` and `.lore/ecosystem/README.md`; architecture, testing docs and CHANGELOG are unchanged because production behavior is unchanged.
* [x] After my changes were applied the app is still buildable
* [x] My changes generate no new warnings (linters, code quality)
* [x] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must
    * Integration testing is recommended
* [x] New and existing unit tests pass locally with my changes
* [ ] Any dependent changes have been merged and published in downstream modules — [rio-controlplane-flink#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218) (Flink control plane) is not merged yet.
* [x] I have updated my current branch with changes made in develop/master previously
* [ ] I already deployed this branch in the pre-production environment — not applicable: local-only change.

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

Java 25, VM `colima-rio`, branch merged with `develop` @ `ca4fe6bef` (no new `develop` commits since). Environments: `L0` (unit and local tests) and the local ecosystem stack (Playmaker on the host; Kafka, ClickHouse and Flink control planes, MySQL, ClickHouse and Flink in Docker). Java sources are unchanged after `bbe14b2c8`; later commits only touch `.lore/ecosystem/`.

* Browser (`ECOSYSTEM_STACK`) — see "Lore end-to-end evidence" above: 13 cases, 28 of 28 Lore scenarios and 48 of 48 backend oracles from an empty workspace at `bc5e283fe`.
* `./scripts/validate-repository-contract.sh` — PASS (7 sources, 12 commands, 8 documents); `./scripts/run-agentic-testing-contract.sh --plan` at `bc5e283fe` — no observable-behavior surface changed.
* `./scripts/run-agentic-testing-contract.sh` at `bbe14b2c8` — PASS: the 60 declared focused test classes and the inherited `L0-LOCAL_STACK` checks `AT-000-S01` (local stack health) and `AT-180-S18` (local deployment loopback), with their own cleanup.
* `./gradlew test` — 5184 tests, 0 failures, 3 skipped (two `@Disabled` and one MySQL-only case, all from `develop`).
* `./gradlew localTest verifyLocalArtifactIsolation compileLocalIntegrationTestJava` — 55 local tests, 0 failures; isolation PASS.
* `./gradlew localFlinkIntegrationTest` (`LOCAL_STACK`) — SQL provisioning and stop/start passed three times, twice on a live stack and once on a recreated one; redeploy, invalid SQL, JAR, Python and unsupported actions passed once each.
* Kafka and ClickHouse regressions (`localIntegrationTest`, `localClickHouseIntegrationTest`) — 7 and 5 tests passed with the Flink control plane running and no Flink jobs triggered.
* Undeploy (`develop-gap`) — ran once: the Flink control plane completed DEPROVISION and canceled the jobs, and Playmaker kept the deployment `requested` with `terminal_component_run`. This is existing `develop` behavior and is not changed here.
* Review fixes (`b2d7dded6`) — `KafkaAbsenceOracleTest` 5/0; full agentic testing contract PASS; runner ownership guards checked with a foreign `rio-*` container (`down` without state, with stale state and `all` all abort without removing it); `kafka-clickhouse-connector` Lore run and its 5 oracles PASS with the new runner, teardown 0 resources; `localFlinkIntegrationTest` with the new Kafka polling: Python, JAR, stop/start and redeploy passed.
* Docker context lock (`f9862eff0`) — one stack per context: a held lock, a lock being created and a stale lock with a foreign stack container all stop the second run without touching the other run's resources; `all kafka-topic` held the lock during the run, passed Lore and its 3 oracles (with `--` data product names and seed-scoped oracles), left 0 stack resources and released the lock.
* Cleanup — every stack run ended with 0 containers, 0 `rio-*` networks and free ports.

## Testing contract

* [x] I added or updated `.testing/impact.json`, or this PR qualifies for the migration-only exception in `testing.md`, or does not change an observable-behavior surface.
* [x] The impacted/new AT scenarios and focused tests are declared in the manifest, when required.
* [ ] If a manifest is required and behavior is unchanged, it includes the reviewed scenarios and a concrete justification. — not applicable: the manifest declares a local fixture change with its focused test.
* [x] Evidence distinguishes environment (`L0`, `L1`, `F1`) from layer (`UNIT`, `H2_INTEGRATION`, `CONTRACT`, `LOCAL_STACK`, `ECOSYSTEM_STACK`, `SMOKE`).
* [x] Any mutable run published cleanup evidence; blocked L1/F1 capabilities are declared rather than replaced with L0 evidence.

## Issue

RIO local E2E initiative (see the table above). Sibling PRs: [rio-controlplane-flink#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218) (Flink control plane) and [ads-signals-frontend#824](https://github.com/melisource/fury_ads-signals-frontend/pull/824) (frontend README). Operational instructions are in `.lore/ecosystem/README.md` and `local/RIO_E2E.md`.

---

## Notas internas — NO van al PR

- **Relación con #1324/#1327 (Ale):** la policy de Grimorio de #1327 marca `src/local/` y `local/` como `functional_paths` con E2E Lore requerido y `.lore/scenarios` como `scenario_directory`. Cuando esos PRs entren, un push que toque esas rutas pedirá el gate Cleric sobre la suite de Playmaker; los escenarios de ecosistema quedan fuera de ese inventario por diseño.
- **Orden de commit:** `d287dd2cb` se pusheó antes de correr el contrato staged, que pedía actualizar `.testing/impact.json`; quedó corregido en `bbe14b2c8` con el contrato completo en PASS.
- **Manifiesto tras la sincronización:** `testing.md` exige actualizar `.testing/impact.json` cuando cambia el stack local. El conflicto con `develop` se resolvió como en sincronizaciones previas del repo: unión de escenarios, tests y `executionChecks` de ambos lados, `notes` combinadas y el `changeSummary` de este PR. Eso hereda los dos checks `L0-LOCAL_STACK` de `develop`, que pasaron con `DOCKER_CONTEXT=colima-rio`.
- **Reservas del code review:** `@SuppressWarnings("PMD.GodClass")` agregado a `LocalAcmeGrantsFixtureServer` y reformateo completo de `KafkaE2EContext`/fixture impuesto por los hooks sobre el archivo entero; `PlaymakerFlinkE2ETest` sigue grande (1109 líneas, la de ClickHouse tiene 215).
- **Fuera de alcance, sin fix:** undeploy `develop-gap`; el CP Flink registra envelopes crudos con credenciales sintéticas; urllib normaliza headers y un GET de action devolvió 502 en un parseo (observación de Sol en F2).
- **Lore:** el agente no puede arrastrar al canvas, por eso los componentes de los escenarios se siembran por API; la creación por arrastre se validó con Playwright en F4. El binario nativo del Claude Agent SDK se instaló con `--no-save` en el checkout de Lore.
- **Plan:** el detalle de fases, gates y decisiones vive en [[RIO E2E local — Integración Flink Playmaker]]; G4/G5 en `review` esperando al owner.
- **Orden del cuerpo:** las secciones «Lore end-to-end evidence» y «RIO local E2E initiative» van antes del template por pedido del owner (pruebas arriba, iniciativa y PRs hermanos navegables); son idénticas en los tres PRs.
- **Borrador:** `gh pr create` dejó los tres PRs como draft; el owner pidió marcarlos listos para review el 2026-10-23.
