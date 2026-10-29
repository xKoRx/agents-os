---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[SIG-659 — RIO Bus (implementación)]]"
  - "[[rio-playmaker]]"
  - "[[Descripción PR — rio-sdk-events — RIO Bus]]"
aliases: []
tags:
  - kind/doc
  - project/sig-659
created: "2026-10-28"
updated: "2026-10-28"
---

# Descripción PR — rio-playmaker — RIO Bus

**Identidad:** fury_rio-playmaker · `feature/rio-bus` @ `fab68a57f` (local, **sin push**) · base `origin/develop`, merge-base `20e0a9109` (18 commits atrás de `c7d894aad`, merge simulado sin conflictos) · 4 commits · 19 archivos, +645/−71 · spec [SIG-718](https://spellbook.adminml.com/projects/SIG/doc/SIG-718) · depende de [[Descripción PR — rio-sdk-events — RIO Bus]] (melisource/fury_rio-sdk-events#64) · suite 2026-10-28: 5.224 tests, 3 omitidos, 0 fallos.

> [!warning] Bloqueantes
> **Push bloqueado por el gate Cleric.** El pre-push falla con `BLOCKED: Missing ignored .grimoire/lore-readonly.local.json` (`gate:cleric-runner`). El perfil necesita el endpoint aprobado del MCP nativo de Lore y la variable de entorno de su token (`docs/grimoire-enforcement.md`); no están configurados en esta máquina. Sin push no hay PR.
> **Versión de prueba del SDK.** `rio-sdk-events:0.0.3-rio-bus` hasta que #64 se mergee y libere.
> **Base atrasada.** 18 commits detrás de `develop`; el merge simulado no tiene conflictos.

## Propósito

Cuerpo del PR de playmaker del RIO Bus como recurso de [[SIG-659 — RIO Bus (implementación)]], con la estructura del template `.github/pull_request_template.md` del repo (en inglés).

## Contenido

Cuerpo listo para pegar, seguido de notas internas que no van al PR.

---

## Description

**feat: subscribe playmaker to Discovery contracts through RIO Bus**

> [!IMPORTANT]
> **Merge blockers:** `build.gradle` uses the SDK test version `rio-sdk-events:0.0.3-rio-bus` from melisource/fury_rio-sdk-events#64, which is not merged or released; it must move to the released semver before merge.

Control planes will publish their Discovery V2 contracts to playmaker through the RIO Bus ([SIG-718](https://spellbook.adminml.com/projects/SIG/doc/SIG-718)): a single BigQueue topic, `rio-bus`, where every message carries `envelope_version`, `process`, `scope` and `body`. The SDK owns publishing and consuming. Playmaker only declares the processes it subscribes to and receives pushes on `POST /rio-bus`.

This PR subscribes playmaker to the `discovery` process. Received contracts are validated and logged, but not persisted: registry ingestion, ownership and versioning belong to SIG-671 and will replace the body of `run`. No existing topic, controller or flow changes. The V1 consumer on `/events/cp-components` is untouched.

Changes:

* `DiscoveryBusProcess`: subscribes to `discovery`. `parse` reads the contract with the SDK `DiscoveryMessageReader` and rejects anything that is not accepted, so an invalid contract is acknowledged and not retried. `run` logs `component_type`, `contract_version` and `producer.service_name`, never the body.
* `SecurityConfig`: `POST /rio-bus` is `permitAll`, like the other BigQueue push endpoints under `/events/**`; any other method on `/rio-bus` still requires a token.
* `rio.bus` block in every profile that declares `bigqueue.segment`: `topic: rio-bus`, `scope: ${SCOPE}`, and `segment-id` equal to that profile's `bigqueue.segment` (`nonprod` or `nonsite`).
* `rio-sdk-events` `1.5.0` → `0.0.3-rio-bus`. `1.5.0` is an ancestor of that version, so nothing from the current SDK is lost. The SDK's Jackson 3 does not replace playmaker's Jackson 2 HTTP converter; an integration test pins this.
* Backend E2E (Lore): the existing boot-health scenario now also sends a valid contract, an invalid contract and a foreign scope to `/rio-bus`, and checks the outcomes and that no body is logged.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — Verification in the test scope (real consumer and control plane) is pending.
* [ ] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) — Commit subjects are imperative, not conventional; the PR title is.
* [ ] My code follows the style guidelines of this project — `./gradlew check` was not run in this session.
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] I have performed a self-review of my own code
* [x] I have commented portions of my code, particularly in hard-to-understand areas
* [ ] I updated the applicable canonical documentation (`docs/architecture.md`, `testing.md`, `testing-scenarios.md`, Swagger, README, or CHANGELOG), or documented why it is unchanged. — Only the `SecurityConfig` javadoc lists `/rio-bus`; `docs/architecture.md` does not describe the bus yet.
* [x] After my changes were applied the app is still buildable
* [ ] My changes generate no new warnings (linters, code quality) — Not verified in this session.
* [x] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must
    * Integration testing is recommended
* [x] New and existing unit tests pass locally with my changes
* [ ] Any dependent changes have been merged and published in downstream modules — melisource/fury_rio-sdk-events#64 is open; only the test version `0.0.3-rio-bus` is published.
* [ ] I have updated my current branch with changes made in develop/master previously — 18 commits behind `develop`; a simulated merge has no conflicts.
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

On `feature/rio-bus` @ `fab68a57f`, JDK 21, local (`L0`):

* `./gradlew test` → 5,224 tests, 0 failures, 3 skipped (pre-existing).
* Focused: `bus.*`, `SecurityConfig*` and `CpCapability*` → 51 tests, 0 failures. `RioBusIntegrationTest` covers a valid contract (`PROCESSED`), an invalid one (`REJECTED`), a foreign scope (`SCOPE_MISMATCH`, `run` not called), the endpoint without a Tiger token, body-free logs and the unchanged Jackson 2 converter.
* Pre-push repository contracts: `repository-contract` PASS, `agentic-testing-contract` PASS.
* Not run in this session: `./gradlew check`.

## Testing contract

* [ ] Changed observable behavior is covered by added or updated Lore scenarios in `.lore/scenarios/`, verified by the Cleric/Lore push gate (`.testing/impact.json` is retired). — The scenario is updated; the push gate verification is pending.
* [x] Focused tests for the changed classes pass locally.
* [ ] Evidence distinguishes environment (`L0`, `L1`, `F1`) from layer (`UNIT`, `H2_INTEGRATION`, `CONTRACT`, `LOCAL_STACK`, `ECOSYSTEM_STACK`, `SMOKE`).
* [ ] Any mutable run published cleanup evidence; blocked L1/F1 capabilities are declared rather than replaced with L0 evidence.

## Issue

* Spec (functional and technical): [SIG-718](https://spellbook.adminml.com/projects/SIG/doc/SIG-718) · Epic: [SIG-659](https://spellbook.adminml.com/projects/SIG/specs/SIG-659)
* SDK: melisource/fury_rio-sdk-events#64

## Cleric and Lore E2E

* [ ] This agent-assisted change passed the direct Cleric E2E gate through the effective local pre-push hook.
* [x] Functional changes include added/updated committed `.lore/scenarios/` with behavior coverage.
* [ ] Cleric evaluated E2E selection, behavior coverage, and evidence for the exact source/scenario contents.
* [ ] Lore evidence identifies the run, final app commit/build/profile/target, scenario hashes,
      validation, complete execution, release gate, and cleanup; or the diff is outside functional paths.

_Record sanitized evidence links and exact identities. BLOCKED/FAIL is not passing evidence._

_The full Grimorio workflow is optional for this E2E gate. Existing security hooks and ordinary
code/security review requirements still apply independently._

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## Notas internas — NO van al PR

- El bloque `rio.bus` se repite en 9 yml; alcanza con declararlo en `application.yml` con `segment-id: ${bigqueue.segment}` (D-11 literal) y ajustar `RioBusProfileTest`.
- El escenario Lore de Discovery vive dentro de boot-health y el runner lo condiciona por id fijo (`playmaker-grimoire-enforcement-6swcza-boot-health`) con una regex atada al formato del log; debería ser un escenario propio.
- La evidencia Lore de Codex (`run_mvsm856f2ae9aada8f`) no se re-ejecutó en esta sesión; los checkboxes de Lore quedan sin marcar hasta que el pre-push pase.
