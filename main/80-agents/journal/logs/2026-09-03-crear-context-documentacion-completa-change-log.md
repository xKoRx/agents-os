---
type: change_log
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Meli]]"
project: "[[Crear Context]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
related:
  - "[[2026-09-02-crear-context-playmaker-summary]]"
  - "[[Descripción PR — rio-playmaker]]"
aliases: []
confidence: verified
source_session: 9c1f9d46-34d9-4921-809f-b823fb3343f1
source_feedbacks:
  - "[[2026-09-02-crear-context-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Documentación completa del contrato cerrado, y corrección de dos afirmaciones falsas

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated / created
- **Archivo(s):**
  - `.sdd/features/new-component-context/2-technical/spec.md` en `rio-playmaker` — **updated**: 30,4k → 39,7k. `DD-1..DD-14` contiguas, con los textos congelados de DD-7 y DD-14 incorporados **literales**. Se fueron el viejo DD-7 (guard `hasEnvironmentMismatch` y `reason:env_mismatch`, que no existen en código), el viejo DD-8 ("sin camino cross-data-product"), `parameters["version"]` como fuente, el fallback a `component_template`, y la afirmación falsa de la "métrica clavada en 0".
  - `.sdd/features/new-component-context/1-functional/spec.md` — **updated**: 11,5k → 12,8k. `username`, el par de versiones como id de definición, `DataProduct.environment` como atributo, y RF-6/CA-5/E2E-3 reescritos porque decían que un vecino de otro data product no se lee contra el original, cuando el código sí lo lee.
  - `10-projects/Meli/Crear Context/Crear Context.md` — **updated**: tabla de ramas, callout de estado, checklist, sección del contrato cerrado y entrada de bitácora del 2026-09-03. Las entradas viejas de la bitácora **no se tocaron**: eran ciertas cuando se escribieron.
  - `[[Descripción PR — rio-playmaker]]` y `/Users/rjara/pr-1068-body.md` — **updated**, consistentes entre sí por hash.
  - `/Users/rjara/pr-1068-respuestas-david.md` — **updated**: respuestas 3, 6 y 8 rehechas más una extra por los campos nuevos.
  - `80-agents/memory/public/learning/el-context-de-playmaker-es-estructurado-solo-en-el-primer-nivel.md` — **updated**: se le quitó la afirmación de que `last_deployed_version` no se puebla nunca, superada por el contrato, y se le agregó el hecho de que `outputs` es la autoridad.
  - `80-agents/memory/public/known-error/clickhouse-controlplane-plaintext-password-en-output-de-deployment.md` — **updated**: la premisa de que el flag no tiene productor era falsa.

## Motivo

- El estado real estaba dos pasos adelante de lo documentado: las dos ramas **ya estaban pusheadas** y el contrato se había cerrado con `ComponentContext.username` y las versiones como id de `component_definition`. Todo el cierre anterior decía "pendiente: push".
- **Dos afirmaciones propias eran falsas y estaban a punto de llegar al PR.** El flag `sensitive` **sí tiene productor** —`ClickHouseGrantedTableCreator` en `rio-materializer`, sobre valores ya cifrados con KMS, con 48 filas de `service` y 52 de `deployment` en `playmkrprod`—, así que "métrica clavada en 0" era falso; el relevamiento que lo concluyó había **excluido `rio-materializer`** pese a que el propio subagente avisó que quedaba fuera. Y el hallazgo de que `last_deployed_version` no se poblaba nunca quedó superado porque el campo dejó de leer `parameters`.
- Los textos de **DD-7** y **DD-14** ya estaban redactados y aprobados en `/Users/rjara/context-pendiente-documentacion.md`: se incorporaron literales, no reescritos.

## Fuentes usadas

- Código en `rio-playmaker` @ `97065eb17` (dos commits convencionales más el merge, base `develop @ be48d89a9`, 31 archivos `+2333/−54`) y `rio-sdk-events` @ `8932dec` en `feature/component-version-identity`.
- `/Users/rjara/context-pendiente-documentacion.md`, congelado por decisión de rjara y autoritativo.
- Log de un dispatch real del 2026-09-03 11:11 con la versión de prueba.
- Conteos de `playmkrprod` tomados del doc congelado; no se corrió ninguna query en esta sesión.

## Pendiente que quedó identificado

- **No pedir review ni mergear en `97065eb17`:** `createSingle` arma el `EnvironmentModel` sólo con el id, así que ninguna copia importada resuelve valores por el camino de deploy de un solo componente. El árbol de trabajo ya lo arregla con un `resolveEnvironment` del lado del Context.
- El pin del SDK es una versión de prueba y el mensaje de `fe7e8255e` anuncia un `1.5.0` que no existe.
- Las "tres queries acotadas" son tres lecturas **por endpoint importado**; el batching está en curso sin commitear.
- Residuo de javadoc en el SDK: `DeploymentTriggerMessage` menciona un flag de emisión de valores que nunca existió.

## Cierre posterior del PR

- Los dos pendientes de implementación quedaron resueltos en `f49789d2c`: `resolveEnvironment` cubre el camino v1 y los originales, ambientes y service slots de imports se precargan en batch. `origin/feature/new-component-context` coincide con el commit.
- [[Descripción PR — rio-playmaker]] se reescribió contra el head vigente y se publicó como body de [PR #1068](https://github.com/melisource/fury_rio-playmaker/pull/1068). Se retiraron estados intermedios, cifras volátiles y nombres de métodos eliminados.
- Los 12 threads inline de David quedaron respondidos, sin resolverlos en su nombre. El comentario propio C01 se corrigió para retirar la premisa falsa de que todo valor sensible se cifra antes de persistirse.
- Validación local reproducible: `./gradlew test jacocoTestCoverageVerification --rerun-tasks` → 3574 tests, 0 fallas, 0 errores, 2 skipped preexistentes y gate de cobertura PASS. Cinco checks remotos pasaron y el reviewer automático no encontró issues en `f49789d2c`.
- Evidencia de BigQueue: la documentación oficial no publica un hard limit individual, pero desaconseja mensajes sobre 200 KB. El límite de 40 KB corresponde al request agregado de consumidores bulk. Un safety budget futuro debe medir el mensaje completo y omitir el Context entero cuando sea necesario; truncar valores no es una degradación segura.

## Ampliación — safety limit y versión 0.0.6

- El safety budget dejó de ser futuro: `0a23579e9` mide el `DeploymentTriggerMessage` serializado completo antes de publicar y emite `rio.playmaker.context.size` antes de cualquier descarte. Hasta 200 KiB conserva el Context; por encima registra `rio.playmaker.context.discarded{reason:too_large}` y publica sin el campo. Un fallo de medición usa `reason:measurement_failed` y también degrada sin bloquear el deploy. Nunca trunca mapas.
- La evidencia funcional aportada por el owner sitúa el máximo observado en 4–5 KB; se conserva en la respuesta #2 de David sin convertirla en garantía para componentes mayores.
- El flujo de identidad quedó trazado en código: `TigerTokenServiceImpl` valida los headers y retorna `claims.getUsername()`; `PipelineDeployServiceImpl` lo persiste en `PipelineExecution.createdBy`, `DeploymentGroupServiceImpl` lo copia a `DeploymentGroup.createdBy` y `DispatchRequestFactory` lo entrega al Context. No se deriva del group id.
- `feature/new-component-context @ 0a23579e9` y `feature/new-component-context-test @ 9cc84fb06` quedaron pusheadas y al día con `develop @ be48d89a9`. La rama de test preserva su log deliberado sobre el mensaje posterior al guard.
- `fury create-version 0.0.6-component-context-test --confirmed --watch --skip-dirty-check` terminó exitosamente; el tag remoto apunta exactamente a `9cc84fb06`. El bypass sólo ignoró el cambio local ajeno de `Claude.md`, que no entró al build.
- Validación local: 3578 tests, 0 fallas, 0 errores, 2 skipped preexistentes y `jacocoTestCoverageVerification` PASS. Los cinco checks remotos del PR pasaron sobre `0a23579e9`.
- El body remoto del PR y [[Descripción PR — rio-playmaker]] se actualizaron con el guard, sus métricas, la procedencia de `username` y la evidencia vigente. La respuesta #2 ya publicada a David fue editada para describir la implementación efectiva.

## Pendientes vigentes

- Publicar desde `master` el contrato nuevo de `rio-sdk-events` y cambiar el pin `0.0.1-component-version-identity` al semver definitivo.
- Sincronizar SIG-573 y SIG-590 en Spellbook.
- Validar el runtime de `0.0.6-component-context-test`; que la versión haya terminado exitosamente no demuestra el dispatch funcional.

## Validación

- Lint estricto dirigido sobre [[Crear Context]], [[Descripción PR — rio-playmaker]], este change log y el agent run del cierre: sin findings después de completar este registro.
- Rerun completo de Gradle, verificación de head local/remoto, checks del PR y cobertura GraphQL de las respuestas inline.
- El reindex manual de Graphify se intentó y quedó bloqueado por 26 errores y 6 warnings globales ajenos al delta; el índice válido anterior se conservó.

## Rollback

- Restaurar el body anterior desde el historial de edición de GitHub, borrar sólo las respuestas nuevas si fuese necesario y revertir los deltas focales de [[Crear Context]] y [[Descripción PR — rio-playmaker]]. No tocar `f49789d2c`, las ramas ni la versión de prueba: esta sesión no los modificó.
