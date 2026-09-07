---
type: change_log
scope: session
created: "2026-08-04"
updated: "2026-08-04"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[2026-08-04-echo-forge-robust-run-closure-certificate]]"
aliases: []
confidence: verified
source_session: "2026-08-04-sqx-plugin-skill"
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - tech/sqx
  - tech/skills
  - project/echo-forge
---

# Creación de la skill sqx-plugin-lifecycle

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/skills/sqx-plugin-lifecycle/SKILL.md`
  - `80-agents/skills/sqx-plugin-lifecycle/references/echo-forge-build142.md`
  - `80-agents/skills/sqx-plugin-lifecycle/references/deployment-checklist.md`
  - `80-agents/skills/sqx-plugin-lifecycle/agents/openai.yaml`
  - `80-agents/skills/INDEX.md`

## Motivo

- Convertir el aprendizaje validado al corregir y desplegar Robust Run en un procedimiento reutilizable para modificar plugins SQX sin confundir source, packaging histórico y classpath efectivo.

## Fuentes usadas

- Contrato de autoría de skills de AGENTS OS.
- Reglas SDD y build vigente del repositorio Symphony.
- Evidencia certificada de Robust Run sobre SQX Build 142 y tres workers.
- Learnings y known errors públicos sobre carga de Custom Analysis.

## Resolución aplicada

- Se creó una skill agent-facing con gates de autoridad, source-first, descubrimiento del runtime, build simulator/SDK real, despliegue secuencial, backup, actualización quirúrgica de clases, canary semántico y rollback.
- Se aisló el detalle de EchoForge/Build 142 y la lista mecánica de despliegue en referencias lazy-load.
- Se registró la skill en el catálogo canónico y se añadió metadata de superficie no canónica.

## Validación

- `quick_validate.py` fue invocado, pero el runtime disponible no incluye `PyYAML`; se ejecutó la validación equivalente de frontmatter y `openai.yaml` con el parser YAML de Ruby.
- Nombre, campos obligatorios, tags, referencias y límite de líneas validados; `SKILL.md` quedó en 139 líneas.
- Búsqueda de rutas absolutas, credenciales y placeholders realizada.
- Checklist Draft→Ready revisado.
- Forward-test tabletop ejecutado con tres solicitudes realistas: corregir y desplegar Robust Run, auditar una clase que no carga sin modificar, y copiar un JAR completo a los tres workers. La skill enruta correctamente `modify+deploy`, conserva modo read-only en auditoría y bloquea `INSTALL=1`/reemplazo ciego del contenedor.
- `graphify-obsidian update` completó la reextracción, pero el wrapper de consulta siguió buscando `graphify-out/graph.json` mientras la salida viva configurada permanece en `95-graphify/obsidian/`; la validación de descubribilidad queda registrada como gap de infraestructura, no como fallo de la skill.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos.

## Rollback

- Eliminar la carpeta `sqx-plugin-lifecycle`, retirar su fila de `80-agents/skills/INDEX.md` y restaurar la fecha anterior del índice.
