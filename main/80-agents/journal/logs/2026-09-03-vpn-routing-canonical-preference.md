---
type: change_log
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
area:
project: "[[Crear Context]]"
application:
entities:
  - "[[Meli]]"
  - "[[Aranea]]"
  - "[[AGENTS OS]]"
related:
  - "[[rjara-vpn-routing-preferences]]"
  - "[[2026-09-03-vpn-routing-session-feedback]]"
  - "[[2026-09-03-vpn-routing-reindex-gate-feedback]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-03-vpn-routing-session-feedback]]"
  - "[[2026-09-03-vpn-routing-reindex-gate-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Change Log — Routing canónico de VPN

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated + conflict-resolution
- **Archivo(s):**
  - `80-agents/memory/public/user-preference/rjara-vpn-routing-preferences.md`
  - `80-agents/memory/public/user-preference/rjara-agent-profile.md`
  - `80-agents/memory/public/user-preference/rjara-meli-work-preferences.md`
  - `80-agents/memory/public/user-preference/rjara-aranea-operations-preferences.md`

## Motivo

- Un agente confundió la VPN personal Aranea con la VPN corporativa requerida para publicar en un repositorio MELI. El usuario fijó la distinción como regla durable.

## Fuentes usadas

- Corrección explícita del owner: proyectos MELI requieren GlobalProtect; repos propios y homelab requieren Aranea.

## Resolución aplicada

- Se creó una única preferencia global always-load con la matriz de decisión y se enlazó desde el perfil global y los dos perfiles scoped. No se duplicó la autoridad.

## Validación

- Schema contract validado y lint estricto dirigido ejecutado con 0 findings. El reindex de Graphify se intentó, pero quedó bloqueado por 32 findings globales ajenos; el índice anterior se conservó y la degradación quedó registrada.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** local; no contiene credenciales, endpoints ni secretos.

## Rollback

- Eliminar la preferencia nueva y retirar sus tres enlaces; reconstruir Graphify.
