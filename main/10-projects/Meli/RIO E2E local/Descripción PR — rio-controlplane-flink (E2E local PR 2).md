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
updated: "2026-10-20"
---

# Descripción PR — rio-controlplane-flink (E2E local PR 2)

Repo fury_rio-controlplane-flink · rama `feature/rio-e2e-local-flink-pr2` @ `91cdd5f8` · base `develop` @ `0b60e64b` (squash de #209) · diff develop...HEAD: 15 archivos/+1229/−157 · src/main y src/test sin diff contra develop · 1937 productivos/28 locales, cobertura productiva 96,06% líneas/91,59% ramas, pre-commit PASS · E2E físico completo PASS desde VM vacía, cleanup 0/0 · CI verde, 0 hilos abiertos · verificado 2026-10-20.

## Propósito

Recurso del proyecto con la descripción del PR, alineada con la serie #209 → #211 → #213 para que las tres cuenten una sola historia. El repo no tiene template de pull request; se reutilizan las secciones de #209 (What changes / Why / How this was tested / Issue / specification) precedidas por una tabla de serie idéntica en #211 y #213. El cuerpo está en inglés conforme a CLAUDE.md y se redactó con [[human-first-technical-writing]].

## Contenido

Título del PR: `feat(local): SQL UPDATE, SQL CRUD and JAVA/JAR (PR 2 of 3)`.

Cuerpo listo para GitHub entre los separadores.

---

## Series: standalone local Flink E2E

The Flink control plane runs locally against a real Kafka broker, SQL Gateway, JobManager and TaskManager, through its existing controllers, handlers and pollers. Local adapters replace the AWS KDA and S3 operations; production code stays unchanged except for the optional stop query added in #209. The work lands in three PRs, one deployable language at a time:

| PR | Adds | Status |
|---|---|---|
| [#209](https://github.com/melisource/fury_rio-controlplane-flink/pull/209) | SQL lifecycle: PROVISION, DEPROVISION, stop/start and runtime status | Merged |
| **#211 (this PR)** | SQL UPDATE, HTTP SQL CRUD and JAVA/JAR | Ready for review |
| [#213](https://github.com/melisource/fury_rio-controlplane-flink/pull/213) | PYTHON/ZIP | Stacked on this PR |

Playmaker integration follows this series in a separate PR; the [Playmaker hub](https://github.com/melisource/fury_rio-playmaker/blob/develop/local/RIO_E2E.md) records it as pending.

## What changes

This PR builds on the runtime from #209: the health view for provision/start, the activity view for stop/update/delete, pending SQL operation recovery and idempotent create.

- **SQL UPDATE** replaces a stopped application's definition, and the production UPDATE chain starts jobs with the new transformation. The stopped check uses the activity view, so an application whose jobs are all FAILED or CANCELED can be updated. Update registers the replacement directly because `create()` keeps an already registered application unchanged.
- **HTTP SQL CRUD** through `/flink/sql-code` creates, reads, lists by workspace and deletes the SQL that deployments reference.
- **JAVA/JAR** runs through the production Nexus search and multipart handlers. The nginx `nexus-local` stub serves `TopSpeedWindowing.jar` from the Flink image as `org.apache.flink:top-speed:1.20-local`, and `LocalNexusUrlValidator` allows HTTP only for that stub origin while keeping the production repository and path validation.
- **Shared storage:** `LocalFlinkStorage` serves SQL CRUD, deployment attachments and multipart uploads. It retains SQL and artifacts after UPDATE and DEPROVISION, as S3 does, so `CheckArtifactHandler` reuses a cached artifact on re-provision.
- **Runtime split:** `LocalFlinkJobLauncher` owns the calls to the Flink endpoints: SQL sessions and their replacement, statement submission through `LocalFlinkSqlOperations` from #209, JAR upload and run, and job cancellation. `LocalFlinkRuntime` keeps only application state.
- **Replacement-session cleanup** ([suggested in #209](https://github.com/melisource/fury_rio-controlplane-flink/pull/209#discussion_r4318564696)): when a restart fails to delete the previous session and the compensating DELETE of its replacement also fails, the launcher keeps the replacement handle. The next stop, which also runs on start rollback and delete, retries the close without blocking the lifecycle and keeps the handle while the close still fails.
- **E2E runner fix:** the runtime-failure case now reads the input topic from its current end offset. With the earliest offset, its integer-cast INSERT failed on records from earlier cases before PROVISION completed, and the health view from #209 then correctly reported that PROVISION as FAILED. This also fixes the same case on `develop`.

## Why

Complete the SQL feature set (UPDATE and SQL managed over HTTP) and add the second deployable language, JAVA/JAR, with the same transparent local path as #209. `src/main` and `src/test` have no diff against `develop`.

## How this was tested

- `./gradlew --offline test jacocoTestReport localTest`: PASS; 1937 production tests and 28 local tests, zero failures, errors or skips; production line coverage 96.06% and branch coverage 91.59%.
- `retainsOriginalStateWhenReplacementSessionCleanupAlsoFails` covers the double DELETE failure, a failed retry that keeps the handle, the successful close, no further retries and a later restart; it fails when the retry is removed.
- Pre-commit: PASS, including formatting, Checkstyle and PMD.
- Physical E2E from an empty `colima-rio`, one run on the `91cdd5f8` tree: PASS. It covers SQL with two INSERTs and comments through PROVISION, stop/start, runtime POLL, UPDATE and DEPROVISION; invalid SQL with rollback; FAILED+RUNNING stop; HTTP SQL CRUD with real data and SQL retained after DEPROVISION; JAR PROVISION, stop/start, UPDATE with a new job and file sink and DEPROVISION; and JAR re-provision with a cache hit and no new Nexus download. Teardown left 0 containers and 0 `rio-*` networks.
- GitHub checks on `91cdd5f8`: continuous integration, code coverage, dependencies, static analyzer, workflow and CodeQL PASS; Code Reviewer NEUTRAL with no open threads.

## Issue / specification

RIO E2E local. Branch `feature/rio-e2e-local-flink-pr2` → `develop`. Operational instructions: `local/README.md`, section "SQL UPDATE, HTTP SQL CRUD and JAVA/JAR"; integration source: `fury_rio-playmaker/local/RIO_E2E.md`. PYTHON/ZIP belongs to #213; GCP and Playmaker are outside this series.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## Notas internas — NO van al PR

- La cobertura de `jacocoTestReport` mide sólo el código productivo (task `test`); `src/local` no entra en ese reporte. Por eso coincide con el 96,06% de #209.
- El E2E limpio corrió sobre `03e681b7` más el cambio de `local/e2e.py` sin commitear; el commit `91cdd5f8` agrega sólo ese archivo, así que el árbol es idéntico. Dos corridas previas no cuentan como evidencia: la primera falló por el caso del offset y la segunda se hizo sobre un stack con jobs vivos.
- #209 entró como squash (un padre); por eso #211 se sincronizó mergeando primero `feature/rio-e2e-local-flink-kiss` y luego `develop`.
- La descripción de #209 (mergeado) todavía menciona la mejora de Karla como seguimiento opcional en #211; no se editó un PR mergeado.
- Tensión heredada: #209 agregó un seam productivo (`ActionAppQuery`, query opcional de stop en `ActionProcessor`/`ActionPollingJob`) pese a la regla «sin cambios productivos»; la tabla de serie lo nombra para que la historia sea honesta.
