---
type: user_preference
schema_version: 1
scope: area
created: 2026-07-27
updated: 2026-09-03
area: "[[Aranea]]"
entities:
  - "[[Aranea]]"
related:
  - "[[rjara-agent-profile]]"
  - "[[rjara-vpn-routing-preferences]]"
confidence: verified
load_policy: when_area_loaded
indexable: true
index_priority: high
tags:
  - area/aranea
  - kind/user-preference
  - scope/area
---

# rjara — Preferencias de operaciones Aranea

## Preferencias de interacción

- Hereda las preferencias de interacción del perfil global [[rjara-agent-profile]].

## Preferencias de trabajo

- La VPN aplicable a recursos propios y del homelab se resuelve en [[rjara-vpn-routing-preferences]].
- En hosts remotos, transferir el archivo a local de forma segura, modificarlo
  localmente, validarlo y devolverlo si corresponde.
- No editar archivos de forma interactiva en el host remoto.
- No persistir credenciales, endpoints sensibles ni dumps operativos en el
  vault; usar referencias seguras.
