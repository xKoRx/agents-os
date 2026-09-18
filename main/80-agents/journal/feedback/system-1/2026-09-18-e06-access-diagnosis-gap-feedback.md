---
type: feedback
schema_version: 1
scope: session
created: 2026-09-18
updated: 2026-09-18
area: "[[Personal]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
entities:
  - "[[Echo]]"
  - "[[Aranea]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
related:
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-mcp-capability-plane]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (zai-individual-coding-plan/GLM-5.3-Flash)
agent_run: "[[2026-09-18-zcode-glm-5.3-flash-e06-t21-prereq-access-restored]]"
session_goal: "Corregir el diagnóstico erróneo de acceso a mt5-kronos/MetaEditor y avanzar el prerrequisito físico de T21."
source_session: 2026-09-18-e06-t21-prereq-access-restored
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

# Session Feedback - 2026-09-18 - E06 access diagnosis gap

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3-Flash
- Agent run: [[2026-09-18-zcode-glm-5.3-flash-e06-t21-prereq-access-restored]]
- Session goal: corrección documental de acceso + prerrequisito físico T21.
- Main entity: [[Echo — E-06 Reference Enrollment and Binding]] / [[AGENT-PLATFORM - MCP Access Plane]]
- Skills used: agents-os-bootstrap, aranea-agent-dev, aranea-mcps-expert, aranea-ssh-mcp, aranea-mcp-plane-operator, hermes-agent-operator, agents-os-session-close.
- Retrieval mode: runbooks canónicos + estado vivo del plano (smoke MCP con bearer por stdin).

## Fricción observada

- **Diagnóstico de acceso por analogía en lugar de por el plano:** dos sesiones (T09b C2 y Forge R2) declararon «sin capability MCP del host Windows» / «falta terminal con MetaEditor» a partir de un Permission denied de SSH directo con una key temporal revocada, sin ejecutar el diagnóstico del capability plane (`/status` + initialize + `tools/list`). La capacidad existía, estaba certificada en el runbook y costó una corrección del Manager más una sesión de re-discovery. La lección operativa ya quedó errateada en las notas afectadas.
- **Pool de 64 sesiones de ssh-mcp vuelve a agotarse:** es el segundo incidente documentado (el primero se recuperó el 2026-09-17). Los probes init-per-call sin `close-session` agotan el pool global y el síntoma externo es un 503 que parece «servicio caído». La sesión lo resolvió con el recovery documentado, pero el problema es estructural (TTL de sesión inactivo largo o fuga de sesiones por parte de consumers).
- **Menor:** `sftp-upload` normaliza saltos de línea y falla silenciosamente como canal byte-exacto (ya documentado en el runbook); toda transferencia de fuentes MQL exige la ruta base64+`certutil -decode`+sha256. Se aplicó sin fricción, se registra para refuerzo.

## Mejora propuesta

- Añadir al runbook `aranea-mcp-capability-plane` (o `aranea-ssh-mcp`) una regla de gate previo: antes de declarar NOT_RUN/BLOCKED por acceso a un host con perfil certificado, ejecutar el smoke mínimo del plano (auth negativa, `/status`, initialize, `tools/list`) y registrar el resultado exacto; el 503 de session-limit debe leerse como «pool», no como «capability caída».
- Considerar en el appliance (owner/`mcps-ops`) un TTL de expiración de sesiones MCP inactivas o un job de higiene que cierre sesiones huérfanas, para que el pool de 64 no dependa de la disciplina de los consumers.
- En `aranea-ssh-mcp`, dejar explícito que `mt5-kronos-operator` es el camino canónico de compile/upload para E-06/T21 (con la receta base64+certutil), y que las keys SSH temporales por sesión NO son el mecanismo de transferencia autorizado recurrente.

## Impacto

- Corrección ya aplicada en: nota E-06 (errata + bullet nuevo), VERIFICATION.md @ `1f59b19b`, log C2 y agent-runs C2/R2 (secciones de corrección appended), change_log `2026-09-18-e06-t21-prereq-access-restored`.
