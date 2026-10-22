---
type: change_log
schema_version: 1
scope: session
created: "2026-10-22"
updated: "2026-10-22"
area: "[[Echo]]"
project: "[[Echo — Producto Integrado]]"
application:
entities:
  - "[[Echo — Producto Integrado]]"
related:
  - "[[F — Decision Register]]"
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

# Echo — rama runtime única y migración posterior de estrategias

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):** `10-projects/Echo/The Lab/F — Decision Register.md`; `10-projects/Echo/The Lab/V4 — Shot 2/0 — Submanager State.md`; `10-projects/Echo/Echo — Producto Integrado.md`.

## Motivo

- El Owner aclaró el 2026-10-22 que la evolución correcta se desarrolla **solamente** en la rama runtime de Echo; los branches anteriores de backtester están desactualizados y sus estrategias se migrarán a ese motor sólo después de finalizar la extracción en curso.

## Fuentes usadas

- Indicación explícita del Owner en la conversación actual.
- Decision Register D09–D23 y handoff primario anterior.
- GitHub: `feature/ef-runtime-pools` HEAD `2ee61791` verificado, referencia móvil.

## Resolución aplicada

- Nueva ratificación D24 en Decision Register: runtime como única rama base, backtester legacy fuera del programa, migración posterior a la extracción.
- Handoff primario y proyecto Echo enlazan D24 y descartan interpretación de dos baselines; se preserva la evidencia histórica de LAB V4.
- No se modifica el alcance de los cuatro shots ni se anulan las decisiones D09–D23; se elimina la obligación de reconciliar ramas obsoletas.

## Validación

- Cambio documental dirigido y sin escritura de código de producto; contenido de los tres archivos y log a verificar tras commit en `master`.
- Sin pruebas de runtime, deployments, merges ni ejecuciones de backtester.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos ni paths absolutos de máquinas.

## Rollback

- Revertir el commit documental si el Owner cambia la decisión; no hay cambios de producto.
