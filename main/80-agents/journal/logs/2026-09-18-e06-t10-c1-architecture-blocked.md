---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
application:
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
related:
  - "[[2026-09-18-e06-t10-replay-stop]]"
  - "[[2026-09-17-e06-t10-bridge-emitter]]"
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

# 2026-09-18-e06-t10-c1-architecture-blocked

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` — **actualizado**: bitácora 2026-09-18 con el resultado CORRECTION_C1 (`E06_T10_C1_ARCHITECTURE_BLOCKED`), invalidación explícita del STOP anterior (interpretó incorrectamente el baseline) y estado actual del proyecto actualizado al bloqueo pendiente de decisión Manager.
  - `80-agents/journal/agent-runs/2026-09-18-zcode-glm-5.3-flash-e06-t10-c1-architecture-blocked.md` — **creada**.
  - `80-agents/journal/logs/2026-09-18-e06-t10-c1-architecture-blocked.md` — **creada** (este log).
  - Repo `xKoRx/echo` — **intocado** (RUTA B §15: 0 commits, 0 push, worktree devuelto limpio a `35db8b67`; los tests temporales de reproducción se eliminaron).

## Motivo

- El Manager emitió `E06_T10_BLOCKED — CORRECTION_C1`: el STOP del 2026-09-18 interpretó incorrectamente el baseline (el commit `35db8b67` es la entrega T10 publicada y el baseline obligatorio de la corrección, no drift). El defecto a resolver: `received_at` sellado por recepción en Bridge T10 vs digest contractual T08 vs deduplicación append-only T09 — una retransmisión legítima del mismo hecho físico produce digest distinto y `CONTRACT_CONFLICT`.

## Fuentes usadas

- Worktree `/tmp/echo-e06-reference-enrollment` @ `35db8b67`: emitter/handler T10, `reference_readback.go` (T08), `reference_readback_store.go` (T09), migration 064, SPEC v1.2.2 §7.1/§7.2, tests T09/T10.
- Reproducción ejecutable: camino real handler→emitter con reloj inyectado (test temporal) y `ReferenceReadbackStore.Insert` real sobre PostgreSQL 17.11 descartable (cluster efímero `/tmp/e06-pg17/data-c1repro`, schema por `run.sh` PASS).
- Mandato E06_T10_C1 (2026-09-18) y veredicto Manager.

## Resolución aplicada

- Hipótesis CONFIRMADA (CONTRACT y PG REAL): S preservado, T1≠T2 ⇒ D1=`sha256:d12df650…` ≠ D2=`sha256:d0d4b07f…`; con received_at igualado D1==D2 (único campo divergente). PG REAL: Insert R1 `created=true`; Insert R2 ⇒ `CONTRACT_CONFLICT (same source_event_id, different payload)`; 1 fila; Caso F ⇒ `CONTRACT_CONFLICT` (conflicto verdadero intacto); replay exacto converge.
- Matriz A–F: A y E convergen (mismo objeto/mismo mensaje ⇒ mismo digest; dedupe T09); B/C/D caen en el defecto; F preserva conflicto. Alternativas 1–5 analizadas: ninguna integral sin alterar autoridad (T08/T09 READ ONLY, boundary sin-PG de Bridge congelado, protocolo collector sin instante de primer ingreso).
- Decisión: RUTA B — `E06_T10_C1_ARCHITECTURE_BLOCKED`. Cero implementación, cero commit. Cambio mínimo requerido para el Manager: (i) redefinir la equivalencia de replay excluyendo `received_at` de la vista de digest (T08) Y de la comparación canónica (T09) — decisión contractual con efecto a revisar sobre el dedupe cross-ID de `uq_e6_readbacks_payload_digest`; o (ii) alterar el boundary para que el owner durable selle/recupere el primer `received_at` (p.ej. Gateway como primer punto durable, cambiando §7.1 «primer Bridge UTC»). Recomendación técnica: (i), por un solo lugar de verdad y sin storage nuevo.

## Validación

- `run.sh` PASS completo (rebuild 001–063 + 064 + aserciones + up/down/up). Reproducciones CONTRACT y PG REAL PASS con distinción explícita. Post-limpieza: `git status` limpio, `git diff` vacío, HEAD `35db8b67` == origin. Cluster PG descartable detenido.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No aplica: el repo Echo quedó sin cambios; revertir el registro = eliminar este log, el agent_run y revertir la edición de la entidad.
