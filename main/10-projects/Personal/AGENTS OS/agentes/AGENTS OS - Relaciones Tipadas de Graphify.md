---
type: project
schema_version: 1
owner: agent
root: false
status: completed
priority: P0
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start: 2026-08-11
due:
progress: 100
repo: graphify
jira:
prs:
aliases:
  - AGENTS OS Graphify Typed Relations
  - Graphify Multi-relación Tipada
tags:
  - kind/project
  - area/personal
  - project/agents-os
  - tech/graphify
created: 2026-08-11
updated: 2026-08-11
---

# AGENTS OS - Relaciones Tipadas de Graphify

> [!info]+ Correctitud de relaciones tipadas
> **Padre:** [[AGENTS OS]] · **Owner:** agent · **Estado:** completed · **Prioridad:** P0 · **Repo:** `graphify`

## 🎯 Objetivo

- Evitar que Graphify pierda una relación tipada cuando una nota declara dos relaciones de frontmatter con el mismo par source-target, preservando compatibilidad con los grafos y comandos existentes.

## 📊 Estado actual

- **Proyecto completado y aceptado por el owner.** T0.1–T2.2 completas; wheel `graphifyy 0.9.6.post2` construido, documentado e instalado. La reproducción demostró que la extracción conservaba `references`, `child_of` y `related_to`, pero `build_from_json` dejaba sólo `related_to`; ahora `relation` mantiene compatibilidad y `relations` conserva el conjunto lossless. Validación: 74 tests focalizados; suite completa `2844 passed, 28 skipped`; Ruff verde; grafo de código `10415/17579`; strict/gate vault `0/0`; reindex final de cierre `5138/6134`; Context Router `14/14`, 0 misses y precisión proxy 100%.

## 🧩 Subproyectos

- Ninguno.

## ✅ Tareas

> [!note]+ Fuente única de planificación
> Estas tareas `#owner/agent` viven sólo en este proyecto. El cockpit padre conserva una única tarea puente humana de supervisión.

> [!example]- Fuente de tareas del proyecto de agente
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] T0.1 Reproducir la pérdida `child_of` + `related_to` para el mismo source-target y localizar el punto de colapso #owner/agent #type/research #area/personal
> - [x] T0.2 Definir el contrato compatible para representar y consultar múltiples relaciones por par #owner/agent #type/research #area/personal
> - [x] T1.1 Implementar la representación lossless sin romper consumidores legacy de `relation` #owner/agent #type/dev #area/personal
> - [x] T1.2 Adaptar serialización, `affected`, `path` y demás consumidores que filtren relaciones #owner/agent #type/dev #area/personal
> - [x] T1.3 Agregar fixtures y regresiones dirigidas para relaciones tipadas múltiples, colisiones con `references` y grafos legacy #owner/agent #type/dev #area/personal
> - [x] T2.1 Ejecutar suite focalizada y completa, Ruff y actualización del grafo de código #owner/agent #type/dev #area/personal
> - [x] T2.2 Construir e instalar el wheel, reindexar el vault y validar Context Router E2E #owner/agent #type/dev #area/personal

## 📆 Bitácora

- **2026-08-11** — El owner aceptó la entrega y pidió cierre explícito. El proyecto pasa `active→completed`; la tarea puente pasa Review→Done y no quedan tareas abiertas en esta iteración.
- **2026-08-11** — T2.1–T2.2 completas y entrega en Review. La primera suite completa expuso 13 fallas ambientales porque `core.hooksPath` global contaminaba los repos temporales; aislando `GIT_CONFIG_GLOBAL` quedó `2844 passed, 28 skipped`. Ruff y grafo de código quedaron verdes. Se construyó e instaló `0.9.6.post2` con SHA-256 `fd36205f41f9d9455c67f40cca1d191e1662b7c6f7146a9aebe23e56c57dc4a8`; gate `0/0`, reindex `5138/6133`. El E2E inicialmente detectó que el nuevo proyecto era un tercer hijo legítimo de [[AGENTS OS]]; se actualizó la expectativa canónica y la repetición pasó `14/14`, 0 misses y precisión 100%. Resource Wiki, runbook, known error, artefactos y change log quedaron sincronizados; tarea puente WIP→Review.
- **2026-08-11** — T0.1–T1.3 completas. Fixture mínimo: extracción `references + child_of + related_to`, build anterior `related_to` solamente. Se agregó `relations` lossless con fallback al `relation` legacy; `affected` filtra cualquiera de las relaciones preservadas y `path`/`explain` muestran el conjunto. Suite focalizada `74 passed`; Ruff verde. T2.1 queda WIP para la suite completa y actualización del grafo de código.
- **2026-08-11** — Proyecto creado desde el contrato ejecutable; tarea puente WIP en [[AGENTS OS]]. Se inicia T0.1 sobre el fork metadata-aware existente, preservando sus cambios no commiteados.

## 🧭 Decisiones

- D1: se conserva `Graph`/`DiGraph` y el atributo escalar `relation`; cuando un par colapsa variantes semánticas, `relations` guarda la lista ordenada y deduplicada. `MultiDiGraph` no entra en este cambio.
- D2: el gate exige que `affected --relation child_of` y `affected --relation related_to` encuentren el mismo par cuando ambas relaciones existen en Markdown canónico.

## 🔗 Docs / Links

- [[graphify-frontmatter-alias-and-typed-edge-dedup-gaps]] — causa, mitigación legacy y resolución `0.9.6.post2`.
- [[graphify-contract]] — contrato del índice derivado.
- [[AGENTS OS - Fase 3]] — implementación metadata-aware de base.
- Repo `graphify` — fork local en el workspace de repositorios configurado por [[Fuentes — Workspace de repositorios]].

## 💡 Ideas

### Backlog de ideas

- Evaluar `MultiDiGraph` como evolución explícita de formato sólo si la representación compatible resulta insuficiente.

### Motivos / principios

- Markdown conserva todas las relaciones canónicas; el índice derivado no debe descartarlas silenciosamente.

### Memoria pública / interna

- **Memoria pública:** el known error y el contrato Graphify conservan comportamiento, mitigación y resolución reusable.
- **Memoria interna:** no se crea una memoria scoped mientras el planificador contenga todo el estado necesario.
- **Motivo:** evitar duplicar estado de implementación fuera del proyecto activo.
