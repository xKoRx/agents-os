# change_log — 2026-09-23 · The Lab D1 — Echo Foundation: Shot 1 IMPLEMENTATION ejecutado con evidencia

**Entidad:** [[The Lab]] · repo `xKoRx/echo`

## Cambio

Ejecución del mandato Shot 1 de D1 (paquete A-F congelado): implementación completa de la foundation Echo en branch `feature/d1-echo-foundation` @ `e35d4347` (4 commits sobre `3596fc48`, sin push, sin merge a master): contrato `strategy-history.v1` en el SDK compartido, migración 064 (`echo.canonical_operations` + `echo.strategy_history_state`, FK a la autoridad real de StrategyVersion 061), servicio `StrategyHistoryService.ReplaceHistory` (replacement atómico SQX+MT5 preservando REFERENCE, replay fast-path, advisory lock, bulk acotado) y boundary Gateway `PUT/GET /api/v1/strategy-versions/{strategy_version_ref}/history`.

- Nota de proyecto creada: `10-projects/Echo/The Lab/D1 — Echo Foundation/G — Implementation Evidence D1 (Shot 1).md` (baseline, commits, migración, tests exactos, evidencia PG, regresiones clasificadas, riesgos).
- Agent run registrado: `80-agents/journal/agent-runs/2026-09-23-zcode-glm53-d1-echo-foundation-shot1.md`.
- Feedback de sesión: `80-agents/journal/feedback/session/2026-09-23-d1-echo-foundation-shot1-feedback.md`.

## Evidencia (resumen)

- Migración 064 aplicada y verificada en PG 17.11 desechable `127.0.0.1:15445/d1_foundation` con harness nuevo `v3/sdk/postgres/tests/d1_foundation/run.sh` (probe BEGIN+ROLLBACK, apply estricto, idempotencia, down+up: OK).
- Tests del Test Plan D1: contratos 20/20 PASS (coverage 95.1% paquete / 96.3% archivo nuevo); PG 11/11 TestD1 PASS; gateway HTTP 6/6 TestD1 PASS; lab-worker 5/5. Únicos FAILs clasificados preexistentes en master sin modificar (`TestScratch_QueryDB`, `TestAutomationHandler_HandleMessage_ValidAction`).
- Evidencia conductual: CREATED/REPLACED/UNCHANGED exactos, REFERENCE nunca tocada, rollback forzado conserva dataset y head, reemplazo concurrente convergente, 700 trades ⇒ 3 INSERT statements (sqlmock), delta 0 journal/posiciones.

## Notas

- No se ejecutaron seed tests ETCD ni `go test ./...` raíz (riesgo conocido en master sin fix E-04). Sin contacto con PROD ni workers compartidos; PG desechable local nueva (puerto 15445, PGDATA fuera del vault).
- Adaptación mecánica registrada en la evidencia: 4 TRUNCATEs de harnesses E-03/E-04 incorporan las tablas D1 por las FK nuevas.
- Riesgo activo para D2: migración 064 no aplicada en DEV real; defaults de body limit/deadline a medir con datasets reales.
