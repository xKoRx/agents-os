---
type: decision
schema_version: 1
scope: project
created: "2026-08-28"
updated: "2026-08-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[durable-verified-reads-apply-reconcile-infers-digest-from-key]]"
  - "[[2026-08-27-durable-artifact-plane-write-once-final-e2e]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
---

# 2026-08-28-durable-artifact-verified-reads-final-e2e-normal

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Sesión operacional sobre Symphony baseline `5e93c7cda3f4fcc825f3939a951247cd4e63fec2`; SDK baseline `ea09cc1bb8b34e661c8f31f887dce58613b0475a`.
- Release desplegada: `0.2.78`, source SHA `5e93c7cda3f4fcc825f3939a951247cd4e63fec2`; sin cambios de código, schema, migration, commit ni Temporal Reset.
- Zeus, Hera, Kronos y Windows MT5 fueron observados en la misma release.

## Decisión

- No cerrar `ARTIFACT_VERIFIED_READS`. La certificación queda `BLOCKED / CLOSED` por un defecto productivo en la ruta durable de Apply.
- `ReconcileApplySelectedRun` ejecuta `StatObject(key)` y `GetObject(key)`, calcula SHA sobre los bytes obtenidos y fabrica un `DurableArtifactRef`; el digest esperado no proviene de Evidence/carrier.
- Siguiente RCA exacto: `DURABLE-ARTIFACT-VERIFIED-READS-APPLY-RCA-TOP`. No se aplica fix en esta sesión.

## Rationale

- El boundary canónico `FetchDurableToPath` validó Size y SHA256 antes de publicación atómica; el harness contra MinIO real confirmó mismatch same-size, missing object y cleanup de cohorte.
- Eso no compensa el defecto de autoridad en la reconciliación durable de Apply: un lector productivo no puede reconstruir la identidad desde el objeto almacenado.
- Intake normal creó FlowRun nuevo `16017335-b6af-4325-b810-cde3ae43d6ac`, token `ce5694aa-02a2-41b0-88e5-c5826e12572b`, workflow `sqx-main-v1-ce5694aa-02a2-41b0-88e5-c5826e12572b`, run `01a049c9-3d25-7771-b99c-0f57daf4d86b`; no se afirmó cadena completa hasta MT5.

## Consecuencias

- Gates: `DURABLE_LIST_AS_READ_AUTHORITY=0`, `ETAG_AS_DIGEST=0`; pero `DURABLE_KEY_ONLY_READ_AUTHORITY=1`, `KEY_TO_EXPECTED_DIGEST_INFERENCE=1` y `STAT_AS_INTEGRITY_AUTHORITY=1` por Apply.
- Prefijo disposable MinIO real: `certification/verified-reads-final-e2e-normal-1787945118675394000/`, bucket `sqx-strategies`. Válido size 23/SHA `sha256:2ec6cc4870c4e84806f63d59d9f98fdbd6f7331d91db3c46c7a8ef8f1e3fa55b`; mismatch actual `sha256:548fe67c014bcd0892887f767d225736f0414ee255ed605b5ddf7f859d542170` frente a expected `sha256:05e0c955c2d04fcdf9711765808f2b7b5d3c08cbe320da431320d645c1345a8d`; ambos size 23.
- Tests dirigidos de storage, WFM físico, MT5 y carriers relevantes pasaron. La suite SDK completa falló por módulos privados/dependencias y drift preexistente.
- Write-once permanece `CERTIFIED_CLOSED / NOT_REOPENED`; foreign dirty preservado.

## Alternativas descartadas

- No se reinterpretó un GET que calcula su propio SHA como verified read.
- No se corrigió Apply, no se hizo reset Temporal y no se mezclaron versiones.
