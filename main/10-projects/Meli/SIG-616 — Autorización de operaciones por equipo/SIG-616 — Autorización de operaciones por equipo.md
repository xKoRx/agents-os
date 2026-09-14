---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P2
area: "[[Meli]]"
parent:
sprint:
start: 2026-09-14
due:
progress: 0
repo: https://github.com/melisource/fury_rio-playmaker
jira:
prs:
aliases:
  - SIG-616
  - Autorización por equipo en Playmaker
tags:
  - kind/project
  - area/meli
created: "2026-09-14"
updated: "2026-09-14"
---

# SIG-616 — Autorización de operaciones por equipo

%% Naming: SIG-616 — Autorización de operaciones por equipo es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ SIG-616 — Autorización de operaciones por equipo
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P2 · **Sprint:** —
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[SIG-616 — Autorización de operaciones por equipo]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- Diseñar e implementar la autorización server-side de operaciones de componentes por equipo en `rio-playmaker`, tomando como referencia [SIG-616 en Spellbook](https://spellbook.adminml.com/projects/SIG/specs/SIG-616).
- Asegurar que Playmaker autorice con identidad Tiger validada, ownership persistido del Data Product y rol ACME; el cambio debe ser reutilizable en actions, deployments y demás mutaciones sin trasladar esa responsabilidad a los control planes.

## 📊 Estado actual

- **Fase actual:** diseño previo y análisis de casos; no se modificó código ni se crearon tasks de implementación.
- La arquitectura y las decisiones vigentes están consolidadas en [[Diseño previo — Autorización de operaciones por equipo]]. Primero se cerrará ese diseño; después se crearán la SPEC técnica de Actions Signals y sus tasks en Spellbook.
- La SPEC menciona todas las mutaciones y actions de componentes, no sólo actions. En Spellbook está clasificada como `technical`, aunque fue presentada como funcional: confirmar si falta el funcional antes de implementar.
- El ownership vive en `DataProduct.teamName`; los componentes pertenecen a un Data Product. Un componente importado conserva su DP local y señala su procedencia mediante `sourceComponentId`.
- La primera vertical se limita a Actions component-bound de Signals: `catalog-signal + start/stop`. Legacy, otras tecnologías, precreation, polling, deployments y otras mutaciones quedan fuera de esa entrega.
- El [PR 1126](https://github.com/melisource/fury_rio-playmaker/pull/1126) aporta la consulta ACME y casos de autorización para delete/inactivate; se refactorizará progresivamente para converger al mecanismo común, sin adoptar `PipelineAuthorizationService.assertAdminAccess` como contrato transversal definitivo.

## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `rio-playmaker` | Pendiente | Pendiente | Pendiente de confirmar o reclasificar; SIG-616 figura como técnica en Spellbook | Pendiente de crear: Actions mutantes de Signals | Diseño previo; no implementar hasta aprobar SPEC funcional, técnica y tasks |

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
> - [/] Pulir [[Diseño previo — Autorización de operaciones por equipo]] y cerrar los gates de Actions Signals #owner/me #type/research #area/meli
> - [ ] Confirmar `catalog-signal + start/stop`, roles ACME, importados y ausencia de precreation con los dueños del flujo #owner/me #type/research #area/meli
> - [ ] Confirmar o corregir la relación funcional/técnica de SIG-616 en Spellbook #owner/me #type/dev #area/meli
> - [ ] Crear y aprobar la SPEC técnica de Actions mutantes de Signals #owner/me #type/dev #area/meli #blocked
> - [ ] Derivar y aprobar las tasks de la SPEC técnica en Spellbook #owner/me #type/dev #area/meli #blocked
> - [ ] Definir branch/base limpias y comenzar implementación sólo después de SPECs + tasks #owner/me #type/dev #area/meli #blocked

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

%% Rollup de iniciativa — descomentar solo en proyectos padre para ver las tareas #owner/me (incluye puentes) de todos los subproyectos, agrupadas por nota. Cambiar la ruta por la carpeta de esta iniciativa. Nunca muestra tareas de agente.
```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
const pages=dv.pages('"10-projects/CARPETA-DE-LA-INICIATIVA"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-09-14** — Se revisó SIG-616 y el código de Playmaker. Se acordó iniciar por el diseño de autorización reusable antes de tocar rutas o control planes.
- **2026-09-14** — Se acotó la primera vertical a `catalog-signal + start/stop`; se eligieron Tiger filter + interceptor ACME configurable sobre el endpoint component-bound, se excluyeron legacy/precreation/polling y se documentó el refactor evolutivo del PR 1126.

## 🧭 Decisiones

- **D1 — Primera vertical sólo Signals.** La primera implementación protege `catalog-signal + start/stop` sobre componentes existentes; no incluye legacy, otras tecnologías, precreation ni polling.
- **D2 — Dos capas HTTP con responsabilidades distintas.** Tiger se valida una vez en el filtro y publica username; un interceptor específico reconoce Signals, resuelve ownership persistido y consulta ACME antes del controller.
- **D3 — Whitelist de tipo + Action.** Una Action desconocida sobre `catalog-signal` se rechaza; tecnologías fuera del alcance conservan su comportamiento hasta contar con SPEC propia.
- **D4 — Services sin llamadas de seguridad externas.** Actions consume identidad desde `SecurityContext` y ejecuta el caso de uso sólo después de superar ambos middlewares.
- **D5 — PR 1126 converge por refactor.** Se reutiliza `AcmeClient.getOwnerProjectGrants`; la API acoplada a pipeline y la política estática se refactorizan a medida que se incorporan casos reales.
- **D6 — Annotation al final, no ahora.** `@RequiresCapability` se evaluará sobre services cuando exista repetición comprobada; queda documentada como evolución final y fuera de alcance inicial.
- **D7 — Playmaker es el enforcement point.** Los CPs siguen procesando eventos defensivamente, pero no resuelven Tiger ni ACME; reciben sólo requests ya autorizados por Playmaker.
- **D8 — SPECs y tasks antes de código.** Se cierra diseño, se valida la SPEC funcional, se crea la técnica por vertical y se aprueban sus tasks antes de definir branch/base e implementar.

## 🔗 Docs / Links

- [SIG-616 — Spellbook](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
- [[Diseño previo — Autorización de operaciones por equipo]]
- [PR 1126 — Autorización ACME para inactivate/delete](https://github.com/melisource/fury_rio-playmaker/pull/1126)
- [DataProductModel — `teamName`](file:///Users/rjara/fuentes/rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/model/DataProductModel.java)
- [ComponentModel — `dataProduct` y `sourceComponentId`](file:///Users/rjara/fuentes/rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/model/ComponentModel.java)

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

-

### Motivos / principios

-

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:**
- **Memoria interna:**
- **Motivo:**
