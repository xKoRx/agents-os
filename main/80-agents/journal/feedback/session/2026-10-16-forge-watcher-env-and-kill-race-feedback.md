---
type: session_feedback
schema_version: 1
created: "2026-10-16"
updated: "2026-10-16"
area: "[[Aranea]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[aranea-agent-dev]]"
related:
  - "[[forge-wave-dispatch]]"
severity: high
category: process
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
---

# Feedback — carrera y scope del watcher candidate-local (2 identidades quemadas en 8 minutos)

**Qué pasó (2026-10-16, FLOW_EXAMPLE_2):** dos despachos consecutivos del mismo spec fueron consumidos por watchers en scope equivocado y quemaron dos identidades de wave (`NDX_flow_example_2_v1_w1/_w2`) sin ejecutar task alguna: (1) el watcher se lanzó sin el prefijo `ENV=production` de la línea canónica de [[forge-wave-dispatch]] §3 → cargó ETCD development → despachó a Temporal `sqx-dev`, namespace sin pollers ("Workflow iniciado exitosamente" en su log era mentira operativa); (2) al corregir, `screen -S X -X quit` no mató el pipeline hijo (`sqx-watcher | tee`) de inmediato: el watcher viejo (dev) sobrevivió lo justo para consumir el paquete recién empacado y quemar la segunda identidad.

**Por qué importa:** la identidad del FlowRun se deriva de `{instrument}_{strategy}_{version}_w{wave}` y es única para siempre aunque el run termine CANCELLED/FAILED; además un CancelWorkflow no alcanza a un workflow en un namespace sin pollers (el cancel viaja como workflow task) — hay que TERMINATE server-side. El costo fue silencioso: logs verdes, flota intacta, identidades quemadas.

**Lección accionable (candidata a la skill si se repite):** (1) el launch del watcher se copia LITERAL de la skill (`ENV=production screen -dmLS …`) y antes de despachar se verifica en su log `temporal.namespace: sqx-prop` + `env: production`; (2) tras matar un watcher, verificar con `pgrep -af sqx-watcher` que NO queda ningún proceso antes de re-empacar `input/` — el patrón screen|tee deja huérfanos; (3) todo paquete consumido por un watcher fuera de scope se trata como identidad quemada aunque el log diga éxito.

**No repetir:** confiar en el "éxito" del log del watcher sin corroborar namespace; re-empacar input inmediatamente después de un kill de screen.
