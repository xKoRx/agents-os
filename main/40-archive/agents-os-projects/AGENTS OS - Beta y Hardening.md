---
type: project
owner: agent
root: false
cssclasses:
  - wide
status: completed
priority: P1
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start: 2026-07-01
due:
progress: 100
repo:
jira:
prs:
tags:
  - area/personal
  - kind/project
created: 2026-07-01
updated: 2026-08-01
aliases:
  - AGENTS OS Beta y Hardening
---

# AGENTS OS - Beta y Hardening

> [!info]+ AGENTS OS - Beta y Hardening
> **Padre:** [[AGENTS OS]] · **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1
> Ejecución activa pendiente de AGENTS OS: correr la beta real end-to-end (Fase 5) y cerrar el hardening abierto de Fase 6 (evaluación de watcher).

## 🎯 Objetivo

- Ejecutar el circuito completo de AGENTS OS (bootstrap → retrieval → trabajo → cierre → destilación → reindex) sobre proyectos Meli reales, medir si reduce reexplicación y mejora continuidad, y validar agnosticismo entre Codex, Claude, Cursor y Antigravity.
- Cerrar el único ítem abierto de hardening post-beta (Fase 6): decidir si el watcher de reindex automático de Graphify aporta valor real frente al reindex manual.

## 📊 Estado actual

- **Cerrado administrativamente el 2026-08-01.** La beta E2E, validación
  multisuperficie y evaluación del watcher fueron migradas a
  [[AGENTS OS - Fase 2]]. Esta nota queda como historial y no como planificador
  activo.
- **To Do**: además de la beta E2E, está pendiente validar cómo Codex y Claude
  invocan las skills directamente desde `80-agents/skills/`, sin copias,
  symlinks ni adapters por superficie, y medir qué mecanismo ofrece mejor
  discovery con menor costo de contexto. Un smoke read-only por nombre ya pasó
  en ambas superficies; falta ejecución real, matriz y benchmark.

## ✅ Tareas

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
const tasks=dv.current().file.tasks.array().sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));
const el=dv.el('div','');
el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> **Fase 5 — Beta en proyecto real**
> - [ ] [[AGENTS OS]] Ejecutar sesión 1 con una app Meli elegida usando bootstrap + retrieval #owner/agent #type/dev #area/personal
> - [ ] [[AGENTS OS]] Cerrar sesión 1 generando L0/L1/L3 y logs de cambios #owner/agent #type/dev #area/personal
> - [ ] [[AGENTS OS]] Reindexar Graphify y validar queries #owner/agent #type/dev #area/personal
> - [ ] [[AGENTS OS]] Ejecutar sesión 2 con agente fresco y medir qué contexto recupera #owner/agent #type/dev #area/personal
> - [ ] [[AGENTS OS]] Repetir con Claude, Cursor y Antigravity además de Codex #owner/agent #type/dev #area/personal
> - [ ] [[AGENTS OS]] Escribir reporte beta con métricas, aprendizajes y decisión go/no-go #owner/agent #type/research #area/personal
>
> **Fase 6 — Hardening post-beta (pendiente)**
> - [ ] [[AGENTS OS]] Evaluar/implementar watcher post-beta si el reindex manual fue fricción real #owner/agent #type/dev #area/personal
> - [ ] [[AGENTS OS]] Forward-test Codex invocando skills canónicas sin copias por superficie #owner/agent #type/research #area/personal
> - [ ] [[AGENTS OS]] Forward-test Claude invocando skills canónicas sin copias por superficie #owner/agent #type/research #area/personal
> - [ ] [[AGENTS OS]] Validar discovery nativo tras reiniciar cada superficie y distinguir caché de sesión de capacidad real #owner/agent #type/research #area/personal
> - [ ] [[AGENTS OS]] Comparar rule-routing, path explícito y discovery nativo con tokens, latencia y tasa de éxito #owner/agent #type/research #area/personal
> - [ ] [[AGENTS OS]] Definir mecanismo optimizado de carga de skills sin crear otra fuente física #owner/agent #type/dev #area/personal

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes AGENTS OS/agentes/AGENTS OS - Beta y Hardening
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes AGENTS OS/agentes/AGENTS OS - Beta y Hardening
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes AGENTS OS/agentes/AGENTS OS - Beta y Hardening
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes AGENTS OS/agentes/AGENTS OS - Beta y Hardening
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-08-01** — Proyecto archivado tras consolidar todo el trabajo abierto
  relevante en [[AGENTS OS - Fase 2]].
- **2026-07-14** — Se fijó `80-agents/skills/` como única ubicación física.
  Se removieron adapters por superficie y se abrió el trabajo de validación y
  optimización separado para Codex y Claude. Smoke read-only por nombre:
  aprobado en ambas superficies contra el `SKILL.md` canónico. Una sesión
  Codex ya abierta conservó el catálogo anterior, por lo que el benchmark
  nativo debe comenzar desde procesos reiniciados.
- **2026-07-01** — Proyecto de agente creado por migración desde el roadmap de [[AGENTS OS]] (Fase 5 completa + el ítem pendiente de watcher de Fase 6), como corrección de la deuda flageada en la bitácora de AGENTS OS del 2026-07-01 y en las consecuencias de [[project-ownership-human-vs-agent]]. Las Fases 0-4 y los ítems ya cerrados de Fase 6 quedaron como historial de diseño en el proyecto padre (ver Bitácora de [[AGENTS OS]] para el motivo de no migrarlos).

## 🧭 Decisiones

- Se migró solo la ejecución **abierta** (Fase 5 completa + el ítem pendiente de watcher de Fase 6), no el roadmap histórico ya cerrado (Fases 0-4 y el resto de Fase 6), porque ese historial no es ejecución activa que requiera supervisión vía tarea puente — es registro de diseño ya completado. Ver judgment call en el log de migración `80-agents/journal/logs/2026-07-01-agents-os-self-migration-agent-project.md`.

## 🔗 Docs / Links

- [[AGENTS OS]] (proyecto padre)
- [[agents-os]] (guía operativa)
- [[project-ownership-human-vs-agent]] (decisión que originó el modelo y flageó esta deuda)
- `80-agents/skills/agents-os-agent-project-workflow/SKILL.md` (cómo operar este proyecto)
