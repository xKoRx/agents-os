---
type: runbook
schema_version: 1
scope: global
created: 2026-07-05
updated: 2026-09-03
area:
project:
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
  - "[[Economía de Tokens]]"
aliases:
  - instalar graphify-obsidian
  - graphify-obsidian install
  - install graphify fork
confidence: verified
source_session:
load_policy: when_installing_graphify_obsidian
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/global
  - tech/agents-os
  - tech/graphify
  - action/install
---

# Instalar graphify-obsidian (fork vault-aware)

%% Routing: entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Instalar el índice de retrieval de AGENTS OS (`graphify-obsidian`) en una máquina que
comparte el vault pero **no** tiene la app. Deja funcionando el comando `graphify-obsidian`
con índice y artefactos locales a esa máquina, fuera del vault. Fuente de verdad
del contrato: `[[agents-os]]` y `80-agents/skills/_shared/graphify-contract.md`.

## Precondiciones

- Python 3.10+ y `uv` disponibles (`uv --version`). Sin `uv`: `pip install uv` o usar `pip` en su lugar.
- Ejecutar el runbook desde la raíz del vault o definir `AGENTS_OS_VAULT`.
- Fuente de instalación local: un wheel en
  `~/.local/share/graphify-obsidian/dist/`, o un checkout indicado por
  `AGENTS_OS_GRAPHIFY_SOURCE`. Los binarios no viajan dentro del vault.
- Wrapper canónico:
  `80-agents/skills/agents-os-graphify-install/scripts/graphify-obsidian`.

## Procedimiento

1. **Instalar el compilado (la app) en un venv aislado.** No contamina `graphify` (Work) ni
   `graphify-personal`; el fork vive en su propio venv. Instala el `.whl` con el extra `[all]`
   (las dependencias se bajan de PyPI):

   ```bash
   LOCAL_DIST="$HOME/.local/share/graphify-obsidian/dist"
   WHL=$(ls -1 "$LOCAL_DIST"/graphifyy-*-py3-none-any.whl | tail -1)
   uv venv "$HOME/.local/share/graphify-obsidian/venv" --python 3.12
   uv pip install --python "$HOME/.local/share/graphify-obsidian/venv/bin/python" "${WHL}[all]"
   ```

   Si no existe wheel local y sí existe `AGENTS_OS_GRAPHIFY_SOURCE`, instalar
   `"${AGENTS_OS_GRAPHIFY_SOURCE}[all]"`. Si no existe ninguna fuente local,
   detenerse: el vault no es un registry de artefactos.

2. **Instalar el wrapper.** Copiar la versión canónica del vault a `~/bin/` y hacerlo ejecutable:

   ```bash
   mkdir -p "$HOME/bin"
   cp "$VAULT/80-agents/skills/agents-os-graphify-install/scripts/graphify-obsidian" \
     "$HOME/bin/graphify-obsidian"
   chmod +x "$HOME/bin/graphify-obsidian"
   ```

3. **Asegurar `~/bin` en el PATH** (si `which graphify-obsidian` no lo encuentra):

   ```bash
   echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.zshrc" && exec zsh
   ```

4. El wrapper resuelve `VAULT_ROOT` desde `AGENTS_OS_VAULT`, el directorio
   actual o `~/.config/agents-os/vault-root`. No editarlo por máquina.

## Validación

- El compilado responde: `graphify-obsidian --help` (muestra ayuda del wrapper + flags heredados).
- La versión actual responde `graphify 0.9.6.post2`, expone `filter` más `query --filter` y preserva bajo `relations` todas las variantes semánticas que comparten source-target.
- **Estado fuera del vault** (requisito clave): `cache-path` debe resolver bajo
  el cache home de la máquina. `GRAPHIFY_MD_VAULT_ROOT` se limita a la copia
  temporal y nunca apunta el output al vault.
- Inspección y query con auto-refresh:

  ```bash
  graphify-obsidian cache-path
  graphify-obsidian status
  graphify-obsidian explain "AGENTS OS"
  ```
- `explain` reconstruye automáticamente si falta o está stale. La deuda global
  de lint se informa sin bloquear el auto-refresh local; un `update` manual sí
  mantiene el gate estricto. Un error del extractor conserva el último índice válido.

## Rollback / recuperación

- Compilado corrupto o falta el venv (el wrapper aborta con exit 42): repetir Paso 1.
- Regresión de relaciones lossless: reinstalar explícitamente un wheel local
  de rollback con `--reinstall --no-deps`; Markdown no cambia porque el índice es derivado.
- Volver a un estado limpio: `rm -rf "$HOME/.local/share/graphify-obsidian/venv"` y reinstalar (Paso 1).
- Regenerar un compilado nuevo (máquina origen):
  `cd <graphify-repo> && uv build --wheel`, luego guardarlo en
  `~/.local/share/graphify-obsidian/dist/` o publicarlo en un registry externo.
- Para limpiar el índice local, borrar sólo la ruta exacta devuelta por
  `graphify-obsidian cache-path`; la próxima query lo reconstruye.

## Evidencia

- Compilado actual y provenance: `80-agents/skills/agents-os-graphify-install/BUILD.md`.
- Wrapper canónico: `80-agents/skills/agents-os-graphify-install/scripts/graphify-obsidian` → se instala en `~/bin/graphify-obsidian`.
- Contrato: `80-agents/skills/_shared/graphify-contract.md`.
- Skill que ejecuta este runbook: `80-agents/skills/agents-os-graphify-install/SKILL.md`.
