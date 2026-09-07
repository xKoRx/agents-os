---
type: project
cssclasses:
  - wide
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Destaques de Precio]]"
sprint: "[[A26Q2S7]]"
start:
due:
progress: 0
repo: vis-items-loader-tagging, search-middleware, vis-octopus-lib, vpp-backend
jira:
prs:
tags:
  - area/meli
  - kind/project
created: 2026-06-24
updated: 2026-07-03
aliases:
  - Destaques de Precio (tiers)
  - Hito 2
  - Hito 2 - Destaques de Precio
---

# Bajo y Muy Bajo Precio

> [!info]+ Bajo y Muy Bajo Precio (Hito 2)
> **Padre:** [[Destaques de Precio]] · **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** [[A26Q2S7]]
> Diseño en curso. **MLB**: destaque único basado en precio FIPE (pivot 2026-06-30). **Sites no-MLB**: tiers `PRECIO MUY BAJO` / `PRECIO BAJO` vía Sugeridor 2.0. Ambos forman parte de este mismo proyecto (Hito 2), con implementación base común y condiciones de tageo por site.

## 🎯 Objetivo

- **MLB**: calcular un destaque único server-side comparando contra precio FIPE (pivot 2026-06-30, detalle y puntos abiertos en el RFC).
- **Sites no-MLB**: calcular tier (`MUY_BAJO` / `BAJO`) server-side con Sugeridor 2.0.
- En ambos casos: renderizar en Search + VIP, con reproceso masivo quincenal (la fuente de cálculo se ramifica por site; el resto del pipeline es compartido).

## 📊 Estado actual

- En fase de diseño. Propuesta de continuación de la iniciativa.
- **MLB (FIPE)**: bloqueado por (a) confirmar fuente técnica del precio FIPE, (b) confirmar rango real de elegibilidad (el -10%/-1% mencionado en la reunión es ilustrativo), (c) lista marca/modelo/año de exclusión de ítems mal catalogados, en revisión por el equipo sin ETA.
- **Sites no-MLB (Sugeridor)**: falta cliente Sugeridor bypass-cache y proceso masivo. Rollout vigente (2026-07-03): MLA+MLM primero por disponibilidad del Sugeridor; luego resto de sites no-MLB en paralelo.
- **Diseño técnico Hito 2**: debe escalar el flujo existente de Bajó de Precio. Pendientes clave: atributos mínimos/booleanos filtrables, caché de Search API Go, consumer de cambios de atributos, consumer de procesamiento común con prioridad Hito 2 antes que Hito 1, y proceso masivo paginado que encola al mismo consumer.
- **RFC**: continuación de Hito 2 en curso — ver [[RFC Destaques de Precio - Hito 2|proyecto de agente de desarrollo del RFC]].
- **Specs técnicas (Sugeridor, MLA/MLM)**: creadas en Spellbook el 2026-07-01, en estado `review` (propuesta con puntos abiertos, no implementación) — ver Docs/Links.
- **Implementación**: proyecto humano creado — ver [[Implementación Hito 2 - Destaques de Precio]]. Organiza subproyectos por aplicación y tareas puente para proyectos de agente.

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
> - [x] Refinamiento #owner/me #type/research #area/meli
> - [/] Análisis #owner/me #type/research #area/meli #sprint/A26Q2S7
> - [/] Diseño #owner/me #type/research #area/meli #sprint/A26Q2S7 📅 2026-07-03
> - [ ] Preparar tests LTP para inicio de implementación #owner/me #type/dev #area/meli #sprint/A26Q2S7
> - [/] [[RFC Destaques de Precio - Hito 2]] arrancar + seguimiento #owner/me #type/supervision #area/meli #sprint/A26Q2S7
> - [ ] [[Implementación Hito 2 - Destaques de Precio]] implementación + seguimiento #owner/me #type/dev #area/meli #sprint/A26Q2S7
> - [x] Crear specs técnicas de Search y VIP (Sugeridor, MLA/MLM) en Spellbook #owner/agent #type/dev #area/meli #sprint/A26Q2S7
> - [ ] Revisar y aprobar en Spellbook los specs técnicos de Search y VIP (Sugeridor) para pasarlos a `ready_to_code` e importar las tasks preparadas #owner/me #type/research #area/meli #sprint/A26Q2S7
> - [ ] tarea 
> %% Las tareas de desarrollo se agregarán desde el second brain del proyecto. %%

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes Bajo y Muy Bajo Precio
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes Bajo y Muy Bajo Precio
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes Bajo y Muy Bajo Precio
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes Bajo y Muy Bajo Precio
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-06-24** — 
- **2026-07-01** — Corrección de alcance: este proyecto es la "parte 2" / **Hito 2** completo del RFC (fase de diseño), no solo el esquema de tiers vía Sugeridor. Incluye tanto el destaque único FIPE de MLB como los 2 tiers vía Sugeridor del resto de sites — ambos ramificados dentro de este mismo proyecto, no repartidos entre este proyecto y el padre [[Destaques de Precio]].
- **2026-06-30** — Reunión de equipo: FIPE en MLB tiene ítems mal catalogados (Cris: vehículos verificados podrían tener el FIPE correcto porque los proveedores lo devuelven en validaciones históricas). Decisión, dentro de este mismo proyecto: **MLB** pivota a un destaque único basado en precio FIPE; el **resto de los sites** mantiene el diseño original de 2 tiers vía Sugeridor 2.0, sin FIPE. Rango ilustrativo (no confirmado) de -10%/-1% vs FIPE mencionado para MLB. Lista marca/modelo/año de exclusión en revisión por el equipo, sin ETA. Detalle completo y puntos abiertos en el RFC.
- **2026-07-01** — Confirmado el rollout de Hito 2 (vía Sugeridor 2.0) en **MLA y MLM**; MLM deja de ser "candidato por madurez" y queda en scope funcional confirmado, como segundo site de validación después de MLA. Actualizado el RFC (`rfc.md`) y las specs técnicas de Search y VIP en `sb-main/01_Projects/previous-price-motors/` para reflejarlo, dejando explícito que MLB queda fuera de esos documentos (usa flujo FIPE separado). Se crea [[RFC Destaques de Precio - Hito 2]] como proyecto de agente para continuar el desarrollo del RFC/specs con seguimiento propio.
- **2026-07-01** — Se crean en Spellbook las specs técnicas de Hito 2 (Sugeridor 2.0, MLA/MLM), como continuación de las specs funcionales ya existentes ahí: **Search** en proyecto Upper Funnel (`VMDUPPER`, spec `9b8e70ce-f46a-497b-9df7-4b1ab2c99208`, dependencia de la spec funcional `2513a123-bdfe-481d-98d0-f7bfb3d572fe`) y **VIP** en proyecto Mid Funnel (`VISMDMID`, spec `93d572e8-4d58-4876-8e1c-71653b58f035`, dependencia de la spec funcional `ddf10fe9-af96-4208-9eac-01bfb71abfe5`). Contenido migrado 1:1 desde las "Spec Técnica Propuesta" locales de `sb-main`. Ambas quedan en estado `review` (no `ready_to_code`): siguen siendo propuestas con puntos abiertos (ver §12 de cada doc), no aprobadas ni implementadas — no correspondía auto-aprobarlas para forzar la importación de tasks. Se prepararon localmente las tasks de implementación (`tasks-destaques-precio-search.json`, `tasks-destaques-precio-vip.json` en `sb-main/01_Projects/previous-price-motors/`) listas para `POST .../tasks/import` una vez que cada spec tenga ≥1 aprobación y pase a `ready_to_code`, siguiendo el mismo patrón ya usado para Hito 1 (Bajó de Precio). MLB queda fuera de ambas specs (flujo FIPE separado, documentado solo en el RFC).
- **2026-07-03** — Se actualiza el RFC legacy con el orden de despliegue vigente: **MLA + MLM primero** porque la nueva versión del Sugeridor ya corre hace tiempo en ambos sites; después **resto de sites no-MLB en paralelo**; y **MLB** después de MLA/MLM como carril separado FIPE. También queda explícito que la implementación base es común para todos los sites y que la diferencia vive en las condiciones de tageo por site.
- **2026-07-03** — Se actualiza el RFC legacy con la iteración técnica de Hito 2: atributos mínimos y preferentemente booleanos quedan como pendiente, junto con agregarlos a caché Search API Go y conversar filtrabilidad con Search. El procesamiento debe escalar el consumer/flujo existente de Bajó de Precio: cambios de precio + nuevo consumer de cambios de atributos alimentan un consumer común, que evalúa primero Bajo/Muy Bajo y luego Bajó de Precio. El proceso masivo queda como orquestador paginado que encola items al consumer común. Observabilidad, experimentos y rollout operativo quedan `TBD`.
- **2026-07-03** — Corrección de target documental: el RFC fuente de Hito 2 es `RFC Destaque de precio — Hito 2.md`, no `rfc.md`. Se aplicó ahí la iteración técnica vigente: atributos mínimos/booleanos pendientes, caché Search API Go, filtrabilidad Search, consumer común escalado desde Bajó de Precio, consumer de cambios de atributos, proceso masivo paginado y Experimentos/Rollout/Observabilidad como `TBD`.
- **2026-07-03** — Se crea [[Implementación Hito 2 - Destaques de Precio]] como proyecto humano de implementación, con proyectos de agente por aplicación: [[Hito 2 - vis-items-loader-tagging]], [[Hito 2 - Search API Go]], [[Hito 2 - search-middleware]], [[Hito 2 - java-polycard-sdk]], [[Hito 2 - vis-octopus-lib]] y [[Hito 2 - vpp-backend]]. Se corrigen/crean specs técnicas locales para productor, Search y VIP.

## 🧭 Decisiones

- Sin allowlist de dominio (`vertical:motors`). Reproceso masivo idempotente.
- **2026-06-30**: el diseño de este proyecto se ramifica por site — FIPE (destaque único) en MLB, Sugeridor 2.0 (2 tiers) en el resto. FIPE queda exclusivo de MLB. Detalle en el RFC.
- **2026-07-03**: rollout secuenciado: MLA+MLM primero, resto de sites no-MLB después en paralelo, MLB después de MLA+MLM como carril FIPE. La implementación base se mantiene común; sólo cambian las condiciones de tageo por site.
- **2026-07-03**: el diseño técnico debe partir de Bajó de Precio y escalar sus componentes. No crear una línea paralela si el consumer/procesamiento existente puede evolucionar. Prioridad funcional: Hito 2 antes que Hito 1.
- **2026-07-03**: la implementación se gestiona desde un proyecto humano separado con subproyectos de agente por aplicación y tareas puente en el padre, siguiendo `agents-os-agent-project-workflow`.

## 🔗 Docs / Links

- **Spellbook — Spec Funcional Search**: proyecto `VMDUPPER` (Upper Funnel), spec `2513a123-bdfe-481d-98d0-f7bfb3d572fe` (status: review)
- **Spellbook — Spec Técnica Search**: proyecto `VMDUPPER` (Upper Funnel), spec `9b8e70ce-f46a-497b-9df7-4b1ab2c99208` (status: review)
- **Spellbook — Spec Funcional VIP**: proyecto `VISMDMID` (Mid Funnel), spec `ddf10fe9-af96-4208-9eac-01bfb71abfe5` (status: draft)
- **Spellbook — Spec Técnica VIP**: proyecto `VISMDMID` (Mid Funnel), spec `93d572e8-4d58-4876-8e1c-71653b58f035` (status: review)
- [Tasks preparadas — Search](file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/tasks-destaques-precio-search.json) (para importar cuando el spec técnico pase a `ready_to_code`)
- [Tasks preparadas — VIP](file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/tasks-destaques-precio-vip.json) (ídem)
- [Spec Técnica Search — fuente local (legacy, migrada a Spellbook)](file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/Destaques%20de%20Precio%20%E2%80%94%20Polycard%20Search%20%E2%80%94%20Spec%20T%C3%A9cnica%20Propuesta.md)
- [Spec Técnica VIP — fuente local (legacy, migrada a Spellbook)](file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/Destaques%20de%20Precio%20%E2%80%94%20VIP%20%E2%80%94%20Spec%20T%C3%A9cnica%20Propuesta.md)
- [Spec Técnica Producer — fuente local](file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/Destaques%20de%20Precio%20%E2%80%94%20vis-items-loader-tagging%20%E2%80%94%20Spec%20T%C3%A9cnica%20Propuesta.md)
- Proyecto implementación: [[Implementación Hito 2 - Destaques de Precio]]
