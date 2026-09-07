---
type: session
scope: session
created: 2026-07-20
updated: 2026-07-20
area: "[[Meli]]"
project: "[[Refactor Bajó de Precio VPP]]"
application: "[[vpp-backend]]"
entities:
  - "[[Refactor Bajó de Precio VPP]]"
  - "[[vpp-backend]]"
  - "[[vis-octopus-lib]]"
related:
  - "[[2026-07-20-refactor-bajo-precio-vpp-plan-raw]]"
aliases: []
confidence: high
source_session: "codex-vpp-price-drop-motors-refactor-planning-2026-07-20"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
  - area/meli
---

# Refactor Bajó de Precio VPP — planificación

## Objetivo

- Crear un proyecto ejecutable por IA pequeña para llevar el componente/lógica nueva a Octopus y minimizar VPP sin sacrificar seguridad cross-vertical.

## Contexto cargado

- Código y arquitectura de VPP/Octopus, historial de `PriceComponent`, implementación publicada 3.4.1 y reglas AGENTS OS.

## Trabajo realizado

- Se definió arquitectura objetivo, gate técnico, fallback, fases, matriz funcional, archivos prohibidos, criterios de aceptación y prompt maestro.
- Se creó [[Refactor Bajó de Precio VPP]] como proyecto de agente y su tarea puente en [[Bajó de Precio]].

## Artifacts creados o modificados

- Proyecto canónico, parent, change log, L0/L1, feedback e internal memory.

## Memoria propuesta o creada

- No se creó L3 pública: la decisión es específica del proyecto y queda en su entidad canónica; se actualizó continuidad interna.

## Decisiones

- Octopus concentra componente y lógica Motors; VPP conserva routing/layout/mapping.
- No migrar Price completo ni corregir `PriceComponent` general en este PR.
- Ejecutar spike obligatorio antes de confiar en ID interno + `baseMarshallerId=price`.

## Pendiente

- Ejecutar el proyecto con el prompt maestro y pasar la tarea puente a Review solo con todos los gates verdes.
