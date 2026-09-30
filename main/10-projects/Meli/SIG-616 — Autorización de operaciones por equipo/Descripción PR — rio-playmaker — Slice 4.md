---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[rio-playmaker]]"
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
  - "[[SPEC técnica — Slice 4 — Relaciones y pipelines]]"
aliases: []
tags:
  - kind/doc
created: "2026-09-23"
updated: "2026-09-30"
---

# Descripción PR — rio-playmaker — Slice 4

`rio-playmaker` · branch `feature/operation-authorization-by-team-f4@1c9f1aba7` + fix staged · base PR `develop@621167382` · 52 commits existentes · diff local total 47 archivos, +1623/-380 · SIG-616/SIG-621 · sin dependencias nuevas entre repos · suite PASS el 2026-09-30.

> [!warning] Bloqueantes
> **Corrección local sin commit/push:** el PR remoto todavía conserva el rechazo cross-DP en delete. **Gate MySQL previo fallido:** el orden de migraciones impide bootstrap; dos checks del stack quedaron sin ejecutar. **Conflictos contra develop:** GitHub CONFLICTING/DIRTY. **Política sin owner:** riesgo del cascade pendiente de elección. Review humano, sub-SPEC F4 y smoke remoto pendientes.

## Propósito

Guardar la descripción verificable del PR como recurso de la iniciativa, con la corrección local autorizada para limpiar relaciones históricas.

## Contenido

---

## Description

feat(sig-616): authorize configured relation, pipeline and cascade operations

Este PR agrega autorización configurable a nueve operaciones existentes de F4. El guard sólo se activa para un par exacto de `app.action-authorization.permissions`; el nivel se toma de esa configuración. F4 forma parte de la entrega por slices de SIG-616; F5 y el smoke remoto siguen pendientes.

* Relaciones: create/update exigen source y destination en el mismo DP y responden `400` antes de ACME o persistencia si son cross-DP. Delete permite limpiar relaciones cross-DP históricas aplicando `component-relation:delete` a cada owner persistido distinto antes del soft delete. Con ownership completo y regla configurada, ambos deben autorizar; deny o falla ACME impiden toda mutación. Update autoriza owners actual y solicitado al cambiar endpoints.
* Pipeline: replace-topology, update-design, update-relations, create-component y deploy usan el scope `pipeline` antes del primer side effect. Relaciones y pipeline usan `DEV_AND_UP` en la configuración efectiva.
* Cascade: `DELETE /data-products/{id}` conserva blockers y bypass histórico de plataforma; los demás usuarios con ownership completo pasan por `data-product:cascade-delete-components=DEPLOYER_AND_UP`. Actualmente sin `teamName` se omiten tanto el precheck ACME heredado como el guard F4; con equipo y sin proyecto se conserva el precheck. Ese riesgo sigue pendiente de una alternativa de compatibilidad, sin backfill masivo.
* No se agregan endpoints, modelos, schema ni estados. Se actualizan arquitectura, escenarios y `.testing/impact.json`; no hubo cambios de OpenAPI al regenerarlo.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — review humano, sub-SPEC y smoke pendientes.
* [x] I have used conventional commits — commits previos del PR; esta corrección todavía no está commiteada.
* [x] My code follows the style guidelines of this project.
* [x] I have performed a self-review of my own code.
* [x] I have commented portions of my code, particularly in hard-to-understand areas — no se necesitó un comentario productivo nuevo para retirar el check de delete.
* [x] I updated the applicable canonical documentation.
* [x] After my changes were applied the app is still buildable — `check` PASS.
* [ ] My changes generate no new warnings (linters, code quality) — warnings preexistentes de JVM/Gradle; análisis remoto del fix aún no ejecutado.
* [x] I have added tests that prove my fix is effective or that my feature works — unit con autorizador real y H2/HTTP con owners persistidos.
* [x] New and existing unit tests pass locally with my changes.
* [ ] Any dependent changes have been merged and published in downstream modules — sub-SPEC y validación remota de F4 pendientes; no se cambian módulos downstream en este fix.
* [ ] I have updated my current branch with changes made in develop/master previously — GitHub informa conflictos contra el develop actual.
* [ ] I already deployed this branch in the pre-production environment — no se desplegó.

## Code Review checklist (must be completed by the code reviewer)

* [ ] Is it the issue being completed?
* [ ] Is the code good in style?
* [ ] The code runs correctly? (Optional)
* [ ] Is this a good enough implementation?

## How Has This Been Tested?

Evidencia del 2026-09-30: HEAD `1c9f1aba77c0fd749924b879d3ad55982e16b56d` más el diff staged local de seis archivos; la corrección no está publicada en GitHub.

* `./scripts/run-agentic-testing-contract.sh --plan` — L0/CONTRACT PASS; 51 selectores y tres checks declarados.
* `./gradlew test --offline --no-daemon --tests com.mercadolibre.rio.playmaker.service.impl.ComponentRelationServiceImplTest --tests com.mercadolibre.rio.playmaker.integration.ComponentRelationControllerIntegrationTest` — L0/UNIT + H2_INTEGRATION PASS; 51 casos entre las dos clases, incluyendo ambos grants, deny de cada owner y ACME unavailable.
* `./scripts/run-agentic-testing-contract.sh` — los 51 selectores pasaron. El primer check L0/LOCAL_STACK falló con MySQL 3959: una migración previa intenta eliminar `component_type` antes de sustituir `chk_deployment_freeze_reach`. Los dos checks restantes no se ejecutaron por la dependencia común. Cleanup verificado sin contenedores, volúmenes ni redes propios.
* `./gradlew check jacocoTestReport --offline --no-daemon` — L0/UNIT + H2_INTEGRATION PASS; 4.097 tests, cero fallas/errores, dos skips; cobertura global 14.689/15.118 líneas (97,16%). No se agregaron líneas productivas en este fix. `GenerateDocTest` no produjo diff de Swagger.
* `git diff --check` y `git diff --cached --check` — PASS.
* Sin Zord por instrucción explícita del usuario; sin L1/F1, smoke remoto ni mutaciones de datos externos. H2 no sustituye los checks del stack pendientes.

## Testing contract

* [x] I added or updated `.testing/impact.json`.
* [x] The impacted/new AT scenarios and focused tests are declared in the manifest — AT-050-S15 queda en create/update; AT-050-S16 cubre limpieza histórica cross-DP.
* [ ] If behavior is unchanged, the manifest includes the reviewed scenarios and a concrete justification — no aplica: cambia el delete cross-DP.
* [x] Evidence distinguishes environment (`L0`, `L1`, `F1`) from layer (`UNIT`, `H2_INTEGRATION`, `CONTRACT`, `LOCAL_STACK`, `ECOSYSTEM_STACK`, `SMOKE`).
* [x] Any mutable run published cleanup evidence; blocked L1/F1 capabilities are declared rather than replaced with L0 evidence — cleanup local verificado; F1 no ejecutado.

## Issue

[SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616) · [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621).

---

## Notas internas — NO van al PR

- D25 fue ajustada por el owner el 2026-09-30: same-DP se exige en create/update; delete histórico aplica guards a ambos owners persistidos. La SPEC técnica local está alineada. No se comprobó aprobación formal de una sub-SPEC en Spellbook.
- D26 sigue implementada sin cambios. Se propuso usar `systemId` persistido con `SystemsByUserService.getTeamCodeFromSystem` o un scope ACME fijo de compatibilidad para usuarios comunes. Son alternativas, no políticas aprobadas ni código aplicado. No se asume que todos los DPs tienen `systemId`.
- La descripción remota y los hilos de review no se modificaron. El texto anterior de GitHub sigue describiendo el rechazo de delete cross-DP hasta publicar esta corrección. No se resolvieron conflictos ni se editaron migraciones.
