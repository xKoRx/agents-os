---
type: project
owner: agent
root: false
status: completed
priority: P2
area: "[[Echo]]"
parent: "[[Echo Forge]]"
sprint: "[[A26Q2S7]]"
start: 2026-07-07
due:
progress: 100
repo: symphony
jira:
prs:
aliases:
  - WFM Dashboard
  - Echo Forge WFM Dashboard
tags:
  - project
  - area/echo
created: 2026-07-07
updated: 2026-07-08
---

# Echo Forge WFM Dashboard

%% Naming: Echo Forge WFM Dashboard es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge WFM Dashboard
> **Área:** [[Echo]] · **Estado:** completed · **Prioridad:** P2 · **Sprint:** [[A26Q2S7]]
> _parent: [[Echo Forge]]_

## 🎯 Objetivo

Desarrollar un visor/dashboard interactivo de Walk-Forward Matrix (WFM) dentro del vault de Obsidian que consuma reportes Markdown generados por el pipeline de Symphony. Esto permitirá a Rodrigo auditar rápidamente los resultados del proceso de optimización, verificar la consistencia del Robust Run, y abrir en el SQX GUI nativo cualquier estrategia sospechosa con un solo clic.

---

## 📊 Estado actual

- **Completado**: Implementación técnica del pipeline, dashboard interactivo DataviewJS en Obsidian y comando `download-wave` en la CLI. Todo compilado, testeado y verificado con éxito.
- **Ubicación**:
  - Dashboard principal: `30-resources/dashboards/echo-forge/Echo Forge WFM Dashboard.md`
  - Base de datos (reportes estructurados): `30-resources/dashboards/echo-forge/bases/` con nomenclatura estructurada.
  - Tarea en Symphony: Actividad `generate_report` integrada en `GenericSQXWorkflow`.

---

## ✅ Tareas

> [!note]+ Tarea Puente
> Este proyecto tiene asignada una tarea puente de tipo supervisión (`#type/supervision`) en el proyecto humano padre [[Echo Forge]].

- [x] Diseñar el esquema YAML del frontmatter para las bases Markdown en `bases/` #owner/agent #type/research #area/echo
- [x] Implementar la actividad `generate_report` en el pipeline de Symphony (`sqx/activities/worker/`) que genere los Markdown estruturados tras finalizar una Wave #owner/agent #type/dev #area/echo
- [x] Crear la estructura de carpetas en Obsidian `30-resources/dashboards/echo-forge/bases/` #owner/agent #type/dev #area/echo
- [x] Desarrollar el visor/intérprete `Echo Forge WFM Dashboard.md` usando DataviewJS y React para leer las bases de markdown y renderizar las grillas Walk-Forward #owner/agent #type/dev #area/echo
- [x] Agregar controles interactivos al Dashboard (filtros dinámicos por wave, instrumento, versión y estado) #owner/agent #type/dev #area/echo
- [x] Desarrollar la opción de descarga rápida en la CLI de Symphony para descargar las estrategias `.sqx` asociadas al reporte visualizado #owner/agent #type/dev #area/echo
- [x] Realizar pruebas E2E con el lote de ejemplo y validar en Obsidian #owner/agent #type/dev #area/echo

---

## 📆 Bitácora

- **2026-07-08** — Implementación técnica completa y validación realizada por el agente. Se crearon el dashboard DataviewJS, la actividad de generación de reportes en Go y el comando `download-wave` en la CLI de Symphony.
- **2026-07-07** — Sesión de diseño conceptual de la visualización en Obsidian. Rodrigo aprueba el enfoque progresivo (Markdown estructurado en `bases/` + visor dinámico DataviewJS/React en el recurso Dashboard) frente a reportes estáticos HTML. Creación de la nota de proyecto.

---

## 🧭 Decisiones de Proyecto

- **Independencia de Código**: Los reportes generados se guardarán como archivos Markdown en una subcarpeta dedicada (`bases/`) separada de las notas generales y fuera de `graphify-out/` para evitar contaminación de contextos del grafo.
- **Filtros Dinámicos en Cliente**: El dashboard en Obsidian cargará dinámicamente el catálogo de notas bajo `bases/` y usará JavaScript para construir los selectores (Wave, Instrumento, Versión) en tiempo de ejecución, eliminando la necesidad de reconstruir el dashboard cada vez.

---

## 🔗 Docs / Links

- [[Echo Forge]] (Proyecto Padre)
- [generic_workflow.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/workflows/generic_workflow.go)
- [robust_activity.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/robust_activity.go)
