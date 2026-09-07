---
type: change_log
scope: session
created: 2026-08-01
updated: 2026-08-01
area: "[[Echo Forge]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Symphony]]"
  - "[[echo-forge]]"
related:
  - "[[deployer-manifest-publication-race]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-01-symphony-release-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - app/echo-forge
  - change/created
---

# Symphony — corrección de publicación de manifest

## Cambio

- **Tipo:** created
- **Archivo(s):** [[deployer-manifest-publication-race]]; `deploy_release.sh`, `deploy_sqx.sh` y `deployer/watcher` en Symphony.

## Motivo

- Un release podía quedar sin activación remota fiable porque el manifest no se publicaba como señal final y el orquestador dependía de `rg` dentro de screen.

## Fuentes usadas

- Ejecución real del release `0.2.21`, log del deployer y tests del módulo watcher.

## Resolución aplicada

- El watcher publica/confirma el manifest después de los artefactos, reintenta fallos y el script espera la confirmación portable antes de enviar el flujo.

## Validación

- Confirmación de manifest en MinIO y workflow iniciado para `0.2.21`.
- Suite focalizada de Go y validación sintáctica de Bash aprobadas.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir los cambios de Symphony y volver a una versión previa del manifest sólo mediante un release nuevo; no sobrescribir carpetas de release existentes.
