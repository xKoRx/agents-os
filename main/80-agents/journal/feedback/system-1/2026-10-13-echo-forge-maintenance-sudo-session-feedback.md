---
type: feedback
schema_version: 1
scope: session
created: 2026-10-13
updated: 2026-10-13
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-10-13-zcode-glm-5-3-flash-symphony-maintenance-kiss]]"
session_goal: cierre de sesión con remediación KISS de maintenance SQX y prueba física parcial
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/echo
  - agent/system1
---

# Feedback — maintenance SQX: bloqueo de sudo para agentes en lab hosts

- Fricción real: el flujo de maintenance exige `sudo -n proactiva-set-machine-id.sh` y el sudoers del lab sólo cubre a `kor`; el rol `operator` de aranea-ssh (grupo dev) tiene denegada la clase privileged, así que un mandato owner explícito de probar con licencias reales queda a mitad de camino (fallo verificado en Hera; shots intactos por el gate fail-closed). `privileged-command` también lo rechaza por roleBinding, no por falta de credencial.
- Sistema 1: sin soporte para conceder elevación puntual auditable en lab hosts; la vía fue preparar binarios verificados (SHA256) en `/tmp` del host para que kor ejecute 1 comando. Funcionó, pero el agente no puede cerrar el ciclo él solo.
- Candidato de mejora: rol/arquitectura que permita ejecutar el helper de maintenance como kor (o regla sudoers para echo-dev limitada al helper), con log de auditoría. Impacto MEDIUM, riesgo LOW.
