---
type: known_error
scope: tool
created: 2026-06-27
updated: 2026-09-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[graphify-contract]]"
  - "[[80-agents/skills/agents-os-graphify-maintenance/SKILL|agents-os-graphify-maintenance]]"
aliases:
  - graphify output path confusion
  - graphify live report path
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - area/personal
  - kind/known-error
  - priority/high
  - project/agents-os
  - project/agentsos
  - scope/tool
---
# Graphify output inside the vault was removed

> [!success] Superado 2026-09-03
> `graphify-obsidian` ahora usa caché local por máquina. Ningún output dentro
> del vault es válido; `graphify-obsidian cache-path` es la única resolución.

## Síntoma

- Aparece un directorio `graphify-out/` o `95-graphify/` dentro del vault.
- Obsidian consume CPU/indexa miles de archivos o LiveSync genera conflictos.
- El tamaño del vault crece por snapshots fechados, HTML, JSON y cache AST.

## Causa

- Se ejecutó el binario crudo `graphify` desde una ruta del vault, o se usó un
  wrapper legacy que publicaba reportes en el vault.
- Cada actualización podía conservar history por fecha y multiplicar el peso.

## Impacto

- Bloat local y remoto, sincronización lenta y conflictos entre máquinas.
- Ruido de búsqueda y posibilidad de consultar un índice derivado obsoleto.

## Detección

```bash
find "$AGENTS_OS_VAULT" -type d \
  \( -name graphify-out -o -name 'graphify-out-*' -o -name 95-graphify \) \
  -prune -print
graphify-obsidian status
```

El primer comando debe quedar vacío y `cache=` debe resolver fuera del vault.

## Mitigación

- Usar exclusivamente `graphify-obsidian` para el vault. Sus queries refrescan
  el índice local automáticamente.
- No copiar reports, HTML, graph JSON, manifests, histories, caches ni wheels al vault.
- Mantener las defensas en `.gitignore`, Obsidian `userIgnoreFilters` y LiveSync.
- Ante una salida accidental, mover el directorio exacto fuera del vault; el
  índice válido se resuelve con `graphify-obsidian cache-path`.

## Evidencia

- La migración 2026-09-03 retiró 521 MB de derivados del vault y dejó un cache
  local de 8.5 MB.
- El E2E del Context Router pasó 14/14 operaciones, sin misses y con precisión
  proxy de 100% usando el índice local.
