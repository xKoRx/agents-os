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
  - "[[2026-09-17-e06-t09b-c2-correction-freshness]]"
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

# 2026-09-17-e06-t10-bridge-emitter

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - Repo `xKoRx/echo` (externo, `feature/e06-reference-enrollment-binding` @ `891ab1d8`→`35db8b67`, push FF, sin merge/master): WP-C T10 — Bridge emitter zero-order + runtime attestations. Nuevo `v3/bridge/internal/reference_readback_emitter.go` (transformación verbatim `reference_status`→`REFERENCE_READBACK.v1`, coherencia de sesión login/rol, registration ref por receta congelada §7.2, received_at al ingreso con reloj inyectable, Validate pre-publish, `PublishSync` sobre el producer inyectado, key = `source_event_id`, errores propagados); hook único `case "reference_status"` en `ReferencePipeHandler.handleMessage` (+ campos/constructores emitter y reloj); nuevo `v3/bridge/internal/reference_readback_emitter_test.go` (27 tests: 7 canónicos TASKS + 20 negativos/de transporte con fake Kafka y fixture CONTRACT T09b). Detalle y gates en VERIFICATION.md §WP-C/T10.
  - `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/TASKS.md` y `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/VERIFICATION.md` — **actualizados**: párrafo WP-C T10 + checkbox `[x]` T10; sección §WP-C/T10 con evidencia.
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` — **actualizado**: Estado actual (bullet T10 al frente), tabla Entrega (`E06_T10_READY_FOR_MANAGER_REVIEW @ 35db8b67`), bitácora T10.
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-e06-t10-bridge-emitter.md` — **creada**.
  - `80-agents/journal/logs/2026-09-17-e06-t10-bridge-emitter.md` — **creada** (este log).

## Motivo

- Manager aprobó T09b C2 (`E06_T09B_APPROVED — RELEASE_T10`) y autorizó T10: el emitter que transporta el hecho físico `reference_status` del collector hacia el Gateway vía `echo.reference-readback.v1`, zero-order (KNOWN_EMPTY válido, sin exigir posiciones) y con atestaciones runtime retransmitidas verbatim. Matching/attribution queda en T11 (no autorizado).

## Fuentes usadas

- SPEC v1.2.2 §§7.1/7.2/7.2a/7.3 (`specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/SPEC.md`), TASKS.md (T10), VERIFICATION.md, código real @ `891ab1d8` (`reference_pipe_handler.go`, `messages.go`, `reference_readback.go`, `snapshots.go` topics, `messaging/producer.go`, `account_registry.go`, `pipe_manager.go`), golden CONTRACT T09b (`messages_test.go`).

## Resolución aplicada

- La autenticidad de procedencia no se inventa: la ruta vive sólo en el switch del `ReferencePipeHandler` (alcanzable sólo desde `handleSession` tras `WaitForConnection` de un pipe creado exclusivamente para cuentas `AccountTypeReference`) y el emitter exige coherencia entre el `account_login` observado y la cuenta vinculada al handler (`RegisteredAccount.AccountID()`, número de login decimal) y rol `reference`; contradicción ⇒ rechazo sin publicación. Sin sistema de autenticación nuevo.
- `received_at` se captura con el reloj UTC del Bridge en el límite de ingreso del hecho (top de `handleReferenceStatus`, antes del parseo) mediante seam mínimo `h.now` (default `time.Now`, inyectable en tests); un intento de publicación jamás lo refresca; el dedupe/replay permanece en Gateway/PostgreSQL (T09).
- Key Kafka determinista = `source_event_id` (identidad producer-assigned §7.1): el retry del mismo hecho converge a la misma key; sin IDs artificiales; IDs preservados en el payload.

## Validación

- `bridge/internal` PASS plain (0.474s) y `-race` (1.885s) con 27/27 tests T10; `sdk/domain` `-race` PASS; vet OK; builds sdk/bridge/gateway OK; failing sets `sdk+bridge+gateway` idénticos por nombre al baseline `891ab1d8` en worktree aislado (4 colaterales preexistentes infra-dependientes). CONTRACT+TRANSPORT+SOURCE PASS; PHYSICAL=PENDING (GAP-ECHO-006); MQL_COMPILE_C2=NOT_RUN (deuda heredada T09b C2, no resuelta por T10). SPEC diff 0; `go.mod`/`go.sum` diff 0; Gateway/Forge/MQL diff 0. Commit `35db8b67`, push FF `891ab1d8..35db8b67`, HEAD==origin, worktree limpio.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert 35db8b67` sobre `feature/e06-reference-enrollment-binding` (delta autocontenido: 2 archivos nuevos + hook + docs); el carril E-06 queda de nuevo en el estado aprobado `891ab1d8`.
