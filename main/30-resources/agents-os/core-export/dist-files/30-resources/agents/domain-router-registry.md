---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related: []
aliases:
  - domain router registry
  - registro de routers de dominio
tags:
  - kind/doc
  - tech/agents-os
  - action/domain-routing
created: "2026-09-14"
updated: "2026-09-14"
---

# Domain Router Registry

## Propósito

Registrar opcionalmente routers de dominio sin introducir nombres, políticas o
herramientas de dominio en el core de AGENTS OS.

## Contenido

| Domain | Areas | Router | Evidence markers |
|---|---|---|---|

Cero filas significa DEFAULT sin router. Un match carga exactamente un router;
más de un match falla cerrado. La evidencia debe pertenecer a la tarea: la mera
disponibilidad ambiental de una herramienta no activa un dominio.

## Fuentes

- `80-agents/skills/agents-os-bootstrap/SKILL.md` — consumidor ejecutable.
