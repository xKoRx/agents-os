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
updated: "2026-10-20"
---

# Descripción PR — rio-controlplane-flink (E2E local PR 3)

Repo fury_rio-controlplane-flink · rama `feature/rio-e2e-local-flink-pr3` @ `e7e12bff` · base `feature/rio-e2e-local-flink-pr2` @ `91cdd5f8` (#211) · diff base...HEAD: 13 archivos/+333/−29 · src/main y src/test sin diff contra develop ni #211 · 1937 productivos/30 locales, cobertura productiva 96,06% líneas/91,59% ramas, pre-commit PASS · E2E físico completo PASS en `e7e12bff` desde VM vacía, cleanup 0/0 · CI verde, 0 hilos · PR draft [#213](https://github.com/melisource/fury_rio-controlplane-flink/pull/213) · verificado 2026-10-20.

## Propósito

Recurso del proyecto con la descripción del PR, alineada con la serie #209 → #211 → #213 para que las tres cuenten una sola historia. El repo no tiene template de pull request; se reutilizan las secciones de #209 (What changes / Why / How this was tested / Issue / specification) precedidas por una tabla de serie idéntica en #211 y #213. El cuerpo está en inglés conforme a CLAUDE.md y se redactó con [[human-first-technical-writing]].

## Contenido

Título del PR: `feat(local): PYTHON/ZIP (PR 3 of 3)`.

Cuerpo listo para GitHub entre los separadores.

---

## Series: standalone local Flink E2E

The Flink control plane runs locally against a real Kafka broker, SQL Gateway, JobManager and TaskManager, through its existing controllers, handlers and pollers. Local adapters replace the AWS KDA and S3 operations; production code stays unchanged except for the optional stop query added in #209. The work lands in three PRs, one deployable language at a time:

| PR | Adds | Status |
|---|---|---|
| [#209](https://github.com/melisource/fury_rio-controlplane-flink/pull/209) | SQL lifecycle: PROVISION, DEPROVISION, stop/start and runtime status | Merged |
| [#211](https://github.com/melisource/fury_rio-controlplane-flink/pull/211) | SQL UPDATE, HTTP SQL CRUD and JAVA/JAR | Ready for review, base of this PR |
| **#213 (this PR)** | PYTHON/ZIP | Draft, stacked on #211 |

Playmaker integration follows this series in a separate PR; the [Playmaker hub](https://github.com/melisource/fury_rio-playmaker/blob/develop/local/RIO_E2E.md) records it as pending.

## What changes

This PR adds the third deployable language on top of #211, reusing its JAR submission, job tracking, stop/start, cancellation and storage.

- **Python image:** the local Flink image installs `apache-flink==1.20.5` with Python 3 and loads `flink-python` from `/opt/flink/lib`. pip reads the Fury PyPI mirror through a BuildKit secret (`pip_conf`), so the mirror credential never reaches image layers or history. The image links `python` to `python3` because the PyFlink client and the Beam workers invoke `python`.
- **Nexus stub:** `nexus-local` also serves `org.apache.flink:py-upper:1.20-local`, a ZIP with the KDA layout: `src/main/python/main.py`, a PyFlink job whose Python UDF maps each Kafka value to `py-` plus its lowercase value, and `lib/pyflink-dependencies.jar`.
- **Submission:** `LocalFlinkRuntime.create` accepts JAR and ZIP binaries. For PYTHON deployments, `LocalFlinkPythonArchive` extracts the stored ZIP into the shared `python-apps` volume (`/opt/rio/python/<application>`, read-only in JobManager and TaskManager) and rejects entries that resolve outside the application directory. `LocalFlinkJobLauncher` then uploads `lib/pyflink-dependencies.jar` and runs it with `org.apache.flink.client.python.PythonDriver` and `-py` pointing to the extracted `main.py`, mirroring the KDA `python`/`jarfile` run options.

## Why

Complete the standalone local E2E series with the last language the control plane deploys, using the production controllers, handlers and pollers. `src/main` and `src/test` have no diff against `develop` or #211.

## How this was tested

- `./gradlew --offline test jacocoTestReport localTest`: PASS; 1937 production tests and 30 local tests, including Python ZIP submission through PythonDriver and zip-slip rejection, zero failures, errors or skips; production line coverage 96.06% and branch coverage 91.59%.
- Pre-commit: PASS, including formatting, Checkstyle and PMD.
- Physical E2E from an empty `colima-rio`, one run on `e7e12bff`: PASS. It covers every SQL and JAR scenario from #211, plus PYTHON/ZIP: PROVISION with the job RUNNING, Python UDF output on Kafka, stop/start with a new job and more output, DEPROVISION with the job CANCELED, and re-provision with a cache hit and no new ZIP download from Nexus. Teardown left 0 containers and 0 `rio-*` networks.
- The mirror credential is absent from the E2E log and from the history and metadata of every Flink image in `colima-rio`.
- GitHub checks on `e7e12bff`: continuous integration, code coverage, dependencies, static analyzer, workflow and CodeQL PASS.

## Issue / specification

RIO E2E local. Branch `feature/rio-e2e-local-flink-pr3` → `feature/rio-e2e-local-flink-pr2` (#211); retarget to `develop` after #211 merges. Operational instructions: `local/README.md`; building the image requires GlobalProtect, `docker-buildx` and `RIO_PIP_CONF` pointing to a Fury `pip.conf`. Python UPDATE uses the language-independent UPDATE chain covered by SQL and JAR, so it has no dedicated E2E scenario. GCP and Playmaker are outside this series.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## Notas internas — NO van al PR

- **Bloqueante de forma, no de código:** #213 sigue en draft y apunta a #211; sacarlo de draft y retargetear a `develop` después del merge de #211.
- Spike previo: REST `/jars/upload` + `/jars/<id>/run` con `PythonDriver` y `-py`; `-pyclientexec`/`-pyexec` no alcanzan al worker Beam del TaskManager; el symlink `python → python3` resuelve cliente y worker sin flags, igual que el contrato KDA.
- PyFlink en aarch64 no tiene wheel binario y compila (~10 min); la capa queda en caché del builder de `colima-rio`. Un build en frío necesita el mirror Fury.
- Divergencia conocida: KDA ejecuta el ZIP con su runtime administrado; localmente se usa PythonDriver vía REST. El layout (`src/main/python/main.py`, `lib/pyflink-dependencies.jar`) es el mismo.
- La extracción ZIP pasó a `LocalFlinkPythonArchive` al re-sincronizar con #211 porque PMD marcaba GodClass en el launcher.
