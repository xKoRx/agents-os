---
type: learning
scope: project
created: "2026-06-30"
updated: "2026-06-30"
area: "[[Meli]]"
project: "[[Destaques de Precio]]"
application: search-middleware
entities:
  - "[[Meli]]"
related:
  - "[[Destaques de Precio]]"
aliases:
  - clean PR branch reconstruction
  - evitar PRs sucios por merge
confidence: verified
source_session: "2026-06-30-search-middleware-bajo-de-precio-merge"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - workflow/git
  - scope/agent
---

# Reconstruir Ramas De PR Sin Arrastrar Commits Ajenos

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- Cuando el objetivo es "llevar funcionalidad, no commits", no se debe resolver la divergencia copiando un árbol completo desde otra rama ni mergeando ramas correctivas sobre la rama original sin medir el PR resultante.
- El flujo correcto es reconstruir una rama limpia desde el target actualizado, normalmente `origin/develop`, aplicar solo el delta funcional con allowlist de archivos o hunks, y validar con `git diff --name-only origin/develop..HEAD` antes de publicar.
- Si aparecen archivos de otras iniciativas en el diff, se deben restaurar desde `origin/develop` y reaplicar hunks mínimos. Copiar archivos completos desde una rama vieja puede pisar cambios recientes aunque el conteo de archivos parezca razonable.
- Para corregir una rama remota ya contaminada, crear primero un backup local del estado ruidoso y luego publicar la rama limpia con `git push --force-with-lease`, nunca con force ciego.

## Aplicabilidad

- **Cuándo cargarlo:** al sincronizar ramas de PR divergentes, comparar rama original vs rama `*-test`, reconstruir branches sobre `develop`, limpiar PRs con demasiados archivos cambiados, o cuando el usuario pida "no llevar commits, llevar funcionalidades".
- **Cuándo no cargarlo:** merges normales donde el objetivo explícito sea conservar historia completa de otra rama, o ramas compartidas donde no está autorizado reescribir historia remota.

## Entidades relacionadas

- [[Meli]]
- [[Destaques de Precio]]
- search-middleware

## Evidencia

- Fuente: sesión `2026-06-30-search-middleware-bajo-de-precio-merge`.
- Prueba: `feature/bajo-de-precio-motors` quedó contaminada con cambios de proximity/plugin/docs al sincronizar con la rama `*-test`; se corrigió reconstruyendo desde `origin/develop`, aplicando solo los hunks de Bajo de Precio (SDK `polycardVersion = "8.179.0"`) y publicando con `--force-with-lease`.
