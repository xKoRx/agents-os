---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related: []
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-NQZ3-REAL-HISTORICAL-EXECUTION

## Propósito

Registrar la primera ejecución auténtica reproducida del perfil S2 / GerardMM con el CLI local, datos históricos transferidos por Owner y una continuidad limpia suficiente para observar fills, costos, PnL y lifecycle. Es un baseline funcional de evaluación OHLC de un solo contrato; no es una cuenta financiada, ejecución observada por ticks ni backtest continuo de trece contratos.

## Contenido

### Resultado ejecutable

Con el binario candidato `echo-backtest-counters` del commit `d69d03eceeac1495522473a95baf08087f5c28b3` (Go 1.27.1, SHA256 `79bd5f2aab74c242dbece8ebd274975c94d37100d18af80103e3c44d62e69839`) se completaron dos corridas offline con su reproducción en proceso fresco. El CLI reportó `COMPLETE` en ambas corridas y `IDENTICAL` en ambas reproducciones.

La smoke de cinco días corrió desde warmup `2023-10-15T22:00Z`, con trading desde `2023-10-29T22:00Z` hasta `2023-11-03T21:00Z` exclusive. Produjo 136,932 registros, 20,700 barras físicas SOURCE_CLOSE (y 20,700 OPEN), 60 señales (30 OPEN y 30 CLOSE_ALL), 30 operaciones, 12 operaciones con fills y 24 fills. Dejó el balance/equity en USD 90,029.30: PnL bruto −USD 8,900, costos USD 1,070.70, neto −USD 9,970.70, unrealized 0 y posición final plana. Resultado `bt-b9676b4bb62b7ed7dbd30a626209b0ead77f92672c5b6754b9fef6ade10e4d44`, artefacto SHA256 `9fa6cdbd4bfad7bc1e6e629c84298b812a9ea3294abc160bbd9b73b851c7ff54`; reproducción fresca `IDENTICAL` sobre 136,932 registros.

La corrida longitudinal reutilizó el mismo intervalo inicial y una sola cuenta nueva de USD 100,000 desde el warmup, sin sumar la smoke ni iniciar otra cuenta el 3 de noviembre. Extendió `end_exclusive` a `2023-11-23T03:29Z`, la última barra completa antes del primer gap intrasesión visible. Consumió 38,909 barras físicas SOURCE_CLOSE (38,909 OPEN), emitió 225 señales (113 OPEN: 96 long y 17 short; 112 CLOSE_ALL), 113 operaciones y 78 fills con 78 IDs de ejecución únicos. Hubo fills entre `2023-10-30T00:15Z` y `2023-11-23T03:06Z` y actividad realizada en 19 account-days.

El resultado longitudinal cerró en balance/equity USD 65,706.68: bruto −USD 27,650, costos USD 6,643.32, neto −USD 34,293.32, unrealized y flujos no operativos 0. El máximo drawdown de la serie de equity del ledger fue USD 35,225.55, desde USD 100,375.30 (`2023-10-30T00:16Z`) hasta USD 65,149.75 (`2023-11-22T04:06Z`). La última observación de posición (`2023-11-23T03:06Z`) fue plana.

El resultado es COMPLETE pero conserva el residual real exigido por `REPORT_RESIDUALS`: la última operación queda `ACTIVE` aunque sus órdenes ENTRY BUY 100 y PROTECTIVE SELL 100 figuran FILLED y la posición observada es 0. No hubo intención terminal tras el fill protector antes del límite del source; ese residual queda explícito, sin liquidación artificial. También quedan abiertos el account-day y stage al corte, y timers futuros del calendario. El artefacto es `bt-bd627d8a82e7faf07c5f17c0e89e60352d46abd882e64fa7286f99fd0430029f`, SHA256 `b11bd4e7776762523f29c9dda8e264c98818f5e209c7b051e72e6e671222a637`, con 270,781 registros. La reproducción fresca dio `IDENTICAL`, mismo número de registros y mismo SHA256 del gzip. La corrida tardó 6:47.02, reproducción 7:41.56; RSS máximo 539,916 KiB y 543,384 KiB respectivamente.

### Fuente, calendario y límites

Owner transfirió 13 archivos trimestrales NQ a `/home/kor/aranea/work/btg-s01-20261006/history/nq/nq/`. Los originales locales suman 57,457,558 bytes y 1,096,336 líneas; el inventario SHA completo es `/home/kor/aranea/work/btg-s01-20261006/reports/historical-smoke/corpus-manifest.json` (SHA256 `226f37dd77e9daabc7fe7e985ae1ce11e72f3ecb7fbbd8c54e62fc329f509326`). Las validaciones locales encontraron cero líneas malformadas, desordenadas o duplicadas, precios OHLC no alineados a tick, OHLC inválido o volumen negativo. El origen histórico previo no era legible para este usuario, por lo que no se compararon los bytes de origen contra la copia; la procedencia de la transferencia fue confirmada por Owner y sí se verificaron todos los bytes locales. Los originales no fueron editados.

El archivo físico de esta corrida es `NQ 12-23.Last.txt` (2023, mes 12). La referencia externa/alias de Owner `NQZ23` se mapeó de forma explícita a `NQZ3` / `NQ:NQZ3` en el RunSpec por filename, año y mes; eso conserva la proveniencia y no declara equivalencia intrínseca de etiquetas.

La primera lectura del archivo completo fue rechazada correctamente porque incluía intervalos fuera de la región de sesión configurada. Para continuar sin cambiar política, TOP generó una derivación auditable byte-preserving: mantiene únicamente intervalos completos que el resolver y `bars.Grid.RegionAt(1m)` del calendario compartido `BTG_FUNCTIONAL_NQ_WEEKLY_V1` asignan a sesión; elimina 226 filas fuera de sesión en los 13 archivos (6 de este contrato) y mantiene todas las ausencias dentro de sesiones. El manifiesto por fila registra hash del original, número de línea, inicio/fin, hash de línea cruda y razón. Verificación: `/home/kor/aranea/work/btg-s01-20261006/reports/real-gap-forensics/derived-nt-weekly-v1/verification.json`. No se interpolaron barras, inventaron cierres, añadieron reglas de feriados ni cambiaron la estrategia, la calendar policy o GerardMM.

La corrida larga terminó exactamente en el gap intrasesión visible del 23 de noviembre; no se rellena. Aunque los 13 archivos fueron inventariados, esta evidencia cubre solo el contrato diciembre 2023. No se infirió la secuencia de roll/continuidad entre contratos, no se agregaron cuentas separadas y no se reclama un backtest longitudinal continuo de 13 contratos.

El perfil congelado fue `S2_H4_TREND_BB_PULLBACK_V1`, `BTG_FUNCTIONAL_NQ_EVAL_V1`, GerardMM EVALUATION con SL USD 2,000 y TP USD 1,500 por account-day incluyendo el tercer día, SIM/GENERIC100K de USD 100,000, y `NO_ADDS_FUNCTIONAL_BASELINE_V1`. La ejecución usa `OHLC_1M_MODEL_V1`, salidas same-bar `SL_FIRST_NEXT_OPEN_V1`, 1 tick de slippage, 1 tick de offset modelado por lado, fee USD 2.49/contrato/lado y calendario America/Chicago compartido. Los resultados reflejan barras OHLC modeladas; no son ticks/BBO observados ni equivalencia con operación real.

### Intentos conservados

Se preservaron fallos previos que probaron el fail-closed: un tramo con gap abierto (`SOURCE_COVERAGE_INCOMPLETE`), barras fuera de calendario y una corrida cruda longitudinal rechazada por intervalos de sesión no válidos. No se etiquetan como baseline válido ni se ocultan bajo la derivación; sus RunID, causas y rutas están en el JSON de evidencia.

### Evidencia reproducible

El detalle pesado de métricas, comandos, hashes, ventanas, resúmenes de resultados, reproducciones y fallos está en `/home/kor/aranea/work/btg-s01-20261006/reports/historical-smoke/historical-smoke-evidence.json`. Los resultados gzip, RunSpecs sellados, logs y `/usr/bin/time -v` están bajo `/home/kor/aranea/work/btg-s01-20261006/reports/real-history-execution/`. Los run IDs y SHA arriba son el vínculo inmutable desde este apunte a los datos completos.

## Fuentes

- [[BTG-S01-REAL-GERARD-PLAN]]
- [[BTG-S01-REAL-GERARD-RESULT]]
- [[BTG-S01-REAL-GERARD-PROJECT]]
- [[BTG-S01-REAL-GERARD-ROOT-LOG]]
- Copia Owner y manifiesto local: `/home/kor/aranea/work/btg-s01-20261006/reports/historical-smoke/corpus-manifest.json`.
- Derivación y exclusiones por calendario compartido: `/home/kor/aranea/work/btg-s01-20261006/reports/real-gap-forensics/derived-nt-weekly-v1/exclusions-manifest.json`.
- Evidencia por corrida y reproducción: `/home/kor/aranea/work/btg-s01-20261006/reports/historical-smoke/historical-smoke-evidence.json`.
