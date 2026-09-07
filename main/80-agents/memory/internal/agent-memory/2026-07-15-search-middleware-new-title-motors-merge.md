---
type: known_error
scope: agent
created: 2026-07-15
updated: 2026-07-15
area: "[[Meli]]"
project: "[[Single View Layout — Migración al Polycard SDK]]"
application: "[[search-middleware]]"
entities:
  - "[[search-middleware]]"
  - "[[java-polycard-sdk]]"
related:
  - "[[2026-07-09-search-middleware-sdk-test-artifact-not-published]]"
aliases:
  - legacy overlay label incompatibility
confidence: verified
source_session:
load_policy: when_error_matches
indexable: false
index_priority: high
tags:
  - agent/internal
  - app/search-middleware
  - error/polycard-sdk-compatibility
---

# Search Middleware — overlay label incompatible con SDK de prueba legacy

## Síntoma

- Con `polycardVersion = 0.0.11-new-title-motors`, registrar `OVERLAY_LABEL` en la definición o registry legacy hace fallar la regresión CPG de `PolycardSdkDecoratorTest`.

## Causa

- La versión de prueba contiene el cambio de título Motors, pero no es compatible con la incorporación del overlay label de `develop` en el flujo legacy.

## Mitigación validada

- Mantener overlay labels en el flujo de personalización desacoplado.
- No agregar `OVERLAY_LABEL` a `BaseSearchDecorationDefinition` ni a `SearchDecoratorRegistryV1` legacy mientras se use esa versión de SDK.
- Validar con `./gradlew build` completo.

## Evidencia

- La suite completa pasó con `34680` tests y `44 skipped` luego de aislar el componente legacy.
- Fuente de implementación: `search-middleware`, commit `e64905ed1d5`.

## 2026-07-15 — auditoría PR new-title-motors-single

- El merge `e64905ed1d5` inflaba la comparación contra `develop` a 50 rutas.
- Se reconstruyó el estado contra `develop`, conservando solo la eliminación de
  `subtitle`, el SDK de título corto y sus tests/golden contracts; se restauraron
  `OVERLAY_LABEL`, `PriceDecoratorFactory`, `PadsIntervention*` y comentarios de
  `develop`. `descripcion_pr.md` quedó fuera del índice y sin track.
- Con `PriceDecoratorFactory` de `develop` y SDK `0.0.11-new-title-motors`,
  `compileJava` falla porque el artefacto no expone los métodos de precio de
  `develop`; el artefacto también falla en regresiones de `OVERLAY_LABEL` y
  expectativa de año CORE. La versión SDK debe alinearse antes de exigir suite verde.

## 2026-07-15 — diagnóstico compileJava

- `697cd7fe2a2` cambió las dos rutas legacy de `withDiscountPolylabel(PROMOTIONAL_DISPLAY_LABEL)` a `withDiscountPillAsPolylabel()` + `withPromotionalDisplayLabelAsUnitDescription()`.
- `build.gradle` mantiene `polycardVersion = 0.0.11-new-title-motors`; el JAR resuelto no contiene ninguno de esos dos métodos. Ambos existen desde el cambio de PriceV2 publicado en SDK `8.190.0`.
- Solución preferida: publicar el SDK de título con una nueva versión explícita de prueba (no reutilizar `0.0.11` ni usar una versión productiva) y actualizar Search a esa versión. Workaround compatible: revertir ambas llamadas al supplier viejo, pero se pierde la semántica nueva de PriceV2.

## 2026-07-15 — test suite after SDK 0.0.12

- `./gradlew test` completed `34681` tests with `2 failed`, `44 skipped`; compile passed and no tracked files were altered.
- Both failures are title expectations introduced/changed in Search commit `697cd7fe2a2`: CORE fixtures use domain `CARS_AND_VANS` while `TitleDecorator`'s `versionInTitle=false` contract is domain-based and always composes the vehicle year. The short-title branch does not consult `yearInTitlePredicate`.
- Failing assertions: `SearchVISTitleDecoratorTest.java:295` and `TitleDecoratorFactoryTest.java:238`. Review test fixtures/contract before changing production: use a valid non-Motors domain for CORE cases or restore the Cars & Vans Motors scenario; do not blindly weaken assertions.
- Final resolution in Search: restored the Cars & Vans composite-title expectations in both tests. Full suite then passed: `34681` tests, `44` skipped, BUILD SUCCESSFUL in 4m05s. No production source was changed in this follow-up.

## 2026-07-15 — cierre de code review prep

- El proyecto canónico [[Título Compuesto Motors — Short Version y Dedup]] quedó en Code Review.
- La tarea puente en [[Refactor Polycard]] está en `[r] Review`; no marcarla Done hasta aceptación humana.
- El SDK PR usa `0.0.12-new-title-motors`; la descripción debe hablar solo del diff final: título corto Motors, fallback `SHORT_VERSION/TRIM`, dedup textual, guardrail de 45 caracteres y layouts/contrato intactos.

## 2026-07-15 — corrección de artefacto objetivo

- La descripción solicitada corresponde al PR de `search-middleware`, no al PR del SDK. El archivo correcto es el `descripcion_pr.md` no trackeado de `feature/new-title-motors-single`.
- Su alcance real: habilitación experimental del título corto vía `versionInTitle=false`, eliminación del wiring de `SUBTITLE` en Native/VIS, actualización de tests/snapshots y dependencia `0.0.12-new-title-motors`.

## 2026-07-23 — short title como opción explícita

- El SDK separa `withShortVersionInTitle(...)` de `withVersionInTitle(...)`; el
  nuevo predicado default es `FALSE` y tiene precedencia solo cuando se habilita.
- `withVersionInTitle(FALSE)` vuelve a significar título sin versión, preservando
  consumidores legacy. Search activa el predicado nuevo en sus tres fábricas de
  título cuando el experimento Motors está activo.
- `:decorator:test` pasó. `search-middleware compileJava` llegó a compilar las
  rutas modificadas, pero quedó bloqueado por el error preexistente de
  `FloatHighlightGenericDecoratorBuilder.withPriceDroppedV2(...)` contra el
  artefacto local.

## 2026-07-23 — cobertura de predicados

- Unitarios y DDT cubren el default con versión completa, `withShortVersionInTitle(TRUE)`
  con precedencia sobre `withVersionInTitle`, y `withVersionInTitle(FALSE)` sin short version.
- `./gradlew :decorator:test` y `./gradlew :api:ddtTest` pasaron; los tres escenarios Motors
  nuevos aparecen exitosos en `PolycardV1DataDrivenTest`.
