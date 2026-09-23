---
type: feedback
schema_version: 1
scope: session
created: "2026-09-23"
updated: "2026-09-23"
area: "[[Aranea]]"
project: "[[The Lab]]"
entities:
  - "[[Echo]]"
related:
  - "[[I — Independent Verification D1 (Shot 2)]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (account:zai-individual-coding-plan)
agent_run: "[[2026-09-23-zcode-glm53-d1-echo-foundation-shot2]]"
session_goal: INDEPENDENT VERIFICATION shot 2 de D1 Echo Foundation (falsificación adversarial del PASS de Shot 1 con veredicto y reproducers)
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agentsos
  - agent/system1
---

# Session Feedback - 2026-09-23 - d1 echo foundation shot2

## Fricciones y lecciones del entorno (para la próxima sesión de verificación en Echo)

- **psql/postgres no están en PATH** del shell base: los binarios reutilizables viven en `/tmp/echo-e08-pg/postgresql-17.11.0-x86_64-unknown-linux-gnu/bin` y requieren `LD_LIBRARY_PATH=/tmp/echo-e08-pg/libs` (si no, el ejecutable `postgres` falla con "command not found" por `libxml2.so.2`). Todo harness debe anteponer ambos.
- **Varios PG desechables ya corren** (15432/15441/15445/15446/15447): no reutilizar el 15445 de Shot 1 (PGDATA ajeno); levantar instancia propia en puerto nuevo con PGDATA en disco (no tmpfs).
- **`echo.strategy_versions` es write-once** (trigger `IDENTITY_BWC_WRITE_ONCE`, E-03): los tests que limpian no pueden DELETE la tabla; usar TRUNCATE multi-tabla como los harnesses E-03/E-04 o seeding idempotente `ON CONFLICT DO NOTHING` con cleanup sólo de `canonical_operations`/`strategy_history_state`.
- **`strategy_identity_mappings.strategy_ref` exige forma UUID** (`chk_identity_mappings_strategy_ref`): los fixtures deben generar refs UUID-shaped.
- **`GOWORK=off` rompe la resolución entre módulos v3** (go.sum del workspace): correr suites por módulo con GOWORK=off sólo dentro del módulo, o con el `go.work` del repo desde la raíz; para el baseline (checkout sin go.work, untracked) usar un go.work EXTERNO apuntando a los módulos del checkout, nunca crear archivos dentro del repo del desarrollador.
- **Decimales canónicos del wire son estrictos** (`1.0`/`149.50` se rechazan por trailing zero): los fixtures de test deben usar forma canónica; esta fricción confirmó positivamente el comportamiento de canonicalización.

## Feedback al proceso D1

- El modelo de tres shots funciona: los dos defectos encontrados (torn read del GET y truncado sub-segundo de la proyección) son de la superficie de lectura y no fueron cubiertos por el Test Plan §4 ni por los tests de Shot 1; conviene añadir al Test Plan de futuros shots un caso explícito de "GET consistente bajo replacement concurrente" y "fidelidad temporal de la proyección de lectura".
