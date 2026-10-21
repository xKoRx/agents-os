---
type: change_log
schema_version: 1
scope: project
created: 2026-10-21
updated: 2026-10-21
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
entities:
  - "[[Echo Futures — Optimización de Campañas]]"
related: []
aliases: []
confidence: verified
load_policy: manual
indexable: true
index_priority: low
tags:
  - kind/change-log
  - area/echo
---

# Change log — R01 ejecución histórica del laboratorio (lanzamiento, D1, supervisor)

- `10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md`: bitácora R01 (autorización `RESEARCH_EXECUTION_AUTHORIZED_R01`, congelamiento en `/home/kor/echo-work/runs/R01-HIST-20261021/` con binario sellado `8158ddc1…/00f0f5d1…` reutilizado por delta Go vacío, preparación 89/89 con recibo, defecto D1 del motor con repro en dos binarios y alcance SG detenido como ENGINE_BLOCKED_D1, brazo NATIVE en dispatcher de 5 workers, supervisor cron `automation-ed3e89fa-69d5-4f66-82b3-56b944f5feef`).
- Run root (fuera de Git, con hashes): `DEFECT-D1.md` (repro/ causa raíz/trazas), `prepare-receipt.json` (89 filas), `all26-plan.json` + `manifest-all26-hist-R01.json`, `r01-dispatch.log`, `r01-util.jsonl`, `lab*/` intentos byte-intactos, entregables en `deliverables/` al cierre.
- Repo `xKoRx/echo` sin cambios de código en esta fase (sólo lectura del árbol `d641156f`; builds de diagnóstico en `tmp-r01`, árbol revertido y limpio). El commit de entregables compactos en `correction/s04/lab-r01/` queda para el cierre del supervisor.
- Supervisor: automatización `automation-ed3e89fa-69d5-4f66-82b3-56b944f5feef` (cada 20 min) continua esta misma sesión; cierre de sesión ejecutor autorizado ocurre al final del ciclo.
