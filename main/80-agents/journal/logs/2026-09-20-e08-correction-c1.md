# Change Log — 2026-09-20 — E-08 Corrección Manager C1

## Alcance

Sesión NORMAL de corrección «ECHO E-08 — MANAGER CORRECTION C1» (seguridad económica, identidad y persistencia) sobre `xKoRx/echo`, branch `feature/e08-routing-economic-command-risk-reservation`, worktree `/tmp/echo-e08-routing-economic-command-risk-reservation`. Baseline verificado: `b0012909` (HEAD == origin, clean). Sin Forge, E-06, E-07, master, SHARED DEV ni PROD; sin dispatcher, órdenes, releases ni activación. Evidencia completa en el repo: `specs/FEAT-ROUTING-ECONOMIC-COMMAND-RISK-RESERVATION-E8/VERIFICATION.md` §10 y `SPEC.md` §18 (ERRATUM C1).

## Cambio

- **Tipo:** repo mutation (delta cerrado E-08) + documentation + journal.
- **Repo (`xKoRx/echo`, push FF `b0012909..53d42615`, HEAD == origin, 9 commits):**
  - C1-A `977e4fde` — reserva ANTES del comando económico: `CheckHeadroom` (FOR UPDATE, lock hasta el commit) separado de `InsertReservation`; fanout sin headroom deja CERO filas en `echo.economic_commands` (COUNT directo sin JOIN); check+comando+reserva+EXPECTED atómicos; `REPLAY_CONVERGED` exige su reserva durable.
  - C1-B `52c28f29` — `ClaimReady` exclusivamente `READY`; IN_FLIGHT vencido jamás se re-claima; único camino = sweeper §12(c) ⇒ `UNKNOWN_OUTCOME`+`UNKNOWN_HELD` con `command_ref` y reserva conservados.
  - C1-C `0da85fb9` — CONSUMED computa en headroom y en el límite de comandos abiertos (`RESERVED+UNKNOWN_HELD+CONSUMED`); `HeldExposure` alineado; CONSUMED terminal en V1 (guard 066 intacta); sin auto-release.
  - C1-D `ff9e6744` — `RoutingGate.Evaluate(GateQuery)` compara pin write-once del raw = resolución OBSERVING = request (raw_row_id, source_event_id, fact_digest, trade_id, binding_id, binding_ref, strategy_version_ref, observation_class CANONICAL); contradicción/ausencia ⇒ `PIN_MISMATCH` sin comando ni reserva; gate expone `magic_decimal` del binding.
  - C1-F `21c363ae` — sin defaults fabricados: `magic_effective` = override explícito o `magic_decimal` del binding (congelado en `ROUTING_INPUT`); `MAGIC_UNVERIFIED` sustituye al placeholder 1; moneda demostrada contra `budget.currency` bajo lock ⇒ `RISK_CURRENCY_UNVERIFIED` (adiós "USD" default).
  - C1-E `5ddfb471` — 066 añade `echo.economic_copy_authorizations` (octava tabla; superficie contratada faltante de Live Authority §7; E-08 sólo lee; sin fila ⇒ `COPY_GATE_CLOSED`; autorización congelada en `ROUTING_INPUT`, re-drive jamás re-evalúa) + RG-4.1: cobertura demostrada ante `echo.reference_coverage` (`KNOWN_COMPLETE` cubriendo event time; `PARTIAL`/`UNKNOWN`/ausencia ⇒ `COVERAGE_UNKNOWN`); `binding_lookup_test.go` (E-07, fuera de lista) devuelto a baseline exacto por amend.
  - docs `79da8f8e` + `e6a0d9a3` + `53d42615` — SPEC ERRATUM C1 (§18, razones nuevas §18.7: `PIN_MISMATCH`, `COVERAGE_UNKNOWN`, `MAGIC_UNVERIFIED`, `RISK_CURRENCY_UNVERIFIED`) y VERIFICATION §10 (evidencia por defecto, failing-set parity, COVERAGE_GATE_PENDING con rutas exactas, deuda copy-auth, gates).
- **Razones durables nuevas en `v3/sdk/domain/economic_command.go`** (archivo de la lista cerrada); cero cambios en `v3/sdk/contracts/**`, migraciones 001–065, `go.mod`/`go.sum`/`go.work`, legacy `v3/core/internal/functions/**`, gateway, MQL, Forge.
- **Vault:** este change log, agent run `[[2026-09-20-zcode-glm-5.3-flash-e08-correction-c1]]` y memoria de sesión (`memory/MEMORY.md` + `polymarket/echo-e08-implementation-state` actualizada). Cero notas canónicas nuevas (agent run materializado vía `materialize_schema_note.py`, schema-validado).

## Verificación

- Harness 066 de OCHO tablas PASS (up/down/up 001→066, interlock rojo sin 065, guardas por nombre, matriz UNIQUE con `uq_e8_copy_auth`, REVOKEs de la octava tabla) sobre PostgreSQL 17.11 portable descartable (localhost:15432; jamás SHARED DEV/PROD).
- Suites `-race -count=1` con metodología de VERIFICATION §3 (comandos separados por paquete): domain limpio; postgres failing set 53/53 idéntico al T00 (diff por nombre: cero nuevos, cero cambiados); econroute ok estable en 6 corridas; etcd/telemetry 2 fallos preexistentes de infra externa.
- Gates finales: `SOURCE_VERIFIED · CONTRACT_PASS · PG_PASS · COVERAGE_GATE_PENDING (residuo declarado §10.4, sin fabricar cobertura) · PHYSICAL_PENDING · ECONOMIC_ACTIVATION_PENDING · FINAL_CLOSED=NO`.
- MT-01…MT-18 verdes tras el delta; tests rojo→verde focalizados por defecto antes de suites amplias.

## No tocado / pendientes

- `echo.economic_copy_authorizations` sin escritor en este carril (plano de config del owner; sin fila, el carril no emite comandos) — listado como deuda de superficie/prerrequisito clase C en VERIFICATION §10.6.
- PHYSICAL y ECONOMIC_ACTIVATION siguen pendientes por diseño (SPEC §14/VERIFICATION §7); flag `ECHO_E8_DURABLE_ROUTING` sin activar; router desconectado del flujo legacy; sin dispatcher.
- Siguiente acción única: **Manager review del delta C1 en `origin/feature/e08-routing-economic-command-risk-reservation`**.
