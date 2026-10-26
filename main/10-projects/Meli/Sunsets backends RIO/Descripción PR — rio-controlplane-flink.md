---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Sunsets backends RIO]]"
  - "[[rio-controlplane-flink]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# Descripción PR — rio-controlplane-flink

Repo rio-controlplane-flink · feature/rio-sunset-update-rio-controlplane-flink @ 884c1326 · base develop @ 920a7075 · un commit · build.gradle +4 · SPEC [[Sunsets backends RIO#SPEC técnica — Flink]].

## Propósito

Conservar la descripción revisable fuera del checkout.

## Contenido

Cuerpo del PR con evidencia nativa y catálogo completo.

---

## Cambio

Actualiza Guava de la versión transitiva `33.6.0-android` a `33.7.2-jre` con el mismo `resolutionStrategy.eachDependency` que el proyecto usa para sus pins de seguridad. Fury recomienda ese objetivo para el issue `6657835`, con sunset el 11/11/2026 a las 21:00 America/Santiago (`2026-11-12T00:00:00Z`). La versión existe en Maven Fury y Gradle confirma la resolución efectiva.

Branch: `feature/rio-sunset-update-rio-controlplane-flink`. Base: `develop@920a7075bc3dd34e5aaf2a0834848b9387fdfd30`. Único archivo modificado: `build.gradle` (4 líneas añadidas). Horizonte autorizado: todos los sunsets abiertos de la aplicación.

## Cobertura del lote

| Dependencia | Issues Fury | Versión afectada | Objetivo | Resultado |
| --- | --- | --- | --- | --- |
| com.google.guava/guava | 6657835 | 33.6.0-android | 33.7.2-jre | Pin aplicado en este PR. |
| com.fasterxml.jackson.core/jackson-core | 6552766 | 2.21.5 | 2.21.7 | Ya corregido en develop; Gradle confirma 2.21.7. Los scopes antiguos requieren redeploy. |
| com.fasterxml.jackson.core/jackson-databind | 6508087, 6508032, 6507463 | 2.21.5 | 2.21.7 | Ya corregido en develop; Gradle confirma 2.21.7. Los scopes antiguos requieren redeploy. |

Discovery completo: 3 dependencias con sunset, 5 issues, 0 vencidos; conteo consistente con el resumen Fury y los catálogos paginados de todas las versiones desplegadas. No hay otro PR abierto ni rama con build reciente que cubra Guava 33.7.2-jre. Este único PR conserva el lote de la aplicación, sin duplicar los cambios de Jackson ya mergeados.

## Validación

- Java 25 y wrapper Gradle 9.3.1 del repo.
- `./gradlew dependencies --configuration runtimeClasspath --console=plain`: Guava 33.7.2-jre; Jackson core/databind 2.21.7 efectivos.
- `./gradlew build jacocoTestReport --console=plain`: BUILD SUCCESSFUL; 199 suites, 1.966 tests, 0 fallas, 0 errores y 0 omitidos.
- `pre-commit run --files build.gradle`: hooks de credenciales y PII pasan; formatter/Checkstyle/PMD omiten el archivo porque no es Java.
- `git diff --check`: pasa. Gradle conserva avisos de APIs deprecadas.
- Build Fury `202609.24.0-feat-rio-sunset.0` FINISHED, gate SHA aceptado; catálogo completo de 339 dependencias, cero sunsets. Deploy de prueba completado en `api-nonprod`, con selección y confirmación explícitas: pipeline `533792` completed/100%, deployment `38932155` finished/active=false; deploy/wait/finish completos.

## Evidencia

[Catálogo Fury](https://web.furycloud.io/engineering/applications/rio-controlplane-flink/dependency-catalog-summary). Objetivo extraído de `issues[].upgrade_to`, no del texto libre `suggested`.

---

## Notas internas — NO van al PR

- Tono auditado con [[human-first-technical-writing]]: factual, conciso y profesional. Validación runtime completada en api-nonprod.
