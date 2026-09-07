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
start: 2026-08-18
due:
progress: 5
repo: ads-signals-knowledge-library
jira:
prs:
related:
  - "[[Onboarding Signals]]"
  - "[[ads-signals-knowledge-library]]"
  - "[[RIO]]"
aliases:
  - Signals Knowledge Harness
  - Harness de contribución Signals Knowledge
  - harness signals-knowledge
tags:
  - kind/project
  - area/meli
  - project/signals-knowledge-harness
created: "2026-08-18"
updated: "2026-09-01"
---

# Signals Knowledge Harness

%% Naming: Signals Knowledge Harness es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Signals Knowledge Harness
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P2 · **Tipo:** iniciativa de **cambio/delivery** (root)
> **Repo objetivo vigente:** [[ads-signals-knowledge-library]] (`~/fuentes/ads-signals-knowledge-library`) · **Comprensión asociada:** [[Onboarding Signals]] · **Plataforma:** [[RIO]]
> **Stakeholder / dueño:** **Carlos Montecinos** (`cmontecinos`, Software Expert — Advertising, mgr `vmilesi`) — **autor del bundle** (2026-08-18). **Relación ya establecida:** conversado varias veces; Carlos me contó del proyecto, sabe que soy nuevo y que quiero aportar aprovechando el onboarding, y ayer (2026-08-18/19) me confirmó que el repo está arriba. **Falta liviano:** confirmar punto de partida + convenciones antes del 1er PR (no hace falta "vender" nada); su visión de fondo la converso en corto.

> [!tip]+ Visión / el giro de valor
> No es "un harness de docs": es **cómo tomo `ads-signals-knowledge-library` y lo llevo a ser el "SecondBrain" vivo de la iniciativa Signals/RIO** — una base de conocimiento **consumible y contribuible por humanos y por agentes**, que se autogobierna y no driftea. Es la aplicación directa de lo que vengo haciendo con AGENTS OS / LLM Wiki, ahora **a escala de equipo**. Norte final: que el bundle deje de ser "documentación" y pase a ser **herramienta de contexto para agentes** de la iniciativa; y si el modelo prende, **escalarlo a toda la vertical Ads** como substrato de conocimiento compartido para todos sus agentes.

> [!note]- Alcance: delivery completo (no mezclar con onboarding)
> Este proyecto es **delivery** sobre [[ads-signals-knowledge-library]] en **tres frentes: contenido + harness + tooling** (todos parte del mismo esfuerzo). Lo que NO vive acá es el **discovery del dominio** (entender RIO/Signals): eso es [[Onboarding Signals]] + la Resource Wiki (`30-resources/`), que este proyecto **consume** como insumo. La separación es comprensión↔cambio, no un veto a contribuir contenido.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[Signals Knowledge Harness]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- **Tomar `ads-signals-knowledge-library` como oportunidad y llevarlo adelante:** definir *cómo abordo inicialmente el repo* y *qué hago yo* para convertirlo en el **SecondBrain vivo y agéntico de la iniciativa** — base de conocimiento consumible/contribuible por humanos y agentes, autogobernada. Ver Visión arriba.
- **Un solo delivery, tres frentes que se refuerzan:**
  - **Contenido** — validar/corregir lo que hay y aportar lo que ya tengo: capa **horizontal** ([[system-map]], [[integration-map]], journeys), **scopes** ([[scope-inventory]], naming), y completar stubs (`signals-catalog`/`signals-frontend`) desde mis fichas.
  - **Harness** — `AGENTS.md` + skills + **gobierno LLM Wiki** en el propio repo, para que cualquier dev/agente (con o sin AGENTS OS) contribuya alineado y termine en PR bien formado.
  - **Tooling** — **linter de links OKF** + [[rio-inspector]] con **check de drift** doc↔código, ambos como checks de CI (hoy el repo no tiene ninguno).
- **Por qué yo / por qué ahora:** es la continuación natural de mi trabajo con AGENTS OS/LLM Wiki; entro por **backend** (donde ya tengo evidencia de código), con el atlas horizontal como ventaja diferencial, y la contribución de contenido me da la credibilidad para empujar el gobierno.
- **Ambición escalable:** probar el modelo en Signals y, si prende, ofrecerlo como **herramienta de conocimiento para todos los agentes de la vertical Ads**.

## 📊 Estado actual

- **Reencuadrado (2026-08-18):** de "propuesta de harness" a *iniciativa de SecondBrain agéntico de Signals*; contenido + harness + tooling son parte del mismo proyecto (decisión del usuario).
- **Repo revisado a fondo:** ver la sección **🔎 Análisis del repo** (cobertura, gaps, delta, roadmap). Resumen: **RIO profundo y bien linkeado, 6 áreas stub, 0 gobierno/CI**; mi `rio-atlas` complementa casi exactamente sus gaps.
- **Pendiente inmediato:** (1) alinear visión + gap analysis con el **expert dueño del repo**; (2) arrancar por un quick win de alto respaldo (link-linter en CI y/o completar un stub desde mi vault).

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
> - [x] Inventariar el modelo de contribución actual de `ads-signals-knowledge-library` (AGENTS, estructura, gobierno, scripts, templates, CI/checks y convenciones) #owner/me #type/research #area/meli
> - [ ] Diseñar el `AGENTS.md` del repo: contrato de contribución (formato OKF, convenciones de `type`, links relativos, cómo abrir PR, gate pre-commit) descrito para agentes #owner/me #type/dev #area/meli
> - [ ] Definir el gobierno por **LLM Wiki** aplicado al repo (índice + log + provenance/freshness) para que la guía viva en el propio repo #owner/me #type/dev #area/meli
> - [ ] Diseñar el set de **skills portables** (sin dependencia de AGENTS OS): ingest de conocimiento nuevo, validación OKF, y apertura de PR alineado #owner/me #type/dev #area/meli
> - [ ] Empaquetar la **propuesta** (piezas + justificación desde experiencia AGENTS OS) y validarla con el equipo #owner/me #type/research #area/meli
> - [ ] **[Tooling]** Skill + check de CI: **linter del grafo de links OKF** (rotos/huérfanos/in-out-degree/hubs) — el repo hoy no tiene ninguna validación #owner/me #type/dev #area/meli
> - [ ] **[Tooling]** Portar [[rio-inspector]] como herramienta del repo: regenerar el Integration Map desde código/config y **check de drift** doc↔código en CI #owner/me #type/dev #area/meli
> - [ ] **[Contenido]** Completar los stubs `signals-catalog` y `signals-frontend` en OKF desde [[ads-signals-catalog]] / [[ads-signals-frontend]] #owner/me #type/dev #area/meli
> - [ ] **[Contenido]** Aportar la **capa horizontal** a `rio/architecture/`: system-map + integration-map (Mermaid) + secuencia de deploy, desde [[system-map]] / [[integration-map]] #owner/me #type/dev #area/meli
> - [ ] **[Contenido]** Aportar el área **scopes** (inventario + naming standard) desde [[scope-inventory]] / [[scope-naming-standard]] #owner/me #type/dev #area/meli
> - [ ] **[Colab]** Confirmar con Carlos el punto de partida + convenciones OKF antes del 1er PR (relación ya establecida; mensaje corto) #owner/me #type/research #area/meli

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
- **2026-08-18** — Creado el proyecto (iniciativa de cambio, `root: true`) al modelar [[signals-knowledge]] como external-resource. Objetivo: proponer la harness de contribución de agentes (AGENTS.md + skills + gobierno LLM Wiki) portable a devs sin AGENTS OS. Primer paso definido: inventariar el modelo de contribución actual del repo.
- **2026-08-19** — Stakeholder identificado: **Carlos Montecinos** (`cmontecinos`, Software Expert Advertising) es el **autor del bundle**. Definidos los 2 primeros focos del usuario: (1) **alinear con Carlos** (intención por confirmar), (2) **fuente única de verdad** — llevar el `rio-atlas` al repo para que sea contenido compartido y usable por todos. Decisión SSOT + flujo de graduación registrados. Pendiente: enviar el acercamiento a Carlos.
- **2026-08-18** — **Reencuadre del proyecto (usuario):** deja de ser "propuesta de harness" y pasa a ser *cómo abordo el repo y qué hago para tomar la oportunidad y llevarla adelante* → **SecondBrain agéntico de la iniciativa**, con contenido + harness + tooling como un mismo delivery, en conjunto con el **expert dueño del repo**, con ambición de escalar a la vertical Ads. Agregadas tareas de contenido y de colaboración; análisis del repo persistido.
- **2026-08-18** — Revisión inicial del repo (WIP inventario). **Estructura:** 21 `.md`; **RIO desarrollado** (9 services + 3 concepts + `rio-sdk-events` + hub `rio/index`), las **6 áreas restantes son stubs** de ~20 líneas que se autodeclaran `⚠️ Stub` con checklist "Por completar" (collector → repo `fury_ads-signals-collector-api`, Go). **Remote:** `melisource/fury_signals-knowledge` (Fury, `master`, 3 commits — nuevo). **Sin CI, sin validación OKF, sin `.pre-commit-config.yaml`.** **Grafo de links:** 98 links relativos, **0 rotos, 0 huérfanos**; hubs por in-degree (`rio/index` 14, `bigqueue-contract` 11, `playmaker`/`materializer` 9) = arquitectura real hub-and-spoke por BigQueue → **el bundle coincide con mi vault**. **Novedad vs mis notas:** modelo declarativo **SIG-186** (`DeploymentGroup`/`PipelineExecution`, `desired_state_hash`, tandas topológicas) + consolidación Materializer→Playmaker → candidato a contrastar/actualizar `rio-atlas`.
- **2026-09-01** — El repo objetivo fue reemplazado por [[ads-signals-knowledge-library]]. La nueva librería ya trae `AGENTS.md`, progressive disclosure, gobierno, scripts, catálogo y evaluaciones, por lo que el proyecto debe rebaselinar su backlog contra esas capacidades en vez de construirlas desde cero. Auditoría en [[Revisión de ads-signals-knowledge-library]].

## 🧭 Decisiones

- **Proyecto separado del onboarding (2026-08-18):** esto es *cambio/delivery*, no *comprensión*. Por la regla dura de no mezclar proyectos, va como iniciativa raíz propia; consume el entendimiento de [[Onboarding Signals]] y de la Resource Wiki, no lo lidera.
- **La guía vive en el repo, no en mi vault:** para que agentes de otros devs sin AGENTS OS contribuyan igual que los míos, el gobierno (LLM Wiki + AGENTS.md + skills) debe ser autónomo dentro de `ads-signals-knowledge-library`. Mi vault solo referencia el repo vía [[ads-signals-knowledge-library]].
- **Fuente única de verdad (2026-08-18, decisión del usuario):** para el conocimiento **curado y compartible** de RIO/Signals, el **repo `signals-knowledge` es la fuente canónica del equipo**. Mi `rio-atlas` deja de ser un fin en sí: es mi **banco de trabajo** que **gradúa** su contenido al repo vía PR. Flujo de graduación por página: (1) trabajo/pulo en el vault → (2) PR a OKF en el repo → (3) al mergear, **la verdad vive en el repo**; la página del vault se recorta a **puntero/nota personal** que enlaza a la página canónica del repo (no se mantiene una copia canónica paralela → evita drift, respeta "una fuente por hecho"). El vault conserva lo **privado/borrador**; lo curado es del repo.
- **Definición del proyecto (2026-08-18):** el norte es transformar el repo en el **SecondBrain agéntico de Signals** (herramienta de contexto para agentes), no solo documentarlo; el gobierno LLM Wiki + tooling es el mecanismo, la contribución de contenido es el bootstrap, y el trabajo es **con el expert dueño**, no en paralelo. Escalabilidad objetivo: substrato de conocimiento para todos los agentes de la vertical Ads.
- **Graphify NO se corre sobre el bundle (2026-08-18):** Graphify `update` es grafo AST de *código* por-repo; sobre un repo puro-Markdown no hay AST útil que extraer (grafo degenerado) y la capa semántica está parqueada (decisión Resource Wiki: para Markdown ganan tags + índice curado). Además **el bundle OKF ya es un grafo de links nativo, determinístico y sano** (98 links, 0 rotos/huérfanos) — mejor que cualquier derivado. Lo que la harness sí incorpora es un **linter del grafo de links** (rotos/huérfanos/in-out-degree/hubs, ~30 líneas de Python) como skill + check de CI. Graphify solo tendría sentido para navegar del bundle al código real, pero para eso ya están los `resource:` (URLs GitHub) en frontmatter + los grafos por-repo en `~/fuentes`.
- **Reemplazo de SSOT (2026-09-01):** [[ads-signals-knowledge-library]] supersede a [[signals-knowledge]] como knowledge compartida. Las decisiones históricas sobre el repo anterior quedan como provenance; todo delivery nuevo apunta a la librería vigente y debe respetar su regla código > library > wiki.

## 🔎 Análisis del repo — cobertura, gaps y oportunidades (2026-08-18)

- **Tipo de conocimiento presente:** estructural (qué es cada servicio + modelo de dominio), de **contrato** (topics BigQueue, mensajes, endpoints), **operacional/comportamiento** (idempotencia, ACK/NACK, CQRS, retry) y **temporal/migración** (SIG-186, gate `use-group`, deprecación Materializer). Alta fidelidad "desde código" (nombres reales de clases, handlers, keys KVS).
- **Presentación:** OKF Markdown + frontmatter YAML (`type/title/description/resource/tags/timestamp`) + links relativos. Prosa densa + tablas. **Sin diagramas** (0 Mermaid), casi sin código, sin `last_verified`/`confidence` (OKF solo tiene `timestamp`).
- **Cobertura sesgada:** RIO **profundo** (9 services + 3 concepts + SDK + hub); las **otras 6 áreas Signals son stubs** (catalog, collector, sdk-go, cli, migrator, frontend) que se autodeclaran `⚠️ Stub` con checklist "Por completar".
- **Gaps del repo:** (1) **capa horizontal** — no hay system-map, integration-map, journeys end-to-end ni diagramas; (2) **gobierno** — 0 CI, 0 validación OKF, sin freshness/confidence, sin OWNS/ownership, sin glossary; (3) **el "por qué"** — casi no hay decisiones/ADR/tradeoffs; (4) **la mitad no-RIO de Signals** apenas existe; (5) **scopes/naming** — cero.
- **Mi delta (lo que YO tengo y al repo le falta):** `rio-atlas/` horizontal — [[system-map]], [[integration-map]] (auto-generado), journeys [[deploy-request-path]]/[[deploy-component]], [[signals-context-flow]] (contrato params→outputs por CP); **scopes** ([[scope-inventory]] 87 scopes live, [[scope-naming-standard]], [[scope-compatibility-matrix]]); tooling [[rio-inspector]]; fichas profundas [[ads-signals-catalog]] y [[ads-signals-frontend]] (llenan 2 de 6 stubs ya); disciplina estable/volátil + provenance/confidence.
- **Roadmap de contribución (tiers):**
  - **Quick wins (días):** completar stubs `signals-catalog` y `signals-frontend` desde mis fichas; sembrar glossary; PR del **link-linter** en CI.
  - **Estructural (semanas):** aportar `rio/architecture/` (system-map + integration-map con Mermaid + secuencia de deploy); aportar área **scopes**; portar [[rio-inspector]] como tool del repo con **check de drift** en CI.
  - **Estratégico (el valor real):** la **harness** (AGENTS.md + skills + gobierno LLM Wiki + freshness/confidence + OWNS map + narrativa "how RIO works") que convierte el bundle de *snapshot de una persona* en *base de conocimiento viva y autogobernada del equipo*.
- **Validación cruzada:** el modelo RIO del repo **coincide** con mi vault (hub-and-spoke BigQueue, Playmaker orquestador, Materializer deprecando, Flink migrando). Enriquecimiento bidireccional: backportear a mi `rio-atlas` el detalle **SIG-186** (delta + tandas topológicas + `desired_state_hash`) que el repo documenta mejor.
- **Alcance (decisión del usuario, 2026-08-18):** los tres frentes — **contenido, harness y tooling** — son **parte de este proyecto**. No se separa la contribución de contenido: el proyecto es *cómo abordo el repo y qué hago para llevar la oportunidad adelante*, no solo la propuesta de la harness.

## 🔗 Docs / Links

- Repo objetivo (external-resource): [[ads-signals-knowledge-library]] · dominio `30-resources/knowledges/`
- Comprensión asociada: [[Onboarding Signals]] · Plataforma: [[RIO]]
- Patrón de gobierno: [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] · [[LLM Wiki]]
- Provenance del repo: [[ads-signals-knowledge-library-repo]]
- Spec OKF: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

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
