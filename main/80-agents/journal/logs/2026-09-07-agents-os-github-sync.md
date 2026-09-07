---
type: change_log
schema_version: 1
scope: session
created: "2026-09-07"
updated: "2026-09-07"
area: "[[Personal]]"
project:
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents_os_github_sync]]"
  - "[[2026-09-07-zcode-glm-5.3-flash-agents-os-github-sync]]"
  - "[[ZCode]]"
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

# 2026-09-07-agents-os-github-sync

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `/home/kor/secondbrain/.git` + commit inicial del vault en `master` (created) — repo local del vault, remoto `github.com/xKoRx/agents-os`.
  - `/home/kor/secondbrain/sync.sh` (created) — sincronizador automático con política de colisiones.
  - `/home/kor/secondbrain/README.md`, `/home/kor/secondbrain/AGENTS.md`, `/home/kor/secondbrain/.gitignore` (created) — entrada para agentes externos y exclusiones (`.obsidian/`, `.sync/`).
  - crontab de usuario: `* * * * * /home/kor/secondbrain/sync.sh` (created).
  - `30-resources/runbooks/agents_os_github_sync.md` (created).
  - `80-agents/crew/INDEX.md` (updated) — [[ZCode]] agregada a superficies registradas (la nota canónica ya existía).
  - `80-agents/journal/agent-runs/2026-09-07-zcode-glm-5.3-flash-agents-os-github-sync.md` (created).

## Motivo

- El usuario pidió sincronización automática del vault con GitHub (repo `xKoRx/agents-os`), con `.git` a nivel de `~/secondbrain`, el vault como carpeta completa (`main/`) dentro del repo, README y AGENTS.md al lado, y un cron cada 1 minuto que haga commit `sync HH:MM` + push resistiendo el peor caso (cambios locales y remotos simultáneos, por ejemplo desde ChatGPT).

## Fuentes usadas

- `80-agents/skills/agents-os-session-close/SKILL.md`
- `80-agents/skills/agents-os-agent-run-register/SKILL.md`
- `80-agents/agents-os/agent-constitution.md`
