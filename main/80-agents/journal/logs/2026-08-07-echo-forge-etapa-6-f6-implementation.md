---
type: change_log
scope: session
created: 2026-08-07
updated: 2026-08-07
area: "[[Echo]]"
project: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Etapa 6]]"
  - "[[echo-forge]]"
related: []
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
share_scope: local
tags:
  - kind/change-log
  - scope/session
  - area/echo
  - project/echo-forge
  - change/updated
---

# Change Log — Implementación de F6 en Echo Forge Etapa 6

## Cambio

- Se implementó F6 en el repo `symphony`, commit `e3aee85`: el task type
  `mt5_compiler` quedó integrado en Generic y Group mediante un agregador
  compartido que lista `.mq5` desde `source_folder`, ordena full keys, despacha
  un child por artefacto y conserva sólo los `.ex5` exitosos.
- El parent y sus children permanecen en la queue principal; únicamente
  `mt5_compile_artifact` usa `sqx-mt5-queue`. Los fallos funcionales y los
  errores de infraestructura agotados se contabilizan sin abortar el lote.
- Se agregó el test de integración permitido por el PLAN para ambos
  intérpretes: cero/una/múltiples keys, orden determinista, fallo parcial,
  retries agotados, routing, preservación de `Origin`, rerun y task desconocido.

## Verificación

- Suite focalizada y suite completa de `workflows`: PASS.
- Detector de carreras focalizado, `go vet ./workflows`, build de `sqx-worker`
  y `git diff --check`: PASS.
- `deployer_screen.log` se mantuvo fuera del commit por ser un cambio ajeno.

## Estado durable

- [[Echo Forge - Etapa 6]] avanzó de 50% a 58%; F6 quedó `[x]` y F7 es el
  próximo paso.
- La tarea puente de [[Echo Forge]] permanece en WIP porque F7–F11 siguen
  abiertos; sólo el owner puede aceptar el proyecto completo.
