---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
application:
entities:
  - "[[Aranea]]"
  - "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
related:
  - "[[hermes-agent-operator]]"
  - "[[hermes-linux-update-recovery]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-16-hermes-runtime-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/aranea
  - tech/hermes
---

# 2026-09-16 — Hermes runtime operator and update recovery

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `30-resources/agents/skills/hermes-agent-operator/SKILL.md`
  - `30-resources/runbooks/hermes-linux-update-recovery.md`
  - `30-resources/agents/skills/aranea-agent-dev/SKILL.md`
  - `30-resources/agents/00-index.md`
  - `30-resources/agents/log.md`
  - `30-resources/runbooks/00-index.md`
  - `30-resources/runbooks/log.md`
  - `10-projects/Aranea/agentes/HERMES — Infrastructure Operations.md`

## Motivo

- Una actualización real de Hermes dejó `mixed sys.modules`, procesos stale y un `fleet_restart_pending` que exigía un gateway default legacy. No existía una skill dedicada para operar Hermes como target ni un runbook de recovery de su updater Linux.
- La ausencia obligó a reconstruir manualmente el boundary entre perfil sticky, `HERMES_HOME`, unidades `systemd --user`, receipts, markers y gateways duplicados.

## Fuentes usadas

- Evidencia física de la sesión 2026-09-16 sobre el host Hermes: versión/SHA, procesos/cgroups, unidades user, receipts/markers, gateway state y health HTTP/Telegram.
- `80-agents/skills/_shared/note-types.md` para separar skill vs runbook vs memoria.
- `80-agents/skills/agents-os-skill-authoring/SKILL.md` y `80-agents/skills/_shared/skill-contract.md` para el boundary agent-facing.
- `HERMES — Infrastructure Operations` como source of truth del management plane Hermes.

## Resolución aplicada

- Se crea `hermes-agent-operator` como skill federada Aranea: decisiones, routing, guards y contrato de salida cuando Hermes mismo es el target.
- Se crea `hermes-linux-update-recovery` como runbook mecánico validado: baseline, fresh-process proof, supervisor discovery, restart ordenado, duplicación de gateways, receipt/marker reconciliation, backup/cleanup y smoke final.
- `aranea-agent-dev` enruta a la nueva skill sólo cuando Hermes es el target, evitando activarla cuando Hermes sólo opera otro servicio.
- El proyecto canónico registra el baseline vigente: Hermes v0.21.3/`8c8003f8`, dashboard loopback HTTP 200, gateway Ariadna conectado y gateway default legacy disabled por token Telegram compartido.

## Validación

- Recovery físico final PASS: `PENDING_RESTART = False`; proceso fresco `Hermes Agent v0.21.3 (2026.9.14) · upstream 8c8003f8 · Up to date`; dashboard HTTP 200; `hermes-gateway-ariadna.service` active; Telegram `connected`, `needs_attention=false`.
- Skill/runbook mantienen responsabilidades separadas: juicio/orquestación en skill, secuencia mecánica/rollback en runbook.
- Índices y resource logs actualizados para discovery.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** no contiene tokens Telegram ni valores secretos; sólo topología, nombres de unidades, paths operativos y hashes/versiones de código.

## Rollback

- Revertir los commits de documentación si la clasificación skill/runbook se rechaza.
- El estado operativo del host no depende de estos documentos; para el marker runtime existe backup `fleet_restart_pending.bak-20260916-220032` en el perfil Ariadna.
