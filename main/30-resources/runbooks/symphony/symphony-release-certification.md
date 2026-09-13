---
type: runbook
schema_version: 1
scope: application
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Symphony]]"
related:
  - "[[release-certification]]"
  - "[[echo-forge-golden-e2e]]"
aliases:
  - certificación de release Symphony
  - baseline y source gate Symphony
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/application
  - project/echo-forge
---

# symphony-release-certification

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Ejecutar los gates baseline/source/release de `release-certification` sobre el repo `xKoRx/symphony` (workspace Go `~/go/src/github.com/xKoRx/symphony`), demostrando que una release corresponde al commit autorizado y conserva los contratos congelados.

## Precondiciones

- Repo local en el workspace Go; acceso de red a origin (fetch). Baseline autorizado y commit(s) certificado(s) de referencia vienen del runbook del ciclo (ej. [[echo-forge-golden-e2e]]) o del checkpoint del proyecto.

## Procedimiento

1. Baseline: `git fetch origin`; `git rev-parse HEAD` y `git rev-parse origin/master` deben ser iguales entre sí y al baseline autorizado; `git merge-base --is-ancestor <commit_certificado> HEAD` debe salir 0; `git status --porcelain` para inventariar dirty (foreign dirty típico: `go.work.sum` — preservar, sin stage/commit/clean).
2. Source integrity: si HEAD avanzó desde el commit certificado, `git log --oneline <certificado>..HEAD` y `git diff --name-only <certificado>..HEAD -- '*.go' '*.sql'`; sólo chores/artifacts ⇒ rebaseline operacional documentado; fuentes funcionales ⇒ BLOCKED. Blob equality de los archivos congelados: `git rev-parse <ref>:<path>` vs `HEAD:<path>`; last-commit por carrier: `git log -1 --format='%h %s' -- <path>` debe dar el commit de su slice certificada.
3. Release: construir con el mecanismo canónico `./deploy_release.sh "" [rollout_s]` (versión AUTO desde el manifest publicado en MinIO; NO reutilizar versiones; el script además despacha intake — ver [[echo-forge-golden-e2e]]). Demostrar contenido: `go version -m deploy/<v>/linux-amd64/symphony` y `deploy/<v>/windows-amd64/sqx-mt5-worker.exe` → `vcs.revision` == HEAD autorizado y `dep github.com/xKoRx/sdk` == pin esperado; sha256/size de cada artefacto desde `deploy/manifest.json` (`.artifacts[].files[]`). `vcs.modified=true` es esperable por dirty operacional no-Go; exigir explicación de qué archivos.
4. SDK: el repo `~/go/src/github.com/xKoRx/sdk` debe estar en el commit del pin; verificar `git rev-parse HEAD` allí y el `replace ../sdk` en `go.mod`.

## Validación

- Los tres veredictos PASS con evidencia (refs, hashes, salidas `go version -m`) pegadas en el checkpoint de la sesión. Fin de estado esperado del worktree tras una corrida: `go.work.sum` (foreign) + `input/example/config.json` (intake) + `deploy/manifest.json` (release) — nada más.

## Rollback / recuperación

- No hay rollback de gates de lectura. Si la release quedó mal construida, NO sobrescribir la versión: publicar una versión nueva desde el source correcto. Si `deploy_release.sh` aborta con carpeta huérfana, sigue sus propias instrucciones (nunca eliminar releases a mano sin entendimiento).

## Evidencia

- Sesión 2026-08-29 (`1f0880c`, release 0.2.79): gates PASS con blob equality de 8 archivos Apply vs `2fa17010`; intervalo con 3 chores (`baadc35`,`6d30d0f`,`1f0880c`); [[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]].
