---
type: skill
name: sync-local-branch
scope: global
created: 2026-07-15
updated: 2026-08-08
description: Sincroniza una rama Git local con otra rama Git local mediante pull literal de la base, merge local, resolución conservadora de conflictos, commit y push. Usar cuando el usuario pida sincronizar, actualizar o mergear una rama con develop, master o una rama específica.
tags:
  - kind/skill
  - tech/agents-os
  - action/git
  - scope/local
---

# Sync Local Branch

## Purpose

Ejecutar sincronizaciones entre ramas locales preservando los cambios de ambas ramas y evitando operaciones remotas o destructivas no autorizadas.

## Minimal Read

Read only:
1. `80-agents/agents-os/agent-constitution.md`.
2. `80-agents/memory/public/user-preference/rjara-agent-profile.md`.
3. Estado Git del repositorio objetivo.

## Procedure

Inputs:
- `target_branch`: rama que recibirá la sincronización.
- `base_branch`: rama local desde la que se sincroniza.
- `repo_path`: raíz Git del repositorio.

1. Resolver `repo_path` sin asumir el directorio actual. Verificar que sea la raíz Git correcta.
2. Ejecutar `git status --short --branch` y clasificar por separado cambios trackeados y archivos no trackeados.
3. En repos Meli, permitir por defecto archivos y carpetas no trackeados que sean configuración local o artefactos operativos sin impacto en la funcionalidad de la rama, por ejemplo `.agents/`, `.codex/`, `graphify-out/`, `.claude/`, `.idea/`, `.vscode/` y equivalentes. Preservarlos intactos, no agregarlos al commit y no incluirlos en el push.
4. Bloquear solo si existen cambios trackeados sin commit, archivos no trackeados que parezcan código/tests/recursos funcionales, o una ruta no trackeada que pueda ser sobrescrita por un archivo de `target_branch` o `base_branch`. No hacer `stash`, `reset`, `clean`, checkout destructivo ni commit de trabajo ajeno.
5. Verificar que `target_branch` y `base_branch` existan como ramas locales con `git branch --list`. No crear ninguna desde `origin` ni desde otra referencia remota.
6. Posicionarse en la base y ejecutar literalmente:
   ```bash
   git switch <base_branch>
   git pull
   ```
   No usar `fetch`, `pull --rebase`, `pull <remote> <branch>` ni opciones adicionales.
7. Volver a la rama objetivo y ejecutar literalmente:
   ```bash
   git switch <target_branch>
   git merge <base_branch>
   ```
8. Si hay conflictos:
   - listar los archivos en conflicto con `git status`;
   - leer el contexto de ambos lados;
   - conservar la funcionalidad de la rama objetivo y de la base;
   - resolver con cambios mínimos, sin borrar una implementación por conveniencia;
   - verificar que no queden marcadores `<<<<<<<`, `=======` o `>>>>>>>`;
   - ejecutar las validaciones relevantes del módulo si están disponibles;
   - revisar `git diff --cached` antes de continuar.
   Si el conflicto no se puede resolver con evidencia suficiente, detenerse y pedir decisión; nunca elegir silenciosamente un lado completo.
9. Confirmar que el diff contiene solo el merge y las resoluciones necesarias. No incluir archivos ajenos, archivos no trackeados permitidos ni artefactos generados.
10. Agregar únicamente los archivos resueltos y crear el commit con:
   ```bash
   git add <archivos-resueltos>
   git commit -m "merge <base_branch>"
   ```
   Para `develop`, el mensaje exacto es `merge develop`.
11. Desde `target_branch`, ejecutar literalmente:
    ```bash
    git push
    ```
    No usar `--force`, `--force-with-lease`, otro remoto ni otra rama.
12. Verificar estado final, commit creado y rama publicada. Los artefactos no trackeados permitidos pueden seguir presentes y deben permanecer sin staging.

## Output

```text
Repositorio:
Rama objetivo:
Rama base:
Estado inicial:
Pull local de base:
Merge local:
Conflictos:
Validaciones:
Commit:
Push:
Estado final:
Bloqueos o decisiones pendientes:
```

## Hard Rules

- Las ramas deben existir localmente antes de iniciar.
- La política por defecto es exclusivamente local; no hacer fetch, crear ramas desde remotos ni sustituir una rama ausente por `master`, `develop` u otra sin instrucción explícita.
- No usar `reset`, `clean`, `stash`, rebase, cherry-pick, squash, force-push ni comandos que oculten o reescriban commits.
- No iniciar si existen cambios trackeados sin commit, archivos no trackeados funcionales o colisiones de rutas; permitir y preservar artefactos locales de configuración/agente/Graphify que no afecten la funcionalidad.
- No resolver conflictos eliminando cambios de la rama objetivo o de la base sin evidencia y decisión explícita.
- No mezclar cambios no relacionados ni artefactos generados en el commit de merge.
- Si cualquier precondición falla, detenerse antes de cambiar ramas.
