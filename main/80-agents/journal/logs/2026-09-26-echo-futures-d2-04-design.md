---
type: change_log
schema_version: 1
scope: session
created: "2026-09-26"
updated: "2026-09-26"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
related:
  - "[[Echo Futures — D1 Analysis Pack]]"
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
  - area/echo
  - echo-futures
---

# 2026-09-26-echo-futures-d2-04-design

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures — D2-04 Operation Order Fill Position.md` (nuevo artefacto durable del workstream D2-04, commit `db7f46c8`).
  - `80-agents/journal/sessions/2026-09-26-echo-futures-d2-04-design-summary.md`, `80-agents/journal/feedback/system-1/2026-09-26-echo-futures-d2-04-session-feedback.md`, este change_log.

## Motivo

- Ejecutar el workstream D2-04 del milestone D2 de Echo Futures: diseño V1 de `Operation / Order / Fill / Position` (dominio + runtime) como artefacto autosuficiente para Primary Manager review.

## Fuentes usadas

- [[Echo Futures]] (decisiones owner D2-01/02/03 y lifecycle A2), [[Echo Futures — D1 Analysis Pack]] (baseline D1 aceptada), Environment Contract Echo/Forge, y source físico `xKoRx/echo@372af59a` verificado por esta sesión (paths y blob SHAs en §14 del artefacto).

## Resolución aplicada

- Diseño completo con veredicto `D2-04 STATUS = READY_FOR_MANAGER_REVIEW` y `OWNER DECISIONS REQUIRED: NONE`; no se modificó la nota canónica del proyecto ni las decisiones owner (la integración del gate queda al Primary Manager).

## Validación

- Baseline física verificada (`git fetch` + `origin/master = 372af59a…`, sin delta); inspección de cada pieza relevante vía `git show` sobre el SHA exacto; casos de aceptación A–G del mandato resueltos en el artefacto.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos (los paths de workspace externo citados son convención de campaña ya pública en la entidad).

## Rollback

- Revert del commit `db7f46c8` y commits de cierre; sin efectos laterales fuera del vault (ningún runtime ni repositorio productivo fue tocado).

---

# 2026-09-26 — Echo Futures D2-04 repair (R1–R9)

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures — D2-04 Operation Order Fill Position.md` (repair en el mismo archivo, sin variantes paralelas; capturado por sync en commit `89a089ed`).

## Motivo

- `D2_04_MANAGER_REVIEW = CORRECTION_REQUIRED` con 9 defectos concretos (R1–R9) registrados por el Primary Manager en [[Echo Futures]].

## Resolución aplicada

- R1 sin referencias versionadas del binding (D2-01); R2 direction desde el OPEN Signal antes de MM/Orders; R3 ForceClose como intent de terminación con guards uniformes; R4 fill truth jamás clamped + `EXPOSURE_INVARIANT_BREACH` fail-visible; R5 separación conmutatividad-de-hechos vs decisiones-stateful + `operation_event_seq`; R6 crash window cerrada con egress StateFun 3.2 `EXACTLY_ONCE` (2PC documentada, Javadoc oficial) + dedup de adapter por `client_order_id`; R7 dedup de fills con horizonte = vida de la Operation (sin TTL); R8 Position reclasificada REUSE pattern / REPLACE shape (proyección neta por account+contract); R9 superficie reducida (sin tablas de eventos, sin router, sin store function: 2 funciones, 2 ingress, 1 egress, 4 tablas PG).

## Validación

- Baseline re-verificada por fetch (`origin/master = 372af59a…`, sin delta); garantía egress citada del Javadoc oficial de `KafkaEgressBuilder` 3.2 con URL en §14; runtime desplegado confirmado `apache/flink-statefun:3.2.0` (docker-compose); casos 1–8 del mandato resueltos; grep de contradicciones internas limpio.

---

# 2026-09-26 — Echo Futures D2-04 second repair (R10–R13)

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures — D2-04 Operation Order Fill Position.md` (second repair en el mismo archivo; commit `57e09436`).

## Motivo

- `D2_04_MANAGER_REVIEW_2 = CORRECTION_REQUIRED` con 4 defectos de correctness (R10–R13) registrados por el Primary Manager en [[Echo Futures]].

## Resolución aplicada

- R10 contrato restart-safe de idempotencia de efectos externos del adapter: journal durable write-ahead + resolución de `PENDING` ambiguos contra venue (open + history por client tag o idempotencia nativa) con gate `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION`; dos boundaries EXACTLY_ONCE explícitos (state↔egress vs adapter↔venue). R11 autoridad de recovery congelada: checkpoint Flink + replay Kafka; PG proyección eventual/query-only stale-safe; `COLD_RECOVERY_REQUIRED` fail-closed para desastre frío. R12 claim de replay reducido a propiedad de dominio; `operation_event_seq` = runtime ordering/stale protection/provenance; seam de recorded streams → workstream Market/Replay. R13 guard de identidad (`operation_id` en events vs `current_operation_id`) + late-event path: duplicados viejos por PK PG, fills nuevos tardíos como hechos + `POST_TERMINAL_EXECUTION_BREACH`, sin tombstones, sin tocar la sucesora.

## Validación

- Baseline re-verificada (fetch, sin delta); invariantes I13–I15 añadidas; casos A–F del mandato resueltos; grep de contradicciones limpio (eliminadas referencias residuales a recovery desde PG y al registry RAM del primer repair).

---

# 2026-09-26 — Echo Futures D2-04 final durability repair (R14)

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures — D2-04 Operation Order Fill Position.md` (R14 en el mismo archivo; capturado por sync en commit `bbb7ff27`).

## Motivo

- `D2_04_MANAGER_REVIEW_3 = FINAL_CORRECTION_REQUIRED`: ventana de pérdida entre checkpoint StateFun (que avanza el offset de ingress) y el writer PG embebido — un Fill checkpointeado pero no flusheado a PG quedaba sin fuente durable, contradiciendo `Fill = immutable durable fact`.

## Resolución aplicada

- R14: `echo/operation` deja de tener writer PG embebido y emite `OPERATION_SNAPSHOT` / `ORDER_SNAPSHOT` / `FILL_FACT` por el mismo egress Kafka transaccional EXACTLY_ONCE (misma frontera atómica con el checkpoint) hacia `echo.operation-projections.v1`; nuevo projector dedicado `echo/operation_projector` materializa PG asincrónicamente (idempotente, stale-safe por seq; FILL_FACT insert-only por identity natural). R13 migrado al fact path durable (FILL_FACT con flag `post_terminal`; breach definitivo lo levanta el projector al materializar, telemetría Core inmediata como candidato). Invariante I16 añadida; superficie final: 2 funciones de estado + projector + position projector, 2 familias de egress transaccional, 4 ingress, 4 tablas PG. Sin event sourcing, sin tablas de eventos, `mm_state` no viaja en el topic.

## Validación

- Casos A–D del mandato (fill antes de crash, checkpoint abortado, PG caída 30 min, late fill post-terminal) resueltos en §13; grep de contradicciones limpio (sin referencias residuales al writer embebido como fuente durable); la garantía EXACTLY_ONCE citada (Javadoc 3.2) aplica a ambos egress; baseline `372af59a` sin delta.



