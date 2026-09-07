---
type: change_log
schema_version: 1
scope: session
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Meli]]"
project: "[[Crear Context]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
  - "[[rio-sdk-events]]"
related:
  - "[[signals-context-flow]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-19-crear-context-code-review-and-pr-docs

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/Meli/Crear Context/Guía de implementación — Component Context.md` — creado
  - `10-projects/Meli/Crear Context/Descripción PR — rio-playmaker.md` — creado
  - `10-projects/Meli/Crear Context/Descripción PR — rio-sdk-events.md` — creado
  - `10-projects/Meli/Crear Context/Crear Context.md` — actualizado: tabla de branches por repo, 7 tareas nuevas derivadas del review, entrada de bitácora
  - `10-projects/Meli/Crear Context/SPEC Tecnica — Context IO.md` — actualizado: callout de desalineación con lo implementado
  - `~/.claude/skills/signals-code-review/` (fuera de `VAULT_ROOT`) — skill de usuario creada, con `references/pr-description.md`

## Motivo

Code review pedido sobre la entrega de SIG-573 en los dos repos, más tres deliverables: una skill de revisión de código alineada a las preferencias del usuario, una guía explicativa de la implementación y su cobertura de tests, y la descripción de PR. El usuario fijó además una convención nueva: la descripción de PR **no** se escribe como `descripcion_pr.md` en la raíz del repo, sino como recurso del proyecto en el vault, estructurada con el template `.github` del repo destino y siempre nombrando la branch.

## Fuentes usadas

- Diffs contra base real: `rio-playmaker` `dac615f47..e6fadaf0b` (12 archivos, +683/-14) y `rio-sdk-events` `9d86eb8..d21001b` (5 archivos, +280/-4).
- Suites corridas en la sesión: `rio-sdk-events` `./gradlew test jacocoTestCoverageVerification` → 696 passed, 0 failed, gate 88.8% OK. `rio-playmaker` `./gradlew test` → 3141 passed, 0 failed.
- Convenciones del repo: `CODING_GUIDELINES.md` y `.github/PULL_REQUEST_TEMPLATE.md` de `rio-sdk-events`; `.github/pull_request_template.md` de `rio-playmaker`.
- `meli-security-expert` en modo audit, con `references/rules/java-security-patterns-rules.md`.

## Resolución aplicada

- Veredicto del review: **aprobado con reservas**. 4 findings de corrección — sufijo `%completed` que también captura `undeploy_completed`; `Objects.requireNonNull` y `lastCompletedSemver` fuera del `try` que rompen la garantía "never throws"; outputs anidados sin clave `value` descartados en silencio; `findById` por vecino importado contra el batch declarado del resto. 5 findings de documentación/dead code — CHANGELOG del SDK describiendo el envelope descartado, javadoc que promete clasificación por sensibilidad inexistente, constraints Jakarta decorativos, SPEC técnica desalineada, commit `wip` en la branch del SDK. Gap de tests: el punto de creación en `BatchDispatchServiceImpl` y `findLastCompletedSemver` sin cobertura.
- Seguridad: sin inyección (JPQL parametrizado) y sin fuga por logs (se loguea solo el tipo de excepción, y `toString()` está redactado y verificado por test). Dos observaciones sí materiales: la marca de sensibilidad se descarta al desenvolver, y la autorización de import se infiere de un string de estado local mutable.
- Daño colateral de los builds: `docs/specs/swagger.yaml` en `rio-playmaker` quedó reordenado por la tarea de test y **se restauró** con `git checkout --`. Ambos repos quedaron limpios salvo `graphify-out/` sin trackear.
- Ningún archivo de código fue modificado: la revisión fue de solo lectura, sin regresión propia que corregir.
