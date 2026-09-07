---
type: change_log
schema_version: 1
scope: project
created: "2026-08-10"
updated: "2026-08-11"
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 3]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Aranea]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
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

# AGENTS OS Fase 3 T6.4 — Segundo piloto de layout por área

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Movimiento:** proyecto owner Backup/DR y sus nueve subproyectos agente desde `10-projects/Aranea/` a `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/`.
- **Lote físico:** once notas Markdown, 66.414 bytes; ningún rename canónico, symlink, borrado ni cambio de metadata.
- **Move map:**

| Origen | Destino | SHA-256 de transporte |
|---|---|---|
| `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT.md` | `20f66fa1edc2de53ad33f8378b8786f9051ba0e2fb4839e3928bce691d30810a` |
| `10-projects/Aranea/BACKUP-DR-CONTRACT.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-CONTRACT.md` | `8217aef64c3a835f9b7b427d0d6b370cb130e3351e339de521ae77cf174d6e22` |
| `10-projects/Aranea/agentes/agent-project-00-policy-and-doc-cleanup.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-00-policy-and-doc-cleanup.md` | `65c5ff19a415385273980c99bf821982e9cc7fcdfa406b63acfda4850947e466` |
| `10-projects/Aranea/agentes/agent-project-01-critical-config-backup.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-01-critical-config-backup.md` | `a96b0d05b92a19c2261a346a7f2e1e6a3841cd1735b2f728f34bb7567e2a6a2a` |
| `10-projects/Aranea/agentes/agent-project-02-pbs-on-backup-node.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-02-pbs-on-backup-node.md` | `af922e0c9b9e70d842d523361bb50b3c96e99c6b703028267a5414ba27b2f1ab` |
| `10-projects/Aranea/agentes/agent-project-03-app-consistent-data-backups.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-03-app-consistent-data-backups.md` | `cf1c141e7956d9111255b9e0362a8202c171e650941f9e2d852ba3406fc40ebe` |
| `10-projects/Aranea/agentes/agent-project-04-cloud-critical-tier.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-04-cloud-critical-tier.md` | `2d1d8d4b7c7e697b03c6d08a8ca509ba2a7899b2c12b5e01a865032579b539c0` |
| `10-projects/Aranea/agentes/agent-project-05-cloud-bulk-archive-tier.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-05-cloud-bulk-archive-tier.md` | `fd885da483364d3b6ac49ccfd630b15c3f67c6ca9c5691e3babf7860adf3c22e` |
| `10-projects/Aranea/agentes/agent-project-06-observability-and-alerting.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-06-observability-and-alerting.md` | `a789d1a7ddbcca55aaf3a56f97346ea188f345164a40e1e54cd3e6b7da059ca0` |
| `10-projects/Aranea/agentes/agent-project-07-restore-drills.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-07-restore-drills.md` | `ad69936ff8184783344f6975bd765b08a5b508dac1114edb83a693849847f9ba` |
| `10-projects/Aranea/agentes/agent-project-08-session-closeout-and-learning-loop.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-08-session-closeout-and-learning-loop.md` | `432eb11ef0f3446065381ca452f1dcaab390a677c4d3ba5fa526f999c40daeda` |

## Motivo

- Ejecutar R21/T6.4 con un segundo proyecto humano, pequeño y consumido por una vista real de Task Board antes de generalizar el layout `10-projects/<Área>/<Proyecto>/`.
- El lote declara `area: [[Aranea]]`, no tiene destino previo ni archivos pesados, cumple schema v1 en strict y ejercita identidad, parent/children, links tipados y cache path-based.

## Fuentes usadas

- [[AGENTS OS - Fase 3]], R21 y T6.4.
- [[AGENTS OS Fase 5 — Piloto de layout por área]], checklist reusable y recomendación del primer piloto.
- [[Moves externos del vault requieren rescan de caches de plugins]].
- [[BACKUP-DR-OWNER-PROJECT]], fuente canónica del proyecto piloto.
- [[BACKUP-DR-CONTRACT]] y `30-resources/aranea/03-storage/backup-dr/00-index.md`, referencias path-based vigentes que deben seguir el move.

## Resolución aplicada

- Preservar títulos canónicos, contenido, metadata y checksums; el nuevo subárbol agrupa el proyecto owner, su contrato vivo y sus subproyectos agente bajo el área ya declarada.
- Actualizar sólo las tres referencias operativas path-based vigentes; no reescribir journal, outputs ni caches derivadas como si fueran autoridad.
- La reparación de `30-resources/aranea/00-index.md` lo migró al schema v1, normalizó sus dos tags legacy, alineó sus headings contractuales y reemplazó dos paths absolutos de máquina por `VAULT_ROOT`.
- Task Board debe descubrir los paths nuevos mediante su scanner nativo; Graphify debe reconstruir file-node IDs y preservar relaciones semánticas por título.
- Probar el rollback físico real, verificar el hash restaurado y reaplicar exactamente el mismo move antes de aceptar el piloto.

## Validación

- **Baseline pre-move:** destino ausente; strict de once notas `0 ERROR / 0 WARN`; hashes capturados; Graphify resolvía `BACKUP-DR-OWNER-PROJECT.md` en `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT.md` con 33 conexiones y backlinks `references` vivos; Task Board contenía 130 ocurrencias de los once paths origen y Workspace ninguna.
- **Forward move:** los once hashes de transporte coincidieron antes de reparar referencias; strict de las fuentes afectadas `0 ERROR / 0 WARN`; no quedan referencias path-based live a los orígenes.
- **Rollback real:** referencias vigentes revertidas, once archivos restaurados con hashes exactos, carpeta destino ausente, strict `0/0`; Graphify reconstruyó `5118/6101`, recuperó el file-node origen con 33 conexiones y dejó cero nodos bajo el destino.
- **Forward definitivo:** once file-nodes en el subárbol nuevo, parent y children resuelven, parent conserva 33 conexiones y sus backlinks; Graphify `5118/6101`; lint global `0 ERROR / 0 WARN`, gate `new=0 resolved=175`, strict dirigido y contrato ejecutable verdes.
- **Cache Task Board:** el move externo reprodujo la cache stale (`old=130`, `new=0`). El scanner nativo no pudo automatizarse porque macOS niega acceso de eventos a esta superficie (`CGPreflightPostEventAccess=false`); no se editó `tasks.json` a mano. T6.4 permanece WIP hasta ejecutar `Cmd+P` → `Task Board: Open vault scanner` → scan completo y verificar `old=0`, paths nuevos presentes y tablero real operativo.
- **Reverificación 2026-08-11:** `.obsidian/plugins/task-board/tasks.json` sigue siendo JSON válido y contiene `28` valores string con la ruta anterior y `0` con el prefijo del subárbol nuevo. Es un conteo estructural posterior, distinto de las `130` ocurrencias textuales del baseline pre-move; confirma que el scanner nativo todavía no se ejecutó. El derivado no se modificó.
- **Scanner nativo 2026-08-11:** el owner ejecutó el scanner completo de Task Board sobre 1560 archivos. La cache read-only posterior quedó JSON válida, con `old=0`, `new=139`, los once paths nuevos presentes y 117 tareas pendientes distribuidas entre el owner y sus nueve subproyectos; no se editó el derivado manualmente.
- **Decisión:** GO final del segundo piloto; T6.4 queda cerrada y el patrón de layout puede adoptarse con scanner nativo obligatorio después de moves externos.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin paths absolutos de máquina, memoria interna ni secretos.

## Rollback

- Confirmar que los once orígenes no existan y que cada destino conserve su SHA-256 esperado.
- Mover los nueve subproyectos desde `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/` a `10-projects/Aranea/agentes/`, luego restaurar `BACKUP-DR-CONTRACT.md` y `BACKUP-DR-OWNER-PROJECT.md` en `10-projects/Aranea/`; retirar las carpetas destino sólo si quedan vacías.
- Revertir las dos referencias operativas path-based, ejecutar el scanner nativo de Task Board, reindexar Graphify y verificar que los orígenes resuelvan una sola identidad sin referencias al destino.
