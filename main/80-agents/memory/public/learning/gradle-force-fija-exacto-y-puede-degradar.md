---
type: learning
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
  - "[[resolver-versiones-java-sin-construir-via-fury-nexus]]"
  - "[[2026-09-03-sigfoun-websec-vuln-intake-rio-foundation]]"
aliases:
  - forzar versiones en Gradle
  - resolutionStrategy force
  - pin de seguridad que degrada
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/global
  - tech/gradle
  - topic/security
---

# gradle-force-fija-exacto-y-puede-degradar

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- `resolutionStrategy.force` y `eachDependency { useVersion }` en Gradle fijan la versión **exacta**, no un piso. Un pin escrito como remedio de seguridad —con el comentario "forzar X o superior"— deja de proteger y pasa a **degradar** en cuanto el BOM del proyecto empieza a traer algo mayor que X.
- Por eso todo pin de seguridad es deuda con fecha de vencimiento: sobrevive al bump de BOM que lo volvió innecesario y nadie lo nota, porque el build sigue verde. Al subir la versión de un BOM o de un plugin que administra dependencias, **revisar y borrar los forces que ese bump vuelve obsoletos** es parte del mismo cambio.
- Un force parcial es peor que ninguno: si se fija una lista de módulos de una familia y quedan otros afuera, el classpath termina partido entre dos líneas de la misma librería, con riesgo de incompatibilidad binaria además del de seguridad.

## Aplicabilidad

- **Cuándo cargarlo:** al revisar, escribir o auditar bloques `resolutionStrategy` en repos Gradle; al subir la versión de un BOM o del plugin de Spring Boot; al triagear vulnerabilidades de dependencias donde el repo ya declara un pin.
- **Cuándo no cargarlo:** proyectos sin gestión de dependencias por BOM, o stacks que no son Gradle.

## Entidades relacionadas

- [[RIO]] · [[Vulnerabilidades WebSec — RIO Foundation]]

## Evidencia

%% Cita de fuente, NO prosa narrativa: link a sesión/log/archivo + una línea de qué la respalda. No re-parafrasear el aprendizaje ya destilado arriba (constitución: memorias compactas). %%

- Fuente: [[2026-09-03-sigfoun-websec-vuln-intake-rio-foundation]] — `rio-controlplane-observability` fuerza siete módulos de netty a `4.1.122.Final` bajo Boot 4.1.1, que gestiona `4.2.17.Final`; `netty-resolver-dns` quedó fuera de la lista y se mantuvo en 4.2.17.
