---
type: feedback
schema_version: 1
scope: session
created: 2026-09-04
updated: 2026-09-04
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-04-zcode-glm-5.3-flash-echo-forge-mt5-6140-allowlist-fix]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: builtin:zai-coding-plan/GLM-5.3-Flash
agent_run: "[[2026-09-04-zcode-glm-5.3-flash-echo-forge-mt5-6140-allowlist-fix]]"
session_goal: implementar allow-list {6090,6140} + fixture físico 6140
source_session: ECHO-FORGE-MT5-REPORT-CERTIFIED-BUILD-ALLOWLIST-6140-FIX-NORMAL
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/echo-forge
  - agent/system1
---

# Session Feedback - 2026-09-04 - echo-forge-mt5-6140-allowlist-fix

## Context

- Agent surface: [[ZCode]]
- Agent model: builtin:zai-coding-plan/GLM-5.3-Flash
- Agent run: [[2026-09-04-zcode-glm-5.3-flash-echo-forge-mt5-6140-allowlist-fix]]
- Session goal: certificar build 6140 en `mt5-report.v1` (allow-list explícita) sin release ni deploy
- Main entity: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]
- Skills used: agents-os-bootstrap, agents-os-agent-run-register
- Retrieval mode: búsqueda enfocada (grep) sobre memoria interna/known-errors + repo; Graphify no usado (stale por sesiones previas)

## Fricción detectada

- **Acceso MinIO degradado:** `mc` no está instalado en esta máquina y los aliases `f5`/`local` de `~/.mc/config.json` devuelven 403 contra el endpoint real (`192.168.31.92:9000`). La vía que funcionó: claves `minio/endpoint|access_key|secret_key` de etcd documentadas en `sdk/pkg/shared/minio/example_test.go` + cliente S3 SigV4 en stdlib. Sugerencia: runbook corto de "descarga de artifact durable" o instalar `mc` y refrescar aliases.
- **Deuda gitignore `mt5-export.htm` (FIX-AL-75):** `repoRoot()` del package `report` exige el archivo en la raíz, pero está gitignoreado; toda sesión que corra el corpus debe restaurarlo manualmente desde `git show b5c71d5:mt5-export.htm` (SHA `090ca4d1…`). Es higiene separada por diseño de la misión, pero la fricción se repite en cada sesión de parser.
- **`crew/INDEX.md` desactualizado:** la línea de superficies registradas no incluye [[ZCode]] aunque la nota canónica existe desde 2026-08-14.
- **Graphify stale:** no se reparó por instrucción de la misión; la búsqueda enfocada bastó, pero el costo de arranque crece sin índice.

## Aprendizaje

- El patrón crear→correr→borrar para tests dirigidos fuera de budget (probe `Normalize` 6140) demostró la semántica sin violar el file budget; el checkpoint deja constancia de que la evidencia no es un test permanente.

## Sugerencia

- Incorporar la restauración de `mt5-export.htm` (o mover el corpus a paths versionados) a la sesión de higiene pendiente; registrar ZCode en `crew/INDEX.md` en el próximo cambio de Sistema 1.
