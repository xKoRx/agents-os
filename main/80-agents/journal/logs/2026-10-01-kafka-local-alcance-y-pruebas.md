---
type: change_log
schema_version: 1
scope: session
created: "2026-10-01"
updated: "2026-10-01"
area: "[[Meli]]"
project: "[[Kafka — Ambiente local con servicios reales]]"
application: "[[rio-controlplane-kafka]]"
entities: ["[[Kafka — Ambiente local con servicios reales]]"]
related: ["[[Kafka local — Historia y prueba de arranque (2026-10-01)]]"]
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Kafka local — Alcance completo y pruebas automáticas

## Cambio

- **Tipo:** updated + created.
- **Archivo(s):**
  - `10-projects/Meli/Kafka — Ambiente local con servicios reales/Kafka — Ambiente local con servicios reales.md`.
  - Esta nota de cambio, materializada desde el template contratado v1.

## Motivo

- El owner pide que el CP funcione completo localmente, incluido KVS, y que exista un mecanismo de pruebas automáticas. Confirma explícitamente KVS real de Fury Sandbox frente a la alternativa autocontenida sin VPN.

## Fuentes usadas

- Solicitud del owner y respuesta explícita sobre KVS.
- `KvsConfig` e `IdempotencyGuard` en `develop@c9355395ef4b2bf438f0eb44528e24fa76ca498c`: cliente Toolkit, create, read-back de versión, CAS/update y TTL.
- `build.gradle` e integración existente: JUnit, Testcontainers y Awaitility declarados; tests actuales con Mockito no demuestran esos flujos reales.
- [[Kafka local — Historia y prueba de arranque (2026-10-01)]].
- Documentación primaria de [Testcontainers Kafka](https://java.testcontainers.org/modules/kafka/) y [Gradle Testing](https://docs.gradle.org/current/userguide/java_testing.html).

## Resolución aplicada

- KVS pasó de propuesta por confirmar a backend elegido: Fury Sandbox real con contenedor propio y conectividad corporativa aceptada. La configuración concreta del cliente sigue por demostrar.
- Se actualizaron objetivo, estado, tareas, decisiones y criterios de aceptación del proyecto, conservando su identidad y la tabla de entrega.
- Se agregó una estrategia concreta de suites Gradle reales, aislamiento por corrida, comprobación de efectos/resultados, reportes y ejecución en un runner con Docker y acceso al sandbox.
- Se registraron las primeras comprobaciones técnicas: protocolo KVS del cliente actual y capacidad del runner. Las tasks/launchers nuevos están identificados como futuros; no se presentaron como implementados.
- El cambio es estado actual del proyecto basado en una decisión del owner. No se modificaron repositorios ni se publicaron SPEC o pipelines durante esta iteración.

## Validación

- Lint estricto dirigido sobre el proyecto y esta nota: ERROR=0 y WARN=0. Se comprobó que las suites/launchers están señalados como futuros. No se ejecutaron pruebas nuevas de producto en esta iteración de diseño.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin credenciales, valores privados de sandbox ni paths absolutos de máquina.

## Ampliación — BigQueue sandbox

- **Motivo:** el owner pregunta si existe Fury BigQueue Sandbox.
- **Fuentes:** `fury_sandbox-services-docs@961c80339f0b12cd0a88610f5af9edf79d58385f`, capítulo `docs/guide/sandbox_service.md`; `fury_cli-services-docs@2ae4d44d8750497cb36e1fa6f85aff62b03fa583`, capítulo `docs/guide/services/bigq.md`; ayuda instalada de `fury services bigq mock` y `send-msg`.
- **Hallazgo:** Sandbox Services lista BigQueue a través de comandos mock para entregar mensajes a endpoints locales. No demuestra una cola sandbox provisionada equivalente a KVS. La CLI además documenta reenvío desde un consumer real de test, cuyo paso init lo pausa.
- **Aplicación:** se agregó la distinción y la alternativa por evaluar al proyecto. No se ejecutaron envíos ni se modificaron topics, consumers o servicios. Se conservaron las decisiones de KVS y el alcance de la integración.
- **Validación:** lectura directa de documentación oficial en GitHub y ayuda del CLI; no se probó runtime BigQueue.

## Rollback

- Revertir únicamente los cambios de alcance/automatización de esta iteración en el proyecto y registrar la reversión. Conservar la investigación y las pruebas previas.
