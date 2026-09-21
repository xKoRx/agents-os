---
type: agent_run
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[2026-09-21-historical-backtest-readiness]]"
aliases: []
agent_surface: "[[Cursor]]"
agent_model: Grok 4.7
model_source: host
task_type: coding
task_complexity: high
outcome: partial
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

# Agent Run — 2026-09-21-cursor-grok-4.7-historical-backtest-readiness

## Trabajo

- **Objetivo:** dejar PE-005-R1 listo para un backtest histórico causal, o demostrar qué dato indispensable no existe.
- **Alcance atribuible a esta combinación superficie×modelo:** barrido remoto de tick y `new_market`, pruebas de ancla y de inbox, SCREEN/REPLAY/SHADOW con parámetros congelados, certificación no-live y publicación.
- **Artefactos afectados:** `xKoRx/polymarket-engine` código `66486ac` y recibo `09e8c76`; resultados JSON en `historical-m0/readiness`; notas del change log [[2026-09-21-historical-backtest-readiness]].

## Evidencia

- **Validaciones ejecutadas:** `gofmt`, `go vet`, `go test ./...`, `go test -race ./...`, `journal verify` de los cuatro journals, `engine experiment certify --profile no-live --baseline 66486ac` con outcome `M4_CERTIFIED_NON_LIVE` 27/0/5.
- **Resultado observable:** `DESCRIPTIVE_ONLY`. SCREEN `cuts=30` completo, 0 oportunidades. Shadow `INCONCLUSIVE`. El tick `0.01` está acreditado sólo por un `old_tick_size` posterior a la ventana.
- **Limitaciones de la evidencia:** el sha256 del parquet horario completo no se recalculó en local. Wayback respondió 503. El kickoff sigue siendo posterior a la decisión. `Qualities` lee el régimen ya proyectado, no el régimen conocido en el instante del libro.

## Evaluación

- **Correctness:** no se fabricó tick ni fee, no se abrió el OOS y no se alteró el modelo de calidad ni la campaña semanal.
- **Autonomy:** el veredicto descriptivo se cerró sin una decisión intermedia. La única decisión de modelo queda nombrada y no es necesaria para aceptar este resultado.
- **Efficiency:** el barrido usó predicados remotos. Las copias de journal usadas por SCREEN se borraron después de conservar los JSON.

## Resultado

- **Outcome:** partial. El estudio descriptivo es reproducible. No hay cohorte causalmente elegible.
- **Rework posterior:** unknown
- **Aprendizaje para comparar herramientas:** un `old_tick_size` posterior demuestra el valor que regía, y no es un hecho que el reducer congelado pueda aplicar hacia atrás sin cambiar el modelo.
