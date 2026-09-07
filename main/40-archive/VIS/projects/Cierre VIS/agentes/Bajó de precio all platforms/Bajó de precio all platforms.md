---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Cierre VIS]]"
sprint:
start: 2026-07-29
due:
progress: 90
repo: search-middleware
jira: VMDEM-21
prs:
aliases:
  - Price Variation All Platforms
  - Bajó de Precio all platforms
tags:
  - project
  - area/meli
  - app/search-middleware
  - feature/destaques-de-precio
created: 2026-07-29
updated: 2026-07-29
---

# Bajó de precio all platforms

%% Naming: Bajó de precio all platforms es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Bajó de precio all platforms
> **Padre:** [[Cierre VIS]] · **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1
> Extender "Bajó de Precio" de Motors a Desktop y WebMobile en `search-middleware`, delegando la audiencia por plataforma al experimento `vis/item-dropprice-motors`. **Sin cambios en el SDK Polycard.**

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente.

## 🎯 Objetivo

- Mostrar el label "BAJÓ DE PRECIO" y el precio tachado gobernado por experimento para ítems **Motors** también en **Desktop** y **WebMobile** (hoy solo funciona en nativo).
- Que la audiencia por plataforma la controle **Fury Experiments** (`vis/item-dropprice-motors`), no el código: activar/desactivar web sin deploy.
- No regresionar el comportamiento vigente de **Real Estate** (label web y tachado) ni el de **Motors nativo**.

## 📊 Estado actual

- **Reevaluación técnica cerrada (2026-07-29).** El spec adjunto es **correcto y suficiente para el rollout actual**; se verificó línea a línea contra `origin/develop`. Ver sección **🔬 Reevaluación** más abajo.
- **Pregunta del SDK resuelta: NO se toca `java-polycard-sdk`.** Los predicados `withPriceDropLabel` y `withCrossedOutPrice` ya existen en Polycard SDK `8.198.0` (versión actual en develop) y ya se consumen en `search-middleware`. Extender a Motors web es solo cambiar booleanos en el middleware. La hipótesis inicial de impactar Polycard SDK queda **descartada**.
- Rama `feature/VMDEM-21-price-drop-all-platforms` creada desde `develop`; los cuatro gates productivos y las pruebas focalizadas ya están implementados.
- Validación focalizada y `CartDecoratorMediatorTest` en verde. La suite completa ejecutó 35.219 tests: 13 fallas preexistentes de `SearchShopsAdsServiceTest` por `NoSuchMethodError` de `Platform.getSearchShopsAdsConfig()`; ninguna corresponde al cambio.
- `checkstyleMain` también falla por violaciones preexistentes distribuidas en el repositorio; no reportó los archivos modificados del feature.
- Working tree listo para revisión; sin commit ni push.
- **Rama deprecada detectada y descartada:** `feature/price-variation-all-platforms-motors` (262 archivos, baja Polycard 8.198→8.194, toca highlights/shipping/title/ads sin relación). **NO usarla, NO mergearla, NO copiar su árbol.** Arrancar desde `develop` limpio.

## 🔬 Reevaluación (evidencia contra `origin/develop`)

> Repo local: `/Users/rjara/fuentes/search-middleware` · base: `develop` · Polycard SDK: `8.198.0`.

### Diagnóstico: dónde está bloqueado Motors en web hoy

Motors "bajó de precio" está atado a nativo por **cuatro** gates. Los cuatro se verificaron presentes en el código actual:

| # | Archivo | Método | Estado hoy | Por qué bloquea web |
|---|---------|--------|-----------|---------------------|
| 1 | `app/shared/tasks/PriceDropMotorsExperimentTask.java` | `isExperimentApplicable()` | Depende de `PolycardSingleMotorsExperimentTask` (`@TaskDependency`) | `polycardSingleMotors` es nativo-only → la task no evalúa en web |
| 2 | `app/shared/utils/PriceDropExperimentHelper.java` | `isPriceDropExperimentActive()` | Rama Motors exige `SearchBaseExperimentModel.isActive(model.polycardSingleMotorsExperiment)` **además** de `priceDropMotorsExperiment.show` | mismo gate nativo-only encadenado |
| 3 | `app/shared/services/polycard/registry/v1/factories/PriceDecoratorFactory.java` | `shouldShowPriceDropLabel()` (línea ~185) | Rama `!device.isNative()` retorna **solo** `isRealEstate(item)` | web nunca considera Motors para el label |
| 4 | `app/shared/services/polycard/registry/v1/factories/PriceDecoratorFactory.java` | `isPriceDropGovernedItem()` (línea ~193) | retorna **solo** `isRealEstate(item)` | Motors no entra al gate de experimento del precio tachado → tachado siempre "libre" |

**Conclusión:** el spec identifica exactamente estos 4 puntos y los cambios propuestos son correctos. El diseño (delegar plataforma al experimento, borrar los gates de código) es el approach YAGNI/KISS correcto: es un feature-flag que ya existe, no hace falta inventar nada.

### Por qué NO se toca el SDK

- El label "BAJÓ DE PRECIO" y el tachado se activan vía predicados del `PriceDecoratorBuilder` del SDK (`withPriceDropLabel(...)`, `withCrossedOutPrice(...)`) que **ya están cableados** en el factory y **ya se usan** para RES web y Motors nativo.
- El contrato REST (`discount_label`, `crossed_out_price`) ya existe. No hay campo nuevo.
- Extender a Motors web = cambiar el valor booleano que devuelven esos predicados. Cero cambios en `java-polycard-sdk`, cero bump de versión.

### ⚠️ Hallazgos que el spec NO cubre (leer antes de implementar)

1. **Gate broad + narrowing interno (NO "simplificar").** `isPriceDropGovernedItem()` usa el gate **broad** `isRealEstate` (sin excluir `DEVELOPMENT`) y el narrowing fino ocurre después dentro de `shouldShowPriceDropFeatures → isPriceDropExperimentActive → isIndividualRealEstateItem`. El cambio #4 debe quedar `isRealEstate(item) || isMotorsItem(item)` — **broad para ambos**. **NO** reemplazar por `PriceDropExperimentHelper.appliesToPriceDrop(...)`, porque ese helper usa el check **narrow** de RES (`isIndividualRealEstateItem`) y eso regresiona el tachado de RES `DEVELOPMENT` (regresión que el equipo ya corrigió una vez — ver [[Search Middleware - Correccion Bajo de Precio Motors]]).

2. **Map layout: fuera de alcance, dejarlo explícito.** En el mismo factory v1, `create()` tiene una rama `isMapLayout` con un `withPriceDropLabel` **inline** distinto (línea ~60): `!isNative && isRealEstate`. Esa rama **no** llama a `shouldShowPriceDropLabel()`, así que Motors no tendrá label en map layout aunque hagamos el cambio #3. Es correcto dejarlo así (Motors no usa vista mapa; el mapa es geo/RES). **Declararlo out-of-scope** en el PR para que Code Review no lo marque como olvido.

3. **Riesgo latente: el factory sucesor (`overrides/common/PriceDecoratorFactory`) NO implementa Motors.** Existe una migración en curso a la nueva arquitectura task-path de Polycard (`app/polycard/overrides/...`, anotada `@Successor(status = IN_PROGRESS)` que reemplazará al factory v1). Ese factory sucesor:
   - solo cablea `priceDropExperiment` (RES); **no** cablea `priceDropMotorsExperiment`;
   - su `shouldShowCrossedOutPrice` solo gobierna RES (Motors cae al `return true`);
   - **no tiene `withPriceDropLabel` en ningún lado** del árbol `overrides/` (ni RES ni Motors).
   
   Hoy `IN_PROGRESS` = "no usar en producción", así que el **path productivo es el v1** y este proyecto está bien apuntado. **PERO**: cuando esa migración pase a `READY`, "bajó de precio" Motors (y el label RES web) regresionarán en todas las plataformas si nadie porta la lógica. **Acción:** dejar comentario/aviso en el PR y coordinar con el dueño de la migración single-view. No es bloqueante para este PR, pero sí un pendiente de seguimiento (ver Tareas).

4. **RES no debe regresionar.** El cambio #3 en la rama web debe quedar `isRealEstate(item) || (isMotorsItem(item) && shouldShowPriceDropFeatures(...))` — se **suma** Motors, no se reemplaza RES. Test de no-regresión RES obligatorio.

## 🛠️ Plan de implementación (para el agente que lo tome)

### Git (regla dura del usuario)

- Rama **nueva** desde `develop`, nombre sugerido: `feature/VMDEM-21-price-drop-all-platforms`.
- **Prohibido** reutilizar `feature/price-variation-all-platforms-motors` ni ninguna rama existente del listado (todas deprecadas).
- Crear la rama, implementar, correr validaciones y **dejar en working tree sin commit/push** hasta OK explícito del humano (preferencia [[rjara-meli-work-preferences]]).
- No tocar untracked no funcionales del repo (`.agents/`, `AGENTS.md`, `graphify-out/`, `previous-price/`, `descripcion_pr.md`).

### Los 4 cambios (diffs verificados contra develop)

```java
// 1. PriceDropMotorsExperimentTask.java — quitar dependency + override nativo-only.
//    La task hereda el default (isExperimentApplicable == true). Fury controla la audiencia.
- import com.mercadolibre.middleend.core.task.TaskDependency;
- import com.mercadolibre.search.middleware.app.shared.models.SearchBaseExperimentModel;
- import meli.rx.Observable;   // (revisar: sigue usándose en execute()/fallback → conservar)

- @TaskDependency(PolycardSingleMotorsExperimentTask.class)
- public Observable<SearchBaseExperimentModel> polycardSingleMotorsExperimentTask;
-
- @Override
- protected Observable<Boolean> isExperimentApplicable() {
-     return polycardSingleMotorsExperimentTask.map(SearchBaseExperimentModel::isActive);
- }
// (dejar execute(), getDefaultModel(), createForcedExperiment(), fallback() intactos)

// 2. PriceDropExperimentHelper.isPriceDropExperimentActive() — rama Motors.
  if (isMotorsItem(polycardItem)) {
-     return SearchBaseExperimentModel.isActive(model.polycardSingleMotorsExperiment)
-             && nonNull(model.priceDropMotorsExperiment)
-             && model.priceDropMotorsExperiment.show;
+     return nonNull(model.priceDropMotorsExperiment)
+             && model.priceDropMotorsExperiment.show;
  }

// 3. PriceDecoratorFactory (registry/v1/factories) — shouldShowPriceDropLabel(), rama web.
  if (!device.isNative()) {
-     return isRealEstate(polycardItem);
+     ItemModelBase itemModelBase = getItemModelBase(polycardItem);
+     return isRealEstate(polycardItem)
+         || (PriceDropExperimentHelper.isMotorsItem(polycardItem)
+             && PriceDropExperimentHelper.shouldShowPriceDropFeatures(model, polycardItem, itemModelBase));
  }
// (la rama nativa ya evalúa Motors; queda igual)

// 4. PriceDecoratorFactory (registry/v1/factories) — isPriceDropGovernedItem().
  private boolean isPriceDropGovernedItem(PolycardItem polycardItem) {
-     return isRealEstate(polycardItem);
+     return isRealEstate(polycardItem) || PriceDropExperimentHelper.isMotorsItem(polycardItem);
  }
```

> Nota SOLID/clean: los 4 cambios son sustracción de acoplamiento (borrar un prerequisito nativo-only) + una suma explícita de la vertical Motors. No se introduce ninguna abstracción nueva (rules/strategy/gate) — se respeta el estilo local de helper estático ya consolidado en la corrección previa.

### Verificar tras editar

- `PriceDropMotorsExperimentTask`: confirmar que al quitar el `@TaskDependency` no quede import ni campo huérfano, y que `PolycardSingleMotorsExperimentTask` **siga existiendo** (otras features la usan; solo se desacopla de esta task).
- Confirmar que `getItemModelBase(...)` y `ItemModelBase` ya están importados/disponibles en el factory (la rama nativa ya los usa → sí).

## 🧪 Testing

Objetivo cobertura: ≥85% líneas nuevas/modificadas (repo exige 90% en critical paths; DTOs/models excluidos).

**`PriceDecoratorFactoryTest`** (label + tachado):

| Escenario | Platform | Vertical | exp Motors | hasPriceVariation | Esperado |
|-----------|----------|----------|-----------|-------------------|----------|
| Motors Desktop, exp activo | Desktop | MOTORS | show=true | true | label visible + tachado |
| Motors WebMobile, exp activo | WebMobile | MOTORS | show=true | true | label visible + tachado |
| Motors Desktop, exp apagado | Desktop | MOTORS | show=false | true | sin label / sin tachado |
| Motors Desktop, sin variación | Desktop | MOTORS | show=true | false | sin label / sin tachado |
| **RES web NO regresiona** | Desktop | REAL_ESTATE | — | true | label visible (igual que hoy) |
| **RES DEVELOPMENT NO regresiona** | Desktop | REAL_ESTATE (domainId DEVELOPMENT) | — | true | sin tachado (comportamiento histórico) |

**`PriceDropMotorsExperimentTaskTest`**: la task evalúa (applicable) en Desktop/WebMobile sin gate `polycardSingleMotors`.

**`PriceDropExperimentHelperTest`**: `isPriceDropExperimentActive` para Motors true con solo `priceDropMotorsExperiment.show` (sin `polycardSingleMotors`); suite RES intacta (individual aplica, `domainId==null` aplica, `DEVELOPMENT` no aplica).

### Comandos de validación

```bash
cd /Users/rjara/fuentes/search-middleware
JAVA_HOME=/Users/rjara/Library/Java/JavaVirtualMachines/corretto-17.0.14/Contents/Home \
PATH=$JAVA_HOME/bin:$PATH ./gradlew test \
  --tests 'com.mercadolibre.search.middleware.app.shared.utils.PriceDropExperimentHelperTest' \
  --tests 'com.mercadolibre.search.middleware.app.shared.services.polycard.registry.v1.factories.PriceDecoratorFactoryTest' \
  --tests 'com.mercadolibre.search.middleware.unit.app.shared.tasks.PriceDropMotorsExperimentTaskTest'
```

Si pasa, suite completa: `./gradlew test`. (El repo usa Java 21 según CLAUDE.md; el corretto-17 del comando histórico puede requerir ajuste a 21 — verificar `JAVA_HOME` disponible antes de correr.) `checkstyleMain`/`pmdMain` pueden fallar por falta de `config/checkstyle/checkstyle_rules.xml` en el entorno local: gap preexistente, no introducido por este cambio.

## 🚀 Rollout

- Deploy **sin** cambios de audiencia → comportamiento idéntico al actual (web sigue sin ver Motors porque el experimento no incluye web todavía).
- Activar web: agregar Desktop y WebMobile a la audiencia de `vis/item-dropprice-motors` en la consola de Fury Experiments. **Owner del experimento: rodrigo.jara@mercadolibre.cl** (confirmado en `@ExperimentMetadata` de la task).
- Rollback: reducir audiencia en Fury, sin revert de código.
- Validar segmentando por plataforma en la consola de Fury.

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

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. %%
> - [x] Reevaluar el spec contra el código real y resolver la duda SDK vs search-middleware #owner/agent #type/research #area/meli #app/search-middleware
> - [x] Crear rama nueva `feature/VMDEM-21-price-drop-all-platforms` desde `develop`, sin commit ni push #owner/agent #type/dev #area/meli
> - [x] Aplicar los 4 cambios (task, helper, factory label, factory governed) conservando gate broad + narrowing interno #owner/agent #type/dev #area/meli #app/search-middleware
> - [x] Agregar/ajustar tests: Motors Desktop/WebMobile, no-regresión RES y RES DEVELOPMENT, task sin gate polycardSingle #owner/agent #type/dev #area/meli #app/search-middleware
> - [x] Correr validaciones (tests focalizados + suite) y dejar working tree listo para revisión humana #owner/agent #type/pr-review #area/meli
> - [ ] Correr validaciones (tests focalizados + suite) y dejar working tree listo para revisión humana #owner/agent #type/pr-review #area/meli
> - [ ] Confirmar con el humano la audiencia del experimento (Desktop/WebMobile) antes del rollout web #owner/me #type/admin #area/meli
> - [ ] Coordinar con el dueño de la migración `overrides/` (single-view SDK) para portar Motors price drop antes de que pase a READY #owner/me #type/dev #area/meli #app/search-middleware

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-07-29** — Se crea el proyecto agente bajo [[Cierre VIS]] y se mueve el spec técnico recibido a `resources/`.
- **2026-07-29** — **Reevaluación completa contra `origin/develop`.** Verdict: el spec es correcto y suficiente para el rollout actual; se resuelve la duda del SDK (no se toca `java-polycard-sdk`). Se verificaron los 4 gates en código real, se detectaron 4 hallazgos no cubiertos por el spec (gate broad vs narrow, map layout out-of-scope, factory sucesor `overrides/` sin Motors, no-regresión RES) y se descartó la rama `feature/price-variation-all-platforms-motors` por estar deprecada/contaminada. Plan de implementación y tests escritos en esta nota. No se creó rama ni se tocó código.
- **2026-07-29** — Se crea `feature/VMDEM-21-price-drop-all-platforms` desde `develop`; el agente inicia la implementación de los cuatro gates en `search-middleware`, sin commit ni push.
- **2026-07-29** — Implementación y tests focalizados completados. `./gradlew test` con Corretto 21 pasó para `PriceDropExperimentHelperTest`, `PriceDecoratorFactoryTest` y `PriceDropMotorsExperimentTaskTest`; se inicia la suite completa.
- **2026-07-29** — `CartDecoratorMediatorTest` se ajusta al contrato nuevo y pasa junto con la suite focalizada. La suite completa queda con 13 fallas ajenas en `SearchShopsAdsServiceTest` por `NoSuchMethodError: Platform.getSearchShopsAdsConfig()`. Código listo para revisión humana, sin commit ni push.
- **2026-07-29** — `checkstyleMain` falla por errores preexistentes de formato/Javadoc en múltiples archivos fuera del cambio; no se amplía el alcance para corregirlos.
- **2026-07-30** — Se completa `descripcion_pr.md` en el root con alcance funcional, flujo Mermaid, pruebas ejecutadas, limitaciones de suite/checkstyle y rollout/rollback de Fury. Queda listo para revisión del PR.

## 🧭 Decisiones

- **No se borra ni recrea el proyecto:** el approach del spec es sólido. Se conserva el spec en `resources/` como fuente y esta nota pasa a ser el plan ejecutable reevaluado.
- **Alcance: solo `search-middleware`.** Sin `java-polycard-sdk`, sin bump de versión de Polycard.
- **Sin abstracciones nuevas.** Se respeta el helper estático `PriceDropExperimentHelper` ya consolidado; nada de rules/strategy/gate (aprendizaje de [[Search Middleware - Correccion Bajo de Precio Motors]]).
- **Preservar `isPriceDropGovernedItem` como gate broad** (`isRealEstate || isMotorsItem`) con narrowing interno; no unificar con el helper narrow.
- **Map layout fuera de alcance** (declararlo en el PR).

## 🔗 Docs / Links

- [Price Variation All Platforms — Search - Technical Spec](resources/Price%20Variation%20All%20Platforms%20%E2%80%94%20Search%20-%20Technical%20Spec.md)
- Spellbook spec base: `https://spellbook.adminml.com/projects/VMDEM/specs/1c9f4d16-60de-4a8d-9437-820b20a043f4`
- Referencia Motors nativo: `fury_search-middleware` PR #13976
- Referencia RES all platforms: `fury_search-middleware` PR #13767 / #12851
- [[Cierre VIS]] · [[Search Middleware - Correccion Bajo de Precio Motors]] · [[Bajó de Precio]] · [[search-middleware]]

## 💡 Ideas

### Backlog de ideas

- Dejar comentario en el PR: (1) el cambio no altera RES; (2) Motors queda gobernado solo por `vis/item-dropprice-motors`; (3) map layout out-of-scope; (4) el factory sucesor `overrides/` deberá portar esta lógica antes de pasar a READY.

### Motivos / principios

- Agregar/extender una vertical no debe relajar restricciones históricas de otra (RES `DEVELOPMENT`).
- Delegar audiencia a Fury > gates de plataforma en código: activar/desactivar sin deploy.

### Memoria pública / interna

- **Memoria pública:** el estado y el plan viven en esta nota; el aprendizaje reusable (SDK innecesario, gate broad vs narrow) ya está capturado en [[Search Middleware - Correccion Bajo de Precio Motors]].
- **Memoria interna:** riesgo latente del factory sucesor `overrides/` como pendiente de coordinación.
- **Motivo:** que el próximo agente ejecute sin redescubrir el código ni repetir la regresión de RES.
