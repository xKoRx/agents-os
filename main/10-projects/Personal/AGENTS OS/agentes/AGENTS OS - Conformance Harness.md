---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start: 2026-09-12
due:
progress: 100
repo:
jira:
prs:
aliases:
  - Agents OS Conformance Harness
  - Conformance Harness
tags:
  - kind/project
  - area/personal
  - project/agents-os
created: "2026-09-12"
updated: "2026-09-13"
---

# AGENTS OS - Conformance Harness

%% Naming: AGENTS OS - Conformance Harness es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ AGENTS OS - Conformance Harness
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P2 · **Sprint:** —
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[AGENTS OS - Conformance Harness]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- Construir un **conformance harness** ejecutable localmente que demuestre automáticamente que Agents-OS cumple sus contratos actuales (bootstrap, cold/warm, entity switch, domain gates MELI/ARANEA/DEFAULT, skills routing, exclusión de deprecated/superseded, minimal context loading, ausencia de leakage entre scopes) con evidencia reproducible, sin rediseñar el sistema.

## 📊 Estado actual

- **Entregado y verificado (2026-09-13):** harness operativo en `80-agents/tools/conformance-harness/` (entrypoint `agents_os_conformance.py` + `rules.py` + `README.md`), L0/L1/L2 implementados, adversarial verification en 2 rondas con defectos corregidos (máx 2 ciclos respetado). Full run gated: `PASS 4 · FAIL 1 · WARN 4 · SKIP 17`; matriz por escenario: 16 PASS + 1 FAIL (hallazgo real del sistema) + 8 WARN (ambigüedades declaradas) + L2 PASS. Comando: `python3 80-agents/tools/conformance-harness/agents_os_conformance.py [--layer|--scenario|--json|--no-live]`.
- **Baseline de contexto capturado (baseline-only):** always-load ≈ 6.878 tok · pack meli ≈ 2.017 tok · pack aranea ≈ 1.197 tok (chars/4, sin tokenizador de autoridad).

## 🚨 Findings sobre Agents-OS (registrados, NO auto-corregidos)

- **F1 — MEDIUM — Conformance failure demostrada (C17):** `validate_schema_contract.py` en rojo (`errors=1`): "creation entrypoint bypasses materializer: 80-agents/skills/agents-os-skill-authoring/SKILL.md" — la skill está declarada como creation entrypoint en schema-contract.md pero no referencia `materialize_schema_note.py`. Escenario: SCHEMA-VALIDATOR-GREEN (L0). Estado observado verde al 2026-09-09 (nota cockpit); drift posterior del corpus. Acción recomendada: decidir owner — referenciar el materializador en la skill o retirar la declaración de entrypoint; re-verde antes de confiar en el gate.
- **F2 — WARN — Ambigüedad contractual DEFAULT (C10, Hallazgo 6):** la cláusula de evidencia de superficie del paso 6 no distingue evidencia ambiental (MCPs aranea-* siempre conectados a nivel máquina) de evidencia de tarea; puede colapsar DEFAULT→ARANEA. Escenarios: COLD-DEFAULT, SESSION-SURFACE-EXPOSURE. Acción recomendada: ADR que fije la lectura; hasta entonces el harness la registra como WARN.
- **F3 — WARN — Vocabulario load_policy sin árbitro (C09, Hallazgos 7/11/12):** tres enumeraciones coexisten (constitución `when_*_loaded|manual`; bootstrap lista 4; uso real incluye `when_area_loaded`, `when_echo_forge_loaded`, `when_entity_loaded`, `when_installing_graphify_obsidian`); nota VPN `when_area_loaded` sin campo `area`; 3 notas activas con `area: "[[Echo Forge]]"` no canónica. Escenario: LOAD-POLICY-VOCABULARY, ACTIVE-MEMORY-DOMAIN-PURITY. Acción recomendada: unificar vocabulario por ADR y normalizar `area`.
- **F4 — LOW — Redacción ambigua en memoria interna:** `80-agents/memory/internal/agent-memory/2026-09-04-echo-forge-c3-0290-mt5-build-blocked.md:38` registra UUIDs consumidos tras la palabra "token" (identificador vs credencial). Escenario: NO-SECRETS-IN-MARKDOWN (WARN, 0 valores con forma de credencial). Acción recomendada: rewording en la próxima pasada de memoria.

## 🧩 Artifacts

- `80-agents/tools/conformance-harness/artifacts/contract-audit.md` (C01-C17) · `domain-isolation-audit.md` (17 hallazgos) · `conformance-scenarios.md` (25 escenarios) · `conformance-spec-v1.md` (test model) · `adversarial-verification.md` (ronda 1) · `adversarial-verification-r2.md` (ronda 2).
- Artifacts y código del harness en `80-agents/tools/conformance-harness/` (audits, scenarios, spec, resultados de runs).

## 🧱 Entrega de desarrollo

_No aplica — el harness vive como scripts/tests dentro del vault bajo `40-archive/agents-os-conformance-harness/`; no toca repos de aplicaciones._

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
> - [x] T1 — Auditorías A/B/C: contract-audit (C01-C17), domain-isolation-audit (17 hallazgos), conformance-scenarios (25 escenarios) #owner/agent #type/research #area/personal
> - [x] T2 — Reconciliación parent → conformance-spec-v1 (test model V1) #owner/agent #type/research #area/personal
> - [x] T3 — Harness Implementer subagent → entrypoint L0/L1/L2 #owner/agent #type/dev #area/personal
> - [x] T4 — Suite ejecutada y reproducible: full-run gated (PASS 3/FAIL 1/WARN 4/SKIP 17) + matriz individual (16 PASS/1 FAIL/8 WARN) #owner/agent #type/dev #area/personal
> - [x] T5 — Adversarial Verifier fresco + correcciones derivadas (ronda 1: D1/D2/D3; ronda 2: N1/N2/N3) #owner/agent #type/research #area/personal
> - [x] T6 — Documentación mínima, findings registry, entrega final y cierre con feedback #owner/agent #type/admin #area/personal

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

- **2026-09-13** — Entrega completa: harness implementado (stdlib Python, entrypoint + rules + README), suite ejecutada y reproducible; adversarial verification ronda 1 (D1 telemetría off-by-one → falsos positivos WARM/SWITCH; D2 sin guarda de fidelidad; D3 crash en vez de SKIP) corregida en ciclo 1 con pruebas de inyección; ronda 2 confirmó D1/D2/D3 y halló N1 (cláusula de evidencia de superficie sin ancla) corregido en ciclo 2 (26 anclas) junto a N2/N3; límite de 2 ciclos respetado; residuos documentados como limitaciones en README. Hallazgo real del sistema F1 (validador schema en rojo) registrado sin auto-corrección. Tarea puente pasa a Review.
- **2026-09-12** — Reconciliación parent completada: los tres artifacts son consistentes (sin contradicciones factuales); las tensiones reales (cláusula de evidencia de superficie de DEFAULT, vocabulario `load_policy` con 3 enumeraciones sin árbitro, nota VPN cross-domain sin `area`, MCPs a nivel máquina fuera del vault, sin unload) quedan como WARN de diseño. `conformance-spec-v1.md` publicado: L0 estático (8), L1 simulado (16), L2 live-exposure (1 + baseline de contexto), stdlib Python, side-effect policy read-only.
- **2026-09-12** — A (Contract Auditor) completó en modo síncrono: 17 contratos C01-C17; club cerrado 4/4 sin terceros vivos; ambiguities: vocabulario load_policy, INDEX.md fuera del club declarativo, nota VPN, MCP host-level NOT-TESTABLE desde vault. Entorno: límite de concurrencia de subagents (1 a la vez) forzó ejecución secuencial A/B/C.
- **2026-09-12** — B (Domain Isolation Auditor) completó: 17 hallazgos con evidencia en `80-agents/tools/conformance-harness/artifacts/domain-isolation-audit.md`. Claves: gate es prompt-discipline sin enforcement mecánica; MCPs `aranea-*` visibles en toda sesión (config a nivel máquina, fuera del vault); DEFAULT no neutral por cláusula de evidencia de superficie; sin mecanismo de unload; nota VPN cross-domain sin `area` resoluble; `when_echo_forge_loaded` no canónico; drift de `area` en memoria activa.
- **2026-09-12** — Proyecto creado como único planificador durable. Baseline `a6a503f`. Bootstrap ejecutado; auditorías A/B/C como subagents con artifacts en `80-agents/tools/conformance-harness/artifacts/`.

## 🧭 Decisiones

- El harness no rediseña Agents-OS: cualquier defecto real detectado se registra como finding, no se auto-corrige.
- El harness vive en `80-agents/tools/conformance-harness/`: es tooling del sistema (como el materializador), no una skill de comportamiento del agente.

## 🔗 Docs / Links

- 

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
