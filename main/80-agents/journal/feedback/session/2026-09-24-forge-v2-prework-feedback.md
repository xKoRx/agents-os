---
type: session_feedback
schema_version: 1
created: "2026-09-24"
updated: "2026-09-24"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
severity: medium
category: environment
load_policy: manual
indexable: false
tags:
  - kind/feedback
  - scope/session
---

# Feedback — Prework Forge V2 ambiente (2026-09-24)

## Observaciones

1. **`run_watcher.sh` del repo symphony cae por defecto a `ENV=production`.** El default `${ENV:-production}` convierte un olvido de exportar ENV en operaciones contra la flota PROD (namespace `sqx`). En esta sesión se operó siempre con `ENV=development` explícito; sugerencia: cambiar el default a `development` o fail-closed si ENV no viene seteada (cambio de producto → owner, registrado como finding, no corregido aquí).
2. **La config ETCD DEV del watcher estaba rota respecto del worker DEV** (`temporal/namespace=sqx` y `sqx/task_queue=sqx-dev-queue` vs worker `sqx-dev`/`sqx-main-queue`): cualquier watcher DEV habría despachado al namespace de la flota PROD. Corregido en esta sesión con rollback documentado (contract §5.8). Recomendación: un chequeo de coherencia watcher/worker (namespace+cola) en el bootstrap de ambos binarios, fail-closed.
3. **MCP etcd es read-only** y no existe `etcdctl`/`mc`/`java` en Daedalus: toda escritura ETCD/MinIO/PG y la cancelación Temporal requirieron helpers Go desechables dentro del módulo del repo (patrón `di.InitSelective`, 20–40 líneas c/u, creados y eliminados en la misma sesión). Para la próxima sesión que deba operar: el patrón funciona offline y no ensucia el repo, pero si estas operaciones se repiten conviene un único helper `sqx/tools/opshelper` autorizado (decisión owner) en vez de recrear desechables.
4. **Mongo MCP (`aranea-mongo-forge-ro/rw`) devolvió `session not found`** en todos los intentos; no fue bloqueante (el smoke watcher/worker no consume Mongo), pero la reachability de Mongo DEV `forge` quedó sin demostrar en esta sesión.

## Lo que funcionó bien

- El worker valida `sqcli` al arranque y falla cerrado: el blocker de SQX quedó demostrado con el binario real, sin necesidad de mocks.
- La cola `sqx-main-queue` en `sqx-dev` con 0 pollers ajenos es la prueba de aislamiento más simple y contundente: namespace Temporal separa DEV de la flota por construcción.
- Los logs JSON estructurados del SDK hicieron verificable cada paso del pipeline sin adjuntar configuración.
