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
updated: "2026-10-09"
---


# Descripción PR — rio-controlplane-kafka

**PR:** [Kafka #86](https://github.com/melisource/fury_rio-controlplane-kafka/pull/86) ·checks ejecutables SUCCESS,2026-10-09T18:22:45Z; Code Reviewer NEUTRAL y Upload empty SARIF SKIPPED.

**Identidad:** melisource/fury_rio-controlplane-kafka · feature/rio-e2e-local-kafka @90710a590794e8a35b39f420013b24e2367ea4c1 · base develop@6a91937c0664d83f907dec222af8a96b4042c6ae ·4 commits ·20 archivos,+1691/-16 ·SPEC funcional/técnica feature20261009 ·companionPM paraE2E ·691/50/25 y normal/gap root+independiente PASS2026-10-09.

## Propósito

Descripción reviewable del PR CP Kafka; texto generado con human-first-technical-writing y pr-description, sustentado en la entrega F1.

## Contenido

Cuerpo listo para GitHub. Este repo no tiene template de PR; se usan secciones mínimas de cambio, motivo, validación y spec.

---

## What changes

Adds embedded Kafka ingress and result publishing for local Playmaker → CP Kafka E2E. With `compose,local,local-kafka`, raw SDK deployment/action events enter the existing productive controllers, processors and publishers. One broker remains owned by CP Compose; Playmaker's runner supplies the ecosystem topics. The standalone HTTP/local flow remains available.

Spring Kafka owns intake, retry, rebalance and shutdown. Recovery preserves the original bytes/key, waits for acknowledged DLT publication before committing, and uses a bounded two-retry budget even when exception types change. Local readiness also fails when the consumer stops or loses assignment. The existing cluster-registry fallback replaces a synthetic environment map.

## Why

Testing only BigQueue-shaped HTTP requests misses asynchronous wire, offset, replay and result-consumption behavior. This profile replaces the local BigQueue transport with Kafka while retaining the real business handlers. The productive `src/main` sources are unchanged. Local Kafka clients4.2.1/Spring Kafka4.1.1 are isolated from the productive artifact, which retains clients3.9.2 and excludes Spring Kafka and local classes/resources.

[Playmaker companion PR #1286](https://github.com/melisource/fury_rio-playmaker/pull/1286) is required to execute the ecosystem matrix; it does not introduce a shared library or unpublished SDK dependency. ClickHouse, Flink, browser journeys and corporate BigQueue/auth are later phases.

## How this was tested

Source `b0d4587f0e0fc90180ddb5ceb05bdd96c3147dc8`; PR HEAD `90710a590794e8a35b39f420013b24e2367ea4c1` adds Markdown only. JDK25, CP target21. Local evidence and immutable independent rebuilds bind tests to identical jar hashes.

- `./gradlew --offline test`:691 tests, zero failures/errors/skips.
- `./gradlew --offline localTest jacocoLocalKafkaCoverageVerification compileLocalFunctionalTestJava verifyLocalArtifactIsolation`:50 local tests, zero failures/errors/skips; critical lines164/164(100%), branches49/50(98%); artifact/dependency isolation PASS. Framework tests use the actual configured Spring containers/error handlers and Kafka client test doubles, including failed/pending DLT ACK, poll failure, retries, restart and readiness.
- `./gradlew --no-daemon localFunctionalTest` against the real standalone broker:25/25 PASS, owned cleanup certified; source unchanged.
- Playmaker physical runner: root normal2×11/11 + publication-gap2×1/1 (`f4ec56bb0c47`), independently reproduced from exact-commit clean clones: normal2×11/11 with productive budgets (`d566b230fa3b`) and fresh15s gap2×1/1 (`12e65ac4a701`). Zero failures/errors/skips; physical lifecycle/PEEK/replay/DLT and actual CP restart with retained offsets verified. No HTTP bridge or fabricated successful result.

The passing stacks use the explicit healthy Docker context `colima-rio-kafka-e2e-01a0f8e0`. Cleanup preserves baseline networks/images and leaves no own process/container/volume/state; ports become reusable after host forwarding/TCP settles (54s observed). The original `colima-rio` profile is offline after host ENOSPC/I/O; its interrupted run's cleanup is uncertified and private recovery state is preserved. Passing the healthy context does not certify repair or cleanup of that old profile. The productive swallowed-publication gap and unmapped GCP PEEK failure remain visible.

Full matrix, limits and hashes: [verification](https://github.com/melisource/fury_rio-controlplane-kafka/blob/90710a590794e8a35b39f420013b24e2367ea4c1/meli/features/20261009-rio-e2e-local/4-implementation/VERIFICATION.md). [Independent disposition](https://github.com/melisource/fury_rio-playmaker/blob/ccc43d0d5c83ec2d144d022db011ec98ea9ec038/meli/features/20261009-rio-e2e-local/4-implementation/SIMPLIFICATION_REVIEW.md). Remote checks on90710a5 passed: continuous-integration, code-coverage, dependencies, static-analyzer, CodeQL/java, CodeQL/configuration and workflow. Code Reviewer concluded NEUTRAL and Upload empty SARIF was SKIPPED; human review/merge remains separate. Local evidence does not substitute for these actual remote results.

The new integrated Playmaker source642aa53 includes current develop authorization. Its root run44941be9e81d passed normal2×11 and gap2×1 with the same CP local jar7fe507; cleanup certified. Independent integrated-source reproduction completed: normal productive-budget810238a329de2×11/11 and fresh15s gap9444d48eba3d2×1/1,0 failures/errors/skips; exact CP local jar, baseline preservation and bounded port reuse verified. [Final companion review](https://github.com/melisource/fury_rio-playmaker/blob/c3ecf8cb78bf5f4a8df093e1a1a40488d6d91a7f/meli/features/20261009-rio-e2e-local/4-implementation/PR_INTEGRATION_REVIEW.md). Prior PM90df evidence above remains historical for PM and current for unchanged CP source, not certification of new PM bytecode.

## Issue / specification

AGENTS OS project RIO E2E local, F1. Repository specifications: `meli/features/20261009-rio-e2e-local/1-functional/spec.md` and `2-technical/spec.md`; execution guide `local/README.md`. No Jira issue was supplied.

---

## Notas internas — NO van al PR

- Autorización explícita del owner para crear y pushear los dos PR prevalece sobre el alcance sólo autoría de pr-description; no merge/deploy autorizado.
- Kafka no tiene delta de develop; PM preservó auth upstream y está publicado en #1286 tras gates completos y nuevas cuatro suites físicas. Independiente integrado PASS calificado; PM CodeQLstartup pendiente, CIprincipalPASS.
- VM original offline y cleanup36868 no certificado son deuda operacional, sin reinterpretarla como PASS. MCPs security/dependency-analysis no disponibles en la entrega local; los checks remotos reales del PR sí pasaron y se registran por separado.
