---
type: change_log
schema_version: 1
scope: session
created: "2026-08-20"
updated: "2026-08-20"
area: "[[Meli]]"
project: "[[Crear Context]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
  - "[[rio-sdk-events]]"
related:
  - "[[2026-08-19-crear-context-code-review-and-pr-docs]]"
  - "[[2026-08-19-crear-context-simplified-contract-and-squash]]"
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

# Crear Context — spec técnica reescrita y publicada (SIG-589)

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `10-projects/Meli/Crear Context/SPEC Tecnica — Context IO.md` — reescrita de cero (23.4k → 24.6k)
  - `10-projects/Meli/Crear Context/Crear Context.md` — callout de estado, sección Contrato v1, nota histórica y bitácora
  - Spellbook `SIG-589` "Context de componente — Spec Técnica" (technical, draft) — creada y publicada

## Motivo

El funcional SIG-573 quedó reescrito con el contrato de la cuarta pasada (objetos `data_product` / `component` / `last_deployed_version`, `id` en `RelatedComponent`) y la spec técnica seguía describiendo el envelope rico descartado en la tercera pasada. El equipo trabaja con Spellbook SDD, así que la técnica tiene que existir como spec propia y no solo como nota del vault.

## Fuentes usadas

- SIG-573 leído por CLI (`spellbook specs view 73560842-8585-411a-96a8-5722cdf1a974`), versión del 2026-08-20T22:56Z
- `rio-sdk-events` @ `feature/SIG-573-component-context` (`d21001b`): `ComponentContext.java`, `build.gradle`
- `rio-playmaker` @ `feature/component-context` (`e6fadaf0b`) y `feature/component-context-test` (`e6b810f05`): `ComponentContextBuilder`, `BatchDispatchServiceImpl`, `DeploymentRepository`, `DispatchRequest`, `BigQueueDispatchAdapter`, `DeploymentTriggerProducerImpl`, `application.yml`
- `DeploymentModel.setStatus` / `DeploymentStatus` / `DeploymentAction` para confirmar el formato `<action>_<status>`
- `DataProductModel` para confirmar `team_name` y `environment` como columnas reales
- Skill `meli-security-expert` en Build mode: reglas Java, CWE-532, CWE-209, CWE-862

## Resolución aplicada

Decisión del usuario: publicar en vault **y** Spellbook, y borrar el discovery por tipo de componente en vez de moverlo a anexo. La spec técnica quedó en 9 secciones: contrato de datos con tabla de campos calificados, derivación, punto de integración, seguridad, delta contra lo implementado (por repo + 3 bugs), verificación, rollback/bloqueantes, supuestos y apps afectadas. Se caracterizó la iniciativa como **modificación, no refactor**. `SIG-589` no pudo colgarse de `SIG-573` como hijo: la API rechaza `parentId` si el padre no es epic.

## Validación

`spellbook specs view 200634bf-806c-4b58-8875-d7353153c711` releído contra el remoto: 23.945 chars, type `technical`, status `draft`, marcadores presentes (`LastDeployedVersion`, `B-1`/`B-2`/`B-3`, `1.4.0`, `deploy_completed`, `CWE-862`) y sin wikilinks sin resolver. Sin cambios en repos: no se tocó código.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

Borrar `SIG-589` en Spellbook y restaurar las dos notas del vault desde el snapshot previo del vault (la versión anterior de la spec técnica está descrita en `2026-08-19-crear-context-code-review-and-pr-docs`).
