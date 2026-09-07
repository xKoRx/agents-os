---
type: change_log
schema_version: 1
scope: session
created: "2026-08-15"
updated: "2026-08-15"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
  - "[[echo-forge]]"
related:
  - "[[Echo Forge - Etapa 6]]"
  - "[[Echo Forge - Cierre de Etapa 4]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/echo
  - change/created
  - kind/change-log
  - project/echo-forge
  - scope/session
---

# Change Log - Proyecto MT5 Reconciliation and Scoring

## Cambio

- **Tipo:** created + updated.
- **Archivos:** `10-projects/Echo Forge/agentes/Echo Forge - Reconciliación y Scoring MT5.md` y `10-projects/Echo Forge/Echo Forge.md`.

## Motivo

Crear un planificador único y retomable para la ingesta del HTM de MT5, su normalización en MongoDB y la comparación explicable contra métricas SQX.

## Fuentes usadas

- [[Echo Forge]]
- [[Echo Forge - Etapa 6]]
- [[Echo Forge - Cierre de Etapa 4]]

## Resolución aplicada

- Se creó un proyecto `owner: agent` con parent [[Echo Forge]], checklist T0-T3, contratos de provenance, dos colecciones propuestas y scoring risk-first en `shadow`.
- Se agregó una única tarea puente humana al proyecto padre.
- Los thresholds quedaron pendientes de calibración y aprobación; no se fijaron cifras productivas por inferencia.

## Validación

- Contrato de schema y vínculo parent/bridge verificados mediante los validadores de AGENTS OS.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos, dumps ni paths absolutos persistidos.

## Rollback

- Eliminar la nota del proyecto y este change log, y retirar de [[Echo Forge]] la tarea puente y la entrada de bitácora agregadas el 2026-08-15.
