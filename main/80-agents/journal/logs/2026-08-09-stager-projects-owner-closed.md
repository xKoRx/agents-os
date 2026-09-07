---
type: change_log
created: 2026-08-09
project: "[[Echo Forge]]"
entities:
  - "[[Stager]]"
  - "[[Stager - Symphony Publisher Integration]]"
tags:
  - kind/change-log
  - area/echo
  - tech/deployment
---

# Cierre por owner — Stager y Symphony Publisher Integration

El owner confirmó que Symphony ya opera en Windows y cerró ambos proyectos.

- El core Stager queda entregado: descarga, verificación, staging versionado y
  marcadores `CURRENT`/`PENDING` para Linux y Windows.
- La integración con el publisher Symphony queda entregada y el cutover Linux
  documentado permanece como evidencia operacional.
- Quiesce/drain, Task Scheduler y launcher/SCM Windows no forman parte del
  core Stager ni de esta integración; sólo se abrirán como un proyecto nuevo
  bajo autorización explícita.
