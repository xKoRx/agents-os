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
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
aliases: []
confidence: verified
source_session: 2026-09-13-0217-f04-runtime-authority-correction
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# F-04 Runtime Authority Correction — 2026-09-13

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution / updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo Forge — F-04 Magic allocation, version seal and handoff.md`
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md`
  - cierre de sesión y agent run de esta sesión

## Motivo

- Corregir la conclusión previa que trató `/opt/symphony/*` como identidad de release.

## Fuentes usadas

- F-04 project/SPEC, `aranea-ssh-mcp`, `sqx-deployer`, `deployment-proof`, runtime/release runbooks y evidencia MCP actual.

## Resolución aplicada

- Se dejó explícito que los marcadores `/opt/symphony/*` son `LEGACY / NON-AUTHORITATIVE` y que `0.2.98 absent` no fue probado. La autoridad real observada en Zeus/Hera/Kronos es `/opt/stager/releases/0.2.98/bin/symphony` bajo `stager-runtime.service`, con Stager activation committed y poller `sqx-main-queue`. Windows queda no probado por `POLICY_DENIED` del viewer; no se hizo bypass ni operación writable.

## Validación

- Baseline y release PASS; rollout global INCONCLUSIVE; no se crearon IDs, no se ejecutó licencia/workflow y T2.11/T2.12/T2.13 permanecen OPEN.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- El cambio es de evidencia/documentación y es reversible retirando la entrada de corrección; no hubo cambios de producto, release ni configuración remota.
