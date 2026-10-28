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
start: 2026-10-27
due: 2026-12-31
progress: 0
repo: https://github.com/melisource/fury_rio-controlplane-clickhouse
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
created: 2026-10-27
updated: 2026-10-27
cssclasses:
  - wide
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

- Tener un **ClickHouse full** en RIO al 31-dic-2026: cada componente ClickHouse con su ciclo de vida completo, warehouse como componente y lectura con keys propias. Se hace con dos personas, construyendo tres piezas base reutilizables en vez de ítems aislados. Plan completo en [[Roadmap Q4 — CP ClickHouse]].

## 📊 Estado actual

- **2026-10-27 — Roadmap propuesto, pendiente de acordar con Flor.** Ocho entregables funcionales en dos lanes, ordenados por valor; cada uno es una capacidad usable en producción con su caso E2E. El código compartido entra como PR habilitante dentro del primer entregable que lo consume. Deprovision y start-stop de refreshable ya están en `master` (PR #346), y el import refreshable está desarrollado ([[Import de Refreshable Materialized Views externas]]). Detalle en [[Roadmap Q4 — CP ClickHouse]].

| Ventana | Rodrigo · vistas y credenciales | Flor · salud y warehouse |
|---|---|---|
| 27-oct → 7-nov | R1 Adoptar refreshable existentes | F1 Ver si mi refreshable falla |
| 10-nov → 21-nov | R2 Keys siempre vigentes | F2 Crear mi warehouse (→ 28-nov) |
| 24-nov → 12-dic | R3 Leer con mis keys | F3 Prender/apagar mi warehouse |
| 15-dic → 23-dic | R4 Vista normal (condicionado) | F4 Borrar mi warehouse |
| 24-dic → 31-dic | Hardening, rollout y release | Hardening, rollout y release |


## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

_Proyecto de planificación interno. Cada pieza tiene su documento de diseño dentro de este proyecto antes de implementarse; las specs del equipo que ya existen se enlazan sólo como referencia. Las ramas se agregan al iniciar cada ola._

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-controlplane-clickhouse]] · [[rio-playmaker]] · [[ads-signals-frontend]] | `feature/refreshable-view-import` | `develop` | [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700) | SIG-701 / SIG-702 / SIG-703 | R1; desarrollado, última prueba bloqueada por permisos |
| [[rio-controlplane-clickhouse]] | — | `develop` | — | [SIG-705](https://spellbook.adminml.com/projects/SIG/specs/SIG-705) | F2–F4; técnica en draft (Flor) |
| [[rio-controlplane-clickhouse]] · [[rio-playmaker]] | — | `develop` | — | Doc interno de diseño R2/R3 (por escribir) | R2 → 21-nov, R3 → 12-dic |
| [[rio-controlplane-clickhouse]] · [[rio-playmaker]] · [[ads-signals-frontend]] | — | `develop` | — | Doc interno de diseño R4 (por escribir) | R4 → 23-dic, condicionado |
| [[rio-controlplane-clickhouse]] · [[ads-signals-frontend]] | — | `develop` | — | Doc interno de diseño F1 (por escribir) | F1 → 7-nov |

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
> - [ ] Acordar el roadmap con Flor (orden por valor, lanes y las cinco decisiones del roadmap §8) #owner/me #type/admin #area/meli
> - [ ] Pedir a terceros: permiso de la última prueba, API key Cloud con escritura, contrato de aprobación RIO, credenciales de vistas existentes #owner/me #type/admin #area/meli
> - [ ] Traer los datos para validar el valor: cantidad de refreshable en prod y teams esperando warehouse #owner/me #type/research #area/meli
> - [ ] Actualizar la planilla: deprovision y start-stop refreshable → hechos #owner/me #type/admin #area/meli
> - [ ] R1 — Última prueba del import refreshable #owner/me #type/dev #area/meli #blocked
> - [ ] R1 — Push de Playmaker tras el merge de #1332 y gate Cleric #owner/me #type/dev #area/meli #waiting
> - [ ] R1 — Precarga de credenciales de las refreshable reales con sus owners #owner/me #type/admin #area/meli
> - [ ] R1 — Limpieza de KVS y KMS al borrar una vista importada #owner/me #type/dev #area/meli
> - [ ] R2 — Verificar si Playmaker conserva outputs previos cuando el CP no los reenvía #owner/me #type/research #area/meli
> - [ ] R2 — Keys siempre vigentes tras ALTER (PR habilitante: credencial única) #owner/me #type/dev #area/meli
> - [ ] R3 — Leer ClickHouse con keys propias (MVP de la lib) #owner/me #type/dev #area/meli
> - [ ] R4 — Query de demanda de vistas normales en prod #owner/me #type/research #area/meli
> - [ ] R4 — Vista normal provision/deprovision (PR habilitante: variante de vista), si hay demanda #owner/me #type/dev #area/meli

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
- **2026-10-27** — Backlog contrastado contra el código en `origin/develop` de CP, Playmaker y front; dos P0 resultaron ya entregados. Roadmap por olas documentado en [[Roadmap Q4 — CP ClickHouse]]. Se agregó la definición de ClickHouse full y dos huecos fuera del backlog; se quitó todo uso de Spellbook. El roadmap se reordenó por valor en ocho entregables funcionales (R1–R4, F1–F4) con una agenda para acordarlo con Flor.

## 🧭 Decisiones

_Salvo la primera, son propuestas a acordar con Flor._

- Definido por el owner: este proyecto y sus docs son internos (AGENTS OS); nada se crea en Spellbook.
- Propuesta: el roadmap se ordena por valor y cada entregable es una capacidad funcional en producción con caso E2E; los PRs habilitantes sólo entran si un entregable los consume en su misma ventana.
- Propuesta: dos lanes, Rodrigo con vistas y credenciales y Flor con salud y warehouse.
- Propuesta: lo último de cada lane (R4, F4) es lo primero que se recorta.
- Propuesta: descartar start-stop de vista normal; import de vista normal, import explícito de MergeTree, Dictionary, Control y multi-source quedan para Q1.


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
