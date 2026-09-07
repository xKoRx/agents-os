---
type: learning
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-c3-zero-supply-closure]]"
aliases:
  - C3 physical-cert-as-discovery-loop
confidence: high
source_session: ECHO-FORGE-C3-END-TO-END-BLOCKER-BURNDOWN-AND-ZERO-SUPPLY-CLOSURE-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/project
  - project/echo-forge
---

# C3 ya no usa certificación física como loop de descubrimiento

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- La metodología C3 cambió: de `physical-cert-as-discovery-loop` (cert → blocker A → fix → release → cert → blocker B) a `static/deterministic blocker burn-down → cohesive implementation → one release → physical certification`.
- Un defecto físico conocido no es stop de un audit TOP de burn-down: hay que seguir aguas abajo con cohort=0 y cerrar el contrato completo antes de implementar.

## Aplicabilidad

- **Cuándo cargarlo:** cualquier recertificación C3, RCA de pipeline Echo Forge, o tentación de “arreglar el último error observado”.
- **Cuándo no cargarlo:** certificación física ya autorizada después de tests deterministas verdes del FIX CONTRACT.

## Entidades relacionadas

- [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] · [[2026-09-04-echo-forge-c3-zero-supply-closure]]

## Evidencia

- Fuente: [[2026-09-04-echo-forge-c3-zero-supply-burndown-summary]] — CERT 0.2.89 reretester cardinality, 0.2.90 build 6140 y 0.2.91 empty cohort son la misma clase de descubrimiento tardío.
