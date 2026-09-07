---
type: change_log
scope: session
created: 2026-08-09
updated: 2026-08-09
area: "[[Echo]]"
project: "[[Stager - Symphony Publisher Integration]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Stager - Symphony Publisher Integration]]"
  - "[[stager-app]]"
related:
  - "[[2026-08-09-stager-publisher-f0-sdd-complete]]"
aliases: []
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
  - area/echo
  - project/stager-symphony-publisher-integration
---

# Stager publisher F1 release local complete

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Stager - Symphony Publisher Integration.md`
  - repo `xKoRx/symphony` → `deploy_sqx.sh`

## Motivo

- El owner autorizó G0 y el desarrollo de F1: crear una release local completa
  para Linux y Windows sin promover estados parciales.

## Resolución aplicada

- El staging único ahora contiene `linux-amd64` y `windows-amd64`.
- Se conservan los cuatro artefactos Linux y se agrega
  `sqx-mt5-worker.exe` compilado para Windows.
- Antes del único `mv` final se comprueba que los cinco archivos sean regulares
  y no vacíos; cualquier fallo limpia el staging mediante el trap existente.

## Validación

- `bash -n deploy_sqx.sh` y `git diff --check` PASS.
- Una release temporal produjo los cinco artefactos esperados; se retiró al
  terminar la comprobación.
- Un fallo Windows simulado no promovió la versión objetivo ni dejó staging.
- No se modificó el cambio ajeno `deployer_screen.log`.

## Rollback

- Revertir únicamente `deploy_sqx.sh` y devolver F1 a pendiente; no borrar
  releases productivas ni modificar el manifest, MinIO o el Bash legacy.
