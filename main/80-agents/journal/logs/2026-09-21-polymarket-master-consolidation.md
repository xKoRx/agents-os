---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[u02-v2-cash-confirmed]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
  - "[[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]]"
  - "[[2026-09-21-u02-v2-authority-register]]"
aliases:
  - "Polymarket master consolidation 2026-09-21"
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
  - area/personal
  - project/polymarket-engine
---

# 2026-09-21-polymarket-master-consolidation

## Cambio

- **Tipo:** updated (notas canónicas) + created (este change log + agent run) + publicación Git del engine.
- **Archivo(s):**
  - `main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`
  - `main/10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md`
  - `main/30-resources/polymarket/Polymarket Engine — Five-POC Guía Operativa 2026-09-20.md`
  - `main/30-resources/polymarket/00-index.md`
  - `main/30-resources/polymarket/log.md`
  - `main/00-inbox/U-02 V2-CASH-CONFIRMED — handoff consolidación.md`
  - repo engine: `master`/`main` @ `a770da6` (recibo `testdata/research-master/`)

## Motivo

Mandato owner one-shot: consolidar Polymarket Engine en `master` como única rama canónica de desarrollo aceptado, integrar Five-POC verificable, absorber U-02 sin mergear `d5ce263`, recertificar M4 sobre el SHA integrado y publicar sin live.

## Fuentes usadas

- Checkout físico: `feature/five-poc-integration@85e27ff`, `origin/main@9ae5dde` (ancestro), U-02 `d62768a`/`d5ce263`.
- Decisión [[u02-v2-cash-confirmed]] y handoff de inbox.
- Sports E2 ya entregado en continuidad §12 (`NO_SIGNALS_IN_SAMPLE`, cero código).

## Resolución aplicada

- Creada y publicada `master` desde Five-POC. Recertificación M4 no-live **en `85e27ff`** (27/0/0/5); commit de recibo `a770da6`. Default GitHub = `master`. `main` fast-forward al mismo SHA.
- Excluido `d5ce263` (`PATCH_NOT_ACCEPTED_FOR_V2`). Evidencia v08 + tag `archive/u02-patch-not-accepted-for-v2`. `REAL_FEE_READY=false`.
- Sports: research entregado, sin código que integrar; worktree `feature/five-poc-integration` conservado.
- Worktrees POC/shared/U-02 eliminados tras verificar ancestría o respaldo.

## Validación

- `go build` / `go vet` / `go test ./... -count=1` / `go test ./... -race -count=1` PASS en `85e27ff`.
- `engine experiment certify --profile no-live --baseline 85e27ff` → `M4_CERTIFIED_NON_LIVE`.
- `git push` fast-forward; `origin/HEAD` → `master`; sin force-push.
- Graphify `NOT_RUN`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin wallet, secretos ni órdenes

## Rollback

Revertir notas del vault. En engine: `master`/`main` apuntan a `a770da6`; un rollback de default branch a `main` no cambia el código (mismo SHA). No restaurar `d5ce263` sobre la línea canónica.
