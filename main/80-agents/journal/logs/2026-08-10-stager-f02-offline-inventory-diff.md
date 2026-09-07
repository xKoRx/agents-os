---
type: change_log
schema_version: 1
scope: session
created: 2026-08-10
updated: 2026-08-10
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[Stager]]"
  - "[[Echo Forge]]"
related:
  - "[[2026-08-10-stager-f01-readonly-capture-blocked]]"
  - "[[2026-08-10-stager-f02-offline-inventory-raw]]"
  - "[[stager-go-requires-current-pending-bridge]]"
  - "[[stager-go-noop-pending-sync-thrash]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-10-stager-f02-offline-inventory-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/echo
---

# Stager F0.2 offline inventory / diff redacted

## Cambio

- **Tipo:** created / research evidence
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - este change_log (inventario/diff redacted F0.2)

## Motivo

- F0.2 exige normalizar la captura offline, compararla contra runbook/repo y producir inventario/diff redacted; escalar contradicciones.

## Fuentes usadas

- [[2026-08-10-stager-f01-readonly-capture-blocked]] / raw F0.1 — captura host = vacía (SSH BLOQ).
- Runbook `docs/deployment/stager-publisher-integration.md` (repo Symphony) — sección Fleet cutover `0.2.40`.
- Checkout Stager (`repo: stager`) — árbol offline, git sin commits/remote.
- Ejemplos versionados Symphony `deployer/doc/examples/client/symphony-stager*` — **no** autoridad de host.
- Known errors [[stager-go-requires-current-pending-bridge]] y [[stager-go-noop-pending-sync-thrash]].

## Resolución aplicada

### Oráculo PASS/FAIL

| Chequeo | Resultado |
|---|---|
| ¿Existe captura F0.1 por host (6 clases × Zeus/Hera/Kronos)? | **FAIL** — 0 artefactos de host |
| ¿Wrapper Go productivo versionado en repo Stager o ejemplos Symphony? | **FAIL** — ABSENT |
| ¿Checkout Stager recuperable (commit + remote)? | **FAIL** — sin commits / sin remote |
| ¿Inventario/diff redacted emitido y contradicciones escaladas? | **PASS** — este documento |

### Matriz host — captura observada (normalizada)

Clases requeridas por F0.1: binario, wrapper, env redacted, units/timers, permisos, layouts.

| Host | binario | wrapper | env | units/timers | permisos | layouts |
|---|---|---|---|---|---|---|
| Zeus | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT |
| Hera | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT |
| Kronos | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT |

No se inventó estado desde ejemplos ni desde cutover histórico.

### Esperado (runbook / cutover docs) vs repo — diff redacted

| Componente | Esperado productivo (runbook cutover) | Repo Stager | Ejemplos Symphony | Diff |
|---|---|---|---|---|
| Binario Go | `/usr/local/bin/stager` | `cmd/stager` (fuente); sin artifact linux empaquetado en árbol | n/a | fuente ≠ install path verificado en host |
| Wrapper bridge | `/usr/local/sbin/symphony-stager-go` | **ABSENT** | **ABSENT** (solo Bash `symphony-stager`) | **C2** fuera de repo |
| Bash backup | `symphony-stager.bash.bak` | ABSENT | script Bash de ejemplo | producción ≠ ejemplo versionado |
| Unit | `symphony-stager.service` → wrapper Go | ABSENT | `ExecStart=/usr/local/sbin/symphony-stager` (Bash) | **C5** ejemplos ≠ cutover |
| Timer | presente (periodo efectivo desconocido sin captura) | ABSENT | `OnUnitActiveSec=30s` (desc. dice 5 min) | **C6** inconsistencia ejemplo |
| Env keys (redacted) | STAGER_* / MinIO (valores no capturados) | `.env.example` keys locales | `MINIO_*`, `MANIFEST_KEY`, … | schemas distintos; sin valores de host |
| Layout root | `STAGER_ROOT=/opt/symphony` + `current` + `/var/lib/symphony/PENDING` | layout MVP `releases/`, `CURRENT`, `PENDING` bajo root configurable | FHS Bash `current` + PENDING legacy | bridge proyecta legacy; core no versiona wrapper |
| Release flota | `CURRENT=0.2.40` (claim cutover) | n/a | n/a | **C4** no verificable sin F0.1 |

### Inventario offline repo Stager (sin secretos)

- Specs: sólo `specs/STAGER-MVP/` — **no** existe aún `specs/STAGER-DEPLOYMENT-LIFECYCLE/`.
- Docs: `ARCHITECTURE.md`, `MANIFEST.md`, `SYMPHONY.md`.
- Core: `internal/staging/{runner,state,lock}_*`, `internal/manifest`, `internal/source`.
- Git: working tree sin commits; remote vacío; `.env` local ignorado en este inventario (no se leyeron valores).

## Contradicciones escaladas

1. **C1 CRITICAL** — Precondición F0.1 fallida: sin captura host no hay diff live; F0.3/G0 no deben asumir verdad de flota.
2. **C2 HIGH** — Wrapper `symphony-stager-go` es autoridad productiva documentada y está fuera de repositorio (Stager y ejemplos Symphony).
3. **C3 HIGH** — Checkout Stager no es baseline Git recuperable (gate P0 del proyecto).
4. **C4 MEDIUM** — Claim cutover `CURRENT=0.2.40` / workers `active` no contrastable hoy.
5. **C5 MEDIUM** — Ejemplos Bash (`ExecStart` → `symphony-stager`) divergen del cutover Go+bridge; no sustituyen captura.
6. **C6 LOW** — Ejemplo timer: descripción “5 min” vs `OnUnitActiveSec=30s`.

## Validación

- Búsqueda de artefactos F0.1 de host: ninguno.
- `find`/`rg` offline: `symphony-stager-go` ausente en Stager y en ejemplos client; sólo aparece en runbook/docs de cutover.
- `git status` / `git remote` / `git log` en checkout Stager: sin commits ni remote.
- Cero mutaciones de host; cero secretos en este documento.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales, valores de env, outputs de host ni paths absolutos de máquina local.

## Rollback

- Revertir este change_log y el estado F0.2 del planificador si una captura F0.1 posterior invalida el inventario vacío; no hay cambios de runtime que revertir.
