---
type: change_log
scope: session
created: 2026-08-06
updated: 2026-08-06
area: "[[Echo]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Cierre de Etapa 4]]"
related:
  - "[[2026-08-06-echo-forge-stage-4-audit-reconciled]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/echo
  - project/echo-forge
---

# Echo Forge — corrección de alcance por owner

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/Echo Forge.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Cierre de Etapa 4.md`
- **Antes:** la revisión estática clasificaba EF-G29 como corrupción bloqueante y volvía EF-G31 una precondición.
- **Después:** EF-G29 se marca deprecado a propósito y EF-G31 vuelve a quedar diferido para este ciclo.

## Motivo

- Decisión explícita del owner: el uso de `XAUUSD_darwinex` en los `.cfx` es configuración intencional de fixtures de prueba controlados por el JSON; no es un bug de producto ni requiere reparación.

## Fuentes usadas

- Instrucción explícita del owner en la sesión del 2026-08-06.
- [[2026-08-06-echo-forge-stage-4-audit-reconciled]].

## Resolución aplicada

- Se retira EF-G29 del camino bloqueante y se prohíbe abrir trabajo de patch, validación de identidad o cuarentena por esa condición de fixture.
- El camino de cierre queda en EF-G30 → EF-G32 → smoke E2E → decisión de cuarentena/Review con evidencia de TradeList.

## Validación

- Checklist, estado actual, roadmap, bitácora y tarea puente del proyecto hijo están alineados.
- El proyecto padre apunta al mismo camino vigente.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, credenciales, paths locales ni memoria interna.

## Rollback

- Revertir esta corrección sólo si el owner redefine explícitamente el alcance de los fixtures o de la validación de identidad.
