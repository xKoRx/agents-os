---
type: decision
schema_version: 1
scope: project
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-27-durable-sdk-minio-atomic-create]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-PLANE-WRITE-ONCE-INTEGRATION-SLICE2-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
---

# Artifact Plane write-once — integración Slice 2

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- El baseline `8619a50` dejó dos writers MT5 sin la autoridad física write-once y mantuvo wiring productivo de un writer legacy sin callers legítimos.

## Decisión

- `UploadArtifactFromPath` y `PutObjectFromPath` usan exactamente `durableRefFromFile` → `openStableFile` → `putObjectIfAbsentAndReconcile`. El contrato público de `ArtifactRef.SHA256` permanece como hex lowercase de 64 caracteres sin prefijo. `mt5ObjectStore` compone `*storageminio.Storage`; `TradeListStorage` no se inyecta al boot productivo y TradeSet sigue `PersistTradeSet` → `PutPayload`.

## Rationale

- La autoridad compartida evita duplicar hashing/create-only/reconcile y garantiza fail-closed: same bytes = ACK; bytes distintos, incluso same-size = `CONTRACT_CONFLICT`; objeto remoto nunca se sobrescribe.

## Consecuencias

- Los cinco writers durable productivos quedan write-once sin schema/migration nuevos ni cambio del SDK pin. El estado global queda implementado pero pendiente de certificación física final de Slice 3.

## Alternativas descartadas

- Se descartan content-addressed keys, versionado S3, sidecars y una segunda implementación de hashing/reconcile: ampliar la autoridad existente conserva keys y contratos con menor blast radius.
