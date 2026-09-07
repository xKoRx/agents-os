---
type: storage
schema_version: 1
status: active
slug: "echo-go-workspace"
aliases:
  - workspace Go Echo
  - "~/go/src/github.com/xKoRx"
  - repos Echo Forge Go
tags:
  - kind/storage
  - storage/echo-go-workspace
created: "2026-08-16"
updated: "2026-08-16"
---

# Echo — Workspace Go de repositorios

## Propósito

- Workspace externo para checkouts completos de los repositorios del ecosistema Echo Forge (hogar personal, no Meli).

## Ubicación y contrato

- **Path:** `~/go/src/github.com/xKoRx`
- **Qué contiene:** repositorios completos del ecosistema Echo: `symphony`, `sdk`, `stager`, `echo`, `mde`, `api-core`, `api-persist`.
- **Qué no contiene:** notas del vault, memoria de agentes ni repositorios completos bajo `VAULT_ROOT`. Los repos Meli/RIO viven en [[Fuentes — Workspace de repositorios]] (`~/fuentes`), no aquí.
- **Reglas de uso:** los checkouts conservan los nombres canónicos del remote (`symphony`, `sdk`, etc.; organización `xKoRx`); no se aplican alias `rio-*` ni renombres locales. Antes de clonar, resolver esta nota por su título canónico.

## Operación

- **Comandos seguros:** `go build`/`go test` desde la raíz de cada repo; verificar rama/commit contra el frontmatter `repo:` del proyecto antes de trabajar.
- **Backups / recuperación:** los repos son Git; no borrar worktrees sin confirmar destino y recuperación.
- **Fuentes relacionadas:** [[Echo Forge]], [[Echo]], [[Fuentes — Workspace de repositorios]]
