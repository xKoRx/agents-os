---
type: change_log
schema_version: 1
scope: session
created: "2026-09-25"
updated: "2026-09-25"
area:
project:
application:
entities: []
related: []
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

# 2026-09-25 — Nueva skill echo-prod-deploy (owner-gated)

## Cambios

- **Creada** `30-resources/agents/skills/echo-prod-deploy/SKILL.md`: despliegue autorizado de Echo a PROD (BD .220, ETCD production, Hasura .48, deploy-prod.sh en .71, front nginx) con orden validado, verificación física y rollback.
- **Registrada** en el catálogo federado de `80-agents/skills/INDEX.md` (16→17) con cuándo cargar.
- Trigger boundary owner-gated por mandato del owner: sólo carga/ejecuta ante pedido explícito de usar la skill; cada corrida exige autorización + secretos propios (Trigger Guard + Hard Rules).

## Contenido clave

- Orden validado en el rollout real 2026-09-25 (SHA 372af59a): BD delta + suplementos certificados → seed/convergencia ETCD → Hasura merge aditivo (sin metadata apply directo; strip role admin; wrapper version:2; sólo source echo_prod) → builds v3/bin → deploy-prod.sh scopes core→gateway→lab-worker→front → verificación de puertos/healths/auth/GraphQL/lab.
- Failure modes codificados: crash-loop de echo-functions nuevo (namespace development + puerto 9090), event_triggers fuera del repo, tokens desalineados por rsync, seed tests que rompen password ETCD (4aad647b pendiente), lab_curves=0 correcto sin historia.

## Activación (3 casos)

- Positiva: owner dice "usa la skill echo-prod-deploy para pasar la versión X a prod" → aplica.
- Negativa: owner pide auditoría de PROD → no aplica (→ echo-production-operational-audit).
- Adyacente: owner pide trabajo DEV/despliegue DEV → no aplica (Environment Contract; PROD nunca fallback).
