---
type: project
owner: me
root: true
status: active
cssclasses:
  - wide
priority: P2
area: "[[Meli]]"
parent:
sprint:
start:
due:
progress: 100
repo: search-middleware, vpp-backend
jira:
prs:
tags:
  - area/meli
  - kind/project
created: 2026-06-26
updated: 2026-07-01
---

# Automatización despliegue SDK

> [!info]+ Automatización despliegue SDK
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P2 · **Sprint:** —
> Idea transversal: skill que orquesta el despliegue end-to-end de versiones de librerías hacia apps consumidoras.

## 🎯 Objetivo

- Desarrollar una skill reutilizable que, en un **one-shot**, guíe a una IA durante el proceso de publicar una versión test de librería, importarla en el consumidor y desplegar el consumidor a un scope de test para [[search-middleware]] y [[vpp-backend]].

## 📊 Estado actual

- Skill unificada creada: [[30-resources/agents-skills/fury-lib-consumer-deploy/SKILL.md|fury-lib-consumer-deploy]].
> [!IMPORTANT]
> **Requisito obligatorio:** Para la automatización del despliegue en FURY, es indispensable estar conectado a la **VPN**.

## 🔁 Flujo objetivo (one-shot)

1. Desarrollar y **publicar** nueva versión del SDK.
2. **Esperar** a que la versión quede publicada.
3. **Importar** la versión en el repo consumidor (search-middleware / vpp-backend).
4. **Compilar**.
5. **Pushear**.
6. **Desplegar** en scope de **test**.

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
> - [x] Skill despliegue SDK → [[search-middleware]] #owner/agent #type/dev #area/meli ✅ 2026-07-01
> - [x] Skill despliegue SDK → [[vpp-backend]] #owner/agent #type/dev #area/meli ✅ 2026-07-01

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes Automatización despliegue FURY
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes Automatización despliegue FURY
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes Automatización despliegue FURY
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes Automatización despliegue FURY
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-06-26** — Idea capturada como proyecto.
- **2026-07-01** — Creada skill unificada [[30-resources/agents-skills/fury-lib-consumer-deploy/SKILL.md|fury-lib-consumer-deploy]]. Confirma scope obligatorio, nomenclatura `0.0.N-branch-slug`, publicación de librería con `fury create-version`, import en consumidor, commit/push y despliegue test con `fury stage`/`fury deployments`.

## 🧭 Decisiones

- 

## 🔗 Docs / Links

- Apps: [[search-middleware]] · [[vpp-backend]]
