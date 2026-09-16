---
type: project
schema_version: 1
owner: me
root: true
status: archived
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-08-10
due:
progress: 65
repo:
jira:
prs:
aliases:
  - Onboarding Signals
  - Traspaso Signals
  - Onboarding RIO
tags:
  - area/meli
  - kind/project
  - project/onboarding-signals
created: 2026-08-10
updated: 2026-09-11
cssclasses:
  - wide
---

# Onboarding Signals

> [!info]+ Onboarding Signals
> **Área:** [[Meli]] · **Estado:** archived · **Prioridad:** P1
> **Plataforma:** [[RIO]] · **Workspace:** [[Fuentes — Workspace de repositorios]] · **Metodología:** [[data-mesh]]

## 🎯 Objetivo

- Comandar mi traspaso al equipo **Signals** llegando con rol de **Sr Software Engineer**: tener **mira global desde el minuto 1** de la plataforma [[RIO]] (10 apps), entender qué hace cada app, sus patrones, tecnologías y responsabilidades, y dejar todo como **contexto durable para mis agentes** (AGENTS OS).

## 📊 Estado actual

- **Archivado el 2026-09-11 por solicitud del owner.** El material se conserva como historial; no representa trabajo activo.

- **Documentación base lista:** entidad paraguas [[RIO]], metodología [[data-mesh]], índice operativo `~/fuentes/AGENTS.md`, y las **10 notas de app documentadas** (deep-dive desde código, corte estable/volátil, `confidence` por nota) en `30-resources/applications/`. Convención LLM Wiki codificada en Sistema 1.
- **Grafo analizado (2026-08-10):** `graphify-signals.json` tiene 0 aristas cross-repo; el acoplamiento real es hub-and-spoke por BigQueue (ver Decisiones/Bitácora).
- **Pendiente (discovery):** contrastar [[data-mesh]] con la implementación real, extraer contexto de los 3 canales de Slack, limpiar Mac y resolver el propósito de `rio-controlplane-signals`.

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] Mapear las 10 apps RIO y crear índice `~/fuentes/AGENTS.md` #owner/me #type/research #area/meli ✅ 2026-08-10
> - [x] Crear entidad paraguas [[RIO]] y nota de metodología [[data-mesh]] #owner/me #type/research #area/meli ✅ 2026-08-10
> - [x] Deep-dive de diseño de las 10 apps RIO (patrones, tech, responsabilidad, deps) y enriquecer cada nota de app con corte estable/volátil #owner/me #type/research #area/meli ✅ 2026-08-10
> - [x] Analizar el grafo mergeado `graphify-signals.json`: dependencias cross-app y acoplamiento real #owner/me #type/research #area/meli ✅ 2026-08-10
> - [x] **[Atlas 1]** System Map de RIO — diagrama único de la vista de 30s (quién recibe/orquesta/decide/ejecuta/habla con infra; async vs sync; dónde viven los contratos) #owner/me #type/research #area/meli ✅ 2026-08-10
> - [x] **[Atlas 2]** Integration Map **generado desde código/config** con `rio-inspector` → `rio-integrations.{json,md,mmd}` (producer/consumer/transport/contract/purpose/sync-async) #owner/me #type/research #area/meli ✅ 2026-08-10
> - [/] **[Atlas 3]** Journey end-to-end de una operación real (deploy component) → documentado en [[deploy-component]] (contrato de I/O as-is + dolor). Falta amplitud: auditar todos los handlers/CP (`HandlerRegistry`/`PusherEventRouter`, flink/kafka/clickhouse). Alimenta el proyecto [[Crear Context]]. #owner/me #type/research #area/meli
> - [ ] **[Atlas 4]** Contract Map de [[rio-sdk-events]] (eventos: produced/consumed by, campos, lifecycle, compat) #owner/me #type/research #area/meli
> - [ ] **[Atlas 5]** State / lifecycle model de un componente (desired vs actual, quién reconcilia, idempotencia) #owner/me #type/research #area/meli
> - [ ] **[Atlas 6]** Failure + retry model (DLQ, timeouts, doble consumo, result perdido, dónde miro) #owner/me #type/research #area/meli
> - [ ] **[Atlas 7]** Runtime / Observability Map (logs/metrics/traces/dashboards/alerts por app) #owner/me #type/research #area/meli
> - [ ] **[Atlas 8]** Glossary + App Cards con `OWNS` / `DOES NOT OWN` por app #owner/me #type/research #area/meli
> - [ ] **[Atlas 9]** Documento narrativo `How RIO Works` (5-10 pág) → candidato a contexto L1 de agentes #owner/me #type/research #area/meli
> - [x] **[Atlas · conformidad]** Re-materializar las notas del RIO Atlas vía `agents-os-entity-lifecycle`: [[00-index]] (`index`), [[system-map]]/[[integration-map]] (`resource`), [[rio-inspector]] (`tool`); `lint --strict` verde y gate GO (new=0). Descubribles por bootstrap. #owner/me #type/debt #area/meli ✅ 2026-08-10
> - [x] **[Atlas · deuda generador]** `rio-inspector` ahora emite [[integration-map]] como nota `resource` **conforme** y la escribe directo en el vault (idempotente, preserva `created`, pasa `lint --strict`); crudos json/mmd quedan fuera del vault. Drift eliminado. #owner/me #type/debt #area/meli ✅ 2026-08-10
> - [ ] Extraer contexto de los 3 canales de Slack para **validar/corregir** el modelo Atlas #owner/me #type/research #area/meli
> - [ ] Entender a fondo [[data-mesh]] y contrastarlo con la implementación real de RIO #owner/me #type/research #area/meli
> - [ ] Limpiar Mac (repos VIS viejos en `~/fuentes/vis`, `others/`, `vibe-coding/`, caches) — confirmar antes de borrar #owner/me #type/admin #area/meli
> - [ ] Resolver el warning de Nexus: `~/fuentes/second-brain/sb-main` no es repo git (`/nexus-setup`) #owner/me #type/admin #area/meli
> - [x] Eliminar el archivo vacío `SecondBrain/main/signals.md` de la raíz #owner/me #type/admin #area/meli ✅ 2026-09-03
> - [ ] Averiguar con el equipo para qué está reservado `rio-controlplane-signals` (repo scaffold Fury recién creado, sin renombrar; posible pieza nueva del roadmap) #owner/me #type/research #area/meli

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

## 💬 Slack — canales del equipo (contexto a extraer)

Fui agregado a 3 canales. **Pendiente extraer info** (último trabajo, dinámica de cada canal, decisiones) y registrarlo como notas de referencia para usar como contexto de agentes. Aún no leídos.

| Canal | Propósito (hipótesis) | Qué sacar |
|-------|-----------------------|-----------|
| `#ads-signals-foundation` | Canal base del equipo Signals (foundation/plataforma RIO) | Dinámica del día a día, dueños, decisiones técnicas |
| `#guild-room-of-elite` | Guild transversal (¿comunidad de práctica / seniors?) | Estándares, buenas prácticas, temas de guild |
| `#q3-pipeline-and-cps` | Pipeline Q3 + CPS | Roadmap Q3, prioridades, qué es "CPS" en este contexto |

## 📆 Bitácora

- **2026-08-18 (9)** — El equipo me pasó el repo **signals-knowledge** (`~/fuentes/signals-knowledge`): bundle **OKF** de conocimiento curado del equipo (RIO, catalog, collector, sdk-go, cli, migrator, frontend) — el **espejo canónico del equipo** de lo que yo vengo documentando. Modelado en el vault como **external-resource** en un dominio nuevo `30-resources/knowledges/` ([[signals-knowledge]] `type: resource` + [[signals-knowledge-repo]] `type: source` con repo+path relativo a `~/fuentes`; `00-index.md` + `log.md` del dominio). Me vuelvo **contribuidor** (backend → front → ingesta/collector); toda iniciativa de Signals debería terminar en un PR ahí. Creada la iniciativa de **cambio** [[Signals Knowledge Harness]] (separada de este onboarding por la regla de no mezclar comprensión↔cambio): proponer una harness (AGENTS.md + skills, gobierno LLM Wiki) para que agentes propios y de otros devs sin AGENTS OS contribuyan alineados.
- **2026-08-11 (8)** — Trazado end-to-end del **camino de un request de deploy** (front→playmaker→BigQueue→CP→result→`deployment.values`) documentado en la nueva journey [[deploy-request-path]] (RIO Atlas), con diagrama de secuencia + fork de ruteo. Hallazgos que **corrigen el modelo**: (a) el front nuevo dispara `POST .../pipeline/deploy` (pipeline-level); (b) el trigger viaja por **BigQueue `rio-deployment-trigger`** con entrega **HTTP push** al CP (no HTTP directo, como decía [[system-map]] — reconciliado); (c) **materializer solo se toca en el catch-all** `MATERIALIZER_REST` (catalog/signal + tipos no listados en `routingConfig`), no en el path moderno. Actualizados [[system-map]] (límites resueltos) y [[00-index]]. Cierra buena parte de la amplitud pendiente del Atlas 3.
- **2026-08-11 (7)** — Discovery del **flujo del contrato de componente (as-is)** trazado en código y documentado como conocimiento durable en [[deploy-component]] (RIO Atlas, Atlas 3 en WIP). Reforzado el modelo: el entendimiento vive en `30-resources/` (los proyectos son efímeros); [[Crear Context]] solo lo consume. Pendiente de amplitud: auditar el resto de handlers/CP.
- **2026-08-10 (6)** — Llegó la 1ª tarea real del equipo → creado el proyecto [[Crear Context]] (`root: true`, `owner: me`): llevar la definición de inputs/outputs de componente del front (properties) al backend, con [[rio-playmaker]] armando un `Context` que consumen los control planes. Materializa el tracer bullet del Atlas 3.
- **2026-08-10 (5)** — Conformidad + deuda del generador cerradas. Las 4 notas del Atlas ([[00-index]] `index`, [[system-map]]/[[integration-map]] `resource`, [[rio-inspector]] `tool`) re-materializadas vía `agents-os-entity-lifecycle`, `lint --strict` verde, gate GO (new=0), Graphify reindexado y descubribilidad validada por alias. `rio-inspector` corregido: ahora **escribe directo** la nota `resource` conforme [[integration-map]] en el vault (idempotente, preserva `created`), eliminando el drift; crudos json/mmd quedan fuera del vault (invariante 12).
- **2026-08-10 (4)** — Pivote a **visión horizontal (RIO Atlas)**: se re-prioriza el backlog de onboarding hacia vistas de sistema en vez de más deep-dives por app. Construida la herramienta `rio-inspector` (`~/fuentes/rio-inspector/inspect.py`) que genera `rio-integrations.{json,md,mmd}` desde config+código (19 integraciones, 13 contratos). Creado el Atlas en `30-resources/rio-atlas/` con [[system-map]] y [[integration-map]] (v1). **Corrección de modelo:** los triggers Playmaker→control planes van por **HTTP POST** (BigQueue solo fallback V1), no por BigQueue; los results/status sí por BigQueue async; Materializer se conecta por REST (Playmaker→Materializer, Materializer→control-planes/KMS) y por Fury Streams (`/v2/events`). Actualizada la nota [[RIO]] en consecuencia.
- **2026-08-10 (3)** — Análisis del grafo `graphify-signals.json` (41.629 nodos / 85.431 aristas). Hallazgo clave: **0 aristas cross-repo** — el grafo es la unión de 10 grafos AST por-repo; Graphify no resuelve el acoplamiento entre servicios. El acoplamiento real se reconstruyó desde configs/constantes: **hub-and-spoke por BigQueue** con [[rio-playmaker]] al centro (produce `rio-action-trigger`/`rio-deployment-trigger`; consume `rio-action-result`/`rio-deployment-result`/`rio-component-runtime-status`), control planes como consumidores de trigger + publicadores de result/status, [[rio-materializer]] como motor de ejecución (consume `ControlPlaneEvent`, llama infra real + [[rio-controlplane-kms]] por REST), [[rio-controlplane-kms]] es servicio REST síncrono (encrypt/decrypt) y [[rio-sdk-events]] es la librería de contratos compartida (acoplamiento en compile-time). Ver Decisiones.
- **2026-08-10 (2)** — Deep-dive LLM Wiki de las 10 apps RIO con 10 subagentes: cada nota reescrita con corte estable/volátil y evidencia de código. Hallazgos: [[rio-controlplane-signals]] en scaffold, [[rio-controlplane-fury]] es Kotlin, [[rio-materializer]] es el motor real de infra. Convención estable/volátil promovida a Sistema 1 (templates + wiki + perfil). Nexus (VIS) removido.
- **2026-08-10** — Bootstrap AGENTS OS. Mapeo de las 10 apps RIO (JVM/Spring/Fury), grafo global identificado. Creado `~/fuentes/AGENTS.md`, entidad [[RIO]] y nota [[data-mesh]] con digest del artículo de Fowler. Definido plan de onboarding y tareas.

## 🧭 Decisiones

- **Topología de acoplamiento (evidencia de código, 2026-08-10):** RIO es **hub-and-spoke por BigQueue**, no un grafo estático (Graphify da 0 aristas cross-repo). Flujo: [[rio-playmaker]] (orquestador/API) emite comandos `rio-*-trigger` → control planes ([[rio-controlplane-kafka]], [[rio-controlplane-flink]], [[rio-controlplane-clickhouse]], [[rio-controlplane-fury]], [[rio-controlplane-observability]]) ejecutan y devuelven `rio-*-result` + `rio-component-runtime-status` que Playmaker consume. [[rio-materializer]] es el motor de ejecución de infra (consume `ControlPlaneEvent`, integra AWS MSK/ClickHouse/BuildCloud y llama a [[rio-controlplane-kms]] por REST). [[rio-controlplane-kms]] NO usa BigQueue: es REST síncrono (`EncryptController`/`DecryptController`). [[rio-sdk-events]] es la librería de contratos de eventos (`ControlPlaneEvent`, `DeploymentEvent`, …) = único acoplamiento en compile-time. [[rio-controlplane-flink]] es el control plane más completo (trigger+result+runtime-status).
- **Nombres:** RIO = **Real time Input Output**; **Signals es el otro nombre de RIO** (equipo Signals = equipo RIO = equipo ADS). No es un sub-dominio: mi dominio como parte del equipo Signals **son las 10 apps RIO**. Ver [[RIO]].
- `rio-controlplane-signals` es hoy un **repo scaffold vacío** (placeholder), no una app real.
- Proyecto de onboarding bajo `10-projects/Meli/` (Signals se trata como equipo dentro del área [[Meli]], no como área propia).
- Entidades Sistema 2: nota paraguas [[RIO]] + una nota por app (ya scaffoldeadas); el deep-dive las enriquece.
- Slack: por ahora solo registrado como tarea/sección; la extracción de info es paso siguiente.

## 🔗 Ideas

- Revisar rutas de fury routes
- Inventario, naming y estándar de scopes → [[Estandarización de Scopes RIO]]
- revisar context
- revisar discovery

## 🔗 Docs / Links

- Proyecto derivado (1ª tarea real): [[Crear Context]]
- Proyecto derivado (scopes): [[Estandarización de Scopes RIO]]
- Proyecto derivado (harness de conocimiento): [[Signals Knowledge Harness]]
- Repo de conocimiento vigente del equipo (external-resource): [[ads-signals-knowledge-library]] · dominio `30-resources/knowledges/`
- Índice operativo del workspace: `~/fuentes/AGENTS.md`
- Plataforma: [[RIO]] · Metodología: [[data-mesh]]
- Workspace: [[Fuentes — Workspace de repositorios]]
- Artículo Fowler: https://martinfowler.com/articles/data-monolith-to-mesh.html
