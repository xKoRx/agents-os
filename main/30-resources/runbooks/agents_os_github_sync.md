---
type: runbook
schema_version: 1
scope: service
created: "2026-09-07"
updated: "2026-09-07"
area: "[[Personal]]"
project:
application:
entities: []
related:
  - "[[AGENTS OS]]"
aliases:
  - Sync GitHub del vault
  - repo agents-os
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - area/personal
  - kind/runbook
  - scope/service
  - tech/git
  - tech/github
  - tech/cron
---

# Sync del vault a GitHub — repo agents-os

> El vault (`~/secondbrain/main`) se sincroniza automáticamente cada 1 minuto con `github.com/xKoRx/agents-os`. Cualquier cambio local o remoto se integra solo; este runbook describe el estado, la política de colisiones y la operación manual.

## Estado

- Repo root: `/home/kor/secondbrain` (`.git` ahí, branch `master`).
- Remote: `git@github.com:xKoRx/agents-os.git` — **repo PÚBLICO**.
- `main/` es el vault completo, como carpeta dentro del repo. `README.md` y `AGENTS.md` viven al lado del vault.
- Ignorados por git: `main/.obsidian/`, `.sync/`.
- Cron (crontab de usuario): `* * * * * /home/kor/secondbrain/sync.sh >> /home/kor/secondbrain/.sync/cron.log 2>&1`.

## Procedimiento (lo que hace `sync.sh` cada minuto)

1. `flock` no bloqueante: si otra corrida vive, este ciclo no hace nada.
2. `fetch origin master`; sin red → corta en silencio y reintenta el próximo ciclo.
3. Cambios locales (incluidos nuevos) → `git add -A` + commit `sync HH:MM`.
4. Remoto avanzó → integrar en este orden:
   - sólo atrás → `merge --ff-only`;
   - divergido → `rebase`;
   - conflicto de contenido → `rebase --abort` + `merge -X ours` (gana lo local, archivos nuevos del remoto entran igual);
   - conflicto duro → push del remoto a branch `conflict-<fecha>` + `merge -s ours`.
5. `push` con 3 reintentos (re-integra si el remoto se movió en el camino). Nunca force-push.

Agente externo (ChatGPT, etc.): pushear directo a `master`, nunca force-push; leer `AGENTS.md` del repo root antes de trabajar.

## Validación

- `tail /home/kor/secondbrain/.sync/sync.log` — cada acción queda con timestamp.
- `git -C /home/kor/secondbrain ls-remote origin refs/heads/master` debe ser igual a `git -C /home/kor/secondbrain rev-parse HEAD`.

## Rollback / recuperación

- Estado remoto previo a un conflicto duro: branches `conflict-<fecha>` en origin.
- Historial local de referencia: `git reflog` en el repo root.
- Reinstalar el cron: ver línea exacta en la sección Estado.
