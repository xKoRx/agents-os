---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
  - "[[SPEC técnica — Slice 4 — Relaciones y pipelines]]"
aliases: []
tags:
  - kind/doc
created: "2026-09-23"
updated: "2026-09-23"
---

# Descripción PR — rio-playmaker — Slice 4

## Propósito

Regularizar F4 como un delta completamente aditivo sobre F3/develop: autorización config-backed
para relaciones, pipeline y el cascade de Data Product reportado por Ale, sin endpoints ni reglas de
negocio nuevas.

## Contenido

## Description

feat(sig-616): authorize configured relation, pipeline and cascade operations

Este PR agrega guards de autorización sólo a nueve operaciones existentes. Cada guard se activa por
un par exacto de `app.action-authorization.permissions`; al quitar la entrada, el flujo previo se
mantiene y no se invoca ACME por ese guard.

Cambios:

- Relaciones: `create`, `update` y `delete` con scope `component-relation`, `DEV_AND_UP` y owners
  persistidos distintos. Update conserva el comportamiento de F3, incluido cambiar endpoints/Data
  Products; no se agregó same-DP ni ownership inmutable.
- Pipeline: `replace-topology`, `update-design`, `update-relations`, `create-component` y `deploy`
  con scope `pipeline` y `DEV_AND_UP`, antes del primer side effect.
- Cascade: `DELETE /data-products/{id}` autoriza una vez el Data Product persistido mediante
  `data-product:cascade-delete-components=DEPLOYER_AND_UP` antes de borrar components,
  notifications, publicar eventos o guardar. El bypass histórico de miembros de equipos plataforma
  sigue vigente; el guard nuevo aplica a los demás actores.
- Resolución exacta: los scopes no-component no usan el wildcard `component-type: "*"`, evitando
  colisiones con nombres como `create`, `update`, `delete`, `update-design` o `deploy`.
- Compatibilidad: ownership incompleto omite sólo los guards nuevos de F4; F1/F2/F3 mantienen su
  semántica previa. Component delete/inactivate siguen en `DEPLOYER_AND_UP`.
- Identidad: los controllers toman `Authentication.getName()` y la propagan; headers Tiger se
  conservan únicamente para ACME y cancelaciones downstream existentes.
- No se agregaron endpoints, casos de uso, schema, estados, reglas de ownership ni nuevos status.

### Permisos configurados

| Scope | Operaciones | Nivel |
|---|---|---|
| `component-relation` | `create`, `update`, `delete` | `DEV_AND_UP` |
| `pipeline` | `replace-topology`, `update-design`, `update-relations`, `create-component`, `deploy` | `DEV_AND_UP` |
| `data-product` | `cascade-delete-components` | `DEPLOYER_AND_UP` |

### Review

- El comentario de Ale en #1178 sobre cascade se implementó en `e8b957c47` y fue respondido con
  evidencia de tests.
- El comentario del bot sobre ownership inmutable no aplica: F3 ya permitía el cambio. Se conservó
  el baseline, se corrigió la documentación y se resolvió el thread.
- El comentario de kmontero sobre el cascade era válido: el guard inicial anulaba el bypass de
  equipos plataforma. Se corrigió en `e75ca90d9` y se agregó regresión con la configuración real.
- Los demás comentarios de F3 estaban corregidos en la base mergeada; no se duplicó lógica en F4.

### Sincronización

- F3 final: `e45830fe7`; merge inicial en F4: `7c9195a65`.
- F3 fue mergeado a develop como `19d70a6cf` y la rama se eliminó; GitHub retargeteó #1181 a
  `develop`.
- Merge final sin cambio de árbol: `d792b902b`. El PR está sin conflictos.
- Corrección de compatibilidad: `e75ca90d9`; es el HEAD vigente del PR.
- Después de ese merge, `develop` avanzó a `9a559dfb3` con metadata de agentes; el merge-tree sigue
  limpio. Las variantes de prueba nuevas incorporan `e75ca90d9`.

## Dev checklist

- [x] Implementación, documentación, tests y publicación de la rama completados.
- [x] Commits convencionales, self-review y estilo del repositorio.
- [x] Documentación canónica y `.testing/impact.json` actualizados.
- [x] Build, tests focalizados, regresión completa y coverage local pasaron.
- [x] No se agregó lógica de negocio ni se debilitó seguridad heredada.
- [x] No se desplegó en preproducción ni producción.

## How Has This Been Tested?

- `./scripts/validate-repository-contract.sh --staged` — PASS.
- `./scripts/validate-testing-contract.sh --staged` — PASS.
- `./scripts/run-agentic-testing-contract.sh` — PASS; 20 selectores focalizados y dos checks
  `L0/LOCAL_STACK`, ambos con cleanup certificado.
- `./gradlew check --rerun-tasks --no-daemon --no-build-cache` — PASS sobre `e75ca90d9`:
  3.995 tests, 0 fallas, 0 errores y dos skips preexistentes.
- `./gradlew jacocoTestReport --no-daemon --no-build-cache` — PASS.
- Coverage diferencial contra F3: 94/95 líneas ejecutables, 98,95%. Global:
  14.350/14.784, 97,06%.
- Con `application.yml` real y `DataProductAccessService` real: plataforma sin owner grant permite;
  usuario común sin grant deniega antes de efectos; grant suficiente permite.
- `git diff --check origin/develop...HEAD` — PASS.

### Versiones de prueba

- [`0.1.15-p4-committer-allowed`](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.15-p4-committer-allowed), rama `feature/sig-616-auth-p4-committer-test3-v19`, commit `632ce2bf9`.
- [`0.1.16-p4-viewer-denied`](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.16-p4-viewer-denied), rama `feature/sig-616-auth-p4-viewer-test3-v20`, commit `a4ddafb86`.

Ambas incorporan `e75ca90d9`, usan únicamente el profile/scope `test3`, terminaron `FINISHED` y no
fueron desplegadas. El team mock se excluyó de `app.acmeClient.platform-teams` sólo en estas variantes para
ejercitar el guard nuevo. `0.1.13`/`0.1.14` quedaron superadas; no se publicó versión estable.
El bypass de un miembro real de plataforma está cubierto por test automatizado con configuración
real, no por estas variantes mock; con `FURY_IS_TEST_SCOPE=true` se omite la precondición histórica
antes de evaluar la membresía plataforma.

### Casos manuales previstos

- Relación: committer permite; viewer deniega sin save.
- Pipeline deploy: committer permite; viewer deniega sin execution/run/dispatch.
- Cascade: admin/maintainer con grant del owner suficiente permite; miembro plataforma conserva el
  bypass histórico (cobertura automatizada; requiere otro entorno para smoke real); committer/viewer
  no-plataforma deniega sin mutaciones.
- Entrada removida: conserva comportamiento previo y no llama ACME por F4.
- Ownership incompleto: omite sólo el guard nuevo, compatible con F3.

## Riesgos y pendientes externos

- Checks visibles del nuevo HEAD (`continuous-integration`, `code-coverage`, `dependencies`, `workflow`) en `SUCCESS`; review `APPROVED`. GitHub aún informa `mergeStateStatus=BLOCKED`, sin conflictos (`MERGEABLE`).
- Deploy de las variantes terminadas y ejecución manual no productiva.
- No se ejecutó smoke remoto ni se modificaron datos externos.
- AppSec especializado no estaba disponible; se hizo auditoría manual y regresión completa.

## Issue

SIG-616

## Fuentes

- [PR #1181](https://github.com/melisource/fury_rio-playmaker/pull/1181)
- [[SPEC técnica — Slice 4 — Relaciones y pipelines]]
- [PR #1178](https://github.com/melisource/fury_rio-playmaker/pull/1178)
