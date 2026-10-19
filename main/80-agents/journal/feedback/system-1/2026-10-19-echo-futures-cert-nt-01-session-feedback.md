---
type: feedback
schema_version: 1
scope: session
created: 2026-10-19
updated: 2026-10-19
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[Codex]]"
agent_model: GLM-5.3-Flash
agent_run:
session_goal:
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

# 2026-10-19-echo-futures-cert-nt-01-session-feedback

## Observación

- **Lectura fuzzy del MCP etcd casi falsifica un control:** `etcd_get_value` devolvió «17:00» (valor de OTRA clave) para la clave de armado `futures-bridge/accounts`. El control crítico de egress se verificó bien sólo por cliente HTTP crudo (kvs vacío). Instancia nueva del gotcha ya documentado en [[aranea-etcd-mcp-fuzzy-read-gotcha]] — patrón: cualquier verificación de ABSENTE debe hacerse por cliente crudo, nunca por el MCP.
- **Sesión del MCP aranea-ssh expira en operaciones largas:** dos expiraciones (-32001) a mitad de encargo; la recuperación HTTP (initialize + bearer de `~/.zcode/cli/config.json`) quedó scriptada en `~/aranea/work/cert-nt-01-mgr/mcp_ssh_call.sh` (reutilizable; listar y llamar tools).
- **Perfiles SSH viewer de Windows inutilizables para lectura:** `dev-win` (viewer) rechaza incluso comandos seguros; todo inventario RO de .132 tuvo que pasar por `dev-win-operator`. Coste: toda lectura toca un perfil con capacidad de mutación (disciplina extra).

## Pain Pattern Candidate

- Diagnóstico de grupos Kafka: `state=EMPTY` + membresía vacía NO implica consumidores muertos (consumidores assign-based no registran miembros); la prueba de suscripción/vida es el avance de offsets. Casi cuesta un incidente FX (la variante del module lo cortó antes de detectarse); el rollback evitó el daño.
