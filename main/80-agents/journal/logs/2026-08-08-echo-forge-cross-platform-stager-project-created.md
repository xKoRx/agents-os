---
type: change_log
scope: project
created: 2026-08-08
updated: 2026-08-08
area: "[[Echo]]"
project: "[[Echo Forge - Cross-Platform Stager]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Cross-Platform Stager]]"
  - "[[Echo Forge]]"
related:
  - "[[echo-forge]]"
aliases: []
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/project
  - project/echo-forge
  - area/echo
  - change/created
---

# Change log — Echo Forge Cross-Platform Stager project created

## Qué cambió

- Creado [[Echo Forge - Cross-Platform Stager]] como proyecto `owner: agent`, hijo de [[Echo Forge]], desde el template vigente.
- Agregada una única tarea puente en el padre y movida a Review al quedar el diseño completo.
- La nota canónica documenta discovery, evidencia, alternativas, arquitectura recomendada, state machine, manifest v2, lifecycles Linux/Windows, seguridad, testing, riesgos, acceptance criteria y roadmap F0-F6.

## Validación

- No se modificó código de producción.
- Builds focales `linux-amd64` de `sqx-worker` y `windows-amd64` de `sqx-mt5-worker`: PASS.
- Core/adapters/watcher del publisher: PASS; el único fallo del suite amplio fue un example test acoplado a ETCD real y quedó planificado en F0.
- Credenciales con apariencia real se registraron sólo como riesgo P0, sin copiar valores al vault.

## Rollback

Retirar la nota de proyecto, su tarea puente y este change log si el owner rechaza la creación completa. No hay runtime, release ni datos externos que revertir.
