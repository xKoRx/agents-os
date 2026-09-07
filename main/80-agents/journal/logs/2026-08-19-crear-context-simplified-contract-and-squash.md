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
  - "[[reference-spellbook-cli]]"
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

# 2026-08-19-crear-context-simplified-contract-and-squash

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/Crear Context/SPEC Funcional — Context IO.md` — condensado y contrato reescrito; publicado en SIG-573.
  - `10-projects/Meli/Crear Context/Crear Context.md` — estado, contrato v1 y rama de entrega.
  - Repos externos (fuera del vault): `rio-sdk-events` `ComponentContext` reescrito 440→105 líneas; `rio-playmaker` `ComponentContextBuilder` 731→264 líneas.

## Motivo

El equipo simplificó el alcance: el Context deja de modelar properties, mappings, issues y completeness, y pasa a un contrato mínimo `dataProduct` + `lastVersion` + `sources`/`destinations`, con `RelatedComponent` = `name`/`type`/`outputs`. El spec funcional además estaba verboso (13.6k chars) para una definición simple.

## Fuentes usadas

- Dictado directo del usuario sobre el contrato y las podas sucesivas de RF.
- Código: `ParameterParseServiceImpl` (unwrap `.value` retrocompat), `DeploymentResultHandlerImpl.storeResultOutput` (persistencia verbatim del output del CP), `PipelineConfigPatchServiceImpl` (el slot del service es estado deseado).
- Convenciones de spec: skill `signals-spec-authoring`.

## Resolución aplicada

- **Outputs = valores ya resueltos** (`Map<String,String>`), no passthrough del wrapper `{type,value,sensitive}`: desenvolver es del resolver de params, y al CP le llega data resuelta. Corrige una recomendación previa mía en sentido contrario.
- **`lastVersion` sale del historial de deployments**, no del slot: `service.componentDefinition` es estado deseado y ya apunta a la versión que se está desplegando. Query nueva `DeploymentRepository.findLastCompletedSemver` (status se guarda como `Action_Status`, de ahí el match por sufijo).
- **Fuera de alcance explícito:** no se toca la operación del mensaje (`DeploymentOperation.PROVISION` sigue hardcodeada). Se intentó derivar `PROVISION`/`UPDATE` y se revirtió: es código preexistente, ajeno al Context, y cambiaba lo que reciben los CP.
- **Entrega:** rama `feature/component-context` en `rio-playmaker`, 1 commit (`component context`) recién salido de `origin/develop`, sin upstream. El SDK queda con sus 4 commits, por decisión del usuario.

## Validación

- Suites completas verdes en ambos repos; 12 tests nuevos del builder + 7 del contrato SDK.
- Árbol del commit final verificado idéntico al ya testeado (solo cambió el mensaje).
- Payload verificado serializando `DeploymentTriggerMessage`: `params` y `context` viajan como campos hermanos.
- Security build mode (reglas Java): APPROVED, 0 blocking. Gate fail-closed del importado (CWE-862) y no-logueo de valores (CWE-532/209) cubiertos por test.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Tag `backup/pre-sync-20260819-214938` en `rio-playmaker` conserva el estado previo al squash; la rama vieja `feature/SIG-573-context-io` sigue en origin con la historia anterior.
