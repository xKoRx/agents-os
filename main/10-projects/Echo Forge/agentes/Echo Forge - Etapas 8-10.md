---
type: project
owner: agent
root: false
cssclasses:
  - wide
status: active
priority: P2
area: "[[Echo]]"
parent: "[[Echo Forge]]"
sprint:
start:
due:
progress: 0
repo: symphony
jira:
prs:
tags:
  - area/echo
  - kind/project
created: 2026-06-27
updated: 2026-06-27
aliases:
  - Echo Forge - Etapas 8-10
---
# Echo Forge - Etapas 8-10: Ingesta, Publicación y Escala

> [!info]+ Echo Forge - Etapas 8-10: Ingesta, Publicación y Escala
> **Padre:** [[Echo Forge]] · **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P2 · **Progreso:** 0%
> Integración API-first con Echo Core, publicación en cuentas demo MT5 y escalamiento del pipeline E2E.

## 🎯 Objetivo

- Consolidar la última milla del pipeline: ingestar finalistas en Echo Core de forma segura e idempotente, publicarlos en cuentas demo de MT5 en ejecución continua, y habilitar el escalamiento de waves a producción (500–1000 estrategias).

## 📊 Estado actual

- **Planificado**: Bloqueado conceptualmente por contratos externos (APIs de Echo Core y el mecanismo de attach de MT5). Se implementará mock-first contra contratos propuestos.

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
> - [ ] **Etapa 8: Ingesta en Echo API**
>   - [ ] [[echo-forge]] Diseñar y desarrollar adaptador de cliente API Echo (`FEAT-SQX-ECHO-INGESTION`) #owner/agent #type/dev #area/echo #blocked
>   - [ ] [[echo-forge]] Validar e implementar API con mock server si los contratos reales de Echo Core no están cerrados #owner/agent #type/dev #area/echo
> - [ ] **Etapa 9: Publicación en MT5 y Deployment Link**
>   - [ ] [[echo-forge]] Resolver spike sobre attach desatendido de EA en MT5 (NI-MP-1) #owner/agent #type/research #area/echo
>   - [ ] [[echo-forge]] Desarrollar funcionalidad de publicación y des-publicación en MT5 Demo (`FEAT-SQX-MT5-PUBLISH`) #owner/agent #type/dev #area/echo
>   - [ ] [[echo-forge]] Implementar vínculo de deployment en Echo API (`FEAT-SQX-ECHO-DEPLOYMENT-LINK`) #owner/agent #type/dev #area/echo #blocked
> - [ ] **Etapa 10: Escalamiento y E2E**
>   - [ ] [[echo-forge]] Ejecutar wave de prueba reducida (50 estrategias) para certificación E2E del sistema #owner/agent #type/dev #area/echo
>   - [ ] [[echo-forge]] Escalar el pipeline a waves completas (500-1000 estrategias) en producción #owner/agent #type/dev #area/echo

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes Echo Forge - Etapas 8-10
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes Echo Forge - Etapas 8-10
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes Echo Forge - Etapas 8-10
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes Echo Forge - Etapas 8-10
done
short mode
hide task count
```

## 🔗 Docs / Links

- [[echo-forge]] (Aplicación)
- [SPEC-EF-ECHO-INGESTION](file:///Users/rjara/go/src/github.com/xKoRx/symphony/specs/FEAT-SQX-ECHO-INGESTION/SPEC.md)
- [SPEC-EF-MT5-PUBLISH](file:///Users/rjara/go/src/github.com/xKoRx/symphony/specs/FEAT-SQX-MT5-PUBLISH/SPEC.md)
- [SPEC-EF-ECHO-DEPLOYMENT-LINK](file:///Users/rjara/go/src/github.com/xKoRx/symphony/specs/FEAT-SQX-ECHO-DEPLOYMENT-LINK/SPEC.md)
