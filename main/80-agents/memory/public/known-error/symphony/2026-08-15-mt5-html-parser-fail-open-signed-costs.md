---
type: known_error
schema_version: 1
scope: application
created: "2026-08-15"
updated: "2026-08-15"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[echo-forge]]"
related:
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
aliases:
  - MT5 parser UTF-16 fail-open
  - MT5 signed costs bug
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - area/echo
  - kind/known-error
  - project/echo-forge
  - scope/application
  - tech/echo-forge
---

# MT5 HTML parser fail-open y costos firmados

## Síntoma

- Un reporte Strategy Tester real UTF-16LE puede producir parse exitoso con métricas vacías convertidas a `0`, Profit Factor `999` y cero deals, en vez de fallar.
- El net profit derivado por deal puede aumentar al aplicar una comisión negativa, contradiciendo el balance y el footer del HTM.

## Causa

- `sqx/adapters/mt5/parser.go` entrega el stream UTF-16 directamente al parser HTML, acepta string vacío como cero, convierte missing/NaN/Inf a valores numéricos y omite errores en varios campos.
- El extractor toma sólo el primer par label/value por fila y busca headers en la primera fila decorativa, por lo que pierde métricas y tablas del formato real.
- La fórmula vigente usa `profit - commission - swap`, pero el HTM representa commission y swap con signo; el balance usa `profit + commission + swap`.

## Impacto

- Estrategias pueden recibir métricas y scores plausibles pero falsos; missing data se confunde con evidencia observada y la reconciliación SQX/MT5 queda corrupta.

## Detección

- Verificar BOM/encoding antes de parsear y exigir labels/tablas obligatorias.
- Reconciliar `sum(profit) + sum(commission) + sum(swap)` contra Total Net Profit y cambio de balance.
- En `repo:symphony/mt5-export.htm`, `-441,40 + -63,15 + 0 = -504,55`; balance inicial `10.000` y final `9.495,45` confirman la semántica.

## Mitigación

- Decodificar UTF-16LE de forma explícita, declarar locale, ubicar secciones/headers semánticamente y fallar cerrado ante estructura desconocida.
- Representar `observed`, `derived`, `missing` e `invalid`; no usar cero ni `999` como sustitutos de ausencia/infinito.
- Aplicar costos con su signo y agregar goldens zero-trade, all-loss, mixed win/loss y variantes reales de locale/build.
- Corregir primero los artefactos SDD que hoy prescriben resta y sentinels antes de modificar código productivo.

## Evidencia

- `repo:symphony/mt5-export.htm`, SHA-256 `090ca4d16407598f67c0ad52de43fae8012c7e4043c99db7a559d77657f79326`.
- `repo:symphony/sqx/adapters/mt5/parser.go` y `repo:symphony/specs/FEAT-SQX-MT5-BACKTEST-COMPILE/SPEC.md`.
