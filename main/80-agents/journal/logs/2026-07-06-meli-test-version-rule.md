---
type: change_log
scope: user_profile
created: 2026-07-06
updated: 2026-07-06
entities:
  - "[[AGENTS OS]]"
  - "[[Meli]]"
related:
  - "[[rjara-agent-profile]]"
confidence: verified
indexable: false
tags:
  - agent/log
  - area/meli
  - kind/change-log
---

# Change Log — Meli Test Version Rule

## Motivo

El usuario corrigió una falla operativa: para cambios en apps/repos de Meli no se deben usar versiones productivas en pruebas, integraciones o PRs no mergeados.

## Cambio

- Se agregó una directiva `[DURA]` al perfil del usuario: en apps/repos de Meli, nunca setear versiones productivas para pruebas o PRs no mergeados; usar siempre versiones de test explícitas con formato `0.0.x-<descripcion>` y alinear consumidores contra esa versión.

## Validación

- Regla incorporada en `80-agents/memory/public/user-preference/rjara-agent-profile.md`.
