---
type: change_log
scope: application
created: 2026-07-03
updated: 2026-07-03
area: "[[Echo]]"
application: "[[echo-core]]"
entities:
  - "[[echo-core]]"
related: []
aliases: []
confidence: verified
source_session: "ca7312d2-f138-4a35-9af2-87ea17b79c1b"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/application
  - application/echo-core
---

# Echo Core — Changelog

Bitácora cronológica de modificaciones de la aplicación [[echo-core]].

---

## [2026-08-20] | Síntesis de OPEN nativo del journal desde CloseResult

- **Tipo:** Bugfix (core + sdk)
- **Motivo:** Los EAs de los terminales (pre-`0abdf720`, 05-07) no envían `lot_size`/side/símbolos en el `execution_result` del open nativo, por lo que el core rechazaba todos los opens NATIVE (`lot_size must be positive`) y los closes caían en `close_without_open`: 0 filas NATIVE en `trade_journal` desde el 1-jun. El fix del EA existe en el repo pero no se ha instalado en los terminales.
- **Resolución:**
  - **SDK:** nuevo constructor `NewTradeJournalOpenFromCloseResult` (`v3/sdk/domain/trade_journal.go`) que sintetiza la fila OPEN a partir de los facts del CloseResult (ticket, side, símbolos, lot_size, open_price, opened_at_ms, SL/TP final) con validación completa; ante payload incompleto retorna error y se conserva el rechazo original.
  - **Core:** en `handleExecutionCloseWithTelemetry` (`v3/core/internal/functions/trade_journal.go`), si `SaveClose` devuelve `ErrCloseWithoutOpen` y el trade es NATIVE, sintetiza el OPEN y reintenta el close. Solo NATIVE; path ECHO intacto; idempotente ante reentregas de Kafka.
- **Validación:**
  - Tests nuevos en `journal_open_test.go` (domain) y `trade_journal_test.go` (core): síntesis completa (assert de los args del INSERT), open existente sin síntesis, close incompleto mantiene skip, close ECHO intacto, redelivery sin duplicados. `go build` OK; `go test` core PASS; sdk PASS excepto 3 fallos preexistentes que requieren infra (etcd/Kafka/Jaeger), verificados idénticos en master.
  - Deploy a prod `192.168.31.71` (20-08 22:26, commit `e25165ba`, backup `echo-core.bak-20260820-pre-synthesis`): servicio activo, arranque limpio, pipeline ECHO fluyendo.
  - **Verificado 21-08: 18 filas NATIVE CLOSED (GOLD, EXECUTION) entre 06:00 y 17:59 UTC — las primeras NATIVE de la historia de `trade_journal`.** Alertas de calidad del path: `risk_pips` NULL en las 18 (close legacy sin SL inicial → sin R) y duraciones ≈3h exactas (10798–10800s, `opened_at_ms` del EA legacy aparenta ser sintético).
- **Pendiente:**
  - Fix canónico: recompilar EAs post-05-07 e instalarlos en los terminales MT4/MT5 (manual, MetaEditor).
  - El fix no es retroactivo: hueco NATIVE 1-jun→20-08 requiere backfill opcional (logs de core traen profit/commission/close_price por trade).

---

## [2026-08-19] | Backfill de broker en opens nativos + fallback unknown_broker

- **Tipo:** Bugfix (bridge + sdk/postgres)
- **Motivo:** Opens nativos sin `broker` no provisionaban `strategy_definitions` y el INSERT caía por FK; closes rechazados por `ErrCloseWithoutOpen`.
- **Resolución:** `v3/bridge/internal/pipe_handler.go` backfill `result.Broker` desde sesión en `handleExecutionResult`; `ensureJournalParentRows` provisiona sin broker (fallback `unknown_broker`). Commit `c8aa59a4` (mergeado y pusheado el 20-08; deployado en prod el 19-08 22:28).

---

## [2026-07-03] | Corrección de persistencia de operaciones nativas

- **Tipo:** Bugfix (updated)
- **Motivo:** Las operaciones nativas (tanto manuales como automáticas) no se registraban en la base de datos `trade_journal`. Las manuales fallaban por no tener `strategy_id`, y las automáticas porque el JSON del EA (`execution_result` de apertura) omitía toda la metadata.
- **Resolución:**
  - **EA MT4/MT5:** Se corrigió `EnqueueNativeOpenResult` para serializar y enviar la metadata de apertura (`strategy_id`, `magic_number`, `symbol`, `side`, `lot_size`).
  - **Go SDK (Domain & Postgres):** Se actualizó el mapper del backend para detectar operaciones nativas, asignarles el origen y tipo de fuente `"NATIVE"`, y proveer el default `"NATIVE"` si el `strategy_id` está vacío. Se actualizó el repositorio SQL para persistir y actualizar la columna `origin`.
- **Validación:**
  - Se agregaron unit tests en `journal_open_test.go` (PASS).
  - Pruebas unitarias de dominio y base de datos validadas (PASS).
- **Pendiente:**
  - Recompilar y redesplegar los robots (EAs) de Metatrader en los terminales de trading para restaurar la transmisión correcta del payload de apertura.
