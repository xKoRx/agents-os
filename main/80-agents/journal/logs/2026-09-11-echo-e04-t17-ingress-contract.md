---
type: change_log
schema_version: 1
scope: session
created: "2026-09-11"
updated: "2026-09-11"
area: "[[Echo]]"
project: "[[Echo — E-04 Forge Ingestion E1]]"
application: "[[echo-core]]"
entities:
  - "[[Echo — E-04 Forge Ingestion E1]]"
related:
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-11-echo-e04-t17-ingress-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-04 Forge Ingestion E1.md` — planning: T17 alineado a `payloadDigest`; HEAD `6beac29f`; no implementing/closed.
  - Repo `xKoRx/echo` `feature/e04-forge-ingestion-e1` @ `6beac29f9b6daa5a3d935b7074de3bb2b2098014`: `specs/FEAT-FORGE-INGESTION-E1/TASKS.md` T17.

## Motivo

- Contradicción documental: SPEC v1.0.1 §6.1 ya tenía `Deliver(ctx, ns, *HandoffManifestV1, payloadDigest)`; TASKS T17 omitía `payloadDigest`.

## Fuentes usadas

- `80-agents/skills/agents-os-bootstrap`, constitución, `agents-os-agent-project-workflow`, `agents-os-entity-update`
- [[Echo — E-04 Forge Ingestion E1]]
- Authority F-04: `sqx/core/capabilities/handoff.go` @ `ea8be76` (inspección previa; no se reabrió Symphony)

## Resolución aplicada

- T17 queda `Deliver(ctx, ns, *HandoffManifestV1, payloadDigest) (PromotionRecord, httpStatus, error)`. `payloadDigest` verifica coincidencia con `receipt.payload_digest`; Echo sigue computando digest server-side. SPEC/PLAN/VERIFICATION no tocados. T21/`FORGE_GOLDEN_FIXTURE_PENDING` y E-03 interlock intactos.

## Validación

- `python3 80-agents/skills/_shared/scripts/materialize_schema_note.py` para este change_log.
- Echo: `git push` FF `c8e68538..6beac29f` a `origin/feature/e04-forge-ingestion-e1`; `origin/master` permanece `c408a12f`.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir delta Agents OS E-04; revertir commit `6beac29f` en la feature branch. No afecta `origin/master`.
