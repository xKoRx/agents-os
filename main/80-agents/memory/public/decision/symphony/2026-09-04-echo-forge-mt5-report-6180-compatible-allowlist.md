---
type: decision
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-mt5-report-6140-compatible-allowlist]]"
  - "[[2026-09-04-mt5-terminal-build-unsupported]]"
aliases:
  - BUILD_6180_COMPATIBLE_WITH_MT5_REPORT_V1
  - SUPPORTED_FORMAT_UNCERTIFIED_BUILD 6180
confidence: verified
source_session: ECHO-FORGE-MT5-BUILD-6180-PARSER-CERTIFICATION-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-echo-forge-mt5-report-6180-compatible-allowlist

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Recert física Finalist Factory V1 sobre release `0.2.95` (`0f18ef0440e104c6a38ba4cc259f674cfad3c390`) se detuvo fail-closed antes de Campaign: `WORKER-KRONOS` FileVersion `5.0.0.6180` vs allow-list `{6090,6140}` → `MT5_RUNTIME_BUILD_NOT_CERTIFIED`.
- Política congelada: Live Update permitido; build desconocido fail-closed; sin rango numérico; certificar cada build con reporte físico. No pinnear/downgrade a 6140.

## Decisión

- **BUILD_6180_COMPATIBILITY = COMPATIBLE_WITH_MT5_REPORT_V1.** Clasificación primaria: `SUPPORTED_FORMAT_UNCERTIFIED_BUILD`. `parser_version` permanece `mt5-report.v1`.
- Allow-list explícita debe pasar a `{6090,6140,6180}` en un NORMAL posterior. Vecinos `6179`/`6181`/`6200` siguen rechazados. Sin `build >= 6090` y sin rango.
- Fixture físico durable: SHA-256 `6c9e975fff5b9821257d250a9877bcba87f5adce69f14d3bc396821056076485`, 28572 bytes, UTF-16LE+BOM, fila `Darwinex-Demo (Build 6180)` una sola vez. `Parse()` sobre bytes originales → `ErrBuildNotSupported{build=6180}`. Ignorando sólo el gate de allow-list: `Parse()` nil, 7/7 crosschecks PASS, `Normalize()` `TradeSet EMPTY` (`mt5-normalize.v1`).
- Margin Level en este reporte: label vacío → `MISSING NOT_REPORTED` (igual que fixtures 6090 ZT). El `414.35%` INVALID de 6140 mixed sigue deuda no bloqueante congelada; no es drift de 6180.

## Rationale

- Encoding, 2 tablas, headings, headers Orders (11) y Deals (13), labels Settings/Results y gramáticas numéricas coinciden con `mt5-report.v1` y con fixtures 6090 ZT / 6140 mixed.
- El Expert F0 usado tiene `mmLots=0.0` → muestra zero-trade. Eso certifica el camino degenerado del corpus 6090 ZT; las filas operacionales de Orders/Deals no se ejercieron en 6180. Los headers son idénticos a 6090/6140. Residual no bloqueante: no hay filas filled/in-out 6180.
- Live Update produjo 6180; el producto falló cerrado como está diseñado. El siguiente desbloqueo es allow-list + fixture, no pin del terminal.

## Consecuencias

- NEXT EXACT: `ECHO-FORGE-MT5-BUILD-6180-ALLOWLIST-V1-NORMAL`. Después, reanudar la misma recert Finalist Factory V1 sobre un release nuevo. No rediseñar Campaign/Replenishment/caps.
- Replay Temporal: el gate vive en `mt5_reconcile_v1`; ampliar allow-list no cambia decisiones de workflow.

## Alternativas descartadas

- Pin/downgrade a 6140: viola la política congelada y no escala.
- `build >= 6090` o rango `6090–6180`: viola fail-closed.
- `mt5-report.v2` por el solo hecho de ser build nuevo: la evidencia estructural no lo exige.
- Segunda smoke mixed para igualar 6140: superaría el cupo de un job MT5 ya completado; headers idénticos y ZT es régimen canónico del corpus v1.
