---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-S01-SUBMANAGER-PROMPT]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-ACCOUNT-DAY-REMEDIATION

## Propósito

Registrar la corrección local de BTG-S01 finding BT2-F08: una corrida cuyo warmup comienza antes del reset debe abrir el identity del account-day que contiene ese instante, en las rutas nativa y legacy.

## Contenido

La causa estaba en la composición inicial de `v3/backtester/run.go`: el ID se derivaba directamente de la fecha civil de `WarmupStart`. Para el reset Chicago 17:00, warmup `2026-10-05T20:59:00Z` (=15:59 CT) abría `ad-20261005`, y el reset natural `2026-10-05T22:00:00Z` intentaba abrir el mismo ID. La corrección resuelve la fecha civil del intervalo contenedor con `civilDateOf` y `boundaryOf`; si el reset de ese día ocurre después de warmup, retrocede una fecha con `AddDate(0, 0, -1)`. El ledger conserva el `observed_at` real de warmup y las aperturas naturales mantienen su semántica.

La regresión permanente `v3/backtester/account_day_identity_regression_test.go` reproduce el mismo slice en native OHLC y TRADE_MODEL legacy. Verifica `ad-20261004` al inicio, `ad-20261005` al reset, timestamps originales, plan ID `ad-btg-functional-1` separado de la identidad del ledger, ordinal 1 sin consumo por warmup, ausencia de operaciones/fills inventados, extremos antes/en/después del reset, cambio de año, DST de primavera y otoño, fallo nombrado ante timezone inválido, fallo visible ante error del recorder y reset exactamente en `EndExclusive` sin apertura terminal.

Source freeze: `xKoRx/echo`, branch `codex/btg-s01-account-day-remediation`, commit `171fc712e56d731493befeef5c54a2620f25d31a`, tree `aee767d446428fa1223f7f7f0a682e0df53e604c`. El diff de código cambia solo la resolución de la apertura inicial en `v3/backtester/run.go`; no altera accounting, plan/selector IDs, reset, horizonte, identidad schema, MM, Strategy ni Provider.

Verificación local: la regresión nueva y los tests S04 de transición, replay/oráculo, cero trades y controles, Driver DST, plan parcial/DST y OHLC boundary/completeness/horizon/recorder fault pasaron con race; `go vet ./v3/backtester` pasó. Los statements ejecutables del bloque cambiado `run.go:684–693` alcanzan 8/8 (100%); el 93.3% de la función completa incluye un guard preexistente para doble apertura, no alcanzable desde `NewRun` válido que abre sobre un ledger nuevo. `git diff --check` pasó.

El red baseline del mismo input y los logs de gate están fuera del vault en el bundle de workspace `work/btg-s01-20261006/reports/account-day-remediation/`; el reporte independiente previo está en `work/btg-s01-20261006/reports/ohlc-driver-final-review/`. Digests SHA-256: `baseline-red.log` `cea4aa5cb1b4c550a7db7bf3e5211e6ad6d5e46734de04aeeb16e621841b7095`, `targeted-race.log` `fcb09ba31d15515dd9eb226467cfab7044241b768a7f89e1e21de5524647eef6`, `vet.log` (vacío, PASS) `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, `account-day.cover` `8161e26c22c7804140abd54f2c8d71b5593edd1a26acacd19b6ef67d7f2f8a11` y `account-day-legacy-reference.log` `226c29b9fe408a8da457fe7e50831d1d269e4bfb5c526415d4db3c76ecefa839`. El red baseline mostraba el ID inicial incorrecto en ambos modelos y la evidencia independiente confirma `ACCOUNT_DAY_FAILED` en el reset. Las 13 muestras históricas originales siguen `POLICY_DENIED / NOT_ACQUIRED`; no hubo rerun histórico ni certificación de resultados reales. Estado entregado: listo para nueva revisión TOP local, sin aceptación del owner o cierre del coordinador raíz.

## Fuentes

- [[BTG-S01-SUBMANAGER-PROMPT]] y el finding BT2-F08 aceptado por Root; SDD congelado en `xKoRx/echo:specs/btg-s01-account-day-remediation/`.
- Reporte de revisión independiente BTG-S01-OHLC-driver y sus probes sintéticos; autoridades de Echo Futures BTG-S01 §F08 y perfil funcional.
- Evidencia de código y tests del commit `171fc712e56d731493befeef5c54a2620f25d31a` en `xKoRx/echo`.
