---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[CP Flink local]]"
  - "[[RIO E2E local]]"
  - "[[rio-controlplane-flink]]"
  - "[[Descripción PR — rio-controlplane-flink (E2E local PR 2)]]"
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-15"
updated: "2026-10-15"
---

# Descripción PR — rio-controlplane-flink (E2E local PR 3)

Repo fury_rio-controlplane-flink · rama feature/rio-e2e-local-flink-pr3 @ aaec54bd82d6dc0c20e60ad25844d99739dabab9 · base feature/rio-e2e-local-flink-pr2 @ 0728044c (#211) · 3 commits sobre la base · diff base...HEAD: 12 archivos/+310/−29; diff origin/develop...HEAD: 30 archivos/+3566/−0 (refs de origin del último fetch) · src/main y src/test sin diff contra ambas referencias · 1937 tests productivos/22 locales/pre-commit PASS · E2E físico completo PASS en aaec54bd, una corrida, cleanup 0 contenedores/0 redes rio-* · verificado 2026-10-15.

> [!warning] **Push pendiente.** La rama no está en origin: el push falló por IP allow list de GitHub (GlobalProtect desconectado). El PR se abre como draft contra `feature/rio-e2e-local-flink-pr2` después del push.

## Propósito

Recurso del proyecto con la descripción del PR 3. El repo no tiene template de pull request; se usan las secciones mínimas de pr-description más Scope y Project, igual que en el PR 2. El cuerpo está en inglés conforme a CLAUDE.md.

## Contenido

Título del PR: `feat(local): PYTHON/ZIP (PR 3 of 3)`.

Cuerpo listo para GitHub entre los separadores.

---

## What changes

- The local Flink image installs `apache-flink==1.20.5` with Python 3 and loads `flink-python` from `/opt/flink/lib`. pip reads the Fury PyPI mirror through a BuildKit secret (`pip_conf`), so the mirror token never reaches image layers or history.
- The `nexus-local` stub also serves `org.apache.flink:py-upper:1.20-local`, a ZIP with the KDA layout: `src/main/python/main.py` (a PyFlink job whose Python UDF maps each Kafka value to `py-` plus its lowercase value) and `lib/pyflink-dependencies.jar`.
- `LocalFlinkRuntime.create` accepts JAR and ZIP binaries. For PYTHON deployments, `LocalFlinkJobLauncher` extracts the stored ZIP into the shared `python-apps` volume (`/opt/rio/python/<application>`, read-only in JobManager and TaskManager), uploads `lib/pyflink-dependencies.jar` and runs it with `org.apache.flink.client.python.PythonDriver` and `-py` pointing to the extracted `main.py`. This mirrors the KDA `python`/`jarfile` run options and reuses the JAR job tracking, stop/start, cancellation and upload cleanup.
- ZIP entries that resolve outside the application directory are rejected.
- The image symlinks `python` to `python3` because PyFlink's client and Beam workers invoke `python`.

## Why

Complete the transparent local E2E environment for the Flink control plane with the third deployable language, using the production controllers, handlers and pollers and no production code changes. This is PR 3 of 3, stacked on [#211](https://github.com/melisource/fury_rio-controlplane-flink/pull/211).

## How it was tested

- `./gradlew test`: PASS, 1937 production tests, with no failures, errors or skips.
- `./gradlew localTest localBootJar check`: PASS, 22 local tests, including Python ZIP submission through PythonDriver and zip-slip rejection.
- Pre-commit: PASS, including formatting, Checkstyle and PMD.
- `src/main` and `src/test` have an empty diff against both `origin/develop` and `origin/feature/rio-e2e-local-flink-pr2`.
- Complete physical E2E: PASS on `aaec54bd` in one run. Scenarios cover every existing SQL and JAR suite plus PYTHON/ZIP: PROVISION with the job RUNNING, Python UDF output on Kafka, stop/start with a new job and more output, DEPROVISION with the job CANCELED, and re-provision with a cache hit and no new ZIP download from Nexus.
- The mirror token is absent from the image history, image metadata and the E2E log.
- Cleanup verified: 0 containers and 0 `rio-*` networks in `colima-rio`.

## Scope

Python UPDATE uses the language-independent UPDATE chain already covered by SQL and JAR, so it has no dedicated suite. GCP and Playmaker are outside this PR. Building the image requires GlobalProtect, `docker-buildx` and `RIO_PIP_CONF` pointing to a Fury `pip.conf` (documented in `local/README.md`).

## Project

RIO E2E local / CP Flink local · repository `fury_rio-controlplane-flink` · branch `feature/rio-e2e-local-flink-pr3` @ `aaec54bd` · base `feature/rio-e2e-local-flink-pr2` @ `0728044c` ([#211](https://github.com/melisource/fury_rio-controlplane-flink/pull/211)).

---

## Notas internas — NO van al PR

- Spike previo: REST `/jars/upload` + `/jars/<id>/run` con `PythonDriver` y `-py` dejó un job RUNNING con UDF Python y salida `py-alpha`/`py-beta` en Kafka. `-pyclientexec`/`-pyexec` no alcanzaban al worker Beam del TaskManager; el symlink `python → python3` resuelve cliente y worker sin flags, igual al contrato KDA.
- La instalación de PyFlink en aarch64 no tiene wheel binario y compila (~10 min); la capa queda en caché del builder de `colima-rio`. Un build en frío necesita el mirror de Fury accesible.
- Divergencia conocida: KDA ejecuta el ZIP con su runtime administrado; localmente se usa PythonDriver vía REST. El contrato de layout (`src/main/python/main.py`, `lib/pyflink-dependencies.jar`) es el mismo.
- Log físico: `/private/tmp/rio-pr3-e2e.log`.
