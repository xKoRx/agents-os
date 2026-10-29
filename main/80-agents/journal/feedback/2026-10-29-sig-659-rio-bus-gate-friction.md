---
type: feedback
schema_version: 1
scope: session
created: 2026-10-29
updated: 2026-10-29
area: "[[Meli]]"
project: "[[SIG-659 — RIO Bus (implementación)]]"
entities:
  - "[[SIG-659 — RIO Bus (implementación)]]"
related: []
aliases: []
agent_surface: "[[Claude Code]]"
agent_model: claude-opus-5-5
agent_run: "[[2026-10-28-claude-code-claude-opus-5-5-rio-bus-review]]"
session_goal: "RIO Bus: specs, review, versión 0.0.3, PRs y gate de playmaker"
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Feedback — SIG-659 RIO Bus, gate de playmaker

## Context

- Sesión de Claude Code sobre [[SIG-659 — RIO Bus (implementación)]]: specs SIG-718, code review del trabajo de Codex, `0.0.3-rio-bus`, PR #64 y gate de playmaker.

## What Complicated The Session Most


- **Diagnóstico tardío del bloqueo del push.** Primero atribuí el fallo del gate Cleric a un endpoint remoto de Lore inexistente; la causa real (perfil local servido por `./local/test-lore.sh --gate`, que exige `local.adminml.com` → loopback en `/etc/hosts`) ya estaba en la Bitácora de Codex. Leer la Bitácora antes de diagnosticar habría ahorrado tres vueltas y la frustración del owner.
- **Comandos con placeholders.** Entregué `DOCKER_CONFIG=<config temporal> JAVA_HOME=<JDK 25>`; el owner los copió literal y zsh falló. Todo comando para el owner va con valores reales y rutas persistentes, nunca con placeholders ni rutas del scratchpad.
- **Verificación de `/etc/hosts` en bucle.** Tres pedidos de "ya agregué la línea" sin cambio en el archivo; ayudó mostrar fecha/tamaño del archivo y el hostname de la máquina.
- **Docker para el launcher de Lore.** El runner descarta `DOCKER_CONTEXT` y usa `docker context show`; con el contexto `default` apagado hace falta un `DOCKER_CONFIG` propio con `currentContext: colima-rio` y `cliPluginsExtraDirs` de Homebrew (sin eso `compose` desaparece: `unknown flag: --project-name`).

## Lo más útil

- La Bitácora del plan de agente como fuente única: permitió reconstruir qué hizo Codex (runs, decisiones D-10/D-15, el bloqueo de hosts).
- Verificar contra el wire real (`JsonUtils` de mqclient) en la revisión de código: confirmó el contrato de punta a punta.

## Falta soporte

- Spellbook pasó a specs v2 (`doc/`); la CLI global del alias seguía en 1.3.0 y rechaza `spec_v2_active`. La 2.3.0 queda en `~/.local/bin/spellbook`. La skill `spellbook.cli` y el runbook no cubren `spec pull/push`.
