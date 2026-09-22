---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge — Import Task V1]]"
related:
  - "[[Echo Forge — Factory V2 Completion]]"
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

# 2026-09-21-forge-git-consolidation-two-branches

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/Echo Forge.md` (bullet de estado «TOP GIT CONSOLIDATION — 2 RAMAS» al tope de Estado actual + entrada de Bitácora 2026-09-21)
  - `10-projects/Echo Forge/Echo Forge — Import Task V1.md` (estado `PUBLISHED`, tabla de entrega con origin SHA, tareas G8 ajustadas, bitácora)
  - Repo `xKoRx/symphony`: `master` FF `0b9742b0→745bc8b94` (push sin force, read-back API `ahead=38 behind=0`); branch `feature/sqx-import-task-v1` publicada @ origin `5e495ae8878559e3ba8971421a26156dcfef040d` (5 commits, merge-base `745bc8b`); 5 tags anotados `archive/*` creados y pusheados; 21 ramas remotas históricas eliminadas; 3 ramas locales merged sin worktree eliminadas (`codex/f04-cert-f04-01-deadline-fix`, `codex/f04-cert-f04-01-encoding-fix`, `feature/f04-magic-version-handoff`)

## Motivo

- Mandato owner: consolidar el repo Symphony a exactamente 2 ramas (`master` = última estable certificada; `feature/sqx-import-task-v1` = único desarrollo activo) antes de continuar con la certificación física G7 de Import, preservando todo commit, documentación y trazabilidad.

## Resultado (verificado contra GitHub API)

- **MASTER:** `745bc8b94e1f6148ddc16c02eb86a755088c2666` (fast-forward puro desde `0b9742b09019526a8119f086199d15d1f0d42cb1`; checks del baseline sin regresiones — fallos zmq4/`Test_LoadEnvVars` ambientales e idénticos en `0b9742b`).
- **IMPORT:** local == remoto == `5e495ae`; scan de secretos/accidentales limpio (40 archivos, sólo specs/código/tests); sin commits de Import en `master`.
- **BRANCHES REMOTAS FINALES:** exactamente `master` + `feature/sqx-import-task-v1` (verificado `gh api repos/xKoRx/symphony/branches`).
- **ARCHIVED (mapping old_branch → SHA → permanent_ref):** `codex/f05-post-cert-delta`→`145d6be`→tag `archive/f05-post-cert-delta`; `codex/forge-explorer-v0`→`648d5e6`→tag `archive/forge-explorer-v0`; `codex/f05-r3-integration`→`3f6cd11`→tag `archive/f05-r3-integration` (7 commits NO contenidos — capturado por el chequeo de alcanzabilidad ANTES del borrado); `feature/e06-runtime-attestation-exporter`→`b738a6d`→tag `archive/e06-attestation-r1`; `feature/e06-runtime-attestation-exporter-r3`→`5d55c6b`→tag `archive/e06-attestation-r3` (contiene r2 `a1f62a6`). Lanes E-06: ownership documentado (track bloqueado `E06_T21_ARTIFACTS_SEALED_ENV_PENDING`), worktrees `symphony-e06-*` y ramas locales intactas.
- **LOST_COMMITS: 0** (22 SHAs inventariadas, todas alcanzables desde `master` ∪ `import` ∪ tags `archive/*`).
- **DEPLOYMENTS: sin cambios** (flota 4/4 en `0.2.105`; mover master no es deploy; workers intactos). **IMPORT_CERTIFICATION:** G7 sigue pendiente (runtime aislado, autoridad owner); MR-1/MR-2 pendientes de review.
- Dirty del checkout principal preservado sin commit (`deploy/manifest.json` registro deploy 0.2.96→0.2.105 + 2 artefactos de tests). Deuda de migración restante: secretos versionados en historial (historia intacta por diseño) y sdk `c7f1149` sin merge. Política vigente: una rama activa por desarrollo; no integrado = tag `archive/*` + baja de rama.

## Fuentes usadas

- Git de `xKoRx/symphony` (22 refs remotas, 17 locales, 20 worktrees, merge-bases, conteos de exclusividad), GitHub API (`branches`, `compare`, `tags`, `commits`), `gh pr list` (0 abiertos), sin tags/releases previos; checks de build/test en worktrees temporales `/tmp/symph-basecheck` y `/tmp/symph-oldmaster` (removidos).

## Resolución aplicada

- Verificación de alcanzabilidad ejecutada ANTES de cada borrado; el único falso candidato (r3-integration) se detectó y archivó con tag antes de eliminar. Ningún worktree ocupado perdió su rama local. Sin rebase/force/squash; `codex/f05-release-prep` contenida en el baseline; asociación release `0.2.105` conservada porque el tag-verdict vive en el historial ahora alcanzable desde `master`.
