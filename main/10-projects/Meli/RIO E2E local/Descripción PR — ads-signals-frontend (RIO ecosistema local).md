---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[RIO E2E local]]"
  - "[[RIO E2E local — Integración Flink Playmaker]]"
  - "[[Descripción PR — rio-playmaker (E2E local Flink)]]"
  - "[[Descripción PR — rio-controlplane-flink (E2E local Playmaker)]]"
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-23"
updated: "2026-10-23"
---

# Descripción PR — ads-signals-frontend (RIO ecosistema local)

Repo fury_ads-signals-frontend · [PR #824](https://github.com/melisource/fury_ads-signals-frontend/pull/824) (listo para review) · rama `feature/rio-local-ecosystem-docs` @ `82055bd56` · base `develop` @ `4e7b95cbe` · 1 commit · `README.md` y `CHANGELOG.md` · sin cambios de código · hermanos Playmaker [#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332) y CP Flink [#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218) · suite no corrida (sólo docs) · verificado 2026-10-23.

> [!warning] Bloqueantes antes del merge
> **Link del README:** apunta a `.lore/ecosystem/README.md` en `develop` de Playmaker, que existe sólo cuando [#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332) mergee.

## Propósito

Recurso del proyecto con la descripción del PR de docs del front: cómo correrlo dentro del ecosistema RIO local. Vive en el vault, no en el repo, según [[pr-description]].

## Contenido

Título del PR: `docs: document running against the local RIO ecosystem`.

Cuerpo con el template `.github/pull_request_template.md` del repo, en inglés, precedido por la evidencia Lore y la tabla de la iniciativa.

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


# ![alt text][description] PR Description

## What is the current behavior?

The README explains local development against live Kraken and a Fury Tiger token, but not how to run this frontend inside the local RIO ecosystem (local Playmaker and the Kafka, ClickHouse and Flink control planes) or how to run the Lore end-to-end scenarios that exercise it.

## What is the expected behavior with the new change?

The README's Development section gains "Local RIO ecosystem", which points to the runner and runbook in Playmaker ([rio-playmaker#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332)) and states what the runner does here: it sets `PLAYMAKER_BASE_URL` to local Playmaker, uses the Tiger mock token, enables the recorded Kraken mocks through `NODE_CONFIG`, serves on `https://local.adminml.com:8443/`, and writes only the gitignored `mocks/development/` fixtures. The CHANGELOG records the entry under `[Unreleased]`.

No application code changes: the evidence above ran this frontend from `develop` @ `4e7b95cbe` unmodified. The integration needed only configuration that already exists (`PLAYMAKER_BASE_URL`, `TIGER_DEV_TOKEN`, `NODE_CONFIG`, the mocks under `mocks/test`).

# ![alt text][testing] Testing

## How to test the new behavior?

Documentation only. The section describes the setup used for the Lore evidence above; to reproduce it, run `.lore/ecosystem/rio-ecosystem setup` and `.lore/ecosystem/rio-ecosystem all` from Playmaker's branch `feature/rio-e2e-local-flink`. The README link targets Playmaker's `develop` and resolves once [rio-playmaker#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332) merges.

# ![alt text][checkmark] Related Issue

RIO local E2E initiative (see the table above). Sibling PRs: [rio-playmaker#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332) (Playmaker) and [rio-controlplane-flink#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218) (Flink control plane).

# ![alt text][checklist] PR Checklist

- [x] I carefully reviewed the code before creating this PR.
- [x] I made sure the `diff` clearly represents my changes.
- [x] I made sure this PR doesn't make sense to split into smaller PRs.
- [x] I verified that my code style and scaffolding follow the project standards.
- [x] I made sure my changes don't affect any functionality other than this PR.
- [ ] I added/modified the necessary `tests` for the component or functionality I'm implementing. — not applicable: documentation only.
- [ ] I ran the `tests` and made sure they pass. — not run: no code changed; the frontend ran unmodified in the Lore evidence above.
- [x] I updated the `CHANGELOG.md` file with the change in the `[Unreleased]` section under `Fixed` or `Added` as appropriate.
- [x] I made sure to update the README with the new behavior, if applicable.

[description]: https://img.icons8.com/material-sharp/24/000000/document.png
[checkmark]: https://img.icons8.com/material-sharp/24/000000/checkmark.png
[checklist]: https://img.icons8.com/material-sharp/24/000000/check-all.png
[testing]: https://img.icons8.com/material-sharp/24/000000/test-partial-passed.png

---

## Notas internas — NO van al PR

- **Tensión de convenciones:** `.claude/rules/semantic-commits.md` pide commits de una sola línea; el commit lleva el trailer `Co-Authored-By`. La rama usa el prefijo `feature/` que exige esa misma regla.
- **Orden del cuerpo:** las secciones «Lore end-to-end evidence» y «RIO local E2E initiative» van antes del template por pedido del owner; son idénticas en los tres PRs.
- **Borrador:** `gh pr create` dejó los tres PRs como draft; el owner pidió marcarlos listos para review el 2026-10-23.
