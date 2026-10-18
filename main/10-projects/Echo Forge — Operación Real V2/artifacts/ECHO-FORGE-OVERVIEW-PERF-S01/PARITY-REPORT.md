---
type: evidence_doc
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/evidence
  - area/echo
  - tech/performance
---

# PARITY-REPORT — baseline vs candidato, mismo corpus auténtico

## Protocolo

Mismo corpus pristine restaurado + SHA verificado antes de cada run; mismo entorno (copia candidate-local en Kronos), mismo comando, misma JVM. Comparación con `parity.py` (en `bench/`): parse NDJSON línea a línea, eliminación de campos legítimamente variables de ejecución (`job_id`, `exported_at`, `finished_at` — derivados del timestamp del run), normalización canónica de claves y comparación profunda fila a fila en el MISMO orden. Casos inválidos y errores: contados por los manifiestos (deben ser idénticos).

## Resultados

### Corpus estándar (24 estrategias NDX, 48.000 trades)

- Baseline: `out/deployed-baseline` (run3, jar desplegado 0.3.1 vía snippet) vs Candidato: `out/candidate-real` (run3, Snippets.jar con clases del candidato).
- `overview.ndjson`: 24 vs 24 filas, mismo orden, **0 diffs**.
- `monthly.ndjson`: 2.976 vs 2.976 filas, mismo orden, **0 diffs**.
- Conteos del log del exporter idénticos: `seen=24 written=24 errors=0 monthly_rows=2976` (0 errores ambos → misma política de casos inválidos ejercitada).
- Normalización usada: `job_id`, `exported_at`, `finished_at` solamente.

### Corpus heavy (6 estrategias NDX_W3_80oosSPP_V1, 16.000 trades, 2,6–5,4 MB)

- Baseline: `~/SQX_exports/overview_json` (heavybase, corrió sin exporter.properties → defaults de config) vs Candidato: `out/heavy-candidate`.
- `overview.ndjson`: 6 vs 6, **0 diffs**; `monthly.ndjson`: 739 vs 739, **0 diffs**.
- Normalización extra documentada y JUSTIFICADA: `wave_key`, `instrument`, `timeframe`, `direction` (eco de configuración del run, no resultados; difieren porque el run baseline heavy no tenía properties — defecto del protocolo corregido a posteriori, no del candidato). Con la normalización estándar las únicas diferencias eran exactamente esos 4 campos en 6/6 y 739/739 filas.

## Elementos de paridad verificados

Mismos StrategyRefs/identidades (`strategy_name`/`strategy_id` por fila), mismas métricas (`metrics`/`overview` por muestra full/in/oos), mismos indicadores y bloques clasificados (`entry_indicators`, `exit_indicators`, `price_indicators`, `*_blocks`, `strategy_parameters_detected`, `strategy_structure_diagnostics` con misma fuente/longitud de XML), mismos monthly aggregates (739 y 2.976 filas), mismos conteos de trades (`trade_field_diagnostics`), mismos valores numéricos (comparación profunda exacta post-normalización de timestamps), mismos errores (0/0), mismo orden lógico de registros.

## Veredicto

**PARITY = EXACTA en ambos corpus.** Una mejora de rendimiento que modificara resultados es FAIL por mandato; no ocurrió.
