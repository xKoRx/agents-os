---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Bajo y Muy Bajo Precio]]"
sprint: A26Q2S7
start: 2026-07-01
due:
progress: 45
repo:
jira:
prs:
aliases:
  - RFC Hito 2 Destaques de Precio
  - RFC pricing motors continuidad
tags:
  - project
  - area/meli
  - feature/destaques-de-precio
created: "2026-07-01"
updated: "2026-07-03"
---

# RFC Destaques de Precio - Hito 2

%% Naming: RFC Destaques de Precio - Hito 2 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ RFC Destaques de Precio - Hito 2
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** A26Q2S7
> **Parent:** [[Bajo y Muy Bajo Precio]]

## 🎯 Objetivo

- Continuar y cerrar la redacción del RFC de Hito 2 (`sb-main/01_Projects/previous-price-motors/RFC Destaque de precio — Hito 2.md`) y sus specs técnicas asociadas (Search, VIP), manteniéndolos reconciliados contra las decisiones más recientes del equipo.
- No es un RFC nuevo desde cero: es continuidad del RFC ya existente (autor Rodrigo Jara, creado 2026-05-28), cuya última sección abierta era el pivot FIPE de MLB del 2026-06-30.
- Incorporar el rollout confirmado en **MLA y MLM** (decisión 2026-07-01) y el orden actualizado de despliegue (2026-07-03): MLA+MLM primero por disponibilidad del Sugeridor, luego resto de sites no-MLB en paralelo, y MLB como carril FIPE posterior.
- Mantener la bifurcación por site explícita en toda la documentación: MLB (FIPE, destaque único) vs sites no-MLB (Sugeridor 2.0, dos tiers), con implementación base común y condiciones de tageo por site.

## 📊 Estado actual

- **2026-07-01**: RFC (`rfc.md`) actualizado — tabla de alcance, madurez de Sugeridor por site, rollout propuesto y pendientes de definición ahora reflejan MLA+MLM confirmados (ya no "candidato"/"por confirmar" para MLM).
- **2026-07-03**: RFC (`rfc.md`) actualizado — el rollout queda secuenciado como MLA+MLM primero por disponibilidad de Sugeridor, resto de sites no-MLB después en paralelo, y MLB después de MLA+MLM como carril FIPE separado. También queda explícito que la implementación base es común y sólo cambian las condiciones de tageo por site.
- **2026-07-03**: RFC (`rfc.md`) actualizado con nueva iteración técnica — atributos mínimos y preferentemente booleanos quedan como pendiente; consumer de procesamiento debe escalar el flujo de Bajó de Precio y evaluar prioridad Hito 2 antes que Hito 1; se agrega pendiente de consumer de cambios de atributos; proceso masivo debe paginar y encolar al consumer común; observabilidad, experimentos y rollout operativo quedan `TBD`.
- **2026-07-03**: Corrección de target — el RFC correcto de Hito 2 es `RFC Destaque de precio — Hito 2.md`, no el `rfc.md` legacy. Se aplicó la iteración técnica al archivo correcto: atributos mínimos/booleanos pendientes, consumer común escalado desde Bajó de Precio, consumer de atributos, proceso masivo paginado y secciones Experimentos/Rollout/Observabilidad como `TBD`.
- **2026-07-01**: Specs técnicas de Search y VIP (`Destaques de Precio — Polycard Search — Spec Técnica Propuesta.md`, `Destaques de Precio — VIP — Spec Técnica Propuesta.md`) actualizadas para acotar explícitamente su alcance a MLA/MLM (flujo Sugeridor) y dejar fuera a MLB (flujo FIPE separado, documentado solo en el RFC).
- Las specs **funcionales** de Search/VIP no se tocaron: documentan el refinamiento histórico (2026-06-23) tal como se dijo en su momento; el estado vigente vive en el RFC y las specs técnicas.
- Pendiente real más grande: los puntos abiertos del pivot FIPE en MLB (fuente técnica del precio FIPE, rango de elegibilidad, lista marca/modelo/año de exclusión, wording, trigger de reproceso) siguen sin resolver — están listados en el RFC bajo "Puntos abiertos (MLB)" y "Pendientes de Definición".
- **2026-07-01**: Se migraron a Spellbook las specs técnicas de Search y VIP (flujo Sugeridor, MLA/MLM) como continuación de las specs funcionales que ya vivían ahí. Quedaron en `review` (no `ready_to_code`) porque siguen siendo propuestas con puntos abiertos — no implementación. Tasks de desarrollo preparadas localmente para import cuando cada spec sea aprobada. Ver sección Docs/Links.

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
> - [x] Actualizar RFC legacy (`rfc.md`) con rollout MLA+MLM confirmado #owner/agent #type/dev #area/meli
> - [x] Ajustar RFC legacy (`rfc.md`) con orden de despliegue 2026-07-03: MLA+MLM primero, resto de sites no-MLB en paralelo después, MLB como carril FIPE posterior #owner/agent #type/dev #area/meli
> - [x] Ajustar RFC legacy (`rfc.md`) con iteración técnica de atributos mínimos, consumer común escalado desde Bajó de Precio, consumer de atributos y proceso masivo paginado #owner/agent #type/dev #area/meli
> - [x] Corregir el RFC específico de Hito 2 (`RFC Destaque de precio — Hito 2.md`) con la iteración técnica correcta #owner/agent #type/dev #area/meli
> - [x] Actualizar spec técnica Search con alcance MLA/MLM y exclusión explícita de MLB #owner/agent #type/dev #area/meli
> - [x] Actualizar spec técnica VIP con alcance MLA/MLM y exclusión explícita de MLB #owner/agent #type/dev #area/meli
> - [ ] Confirmar con Producto/UX los puntos abiertos del pivot FIPE en MLB (rango de elegibilidad, wording, fuente técnica del precio FIPE) #owner/me #type/research #area/meli
> - [ ] Confirmar ETA de la lista marca/modelo/año de exclusión de MLB (a cargo del equipo) #owner/me #type/research #area/meli #waiting
> - [ ] Revisar si la validación de moderación/Producto que condicionaba el rollout de MLB sigue aplicando ahora que no depende de Sugeridor #owner/me #type/research #area/meli
> - [ ] Definir storage y mecanismo de trigger de reproceso para MLB (no depende del cambio de `origin` de Sugeridor) #owner/agent #type/research #area/meli
> - [ ] Cerrar RFC como versión estable una vez resueltos los puntos abiertos de MLB #owner/agent #type/dev #area/meli #blocked
> - [x] Crear en Spellbook las specs técnicas de Search y VIP (Sugeridor, MLA/MLM) como continuación de las specs funcionales existentes #owner/agent #type/dev #area/meli
> - [x] Preparar tasks de implementación de ambas specs técnicas (search/VIP) listas para import #owner/agent #type/dev #area/meli
> - [ ] Revisar y aprobar en Spellbook los 2 specs técnicos (Search `9b8e70ce-f46a-497b-9df7-4b1ab2c99208`, VIP `93d572e8-4d58-4876-8e1c-71653b58f035`) para pasarlos a `ready_to_code` #owner/me #type/research #area/meli
> - [ ] Importar las tasks preparadas a Spellbook una vez aprobados los specs técnicos #owner/agent #type/dev #area/meli #blocked

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner="agent";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, "🤖 Tareas del agente");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## 📆 Bitácora

- **2026-07-01** — Se crea este proyecto de agente como continuidad del RFC de Hito 2 (no es un RFC nuevo: el RFC ya existía desde 2026-05-28, con el pivot FIPE de MLB del 2026-06-30 como último cambio antes de esta sesión). Cambio nuevo de esta sesión: **rollout confirmado en MLA y MLM**. Se actualizó `rfc.md` y las specs técnicas de Search y VIP en `sb-main/01_Projects/previous-price-motors/` para reflejar esa confirmación y dejar explícito que MLB usa un flujo separado (FIPE) fuera de esos dos documentos técnicos. Las specs funcionales no se tocaron (quedan como registro histórico del refinamiento 2026-06-23). Nota importante de política: `sb-main` (Brain del squad) tiene una regla vigente que prohíbe RFC/specs locales — deberían vivir en Google Doc/Spellbook con solo el link en `brief.md`. Se decidió con el usuario mantener el RFC y specs en el archivo legacy local ya existente como excepción, en vez de migrar a Google Doc, porque esta sesión no cuenta con herramienta de Google Docs. Pendiente para el usuario: evaluar migración futura a la política vigente de `sb-main`.
- **2026-07-01** — Migración parcial ejecutada: las **specs técnicas** de Search y VIP (flujo Sugeridor 2.0, MLA/MLM) se crearon en Spellbook, resolviendo el pendiente de la sección Ideas de abajo. Se identificaron los proyectos Spellbook correctos vía `sb-main/03_Resources/config/nexus-config.json` (mapeo Nexus↔Spellbook): `VMDUPPER` (Upper Funnel) para Search y `VISMDMID` (Mid Funnel) para VIP. Contenido migrado 1:1 desde las "Spec Técnica Propuesta" locales, con el header `Funcional:` re-apuntado a la spec funcional real en Spellbook (`2513a123-bdfe-481d-98d0-f7bfb3d572fe` Search, `ddf10fe9-af96-4208-9eac-01bfb71abfe5` VIP) y linkeado como dependencia (`specs deps add`) — no como hijo, porque `specs children` está reservado a epics. Ambas specs quedan en `review`, no `ready_to_code`: siguen siendo propuesta técnica con puntos abiertos (§12 de cada doc), no implementación confirmada; no correspondía auto-aprobarlas solo para poder importar tasks. El RFC (`rfc.md`) sigue como excepción legacy local — esta sesión no migró RFC ni specs funcionales, solo las técnicas de Hito 2 que faltaban en Spellbook.
- **2026-07-03** — RFC legacy actualizado con el nuevo orden de despliegue pedido por el usuario: **MLA + MLM primero** porque la nueva versión del Sugeridor ya corre hace tiempo en ambos sites; luego **resto de sites no-MLB en paralelo**; y **MLB después de MLA/MLM** como carril separado de FIPE. Se reforzó en resumen, alcance, madurez por site, principios de diseño, proceso masivo, rollout propuesto y pendientes que la implementación base es común para todos los sites y que sólo cambian las condiciones de tageo por site.
- **2026-07-03** — Segunda iteración del RFC legacy: se corrige el diseño para tratar Hito 2 como evolución de Bajó de Precio. Atributos de item quedan como pendiente, mínimos y preferentemente booleanos/filtrables; se documenta que hay que sumar los atributos a la caché de Search API Go y conversar filtrabilidad con Search. El consumer de procesamiento debe ser único, reutilizar el flujo de cambios de precio existente, sumar consumer de cambios de atributos, y aplicar prioridad funcional: Bajo/Muy Bajo primero, Bajó de Precio segundo. El proceso masivo queda como orquestador paginado que encola items al consumer común. Observabilidad, experimentos y rollout operativo quedan `TBD`.
- **2026-07-03** — Corrección: el archivo que debe gobernar Hito 2 es `RFC Destaque de precio — Hito 2.md`. Se aplicó ahí la iteración técnica pedida por el usuario. El `rfc.md` legacy quedó como archivo separado y no debe tratarse como fuente principal del Hito 2.

## 🧭 Decisiones

- Se trata como continuación de un RFC existente, no como RFC nuevo — se preserva el historial y la numeración de hitos ya definida en `rfc.md`.
- Se mantiene el RFC y las specs técnicas en el archivo legacy local de `sb-main` (excepción a la política vigente de RFC/specs externos), por decisión explícita del usuario en esta sesión.
- Las specs técnicas de Search/VIP quedan acotadas a MLA/MLM (flujo Sugeridor); el flujo FIPE de MLB se documenta solo en el RFC hasta que se resuelvan sus puntos abiertos.
- El orden de despliegue vigente del RFC es: MLA+MLM primero, resto de sites no-MLB después en paralelo, MLB después de MLA+MLM como carril FIPE. La base de implementación debe ser común; la variación vive en condiciones/configuración de tageo.
- Hito 2 se documenta como evolución de Bajó de Precio: se debe escalar el consumer/procesamiento existente, no diseñar una línea paralela innecesaria. La prioridad funcional es Hito 2 antes que Hito 1.

## 🔗 Docs / Links

- RFC Hito 2: `file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/RFC%20Destaque%20de%20precio%20%E2%80%94%20Hito%202.md`
- Spellbook — Spec Técnica Search: proyecto `VMDUPPER` (Upper Funnel), spec `9b8e70ce-f46a-497b-9df7-4b1ab2c99208` (status: review)
- Spellbook — Spec Técnica VIP: proyecto `VISMDMID` (Mid Funnel), spec `93d572e8-4d58-4876-8e1c-71653b58f035` (status: review)
- Tasks preparadas (pendientes de import): `sb-main/01_Projects/previous-price-motors/tasks-destaques-precio-search.json`, `tasks-destaques-precio-vip.json`
- Spec Técnica Search — fuente local (legacy, migrada a Spellbook): `file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/Destaques de Precio — Polycard Search — Spec Técnica Propuesta.md`
- Spec Técnica VIP — fuente local (legacy, migrada a Spellbook): `file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/Destaques de Precio — VIP — Spec Técnica Propuesta.md`
- Proyecto padre: [[Bajo y Muy Bajo Precio]]

## 💡 Ideas

### Backlog de ideas

- Evaluar con el usuario si migrar el RFC/specs a Google Doc + Spellbook para cumplir la política vigente de `sb-main`, o mantener la excepción legacy de forma permanente.
- **Resuelto parcialmente 2026-07-01**: las specs técnicas de Hito 2 ya viven en Spellbook. Queda pendiente evaluar migrar también el RFC (a Google Doc) y crear el `brief.md` de la iniciativa en `sb-main/01_Projects/previous-price-motors/` con FM `spellbook_project_id`/`functional-spec`/`technical-spec` para cumplir totalmente la política — no se hizo en esta sesión porque no fue pedido explícitamente y es un cambio estructural más amplio del repo del squad.

### Motivos / principios

- Un RFC que fork­ea por site (MLB vs resto) debe dejar explícito en cada documento derivado a qué sites aplica, para evitar que un lector asuma cobertura total de Motors donde en realidad hay dos flujos distintos.

### Memoria pública / interna

- **Memoria pública:** ninguna promovida aún — el trabajo de esta sesión es actualización de Sistema 2 (RFC/specs), no un aprendizaje reusable nuevo.
- **Memoria interna:** ninguna registrada aún.
- **Motivo:** el valor de esta sesión está en el propio RFC actualizado, no en una heurística nueva de proceso.
