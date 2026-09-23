---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
  - "[[SPEC técnica — Slice 5 — Actions restantes]]"
  - "[[rio-playmaker]]"
aliases:
  - PR Slice 5 SIG-616
tags:
  - kind/doc
  - project/sig-616-operation-authorization
created: "2026-09-16"
updated: "2026-09-23"
---

# Descripción PR — rio-playmaker — Slice 5

**Identidad:** `melisource/fury_rio-playmaker` · branch `feature/operation-authorization-by-team-f5@a89fcffcb` · base `feature/operation-authorization-by-team-f4@e75ca90d9` · [PR #1182](https://github.com/melisource/fury_rio-playmaker/pull/1182) · SPEC [[SPEC técnica — Slice 5 — Actions restantes]].

## Propósito

Mantener la descripción verificable del PR de F5 junto al proyecto SIG-616 y su base F4 vigente.

## Contenido

El cuerpo siguiente refleja el PR publicado tras integrar la corrección F4 y agrupar los permisos Flink por familia. La verificación local pasó con 4.086 tests y dos skips preexistentes; el smoke no productivo Tiger/ACME sigue pendiente.

---

## Description

feat(auth): configure remaining mutating Actions

Este PR completa el Slice 5 de SIG-616 agregando validación ACME para Actions mutantes ya existentes de Flink y ClickHouse mediante YAML en `app.action-authorization`. Integra la última corrección de Slice 4 (`e75ca90d9`), incluido el bypass histórico de equipos plataforma en el cascade. No crea Actions, endpoints ni casos de uso; no cambia lecturas, pares no configurados, precreation ni el tratamiento de componentes importados.

Changes:

* Define las familias abstractas `flink-sql` y `flink-job` en YAML: `start/stop` requieren `DEV_AND_UP` para `flink-sql`/`gcp-flink-sql` y `aws-flink-job`/`gcp-flink-job`, respectivamente. Los nombres concretos sólo aparecen como miembros; quitar el permiso de una familia desactiva el guard adicional para AWS y GCP. Agrega el par exacto `clickhouse-mat-view` + `start-materialized-view/stop-materialized-view`.
* Conserva las reglas F2–F4 de señales, relaciones, pipelines y cascade en `permissions`; las operaciones no-component usan lookup exacto y no heredan el wildcard de components.
* Verifica familias y pares F5 contra `application.yml` real, mantiene las pruebas de guards F4 y prueba que la denegación ocurre antes de KVS y BigQueue.
* Actualiza la trazabilidad de escenarios existentes, el manifiesto de testing, la documentación de verificación y el `403` de la ruta component-bound.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — falta el smoke no productivo con Tiger/ACME reales.
* [x] I have used [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* [x] My code follows the style guidelines of this project
* [x] I have performed a self-review of my own code
* [x] I have commented portions of my code, particularly in hard-to-understand areas
* [x] I updated the applicable canonical documentation (`testing-scenarios.md`, Swagger y documento de verificación; no cambian arquitectura ni entornos de testing).
* [x] After my changes were applied the app is still buildable
* [ ] My changes generate no new warnings (linters, code quality) — CI remota bloqueada antes del checkout por error de certificado en Jenkins.
* [x] I have added tests that prove my fix is effective or that my feature works
* [x] New and existing unit tests pass locally with my changes
* [ ] Any dependent changes have been merged and published in downstream modules — F4 sigue abierto como base de este PR.
* [x] I have updated my current branch with changes made in develop/master previously — F5 incorpora F4 `e75ca90d9`, que ya contiene el merge de `develop`.
* [ ] I already deployed this branch in the pre-production environment

## Code Review checklist (must be completed by the code reviewer)

* [ ] Is it the issue being completed?
* [ ] Is the code good in style?
* [ ] The code runs correctly? (Optional)
* [ ] Is this a good enough implementation?

## How Has This Been Tested?

HEAD: `a89fcffcb21f7a09286ca1e5d2d9ec09eaf04fec` · base F4: `e75ca90d98fba2dc4e4ef35686e2f38cf8462402`.

* L0/UNIT + H2_INTEGRATION + CONTRACT: `./scripts/run-agentic-testing-contract.sh` pasó sus 25 selectores focalizados; `./scripts/validate-repository-contract.sh` y `./scripts/validate-testing-contract.sh --staged` pasaron.
* L0/LOCAL_STACK: `AT-000-S01` y `AT-180-S18` pasaron con MySQL aislado; el runner eliminó contenedores, redes y volúmenes propios.
* L0/FULL_REGRESSION: `./gradlew check --no-daemon` pasó con 4.086 tests, 0 fallas, 0 errores y 2 skips preexistentes.
* JaCoCo local: `./gradlew jacocoTestReport --no-daemon` pasó; `ConfiguredActionPermissionProvider` registró 31/31 líneas cubiertas.
* Diferencia F4→F5: 11 archivos; no hay cambios en la implementación de `ActionServiceImpl`, los otros casos de uso ni sus endpoints.
* CI remota: [job #5490](https://rp-ci-java.furycloud.io/job/rio-playmaker/5490/) falló antes del checkout de la aplicación porque Git no confía en el certificado al descargar `fury_rp-ci-pipelines.git`. Cobertura y dependencias fueron abortadas por ese fallo; no hay resultado remoto de código para este HEAD.
* F1/SMOKE Tiger/ACME real: pendiente de ejecución no productiva; esta evidencia local no lo reemplaza.

## Testing contract

* [x] I added or updated `.testing/impact.json`, or this PR does not change an observable-behavior surface.
* [x] The impacted/new AT scenarios and focused tests are declared in the manifest.
* [ ] If behavior is unchanged, the manifest includes the reviewed scenarios and a concrete justification — no aplica: la validación ACME configurada agrega comportamiento.
* [x] Evidence distinguishes environment (`L0`, `L1`, `F1`) from layer (`UNIT`, `H2_INTEGRATION`, `CONTRACT`, `LOCAL_STACK`, `ECOSYSTEM_STACK`, `SMOKE`).
* [x] Any mutable run published cleanup evidence; blocked L1/F1 capabilities are declared rather than replaced with L0 evidence — los checks L0 limpiaron recursos propios; el smoke F1 sigue pendiente.

## Issue

* [SIG-616 — Autorización de operaciones por equipo](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
* [SIG-621 — Autorización de operaciones por equipo](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)

---

## Notas internas — NO van al PR

- El PR #1182 informa base F4 `e75ca90d9`, HEAD F5 `a89fcffcb` y `MERGEABLE` tras el push. CI #5490 falló en infraestructura antes del checkout por certificado no confiable; cobertura y dependencias se abortaron. Re-request de GitHub devolvió 404; el smoke no productivo sigue pendiente.
- La diferencia F4→F5 modifica 11 archivos: configuración, adapter de permisos, pruebas, manifest de testing, Swagger y documentación. No cambia los casos de uso ni introduce Actions.
