---
type: change_log
schema_version: 1
scope: project
created: "2026-08-14"
updated: "2026-08-14"
area: "[[Echo]]"
project: "[[Echo Forge - Optimización de Latencia WFM Exporter]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Symphony]]"
related:
  - "[[2026-08-14-echo-forge-one-vm-one-worker-one-task]]"
  - "[[2026-07-31-task-local-dirs-input-output-only]]"
  - "[[2026-08-14-echo-forge-wfm-exporter-performance-agent-project]]"
aliases:
  - Corrección arquitectura serial WFM exporter
confidence: verified
source_session: owner-correction-2026-08-14
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/project
  - change/project
  - area/echo
---

# 2026-08-14-echo-forge-serial-worker-invariant-plan-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution + updated + created
- **Archivo(s):**
  - `80-agents/memory/public/decision/symphony/2026-08-14-echo-forge-one-vm-one-worker-one-task.md`
  - `80-agents/memory/public/decision/symphony/2026-07-31-task-local-dirs-input-output-only.md`
  - `30-resources/applications/echo-forge.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Optimización de Latencia WFM Exporter.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - `80-agents/journal/sessions/2026-08-14-echo-forge-wfm-exporter-distributed-plan-summary.md`
  - `80-agents/journal/logs/2026-08-14-echo-forge-wfm-exporter-performance-agent-project.md`

## Motivo

- Corregir una propuesta que confundió el fan-out entre VMs con concurrencia dentro de un worker e incorporó locks, scopes y decisiones de orquestación no solicitadas.
- Dejar durable y visible la regla confirmada por el owner: `1 VM = 1 worker = 1 task`.

## Fuentes usadas

- Confirmación explícita del owner del 2026-08-14.
- [[2026-07-31-task-local-dirs-input-output-only]], que ya documentaba `MaxConcurrentActivityExecutionSize: 1` y serialización por host.
- [[Echo Forge - Trade List Export Contrato Remoto]], D10, que aplica cleanup seguro sin locks bajo el mismo contrato.

## Resolución aplicada

- Se creó [[2026-08-14-echo-forge-one-vm-one-worker-one-task]] como decisión canónica, crítica y cargable con la aplicación.
- Se hizo visible la invariante en [[echo-forge]] y se enlazó desde la decisión previa de directorios locales.
- Se reemplazó el plan WFM por seis fases acotadas: SPEC, PLAN, fix de doble ejecución, una estrategia por task, heartbeat contextual y verificación.
- Se retiraron como requisitos locks, scopes/hashes, layout MinIO nuevo, sort/dedupe, nuevas semánticas de fan-in/retry/fallo, identidad canónica inventada, OTel y canary multi-worker obligatorio.
- Se marcaron summary y change log anteriores como supersedidos donde contradecían la arquitectura.

## Validación

- `validate_plan.py`: PASS con `phases=6`, `gates=6`, `dispatches=6`, `local_refs=2`, sin errores ni warnings.
- Lint AGENTS OS strict sobre las ocho notas creadas/modificadas: `ERROR=0 WARN=0`.
- Revisión del plan: la única arquitectura de concurrencia declarada es serial por worker; locks, scopes, layouts y cambios de fan-in aparecen únicamente como alcance prohibido/supersedido.
- `graphify-obsidian update`: PASS; índice regenerado con `61996 nodes / 132937 edges / 2743 communities`.
- Symphony no fue modificado.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar las notas modificadas y retirar la decisión nueva solo si el owner cambia explícitamente la arquitectura de concurrencia del worker. No hay rollback de código porque Symphony no fue modificado.
