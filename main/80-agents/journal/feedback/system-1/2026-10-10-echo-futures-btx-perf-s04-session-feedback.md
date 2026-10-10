---
type: feedback
schema_version: 1
created: "2026-10-10"
updated: "2026-10-10"
area: "[[Echo Futures]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[ZCode]]"
aliases: []
feedback_type: friction
severity: low
status: open
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/system-1
---

# Feedback — BTX-PERF-S04 (go tooling frictions en Daedalus)

- `go test ./backtester/` (paquete completo del backtester, ~11 min con suites E2E CLI) muere con el timeout default de 600s de go: la suite necesita `-timeout 40m`. Recurrente (ya observado en S02, re-confirmado por el verificador interno S04 con `FAIL … 600.081s` y segunda pasada limpia con `-timeout 40m`). Candidato a runbook/memoria del repo: todo comando de suite completa del backtester debe llevar timeout explícito ampliado.
- `go -C <dir> test -coverprofile=<ruta-relativa>` resuelve la ruta relativa DESPUÉS del cambio de directorio: el perfil se intenta escribir bajo `<dir>/<ruta>` y el run aborta con "no such file or directory" tras perder la corrida completa. Usar siempre ruta absoluta para `-coverprofile` cuando se combina con `-C` o con `cd` en subshells. Coste observado: una corrida de coverage ~20 min perdida en S04.
