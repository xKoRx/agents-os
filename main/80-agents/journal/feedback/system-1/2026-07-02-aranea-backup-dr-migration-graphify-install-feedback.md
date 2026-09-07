---
type: feedback
scope: session
created: 2026-07-02
updated: 2026-07-02
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[Aranea]]"
  - "[[AGENTS OS]]"
related:
  - "[[10-projects/Aranea]]"
  - "[[graphify]]"
aliases: []
agent: ariadna
session_goal: "Aplicar convención PARA al proyecto Backup/DR (mover a 10-projects/Aranea/) + instalar graphify-obsidian en VM Hermes."
source_session: ariadna-2026-07-02-telegram
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-07-02 - aranea-backup-dr-migration + graphify-install

## Context

- Agent: Ariadna (Hermes Agent profile, MiniMax-M3, Telegram channel "Rodrigo Jara")
- Session goal: Dos tareas owner-driven en una sesión: (1) mover el proyecto Backup/DR de 30-resources/ a 10-projects/Aranea/ por convención PARA; (2) instalar graphify-obsidian en VM Hermes.
- Main entity: [[Aranea]] (homelab) — específicamente `BACKUP-DR-OWNER-PROJECT` y la tool `graphify`.
- Skills used:
  - `second-brain-vault-conventions` — para validar la decisión de ubicación del proyecto.
  - `note-taking/obsidian` — implícita en toda lectura/escritura del vault.
  - `devops/session-handover` — para el bloque de cierre.
  - Skill `agents-os-bootstrap` — implícita al leer la constitución.
- Retrieval mode: filesystem-first (search_files + read_file). NO se usó graphify (todavía no instalado) para validar el estado del proyecto.
- Artifacts changed: ~18 archivos (15 movidos/creados, 5 actualizados, 2 logs, 1 wrapper, 1 README de handover).

## Scores

1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5 — Constitución y convenciones leídas antes de actuar.
- Retrieval usefulness: 5 — `search_files` con patrones específicos (`03-storage/backup-dr/(BACKUP-DR-OWNER-PROJECT|agent-project)`) confirmó cero links rotos al final; `find` confirmó el wrapper legacy no requería cambios.
- Skill fit: 5 — `second-brain-vault-conventions` cargada justo cuando era relevante; `session-handover` cargada en el cierre.
- Template fit: 4 — Usé `templates/raw-session.md` y `templates/session-summary.md` correctamente, pero improvisé el handover block en el README (no usé un template específico para handover; el README de proyecto es nuevo).
- Closeout friction: 3 — 7 sub-tareas para cerrar limpio (handover, raw, summary, feedback, 2 logs, memory). Owner pidió "cierra sesión" y el agente ejecutó todo el ritual AGENTS OS completo; feedback es que ese ritual es verboso para sesiones cortas — pero útil para sesiones largas.
- Overall confidence: 5 — Todas las acciones verificadas con exits 0 y archivos persistidos.

## What Complicated The Session Most

- **Observation**: el proyecto Backup/DR ya estaba creado en la ubicación equivocada (30-resources/) antes de esta sesión. El agente (yo) participé en esa creación ayer sin aplicar la convención PARA estricta.
- **Why it was hard**: el patrón "crear archivo en 30-resources/03-storage/backup-dr/" parecía razonable en el momento (estábamos construyendo el refactor, todo bajo un mismo techo). Pero convencionalmente, cuando un archivo tiene plazo, owner, subproyectos y tickets, debe vivir en `10-projects/`. Esa decisión requiere leer la convención ANTES de crear, no después.
- **Proposed improvement**: añadir al skill `second-brain-vault-conventions` un check explícito: "Antes de crear/renombrar un archivo `.md` en `30-resources/`, verificar: ¿tiene `owner`, `due`, `parent`? Si sí → mover o crear en `10-projects/<área>/` en su lugar". Otra opción: hacer que el skill devuelva la ruta canónica recomendada como primer output.

## Most Useful Part Of Sistema 1

- **What helped**: la skill `second-brain-vault-conventions` con su tabla "Pick the right folder" + lista de `Common pitfalls`. Esa tabla me confirmó inmediatamente que la decisión correcta era `10-projects/<área>/` y no `30-resources/<área>/`.
- **Why it helped**: la decisión "mover 15 archivos" hubiera requerido re-derivar la convención desde cero sin esa tabla; con ella, fue una confirmación directa.
- **Keep/change**: keep. Es la fuente de verdad operativa.

## Least Useful Or Noisy Part

- **What did not help**: el bucle de patches frontmatter repetitivos (`area: "[[Personal]]"` → `[[Aranea]]"` en 14 archivos) — el agente debería batch-ear esto con un script o detectar el patrón automáticamente.
- **Why it was weak/noisy**: high cognitive load para cambios mecánicos idénticos.
- **Proposed cleanup**: crear un script `vault-migrate-area.sh` o skill `vault-migrate-area` que tome (área origen, área destino, dry-run) y haga el batch de cambios de frontmatter + rutas relativas en una pasada. Skill futura.

## Missing Support

- **Problem not solved by Sistema 1**: detección de rutas relativas rotas en wikilinks automáticamente. Auditoría manual con `search_files` funciona pero es O(N×grep). Para un vault de 300+ archivos, una herramienta de análisis estático de Obsidian sería útil.
- **How Sistema 1 could help next time**: skill `obsidian-link-audit` que liste todas las wikilinks rotas o rutas relativas inválidas del vault.
- **Suggested artifact type**: skill (no aplica, es operación). O un script Python que use el graph.json de Graphify para detectar backlinks huérfanos.

## Retrieval Feedback

- Useful query or source: `search_files pattern="03-storage/backup-dr/(BACKUP-DR-OWNER-PROJECT|agent-project)"` → devolvió 0 resultados post-move, confirmando que ningún archivo apunta a la ruta vieja. Necesario y barato.
- Missing context: ninguna.
- Duplicate/noisy result: ninguno.
- Better future query: usar `graphify-obsidian query "agent-project-02 PBS schedule"` con `--budget 1000` para validar que el grafo refleja la nueva ubicación.

## Skill Feedback

- Skill that worked well: `second-brain-vault-conventions`. Trigger claro, contenido concreto.
- Skill that was confusing: ninguna.
- Trigger/routing gap: cuando el owner dice "instala graphify" o "crea wrapper", no hay skill que enrute a los templates `python3 -m venv` + `pip install`. El agente improvisó el patrón. Considerar agregar skill `hermes-tools-install-from-pypi` con template.
- Suggested contract change: añadir al skill `hermes-agent` (si existe) o crear skill nueva para tools de terceros desde PyPI con instrucciones de "venv dedicado siempre".

## Template Feedback

- Template used:
  - `70-templates/project.md` — base del template de proyecto (no usado directamente; el nuevo `BACKUP-DR-OWNER-PROJECT` se editó a mano conservando campos coincidentes).
  - `80-agents/templates/raw-session.md` — para L0 (usado).
  - `80-agents/templates/session-summary.md` — para L1 (usado).
  - `80-agents/templates/session-feedback.md` — para feedback (usado, este archivo).
  - `80-agents/templates/change-log.md` — para logs en `80-agents/journal/logs/` (usado).
- Field that helped: en `raw-session`, el campo `entities` (link canónico) facilita el grafo de cobertura.
- Field that felt redundant: en `session-summary`, el campo `Memoria propuesta o creada` me obligó a duplicar lo que el bloque "memory update" abajo va a tener. Considerar fusionarlos o referenciar uno al otro.
- Missing field: en `raw-session` y `session-summary`, falta un campo `acceptance_criteria` o `done_definition` — ¿cuándo una sesión está realmente cerrada?

## Memoria Interna (Internal Memory)

- ¿Consulté la memoria interna (`80-agents/memory/internal/`) al iniciar? **No** — solo leí constitución + convenciones + nota canónica de graphify. La memoria interna tiene hechos crudos de sesiones previas; debería haberla escaneado con session_search al inicio (ahorraría reabrir el `30-resources/aranea/00-index.md` que ya tenía info de tickets).
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? Nulo esta vez, porque la memoria inyectada al inicio ya contenía el resumen compacto de Aranea ("aranea propuesta... capex $0... tickets 018-021..."). Memoria interna habría dado más detalle pero no era bloqueante.
- ¿Dejé algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? **No explícitamente** — solo el raw session y el L1 summary quedan como rastro. Memorable en sí no es necesario porque la memoria always-load ya cubre el "qué es Aranea".
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4 — útil para hechos crudos que no van a pública (ej. "agente Y desplegó a producción sin OK del owner" como advertencia interna). Mejorar: hacer que memoria interna se inyecte automática al inicio si hay algo en `80-agents/memory/internal/startup/`.

## Pain Pattern Candidate

- Is this likely to repeat? **yes** — la convención PARA se va a violar cada vez que creemos un proyecto nuevo en `30-resources/` por inercia ("lo dejo donde están los docs del tema"). Necesita guardrail.
- Suggested severity: medium.
- Candidate owner: agente + owner.
- Promote to L3 memory? **yes** (o a una `known_error` en `80-agents/memory/public/known-error/`).

## One Next Improvement

- Crear skill `obsidian-link-audit` + `vault-migrate-area` para automatizar batch de frontmatter y validación de wikilinks rotas. Patrón se repetirá en futuras migraciones (no es la primera ni será la última).
