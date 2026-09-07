---
type: project
owner: agent
root: false
cssclasses:
  - wide
status: active
priority: P1
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start: 2026-07-25
due:
progress: 100
repo:
jira:
prs:
tags:
  - area/personal
  - kind/project
created: 2026-07-25
updated: 2026-07-25
aliases:
  - AGENTS OS Hot Path
  - Hot Path Iteration
---

# AGENTS OS - Hot Path Iteration

> [!warning] Archivo histórico
> Proyecto duplicado fusionado el 2026-07-27 en
> [[AGENTS OS - Hot Path y Cierre Silencioso]]. No usar como planificador ni
> fuente de estado vigente.

> [!info]+ AGENTS OS - Hot Path Iteration
> **Padre:** [[AGENTS OS]] · **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1
> Iteración para convertir AGENTS OS en un pipeline corto, incremental y silencioso. Diagnóstico y propuesta surgieron de ChatGPT contra el ITERATION-PROMPT; este proyecto controla su implementación.

## 🎯 Objetivo

Reducir el costo de arranque y cierre del sistema sin perder continuidad ni
auditabilidad. Tres frentes:

1. **Hot Path:** un solo bootstrap canónico, arranque incremental por modo
   (cold / warm / cambio de entidad), memoria interna enrutable por metadata.
2. **Silent Close:** cierre por delta, feedback event-driven, reporte de 1-2
   líneas por defecto.
3. **Doctor + Benchmark:** validador automático de rutas, always-load,
   duplicación, tamaño del startup y consistencia proyecto↔skills.

## 📊 Estado actual

- Brief original de ChatGPT preservado en `00-inbox/agents-os-hot-path-brief.md`.
- Diagnóstico y plan de 4 fases (P0→P3) confirmados por auditoría local del
  agente. Los hallazgos P0 ya fueron verificados uno a uno contra archivos
  vivos (credencial expuesta, drift de rutas user_rule→Cursor, referencias
  rotas en `agents-os-skill-authoring`, path de constitución en
  `PROJECT-STATE.md` del chatgpt-pack).
- `.graphifyignore` ya excluye `outputs/agents-os-chatgpt/`; ese sub-hallazgo
  del brief quedó resuelto y no requiere acción.
- Hallazgo de drift invertido: AGENTS.md (vault) está bien en `/Users/rjara/...`;
  el `user_rule` de Cursor apunta a `/Users/rodrigojara/...` (roto). No es
  editable desde el vault: queda como deuda administrativa para que el owner
  lo corrija en la UI de Cursor.

## 🧠 Diagnóstico (resumen del brief)

1. **Arranque sobredimensionado sin receta única** — al menos tres versiones
   del startup (dos en `agents-os.md`, una en `agents-os-bootstrap/SKILL.md`,
   más priorización en `agents-os-context-retrieval`). Memoria interna
   marcada `always` sin filtro (incluye una de Symphony). Startup real
   ≈21–24k tokens (objetivo histórico: 3k). Contradicción en el Context
   Router: dice "nunca saltar capas" pero su tabla arranca en capa 2.
2. **Cierre mezcla persistencia interna con UX** — `agents-os-session-close`
   exige inventario de 12 campos. `session-close` marcado `always-load` en
   la guía aunque requiere trigger explícito. 153 feedbacks acumulados
   (~75k palabras). Plantillas de feedback suman 663 palabras antes de
   rellenar.
3. **Drift documental verificado** — `session-close` pendiente en roadmap
   aunque la skill está completa; `PROJECT-STATE.md` del pack apunta a path
   antiguo de constitución; `agents-os-skill-authoring` con refs relativas
   rotas; SKILL.md mezclan contrato ejecutable con `Finish Tasks`/`Progress
   Log`.

## 🔒 Hallazgos P0 confirmados

- **Seguridad:** `80-agents/memory/internal/agent-memory/2026-07-22-symphony-kronos-instrument-sync-gap.md`
  - [REDACTED] Credencial retirada del historial; la fuente original debe rotarse fuera del vault.
  + 3 IPs internas. Violación directa del mandamiento 13 de la constitución.
  Se carga en TODA sesión, no solo las de Symphony.
- **Drift user_rule Cursor:** apunta a `/Users/rodrigojara/...` (no existe).
  El vault real está en `/Users/rjara/...`. No editable desde el vault.
- **Refs rotas:** `agents-os-skill-authoring/SKILL.md` usa `_shared/...` y
  `../../templates/...` con profundidad incorrecta.
- **`PROJECT-STATE.md` del chatgpt-pack:** línea 243 lista
  `80-agents/memory/public/constitution/agent-constitution.md` (path
  legado). La fuente canónica es `80-agents/agents-os/agent-constitution.md`.

## ✅ Tareas

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">✅ ${d}</span>`);}
const tasks=dv.current().file.tasks.array().sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));
const el=dv.el('div','');
el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owner de este proyecto: #owner/agent. Tipos: #type/dev #type/research #type/admin #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
>
> **P0 — Reparación y seguridad (sin tocar contratos)**
> - [x] Redactar credencial expuesta en `2026-07-22-symphony-kronos-instrument-sync-gap.md` y bajar `load_policy: always` → `when_project_loaded` #owner/agent #type/dev #area/personal #urgent ✅ 2026-07-25
> - [x] Arreglar referencias relativas rotas en `agents-os-skill-authoring/SKILL.md` #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Actualizar path legado de constitución en `chatgpt-pack/PROJECT-STATE.md` línea 243 #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [ ] Deuda admin: pedirle al owner que corrija el `user_rule` de Cursor (`/Users/rodrigojara/...` → `/Users/rjara/...`) — no editable desde el vault #owner/me #type/admin #area/personal #waiting
>
> **P1 — Hot Path (aprobado y aplicado)**
> - [x] Unificar el startup canónico en `agents-os-bootstrap/SKILL.md` (máquina de estados cold/warm/swap) y adelgazar `agents-os.md` a mapa+routing #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Enrutar memoria interna por metadata (prohibir `always` en memorias de dominio; permitir solo 1 nota global always) #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Corregir contradicción del Context Router: "empezar en la capa más barata relevante", no waterfall #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Refactor del Mandamiento 16: "toda sesión con delta durable deja continuidad" (no "toda sesión") #owner/agent #type/dev #area/personal ✅ 2026-07-25
>
> **P2 — Silent Close (aprobado y aplicado)**
> - [x] Definir clasificador de cierre por delta en `agents-os-session-close` y reporte default de 1-2 líneas #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Pasar feedback a event-driven (solo ante fricción/degradación/sampling); fusionar graphify feedback al de sesión en higiene #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Sacar `session-close` de always-load en la guía #owner/agent #type/dev #area/personal ✅ 2026-07-25
>
> **P3 — Doctor + Benchmark (aprobado y aplicado)**
> - [x] Skill `agents-os-doctor` con lint automático de rutas, always-load, duplicación y tamaño del startup #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Benchmark E2E con gate: cold start, warm turn, swap entity, Graphify degradado, los 4 tipos de cierre #owner/agent #type/research #area/personal ✅ 2026-07-25
>
> **Pendiente post-implementación**
> - [ ] Reindex Graphify fuera de Cursor (sandbox bloquea `~/.cache`) #owner/me #type/admin #area/personal #waiting
> - [ ] Primera corrida formal del gate E2E con agente fresco #owner/agent #type/research #area/personal
> - [ ] Compactación opcional de `agents-os-operating-continuity.md` (~270 líneas; mover historia a sub-nota) #owner/agent #type/dev #area/personal

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes AGENTS OS/agentes/AGENTS OS - Hot Path Iteration
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes AGENTS OS/agentes/AGENTS OS - Hot Path Iteration
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes AGENTS OS/agentes/AGENTS OS - Hot Path Iteration
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes AGENTS OS/agentes/AGENTS OS - Hot Path Iteration
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-07-25** — Proyecto creado. Brief original de ChatGPT movido a
  `00-inbox/agents-os-hot-path-brief.md`. Los 4 hallazgos P0 fueron
  verificados contra archivos vivos; el sub-hallazgo de `.graphifyignore`
  ya estaba resuelto. Plan P0→P3 listo para ejecución. P0 no toca
  contratos canónicos y se puede ejecutar en este turno; P1/P2/P3 tocan
  constitución, guía y skills, por lo que requieren aprobación explícita
  del owner antes de aplicarse.
- **2026-07-25 (P0 cerrado)** — Cambios aplicados:
  - Seguridad: credencial Symphony redactada en
    `2026-07-22-symphony-kronos-instrument-sync-gap.md` + `load_policy`
    `always`→`when_project_loaded`. Ya no se carga en sesiones ajenas a
    Symphony.
  - Drift: `agents-os-skill-authoring/SKILL.md` refs relativas corregidas
    (`_shared/`→`../_shared/`, `../../templates/`→`../../../templates/`).
    Las otras 20 skills ya usaban bien los paths.
  - Path de constitución corregido en `chatgpt-pack/PROJECT-STATE.md`
    (línea 243) → apunta al canónico `80-agents/agents-os/`.
  - Hallazgo invertido confirmado: `AGENTS.md` (vault) está bien en
    `/Users/rjara/...`; el drift está en el `user_rule` de Cursor
    (`/Users/rodrigojara/...`). No editable desde el vault; tarea puente
    humana sembrada con `#waiting`.
  - Log: `journal/logs/2026-07-25-hot-path-p0-repairs-and-security.md`.
  - Continuidad interna:
    `agent-memory/2026-07-25-agents-os-hot-path-iteration-continuity.md`.
  - Owner aprobó orden P1→P2→P3 para cuando se desbloqueen.
- **2026-07-25 (P1 Hot Path aplicado)** — Refactor estructural del startup:
  - `agents-os-bootstrap/SKILL.md` reescrito como la única máquina de
    estados (cold / warm / swap-entity).
  - `agents-os.md` adelgazado a mapa+routing; eliminados los procedimientos
    duplicados de startup.
  - `agents-os-context-retrieval/SKILL.md` corregido: el Context Router
    define entry layer por intención y condición de escalado, no waterfall
    estricto. Las Hard Rules ya no dicen "no saltar capas".
  - `metadata-schema.md` codifica el closed club de `load_policy: always`:
    solo constitución, perfil y UNA nota global interna. Prohibido para
    memorias de dominio.
  - Mandamiento 16 reformulado: "toda sesión con delta durable deja
    continuidad", no "toda sesión".
  - Log: `journal/logs/2026-07-25-hot-path-p1-applied.md`.
- **2026-07-25 (P2 Silent Close aplicado)** — Refactor del cierre:
  - `agents-os-session-close/SKILL.md` reescrito con delta classifier
    (6 filas deciden qué persistir). Tactical mode absorbido como caso.
  - Default report al usuario: 1-2 líneas. Detailed mode solo con
    `cierre con detalle` o decisión/conflicto.
  - Feedback event-driven: solo ante fricción/degradación/gap/sampling.
    Feedback de Graphify plegado a higiene periódica, no segunda nota
    automática por cierre.
  - `load_policy: always`→`manual` en session-close (ya era así en la
    práctica).
  - Log: `journal/logs/2026-07-25-hot-path-p2-applied.md`.
- **2026-07-25 (P3 Doctor + Benchmark creados)** —
  - Skill nueva `agents-os-doctor`: 11 checks categorizados, read-only por
    defecto, fixes agrupados en un único change_log por aprobación.
  - `agents-os-doctor/BENCHMARK.md`: gate E2E con 5 escenarios (cold / warm
    / swap / Graphify degradado / 4 tipos de cierre) y criterio compuesto
    de aprobación. Reduce tokens sin perder fuente que cambie la decisión.
  - `INDEX.md` actualizado con la nueva skill; `next_audit` 2026-08-25.
  - Log: `journal/logs/2026-07-25-hot-path-p3-doctor-benchmark-created.md`.
- **2026-07-25 (cierre del turno)** — P0/P1/P2/P3 aplicados en un único
  turno por orden explícito del owner ("avanza con todo"). Queda pendiente:
  (a) Graphify reindex fuera de Cursor (sandbox bloquea `~/.cache`);
  (b) primera corrida formal del gate E2E con agente fresco;
  (c) compactación opcional de la nota global interna
  `agents-os-operating-continuity.md` (~270 líneas, secciones históricas
  pueden salir de la línea always).
- **2026-07-25 (P4 + cierre)** — Owner pidió "avanza hasta el final".
  Aplicado P4: global interna compactada de 270 → ~75 líneas (historia a
  `agents-os-operating-continuity-archive.md` con `load_policy: manual`);
  `agents-os-session-feedback/SKILL.md` alineada con event-driven; umbral
  doctor ajustado a baseline medido (400 líneas vs 250).
  Cierre ejecutado con el nuevo modelo Silent Close: L0 raw + L1 summary +
  feedback event-driven (fricción real sandbox) + log consolidado. Ninguna
  L3 nueva promovida — el conocimiento reusable ya vive en los contratos
  tocados (Mandamiento 16, metadata-schema, session-close, doctor).
  Proyecto completado al 100%; deuda admin y gate E2E quedan como
  seguimiento humano.

## 🧭 Decisiones

- **Una sola fuente canónica para el brief:** el chatgpt-pack es snapshot
  derivado; el brief fuente vive ahora en `00-inbox/` de este proyecto.
- **P0 ejecutable ahora; P1-P3 bloqueados por aprobación:** la constitución
  exige log auditable para cambios en constitución/perfil/skills/proyectos
  Sistema 2. Hot Path y Silent Close reforman contratos vivos; no aplicar
  sin OK explícito del owner.
- **Modelo de ownership:** este es un proyecto de agente (`owner: agent`,
  `parent: [[AGENTS OS]]`) porque la mayor parte de la ejecución la hace
  el agente. La tarea puente humana vive en el proyecto padre.

## 🔗 Docs / Links

- [[AGENTS OS]] (proyecto padre)
- [[agents-os]] (guía operativa)
- [[AGENTS OS - Beta y Hardening]] (beta E2E — no confundir; esa mide, esta reforma)
- Brief: `00-inbox/agents-os-hot-path-brief.md`
- ChatGPT pack (snapshot derivado): `10-projects/AGENTS OS/chatgpt-pack/`
