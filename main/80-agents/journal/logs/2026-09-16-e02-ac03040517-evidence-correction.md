---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Echo]]"
project: "[[Echo — E-02 Control Safety, Auth and Journal Recovery]]"
application:
entities:
  - "[[Echo — E-02 Control Safety, Auth and Journal Recovery]]"
  - "[[Echo — Live Platform V1]]"
related:
  - "[[Echo — Access & Physical Capability Matrix]]"
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

# 2026-09-16 E-02 evidencia AC-03/04/05/17

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `xKoRx/echo` `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/VERIFICATION.md` @ `92d0ec2e` (producto `f6e6af1b` intacto)
  - `10-projects/Echo/agentes/Echo — E-02 Control Safety, Auth and Journal Recovery.md`
  - `10-projects/Echo/agentes/Echo — Live Platform V1.md`
  - `10-projects/Echo/agentes/Echo — Access & Physical Capability Matrix.md`

## Motivo

- La certificación independiente marcó PASS en AC-03/04/05/17 con evidencia que no cubría el flujo integrado exigido por SPEC §12 (triggers a `.211` sin Bearer, hook ausente, GraphQL por admin-secret, sin E2E permanente).

## Fuentes usadas

- SPEC v1.0.2 §12; PLAN §3 (activación ≠ certificación de fixture); capabilities `aranea-hasura-dev-admin`, `aranea-kafka-dev-admin`, `aranea-ssh` profile `docker-echo-dev-operator`.

## Resolución aplicada

- Se construyó un stack Hasura+PG descartable en `.75` y un Gateway fixture en Daedalus con producer recorder; no se mutó Hasura compartido ni Kafka DEV. Evidencia nueva en VERIFICATION.md; historia previa conservada.

## Validación

- AC-03/04/05/17 PASS con request/response, event_log `delivered=t error=f`, GraphQL tokenizado, hook-down fail-closed y close-positions aislado (`partition_count=0` en Kafka). Cleanup `compose down -v` + shred de secretos.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit documental `92d0ec2e` en la feature; el producto `f6e6af1b` no cambió.
