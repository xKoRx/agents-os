---
type: session_raw
schema_version: 1
created: "2026-09-20"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
source_session:
tags:
  - kind/session-raw
  - area/aranea
---

# 2026-09-20 — WP-A7 · Primer off-site recuperable (raw)

Mandato owner ONE-SHOT. Resultado: **PARTIAL** (`OFFSITE_COPY_BLOCKED / RECOVERY_CERTIFIED`).

## Secuencia real

1. Bootstrap Agents-OS (constitución, continuidad, índice, router `aranea`, preferencias). `VAULT_ROOT` verificado.
2. Autoridades leídas: ROADMAP WP-A7, tickets 020/021 (ambos `todo`), KEY-RECOVERY, bitácora G1A/G1B/MP-01, MANDATOS.
3. Estado físico: claves G1A/G1B en `~/aranea/secrets/` con huellas canónicas; sin rclone/env/configs pCloud; vault navegador vacío; 4 `.enc` config en staging MP-01.
4. Verificación de artefactos: descifrado+listing OK de r1/pve/etcd/a5 (lección: `pass file:` no expande `~`). Hallazgo: bundle PVE sin pmxcfs (run 2026-09-19 falló esa captura) → password PBS no cubierto por config backups.
5. PBS: dumps `.enc` en `~/r0d/close-{pg,mg}` con SHAs canónicos → scp a staging A7; password PBS obtenido de `/etc/pve/priv/storage/aranea-pbs.pw` (kronos sudo) y validado AUTENTICANDO contra PBS (17 snapshots). Los `.pw` que buscaron los drivers en `$HOME` de PBS ya no existen (purga G1A 19sep).
6. Paquete Secret Zero: keys G1A/G1B + pbs-backup.pw + RECOVER.md + INVENTORY.md + manifiesto; passphrase nueva `r0d-a7-recovery.pw` (custodia hermes+daedalus+envelope, huella `bbdc1054…`); contenedor final SHA `5cd8de94…51a9b` en `~/aranea/work/a7-offsite-20260920/`.
7. Payload mínimo 288 MB (6 `.enc` + MANIFEST): configs R1/etcd/PVE/A5 + dumps PG/Mongo; SHAs vs manifiestos/PBS OK.
8. pCloud: landing pública sin sesión; `getquota` 404; sin credencial en 5 fuentes → BLOQUEO registrado (mandato §2: no cambiar proveedor, no crear cuenta).
9. Drill clean-room en daedalus (`/tmp/a7-drill`, eliminado post-drill): SHA contenedor OK → apertura solo envelope+openssl → huellas internas 3/3 → descifrado pve.tgz.enc + dump PG real → SHA plaintext `7d878392…dee4` = canónico → teardown. Evidencia: `logs/cleanroom-drill-evidence.md`.
10. Vault: bitácora (entrada WP-A7 + Status), KEY-RECOVERY (sección paquete), change log `2026-09-20-a7-offsite-preparacion`. Higiene: plaintexts /tmp (hermes+daedalus) eliminados; contenedor obsoleto de /tmp purgado.

## Bloqueo

pCloud sin credencial (gates 020/021 sin decisión owner). Única acción owner: crear/autorizar acceso pCloud (OAuth opción A ticket 021) + registrar credencial en custodia → continuación = push + drill descarga.

## Fuera de alcance declarado

MinIO 64G, pool0, vzdump imagen-level, CouchDB 116 (A3 SKIP), recurrencia (todo quedó one-shot).
