---
type: known_error
schema_version: 1
scope: application
created: 2026-08-14
updated: 2026-08-14
area: "[[Echo]]"
project: "[[Echo Forge - Etapa 6]]"
application: "[[symphony]]"
entities:
  - "[[Symphony]]"
  - "[[Echo Forge]]"
related:
  - "[[symphony-mt5-backtest-report-htm-absent]]"
aliases:
  - utf-16 journal sanitizer
  - mt5 log utf16
confidence: verified
source_session: "[[2026-08-14-1620-echo-forge-etapa6-close-raw]]"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/echo
  - tech/mt5
  - project/echo-forge
---

# symphony-mt5-utf16-journal-sanitizer-bypass

## Síntoma

- Los journals subidos (`.agent.log` / `.tester.log` / `.terminal.log`) están en UTF-16 LE.
- `sanitizeLog` no redacta IPs ni paths porque opera sobre texto UTF-8.

## Causa

- MT5 escribe journals en UTF-16. El sanitizer aplica regex UTF-8 sobre esos bytes.

## Impacto

- Pueden quedar literales `127.0.0.1` y un path portable de instalación. No se vieron credenciales ni IPs del cluster en el E2E `example_flow_3`.
- No bloquea Etapa 6; es residual de evidencia, no de `report_not_found`.

## Detección

- Decodificar el objeto MinIO como UTF-16 LE y buscar IPv4 / `[A-Za-z]:\`.

## Mitigación

- Decodificar UTF-16 (y UTF-8) antes de `sanitizeLog`. Hasta entonces, no tratar el journal crudo como texto sanitizado.

## Evidencia

- E2E 2026-08-14, `09_mt5_backtest` agent.log de `example_flow_3`.
- Código: `sqx/adapters/mt5/log_snapshot.go` `sanitizeLog`.
