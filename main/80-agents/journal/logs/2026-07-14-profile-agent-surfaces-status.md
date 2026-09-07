---
type: change_log
scope: user
created: 2026-07-14
updated: 2026-07-14
project: "[[AGENTS OS]]"
entities: []
related: []
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
  - scope/user
  - project/agentsos
  - change/updated
---

# Estado local de superficies AGENTS OS

## Cambio

- Se registró que la instalación personal está activa y que Codex y Claude Code
  cargan las reglas repo-scoped y descubren las skills canónicas.
- Se dejó higiene semanal como cadencia operativa y la automatización pendiente
  de confirmar día y hora.

## Motivo

- Evitar que un perfil legado sin `installation_status` vuelva a disparar el
  onboarding en cada turno.

## Validación

- Forward-tests efímeros de Codex y Claude Code confirmaron reglas y discovery
  de bootstrap, instalación e higiene.

## Compartibilidad

- **Scope:** local

## Rollback

- Eliminar únicamente la sección de instalación/superficies del perfil.

## Corrección posterior

- La validación de discovery de esta corrida usó adapters generados. Fue
  superseded por `2026-07-14-canonical-skill-location-correction.md`; la carga
  canónica sin copias queda pendiente.
