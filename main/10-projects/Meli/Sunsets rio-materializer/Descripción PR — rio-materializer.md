---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Sunsets rio-materializer]]"
  - "[[rio-materializer]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# Descripción PR — rio-materializer

Repo rio-materializer · feature/rio-sunset-update-rio-materializer @ d2d0f8b3dfa607fecc1743129e63e449cc7c7749 · base develop @ 216c0e54 · dos commits · build.gradle +7/−1 · SPEC [[Sunsets rio-materializer]].

## Propósito

Conservar el texto del PR #738 y su evidencia fuera del checkout.

## Contenido

Lote completo autorizado y validado; build Fury 202610.9.0-feat-rio-sunset-u.1 FINISHED, gate SHA aceptado y catálogo completo sin sunsets.

---

## Description

fix(deps): corrige sunsets de NoSQL, Jackson y Vert.x

NoSQL 0.2.1 tiene un bug que puede acceder al segmento Legacy cuando existen bases con el mismo nombre en segmentos distintos. Este PR actualiza NoSQL a 0.2.6 y aplica los pins Jackson core/databind 2.21.7 y Vert.x core 4.5.35 autorizados explícitamente. Todas las versiones existen en Maven Fury y Gradle confirma las cinco versiones efectivas, incluido LZ4 1.11.4 ya presente.

- Branch: `feature/rio-sunset-update-rio-materializer`; base: `develop` (`216c0e540e583e8e2d0a34f2af323ca5caf7088d`).
- Horizonte elegido: los cinco sunsets abiertos informados, hasta el 19/11/2026 en America/Santiago (20/11 00:00 UTC); ninguno estaba vencido el 22/10.
- Discovery completo: 5 dependencias y 10 issues; conteo consistente con Fury y catálogo paginado de las dos versiones desplegadas.
- Cambio: `build.gradle`, NoSQL 0.2.6 y tres pins en el `resolutionStrategy.eachDependency` existente.

### Aplicado

| Issues Fury | Dependencia | Vence (America/Santiago) | Anterior | Objetivo |
| --- | --- | --- | --- | --- |
| 892-1814014, 893-1814014 | com.fury.toolkit/java-toolkit-nosql | 02/11/2026 21:00 −03 | 0.2.1 | 0.2.6 |

### Resto del lote

| Issues Fury | Dependencia | Vence local | Objetivo | Estado y acción |
| --- | --- | --- | --- | --- |
| 6507463, 6508032, 6508087 | jackson-databind | 31/10/2026 | 2.21.7 | Pin autorizado aplicado; resolución efectiva 2.21.7. |
| 6552766 | jackson-core | 31/10/2026 | 2.21.7 | Pin autorizado aplicado; resolución efectiva 2.21.7. |
| 6619356, 6619368 | lz4-java | 06/11/2026 | 1.11.4 | develop y producción ya resuelven 1.11.4; work-queues-test/stage mantienen el artefacto 202609.18.1 con 1.10.1. Requiere redeploy. |
| 6721837, 6721950 | vertx-core | 19/11/2026 | 4.5.35 | Pin autorizado aplicado; resolución efectiva 4.5.35. |

El manifest declara `id 'org.springframework.boot' version '4.0.8'`, `id 'io.spring.dependency-management' version '1.1.6'` y `implementation platform('com.mercadolibre.library:java-melitk-bom:2.2.2')`. Conserva el idioma de override existente `eachDependency { d -> ... d.useVersion '1.11.4' }` para LZ4. No se afirma que una versión distinta de estos gestores resuelva los sunsets pendientes. Los tres pins están incluidos por autorización explícita de Rodrigo.

No hay otro PR abierto ni rama con build reciente que cubra NoSQL, Jackson o Vert.x. El PR #737 actualiza kubernetes-client a 8.0.0, pero su dependencia transitiva efectiva no fue validada como solución de Vert.x; no se cuenta como cobertura probada.

## Dev checklist (should be completed by the developer assigned to the issue)

- [ ] Definition of done: validación runtime pendiente.
- [x] Conventional commits.
- [x] Cambio limitado al manifest y revisado contra develop.
- [x] Registry y versión efectiva verificados.
- [x] Build y tests locales pasan.
- [ ] Deploy de prueba: test y api-test seleccionados; pendientes gate de scopes y confirmación inmediata.

## Code Review checklist (must be completed by the code reviewer)

- [ ] Revisión humana del cambio y riesgos.
- [ ] Confirmación de aceptación del lote.

## How Has This Been Tested?

- Java 21 y wrapper Gradle 9.4.0 del repositorio.
- `./gradlew dependencies --configuration runtimeClasspath --console=plain`: NoSQL 0.2.6, LZ4 1.11.4, Jackson core/databind 2.21.7 y Vert.x core 4.5.35 efectivos.
- `./gradlew build jacocoTestReport --console=plain`: BUILD SUCCESSFUL; 250 suites, 1.825 tests, 0 fallas, 0 errores, 0 omitidos.
- `git diff --check`: sin errores. Compilador y Gradle emiten advertencias de APIs deprecadas; no se presenta la ejecución como libre de warnings.
- Build Fury `202610.9.0-feat-rio-sunset-u.1` FINISHED, gate SHA aceptado; catálogo completo de 349 dependencias, cero sunsets. Deploy pendiente. Este PR no solicita deploy productivo.

## Issue

[Catálogo Fury](https://web.furycloud.io/engineering/applications/rio-materializer/dependency-catalog-summary) · [Artefacto de producción](https://web.furycloud.io/engineering/applications/rio-materializer/artifact-details/version/202610.8.0/detail).

---

## Notas internas — NO van al PR

- Pins aprobados explícitamente por Rodrigo. Tests: 250 suites y 1.825 casos pasan.
