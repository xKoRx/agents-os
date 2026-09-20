---
type: change_log
schema_version: 1
scope: session
created: 2026-09-20
updated: 2026-09-20
area: "[[Echo]]"
project: "[[Echo Forge]]"
application:
entities:
  - "[[Echo Forge]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
related:
  - "[[Aranea]]"
aliases: []
confidence: verified
source_session: sess_3cf3822e-5d39-459c-821a-18d26aa39ad1 (ZCode)
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-20 — Echo Forge CERT-F04-01 C12/RERUN-6: release 0.2.103, campaña física y defecto #6

## Cambio canónico

- **Entidades actualizadas por delta, no recreadas:** `main/10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (delta C12/RERUN-6 añadido al final de la narrativa de estado de entrada: `CERT-F04-01 = BLOCKED / SOURCE_READY_FOR_MANAGER_REVIEW (defecto #6)`) y `main/10-projects/Echo Forge/Echo Forge.md` (nueva entrada 2026-09-20 en `## 📆 Bitácora`). Cero cambios a contratos, templates ni a otras entidades.

## Cambio en repos externos (symphony, fuera del vault)

- `codex/f05-release-prep` fast-forward `66faa42…`→`2993da0…` (push sin force, read-back origin) y release `0.2.103` publicada en MinIO vía `deploy_release.sh --release-only` + deployer-watcher; flota 4/4 convergida por Stager (deploy canónico; sin SSH de configuración).
- Branch nuevo publicado sin desplegar: `codex/f05-seal-failclosed-delivery-fix` @ `25a5122baec197ab67bb38eec454d6e62400a472` (worktree aislado `~/aranea/work/f04-cert-f04-01-g5/seal-fix`; fix del defecto #6: terminal `HANDOFF_CREATED` para ingress sin autoridad E-04).

## Evidencia de la sesión

- Workdirs: `~/aranea/work/f04-cert-f04-01-rerun6/` (receta, validación, monitor.log 13 muestras, g0-g3-gates.md, g4-g5-evidence.md, seal-request-ev640.json) y `~/aranea/work/f04-cert-f04-01-g1/` (12 artefactos auténticos RERUN-5 + 6 evaluaciones durables + log del ensayo del seal 3/3).
- Recuperación de plano MCP documentada aplicada: `docker restart ssh-mcp` en mcps por cadena daedalus→hermes→mcps-ops (runbook aranea-ssh-mcp §106; pool 64 agotado). Ningún producto tocado.
- Agent run: [[2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-01-c12-rerun6]].
