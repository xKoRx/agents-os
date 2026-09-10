---
type: agent_memory
scope: agent
created: 2026-07-07
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - agent/internal
  - area/meli
  - app/search-middleware
  - app/java-polycard-sdk
  - feature/bajo-de-precio
---

# Bajó de Precio — por qué la pill no se ve (diagnóstico cross-repo)

Sesión 2026-07-07: Rodrigo reporta que la pill "BAJÓ DE PRECIO" (Motors) no
aparece en Search pese a estar mergeado.

## CAUSA RAÍZ VERIFICADA (final — surface iOS nativo)

**Regresión del SDK en el commit `#1630 "fix: Styles to price V2 added"`, release
`8.182.1`.** Rompe el render de la pill de precio en **iOS nativo**.

Datos del usuario que fijan todo: surface = **iOS nativo**; versión que FUNCIONA =
SDK **8.182.0** (search branch `0.0.20-discount-price-motors`); versión que rompe =
la siguiente (develop pinea `8.182.1`). Síntoma: **tachado (`previous_price`) SÍ se
ve, la pill NO**.

Ventana de regresión = 8.182.0 → 8.182.1 = SOLO el commit #1630. Verificado:
- **V1 (`PriceDecorator`, texto "BAJÓ DE PRECIO"): blob byte-idéntico** entre 8.182.0
  y 8.182.1 → no cambió. Como la regresión es real, el item rutea por **PriceV2** en
  iOS (app ≥ 10.524.1). Deducción: NO es V1.
- Pipeline de íconos (`Icon.java`, `NativeIconSizeProvider`, `Icon.fromKey`) inocuo
  para `PRICE_DROPPED` (`fromKey` devuelve null sin throw; `PRICE_DROPPED` no está en
  el mapa iOS de tamaños).
- Culpable: `PriceV2Decorator.appendDiscountPill` agregó estilo **específico iOS** a
  la pill `previous_label`: `s.padding(BoxValue.of(2,2,2,2))` con comentario
  "TEMPORARY: padding workaround for iOS rendering bug". La versión de app iOS
  probada no soporta ese atributo → descarta la pill. El crossed-out es otro
  componente (price amount, no pill) → sobrevive. Calza exacto con el síntoma.

**Mitigación inmediata:** search-middleware quedarse en SDK `8.182.0` (no subir a
8.182.1+). Develop hoy pinea `8.182.1` = el que rompe.
**Fix real (SDK):** revertir/corregir el `padding` iOS de #1630 en
`appendDiscountPill`; el fix definitivo va en el cliente nativo iOS (coordinar).
Aparte: en iOS-V2 la pill es `% OFF`, no el texto "BAJÓ DE PRECIO" (ese es V1-only) —
validar con producto si esperan el texto literal en iOS.

## Lo que NO era el problema (verificado)

- **Search (develop, PR #13976):** gating completo y bien wireado. No es el bug.
- **Desfase de versión / que el label no exista en V2:** hipótesis mías previas,
  DESCARTADAS. El label del feature en V2 es la pill `% OFF`, sí existe; el problema
  es el estilo iOS de #1630, no la ausencia de código.
- **Data/experimentos:** atributo presente y condiciones correctas; el tachado
  renderiza. No es data.

## Fix aplicado (2026-07-07, local, sin VPN)

- **SDK** `java-polycard-sdk`, rama local `fix/ios-pill-padding-price-v2` (base tag `8.182.1`):
  `PriceV2Decorator.appendDiscountPill` — quitado el `s.padding(BoxValue.of(2,2,2,2))` iOS de la
  pill `previous_label` (Android intacto). Test `when_iosPlatform_thenPillPaddingIs2222` reemplazado
  por `when_iosPlatform_thenDiscountPillHasNoPadding` (regression guard). Suite `:decorator:test`
  3894/0/0. Publicado a Maven local: `version = 0.0.1-fix-ios-pill-padding` (`publishToMavenLocal`).
  CHANGELOG actualizado.
- **search-middleware**, rama `feature/bajo-de-precio-motors`: `polycardVersion` 8.182.0 →
  `0.0.1-fix-ios-pill-padding`, agregado `mavenLocal()` a repositories. Compila + 425 tests de
  price-drop en verde contra el SDK local.
- **Confirmación:** contract-level — la salida iOS de la pill queda idéntica a 8.182.0 (known-good que
  Rodrigo validó). Falta confirmación ON-DEVICE (el fallo real es de render del cliente iOS, ningún
  test server-side lo observa). Sin commitear/pushear; pendiente `fury create-version` + backport a
  master cuando vuelva VPN. Decisión abierta: ¿quitar también el padding Android? (no reportado roto).

## Lección para próxima IA

No cerrar causa raíz de un "no se ve" sin la versión exacta buena vs rota y el
surface (web/native + versión de app). La primera hipótesis (config/experimentos) y
la segunda (V2 sin label / desfase de versión) fueron erradas por no anclar esos
datos. La ventana mínima buena→rota + diff del único commit fue lo que lo resolvió.

## Hechos verificados

- **SDK (master):** el texto "BAJÓ DE PRECIO" lo genera 100% el SDK, no Search:
  `PriceDecorator.buildPriceMarkdownDiscountLabel` →
  `context.getI18n().tr("BAJÓ DE PRECIO")` en
  `polycard-decorator/.../decoration/PriceDecorator.java:613`. Se dispara si
  `DetailedPrice.previousPrice() != null` + `hasValidPreviousPriceDrop` (discount
  5-80%) + `priceDropLabelPredicate.test(...)`. NO hay path específico Motors ni
  highlight `PREVIOUS_PRICE` separado; es el path genérico de price-drop.
- **Versión:** el soporte Motors (#1586 "Feature/discount price motors") landeó en
  **8.179.0**. Develop pinea `polycardVersion = "8.182.1"` (build.gradle:57) →
  **ya contiene el soporte**. Descarta el desfase de versión. (Un sub-agente
  recomendó erróneamente subir a 8.186.0 basándose en que #1586 estaba en 8.186.0;
  es falso, #1586 = 8.179.0.)
- **Search (develop, PR #13976 mergeado):** gating completo y bien wireado.
  `PriceDropMotorsExperimentTask` extiende `TrackedExperimentTask` (emite
  exposición), `EXPERIMENT_NAME = "vis/item-dropprice-motors"`, gateada por
  `@TaskDependency(PolycardSingleMotorsExperimentTask.class)`, registrada en los 3
  controllers (SearchController default:447, native:362, MapController:168).
  `PillPriceMarkdownDecoratorFactory` sólo produce un `DecoratorPredicate` booleano
  que alimenta el `priceDropLabelPredicate` del SDK; no construye el texto.

## Cadena de gating runtime (TODO debe ser true a la vez)

1. `SearchBaseExperimentModel.isActive(polycardSingleMotorsExperiment)` — single-view
   Motors activo (gate dependencia). Si single-view-motors está OFF para el segmento,
   la pill nunca aparece.
2. `priceDropMotorsExperiment.show == true` — experimento `vis/item-dropprice-motors`
   enrolado y en variante activa (Growthbook).
3. `hasPriceVariation == true` — `calculateHasPriceDrop`: `salePrice.regularAmount()`
   (= `item.salePrice.previousPrice` de search-api) `>` `salePrice.amount()`. Si
   search-api no trae `previous_price`, o no hay baja real, es false.
4. SDK: discount en rango **5-80%** (`hasValidPreviousPriceDrop`) y `previousPrice != null`.

## Sospechosos ordenados (para próxima IA / debugging)

1. Enrollment de experimentos: `vis/item-dropprice-motors` Y el gate
   `single-view-motors` activos para el user/segment/plataforma de prueba.
2. Data: items Motors de search-api realmente traen `previous_price` con baja ≥5%.
3. Descuento fuera de rango 5-80% → SDK no renderiza aunque el predicado sea true.

Ver [[search-middleware-experiment-tracking]] (exposición) y proyecto
[[Search Middleware - Correccion Bajo de Precio Motors]].

## VPP: doble campo RES en `MaintenanceFeeModel` (2026-07-08)

`applicablePriceDrop` es un residuo semántico de la implementación anterior:
elegía entre `PriceDropRESModel` y `PriceDropMotorsModel` para el margen del
maintenance fee. El CR `3de4ba2111c` eliminó el segundo origen y ambos campos
quedaron asignados al mismo `VisPriceDropRESTask` value. Hoy no existe filtro:
los tests verifican igualdad incluso con `isPriceDrop=false` o experimento
oculto. El único consumidor productivo de `applicablePriceDrop` es el marshaller
de maintenance fee; iOS/Android allí vuelven a evaluar `isPriceDrop && show` para
aplicar `marginTop=16`. `priceDrop` no tiene consumidor productivo en ese modelo.
