---
type: decision
scope: project
created: "2026-06-30"
updated: "2026-06-30"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[Aranea]]"
  - "[[AGENTS OS]]"
related:
  - "[[70-templates/project]]"
  - "[[30-resources/aranea/00-index]]"
aliases: []
confidence: high
source_session: "[[2026-06-30-1636-aranea-docs-storage-batch-summary]]"
load_policy: never
indexable: true
index_priority: medium
tags:
  - kind/decision
  - kind/adr
  - scope/agent
  - area/personal
  - project/agents-os
---

# Decision: Ubicación de docs del homelab Aranea

> [!info]+ Decision ADR
> **Tipo:** decisión arquitectónica · **Estado:** accepted · **Fecha:** 2026-06-30

## Contexto

El owner pidió el 2026-06-30 cerrar las dos tareas de documentación en la frase literal:

> "puede quedar mientras la documentación en resources dentro de una carpeta llamada aranea"

Esa instrucción **contradice** el patrón canónico de AGENTS OS, que sugiere `10-projects/{Aranea Cluster}/` para entidades-proyecto nuevas.

## Decisión

La documentación oficial canónica del homelab Aranea vive en `30-resources/aranea/` (relativo a `VAULT_ROOT`), no en `10-projects/`.

## Fundamento

- **Owner explícito**: la instrucción literal del owner tiene precedencia sobre el patrón canónico de AGENTS OS cuando difieren.
- **Aranea es una aplicación/sistema**, no un proyecto con ciclo de vida finito. `30-resources/` es la carpeta correcta para "aplicaciones, herramientas y recursos" según `80-agents/agents-os/agents-os.md` línea 181-189.
- **`10-projects/` se reserva** para proyectos con inicio/fin definidos (Meli, Echo Forge, Refactor Polycard, etc.). Aranea es una plataforma viva.

## Consecuencias

- El proyecto en sentido AGENTS OS (con tareas, sprints, etc.) para Aranea podría existir en `10-projects/Aranea-Cluster-Documentation/` en el futuro, pero NO se crea ahora porque el owner no lo pidió.
- El `00-index.md` en `30-resources/aranea/` cumple el rol de entry point visual.
- Los tickets de cambio operativo siguen en `~/aranea/tickets/` (convención externa al vault), no en el vault. Consistente con el flujo del owner.

## Estado

accepted. Sin revertir mientras el owner lo ratifique.
