---
type: project
schema_version: 1
owner: me
root: true
status: active
cssclasses:
  - wide
priority: P1
area: "[[Personal]]"
parent:
sprint:
start: 2026-06-27
due:
progress: 100
repo:
jira:
prs:
aliases:
  - Sistema de Memoria de Agentes
  - Agent Memory System
tags:
  - area/personal
  - kind/project
  - project/agents-os
created: 2026-06-27
updated: 2026-09-09
---

# AGENTS OS

> [!info]+ Cockpit humano
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1
> Sistema para entregar a agentes contexto Markdown curado, suficiente,
> verificable y recuperable sin convertir el startup en una lectura amplia.

## 🎯 Objetivo

- Mantener un sistema agnóstico al modelo que combine instrucciones, memoria,
  documentación curada, estrategias de carga y procedimientos ejecutables.
- Permitir que un agente fresco retome trabajo con el menor contexto suficiente
  y sin depender del historial del chat.
- Mantener una sola fuente canónica por regla, hecho, procedimiento y estado.

## 📊 Estado actual

- **Estado exacto vigente:** sistema operativo y baseline maduro conservado en 100%; [[AGENTS OS - Fase 4]] está activa únicamente como backlog canónico con progreso 0%, todas sus tareas en To Do y ninguna ejecución WIP/Review iniciada.
- **Registro de performance activo:** las superficies canónicas [[Codex]], [[Claude Code]], [[Cursor]] y [[Antigravity]] registran cada segmento material de trabajo de código como `agent_run`, separado por superficie×modelo exacto y con outcome, verificación, rework y scores opcionales con evaluator.
- **Iteración activa:** [[AGENTS OS - Fase 4]], backlog-only y sin tarea iniciada. [[AGENTS OS - Relaciones Tipadas de Graphify]] permanece `completed`, entrega aceptada y `graphify-obsidian 0.9.6.post2` activo.
- **Salud verificada al 2026-09-09:** schema `45 tipos / 44 templates / 5 fixtures / 0 errores`; Doctor `HIGH=0 / MEDIUM=0 / LOW=0`, startup≈5033; lint del corpus `32 → 9 ERROR` con el gate en `GO` y `new=0`; Graphify `fresh` tras el primer reindex verde en seis sesiones. Los 9 errores residuales quedaron declarados en el baseline: cinco son secciones de las dos skills de specs de Signals y cuatro son secciones faltantes en tres notas de proyecto o recurso.
- [[AGENTS OS - Fase 2]] quedó `completed` con G7 accepted. Su deuda residual
  se transfirió sin retrabajo a Fase 3: templates/schema versionados, lint
  preventivo, Resources/agents, Graphify metadata-aware, Context Router local,
  `41 ERROR / 84 WARN`, dos skills SQX y segundo piloto de layout.
- El proyecto controlador anterior y los proyectos Beta/Hot Path se preservaron
  en `40-archive/agents-os-projects/`; ya no son planificadores vigentes.
- El parent es deliberadamente compacto: la ejecución detallada vive en el
  proyecto de agente activo; las reglas runtime viven en constitución y skills.

## 🧩 Subproyectos

- **Activo:** [[AGENTS OS - Fase 4]] — auditoría base y backlog canónico; progreso 0%, sin WIP/Review.
- **Completados:** [[AGENTS OS - Relaciones Tipadas de Graphify]] — preservación lossless de relaciones semánticas por par source-target; [[AGENTS OS - Fase 3]] — schema ejecutable, metadata retrieval, retrofit, segundo piloto y gate estricto; [[AGENTS OS - Fase 2]] — arquitectura, gobierno del vault, documentación curada y baseline heredado.
- **Históricos:** [[AGENTS OS - Hot Path y Cierre Silencioso]],
  [[AGENTS OS - Beta y Hardening]], [[AGENTS OS - Fase 1 - Historial]].

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> Este proyecto es `owner: me`: muestra sólo tareas humanas y tareas puente
> `#type/supervision`. Las tareas `#owner/agent` viven en sus proyectos de
> agente y no se duplican en este cockpit. Una tarea sin owner queda visible
> para clasificarla.

> [!example]- Fuente de tareas del proyecto humano
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [x] [[AGENTS OS - Fase 2]] cierre aprobado por owner; marcar Done en Obsidian #owner/me #type/supervision #area/personal
> - [x] [[AGENTS OS - Fase 3]] ejecutar F6 y revisar G6 — retrofit, segundo piloto y decisión strict #owner/me #type/supervision #area/personal
> - [x] [[AGENTS OS - Relaciones Tipadas de Graphify]] desarrollar y revisar preservación lossless de relaciones tipadas #owner/me #type/supervision #area/personal
> - [ ] [[AGENTS OS - Fase 4]] priorizar y supervisar la próxima mejora desde el backlog auditado #owner/me #type/supervision #area/personal
> - [r] [[AGENTS OS - Conformance Harness]] arrancar + seguimiento #owner/me #type/supervision #area/personal

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const all=dv.current().file.tasks.array();
const mine=all.filter(t=>has(t,"owner/me"));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3,"🧍 Mis tareas y supervisiones");
board(mine);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## 📋 Tablero

> [!note]+ Alcance del rollup
> Busca sólo `#owner/me` bajo `10-projects/Personal/AGENTS OS/`. Incluye tareas
> humanas y puentes de subproyectos, pero nunca tareas `#owner/agent`.

#### 🟦 To Do
```tasks
sort by priority
path includes 10-projects/Personal/AGENTS OS
tag includes #owner/me
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes 10-projects/Personal/AGENTS OS
tag includes #owner/me
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes 10-projects/Personal/AGENTS OS
tag includes #owner/me
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes 10-projects/Personal/AGENTS OS
tag includes #owner/me
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-09-09** — Ciclo de higiene `full-system-1` con el segundo reporte Kaizen del sistema (340 feedbacks, 67 días de backlog). Se desbloqueó el reindex poblando el baseline del lint después de bajar la deuda de 32 a 9 errores; se corrigió un bug de una línea en el linter de tags que generaba 104 errores fantasma; se cerraron cinco contradicciones define≠implement en fuentes canónicas, incluida una que hacía nacer toda skill nueva violando el contrato de leanness y otra que dejaba ciego al gate del club cerrado de `always`. La continuidad interna pasó de 112 notas per-sesión a 5 slots activos. Cinco patrones se promovieron a L3 y diez propuestas estructurales quedaron abiertas, entre ellas la descubribilidad de skills y el diagnóstico de capacidades por superficie. Se regeneró el core compartible como build declarativo con verificación SHA-256, corrigiendo en el camino cuatro defectos de portabilidad que sólo se ven al instalar en otra máquina. El entregable remoto pasó de evaluación con score a contraste promesa vs. evidencia, versión 4 verificada.

- **2026-09-03** — Se saneó el hot path de memoria: startup `≈24492→≈4724` tokens; la continuidad global quedó reducida a comportamientos transferibles; cuatro decisiones/patrones de Echo Forge pasaron de `always` a `when_project_loaded`; cinco memorias internas mal marcadas `scope: global` quedaron scoped; Context Retrieval pasó a lazy `when_entity_loaded`; la regla global de Codex, el hook local y su generador ahora ejecutan bootstrap una vez por nueva sesión y nunca por mensaje. Se incorporó lifecycle de continuidad con un slot mutable por `continuity_key`, estados `active/superseded/archived` y retiro atómico; Doctor impide project ledgers, scopes globales de dominio, transiciones inválidas y más de un checkpoint activo por clave. Doctor, schema, strict del fix, probes y Context Router quedaron verdes; reindex bloqueado por `26/6` findings ajenos al fix.

- **2026-08-11** — Se abrió [[AGENTS OS - Fase 4]] como backlog-only desde una auditoría completa de ideología, componentes, memoria, skills, Resource Wiki y observabilidad. Se corrigieron de inmediato secretos persistidos, un archivo Markdown corrupto, paths client-owned, drift de índices/logs, lifecycle `deprecating` y perfiles de superficie; ninguna tarea estructural quedó iniciada.

- **2026-08-11** — Se incorporó el registro canónico de performance superficie×modelo: cuatro perfiles de superficie, tipo/template `agent_run`, skill `agents-os-agent-run-register`, dashboard de evidencia y wiring en preferencias, feedback y cierre. No se backfillea historial ambiguo; la medición confiable comienza con este contrato.

- **2026-08-11** — Se regularizó el estado post-entrega: cockpit `progress: 100`, modo estabilización/mantención sin backlog ni iteración activa, Doctor `0/0/0` y bundles globales Graphify de Copilot/Antigravity/Gemini sincronizados a `0.9.6.post2`. No se abre una nueva fase sin evidencia de uso real.

- **2026-08-11** — El owner aceptó [[AGENTS OS - Relaciones Tipadas de Graphify]] y pidió cierre de sesión. El proyecto pasa a `completed`, la tarea puente queda Done y AGENTS OS vuelve a no tener una iteración activa.

- **2026-08-11** — [[AGENTS OS - Relaciones Tipadas de Graphify]] completó T0.1–T2.2: causa raíz confirmada en el colapso de `Graph`/`DiGraph`, representación `relation + relations` implementada, wheel `0.9.6.post2` instalado y matriz completa verde. La tarea puente pasa WIP→Review para aceptación del owner.

- **2026-08-11** — Se abrió [[AGENTS OS - Relaciones Tipadas de Graphify]] como único planificador activo para reproducir y corregir la pérdida de una relación cuando `parent` y `related` apuntan al mismo target. La tarea puente queda WIP y T0.1 inicia sobre el fork metadata-aware existente.

- **2026-08-11** — El owner aceptó G6 de [[AGENTS OS - Fase 3]] y cerró la tarea puente. Fase 3 pasa a `completed`; no queda una iteración activa ni tareas abiertas de AGENTS OS, fuera de la mantención periódica normal.

- **2026-08-11** — F6 de [[AGENTS OS - Fase 3]] quedó completa con T6.1–T6.6 Done y G6 en Review. Segundo piloto Task Board `old=0/new=139`; corpus y baseline `0/0`; gate estricto activo; Doctor `0/0/0`; pack 183; Graphify `5123/6114`; E2E `14/14` sin misses. La tarea puente pasa WIP→Review para aceptación del owner.

- **2026-08-11** — T6.4 de [[AGENTS OS - Fase 3]] quedó completa después del scanner nativo sobre 1560 archivos: Task Board `old=0/new=139`, once paths nuevos y 117 tareas pendientes del piloto. T6.6 quedó WIP con baseline `0/0` y gate estricto activo; la tarea puente permanece WIP hasta la matriz final.

- **2026-08-11** — Se intentó ejecutar el scanner nativo de Task Board para cerrar T6.4, pero macOS bloqueó `osascript` con error `1002` por falta de permiso de Accesibilidad; la cache sigue `old=28/new=0`. La tarea puente permanece WIP y T6.6 no puede iniciarse sin esa evidencia.

- **2026-08-11** — T6.5 de [[AGENTS OS - Fase 3]] quedó completa: contrato y lint `0/0`, gate `new=0`, Doctor `0/0/0`, pack de 183 archivos validado, Graphify `5118/6101` y E2E `14/14` con 0 misses. T6.4 permanece WIP porque Task Board sigue `old=28/new=0`; la tarea puente continúa WIP y el próximo paso es ejecutar el scanner nativo, verificar el tablero y luego avanzar a T6.6.

- **2026-08-10** — T6.2 de [[AGENTS OS - Fase 3]] quedó completa: resolvió los 56 ERROR residuales de campos, tags, secciones y lifecycle mediante normalización contractual acotada. Contrato y strict de 19 notas quedan `0/0`; gate global `0/80`, `new=0`, `resolved=95`. T6.3 debe clasificar y resolver los 80 warnings restantes; la tarea puente permanece WIP.
- **2026-08-10** — T6.1 de [[AGENTS OS - Fase 3]] quedó completa: los doce entregables legacy restantes migraron a `doc` v1, dos históricos quedaron `archived` y diez `active` preservaron autoridad, lifecycle y provenance. Strict del lote `0/0`; gate global `56/80`, `new=0`, `resolved=39`; Graphify `5081/6011` verificó los doce nodos. T6.2 es el próximo paso y la tarea puente permanece WIP.
- **2026-08-10** — El owner aceptó G5 de [[AGENTS OS - Fase 3]] y pidió cierre de sesión. F6 queda habilitada sin iniciar, la tarea puente vuelve Review→WIP y el próximo paso es T6.1: resolver 35 `unknown-type` con evidencia.
- **2026-08-10** — F5 de [[AGENTS OS - Fase 3]] quedó completa y G5 pasó a Review: rutas metadata/facets→índice→grafo→body, fallback Markdown, cold/warm/swap y dos superficies sin API. Cinco repeticiones sumaron 70 operaciones con 0 misses y precisión proxy 100%; lint, schema, gate, Doctor y reindex `5014/5942` quedaron verdes. Las comunidades variables no son gate. La tarea puente pasa WIP→Review y F6 espera aceptación owner.
- **2026-08-10** — F5 de [[AGENTS OS - Fase 3]] completó T5.1: contrato Graphify, skill de retrieval y doc conceptual ahora fijan metadata/facets→índice curado→edges tipados/`references`→body con autoridades separadas. Lint estricto, validator, filtros, query filtrada, traversal y reindex quedaron verdes; T5.2 pasa a WIP y la tarea puente permanece WIP.
- **2026-08-10** — El owner aceptó G4 de [[AGENTS OS - Fase 3]]. F5 queda habilitada e iniciada con T5.1 WIP para actualizar contrato y Context Router a metadata/facets→grafo→body; la tarea puente vuelve Review→WIP hasta entregar G5.
- **2026-08-10** — F4 de [[AGENTS OS - Fase 3]] quedó completa y G4 pasó a Review: Graphify `0.9.6.post1` proyecta metadata/facets, resuelve aliases, emite siete relaciones allowlisted, honra `.graphifyignore` y preserva comandos legacy. Suite `2840 passed, 28 skipped`; benchmark pareado `4984/5893/493`, `15.93 s`, `5,308,347 bytes`, sin tag-nodes ni ignored paths; refresh post-registro `4985/5894`. La tarea puente pasa WIP→Review y F5 espera aceptación del owner.
- **2026-08-10** — El owner aprobó G3. F4 queda habilitada sin iniciar, la tarea puente vuelve Review→WIP y el próximo paso es T4.1: diseñar la proyección de metadata y facets.
- **2026-08-10** — F3 quedó completa y G3 pasó a Review. Las dos skills app-owned pendientes se migraron al checkout real `xKoRx/symphony` bajo GOPATH, se restauró la piloto `sqx-plugin-lifecycle` en la rama activa, registry/pack quedaron actualizados y el forward-test core/portable/prompt/app-owned terminó con cero fallas. La tarea puente pasa WIP→Review; F4 espera aceptación del owner.
- **2026-08-10** — F3 avanzó T3.1–T3.3: se creó `30-resources/agents/`, se movieron tres skills portables sin copias ni cambio de hashes y se formalizó `type: prompt` con template y fixture. Schema, strict, Doctor y reindex Graphify están verdes. T3.4/T3.5 quedan WIP bloqueadas porque el checkout/remoto de `xKoRx/symphony` no está accesible; la tarea puente permanece WIP y G3 no pasa a Review.
- **2026-08-10** — El owner aceptó G2 y pidió cerrar la sesión para continuar F3 con un agente fresco. F3 queda habilitada sin iniciar, la tarea puente vuelve Review→WIP con foco T3.1/G3 y el próximo paso es inventariar referencias a `30-resources/agents-skills/` con move map y rollback.
- **2026-08-10** — F2 quedó completa y G2 pasó a Review: lint contractual, strict explícito, baseline SHA-256 decreciente, fixtures read-only y gate no-new-debt integrado a Graphify. E2E verde con `94/81`, `new=0` y Graphify `5041/5890`; la tarea puente pasa WIP→Review y F3 no inicia sin aceptación del owner.
- **2026-08-10** — Se corrigió el drift del cockpit: G1 ya estaba `accepted` en el planificador canónico y F2 comenzó por T2.1; la tarea puente permanece WIP hasta entregar G2 en Review.
- **2026-08-10** — El owner ordenó corregir la fricción de materialize y
  terminar G1. T1.7 aisló validación create por tipo sin debilitar fail-closed;
  G1 `review→accepted`, F2 queda habilitada y el bridge pasa Review→WIP para
  T2.1/G2.
- **2026-08-10** — T1.6 completada: materializador único y 13 entrypoints
  auditados, sin agregar el contrato al hot path. G1 vuelve a Review y el
  bridge WIP→Review.
- **2026-08-10** — El owner rechazó implícitamente G1 al detectar que la
  garantía universal de creación no estaba demostrada. Bridge Review→WIP;
  T1.6 centraliza materialización y hace explícita [[Economía de Tokens]] como
  invariante.
- **2026-08-10** — F1 de [[AGENTS OS - Fase 3]] completada: contrato v1,
  cobertura type→template, tags/secciones y lifecycle/create validados. G1
  queda en Review y la tarea puente pasa WIP→Review; sólo el owner acepta G1
  y habilita F2.
- **2026-08-08** — El owner aceptó G0 de [[AGENTS OS - Fase 3]]. F1 queda
  habilitada sin iniciar; la tarea puente permanece WIP y el próximo paso es
  T1.1, contrato machine-readable + `schema_version`.
- **2026-08-08** — Se agregó la vista de tareas del cockpit: Dataview renderiza
  sólo la fuente local `#owner/me` y el tablero Tasks hace rollup del árbol
  AGENTS OS filtrando `#owner/me`. Las tareas internas `#owner/agent` siguen
  viviendo exclusivamente en cada proyecto de agente. El owner ya marcó Done
  la tarea puente de Fase 2; Fase 3 permanece WIP.
- **2026-08-08** — El owner ordenó cerrar Fase 2 y trasladar su deuda viva a
  [[AGENTS OS - Fase 3]] sin repetir trabajo. Fase 3 queda activa con G0 en
  Review y una nueva tarea puente WIP. La tarea puente Fase 2 se mantiene en
  Review hasta que el owner la marque Done, según el contrato de proyectos de
  agente.
- **2026-08-08** — El owner confirmó el rescan real path-based. T7.4 quedó
  cerrada y G7 aceptada; Fase 2 está lista para que el owner cierre la tarea
  puente o decida una nueva iteración. La tarea puente permanece en Review
  porque el agente no la marca Done.
- **2026-08-08** — F7 entregada para revisión: `237→41 ERROR`, doctor
  `0/0/0`, Graphify verde y gate estricto NO-GO; `warn-first` se conserva. La
  tarea puente pasa a Review. Falta ejecutar la prueba real de rescan en
  Obsidian antes de aceptar G7.
- **2026-08-08** — El owner autorizó aceptar G6 si la revalidación estaba
  verde; doctor, Graphify y la evidencia multisuperficie lo confirmaron. G6
  quedó `accepted` y F7 inició con baseline de metadata `237/84`. La tarea
  puente vuelve a WIP mientras G7 permanezca abierto.
- **2026-08-09** — G6 de [[AGENTS OS - Fase 2]] pasó a `review`: doctor
  estricto y Graphify verdes; Codex Desktop + un proceso fresco de Codex CLI
  recuperaron bootstrap y registry. Queda la decisión humana de aceptar y
  cerrar, o abrir una nueva iteración.
- **2026-08-08** — Piloto F5 movió el proyecto completo a
  `10-projects/Personal/AGENTS OS/` sin cambiar `[[AGENTS OS]]`, su parent ni
  la tarea puente. Lint, pack, doctor y Graphify resolvieron el nuevo path.
- **2026-08-01** — Se abrió [[AGENTS OS - Fase 2]] como único planificador
  activo. Se compactó este cockpit y se archivaron los proyectos anteriores,
  migrando sus pendientes relevantes a Fase 2.
- **2026-06-27** — Inicio del proyecto AGENTS OS.

## 🧭 Decisiones vigentes

- `AGENTS.md` es un hook mínimo hacia `agents-os-bootstrap`; no implementa el
  startup.
- `agents-os.md` es un mapa conceptual, no una dependencia obligatoria.
- La constitución contiene invariantes; las skills contienen procedimientos;
  los proyectos contienen estado; el journal contiene historia.
- Markdown es fuente de verdad; LLM Wiki compila conocimiento curado y Graphify
  es un índice derivado.
- El proyecto de agente activo es el único planificador durable de la iteración.

## 🔗 Fuentes canónicas

- [[agents-os]] — mapa del sistema.
- [[agent-constitution]] — invariantes runtime.
- [[AGENTS OS - Fase 4]] — backlog activo derivado de auditoría completa; estado base sin ejecución iniciada.
- [[AGENTS OS - Fase 3]] — iteración completada; schema ejecutable, retrofit, segundo piloto y gate estricto.
- [[AGENTS OS - Fase 2]] — iteración completada y baseline heredado.
- `80-agents/skills/agents-os-bootstrap/SKILL.md` — startup.
- `80-agents/skills/agents-os-context-retrieval/SKILL.md` — retrieval.
- `80-agents/skills/agents-os-agent-run-register/SKILL.md` — registro de ejecuciones atribuibles por superficie×modelo.
- `80-agents/crew/INDEX.md` — superficies canónicas y dashboard de performance.
- `90-system/convenciones.md` — convenciones actuales de Sistema 2.
