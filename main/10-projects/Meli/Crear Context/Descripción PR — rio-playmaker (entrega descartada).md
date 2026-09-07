---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
  - "[[Guía de implementación — Component Context]]"
aliases:
  - PR rio-playmaker component context
  - descripción PR playmaker SIG-573
tags:
  - kind/doc
  - project/crear-context
created: "2026-08-19"
updated: "2026-08-19"
---

# Descripción PR — rio-playmaker

**Repo:** `rio-playmaker` · **Branch:** `feature/component-context` · **Base:** `develop` @ `dac615f47` · **Commits:** 1 (`e6fadaf0b`) · **Diff:** 12 archivos, +683/-14 · **Spec:** [SIG-573](https://spellbook.adminml.com/projects/SIG/specs/SIG-573) · **Depende de:** `rio-sdk-events` branch `feature/SIG-573-component-context` (ver [[Descripción PR — rio-sdk-events]])

> [!warning] Bloqueante abierto
> El `build.gradle` de esta branch apunta a `mavenLocal()` y a `rio-sdk-events:0.0.1-component-context`, que no resuelve en CI. **No mergeable** hasta que el SDK se publique con versión semver real y este PR la referencie.

## Propósito

Descripción del Pull Request de `rio-playmaker` para SIG-573, lista para copiar y pegar en GitHub. Vive en el vault como recurso del proyecto, no como archivo en la raíz del repo: así no se cuela en el diff que describe, no se pierde al cambiar de branch y queda enlazada al proyecto y a las specs.

## Contenido

Identidad de la entrega (branch, base, commits, diff) · bloqueante de merge · las cinco secciones del template `.github/pull_request_template.md` de este repo, en su idioma original · notas internas que **no** van al PR.

---

## Description

feat(pipeline): create and dispatch the ephemeral component context (SIG-573)

A control plane receives identifiers, component type, criticality and a `params` map of values Playmaker already resolved. It receives `"broker:9092"` with no way to know it came from a neighbouring Kafka topic: it does not know which components surround it, what each one publishes, or which version its own last deployment ended on. The deployment message carries values, not context — and the information that explains them already lives in Playmaker, in the active relations and in the outputs the control planes themselves published.

This PR creates a `Context` entity, calculated per request and carried on each component's own trigger message. Derivation is topological: every active relation is reported in both directions, whether or not the component under deployment consumes any of its outputs, and a peer that has published nothing yet keeps its slot with empty outputs. Outputs travel already resolved — the same unwrapping the parameter resolver applies — so a control plane never has to open a storage envelope.

Nothing is persisted, `parameters` and properties are untouched, and no control plane is required to change: the message field is nullable and additive. This is a self-contained slice; adoption by the control planes is a separate initiative.

Changes:
* `ComponentContextBuilder` — new service that derives the context: classifies active relations into sources and destinations, resolves imported copies against their original component (failing closed when the import is not authorized), reads persisted control-plane outputs in a single batched query, and unwraps `{type,value,sensitive}` to the effective value. Any internal failure yields `null` and the dispatch proceeds without context.
* `DeploymentRepository.findLastCompletedSemver` — new JPQL query returning the semver of the newest completed deployment for a service slot, bounded by `Pageable`. Needed because the slot's own component definition is desired state and already points at the version being deployed.
* `DispatchRequest` — new nullable `context` component on the internal pipeline carrier.
* `BatchDispatchServiceImpl` — creation point: derives `lastVersion` and the context per dispatch item, after parameter resolution and after the previous topological batch committed, which is what makes peer outputs readable.
* `BigQueueDispatchAdapter` — passes `request.context()` into the trigger message. The materializer and legacy paths are untouched and keep publishing without context.
* `build.gradle` — SDK bumped to the branch version (**temporary, see blocker above**).
* Tests — new `ComponentContextBuilderTest` (12 tests) and two new cases in `BigQueueDispatchAdapterTest`; existing dispatch tests updated for the new record component.

## Dev checklist (should be completed by the developer assigned to the issue)

* [x] I have met the definition of done
* [ ] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) — **pending**: the single commit is titled `component context`; it must be rewritten as a conventional, imperative, capitalized subject before merge
* [x] My code follows the style guidelines of this project
* [x] I have performed a self-review of my own code
* [x] I have commented portions of my code, particularly in hard-to-understand areas — comments are limited to decisions that depart from convention: why `lastVersion` comes from history and not from the slot, why only the exception type is logged, why the import check fails closed
* [x] After my changes were applied the app is still buildable
* [x] My changes generate no new warnings (linters, code quality)
* [x] I have added tests that prove my fix is effective or that my feature works
    * Unit testing is a must — 12 new builder tests + 2 adapter tests
    * Integration testing is recommended — **not added**: the creation point in `BatchDispatchServiceImpl` and the new query have no coverage yet
* [x] New and existing unit tests pass locally with my changes — full suite: **3141 passed, 0 failed**
* [ ] Any dependent changes have been merged and published in downstream modules — **blocked**: `rio-sdk-events` must be published first
* [x] I have updated my current branch with changes made in develop/master previously — branch is 1 commit on top of `dac615f47`
* [ ] I already deployed this branch in the pre-production environment — **pending**, blocked by the SDK version
* [ ] I have made corresponding changes to the documentation — **partial**: the technical spec still describes the earlier rich envelope and needs to be realigned or marked superseded

## How Has This Been Tested?

* `./gradlew test` — full suite green: **3141 passed, 0 failed**
* `ComponentContextBuilderTest` — 12 unit tests covering both directions of the topology, wrapper unwrapping, undeployed peers keeping their slot, authorized and unauthorized imports (the unauthorized cases plant a recoverable `leaked:9092` value in the copy's own service row and assert it does not surface), unreadable JSON, peer deduplication and self relations
* `BigQueueDispatchAdapterTest` — captures the published `DeploymentTriggerMessage` and asserts the context travels when present, that `params` is unchanged, and that the message stays backward compatible (`context == null`) when no context was derived
* Not yet tested: deployment to a pre-production scope, blocked by the SDK version

## Issue

* Spec: [SIG-573](https://spellbook.adminml.com/projects/SIG/specs/SIG-573)

---

## Notas internas (no van al PR)

- Findings abiertos del code review que conviene resolver antes de pedir review a flor: `findLastCompletedSemver` hace match por sufijo `%completed` y por lo tanto también captura `undeploy_completed`; los `Objects.requireNonNull` del builder quedaron fuera del `try` y rompen la garantía "never throws"; `lastCompletedSemver` se invoca fuera del `try/catch` del dispatch; outputs anidados sin clave `value` se descartan en silencio; `origin()` hace un `findById` por vecino importado, contra el batch del resto.
- Trazabilidad: [[Crear Context]] · [[Guía de implementación — Component Context]] · [[Descripción PR — rio-sdk-events]]
