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

# 2026-09-17 — E-06 NORMAL WP-B (T04–T07, enrollment HTTP) registrada

## Cambios

- **Entidad Sistema 2 actualizada:** [[Echo — E-06 Reference Enrollment and Binding]] — nuevo bullet de estado `E06_WPB_READY_FOR_MANAGER_REVIEW`, tabla de entrega de desarrollo con commit `cd2aca6`, tarea WP-B `[r]`, bitácora con evidencia completa.
- **Repo `xKoRx/echo`:** commit `cd2aca6` en `feature/e06-reference-enrollment-binding`, push FF `1614028b..cd2aca6` sobre origin, sin merge ni master. Delta de 7 archivos productivos + TASKS/VERIFICATION, todos allowed: `client_config.go`+test, `reference_binding_handler.go`+test (nuevos), `server.go`, `reference_binding_store.go`+test (expansión mínima autorizada: `ListByVersion` + separación del suspend operator). Contracts, 061–064, Bridge, MQL, core, hasura diff 0; `go.mod`/`go.sum` delta 0; `TEST_CHANGE_REQUEST.md` intacto.

## Implementación (T04–T07, SPEC v1.2.2)

- **T04:** pin E-06 aditivo en ClientConfig (`runtime_binding_id`, `strategy_version_ref`, `magic_decimal`, `map_revision`) omitempty con validación estricta sólo al presence (UUID lowercase, `sha256:<64hex>`, decimal canónico sin float); legacy intacto (AC-14).
- **T05:** `POST /api/v1/reference/bindings` siempre PREPARED; idempotencia §17.1 verificada deterministamente — `attach_request_digest = sha256(canonical body echo-wire-json.v1)` y `Idempotency-Key = H("echo-reference-enroll.v1",[ns,version_ref,acct_reg,class,digest])`, golden cruzado Go/Python/sha256sum; header ausente 400 / distinto 409 CONTRACT_CONFLICT; `proof_recorded_at` dentro del proof para convergencia de replay; verifica Version E-03 correspondiente, account role reference, pin magic, map_revision declarado, MT4 ≤ int32; body con `acked`/`state`/`coverage_started_at` 400. GETs by-id y by-version (lista pura sin latest implícito), actors CONFIG|READ, auth E-02 reuse.
- **T06:** ACK con proof `MANUAL_VERIFIED` y hashes EX5/inputs/deps == fila Version (400 con field culpable); `acked_at` seteado, estado PREPARED intacto; replay conserva `acked_at` (AC-02).
- **T07:** drain sella `accepts_opens_to`; suspend operator auditado `config_operator`/`OPERATOR_SUSPEND` (decisión Manager; path `system/STALENESS` intacto para T14, refactor helper parametrizado sin tocar triggers); close PREPARED permitido, OBSERVING→CLOSED 409 NOT_OBSERVING, DRAINING→CLOSED exige evidencia C1-2 (fixture CONTRACT KNOWN_EMPTY en `reference_readbacks` para el positivo HTTP); publish del pin exacto por `echo.account-configs.v1` post-PREPARED sin cambiar estado, fallo ⇒ 503 retryable con republicación en retry idempotente, cero `echo.commands.*`/`echo.reference-events.v1`; `hasura_handler.go` intocado.

## Validación

- PG REAL PostgreSQL 17.11 descartable local (binarios Zonky + cliente PGDG, cluster efímero recién initdb'd; cero acceso a Aranea PROD/SHARED DEV): harness `reference_binding_e6/run.sh` PASS completo ×2 (rebuild 001–063, probe, up, aserciones 10, idempotencia, máquina de estados, unicidad A–G, watermark/vista/revokes, down fail-closed, up/down/up final).
- Tests Go E-06 15/15 `sdk/postgres` (13 previos + `TestSuspendByOperator_Audit` + `TestListByVersion`) y 15/15 `gateway/internal` PASS con `DATABASE_URL` y `-race`; `sdk/domain` PASS plain/race; `go vet` OK; builds sdk/gateway/bridge OK (Bridge compila sin modificaciones); skip-mode idéntico al baseline (sólo `TestScratch_QueryDB` documentado).
- Regresión: failing set de `gateway/internal` idéntico al baseline puro `1614028b` (29=29, colateral preexistente clase TC-06-1 en harnesses forge; `TestForgeIngest_CertPack` con inestabilidad de orden falla idéntico en ambos aislado); `sdk/postgres` 0=0 en este cluster. Cero regresiones nuevas.
- Bug propio detectado y corregido por gates: conflicto de patrones del mux en el fallback sin PG (skip-mode panic `TestServer_MountsForgeIngest`) — resuelto con patrón subtree.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni rutas con credenciales; el cluster PG descartable vive fuera del vault.

## Rollback

- Repo: revertir el commit `cd2aca6` en la branch feature (sin efecto en master). Vault: revertir el delta fechado de la nota E-06 y borrar este log.
