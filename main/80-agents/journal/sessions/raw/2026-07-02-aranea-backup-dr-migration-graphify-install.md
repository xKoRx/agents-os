---
type: raw_session
scope: session
created: 2026-07-02
updated: 2026-07-02
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[Aranea]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[graphify]]"
  - "[[10-projects/Aranea]]"
  - "[[30-resources/tools/graphify]]"
aliases: []
confidence: verified
source_session: ariadna-2026-07-02-telegram
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
  - project/agents-os
  - area/aranea
---

# 2026-07-02-ariadna-aranea-backup-dr-migration-graphify-install

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Ariadna (perfil Hermes Agent, MiniMax-M3, Telegram)
- Proyecto o entidad: [[Aranea]] (homelab) + [[AGENTS OS]] (sistema de memoria)
- Objetivo de la sesión: dos tareas secuenciales —
  1. (Owner-driven) Mover el proyecto Backup/DR de `30-resources/aranea/03-storage/backup-dr/` a `10-projects/Aranea/` por convención PARA.
  2. (Owner-driven) Instalar `graphify-obsidian` en la VM Hermes para retrieval del vault.

## Transcript

### Fase 1 — Bootstrap y validación de convención del vault

```
Owner: "pero si te pedí que crearas el proyecto en 10-projects... pero antes de comenzar a hacer el cambio.... ves las reglas del vault? no hay algo que te diga que todo proyecto que tiene plazo y tareas se guarda en 10-projects? de ahí quiero poner carpetas por área que en este caso es aranea y dentro de esa carpeta que pongas este proyecto, que son las tareas a realizar. en resources va la documentación, esa que es prácticamente evergreen, este como es un proyecto y tiene tiempo y plazo va en 10-projects"
```

Agente: lee `80-agents/agents-os/agents-os.md` (constitución), carga skill
`second-brain-vault-conventions`, lee `90-system/convenciones.md`, lee
`20-areas/Aranea.md`, ve que `BACKUP-DR-OWNER-PROJECT.md` ya existe en
`30-resources/aranea/03-storage/backup-dr/` y que es efectivamente un
proyecto con plazo + tareas (no evergreen) → confirma plan de migración
con el owner y espera "correcto, eso es" antes de mover.

### Fase 2 — Migración Backup/DR (15 archivos movidos + 5 actualizados + 2 creados)

- mkdir `10-projects/Aranea/`, `agentes/`, `05-tickets/`
- mv proyecto + 9 subproyectos + 4 tickets
- patch frontmatter: `area: "[[Personal]]"` → `[[Aranea]]"` en 14 archivos
- patch frontmatter: `area/personal` → `area/aranea` en 14 archivos
- patch proyecto: agregar `owner: me`, `root: true`, `priority: P1`, `start`, `due`,
  `progress`; renombrar `parent: "[[BACKUP-DR-DESIGN]]"` →
  `design_ref` (era incorrecto, BACKUP-DR-DESIGN es doc de recursos)
- sed en tickets 018-021: rutas relativas `[[../03-storage/backup-dr/...]]`
  rotas → links canónicos (los agent-project-* migrados rompen la ruta)
- sed en agent-project-00: rutas `../DESIGN-PROPOSAL.md` rotas →
  `../../../../30-resources/aranea/03-storage/DESIGN-PROPOSAL.md`
- reescribir `30-resources/aranea/03-storage/backup-dr/00-INDEX.md`
  como índice de docs evergreen (no del proyecto)
- crear `10-projects/Aranea/README.md` (índice por área)
- actualizar `30-resources/aranea/00-index.md` § mapa de documentación
  (líneas 119-120)
- actualizar `20-areas/Aranea.md` línea "Propuesta activa" →
  "Proyecto activo: [[10-projects/Aranea/BACKUP-DR-OWNER-PROJECT]]"
- actualizar `30-resources/aranea/05-tickets/README.md` →
  status: legacy (histórico)
- agregar nota de migración en `30-resources/aranea/03-storage/backup-dr/DIFF-CONCEPTUAL.md`
- crear log en `80-agents/journal/logs/2026-07-02-aranea-backup-dr-migration-to-10-projects.md`

Validación final: `search_files pattern="03-storage/backup-dr/(BACKUP-DR-OWNER-PROJECT|agent-project)"`
→ 0 resultados (cero links rotos a las rutas viejas).

### Fase 3 — Instalación graphify-obsidian (segunda tarea del owner)

```
Owner: "quiero que instales graphify en la máquina para que la puedas
usar con el usuario hermes. la idea es que puedas buscar por ahí los
documentos del vault"
```

Agente: lee `30-resources/tools/graphify.md`, ve que el binario NO está
instalado pero hay wrapper legacy `~/bin/graphify-aranea` que falla
limpio. Wrappers esperados por la doc canónica: `graphify`,
`graphify-obsidian`, `graphify-personal`. PyPI metadata: paquete
`graphifyy` 0.9.4 (Safi Shamsi, MIT, requires python >= 3.10, deps
networkx + numpy + tree-sitter). Entry points: `graphify`,
`graphify-mcp`. Confirmo con owner:

```
Agente: "Confirmaste instalar. Pero el alcance exacto no. ¿Qué hago?"
Owner: "si dale, instala, luego el uso debe ser de fácil uso ojo.. ideal
que puedas crear un wrapper para llamarlo por graphify-obsidian, así
está me parece en las reglas"
```

Plan aplicado:
- NO usar `uv` (no estaba instalado, y `pip3` global es PEP 668).
- Crear venv dedicado: `python3 -m venv ~/.local/share/graphify-venv`
- `~/.local/share/graphify-venv/bin/pip install graphifyy` (instala
  graphifyy 0.9.4 + 30 dependencias tree-sitter + numpy 2.4.6 + networkx 3.6.1).
- Crear wrapper `~/.local/bin/graphify-obsidian` (BASH, ~5 KB) que:
  - apunta a `~/.local/share/graphify-venv/bin/graphify`
  - fija VAULT = `~/obsidian/SecondBrain/main`
  - fija GRAPH_DIR = `<VAULT>/95-graphify/obsidian`
  - para `update`, fuerza `--out-dir` al GRAPH_DIR canónico
  - para `query/explain/path/affected/diagnose`, fuerza `--graph` al
    `<GRAPH_DIR>/graph.json`
  - muestra VAULT y GRAPH en stderr antes de cada ejecución
  - fail limpio con exit 2 si falta argumento
  - pasa `--help` al upstream para catálogo completo
- `chmod +x` y symlink `~/.local/bin/graphify` → `graphify-obsidian`
- El wrapper legacy `~/bin/graphify-aranea` ya estaba bien diseñado
  (delega a `graphify` o `graphify-obsidian`); el `for cand in graphify
  graphify-obsidian` ahora encuentra ambos y el wrapper funciona sin
  cambios.

Smoke tests ejecutados (todos exit 0):
- `graphify-obsidian --help` → muestra help propio
- `graphify-obsidian explain "Aranea"` → nodo `10-projects/Aranea/README.md`,
  community 26, 6 connections EXTRACTED (el grafo ya estaba al día)
- `graphify-obsidian query "BACKUP-DR-OWNER-PROJECT agent-project-02 PBS" --budget 300`
  → 21 nodos encontrados en BFS depth=2
- `graphify-obsidian path "Aranea" "ticket-018"` → "No path found" +
  warning de ambigüedad (no crash; funciona correctamente)
- `graphify-aranea explain "Aranea"` → delega correctamente al nuevo wrapper

### Fase 4 — Documentación post-instalación

- actualizar `30-resources/tools/graphify.md`:
  - frontmatter: `updated: 2026-07-02`, agregar campos
    `installed_in_vm`, `installed_path`, `wrapper_path`,
    `wrapper_legacy`
  - cuerpo: estado actualizado (✅ INSTALADO), tabla comandos, sección
    "Estado actual en VM Hermes" reescrita, sección de instalación
    renombrada a "Instalación histórica"
- log en `80-agents/journal/logs/2026-07-02-graphify-install-in-vm-hermes.md`

### Fase 5 — Owner pide cierre

```
Owner: "ok, cierra sesión"
```

Agente: aplica skill `session-handover`. Crea:
- L0 raw session (este archivo)
- L1 summary
- feedback de sesión
- handover block en `10-projects/Aranea/README.md` (top del index)
- memory update con hechos durables

## Evidencia externa

- 15 archivos en `10-projects/Aranea/` (1 proyecto, 9 subproyectos, 4 tickets, 1 README)
- 9 archivos en `30-resources/aranea/03-storage/backup-dr/` (solo evergreen)
- 2 logs en `80-agents/journal/logs/` (migración + install graphify)
- Binario: `~/.local/share/graphify-venv/bin/graphify` (graphifyy 0.9.4)
- Wrapper: `~/.local/bin/graphify-obsidian` (5229 bytes, ejecutable)
- Symlink: `~/.local/bin/graphify` → `graphify-obsidian`
- Grafo vivo: `95-graphify/obsidian/graph.json` (3.0 MB, last mod 2026-07-02 05:25 UTC, contiene ya la migración 10-projects/Aranea/ que ocurrió esta mañana)
- Smoke tests de `graphify-obsidian explain/query/path` con exit 0
