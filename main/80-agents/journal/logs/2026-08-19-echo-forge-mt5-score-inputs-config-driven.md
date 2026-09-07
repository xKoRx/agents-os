---
type: change_log
schema_version: 1
scope: session
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
related:
  - "[[2026-08-19-1010-cursor-grok-4.6-echo-forge-mt5-score-inputs]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge MT5 — Score inputs config-driven

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Reconciliación y Scoring MT5.md`
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
  - repo `xKoRx/symphony`: `eba11f0` (`fix: make score inputs config-driven`)

## Motivo

- M6-TOP resolvía el baseline del Score con el primer `trade_list_exporter`. Owner exigió selector explícito por config (`task` name + `metric_set`) sin acoplar a stage/folder.

## Fuentes usadas

- Decisión owner de esta sesión. HEAD previo `2fb01df`.

## Resolución aplicada

- `WorkflowSpec.Scores` selecciona MetricSet(s) por `TaskSpec.Name`. Lookup fail-closed. Configured period sale del producer baseline declarado. `CanonicalPeriodDate` rechaza fechas calendario inválidas.

## Validación

- `go test` / `-race` / `go vet` en runtime, evaluation y worker: PASS. Push a `master`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir `eba11f0`.
