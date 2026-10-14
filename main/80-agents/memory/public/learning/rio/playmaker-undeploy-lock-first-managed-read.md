---
type: learning
schema_version: 1
scope: application
created: "2026-10-13"
updated: "2026-10-13"
area: "[[Meli]]"
project: "[[RIO E2E local]]"
application: "[[rio-playmaker]]"
entities: ["[[rio-playmaker]]"]
related: ["[[RIO E2E local — Diseño revisado]]"]
aliases: []
confidence: verified
source_session:
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/application
---

# Playmaker — Bloquear la primera lectura de undeploy

## Aprendizaje

Undeploy debe tomar el lock de fila antes de la primera lectura que decide idempotencia y asigna una correlación nueva. Bloquear sólo el delegate deja abierta la carrera si su caller ya cargó el deployment en el mismo persistence context: la query con lock puede conservar el estado managed anterior al commit concurrente.

En Playmaker las entradas directa y component API adquieren PESSIMISTIC_WRITE antes de decidir. Dos transacciones reales deben conservar un único trigger/UUID y correlación persistida; probar sólo llamadas a un mock no demuestra esa invariante. La regresión pausa el primer request antes del commit y observa el segundo, incluyendo la precarga del caller. El lock no cambia las garantías del publisher; MATERIALIZER_REST lo sostiene durante su DELETE síncrono y BigQueue publica en afterCommit.

## Aplicabilidad

- **Cuándo cargarlo:** al modificar undeploy, sus callers transaccionales o una precarga del deployment; revisar todos los primeros lookups, límites de transaction/OSIV y orden de locks.
- **Cuándo no cargarlo:** para asumir refresh universal en JPA, resolver cambios de authorization o inferir garantías de entrega del CP. El comportamiento se verificó con las versiones/configuración de este repo.

## Entidades relacionadas

[[rio-playmaker]] y [[RIO E2E local]].

## Evidencia

- [[2026-10-13-rio-e2e-local-pr-comments]] — RED original, RED con sólo lock interno, dos variantes finales PASS e inspección independiente.
- [Review PR1286](https://github.com/melisource/fury_rio-playmaker/pull/1286#discussion_r4259889686); regresión permanente `DeploymentResultConsumerIntegrationTest.whenTwoUndeployTransactionsOverlap_thenOnlyOneOperationIsCommittedAndPublished`.
