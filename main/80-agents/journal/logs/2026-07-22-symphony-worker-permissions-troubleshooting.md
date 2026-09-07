---
type: change_log
scope: session
created: 2026-07-22
updated: 2026-07-22
area: "[[Personal]]"
project: "[[Symphony]]"
entities:
  - "[[Symphony]]"
related:
  - "[[2026-07-22-symphony-worker-permissions-summary]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-07-22-symphony-worker-permissions-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/symphony
---

# Symphony Worker Troubleshooting — Permisos de Input

## Cambio

- **Tipo:** updated
- **Archivo:** `.agents/skills/worker-troubleshooting/SKILL.md`
- **Versión:** `1.0.0` → `1.1.0`

## Motivo

- Hera y Kronos ejecutaban el worker desde el release inmutable y no podían crear la ruta relativa `input/`.

## Fuentes usadas

- Código de `apply_selected_run`.
- Unidades systemd, cwd efectivos y logs de Zeus, Hera y Kronos.

## Resolución aplicada

- Se agregó el caso de diagnóstico y remediación a la skill, incluyendo validación por hash, cwd y escritura.
- Se homologaron las unidades de Hera y Kronos con Zeus.

## Validación

- Las tres unidades tienen el mismo SHA-256.
- Los tres servicios están activos en `0.1.130`, cwd `/var/lib/symphony` y prueba de escritura exitosa.
- Temporal ejecutó el intento 9 de `apply_selected_run` sin repetir el error y el workflow avanzó a actividades `mt5_exporter`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** no se copiaron credenciales a este changelog.

## Rollback

- Cada host conserva un backup timestamped de su unidad previa en `/etc/systemd/system/`; restaurarlo, ejecutar `daemon-reload` y reiniciar el servicio.
