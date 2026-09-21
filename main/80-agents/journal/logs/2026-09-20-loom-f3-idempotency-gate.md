---
type: change_log
schema_version: 1
scope: session
created: 2026-09-20
updated: 2026-09-20
area: "[[Personal]]"
project: "[[Loom]]"
application:
entities:
  - "[[Loom]]"
related:
  - "[[Loom — Foundation v0.1]]"
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

# 2026-09-20 — Loom F3: ledger durable de identidades (idempotency gate)

## Cambio

- **Tipo:** updated (bitácora de `10-projects/Personal/Loom/Loom.md`) + registro de ejecución.
- **Archivo(s):** `main/10-projects/Personal/Loom/Loom.md`; este change_log; agent-run del mismo día.
- **Código (fuera del vault):** rama `feature/f3-idempotency-gate` del repo `xKoRx/loom`, publicada en origin @ `04a3ae8` (base `feature/f3-ux-lab @ 47cbadb`; commits `8196165`, `79ec14f`, `04a3ae8`). Sin merge a master ni a v0.6.

## Motivo

- El mandato "Loom F3 / Durable Request Ledger" ordenó cerrar el bloqueante §5.B identificado en G3: la destrucción física de un registro del journal permitía que un retry con el mismo `requestId` re-aplicara una operación; el ledger del navegador no es garantía de producto.

## Contenido

- Ledger durable de identidades del lado servidor (`poc/f3writer/ledger.go`): reserva fsync-ada previa a cualquier aplicación, máquina de estados `reserved→prepared→applied | recovery_required`, flock por identidad, reconstrucción con evidencia inequívoca, fail closed, GC con retención y arbitraje audit+contenido.
- Regresiones L01–L21 (21/21) con SIGKILL real; corrección de los hallazgos P0/P1 de dos auditorías independientes (Agente A: revisión; Agente B: adversarial con exploits demostrados y luego bloqueados).
- `specs/FEAT-F3-IDEMPOTENCY/RESULTS.md` en la rama con diseño, veredictos, gates, garantías y límites.

## Impacto

- Ningún cambio en el binario productivo (read-only; aislamiento `go list -deps ./cmd/loom` = 0), sin endpoints POST productivos, sin `--allow-write-plan`, v0.6 intacta. La habilitación de producto (G4/G5) sigue pendiente del owner.
