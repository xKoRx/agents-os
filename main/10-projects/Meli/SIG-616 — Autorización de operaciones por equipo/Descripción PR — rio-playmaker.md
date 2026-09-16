---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
  - "[[rio-playmaker]]"
aliases:
  - PR description SIG-622
tags:
  - kind/doc
  - project/sig-616-operation-authorization
created: "2026-09-15"
updated: "2026-09-15"
---

# Descripción PR — rio-playmaker

**Identidad:** `rio-playmaker` · `feature/operation-authorization-by-team-f1` @ `7cac000896befd8215b047681ad4851be51406c4` · base `develop` @ `a78db6edee803083d73b38937adda099bb75d2cc` · 7 commits · 15 archivos, +664/−321 · SPECs [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) y [SIG-622](https://spellbook.adminml.com/projects/SIG/specs/SIG-622) · sin dependencia downstream · suite local completa del 2026-09-15: 3.829 tests, 0 fallas y 2 skips preexistentes; autorizador, niveles y helper de ownership con 100% de líneas y branches cubiertos localmente.

> [!warning] **Smoke no productivo pendiente**
> El smoke de ACME/Data Product no se ejecutó por falta de credenciales apropiadas para el ambiente no productivo. No afecta la suite automatizada, pero debe completarse antes de afirmar confianza de merge o release.

## Propósito

Materializar en el vault el cuerpo del PR de Slice 1 de SIG-616, basado en evidencia y siguiendo el template del repositorio destino.

## Contenido

El PR extrae la política ACME existente a un servicio reutilizable de autorización por operación y migra exclusivamente delete e inactivate, sin cambiar su nivel requerido `DEPLOYER_AND_UP`, la precondición local de compatibilidad `systemId`, el status de falla ni el orden de autorización previo a side effects.

---

## Descripción

feat(auth): centralize operation authorization

Este es el Slice 1 de la iniciativa de autorización de operaciones. Es un refactor de compatibilidad autocontenido para los flujos existentes de delete e inactivate: centraliza su autorización ACME de owner-project sin extender la protección a Actions, deployments, relaciones, pipelines u otras mutaciones. El Slice 2 (Actions de Signals) queda deliberadamente fuera de alcance.

Cambios:
* Se agregaron `OperationAuthorizationService` y el enum finito `OperationAccessLevel` para validar caller y scope de ownership no vacíos, consultar una vez los grants owner-project, exigir un grant exacto de team/project y aplicar los roles permitidos sin distinguir mayúsculas.
* Se migraron `PipelineComponentDeleteServiceImpl` y `ComponentInactivationServiceImpl` a `DEPLOYER_AND_UP`, preservando y centralizando su precondición legacy de ownership fuera del autorizador transversal, y autorizando antes del lookup de componentes, locks, creación de ejecuciones o publicación.
* Se retiraron los helpers de autorización de delete/inactivate que ya no tenían uso, manteniendo sin cambios los helpers no relacionados de write/team-admin.
* Se agregaron tests focalizados de autorización y consumidores para matriz de roles, match exacto de grants, scope nulo/vacío, fallas ACME, precondiciones de compatibilidad y orden de autorización.
* Se agregaron logs de denegación con `access_level`, team y project persistidos; no se registran username, grants ni credenciales Tiger, y las fallas ACME sólo agregan el tipo de excepción.
* Se preservó el contrato de `no owning team`; ante una excepción de ACME, el autorizador falla cerrado con el mensaje genérico y no conserva la excepción interna como `cause`.

## Checklist de desarrollo (debe completarlo quien desarrolla el issue)

* [ ] Cumplí la definición de terminado — falta el smoke no productivo de ACME/Data Product.
* [x] Usé [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [x] Mi código sigue las guías de estilo de este proyecto
    * [Java Fury Guideline](https://furydocs.io/code-quality/latest/guide/#/languages/java)
    * [Deep Source Java Guideline](https://deepsource.com/blog/java-code-review-guidelines#10-override-hashcode-when-overriding-equals)
* [x] Hice una auto-revisión del código
* [x] Comenté las partes necesarias, especialmente las de comprensión menos directa
* [x] Actualicé la documentación correspondiente (`README.md`, `DEV.md`, `CHANGELOG.md`) — este refactor interno de compatibilidad no requiere cambios de documentación de usuario u operación.
* [x] La aplicación sigue siendo compilable después de los cambios
* [x] Los cambios no generan warnings nuevos de linters o calidad de código
* [x] Agregué tests que prueban que el cambio funciona
    * [x] Se agregaron unit tests
    * [x] Se agregó un integration test del contrato HTTP `403`; el smoke ACME/Data Product sigue pendiente por falta de credenciales no productivas.
* [x] Los unit tests nuevos y existentes pasan localmente
* [x] Los cambios dependientes fueron mergeados y publicados — no se requiere dependencia downstream.
* [x] Actualicé la rama con cambios previos de develop/master
* [ ] Desplegué la rama en preproducción — no se desplegó; falta el smoke requerido.

## Checklist de code review (debe completarlo quien revisa)

* [ ] ¿Corresponde al issue que se está completando?
  * ¿Se cumplen los criterios de aceptación?
  * ¿Está listo según la Definition Of Done del proyecto?

* [ ] ¿El código tiene buen estilo? (legible y alineado con las buenas prácticas y guías)
  * ¿Se usan linters?
  * ¿Está claro qué hace cada clase, método o función?
  * ¿Los nombres reflejan lo que hace el código?
  * ¿Las funciones son simples y claras?

* [ ] ¿El código funciona correctamente? (opcional)
  * ¿Se probó localmente?
  * ¿Las excepciones se manejan correctamente?
  * ¿Se cubren los casos borde?
  * Revisar gotchas de Java.
  * Casos borde de ifs, fors, whiles y fechas.
  * ¿Hay while loops innecesarios?

* [ ] ¿La implementación es suficientemente buena?
  * ¿Cada línea de código tiene uso?
  * ¿Hay [side effects](https://medium.com/@ryk.kiel/dont-let-your-code-get-out-of-control-avoiding-side-effects-in-python-d68faf26912) inesperados?
  * Revisar uso de librerías de terceros (madurez, copyright, etc.).
  * ¿La solución tiene un rendimiento razonable sin optimización prematura?
  * ¿Podría ser más simple?
  * Buscar vulnerabilidades ([OWASP](https://owasp.org/www-project-top-ten/) top 10).
  * ¿Está bien modularizada y sigue [S.O.L.I.D.](https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/)?
  * ¿Está correctamente testeada?
  * ¿Hay código duplicado?
  * ¿Qué falta (documentación, comentarios, métricas, logs, etc.)?
  * ¿Existe código previo que ya resuelva este problema?

## ¿Cómo se probó?

* Suite focalizada de autorización, consumidores, helper y handler HTTP: pasó tras aplicar el feedback de review.
* `./gradlew test jacocoTestReport`: 3.829 tests pasaron, 0 fallas y 2 skips preexistentes; autorizador, niveles y helper de ownership con 100% de líneas y branches cubiertos localmente.
* `./gradlew check`: pasó.
* `git diff --check origin/develop...HEAD`: pasó.
* El smoke no productivo de ACME/Data Product sigue pendiente por falta de credenciales apropiadas.

## Issue

* [SIG-621 — Autorización de operaciones por equipo](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)
* [SIG-622 — Slice 1: autorizador común de operaciones](https://spellbook.adminml.com/projects/SIG/specs/SIG-622)

---

## Notas internas — NO van al PR

- El head remoto de la rama es `7cac000896befd8215b047681ad4851be51406c4`; contiene el refactor, la sincronización con `origin/develop@a78db6edee803083d73b38937adda099bb75d2cc`, la corrección de contrato, cobertura adicional y feedback de review.
- La única brecha de evidencia relevante para merge es el smoke no productivo. No presentar el PR como completamente Definition-of-Done hasta contar con esa evidencia.
