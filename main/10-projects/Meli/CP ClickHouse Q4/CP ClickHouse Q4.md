---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P0
area: "[[Meli]]"
parent:
sprint:
start: "2026-10-27"
due: "2026-12-31"
progress: 0
repo: "https://github.com/melisource/fury_rio-controlplane-clickhouse"
jira:
prs:
aliases:
  - CP Clickhouse Q4
  - ClickHouse Q4
  - Backlog ClickHouse Q4
tags:
  - kind/project
  - area/meli
  - app/rio-controlplane-clickhouse
created: "2026-10-27"
updated: "2026-10-27"
---

# CP ClickHouse Q4

%% Naming: CP ClickHouse Q4 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ CP ClickHouse Q4
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P0 · **Sprint:** — · **Equipo:** Rodrigo Jara + Florencia Sicre
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[CP ClickHouse Q4]] arrancar + seguimiento #owner/me #type/supervision #area/personal`

## 🎯 Objetivo

- Entregar en Q4 2026 los P0 del backlog de ClickHouse (refreshable, credenciales, Context v2 y warehouse) con dos personas, construyendo tres piezas base reutilizables en vez de ítems aislados. Plan completo en [[Roadmap Q4 — CP ClickHouse]].

## 📊 Estado actual

- **2026-10-27 — Roadmap propuesto, pendiente de validar con Flor.** El backlog está desactualizado: deprovision y start-stop de refreshable ya están en `master` (PR #346, release `202610.21.1`) en CP, Playmaker y front. Import refreshable está desarrollado y espera la última prueba por permisos ([[Import de Refreshable Materialized Views externas]]). Warehouse PROVISION tiene técnica en draft ([SIG-705](https://spellbook.adminml.com/projects/SIG/specs/SIG-705)). El resto se ordena en olas sobre tres piezas base: ciclo de vida de vistas, credenciales y cliente de escritura de ClickHouse Cloud.

| Pieza / lane | Owner | Ítems que destraba | Ola |
|---|---|---|---|
| Credenciales | Rodrigo | Context v2 sin duplicidad, credenciales import RMV, deprovision de importadas, lib de consumo | 1-2 |
| Ciclo de vida de vistas | Rodrigo | Vista normal provision/deprovision/import, base de multi-source | 2 (con gate de demanda) |
| Cliente Cloud de escritura | Flor | Warehouse provision, start-stop, deprovision | 1-2 |

## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

_Proyecto de planificación: cada ola se entrega como proyecto o rama propia con sus SPEC. La tabla registra los frentes conocidos; las ramas se agregan al especificar._

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-controlplane-clickhouse]] · [[rio-playmaker]] · [[ads-signals-frontend]] | `feature/refreshable-view-import` | `develop` | [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700) | SIG-701 / SIG-702 / SIG-703 | Desarrollado; última prueba bloqueada por permisos |
| [[rio-controlplane-clickhouse]] | — | `develop` | — | [SIG-705](https://spellbook.adminml.com/projects/SIG/specs/SIG-705) | Técnica en draft (Flor) |
| [[rio-controlplane-clickhouse]] | — | `develop` | Por escribir (épico credenciales) | Por escribir | Ola 1 |
| [[rio-controlplane-clickhouse]] · [[rio-playmaker]] · [[ads-signals-frontend]] | — | `develop` | Por escribir (épico vistas) | Por escribir | Ola 2, sujeto a demanda |

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
> - [ ] Validar el roadmap con Flor y actualizar la planilla (deprovision y start-stop refreshable → hechos) #owner/me #type/admin #area/meli
> - [ ] Ola 0 — Conseguir el permiso para la última prueba del import refreshable #owner/me #type/admin #area/meli #blocked
> - [ ] Ola 0 — Push de Playmaker del import tras el merge de #1332 y gate Cleric #owner/me #type/dev #area/meli #waiting
> - [ ] Ola 0 — Campaña de credenciales de refreshable existentes (inventario de DEFINER + gestión con owners) #owner/me #type/admin #area/meli
> - [ ] Ola 0 — Query dirigida de vistas normales en prod para el gate de demanda #owner/me #type/research #area/meli
> - [ ] Ola 0 — Decidir con Flor los permisos mínimos de admin del CP y de la API key Cloud #owner/me #type/research #area/meli
> - [ ] Ola 0 — Verificar si Playmaker conserva outputs de la versión anterior cuando el CP no los re-envía #owner/me #type/research #area/meli
> - [ ] Ola 1 — Pieza credenciales: Context v2 sin duplicidad (MergeTree, MV, RMV) #owner/me #type/dev #area/meli
> - [ ] Ola 1 — Revocación de credenciales al deprovisionar vistas importadas (KVS + KMS) #owner/me #type/dev #area/meli
> - [ ] Ola 1 — Spec de la lib de consumo de permisos #owner/me #type/dev #area/meli
> - [ ] Ola 2 — MVP de la lib de consumo de permisos #owner/me #type/dev #area/meli
> - [ ] Ola 2 — Vista normal provision/deprovision sobre la pieza de vistas (si hay demanda) #owner/me #type/dev #area/meli
> - [ ] Ola 3 — Spike de diseño multi-source (documento, sin código) #owner/me #type/research #area/meli

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
const pages=dv.pages('"10-projects/Meli/CP ClickHouse Q4"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-10-27** — Backlog contrastado contra el código en `origin/develop` de CP, Playmaker y front; dos P0 resultaron ya entregados. Roadmap por olas documentado en [[Roadmap Q4 — CP ClickHouse]].

## 🧭 Decisiones

_Propuestas de este roadmap; ninguna está acordada todavía con el equipo._

- Propuesta: dos lanes (Rodrigo vistas + credenciales en SQL; Flor warehouse en API Cloud) para no tocar los mismos archivos.
- Propuesta: descartar start-stop de vista normal por falta de semántica de negocio.
- Propuesta: vista normal entra a Q4 sólo si la query de prod muestra demanda.
- Propuesta: multi-source, Dictionary y Control salen de Q4; multi-source queda como spike de diseño.

## 🔗 Docs / Links

- [[Roadmap Q4 — CP ClickHouse]] — diagnóstico, piezas base, olas, riesgos.
- [[Import de Refreshable Materialized Views externas]] — entrega en curso del import.
- [[Plan de implementación — Context en ClickHouse]] — diseño previo de Context en el CP.
- [Planilla del backlog](https://docs.google.com/spreadsheets/d/1x5Wv9Wn1j0mkyycsN5X3L8d7r4PZSCpzqo5mhDMqjy4/edit?gid=1985317832#gid=1985317832)
- [SIG-705 Warehouse-programatic](https://spellbook.adminml.com/projects/SIG/specs/SIG-705) · [SIG-640 Refreshable](https://spellbook.adminml.com/projects/SIG/specs/SIG-640) · [SIG-700 Import refreshable](https://spellbook.adminml.com/projects/SIG/specs/SIG-700)

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
