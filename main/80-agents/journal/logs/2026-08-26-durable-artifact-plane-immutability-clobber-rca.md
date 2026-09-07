---
type: change_log
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
confidence: verified
source_session: DURABLE-ARTIFACT-PLANE-IMMUTABILITY-CLOBBER-RCA-TOP
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-26-durable-artifact-plane-immutability-clobber-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` checkpoint append-only DURABLE-ARTIFACT-PLANE-IMMUTABILITY-CLOBBER-RCA-TOP.
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` delta de continuidad.
  - `80-agents/journal/agent-runs/2026-08-26-zcode-ox-alpha-durable-artifact-plane-immutability-clobber-rca-top.md` creado.
  - `80-agents/journal/feedback/system-1/2026-08-26-symphony-artifact-plane-runtime-observability-session-feedback.md` creado.

## Motivo

- Cerrar el RCA read-only del defecto descubierto en DURABLE-RETESTER-RESUMABILITY-RCA-TOP: un retry físico puede sobrescribir en MinIO una ObjectKey ya referenciada por una Evaluation immutable; auditar clobber, alcance por superficie, opciones de inmutabilidad y orden respecto al recovery del Retester, sin implementar código.

## Fuentes usadas

- `symphony` @ `1bb5fdb470ae3d833c98d96c3100e6b09c938345` (HEAD == origin/master): pipeline (`sqx/activities/worker/pipeline/builder.go`, `project_activity.go`), steps (`steps/steps.go`), storage MinIO (`sqx/adapters/storage-minio/{minio_storage,artifact_store,payload_store,durable_artifacts,apply_selected_run,trade_lists}.go`), dominio (`sqx/core/domain/{paths,persistence_contracts,artifact_paths,trade_list_paths}.go`), Mongo (`sqx/adapters/metadata-mongo/evidence_store.go`, `sqx/core/capabilities/persistence.go`), SDK (`~/go/src/github.com/xKoRx/sdk/pkg/shared/minio/client.go`) y minio-go v7.0.95 (`api-put-object.go`).
- Evidencia sellada previa: checkpoint DURABLE-RETESTER-RESUMABILITY-RCA-TOP (drift físico 56664/sha256:2f64… bajo key sellada 56662/sha256:5a54…).

## Resolución aplicada

- ROOT CAUSE: el artifact plane MinIO carece de enforcement de inmutabilidad — PutObject incondicional bajo keys lógicas sin digest, upload_results antes del evidence commit, sin conditional write/versioning y downloads por key sin verificación ⇒ CAN_RETRY_OVERWRITE_SEALED_ARTIFACT=YES y drift indetectable en la cadena .sqx.
- CHALLENGE al premise «refs selladas = autoridad única; drift físico como limitación conocida» RECHAZADO: sin write-once ni digest-on-read la ref sellada no es autoridad sino metadata no enforcement; IS_SEALED_ARTIFACTREF_CURRENTLY_PHYSICALLY_TRUSTWORTHY=NO.
- PREFERRED_STORAGE_SEMANTIC=WRITE_ONCE vía patrón existente `PutPayload` extendido a `UploadFromDiskExact` y `UploadArtifactFromPath`; DURABLE_ARTIFACTREF_SCHEMA_SUFFICIENT=YES sin VersionID; digest verification REQUIRED en downloads durables; MONGO_IMMUTABLE_BEHAVIOR=CORRECT; MUST_FIX_BEFORE_RETESTER_RECOVERY=YES; NEXT EXACT DURABLE-ARTIFACT-PLANE-IMMUTABILITY-CORRECTION-NORMAL.

## Validación

- Tres trazas read-only paralelas (scouts) con file:line sobre baseline exacto; inventario exhaustivo de write-paths (20 terminales PutObject clasificados); verificación física directa del objeto hoy IMPOSIBLE (credenciales `.env` stale rechazadas por el server, sin mc/mongosh, logs rotados sin telemetría del run) ⇒ veredicto de contaminación apoyado en hallazgo físico sellado de la sesión anterior más inevitabilidad por orden de pipeline; cero cambios de código o datos.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Notas append-only; revertir = eliminar las notas creadas y el bullet de continuidad añadido.
