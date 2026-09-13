---
type: change_log
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Echo]]"
project: "[[Echo — Producto Integrado]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
related:
  - "[[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
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
---

# 2026-09-13-echo-forge-f05i-planning-frozen

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo Forge — F-05-I Cohesive release and read surfaces.md` (creada vía materialize contract)
  - `30-resources/applications/echo/Echo Forge — F-05-I Release Matrix and Read Surface Contract.md` (creada vía materialize contract)
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md` (links, board, roadmap F-05, bitácora)

## Qué cambió

- TOP F-05-I convirtió el roadmap block F-05-I en paquete de implementación inequívoco para NORMAL: SPEC técnica frozen (scope, release matrix `sqx-release-matrix.v1`, read surface CLI JSON, funnel `sqx-forge-funnel-projection.v1`, error/empty semantics, provenance por refs exactos, BWC, `DATABASE MIGRATION: NONE`, fixtures sintéticas, handoff F-05-C) y proyecto con tareas atómicas F05I-T1…T7, allowed files exactos, matriz de tests congelada y stop conditions.
- Recon source read-only @ `xKoRx/symphony@b57bfb2` (sin tocar product code): read models V2 existentes sin callers productivos (`forge.Service`, `LoadForgeCampaignResult`), cero HTTP/API/GraphQL, tools informales `sqx/tools`, authorities PG/Mongo/MinIO/Temporal mapeadas. Decisión de arquitectura: CLI JSON determinística sobre ports narrow; sin HTTP; sin `internal/di` changes; release matrix declarativa en `deploy/release-matrix.json` + validador, no segunda autoridad de release.
- Factory V2 enlaza proyecto y SPEC de F-05-I; F-05-C sigue diferido (CERT-F05-01…03); Deferred Certification Backlog no requirió cambios (sin dependencias nuevas descubiertas).

## Validación

- Materialización canónica de las dos notas vía `materialize_schema_note.py` (contract gate PASS).
- Ningún product code tocado; sin writes en repos; baseline `b57bfb2` verificado existente (HEAD de `origin/feature/f04-magic-version-handoff`).

## Compatibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales de máquina, memoria interna ni secretos

## Rollback

- Eliminar las dos notas creadas y revertir el delta de Factory V2; no hay otra superficie afectada.
