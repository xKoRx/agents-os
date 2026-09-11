---
type: user_preference
schema_version: 1
scope: area
created: 2026-07-27
updated: 2026-09-11
area: "[[Meli]]"
entities:
  - "[[Meli]]"
related:
  - "[[rjara-agent-profile]]"
  - "[[rjara-vpn-routing-preferences]]"
confidence: verified
load_policy: when_area_loaded
indexable: true
index_priority: high
tags:
  - area/meli
  - kind/user-preference
  - scope/area
---

# rjara — Preferencias de trabajo Meli

## Preferencias de interacción

- Hereda las preferencias de interacción del perfil global [[rjara-agent-profile]].

## Preferencias de trabajo

- La VPN aplicable a trabajo corporativo se resuelve en [[rjara-vpn-routing-preferences]].
- **Metodología del equipo Signals: Spellbook (SDD), no Jira.** Todo trabajo
  parte por un **SPEC funcional**, luego **SPEC técnica**, luego **tasks** y
  recién ahí implementación. El tracking de tareas vive en Spellbook, no en
  Jira. (Equipo anterior VIS usaba Jira; ya no aplica.)
- Antes de aplicar un finding, comparar la branch contra su base y separar
  regresión introducida, comportamiento heredado y cambios locales. Sin
  regresión de la branch, no editar.
- Sincronizar ramas con `sync-local-branch`: actualizar la base local, merge
  local conservador, commit de merge y push desde la rama objetivo. No crear
  ramas desde remoto, reescribir commits ni hacer force-push.
- Ante cambios trackeados sin commit, archivos funcionales no trackeados o
  conflicto ambiguo, detenerse. Preservar sin staging configuración de
  herramientas no funcional (`.agents/`, `.codex/`, `.claude/`, IDEs,
  `graphify-out/`) salvo instrucción contraria.
- Para pruebas o PRs no mergeados usar versión explícita de test (`0.0.x-<descripcion>`), nunca una versión productiva. Una versión limpia `X.Y.Z` sólo se crea, fija y publica desde `master` después del merge; jamás desde una feature.
- Agregar comentarios en código solo cuando sean necesarios y profesionales.
- **Descripción de PR: recurso del proyecto en el vault, nunca archivo en la raíz del repo.** Se crea junto a la nota del proyecto, con la estructura del template `.github` del repo destino (uno por repo cuando el cambio es cross-repo) y **siempre nombrando la branch y su base**. Queda prohibido `descripcion_pr.md` en root: se cuela en el diff del PR que describe, se pierde al cambiar de branch y queda fuera del grafo. El code review usa [[signals-code-review]] y la descripción se delega a [[pr-description]].
