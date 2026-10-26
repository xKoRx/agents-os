---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Sunsets backends RIO]]"
  - "[[rio-playmaker]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# Rio sunset update — rio-playmaker

**Desenlace: STOPPED** — Solo redeploy; todos los objetivos ya satisfechos por la resolución de develop. El manifest no cambió entre 3cb4a0497 (inspección nativa) y 4011c077 (head actualizado del build).

## Propósito

Registro de la corrida del 2026-10-22T13:31:42-03:00; horizonte autorizado: todos los sunsets abiertos, incluidos vencidos. America/Santiago.

## Contenido

### Sunsets mapeados

| Dependencia | Issues | Fecha local | Afectada | Objetivo Fury | Efectiva en código |
| --- | --- | --- | --- | --- | --- |
| org.springframework/spring-webmvc | 5972001 | 2026-09-17 | 6.2.17 | 7.0.9 | 7.0.9 |
| io.netty/netty-handler | 6260485 | 2026-10-02 | 4.1.132.Final | 4.1.137.Final | 4.2.17.Final |
| org.springframework.security/spring-security-crypto | 6219688 | 2026-10-03 | 6.5.9 | 7.0.7 | 7.1.1 |
| org.springframework.security/spring-security-core | 6219672 | 2026-10-03 | 6.5.9 | 7.0.7 | 7.1.1 |
| com.mercadolibre.library/java-melitk-config | 627-945726 | 2026-10-27 | 0.5.0 | 2.0.0 | 2.0.0 |
| com.fasterxml.jackson.core/jackson-databind | 6507460,6508084,6508029 | 2026-10-31 | 2.21.2 | 2.21.7 | 2.21.7 |
| org.eclipse.jetty.websocket/jetty-websocket-core-common | 6453190 | 2026-10-31 | 12.0.33 | 12.0.38 | 12.1.12 |
| com.fasterxml.jackson.core/jackson-core | 6552763 | 2026-10-31 | 2.21.2 | 2.21.7 | 2.21.7 |
| com.mercadolibre.resilience/rate-limiter | 718-1488395 | 2026-12-10 | 3.1.5 | 4.0.1 | 4.0.1 |
| com.mercadolibre.restclient/meli-restclient-context | 727-1488403 | 2026-12-10 | 3.1.2 | 4.0.0 | 4.0.0 |
| com.mercadolibre.restclient/meli-restclient-core | 727-1488404 | 2026-12-10 | 3.1.2 | 4.0.0 | 4.0.0 |
| com.mercadolibre/routing | 721-1488410 | 2026-12-10 | 3.1.3 | 4.0.2 | 4.0.2 |
| com.mercadolibre.restclient/meli-restclient-default | 727-1488415 | 2026-12-10 | 3.1.2 | 4.0.0 | 4.0.0 |
| com.mercadolibre/threading | 720-1488417 | 2026-12-10 | 1.2.2 | 3.0.0 | 3.0.0 |
| com.mercadolibre.library/java-melitk-secrets | 734-1537983 | 2026-12-10 | 1.3.5 | 2.0.0 | 2.0.0 |

### Scopes afectados

Solo test4-nonprod conserva las 15 dependencias afectadas.

### Cambio, PR y validación

- Ruta: Solo redeploy; todos los objetivos ya satisfechos por la resolución de develop. El manifest no cambió entre 3cb4a0497 (inspección nativa) y 4011c077 (head actualizado del build).
- PR: No corresponde: no se modificó código.
- SHA completo: `4011c077bdf86965361fc7fbbb94896eb5223c96`.
- Validación nativa: runtimeClasspath de Gradle confirma las versiones efectivas; no se modificó código..
- Build: `202608.13.1-develop.3` — FINISHED; gate SHA aceptado; catálogo completo 303 dependencias, cero sunsets.

### Deploy a test

No ejecutado. Falta scope exacto indicado por una persona y confirmación inmediata, después del gate de build. No hubo pipeline, deployment ni Finish en esta corrida.

### Notas y bloqueos

- Los checkouts locales con cambios ajenos se preservaron. No se creó release productiva, promoción ni merge.
- No se publicaron comentarios de GitHub ni mensajes a terceros.
- Reporte local; no se subió copia a Drive durante esta fase.

## Fuentes

- [Catálogo agregado](https://web.furycloud.io/engineering/applications/rio-playmaker/dependency-catalog-summary); conteos contrastados, segmentos y versiones desplegadas inspeccionados hasta completar páginas.
- Objetivos obtenidos de `issues[].upgrade_to`; los valores internos sin purl se conservaron como campo estructurado, nunca se extrajeron de `suggested`.
- Repo `melisource/fury_rio-playmaker` y evidencia Gradle del SHA indicado.
