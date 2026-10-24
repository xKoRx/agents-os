---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo Futures — Runtime Pools]]", "[[EF-PROD-GOD-03-IMPLEMENTATION-PLAN]]", "[[EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE]]", "[[EF-PROD-GOD-05-MANAGER-ADJUDICATION]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-24"
updated: "2026-10-24"
---



## Propósito

Compatibilidad de estado/datos/schemas y prueba de recuperación (autoridad de restauración y rollback) del candidato fd5612f5, según GOD-02 §3–§7 y GOD-03 §7. Documento de evidencia; la aplicación física queda en G-ENV/G-REC.

## Contenido

Matriz old/new reader-writer por tipo de estado, recovery-proof source-level y condiciones de rollback.

# EF-PROD-GLM-01 — STATE-COMPATIBILITY y RECOVERY-PROOF (resumen de compatibilidad y recuperación)

Corte `fd5612f5`. Detalle normativo: GOD-02 §3–§6; contratos congelados en `v3/sdk/futures/recovery/` (schema `recovery.v1`, marker `owner-continuity.v1`, policy de compatibilidad `strict-v1`).

## Matriz old/new reader-writer

| Estado | Escritor nuevo | Lector nuevo | Lector/writer viejo (pre-ac0621a1 behaviour) | Migración |
|---|---|---|---|---|
| StateFun owners | ValueSpec aditivo `continuity` (JSON OwnerContinuity) por owner; ValueSpecs económicos intactos | marker ausente en RECOVER con key rostered ⇒ StateMissingInRecoveryError (fail-closed intencional); BIRTH sólo por tabla de config versionada | Compose() directa (harness/drivers) sin recovery config ⇒ sin exigencia (M07/strict-v1) | Restaurar checkpoint pre-delta en modo RECOVER ⇒ rostered keys sin marker fallan cerrado: la migración real exige bootstrap autorizado o restore bajo RECOVER con marker inicializado por el control path; jamás allowNonRestoredState |
| Recovery plane | ETCD `futures/recovery/{active_manifest,lineages/<id>,bootstrap_token}` (CAS) | registry ausente ⇒ UNKNOWN (ErrLineageUnknown), RETIRED terminal | pins legacy `futures/recovery/{prior_run,runtime_continuity}` siguen leyéndose: sin registro/manifest ⇒ COLD_RECOVERY_REQUIRED (antes pasaban con pins coincidentes: regresión intencional documentada) | Sin datos: el arranque exige control path; sin borra de pins |
| Permits (F06) | Writer canónico `runtimecontrol.PermitStore` envelope `{schema_version,epoch,permit}` + `futures/execution/permit_epoch/<lineage>` | Ambos lectores último-salto (bridge permit + fxpermit) parsean envelope primero con fallback plano legacy epoch 0; store_epoch > permit_epoch ⇒ PERMIT_REVOKED_BY_EPOCH | Formato plano de W2 sigue legible (compat de lectura) | Nueva config ETCD requerida: `futures-bridge/accounts/<id>/{terminal-identity,scope}`, `bridge/runtime/*` — ausente ⇒ fail-closed (expansión cerrada) |
| NTX wire | Campo aditivo `runtime_generation` en CommandData (omitheader viejo lo ignora) | GenerationGuard AddOn: gen 0 legacy pasa; gen menor persistida ⇒ GENERATION_BEHIND | Frames viejos sin campo siguen operando | Ninguna (wire compatible) |
| Feed storage (F05) | OB2 (CRC-32, Flush(true), replace atómico con .bak) | Lector dual OB1/OB2; tail roto ⇒ GAP declarado, nunca truncado | OB1 legacy se lee; conversión con checksum y rename atómico, original preservado | Conversión en ventana de despliegue; cursor jamás por delante del dato |
| FEFB wire (F04) | Stamps aditivos `lane_id/source_epoch/stream_data_seq/previous_stream_data_seq` por frame/item | Con stamps ⇒ cursor C-SEQ-1; sin stamps ⇒ LEGACY_DEGRADED (ventana 4096, sin nueva exposición con horizonte); mezcla con cursor establecido ⇒ CURSOR_REQUIRED | Frames legacy parsean byte-idéntico | El horizonte sólo activa con AddOn estampador desplegado (G-ENV/G-FEED) |
| PG contabilidad (F08) | Migración aditiva `081_futures_account_authority` (DDL nuevo, sin alterar existentes) + outbox transaccional | Provider con RevisionAuthority: nil ⇒ legacy byte-a-byte | Esquemas 061–075 intactos | Sin aplicar a ninguna BD real; aplicación por flujo de release |
| M2/journalfs | Observations store append-only con checksum en segmentos separados de intents; fence propaga fsync | PENDING/QUARANTINE jamás GC; PUBLISHED compacta con tombstone | journals/segments existentes intactos | Sin truncar journals; drain de pending antes de readiness |
| FX consumer | Grupo estable `echo-bridge-session-<env>-<acct>-<binding>` + ReadCommitted + OffsetOldest | — | Grupo viejo por hostname: cambio de grupo exige barrera con M2 conciliado (documentado; jamás desde head) | Ventana de despliegue coordinada con egress exactly-once (los comandos FX dejan de ser visibles para consumidores no-committed: el despliegue de ambos es atómico por ambiente) |

## Recovery-proof (autoridad de restauración, capa source)

- Único submitter: `runtimecontrol.Submitter.PlanStart` — RESTORE exige registry ACTIVE/INITIALIZED + manifest validado + `CheckManifestCompatibility` (generación estrictamente mayor) + objetos de checkpoint con digest verificado vía ObjectStore; BOOTSTRAP exige token single-use CAS ligado a roster+config digest; en ambos casos idempotencia por (lineage,generation) con CAS y consulta del JobID esperado ante resultado incierto. Fresh-submit sin autoridad: imposible por construcción (T1–T7 de B1).
- Watchdog: GenerationGuard pollea el JobID atestado (default 5s); divergencia ⇒ estado BLOCKED `RUNTIME_JOB_CHANGED` + `BumpEpoch` que revoca todos los permits vivos con visibilidad ≤TTL (1s) en el último salto (verificado por W6/D1 fix).
- Attestation: `RestoreAttestation` deriva de lectura post-restore (nonce de operación, JobID real, checkpoint id/digest, roster de markers realmente observados, offsets restaurados) y `CheckAgainstManifest` rechaza checkpoint/job/offsets divergentes; PENDING bloquea permits; CLEAN los habilita.
- Estado ausente previamente existente ⇒ BLOCKED (StateMissingInRecoveryError); no se fabrican pins, no se escogen checkpoints por nombre/timestamp (M01).

## Rollback

Binario anterior + snapshot compatible = válido antes de efectos; después de efectos ⇒ forward repair o MANAGE_ONLY (GOD-02 §5). Generation no retrocede; `CheckManifestCompatibility` rechaza generación ≤ instalada. Los procedimientos operativos completos quedan en el plan de instalación/rollback para G-ENV (no ejecutados aquí).
