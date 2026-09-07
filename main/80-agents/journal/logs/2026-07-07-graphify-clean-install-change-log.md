---
type: change_log
scope: session
created: "2026-07-07"
updated: "2026-07-07"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application: "[[Graphify]]"
entities:
  - "[[Graphify]]"
  - "[[AGENTS OS]]"
related: []
aliases: []
confidence: verified
source_session: "571245b7-25e7-4875-a593-e99ce03ea480"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-07-07 - Graphify Clean Install Change Log

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `/usr/local/bin/graphify-personal`
  - `/usr/local/bin/graphify-obsidian`
  - `/Users/rodrigojara/obsidian/SecondBrain/main/.graphifyignore`

## Motivo

- Habilitar el uso de Graphify en el host local de forma segura y aislada (evitando colisión con proyectos del trabajo del usuario y previniendo errores de permisos en sandbox mediante redirección de cachés).

## Fuentes usadas

- [[graphify-contract]]
- [[30-resources/tools/graphify.md]]

## Resolución aplicada

- Instalación de la biblioteca `graphifyy` a nivel del sistema y provisión de scripts de envoltura robustos que manejan caches de forma local y envían logs de forma aislada.

## Validación

- Ejecución exitosa de `graphify-obsidian update`, `graphify-personal update` (en `/Users/rodrigojara/go/src/github.com/xKoRx/echo`), y queries correspondientes verificando los logs resultantes en `~/.config/`.
