---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[RIO E2E local]]"
  - "[[RIO E2E local — Integración Flink Playmaker]]"
  - "[[CP Flink local]]"
  - "[[rio-controlplane-flink]]"
  - "[[Descripción PR — rio-playmaker (E2E local Flink)]]"
  - "[[Descripción PR — ads-signals-frontend (RIO ecosistema local)]]"
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-23"
updated: "2026-10-23"
---

# Descripción PR — rio-controlplane-flink (E2E local Playmaker)

Repo fury_rio-controlplane-flink · [PR #218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218) (listo para review) · rama `feature/rio-e2e-local-flink-playmaker` @ `da3e33c6` · base `develop` (al día) · 3 commits · 12 archivos/+556/−66 · `src/main` y `src/test` sin diff · hermanos Playmaker [#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332) y front [#824](https://github.com/melisource/fury_ads-signals-frontend/pull/824) · `./gradlew test` 1966/0, `localTest` 86/0, pre-commit PASS · CI 2 checks OK · verificado 2026-10-23.

> [!note] Sin bloqueantes de merge en este repo
> Al día con `develop`, sin artefactos sin publicar. Es el primero en mergear de la ronda.

## Propósito

Recurso del proyecto con la descripción del PR del CP Flink para su integración local con Playmaker. Vive en el vault, no en el repo, según [[pr-description]].

## Contenido

Título del PR: `feat(local): integrate with Playmaker through Kafka action triggers`.

El repo no tiene template de pull request; se reutilizan las secciones de la serie #209/#211/#213 (What changes / Why / How this was tested / Issue), precedidas por la evidencia Lore y la tabla de la iniciativa. Cuerpo en inglés publicado en GitHub entre los separadores.

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


## What changes

The standalone local stack from #209, #211 and #213 already consumed deployment triggers from Kafka, but actions arrived only through `POST /triggers/actions`, while Playmaker publishes them to Kafka. This PR closes that gap and makes deployments created from `ads-signals-frontend` run locally, which is what lets the Flink cases above (`flink-sql`, `flink-sql-invalid`, `flink-jar`, `flink-python`, `cross-cp-pipeline`) pass from the browser. `src/main` and `src/test` have no diff against `develop`.

- **Action intake from Kafka:** `LocalKafkaTriggerListener` also subscribes to `rio-action-trigger-local`. `LocalKafkaTriggerAdapter` routes by topic: actions are wrapped as the BigQueue envelope, bound to `BigQueueMessage<ActionTriggerMessage>` and passed to the existing `ActionTriggerController.handleActionTrigger`. The same listener id keeps the readiness check covering both topics, and the same group (`rio-cp-flink-local`) means component types owned by other control planes are acknowledged as no-ops by the productive controller.
- **Same delivery rules as deployments:** record acknowledgement, two retries one second apart, poison payloads straight to the dead-letter topic, and a separate DLT for actions (`rio-action-trigger-local-dlt-flink`). The controller is asynchronous, so the commit marks acceptance; the terminal state still travels through `rio-action-result-local`.
- **Standalone runner:** `local/e2e.py` publishes actions to Kafka like Playmaker does, using the SDK field `action_timeout` (the previous `timeout` key was ignored by the snake-case mapper). `RIO_E2E_KAFKA_CONTAINER` selects the broker container for the integrated stack.
- **Frontend SQL deployments:** the frontend names the production SQL runner (`com.mercadolibre.library:rio-flink-sql:1.0.3`) in `flink-sql` deployments. The Nexus stub serves a placeholder for it so the productive upload handler succeeds, and `LocalFlinkJobLauncher.runsSql` sends any deployment that carries SQL files through the SQL Gateway, which plays the runner's role locally. JAR and Python deployments keep their binary path.
- **Documentation:** `local/README.md` describes the integrated Kafka mode (shared broker and network owned by the Kafka control plane, extra topics and DLTs) and the runner placeholder.

## Why

Let Playmaker and the frontend drive the Flink control plane end to end in the local RIO ecosystem (deploy, stop/start, runtime status and results) without changing production code. The Playmaker side, with the ecosystem runner and cases, is [rio-playmaker#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332).

## How this was tested

HEAD `da3e33c6`, up to date with `develop`, Java 25, VM `colima-rio`.

- Browser, through the frontend and Playmaker — see "Lore end-to-end evidence" above: the five Flink cases passed with this branch, including a record that crosses Kafka, Flink and ClickHouse in one deployment.
- `./gradlew test` — 1966 tests, 0 failures.
- `./gradlew localTest` — 86 tests, 0 failures. New coverage: a valid action reaches the controller with its SDK fields intact; a foreign component type goes through the real controller and is acknowledged without work; oversized, non-UTF-8, wrapped and multi-object payloads go straight to the action DLT with their original bytes and key; a rejected action is retried twice before reaching its own DLT while deployments keep theirs; SQL files take precedence over a named runner binary, and binary-only deployments keep the binary path.
- Pre-commit (credentials, PII, formatter, Checkstyle, PMD) — PASS.
- Physical, standalone (`local/e2e.py` at `ac019e17`): SQL, UPDATE, SQL CRUD, JAR and Python flows passed with actions sent through Kafka; a poison action reached `rio-action-trigger-local-dlt-flink` with its key and bytes while the consumer kept running.
- Physical, through Playmaker's `localFlinkIntegrationTest`: SQL provisioning and stop/start, redeploy, invalid SQL, JAR and Python passed; Kafka and ClickHouse control plane regressions passed with this control plane running.
- Cleanup — 0 containers and 0 `rio-*` networks after every run.

## Issue / specification

RIO local E2E initiative (see the table above); follows #209, #211 and #213. Sibling PRs: [rio-playmaker#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332) (Playmaker) and [ads-signals-frontend#824](https://github.com/melisource/fury_ads-signals-frontend/pull/824) (frontend README). Operational instructions are in `local/README.md` and Playmaker's `.lore/ecosystem/README.md`.

---

## Notas internas — NO van al PR

- **Commits mixtos:** `ac019e17` usa `feat(local):`; `ff0e8d10` y `da3e33c6` usan sujetos imperativos sin prefijo.
- **Alcance del runner:** `runsSql` decide por presencia de archivos, no por tipo de componente. Hoy sólo `flink-sql` envía archivos; si un `aws-flink-job` llegara a traerlos, iría por SQL. Aceptado por KISS y por emular el runner productivo.
- **Fuera de alcance, sin fix:** envelopes crudos con credenciales sintéticas en logs del CP (observación de F3); doble dispatch de `CreateAppInAWSHandler`/`StartAppInAWSHandler` y `component_type: null` en el resultado de undeploy siguen como tareas de [[CP Flink local]].
- **Plan:** fases, gates y decisiones en [[RIO E2E local — Integración Flink Playmaker]].
- **Orden del cuerpo:** las secciones «Lore end-to-end evidence» y «RIO local E2E initiative» van antes del template por pedido del owner (pruebas arriba, iniciativa y PRs hermanos navegables); son idénticas en los tres PRs.
- **Borrador:** `gh pr create` dejó los tres PRs como draft; el owner pidió marcarlos listos para review el 2026-10-23.
