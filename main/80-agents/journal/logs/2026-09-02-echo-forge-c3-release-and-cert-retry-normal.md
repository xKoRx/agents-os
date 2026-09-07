---
type: change_log
schema_version: 1
scope: session
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: ["[[Echo Forge]]"]
related: ["[[2026-09-02-sqx-watcher-stager-current-link-mismatch]]"]
aliases: []
confidence: verified
source_session: "ECHO-FORGE-C3-RELEASE-0.2.86-AND-CERT-RETRY-NORMAL"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge C3 release 0.2.86 and certification retry

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `xKoRx/symphony/deploy/manifest.json` and `deploy/0.2.86/` (operational release)
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`
  - `80-agents/journal/agent-runs/2026-09-02-2335-codex-unknown-echo-forge-c3-release-and-cert-retry-normal.md`
  - `80-agents/journal/feedback/system-1/2026-09-02-2335-echo-forge-c3-release-and-cert-retry-normal-session-feedback.md`

## Motivo

- Registrar el release físico 0.2.86 y el bloqueo de convergencia Windows que impidió iniciar una nueva certificación.

## Fuentes usadas

- Source gate, release-authority real, logs del deployer/watcher, hashes locales y auditoría remota read-only de Zeus/Hera/Kronos/Windows.

## Resolución aplicada

- `./deploy_release.sh` publicó 0.2.86 y dejó la autoridad en `CONSISTENT/EXACT_MATCH`; Linux 3/3 convergió. Windows quedó `CURRENT=0.2.86` pero `StagerRuntime=StopPending`, activación `signaled` y worker activo 0.2.85. La única recuperación normal autorizada falló al detener el servicio; C3 se cerró `BLOCKED` antes de supply/Campaign.

## Validación

- Se preservaron source, commit, push, DB, MinIO manual, fixtures y el FlowRun contaminado. No se creó una nueva known-error por falta de recurrencia confirmada; el bloqueo queda en el checkpoint y este log.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- PASS: source/SDK exactos, parent/diff exactos, autoridad pre/post, publicación canónica, hashes y ausencia de 0.2.87. BLOCKED: Windows 4/4 y todos los gates posteriores no ejecutados por stop rule.
