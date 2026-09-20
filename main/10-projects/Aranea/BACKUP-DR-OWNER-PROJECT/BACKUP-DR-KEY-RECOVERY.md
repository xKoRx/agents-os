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

Ambas copias verificadas con la misma huella el 2026-09-20. Copia al owner mediante el archivo `r0d-g1a.key.owner-envelope` (0600, byte-idéntico a la clave, misma huella), entregable por cualquier canal privado del owner; verificado idéntico a la copia 1.

## Cómo ve o copia el owner la clave (ruta real, probada)

Desde cualquier máquina con SSH a hermes (VM 118), como su usuario:

```bash
# 1. Ver la huella (verificación sin exponer la clave)
ssh <usuario>@hermes 'sha256sum ~/aranea/secrets/r0d-g1a.key'
#    → debe imprimir 8e8e7efc40910ed7cebf48ea98574df4c50ed7071a298b2849eca7f3e6f46038

# 2. Copiar la clave a su equipo (por scp; la clave nunca pasa por chat ni logs)
scp <usuario>@hermes:aranea/secrets/r0d-g1a.key ~/Escritorio/r0d-g1a.key
sha256sum ~/Escritorio/r0d-g1a.key   # verificar huella localmente
```

Alternativa equivalente: copia 2 en daedalus (`scp <usuario>@daedalus:.aranea-secrets/r0d-g1a.key …`). El archivo sobrante `r0d-g1a.key.owner-envelope` en `~/aranea/secrets/` es byte-idéntico a la clave y sirve como entregable directo del owner.

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

## Fuentes

- `80-agents/journal/logs/2026-09-20-g1a-custodia-clave.md` — change log de esta operación de custodia.
- Bitácora de [[BACKUP-DR-OWNER-PROJECT]] — entrada 2026-09-20 (custodia de clave + demo de recuperación).
- `~/aranea/work/custody-key-20260920/` (hermes) — evidencia de la demo (logs de restore, shas, limpieza).
- `~/aranea/work/weekend-gate-01-20260919/GATE-G1A-v3.md` — diseño G1A y decisiones de cifrado (§ tabla Cifrado, § owner).
- `80-agents/journal/logs/2026-09-20-g1a-execution.md` — ejecución original G1A y cierre-certificación.
