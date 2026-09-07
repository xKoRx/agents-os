---
type: change_log
scope: project
created: 2026-07-14
updated: 2026-07-14
project: "[[AGENTS OS]]"
entities:
  - "[[agents-os]]"
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/project
  - project/agentsos
  - change/updated
---

# Port de mejoras compartibles a AGENTS OS personal

## Cambio

- Se incorporaron onboarding multisuperficie, prompt maestro, configuración de
  Codex/Claude, ciclo periódico de higiene, Kaizen incremental y trazabilidad
  de mejoras compartibles.
- La constitución se movió a `80-agents/agents-os/agent-constitution.md` y se
  corrigieron las referencias operativas.
- Se preservaron perfil personal, memoria interna, sesiones y estado histórico
  del proyecto.

## Motivo

- Mantener alineado el sistema personal con el scaffolding que usará el equipo
  sin importar datos ni estado de otras instalaciones.

## Fuentes usadas

- Distribución limpia de AGENTS OS y decisiones confirmadas por el usuario.

## Resolución aplicada

- Port selectivo de contratos reutilizables; overlays personales intactos.

## Validación

- Sintaxis de scripts y contrato de skills aprobados.
- Instalación project/global simulada en entorno temporal aprobada.
- Codex y Claude Code cargaron las reglas y encontraron bootstrap, instalación
  e higiene en forward-tests efímeros.
- Graphify se reindexó después de mover la constitución; validación final del
  grafo registrada en la misma corrida.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir por archivo usando este log como inventario; restaurar la ruta
  anterior de constitución solo junto con todas sus referencias.
