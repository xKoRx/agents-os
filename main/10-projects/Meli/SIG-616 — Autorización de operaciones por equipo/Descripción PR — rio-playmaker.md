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

**Identidad:** `rio-playmaker` · `feature/operation-authorization-by-team-f1` @ `7fbb7efcf78e85529c46eee65e8d0a28ec9cf6f3` · base `develop` @ `e02b2b09fbd553161d0f4937040fdce9294cafd4` · 3 commits (feature + merge + corrección de contrato) · 15 archivos, +572/−320 · SPECs [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) y [SIG-622](https://spellbook.adminml.com/projects/SIG/specs/SIG-622) · sin dependencia downstream · suite local completa del 2026-09-15: 3.785 tests, 0 fallas, 0 errores y 2 skips preexistentes; 100% de cobertura de líneas nuevas y 31/32 branches nuevas (96,875%).

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
* Se migraron `PipelineComponentDeleteServiceImpl` y `ComponentInactivationServiceImpl` a `DEPLOYER_AND_UP`, preservando la precondición existente de `systemId` y autorizando antes del lookup de componentes, locks, creación de ejecuciones o publicación.
* Se retiraron los helpers de autorización de delete/inactivate que ya no tenían uso, manteniendo sin cambios los helpers no relacionados de write/team-admin.
* Se agregaron tests focalizados de autorización y consumidores para matriz de roles, match exacto de grants, scope nulo/vacío, fallas ACME, precondiciones de compatibilidad y orden de autorización.
* Se agregaron logs de denegación de baja cardinalidad con `access_level`; las fallas de ACME sólo registran el tipo de excepción y no exponen grants ni credenciales Tiger.
* Se preservó el contrato previo de `no owning team` para ownership incompleto y se recuperó la causa encadenada ante una excepción de ACME.

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
    * [ ] Se recomienda integration testing — el smoke ACME/Data Product está pendiente por falta de credenciales no productivas.
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

* Suite focalizada de autorización/consumidores: 60 tests pasaron tras la corrección de contrato.
* `./gradlew test jacocoTestReport`: 3.785 tests pasaron, 0 fallas, 0 errores y 2 skips preexistentes; 100% de cobertura de líneas nuevas y 31/32 branches nuevas (96,875%).
* `./gradlew check`: pasó.
* `git diff --check origin/develop...HEAD`: pasó.
* El smoke no productivo de ACME/Data Product sigue pendiente por falta de credenciales apropiadas.

## Issue

* [SIG-621 — Autorización de operaciones por equipo](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)
* [SIG-622 — Slice 1: autorizador común de operaciones](https://spellbook.adminml.com/projects/SIG/specs/SIG-622)

---

## Notas internas — NO van al PR

- El head remoto de la rama es `7fbb7efcf78e85529c46eee65e8d0a28ec9cf6f3`; contiene un merge limpio de `origin/develop@e02b2b09fbd553161d0f4937040fdce9294cafd4` y una corrección de contrato posterior.
- La única brecha de evidencia relevante para merge es el smoke no productivo. No presentar el PR como completamente Definition-of-Done hasta contar con esa evidencia.
