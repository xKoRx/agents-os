---
type: change_log
schema_version: 1
scope: session
created: "2026-08-25"
updated: "2026-08-25"
area: "[[Meli]]"
project: "[[Crear Context]]"
application:
entities:
  - "[[Crear Context]]"
  - "[[rio-sdk-events]]"
  - "[[rio-playmaker]]"
related:
  - "[[SPEC Funcional — Context IO]]"
  - "[[SPEC Tecnica — Context IO]]"
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

# Crear Context — separación de inputs y outputs

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/Crear Context/Crear Context.md`
  - repo `rio-playmaker` → `.sdd/features/new-component-context/1-functional/spec.md`
  - repo `rio-playmaker` → `.sdd/features/new-component-context/2-technical/spec.md`
  - repo `rio-playmaker` → `.sdd/features/new-component-context/3-tasks/tasks.md`
  - repo `rio-sdk-events` → `src/main/java/com/mercadolibre/rio/sdk/events/deployment/context/LastDeployedVersion.java`
  - repo `rio-sdk-events` → `src/main/java/com/mercadolibre/rio/sdk/events/deployment/context/RelatedComponent.java`
  - repo `rio-sdk-events` → tests de contrato, `CHANGELOG.md` y `build.gradle`

## Motivo

- El owner corrigió el modelo: la configuración ingresada por el usuario es `inputs`; los valores generados por los control planes después de provisionar son `outputs`; ambos deben viajar separados en vez de compartir un único mapa.
- La branch feature del SDK tenía una versión productiva limpia `1.4.0`; se devolvió a `0.0.5-component-context-inputs` para cumplir la regla de release del proyecto.

## Fuentes usadas

- Pedido explícito del owner y diagrama adjunto del 2026-08-25.
- Código vigente de `rio-sdk-events/feature/new-component-context` sobre `1c0ff51`.
- Copias SDD canónicas de SIG-573/SIG-590 bajo `.sdd/features/new-component-context/` en `rio-playmaker`.

## Resolución aplicada

- `LastDeployedVersion` y `RelatedComponent` agregan `Map<String,String> inputs` antes de `outputs`; ambos mapas quedan no nulos e inmutables.
- Payloads anteriores sin `inputs` y constructores Java anteriores defaultéan `inputs = {}`; `outputs` conserva su contrato obligatorio.
- `toString` reporta sólo cardinalidades y no expone claves ni valores de ninguno de los mapas.
- Las SPECs distinguen fuente y semántica: `inputs` proviene de `component_definition.parameters`; `outputs`, de `_values`. Poblar `inputs` en Playmaker queda como T-24 y exige revisar sensibilidad y autorización cross-data-product.
- La nota [[Crear Context]] reemplaza el contrato vigente, el estado y las tareas desactualizadas por el challenge actual.
- La branch `rio-sdk-events/feature/new-component-context` quedó commiteada y pusheada en `d6903aa`.

## Validación

- Gate completo del SDK: 699 tests PASS y `jacocoTestCoverageVerification` PASS.
- `git diff --check` PASS antes del commit; push `1c0ff51..d6903aa` a `origin/feature/new-component-context`.
- Lint estricto del proyecto y este change log: `ERROR=0 WARN=0`; contrato de schemas: `errors=0`.
- Reindexación Graphify intentada y bloqueada por 11 errores/6 warnings ajenos al delta en las skills de specs y `zsh-modifier-breaks-git-show-sha-path`; los dos archivos modificados pasan lint estricto y no aparecen en los findings.
- Spellbook live no fue modificado; SIG-573/SIG-590 remotas quedan pendientes de sincronización.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit del challenge en `rio-sdk-events`, restaurar las tres copias SDD desde su estado previo y revertir el delta focal de [[Crear Context]]; no tocar los mirrors archivados del vault.
