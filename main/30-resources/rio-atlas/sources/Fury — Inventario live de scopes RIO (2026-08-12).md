---
type: source
schema_version: 1
status: active
area: "[[Meli]]"
source_url:
repo: fury-cli
path: list-infra + scopes status --json + services bigq consumers list + apps details + collab projects
author: Mercado Libre Fury Platform
published: 2026-08-12
captured: "2026-08-12"
license:
checksum:
supersedes:
superseded_by:
aliases:
  - fury-scope-inventory-2026-08-12
  - Fury live scopes RIO 2026-08-12
tags:
  - kind/source
  - tech/rio
  - project/scopes-rio
created: "2026-08-12"
updated: "2026-08-12"
---

# Fury — Inventario live de scopes RIO (2026-08-12)

> [!warning] Snapshot parcial supersedido
> Esta captura documenta la extracción CLI inicial. La autoridad vigente es `~/fuentes/rio-inspector/rio-scopes.json`, obtenida del service graph completo y representada en [[scope-inventory]]; el corte vigente es 88 runtimes y 40 consumers.

## Referencia

- **Origen resoluble:** CLI autenticada `fury list-infra`, `fury scopes status -j`, `fury services bigq consumers list`, `fury apps details` y `fury collab projects list --project dps-rio`, ejecutadas desde los checkouts backend RIO identificados por su `.fury`.
- **Fecha de captura:** 2026-08-12.

## Alcance

- Estado desplegado de `rio-playmaker`, siete control planes, `rio-materializer` y `rio-sdk-events`: nombre de scope, versión/tipo/ambiente cuando `list-infra` los expone, y salud/criticidad cuando `scopes status` los expone.
- Ownership técnico: los 10 repos pertenecen al Fury project `dps-rio`, cuyo team es `cross-dps-rio` y cuya iniciativa es `advertising`.
- Estado de consumidores BigQueue por scope: 39 consumidores, 38 `running` y 1 `paused`, distribuidos en 22 scopes. Esta fuente prueba registro y estado operacional actual del consumidor, no el timestamp del último mensaje, tráfico HTTP, necesidad vigente ni owner humano.

## Notas de provenance

- No se persiste el dump crudo de la CLI; la tabla normalizada vive en [[scope-inventory]] y puede regenerarse ejecutando las superficies indicadas por repo. Las superficies no son equivalentes: `scopes status` reveló 21 runtimes administrados que `list-infra` omitió, mientras BigQueue reveló consumidores `running` sobre scopes que Fury podía mostrar `Desired`.
- Los nombres de checkout se resuelven desde [[Fuentes — Workspace de repositorios]]; no se guardan paths absolutos.

## Lifecycle

- **Supersedes:** —
- **Superseded by:** —
