---
type: source
schema_version: 1
status: superseded
area: "[[Meli]]"
source_url:
repo: signals-knowledge
path: signals-knowledge
author: Carlos Montecinos (cmontecinos, Software Expert — Advertising)
published: 2026-07-30
captured: "2026-08-18"
license:
checksum:
supersedes:
superseded_by: "[[ads-signals-knowledge-library-repo]]"
aliases:
  - signals-knowledge repo
  - repo signals-knowledge
tags:
  - kind/source
  - area/meli
created: "2026-08-18"
updated: "2026-09-01"
---

# signals-knowledge-repo

## Referencia

- **Origen resoluble:** `repo: signals-knowledge` · `path: signals-knowledge`, relativo a [[Fuentes — Workspace de repositorios]] (`~/fuentes`). Aplicación Fury `signals-knowledge` (`.fury`). Invariante 12: el checkout completo vive en el workspace externo, no bajo `VAULT_ROOT`.
- **Fecha de captura:** 2026-08-18 (`index.md` del bundle declara `timestamp: 2026-07-30`).

## Alcance

- Bundle OKF (Open Knowledge Format) de conocimiento curado del equipo Signals: áreas `rio/`, `signals-catalog/`, `signals-collector/`, `signals-sdk-go/`, `signals-cli/`, `signals-migrator/`, `signals-frontend/`.
- Respalda la página canónica [[signals-knowledge]] en el dominio `30-resources/knowledges/`.

## Notas de provenance

- Contribución vía PR sobre archivos `.md` OKF (frontmatter YAML + links relativos).
- Hook de `pre-commit` sin `.pre-commit-config.yaml`: commitear con `PRE_COMMIT_ALLOW_NO_CONFIG=1`.
- Spec OKF: `https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md`.

## Lifecycle

- **Supersedes:** —
- **Superseded by:** [[ads-signals-knowledge-library-repo]] (2026-09-01)
