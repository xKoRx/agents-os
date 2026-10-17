---
type: session_feedback
schema_version: 1
created: "2026-10-17"
updated: "2026-10-17"
area: "[[Aranea]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[aranea-agent-dev]]"
related:
  - "[[2026-10-17-fe2-single-flow-e2e-lessons-feedback]]"
severity: medium
category: process
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
---

# Feedback — Reconciliación post-E2E: el informe de certificación afirmó 2 hechos de control plane sin leerlo

**Qué pasó (2026-10-17, FLOW_EXAMPLE_2):** el informe `E2E-FINAL-CERTIFICATION.md` de la sesión E2E quedó publicado con dos afirmaciones falsas que una reconciliación read-only posterior detectó de inmediato: (1) la tabla por tipo lógico decía "finalistas con trades MT5 > 0: 5/5" en los 6 grupos cuando el CSV durable del MISMO bundle muestra 16/30 con cero trades, 14/30 con trades y 0 con beneficio MT5 positivo; (2) PRE_ECHO declaraba "forge_seal_handoff: ZERO" cuando la historia Temporal muestra que `forge_seal_handoff_v1` ejecutó y COMPLETÓ tras `promote_finalists` (lo que es cero es la entrega real a Echo: 30 deliveries en `HANDOFF_CREATED` con `ingress_not_configured` y 0 versiones/promotions en la BD de Echo PROD). El PASS E2E (pipeline físico) sigue siendo válido; las afirmaciones erróneas eran de alcance e interpretación, no de ejecución.

**Por qué importa:** un informe de certificación que resume veredictos con cifras y "cero X" sin contrastarlos contra la capa que posee la semántica (CSV durable, Temporal, PG control plane, BD del consumidor) siembra decisiones erróneas río abajo (p.ej. creer que las 30 finalistas tienen trades MT5 y son candidatas operativas). El costo de la verificación era una consulta por fuente; el costo del error es una certificación con lectura engañosa.

**Lección accionable:** en informes de certificación, toda cifra agregada (N/N, "cero X") y toda afirmación PRE_ECHO debe citarse de una lectura durable del control plane hecha en la misma sesión (PG/Temporal/Mongo/CSV del bundle), con la fuente anotada en el informe; los contadores de actividad y los resultados de negocio viven en capas distintas y ninguna se infiere de la forma del pipeline. Aplica también a [[forge-wave-dispatch]]: sección de veredicto = tabla claim→fuente→valor, sin celdas inferidas.

**Notas de sesión (agente):** sesiones MCP aranea (Temporal, Mongo, Postgres) expiraron o apuntaron a namespace/BD distintos del objetivo (Temporal MCP en sqx-dev vs FlowRun en sqx-prop; postgres-ro en BD echo vs trading_systems_test); el patrón efímero ya probado (helper Go con DSN/config desde ETCD + rutas MCP correctas) volvió a ser la vía práctica. El helper de historia Temporal read-only (`--history`) añadido a las herramientas de sesión no muta nada y fue suficiente para certificar la secuencia de eventos.
