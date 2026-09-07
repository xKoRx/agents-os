---
type: project
owner: agent
root: false
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
aliases:
  - Echo Forge - Desacoplamiento SOLID del Pipeline
tags:
  - project
  - area/echo
created: 2026-07-11
updated: 2026-07-11
---

# Echo Forge - Desacoplamiento SOLID del Pipeline

> [!info]+ Echo Forge - Desacoplamiento SOLID del Pipeline
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P2 · **Padre:** [[Echo Forge]]
> Rediseñar e implementar el motor del pipeline en Go para desacoplar la exportación de metadatos de las tareas tipo `project` (retester/optimizer) y delegar responsabilidades de forma pura.

## 🎯 Objetivo

- Convertir la tarea `project` en un ejecutor puro de configuraciones SQX.
- Mantener los cinco proyectos fijos `EchoForgeOverviewExporter`, `EchoForgeWFMExporter`, `EchoForgeTradeListExporter`, `EchoForgeMT5Exporter` y `EchoForgeRobustRunExporter` como piezas independientes seleccionables por la definición dinámica del flujo.
- Eliminar la lógica de inyección de exportación implícita de `02_retester` y `03_optimizer`.
- Asegurar que `evaluate_wfm`, `apply_selected_run` y `generate_report` definan explícitamente sus orígenes mediante `source_folder`.

## 📊 Estado actual

- **Planificado**: Analizando el impacto de los cambios sobre las actividades de Temporal (`generic_workflow.go`, `steps.go` e `import_metadata.go`).

## ✅ Tareas

🤖 Tareas del agente:
- [/] **Fase 1: Planificación detallada y Estructura en Vault**
  - [x] Crear esta nota de proyecto en el Vault #owner/agent #type/admin #area/echo
  - [/] Crear el plan arquitectónico detallado `PLAN.md` en el repositorio #owner/agent #type/dev #area/echo
- [ ] **Fase 2: Refactorización en Go (TaskSpecs y Registros)**
  - [ ] Extender el registro/configuración dinámica de tareas `project` para seleccionar cualquiera de los cinco `EchoForge*` por nombre, sin mappings estáticos por tipo ni secuencia hardcodeada #owner/agent #type/dev #area/echo
  - [ ] Modificar `generic_workflow.go` y `steps.go` para desactivar el trigger implícito de `ImportMetadataStep` en tareas de tipo `project` #owner/agent #type/dev #area/echo
- [ ] **Fase 3: Implementación de Tareas Dedicadas**
  - [ ] Validar que la tarea `project` ejecute Overview, WFM, TradeList, MT5 o RobustRun de forma aislada según la definición del flujo #owner/agent #type/dev #area/echo
  - [ ] Modificar `evaluate_wfm` para consumir explícitamente el output declarado de `EchoForgeWFMExporter`, sin invocarlo implícitamente #owner/agent #type/dev #area/echo
  - [ ] Modificar `apply_selected_run` y `generate_report` para usar explícitamente `source_folder` #owner/agent #type/dev #area/echo
- [ ] **Fase 4: Despliegue y Verificación en Zeus**
  - [ ] Ejecutar compilación local y pruebas unitarias `go test ./sqx/...` #owner/agent #type/dev #area/echo
  - [ ] Desplegar la nueva versión del worker en Zeus mediante `./deploy_sqx.sh` #owner/agent #type/dev #area/echo
  - [ ] Lanzar corrida de prueba (wave v10) y verificar la ejecución en caliente #owner/agent #type/dev #area/echo

## 📆 Bitácora

- **2026-07-11** — Creación del proyecto de agente en Obsidian para documentar el desacoplamiento.
- **2026-07-23** — Corrección de arquitectura: se elimina la propuesta de mappings estáticos por tipo. Los cinco proyectos `EchoForge*` son piezas independientes elegidas por la configuración dinámica del flujo; ningún paso debe invocar implícitamente a otro exporter.
