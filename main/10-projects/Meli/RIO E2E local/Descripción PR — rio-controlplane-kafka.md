---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related: ["[[RIO E2E local]]", "[[rio-controlplane-kafka]]", "[[Descripción PR — rio-playmaker]]"]
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-09"
updated: "2026-10-14"
---

# Descripción PR — rio-controlplane-kafka

**Identity:** fury_rio-controlplane-kafka · feature/rio-e2e-local-kafka @ aae17bc4b7d57d76c120461eafbf51440d5b3420 · base origin/develop @ 6a91937c0664d83f907dec222af8a96b4042c6ae · 11 commits · 19 files changed, 1662 insertions(+), 138 deletions(-) · validation 2026-10-14.

> [!warning] Physical validation pending
> The shared VM startup command fails while another session owns `rio-local`; this pass claims local checks and documentation publication only.

## Propósito

Keep the PR #86 body as a resource of [[RIO E2E local]].

## Contenido

This repository has no PR template under `.github`; the body uses the minimal pr-description sections.

---

## What changes

Adds embedded Kafka intake and raw SDK result transport under `compose,local,local-kafka`, using the existing controllers, processors and publishers. Compose owns the single broker and `rio-local`; it creates the six intake/result/DLT topics plus the two standalone result topics. The HTTP standalone suite uses `compose,local` and its environment-1 fixture.

`local/README.md` separates the standalone commands and physical coverage from the Playmaker integration, links to its canonical hub, explains ports/topics/profiles, and checks network ownership before startup. The Spanish feature specs describe the current Spring Kafka implementation and correlation boundary.

Spring Kafka commits after controller acceptance or acknowledged DLT publication. Poison skips retries; transient failures retry twice at one-second intervals. Readiness requires both trigger streams assigned, but a failed DLT can block a partition while readiness stays green. Asynchronous business completion and absorbed publisher failures remain unchanged. Local dependencies/resources are excluded from the production jar; production sources remain unchanged.

## Why

Make the local test path and its boundaries understandable without reading source code, while preserving the integration model in the Playmaker hub.

## How this was tested

- Java 25, literal `./gradlew --offline localBootJar localTest verifyLocalArtifactIsolation`: PASS; 62 local tests, zero failures/errors/skips; production artifact isolation PASS.
- Literal Compose startup failed with a broker container-name conflict when another session occupied the VM during the build. The documentation adds a network preflight; its repeated block stops with `rio-local is occupied; wait for its owner to finish` before Compose. No owned container remains.
- `localFunctionalTest` and standalone teardown remain pending until the shared VM is free. Playmaker integration follows the hub in companion [#1286](https://github.com/melisource/fury_rio-playmaker/pull/1286).
- `git diff --check` and required pre-commit checks on changed Markdown: PASS. This documentation pass changes only Markdown.

## Issue / specification

RIO E2E local. Operational instructions: `local/README.md`; integration source: `fury_rio-playmaker/local/RIO_E2E.md`.

---

## Notas internas — NO van al PR

- Documentation-only delta; runtime sources, build files, Compose, scripts and Dockerfiles are unchanged.
