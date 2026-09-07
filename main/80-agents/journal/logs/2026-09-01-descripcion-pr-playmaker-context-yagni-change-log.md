---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Crear Context]]"
  - "[[Descripción PR — rio-playmaker]]"
  - "[[rio-playmaker]]"
  - "[[pr-description]]"
tags:
  - kind/doc
  - project/crear-context
  - application/rio-playmaker
created: "2026-09-01"
updated: "2026-09-01"
---

# change_log — Descripción PR #1068 reescrita de cero (Playmaker, Context opcional)

**Qué se hizo.** Se reescribió desde cero [[Descripción PR — rio-playmaker]] contra el código del worktree `/Users/rjara/rio-playmaker-context-yagni` (rama `feature/new-component-context`, base `develop @ fe899d5a4`). No se creó, abrió, editó ni comenteó el PR en GitHub, y no se modificó ni commiteó nada del worktree.

**Por qué.** El cuerpo remoto de #1068 y la versión anterior de la nota describían una implementación que ya no existe. Cuatro afirmaciones falsas retiradas: validación de contrato del SDK antes de publicar; acceso cross-data-product con autorización aprobada ligando el par `(copia, original)`; equivalencia de ambientes con `EnvironmentType` y normalización de `Test`/`Sandbox` a `Staging`; y Context obligatorio con falla de derivación que falla el deployment. Ninguna frase de la versión anterior se heredó.

**Evidencia recogida en la sesión.** Template `.github/pull_request_template.md` (5 secciones: `Description`, `Dev checklist`, `Code Review checklist`, `How Has This Been Tested?`, `Issue`). Diff vs base: 25 archivos, +1563/−54. Diff HEAD vs working tree: 21 archivos, +173/−1350. `build/test-results/test`: 330 XML, 3422 tests, 0 fallas, 0 errores, 2 skipped preexistentes (`TopologicalSortServiceImplTest`), corrida del 2026-09-01 15:53. `rio-sdk-events-1.4.0.jar` inspeccionado con `javap`: `DeploymentSchemaVersion.CURRENT = 1` y `DeploymentTriggerMessage` con constructor legacy de 14 args más el de 15 con `ComponentContext`. `gh pr checks 1068`: 5 PASS y `Code Reviewer` en `skipping`, todos sobre `3c788a390`.

**Bloqueantes levantados.** (1) El estado descrito no está commiteado ni pusheado; el PR muestra la versión anterior. (2) Los checks remotos verdes no cubren el código descrito. (3) Commits intermedios no convencionales, corresponde squash merge. No bloqueantes: sincronizar SIG-573 y SIG-590 en Spellbook, y validar en preproducción. El diff ajeno de `docs/specs/swagger.yaml` ya está resuelto.

**Referencias cerradas.** Estado, tabla de branches y checklist de [[Crear Context]] corregidos: la nota afirmaba con fecha 2026-09-01 que el Context era obligatorio por componente, lo que describe `9b35ce7e6`, revertido en el working tree. Bitácora del proyecto con entrada del 2026-09-01 (2).

**Tensión registrada.** El cuerpo va en español por instrucción explícita del owner del 2026-08-26, contra el idioma del template (inglés) y contra el `CODING_GUIDELINES.md` del repo, que exige inglés para toda contribución.

---

## Corrección — misma sesión, después de la reescritura de la branch

**Datos que cambiaron.** La branch se rehizo: **un único commit convencional** `07ffc382a` rebasado sobre `develop @ 1f3e741b0`. Los nueve commits intermedios y el commit que hacía el Context obligatorio ya no existen. El working tree quedó limpio, `docs/specs/swagger.yaml` no aparece en el diff, y la suite subió a **3433 tests** (0 fallas, 0 errores, 2 skipped preexistentes) porque el rebase trajo tests de develop. Diff estable en 25 archivos, +1563/−54. Conteos por clase sin cambios.

**Cambio de fondo.** Por instrucción del owner —la descripción tiene que estar "sin usar como base ningún documento, descrito solo con lo nuevo"— la sección `Descripción` se reescribió autocontenida, partiendo del cambio mismo y no de la sección "Problema" del funcional. Se conservó el árbol ASCII del contrato.

**Cuatro agregados.** (1) Bloque titulado **"Lo que no cambia"** consolidando los cinco no-cambios de riesgo, que antes estaban dispersos en prosa. (2) Que el **snapshot envejece y nadie lo refresca**: se calcula en el dispatch, no se persiste, y un consumidor no debe asumir vigencia — distinto del boundary transaccional, que es dónde se deriva. (3) Que la **prohibición de loguear cruza el boundary hacia el consumidor**: verificado textualmente en `ComponentContext.java:22` del SDK, "Consumers MUST NOT log this context or any input or output value at any level"; ningún CP tiene hoy regla propia y el contrato no cifra ninguno de los dos mapas. (4) El **caveat de evidencia dentro del cuerpo del PR**, no sólo en las notas internas.

**Checklist.** Conventional commits pasa a `[x]`; se borraron las notas de squash merge y de commits intermedios no convencionales. "Actualicé la branch con develop" sigue `[x]` y ahora es literal: está rebasada sobre el tip.

**Bloqueantes al cierre.** Queda uno: falta **force-push**. `origin/feature/new-component-context` sigue en `3c788a390`, así que el PR muestra el historial viejo y los 5 checks remotos en PASS corresponden a ese código. Los dos bloqueantes anteriores —trabajo sin commitear y commits no convencionales— quedaron resueltos por la reescritura.

---

## Segunda corrección — dos cambios de código en la rama

**Datos.** Commit `15ddcc757` (amend, sigue siendo un único commit convencional sobre `develop @ 1f3e741b0`). Diff 25 archivos, **+1649/−54**. Suite **3435 tests**, 0 fallas, 0 errores, 2 skipped preexistentes. Worktree limpio.

**Guard de ambiente (nuevo en la descripción).** `Component.last_deployed_version` se omite cuando el último deployment completado pertenece a un ambiente distinto del que se despliega, contado como `env_mismatch`. La causa raíz: `BatchDispatchServiceImpl.resolveService`, con `entry.serviceId()` no null, resuelve por id vía `loadServicesById` → `findAllById`, **sin filtro de ambiente**. `hasEnvironmentMismatch` es conservador: sólo declara mismatch cuando los dos ids están presentes y difieren.

**Semántica de `unresolved`.** `ContextValueResolver.resolve` ya **no** cuenta supresión cuando el documento es null o blank; sólo cuando el root no es objeto JSON o el parseo lanza, más el caso de versión ausente en `resolveLastDeployedVersion`. Motivo: el resolver se invoca dos veces por entidad, así que un vecino sin datos emitía dos `unresolved` y eso volvía el contador inalertable. La métrica pasa a tres razones: `no_slot`, `unresolved`, `env_mismatch`.

**`inputs` pre-resolución.** Verificado: `params` pasa por `parameterResolutionService.resolveComponentParameters(...)` y `ParameterParseServiceImpl` expande `${(dp.)?componente(\[env\])?.propiedad}`; el Context lee `component_definition.parameters` crudo. Un consumidor puede recibir `${kafka_topic.topic_name}` literal en `RelatedComponent.inputs` y el valor expandido en `params`. Documentado en la descripción de los dos mapas y en la guía de revisión, como semántica elegida y pregunta abierta para el primer CP que adopte el campo.

**Dato corregido contra la evidencia.** Llegó como dato que `ContextValueResolverTest` subía de 9 a 11 casos. Es **9**: 9 `@Test` en el fuente y 9 en `TEST-...ContextValueResolverTest.xml`. El delta total 3433 → 3435 lo explican íntegramente los 23 → 25 de `ComponentContextServiceTest`; con las dos subiendo el total sería 3437. Escrito 9 en la descripción y anotado en las notas internas.

**Bloqueante al cierre.** Sigue faltando el **force-push**: `origin/feature/new-component-context` está en `3c788a390`.

---

## Tercera corrección — `ed23aa76a`, acortar y limpiar

**Estado.** 27 archivos, **+2238/−54**. Suite **3451 tests**, 0 fallas, 0 errores, 2 skipped preexistentes (331 XML). Conteos verificados: `ComponentContextServiceTest` 34, `ContextValueResolverTest` 9, `ContextValueResolverLoggingTest` 4, `ContextMetricsTest` 3, `BigQueueDispatchAdapterTest` 7, `BatchDispatchServiceImplTest` 20, `ParameterParseServiceImplTest` 42, `DeploymentOrchestrationIntegrationTest` 4. `ComponentContextService` pasó a 452 líneas y ocho dependencias.

**Principio ordenador (owner).** "La misma data con `params` y contexto, pero en el contexto la data está estructurada y tiene sentido; no es una bolsa de gatos como `params`." Es la tesis de la descripción; todo lo que no la sirva sobra.

**Cambios de código reflejados.** (1) Los `inputs` se resuelven con `ParameterResolutionService.resolveComponentParameters(...)`, el mismo servicio que resuelve `params`: se borró el párrafo de "pre-resolución" y su punto de la guía. (2) Vecinos importados: `resolveSlot` sigue `sourceComponentId` hasta el original vía `componentRepository.findById`, resuelve el ambiente por nombre con fallback a `EnvironmentType.normalize` y desempate por menor id, y lee sus valores; publica `id`/`name`/`type` de la copia. Sin autorización. Se borró el bullet de "sin camino cross-data-product", que era incorrecto. (3) Métrica `rio.playmaker.context.size`, histograma en bytes emitido en el adapter una vez por contexto publicado.

**Error propio corregido.** Una copia importada vive **dentro** del data product que importa; lo que apunta afuera es `sourceComponentId`. Las pasadas anteriores lo tenían al revés. Un vecino de otro data product sin `sourceComponentId` sí degrada a mapas vacíos.

**Poda.** Fuera: toda mención de logging y el punto que le pasaba la obligación al consumidor citando un javadoc propio; el párrafo del snapshot que envejece; "verbatim"; la explicación de la semántica de `unresolved`; "por qué los dos mapas salen del mismo slot"; "por qué hace falta un guard de ambiente"; y el caveat de evidencia. La guía de revisión quedó en cuatro puntos: nullable/best effort, `deploy_completed` exacto, importado sin gate, y boundary transaccional.

**Diagrama.** Mermaid `flowchart TD` del flujo de dispatch, con `classDef nuevo` / `classDef existente`, leyenda y subgraphs con `fill:none` para que funcione en tema claro y oscuro. Validado con `mermaid@11` en navegador: `mermaid.parse` devuelve `flowchart-v2` y `mermaid.render` produce SVG de ~75 KB; revisado visualmente por screenshot.

**Decisión que queda expuesta al owner.** `ContextValueResolverLoggingTest` (4 casos) se mantuvo nombrado en "¿Cómo se probó?" porque es uno de los 27 archivos del diff y un reviewer lo va a ver igual. Es la única mención de logging que sobrevive, y es inventario, no advertencia.

**Bloqueante al cierre.** Sigue faltando el **force-push**: `origin/feature/new-component-context` está en `3c788a390`.
