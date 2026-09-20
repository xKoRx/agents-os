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
  - "[[BACKUP-DR-KEY-RECOVERY]]"
related:
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
  - "[[ROADMAP-WP-BACKUP-DR]]"
aliases:
  - "WP-A7 off-site 2026-09-20"
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

# 2026-09-20-a7-offsite-preparacion

%% Mandato owner ONE-SHOT: primer off-site recuperable (WP-A7). Sin gestores de secretos nuevos, sin repetir research, sin cambiar proveedor. Resultado: PARTIAL — Secret Zero y demo clean-room PASS, subida pCloud bloqueada sin credencial (gates 020/021). %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT.md` — entrada de bitácora 2026-09-20 (WP-A7) y una línea en Status.
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-KEY-RECOVERY.md` — sección "Paquete de recuperación off-site (WP-A7)": SHA del contenedor, passphrase de apertura y custodia, contenido, demo clean-room y pendiente off-site.
  - Este change log (creado con contrato `change_log`).

## Mutaciones de infra (en alcance del mandato, revertibles)

- Paquete cifrado `r0d-a7-recovery-pkg.tgz.enc` (3.824 B) + payload off-site (6 `.enc`, 288 MB, SHAs verificados vs manifiestos) en `~/aranea/work/a7-offsite-20260920/` (0700; payload 0600). Ningún plaintext nuevo en reposo fuera de los ya custodiados.
- Passphrase nueva `r0d-a7-recovery.pw` (32 B, `openssl rand -base64 24`): copias hermes `~/aranea/secrets/` + daedalus `/home/hermes-ops/.aranea-secrets/` (0700/0600, pipe SSH, huella idéntica `bbdc1054…230b4`) + envelope owner `~/aranea/secrets/r0d-a7-recovery.pw.owner-envelope`.
- `secrets/pbs-backup.pw` (password token `backup@pbs!aranea`) leído de `/etc/pve/priv/storage/aranea-pbs.pw` (kronos, sudo existente) → verificado AUTENTICANDO contra PBS con él (17 snapshots listados); incluido cifrado en el paquete. Cero secretos en Markdown/chat/logs (huellas y SHAs públicos solamente).
- Drill clean-room en daedalus `/tmp/a7-drill`: SHA contenedor OK → apertura con passphrase → huellas internas OK → descifrado de `pve.tgz.enc` y del dump PG real (SHA plaintext `7d878392…dee4` = canónico) → directorio de drill eliminado.
- Read-only: dumps `.enc` descargados de PBS `~/r0d/close-{pg,mg}` (SHAs canónicos), snapshots listados, listing de bundles config.

## NO tocado

- Claves y backups existentes (byte-idénticos), PBS datastore y retención (sin prune/forget), Ceph/TrueNAS/R2/pool2, timers R1/R2/R3, tickets 018-021 (status intacto), diseño F-01..F-14. Sin scrub, sin migraciones, sin borrado de claves. pCloud: sin cuenta creada ni OAuth iniciado (sin autorización 020/021).

## Motivo

- WP-A7 (roadmap): 3ª copia fuera del homelab con operación obligatoria de escrow de claves r0d. Bloqueo de destino: pCloud sin credencial en 5 fuentes verificadas (vault navegador, rclone, env, filesystem, sesión viva); el mandato prohíbe cambiar de proveedor o crear cuentas sin gates 020/021.

## Fuentes usadas

- ROADMAP WP-A7, tickets 020/021, [[BACKUP-DR-KEY-RECOVERY]], bitácora del proyecto (G1A/G1B/MP-01), `~/aranea/bin/mp01-a1-dumps.sh` (patrón cifrado), `~/aranea/work/weekend-gate-01-20260919/g1a-exec.log` (SHAs plaintext).

## Resolución aplicada

- Secret Zero como paquete cifrado autodescriptivo (Agents-OS catálogo; passphrase = única llave, custodia owner+hermes+daedalus), demo de apertura en host independiente sin dependencias de Aranea, payload mínimo útil preparado para un solo push cuando exista destino.

## Validación

- SHAs de los 6 payload contra manifiestos y referencias canónicas: OK. Demo clean-room PASS completa en daedalus (evidencia en transcripción de sesión; directorio temporal eliminado). Autenticación PBS con la credencial empaquetada: OK. Verificación post-drill de custodia G1A/G1B en hermes: huellas canónicas intactas.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos (solo huellas/SHAs públicos y hosts ya documentados en el proyecto).

## Rollback

- Eliminar `~/aranea/work/a7-offsite-20260920/`, `~/aranea/secrets/r0d-a7-recovery.pw{,.owner-envelope}` y `/home/hermes-ops/.aranea-secrets/r0d-a7-recovery.pw`; revertir las tres notas (borrar sección/entrada). Nada más: ninguna mutación productiva.
