---
type: change_log
scope: user
created: 2026-07-15
updated: 2026-07-15
share_scope: local
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[sync-local-branch]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/user
  - project/agentsos
  - change/updated
---

# Artefactos locales no trackeados durante sincronización Git

## Cambio

- Se corrigió `sync-local-branch` para que los artefactos locales no trackeados de configuración, agentes y Graphify no bloqueen por defecto una sincronización en repos Meli.
- Se mantuvo el bloqueo para cambios trackeados, archivos no trackeados funcionales y colisiones de rutas que puedan sobrescribir contenido de las ramas.

## Motivo

- Evitar bloquear merges por carpetas operativas que no participan en la funcionalidad del código.

## Validación

- La skill y el perfil always-load quedaron alineados con la nueva clasificación.
- Los artefactos permitidos deben permanecer sin staging y fuera del commit/push.
