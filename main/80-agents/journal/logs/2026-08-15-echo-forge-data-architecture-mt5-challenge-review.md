---
type: change_log
schema_version: 1
scope: session
created: "2026-08-15"
updated: "2026-08-15"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
  - "[[2026-08-15-echo-forge-g0l-owner-amendments]]"
related:
  - "[[2026-08-15-mt5-html-parser-fail-open-signed-costs]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/echo-forge
  - area/echo
  - kind/change-log
  - kind/changelog
  - project/echo-forge
  - scope/session
---

# Echo Forge — revisión arquitectónica challenge-first y contrato MT5

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Reconciliación y Scoring MT5.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - `80-agents/memory/public/decision/symphony/2026-08-15-echo-forge-g0l-owner-amendments.md`

## Motivo

- Reemplazar una propuesta física prematura y un gate bidireccional duplicable por un modelo lógico challenge-first, una fuente canónica del binding y gates explícitos de aprobación lógica, diseño físico MVP, vertical MT5 y validación posterior.
- Aplicar los amendments aprobados por el owner y organizar el trabajo por capacidad TOP/NORMAL sin reabrir el significado funcional decidido.
- Es Sistema 2 current truth porque cambia planners de proyectos activos, sus contratos, gates, tareas y el estado resumido del programa; no es una memoria reutilizable ni un relato de sesión.

## Fuentes usadas

- Checkout local `xKoRx/symphony` en commit `b5c71d5`, inspeccionado en modo sólo lectura.
- `GenericSQXWorkflow`, contratos runtime, `CanonicalStrategyID`, adapters Mongo/PostgreSQL/MinIO, catálogo/MetricValue, trade manifests, comparación/ranking/decisiones y SDDs relevantes.
- Fixtures MT5 zero-trade y all-loss, incluido el caso de costos firmados registrado en [[2026-08-15-mt5-html-parser-fail-open-signed-costs]].

## Resolución aplicada

- La arquitectura ahora distingue FlowRun, Strategy, StageExecution, Evaluation, MetricSet, TradeSet, ArtifactRef, Score, RankingSnapshot y Decision, con lifecycle, cardinalidad, ownership, queries y recovery explícitos.
- `EvaluationResult` paralelo y `ScoreRun` universal se rechazan; `logical_type` conserva su nombre/mecanismo y queda como estructura estable de identidad descriptiva sin implicar PK.
- FlowRunStrategy preserva un origen autoritativo y participaciones posteriores; MetricSet/TradeSet referencian Evaluation sin arrays inversos autoritativos; RankingSnapshot mantiene abierto el storage de entries.
- `Strategy-MT5 Binding v1` tiene una sola fuente canónica en arquitectura; MT5 consume el contrato por referencia y mantiene conformance funcional.
- `G0-L = APPROVED_BY_OWNER / CLOSED`; G0-P pasa a `MVP_PHYSICAL_DESIGN`, G1-MT5 depende de ese diseño y G2-REAL-WORKLOAD valida assumptions después de waves.
- Arquitectura queda agrupada A0–A5 y MT5 M0–M7, con modelo TOP/NORMAL y reglas de escalamiento visibles por fase.
- No se modificó código productivo ni se aprobó una tabla, collection, UUID o threshold de enforce.

## Validación

- Schema contract: PASS (`errors=0`).
- Lint estricto dirigido sobre las tres notas, la decisión, este change log y el agent run: PASS (`ERROR=0`, `WARN=0`).
- Tag lint dirigido sobre esos seis artefactos: PASS (`6/6`, cero hallazgos). El lint global fue ejecutado y conserva deuda heredada fuera de este cambio (`1115` archivos con errores, `2549` hallazgos).
- AGENTS OS doctor: `HIGH=0`; conserva un `MEDIUM` heredado por `signals-spec-authoring` ausente del índice de skills.
- Revisión de links, contradicciones y separación de proyectos: PASS dirigida; referencias legacy aparecen solo en challenges, migración o bitácora histórica.
- Graphify `update`: PASS; reconstruyó `62185` nodos, `133122` edges y `2717` communities, y actualizó el reporte canónico. La visualización HTML se omitió por exceder el límite de 5000 nodos, sin afectar `graph.json` ni `GRAPH_REPORT.md`.
- Gap no bloqueante: la escala futura se expresa como assumptions/rangos en G0-P y se valida con datos reales en G2; no se exige medir el sistema nuevo antes de diseñarlo.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni memoria interna; solo rutas relativas del vault y referencias de dominio necesarias para auditoría local

## Rollback

- Restaurar las versiones previas de las tres notas desde Git. No hay migración ni cambio de datos que revertir; el checkout de Symphony permanece intacto.
