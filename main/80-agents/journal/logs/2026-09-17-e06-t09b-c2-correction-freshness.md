---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
application:
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
related:
  - "[[2026-09-17-e06-t09b-c1-correction-mql-compile]]"
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

# 2026-09-17-e06-t09b-c2-correction-freshness

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - Repo `xKoRx/echo` (externo, `feature/e06-reference-enrollment-binding` @ `fc2d4e5d`→`891ab1d8`, push FF, sin merge/master): corrección C2 T09b — C2-1 elegibilidad del retry rollover-safe fail-closed (marcas `ulong`→`uint`, resta modular 32 bits, reloj grueso `TimeGMT()` sólo descalifica, gate build→primera escritura) y C2-2 `outOldestRemainMs` sólo de slots realmente incorporados al snapshot; 3 tests C2 nuevos en `v3/sdk/domain/messages_test.go` + actualización del pin C1 del mínimo. Archivos: `v3/clients/mt{5,4}/reference_v3.mq{5,4}`, `v3/clients/mt{5,4}/EchoCommon.mqh`, `v3/sdk/domain/messages_test.go`, `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/TASKS.md`, `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/VERIFICATION.md`. Detalle y gates en VERIFICATION.md §WP-C2 CORRECTION C2.
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` — **actualizado**: Estado actual (bullet C2 al frente), tabla Entrega (`E06_T09B_C2_READY_FOR_MANAGER_REVIEW @ 891ab1d8`), bitácora C2.
  - `80-agents/journal/logs/2026-09-17-e06-t09b-c2-correction-freshness.md` — **creada** (este log).

## No cambió

- SPEC v1.2.2, PLAN, `messages.go`, contrato T08, migration 064, Gateway, Bridge, Forge, stores, `go.mod`/`go.sum` — diff 0. Identidad durable C1-1 intacta (4 tests C1 en verde).
- MQL_COMPILE=NOT_RUN en C2: host `mt5-kronos.lab.aranea.cl` sin path de acceso ejecutable en esta sesión (publickey denegada para todas las identidades locales; la key temporal de C1 fue revocada post-uso); bloqueo documentado, no PASS inventado. Los binarios ex5/ex4 de C1 no se reutilizan como evidencia C2.
