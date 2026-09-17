---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]"
aliases: []
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
---

# 2026-09-17-f05c-cert-f04-01-c2-release-rollout

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-17 — Release 0.2.99 y rollout` con veredicto `RELEASE/ROLLOUT PASS` + actualización de `Estado de entrada` + reemplazo de `Próxima tarea única recomendada para NORMAL`; sin cambio de clases A/B/C y sin ejecutar ningún gate físico)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-c2-release-rollout.md` (creado)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-C2`: convertir el fix ya implementado (`49fce32eb9eb6d0a4144891700fb6e5ccb36c2d1`, branch `codex/f04-cert-f04-01-deadline-fix`) en una release física desplegada y verificable, preparada para re-ejecutar `CERT-F04-01`. Sin ejecutar el gate, sin modificar el fix, sin tocar ETCD, sin campañas y sin lanzar watcher de certificación.

## Fuentes usadas

- [[Echo + Echo Forge — Deferred Certification Backlog]] (delta C1 `SOURCE FIX PASS` y estado `CERT-F04-01 = BLOCKED`), [[Echo Forge — F-04 Magic allocation, version seal and handoff]] y [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]].
- Runbook `symphony-release-certification`, decisiones `2026-09-01-release-version-authority` y `2026-09-03-deploy-release-only`, contrato `aranea-ssh-mcp` § Evidence publisher worker-kronos.

## Resolución aplicada

- **Source authority:** gate local PASS (branch/HEAD/parent/diff exacto, 3 archivos permitidos, dirty foráneo fuera del commit); fix branch publicado a `origin` y verificado por `ls-remote` + fetch + API GitHub (`HEAD 49fce32…`, `PARENT 3d0e8c9…`); `codex/f05-release-prep` fast-forward puro `3d0e8c9..49fce32` (sin merge/rebase/squash) con read-back remoto exacto.
- **Release `0.2.99`:** resuelta por autoridad remota (`release-authority` AUTO: `published=0.2.98`, `CONSISTENT`, candidato `0.2.99`); build completo con el pipeline canónico `./deploy_release.sh --release-only 0.2.99` (6 artifacts, sin reutilizar binarios 0.2.98); publicación vía deployer-watcher con confirmación de manifest en MinIO; read-back `release-authority --target 0.2.99` → `published_version=0.2.99`, `authority_state=CONSISTENT`, `target_state=EXACT_MATCH`.
- **Rollout:** Linux Zeus/Hera/Kronos converged vía Stager (CURRENT `0.2.99`, worker único por host bajo `releases/0.2.99/bin`, pollers `sqx-prop/sqx-main-queue` vivos; SHA256 del binario Zeus byte-exacto); Windows `worker-kronos` converged vía Stager y demostrado con el evidence publisher recurrente (`partial=false`, publisher SYSTEM, worker PID 20044 @ `releases\0.2.99\bin\sqx-mt5-worker.exe`, SHA256 == artifact, padre `stager-runtime`, poller ESTABLISHED, CURRENT/PENDING `0.2.99`).

## Validación

- Tests pre-release desde `49fce32…`: `sqx/adapters/mt5` (raíz, con C4/C5/durable y regresión T1–T6), `sqx/core/capabilities` y `sqx/adapters/storage-minio` OK; fallos `mt5/report`+`mt5/binding`+`mt5/normalization` = clase baseline conocida (fixture físico ausente), idénticos a C1, ninguno atribuible al fix. Buildinfo de los 3 binarios con `vcs.revision=49fce32…`. Manifest remoto capturado byte-exacto (6/6 objetos, SHA256/size == locales). Windows freshness 3 min (< stale 15 min). `CERT-F04-01` permanece `BLOCKED` — no ejecutado, READY TO RERUN.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales sensibles, memoria interna ni secretos

## Rollback

- Repo: los dos pushes son fast-forward del mismo lineage; rollback documental = revertir el delta fechado, `Estado de entrada` y `Próxima tarea` del backlog y borrar este log + agent-run. Release: no sobrescribir; una corrección future publica versión nueva desde el source correcto (política vigente). Runtimes: el Stager puede converger a cualquier manifest posterior; no se tocan binarios a mano.
