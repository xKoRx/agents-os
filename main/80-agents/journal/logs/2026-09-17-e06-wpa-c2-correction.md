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

# 2026-09-17 — E-06 NORMAL WP-A corrección C2 (T01–T03) registrada

## Cambios

- **Entidad Sistema 2 actualizada:** [[Echo — E-06 Reference Enrollment and Binding]] — nuevo bullet de estado `E06_WPA_C2_READY_FOR_MANAGER_REVIEW`, tabla de entrega de desarrollo con commit `1614028b`, bitácora con evidencia completa. La tarea WP-A permanece `[r]` (Review; gate Manager pendiente).
- **Repo `xKoRx/echo`:** commit `1614028b` en `feature/e06-reference-enrollment-binding`, push FF `c021983f..1614028b` sobre origin, sin merge ni master. Delta de 6 archivos allowed: `064_reference_enrollment_binding.up.sql`, `reference_binding_store_test.go`, `tests/reference_binding_e6/{10,13}_*.sql`, TASKS.md, VERIFICATION.md. Contracts y 061–063 diff 0; `TEST_CHANGE_REQUEST.md` intacto; `reference_binding_store.go` sin cambios.

## Corrección (Manager audit de `c021983f`)

- **C2:** el predicado de `uq_e6_canonical_admission` (C1-4) `state <> 'CLOSED'` retenía la titularidad de admisión durante DRAINING, contradiciendo SPEC §11. Ahora `state IN ('PREPARED','OBSERVING','SUSPENDED')`: DRAINING y CLOSED liberan la reserva; el switch de cuenta canónica explícito admite el sucesor PREPARED en OTRA physical account durante DRAINING; SUSPENDED sigue sin reemplazo implícito; `uq_e6_canonical_open_admitting` permanece defensa en profundidad (ninguna transición enumerada §6 re-entra al índice); `uq_e6_overlap_live` sin cambios (handover same-account sigue exigiendo CLOSED + inventario vacío C1-1/C1-2).

## Validación

- PG REAL en PostgreSQL 17.11 descartable local (binarios Zonky + cliente PGDG, cluster efímero `/tmp/e06-pg17/data-c2` recién initdb'd; sin docker/sudo; cero acceso a Aranea PROD/SHARED DEV; server detenido al cierre): harness `reference_binding_e6/run.sh` PASS completo dos veces (rebuild 001–063, probe interrupción, up, aserciones 10 con predicado C2, idempotencia, máquina de estados, unicidad con evidencia A–G, watermark/vista/revokes, down fail-closed >50 bytes, up/down/up final).
- Tests Go E-06 13/13 PASS con `DATABASE_URL` y `-race`; `go vet` OK; builds sdk/gateway/bridge OK; skip-mode CONTRACT PASS (sólo falla el `TestScratch_QueryDB` preexistente).
- Regresión: failing set del paquete `sdk/postgres` idéntico al baseline puro `c021983f` (53 = 53; colateral TC-06-1 + `TestScratch_QueryDB` preexistentes) — cero regresiones nuevas.
- Evidencia A–G añadida a `13_uniqueness.sql` (A/B/C conflictos PREPARED/OBSERVING/SUSPENDED; D sucesor admitido con viejo DRAINING en otra physical key; E sucesor observa porque el viejo DRAINING ya no es OPEN-admitting; F overlap same-account rechazada con viejo DRAINING; G CLOSED libera y admite sucesor fresco); `TestCanonicalUnique` refleja el mismo lifecycle. Nota colateral documentada en VERIFICATION: comentario de `14_watermark_view_revoke.sql` (no allowed file) queda desactualizado respecto del binding vivo final (109, no 102); funcionalmente irrelevante.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni rutas con credenciales; los binarios y el cluster PG descartables viven y mueren fuera del vault.

## Rollback

- Repo: revertir el commit `1614028b` en la branch feature (sin efecto en master). Vault: revertir el delta fechado de la nota E-06 y borrar este log.
