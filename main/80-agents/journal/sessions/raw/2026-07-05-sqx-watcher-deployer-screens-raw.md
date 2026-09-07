---
type: raw_session
scope: session
created: 2026-07-05
updated: 2026-07-05
area:
project:
application: symphony
entities: []
related: []
aliases: []
confidence: verified
source_session: 92d24819-894f-4754-bd61-88c79d82aa69
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

# Activación de Watcher y Deployer en screens - 2026-07-05

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Antigravity
- Proyecto o entidad: Symphony
- Objetivo de la sesión: Levantar el watcher y el deployer de SQX en sesiones de screen en background.

## Transcript

```
Pegar aquí la sesión completa.
```

## Evidencia externa

- Procesos en ejecución:
  - `SCREEN -dmS watcher ./run_watcher.sh ./input` (go run sqx/cmd/sqx-watcher/main.go ./input)
  - `SCREEN -dmS deployer ./run_deployer.sh ./deploy deploy` (go run deployer/cmd/deployer-watcher/main.go -watch-root ./deploy -bucket deploy)
