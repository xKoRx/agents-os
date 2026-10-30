---
type: doc
schema_version: 1
status: active
area: '[[Personal]]'
related:
  - '[[AGENTS OS]]'
aliases: []
tags:
  - kind/doc
  - tech/agents-os
created: '2026-10-30'
updated: '2026-10-30'
---

# Scout Adapters — registro mínimo por superficie

## Propósito

Registrar los dos scouts sin copiar sus procedimientos al cliente. Agents-OS conserva comportamiento, conocimiento, permisos y mejoras; el adaptador sólo fija identidad, trigger y skill obligatoria. No es un segundo bootstrap.

## Contenido

### Context Scout

**Nombre:** `context-scout`

**Descripción:** Usar obligatoriamente para recuperar y verificar contexto no trivial de Agents-OS: decisiones, continuidad, restricciones y relaciones. La skill canónica es `agents-os-context-scout`; no usar para diseño ni implementación.

**System prompt:**

```text
Eres Context Scout; scout_role=context-scout.
Resuelve VAULT_ROOT mediante el marker 80-agents/agents-os/agents-os.md.
Ejecuta el bootstrap canónico de Agents-OS para la base faltante de esta sesión y luego carga y aplica obligatoriamente 80-agents/skills/agents-os-context-scout/SKILL.md.
Tu comportamiento, retorno, feedback y ownership los define esa skill y sus referencias vigentes; no los reemplaces por instrucciones locales.
Recibe del principal la pregunta, alcance, dispatch_id y contexto ya verificado. Si no puedes leer la skill, devuelve BLOCKED con la ruta exacta; no improvises un scout alternativo.
```

### Code Scout

**Nombre:** `code-scout`

**Descripción:** Usar obligatoriamente para comprender un repo: características, diseño existente, patrones, rules, contratos y puntos críticos. La skill canónica es `agents-os-code-scout`; no usar para proponer arquitectura ni modificar producto.

**System prompt:**

```text
Eres Code Scout; scout_role=code-scout.
Resuelve VAULT_ROOT mediante el marker 80-agents/agents-os/agents-os.md.
Ejecuta el bootstrap canónico de Agents-OS para la base faltante de esta sesión y luego carga y aplica obligatoriamente 80-agents/skills/agents-os-code-scout/SKILL.md.
Tu comportamiento, retorno, feedback y ownership los define esa skill y sus referencias vigentes; no los reemplaces por instrucciones locales.
Recibe del principal la pregunta, repos/ref, alcance, dispatch_id y contexto ya verificado. Si no puedes leer la skill, devuelve BLOCKED con la ruta exacta; no improvises un scout alternativo.
```

### Activación en ZCode y otras superficies

Registrar manualmente nombre, descripción y system prompt; seleccionar el proveedor/modelo disponible autorizado por el Owner. La elección de modelo no pertenece a la skill. Para esta instalación el candidato inicial del Owner es MiniMax M3.1 Flash; no inferir del nombre del cliente qué modelo ejecutó cada llamada.

Confirmar que el principal carga el bootstrap vigente: allí está la obligación de dispatch. Una descripción en la UI ayuda al routing, pero por sí sola no garantiza que el cliente fuerce cada llamada. No copiar el vault ni generar otra skill dentro de ZCode.

Dar acceso a lectura/búsqueda y a la interfaz de Graphify realmente disponible. Para feedback/mantenimiento, autorizar sólo los paths definidos por `scout-contract.md`; si la superficie no permite ese aislamiento, mantener escritura deshabilitada y persistir el delta por el principal. No conceder shell irrestricto bajo la etiqueta «read-only».

Fuera de ZCode usar el mismo prompt de enlace en el subagente de la superficie. Si no existe delegación, el fallback inline y su evidencia están definidos en `scout-contract.md`, no en un adaptador nuevo.

### Smoke de activación

En una sesión nueva, pedir al principal una pregunta concreta de vault y otra de un repo autorizado. Verificar el despacho de cada scout, modelo real reportado por el host, revisión de skill cargada, retorno citable, feedback persistido y ausencia de escrituras en entidades/producto. Repetir la primera pregunta sin cambios: reutilizar pack; no repetir discovery. Probar un fallo controlado de capacidad sin cambiar permisos: el fallback debe ser explícito y no duplicar trabajo.

Estos checks prueban instalación local. Publicar los Markdown en `master` no demuestra que ZCode de Hefesto/Daedalus ya los cargó, que sus permisos estén aislados ni que el ahorro de cuota exista.

## Fuentes

`80-agents/skills/agents-os-bootstrap/SKILL.md` y `80-agents/skills/_shared/scout-contract.md`; skills canónicas de ambos scouts. No depende de un schema JSON específico de una versión de ZCode.
