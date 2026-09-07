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
  - "[[2026-08-28-durable-artifact-verified-reads-slice1b]]"
  - "[[2026-08-27-durable-artifact-verified-reads-rca]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-SLICE2-MT5-NORMAL
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

# 2026-08-28-durable-artifact-verified-reads-slice2

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Slice 2 de `xKoRx/symphony` cierra la frontera portable MT5 sobre baseline `ce21d253680fa925d4c9d33e25b39fc0b94519f4`, con write-once y verified reads previos certificados y congelados.
- El riesgo era truncar el `DurableArtifactRef` en MQ5 y volver a ejecutar con `SourceKey` sin autoridad física en compile/backtest.

## Decisión

- `ArtifactTaskRequest.SourceArtifact` es la autoridad física aditiva; `SourceKey` se conserva como mirror y debe ser exactamente `SourceArtifact.ObjectKey` en contexto durable.
- `ArtifactTaskResult.PrimaryDurable` es obligatorio junto a `Primary` en éxitos durables y ambos deben coincidir en key, tamaño y SHA-256; `Primary` queda como shape legacy/evidence.
- `ExportMT5EAResult.Artifact` devuelve el mismo ref exacto usado por `PutPayload`; el carrier transiciona MQ5 → EX5 → HTM reemplazando el Artifact anterior y preservando lineage.
- Compile y backtest comparten un boundary que valida el contrato, usa `FetchDurableToPath` sin fallback key-only en durable, verifica el archivo antes de ejecutar y clasifica `ErrContractConflict` como non-retryable.

## Rationale

- Todos los inputs durables productivos del boundary portable siguen `DurableArtifactRef exacto → descarga física verificada → ejecución`; listing y key-only permanecen sólo para legacy explícito.
- No se modificaron SDK, schema, migraciones, storage-minio, primitive write-once, tipo de dominio nuevo ni sentinel de error. El siguiente y único paso de implementación es la certificación E2E final.

## Consecuencias

- Mantener `ArtifactRef` como presentación/evidence y agregar autoridad durable sólo en boundaries de ejecución evita una migración amplia y mantiene compatibilidad legacy.
- No derivar bucket, tamaño o SHA desde `SourceKey`, ni convertir el carrier en sustituto de la autoridad Evidence del exporter.

## Alternativas descartadas

- Migrar todo `ArtifactRef` a una nueva jerarquía de tipos, tocar schema/SDK o reabrir la primitive write-once: habría ampliado el blast radius sin aportar autoridad adicional.
- Mantener descargas key-only o usar listing como autoridad durable: permitiría ejecutar bytes no verificados y rompería el cierre del boundary portable.
