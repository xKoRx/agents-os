---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[CP Flink local]]"
  - "[[RIO E2E local]]"
  - "[[rio-controlplane-flink]]"
  - "[[Descripción PR — rio-controlplane-flink (E2E local)]]"
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-13"
updated: "2026-10-14"
---

# Descripción PR — rio-controlplane-flink (E2E local PR 2)

Repo fury_rio-controlplane-flink · rama feature/rio-e2e-local-flink-pr2 @ 0728044cbe0c97c7a785bc023601860825ec1c7a · base feature/rio-e2e-local-flink-kiss @ c0cabe7213461793bf1382c4e2816dea258361fd (#209) · 13 commits sobre la base · diff base...HEAD: 15 archivos/+1160/−149; diff origin/develop...HEAD: 29 archivos/+3285/−0, medidos tras git fetch origin · src/main y src/test sin diff contra ambas referencias · 1937 tests productivos/20 locales/pre-commit PASS · E2E físico completo PASS en 0728044c, una corrida y cleanup 0 contenedores/0 redes rio-* · 0 hilos pendientes y CI verde (Code Reviewer NEUTRAL) · verificado 2026-10-14.

## Propósito

Recurso del proyecto con la descripción final del PR 2. Se verificó que el repo no tiene template de pull request; se usan las secciones mínimas de pr-description, con Scope y Project según el alcance solicitado. El cuerpo está en inglés conforme a CLAUDE.md.

## Contenido

Título del PR: `feat(local): SQL UPDATE, SQL CRUD and JAVA/JAR (PR 2 of 3)`.

Cuerpo listo para GitHub entre los separadores; la nota conserva la identidad y evidencia fuera del cuerpo publicado.

---

## What changes

- SQL UPDATE replaces the running SQL jobs with jobs using the new transformation.
- HTTP SQL CRUD through `/flink/sql-code` creates, reads, lists and deletes SQL used by deployments.
- JAVA/JAR uses the production Nexus and multipart handlers, with the nginx `nexus-local` stub serving `TopSpeedWindowing.jar` from the Flink image.
- Shared process-local storage serves SQL CRUD, deployment attachments and multipart uploads. It retains SQL and artifacts after UPDATE and DEPROVISION, matching S3 retention so `CheckArtifactHandler` can reuse a cached artifact.
- `LocalNexusUrlValidator` permits HTTP only for the local stub while preserving production repository and path validation.

## Why

Provide a transparent local E2E environment for the Flink control plane using its existing controllers, handlers and pollers, with no production code changes. This is PR 2 of 3, stacked on [#209](https://github.com/melisource/fury_rio-controlplane-flink/pull/209).

## How it was tested

- `./gradlew test`: PASS, 1937 production tests, with no failures, errors or skips.
- `./gradlew localBootJar localTest`: PASS, 20 local tests, with no failures, errors or skips.
- Pre-commit: PASS, including formatting, Checkstyle and PMD.
- After `git fetch origin`, `src/main` and `src/test` have an empty diff against both `origin/develop` and `origin/feature/rio-e2e-local-flink-kiss`.
- Complete physical E2E: PASS on `0728044c` in one run. Scenarios cover SQL with two INSERT statements and comments; invalid SQL with rollback; stop with FAILED+RUNNING jobs; SQL UPDATE with a new transformation; HTTP SQL CRUD with real data and SQL retained after DEPROVISION; JAR PROVISION, stop/start, UPDATE with a new job and file sink, and DEPROVISION; and JAR re-provision with a cache hit and no new artifact download from Nexus.
- Cleanup verified: 0 containers and 0 `rio-*` networks in `colima-rio`.

## Scope

Python/ZIP belongs to PR 3. GCP and Playmaker are outside this PR.

## Project

RIO E2E local / CP Flink local · repository `fury_rio-controlplane-flink` · branch `feature/rio-e2e-local-flink-pr2` @ `0728044c` · base `feature/rio-e2e-local-flink-kiss` @ `c0cabe72` ([#209](https://github.com/melisource/fury_rio-controlplane-flink/pull/209)).

---

## Notas internas — NO van al PR

- Evidencia: reportes XML existentes de test (1937) y localTest (20), sin fallas, errores ni skips; log físico temporal `rio-pr211-e2e-final.log`, con PASS completo y SHA final 0728044c. Tests y E2E corresponden a la certificación del mismo SHA realizada en esta conversación; esta actualización documental no los repite.
- Pre-commit PASS corresponde a la certificación aportada para el mismo SHA. El fetch, los diffs, el estado del PR y los hilos se verificaron nuevamente para esta actualización.
- Fuentes funcionales: local/README.md, LocalFlinkStorage y LocalNexusUrlValidator. No se detectaron afirmaciones sin respaldo ni bloqueantes nuevos.
