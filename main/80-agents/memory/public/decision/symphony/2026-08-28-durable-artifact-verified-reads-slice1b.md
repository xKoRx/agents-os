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
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-27-durable-artifact-verified-reads-rca]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-SLICE1B-WFM-APPLY-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - scope/symphony
  - project/echo-forge
  - tech/durable-pipeline
---

# 2026-08-28-durable-artifact-verified-reads-slice1b

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Slice 1B de `xKoRx/symphony` sobre baseline `1e2564062987b7762f29c499b90c1e91522c1a96`, con Artifact Plane write-once certificado y Slice 1 de verified reads cerrados.
- El pipeline durable ya llevaba `DurableArtifactRef` como autoridad física; faltaba cerrar la frontera WFM → robust selection → ApplySelectedRun → FinalReretester.

## Decisión

- `DurableApplySelectedRunResult.Artifact` transporta el `DurableArtifactRef` exacto reconciliado/producido, y `ObjectKey` queda sólo como mirror obligatorio (`ObjectKey == Artifact.ObjectKey`). El workflow valida el resultado y reemplaza el carrier por el Artifact nuevo de Apply, preservando lineage.
- Final Reretester exige `StrategyArtifact.ValidateDurable()` y descarga con `DownloadDurableToCustom` usando refs exactos; no existe fallback key-only. Apply sigue resolviendo la autoridad de lectura desde Evidence y usando `FetchDurable`.
- La API física WFM recibe sólo `domain.DurableArtifactRef`; `PipelineWFMPhysical` usa `DownloadDurableToCustom` antes de escribir properties o ejecutar SQX. `ErrContractConflict` se clasifica non-retryable; errores transitorios y `ErrUnknownCommit` conservan retryabilidad existente.
- WFM valida carriers durables y conserva el Artifact del Optimizer al cambiar sólo `EvaluationRef` al aggregate. Robust selection conserva ese mismo Artifact al actualizar `DecisionRef`.

## Rationale

- `Artifact` es autoridad física y `Key` es mirror; reconstruir refs desde keys truncaría bucket, tamaño y SHA y permitiría consumir bytes equivocados.
- Los objetos sellados son inmutables: missing/size/SHA conflict no se corrige reintentando, mientras una lectura de red transitoria sí puede reintentarse. Reusar `ErrContractConflict` mantiene la taxonomía existente sin crear un sentinel nuevo.

## Consecuencias

- La cadena Builder → Retester → Optimizer → WFM → Robust Selection → Apply → Final Reretester queda ref-exacta y verificada antes de usar bytes físicos; Apply cambia la autoridad de Optimizer `O` a su nuevo output `A`.
- No hay schema, migración, tipo de dominio, cambio SDK ni modificación de write-once. MT5 portable MQ5/EX5 permanece explícitamente en Slice 2.

## Alternativas descartadas

- Mantener `DownloadToCustom(keys)` en Final Reretester o WFM: permitiría input key-only sin verificación.
- Confiar en el Artifact del carrier como autoridad de Apply: Apply debe seguir leyendo el ref exacto autorizado por Evidence.
- Crear `ApplyArtifactRef`/`WFMArtifactRef`, campos SHA planos, sentinel nuevo o persistencia adicional: duplicaría contratos ya existentes.
