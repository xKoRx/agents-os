---
log_type: change_log
scope: local
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
created: 2026-09-17
tags:
  - kind/change-log
  - area/echo
  - project/agentsos
---

# 2026-09-17 — E-06 NORMAL WP-A corrección C1 (T01–T03) registrada

## Cambios

- **Entidad Sistema 2 actualizada:** [[Echo — E-06 Reference Enrollment and Binding]] — nuevo bullet de estado `E06_WPA_C1_READY_FOR_MANAGER_REVIEW`, tabla de entrega de desarrollo con commit `c021983f`, bitácora con evidencia completa. La tarea WP-A permanece `[r]` (Review; gate Manager pendiente).
- **Repo `xKoRx/echo`:** commit `c021983f` en `feature/e06-reference-enrollment-binding`, push FF `429e5c03..c021983f` sobre origin, sin merge ni master. Delta de 9 archivos allowed: `064_reference_enrollment_binding.up.sql`, `reference_binding_store.go` + test, `tests/reference_binding_e6/{10,12,13,14}_*.sql`, TASKS.md, VERIFICATION.md. Contracts y 061–063 diff 0; `TEST_CHANGE_REQUEST.md` intacto.

## Correcciones (Manager audit de `429e5c03`)

- **C1-1:** `uq_e6_overlap_live` retiene la overlap key también en SUSPENDED; liberación = CLOSED + inventario vacío.
- **C1-2:** DRAINING→CLOSED exige read-back durable MATCHED (misma physical key, collector epoch autorizado, KNOWN_EMPTY, posterior al drain auditado) en el trigger 064; protege UPDATE SQL directo; PREPARED→CLOSED nunca observado sigue permitido.
- **C1-3:** recovery SUSPENDED→OBSERVING restaura `coverage_quality=PROVEN` (`E06_RECOVERY_QUALITY`) con `accepts_opens_from=received_at`, `accepts_opens_to=NULL`, watermark inmutable; gap queda UNKNOWN.
- **C1-4:** nueva reserva `uq_e6_canonical_admission` UNIQUE serializa el segundo PREPARED CANONICAL de la misma Version desde el POST (§14, `ErrCanonicalExists`); SUSPENDED sin reemplazo implícito; switch explícito tras DRAINING/CLOSED; SHADOW coexiste.

## Validación

- PG REAL en PostgreSQL 17.11 descartable local (binarios Zonky + cliente PGDG, cluster efímero `/tmp/e06-pg17` recién initdb'd; sin docker/sudo; cero acceso a Aranea PROD/SHARED DEV; server detenido al cierre): harness `reference_binding_e6/run.sh` PASS completo dos veces (rebuild 001–063, probe interrupción, up, aserciones de índices actualizadas, idempotencia, máquina de estados con C1-2/C1-3 neg+pos, unicidad con C1-4/C1-1 y switch post-CLOSED, watermark/vista/revokes, down fail-closed >50 bytes, up/down/up final).
- Tests Go E-06 13/13 PASS con `DATABASE_URL` y `-race`; `go vet` OK; builds sdk/gateway/bridge OK; skip-mode CONTRACT PASS. SOURCE: tokens prohibidos 0 en el delta.
- Fixtures cross-file ajustados (bindings 004 de 12 y 201 de 14 → SHADOW): la reserva C1-4 opera sobre fixtures que probaban borrado/watermark, no la clase; documentado en VERIFICATION.md §WP-A CORRECTION C1.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni rutas con credenciales; los binarios y el cluster PG descartables viven y mueren fuera del vault.

## Rollback

- Repo: revertir el commit `c021983f` en la branch feature (sin efecto en master). Vault: revertir el delta fechado de la nota E-06 y borrar este log.
