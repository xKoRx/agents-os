---
type: change_log
schema_version: 1
scope: session
created: "2026-10-09"
updated: "2026-10-09"
area: "[[Meli]]"
project: "[[RIO E2E local]]"
application:
entities: ["[[RIO E2E local]]", "[[RIO E2E local — Diseño revisado]]"]
related: ["[[Kafka — Ambiente local con servicios reales]]", "[[2026-10-08-rio-e2e-local-created]]"]
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

# 2026-10-09-rio-e2e-local-design-challenge

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - [[RIO E2E local — Diseño revisado]] (created, template `doc`).
  - [[RIO E2E local]] (updated: estado actual, fila del front, SPEC técnica como estado objetivo, tareas, bitácora, decisiones y links).

## Motivo

- El owner pidió challenge crítico del diseño E2E local de cinco apps con transporte Kafka embebido, sin bridge, antes de escribir código, permitiendo actualizar sólo documentos del proyecto por delta.

## Fuentes usadas

- Lectura por ref git de PM `origin/develop` 44c2905, CP Kafka `origin/develop` 6a91937, CH c8b20b6, Flink 7c645ea, ads-signals-frontend a3f82ab y rio-frontend 6d644ec, más worktrees históricos HTTP/E2E; `ls-remote` de `develop` el 09/10.
- `javap` sobre `rio-sdk-events` 1.3.1, 1.5.0 y 1.6.1 en el cache Gradle local.
- `local/KAFKA_HTTP.md` de la rama HTTP de Playmaker y evidencias de [[Kafka — Ambiente local con servicios reales]].

## Resolución aplicada

- Consenso confirmado por la IA revisora el09/10 tras leer el diseño actualizado: las nueve correcciones y las precisiones D5 (ramas apiladas, sin merge previo) y D6 (versión productiva preferida; alternativa probada con límite declarado) son compatibles. Resumen del proyecto alineado con A condicionada a paridad y Flink físico obligatorio en el cierre. Acuerdo de diseño con gates; no acredita ejecución ni autoriza merges/infraestructura. Repos sin modificaciones en esta revisión.
- Veredicto: viable para PM, CP Kafka y CP ClickHouse; Flink físico BLOCKED; front BLOCKED por datos de referencia y actions. Front elegido ads-signals-frontend.
- Diseño objetivo con seam de entrada A (listener local invoca el handler del controller), groups por CP, ACK tras 2xx, DLT por CP, `BigQueueClient` Kafka bajo publishers productivos y seis decisiones D1–D6 para el owner.
- La SPEC técnica propuesta del proyecto se reemplazó por el estado objetivo (sin historial de edición).
- Revisión cruzada con otra IA aceptada: la certificación final conserva Flink físico y journeys browser con las actions necesarias; A exige pruebas de paridad HTTP↔Kafka y B queda donde A no conserve la capa MVC; el timeout de PM es detección, no recuperación; una partición y `earliest` no eliminan carreras, por lo que la readiness es explícita y el orden de ejecución async se trata aparte; extracción selectiva desde LOCAL-HTTP-2 en ramas apiladas; versión ClickHouse fijada por pruebas físicas, preferentemente la productiva.

## Validación

- Repos originales sin alteraciones tras el discovery: conteos de `git status --porcelain` iguales a los del 08/10 (PM 2, CP Kafka 12, CH 10, Flink 1, ads 5, rio-frontend 1).
- Hallazgos críticos verificados directamente además del discovery delegado: tópico de resultado CP Kafka vs Playmaker, guard loopback de PM, campo `context` por versión de SDK, firmas de controllers y perfiles de publishers en CH/Flink.
- Sin código, ramas, fetch, Docker, VM ni recursos Fury.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos; contiene nombres de repos corporativos y SHAs, no exportar automáticamente.

## Rollback

- Eliminar [[RIO E2E local — Diseño revisado]] y este log, y restaurar las secciones afectadas de [[RIO E2E local]] desde el historial de versiones del vault.
