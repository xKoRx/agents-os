---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Sunsets backends RIO]]"
  - "[[rio-materializer]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# Rio sunset update — rio-materializer

**Desenlace: STOPPED** — PR con NoSQL y pins aprobados; LZ4 ya estaba corregido en código.

## Propósito

Registro de la corrida del 2026-10-22T13:31:42-03:00; horizonte autorizado: todos los sunsets abiertos, incluidos vencidos. America/Santiago.

## Contenido

### Sunsets mapeados

| Dependencia | Issues | Fecha local | Afectada | Objetivo Fury | Efectiva en código |
| --- | --- | --- | --- | --- | --- |
| com.fasterxml.jackson.core/jackson-databind | 6507463,6508032,6508087 | 2026-10-31 | 2.21.5 | 2.21.7 | 2.21.7 |
| com.fasterxml.jackson.core/jackson-core | 6552766 | 2026-10-31 | 2.21.5 | 2.21.7 | 2.21.7 |
| com.fury.toolkit/java-toolkit-nosql | 892-1814014,893-1814014 | 2026-11-02 | 0.2.1 | 0.2.6 | 0.2.6 |
| at.yawk.lz4/lz4-java | 6619356,6619368 | 2026-11-06 | 1.10.1 | 1.11.4 | 1.11.4 |
| io.vertx/vertx-core | 6721837,6721950 | 2026-11-19 | 4.5.24 | 4.5.35 | 4.5.35 |

### Scopes afectados

NoSQL/Jackson/Vert.x: production, work-queues-production, work-queues-test y work-queues-stage. LZ4 antiguo: work-queues-test y work-queues-stage.

### Cambio, PR y validación

- Ruta: PR con NoSQL y pins aprobados; LZ4 ya estaba corregido en código.
- PR: https://github.com/melisource/fury_rio-materializer/pull/738
- SHA completo: `d2d0f8b3dfa607fecc1743129e63e449cc7c7749`.
- Validación nativa: 250 suites, 1.825 tests, cero fallas/errores/skips; build y jacocoTestReport pasan.
- Build: `202610.9.0-feat-rio-sunset-u.1` — FINISHED; gate SHA aceptado; catálogo completo 349 dependencias, cero sunsets.

### Deploy a test

Rodrigo autorizó activar y luego desplegar secuencialmente test y api-test. Ambos scopes se activaron sobre la versión anterior; gates aceptados con respuesta original completa. Se inició únicamente test con 202610.9.0-feat-rio-sunset-u.1, SHA d2d0f8b3dfa607fecc1743129e63e449cc7c7749.

- Pipeline: [533333](https://web.furycloud.io/engineering/applications/rio-materializer/deployment-pipelines/hands-off/executions/533333), estado alerted, completion 33.
- Deployment: [38929535](https://web.furycloud.io/rio-materializer/deployments/38929535), llegó a effective. Señales observadas: application_up=1, containers_started=1, failed_instances=0, swappedIn=100.
- Finish ejecutado y confirmado; último estado del deployment finishing/active=true. No se atribuye éxito terminal.
- Paso alertado: deploy, id 1977521, target 4170279 FAILED; last_attempt.deployment_id=38929535. La respuesta no expone una razón adicional.
- Wait de 1 minuto completed; finish del pipeline pending. api-test no se ejecutó.
- Se detuvo la secuencia para atención humana; sin retry, ignore, aborto, rollback ni Instant termination.

### Notas y bloqueos

- Los checkouts locales con cambios ajenos se preservaron. No se creó release productiva, promoción ni merge.
- No se publicaron comentarios de GitHub ni mensajes a terceros.
- Reporte local; no se subió copia a Drive durante esta fase.

## Fuentes

- [Catálogo agregado](https://web.furycloud.io/engineering/applications/rio-materializer/dependency-catalog-summary); conteos contrastados, segmentos y versiones desplegadas inspeccionados hasta completar páginas.
- Objetivos obtenidos de `issues[].upgrade_to`; los valores internos sin purl se conservaron como campo estructurado, nunca se extrajeron de `suggested`.
- Repo `melisource/fury_rio-materializer` y evidencia Gradle del SHA indicado.
