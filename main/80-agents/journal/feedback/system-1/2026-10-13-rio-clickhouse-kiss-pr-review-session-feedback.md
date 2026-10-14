---
type: feedback
schema_version: 1
scope: session
created: 2026-10-13
updated: 2026-10-13
area: "[[Meli]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[RIO E2E local]]"
related: ["[[2026-10-13-codex-gpt-6-rio-clickhouse-kiss-pr-review]]"]
aliases: []
agent_surface: "[[Codex]]"
agent_model: GPT-6
agent_run: "[[2026-10-13-codex-gpt-6-rio-clickhouse-kiss-pr-review]]"
session_goal: "Abordar y responder revisión de PRs ClickHouse KISS"
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback — revisión ClickHouse KISS

## Context

- [[Codex]] / `GPT-6` declarado por el host; [[RIO E2E local]], ejecución [[2026-10-13-codex-gpt-6-rio-clickhouse-kiss-pr-review]]. Los dos comentarios aplicaban: idempotencia SQL y recuperación Kafka.
- Se reutilizó contexto warm; cierre con [[agents-os-session-close]] y registro con [[agents-os-agent-run-register]].

## What Complicated The Session Most

- Introduje una regresión al cambiar la comparación de MV al normalizador compartido sin probar GROUP BY/HAVING/ORDER/LIMIT. Los tests del SELECT simple no cubrían una cláusula común de las MVs incrementales; el reviewer detectó lo que debía haber verificado antes.
- Reutilicé el factory de resultados sin revisar su resolver binario de DLT. Runtime era un tercer canal, pero su caso de error quedaba etiquetado como action-result. Compartir transporte exige comprobar el contrato de fallo, no sólo que el mensaje llegue al controller.

## Most Useful Part Of Sistema 1

- Los presupuestos y el alcance aceptado evitaron otra expansión: CH tocó sólo los dos archivos existentes del parser; PM agregó el factory de runtime en su listener existente y reutilizó productor, byte consumer y reintentos de F1.
- La reproducción roja de los tres round-trips y las pruebas de destino DLT/bytes/key/reintentos/publicación fallida hicieron verificables las respuestas al reviewer.

## Least Useful Or Noisy Part

- Dejé las descripciones con enlace al proyecto, pero sin la referencia inversa desde la entrega vigente. El owner tuvo que pedirlo: un recurso guardado no queda integrado al trabajo actual hasta cerrar ambos sentidos del enlace.
- Releer bootstrap y volver a agrupar lecturas grandes en un turno warm aportó poco y produjo truncamiento. Bastaba recuperar los dos comentarios, sus fuentes directas y el delta de cierre.

## One Next Improvement

- Antes de reutilizar una comparación o un factory, probar una entrada productiva representativa y su ruta de error: SQL agregado con identificadores sensibles a case, y cada canal Kafka con su DLT y fallo de publicación. Mantener la prueba en los archivos pertinentes existentes.
