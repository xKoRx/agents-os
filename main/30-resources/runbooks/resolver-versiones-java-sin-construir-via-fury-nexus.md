---
type: runbook
schema_version: 1
scope: global
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Meli]]"
project:
application:
entities:
  - "[[Meli]]"
related:
  - "[[gradle-force-fija-exacto-y-puede-degradar]]"
  - "[[2026-09-03-sigfoun-websec-vuln-intake-rio-foundation]]"
aliases:
  - qué versión resuelve mi build de Gradle
  - techo publicado de una dependencia
  - versiones gestionadas por el BOM de Spring Boot
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/global
  - tech/gradle
  - tech/fury
---

# resolver-versiones-java-sin-construir-via-fury-nexus

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Saber qué versión de una dependencia resuelve un proyecto Java/Kotlin de Fury, y hasta dónde se puede subir, **sin construir el proyecto**. Evita correr Gradle en N repos, no toca archivos de trabajo y sirve para triage de vulnerabilidades y para decidir si un ticket tiene arreglo posible.

## Precondiciones

- VPN corporativa **GlobalProtect** conectada; ver [[rjara-vpn-routing-preferences]]. Sin ella, `repo1.maven.org` no responde y el Nexus de Fury tampoco.
- El repo clonado sólo se necesita para leer la versión del plugin `org.springframework.boot` y los pins propios; alcanza con `git show origin/develop:build.gradle`.

## Procedimiento

1. Leer del repo la versión del plugin de Boot y los pins propios, sin checkout: `git show origin/develop:build.gradle | grep -nE "springframework.boot|melitk-bom|useVersion|force '"`.
2. Obtener las **versiones gestionadas** por ese BOM desde el Nexus de Fury: `curl -s "https://maven.artifacts.furycloud.io/repository/all/org/springframework/boot/spring-boot-dependencies/<v>/spring-boot-dependencies-<v>.pom" | grep -oE "<(spring-framework|tomcat|micrometer|netty|spring-security|spring-retry)\.version>[^<]*"`.
3. Obtener el **techo publicado** de una dependencia: `curl -s "https://maven.artifacts.furycloud.io/repository/all/<group/con/slashes>/<artifact>/maven-metadata.xml" | grep -oE "<version>[^<]*"`. Los tags `<latest>` y `<release>` pueden apuntar a un milestone, así que filtrar la línea de versión que interesa en vez de confiar en ellos.
4. Alternativa sin red: los mismos POM suelen estar en la caché local de Gradle, en `~/.gradle/caches/modules-2/files-2.1/<group>/<artifact>/`. Sirve para versiones ya resueltas alguna vez en la máquina.

## Validación

- Contrastar una versión gestionada obtenida por este camino contra un comentario o pin explícito del propio `build.gradle`; si coinciden, la lectura del BOM es correcta.
- Si el `maven-metadata.xml` no lista ninguna versión mayor a la que ya usa el proyecto, **el ticket no tiene bump posible** y el entregable es responder el ticket, no abrir un PR.

## Rollback / recuperación

- Procedimiento de sólo lectura: no escribe en repos ni en la caché. No hay nada que revertir. Si el Nexus responde 000, revisar GlobalProtect antes de dudar de la URL.

## Evidencia

- Fuente: [[2026-09-03-sigfoun-websec-vuln-intake-rio-foundation]] — se resolvieron los BOM de Boot 3.5.6 / 3.5.7 / 3.5.12 / 3.5.16 / 4.1.1 y el techo de siete dependencias sobre nueve repos sin construir ninguno.
