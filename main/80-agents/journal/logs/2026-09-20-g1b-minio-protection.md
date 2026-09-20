---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[agent-project-03-app-consistent-data-backups]]"
related:
  - "[[BACKUP-DR-KEY-RECOVERY]]"
aliases:
  - "G1B ejecución primera protección MinIO 2026-09-20"
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/aranea
---

# 2026-09-20-g1b-minio-protection

%% Ejecución G1B (mandato ONE-SHOT owner: «MinIO 157 · Primera protección recuperable»). Cierre de bloqueantes B1–B4 y primera copia recuperable de MinIO con drill funcional aislado. Evidencia completa: ~/aranea/work/weekend-gate-01-20260919/RUN-G1B.md + raw-g1b/. %%

## Cambio

- **Tipo:** infra-mutation (autorizada por el mandato G1B) + documentation
- **Alcance ejecutado:** primera protección recuperable de MinIO (VM 157, endpoint 192.168.31.92:9000) — export cfg/IAM/metadata B1/B2/B3 + backup per-bucket de los 12 buckets (90.768 objetos, 64,76 GB lógicos) + SYS (.minio.sys) + BIN (binarios exactos del guest) + drill funcional aislado en PBS con arranque real de MinIO.
- **Método:** stream `tar|zstd|openssl enc (AES-256-CBC/PBKDF2 600k)|split 5G` por SSH con comando forzado whitelist (patrón G1A) → spool directo en PBS datastore → ingesta pxar `host/minio-*` → restore round-trip → descifrado → verificación sha por bucket (vs stream-<b>.sha) y por objeto (vs refs de producción). `mc mirror` descartado por capacidad medida (sqx-strategies 25G > 16G libres hermes; pico > 39G daedalus).
- **Archivo(s):**
  - `BACKUP-DR-OWNER-PROJECT.md` — entradas de bitácora (G1B).
  - `agent-project-03-app-consistent-data-backups.md` — status_detail (MinIO protegido).
  - `BACKUP-DR-KEY-RECOVERY.md` — sección clave `r0d-g1b.key` (huella, copias, cifras).
  - este change_log.
- **Mutaciones de infra (todas revertibles, en alcance):**
  - 157: authorized_keys efímera (instalada 03:22, REVOCADA con verify: archivo 0 bytes, auth rechazada, estado pre-G1B); /tmp sin residuos.
  - hermes: `~/aranea/secrets/r0d-g1b.key` (0600) + keypair `~/.ssh/g1b_ephemeral` (conservado como rollback; su parte pública sin efecto tras revocación); `raw-g1b/` con evidencia.
  - daedalus: `/home/hermes-ops/.aranea-secrets/r0d-g1b.key` (0700/0600, huella verificada).
  - PBS: snapshots `host/minio-spool/2026-09-20T07:58:56Z`, `host/minio-SYS/2026-09-20T10:19:53Z`, `host/minio-BIN/2026-09-20T10:19:54Z`, `host/minio-CONFIG/2026-09-20T10:17:11Z`, `host/minio-CONFIG2/2026-09-20T10:19:56Z`; dir `/mnt/pbs-data/r0d-minio-spool` (42M: refs, stream shas, DRILL logs, DRILL-EVIDENCE). Spool de partes cifradas (45G) eliminado tras certificación (regenerable desde snapshots).
- **NO tocado:** R2 piloto (timers/driver/`ct/`), Ceph, zvols, buckets/config de producción MinIO, tickets 018/020, diseño congelado, contratos, SQX/MT4. Sin prune ni forget sobre nada preexistente.

## Motivo

- Mandato owner ONE-SHOT: cerrar B1–B4 (G1B-BLOCKERS) y obtener la primera protección recuperable de MinIO sin interrumpir Echo.

## Fuentes usadas

- `G1B-BLOCKERS.md`, `GATE-G1A-v3.md`, custodia `custodia-claves-backup-g1a`, assessment storage/Ceph 19-09, `BACKUP-DR-KEY-RECOVERY.md`.

## Resolución aplicada

- B1 metadatos: export por bucket (versioning/anonymous/ilm/events/tags/encrypt/quota/retention) + listing JSON gz + verificación por objeto en drill.
- B2 config: unit systemd completa (credenciales root sólo dentro del cifrado) + `mc admin config get` + dependencias de arranque; SYS `.minio.sys` incluido.
- B3 credenciales: clave nueva `r0d-g1b.key` (huella `83c4a94f…`), custodia Hermes+Daedalus certificada; creds root viajan cifradas en CONFIG2/SYS.
- B4 restore aislado: MinIO binario exacto del guest, bind 127.0.0.1 en PBS, arrancó y sirvió S3 autenticado sobre datos restaurados.
- Veredicto: **OBJECT_COPY_PASS + FULL_DR_PASS (config/metadata incluidas)**; 10/12 buckets byte-idénticos, 2/12 DIFF exclusivamente por escritura concurrente (sqx-strategies +8 verificados presentes hoy en producción con mismo sha; obsidian-backups bucket rotativo, restore fiel a su point-in-time 04:17). Limitación registrada: versioning OFF → sin historial (copia = estado point-in-time 03:19–04:26).

## Validación

- `verify main` post-G1B: TASK OK (14/14 grupos); R2 `ct/` intacto; timers R2 vivos (r2-measure día 2 Finished OK 06:08).
- Custodia G1B: huella verificada en copia 1 y copia 2 al crearse; envelope retirado de hermes tras certificación.
- Teardown 157: authorized_keys 0 bytes/600, /tmp limpio, auth efímera rechazada (prueba negativa real).
- Echo: 140/152/153/124 running + PG isready OK antes/durante/después; MinIO live 200 al cierre.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de vault relativos, memoria interna ni secretos (huellas permitidas).

## Rollback

- Clave efímera: ya revocada (0 bytes; auth rechazada). Keypair local `~/.ssh/g1b_ephemeral` eliminable sin efecto.
- Snapshots `host/minio-*`: `proxmox-backup-client forget` SOLO de esos backup-ids (jamás `ct/` ni `r0d-*`), + `rm -rf /mnt/pbs-data/r0d-minio-spool`.
- Copias de clave: borrar `~/aranea/secrets/r0d-g1b.key` y `hermes-ops@daedalus:~/.aranea-secrets/r0d-g1b.key` (requiere decisión owner — pierde la capacidad de descifrar las copias MinIO).
