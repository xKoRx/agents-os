---
type: change_log
scope: application
created: 2026-08-08
updated: 2026-08-08
area: "[[Echo]]"
project: "[[Stager - Symphony Publisher Integration]]"
application: "[[stager-app]]"
entities:
  - "[[stager-app]]"
  - "[[Stager]]"
  - "[[Stager - Symphony Publisher Integration]]"
  - "[[2026-08-08-stager-deployment-system]]"
  - "[[Echo Forge]]"
  - "[[echo-forge]]"
related:
  - "[[2026-08-08-stager-mvp-boundary-and-activation]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: normal
tags:
  - kind/changelog
  - scope/application
  - area/echo
  - project/stager-symphony-publisher-integration
  - app/stager-app
---

# Stager system documentation and Symphony publisher handoff

## Cambio

- [[stager-app]] pasó de registro compacto a documentación canónica del sistema: arquitectura, estado real vs pendiente, manifest, configuración, failure semantics, repo map, roadmap y handoff para agentes.
- El repo Stager agregó `docs/ARCHITECTURE.md` y `docs/MANIFEST.md`; README/Symphony docs enlazan las nuevas fuentes.
- Se corrigió de forma explícita la semántica MinIO: `STAGER_BUCKET=deploy` y `object_key=worker/sqx/...`; `deploy/worker/...` queda sólo para campos legacy consumidos por `mc`.
- Se creó [[Stager - Symphony Publisher Integration]] como proyecto `owner: agent`, con baseline `symphony@9612f83`, plan F0–F5, manifest objetivo, Allowed Files, tests, MinIO/shadow, rollback y evidencia exigida.
- Se creó [[2026-08-08-stager-deployment-system]] como backlog `seed` para targets/scopes/control plane futuro, con señales estrictas de promoción.
- [[Echo Forge]] recibió una única tarea puente To Do para la implementación futura.

## Decisiones preservadas

- No rediseñar Stager antes de integrar publisher, MinIO real y shadow Linux.
- Un solo deployer watcher publica ambas plataformas; no dos publishers compitiendo por el manifest.
- Symphony usa Linux+Windows como default de release completa inicial; esto no se convierte en invariante del core Stager.
- Publisher integration termina antes de quiesce/launcher/SCM y no hace cutover.

## Evidencia

- Discovery focalizado contra Symphony branch `feature/feat-sqx-mt5-pipeline-artifacts`, HEAD `9612f83`.
- Cambio ajeno `deployer_screen.log` documentado como intocable.
- Lint de application, idea, proyectos y parent: ERROR=0, WARN=0.
- Código Symphony no fue modificado.

## Próximo paso

- Iniciar [[Stager - Symphony Publisher Integration]] por G0 SDD y gate de arquitectura; luego ejecutar F1–F5 en orden.
