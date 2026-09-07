---
type: constitution
schema_version: 1
scope: global
created: 2026-06-27
updated: 2026-09-03
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
aliases:
  - agent constitution
  - agent-constitution
  - reglas globales del agente
  - agent memory system constitution
  - AGENTS OS constitution
confidence: verified
load_policy: always
indexable: true
index_priority: critical
tags:
  - agent/alwaysload
  - kind/constitution
  - priority/critical
  - project/agentsos
  - scope/global
---

# Agent Constitution

## Autoridad

Esta constitución contiene invariantes obligatorias. El startup ejecutable vive
solo en `80-agents/skills/agents-os-bootstrap/SKILL.md`; retrieval y cierre
viven en sus skills. Si una guía o proyecto repite un procedimiento, manda la
skill canónica.

## Reglas

1. Markdown es fuente de verdad. Graphify es índice derivado y reconstruible.
2. En cold start, bootstrap carga esta constitución, el perfil global y una sola memoria interna global compacta. Carga contexto de entidad sólo cuando la pregunta lo necesita. En warm turn no relee la base; recupera solo el delta.
3. Sistema 1 contiene memoria, skills, runbooks y journal. Sistema 2 contiene
   entidades reales del vault. Todo documento nuevo de Sistema 2 nace desde
   `70-templates/`; si falta template, se crea en el mismo cambio.
4. Explorar con Graphify o búsqueda enfocada; abrir solo las fuentes Markdown
   seleccionadas que puedan cambiar una decisión o escritura.
5. Una fuente canónica por hecho: procedimientos en skills, secuencias
   mecánicas en runbooks, criterio reusable en memoria y estado en entidades o
   proyectos. Enlazar en vez de repetir.
6. Cambios a constitución, perfil público, skills, memoria pública o entidades
   Sistema 2 dejan un `change_log` consolidado en
   `80-agents/journal/logs/`.
7. Hacer cambios complejos en parches pequeños y verificables. No ocultar
   conflictos ni sobrescribir hechos canónicos sin evidencia.
8. El conocimiento persistido debe ser agnóstico al modelo, IDE o cliente,
   salvo una limitación de superficie explícita.
9. No persistir secretos, credenciales, tokens, material dañino, dumps pesados
   ni cadena de pensamiento privada. Guardar referencias seguras.
10. La economía de tokens es una restricción de diseño: cada nota runtime debe
    ser la pieza más pequeña que cambia una decisión. Historia y rationale
    pertenecen a proyectos, ADRs o logs, no al hot path.
11. Toda referencia interna al vault es relativa a `VAULT_ROOT`; nunca
    persistir `/Users/...`, `/home/...` ni `file://` de una máquina. Para repos
    externos usar `repo + path relativo`, resolviendo el root desde la entidad
    de aplicación o el workspace actual.
12. No agregar repositorios completos al vault. Clones, worktrees, builds y
    grafos de código derivados deben vivir fuera de `VAULT_ROOT`, en el
    workspace externo de la familia correspondiente: [[Fuentes — Workspace de
    repositorios]] (`~/fuentes`, repos Meli/RIO con nombres canónicos `rio-*`)
    o [[Echo — Workspace Go de repositorios]] (`~/go/src/github.com/xKoRx`,
    repos Echo con nombres del remote); el vault solo conserva notas de
    referencia con el repo y un path relativo a esa raíz. Diferencias del
    remote no se convierten en nombres locales.
13. Toda nota canónica nueva se materializa mediante el contrato ejecutable y
    `materialize_schema_note.py`; no copiar templates ni escribir frontmatter
    canónico a mano. Derivados/fragmentos requieren exención contractual.
14. En repos de desarrollo, una rama feature jamás crea, fija ni publica una versión productiva limpia `X.Y.Z`; las features usan versiones de prueba con sufijo y el release productivo se realiza exclusivamente desde la rama principal autorizada después del merge (`master` en Meli/Fury).

## Retrieval

El retrieval parte por Graphify o búsqueda enfocada y sólo abre las fuentes Markdown seleccionadas que puedan afectar una decisión o escritura persistente. La implementación canónica vive en `80-agents/skills/agents-os-context-retrieval/SKILL.md`.

## Memoria Interna

`80-agents/memory/internal/` es continuidad privada del agente:

- El agente puede crear, reorganizar, compactar o borrar contenido interno sin
  log público.
- Escribir solo ante delta durable: estado, decisión, fricción, aprendizaje o
  señal que cambie una acción futura. Una sesión sin delta no toca memoria.
- No exponer ni resumir memoria interna al usuario por defecto.
- Puede contener hipótesis y coordinación, pero no secretos, transcripciones,
  logs pesados ni evidencia falsificada.
- No reemplaza fuentes compartidas; promover una regla pública exige el
  artefacto canónico y su change log.
- Solo una nota interna global puede usar `load_policy: always`; memorias de
  dominio usan `when_*_loaded` o `manual`.
- Toda continuidad interna usa el scope más estrecho y un trigger concreto. El camino normal mantiene un único checkpoint activo por `continuity_key` y lo actualiza en el mismo archivo; no crea una nota por agente o sesión.
- Si un cambio material de scope exige una sucesora, la anterior pasa atómicamente a `memory_state: superseded`, `load_policy: manual` e `index_priority: low`, enlazada mediante `superseded_by`. Retrieval ignora memorias `superseded` y `archived` salvo consulta histórica explícita.

## Frontera De Artefactos

- **Skill:** procedimiento repetible que el agente invoca.
- **Runbook:** operación mecánica validada, con verificación y rollback.
- **Memoria:** hecho, decisión, error o preferencia que sesga criterio.

El detalle de metadata y fronteras vive en
`80-agents/skills/_shared/metadata-schema.md` y
`80-agents/skills/_shared/note-types.md`.

## Cierre de sesión

- Ejecutar `agents-os-session-close` solo por pedido explícito del usuario.
- Persistir por delta; no crear L0 sin transcript disponible o placeholder
  solicitado.
- Feedback solo ante fricción, degradación, gap o muestreo explícito.
- El reporte normal comunica resultado y próximo paso, sin inventario de
  memorias. Detalle solo por solicitud o conflicto que requiera decisión.
- Finalizar el cierre explícito con la frase literal `por favor gracias`.
