---
type: learning
schema_version: 1
scope: application
created: "2026-10-09"
updated: "2026-10-09"
area: "[[Meli]]"
project: "[[RIO E2E local]]"
application: "[[rio-controlplane-kafka]]"
entities: ["[[rio-playmaker]]", "[[rio-controlplane-kafka]]", "[[rio-controlplane-clickhouse]]", "[[rio-controlplane-flink]]"]
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
  - project/rio-e2e-local
---

# Kafka local — Reintentos y ACK se verifican en el container

## Aprendizaje

Un listener pequeño con Spring Kafka conserva el contrato sólo si se prueba el container configurado. Con RECORD y auto commit apagado, la fuente se confirma tras aceptación productiva o publicación DLT confirmada. Una DLT fallida/pendiente retiene el offset; ACK de entrada no acredita completion de trabajo async. Un presupuesto de dos retries necesita impedir el reset por cambio de tipo de excepción; poison no reintenta y FAILED de negocio es resultado normal.

La configuración aislada no demuestra retry/seek/rebalance/shutdown: verificar esos caminos con el framework real y clientes de frontera controlados. Readiness debe detectar container detenido y falta de assignment. El shutdown debe superar el wait de ACK y drenar trabajo propio antes del teardown.

## Aplicabilidad

- **Cuándo cargarlo:** al incorporar un CP RIO al transporte local Kafka o modificar su factory, error handler, recoverer o lifecycle.
- **Cuándo no cargarlo:** para inferir semántica de provisioning, exactamente una vez o capacidades que el CP no ofrece. Adaptar API/versiones al classpath efectivo; el pin F1 no es una receta universal.

## Entidades relacionadas

[[rio-playmaker]], [[rio-controlplane-kafka]], [[rio-controlplane-clickhouse]] y [[rio-controlplane-flink]].

## Evidencia

- [[2026-10-09-rio-e2e-local-f1-implementation]] — simplificación challengeada, framework tests, cobertura y reproducción física independiente.
- CP Kafka: `src/localTest/` y `meli/features/20261009-rio-e2e-local/4-implementation/VERIFICATION.md`; PM: transporte local compartido y su suite permanente. PR fuente: https://github.com/melisource/fury_rio-controlplane-kafka/pull/86.
