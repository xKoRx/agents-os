---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Echo Futures]]"
related: []
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 NT minute ingress implementation

## Propósito

Documentar la implementación de la entrada nativa NT Last de un minuto y su contrato de identidad para BTG-S01.

## Contenido

El código quedó congelado en la rama `codex/btg-s01-ntminute-ingress`, commit `933b40d65d7fe0946bb5b75038f6c4858d9912ea` del repositorio Echo. Añade `HistoricalRecord.SourceBar` exclusivo, el modelo explícito `OHLC_1M_MODEL_V1` y un adaptador limitado por streaming que valida campos, tick grid, orden, receipts físicos, identidad lógica, selección y gaps sin rellenarlos.

El modelo exige offsets bid/ask proporcionados por el llamador, incluso para cero, y las políticas `SL_FIRST_NEXT_OPEN_V1`, `FAIL_VISIBLE_INTRABAR_AMBIGUITY_V1`, `FAIL_VISIBLE_GAPS_V1`, `SETTLE_CLOSE_BOUNDARY_TIMERS_NEXT_OPEN_V1`, `ADVERSE_FAVORABLE_CLOSE_AT_END_V1` y `NO_ADDS_FUNCTIONAL_BASELINE_V1`. No se modificó SDK, estrategia, MM, driver, venue ni contabilidad; esta implementación no habilita ejecución OHLC ni presenta resultados económicos.

Las verificaciones offline dirigidas pasaron; el lector NT obtuvo 244/256 (95,3%) sentencias ejecutables cubiertas. La serialización y los digests legacy coinciden exactamente con el baseline limpio. La nota `VERIFICATION.md` en el SDD registra comandos, oracle, cobertura y límites.

Las pruebas usan el valor observado `20231211 030000;16053.5;16054;16053.25;16053.5;35` como regression del parser y otros fixtures sintéticos para reglas. No se adquirieron los 13 archivos originales: el perfil de SFTP autorizado rechazó la descarga con `POLICY_DENIED`. No se afirma cobertura integral, gaps libres, señales, fills, PnL ni paridad BBO.

## Fuentes

- [[BTG-S01-NT-CANDLES-ACQUISITION]]
- [[BTG-S01-NINJATRADER-ACQUISITION]]
