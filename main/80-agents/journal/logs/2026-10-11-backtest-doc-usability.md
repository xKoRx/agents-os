---
type: change_log
schema_version: 1
scope: session
created: "2026-10-11"
updated: "2026-10-11"
area: "[[Personal]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[BTX-PERF-LAST-FINAL]]"
aliases: []
confidence: verified
source_session: sess_2299342a-86fe-4ca6-9ad2-b9979bff02e9 (ZCode)
source_feedbacks:
  - "[[2026-10-11-backtest-doc-usability-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-11-backtest-doc-usability

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BACKTEST-DOC-USABILITY-REPORT.md` — informe de usabilidad del manual `v3/backtester/README.md @ c75023c8`: veredicto EJECUTABLE_SOLO_CON_DOC, nota 9/10 (preparación 2, comandos 2, ejecución/replay 2, interpretación 1, diagnóstico 2), 5 problemas menores con corrección textual propuesta.
  - `80-agents/journal/feedback/system-1/2026-10-11-backtest-doc-usability-session-feedback.md` — feedback event-driven de la sesión.
  - `80-agents/journal/sessions/raw/2026-10-11-backtest-doc-usability-raw.md` — L0 de auditoría.

## Motivo

- Encargo ONE-SHOT del Owner: probar si un agente nuevo puede operar el backtester (BASIC+CAMPAIGN NQZ5 + replays oficiales) solo con el manual y calificar la documentación.

## Fuentes usadas

- Manual bajo prueba (commit exacto indicado por el encargo), release `btx-perf-last-20261010`, recetas §2–§4 y diagnóstico §8 del propio manual.

## Resolución aplicada

- Instalación nueva completa probada (descarga, 3 niveles de checksum, identidad del binario `0320b80e…`); BASIC NQZ5 COMPLETE rc0 858 s; CAMPAIGN NQZ5 COMPLETE rc0 604 s; ambos replays IDENTICAL rc0; cifras de §4.3 reconciliadas al 100%. Sin edición de producto, datos ni parámetros; sin NQU6/all13/suites.

## Validación

- Estados leídos en `experiment-manifest.json` (COMPLETE) y `logs/*.replay.json` (verdict IDENTICAL); conciliación financiera contra `campaign-result.json` y `summary.economics` del artefacto; reporte diario agregado (39/22/24 y 15/6/24). Evidencia del operador en `~/echo-backtest-873/package/{runs,replay,logs}` y copia del manual con SHA en `~/aranea/work/bt-doc-usability-20261011/`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Borrar los tres archivos creados; no afecta producto, paquete ni resultados certificados.
