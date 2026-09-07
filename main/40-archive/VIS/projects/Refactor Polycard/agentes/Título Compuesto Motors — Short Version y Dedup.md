---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Refactor Polycard]]"
sprint: "[[A26Q2S7]]"
start: 2026-07-09
due:
progress: 85
repo: java-polycard-sdk, search-middleware
jira:
prs:
aliases:
  - Título Motors Short Version + Dedup
  - Motors composite title dedup
  - dedup título motors
tags:
  - project
  - area/meli
  - feature/refactor-polycard
created: "2026-07-09"
updated: "2026-07-15"
---

# Título Compuesto Motors — Short Version y Dedup

%% Naming: link canónico; aliases guarda variantes. Proyecto de agente (owner: agent) bajo [[Refactor Polycard]]. Reemplaza la tarea suelta "Crear versión solo title {BRAND} {MODEL} {SHORT_VERSION} {VEHICLE_YEAR}" del padre, que se extendió más de lo previsto. %%

> [!info]+ Título Compuesto Motors — Short Version y Dedup
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** [[A26Q2S7]]
> **Parent:** [[Refactor Polycard]] · **Repos:** [[java-polycard-sdk]] · [[search-middleware]]
> Componer el título de la card de Motors como `marca modelo short_version año` y **evitar palabras repetidas** entre `modelo` y `short_version` (ej. `MI 320` vs `MI320`) con una validación robusta de normalización + dedup.

> [!warning] Para la IA ejecutora — leer primero
> Esta nota es el **planificador único**. Todo el contexto, decisiones y pasos exactos están acá; no necesitas la conversación original ni el hilo de Slack.
> - Rama en revisión: **`feature/new-title-motors-test`** en `/Users/rjara/fuentes/java-polycard-sdk`; versión de test `0.0.12-new-title-motors`.
> - **Tests con Java 17, NO 21** (JDK 21 rompe Mockito): `export JAVA_HOME=/Users/rjara/Library/Java/JavaVirtualMachines/corretto-17.0.14/Contents/Home` antes de `./gradlew`. Módulos usan nombres cortos (`:decorator`, `:api`).
> - **NUNCA versión productiva** para pruebas/PR: usar versión de test `0.0.x-new-title-motors`.
> - El síntoma "marca modelo año" sin versión en test **no es bug**: los mocks casi no traen `SHORT_VERSION` (1/7). Ver [[2026-07-09-polycard-short-version-title-data-dependency]].
> - Actualizá `## ✅ Tareas`, `## 📊 Estado actual` y `## 📆 Bitácora` **a medida que avanzás**, no al final.
> - Seguí la skill `agents-os-agent-project-workflow` para el ciclo de la tarea puente.

## 🎯 Objetivo

- En Motors (Cars & Vans), mostrar en el título `marca modelo short_version año`, homologado cross-site/cross-plataforma (search card, Ads, single y lista).
- `short_version` = atributo `SHORT_VERSION` con **fallback a `TRIM`** (ya implementado vía `AttributeUtils.Motors.getShortVersionOrTrim`).
- **Nuevo (foco de este proyecto):** eliminar repeticiones de palabras entre `modelo` y `short_version` (~5% de casos observados en `furytest37`), con una validación que cubra el 100% de la repetición **textual** (igualdad, contención, espaciado tipo `MI 320`/`MI320`, mayúsculas, acentos, símbolos).
- Mantener el guardrail de largo: si el título compuesto supera `DEFAULT_MAX_MOTORS_TITLE_LENGTH` (45), volver a `marca modelo año`.
- **Entregable:** título corto + dedup implementados y testeados en el SDK, consumidos por Search con versión de test y entregados a code review en `feature/new-title-motors-test`.

## 📊 Estado actual

- **2026-07-15 — Code review.** El PR actual del SDK implementa el título corto para Motors cuando `versionInTitle = false`: `marca modelo SHORT_VERSION/TRIM año`, con fallback a `marca modelo año` si supera 45 caracteres.
- La composición usa `TitleTokenDeduplicator` para evitar repeticiones textuales entre modelo y versión (`MI 320`/`MI320`, prefijos, mayúsculas, acentos y símbolos). El año queda protegido fuera del dedup.
- El componente y el orden compartido de `SUBTITLE` se mantienen en el SDK. El consumidor de Search deja de solicitar el subtítulo para esta modalidad, evitando duplicar la versión corta sin afectar otras verticales.
- Validación registrada: `:decorator:test` completo en verde con Java 17; tests unitarios, integración del `TitleDecorator` e invariante sobre muestra real de catálogo. No hay cambios pendientes de código para esta revisión; quedan abiertos los pendientes humanos de cobertura/observabilidad y la aceptación del PR.

## ✅ Tareas

> [!note]+ Ownership
> Tareas de ejecución del agente = `#owner/agent` (viven acá). La tarea puente humana vive en el padre [[Refactor Polycard]]. Los **pendientes de Rodrigo** (investigación de caché/coverage) son `#owner/me` y están en su propia sección más abajo.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled %%
>
> **Bloque A — Dedup en el SDK (`java-polycard-sdk`, rama `feature/new-title-motors`)** — DONE (sin commit)
> - [x] A1. Crear utilitario `TitleTokenDeduplicator` (normalización: mayúsculas + sin acentos + sin símbolos; clave compacta para el caso `MI 320`/`MI320`; drop de prefijo cubierto + dedup por token) #owner/agent #type/dev #area/meli ✅ 2026-07-09
> - [x] A2. Integrar el dedup en `getMotorsShortTitle` de `TitleDecorator` (limpiar `short_version` contra `marca+modelo` antes de componer; el año se protege aparte) #owner/agent #type/dev #area/meli ✅ 2026-07-09
> - [x] A3. Tests unitarios del deduplicador cubriendo casos borde (`MI 320`/`MI320`, `Corolla`/`Corolla Cross XEI`, `Onix`/`ONIX`, acentos/símbolos, no-op sin repetición) #owner/agent #type/dev #area/meli ✅ 2026-07-09
> - [x] A4. Test de integración en `TitleDecoratorTest` (repetición vía decorator) #owner/agent #type/dev #area/meli ✅ 2026-07-09
> - [x] A5. CHANGELOG + bump a versión de test `0.0.3-new-title-motors` (NUNCA productiva) #owner/agent #type/dev #area/meli ✅ 2026-07-09
> - [x] A6. Correr `:decorator:test` en verde con Java 17 #owner/agent #type/dev #area/meli ✅ 2026-07-09
>
> **Bloque B — Consumo en Search (`search-middleware`)**
> - [x] B1. Configurar Search para consumir la versión de test del SDK, activar el título corto mediante `versionInTitle = false` y omitir `SUBTITLE` en la modalidad Motors #owner/agent #type/dev #area/meli ✅ 2026-07-15
> - [ ] B2. Validar en `furytest37` los casos borde traídos por Rodrigo #owner/agent #type/dev #area/meli #waiting
>
> **Bloque C — Decisión abierta de mesa (no bloquea A)**
> - [ ] C1. Definir fallback cuando NO hay short_version y el título es largo: ¿mantener TRIM actual vs. **quitar la marca** (propuesta Fabiano: "todos saben que Onix es Chevrolet") vs. char-limit? → decisión de mesa, luego ajustar código #owner/agent #type/dev #area/meli
>
> **Bloque D — Ajustes de alcance pre-PR (delegado a IA vía prompt maestro) — SIN romper funcionalidad**
> - [x] D1. Mantener `PredefinedPolycardComponent.SUBTITLE` en los layouts y sus tests; el componente queda disponible para futuras verticales #owner/agent #type/dev #area/meli ✅ 2026-07-15
> - [x] D2. Suprimir el subtítulo **solo para Motors** cuando el consumidor activa el título corto, a nivel de configuración/predicado y sin remover el componente del layout #owner/agent #type/dev #area/meli ✅ 2026-07-15
> - [x] D3. Mantener la composición específica de Motors en `TitleDecorator` y extraer solo el dedup a `TitleTokenDeduplicator`, aplicando KISS/YAGNI #owner/agent #type/dev #area/meli ✅ 2026-07-15
> - [x] D4. Actualizar `descripcion_pr.md` (estructura del template, descripción acotada al impacto real) #owner/agent #type/docs #area/meli ✅ 2026-07-09
> - [r] D5. PR del SDK abierto con la versión de test y la descripción; esperando code review #owner/me #type/pr-review #area/meli ✅ 2026-07-15

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
const mine=all.filter(t=>has(t,"owner/me"));
if(mine.length){dv.header(3,"🙋 Pendientes de Rodrigo");board(mine);}
```

## 🙋 Pendientes de Rodrigo (#owner/me) — para mañana

> **Actualización 2026-07-09:** Rodrigo **descarta la investigación de la caché** (la Redis de search-api-go no es queriable por valor; BQ ya cubre el universo de casos borde). Se avanza directo al PR del SDK. Los pendientes de coverage/quién-puebla quedan informativos, no bloquean el PR.

- [x] Ver si la **caché de `SHORT_VERSION` es "queriable"** ✅ 2026-07-09 — **Matiz importante:** la caché runtime de `search-api-go` es **Redis** (doc de ítem con `catalog_product_id` + atributos, `fury_go-toolkit-cache`), poblada desde el catálogo; **NO es queriable por valor** (acceso por key) → no se puede barrer por repetición (esto era lo que planteaba Fabi). El **upstream sí es queriable**: `meli-bi-data.WHOWNER.LK_CATALOG_PRODUCTS_CARS_AND_VANS` (BRAND, MODEL, SHORT_VERSION, TRIM, VEHICLE_YEAR, SIT_SITE_ID). Como el `short_version` es por `catalog_product_id`, el catálogo == universo distinto que renderiza search. Barrido: 12.910 combos, **549 (~4.25%) con repetición** (P1 exacto 164, P2 short⊆base 353, P3 modelo-prefijo 146). Mecanismo del script = BQ (universo) + `MotorsTitleDedupInvariantTest` (dedup real + invariante). #owner/me #type/research #area/meli #sprint/A26Q2S7
- [ ] Traer **ejemplos concretos de casos borde/extremos** para la mesa: títulos que pasan a 2 líneas, repeticiones (~5%), y **0km con TRIM extenso** (planteo de Valentina) #owner/me #type/research #area/meli #sprint/A26Q2S7 📅 2026-07-10
- [ ] Obtener el **% de coverage de `SHORT_VERSION`** (aunque sea un proxy) — lo pidió Nacho #owner/me #type/research #area/meli #sprint/A26Q2S7 📅 2026-07-10
- [ ] Confirmar **quién puebla `SHORT_VERSION`** en prod (API Decoradora) y qué tan estable es (se maneja independiente del service de ítems) #owner/me #type/research #area/meli #sprint/A26Q2S7 📅 2026-07-10
- [ ] Validar el título en **pantallas chicas** (el tamaño de device afecta el corte a 2 líneas; el guardrail de 40 chars puede no alcanzar en celus chicos) #owner/me #type/research #area/meli #sprint/A26Q2S7 📅 2026-07-10

## 🧭 Contexto técnico

### Dónde vive la composición (SDK)

`polycard-decorator/.../decoration/TitleDecorator.java`:
- `decorate()` (~L105): cuando `versionInTitlePredicate` es falso, resuelve `SHORT_VERSION` con fallback a `TRIM` y llama a `getMotorsShortTitle(brand, model, subtitle, year)`.
- `getMotorsShortTitle(...)` (~L218): compone `brand model subtitle year` (con `capitalizeWords`), deduplica modelo/versión y, si supera `DEFAULT_MAX_MOTORS_TITLE_LENGTH=45`, cae a `getMotorsTitle(brand, model, null, year, true, false)` = `brand model year`.
- **Punto de inserción del dedup:** limpiar `subtitle` contra la base `brand+model` **antes** de componer `restParts`. El `year` no entra al dedup (se protege).

Atributos (`polycard-decorator/.../utils/AttributeUtils.java`, clase interna `Motors`):
- `getBrand`, `getModel`, `getShortVersion` (key única `SHORT_VERSION`, L271), `getTrim`, `getVersion` (TRIM/VERS), `getShortVersionOrTrim` (L281, short con fallback a trim).

### Algoritmo de dedup (spec robusta)

Trabaja con **claves normalizadas** para comparar, preservando el texto original para mostrar:

1. `normalize(s)` = `NFD` → quitar diacríticos (`\p{M}+`) → uppercase (`Locale.ROOT`). Regex **lineales, ReDoS-safe**.
2. `compact(s)` = `normalize` sin ningún no-alfanumérico → resuelve `MI 320` == `MI320`.
3. `tokens(s)` = `normalize` split por no-alfanumérico.
4. **Base** = `marca + modelo`. **Pass 1 (prefijo cubierto):** recorrer tokens de `short_version`, acumular su `compact`; mientras el acumulado sea substring de `compact(base)`, descartarlos (drop del prefijo ya representado). **Pass 2 (dedup por token):** de lo que queda, descartar tokens cuya clave ya esté en la base o ya haya aparecido (preservando orden).
5. Resultado = remanente de `short_version` (texto original), que luego pasa por `capitalizeWords` como hoy.

Cobertura: 100% de repetición **textual** (igualdad, contención, espaciado, mayúsculas, acentos, símbolos). **No** cubre repetición semántica (sinónimos/abreviaturas tipo `AUT`/`AUTOMATICO`) — requeriría diccionario; fuera de alcance (KISS/YAGNI).

### Casos de referencia (del hilo)

| modelo | short_version | resultado esperado |
|---|---|---|
| `MI 320` | `MI320` | `... MI 320 ...` (remanente vacío) |
| `MI 320` | `MI320 Avantgarde` | `... MI 320 Avantgarde ...` |
| `Corolla` | `Corolla Cross XEI` | `... Corolla Cross XEI ...` |
| `Onix` | `ONIX` | `... Onix ...` |

## 🧭 Decisiones

- **Dedup por normalización + merge por diferencia**, no un simple `contains`: el `contains` crudo falla en `MI 320`/`MI320` (espaciado) y en mayúsculas/acentos. La propuesta de Nacho ("dejar el de mayor length si uno contiene al otro") es correcta pero debe correr sobre la **clave compacta**, no sobre el string crudo.
- **Utilitario dedicado** (`TitleTokenDeduplicator`) en vez de meter todo en `TitleDecorator`: SRP + testeable en aislamiento con casos borde.
- **Fallback a TRIM se mantiene** (ya en `getShortVersionOrTrim`), alineado con lo acordado en el hilo (short con fallback a trim). La discusión de "quitar la marca" queda como decisión abierta (C1), no bloquea el dedup.
- **Subsunción de tokens bidireccional (v2):** cuando un token contiene al otro, gana el más informativo. Un token de short version totalmente cubierto por `marca+modelo` se descarta (`MI 320`/`MI320`); un token de short version que trae un token de modelo + info extra lo reemplaza (`Nx`→`Nx300h`, `Clc`→`Clc200`).
- **Reglas para tokens de 1 letra (guiadas por datos reales de BQ):** (a) NO descartar por contención un token de short version de 1 letra (son trims reales: `L`, `S`, `M`); (b) reemplazar una letra sola del modelo solo si la versión continúa con dígito (`C`→`C230` sí; `A`→`AMG` no). Umbral `MIN_SUPERSEDE_LENGTH=2`.
- **Detección escalable = invariante sobre corpus real**, no salida esperada por caso. `MotorsTitleDedupInvariantTest` corre el dedup sobre un CSV de casos reales del catálogo y falla si queda alguna palabra redundante. Se extiende agregando filas (regenerables con la query de BQ documentada abajo).

## ⚠️ Riesgos / Dependencias / Preguntas abiertas

- **Coverage de short_version** no es 100% y no es estable (atributo independiente del service de ítems) → el fallback a TRIM y el guardrail de largo son la red. Pendiente medir el % real (pendiente Rodrigo).
- **Casos borde de caché** (pendiente Rodrigo) desbloquean el Bloque B / validación en `furytest37`.
- **Pantalla del device** afecta el corte a 2 líneas; el guardrail de 40 chars es una heurística, no garantía en celus chicos.
- **C1 (fallback sin short_version):** decisión de mesa pendiente (TRIM vs quitar marca vs char-limit).
- **Repetición semántica** (sinónimos/abreviaturas) fuera de alcance del dedup textual (requeriría diccionario).
- **Fuente del corpus (BQ):** el barrido y el CSV del test salen de:
  ```sql
  SELECT DISTINCT SIT_SITE_ID, BRAND, MODEL, SHORT_VERSION, TRIM, VEHICLE_YEAR
  FROM `meli-bi-data.WHOWNER.LK_CATALOG_PRODUCTS_CARS_AND_VANS`
  WHERE MODEL IS NOT NULL AND SHORT_VERSION IS NOT NULL
  ```
  Nota: es catálogo a nivel producto/configuración (no ítem); para atributos por ítem existe `BT_VIS_ATTRIBUTES_MO_SE`. La short version en runtime igual viene de la caché de search, no de BQ — BQ sirve para enumerar el universo de combinaciones y encontrar casos borde a escala.
- **Casos que el dedup textual deja pasar a propósito** (documentados, no bloquean): reordenamientos cosméticos cuando un token de versión reemplaza uno de modelo largo (`Iveco Daily Furgão`), y pares letra+símbolo tipo `Captain c` / `C/Caja`. Ninguno es repetición dura.

## 📆 Bitácora

- **2026-07-09** — Proyecto de agente creado desde el hilo de Slack (aprobación de Short Version + aparición del problema de repetición). Reemplaza la tarea suelta del padre "Crear versión solo title …". Tarea puente sembrada en [[Refactor Polycard]]. Pendientes humanos (caché/coverage) registrados. Arranca ejecución del Bloque A (dedup en el SDK).
- **2026-07-09** — Bloque A completo (sin commit). `TitleTokenDeduplicator` creado + integrado en `TitleDecorator.getMotorsShortTitle`; tests unitarios (CsvSource) + integración (`MI 320`/`MI320` → "Mercedes-Benz Mi 320 Avantgarde 2020") en verde con `:decorator:test` (Java 17); CHANGELOG + bump a `0.0.3-new-title-motors`. Sigue: consumo en Search (Bloque B, depende de pendientes de caché/coverage) y decisión de mesa C1.
- **2026-07-09** — **Rumbo a PR (se descarta la caché).** Rodrigo revisó el diff y levantó 2 puntos de alcance: (1) el `SUBTITLE` se removió estructuralmente de `SingleNative*LayoutOrder` — debe **mantenerse** en el layout y suprimirse **solo para motors** (el componente es motors-only hoy pero lo usarán otras verticales); (2) el título lo usan TODAS las verticales pero solo se tocó motors → evaluar abstraer a helper/util (KISS/YAGNI). Ambos ajustes se delegaron a otra IA vía **prompt maestro** (SIN romper funcionalidad). `descripcion_pr.md` actualizado con la descripción acotada al impacto real. Bloque D creado.
- **2026-07-09** — Rodrigo commiteó v1 (`se agrega validación de info repetida`) y al probar encontró 2 casos: `Lexus Nx / Nx300h` y `Mercedes-Benz classe Clc / Clc200` (token de modelo es **prefijo** del de short version — inverso al caso `MI320`). **v2 (hardening):** regla unificada de subsunción de tokens en `mergeModelAndVersion` (reemplaza `removeRedundant`). **Barrido BQ del catálogo** (`LK_CATALOG_PRODUCTS_CARS_AND_VANS`, 12.910 combos): 549 (~4.25%) con repetición; reveló 2 falsos positivos que se corrigieron: (a) no descartar short version de 1 letra por contención coincidente (trims `L`/`S`/`M`: `Acura Legend / L`), (b) permitir reemplazo de letra sola del modelo solo si la versión sigue con dígito (`Classe C / C230` sí, `Clase A / AMG` no). **Test de invariante** `MotorsTitleDedupInvariantTest` alimentado por CSV de casos reales (`title_dedup_catalog_sample.csv`) = detección escalable. Bump a `0.0.5-new-title-motors` (0.0.4 era v1). `:decorator:test` completo en verde, 0 borrados. Sin commit.

- **2026-07-15** — Diff final acotado al título Motors, fallback `SHORT_VERSION/TRIM`, deduplicación, tests, documentación de ejemplo, changelog y versión de test `0.0.12-new-title-motors`. Los layouts compartidos y el contrato no cambian; Search omite `SUBTITLE` para la modalidad de título corto. PR del SDK en code review.

## 🔗 Docs / Links

- Iniciativa padre: [[Refactor Polycard]]
- Apps: [[java-polycard-sdk]] · [[search-middleware]]
- Dependencia de datos: [[2026-07-09-polycard-short-version-title-data-dependency]]
- SDK: `polycard-decorator/.../decoration/TitleDecorator.java` · `.../utils/AttributeUtils.java` (Motors)
- Rama: `feature/new-title-motors`
