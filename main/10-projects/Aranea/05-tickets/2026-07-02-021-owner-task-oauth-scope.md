---
id: 2026-07-02-021
title: "OWNER-TASK — Decidir quién ejecuta OAuth flows (pcloud + GDrive)"
type: action
schema_version: 1
status: todo
status_detail: "Bloqueante para ap-04 y ap-05. OAuth apps son credenciales sensibles. Decidir alcance del agente en OAuth flows. F-08 segregación."
severity: high
icon: 🔑
slug: 2026-07-02-021-owner-task-oauth-scope
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-02
updated: 2026-08-10
owner: me
aliases:
  - ticket 021
  - OWNER-TASK-OAUTH-SCOPE
  - OAuth
tags:
  - kind/action
  - area/aranea
  - project/agents-os
  - action/owner
  - priority/critical
related:
  - "[[agent-project-04-cloud-critical-tier]]"
  - "[[agent-project-05-cloud-bulk-archive-tier]]"
  - "[[BACKUP-DR-DESIGN]]"
---

# 2026-07-02-021 — OWNER-TASK-OAUTH-SCOPE

## Descripción

Decidir quién ejecuta los flujos OAuth de pCloud y Google Drive y con qué alcance operativo.

## Checklist

- [ ] Completar la tarea del owner y verificar los criterios de aceptación documentados.

## Contexto

`agent-project-04` (pcloud + Restic) y `agent-project-05` (GDrive + rclone crypt) requieren configurar remotes con credenciales OAuth. OAuth apps tienen scopes:
- `pcloud`: client_id + client_secret, scopes `files.read` + `files.write`.
- `Google Drive`: client_id + client_secret de OAuth 2.0 web app en Google Cloud project; scopes `drive.file` (mínimo) o `drive` (full).

El agente **podría** ejecutar el OAuth flow programáticamente, pero eso requiere que el agente tenga acceso al callback URL (localhost:port) y a secrets en runtime. Owner-driven OAuth es más seguro pero más lento.

## Tarea del owner

Decidir **quién crea y opera las OAuth apps**:

### Opción A — Agent con scope limitado (recomendado)
- Owner crea la OAuth app via consola web (pcloud / Google Cloud Console) **una vez** y guarda client_id + client_secret en Secret Zero.
- Agent ejecuta el OAuth flow programáticamente usando client credentials de Secret Zero, con scope mínimo.
- Refresh tokens se materializan en Secret Zero, no en filesystem.

### Opción B — Owner-driven completo
- Owner crea OAuth app, ejecuta OAuth flow, entrega tokens a agent vía Secret Zero.
- Agent solo lee tokens desde Secret Zero.

### Opción C — Service account OAuth (solo GDrive)
- Crear service account Google, descargar JSON key, guardar en Secret Zero.
- Agent usa directamente sin OAuth flow.
- Restricción: service account tiene su propio quota, no cuenta personal.

## Recomendación del agente

**Opción A** para pcloud (OAuth simple). **Opción C** para GDrive (más limpia y reproducible).

## Inputs requeridos

- Acceso owner a consola pcloud (cuenta personal o business).
- Acceso owner a Google Cloud Console con un proyecto activo.
- Decisión de scopes (mínimo necesario = `drive.file` para GDrive, `files.read/write` para pcloud).

## Outputs esperados

```yaml
oauth_scope_decision:
  pcloud:
    operator: "owner"             # owner-driven or agent-with-scope
    scopes: ["files.read", "files.write"]
    client_credentials_storage: "secret-zero"
  gdrive:
    method: "service-account"     # oauth-flow or service-account
    scopes: ["drive.file"]
    service_account_key_storage: "secret-zero"
```

## Acceptance criteria

- Decisión firmada por owner.
- OAuth apps creadas (si aplica) o service account JSON descargado (si aplica).
- Tokens / keys transferidos a Secret Zero físicamente.

## Bloquea

- `agent-project-04` setup paso 1 (crear cuenta-servicio o autorizar OAuth app).
- `agent-project-05` setup paso 1 (crear service account o autorizar OAuth app).

## Riesgo si no se resuelve

- Agent no puede operar remotes cloud sin credenciales.
- Backup tier crítico cloud no se ejecuta (single point of failure).

## Política de manejo

- OAuth client_secret NUNCA en filesystem plano.
- Refresh tokens NUNCA en filesystem plano.
- Scope mínimo estricto (no `drive` full si `drive.file` alcanza).

## Referencias

- BACKUP-DR-OWNER-PROJECT.md §"Tareas del owner"
- BACKUP-DR-DESIGN.md §3 (F-08), §5 (Cloud tier)
- agent-project-04 / agent-project-05

## Source files

- agent-project-04-cloud-critical-tier.md
- agent-project-05-cloud-bulk-archive-tier.md

## Captured

Ticket creado 2026-07-02 como materialización formal de OWNER-TASK-OAUTH-SCOPE listada en BACKUP-DR-OWNER-PROJECT.md.
