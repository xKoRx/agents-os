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
source_session: ZCode (daedalus, F05C-CERT-F04-01-C13)
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-20 — Echo Forge CERT-F04-01 C13: release 0.2.104, recuperación natural de RERUN-6 y CERT_F04_01_PASS

## Cambio canónico

- **Entidades actualizadas por delta, no recreadas:** `main/10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (párrafo C13 añadido al final de la narrativa de estado de entrada con el veredicto `CERT_F04_01_PASS`/`RERUN6_RECOVERED`/`RERUN7_NOT_REQUIRED`; nueva sección `### Delta de release, recuperación natural y certificación C13 — 2026-09-20` con G0–G7 completos; "Próxima tarea única recomendada para NORMAL" actualizada: C13 consumió el ciclo restante y el próximo gate único es CERT-F04-02 desbloqueado) y `main/10-projects/Echo Forge/Echo Forge.md` (nueva entrada 2026-09-20 en `## 📆 Bitácora`). Cero cambios a contratos, templates ni a otras entidades.

## Cambio en repos externos (symphony, fuera del vault)

- `codex/f05-release-prep` fast-forward `2993da0…`→`25a5122baec197ab67bb38eec454d6e62400a472` (push sin force, read-back origin en ambas ramas) y release `0.2.104` publicada en MinIO vía `deploy_release.sh --release-only` + deployer-watcher; flota 4/4 convergida por Stager (Zeus 2839157 / Hera 1421854 / Kronos 1383513 / Windows 40192; deploy canónico, sin SSH de configuración).
- Ningún commit nuevo creado: `25a5122` fue el fix C13 ya publicado y aprobado por el manager; esta sesión sólo lo integró a la rama de release y lo publicó.
- Ningún cambio a Echo, contratos, schemas, SDK, migrations ni ETCD (echo permanece en 0 keys; fail-closed vigente).

## Evidencia de la sesión

- Workdirs: `~/aranea/work/f04-cert-f04-01-rerun6/` (evidencia canónica C12 + `g1-stage/` nuevo con los 20 artefactos auténticos SHA256-verificados, las 10 evaluaciones y el ancla `effective_inputs_m16_REAL.json`) y `~/aranea/work/f04-cert-f04-01-g5/seal-fix/` (worktree del fix; arnés G1 creado y eliminado sin residuo; worktree gemelo de baseline creado y eliminado).
- Lecturas de producción: Temporal `sqx-prop` vía gRPC `/tmp/thist` (list/show/actres/result + describes scratch `g0desc2.go`/`g0retry.go`); Mongo forge RO; MinIO presign GET + curl; ETCD RO; SSH operator (zeus/hera/kronos/mt5-kronos).
- Agent run: [[2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-01-c13-recovery-certified]].
