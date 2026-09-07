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
source_session: DURABLE-ARTIFACT-PLANE-WRITE-ONCE-ATOMICITY-DESIGN-TOP
source_feedbacks:
  - "[[2026-08-26-zcode-subagent-final-report-loss-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-26-durable-artifact-plane-write-once-atomicity-design

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` checkpoint append-only DURABLE-ARTIFACT-PLANE-WRITE-ONCE-ATOMICITY-DESIGN-TOP.
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` delta de continuidad.
  - `80-agents/journal/agent-runs/2026-08-26-zcode-glm-5.3-durable-artifact-plane-write-once-atomicity-design-top.md` creado.
  - `80-agents/journal/feedback/system-1/2026-08-26-zcode-subagent-final-report-loss-session-feedback.md` creado.

## Motivo

- Cerrar el único gap de diseño pendiente antes de implementar la corrección de inmutabilidad del artifact plane: garantizar WRITE-ONE atómico para una ObjectKey durable bajo concurrencia real entre workers/procesos/hosts. El RCA anterior propuso check-then-put y trató el conditional PUT como hardening opcional; esta sesión demuestra que ese perfil no resuelve CONCURRENT_WRITE_ONCE y congela la primitive definitiva, sin implementar código.

## Fuentes usadas

- `symphony` @ `1bb5fdb470ae3d833c98d96c3100e6b09c938345` (paquete `sqx/adapters/storage-minio/` completo: payload_store, minio_storage, artifact_store, durable_artifacts, apply_selected_run, trade_lists y tests).
- `sdk` @ `2e5fa11fe9ccd628a075e00fc4b30fe1b60be486` (`pkg/shared/minio/client.go`, `domain.go`, go.mod → minio-go v7.0.95) y fuente minio-go v7.0.95 en module cache (api-put-object, api-error-response, s3-error, object-lock/retention, bucket-versioning).
- Docs oficiales: MinIO S3 API compatibility (conditional writes), AWS S3 conditional writes, discusión minio#20318 (releases antiguas ignoran `If-None-Match:*` en PUT).
- Checkpoint previo DURABLE-ARTIFACT-PLANE-IMMUTABILITY-CLOBBER-RCA-TOP en la nota del proyecto.

## Resolución aplicada

- CHALLENGE aceptado contra la implementación propuesta por el RCA: check-then-put tiene TOCTOU (dos Stat→missing→Put ⇒ last-writer-wins ⇒ PUTPAYLOAD_CONCURRENT_WRITE_ONCE=FAIL) y releases antiguas de MinIO ignoran el header silenciosamente ⇒ conditional create pasa a ser MECANISMO PRIMARIO con capability probe fail-closed, no hardening.
- Diseño congelado: OPTION A conditional create-if-absent single-PUT `If-None-Match:*` (DisableMultipart) + read-compare exacto (ClassifyExistingArtifact/VerifyArtifactStream) + UNKNOWN_COMMIT read/verify/retry no-destructivo; primitive única compartida (`write_once.go` p.ej. PutExactIfAbsent) sobre método aditivo del SDK (`PutObjectIfAbsent` + 412 terminal); migración de UploadFromDiskExact (pre-hash+rewind, F6), UploadArtifactFromPath y PutPayload a la misma primitive; VERIFIED_READ_RULE: poseedor de DurableArtifactRef ⇒ exact read obligatorio, legacy key queda legacy; secuencia gate server → SDK → primitive+probe+harness MinIO real → superficies → PutPayload → verified reads → race tests → E2E → Retester EXACT_RECOVERY.

## Validación

- Sesión read-only total (cero cambios en repos o datos); evidencia con file:line de dos scouts paralelos contra los HEADs verificados, fuente exacta de minio-go v7.0.95 en module cache y docs oficiales; race semantics same-bytes/different-bytes/UNKNOWN_COMMIT resueltas por diseño del primitive; soporte del server desplegado declarado NO asumible y cubierto por probe runtime (creds stale impiden verificación directa).

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Notas append-only; revertir = eliminar las notas creadas, el checkpoint añadido y el bullet de continuidad.
