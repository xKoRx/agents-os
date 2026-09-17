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

# 2026-09-17-f05c-cert-f04-01-c3-encoding-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-17 — Corrección source CERT-F04-01 encoding` con veredicto `SOURCE FIX PASS` + actualización de `Estado de entrada` con `blocker source fix encoding = SOURCE FIX VERIFIED` + reemplazo de `Próxima tarea única recomendada para NORMAL`; sin cambio de clases A/B/C y sin ejecutar ningún gate físico)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-c3-encoding-fix.md` (creado)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-C3`: corregir en source el segundo defecto determinístico de la release `0.2.99` demostrado por el run físico RERUN 2026-09-17 (`mt5_compile_persist_v1` → `CONTRACT_CONFLICT / artifact_integrity: compile log does not report 0 errors` con MetaEditor `0 errors, 1 warnings` y log UTF-16LE con BOM), sin publicar release, sin deploy, sin campañas y sin re-ejecutar CERT-F04-01. Decisión de implementación de la misión: un único criterio compartido de compile success con autoridad en `sqx/core/capabilities`; prohibido cambiar el significado del patrón de éxito, convertir warnings en errores, aceptar `1 errors` o usar heurísticas de encoding por substrings.

## Fuentes usadas

- [[Echo + Echo Forge — Deferred Certification Backlog]] (delta RERUN 2026-09-17 con el defecto físico y las identidades del run) y [[Echo Forge — F-04 Magic allocation, version seal and handoff]] (contrato F-04 vigente).
- Source @ `xKoRx/symphony` `49fce32eb9eb6d0a4144891700fb6e5ccb36c2d1` (== `origin/codex/f05-release-prep`): `sqx/adapters/mt5/artifact_compiler.go`, `sqx/core/capabilities/strategy_version.go`, `sqx/activities/worker/mt5_compile_persist_activity.go` (path del seal), `sqx/core/domain/artifact_paths.go` (derivación de keys).
- Lecturas read-only acotadas para la evidencia física: Temporal RO, MinIO RO, Postgres RO, Mongo forge RO y ETCD RO (etcd `/sqx-mt5-worker/production/*` para namespace/endpoint del stack 0.2.99).

## Resolución aplicada

- Función pura exportada `CompileLogReportsZeroErrors(raw []byte) bool` en `sqx/core/capabilities/strategy_version.go`: única autoridad de interpretación de compile logs para compiler y seal (UTF-8; UTF-16LE/BE con BOM; patrón contractual intacto `(?i)Result:\s*0 errors`; fail-closed estricto para log ausente/vacío/encoding inválido, sin truncamiento silencioso de bytes finales ni surrogates sin pareja). `VerifyCompiledArtifactForSeal` delega en ella (mismo error y envoltura `ErrArtifactIntegrity`); `evaluateCompileArtifacts` delega y el parser duplicado del adapter (`compileSuccessPattern` local, `normalizeCompileLog`, `utf16LEToString`, `utf16BEToString`) fue eliminado. Los bytes durables originales nunca se modifican ni re-escriben.
- Commit único `18d09054630f1da0f3c44a13c6132af3e17b0596` (`fix(forge): unify compile log validation across compiler and seal`) en branch `codex/f04-cert-f04-01-encoding-fix` (base `49fce32…`, 4 archivos autorizados); publicado a origin con read-back remoto completo (HEAD/parent/archivos/patch digest). Sin merge a `codex/f05-release-prep`, sin tag, sin release, `MIGRATION: NONE`.
- Regresión T1–T8 agregada; los tests seal-level de UTF-16 fallan contra `49fce32` (demostrado con worktree temporal @ base + tests nuevos, eliminado sin residuo) y pasan con el fix. Límite declarado: PHYSICAL LOG BYTES NOT AVAILABLE (fixtures determinísticos, no bytes auténticos).

## Validación

- `go test ./sqx/core/capabilities/...` OK; `./sqx/adapters/mt5/` OK (paquete del fix, C4/C5 incluidos); `MT5CompilePersist` enfocado 7/7 PASS; `TestGenericWorkflow_WiresCompilePersistAfterDurableSuccess` PASS; `go vet` + `gofmt` OK en los 4 archivos. Fallos preexistentes aislados por diff de listas exactas `--- FAIL` contra baseline `49fce32` (`mt5/binding`+`mt5/normalization`+`mt5/report` 55; `activities/worker` 16 — fixture físico `mt5-export.htm` ausente, clase documentada C1); ningún fallo nuevo atribuible al fix.
- Sin ejecutar `CERT-F04-01`, sin release, sin rollout, sin campañas, sin writes en ETCD/PG/Mongo/MinIO; dirty foráneo `deploy/manifest.json` + `phase4_performance.json` preservados intactos y fuera del commit.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales sensibles, memoria interna ni secretos

## Rollback

- Repo: `git revert 18d09054630f1da0f3c44a13c6132af3e17b0596` en el branch (o borrar el branch remoto/local; base `49fce32…` y `codex/f05-release-prep` intactos, sin release publicada). Vault: revertir el delta fechado, `Estado de entrada` y `Próxima tarea` en el backlog y borrar este log + el agent-run. Los worktrees de verificación ya no existen.
