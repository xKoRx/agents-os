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
  - "[[2026-09-21-historical-research-m0]]"
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

# Agent Run — 2026-09-21-cursor-grok-4.7-historical-research-m0

## Trabajo

- **Objetivo:** primer experimento histórico reproducible de PE-005-R1 sobre datos reales, sin abandonar la campaña prospectiva y sin declarar la hipótesis validada.
- **Alcance atribuible a esta combinación superficie×modelo:** auditoría de contratos y fuentes, cohorte MLB, adapter `histimport`, import/replay/describe de cuatro mercados, screen y shadow, certificación no-live, publicación.
- **Artefactos afectados:** `xKoRx/polymarket-engine` código `56195c9` y recibo `de33d7d`; dataset `historical-m0`; notas del change log [[2026-09-21-historical-research-m0]].

## Evidencia

- **Validaciones ejecutadas:** `gofmt`, `go vet`, `go test ./...`, race de `histimport` y `cmd/engine`, `engine experiment certify --profile no-live --baseline 56195c9` con outcome `M4_CERTIFIED_NON_LIVE` 27/0/5.
- **Resultado observable:** `HISTORICAL_DATA_PARTIAL`. Cuatro mercados en `SYNCING`, 0 ensanchamientos descriptivos al umbral congelado, replay determinista, shadow `INCONCLUSIVE`. Sports Week intacta.
- **Limitaciones de la evidencia:** el sha256 del parquet completo no se recalculó en local; el kickoff está corroborado a posteriori; la cobertura de `histimport` quedó en 87.8%, bajo el piso 95, en ramas de error de IO y parseo.

## Evaluación

- **Correctness:** el pipeline no fabrica tick ni fee; la calidad `SYNCING` se reporta aparte del `OBSERVED_USABLE` del replay sin restricciones.
- **Autonomy:** la cohorte y el veredicto se cerraron sin pedir una decisión intermedia. La decisión que queda es del owner y está nombrada.
- **Efficiency:** las horas completas no se almacenaron. El screen congelado se cortó al quedar demostrado el inbox, para no repetir la espera en cada mercado.

## Resultado

- **Outcome:** partial. El experimento histórico es real y auditable. No hay backtest elegible para la estrategia mientras falte un tick point-in-time.
- **Rework posterior:** unknown
- **Aprendizaje para comparar herramientas:** un journal histórico válido no vuelve elegible a una estrategia cuyo gate exige un hecho que la hora no contiene.
