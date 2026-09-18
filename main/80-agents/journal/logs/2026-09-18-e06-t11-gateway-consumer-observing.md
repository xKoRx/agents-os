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
  - "[[2026-09-18-e06-t10-c2-replay-equivalence]]"
  - "[[2026-09-18-e06-t10-c1-architecture-blocked]]"
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

# 2026-09-18-e06-t11-gateway-consumer-observing

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - Repo `xKoRx/echo` branch `feature/e06-reference-enrollment-binding` — **commit único `25bde646e9cd75d917bfa7e4fc6206128fabec3c`** sobre el baseline obligatorio `b13eb2763bff579d1bfe85339b5a5ddac7db2555` (parent exacto), push FF `b13eb276..25bde646` (remoto compatible, sin avance concurrente), working tree limpio. Delta = 10 archivos: `v3/gateway/internal/enrollment_service.go` (nuevo — matching §7.3 fail-closed, transiciones idempotentes vía stores T09/T02 existentes, atribución write-once UNBOUND→MATCHED/MATCH_FAILED, COLLECTOR_CONFLICT §7.5 con precedencia), `v3/gateway/internal/enrollment_service_test.go` (nuevo — 18 tests incluidos los 10 obligatorios TASKS), `v3/gateway/internal/reference_readback_consumer.go` (nuevo — consumer `echo.reference-readback.v1` con lifecycle New→Start→Stop y clasificación contractual/operacional), `v3/gateway/internal/reference_readback_consumer_test.go` (nuevo — fake Kafka + 6 tests de consumer), `v3/gateway/internal/server.go` (arranque/shutdown del consumer en el ciclo de vida del server, sólo con PG), `v3/gateway/cmd/echo-gateway/main.go` (autorización adicional Manager — SaramaConsumer con DI existente, group dedicado `echo-gateway-v3-reference-readback`, earliest), `v3/sdk/messaging/kafka_consumer.go` (**expansión acotada demostrada**: `ConsumeClaim` dejaba de marcar el offset ante error del handler y abandonaba la claim — el código anterior confirmaba trabajo durable fallido violando el contrato propio de `MessageHandler`; pineado por tests), `v3/sdk/messaging/kafka_consumer_test.go` (nuevo — 3 contract tests con session/claim sarama falsos), `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/TASKS.md` y `VERIFICATION.md`. Migration 064, contracts, `reference_readback.go`, stores T09/T02, Bridge, MQL, `go.mod`/`go.sum` diff 0.
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` — **actualizado**: nuevo estado `E06_T11_READY_FOR_MANAGER_REVIEW` al inicio de "Estado actual", fila de entrega actualizada @ `25bde646`, tarea WP-C pasada a `[r]`, bitácora 2026-09-18 con la implementación T11 y evidencia.
  - `80-agents/journal/agent-runs/2026-09-18-zcode-glm-5.3-flash-e06-t11-gateway-consumer-observing.md` — **creada**.
  - `80-agents/journal/logs/2026-09-18-e06-t11-gateway-consumer-observing.md` — **creada** (este log).

## Evidencia

- Gates (PostgreSQL 17.11 descartable, cluster efímero recién initdb'd puerto 55441 + fake Kafka): harness migration 064 PASS up/down/up; T11 24/24 PASS incluido `-race` (`gateway/internal`, `sdk/messaging`); failing sets por nombre idénticos al baseline puro `b13eb276` en worktree aislado `/tmp/echo-e06-baseline-t11` (gateway 29=29, postgres 53=53 — colaterales preexistentes); regresiones T09/T10 intactas (`TestReadback_` 12/12 `-race`, `TestEmitter_` PASS, `sdk/domain` `-race` PASS); vet OK; builds gateway/sdk/bridge/core OK; `git diff --check` limpio; `go.mod`/`go.sum` delta 0. Detalle completo en `VERIFICATION.md` §T11.
- Deudas heredadas intactas: PHYSICAL=PENDING (GAP-ECHO-006 — los tests CONTRACT no certifican físico); MQL_COMPILE_C2=NOT_RUN (deuda T09b).
- Observación reportada al Manager (no corregida en esta sesión para no expandir scope): `VERIFICATION.md` @ `b13eb276` contiene duplicada la sección "T10 CORRECTION C2" (mismo encabezado y párrafo inicial dos veces seguidas).

## Estado resultante

- `E06_T11_READY_FOR_MANAGER_REVIEW` — pendiente de Manager review de T11. E-06 NO CLOSED; T12–T22 no iniciados; siguiente gate: Manager review + preparación del paquete T12–T20.
