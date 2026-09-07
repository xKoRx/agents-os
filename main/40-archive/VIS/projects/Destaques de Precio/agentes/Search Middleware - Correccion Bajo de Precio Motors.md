---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Bajó de Precio]]"
sprint: A26Q2S7
start: 2026-07-01
due:
progress: 80
repo: /Users/rjara/fuentes/search-middleware
jira:
prs:
  - https://github.com/melisource/fury_search-middleware/pull/13976
aliases:
  - search middleware bajo de precio motors cleanup
  - limpieza PR bajo de precio motors
  - correccion reglas RE price drop motors
tags:
  - project
  - area/meli
  - application/search-middleware
  - feature/bajo-de-precio
created: "2026-07-01"
updated: "2026-07-01"
---

# Search Middleware - Correccion Bajo de Precio Motors

%% Naming: Search Middleware - Correccion Bajo de Precio Motors es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Search Middleware - Correccion Bajo de Precio Motors
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** A26Q2S7
> **Parent:** [[Bajó de Precio]] · **Aplicación:** [[search-middleware]]

## 🎯 Objetivo

- Corregir el PR de `search-middleware` para que el desarrollo sea estrictamente "Bajó de Precio Motors" sin cambiar reglas históricas de Real Estate.
- Recuperar todas las reglas anteriores de Real Estate, llevarlas a tests y corregir el código hasta que los tests pasen.
- Refactorizar el diseño para seguir el estilo local de helpers: evitar conceptos poco claros como `PriceDropFeatureGate` y revisar si `AbstractPriceDropExperimentTask`/`PriceDropRealEstateExperimentTask` son sobreingeniería.
- Dejar la rama `feature/bajo-de-precio-motors` en un estado fácil de revisar, con diff acotado y semántica preservada.

## 📊 Estado actual

- PR abierto: [#13976 feat(price-drop): Soporte Motors para "Bajó de Precio"](https://github.com/melisource/fury_search-middleware/pull/13976)
- Base: `develop`
- Head: `feature/bajo-de-precio-motors`
- Estado GH al 2026-07-01: `OPEN`, `MERGEABLE`, `REVIEW_REQUIRED`
- Commit remoto actual del PR: `75b4e0f7901bbf6a8c08f3891895eeab5d830aee`
- Commit message actual: `fix(search): clean motors price drop branch`
- Rama local actual: `/Users/rjara/fuentes/search-middleware`, branch `feature/bajo-de-precio-motors`
- La rama ya fue limpiada de commits/archivos ajenos y publicada con `git push --force-with-lease`.
- Diff actual contra `origin/develop`: 35 archivos, 1620 insertions, 745 deletions (histórico, antes del refactor de corrección).
- **2026-07-01 — Refactor de corrección aplicado y validado.** Nuevo diff contra `origin/develop`: 23 archivos, 1079 insertions, 468 deletions — diff más acotado que el original.
- **Estado: `[r]` listo para revisión humana. Cambios en el working tree, sin commitear/pushear — pendiente de tu OK explícito antes de tocar git.**
- Comando de validación completo ejecutado y verde:
  - `./gradlew test` → `BUILD SUCCESSFUL` (suite completa, incluye todos los módulos de test, ~3m16s).
  - Foco previo también verde: `./gradlew test --tests '...PriceDropExperimentHelperTest' --tests '...SearchMetadataDecoratorTest' --tests '...CartDecoratorMediatorTest' --tests '...PriceDecoratorFactoryTest' --tests '...PillPriceMarkdownDecoratorFactoryTest' --tests '...ExperimentsDataTaskTest' --tests '...unit...PriceDropExperimentTaskTest' --tests '...unit...PriceDropMotorsExperimentTaskTest'`.
  - `checkstyleMain`/`pmdMain` no corrieron: `config/checkstyle/checkstyle_rules.xml` no existe en el working tree local — gap preexistente del entorno, no causado por este cambio (confirmado: no aparece en `git status`, no fue tocado).
- Advertencia histórica (ya resuelta): los tests que antes validaban la regresión de RE development fueron corregidos o eliminados; ver Bitácora.

## 🚨 Diagnóstico crítico

- El reporte de GenAI Code Review es correcto: se eliminó una regla histórica importante de Real Estate.
- En `origin/develop`, `PriceDropExperimentHelper.isIndividualRealEstateItem(...)` excluía proyectos inmobiliarios:
  - `REAL_ESTATE`
  - `domainId == null || !domainId.contains("DEVELOPMENT")`
- En el PR actual, `RealEstatePriceDropRule.appliesTo(...)` solo valida `ItemVertical.REAL_ESTATE`, por lo que incluye proyectos `DEVELOPMENT`.
- Ese cambio impacta tres caminos:
  - `SearchMetadataDecorator.decorateUrlFragments`: puede emitir `price_drop=true` en proyectos RE.
  - `CartDecoratorMediator.calculatePriceDropValue`: puede emitir `has_price_drop=true` en proyectos RE.
  - `PriceDecoratorFactory.shouldShowCrossedOutPrice`: puede renderizar precio tachado para proyectos RE.
- Esto no está justificado por el requerimiento. El desarrollo debería agregar Motors, no redefinir Price Drop para Real Estate.

## 🧠 Regla anterior que hay que preservar

Referencia de `origin/develop`:

```java
public static boolean isIndividualRealEstateItem(PolycardItem polycardItem) {
    return nonNull(polycardItem)
            && nonNull(polycardItem.getVertical())
            && ItemVertical.REAL_ESTATE.equals(polycardItem.getVertical())
            && (isNull(polycardItem.getDomainId())
                || !polycardItem.getDomainId().contains(DEVELOPMENT));
}
```

Comportamiento esperado para RE:

- RE individual con `domainId` sin `DEVELOPMENT`: aplica.
- RE con `domainId == null`: aplica, como antes.
- RE proyecto/desarrollo con `domainId` que contiene `DEVELOPMENT`: no aplica.
- Non-RE: no aplica a reglas RE.

## 🧩 Análisis de diseño

### `PriceDropFeatureGate`

- No calza con el estilo local: el repo ya usaba `PriceDropExperimentHelper`.
- El nombre es poco explícito para quienes trabajan en este codebase.
- Mezcla responsabilidades:
  - elegibilidad por vertical,
  - resolución de experimento,
  - decisión de show basada en `hasPriceVariation`.
- Recomendación: eliminar `PriceDropFeatureGate` y mover la lógica a `PriceDropExperimentHelper`, manteniendo nombres explícitos.

### `PriceDropVerticalRule`, `RealEstatePriceDropRule`, `MotorsPriceDropRule`

- Introducen patrón rule/strategy para dos verticales y lógica simple.
- En este repo esa abstracción no parece compensar el costo cognitivo.
- Además escondió la semántica crítica de RE y facilitó la regresión.
- Recomendación: eliminar las clases y reemplazarlas por métodos estáticos explícitos en `PriceDropExperimentHelper`.

### `AbstractPriceDropExperimentTask`

- Centraliza código duplicado entre dos tasks de experimento.
- El costo es que introduce binding implícito por nombre de clase y una `PriceDropRealEstateExperimentTask` nueva para algo que ya existía como `PriceDropExperimentTask`.
- El patrón local era más directo: una task concreta con nombre explícito.
- Recomendación conservadora:
  - Restaurar `PriceDropExperimentTask` como task RE original.
  - Eliminar `PriceDropRealEstateExperimentTask`.
  - Eliminar `AbstractPriceDropExperimentTask`, salvo que el equipo prefiera explícitamente esa abstracción.
  - Agregar `PriceDropMotorsExperimentTask` concreta, aunque duplique algo de código. Para dos tasks, claridad gana.

## ✅ Refactor propuesto

### Modelo

- Restaurar campo RE histórico:
  - `SearchModel.priceDropExperiment`
- Mantener campo Motors:
  - `SearchModel.priceDropMotorsExperiment`
- Evitar `SearchModel.priceDropRealEstateExperiment` si no es estrictamente necesario, porque renombra la semántica existente y agranda el diff.

### Helper

Centralizar en `PriceDropExperimentHelper`:

```java
public static boolean isIndividualRealEstateItem(PolycardItem item)
public static boolean isMotorsItem(PolycardItem item)
public static boolean appliesToPriceDrop(PolycardItem item)
public static boolean isPriceDropExperimentActive(SearchModel model, PolycardItem item)
public static boolean shouldShowPriceDropFeatures(SearchModel model, PolycardItem item, ItemModelBase itemModelBase)
```

Semántica esperada:

- Para RE:
  - aplica solo `isIndividualRealEstateItem(item)`.
  - experimento: `model.priceDropExperiment`.
- Para Motors:
  - aplica si `ItemVertical.MOTORS`.
  - experimento: `model.priceDropMotorsExperiment`.
  - además debe requerir `SearchBaseExperimentModel.isActive(model.polycardSingleMotorsExperiment)`.
- Para ambos:
  - `shouldShowPriceDropFeatures` requiere `hasPriceVariation == true`.

### Callers

- `SearchMetadataDecorator`: usar helper para decidir si se agrega fragment `price_drop`.
- `CartDecoratorMediator`: usar helper para `has_price_drop`.
- `PriceDecoratorFactory`: usar helper para crossed-out price y label.

## 🧪 Tests que hay que recuperar/corregir

### Tests RE obligatorios

- `PriceDropExperimentHelperTest`
  - RE individual aplica.
  - RE `domainId == null` aplica.
  - RE `domainId.contains("DEVELOPMENT")` no aplica.
  - Non-RE no aplica.
  - `shouldShowPriceDropFeatures` false para RE development aunque tenga `hasPriceVariation=true` y experimento activo.
- `SearchMetadataDecoratorTest`
  - RE development no emite `price_drop=true`; comportamiento esperado histórico: no tratarlo como price-drop eligible. Verificar si debe no incluir fragment o quedar `not_apply` según comportamiento anterior en el test existente.
- `CartDecoratorMediatorTest`
  - RE development debe volver a `has_price_drop = "not_apply"` como en `origin/develop`.
- `PriceDecoratorFactoryTest`
  - RE development debe devolver false para `shouldShowCrossedOutPrice`.

### Tests Motors obligatorios

- Motors aplica con:
  - vertical Motors,
  - single view Motors activo,
  - experimento Motors activo,
  - `hasPriceVariation=true`.
- Motors no aplica si:
  - single view Motors apagado,
  - experimento Motors apagado,
  - `hasPriceVariation=false`,
  - item no es Motors.
- Native Motors puede renderizar label `BAJÓ DE PRECIO` si cumple condiciones.
- Web RE debe conservar comportamiento previo.

### Tests actuales sospechosos

Estos tests actualmente codifican la regresión y deben invertirse o eliminarse:

- `src/test/java/com/mercadolibre/search/middleware/app/shared/pricedrop/RealEstatePriceDropRuleTest.java`
  - `givenDevelopmentRealEstate_whenAppliesTo_thenTrue` debe ser false o desaparecer si se elimina la clase.
- `src/test/java/com/mercadolibre/search/middleware/app/shared/services/polycard/decorationdefinition/CartDecoratorMediatorTest.java`
  - `givenRealEstateProjectItem_whenGetTracksWithAction_thenHasPriceDropTrue` debe volver a `not_apply`.
- `src/test/java/com/mercadolibre/search/middleware/app/shared/services/polycard/registry/v1/factories/PriceDecoratorFactoryTest.java`
  - `givenRealEstateProjectItem_whenShouldShowCrossedOutPrice_thenReturnsTrue` debe volver a false.
- `src/test/java/com/mercadolibre/search/middleware/app/shared/pricedrop/PriceDropFeatureGateTest.java`
  - probablemente eliminar junto con `PriceDropFeatureGate`.

## 📁 Archivos relevantes actuales del PR

### Clases productivas principales

- `build.gradle`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/pricedrop/MotorsPriceDropRule.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/pricedrop/PriceDropFeatureGate.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/pricedrop/PriceDropVerticalRule.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/pricedrop/RealEstatePriceDropRule.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/services/polycard/SearchMetadataDecorator.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/services/polycard/decorationdefinition/CartDecoratorMediator.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/services/polycard/registry/v1/factories/PriceDecoratorFactory.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/tasks/AbstractPriceDropExperimentTask.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/tasks/ExperimentsDataTask.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/tasks/PriceDropExperimentTask.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/tasks/PriceDropMotorsExperimentTask.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/tasks/PriceDropRealEstateExperimentTask.java`
- `src/main/java/com/mercadolibre/search/middleware/app/shared/utils/PriceDropExperimentHelper.java`
- `src/main/java/com/mercadolibre/search/middleware/app/versioned/_default/_native/v00_01/controllers/SearchController.java`
- `src/main/java/com/mercadolibre/search/middleware/app/versioned/_default/v00_01/controllers/MapController.java`
- `src/main/java/com/mercadolibre/search/middleware/app/versioned/_default/v00_01/controllers/SearchController.java`
- `src/main/java/com/mercadolibre/search/middleware/app/versioned/_default/v00_01/model/SearchModel.java`

### Tests principales

- `src/test/java/com/mercadolibre/search/middleware/app/shared/pricedrop/MotorsPriceDropRuleTest.java`
- `src/test/java/com/mercadolibre/search/middleware/app/shared/pricedrop/PriceDropFeatureGateTest.java`
- `src/test/java/com/mercadolibre/search/middleware/app/shared/pricedrop/RealEstatePriceDropRuleTest.java`
- `src/test/java/com/mercadolibre/search/middleware/app/shared/services/polycard/SearchMetadataDecoratorTest.java`
- `src/test/java/com/mercadolibre/search/middleware/app/shared/services/polycard/decorationdefinition/CartDecoratorMediatorTest.java`
- `src/test/java/com/mercadolibre/search/middleware/app/shared/services/polycard/registry/v1/factories/PriceDecoratorFactoryTest.java`
- `src/test/java/com/mercadolibre/search/middleware/app/shared/utils/PriceDropExperimentHelperTest.java`
- `src/test/java/com/mercadolibre/search/middleware/unit/app/shared/tasks/PriceDropMotorsExperimentTaskTest.java`
- `src/test/java/com/mercadolibre/search/middleware/unit/app/shared/tasks/PriceDropRealEstateExperimentTaskTest.java`

## 🧪 Comandos de validación recomendados

Primero correr tests focalizados:

```bash
/usr/bin/env JAVA_HOME=/Users/rjara/Library/Java/JavaVirtualMachines/corretto-17.0.14/Contents/Home PATH=/Users/rjara/Library/Java/JavaVirtualMachines/corretto-17.0.14/Contents/Home/bin:$PATH ./gradlew test \
  --tests 'com.mercadolibre.search.middleware.app.shared.utils.PriceDropExperimentHelperTest' \
  --tests 'com.mercadolibre.search.middleware.app.shared.services.polycard.SearchMetadataDecoratorTest' \
  --tests 'com.mercadolibre.search.middleware.app.shared.services.polycard.decorationdefinition.CartDecoratorMediatorTest' \
  --tests 'com.mercadolibre.search.middleware.app.shared.services.polycard.registry.v1.factories.PriceDecoratorFactoryTest' \
  --tests 'com.mercadolibre.search.middleware.app.shared.tasks.ExperimentsDataTaskTest' \
  --tests 'com.mercadolibre.search.middleware.app.shared.tasks.PriceV2SearchDecorateExperimentTaskTest' \
  --tests 'com.mercadolibre.search.middleware.unit.app.shared.tasks.PriceDropMotorsExperimentTaskTest'
```

Luego, si pasa, considerar:

```bash
/usr/bin/env JAVA_HOME=/Users/rjara/Library/Java/JavaVirtualMachines/corretto-17.0.14/Contents/Home PATH=/Users/rjara/Library/Java/JavaVirtualMachines/corretto-17.0.14/Contents/Home/bin:$PATH ./gradlew test
```

## 🧾 Referencias de repo y versiones

- Repo local: `/Users/rjara/fuentes/search-middleware`
- PR: `https://github.com/melisource/fury_search-middleware/pull/13976`
- Branch: `feature/bajo-de-precio-motors`
- Commit limpio actual: `75b4e0f7901bbf6a8c08f3891895eeab5d830aee`
- Base remota actual usada: `origin/develop` en `5c322d083b8`
- SDK Polycard actual: `polycardVersion = "8.179.0"`
- `0.0.14-discount-price-motors` existía como tag, pero no resolvía Maven/Fury.
- `fury list-versions --limit 40` en `/Users/rjara/fuentes/java-polycard-sdk` mostró `8.179.0` como última versión `FINISHED` de master y `0.0.12-discount-price-motors` como última versión branch publicada de la línea experimental.

## ⚠️ Riesgos operativos

- No volver a hacer merge/copiar árbol completo desde `feature/bajo-de-precio-motors-test`; esa fue la fuente de contaminación inicial.
- Si se requiere reescribir la rama remota, usar solo `git push --force-with-lease`.
- Hay un backup local del estado ruidoso:
  - `backup/bajo-de-precio-motors-noisy-20260630-fix`
- Hay un branch local limpio auxiliar:
  - `feature/bajo-de-precio-motors-clean`
- En el repo hay untracked previos no relacionados; no tocarlos:
  - `.agents/`
  - `AGENTS.md`
  - `descripcion_pr.md`
  - `graphify-out/`
  - `previous-price/`

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!note]+ Convención de ownership
> Usa `#owner/me` para tareas humanas y `#owner/agent` para tareas de agentes.
> Si una tarea no tiene owner, queda visible abajo para corregirla.

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function render(tasks){
  const el=dv.el('div','');
  el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");
}
function owned(tasks, owner){return tasks.filter(t=>new RegExp(`(^|\\s)#owner/${owner}(\\s|$)`).test(String(t.text)));}
const tasks=dv.current().file.tasks.array().sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));
const mine=owned(tasks,"me");
const agent=owned(tasks,"agent");
const loose=tasks.filter(t=>!new RegExp(`(^|\\s)#owner/(me|agent)(\\s|$)`).test(String(t.text)));

dv.header(3,"🧍 Tareas mías");
mine.length ? render(mine) : dv.paragraph("_Sin tareas mías._");

dv.header(3,"🤖 Tareas de agentes");
agent.length ? render(agent) : dv.paragraph("_Sin tareas de agentes._");

dv.header(3,"🧺 Sin owner");
loose.length ? render(loose) : dv.paragraph("_Sin tareas sin owner._");
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [x] Restaurar semántica RE individual: `DEVELOPMENT` no aplica a price drop #owner/agent #type/dev #area/meli #urgent
> - [x] Mover lógica de elegibilidad/experimento a `PriceDropExperimentHelper` y eliminar `PriceDropFeatureGate` #owner/agent #type/dev #area/meli
> - [x] Evaluar y probablemente eliminar `AbstractPriceDropExperimentTask` + `PriceDropRealEstateExperimentTask` #owner/agent #type/dev #area/meli
> - [x] Ajustar tests que hoy validan la regresión de RE development #owner/agent #type/dev #area/meli #urgent
> - [x] Correr tests focalizados y registrar comando exacto en PR #owner/agent #type/dev #area/meli
> - [x] Revertir código de diagnóstico ajeno (LOGGER sin uso, wiring de `isElegibleItemToPricingV2Decorator`) heredado del commit `test(search): add motors price drop diagnostics`, sin relación con Bajo de Precio Motors #owner/agent #type/dev #area/meli
> - [ ] Revisar diff final para mantenerlo acotado y responder GenAI Code Review #owner/me #type/pr-review #area/meli
> - [ ] Decidir commit/push de la corrección (branch `feature/bajo-de-precio-motors`) #owner/me #type/dev #area/meli #urgent

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes Search Middleware - Correccion Bajo de Precio Motors
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes Search Middleware - Correccion Bajo de Precio Motors
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes Search Middleware - Correccion Bajo de Precio Motors
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes Search Middleware - Correccion Bajo de Precio Motors
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-07-01** — Se crea subproyecto de corrección/handoff. Análisis confirma regresión: proyectos Real Estate `DEVELOPMENT` pasaron a ser elegibles para price drop, lo que contradice la regla anterior. Se recomienda refactor a helper y eliminar abstracciones innecesarias.
- **2026-07-01** — Inicio de implementación. Hallazgo clave: `PriceDropExperimentTask.java` (el original de `develop`, con `EXPERIMENT_NAME = "vis/item-dropprice-res"`) sigue existiendo intacto en el repo, sin usar y sin wiring — quien creó la rama Motors nunca lo borró ni lo reconectó, solo agregó `PriceDropRealEstateExperimentTask`/`AbstractPriceDropExperimentTask` en paralelo. El repo compila hoy (`compileJava`/`compileTestJava` verdes) porque esa clase orfana no choca con nada. Esto simplifica el fix: no hay que "restaurar" la task RE, solo re-conectarla y borrar el duplicado. Diseño de fix confirmado comparando `origin/develop` línea a línea contra la rama: `PriceDropExperimentHelper` unificado con `isIndividualRealEstateItem`/`isMotorsItem`/`appliesToPriceDrop`/`isPriceDropExperimentActive(model, item)`/`shouldShowPriceDropFeatures`. Detalle importante de diseño: `SearchMetadataDecorator` y `CartDecoratorMediator` deben usar el gate **narrow** (`appliesToPriceDrop`) directamente — así un item RE `DEVELOPMENT` no entra a la rama y cae a `not_apply`/ausencia de fragment, igual que en `develop`. `PriceDecoratorFactory.shouldShowCrossedOutPrice` en cambio mantiene su propio gate **broad** local (`isRealEstate` sin narrowing) seguido de narrowing interno vía `shouldShowPriceDropFeatures` — ese patrón de dos pasos ya existía en `develop` y hay que preservarlo intacto, no unificarlo con el gate narrow o se rompe la semántica (un item RE `DEVELOPMENT` que no aplica a price drop debe devolver `false` en crossed-out-price, no `true`).
- **2026-07-01** — Refactor de corrección aplicado y validado completo. Cambios:
  - `SearchModel.priceDropRealEstateExperiment` → `priceDropExperiment` (nombre histórico de `develop` restaurado; `priceDropMotorsExperiment` intacto).
  - `PriceDropExperimentHelper` reescrito: `isIndividualRealEstateItem` (idéntico a `develop`, con exclusión `DEVELOPMENT`), `isMotorsItem`, `appliesToPriceDrop`, `isPriceDropExperimentActive(model, item)` (ahora item-aware: RE depende solo de su experimento; Motors requiere además `SearchBaseExperimentModel.isActive(polycardSingleMotorsExperiment)`), `shouldShowPriceDropFeatures`, `calculateHasPriceDrop` (sin cambios).
  - Eliminados: `PriceDropFeatureGate`, `PriceDropVerticalRule`, `RealEstatePriceDropRule`, `MotorsPriceDropRule`, `AbstractPriceDropExperimentTask`, `PriceDropRealEstateExperimentTask` (y sus tests).
  - `PriceDropMotorsExperimentTask` reescrita concreta (sin heredar de Abstract), duplicando lo mínimo — misma API pública, tests originales sin tocar y verdes.
  - `PriceDropExperimentTask` (RE, original de `develop`) reconectada en `ExperimentsDataTask` + los 3 controllers (`SearchController` native, `SearchController` default, `MapController`), reemplazando `PriceDropRealEstateExperimentTask`.
  - Callers migrados a `PriceDropExperimentHelper`: `SearchMetadataDecorator` (gate narrow), `CartDecoratorMediator` (gate narrow), `PriceDecoratorFactory` (gate broad local preservado + narrowing interno), `PillPriceMarkdownDecoratorFactory` (delegación directa).
  - Tests corregidos para reflejar el comportamiento correcto (ya no la regresión): `CartDecoratorMediatorTest.givenRealEstateProjectItem_whenGetTracksWithAction_thenHasPriceDropNotApply` (antes `...thenHasPriceDropTrue`, ahora asserta `"not_apply"`); `PriceDecoratorFactoryTest.givenRealEstateProjectItem_whenShouldShowCrossedOutPrice_thenReturnsFalse` (antes `...thenReturnsTrue`, ahora asserta `false`). `PriceDropExperimentHelperTest` reescrito completo: suite RE de `develop` + suite nueva de Motors (single-view gating, independencia entre verticales, `appliesToPriceDrop`).
  - Validación: `./gradlew compileJava compileTestJava` verde; tests focalizados verdes; **`./gradlew test` (suite completa) → `BUILD SUCCESSFUL`**. `checkstyleMain`/`pmdMain` no corrieron por falta de `config/checkstyle/checkstyle_rules.xml` en el entorno local (gap preexistente, no introducido por este cambio).
  - Diff final contra `origin/develop`: 23 archivos, 1079 insertions, 468 deletions (antes: 35 archivos, 1620/745) — diff más acotado, como pedía el objetivo del subproyecto.
  - **Sin commitear ni pushear.** Cambios viven en el working tree de `/Users/rjara/fuentes/search-middleware`, branch `feature/bajo-de-precio-motors`. Pendiente de tu OK explícito para `git add`/`commit`/`push --force-with-lease` — no se toca git sin confirmación.
- **2026-07-01 (sesión 2) — Limpieza de código de diagnóstico ajeno detectada por el humano.** Al revisar el diff, detectaste ruido no relacionado con Bajo de Precio Motors en `PriceDecoratorFactory.java` (variables locales sin propósito en `shouldUsePriceV2Decorator`/`isElegibleItemToPricingV2Decorator`) y `SearchDecoratorRegistryV1.java` (un `LOGGER` nunca usado + wiring nuevo de `isElegibleItemToPricingV2Decorator` en el fallback de Price V2). Investigación con `git log -S` confirmó el origen: commit `5996a3af99f4` "test(search): add motors price drop diagnostics" (17-jun-2026), código exploratorio de un área completamente distinta (Price V2 / consumer credits decorator) que sobrevivió intacto a la reconstrucción de rama del 30-jun y a la corrección del 01-jul porque estaba fuera del alcance de esa corrección (RE/Motors price-drop). Revertido a paridad exacta con `origin/develop` en ambos archivos productivos + en `SearchDecoratorRegistryV1Test.java` (traía un test nuevo y un bump de versión gratuito del mismo commit de diagnóstico). `SearchDecoratorRegistryV1.java` terminó sin ningún diff contra `origin/develop` — no tenía cambios reales del feature, solo ese diagnóstico. Diff final actualizado: 22 archivos, 1042 insertions, 465 deletions. Validado: tests focalizados verdes + `./gradlew test` completo → `BUILD SUCCESSFUL` (4m59s). Sigue sin commitear/pushear, pendiente de tu OK.

## 🧭 Decisiones

- Este subproyecto debe preservar comportamiento histórico de Real Estate y limitar el alcance funcional nuevo a Motors.
- Preferir helper explícito (`PriceDropExperimentHelper`) sobre `PriceDropFeatureGate`/rules para alinear con patrones locales del repo.
- Preferir claridad sobre abstracción en tasks; duplicación menor entre dos experiments es aceptable si evita binding implícito y renombres innecesarios.
- Cualquier código sin relación directa con Bajo de Precio Motors detectado en el diff (aunque preexistiera en la rama) se revierte a paridad con `origin/develop`, no se "adopta" ni se justifica retroactivamente — el diff debe reflejar solo el delta funcional real.

## 🔗 Docs / Links

- PR search-middleware: https://github.com/melisource/fury_search-middleware/pull/13976
- Proyecto padre: [[Bajó de Precio]]
- App: [[search-middleware]]
- Aprendizaje de ramas limpias: [[Reconstruir Ramas De PR Sin Arrastrar Commits Ajenos]]
- Spec Técnica Search: `file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/VMDUPPER-tecnica-bajo-de-precio-search.md`
- Spec Técnica VIP: `file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/VISMDMID-tecnica-bajo-de-precio-vip.md`

## 💡 Ideas

### Backlog de ideas

- Considerar dejar un comment en PR explicando que la corrección no cambia RE y que Motors queda gobernado por su experimento más single-view.
- Si el equipo insiste en abstraer reglas por vertical, exigir tests de no-regresión para cada vertical preexistente antes de aceptar.

### Motivos / principios

- Agregar una vertical nueva no debe relajar restricciones históricas de otra vertical.
- Tests de refactor deben preservar semántica anterior antes de probar comportamiento nuevo.

### Memoria pública / interna

- **Memoria pública:** aprendizaje de evitar arrastre de commits y aprendizaje de preservar semántica legacy al extender features multi-verticales.
- **Memoria interna:** continuidad operativa de esta sesión y advertencia para próximos agentes.
- **Motivo:** próxima IA debe poder seguir con menos contexto y evitar repetir el mismo tipo de regresión.
