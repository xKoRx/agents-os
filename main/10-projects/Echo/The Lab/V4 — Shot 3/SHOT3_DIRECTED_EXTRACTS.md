---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[0 — Submanager State]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-21"
updated: "2026-10-21"
---

# SHOT3_DIRECTED_EXTRACTS

## Propósito

Seis fragmentos dirigidos para validar tres conclusiones críticas: dinero/ingesta, revisión reproducible y migraciones/harness. Source anclado al SHA `61ac1f720d07513e48b0310b84b5b415b80ff48f`; evidence a repros ejecutados. Total de líneas de fragmentos calculado al final, inferior a600. No son logs completos ni certifican capacidades ausentes.

## Contenido

### 1. S3-F01 — bucle e igualdad decimal

`xKoRx/echo@61ac1f720d07513e48b0310b84b5b415b80ff48f:v3/sdk/postgres/strategy_history_ingestion_v2.go:370–406`

```text
370: 	for _, no := range nh.ops {
371: 		if _, err := tx.ExecContext(ctx,
372: 			`INSERT INTO echo.strategy_history_operations
373: 				(registry_namespace, strategy_version_ref, producer_writer, history_id, revision_no, source_operation_id,
374: 				 grain, status, instrument_id, side, opened_at, closed_at,
375: 				 entry_price, exit_price, stop_loss, take_profit, volume, volume_unit,
376: 				 gross_pnl, commission, swap, net_pnl, net_currency,
377: 				 initial_risk_amount, initial_risk_currency, risk_method, risk_evidence_ref,
378: 				 record_digest, terminal_at)
379: 			 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27,$28,$29)`,
380: 			namespace, versionRef, writer, historyID, revisionNo, no.op.SourceOperationID,
381: 			no.op.Grain, opStatus(no.op), nullStr(no.op.InstrumentID), nullStr(no.op.Side),
382: 			nullTime(no.op.OpenedAt), nullTime(no.op.ClosedAt),
383: 			nullStr(no.op.EntryPrice), nullStr(no.op.ExitPrice), nullStr(no.op.StopLoss), nullStr(no.op.TakeProfit),
384: 			nullDecimal(no.op.Volume), nullStr(no.op.VolumeUnit),
385: 			nullDecimal(no.op.GrossPnL), nullDecimal(no.op.Commission), nullDecimal(no.op.Swap),
386: 			nullDecimal(no.op.NetPnL), nullStr(no.op.NetCurrency),
387: 			nullDecimal(no.op.InitialRiskAmount), nullStr(no.op.InitialRiskCurrency),
388: 			nullStr(no.op.RiskMethod), nullStr(no.op.RiskEvidenceRef),
389: 			no.op.RecordDigest, nullTime(no.op.TerminalAt)); err != nil {
390: 			return fmt.Errorf("insert operation %q: %w", no.op.SourceOperationID, err)
391: 		}
392: 		for _, no := range nh.ops {
393: 			for _, mv := range no.movements {
394: 				if _, err := tx.ExecContext(ctx,
395: 					`INSERT INTO echo.strategy_history_movements
396: 					(registry_namespace, strategy_version_ref, producer_writer, history_id, revision_no,
397: 					 source_operation_id, movement_id, movement_type, amount_signed, currency, economic_at, source_ref, record_digest)
398: 				 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)`,
399: 					namespace, versionRef, writer, historyID, revisionNo, no.op.SourceOperationID,
400: 					mv.MovementID, mv.MovementType, mv.AmountSigned, mv.Currency, mv.EconomicAt, nullStr(mv.SourceRef), mv.RecordDigest); err != nil {
401: 					return fmt.Errorf("insert movement %q/%q: %w", no.op.SourceOperationID, mv.MovementID, err)
402: 				}
403: 			}
404: 		}
405: 	}
406: 	return nil
```

`strategy_history_ingestion_v2.go:613–625,728–735`: decimalAdd devuelve FloatString(18), luego el normalizador compara strings.

### 2. S3-F01/F03 — contraejemplos ejecutados

`evidence/functional.json`; aserciones ancladas al test y línea observada.

```text
TestShot3Functional/A01_TerminalCanonicalDecimal: shot3_functional_test.go:45: valid exact 10 == sum(10) rejected: histories[0] op "op": net_pnl 10 != Σ movements 10.000000000000000000
TestShot3Functional/A02_MultipleOperationsWithMovements: shot3_functional_test.go:49: two valid OPEN operations rejected: insert movement "b"/"m1": pq: insert or update on table "strategy_history_movements" violates foreign key constraint "strategy_history_movements_op_fk"
TestShot3Functional/A07_TerminalNullInsert: shot3_functional_test.go:78: TERMINAL INSERT committed with NULL net_pnl/net_currency/terminal_at
TestShot3Functional/A08_MixedCurrencyCannotSum: shot3_functional_test.go:84: 10 USD + (-1 EUR) sealed as 9 USD without FX
TestShot3Functional/A23_CanonicalDecimalPrecision: shot3_functional_test.go:162: accepted input rounded silently in numeric(38,18): 0.123456789012345679
```

### 3. S3-F02 — guard y validación de terminalidad

`xKoRx/echo@61ac1f720d07513e48b0310b84b5b415b80ff48f:v3/sdk/postgres/migrations/069_strategy_platform_kinds_v4.up.sql:474–551`

```text
474: CREATE OR REPLACE FUNCTION echo.fn_labv4_operations_terminal_guard()
475: RETURNS trigger
476: LANGUAGE plpgsql
477: AS $fn$
478: BEGIN
479:     -- Inmutabilidad de identidad/contenido: solo la transición de terminalidad
480:     -- puede cambiar status/terminal_at/closed_at/net_pnl.
481:     IF NEW.registry_namespace <> OLD.registry_namespace
482:        OR NEW.strategy_version_ref <> OLD.strategy_version_ref
483:        OR NEW.producer_writer <> OLD.producer_writer
484:        OR NEW.history_id <> OLD.history_id
485:        OR NEW.revision_no <> OLD.revision_no
486:        OR NEW.source_operation_id <> OLD.source_operation_id
487:        OR NEW.grain <> OLD.grain
488:        OR NEW.record_digest <> OLD.record_digest
489:        OR NEW.initial_risk_amount IS DISTINCT FROM OLD.initial_risk_amount
490:        OR NEW.initial_risk_currency IS DISTINCT FROM OLD.initial_risk_currency
491:        OR NEW.risk_method IS DISTINCT FROM OLD.risk_method
492:        OR NEW.risk_evidence_ref IS DISTINCT FROM OLD.risk_evidence_ref THEN
493:         RAISE EXCEPTION 'strategy_history_operations inmutable: solo la transición de terminalidad puede cambiar status/terminal_at/closed_at/net_pnl';
494:     END IF;
495:     -- Un solo sellado: terminal no vuelve a OPEN ni re-sella.
496:     IF OLD.status = 'TERMINAL' THEN
497:         RAISE EXCEPTION 'strategy_history_operations ya terminal: sin re-sellado';
498:     END IF;
499:     IF NEW.status = 'TERMINAL' THEN
500:         IF NEW.terminal_at IS NULL OR NEW.net_pnl IS NULL OR NEW.net_currency IS NULL THEN
501:             RAISE EXCEPTION 'terminalidad exige terminal_at + net_pnl + net_currency sellados';
502:         END IF;
503:     END IF;
504:     RETURN NEW;
505: END;
506: $fn$;
507: 
508: DROP TRIGGER IF EXISTS trg_sho_terminal_guard ON echo.strategy_history_operations;
509: CREATE TRIGGER trg_sho_terminal_guard
510:     BEFORE UPDATE ON echo.strategy_history_operations
511:     FOR EACH ROW EXECUTE FUNCTION echo.fn_labv4_operations_terminal_guard();
512: 
513: CREATE OR REPLACE FUNCTION echo.fn_labv4_terminal_net_check()
514: RETURNS trigger
515: LANGUAGE plpgsql
516: AS $fn$
517: DECLARE
518:     v_sum numeric(38,18);
519:     v_count bigint;
520: BEGIN
521:     -- Solo grano ECONOMIC_MOVEMENTS: una CLOSED_SUMMARY sin movements es
522:     -- legítima y este trigger no la toca (freeze §2.2 punto 5).
523:     IF NEW.grain <> 'ECONOMIC_MOVEMENTS' OR NEW.status <> 'TERMINAL' THEN
524:         RETURN NEW;
525:     END IF;
526:     SELECT COALESCE(SUM(amount_signed), 0), COUNT(*)
527:       INTO v_sum, v_count
528:       FROM echo.strategy_history_movements m
529:      WHERE m.registry_namespace = NEW.registry_namespace
530:        AND m.strategy_version_ref = NEW.strategy_version_ref
531:        AND m.producer_writer = NEW.producer_writer
532:        AND m.history_id = NEW.history_id
533:        AND m.revision_no = NEW.revision_no
534:        AND m.source_operation_id = NEW.source_operation_id;
535:     IF v_count = 0 THEN
536:         RAISE EXCEPTION 'terminalidad ECONOMIC_MOVEMENTS sin movements: usa CLOSED_SUMMARY si solo existe resumen';
537:     END IF;
538:     IF NEW.net_pnl <> v_sum THEN
539:         RAISE EXCEPTION 'net_pnl (%) <> Σ movements activos (%) para %/rev %/op %',
540:             NEW.net_pnl, v_sum, NEW.source_operation_id, NEW.revision_no, NEW.source_operation_id;
541:     END IF;
542:     RETURN NEW;
543: END;
544: $fn$;
545: 
546: DROP TRIGGER IF EXISTS trg_sho_terminal_net_check ON echo.strategy_history_operations;
547: CREATE CONSTRAINT TRIGGER trg_sho_terminal_net_check
548:     AFTER INSERT OR UPDATE OF status, net_pnl ON echo.strategy_history_operations
549:     DEFERRABLE INITIALLY DEFERRED
550:     FOR EACH ROW
551:     EXECUTE FUNCTION echo.fn_labv4_terminal_net_check();
```

### 4. S3-F02/F04 — revisión y metadatos

`evidence/functional.json`; aserciones ancladas al test y línea observada.

```text
TestShot3Functional/A03_NilSinkMustFailClosed: shot3_functional_test.go:53: accepted revision without artifact: [{HistoryID:nil-sink RevisionNo:1 HeadDigest:sha256:be4b5aaebd3a07c8296520fcdba35828d998a663a6819864a33dc4ba69583ee6 State:ACCEPTED}]
TestShot3Functional/A05_MetadataRoundTripAndRetention: shot3_functional_test.go:63: different construction_at produces identical retained artifact bytes
TestShot3Functional/A05_MetadataRoundTripAndRetention: shot3_functional_test.go:66: PUT revision accepted but current construction_at=2025-01-01
TestShot3Functional/A09_AppendAfterTerminalChangesPinnedRevision: shot3_functional_test.go:93: late append accepted, same head=true; sealed net=10, movements sum=8.000000000000000000
TestShot3Functional/A10_OpenContentImmutable: shot3_functional_test.go:98: OPEN economics/content updated without new revision or digest
TestShot3Functional/A11_DeleteOperationImmutable: shot3_functional_test.go:102: summary deleted while revision metadata/digest remains
TestShot3Functional/A17_SupersededRowsCannotChange: shot3_functional_test.go:134: superseded revision changed by append without revision identity change
```

A09 se repitió tras insertar referencia sintética READY en `lab.curves` para revisión1: `evidence/pinned-revision.json`, mismo fallo. No fue resultado de un worker existente. `strategy_history_ingestion_v2.go:694–723` muestra header retenido sin D16/MM/cobertura y `:502–505` sólo mueve head/digest.

### 5. S3-F07 — guard de down 067

`xKoRx/echo@61ac1f720d07513e48b0310b84b5b415b80ff48f:v3/sdk/postgres/migrations/067_execution_projection_v4.down.sql:1–24`

```text
1: -- 067_execution_projection_v4.down.sql
2: -- Retiro de la proyección execution.* V4 (no autoritativa, reconstruible).
3: -- Elimina su fila de lab_migration_state; la tabla de estado permanece
4: -- (fue creada aquí pero su ciclo de vida es de la cadena V4 completa).
5: -- Fail-closed: si existen filas (proyección poblada), el down exige la
6: -- bandera de entorno destructible, igual que el patrón 063/065.
7: 
8: DO $$
9: BEGIN
10:     IF to_regclass('echo.execution_operations') IS NOT NULL
11:        AND EXISTS (SELECT 1 FROM echo.execution_operations LIMIT 1)
12:        AND COALESCE(current_setting('lab.destructible_down', true), 'off') <> 'on' THEN
13:         RAISE EXCEPTION '067 down refused: execution_operations populated (set lab.destructible_down=on on a disposable cluster)';
14:     END IF;
15: END $$;
16: 
17: DROP TABLE IF EXISTS echo.execution_session_observations;
18: DROP TABLE IF EXISTS echo.execution_position_observations;
19: DROP TABLE IF EXISTS echo.execution_provider_decisions;
20: DROP TABLE IF EXISTS echo.execution_fills;
21: DROP TABLE IF EXISTS echo.execution_orders;
22: DROP TABLE IF EXISTS echo.execution_operations;
23: 
24: DELETE FROM echo.lab_migration_state WHERE migration_id = '067_execution_projection_v4';
```

### 6. S3-F07/F08 — datos perdidos y contraste baseline

`evidence/migrations-data.json`; aserciones ancladas al test y línea observada.

```text
TestShot3MigrationsWithData/M04_DownMustProtectFillOnlyData: shot3_migrations_test.go:44: 067 down deleted populated fills while operations was empty, without destructible flag
```

El mismo `TestIdentity_Insert65And1024` pasa baseline y falla candidato; los dos POST gateway también. Evidencia: `baseline-functional-regression.json`, `candidate-functional-regression.json`, `baseline-gateway-functional.json`, `candidate-gateway-functional.json`. Fixtures exactos: `strategy_identity_repository_test.go:34–39` y `gateway/internal/forge_ingest_handler_test.go:62–66`; nuevas FK desde `069...up.sql:207–212`.

**Fragmentos totales: 152 líneas**, más referencias/anotaciones; seis fragmentos para tres conclusiones.

## Fuentes

[[SHOT3_ADVERSARIAL_REPORT]] y MANIFEST.sha256 del paquete de evidencia.
