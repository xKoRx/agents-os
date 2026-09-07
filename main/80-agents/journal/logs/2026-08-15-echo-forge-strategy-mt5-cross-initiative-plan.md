---
type: change_log
schema_version: 1
scope: session
created: "2026-08-15"
updated: "2026-08-15"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[echo-forge]]"
related:
  - "[[2026-08-15-mt5-html-parser-fail-open-signed-costs]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-15-echo-forge-strategy-mt5-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/echo
  - change/updated
  - kind/change-log
  - project/echo-forge
  - scope/session
---

# Change Log - Plan cruzado Strategy y MT5

## Cambio

- **Tipo:** updated + created.
- **Archivos:** `10-projects/Echo Forge/agentes/Echo Forge - Reconciliación y Scoring MT5.md`, `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`, `10-projects/Echo Forge/Echo Forge.md` y `80-agents/memory/public/known-error/symphony/2026-08-15-mt5-html-parser-fail-open-signed-costs.md`.

## Motivo

- Hacer ejecutable el proyecto MT5 por agentes de distinto tamaño y convertir la dependencia con el nuevo modelo de Strategy en un contrato bidireccional verificable.

## Fuentes usadas

- `repo:symphony/mt5-export.htm`.
- `repo:symphony/sqx/adapters/mt5/parser.go`, `sqx/core/domain/mt5.go`, `sqx/core/domain/mt5_artifacts.go` y workflow MT5 vigente.
- SPECs `FEAT-SQX-MT5-BACKTEST-COMPILE`, `FEAT-SQX-METRICS-CONTRACT`, `FEAT-SQX-DEVIATION-FILTER` y `FEAT-SQX-STRATEGY-EVALUATION`.
- [[Echo Forge - Reconciliación y Scoring MT5]] y [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]].

## Resolución aplicada

- Se definió F0-F9 con tiers Grande/Mediano/Pequeño, roles SDD, precondiciones, pasos, outputs y gates.
- F0.1/T0.4 producen el mismo `Strategy-MT5 Binding v1`; persistencia espera G0+T1A y arquitectura T2 espera waves shadow.
- Se verificó el HTM UTF-16LE all-loss y se registraron los conflictos de costos firmados, fail-open, missing numérico, parsing estructural y pérdida de `ArtifactRef`.
- Se creó un known error reusable; no se modificó código ni artefactos SDD del repositorio.
- La tarea puente humana avanzó a WIP; el agente nunca la marcó Done.

## Validación

- Lint AGENTS OS estricto sin errores ni warnings para ambos proyectos y el known error.
- Evidencia del HTM verificada mediante tipo, encoding, tamaño, checksum, Settings, Results, Orders, Deals y footer.
- Handoff cruzado y gate `Strategy-MT5 Binding v1` presentes en ambos proyectos.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos, dumps ni paths absolutos persistidos.

## Rollback

- Revertir las secciones F0-F9/handshake de ambos proyectos y retirar el known error si el owner descarta la iniciativa; no hay cambios en Symphony que revertir.
