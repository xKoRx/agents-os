# Change Log — 2026-09-20: E-07 corrección Manager C3 (ticket ≠ position_identifier en CLOSE MT5)

## Contexto

Consumo de la corrección Manager C3 (mandato "ECHO E-07 — MANAGER CORRECTION C3"): `SendTradeCloseImmediate` (`v3/clients/mt5/reference_v3.mq5`) ejecutaba `HistorySelectByPosition(ticket)` con el POSITION_TICKET cuando la API exige el POSITION_IDENTIFIER (ambos pueden diferir; docs MQL5), de modo que el campo `position_identifier` del CLOSE (protocolo V1.1, SPEC §17.1) podía quedar ausente incorrectamente y el origin key §5.1 del CLOSE divergía del OPEN. Objetivo: resolver el identificador auténtico desde la relación física/histórica MT5, sin tocar economía legacy, S0, 065, E-03/E-06 ni Forge.

## Cambios

- Repo `xKoRx/echo` (fuera del vault): push FF `28213bbc..3765f2ba` en `origin/feature/e07-raw-facts-deal-lifecycle`, commit único `3765f2ba`. HEAD == origin, worktree limpio.
- **Resolver `ResolvePositionIdentifier(ticket)`**: fuentes observadas en orden — (1) posición viva (`PositionSelectByTicket` → `POSITION_IDENTIFIER`); (2) relación durable del historial orden→posición (`HistoryOrderSelect(ticket)` → `ORDER_POSITION_ID`, disponible con la posición cerrada); contradicción entre fuentes o relación no demostrable ⇒ 0 = fail-closed §17.3 (el campo no viaja; jamás se fabrica). Sin estado volátil de sesión (estable ante reinicio).
- **`HistorySelectByPosition` exclusivamente con el identificador resuelto** (`if(resolvedIdentifier > 0 && ...)`); `DEAL_POSITION_ID` de los deals sigue siendo la provenance observada (C4 intacta). Sitios corregidos: `SendTradeCloseImmediate`, `CheckForClosedOrders` (razón + precio/profit), guard `positionId == 0` en `DetectCloseReasonFromDeals`. Los cierres offline (OnInit → cola) y los reenvíos tras reconexión (`ProcessPendingCloses`) confluyen al mismo path. OPEN/MODIFY/reenvío de intents ya observaban `POSITION_IDENTIFIER` de la posición seleccionada (C4) — sin retoque. MT4 diff 0 (MQL4 no posee la API; ticket = identidad durable).
- **Contrato mínimo:** sin extensión del formato binario `TradeMapper` (§10.6 E-03 intacto) — la relación durable vive en el historial MT5 y no requiere campo nuevo en persistencia; sin migración ni BWC de archivos binarios que demostrar.
- **Hallazgo registrado sin retoque:** `v3/clients/mt5/EchoPersistence.mqh` (`ReconcileWithMT4`, `DetectCloseReasonFromHistory`) repite el patrón en la DETECCIÓN de cierres offline (no porta el campo E-07); archivo compartido con `execution_agent_v3.mq5` y fuera del delta autorizado §17.1 (sólo los 2 EAs reference) — queda para decisión del Manager (SPEC §17.6, VERIFICATION §10.1).
- **Tests A–H** (`v3/sdk/domain/position_identifier_resolution_test.go`, patrón C1/C2: pines SOURCE sobre el MQL real + tabla de decisión espejo Go): A ticket==identificador, B ticket≠identificador (con demostración mecánica del defecto), C posición cerrada, D offline+reconexión, E restart, F historial insuficiente fail-closed, G origin key OPEN==CLOSE, H BWC legacy (pines del builder trade_close intactos).
- **SPEC E-07 §17.6** (enmienda provenance CLOSE); **VERIFICATION §10** (evidencia); PLAN/TASKS con delta acotado.
- Registro de ejecución: `80-agents/journal/agent-runs/2026-09-20-zcode-glm-5.3-flash-e07-manager-correction-c3.md`.

## Verificación

- Fase roja demostrada sobre `28213bbc`: 2 tests SOURCE rojos exactos (`TestSOURCE_C3_CloseHistorySelectedByResolvedIdentifierOnly`: 2× `HistorySelectByPosition(ticket)` + 1× `DetectCloseReasonFromDeals(ticket)` presentes y resolver ausente; `TestSOURCE_C3_ResolverPinsPhysicalSourcesAndFailClosed`: resolver ausente). Guards BWC y espejo verdes en ambas fases.
- Fase verde: tests C3 completos PASS; `go test -race` PASS en `v3/sdk/domain`, `v3/bridge/...`, `v3/core/internal/tradefacts`; `go vet` + `go build` 4 módulos PASS; `git diff --check` limpio; tokens prohibidos 0.
- Delta total: 2 archivos código/tests (`reference_v3.mq5` +62/−8; test nuevo) + 4 docs. S0 (`v3/sdk/contracts/**`), migraciones 001–065, go.mod/go.sum de los 11 módulos: diff 0. Sin impacto PG ⇒ harness 065 no re-ejecutado.
- **MQL_COMPILE_PENDING:** sin compilador MQL real en el entorno (sin MetaEditor/wine, verificado); pines SOURCE certifican estructura, no compilación. Compilar NO equivale a instalar.

## No-tocados

- Forge, E-06 (código y objetos 064), master, flota, releases/tags, SHARED DEV, PROD, operaciones de cuentas: sin intervención. S0/065/E-03/E-06 sin cambio. C1–C2 sin retoque. Persistencia binaria sin extensión. PHYSICAL PENDING, FINAL_CLOSED=NO, RAW-BEFORE-ROUTE global NO declarado (gate E-08 vigente, SPEC §17.4).
