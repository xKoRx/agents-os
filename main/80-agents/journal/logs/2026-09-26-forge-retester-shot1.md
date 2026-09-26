---
type: change_log
schema_version: 1
scope: session
created: "2026-09-26"
updated: "2026-09-26"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[2026-09-26-zcode-glm53-forge-retester-shot1]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[Session Feedback - 2026-09-26 - forge-retester-shot1]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge — Shot 1 Ranking→Retester bloqueado por producto + sync histórico flota EQUAL

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md` — bitácora 8.ª sesión (2026-09-26) + tarea C2 actualizada con causa raíz corregida y desbloqueo propuesto.

## Motivo

- Sesión Shot 1 (mandato owner con `OWNER_RETESTER_CFX`): el FlowRun `1a4d66d6` resultó no re-ejecutable (workflow Temporal wedged) y la causa raíz de C2 se corrigió con evidencia: el intento 2 (Hera, 25-sep 05:00Z) sí corrió el sqcli completo y falló en `persist_import_evidence` porque `CanonicalSymbol("NDX")` es vacío (instrumento del spec no-canónico) — no por la GUI como decía la continuidad de la 7.ª sesión. La corrección propuesta (alias `ndx→usatechidxusd` + re-despacho técnico wave1c) toca contrato de producto congelado y queda como decisión owner.

## Fuentes usadas

- Logs `/var/log/symphony/symphony-worker.log` de Hera/Zeus (25-sep 05:00Z / 04:52Z); código `sqx/core/evaluation/canonical_scope.go`, `sqx/adapters/overview/binding/evidence.go`, `sqx/adapters/registry-postgres/adopt_strategy.go`, `sqx/adapters/dispatcher-temporal/temporal_dispatcher.go`, `sqx/activities/watcher/import_intake.go` @ a95ef2c; flowkit RO (stages timeline); manifest sellado en MinIO; skill app-owned `sqx-instrument-sync`.

## Resolución aplicada

- Intermisión owner ejecutada: sync histórico `~/sqx/user/data` Zeus→Hera/Kronos EQUAL (hash maestro `07f1f285…` 3/3), previa reparación de host keys stale en Zeus (backup + re-add verificado por doble camino).
- Sin mutación de producto ni de identidades; intento de spec corregido limpiado al 100% (5 objetos MinIO borrados, staging restaurado, watcher detenido).

## Validación

- Audit/sync del script con manifests SHA-256 bit-a-bit; reconciliación 727/727 del freeze manifest; verificación de namespace MinIO limpio post-limpieza; 0 actividades de workers el 26-sep (descarta re-ejecución parcial).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Documental; revertir = restaurar el párrafo previo de la tarea C2 y eliminar la entrada de bitácora 8.ª. No aplica a infraestructura (todo efecto físico quedó en estado final deseado o limpiado).
