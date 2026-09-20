---
type: session_summary
schema_version: 1
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[agent-project-03-app-consistent-data-backups]]"
  - "[[MinIO]]"
related:
  - "[[BACKUP-DR-KEY-RECOVERY]]"
aliases:
  - g1b minio protection 2026-09-20
confidence: verified
source_session:
share_scope: local
load_policy: manual
indexable: true
index_priority: low
tags:
  - kind/session-summary
  - scope/session
  - area/aranea
  - domain/backup-dr
---

# 2026-09-20 — G1B MinIO primera protección recuperable

## Objetivo

Mandato owner ONE-SHOT «MinIO 157 · Primera protección recuperable»: cerrar B1–B4 de `G1B-BLOCKERS.md` y dejar MinIO con copia recuperable certificada, sin interrumpir Echo y respetando ventana R2 (dom 05:55–07:15).

## Ejecución (resumen)

- Preflight RO: MinIO real = 192.168.31.92:9000 (health 200), 12 buckets un-versioned, 90.768 objetos/64,76G; Echo (140/152/153/124) y PBS sanos; hermes 16G libres → `mc mirror` descartado, streaming directo a PBS elegido.
- Canal: clave efímera con comando forzado whitelist en 157 (patrón G1A); pipeline `tar|zstd|openssl enc|split 5G` → spool datastore PBS; ingesta pxar `host/minio-{spool,SYS,BIN,CONFIG,CONFIG2}`.
- Backup: 12/12 buckets + SYS + BIN + CONFIG, todos RC=0; sqx-strategies re-streamed con sha determinista idéntico (integridad probada tras incidente de spool).
- Drill PBS 07:57–09:06: restore round-trip completo RC=0; descifrado con `r0d-g1b.key`; sha(raw tar) 12/12 OK; por objeto vs refs producción 10/12 IDENTICAL, 2/12 DIFF por escritura concurrente (sqx +8 presentes hoy con mismo sha; obsidian rotativo, point-in-time fiel).
- **Arranque aislado: MinIO RELEASE.2025-04-22 UP en 127.0.0.1:9000 con datos+creds recuperadas; mc stat autenticado OK; teardown limpio.**

## Veredicto

**OBJECT_COPY_PASS + FULL_DR_PASS.** Limitación: versioning OFF (sin historial; point-in-time 03:19–04:26 del 2026-09-20). Ver detalle completo en bitácora de [[BACKUP-DR-OWNER-PROJECT]] y change log `2026-09-20-g1b-minio-protection`.

## Teardown y estado final

- 157: authorized_keys vacío (0 bytes, auth rechazada), /tmp limpio, MinIO intacto (live 200).
- PBS: spool 45G→42M (refs/shas/logs/evidencia), 5 snapshots nuevos, `verify main` TASK OK 14/14, R2 `ct/` intacto (día 2 Finished OK 06:08).
- Claves: G1B en hermes 0600 + daedalus 0700/0600 (huella 83c4a94f… verificada); envelope retirado de hermes (entrega owner pendiente); G1A sin cambios.
- Limpieza staging G1B: autorizada por mandato §1 y ejecutada tras certificación (plaintexts nunca existieron en reposo).

## Pendiente owner

Retiro de copia owner de `r0d-g1b.key` (pedir a Hermes en sesión privada y verificar huella) — idéntico al pendiente G1A con `r0d-g1a.key`.
