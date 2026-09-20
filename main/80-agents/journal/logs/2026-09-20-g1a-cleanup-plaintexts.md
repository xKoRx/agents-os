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
  - "G1A purga plaintexts 2026-09-20"
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

# 2026-09-20-g1a-cleanup-plaintexts

%% Mandato owner ONE-SHOT: purga definitiva de los plaintext temporales G1A identificados, tras verificar custodia redundante de la clave y snapshots PBS. Cierre de la cadena G1A. %%

## Cambio

- **Tipo:** deleted (datos temporales; sin cambios canónicos de estructura)
- **Eliminado (19 archivos, ~698 MiB):**
  - `~/aranea/backup-staging/r0d-pg/r0d-20260920T004739Z.tgz` (sha 7d87839267c40d26…, byte-idéntico a la referencia in-guest)
  - `~/aranea/backup-staging/r0d-mongo/r0d-mongo.tgz` (sha 80f968cef9728f67…, ídem)
  - `/var/tmp/r0d-close.Jh1J0f/r0d-20260920T004739Z.tgz` y `/var/tmp/r0d-close.Jh1J0f/r0d-mongo.tgz` (mismos shas de referencia)
  - `/var/tmp/r0d-close.Jh1J0f/r0d-pg/20260920T004739Z/` — 13 `db-*.dump.gz` + `globals.sql.gz` (drill PG)
  - `/var/tmp/r0d-close.Jh1J0f/r0d-mongo/20260920T004810Z/all-dbs.archive.gz` (drill Mongo)
- **Actualizado:** bitácora de [[BACKUP-DR-OWNER-PROJECT]] (entrada 2026-09-20 PURGA), status del proyecto, [[BACKUP-DR-KEY-RECOVERY]] (estado de custodia → en vigor) y nota de feedback de sesión.
- **NO tocado:** claves (copia 1 hermes, copia 2 daedalus, envelope), manifiestos (`r0d-manifest.txt{,.sha}` + `SHA256SUMS`/`MANIFEST.txt` de drills), snapshots PBS `host/r0d-postgresql/2026-09-20T02:22:46Z` y `host/r0d-mongodb/2026-09-20T02:22:53Z`, ciphertexts `.enc` (staging, `/var/tmp` y PBS `close-{pg,mg}`), artefactos R2, VMs 152/153, Ceph, MinIO.

## Motivo

- Cierre G1A: la clave tiene custodia redundante certificada (2 hosts + envelope, huella 8e8e7efc…f46038 verificada pre-purga) y la recuperación desde PBS está demostrada (restore → descifrado → shas byte-idénticos → drills funcionales PASS). Los plaintexts duplicados dejaron de ser necesarios y eran la superficie residual de exposición.

## Fuentes usadas

- `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-KEY-RECOVERY.md` — huellas, shas de referencia y snapshots.
- `80-agents/journal/logs/2026-09-20-g1a-custodia-clave.md` — conjunto exacto «sin purgar (decisión owner)» que este mandato autoriza.
- Bitácora [[BACKUP-DR-OWNER-PROJECT]] — entradas G1A EXECUTED / CLOSE / CUSTODIA.
- Live: PBS 192.168.31.123 (datastore `/mnt/pbs-data`, snapshots verificados), daedalus (huella copia 2), hermes local (staging, /var/tmp, secrets).

## Resolución aplicada

- Precondiciones verificadas ANTES de borrar: (1) snapshots PBS existen con índices (`pg.pxar.didx`, `mongo.pxar.didx`); (2) huellas copia 1 = copia 2 = envelope = huella canónica; (3) cada archivo eliminado atribuido por SHA256 byte-exacto a la referencia in-guest del gate o listado 1:1 del drill.
- Borrado por ruta exacta (sin globs) sobre los 19 archivos; los `.enc` de `/var/tmp/r0d-close.Jh1J0f/` se conservaron (verificados idénticos al manifiesto).
- Búsqueda residual post-limpieza: cero plaintext G1A en `~/aranea/backup-staging/`, `/var/tmp`, `/tmp` y home de hermes.

## Validación

- Post-borrado: `sha256sum` de los 4 `.enc` conservados + manifiesto = valores del manifiesto (PG 14a1a885…, MG 27e73f53…, manifest 35130df4…).
- Staging `r0d-{pg,mongo}/` contiene solo `.enc`; `/var/tmp/r0d-close.Jh1J0f/` contiene solo `.enc` + manifiestos/logs de drills.
- Residual reportado (fuera de alcance, sin borrar): `~/.ssh/r0d_ephemeral{,.pub}` + `~/.ssh/r0d_known_hosts` (claves efímeras del traslado; grep=0 dentro de 152/153 ya demostrado en el cierre G1A) y `probe/p.txt` (6 B) en PBS — quedan para decisión owner.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, sin secretos (solo huellas públicas y rutas de hosts Aranea), sin memoria interna.

## Rollback

- Los plaintexts eliminados son REGENERABLES: restore desde PBS (`host/r0d-{postgresql,mongodb}/2026-09-20T02:22:46Z|53Z`) + descifrado con la clave documentada en [[BACKUP-DR-KEY-RECOVERY]] — procedimiento demostrado y con shas de referencia en esta nota.
- Ningún archivo canónico eliminado; las ediciones de bitácora/status/nota son revertibles por historial del vault.
