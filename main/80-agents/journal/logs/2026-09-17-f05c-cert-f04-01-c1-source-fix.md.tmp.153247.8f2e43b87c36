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
  - "[[Echo Forge — F-01 Canonical Generation Concurrency Contract]]"
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

# 2026-09-17-f05c-cert-f04-01-c1-source-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-17 — Corrección source CERT-F04-01` con veredicto `SOURCE FIX PASS` + actualización de `Estado de entrada` con `blocker source fix = SOURCE VERIFIED` + reemplazo de `Próxima tarea única recomendada para NORMAL`; sin cambio de clases A/B/C y sin ejecutar ningún gate físico)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-c1-deadline-fix.md` (creado)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-C1`: corregir en source el defecto determinístico demostrado por el run físico EXEC 2026-09-17 (`mt5_compile_artifact` → `persistence_deadline_required` en 3/3 compile children @ release `0.2.98` / `b57bfb2`), sin re-ejecutar el gate, sin publicar release, sin deploy y sin tocar infraestructura. Diseño frozen: fix en el boundary compartido `DownloadArtifactTaskSource`; prohibido tocar `MT5OwnershipCoordinator`, workflows Temporal, ActivityOptions, ETCD, MinIO adapter global, worker boot y release config.

## Fuentes usadas

- [[Echo + Echo Forge — Deferred Certification Backlog]] (delta EXEC 2026-09-17 con el defecto y la decisión manager) y [[Echo Forge — F-04 Magic allocation, version seal and handoff]] (contrato F-04 vigente).
- Decisiones B1A/B1B/B2 de ownership MT5 (contexto B2: `physicalCtx` derivado de `context.WithoutCancel(activityCtx)` sin deadline; D1–D4) documentadas en la entidad Echo Forge.
- Source @ `xKoRx/symphony` `3d0e8c958765da23840e00bf1a0ac017fc47597a` (== `origin/codex/f05-release-prep`; `b57bfb2` ancestro; locus idéntico al source de la release): `sqx/adapters/mt5/artifact_compiler.go`, `sqx/adapters/mt5/artifact_runner.go`, `sqx/adapters/storage-minio/durable_artifacts.go`, `sqx/core/capabilities/persistence.go`, convención self-wrap `sqx/activities/worker/durable_select_robust_run.go`.

## Resolución aplicada

- Fix en `DownloadArtifactTaskSource` (`sqx/adapters/mt5/artifact_compiler.go`): fetch durable auto-acotado con `context.WithTimeout` sobre la constante package-local `artifactSourcePersistenceTimeout = 2 * time.Minute` sólo cuando el ctx entrante no tiene deadline; deadline entrante preservado exacto; cancelación del caller permanece observable; legacy key-only sin cambios; durable → key-only sigue prohibido (sin downgrade, SHA/size fail-closed intactos). El timeout de persistencia no afecta al timeout del proceso físico MetaEditor (`Compile` crea su `execCtx` después de la descarga).
- Commit único `49fce32eb9eb6d0a4144891700fb6e5ccb36c2d1` (`fix(mt5): bound durable source fetch context`) en branch `codex/f04-cert-f04-01-deadline-fix`; 3 archivos (producción + 2 suites de regresión); sin merge, sin tag, sin release artifact; `MIGRATION: NONE`.
- Regresión T1–T6 agregada (habrían fallado en 0.2.98) + repro standalone del defecto contra el source de la release en worktree temporal eliminado después.
- Gates: `adapters/mt5` (C4/C5 incluidos), `core/capabilities`, `adapters/storage-minio` y `activities/worker/{pipeline,hooks,steps}` OK; resto de `./sqx/...` verde salvo fallos preexistentes demostrados idénticos contra baseline limpio (`activities/worker` 16, `mt5/report`, `mt5/binding`+`mt5/normalization` 37 — fixture físico `mt5-export.htm` ausente; `registry-postgres` 4; `workflows` 22; `tools` múltiples `main`). Efecto lateral de suite (`f5_warning_example.json`) restaurado a HEAD.

## Validación

- T1–T6 PASS con mocks que fallan el test si `FetchDurableToPath` no recibe deadline (T5/T6 sobre `Compile`/`Backtest` completos, no sólo el helper); repro del defecto contra 0.2.98 devuelve exactamente `persistence_deadline_required`; review local (`git diff --check`, `git status --short`, diff vs base) confirma sólo allowed files, dirty foráneo `phase4_performance.json` intacto, sin config/ownership/workflow/migration/release changes.
- Sin ejecutar `CERT-F04-01`, sin release, sin rollout, sin infraestructura; cero writes en ETCD/PG/Mongo/MinIO.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales sensibles, memoria interna ni secretos

## Rollback

- Repo: `git revert 49fce32eb9eb6d0a4144891700fb6e5ccb36c2d1` en el branch (o borrar el branch; base intacta). Vault: revertir el delta fechado, `Estado de entrada` y `Próxima tarea` en el backlog y borrar este log + el agent-run. El worktree de repro ya no existe.
