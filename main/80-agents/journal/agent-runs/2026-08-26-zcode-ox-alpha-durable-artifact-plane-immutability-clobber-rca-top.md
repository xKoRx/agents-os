---
type: agent_run
schema_version: 1
scope: session
created: "2026-08-26"
updated: "2026-08-26"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: ox-alpha
model_source: host_reported
task_type: debugging
task_complexity: high
outcome: pass
verification: verified_read_only
evaluator: agent
user_rework: unknown
source_session: DURABLE-ARTIFACT-PLANE-IMMUTABILITY-CLOBBER-RCA-TOP
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-08-26-zcode-ox-alpha-durable-artifact-plane-immutability-clobber-rca-top

## Trabajo

- **Objetivo:** RCA READ-ONLY del clobber del artifact plane sobre `symphony` @ `1bb5fdb`: demostrar que un retry puede sobrescribir en MinIO una ObjectKey referenciada por una Evaluation immutable, clasificar todas las superficies, evaluar opciones de inmutabilidad (write-once/content-addressed/versioned/staging) y fijar orden respecto al recovery del Retester, sin implementar código.
- **Alcance atribuible a esta combinación superficie×modelo:** demostración mecánica del clobber (pipeline order, PutObject incondicional, ausencia de conditional write/versioning/VersionID), inventario completo de 20 terminales PutObject con clasificación por superficie, análisis de capacidades condicionales de minio-go v7.0.95, confirmación de la semántica immutable Mongo, challenge al premise del RCA anterior, decisión WRITE_ONCE + REQUIRED digest-on-read y redacción de checkpoint/handoff.
- **Artefactos afectados:** Sólo notas Agents OS (checkpoint append-only, agent-run, change_log, continuidad interna, feedback). Cero cambios en el repo o datos.

## Evidencia

- **Validaciones ejecutadas:** Tres trazas de repositorio read-only paralelas (scouts) contra HEAD verificado `1bb5fdb…` + intento de verificación física read-only del objeto (list MinIO por tamaño 56662/56664) que falló por credenciales `.env` stale (Access Key rechazada) — sin mc/mongosh y con logs rotados, la re-verificación física directa quedó imposible esta sesión.
- **Resultado observable:** CAN_RETRY_OVERWRITE_SEALED_ARTIFACT=YES (upload_results precede a db_register en builder.go:26-47/project_activity.go:217-244; UploadFromDiskExact minio_storage.go:305 y UploadArtifactFromPath artifact_store.go:146 son PutObject incondicional bajo BuildMinIOPath/DeriveArtifactKey sin digest); CAN_DOWNSTREAM_DETECT_MISMATCH_BEFORE_USE=NO en cadena .sqx (DownloadToCustom/DownloadObjectToPath/DownloadArtifactToPath sin size/sha; validación existente sólo en FetchDurable payload_store.go:76-102, DownloadNDJSON trade_lists.go:145-198 y ReconcileApplySelectedRun); OVERWRITE_POSSIBLE Builder/Retester/Optimizer/FinalReretester + MT5 compile/backtest; IMMUTABLE_SAFE Apply/MT5-exporter-mq5/TradeList-durable/WFM; Mongo CONTRACT_CONFLICT CORRECT (insert-only, ResolveImmutableWrite persistence.go:498-521); PREFERRED=WRITE_ONCE (patrón payload_store.go:43-70), schema SUFFICIENT sin VersionID, MUST_FIX_BEFORE_RETESTER_RECOVERY=YES.
- **Limitaciones de la evidencia:** bytes actuales del objeto contaminado no re-verificados físicamente en esta sesión (veredicto YES apoyado en el hallazgo físico sellado del RCA previo y en la inevitabilidad por orden de pipeline); soporte real de conditional PUT en el server MinIO desplegado no verificable desde el repo (capacidad confirmada sólo en lib v7.0.95).

## Evaluación

%% Scores opcionales 1–5: agregar al frontmatter sólo cuando exista evidencia suficiente. Si son autoevaluados, conservar evaluator: agent. %%

- **Correctness:**
- **Autonomy:**
- **Efficiency:**
- **Tool use:**
- **Overall:**

## Resultado

- **Outcome:** PASS; SEALED_ARTIFACTREF_PHYSICALLY_TRUSTWORTHY=NO; DURABLE_ARTIFACTREF_SCHEMA_SUFFICIENT=YES; DURABLE_DOWNLOAD_DIGEST_VERIFICATION=REQUIRED (parcialmente presente vía FetchDurable); RETESTER_TEST_RUN_PHYSICALLY_CONTAMINATED=YES; MONGO_IMMUTABLE_BEHAVIOR=CORRECT; MUST_FIX_BEFORE_RETESTER_RECOVERY=YES; RECOMMENDED_FIX=write-once guard compartido en las dos superficies sin guardia + puerto aditivo de download verificado; FILE BUDGET ~8; NEXT EXACT DURABLE-ARTIFACT-PLANE-IMMUTABILITY-CORRECTION-NORMAL, luego DURABLE-RETESTER-RESUMABILITY-CORRECTION-NORMAL.
- **Rework posterior:** unknown.
- **Aprendizaje para comparar herramientas:** a diferencia de la sesión anterior (feedback scout-subagent-timeouts), tres scouts read-only paralelos con contratos acotados completaron sin timeouts (~2.6M/7.2M/0.7M tokens); la fricción de esta sesión fue operacional (observabilidad runtime efímera), no de herramientas agénticas.
