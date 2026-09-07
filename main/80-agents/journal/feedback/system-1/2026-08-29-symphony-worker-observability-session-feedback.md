---
type: feedback
schema_version: 1
scope: session
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]]"
aliases: []
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# 2026-08-29-symphony-worker-observability-session-feedback

## Gap

- No existe canal no-interactivo desde la máquina del operador para demostrar la release efectiva por worker: SSH a los hosts es sólo password (sin key), el Loki de `192.168.31.60:3100` no recibe streams de `symphony-worker`/stager, y la key etcd `version` es estática (`0.0.21`) así que `app.version` en telemetría no identifica release.
- La rotación de Kronos Linux (stager) no ocurrió en ~2h tras publicar el manifest; sin acceso al host no se distingue stager caído, timer lento o runner sin reinicio.

## Pain Pattern Candidate

- Las certificaciones E2E dependen de evidencia de runtime por host que hoy exige sesión interactiva; formalizar un endpoint/readout de versión por worker (o envío real de logs de worker a Loki) cerraría el gap.

## Acción sugerida

- En el próximo ciclo de plataforma: promtail real por worker hacia Loki o `GET /version` en el worker; y documentar el password/credencial de observación en el mecanismo canónico de despliegue (sin secretos en el vault).
