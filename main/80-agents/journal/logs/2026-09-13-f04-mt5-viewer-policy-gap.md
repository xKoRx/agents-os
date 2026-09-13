---
type: change_log
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Echo]]"
project: "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Aranea]]"
related:
  - "[[aranea-ssh-mcp]]"
aliases: []
confidence: verified
source_session: 2026-09-13-f04-mt5-viewer-policy-gap
source_feedbacks:
  - "[[2026-09-13-f04-mt5-viewer-policy-gap-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# F-04 MT5 Viewer Policy Gap — 2026-09-13

## Cambio

- Tipo: conflict-resolution / updated.
- Archivos: F-04 project note, Factory V2 parent note, session summary y session feedback.

## Motivo

- Resolver el gap Windows mt5-kronos siguiendo la corrección de autoridad: no asumir viewer capability missing ni escalar a operator por conveniencia.

## Fuentes usadas

- aranea-mcps-expert, aranea-ssh-mcp, capability-plane, deployment-proof, F-04 project/SPEC y probes MCP actuales.

## Resolución aplicada

- Baseline remoto confirmado en b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43; release 0.2.98 se dejó intacta.
- mt5-kronos viewer admitió hostname y whoami, pero rechazó con POLICY_DENIED las operaciones únicas de StagerRuntime, sqx-mt5-worker, filesystem Stager, executable y poller.
- Se corrigió el estado vigente a confirmed MCP policy gap after minimal allowlisted probes y se preservó la historia previa.
- No se usó operator, no se modificó código/input/configuración, no se generaron IDs y no se inició LICENSE/T2.12/T2.11; T2.13 permanece fuera de scope.

## Validación

- Resultado: PHYSICAL BLOCKED — ARANEA MCP POLICY GAP — MT5 VIEWER.
- Próximo paso: corregir la allowlist viewer Windows o exponer un probe read-only equivalente y repetir rollout proof sin republish.

## Compartibilidad

- Scope: local / team.
- Redacción revisada: sin secretos, credenciales ni dumps operativos.

## Rollback

- El cambio es documental y reversible; no hubo mutaciones remotas ni cambios de product code.
