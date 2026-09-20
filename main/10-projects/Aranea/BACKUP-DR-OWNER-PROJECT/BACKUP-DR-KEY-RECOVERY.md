---
type: doc
schema_version: 1
status: active
icon: 🔑
slug: backup-dr-key-recovery
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[agent-project-03-app-consistent-data-backups]]"
aliases:
  - Custodia clave G1A
  - Backup DR key recovery
  - Recuperación de claves Backup/DR
confidence: high
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - security/secrets
created: "2026-09-20"
updated: "2026-09-20"
---

# 🔑 Backup/DR — Recuperación de claves (G1A)

> [!warning] Regla de esta nota
> Esta nota NO contiene secretos (regla constitucional §9): solo ubicaciones, huellas de verificación y procedimientos exactos. La huella de verificación es el SHA256 **de la clave** (permitido; no permite reconstruir la clave).

## Propósito

Custodia y recuperación de la clave de cifrado de los backups G1A de PostgreSQL (VM 152) y MongoDB (VM 153). Dos copias privadas en hosts de confianza con permisos restrictivos, huella de verificación, ruta de acceso para el owner y procedimiento de recuperación completa si Hermes desaparece. Sin gestor externo ni infraestructura nueva; la custodia la opera Hermes/Ariadna con segunda copia independiente en otro host (mandato owner 2026-09-20).

## Identificador de la clave y backups asociados

- **Clave:** `r0d-g1a.key` — 32 bytes hex (65 chars con `\n`), generada con `openssl rand -hex 32`.
- **Huella de verificación (SHA256 de la clave):** `8e8e7efc40910ed7cebf48ea98574df4c50ed7071a298b2849eca7f3e6f46038`.
- **Cifra:** `openssl enc -aes-256-cbc -pbkdf2 -iter 600000 -salt` (descifrado con `-d` y `-pass file:<clave>`).
- **Backups que descifra:** snapshots PBS `host/r0d-postgresql/2026-09-20T02:22:46Z` y `host/r0d-mongodb/2026-09-20T02:22:53Z` (datastore `main` de PBS 192.168.31.123, VM 180). Cada snapshot contiene el dump comprimido cifrado (`.enc`) + manifiesto con los SHA256 de los `.enc`.
- **SHAs de referencia de los ciphertexts:** PG `14a1a8856afabcf8…` · Mongo `27e73f5356d2388b…` (completos en el manifiesto dentro de cada snapshot y en el staging de Hermes).
- **SHAs de los plaintexts** (para validar tras descifrar): PG tgz `7d87839267c40d26…` · Mongo tgz `80f968cef9728f67…`.

## Ubicaciones de las copias

| Copia | Host | Ruta | Permisos |
|---|---|---|---|
| 1 | hermes (VM 118), usuario `hermes` | `~/aranea/secrets/r0d-g1a.key` | dir `~/aranea/secrets/` 0700, archivo 0600 |
| 2 | daedalus (desarrollo), usuario `hermes-ops` | `/home/hermes-ops/.aranea-secrets/r0d-g1a.key` | dir 0700, archivo 0600 (grupo/others: sin acceso) |

Ambas copias verificadas con la misma huella el 2026-09-20. Copia al owner mediante el archivo `r0d-g1a.key.owner-envelope` (0600, byte-idéntico a la clave, misma huella), entregable por cualquier canal privado del owner; verificado idéntico a la copia 1. **2026-09-20 (purga G1A):** con esta custodia en vigor se purgaron los plaintexts temporales (staging + `/var/tmp/r0d-close.*`, 19 archivos); los ciphertexts `.enc`, manifiestos y snapshots PBS se conservan — los plaintexts son regenerables mediante el procedimiento de recuperación de esta nota (demostrado).

## Cómo ve o copia el owner la clave (ruta real, documentada)

El owner no tiene cuenta local en hermes/daedalus (no se crean cuentas para esto). Ruta de acceso real, por orden de fricción:

1. **Pedirla a Hermes en una sesión** (`cat ~/aranea/secrets/r0d-g1a.key`): entrega directa en chat privado; la huella debe calzar con `8e8e7efc…f46038`. Es la ruta prevista por el mandato (la custodia la opera el agente).
2. **Por SSH a hermes** desde su equipo (si dispone de acceso): `ssh <usuario>@hermes 'cat ~/aranea/secrets/r0d-g1a.key' > r0d-g1a.key && sha256sum r0d-g1a.key` — la clave nunca pasa por chat ni logs, solo por su terminal.
3. **Archivo entregable ya existente:** `~/aranea/secrets/r0d-g1a.key.owner-envelope` (0600, byte-idéntico a la clave, misma huella), pensado para retiro por canal privado del owner.
4. **Copia 2 alternativa:** `hermes-ops@daedalus:/home/hermes-ops/.aranea-secrets/r0d-g1a.key` (0700/0600; solo el usuario `hermes-ops` puede leerla — aislamiento POSIX verificado; `kor` u otros usuarios de daedalus no tienen acceso).

## Recuperación si desaparece Hermes

Con Hermes fuera, la copia 2 (daedalus) + PBS son suficientes. Procedimiento validado el 2026-09-20 con la clave de Hermes escondida (demo real):

```bash
# 1. En daedalus: restore del snapshot PBS y verificación de ciphertexts
ssh -i <key> ariadna@192.168.31.123   # PBS; key de Ariadna en hermes ~/.ssh/ariadna_pbs
cd /home/ariadna/r0d && rm -rf recovery && mkdir recovery
PBS_PASSWORD='<secreto de backup@pbs!aranea>' proxmox-backup-client restore \
  'host/r0d-postgresql/2026-09-20T02:22:46Z' pg.pxar recovery/ \
  --repository backup@pbs!aranea@192.168.31.123:main --allow-existing-dirs
# (ídem host/r0d-mongodb/2026-09-20T02:22:53Z con mongo.pxar)

# 2. Ciphertext hacia daedalus y descifrado con la copia local de la clave
cat /home/ariadna/r0d/recovery/r0d-*.tgz.enc | ssh daedalus 'cat > ~/rec.tgz.enc'
openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 -in ~/rec.tgz.enc \
  -out ~/rec.tgz -pass file:$HOME/.aranea-secrets/r0d-g1a.key
sha256sum ~/rec.tgz   # PG: 7d87839267c40d26… · Mongo: 80f968cef9728f67…
```

Resultado esperado: `sha256sum` del tgz descifrado = los SHAs de referencia de arriba; el tgz es el dump íntegro (PG: globals + 13 bases; Mongo: archive mongodump), listo para los drills documentados en `~/aranea/work/weekend-gate-01-20260919/restore-{pg,mongo}-drill.sh`. La recuperación de los secretos de acceso PBS (`backup@pbs!aranea`, SSH) está cubierta por R2/infra (secreto del token en `/etc/pve/priv/storage/aranea-pbs.pw` en el nodo PVE; llaves SSH de Ariadna en `~/.ssh/` de hermes).

## Evidencia de la recuperación demostrada (2026-09-20)

Cadena ejecutada con la clave local de Hermes **fuera de su ubicación** (stash temporal): restore desde PBS → SHA de ambos `.enc` idénticos al manifiesto → descifrado **en daedalus usando solo la copia 2** → SHAs de plaintext byte-idénticos a los originales in-guest del 2026-09-20 (PG `7d87839267c40d26…`, Mongo `80f968cef9728f67…`) → artefactos temporales eliminados y estado original restaurado (huella verificada post-restauración). PASS. Bitácora y change log en las Fuentes.

## Clave G1B — `r0d-g1b.key` (MinIO, 2026-09-20)

- **Clave:** `r0d-g1b.key` — 32 bytes hex (65 chars con `\n`), generada con `openssl rand -hex 32`. Cifra los backups G1B de MinIO 157.
- **Huella de verificación:** `83c4a94fc62ec05280da6344380cdebe0833567414fb82778fc6d415ecb99d71`.
- **Cifra:** idéntica a G1A: `openssl enc -aes-256-cbc -pbkdf2 -iter 600000 -salt` (los streams además van comprimidos zstd ANTES de cifrar; descifrar = `openssl enc -d … | zstd -dc`).
- **Backups que descifra:** snapshots PBS `host/minio-spool/2026-09-20T07:58:56Z` (12 buckets + CONFIG en partes `*_<tag>.part-*.enc`), `host/minio-SYS/2026-09-20T10:19:53Z` (`.minio.sys`), `host/minio-BIN/2026-09-20T10:19:54Z` (binarios), `host/minio-CONFIG2/2026-09-20T10:19:56Z` (cfg/IAM/metadata). Dentro del spool snapshot, cada stream tiene su SHA de referencia en `stream-<tag>.sha` (sha del tar en claro) y los refs por objeto en `refs-<bucket>.txt`.
- **Ubicaciones:** copia 1 hermes `~/aranea/secrets/r0d-g1b.key` (0700/0600) · copia 2 daedalus `/home/hermes-ops/.aranea-secrets/r0d-g1b.key` (0700/0600). Envelope entregable al owner: pedir a Hermes en sesión privada y verificar huella (la copia local del envelope fue retirada tras la certificación del drill).
- **Recuperación demostrada:** drill G1B (2026-09-20) descifró y verificó TODOS los streams con esta clave y arrancó un MinIO aislado con las credenciales recuperadas del export.

## Paquete de recuperación off-site (WP-A7, 2026-09-20)

Preparado por mandato WP-A7 (Secret Zero sin servicios nuevos). El paquete reúne las claves de esta nota + G1B + la credencial PBS, cifrado con una passphrase independiente:

- **Contenedor:** `r0d-a7-recovery-pkg.tgz.enc` (hermes `~/aranea/work/a7-offsite-20260920/`). **SHA256:** `5cd8de942d865a3c2acaee20ca2b7133899f095835138660afbc24094e951a9b`.
- **Passphrase de apertura:** `r0d-a7-recovery.pw` — NO está dentro del paquete. Copias: hermes `~/aranea/secrets/` y daedalus `/home/hermes-ops/.aranea-secrets/` (0700/0600, huella `bbdc10544d07fe5663fe6d69869d7d87e930339486e915411a717f81427230b4`) + envelope owner `~/aranea/secrets/r0d-a7-recovery.pw.owner-envelope` (retirable por canal privado).
- **Contenido:** `keys/r0d-g1a.key` + `keys/r0d-g1b.key` + `secrets/pbs-backup.pw` (password del token `backup@pbs!aranea`; huella `4a6f3755…abc0a`; verificado autenticando contra PBS) + `RECOVER.md` (procedimiento clean-room: requisitos, verificación, apertura, casos PBS/off-site) + `INVENTORY.md` (artefactos protegidos con SHAs).
- **Demo clean-room (2026-09-20, PASS):** en daedalus, con solo el envelope owner + openssl: SHA del contenedor OK → apertura OK → huellas internas OK → descifrado de `pve.tgz.enc` y del dump PG real → SHA plaintext PG `7d878392…dee4` = referencia canónica. Sin usar copias operativas de claves.
- **Pendiente (bloqueo registrado):** subir el paquete + payload (6 `.enc`, 288 MB, manifiesto `MANIFEST-A7-PAYLOAD.sha256`) a pCloud — bloqueado por gates 020/021 sin credencial. Hasta entonces el paquete no tiene copia fuera de Aranea.

## Fuentes

- `80-agents/journal/logs/2026-09-20-g1a-custodia-clave.md` — change log de esta operación de custodia.
- Bitácora de [[BACKUP-DR-OWNER-PROJECT]] — entrada 2026-09-20 (custodia de clave + demo de recuperación).
- `~/aranea/work/custody-key-20260920/` (hermes) — evidencia de la demo (logs de restore, shas, limpieza).
- `~/aranea/work/weekend-gate-01-20260919/GATE-G1A-v3.md` — diseño G1A y decisiones de cifrado (§ tabla Cifrado, § owner).
- `80-agents/journal/logs/2026-09-20-g1a-execution.md` — ejecución original G1A y cierre-certificación.
