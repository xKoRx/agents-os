---
type: doc
schema_version: 1
status: active
tags:
  - kind/doc
  - kind/system
created: 2026-06-24
updated: 2026-08-10
---

# 🧭 Convenciones del Second Brain

## Propósito

Definir las convenciones humanas del vault sin duplicar los contratos ejecutables de AGENTS OS.

## Contenido

## Estados de tarea (plugin Tasks)

Al clickear el checkbox, la tarea avanza al siguiente estado:

| Símbolo | Estado | Avanza a |
|---------|--------|----------|
| `[ ]` | To Do | WIP |
| `[/]` | WIP | Review |
| `[r]` | Review | Done |
| `[x]` | Done | To Do |
| `[-]` | Canceled | To Do |

> Al clickear, la tarea avanza por el ciclo: To Do → WIP → Review → Done → (vuelve a To Do). Para saltar directo a un estado (o cancelar), usa el menú contextual del checkbox / el modal de edición (⌘⇧Y).

## Tipos de tarea (tags)

| Tag | Uso |
|-----|-----|
| `#type/dev` | Desarrollo: código, PRs, fixes |
| `#type/admin` | Gestión: releases, permisos, reuniones, Jira, configs |
| `#type/research` | Spikes, refinamiento, investigación, definiciones |
| `#type/pr-review` | Revisar PRs de otros / QA |
| `#type/supervision` | **Tarea puente**: arrancar + dar seguimiento a un proyecto de agente. No la ejecutas tú, la vigilas. Ver [[#Proyectos humanos vs proyectos de agente]] |

## Tags flag (opcionales, conviven con cualquier estado)

- `#blocked` — bloqueada por una dependencia
- `#waiting` — esperando a alguien/algo
- `#urgent` — urgente

## Tags de contexto

- `#area/<slug>` — área (ej. `#area/meli`). Alimenta el panel del área.
- `#sprint/<id>` — sprint (ej. `#sprint/A26Q2S7`). Alimenta la nota del sprint.
- `#quarter/<id>` — quarter (ej. `#quarter/A26Q3`).
- `#app/<slug>` — aplicación relacionada (ej. `#app/search-middleware`).
- `#topic/<slug>` — tema transversal (ej. `#topic/polycard`).
- `#idea/<slug>` — tipo de idea (ej. `#idea/validation`).
- `#size/<slug>` — tamaño aproximado de idea/tarea no planificada (ej. `#size/small`).

## Naming canónico y enlaces

La identidad de una entidad se separa en tres capas:

- **Nombre canónico:** el nombre exacto del archivo/nota y destino de links
  Obsidian. Ejemplo: `[[Meli]]`, `[[Áreas]]`, `[[java-polycard-sdk]]`.
- **Alias:** variantes humanas o históricas en frontmatter `aliases`. Ejemplo:
  `meli`, `MELI`, `Mercado Libre`.
- **Slug técnico:** identificador lowercase/kebab-case para tags, paths y filtros.
  Ejemplo: `area/meli`, `project/agents-os`, `app/search-middleware`.

Reglas:

- Los links internos deben apuntar siempre al nombre canónico exacto.
- Si el texto visible necesita otra forma, usar alias visual:
  `[[Meli|meli]]`, no `[[meli]]`.
- `area`, `project`, `application`, `entities` y `related` deben usar links
  canónicos cuando referencian entidades.
- En notas de entidad, usar `slug:` para el identificador técnico de la propia
  entidad. No usar `area: meli` para representar identidad; `area:` queda
  reservado para routing hacia una nota de área, por ejemplo `area: "[[Meli]]"`.
- Los tags siguen siendo slugs técnicos y no reemplazan los links canónicos.
- Antes de crear una nota nueva, buscar por filename, heading, alias, slug, repo
  y path local para evitar duplicados por mayúsculas, acentos o singular/plural.

## Ejemplo de tarea

```
- [/] Implementar cliente Sugeridor bypass-cache #type/dev #area/meli #sprint/A26Q2S7
```

## Ownership: humano vs agente

El seguimiento distingue **quién conduce la ejecución**, en dos niveles.

### Tareas (tags)

- `#owner/me` — tarea humana: la haces tú.
- `#owner/agent` — tarea de agente: la ejecuta un agente dentro de un proyecto de agente.
- Sin tag de owner → queda visible en el bloque "🧺 Sin owner" para que la corrijas.

### Proyectos (frontmatter `owner`)

- `owner: me` — **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
- `owner: agent` — **proyecto de agente**: un curro delegado con detalle pesado, que escribe y sigue un agente.

## Proyectos humanos vs proyectos de agente

Un **proyecto de agente** es casi siempre subproyecto de uno humano. Reglas:

1. **Carpeta:** vive en la subcarpeta `agentes/` de su iniciativa (ej. `10-projects/Destaques de Precio/agentes/`). Los links `[[...]]` no se rompen al mover, son por nombre.
2. **Parent obligatorio:** `parent: "[[Proyecto humano padre]]"`.
3. **Tarea puente:** en el proyecto **padre** existe UNA sola tarea humana que lo representa:
   ```
   - [ ] [[Proyecto de agente]] arrancar + seguimiento #owner/me #type/supervision #area/meli
   ```
   Su estado refleja **tu** relación con el curro: `[ ]` no arranqué → `[/]` lo sigo → `[r]` reviso la entrega → `[x]` cerrado.

Efecto: tu cockpit ("Mis tareas") ve **una línea** por curro delegado, no las tareas internas del agente. Las tareas `#owner/agent` viven dentro del proyecto de agente.

Cómo un agente debe **operar** ese proyecto sesión a sesión (la nota como planificador único, actualización continua de tareas/estado/bitácora, ciclo de la tarea puente WIP→Review→Done/rechazo) está definido en la skill `80-agents/skills/agents-os-agent-project-workflow/SKILL.md`.

## Regla anti-huérfano

- Todo **subproyecto** setea `parent`.
- Solo las **iniciativas raíz** (sin `parent`) llevan `root: true`.
- Los proyectos sin `parent` y sin `root` aparecen como **huérfanos** en [[Panel de Proyectos]] para que los adoptes.

## Schema de Sistema 2 (autoridad)

El bloque JSON de `80-agents/skills/_shared/schema-contract.md` es la autoridad
única y versionada para tipos, lifecycle, campos, tags, secciones y mappings
`type → template` de S1/S2. Esta sección conserva sólo la interpretación humana.

Toda nota S2 nueva nace del template que resuelve el contrato, usa su versión
actual y declara el envelope común. Si el tipo tiene lifecycle, el template
materializa un `status` permitido; un evento sin lifecycle no lo inventa.

Los campos adicionales deben cambiar identidad, routing, lifecycle,
provenance u operación. No agregar YAML ceremonial. Los tags filtran; no
reemplazan `type`, `status`, `area` ni links canónicos. La regla anti-huérfano
de proyectos y los contratos de provenance siguen aplicando como invariantes
semánticos.

La cobertura se valida con:

```bash
python3 80-agents/skills/_shared/scripts/validate_schema_contract.py
```

El lint all-vault consume el mismo contrato ejecutable. `--strict <path...>` valida notas nuevas o modificadas sin depender de Git; `--gate` compara fingerprints contra el baseline contratado. Durante una migración permite que la deuda heredada disminuya y bloquea findings nuevos; con baseline vacío es el gate estricto all-vault y cualquier finding bloquea.

### Naming canónico

Aplica lo definido en "Naming canónico y enlaces": el link interno apunta
siempre al título canónico; variantes van en `aliases`; el slug técnico va en
`slug`/tags.

## Ideas

- Las ideas viven como notas atómicas en `30-resources/ideas/`.
- Usan `type: idea`, template `70-templates/idea.md`, `status: seed/exploring/promoted/discarded`, `priority`, y routing explícito (`area`, `project`, `application`, `entities`, `related`).
- Deben ser cortas: una observación, motivo, clasificación y una próxima acción.
- Las áreas las referencian por link canónico y tags; no se duplican como listas manuales permanentes.
- Si una idea exige más de una acción o ya impacta una iniciativa activa, se promueve a tarea o proyecto conservando alias y link de origen.
