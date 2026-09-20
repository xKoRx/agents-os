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
  - "[[BACKUP-DR-CONTRACT]]"
aliases:
  - "G1A custodia clave 2026-09-20"
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

# 2026-09-20-g1a-custodia-clave

%% Mandato owner ONE-SHOT: custodia definitiva de la clave G1A (r0d-g1a.key). Reutilizar mecanismos existentes, segunda copia en otro host, nota privada en Agents-OS, demo de recuperación sin Hermes, cero secretos en Markdown. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-KEY-RECOVERY.md` — **creada** (materializada con contrato `doc`): ubicaciones de copias, identificador/huella de la clave y backups asociados, procedimiento de acceso owner, procedimiento de recuperación si desaparece Hermes, evidencia. Sin secretos (verificado por grep exacto del material y del secreto PBS).
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT.md` — entrada de bitácora 2026-09-20 (custodia + demo) y enlace en Fuentes de la nota nueva.
- **Mutaciones de infra (revertibles, en alcance del mandato):**
  - daedalus: creado `/home/hermes-ops/.aranea-secrets/` (0700) con `r0d-g1a.key` (0600, propietario `hermes-ops`) — copia 2 de la clave, transporte por pipe SSH (sin intermediarios en claro), huella verificada idéntica (8e8e7efc…f46038).
  - `~/aranea/work/custody-key-20260920/` (hermes, 0700) — evidencia de la demo.
  - `~/.hermes/profiles/ariadna/skills/devops/…/custodia-claves-backup-g1a/` — skill procedural para futuras claves.
- **NO tocado:** claves, backups ni plaintext existentes (nada borrado; staging, `/var/tmp/r0d-close.*`, `close-{pg,mg}` y `probe` intactos); R2 (timers/piloto/datastore), Ceph, producción, tickets; copia 1 en `~/aranea/secrets/` quedó byte-idéntica (verificado post-demo).

## Motivo

- Owner no administrará archivos de claves manualmente; la clave de cifrado G1A vivía solo en Hermes (riesgo de pérdida única). Pendiente owner previo (retiro de clave) se resuelve con segunda copia host + ruta de acceso documentada.

## Fuentes usadas

- `~/aranea/work/weekend-gate-01-20260919/GATE-G1A-v3.md` + `g1a-driver.sh` (cadena de cifrado, repository, manifiestos).
- `80-agents/journal/logs/2026-09-20-g1a-execution.md` (estado G1A al cierre, pendiente owner).
- PBS live 192.168.31.123 (snapshots `host/r0d-postgresql/2026-09-20T02:22:46Z`, `host/r0d-mongodb/2026-09-20T02:22:53Z`) y PVE 192.168.31.90 (lectura del secreto del token, sin exponerlo).

## Resolución aplicada

- **Copia 2:** transporte `cat clave | ssh daedalus-ops 'cat > ~/.aranea-secrets/r0d-g1a.key'` con `chmod 700` dir / `600` archivo; verificación `sha256sum` remota = huella esperada.
- **Demo de recuperación (PASS):** (1) clave+envelope de Hermes stash a work dir → `secrets/` sin material; (2) restore de `host/r0d-postgresql` desde PBS a `r0d/custody-demo` en PBS — sha `.enc` idénticos al manifiesto (PG 14a1a885…, MG 27e73f53…); (3) ciphertexts por stream SSH PBS→daedalus; (4) descifrado en daedalus con SOLO la copia 2 (`openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 -pass file:…`) — sha plaintext byte-idénticos a los originales in-guest del gate (PG 7d87839267c40d26…, MG 80f968cef9728f67…); (5) limpieza de demo en daedalus y PBS, restauración del stash con verificación de huella y permisos 0600.
- **Nota canónica** sin secretos + **skill** procedural reutilizable.

## Validación

- Nota: grep exacto del contenido de la clave y del secreto PBS = 0 matches en vault y evidencia; huella de verificación presente (2 menciones).
- Demo: shas vistos arriba; evidence `~/aranea/work/custody-key-20260920/daedalus-demo-evidence.txt` + `recovery-demo/restore-pbs.log` (sin secretos: grep = 0).
- Estado final: copia 1 hermes 0600 huella 8e8e7efc… ✓; copia 2 daedalus 0700/0600 misma huella ✓; directorios PBS `close-{pg,mg}`/`mnt`/`probe` intactos ✓.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de vault, memoria interna ni secretos (solo rutas de hosts Aranea y huellas públicas).

## Rollback

- Copia 2: `ssh daedalus-ops 'rm -rf ~/.aranea-secrets'` (la copia 1 permanece).
- Nota: `rm 10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-KEY-RECOVERY.md` + revertir entrada de bitácora del proyecto.
- Work dir: `rm -rf ~/aranea/work/custody-key-20260920`.
- La demo no dejó estado persistente (dirs temporales ya eliminados en daedalus y PBS).
