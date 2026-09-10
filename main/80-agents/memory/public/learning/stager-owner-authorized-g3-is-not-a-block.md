---
type: learning
schema_version: 1
scope: project
created: "2026-08-13"
updated: "2026-08-13"
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[Stager - Cross-Platform Deployment Lifecycle]]"
related:
  - "[[Echo Forge]]"
aliases:
  - no inventar BLOQ F3 G3
  - owner authorized cutover
confidence: verified
source_session: a896f77f-7e50-4c60-b186-a027e8f81792
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/project
  - area/echo
  - app/stager
  - project/stager-cross-platform-deployment-lifecycle
---

# stager-owner-authorized-g3-is-not-a-block

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- Con F3.3–F3.10 / G3 autorizados, un fallo de cutover (CRLF, sudo, dual poller, fake vs worker real, MetaEditor exit 1) se repara y se reintenta; no se declara BLOQ ni se pregunta al owner por permisos ya dados.
- Las únicas puertas reales: no publicar MinIO/manifest de flota; no kill/cancel por timeout; F3.9 sólo con soak + inventario cero; puente Echo Forge máximo `[r]`, nunca Done; no persistir secretos.

## Aplicabilidad

- **Cuándo cargarlo:** al retomar [[Stager - Cross-Platform Deployment Lifecycle]] en F3/G3.
- **Cuándo no cargarlo:** fases F0–F2 ya cerradas, o trabajo fuera de cutover productivo.

## Entidades relacionadas

- [[Stager - Cross-Platform Deployment Lifecycle]]
- [[stager-app]]

## Evidencia

%% Cita de fuente, NO prosa narrativa: link a sesión/log/archivo + una línea de qué la respalda. No re-parafrasear el aprendizaje ya destilado arriba (constitución: memorias compactas). %%

- Fuente: [[2026-08-13-stager-f3-g3-fake-block-session-feedback]] — el owner cerró la sesión furioso porque el agente trató reparaciones como bloqueos.
