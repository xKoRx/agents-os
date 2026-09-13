---
type: change_log
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
  - "[[aranea-ssh-mcp]]"
related:
  - "[[aranea-mcp-capability-plane]]"
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
aliases: []
confidence: verified
source_session: 2026-09-13-aranea-ssh-session-limit-incident
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Aranea SSH session-limit incident recovery

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Aranea/AGENT-PLATFORM/agentes/AGENT-PLATFORM - MCP Access Plane.md`
  - `10-projects/Echo/agentes/Echo Forge — F-04 Magic allocation, version seal and handoff.md`
  - `80-agents/journal/agent-runs/2026-09-13-codex-unknown-aranea-ssh-session-recovery.md`
  - `80-agents/journal/feedback/system-1/2026-09-13-aranea-ssh-session-limit-incident-session-feedback.md`

## Motivo

- Persistir el incidente confirmado y el estado de handoff sin convertir evidencia incompleta en root cause ni ejecutar cambios fuera del runtime `mcps`.

## Fuentes usadas

- Fuentes canónicas: `aranea-mcps-expert`, `aranea-mcp-capability-plane`, `aranea-ssh-mcp`, proyecto MCP Access Plane, `ml-ia.md` y F-04 physical resume.

## Resolución aplicada

- Se confirmó endpoint DNS/IP alcanzable, bearer presente sin revelar valor, `401` sin auth, `/health` `200 healthy=true configured=true` y `initialize` autenticado `503` con `session limit (64)`. La inspección LXC/Docker y recovery no fueron posibles: SSH administrativo rechazado y Portainer sólo expuesto detrás de login sin credencial disponible. No hubo restart, cambio de config, rotación de bearer, cambio de perfiles, uso de targets ni workflow.

## Validación

- Requests HTTP ejecutados el 2026-09-13 a las 04:21–04:26 America/Santiago; la primera falla exacta fue `HTTP/1.1 503 Service Unavailable` con `Server is at its session limit (64). Close an existing session and retry.`. Root cause: `UNKNOWN` — session registry/reaper/client-leak no observables sin autoridad server-side.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No aplica: no se mutó el runtime. Retomar con autoridad existente para LXC 113/hades; si se demuestra saturación no legítima, reiniciar únicamente `aranea-ssh` y certificar server/client/lifecycle antes de desbloquear F-04.
