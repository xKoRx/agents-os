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
  - "[[BACKUP-DR-CONTRACT]]"
aliases:
  - "G1A ejecución primera copia PG/Mongo 2026-09-20"
confidence: high
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

# 2026-09-20-g1a-execution

%% Ejecución G1A (primera copia PG/Mongo + drills) autorizada por owner («OK G2» + «OK G1A» con SHA256 6f8497ce… verificado pre-inicio). Cambios documentales G2 aplicados con diff exacto y hashes baseline verificados (7dd35985… / 6eac7bf5…). %%

## Cambio

- **Tipo:** infra-mutation (autorizada, alcance G1A) + documentation
- **Archivos tocados:**
  - `BACKUP-DR-OWNER-PROJECT.md` — diff línea Status (PROPUESTO → registro de ejecución posterior en bitácora), 2 entradas bitácora (2026-09-19 gate, 2026-09-20 ejecución).
  - `agent-project-03-….md` — status_detail actualizado (R3 re-scoped, diff aprobado).
  - `80-agents/journal/logs/2026-09-20-g1a-execution.md` — este log.
- **Mutaciones de infra (todas revertibles, en alcance autorizado):**
  - 152/153: run-dirs `/root/r0d-pg|r0d-mongo` (conservados como rollback), clave efímera instalada y REVOCADA con verify (grep=0), tgz trasladados eliminados.
  - hermes: staging `~/aranea/backup-staging/r0d-*/` (tgz + .enc + manifiesto — plaintext PENDIENTE de purga hasta recibo de claves por el owner), `~/aranea/secrets/r0d-g1a.key` + `.owner-envelope` (0600), keypair `~/.ssh/r0d_ephemeral`, `r0d_known_hosts` (ed25519 pineado).
  - PBS .123: snapshots `host/r0d-postgresql/2026-09-20T02:22:46Z`, `host/r0d-mongodb/2026-09-20T02:22:53Z`, `host/r0d-probe` (220B, test de auth — a eliminar por owner o en R3), dir `/home/ariadna/r0d` (mnt con blobs .enc), confirmación de huella del proxy cert persistida.
- **NO tocado:** R2 (timer, driver, ct/155, datastore cfg), Ceph, zvols, MinIO 157, tickets 018/020, diseño congelado, contratos.

## Resultado

- Drills: PG 13/13 bases + pg_isready + SELECTs funcionales (sqx.strategies 9090, dashboard_version 44, hdb_metadata 1, echo_mcp EMPTY_OK legítimo) — PASS. Mongo: mongod aislado :27018, mongorestore 55.968 docs 0 fallos, índices únicos, find() forge PASS.
- Round-trip PBS→disco con sha256 idéntico al manifiesto en ambos .enc — PASS. verify main TASK OK (chunks 429→500). R2 ct/155 intacto.
- Plaintext staging: NO purgado (condición 2 del owner: recibo de claves fuera de Hermes pendiente). Purga diferida a confirmación del owner.

## Defectos corregidos durante ejecución (documentados en bitácora)

1. `/root` 0700 bloqueaba a usuarios de servicio en drills → `/var/tmp`.
2. initdb crea rol `postgres` → globals sin ON_ERROR_STOP + conteo de roles como control (10/10).
3. `set -e` + `grep -c` sin match mata el script (asignación) → `|| true`.
4. Quoting de authorized_keys vía guest-exec corrompía `command="…"` → línea generada localmente, subida por base64 (bytes exactos).
5. PBS client 4.2.5: sin `pbundle1`/`--driver`/`--fingerprint` → pxar estándar + confirmación interactiva de huella (persistida).
6. Repository exige auth-id completo del token (`backup@pbs!aranea@…`) — ACL DatastoreBackup en `/datastore/main`.
7. Host-key negotiation: pinear solo ed25519 + `HostKeyAlgorithms=ssh-ed25519`.

## Pendientes (owner)

- Recibo de claves (`r0d-g1a.key.owner-envelope`) por canal fuera de Hermes → habilita purga de plaintext en staging.
- Eliminar snapshot probe `host/r0d-probe` (o decidir retención en R3).
- Retención: 30 días mínimo, sin prune automático.
