---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related: ["[[RIO E2E local]]", "[[rio-playmaker]]", "[[Descripción PR — rio-controlplane-kafka]]"]
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-09"
updated: "2026-10-09"
---

# Descripción PR — rio-playmaker

**PR:** [Playmaker #1286](https://github.com/melisource/fury_rio-playmaker/pull/1286) ·CI6144, cobertura, dependencias, static-analyzer y workflow SUCCESS sobrec3ecf8c; Code Reviewer en curso y CodeQL startup_failure.

**Identidad:** melisource/fury_rio-playmaker ·feature/rio-e2e-local-kafka@c3ecf8cb78bf5f4a8df093e1a1a40488d6d91a7f ·base develop@1ba12db957576db04eca686c16e6afac7564edd1 ·11 commits ·66 files changed, 6079 insertions(+), 409 deletions(-) ·source642aa53 ·CP companion #86.

## Propósito

Descripción reviewable con las skills canónicas human-first-technical-writing y pr-description; template English del repo conservado y evidencia vigente separada de historia.

## Contenido

Cuerpo para GitHub; reviewer checklist sin completar y límites declarados.

---

## Description

feat: run Playmaker and Kafka CP E2E through embedded local Kafka

The local Kafka profile now sends deployment and action triggers to the real CP and consumes its SDK results through Playmaker's existing business handlers. This replaces the local BigQueue transport and enables physical lifecycle, PEEK, replay, poison/DLT and restart checks from Playmaker APIs. There is one CP-owned broker and no Kafka→HTTP bridge. [Companion CP Kafka PR #86](https://github.com/melisource/fury_rio-controlplane-kafka/pull/86) is required for the ecosystem run; ClickHouse, Flink and browser journeys remain later phases.

- Share the acknowledged raw-byte result transport across deployment/actions; use the real guards, idempotency and result state transitions.
- Add isolated local actions/KVS/grants boundaries and an owned `start|test|test-gap|stop` launcher. The normal suite accepts productive timeouts; the destructive publication gap has a separate task.
- Split the physical harness into independent method fixtures with physical engine, wire, offset and PM-state oracles. The runner supplies ecosystem topics and preserves process/resource ownership during bootstrap, restart and teardown.
- Include the separate DEPROVISION fix (b603098): new operation correlation, correct legacy dispatch and preservation of prior completed ComponentRuns. Regression evidence is in `deprovision-evidence.md`.

Productive adapters receive only the required profile exclusions; inherited local deployment transport is shared without weakening decoding/DLT semantics. New `src/local` classes/resources remain outside the productive jar. The branch includes current develop@1ba12db957576db04eca686c16e6afac7564edd1; upstream action/history authorization is preserved byte-for-byte, with fresh integrated artifacts and gates.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done
* [x] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [ ] My code follows the style guidelines of this project
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code
* [x] I have commented portions of my code, particularly in hard-to-understand areas
* [x] I updated the applicable canonical documentation (`docs/architecture.md`, `testing.md`, `testing-scenarios.md`, Swagger, README, or CHANGELOG), or documented why it is unchanged.
* [x] After my changes were applied the app is still buildable
* [ ] My changes generate no new warnings (linters, code quality)
* [x] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must
    * Integration testing is recommended
* [x] New and existing unit tests pass locally with my changes
* [ ] Any dependent changes have been merged and published in downstream modules
* [x] I have updated my current branch with changes made in develop/master previously
* [ ] I already deployed this branch in the pre-production environment


Unchecked items are deliberate: local integrated acceptance is complete; CodeQL startup failure is still unresolved; companion CP changes are a runtime pairing and are not merged; pre-production deployment is outside this local-only scope. Style/warning certification is reported by remote checks rather than inferred from the local build. The reviewer owns the checklist below.

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

Source HEAD `642aa53ab929fa89394a4421051a7567b0585651`; PR HEAD `c3ecf8cb78bf5f4a8df093e1a1a40488d6d91a7f` adds Markdown only. JDK25; explicit Docker context `colima-rio-kafka-e2e-01a0f8e0`; real CP Kafka + broker + MySQL and host Playmaker.

- `./scripts/validate-repository-contract.sh --staged` and `git diff --cached --check`: PASS on exact intended index.
- `RIO_CP_ROOT=<CP checkout> ./scripts/run-agentic-testing-contract.sh` with explicit JAVA_HOME/RIO_JAVA_HOME/DOCKER_CONTEXT: complete outer exit0,22 unique focused selectors, all3 L0 capabilities and required L1 ecosystem. All7 upstream changed test classes plus transitive auth tests are retained. An initial incorrect selector package was corrected and the full contract restarted; no selector was omitted.
- `./gradlew --no-daemon test localTest localJacocoCoverageVerification criticalKafkaJacocoReport criticalKafkaCoverageVerification verifyLocalArtifactIsolation`:4818 regression tests,0 failures/errors,2 inherited TopologicalSort skips;23 local tests with0 failures/errors/skips. Critical lines235/241(97.5104%), branches94/98(95.9184%); coverage/isolation PASS. Tasks already completed by L1's coverage dependencies were reused by the final invocation; counts come from completed XML, not that invocation's duration.
- `python3 -m unittest discover -s local/tests`:24/24 PASS, including bootstrap partial-write/termination and ownership/interruption boundaries.
- Physical integrated run44941be9e81d: `local/rio-e2e.sh test`2×11/11, actual CP restart and retained offsets; `test-gap`2×1/1.0 failures/errors/skips. Local jar hashes PM071123de89ecba5e594b978c72d2b059fb372afc80998fb5bcbe78d91fca2808 / CP7fe507f62b4487d4306d0e22784a6eb49b0c2236e3bc7088a9a03f6718fa5e90.

Independent final review: QUALIFIED PASS on source642aa53/CP907, clean clones with spaces and unrelated cwd; both local jars and PM product match root. Normal productive-budget run810238a329de2×11/11, fresh15s gap9444d48eba3d2×1/1,0 failures/errors/skips. Actual restarts/offsets, physical effects and PM state verified; independent cleanup preserves all24 image IDs and3 baseline networks, with ports free after bounded54s settlement. Root snapshot405 hashes/class IDs and critical coverage were independently verified. No source blockers. Previous PM90df clean-clone acceptance is historical, not evidence for the new jar.

Cleanup certified for this run: no own state/processes/containers/volumes; baseline networks/images preserved. Host ports can require bounded forwarding/TCP settlement. The original `colima-rio` VM remains offline after an earlier ENOSPC/I/O incident; its interrupted run's cleanup is uncertified and private recovery state is preserved. No VM repair is claimed. Corporate transport/auth/cloud, CH/Flink/browser and pre-production are not certified. The real swallowed-publication gap and unmapped GCP PEEK failure remain visible.

[Current verification](https://github.com/melisource/fury_rio-playmaker/blob/c3ecf8cb78bf5f4a8df093e1a1a40488d6d91a7f/meli/features/20261009-rio-e2e-local/4-implementation/VERIFICATION.md) includes exact gates, hashes and historical limits; operational commands are in `local/RIO_E2E.md`. CI principal6144, coverage, dependencies, static-analyzer and workflow passed on current HEADc3ecf8c. Code Reviewer is still in progress at this snapshot. **[Code Scanning run37975496615](https://github.com/melisource/fury_rio-playmaker/actions/runs/37975496615) failed at startup without jobs/checkruns; retry is unavailable.** Other PM branches show the same symptom, but cause remains unproven. A one-line corporate-runner proposal for file-limit was rejected by automatic permission review as an environment/security boundary change and awaits explicit owner authorization. No runner, script, threshold, permissions or gate was changed/bypassed. Overall CodeQL green is not claimed. The final [independent integration review](https://github.com/melisource/fury_rio-playmaker/blob/c3ecf8cb78bf5f4a8df093e1a1a40488d6d91a7f/meli/features/20261009-rio-e2e-local/4-implementation/PR_INTEGRATION_REVIEW.md) records local acceptance separately.

## Testing contract

* [x] I added or updated `.testing/impact.json`, or this PR does not change an observable-behavior surface.
* [x] The impacted/new AT scenarios and focused tests are declared in the manifest.
* [ ] If behavior is unchanged, the manifest includes the reviewed scenarios and a concrete justification. (Not applicable: `behaviorChange=true`.)
* [x] Evidence distinguishes environment (`L0`, `L1`, `F1`) from layer (`UNIT`, `H2_INTEGRATION`, `CONTRACT`, `LOCAL_STACK`, `ECOSYSTEM_STACK`, `SMOKE`).
* [x] Any mutable run published cleanup evidence; blocked L1/F1 capabilities are declared rather than replaced with L0 evidence.

## Issue

AGENTS OS project RIO E2E local, F1. No Jira issue was supplied. Repository functional/technical specs: `meli/features/20261009-rio-e2e-local/1-functional/spec.md` and `2-technical/spec.md`; tasks and evidence sit beside them.


---

## Notas internas — NO van al PR

- Pedido explícito autoriza crear/pushear ambos PR, superando el alcance sólo autoría default de pr-description. No merge/deploy.
- Merge actual preserva auth upstream sin bypass; gates/jars/receipts actuales e independiente integrado PASS calificado. Fuente642aa53; tres archivos Markdown de evidencia posteriores.
- PR publicado y adjunto al chat; checks remotos en curso. No confundir gate local con CI.
