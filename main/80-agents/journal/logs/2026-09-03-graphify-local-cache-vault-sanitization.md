---
type: change_log
schema_version: 1
scope: global
created: 2026-09-03
updated: 2026-09-04
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
indexable: false
index_priority: low
load_policy: audit_only
share_scope: team
tags:
  - kind/change-log
  - scope/global
  - tech/graphify
  - project/agents-os
---

# Graphify local cache and vault sanitization

## Cambio

- Migrated `graphify-obsidian` output from the vault to a machine-local cache
  resolved by `graphify-obsidian cache-path`.
- Query commands now perform a freshness check and rebuild automatically only
  when relevant sources changed. Failed refreshes preserve the last valid graph.
- Builds use unique temporary directories and atomically promote only the JSON
  graph and report; generated HTML, manifests, caches and dated histories are discarded.
- Enabled Obsidian excluded-file filters and LiveSync `.gitignore` support for
  `95-graphify/` and any `graphify-out/` path.
- Removed the `graphify-personal` export into the vault.
- Migrated existing generated folders out of the vault to the host Trash for
  recoverability. Markdown remains the source of truth.
- Reduced the vault root to the official PARA/AGENTS OS directories, the two
  agent entrypoints and hidden configuration files.
- Relocated the AGENTS OS installation prompt, portable pack sources and ZIP
  to `30-resources/agents-os/`; the builder now stages outside the vault and
  leaves only the ZIP, avoiding a second Obsidian-visible copy of 194 files.
- Redirected Excalidraw assets to `30-resources/diagrams/excalidraw` and set
  Obsidian deletions to the host system Trash so root-level `.trash/` and
  `Excalidraw/` directories are not recreated by normal use.
- Removed domain-specific Echo Forge ledgers from always-loaded global
  continuity and demoted the VPN routing preference to contextual retrieval.

## Validación

- `graphify-obsidian cache-path` resolvió fuera del vault.
- `explain "AGENTS OS"` leyó el grafo local.
- No quedaron directorios `95-graphify/` ni `graphify-out/` dentro del vault.
- El paquete portable se regeneró desde su nueva ruta: 194 fuentes verificadas
  por SHA-256 y ZIP validado; no quedó el árbol desempaquetado en el vault.
- Los enlaces relativos de la guía migrada resolvieron correctamente; schema
  contract, lint dirigido y doctor estricto quedaron verdes.
- El refresh de Graphify respetó el gate y preservó el último índice válido:
  siguen pendientes 27 errores y 6 warnings heredados fuera de este cambio. El
  baseline no se relajó para ocultarlos.
- Los artefactos nuevos o ya migrados al schema vigente pasaron lint dirigido.
  El gate global mantiene deuda ajena a este cambio (27 errores y 6 warnings),
  reportada sin bloquear el auto-refresh local.

## Rollback

Los directorios y archivos retirados permanecen en una carpeta fechada de la
Papelera del host. Pueden recuperarse desde allí, aunque las fuentes Markdown y
el paquete portable ya no dependen de ellos.

## Ejecución local (vault `main`, esta máquina)

- Esta máquina completó la migración pendiente: rescate de los wheels del fork desde `95-graphify/dist/` hacia `~/.local/share/graphify-obsidian/dist/` (SHA-256 del wheel `0.9.6.post2` verificado contra BUILD.md), creación del venv aislado con `python3 -m venv` + `pip` (sin `uv`) e instalación de `graphifyy 0.9.6.post2`.
- El wrapper legacy `/usr/local/bin/graphify-obsidian` (cacheaba dentro del vault vía `XDG_CACHE_HOME=95-graphify/...`) fue reemplazado por el wrapper canónico, instalado también en `~/bin/graphify-obsidian` con `export PATH="$HOME/bin:$PATH"` en `.zshrc`; el binario compartido `/usr/local/bin/graphify` (`0.9.4`) no fue tocado.
- Enviado a carpeta fechada de la Papelera del host: `95-graphify/` (151 MB), `graphify-out/` (1.9 GB), un `graphify-out/` anidado en `10-projects/Echo Forge/` (1 MB), `.trash/` local de Obsidian (232 MB, 9964 entradas), `scratch/`, `specs/` y `sqx/` vacíos, `.DS_Store` de raíz y el wrapper legacy respaldado.
- Config local sincronizada: `.gitignore` creado, `.graphifyignore` ampliado (`.trash/`, `.DS_Store`, `Excalidraw/`, variantes `graphify-out-*` y exclusiones `30-resources/agents-os/chatgpt-pack/` y `30-resources/agents-os/distribution/` que exigía doctor), `.obsidian/app.json` con `"trashOption": "system"` y `userIgnoreFilters`, LiveSync `useIgnoreFiles: true`, y creado el destino canónico `30-resources/diagrams/excalidraw/` (el plugin Excalidraw no está instalado en esta máquina).
- Validación local: `cache-path` fuera del vault, `explain "AGENTS OS"` construyó el índice en modo tolerante y resolvió el nodo canónico, raíz reducida a la allowlist, doctor estricto `HIGH=0 / MEDIUM=0 / LOW=0`, cero directorios `95-graphify`/`graphify-out*` dentro del vault y lint dirigido del cambio `0/0`.
- Señal de drift: el gate global de este local reporta deuda heredada mayor que la registrada en la migración original (`136 ERROR / 31 WARN` vs `27/6`, baseline `0/0` intacto y sin relajar), consistente con un local atrasado respecto del remote de LiveSync; la deuda global y el rebaseline quedan fuera de este cambio.

## Ejecución local segunda (vault `main`, máquina Hermes, 2026-09-04 00:47–02:00 UTC)

- Ejecución solicitada explícitamente por el owner tras el cambio original. El
  estado local de esta máquina estaba **atrasado**: el venv aislado
  `~/.local/share/graphify-obsidian/venv` no existía (evidencia: ausente a las
  00:52), el wrapper activo en `~/.local/bin/graphify-obsidian` era la versión
  legacy que escribía en `95-graphify/obsidian/`, y los wheels seguían dentro
  del vault en `95-graphify/dist/` (150 MB). La sección anterior describe la
  ejecución en la otra máquina; esta completa el procedimiento aquí.
- Rescate: wheels `graphifyy 0.9.6.post2 / post1 / 0.9.6` copiados de
  `95-graphify/dist/` a `~/.local/share/graphify-obsidian/dist/`; SHA-256 del
  `post2` verificado (`fd36205f…dc4a8`, igual a BUILD.md).
- Instalación: venv con `python3.12 -m venv` + `pip install "graphifyy[all]"`
  desde el wheel local (sin `uv`, no disponible); `graphify 0.9.6.post2`
  verificado con `--version`. Nota: el extra `[all]` instala `hermes-agent`
  como dependencia dentro del venv aislado; no afecta al venv real del sistema.
- Wrapper: canónico del vault instalado en `~/bin/graphify-obsidian`
  (`~/bin` ya estaba en PATH; `.zshrc` no modificado); wrapper legacy
  `~/.local/bin/graphify-obsidian` enviado a la Papelera; creado
  `~/.config/agents-os/vault-root`.
- Rescate de contenido: los dos audits únicos `EF-G32-audit-1785705893*.md`
  movidos de `95-graphify/personal/symphony/audits/` a
  `10-projects/Echo Forge/audits/`; reconformados al contrato `doc`
  (`schema_version: 1`, tag `kind/doc`, secciones Propósito/Contenido); lint
  strict dirigido `0/0`.
- Papelera del host (`gio trash`, recuperables vía `~/.local/share/Trash/`):
  `95-graphify/`, `graphify-out/` y `10-projects/Echo Forge/graphify-out/`.
- Config local: `.graphifyignore` ampliado (`.obsidian/`,
  `chatgpt-pack/`, `distribution/` — exigidos por doctor); `.gitignore`
  creado; `.obsidian/app.json` con `{"trashOption": "system"}`; LiveSync
  `useIgnoreFiles: true` + `ignoreFiles: .gitignore` (166 claves preservadas);
  creado `30-resources/diagrams/excalidraw/` (destino canónico; el plugin
  Excalidraw no está instalado en esta máquina).
- Validación local: `cache-path` =
  `~/.cache/agents-os/graphify-obsidian/db7a61cfa657167c` (fuera del vault);
  `explain "AGENTS OS"` construyó el índice en modo tolerante y resolvió el
  nodo canónico (WARN de deuda heredada 136/33 → 136/31, sin bloquear); raíz
  exacta contra la allowlist; doctor estricto `HIGH=0 / MEDIUM=0 / LOW=0`
  (antes 3 MEDIUM); cero `95-graphify`/`graphify-out*` dentro del vault;
  lint strict dirigido de los 2 archivos modificados `0/0`.
