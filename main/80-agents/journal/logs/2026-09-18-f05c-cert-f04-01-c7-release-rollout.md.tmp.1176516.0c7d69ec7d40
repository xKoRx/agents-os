---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
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

# 2026-09-18-f05c-cert-f04-01-c7-release-rollout

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-18 — Release y rollout 0.2.101 (build 6182)` con veredicto `RELEASE/ROLLOUT PASS` + actualización de `Estado de entrada` + actualización de `Próxima tarea única recomendada para NORMAL`; CERT-F04-01 pasa a `BLOCKED / READY TO RERUN-4`)
  - `10-projects/Echo Forge/Echo Forge.md` (entrada de bitácora 2026-09-18)
  - `80-agents/journal/agent-runs/2026-09-18-zcode-glm-5.3-flash-f05c-cert-f04-01-c7-release-rollout.md` (creado)
  - Repo `xKoRx/symphony` — rama `codex/f05-release-prep` fast-forward `a440ac4…`→`c1d24c1…` en origin y release `0.2.101` publicada en MinIO (cambios de repo/flota documentados aquí, no en el vault)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-C7` (Approved Source → Release → Certified Fleet Rollout): el source aprobado C6+C6R (`c1d24c1…`, `SOURCE_READY`) exigía el gate Release Authority — publicar la release siguiente a `0.2.100` desde la rama productiva autorizada y desplegarla/certificarla en la flota completa. Sin ejecutar RERUN-4, sin repetir C5/C6/C6R, sin campañas, sin ETCD, sin IAM, sin tocar código de negocio.

## Fuentes usadas

- Mandato maestro F05C-CERT-F04-01-C7 (texto de la misión).
- Backlog deferred (estado vigente C6R), contrato [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]] (rama autorizada `codex/f05-release-prep`, dimensiones released/deployed), runbook `.agents/rules/12-watcher-and-deployer-services.md` y precedentes C2/C4 del backlog.
- Fixture auténtico FIX-B6182 en la copia privada de `daedalus` (13074872 B, SHA256 `21917e14…8b5c`) y CORPUS `FIX-AL-75` para el fixture de corpus `mt5-export.htm` (commit de autoridad `b5c71d5`, SHA `090ca4d1…`).
- `release-authority` (`sqx-release-authority.v1`), `deploy_release.sh --release-only`, evidencia Windows vía `AraneaEvidencePublish` + `mt5-kronos-operator` read-only (contrato [[aranea-ssh-mcp]]).

## Resolución aplicada

- Preflight git: descendencia exacta verificada (`bcf67be^` == `a440ac4…`, `c1d24c1^` == `bcf67be…`, sin commits intermedios); dirty foráneo preservado sin stage y sin overlap; policy resuelta por el contrato F-05-I — la rama feature no obtiene autoridad productiva; FF puro de `codex/f05-release-prep` a `c1d24c1…`, push y read-back (`ls-remote`).
- Release test gate desde el source a publicar: primera corrida exit 1 por 7 FAILs del corpus (`mt5-export.htm` ausente, defecto ambiental preexistente documentado); fixture recuperado byte-exacto del commit de autoridad como untracked; segunda corrida **exit 0 — 53 PASS / 0 FAIL / 0 SKIP / coverage 99.1%** con `SQX_MT5_REQUIRE_B6182_FIXTURE=1`, 7/7 crosschecks, regresión histórica PASS; gofmt/vet/build del scope limpios con hallazgos preexistentes demostrados idénticos en worktree del baseline `a440ac4`.
- Versión `0.2.101` resuelta por autoridad (`published_version=0.2.100`, `candidate_version=0.2.101`, `CONSISTENT`; sin release posterior que hubiera consumido los commits). Build/publicación canónica: 6 artifacts con `vcs.revision=c1d24c1…`; read-back `--target 0.2.101` → `EXACT_MATCH/CONSISTENT`.
- Rollout Stager canónico sin intervención manual: Zeus PID 2769428, Hera PID 1365120, Kronos PID 1328601 (todos `/opt/stager/releases/0.2.101/bin/symphony`, SHA `d795a998…` == artifact, poller ESTABLISHED, sin procesos `0.2.100`); worker-kronos PID 19436 @ `releases\0.2.101` (SHA `f5a8baa1…` == artifact, padre `stager-runtime` 35900, servicio Running/Automatic `.\kor`, CURRENT/PENDING `0.2.101`, singleton, evidence `partial=false` fresca). Invariante física preservada: `MT5_PHYS=0` antes y después; sin takeover; sin drenaje manual (nada activo que drenar).
- Deuda de seguridad registrada (no bloqueante): contraseña SSH publicada literalmente en el `AGENTS.md` del repo symphony (sección Inventario de Workers; valor NO reproducido aquí ni en ningún log/handoff). Acción owner: rotación de la credencial y saneamiento del documento. El Access Plane opera por identidad propia (`echo-dev`/keys), por lo que ningún gate del rollout se detuvo.

## Validación

- Git: `git merge --ff-only` limpio; push con read-back remoto exacto; sin force-push/rebase/squash; diff del delta limitado a los 7 archivos de C6+C6R.
- Tests: evidencia completa en `~/aranea/work/f04-cert-f04-01-c7/test-report-package.log` (53 PASS, coverage 99.1%, `-count=1` sin caché) y hashes en `artifact-hashes.txt`.
- Publicación: SHA256 recomputados == `deploy/manifest.json` == read-back de autoridad (`EXACT_MATCH`); `go version -m` de los 3 binarios con `vcs.revision=c1d24c1…`.
- Flota 4/4: certificación por host con CURRENT, PID, hash instalado == artifact, padre stager, poller y ausencia de versiones viejas; legado `symphony-f03-382f4ba` de Hera intacto y documentado como no blocker.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos (la credencial publicada NO se reproduce; sólo su ubicación y la acción de rotación)

## Rollback

- Repo: el FF de `codex/f05-release-prep` es avance puro de puntero sobre commits ya publicados; revertir el puntero no restaura nada roto (los commits C6/C6R siguen disponibles en `codex/f05-build6182-parser-cert`). Release: `0.2.101` no sobrescribió ninguna versión histórica; rollback de flota = publicar/restore de la versión anterior vía Stager (los hosts conservan `releases/0.2.100/` en disco). Vault: deltas append-only; revertir = eliminar el delta C7 del backlog, la entrada de bitácora, este log y el agent-run.
