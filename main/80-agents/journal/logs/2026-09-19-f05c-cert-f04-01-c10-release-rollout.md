---
type: change_log
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
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

# 2026-09-19-f05c-cert-f04-01-c10-release-rollout

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-19 — Delta de release y rollout CERT-F04-01 fix C9+C9R` con veredicto `RELEASE/ROLLOUT PASS` + actualización de `Estado de entrada` + actualización de `Próxima tarea única recomendada para NORMAL` (estado vigente tras C10, Consumidas ampliada con C9R y C10, próximo paso único = RERUN-5 sobre `0.2.102`/`66faa42…`); CERT-F04-01 permanece `BLOCKED / READY TO RERUN-5`)
  - `10-projects/Echo Forge/Echo Forge.md` (entrada de bitácora 2026-09-19 + Session checkpoint C10)
  - `80-agents/journal/agent-runs/2026-09-19-zcode-glm-5.3-flash-f05c-cert-f04-01-c10-release-rollout.md` (creado)
  - `xKoRx/symphony` — `codex/f05-release-prep` fast-forward `c1d24c1…`→`66faa42debba18cd0dd09de127ae1374ea2a07f0` en origin (sin commits nuevos, push sin force) + release `0.2.102` publicada en MinIO vía `./deploy_release.sh --release-only 0.2.102` (6 artifacts + manifest; efectos documentados aquí y en el delta C10)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-C10` (Release Engineer): el manager aprobó el source C9+C9R; integrar el rango aprobado, publicar la release siguiente a `0.2.101` con el mecanismo canónico y desplegarla en los cuatro hosts con evidencia viva, sin ejecutar RERUN-5 ni campañas.

## Fuentes usadas

- Mandato maestro F05C-CERT-F04-01-C10 (baseline `c1d24c1…`, SHA aprobado `66faa42…`, gates G0–G5, prohibiciones, formato de handoff).
- Delta C9/C9R del backlog y checkpoint C9/C9R de [[Echo Forge]]; delta C7 (runbook canónico de release y rollout); skills app-owned `sqx-deployer` y `anti-test-masking-guard`; autoridad viva `sqx-release-authority.v1` vía `release-authority`; runbook `aranea-ssh-mcp.md` (contrato del evidence publisher Windows).

## Resolución aplicada

- G0: fast-forward puro `c1d24c1..66faa42` en el checkout principal (dirty operacional preservado sin stage), push sin force y read-back `ls-remote == 66faa42…` en ambas ramas; rango verificado 2 commits / 7 archivos (845+/9−).
- G1: suites `-count=1` en worktree limpio `66faa42` con fixture auténtico `mt5-export.htm` restaurado byte-exacto desde el commit de autoridad `b5c71d5` (SHA `090ca4d1…`, untracked, sin cambio al repo); comparación contra baseline `c1d24c1` en worktree temporal hermano — `sqx/workflows` 21 fallos idénticos por nombre y causa normalizada (16 harness sin `flow_run_start` + 5 simulación MT5; normalización del orden no determinista del sufijo `Supported types`), `activities/worker` y `core/runtime` PASS completos; tests C9/C9R PASS por nombre; release test gate 53/53 / 0 skips / coverage 99.1%; gofmt/vet limpios; builds con los 2 fallos preexistentes documentados; anti-test-masking PASS (805+/0−).
- G2: preflight `release-authority` CONSISTENT con candidato resuelto `0.2.102`; publicación canónica EXIT=0; 6 SHA256 == manifest; `vcs.revision=66faa42` en 3 binarios; read-back `EXACT_MATCH/CONSISTENT`; releases históricas 0.2.100/0.2.101 byte-intactas; sin FlowRun (`--release-only`).
- G3/G4/G5: preflight con `sqx-prop` Running = 0 (visibilidad gRPC directa, scratch `/tmp/thist`); rollout Stager 4/4 — Zeus PID 2801657 / Hera PID 1390690 / Kronos PID 1353062 / Windows PID 6648 — todos con SHA instalado == artifact, poller ESTABLISHED, singleton Windows `COUNT=1`, evidencia inspector `partial=false` en dos ciclos, `MT5_PROCS=0` fresco, cero residuos de versiones anteriores, releases históricas intactas y cero workflows iniciados desde 20:25Z; sin campañas ni RERUN-5; allocations `26090011001–009` intactas.

## Validación

- Cadena independiente verificada: `66faa42` (read-back remoto) → release `0.2.102` (`EXACT_MATCH/CONSISTENT`) → manifest (6 hashes) → artefactos (SHA256 recomputados) → ejecutables efectivos en los 4 hosts (SHA instalado == artifact, PIDs y log lines `Started Worker Namespace sqx-prop`). `MT5_PROCS=0` con singleton preservado. Worktree temporal del baseline eliminado sin residuo; workdir de la misión con logs de publicación, listas de fallo fix/baseline, causas normalizadas y hashes.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, sin credenciales ni secretos; la contraseña SSH expuesta en el `AGENTS.md` del repo symphony permanece como deuda documentada en el delta C7 (no reproducida; el rollout se ejecutó íntegramente por las identidades del Access Plane).

## Rollback

- La rama productiva de release quedó en `66faa42…` (FF sobre `c1d24c1…`): revertir = re-alinear `codex/f05-release-prep` a `c1d24c1…` y republicar manifest `0.2.101` (la flota convergería de vuelta; los PENDING/CURRENT son reversibles por el mismo mecanismo Stager). Las releases `0.2.100`–`0.2.102` coexisten en el registry y los hosts retienen los directorios de release anteriores, por lo que el rollback de runtime no requiere reconstruir artifacts. Vault append-only (revertir = eliminar el delta C10, la entrada de bitácora/checkpoint, este log y el agent-run).
