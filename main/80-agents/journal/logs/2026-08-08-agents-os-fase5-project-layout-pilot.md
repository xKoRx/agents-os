---
type: change_log
scope: project
created: 2026-08-08
updated: 2026-08-08
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 2]]"
entities:
  - "[[AGENTS OS]]"
  - "[[AGENTS OS - Fase 2]]"
related:
  - "[[agents-os]]"
  - "[[Moves externos del vault requieren rescan de caches de plugins]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/project
  - project/agents-os
---

# AGENTS OS Fase 5 — Piloto de layout por área

## Cambio

- **Tipo:** updated
- **Movimiento:** `10-projects/AGENTS OS/` →
  `10-projects/Personal/AGENTS OS/`.
- **Lote físico:** 8 archivos; ningún rename canónico, symlink, borrado ni
  cambio de parent.
- **Referencias operativas reparadas:** `.graphifyignore`, README raíz,
  `agents-os.md`, `agents-os-install` y builder/README/estado/selección del pack.
- **Derivados regenerados:** `outputs/agents-os-chatgpt/`, ZIP y Graphify.

## Motivo

- Validar D9: `area:` es autoridad semántica y el path refleja navegación.
- Probar una carpeta por proyecto bajo `10-projects/<Área>/<Proyecto>/` antes
  de considerar un retrofit de otros proyectos.

## Fuentes usadas

- [[AGENTS OS - Fase 2]], paquete autónomo Fase 5.
- `90-system/convenciones.md`.
- `80-agents/skills/agents-os-vault-refactor/SKILL.md`.
- Contratos compartidos de metadata, tipos y Graphify.

## Resolución aplicada

- Se preservaron `[[AGENTS OS]]` y `[[AGENTS OS - Fase 2]]` como identidades.
- El pack dejó de exigir el proyecto archivado Beta/Hardening y ahora incluye
  parent + planificador activo.
- Historia, archive, journal, `.trash`, outputs previos y snapshots Graphify no
  se reescribieron como si fueran autoridad vigente.

## Validación

- Lint dirigido: `ERROR=0 WARN=0`, 2 notas.
- Doctor estricto: `HIGH=0 MEDIUM=0 LOW=0`, startup≈4979.
- Pack: 145 archivos, hashes fuente/copia PASS, ZIP PASS.
- Graphify update: exit 0, 5465 nodos, 6284 edges.
- `graphify-obsidian explain "AGENTS OS"`: una entidad en el nuevo path.
- Backlinks `references`: parent/child y consumidores resuelven.
- Pack excluido del grafo por `.graphifyignore`.
- No existen Bases activas ni selectores Dataview/Tasks vivos ligados al path
  anterior. Las tareas fuente y la tarea puente están en el nuevo path.
- Limitación: la caché derivada `.obsidian/plugins/task-board/tasks.json` no se
  autoactualizó ante el move externo; requiere un rescan desde Obsidian. No se
  editó manualmente ni se usó como evidencia canónica.
- El criterio reusable se promovió a
  [[Moves externos del vault requieren rescan de caches de plugins]].

## Recomendación de retrofit

- **GO** para conservar el layout del piloto: identidad, lint, pack y Graphify
  quedaron estables.
- **NO-GO temporal** para un movimiento masivo hasta automatizar o verificar el
  rescan de caches de plugins path-based y repetir el piloto con un proyecto
  que tenga vistas activas de Tasks/Bases.
- Próximo proyecto piloto debe ser un lote pequeño, con owner humano, una vista
  activa y sin archivos pesados.

### Checklist reusable por proyecto

1. Verificar gate/backup y que el destino no exista.
2. Inventariar archivos, referencias vivas, scripts, ignores, vistas y caches.
3. Capturar checksums y escribir move map + rollback exacto.
4. Actualizar referencias operativas; no reescribir historia ni derivados.
5. Mover un solo árbol preservando título, aliases, `area:` y `parent:`.
6. Ejecutar lint dirigido, artifacts/builds, doctor, reindex, `explain` y
   backlinks.
7. Reescanear plugins path-based desde su superficie y verificar una vista real.
8. Emitir recomendación go/no-go antes del siguiente lote.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni paths absolutos de máquina.

## Rollback

1. Confirmar que `10-projects/AGENTS OS/` no exista.
2. Mover `10-projects/Personal/AGENTS OS/` de vuelta a
   `10-projects/AGENTS OS/`.
3. Revertir el mismo set de referencias operativas y restaurar la selección
   previa del pack sólo si vuelve a existir su fuente.
4. Regenerar pack, ejecutar lint/doctor, reindexar y repetir `explain` +
   backlinks.
