---
type: project
owner: me
root: false
cssclasses:
  - wide
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Destaques de Precio]]"
sprint: "[[A26Q2S7]]"
start:
due:
progress: 70
repo: vis-items-loader-tagging, java-polycard-sdk, search-middleware, vis-octopus-lib, vpp-backend
jira: VMDUPPER-5, VISMDMID-4
prs:
tags:
  - area/meli
  - kind/project
created: 2026-06-24
updated: 2026-07-25
---

# Bajó de Precio

> [!info]+ Bajó de Precio
> **Padre:** [[Destaques de Precio]] · **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** [[A26Q2S7]]
> Señal `PREVIOUS_PRICE` (label "BAJÓ DE PRECIO") en Search + VIP Motors MLB. Desarrollo en code review.

## 🎯 Objetivo

- Renderizar "BAJÓ DE PRECIO" en Search y VIP Motors MLB con gate experimental `vis/item-dropprice-motors`.

## 📊 Estado actual

- Los 5 componentes con desarrollo terminado, en **code review**.
- **vpp-backend** quedó actualizado en la rama `feature/bajo-de-precio-motors` con soporte de bajo de precio Motors en Price, layout Android/iOS y tracking de view; Maintenance Fee permanece con el comportamiento de `develop` para Real Estate.
- **vpp-backend PR #18471**: merge con `develop` resuelto localmente; `visLibVersion` actualizado a release estable `3.4.0`; duplicación de tests de Maintenance Fee y Price Marshaller corregida con `@ParameterizedTest`.
- En VPP se corrigieron los dos pendientes detectados en revisión: coverage de PR bajo el umbral y race-condition por mutación de modelos recibidos desde `Observable.zip`.
- Validación local registrada: tests focalizados de tracking/coverage y `./gradlew :jacocoTestReport` en verde.

## ✅ Tareas

%% Board adaptivo por owner (ver [[convenciones]]). Proyecto humano → muestra mis tareas y puentes; nunca tareas de agente. %%

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

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [x] Refinamiento #owner/me #type/research #area/meli
> - [x] Análisis #owner/me #type/research #area/meli
> - [x] Diseño #owner/me #type/research #area/meli
> - [x] Configuración de experimento (Growthbook `vis/item-dropprice-motors`) #owner/me #type/admin #area/meli
> - [r] [[vis-items-loader-tagging]] Implementación #owner/me #type/dev #area/meli #sprint/A26Q2S7 📅 2026-06-24
> - [x] [[java-polycard-sdk]] Implementación #owner/me #type/dev #area/meli #sprint/A26Q2S7 ✅ 2026-07-03
> - [x] [[search-middleware]] Implementación #owner/me #type/dev #area/meli #sprint/A26Q2S7 ✅ 2026-07-08
> - [x] [[vis-octopus-lib]] Implementación #owner/me #type/dev #area/meli #sprint/A26Q2S7 ✅ 2026-07-08
> - [r] [[vpp-backend]] Implementación #owner/me #type/dev #area/meli #sprint/A26Q2S7
> - [x] [[java-polycard-sdk]] Responder code review #owner/me #type/dev #area/meli #sprint/A26Q2S7 ⏫ 📅 2026-06-24 ✅ 2026-07-01
> - [x] [[search-middleware]] Responder code review #owner/me #type/dev #area/meli #sprint/A26Q2S7 ⏫ 📅 2026-06-24 ✅ 2026-07-01
> - [/] [[vpp-backend]] Responder code review y probar nueva versión #owner/me #type/dev #area/meli #sprint/A26Q2S7 ⏫ 📅 2026-06-24
> - [x] Reconciliar el RFC (Estado Implementado, Hito 1) con lo realmente implementado/desplegado por componente — gap detectado 2026-06-30 #owner/me #type/research #area/meli #sprint/A26Q2S7 ✅ 2026-07-08
> - [x] [[Search Middleware - Correccion Bajo de Precio Motors]] arrancar + seguimiento #owner/me #type/supervision #area/meli #sprint/A26Q2S7 ⏫ ✅ 2026-07-01
> - [/] [[Refactor Bajó de Precio VPP]] arrancar + seguimiento #owner/me #type/supervision #area/meli
> - [ ] [[vis-items-loader-tagging]] Crear/configurar el tópico y consumer de trabajo del backfill de Bajó de Precio Motors #owner/me #type/devops #area/meli

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes Bajó de Precio
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes Bajó de Precio
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes Bajó de Precio
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes Bajó de Precio
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-06-24** — 
- **2026-06-30** — [[search-middleware]]: corrección posterior de la sincronización de ramas. La rama `feature/bajo-de-precio-motors` fue reconstruida desde `origin/develop` aplicando solo el delta funcional de Bajo de Precio Motors, sin arrastrar commits/archivos de proximity/plugin/docs. Se publicó con `--force-with-lease` en el commit limpio `75b4e0f7901`, usando Polycard SDK publicado `8.179.0`. Tests acotados de Gradle pasaron.
- **2026-06-30** — Se detecta gap entre el RFC (sección Estado Implementado, Hito 1) y el estado real de implementación/despliegue de los componentes. Se crea tarea pendiente en este subproyecto para reconciliar. RFC reordenado en Hito 1 (Bajó de Precio) / Hito 2 (Destaques de Precio) para reflejar esta separación.
- **2026-07-01** — Se crea subproyecto [[Search Middleware - Correccion Bajo de Precio Motors]] para corregir regresión detectada por review: la rama actual cambió indebidamente reglas de Real Estate para proyectos `DEVELOPMENT`. Próxima sesión debe recuperar reglas RE, llevarlas a tests, refactorizar hacia `PriceDropExperimentHelper` y eliminar abstracciones innecesarias.
- **2026-07-01** — Corrección completada y validada por el agente en [[Search Middleware - Correccion Bajo de Precio Motors]]: regresión de RE `DEVELOPMENT` resuelta, `./gradlew test` completo en verde, diff más acotado (23 archivos vs 35 original). Tarea puente pasa a Review. Pendiente de ti: revisar el diff, responder GenAI Code Review, y decidir si commiteas/pusheas — el agente no tocó git.

- **2026-07-01** — [[vpp-backend]]: se documenta el estado efectivo del PR de Bajo de Precio Motors. El cambio integra `VisPriceDropMotorsTask` en Price, propaga `shouldShowPriceDropOriginalValue`/`priceDropPreviousPrice`, agrega `VisCouponSummary` al layout nativo Android/iOS, ajusta Maintenance Fee y tracking de `/vip`. También se agregaron tests para levantar el PR coverage y se corrigió el riesgo de race-condition copiando `VISItemTrackingInfoModel`/experiments antes de mutar datos derivados del `Observable.zip`. Validación local: tests focalizados y `./gradlew :jacocoTestReport` verdes. Pendiente para cierre de PR: evidencia funcional/nativa, Track Inspector/catalog si aplica y completar responsables/Jira/Figma si el equipo los requiere.
- **2026-07-08** — [[vpp-backend]] PR #18471: después de mergear `develop`, se resolvieron conflictos en `build.gradle`, `VipMotorsViewTrackingInfoTask` y su test. Ese merge reintrodujo Vehicle Reservation y duplicó estado de Maintenance Fee; ambas situaciones fueron identificadas posteriormente como regresiones ajenas a la iniciativa. `visLibVersion` quedó en `3.4.0` estable.
- **2026-07-09** — [[vpp-backend]]: review integral y correcciones completadas. Maintenance Fee volvió a `develop`; Vehicle Reservation fue eliminado; RE y Motors conservan tracking separado; Price resuelve primero la vertical y solo suscribe la tarea aplicable, proyectando un único `priceDropPreviousPrice`. Validación final: compilación, tests focales, `./gradlew test`, `archTest` y `pmdMain` exitosos. Sin stage, commit ni push.
- **2026-07-20** — Se crea el proyecto de agente [[Refactor Bajó de Precio VPP]] para trasladar a Octopus el nuevo componente/lógica Price Drop Motors, restaurar el Price core de VPP y conservar VPP como integración mínima. Incluye gates de arquitectura, matriz cross-vertical, prompt para IA pequeña y prohibición de modificar RE/deprecated.
- **2026-07-25** — [[vis-items-loader-tagging]]: implementado el backfill retroactivo de Bajó de Precio Motors. El handler encola un mensaje por ítem en un tópico de trabajo nuevo; el consumer reconstruye y valida la baja con `vis-items-history`, setea `PREVIOUS_PRICE` y agenda solo el tiempo restante. La expiración reutiliza el tópico productivo `BIGQUEUE_TOPIC_PRICEDROP_BADGE_EXPIRE_TOPIC_NAME` y `/consume-price-drop-calendar-cleanup`; se eliminó la primera versión que había creado un calendario paralelo. `go test ./...`, `go vet ./...`, `go build ./...` y race tests focalizados quedaron en verde. Pendiente humano: crear/configurar únicamente el tópico y consumer de trabajo.

## 🧭 Decisiones

- Search no filtra `CARS_AND_VANS`; gate compartido Search + VIP. VIP consume señal resuelta (no revalida).

## 🔗 Docs / Links

- [Spec Técnica Search](file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/VMDUPPER-tecnica-bajo-de-precio-search.md)
- [Spec Técnica VIP](file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/VISMDMID-tecnica-bajo-de-precio-vip.md)
