---
type: change_log
scope: session
created: "2026-07-02"
updated: "2026-07-02"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[graphify]]"
related:
  - "[[30-resources/tools/graphify]]"
  - "[[10-projects/Aranea]]"
aliases:
  - "graphify-obsidian install vm hermes"
  - "graphifyy 0.9.4"
  - "venv dedicado graphify"
confidence: verified
source_session: "2026-07-02 telegram ariadna"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-07-02 — Instalación operativa de `graphify-obsidian` en VM Hermes

## Cambio

- **Tipo:** created (instalación + wrapper) + updated (nota canónica)
- **Archivos:**
  - **Creados**:
    - `~/.local/share/graphify-venv/` (venv dedicado, PEP 668 avoided)
    - `~/.local/bin/graphify-obsidian` (wrapper bash, 5229 bytes, ejecutable)
    - `~/.local/bin/graphify` (symlink a `graphify-obsidian`)
    - `80-agents/journal/logs/2026-07-02-graphify-install-in-vm-hermes.md` (este log)
  - **Actualizados**:
    - `~/.local/share/graphify-venv/bin/graphify` (instalado por pip, ~250 KB)
    - `30-resources/tools/graphify.md` (estado: ✅ INSTALADO; tabla de comandos; instalación histórica)
  - **Sin cambios**:
    - `~/bin/graphify-aranea` (wrapper legacy ya estaba bien: delega a `graphify` o `graphify-obsidian`; ahora encuentra ambos en PATH y funciona tal cual).

## Motivo

- Owner pidió instalar graphify para retrieval del vault: *"quiero que instales graphify en la máquina para que la puedas usar con el usuario hermes. la idea es que puedas buscar por ahí los documentos del vault"*.
- Owner pidió wrapper de fácil uso: *"luego el uso debe ser de fácil uso ojo.. ideal que puedas crear un wrapper para llamarlo por graphify-obsidian, así está me parece en las reglas"*.
- La nota canónica `30-resources/tools/graphify.md` advertía: *"No la voy a correr sin OK del owner porque modifica el sistema y descarga dependencias remotas"*. Owner OK explícito en esta sesión.

## Fuentes usadas

- [[30-resources/tools/graphify]] — nota canónica con 3 opciones de instalación y contexto de comandos esperados.
- PyPI metadata de `graphifyy` 0.9.4 (MIT, Safi Shamsi, requires-python >=3.10).
- Wheel METADATA (leído en /tmp; entry_points: `graphify` + `graphify-mcp`).

## Resolución aplicada

1. **Decisión de packaging**: NO usar `uv tool install` (no había `uv` instalado y descarga otro toolchain). NO usar `pip install --break-system-packages` en el venv de Hermes (lo contamina). Opté por **venv dedicado** en `~/.local/share/graphify-venv/` + symlink/wrapper en `~/.local/bin/`. Patrón replicable.
2. **Creación del venv**: `python3 -m venv ~/.local/share/graphify-venv` (PEP 668 avoided).
3. **Upgrade pip**: `~/.local/share/graphify-venv/bin/pip install --upgrade pip` (24.0 → 26.1.2).
4. **Instalación del paquete**: `~/.local/share/graphify-venv/bin/pip install graphifyy` → graphifyy 0.9.4 + numpy 2.4.6 (16.9 MB) + networkx 3.6.1 (2.1 MB) + rapidfuzz 3.14.5 (3.2 MB) + tree-sitter 0.25.2 + 29 lenguajes.
5. **Wrapper canónico `~/.local/bin/graphify-obsidian`** (~5 KB):
   - Apunta a `~/.local/share/graphify-venv/bin/graphify`.
   - Fijar `VAULT = ${OBSIDIAN_VAULT:-$HOME/obsidian/SecondBrain/main}` (overridable por env).
   - Fijar `GRAPH_DIR = $VAULT/95-graphify/obsidian`.
   - Comandos de vault (`update|cluster-only|watch`): default-ean a VAULT; `update` fuerza `--out-dir $GRAPH_DIR`.
   - Comandos de lectura (`query|explain|path|affected|diagnose`): fuerzan `--graph $GRAPH_DIR/graph.json`; falla limpio con exit 2 + mensaje si falta argumento.
   - Comandos de plataforma (`install|uninstall|hermes install|claude install|...`): delegan tal cual al upstream.
   - Stderr muestra VAULT y GRAPH_DIR antes de cada comando (trazabilidad para el operador).
   - Pasa `--help` al upstream.
6. **Symlink `~/.local/bin/graphify` → `graphify-obsidian`**.
7. **`chmod +x` sobre el wrapper**. PATH ya incluye `~/.local/bin`, así que ambos comandos están disponibles inmediatamente.

## Validación

- ✅ `graphify-obsidian --help` → muestra help del wrapper propio, menciona `graphify-obsidian --help` para help upstream.
- ✅ `graphify-obsidian explain "Aranea"` → exit 0; nodo `10-projects/Aranea/README.md L23`, community 26, 6 connections EXTRACTED.
- ✅ `graphify-obsidian query "BACKUP-DR-OWNER-PROJECT agent-project-02 PBS" --budget 300` → exit 0; 21 nodos encontrados en BFS depth=2.
- ✅ `graphify-obsidian path "Aranea" "ticket-018"` → exit 0; warning de ambigüedad + "No path found" (limpio, sin crash).
- ✅ `graphify-obsidian explain` sin argumento → exit 2 + mensaje accionable ("'explain' requiere un argumento. Ej: ...").
- ✅ `graphify-aranea explain "Aranea"` → exit 0; delega correctamente al wrapper nuevo (mensajes `[graphify-obsidian] VAULT=...` visibles).
- ✅ Grafo vivo del vault accesible: `95-graphify/obsidian/graph.json` (3.0 MB, last mod 2026-07-02 05:25 UTC, contiene ya la migración 10-projects/Aranea/ de esta mañana).

## Consecuencias / Follow-ups

- **Operativo inmediato**: el agente (Arianna en este perfil) puede usar `graphify-obsidian query|explain|path|affected` para retrieval barato del vault sin abrir carpetas.
- **Memoria inyectable**: considerar subir a memoria always-load los patrones canónicos de query (`<entidad> + <tipo> + <tema>`) y el comando base. Decisión para próxima sesión.
- **Skill operativa nueva**: considerar crear `graphify-vault-query` como skill que envuelva los patrones canónicos de query con budget + retry ante templates/noise (problema conocido documentado en `80-agents/memory/internal/`).
- **No reindexar manualmente todavía**: el grafo está al día vía LiveSync del Mac del owner. Si pasan >24 h sin sync, `graphify-obsidian update <VAULT> --out-dir <GRAPH_DIR>` toma ~5-10 min y regenera el grafo desde cero.
- **`graphify-personal` queda como stub legacy** — si el owner quiere que el agente pueda grafar `symphony/echo/sdk` desde esta VM, hay que implementar el wrapper (3 archivos, ~30 min).
