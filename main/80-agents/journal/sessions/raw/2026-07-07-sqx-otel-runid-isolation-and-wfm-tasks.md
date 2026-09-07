---
type: raw_session
scope: session
created: 2026-07-07
updated: 2026-07-07
area: "[[Symphony]]"
project: "[[Echo Forge]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
  - "[[Echo Forge]]"
related: []
aliases: []
confidence: verified
source_session: "241add91-8048-41f7-b2cd-87470b589ef0"
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

# Sesión: Aislamiento por Trace ID en DB y Tareas WFM (Symphony)

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Antigravity
- Proyecto o entidad: [[Echo Forge]]
- Objetivo de la sesión: Revertir mutación de Wave a nivel de workflow (usar static wave_1 en MinIO), implementar aislamiento E2E asociando los registros en MongoDB/Postgres al Trace ID de OpenTelemetry (OTel). Filtrar subidas del optimizador a MinIO a solo archivos que comiencen por WF_Matrix. Agregar tareas de evaluación WFM y clasificación a config.json. Soportar clasificación y ranking basado en métricas de los runs robustos seleccionados post-subflujo en classify_and_rank.

## Transcript

```
[El usuario cargará la transcripción de la sesión aquí]
```

## Evidencia externa

- Walkthrough: [[walkthrough.md]]
