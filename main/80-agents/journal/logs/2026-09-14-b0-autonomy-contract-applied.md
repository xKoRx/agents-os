---
type: change_log
schema_version: 1
scope: session
created: "2026-09-14"
updated: "2026-09-14"
area: "[[Aranea]]"
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
application:
entities:
  - "[[HERMES — Bootstrap & Self-Sufficiency]]"
  - "[[Ariadna]]"
related:
  - "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases:
  - B0 autonomy contract patch
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/aranea
  - project/hermes-aranea-autonomous-operations
---

# B0 — Contrato de autonomía AUTO/GATED aplicado

## Cambio

- **Tipo:** updated
- **Alcance:** contrato operativo de Ariadna (B0.2/B0.3 del bootstrap) + preparación B1.

## Archivos modificados

1. `~/.hermes/profiles/ariadna/SOUL.md` — §8 paso 6 pasa de "owner confirmation por
   defecto" a confirmation sólo para GATED; se agrega §8.1 con clasificación AUTO
   (discovery, Agents-OS normal, administración LXC `mcps` por `~/aranea/bin/mcps-ops`,
   repair DEV/test MCP, rollback propio, onboarding consumers DEV/test) vs GATED
   (PROD no preautorizado, destructivo permanente, red/firewall alto blast radius,
   host-level Proxmox/TrueNAS fuera de fase, borrado irreversible VM/LXC/storage,
   rotación credenciales sin recovery, trading echo siempre gated, acción fuera de
   authority certificada). Preservados: secretos, target proof, rollback/post-condition.
2. `80-agents/crew/Ariadna.md` — Regla Dura 1 "No auto-aprobar tickets" reemplazada
   por el approval model AUTO/GATED; callout de evolución 2026-09-14 en la cabecera.
3. `~/.hermes/profiles/ariadna/memories/USER.md` — regla "owner ejecuta root
   manualmente, ariadna solo lee" scopeada a Proxmox/TrueNAS/hosts, con excepción
   `mcps` vía management path nativo.

## Artefactos B1 creados (sin authority en destino aún)

- `~/.ssh/agent_mcps_ops` — identity ED25519 dedicada `hermes-ops@mcps.lab.aranea`,
  fingerprint `SHA256:1ebPwqXIyeCC8zo4spKg+OyTDPYMXg78Kv1BaKRgp48` (sólo fingerprint
  público; private key nunca se imprime ni persiste en vault).
- `~/.ssh/known_hosts` — host key ED25519 de `mcps.lab.aranea.cl` pinneada strict
  (`SHA256:REpcjg31iDIJ5xysEaM63UBgbtuIU3KCuvuJ0NZo+lY`).
- `~/.ssh/config` — host alias `mcps-ops` (User hermes-ops, IdentitiesOnly, StrictHostKeyChecking yes, BatchMode).
- `~/aranea/bin/mcps-ops` — wrapper entrypoint con logging a `~/.hermes/logs/mcps-ops.log`.
- Estado actual del path: `Permission denied (publickey)` — falta instalar la public
  key y el usuario `hermes-ops` en el LXC `mcps` (OWNER ACTION BUNDLE emitido).

## Motivo

Proyecto [[HERMES — Bootstrap & Self-Sufficiency]] B0: el approval model histórico
bloqueaba la autonomía objetivo del programa padre. El patch preserva los gates de
alto impacto y no debilita secret/target-proof/rollback.
