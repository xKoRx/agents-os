---
id: 2026-07-02-020
title: "OWNER-TASK — Confirmar ubicación de Secret Zero (caja fuerte + USB cifrado)"
type: action
schema_version: 1
status: todo
status_detail: "Bloqueante para ap-04 (pcloud+Restic passphrase), ap-05 (rclone crypt passphrase), step-ca backup passphrase, etc. Owner-driven physical vault setup. F-08 segregación. Sin Secret Zero no hay tier crítico cloud."
severity: high
icon: 🔒
slug: 2026-07-02-020-owner-task-secret-zero
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-02
updated: 2026-08-10
owner: me
aliases:
  - ticket 020
  - OWNER-TASK-SECRET-ZERO
  - Secret Zero
  - physical vault
tags:
  - kind/action
  - area/aranea
  - project/agents-os
  - action/owner
  - priority/critical
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[agent-project-04-cloud-critical-tier]]"
  - "[[agent-project-05-cloud-bulk-archive-tier]]"
  - "[[backup-policy]]"
---

# 2026-07-02-020 — OWNER-TASK-SECRET-ZERO

## Descripción

Confirmar la ubicación física y el mecanismo de recuperación de Secret Zero sin persistir secretos en el vault.

## Checklist

- [ ] Completar la tarea del owner y verificar los criterios de aceptación documentados.

## Contexto

Varios passphrases y API tokens del sistema de backup viven en "Secret Zero": caja fuerte + USB cifrado + (recomendado) Bitwarden para acceso cotidiano. El agente **no tiene acceso**, **no debe tener acceso**, y el patrón owner-driven es no-negociable.

Sin Secret Zero resuelto, **todos los secrets referenciados** en `inventory_2026-07-02.json → secrets_refs[]` quedan en status `pending`:

- `secret-zero` (la raíz: ubicación física)
- `pcloud-service-account` (oauth client)
- `gdrive-service-account` (oauth client)
- `restic-passphrase`
- `rclone-crypt-passphrase-salt`
- `pbs-api-token`
- `stepca-backup-passphrase`

## Tarea del owner

1. **Confirmar ubicación física de caja fuerte**: dirección/descripción suficiente para encontrar en caso de incidente fuera de horario.
2. **Confirmar USB cifrado**: que exista y esté probado (cifrado LUKS o equivalente).
3. **Definir procedimiento de acceso**: pasos para recuperar acceso a Secret Zero si bitwarden queda inaccesible (documentar en `BACKUP-DR-RUNBOOK.md §8` ya existente).
4. **Bitwarden recovery code**: 2da factorización impresa y guardada en caja fuerte, separada del USB.
5. **Validar write-back procedure**: que el agente pueda dejar nuevos secretos en Bitwarden vía approved-runbook script (no vía shell libre).

## Inputs requeridos

- Caja fuerte física.
- USB cifrado (LUKS).
- Bitwarden (cuenta owner) configurado.
- Backup de recovery code de Bitwarden impreso.

## Outputs esperados

```markdown
secret_zero_setup:
  vault_location: "ubicación física descrita"
  encrypted_usb:
    encryption: "LUKS"
    label: "aranea-secret-zero-v1"
    capacity_gb: 8
    recovery_code_bitwarden: "almacenado en vault (separado)"
  bitwarden:
    account: "owner personal"
    org: "aranea-personal"
    access_method: "password + 2fa TOTP"
  write_back_procedure: "documentado en BACKUP-DR-RUNBOOK §8"
  tested_at: "YYYY-MM-DD"
```

## Acceptance criteria

- Procedimiento de acceso testeado por owner al menos 1 vez (write/read round-trip).
- Recovery code de Bitwarden físicamente fuera de USB y de la laptop primaria.

## Bloquea

- `agent-project-04` (pcloud + Restic) — necesita passphrase del repo.
- `agent-project-05` (GDrive + rclone crypt) — necesita passphrase + salt.
- `agent-project-01` (config backup) — específicamente step-ca passphrase si se cifra con secret-zero.
- `agent-project-02` PBS setup — PBS datastore passphrase requiere guardarse en Secret Zero.

## Riesgo si no se resuelve

- Secrets viven en plaintext en filesystem (grave).
- Single point of failure si owner ausente.
- Backup crítico offline-air-gap comprometido.

## Política de manejo

- El agente **NUNCA** escribe secretos a filesystem sin encriptar, ni los logs contiene paths de key material.
- El agente **NUNCA** comunica secrets por chat (Telegram), aunque cifrado E2E.
- El owner **SIEMPRE** opera Bitwarden por UI propia o CLI aprobado.

## Referencias

- BACKUP-DR-DESIGN.md §7 (Secret Zero)
- BACKUP-DR-OWNER-PROJECT.md §"Tareas del owner"
- BACKUP-DR-RUNBOOK.md §8 (Secret Zero recovery procedure)
- agent-project-04/05 Required credentials

## Source files

- BACKUP-DR-DESIGN.md §7
- BACKUP-DR-RUNBOOK.md §8

## Captured

Ticket creado 2026-07-02 como materialización formal de OWNER-TASK-SECRET-ZERO listada en BACKUP-DR-OWNER-PROJECT.md.
