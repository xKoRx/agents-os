---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-06"
updated: "2026-10-06"
area: "[[Personal]]"
project: "[[Echo Futures]]"
application:
entities: []
related:
  - "[[BTG-S01-NQZ3-REAL-HISTORICAL-EXECUTION]]"
aliases: []
agent_surface: "[[Codex]]"
agent_model: gpt-6-luna
model_source: host
task_type: mixed
task_complexity: high
outcome: success
verification: passed
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-10-06-codex-gpt-6-luna-historical-smoke

## Trabajo

- **Objetivo:** Ejecutar la smoke histórica S2/GerardMM con datos NQ transferidos por Owner, medir una ventana longitudinal continua y reproducir resultados en procesos frescos.
- **Alcance atribuible a esta combinación superficie×modelo:** inventario y hashes de la copia local, validación de NT, preparación funcional del CLI existente, corrida offline, análisis de operaciones/economía/lifecycle, fresh reproduce y handoff documentado. La reparación de counters/lifecycle diagnósticos y su suite enfocada fueron atribuibles al agente TOP; aquí se usó el binario de commit `d69d03e` tras sus pruebas reportadas PASS.
- **Artefactos afectados:** `BTG-S01-NQZ3-REAL-HISTORICAL-EXECUTION.md`; registro de ejecución; evidencia externa bajo `/home/kor/aranea/work/btg-s01-20261006/reports/historical-smoke/` y logs/results en `reports/real-history-execution/`.

## Evidencia

- **Validaciones ejecutadas:** los 13 archivos de copia local fueron leídos y hasheados; verificación de formato, orden, duplicados, tick y OHLC pasó. El filtrado derivado usó el resolver y `bars.Grid.RegionAt(1m)` del calendario compartido, preservó gaps intrasesión y tuvo manifiesto por fila. Smoke COMPLETE: 136,932 registros; 24 fills; balance final USD 90,029.30. Longitudinal COMPLETE: 270,781 registros; 78 fills, 113 operaciones, balance final USD 65,706.68. Ambas reproducciones fresh-process dieron `IDENTICAL`; los artefactos comprimidos mantuvieron mismo SHA. Los CLI se ejecutaron aislados de red.
- **Resultado observable:** PnL negativo legítimo bajo el perfil congelado; corrida de 19 account-days activos dentro de 39 account-day IDs observados; costo y drawdown medidos desde la serie de eventos de equity. El último cierre protector dejó la posición plana pero la última operación `ACTIVE`; se conservó como residual real conforme `REPORT_RESIDUALS`.
- **Limitaciones de la evidencia:** un único contrato (archivo físico NQ 12-23, explícitamente mapeado a NQZ3), no trece contratos en continuidad. Se excluyeron 226 filas fuera de sesión de los trece archivos; se retuvieron todos los gaps intrasesión. Los bytes locales se verificaron, pero no se pudo comparar con el directorio origen inaccesible. OHLC modelado no equivale a ticks/BBO ni LIVE.

## Evaluación

%% Scores opcionales 1–5: agregar al frontmatter sólo cuando exista evidencia suficiente. Si son autoevaluados, conservar evaluator: agent. %%

- Sin scores autoasignados; el owner mantiene la aceptación final S01.

## Resultado

- **Outcome:** completado para smoke y longitudinal single-contract; fresh reproductions idénticas.
- **Rework posterior:** unknown; no hay feedback del usuario todavía.
- **Aprendizaje para comparar herramientas:** distinguir contadores físicos SOURCE_CLOSE de root-input ordinals; conservar un filtro calendario auditable por fila sin borrar gaps de mercado; verificar lifecycle residual y fresh-process determinismo sobre un resultado real.
