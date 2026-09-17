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

# 2026-09-17-f05c-cert-f04-01-c4-microfix-release-rollout

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-17 — Microfix, release y rollout CERT-F04-01 encoding` con veredicto `RELEASE/ROLLOUT PASS` + actualización de `Estado de entrada` + reemplazo de `Próxima tarea única recomendada para NORMAL`; sin cambio de clases A/B/C y sin ejecutar ningún gate físico)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-c4-microfix-release-rollout.md` (creado)
  - repo `xKoRx/symphony`: commit `a440ac4ed730747b1ae6b07557cb6204102f16ac` en `codex/f04-cert-f04-01-encoding-fix` y fast-forward puro de `codex/f05-release-prep`; release `0.2.100` (6 objetos + manifest en bucket `deploy`)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-C4`: aplicar el microfix UTF-8 exigido por la revisión manager del source C3 (branch sin BOM de `decodeCompileLogText` retornaba bytes sin validar), integrarlo en el branch de release, publicar versión nueva resuelta por `release-authority` y desplegarla en flota completa. Sin campañas, sin CERT-F04-01, sin infraestructura, sin ETCD, sin watcher de certificación.

## Fuentes usadas

- [[Echo + Echo Forge — Deferred Certification Backlog]] (delta C3 `SOURCE FIX PASS`, estado `CERT-F04-01 = BLOCKED`, contrato RERUN frozen).
- Runbook `aranea-ssh-mcp` (§ Evidence publisher worker-kronos y SQX operators), runbook `symphony-release-certification`, pipeline canónico `deploy_release.sh --release-only` y CLI `release-authority` del repo.

## Resolución aplicada

- **Microfix:** commit único `a440ac4…` sobre C3 con `utf8.Valid` en el branch sin BOM + regresiones M1–M4; demostrado fallar contra C3 (worktree temporal) y pasar con el fix; scope exacto de 2 archivos; push con read-back remoto.
- **Release `0.2.100`:** resuelta por autoridad remota (`release-authority` AUTO: `published=0.2.99`, `CONSISTENT`, candidato `0.2.100`); build/publicación con `./deploy_release.sh --release-only 0.2.100`; `vcs.revision=a440ac4…` en los 3 binarios; manifest publicado 22:44:45Z y read-back `CONSISTENT`/`EXACT_MATCH` (6/6 objetos byte-exactos); sin sobrescribir `0.2.99`.
- **Rollout:** Linux Zeus/Hera/Kronos converged vía Stager (CURRENT `0.2.100`, worker único por host bajo `releases/0.2.100/bin` con SHA256 == artifact, pollers vivos); Windows `worker-kronos` converged vía evidence publisher SYSTEM (`partial=false`, PID 5496 @ `releases\0.2.100\bin`, SHA256 exacto, CURRENT/PENDING `0.2.100`, poller ESTABLISHED, singleton).

## Validación

- Tests: T1–T8 + M1–M4 PASS; `core/capabilities` OK; `adapters/mt5` raíz OK (C4/C5/durable); MT5CompilePersist 7/7 + workflow wiring PASS; 75 fallos de fixtures históricos idénticos al baseline C3 (listas normalizadas comparadas); ninguna suite fallida declarada verde. Integración fast-forward exacta con read-back. `CERT-F04-01` permanece `BLOCKED / READY TO RERUN`; rollout ≠ certificación física.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales sensibles, memoria interna ni secretos

## Rollback

- Repo: los dos pushes son fast-forward del mismo lineage; rollback documental = revertir el delta fechado, `Estado de entrada` y `Próxima tarea` del backlog y borrar este log + agent-run; el microfix en source se revertiría con un commit nuevo (no force-push). Release: no sobrescribir; una corrección futura publica versión nueva desde el source correcto (política vigente). Runtimes: el Stager converge a cualquier manifest posterior; no se tocan binarios a mano.
