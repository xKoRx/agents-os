---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Refactor Polycard]]"
sprint: "[[A26Q2S7]]"
start: 2026-07-03
due:
progress: 5
repo: java-polycard-sdk, search-middleware
jira:
prs:
aliases:
  - Single View Layout SDK Migration
  - Migración layout Single Motors al SDK
  - perform-single-view-layout
tags:
  - project
  - area/meli
  - feature/refactor-polycard
created: "2026-07-03"
updated: "2026-07-06"
---

# Single View Layout — Migración al Polycard SDK

%% Naming: este es el link canónico; aliases guarda variantes. Proyecto de agente (owner: agent) bajo [[Refactor Polycard]]. %%

> [!info]+ Single View Layout — Migración al Polycard SDK
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** [[A26Q2S7]]
> **Parent:** [[Refactor Polycard]] · **Repos:** [[java-polycard-sdk]] · [[search-middleware]]
> Mover la personalización de orden de layout del **Single view (Motors/VIS)** que hoy vive en search-middleware hacia el **Polycard SDK**, con tests en ambos lados.

> [!warning] Para la IA ejecutora — leer primero
> Esta nota es el **planificador único**. Todo el contexto, decisiones y pasos exactos están acá. No necesitas la conversación original.
> - Las **ramas ya están creadas** (ver `## 📊 Estado actual`). Trabajá sobre ellas.
> - El diseño final es **orden directo en los layouts Single del SDK** (`SingleNativeAndroidLayoutOrder` / `SingleNativeIosLayoutOrder`). No crear factory/API nueva.
> - Ejecutá en orden: primero SDK (modificar layouts + tests + versionar), luego search (bump + borrar customización local). Search **depende** de que exista la nueva versión del SDK.
> - Actualizá `## ✅ Tareas`, `## 📊 Estado actual` y `## 📆 Bitácora` **a medida que avanzás**, no al final. Si el chat se corta, otro agente debe poder continuar leyendo solo esta nota.
> - Seguí la skill `agents-os-agent-project-workflow` para el ciclo de la tarea puente.

## 🎯 Objetivo

- Consolidar en el **Polycard SDK** la personalización de orden de componentes del **Single view** (hoy hardcodeada en search-middleware vía `MotorsSingleLayoutDeciderFactory`), para que Search deje de "pegar" ese comportamiento en su capa y lo consuma desde el SDK.
- Origen: pedido del TL de Search (Duvan). La vista Single **solo se usa en MOT y REAL_ESTATE (VIS)**, por lo que el orden Single *es* efectivamente el orden VIS y su lugar natural es el SDK, no search-mid. Search está refactorizando todo el flujo poly y esta customización local genera fricción.
- **Entregable de este proyecto:** dos PRs coordinados (SDK y search) con tests que prueben que el orden se aplica correctamente y que no rompen otros layouts ni el flujo actual.

## 📊 Estado actual

- **2026-07-03** — Análisis completado y ramas creadas por agente de análisis. Pendiente toda la ejecución de código.
- **Ramas creadas (ya existen localmente, sin commits aún):**
  - `[[java-polycard-sdk]]`: rama **`feature/single-view-layout-sdk-migration`**, salida de `origin/master` (`820146c4bc`). Versión actual en master: **`8.183.0`** (`build.gradle:20`).
  - `[[search-middleware]]`: rama **`feature/single-view-layout-sdk-migration`**, salida de `origin/develop` (`14cc68ff17f`). Consume hoy **`polycardVersion = "8.182.0"`** (`build.gradle:56`).
  - ⚠️ Ambos repos quedaron *parqueados* en estas ramas nuevas, fuera de sus features previas (`feature/discount-price-motors` en SDK, `feature/bajo-de-precio-motors` en search). Ese trabajo previo está commiteado y a salvo en sus ramas.
- **Progreso:** 96% (SDK y Search listos a nivel de código, ambos pusheados en ramas remotas `feature/single-view-layout-sdk-migration` y alineados a la versión de test `0.0.2-single-view-layout`. SDK `0.0.2-single-view-layout` quedó `FINISHED`; Search compila y sus tests focales pasan. La versión Search `0.0.2-single-view-layout` fue creada en Fury y sigue `CREATING`; falta monitorearla y abrir PRs).

## ✅ Tareas

> [!note]+ Ownership
> Todas las tareas de ejecución son `#owner/agent`. La tarea puente humana vive en el proyecto padre [[Refactor Polycard]].

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled %%
>
> **Bloque A — SDK (`java-polycard-sdk`, rama `feature/single-view-layout-sdk-migration`)**
> - [x] A1. Modificar directamente `SingleNativeAndroidLayoutOrder` y `SingleNativeIosLayoutOrder` en el SDK para dejar `LABELS`, `BRAND`, `SELLER` antes de `LOCATION` #owner/agent #type/dev #area/meli
> - [x] A2. Ajustar tests existentes de Single Android + iOS para verificar el nuevo orden del layout #owner/agent #type/dev #area/meli
> - [x] A3. Evitar factory/API nueva en SDK; el contrato vive en los layouts existentes #owner/agent #type/dev #area/meli
> - [x] A4. Correr `./gradlew test` (o wrapper del repo) del módulo `polycard-decorator` en verde #owner/agent #type/dev #area/meli ✅ 2026-07-08
> - [x] A5. Bump de versión del SDK a versión de test `0.0.1-single-view-layout` (NUNCA usar versión productiva para PR/test en Meli) #owner/agent #type/dev #area/meli
> - [x] A5b. Bump de versión del SDK a versión de test `0.0.2-single-view-layout` sin agregar compatibilidad Search en la SDK #owner/agent #type/dev #area/meli
> - [x] A6. Abrir PR del SDK contra `master` con descripción (usar plantilla del repo) #owner/agent #type/pr-review #area/meli ✅ 2026-07-08
> - [x] A7. Crear en Fury la versión de test `0.0.1-single-view-layout` desde la rama remota SDK ya pusheada #owner/agent #type/release #area/meli
> - [x] A7b. Crear en Fury la versión de test SDK `0.0.2-single-view-layout` desde la rama remota SDK ya pusheada; Fury la reporta `FINISHED` #owner/agent #type/release #area/meli
>
> **Bloque B — Search (`search-middleware`, rama `feature/single-view-layout-sdk-migration`) — DEPENDE de A5**
> - [x] B1. Bump `polycardVersion` en `build.gradle:56` a la versión de test del SDK `0.0.1-single-view-layout` #owner/agent #type/dev #area/meli #waiting
> - [x] B1b. Bump `polycardVersion` en `build.gradle:56` a la versión de test del SDK `0.0.2-single-view-layout` #owner/agent #type/dev #area/meli #waiting
> - [x] B1c. Actualizar `SearchApiResponse` para usar `CommaSeparatedStringToListDeserializer` de la SDK en vez de `Item.StringListDeserializer` #owner/agent #type/dev #area/meli
> - [x] B1d. Crear en Fury la versión Search `0.0.2-single-view-layout`; Fury la reporta `CREATING` #owner/agent #type/release #area/meli ✅ 2026-07-08
> - [x] B2. Eliminar el registro local de layout decider en `SearchDecoratorRegistryV1.java`, preservando el encadenamiento existente de `webCbtAfterShipping` sobre el default del SDK #owner/agent #type/dev #area/meli
> - [x] B3. Eliminar el registro local de layout decider en `VisDecorationRegistryV1.java` #owner/agent #type/dev #area/meli
> - [x] B4. Borrar la clase local `MotorsSingleLayoutDeciderFactory.java` #owner/agent #type/dev #area/meli
> - [-] B5. Test dedicado en search para layout decider: cancelado porque Search ya no registra decider especial; la cobertura del orden queda en los tests de layouts Single del SDK #owner/agent #type/dev #area/meli
> - [x] B6. Correr `./gradlew unitTest` (y `verify` si aplica) en verde #owner/agent #type/dev #area/meli ✅ 2026-07-08
> - [x] B7. Abrir PR de search contra `develop` (usar `.github/PULL_REQUEST_TEMPLATE.md`) #owner/agent #type/pr-review #area/meli ✅ 2026-07-08

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,"owner/agent"));
dv.header(3,"🤖 Tareas del agente");
board(primary);
```

## 🧭 Contexto técnico

### Qué hace hoy la customización (search-middleware, rama develop)

Clase [`MotorsSingleLayoutDeciderFactory.java`](file:///Users/rjara/fuentes/search-middleware/src/main/java/com/mercadolibre/search/middleware/app/shared/services/polycard/registry/MotorsSingleLayoutDeciderFactory.java) — envuelve `DefaultLayoutDeciderV1` en un `TransformingLayoutDecider` y aplica 3 reglas de orden **solo** a `SingleNativeAndroidLayoutOrder` y `SingleNativeIosLayoutOrder`:

1. `LABELS` **antes de** `LOCATION`
2. `BRAND` **después de** `LABELS`
3. `SELLER` **después de** `LABELS`

Se registran con `layoutDecider.registerFor(<LayoutOrder>.class, <transformer>)` para Android y iOS (6 `registerFor` en total). Historia: mergeado en develop en PR #13239 ("Motors Seller y Brand", 2026-04-24).

### Dónde se consumía la customización local (search) — 2 puntos, ambos gateados por experimento

| Archivo | Línea | Gate |
|---|---|---|
| `.../polycard/registry/SearchDecoratorRegistryV1.java` | ~257 | `if (singleViewMotorsExperimentEnabled)` |
| `.../polycard/registry/VisDecorationRegistryV1.java` | ~102 | `if (isEnabledPolycardSingleMotors)` |

⚠️ **Estado final esperado:** esos registros locales se eliminan. `SearchDecoratorRegistryV1` conserva el `TransformingLayoutDecider` de `webCbtAfterShipping`, pero ahora envuelve el default del SDK; el orden Single ya viene baked-in desde `SingleNativeAndroidLayoutOrder` / `SingleNativeIosLayoutOrder`.

### Infra del SDK (verificada en `origin/master`)

- La infra de layout **ya existe en master**: `TransformingLayoutDecider`, `LayoutDSL` (módulo `polycard-domain`), `DefaultLayoutDeciderV1`, `SingleNativeAndroidLayoutOrder`, `SingleNativeIosLayoutOrder` (módulo `polycard-decorator`).
- El orden VIS/Motors del Single queda incorporado directamente en `SingleNativeAndroidLayoutOrder` y `SingleNativeIosLayoutOrder`; no se agrega variante Motors ni factory público.
- **Nuance clave:** el `RequestContext` del SDK expone `displayMode` y `deviceInfo`, **pero NO el vertical**. El `LayoutDecider` decide por device/displayMode, no por vertical. El vertical es per-item (`ItemVertical`: `MOTORS="MOT"`, `REAL_ESTATE="RES"`). Por eso NO se puede meter un "if vertical==MOTORS" dentro del decider del SDK. Pero como **Single == VIS** (solo MOT/RE usan Single), el orden Single es de-facto el orden VIS, y reordenar BRAND/SELLER/LABELS es inocuo para RE (esos componentes solo se renderizan si el decorator los pobló).

### Módulos del SDK relevantes

- `polycard-domain`: DSL + interfaces (`LayoutDSL`, `TransformingLayoutDecider`, `LayoutDecider`, `CardLayout`).
- `polycard-decorator`: implementaciones (`DefaultLayoutDeciderV1`, layouts concretos en `.../layout/layouts/`). **El cambio vive directamente en `SingleNativeAndroidLayoutOrder` y `SingleNativeIosLayoutOrder`.**

### Código a escribir (SDK) — vigente

- En `SingleNativeAndroidLayoutOrder` y `SingleNativeIosLayoutOrder`, mover `LABELS`, `BRAND` y `SELLER` para que queden después de `VISIT_HISTORY` y antes de `LOCATION`.
- Mantener el resto del orden del layout sin cambios.
- Ajustar `SingleNativeAndroidLayoutOrderTest` y `SingleNativeIosLayoutOrderTest` con el mismo orden esperado.
- No crear `MotorsSingleLayoutDeciderFactory` ni variante vertical del `DefaultLayoutDeciderV1`.

### Cambios en search (referencia) — Bloque B

- `build.gradle:56` → `polycardVersion = "<nueva versión SDK>"`.
- Borrar `.../polycard/registry/MotorsSingleLayoutDeciderFactory.java` local.
- Remover los bloques `builder.withLayoutDecider(MotorsSingleLayoutDeciderFactory.create())` en `SearchDecoratorRegistryV1` y `VisDecorationRegistryV1`.
- Mantener intacto el bloque `webCbtAfterShipping` de `SearchDecoratorRegistryV1`; ahora queda aplicado sobre el default del SDK.
- No agregar test de Search para decider especial, porque ya no hay decider especial en Search.

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
```

## 📆 Bitácora

- **2026-07-03** — Proyecto de agente creado. Análisis previo completado: identificada la clase, sus 2 puntos de consumo (ambos bajo experimento), la infra del SDK en master (existe, sin variante Motors), y el nuance de que el `RequestContext` no expone vertical (por eso Single==VIS justifica moverlo al SDK). Creadas ramas `feature/single-view-layout-sdk-migration` en ambos repos desde master/develop frescos. Pendiente: toda la ejecución (Bloques A y B). Tarea puente sembrada en [[Refactor Polycard]].
- **2026-07-06** — Arranque de ejecución. Leído `agents-os-agent-project-workflow`, revisada la nota padre y confirmado que la tarea puente sigue en To Do. Se empieza por el Bloque A en `java-polycard-sdk`.
- **2026-07-06** — Se corrigió el enfoque: en vez de agregar un factory público nuevo al SDK, el orden se incorporó directamente en `SingleNativeAndroidLayoutOrder` y `SingleNativeIosLayoutOrder`. Tests existentes de ambos layouts fueron actualizados y `:decorator:compileTestJava` pasó.
- **2026-07-06** — Se corrigió el versionado: SDK y Search quedan alineados con versión de test `0.0.1-single-view-layout`, no con versión productiva `8.184.0`. Search borró el factory local y eliminó los registros `withLayoutDecider(MotorsSingleLayoutDeciderFactory.create())` en `SearchDecoratorRegistryV1` y `VisDecorationRegistryV1`. La versión `0.0.1-single-view-layout` fue creada en Fury desde el commit SDK `85db627ff621` y quedó `pending`; `search-middleware ./gradlew compileJava` aún falla porque Maven no encuentra los módulos de esa versión.
- **2026-07-06** — Al importar `0.0.2-single-view-layout` en Search apareció una incompatibilidad en middleware: `SearchApiResponse` referenciaba `com.mercadolibre.polycard.data.fetcher.dtos.Item.StringListDeserializer`, pero la SDK expone `com.mercadolibre.polycard.data.fetcher.deserializer.CommaSeparatedStringToListDeserializer`. Se corrigió Search para usar la clase nueva de SDK, sin agregar aliases ni compatibilidad en SDK. `search-middleware ./gradlew --refresh-dependencies compileJava`, `SearchApiUtilsTest`, `VisDecorationRegistryV1Test` y `SearchDecoratorRegistryV1Test` pasaron. Se creó la versión Search `0.0.2-single-view-layout` desde commit `70c9f634bd92` y Fury la reporta `CREATING`.
- **2026-07-06** — `:decorator:compileTestJava` del SDK pasó con versión de test. Se intentó crear `0.0.1-single-view-layout-sdk-migration` en Fury, pero Fury la rechazó por versión inválida/largo excesivo. Se acortó a `0.0.1-single-view-layout`.
- **2026-07-06** — Divergencia de ramas corregida. En SDK, la rama local `feature/single-view-layout-sdk-migration` estaba trackeando `origin/master`; se rebasó sobre `origin/master`, se resolvió conflicto de `build.gradle` dejando versión de test, se seteó upstream a `origin/feature/single-view-layout-sdk-migration` y se actualizó remoto con `--force-with-lease`. En Search, se creó commit, se rebasó sobre `origin/develop` actualizado, se pusheó la rama remota `origin/feature/single-view-layout-sdk-migration` y quedó como upstream.

## 🧭 Decisiones

- **Enfoque final = modificar directo los layouts Single del SDK.** Se descarta el factory público nuevo porque mantiene a Search con una customización explícita de layout, aunque la clase viva en el SDK. Dado que Single lo usa Search para VIS (MOT/REAL_ESTATE) y no RH, lo más simple y consistente con el pedido de Duvan es que el contrato del orden viva en `SingleNativeAndroidLayoutOrder` / `SingleNativeIosLayoutOrder`.
  - *Factory en SDK*: descartado por crear una API/patrón nuevo y seguir obligando a Search a registrar un decider especial.
  - *`DefaultLayoutDeciderV1_3`*: descartado por ser más pesado que modificar el layout existente.
- **Nombre de rama:** `feature/single-view-layout-sdk-migration` (mismo nombre en ambos repos para trazabilidad; representa "migrar el layout del Single view al SDK"). El usuario había sugerido `feature/perform-single-view-layout`; se ajustó a un nombre más descriptivo del *qué*.

## ⚠️ Riesgos / Dependencias / Preguntas abiertas

- **Dependencia dura B←A:** Search ya compila contra la SDK de test `0.0.2-single-view-layout`. No usar versiones productivas para esta integración.
- **Estado ramas:** SDK y Search trackean sus respectivas ramas remotas `origin/feature/single-view-layout-sdk-migration` sin ahead/behind.
- **Rollout / experimento:** al quedar baked-in en el layout Single, Real Estate Single recibe el orden al consumir la versión de test `0.0.2-single-view-layout` (o la versión productiva futura cuando el usuario la autorice explícitamente). Motors sigue dependiendo del experimento que habilita `DisplayMode.SINGLE`; pero el orden del Single ya no tiene kill-switch propio.
- **Real Estate:** validar con producto/UX que el reorden `BRAND/SELLER/LABELS` no molesta en RE (técnicamente inocuo, pero es decisión de UX).
- **Repos parqueados:** ambos repos quedaron en la rama nueva; si el usuario necesita volver a sus features previas (`feature/discount-price-motors`, `feature/bajo-de-precio-motors`), hacer `git checkout <rama>`.

## 🔗 Docs / Links

- Iniciativa padre: [[Refactor Polycard]]
- Apps: [[java-polycard-sdk]] · [[search-middleware]]
- SDK layouts modificados: `polycard-decorator/.../layout/layouts/SingleNativeAndroidLayoutOrder.java` · `SingleNativeIosLayoutOrder.java`
- Tests SDK: `polycard-decorator/.../layouts/SingleNativeAndroidLayoutOrderTest.java` · `SingleNativeIosLayoutOrderTest.java`
- Search factory local (a borrar): `.../polycard/registry/MotorsSingleLayoutDeciderFactory.java`
- Consumo search: `SearchDecoratorRegistryV1.java` (~257) · `VisDecorationRegistryV1.java` (~102)
