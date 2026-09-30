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

`rio-playmaker` · branch `feature/operation-authorization-by-team-f4@99c51fe8b` · base `develop@0c9e9e3ee` · 53 commits · 53 files changed, 1724 insertions(+), 393 deletions(-) · SIG-616/SIG-621 · sin dependencias nuevas entre repos · suite y stacks locales PASS el 2026-09-30.

> [!warning] Pendientes
> **Aprobación humana, sub-SPEC formal y smoke no productivo.** dependencies FAIL; los demás checks publicados pasaron. GitHub `MERGEABLE` / `BLOCKED` / `REVIEW_REQUIRED`. La excepción sin equipo conserva el riesgo reconocido por el reviewer y aceptado expresamente por el owner.

## Propósito

Guardar la descripción verificable del PR como recurso de la iniciativa y publicar su contrato final autorizado.

## Contenido

---

## Description

feat(sig-616): authorize configured relation, pipeline and cascade operations

Este PR agrega guards configurables a nueve operaciones existentes de F4. Cada guard usa el par exacto de `app.action-authorization.permissions`; quitarlo conserva el flujo previo sin la consulta ACME nueva. F5 y el smoke remoto completan las fases posteriores. La rama integra `develop@0c9e9e3ee`; la corrección final quedó publicada en `99c51fe8b`.

* Relaciones: create/update exigen same-DP y rechazan cross-DP con `400` antes de ACME o persistencia. Delete permite limpiar relaciones cross-DP históricas aplicando `component-relation:delete` a cada owner persistido distinto antes del soft delete. Con ownership completo y regla configurada, ambos owners deben autorizar; deny o falla ACME impiden toda mutación. Update autoriza el owner actual y el solicitado al mover ambos endpoints a otro DP válido.
* Pipeline: replace-topology, update-design, update-relations, create-component y deploy aplican el guard `pipeline` antes del primer side effect. La configuración efectiva de relaciones y pipeline usa `DEV_AND_UP`.
* Cascade: `DELETE /data-products/{id}` mantiene los blockers y el bypass histórico de plataforma. Los demás usuarios con ownership completo requieren `data-product:cascade-delete-components=DEPLOYER_AND_UP`. Si falta `teamName`, se omiten tanto el precheck ACME heredado como el guard F4. Con equipo y sin `projectCode`, permanece el precheck de pertenencia al equipo y se omite sólo el guard nuevo.
* **Excepción y riesgo aceptados para F4:** un usuario autenticado sin grants puede borrar un DP sin equipo y sus componentes si pasan las precondiciones de estado y blockers. Tiger autentica; no sustituye el permiso de borrado. El owner ratificó mantener esta compatibilidad sin backfill masivo ni restringir esos DP a plataforma. [Decisión respondida al reviewer](https://github.com/melisource/fury_rio-playmaker/pull/1181#discussion_r4146982952).
* Los scopes no-component usan lookup exacto, sin heredar el wildcard de componentes. Configuración ausente y ownership incompleto conservan el contrato aditivo; las rutas legacy retienen sus políticas. Los controllers pasan `Authentication.getName()` y mantienen los headers necesarios para ACME/downstreams.
* Se corrigió el bootstrap local para aplicar la sustitución del CHECK antes del DROP histórico y se ajustó la detección de puerto a Jetty/Tomcat. No se cambiaron SQL de migraciones ni se omitieron constraints. La metadata OpenAPI incorporada desde develop se genera ahora desde sus anotaciones; no cambia el comportamiento de esos endpoints.

Los comentarios quedaron contestados y resueltos, incluyendo la actualización de las respuestas previas sobre delete cross-DP. Las observaciones opcionales de refactor y consolidación de políticas siguen documentadas como mejoras posteriores. Falta aprobación humana, publicación/aprobación formal de la sub-SPEC F4 bajo SIG-621 y smoke no productivo; la decisión local del owner no se presenta como aprobación de Spellbook.

## Dev checklist (should be completed by the developer assigned to the issue)

* [ ] I have met the definition of done — aprobación humana, sub-SPEC formal y smoke pendientes.
* [x] I have used conventional commits.
* [x] My code follows the style guidelines of this project.
* [x] I have performed a self-review of my own code.
* [x] I have commented portions of my code, particularly in hard-to-understand areas.
* [x] I updated the applicable canonical documentation (`docs/architecture.md`, `testing.md`, `testing-scenarios.md`, Swagger and `.testing/impact.json`).
* [x] After my changes were applied the app is still buildable.
* [ ] My changes generate no new warnings (linters, code quality) — permanecen avisos preexistentes de JVM/Gradle; dependencies FAIL; los demás checks publicados pasaron.
* [x] I have added tests that prove my fix is effective or that my feature works — autorizador real y HTTP/H2.
* [x] New and existing unit tests pass locally with my changes.
* [x] Any dependent changes have been merged and published in downstream modules — sin dependencias downstream nuevas.
* [x] I have updated my current branch with changes made in develop/master previously — merge de `0c9e9e3ee`, sin reescritura de historia.
* [ ] I already deployed this branch in the pre-production environment — no se desplegó.

## Code Review checklist (must be completed by the code reviewer)

* [ ] Is it the issue being completed?
* [ ] Is the code good in style? (Easy to read, follows good practices and our style guide)
* [ ] The code runs correctly? (Optional)
* [ ] Is this a good enough implementation?

## How Has This Been Tested?

Evidencia local del 2026-09-30 sobre el árbol publicado en `99c51fe8bd3da2e73ede96ae717a1ab1fae723c7`:

* `./scripts/run-agentic-testing-contract.sh --plan` — L0/CONTRACT PASS: 53 selectores y tres checks declarados; manifiesto y catálogo combinados sin perder los escenarios de develop.
* `./scripts/run-agentic-testing-contract.sh` — PASS: 53 selectores L0/UNIT + H2_INTEGRATION y los tres checks L0/LOCAL_STACK (MySQL/app, deployment loopback y Kafka). Los tres completaron cleanup certificado; Kafka publicó `CLEANUP_CERTIFIED`. Sin recursos Compose propios restantes.
* `./gradlew check jacocoTestReport --offline --no-daemon` — PASS: 4.129 tests en 372 suites, cero fallas/errores y 2 skips preexistentes; 14,781/15,209 líneas cubiertas (97,19%).
* Relaciones: 51 casos entre las clases unit e integración; grants de ambos owners antes de save, deny de cualquiera y ACME unavailable sin mutación. HTTP/H2 persiste relaciones históricas y comprueba `200`/`403` y estado persistido. Create/update same-DP y deduplicación de owner siguen cubiertos.
* `GenerateDocTest` regenera OpenAPI desde las anotaciones; el resultado generado queda publicado. `git diff --check`, validadores de contrato y `bash -n local/01-mysql.sh scripts/run-local-kafka-stack-check.sh` — PASS.
* Checks remotos del mismo HEAD: dependencies FAIL; los demás checks publicados pasaron — [ejecución CI](https://rp-ci-java.furycloud.io/blue/organizations/jenkins/rio-playmaker/detail/rio-playmaker/5625/pipeline/). GitHub mantiene `REVIEW_REQUIRED`; resolver comentarios no equivale a aprobación.
* Sin Zord por instrucción explícita del owner; sin L1/F1, smoke remoto ni deployment. Las variantes test3 anteriores `0.1.15-p4-committer-allowed` / `0.1.16-p4-viewer-denied` no incluyen este nuevo HEAD y no certifican esta corrección.

## Testing contract

* [x] I added or updated `.testing/impact.json`, or this PR does not change an observable-behavior surface.
* [x] The impacted/new AT scenarios and focused tests are declared in the manifest — AT-050-S16 cubre delete histórico; AT-000-S10 cubre bootstrap y descubrimiento del puerto local.
* [ ] If behavior is unchanged, the manifest includes the reviewed scenarios and a concrete justification — no aplica: cambia delete cross-DP.
* [x] Evidence distinguishes environment (`L0`, `L1`, `F1`) from layer (`UNIT`, `H2_INTEGRATION`, `CONTRACT`, `LOCAL_STACK`, `ECOSYSTEM_STACK`, `SMOKE`).
* [x] Any mutable run published cleanup evidence; blocked L1/F1 capabilities are declared rather than replaced with L0 evidence.

## Issue

[SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616) · [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621).

---

## Notas internas — NO van al PR

- D25: create/update conservan same-DP; delete admite limpieza histórica aplicando guards de owners persistidos distintos. D26: se mantiene explícitamente la excepción sin equipo y su riesgo, sin exigir backfill masivo. La SPEC local quedó alineada; no se afirma aprobación formal de Spellbook.
- La descripción y las respuestas de GitHub se actualizaron por autorización explícita del owner. Los hilos se resolvieron por fix probado o decisión documentada; la resolución no equivale a aprobación del reviewer.
- El merge de develop preservó escenarios y tests de ambas ramas. Se reparó el runner local sin alterar las migraciones SQL; también se corrigió su descubrimiento de puerto Jetty. Swagger deriva de las anotaciones y refleja la regla real de importación.
