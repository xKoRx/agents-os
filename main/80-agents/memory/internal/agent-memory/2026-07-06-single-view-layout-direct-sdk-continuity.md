---
type: agent_memory
scope: internal
created: 2026-07-06
updated: 2026-07-06
load_policy: manual
tags:
  - agent/internal
  - project/refactor-polycard
---

# Continuidad — Single View Layout directo en SDK

En la validación del proyecto `[[Single View Layout — Migración al Polycard SDK]]`, se descartó el enfoque inicial de crear `MotorsSingleLayoutDeciderFactory` como API pública del SDK. Aunque movía código fuera de Search, seguía dejando a Search con una customización explícita de layout y agregaba un patrón nuevo.

Estado final recomendado e implementado:

- `java-polycard-sdk`: modificar directamente `SingleNativeAndroidLayoutOrder` y `SingleNativeIosLayoutOrder`, moviendo `LABELS`, `BRAND` y `SELLER` para que queden después de `VISIT_HISTORY` y antes de `LOCATION`.
- `java-polycard-sdk`: ajustar los tests existentes `SingleNativeAndroidLayoutOrderTest` y `SingleNativeIosLayoutOrderTest`; no crear test/factory nuevo.
- `java-polycard-sdk`: versionar como test, no productivo. Versión actual seleccionada: `0.0.2-single-view-layout`; la SDK debe mantenerse responsable solo del orden del layout Single, no de compatibilidad Search.
- `search-middleware`: corregir `SearchApiResponse` para usar `com.mercadolibre.polycard.data.fetcher.deserializer.CommaSeparatedStringToListDeserializer`; no agregar `Item.StringListDeserializer` en la SDK.
- `search-middleware`: bump a `polycardVersion = "0.0.2-single-view-layout"`, borrar `MotorsSingleLayoutDeciderFactory.java`, eliminar los bloques `builder.withLayoutDecider(MotorsSingleLayoutDeciderFactory.create())` en `SearchDecoratorRegistryV1` y `VisDecorationRegistryV1`.
- `SearchDecoratorRegistryV1`: conservar el `webCbtAfterShipping`; ahora envuelve el default decider del SDK, que ya trae el orden Single correcto.

Validación realizada:

- `./gradlew :decorator:compileTestJava` pasó en `java-polycard-sdk`.
- `fury create-version 0.0.1-single-view-layout --skip-dirty-check --confirmed` fue ejecutado en `java-polycard-sdk` y Fury dejó la versión `pending` para commit `85db627ff621`.
- `./gradlew :data-fetcher:test --tests "com.mercadolibre.polycard.data.fetcher.deserializer.CommaSeparatedStringToListDeserializerTest"` pasó.
- `./gradlew :decorator:test --tests "com.mercadolibre.polycard.decorator.layouts.SingleNativeAndroidLayoutOrderTest" --tests "com.mercadolibre.polycard.decorator.layouts.SingleNativeIosLayoutOrderTest"` pasó.
- `fury create-version 0.0.2-single-view-layout --skip-dirty-check --confirmed` fue ejecutado en `java-polycard-sdk` y Fury dejó la versión `FINISHED` para commit `86c5afaac2de`.
- `search-middleware ./gradlew --refresh-dependencies compileJava` pasó con `polycardVersion = "0.0.2-single-view-layout"`.
- `search-middleware ./gradlew test --tests "com.mercadolibre.search.middleware.utils.SearchApiUtilsTest"` pasó.
- `search-middleware ./gradlew test --tests "com.mercadolibre.search.middleware.app.shared.services.polycard.registry.VisDecorationRegistryV1Test"` pasó.
- `search-middleware ./gradlew test --tests "com.mercadolibre.search.middleware.app.shared.services.polycard.registry.SearchDecoratorRegistryV1Test"` pasó al correrlo solo; un intento paralelo previo falló solo por colisión escribiendo XML de resultados.
- `fury create-version 0.0.2-single-view-layout --skip-dirty-check --confirmed` fue ejecutado en `search-middleware` y Fury dejó la versión `CREATING` para commit `70c9f634bd92`.
- Divergencia de ramas corregida después: SDK local trackea `origin/feature/single-view-layout-sdk-migration`, fue rebasado sobre `origin/master` actual y pusheado con `--force-with-lease`. Search también tiene rama remota `origin/feature/single-view-layout-sdk-migration`, rebasada sobre `origin/develop` actual y pusheada.

Pendiente para el próximo agente: no reintroducir el factory salvo que un reviewer del SDK lo pida explícitamente; el criterio del usuario y el pedido de Duvan favorecen el cambio directo en layouts Single. En apps/repos Meli, no usar versiones productivas para PR/test: usar `0.0.x-<descripcion>` y alinear consumidores contra esa versión de test. Próximo paso: monitorear Fury hasta que la versión Search `0.0.2-single-view-layout` pase de `CREATING` a `FINISHED`.

Validación adicional 2026-07-06: en `search-middleware` hay flujos separados para resultados orgánicos y ads/VIS. Orgánico pasa por `GenerateEnhancedSearchNordicHelper#getPolycard` → `DecorationDefinitionFactory` → `SearchDecoratorRegistryV1`; VIS/PADS Lite pasa por `PadsLiteInterventionItemsSupplierTask` → `VisDecorationDefinition` → `VisDecorationRegistryV1` con `VISPadsLiteFeaturesDecider`. En la branch actual solo queda un `withLayoutDecider` local en `SearchDecoratorRegistryV1` para mover `CBT` después de `SHIPPING` en web; no redefine el orden Single de `ATTRIBUTE_LIST`/`LOCATION`. La SDK `0.0.2-single-view-layout` define Single nativo como `ATTRIBUTE_LIST` → `VISIT_HISTORY` → `LABELS` → `BRAND` → `SELLER` → `LOCATION`. Ojo: `VisDecorationDefinition` excluye `ATTRIBUTE_LIST` cuando `polycardSingleMotorsExperiment` está activo, por lo que una diferencia entre orgánico y VIS/PADS en prod puede venir de la definición de componentes/experimento o de versiones desplegadas, no necesariamente de un layout decider local.

Descripción de PR 2026-07-06: se completaron los templates locales `descripcion_pr.md` en `/Users/rjara/fuentes/java-polycard-sdk` y `/Users/rjara/fuentes/search-middleware`. La descripción SDK debe ser agnóstica al consumidor: declarar solo el cambio directo en `SingleNativeAndroidLayoutOrder`/`SingleNativeIosLayoutOrder`, tests de layout y versión test `0.0.2-single-view-layout`, sin mencionar Search/Motors/VIS. La descripción Search declara consumo de esa versión test, eliminación de `MotorsSingleLayoutDeciderFactory` y remoción del decider Single en `SearchDecoratorRegistryV1` y `VisDecorationRegistryV1`. No mencionar el ajuste del deserializador `category_path` en la descripción del PR porque no pertenece al cambio funcional de layout. No se inventaron scopes, curls, capturas, Jira ni Figma.

Investigación 2026-07-06 sobre diferencias orgánico vs VIS/PADS: el SDK ordena recorriendo el `CardLayout` y filtrando contra `polycardComponents`; por tanto, si `LABELS`, `BRAND`, `SELLER`, `LOCATION` están pedidos, la versión `0.0.2-single-view-layout` los ordena como `LABELS -> BRAND -> SELLER -> LOCATION` después de `ATTRIBUTE_LIST/VISIT_HISTORY`. La diferencia real en Search está en las `DecorationDefinition`: orgánico usa `BaseSearchDecorationDefinition` + `NativeSearchDecorationDefinition`, mientras VIS/PADS usa `VisDecorationDefinition`. `c4bb225b9629` (#13447) dejó en VIS/PADS `SELLER`, `BRAND`, `LOCATION`, `LABELS` en una lista distinta y además excluye `ATTRIBUTE_LIST` cuando `isEnabledPolycardSingleMotors` está activo. La razón por la que el cambio original se veía correcto es que `39d72b159c64` (#13239) agregó `MotorsSingleLayoutDeciderFactory` y lo conectó en ambos registries, forzando `LABELS before LOCATION` y `BRAND/SELLER after LABELS`; el commit actual `601e872e626` lo elimina para consumir el layout desde SDK. La lógica 0km de visibilidad no es layout: `39d72b159c64` agregó `MotorsEnhancedBrandDecorator` (oculta brand en Motors Single) y `MotorsEnhancedSellerDecorator` (oculta seller salvo 0km), y `8ee36f9d8ea`/#13210 agregó `MotorsEnhancedLocationDecorator` (oculta location en 0km), luego tocado por `31ef3a828d4`/#14030 para sitios.

Rollback 2026-07-07 en `java-polycard-sdk`: el usuario pidió revertir completamente los cambios DDT/schema y dejar solo el cambio original de layout SDK con changelog, además de quitar el diff accidental de `polycard-data-fetcher/.../Item.java`. Se restauraron los tracked del DDT/schema, se limpiaron los archivos no trackeados agregados para `component_order`/fixtures/schema `labels`, y `Item.java` quedó sin diff contra `origin/master`. Corrección crítica: `0.0.2-single-view-layout` es versión de test y no se documenta en `CHANGELOG.md`; el changelog debe declarar el release productivo `8.186.0`. Commit local actual: `a337f91b20 chore: add single view layout changelog`, con diff contra master limitado a `CHANGELOG.md`, `build.gradle`, layouts Single nativos y sus tests. El push falló por allow list de IP del repo (`186.79.89.172` no permitido); próximo agente debe pushear desde red autorizada o pedir al usuario habilitar/VPN.

Consulta 2026-07-07 sobre Search `SearchApiResponse`: el cambio de `category_path` no pertenece al layout. Search apuntaba a `com.mercadolibre.polycard.data.fetcher.dtos.Item.StringListDeserializer`, clase interna/anidada que ya no existe en la SDK 8.186.0; en SDK el DTO `Item` usa ahora `com.mercadolibre.polycard.data.fetcher.deserializer.CommaSeparatedStringToListDeserializer`. Search necesita cambiar la referencia para seguir compilando y para mantener la deserialización de `category_path` cuando Search API lo entrega como string comma-separated.

Continuidad 2026-07-09: para probar títulos Motors con `polycardVersion = "0.0.1-new-title-motors"`, Search mockea `PolycardSingleMotorsExperimentTask` como `show=true` sin consultar Melidata, manteniendo el gate Motors/native/version. Se agregaron logs `ERROR` de inputs y resultado en ambos resolvers de display mode, el contexto polycard, VIS/PADS y el task del experimento; no se escriben user ID ni d2 ID, solo presencia, para evitar PII. La validación Gradle quedó bloqueada porque esa versión SDK aún no está publicada/disponible en el Maven configurado.
