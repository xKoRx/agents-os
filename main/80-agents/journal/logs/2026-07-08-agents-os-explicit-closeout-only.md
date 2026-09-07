---
type: change_log
scope: session
created: 2026-07-08
updated: 2026-07-08
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
  - "[[rjara-agent-profile]]"
  - "[[agents-os-session-close]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/personal
  - project/agents-os
  - change/updated
---

# AGENTS OS explicit closeout only

## Cambio

- Persistida preferencia dura del usuario: no ejecutar cierre completo de sesion
  salvo pedido explicito.
- Actualizada la constitucion para aclarar que terminar una tarea, llegar a un
  checkpoint o detectar conocimiento reusable no autoriza por si solo L0/L1/feedback.
- Actualizada `agents-os-session-close` con trigger guard.
- Corregido `80-agents/skills/INDEX.md`, que decia incorrectamente
  "**Always-run** al finalizar la tarea".
- Anotado el error historico en `agents-os-behavior-config`: "no cierres sesion"
  fue clasificado como temporal cuando debia ser preferencia estable.

## Motivo

Los agentes estaban gastando demasiado output cerrando sesiones antes de que el
usuario lo pidiera. La causa eran reglas contradictorias: cierre explicito en la
skill, pero "always-run al finalizar tarea" en el indice y proactividad/checkpoints
en la constitucion.

## Validacion

- `agents-os-session-close` ahora exige trigger explicito en el paso 0 y hard rules.
- `rjara-agent-profile` contiene una regla `[DURA]` visible en always-load.
- `agents-os.md` declara que el cierre completo corre solo por pedido explicito.
