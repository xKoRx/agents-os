---
type: agent_memory
scope: agent
created: 2026-07-20
updated: 2026-09-09
index_priority: never
memory_state: archived
load_policy: manual
indexable: false
tags:
  - kind/agent-memory
  - scope/internal
  - area/meli
  - app/vpp-backend
---

# Continuidad — resumen Meli últimas dos semanas

- El trabajo principal de 2026-07-06 a 2026-07-20 fue Bajó de Precio Motors:
  integración VPP/Octopus para resolver previous price en VIS/VIP nativo,
  tracking `hasGoodPrice`/experimento, layouts Android/iOS, cobertura y
  correcciones de race condition mediante copias defensivas.
- La rama `feature/bajo-de-precio-motors` recibió sincronizaciones con develop,
  fixes de review/tests y una refactorización final de `PriceDeprecatedComponent`
  y sus marshallers/tracking. `pr_descripcion.md` sigue no trackeado.
- En paralelo hubo trabajo cross-repo de Polycard/Search Motors: migración del
  orden de Single View al SDK, título compuesto con `SHORT_VERSION`/dedup y
  diagnóstico de la regresión iOS de la pill entre SDK 8.182.0 y 8.182.1.
- También se avanzó el RFC/Hito 2 de Destaques de Precio, dejando preguntas
  abiertas sobre atributos, consumers, Search, rollout y FIPE/MLB.
