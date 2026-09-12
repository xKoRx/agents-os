---
type: change_log
schema_version: 1
scope: session
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Echo]]"
project: "[[Echo — E-04 Forge Ingestion E1]]"
application: "[[echo-core]]"
entities:
  - "[[Echo — Live Platform V1]]"
  - "[[Echo — E-03 Identity and BWC Foundation E0]]"
  - "[[echo-core]]"
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

# 2026-09-12-echo-e04-normal-implementation

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-04 Forge Ingestion E1.md` (estado + bitácora + WPs: NORMAL IMPLEMENTING → IMPLEMENTATION READY FOR MANAGER SOURCE REVIEW).
  - Repo `xKoRx/echo` branch `feature/e04-forge-ingestion-e1` (push FF `6beac29f..bfc0bc4b`): `03b20abd` ingestion core (DBTX mecánico, ArtifactSource/FilesystemStore, IngestionService, tests PG real), `fc590b31` gateway boundary (auth, POST/GET, wiring, HandoffIngress client, pack físico), `bfc0bc4b` SDD evidence (TASKS T01–T20 `[x]`, VERIFICATION.md NORMAL).

## Motivo

- Manager aprobó el planning E-04 → NORMAL one-shot ejecuta T01–T20 mecánicamente (SPEC v1.0.1 @ `c8e68538`, TASKS T17 @ `6beac29f`). E-03 no tocado; master read-only; T21 fail-closed por `FORGE_GOLDEN_FIXTURE_PENDING`.

## Fuentes usadas

- `specs/FEAT-FORGE-INGESTION-E1/{SPEC,PLAN,TASKS,VERIFICATION}.md` @ `6beac29f`; S0 READ ONLY @ `91671f6f`; PG 17.5 local port 5561 (harness E-03, DB `e04_ingestion`); MCPs Aranea vía [[aranea-mcps-expert]].

## Resolución aplicada

- Cambio mecánico único sobre repos E-03: `DBTX` (`v3/sdk/postgres/dbtx.go`); SQL y semántica write-once intactas (regresión E-03 34 PASS).
- Los AC de aceptación se demostraron con builders sintéticos S0-API + matriz G10 literal: el corpus S0 no embarca los bytes de artefacto que sus refs declaran (sólo G10; shas de G01 sin preimage). `TestCorpus_G01_ArtifactPreimages` documenta el 422 físico. Authority pin de bytes-artefacto = decisión Manager.
- Coverage gateway 92% / sdk ingestion ~77%: delta = plumbing defensivo inalcanzable + fault-injection; registrado en VERIFICATION.md.
- MCPs: DEV `echo-develop` sin tablas 061 (no mutado); Forge Mongo PROD sin manifest handoff dedicado → `FORGE_GOLDEN_FIXTURE_PENDING` sin cambio.

## Validación

- `tests/identity_bwc/run.sh` PASS (061 intacto); E-03 `Identity|Version|Promotion|Magic|Alias` 34 PASS; E-04 `-race` PASS (svc+gateway, PG real + HTTP físico + filesystem); SOURCE greps vacíos; `git diff c408a12f -- v3/sdk/contracts` y `migrations/` = 0; pre-push race OK; push FF; `origin/master` permanece `c408a12f`.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- La feature branch puede rebobinarse a `6beac29f` (FF-only). El vault vuelve al estado previo revirtiendo la nota del proyecto. Master no fue tocado.
