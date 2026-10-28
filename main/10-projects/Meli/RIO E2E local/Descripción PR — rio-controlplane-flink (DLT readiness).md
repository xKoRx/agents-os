---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related: ["[[RIO E2E local]]", "[[rio-controlplane-flink]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-28"
---

# Descripción PR — rio-controlplane-flink (DLT readiness)

Repo: `melisource/fury_rio-controlplane-flink` · branch `feature/local-kafka-dlt-readiness` · base `develop` @ `e8755055` · commit `06e073bd` · 6 archivos (+257/-10) · [PR #221](https://github.com/melisource/fury_rio-controlplane-flink/pull/221) · validación 2026-10-28.

## Propósito

Conservar la descripción del nuevo PR que aborda los dos comentarios de marellanoqui_meli en #218.

## Contenido

Sin template de PR en este repo; se usan las secciones mínimas. Cuerpo en inglés para el repositorio.

---

## What changes

Local Kafka readiness now requires both configured Flink dead-letter topics to be describable, in addition to the existing trigger-topic assignment checks. Missing topics, metadata failures and timeouts return HTTP 503; the metadata request and wait are bounded to two seconds, and interruption preserves the thread interrupt flag. Spring owns and closes the metadata client.

The adapter and listener tests now use the actual trigger and DLT names from `application-local-kafka.yml`.

## Why

Follow-up to the two review comments on #218: a missing action DLT can prevent recovery of a poison record while the shared consumer still appears ready; test topic names also represented a different topology from the real configuration. This detects missing DLTs; it does not isolate the shared consumer against runtime dead-letter publish failures.

Only local source sets, local tests and local documentation change.

## How this was tested

- `./gradlew localTest test`: 1,969 production tests and 100 local tests passed; the subsequent local suite, including the real-client timeout regression, passed 101 tests.
- Temporary JaCoCo report for the local source set: readiness 100% lines and branches, trigger configuration 100% lines.
- Pre-commit checks: credentials, PII, formatter, Checkstyle and PMD passed on the final staged diff. The final readiness-focused suite also passed (15 tests).
- `.lore/ecosystem/rio-ecosystem all flink-sql flink-sql-invalid flink-jar flink-python cross-cp-pipeline` from Playmaker develop, with `RIO_CP_FLINK_ROOT` pointing to this branch: **13/13 Lore scenarios and 23/23 backend oracles passed, with 0 failed, blocked or skipped scenarios**.
- Teardown exited 0: no containers or RIO networks remain on `colima-rio`; Playmaker, frontend and Lore ports are closed.
- GitHub CI, code coverage, dependencies, static analyzer, CodeQL and workflow checks passed.

| Case | Lore run | Scenarios | Backend oracles |
|---|---|---|---|
| Flink SQL deploy and stop/start | `run_mvs3jjk180bcdd250b` | 3/3 | 5/5 |
| Invalid SQL | `run_mvs3pwmh1f4d8aaf81` | 2/2 | 2/2 |
| JAR deploy and stop/start | `run_mvs3tgq911dbc6b295` | 3/3 | 4/4 |
| Python deploy and stop/start | `run_mvs3zb4d325ab9df74` | 3/3 | 4/4 |
| Kafka → Flink → Kafka → ClickHouse | `run_mvs44fnhc489dfe5a6` | 2/2 | 8/8 |

The oracles verified deployment/action results, real running jobs, SQL and Python record transformations, and a record arriving in ClickHouse through the cross-control-plane pipeline. Each Lore run includes the shared smoke scenario. Lore duration: 19 min 32 s; reported cost: US$4.18.

Tested revisions: Flink `06e073bd`, Playmaker `20e0a9109`, Kafka `f4b5701`, ClickHouse `b1dbe13d`, frontend `8677932f`, Lore `e1c05ef`. All supporting applications were on `develop`; only Flink used the candidate feature branch.

## Issue / specification

Follow-up to [#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218), comments [missing DLT readiness](https://github.com/melisource/fury_rio-controlplane-flink/pull/218#discussion_r4389708695) and [test topic names](https://github.com/melisource/fury_rio-controlplane-flink/pull/218#discussion_r4389709058).

---

## Notas internas — NO van al PR

El alcance es readiness y nombres de tests; consumidores separados quedan fuera. Playmaker develop conserva nombres de ramas premerge en el manifiesto del runner: doctor advierte, pero no bloquea. El chequeo Grimoire de Playmaker detectó instalación global distinta a su pin; no se instaló ni alteró. AOC update-internal no pudo cargar su cache de prompts. Sin Zord: esta tarea implementa feedback existente, no solicita un nuevo code review.
