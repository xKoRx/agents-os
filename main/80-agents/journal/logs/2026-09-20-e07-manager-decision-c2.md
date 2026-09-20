# Change Log — 2026-09-20: E-07 decisión Manager C2 (C4 protocolo V1.1 + C5 receta frozen + gate RAW-BEFORE-ROUTE)

## Contexto

Consumo de las decisiones frozen del Manager sobre C4/C5 (mandato "ECHO E-07 — MANAGER DECISION C2"): C4 autoriza el cambio aditivo del protocolo Reference para transportar identidad física auténtica; C5 ratifica la receta `fact_ref`. Objetivo: dejar E-07 en el máximo estado técnicamente demostrable, sin repetir planning ni rehacer C1–C3, sin intervenir Forge/E-06/master/flota, sin releases ni operaciones.

## Cambios

- Repo `xKoRx/echo` (fuera del vault): push FF `a7a61875..28213bbc` en `origin/feature/e07-raw-facts-deal-lifecycle`, commits atómicos `33730d4e` (código+tests) y `28213bbc` (erratum docs). HEAD == origin, worktree limpio.
- **C4 — productor resuelto EN el repo echo** (`v3/clients/mt5/reference_v3.mq5`, `v3/clients/mt4/reference_v3.mq4`): protocolo pipe V1.1 aditivo con `position_identifier` (OPEN: `POSITION_IDENTIFIER`; CLOSE: `DEAL_POSITION_ID` de la relación durable deal↔posición, posición cerrada OK; MT4: ticket = identificador durable del modelo), `account_server` (`EchoAccountServerRef` = `ACCOUNT_SERVER` observado) y `platform` (`ECHO_PLATFORM` atestada). 6 sitios de construcción; campo no demostrable ⇒ no viaja. `reference_ticket` y `reference_account_id` (login observado) por separado ya viajaban; nada desde ClientConfig ni allocations Forge.
- **C4 — Bridge en carril E-07 exclusivo:** `domain.TradeFactOriginIdentity` + `PipeMessage.ParseTradeFactOriginIdentity` (structs legacy intactos → flujo legacy byte-idéntico por construcción); `TradeFactEmitter` publica sólo con identidad completa: `broker_server_ref` = `account_server` observado (`h.broker` jamás lo sustituye), `platform` = atestación, `account_registration_ref` = receta §7.2 sobre observados; contradicción de cuenta y ausencias ⇒ fail-closed sólo en E-07 (`ErrOriginIdentityUnavailable`), legacy intacto (T10).
- **C5:** `FactRefForV1` reescrita con la receta frozen del Manager `H("echo-trade-fact-ref.v1", [contract_version, kind, source_key, broker_server_ref, account_registration_ref, platform, origin_position_id, trade_id, raw_payload_sha256])`, digest de los bytes ORIGINALES (no base64); excluye relojes de transporte, coordenadas Kafka, reloj PG y sesión Bridge; `fact_digest` (§5.1) y `source_event_id` intactos; firma `(string, error)`.
- **RAW-BEFORE-ROUTE (gate documentado, SPEC §17.4):** PublishSync a Kafka ≠ commit durable PostgreSQL; routing legacy sin cambio; `RAW_DURABLE_BEFORE_ROUTE` global NO declarado; gate obligatorio registrado para integración E-08 (ningún routing/dispatch sin aceptación durable `PROCESSED` + pin válido; sin reenvíos ciegos).
- **SPEC E-07:** ERRATUM-A §17 (protocolo V1.1 + provenance + producto antiguo + receta frozen + identidad no demostrable + gates CONTRACT vs PHYSICAL); cuerpo original §1–16 preservado como historial. VERIFICATION §9 (evidencia completa del delta); PLAN/TASKS con nota de delta acotada.
- Entidad/proyecto `[[Echo — E-07 Raw Facts DEAL Coverage Trade Lifecycle]]`: bitácora y estado por delta. `[[Echo — Live Platform V1]]`: delta roadmap E-07.
- Registro de ejecución: `80-agents/journal/agent-runs/2026-09-20-zcode-glm-5.3-flash-e07-manager-decision-c2.md`.

## Verificación

- Rojo→verde: 5 rojos exactos @ `a7a61875` (receta ≠ frozen; colisión B dos DEALs; colisión C MODIFY por secuencia; E payload modificado converge; hooks: 0 facts con productor enriquecido) → verde, con guards A/D/F (F registra el límite de bytes idénticos).
- Gates: `go vet` + `go build` 4 módulos PASS; suites `-race` dominio/bridge(internal+session)/tradefacts PASS; store E-07 7/7 + binding lookup 3/3 PASS con PG real; harness `trade_facts_e7` 061→065 PASS (PG 17.11 descartable puerto 15441, up/down/up, interlock, guardas, REVOKEs).
- Failing sets por nombre apples-to-apples (worktree baseline `a7a61875` vs delta, DBs frescas equivalentes, mismo comando): equivalentes — únicas diferencias = flakes preexistentes documentados de suites 061/064 ajenas a E-07 (pertenencia variable entre corridas del mismo árbol; demostrado con tercera DB fresca). Cero nombres E-07 en ningún failing set. Sin `DATABASE_URL`: los 4 canónicos §7.1, sin diferencias.
- `git diff --check` limpio; go.mod/go.sum delta 0; `v3/sdk/contracts/**` y migraciones 001–065 diff 0.

## No-tocados

- Forge, E-06 (código y objetos 064), master, flota, releases/tags, SHARED DEV, PROD, operaciones de cuentas: sin intervención. Migración 065 sin modificación SQL. S0 `contracts/**` sin cambio. C1–C3 sin retoque. PHYSICAL PENDING y FINAL_CLOSED=NO (prohibido declarar producción funcional E-07 sin productor real demostrando identidad en terminal).
