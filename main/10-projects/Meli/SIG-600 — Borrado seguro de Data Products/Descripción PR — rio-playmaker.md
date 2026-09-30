---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[SIG-600 — Borrado seguro de Data Products]]"
  - "[[rio-playmaker]]"
aliases: []
tags:
  - kind/doc
  - project/sig-600
created: "2026-09-30"
updated: "2026-09-30"
---

# Descripción PR — rio-playmaker

Repo `melisource/fury_rio-playmaker` · branch `feature/sig-600-delete-auth@37dc1f2d3` · base `develop@0c9e9e3ee` · 2 commits sobre la base · 17 archivos, +458/−29 · SPECs [SIG-600](https://spellbook.adminml.com/projects/SIG/specs/SIG-600) y [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643) · suite 2026-09-30: 4.093 tests, 0 fallas, 0 errores, 2 skips; 11 selectores focalizados exitosos.

> [!warning] Brecha de validación LOCAL_STACK
> **La cadena histórica de migraciones de develop falla en MySQL** al intentar borrar component_type mientras chk_deployment_freeze_reach todavía lo referencia. Recursos del run local eliminados y teardown verificado. El runner no llegó al check posterior de deployment-loopback.

> [!info] Dependencias para desplegar con providers reales
> Habilitar tráfico Fury a Kraken y validar application/permission en el scope objetivo. BFF/UI siguen pendientes para el acceso Kraken-only a través del front. Las tres versiones mock de test3 ejercitan la regla OR y el blocker existente con respuestas sintéticas.

## Propósito

Conservar en el proyecto el texto publicable del PR #1228 y su evidencia, aplicando el template del repo y la skill human-first-technical-writing.

## Contenido

Descripción del alcance, regla de autorización, evidencia del HEAD actualizado y tabla con las tres versiones mock y capturas aportadas por el usuario. Los checkboxes del reviewer se preservan pendientes.

---

## Descripción

El `DELETE` de Playmaker permite borrar un Data Product si el usuario autenticado por Tiger tiene **`delete-data-products` en Kraken O membresía ACME en el equipo dueño**. Antes solo se consultaba ACME; ahora basta la membresía, sin exigir un rol privilegiado de proyecto.

La autorización se evalúa antes de los bloqueos existentes: **403** sin permisos; **409** con permisos y recursos activos. Se conserva **401** sin autenticación y se devuelve **503** si falla una consulta y ninguna fuente permite autorizar. Este PR cubre la autorización en Playmaker; las validaciones de recursos activos ya existían.

**Pendiente de revisión:** [carrera por cambio de equipo durante la autorización](https://github.com/melisource/fury_rio-playmaker/pull/1228#discussion_r4144981821). El comentario es válido y requiere corrección antes del merge.

Para Kraken real se debe habilitar el tráfico Fury y configurar la aplicación/permiso del scope. El BFF conserva su guard ACME, por lo que las pruebas aisladas usan el endpoint de Playmaker.

## Checklist del desarrollador

<details>
<summary>Ver checklist</summary>

- [ ] Definición de terminado cumplida: pendiente corregir la carrera de ownership.
- [x] Commits convencionales.
- [x] Código conforme a las guías del proyecto.
- [x] Autorrevisión realizada.
- [x] Comentarios en las partes relevantes.
- [x] Documentación canónica actualizada (`testing-scenarios.md`).
- [x] La aplicación compila.
- [ ] Sin nuevas advertencias: checks de calidad verdes; persisten advertencias de Gradle/JDK.
- [x] Tests unitarios e integración agregados.
- [x] Tests nuevos y existentes pasan localmente.
- [ ] Dependencias downstream listas: ajuste frontend/BFF pendiente para Kraken-only.
- [x] Rama sincronizada con `develop`.
- [ ] HEAD actual desplegado en preproducción: las capturas corresponden a las versiones mock.

</details>

## Checklist de revisión de código

<details>
<summary>Para completar por el reviewer</summary>

- [ ] Se cumplen los criterios de aceptación y la definición de terminado.
- [ ] El código es claro y cumple las guías de estilo.
- [ ] El comportamiento, las excepciones y los casos borde son correctos.
- [ ] La implementación es suficiente, segura, simple y está probada.

</details>

## Pruebas

**HEAD `37dc1f2d3` · base `develop@0c9e9e3ee` · 30/09/2026.**

- `./gradlew test jacocoTestReport`: **4.093 tests, 0 fallas, 0 errores y 2 skips preexistentes** (L0).
- `./scripts/run-agentic-testing-contract.sh`: **11 selectores focalizados aprobados** (UNIT/H2_INTEGRATION/CONTRACT). LOCAL_STACK falló antes de iniciar la app: la migración `20260922153217845_drop_deployment_freeze_component_type.sql` intenta borrar una columna usada por un constraint. Limpieza local verificada; el check posterior de deployment-loopback no se ejecutó.
- `./scripts/validate-repository-contract.sh --staged`, `./scripts/validate-testing-contract.sh --staged` y `git diff --check`: aprobados.
- GitHub: **workflow, CI, cobertura, dependencias y análisis estático verdes**. Code Reviewer solicita aprobación humana.

### Tres versiones para probar en `test3`

Se crearon tres versiones con respuestas mock de ACME/Kraken, conservando Tiger y los bloqueos reales. Los builds terminaron con tests habilitados. Las capturas muestran la validación manual de UI; el HTTP indicado es el esperado para un DP con despliegue activo.

| Caso | Versión para desplegar | Resultado esperado / captura |
|---|---|---|
| Sin ACME ni Kraken | [0.0.5-test-sig600-denied](https://web.furycloud.io/engineering/applications/rio-playmaker/versions/detail/0.0.5-test-sig600-denied) | **403**, sin permiso.<br><img width="360" alt="Sin permiso para eliminar el Data Product" src="https://github.com/user-attachments/assets/299578f7-a99d-425c-9e4d-9c7120ea14f7" /> |
| Solo ACME | [0.0.3-test-sig600-acme](https://web.furycloud.io/engineering/applications/rio-playmaker/versions/detail/0.0.3-test-sig600-acme) | **409**, componentes activos.<br><img width="360" alt="Solo ACME: bloqueo por componentes activos" src="https://github.com/user-attachments/assets/0fb24f5c-2e4d-43d9-a7ae-f8375145b9e0" /> |
| Solo Kraken | [0.0.4-test-sig600-kraken](https://web.furycloud.io/engineering/applications/rio-playmaker/versions/detail/0.0.4-test-sig600-kraken) | **409**, componentes activos.<br><img width="360" alt="Solo Kraken: bloqueo por componentes activos" src="https://github.com/user-attachments/assets/ff0aa656-ee85-4e26-b267-d3129215f8b2" /> |

**Cómo probar:** desplegar la versión elegida en `test3` y llamar `DELETE /data-products/{id}` directamente a Playmaker, con Tiger válido y un DP descartable del run que tenga un despliegue no importado en `deploy_requested` o `deploy_completed`. Verificar el resultado de la tabla y que no se borró ningún recurso. Sin bloqueos, las versiones ACME/Kraken ejecutan el borrado real; la versión sin permisos mantiene el 403. Limpiar los recursos propios al finalizar.

Los mocks están en ramas separadas, basadas en `73fabcfb9`; no forman parte de este PR. La conectividad/permisos reales de Kraken y el 503 en un entorno desplegado requieren validación adicional.

## Contrato de pruebas

<details>
<summary>Evidencia y pendientes</summary>

- [x] `.testing/impact.json` actualizado.
- [x] Escenarios AT y tests focalizados declarados.
- [ ] Justificación de comportamiento sin cambios: no aplica, cambia la autorización.
- [x] Evidencia distingue entornos y capas de prueba.
- [x] Recursos de LOCAL_STACK eliminados y limpieza verificada.
- [ ] Ledger y certificado de limpieza F1 adjuntos: se aportaron capturas de UI, no estos artefactos.

</details>

## Issue

[SIG-643 — técnica](https://spellbook.adminml.com/projects/SIG/specs/SIG-643) · [SIG-600 — funcional](https://spellbook.adminml.com/projects/SIG/specs/SIG-600)

---

## Notas internas — NO van al PR

- Revisión puntual del comentario existente #discussion_r4144981821: confirmado contra DELETE/findById → autorización remota → save, UPDATE permite cambiar teamName y DataProductModel/BaseModel no tienen @Version. La carrera puede autorizar por un equipo viejo; no se aplicó un fix ni se publicó respuesta al reviewer. Recomendación: coordinar el bloqueo en DELETE y los escritores de ownership y probar ambos órdenes de la carrera. El findByIdForUpdate existente filtra deletedAt IS NULL; reutilizarlo ciegamente cambiaría el contrato de DP ya borrado. Una relectura sin lock/refresh o dentro del mismo contexto JPA no ofrece la garantía necesaria. No se ejecutó una revisión completa del PR mediante Zord: se analizó únicamente el comentario solicitado.

- El usuario autorizó actualizar la descripción en GitHub, resolver lo necesario para dejar CI verde y pasar el PR a Ready for review. Esa instrucción explícita prevalece sobre la restricción genérica de publicación de la skill pr-description.
- Conflicto con develop resuelto únicamente en .testing/impact.json, uniendo escenarios y selectores de ambos lados. Se portó el arreglo del test de fecha ya usado en las variantes mock; no se agregó código de mocks al PR funcional.
- GenerateDocTest modifica metadata Swagger ajena a la autorización (environment/source_environment_id); se restauró el espejo canónico de develop para no incluir ese ruido.
- Las capturas son evidencia manual de UI aportada por el usuario. No prueban por sí solas el HTTP ni el acceso a Kraken real. El ledger y cleanup F1 no fueron proporcionados. El agente no ejecutó deploy ni DELETE remoto.
- SIG-600 y SIG-643 no se editaron. Siguen fuera de este PR los tres blockers nuevos, el frontend/BFF y la discrepancia de CA-1. El usuario pidió expresamente español y síntesis; esa instrucción prevalece sobre el idioma inglés del template. Se conserva el orden de secciones y las casillas; se sintetizan los subpuntos de revisión y se colapsan los checklists.

## Fuentes

- [PR #1228](https://github.com/melisource/fury_rio-playmaker/pull/1228)
- Template .github/pull_request_template.md, diff contra develop y tests locales del HEAD 37dc1f2d3.
- BuildApi oficial de Fury: las tres versiones mock verificadas FINISHED, con tests habilitados y commits iguales a sus refs publicadas.
