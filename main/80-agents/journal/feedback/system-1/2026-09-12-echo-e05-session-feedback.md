---
type: feedback
schema_version: 1
scope: session
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Echo]]"
project: "[[Echo — E-05 Analytics Convergence A0]]"
application: "[[echo-core]]"
entities:
  - "[[Echo — E-05 Analytics Convergence A0]]"
related:
  - "[[ZCode]]"
aliases: []
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# Session Feedback — 2026-09-12 E-05 NORMAL implementation (ZCode)

## Friction

- El host Linux no tiene `psql`/`initdb`/`pg_ctl` ni Docker daemon: el gate PG REAL exigió armar un PostgreSQL portable (binarios theseus-rs 17.11 musl + `libxml2.so.2`/`libicu74` extraídos de debs de Ubuntu archive). Los gates E-03/E-04/E-05 repiten este setup cada vez — un toolkit PG descartable versionado (`~/fuentes` o script de bootstrap) lo eliminaría.
- `yq` instalado vía mise no está en PATH directo del shell no-interactivo; la validación YAML terminó haciéndose con Python. Menor.

## Pain Pattern Candidate

- Gates SQL de repo (E-03 identity_bwc, E-05 analytics_a0) asumen `psql` en PATH y dependen del quirk documentado de `001_*` tolerante; cada nueva lane redisuelve el binario PG. Candidato a runbook único "PG descartable para gates Echo".

## What worked

- Planning v1.0.1 + Allowed Files explícitos hicieron la implementación lineal; MCPs Postgres/Hasura bastaron READ ONLY para evidencia DEV.
