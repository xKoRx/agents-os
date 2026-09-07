---
type: change_log
scope: project
created: 2026-07-01
updated: 2026-07-01
area: "[[Meli]]"
project: "[[Automatización despliegue FURY]]"
entities:
  - "[[AGENTS OS]]"
  - "[[search-middleware]]"
  - "[[java-polycard-sdk]]"
  - "[[vis-octopus-lib]]"
  - "[[vpp-backend]]"
related:
  - "[[80-agents/skills/fury-lib-consumer-deploy/SKILL.md]]"
confidence: verified
tags:
  - area/meli
  - kind/log
  - project/automatizacion-despliegue-fury
  - tech/agents-os
  - tech/fury
---

# 2026-07-01 fury-lib-consumer-deploy skill created

## Cambios

- Creada skill `80-agents/skills/fury-lib-consumer-deploy/SKILL.md`.
- Creada metadata `80-agents/skills/fury-lib-consumer-deploy/agents/openai.yaml`.
- Actualizado `80-agents/skills/INDEX.md`.
- Actualizado proyecto `10-projects/Automatización despliegue FURY.md`.
- Corregido flujo para librerias Java: la version test debe escribirse en `build.gradle`, validarse, commitearse y pushearse antes de ejecutar `fury create-version`.
- Reforzada regla de versionado para ramas test: siempre `X.Y.Z-branch-slug`; prohibido usar semver productiva limpia, `rc`, `hotfix` o `release`.
- Agregada regla de evolucion continua: despues de cada uso real, si hubo aprendizaje operativo, actualizar la skill; memoria queda solo como contexto, no como sustituto del procedimiento.

## Verificaciones

- `fury --help` confirmó comandos generales `list-infra`, `list-versions`, `create-version` y `stage`.
- `fury create-version --help` confirmó `--confirmed` y `--watch`.
- `fury stage --help` confirmó deploy a test con `--scope` y `--confirmed`.
- `fury deployments list/details/create --help` confirmó monitoreo con `details --watch` y despliegue manual con `deployments create`.
- `fury stage --help`, `fury deployments create --help`, `fury deployments details --help` y `fury deployments list --help` fueron revalidados fuera del sandbox porque Fury escribe logs en `~/.fury`.
- `fury list-infra` en `~/fuentes/search-middleware` confirmó scopes de test para `fury_search-middleware`, incluyendo `furytestvis1`.
- `fury list-infra` en `~/fuentes/vis-vpp-backend` confirmó scopes `testvis-0`, `testvis-1`, `testvis-2`, `stage` y `prod`; la skill exige escoger un scope con `Environment Test`.

## Notas

- `search-middleware` importa Polycard SDK mediante `polycardVersion` en `build.gradle`.
- En el checkout actual de `vis-vpp-backend` no se encontró un import textual claro de `vis-octopus-lib`; la skill obliga a detectar el punto real o pedir confirmación antes de editar.
- El camino normal documentado es Fury CLI; Fury MCP queda como fallback para cuando el flujo CLI documentado falle o no alcance.
- El validador oficial de `skill-creator` no corrió porque el Python disponible no tiene PyYAML; se validó el frontmatter y `agents/openai.yaml` con Ruby `YAML`.
