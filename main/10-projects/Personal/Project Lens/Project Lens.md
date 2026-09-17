---
type: project
schema_version: 1
owner: me
root: true
cssclasses:
  - wide
status: active
priority: P2
area: "[[Personal]]"
parent:
sprint:
start: 2026-08-23
due:
progress: 0
repo:
jira:
prs:
aliases:
  - Vault Viewer
  - Obsidian viewer
  - project-lens
tags:
  - kind/project
  - area/personal
created: "2026-08-23"
updated: "2026-08-23"
---

# Project Lens

%% Naming: Project Lens es el link canónico del proyecto (nombre de trabajo); aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Project Lens
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P2 · **Sprint:** —
> Viewer local read-only del vault para usar en la pega, dado que MELI vetó Obsidian y con eso perdí la visibilidad de mis proyectos durante el día.

## 🎯 Objetivo

- Recuperar en la pega la parte del flujo que cubría Obsidian: navegar, leer, buscar y relacionar los `.md` del vault (proyectos, áreas, recursos, tareas, backlinks).
- No es un clon de Obsidian: es un viewer deliberadamente sin plugins, sin JavaScript dinámico y sin editor en v1. La edición sigue fuera del horario/herramienta vetada (VSCode + vault sincronizado).
- Los Markdown siguen siendo la base de datos; el índice es derivado, desechable y reconstruible.

## 📊 Estado actual

- **Discovery/diseño (2026-08-23)**: evaluada una primera propuesta de arquitectura (IA externa). Base candidata: binario Go con HTTP en localhost + SPA embebida vía `go:embed`, en tres capas — Core Vault (scan/parse/index) → Project Model (entidades, relaciones, tareas) → UI (explorer, viewer, dashboard, search, backlinks). Sin Electron, sin auto-update, sin runtime adicional; envoltorio desktop (Wails v3) diferido y opcional.
- **Hallazgo clave al mirar el vault real**: los tableros de proyectos y tareas dependen de Dataview/Bases (`dataviewjs`, checkboxes con `#owner/me #type/dev`, rollups en [[Panel de Proyectos]] y en cada proyecto). Un render Markdown plano mostraría esos bloques como código crudo y perdería justo el valor diario. El MVP necesita un subset server-side: índice de tareas (línea checkbox + tags), rollup de frontmatter de proyectos (area/priority/progress/status) y backlinks. Reencuadre útil: Project Lens ≈ reconstruir en Go el subset de Dataview que realmente uso, no "otro Obsidian".
- **Riesgo principal no técnico**: la política corporativa. Que MELI haya bloqueado Obsidian no implica que un binario compilado por mí esté permitido; podría ser cualquier software no aprobado. Validar esto antes de invertir horas serias.

### Preguntas abiertas

- ¿Qué prohíbe exactamente MELI: instalar software no aprobado en general, ejecutar extensiones/plugins, o algo más acotado? ¿Existe canal aprobado equivalente (web interna, navegador, contenedor)?
- ¿Dónde correrá: solo máquina personal, o también la corporativa? Esto decide si el objetivo real es un binario portable o algo tipo snapshot HTML estático sincronizado por canal aprobado.
- Nombre definitivo y repo (hoy "Project Lens" es nombre de trabajo).
- ¿Conviene exponer el Core Vault como servidor MCP para que los agentes consulten proyectos/backlinks/tareas? Sinergia directa con [[AGENTS OS]].

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

- [ ] Validar política corporativa MELI: qué está vetado exactamente y qué canales alternos existen #owner/me #type/research #area/personal
- [ ] Definir nombre canónico definitivo y crear repo (GitHub personal) #owner/me #type/admin #area/personal
- [ ] Diseño v0: contrato del modelo (Note, Frontmatter, Links, Tasks) y frontera Core Vault → Project Model → UI #owner/me #type/research #area/personal
- [ ] MVP v0.1: vault scanner + parser frontmatter + resolución de WikiLinks/backlinks + render Markdown read-only en localhost #owner/me #type/dev #area/personal
- [ ] Dashboard de proyectos: rollup por área/prioridad/progreso + índice de tareas con estados #owner/me #type/dev #area/personal
- [ ] Search v1: índice simple en memoria; FTS5/Bleve solo si el scan simple queda corto #owner/me #type/dev #area/personal

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

- **2026-08-23** — Creación del proyecto. Evaluada propuesta inicial de arquitectura (IA externa): Go + HTTP localhost + SPA embebida, sin plugins/editor en v1, markdown como base de datos. Aporte propio principal: el valor real está en replicar server-side el subset de Dataview/Bases que ya uso (tableros, rollups, backlinks), no en el render de markdown. Gate previo a desarrollar en serio: validar qué prohíbe la política de MELI.

## 🧭 Decisiones

- **2026-08-23** — Alcance v1 read-only: navegar/leer/buscar/relacionar. Sin plugin system, sin `eval()`, sin módulos remotos, sin URLs externas por defecto; superficie de privilegios mínima a propósito (es la razón por la que vetaron Obsidian).
- **2026-08-23** — Arquitectura: binario Go escuchando en `127.0.0.1` + SPA embebida con `go:embed`; sin Electron ni instaladores. Wails v3 queda como envoltorio opcional posterior.

## 🔗 Docs / Links

- Propuesta original evaluada (ChatGPT, 2026-08-23): resumen destilado en Estado actual y Decisiones; texto completo quedó en la conversación.
- Refs técnicas candidatas: goldmark (markdown), fsnotify (hot reload), SQLite FTS5 / Bleve (búsqueda full-text, diferido), Wails v3 (desktop, diferido).

## 💡 Ideas

### Backlog de ideas

- Exponer el Core Vault como servidor MCP: agentes consultando proyectos, tareas y backlinks del vault directamente.
- Graph view ligero (solo entidades proyecto/app/área) más adelante.
- Snapshot HTML estático exportable como plan B si la política corporativa no permite binarios propios.

### Motivos / principios

- Los Markdown son la base de datos; el índice es desechable y reconstruible.
- Read-only primero; Project Lens nunca compite con el editor.
- Sin plugins: eliminar la superficie exacta que motivó el veto.
