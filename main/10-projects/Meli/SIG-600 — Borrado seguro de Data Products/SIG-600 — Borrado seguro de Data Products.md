---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-09-28
due:
progress: 0
repo:
jira:
prs:
aliases:
  - SIG-600
  - Delete Data Products
  - Borrado de Data Products
  - SIG-643
entities:
  - "[[rio-playmaker]]"
  - "[[ads-signals-frontend]]"
related:
  - "[[RIO]]"
tags:
  - kind/project
  - area/meli
  - project/sig-600
created: "2026-09-28"
updated: "2026-09-28"
---

# SIG-600 — Borrado seguro de Data Products

%% Naming: SIG-600 — Borrado seguro de Data Products es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ SIG-600 — Borrado seguro de Data Products
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** —
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[SIG-600 — Borrado seguro de Data Products]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- Implementar el borrado seguro de Data Products de [SIG-600](https://spellbook.adminml.com/projects/SIG/specs/SIG-600): bloquearlo ante componentes activos en producción, importaciones pendientes o vigentes, y despliegues o infraestructura activa; mostrar una causa específica en el listado y en el detalle.
- Usar [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643) como diseño técnico. Playmaker valida dentro del `DELETE`; el frontend comparte modal y mensajes entre ambas entradas. La ejecución y el avance viven en este proyecto; los contratos viven en las SPECs.

## 📊 Estado actual

- **Autorización Playmaker en PR draft [#1228](https://github.com/melisource/fury_rio-playmaker/pull/1228), CI verde y [versión TEST `0.0.1-test-sig600-delete-auth`](https://web.furycloud.io/engineering/applications/rio-playmaker/versions/detail/0.0.1-test-sig600-delete-auth) terminada; CA-1 abierto.** SIG-600 (`review`) conserva su redacción original. SIG-643 (`draft`) asigna a Playmaker la autorización con Kraken `delete-data-products` o membresía del equipo dueño en ACME, con 403 si ninguna aplica y 503 cuando no se puede decidir. La rama usa el SDK Java oficial (`com.mercadolibre.library:kraken-client-java:5.0.0`) con LDAP extraído de Tiger. La regresión local pasó (4.037 tests, 0 fallas, 2 omitidos); el check LOCAL_STACK quedó bloqueado por falta de Docker. Queda por habilitar el access group de tráfico Fury a Kraken, revisar la dependencia con el MCP de seguridad (no disponible en esta sesión), retirar `requireDpOwnerRole` del proxy BFF para admitir usuarios Kraken-only, y alinear la visibilidad de la UI.
- SIG-600 CA-1 aún pide prevalidar antes del `DELETE`; SIG-643 valida dentro. También queda pendiente coordinar las rutas de deploy concurrentes y las demás reglas de bloqueo antes de considerar lista la iniciativa completa.

## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] | `feature/sig-600-delete-auth` · `/Users/rjara/fuentes/rio-playmaker-sig-600-delete-auth` | `origin/develop@c4ac43da4` | [SIG-600](https://spellbook.adminml.com/projects/SIG/specs/SIG-600) | [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643) | [PR draft #1228](https://github.com/melisource/fury_rio-playmaker/pull/1228), commit `73fabcfb9`; autorización Kraken OR ACME, 4.037 tests locales sin fallas, CI verde y [versión TEST](https://web.furycloud.io/engineering/applications/rio-playmaker/versions/detail/0.0.1-test-sig600-delete-auth) lista para desplegar; acceso Fury y revisión de seguridad pendientes; reglas de bloqueo restantes sin implementar |
| [[ads-signals-frontend]] | Pendiente de crear | `origin/master@791f79dd8` (baseline leído para SIG-643; base de trabajo por definir) | [SIG-600](https://spellbook.adminml.com/projects/SIG/specs/SIG-600) | [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643) | Retirar guard duplicado del proxy; CA-1 abierto; sin implementación |

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
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [ ] Resolver la discrepancia de CA-1 entre SIG-600 y SIG-643 antes de implementar #owner/me #type/admin #area/meli
> - [x] Confirmar SDK o API Java de Kraken para consultar `delete-data-products` con identidad Tiger #owner/me #type/research #area/meli ✅ 2026-09-29
> - [ ] Habilitar tráfico Fury de rio-playmaker a Kraken (`kraken_for_applications_external-kraken-all`) y revisar nueva dependencia con el MCP de seguridad #owner/me #type/admin #area/meli
> - [r] Implementar autorización Kraken OR ACME en Playmaker; [PR #1228](https://github.com/melisource/fury_rio-playmaker/pull/1228) en revisión y CI #owner/me #type/dev #area/meli
> - [x] Fijar precedencia de bloqueos, producción por `EnvironmentModel.type` y HTTP 409 con códigos #owner/me #type/admin #area/meli ✅ 2026-09-28
> - [ ] Relevar rutas de deploy que crean blockers, cerrar su protocolo transaccional y llevar SIG-643 a review #owner/me #type/research #area/meli
> - [/] Elegir branch y base actualizadas para Playmaker y frontend; Playmaker en `develop`, frontend pendiente #owner/me #type/dev #area/meli
> - [ ] Implementar en Playmaker los tres bloqueos, coordinar importaciones y rutas de deploy, y emitir códigos estables #owner/me #type/dev #area/meli
> - [ ] Propagar códigos en el BFF y compartir modal/flujo entre listado y detalle con resultado incierto separado de éxito #owner/me #type/dev #area/meli
> - [ ] Verificar los CA de SIG-600, el `DELETE` directo, permisos y ambas órdenes de carrera; preparar PRs #owner/me #type/dev #area/meli

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
- **2026-09-28** — Proyecto creado a partir de SIG-600 y SIG-643. Se actualizó SIG-643 con precedencia de bloqueos, HTTP 409, resultado incierto de UI y coordinación de importaciones. Una edición no solicitada de SIG-600 fue revertida y se verificó que su contenido volvió a coincidir exactamente con la versión anterior. Sigue abierta la discrepancia entre ambas SPECs y el protocolo de las rutas de deploy. No se creó branch ni se modificó código.
- **2026-09-28** — SIG-643 actualizada: Playmaker autoriza el borrado con permiso Kraken o membresía ACME, tras Tiger y antes de los bloqueos; falta de permiso devuelve 403. El guard ACME duplicado del proxy BFF debe retirarse para admitir Kraken. SIG-600 no se editó. Quedan abiertos CA-1, la integración Java de Kraken y la concurrencia de deploys.
- **2026-09-29** — Se creó un worktree aislado de Playmaker y se implementó la autorización del `DELETE` con el SDK Java oficial de Kraken 5.0.0 o grants ACME del equipo dueño. Se configuró sandbox para test/test2/test3/local y producción por defecto; `compileJava` y `compileTestJava` pasaron sin ejecutar tests. Pendiente habilitar acceso de tráfico Fury, revisar la dependencia con el MCP de seguridad y alinear BFF/UI. SIG-600 no se editó.
- **2026-09-29** — La rama se rebasó sobre `develop` y se abrió el [PR draft #1228](https://github.com/melisource/fury_rio-playmaker/pull/1228). Pasaron 4.037 tests locales, los cinco tests focalizados y ambos validadores de contrato; el health check LOCAL_STACK no pudo arrancar por falta de Docker. El primer intento contra `master` fue rechazado por el workflow de Fury y se corrigió la base a `develop`. CI quedó verde y Fury terminó la [versión TEST `0.0.1-test-sig600-delete-auth`](https://web.furycloud.io/engineering/applications/rio-playmaker/versions/detail/0.0.1-test-sig600-delete-auth) del commit `73fabcfb9`; aún no se desplegó.

## 🧭 Decisiones

- Playmaker es la autoridad de las reglas de borrado en el `DELETE`; no se diseña un endpoint `delete-validation`. Los blockers responden HTTP 409 con código específico y prevalece producción sobre infraestructura activa cuando aplican ambas. Fuente: [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643).
- Playmaker también es la autoridad de permisos para el borrado: Kraken `delete-data-products` o membresía ACME; 401 sin autenticación, 403 sin autorización, 503 cuando no se puede verificar. Fuente: [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643).
- Esta es una iniciativa humana (`owner: me`, `root: true`) de dos repos. La rama Playmaker parte de `origin/develop@c4ac43da4`; la rama frontend sigue pendiente.

## 🔗 Docs / Links

- [SIG-600 — funcional](https://spellbook.adminml.com/projects/SIG/specs/SIG-600) · [SIG-643 — técnica](https://spellbook.adminml.com/projects/SIG/specs/SIG-643)
- Aplicaciones: [[rio-playmaker]], [[ads-signals-frontend]]; plataforma: [[RIO]].

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

_Sin ideas registradas._

### Motivos / principios

_Sin motivos adicionales._

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
_No aplica para esta iniciativa._
